                                         AI IDEs or Autonomous Agents? Measuring the Impact of Coding
                                                        Agents on Software Development
                                                          Shyam Agarwal                                                    Hao He                               Bogdan Vasilescu
                                                   Carnegie Mellon University                                Carnegie Mellon University                    Carnegie Mellon University
                                                  Pittsburgh, Pennsylvania, USA                             Pittsburgh, Pennsylvania, USA                 Pittsburgh, Pennsylvania, USA

                                         Abstract                                                                                1   Introduction
                                         Large language model (LLM) based coding agents increasingly act as                      The landscape of software development is rapidly changing with the
                                         autonomous contributors that generate and merge pull requests, yet                      growing use of AI-powered coding tools. Importantly, AI-assisted
                                         their real-world effects on software projects are unclear—especially                    development is not uniform: two distinct paradigms have emerged.
                                         compared with widely adopted IDE-based AI assistants. We present                        The first consists of pre-agentic IDE-based coding assistants
arXiv:2601.13597v2 [cs.SE] 27 Jan 2026




                                         a longitudinal causal study of agent adoption in open-source repos-                     such as early GitHub Copilot and Cursor, which integrate directly
                                         itories using staggered difference-in-differences with matched con-                     into developers’ environments to provide real-time code sugges-
                                         trols. Using the AIDev dataset, we define adoption as the first agent-                  tions and inline assistance [21, 23, 33]. These tools operate syn-
                                         generated pull request and analyze monthly repository-level out-                        chronously within the editing workflow, offering suggestions that
                                         comes spanning development velocity (commits, lines added) and                          developers can accept, modify, or reject as they type [24, 30].
                                         software quality (static-analysis warnings, cognitive complexity,                          The second, more recent paradigm involves IDE and web-based
                                         duplication, and comment density). Results show large, front-loaded                     coding agents—autonomous AI systems that operate at the repos-
                                         velocity gains only when agents are the first observable AI tool in a                   itory level to generate entire pull requests, implement features,
                                         project; repositories with prior AI IDE usage experience minimal or                     and make substantial code contributions with minimal human in-
                                         short-lived throughput increases. In contrast, quality risks are per-                   tervention. Tools such as OpenAI Codex [4], Anthropic’s Claude
                                         sistent across settings, with static-analysis warnings and cognitive                    Code Agent [2], Devin [6], and the Cursor Agent [5] exemplify this
                                         complexity rising by roughly 18% and 39%, indicating sustained                          emerging category, where AI systems act more like autonomous
                                         agent-induced technical debt even when velocity advantages fade.                        contributors. Unlike pre-agentic assistants that augment individual
                                         These heterogeneous effects suggest diminishing returns to AI as-                       coding sessions, coding agents can work asynchronously, poten-
                                         sistance and highlight the need for quality safeguards, provenance                      tially completing full features or bug fixes independently [37]. They
                                         tracking, and selective deployment of autonomous agents. Our find-                      differ from traditional assistants in at least four key dimensions:
                                         ings establish an empirical basis for understanding how agentic and                     (1) Autonomy—ability to complete tasks without continuous hu-
                                         IDE-based tools interact, and motivate research on balancing accel-                     man guidance; (2) Scope—operation across multiple files and entire
                                         eration with maintainability in AI-integrated development work-                         codebases; (3) Planning—breaking down requirements into subtasks
                                         flows. The replication package for this study is publicly available                     and executing multi-step solutions; and (4) Interaction—primarily
                                         at https://github.com/shyamagarwal13/agentic-coding-impact.                             contributing through pull requests rather than inline suggestions.
                                                                                                                                    Despite the growing use of agentic coding tools in open-source
                                         CCS Concepts                                                                            development, empirical research has largely focused on pre-agentic
                                                                                                                                 assistants, in part due to the recency of agentic tools as a tech-
                                         • Software and its engineering → Development frameworks and
                                                                                                                                 nology category. Existing evaluations of coding agents primarily
                                         environments; • Computing methodologies → Intelligent agents.
                                                                                                                                 rely on benchmarks without humans-in-the-loop [16], limiting in-
                                                                                                                                 sight into impacts on user experience and productivity [20]. In
                                         Keywords                                                                                contrast, pre-agentic coding assistants like GitHub Copilot have
                                         Autonomous coding agents, Agentic AI, AI-assisted programming,                          been extensively studied, with work documenting positive effects
                                         Software quality, Longitudinal study, Causal inference                                  on perceived productivity [20, 41, 47]. Research on Copilot spans
                                                                                                                                 productivity [22, 39, 48], code quality [32, 36, 46], and developer
                                         ACM Reference Format:                                                                   experience [29, 43], yet the impacts of autonomous, repository-level
                                         Shyam Agarwal, Hao He, and Bogdan Vasilescu. 2026. AI IDEs or Au-
                                                                                                                                 agents remain largely unexplored. This gap is concerning given
                                         tonomous Agents? Measuring the Impact of Coding Agents on Software
                                         Development. In 23rd International Conference on Mining Software Reposito-
                                                                                                                                 that agentic tools operate with greater autonomy, make larger-scale
                                         ries (MSR ’26), April 13–14, 2026, Rio de Janeiro, Brazil. ACM, New York, NY,           contributions, and introduce distinct challenges [38].
                                         USA, 5 pages. https://doi.org/10.1145/3793302.3793589                                      Understanding the impact of agentic coding tools is critical for
                                                                                                                                 several reasons. First, these tools are rapidly gaining traction in
                                                                                                                                 open-source development, with an increasing number of reposi-
                                                                                                                                 tories accepting AI-generated pull requests [44]. Second, the au-
                                                                                                                                 tonomous nature of agentic tools raises unique questions about code
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.
                                         MSR ’26, Rio de Janeiro, Brazil
                                                                                                                                 quality, maintainability, and technical debt that may not generalize
                                         © 2026 Copyright held by the owner/author(s).                                           from IDE-based tool studies [25]. Third, the scale of contributions,
                                         ACM ISBN 979-8-4007-2474-9/2026/04
                                         https://doi.org/10.1145/3793302.3793589
MSR ’26, April 13–14, 2026, Rio de Janeiro, Brazil                                                                                                                                                                                         Agarwal et al.


entire features versus individual code snippets, necessitates differ-     Table 1: Descriptive statistics of treated repositories by prior
ent evaluation frameworks and metrics [20]. Finally, as organiza-         AI exposure. AF repositories are older but smaller and less
tions consider adopting these tools, evidence-based understanding         popular, while IF repositories are more starred, forked, and
of their impact on development velocity and software quality be-          active; both exhibit substantial agentic contributions.
comes essential for informed decision-making [14, 19].
   In this paper, we use the AIDev dataset [28] to examine how agen-                 Outcome                                                   Mean (AF/IF)                    Min (AF/IF)                 Median (AF/IF)                   Max (AF/IF)
tic coding tools affect software development velocity and quality                    Age (days) †                                              1537.8/1215.2                     131/199                      1069/926                       6141/5570
at the repository level, reflecting their role as autonomous contrib-                Stars ††                                                  1460.9/8123.4                      10/10                        68/423                      48110/177379
                                                                                     Forks ††                                                   236.8/1340.2                       0/0                          12/120                      8940/45908
utors rather than inline assistants. Focusing on repository-level                    Pull Requests †                                            696.7/2146.0                      10/21                        122/740                      31836/35389
outcomes, rather than individual-level, captures the fundamentally                   Agentic Pull Requests †                                    121.5/101.5                       10/10                         28/37                        13462/912
different operational model of agentic tools. Prior work finds short-     Note: † as of November end; †† as in original dataset.
term velocity gains but also increased technical debt for repositories
adopting the Cursor AI IDE [25]. Using similar causal inference




                                                                          Number of Repositories
methods [18], we estimate the effects of adopting a wide range of                                  250
                                                                                                   200
agentic coding tools, comparing the development trajectories of                                                                                                                                                            147
                                                                                                                                                                                                                                          159
                                                                                                   150
repositories that used pre-agentic coding tools to those that directly                             100
adopted coding agents. Our methodology accounts for staggered                                      50
                                                                                                                                                                    11                          10
                                                                                                                                                                                                                                   51
                                                                                                                                                                                                                                                  38
                                                                                                                                                                                                                                                          50

                                                                                                             0     1       1     0       1     1       9     6             2       8     3             3       5     8                                           4
adoption, heterogeneous treatment effects, and time-varying con-                                    0




                                                                                                             07



                                                                                                                           09



                                                                                                                                         11



                                                                                                                                                       12



                                                                                                                                                                     01



                                                                                                                                                                                   02



                                                                                                                                                                                                 03



                                                                                                                                                                                                               04



                                                                                                                                                                                                                             05



                                                                                                                                                                                                                                            06



                                                                                                                                                                                                                                                           07
founders, enabling a causal assessment of the marginal impact of




                                                                                                               -



                                                                                                                             -



                                                                                                                                           -



                                                                                                                                                         -



                                                                                                                                                                       -



                                                                                                                                                                                     -



                                                                                                                                                                                                   -



                                                                                                                                                                                                                 -



                                                                                                                                                                                                                               -



                                                                                                                                                                                                                                              -



                                                                                                                                                                                                                                                             -
                                                                                                            24



                                                                                                                          24



                                                                                                                                        24



                                                                                                                                                      24



                                                                                                                                                                    25



                                                                                                                                                                                  25



                                                                                                                                                                                                25



                                                                                                                                                                                                              25



                                                                                                                                                                                                                            25



                                                                                                                                                                                                                                           25



                                                                                                                                                                                                                                                          25
                                                                                                         20



                                                                                                                       20



                                                                                                                                     20



                                                                                                                                                   20



                                                                                                                                                                 20



                                                                                                                                                                               20



                                                                                                                                                                                             20



                                                                                                                                                                                                           20



                                                                                                                                                                                                                         20



                                                                                                                                                                                                                                        20



                                                                                                                                                                                                                                                       20
                                                                                                                                                                               Year-Month
autonomous coding agents. Our research addresses:
                                                                                                                           Repositories without prior AI traces (AF)                                 Repositories with prior AI traces (IF)
     • RQ1: Development Velocity Impact — How does the adop-
       tion of coding agents affect development velocity?
     • RQ2: Software Quality Impact — How does the adoption
       of coding agents affect software quality?                          Figure 1: Monthly distribution of agent adoption dates, sepa-
     • RQ3: Prior AI Exposure and Transition Effects — How                rated by prior AI exposure. Most adoptions occur between
       do the effects of adopting coding agents differ between repos-     May–July 2025.
       itories with and without prior IDE-based AI assistance?

    Our contributions are twofold: (1) We replicate and extend prior      3                              Methods
results on newer data and a broader ecosystem of autonomous cod-
                                                                          We estimate the causal effects of adopting LLM-based coding agents
ing agents, providing the first large-scale longitudinal evidence on
                                                                          on project-level development velocity and software quality using
agentic contributions at the repository level, and (2) We provide the
                                                                          a quasi-experimental difference-in-differences (DiD) design with
first causal evidence on the differential effects of transitioning from
                                                                          staggered adoption. Our empirical strategy, outcome definitions,
IDE-based AI assistants to autonomous coding agents, showing
                                                                          matching procedure, and estimation methods follow similar work
how prior AI tool adoption affects both velocity and code quality.
                                                                          on Cursor adoption [25], unless otherwise specified, enabling di-
                                                                          rect comparability. We summarize the methodology and highlight
2    Related Work                                                         deviations specific to coding agents.
Prior work evaluates AI coding tools using development veloc-
ity and software quality metrics. Velocity has been measured via          3.1                               Data Collection and Treatment Definition
task completion time [35], code volume and throughput [27], and           We build on the AIDev dataset (v3) [28], which links GitHub repos-
cycle-time reductions [22]. Quality outcomes span security vul-           itories to AI-generated pull requests and provides explicit evidence
nerabilities [36], code churn and revision requirements [44], static      of agentic contributions (e.g., multi-file edits, autonomous refactor-
analysis warnings and code complexity [25], and broader indicators        ings, test and documentation generation). For each repository, we
of technical debt. Methodologically, studies employ randomized            define the agent adoption date as the earliest month containing an
trials [35], observational field studies [22], and quasi-experimental     agent-attributed PR. Because AIDev coverage begins in December
designs including difference-in-differences [25].                         2024 while most agentic tools were released earlier that year, we mit-
   The vast majority of real-world research focuses on IDE-based          igate left-censoring by retrospectively parsing all PRs from January
AI assistants [15, 17, 22, 31, 32, 34, 36, 39, 40, 44–46], typically      2024 through November 2025, ensuring that the earliest observed
reporting modest velocity improvements [25, 26, 41, 47]. In con-          agentic PR closely approximates true adoption timing—crucial for
trast, early studies of agentic tools show mixed results: maintainers     valid temporal ordering in our staggered DiD design.
merge the majority of Claude Code pull requests (83.8% of 567) [42],         We extend the original agent taxonomy (Claude [2], Copilot [7],
yet controlled experiments with tools such as Cursor find limited         Cursor [5], Devin [6], Codex [4]) to mutually exclusive labels: hu-
productivity benefits for experienced open-source developers [16],        man, bot, codex [4], devin [6], jules [8], cursor [5], claude [2], copilot
potentially due to over-optimism, unreliability, and high task com-       [7], openhands [9], codegen [3], cosine [10], and tembo [12]. Attribu-
plexity. These inconsistencies underscore the need for longitudinal       tion follows a cascading strategy prioritizing agent-specific signals
evidence on the real-world effects of autonomous coding agents.           before generic labels: (1) branch prefixes (e.g., cursor/, claude/ );
AI IDEs or Autonomous Agents? Measuring the Impact of Coding Agents on Software Development                                 MSR ’26, April 13–14, 2026, Rio de Janeiro, Brazil


(2) PR author logins (e.g., codegen-sh, tembo-io); (3) first-commit                 Table 2: The Borusyak et al. [18] estimated average post-
author names (e.g., google-labs-jules[bot], claude[bot]); (4) GitHub                adoption treatment effects of agentic coding tools separated
actor type bot; and (5) default classification as human. For Claude-                by prior AI exposure. The estimate and standard error are
specific attribution, we additionally search PR descriptions, com-                  log-transformed to facilitate easy comparison.
ments, and reviews for distinctive co-authorship patterns (“Gen-
erated with Claude Code”, optionally including “Co-Authored-By:                         Outcome                        𝛽 (AF / IF)      Std. Err. (AF / IF)   % Change (AF / IF)
Claude <no-reply@anthropic.com>”). This multi-signal approach                           Commits                      0.309∗∗∗ /0.030     (0.051)/(0.092)          36.25 / 3.06
                                                                                        Lines Added                 0.569∗∗∗ /–0.066     (0.103)/(0.189)         76.59 / –6.34
improves recall for agentic PRs lacking explicit bot authorship or                      Duplicate Line Density        0.076/–0.009       (0.044)/(0.056)         7.92 / –0.94
branch naming.                                                                          Comment Line Density         0.042/0.201∗∗∗      (0.028)/(0.055)          4.34 / 22.30
                                                                                        Static Analysis Warnings     0.163∗∗∗ /0.174     (0.048)/(0.114)         17.73 / 19.00
   By following this convention, we identified several misclassifica-                   Code Complexity             0.299∗∗∗ /0.357∗∗    (0.059)/(0.114)         34.85 / 42.87
tions and missing PRs in the original dataset (replication package).                Note: ∗ 𝑝 < 0.05; ∗∗ 𝑝 < 0.01; ∗∗∗ 𝑝 < 0.001.
Correctly recovering the earliest agentic PR is essential because
adoption timing determines treatment assignment in our causal
design; any remaining attribution errors primarily introduce noise                  come from SonarQube [11], contributor counts from version his-
in treatment timing rather than systematic bias, likely attenuating                 tory, and activity covariates from GHArchive [1]. These covariates
effects toward zero.                                                                are collected consistently for both treated and control repositories
   We restrict analysis to repositories with ≥10 stars to exclude toy               across the full observation window, ensuring comparable temporal
and spam projects and require ≥10 agentic PRs per treated repos-                    coverage and supporting adjustment for confounding dynamics
itory to ensure non-trivial exposure. Repositories are observed                     unrelated to agent adoption.
monthly before and after adoption, forming an unbalanced panel
with staggered timing. To examine moderation by prior AI usage,                     3.3       Causal Inference Strategy
we partition treated repositories into agent-first (AF), which show
no traces of AI IDEs throughout the collection time period, and                     We estimate effects using DiD with staggered adoption: later adopters
IDE-first (IF), which exhibit IDE activity prior to agent adoption.                 serve as controls for earlier adopters prior to adoption; never-
Prior IDE usage is detected monthly by scanning the most recent                     adopters provide additional counterfactuals. To address selection
commit for configuration artifacts associated with agent-enabled                    bias of control repositories and satisfy the conditional indepen-
IDEs (GitHub Copilot [7], Cursor [5], WindSurf [13]). A repository                  dence assumption to establish the quasi-experimental settings, we
is IF if such artifacts appear before its first agentic PR and AF if                perform propensity score matching prior to estimation. Propensity
they don’t exist at all. Analyses are conducted separately for AF                   scores use logistic regression over dynamic pre-treatment char-
and IF using control repositories that mirror the same IDE expo-                    acteristics, incorporating both activity levels (recent covariates)
sure pattern. Figure 1 shows both groups adopt primarily between                    and trajectories (lagged covariates) to capture whether repositories
April–June 2025, with AF more numerous. Table 1 shows AF repos                      are growing, declining, or stable. Specifically, we model adoption
are older but smaller and less popular, whereas IF repos are more                   likelihood using repository age at the month prior to observation,
starred, forked, and PR-active; both groups nonetheless exhibit                     six monthly covariate lags, and cumulative historical covariates,
substantial agentic PR volume, motivating separate analyses.                        enabling discrimination between repositories with similar recent ac-
   Our control set consists of all GitHub repositories with ≥10                     tivity but different long-term trends. Because candidates outnumber
stars at collection time. For each month with agent adoption, we                    adopters, we subsample at most 10,000 candidates/month, yield-
extract monthly activity series from GHArchive [1] for repositories                 ing propensity models with AUC 0.92–0.99. Treated repositories
with at least one event (age, active users, stars, forks, releases, pull            are matched to maximum three controls with similar propensity
requests, issues, comments, total events). Because inferring prior                  scores and the same primary language, ensuring comparable pre-
IDE exposure at this scale is initially infeasible, we first perform                adoption activity, exposure histories, and language-specific perfor-
propensity-score matching over the full control population without                  mance characteristics. We estimate average and dynamic treatment
conditioning on prior exposure. We then infer prior exposure only                   effects using the imputation-based DiD estimator of Borusyak et
for matched candidates and retain matched control sets that mirror                  al. [18], which avoids biases from traditional two-way fixed effects
treated repositories’ AF/IF status. After filtering, our heterogeneous              models under staggered adoption and heterogeneous effects. Event-
samples contain 401 AF repositories matched to 606 controls and                     study specifications are used to assess pre-treatment trends and
117 IF repositories matched to 73 controls.                                         to characterize how effects evolve over time. Standard errors are
                                                                                    clustered at the repository level. As in prior work, our estimates
                                                                                    should be interpreted as intent-to-treat effects of observable agent
3.2    Outcomes and Covariates                                                      adoption. While we cannot directly measure usage intensity or
We measure development velocity via monthly commit counts and                       developer-level interactions, staggered adoption and matching on
lines added; software quality via static-analysis warnings, duplicated-             pre-treatment dynamics strengthen the causal interpretation of our
line density, and cognitive complexity using SonarQube[11]. All                     findings.
outcomes are aggregated at the repository–month level. We control
for time-varying covariates: lines of code, repository age (days),                  4     Results and Discussion
contributors, stars received, issues opened, and issue comments                     Table 2 summarizes average post-adoption effects, while Figure 2
added in the observation month. Lines of code nd outcome metrics                    shows six-month dynamic estimates.
MSR ’26, April 13–14, 2026, Rio de Janeiro, Brazil                                                                                                                                                                                                  Agarwal et al.


                                    Commits                              Lines Added                          % Comment Lines                      Duplicated Lines Density                   Static Analysis Warnings                Cognitive/Code Complexity
                                                                                                                                            0.3                                       0.6

                                                            1                                      0.4
                                                                                                                                            0.2                                       0.4
                   0.5                                                                                                                                                                                                         0.5
Treatment Effect




                                                                                                                                            0.1                                       0.2
                                                            0                                      0.2
                   0.0
                                                                                                                                            0.0                                       0.0
                                                                                                                                                                                                                               0.0

                                                                                                   0.0                                     -0.1                                       -0.2
                   -0.5                                     -1

                                                                                                                                           -0.2                                       -0.4                                     -0.5
                          -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6        -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6         -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6          -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6            -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6          -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6
                                                                                                                           Months Relative to Agent Adoption
                                                                   Setting     Repositories without prior AI traces (AF) (n=401+606, obs=15664)           Repositories with prior AI traces (IF) (n=117+73, obs=3572)
                                                                                                         Filled dots: p < 0.05 (signiﬁcant), Hollow dots: p ≥ 0.05 (non-signiﬁcant)



Figure 2: Estimated post-adoption effects of agentic coding tools by prior AI exposure. AF repositories gain velocity and
accumulate maintainability risks; IF repositories show minimal velocity gains but comparable maintainability increases.


Development Velocity. Agentic tools substantially accelerate de-                                                                                  code. While additional comments can aid comprehension, they do
velopment only when introduced as a repository’s first observable                                                                                 not counterbalance persistent complexity growth. Relative to prior
AI tool. AF repos see large average gains (+36.3% commits; +76.6%                                                                                 work on AI IDEs [25], which finds modest productivity gains and
lines added), whereas IF repos show minimal changes (+3.1%; −6.3%).                                                                               mixed quality effects, these findings suggest autonomous agents
Dynamics reveal a sharper contrast: AF repositories experience                                                                                    amplify the speed–maintainability trade-off, and in AI-rich envi-
a spike at 𝑡=0 (about +111% commits; +216% lines added) and                                                                                       ronments may magnify complexity without delivering sustained
persistently elevated activity, with lines added remaining roughly                                                                                velocity benefits. We also observe isolated significant pre-treatment
+49–+109% through 𝑡=6. IF repositories show only a short-lived                                                                                    coefficients in static-analysis warnings and code complexity, sug-
bump around adoption (commits +16–28% at 𝑡=0–2) before esti-                                                                                      gesting that untreated potential outcomes are not fully captured
mates return near zero and eventually turn negative (lines ∼ − 61%,                                                                               by additive fixed effects, reflecting systematic mean differences
commits ∼ − 35% by 𝑡=6).                                                                                                                          between treated and matched controls. These are not pervasive
   These patterns indicate that agentic tools act as high-throughput                                                                              enough to indicate a sustained pre-trend or clear violation of paral-
contributors primarily in new-to-AI workflows, but yield dimin-                                                                                   lel trends, but they are concerning and highlight a limitation of our
ishing returns in AI-saturated ones. AF repositories appear able to                                                                               quasi-experimental design and the underlying data.
harvest “first AI” acceleration, while IF repositories, having already                                                                            Implications and Ethical Considerations Autonomous coding
absorbed productivity gains from AI IDEs, likely face higher coor-                                                                                agents function as powerful but risky accelerators whose value de-
dination and integration costs that limit throughput. The greater                                                                                 pends on prior AI exposure: in our sample substantial front-loaded
maturity of IF repos (higher stars, forks, PR volume; from Table 1)                                                                               velocity gains materialize only when agents are a project’s first
likely constrains how aggressively agentic changes can be merged,                                                                                 AI tool; more broadly, velocity increases likely won’t suffice, and
so that localized speedups are offset by triage and review overhead.                                                                              AI adoption will need to be paired with strong quality safeguards
Overall, agent adoption yields sustained velocity gains only when                                                                                 (e.g., complexity-aware review of agent pull requests, routine refac-
not preceded by IDE-based AI tooling.                                                                                                             toring, comprehensive automated tests) to prevent accumulating
Software Quality. Regardless of prior AI exposure, adoption is                                                                                    complexity debt. Teams using AI IDEs should not assume addi-
associated with increased maintainability risks. Across both AF                                                                                   tive productivity and may instead deploy agents selectively or for
and IF repositories, static-analysis warnings rise by about 18% and                                                                               tightly scoped tasks. Persistent complexity growth underscores
cognitive complexity by roughly 39% (Table 2). Dynamics show                                                                                      the need to surface maintainability metrics directly in agent plan-
persistent complexity accumulation: AF repos increase +20.7% at                                                                                   ning and prompting, while modulating behavior according to exist-
𝑡=0 and reach ∼ + 49% by 𝑡=5, while IF repositories become signifi-                                                                               ing AI usage. Ethically, increased automation shifts accountability
cantly elevated as early as 𝑡=−2 and remain ∼ + 15–+62% through                                                                                   and maintainability burdens; provenance tracking, transparency
𝑡=6. Warning growth is somewhat noisier but similarly persistent                                                                                  of agent-generated changes, and review practices that emphasize
(∼ +22–+31% in AF by 𝑡=4–5; IF values consistently positive around                                                                                human oversight are still essential to avoid debt.
+25% at 𝑡=4–6).
   These simultaneous increases in complexity and warnings, even                                                                                  5     Conclusion
when net velocity gains are weak or negative (IF), indicate agent-                                                                                Autonomous agents offer meaningful velocity gains only in new-to-
induced complexity debt: agents accelerate the introduction of code                                                                               AI settings while consistently raising complexity and warning levels
that raises long-term cognitive and maintenance load. Duplication                                                                                 across contexts, reinforcing a speed–maintainability trade-off. Prior
effects are small and inconsistent, suggesting quality risks stem                                                                                 exposure to AI IDEs moderates benefits but not risks, underscoring
from structural complexity rather than copy–paste proliferation.                                                                                  the need for selective deployment and active oversight. Future
Comment density diverges across groups: IF repositories show                                                                                      work should follow post-adoption trajectories over longer horizons
substantial and sustained increases (about +22% on average and                                                                                    and examine collaborative patterns that balance acceleration with
> + 30% by 𝑡=6), whereas AF effects are muted, hinting that teams                                                                                 sustained code quality.
already using AI IDEs rely on agents for documentation as well as
AI IDEs or Autonomous Agents? Measuring the Impact of Coding Agents on Software Development                                  MSR ’26, April 13–14, 2026, Rio de Janeiro, Brazil


References                                                                               [29] Jenny T Liang, Chenyang Yang, and Brad A. Myers. 2023. A Large-Scale Survey
 [1] 2011. GHArchive. Retrieved Nov 30, 2024 from https://www.gharchive.org/                  on the Usability of AI Programming Assistants: Successes and Challenges. 2024
 [2] 2025. Claude Code | Claude. Retrieved Nov 30, 2025 from https://claude.com/              IEEE/ACM 46th International Conference on Software Engineering (ICSE) (2023),
     product/claude-code                                                                      616–628.
 [3] 2025. Codegen | The OS for Code Agents. Retrieved Nov 30, 2025 from https:          [30] Hussein Mozannar, Gagan Bansal, Adam Fourney, and Eric Horvitz. 2022. Reading
     //codegen.com/                                                                           Between the Lines: Modeling User Behavior and Costs in AI-Assisted Program-
 [4] 2025. Codex | OpenAI. Retrieved Nov 30, 2025 from https://openai.com/codex/              ming. ArXiv abs/2210.14306 (2022).
 [5] 2025. Cursor - The AI Code Editor. Retrieved Nov 30, 2025 from https://www.         [31] Kevin KB Ng, Liyana Fauzi, Leon Leow, and Jaren Ng. 2024. Harnessing the
     cursor.com/                                                                              Potential of Gen-AI Coding Assistants in Public Sector Software Development.
 [6] 2025. Devin | The AI Software Engineer. Retrieved Nov 30, 2025 from https:               ArXiv abs/2409.17434 (2024).
     //devin.ai/                                                                         [32] Nhan Ton Nguyen and Sarah Nadi. 2022. An Empirical Evaluation of GitHub
 [7] 2025. GitHub Copilot · Your AI pair programmer. Retrieved Nov 30, 2025 from              Copilot’s Code Suggestions. 2022 IEEE/ACM 19th International Conference on
     https://github.com/features/copilot                                                      Mining Software Repositories (MSR) (2022), 1–5.
 [8] 2025. Jules - An Autonomous Coding Agent. Retrieved Nov 30, 2025 from               [33] Ruchika Pandey, Prabhat Singh, Raymond Wei, and Shaila Shankar. 2024. Trans-
     https://jules.google/                                                                    forming Software Development: Evaluating the Efficiency and Challenges of
 [9] 2025. OpenHands. Retrieved Nov 30, 2025 from https://app.all-hands.dev/                  GitHub Copilot in Real-World Projects. ArXiv abs/2406.17910 (2024).
[10] 2025. Self sufficient agentic AI software engineer | Cosine AI. Retrieved Nov 30,   [34] Elise Paradis, Kate Grey, Quinn Madison, Daye Nam, Andrew Macvean, Vahid
     2025 from https://cosine.sh/                                                             Meimand, Nan Zhang, Ben Ferrari-Church, and Satish Chandra. 2024. How
[11] 2025. SonarQube Community Build Documentation. Retrieved Nov 30, 2025 from               Much Does AI Impact Development Speed? an Enterprise-Based Randomized
     https://docs.sonarsource.com/sonarqube-community-build/                                  Controlled Trial. 2025 IEEE/ACM 47th International Conference on Software Engi-
[12] 2025. Tembo — Delegate work to any coding agent. Retrieved Nov 30, 2025 from             neering: Software Engineering in Practice (ICSE-SEIP) (2024), 618–629.
     https://www.tembo.io/                                                               [35] Elise Paradis, Ambar Murillo, Maulishree Pandey, Sarah D’Angelo, Andrew
[13] 2025. Windsurf - The best AI for Coding. Retrieved Nov 30, 2025 from https:              Macvean, Ben Ferrari-Church, and Matthew Hughes. 2025. Creating bench-
     //windsurf.com                                                                           markable components to measure the quality of AI-enhanced developer tools.
[14] Magnus Chukwuebuka Ahuchogu, Pravin Ganpatrao Gawande, Dr Charu Mohla,                   Proceedings of the Extended Abstracts of the CHI Conference on Human Factors in
     Dr. Deepak A. Vidhate, and Nidal Al Said. 2025. Evaluating the Impact of Gener-          Computing Systems (2025).
     ative AI on Intelligent Programming Assistance and Code Quality. Power System       [36] Hammond A. Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, and
     Technology (2025).                                                                       Ramesh Karri. 2021. Asleep at the Keyboard? Assessing the Security of GitHub
[15] Owura Asare, Meiyappan Nagappan, and Nirmal Asokan. 2022. Is GitHub’s                    Copilot’s Code Contributions. 2022 IEEE Symposium on Security and Privacy (SP)
     Copilot as bad as humans at introducing vulnerabilities in code? Empirical               (2021), 754–768.
     Software Engineering 28 (2022), 1–24.                                               [37] Abhik Roychoudhury. 2025. Agentic AI for Software: thoughts from Software
[16] Joel Becker, Nate Rush, Elizabeth Barnes, and David Rein. 2025. Measuring the            Engineering community. ArXiv abs/2508.17343 (2025).
     Impact of Early-2025 AI on Experienced Open-Source Developer Productivity.          [38] Ranjan Sapkota, Konstantinos I. Roumeliotis, and Manoj Karkee. 2025. Vibe
     ArXiv abs/2507.09089 (2025).                                                             Coding vs. Agentic Coding: Fundamentals and Practical Implications of Agentic
[17] Marta Borek and Robert Nowak. 2025. Quality evaluation of Tabby coding                   AI. ArXiv abs/2505.19443 (2025).
     assistant using real source code snippets. ArXiv abs/2504.08650 (2025).             [39] Md. Istiak Hossain Shihab, Christopher Hundhausen, Ahsun Tariq, Summit
[18] Kirill Borusyak, Xavier Jaravel, and Jann Spiess. 2021. Revisiting event study           Haque, Yunhan Qiao, and Brian Mulanda. 2025. The Effects of GitHub Copilot on
     designs: robust and efficient estimation.                                                Computing Students’ Programming Effectiveness, Efficiency, and Processes in
[19] Eric W. Bridgeford, Iain Campbell, Zijao Chen, Zhicheng Lin, Harrison Ritz,              Brownfield Coding Tasks. Proceedings of the 2025 ACM Conference on International
     Joachim Vandekerckhove, and R.A. Poldrack. 2025. Ten Simple Rules for AI-                Computing Education Research V.1 (2025).
     Assisted Coding in Science. ArXiv abs/2510.22254 (2025).                            [40] Antero Taivalsaari, Tommi Mikkonen, and Cesare Pautasso. 2025. On the Fu-
[20] Valerie Chen, Ameet Talwalkar, Robert Brennan, and Graham Neubig. 2025.                  ture of Software Reuse in the Era of AI Native Software Engineering. ArXiv
     Code with Me or for Me? How Increasing AI Automation Transforms Developer                abs/2508.19834 (2025).
     Workflows. ArXiv abs/2507.08149 (2025).                                             [41] Priyan Vaithilingam, Tianyi Zhang, and Elena L. Glassman. 2022. Expectation
[21] Ruijia Cheng, Ruotong Wang, Thomas Zimmermann, and Denae Ford. 2022. “It                 vs. Experience: Evaluating the Usability of Code Generation Tools Powered by
     would work for me too”: How Online Communities Shape Software Developers’                Large Language Models. CHI Conference on Human Factors in Computing Systems
     Trust in AI-Powered Code Generation Tools. ACM Transactions on Interactive               Extended Abstracts (2022).
     Intelligent Systems 14 (2022), 1 – 39.                                              [42] Miku Watanabe, Hao Li, Yutaro Kashiwa, Brittany Reid, Hajimu Iida, and Ahmed E
[22] Lena Chretien and Nikolas Albarran. 2024. Impact of AI-tooling on the Engineer-          Hassan. 2025. On the use of agentic coding: An empirical study of pull requests
     ing Workspace. ArXiv abs/2406.07683 (2024).                                              on GitHub. CoRR abs/2509.14745 (2025).
[23] Mariana Coutinho, Lorena Marques, Anderson Santos, Marcio Dahia, César              [43] Justin D. Weisz, Shraddha Kumar, Michael J. Muller, Karen-Ellen Browne, Arielle
     França, and Ronnie de Souza Santos. 2024. The Role of Generative AI in Software          Goldberg, Katrin Ellice Heintze, and Shagun Bajpai. 2024. Examining the Use
     Development Productivity: A Pilot Case Study. Proceedings of the 1st ACM                 and Impact of an AI Code Assistant on Developer Productivity and Experience
     International Conference on AI-Powered Software (2024).                                  in the Enterprise. Proceedings of the Extended Abstracts of the CHI Conference on
[24] Emanuela Guglielmi, Venera Arnoudova, Gabriele Bavota, Rocco Oliveto, and                Human Factors in Computing Systems (2024).
     Simone Scalabrino. 2025. How do Copilot Suggestions Impact Developers’ Frus-        [44] Tao Xiao, Youmei Fan, Fabio Calefato, Christoph Treude, Raula Gaikovina Kula,
     tration and Productivity? ArXiv abs/2504.06808 (2025).                                   Hideaki Hata, and Sebastian Baltes. 2025. Self-Admitted GenAI Usage in Open-
[25] Hao He, Courtney Miller, Shyam Agarwal, Christian Kastner, and Bogdan                    Source Software. ArXiv abs/2507.10422 (2025).
     Vasilescu. 2026. Speed at the Cost of Quality: How Cursor AI Increases Short-Term   [45] Feiyang Xu, Poonacha K. Medappa, Murat Mustafa Tunç, Martijn Vroegindeweij,
     Velocity and Long-Term Complexity in Open-Source Projects. In International              and Jan C Fransoo. 2025. AI-assisted Programming May Decrease the Produc-
     Conference on Mining Software Repositories (MSR).                                        tivity of Experienced Developers by Increasing Maintenance Burden. ArXiv
[26] Saki Imai. 2022. Is GitHub Copilot a Substitute for Human Pair-programming?              abs/2510.10165 (2025).
     An Empirical Study. 2022 IEEE/ACM 44th International Conference on Software         [46] Burak Yetistiren, Isik Ozsoy, and Eray Tüzün. 2022. Assessing the quality of
     Engineering: Companion Proceedings (ICSE-Companion) (2022), 319–321.                     GitHub copilot’s code generation. Proceedings of the 18th International Conference
[27] Anand Kumar, Vishal Khare, Deepak Sharma, Satyam Kumar, Vijay Saini, Anshul              on Predictive Models and Data Analytics in Software Engineering (2022).
     Yadav, Sachendra Jain, Ankit Rana, Pratham Verma, Vaibhav Meena, and Avinash        [47] Albert Ziegler, Eirini Kalliamvakou, Shawn Simister, Ganesh Sittampalam, Alice
     Edubilli. 2025. Intuition to Evidence: Measuring AI’s True Impact on Developer           Li, Andrew Rice, Devon Rifkin, and Edward Aftandilian. 2022. Productivity
     Productivity. ArXiv abs/2509.19708 (2025).                                               assessment of neural code completion. Proceedings of the 6th ACM SIGPLAN
[28] Hao Li, Haoxiang Zhang, and Ahmed E. Hassan. 2025. The Rise of AI Team-                  International Symposium on Machine Programming (2022).
     mates in Software Engineering (SE) 3.0: How Autonomous Coding Agents Are            [48] Albert Ziegler, Eirini Kalliamvakou, LI X.ALICE, Andrew Rice, Devon Rifkin,
     Reshaping Software Engineering. arXiv preprint arXiv:2507.15003 (2025).                  Shawn Simister, Ganesh Sittampalam, and Edward Aftandilian. 2024. Measuring
                                                                                              GitHub Copilot’s Impact on Productivity. Commun. ACM 67 (2024), 54 – 63.
