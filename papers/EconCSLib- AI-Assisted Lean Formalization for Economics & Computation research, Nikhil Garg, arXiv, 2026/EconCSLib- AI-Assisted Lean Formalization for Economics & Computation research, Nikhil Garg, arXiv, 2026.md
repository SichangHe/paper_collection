                                                 E CON CSL IB : AI-A SSISTED L EAN F ORMALIZATION FOR
                                                        E CONOMICS & C OMPUTATION R ESEARCH


                                                                                             Nikhil Garg
                                                                                            Cornell Tech
                                                                            Operations Research & Information Engineering
                                                                                        ngarg@cornell.edu
arXiv:2606.13306v2 [cs.GT] 2 Jul 2026




                                                                                               July 3, 2026



                                                                                              A BSTRACT
                                                   This paper presents E CON CSL IB, a Lean 4 library and workflow for formalizing research papers
                                                   in applied modeling fields such as Economics and Computation, with language-model assistance.
                                                   The goal of E CON CSL IB is to enable researchers to formalize their papers in Lean without knowing
                                                   Lean themselves. The central design principle is a human-AI-Lean formalization workflow: an LLM
                                                   writes Lean code, Lean checks formal statements and proofs, and both humans and LLM-as-judge
                                                   processes can verify that the paper’s statements were translated into Lean correctly. We develop agent
                                                   skills, human-facing reporting, a review dashboard, and auditing procedures to support this workflow.
                                                   The current public repository contains 20 formalized papers and 4 partially formalized papers, along
                                                   with shared libraries for probability (including stochastic processes), auctions, matching markets,
                                                   social choice, and graph tools, totaling 986,391 lines of Lean code. To our knowledge, we are also
                                                   among the first applied math researchers to systematically pursue Lean formalization of one’s own
                                                   publications in the process of building such a community library.
                                                   We welcome users and contributors to the project. The library and workflow are available at
                                                   https://github.com/nikhgarg/EconCSLib, with corresponding project webpage at https:
                                                   //gargnikhil.com/EconCSLib/.

                                        Keywords Lean · AI-assisted formalization · Economics and Computation


                                        1       Introduction

                                        Lean is a formal verification language for mathematics. If a statement is written and compiled in Lean, then the Lean
                                        statement is correct up to its assumed premises (subject to Lean’s correctness). Formal verification holds great promise
                                        in guaranteeing the correctness of research papers with mathematical components. However, writing Lean code is
                                        tedious and difficult, and the libraries available in Lean have historically concentrated in pure mathematics. Thus,
                                        many areas of applied mathematics have not yet begun to be formalized, and formalization is out-of-reach for most
                                        researchers.
                                        Auto-formalization, through language models, is changing this.1 As of early 2026, the frontier large language models—
                                        e.g., GPT 5.5 Pro—became capable of writing Lean code at a level good enough to perform non-trivial verification of
                                        research: given a paper, translating its definitions, theorem statements, and proofs into Lean. Such writing of Lean code
                                        is arguably the ideal application of capable but error-prone AI: as long as the theorem statements and definitions are
                                        correctly translated from the intended statement (and this may be reasonably quickly checked by a human who can read
                                        Lean), the Lean compiler verifies that the proof code (potentially hundreds of thousands of lines) correctly proves those

                                            1
                                            The cost is non-trivial but manageable. Formalizing one paper takes about a full week’s quota on a GPT Pro with Max tier
                                        account, which as of this writing costs $200/month.
E CON CSL IB


translated statements – no human needs to check these lines.2 This human-AI-Lean workflow leverages the particular
strength of each agent. However, LLM agents cannot conduct trustworthy verification out-of-the-box, and starting from
scratch for each paper is prohibitively wasteful.
This paper presents E CON CSL IB – an AI-generated Lean library and corresponding LLM skills and a human validation
interface – to formalize Economics & Computation research. Our goal is to put auto-formalization within reach of
researchers in the field for their own papers, without needing to learn Lean. E CON CSL IB tackles two key challenges:
(a) building shared library infrastructure, encoding commonly used concepts across papers; (b) developing an auto-
formalization workflow and auditing tools, to increase autonomy and trust that a paper has actually been formalized.
E CON CSL IB is organized as follows. The central workflow is to verify a specific research paper using a language
model agent: given a paper’s LATEX source or PDF, the agent extracts the mathematical statements (definitions, lemmas,
theorems) and formalizes them in Lean, following the paper’s given proofs to the extent possible. Papers from
the community share many components, and so the workflow also builds a shared library: an individual paper’s
formalization can make use of this library, and the formalization agent “elevates” a statement from a paper’s code to the
shared library when it determines that it is likely to be useful for other papers.
This Lean code is supplemented with automated workflows and LLM skills to (1) aid AI agents in formalizing papers,
by maintaining shared lessons across papers; and (2) automatically audit via code that each paper’s formalization
follows best practices. These skills and workflow are being actively updated as we formalize papers, with the goal to
get close to full-automation of paper formalization. Most importantly, each paper’s formalization contains (3) a set of
artifacts to help humans understand the formalization status and verify that the paper’s statements have been translated
correctly into Lean. These artifacts include a Directed Acyclic Graph (DAG) visualizing the paper’s mathematical
statements and current formalization status (see Figure 1 for the DAG associated with a fully formalized paper); a
post-formalization report that documents the process such as whether the Lean proofs needed to deviate from the paper’s
approach or add additional assumptions, or whether any mistakes were found (see Section C); and a dashboard in which
a human can verify (and log) whether the paper’s statements were correctly translated into Lean (see Figure 2). This
last component, the dashboard to verify translation, is further supported by an LLM-as-judge module. These artifacts
are automatically generated and maintained by the formalization agent.
At present, the library has been used to fully formalize 20 papers; these include 14 papers by the author [GGSG19, GJ20,
LG21, GN22, PRP+ 24, GCG24, PGK25, DSWG25, MBJG25, GJ19, DGD26, GGRS26, DGJ24, DGJ26], and 6 other
prominent papers from the EconCS community [GS62, Rot82, GHW01, MSVV07, EOS07, KR21]. Another 4 papers
are partially formalized in the public repository, with the remaining formalization depending on infrastructure beyond
the current scope of E CON CSL IB and not yet available in other libraries [LOS02, LMMS04, LBG24, GKG+ 19]; two
require computational-complexity results, one requires Poisson process and stopping-time infrastructure, and one
requires stochastic subgradient descent convergence formalization. The shared library’s modules currently include
those for probability and optimization, matching markets, social choice theory, and auctions and mechanisms, among
others. We have especially focused on developing continuous probability tooling – as commonly used in EconCS and
Operations Research – but which is especially challenging in Lean.
I stress that this project is experimental and early days: while formal auto-verification of mathematical research
papers – aided by language models – is clearly valuable, it is unclear what role shared libraries like E CON CSL IB, and
E CON CSL IB in particular, will play. Furthermore, while we have built tools to help humans verify the paper statements’
translations into Lean code, this step is ultimately limited by having contributors with the requisite Lean expertise to
do so. Finally, and relatedly, it is unclear how to organize E CON CSL IB as an open source software project to which
anyone can contribute. One potential ultimate goal would be to allow others to use the workflow to formalize their own
papers of interest, and then contribute its formalization and potential library-level components back to E CON CSL IB.
Another goal could be to then, in turn, use this library as a basis for novel AI-generated proofs for EconCS papers.

Get started. To get started in formalizing your own paper, clone the repository and open an LLM agent tool (I use
Codex with GPT 5.5 in xhigh thinking mode). Give the agent the paper link, and ask it to formalize the paper using
the skill and workflow in the repository. And please feel free to reach out as you do so. The repository is available at
https://github.com/nikhgarg/EconCSLib, with project webpage at https://gargnikhil.com/EconCSLib/.

Contributions and organization. Overall, this paper makes three contributions. First, it introduces a public Lean
4 library for Economics & Computation, with reusable library infrastructure. Second, it presents a paper-oriented
formalization workflow in which each research paper has a compact paper-facing Lean interface, a dependency DAG, a
    2
      Of course, one needs to trust the Lean kernel/typechecker and its surrounding toolchain. In contrast, while frontier LLMs can
directly find errors in mathematical arguments, they cannot by themselves verify that a statement is correct, without a language such
as Lean; an LLM not finding an error is not sufficient evidence that there are no errors.


                                                                 2
E CON CSL IB


validation report, and dashboard- and LLM-as-judge-based translation review. Our formalization agent skills integrate
lessons from our own formalization and best practices from the literature, with the goal of near-fully-automated
formalization. Third, it reports an initial formalization case study, illustrating both the promise and the bottlenecks
of author-led AI-assisted formalization. To our knowledge, we are also among the first applied math researchers to
systematically pursue Lean formalization of one’s own publications in the process of building such a community library.
The rest of the paper is organized as follows. Section 2 discusses related work, and especially the substantial recent work
on LLM-based autoformalization in Lean. Section 3 describes the system architecture: shared library, paper-specific
artifacts, scripts, skills, and review dashboard. Section 4 summarizes the current formalization status and library
coverage, alongside next immediate steps. Section 5 discusses various aspects of auto-formalization and lessons learned.

2       Related Work
Lean ecosystem and formalization projects E CON CSL IB builds on the Lean ecosystem [DMKA+ 15, MU21], and
the mature, human-written, community-maintained mathematical library M ATHLIB [Mat20]. M ATHLIB and similar
projects emphasize that coordination and community workflows are as important as individual development in such
projects [vDEL20, BBC+ 25, BBB+ 25].
Domain-specific Lean projects now exist across several applied mathematics fields – these include in high energy
physics, chemical physics, and scientific computing [TS25, BSF+ 24, Skr26]. CSL IB is the closest analogue for
computer science [BCM+ 26], aiming to formalize core computer science theory concepts; we expect E CON CSL IB to
be a downstream user of CSL IB – for example, we are waiting to finish formalizing several papers until computational
complexity libraries are more mature. We note that these projects are largely (but not exclusively) human-written, and
aim to formalize central concepts as opposed to research papers in a specific field.
We aim to build a workflow for human-AI-Lean formalization, and apply this workflow to formalize EconCS papers
while building a library. Because of language model progress, substantial recent work has started on this path in
other domains [MYS+ 24, WMM+ 26, GRA+ 26, RPG+ 26, DHMN26, Ili26, Urb26], including workflows to formalize
scientific papers [MZF26, RLQ26]. Zhang, Lee, and Liu [ZLL26] formalize core statistical learning concepts in Lean,
using a Human-AI workflow. Many of these projects share workflow components with ours, including LLM generation
of Lean code, compiler-guided proof repair, and human-facing tools for checking whether informal statements have
been faithfully translated into formal statements. We note that many (but not all [RLQ26, DHMN26, Ili26]) of these
existing projects focus on formalizing the textbook canon of a field, as opposed to a research-paper driven approach.
To our knowledge, E CON CSL IB is among the first public Lean projects to make systematic author-led formalization
of research papers the organizing principle for a Lean library in an applied area. The M ATHLIB Initiative [Mat26]
aims to bring autoformalization closer to the math research frontier, and is developing a specification to make such
autoformalization more scalable and useful. We will adopt such a specification and its best practices.
Finally, we note that formalization has a longer history, including in game theory, cf. [BMS17]. Lean has also
grown beyond formalizing mathematical results, to formalizing neural network-based software at runtime [GCA+ 26],
cryptographic code in Rust [KTC26], and Lean itself [Car24].

Concurrent work: [BMJ+ 26] Independently and concurrently to this project, Bei et al. [BMJ+ 26] also develop a
Lean library entitled E CON CSL IB; both projects share substantial commonalities in aiming to ease Lean formalization
of EconCS ideas and research, through the development of a library with concepts that are shared across papers. Both
projects also make use of LLM tooling to support this goal.
The projects are highly complementary rather than redundant, stemming from a difference in philosophy.3 Bei et
al. [BMJ+ 26] have a tighter human-in-the-loop workflow aimed at correct and clean shared common abstractions – a
human Lean expert encodes the major definitions and statements, with proof support by an LLM. This enables, for
example, precisely stating open problems in the language of the domain library. Our project, on the other hand, has
a more automated workflow for formalizing research papers, with human-in-the-loop tooling aimed at ensuring that
research paper statements are translated correctly; shared library concepts are an outcome of paper-focused development,
and we do not pursue human curation or validation of the shared library concepts. In other words, the two projects
are on opposing ends of a speed–human curation tradeoff: Bei et al. [BMJ+ 26] requires humans who are experts
in Lean and EconCS, yielding a human-curated and validated shared library; our project, in contrast, aims to make
formalization of research papers accessible to researchers who do not know Lean, but in turn produces substantial
supporting library code that has not been human-validated.
    3
     I thank the authors of Bei et al. [BMJ+ 26] for discussion contributing to this note. We have also discussed potentially more
direct collaboration or integration in the future.


                                                                3
E CON CSL IB


In the future, we hope to be able to use the curated concepts from the library of Bei et al. [BMJ+ 26] in our project,
and researcher use of our project may help guide which concepts are most important for humans to curate in the project
of Bei et al. [BMJ+ 26] . Our E CON CSL IB project already preferentially uses results from M ATHLIB and CSL IB
(which are human curated) when available, for analogous reasons.

Autoformalization and theorem proving methods AI-assisted theorem proving and autoformalization is a growing
methodological field. Autoformalization asks (language) models to translate informal mathematics into formal
language [WJL+ 22, WDL+ 25, MCF+ 26]; multiple benchmarks now measure progress in the field [ZHP21, APS+ 23,
PAB+ 26]. Research considers how to best build autoformalization pipelines, including incorporating RAG, RL, and
fine-tuning [XLY+ 25, LDL+ 25, WHW+ 26, HJL+ 25, She26]. Others build richer workflows, such as how to create
proof blueprints, repair proofs using compiler feedback, improving translation of natural language statements into Lean
statements, creating dependency graphs, and Human-AI interfaces [ZMAW26, OFY26, JKT+ 26, WXW+ 25, CDY+ 25,
YS26, LWH+ 25, GWJ+ 25, YWG+ 24]. E CON CSL IB incorporates some of these lessons into its skills and workflows
(in particular, an LLM agent went through many of the above papers and integrated lessons into repository skill file).
Language models can go beyond formalizing human-written proofs into Lean – they can now generate novel
proofs [HRW+ 21, FRRB23, LLL+ 22, JWZ+ 22, JGJ+ 26, LTL+ 25a, LTL+ 25b, PHZ+ 22, PS20]; [ABH+ 26] seek
to evaluate this ability while preventing leakage. Substantial work builds on top of Lean, such as to train or fine-tune
language models to generate novel theorems [YSG+ 23, ASM+ 25, SYA24, RSS+ 25, XGS+ 24, WUL+ 25, MMG+ 26,
LDS+ 24]. Our hope is that E CON CSL IB can be used by such provers to prove novel EconCS results. Lean is also used
to provide supervision and generate synthetic data during training for LLM theorem provers [CGH+ 25, LSWY25].

3     E CON CSL IB Architecture
Here, we describe the system components in more detail.

3.1     Lean code

E CON CSL IB has two layers of Lean code. The reusable library layer, in EconCSLib/, contains paper-independent,
common definitions and results for areas such as probability, optimization, matching, auctions, online algorithms,
recommender systems, rankings, and fair division. The current library components are listed in Table 1. The research
layer, in papers/, has one folder per research paper; each folder is meant to audit and formalize a specific research
paper preserving source notation, theorem numbering, formal statements, and proof approach. Each paper folder also
contains the human-facing validation artifacts as described below.

3.2     Statement translation validation and human-in-the-loop workflow

The Lean code is not sufficient on its own. Researchers have to be able to verify that the Lean code actually has
formalized what the paper intended it to, be able to monitor progress, and understand the process’s outcome.

3.2.1    Human and agentic validation of translation
While the Lean compiler verifies that a given Lean statement can be derived from the axioms, it cannot confirm that
the paper’s intended mathematical statement was correctly translated to the Lean statement. This task must be done
outside Lean, and is where formalization errors are most common. Notably, a human does not need to validate every
Lean statement was correctly translated, just the paper facing statements – the Lean compiler can do the rest. Thus,
while the Lean proof files can extend to over a hundred thousand of lines, the workflow enforces that each paper has
a compact PaperInterface.lean file that just contains these paper-given definitions and theorem statements (but
not proofs). The translation verification task is thus to validate that the statements in these files correctly translate the
intended statements from the paper.
E CON CSL IB pursues two complementary approaches to validating this translation: (1) LLM-as-judge validation; (2) a
dashboard to support human understanding and validation. Both approaches save persistent logging documenting which
statements’ translations have been validated.

LLM validation The first validation layer is itself automated, via an LLM-as-judge approach. This validation has
three components: coverage, translation accuracy, and holistic audit. The first two components are at the individual
statement level: each mathematical statement from the paper is extracted into a table, and mapped to specific Lean
statements; then, an LLM-as-judge approach is used to validate that each source statement is covered by some Lean


                                                             4
E CON CSL IB




 Paper: User-item fairness tradeoffs in recommendations                                  Legend
 Authors: Sophie Greenwood, Sudalakshmee Chiniah, and Nikhil Garg
 Publication venue: NeurIPS 2024
 Year: 2024
 Formalized PDF: https://openreview.net/pdf?id=ZOZjMs3JTs
                                                                                                 formalized   formalized                      formalized          formalized
                                                                                                    result      lemma                          definition         with caveat




                                                                                                  partially                                                      not started /
                                                                                                              conditional                      scaffold
                                                                                                 formalized                                                     not formalized



                                              Problem 1 (Sec. 3)
                                            user-item fairness tradeoff
                                                 model formalized


                                                                             Problem 6 (App. D)                                                                Problem 11 (App. E)
                                                                               opposing-type LP                                                                three-type fairness LP
                                                                                  formalized                                                                     model formalized


         Example 1 (Sec. 4)
          two-item intuition
             formalized



                                                                              Lemma 4 (App. D)                       Lemma 9 (App. D)                          Lemma 12 (App. E)
                                                                             unique sparse solution                   qj (α) monotonicity                    symmetric reduction to S ′
                                                                                  formalized                               formalized                              formalized

                                              Lemma 1 (App. C)
                                                  ∗
                                                 Imin  > 0
                                                  formalized



                                                                             Lemma 5 (App. D)                                                                  Lemma 17 (App. E)
                                                                              closed-form policy                                                                right-half zero mass
                                                                                  formalized                                                                         formalized
                                              Lemma 2 (App. C)
                                               LP value reduction
                                                   formalized




                                                                              Lemma 6 (App. D)                      Lemma 10 (App. D)                          Lemma 13 (App. E)
                                                                             first-half type fairness               midpoint pivot bound                          pivot support
                                                                                    formalized                           formalized                                 formalized
                                             Proposition 1 (Sec. 3)
                                             LP-reduction framework
                                                   formalized




                                                                             Lemma 7 (App. D)                        Lemma 11 (App. D)                         Problem 12 (App. E)
                                                                              pivot monotonicity                   fixed-pivot monotonicity                        truncated LP
                                                                                  formalized                              formalized                             model formalized
                                             Proposition 2 (Sec. 3)
                                            symmetric sparse optimum
                                                   formalized




                                                                             Lemma 8 (App. D)                       Lemma 16 (App. E)                          Lemma 14 (App. E)
                                                                               interval stitching                    midpoint qj algebra                         unique optimum
                                                                                   formalized                            formalized                                 formalized
                                               Lemma 3 (App. D)
                                              unconstrained baseline
                                                   formalized




                                                                             Theorem 3 (Sec. 4)                                                                Lemma 15 (App. E)
                                                                          two-sided price monotonicity                                                          closed coordinates
                                                                            source wrappers closed                                                           center convention explicit




                                                                                                                                                            Theorem 4 (Sec. 5/App. E)
                                                                                                                                                               misestimation tradeoff
                                                                                                                                                               source wrappers closed




Figure 1: Full paper statement dependency DAG for [GCG24]. The DAG is auto-generated at the beginning of a paper’s
formalization process, and it is kept up-to-date so that a human can quickly understand formalization status. This DAG
shows that the paper has been completely formalized.




                                                                                                 5
E CON CSL IB


Table 1: Reusable E CON CSL IB library components. The lines of code (LOC) counts are tracked Lean lines in the
listed component files and submodules; the rows partition the public EconCSLib/ Lean files, including folded umbrella
imports and small related layers. Paper users are inferred from direct paper-local imports of the component or one of its
submodules, so the column is a conservative dependency summary rather than a full transitive call graph over public
artifacts.
Library component                  Content details                                                                  Lines of code Paper users
Foundations: finite math and       Core finite mathematics used across the formalizations: finite-choice            15,941        [DSWG25]; [LMMS04]; [GN22];
graph tools                        distances, ranking and order conversions, finite-sum algebra, threshold and                    [LG21]; [GKG+ 19]; [KR21];
                                   interval certificates, asymptotic estimates, and graph-cycle extraction for                    [DGJ24]; [DGD26]; [EOS07];
                                   local-improvement arguments.                                                                   [GHW01]; [GJ19]; [PRP+ 24]
Foundations: probability and       Probability infrastructure for recommendation, ratings, pricing, and ranking     76,470        [DSWG25]; [MBJG25]; [LMMS04];
stochastic processes               papers: finite PMFs and expectations, conditional kernels, Gaussian and                        [GN22]; [LG21]; [LBG24];
                                   random-utility comparisons, large-deviation and method-of-types certificates,                  [GGSG19]; [GJ20]; [GJ19];
                                   stochastic dominance, order statistics, Markov chains, MDPs, CTMCs,                            [GKG+ 19]; [KR21]; [EOS07];
                                   Poisson processes, and renewal-reward models.                                                  [GHW01]; [PRP+ 24]
Foundations: optimization,         Certificate-oriented optimization and complexity for paper-level endpoints:      5,371         [DSWG25]; [MSVV07]; [GN22];
certificates, and complexity       argmax, endpoint, and bisection principles; finite-search and output-check                     [LG21]; [LMMS04]; [GKG+ 19];
                                   certificates; approximation and LP witnesses; binary-policy games;                             [KR21]; [LOS02]; [DGJ24];
                                   move-graph descent; strategic and choice equilibria; NP/ZPP consequence                        [DGJ26]; [GJ19]; [PRP+ 24]
                                   interfaces; and Yao-style lower-bound certificates.
Social choice, rankings, voting,   Executable social-choice infrastructure: ranked ballots, next-active support     23,773        [LMMS04]; [GGSG19];
and fair division                  counts, RCV/STV traces, quotas, coalition-safety lemmas, final-order                           [GKG+ 19]; [KR21]; [DGJ24];
                                   structures, candidate-deletion reductions, Thiele-style proportionality,                       [DGJ26]; [GGRS26]
                                   Mallows/Kendall ranking models, payoff interfaces, envy graphs,
                                   bounded-envy algorithms, and indivisible-goods fairness statements.
Auctions and mechanisms            Mechanism-design infrastructure for digital-goods, combinatorial, and            12,881        [GHW01]; [LOS02]; [EOS07]
                                   position auctions: allocation and payment semantics, utility formulas, DSIC
                                   truthfulness, VCG-style welfare maximization, benchmark-competitive
                                   auctions, single-minded set packing, greedy mechanisms, and critical-value
                                   certificates.
Online algorithms and regret       Online allocation infrastructure centered on AdWords and platform learning:      4,374         [MSVV07]; [MBJG25]
                                   matching/allocation state machines, primal-dual accounting, competitive-ratio
                                   certificates, regret interfaces, and hooks for randomized lower-bound
                                   arguments.
Matching markets and               Stable matching and admissions infrastructure: one-to-one and many-to-one        3,924         [GS62]; [Rot82]; [DGD26]; [LG21]
admissions                         assignments, blocking-pair stability, deferred-acceptance invariants,
                                   applicant/proposer optimality, quota admissions, strategic application cutoffs
                                   and payoffs, and two-group policy objective comparisons.
Ratings and recommender            Ratings and recommendation infrastructure: Bayesian binary and ordinal           3,186         [MBJG25]; [GJ20]; [GJ19];
systems                            signal models, posterior-mean rating formulas, prior-weighted updates,                         [GCG24]; [PRP+ 24]
                                   monotonicity and correction lemmas, Thompson-sampling entrypoints,
                                   exposure/allocation policies, classwise fairness constraints, top-k
                                   recommendation surfaces, policy averaging, and accuracy/diversity trade-off
                                   statements.




statement, and that the Lean statement is a correct translation of the mathematical statement.4 The third component, as a
holistic audit, focuses on the connections between statements as opposed to a statement-by-statement approach—in early
formalization campaigns, a failure mode was that the statement-by-statement approach made errors due to semantic drift
between statements. This workflow can (and does) raise when the judge LLM is “uncertain” about a match, flagging it
for human review.
This pipeline can be run anytime, and is currently designed to run both at the beginning of a paper formalization and at
the end. At the beginning, it can be used to iterate on the intended Lean targets until translation-verified Lean statements
are found. Python tooling, supported by GitHub Continuous Integration (CI) checks, enforces that this pipeline has
been run and is passing before a paper can be declared formalized.
We note that, at the moment, all validations are done by a codex (sub-)agent itself, and so self-preferencing or correlated
errors [KGPG25] concerns exist (that the judge agent makes the same mistakes that the original translation and
Lean-writing agents do).

Human validation dashboard As illustrated in Figure 2, in the dashboard, each Lean statement is presented alongside
the original paper statement (visualized from the original LATEX if available) and the LLM translation and verdict as
described above. The human can then mark whether the Lean statement matches the intended paper statement, which is
stored in the repository. Thus, the human work in formalizing the paper is analogous to a human checking that the

    4
      First, an LLM (without any context on the source paper) is asked to translate from the Lean code back to LATEX. Then, a second
LLM (also without any context) is asked to compare the LATEXtranslation to the source statement in the paper, and judge whether they
are equivalent.


                                                                                   6
E CON CSL IB




Figure 2: Screenshot of the paper-interface review dashboard for [MBJG25]. For each paper mathematical statement,
the dashboard shows the paper’s LATEX statement and Lean statement, so that a human can verify that these match.
The dashboard further shows an AI-generated Lean-to-TeX draft (generated without any context for the original
paper)—ideally, this should match the original paper, and may be helpful for the human to verify translation accuracy.
Finally, there are human review controls for recording whether the formal statement matches the source claim, which
get logged into the repository.


theorem statement is correctly written down, as opposed to checking the proof directly. As we discuss below, this step
is the key bottleneck for autoformalization, and where E CON CSL IB is most lagging.

Outputs from each of the above validations are stored persistently in the repository itself, including the validator identity,
timestamp, and any comments – provenance of all judgements (github username, or LLM model with timestamp) as
well as hashes of the validated Lean statements are included in the documentation. We note that errors and imprecision
in this step are the most common issues found in the formalization process so far: since it is not programmatic but rather
human and using a language model, subtle issues can emerge such as a statement being assumed in a Lean function
statement as opposed to proven in its proof. Over time, we have focused on improving the LLM-as-judge and automated
checks (in Python) for this task; we foresee this audit tooling being improved over time, as failures are detected and
patched.

3.2.2   Other human-facing artifacts and documentation.
Two other human-facing artifacts enable the human-in-the-loop process and steering of the formalization agent.
(1) DAG with concise result formalization status. As illustrated in Figure 1, the LLM agent generates and then
maintains a DAG of the paper’s named mathematical statements (e.g., definitions, lemmas, theorems); while the paper
is not fully formalized, this DAG contains the status of each result. Monitoring this DAG is a key way that the human
can track progress and steer the agent toward certain results; status updates documented in the DAG also give insight on
where the LLM may be stuck, and need guidance.
(2) Final human-facing validation report. The workflow produces a FINAL_VALIDATION_REPORT.md that com-
plements the DAG in describing the formalization process, in a human digestible form. Its components include: the
formalization status of each result, whether the agent was able to follow the paper’s proof approach or needed to deviate
(either due to an error, or a missing library-level result that it did not build), and what if any additional assumptions


                                                              7
E CON CSL IB


were needed to prove the result. See Section C for examples; for example, the validation report for [MBJG25] reports
that a theorem statement’s strict inequality required an extra assumption implicit in the paper (that Bernoulli success
probabilities p were bounded away from 0 and 1). This report also tracks the current status of the LLM-as-judge and
human translation verification.

3.3   Agent “skill” and automation scripts to autoformalize papers

Finally, as we’re formalizing papers, we ask the agent to log lessons for future agents. LLM agents use markdown files
to document such learnings; these markdown files are called Skill files, and are often shared online. The goal here is to
create the self-orchestration scaffolding so that an LLM, with no other context, can receive a paper link and follow a
workflow to formalize it. These learnings are split into two components:
(1) “Workflow” skills and auditing scripts. These skills document and automate workflows for starting and then ending
a paper: for example, they document that to start a paper, the agent should acquire the paper pdf and LATEX source from
arXiv if available; then, it should extract mathematical statements and create a formalization plan and the DAG. After fin-
ishing a paper, the agent should check that the PaperInterface.lean, DAG, and FINAL_VALIDATION_REPORT.md
files follow best practices. Other skill components include advice to: keep the paper interface reviewable; record
proof-route deviations immediately; and upstream reusable lemmas only when a second paper is likely to need them.
Non-markdown scripts, such as those in Python, also check for things like “sorry,” a Lean command that can take the
place of a proof to allow a file to compile without a real proof; templates for each of the human-facing artifact files are
also included.
(2) “Proof” skill files: In addition to the above “Workflow” skills, we are creating “Proof best practices” skills – both
for overall formalization suggestions and guardrails, and for specific types of mathematical claims. Within each library
component, files document component file structure and suggestions on various proof approaches. For example, for
probability-heavy papers, the skill suggests that a default interpretation for many statements should be an "up to measure
0" result, as opposed to statements that are true pointwise everywhere. These skills also document common proof
patterns needed to turn standard statements (such as that a certain type of limit converges) into formal Lean statements.

Developing this skill in the process of formalizing papers – and especially the audit tooling as discussed above – has
been a primary output of the project, and where human feedback has been most encoded. This skill has been developed
through three main avenues. First and foremost, we instruct Codex to encode feedback and lessons from our interactions
into the skill file, especially when it comes to course-corrections in the formalization or documentation process. Second,
this feedback-to-skill process was then itself automated, using the approach of [GQG+ 26] : a Codex agent was
instructed to analyze all its past sessions and then extract durable lessons from its traces and our interactions into the skill
file. Third, an LLM agent extracted workflow lessons from the literature on autoformalization, and hardened skill patterns
where appropriate [WMM+ 26, CDY+ 25, ZMAW26, WXW+ 25, FRRB23, OFY26, RLQ26, MZF26, LWH+ 25].


4     Current Formalization Progress

As of July 2, 2026, the public repository contains 24 paper formalizations: 20 fully formalized papers and 4 partial
formalizations, totaling 986,391 lines of Lean code. Table 3 details these papers and their status. These include 14
formalized papers co-authored by the author of this paper, and 6 other prominent EconCS papers, including those
selected from the test-of-time awardees of the ACM EC conference. This approach – formalizing both the author’s
papers and classic papers – balances (a) developing the formalization workflow using results with which the author is
familiar and (b) building out the shared library with results most likely to be useful in formalizing other EconCS papers.
In addition, 3 non-public paper formalizations are active in our private repository.
I stress that these papers are formalized in the following sense:

       • The Lean code compiles, and so Lean has checked the correctness of the translated statements, given the stated
         assumptions and definitions.
       • Our LLM-as-judge and post-formalization audit workflow concludes that the Lean code fully covers the math-
         ematical statements in the paper, that they have been translated correctly, and that no additional assumptions
         not in the paper (except where documented) are made.
       • While the human verification dashboard exists, it has only been sparsely used to verify the translation fully
         captures the paper statement, and that no extra assumptions have been made.


                                                               8
E CON CSL IB


Table 2: Codex token usage for E CON CSL IB formalization sessions across two measured machines through June 5,
2026, when the public repository contained 13 paper formalizations, with about 5 more in progress. Codex was asked
to go through its own session logs and count tokens, deduplicating counts across resumed sessions and subagents.

 Quantity                                                            Logged tokens                 Credits      Approximate cost†
 Uncached input tokens                                                  665,103,654                83,138                   $3,326
 Cached input tokens                                                 22,054,285,696               275,679                  $11,027
 Output tokens, including reasoning                                      68,771,979                51,579                   $2,063
 Reasoning output tokens                                                 24,456,589                     –        Included in output
 Total                                                               22,788,161,329               410,396                  $16,416
 †
  Cost calculation. Approximate cost uses the OpenAI Codex GPT-5.5 token-based rate card as viewed June 1, 2026: 125 credits
 per million uncached input tokens, 12.5 credits per million cached input tokens, and 750 credits per million output tokens. Fast
 mode would multiply the credit cost by about a factor of 2, and was often used. We note that we did not spend this in raw dollars –
 these tokens were included as part of a GPT Pro subscription, which costs $200/month (and were provided to the author for free).


In other words, for these papers, we have completed the “AI agent” and “Lean compiler” parts of the Human-AI-Lean
process. However, we have not yet completed the expensive “human” cost of this process, where a human with some
knowledge of reading Lean verifies the paper-facing statements have been correctly translated. A big open question
for this project, and similar such projects, is how they will complete this translation validation process with human
checkers. In the meantime, we are relying on an LLM-as-judge approach to aid in this process. We foresee that this will
be the default workflow for most intended users of E CON CSL IB.

5     Discussion
While the project is still in its infancy, there are several lessons that can be drawn and open questions important for its
long-term contributions.

Human monitoring and steering The workflow is not yet fully automated – not quite at the vision in which we can
hand an agent the paper pdf and receive full Lean code verification. However, it is getting closer, and the Codex agent
can now work for many hours (e.g., overnight or all day) on a paper without human intervention or feedback.
While I have not written a single line of Lean code, for the early papers I actively monitored the Codex windows that are
writing the proofs and intervene when it seems to get stuck. For example, it might start generating large proof sections
designed to circumvent needing to use an assumption that is implicit in the paper. (In one case during verification
of [GN22], it constructed large proof sections because it did not realize that the paper’s assumptions imply that the
denominator of a given equation cannot be 0). The agent sometimes also stops at not proving the full paper statements
from raw primitives but instead assumes an intermediate step. Several times, the agent also stalled at trying to prove
pointwise statements where the paper (implicitly or explicitly) proved an “up to measure 0” statement. Section A details
some of this back-and-forth, based on an analysis of session logs.
Over time, as the agent formalization skill has been developed, these common traps have been documented, automated
audit tooling has been built, and autonomy has increased substantially, especially given the audit procedures, the
LLM-as-judge workflow, and in the development of human-facing artifacts.

Human translation verification – is it feasible? The primary open question is how far human verification should go
for a paper. In theory, the goal of a library like E CON CSL IB is that downstream paper consumers can “trust” a library
as having provided correctly translated statements. For example, a Lean paper-facing statement for [MBJG25] is as
follows, referring to EconCSLib.Statistics.JensenConvex, a E CON CSL IB library function defining convexity.
     theorem paper_facing_theorem3_2_squared_bias_convex_in_quality
         {alpha beta eta t : R}
         (hden : eta * alpha + eta * beta + t ̸= 0) :
       EconCSLib.Statistics.JensenConvex
           (fun q => paper_squared_bias alpha beta eta t q)

A human in the dashboard can verify that this statement matches the paper’s statement, but someone needs to verify that
what the paper means by convexity is correctly implemented in EconCSLib.Statistics.JensenConvex. Ideally,
not every human verifier of a paper that uses convexity needs to do this validation.


                                                                 9
E CON CSL IB


More generally, most intended users of E CON CSL IB will not know enough Lean code to be able to verify that it has
correctly translated their paper statements, nor will they wish to invest the effort to verify the translations. For example,
the function that defines Thompson sampling looks as follows.
  def paper_facing_thompson_sampling_mechanism
      {V : Type*} [Fintype V] [DecidableEq V] [Nonempty V]
      (belief : PMF (V → R))
      (policy : PMF V) : Prop :=
    ∃ tie_breaker : (V → R) → V,
      (∀ (profile : V → R) (v : V),
        profile v ≤ profile (tie_breaker profile)) ∧
      policy = belief.bind (fun profile => PMF.pure (tie_breaker profile))

Whether this precisely matches what we mean by Thompson sampling is not apparently obvious to someone who is not
familiar with Lean code (including the author of this paper).
For this reason, we have implemented the LLM-as-judge workflow to validate paper translations. This may be
insufficient for high-stakes validations; whether it is sufficient for an intended use case such as validating proofs of
submitted papers to conferences is an open, sociological question.

Human vs AI verification in Lean more generally [Bes26] discusses early tensions between the M ATHLIB com-
munity – which is pursuing painstaking, clean, human verification of pure mathematics papers – and various math AI
startups, that are leveraging the work of this community without, potentially, giving enough back. There are substantial
questions for how a library like E CON CSL IB can give back to M ATHLIB and other human-curated repositories: ul-
timately, while verified for correctness via the Lean compiler, E CON CSL IB is still a form of “AI Slop” – its code is
bloated and messier than the analogous human project would be.
Besides aesthetics, there are also questions of intermediate translation correctness: while paper-facing statement
translations can be confirmed by a human (though this itself has costs, as discussed above), not every intermediate
library statement can be. Thus, it may not be clear what exactly a library actually contains until it is needed by an agent
to prove a particular statement in another paper (for example, the convexity definition issue discussed above). Such
ambiguity likely prevents any integration of AI-generated libraries with human-curated Lean projects.
As discussed above, human verification of translated statements is the primary contrast with the E CON CSL IB project
of Bei et al. [BMJ+ 26] . Their project only includes statements in the shared library that have been curated and
validated by an expert in Lean (and EconCS as needed). This results in a more trusted shared library (they may not
face this “convexity” issue), but cannot be built in as automated a manner. A “best of both worlds” approach would be
to preferentially use formalized concepts from trusted libraries when available; our E CON CSL IB project agent skill
specifies such preferencing.

Token cost The process is expensive in terms of tokens. This project is only possible on an academic budget because
of the heavy subsidization by OpenAI for tokens within Codex. Formalizing one paper approximately takes a full
week’s quota on an OpenAI Pro subscription on the Max tier, the highest tier available. Table 2 quantifies the overall
approximate token usage on this project so far (calculated by summing the token usage across measured sessions in
the project folders). For the first 13 fully formalized papers (and about 5 in progress), this added up to about $16,000
(or more if fast mode usage is counted) if paid for directly on a per-token API cost basis as opposed to via a Pro
subscription on the Max tier. Reducing this cost, such as through better agent scaffolding, is an important direction for
future work; we also hope that as the shared library is further developed (especially for continuous probability), this
cost will decrease.

Dependence on other libraries and standard results Just like the EconCS community depends on mathematical
advances in other fields, E CON CSL IB depends on mathematical libraries in Lean, notably M ATHLIB; this project would
not be possible without the years of careful human work to develop such libraries. Notably, some required results are
not yet available in standard libraries, and so we are left with the following choices: (1) pause on formalizing a paper
fully until those results are available, such as by the CSL IB library; (2) declare “victory” by assuming those (potentially
standard) results; (3) develop the necessary results ourselves in our Lean library; (4) prove our final desired statement
another way which does not need the result. For example, for [LOS02] and [LMMS04], we have gone with choice (2),
assuming standard computational complexity results. For [GCG24], the agent avoided invoking a result on the number
of basic feasible solutions in a linear program by proving the necessary statements in a more paper-local, ad hoc fashion.
For several other papers, the agent proved (and elevated to our probability library) statements about Gaussian random
variables and Continuous Time Markov Chains that may one day exist in an upstream Lean library.


                                                            10
E CON CSL IB


One notable characteristic is that Lean is better suited for discrete math arguments, as opposed to the continuous,
measure-theoretic probability arguments needed for many EconCS or Operations papers. However, LLM-generated
formalization now makes formalizing papers with substantial probability feasible, if not easy. For example, the
formalizations of [LG21] and [GN22] each took well over 100,000 lines of Lean code, much of it to define and
formalize measure theoretic equilibria equations (for example, that a given strategy was optimal up to measure 0). Our
hope is that the probability and equilibria-related components being developed for E CON CSL IB make formalizing such
papers more efficient in the future.

Errors and hand-waviness in published papers This project raises several “sociological” questions about correctness
in applied modeling EconCS papers. While we have not yet found any “fatal” mistakes in a paper, we have found several
minor “bugs” that can be patched, unspoken assumptions, or true theorem statements whose proofs were nevertheless
incorrect, requiring new proofs (that the LLM agent was able to find). Furthermore, some proof steps, even if correct,
are under-specified to the point that it takes the LLM agent substantial work to try to complete the step. For example,
the agent was able to formalize our paper [DSWG25]; however, a proof step was seemingly underspecified, and the
final validation report documents the following:

         Theorem 1 proof deviation. The paper’s continuous source-transformation proof sketch is underspeci-
         fied at the measurable transformation step and in the multiclass Sb , Sd mass accounting. Lean proves
         the same paper-facing bound directly from calibration, and formalizes the source-transformation
         route using an explicit real-coordinate sweep with coordinate pushforward and pullback. This is a
         proof-strategy deviation, not a theorem-statement change.

In the past, such issues have largely gone under the radar, and the community generally believes that most such errors
if they exist are inconsequential if they can be repaired with minor edits. We are now at a time where such errors
can be found at scale using LLMs, and not all papers will be successfully formalized by Lean, which by definition
does not permit such hand-waving. This raises several questions about process: if I as an author find such substantial
hand-waving (or even an error that can be patched by an additional assumption or clarification), do I submit an erratum
for journal publications? Post a note on arXiv? By some standards, such issues will be found in many papers, and then
the community will be drowning in errata. What if I find such issues in someone else’s paper? Is it reasonable to email
them, or just post a verification report in a repository? While such issues regarding errors have always existed, we are
now at a time that they can no longer slip under the radar.

Long term goals and roadmap This project is in its extremely early days, and it is unclear how it can provide value
to the community. However, it seems to be a project worth doing, both to verify the EconCS canon and published
research papers. One can imagine a world, perhaps in the very near future (STOC‘27 or EC‘27 perhaps), in which
every submitted paper comes with an AI-generated Lean verification of its statements. Libraries such as CSL IB and
E CON CSL IB aim to make such verification more efficient and in reach for every author. Similarly, many researchers
may seek to verify all their own published papers, a process that I have begun for myself.
Of course, AI generation of novel proofs is also a rapidly advancing area; it may be the case that Lean libraries help in
this process for EconCS papers. [Kor26] is building a toolkit for LLMs to help in the development and validation of
applied models in economics. As more papers are verified, it may be that the library’s progress makes this process
easier, for both verification of human-written and AI-generated proofs.
One vision, that hopefully will come about, is that people can focus on the creativity, conceptual insights, and real-world
usefulness components of applied modeling – while AI helps most with ensuring correctness and helping prove
generality.
I welcome contributions by others for the library and to aid in this effort.

Acknowledgments
I thank Guanting Chen, Jiajun Ma, Xiaohui Bei, and members of the Garg lab for helpful discussions. The full
formalization work so far was completed through a single OpenAI Codex Pro subscription on the Max tier, provided for
free by Arjun Seshadri at OpenAI. I am supported by NSF CAREER IIS-2339427, the William T Grant Foundation
Scholars Award, NASA, and Google, Mastercard, and Amazon research awards.




                                                            11
E CON CSL IB


                                                  Table 3: Current formalization status of papers in E CON CSL IB.

Paper info                                             Lean proof       Human translation      Lines of     Note
                                                                                               Code
College Admissions and the Stability of Marriage. D. Formalized         0/7 reviewed           388          This only uses a few lines of code as its infrastructure has
Gale and L. S. Shapley; American Mathematical                                                               largely been elevated to the shared matching library.
Monthly, 1962 [GS62].
The Economics of Matching: Stability and Incentives. Formalized         0/29 reviewed          8,931
Alvin E. Roth; Mathematics of Operations Research,
1982 [Rot82].
Competitive Auctions and Digital Goods. Andrew V.        Formalized     0/30 reviewed          14,624      Formalizes the SODA paper; Theorem 8.2 uses the
Goldberg, Jason D. Hartline, and Andrew Wright;                                                            refined monotone-auction wording from the journal
SODA, 2001 [GHW01].                                                                                        version [GHK+ 06].
AdWords and Generalized Online Matching. Aranyak Formalized             0/43 reviewed          13,711
Mehta, Amin Saberi, Umesh Vazirani, and Vijay V.
Vazirani; Journal of the ACM, 2007 [MSVV07].
Internet Advertising and the Generalized Second-Price Formalized        0/26 reviewed          133,338
Auction. Benjamin Edelman, Michael Ostrovsky, and
Michael Schwarz; American Economic Review,
2007 [EOS07].
Designing Optimal Binary Rating Systems. Nikhil Garg, Formalized        0/56 reviewed          85,780
Ramesh Johari; AISTATS / PMLR 89, 2019 [GJ19].
Who is in Your Top Three? Optimizing Learning in         Formalized     0/17 reviewed          35,055
Elections with Many Candidates. Nikhil Garg,
Lodewijk Gelauff, Sukolsak Sakshuwong, Ashish Goel;
HCOMP, 2019 [GGSG19].
Designing Informative Rating Systems: Evidence from Formalized          0/15 reviewed          7,027
an Online Labor Market. Nikhil Garg, Ramesh Johari;
Manufacturing & Service Operations Management
23(3), 2020 [GJ20].
Algorithmic Monoculture and Social Welfare. Jon          Formalized     0/49 reviewed          65,646
Kleinberg and Manish Raghavan; PNAS, 2021 [KR21].
Test-optional Policies: Overcoming Strategic Behavior Formalized        0/23 reviewed          125,744
and Informational Gaps. Zhi Liu and Nikhil Garg;
EAAMO, 2021 [LG21].
Driver Surge Pricing. Nikhil Garg and Hamid              Formalized     0/36 reviewed          142,948
Nazerzadeh; Management Science, 2022 [GN22].
Optimal Strategies in Ranked-Choice Voting. Sanyukta Formalized         0/65 reviewed          54,410
Deshpande, Nikhil Garg, Sheldon H. Jacobson;
arXiv:2407.13661, 2024; working paper [DGJ24].
Reconciling the Accuracy-Diversity Trade-off in          Formalized     0/42 reviewed          52,018       Proposition 2’s printed finite bound appears to miss a
Recommendations. Kenny Peng, Manish Raghavan,                                                               factor of 2; Lean proves the corrected finite bound, which
Emma Pierson, Jon Kleinberg, and Nikhil Garg; The                                                           is sufficient for the asymptotic 1/2-homogeneity result.
ACM Web Conference, 2024 [PRP+ 24].
User-item fairness tradeoffs in recommendations.         Formalized     0/48 reviewed          46,174
Sophie Greenwood, Sudalakshmee Chiniah, and Nikhil
Garg; NeurIPS, 2024 [GCG24].
A No Free Lunch Theorem for Human-AI Collaboration. Formalized          0/15 reviewed          2,030
Kenny Peng, Nikhil Garg, Jon Kleinberg; AAAI,
2025 [PGK25].
Addressing Discretization-Induced Bias in                Formalized     0/41 reviewed          26,133
Demographic Prediction. Evan Dong, Aaron Schein,
Yixin Wang, and Nikhil Garg; PNAS Nexus,
2025 [DSWG25].
Balancing Producer Fairness and Efficiency via           Formalized     10/27 reviewed; 2      680          Strict variance decrease is formalized with the explicit
Prior-Weighted Rating System Design. Thomas Ma,                         uncertain                           interior-quality assumption 0 < q_v < 1.
Michael S. Bernstein, Ramesh Johari, and Nikhil Garg;
ICWSM, 2025 [MBJG25].
Capacity Constraints Make Admissions Processes Less Formalized          0/66 reviewed          11,536
Predictable. Evan Dong, Nikhil Garg, Sarah Dean;
AAAI-26 published version, DOI
10.1609/aaai.v40i45.41179 [DGD26].
Combatting Gerrymandering with Ranked Choice             Formalized     0/19 reviewed          9,398
Voting: an Experimental Analysis of Multi-member
Districts in the United States. Nikhil Garg, Wes Gurnee,
David Rothschild, David Shmoys; Operations Research,
2026, DOI 10.1287/opre.2024.1167 [GGRS26].
Simpler Than You Think: The Practical Dynamics of        Formalized     0/50 reviewed          20,736
Ranked Choice Voting. Sanyukta Deshpande, Nikhil
Garg, Sheldon H. Jacobson; Journal of Computational
Social Science, 2026 [DGJ26].
Truth Revelation in Approximately Efficient              Partially      0/39 reviewed          7,582        Greedy approximation, truthfulness, and Theorem 6.1
Combinatorial Auctions. Daniel Lehmann, Liadan Ita formalized                                               reductions are formalized. Full formalization requires
O’Callaghan, and Yoav Shoham; Journal of the ACM,                                                           computational complexity results that are out of scope.
2002 [LOS02].
                                                                                                                                              Continued on next page




                                                                                12
E CON CSL IB


                                            Table 3: Current formalization status of papers in E CON CSL IB (continued).

Paper info                                              Lean proof      Human translation      Lines of     Note
                                                                                               Code
On Approximately Fair Allocations of Indivisible Goods. Partially       0/48 reviewed          80,496       Sections 2 and 4 are fully formalized. Section 3 has
Richard J. Lipton, Evangelos Markakis, Elchanan         formalized                                          query/descent/rounded-search support. The PTAS/FPTAS
Mossel, and Amin Saberi; ACM EC, 2004 [LMMS04].                                                             runtime layer needs reusable fixed-dimension IP
                                                                                                            complexity infrastructure.
Iterative Local Voting for Collective Decision-making in Partially      0/47 reviewed          23,466       Partial formalization: the remaining intentional boundary
Continuous Spaces. Nikhil Garg, Vijay Kamble, Ashish formalized                                             isolated to the SSGM convergence theorem. Theorem 3 is
Goel, David Marn, Kamesh Munagala; JAIR 64,                                                                 proved as a constrained alternative in general and as the
2019 [GKG+ 19].                                                                                             original statement under the explicit full-space condition.
Quantifying Spatial Under-reporting Disparities in       Partially      0/27 reviewed          18,540       Full formalization requires a homogeneous Poisson
Resident Crowdsourcing. Zhi Liu, Uma Bhandaram,          formalized                                         process and stopping-time derivation.
Nikhil Garg; Nature Computational Science,
2024 [LBG24].




References
   [ABH+ 26] Mohammed Abouzaid, Andrew J Blumberg, Martin Hairer, Joe Kileel, Tamara G Kolda, Paul D Nelson,
             Daniel Spielman, Nikhil Srivastava, Rachel Ward, Shmuel Weinberger, et al. First proof. arXiv preprint
             arXiv:2602.05192, 2026.
    [APS+ 23] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W Ayers, Dragomir Radev, and
              Jeremy Avigad. Proofnet: Autoformalizing and formally proving undergraduate-level mathematics.
              arXiv preprint arXiv:2302.12433, 2023.
   [ASM+ 25] Leni Aniva, Chuyue Sun, Brando Miranda, Clark Barrett, and Sanmi Koyejo. Pantograph: A machine-
             to-machine interaction interface for advanced theorem proving, high level reasoning, and data extraction
             in lean 4. In International Conference on Tools and Algorithms for the Construction and Analysis of
             Systems, pages 104–123. Springer, 2025.
   [BBB+ 25] Matthew Bolan, Joachim Breitner, Jose Brox, Nicholas Carlini, Mario Carneiro, Floris van Doorn, Martin
             Dvorak, Andrés Goens, Aaron Hill, Harald Husum, et al. The equational theories project: Advancing
             collaborative mathematical research at scale. arXiv preprint arXiv:2512.07087, 2025.
   [BBC+ 25] Anne Baanen, Matthew Robert Ballard, Johan Commelin, Bryan Gin-ge Chen, Michael Rothgang, and
             Damiano Testa. Growing mathlib: maintenance of a large scale mathematical library. In International
             Conference on Intelligent Computer Mathematics, pages 51–70. Springer, 2025.
   [BCM+ 26] Clark Barrett, Swarat Chaudhuri, Fabrizio Montesi, Jim Grundy, Pushmeet Kohli, Leonardo de Moura,
             Alexandre Rademaker, and Sorrachai Yingchareonthawornchai. Cslib: The lean computer science library.
             arXiv preprint arXiv:2602.04846, 2026.
       [Bes26] David Bessis. The fall of the theorem economy.                                        https://davidbessis.substack.com/p/
               the-fall-of-the-theorem-economy, 2026.
    [BMJ+ 26] Xiaohui Bei, Jiajun Ma, Zhan Jing, Hongfei Fu, and Zhihao Gavin Tang. EconCSLib: A Lean library
              for computational economics and AI-assisted research, June 2026. Accepted to EC’26 Workshop on
              AI-Driven Research in EconCS (AI-EconCS ’26).
     [BMS17] Alexander Bagnall, Samuel Merten, and Gordon Stewart. A library for algorithmic game theory in
             ssreflect/coq. Journal of Formalized Reasoning, 10(1):67–95, 2017.
    [BSF+ 24] Maxwell P Bobbin, Samiha Sharlin, Parivash Feyzishendi, An Hong Dang, Catherine M Wraback, and
              Tyler R Josephson. Formalizing chemical physics using the lean theorem prover. Digital Discovery,
              3(2):264–280, 2024.
        [Car24] Mario Carneiro. Lean4Lean: Verifying a typechecker for lean, in lean. arXiv preprint arXiv:2403.14064,
                2024.
   [CDY+ 25] Rafael Cabral, Tuan Manh Do, Xuejun Yu, Wai Ming Tai, Zijin Feng, and Xin Shen. Proofflow: A
             dependency graph approach to faithful proof autoformalization. arXiv preprint arXiv:2510.15981, 2025.
   [CGH+ 25] Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing
             Jin, Chenggang Li, Kaijing Ma, et al. Seed-prover: Deep and broad reasoning for automated theorem
             proving. arXiv preprint arXiv:2507.23726, 2025.
     [DGD26] Evan Dong, Nikhil Garg, and Sarah Dean. Capacity constraints make admissions processes less
             predictable. Proceedings of the AAAI Conference on Artificial Intelligence, 40(45):38385–38394, 2026.


                                                                                13
E CON CSL IB


    [DGJ24] Sanyukta Deshpande, Nikhil Garg, and Sheldon Jacobson. Optimal strategies in ranked choice voting,
            2024.
    [DGJ26] Sanyukta Deshpande, Nikhil Garg, and Sheldon H. Jacobson. Simpler than you think: The practical
            dynamics of ranked choice voting, 2026. Journal of Computational Social Science, 2026.
 [DHMN26] Michael R Douglas, Sarah Hoback, Anna Mei, and Ron Nissim. Formalization of QFT. arXiv preprint
          arXiv:2603.15770, 2026.
[DMKA+ 15] Leonardo De Moura, Soonho Kong, Jeremy Avigad, Floris Van Doorn, and Jakob von Raumer. The
           lean theorem prover (system description). In International Conference on Automated Deduction, pages
           378–388. Springer, 2015.
 [DSWG25] Evan Dong, Aaron Schein, Yixin Wang, and Nikhil Garg. Addressing discretization-induced bias in
          demographic prediction. PNAS Nexus, 4(2), January 2025.
    [EOS07] Benjamin Edelman, Michael Ostrovsky, and Michael Schwarz. Internet advertising and the generalized
            second-price auction: Selling billions of dollars worth of keywords. American Economic Review,
            97(1):242–259, 2007.
  [FRRB23] Emily First, Markus N Rabe, Talia Ringer, and Yuriy Brun. Baldur: Whole-proof generation and repair
           with large language models. In Proceedings of the 31st ACM Joint European Software Engineering
           Conference and Symposium on the Foundations of Software Engineering, pages 1229–1241, 2023.
  [GCA+ 26] Robert Joseph George, Jennifer Cruden, Will Adkisson, Xiangru Zhong, Huan Zhang, and Anima
            Anandkumar. Torchlean: Formalizing neural networks in lean. arXiv preprint arXiv:2602.22631, 2026.
   [GCG24] Sophie Greenwood, Sudalakshmee Chiniah, and Nikhil Garg. User-item fairness tradeoffs in rec-
           ommendations. In The Thirty-eighth Annual Conference on Neural Information Processing Systems,
           2024.
  [GGRS26] Nikhil Garg, Wes Gurnee, David Rothschild, and David B. Shmoys. Combating gerrymandering with
           ranked choice voting: An experimental analysis of multimember districts in the united states. Operations
           Research, 0(0), 2026.
  [GGSG19] Nikhil Garg, Lodewijk L Gelauff, Sukolsak Sakshuwong, and Ashish Goel. Who is in your top three?
           optimizing learning in elections with many candidates. In Proceedings of the AAAI Conference on
           Human Computation and Crowdsourcing, volume 7, pages 22–31, 2019.
  [GHK+ 06] Andrew V. Goldberg, Jason D. Hartline, Anna R. Karlin, Michael Saks, and Andrew Wright. Competitive
            auctions. Games and Economic Behavior, 55(2):242–269, 2006. Mini Special Issue: Electronic Market
            Design.
   [GHW01] Andrew V. Goldberg, Jason D. Hartline, and Andrew Wright. Competitive auctions and digital goods.
           In Proceedings of the Twelfth Annual ACM-SIAM Symposium on Discrete Algorithms, pages 735–744.
           ACM/SIAM, 2001.
      [GJ19] Nikhil Garg and Ramesh Johari. Designing optimal binary rating systems. In The 22nd International
             Conference on Artificial Intelligence and Statistics, pages 1930–1939. PMLR, 2019.
      [GJ20] Nikhil Garg and Ramesh Johari. Designing informative rating systems: Evidence from an online labor
             market. Manufacturing & Service Operations Management, 23(3):589–605, 2020.
  [GKG+ 19] Nikhil Garg, Vijay Kamble, Ashish Goel, David Marn, and Kamesh Munagala. Iterative local voting for
            collective decision-making in continuous spaces. Journal of Artificial Intelligence Research, 64:315–355,
            2019.
     [GN22] Nikhil Garg and Hamid Nazerzadeh. Driver surge pricing. Management Science, 68(5):3219–3235, May
            2022.
  [GQG+ 26] Zhongxin Guo, Danrui Qi, Hanwen Gu, Peng Cheng, and Yongqiang Xiong. SKILL-DISCO: Distilling
            and compiling agent traces into reusable procedural skills, June 2026.
  [GRA+ 26] Fabian Gloeckle, Ahmad Rammal, Charles Arnal, Remi Munos, Vivien Cabannes, Gabriel Synnaeve,
            and Amaury Hayat. Automatic textbook formalization. arXiv preprint arXiv:2604.03071, 2026.
     [GS62] D. Gale and L. S. Shapley. College admissions and the stability of marriage. The American Mathematical
            Monthly, 69(1):9–15, January 1962.
  [GWJ+ 25] Guoxiong Gao, Yutong Wang, Jiedong Jiang, Qi Gao, Zihan Qin, Tianyi Xu, and Bin Dong. Herald: A
            natural language annotated lean 4 dataset. In International Conference on Learning Representations,
            2025.


                                                        14
E CON CSL IB


    [HJL+ 25] Yanxing Huang, Xinling Jin, Sijie Liang, Peng Li, and Yang Liu. Formarl: Enhancing autoformalization
                 with no labeled data. arXiv preprint arXiv:2508.18914, 2025.
 [HRW+ 21] Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W Ayers, and Stanislas Polu. Proof artifact
                 co-training for theorem proving with language models. arXiv preprint arXiv:2102.06203, 2021.
         [Ili26] Vasily Ilin. Semi-autonomous formalization of the vlasov-maxwell-landau equilibrium. arXiv preprint
                 arXiv:2603.15929, 2026.
           +
     [JGJ 26] Haocheng Ju, Guoxiong Gao, Jiedong Jiang, Bin Wu, Zeming Sun, Leheng Chen, Yutong Wang, Yuefeng
                 Wang, Zichen Wang, Wanyi He, et al. Automated conjecture resolution with formal verification. arXiv
                 preprint arXiv:2604.03789, 2026.
           +
    [JKT 26] Prithwish Jana, Kaan Kale, Ahmet Ege Tanriverdi, Cruise Song, Sriram Vishwanath, and Vijay Ganesh.
                 Proofbridge: Auto-formalization of natural language proofs in lean via joint embeddings. In The
                 Fourteenth International Conference on Learning Representations, 2026.
  [JWZ+ 22] Albert Q Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik, Timothée Lacroix,
                 Yuhuai Wu, and Guillaume Lample. Draft, sketch, and prove: Guiding formal theorem provers with
                 informal proofs. arXiv preprint arXiv:2210.12283, 2022.
  [KGPG25] Elliot Myunghoon Kim, Avi Garg, Kenny Peng, and Nikhil Garg. Correlated errors in large language
                 models. In Forty-second International Conference on Machine Learning, 2025.
       [Kor26] Moran Koren. Theorist toolbox: Tools for agent based llm-assisted economic theory research. arXiv
                 preprint arXiv:2606.22337, 2026.
       [KR21] Jon Kleinberg and Manish Raghavan. Algorithmic monoculture and social welfare. Proceedings of the
                 National Academy of Sciences, 118(22):e2018340118, 2021.
     [KTC26] Natalia Klaus, Palina Tolmach, and Juan Conejero. A rust-to-lean verification pipeline with ai provers:
                 An experience report. arXiv preprint arXiv:2605.30106, 2026.
     [LBG24] Zhi Liu, Uma Bhandaram, and Nikhil Garg. Quantifying spatial under-reporting disparities in resident
                 crowdsourcing. Nature Computational Science, 4(1):57–65, 2024.
           +
  [LDL 25] Wangyue Lu, Lun Du, Sirui Li, Ke Weng, Haozhe Sun, Hengyu Liu, Minghe Yu, Tiancheng Zhang,
                 and Ge Yu. Automated formalization via conceptual retrieval-augmented llms. arXiv preprint
                 arXiv:2508.06931, 2025.
           +
   [LDS 24] Yang Li, Dong Du, Linfeng Song, Chen Li, Weikang Wang, Tao Yang, and Haitao Mi. Hunyuanprover:
                 A scalable data synthesis framework and guided tree search for automated theorem proving. arXiv
                 preprint arXiv:2412.20735, 2024.
        [LG21] Zhi Liu and Nikhil Garg. Test-optional policies: Overcoming strategic behavior and informational
                 gaps. In Proceedings of the 1st ACM Conference on Equity and Access in Algorithms, Mechanisms, and
                 Optimization, EAAMO ’21, page 1–13. ACM, October 2021.
   [LLL+ 22] Guillaume Lample, Timothee Lacroix, Marie-Anne Lachaux, Aurelien Rodriguez, Amaury Hayat,
                 Thibaut Lavril, Gabriel Ebner, and Xavier Martinet. Hypertree proof search for neural theorem proving.
                 Advances in neural information processing systems, 35:26337–26349, 2022.
 [LMMS04] R. J. Lipton, E. Markakis, E. Mossel, and A. Saberi. On approximately fair allocations of indivisible
                 goods. In Proceedings of the 5th ACM Conference on Electronic Commerce, EC04, page 125–131. ACM,
                 May 2004.
      [LOS02] Daniel Lehmann, Liadan Ita O’Callaghan, and Yoav Shoham. Truth revelation in approximately efficient
                 combinatorial auctions. Journal of the ACM, 49(5):577–602, September 2002.
 [LSWY25] Haohan Lin, Zhiqing Sun, Sean Welleck, and Yiming Yang. Lean-STaR: Learning to interleave thinking
                 and proving. In International Conference on Learning Representations, pages 66041–66062, 2025.
         +
 [LTL 25a] Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu, Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou Xia,
                 Danqi Chen, Sanjeev Arora, et al. Goedel-prover: A frontier model for open-source automated theorem
                 proving. arXiv preprint arXiv:2502.07640, 2025.
         +
 [LTL 25b] Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng,
                 Jiawei Ge, Jingruo Sun, et al. Goedel-prover-v2: Scaling formal theorem proving with scaffolded data
                 synthesis and self-correction. arXiv preprint arXiv:2508.03613, 2025.
           +
 [LWH 25] Jianqiao Lu, Yingjia Wan, Yinya Huang, Jing Xiong, Zhengying Liu, and Zhijiang Guo. Formalalign:
                 Automated alignment evaluation for autoformalization. In International Conference on Learning
                 Representations, 2025.


                                                         15
E CON CSL IB


    [Mat20] Mathlib Community. The Lean Mathematical Library. In Proceedings of the 9th ACM SIGPLAN
            International Conference on Certified Programs and Proofs, CPP ’20. ACM, January 2020.
    [Mat26] Mathlib Initiative. Formal frontier. https://mathlib-initiative.org/formal-frontier/, 2026.
  [MBJG25] Thomas Ma, Michael S. Bernstein, Ramesh Johari, and Nikhil Garg. Balancing producer fairness and
           efficiency via prior-weighted rating system design. Proceedings of the International AAAI Conference
           on Web and Social Media, 19(1):1139–1157, Jun. 2025.
  [MCF+ 26] Agnieszka Mensfelt, David Tena Cucala, Santiago Franco, Angeliki Koutsoukou-Argyraki, Vince
            Trencsenyi, and Kostas Stathis. Towards a common framework for autoformalization. In Proceedings of
            the AAAI Conference on Artificial Intelligence, volume 40, pages 40971–40980, 2026.
 [MMG+ 26] David Ma, Kaijing Ma, Shawn Guo, Yunfeng Shi, Enduo Zhao, Jiajun Shi, Zhaoxiang Zhang, Gavin
           Cheung, Jiaheng Liu, and Zili Wang. Oprover: A unified framework for agentic formal theorem proving.
           arXiv preprint arXiv:2605.17283, 2026.
 [MSVV07] Aranyak Mehta, Amin Saberi, Umesh Vazirani, and Vijay Vazirani. AdWords and generalized online
          matching. Journal of the ACM, 54(5):22, October 2007.
    [MU21] Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language. In
           International Conference on Automated Deduction, pages 625–635. Springer, 2021.
 [MYS+ 24] Logan Murphy, Kaiyu Yang, Jialiang Sun, Zhaoyu Li, Anima Anandkumar, and Xujie Si. Autoformaliz-
           ing euclidean geometry. arXiv preprint arXiv:2405.17216, 2024.
   [MZF26] Jordan Meadows, Lan Zhang, and Andre Freitas. Formalscience: Scalable human-in-the-loop aut-
           oformalisation of science with agentic code generation in lean. arXiv preprint arXiv:2604.23002,
           2026.
   [OFY26] Azim Ospanov, Farzan Farnia, and Roozbeh Yousefzadeh. APOLLO: Automated LLM and lean collabo-
           ration for advanced formal reasoning. In The Thirty-ninth Annual Conference on Neural Information
           Processing Systems, 2026.
  [PAB+ 26] Nilay Patel, Noah Arias, Davit Babayan, Victoria Cochran, Timothy Libman, Hafsah Mahmood, Liam
            McCarty, Soli Munoz, Laurel Willey, and Jeffrey Flanigan. Mathatlas: A benchmark for autoformaliza-
            tion in the wild. arXiv preprint arXiv:2605.14061, 2026.
   [PGK25] Kenny Peng, Nikhil Garg, and Jon Kleinberg. A no free lunch theorem for human-ai collaboration. In
           Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, pages 14369–14376, 2025.
  [PHZ+ 22] Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor Babuschkin, and Ilya Sutskever.
            Formal mathematics statement curriculum learning. arXiv preprint arXiv:2202.01344, 2022.
  [PRP+ 24] Kenny Peng, Manish Raghavan, Emma Pierson, Jon Kleinberg, and Nikhil Garg. Reconciling the
            accuracy-diversity trade-off in recommendations. In Proceedings of the ACM Web Conference 2024,
            pages 1318–1329, 2024.
     [PS20] Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving. arXiv
            preprint arXiv:2009.03393, 2020.
   [RLQ26] Yuanjie Ren, Jinzheng Li, and Yidi Qi. Merlean: An agentic framework for autoformalization in quantum
           computation. arXiv preprint arXiv:2602.16554, 2026.
     [Rot82] Alvin E. Roth. The economics of matching: Stability and incentives. Mathematics of Operations
             Research, 7(4):617–628, November 1982.
  [RPG+ 26] Ahmad Rammal, Niket Patel, Fabian Gloeckle, Amaury Hayat, Julia Kempe, Remi Munos, Charles
            Arnal, and Vivien Cabannes. Formalizing mathematics at scale. arXiv preprint arXiv:2605.29955, 2026.
  [RSS+ 25] ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe
            Fu, Qihao Zhu, Dejian Yang, et al. Deepseek-prover-v2: Advancing formal mathematical reasoning via
            reinforcement learning for subgoal decomposition. arXiv preprint arXiv:2504.21801, 2025.
     [She26] Arsen Shebzukhov. Improving lean4 autoformalization via cycle consistency fine-tuning. arXiv preprint
             arXiv:2603.24372, 2026.
     [Skr26] Tomas Skrivan.     Scientific computing           in   lean.      https://lecopivo.github.io/
             scientific-computing-lean/, 2026.
    [SYA24] Peiyang Song, Kaiyu Yang, and Anima Anandkumar. Towards large language models as copilots for
            theorem proving in lean. arXiv preprint arXiv:2404.12534, 2024.


                                                       16
E CON CSL IB


       [TS25] Joseph Tooby-Smith. HepLean: Digitalising high energy physics. Comput. Phys. Commun., 308:109457,
              2025.
      [Urb26] Josef Urban. 130k lines of formal topology in two weeks: Simple and cheap autoformalization for
              everyone? arXiv preprint arXiv:2601.03298, 2026.
   [vDEL20] Floris van Doorn, Gabriel Ebner, and Robert Y Lewis. Maintaining a library of formal mathematics. In
              International Conference on Intelligent Computer Mathematics, pages 251–267. Springer, 2020.
 [WDL+ 25] Ke Weng, Lun Du, Sirui Li, Wangyue Lu, Haozhe Sun, Hengyu Liu, and Tiancheng Zhang. Autoformal-
              ization in the era of large language models: A survey. arXiv preprint arXiv:2505.23486, 2025.
         +
[WHW 26] Yutong Wu, Di Huang, Ruosi Wan, Yue Peng, Shijie Shang, Chenrui Cao, Lei Qi, Rui Zhang, Xishan
              Zhang, Zidong Du, et al. Stepfun-formalizer: Unlocking the autoformalization potential of llms through
              knowledge-reasoning fusion. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 40,
              pages 33980–33988, 2026.
         +
  [WJL 22] Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus Rabe, Charles Staats, Mateja Jamnik, and Christian
              Szegedy. Autoformalization with large language models. Advances in neural information processing
              systems, 35:32353–32368, 2022.
         +
[WMM 26] Zichen Wang, Wanli Ma, Zhenyu Ming, Gong Zhang, Kun Yuan, and Zaiwen Wen. M2f: Automated
              formalization of mathematical literature at scale. arXiv preprint arXiv:2602.17016, 2026.
 [WUL+ 25] Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,
              Marina Vinyes, Zhenzhe Ying, Zekai Zhu, et al. Kimina-prover preview: Towards large formal reasoning
              models with reinforcement learning. arXiv preprint arXiv:2504.11354, 2025.
         +
[WXW 25] Hanyu Wang, Ruohan Xie, Yutong Wang, Guoxiong Gao, Xintao Yu, and Bin Dong. Aria: An agent for
              retrieval and iterative auto-formalization via dependency graph. arXiv preprint arXiv:2510.04520, 2025.
         +
  [XGS 24] Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and
              Xiaodan Liang. Deepseek-prover: Advancing theorem proving in llms through large-scale synthetic data.
              arXiv preprint arXiv:2405.14333, 2024.
         +
  [XLY 25] Jiaxuan Xie, Chengwu Liu, Ye Yuan, Siqi Li, Zhiping Xiao, and Ming Zhang. Fmc: Formalization of
              natural language mathematical competition problems. arXiv preprint arXiv:2507.11275, 2025.
       [YS26] Banri Yanahama and Akiyoshi Sannai. Lean atlas: An integrated proof environment for scalable
              human-ai collaborative formalization. arXiv preprint arXiv:2604.16347, 2026.
         +
  [YSG 23] Kaiyu Yang, Aidan M Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan
              Prenger, and Anima Anandkumar. Leandojo: Theorem proving with retrieval-augmented language mod-
              els. In Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks
              Track, 2023.
 [YWG+ 24] Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang, Dahua Lin, and Kai Chen. Lean workbook: A
              large-scale lean problem set formalized from natural language math problems. Advances in Neural
              Information Processing Systems, 37:105848–105863, 2024.
    [ZHP21] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: a cross-system benchmark for formal
              olympiad-level mathematics. arXiv preprint arXiv:2109.00110, 2021.
     [ZLL26] Yuanhe Zhang, Jason D Lee, and Fanghui Liu. Ai4slt: Empirical processes in lean 4 for formal statistical
              learning theory. arXiv preprint arXiv:2602.02285, 2026.
 [ZMAW26] Thomas Zhu, Pietro Monticone, Jeremy Avigad, and Sean Welleck. Leanarchitect: Automating blueprint
              generation for humans and ai. arXiv preprint arXiv:2601.22554, 2026.




                                                         17
E CON CSL IB


A    Human Feedback Workflows

Note: The initial text for this appendix section was written by Codex, based on its session logs: about 30 distinct
sessions from April 23 through June 6, 2026, with over 2,000 user prompts. The author performed an editing pass on
the appendix, for substance, style, and concision, but much of the raw text originally generated by Codex remains. The
main text was written by the author, with some supporting information provided by Codex.
This appendix summarizes the human steering workflow used to formalize individual papers and to develop the library
itself.

Summary: Lessons for Human-AI Formalization

The most productive feedback was both operational and mathematical. The user did not only say whether a the-
orem was right; the user repeatedly specified what artifact would make the claim reviewable. Examples include:
PaperInterface.lean as the statement checkpoint, the DAG as the source-dependency checkpoint, status.json
as the status source of truth, and the final validation report as a one-page human audit rather than an agent progress log.
The second lesson is that expert feedback should be compiled into the workflow. Several recurring corrections became
durable instructions: download and cache the source PDF once; avoid broad documentation churn during proof loops;
commit at named theorem or stopping boundaries; keep generated tables tied to status metadata; use official publication
metadata; distinguish formalized, partial, conditional, and caveated results; preserve human-written summaries; and
keep the main formalization skill mostly paper-agnostic, with paper-specific proof recipes living in library notes or
paper-local plans. This reduced repeated mistakes across later papers.
The third lesson is that the human’s role is especially important at the translation boundary from informal paper
mathematics to formal statements. The agent can write and repair Lean proofs, but the user often supplied the decisive
question: does this theorem state the paper’s claim, are the certificates internally discharged, does a green DAG node
depend on an unproved assumption, and is the remaining boundary a missing proof or a missing reusable library? Those
questions are the main reason the project can expose partial formalizations honestly while still making completed paper
claims useful for human readers.

A Feedback Loop for Paper Formalization

The basic workflow was not a one-shot “paper link to proof” process. It was a loop in which Codex proposed or
implemented a formalization step, Lean checked the proof objects, and the user corrected the translation boundary,
review surface, or repository process. Over time, those corrections were written into the repository skill file, status
scripts, validation reports, and contribution workflow. In this sense, the user feedback did two jobs: it improved
individual paper formalization, and it converted mistakes into durable instructions for future agents.
The loop stabilized around several stages alongside the Lean work. First, the agent was told to get context from
the repository and the formalization skill, then inventory the paper’s definitions, lemmas, propositions, theorems,
and displayed theorem-like claims. Second, the agent built a source dependency DAG and a proof plan before or
alongside Lean work. Third, the agent formalized the reusable mathematics and paper-facing wrappers, prioritizing
theorem seams over a line-by-line encoding of the PDF. Fourth, the agent exposed a small human-review surface:
PaperInterface.lean, a dependency DAG, a paper README, and a final validation report. Fifth, the user audited
whether those surfaces faithfully matched the paper and whether any assumptions or certificates remained. Sixth, the
resulting status metadata regenerated the README, website, paper tables, and public/private release artifacts.

How the Interaction Pattern Changed Over Time

The earliest sessions were mostly persistence-oriented proof sessions. The user gave broad goals such as fully
formalizing a family of papers and repeatedly pushed the agent to continue rather than stop at a local obstruction. This
often appeared as a queue of short steering commands: “keep going,” “continue,” “you do not have a time limit,” “just
keep going until the paper is formalized,” and “create sub-agents as needed.” Over time this moved the interaction
from short supervised edits to longer autonomous loops, where the agent could spend several hours on a proof seam,
run targeted builds, repair the mathematical route, and continue after resumptions without asking for each next step.
The main feedback at this stage was about effort allocation: commit less often, avoid updating broad reports during
every proof loop, cache source PDFs instead of re-searching, and spend more time repairing imprecise informal proofs
outside Lean before returning to code; this feedback is now integrated into the skill.


                                                           18
E CON CSL IB


A second phase shifted from proof production to reviewability. After the agent claimed progress on paper theorems,
the user asked what a human should inspect to know that the paper was actually formalized. That changed the
workflow from “many compiling declarations” to a smaller review contract: PaperInterface.lean in source order, a
dependency DAG containing the paper’s named results, and a final validation report written for a human rather than
for the next agent. Next, we focused on semantics of status and assumptions. The user pressed on whether results
were actually proven according to the source paper, or whether green DAG nodes depended on unproved inputs. This
produced stricter status language: completed paper-facing claims are formalized; results that are not fully deduced
from the basic Lean axioms are partially formalized; and caveats are reserved for source-version corrections or
extra assumptions that remain in the final theorem.
The next phase was artifact and publication governance. Once the repository was moving toward a public release and this
paper, the feedback became more about source-of-truth discipline: generated tables should come from status.json,
public pages should mirror the same metadata, unfinished papers should stay private by default, bibliography entries
should come from official sources, and human-authored status summaries should not be overwritten once marked
as human-written or human-approved. A later consolidation phase sharpened the workflow. For example, post-
formalization review became a stricter workflow: DAGs should contain the paper’s numbered results, final reports
should be human-facing; further, the dashboard and LLM-as-judge translation verification approach was developed.
Reproducibility and measurement became explicit requirements: source PDFs and TEX should be cached locally,
generated status files should be updated only at meaningful boundaries, and token/cost accounting should deduplicate
resumed sessions and subagent rollout logs.




                                                         19
E CON CSL IB


Examples of User Feedback and Resulting Workflow Rules




  Feedback type                 Example user feedback                              Resulting workflow rule or artifact
  Autonomy and persistence      Queued commands such as “keep going,”              Agents now work toward clean theorem or
                                “continue,” and “you do not have a time            compile boundaries, use targeted builds,
                                limit,” with permission to think outside Lean      and write handoff notes only at real
                                and patch imprecise informal proofs.               stopping points. The skill explicitly says
                                                                                   not to stop at identifying a gap if the proof
                                                                                   can be repaired.
  Proof-loop pacing             Feedback such as “focus on proving things,”        During active proof work, agents should
                                “do not keep updating status.json,”                prefer theorem progress, local builds, and
                                “commit less,” and “update documentation           proof-plan repair. Status JSON, DAG PDFs,
                                only at major milestones.”                         skill notes, and commits are batched at
                                                                                   named proof or audit boundaries rather than
                                                                                   every proof loop.
  Source inventory and DAG      Create a DAG for every named definition,           Each paper folder maintains a dependency
  discipline                    lemma, theorem, proposition, and corollary;        DAG. The DAG is treated as a source map,
                                each numbered result should be one node;           not a changelog of helper lemmas, and
                                green nodes must state the actual result and       status colors must agree with the
                                mean that the paper-facing theorem is fully        paper-local status.json.
                                formalized.
  Human-facing Lean interface   The decisive review object should be a Lean        PaperInterface.lean became the
                                file whose definitions and theorems appear in      canonical statement surface.
                                paper order; if Lean checks it and a human         Implementation endpoints move to
                                confirms it matches the paper, the paper is        ProofInterface.lean or
                                done.                                              PostPaperAudit.lean when they would
                                                                                   make the review file too large.
  Validation report scope       The final validation report is not a handoff       Completed papers get concise
                                log; it should be a short human report: what       FINAL_VALIDATION_REPORT.md files.
                                was proved, what assumptions were added,           Long theorem ledgers and status chatter are
                                what mistakes were found, and whether the          kept out of the human report.
                                proof follows the paper.
  Status vocabulary and         “Formalized” and “verified in Lean” should         The status vocabulary was standardized.
  assumption boundaries         not be separate statuses. If a paper-facing        Fully closed papers have status
                                theorem still requires an external certificate,    formalized; papers such as
                                mark the paper partial.                            [LOS02, LMMS04] remain partial because
                                                                                   the remaining complexity/runtime
                                                                                   infrastructure is outside the current library.
  Library extraction            When proof infrastructure is reusable,             Reusable probability, optimization,
                                elevate it to the shared library; e.g., matching   matching, auction, online-algorithm, and
                                and auction code should explain why some           fair-division components were separated
                                papers have few paper-local lines.                 from paper folders. Paper-local code is kept
                                                                                   as source-shaped wrappers over shared
                                                                                   infrastructure.
  Publication and provenance    Public/private repositories should protect         The project now has private-workflow
  hygiene                       unfinished papers; public tables should be         contribution docs, generated
                                generated from status JSON; BibTeX should          human_status.json tables, GitHub
                                come from official sources; human-written          Pages scaffolding, bibliography hygiene
                                summaries should not be overwritten.               rules, and review-status metadata for
                                                                                   human-authored summaries.
  Token and cost accounting     The user challenged naive counts that              The workflow now treats root-session
                                double-counted resumed sessions and                history as the human-feedback record and
                                embedded parent transcripts inside subagent        counts usage from each rollout’s own turn
                                rollouts.                                          boundary. Guardian/auto-review logs are
                                                                                   separated from billed interactive work
                                                                                   unless explicitly being audited.


                                                             20
E CON CSL IB


Feedback on DAGs and Human-Facing Audits

A recurring theme was that proof artifacts needed to be legible to a human reviewer, not merely useful to the agent.
For dependency DAGs, the user pushed for source completeness and semantic accuracy: every named result should
appear; node labels should describe the paper claim rather than the implementation helper family; green should mean
the paper-facing theorem is fully formalized; and a theorem should not be marked green if its visible inputs are still
open. The user also gave presentation-level feedback: avoid overlapping nodes and arrows, do not duplicate a numbered
proposition across several boxes, do not use internal labels such as lem:... as the visible node name, and state
the mathematical content of a green theorem rather than merely saying that it is closed. Empirical sections can be
acknowledged in reports, but they do not belong in proof DAGs unless the paper states a theorem-like empirical claim
that is being formalized. Venue metadata also belongs on the DAG: the formalized PDF may be an arXiv version, but
the public node header should still say, for example, HCOMP 2019, AISTATS, or MSOM when that is the official
publication venue. This turned the DAG from a progress sketch into a human-auditable dependency map whose status
colors had to agree with the validation report and status.json.
The same pattern applied to final audits. The user repeatedly separated three documents that the agent had initially
blurred: README/handoff notes for future work, PaperInterface.lean for statement-level human review, and
FINAL_VALIDATION_REPORT.md for a short final audit. The report was not supposed to be a theorem ledger, dashboard
dump, or agent status transcript; it should answer whether the paper is formalized, what assumptions or certificates
remain, whether the proof follows the paper strategy or uses a cleaner route, and whether any source mistakes were
found. This also led to filtering large dashboard surfaces—for example, hundreds of rows in one paper were too many
for a human report—and to treating human summaries in generated tables as review prose that should be preserved
once marked human-written or human-approved.
This feedback also affected dashboards. Human-review row counts should track paper-facing definitions and named
results, not every helper theorem produced during implementation. A paper with dozens of rows may be correct if
the source has many named statements, but high row counts require an audit pass: shrink PaperInterface.lean
to source-facing statements, move proof endpoints to ProofInterface.lean, and keep generated dashboards from
creating an inflated impression of the human audit burden.

Feedback on Assumptions and Status Language

Several sessions were devoted to the difference between a caveat, a partial formalization, and a source-theorem
assumption. The user repeatedly asked whether an apparently extra hypothesis was actually stated in the paper, whether
it could be derived from the paper’s model, and whether the final theorem should expose it. In one paper, this changed
descriptions of several lemmas: the issue was not that the result was conditional on an external certificate, but whether
the formal statement reflected a meaningful difference from the source paper. In the ranking/rating papers, the same
question arose for strict rankings, finite support, threshold behavior, and Laplace-style limits. The resulting workflow
rule is to search the source first, and derive assumptions that the source structure already implies.

Representative Case Studies

Ranking and rating papers. The ranking and rating papers [GGSG19, GJ20, GJ19] show the interaction between
source reading, large-deviation boundaries, and library extraction. The user first asked for three large-deviation papers
to be formalized in a sequence, starting with the multi-candidate election paper [GGSG19] but instructing the agent to
produce library-level large deviations tooling useful for all three papers. For the two rating-system papers [GJ20, GJ19],
the user pushed on whether a generic Laplace principle was truly required or whether the paper’s finite-support and
strict-ranking hypotheses already removed the apparent threshold obstruction. That changed the plan from “stop at a
broad LDP boundary” to “derive the finite-support convention used by the paper, close what can be closed, and extract
any genuinely reusable rating-model or finite-sum optimization lemmas to the shared library.”

Auctions and digital goods. The auction formalization [GHW01, GHK+ 06] illustrates how statements might be
refined or clarified in published papers. E CON CSL IB formalizes the SODA version [GHW01] of the paper. However,
the journal version [GHK+ 06] is referenced to interpret the statement for Theorem 8.2 – the journal paper refines this
part of the preliminary presentation by introducing monotone auctions and proving the upper bound for monotone
truthful randomized auctions.

Complexity boundaries. The combinatorial-auction and fair-division papers [LOS02, LMMS04] show how the user
can decide on the boundary between what should be proved versus assumed.


                                                           21
E CON CSL IB


For the combinatorial-auction paper [LOS02], the decision was: greedy approximation, truthfulness, and Theorem 6.1
reductions are formalized, while full formalization required computational complexity results that are out of scope.
For the fair-division paper [LMMS04], the proof boundary similarly stops at fixed-dimension integer-program runtime
infrastructure.

Producer fairness. The producer-fairness paper [MBJG25] demonstrates a different kind of expert feedback: the
user asked whether a caveat was really a paper assumption, a derived fact, or an extra condition introduced by the
formalization. Ultimately formalizing the paper required a trivial assumption (that Bernoulli success probabilities were
not exactly 0 or 1) for the strict endpoint; this was documented as an additional assumption, not as a result caveat or
incorrect statement.




                                                          22
E CON CSL IB


B        Supplemental Information

Label                                                Meaning
formalized                                           The paper-facing claim is represented by a Lean statement and closed by a Lean proof from the
                                                     paper’s source-shaped assumptions.
formalized with caveat                               The Lean proof closes, but a reader should account for a material qualification, such as an added
                                                     non-paper assumption, a corrected or clarified source statement, or a documented paper issue.
partially formalized                                 The paper has a declared formalized subset, but at least one paper-facing result or required source
                                                     layer remains outside the current Lean proof.
                   Table 4: Formalization status labels used in paper summaries, validation reports, and status tables.



Label                       Meaning
match                       Lean statement faithfully captures the paper-facing claim.
uncertain                   Reviewer cannot decide without auditing a shared predicate, hidden convention, or source ambiguity.
mismatch                    Lean statement differs materially from the paper claim.
stale                       Review was made against an older statement hash.
missing                     Source statement lacks a corresponding Lean statement.
                     Table 5: Statement-translation audit labels used in the dashboard and LLM-as-judge summaries.



    Paper: Competitive Auctions and Digital Goods
    Authors: Andrew V. Goldberg, Jason D. Hartline, and Andrew Wright
    Publication venue: SODA paper; journal refinement for Section 8.2                           Legend
    Year: SODA 2001; 2006 Section 8.2 refinement
    Formalized PDF: https://www.cs.miami.edu/home/burt/learning/Csc597.052/docs/goldberg.pdf
                                                                                                        Theorem             Lemma           Definition
                                                                                                        corollary           support         model layer




                                                     Benchmarks (Section 4)                          Random Sam-                           Weighted Pair-
        Definitions (Sections 2–3)                                                                                                                                    pi , ci , gi (Section 8)
                                                        optimal fixed-price                       pling (Section 5.2)                      ing (Section 7)
        digital-goods auctions, rev-                                                                                                                               win probabilities, expected
                                                        benchmark F and                           sample-independent                  bid-independent random-
         enue, DSIC, IR, and NPT                                                                                                                                     costs, expected gains
                                                         total bid value T                         threshold auction                   ized multi-price auction




            Threshold Mecha-                                                                                                                                        Lemma 8.1 (Section 8)
            nisms (Section 5)                        Theorem 4.1 (Section 4)                    Lemma 6.1 (Section 6)                 Theorem 7.1 (Section 7)
                                                                                                    independent fair-                                                 truthfulness implies
             posted prices and                        normalized [1, h] model                                                         paper 4h ≤ T model gives
                                                                                                 coin lower-tail model                                             monotone win probabilities
           own-bid-independent                       gives T ≤ 2(log2 h + 2)F                                                          T ≤ 192(log2 h + 2)W
          thresholds are truthful                                                                 gives e−|S|/36 bound



                                                                                                                                                                   Theorem 8.2 (Section 8)
                                                     Corollary 4.2 (Section 4)                                                        Theorem 7.2 (Section 7)         journal Section 8.2
                                                                                               Theorem 6.2 (Section 6)
        F (2) Benchmark Support                         h/n cutoff trunca-
                                                                                                 ranked finite-candidate               paper F (2) ≥ 2h model         monotone truthful
          finite bidder-value can-                      tion and Theorem
                                                                                               wrapper gives 1 − e−α/36 −             gives F (2) ≤ 576sW and        randomized auctions
             didate benchmark                          4.1 give T ≤ 4mF                                                               tightness family is closed
                                                                                                   40e−α/72 guarantee                                                satisfy E[R] ≤ F (b)




          Deterministic Mod-
             els (Section 9)
          optimal threshold and
            deterministic bid-
          independent auctions




                Theorem 9.1
                (Section 9.2)
        anonymous bid-independent
            list bridge, actual F
            benchmark witness,
           and ratio form closed



                                                      Theorem 9.3
        Lemma 9.2 (Section 9.3)
                                                      (Section 9.3)
           truthful determinis-
                                                 anonymous set-of-bids
            tic IR/NPT binary
                                                   deterministic truth-
         auctions admit critical-
                                                  ful auctions have an
              price offer slices
                                                  R/F ≤ 1/h witness




Figure 3: Full dependency DAG for [GHW01], Competitive Auctions and Digital Goods. The DAG shows the SODA
paper. Section 8.2 is checked against the later journal version’s monotone-auction formulation of the revenue upper
bound; the preliminary unrestricted wording is tracked only as source-version provenance.




                                                                                                         23
    E CON CSL IB


    C   Sample Validation Reports auto-generated by LLM workflow
                      MBJG25 Producer Fairness Validation Report



Final Validation Report: MBJG25 Producer Fairness
Updated: 2026-07-02
Paper appendix note: this manuscript copy omits the detailed evidence, provenance, DAG-audit, validation-check,
and statement-ledger sections that begin at Section 11 in the full validation report. See the repository copy at
papers/MBJG25ProducerFairness/docs/FINAL_VALIDATION_REPORT.md for the complete machine-readable and review-
ledger version.

1. Human Verdict
Formalized. The paper-facing producer-fairness model, Theorems 3.1 and 3.2, Section 4 responsive-market definitions,
and Appendix C responsive MSE decomposition are checked. The strict variance-decrease endpoint is checked with
the explicit interior-quality assumption 0 < q_v < 1; boundary audit rows at q_v = 0 and q_v = 1 record why the
unconditional strict statement is not claimed. Human dashboard review has saved entries for 10 of 27 rows, with 0
stale rows, 0 human mismatches, and 2 human-uncertain shared-predicate rows.

2. Closeout Status
  • Completion status: formalized.
  • One-sentence recap: Theorems 3.1 and 3.2 are checked, with the strict variance-decrease endpoint carrying the
    explicit interior-quality additional assumption.
  • Lean footprint: 680 paper-local Lean LOC; PaperInterface.lean is 332 lines; 27 human-review declarations are
    exposed.
  • Audit summary: paper coverage has 24 covered, 3 conditional_boundary; statement LLM-as-judge has 24
    matches, 3 mismatch; resolutions: 3 conditional_boundary; assumption provenance has 4 paper_condition,
    4 paper_assumption, 2 additional-assumption rows; source-record audit reports 24 boundary inputs and 0
    recursion failures; review-surface audit passes; holistic source-first audit PASS; DAG/source-json audit PASS
    in docs/PUBLIC_DAG_HOLISTIC_AUDIT_2026-07-02.md.

3. Source and Scope
  • Paper: Balancing Producer Fairness and Eﬀiciency via Prior-Weighted Rating System Design
  • Authors: Thomas Ma, Michael S. Bernstein, Ramesh Johari, and Nikhil Garg
  • Source version: ICWSM 2025 / arXiv:2207.04369
  • Lean folder: MBJG25ProducerFairness/
  • Human-facing theorem file: MBJG25ProducerFairness/PaperInterface.lean
  • Paper assumption file: MBJG25ProducerFairness/Assumptions.lean
  • DAG artifacts: MBJG25ProducerFairness/docs/DependencyDAG.tex, MBJG25ProducerFairness/docs/DependencyDAG.
     pdf
  • Supporting audit ledgers: MBJG25ProducerFairness/AGENT_SOURCE_AUDIT.md and MBJG25ProducerFairness/audit/
     *.json

Scope: this audit covers the paper’s fixed binary-rating formulas, Theorems 3.1 and 3.2, Section 4 responsive-market
definitions, and Appendix C responsive MSE decomposition.




                                                        24
    E CON CSL IB

4. Researcher Summary of Checked Results
  • The posterior mean, bias, variance, squared-bias, individual-unfairness, Thompson-sampling, expected-regret,
    and responsive-MSE definitions are exposed as paper-facing formula rows.
  • Theorem 3.1’s weak variance decrease, squared-bias nondecrease, and strict interior variance decrease are
    checked.
  • Theorem 3.2’s squared-bias convexity, squared-bias minimizer, variance concavity, and variance maximizer are
    checked.
  • Section 4’s individual producer unfairness, Thompson-sampling mechanism, and expected regret definitions are
    checked.
  • Appendix C’s responsive MSE decomposition is checked with the random review count made explicit.
  • The only theorem-statement qualification is the explicit interior-quality assumption for the strict variance-
    decrease endpoint.

5. Remaining Boundaries and Gaps
None for the declared formalized paper surface. Human review remains partial as a review-process item: 10 of 27
rows have saved human entries, and two saved human entries are intentionally uncertain because they ask how to
audit or trust shared-library predicates such as JensenConvex and GlobalMinAt.

6. Additional Assumptions Beyond Paper
  • Theorem 3.1 strict variance decrease: the formal statement assumes 0 < q_v < 1. Boundary rows at q_v = 0
    and q_v = 1 record why the unconditional strict statement is false at the endpoints.
All other named assumptions are paper/model assumptions or paper theorem conditions: positive prior-shape mass,
positive/nonnegative time, closed quality interval bounds, nonnegative prior strength, and weak/strict prior strength
order.

7. Proof-Strategy Deviations
None. The proof follows the algebraic structure of the paper’s fixed-model definitions. The strict-variance endpoint
is a statement qualification, not a different proof strategy.

8. Proof Tricks Worth Reusing
  • Add explicit boundary audit rows when a source strict inequality is only true on an interior domain.
  • Keep formula rows for definitions such as posterior mean, variance, and squared bias in PaperInterface.lean,
    so statement translation review is over paper formulas rather than opaque Lean helpers.

9. Mathematical Typos or Other Fixes Suggested in the Source Paper
  • Theorem 3.1 strict variance decrease: the unconditional strict wording should be read with the interior-quality
    condition 0 < q_v < 1. At boundary qualities q_v = 0 and q_v = 1, the variance term is identically zero, so
    strict decrease cannot hold unconditionally.

10. Paper Issues or Caveats
None. The interior-quality condition for strict variance decrease is recorded above as an additional assumption, and
the boundary behavior is exposed by separate audit rows.




                                                         25
    E CON CSL IB




                        LMMS04 Fair Division Validation Report



Final Validation Report: LMMS04 Fair Division
Updated: 2026-07-02
Paper appendix note: this manuscript copy omits the detailed evidence, provenance, DAG-audit, validation-check,
and statement-ledger sections that begin at Section 11 in the full validation report. See the repository copy at
papers/LMMS04FairDivision/docs/FINAL_VALIDATION_REPORT.md for the complete machine-readable and review-ledger
version.

1. Human Verdict
Partially formalized. Sections 2 and 4 are checked, and Section 3 has the query, descent, Graham-consequence,
rounded-search, and ratio-transfer support needed for the approximation route. Full formalization still requires
reusable fixed-dimension integer-programming runtime infrastructure for the PTAS/FPTAS layer. No fatal paper
error is reported. The Lemma 2.4 proof prose appears to say to choose a minimum endpoint where the finite-partition
construction needs a maximal or supremal endpoint; this is recorded as a typo, not a caveat. No human dashboard
sign-off has been recorded.

2. Closeout Status
  • Completion status: partially formalized.
  • One-sentence recap: Sections 2 and 4 are fully formalized. Section 3 has query/descent/rounded-search support.
    The PTAS/FPTAS runtime layer needs reusable fixed-dimension IP complexity infrastructure.
  • Lean footprint: 80,496 paper-local Lean LOC; PaperInterface.lean is 303 lines; 48 human-review declarations
    are exposed.
  • Audit summary: paper coverage has 37 covered, 12 conditional_boundary; statement LLM-as-judge has 36
    matches, 12 mismatch; resolutions: 12 conditional_boundary; assumption provenance has 11 paper_condition,
    2 partial_boundary; source-record audit reports 0 boundary inputs and 0 recursion failures; review-surface
    audit passes; holistic source-first audit PASS; DAG/source-json audit PASS in docs/PUBLIC_DAG_HOLISTIC_
    AUDIT_2026-07-02.md.


3. Source and Scope
  • Paper: On Approximately Fair Allocations of Indivisible Goods
  • Authors: Richard J. Lipton, Evangelos Markakis, Elchanan Mossel, and Amin Saberi
  • Source version: ACM EC 2004, DOI 10.1145/988772.988792
  • Lean folder: LMMS04FairDivision/
  • Human-facing theorem file: LMMS04FairDivision/PaperInterface.lean
  • Paper assumption file: LMMS04FairDivision/Assumptions.lean
  • DAG artifacts: LMMS04FairDivision/docs/DependencyDAG.tex, LMMS04FairDivision/docs/DependencyDAG.pdf
  • Supporting audit ledgers: LMMS04FairDivision/docs/POST_FORMALIZATION_AUDIT.md, LMMS04FairDivision/AGENT_
    SOURCE_AUDIT.md, and LMMS04FairDivision/audit/*.json

Scope: this audit covers the declared partial public surface: Section 2 envy and allocation results, Section 3
query/descent/rounded-search support, and Section 4 truthfulness results. The final PTAS/FPTAS runtime layer
for Theorem 3.3 remains outside the current reusable library because fixed-dimension integer-programming runtime
infrastructure is not yet available.

                                                        26
    E CON CSL IB

4. Researcher Summary of Checked Results
  • Section 2 finite-allocation envy definitions, envy-cycle reduction, bounded-envy allocation, and the real-interval
    atom-bound route are checked.
  • Section 3 has checked adaptive-query lower-bound wrappers, Graham-scheduling consequence rows, rounded
    type/value-pair search infrastructure, bounded-optimal allocation support, and additive/ratio transfer lemmas.
  • Section 4 finite truthfulness results are checked: the no-truthful-envy-free/minimum-envy counterexample route
    and the uniform randomized mechanism with its explicit probability bound.
  • The final PTAS/FPTAS runtime conclusion remains a visible reusable-library boundary, not a completed paper
    theorem.

5. Remaining Boundaries and Gaps
Full formalization requires reusable fixed-dimension integer-programming runtime infrastructure for the
PTAS/FPTAS layer in Theorem 3.3. The current Lean code records that layer through explicit partial-boundary
rows and proves the supporting finite algebraic, rounded-search, and transfer statements around it.

6. Additional Assumptions Beyond Paper
None. Positive error parameters, finite duplicate-free goods enumerations, positive atom bounds, normalized random-
allocation weights, and Section 3 load and rounding conditions are source theorem/model conditions. Graham schedul-
ing and fixed-dimension IP runtime are partial or external theorem/library boundaries, not additional assumptions
accepted as completed theorem hypotheses.

7. Proof-Strategy Deviations
  • Theorem 4.1 is proved with a smaller finite counterexample than the source exposition; this is suﬀicient for the
    impossibility theorem.
  • Claim 3.4 required a more explicit finite-descent proof than the prose presentation. The formal proof separates
    high-source moves from low-only tie-breaking moves.
  • Theorem 4.2 is recorded as the finite inequality used by the proof rather than a separate asymptotic Big-O
    wrapper.

8. Proof Tricks Worth Reusing
  • For algorithmic PTAS/FPTAS claims, isolate the finite algebraic/search support from the machine-level runtime
    theorem so the partial boundary is precise.
  • For prose partition arguments over intervals, formalize the constructive endpoint choice explicitly; this exposes
    min/max or supremum direction errors cleanly.

9. Mathematical Typos or Other Fixes Suggested in the Source Paper
  • Lemma 2.4 proof typo: the prose appears to say to choose the minimum endpoint whose prefix interval has
    value at most alpha for every player. To obtain progress and the stated finite partition, this should be read as
    a maximal/supremal endpoint choice.

10. Paper Issues or Caveats
No fatal paper error is reported. The Lemma 2.4 endpoint issue is recorded as a typo, not a caveat. Several implicit
real-support and atom-bound modeling choices are documented in the evidence below. The paper status is partial
only because the reusable fixed-dimension IP runtime infrastructure for the final PTAS/FPTAS layer is not yet
present in the library.




                                                         27
    E CON CSL IB




                   LOS02 Combinatorial Auctions Validation Report



Final Validation Report: LOS02 Combinatorial Auctions
Updated: 2026-07-02
Paper appendix note: this manuscript copy omits the detailed evidence, provenance, DAG-audit, validation-check,
and statement-ledger sections that begin at Section 11 in the full validation report. See the repository copy at papers/
LOS02CombinatorialAuctions/docs/FINAL_VALIDATION_REPORT.md for the complete machine-readable and review-ledger
version.

1. Human Verdict
Partially formalized. The finite auction model, generalized Vickrey auction, single-minded welfare/set-packing re-
ductions, greedy approximation, critical-value lemmas, and average-greedy truthfulness theorem are checked. Full
formalization still requires reusable computational-complexity infrastructure for the native Theorem 6.1 hardness
and NP = ZPP consequences. No auction-theoretic paper error is reported, and no human dashboard sign-off has been
recorded.

2. Closeout Status
  • Completion status: partially formalized.
  • One-sentence recap: Greedy approximation, truthfulness, and Theorem 6.1 reductions are formalized. Full
    formalization requires computational complexity results that are out of scope.
  • Lean footprint: 7,582 paper-local Lean LOC; PaperInterface.lean is 371 lines; 39 human-review declarations
    are exposed.
  • Audit summary: paper coverage has 31 covered, 8 conditional_boundary; statement LLM-as-judge has 31
    matches, 8 mismatch; resolutions: 8 conditional_boundary; assumption provenance has 7 paper_condition, 2
    partial_boundary; source-record audit reports 1 boundary inputs and 0 recursion failures; review-surface audit
    passes; holistic source-first audit PASS; DAG/source-json audit PASS in docs/PUBLIC_DAG_HOLISTIC_AUDIT_
    2026-07-02.md.


3. Source and Scope
  • Paper: Truth Revelation in Approximately Eﬀicient Combinatorial Auctions
  • Authors: Daniel Lehmann, Liadan Ita O’Callaghan, and Yoav Shoham
  • Source version: Journal of the ACM 49(5), 2002
  • Lean folder: LOS02CombinatorialAuctions/
  • Human-facing theorem file: LOS02CombinatorialAuctions/PaperInterface.lean
  • Paper assumption file: LOS02CombinatorialAuctions/Assumptions.lean
  • DAG artifacts: LOS02CombinatorialAuctions/DependencyDAG.tex, LOS02CombinatorialAuctions/DependencyDAG.
     pdf
  • Supporting audit ledgers: LOS02CombinatorialAuctions/POST_FORMALIZATION_AUDIT.md, LOS02CombinatorialAuctions/
    AGENT_SOURCE_AUDIT.md, and LOS02CombinatorialAuctions/audit/*.json

Scope: this audit covers the paper’s mathematical definitions and theorem-level auction results. The paper’s na-
tive computational-complexity consequences are represented only as partial external-boundary interfaces until the
shared library has a machine-level theory of polynomial-time reductions, hardness, inapproximability, randomized
complexity, and the cited set-packing/clique facts.

                                                          28
    E CON CSL IB

4. Researcher Summary of Checked Results
  • The finite combinatorial-auction definitions are checked with source-facing formula rows for utility, truthful-
    ness, generalized Vickrey payments, single-minded profiles, set-packing value, greedy order, accepted set, and
    payments.
  • The generalized Vickrey auction truthfulness theorem and nonnegative truthful-utility proposition are checked
    for the finite combinatorial-auction model.
  • The Theorem 6.1 finite reduction layer is checked: set-packing feasibility and value encodings, weighted set-
    packing reduction, and the clique-to-single-minded-welfare route.
  • The Theorem 7.2 greedy sqrt(m) approximation proof is checked for the explicit average-descending order and
    optimal-allocation comparison conditions.
  • Lemmas 9.1--9.5, Theorem 9.6, Definition 10.1, and Theorem 10.2 are checked for the documented single-minded
    domain and critical-value conditions.
  • The remaining theorem-level boundary is the native complexity layer for Theorem 6.1 and the related NP = ZPP
    complexity-class note.

5. Remaining Boundaries and Gaps
Full formalization requires reusable computational-complexity infrastructure for the final native Theorem 6.1 hardness
and NP = ZPP consequences. The current Lean code proves the finite auction/reduction statements and records the
complexity consequences as conditional external-boundary interfaces.

6. Additional Assumptions Beyond Paper
None. The nonnegative/nonempty single-minded domain, optimal-allocation comparison conditions, denied-bidder
case, nonnegative-value deviation domain, critical-value conditions, and finite-threshold condition are source theorem
conditions. The two complexity rows are partial boundaries, not additional assumptions accepted as completed
theorem hypotheses.

7. Proof-Strategy Deviations
None beyond the formalization boundaries already recorded above. The finite auction, greedy, and critical-value
arguments follow the paper’s proof routes; the native complexity consequences are not claimed as fully formalized.

8. Proof Tricks Worth Reusing
  • For source definitions that otherwise appear as opaque function abbreviations, expose exact formula or iff rows
    in PaperInterface.lean before running LLM-as-judge translation. This keeps the judged review surface at the
    paper-formula level rather than at opaque Lean function signatures.
  • For partial complexity results, separate the finite reduction theorem from the native machine-level complexity
    consequence. The finite theorem can be checked while the external complexity infrastructure remains a visible
    partial boundary.

9. Mathematical Typos or Other Fixes Suggested in the Source Paper
None found.

10. Paper Issues or Caveats
No auction-theoretic paper error is reported. The paper status is partial only because the reusable computational-
complexity infrastructure for the final native complexity claims is not yet present in the library.




                                                         29
