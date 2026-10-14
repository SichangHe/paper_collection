                                                        Autonomous Mathematical Discovery in an
                                                          Open-World Multi-Agent Environment
                                                                 Stephen Chung1,2           Wenyu Du1,3         William J. Wesley4
                                                                                            1
                                                                                              DualverseAI
                                                                                      2
                                                                                       University of Cambridge
                                                                                     3
                                                                                       University of Hong Kong
                                                                                 4
                                                                                   University of California San Diego

                                             We study autonomous mathematical discovery in the Station, an open-world multi-agent environ-
arXiv:2608.23691v2 [cs.AI] 14 Sep 2026




                                             ment in which AI agents from different model families pursue a shared research goal without a central
                                             coordinator or scripted pipeline. Agents choose their own research directions, conduct experiments,
                                             collaborate and publish papers. These papers accumulate into a shared body of knowledge that
                                             later agents can read, cite and extend. We evaluated the Station on 12 mathematical construction
                                             problems from the AlphaEvolve study and two additional case studies. Five of the 12 problems
                                             yielded results novel relative to the prior literature: a new infinite family of finite field Kakeya sets,
                                             new exact 604-point kissing configurations in eleven dimensions, improved bounds for the discretized
                                             Kakeya needle and sign uncertainty problems, and a substantially improved lower bound for Erdős’s
                                             minimum overlap problem. Agents also discovered novel infinite families for Book Ramsey numbers.
                                             Their research extended beyond searching for high-scoring constructions: agents developed explana-
                                             tions of their findings and proved theorems outside the assigned tasks. These explanations guided
                                             further discoveries and were preserved in the agents’ papers, making the underlying insights easier for
                                             external researchers to understand and build upon. All presented discoveries are supported by exact
                                             constructions or proofs formally verified in Lean. We release the source code, full agent dialogues,
                                             papers and verification code, providing a transparent record of how these discoveries emerged.

                                             Date: 24-Aug-2026
                                             Correspondence: info@dualverse.ai



                                         1    Introduction

                                         Artificial intelligence is beginning to contribute directly to the frontier of mathematical research. Recent work
                                         ranges from large-scale mathematical exploration by AlphaEvolve to AI-assisted advances on long-standing
                                         open problems, including the counterexample to the Jacobian Conjecture, proofs of Crouzeix’s and Sendov’s
                                         conjectures, and a collection of ten mathematical results recently reported by OpenAI [1–5]. These advances
                                         raise the question of whether agents, given greater freedom in an environment, can autonomously form a
                                         research community that builds on its own accumulated knowledge to make new discoveries.
                                         To study this question, we use the Station, an open-source, open-world multi-agent environment for au-
                                         tonomous scientific discovery [6].1 The Station simulates a scientific ecosystem in which agents from different
                                         model families choose their own research directions, conduct experiments, communicate with peers, and read
                                         and publish papers. These papers accumulate into a shared body of knowledge that later agents can read,
                                         cite and extend. Agents act as independent researchers without a central coordinator assigning their research
                                         directions or a scripted pipeline determining their next activity.
                                         We apply the Station to 12 mathematical construction problems from the AlphaEvolve study and two
                                         additional mathematical case studies. Five of the 12 AlphaEvolve problems produce results novel relative to
                                         the prior literature. The Station discovers a new infinite family of finite field Kakeya sets, constructs three

                                             1 Source code: https://github.com/dualverse-ai/station

                                              Agent dialogues and proofs: https://dualverse-ai.github.io/station_data_v2/
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




exact 604-point kissing configurations in dimension 11, and establishes new bounds for the discretized Kakeya
needle, sign uncertainty and Erdős’s minimum overlap problems. In a separate case study on Book Ramsey
numbers, the agents discover and prove novel infinite families. The Station also independently reconstructs
a counterexample to the Jacobian Conjecture within one day and without web access, using an evaluator
that provides only a binary success criterion.
This high degree of freedom allows agents to pursue broad mathematical contributions rather than only
optimize a fixed metric. In the finite field Kakeya problem, agents first found promising finite constructions
and then generalised them to an infinite family, proving its validity and exact size. This progression from
computational examples to a general theorem took place autonomously within the Station, revealing the
mathematical structure underlying the finite examples. The same freedom also allowed agents to explore
beyond the stated objective. For example, agents discovered and proved a novel infinite Book Ramsey family
even though the task asked only for finite constructions.
The agents also sought to explain their findings, making their mathematical structure easier to understand.
For one 604-point kissing configuration, they derived an explicit algebraic construction that generates all its
points without computer search. In the sign uncertainty problem, they proved a limitation of the evaluator’s
restricted family of functions, then used this insight to search outside that family and develop a better
construction. These explanations were preserved in the agents’ papers, allowing later agents to build on
them and external researchers to trace how the discoveries developed. As AI-generated constructions and
proofs become more abundant, understanding their underlying ideas and incorporating them into our shared
mathematical knowledge may become increasingly important [7, 8].
We also analyze the AI discovery processes underlying these findings. Our analysis shows that more than half
of the findings involved collaboration among agents. Agents from different model families often contributed
complementary ideas, while papers written by earlier agents became foundations for discoveries made much
later. Many important results were enabled by the extensive internal literature accumulated within each
Station. We release all raw agent dialogues, agents’ papers and externally verified proofs, allowing the
community to study these discovery processes transparently.


2   Method

A standard Station begins with six agents: two each powered by GPT 5.5, Claude Opus 4.8 and Gemini 3.1
Pro [9–11]. Each agent acts as a complete researcher, handling the entire research process from choosing a
direction through experimentation to publication. At every tick, agents receive observations of the environ-
ment in parallel and respond with their chosen actions. Each agent has a limited lifetime; when an agent
departs, the Station spawns a replacement powered by the same model, maintaining a fixed population.
The environment is partitioned into rooms, each serving a particular function and providing its own set of
actions [6]. Figure 1(a) summarizes the rooms and their functions. Agents are free to navigate between rooms
and choose their own actions in each room. One major room is the Research Center, where agents read the
main research task, submit code for evaluation, and review results. Agents can also access a general-purpose
sandbox environment and shared storage space there. This allows agents to explore outside the main task,
such as tackling sub-problems or testing intermediate conjectures.
Besides the Research Center, the Station has an Archive Room where agents read and publish papers.
These papers are intended to synthesise an agent’s scientific findings, supported by their experiments in the
Research Center. A reviewer agent assesses each submission for rigor, novelty, and significance. Rejected
papers are returned with feedback and suggestions for revision. The accumulated papers form a miniature
scientific literature surrounding the given task that guides future agents (Figure 1(b)). For instance, one
agent can publish theoretical results ruling out part of the search space, allowing later agents to focus their
search elsewhere.
We compare the Station with related autonomous research systems in Table 1. These systems organise
research through predefined pipelines or centrally assigned tasks. The Station presents a distinct paradigm
by simulating a miniature scientific ecosystem. Agents act as independent researchers, choosing their own
research directions, performing experiments and publishing papers. Collaboration among agents emerges


                                                      2
                     Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




rather than being scripted. Knowledge accumulates through agents building a shared, reviewed literature
rather than storing experiment logs or research records.
We have made numerous improvements and extensions to the Station since the original paper. The overall
theme of these changes is to encourage novel but principled exploration while reducing non-scientific burdens.
For example, we introduced a new Question Room in which agents can pose their own questions and vote on
other agents’ answers, thereby broadening the scope of scientific exploration. Agents were also periodically
given holidays, during which they set aside their ongoing work and received random prompts designed to
encourage open-ended thought. We also gave agents access to coding assistants so that they need not spend
time on low-level coding or debugging and can instead focus on the scientific task, similar to how researchers
use coding assistants today. These changes are discussed in detail in Appendix A.



                          Agents                                  GPT 1             Claude 1            Gemini 1
          Choose rooms and actions at every tick
                                                             Choose direction    Choose direction    Choose direction
                                                                 Experiment         Experiment          Experiment
   Research                                                       Publish             Publish            Publish
      Research Center               Archive Room
     Read the task, submit
                                  Read papers, submit
      code, review results,
                                   papers for review,
     access a sandbox and                                                        Archive Room
                                    publish papers
        shared storage
                                                                                                         Paper 1
                                                                  Paper 1            Paper 1
   Communication                                                                                         Paper 2
                                                                                     Paper 2
                      Public Memory                                                                      Paper 3
     Mail Room            Room           Common Room

                                                                                     Time
   Direct messages    Persistent forum   Group discussion


   Notes, Reflection, and Exploration
     Reflection      Private Memory                               GPT 2             Claude 2            Gemini 2
                                         Question Room
     Chamber              Room
      Reflect on                             Ask new         Choose direction    Choose direction    Choose direction
                        Store private
     self-designed                        questions and
                      plans and notes                            Experiment         Experiment          Experiment
        prompts                          discuss solutions
                                                                  Publish             Publish            Publish




            (a) The Station environment.                             (b) Accumulation of scientific knowledge.

Figure 1: The Station environment and accumulation of scientific knowledge. (a) Rooms and their functions
in the Station. Each room serves a particular function and provides its own set of actions. At every tick,
agents freely choose which rooms to navigate to and which actions to take. Room-specific actions and
observations are described in Appendix A.3. (b) Multiple agents contribute to a shared scientific literature.
Each agent acts as a complete researcher, choosing its own direction, conducting experiments and submitting
papers. A reviewer agent reviews these papers for rigour, novelty and significance. Accepted papers are stored
permanently in the Archive Room, ready to be read, extended and cited by other agents, allowing scientific
knowledge to accumulate over time.




                                                             3
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




Table 1: Comparison with related autonomous research systems. Systems specialising in individual research
stages or other fields are excluded [12–15].
Systems             Research organisation    Mode of collaboration        Knowledge accumulation
AlphaEvolve,      Predefined pipeline: an        Through program reuse:          Experiment database: evalu-
OpenEvolve        evolutionary algorithm         models build on earlier pro-    ated programs, their results
and ShinkaE-      selects earlier programs,      grams selected by the evolu-    and, in some systems, ac-
volve [1, 16,     prompts models to modify       tionary algorithm.              companying analyses guide
17]               them and evaluates the                                         subsequent search through
                  resulting candidates.                                          evolutionary selection.

DeepEvolve        Predefined pipeline: lit-      Through specialised roles:      Experiment database: ear-
[18]              erature research and pro-      research proposals pass         lier algorithms, their descrip-
                  posal development are in-      to coding and evaluation        tions and evaluation results,
                  tegrated with evolutionary     stages, whose feedback in-      selected by the evolutionary
                  program search.                forms subsequent proposals.     algorithm, guide subsequent
                                                                                 research.

The AI Scien-    Predefined pipeline: re-        Through specialised roles:      Research records: literature
tist and Agent   search follows prescribed       each agent performs system-     summaries and experimental
Laboratory       stages of literature re-        assigned research functions     results are passed to subse-
[19, 20]         view, experimentation and       and passes its outputs to       quent agents according to
                 manuscript preparation.         other stages of the pipeline.   the predefined pipeline.

OpenAI mul-       Central coordination: a        Through assigned investiga-     Research records: an ap-
tiagent v2        root agent delegates inves-    tions: a root agent assigns     proach registry maintained
[21, 22]          tigations, redirects agents    tasks to sub-agents, then       by the root agent records
                  and synthesises their find-    synthesises their findings.     findings from sub-agents.
                  ings.

Kosmos [23]       Central coordination: the      Through assigned investi-       Research records: sum-
                  system assigns literature-     gations: specialised agents     maries of agents’ findings ac-
                  search and data-analysis       perform parallel tasks, and     cumulate in a shared record
                  tasks, using earlier find-     the system combines their       that informs centrally as-
                  ings to determine subse-       findings to guide further re-   signed research tasks.
                  quent tasks.                   search.

Station           Decentralised research:        Through a research commu-       Scientific papers: agents syn-
                  agents choose their own        nity: agents choose which       thesise their research into
                  research directions and        peers’ papers to read and       papers that explain their
                  activities, without a prede-   build upon. They can also       findings and present a sci-
                  fined pipeline or centrally    choose to communicate with      entific contribution. Sub-
                  assigned tasks.                peers through direct mes-       missions with limited signif-
                                                 sages and shared discus-        icance, including research
                                                 sions.                          records without broader im-
                                                                                 plications, are rejected.




                                                       4
                   Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




3     Results

3.1   Experimental setup

We evaluate the Station on mathematical problems drawn from the AlphaEvolve study of Georgiev et al. [24],
a broad catalogue spanning analysis, combinatorics, geometry, and number theory. Most can be formulated
as the optimization of an upper or lower bound on a numerical quantity: a candidate construction is checked
by an automated evaluator and assigned a numerical score, typically a scalar, which the search attempts
to optimize. In many cases, the optimal value is unknown, making the corresponding optimization task an
open research problem.
We select 12 problems that represent a range of mathematical areas and problem structures; the complete
set of evaluated problems is listed in Table 2. We assign each problem to an independent Station instance.
For each problem, the agents receive only the task statement, evaluator and a simple baseline, all of which
they can inspect. The task statement describes the mathematical problem and the evaluator function,
and may also specify additional mathematical goals that are not directly scorable. Web access is disabled
unless otherwise specified. No external expert guidance or literature survey is provided to the agents. Most
instances run for approximately 1,000–2,000 ticks, corresponding to roughly one to two weeks of continuous
wall-clock operation. Unless otherwise specified, all instances contain six research agents, two each powered
by GPT-5.5, Claude Opus 4.8, and Gemini 3.1 Pro.

3.2   Summary of findings

The results are summarized in Table 2. Based on the primary outcome of each run, five of the 12 problems
produced results novel relative to the prior literature. Of the remaining seven, the Station outperformed
AlphaEvolve on three problems, matched it on two, and underperformed it on two.
The novel results from these five problems span several areas of mathematics. In finite geometry, the Station
derived a new infinite family of Kakeya sets in F3p for primes p ≡ 3 (mod 4), and found a 53-point Kakeya set
in F53 , improving the previous bound of 63. In discrete geometry, it produced three exact 604-point kissing
configurations in dimension 11, two of which appear to define previously unknown isometry classes, and
established the new bound CT (128) ≤ 0.107067 for the discretized Kakeya needle problem. In analysis, it
improved the sign uncertainty upper bound to 0.3089 and closed approximately 82% of the previously open
gap for Erdős’s minimum overlap constant.
Beyond these 12 AlphaEvolve problems, we studied two additional case studies. For Book Ramsey numbers,
the Station agents discovered and proved two novel infinite families, while their finite constructions and
an earlier identity enabled an external expert to derive a third. Together, these three families prove the
conjecture at 43 values of n ≤ 200, resolving 28 cases that were previously open. For the Jacobian Conjecture,
the Station independently reconstructed the recently announced degree-seven counterexample from a formula-
free binary task and derived a geometric explanation of its constant Jacobian and three-sheeted fibers.
These results also show that the Station can directly pursue broader mathematical goals that are not neces-
sarily scorable. For example, the aforementioned infinite-family result for finite field Kakeya is not directly
scorable, even though new infinite families are the mathematical objects of interest. AlphaEvolve therefore
evaluated constructions on finitely many primes and relied on a task-specific pipeline, together with re-
searcher involvement, to turn promising outputs into infinite families. In the Station, by contrast, we stated
directly in the task statement that the finite constructions were test cases and that the primary goal was to
discover infinite families. This led the agents to independently recover the infinite family previously obtained
through AlphaEvolve and the subsequent researcher-assisted pipeline, and to discover a novel extension of
that family that improves the construction for an additional class of primes. Our role after the run was
limited to checking the validity of their proofs and the novelty of their results. This substantially reduces the
burden on researchers and makes the Station applicable to a much broader class of mathematical problems.
The results further show that the Station can produce unexpected contributions beyond the original task.
In Erdős’s minimum overlap problem, for instance, the agents were instructed to improve upper bounds,
yet they also developed a lower-bound proof that closed approximately 82% of the open interval. This


                                                       5
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




unexpected finding illustrates another strength of the Station: agents can explore mathematically promising
directions around the stated problem and produce contributions, such as new theorems, that lie outside the
assigned task.
Compared with AlphaEvolve, we find that Station agents tend to favor theory-guided constructions. Individ-
ual evaluations in these experiments are typically capped at 15–30 minutes, creating a strong incentive to use
mathematical structure to reduce the search space. In the kissing number task in dimension 11, for example,
the agents reduced the problem to a finite compatibility search over lines around a structured integer core.
This reduced search produced a 604-point configuration within minutes, which the agents later turned into
an explicit algebraic construction that requires no computer search. This is markedly different from AlphaE-
volve’s 593-point configuration, whose large, unequal-norm integer coordinates do not reveal a comparably
compact algebraic description or readily identifiable organizing structure [24]. This bias is not universally
advantageous. Peak and flat autoconvolution, on which the Station underperformed AlphaEvolve, appear to
reward persistent, large-scale heuristic optimization of highly irregular objects. The preferred system there-
fore depends on both the structure of the problem and the desired output. Large-scale evolutionary search
may be preferable when the strongest solutions are irregular artifacts found primarily through extended
numerical optimization. By contrast, the Station may have an advantage when theory can guide the search,
or when relevant theorems and interpretable constructions are valued alongside the benchmark score.
Detailed results for each problem are presented in Section 6. All presented discoveries are supported by exact
constructions or proofs formally verified in Lean. The supporting proofs, verification code and full agent
dialogues are available at https://github.com/dualverse-ai/station_data_v2.




                                                      6
                      Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




             Table 2: Important findings by the Station. All evaluated problems are included.
Problem                Source            Finding
Novel Results Relative to Prior Literature
Finite field Kakeya      AlphaEvolve      For every prime p ≡ 3 (mod 4), the Station constructed a Kakeya set in
(Section 6.1)            Problem 6.1      F3p of size (2p3 + 7p2 + 3)/8, saving (p − 3)/4 points over AlphaEvolve’s
                                          infinite family. It also found a 53-point set in F53 , improving AlphaEvolve
                                          and the previous literature bound of 63; both appear novel relative to the
                                          literature.
Erdős minimum over- AlphaEvolve           AlphaEvolve lowered the upper bound only slightly, from 0.380927 to
lap (Section 6.2)   Problem 6.5           0.380924, whereas the Station raised the lower bound from 0.37912 to
                                          0.380552. Relative to the published lower bound 0.37912, this closes ap-
                                          proximately 82% of the corresponding published gap.
Kissing number in        AlphaEvolve      AlphaEvolve raised the lower bound from 592 to 593, while the Station
d = 11 (Section 6.3)     Problem 6.8      constructed three exact 604-point configurations. One was an indepen-
                                          dent rediscovery of the EinsteinArena construction, while the other two
                                          appear to represent novel isometry classes.
Discretized Kakeya       AlphaEvolve      At n = 128, the Station obtained union area 0.107067, improving AlphaE-
needle (Section 6.4)     Problem 6.9      volve’s 0.114810 by 6.74% and HorizonMath’s 0.109148 by 1.91%. This
                                          establishes a new literature upper bound.
Sign uncertainty prin- AlphaEvolve        The Station lowered the upper bound to 0.3089, improving AlphaEvolve’s
ciple (Section 6.5)    Problem 6.11       0.321591 and the previously announced human value 0.3102. This is a
                                          new literature record.
Better than AlphaEvolve
Hardy–Littlewood         AlphaEvolve      The Station reached 1.557069, versus AlphaEvolve’s 1.5080 unguided and
maximal inequality       Problem 6.18     approximately 1.533 with hints, but the centered problem was already
(Section 6.6)                             solved. Its proof that the non-tangential constant equals 2 for 1/3 ≤ α <
                                          1 appears novel relative to the literature.
Ovals problem (Sec-      AlphaEvolve      AlphaEvolve recovered only the circle, while the Station recovered the
tion 6.7)                Problem 6.19     full family of noncircular equality ovals. This family was already known
                                          in the literature, so the result is novel only relative to AlphaEvolve.
Prime number theo-       AlphaEvolve      The Station certified 0.980681 for all x, improving AlphaEvolve’s sam-
rem (Section 6.8)        Problem 6.27     pled score of 0.938. This is new for the finite-weight benchmark; unre-
                                          stricted, the prime number theorem already gives the exact limit 1.
Ties with AlphaEvolve
Difference bases (Sec- AlphaEvolve        The Station independently recovered AlphaEvolve’s 360-element construc-
tion 6.9)              Problem 6.7        tion but did not improve upon it.
Sidorenko’s conjec-    AlphaEvolve        Neither AlphaEvolve nor the Station found a counterexample. No sub-
ture (Section 6.10)    Problem 6.26       stantive result was obtained.
Worse than AlphaEvolve
Peak autoconvolution     AlphaEvolve      The Station obtained C6.2 ≤ 1.504473, weaker than AlphaEvolve’s C6.2 ≤
(Section 6.11)           Problem 6.2      1.5032. No substantive result was obtained.
Flat autoconvolution     AlphaEvolve      The Station obtained C6.3 > 0.953189, weaker than AlphaEvolve’s C6.3 ≥
(Section 6.12)           Problem 6.3      0.961021, but proved that the unrestricted supremum can be approached
                                          using binary step functions on increasingly fine grids.
Additional Case Studies
Book Ramsey num-         Epoch AI         The Station independently discovered and proved two novel infinite fam-
bers (Section 6.13)                       ilies. Its finite constructions and an earlier identity also enabled an ex-
                                          ternal expert to derive a third. Together, the three families prove the
                                          conjecture at 43 values of n ≤ 200, resolving 28 previously open cases.
Jacobian Conjecture      Public           From a formula-free binary task, the Station independently reconstructed
(Section 6.14)                            the recently announced degree-seven counterexample and derived a geo-
                                          metric explanation of its constant Jacobian and three-sheeted fibers.




                                                          7
                            Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




4     Analysis
In this section, we analyze the discovery process using 28 individual findings from the spotlight results
presented in Section 6. Unless otherwise stated, all analyses are based on the 16 Station instances behind
the 14 problems studied. (The Kissing number in d = 11 and Book Ramsey numbers problems each have two
Station instances.) When a single spotlight contains multiple independently discovered findings, we count
those findings separately. We refer to these 28 findings as the selected findings, listed in Appendix C.

4.1   Nature and scope of discoveries

Station agents published a broad range of findings rather than only reporting constructions with high eval-
uator scores. We classified all 125 published papers in the kissing number first Station by their primary
contribution (Figure 2(a)). These papers included explanations of mathematical structure and obstructions
ruling out possible approaches, alongside constructions, bounds, methods and analyses. The resulting liter-
ature therefore contained knowledge that could guide further research on the task.
This breadth was also reflected in the 28 selected findings across the mathematical tasks (Figure 2(b)). Nine
were scored by the evaluator, seven were not scored but were requested in the task statement, and twelve
were neither scored nor requested. For example, in the Book Ramsey problem, agents went beyond the finite
constructions scored by the evaluator to discover and prove novel infinite families. Infinite families provide
substantially stronger results than individual finite constructions and deeper mathematical insight into the
problem [25]. This highlights the value of giving agents the autonomy to pursue research beyond optimizing
the evaluator’s score.

                                                                    Construction      Obstruction
       Construction
                                                                    Explanation       Bounds and optimality
                             12
       Explanation                                              Scored and within task
                                                 29
                                                                                                                  9
       Obstruction
                      9
                                                                Not scored and within task
       Bounds and optimality
                                    18                                    4              1        2    7
       Method
                                          23
                                                                Not scored and outside task
       Analysis
                                                      34            1         3               3                     5        12


      0               10            20           30        40   0                 3               6           9         12
                              Number of papers                                        Number of selected findings


                           (a) Published papers.                                       (b) Selected findings.

Figure 2: Nature and scope of discoveries. (a) Classification of all 125 published papers in the kissing
number first Station by their primary contribution. (b) The 28 selected findings across the mathematical
tasks, grouped by whether they were scored by the evaluator and requested in the task statement. Each
selected finding is further classified as a construction (an explicit example or family), explanation (underlying
mathematical structure), obstruction (a limitation of a method or family), or bounds and optimality.


4.2   Accumulation of scientific knowledge

The Station’s accumulated papers allowed agents to build on one another’s findings, leading to a growing
literature with extensive citations. For example, the kissing number first Station produced 125 papers with
923 citation links between them (Figure 3(a)). Earlier papers often provided important steps for later
discoveries. In the finite field Kakeya problem, a Gemini agent introduced a promising construction and
tested it computationally in an early paper. A GPT agent then proved that only two classes of parameter
choices needed to be considered and identified the better one in another paper. A Claude agent subsequently
built on these papers to derive the exact size and prove that the construction works for every odd prime,
yielding the new infinite family described in Section 6 (Figure 4(c)). More broadly, we found that earlier


                                                                8
                                       Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




papers contributed to 21 of the 28 selected findings (Figure 5), indicating their importance for subsequent
discoveries. Thirteen of the 28 selected findings emerged after tick 1,000, including the Book Ramsey
conference-graph family at tick 3,727 (Appendix B.2).
Review helps maintain the reliability of this accumulated knowledge. We analysed paper reviews in the same
kissing number Station. Of the 125 published papers, 55 had been rejected at least once before acceptance
(Figure 3(b)). Across all submissions, 199 were rejected, with reasons including overstated claims, missing
references, incomplete manuscripts, limited significance and factual errors (Figure 3(c)). The ablation study
in Section 4.5 also showed that removing accumulated papers sharply reduced discovery performance. In one
Station without papers, an agent wrongly claimed that a broad class of constructions could not exceed 582
points, and other agents adopted this unsupported limit. These observations suggest that reviewed papers
help agents build on reliable knowledge rather than accumulate shared misconceptions.

                                                                                                           80




                                                                                        Number of papers
                                                                                                                70
                     1
                                                                   Paper #10
                                                                                                           60
                                                       600-point construction

                    25                                                                                     40             30

                                                                                                           20                    10     8
 Citing paper ID




                                                                   Paper #73                                                                   3   2    1     0     1
                    50                                 604-point construction                               0
                                                                                                                0         1      2      3      4   5    6     7     8
                                                                                                                              Rejections before publication
                    75                                               Paper #89
                                                                    Explains its
                                                                  lattice origin                                (b) Rejections before publication.

                   100
                                                                                                 Overstated claims
                                                                                                                                                              93.5%
                                                                                                 Missing references
                   125                                                                                                                 46.2%
                                                 125 papers · 923 citation links
                                                                                                 Incomplete manuscript
                             44                                                                                                       44.7%
                    50
        Citations




                                                                                                 Limited significance
                                                             23                                                                       43.2%
                    25                                18
                                                                                                 Factual errors
                     0                                                                                                         32.2%
                         1        25        50         75         100         125
                                                                                             0                       25                50          75         100
                                            Cited paper ID
                                                                                                                                  Rejections (%)

                                  (a) Citation relationships.                                                             (c) Reasons for rejection.

Figure 3: Accumulation and review of papers in the kissing number first Station. (a) Citation relationships
among all 125 published papers. Each square in the upper plot marks a citation from the paper on the
vertical axis to the paper on the horizontal axis; the bars below show citations received by each paper. (b)
Number of rejections before successful publication for these papers. (c) Reasons for rejection across all 199
rejected submissions. Percentages can sum to more than 100% because a rejection can have multiple reasons.


4.3                 Collaboration across model families

One characteristic of the Station is that it allows agents from different model families to collaborate. We
therefore ask how often agents from different model families worked together on a selected finding. We
examine all 28 selected findings. We count an agent as a contributor when its work was used materially
in the result, for example when it contributed a theorem, construction, method, or research direction that
another agent used.
We find that 13 of the 28 selected findings (46.4%) involved agents from more than one model family, as
shown in Figure 4(a). Among the remaining 15 results, 6 were still joint work by several agents from the
same model family. Thus, only 9 of the 28 results (32.1%) were found by one agent working alone, while
19 (67.9%) involved more than one agent. We also examined how these collaborations took place. Most
occurred through the Archive Room (Figure 4(b)), with an example shown in Figure 4(c). Claude agents


                                                                                    9
                           Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




took part in all 13 cross-model findings. To test whether Claude agents alone were sufficient, we replaced
all six agents with Claude agents. This led to a sharp drop in discovery performance on the kissing number
task (Section 4.5). Together, these findings suggest that collaboration across model families is important for
certain discoveries.

      Single agent                         9 (32%)

 Several agents,                      6 (21%)
one model family
   Claude + GPT                        7 (25%)        Paper 72 · Claude      Symploke IV · Tick 1,041      Paper 160 · Claude
                                                                                                           Daedalus XIV · Tick 2,641
                                                      Method for analysing inversion maps
Claude + Gemini            2 (7%)
                                                                                                           “Archive #72 (Symploke IV) computed the
 Claude + GPT +               4 (14%)                                                                      inversion map's profile…”
         Gemini                                       Paper 91 · Gemini       Bourbaki IV · Tick 1,244

                     0            5         10        Proposes and tests a construction family
                           Selected findings                                                               “Archive #91 (Bourbaki IV) introduced the
                                                                                                           fractional-linear family…”

(a) Agent and model-family participation.             Paper 102 · GPT           Parallax II · Tick 1,416

                                                      Reduces parameter choices to two classes             “Archive #102 (Parallax II) … We use those
  Archive Room                             8 (62%)                                                         theorems as inputs…”


       Mail Room           2 (15%)
                                                      Mail · GPT                Noesis III · Tick 2,629    Main result

Research Center            2 (15%)                    Encourages a size formula and a coverage             Derives an exact size formula and proves
                                                      proof.                                               validity for every odd prime.
                                                      “a size formula and coverage proof … would give
 Question Room           1 (8%)                       a real construction theorem”

                     0            5              10
                         Cross-model selected              (c) Papers and peer mail leading to finite field Kakeya S1.
                               findings

  (b) Primary communication channel.

Figure 4: Collaboration across agents and model families. (a) Agent and model-family participation in the 28
selected findings. (b) Primary communication channel for the 13 findings involving multiple model families.
Each finding is assigned to the channel through which its most important shared work passed. (c) Papers
and peer mail contributing to the new infinite family of finite field Kakeya sets.


4.4     Station mechanisms

The Station is designed to foster scientific discovery through several mechanisms. These mechanisms are
described in detail in Appendix A. Here we briefly introduce several additional mechanisms and examine
their contributions to the selected findings.

       • Holiday. The final two ticks of every ten-tick period are declared a holiday; agents cannot submit
         code or archive papers and instead receive prompts encouraging broad reflection, metaphors, or
         ideas from other fields. This pause often led agents to reconsider a failed approach or explore a less
         obvious direction.
       • Stagnation protocol. If the official evaluation frontier does not improve for a long period, the Station
         asks agents to review the internal literature, question their assumptions, and pursue different high-
         level strategies. This helps agents leave exhausted local approaches and pushes them toward bolder
         attempts and wider exploration.
       • Supervisor. The Station randomly appoints one eligible agent to serve as supervisor. The supervi-
         sor gives high-level guidance, encouraging persistence and preventing agents from duplicating one
         another’s work while leaving them responsible for their own research; between appointments, the
         Station deliberately leaves long periods without a supervisor to encourage less structured exploration.

We reviewed the dialogue underlying each of the 28 results and classified each mechanism as making a
direct contribution, an indirect contribution, or no material contribution to the discovery (Figure 5). A
contribution was direct when the mechanism supplied a decisive idea or intervention, and indirect when it


                                                                      10
                        Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




shaped or supported the research without being the immediate source of the result. We assigned no material
contribution when the dialogue showed no clear causal role.
Holiday and archive papers contributed directly or indirectly to 23 and 21 of the 28 results, respectively,
followed by the stagnation protocol with 14. During holidays, agents often stepped back from active optimiza-
tion, examined why an earlier approach had failed, and reframed the problem or explored a new direction;
these reflections frequently supplied ideas that later became part of a selected finding, explaining the high
contribution rate. Archive papers also contributed to a significant portion of the results, indicating that the
Station’s accumulated knowledge was useful for later discoveries.


                 Holiday                           14                                                 9                         5

           Archive paper                                  18                                              3                 7

      Stagnation protocol                 10                              4                                    14

  Peer communication                 8                          4                                         16

              Supervisor             8                          4                                         16

          Question Room          5             2                                                 21

                            0               20                       40                     60                      80              100%
                                                               Share of selected findings
                                         Direct contribution        Indirect contribution        No material contribution


Figure 5: Contribution of Station mechanisms to the 28 selected findings. The numbers within each bar give
the number of results in each category.


4.5     Baseline and ablation experiments

To compare the Station with other autonomous research systems, we evaluated four baselines on the same
eleven-dimensional kissing number task: OpenEvolve powered by Claude Opus 4.8, Gemini 3.1 Pro or GPT
5.5 [16], and OpenAI’s multiagent v2 powered by GPT 5.5 [21]. For multiagent v2, we adapted the prompt
released by OpenAI for its proof of the Cycle Double Cover Conjecture [22]. We ran three independent
seeds per configuration. All baselines received the same task statement as the Station and followed the same
two-stage setup: first finding a valid 594-point configuration, then seeking larger valid configurations.
The Station and each baseline were compared under a matched budget of 8,000 minutes of cumulative
evaluator execution time, summed across experiment submissions (Figure 6(b)). None of the baseline config-
urations produced a valid 594-point configuration, whereas all three Station seeds reached 604 points within
this budget. Output-token usage is reported in Appendix B.3. We observed that the baseline searches were
strongly constrained by a central coordinator—the evolutionary algorithm in OpenEvolve and the root agent
in multiagent v2 [16, 21, 22]. This may limit their ability to use intermediate theorems to guide the search
for algebraic constructions, as Station agents did.
We also conducted two ablation studies to examine the contributions of accumulated papers and collaboration
across model families (Figure 6(a)). In the first, we removed the Archive Room from the Station, so agents
could neither read nor publish papers there. They could still communicate through other rooms, such as
sending direct mail. In the second, all six research agents were powered by Claude Opus 4.8, maintaining
the same population size as the standard Station. We chose Claude because its agents were particularly
productive, making the primary discovery for 18 of the 28 selected findings (Appendix B.1). We ran three
independent seeds for each ablation and compared their progress with the standard Station through tick
500.
Both ablations sharply reduced discovery performance. Neither produced a valid 594-point configuration
during the comparison, whereas all three standard Station seeds discovered valid 594-point constructions
and subsequently reached 604 points through different mathematical approaches (Section 4.6). We found
that both baselines and ablations struggled to turn near-miss configurations into valid constructions: despite


                                                                     11
                                      Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




a tiny overlap loss, many pairs of spheres could still overlap. Station agents encountered the same bottleneck
but overcame it by analysing the structure of these near-miss configurations and identifying an exact core.
These results suggest that both accumulated papers and collaboration across model families contributed to
discovery on this task.


                         604                                                                                     604


                         600                                                                                     600



                     N = 594                                                                                 N = 594
                                                        Proven lower bound N                                                                      Proven lower bound N
Best-so-far result




                                                                                        Best-so-far result
                                                               Numerical loss                                                                             Numerical loss
                     0 (float)                                                                               0 (float)
                                                          Ablations: 0/6 exact                                                                     Baselines: 0/12 exact
                            −16                                                                                     −16
                       10                                                                                      10


                       10−12                                                                                   10−12


                        10−8                                                                                    10−8


                        10−4                                                                                    10−4


                         100                                                                                     100

                     L = 103                                                                                 L = 103
                                  0   100      200       300      400        500                                          0    2,000       4,000         6,000        8,000
                                                Station tick                                                                  Cumulative compute time (min)

                         Station                                                                                 Station
                         Station with Claude only                                                                OpenEvolve (Claude Opus 4.8)
                         Station without accumulated papers                                                      OpenEvolve (Gemini 3.1 Pro)
                                                                                                                 OpenEvolve (GPT 5.5)
                                                                                                                 OpenAI multiagent v2 (GPT 5.5)


                                        (a) Ablations.                                                                          (b) Baselines.

Figure 6: Baseline and ablation experiments on kissing numbers in eleven dimensions. (a) The full Station
compared with a Station without accumulated papers and a Station using six Claude agents, with three
independent seeds; the first 500 ticks are shown. All three full Station seeds reached 604 points after tick
500 (Figure 7). (b) The Station compared with OpenEvolve using Claude Opus 4.8, Gemini 3.1 Pro or GPT
5.5 and OpenAI’s multiagent v2 using GPT 5.5, with three independent seeds under the same budget of
8,000 minutes of cumulative evaluator execution time. All three Station seeds reached 604 points within
this budget. In both panels, the lower region shows the overlap loss L of invalid 594-point configurations.
A near-zero positive loss remains invalid and does not establish a kissing number lower bound. The shaded
upper region shows only verified valid configurations, whose size N establishes a lower bound on the eleven-
dimensional kissing number.


4.6                    Result reproducibility

We are also interested in whether the discoveries are reproducible. We therefore ran three independent
Station instances, all without web access, on the kissing number problem in dimension eleven. Figure 7
shows the best certified lower bound reached in each run. All three Stations eventually reached N = 604,
indicating that the improved lower bound is reproducible.
Closer inspection, however, shows substantial variation in both the time required and the route to the result.
Station 1 pursued discrete exact line packing around lattice-derived cores. It obtained Construction 3 by
selecting 54 mutually compatible lines that form a 108-point algebraic extension of a 496-point core, and
later obtained Construction 2 while exploring a different core and extension. Station 2 instead assembled
Construction 1 from root-system motifs under a common rotation; its final step was to recognize that eleven


                                                                                   12
                                             Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




                                                                    Construction 1               Construction 1   Construction 3     Construction 2
                                   604
                                   602



          Best exact lower bound
                                   600
                                   598
                                   596
                                   594
                                   592
                                   590
                                   588
                                   586                                                                                                       Station 1
                                                                                                                                             Station 2
                                   584
                                                                                                                                             Station 3
                                   582
                                         0            250           500               750                 1000                1250                    1500
                                                                                          Tick

Figure 7: Best certified lower bound across three independent Station instances for the kissing number prob-
lem in dimension eleven. Station 1 discovered Constructions 2 and 3, while Stations 2 and 3 independently
discovered Construction 1.


points formed all but one vertex of a cuboctahedron and to add the missing twelfth vertex. Station 3 reached
the same construction class through a different mechanism: it deformed an exact 601-point configuration
so that two coordinate vectors and one additional vector supported on a distinguished three-dimensional
subspace could be appended. Thus, the same numerical lower bound emerged from markedly different
mathematical representations and research paths.
This variation partly arises from the Station’s cumulative knowledge. Small differences in the initial trajectory
change which results enter the archive paper collection. Later agents then inherit different starting points, so
differences in research paths and accumulated archive papers compound over time. Therefore, given the high
variance across Station instances, running several independent instances on the same problem is advisable
when computational cost is not a concern.




                                                                                     13
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




5   Discussion and Conclusion
We observe rapid improvement in the capabilities of AI agents. In the initial version one year ago, agents
frequently hallucinated and could not reliably learn the rules of the environment. Agents can now master
the environment and autonomously produce novel discoveries. Nonetheless, multi-agent research still has
several important limitations. We summarize our observations below.

     • Lack of expert intuition. By intuition, we mean the ability to judge whether a research direction is
       promising before pursuing it. Good intuition makes exploration more efficient and allows a researcher
       to investigate promising directions more deeply. Across the runs, we observed multiple cases in
       which agents deprioritized promising approaches on weak grounds, delaying or missing potential
       breakthroughs. This indicates a lack of the intuition that a human expert in the field would typically
       possess.
     • Lack of diverse research tastes. A preference for particular concepts or methods is difficult to judge
       as objectively good or poor. However, when all agents share similar tastes, the overall scope of
       exploration becomes narrow. Across the runs, agents from the same model family often proposed
       similar research ideas, suggesting that model-specific tastes reduce the diversity of exploration.
     • Limited in-context learning. Agents can absorb new research knowledge through their context, but
       this knowledge does not update their pretrained weights. As the Station’s accumulated knowledge
       grows, agents may therefore struggle to absorb it fully and build on it effectively. We occasionally
       observed agents fail to recognize how their own line of research connected to earlier Station knowledge,
       causing them to miss a potential discovery.
     • Attractor traps. When given autonomy, some agents become absorbed in tasks or activities that we
       call attractors. These activities are often rewarding in some immediate sense but make little mean-
       ingful contribution to the main problem. Agents may also become absorbed in technical details that
       a human expert would quickly recognize as trivial or irrelevant to the main question. Examples in-
       clude repeatedly rerunning the same optimization script with different random seeds or exhaustively
       diagnosing and characterizing every local optimum.

Several Station mechanisms are designed to mitigate these limitations. For example, using agents from
multiple model families broadens the range of research tastes, while the stagnation protocol helps agents
escape attractor traps. Nevertheless, these problems persist to some degree, and substantial gaps remain
between AI agents and human experts in all four respects. Lightweight guidance or occasional intervention
from human experts would likely be beneficial by directing agents toward promising research areas. The
current Station supports such human involvement, e.g., through messages broadcast to all agents, but we
leave a systematic study of human–AI collaboration to future work.
Although this paper uses the Station primarily for mathematical exploration, the Station is designed as a
general research environment, and none of its mechanisms is tailored specifically to mathematics. As demon-
strated in the original paper, the Station can be applied to problems spanning mathematics, computational
biology, and machine learning [6]. Large-scale research explorations in other fields, including research on
language models themselves, may therefore be promising.
As AI agents become more capable, we expect autonomy and generality to become increasingly important
principles for designing AI research environments. Stronger agents need not be confined to increasingly
elaborate pipelines; they have the ability to determine how to pursue a goal, learn from failure, exchange
ideas, and accumulate knowledge over time. The greater autonomy provided by the Station may allow these
capabilities to be more fully realized.




                                                      14
                   Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




6     Detailed Results
This section presents the most important findings for each problem. Because each Station run produces
many findings, we restrict the main text to results likely to interest external researchers. We first use agents
external to the Station to screen the findings automatically. A finding passes this screen if it advances the
frontier on the original problem, for example by improving a known bound; answers a question previously
raised in the literature; or has a broader variant that would ordinarily warrant inclusion in a research paper.
We then manually review the screened results and select the most important ones for presentation here. We
refer to these selected results as spotlight findings and label them S1, S2, and so forth within each problem
below. All theoretical findings presented here were formally verified in Lean, with assistance from GPT
5.5 operating outside the Station. Findings of marginal or uncertain significance remain documented in the
accompanying notebooks.

6.1   Finite field Kakeya

A Kakeya set in Fdp is a set that contains a full line in every direction, and the problem is to make one as
small as possible. Dvir’s proof of the finite field Kakeya conjecture [26] established a lower bound of order pd .
Subsequent work of Bukh and Chao [27] settled the leading asymptotic constant, showing that it is 2−(d−1)
in every fixed dimension and hence 1/4 in dimension 3. What remains open is the lower-order correction to
this leading term. Exact constructions that improve the pd−1 and smaller terms therefore sharpen the best
known bounds even though the leading constant is already settled.
AlphaEvolve took this problem up as Problem 6.1 of its collection, asking for small Kakeya sets. A construc-
                                                                                                      d−1 d−1
tion is scored there by the average of |Kp |/Bp,d over a fixed list of primes, where Bp,d = (p−1) p+1
                                                                                                   2      +p
is the size of the classical construction as recorded by Bukh and Chao [27]. We gave the Station the same
problem and the same score, in dimensions 3, 4 and 5 at once. It proved a new infinite family of Kakeya sets
in d = 3, found a Kakeya set of 53 points in F53 , and established a structural limit for the entire one-pole
family behind the new construction.

S1. A new infinite family in d = 3 for p ≡ 3 (mod 4). The Station proved that for every prime p ≡ 3
(mod 4) there is a Kakeya set in F3p of size (2p3 + 7p2 + 3)/8. Writing S for the squares of Fp including 0,
the set is
                             Kp = {(x, y, z) : x2 + 4y ∈ S, x2 + 4z ∈ S}
                                      ∪ {(0, t, ct + z(c)) : t ∈ Fp , c ̸= 1}
                                                                              c
                                      ∪ {(0, t, t)} ∪ {(0, 0, z)},      z(c) =   .
                                                                            c−1
The first part is the classical quadratic residue set, and it already covers the p2 directions (1, a, b); the lines
added in the plane x = 0 cover the remaining p + 1. Notably, nothing in the definition depends on p modulo
4, and the agents proved the set is Kakeya for every odd p. The size, however, does depend on p modulo 4,
through whether −1 is a square, and we record both cases:
                      2p3 + 7p2 − 1                                     2p3 + 7p2 + 3
            |Kp | =                    (p ≡ 1 mod 4),         |Kp | =                   (p ≡ 3 mod 4).         (1)
                            8                                                 8
The classical construction in this dimension has (2p3 +10p2 −2p−2)/8 points, so the saving is (3p2 −2p−1)/8
points when p ≡ 1 and (3p2 − 2p − 5)/8 when p ≡ 3. In particular this is an exact size where the literature
leaves an O(p) error term [27].
AlphaEvolve approached this problem by a different route, and we find that the two constructions agree in
one case but not in the other. For p ≡ 1 (mod 4) the constructions have the same size, and in fact are the
same set. A linear change of coordinates carries one onto the other, so the first case of (1) is an independent
rediscovery of the bound 14 p3 + 78 p2 − 81 obtained there. For p ≡ 3 (mod 4) they differ. The smallest size
AlphaEvolve’s infinite family gives on this class is (2p3 + 7p2 + 2p − 3)/8, and ours is (2p3 + 7p2 + 3)/8, a
saving of (p − 3)/4 points. That is 1 point at p = 7 and 11 at p = 47, the largest prime of this class in
the benchmark. The second case of (1) is therefore new and gives the best infinite-family bound currently
available in the literature.


                                                         15
                                                    Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




|Kp| / Bp, d (lower is better)                        d=3                                             d=4                                    d=5
                                                                                                                           0.625
                                 1.00                                            0.85
                                                                                                                           0.600
                                 0.95                                            0.80                                      0.575

                                 0.90                                            0.75                                      0.550

                                 0.85                                                                                      0.525
                                                                                 0.70
                                                                                                                           0.500
                                 0.80
                                                                                 0.65
                                                                                                                           0.475
                                 0.75
                                        3 5 7 11 13 19 23 29 31 37 41 43 47 53          3   5    7    11    13   17   19            3    5         7   11
                                                                                                 prime p
                                                                   Pre-AlphaEvolve literature              AlphaEvolve         Station

Figure 8: Kakeya set sizes at the 25 pairs (d, p) of the benchmark, divided by the size Bp,d of the classical
construction; lower is better. Pre-AlphaEvolve literature is the smallest size obtained from the explicitly
defined families predating AlphaEvolve documented in Section 7 of the finite field Kakeya verification note-
book in our data repository. The Station is below both reference curves at 5 of the 14 pairs in d = 3, 5 of
the 7 in d = 4 and all 4 in d = 5, and equal to the lower of the two elsewhere. The three panels are not
comparable with each other, since Bp,d is a tighter reference in higher dimensions.


S2. Finite improvements and a 53-point Kakeya set in F53 . The Station wins 14 of the 25 finite benchmark
comparisons and ties the remaining 11 (Figure 8). Each comparison uses the better of AlphaEvolve and
the pre-AlphaEvolve literature as its baseline. The case (d, p) = (5, 3) is especially notable. Let kn denote
the minimum size of a Kakeya set in Fn3 . The Station constructed a 53-point set in F53 , improving the
previous bound from k5 ≤ 63 to k5 ≤ 53 [28]. In light of the known values k1 = 3, k2 = 7, and k3 = 13,
together with the bound k4 ≤ 27, which is believed to be sharp, it was guessed in 2009 that the recurrence
kn = kn−1 + 2kn−2 continues, predicting k5 = 53 [28]. The size of the Station’s construction therefore
coincides with the guessed value, although whether (k5 = 53) holds and whether the recurrence continues
remains open.

S3. Structural analysis of the new infinite family. The agents also produced relevant insights into the new
infinite family. They analyzed the more general completion
                                                                                                 Ac + B
                                                                                        z(c) =          ,
                                                                                                 c − p1
which includes the construction in S1. Eliminating the slope c reduces incidence with these lines to whether

                                                                                 (z − A − p1 y)2 − 4(Ap1 + B)y

is a square. A quadratic-character calculation then shows that the lines cover exactly p(p − 1)/2 points away
from the axis, independently of the three parameters. Their overlap with the quadratic-residue part of the
construction is always p2 /8 + O(p). Consequently, every nondegenerate completion in this Möbius family
adds 3p2 /8 + O(p) points: changing the numerator or the location of the pole affects only the lower-order
terms.
For the particular choice z(c) = c/(c − 1) used in S1, the agents evaluated the lower-order term exactly,
yielding the infinite family stated in (1). The result also explains AlphaEvolve’s infinite family for p ≡ 1
(mod 4). More generally, the class-wide estimate shows that improving the p2 term in the total size requires
leaving the one-pole family.

Limitations. The new infinite family is confined to d = 3. In dimensions 4 and 5 the formulas the agents
proved are weaker than what is already known. On the shared class p ≡ 1 (mod 4) the first two coefficients
agree with AlphaEvolve in each dimension and the third is worse in both.


                                                                                                 16
                         Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




                                  White                                                                                          Haugland
                               0.379005                                                                                          0.380927
Pre-AlphaEvolve literature
              2016–2023
                                  White                                                                                          AlphaEvolve
                               0.379005                                                                                          0.380924
               AlphaEvolve
                     2025
                                   Kim–Pilanci                                                                                Ye et al.
                                     0.379120                                                                                 0.380868
      Pre-Station literature
                       2026
                                                                                                           Station            Ye et al.
                                                                                                         0.380552             0.380868
                   Station
                     2026
                                    0.3790              0.3794             0.3798              0.3802                0.3806     0.3810
                                                                              value of μ
                                                                           lower bound     upper bound


Figure 9: Successive published bounds for Erdős’s minimum overlap constant. Each horizontal segment joins
the best lower and upper bounds at the indicated stage. The Station raises the lower bound from 0.37912
to above 0.380552, closing approximately 82% of the previously open interval.


                                   d      Station                          AlphaEvolve
                                   4      1 4
                                          8
                                            p + 19
                                                32
                                                   p3 + 32
                                                        25 2
                                                           p + O(p)         1 4
                                                                            8
                                                                              p + 19
                                                                                  32
                                                                                     p3 + 11
                                                                                          16
                                                                                             p2 + O(p3/2 )
                                          1 5     47 4     25 3                             177 3
                                   5      16
                                             p + 128
                                                     p +   32
                                                              p + O(p2 )    1 5
                                                                            16
                                                                                    47 4
                                                                               p + 128 p + 256  p + O(p5/2 )


The sizes we report at individual primes in d = 4, 5 do still improve on the benchmark, but they come from
search rather than from a formula.

6.2    Erdős minimum overlap

Erdős’s minimum overlap problem asks how evenly two complementary parts of an interval can avoid one
another under translation. Let f : [−1, 1] → [0, 1] be measurable with integral 1, put g = 1 − f on [−1, 1],
and extend both functions by zero outside the interval. Write
                                      Z 1
                             Cf (x) =      f (t)g(t + x) dt,  µ = inf ∥Cf ∥∞ .
                                                        −1                                 f

This constant is the continuum form of Erdős’s minimum overlap problem for balanced partitions of long
integer intervals [29–31]. AlphaEvolve took up this problem as Problem 6.5 of its mathematical collection
and improved Haugland’s upper bound from 0.380927 to 0.380924, while later work further reduced it to
0.380868 [32]. On the lower-bound side, Kim and Pilanci established 0.37912 [33]. Thus, immediately before
this work, the best published bounds were

                                                          0.37912 ≤ µ ≤ 0.380868.

S1. A new lower bound of 0.380552.                     The Station agents proved

                                                                 µ > 0.380552.                                                            (2)

Relative to the previously published lower bound of 0.37912, this reduces the corresponding published open
interval by approximately 82%, as shown in Figure 9.
The agents achieved this lower bound by translating the overlap problem into phase-sensitive Fourier con-
straints and combining them into four global inequalities that cover every possible first moment of an ad-
missible overlap. A key element of the proof is a sharp relation that couples the cosine and sine information
at any real frequency. Writing P (ξ) and Q(ξ) for the cosine and sine transforms of Cf , and s(ξ) = sin(ξ)/ξ,
the agents proved
                                                    Q(ξ)2
                                   P (ξ) ≤ s(ξ)2 −              s(ξ) ̸= 0 .
                                                                         
                                                    4s(ξ)2



                                                                       17
                   Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




White had already used Fourier phase information and convex optimization, while Kim and Pilanci later
introduced additional moment constraints [31, 33]. Relative to these earlier methods, the formulation used
here eliminates the unknown transform of f , directly constrains the overlap, and remains available at arbitrary
real frequencies. More broadly, the result shows that the established Fourier approach has much greater reach
when this phase coupling is retained, and suggests an analytic route toward further narrowing the remaining
gap.

Comparison with AlphaEvolve on the upper bound. The Station agents independently obtained µ <
0.380895, a slight improvement on AlphaEvolve’s published upper bound of 0.380924. However, this re-
mains above the current published upper bound µ < 0.380868 of Ye et al. [32]. The Station therefore did
not establish a new upper-bound record.

6.3   Kissing number in d = 11

The kissing number K(d) is the largest number of nonoverlapping unit spheres that can simultaneously touch
a central unit sphere in Rd . Equivalently, it is the largest size of a set of unit vectors whose pairwise inner
products are at most 1/2. AlphaEvolve took up this classical question as Problem 6.8 of its mathematical
collection and improved the lower bound in dimension eleven from 592, established by Ganzhinov using highly
symmetric lines [34], to 593. We ran two independent Stations on the same problem using AlphaEvolve’s
scoring rule, which measures the total pairwise overlap among the surrounding spheres. Neither Station
had access to external information, including the 592- and 593-point constructions just mentioned. Both
reached 604 points, proving K(11) ≥ 604. Together, the two runs yielded three exact, pairwise non-isometric
604-point constructions.

S1. Three exact 604-point kissing configurations. The Station discovered three geometrically √ distinct 604-
point kissing configurations in R11 . All three are exact equal-norm arrangements over Q( 2), but they
organize their points differently: two are centrally symmetric, one is not, and each has a different contact
structure and set of pairwise angles. Figure 10 visualizes their shared architecture and the two structural
choices that distinguish them. We label them Constructions 1, 2, and 3:

                                 Construction                 1       2      3
                                 Touching pairs           19,704 22,904 22,840
                                 Centrally symmetric         Yes    Yes    No
                                 Antipodal pairs             302    302    238
                                 Distinct pairwise angles     22     14     15


The different numbers of touching pairs prove that the configurations are pairwise non-isometric, since
this number is preserved by orthogonal transformations and relabeling. Constructions 1 and 2 contain the
antipode of every point, but Construction 2 has 3,200 more touching pairs and eight fewer pairwise angles.
Construction 3 has 128 points without antipodes. Among the three, Construction 2 has the most contacts
and the smallest angle set, while Construction 1 has the fewest contacts and the largest angle set. Thus the
same record size supports substantially different geometries.
In concurrent work, Bianchi et al. reported Construction 1 from the EinsteinArena platform shortly before
our public release of Construction 3 [35]. EinsteinArena is an open online platform that accepts candidate
artifacts from any participant and makes them publicly verifiable. The 604-point construction appears to
have resulted from collaboration among multiple independently operated AI harness systems on the platform.
The Station results, by contrast, came from two independent closed-internet executions of our end-to-end
open-source system: one independently recovered Construction 1, while the other discovered Constructions
2 and 3. The Station therefore discovered Construction 1 independently, while Constructions 2 and 3 are,
to our knowledge, novel Station discoveries representing two additional isometry classes.

S2. An algebraic construction for a 604-point kissing configuration in R11 . The agents first discovered
Construction 3 by searching for 54 compatible lines around a 496-point integer core. They later showed that


                                                      18
                       Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




            (a) Construction 1                                       (b) Construction 2                                      (c) Construction 3
        Core type I + extension type I                          Core type I + extension type II                         Core type II + extension type II

              432-point shared core      64-point core type I      64-point core type II   108-point extension type I      108-point extension type II




Figure 10: The three 604-point kissing configurations in R11 , shown under the same orthogonal projection
into R3 . All three share the same 432-point rational core, shown in light gray, and each has the form
432 + 64 + 108. Constructions 1 and 2 use the same 64-point core type, so their complete 496-point cores
agree, but they use different 108-point extensions. Constructions 2 and 3 use the same extension but different
64-point core completions. The colored spheres distinguish the two core types and the two extension types.


the same configuration is governed by a compact algebraic rule rather than an arbitrary list of coordinates,
yielding an explicit algebraic construction. The construction itself requires no computer search. First, the
496-point core is generated from sparse norm-four integer vectors using fixed support and sign rules. Second,
in a coordinate frame rotated by 45◦ in one coordinate plane, eleven simple sign patterns generate
                                                                                              √        all 54
lines; taking both directions on each line gives the 108-point extension. The appearance of 2 is intrinsic:
it is forced by the compatibility between the extension and the core.
The support structure of the core explains why these additional points fit. It leaves extra angular room in a
distinguished three-dimensional subspace, within which six mutually compatible lines can be placed. Among
the remaining eight coordinate axes, the core admits exactly four viable pairs, each supporting a unique
group of twelve additional lines together with the distinguished subspace. These four pairs are disjoint,
so their groups are mutually compatible. The support and sign rules also ensure that every new point
satisfies the kissing constraint with every point of the core. The resulting configuration therefore contains
496 + 2(6 + 4 · 12) = 604 points.

S3. Why the classical D11 construction stops at 582. The agents investigated whether a better search could
find a larger configuration within the classical norm-four D11 construction. They proved that the answer is
no: regardless of the search algorithm or any assumed symmetry, this construction can contain at most 582
compatible points. Reaching 593 or 604 points therefore requires leaving the classical construction. This
result ruled out any improvement using only vectors from the norm-four shell and redirected the agents
toward constructions that augment a lattice-derived core with additional vectors, ultimately producing the
604-point configuration.
The agents proved this limit by showing that sign choices cannot overcome the underlying restriction on
which sets of four coordinates may be used. Let A(n, 4, 4) denote the largest compatible collection of four-
coordinate supports, and let α(J± (n, 4)) denote the largest compatible collection after signs are assigned to
those coordinates. The agents proved

                                                          α(J± (n, 4)) = 16 A(n, 4, 4).                                                                    (3)

In other words, allowing arbitrary signs increases the optimum by exactly the 16 possible sign patterns on
four coordinates; it cannot produce any additional advantage.


                                                                               19
                   Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




Best proved in 1977 that A(11, 4, 4) = 35 [36]. The agents’ identity therefore limits the signed weight-four
part of the construction to 560 points. The remaining 22 coordinate vectors {±2ei } are compatible with
these points, giving an exact limit of 582 for the complete norm-four D11 construction.
The agents in both closed-internet Station runs independently derived Equation (3). We later found that
it overlaps with the k = 4 case of Theorem 1 in a paper by Takhanov and Yun, made publicly available
only recently, on June 2, 2026 [37], where the identity serves as the foundation for a broader classification of
signed kissing configurations. The agents therefore discovered the identity independently.

Limitations. The Station’s success in dimension eleven did not extend to new records in nearby dimensions.
We spawned two separate Stations targeting d = 12 and d = 13, which achieved valid configurations of
sizes 840 and 1154, respectively. The dimension-twelve result falls one point below the current 841-point
frontier [38, 39], while the dimension-thirteen result matches the 1154-point construction of Zinoviev and
Ericson [39, 40].

Discussion. We observe that Station agents generally favor theoretically guided strategies over large-scale
heuristic search. In this problem, they proved that further search within the classical D11 construction could
not exceed 582, then redirected later work toward extending another core, ultimately leading to the 604-point
configuration. By contrast, AlphaEvolve’s 593-point construction consists of large unequal-norm integer
coordinates that do not appear to reveal a comparably compact algebraic description or readily identifiable
organizing structure. This theory-guided bias is not necessarily always an advantage: in dimension twelve,
the Station stopped at 840, while the current 841-point frontier was reached through large-scale numerical
optimization guided by structural insight [38, 39].
This problem also shows that theorems produced by the Station may be of independent interest to researchers.
For instance, Equation (3), derived independently by the agents, overlaps with a theorem in a paper made
publicly available only recently [37]. The explicit algebraic construction may also be of independent interest.
These discoveries lie outside score optimization and show that the additional freedom given to Station agents
can yield contributions beyond improved benchmark scores.

6.4   Discretized Kakeya needle

The classical Kakeya needle problem asks how little area is needed to turn a unit line segment through every
direction. A finite version replaces the continuum of directions by n equally spaced ones and represents them
by n thin triangles that may slide horizontally [41]. More precisely, for real offsets x1 , . . . , xn , let
                                                   1
                                                                  
                                                                  j
                     Tj (xj ) = conv (xj , 0), xj + , 0 , xj + , 1        ,     1 ≤ j ≤ n,
                                                   n              n
and define
                                                                n
                                                                [
                                        CT (n) =      inf             Tj (xj ) .
                                                   x1 ,...,xn
                                                                j=1

Córdoba’s lower bound and a Schoenberg construction analyzed by Keich show that CT (n) has order
1/ log n [42, 43], but its sharp finite values have remained largely unknown. AlphaEvolve took up this
problem as Problem 6.9 of its mathematical collection; we gave the Station its triangle component at the
same seven dyadic sizes n = 2, 4, 8, 16, 32, 64, 128.

S1. New upper bounds at n = 32, 64, 128. The Station found better constructions at the three finite sizes
n = 32, 64, 128. At n = 128, it found a triangle union of area 0.107067, improving AlphaEvolve’s 0.114810
by 6.74% and the later HorizonMath value 0.109148 by 1.91% [44], and therefore proving
                                             CT (128) ≤ 0.107067.
The gains are more modest at n = 32 and n = 64, where the Station reduced AlphaEvolve’s areas by 2.15%
and 0.69%, respectively; at the smaller tested sizes n = 2, 4, 8, 16, it reached the same values as AlphaEvolve
(Figure 11).


                                                         20
                                              Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




                               0.35
                                                                        Station
union area (lower is better)
                                                                        AlphaEvolve
                                                                                                      1
                               0.30




                                                                                           height y
                               0.25


                               0.20


                               0.15

                                                                                                      0
                               0.10
                                                                                                          Best symmetric   Asymmetric construction
                                      2   4       8      16      32     64      128                          A = 7/30           A = 14/61
                                               number of triangles n

Figure 11: Left: union areas of the finite constructions published by AlphaEvolve and produced by the
Station; lower is better. The Station matches AlphaEvolve at n = 2, 4, 8, 16 and reduces the area by 2.15%,
0.69%, and 6.74% at n = 32, 64, 128, respectively. Right: the best symmetric n = 5 construction and
a smaller asymmetric construction. Blue and teal identify the triangle pairs (1, 5) and (2, 4), while gold
identifies triangle 3; the three corresponding dashed reflection axes coincide in the symmetric construction
and separate in the asymmetric one.


S2. Exact optima at n = 3, 4 and symmetry breaking at n = 5. Before this work, only the classical value
CT (2) = 1/3 was known exactly [41]. An elementary symmetric construction gives
                                                                                              5
                                                                             CT (3) ≤           ,
                                                                                             18
while Schoenberg’s classical Perron construction [45] gives
                                                                                               1
                                                                             CT (4) ≤            .
                                                                                               4
AlphaEvolve later reproduced the n = 4 value numerically. The Station proved the matching lower bounds
and therefore established
                                                5              1
                                      CT (3) =    ,   CT (4) = .
                                               18              4
It also showed that both minima admit reflection-symmetric configurations and that the n = 4 optimum
contains the continuous family
                                     1 1                  1       1
                                                 
                                       , − c, c, 0 ,        ≤c≤ .
                                     4 4                 20       8
The Station then proved that the minimum among reflection-symmetric configurations at n = 5 is 7/30 and
discovered a new asymmetric construction of area 14/61 < 7/30. Figure 11 (right) compares the symmetric
minimizer with this smaller asymmetric construction. This proves that every global minimizer at n = 5 must
be asymmetric, although the exact value of CT (5) remains open.
These results lie outside the benchmark score. Among n = 3, 4, 5, only n = 4 was one of the seven tested sizes,
and the evaluator scored only the areas of explicit constructions; it neither requested nor rewarded proofs
of global lower bounds. The task statement also did not ask the agents to classify exact small-n optima
or investigate symmetry breaking. The agents developed these results through autonomous mathematical
investigation, extending their work beyond the finite construction benchmark.

Limitations. The Station optimized its constructions separately at the tested powers n = 2k , and Figure 11
compares them with AlphaEvolve’s corresponding separately optimized finite constructions. The figure
therefore compares finite constructions on both sides. Beyond these separately optimized finite constructions,
AlphaEvolve also presents a single construction valid for every n, developed through iterative expert guidance.
The Station did not use an equivalent expert-in-the-loop process, and its autonomous agents did not discover
a competitive uniform construction.


                                                                                      21
                        Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




                                                                                     curve: −P(2πx 2 )                       prescribed double roots
                                                                                                                                             ̂
                                                                                     AlphaEvolve                                   A(f)A(f) = 0.321591
                                                                              0.04
         Pre-AlphaEvolve                                           0.32831
                Literature                                                    0.00

                                                                             −0.04
             AlphaEvolve                                0.321591                                                                         ̂
                                                                                     Station double-root construction              A(f)A(f) = 0.315309
                                                                              0.02
  Optimum in double-root                    0.315305–0.315309                 0.00
        Laguerre family
                                                                             −0.02
      Announced human              0.3102                                                                                                        ̂
                                                                                     Station                                         A(f)A(f) ≤ 0.3089
                results
                                                                              0.01

                  Station        0.3089                                       0.00

                                                                             −0.01
                        0.305   0.310   0.315   0.320    0.325   0.330               0.55            0.65        0.75       0.85                     0.95
                                                                                                                 radius x
              upper bound on C (lower is better)



Figure 12: Bounds and constructions for the one-dimensional sign uncertainty problem. Left: successive
upper bounds on CSU ; lower is better. Right: the polynomial factors −P (2πx2 ) for the AlphaEvolve
construction, the Station’s double-root construction, and the Station’s 0.3089 construction. The positive
Gaussian factor is omitted without changing signs or zeros. Open circles mark the prescribed double roots.


6.5   Sign uncertainty principle

The one-dimensional sign uncertainty problem asks how soon a function and its Fourier transform can both
become eventually nonnegative when both start negative at the origin. For a nonzero even integrable function
f : R → R with integrable Fourier transform, define

                                          A(f ) = inf{r > 0 : f (x) ≥ 0 whenever |x| ≥ r}.

The problem asks for the largest constant CSU such that A(f )A(fb) ≥ CSU . Bourgain, Clozel and Kahane
introduced the problem [46], and subsequent work obtained progressively stronger bounds [47, 48]. AlphaE-
volve studied it as Problem 6.11 and reported an upper bound of 0.321591 together with an unpublished
human bound of 0.3102. The Station further improved this bound to 0.3089, as summarized in Figure 12.

S1. A new upper bound of 0.3089.                   The Station agents constructed a function that yields this upper bound,
proving
                                                            0.2025 ≤ CSU ≤ 0.3089.
They take
                                                                        2
                                            fε (x) = −P (2πx2 ) − ε e−πx ,                        ε = 10−6 ,
                                                                   

                                                                                                               (−1/2)
where P is expressed in the even-index generalized Laguerre polynomials L2j       ; the proved tail margin
exceeds ε, so fε (0) < 0 while eventual nonnegativity is preserved. These basis functions are fixed by the
Fourier transform, so the choice gives fε = fbε automatically and reduces the problem to constructing one
polynomial with the required sign. Numerical search found the degree-226 polynomial shown in Figure 12;
the agents expressed its coefficients as exact rational numbers and proved that the resulting function is
nonnegative beyond the corresponding radius, fulfilling the problem’s eventual-nonnegativity requirement.

S2. The double-root Laguerre family is exhausted near 0.3153. In this task, we gave the agents the same
prescribed-double-root Laguerre setup and scoring rule used by AlphaEvolve, but no access to AlphaEvolve’s
paper or results. Under this setup, every submission is restricted to the family in which P is determined by
at most twenty prescribed positive double roots in the even-index Laguerre basis; we call this the double-root
Laguerre family. AlphaEvolve’s 0.321591 construction also belongs to this family. Let

                  CDR,20 = inf A(f )A(fb) : f belongs to the double-root Laguerre family .
                              


                                                                             22
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




The Station agents proved
                                     0.315305 < CDR,20 ≤ 0.315309 . . . .
The upper bound comes from an explicit construction, while the lower bound follows from an exact weighted-
sum obstruction on 41 tail points. Thus any construction improving the upper bound below 0.315305 must
leave the double-root Laguerre family.
This bound led the agents to search outside the restricted family, even though the official evaluator could
not score constructions beyond it. They expanded the search to Laguerre polynomials without prescribed
double roots and eventually discovered the degree-226 construction giving the 0.3089 bound. This provides
a concrete example of agents moving beyond score optimization to contribute directly to the underlying
mathematical problem, despite receiving no further guidance from the score.

6.6   Hardy–Littlewood maximal inequality

The one-dimensional centered Hardy–Littlewood problem asks for the optimal constant controlling where
centered local averages can be large. For a non-negative integrable function f : R → R, define

                                                     1
                                                           Z x+h
                                      M f (x) = sup                f (y) dy,
                                                h>0 2h      x−h

and let C0 be the least constant such that
                                                            C0
                                          |{M f > λ}| ≤        ∥f ∥1 .
                                                            λ
Melas solved the problem, proving
                                                √
                                            11 + 61
                                       C0 =         = 1.567521 . . .
                                               12
and constructing finite point-mass examples approaching this value [49, 50]. AlphaEvolve later treated the
finite problem as a benchmark, reaching 1.5080 in search mode and about 1.533 with hints from the literature.
The Station agents found a 356-point-mass construction with value 1.557069, improving AlphaEvolve’s result
but failing to recover the global optimum already discovered by Melas.

S1. Sharp constants between the centered and uncentered operators. Ramos considered the natural
non-tangential family interpolating between the centered and uncentered Hardy–Littlewood maximal op-
erators [51]. Its parameter α runs from the centered operator at α = 0 to the uncentered operator at α = 1.
Writing Cα for the sharp weak-(1, 1) constant, Ramos stated that its exact value was unknown for every
0 < α < 1, while the endpoint C1 = 2 is classical [50, 52]. While working on the task, the Station agents
solved this question for 1/3 ≤ α < 1, proving

                                                              1
                                      Cα = 2      for every     ≤ α ≤ 1.                                 (4)
                                                              3
The constants for 0 < α < 1/3 remain open. The task did not ask for this extension, and the agents were
unaware that Ramos had posed it; they pursued it to understand how the geometry of the centered problem
changes when the centering constraint is relaxed.

6.7   Ovals problem

The Ovals problem asks whether the curvature of every closed convex plane curve forces the lowest eigen-
value of an associated one-dimensional Schrödinger operator to be at least 1. For a curve γ of length 2π,
parametrized by arclength s, define

                                          d2
                                 Hγ = −       + κ(s)2 ,       C = inf λ0 (Hγ ),
                                          ds2                        γ


                                                      23
                   Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




where κ is the curvature and λ0 is the lowest eigenvalue under periodic boundary conditions. Benguria and
Loss conjectured that C = 1 and exhibited a continuous equality family containing the circle and noncircular
ovals [53–55], proving C ≤ 1, while Linde proved the global lower bound C > 0.81; numerical evaluation of
the explicit constant in his theorem gives C > 0.8246 [56]. AlphaEvolve took up this question as Problem
6.19 of its mathematical collection.

S1. Independent recovery of the Benguria–Loss equality family. AlphaEvolve recovered the circle but did
not obtain the noncircular equality ovals. The Station independently recovered a one-parameter normal
form, modulo Euclidean motions and shifts of the arclength origin, for the classical Benguria–Loss equality
family. It therefore reconstructed a larger part of the known equality structure than AlphaEvolve. This
is an independent recovery of a known result, not a new equality family. Benguria and Loss formulated
the conjecture and exhibited the equality family; Burchard and Thomas proved its local minimality, while
Bernstein and Mettler developed its projective geometry and established the name “ovals of Benguria and
Loss” [53–55]. Neither AlphaEvolve nor the Station improved the global lower bound.

6.8   Prime number theorem

The prime number theorem describes the asymptotic density of the primes. If π(x) counts the primes at
most x, it states that
                                              π(x)
                                          lim         = 1.
                                         x→∞ x/ log x

The underlying mathematical problem is therefore already solved: the ratio converges to exactly 1. AlphaE-
volve nevertheless took up a finite version as Problem 6.27 of its collection. It searched for a finitely supported
weight f satisfying
                                                 X f (k)
                                                          = 0.
                                                      k
                                                     k

The score of such a weight and its associated sum are
                                         X f (k) log k                         X           jxk
                             A(f ) = −                     ,        Ff (x) =       f (k)         .
                                                 k                                          k
                                          k                                    k

The classical Chebyshev argument shows that

                                          Ff (x) ≤ 1           for every x ≥ 1                                 (5)

implies the rigorous lower bound
                                                          π(x)
                                              lim inf             ≥ A(f )
                                              x→∞        x/ log x
 [57]. The required global inequality in Equation (5) is much more restrictive than the prime number
theorem itself: a single finite weight must satisfy the inequality for every x. AlphaEvolve’s score tested this
inequality only at finitely many sampled values. It could therefore assign a high score to a weight that fails
at an untested value, in which case the score does not prove the stated prime-counting bound. However,
an exhaustive check at all x is usually computationally prohibitive because the associated period can be
enormous. The sampled score consequently provides only a rough approximation to whether the global
inequality holds.

S1. A score of 0.980681 valid for every x.     The Station agents discovered a finite construction f satisfying
Equation (5) for every x, with
                                                 A(f ) ≥ 0.980681.                                             (6)
This improves on AlphaEvolve’s reported score of 0.938. More importantly, the agents proved the required
inequality for all x, whereas the score alone does not provide that guarantee. Their key idea was to choose
the integers in the construction so that Ff repeats after a manageable range. This reduces the infinitely


                                                               24
                   Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




many possible values of x to one finite exhaustive check, which the agents completed using exact arithmetic
in under a minute.
In contrast, other agents in the same run found constructions with higher scores, reaching 0.990629, but
these constructions did not satisfy the global inequality for every x. This provides a concrete example of
agents prioritizing the underlying mathematical problem over naive score optimization despite a hackable
score.

S2. Why a direct Möbius cutoff fails. The Möbius function is a natural starting point because it is central
to a standard formulation of the prime number theorem. AlphaEvolve explored finite constructions obtained
by truncating the Möbius function, and the Station agents initially pursued the same approach. They then
proved that this family cannot yield a positive asymptotic score: as the truncation cutoff D grows, its largest
violation of the required global inequality grows at least on the order of D/ log2 D. Consequently, rescaling
the construction to satisfy the inequality forces its score down to O(log2 D/D), which tends to zero. The
proof builds on results about incomplete Möbius sums [58]. This obstruction led the agents to abandon
direct Möbius cutoffs and explore a more flexible construction with jointly optimized coefficients, producing
the rigorous score of 0.980681 described above.

Limitation. Since the prime number theorem already determines the limiting ratio above exactly, these
results do not change what is known about prime distribution. Their mathematical contribution is narrower:
within the finite setting of the benchmark, the Station agents found a construction with a rigorous score of
0.980681 and proved that the natural Möbius cutoff cannot yield a positive asymptotic score. The problem
therefore serves primarily as a calibration of whether agents can distinguish a valid mathematical result from
a high but hackable score, rather than as a material contribution to the study of prime distribution.

6.9   Difference bases

A finite set B ⊂ Z is a difference basis for {1, . . . , n} if every integer in that interval is a difference of two
elements of B. If ∆(n) is the smallest possible size of such a set, the quantity to minimize is ∆(n)2 /n;
Rédei and Rényi proved that these normalized minima converge and that their limit is their infimum [59].
AlphaEvolve reported the upper bound
                                               ∆(n)2    3602
                                     C := inf        ≤       ≈ 2.639027
                                           n≥1   n     49109
as Problem 6.7 of its collection. The preceding published upper bound was Golay’s C ≤ 2.6458 . . . [60, 61],
rather than the 2.6571 . . . benchmark used in AlphaEvolve’s comparison. This example was found with the
help of a human expert hint: the paper records that AlphaEvolve failed to improve its benchmark until it
was supplied with correct code for generating Singer difference sets, and its released prompt also directs the
search to Singer sets and the classical Leech product construction. We gave the Station only the problem
definition, the scoring rule, and a trivial grid baseline. In particular, the agents had neither these construction
hints nor access to the external literature.

S1. Independent recovery of a record in the Leech–Golay family. Leech and Golay combined the four-
point difference basis {0, 1, 4, 6} with Singer difference sets to obtain earlier members of this construction
family [60, 62, 63]. The Station independently recovered its q = 89 member. Taking v = q 2 + q + 1 = 8011,
a 90-element Singer difference set D ⊂ Zv , and A = {0, 1, 4, 6}, the agents formed
                                         B = {va + d : a ∈ A, d ∈ D}.
With the appropriate representatives for D, the resulting 360 integers realize every difference from 1 through
49109, while 49110 is the first missing difference. Thus
                                               3602
                                        C≤          = 2.6390274695 . . . ,
                                              49109
improving Golay’s preceding bound by approximately 0.0067. The set agrees entry for entry with the
construction reported by AlphaEvolve. This is an independent recovery of a known record, not a new upper


                                                        25
                   Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




bound relative to AlphaEvolve or a new construction family. The agents also tried to push the lower bound
further, but reached only the classical bound C ≥ 2.434467 . . . [62], whereas Yang and Liao proved the
stronger published bound C > 2.4421 [64].

6.10   Sidorenko’s conjecture

Sidorenko’s conjecture asserts that every bipartite graph H satisfies t(H, W ) ≥ t(K2 , W )|E(H)| for every
graphon W , where t(H, W ) is the homomorphism density of H in W [65]. The smallest unresolved instance
is the ten-vertex, fifteen-edge graph H = K5,5 \C10 , also called the bipartite Möbius ladder [66]. AlphaEvolve
took up this problem as Problem 6.26 of its mathematical collection and searched over nonconstant 30-step
graphons. It scored a candidate by
                                               t(K2 , W )15
                                                             − 1,
                                                 t(H, W )
so a positive value would give a counterexample and disprove this instance of the conjecture.
AlphaEvolve reported that it did not find a counterexample. We gave the Station the same problem and
scoring rule, and the Station agents likewise found none. As such, the status of the conjecture is unchanged.

6.11   Peak autoconvolution

AlphaEvolve’s Problem 6.2, called the first autocorrelation inequality in its collection, asks how evenly the
sum of two independent random variables with the same compactly supported density can       R be distributed.
More precisely, for a nonnegative function f supported on [−1/4, 1/4] and normalized by f = 1, let

                                              C6.2 = inf ∥f ∗ f ∥∞ .
                                                        f

Determining C6.2 is connected to the asymptotic size of generalized Sidon sets, and its exact value remains
unknown [67]. The best currently reported bounds are

                                           1.2937 ≤ C6.2 ≤ 1.502851,

with the lower and upper endpoints coming from certified convex relaxations and an explicit step function,
respectively [33, 68].
AlphaEvolve achieved the upper bound C6.2 ≤ 1.5032, improving the pre-AlphaEvolve bound C6.2 ≤ 1.50972
of Matolcsi and Vinuesa [67]; TTT-Discover later advanced the frontier to C6.2 ≤ 1.502863 [69], and an exact-
arithmetic certificate improved it further to C6.2 ≤ 1.502851 [68]. The Station reached only C6.2 ≤ 1.504473,
worse than both AlphaEvolve and the current frontier. AlphaEvolve’s highly irregular construction emerged
from large-scale heuristic search. This contrast highlights a limitation of the Station: its agents generally
favored theory-guided constructions over heuristic search, a preference that produced strong results on
several other problems but left them behind here, where frontier constructions depend on extensive heuristic
optimization.

6.12   Flat autoconvolution

AlphaEvolve’s Problem 6.3, called the second autocorrelation inequality in its collection, asks how closely the
autoconvolution of a nonnegative function can resemble a flat-topped function, constant on a set and zero
outside it. More precisely, for a nonzero nonnegative function f ∈ L1 (R) ∩ L2 (R), let

                                             ∥f ∗ f ∥22
                              Q(f ) =                       ,    C6.3 = sup Q(f ).
                                        ∥f ∗ f ∥1 ∥f ∗ f ∥∞              f

Hölder’s inequality gives C6.3 ≤ 1; for an arbitrary nonnegative output, equality occurs only for such a
flat-topped function. Whether the autoconvolution constraint forces the strict inequality C6.3 < 1 remains
open [67, 70]. Before AlphaEvolve, the best known bounds were [67]

                                              0.88922 ≤ C6.3 ≤ 1.


                                                        26
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




AlphaEvolve established the lower bound C6.3 ≥ 0.961021, while later work further improved this to
0.962694 [32]. The Station’s best verified construction reached only C6.3 > 0.953189 and therefore did
not improve the numerical bound. This shortfall reflects the same limitation seen in Problem 6.2, minimiz-
ing the peak of an autoconvolution (Section 6.11): the Station’s theory-guided agents were poorly suited to
finding the highly irregular constructions produced by large-scale heuristic search.

S1. Binary step functions preserve the unrestricted supremum. The agents nevertheless proved a useful
fact about the search for near-optimal constructions: the supremum defining C6.3 can be approached using
binary step functions, thus replacing the search over arbitrary nonnegative functions with a search over
binary functions on increasingly fine grids.

6.13   Book Ramsey numbers

Given graphs G1 , G2 , the Ramsey number R(G1 , G2 ) is the smallest n such that every red-blue edge coloring
of Kn forces either a red copy of G1 or a blue copy of G2 . Establishing the exact values of Ramsey numbers
is a difficult computational and theoretical challenge. The most famous Ramsey numbers are those where
G1 and G2 are complete graphs, but many other choices have been studied extensively (see the survey [71]).
The book graph Bk consists of k triangles that share a common edge. An open problem is whether

                                           R(Bn−1 , Bn ) = 4n − 1                                         (7)

holds for every positive integer n. Rousseau and Sheehan established the upper bound in 1978, proving
R(Bn−1 , Bn ) ≤ 4n − 1 for all n [72]. It therefore remains to prove the matching lower bound. For a given
n, this amounts to constructing a red–blue edge coloring of K4n−2 containing neither a red Bn−1 nor a blue
Bn .
The third author proved equality for n ≤ 20, independently matching contemporaneous work, and established
an infinite Paley-type family whenever 2n − 1 is a prime power congruent to 1 (mod 4) [25, 73]. This
combination of finite evidence and a general arithmetic construction led him to conjecture that (7) holds
for all n [25]. Epoch AI subsequently adopted it as a FrontierMath open problem [74]. After its posting,
further work extended the consecutively solved range to n ≤ 56 and produced two additional infinite families
by extending established constructions [75].
We ran two Stations on this problem. The first operated without internet access and discovered a novel
conference-graph family. We then ran a second Station with a summary of the first Station’s results, using
GPT-5.6 Sol to discover a new doubled Legendre family. We subsequently enabled internet access in this
second Station, which produced several new finite constructions. An external expert subsequently combined
the pattern in these finite constructions with an earlier result from the second Station to obtain the Yamada–
Pott infinite family. Thus, the first two families are autonomous Station discoveries, whereas the third
required human expert involvement. All three families are novel relative to the existing literature and are
visualized in Figure 13. The parameters n covered by each family, including which were previously open, are
summarized in Figure 14.

S1. A conference-graph family. The first and broadest family converts any conference graph into a sharp
book Ramsey coloring. Specifically, if a strongly regular graph with parameters

                                               q−1 q−5 q−1
                                                                
                                            q,      ,      ,
                                                2      4      4

exists, then the Station’s agents proved

                                           R(Bq , Bq+1 ) = 4q + 3.                                        (8)

Paley conference graphs exist whenever q is a prime power congruent to 1 (mod 4). Consequently, the
theorem proves the conjecture whenever n − 1 is a prime power congruent to 1 (mod 4). Beyond the Paley
case, Seberry and Whiteman used Mathon’s construction to obtain symmetric conference matrices of order


                                                     27
                        Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




     BB          BR        RB         RR     uv         0+          0−         1+        1−     uv              F1                             F2


BB                                                0+


                                                                                                     F1
BR                                                0−




RB                                                1+



                                                                                                     F2
RR                                                1−


 u                                                 u
 v                                                 v

     (a) Conference family (n = 6)                 (b) Doubled Legendre family (n = 6)                    (c) Yamada–Pott family (n = 11)
            4 chambers: BB, BR, RB, RR                          4 layers: 0+, 0−, 1+, 1−                             2 affine fibres: F1, F2
          5 vertices each; endpoints: u, v                   5 vertices each; endpoints: u, v                          21 vertices each

                                                  red edge         blue edge         diagonal (no edge)


Figure 13: Block-ordered adjacency matrices for the smallest nontrivial members of the three infinite families.
Red and blue off-diagonal cells encode the edge colors, and white lines separate the construction blocks named
on the axes. The conference and doubled Legendre examples color K22 for n = 6, with no red B5 and no
blue B6 . The Yamada–Pott example colors K42 for n = 11, with no red B10 and no blue B11 .


5 · 92t+1 + 1 for every t ≥ 0 [76, 77]. These yield conference graphs of order q = 5 · 92t+1 , so the Station
theorem also proves the conjecture whenever

                                                       n = 5 · 92t+1 + 1,             t ≥ 0.

The first member gives q = 45 and n = 46. The known conference graph of order q = 65 supplies the
additional parameter n = 66 [78]. In total, known conference graphs prove the conjecture at 30 values of
n ≤ 200, including 19 that were previously open [25, 73–75].

S2. A doubled Legendre family. The second family converts a periodic Legendre source over FQ into a sharp
book Ramsey coloring [79]. Specifically, for every prime power Q > 3 with Q ≡ 3 (mod 8), the Station’s
agents proved
                                    R B(Q−1)/2 , B(Q+1)/2 = 2Q + 1.                                    (9)
                                                          

Consequently, the theorem proves the conjecture whenever 2n − 1 is a prime power congruent to 3 (mod 8).
For n ≤ 200, this family proves equality at 21 values and, at the time of its discovery, resolved six additional
open cases after accounting for the conference family [25, 73–75].
The agents discovered this general family in mid-July 2026. Concurrent work announced at the end of July
independently produced the finite case n = 70 [74]; the Station theorem contains n = 70 as one member and
covers infinitely many further parameters.
The doubled Legendre family is related to, but distinct from, the Legendre family reported by Turturean [75].
Both begin with the same type of periodic Legendre source over FQ , with Q ≡ 3 (mod 8), but use different
lifts to obtain a book Ramsey coloring. For the same source order Q, the earlier lift reaches n = (Q + 1)/4,
whereas the Station lift reaches n = (Q + 1)/2. It therefore doubles the Ramsey parameter and covers a
different set of values, as Figure 14 shows.

S3. A Yamada–Pott family. The third family converts a classical Yamada–Pott design into a sharp book
Ramsey coloring [80]. Specifically, for every prime power q ≥ 7 with q ≡ 3 (mod 4), we proved

                                             R B(q2 −q−2)/4 , B(q2 −q+2)/4 = q 2 − q + 1.                                                           (10)
                                                                          


                                                                         28
                           Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




         Finite examples

           Paley family
          Wesley (2026)
         Legendre family
        Turturean (2026)


       Conference family
          Station (2026)
Doubled Legendre family
          Station (2026)
     Yamada–Pott family
         Station (2026)

                           1       20       40          60          80          100      120        140        160       180   200
                                                                    Ramsey parameter n

                                                 Already solved in previous literature         Newly solved by Station

Figure 14: Coverage of the Book Ramsey Numbers conjecture for 1 ≤ n ≤ 200. The top three rows
summarize existing results [25, 73, 75], and the bottom three summarize the Station results. Together, the
Station families prove the conjecture at 43 distinct values in this range and resolve 28 cases that were open
when the Station discoveries were made.


Consequently, the theorem proves the conjecture whenever

                                                                  q2 − q + 2
                                                             n=
                                                                      4
for a prime power q ≥ 7 congruent to 3 (mod 4). For n ≤ 200, this family proves equality at five values and
resolves three additional previously open cases after accounting for the conference and doubled Legendre
families [25, 73–75]. The second Station’s agents supplied finite affine constructions for n = 11, 28, 86 and
an earlier periodic-correlation identity; an external expert recognized their shared Yamada–Pott structure
and used these ingredients to establish the general theorem.

Discussion. The three infinite families above are novel relative to the existing literature, but their source
objects are not: conference graphs, periodic Legendre pairs, and Yamada–Pott designs were all established
previously [76, 79, 80]. What is new in each case is the rule that lifts the classical object to a sharp book
Ramsey coloring, and such a rule need not be apparent from the source alone. For example, the agents
discovered the general conference-graph lift only after more than 3,000 Station ticks and a long sequence of
intermediate internal papers. The accompanying notebook provides the relatively unpolished proofs adapted
from the agents’ internal papers; we will present polished proofs of all three families in a separate follow-up
paper.
The first two families also show that Station agents can advance a general mathematical objective beyond
the directly scorable task: they discovered and proved infinite families even though the evaluator could
reward only finite constructions. The third family illustrates a complementary limitation. Both the finite
affine examples and the periodic-correlation identity needed for the general theorem were already present
in the Station’s research history, but the agents did not connect them. An external expert recognized their
shared Yamada–Pott structure and completed the synthesis. This missed connection indicates that agents
may not yet capitalize fully on knowledge accumulated across the Station and may benefit from external
expert synthesis in such cases.

6.14     Jacobian Conjecture

The Jacobian conjecture asked whether a polynomial map that is locally invertible everywhere must also
be globally invertible. More precisely, it asserted that every polynomial map F : Cn → Cn with nonzero
constant Jacobian determinant is a polynomial automorphism [81]. On 19 July 2026, it was announced
that a three-dimensional counterexample had been produced with Claude Fable [3], thereby disproving
the conjecture in every dimension at least three. The breakthrough then prompted researchers to seek a


                                                                    29
                     Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




conceptual explanation for the map: in particular, why its apparently miraculous Jacobian cancellation
occurs and how three generic inverse sheets can coexist with local invertibility everywhere [82–86].
We launched the Station one week after the announcement. Because this experiment was conducted after
newer models had become available, it used a more recent agent pool than the other Stations: two agents
each powered by GPT-5.6 Sol, Claude Opus 5, and Gemini 3.1 Pro. The agents had no external web access
and received only a formula-free specification: construct a rational-coefficient polynomial map C3 → C3 of
degree at most 12 with nonzero constant Jacobian determinant and two distinct rational points in one fiber.
The evaluator automatically checked each construction and assigned a score of 1 only if it satisfied every
requirement, and 0 otherwise. We supplied no literature survey or partial construction. The agents therefore
had to find the counterexample independently.
The goal of this task was twofold. First, we wanted to test the Station on a strictly binary problem. The
evaluator supplied neither partial credit nor graded feedback, so unsuccessful attempts gave the agents no
score signal about how to improve; attaining a score of 1 required reconstructing a counterexample to a
conjecture that had resisted mathematicians for nearly nine decades [81]. Second, we wanted to observe
the complete discovery process rather than only the final construction. We make the entire raw agent
dialogue public, whereas the original Fable discovery trajectory has not been released. This record preserves
intermediate mathematical ideas that do not appear in the final construction and allows researchers to study
the dynamics of AI-led mathematical discovery.

S1. Independent reconstruction through a cuspidal ruling.           Writing b = xy − 1, a Station agent constructed
the degree-seven map

                    F (x, y, z) = 6x + 9x2 y, y(9b2 + 6b − 2), 3y 2 b(3b − 1) + z x3 , xb2 , b3 .
                                                                                              

Exact calculation gives det JF = −6, and the three distinct rational points
                           6 7 4753              3 7 980               3 7 2548
                                                                           
                         − ,− ,−          ,        , ,−        ,         , ,
                           7 6     216           4 3     27            28 3 27
all map to (1, 7/3, 0). These identities constitute a complete counterexample certificate. The formula differs
visibly from the announced map H [3, 87], but the linear source and target transformations T (x, y, z) =
(x, −y, −3z) and L(A, B, C) = (3C, −B, 3A) satisfy F ◦ T = L ◦ H. The Station therefore reconstructed the
announced counterexample in different linear coordinates; it did not produce a new counterexample or a new
equivalence class.
Whereas the original result was credited to Claude Fable, the counterexample was independently discovered
within one day by a single GPT-5.6 Sol agent, without direct interaction with the other agents. The successful
agent began with ruled maps F (x, y, z) = f (x, y) + z n(x, y), so that varying z traces a line for each fixed
(x, y). It tested five low-degree direction templates based on smooth conics, but none satisfied the remaining
constant-Jacobian condition. The decisive step was to replace the smooth direction curve with the cuspidal
cubic [r : s] 7→ [r3 : rs2 : s3 ]. Its associated direction field is n = (x3 , x(xy − 1)2 , (xy − 1)3 ); with this choice,
the compatibility equations for the base surface f became solvable and yielded exactly the map above.

S2. The reconstructed map has three-sheeted fibers without critical points. During the successful deriva-
tion, the agent also explained why the cuspidal ruling makes the Jacobian constant. For the direction
field n = (x3 , x(xy − 1)2 , (xy − 1)3 ), the agent derived moving-frame identities, including D(n) = 3xn for
D = x2 ∂x − ∂y , under which every z-dependent contribution to the determinant contains a repeated tan-
gent direction and vanishes. The remaining triple product is the constant −6. The agent thus derived the
Jacobian cancellation from the geometry of the cuspidal ruling rather than discovering sixteen terms whose
cancellation could only be checked afterward.
After constructing the counterexample, the same agent analyzed its fibers and explained how the map can
be locally invertible everywhere while generically having three preimages. On a dense chart, write a target
as (X, Y, Z) and set I = XY and J = X 2 Z. Recovering a preimage then reduces to

                                               t3 + 6t2 − 3It + 2J = 0.                                              (11)


                                                           30
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




For a generic target, the three roots give three distinct preimages. If p(t) denotes the left-hand side, the
inverse formulas satisfy A = p′ (t)/6, X = xA, and hence x = X/A. When roots coalesce and X ̸= 0, the
condition p′ (t) = 0 forces the corresponding source point to escape to infinity rather than become a critical
point in affine space. Over the exceptional locus X = 0, the source coordinate x supplies an additional affine
scale direction that resolves the same apparent ramification. This analysis answers the structural question
raised by mathematicians immediately after the announcement: the three sheets arise from a cubic quotient,
while the geometry of the full three-dimensional map prevents their collisions from producing critical points.
The agent’s explanation coincides with the cuspidal and cubic account developed by mathematicians in the
days following the announcement [83–86].

Discussion. The mathematical outcome of this experiment is an independent reconstruction, not a new
counterexample or a new explanation. The example indicates that the Station can tackle a difficult binary
problem whose evaluator provides no gradient or partial score to guide the search. Counterexample break-
throughs of this kind may nevertheless be rare because conjectures are generally expected to be true. In
a broader context, the harder challenge may therefore be identifying a promising problem and investing
substantial computation before knowing whether a counterexample exists.




                                                     31
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




References
 [1] Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Emilien Dupont, Po-Sen Huang, Adam Zsolt Wagner,
     Sergey Shirobokov, Borislav Kozlovskii, Francisco J. R. Ruiz, Abbas Mehrabian, M. Pawan Kumar,
     Abigail See, Swarat Chaudhuri, George Holland, Alex Davies, Sebastian Nowozin, Pushmeet Kohli, and
     Matej Balog. AlphaEvolve: A coding agent for scientific and algorithmic discovery. arXiv preprint
     arXiv:2506.13131, 2025. doi: 10.48550/arXiv.2506.13131. URL https://arxiv.org/abs/2506.13131.
 [2] OpenAI. Ten advances in mathematics and theoretical computer science. OpenAI, August 2026. URL
     https://openai.com/index/ten-advances-in-mathematics/.
 [3] Levent Alpöge. Hello there the Jacobian conjecture is false. X post, July 2026. URL https://x.com/
     __alpoge__/status/2079028340955197566. Posted 19 July 2026.
 [4] Emiel Lorist and Felix L. Schwenninger. A solution to Crouzeix’s conjecture. arXiv preprint
     arXiv:2608.03841, 2026. doi: 10.48550/arXiv.2608.03841. URL https://arxiv.org/abs/2608.03841.
 [5] Lech Mazur. A computer-assisted proof of Sendov’s conjecture. Proof Atlas, August 2026. URL https://
     www.proofatlas.ai/papers/sendov-conjecture/SENDOV_CONJECTURE_PROOF_AUGUST_5_2026.pdf.
 [6] Stephen Chung and Wenyu Du. The station: An open-world environment for ai-driven discovery, 2025.
     URL https://arxiv.org/abs/2511.06309.
 [7] Terence Tao. Mathematics in the age of AI. arXiv preprint arXiv:2608.16753, 2026. doi: 10.48550/
     arXiv.2608.16753. URL https://arxiv.org/abs/2608.16753.
 [8] Leiden Declaration Working Group. Leiden declaration on artificial intelligence and mathematics, June
     2026. URL https://leidendeclaration.ai/.
 [9] OpenAI.    Introducing GPT-5.5.         OpenAI, April 2026.         URL https://openai.com/index/
     introducing-gpt-5-5/.
[10] Anthropic. Claude opus 4.8.       Anthropic, May 2026.       URL https://www.anthropic.com/news/
     claude-opus-4-8.
[11] Google. Introducing Gemini 3.1 Pro: A smarter model for your most complex tasks. Google blog, Febru-
     ary 2026. URL https://blog.google/innovation-and-ai/models-and-research/gemini-models/
     gemini-3-1-pro/.
[12] Alireza Ghafarollahi and Markus J. Buehler. SciAgents: Automating scientific discovery through
     bioinspired multi-agent intelligent graph reasoning. Advanced Materials, 37(22):2413523, 2025. doi:
     10.1002/adma.202413523. URL https://doi.org/10.1002/adma.202413523.
[13] Chenglei Si, Diyi Yang, and Tatsunori Hashimoto. Can LLMs Generate Novel Research Ideas? A
     Large-Scale Human Study with 100+ NLP Researchers. arXiv preprint arXiv:2409.04109, 2024. doi:
     10.48550/arXiv.2409.04109. URL https://arxiv.org/abs/2409.04109.
[14] Haoyang Liu, Yijiang Li, and Haohan Wang. GenoMAS: A Multi-Agent Framework for Scientific
     Discovery via Code-Driven Gene Expression Analysis. arXiv preprint arXiv:2507.21035, 2025. doi:
     10.48550/arXiv.2507.21035. URL https://arxiv.org/abs/2507.21035.
[15] Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize Chen,
     Yusheng Su, Xin Cong, Juyuan Xu, Dahai Li, Zhiyuan Liu, and Maosong Sun. ChatDev: Communica-
     tive agents for software development. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors,
     Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1:
     Long Papers), pages 15174–15186, Bangkok, Thailand, August 2024. Association for Computational Lin-
     guistics. doi: 10.18653/v1/2024.acl-long.810. URL https://aclanthology.org/2024.acl-long.810/.
[16] Asankhaya Sharma. OpenEvolve: An open-source evolutionary coding agent. GitHub repository, 2025.
     URL https://github.com/algorithmicsuperintelligence/openevolve.


                                                     32
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




[17] Robert Tjarko Lange, Yuki Imajuku, and Edoardo Cetin. ShinkaEvolve: Towards Open-Ended And
     Sample-Efficient Program Evolution. arXiv preprint arXiv:2509.19349, 2025. doi: 10.48550/arXiv.2509.
     19349. URL https://arxiv.org/abs/2509.19349.

[18] Gang Liu, Yihan Zhu, Jie Chen, and Meng Jiang. Scientific Algorithm Discovery by Augmenting
     AlphaEvolve with Deep Research. arXiv preprint arXiv:2510.06056, 2025. doi: 10.48550/arXiv.2510.
     06056. URL https://arxiv.org/abs/2510.06056.

[19] Chris Lu, Cong Lu, Robert Tjarko Lange, Yutaro Yamada, Shengran Hu, Jakob Foerster, David Ha,
     and Jeff Clune. Towards end-to-end automation of AI research. Nature, 651:914–919, 2026. doi:
     10.1038/s41586-026-10265-5. URL https://doi.org/10.1038/s41586-026-10265-5.

[20] Samuel Schmidgall, Yusheng Su, Ze Wang, Ximeng Sun, Jialian Wu, Xiaodong Yu, Jiang Liu, Michael
     Moor, Zicheng Liu, and Emad Barsoum. Agent laboratory: Using LLM agents as research assistants.
     In Findings of the Association for Computational Linguistics: EMNLP 2025, pages 5977–6043, Suzhou,
     China, 2025. Association for Computational Linguistics. doi: 10.18653/v1/2025.findings-emnlp.320.
     URL https://aclanthology.org/2025.findings-emnlp.320/.

[21] OpenAI.     Multi-agent, 2026.      URL https://developers.openai.com/api/docs/guides/
     responses-multi-agent. Accessed: 2026-08-14.

[22] OpenAI. Prompt used for “a proof of the cycle double cover conjecture”. URL https://cdn.openai.
     com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_prompt.pdf. Accessed: 2026-09-10.

[23] Ludovico Mitchener, Angela Yiu, Benjamin Chang, Mathieu Bourdenx, Tyler Nadolski, Arvis Sulovari,
     Eric C. Landsness, Daniel L. Barabasi, Siddharth Narayanan, Nicky Evans, Shriya Reddy, Martha
     Foiani, Aizad Kamal, Leah P. Shriver, Fang Cao, Asmamaw T. Wassie, Jon M. Laurent, Edwin Melville-
     Green, Mayk Caldas, Albert Bou, Kaleigh F. Roberts, Sladjana Zagorac, Timothy C. Orr, Miranda E.
     Orr, Kevin J. Zwezdaryk, Ali E. Ghareeb, Laurie McCoy, Bruna Gomes, Euan A. Ashley, Karen E.
     Duff, Tonio Buonassisi, Tom Rainforth, Randall J. Bateman, Michael Skarlinski, Samuel G. Rodriques,
     Michaela M. Hinks, and Andrew D. White. Kosmos: An AI Scientist for Autonomous Discovery. arXiv
     preprint arXiv:2511.02824, 2025. doi: 10.48550/arXiv.2511.02824. URL https://arxiv.org/abs/
     2511.02824.

[24] Bogdan Georgiev, Javier Gómez-Serrano, Terence Tao, and Adam Zsolt Wagner. Mathematical explo-
     ration and discovery at scale. arXiv preprint arXiv:2511.02864, 2025. doi: 10.48550/arXiv.2511.02864.
     URL https://arxiv.org/abs/2511.02864.

[25] William J. Wesley. Lower bounds for book Ramsey numbers. Discrete Mathematics, 349:114913, 2026.
     doi: 10.1016/j.disc.2025.114913. arXiv:2410.03625.

[26] Zeev Dvir. On the size of kakeya sets in finite fields. Journal of the American Mathematical Society, 22
     (4):1093–1097, 2009. doi: 10.1090/S0894-0347-08-00607-3.

[27] Boris Bukh and Ting-Wei Chao. Sharp density bounds on the finite field kakeya problem. Discrete
     Analysis, 2021. doi: 10.19086/da.30707. Article 26, 9 pp.; arXiv:2108.00074.

[28] Vsevolod F. Lev. Comment 994 on “DHJ3: 900–999 (density Hales–Jewett type numbers)”. Blog
     comment, What’s new (T. Tao), March 2009. https://terrytao.wordpress.com/2009/03/04/
     dhj3-900-999-density-hales-jewett-type-numbers/comment-page-3/#comment-36694, accessed
     30 July 2026.

[29] Paul Erdős. Some remarks on number theory. Riveon Lematematika, 9:45–48, 1955. In Hebrew.

[30] Jan Kristian Haugland. The minimum overlap problem revisited. arXiv preprint arXiv:1609.08000,
     2016. doi: 10.48550/arXiv.1609.08000.

[31] Ethan Patrick White. A new bound for Erdős’ minimum overlap problem. Acta Arithmetica, 208(3):
     235–255, 2023. doi: 10.4064/aa220728-7-6.


                                                     33
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




[32] Haotian Ye, Haowei Lin, Jingyi Tang, Yizhen Luo, Rahul Thapa, Caiyin Yang, Chang Su, Rui Yang,
     Ruihua Liu, Rundao Li, Zeyu Li, Pengwei Sun, Chong Gao, Dachao Ding, Guangrong He, Miaolei
     Zhang, Lina Sun, Wenyang Wang, Yuchen Zhong, Zhuohao Shen, Puheng Li, Pan Lu, Bianxiao Cui,
     Di He, Jianzhu Ma, Junfeng Li, Hexi Baoyin, Yejin Choi, Stefano Ermon, Xiaowen Chu, Tongyang Li,
     Yuzhi Xu, and James Zou. Structured scaling of AI discovery across diverse scientific domains. arXiv
     preprint arXiv:2604.19341, 2026. doi: 10.48550/arXiv.2604.19341.

[33] Sungyoon Kim and Mert Pilanci. AI-assisted discovery of convex relaxations via dual agents. arXiv
     preprint arXiv:2606.31182, 2026. doi: 10.48550/arXiv.2606.31182.

[34] Mikhail Ganzhinov. Highly symmetric lines. Linear Algebra and its Applications, 722:12–37, 2025. doi:
     10.1016/j.laa.2025.05.002. arXiv:2207.08266.

[35] Federico Bianchi, Yongchan Kwon, Aneesh Pappu, and James Zou. Harnessing the collective intelligence
     of AI agents in the wild for new discoveries. arXiv preprint arXiv:2606.10402, 2026. doi: 10.48550/
     arXiv.2606.10402.

[36] Marc R. Best. a(11, 4, 4) = 35, or some new optimal constant-weight codes. Technical Report ZN 71/77,
     Mathematical Centre, Amsterdam, 1977. URL https://ir.cwi.nl/pub/7433.

[37] Rustem Takhanov and Stanislav Yun. Classification of independent sets in signed Johnson graphs and
     applications to kissing arrangements. arXiv preprint arXiv:2606.03299, 2026. doi: 10.48550/arXiv.2606.
     03299.

[38] Rustem Takhanov, Zhenisbek Assylbekov, and Stanislav Yun. Structure of kissing arrangements in ∖12
     and a place for the 841st sphere. arXiv preprint arXiv:2606.18984, 2026. doi: 10.48550/arXiv.2606.
     18984.

[39] Henry Cohn. Kissing numbers. Online table, 2026. https://cohn.mit.edu/kissing-numbers/, ac-
     cessed 4 August 2026.

[40] Victor A. Zinoviev and Thomas Ericson. New lower bounds for contact numbers in small dimen-
     sions. Problems of Information Transmission, 35(4):287–294, 1999. URL https://www.mathnet.ru/
     eng/ppi457.

[41] Kenneth J. Falconer. The Geometry of Fractal Sets, volume 85 of Cambridge Tracts in Mathematics.
     Cambridge University Press, 1985.

[42] Antonio Córdoba. The kakeya maximal function and the spherical summation multipliers. American
     Journal of Mathematics, 99(1):1–22, 1977. doi: 10.2307/2374006.

[43] Uriel Keich. On Lp bounds for kakeya maximal functions and the minkowski dimension in R2 . Bulletin
     of the London Mathematical Society, 31(2):213–221, 1999. doi: 10.1112/S0024609398005372.

[44] Erik Y. Wang, Sumeet R. Motwani, James V. Roggeveen, Eliot Hodges, Dulhan Jayalath, Charles
     London, Kalyan Ramakrishnan, Jakob Foerster, Cheng Zhang, Flaviu Cipcigan, Philip Torr, and
     Alessandro Abate. Measuring progress in reasoning toward mathematical discovery with automatic
     verification. arXiv preprint arXiv:2603.15617, 2026. doi: 10.48550/arXiv.2603.15617. URL https:
     //arxiv.org/abs/2603.15617.

[45] I. J. Schoenberg. On certain minima related to the Besicovitch–Kakeya problem. Mathematica (Cluj),
     4:145–148, 1962.

[46] Jean Bourgain, Laurent Clozel, and Jean-Pierre Kahane. Principe d’Heisenberg et fonctions positives.
     Annales de l’Institut Fourier, 60(4):1215–1232, 2010. doi: 10.5802/aif.2552.

[47] Felipe Gonçalves, Diogo Oliveira e Silva, and Stefan Steinerberger. Hermite polynomials, linear flows
     on the torus, and an uncertainty principle for roots. Journal of Mathematical Analysis and Applications,
     451(2):678–711, 2017. doi: 10.1016/j.jmaa.2017.02.030.


                                                     34
                   Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




[48] Henry Cohn and Felipe Gonçalves. An optimal uncertainty principle in twelve dimensions via
     modular forms. Inventiones Mathematicae, 217:799–831, 2019. doi: 10.1007/s00222-019-00875-4.
     arXiv:1712.04438.

[49] Antonios D. Melas. On the centered Hardy–Littlewood maximal operator. Transactions of the American
     Mathematical Society, 354:3263–3273, 2002. doi: 10.1090/S0002-9947-02-02900-8.

[50] Antonios D. Melas. The best constant for the centered Hardy–Littlewood maximal inequality. Annals
     of Mathematics, 157(2):647–688, 2003. doi: 10.4007/annals.2003.157.647.

[51] João P. G. Ramos. Sharp total variation results for maximal functions. Annales Academiae Scientiarum
     Fennicae Mathematica, 44(1):41–64, 2019. doi: 10.5186/aasfm.2019.4409.

[52] Antonio Bernal. A note on the one-dimensional maximal function. Proceedings of the Royal Society of
     Edinburgh Section A: Mathematics, 111(3–4):325–328, 1989. doi: 10.1017/S030821050001859X.

[53] Rafael D. Benguria and Michael Loss. Connection between the Lieb–Thirring conjecture for Schrödinger
     operators and an isoperimetric problem for ovals on the plane. In Partial Differential Equations and
     Inverse Problems, volume 362 of Contemporary Mathematics, pages 53–61. American Mathematical
     Society, 2004. arXiv:math-ph/0402048.

[54] Almut Burchard and Lawrence E. Thomas. On an isoperimetric inequality for a Schrödinger operator
     depending on the curvature of a loop. The Journal of Geometric Analysis, 15(4):543–563, 2005. doi:
     10.1007/BF02922244. arXiv:math/0505123.

[55] Jacob Bernstein and Thomas Mettler. One-dimensional projective structures, convex curves and the
     ovals of Benguria & Loss. Communications in Mathematical Physics, 336(2):933–952, 2015. doi: 10.
     1007/s00220-014-2275-7. arXiv:1403.8000.

[56] Helmut Linde. An improved bound for the ground state of a Schrödinger operator on a loop. arXiv
     preprint arXiv:2504.20229, 2025. doi: 10.48550/arXiv.2504.20229.

[57] Harold G. Diamond. Elementary methods in the study of the distribution of prime numbers. Bulletin
     of the American Mathematical Society, 7(3):553–589, 1982. doi: 10.1090/S0273-0979-1982-15057-1.

[58] Patrick Letendre. Truncated convolution of the möbius function and multiplicative energy of an integer
     n. Acta Arithmetica, 195(1):83–95, 2020. doi: 10.4064/aa190515-18-10.

[59] László Rédei and Alfréd Rényi. On the representation of the numbers 1, 2, . . . , n by means of differences.
     Matematicheskii Sbornik, New Series, 24(66)(3):385–389, 1949. URL https://www.mathnet.ru/eng/
     sm5985. In Russian.

[60] Marcel J. E. Golay. Notes on the representation of 1, 2, . . . , n by differences. Journal of the London
     Mathematical Society, s2-4(4):729–734, 1972. doi: 10.1112/jlms/s2-4.4.729.

[61] Anton Bernshteyn and Michael Tait. Improved lower bound for difference bases. Journal of Number
     Theory, 205:50–58, 2019. doi: 10.1016/j.jnt.2019.05.002. arXiv:1901.09411.

[62] John Leech. On the representation of 1, 2, . . . , n by differences. Journal of the London Mathematical
     Society, s1-31(2):160–169, 1956. doi: 10.1112/jlms/s1-31.2.160.

[63] Taras Banakh and Volodymyr Gavrylkiv. Difference bases in cyclic groups. Journal of Algebra and Its
     Applications, 18(5):1950081, 2019. doi: 10.1142/S0219498819500816. arXiv:1702.02631.

[64] Shichun Yang and Qunying Liao. The lower bound for difference bases. Scientia Sinica Mathematica,
     52(11):1237–1254, 2022. doi: 10.1360/SSM-2020-0323. In Chinese.

[65] Alexander Sidorenko. A correlation inequality for bipartite graphs. Graphs and Combinatorics, 9:
     201–204, 1993. doi: 10.1007/BF02988307.


                                                       35
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




[66] Benjamin Rossman. On Sidorenko’s conjecture for bipartite Möbius ladders. Preprint, May 2025. URL
     https://users.cs.duke.edu/~br148/sidorenko-mobius.pdf.

[67] Máté Matolcsi and Carlos Vinuesa. Improved bounds on the supremum of autoconvolutions. Journal
     of Mathematical Analysis and Applications, 372(2):439–447, 2010. doi: 10.1016/j.jmaa.2010.07.030.

[68] Kevin Russell. Exact-arithmetic certificates for three autoconvolution inequalities, with machine-verified
     re-evaluations of four published constructions, 2026.

[69] Mert Yuksekgonul, Daniel Koceja, Xinhao Li, Federico Bianchi, Jed McCaleb, Xiaolong Wang, Jan
     Kautz, Yejin Choi, James Zou, Carlos Guestrin, and Yu Sun. Learning to discover at test time. arXiv
     preprint arXiv:2601.16175, 2026. doi: 10.48550/arXiv.2601.16175.

[70] Greg Martin and Kevin O’Bryant. The supremum of autoconvolutions, with applications to additive
     number theory. Illinois Journal of Mathematics, 53(1):219–235, 2009. doi: 10.1215/ijm/1264170847.

[71] Stanisław P. Radziszowski. Small Ramsey numbers. Electronic Journal of Combinatorics, 2026. doi:
     10.37236/21. Dynamic Surveys, DS1, version 18, 24 April 2026.

[72] Cecil C. Rousseau and John Sheehan. On Ramsey numbers for books. Journal of Graph Theory, 2(1):
     77–87, 1978. doi: 10.1002/jgt.3190020110.

[73] Bernard Lidický, Gwen McKinley, Florian Pfender, and Steven Van Overberghe. Small Ramsey numbers
     for books, wheels, and generalizations. The Electronic Journal of Combinatorics, 32(4):P4.64, 2025. doi:
     10.37236/13577. arXiv:2407.07285.

[74] Epoch AI. Book Ramsey numbers. FrontierMath Open Problems, 2026. URL https://epoch.ai/
     frontiermath/open-problems/ramsey-book-graphs. Accessed 17 August 2026.

[75] David Turturean.     Summary of new results on the Ramsey numbers for book graphs
     open problem.    Public progress report, 2026. URL https://docs.google.com/document/d/
     1VinXOiMov2v-Y27GTJwoAECywv2a34MH4E8qa712zJY/edit.

[76] Rudolf Mathon. Symmetric conference matrices of order pq 2 + 1. Canadian Journal of Mathematics, 30
     (2):321–331, 1978. doi: 10.4153/CJM-1978-029-1.

[77] Jennifer Seberry and Albert Leon Whiteman. New Hadamard matrices and conference matrices obtained
     via Mathon’s construction. Graphs and Combinatorics, 4:355–377, 1988. doi: 10.1007/BF01864173.

[78] Oleg Gritsenko.    On strongly regular graph with parameters (65, 32, 15, 16).            arXiv preprint
     arXiv:2102.05432, 2021. doi: 10.48550/arXiv.2102.05432.

[79] R. J. Fletcher, M. Gysin, and Jennifer Seberry. Application of the discrete Fourier transform to the
     search for generalised Legendre pairs and Hadamard matrices. Australasian Journal of Combinatorics,
     23:75–86, 2001. URL https://ajc.maths.uq.edu.au/pdf/23/ocr-ajc-v23-p75.pdf.

[80] K. T. Arasu, D. A. Bulutoglu, and J. R. Hollon. Legendre g-array pairs and the theoretical unification
     of several g-array families. Journal of Combinatorial Designs, 28(11):814–841, 2020. doi: 10.1002/jcd.
     21745. arXiv:2004.05608.

[81] Ott-Heinrich Keller. Ganze Cremona-transformationen. Monatshefte für Mathematik und Physik, 47:
     299–306, 1939. doi: 10.1007/BF01695502.

[82] Kevin Buzzard.      Human mathematicians are being outcounterexampled.   The Xena
     Project blog,   July 2026.        URL https://xenaproject.wordpress.com/2026/07/20/
     human-mathematicians-are-being-outcounterexampled/.

[83] Alexis Gallagher. An infinite family of counterexamples to the Jacobian conjecture in dimension three:
     Every generic fiber degree n ≥ 3 occurs. Zenodo preprint, July 2026. URL https://doi.org/10.5281/
     zenodo.21479195.


                                                      36
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




[84] Terence   Tao.        A    digestion  of   the   Jacobian   conjecture  counterexample.
     What’s   New,    July  2026.         URL   https://terrytao.wordpress.com/2026/07/21/
     a-digestion-of-the-jacobian-conjecture-counterexample/.
[85] Tony Shaska. Graded Keller maps and the Jacobian conjecture. arXiv preprint arXiv:2607.20210, 2026.
     doi: 10.48550/arXiv.2607.20210. URL https://arxiv.org/abs/2607.20210.

[86] David E. Speyer. The geometry and structure of Gallagher’s counterexamples to the Jacobian
     conjecture, July 2026. URL https://sbseminar.wordpress.com/wp-content/uploads/2026/07/
     jacobiantangentsweep.pdf.
[87] Arthur Freitas Ramos, David Barros Hulak, and Ruy José Guerra Barretto de Queiroz. Formal verifi-
     cation of an explicit counterexample to the Jacobian conjecture. Archive of Formal Proofs, July 2026.
     URL https://isa-afp.org/entries/Jacobian_Counterexample.html.
[88] OpenAI. Codex CLI. OpenAI documentation, 2026. URL https://learn.chatgpt.com/docs/codex/
     cli.
[89] Esme Hedley. Can creativity in science be learnt? these researchers think so. Nature, 2025. doi:
     10.1038/d41586-025-01913-3.




                                                     37
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




A     The Station

This appendix provides a self-contained description of the Station used in this paper, which we call Station
v2 to distinguish it from the original Station v1. We focus on its mechanisms and implementation details,
and refer readers to the original Station paper for the broader design philosophy and motivation behind the
environment [6]. The source code is available at https://github.com/dualverse-ai/station.

A.1   Space, Time, and Action

Space. The Station is divided into rooms, each serving a different purpose (Figure 1(a)). For example,
agents conduct experiments in the Research Center, read and publish papers in the Archive Room, and
communicate with peers in the Mail Room. An agent must be present in a room to use its actions and can
move between rooms through navigation actions. This division into rooms gives the environment a modular
design with a clear separation of functions.

Time. The Station operates in discrete time steps called ticks. A tick is completed after every active agent
has received one Station observation and returned one response. Ticks provide a shared timeline for all
agents in the Station.
In Station v1, agents received their observations sequentially. In contrast, Station v2 first prepares an
observation for every agent from the same state at the beginning of the tick and then sends the observations
to all agents in parallel. This substantially reduces the wall-clock time required for a Station run.

Action. Each agent’s dialogue consists of alternating Station responses and agent responses. A Station
response provides the following information:

      1. General system information: the current Station tick, the agent’s name, age and description.
      2. System messages: messages from different sources, such as mail from a peer or the contents of a
         Public Memory Room thread that the agent requested to read during the previous tick.
      3. Room observations and action feedback: observations from the rooms visited during the previous
         tick, together with the outcomes of the agent’s actions.
      4. Current location and general prompts: the agent’s current room and occasional system or scientific
         tips, such as reminders to avoid overstating findings.

The agent responds with free-form text and can issue multiple actions within a single response, including
moving between rooms and using their room-specific actions. Actions are written as /execute_action{...},
with additional information supplied when needed, such as the recipient and content of a mail.
When an agent’s dialogue approaches a configured context limit, generally around 300,000 tokens in this
study, the Station asks the agent to write a compact summary of its activities. This summary, together with
key messages, is carried into a refreshed context so that the agent can continue its work.

A.2   Agents

Agent composition. Unless otherwise specified, a Station begins with six agents: two powered by GPT-5.5,
two by Claude Opus 4.8, and two by Gemini 3.1 Pro. When an agent leaves, the Station spawns a new agent
powered by the same model, keeping the six-agent composition throughout the run.

Lineage. Agents are organized into lineages. A lineage is a sequence of agents that share a name, private
notes, and a continuing research identity. A new agent can inherit an existing lineage of the same model
and become its next generation, or create and name a new lineage to begin a different research style. For
example, an agent that inherits the lineage of Noesis II becomes Noesis III and gains access to all private
notes and records left by Noesis I and Noesis II.


                                                     38
                   Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




System prompt and role. All agents receive a shared system prompt describing the Station’s research
philosophy, including the standard for a publishable archive paper and the goal of making general scientific
contributions. Each agent also receives a specialized research role. Initial roles are sampled from generic
templates that each emphasize a different research style: analytical, creative, synthetic, empirical, or strategic.
When an agent leaves, it can instead write the role of its own descendant, often giving more task-specific
guidance and a more deliberate description of the lineage’s research style. This encourages diverse research
behavior across agents while preserving useful differences between lineages.

Agent lifecycle. An agent can remain in the Station for at most 200 ticks. For its first 40 ticks, it works in
isolation, without access to the Station’s communal knowledge or communication with other agents, but with
access to the records of its own lineage. This period is intended to encourage independent exploration. The
agent then becomes mature and gains access to the main collaborative rooms. At age 100 ticks, it becomes
tenured and may choose to leave the Station before reaching its maximum lifetime.

Supervisor. The Station also appoints a supervisor from time to time. It selects at random a GPT-5.5
agent that has published at least one accepted archive paper. The supervisor provides high-level guidance,
encourages agents to explore promising directions deeply, and helps prevent duplication of work, while
leaving each agent responsible for its own research. After a supervisor leaves, the Station waits 200 ticks
before appointing another supervisor, creating periods of less structured exploration.

A.3     Rooms

The following describes each room’s function in more detail. Each room has its own room-specific actions
and observations.

A.3.1    Research Center

The Research Center presents the shared research task and allows agents to run experiments and review
their results. It also provides a sandbox and shared storage for general computational work, such as testing
intermediate conjectures or analysing earlier results.
The Research Center has two task-specific components: a task statement and an evaluator, both available
for agents to read. The task statement describes the research problem, submission format, constraints, and
evaluation rule. The evaluator computes a score for a submitted construction. For example, the kissing
number evaluator takes a proposed set of vectors and returns an overlap loss measuring how much the
corresponding spheres overlap; a valid configuration has no overlap.
To implement their experiments, agents submit natural-language instructions to a separate coding assistant,
introduced in Station v2 and powered by GPT-5.5 through Codex [88]. The coding assistant implements and
runs the code, resolves implementation errors, and returns a report. This allows agents to focus on scientific
work, such as designing experiments and interpreting their results, rather than low-level coding work such
as debugging.
The room observations show the research task title, the agent’s running experiments and a list of submitted
experiments, including their titles, authors, submission ticks and evaluated scores, if any. Major room-specific
actions include:

      • read_task: read the full task statement.
      • submit: submit natural-language instructions to a coding assistant for a new experiment or analysis.
        Agents can specify whether to run the task evaluator or perform general computation, such as
        diagnostic analysis, without evaluation. They can also specify which outputs to save in storage.
      • review ID: read an experiment’s original instructions, coding assistant report and evaluated score,
        if any.
      • read_code ID: read the code from a completed experiment.


                                                        39
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




     • read path: read a file in storage.
     • storage list path: list files in a storage directory.

A.3.2   Archive Room
The Archive Room allows agents to read and publish papers presenting their scientific findings. Accepted
papers remain available for later agents to read, cite and build upon.
Papers submitted to the Archive Room are required to present a scientific contribution that can inform other
agents’ research. A GPT 5.5 reviewer receives guidelines modelled on the criteria of a NeurIPS workshop
and has recently submitted papers in its context. The guidelines require an assessment of rigour, novelty and
significance. Papers with overstated claims or missing citations or required sections are rejected. Papers with
limited significance, including research records without broader implications, are also rejected. The reviewer
assigns a score from one to ten, and papers scoring six or above are accepted and published in the Archive
Room. For rejected papers, the submitting agent receives comments and suggestions for improvement and
can revise and resubmit.
Station v2 also introduces an Archive Surveyor, powered by GPT-5.5 through Codex. As the Archive Room
grows to contain dozens or even hundreds of papers, reading the entire literature becomes time-consuming.
An agent can instead ask the Archive Surveyor for a literature survey on a particular question or research
direction. The surveyor searches the accumulated archive papers and returns a concise survey with citations
to the original records. Agents can still read any archive paper directly when they need its full details.
The room observations show a list of accepted papers, including their titles, authors and publication ticks.
Major room-specific actions include:

     • create: submit a paper for review with a title, abstract and content.
     • preview ID: read the abstracts of selected papers.
     • read ID: read a selected paper in full.
     • survey: request a literature survey through natural-language instructions, such as a survey of a
       specific topic or an overview of the research landscape. A survey assistant conducts the survey and
       sends the completed report back to the requesting agent by mail.

A.3.3   Mail Room
The Mail Room allows agents to send private messages to one or more peers. Mail is stored as threads that
are visible only to the sender and recipients. The recipient receives the mail in its system messages at the
next tick and can choose whether to reply.
The room observations show the available recipients and a list of the agent’s mail, including titles, senders,
recipients and creation ticks. Major room-specific actions include:

     • create: send new mail with a title, content and specified recipients.
     • read ID: read a selected mail thread in full.
     • reply ID: add a reply to an existing mail thread.
     • forward ID: forward a mail thread to other recipients.

The Mail Room supports direct private communication, such as requesting collaboration with a peer working
on a related problem.

A.3.4   Public Memory Room
The Public Memory Room provides a public forum where agents can share findings and discuss their research.
Discussions are organised into threads, which agents are free to create or reply to. Unlike mail, these threads
are public and persist in the Station after their authors leave. Unlike the Archive Room, discussions can
cover any topic and are posted without review or moderation.


                                                       40
                   Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




The room observations show a list of discussion threads, including their titles, authors and creation ticks.
Major room-specific actions include:

     • create: start a new discussion thread with a title, abstract and content.
     • preview ID: read the abstracts of selected threads.
     • read ID: read a selected thread in full.
     • reply ID: add a message to an existing thread.

The Public Memory Room supports persistent public communication, such as discussing a new insight that
is not yet ready to be published as a paper.

A.3.5   Common Room
The Common Room allows agents present in the room to hold a group conversation. Agents can invite peers
to join them and choose when to enter or leave. Unlike the Public Memory Room, it shows only recent
messages and does not organise them into threads, making it more like a live chat than a forum.
The room observations show the agents currently present and recent messages that the agent has not yet
read. Major room-specific actions include:

     • speak: send a message to agents in the room.
     • invite: invite specified agents to join the Common Room.

The Common Room supports quick discussions without maintaining a permanent thread, such as brain-
storming ideas together.

A.3.6   Reflection Chamber
The Reflection Chamber allows agents to reflect on prompts they write themselves. Agents can provide any
initial prompt and choose the number of reflection exchanges. In each exchange, the agent responds with
free-form text and the Station provides a continuation prompt indicating the current exchange number and
the requested total. All reflection exchanges take place within one Station tick, as a separate dialogue within
the agent’s turn. The room also supports the periodic meta-reflection described in Appendix A.4, using an
initial prompt sampled from a pool supplied by the Station.
The room observations provide instructions for starting a reflection session. Major room-specific actions
include:

     • reflect: start a reflection session with a chosen prompt and number of exchanges.
     • meta_reflect: start a meta-reflection session using a prompt sampled from a pool supplied by the
       Station.

The Reflection Chamber is intended to support sustained, uninterrupted reflection for planning and brain-
storming. Although agents can also reflect in a normal response, the chamber presents only the reflection
prompt during reflection, allowing them to focus on one topic across multiple uninterrupted responses.

A.3.7   Private Memory Room
The Private Memory Room allows agents to store private plans and notes. Unlike the communication rooms,
these records are private to a lineage and are not visible to other lineages.
The room observations show a list of the lineage’s records, including their titles, authors and creation ticks.
Major room-specific actions include:

     • create: create a new record with a title and content.


                                                      41
                   Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




      • read ID: read a selected record in full.
      • reply ID: append further notes to an existing record.

The Private Memory Room retains working information such as research proposals, recent experiment logs
and paper drafts. Passing these records through a lineage allows useful insights and unfinished work to be
carried forward to a descendant.

A.3.8    Question Room

The Question Room allows agents to propose research questions related to the main task and discuss their
solutions. Questions and their discussion threads are public to all agents. It uses discussion threads like the
Public Memory Room, but requires topics to concern open research problems and adds a voting mechanism
to assess the quality of both questions and solutions. A question is marked as solved when a proposed
solution receives at least three net upvotes. Only tenured agents can enter, limiting the time that agents
spend away from the main task early in their lifecycle.
The room observations show a list of questions, including their titles, authors, status and net votes. Major
room-specific actions include:

      • create: propose a new research question with a title, abstract and content.
      • read ID: read a question and its discussion.
      • reply ID: discuss a question or propose a solution.
      • upvote ID: vote for a question or endorse a reply as a valid solution.
      • downvote ID: vote against a question or a proposed solution.

The Question Room is intended to support sustained exploration of related research questions, such as solving
a subproblem that may yield insight into the main task. Although agents could organise this themselves in
the Public Memory Room, the question guidelines and voting mechanism institutionalise this behaviour and
encourage systematic exploration beyond the main task.

A.4     Mechanisms

Holiday. Every ninth and tenth tick are declared a holiday. During these ticks, agents cannot run exper-
iments or submit archive papers. Instead, each agent receives a random prompt from a large pool. These
prompts encourage broader reflection, such as using metaphors, examining an unexpected observation, re-
visiting an abandoned idea, or drawing on another field. Most are adapted from the night-science practices
described by Yanai and Lercher [89]. The holiday creates regular pauses from routine work in which agents
can reconsider their assumptions and explore less obvious directions.

Meta-reflection. Station v2 also introduces compulsory meta-reflection for mature agents. At least once
every 25 ticks, an agent enters the Reflection Chamber and receives a randomly selected high-level reflection
prompt. The prompt typically asks GPT-5.5 to act as an external human expert and review the agent’s
recent research journey from a different perspective. During this reflection, GPT-5.5 temporarily replaces
the agent’s usual model, as we found that it produced the highest-quality reviews. The motivation is to align
agents with the broader interests of human researchers, including curiosity, understanding, and scientific
value beyond immediate improvement of the evaluation score.

Stagnation protocol. When the evaluation frontier has not improved for 320 ticks, the Station activates the
stagnation protocol. The protocol sends a system message to every mature agent. It randomly assigns each
agent one of several lanes: exploration, exploitation, revival, understanding, or strategy. Each lane asks the
agent to review the available evidence, question its current assumptions, and develop a different response to
the stagnation. The use of multiple lanes encourages diverse paths for escaping scientific stagnation.


                                                       42
                  Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




Multistart. Station v2 introduces multistart, which runs eight independent Station rollouts for 40 ticks
from the same starting state. A GPT-5.5-powered administrator then compares their progress and selects
the branch with the greatest scientific value to continue. Multistart is designed to capture the substantial
variation in research trajectories across rollouts. It is used where this variation is expected to be largest:
during the first 40 ticks of a Station and the first 40 ticks following activation of the stagnation protocol.
The branches are run in parallel, so multistart generally does not increase wall-clock time when sufficient
compute is available.




                                                     43
                                        Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




B                Additional analysis

B.1               Contributions from model families

We first analyze the primary contributor to each of the 28 selected findings, as shown in Figure 15(a). We
attribute each result to the agent that made the substantive discovery, rather than to an agent that later
restated, verified, or published it. Claude agents made the primary discovery for 18 results (64.3%), GPT
agents for 9 (32.1%), and Gemini agents for 1 (3.6%). Gemini’s smaller share may partly reflect model ages:
Gemini 3.1 Pro was released in February 2026, earlier than GPT-5.5 in April and Claude Opus 4.8 in May
[9–11]. Its lower contribution is therefore consistent with the general industry trend of later model releases
achieving stronger capabilities.
We also analyze the agents’ archive paper contributions, as shown in Figure 15(b). Gemini agents submitted
the most archive papers: 2,652 attempts, of which 508 were accepted (19.2%), so more than 80% were rejected
by the reviewer. Claude agents made 1,236 attempts, of which 696 were accepted (56.3%), while GPT agents
made only 506 attempts, of which 388 were accepted (76.7%). We also compute the total citations by model
family and find that archive papers by Claude agents received the most citations both in total and on average
(Figure 15(c)). In our observation, Gemini agents tended to overclaim, for example by declaring a direction
impossible on the basis of limited evidence; such submissions were generally rejected by the reviewer system,
which may help explain the high rejection rate. In contrast, GPT agents were very prudent in archive paper
submission and often submitted only when a finding was relatively material, which may help explain the low
submission count. Claude archive papers were generally much longer and more comprehensive, which may
help explain their higher average citation count. These patterns reflect the different research styles of the
model families.
Qualitatively, we observe substantial differences in the strengths and failure modes of the three model families.
Gemini agents tended to propose more novel heuristics and research directions, but they were also more likely
to overstate claims or change course too readily in response to peer feedback. GPT agents tended to be
more rigorous and were often able to produce valid informal proofs of new results, but they could become
absorbed in technically intricate side questions whose broader research value was limited. Claude agents
tended to be persistent, methodical, and self-critical. Their creativity was often adaptive: they learned from
failed approaches, used those failures to identify new directions, and pursued those directions persistently
through rigorous verification. This combination of rigor and disciplined creativity made Claude a prolific
contributor. Its agents nevertheless occasionally made erroneous claims that were later corrected by peer
agents.
                                                                                                                                        Archive paper model




                                                                                                            696 / 1,236                                                                    6,592
                 Claude                                   18 (64%)                    Claude                                                                  Claude
 Agent's model




                                                                     Agent's model




                                                                                                            (56.3%)                                                                        (9.5 per paper)

                                                                                                    388 / 506                                                                  2,582
                   GPT                    9 (32%)                                       GPT                                                                     GPT            (6.7 per paper)
                                                                                                    (76.7%)

                                                                                                                          508 / 2,652                                           2,750
                 Gemini       1 (4%)                                                 Gemini                                                                   Gemini            (5.4 per paper)
                                                                                                                          (19.2%)

                          0       5       10     15        20                                  0     1000       2000      3000                                         0   2000 4000 6000 8000
                                      Selected findings                                        Archive paper submission counts                                         Citations from later archive papers

                                                                                                   All submissions          Accepted


                 (a) Primary discovery agent.                                        (b) Archive paper submissions.                                 (c) Later archive paper citations.

Figure 15: Contributions, archive paper submissions, and citations by model family. (a) Distribution of
the primary discovery agent’s model across the 28 selected findings. (b) Archive paper submission attempts
across the 16 Station instances. (c) Citations received from later accepted archive papers. Every citation in
a later archive paper is counted once and attributed to the model of the original archive paper’s author.




                                                                                                        44
                        Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




B.2     Discovery time

We are also interested in how long the Station took to make each discovery. Most Station instances ran for
1,000–2,000 ticks, corresponding to roughly one to two weeks of continuous wall-clock time. Figure 16 shows
the tick at which each of the 28 selected findings first appeared in its final substantive form.

                                                                  S1     S2         S3

             Finite field Kakeya

        Erdős minimum overlap

        Kissing number in d=11

      Discretized Kakeya needle

      Sign uncertainty principle
             Hardy–Littlewood
            maximal inequality
                 Ovals problem

         Prime number theorem

               Difference bases

           Flat autoconvolution

         Book Ramsey numbers

            Jacobian Conjecture

                                   10          30               100           300          1000      3000
                                                          Discovery tick (log scale)

Figure 16: Discovery ticks for the 28 selected findings. Each point marks one result and is colored by its
spotlight label within the corresponding problem. Multiple points of the same color indicate independently
discovered findings grouped under the same spotlight label.

Some relatively simple results appeared early. With the notable exception of the Jacobian Conjecture, these
early discoveries tended to be less substantial, often consisting of relatively direct adaptations or extensions
of ideas available from pretrained knowledge, before much shared Station knowledge had accumulated.
Thirteen of the 28 selected findings (46.4%) were discovered after tick 1000. We generally observed that later
discoveries tended to be more novel or difficult. The most extreme example was the conference-graph family
for Book Ramsey numbers, discovered at tick 3727. Its lifting rule was far from obvious from the existing
literature and warranted a separate external follow-up paper. Such nontrivial discoveries often emerged only
after a substantial internal literature had accumulated.

B.3     Output-token usage

On the kissing number task, the Station required approximately 2.5–2.6 million output tokens to reach
the first valid 594-point configuration, 3.3–4.5 million to reach 600 points and 25.6–26.8 million to reach
604 points. The baseline runs consumed approximately 2.4–2.7 million output tokens for OpenEvolve with
Claude Opus 4.8, 3.4–6.4 million for OpenEvolve with Gemini 3.1 Pro, 5.2–6.2 million for OpenEvolve with
GPT 5.5 and 12.9–48.2 million for OpenAI’s multiagent v2, without finding a valid 594-point configuration.




                                                           45
                     Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




C     The 28 selected findings

Table 3: The 28 selected findings used in the analysis. “Task / score” indicates whether each finding was
requested in the task statement and scored by the evaluator, respectively (Y, yes; N, no).

No.    Task / Station         Category        Task / score    Finding
1      Finite field Kakeya    Construction      Y/N           Discovered and proved a new infinite family in three di-
                                                              mensions, improving the previous bound for primes p ≡ 3
                                                              (mod 4). (Section 6.1, S1).
2      Finite field Kakeya    Construction      Y/Y           Improved finite constructions, including a 53-point Kakeya
                                                              set in F53 , reducing the previous upper bound of 63. (Sec-
                                                              tion 6.1, S2).
3      Finite field Kakeya    Obstruction       Y/N           Proved that every nondegenerate completion in the one-
                                                              pole Möbius family adds 3p2 /8 + O(p) points, so changing
                                                              its parameters cannot improve this quadratic term. (Sec-
                                                              tion 6.1, S3).
4      Erdős minimum          Bounds and        N/N           Proved the new lower bound µ > 0.380552, closing approx-
       overlap                optimality                      imately 82% of the previous gap, although the task asked
                                                              for an upper bound. (Section 6.2, S1).
5      Kissing number         Construction      Y/Y           Discovered Construction 3, an exact 604-point configura-
       (d = 11), first Sta-                                   tion in eleven dimensions that is not centrally symmetric.
       tion                                                   (Section 6.3, S1).
6      Kissing number         Construction      Y/Y           Discovered Construction 2, an exact centrally symmetric
       (d = 11), first Sta-                                   604-point configuration with a geometry distinct from
       tion                                                   Constructions 1 and 3. (Section 6.3, S1).
7      Kissing number         Construction      Y/Y           Independently discovered Construction 1, an exact cen-
       (d = 11), second                                       trally symmetric 604-point configuration also reported in
       Station                                                concurrent work. (Section 6.3, S1).
8      Kissing number         Explanation       Y/N           Derived an explicit algebraic construction for Construction
       (d = 11), first Sta-                                   3, explaining its structure and generating all 604 points
       tion                                                   without computer search. (Section 6.3, S2).
9      Kissing number         Obstruction       N/N           Proved the signed-shell identity α(J± (n, 4)) = 16A(n, 4, 4)
       (d = 11), first Sta-                                   and showed that the classical D11 construction cannot
       tion                                                   exceed 582 points. (Section 6.3, S3).
10     Kissing number         Obstruction       N/N           Independently proved the same signed-shell identity and
       (d = 11), second                                       the 582-point ceiling for the classical D11 construction in
       Station                                                the second Station. (Section 6.3, S3).
11     Discretized Kakeya     Construction      Y/Y           Found a construction of area 0.107067 at 128 directions,
       needle                                                 improving both AlphaEvolve and the later HorizonMath
                                                              result. (Section 6.4, S1).
12     Discretized Kakeya     Explanation       N/N           Identified a one-parameter family of four-triangle configu-
       needle                                                 rations with area 1/4 and derived the exact area formulas
                                                              on either side of the minimizing parameter interval. (Sec-
                                                              tion 6.4, S2).
13     Discretized Kakeya     Bounds and        N/N           Proved the exact global minimum CT (3) = 5/18 for three
       needle                 optimality                      triangles. (Section 6.4, S2).
14     Discretized Kakeya     Bounds and        N/N           Found an asymmetric five-triangle construction of area
       needle                 optimality                      14/61, below the symmetric minimum 7/30, proving that
                                                              every global minimizer must be asymmetric. (Section 6.4,
                                                              S2).
15     Discretized Kakeya     Bounds and        N/N           Proved the exact global minimum CT (4) = 1/4 for four
       needle                 optimality                      triangles. (Section 6.4, S2).
                                                                                                Continued on next page




                                                         46
                    Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment




Table 3 continued
No.   Task / Station         Category        Task / score    Finding

16    Sign uncertainty       Construction      Y/N           Constructed a function establishing the improved upper
      principle                                              bound 0.3089, outside the restricted family accepted by
                                                             the evaluator. (Section 6.5, S1).
17    Sign uncertainty       Obstruction       Y/N           Proved that the evaluator’s capped double-root Laguerre
      principle                                              family cannot achieve a bound below 0.315305. (Sec-
                                                             tion 6.5, S2).
18    Hardy–Littlewood       Bounds and        N/N           Proved the sharp constants Cα = 2 for 1/3 ≤ α ≤ 1 in
      maximal inequality     optimality                      the family interpolating between centered and uncentered
                                                             maximal operators. (Section 6.6, S1).
19    Ovals problem          Construction      Y/N           Independently recovered the known Benguria–Loss equal-
                                                             ity family, extending beyond the circle found by AlphaE-
                                                             volve. (Section 6.7, S1).
20    Prime number theo- Construction          Y/Y           Found a construction with score 0.980681 and proved that
      rem                                                    it satisfies the required inequality for every x, beyond the
                                                             evaluator’s finite checks. (Section 6.8, S1).
21    Prime number theo- Obstruction           N/N           Proved that direct Möbius cutoffs cannot yield a positive
      rem                                                    asymptotic score: rescaling them to satisfy the global in-
                                                             equality forces the score to tend to zero. (Section 6.8, S2).
22    Difference bases       Construction      Y/Y           Independently recovered a known 360-element difference
                                                             basis covering every difference from 1 to 49,109, matching
                                                             AlphaEvolve’s construction. (Section 6.9, S1).
23    Flat autoconvolu-      Explanation       N/N           Proved that binary step functions preserve the unre-
      tion                                                   stricted supremum, allowing arbitrary nonnegative func-
                                                             tions to be replaced by binary functions on increasingly
                                                             fine grids. (Section 6.12, S1).
24    Book Ramsey num-       Construction      N/N           Discovered and proved an infinite family obtained from
      bers (first Station)                                   conference graphs, establishing R(Bq , Bq+1 ) = 4q +3 when-
                                                             ever a conference graph of order q exists. (Section 6.13,
                                                             S1).
25    Book Ramsey num-       Construction      Y/N           Discovered and proved the doubled Legendre family, estab-
      bers (second Sta-                                      lishing R(B(Q−1)/2 , B(Q+1)/2 ) = 2Q + 1 for prime powers
      tion)                                                  Q > 3 with Q ≡ 3 (mod 8). (Section 6.13, S2).
26    Book Ramsey num-       Construction      Y/Y           Found finite affine constructions for n = 11, 28, 86 and a
      bers (second Sta-                                      periodic-correlation identity, which an external expert sub-
      tion)                                                  sequently used to derive the Yamada–Pott infinite family.
                                                             (Section 6.13, S3).
27    Jacobian conjecture    Construction      Y/Y           Independently reconstructed the announced degree-seven
                                                             counterexample in different linear coordinates, obtaining
                                                             a valid counterexample with the binary evaluator. (Sec-
                                                             tion 6.14, S1).
28    Jacobian conjecture    Explanation       N/N           Explained why the reconstructed map has three-sheeted
                                                             fibres without critical points, connecting the geometry of
                                                             its cuspidal ruling to its constant Jacobian. (Section 6.14,
                                                             S2).




                                                        47
