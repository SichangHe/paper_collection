                                           Vibe Coding in Practice: Motivations, Challenges, and a Future
                                                        Outlook – a Grey Literature Review
                                                             Ahmed Fawzy                                                      Amjed Tahir                                    Kelly Blincoe
                                                     Massey University                                                     Massey University                          The University of Auckland
                                                       New Zealand                                                           New Zealand                                      New Zealand
                                              ahmed.mohamed.6@uni.massey.ac.nz                                           a.tahir@massey.ac.nz                          k.blincoe@auckland.ac.nz

                                         Abstract                                                                                        1    Introduction
                                         AI code generation tools are transforming software development,                                 Recent progress in large language models (LLMs), accessible through
                                         especially for novice and non-software developers, by enabling                                  AI code generation tools, such as GitHub Copilot and ChatGPT,
arXiv:2510.00328v1 [cs.SE] 30 Sep 2025




                                         them to write code and build applications faster and with little to                             is rapidly transforming software development. These tools enable
                                         no human intervention. Vibe coding is the practice where users rely                             developers to describe functionality in natural language and receive
                                         on AI code generation tools through intuition and trial-and-error                               executable code, thereby speeding up routine work and lowering
                                         without necessarily understanding the underlying code. Despite                                  the barrier to entry for individuals with limited programming expe-
                                         widespread adoption, no research has systematically investigated                                rience [20, 46, 53]. With the use of these tools, even people without
                                         why users engage in vibe coding, what they experience while doing                               any formal training are increasingly able to develop functional ap-
                                         so, and how they approach quality assurance (QA) and perceive the                               plications [14]. This change represents a broader shift in developer
                                         quality of the AI-generated code.                                                               roles, which now involve orchestrating, supervising, and integrat-
                                            To this end, we conduct a systematic grey literature review of 101                           ing rather than writing every line of code [39, 58]. However, while
                                         practitioner sources, extracting 518 firsthand behavioral accounts                              these tools are transforming how software is created, less is known
                                         about vibe coding practices, challenges, and limitations. Our anal-                             about the new coding practices emerging from their everyday use.
                                         ysis reveals a speed–quality trade-off paradox, where vibe coders                                   Within the wave of rapid adoption of AI code generation tools, a
                                         are motivated by speed and accessibility, often experiencing rapid                              new practice known as vibe coding has emerged. Coined by Karpa-
                                         “instant success and flow”, yet most perceive the resulting code as                             thy in 2025 [26], vibe coding is a new programming approach where
                                         fast but flawed. QA practices are frequently overlooked, with many                              users employ AI code generation tools to write code by describing
                                         skipping testing, relying on the models’ or tools’ outputs without                              their desired outcome (in natural language) without fully under-
                                         modification, or delegating checks back to the AI code generation                               standing the AI-generated code. For example, a recent report noted
                                         tools. This creates a new class of vulnerable software developers,                              that 25% of Y Combinator’s Winter 2025 startups had codebases
                                         particularly those who build a product but are unable to debug it                               written almost entirely by AI code generation tools, illustrating how
                                         when issues arise.                                                                              quickly this practice is spreading [37]. In contrast to AI-assisted
                                            We argue that vibe coding lowers barriers and accelerates pro-                               programming, vibe coding prioritizes speed and experimentation
                                         totyping, but at the cost of reliability and maintainability. These                             over understanding.
                                         insights carry implications for tool designers and software devel-                                  In this paper, we define vibe coding as the practice of using AI
                                         opment teams. Understanding how vibe coding is practiced today                                  code generation tools to produce software primarily by describing
                                         is crucial for guiding its responsible use and preventing a broader                             goals in natural language and iteratively prompting, while relying
                                         QA crisis in AI-assisted development.                                                           on minimal review of the generated code. The definition is derived
                                                                                                                                         from Karpathy’s original introduction of the term [26] and further
                                         Keywords                                                                                        grounded in how practitioners themselves describe the practice in
                                         Vibe coding, AI-assisted programming, AI-generated code                                         grey literature (e.g., [74]). This definition applies across user groups,
                                                                                                                                         including both professional developers (who may use vibe coding to
                                         ACM Reference Format:                                                                           prototype quickly) and non-software developers (who may attempt
                                         Ahmed Fawzy, Amjed Tahir, and Kelly Blincoe. 2025. Vibe Coding in Prac-                         to build applications without coding knowledge) [12, 75].
                                         tice: Motivations, Challenges, and a Future Outlook – a Grey Literature                             Vibe coding has introduced advantages such as accessibility,
                                         Review. In . ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/                         speed, and creative potential. For example, non-software devel-
                                         nnnnnnn.nnnnnnn                                                                                 opers can now build working applications, and professionals can
                                                                                                                                         explore ideas faster than before [47, 48, 80]. However, prior research
                                         Permission to make digital or hard copies of all or part of this work for personal or           and industry commentary warn of severe limitations. Educational
                                         classroom use is granted without fee provided that copies are not made or distributed           studies show that students often adopt AI-generated code without
                                         for profit or commercial advantage and that copies bear this notice and the full citation
                                         on the first page. Copyrights for components of this work owned by others than the              understanding it, risking poor learning outcomes [20, 53]. Security
                                         author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or          research has demonstrated that AI-generated code frequently con-
                                         republish, to post on servers or to redistribute to lists, requires prior specific permission   tains vulnerabilities [34, 45], that has also been identified across
                                         and/or a fee. Request permissions from permissions@acm.org.
                                         Conference’17, Washington, DC, USA                                                              existing projects [16]. Practitioners have also highlighted risks of
                                         © 2025 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         ACM ISBN 978-x-xxxx-xxxx-x/YYYY/MM
                                         https://doi.org/10.1145/nnnnnnn.nnnnnnn
Conference’17, July 2017, Washington, DC, USA                                                                                         Fawzy et al.


technical debt [12, 74]. These findings suggest that while vibe cod-       grasp the concepts behind the AI-generated code. Sheard et al. [56]
ing lowers barriers and accelerates development, it also introduces        interviewed instructors, many of whom expressed concern that stu-
concerns regarding quality, security, and maintainability.                 dents might submit AI-generated work without understanding it. Zi
   Despite the widespread adoption in practice, there is still no          et al.[79] similarly found that CS1 students struggled to understand
research that systematically examined vibe coding as a distinct            LLM-generated code, with only 32.5% success in comprehension
practice. Existing studies either focus on general AI code genera-         tasks due to unfamiliar coding styles, automation bias, and limited
tion tools use without isolating the intuition-driven trial-and-error      experience. Overall, these findings suggest that while AI code gen-
style that defines vibe coding [28, 30, 46, 66]. To address this gap,      eration tools can support confidence and accessibility, over-reliance
we conduct a systematic grey literature review (GLR) to analyze            may harm learning outcomes [20, 53].
firsthand behavioral accounts of vibe coding documented in blogs,              Other work has examined individuals with no formal program-
forums, media articles, and other publicly available sources. In this      ming training. Feldman and Anderson [14] studied how non-software
review, we attempt to answer the following four research questions:        developers use AI code generation tools to generate working code.
RQ1: What are the motivations behind vibe coding?                          While they were able to produce basic programs, they struggled to
This question examines why users opt to vibe code, delving deeper          articulate their intent in prompts clearly and to verify whether the
into their motivations for choosing to code in this manner (such           resulting AI-generated code was correct. These findings suggest
as speed, ease of use, creativity, learning, or accessibility). We also    that while AI code generation tools open access to new user groups,
explain the contexts in which users find the practice valuable (such       significant barriers remain in effectively prompting and validating
as when rapid prototyping, working on personal projects, or em-            AI outputs.
powering non-software developers).                                             Ferino et al. [15] investigated how junior developers adopt GitHub
RQ2: What is the user experience while vibe coding?                        Copilot, finding that many relied on trial-and-error and accepted
In this question, the focus is on users’ hands-on experiences while        suggestions without full understanding. At the professional level,
vibe coding, exploring what worked well and what went wrong. We            Barke et al. [6] found that experienced developers used AI code
aim to capture how users actually work with AI code generation             generation tools in two main ways: (1) to accelerate code they
tools during vibe coding.                                                  already knew how to write, and (2) to explore unfamiliar ideas,
RQ3: What is the perception of the AI-generated code quality               while generally testing results carefully. Vaithilingam et al. [66]
with vibe coding ?                                                         found that developers enjoyed using Copilot but often struggled to
The question investigates how users perceive the outputs they              fix generated code when bugs appeared. Peng et al. [46] reported
produce with AI code generation tools. It captures how users judge         productivity benefits, particularly for less experienced developers,
the usefulness and reliability of the code they obtain.                    though the quality of AI-generated code was not evaluated. To-
RQ4: What quality assurance (QA) practices are applied when                gether, these studies suggest that developer experience plays a role
vibe coding?                                                               in how carefully AI code generation tools are used.
Here we explore how users check or manage the quality of AI-                   In prompt engineering, Kruse et al. [30] investigated how devel-
generated code, and whether they carefully review it before ac-            opers craft prompts for code generation and how their experience
ceptance, or instead fully trust the output without verifying its          influenced outcomes. While this sheds light on the importance of
correctness and quality.                                                   prompt design, it does not specifically examine vibe coding, where
   By synthesizing insights from diverse practitioners and settings,       trial-and-error prompting and intuition often dominate.
our study offers a grounded account of how vibe coding is practiced            Several studies highlight risks associated with adopting AI code
in real-world contexts. We find that users are primarily motivated         generation tools without sufficient code review. Pearce et al. [45]
by speed and accessibility, but their reliance on minimal review           found that approximately 40% of Copilot outputs (out of 1,689 pro-
often results in fragile or error-prone code. These insights offer         grams) contained security vulnerabilities. Majdinasab et al. [34]
implications for tool designers and software teams (e.g., designing        showed that even with additional safety layers, insecure code was
tools that encourage review and validation rather than uncritical          still frequently produced. Fu et al. [16] further identified security
acceptance of AI-generated code).                                          weaknesses in AI-generated code across GitHub projects. These
                                                                           findings show that while AI code generation tools increase accessi-
                                                                           bility and speed, the resulting code may introduce significant risks
2    Related Work                                                          if not carefully checked.
Research on AI code generation tools has grown rapidly, focusing               Beyond technical outcomes, some studies explore how devel-
on different user groups and concerns. While these studies provide         opers perceive the role of AI code generation tools. Kuhail et al.
valuable insights, no direct investigation has been done on vibe           [31] examined developers’ views on ChatGPT, focusing on job se-
coding as a distinct practice.                                             curity, role changes, and whether AI would replace or augment
   Some studies have examined how students and novices use AI              programming work. Weisz et al. [70] studied IBM’s use of an AI
code generation tools in learning contexts. Prather et al. [47, 48]        code assistant (watsonx Code Assistant) and found that, although
found that students often accept AI suggestions without deeply             many developers reported productivity gains, these benefits were
considering or understanding them, leading to confusion when               uneven and often raised concerns about authorship, responsibility,
errors arise. Zviel-Girshin et al. [80] studied a full class of beginner   and loss of skills. While relevant to understanding adoption, this
software developers and reported that while students felt more             research does not investigate how developers actually check or test
confident using AI code generation tools, they often did not fully         AI-generated code in practice.
Vibe Coding in Practice                                                                                Conference’17, July 2017, Washington, DC, USA


   In summary, prior research has examined educational contexts,
non-software developers, juniors, professionals, prompting, secu-
rity, and developer perceptions. However, none directly addresses
vibe coding as an intuition-driven trial-and-error practice distinct
from general AI-assisted software development. This gap moti-
vates our GLR, which synthesizes firsthand accounts of vibe coding
behaviors across diverse user groups.


3     Methodology
Grey literature encompasses sources that are not published in tra-
ditional peer-reviewed venues, including blogs, technical reports,
and web articles. In software engineering, practitioners often share
their experiences and practices via these online channels rather
than academic journals [24, 25].
    Several studies have demonstrated that GL is becoming a signif-
icant source of evidence in SE. For example, a review found that
approximately one in five secondary studies already utilize GL, as
it incorporates perspectives from real practitioners that may not
be evident in peer-reviewed research [24]. Kamei et al. [25] also
argue that GL reviews are useful because they capture insights from
materials that practitioners themselves read (like blog posts and
technical reports).


3.1     Search Strategy
In conducting this review, we have closely followed the review
guidelines proposed by Garousi et al. [17]. As grey literature is
spread across the web, we used Google as our search engine. Prior
work has shown that Google is particularly effective for discovering
diverse forms of grey literature across blogs, forums, and media
posts [4, 5, 65]. We also applied backward snowballing (following
links and references inside included sources) to find further relevant
sources (see Section 3.2.5). We discuss our search string develop-
ment, data extraction, and analysis steps below. Figure 1 outlines
the full steps of the GL process.


3.2     Search String
We followed an iterative, multi-stage process to develop an effective
search string. Our goal is to maximize both recall and practical                        Figure 1: Grey Literature Process
relevance. We explain our string development steps below:

3.2.1 Stage 1: Problem Framing and Concept Definition. Vibe cod-             (“AI-assisted programming” OR “AI code generation” OR
ing refers to situations where software developers and other users           “prompt-based programming” OR “LLM-assisted develop-
(e.g., novices / non-software developers) rely on AI code generation         ment”) + tool names (e.g., “ChatGPT” or “Copilot”) + role
tools based on intuition and trial and error, often without a thor-          (e.g., “developer” OR “student” OR “non-programmer”)
ough understanding of the code or conducting a rigorous review
and testing. This distinguishes it from more structured or expert-          However, this term combination had limited success. The search
guided AI-assisted programming. Therefore, our search needed to          retrieved mostly unrelated sources (e.g., more technical AI articles,
focus on behavioral indicators and practitioner phrasing, not just       promotional content, or conceptual content) and missed the primary
technical descriptions.                                                  target of our GLR. The first 100 results (a manageable representation
                                                                         of relevant grey literature [5, 9]) of this stage were screened against
3.2.2 Stage 2: Initial Candidate Terms. We began with domain-            our inclusion and exclusion criteria (see Section 3.3), but since they
informed candidate terms commonly seen in early articles, consist-       did not contain firsthand evidence of vibe coding behaviors, they
ing of the following terms:                                              were excluded (screened 100, 8% relevant). This stage nevertheless
Conference’17, July 2017, Washington, DC, USA                                                                                           Fawzy et al.


helped us refine our search strategy by clarifying which terminolo-        experiences using LLMs to vibe code [73]; and Maxime Najim, An
gies were too broad or non-practitioner-focused.                           experienced software engineer, whose reflective post documented
                                                                           the intentional and risky use of vibe coding in practice [38]; and
3.2.3 Stage 3: Pivot to Practitioner Language. We then shifted focus
                                                                           Tyler Shields, an early practitioner account that described vibe
to how practitioners describe AI coding tools in everyday usage. We
                                                                           coding as relying entirely on LLMs without verification [57]. This
noticed that several terms are frequently used, including: “coding
                                                                           validation process increased our confidence that the final search
with AI”, “AI writes code”, “prompting for code”, “using AI to code”,
                                                                           string would capture the full range of behavioral evidence needed to
“programming with an AI assistant”. We also incorporated the term
                                                                           address our research questions, and was aligned with the guidelines
“vibe coding” directly, as it had become widely adopted following
                                                                           of Garousi et al. [17].
its introduction in 2025 [26]. In this stage, we screened 100 sources,
with approximately 50% considered relevant.
                                                                           3.3     Inclusion and Exclusion Criteria
3.2.4 Stage 4: Iterative Expansion and Saturation. As part of an           We applied a set of inclusion and exclusion criteria. Our inclusion
iterative design and test process, we expanded the candidate string        criteria are:
to capture semantically adjacent behaviors. We added terms such as
“LLM-assisted coding”, “AI programming tool”, and “AI pair                       • English-language sources
programmer”, which returned relatively few additional relevant                   • Sources published between 2022 and 2025
hits ( 12%) when we screened 100 results, based on their appearance              • Relevance to the research questions
in pilot searches and known grey literature sources (Quasi-Gold                  • Identifiable author or publishing entity
Standard see Section 3.2.6). Each term was tested for recall and                 • Publicly accessible full text
specificity using Google search, and retained only if it increased               • Behavioral evidence of vibe coding, including: AI-generated
the relevance of retrieved documents.                                              code used as-is or with light edits, prompting and reprompt-
                                                                                   ing, minimal or no testing, review, or improvement
3.2.5 Stage 5: Final Search String. The final version of the search              • Critical or negative reflections are accepted if based on first-
string retrieved all items in the quasi-gold standard set and pro-                 hand experience with vibe coding
duced strong recall without adding excessive unnecessary informa-
tion. We initially screened the first 100 results of the final search         We excluded material that met any of the following exclusion
string, then continued until we reached thematic saturation (ad-           criteria:
ditional screening no longer surfaced substantially new related                  • Duplicates or mirrored content
sources). Backward reference (Snowballing) chaining was applied                  • Irrelevant topics or purely technical focus
to the first 100 results of the final search string retrieved sources,           • Promotional content
following the guidelines of Wohlin et al [77]. This involved tracing             • Undated or anonymous sources
hyperlinks, named references, or cited resources within blogs and                • Tool descriptions without user insight (e.g., Copilot/ChatGPT
forums (e.g., [73, 74],[41, 42]). This leads to a total of 154 sources.            feature summaries)
The String:                                                                      • Very short content (e.g., tweets or headlines without com-
                                                                                   mentary)
    “vibe coding” OR “coding with AI” OR “AI writes code”                        • Abstract speculation or general opinions unsupported by
    OR “AI code assistant” OR “LLM-assisted coding” OR “AI                         observable vibe coding actions such as prompting, accepting,
    programming tool” OR “prompting for code” OR “using                            skipping QA.
    AI to code” OR “AI pair programmer” OR “programming                          • No firsthand behavior involving vibe coding, such as:
    with an AI assistant”                                                          – No prompting or AI code generation
                                                                                   – No code acceptance or editing
                                                                                   – Experienced developers applying critical oversight with-
3.2.6 Stage 6: Quasi-Gold Standard Validation and Pilot Search. To
                                                                                      out skipping QA
ensure the effectiveness of the final string, we employed a quasi-gold
standard evaluation approach. Additionally, this involved testing
each search iteration against a curated set of known relevant grey         3.4     Quality Assessment
literature sources, posts we had previously identified as clear exam-      The quality assessments were mainly conducted by the first author,
ples of vibe coding behavior. These sources were identified during         with each source scored from 0 to 3 across five quality dimensions,
our pilot search stages and met all inclusion criteria (see Section 3.3)   following Garousi et al.’s GL guidelines [17] with a maximum score
with high quality scores (see Section 3.4). The quasi-gold set in-         of 15. These five quality criteria (Authority, Evidence, Objectivity,
cluded firsthand accounts involving AI prompting, minimal over-            Currency, and Purpose) were adapted from Garousi et al.’s [17]
sight, trial-and-error acceptance, or skipped QA practices. Specif-        framework for grey literature quality assessment, which has been
ically, it comprised: Andrej Karpathy, who coined the term vibe            widely adopted in software engineering GLR [24, 59]. To increase
coding in early 2025 and demonstrated it by developing a restaurant        reliability, a subset of sources was cross-validated by another co-
menu application using this approach [27], including clear experi-         author. Sources scoring ≥ 10 were retained for further analysis. The
ential reflections on the process and deployment; Simon Willison,          full scoring descriptions, including the results and justification for
who emphasized that not all AI-assisted programming is vibe cod-           each article quality score, have been included in our dataset [13].
ing [74], and described his own prototyping workflow and personal          Scoring Criteria:
Vibe Coding in Practice                                                                                   Conference’17, July 2017, Washington, DC, USA


      • Authority: Author identity and credibility (e.g., known de-       3.7     Data Analysis
        veloper, reputable organization)                                  We used thematic analysis to analyze the extracted behavioral units
      • Evidence: Use of examples, rationale, or empirical support        of grey literature data, following the procedures recommended
      • Objectivity: Neutral and balanced presentation of ideas           by Braun & Clarke [8]. Behavioral insights were organized and
      • Currency: Published between 2022 and 2025                         coded, guided by our research questions, according to patterns in
      • Purpose: Intended to inform, reflect, or explain (not promote     motivations, experiences, perceptions of code quality, and quality
        or market)                                                        assurance practices related to vibe coding. The data analysis steps,
                                                                          including theme development, were mainly conducted by the first
3.5     Data Filtration:                                                  author. To increase reliability, reviews and discussions with other
Our search string retrieved 154 grey literature sources (e.g., blog       co-authors were carried out. We followed a set of steps to develop
posts, online articles, and technical reports), of which 101 met          the themes, explained below:
our inclusion criteria and quality thresholds. All other 53 sources
were excluded. Among the exclusions, 40 sources were excluded be-               • Familiarization with the Data: We read through all the
cause they did not reach the minimum quality threshold (QA score                  extracted 518 behavioral units multiple times to understand
≥ 10/15), and 13 were excluded based on the inclusion and exclu-                  patterns. For example, “I just trust it works.” [51] and “They’re
sion criteria (see Section 3.3). For example, [71] (a Wikipedia entry),           accepting the responses in a very trusting way.” [22] suggests
[43] (a promotional Replit blog post), and [60] (a satirical news                 a common pattern of uncritical trust in AI-generated code
commentary in The Register) were excluded for not meeting our                     without any checks.
quality thresholds for behavioral detail/provenance. By contrast,               • Generating Initial Codes: We then labeled each behavioral
[23] (an explanatory article in The Conversation), [2] (a Cloud-                  unit with a potential theme. For example, “Copy and paste
flare vendor learning page), and [3] (a Google Cloud conceptual                   them in. . . usually, that fixes it.” we labeled it as “Reprompting
overview) were likewise excluded under our inclusion/exclusion cri-               Instead of Debugging”. We set the potential theme “Speed” to
teria and for lacking firsthand behavioral evidence (no prompting,                “Alex Finn famously created a Call of Duty style shooter game
code acceptance, or QA evidence).                                                 in just 87 minutes using AI tools.” [49]. These initial codes
                                                                                  summarize the behaviors, but they do not group them yet.
3.6     Behavioral Unit Extraction                                              • Searching for Themes: We grouped similar initial codes
To move from raw articles to analyzable data, we systematically                   (potential themes) into larger candidate themes. This means
extracted 518 behavioral units from the 101 included sources. A                   we started clustering behaviors that reflected the same idea
behavioral unit is a single coded instance that captures something                or pattern. The potential themes such as “Uncritical Trust”
relevant to the RQs. This may be a practitioner describing their own              [68], “False Confidence” [19], and “Uncritical Security Trust”
vibe coding, or an author/reporter documenting or commenting                      [18] were grouped into the final theme “Uncritical Trust”.
on vibe coding practices. Extraction was performed at the quote                 • Reviewing Themes: We examined whether our potential
level rather than the article level, coding each instance of behavior             themes were consistent throughout the entire dataset. Some-
(motivation, experience, perceptions of code quality, or QA practice)             times we split, rename, or reassign behaviors to better-fitting
separately. This ensured that multiple distinct behaviors within the              themes. For example, some quotes originally coded as “Skipped
same article (e.g., a motivation to save time and a later description             QA” were actually different in behavior. For instance, “Busi-
of skipping QA) were each represented as separate units in our                    nesses often trust AI-generated code uncritically, leading to
dataset.                                                                          vulnerabilities and technical debt’’ [49] were reassigned to
   Each behavioral unit was extracted, classified and recorded in                 the final theme “Uncritical Trust” as they choose to trust
an external spreadsheet with the following fields:                                without understanding.
      • Verbatim Quote: the exact wording from the source.                      • Defining and Naming The Final Themes: For each theme
      • Attribution: who expressed the behavior (author or quoted                 we identified, we wrote a clear description that explained
        user)                                                                     what the theme represented and how it was different from
      • RQ Mapping: whether the unit described motivation (RQ1),                  the other themes. A consolidated overview of all theme defi-
        experience (RQ2), perceptions of code quality (RQ3), or QA                nitions is provided in Table 1.
        practice.                                                               • Producing the Report: Finally, we prepared the results
      • Interpretation: a short analytic summary of what the be-                  for presentation. Each final theme is reported in Section 4
        havior revealed                                                           together with: (its definition, frequency statistics, and illus-
      • Metadata: user type, tool mentioned, vibe coding definition               trative explanations).
        (if given), and notes
Behavioral unit extraction was conducted mainly by the first author.         Table 1 summarizes the final theme definitions used to code be-
To increase reliability, a subset of units was cross-validated by         havioral units across RQ1 (motivations), RQ2 (experiences), RQ3
another co-author. This process yielded 140 motivation units (RQ1),       (perceptions of AI-generated code quality) and RQ4 (quality as-
132 experience units (RQ2), 114 perception of code quality units          surance practices). Figure 2 displays all the vibe coding behavior
(RQ3) and 132 QA practice units (RQ4). These units formed the raw         themes we have constructed, along with their corresponding fre-
data corpus for our subsequent thematic analysis (Section 3.7).           quencies.
Conference’17, July 2017, Washington, DC, USA                                                                                                      Fawzy et al.


                                                Table 1: Description of the identified vibe coding themes

 Theme                                  Description
 Motivation for vibe coding (RQ1)
 Speed & Efficiency                     The ability to produce working software much faster, reducing development cycles from weeks to only hours.
 Accessibility & Empowerment            Enabling Non-Software Developers ability to create applications by describing goals in natural language.
 Learning & Experimentation             Using LLM coding models as a tutor or sandbox to explore new coding tools, concepts, and frameworks.
 Creative Exploration                   Turning imaginative or artistic ideas into functional projects with AI support.
 Fast Prototyping                       Quickly assembling MVPs or demos to test feasibility, concepts, or market interest.
 Reducing Mental Effort                 Offloading syntax and boilerplate to AI, easing the developer’s cognitive load.
 Frustration Avoidance                  Bypassing programming pain points e.g., repetitive debugging, setup issues etc.
 Escape Complexity                      Avoiding difficult design or architecture work by delegating detail to AI.
 Curiosity or Play                      Engaging casually with AI for fun, experimentation, or open-ended exploration.
 Experience with vibe coding (RQ2)
 Instant Success & Flow                 Experiencing rapid, seamless progress that creates momentum, leading to satisfaction.
 Prompt Struggle & Iteration            Refining prompts through repeated trial-and-error until usable results appear.
 Code Breakdown or Abandonment          Abandoning projects when AI outputs become too buggy or complex.
 Fun & Creative Satisfaction            Enjoying the excitement of fast software development, though the novelty can fade.
 AI Hallucinations                      Facing false, inaccurate, or misleading code suggestions that look plausible but fail in execution or introduce bugs.
 Confusion or Misunderstanding          Misaligned prompts and outputs causing frustration and loss of trust
 Code Quality Perception (RQ3)
 Fast but Flawed                        Useful for quick tasks but unsuitable for production deployment.
 Fragile or Error-Prone                 Containing hidden bugs, inconsistencies, or potential security risks.
 Sloppy or Low Maintainability          Functional but poorly structured, undocumented, and hard to extend.
 Prototype-Ready Only                   Adequate for demos and proofs-of-concept but not for long-term systems.
 High Quality & Clean                   Actually well-structured, and close to production quality
 Misleading Confidence                  Appearing reliable while concealing deeper flaws, creating false trust.
 QA Practices (RQ4)
 Skipped QA                             Bypassing structured testing or review, relying only on execution success.
 Manual Testing or Edits                Applying systematic checks (manual code reviews) and edits before adopting AI outputs.
 Uncritical Trust                       Accepting AI-generated code without validation or verification, based on the assumption that it works.
 Delegated QA to AI                     Relying on the AI code generation tools to detect and correct its own mistakes.
 Reprompting Instead of Debugging       Feeding errors back into AI code generation tools rather than fixing them manually.
 Run-and-See Validation                 Running code to check if it works, equating success with correctness.
 QA Breakdown or Confusion              Failing to validate the outputs due to complexity or lack of clarity.


4     Results                                                                      Table 2: Distribution of Motivations for Vibe Coding (n=140)
From these 101 sources, we identified 518 behavioral units, which
we coded into the themes defined earlier (see Table 1 and Figure 2),                    Theme                                 Frequency      Percentage
including motivations (140 units, RQ1), experiences (132 units, RQ2),                   Speed & Efficiency                        87             62%
perceptions of code quality (114 units, RQ3), and QA practices (132                     Accessibility & Empowerment               20             14%
units, RQ4).                                                                            Learning & Experimentation                15             11%
   For each RQ, we identified several distinct themes, which are                        Creative Exploration                      8               6%
summarized with definitions in Table 1. Due to space limitations,                       Fast Prototyping                          4               3%
we describe in detail only themes that account for at least 10% of the                  Reducing Mental Effort                    2               1%
behavioral units for that RQ. Less frequent themes are still included                   Frustration Avoidance                     2               1%
in Table 1 and distribution tables (Tables 2–5).                                        Escape Complexity                         1               1%
                                                                                        Curiosity or Play                         1               1%
4.1     Motivations for Vibe Coding (RQ1)
There were 140 behavioral units related to motivation, from which
we identified nine distinct themes through thematic analysis. A
summary of those motivational themes is shown in Table 2. A                        have built over 140k lines of code (LOC) with tests and documen-
distribution of the motivational themes, including their frequencies               tation in just under 15 days using vibe coding practices [50]. This
and percentages, is shown in Table 2.                                              acceleration was valued not only by beginners but also by experi-
Speed & Efficiency: We found that the most common motiva-                          enced developers and even organizations [40]. Across these groups,
tion theme for vibe coding (62%) is speed & efficiency, with vibe                  speed was not just about coding faster; it translated into tangible
coders highlighting rapid development. Practitioners consistently                  productivity outcomes. For instance, one source expects that the
described how AI code generation tools enabled them to produce                     company will reduce manual testing time by 25%, achieve complete
working software in dramatically less time, often hours instead of                 test coverage on projects 20% faster, and fix significantly more bugs
weeks (e.g., [36, 74]). For example, one source reported that they                 early in the development cycle [64].
Vibe Coding in Practice                                                                              Conference’17, July 2017, Washington, DC, USA




                                      Figure 2: The identified themes from the collected sources


Accessibility & Empowerment: Another important motivation               confidence in coding tasks [10, 27]. Even experienced developers
theme (14%) was accessibility and empowerment, where vibe coding        reported using AI code generation tools to familiarize themselves
lowers the barrier to entry for software development. Non-software      with unfamiliar domains or frameworks more efficiently, position-
developers described being able to turn their ideas into functional     ing vibe coding as a complementary way to learn through practice
applications simply by expressing them in natural language to AI        [7, 73].
code generation tools (e.g., [36, 72]). This democratization repre-
sents a major shift in who can participate in software creation:
tasks that once required teams of technical specialists can now be      4.2    Experiences During Vibe Coding (RQ2)
achieved by individuals without programming training. Evidence          There were 132 behavioral units related to experiences, from which
of this appeared not only in personal projects, but also in organiza-   we identified six distinct themes through thematic analysis. A sum-
tional contexts, where analysts and policy staff reported building      mary of these themes is provided in Table 3. A distribution of the
automations or public-facing forms without relying on IT depart-        experience themes, including their frequencies and percentages, is
ments (e.g., [1, 32]). Overall, this theme highlights how vibe coding   shown in Table 3.
is not only about speed but also about expanding access to software     Instant Success & Flow: The most common experience theme
creation for entirely new groups of users.                              (64%) was instant success and flow, where vibe coders described
Learning & Experimentation: A further motivation theme (11%)            the process as fast, easy, and often “Magical.” Practitioners reported
was learning and experimentation, where vibe coding was used as         being able to build working applications in minutes through sim-
both a hands-on tutor and a sandbox for trying out ideas. Practition-   ple conversations with AI code generation tools [29, 54, 55]. This
ers described how experimenting with prompts and outputs helped         immediacy created a sense of addictive momentum, with some de-
them quickly build intuition about what works and what does not         scribing it as a “dopamine hit” when prototypes, QA checks, and
[73]. Vibe coding also enabled users to explore new programming         deployments came together quickly [67]. Accounts ranged from
languages and frameworks without formal training, with novices          developers building complete applications within hours [52] to non-
and career changers reporting that it accelerated their learning and    software developers expressing amazement at creating functional
Conference’17, July 2017, Washington, DC, USA                                                                                        Fawzy et al.


Table 3: Distribution of Experiences During Vibe Coding                   and long-term quality. Vibe coders noted that while AI code genera-
(n=132)                                                                   tion tools could quickly generate most of a solution, the remaining
                                                                          critical work to make code production-ready often became a chal-
  Theme                                         Frequency    Percentage   lenge [55]. They accepted these flaws as an inevitable cost of rapid
                                                                          development, keeping the code as long as it worked but recognizing
  Instant Success & Flow                           85            64%
                                                                          that this created technical debt over time [54].
  Prompt Struggle & Iteration                      17            13%
                                                                          Fragile or Error-Prone: Another common perception (19%) was
  Code Breakdown or Abandonment                    14            11%
                                                                          that AI-generated code is fragile or error-prone, raising concerns
  Fun & Creative Satisfaction                      11             8%
                                                                          about hidden issues. Practitioners cautioned that such code was
  AI Hallucinations                                3              2%
                                                                          often excluded from reviews or security checks, creating the risk
  Confusion or Misunderstanding                    2              2%
                                                                          of undetected vulnerabilities [21]. Others emphasized that while
                                                                          the outputs might appear clean and functional, they could conceal
                                                                          subtle logic errors, performance bottlenecks, or serious security
tools and even cultural translation projects without prior coding         flaws that only become apparent later [62].
expertise [78].
Prompt Struggle & Iteration: Not all experiences were positive. A         4.4    QA Practices in Vibe Coding (RQ4)
common experience (13%) was prompt struggle and iteration, where
                                                                          There were 132 behavioral units related to QA practices, from which
vibe coders needed to refine their instructions repeatedly to achieve
                                                                          we identified seven distinct themes through thematic analysis. A
a satisfactory result. Practitioners described going through cycles
                                                                          distribution of these QA practice themes, including their frequencies
of prompt adjustment and code refinement, with some projects
                                                                          and percentages, is shown in Table 5.
requiring dozens or even hundreds of iterations before the output
was usable [21, 42]. This process highlighted the emergence of            Table 5: Distribution of QA Practices in Vibe Coding (n=132)
prompt engineering skills, where users learned to craft, adapt, and
even collect effective prompts as reusable patterns to improve their
results.                                                                   Theme                                   Frequency     Percentage
Code Breakdown or Abandonment: Another experience theme                    Skipped QA                                  48            36%
(11%) was code breakdown or abandonment, where vibe coding                 Manual Testing or Edits                     38            29%
sessions ended in failure. When AI-generated code produced out-            Uncritical Trust                            24            18%
puts that were too complex, buggy, or inconsistent to fix, some            Delegated QA to AI                          13            10%
practitioners reported giving up on projects altogether rather than        Reprompting Instead of Debugging            6              5%
attempting to debug the code [72]. These breakdowns often oc-              Run-and-See Validation                      2              2%
curred when task complexity exceeded the AI’s ability to generate          QA Breakdown or Confusion                   1              1%
reliable solutions, leading to frustration and project abandonment
[78].                                                                     Skipped QA: The most common QA practice (36%) was skipped
                                                                          QA, where vibe coders accepted AI-generated code without valida-
4.3     Perceptions of the Generated Code’s Quality                       tion. Practitioners reported bypassing traditional testing entirely,
        (RQ3)                                                             for example, they did not write unit or integration tests, perform
There were 114 behavioral units related to perceptions of code qual-      structured reviews, or systematically verify correctness beyond
ity, from which we identified six distinct themes through thematic        simply running the code. instead relying on whether the code exe-
analysis. A distribution of these code quality perception themes,         cuted without errors as a proxy for quality [21]. Even experienced
including their frequencies and percentages, is shown in Table 4.         developers described pasting error messages back into AI code gen-
                                                                          eration tools and letting it generate fixes, rather than debugging or
                                                                          testing the code themselves [36].
  Table 4: Distribution of Perceived Code Quality (n=114)
                                                                          Manual Testing or Edits: The second most common QA prac-
                                                                          tice (29%) was manual testing or edits, where practitioners applied
      Theme                                 Frequency       Percentage    careful quality control to AI-generated code. Some emphasized
      Fast but Flawed                            78            68%        the risks of pushing generated code directly to production, warn-
      Fragile or Error-Prone                     22            19%        ing that without review it could introduce bugs, security issues,
      Sloppy or Low Maintainability              5              4%        or performance problems [40]. Experienced developers described
      Prototype-Ready Only                       5              4%        establishing stricter review protocols, treating every generated
      High Quality & Clean                       3              3%        change as something that needed to be understood and verified,
      Misleading Confidence                      1              1%        often supported by testing and automated checks [38].
                                                                          Uncritical Trust: Another QA practice (18%) was uncritical trust,
                                                                          where vibe coders believed the code worked even without checking
Fast but Flawed: We found that the most common perception                 it. As one source noted, humans tend to place more faith in gen-
of the AI-generated code quality theme is “fast but flawed” (68%),        erated code than is warranted, not scrutinizing it as carefully as
where practitioners acknowledged clear trade-offs between speed           code written by a fellow developer [68]. This trust also extended to
Vibe Coding in Practice                                                                                  Conference’17, July 2017, Washington, DC, USA


                                                                          traditional QA practices. A majority of QA practices reflect a depar-
                                                                          ture from code verification, with practitioners commonly skipping
                                                                          tests, placing uncritical trust in outputs, or delegating responsibility
                                                                          back to the AI code generation tools. These QA concerns are possi-
                                                                          bly due to multiple factors: Technical barriers; e.g., the AI-generated
                                                                          code is cited to be difficult to debug as it can lack architectural struc-
                                                                          ture [21] and the contextual details software developers normally
                                                                          rely on, such as comments, assumptions, or information about how
                                                                          the code integrates with the larger system. Confusion: vibe coders
                                                                          report confusion when attempting to understand AI-generated code.
                                                                          False confidence: the “instant success” experience creates illusions
                                                                          of correctness. If current practices continue, vibe-coded apps may
                                                                          look fine but hide serious flaws. Practitioners already warn of this
                                                                          risk, with 19% admitting their code is “fragile or error-prone”. This
        Figure 3: Speed vs QA Trade-off in Vibe Coding
                                                                          matters because once teams get used to shipping fragile or error-
                                                                          prone code without proper QA, they may lower the quality bar
complex systems, with reports that people were no longer checking         across the whole organization. Over time, this creates a culture
outputs line by line but simply accepting the responses in a very         where untested code is considered acceptable, raising the risk of
trusting way [52].                                                        costly failures, outages, and security breaches.
Delegated QA to AI: Another QA practice (10%) was delegating                 Recommendation for AI code generation tools designers: AI code
quality checks back to the AI itself. As one source noted, users were     generation tools should incorporate lightweight verification pro-
overly reliant on the same LLMs that had introduced errors, which         cesses and continuously remind users of the QA aspects (especially
were also used to fix them, giving a false sense of security [63].        those with no formal software development experience) of the gen-
                                                                          erated code. Including code (static and dynamic) analysis checks
5 Discussion                                                              that can verify the generated code and remind developers of poten-
                                                                          tial risks can be a useful tool for coders. This can be offered as a
5.1 Key Observations                                                      real-time indicator (e.g., performance, security concerns, missing
The Speed–Quality Trade-off Paradox: Our results highlight a              tests) of the generated code. Tools should address the “Uncritical
paradox: vibe coders knowingly accept flawed AI-generated code            Trust” issue by including features such as step-by-step code expla-
in exchange for rapid progress. Development speed motivates all           nations (“walkthroughs”), visual diagrams, or inline explanations
groups, but the trade-off manifests differently depending on back-        to clarify what the tool is doing and why.
ground and experience. Non- and novice software developers often
acknowledge that they can build applications quickly while conced-        New Class of Vulnerable Developers: One of the most notable
ing that “it’s not really coding” [36], reflecting both excitement and    implications of our findings is the emergence of a new class of
awareness of possible limitations. Experienced software developers        vulnerable developers. About 14% of vibe coders are motivated
also value speed, but balance it with caution, as 29% reported that       by accessibility and empowerment, with non-software develop-
they usually make some manual adjustments or add tests to the             ers describing how AI code generation tools allow them to create
generated code, showing risk-aware behavior. Developers some-             applications without prior coding skills [78]. Yet, this democratiza-
times apply extensive modifications to the generated code to the          tion often leaves them unprepared when problems arise. Several
level that they no longer consider it AI-generated [28]. This divide      sources illustrate how non-software developers quickly reach dead
shows that while vibe coders are willing to tolerate imperfect code       ends when faced with bugs or technical errors that they cannot
for speed, only experienced users have the skills to fix problems         diagnose or resolve [44, 76]. Others highlight how uncritical trust
when they arise. This observation is also reflected in the Stack Over-    in AI code generation tools suggestions can lead to copy-paste
flow Developer Survey 2025, which reports both high adoption of           development practices where fixes are applied without any real
AI code generation tools (84% use or plan to use them) and low            comprehension of their impact [44]. In practice, this over-reliance
trust in AI-generated code (∼46% report distrust) [61]. The impli-        can introduce serious risks: practitioners have documented cases of
cation is a divide between two groups of vibe coders: empowered           insecure systems built through vibe coding, including applications
novices who may remain dependent on AI code generation tools,             that lacked authentication, authorization, or contained hardcoded
and professionals who integrate selective QA practices.                   secrets [35]. Beyond individual projects, such practices contribute
   Recommendation for Practitioners: Use vibe coding to explore and       to the rise of “shadow IT”, where employees outside formal de-
prototype quickly, but never promote to production without adding         velopment teams build software without oversight or governance
guardrails: tests, code review, and traceable decision records (why the   [69]. As some experts caution, the danger is not when AI-generated
AI change was accepted, which checks passed, any accepted risks, and      code fails outright, but when it appears to work while embedding
a short prompt/response ID log).                                          subtle vulnerabilities and technical debt [19]. Taken together, these
                                                                          accounts suggest that while vibe coding lowers the barrier to entry,
The QA Crisis in AI-Assisted Development: The most observed
concerning issue with vibe coding is the systematic breakdown of
Conference’17, July 2017, Washington, DC, USA                                                                                        Fawzy et al.


it also transfers significant responsibility to users who may not yet     contains subjective judgment, so our findings should be understood
possess the necessary skills to manage it effectively.                    as patterns drawn from the data rather than precise measurements.
    Recommendation for Organizations and Practitioners: Match tasks       External Validity: Our study is based on 101 grey literature sources,
to skill and provide scaffolds (guided debugging, safe templates, and     which reflect the experiences of practitioners who chose to share
escalation paths), so newcomers learn to diagnose issues rather than      their stories online. This introduces self-selection bias, those rep-
outsource all QA to the AI. This is particularly important to avoid       resented may not reflect all vibe coders. We mitigated this by en-
the novice developer trap, where failures can lock beginners into         suring diversity in high-quality source types (blogs, forums, and
reprompt–paste loops, accepting fragile behavior when they cannot         media articles) and user roles (novices and experienced users) from
restore alignment between intent (their goal) and implementation          various industries. However, the findings cannot be considered
(what the AI-generated code actually does).                               generalizable to all vibe coders. Instead, they should be interpreted
                                                                          as indicative of common patterns in reported experiences, not as
5.2     Future Work and Open Research Questions                           representative of the entire population of vibe coders.
                                                                          Construct Validity: To establish a consistent data extraction basis
Further research is needed on how vibe coders’ practices shift
                                                                          for our GLR, we utilized a standard data extraction template to
with experience from non-software developers to novices to pro-
                                                                          ensure uniformity. We refined our data extraction methods after
fessionals, so that AI code generation tools can adapt feedback,
                                                                          several pilot tests. Reviews and discussions with other co-authors
explanations, and safeguards to the user’s expertise. Further empir-
                                                                          were carried out for the extracted data process, resolving discrepan-
ical evidence is needed to understand if these new practices will
                                                                          cies through consensus. Behavioral unit extraction was conducted
lead to new defect and vulnerability patterns unique compared to
                                                                          mainly by the first author. To increase reliability, a subset of units
both conventional AI-assisted (used by experienced developers)
                                                                          was cross-validated by another co-author, minimizing the likeli-
and human coding [11, 33], to inform automated quality signals
                                                                          hood of inaccurate conclusions. This reduced, but did not eliminate,
and assurance features in next-generation AI code generation tools.
                                                                          the risk of subjective bias and inaccurate conclusions.
   It is also unclear which code review practices (e.g., run-and-see
checks, automated tests, AI-assisted reviews) actually work under
vibe coding conditions. Research in this area can inform the design       7   Conclusion
of practical, built-in QA workflows that keep pace with rapid proto-
                                                                          This study provides the first empirical investigation of how users
typing. Understanding how code review and QA strategies should
                                                                          actually engage in vibe coding, especially outside formal devel-
differ for non-software developers, novices, and professionals can
                                                                          opment settings. By systematically analyzing 101 grey literature
enable tools to enhance the quality of the generated code, providing
                                                                          sources containing 518 firsthand behavioral units, we uncovered
guardrails for newcomers while supporting advanced workflows for
                                                                          why users engage in vibe coding, what they experience while doing
experts. Future research should explore how vibe coding practices
                                                                          so, how they perceive the quality of AI-generated code, and what
can be integrated into training for non-software developers, so that
                                                                          practices they apply to review or test the code.
educational interventions complement tool design and enhance
                                                                             Our findings reveal a speed–quality trade-off in vibe coding;
baseline QA competence.
                                                                          vibe coders, particularly those without software development ex-
                                                                          perience, are enabled to create usable applications quickly, which
6     Threats to Validity                                                 often comes at the expense of verification and maintainability limi-
Internal Validity: To address possible search bias in our GLR, we         tations. The widespread use of delegated QA to AI, uncritical trust,
first designed a comprehensive search strategy. We employed a             and skipped testing highlights how vibe coding outputs are vul-
detailed search strategy with iterative pilot searches to refine the      nerable. Moreover, the emergence of vulnerable developers(who
search terms (see Section 3.2). This approach broadened coverage          are capable of building but unable to debug) highlights the risks
and reduced search string bias, but given the diffuse and evolving        of democratizing software creation without corresponding invest-
nature of grey literature, we cannot claim to have captured all           ments in quality practices. For tool designers, our results suggest
relevant sources. We also defined a set of inclusion and exclusion        including QA feedback, visualizing code quality indicators, and pro-
criteria (see Section 3.3) and applied them consistently during the       viding inline explanations to mitigate the impact of uncritical trust.
data filtration to minimize any selection bias.                           For teams adopting AI-assisted development, cautious use of vibe
   To minimize quality bias, we applied Garousi et al.’s five-dimension   coding in production systems is recommended. Adhering to organi-
quality checklist [17] (see Section 3.4), excluding sources scoring       zations’ guardrails that require review processes and maintaining
below 10/15. This reduces the likelihood that anecdotal or promo-         debugging skills.
tional content disproportionately influenced the findings, although          AI code generation tools support will play a bigger role in soft-
there is still some risk of quality bias.                                 ware development in the future. How we respond to the behavioral
   With regards to data extraction bias, to avoid emphasizing certain     patterns identified in this study will determine whether the future
quotes or themes, we used a standardized extraction template and          improves or degrades software quality. The AI code generation
applied Braun and Clarke [8] structured thematic analysis steps           tools exist; the challenge lies in using them wisely.
(see Section 3.7). Coding was conducted primarily by the first au-
thor, with discussions and consensus building among the other
authors. Pilot extractions and iterative refinement helped calibrate      Data Availability Statement
interpretation in findings. However, thematic coding inevitably           We provide our data and detailed analysis in [13]
Vibe Coding in Practice                                                                                                         Conference’17, July 2017, Washington, DC, USA


References                                                                                 [26] Andrej Karpathy. 2025. There’s a new kind of coding I call “vibe coding”. https:
 [1] FedTec 2025. Vibe Coding: Accelerating Service Delivery in the Government.                 //x.com/karpathy/status/1886192184808149383. [Accessed on 01/05/2025].
     FedTec. https://fedtec.com/insights/vibe-coding-accelerating-service-delivery-        [27] Andrej Karpathy. 2025. Vibe coding MenuGen. https://x.com/karpathy/status/
     in-the-government/ [Accessed on 08/07/2025].                                               1917961248031080455 X (formerly Twitter). [Accessed on 07/07/2025].
 [2] Cloudflare 2025. What is vibe coding? Cloudflare. https://www.cloudflare.com/en-      [28] Syed Mohammad Kashif, Peng Liang, and Amjed Tahir. 2025. On Developers’
     gb/learning/ai/ai-vibe-coding/ [Accessed on 07/07/2025].                                   Self-Declaration of AI-Generated Code: An Analysis of Practices. arXiv preprint
 [3] Google Cloud 2025. What is vibe coding? Google Cloud. https://cloud.google.                arXiv:2504.16485 (2025).
     com/discover/what-is-vibe-coding [Accessed on 07/07/2025].                            [29] Gene Kim. 2025. Rearchitecting My Trello Management Tool with Claude Code using
 [4] Jean Adams, Frances C. Hillier-Brown, Helen J. Moore, Amelia A. Lake, Vera                 Vibe Coding/Architecting (Part 2). https://itrevolution.com/articles/rearchitecting-
     Araujo-Soares, Martin White, and Carolyn Summerbell. 2016. Searching and                   my-trello-management-tool-with-claude-code-using-vibe-coding-
     synthesising ‘grey literature’ and ‘grey information’ in public health: critical           architecting-part-2/ [Accessed on 08/07/2025].
     reflections on three case studies. Systematic Reviews 5, 1 (2016), 164. https:        [30] Hans-Alexander Kruse, Tim Puhlfurb, and Walid Maalej. 2024. Can Developers
     //doi.org/10.1186/s13643-016-0337-y                                                        Prompt? A Controlled Experiment for Code Documentation Generation. In 2024
 [5] Richard J. Adams, Paul Smart, and Anne S. Huff. 2016. Searching for grey literature        IEEE International Conference on Software Maintenance and Evolution (ICSME).
     for systematic reviews: challenges and benefits. Research Synthesis Methods 7, 3           IEEE Computer Society, 574–586.
     (2016), 263–281. https://doi.org/10.1002/jrsm.1106                                    [31] Mohammad Amin Kuhail, Sujith Samuel Mathew, Ashraf Khalil, Jose Berengueres,
 [6] Shraddha Barke, Michael B James, and Nadia Polikarpova. 2023. Grounded                     and Syed Jawad Hussain Shah. 2024. “Will I be replaced?” Assessing ChatGPT’s
     copilot: How programmers interact with code-generating models. Proceedings of              effect on software development and programmer perceptions of AI tools. Science
     the ACM on Programming Languages 7, OOPSLA1 (2023), 85–111.                                of Computer Programming 235 (2024), 103111.
 [7] Guillaume Beaulieu-Duchesneau. 2025. Vibe coding or “I let AI write all my code       [32] Kelsey Libert. 2025. Vibe coding with AI tools: A marketer’s guide. https:
     and it was fantastic (until it wasn’t)”. https://ingeno.ca/blog/vibe-coding-or-i-          //searchengineland.com/vibe-coding-with-ai-tools-a-marketers-guide-455134
     let-ai-write-all-my-code-and-it-was-fantastic-until-it-wasn-t/ [Accessed on                [Accessed on 08/07/2025].
     08/07/2025].                                                                          [33] Sherlock A Licorish, Ansh Bajpai, Chetan Arora, Fanyu Wang, and Kla Tan-
 [8] Virginia Braun and Victoria Clarke. 2006. Using thematic analysis in psychology.           tithamthavorn. 2025. Comparing Human and LLM Generated Code: The Jury is
     Qualitative Research in Psychology 3, 2 (2006), 77.                                        Still Out! arXiv preprint arXiv:2501.16857 (2025).
 [9] Simon Briscoe and Morwenna Rogers. 2024. An alternative screening approach            [34] Vahid Majdinasab, Michael Joshua Bishop, Shawn Rasheed, Arghavan Moradi-
     for Google Search identifies an accurate and manageable number of results for              dakhel, Amjed Tahir, and Foutse Khomh. 2024. Assessing the security of github
     a systematic review (case study). Health Information & Libraries Journal 41, 2             copilot’s generated code-a targeted replication study. In 2024 IEEE International
     (2024), 149–155.                                                                           Conference on Software Analysis, Evolution and Reengineering (SANER). IEEE,
[10] KitFu Coda. 2025. Vibe-Coding, Storytelling, and LLMs: A Collaborative                     435–444.
     Approach.        https://ai.plainenglish.io/vibe-coding-storytelling-and-llms-a-      [35] Rami McCarthy. 2025. Rules Files for Safer Vibe Coding. https://www.wiz.io/blog/
     collaborative-approach-db5e9a62c8b1 [Accessed on 07/07/2025].                              safer-vibe-coding-rules-files [Accessed on 07/07/2025].
[11] Domenico Cotroneo, Cristina Improta, and Pietro Liguori. 2025. Human-Written          [36] Niall McNulty. 2025. Vibe Coding: AI-Assisted Coding for Non-Developers.
     vs. AI-Generated Code: A Large-Scale Study of Defects, Vulnerabilities, and                https://medium.com/@niall.mcnulty/vibe-coding-b79a6d3f0caa [Accessed on
     Complexity. arXiv preprint arXiv:2508.21634 (2025).                                        02/07/2025].
[12] Benj Edwards. 2025. Will the Future of Software Development Run on                    [37] Ivan Mehta. 2025. A quarter of YC’s startups have AI-generated code-
     Vibes? https://arstechnica.com/ai/2025/03/is-vibe-coding-with-ai-gnarly-or-                bases. https://techcrunch.com/2025/03/06/a-quarter-of-startups-in-ycs-current-
     reckless-maybe-some-of-both/. [Accessed on 01/05/2025].                                    cohort-have-codebases-that-are-almost-entirely-ai-generated. [Accessed on
[13] Ahmed Fawzy, Amjed Tahir, and Kelly Blincoe. 2025. Vibe Coding in Practice: Mo-            01/05/2025].
     tivations, Challenges, and a Future Outlook - a Grey Literature Review (Replication   [38] Maxime Najim. 2025. Vibe coding brought back my love for programming. https:
     package). https://doi.org/10.5281/zenodo.17188020                                          //leaddev.com/culture/vibe-coding-brought-back-love-programming [Accessed
[14] Molly Q Feldman and Carolyn Jane Anderson. 2024. Non-expert programmers                    on 08/07/2025].
     in the generative AI future. In Proceedings of the 3rd Annual Meeting of the          [39] John Naughton. 2025.          Now you don’t even need code to be a pro-
     Symposium on Human-Computer Interaction for Work. 1–19.                                    grammer. https://www.theguardian.com/technology/2025/mar/16/ai-software-
[15] Samuel Ferino, Rashina Hoda, John Grundy, and Christoph Treude. 2025. Junior               coding-programmer-expertise-jobs-threat. [Accessed on 01/05/2025].
     Software Developers’ Perspectives on Adopting LLMs for Software Engineering:          [40] Gergely Orosz and Elin Nilsson. 2025. Vibe Coding as a Software Engineer. https:
     a Systematic Literature Review. arXiv preprint arXiv:2503.07556 (2025).                    //newsletter.pragmaticengineer.com/p/vibe-coding-as-a-software-engineer [Ac-
[16] Yujia Fu, Peng Liang, Amjed Tahir, Zengyang Li, Mojtaba Shahin, Jiaxin Yu, and             cessed on 02/07/2025].
     Jinfu Chen. 2025. Security Weaknesses of Copilot-Generated Code in GitHub             [41] Addy Osmani. 2025. Speech-to-Code: Vibe Coding with Voice.                  https://
     Projects: An Empirical Study. ACM Transactions on Software Engineering and                 addyo.substack.com/p/speech-to-code-vibe-coding-with-voice [Accessed on
     Methodology (2025).                                                                        07/07/2025].
[17] Vahid Garousi, Michael Felderer, and Mika V Mäntylä. 2019. Guidelines for             [42] Addy Osmani. 2025. Vibe Coding: Revolution or Reckless Abandon? https://addyo.
     including grey literature and conducting multivocal literature reviews in software         substack.com/p/vibe-coding-revolution-or-reckless [Accessed on 07/07/2025].
     engineering. Information and software technology 106 (2019), 101–121.                 [43] Matt Palmer. 2025. What is Vibe Coding? https://blog.replit.com/what-is-vibe-
[18] Namanyay Goel. 2025. Karpathy’s ‘Vibe Coding’ Movement Considered Harmful.                 coding [Accessed on 07/07/2025].
     https://nmn.gl/blog/dangers-vibe-coding [Accessed on 08/07/2025].                     [44] Katie Parrott. 2025. I Tried AI Coding Tools. Now I Want to Learn to
[19] Namanyay Goel. 2025. Vibe Coding is a Dangerous Fantasy. https://nmn.gl/blog/              Code. https://every.to/working-overtime/i-tried-ai-coding-tools-now-i-want-
     vibe-coding-fantasy [Accessed on 08/07/2025].                                              to-learn-to-code [Accessed on 07/07/2025].
[20] Philipp Haindl and Gerald Weinberger. 2024. Does ChatGPT help novice pro-             [45] Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, and
     grammers write better code? Results from static code analysis. IEEE Access                 Ramesh Karri. 2025. Asleep at the keyboard? assessing the security of github
     (2024).                                                                                    copilot’s code contributions. Commun. ACM 68, 2 (2025), 96–105.
[21] Shalini Harkar. 2025. What is Vibe Coding? https://www.ibm.com/think/topics/          [46] Sida Peng, Eirini Kalliamvakou, Peter Cihon, and Mert Demirer. 2023. The impact
     vibe-coding [Accessed on 02/07/2025].                                                      of AI on developer productivity: Evidence from Github Copilot. arXiv preprint
[22] Nick Hodges. 2025. Vibe coding with Claude Code. https://www.infoworld.com/                arXiv:2302.06590 (2023).
     article/3853805/vibe-coding-with-claude-code.html [Accessed on 07/07/2025].           [47] James Prather, Brent N Reeves, Paul Denny, Brett A Becker, Juho Leinonen,
[23] Chetan Jaiswal. 2025. What is vibe coding? A computer scientist explains                   Andrew Luxton-Reilly, Garrett Powell, James Finnie-Ansley, and Eddie Antonio
     what it means to have AI write computer code and what risks that can entail.               Santos. 2023. “It’s weird that it knows what i want”: Usability and interactions
     https://theconversation.com/what-is-vibe-coding-a-computer-scientist-                      with copilot for novice programmers. ACM transactions on computer-human
     explains-what-it-means-to-have-ai-write-computer-code-and-what-risks-                      interaction 31, 1 (2023), 1–31.
     that-can-entail-257172 [Accessed on 02/07/2025].                                      [48] James Prather, Brent N Reeves, Juho Leinonen, Stephen MacNeil, Arisoa S Randri-
[24] Fernando Kamei, Igor Wiese, Crescencio Lima, Ivanilton Polato, Vilmar Nepo-                anasolo, Brett A Becker, Bailey Kimmel, Jared Wright, and Ben Briggs. 2024. The
     muceno, Waldemar Ferreira, Márcio Ribeiro, Carolline Pena, Bruno Cartaxo,                  widening gap: The benefits and harms of generative ai for novice programmers.
     Gustavo Pinto, and Sérgio Soares. 2021. Grey Literature in Software Engineer-              In Proceedings of the 2024 ACM Conference on International Computing Education
     ing: A critical review. Information and Software Technology 138 (2021), 106609.            Research-Volume 1. 469–486.
     https://doi.org/10.1016/j.infsof.2021.106609                                          [49] ProfileTree. 2025. Vibe Coding: How AI is Transforming Software Development in
[25] Fernando Kenji Kamei. 2019. The use of grey literature review as evidence for              2025. https://profiletree.com/vibe-coding/ [Accessed on 07/07/2025].
     practitioners. ACM SIGSOFT Software Engineering Notes 44, 3 (2019), 23–23.            [50] Sujatha R. 2025. 10 Best Vibe Coding Tools: LLM-Powered Code Generators to Try.
                                                                                                https://www.digitalocean.com/resources/articles/vibe-coding-tools [Accessed
Conference’17, July 2017, Washington, DC, USA                                                                                                                        Fawzy et al.


     on 07/07/2025].                                                                            Springer.
[51] David Ramel. 2025. AI’s Takeover of Software Development Gets a Name: ‘Vibe           [78] Angela Yang. 2025. Noncoders are using AI to prompt their ideas into reality. They
     Coding’. https://visualstudiomagazine.com/articles/2025/03/20/ais-takeover-of-             call it ‘vibe coding.’. https://www.nbcnews.com/tech/tech-news/noncoders-ai-
     software-development-gets-a-name-vibe-coding.aspx [Accessed on 07/07/2025].                prompt-ideas-vibe-coding-rcna205661 [Accessed on 07/07/2025].
[52] John Ruwitch. 2025. Anyone can use AI chatbots to ‘vibe code.’ Could that put         [79] Yangtian Zi, Luisa Li, Arjun Guha, Carolyn Anderson, and Molly Q Feldman. 2025.
     programmers out of a job? https://www.npr.org/2025/05/30/nx-s1-5413387/vibe-               “I Would Have Written My Code Differently’: Beginners Struggle to Understand
     coding-ai-software-development [Accessed on 07/07/2025].                                   LLM-Generated Code. In Proceedings of the 33rd ACM International Conference
[53] Andreas Scholl and Natalie Kiesler. 2024. How Novice Programmers Use and                   on the Foundations of Software Engineering. 1479–1488.
     Experience ChatGPT when Solving Programming Exercises in an Introductory              [80] Rina Zviel-Girshin. 2024. The Good and Bad of AI Tools in Novice Programming
     Course. arXiv preprint arXiv:2407.20792 (2024).                                            Education. Education Sciences 14, 10 (2024), 1089.
[54] Natassha Selvaraj. 2025. Building Data Science Projects Using AI: A Vibe Coding
     Guide. https://www.kdnuggets.com/building-data-science-projects-using-ai-a-
     vibe-coding-guide [Accessed on 07/07/2025].
[55] Pete Sena. 2025. Cracking the code of vibe coding. https://uxdesign.cc/cracking-
     the-code-of-vibe-coding-124b9288e551 [Accessed on 07/07/2025].
[56] Judy Sheard, Paul Denny, Arto Hellas, Juho Leinonen, Lauri Malmi, and Simon.
     2024. Instructor Perceptions of AI Code Generation Tools-A Multi-Institutional
     Interview Study. In Proceedings of the 55th ACM Technical Symposium on Computer
     Science Education V. 1. 1223–1229.
[57] Tyler Shields. 2025. My first attempt at vibe coding. https://www.techtarget.com/
     searchapparchitecture/opinion/My-first-attempt-at-vibe-coding [Accessed on
     02/07/2025].
[58] Matthew S. Smith. 2025. Engineers Are Using AI to Code Based on Vibes. https:
     //spectrum.ieee.org/vibe-coding. [Accessed on 01/05/2025].
[59] Jacopo Soldani, Damian Andrew Tamburri, and Willem-Jan Van Den Heuvel.
     2018. The pains and gains of microservices: A systematic grey literature review.
     Journal of Systems and Software 146 (2018), 215–232.
[60] Richard Speed. 2025. Forget Vibe Coding, We’re All About Vine Coding Nowa-
     days. https://www.theregister.com/2025/06/13/forget_vibe_coding_were_all/
     [Accessed on 07/07/2025].
[61] Stack Overflow. 2025. Stack Overflow Developer Survey 2025. https://survey.
     stackoverflow.co/2025/. [Accessed on 11/08/2025].
[62] Tanium Staff. 2025. What is Vibe Coding? The Pros, Cons, and Controversies.
     https://www.tanium.com/blog/what-is-vibe-coding/ [Accessed on 08/07/2025].
[63] Chris Stokel-Walker. 2025. What is vibe coding, should you be doing it, and does it
     matter? https://www.newscientist.com/article/2473993-what-is-vibe-coding-
     should-you-be-doing-it-and-does-it-matter/ [Accessed on 07/07/2025].
[64] Darryl K. Taft. 2024. Amazon Q Developer Now Handles Your Entire Code
     Pipeline. https://thenewstack.io/amazon-q-developer-now-handles-your-entire-
     code-pipeline/ [Accessed on 08/07/2025].
[65] Amjed Tahir, Shawn Rasheed, Jens Dietrich, Negar Hashemi, and Lu Zhang. 2023.
     Test flakiness’ causes, detection, impact and responses: A multivocal review.
     Journal of Systems and Software 206 (2023), 111837.
[66] Priyan Vaithilingam, Tianyi Zhang, and Elena L Glassman. 2022. Expectation
     vs. experience: Evaluating the usability of code generation tools powered by
     large language models. In Chi conference on human factors in computing systems
     extended abstracts. 1–7.
[67] Steven Vaughan-Nichols. 2025. Bad vibes: How an AI agent coded its way to
     disaster. https://www.zdnet.com/article/bad-vibes-how-an-ai-agent-coded-its-
     way-to-disaster/ [Accessed on 08/07/2025].
[68] Todd R. Weiss. 2025. Vibe coding: What automating development means for
     AppSec. https://www.reversinglabs.com/blog/vibe-coding-what-autonomous-
     code-means-for-appsec [Accessed on 08/07/2025].
[69] Todd R. Weiss. 2025. What MSPs Need to Know About Vibe Coding, Agentic AI
     and IT Security. https://www.channele2e.com/news/what-msps-need-to-know-
     about-vibe-coding-agentic-ai-and-it-security [Accessed on 08/07/2025].
[70] Justin D Weisz, Shraddha Vijay Kumar, Michael Muller, Karen-Ellen Browne,
     Arielle Goldberg, Katrin Ellice Heintze, and Shagun Bajpai. 2025. Examining the
     use and impact of an ai code assistant on developer productivity and experience
     in the enterprise. In Proceedings of the Extended Abstracts of the CHI Conference
     on Human Factors in Computing Systems. 1–13.
[71] Wikipedia contributors. 2025. Vibe coding. https://en.wikipedia.org/wiki/Vibe_
     coding [Accessed on 02/07/2025].
[72] Rhiannon Williams. 2025. What is vibe coding, exactly?              https://www.
     technologyreview.com/2025/04/16/1115135/what-is-vibe-coding-exactly/ [Ac-
     cessed on 07/07/2025].
[73] Simon Willison. 2025. Here’s how I use LLMs to help me write code. https:
     //simonwillison.net/2025/Mar/11/using-llms-for-code/ [Accessed on 07/07/2025].
[74] Simon Willison. 2025. Not all AI-assisted programming is vibe coding (but vibe
     coding rocks). https://simonwillison.net/2025/Mar/19/vibe-coding/ [Accessed on
     02/07/2025].
[75] Simon Willison. 2025. Two publishers and three authors fail to understand what
     “vibe coding” means. https://simonwillison.net/2025/May/1/not-vibe-coding/.
     [Accessed on 04/05/2025].
[76] Mark Wilson. 2025. Vibe coding with AI. https://node4.co.uk/blog/vibe-coding-
     with-ai/ [Accessed on 08/07/2025].
[77] Claes Wohlin, Per Runeson, Martin Höst, Magnus C Ohlsson, Björn Regnell,
     Anders Wesslén, et al. 2012. Experimentation in software engineering. Vol. 236.
