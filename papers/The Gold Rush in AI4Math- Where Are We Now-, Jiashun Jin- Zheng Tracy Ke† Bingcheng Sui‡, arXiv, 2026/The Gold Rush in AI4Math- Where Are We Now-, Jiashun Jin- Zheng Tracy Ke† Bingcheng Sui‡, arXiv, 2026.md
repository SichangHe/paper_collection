                                                           The Gold Rush in AI4Math: Where Are We Now?
                                                                        Jiashun Jin*           Zheng Tracy Ke†              Bingcheng Sui‡



                                                                                                      Abstract
arXiv:2608.24961v1 [stat.AP] 25 Aug 2026




                                                          Recent advances in artificial intelligence (AI) have sparked growing interest in its use for mathematical
                                                     research. While some view this as a major opportunity for discovery, others have raised concerns about
                                                     its impact on traditional research practices. Despite extensive debate, empirical evidence on how AI is
                                                     actually being used in mathematics remains limited.
                                                          To address this gap, we collected all 32,944 arXiv submissions posted between March 1 and August
                                                     20, 2026, whose primary or secondary categories included Mathematics. We identified 3,575 submissions
                                                     that explicitly disclosed author use of AI, of which 1,712 involved at least one substantive mathematical
                                                     contribution.
                                                          Our analysis reveals several broad patterns. First, disclosed AI use increased sharply over the study
                                                     period, with substantive use growing from 1.39% of Mathematics submissions in March to 14.09% through
                                                     August 20. Second, substantive AI use is highly uneven across fields: Combinatorics has the largest
                                                     number of such papers, while Metric Geometry has the highest substantive-use rate. Third, substantive AI
                                                     use is geographically concentrated: under weighted author counts, the United States and China together
                                                     account for about two-thirds of the recognized country weight. Fourth, AI is already being applied to
                                                     open research problems: among 717 named open-problem records associated with substantive use, 71%
                                                     are labeled as fully resolved based on the authors’ descriptions, with proofs of the conjectured statement
                                                     more common than counterexamples or disproofs. Finally, AI-system use is also highly concentrated,
                                                     with OpenAI systems appearing most frequently, followed by Anthropic.
                                                          Together, these findings suggest that AI-assisted mathematics is expanding rapidly but remains at
                                                     an early and uneven stage of adoption. They provide an empirical picture of where AI is beginning to
                                                     influence mathematical research and a data-driven basis for ongoing discussions about its future role in
                                                     the discipline.


                                           1        Introduction
                                           Mathematics, one of the most logically rigorous disciplines, has served as a natural test ground for evaluating
                                           the reasoning capabilities of AI systems (Hendrycks et al., 2021; Lewkowycz et al., 2022; Trinh et al.,
                                           2024). Early efforts focused primarily on solving well-specified mathematical problems, ranging from
                                           elementary exercises to competition-level problems. Recent systems such as FunSearch, AlphaGeometry, and
                                           AlphaProof have pushed this frontier further, demonstrating increasingly strong capabilities in mathematical
                                           discovery, geometry, and formal reasoning (Romera-Paredes et al., 2024; Trinh et al., 2024; Hubert et al.,
                                           2026). These advances raise a more ambitious question: Can AI move beyond solving well-specified problems
                                           and contribute meaningfully to research-level mathematics?
                                               There has been encouraging recent progress. In early 2026, Claude Opus 4.6 found a general construction
                                           for an open Hamiltonian-cycle decomposition problem (Knuth, 2026). Soon afterward, an unreleased OpenAI
                                           model produced a counterexample to Erdős’s nearly 80-year-old unit-distance conjecture (Alon et al., 2026).
                                               * jiashunmail@gmail.com
                                               †
                                                   zke@fas.harvard.edu
                                               ‡
                                                   bingchengsui@g.harvard.edu


                                                                                                           1
Figure 1: Substantive AI use in seven-day forward windows. Each daily marker reports the number of
submissions with substantive AI use and their share among all Mathematics submissions in the complete
seven-day window beginning on that date. Dashed vertical lines indicate model release dates, while rounded
callouts mark notable AI-assisted research events. Details of the data construction are provided in Section 2.


The First Proof project offered a more systematic test: on ten unpublished research problems, current AI
systems obtained passing solutions to seven under independent expert refereeing (Abouzaid et al., 2026).
In July, Alpöge and Claude produced an explicit counterexample to the Jacobian conjecture in dimension
three (Alpöge and Claude Fable 5, 2026). In August, OpenAI reported that its Astra model had resolved
or substantially advanced ten long-standing problems across several areas of mathematics and theoretical
computer science (OpenAI, 2026). Around the same time, an unreleased version of Claude improved the
unconditional lower bound for the proportion of simple zeros of the Riemann zeta function on the critical line
from 41.6% to 67.2% (Claude, 2026). Together, these examples suggest that AI is beginning to contribute
directly to the production of new mathematics.
    This transition has generated both excitement and concern within the mathematical community. Recent
perspective articles have begun to examine how AI may reshape mathematical practice, understanding, and
professional norms (Avigad, 2026; Klowden and Tao, 2026; Commelin et al., 2026; Tao, 2026). On the
one hand, AI systems may serve as powerful research assistants by suggesting arguments, searching for
counterexamples, formalizing reasoning, and accelerating mathematical exploration. Formal proof assistants
such as Lean can also help verify AI-generated proofs mechanically (Song et al., 2025; Hubert et al., 2026).
On the other hand, increasing AI use raises concerns about reliability, attribution and credit, access to
proprietary models, and the role of human understanding and judgment (Commelin et al., 2026; Tao, 2026).
These issues have become sufficiently prominent that the 2026 Leiden Declaration on Artificial Intelligence
and Mathematics called for transparency and for preserving established norms of verification, attribution,
openness, and human responsibility (Alper et al., 2026).
    Despite the rapidly growing literature on the capabilities of AI systems in mathematics, much less is
known about their actual adoption in mathematical research. Existing studies largely ask whether AI can
generate formally verified proofs or tackle selected research-level problems. These studies help characterize


                                                      2
the technological frontier, but they do not reveal how frequently mathematicians are using AI in practice, how
adoption is evolving over time, which areas of mathematics are adopting these tools most rapidly, or which
AI systems are most commonly used. This distinction can be summarized by two different questions: “Can
AI do mathematical research?” and “To what extent is AI already being used to do mathematical research?”
The latter is an empirical question for which systematic evidence remains limited.
     To study actual AI adoption in mathematical research, we examine recent submissions to arXiv. We
collected all 32,944 submissions under the Mathematics category between March 1 and August 20, 2026,
and identified 3,575 papers with confirmed disclosed author use of AI, including 1,712 with at least one
substantive mathematical contribution. Under our non-exclusive coding, 1,225 papers report AI involvement
in proof construction. Figure 1 provides an overview of the rapid growth of substantive AI use over this period.
Using these data, we study how disclosed AI use has evolved over time, how it varies across mathematical
fields, what roles AI plays in research, its involvement with named open problems, the authors and institutions
adopting these tools, the AI systems being used, and selected characteristics of AI-assisted papers. Our
reliance on explicit disclosure (arXiv, 2026) provides a transparent and reproducible criterion for identifying
AI-assisted research, but should be interpreted as a conservative measure of adoption because undisclosed
uses cannot be observed.
     Our results reveal a rapidly expanding but highly uneven pattern of AI adoption in mathematics. Disclosed
AI use rises sharply over the study period, with substantive use growing particularly quickly. Adoption is
concentrated in a small number of mathematical fields, led by Combinatorics and Number Theory, and is also
concentrated among a relatively small set of authors and institutions. We find substantial AI involvement
with named open problems, including both unresolved questions and problems reported as resolved. Model
use is similarly concentrated, with OpenAI systems appearing most frequently followed by Anthropic. Taken
together, these findings suggest that AI-assisted mathematics is expanding rapidly, but remains at an early
and highly heterogeneous stage of adoption.
     By providing a systematic snapshot of recent arXiv activity, our study complements the rapidly expanding
literature on AI’s mathematical capabilities with evidence on its adoption in research practice. We aim to
establish an empirical baseline for a debate that has so far been shaped largely by technological demonstrations,
individual case studies, and competing predictions about the future of the field. As AI systems continue to
improve, systematically tracking how, where, and by whom they are used will be important for understanding
how the practice of mathematical research itself is changing.


2    Data and study design
Between March 1 and August 20, 2026, there were 32,944 submissions whose primary or secondary categories
included Mathematics. We downloaded the PDF files for all submissions, together with their arXiv identifiers,
posting dates, titles, category labels, and authors. Each PDF was converted to plain text using advanced
document-parsing tools. Specifically, text was extracted page by page, with page boundaries explicitly
marked. For articles exceeding 300,000 characters, only the beginning and end 150,000 characters of the text
were retained. Among the 32,944 records, only 1,007 were flagged as truncated.
The questionnaire. We designed a questionnaire to analyze each submission and collect information that
cannot be directly obtained from the arXiv metadata. The first group of questions concerns the categories
of AI use. We consider two main categories, substantive use and non-substantive use, each consisting of
four subcategories; see Table 1. For each subcategory, the questionnaire requires a yes/no response, and
the subcategories are non-exclusive. The substantive use category is labeled yes if at least one of its four
subcategories is labeled yes; the same rule applies to non-substantive use.
    The second group of questions identifies whether the article addresses any open problems or conjectures.
For each such problem or conjecture, the questionnaire records its status as open, partially resolved, resolved

                                                       3
true, resolved false, or unclear, and whether AI played a critical role in reaching the reported resolution.
     The third group of questions concerns the authors’ institutions and countries. Because arXiv records
provide author names but generally not institutional affiliations, this information is obtained from the parsed
full text—for example, from listed affiliations or email addresses—or, when necessary, through web searches.
Collection of questionnaire responses. We used AI to answer the questionnaire for each submission.
Importantly, the responses are based on the authors’ disclosures rather than on assessment of the mathematical
content. Therefore, the AI system used for this task does not need to perform mathematical reasoning. Its
primary role is to identify relevant disclosure statements about AI use and extract their semantic meaning.
    We used GPT-5.6 Terra with low reasoning effort and processed the submissions in parallel using 100
worker threads. The prompt consisted of a fixed system instruction and an article-specific user message. The
system instruction defined the scope of AI, specified a three-level confidence scale, required all supporting
evidence to be quoted verbatim from the article, and presented the questionnaire described above. The user
message provided the arXiv metadata and enclosed the extracted article text. The output was restricted to
a single structured object with four components: AI-use judgments, named AI models, qualifying open
problems, and author–institution pairs. For AI-use judgments, it requested confidence scores from 1 to 3 for
each subcategory, and every answer had to be accompanied by a direct quotation (‘evidence’) from the article.

Manual validation. We also conducted a manual validation on a subset of submissions. Because it is
infeasible to manually review all 32,944 submissions, we first performed a keyword search over the parsed
full texts using a comprehensive list of keywords covering nearly all major AI model names. This screening
step identified approximately 5,000 candidate articles. We then sampled articles from this set and manually
completed the questionnaire for each sampled article. The manual validation is still ongoing, and we have
assembled a team of more than 10 volunteers to carry out this process.


3     Results
3.1   A sharp recent increase, from a small base
We begin by examining how disclosed AI use changed over the study period. The overall pattern is striking:
AI use in mathematical research increased rapidly between March and August 2026. Among all Mathematics
submissions, the share with confirmed AI use rose monotonically from 4.75% in March to 24.14% through
August 20. The increase was even more pronounced for substantive AI use, which rose from 1.39% to 14.09%
over the same period. Thus, by the end of the study period, both measures were several times higher than at
the beginning, indicating a rapid acceleration in disclosed AI adoption in mathematical research.
    The nature of AI use is also heterogeneous. As shown in Table 1, language and formatting is by far the
most common individual use, indicating that much of the disclosed AI assistance remains editorial rather than
mathematical. At the same time, substantive uses are already substantial. Proof construction is the largest
substantive subcategory, with 1,225 papers, followed by formalization and verification (427), other research
assistance (289), and problem formulation (146). Because these subcategories are non-exclusive, a single
paper may report multiple forms of AI assistance.
    Figure 2 shows that the increase in AI use is broad rather than driven by a single type of assistance.
Both substantive and non-substantive categories become more prevalent over the study period, and most
individual subcategories show substantial growth. In particular, the rapid increase in proof construction and
other substantive uses indicates that the recent expansion of AI adoption extends beyond writing, coding, and
other non-substantive assistance to more direct participation in mathematical research.
    The rapid increase we observe is consistent with a broader rise in AI use across scientific research. Large-
scale studies have documented growing AI-assisted writing and research across multiple disciplines (Liang
et al., 2025; Cheng et al., 2024; Hao et al., 2026; He and Bu, 2026). These studies primarily capture linguistic

                                                       4
 Table 1: AI-use categories. “All subcategories” is the de-duplicated number of articles carrying at least one
 label in the major category; individual subcategory counts are non-exclusive.

      Category         Subcategory                                 All    Mar       Apr    May      Jun      Jul   Aug∗
                       All articles                          32,944      5,265    5,097    5,525   6,106   6,464   4,487
                       AI usage                               3,575        250      281      430     570     961   1,083
                       All subcategories                      1,712         73      110     174     253     470     632
                       Proof construction                     1,225         50       74     136     183     337     445
      Substantive      Problem formulation                      146          7        9      15      29      41      45
                       Formalization and verification           427         23       31      34      67     108     164
                       Other research assistance                289         15       18      21      41      76     118
                       All subcategories                      2,809       219       229     332     461     758     810
                       Language and formatting                2,108       165       169     227     321     585     641
      Nonsubstantive   Code and computation                   1,229        97       111     158     219     308     336
                       Literature and references                524        33        26      47      66     157     195
                       Other non-substantive assistance         259        25        20      32      41      64      77
                                          ∗ The August data do not cover the full month.




                    (a) Substantive use                                             (b) Non-substantive use
 Table 2: Monthly AI-use category proportions. Panel (a) shows substantive categories: PC (Proof construc-
 tion), PF (Problem formulation), FV (Formalization and verification), OR (Other research assistance), and
 SA (substantive use in total). Panel (b) shows non-substantive categories: LF (Language and formatting),
 CC (Code and computation), LR (Literature and references), ON (Other non-substantive assistance), and
 NA (non-substantive use in total).



signals or broad measures of AI involvement. In contrast, our analysis uses explicit author disclosures
and distinguishes substantive mathematical contributions from non-substantive assistance, suggesting that
the recent growth of AI use in mathematics extends beyond scientific writing to direct participation in
mathematical research.

3.2    Which areas of mathematics are most affected?
The adoption of AI is highly uneven across mathematical fields. Table 3 reports both the number of substantive-
use papers and the total number of submissions in each arXiv Mathematics subfield. Combinatorics stands
out with 397 substantive-use papers, followed by Number Theory (135), Probability (110), and Algebraic
Geometry (95). At the other extreme, K-Theory and Homology, Quantum Algebra, and Symplectic Geometry
each have only four substantive-use papers. These differences already suggest substantial heterogeneity in AI

                                                               5
Table 3: Primary-field results for all 31 arXiv Mathematics primary sub-fields. “All” gives the total number
of submissions in each field, while “AI-use” gives the number in the confirmed-use sample. Substantive
subcategory counts are non-exclusive.

  Sub-field                  arXiv ID     All   AI-use   Substantive   Substantive %   Proof   Form   Verify   Other
  Combinatorics              math.CO    3,382     687           397         11.74%      305      35      99      49
  Number Theory              math.NT    1,698     216           135          7.95%      102      12      40      18
  Optimization and Control   math.OC    2,554     224            73          2.86%       52       2      18      12
  Probability                math.PR    1,712     189           110          6.43%       86       6      21      13
  Numerical Analysis         math.NA    2,195     182            42          1.91%       26       1       6       9
  Analysis of PDEs           math.AP    3,035     167            67          2.21%       47       5      17      11
  Algebraic Geometry         math.AG    1,462     144            95          6.50%       67      13      18      23
  Functional Analysis        math.FA      988     104            52          5.26%       40       3      16       6
  Statistics Theory          math.ST      785      92            42          5.35%       33       1       7       5
  Differential Geometry      math.DG    1,254      90            49          3.91%       33       7      11       7
  Group Theory               math.GR      657      78            43          6.54%       35       3       8       6
  Metric Geometry            math.MG      305      72            40         13.11%       27       0      10       9
  Classical Analysis         math.CA      547      73            43          7.86%       30       3       6      11
  Dynamical Systems          math.DS    1,166      69            22          1.89%       14       2      10       4
  Mathematical Physics       math-ph      817      48            17          2.08%       12       0       3       4
  Representation Theory      math.RT      628      61            35          5.57%       25       6       8       5
  Geometric Topology         math.GT      569      52            31          5.45%       19       5       7       7
  Logic                      math.LO      498      55            34          6.83%       24       2      11       4
  Operator Algebras          math.OA      256      39            16          6.25%        9       3       2       7
  Algebraic Combinatorics    math.AC      359      38            25          6.96%       16       2       6       5
  General Mathematics        math.GM      274      46            14          5.11%        9       3       3       5
  Rings and Algebras         math.RA      442      32            18          4.07%       11       1       5       5
  Complex Variables          math.CV      455      29            16          3.52%        8       4       7       1
  Algebraic Topology         math.AT      366      28            13          3.55%        6       0       3       6
  Category Theory            math.CT      216      21             8          3.70%        6       3       1       1
  Spectral Theory            math.SP      197      20            13          6.60%       10       2       1       3
  History and Overview       math.HO      127      19             6          4.72%        2       1       3       1
  Quantum Algebra            math.QA      216      14             4          1.85%        3       0       1       0
  Symplectic Geometry        math.SG      167      11             4          2.40%        4       0       0       0
  General Topology           math.GN      137       8             5          3.65%        5       0       0       0
  K-Theory and Homology      math.KT       52       4             4          7.69%        4       0       0       0



adoption across mathematical areas.
    The picture changes somewhat after accounting for field size. Metric Geometry has the highest substantive-
use rate, with 40 of 305 papers (13.11%), followed by Combinatorics at 11.74%. Number Theory and Classical
Analysis also have relatively high rates, at 7.95% and 7.86%, respectively. In contrast, some large fields, such
as Numerical Analysis and Analysis of PDEs, contain many AI-use papers in absolute terms but have much
lower substantive-use rates, at 1.91% and 2.21%.
    These differences suggest that current AI adoption is not simply proportional to the volume of research
produced in a field. Some areas appear more receptive to substantive AI assistance than others. This is
consistent with recent observations that automated reasoning has been particularly successful in areas such
as combinatorics, algebra, number theory, and discrete geometry (Avigad, 2026). More broadly, problem
solving, proof generation, and formal verification have been identified as aspects of mathematical practice
especially susceptible to AI progress (Tao, 2026; Commelin et al., 2026). Differences in community norms,
disclosure practices, and the composition of early adopters may also contribute. Our observational data,
however, do not allow us to distinguish among these explanations.




                                                         6
        (a)50                                                                                                       (b)
                         Not reported: 388

                  40                                            39 39 40
                                                                                                                                          2% 14%
Problem records


                                                                                                        36
                                                                                                                                    25%
                  30                               27                                                                                            13%
                                                         24                                     25 24
                                              22
                  20                                                                 19
                                                                                           15
                                                                                                                                          46%
                  10              8   8
                          1   2
                  0
                                                                                                                           Open                 Resolved false
                       190 899
                       192 919
                       195 949
                       197 969
                       198 979
                       199 989
                       200 999
                       201 009
                       201 014
                       202 019
                              022

                                3
                                4
                                5
                                6
                                                                                                                           Partially resolved   Unclear


                            202
                            202
                            202
                            202
                          0-1
                          0-1
                          0-1
                          0-1
                          0-1
                          0-1
                          0-1
                          0-2
                          0-2
                          5-2
                          0-2
                                                                                                                           Resolved true
                   185




                                                   Proposed year
                                   (c)
                 Combinatorics                                                                                                                           196
                Number Theory                                                             60
            Algebraic Geometry                                                  49
                     Probability                                          38
            Functional Analysis                                          35
                  Group Theory                                      29
       Optimization and Control                                24
       Algebraic Combinatorics                            19
              Classical Analysis                          19                                                   Open                  Resolved true     Unclear
               Analysis of PDEs                         15                                                     Partially resolved    Resolved false
                                          0                                    50                        100                  150                       200
                                                                                                    Problem records
    Figure 2: Named open-problem analysis. Panel (a) shows the distribution of problem records by audited
    proposed-year interval among records with a reported proposed year; the 388 records for which the proposed
    year was not reported are omitted from the bars and noted in the legend. Panel (b) shows the overall status
    distribution. Panel (c) shows the ten primary fields with the largest numbers of open-problem records, with
    bars segmented by status classification.


    3.3                What open problems have been solved?
    A particularly interesting question is whether AI is being used only for routine mathematical tasks or is
    already contributing to work on open research problems. Among the substantive-use papers, our review
    identifies 717 named open-problem records. These records span a wide range of mathematical fields and
    include problems proposed across many decades, as summarized in Figure 2.
        Of the 717 open-problem records, 103 remain open and 93 are partially resolved. A much larger group,
    510 records, are labeled as fully resolved: 329 as resolved true and 181 as resolved false; the remaining 11 are
    classified as unclear. These labels are assigned by the LLM-based review from the authors’ own descriptions
    in the manuscripts and do not constitute independent mathematical verification of the claimed resolutions.
    Among the records labeled as fully resolved, proofs of the conjectured statement are more common than
    counterexamples or disproofs. These results indicate that substantive AI use is already extending beyond
    established mathematics to work on unresolved research questions.
        The open-problem records are also highly concentrated across fields. Combinatorics accounts for by far
    the largest number, followed by Number Theory, Algebraic Geometry, and Probability; see Figure 2(c). This


                                                                                                7
pattern broadly mirrors the field distribution of substantive AI use reported above, suggesting that the areas
currently adopting AI most actively are also among those where AI is being applied most frequently to open
research problems.
    The proposed years also span a remarkably wide range; see Figure 2(a). Among the 329 records with a
reported proposed year, 92 date to before 2000, including 68 before 1990, while many others concern much
more recent problems. In particular, 36 records correspond to problems proposed in 2026 itself. Thus, the
sample includes both long-standing conjectures and newly posed research questions. Because the proposed
year is not reported for 388 records, however, this distribution should be interpreted only among problems
with an identifiable proposed date.


Table 4: The 50 earliest proposed open-problem records satisfying three criteria: substantive AI use, an
available proposed year, and a reported full resolution. Records are ordered by proposed year.

      arXiv ID     Conjecture                           Sub-fields              Proposed   Outcome     AI model
  1 2604.09808 Ramanujan Nagell theorem                 math.NT                  1913       proved     Anthropic Claude Code; Aristotle AI
                                                                                                       Aristotle
  2 2608.15904 Characterization of entrywise            math.CA; math.FA         1925       proved     OpenAI ChatGPT 5.6 Sol
               positivity preservers in fixed
               dimension
  3 2608.13536 Banach isometric conjecture                  math.FA; math.DG;    1932       proved     OpenAI ChatGPT 5.5 Pro; OpenAI
                                                            math.MG                                    ChatGPT 5.6 Pro; OpenAI GPT 5.6 Sol
  4   2608.12561   Borsuk’s problem                         math.MG; math.CO     1933      disproved   OpenAI GPT-5.6 Sol
  5   2608.15681   Erdos Problem                            math.NT              1943       proved     OpenAI ChatGPT-5.6
  6   2605.20695   Erdos unit distance conjecture           math.CO; math.NT     1946      disproved   OpenAI Chat GPT
  7   2605.28793   Erdos conjecture that r(s,k) is at least math.CO              1947       proved     not specified
                   k^(s-1) up to polylogarithmic factors
  8 2607.24483     Bellman’s lost-in-a-forest problem math.MG                    1956       proved     Anthropic Claude Fable 5; OpenAI GPT
                                                                                                       5.6 Sol; Anthropic Claude Opus 5
  9 2607.14071 Erdos Conjecture On Complete Sets math.NT; math.CO                1961       proved     OpenAI ChatGPT 5.6
  10 2603.29961 Whether the fractional parts of alpha math.CO; math.NT           1964       proved     Openai GPT 5.4 Pro
                times the primes are well-distributed
  11 2607.12935 Lindenstrauss retraction problem      math.FA                    1964      disproved   OpenAI ChatGPT 5.6 Pro
  12 2605.00301 Erdos Sarkozy Szemeredi Problem math.NT; math.CO;                1966       proved     OpenAI GPT-5.4 Pro; OpenAI GPT-5.5
                1196                                  math.PR                                          Pro; OpenAI Codex; Math Inc Gauss;
                                                                                                       OpenAI ChatGPT
  13 2605.00301 Erdos Sarkozy Szemeredi Problem         math.NT; math.CO;        1966       proved     OpenAI GPT-5.4 Pro; OpenAI GPT-5.5
                1217                                    math.PR                                        Pro; OpenAI Codex; Math Inc Gauss;
                                                                                                       OpenAI ChatGPT
  14 2608.02852 Forsythe conjecture for restart length math.NA; math.DS;         1968       proved     GPT-5.6 Sol Ultra
                two                                    math.OC
  15 2607.22515 Rota’s conjecture for flats            math.CO                   1970      disproved   OpenAI ChatGPT 5.6 Pro
  16 2603.19215 R-equivalence of Manin’s diagonal math.AG; math.NT               1972       proved     Google DeepMind AlphaEvolve; Google
                cubic surface over Q 2 zeta 3                                                          DeepMind Gemini 3 Pro; Google
                                                                                                       DeepMind Gemini 3 Deep Think;
                                                                                                       Google DeepMind Gemini 2.5 Pro;
                                                                                                       Google DeepMind Gemini 3.1 Pro
  17 2607.14140 Cycle Double Cover Conjecture       math.CO                      1973       proved     OpenAI Codex
  18 2605.23837 Gale first move uniqueness question math.CO                      1974       proved     not specified
  19 2606.24872 Erdos Problem 768                   math.NT                      1974       proved     OpenAI ChatGPT; Harmonic Aristotle
  20 2608.07388 Sigma Lebesgue completion           math.FA                      1974      disproved   OpenAI GPT-5.5; Anthropic Claude
                problem                                                                                Opus 4.6
  21 2605.00301 Erdos Primitive Set Conjecture      math.NT; math.CO;            1976       proved     OpenAI GPT-5.4 Pro; OpenAI GPT-5.5
                Problem 164                         math.PR                                            Pro; OpenAI Codex; Math Inc Gauss;
                                                                                                       OpenAI ChatGPT
  22 2605.28781 sum-product conjecture          math.NT; math.CO                 1976      disproved   OpenAI GPT-5.5 Pro
  23 2607.20525 The Erdos Szemeredi Sum Product math.CO; math.NT                 1976      disproved   OpenAI GPT-5.5 Pro; OpenAI GPT-5.5;
                Conjecture over R                                                                      OpenAI GPT-5.5 Codex
  24 2606.13925 Grothendieck vanishing theorem  math.AG                          1977       proved     Anthropic Claude Code; Anthropic
                                                                                                       Claude; OpenAI Codex; Aristotle
  25 2608.16977 Erdos and Straus question on            math.CO                  1977       proved     gpt-oss-120b; gemini-3.5-flash;
                divisibility among binomial                                                            gemini-3.1-pro; gpt-5.5; opencode agent
                coefficients


                                                                       8
 Rank
    arXiv ID     Conjecture                          Sub-fields          Proposed   Outcome     AI model
 26 2604.11220 weaker form of Yau s uniformisation math.DG                1978       proved     OpenAI ChatGPT pro 5.2
               conjecture
 27 2608.08799 Delta Conjecture                    math.CO                1978       proved     OpenAI ChatGPT
 28 2605.08542 Erdos Problem 690                   math.NT                1979       proved     OpenAI gpt-5.4-pro; OpenAI gpt-5.5;
                                                                                                Anthropic Claude Opus 4.7
 29 2608.08118 Bernhart Kainen dispersability        math.CO              1979      disproved   OpenAI GPT-5.5; Anthropic Claude
               conjecture                                                                       Opus 4.7; Google Gemini 3 Flash;
                                                                                                Google Gemini 3.1 Pro; Anthropic
                                                                                                Claude Sonnet 4.6
 30 2607.13165 Brualdi Problem 3.7 Hamiltonicity math.CO                  1980       proved     Anthropic Claude; OpenAI GPT/Codex
               of interchange graphs
 31 2607.15419 Erdos and Graham question on large math.NT; math.CO        1980      disproved   ChatGPT
               sets with a+b not dividing 2ab
 32 2608.02126 The Kalton–Peck hyperplane         math.FA                 1980       proved     OpenAI GPT-5.5
               problem
 33 2608.08953 Planar Berenstein Conjecture       math.AP; math-ph;       1980      disproved   OpenAI ChatGPT 5.6
                                                  math.NA; math.SP
 34 2605.03066 Odifreddi Problem 3                math.LO                 1981      disproved   Google DeepMind Gemini Deep Think
 35 2606.24878 Whether g r is less than 3 r       math.CO                 1981       proved     OpenAI ChatGPT 5.5 Pro; Harmonic’s
                                                                                                Aristotle
 36 2608.08933 Kim Roush Conjecture                  math.CO              1981       proved     OpenAI GPT-5.6-sol; Anthropic Claude
                                                                                                Fable 5
 37 2608.16040 Chudnovsky Conjecture                 math.AG; math.AC     1981       proved     OpenAI ChatGPT-5.6 Sol
 38 2607.20816 Erdos Problem 906                     math.CV              1982       proved     OpenAI GPT-5.6 Sol
 39 2608.02327 Connes’ rigidity conjecture for ICC   math.OA; math.DS;    1982      disproved   GPT-5.6 Sol; Codex; Danus multi-agent
               property (T) groups.                  math.GR                                    research system
 40 2608.16040 Demailly Conjecture                   math.AG; math.AC     1982       proved     OpenAI ChatGPT-5.6 Sol
 41 2608.14438 Conjecture 1.2 Volume Growth          math.DG              1986       proved     OpenAI ChatGPT 5.6 Sol Ultra; OpenAI
                                                                                                Codex
 42 2608.14507 Gromov’s conjectured                  math.DG              1986       proved     OpenAI GPT-5.6 Sol with Ultra
               codimension-two volume growth                                                    reasoning efort; OpenAI Codex
               estimate
 43 2608.18068 Stein’s dimension free weak type      math.CA; math.AP     1986       proved     OpenAI ChatGPT GPT 5.6 Sol; OpenAI
               (1,1) problem                                                                    Codex CLI; Anthropic Claude Opus 5.0;
                                                                                                OpenAI Danus; OpenAI Rethlas
 44 2607.00359 Katz Problem On Equivalence Of        math.RA              1987       proved     MechMath Agent Team (MMAT)
               Generalized Airy Operators
 45 2608.13025 Foregger Sinkhorn tie point           math.CO              1987      disproved   OpenAI GPT-5.6-sol; Anthropic Claude
               conjecture                                                                       Fable 5
 46 2607.22988 Stanley’s rankwise lower-bound        math.CO              1988      disproved   TARS agent system
               conjecture
 47 2607.24541 Stanley Problem 4 on Differential     math.CO              1988      disproved   TARS agent system
               Posets
 48 2606.23659 Erdos Problem                         math.CO              1989       proved     OpenAI ChatGPT; OpenAI Codex;
                                                                                                Harmonic Aristotle
 49 2607.19192 Donoho Stark conjecture               math.CA; math.FA     1989       proved     OpenAI GPT 5.6 Sol; OpenAI GPT-5.5
                                                                                                Pro
 50 2608.15515 Talagrand’s convolution conjecture math.PR                 1989       proved     Odin Automatic AI Research Agent




    Table 4 provides a closer look at selected open-problem records. We restrict attention to records that
satisfy three criteria: the corresponding paper involves substantive AI use, the proposed year of the problem
is available, and the problem is classified as fully resolved. Among these records, we report the first 50 when
ordered by proposed year, from earliest to most recent. The “arXiv ID” column identifies the corresponding
submission; and “Sub-fields” lists all Mathematics subcategories associated with the submission, excluding
non-mathematics categories.
    Table 4 also has substantial overlap with existing online collections of open mathematical problems. Most
notably, 14 of the 50 entries are explicitly Erdős-related. These include Erdős Problem #90, the unit-distance
problem; Problem #986, concerning lower bounds for Ramsey numbers; Problems #1196 and #1217 of
Erdős–Sárközy–Szemerédi; and Problems #768, #164, #690, and #906. The table also contains the Erdős


                                                                  9
                                                                                         Substantive-use authors by number of papers
                                                                 2,312




                           Number of authors (log scale)
                                                           103
                                                                         315


                                                           102                 75

                                                                                    26
                                                                                         16
                                                           101                                6
                                                                                                      4
                                                                                                  3                               3
                                                                                                                            2
                                                                                                                        1                 1
                                                           100
                                                                  1      2     3    4    5    6   7   8   9 10 11 12 13 14 15 16 17 18 19 20
                                                                                                  Number of papers per author

Figure 3: Histogram of substantive-use manuscripts per canonical author. The vertical axis is on a logarithmic
scale.


conjecture on complete sets, the Erdős–Szemerédi sum-product conjecture, an Erdős–Straus question on
binomial coefficients, and an Erdős–Graham divisibility problem. Thus, the Erdős Problems collection
(Bloom, 2026) provides a particularly visible point of overlap between our observational sample and existing
repositories of research-level mathematical problems.
    These findings should, however, be interpreted cautiously. The resolution status is inferred by our
LLM-based review from the authors’ descriptions in the manuscripts and does not constitute independent
mathematical verification. A paper classified as resolving an open problem may later be found to contain an
error, overlap with prior work, or require further expert validation. Accordingly, we interpret these results
as evidence about the kinds of open-problem claims appearing in AI-assisted mathematics, rather than as a
definitive count of previously open problems solved by AI.

3.4   Who is using AI for mathematical research?
We next investigate who is participating in substantive AI-assisted mathematical research. The 1,712
substantive-use manuscripts in our sample involve 2,764 canonical authors and 744 university-level institu-
tions. Institution names were normalized to merge equivalent variants, such as “University of Cambridge”
and “Cambridge University.” We then examine how unevenly substantive AI use is distributed across authors,
institutions, and countries.
    The distribution is highly uneven across authors; see Figure 3. Among the 2,764 canonical authors, 83.6%
appear on only one substantive-use manuscript, and 11.4% appear on two. Thus, more than 95% of authors
appear on at most two substantive-use papers. Only a small minority contribute repeatedly: 75 authors
appear on three papers and 26 on four, while a handful of particularly active authors appear on more than ten
manuscripts, with the maximum reaching 20. Panel (c) of Figure 4 quantifies this concentration using Lorenz
curves and Gini coefficients. In the pooled substantive-use sample, the author-level Gini coefficient is 0.449.
The month-specific coefficients are 0.416, 0.371, 0.481, 0.378, 0.332, and 0.320 from March through August,
respectively. Thus, with the exception of May, monthly concentration is lower than in the pooled sample.
A natural reason is that pooling across months accumulates repeated contributions by the same authors: an
author who appears only once or twice within any given month may appear many times over the full study
period. Such repeated participation increases the dispersion of cumulative manuscript counts across authors
and therefore raises the pooled Gini coefficient.
    The geographic distribution is also highly concentrated; see Figure 4(a). To account for differences in
team size, we use weighted author counts: if a manuscript has m authors, each author contributes a weight
of 1/m. These author weights are then assigned to countries based on the authors’ recognized affiliations,
where multi-country affiliations are split fractionally, while unmatched author records are excluded from both


                                                                                                          10
            (a)        Country distribution
      United States                         33.7%                               (c)            Authors                                                (d)            Institutions




                                                 Cumulative share of papers




                                                                                                                       Cumulative share of papers
              China                         32.9%                             100%                                                                  100%
                                                                                         Overall (Gini = 0.449)                                                 Overall (Gini = 0.606)
    United Kingdom      7.7%                                                  80%
                                                                                         Mar (Gini = 0.416)
                                                                                         Apr (Gini = 0.371)                                         80%
                                                                                                                                                                Mar (Gini = 0.381)
                                                                                                                                                                Apr (Gini = 0.291)
                                                                                         May (Gini = 0.481)                                                     May (Gini = 0.421)
        Switzerland    5.5%                                                              Jun (Gini = 0.378)                                                     Jun (Gini = 0.462)
                                                                                         Jul (Gini = 0.332)                                                     Jul (Gini = 0.454)
             France 4.5%                                                      60%        Aug (Gini = 0.320)                                         60%         Aug (Gini = 0.471)
            Canada 4.2%                                                       40%                                                                   40%
        South Korea 3.8%
          Germany 3.5%                                                        20%                                                                   20%
              Japan 2.3%
                                                                               0%                                                                    0%
              Israel 2.0%                                                            0% 20% 40% 60% 80% 100%                                               0% 20% 40% 60% 80% 100%
                     0%          20%          40%                               Cumulative share of authors                                          Cumulative share of institutions
                                Percent
                                                         (b)                                                Leading institutions
            Massachusetts Institute of Technology                                                                                                                       35
    University of Science and Technology of China                                                                                                                     34
                                Stanford University                                                                                                                  33
                                  Peking University                                                                                                             31
                                         ETH Zurich                                                                                                   27
                                Tsinghua University                                                                                                   27
                          University Of Cambridge                                                                                                     27
                                 Harvard University                                                                                                  26
                               Princeton University                                                                          22
                  University of California, Berkeley                                                           18
                        Carnegie Mellon University                                                            17
                                   Fudan University                                                         16
                               New York University                                                         15
                                 Sichuan University                                                        15
                University of California, San Diego                                                      14
                                  Fuzhou University                                                     13
                  National University Of Singapore                                                      13
                              Shandong University                                                       13
                            University Of Michigan                                                      13
                               University Of Oxford                                                     13
                                                                     0                       10                   20                                       30                   40
                                                                                                                    Papers

Figure 4: Country, institution, and concentration summaries for the substantive-use sample. Panel (a) shows
the ten largest recognized country shares among author records; multi-country affiliations are split fractionally,
unmatched author records are excluded, and percentages are normalized over recognized country weight.
Panel (b) reports the leading normalized school-level institutions by unique substantive-use manuscripts,
with each manuscript counted at most once per institution. Panels (c) and (d) show author and institution
concentration in conventional Lorenz orientation, overlaying the pooled sample with monthly curves from
March through August 2026; each legend reports the corresponding Gini coefficient. For the institution
curves, unknown or non-school labels and papers without a known school are excluded.


the numerator and denominator; the reported percentages are therefore normalized over recognized country
assignments. Among the resulting recognized country weights, the United States accounts for 33.7% and
China for 32.9%, together representing about two-thirds of the total. The United Kingdom is a distant third at
7.7%, followed by Switzerland (5.5%), France (4.5%), and Canada (4.2%). Each of the remaining countries
accounts for less than 4%.
    Institutional participation is even more concentrated; see Figure 4(b) and (d). Among the 744 university-
level institutions, the Massachusetts Institute of Technology appears on the largest number of substantive-use
manuscripts (35), followed closely by the University of Science and Technology of China (34), Stanford Uni-
versity (33), and Peking University (31). ETH Zurich, Tsinghua University, and the University of Cambridge


                                                                                           11
                     (a)                              Company-level AI use and provider shares
                         OpenAI             1,188                                                      960                2,148
                      Anthropic      359    417                   776
                         Google 139 195 334
                          Other      108
                      DeepSeek      80
                                                                                                 Provider share
                       Microsoft 54
                        Alibaba 40
                      Harmonic 29                                                                  7.6%
                    Moonshot AI 17                                                             8.9%                      OpenAI
                                                                                                                         Anthropic
                             xAI 17                                                                                      Google
                                                                                                               57.4%     DeepSeek
                    Axiom Math 15                                                              20.7%                     Other
                                                                                                                         Unspecified company
                         Rethlas 4                                      Substantive
           Unspecified company 85 118                                   Non-substantive
                                 0                   500                 1000               1500                2000                 2500
                                                                                Articles
                         (b) OpenAI model distribution                                    (c) Anthropic model distribution
                        Other                                  43.4% (906)           Claude                                  34.2% (251)
                     ChatGPT                           31.4% (656)                    Other                           25.6% (188)
                        Codex           5.4% (113)                                  Opus 4.8             10.6% (78)
                  ChatGPT 5.5          4.5% (93)                                     Fable 5             10.0% (73)
                   GPT-5.5 Pro        3.6% (75)                                        Code           6.3% (46)
               ChatGPT 5.5 Pro        3.5% (73)                                     Opus 4.7        4.1% (30)
                   GPT-5.6 Sol        3.4% (71)                                     Opus 4.6       4.0% (29)
                      GPT-5.5        2.7% (56)                                    Sonnet 4.6      2.9% (21)
               ChatGPT 5.6 Sol       2.2% (46)                                       Opus 5       2.3% (17)
                             0%               20%          40%          60%                  0%         10% 20% 30% 40%
                                         Share within provider                                          Share within provider

Figure 5: Provider and model distributions in the confirmed-use sample. Panel (a) shows the number
of manuscripts associated with each provider, partitioned into substantive-use and non-substantive-only
manuscripts. The inset pie chart normalizes provider–manuscript associations across providers, so its
percentages differ from the manuscript-level prevalence reported in the text. Panels (b) and (c) show the
distributions of reported model labels within OpenAI and Anthropic, respectively. Provider and model
mentions are non-exclusive across manuscripts because a manuscript may name multiple providers or models.


each appear on 27 manuscripts. Each manuscript is counted at most once for a given institution, although a
manuscript with multiple institutional affiliations may contribute to multiple institutions. Panel (d) further
shows that the pooled institution-level Gini coefficient is 0.606, substantially higher than the corresponding
author-level coefficient of 0.449. The monthly institution-level coefficients are 0.381, 0.291, 0.421, 0.462,
0.454, and 0.471 from March through August, respectively, all below the pooled value. As with authors,
pooling across months accumulates repeated participation by the same institutions. Institutions that appear
regularly throughout the study period therefore separate increasingly from those that appear only occasionally,
producing greater concentration in the pooled sample.

3.5   Which AI systems are being used?
The use of AI systems is concentrated among a small number of providers. As show in Panel (a) of Figure 5,
OpenAI models appear in 2,148 of the 3,575 confirmed-use manuscripts (60.08%), followed by Anthropic


                                                                         12
in 776 (21.71%), Google in 334 (9.34%), and DeepSeek in 80 (2.24%). Other providers appear much less
frequently. Because a manuscript may report using models from more than one provider, these counts and
percentages are non-exclusive and need not sum to the total number of confirmed-use manuscripts.
    Panels (b)–(c) of Figure 5 show that reported usage is also concentrated within providers. For both
OpenAI and Anthropic, a small number of product or model labels account for a large share of the reported
mentions. Some labels, such as “ChatGPT” and “Claude,” are broad product names that may encompass
multiple underlying model versions, whereas others identify a specific model more precisely. The within-
provider distributions should therefore be interpreted as distributions of author-reported system names rather
than exact model-level market shares.

3.6   Article metrics across the archive and confirmed-use groups
Finally, Figure 6 compares several observable article characteristics across the full archive and the two
mutually exclusive confirmed-use groups. The full archive contains all 32,944 Mathematics submissions,
while the confirmed-use sample is divided into 1,712 substantive-use papers and 1,863 non-substantive-only
papers. The full archive therefore serves as a descriptive baseline and overlaps with both confirmed-use groups.
On average, papers in the full archive contain 1.93 pages, 105,756.9 extracted characters, and 26.36 references.
The corresponding means are 2.06 pages, 94,032.3 characters, and 22.22 references for substantive-use papers,
compared with 2.54 pages, 106,050.6 characters, and 25.54 references for non-substantive-only papers.
    Within the confirmed-use sample, substantive-use papers are therefore shorter on average than non-
substantive-only papers, by approximately 0.48 pages and 12,018 extracted characters, and contain about 3.3
fewer references. The permutation comparisons indicate statistically detectable differences in page count and
extracted text length, whereas the difference in reference count is not statistically significant.




Figure 6: Mean article metrics for all 32,944 Mathematics submissions (blue), the 1,712 confirmed-use
manuscripts with substantive use (orange), and the remaining 1,863 confirmed-use manuscripts with no
substantive-use label (green). The blue baseline is the full archive; the orange and green groups form a
mutually exclusive partition of the confirmed-use sample.

    One possible interpretation is that substantive AI assistance is currently more common in papers centered
on relatively focused mathematical arguments, whereas non-substantive AI use—such as language editing,
coding, and literature assistance—occurs across a broader range of manuscript types. These comparisons,
however, are purely descriptive and should not be given a causal interpretation. The two groups may differ
systematically in field, topic, authorship, paper type, or other characteristics, so the results do not imply that
substantive AI use itself causes manuscripts to be shorter or to contain fewer references.



                                                       13
4    Discussion and conclusion
Our results show that AI use in mathematical research is increasingly rapidly. Although language and
formatting remains the most common individual use, a substantial fraction of confirmed-use manuscripts
report AI involvement in proof construction, formalization, problem formulation, or other research tasks.
The evidence therefore suggests that AI is beginning to move beyond auxiliary assistance toward more
direct participation in mathematical research. This shift is especially visible in work on open problems. We
identify hundreds of named open-problem records among substantive-use manuscripts. These records should
not be interpreted as independently verified AI solutions, but they show that AI is already being used in
research directed at unresolved mathematical questions. Adoption is also highly uneven. Substantive AI
use is concentrated in certain mathematical fields, among a relatively small group of repeated users and
institutions, and within a few countries and model providers. We also observe descriptive differences between
substantive-use and non-substantive-only manuscripts, most clearly in manuscript length.
    Several limitations are important. First, our study measures disclosed AI use. Undisclosed use is not
observable from our data, so the reported prevalence should not be interpreted as the total prevalence of
AI use in mathematics. Second, our classifications are produced by an LLM-based review of authors’
descriptions and are therefore subject to classification error, although our ongoing manual validation is
designed to quantify this error. Third, institution and country assignments rely partly on normalized and
inferred affiliation information and should be interpreted as broad distributional summaries rather than precise
rankings. Most importantly, our classification of open-problem outcomes is not a substitute for peer review,
historical priority research, or independent verification of mathematical correctness.
    Despite these limitations, the evidence points to a rapidly changing research landscape. The relevant
question is no longer only whether AI systems can perform research-level mathematics, but increasingly
where, how, and by whom they are already being used to do so. The sharp growth observed over only six
months, together with the emergence of substantive use across many fields and research problems, suggests
that this transition is occurring on a timescale that warrants continued empirical monitoring. Repeating
this disclosure audit over time, together with stronger human validation and independent verification of
mathematical claims, would help determine whether the current “gold rush” represents a short-lived period of
experimentation or the beginning of a durable transformation in the practice of mathematical research.


Disclosure of AI Use
The authors used ChatGPT to assist with language editing, organization, and manuscript preparation. Codex
was used to assist with data collection, data processing, data analysis, and figure generation. All AI-assisted
outputs were reviewed by the authors, who take full responsibility for the final manuscript.


References
Mohammed Abouzaid, Nikhil Srivastava, Rachel Ward, and Lauren Williams. First proof second batch, 2026.

Noga Alon, Thomas F. Bloom, W. T. Gowers, Daniel Litt, Will Sawin, Arul Shankar, Jacob Tsimerman,
 Victor Wang, and Melanie Matchett Wood. Remarks on the disproof of the unit distance conjecture, 2026.

Jarod Alper, Michael J. Barany, Alain Chavarri Villarello, Sander Dahmen, Walter Dean, Karthik Ganapathy,
   Michael Harris, David Holmes, Mateja Jamnik, Steven Kelk, Bryna Kra, Ursula Martin, Bartosz Naskr˛ecki,
   Rodrigo Ochigame, Jim Portegies, and Johannes Schmitt. Leiden declaration on artificial intelligence and
   mathematics, June 2026. URL https://doi.org/10.5281/zenodo.20302944.


                                                      14
Levent Alpöge and Claude Fable 5. A counterexample to the jacobian conjecture in dimension three, 2026.
  Announced July 2026.

arXiv. Policy for authors’ use of generative ai language tools. arXiv Content Moderation Policy, 2026. URL
  https://info.arxiv.org/help/moderation/index.html. Accessed 19 August 2026.

Jeremy Avigad. Mathematicians in the age of AI, 2026.

Thomas F. Bloom. Erdős problems. https://www.erdosproblems.com/, 2026. Online database of
  problems posed by Paul Erdős.

Hu-Zi Cheng, Bin Sheng, Aaron Lee, Varun Chaudhary, Atanas G. Atanasov, Nan Liu, Yue Qiu, Tien Yin
 Wong, Yih-Chung Tham, and Ying-Feng Zheng. Have ai-generated texts from llm infiltrated the realm of
  scientific writing? a large-scale analysis of preprint platforms. bioRxiv, 2024. doi: 10.1101/2024.03.25.
  586710.

Claude. More than two thirds of the zeros of the riemann zeta function are simple and on the critical line,
  2026. Anthropic.

Johan Commelin, Mateja Jamnik, Rodrigo Ochigame, Lenny Taelman, and Akshay Venkatesh. Shaping the
  future of mathematics in the age of ai. Notices of the American Mathematical Society, 73(6):480–483,
  2026.

Qianyue Hao, Fengli Xu, Yong Li, and James Evans. Artificial intelligence tools expand scientists’ impact
  but contract science’s focus. Nature, 649:1237–1243, 2026. doi: 10.1038/s41586-025-09922-y.

Yongyuan He and Yi Bu. Academic journals’ AI policies fail to curb the surge in ai-assisted academic
  writing. Proceedings of the National Academy of Sciences, 123(9):e2526734123, 2026. doi: 10.1073/pnas.
  2526734123.

Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and
  Jacob Steinhardt. Measuring mathematical problem solving with the math dataset. In Advances in Neural
  Information Processing Systems, 2021.

Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z. Horváth, Goran Žužić, Eric Wieser, Aja Huang, Ju-
  lian Schrittwieser, Yannick Schroecker, Hussain Masoom, Ottavia Bertolli, Tom Zahavy, Amol Mandhane,
  Jessica Yung, Iuliya Beloshapka, Borja Ibarz, Vivek Veeriah, Lei Yu, Oliver Nash, Paul Lezeau, Salvatore
  Mercuri, Calle Sönne, et al. Olympiad-level formal mathematical reasoning with reinforcement learning.
  Nature, 651:607–613, 2026. doi: 10.1038/s41586-025-09833-y.

Tanya Klowden and Terence Tao. Mathematical methods and human thought in the age of AI, 2026.

Donald E. Knuth. Claude’s cycles, 2026. Stanford Computer Science Department.

Aitor Lewkowycz, Anders Andreassen, David Dohan, et al. Solving quantitative reasoning problems with
  language models. In Advances in Neural Information Processing Systems, 2022.

Weixin Liang, Yaohui Zhang, Zhengxuan Wu, Haley Lepp, Wenlong Ji, Xuandong Zhao, Hancheng Cao,
 Sheng Liu, Siyu He, Zhi Huang, Diyi Yang, Christopher Potts, Christopher D. Manning, and James Zou.
 Quantifying large language model usage in scientific papers. Nature Human Behaviour, 9(12):2599–2609,
 2025. doi: 10.1038/s41562-025-02273-8.

OpenAI. Ten advances in mathematics and theoretical computer science, 2026.

                                                    15
Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M. Pawan
  Kumar, Emilien Dupont, Francisco J. R. Ruiz, Jordan S. Ellenberg, Pengming Wang, Omar Fawzi,
  Pushmeet Kohli, and Alhussein Fawzi. Mathematical discoveries from program search with large language
  models. Nature, 625:468–475, 2024. doi: 10.1038/s41586-023-06924-6.

Peiyang Song, Kaiyu Yang, and Anima Anandkumar. Lean copilot: Large language models as copilots for
  theorem proving in lean. In Proceedings of the International Conference on Neuro-symbolic Systems,
  volume 288 of Proceedings of Machine Learning Research, pages 144–169. PMLR, 2025. URL https:
  //proceedings.mlr.press/v288/song25a.html.

Terence Tao. Mathematics in the age of ai, 2026. Essay based on a public lecture at the 2026 International
  Congress of Mathematicians.

Trieu H. Trinh, Yuhuai Wu, Quoc V. Le, He He, and Thang Luong. Solving olympiad geometry without
  human demonstrations. Nature, 625:476–482, 2024.




                                                   16
