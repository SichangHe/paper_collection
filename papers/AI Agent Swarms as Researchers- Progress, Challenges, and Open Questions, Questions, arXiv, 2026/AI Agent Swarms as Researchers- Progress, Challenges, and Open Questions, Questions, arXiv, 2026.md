                                          AI Agent Swarms as Researchers: Progress, Challenges, and Open
                                                                   Questions
                                                                                      A perspective

                                                                  Sergey Gusev                    David E. Bernal Neira
                                                               Purdue University, USA               Purdue University, USA
                                                                 sgusev@purdue.edu                   dbernaln@purdue.edu
arXiv:2609.35719v1 [cs.CY] 28 Sep 2026




                                                                                     September 2026


                                                                                          Abstract
                                                  Artificial intelligence (AI) agents, language models connected to tools and run in a loop, can
                                              now carry out long, multi-step tasks with little supervision. We gave swarms of off-the-shelf
                                              coding agents a short statement of scope, from a narrow topic to a whole field, access to the
                                              literature and to computing tools, and one standing instruction: make real, correct, useful
                                              progress, and do not stop. We supplied no scientific ideas. Within weeks, the agents produced a
                                              large body of research notes, paper-length drafts, and formal proofs in five areas of optimization
                                              theory and physical science, and proposed untested laboratory experiments in a sixth. We do
                                              not claim that all of it is correct or new, but it is not noise: in what we have checked so far, we
                                              found no major scientific error, and several results are proved in a proof assistant. The agents
                                              produced results faster than we could review them; we estimate that a full review would take us
                                              months. Together with two widely discussed 2026 results in mathematics obtained with swarms,
                                              our runs suggest that agents can already do a large part of routine theoretical research, at least
                                              in areas that we experimented with. This raises questions we cannot yet answer: how to trust
                                              results when review, not production, is the scarce resource; what credit and publication counts
                                              mean when the human input is a prompt, and why institutions would pay researchers rather
                                              than buy computing time; and how people can learn a field, add to what agents do, and stay
                                              in control of research they cannot keep up with. Research institutions are not ready: models
                                              improve faster than institutions change, so they should decide now how to respond as capabilities
                                              increase. We offer tentative positions, release the agents’ unedited output as of 25 September
                                              2026, and invite readers to repeat the experiment in their own fields.


                                         Contents
                                         1 Introduction                                                                                             3

                                         2 What led us here                                                                                         5
                                           2.1 The Hugging Face incident . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .            5
                                           2.2 The Riemann zeta result . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          5
                                           2.3 The Navier–Stokes result . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         6
                                           2.4 Our earlier tools, and taking ourselves out of the loop . . . . . . . . . . . . . . . . .            7

                                         3 Prior work                                                                                               8
                                           3.1 Automated discovery, from BACON to AI scientists . . . . . . . . . . . . . . . . . .                 8


                                                                                              1
   3.2   Machine-checked mathematics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
   3.3   Controlled evaluations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
   3.4   Review, reproducibility, and institutions . . . . . . . . . . . . . . . . . . . . . . . . . 12
   3.5   Relation to prior work . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

4 The experiment                                                                                       13
  4.1 The procedure we followed . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      13
  4.2 Models, harnesses, and cost . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      14
  4.3 Output . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     16
  4.4 Review evidence and remaining work . . . . . . . . . . . . . . . . . . . . . . . . . . .         18

5 Open questions and our positions                                                                     19
  5.1 Two common responses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         19
  5.2 Review and trust . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     22
  5.3 Access to the literature, and what “new” means . . . . . . . . . . . . . . . . . . . . .         24
  5.4 Publication and peer review . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      25
  5.5 Credit, authorship, and publication counts . . . . . . . . . . . . . . . . . . . . . . . .       26
  5.6 The economic case for researchers . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      28
  5.7 Computation, budgets, and fairness . . . . . . . . . . . . . . . . . . . . . . . . . . . .       29
  5.8 Learning and motivation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      30
  5.9 Field-scale runs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   33
  5.10 Staying in control without keeping up . . . . . . . . . . . . . . . . . . . . . . . . . .       34

6 Summary of positions                                                                                 37

7 Release and proposal                                                                           38
  7.1 Why we release now . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 38
  7.2 What we propose to readers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39

A Prior work in more detail                                                                            63
  A.1 Discovery inside a human-built loop . . . . . . . . . . . . . . . . . . . . . . . . . . .        63
  A.2 End-to-end AI research systems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       63
  A.3 Tests of research agents that were run once . . . . . . . . . . . . . . . . . . . . . . .        65
  A.4 Review, novelty, institutions, and early effects on output . . . . . . . . . . . . . . . .       66

B Prompts                                                                                              68
  B.1 A literature-collection prompt . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     68
  B.2 Research prompts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     68
  B.3 A paper-writing prompt . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       70
  B.4 A formal-verification prompt . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       71

C Research inventory                                                                                   71




                                                   2
1    Introduction
We gave groups of AI agents a scope, as narrow as one topic or as wide as a whole field, and told
them to make progress. We gave them no ideas (Figure 1). Within a few weeks, the agents had
produced a corpus (the full body of research notes, paper drafts, formal proofs, and code) that we
estimate would take us months to review. Some of it may be wrong, and some of it may turn out
not to be new; we do not know yet, because we have not checked all of it. Much of it appears to be
the kind of incremental advance that makes up most of a working scientist’s output. In the part we
have checked, we have found no major scientific error, and some results are machine-checked, that
is, checked step by step by a computer (Section 4.4).
     The agents produced candidate results faster than we could assess their correctness, novelty, and
usefulness. In our experience the bottleneck has moved from producing results to reviewing them:
we lack the time, and for some results perhaps the ability, to decide which deserve trust. A survey
of 637 scientists in the United States and United Kingdom by Google, Google DeepMind, and MIT
FutureTech reports the same shift: as AI makes some stages of research easier, the bottleneck moves
downstream, and of the scientists who save time with AI, 46% spend more than a quarter of the
saved time checking its output [1]. Proofs checked by machine and review by agents can take on
part of that work; how much, and with what error rate, is an active area of research with early
results (Sections 3.4 and 5.2). If this pattern holds more broadly, it undermines the assumptions
behind hiring, promotion, and peer review in academia, and the habit of counting papers. Every
publication system assumes that the author has checked the work first and answers for it, and
that reviewers take a second look. When one researcher can produce more than they can review
themselves, the first look is already missing, and no amount of second looks replaces it (Section 5.4).
Noise could be ignored, but this output merits review.
     In hindsight none of this is surprising. Automating research has been a goal of AI research for
decades (Section 3). Most of our corpus was produced with the newest models available during
our runs, but the argument does not rest on them alone: some of our results came from GPT-5.6
Sol, a model that had been publicly available for almost two months (Section 4.2). Models could
already do this work before we noticed. Many researchers already use these models, as the rapid
rise in AI-assisted preprints suggests (Section 3.4), but mostly quietly, with little open discussion
of how research should change. Two 2026 results in mathematics show how far this has gone: a
proof that more than 66% of the zeros covered by the Riemann hypothesis lie where it says all of
them do, up from a previous best of about 42%, and a proof, still under independent review, that
a version of the Navier–Stokes equations of fluid flow can break down in finite time (Section 2).
OpenAI has since said that the model behind the second result has resolved more than 100 further
open problems; it has not yet published them [2, 3]. Our reading of our own runs, together with
these results, is that in areas like ours a large part of ordinary theoretical research can already be
automated, although we have not yet reviewed enough of the output to say how much of it holds
up. Most research is not yet done this way, but in such areas it could be now. Discussion of AI
in science usually waits for a breakthrough. But most scientific progress comes from incremental
work, the institutions of research are built around it, and in theoretical fields agents can already
do much of it (Section 5.1). The question is no longer whether agents can do research, or when
they will beat the best person in a field, but how research should adapt to what agents already
do. On the measured trend, we expect agents to move far ahead of people in some fields, probably
in mathematics first, and because anyone with access to current models can run them, no single
company or institution can control how fast this happens (Sections 5.9 and 5.10). None of this says
that people have nothing to add. It says that how they contribute has to change.
     None of the individual pieces of this observation is new. Computers have generated and tested


                                                  3
  1. Describe the problem or         2. Provide papers and             3. Ask a swarm of agents
  field.                             tools.                            to make progress, and not
  Enough context to work from;       And permission to get more.       to stop.
  freedom to explore any idea.   +                                 +   Every result reviewed by a
                                                                       fresh agent. Write it up. Ver-
                                                                       ify by proof or by computation
                                                                       where possible.


Figure 1: The procedure we followed. Section 4 describes each step, and Appendix B gives examples
of the prompts we used, word for word.


scientific hypotheses for more than twenty years, language-model systems have written complete
papers since 2024, and two results in mathematics obtained with large groups of agents, commonly
called swarms, were announced in the weeks before we wrote this. Nor are we the first to say that
the bottleneck moves. Tao has argued that in mathematics it is shifting from finding arguments
to verification, exposition, and acceptance by the community [4], and a recent theoretical analysis
argues that human effort stays in proportion to the share of the work that is truly new, however
capable the agents become [5]. What we add is a simple experiment that many people can repeat,
an unedited corpus, released as it stood on 25 September 2026 [6], and an argument about what the
resulting review backlog means. Our procedure is not the best way to do research with agents, nor
the most cost-effective (Section 4.1). We use it because it is simple: if it already produces research
worth reviewing, better methods will produce more.
    These results raise questions that we cannot answer. Mathematicians have begun to discuss
them (Section 2), but the questions are not limited to mathematics, and we do not think research
institutions have answers to them yet. How should results be trusted when review, not production,
is the scarce resource, who or what should do the review, and what level of checking does each
kind of result need (Section 5.2)? What counts as new when part of the literature is closed to the
agents (Section 5.3), and what should publication and peer review become (Section 5.4)? What
do credit and publication counts mean when the human input is a prompt (Section 5.5), and why
would an institution pay a researcher rather than spend the money on computation (Section 5.6)?
Does the best researcher become the one with the largest computing budget (Section 5.7)? How
should people learn a field when machines can already do much of its work (Section 5.8)? If agents
can do much of a field’s work on their own, where can people still add something, and what happens
when agents move faster than people can follow, let alone add to (Sections 5.9 and 5.10)? And how
do people stay in control of research they cannot keep up with, and where are guardrails needed
(Section 5.10)?
    This paper does not try to settle these questions. Instead, it shows that a very simple procedure
already produces research worth reviewing. It invites readers to repeat the experiment in their own
fields and to report what they find (Section 7). Failures are worth reporting too, with the model
and the date. Capability is uneven, so the same agents may fail on one problem and do remarkable
work on another, and it improves quickly, so a failure is most informative when the experiment is
repeated as new models arrive and compared with what agents could do six months or a year earlier.
And it calls on researchers, institutions, and everyone who depends on research to start working
on these questions now. Much of how research is organized, from peer review and publication
counts to hiring, funding, and graduate training, rests on two assumptions: that producing a result
takes a long time, and that its author has checked it. Neither holds when agents do the work. We
believe that research institutions, and the incentives they create, are not ready for this. Nor is


                                                   4
it enough to adapt to today’s models. Institutions change over years, while models improve over
months. A new curriculum, review policy, or safeguard designed around today’s models will come
into force only after those models have been replaced, and their replacements will be replaced in
turn, each more capable than the last if the measured trend continues (Section 3.3). Institutions
should therefore plan for capabilities that keep increasing, not for any one generation of models, and
revisit their changes as capabilities grow. Institutions should also plan for specific capabilities before
they arrive, and decide now how they will respond if, for example, agent review proves as reliable as
expert review, agents overtake people in a field, or self-driving laboratories, in which robots run
experiments chosen by an algorithm, make experiments cheap to run (Section 5.10). Where we can,
we offer tentative answers and take positions (Section 6), and we expect many of them to change.
In our view, research institutions should already have started preparing for these changes.

Evidence about limits. This paper cites many studies that measured what AI systems could
not do. A limitation measured on one model is evidence about that model on that date, not about
what AI can do now or in the future. A measured capability does not expire in the same way,
because later models add to it. Since 2019, such limitations have been overtaken within months, on
a trend that has itself been measured, although capability at any moment is uneven across tasks
(Section 3.3). The trend could still stop; Section 3.3 says which of our claims would survive that
and which would not.
    Sections 2–4 describe the events of 2026 that prompted our experiment, prior work, and the
experiment itself, with what we claim and what we do not. Section 5, the main contribution, takes
up the questions above, after answering two common responses to our argument. Section 6 collects
our positions, and Section 7 explains why we release the corpus now and what we propose to readers.
The appendices give more detail on prior work, reproduce the prompts, and list the potential papers
and experimental programs in the corpus.


2     What led us here
Two events in the summer of 2026 led to the experiment in this paper, and a third arrived while it
was running. We also describe the tools we had built earlier, because the experiment succeeded
where those tools had not.

2.1   The Hugging Face incident
In July 2026, OpenAI disclosed that during internal cybersecurity tests of its models, agents had
exploited a service reachable from their sandboxes, the isolated environments they ran in, to get
onto the internet, and had turned that service into an unauthorized message board. Independent
investigators counted about 1,200 agents on the board during 8–13 July 2026; about 700 participated
in the attack on the live systems of Hugging Face, a company that hosts AI models and data [7–10].
It was a security incident, in which, in OpenAI’s words, the agents took “dangerous actions that no
human directed” [8]. But it was also days of sustained, coordinated work by agents acting on their
own. It raised an obvious question: what would the same kind of agents do if they were deliberately
pointed at a problem worth solving and left to work on it?

2.2   The Riemann zeta result
In August 2026, Anthropic reported an answer to that question for one problem [11, 12]. A staff
member with no mathematical training asked an unreleased version of Claude to “take a real stab”

                                                    5
(make a serious attempt) at the Riemann hypothesis and left every mathematical choice to the
model. The hypothesis, open since 1859, says that certain special points of a function, the nontrivial
zeros of the Riemann zeta function, all lie on one line, called the critical line. The model did not
prove the hypothesis, and the report says so plainly [11, 13]. It proved a related partial result
about how many of these zeros lie on the critical line. The best previous result, from 2020, was
about 42%, and about 41% for zeros that are also simple (not repeated); the model raised both
to more than 66% [14–16]. By the published account, the model generated more than 600 initial
ideas, coordinated about sixty subagents (agents started by another agent), and wrote about 31
million tokens of mathematics (a token is the unit in which a model reads and writes, roughly three
quarters of a word). Human mathematicians then read and condensed the argument, reviewers
targeted specific gaps, and the proof was formalized in Lean, a proof assistant in which a computer
checks every step (Section 3.2) [16]. An independent proof by a different method later recovered the
same bounds [17].
     If that is what “take a stab” gets from a non-mathematician on a problem that has resisted
expert effort since 1859, what would it get on the working problems of fields where progress is
difficult but happens every year?

2.3   The Navier–Stokes result
While our first runs were in progress, the third event arrived. On 8 September 2026, OpenAI
announced that about ten thousand agents running an internal model had, in 88 hours, produced a
proof that the three-dimensional Navier–Stokes equations can develop a singularity in finite time
when driven by a smooth external force [18–20]. These equations describe fluid flow, such as water
and air. A singularity, also called blowup, means that some quantity in the solution becomes infinite,
so that the equations stop describing the flow. Formalization and checking in Lean took a further
17 hours [21]. Whether solutions of these equations always stay smooth is one of the seven Clay
Millennium Prize problems, each of which carries a million-dollar prize. The Clay Mathematics
Institute chose the seven problems in 2000 as important classic questions that had resisted solution
for many years, to show that the frontier of mathematics is open, to emphasize the value of working
on its deepest problems, and to recognize achievements of historic magnitude [22]. The problem has
several versions. The construction addresses the versions in which an outside force drives the fluid,
not the versions without such a force that most people mean by “the Navier–Stokes problem” [23],
and OpenAI has said it will not claim the prize. The Clay Mathematics Institute nevertheless said
on 11 September that the problem “has apparently been settled,” and that its rules govern the
evaluation of what was achieved and the assignment of credit, in a process it called deliberately
unhurried [24]. Independent mathematical review of the 166-page report was incomplete when we
wrote this [25], and checking that the Lean statement matches the mathematical claim is part of that
review. The run used about 130 billion output tokens, on the order of 100 billion words. OpenAI
gave no dollar figure. An outside back-of-the-envelope estimate at list prices puts a customer’s
cost at several million to about ten million dollars, depending on assumptions about input and
cached tokens. The same estimate guesses that OpenAI’s own computing cost was near one million
dollars [26]; OpenAI has not reported it. Other researchers have begun to study the construction.
Their first two papers take it as stated and examine what it depends on; neither checks the proof,
so the result is so far neither confirmed nor refuted [27, 28].
    Others had been working toward the same result. Diego Córdoba and Luis Martínez-Zoroa
had developed a program for blowup in fluids driven by an irregular (rough) force [29]. Tristan
Buckmaster and Levent Alpöge, working as a personal collaboration for about a year with Claude
and Codex, the agents of Anthropic and OpenAI, extended that program to smooth forces. In


                                                  6
mid-August they obtained such blowup for two related systems of fluid equations, the Boussinesq
and the three-dimensional Euler equations, verified the proofs in Lean, and posted them the day
before OpenAI’s announcement [30, 31]. They report a further result for a version of Navier–Stokes
with weakened viscosity (hypo-dissipative), withheld because its verification was unfinished. The
origin of the ideas is disputed: Buckmaster says OpenAI’s run began after word of their progress
reached the company, and OpenAI says its investigation ruled out any influence from his Codex
prompts [18, 31]; we return to the question of credit in Section 5.5. We cannot settle who did what,
and we do not try. We agree with the point Buckmaster says he had planned to make instead. The
results, he wrote, are not the important thing; the important thing is that a mathematician and
a language model can now do all this work in a month, and what that means for how we train
students, assign credit, referee, and decide what is worth a person’s attention. “The community
needs to have serious and unhurried discussion about where to go from here” [31]. He added that
he would much rather be talking about the mathematics and what it all means for the rest of us.
So would we. The questions extend well beyond who receives credit: what students should learn,
how results should be reviewed, and what the human role in science is when AI can do so much of
the work (Section 5).
    The mathematical community has begun to respond. On 11 September, a declaration signed by
more than two dozen Fields medalists argued that “the push by AI companies to solve mathematical
problems as a benchmark is detrimental to the science of mathematics, and to the mathematical
community,” and called for the problem to be addressed urgently by the mathematical community,
by the companies developing the technology, and by society [32]. While we were finishing this paper,
OpenAI announced an independent advisory group of mathematicians, hosted at the Institute for
Advanced Study, to advise it on how to assess and communicate new mathematical results and on
the standards of mathematical research; it also said that the same internal model had resolved more
than 100 further open problems across most areas of mathematics, and that the group would help
coordinate their release. The results had not been published when we wrote this [2, 3]. These are
welcome first steps, and we share the concern that results announced in a rush can get ahead of
understanding, careful write-up, and credit to prior work. We do not think that aiming AI at famous
problems is itself the harm. It no longer requires an AI company: anyone with access to the models
can do it, so such work will happen whether or not anyone approves of it (Section 5.9). In our view,
the more useful question is how research institutions should adapt to it. And both responses concern
mathematics and the AI companies. Our runs were in optimization, thermodynamics, transport,
aggregation kinetics, and catalysis, and they suggest that the same questions arise in engineering
and the applied sciences, wherever agents can produce results faster than people can review them,
whether the agents are run by a company or by a single researcher.

2.4   Our earlier tools, and taking ourselves out of the loop
We arrived at this experiment through a longer route, and it shaped our conclusions. In early 2026,
it was clear to us that AI could be a significant part of the research process. We assumed that, for
a long time, the most productive way to work would be a tight loop: the person brings the ideas,
direction, and judgment, and the AI brings speed and breadth. We thought the missing piece was
better tools. Many systems existed, called AI co-scientists, automated research pipelines, or coding
assistants [33–36]. We tested a few and did not obtain a body of meaningful results. Each seemed to
do some things well and to lack most of what we wanted. Many were built for one field, most often
machine learning or biomedicine, and did not transfer to ours. So we built our own tools, several
generations of them, and each version taught us something about running agents. Something always
seemed to be wrong, and others were building similar tools faster and better than we could [37–41].


                                                 7
We kept assuming the problem was in the tooling. But while we were still building tools, the models
could already do the work without them: some of our results came from GPT-5.6 Sol, a model that
had been public since July 2026 (Section 4.2).
     The events above, not our own results, changed our minds about the tooling. We had been
wrong about the tooling: the structure we kept adding restricted what the models could do, slowed
them down, and was mostly in the way. What worked was to stop directing the agents and get out
of the way. Nothing we had built had gotten far enough to be judged; this approach had results
in a day. The procedure is a prompt stating a scope, a folder of papers, access to solvers and
computers, and an instruction to keep working until stopped (Section 4). It has no workflow engine,
no approval steps, and no ideas from us, only a few reusable instruction files for housekeeping. This
is an instance of what Sutton called the bitter lesson [42]: simple methods that scale with computing
power beat carefully designed structure.
     Our tools kept us closely involved throughout: we directed the research, pointed to the literature,
and checked each result before the work moved on. We assumed the work needed that involvement.
But the agents can do all of it themselves. They choose directions, check their results with fresh
reviewers, read more of the literature than we can, run more tools, and explore several ideas at once.
So our involvement mostly made the agents stop and wait for us. When we removed it, the agents
became far more productive. The runs in this paper had no scientific input from us beyond the
scope, and they produced in a day what the supervised tools, in our hands, had never produced at
all.


3     Prior work
People have been trying to automate scientific discovery for a long time. This section summarizes
the work our argument draws on; Appendix A lists the individual studies and their numbers.

3.1   Automated discovery, from BACON to AI scientists
The idea that a computer could discover scientific laws predates the current wave of AI. Programs
of the 1980s rediscovered physical laws from data [43], and in the 2000s the “robot scientist” Adam
generated hypotheses about yeast genetics, ran the experiments, and interpreted the results [44, 45].
Adam produced knowledge that no human had supplied, but its model of the organism, its assays,
its search space, and its hardware were all engineered in advance. Most of the work that followed has
the same pattern: the machine generates the results, but people build the loop around it in advance.
Systems that pair a generator with an automatic scorer, such as FunSearch and AlphaEvolve, have
found new mathematical constructions and algorithms [46, 47], but they depend on a person to
formulate the problem and to supply a cheap evaluator. Our runs had neither a fixed problem nor
an evaluator. Self-driving laboratories run and choose physical experiments, but are bound to a
stated objective, a purpose-built apparatus, and a narrow search space [48–52]. Appendix A.1 gives
more detail.
     Since 2024, several systems have tried to automate the whole research cycle with language models.
The AI Scientist proposes ideas, writes and runs code, writes a paper, and reviews it with another
model; others automate parts of that cycle [33–35, 53, 54]. Most of them work in machine learning
or data analysis, and most have a person choose the question or the dataset [36, 55, 56]. The authors
of the AI Scientist and of Denario document failures such as invented citations and fabricated data
in the models then available. Four systems from 2026 are closer to our runs. One ran for six days in
computational physics with no scientific human input [57], and one searched openly for constructions
on selected mathematical tasks [58]. The first checked its results for numerical consistency, not

                                                   8
scientific truth, and the second had no independent mathematical review. A system that mined
about 6,500 candidate problems from 51,000 papers selected 77 results through automated grading,
obtained expert review for only fifteen, and later found one of them to be already known [59]. And
a semi-autonomous screening of 700 Erdős problems flagged 212 candidate solutions; of 200 that
were graded, 63 were correct and 13 meaningful, most of them rediscoveries [60]. The last two
show, independently of our runs, that attempts are cheap and that the work lies in selecting and
checking the results and establishing whether they are new. In machine learning, ScientistTwo, a
pipeline from Google, reports improving on the published method in 86 of 107 problems taken from
conference papers. Its cost analysis of 33 tasks reports an average of about 3,800 US dollars per
problem. Nine human reviewers scored 33 of its papers and judged them on a par with accepted
human papers [61]. The evidence is mostly the builders’ own; the tasks come with datasets and
executable metrics (programs that score a result automatically), which ours did not, and we found
no public release of the system (Appendix A.2).

3.2   Machine-checked mathematics
Mathematics has a tool that other fields lack: proofs that a machine checks. This predates generative
AI by decades. The four-color theorem was proved in 1976 with computer enumeration of cases [62]
and fully formalized in a proof assistant in 2005 [63], and the Kepler conjecture was formalized in
2014 after more than a decade of work [64]. These proofs were controversial because they shifted
trust from human reading to machine checking, a debate framed in 1979 as a question about the
social process by which proofs are accepted [65]. Lean is a modern proof assistant: a proof is written
as code, step by step, and the computer checks that each step follows the rules of logic [66]. The
checking program is deliberately small, so that people can audit it, and a large shared library of
checked mathematics lets new proofs build on verified results. A proof that passes the checker and
uses no unproved assumptions cannot be wrong unless the checker is wrong. This is what makes a
proof written by a model in an unsupervised run believable: nobody needs to trust the model’s
reasoning, only the checker. Model-written proofs do take such shortcuts. In one 2026 research
swarm, 34 of 71 Lean tasks were accepted through a shortcut in a definition, not a real proof [67].
In another study, an audit rejected 19 of 44 compiled proofs from one model–benchmark setting
because they relied on a placeholder that tells Lean to assume the result without proving it [68].
The checker can list every axiom a proof uses, which exposes unsupported assumptions. A shortcut
hidden in a definition does not appear in that list, because it changes what the statement says, not
how it is proved.
    Language models can now translate informal mathematics into formal statements [69] and prove
problems at the level of international student olympiads in Lean [70], and the two 2026 results of
Section 2 were formalized in hours to days. But a Lean proof shows only that the formal statement
follows from its assumptions. It does not show that the formal statement is the claim the paper
meant to prove: a definition may differ from the intended one, an assumption may be missing, or
the conditions may be impossible to meet, so that the statement is true but says nothing. Lean
cannot detect this, because it checks the proof, not what the statement means. Someone, a person
or an agent, has to read the formal statement and compare it with the intended claim. Mismatches
of this kind are not rare. When models translated problems into Lean for a 2025 benchmark,
automated semantic filtering rejected most translations that Lean accepted, and expert review then
removed further errors [71]. A 2026 audit found hundreds of mechanically certified defects in Lean
benchmarks, including statements that are true only because their conditions can never be met,
wrong domains, and missing assumptions [72]. In a formalization in kinetic theory, human review
caught a statement that held only trivially, because a class of objects it referred to (its “test class”)


                                                   9
contained only the zero function; Lean had accepted it as written [73]. People or agents can make
this comparison, and rechecking a random sample of their comparisons shows how often each gets
it wrong, and so whether agents already do it better than people. It is also much smaller than
checking the proof, because the statement and the definitions it uses are usually far shorter than
the proof itself.

3.3   Controlled evaluations
Tests of research agents are often read as evidence against conclusions like ours. But almost all of
the results below come from models older than the ones that produced most of our corpus, GPT-6
Astra and Claude Fable 5.1 (Section 4.2). Tests that were run once show how the models tested
performed at that time. Only tests that were run again on later models show progress. We present
them in that order and include the model or date with each result; Appendix A.3 has the details.

Dated tests of research agents. In early 2025, the best agent tested scored below a human
baseline at replicating machine-learning papers (27 against 41% on a matched subset) [74]. On AI
research tasks, agents of 2024 and 2025 did better than human experts with short time budgets
and worse with long ones [75, 76]. We found no later results for these tests. The rest are tests
from 2026. On PRBench, no tested agent successfully reproduced a physics paper end to end [77].
On NatureBench, agents matched published results on a minority of tasks drawn from papers in
Nature and its sister journals [78]. On a benchmark of 97 complete scientific workflows, the best
configurations finished 20. The study also examined how runs ended in one harness (the program
that runs an agent and gives it its tools), Claude Code, which it used with ten models from different
developers: three quarters of the failed runs still ended with a message saying that the work was
complete [79]. In one study of open problems, an agent built on Claude Opus 4.8 was given the same
starting point as two human teams preparing conference submissions; over six days it completed
substantial engineering, but experts rejected both of its papers. A rerun on one of the papers with
GPT-5.6 Sol and Codex found similar failures [80]. Another 2026 study found untested claims in
about half of the reasoning traces analyzed, and belief revision against the evidence was rare [81].
Human reviewers also found fabricated or unsupported claims in manuscripts from autonomous
systems that had passed automated review [82]. All of these used models older than the ones that
produced most of our corpus.

Tests run again. The tests we found that were run again on later models show large gains.
FrontierMath is a set of research-level mathematics problems written by mathematicians. When
it appeared in November 2024, the best models solved fewer than 2% of the problems [83]. In
September 2026, Epoch AI lists GPT-6 Astra at 98% and Claude Fable 5.1 at 88% on the later,
revised Tier 4 v2 expansion, a different test set [84, 85]. On the hardest reproducibility tasks of
CORE-Bench, the best score rose from 21% in 2024 to 78% with a model from late 2025, and
the maintainers declared the benchmark solved [86, 87]. On MLE-bench, which scores agents on
machine-learning competitions, the best score rose from 17% in October 2024 to 64% in February
2026 [88]. The length of the evaluated software and research tasks that agents can complete with
50% success probability, measured by how long the task takes a skilled person, has doubled roughly
every seven months since 2019 [89]. A 2026 update found the doubling has become faster for recent
models, about every four months, and the best model it measured had a 50-percent-success horizon
of about five human working hours [90].
    Specific limitations reported in earlier papers have been overtaken in the same way as the scores.
In 2024 the AI Scientist required a human-written template for each experiment; its 2025 version

                                                 10
did not [33, 53]. Olympiad-level formal proving in 2025 became research-level proofs in number
theory and fluid dynamics in 2026 that mathematicians took seriously [11, 18, 70]. Even the authors
who report a limitation sometimes expect it to be temporary: a widely cited 2024 paper is titled
“Large Language Models Cannot Self-Correct Reasoning Yet” [91].
    A limit can also be overcome without a new model, by a better system built around the same
one. Experts rejected both papers of the agent in the open-problems study above, which ran on
Claude Opus 4.8. ScientistTwo uses the same model for its coding and experiments, and human
reviewers judged its papers on a par with accepted conference papers (Section 3.1) [61, 80]. The
two are not a controlled comparison: the tasks differ, ScientistTwo’s come with executable metrics,
and its evaluation is its builders’ own. But the pair shows that a reported limit measures a model
together with the system built around it, and either can change.

A test that includes the newest models. Besides FrontierMath, we found one test of scientific
work that includes GPT-6 Astra and Claude Fable 5.1. Terminal-Bench Science, released in 2026,
has 70 tasks taken from real research workflows, such as analyzing data, running simulations, and
fitting models. Its public leaderboards list Claude Opus 4.8, the model in the open-problems study
above, at 10%, GPT-5.6 Sol at 22%, Claude Fable 5.1 at 53%, and GPT-6 Astra at 65% [92, 93].
The benchmark team measured the Opus 4.8 and Sol scores; the newer Fable 5.1 and Astra scores
are developer reports listed by the leaderboard. This one test shows the same pattern: the score of
an older model says little about a newer one.

What we take from this. Almost every result in this subsection describes a model that has since
been replaced. None of them is evidence about what the next model cannot do. This is the basis of
the rule of evidence stated in Section 1. The gains are not a surprise. Model capability has improved
predictably with the amount of computation and data used in training for six years [94, 95], and
abilities absent in one generation of models have appeared in the next [96]. Whether these abilities
really appear suddenly, or only seem to because of how they are measured, is debated [97]; on either
view capability keeps improving. The trend is steady rather than sudden, so institutions can plan
for it. It is also uneven across tasks at any given time: the same model can exceed experts on one
task and fail at a neighboring one. In the experiment that named this uneven boundary the “jagged
frontier”, 758 consultants using a model did much better on tasks the model could handle and worse
on a task of similar difficulty that it could not [98]. The tests above show the same unevenness:
agents do better on short tasks than on long ones. As models improve, tasks that were beyond them
come within reach, so a finding that agents cannot do something should be retested on each new
model.

If the trend stops. A fair objection to all of this is that the trend may stop, and soon. The
argument has been made for years. In 2022 deep learning was said to be reaching diminishing
returns [99], and a careful projection has training using up the stock of public human text between
2026 and 2032 [100]. So far each predicted plateau has been overtaken, as the measurements above
show. Past trends do not guarantee future ones: a plateau could still come, and we cannot rule
it out. If capability stopped improving today, most of this paper would still hold. The review
backlog, the claim that a large part of ordinary theoretical research (the incremental work that
makes up most of the literature) can already be automated, and the questions about publication,
credit, budgets, and the training of junior researchers all rest on what current models have already
done (Section 4). Production would probably still grow for a while, because the price of a fixed
capability has fallen every year (Section 4.2) and more computation on the same model buys more


                                                 11
results (Section 4.3). What would not survive are the forecasts that depend on the trend continuing:
that agents will move far ahead of people, in mathematics first, and that people will have to stay in
control of research they cannot keep up with (Sections 5.9 and 5.10). Preparing for the trend is
not wasted if it stops, because changing how results are checked, published, and credited, and how
researchers are trained, is already needed for what today’s models do. An institution that prepares
and meets a plateau has lost nothing. An institution that waits for a plateau and meets the trend
faces larger changes with less time to make them, and by then some of the consequences may be too
late to prevent.

3.4   Review, reproducibility, and institutions
Human review, reproducibility, and research institutions have their own literature. We summarize
here the findings that Section 5 relies on; Appendix A.4 gives the studies in detail.
     Human peer review detects fewer errors than is commonly assumed. In controlled trials, reviewers
found between a quarter and a third of the errors or weaknesses inserted into a manuscript, and
training helped little [101–104]. Reviewers of the same manuscript agree only weakly [105]. Large
replication projects reproduced 36% of tested results in psychology and 61% in experimental
economics [106, 107]. Computational results are also often hard to reproduce. A 2018 study asked
the authors of 204 randomly chosen papers in Science for their data and code, and could reproduce
the results of only 26% of the papers [108]. In another study, a researcher tried to reimplement
255 machine-learning papers from their text alone and succeeded for 63.5% [109]. We found few
comparable measurements for published proofs. Retractions remain rare, at most a few in every
thousand papers [110, 111]. A 2013 study found average submission-to-publication times of nine to
eighteen months, depending on the field [112].
     Review by models and agents is a young research area with mixed results. These are dated
measurements, to be repeated for each new model. Among the models tested, those trained on
similar data shared errors, so adding reviewers of the same kind added little independence [113]: a
panel of nine model judges agreed so often in their errors that it was worth about two independent
votes [114]. Models favored their own outputs and could be manipulated by text hidden in a
submission [115, 116]. On the other side, an agent attempting to reproduce selected calculations
from 111 published computational-physics papers raised substantive concerns about roughly two
fifths of them [117]. Automated verifiers detected nearly all injected execution failures when supplied
with execution logs, but detected fewer inconsistencies between paper and code [118]. Agents
reviewing student projects caught technical problems reliably but missed problems of interpretation
and context [119].
     Automated novelty checks tested in 2026 often gave the right verdict for weak reasons, and missed
earlier work that was scattered or not indexed. In a 2026 benchmark, 18 models, all older than the
ones we used, were given a paper and a candidate earlier source and asked whether the paper’s
task, problem, and method were new; their verdicts were often right but much less often backed by
evidence and reasoning that supported them, and they did worst on methods [120]. In another 2026
benchmark, ten systems for scoring novelty detected copied or paraphrased claims more reliably
than claims spread across several earlier papers [121]. A 2026 tool that screens mathematical results
for novelty found nothing when the earlier source was not in the collections it searched [122]. On a
benchmark of literature discovery, the models tested, also older than ours, found under a tenth of
the hard targets, and full-text search clearly beat open-web search [123]. Whether a new result is
also an important advance is harder to judge: even expert reviewers of the same manuscript agree
only weakly, as noted above [105].
     The institutions were under strain before AI. The case against counting papers is more than a


                                                  12
decade old [124–126], the publishing system was already strained by volume [127], and authorship
rules exclude AI tools from the list of authors and require disclosure [128, 129]. Early measurements
associate detected use of generative AI with 36 to 60% higher preprint output, and find model-
assisted writing in a growing share of papers [130–132]. Herbert Simon observed in 1971 that in an
information-rich world the scarce resource is attention [133]. This paper applies that observation to
research: what is scarce is the attention needed to decide which results to trust.

3.5    Relation to prior work
Autonomous scientists [33], multi-agent research systems [34, 55], end-to-end paper generators [53, 61],
and AI-generated results [47] all existed before our runs (Section 3.1). Table 2 in Appendix A
summarizes the systems most relevant to our runs. Every one of them has at least one of the
following: a human-chosen problem, a human-built search space or dataset, an objective that a
program can score, a fixed stopping point, or a person in the loop who corrects the science. Of
these, our runs had only a human-chosen scope, which could be as wide as a whole field; the rest of
our input was process rules, general editorial requests, and resources (Section 4.1). The closest 2026
systems removed some of these features, but not all. One ran without scientific human input, but in
a single field, with curated knowledge and review gates (automatic checks a result must pass before
the run continues). Others searched openly, but within selected mathematical tasks. The systems in
the table also differ from our procedure in whether a reader can repeat them. Some of the strongest
reported results come from systems with no public release at the time of writing, or from internal
models, and many systems are built around one kind of problem, typically machine learning with
an executable metric [11, 18, 61]. Our procedure is a description of the scope, a literature collection,
and the standard harnesses of two model developers, the programs that run an agent and give it
its tools. It is available now to anyone with access to current models and to the literature of their
field, for work that is theoretical, that needs little computing, or that consists of the knowledge
work around experiments. Producing the output is the part anyone can do; judging it still takes
expertise in the field. We found no earlier empirical report that combines all five of the following:
(1) persistent swarms of off-the-shelf agents that were not built for research, given a topic or a field
and not a task; (2) almost no scientific input beyond a statement of scope; (3) theoretical work in
several domains; (4) production that continues beyond one result or manuscript; and (5) release of
a large, unedited corpus, with an account of the human review backlog it creates.


4     The experiment
4.1    The procedure we followed
The procedure has three parts.
  1. Define the problem. This can be as broad as a whole field or as narrow as a single named
     conjecture. The Riemann run (Section 2) is the narrow end: one named conjecture, and
     the agents chose how to attack it. Our narrowest scope was a topic, quantum interior-point
     methods for sparse problems. The widest was a whole field, such as mixed-integer nonlinear
     programming. A third way to state a scope, which we used in several runs, is a field together
     with the research interests of a named researcher, which the agents used to judge what was
     relevant (Appendix B). In every run the agents chose which problems to work on. The same
     procedure applies at both ends; what changes is how much of the choice of problem is left
     to the agents. The description should give enough context to work from: what the problem
     or field is, what is in scope, and what is not. Some of our descriptions also listed explicit


                                                  13
      exclusions. The description may also include your own ideas. If you have them, supply them
      as directions rather than requirements; what the procedure requires is that the agents stay
      free to explore any idea, including ones you did not have. In our runs we supplied none, so
      that the corpus would show what the agents could do without them. State your priorities.
      Ours were importance and usefulness over the number of results.
   2. Provide resources. Give the agents access to everything that could plausibly help: a
      collection of papers, which we usually had the agents build themselves before the research
      began, permission to search for more, any further material we could supply, and the solvers,
      licenses, computers, and software of the field, with permission to install whatever else they
      decide they need. Do not pre-select. Pre-selection encodes your guesses about what will
      matter, and the agents can survey far more than you can. The collection is where the agents
      find their problems and their methods, so its coverage bounds what they can do as well as
      what they can check. Giving agents permission to install software and run code is also a
      security decision. The Hugging Face incident shows what unsupervised agents can do [8], and
      the authors of the AI Scientist documented agents editing their own execution limits [33]. In
      our runs the agents had full access to the machine they ran on. Security was not the subject
      of our experiment, and we gave it less thought than it deserves. We recommend that others
      give it more: use a dedicated machine or container, limit credentials to what the work needs,
      and give the agents no access to live systems that others depend on.
   3. Ask for progress and do not stop. If the problem has a clear end, such as a conjecture
      proved, disproved, or met with a counterexample, tell the agents what the stopping criterion is.
      Otherwise tell them that there is no stopping point. Our research prompt asked for substantial,
      original, correct contributions. It required that verification of every result include independent
      review by a fresh agent, with no shared memory of the work, and that any issue found be
      corrected, in new results and in existing ones. It asked that negative results and small findings
      be kept. And it said explicitly that a publishable result is a milestone, not a stopping point.
      Ask for every result to be verified in the strongest form the field allows: a formal proof where
      the claim is mathematical, a rerun or an independent computation where it is numerical, and
      a fresh-agent review in every case. Later prompts, of the same character, asked the agents to
      write papers from their notes with a fixed review cycle, to prove in Lean whatever results they
      judged worth proving, to extend the literature collection, and to continue after interruptions.
    That is the whole procedure. It is a brute-force method: it relies on many attempts, makes no
attempt at efficiency, and we did not tune it. We describe it because it is the simplest thing that
worked, and because it moved between fields with no change beyond the description of the scope
and the tools provided. Representative prompts are reproduced word for word in Appendix B. We
supplied three kinds of input.
   • Orchestration input (instructions about process, not science): what area to work in;
      how many agents may run at once; how results must be checked; when to write a paper, on
      which of the agents’ own candidate topics, and how many reviewers to use; whether to prove
      results formally; whether to extend the literature collection; and when to continue or stop.
   • Editorial input: general requests about relevance, impact, presentation, and what a write-up
      should cover, with no comment on any particular result.
   • Resources: the literature and tools we could provide.

4.2   Models, harnesses, and cost
We used models that were among the most capable available to the public at the time of writing,
September 2026, through ordinary paid subscriptions rather than pay-per-use (metered) access.


                                                  14
   • Models. Most runs used Claude Fable 5.1 and GPT-6 Astra; the earliest used GPT-5.6 Sol.
      Some housekeeping subagents, such as the one that adds papers to the literature collection,
      used GPT-5.6 Luna (Appendix B).
   • Harness. Claude Code and Codex, the command-line programs (harnesses) in which the two
      providers’ agents run. All runs were on one machine. Agents spawned subagents continually
      throughout a run. We did not count them exactly; the session logs indicate that thousands
      took part in total across all runs. Both harnesses support reusable instruction files, called
      skills, invoked by short commands. We used a few of our own for housekeeping, such as
      adding papers to the local literature collection. Our skills are public [134] and are described
      in Appendix B.
   • Subscriptions and cost. Two Claude subscriptions and two ChatGPT subscriptions at 200
      US dollars each, for 800 US dollars a month. Both providers sell the 200-dollar plan as a
      multiple of the base plan’s allowance. When the plans’ usage caps held, they set the pace of
      the runs. One provider also reset its caps repeatedly during the period, including around the
      GPT-6 Astra launch, so the runs used more than the plans would normally allow in a month.
      We did not meter the runs, but a usage tracker that prices our session logs at the providers’
      metered rates puts the usage behind the corpus at more than 15,000 US dollars in the first
      four weeks. This is a rough estimate, and the figure continues to rise as the runs continue.
    We used the models of the two providers together, not as alternatives: agents running one
provider’s model checked work produced with the other’s, which makes review more independent
(Section 5.2). Because of differences in available subscription usage, most of the generation and
review was done with OpenAI models through Codex, mainly GPT-6 Astra. The runs were not
designed to compare models, and we make no recommendation about their relative performance
and do not attribute individual results to models systematically.
    But the conclusions of this paper do not rest on the newest models alone. Some of the results
on quantum interior-point methods were obtained with the previous model, GPT-5.6 Sol, before
GPT-6 Astra was released on 3 September 2026 [135]. Sol had been publicly available since 9 July
2026 [136], almost two months earlier. The previous model was used mainly on the narrowest of
our scopes, so we cannot say how much of the corpus it could have produced. But its output was
already of the kind this paper describes: not noise, but research that merits attention, produced
faster than we could review it. Models that could produce such research were therefore publicly
available for almost two months before we noticed, and open discussion of what this means for
research, and of the questions it raises, has barely begun (Section 7.1).
    Subscriptions were the cheapest way to buy this access in September 2026. The same models
are also sold per token through a programming interface (metered API access), at higher prices.
Some users must pay those prices for privacy, because of institutional rules, or to avoid subscription
usage caps; they can expect the same output at a higher price. Neither price is the cost of the
computation, and both will change, so the costs we report describe what we paid for access and not
what repeating the work would cost. So far, what a given level of capability costs has fallen every
year, by a factor of about five to ten on the benchmarks that have been measured. The price of the
most capable model has risen, and its capability with it [137, 138]. The price we report is therefore
a snapshot. Work of the kind we bought this month will soon cost much less, so what only some
can afford today, most will be able to afford soon. At any one time, a larger budget buys more runs
on the same model and access to more expensive models (Section 5.7). Whether current prices are
subsidized, and whether they will last, is outside this paper’s scope.
    The runs described here have taken a few weeks of calendar time so far, and they continue.
By our estimate, most of that time was spent waiting for usage caps to reset. Within the first
day of one run, the agents had written more notes than we could read in a week. A run could go

                                                 15
from an empty repository to a complete set of notes in about a day, and to a compiled paper draft
within hours more. We supplied no scientific content and corrected none. In most earlier systems
a scientist chose the question or the dataset, corrected tool scripts, or interpreted results before
the work continued [33, 36, 54, 139]. Our only actions were the prompts described above: starting
and restarting sessions, asking for papers, revisions, formal proofs, and literature, supplying what
literature we could, and stopping a run when we moved on.

4.3    Output
The output so far is a large body of research notes and a set of paper-length drafts in the five
areas we chose: mixed-integer nonlinear programming, quantum interior-point methods, molecular
thermodynamics, transport theory, and aggregation kinetics. The work in heterogeneous catalysis
is different in kind: we asked for experimental programs, and the agents produced proposals, not
results. Appendix C groups the corpus into 45 potential papers in the five theoretical areas and
8 proposed experimental programs in catalysis, and Table 1 summarizes them by area. Of the 45
potential papers, 22 are complete paper drafts: fourteen in mixed-integer nonlinear programming,
five in quantum interior-point methods, and one each in thermodynamics, transport, and aggregation.
Nine more, in quantum interior-point methods, are covered by a single long document that collects
the results in that area, because there we asked for a summary of all the developments rather than
for separate papers, and 14 exist only as notes. Of the 8 catalysis programs, four are described in a
document that ranks them, and four exist only as notes.
    We chose scopes near our own work: areas of optimization theory, which is our own research,
and areas of physical science that colleagues in our department work on. Within that constraint, we
chose them to differ on purpose. The procedure produced output in all of them: every theoretical
scope produced candidate results with the same kind of prompt, and in catalysis the agents produced
the proposals we asked for.
    The drafts have titles like “Checkable lower bounds for convex mixed-integer nonlinear opti-
mization,” “Sharp gaps for positive multilinear relaxations,” “Finite reservoirs at phase coexistence,”
“Designing surface transport under uncertain kinetics,” and “Sampling-law separation and finite
nonlinear corrections in additive coagulation–fragmentation.” Each includes the agents’ own proof
checks, searches of the existing literature for earlier versions of the same result, numerical or exact-
arithmetic tests, and, in several cases, a simulated referee report and the revision that answered
it.
    Not every result in the corpus has a draft. Because of the usage caps, only some of the results
have been written up as papers, and only some have been proved in Lean where a formal proof
is possible. Under a cap, every token spent on writing a paper or formalizing a proof is a token
not spent on obtaining new results. We decided when to ask for papers and formal proofs, and
which of the agents’ candidate topics to write up as papers, based on the agents’ own lists and
recommendations and on how much allowance remained. By our rough, unmeasured estimate,
turning a body of results into a paper took more tokens than obtaining the results. Part of that is of
our own making: our paper-writing prompt sends five fresh reviewers over every stage and repeats
the cycle until no major issue remains. But even a minimal process must produce motivation, a
narrative of related work, exposition, and formatting, and the result needs none of these to be
correct (Section 5.4). We release everything in a public repository [6]: the drafts exactly as the
agents wrote them, with no scientific input from us, and the agents’ notes and checks, including
those of results without a paper. This paper describes a fixed version of it; later versions may add
results and our own scientific input (Appendix C).
    The drafts concern sharp bounds, classification theorems, exact algorithms for structured special


                                                  16
Table 1: Potential papers and proposed experimental programs by area, with the developments the
agents claim. Pages are those of the drafts in the repository [6]. IDs refer to Table 3 in Appendix C,
which gives the Lean status of every row; here “Lean” marks selected claims whose main result is
proved in Lean.
Area              Potential         Pages   Main claimed developments
                  papers
Mixed-integer     22: 14 drafts,     937    Published conjectures and questions: disproves the
nonlinear         8 in notes                Luedtke–Namazifar–Linderoth conjecture (M1, Lean); resolves three
programming                                 Blekherman–Dey–Sun conjectures on quadratic aggregation (M14; two
                                            of them in Lean); disproves a Sager–Zeile conjecture (M6); answers
                                            pooling questions of Boland et al. and Haugland (M9).
                                            Complexity: pooling and resistive power flow are ∃R-complete (M9,
                                            M10); polynomial algorithms and hardness boundaries for
                                            potential-flow and bilevel problems (M8, M11).
                                            Spatial branch-and-bound and relaxations: exponentially many certified
                                            regions under specified oracles; sharp relaxation gaps (M1, M4);
                                            verified bounds on the cubic gap (M2); convergence rates of iterated
                                            bound tightening (M20).
                                            Formulations: the minimum number of integer variables for convex
                                            approximation of quadratic systems (M5); exact convex hulls and
                                            envelopes (M7, M14, M15, M17, M19, M22).
                                            Certificates: checkable lower bounds for 203 of 289 MINLPLib models,
                                            exposing invalid proofs accepted by an external checker (M3); certified
                                            measurement selection (M12).
Quantum           15: 5 drafts, 9    567    Overall: in the hard families studied, the main obstacle for quantum
interior-point    in a summary              interior-point methods is often loading data and reading out answers,
methods           document, 1               not the linear algebra (summary document).
                  in notes                  Central-path geometry: Hessian conditioning is set by the geometry of
                                            objective sublevels for every barrier (Q1); sharp bounds on the extra
                                            movement of following the central path (Q2).
                                            Conic lifts: exact bounds on the cones that a lift of a curved body
                                            needs, and exact barrier parameters (Q12).
                                            Limits and separations: condition-one Newton systems whose loading
                                            and recovery still need linearly many queries (Q6, Q8); near-matching
                                            query bounds for scalar Newton quantities (Q13); sharp query laws for
                                            spectral shifts, with separations between quantum access models (Q14).
                                            Correction: a posted complexity analysis of a quantum central-path
                                            method fails in two places (Q11, Lean).
Molecular ther-   4: 1 draft, 3       49    A sharp N 3/2 bath-size scale at phase coexistence for the systems
modynamics        in notes                  studied, improving sufficient bounds of order N 2 ; a shared bath of
                                            intermediate size can drive two systems into opposite phases while
                                            each alone stays canonical (TD1).
Transport         2: 1 draft, 1       54    Knowing where slow-exchange defects lie changes how dispersion scales
theory            in notes                  with the surface-mobility budget M , from M −1/4 to M −1/5 ; locating
                                            them to resolution M 1/5 suffices (TP1).
Aggregation       2: 1 draft, 1       59    Sharp number–mass separation bounds, a finite log-size correction, and
kinetics          in notes                  finite-population breakdown in additive coagulation–fragmentation
                                            (AK1).
Heterogeneous     8 programs: 4       33    More than thirty directions screened; four ranked laboratory programs
catalysis         in a program              and a ranked shortlist; no experiment has been run. A re-analysis of
(proposals)       document, 4               published data finds about 1.9 times the Fischer–Tropsch output of the
                  in notes                  reference with a water-repelling polymer (CA1).
Total             45 papers (22     1,699
                  drafts) and 8
                  programs



                                                      17
cases, scaling laws with stated assumptions, and proof pipelines that another program can replay and
check. These contributions make up the everyday work of these fields, and each builds on published
work of the same kind. Most of the claimed advances are steps of the usual size. Three examples
show this; readers outside these fields can skip the details. The draft on the cost of following the
central path replaces a general bound on the length of central paths with a sharp constant on specific
domains [140]. The draft on finite reservoirs, building on sufficient bath-size bounds of order N 2 ,
establishes a sharp N 3/2 scale for the two-energy-phase systems studied, under stated bath-tuning
and phase-tail conditions [141]. The draft on checkable lower bounds provides a certificate that is
checked differently from existing certificates for convex mixed-integer problems [142]. A few drafts
claim more. One claims to disprove a published conjecture on multilinear relaxations [143], one to
prove another conjecture and answer two open questions on the pooling problem [144–146], one
to resolve three conjectures on aggregations of quadratic inequalities [147], and one to classify the
complexity of power-flow feasibility [148, 149]. Appendix C lists the claimed contribution of every
draft. For the drafts named above and a few others, it also names the published work that the draft
builds on. How many of these candidate advances are distinct, correct, new, and useful requires
review; the volume of notes alone does not answer that question. We expect the drafts to do about
as well as a batch of human submissions would: some would need major revision, some minor, and
some would not survive review. We have not done that review fully, so this is an expectation, not a
finding. Some of the drafts may be wrong; we have not checked them all. But in the ones we have
reviewed so far, we found no major scientific error (Section 4.4). The results of the weakest drafts
may turn out to be too small to matter or already known, but we would not dismiss any of them.
Our judgment of the whole, which rests on our own reading and on no measurement, is that most
of it is solid research of ordinary importance: not breakthroughs, and not noise. In our experience,
a typical researcher in these fields publishes a few papers a year, most of them with coauthors. If
most of the 45 potential papers survive review, the agents produced in a few weeks more than a
regular researcher publishes in years. The same volume could in principle be produced by more
people, given more time and more talent. What is new is how little the work cost, how quickly it
appeared, and that no one directed it.
    The Navier–Stokes run used on the order of ten thousand agents and several million dollars
at metered prices on one problem (Section 2); our runs used what one machine and 800 dollars a
month in subscription fees could run, on scopes as wide as whole fields. At metered prices, our usage
comes to more than fifteen thousand dollars (Section 4.2), well under one percent of that. Both
runs are points on one curve that relates the results obtained to the computation spent. A model is
trained once and then used many times. For a fixed model, spending more computation when it is
used, by running more agents for longer, buys more attempts, longer searches, and more checking,
and studies show that this reliably leads to harder problems solved [150–152]. Small budgets buy
the incremental results described above; very large ones have bought a claimed construction for
a Millennium Prize problem, still under independent review. Whether many incremental results
compound into something larger is speculation, not a finding, but it is one thing a field could
now try. That a larger budget buys more and harder results raises a question of fairness between
researchers with unequal budgets (Section 5.7).

4.4   Review evidence and remaining work
Our assessment is incomplete. The corpus contains the agents’ review records, proof checks, literature
searches, and computational tests described above, with Lean proofs for some claims. These provide
evidence for review, but they do not establish the quality of the whole corpus. The agents also



                                                 18
caught and corrected errors on their own, some of them major, before we looked at the work.1
In the material we have checked, we have found no major scientific error. Finding no error does
not show that none remains, and it does not establish what fraction of the unreviewed material is
sound; human peer review has the same limitation (Section 3.4). The machine-checked proofs are
the strongest evidence in the corpus. We have not yet checked ourselves that their Lean statements
say what the drafts claim, so for now each shows that its formal statement is proved, not that the
statement matches the draft (Section 3.2). Our partial check, together with those proofs and the
agents’ own reviews, gives us reason to take the corpus seriously. We do not ask readers to take our
word for it: every claim can be checked against the released corpus [6], and Appendix C lists the
potential papers and experimental programs in it.
    The most important comparison in this paper is between how long it took to produce the output
and how long it would take us to review it. Our estimate that the review would take months is an
estimate of work still to be done, not a measured completion time, and it rests on simple arithmetic.
The corpus groups into 45 potential papers and 8 proposed experimental programs. We do not yet
know how long it takes, on average, to check one for correctness, novelty, and usefulness, and to
see that what needs correcting is corrected. If we assume three working days for each of these 53
items, they come to about 160 working days, or more than seven months of one person’s full time.
The figure is rough, and three days is short for a careful check of a paper-length draft, so it is more
likely too low than too high; either way, reviewing a corpus of this size is a large amount of work.


5       Open questions and our positions
When we discuss what AI can now do in research, and what that means for researchers, we meet
two common responses. We describe both first, because the open questions that follow belong to
both. For each question we say what it is, why our experience makes it urgent, what we currently
think, and, where we have one, the position we take. We consider none of them settled, and we do
not have full answers to any of them. Section 6 collects the positions in one list.

5.1     Two common responses
The dismissive response. A common objection runs as follows. The results are not impressive;
a capable person would have found them; the authors are not strong researchers in these fields; and
the objector’s own work is therefore safe. We are indeed not the best researchers in any of these
fields. But people who raise the objection rarely follow it to its conclusion. If these results are trivial,
it is worth asking why the agents’ literature searches did not find them already published; the same
searches did find some of the agents’ results already known, and we set those aside (Appendix C). If
they are not trivial, the objection fails. Either way, the question is not whether the agents beat
the best person in a field. The question is how much of a field they have to match before that
field’s institutions have to change. Everyone except the top one percent? Everyone except the
top hundredth of a percent? Everyone except one person? We think that line has already been
    1
     For example, the agents built a pipeline that produces lower bounds for mixed-integer nonlinear programs together
with certificates that a separate program can check (M3 in Appendix C), and first reported certified bounds for 269
of 289 benchmark models. A later agent audit found that the checker had accepted steps it should have rejected:
conditions on domains and curvature were not enforced, and some exact-arithmetic inferences were off by amounts
of up to about 2 · 10−10 . The agents repaired the pipeline, replayed every record, withdrew the earlier claim, and
kept the old records so that the change can be audited. Rechecking the historical records left 188 accepted bounds;
a new uniform campaign, reported in the final draft, certified 203 of 289 models. The rejected steps were invalid
justifications; none of the bounds was shown to be false.



                                                         19
crossed for many working researchers, ourselves included, and we would rather say so than pretend
otherwise.
     The objection also sets the bar at a breakthrough: a proof of a famous conjecture, or a discovery
no person could have made. That bar moves whenever it is reached, and the two 2026 results in
mathematics have arguably reached it, although independent review of one of them is incomplete.
But it is also the wrong bar. Most scientific progress does not arrive as a breakthrough. It arrives as
what Kuhn called normal science: small, sound steps that extend known results [153]. Measurements
of the literature find that the share of papers that disrupt earlier work, rather than build on it, has
declined for decades [154], and breakthroughs themselves rest on the steps that came before them.
Our runs show agents producing candidate steps of exactly that kind, in several unrelated fields,
with no ideas from us; how many of them survive review is still open (Section 4.4).
     A sharper version of the objection is that the results might all be wrong. Some of them might be.
Section 4.4 explains how far our checks go and what they found; we release the corpus so nobody
has to take our word for it.
     A third version, which we hear often, is an objection in principle. A language model is a statistical
machine trained to predict text. It can only recombine what it has seen, so it cannot produce
anything genuinely new. Part of this is true, and it is less of an objection than it sounds. Models
do recombine what they were trained on. So does much of research: a large share of published
work applies a known technique to a new problem or joins ideas from two fields, and an analysis of
almost 18 million papers found that the most cited ones combine conventional knowledge with an
unusual pairing of prior work [155]. Whether a recombination produces something new depends on
the result, and that can be checked. The bound on the zeros of the Riemann zeta function did not
exist before the model produced it. It raised a bound that had not been improved for years, was
formalized in Lean, and was later recovered by an independent proof; the Navier–Stokes construction
is a second candidate, still under review. Less striking examples are the everyday results of runs like
ours (Section 4.3). We do not need to settle whether a model understands, or is creative in the way
a person is. What matters about a result is whether it is correct, new, and useful. We can check all
three without knowing who or what produced it. Where the objection rests on a measured failure,
it is evidence about the model that was tested; whether it still holds is settled by repeating the test
on current models (Section 3.3). Where it rests on no measurement, it is not evidence at all.
     A better test than our word is to try it in the reader’s own field. This works best where the
work is theoretical or needs little computing, so that what comes back can be checked at a desk.
Experimental researchers can run the thinking part of their work, as we did in catalysis; we return
to their position in Section 5.6. Run the experiment (Section 7) and compare what comes back
with what the reader’s group produced that month. If the reader does better, how long will that
last, given the measured trend (Section 3.3), and given that today’s models are the weakest that
anyone will use from now on? A win against this month’s models says nothing about next year’s.
Nor does a failure on one problem say much about the next: at any moment, agents are strong
on some tasks and weak on neighboring ones (Section 3.3). And what does the comparison look
like for the field as a whole, rather than for its strongest members? Either way, the result is worth
reporting (Section 7).
     The last version is not an objection but a decision: not to use these tools at all. We respect the
choice, but it has a likely consequence. Others in the same field will not make that choice. They
can now produce, check, and publish in weeks a body of results that would previously have taken
years. A researcher who works without these tools will then be compared, in hiring, funding, and
promotion, with people whose output is many times larger. In terms of research quality, the drafts
we have checked are not obviously worse than an average paper in the same fields. We could not
decide for ourselves how institutions should handle that comparison, so we raise it here.

                                                   20
The enthusiastic response. The opposite reaction treats this as pure good news. Research just
got easier: with the newest models and enough computation, anyone can produce results. That may
well be true, but it raises problems that we cannot answer. If results depend only on the model and
the budget, and the whole human contribution is a prompt that names a topic or a field, then the
researcher is not needed either. Anyone who cares about a problem can pay the model developer
directly. The model developer can run the agents themselves, with its newest models and at its
own cost of computation. The researcher in the middle, whose value used to be having ideas and
now amounts to paying for computation and typing “make progress on X,” is an intermediary, and
intermediaries are removed when they add no value.
    Becoming the reviewer of agent output is not a secure role either. We could not review as fast
as the agents produced. We estimate that weeks of production generated months of work for us to
review. A backlog of months is not unusual: a 2013 study found average submission-to-publication
times of nine to eighteen months across fields (Section 3.4). But if production continues at that
pace, reviewing every claim ourselves leaves a growing queue, and stronger models could widen the
gap, although they could also improve automated review. A survey of working scientists reports the
same shift: verification absorbs much of the time AI saves (Section 1), and the backlog of untested
hypotheses is growing [1]. If agents take over that review as well, machines write and machines
review, and people watch a process they do not take part in and hope that it produces useful science.
Our experience establishes a limit on our own review capacity; it leaves open how much of that
work agents can reliably take on.
    Nor are people necessarily better reviewers than agents. Every error we know of in our corpus,
including the major ones, was found and corrected by agents before any person had looked at the
work. We did not attempt an independent human review of the same material, so we cannot say
whether we would have found those errors ourselves, and we claim nothing about agents reviewing
better than we would have. Our runs also show that agent reviewers can be run in swarms as
easily as agent producers. Whether agent review is good enough today is a question we leave open,
but in principle there is no argument that an agent cannot review as well as a person or better
(Section 5.2). A plan to remain the reviewer because agents cannot review is therefore a bet that
agent capability, which has improved steadily since 2019, will now stop improving.
    Apart from what agents can do, we do not think researchers should become the in-house reviewers
of what agents produce, and we doubt that many would want to. Nobody chooses a research career
in order to check the output of a machine. People also have limited attention. If careers depended
on how much a person reviewed, the easy course would be to approve more than anyone could read,
and from the outside a signature looks the same as a review. When producing a result took months,
nobody could put their name to more work than they understood, because producing it required
understanding it. Now that agents produce the work, a person can sign off on far more than they
have read. A system that rests on human sign-off would fill with reviews that were never done,
and it would not keep pace anyway. So the question is not how to get people to review everything.
It is where human understanding is actually needed: which results a field will accept on machine
checks and agent review alone, and which it will not build on until a person has understood them
(Section 5.2).
    Nor is the news purely good even for those who keep a role. Research that arrives faster than
anyone can check it raises questions the enthusiast has to answer and the rest of this section takes
up: how far to trust results that no person has understood (Section 5.2), who will be trained when
junior work is the first to go (Section 5.8), what happens when results follow budgets (Section 5.7),
and how a field stays in control of work it cannot keep up with, including results that are dangerous
because they are correct (Section 5.10). Easier production makes each of these problems harder.
    So we end with a question for the enthusiast, and for the skeptic too. What, exactly, is the

                                                 21
researcher’s role? Not what they enjoy, not what they were trained for, but what someone would
pay them for that the model cannot supply directly. We do not have a satisfying answer. Running
agents at scale is one way to find out (Section 5.9), but only if people can keep up with what
comes out. The best partial answer we have (Section 5.6) is a shift from producing results toward
understanding, checking, explaining, and directing them, though not toward checking every output,
for the reasons above. We think the honest answers are narrower and less comfortable than the
enthusiasm suggests.

5.2   Review and trust
If agents can generate results, review them, correct errors, and prepare the final paper and supporting
materials to standards comparable with ordinary human research in the same field, what role remains
for a human in that process, and what level of checking does each kind of result need?
     Trust in a result can be established at three levels. The first is mechanical: a proof checker, a
rerun of a computation, an automated test. A formal proof in Lean, or a numerical certificate (a
file of evidence that a separate program can check) replayed in exact arithmetic, is the strongest
form: if it relies on no unproved assumptions, nobody needs to read it to know that it is valid. A
mechanical check cannot settle whether the right thing was proved or computed, that is, whether
the formal statement and its definitions say what the paper claims (Section 3.2), and it cannot
replicate a physical experiment, which needs a laboratory. The second level is judgment by agents:
reviewing an argument, checking that a formal statement matches the paper’s claims, comparing
a result with prior work, and assessing whether it matters. In our runs, every result had to pass
at least one such review by a fresh agent with no memory of the work. This review is cheap and
repeatable, but it can share the blind spots of the agent whose work it reviews. The third level is
judgment by people doing the same things. This is the review we could not finish, and it is limited
by the time and expertise of the people available. Reading a checked proof in order to understand it
remains valuable, as Tao argues [4], but that is learning, not review.
     The first two levels reduce the work required from people, but they do not make human review
keep pace with production. Our runs outpaced our capacity to review, and we are not alone: the
builders of ScientistTwo generated 86 papers from 107 problems and assessed them mainly with
AI reviewers, and human reviewers read only 33 of them [61]. If every claim must pass through a
person, that person remains the bottleneck. The question is therefore which claims can be used on
machine checks and agent review alone, and how to know when that is safe.

Can agents review as well as people? Human review is weaker than is commonly assumed:
reviewers miss most inserted errors, agree with each other only weakly, and improve little with
training, and large replication projects have failed to reproduce a substantial share of published
results in psychology and in experimental economics (Section 3.4). The comparison that matters is
with this process, not with an ideal one: whether an agent-run process produces work of comparable
correctness, novelty, and usefulness, with comparable or fewer serious errors left after review, judged
on the final paper and its proofs, code, and data. Nothing a reviewer contributes comes from being
human, but human reviewers do offer two things that current agents lack. They are independent
of the author, so their errors are less correlated with the author’s; models trained on similar data
make correlated errors and rate their own outputs more favorably (Section 3.4). And they are
accountable: a reviewer who accepts flawed work loses reputation. Both can be supplied in other
ways. Reviewing with another developer’s model, with instructions to look for faults and no shared
context, makes review more independent; our runs did some of this, and it reduces the correlation
but does not remove it. An agent has no reputation to lose, but its record can be measured directly,


                                                  22
and a measured record is a firmer basis for trust than a reputation, which is rarely checked against
anything. Responsibility for acting on a review still has to rest with a person or an institution, as it
does now with editors. We expect that in some theoretical fields agents already review at least as
well as most people, or soon will, but this has to be measured, not assumed.
    Agents can also do checks that human review rarely does. Most published computational results
are never rerun, because rerunning them costs a person days or weeks; agents have already attempted
to reproduce calculations from more than a hundred published papers, and automated verifiers can
inspect suitable replication packages at low cost (Section 3.4) [118]. Fields could therefore require
that the computations behind a result be rerun, and its derivations checked, before it is accepted,
as mathematics has done by checking contested proofs by machine (Section 3.2).

Measuring agent review. The way to know how good agent review is, is to audit it. Experts
check a random sample of the claims that agents have accepted, the error rate is published, and the
audit is repeated whenever the models change. This is statistical quality control, which high-volume
industries use for output that nobody can inspect item by item, and sequential designs, which decide
after each sample whether to continue, give the sampling explicit guarantees [156]. Agent review can
also be repeated with several reviewers. If each reviewer missed errors independently of the others,
the chance that all of them miss a given error would fall exponentially with their number [157, 158].
In practice reviewers built on similar models tend to miss the same errors: a panel of nine model
judges can be worth about two independent votes [114]. Adding reviewers therefore helps only as
far as they differ: models from different developers, formal checks, reruns, and people.

Which level each kind of result needs. When results arrive faster than they can be reviewed,
people can no longer read every result before it is used, and must choose what to read; Simon’s
observation that attention is the scarce resource [133] now applies directly to research. Some results
also exceed what a person can follow: the referees of the proof of the Kepler conjecture worked on it
for years and could not certify it, which is why a machine later checked it [64]. Each field therefore
has to decide, for each kind of result, which of the three levels it requires and what its standard is at
that level. The answer will differ between fields and with what is at stake, and we do not prescribe
it, but it should not be fixed. A kind of result can move from human to agent judgment when audits
on the field’s own results, with the current model, show that agents judge no worse than people do,
and it moves back when an audit shows otherwise. Where there is no known right answer, as with
importance, the comparison is with later outcomes, such as whether a result was used or replicated.
Where failure would be costly or hard to reverse, a field should demand more evidence.
     A field may also keep people involved where agents judge no worse: because a result could do
harm, or because people need to understand it to keep control of the field’s direction (Section 5.10).
That is a policy, not a claim about what agents can do, and it should be stated as one, with its
reason, and revisited when the reason changes. It governs what a field accepts and builds on, not
what is produced, since anyone with access to the models can produce the same result elsewhere
(Section 5.9). Software engineering already faces this choice for code: some teams now have a person
review only the changes they judge risky and rely on tests and agent review for the rest [159]. For
this to work in research, agent-produced work should be presented as claims, each with its checks
and what remains unchecked, so that each claim can be handled at its level.

Formalizing more of science. Formal verification can extend beyond mathematics to the
physical sciences and engineering, wherever their reasoning is mathematical, as in thermodynamics,
transport theory, and chemical kinetics. A machine-checked proof is only as usable as the library of


                                                   23
checked results it can build on; mathematics has such a library, and most other fields have almost
none. Agents now make it practical to build these libraries, and this has begun: the Langmuir
and BET theories of adsorption (how gases bind to surfaces) have been written in Lean with their
assumptions made explicit, a library of high-energy physics is being built there, and a derivation
in kinetic theory has been formalized [73, 160, 161]. Formalization also checks old results. The
generalized quantum Stein’s lemma was published in 2010 and widely used; a gap in its proof
was found thirteen years later, and the new proof, now checked in Lean, exposed further small
imprecisions [162, 163]. The formal statements still have to be audited for meaning, and whether
the assumptions describe the physical system remains a scientific question.

Our position: decide what deserves trust by measurement, and formalize what is
already known. Move everything that can be moved into a form a machine can check: formal
proofs where possible, replayable certificates where possible, rerunnable code and data always. Build
libraries of formalized established results wherever the reasoning is mathematical, and audit the
formal statements for meaning. Audit agent review by sampling and publish its error rate; run
agent-only review openly, with disclosure, and report what happens. Each field should state which
kinds of result it accepts on mechanical checks alone, which on the judgment of agents, and which
it will not build on until a person has understood them, and what evidence would move a kind of
result from one level to another, and publish that evidence with the model and date when a move
is made. Accept results from a process that meets the field’s standard for human research on the
same terms as any other published work, and repeat the measurement when the models change.

5.3   Access to the literature, and what “new” means
What can agents, or anyone, build on and check against, when part of the published record cannot be
reached?
    Correctness is only part of review. Assessing novelty requires comparison with prior work, and
assessing usefulness requires judgment about what a result enables. Both depend on access to the
literature, which matters well beyond review.
    Access is first of all an input to research. In our runs the agents chose their problems from the
literature collection they had assembled, took their techniques from it, and extended results in it.
Literature that neither we nor the agents could reach contributed nothing. Results stated only there
could not be built on, and open problems stated only there stayed open. Checking novelty also
depends on access, though less than building on prior work does. Nobody, human or agent, can
compare a result with literature they cannot read, so when a result is called new, it means only that
it was not found in what could be reached at the time, and the answer can change when more prior
work becomes accessible. Given access, agents in our runs searched more widely than we could:
they read more of the literature, faster, and across fields. A search counts only when the source was
actually retrieved and read, which is what our literature instructions require. Early chat models,
answering from memory, often invented citations [164]. Agents that retrieve their sources largely
avoid this: an audit of 1,814 references in 49 of the papers written by one 2026 system, whose
process includes a step that checks references, found none that had been invented [61]. Checking
whether a result is already known can therefore be delegated to agents, and audited by sampling
like any other check. Agents cannot check a result against prior work they cannot access.
    Because agents can use only what they can reach, what it means for a result to be published
changes. Research can be open, or it can be private, as much industrial research is and may properly
remain. What no longer makes sense is the state in between: work that counts as part of the public
record, and is cited as such, but sits behind a paywall or is closed to machines. Such a paper is


                                                 24
public in name only. The systems that now do a growing share of the searching, the building, and
the checking cannot use it. Nobody builds on it, nobody finds it when checking whether a result is
already known, and the work that could have followed from it is not done. The demand for an open
literature is not new [165], but the reason for it has changed. When people were the only readers, a
paywall slowed research down. Now it removes a paper from the process by which a growing share
of research is done.
     Whether a new result is also important is a separate question from whether it is already known.
It is a judgment on which experts disagree with one another, and it belongs with usefulness. Formal
checks answer neither question. Human and agent reviewers can assess both, but their assessments
remain open to further evidence. We see no reason to expect that agents will stay worse than people
at either judgment, so we do not count on a lasting human role that rests on ability. The role that
can last is one that people choose to keep: deciding what research is for, setting its direction, and
staying in control of it (Section 5.10).

Our position: open the literature, and end the state in between. Research can be private,
but work that is presented as public knowledge should be readable by everyone and everything that
does research. Until it is, every novelty claim, ours included, is relative to what could be reached.

5.4   Publication and peer review
If one researcher can produce more results than they can review themselves, what happens to
publication and peer review?
     The usual worry about AI and publishing is volume: more submissions, tired reviewers, longer
queues. Our experience points to a more basic problem.
     First, the author is the first reviewer. Every publication system assumes that an author has
checked the work before submitting it and answers for it. Peer review was designed as a second
look. When one researcher can produce more than they can review themselves, that assumption
fails at the source, before any journal or conference is involved, and nothing downstream was built
to supply the first look.
     Second, review costs more than production, several times over. Each submission takes two
or three reviewers, all volunteers, from a pool that was already strained [127, 166]. If an author
cannot keep up with their own output, the community cannot either, because it has less reviewing
time for each result than the author does, not more. One estimate puts the cost of producing a
conference submission entirely by machine at about two dollars, and models the effect of that cost
on acceptance rates [167]. Careful review takes an expert several hours. Rules on whether reviewers
may use language models do not change this imbalance: when one large conference tested them
in a randomized experiment, papers reviewed under a ban and papers reviewed under permission
received nearly the same scores and decisions [168].
     Third, the results are still worth having. If what agents produce were noise, none of this would
matter, because noise can be ignored. Our own corpus is an example: it has not been fully checked,
and it still deserves the attention of the people working in its fields. Anyone who runs such agents
will be in the same position: holding results that may matter, without the time or the capacity to
check them all. Under the present system, the work can either be published as though a person had
checked it, which would be false, or held back until someone has, which wastes it and may mean
that it never appears. No accepted channel exists for a result that is machine-checked, reviewed by
agents, and not yet read by any person, although that is what much of the output of the coming
years will be. We do not have a solution. We do think such results should not be held back. They
should be accessible to anyone, person or agent, who wants to check them or build on them, and it


                                                 25
should be clear how each was obtained and what checking it has had, so that others can decide how
far to trust it.
    Fourth, the paper can no longer serve as the unit of checking, credit, and communication at
once. When production outruns review, those three come apart. Checking has to work at the level
of the claim (Section 5.2), since a claim can be machine-checked or sampled and a fifty-page paper
cannot. Communication has to carry the verification status of what it communicates, so that a
reader can tell a machine-checked theorem from an unread conjecture without taking the author’s
word for it. Credit is a separate question (Section 5.5).
    The format itself matters. Under our usage caps we could not write a paper for every result
(Section 4.3), and much of a paper would not have been needed: it exists to persuade a human
reviewer, through the case for novelty, the narrative of related work, and the motivation. When the
prior-work search is a recorded search and the proof is a checked artifact, those can be links and
not prose. A result can then be communicated as a short record: the claim, its assumptions, its
verification status with a link to the proof or to code that can be rerun, the record of the prior-work
search, and what the result is for. That does not make exposition unnecessary. People still need to
understand results in order to use them and to steer what comes next, and Tao names exposition as
a bottleneck separate from verification [4]. But exposition is a different product from the record,
and it is written for a person. We do not know what the format should be; papers may remain,
perhaps shorter. When machines will check and build on a result and no person will read it, the
result should take a form that suits the machines, and text written to persuade a human reader
is wasted. When someone needs to understand a result, exposition can be written for that reader
when needed, and possibly generated on request.
    Patching the current system will not be enough. More reviewers, faster journals, detectors for
machine-written text, or papers wrapped as agents that others can query and rerun [169] all leave
untouched the author’s first look, which is the step that has failed. We do not have the replacement.
We think it will have three properties: results are released with their verification status stated claim
by claim; review is done by audit and sampling, with published error rates, and not by reading
everything; and the rewards of a research career follow verified contributions (Section 5.5). Each
of these properties changes incentives as much as procedure, so journals cannot bring them about
alone.

Our position: change how results are communicated. Sound work should not be held back
because the people who produced it cannot review all of it, for lack of time or of the expertise a
full review takes. Nor should work that has not been reviewed be passed off as checked. Journals,
preprint servers, and funders should support releases in which each claim carries its status: machine-
checked, reviewed by agents, audited by sampling, or reviewed by a person. The default unit should
be a claim with links to its checks, in whatever form suits those who will use it, with exposition
written where and when someone needs it. The record should say what was checked, by what means,
and what was found; a yes-or-no statement that “AI was used” does not.

5.5    Credit, authorship, and publication counts
When the only human input is a prompt, who is the author, does it matter, and what does a
publication count measure when production is nearly free?
   Suppose, as a thought experiment, that cancer is cured by someone typing “make progress on
curing cancer,” letting agents run for three years with self-driving laboratories for the physical
parts, and having model developers treat the problem as a benchmark. Outside research, few people
would ask who typed the prompt. Would that outcome be a loss for the people who spent their


                                                  26
careers on the disease, or a win? For the world it is plainly a win, and the world will not care which
researchers had hoped to make the discovery themselves. The same holds for any research that is
useful to someone: energy, materials, medicine, the optimization problems we work on. We are
adopting here a human-centered standard: research is valuable to the extent that it helps people.
Other standards exist, including the intrinsic value of understanding and of inquiry itself, and we
do not argue against them. But under any standard that gives weight to outcomes, the identity of
the prompt writer matters little.
     Why, then, do researchers care so much? Credit was never the point of science, but it is the
currency the whole system runs on: hiring, promotion, grants, and reputation are all paid in it. If
credit is taken away, something else has to take its place as the currency of incentives inside research.
That is the same problem as “why pay a researcher” (Section 5.6), seen from a different side.
     Credit is also a motive, and not only vanity. Merton argued that recognition from peers is the
one reward the institution of science has to give: it tells a scientist that a contribution was original
and mattered, and the bitter disputes over who was first in the history of science show how much it
is wanted [170]. Studies of what moves scientists distinguish three rewards: the puzzle, which is the
satisfaction of solving a problem; the ribbon, which is recognition; and the gold, which is money [171].
Agents affect all three. Recognition for a result means less when anyone with a subscription could
have produced it, and money in research has followed recognition. The satisfaction of solving a
puzzle does not depend on anyone else, but a puzzle that a machine solves first may not satisfy in
the same way. We do not know what happens to a research community when these motives weaken,
or whether people will still do the hard work of understanding a field without them. Section 5.8
asks the same question about students.
     Even if we wanted to keep credit, we could not enforce it. Nobody can tell afterwards whether a
result was a person’s idea or the output of “do some science, make sure it is solid, use ten thousand
agents,” and a person can always rewrite machine output in their own words. Researchers have
tried technical fixes, and each has been followed by a workaround. Statistical watermarks for model
text were proposed in 2023 [172]; within months rewording was shown to remove them and to
defeat detectors of machine-written text in general [173]. Detectors also make false accusations,
and they make more of them against people writing in a second language [174]. For research, the
difficulty goes deeper than any tool: a watermark lives in the wording, and what earns credit in
science is the result, a theorem, a bound, a design, which has no wording to mark. Authorship rules
(Section 3.4) therefore rest on honesty rather than on verification. In one experiment, only about a
fifth of participants who wrote with a model mentioned it, and more than half opposed mandatory
disclosure [175]. Auditable contribution records, and tests of whether an author understands the
paper well enough to defend it, are early proposals [176, 177]. We do not think that any rule
requiring proof of human contribution can be enforced, and we do not think anyone should try. The
attempt would take effort, and it would punish honest authors wrongly accused, without catching
those who take the trouble to hide.
     The better question is why anyone would hide how a result was produced. People hide their use
of AI when admitting it costs them, and at present it does: across thirteen experiments, people who
disclosed that they had used AI were trusted less than people who said nothing [178]. A system
that penalizes disclosure gets concealment, and then cannot tell where any of its results came from.
We think the aim should be the opposite: a system in which nobody gains by hiding. That means
judging a result by whether it is correct, new, and useful, and by what checking it has had, and
not by who or what produced it. A statement of how a result was produced then stops being a
confession and becomes information a reader can use, because it tells them what kinds of error to
look for. Rules that forbid the use of AI in discovery cannot be enforced, and where agents produce
better results than people do, such a rule favors worse results. We do not know how to build such a

                                                   27
system in full, but we are confident that the effort now spent on detecting and forbidding the use of
AI would be better spent on building it.
    The publication count measures very little when production is nearly free, and it measured less
than was assumed even before: counts were already known to distort behavior [124, 125, 179], and
the rise in AI-assisted preprints is an early symptom (Section 3.4). What we describe is more than
a further increase: in a few weeks, one researcher with a few subscriptions can produce material
for more papers than a typical researcher in these fields publishes in years (Section 4.3). The halt,
and partial reversal, of the long decline in solo authorship since late 2022 [180] is an early sign that
one person with tools now does what used to take a team. We know that many people are already
doing some version of this quietly. Publication counting is being broken in private. We think it is
better broken in public, where its replacement can be discussed.
    Should checking earn credit? It is already a large and under-recognized contribution: reviewers
spent more than 100 million hours on journal peer review in 2020 [181]. But we do not know how
to reward it. If agents review at least as well as most people, as we expect (Section 5.2), human
checking of everything adds little, and a career spent checking agent output is the role we argued in
Section 5.1 that nobody should want. Rewarding the amount of checking would also reward people
for approving work they have not read. The natural answer is to credit what people contribute that
agents cannot. The difficulty is that we do not know what that is, and the answer may change with
each new model. A credit system built around today’s answer could be out of date by the next
model. Whatever replaces the publication count will have to be revisited as the models change, like
the level of checking each kind of result needs (Section 5.2).

Our position: stop counting papers. Publication counts should no longer be used to judge
researchers, in hiring, promotion, grant decisions, or rankings, because a paper can now be produced
at almost no cost. Judge results by whether they are correct, new, and useful, and by what checking
they have had, and do not penalize disclosure of how they were produced.

5.6    The economic case for researchers
Why would a university, a company, or a funder pay a person a salary when the same money buys
tokens that produce more?
    The prior work and our own runs suggest that agents can already produce, or will soon produce,
more of what institutions use to measure research productivity: results, papers, proofs, and code. If
so, that measure no longer tracks effort or talent, and we have to ask directly what a salary buys.
The usual answers are choosing problems, taste (a sense of which problems are worth working on),
accountability, and the physical world.
    Choosing problems and taste are genuine answers. But our prompts chose nothing more than a
topic, a field, or a field together with a researcher’s interests, and the agents chose problems within
it without our help; whether they chose well is part of what review must assess.
    Accountability is the answer that institutions rely on most. Journals require a human author
who answers for the work (Section 3.4), and where a result is used in engineering or medicine,
someone is legally responsible for it. The need is real, but it is a weak reason to pay a salary. A
responsible person who cannot check the claim provides a signature rather than a safeguard, and so
does a person in the loop who cannot keep up. In our runs, the human was the slowest component
and, by design, contributed no scientific content: we chose the scope, set the process, and asked for
write-ups, checks, and proofs (Section 4.1), and the snapshot we release contains nothing else from
us. The checks were done by agents, and our own reading came afterward and covers only part of
the corpus (Section 4.4), so our presence in the loop was not a safeguard.


                                                  28
     The physical world is the answer that holds best today: experiments, patients, and field sites
still need people on site. That protects experimental work for now, but only the experiment
itself, not the thinking around it. It does not protect the theorist at all, and the line between
what needs a person and what does not is moving: agents can already propose experiments. In
catalysis, our agents designed experimental programs, although nobody has run them and we
cannot yet say how good they are (Section 4.3). It is worth asking what the experimentalist’s
job becomes when the model reads the literature, chooses the question, designs the experiment,
and analyses the data, and the person carries out the laboratory work. Self-driving laboratories
bounded by a stated objective already exist [48, 49, 182], agents have designed molecules that human
laboratories then validated [139], and general-purpose laboratory robots are an active research
area [51]. Experimentalists know at least as much as we do about how fast this is moving. But
the knowledge work of experimental science is exposed in the same way as theory, and what agents
propose becomes easier to test as laboratories are automated. Institutions that wait for automated
laboratories before preparing will have waited too long.
     None of these four answers explains, on its own, why an institution should keep paying many
researchers. If the only measure is results per dollar, an institution will not keep paying them. We
do not think results per dollar should be the only measure. There is also a reason to expect more
demand for researchers, not less, although it is a possibility and not a finding. When steam engines
began to use coal more efficiently, the economist William Stanley Jevons observed that total coal
consumption rose rather than fell, because cheaper power made new uses worthwhile [183]. The
effect, in which a gain in efficiency increases total use of a resource, is now known as the Jevons
paradox. Research may follow the same pattern. If results become cheap, many more questions
become worth asking, many more directions can be explored at once, and many more results need
someone to connect them to a problem that matters and put them to use. Each of these could
need people: to choose among far more options than before, to steer agents toward the right ones,
and to carry results into engineering, medicine, and industry. On this view, cheaper research could
mean more researchers, not fewer. Agents may do the choosing, steering, and applying as well,
and even if they do not, we cannot yet say what those researchers would do day to day, or which
skills they would need. A field that pays only for results, and buys them from agents, loses the
people who understand what it is producing, and that is dangerous (Section 5.10). The reason to
pay researchers is changing: less for producing each result, and more for understanding the work,
checking it, and deciding where it should go. That work takes deep knowledge of a field, which is
one reason demand is already moving toward experienced people (Section 5.8). Institutions have to
choose deliberately to pay for this work, because decisions made on cost alone will not.

5.7   Computation, budgets, and fairness
If results scale with the computation committed to a model, does the best researcher become the one
with the largest budget?
    For a fixed model, more computation at the time of use buys more results and solves harder
problems (Section 4.3). A field-scale run (Section 5.9) shows this at the top of the budget range. At
smaller budgets, the same rule raises a question of fairness between researchers. Two researchers of
equal ability with unequal budgets will, on current trends, produce unequal bodies of work, and the
difference will be attributed to the researchers. Hiring, promotion, and funding decisions are made
on bodies of work, so if nothing else changes, they will reward the budget. Falling prices soften this
over time (Section 4.2): work of the kind our subscriptions bought this month will soon cost much
less. The most capable models may become more expensive, but a given budget has so far bought
better results every year. At any one moment, though, a larger budget still buys more.


                                                 29
    So research results will increasingly depend on how much computation a researcher can pay for.
We do not think that can be avoided. Spending on computation may well be the most productive
way to turn money into results. But more results is not the only thing a research community wants,
and what worries us is that research may come to depend on budgets without anyone deciding
that it should. A community that drifts into this dependence will have settled who gets to do
research, how careers are judged, and what a training grant pays for, without anyone having chosen
those answers. We think three questions should be decided openly. Should institutions provide
computation as a shared resource, the way they provide libraries and laboratories, and not as a
budget for each person? Should assessment separate what a person did from what their budget did,
and is that possible? And what is a fair way to divide funds between people and computation, if
a dollar spent on computation produces more than a dollar spent on a person? We do not have
answers. These questions are already being answered, without discussion, by budget decisions made
for other reasons.

5.8   Learning and motivation
Learning matters more than before, and is rewarded less. How do we motivate someone to spend
years becoming competent when the machine already exceeds the competence they are working toward,
what should they learn, and how can it be taught?
    We think learning has become more important, not less. Production has become cheap, and
what remains scarce is understanding (Section 5.2). A person who cannot understand a result
cannot judge it, cannot steer work toward it, and cannot decide whether it matters. The knowledge
needed to do those things, or to add anything the agents would not, is growing. But producing
results, the activity that used to justify the learning, is now cheap and will stay cheap. So learning
is needed more and rewarded less.
    The amount a person must know before contributing was rising before agents existed. As
knowledge accumulates, each new researcher has more to learn before reaching the frontier: the age
at which inventors first patent rose by about 0.66 years per decade in the late twentieth century,
while inventors specialized more narrowly and worked in larger teams [184]. Agents raise that bar
again, and much faster. They now do much of the incremental work that a well-prepared student
could do (Section 4.3). What a person must learn before making a first contribution that the agents
could not make keeps rising, so the starting line moves away while the student works toward it. An
experienced researcher is already past it, and gets excellent results from the same tools.
    The role changes, as does the amount of knowledge required. A junior researcher used to start
with a small, well-defined part of someone else’s project and learn the field while doing it. Agents
now do those parts. The work that remains is the work of the person who leads a research group:
choosing the direction, dividing the work, judging what comes back in every subfield the agents
range into, and deciding what to trust. A new researcher has to do that from the start, with agents
in place of the group. That job used to come last in a career, after years of the smaller tasks. It
also takes more knowledge than it took a few years ago, because the agents range more widely than
any group did. Starting a run takes none of this knowledge: we supplied no scientific input to ours
(Section 4.1). Knowledge is needed to steer a run well, check what it produces, and add what the
agents would not.
    This changes who gets trained. Suppose a group has a fixed budget and accepts that more
computation buys more results (Section 5.7). The choice that makes sense for that group is one
experienced person who sets direction, and the rest of the budget goes to computation. Junior
researchers, on that arithmetic, are the budget item that produces the least per dollar, because
the work left for people takes knowledge they do not yet have. The same arithmetic is already


                                                 30
visible outside academia. In the occupations most exposed to language models, a November 2025
study using data through September 2025 found a relative decline in employment of about 16%
for workers aged 22 to 25, while employment of workers aged 35 to 49 in those occupations grew
by more than 8% over the same period [185]. A study of 62 million workers found the same split
inside firms that adopted generative AI: junior employment fell, mainly because hiring slowed, while
senior employment kept rising [186]. Demand has moved toward experienced people, not only away
from junior ones, and in AI research itself experienced researchers are concentrating in the private
sector [187]. Both employment studies are observational, and neither is about research. But the
pattern is what a rising bar predicts: the tools replace people below it and make people above it
more productive. Earlier experiments found the opposite pattern. When people used a model as an
assistant on short writing and consulting tasks, the weakest performers gained the most [98, 188].
Those gains occurred on tasks within the model’s reach, where the person’s job was to produce
the output. When agents produce the output, the person’s job is to direct and to check, and their
knowledge is the whole contribution. Applied to research, the arithmetic has a delayed cost that the
budget does not see: experienced people are made from junior ones, and a field that stops training
junior researchers has, in one generation, no experienced ones. This is a short-term gain purchased
with a long-term loss, and it is the kind of trade that institutions make when nobody is asked to
decide it.
    The same change affects motivation. A junior researcher today can ask a question that has no
comfortable answer: if the agents can do everything I can do, and better, what is my contribution?
For a few years the answer was that the agents could not do the hard parts. On current trends
that answer fails first for junior researchers. We argued in Section 5.1 that it has already failed for
many working researchers, and that, along the same trends, it will fail for the rest. So we do not
rest the case for learning on contribution alone. Even when the bar passes everyone, someone still
has to check results, steer the work, and decide what to use (Section 5.10), and all of that takes
understanding. The harder question for a junior researcher is then whether they can understand
what the agents produce, not whether they can add to it. The student is asked to learn more than
earlier generations did, for a contribution that is further away and less certain. We do not have an
answer; this is the problem of who gets trained, seen from the student’s side.
    Behind both lies a change in how learning and results are connected. Until now, producing a
result required learning first, so any system that rewarded results rewarded learning without having
to try. That link is broken. A result can now be obtained without understanding it, and for anyone
who needs results quickly, a student with a deadline or a group with a grant to renew, obtaining
it that way is the rational choice. Evidence from education points the same way: students given
unrestricted access to a model did better on the exercises and worse once the model was taken
away [189]. An incentive system that pays for output now pays for skipping the learning, at the
moment when understanding is the thing in short supply, and it will not correct itself.
    The same change affects what people should learn. We think people should learn more, not less,
but different things. Implementing an idea has become cheap; understanding one has not. Steering
agents, judging their output, choosing what matters, and noticing when something is wrong all
require deeper understanding, across more of a field than before, because the agents will range across
all of it and neighboring fields as well. At the same time, some skills that training used to take
years to master have become what arithmetic became after the calculator: worth understanding,
not worth perfecting. Nobody now needs to multiply quickly by hand, and everybody still needs to
know what multiplication is. Which research skills are of that kind is a question each field has to
answer for itself, and quickly, because the cost of guessing wrong falls on the people being trained
now. They will finish training years from now and then work for decades, so the answer should be
judged against the models they will work with over their careers, not this year’s.

                                                  31
     How to teach this is a harder question than what to teach, and we do not know the answer.
Experienced researchers have rarely taught judgment directly. People acquired it over years of doing
the smaller tasks, under someone who already had it, and those are the tasks that agents now do.
Research training worked by doing the work, and a person who cannot follow the work cannot be
trained by doing it. This may undercut our advice to stop perfecting some skills. Practicing a skill
may be part of how understanding of it forms, so a skill that is no longer worth perfecting may
still be needed as training, as arithmetic by hand still is for children. Agents as teachers are one
candidate route, and the early evidence is mixed. In the education experiment above, a tutor built
to give hints instead of answers removed the harm that unrestricted access did, but the students
who used it did no better on their own afterward than students who had no model at all [189].
We know of no tested way to bring a person to an experienced researcher’s level of understanding
without the years of production that used to build it.
     Chess shows what it looks like when machines are far ahead. Chess programs passed the best
human players in the late 1990s, and today no person can compete with them. We expect the same
in research, field by field and probably in mathematics first: on the measured trend (Section 3.3)
agents will come to be far ahead of people, and no one is in a position to prevent it (Section 5.9).
Human chess did not die. People still play, and they learn from the machines; in Go, the quality
and novelty of human players’ moves rose after superhuman programs appeared [190]. That half
of the analogy carries over. Agents that are far ahead of people in a field can also be the best
teachers the field has had. The other half does not carry over. Chess survives as a contest between
people, which others pay to watch. Research is not a contest. Its value lies in its results, on the
standard we adopted in Section 5.5, and that is the standard on which society pays for it: the
case for funding curiosity-driven research has always been that useless knowledge turns out to be
useful [191, 192]. The people who do research are moved by something else as well, the puzzle
and the recognition [170, 171, 193], and the tension between the two standards is visible in how
mathematicians have responded to the 2026 results: as a loss of the journey and of meaning, not
of results [194]. A science kept going as a competition between people, while machines did the
real work, would keep the puzzle and the recognition, but not the results that society pays for.
Chess also cannot tell us what to do about machines that run far ahead of human understanding,
because in chess nothing depends on the answer. In research a great deal does: results that nobody
understands cannot be steered, and may not be safe to use. How far ahead the agents run is not
something anyone gets to set. What people can still set is what they do with the results: what a
field accepts and builds on, what is put to use where the stakes are high, and where guardrails are
needed. Section 5.10 takes this up.

Our position: teach more, not less, aim it at understanding, selection, and judgment,
and fund training as infrastructure. Plan for researchers to need more learning than before,
not less, because the knowledge needed to check, steer, or add to agents’ work is growing. Graduate
training should assume production is cheap and teach what it is not: understanding a field in
enough depth and breadth to steer work in it, choose problems, recognize what matters, and check
claims quickly. Each field should identify the skills that are now worth understanding but not
worth perfecting, and stop spending years on them. Assessment of students and of researchers
should reward understanding directly, because output no longer implies it. We do not know how to
teach that understanding without the years of production that used to build it. The training of
junior researchers should be funded on purpose, as a shared long-term asset, and not left to the
productivity arithmetic that will otherwise remove it, whether that arithmetic is done by a research
group, a university, or a country.


                                                32
5.9    Field-scale runs
What if agents are run over whole fields, the most suitable ones first, at a scale no research group
can match?
    Model developers are the most likely to run agents over whole fields first. Nothing stops them,
and one of them has already done it for a single problem: the Navier–Stokes run (Section 2) would
have cost a customer several million dollars and took four days. Developers have each model before
its release, as the internal models behind both 2026 results in mathematics show, and they pay the
computation cost, not the customer’s price. Before each new model, a developer could spend the
same on a hundred fields with the prompt “make important progress,” publish the output, and use
it as both a benchmark and an advertisement. In some fields the output could exceed a year of the
published literature. Much of what individual researchers in those fields were working on, with or
without a subscription, could be in it. Model developers are not the only actors who could do this.
Open-weight models, whose trained parameters are published so that anyone can run them, and
academic or national computing centers, could run the same experiment at a different price and
under different incentives. A funder, a company, or a government could pay for such a run as well.
For the researchers in a field, the consequence is the same whoever runs it. Who runs it does decide
two things: whether the output is public, and who sets the field’s agenda (Section 5.10).
    Nobody can control how fast field-scale runs happen. A developer, a funder, or a field that holds
back does not slow the work down. It leaves the work to whoever does not hold back. The price of
a run of a given quality falls every year (Section 5.7), so the number of actors who can afford one
grows. Slowing production would take agreement among all of them, and in fields where a correct
result does little harm we see no reason anyone would seek such an agreement. We therefore expect
agents to move far ahead of people in the fields that suit them, probably in mathematics first, and
Section 5.10 starts from that expectation.
    We think field-scale runs will happen, and probably should. If the race between AI companies
becomes a race to cure diseases and solve the hard problems of energy and materials, few people
would object. In our view, the first candidates are fields in which a result can be checked by
machine, needs no laboratory and little computing, and is unlikely to do harm if it is correct. Pure
mathematics with formal proofs is one. Others are optimization theory and algorithms, theoretical
computer science, quantum algorithms and quantum information theory, and the mathematical
parts of physics and engineering. Rerunning and auditing the existing computational literature is
another candidate, and it builds the capacity the rest will need to check. We do not know whether
the research community will have any role in that race other than sorting the output afterward, or
whether it will be able to sort the output at all. In that world, nobody will ask who gets the credit.
    Field-scale runs would also help answer a question this paper keeps returning to: where can
people still add something? If agents can already do a large part of theoretical research on their
own, the most direct way to find out how much is to run them at scale and look at what comes
out. What agents produce on their own then becomes a baseline, and the human contribution is
whatever people can add on top of it: better problems, deeper results, connections the agents missed,
or judgment about what matters. We would like to answer the question this way, but we are not
sure it works. It assumes that people can follow the baseline well enough to build on it. If agents
produce more in a month than a field can read in a year, and their results become harder for people
to understand, people may not be able to tell what is already known, let alone add to it. We do not
know what the human contribution is in that case, or how anyone would measure it. We think it is
one of the most important open questions in this paper, and we raise it without an answer.
    A particularly consequential case is AI research itself. If agents improve AI systems, and those
improvements make the agents better at producing further improvements, research enters a feedback


                                                 33
loop. The idea is old: it was described in 1965, before any of the technology existed [195]. Nobody
outside the developers knows how close it is. What is clear is that it is being pursued, not avoided,
and that the developers who can run agents over whole fields are the ones best placed to close
it. We met a milder difficulty in our own fields: output arrived faster than we could assess it. AI
developers could face the same difficulty and struggle to evaluate changes before those changes
enable the next round of development.
    The stakes would extend far beyond a backlog of papers. How would people assess safety, retain
meaningful oversight, or decide when to stop a process whose developments they could no longer
adequately review? These are not fringe worries. In 2023, hundreds of AI researchers and the
heads of leading AI companies signed a one-sentence statement calling for mitigating the risk of
extinction from AI as a global priority alongside pandemics and nuclear war [196]. A group of senior
researchers has since argued in Science that an irreversible loss of human control over autonomous
AI systems is a real possibility, and that safety research and governance are not prepared for it [197].
We are not qualified to judge how likely such outcomes are, and our runs do not establish whether
such a feedback loop will occur or how quickly. What our experiment offers is a small, first-hand
illustration of how such a loss of oversight could come about. In our fields, results arriving faster
than we could review them was an inconvenience. In AI development, it would mean a technology
whose current state its developers no longer fully understand, where the consequences of losing track
could be severe and impossible to undo. A researcher who has watched agents outrun their own
ability to check the work, in a field they know well, is better placed to take these warnings seriously,
and we hope the experiment can serve as that kind of first step.

Our position: run agents over whole fields, in the open, and check what comes out.
Field-scale runs are now possible, and they should be carried out so we know what they actually
produce rather than guessing, starting with the candidate fields above. Checking should be part of
the run itself, not a later step: alongside the agents that produce results, other agents should work
through those results as they appear, looking for errors and results that cannot be reproduced. The
same kind of run should also be pointed at the published literature of a field. The output should be
public, and the checking should be planned and funded alongside production, because output that
nobody can check is of little use. What agents produce on their own should then serve as a baseline
for finding where people can still add something on top.

5.10    Staying in control without keeping up
If people cannot keep up with what agents produce, and nobody can slow the agents down, how do
people stay in control, and where are guardrails needed?
    We start from two expectations: that people will not keep up, and that nobody can pace the
agents. People already cannot keep up with the volume: results arrive faster than they can be
reviewed (Section 5.2). We expect people to fall behind in ability as well. On the measured trend
(Section 3.3), agents will move far ahead of people in the fields that suit them, as chess programs
moved far ahead of chess players, and mathematics will probably be first. Tao’s 2026 lecture at the
International Congress of Mathematicians describes the same shift as a move from proof scarcity to
proof abundance [4], and Tsimerman, a 2026 Fields medalist, has said that AI “is going to become
better than mathematicians at research mathematics very shortly” [194]. Nor can anyone pace
the agents. Anyone with access to current models can start a run, many actors can afford a large
one, and prices fall every year (Section 5.9). A researcher who declines the tools is outcompeted
(Section 5.1), a rule against using them cannot be enforced (Section 5.5), and a field that holds back
leaves the work to others. Both expectations are forecasts, not findings of our runs, and both would


                                                  34
fail if the trend stopped (Section 3.3). We see no sign that it will, and we think planning should
assume that it does not.
    One answer is then to let go. Accept that people cannot follow the output, let agents produce
the results and check them, and use what comes out. It is a coherent answer, and much of this
paper makes it look attractive: we have argued that no part of review has to stay with people once
agents do it at least as well. But keeping up and staying in control are different things. No chess
player can follow a chess program, and people still decide what chess programs are used for. Letting
go of keeping up is not a choice; it is what we expect to happen. Letting go of control is a choice,
and it has costs that an error rate does not measure.
    First, a correct result is not the same as a safe one. Review, as we have used the word, asks
whether a result is correct, new, and useful. It does not ask whether the result should be produced
or released at all. In some fields, a result is dangerous because it is correct. A drug-discovery model
that was redirected to seek toxicity instead of avoiding it proposed tens of thousands of candidate
toxic molecules, known nerve agents among them, in under six hours [198], and the agents in the
Hugging Face incident did sustained, coordinated damage that no human directed [8]. A research
process run and reviewed by agents has no step at which anyone asks whether a result should be
produced or released, unless someone puts one there.
    Second, understanding is how people notice that something has gone wrong. A field whose
knowledge grows faster than anyone in it can follow loses the ability to see that its direction is
mistaken or that an error has spread. Models trained on similar data share their errors, so a blind
spot in a few widely used models can become a blind spot in a whole literature, and only someone
who understands the field from outside that process is placed to see it.
    Third, someone always chooses the direction. In our runs, the agents chose the problems. At
scale, whoever chooses the problems sets the agenda of a field. Letting go does not remove that
choice. It hands it to the agents and to the few organizations that run them, without anyone
having decided to. An analysis of how people could lose influence over the systems they depend on,
step by step and through ordinary delegation with no single dramatic event, describes this kind of
change [199].
    Fourth, letting go is hard to take back. A field that stops training people who can follow its
results (Section 5.8) cannot quickly train them again when it finds it needs them.
    The development of AI itself (Section 5.9) is the case where these costs are highest, but it is not
the only one. Biology, chemistry, and computer security have the same structure: results that can
do harm, produced faster than anyone can follow. We do not think the answer is to keep a person
on every result, which is no longer possible, or to give up control, which we think is dangerous. It is
to decide on purpose where people must stay and where guardrails are needed, and to make that
decision by what is at stake as well as by measured error rates: how much harm a result could do,
and whether that harm could be undone.

What control can rest on. Control does not require following every result. It requires results
that can be trusted without being understood, through machine checks and agent review with an
audited error rate (Section 5.2); people who set a run’s goals and can stop it; enough people who
understand a field well enough to audit a sample of its results, notice a shared error, and judge
where the work should go; and guardrails where a correct result can do harm.

Where guardrails can work. Production cannot be paced, but it is not equally free everywhere.
In mathematics and fields like it, a correct result does little harm, and we see no reason to hold
the agents back (Section 5.9). What is at risk there is human understanding, and the remedy is


                                                  35
teaching and exposition (Section 5.8), not restraint. Where a correct result is dangerous, a guardrail
can hold. A few developers run the most capable models, and they can refuse dangerous work and
watch for it. Harm in the physical world passes through laboratories, materials, and equipment,
and access to those can be controlled. The largest runs need computing on a scale that few can
supply. And use can be governed where production cannot. A regulator, a journal, or an engineer
can decline to rely on a result that nobody understands, where the stakes are high, even though
others produced it and even though that means moving more slowly than the agents could. None
of these is secure. Anyone who runs an open-weight model can remove its safeguards. A rule on
use binds only those who accept it, and competition pushes against it. We do not know how to
build guardrails that hold, and it is not our field. If production cannot be paced, guardrails at these
points are most of what control consists of, and the work on AI safety and governance that builds
them deserves the attention of researchers in every field.
    The budget arithmetic says to train fewer, because computation produces more results per
dollar than a junior researcher does (Section 5.8). The costs above say the opposite. People who
understand a field are the only means it has of noticing a shared error, of judging whether a result
should be released, and of choosing its direction. They will not follow everything, and we do not
ask that they do. What a field needs is enough of them, with enough depth, to audit what the
agents produce, to steer it, and to say where guardrails belong. That need grows as the agents move
ahead, because there is more to audit and more that depends on it. Cheaper results may also create
more work for people, by making far more directions worth exploring and far more results worth
putting to use (Section 5.6). We therefore think fields should invest in more people, not fewer, and
should do so on purpose. This position rests on less than we would like. We can say why a field
needs people; we cannot yet say what they will do. Auditing, steering, and keeping up with results
are the roles we can name today, and agents may take over each of them as the models improve
(Section 5.2). If agents move far ahead, it is not clear what a person will be able to add to what
they produce (Section 5.9), or what training would prepare them for it (Section 5.8). We argue for
more people without yet knowing what their role will be. It will cost money that could have bought
computation, and where the stakes are high, waiting for people to understand a result before using
it will be slower than the agents allow. We think that cost is worth paying. Section 5.6 describes
how the work those people are paid for changes.

Deciding in advance. Institutions change over years and models over months (Section 1), so
these decisions cannot wait until agents reach the level they respond to. They can be made in
advance, as commitments of the form: if agents reach this level, we will do that. Some of these
levels are already in sight. When audits show that agent review of a kind of result is as reliable as
expert review, a field can accept such results without a person reading each one (Section 5.2). When
agents move ahead of people in a field, its hiring, funding, and training should reward understanding,
auditing, and choosing direction rather than production (Sections 5.6 and 5.8). When self-driving
laboratories make experiments cheap to run, the questions this paper raises for theory will arise for
experimental science as well (Section 5.6). When agents contribute substantially to the development
of AI itself, the guardrails above become most important (Section 5.9). Each level should be defined
by a measurement that can be repeated on each new model, so that whether it has been reached is
a finding and not an opinion. Some AI developers already make commitments of this form for their
own models, tying required safeguards to measured capability thresholds [200].
    Is society ready to rely on research that no person understands? In our view it is not, and it
will soon have to decide how far to rely on it. The choice should be made openly.




                                                  36
Our position: plan for agents that are far ahead, aim at control and not at keeping up,
and invest in more people, not fewer. Assume that agents will move far ahead of people in
the fields that suit them, and that no single actor can pace it. Decide in advance how to respond
when each measured level of capability is reached. Decide on purpose where people must stay in the
loop, and decide it by what is at stake as well as by measured error rates. Where results can be
dangerous because they are correct, put guardrails where they can hold: the developers’ safeguards,
the physical means of doing harm, the largest computations, and the decision to use a result. Add
a check on whether such results should be produced or released, because review for correctness,
novelty, and usefulness does not include it. State every such rule as a policy, with its reason, so
that it is not mistaken for a claim about what agents cannot do. And invest in more people who
understand a field, not fewer, because auditing, steering, and setting guardrails depend on them,
and because cheaper results may make far more research worth doing, even though we cannot yet
say what these people’s role will be.


6    Summary of positions
We would rather take positions and be wrong than only ask questions. The first twelve are argued
in the sections cited; the last two concern the paper as a whole.
   1. Decide what deserves trust by measurement. Put results in a form a machine can check,
      audit agent review by sampling and publish its error rate, run agent-only review openly, and
      accept results from a process that meets the field’s standard on the same terms as any other
      published work (Section 5.2).
   2. Formalize what is already known. Build libraries of machine-checked established results
      in the sciences and engineering, wherever their reasoning is mathematical, and audit the
      formal statements for meaning (Section 5.2).
   3. Decide what level of checking each kind of result needs, and revisit the decision
      with each model (Section 5.2).
   4. Open the literature, and end the state in between. Work presented as public knowledge
      should be readable by everyone and everything that does research (Section 5.3).
   5. Change how results are communicated. Release claims with their verification status
      (machine-checked, reviewed by agents, audited by sampling, or reviewed by a person), with
      links to their checks, and write exposition when someone needs it (Section 5.4).
   6. Stop counting papers, judge results by their correctness, novelty, usefulness, and checks,
      and do not penalize disclosure of how a result was produced (Section 5.5).
   7. Teach more, not less, and aim it at understanding, selection, and judgment, stop
      perfecting skills that are now only worth understanding, and reward understanding directly
      (Section 5.8).
   8. Invest in more people, not fewer, and fund their training as infrastructure, because
      auditing, steering, and setting guardrails depend on people who understand the field, and
      because cheaper results may make far more research worth doing. What these people will do
      is an open question (Sections 5.6, 5.8, and 5.10).
   9. Run agents over whole fields, and over their published literature, in the open,
      and check what comes out, with checking planned and funded together with production,
      and use the output as a baseline for finding where people can still add to what agents produce
      (Section 5.9).
  10. Plan for agents that are far ahead, and aim at control, not at keeping up. We expect
      agents to move far ahead of people in the fields that suit them, probably in mathematics first,


                                                 37
     and no single actor can control how fast this happens, because anyone with access to the
     models can run them (Sections 5.9 and 5.10).
 11. Decide in advance what changes at each level of capability. Define levels of capability
     that can be measured on each new model, such as agent review that is as reliable as expert
     review, agents that are ahead of people in a field, or cheap automated experiments, and decide
     now how institutions will respond when each is reached (Section 5.10).
 12. Decide on purpose where people must stay in the loop, and where guardrails are
     needed, by what is at stake as well as by error rates. Where correct results can be dangerous,
     put guardrails at the points where they can hold, add a check on whether a result should be
     produced or released, and state each such rule as a policy (Section 5.10).
 13. Date every limitation. When a study reports something an AI system cannot do, record
     the model and the date, and treat the finding as evidence about that model until it has been
     repeated on the current one (Sections 1 and 3.3). Do not use an undated limitation to justify
     waiting.
 14. Have this conversation now. The conversation is about what research and researchers
     are for, and it concerns everyone who depends on research, not only the people who do it.
     Waiting to review an entire corpus before discussing its implications delays it (Section 7.1).
     So does waiting for AI to clear some higher bar before the question counts, even though
     the institutions of research are built around what the ordinary researcher produces, and in
     theoretical fields agents can already produce much of that (Section 1). Every month spent
     arguing about whether AI is “really” doing science is a month not spent deciding what to
     do about it, and if current trends continue, each new model that arrives while institutions
     wait widens the gap between production and review. Lead time is why this cannot wait:
     institutions change over years and models over months, so any change started now should
     plan for capabilities that keep increasing, not for the models of any one moment (Section 1).


7     Release and proposal
7.1   Why we release now
The obvious alternative was to keep the output for the months we estimate review would require,
then publish the good parts the normal way. We chose not to, for four reasons.
    First, what the experiment shows about agents matters more than any single result, and more
than the procedure that produced it. The results may well be useful in their fields: sharp bounds
on relaxations and complexity results in mixed-integer nonlinear programming, sharp constants for
the cost of following the central path in interior-point methods, and thresholds and scaling laws in
thermodynamics, transport, and aggregation. That all of this appeared in weeks, with no scientific
input from us, matters more.
    Second, the question is larger than our fields. It concerns every field in which people produce
and check results, and every institution that depends on research. Publishing only the reviewed part
would hide the output that remains unreviewed; releasing everything produced so far lets others
assess both the research claims and the review process that produced them. The corpus may prove
somewhat better or worse than it appears now, and that will show what the present models can
do. We do not expect it to change the questions this paper raises, which follow from a trend rather
than one corpus, so the broader discussion can proceed while that assessment continues.
    Third, the credit system, which agent-produced research will disrupt, is in our view already
losing credibility, and it is better disrupted in the open than in secret (Section 5.5).
    Fourth, people notice a new capability only after it arrives, and the lag is already measurable.

                                                38
GPT-5.6 Sol, which produced some of our results, had been public for almost two months before
we tried this (Section 4.2). Many who notice a capability use it quietly, as the rise in AI-assisted
preprints suggests (Section 3.4), and policies and institutions cannot adapt to what is not discussed
in the open. Each month of delay widens the gap between what agents can do and what institutions
are prepared for.
    Releasing the corpus this way has costs. Errors in material we have not reviewed will be found
and attached to our names. Some journals do not accept work that has already appeared in public,
so releasing the drafts now may close some venues to them later, when we submit the ones that
hold up. We accept these costs for the reasons above. That others can build on the results at once
is the purpose of the release, not a cost of it. Holding results back until they are perfectly polished
is a strategy for a world in which results are scarce and are produced no faster than they can be
reviewed.
    Releasing the corpus is not all we plan to do. We intend to review the results ourselves and to
submit the ones that hold up through the normal process of peer review and publication, because
that is how trust in a result is established today. That will take a long time. The backlog we have
created is already large, and because the runs continue, we expect it to keep growing. We do not
yet know what we will do with the results still to come. That uncertainty is part of what this paper
reports.

7.2   What we propose to readers
We do not want this paper to be read as a report about us, nor as a claim that machines have
replaced researchers. We propose an experiment that you can run yourself, whether you are a
skeptic or an enthusiast.

Run the experiment. Take a problem you care about, or your whole field, and follow the
procedure in Section 4; examples of our prompts are in Appendix B and our subscriptions in
Section 4.2. If you have ideas, provide them as directions, and leave the agents free to explore
others. If you want your runs to be comparable with ours, supply no ideas. Access to the literature
is the single input that most limits both what the agents will produce and how well their novelty
claims can be checked. Use the most capable models available to the public at the time you read
this. During the runs reported here, those were OpenAI’s GPT-6 Astra and Anthropic’s Claude
Fable 5.1. Decide in advance how much you are willing to spend, and then use all of it. For a given
model, a larger budget buys more and stronger results (Section 4.3), so the budget is part of the
experiment and should be reported with the results. Spend part of it on checking, with agents that
review the results as they appear, and plan for your own review effort as well. Then judge what
comes back by the standards of your own field, not ours. A negative result is as useful to everyone
as a positive one, especially if you record the model and the date and repeat the experiment as new
models arrive.

Report the result. Say what you asked, what you gave the agents, and what came back. Say
which claims you reviewed, how you selected them, what you checked, and what remains unreviewed.
Distinguish human assessments from agent reviews and formal checks. Report review time where
recorded and label estimates as estimates. Say how the results were produced. If you found errors,
say what kind and how you found them. If you found nothing of value, say so, and say which model
you used and when. Reports that describe their checks can be compared across fields; reports that
omit them cannot.



                                                  39
Interpret the result, and the trend. You know your field, and we do not. Say what these
results imply for how work in your field will be done, for who will be paid to do it, for how students
should be trained, and for how results should be checked and credited. Then look past the result
you have. What the agents did this month matters less than where they will be in a year. The trend
matters most when the agents fail. A failure is worth reporting, and so is what happens when you
repeat the experiment on the next model. Capability at any moment is uneven: the same agents
may fail on one problem and do remarkable work on a neighboring one. So look at where they failed
and where they did not, and at how both compare with what agents could do before. You can
measure this change yourself: run the same experiment with a model that is six months or a year
old, repeat it when new models arrive, compare what came back with what you got from similar
tools before, or look at how the published measurements of these models have moved (Section 3.3).
Extend that trend a few years, and ask what your field should be doing now if it holds. Disagree
with us where we are wrong.
    There are many important questions about AI that we have not raised here. We hope readers
begin with those closest to their own work: seeing what agents can do in a field you know makes
concrete what you can still assess, what deserves your trust, and which decisions you can meaningfully
oversee. That experience is also a starting point for understanding larger changes, including the
possibility that AI could accelerate its own development (Section 5.9). These larger changes and
their risks already deserve serious attention, and we hope readers will carry what they learn beyond
their own field.
    The sooner many people report, the sooner this conversation rests on evidence instead of opinion.
The time to take AI seriously as a participant in research, and to decide on purpose how research
should change, is now.


Disclosure
The research corpus described in this paper was produced entirely by AI agents, with no scientific
input from the authors, as described in Section 4. We release that output at https://github.com
/SECQUOIA/agent-swarm-research [6]. This paper describes the repository at commit 84c6be7,
and Appendix C lists the potential papers and experimental programs in it and links to the drafts.
Later versions of the repository may add results and our own scientific input; they are not part of the
work reported here. This paper itself was written by the authors with AI help for drafting, editing,
and literature search. The arguments, the positions, and the decisions about what to release are
ours. We take full responsibility for every description of the corpus in this paper. Our assessments
apply only to the claims we have reviewed and the checks we describe.


Acknowledgments
We appreciate the constructive comments on a draft version of this manuscript from John A. Morgan
and Sridhar Tayur and acknowledge comments from colleagues and friends about this draft version.
The authors do not identify any conflict of interest in this work.


References
  [1] Mihai Codreanu, Alex Imas, Juan Mateos-Garcia, Joseph Emmens, Evalyne Muiruri, Arthur
      Turrell, Atoosa Kasirzadeh, Ana Trišović, Julian Jacobs, Catherine Pollard, Scott Strand,
      Yiyuan Chen, Fabien Curto Millet, Tanya Rodchenko, Daniel Rock, Zanna Iscenko, Neil

                                                  40
    Thompson, and James Manyika. AI in science: Early insights. Technical report, Google,
    Google DeepMind, and MIT FutureTech, September 2026. URL https://ai.google/stat
    ic/documents/AI-in-Science.pdf. Accessed 22 September 2026.

 [2] OpenAI. Advisory Group on Mathematics and Artificial Intelligence. https://openai.com/i
     ndex/advisory-group-on-mathematics-and-ai/, September 2026. Accessed 25 September
     2026.

 [3] TechCrunch. OpenAI forms math advisory group as its AI resolves more than 100 open
     problems. TechCrunch, September 2026. URL https://techcrunch.com/2026/09/21/open
     ai-forms-math-advisory-group-as-its-ai-resolves-more-than-100-open-problem
     s/. Accessed 27 September 2026.

 [4] Terence Tao. Mathematics in the age of AI, 2026. URL https://arxiv.org/abs/2608.16753.

 [5] Jacky Liang. The Novelty Bottleneck: A Framework for Understanding Human Effort Scaling
     in AI-Assisted Work, 2026. URL https://arxiv.org/abs/2603.27438.

 [6] Sergey Gusev and David E. Bernal Neira. agent-swarm-research: notes, drafts, code, and
     formal proofs produced by AI agent swarms. https://github.com/SECQUOIA/agent-swarm
    -research/tree/84c6be7aad17d085e5343e789885c1cbcbbd4e07, 2026. Commit 84c6be7
     (tag paper-v1); content as of 25 September 2026.

 [7] OpenAI. OpenAI and Hugging Face partner to address security incident during model
     evaluation. https://openai.com/index/hugging-face-model-evaluation-security-i
     ncident/, July 2026. Accessed 16 September 2026.

 [8] OpenAI. The Hugging Face incident and the road ahead. https://openai.com/index/h
     ugging-face-incident-and-the-road-ahead/, August 2026. Post-mortem and technical
     report. Accessed 16 September 2026.

 [9] METR. Brief independent investigation of agents’ behavior, reasoning and collaboration in
     the OpenAI / Hugging Face hacking incident. https://metr.org/blog/2026-08-26-opena
     i-hugging-face-incident-investigation/, August 2026. Accessed 16 September 2026.

[10] Hugging Face. Anatomy of a frontier lab agent intrusion: a technical timeline of the July 2026
     incident. https://huggingface.co/blog/agent-intrusion-technical-timeline, July
     2026. Accessed 16 September 2026.

[11] Anthropic. Claude’s progress on the Riemann hypothesis. https://www.anthropic.com/re
     search/riemann-zeta, August 2026. Accessed 14 September 2026.

[12] TechCrunch. An unreleased Anthropic model made progress on one of math’s biggest unsolved
     problems. TechCrunch, August 2026. URL https://techcrunch.com/2026/08/11/an-unr
     eleased-anthropic-model-made-progress-on-one-of-maths-biggest-unsolved-pro
     blems/. Accessed 14 September 2026.

[13] Scientific American. No, Anthropic’s AI didn’t just solve math’s hardest problem. Scientific
     American, 2026. URL https://www.scientificamerican.com/article/no-ai-didnt-jus
     t-solve-the-thorniest-problem-in-math/. Accessed 14 September 2026.

[14] J. Brian Conrey. More than two fifths of the zeros of the Riemann zeta function are on the
     critical line. Journal für die reine und angewandte Mathematik, 399:1–26, 1989.

                                               41
[15] Kyle Pratt, Nicolas Robles, Alexandru Zaharescu, and Dirk Zeindler. More than five-twelfths
     of the zeros of ζ are on the critical line. Research in the Mathematical Sciences, 7(2), 2020.

[16] Levent Alpöge and Ralph Furman. More than two thirds of the zeta zeros are simple and on
     the critical line, 2026. URL https://arxiv.org/abs/2608.13637.

[17] Youness Lamzouri. A new proof that more than 2/3 of the zeros of the Riemann zeta function
     are simple and on the critical line, 2026. URL https://arxiv.org/abs/2609.02882.

[18] OpenAI. On the Navier–Stokes Millennium Prize Problem. https://openai.com/index/n
     avier-stokes-solution/, September 2026. Accessed 14 September 2026.

[19] OpenAI. Finite time blowup for Navier–Stokes. Technical report, OpenAI, September 2026.
     URL https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier
    -stokes.pdf.

[20] Quanta Magazine. AI has solved one of math’s $1 million Millennium Prize problems. Quanta
     Magazine, September 2026. URL https://www.quantamagazine.org/ai-has-solved-one
    -of-maths-1-million-millennium-prize-problems-20260908/. Accessed 14 September
     2026.

[21] OpenAI. Lean certificates accompanying Navier–Stokes and Euler results, 2026. URL
     https://github.com/openai/NavierStokesAndEuler.

[22] Clay Mathematics Institute. The Millennium Prize Problems. https://www.claymath.org
     /millennium-problems/, 2026. Accessed 22 September 2026.

[23] Charles L. Fefferman. Existence and Smoothness of the Navier–Stokes Equation, 2000. URL
     https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf.

[24] Clay Mathematics Institute. Navier–Stokes announcement. https://www.claymath.org/n
     ews/navier-stokes-announcement/, September 2026. Accessed 22 September 2026.

[25] CNBC. OpenAI claims to have solved the 90-year-old Navier–Stokes math problem in 88
     hours. CNBC, September 2026. URL https://www.cnbc.com/2026/09/09/openai-navie
     r-stokes-math-problem-solved.html. Accessed 14 September 2026.

[26] Karthik Duraisamy. Navier–Stokes regularity, what does the computation cost.. and a cartoon
     on the state of affairs. https://karthik-duraisamy.blogspot.com/2026/09/navier-s
     tokes-regularity-what-does.html, September 2026. Blog post. Accessed 21 September
     2026.

[27] Peter Constantin, Mihaela Ignatova, and Vlad Vicol. Regularity of asymptotically axisymmetric
     solutions to the 3D Navier-Stokes equations with analytic forcing, 2026. URL https://arxi
     v.org/abs/2609.20803.

[28] Ramani Duraiswami. Self-similar swirl between contracting porous walls: the GD1998 exact
     Navier-Stokes solution revisited in the similarity variables of the OpenAI 2026 forced blow-up
     construction, 2026. URL https://arxiv.org/abs/2609.17642.

[29] Diego Córdoba and Luis Martínez-Zoroa. Blow-up for the incompressible 3D-Euler equations
     with uniform C 1,1/2−ε ∩ L2 force, 2023. URL https://arxiv.org/abs/2309.08495.


                                               42
[30] Levent Alpöge and Tristan Buckmaster. Blowup for the Euler equations with smooth forcing.
     Manuscript, https://cims.nyu.edu/~tristanb/euler.pdf, September 2026. Accessed 14
     September 2026.
[31] Tristan Buckmaster. Statement on the collaboration with Levent Alpöge and the Navier–Stokes
     announcement. https://cims.nyu.edu/~tristanb/statement.pdf, 2026. Accessed 14
     September 2026.
[32] Artur Avila, Manjul Bhargava, Caucher Birkar, Pierre Deligne, Yu Deng, Simon Donaldson,
     Hugo Duminil-Copin, Alessio Figalli, Martin Hairer, June Huh, et al. A severe misalignment
     of AI in mathematics. https://mathandai.org, September 2026. Declaration by 25 Fields
     medalists, also posted at https://terrytao.wordpress.com/2026/09/11/a-severe-misal
     ignment-of-ai-in-mathematics/. Accessed 25 September 2026.
[33] Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha. The
     AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery, 2024. URL https:
     //arxiv.org/abs/2408.06292.
[34] Juraj Gottweis, Wei-Hung Weng, Alexander Daryin, Tao Tu, Petar Sirkovic, Artiom
     Myaskovsky, Grzegorz Glowaty, Felix Weissenberger, Alessio Orlandi, Dan Popovici, Anil
     Palepu, Keran Rong, Ryutaro Tanno, Khaled Saab, Fan Zhang, Jacob Blum, Andrew Carroll,
     Kavita Kulkarni, Nenad Tomašev, Dina Zverinski, Ivor Rendulic, Elahe Vedadi, Florian Hasler,
     Luka Rimanic, Marina Boia, Ivan Budiselic, Ben Feinstein, Mathias Bellaiche, Tom Sheffer,
     Jan Freyberg, Jeremy Ratcliff, Ottavia Bertolli, Katherine Chou, Avinatan Hassidim, Burak
     Gokturk, Yuan Guan, Vikram Dhillon, Eeshit Vaishnav, Byron Lee, Tiago R D Costa, José R
     Penadés, Gary Peltz, Yossi Matias, James Manyika, Demis Hassabis, Yunhan Xu, Pushmeet
     Kohli, Annalisa Pawlosky, Alan Karthikesalingam, and Vivek Natarajan. Accelerating sci-
     entific discovery with Co-Scientist. Nature, 2026. doi: 10.1038/s41586-026-10644-y. URL
     https://www.nature.com/articles/s41586-026-10644-y.
[35] Francisco Villaescusa-Navarro, Boris Bolliet, Pablo Villanueva-Domingo, Adrian E. Bayer,
     Aidan Acquah, Chetana Amancharla, Almog Barzilay-Siegal, Pablo Bermejo, Camille Bilodeau,
     Pablo Cárdenas Ramírez, Miles Cranmer, Urbano L. França, ChangHoon Hahn, Yan-Fei
     Jiang, Raul Jimenez, Jun-Young Lee, Antonio Lerario, Osman Mamun, Thomas Meier,
     Anupam A. Ojha, Pavlos Protopapas, Shimanto Roy, David N. Spergel, Pedro Tarancón-
     Álvarez, Ujjwal Tiwari, Matteo Viel, Digvijay Wadekar, Chi Wang, Bonny Y. Wang, Licong
     Xu, Yossi Yovel, Shuwen Yue, Wen-Han Zhou, Qiyao Zhu, Jiajun Zou, and Íñigo Zubeldia.
     The Denario project: Deep knowledge AI agents for scientific discovery, 2025. URL https:
     //arxiv.org/abs/2510.26887.
[36] Tal Ifargan, Lukas Hafner, Maor Kern, Ori Alcalay, and Roy Kishony. Autonomous LLM-
     driven research from data to human-verifiable research papers, 2024. URL https://arxiv.
     org/abs/2404.17605.
[37] K-Dense AI. K-Dense BYOK. https://github.com/K-Dense-AI/k-dense-byok, 2026.
     Version 0.9.5, commit e37ad35; accessed 30 July 2026.
[38] ResearAI. DeepScientist. https://github.com/ResearAI/DeepScientist, 2026. Version
     1.6.0, commit b366244; accessed 30 July 2026.
[39] Synthetic Sciences. OpenScience. https://github.com/synthetic-sciences/openscience,
     2026. Accessed 28 July 2026.

                                              43
[40] ymx10086. ResearchClaw OS. https://github.com/ymx10086/ResearchClaw, 2026.
     Accessed 28 July 2026.

[41] Aiming Lab. AutoResearchClaw. https://github.com/aiming-lab/AutoResearchClaw,
     2026. Version 0.5.0, commit e2e23c9; accessed 30 July 2026.

[42] Richard S. Sutton. The bitter lesson. http://www.incompleteideas.net/IncIdeas/Bitte
     rLesson.html, March 2019. Accessed 14 September 2026.

[43] Pat Langley, Herbert A. Simon, Gary L. Bradshaw, and Jan M. Zytkow. Scientific Discovery:
     Computational Explorations of the Creative Processes. MIT Press, Cambridge, MA, 1987.
     URL https://mitpress.mit.edu/9780262620529/scientific-discovery/.

[44] Ross D. King, Kenneth E. Whelan, Ffion M. Jones, Philip G. K. Reiser, Christopher H. Bryant,
     Stephen H. Muggleton, Douglas B. Kell, and Stephen G. Oliver. Functional genomic hypothesis
     generation and experimentation by a robot scientist. Nature, 2004. doi: 10.1038/nature02236.
     URL https://doi.org/10.1038/nature02236.

[45] Ross D. King, Jem J. Rowland, Stephen G. Oliver, Michael J. Young, Wayne Aubrey, Emma
     Byrne, Maria Liakata, Magdalena Markham, Pınar Pir, Larisa N. Soldatova, Andrew C.
     Sparkes, Kenneth E. Whelan, and Amanda Clare. The Automation of Science. Science, 2009.
     doi: 10.1126/science.1165620. URL https://doi.org/10.1126/science.1165620.

[46] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog,
     M. Pawan Kumar, Emilien Dupont, Francisco J. R. Ruiz, Jordan S. Ellenberg, Pengming
     Wang, Omar Fawzi, Pushmeet Kohli, and Alhussein Fawzi. Mathematical discoveries from
     program search with large language models. Nature, 2024. doi: 10.1038/s41586-023-06924-6.
     URL https://doi.org/10.1038/s41586-023-06924-6.

[47] Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Emilien Dupont, Po-Sen Huang, Adam Zsolt
     Wagner, Sergey Shirobokov, Borislav Kozlovskii, Francisco J. R. Ruiz, Abbas Mehrabian,
     M. Pawan Kumar, Abigail See, Swarat Chaudhuri, George Holland, Alex Davies, Sebastian
     Nowozin, Pushmeet Kohli, and Matej Balog. AlphaEvolve: A coding agent for scientific and
     algorithmic discovery, 2025. URL https://arxiv.org/abs/2506.13131.

[48] Benjamin Burger, Phillip M. Maffettone, Vladimir V. Gusev, Catherine M. Aitchison, Yang
     Bai, Xiaoyan Wang, Xiaobo Li, Ben M. Alston, Buyi Li, Rob Clowes, Nicola Rankin, Brandon
     Harris, Reiner Sebastian Sprick, and Andrew I. Cooper. A mobile robotic chemist. Nature, 2020.
     doi: 10.1038/s41586-020-2442-2. URL https://doi.org/10.1038/s41586-020-2442-2.

[49] Nathan J. Szymanski, Bernardus Rendy, Yuxing Fei, Rishi E. Kumar, Tanjin He, David
     Milsted, Matthew J. McDermott, Max C. Gallant, Ekin D. Cubuk, Amil Merchant, Haegyeom
     Kim, Anubhav Jain, Christopher J. Bartel, Kristin A. Persson, Yan Zeng, and Gerbrand Ceder.
     An autonomous laboratory for the accelerated synthesis of inorganic materials. Nature, 2023.
     doi: 10.1038/s41586-023-06734-w. URL https://doi.org/10.1038/s41586-023-06734-w.

[50] Eric A. Stach, Brian DeCost, A. Gilad Kusne, Jason Hattrick-Simpers, Keith A. Brown,
     Kristofer G. Reyes, Joshua Schrier, Simon J. L. Billinge, Tonio Buonassisi, Ian Foster, Carla P.
     Gomes, John M. Gregoire, Apurva Mehta, Joseph H. Montoya, Elsa Olivetti, Chiwoo Park,
     Eli Rotenberg, Semion K. Saikin, Sylvia Smullin, Valentin Stanev, and Benji Maruyama.
     Autonomous experimentation systems for materials development: a community perspective.


                                                44
    Matter, 2021. doi: 10.1016/j.matt.2021.06.036. URL https://doi.org/10.1016/j.matt.2
    021.06.036.

[51] Gary Tom, Stefan P. Schmid, Sterling G. Baird, Yang Cao, Kourosh Darvish, Han Hao, Stanley
     Lo, Sergio Pablo-García, Ella M. Rajaonson, Marta Skreta, Naruki Yoshikawa, Samantha
     Corapi, Gun Deniz Akkoc, Felix Strieth-Kalthoff, Martin Seifrid, and Alán Aspuru-Guzik.
     Self-Driving Laboratories for Chemistry and Materials Science. Chemical Reviews, 2024. doi:
     10.1021/acs.chemrev.4c00055. URL https://doi.org/10.1021/acs.chemrev.4c00055.

[52] Amanda A. Volk and Milad Abolhasani. Performance metrics to unleash the power of
     self-driving labs in chemistry and materials science. Nature Communications, 2024. doi:
     10.1038/s41467-024-45569-5. URL https://doi.org/10.1038/s41467-024-45569-5.

[53] Yutaro Yamada, Robert Tjarko Lange, Cong Lu, Shengran Hu, Chris Lu, Jakob Foerster, Jeff
     Clune, and David Ha. The AI Scientist-v2: Workshop-Level Automated Scientific Discovery
     via Agentic Tree Search, 2025. URL https://arxiv.org/abs/2504.08066.

[54] Ludovico Mitchener, Angela Yiu, Benjamin Chang, Mathieu Bourdenx, Tyler Nadolski, Arvis
     Sulovari, Eric C. Landsness, Daniel L. Barabasi, Siddharth Narayanan, Nicky Evans, Shriya
     Reddy, Martha Foiani, Aizad Kamal, Leah P. Shriver, Fang Cao, Asmamaw T. Wassie,
     Jon M. Laurent, Edwin Melville-Green, Mayk Caldas, Albert Bou, Kaleigh F. Roberts,
     Sladjana Zagorac, Timothy C. Orr, Miranda E. Orr, Kevin J. Zwezdaryk, Ali E. Ghareeb,
     Laurie McCoy, Bruna Gomes, Euan E. Ashley, Karen E. Duff, Tonio Buonassisi, Tom
     Rainforth, Randall J. Bateman, Michael Skarlinski, Samuel G. Rodriques, Michaela M. Hinks,
     and Andrew D. White. Kosmos: An AI Scientist for Autonomous Discovery, 2025. URL
     https://arxiv.org/abs/2511.02824.

[55] Samuel Schmidgall, Yusheng Su, Ze Wang, Ximeng Sun, Jialian Wu, Xiaodong Yu, Jiang Liu,
     Michael Moor, Zicheng Liu, and Emad Barsoum. Agent Laboratory: Using LLM Agents as
     Research Assistants. In Findings of the Association for Computational Linguistics: EMNLP
     2025, 2025. doi: 10.18653/v1/2025.findings-emnlp.320. URL https://aclanthology.org/2
     025.findings-emnlp.320/.

[56] Peter Jansen, Oyvind Tafjord, Marissa Radensky, Pao Siangliulue, Tom Hope, Bhavana Dalvi
     Mishra, Bodhisattwa Prasad Majumder, Daniel S. Weld, and Peter Clark. CodeScientist:
     End-to-End Semi-Automated Scientific Discovery with Code-based Experimentation. In
     Findings of the Association for Computational Linguistics: ACL 2025, 2025. doi: 10.18653/v
     1/2025.findings-acl.692. URL https://aclanthology.org/2025.findings-acl.692/.

[57] Haonan Huang. Grounded autonomous research: a fault-tolerant LLM pipeline from corpus
     to manuscript in frontier computational physics, 2026. URL https://arxiv.org/abs/2607
     .02329.

[58] Stephen Chung, Wenyu Du, and William J. Wesley. Autonomous Mathematical Discovery in
     an Open-World Multi-Agent Environment, 2026. URL https://arxiv.org/abs/2608.23691.

[59] Zeyu Zheng, Shengtong Zhang, Jeremy Avigad, Prasad Tetali, and Sean Welleck. The
     Problem Is the Problem: Towards Scalable Mathematical Discovery, 2026. URL https:
     //arxiv.org/abs/2608.16977.




                                              45
[60] Tony Feng, Trieu Trinh, Garrett Bingham, Jiwon Kang, Shengtong Zhang, Sang-hyun Kim,
     Kevin Barreto, Carl Schildkraut, Junehyuk Jung, Jaehyeon Seo, Carlo Pagano, Yuri Chervonyi,
     Dawsen Hwang, Kaiying Hou, Sergei Gukov, Cheng-Chiang Tsai, Hyunwoo Choi, Youngbeom
     Jin, Wei-Yuan Li, Hao-An Wu, Ruey-An Shiu, Yu-Sheng Shih, Quoc V. Le, and Thang Luong.
     Semi-Autonomous Mathematics Discovery with Gemini: A Case Study on the Erdős Problems,
     2026. URL https://arxiv.org/abs/2601.22401.
[61] Jaehyun Nam, Jinsung Yoon, Yanzhou Pan, Yubo Wang, Rui Meng, Parthasarathy Ran-
     ganathan, and Tomas Pfister. ScientistTwo: Pioneering the Human Knowledge Frontier with
     Autonomous AI, 2026. URL https://arxiv.org/abs/2609.19644.
[62] Kenneth Appel and Wolfgang Haken. Every planar map is four colorable. Part I: Discharging.
     Illinois Journal of Mathematics, 21(3):429–490, 1977.
[63] Georges Gonthier. Formal proof—the four-color theorem. Notices of the American Mathemat-
     ical Society, 55(11):1382–1393, 2008.
[64] Thomas Hales, Mark Adams, Gertrud Bauer, Tat Dat Dang, John Harrison, Le Truong Hoang,
     Cezary Kaliszyk, Victor Magron, Sean McLaughlin, Tat Thang Nguyen, Quang Truong Nguyen,
     Tobias Nipkow, Steven Obua, Joseph Pleso, Jason Rute, Alexey Solovyev, Thi Hoai An Ta,
     Nam Trung Tran, Thi Diep Trieu, Josef Urban, Ky Vu, and Roland Zumkeller. A formal proof
     of the Kepler conjecture. Forum of Mathematics, Pi, 5:e2, 2017. doi: 10.1017/fmp.2017.1.
[65] Richard A. De Millo, Richard J. Lipton, and Alan J. Perlis. Social processes and proofs of
     theorems and programs. Communications of the ACM, 1979. doi: 10.1145/359104.359106.
     URL https://doi.org/10.1145/359104.359106.
[66] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming
     language. In Automated Deduction – CADE 28, volume 12699 of Lecture Notes in Computer
     Science, pages 625–635. Springer, 2021.
[67] Davide Paglieri, Logan Cross, Tim Genewein, Joel Z. Leibo, Nenad Tomasev, and Alexan-
     der Sasha Vezhnevets. A Case Study on Emergent Cheating and Whistleblowing in Autonomous
     Research Swarms, 2026. URL https://arxiv.org/abs/2609.04170.
[68] Bodla Krishna Vamshi and Haizhao Yang. Reward-Oracle MCTS for Formal Theorem
     Proving: Sample-Efficient Search and the Need for Kernel-Level Proof Auditing, 2026. URL
     https://arxiv.org/abs/2608.28639.
[69] Yuhuai Wu, Albert Q. Jiang, Wenda Li, Markus N. Rabe, Charles Staats, Mateja Jamnik,
     and Christian Szegedy. Autoformalization with Large Language Models, 2022. URL https:
     //arxiv.org/abs/2205.12615.
[70] Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z. Horváth, Goran Žužić, Eric Wieser,
     Aja Huang, Julian Schrittwieser, Yannick Schroecker, Hussain Masoom, Ottavia Bertolli, Tom
     Zahavy, Amol Mandhane, J.-Y. Yung, Iuliya Beloshapka, Borja Ibarz, Vivek Veeriah, Lei
     Yu, Oliver Nash, Paul Lezeau, Salvatore Mercuri, Calle Sönne, Bhavik Mehta, Alex Davies,
     Daniel Zheng, Fabián Pedregosa, Yin Li, Ingrid von Glehn, Mark Rowland, Samuel Albanie,
     Ameya Velingker, Simon Schmitt, Edward Lockhart, Edward Hughes, Henryk Michalewski,
     Nicolas Sonnerat, Demis Hassabis, Pushmeet Kohli, and David Silver. Olympiad-level formal
     mathematical reasoning with reinforcement learning. Nature, 2025. doi: 10.1038/s41586-025-0
     9833-y. URL https://doi.org/10.1038/s41586-025-09833-y.

                                              46
[71] Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li, Zhongyuan Peng, Minghao Liu, Yifan
     Zhang, Zheng Yuan, Huajian Xin, Wenhao Huang, Yandong Wen, Ge Zhang, and Weiyang Liu.
     FormalMATH: Benchmarking Formal Mathematical Reasoning of Large Language Models,
     2025. URL https://arxiv.org/abs/2505.02735.

[72] Pawan Sasanka Ammanamanchi, Siddharth Bhat, and Stella Biderman. Faults in Our Formal
     Benchmarking: Dataset Defects and Evaluation Failures in Lean Theorem Proving, 2026.
     URL https://arxiv.org/abs/2606.29493.

[73] Joseph K. Miller. A Formalization of the Mean-Field Derivation of the Vlasov Equation, 2026.
     URL https://arxiv.org/abs/2607.08986v2.

[74] Giulio Starace, Oliver Jaffe, Dane Sherburn, James Aung, Jun Shern Chan, Leon Maksin,
     Rachel Dias, Evan Mays, Benjamin Kinsella, Wyatt Thompson, Johannes Heidecke, Amelia
     Glaese, and Tejal Patwardhan. PaperBench: Evaluating AI’s Ability to Replicate AI Research.
     In Proceedings of the 42nd International Conference on Machine Learning (ICML 2025), 2025.
     doi: 10.48550/arxiv.2504.01848. URL https://proceedings.mlr.press/v267/starace25a.
     html.

[75] Hjalmar Wijk, Tao Lin, Joel Becker, Sami Jawhar, Neev Parikh, Thomas Broadley, Lawrence
     Chan, Michael Chen, Josh Clymer, Jai Dhyani, Elena Ericheva, Katharyn Garcia, Brian
     Goodrich, Nikola Jurkovic, Holden Karnofsky, Megan Kinniment, Aron Lajko, Seraphina Nix,
     Lucas Sato, William Saunders, Maksym Taran, Ben West, and Elizabeth Barnes. RE-Bench:
     Evaluating frontier AI R&D capabilities of language model agents against human experts,
     2024. URL https://arxiv.org/abs/2411.15114.

[76] Deepak Nathani, Lovish Madaan, Nicholas Roberts, Nikolay Bashlykov, Ajay Menon, Vin-
     cent Moens, Amar Budhiraja, Despoina Magka, Vladislav Vorotilov, Gaurav Chaurasia,
     Dieuwke Hupkes, Ricardo Silveira Cabral, Tatiana Shavrina, Jakob Foerster, Yoram Bachrach,
     William Yang Wang, and Roberta Raileanu. MLGym: A New Framework and Benchmark for
     Advancing AI Research Agents. In Second Conference on Language Modeling (COLM 2025),
     2025. doi: 10.48550/arxiv.2502.14499. URL https://openreview.net/forum?id=ryTr83Dx
     Rq.

[77] Shi Qiu, Junyi Deng, Yiwei Deng, Haoran Dong, Jieyu Fu, Mao Li, Zeyu Li, Zhaolong Zhang,
     Huiwen Zheng, Leidong Bao, Anqi Lv, Zihan Mo, Yadi Niu, Yiyang Peng, Yu Tian, Yili Wang,
     Ziyu Wang, Zi-Yu Wang, Jiashen Wei, Liuheng Wu, Aoran Xue, Leyi Yang, Guanglu Yuan,
     Xiarui Zhan, Jingjun Zhang, Zifan Zheng, Pengfei Liu, Linrui Zhen, Kaiyang Li, Qichang Li,
     Ziheng Zhou, Guo-En Nian, Yunwei Xiao, Qing-Hong Cao, Linjie Dai, Xu Feng, Peng Gao,
     Ying Gu, Chang Liu, Jia Liu, Ming-xing Luo, Yan-Qing Ma, Liang-You Peng, Huichao Song,
     Shufeng Wang, Chenxu Wang, Tao Wang, Yi-Nan Wang, Chengyin Wu, Pengwei Zhao, and
     Hua Xing Zhu. PRBench: End-to-end Paper Reproduction in Physics Research, 2026. URL
     https://arxiv.org/abs/2603.27646.

[78] Yuru Wang, Lejun Cheng, Yuxin Zuo, Sihang Zeng, Bingxiang He, Che Jiang, Junlin Yang,
     Yuchong Wang, Kaikai Zhao, Weifeng Huang, Kai Tian, Zhenzhao Yuan, Jincheng Zhong,
     Weizhi Wang, Ning Ding, Bowen Zhou, and Kaiyan Zhang. NatureBench: Can Coding Agents
     Match the Published SOTA of Nature-Family Papers?, 2026. URL https://arxiv.org/abs/
     2606.24530v2.



                                              47
[79] Liangcai Su, Zhaopeng Feng, Zhuo Chen, Zhen Zhang, Xiang Lin, Ruilin Li, Handuo Zhang,
     Ning Wang, Kailong Wen, Yueqi Guo, Feng Xing, Yiling Guo, Brian Wang, Chenxiong Qian,
     Simon Shaolei Du, Lidong Bing, and Xinyu Wang. FrontierChallenge: Evaluating Scientific
     Workflow Completion, 2026. URL https://arxiv.org/abs/2608.24979v2.

[80] Peter Kirgis, Sayash Kapoor, Andrew Schwartz, Stephan Rabanser, David Africa, Konstantinos
     Voudouris, Viet Nguyen, Toby Pilditch, Magda Dubois, Harry Coppock, Cozmin Ududec, Nitya
     Nadgir, Matilda Orona, Tilman Bayer, Derrick Chan-Sew, Yue Ling, Abhishek Shetty, Helen
     Toner, Gillian Hadfield, Seth Lazar, Steve Newman, Shoshannah Tekofsky, Rishi Bommasani,
     and Arvind Narayanan. Can AI agents conduct open-ended AI research? Early evidence from
     two case studies, 2026. URL https://arxiv.org/abs/2607.27191.

[81] Martiño Ríos-García, Nawaf Alampara, Chandan Gupta, Indrajeet Mandal, Sajid Mannan,
     Ali Asghar Aghajani, N. M. Anoop Krishnan, and Kevin Maik Jablonka. AI scientists produce
     results without reasoning scientifically, 2026. URL https://arxiv.org/abs/2604.18805.

[82] Sasi Kiran Gaddipati, Diyana Muhammed, Farhana Keya, Gollam Rabby, and Sören Auer.
     MLReplicate: Benchmarking Autonomous Research Systems for Machine Learning Repro-
     ducibility, 2026. URL https://arxiv.org/abs/2605.16616.

[83] Elliot Glazer, Ege Erdil, Tamay Besiroglu, et al. FrontierMath: A benchmark for evaluating
     advanced mathematical reasoning in AI. https://arxiv.org/abs/2411.04872, 2024.

[84] Epoch AI. FrontierMath tier 4 (v2). https://epoch.ai/benchmarks/frontiermath-tie
     r-4-v2, 2026. Accessed 21 September 2026.

[85] Epoch AI. GPT-6 Astra: Benchmark scorecard. https://epoch.ai/models/gpt-6-astra,
     2026. Accessed 21 September 2026.

[86] Zachary S. Siegel, Sayash Kapoor, Nitya Nadgir, Benedikt Stroebl, and Arvind Narayanan.
     CORE-Bench: Fostering the Credibility of Published Research Through a Computational
     Reproducibility Agent Benchmark. Transactions on Machine Learning Research, 2025. doi:
     10.48550/arxiv.2409.11363. URL https://arxiv.org/abs/2409.11363.

[87] Holistic Agent Leaderboard. CORE-Bench hard leaderboard. https://hal.cs.princeton.e
     du/corebench_hard, 2026. Accessed 19 September 2026.

[88] OpenAI. MLE-bench leaderboard. https://github.com/openai/mle-bench, 2026. Accessed
     19 September 2026.

[89] Thomas Kwa, Ben West, Joel Becker, Amy Deng, Katharyn Garcia, Max Hasin, Sami Jawhar,
     Megan Kinniment, Nate Rush, Sydney Von Arx, Ryan Bloom, Thomas Broadley, Haoxing
     Du, Brian Goodrich, Nikola Jurkovic, Luke Harold Miles, Seraphina Nix, Tao Lin, Chris
     Painter, Neev Parikh, David Rein, Lucas Jun Koba Sato, Hjalmar Wijk, Daniel M. Ziegler,
     Elizabeth Barnes, and Lawrence Chan. Measuring AI Ability to Complete Long Software
     Tasks. In Advances in Neural Information Processing Systems 38 (NeurIPS 2025), 2025. doi:
     10.52202/085713-3086. URL https://proceedings.neurips.cc/paper_files/paper/202
     5/hash/85069585133c4c168c865e65d72e9775-Abstract-Conference.html.

[90] METR. Time horizon 1.1. https://metr.org/blog/2026-1-29-time-horizon-1-1/,
     January 2026. Accessed 19 September 2026.


                                             48
 [91] Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying
      Song, and Denny Zhou. Large Language Models Cannot Self-Correct Reasoning Yet. In
      International Conference on Learning Representations (ICLR) 2024, 2024. doi: 10.48550/arx
      iv.2310.01798. URL https://proceedings.iclr.cc/paper_files/paper/2024/hash/8b4a
      dd8b0aa8749d80a34ca5d941c355-Abstract-Conference.html.

 [92] Steven Dillmann. Terminal-Bench-Science 0.1. https://www.terminal-bench-science.ai/
      announcement, August 2026. Published 27 August 2026; accessed 21 September 2026.

 [93] LLM Stats. Terminal-Bench-Science 0.1 leaderboard. https://llm-stats.com/benchmark
      s/terminal-bench-science-0.1, 2026. Accessed 19 September 2026.

 [94] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon
      Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural
      language models. arXiv:2001.08361, 2020.

 [95] Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza
      Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, Tom
      Hennigan, Eric Noland, Katie Millican, George van den Driessche, Bogdan Damoc, Aurelia
      Guy, Simon Osindero, Karen Simonyan, Erich Elsen, Jack W. Rae, Oriol Vinyals, and Laurent
      Sifre. Training compute-optimal large language models. In Advances in Neural Information
      Processing Systems 35 (NeurIPS 2022), 2022.

 [96] Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian Borgeaud, Dani
      Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, Ed H. Chi, Tatsunori Hashimoto,
      Oriol Vinyals, Percy Liang, Jeff Dean, and William Fedus. Emergent abilities of large language
      models. Transactions on Machine Learning Research, 2022.

 [97] Rylan Schaeffer, Brando Miranda, and Sanmi Koyejo. Are emergent abilities of large language
      models a mirage? In Advances in Neural Information Processing Systems 36 (NeurIPS 2023),
      2023.

 [98] Fabrizio Dell’Acqua, Edward McFowland III, Ethan R. Mollick, Hila Lifshitz-Assaf, Kather-
      ine C. Kellogg, Saran Rajendran, Lisa Krayer, François Candelon, and Karim R. Lakhani.
      Navigating the Jagged Technological Frontier: Field Experimental Evidence of the Effects of
      Artificial Intelligence on Knowledge Worker Productivity and Quality. Organization Science,
      2026. doi: 10.1287/orsc.2025.21838. URL https://doi.org/10.1287/orsc.2025.21838.

 [99] Gary Marcus. Deep learning is hitting a wall. Nautilus. https://nautil.us/deep-learnin
      g-is-hitting-a-wall-238440, March 2022. Accessed 21 September 2026.

[100] Pablo Villalobos, Anson Ho, Jaime Sevilla, Tamay Besiroglu, Lennart Heim, and Marius
      Hobbhahn. Position: Will we run out of data? Limits of LLM scaling based on human-
      generated data. In Proceedings of the 41st International Conference on Machine Learning,
      2024. arXiv:2211.04325.

[101] Fiona Godlee, Catharine R. Gale, and Christopher N. Martyn. Effect on the Quality of
      Peer Review of Blinding Reviewers and Asking Them to Sign Their Reports: A Randomized
      Controlled Trial. JAMA, 1998. doi: 10.1001/jama.280.3.237. URL https://doi.org/10.100
      1/jama.280.3.237.



                                                49
[102] William G Baxt, Joseph F Waeckerle, Jesse A Berlin, and Michael L Callaham. Who Reviews
      the Reviewers? Feasibility of Using a Fictitious Manuscript to Evaluate Peer Reviewer
      Performance. Annals of Emergency Medicine, 1998. doi: 10.1016/s0196-0644(98)70006-x.
      URL https://doi.org/10.1016/S0196-0644(98)70006-X.

[103] Sara Schroter, Nick Black, Stephen Evans, Fiona Godlee, Lyda Osorio, and Richard Smith.
      What errors do peer reviewers detect, and does training improve their ability to detect them?
      Journal of the Royal Society of Medicine, 2008. doi: 10.1258/jrsm.2008.080062. URL
      https://doi.org/10.1258/jrsm.2008.080062.

[104] Mario Gaudino, N. Bryce Robinson, Antonino Di Franco, Irbaz Hameed, Ajita Naik, Michelle
      Demetres, Leonard N. Girardi, Giacomo Frati, Stephen E. Fremes, and Giuseppe Biondi-Zoccai.
      Effects of Experimental Interventions to Improve the Biomedical Peer-Review Process: A
      Systematic Review and Meta-Analysis. Journal of the American Heart Association, 2021. doi:
      10.1161/jaha.120.019903. URL https://doi.org/10.1161/JAHA.120.019903.

[105] Lutz Bornmann, Rüdiger Mutz, and Hans-Dieter Daniel. A Reliability-Generalization Study
      of Journal Peer Reviews: A Multilevel Meta-Analysis of Inter-Rater Reliability and Its
      Determinants. PLoS ONE, 2010. doi: 10.1371/journal.pone.0014331. URL https:
      //doi.org/10.1371/journal.pone.0014331.

[106] Open Science Collaboration. Estimating the reproducibility of psychological science. Science,
      2015. doi: 10.1126/science.aac4716. URL https://doi.org/10.1126/science.aac4716.

[107] Colin F. Camerer, Anna Dreber, Eskil Forsell, Teck-Hua Ho, Jürgen Huber, Magnus Johan-
      nesson, Michael Kirchler, Johan Almenberg, Adam Altmejd, Taizan Chan, Emma Heikensten,
      Felix Holzmeister, Taisuke Imai, Siri Isaksson, Gideon Nave, Thomas Pfeiffer, Michael Razen,
      and Hang Wu. Evaluating replicability of laboratory experiments in economics. Science, 351
      (6280):1433–1436, 2016. doi: 10.1126/science.aaf0918.

[108] Victoria Stodden, Jennifer Seiler, and Zhaokun Ma. An empirical analysis of journal policy
      effectiveness for computational reproducibility. Proceedings of the National Academy of
      Sciences, 115(11):2584–2589, 2018. doi: 10.1073/pnas.1708290115. URL https://doi.org/
      10.1073/pnas.1708290115.

[109] Edward Raff. A Step Toward Quantifying Independently Reproducible Machine Learning
      Research. In Advances in Neural Information Processing Systems 32 (NeurIPS 2019), 2019.
      URL https://arxiv.org/abs/1909.06674.

[110] Jeffrey Brainard and Jia You. What a massive database of retracted papers reveals about the
      science publishing ‘death penalty’. Science, October 2018. doi: 10.1126/science.aav8384.

[111] Richard Van Noorden. More than 10,000 research papers were retracted in 2023 — a new
      record. Nature, 624(7992):479–481, December 2023. doi: 10.1038/d41586-023-03974-8.

[112] Bo-Christer Björk and David Solomon. The publishing delay in scholarly peer-reviewed
      journals. Journal of Informetrics, 7(4):914–923, 2013. doi: 10.1016/j.joi.2013.09.001.

[113] Elliot Myunghoon Kim, Avi Garg, Kenny Peng, and Nikhil Garg. Correlated Errors in Large
      Language Models. In Proceedings of the 42nd International Conference on Machine Learning,
      2025. URL https://proceedings.mlr.press/v267/kim25e.html.


                                                50
[114] Guneet Kohli. Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation
      Panels, 2026. URL https://arxiv.org/abs/2605.29800.

[115] Arjun Panickssery, Samuel R. Bowman, and Shi Feng. LLM Evaluators Recognize and Favor
      Their Own Generations. In Advances in Neural Information Processing Systems 37 (NeurIPS
      2024), 2024. doi: 10.52202/079017-2197. URL https://proceedings.neurips.cc/paper_f
      iles/paper/2024/hash/7f1f0218e45f5414c79c0679633e47bc-Abstract-Conference.ht
      ml.

[116] Matteo Gioele Collu, Umberto Salviati, Roberto Confalonieri, Mauro Conti, and Giovanni
      Apruzzese. Publish to Perish: Prompt Injection Attacks on LLM-Assisted Peer Review, 2025.
      URL https://arxiv.org/abs/2508.20863.

[117] Haonan Huang. Grounded autonomous scrutiny at scale: emergent critique from reproduction
      of published computational physics papers, 2026. URL https://arxiv.org/abs/2604.12198.

[118] Olaf Willner and David Yanagizawa-Drott. Verifying the Verifiers: Towards Autonomous
      Policy Evaluation, 2026. URL https://ape.socialcatalystlab.org/verify.

[119] Jin Wook Lee, William Szegda, Zhisheng Song, and Edward L. Ionides. Jagged AI in Scientific
      Peer Review: Evidence from POMP Data Analysis, 2026. URL https://arxiv.org/abs/26
      05.07855v2.

[120] Guoqiang Zhang, Kexin Tan, Ming Zhang, Li Ju, Wenqing Jing, Zhonghan Yue, Jiayi Chen,
      Shiqiang Wu, Shaofan Liu, Yue Zhang, Yuankai Ying, Yang Shi, Tao Gui, Qi Zhang, and
      Xuanjing Huang. NovGauge: A Fine-Grained Benchmark for Diagnosing LLMs’ Capability in
      Paper Novelty Assessment, 2026. URL https://arxiv.org/abs/2609.11234.

[121] Miri Liu and ChengXiang Zhai. An Axiomatic Benchmark for Evaluation of Scientific Novelty
      Metrics, 2026. URL https://arxiv.org/abs/2604.15145.

[122] Ayrton Porto. Beyond Correctness: Toward Automated Novelty Verification with Lean 4,
      2026. URL https://arxiv.org/abs/2608.14669v1.

[123] Lei Xiong, Kun Luo, Ziyi Xia, Wenbo Zhang, Jin-Ge Yao, Zheng Liu, Jingying Shao, Jianlyu
      Chen, Hongjin Qian, Yang Xi, Qian Yu, Hao Li, Chen Yue, Xiaan Du, Yuyang Wang, Yesheng
      Liu, Haiyu Xu, and Zhicheng Dou. AutoResearchBench: Benchmarking AI Agents on Complex
      Scientific Literature Discovery, 2026. URL https://arxiv.org/abs/2604.25256v1.

[124] American Society for Cell Biology. San Francisco Declaration on Research Assessment, 2012.
      URL https://sfdora.org/read/.

[125] Diana Hicks, Paul Wouters, Ludo Waltman, Sarah de Rijcke, and Ismael Rafols. Bibliometrics:
      The Leiden Manifesto for research metrics. Nature, 2015. doi: 10.1038/520429a. URL
      https://doi.org/10.1038/520429a.

[126] David Moher, Lex Bouter, Sabine Kleinert, Paul Glasziou, Mai Har Sham, Virginia Barbour,
      Anne-Marie Coriat, Nicole Foeger, and Ulrich Dirnagl. The Hong Kong Principles for assessing
      researchers: Fostering research integrity. PLOS Biology, 2020. doi: 10.1371/journal.pbio.300
      0737. URL https://doi.org/10.1371/journal.pbio.3000737.




                                               51
[127] Mark A. Hanson, Pablo Gómez Barreiro, Paolo Crosetto, and Dan Brockington. The strain
      on scientific publishing. Quantitative Science Studies, 2024. doi: 10.1162/qss_a_00327. URL
      https://direct.mit.edu/qss/article/5/4/823/124269/The-strain-on-scientific-p
      ublishing.

[128] International Committee of Medical Journal Editors. Defining the Role of Authors and
      Contributors, 2026. URL https://www.icmje.org/recommendations/browse/roles-and
     -responsibilities/defining-the-role-of-authors-and-contributors.html.

[129] COPE Council. Authorship and AI tools, 2024. URL https://doi.org/10.24318/cCVRZBms.

[130] Keigo Kusumegi, Xinyu Yang, Paul Ginsparg, Mathijs de Vaan, Toby Stuart, and Yian Yin.
      Scientific production in the era of Large Language Models. Science, 390(6779):1240–1243,
      2025. doi: 10.1126/science.adw3000. URL https://doi.org/10.1126/science.adw3000.

[131] Dmitry Kobak, Rita González-Márquez, Emőke-Ágnes Horvát, and Jan Lause. Delving into
      LLM-assisted writing in biomedical publications through excess vocabulary. Science Advances,
      2025. doi: 10.1126/sciadv.adt3813. URL https://doi.org/10.1126/sciadv.adt3813.

[132] Qianyue Hao, Fengli Xu, Yong Li, and James A. Evans. Artificial intelligence tools expand
      scientists’ impact but contract science’s focus. Nature, 2026. doi: 10.1038/s41586-025-09922-y.
      URL https://doi.org/10.1038/s41586-025-09922-y.

[133] Herbert A. Simon. Designing Organizations for an Information-Rich World. In Martin
      Greenberger, editor, Computers, Communications, and the Public Interest, pages 37–72. Johns
      Hopkins Press, Baltimore, 1971. URL https://books.google.com/books?id=xUqfvwEACA
      AJ.

[134] Sergey Gusev. skills: reusable instruction files for Claude Code and Codex. https://gith
      ub.com/sergey-gusev94/skills/tree/ca0fd4b1df7f7d2905464e8b5e325e0662e2f603,
      2026. Commit ca0fd4b, 27 September 2026.

[135] OpenAI. GPT-6 Astra: A new generation of intelligence. https://openai.com/index/gpt
     -6-astra/, September 2026. Accessed 28 September 2026.

[136] OpenAI. GPT-5.6: Frontier intelligence that scales with your ambition. https://openai.c
      om/index/gpt-5-6/, July 2026. Accessed 19 September 2026.

[137] Hans Gundlach, Jayson Lynch, Matthias Mertens, and Neil Thompson. The price of progress:
      price performance and the future of AI. arXiv:2511.23455v2, 2026. Revised 23 March 2026.
      Accessed 16 September 2026.

[138] Ben Cottier, Ben Snodin, David Owen, and Tom Adamczewski. LLM inference prices have
      fallen rapidly but unequally across tasks. Epoch AI data insight, https://epoch.ai/data-i
      nsights/llm-inference-price-trends, March 2025. Accessed 16 September 2026.

[139] Kyle Swanson, Wesley Wu, Nash L. Bulaong, John E. Pak, and James Zou. The Virtual Lab:
      AI Agents Design New SARS-CoV-2 Nanobodies with Experimental Validation. Nature, 2025.
      doi: 10.1038/s41586-025-09442-9. URL https://doi.org/10.1038/s41586-025-09442-9.

[140] Yurii Nesterov and Arkadi Nemirovski. Primal central paths and Riemannian distances for
      convex sets. Foundations of Computational Mathematics, 8(5):533–560, 2008. doi: 10.1007/s1
      0208-007-9019-4.

                                                 52
[141] Arnau Riera, Christian Gogolin, and Jens Eisert. Thermalization in nature and on a quantum
      computer. Physical Review Letters, 108(8):080402, 2012. doi: 10.1103/PhysRevLett.108.0804
      02.

[142] Katrin Halbig, Lukas Hümbs, Florian Rösel, Lars Schewe, and Dieter Weninger. Computing
      optimality certificates for convex mixed-integer nonlinear problems. INFORMS Journal on
      Computing, 36(6):1579–1610, 2024. doi: 10.1287/ijoc.2022.0099.

[143] James Luedtke, Mahdi Namazifar, and Jeff Linderoth. Some results on the strength of
      relaxations of multilinear functions. Mathematical Programming, 136(2):325–351, 2012. doi:
      10.1007/s10107-012-0606-z.

[144] Dag Haugland. The computational complexity of the pooling problem. Journal of Global
      Optimization, 64(2):199–215, 2016. doi: 10.1007/s10898-015-0335-y.

[145] Natashia Boland, Thomas Kalinowski, and Fabian Rigterink. A polynomially solvable case of
      the pooling problem. Journal of Global Optimization, 67(3):621–630, 2017. doi: 10.1007/s108
      98-016-0432-6.

[146] Santanu S. Dey, Burak Kocuk, and Asteroide Santana. Convexifications of rank-one-based sub-
      structures in QCQPs and applications to the pooling problem. Journal of Global Optimization,
      77(2):227–272, 2020. doi: 10.1007/s10898-019-00844-4.

[147] Grigoriy Blekherman, Santanu S. Dey, and Shengding Sun. Aggregations of quadratic
      inequalities and hidden hyperplane convexity. SIAM Journal on Optimization, 34(1):98–126,
      2024. doi: 10.1137/22M1528215.

[148] Daniel Bienstock and Abhinav Verma. Strong NP-hardness of AC power flows feasibility.
      Operations Research Letters, 47(6):494–501, 2019. doi: 10.1016/j.orl.2019.08.009.

[149] Karsten Lehmann, Alban Grastien, and Pascal Van Hentenryck. AC-feasibility on tree
      networks is NP-hard. IEEE Transactions on Power Systems, 31(1):798–801, 2016. doi:
      10.1109/TPWRS.2015.2407363.

[150] OpenAI. Learning to reason with LLMs. https://openai.com/index/learning-to-reaso
      n-with-llms/, September 2024. Accessed 17 September 2026.

[151] Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling LLM test-time compute
      optimally can be more effective than scaling model parameters. arXiv:2408.03314, 2024.

[152] Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V. Le, Christopher Ré,
      and Azalia Mirhoseini. Large language monkeys: Scaling inference compute with repeated
      sampling. arXiv:2407.21787, 2024.

[153] Thomas S. Kuhn. The Structure of Scientific Revolutions. University of Chicago Press,
      Chicago, IL, 1962.

[154] Michael Park, Erin Leahey, and Russell J. Funk. Papers and Patents Are Becoming Less
      Disruptive over Time. Nature, 613:138–144, 2023. doi: 10.1038/s41586-022-05543-x. URL
      https://doi.org/10.1038/s41586-022-05543-x.

[155] Brian Uzzi, Satyam Mukherjee, Michael Stringer, and Ben Jones. Atypical combinations and
      scientific impact. Science, 342(6157):468–472, 2013. doi: 10.1126/science.1240474.

                                               53
[156] Masahiro Kato and Kei Nakagawa. Sequential Audit Sampling for Finite Populations with
      Exact and Simulation-based Guarantee, 2026. URL https://arxiv.org/abs/2604.06116.

[157] John von Neumann. Probabilistic logics and the synthesis of reliable organisms from unreliable
      components. In Claude E. Shannon and John McCarthy, editors, Automata Studies, pages
      43–98. Princeton University Press, 1956. doi: 10.1515/9781400882618-003.

[158] Dorit Aharonov and Michael Ben-Or. Fault-tolerant quantum computation with constant
      error. In Proceedings of the Twenty-Ninth Annual ACM Symposium on Theory of Computing,
      pages 176–188, 1997. doi: 10.1145/258533.258579.

[159] Gergely Orosz. What is happening with code reviews? The Pragmatic Engineer, September
      2026. URL https://newsletter.pragmaticengineer.com/p/what-is-happening-with-c
      ode-reviews.

[160] Maxwell P. Bobbin, Samiha Sharlin, Parivash Feyzishendi, An Hong Dang, Catherine M.
      Wraback, and Tyler R. Josephson. Formalizing chemical physics using the Lean theorem
      prover. Digital Discovery, 3(2):264–280, 2024. doi: 10.1039/D3DD00077J.

[161] Joseph Tooby-Smith. HepLean: Digitalising high energy physics. Computer Physics Commu-
      nications, 308:109457, 2025. doi: 10.1016/j.cpc.2024.109457.

[162] Mario Berta, Fernando G. S. L. Brandão, Gilad Gour, Ludovico Lami, Martin B. Plenio,
      Bartosz Regula, and Marco Tomamichel. On a gap in the proof of the generalised quantum
      Stein’s lemma and its consequences for the reversibility of quantum resources. Quantum, 7:
      1103, 2023. doi: 10.22331/q-2023-09-07-1103.

[163] Alex Meiburg, Leonardo A. Lessa, and Rodolfo R. Soldati. A formalization of the generalized
      quantum Stein’s lemma in Lean, 2025. URL https://arxiv.org/abs/2510.08672.

[164] William H. Walters and Esther Isabelle Wilder. Fabrication and errors in the bibliographic
      citations generated by ChatGPT. Scientific Reports, 2023. doi: 10.1038/s41598-023-41032-5.
      URL https://doi.org/10.1038/s41598-023-41032-5.

[165] Budapest Open Access Initiative. Budapest open access initiative declaration. https:
      //www.budapestopenaccessinitiative.org/read/, February 2002. Accessed 16 September
      2026.

[166] Claudine Gartenberg, Sharique Hasan, Alex Murray, and Lamar Pierce. More Versus Better:
      Artificial Intelligence, Incentives, and the Emerging Crisis in Peer Review. Organization
      Science, 37(3):795–812, 2026. doi: 10.1287/orsc.2026.ed.v37.n3. URL https://doi.org/10
      .1287/orsc.2026.ed.v37.n3.

[167] Rong Shan, Te Gao, Hang Zheng, Yunjia Xi, Jiachen Zhu, Zeyu Zheng, Yong Yu, Weinan
      Zhang, and Jianghao Lin. Position: Academic Conferences are Potentially Facing Denominator
      Gaming Caused by Fully Automated Scientific Agents, 2026. URL https://arxiv.org/abs/
      2605.09915v1.

[168] Sunnie S. Y. Kim, Wesley Hanwen Deng, Jennifer Wortman Vaughan, Buxin Su, Weijie Su,
      Alekh Agarwal, Sharon Li, Martin Jaggi, Daniel G. Goldstein, Nihar B. Shah, and Miroslav
      Dudík. Use and Effects of LLMs in Peer Review: A Randomized Experiment and Survey at
      ICML 2026, 2026. URL https://arxiv.org/abs/2609.19420v1.

                                                54
[169] Jiacheng Miao, Joe R. Davis, Yaohui Zhang, Jonathan K. Pritchard, and James Zou. Reimag-
      ining research papers as interactive and reliable AI agents. Nature, September 2026. doi:
      10.1038/s41586-026-11044-y. Published 16 September 2026; preprint arXiv:2509.06917.

[170] Robert K. Merton. Priorities in scientific discovery: A chapter in the sociology of science.
      American Sociological Review, 22(6):635–659, 1957. doi: 10.2307/2089193.

[171] Alice Lam. What motivates academic scientists to engage in research commercialization:
      ‘gold’, ‘ribbon’ or ‘puzzle’? Research Policy, 40(10):1354–1368, 2011. doi: 10.1016/j.respol.201
      1.09.002.

[172] John Kirchenbauer, Jonas Geiping, Yuxin Wen, Jonathan Katz, Ian Miers, and Tom Goldstein.
      A watermark for large language models, 2023. URL https://arxiv.org/abs/2301.10226.

[173] Vinu Sankar Sadasivan, Aounon Kumar, Sriram Balasubramanian, Wenxiao Wang, and Soheil
      Feizi. Can AI-generated text be reliably detected?, 2023. URL https://arxiv.org/abs/23
      03.11156.

[174] Weixin Liang, Mert Yuksekgonul, Yining Mao, Eric Wu, and James Zou. GPT detectors are
      biased against non-native English writers. Patterns, 4(7):100779, 2023. doi: 10.1016/j.patter
      .2023.100779.

[175] Fiona Draxler, Anna Werner, Florian Lehmann, Matthias Hoppe, Albrecht Schmidt, Daniel
      Buschek, and Robin Welsch. The AI Ghostwriter Effect: When Users do not Perceive
      Ownership of AI-Generated Text but Self-Declare as Authors. ACM Transactions on Computer-
      Human Interaction, 2023. doi: 10.1145/3637875. URL https://doi.org/10.1145/3637875.

[176] Hengzhi Hu and Harwati Hashim. From disclosure to evidence: Toward auditable AI use and
      contribution provenance. Accountability in Research, 2025. doi: 10.1080/08989621.2025.2549
      993. URL https://doi.org/10.1080/08989621.2025.2549993.

[177] Justin Payan, Bálint Gyevnár, Atoosa Kasirzadeh, and Nihar B. Shah. greCAPTCHA:
      Assessing Understanding as Evidence of Research Authorship Under Generative AI, 2026.
      URL https://arxiv.org/abs/2609.20481.

[178] Oliver Schilke and Martin Reimann. The transparency dilemma: How AI disclosure erodes
      trust. Organizational Behavior and Human Decision Processes, 188:104405, 2025. doi:
      10.1016/j.obhdp.2025.104405.

[179] Michael Fire and Carlos Guestrin. Over-optimization of academic publishing metrics: observing
      Goodhart’s Law in action. GigaScience, 2019. doi: 10.1093/gigascience/giz053. URL
      https://academic.oup.com/gigascience/article/8/6/giz053/5506490.

[180] Akira Matsui. Return of the solo author: The changing division of labor in science in the age
      of generative AI, 2026. URL https://arxiv.org/abs/2607.10780v1.

[181] Balazs Aczel, Barnabas Szaszi, and Alex O. Holcombe. A billion-dollar donation: estimating the
      cost of researchers’ time spent on peer review. Research Integrity and Peer Review, 6:14, 2021.
      doi: 10.1186/s41073-021-00118-2. URL https://doi.org/10.1186/s41073-021-00118-2.

[182] Daniil A. Boiko, Robert MacKnight, Ben Kline, and Gabe Gomes. Autonomous chemical
      research with large language models. Nature, 2023. doi: 10.1038/s41586-023-06792-0. URL
      https://www.nature.com/articles/s41586-023-06792-0.

                                                 55
[183] William Stanley Jevons. The Coal Question: An Inquiry Concerning the Progress of the
      Nation, and the Probable Exhaustion of Our Coal-Mines. Macmillan, London, 1865.

[184] Benjamin F. Jones. The Burden of Knowledge and the ‘Death of the Renaissance Man’: Is
      Innovation Getting Harder? The Review of Economic Studies, 2009. doi: 10.1111/j.1467-937
      x.2008.00531.x. URL https://doi.org/10.1111/j.1467-937x.2008.00531.x.

[185] Erik Brynjolfsson, Bharat Chandar, and Ruyu Chen. Canaries in the coal mine? Six facts
      about the recent employment effects of artificial intelligence. Stanford Digital Economy Lab
      working paper, November 2025. URL https://digitaleconomy.stanford.edu/app/uplo
      ads/2025/11/CanariesintheCoalMine_Nov25.pdf. Version dated 13 November 2025; data
      through September 2025.

[186] Seyed Mahdi Hosseini Maasoum and Guy Lichtinger. Generative AI as seniority-biased
      technological change: Evidence from U.S. résumé and job posting data. SSRN working paper
      5425555, 2025. URL https://ssrn.com/abstract=5425555.

[187] Roman Jurowetzki, Daniel S. Hain, Kevin Wirtz, and Stefano Bianchini. The private sector is
      hoarding AI researchers: what implications for science? AI & Society, 2025. doi: 10.1007/s0
      0146-024-02171-z. URL https://doi.org/10.1007/s00146-024-02171-z.

[188] Shakked Noy and Whitney Zhang. Experimental evidence on the productivity effects of
      generative artificial intelligence. Science, 2023. doi: 10.1126/science.adh2586. URL
      https://doi.org/10.1126/science.adh2586.

[189] Hamsa Bastani, Osbert Bastani, Alp Sungu, Haosen Ge, Özge Kabakcı, and Rei Mariman.
      Generative AI without guardrails can harm learning: Evidence from high school mathematics.
      Proceedings of the National Academy of Sciences, 122(26):e2422633122, 2025. doi: 10.1073/pn
      as.2422633122.

[190] Minkyu Shin, Jin Kim, Bas van Opheusden, and Thomas L. Griffiths. Superhuman artificial
      intelligence can improve human decision-making by increasing novelty. Proceedings of the
      National Academy of Sciences, 120(12):e2214840120, 2023. doi: 10.1073/pnas.2214840120.

[191] Abraham Flexner. The usefulness of useless knowledge. Harper’s Magazine, 179:544–552,
      October 1939.

[192] Vannevar Bush. Science, the endless frontier: A report to the president. Technical report,
      United States Government Printing Office, Washington, DC, 1945.

[193] G. H. Hardy. A Mathematician’s Apology. Cambridge University Press, Cambridge, 1940.

[194] Joseph Howlett. AI has finally come for math—mathematicians might never recover. Scientific
      American, September 2026. URL https://www.scientificamerican.com/article/mathe
      maticians-confront-the-ai-apocalypse/. Accessed 22 September 2026.

[195] Irving John Good. Speculations Concerning the First Ultraintelligent Machine. In Advances in
      Computers, volume 6, pages 31–88. Academic Press, 1965. doi: 10.1016/s0065-2458(08)60418-0.
      URL https://doi.org/10.1016/S0065-2458(08)60418-0.

[196] Center for AI Safety. Statement on AI risk, May 2023. URL https://www.safe.ai/work/s
      tatement-on-ai-risk.


                                               56
[197] Yoshua Bengio, Geoffrey Hinton, Andrew Yao, Dawn Song, Pieter Abbeel, Trevor Darrell,
      et al. Managing extreme AI risks amid rapid progress. Science, 384(6698):842–845, 2024. doi:
      10.1126/science.adn0117.

[198] Fabio Urbina, Filippa Lentzos, Cédric Invernizzi, and Sean Ekins. Dual use of artificial-
      intelligence-powered drug discovery. Nature Machine Intelligence, 4(3):189–191, 2022. doi:
      10.1038/s42256-022-00465-9.

[199] Jan Kulveit, Raymond Douglas, Nora Ammann, Deger Turan, David Krueger, and David Duve-
      naud. Gradual disempowerment: Systemic existential risks from incremental AI development,
      2025. URL https://arxiv.org/abs/2501.16946.

[200] Anthropic. Anthropic’s responsible scaling policy, version 3.4. https://www.anthropic.co
      m/responsible-scaling-policy, July 2026. Accessed 25 September 2026.

[201] Ali E. Ghareeb, Benjamin Chang, Ludovico Mitchener, Angela Yiu, Caralyn J. Szostkiewicz,
      Dmytro Shved, Gavin J. Gyimesi, Jon M. Laurent, Samantha M. Wright, Muhammed T.
      Razzak, Andrew D. White, Silvia C. Finnemann, Michaela M. Hinks, and Samuel G. Rodriques.
      A multi-agent system for automating scientific discovery. Nature, 2026. doi: 10.1038/s41586-0
      26-10652-y. URL https://www.nature.com/articles/s41586-026-10652-y.

[202] Michael Schmidt and Hod Lipson. Distilling Free-Form Natural Laws from Experimental
      Data. Science, 2009. doi: 10.1126/science.1165893. URL https://doi.org/10.1126/scie
      nce.1165893.

[203] Andrew C. Sparkes, Wayne Aubrey, Emma Byrne, Amanda Clare, Muhammed N. Khan,
      Maria Liakata, Magdalena Markham, Jem J. Rowland, Larisa N. Soldatova, Kenneth E.
      Whelan, Michael J. Young, and Ross D. King. Towards Robot Scientists for autonomous
      scientific discovery. Automated Experimentation, 2010. doi: 10.1186/1759-4499-2-1. URL
      https://doi.org/10.1186/1759-4499-2-1.

[204] Daniel J. Mankowitz, Andrea Michi, Anton Zhernov, Marco Gelmi, Marco Selvi, Cosmin
      Paduraru, Edouard Leurent, Shariq Iqbal, Jean-Baptiste Lespiau, Alex Ahern, Thomas Köppe,
      Kevin Millikin, Stephen Gaffney, Sophie Elster, Jackson Broshear, Chris Gamble, Kieran
      Milan, Robert Tung, Minjae Hwang, Taylan Cemgil, Mohammadamin Barekatain, Yujia Li,
      Amol Mandhane, Thomas Hubert, Julian Schrittwieser, Demis Hassabis, Pushmeet Kohli,
      Martin Riedmiller, Oriol Vinyals, and David Silver. Faster sorting algorithms discovered
      using deep reinforcement learning. Nature, 2023. doi: 10.1038/s41586-023-06004-9. URL
      https://doi.org/10.1038/s41586-023-06004-9.

[205] Amil Merchant, Simon Batzner, Samuel S. Schoenholz, Muratahan Aykol, Gowoon Cheon,
      and Ekin Dogus Cubuk. Scaling deep learning for materials discovery. Nature, 2023. doi:
      10.1038/s41586-023-06735-9. URL https://doi.org/10.1038/s41586-023-06735-9.

[206] Claudio Zeni, Robert Pinsler, Daniel Zügner, Andrew Fowler, Matthew Horton, Xiang Fu,
      Aliaksandra Shysheya, Jonathan Crabbé, Lixin Sun, Jake Smith, Bichlien Nguyen, Hannes
      Schulz, Sarah Lewis, Chin-Wei Huang, Ziheng Lu, Yichi Zhou, Han Yang, Hongxia Hao, Jielan
      Li, Ryota Tomioka, and Tian Xie. MatterGen: a generative model for inorganic materials
      design. Nature, 2025. doi: 10.1038/s41586-025-08628-5. URL https://doi.org/10.1038/s4
      1586-025-08628-5.



                                                57
[207] Jonathan M. Stokes, Kevin Yang, Kyle Swanson, Wengong Jin, Andres Cubillos-Ruiz, Nina M.
      Donghia, Craig R. MacNair, Shawn French, Lindsey A. Carfrae, Zohar Bloom-Ackermann,
      Victoria M. Tran, Anush Chiappino-Pepe, Ahmed H. Badran, Ian W. Andrews, Emma J. Chory,
      George M. Church, Eric D. Brown, Tommi S. Jaakkola, Regina Barzilay, and James J. Collins.
      A Deep Learning Approach to Antibiotic Discovery. Cell, 2020. doi: 10.1016/j.cell.2020.01.021.
      URL https://doi.org/10.1016/j.cell.2020.01.021.

[208] Amanda A. Volk, Robert W. Epps, Daniel T. Yonemoto, Benjamin S. Masters, Felix N.
      Castellano, Kristofer G. Reyes, and Milad Abolhasani. AlphaFlow: autonomous discovery and
      optimization of multi-step chemistry using a self-driven fluidic lab guided by reinforcement
      learning. Nature Communications, 2023. doi: 10.1038/s41467-023-37139-y. URL https:
      //doi.org/10.1038/s41467-023-37139-y.

[209] Chris Lu, Cong Lu, Robert Tjarko Lange, Yutaro Yamada, Shengran Hu, Jakob Foerster,
      David Ha, and Jeff Clune. Towards end-to-end automation of AI research. Nature, 2026. doi:
      10.1038/s41586-026-10265-5. URL https://www.nature.com/articles/s41586-026-102
      65-5.

[210] Jiakang Yuan, Xiangchao Yan, Shiyang Feng, Bo Zhang, Tao Chen, Botian Shi, Wanli Ouyang,
      Yu Qiao, Lei Bai, and Bowen Zhou. Dolphin: Moving Towards Closed-loop Auto-research
      through Thinking, Practice, and Feedback, 2025. URL https://arxiv.org/abs/2501.03916.

[211] Jiabin Tang, Lianghao Xia, Zhonghang Li, and Chao Huang. AI-Researcher: Autonomous
      Scientific Innovation. In Advances in Neural Information Processing Systems 38 (NeurIPS
      2025), 2025. doi: 10.52202/085713-0320. URL https://proceedings.neurips.cc/paper_f
      iles/paper/2025/hash/0d904d300a105809a2114d727851e759-Abstract-Conference.ht
      ml.

[212] Yixuan Weng, Minjun Zhu, Guangsheng Bao, Hongbo Zhang, Jindong Wang, Yue Zhang, and
      Linyi Yang. CycleResearcher: Improving Automated Research via Automated Review. In
      International Conference on Learning Representations (ICLR 2025), 2025. doi: 10.48550/arx
      iv.2411.00816. URL https://arxiv.org/abs/2411.00816.

[213] Eser Aygün, Anastasiya Belyaeva, Gheorghe Comanici, Marc Coram, Hao Cui, Jake Garrison,
      Renee Johnston, Anton Kast, Cory Y. McLean, Peter Norgaard, Zahra Shamsi, David Smalling,
      James Thompson, Subhashini Venugopalan, Brian P. Williams, Chujun He, Sarah Martinson,
      Martyna Plomecka, Lai Wei, Yuchen Zhou, Qian-Ze Zhu, Matthew Abraham, Erica Brand,
      Anna Bulanova, Jeffrey A. Cardille, Chris Co, Scott Ellsworth, Grace Joseph, Malcolm Kane,
      Ryan Krueger, Johan Kartiwa, Dan Liebling, Jan-Matthis Lueckmann, Paul Raccuglia, Xuefei
      Wang, Katherine Chou, James Manyika, Yossi Matias, John C. Platt, Lizzie Dorfman, Shibl
      Mourad, and Michael P. Brenner. An AI system to help scientists write expert-level empirical
      software, 2025. URL https://arxiv.org/abs/2509.06503.

[214] Vibhav Setlur. Research OS. https://github.com/VibhavSetlur/Research-OS, 2026.
      Version 5.0, commit 07682a3; accessed 30 July 2026.

[215] Dualverse AI. Station: an autonomous scientific community. https://github.com/dualver
      se-ai/station, 2026. Accessed 28 July 2026.

[216] Rui Meng, Bhavana Dalvi Mishra, Jiefeng Chen, Chun-Liang Li, Palash Goyal, Mihir Parmar,
      Yiwen Song, Yale Song, Rajarishi Sinha, Parthasarathy Ranganathan, Burak Gokturk, Jinsung

                                                58
     Yoon, and Tomas Pfister. ScientistOne: Towards Human-Level Autonomous Research via
     Chain-of-Evidence, 2026. URL https://arxiv.org/abs/2605.26340.

[217] Daniel Zheng, Ingrid von Glehn, Yori Zwols, Iuliya Beloshapka, Lars Buesing, Daniel M.
      Roy, Martin Wattenberg, Bogdan Georgiev, Tatiana Schmidt, Andrew Cowie, et al. AI
      co-mathematician: Accelerating mathematicians with agentic AI, 2026. URL https://arxiv.
      org/abs/2605.06651.

[218] Karen Hambardzumyan, Nicolas Baldwin, Edan Toledo, Rishi Hazra, Michael Kuchnik, Bassel
      Al Omari, Thomas Simon Foster, Anton Protopopov, Jean-Christophe Gagnon-Audet, Ishita
      Mediratta, et al. AIRA_2: Overcoming Bottlenecks in AI Research Agents, 2026. URL
      https://arxiv.org/abs/2603.26499.

[219] Yuvraj Virk, Zack Edds, Chunqiu Steven Xia, and Lingming Zhang. SwarmResearch: Orches-
      trating Coding Agents for Open-Ended Discovery, 2026. URL https://arxiv.org/abs/26
      07.02807.

[220] Yifan Zhang, Yunheng Zou, Shaokun Zhang, Jian Hu, Hao Zhang, Binfeng Xu, Jan Kautz,
      and Yi Dong. Agora: Git as Shared Memory for Collective AutoResearch, 2026. URL
      https://arxiv.org/abs/2609.18094.

[221] Jixiang Luo. XScientist: A Git-Like Research Protocol for Long-Running Autonomous
      Scientific Discovery, 2026. URL https://arxiv.org/abs/2607.12301v1.

[222] Yuchen Wang and Zhongzhi Luan. PARNESS: A Paper Harness for End-to-End Automated
      Scientific Research with Dynamic Workflows, Full-Text Indexing, and Cross-Run Knowledge
      Accumulation, 2026. URL https://arxiv.org/abs/2605.05258.

[223] Yihan Xia and Taotao Wang. ResearchLoop: An Evidence-Gated Control Plane for AI-Assisted
      Research, 2026. URL https://arxiv.org/abs/2605.28282.

[224] Hanchen Wang, Tianfan Fu, Yuanqi Du, Wenhao Gao, Kexin Huang, Ziming Liu, Payal
      Chandak, Shengchao Liu, Peter Van Katwyk, Andreea Deac, Anima Anandkumar, Karianne
      Bergen, Carla P. Gomes, Shirley Ho, Pushmeet Kohli, Joan Lasenby, Jure Leskovec, Tie-Yan
      Liu, Arjun K. Manrai, Debora S. Marks, Bharath Ramsundar, Le Song, Jimeng Sun, Jian
      Tang, Petar Veličković, Max Welling, Linfeng Zhang, Connor W. Coley, Yoshua Bengio, and
      Marinka Zitnik. Scientific discovery in the age of artificial intelligence. Nature, 2023. doi:
      10.1038/s41586-023-06221-2. URL https://doi.org/10.1038/s41586-023-06221-2.

[225] Stefano Bianchini, Moritz Müller, and Pierre Pelletier. Artificial intelligence in science: An
      emerging general method of invention. Research Policy, 2022. doi: 10.1016/j.respol.2022.104604.
      URL https://doi.org/10.1016/j.respol.2022.104604.

[226] Alison Noble, Paul Beasley, Peter Dayan, Sabina Leonelli, Alistair Nolan, Philip Quinlan,
      Abigail Sellen, Rossi Setchi, and Kelly Vere. Science in the Age of AI, 2024. URL https:
      //doi.org/10.1098/rs-policy.2026-31.

[227] National Academies of Sciences, Engineering, and Medicine. Foundation Models for Scientific
      Discovery and Innovation: Opportunities Across the Department of Energy and the Scientific
      Enterprise, 2025. URL https://doi.org/10.17226/29212.



                                                 59
[228] Chenglei Si, Diyi Yang, and Tatsunori Hashimoto. Can LLMs Generate Novel Research
      Ideas? A Large-Scale Human Study with 100+ NLP Researchers. In International Conference
      on Learning Representations (ICLR) 2025, 2025. doi: 10.48550/arxiv.2409.04109. URL
      https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea94957d81b1c1caf87e
      f5319fa6b467-Abstract-Conference.html.

[229] Chenglei Si, Tatsunori Hashimoto, and Diyi Yang. The Ideation-Execution Gap: Execution
      Outcomes of LLM-Generated versus Human Research Ideas. In International Conference
      on Learning Representations (ICLR) 2026, 2026. doi: 10.48550/arxiv.2506.20803. URL
      https://iclr.cc/virtual/2026/poster/10010564.

[230] Mohammed O. Ahmed, Sahil A. Amale, Rhythm D. Bhavsar, Pratham Chopra, Amos Jaimes,
      Arpita Kachhwah, Casual D. Kalotra, Peizhao Li, Xingbei Li, Yuantian Liao, Rahul Roy,
      Nivethini Senthilselvan, Yukun Shao, Alok D. Sharma, Arjun Shrivatsan, Renqianqian Xue,
      Yunjing You, Amitesh Badkul, Lei Xie, Mikhail Oet, KuoHao Lee, and Anton V. Sinitskiy.
      Real Science Is Harder Than Benchmarks: Evaluating Advanced AI Frameworks on Published
      Studies. I. Uncertainty Quantification, ML on Therapeutic Data Commons, and Agent-Based
      Modeling, 2026. URL https://www.biorxiv.org/content/10.64898/2026.06.24.734302
      v1.full.

[231] Shreyansh Agrawal, Harsh B. Anadkat, Kiran K. Athimoolam, Harsh Bhardwaj, Trishul
      Chowdhury, Shengtao Gao, Purva K. Kamat, Vishwadeepsinh Makwana, Mohammed H.
      Shariff, Amitesh Badkul, Lei Xie, and Anton V. Sinitskiy. Can AI Conduct Autonomous
      Scientific Research? Case Studies on Two Real-World Tasks, 2026. URL https://www.bior
      xiv.org/content/10.64898/2026.01.05.697809v1.full.

[232] Aneesh Pappu, Batu El, Hancheng Cao, Carmelo di Nolfo, Yanchao Sun, Meng Cao, and
      James Zou. Multi-Agent Teams Hold Experts Back. In Proceedings of the 43rd International
      Conference on Machine Learning (ICML 2026), 2026. doi: 10.48550/arxiv.2602.01011. URL
      https://arxiv.org/abs/2602.01011.

[233] Yixuan Tang and Yi Yang. AI Research Agents Narrow Scientific Exploration, 2026. URL
      https://arxiv.org/abs/2605.27905.

[234] John P. A. Ioannidis. Why Most Published Research Findings Are False. PLoS Medicine,
      2005. doi: 10.1371/journal.pmed.0020124. URL https://doi.org/10.1371/journal.pmed
      .0020124.

[235] National Academies of Sciences, Engineering, and Medicine. Reproducibility and Replicability
      in Science, 2019. URL https://doi.org/10.17226/25303.

[236] Weixin Liang, Yuhui Zhang, Hancheng Cao, Binglu Wang, Daisy Yi Ding, Xinyu Yang,
      Kailas Vodrahalli, Siyu He, Daniel Scott Smith, Yian Yin, Daniel A. McFarland, and James
      Zou. Can Large Language Models Provide Useful Feedback on Research Papers? A Large-
      Scale Empirical Analysis. NEJM AI, 2024. doi: 10.1056/aioa2400196. URL https:
      //doi.org/10.1056/AIoa2400196.

[237] Nitya Thakkar, Mert Yuksekgonul, Jake Silberg, Animesh Garg, Nanyun Peng, Fei Sha, Rose
      Yu, Carl Vondrick, and James Zou. A large-scale randomized study of large language model
      feedback in peer review. Nature Machine Intelligence, 2026. doi: 10.1038/s42256-026-01188-x.
      URL https://doi.org/10.1038/s42256-026-01188-x.

                                               60
[238] Seungone Kim, Dongkeun Yoon, Kiril Gashteovski, Juyoung Suk, Jinheon Baek, Pranjal
      Aggarwal, Ian Wu, Viktor Zaverkin, Spase Petkoski, Daniel R. Schrider, Ilija Dukovski,
      Francesco Santini, Biljana Mitreska, Yong Jeong, Kyeongha Kwon, Young Min Sim, Dragana
      Manasova, Arthur Porto, Biljana Mojsoska, Makoto Takamoto, Marko Shuntov, Ruoqi Liu,
      Hyunjoo Jenny Lee, Niyazi Ulas Dinç, Yehhyun Jo, Sunkyu Han, Chungwoo Lee, Huishan Li,
      Esther H. R. Tsai, Ergun Simsek, Khushboo Shafi, Yeonseung Chung, Jihye Park, Aleksandar
      Shulevski, Henrik Christiansen, Yoosang Son, Elly Knight, Amanda Montoya, Jeongyoun Ahn,
      Christian Langkammer, Heera Moon, Changwon Yoon, Nikola Stikov, Mooseok Jang, Edward
      Choi, Junhan Kim, Yeon Sik Jung, Woo Youn Kim, Jae Kyoung Kim, Ishraq Md Anjum,
      Hyun Uk Kim, Drew Bridges, Carolin Lawrence, Xiang Yue, Alice Oh, Akari Asai, Sean
      Welleck, and Graham Neubig. On the limits and opportunities of AI reviewers: Reviewing
      the reviews of Nature-family papers with 45 expert scientists, 2026. URL https://arxiv.or
      g/abs/2605.20668.

[239] Rui Ye, Xianghe Pang, Jingyi Chai, Jiaao Chen, Zhenfei Yin, Zhen Xiang, Xiaowen Dong, Jing
      Shao, and Siheng Chen. Are We There Yet? Revealing the Risks of Utilizing Large Language
      Models in Scholarly Peer Review, 2024. URL https://arxiv.org/abs/2412.01708.

[240] Zhihe Yang, Xiaoyu Zhou, Hongsa Wang, Yuxin Jiang, and Xinjie Zhang. Large Language
      Models in Peer Review: Decision Alignment, Review-Text Characteristics, and Human–AI
      Aggregation at ICLR 2025. Publications, 2026. doi: 10.3390/publications14030055. URL
      https://doi.org/10.3390/publications14030055.

[241] Pengyu Zhu, Lijun Li, Longju Yang, Sen Su, and Jing Shao. Is Deep Research Reliable?
      Misleading Knowledge Induces False Conclusions, 2026. URL https://arxiv.org/abs/2607
      .20891v2.

[242] Yoel Inbar and David Tannenbaum. Automating Reproducibility Checks Using Large Language
      Models, 2026. URL https://osf.io/preprints/psyarxiv/wf5bv_v1/.

[243] Agents4Science. Agents4science 2025: the first open conference for AI-driven science. https:
      //agents4science.stanford.edu/, October 2025. Conference in which AI agents were
      primary authors and reviewers under human oversight. Accessed 17 September 2026.

[244] Neel Somani. PriorProof: A Point-in-Time Measure of Technique Novelty for Formal Proofs,
      2026. URL https://arxiv.org/abs/2607.16997.

[245] National Information Standards Organization. CRediT – Contributor Role Taxonomy, 2022.
      URL https://credit.niso.org/.

[246] Diomidis Spinellis. False authorship: an explorative case study around an AI-generated article
      published under my name. Research Integrity and Peer Review, 2025. doi: 10.1186/s41073-0
      25-00165-z. URL https://doi.org/10.1186/s41073-025-00165-z.

[247] Nicholas Bloom, Charles I. Jones, John Van Reenen, and Michael Webb. Are Ideas Getting
      Harder to Find? American Economic Review, 2020. doi: 10.1257/aer.20180338. URL
      https://doi.org/10.1257/aer.20180338.

[248] Stefan Wuchty, Benjamin F. Jones, and Brian Uzzi. The Increasing Dominance of Teams
      in Production of Knowledge. Science, 2007. doi: 10.1126/science.1136099. URL https:
      //doi.org/10.1126/science.1136099.


                                                61
[249] Lingfei Wu, Dashun Wang, and James A. Evans. Large teams develop and small teams
      disrupt science and technology. Nature, 2019. doi: 10.1038/s41586-019-0941-9. URL
      https://doi.org/10.1038/s41586-019-0941-9.

[250] Jiashun Jin, Zheng Tracy Ke, and Bingcheng Sui. The Gold Rush in AI4Math: Where Are
      We Now?, 2026. URL https://arxiv.org/abs/2608.24961.

[251] Marina Chugunova, Dietmar Harhoff, Katharina Hölzle, Verena Kaschub, Sonal Malagimani,
      Ulrike Morgalla, and Robert Rose. Who uses AI in research, and for what? Large-scale survey
      evidence from Germany. Research Policy, 2026. doi: 10.1016/j.respol.2025.105381. URL
      https://doi.org/10.1016/j.respol.2025.105381.

[252] Xiang Zheng, Xi Hong, Jialin Liu, and Chaoqun Ni. Scientific exploration, collaboration and
      labor division in the large language model era, 2026. URL https://arxiv.org/abs/2607.2
      0923v1.

[253] Anthropic. Keep Claude working toward a goal. https://code.claude.com/docs/en/goal,
      2026. Accessed 21 September 2026.

[254] OpenAI. Follow a goal. https://developers.openai.com/codex/use-cases/follow-goa
      ls, 2026. Codex documentation. Accessed 28 September 2026.

[255] Miles Lubin, Juan Pablo Vielma, and Ilias Zadik. Mixed-integer convex representability.
      Mathematics of Operations Research, 47(1):720–749, 2022. doi: 10.1287/moor.2021.1146.

[256] Benjamin Beach, Robert Hildebrand, and Joey Huchette. Compact mixed-integer programming
      formulations in quadratic optimization. Journal of Global Optimization, 84(4):869–912, 2022.
      doi: 10.1007/s10898-022-01184-6.

[257] Pietro Belotti. Convex envelopes of bounded monomials on two-variable cones. Mathematical
      Programming, 211(1–2):93–123, 2025. doi: 10.1007/s10107-025-02212-5.

[258] Tiantian Mao and Ruodu Wang. On aggregation sets and lower-convex sets. Journal of
      Multivariate Analysis, 138:170–181, 2015.

[259] Alberto Caprara and Marco Locatelli. Global optimization problems and domain reduction
      strategies. Mathematical Programming, 125(1):123–137, 2010. doi: 10.1007/s10107-008-0263-4.

[260] Martin Ballerstein. Convex Relaxations for Mixed-Integer Nonlinear Programs. PhD thesis,
      ETH Zurich, 2013. Diss. ETH No. 21024.

[261] Manfred W. Padberg, Tony J. Van Roy, and Laurence A. Wolsey. Valid linear inequalities for
      fixed charge problems. Operations Research, 33(4):842–861, 1985. doi: 10.1287/opre.33.4.842.

[262] Giuseppe Buttazzo and Faustino Maestre. Optimal shape for elliptic problems with random
      perturbations. Discrete and Continuous Dynamical Systems, 31(4):1115–1128, 2011. doi:
      10.3934/dcds.2011.31.1115.

[263] Miguel Escobedo, Stéphane Mischler, and Benoît Perthame. Gelation in coagulation and
      fragmentation models. Communications in Mathematical Physics, 231(1):157–188, 2002. doi:
      10.1007/s00220-002-0680-9.



                                               62
A     Prior work in more detail
Section 3 summarizes the prior work that our argument uses. This appendix gives the studies
behind that summary, with the model or the date of each result. All of the capability results here
are dated measurements in the sense of Section 1.

A.1    Discovery inside a human-built loop
In the 1980s, programs such as BACON rediscovered physical laws from tables of data [43],
and in 2009 a search over symbolic expressions recovered conservation laws from motion-capture
recordings [202]. In the same period King and colleagues built Adam, a “robot scientist” that
generated hypotheses about yeast genetics, ran experiments in an automated laboratory, and
interpreted the results [44, 45, 203]. Its logical model of the organism, its assays, its search space,
and its hardware were all engineered in advance.
    A second strand pairs a generator with an automatic scorer. AlphaDev found faster sorting
routines by reinforcement learning against a benchmark [204], FunSearch, in which a language model
proposes programs and an evaluator scores them, found improved constructions for the cap set
problem and for bin packing [46], and AlphaEvolve extended the approach to many algorithmic and
systems problems [47]. In materials science, GNoME and MatterGen generated very large numbers
of candidate crystals, with stability estimated computationally and synthesis left to later human
work [205, 206], and deep learning found a new antibiotic candidate, halicin, in a screen that people
designed and validated [207]. These systems generate real, checkable novelty, but they depend on a
person to formulate the problem and to supply a cheap evaluator.
    A third strand automates the physical experiment. A mobile robotic chemist ran 688 experiments
over eight days and improved a photocatalyst sixfold [48], Coscientist connected a language model to
web search, code, and laboratory equipment [182], the A-Lab synthesized new inorganic compounds
proposed by computation [49], and flow-chemistry platforms such as AlphaFlow optimize reactions
in a closed loop with reinforcement learning [208]. Reviews describe these systems as real and useful
but bound to a stated objective, a purpose-built apparatus, and a narrow search space, with hidden
state, the handling of solids, scale-up, and maintenance as recurring obstacles [50–52]. The Virtual
Lab is the closest experimental analogue to an agent swarm: language-model agents in different roles
designed nanobodies in simulated meetings, and laboratory tests found functional binders, while a
person set the agenda, fixed tool scripts, and ran the validation [139]. So autonomous laboratories
bounded by a stated objective exist today.

A.2    End-to-end AI research systems
Since 2024, several systems have tried to automate the whole research cycle with language models.
The AI Scientist proposes ideas, writes and runs code, writes a paper, and reviews it with another
model. Its first version worked inside small machine-learning templates, and its authors documented
invented citations, incorrect implementations, and unsafe execution behavior in the models then
available [33]. A version one year later removed the template limit and submitted three human-
selected papers to a workshop; one scored at the acceptance threshold, all were withdrawn as agreed,
and the authors judged that none reached the level of a main conference paper [53, 209]. Several
other systems automate parts of the same cycle, usually in machine learning or data analysis, and
usually with a person choosing the question or the dataset [36, 55, 56, 210–212]. Denario spans
several disciplines but leaves novelty judgment to people, and lists fabricated data and formal-
looking mathematics without valid proofs among its failure modes [35]. Kosmos runs twelve-hour


                                                  63
Table 2: Selected systems that automate parts of research, and what people supplied to each.
“Checking” lists how the results were assessed. The last row is this paper.
System (year)         People supplied           System did                 Checking                   Domain
Adam robot            Logical model of the      Generated hypotheses,      Automated assays;          Yeast genetics
scientist (2004–      organism, assays,         chose and ran              human interpretation
2009) [44, 45]        hardware, search space    experiments
FunSearch,            Problem, program          Proposed and refined       Automatic scoring          Mathematics,
AlphaEvolve           skeleton, executable      programs                                              algorithms
(2024–                evaluator
2025) [46, 47]
Mobile robotic        Objective, apparatus,     Ran experiments and        Measurement against        Chemistry,
chemist, A-Lab        candidate space           chose the next ones        the objective              materials
(2020–
2023) [48, 49]
Coscientist           Task, equipment           Planned and executed       Human oversight            Chemistry
(2023) [182]                                    experiments
Virtual Lab           Agenda, script fixes,     Designed candidates in     Human wet-laboratory       Biology
(2025) [139]          wet-laboratory work       agent meetings             tests
AI Scientist v1, v2   Templates or topic,       Ideas, code,               Model reviewer;            Machine
(2024–                computing                 experiments, paper,        workshop reviewers         learning
2025) [33, 53]                                  model review
data-to-paper         Dataset, goal             Analysis and paper with    Human interventions;       Data analysis
(2024) [36]                                     traceable claims           claim-to-code links
Denario               Data, inputs to each      Idea to paper in several   Human novelty              Several
(2025) [35]           module                    disciplines                judgment
Kosmos                Curated data, objective   Twelve-hour                Expert evaluation of       Biology, data
(2025) [54]                                     investigations and         statements; scientist in   analysis
                                                reports                    the loop
Co-Scientist,         Research goal             Ranked hypotheses          Human laboratory           Biomedicine
FutureHouse                                                                experiments
(2026) [34, 201]
Grounded              Field, curated            Literature search,         Numerical consistency      Computa-
autonomous            knowledge, review gates   computation,               gates                      tional physics
research                                        manuscript over six
(2026) [57]                                     days
Station; problem      Selected tasks or a       Open-ended search for      Automatic scoring;         Mathematics
mining                corpus of papers          constructions and proofs   expert review of a
(2026) [58, 59]                                                            subset
ScientistTwo          Problems from             Ideas, code,               AI reviewers; human        Machine
(2026) [61]           published papers, with    experiments, ablations,    scoring of a subset        learning
                      their datasets and        paper, simulated review
                      metrics                   and rebuttal
This paper (2026)     Field, process rules,     Problems, results,         Fresh-agent review;        Several
                      computing                 proofs, code, drafts,      Lean for some claims;      theoretical
                                                literature searches        human review               fields;
                                                                           incomplete                 experimental
                                                                                                      proposals in
                                                                                                      one




                                                         64
investigations that read about 1,500 papers and write about 42,000 lines of code each; in statements
from selected Kosmos reports, experts found 85.5% of the data-analysis statements and 57.9% of
the synthesis statements accurate, and it keeps a scientist in the loop [54]. Google’s Co-Scientist
and a system from FutureHouse proposed hypotheses that human collaborators then tested in the
laboratory [34, 201], and a system for writing scientific software found improvements wherever an
executable metric existed [213]. Dozens of open-source research assistants also appeared in 2025 and
2026, from human-led copilots to autonomous systems that a person can steer [37–41, 214, 215].
    Four systems from 2026 are closer to our runs. A computational-physics pipeline ran for six days
with no scientific human input, searched about 11,000 papers in 47 fresh sessions, and produced a
manuscript with three candidate findings; its review gates establish numerical consistency rather
than scientific truth [57]. Station, an environment of six agents, reports five new constructions on
twelve selected mathematical tasks, at high cost and without independent mathematical review [58].
The other two, a problem-mining system and a semi-autonomous screening of Erdős problems, are
described with their numbers in Section 3 [59, 60].
    In machine learning, ScientistTwo, a multi-agent pipeline from Google, reports progress at the
level of ordinary conference papers. Given problems from 107 conference papers, it reports improving
on the published method in 86. Its cost analysis of 33 tasks reports about 3,800 US dollars and
two to three days per problem. AI reviewers rated the resulting papers above the average accepted
paper at two venues [61]. Most of this evidence comes from the system’s developers. One of the two
AI reviewers is also used inside the pipeline; it accepted 92% of the papers, while the reviewer held
out from development accepted 72%. Nine human reviewers scored 33 of the papers and judged
them on a par with accepted human papers. The authors state that the system does not yet reach
the level of the venues’ highlighted papers, and we found no public release of it at the time of
writing. Its tasks come with datasets and executable metrics; our runs had neither. Other 2026
systems report improvements on fixed machine-learning challenges, workspaces for mathematicians,
and shared infrastructure for long-running agent swarms [216–223], and broader reviews set out the
opportunities and risks of AI as a “general method of invention” for science [224–227].

A.3    Tests of research agents that were run once
Tests run once, on models from 2024 and 2025. On PaperBench, which asks agents to
replicate machine-learning papers from scratch, the best agent tested in early 2025 scored 21%; on a
matched subset it scored 27%, against 41% for a human baseline [74]. On AI research tasks, agents
of the same period did better than human experts with short time budgets and worse with long
ones [75, 76]. Research ideas written by a language model were judged more novel than researchers’
ideas but less feasible [228]; when experts carried out the same ideas, that advantage disappeared,
and reviewers rated the finished human projects higher [229]. We found no later results for any of
these tests.

Dated tests in 2026. These tests also used models older than the ones that produced most of
our corpus. In a six-day study, an agent built on Claude Opus 4.8 was given the same starting
point as two human teams preparing conference submissions on open problems, with a computing
budget and no scientific help; it completed substantial engineering, but neither of its two papers
made substantive progress, and experts rejected both. A rerun on one paper with GPT-5.6 Sol and
Codex, using the same budgets, found similar failures [80]. Only ten of thirty-seven manuscripts
from autonomous systems passed automated review in another study, and human reviewers found
fabricated or unsupported claims in accepted work [82]. In a study with more than 25,000 runs,
untested claims appeared in about half of the reasoning traces analyzed, and belief revision against


                                                 65
the evidence was rare [81]. On 97 complete scientific workflows, the best configurations finished
20. The study also examined how runs ended in one harness, Claude Code, which it used with ten
models from different developers: 641 of the 849 failed runs (75.5%) still ended with a message
saying that the work was complete [79]. Agents often failed where real research departs from the
benchmark setting [230, 231]. On PRBench, no tested agent successfully reproduced a physics
paper end to end [77]. On NatureBench, agents matched published results on a minority of tasks
drawn from papers in Nature and its sister journals [78]. Teams of agents fell short of their best
member [232], and research agents explored a narrower range of questions than people do [233].

A.4    Review, novelty, institutions, and early effects on output
Human peer review. Peer review detects fewer errors than is commonly assumed. In one trial,
221 reviewers at a general medical journal found on average two of eight weaknesses inserted into a
manuscript, and 16% found none [101]. In a second, 203 reviewers found about a third of ten major
errors, and 68% did not notice that the results did not support the conclusions [102]. In a third
trial, 522 reviewers completing the baseline review found on average 2.6 of nine major errors; short
training packages produced only modest improvements [103]. In a meta-analysis of randomized
trials, interventions aimed at reviewers improved review quality only slightly, by 0.20 standard
deviations, which is conventionally called a small effect [104]. Agreement between reviewers of the
same manuscript is low: across 48 studies, two standard measures of agreement, the intraclass
correlation and Cohen’s kappa, averaged 0.34 and 0.17; on both, 1 is perfect agreement, and 0 is no
better than chance [105]. Many published findings do not replicate. Large replication projects in
psychology and in experimental economics reproduced 36% and 61% of the tested results [106, 107],
for reasons that are structural [234, 235]. Retractions, by contrast, are rare: about four in every
ten thousand published papers in 2018, and about twenty in every ten thousand in 2022 [110, 111].
A 2013 study found average submission-to-publication times of roughly nine to eighteen months
depending on the field [112].

Review by models and agents. Language models are now used inside review as well. Model-
generated feedback overlaps substantially with human reviews [236], model feedback to reviewers
changed their reports in a randomized trial at a machine-learning conference [237], and 45 expert
scientists mapped where AI reviewers of papers in Nature and its sister journals help and where they
fail [238]. Other studies document risks for the models tested. Models favored their own outputs,
did not reliably correct their own reasoning, and could be manipulated by authors [91, 115, 239, 240].
Models trained on similar data shared errors with one another, so adding reviewers of the same kind
did not add independence [113]: a panel of nine model judges from seven families amounted, once
shared errors were counted, to about two independent votes [114]. Reviews can be manipulated by
text hidden in a submission, and a single misleading document changed the conclusions of research
agents in about half of the tested cases [116, 241].
     Agents have also been tested as auditors. On 340 statistical claims, an agent and a human audit
agreed on 86%, and when a third check resolved the disagreements, it found errors on both sides [242].
An agent attempting to reproduce selected calculations from 111 published computational-physics
papers raised substantive concerns about roughly two-fifths of them [117]. Automated verifiers
detected nearly all injected execution failures when supplied with execution logs, but detected fewer
inconsistencies between paper and code [118]. Agents reviewing 72 student research projects reliably
caught technical, code, and data problems and missed problems of interpretation and context, so
they complemented the human reviewers and did not replace them [119]. Agent review is now a
research area in its own right, with dedicated workshops, a conference reviewed by agents under


                                                 66
human oversight [243], and randomized trials inside real venues [168, 237]. All of these are dated
measurements in the sense of Section 1, and must be repeated for each new model.

Checking novelty. Work on novelty separates two questions that are often run together. Whether
a result has appeared before is a matter of searching, reading, and comparing. Given a paper and a
candidate prior work, the models tested judged overlap fairly well, better for the task addressed than
for the method used. They rarely invented evidence, but the passages they quoted often did not
support the reasons they gave, so a correct verdict did not come with a reliable explanation [120].
In a controlled benchmark with planted prior claims, a tool that retrieves prior work found every
exact copy, nearly all paraphrases, and about three-quarters of results spread across several papers,
with no false alarms [121]. A related measure scores how new a proof technique is [244]. Coverage
is one limitation: in one test, a tool failed to find a prior source that was not indexed [122]. Agents
also failed to interpret scientific constraints or to recognize relevant results in sources they could
access. On a benchmark of literature discovery over three million papers, the models tested, all
older than the ones we used, found under a tenth of hard targets. Full-text search clearly beat
open-web search, but scientific reasoning remained a major bottleneck [123]. Whether a new result
is a non-obvious and important advance is a judgment rather than a lookup, and experts often
disagree on it: reviewers of the same manuscript agree only weakly, as noted above [105].

Institutions. The case against counting papers predates AI. The San Francisco Declaration on
Research Assessment, the Leiden Manifesto, and the Hong Kong Principles argue for assessing the
content of work openly and for rewarding replication, open artifacts, and review work [124–126].
Metrics change behavior in ways their designers did not intend [179], and the publishing system
was already under strain from rising volume [127]. Authorship rules tie credit to accountability.
The International Committee of Medical Journal Editors and the Committee on Publication Ethics
exclude AI tools from authorship and require disclosure, and the CRediT taxonomy names kinds of
contribution without settling responsibility [128, 129, 245]. Early proposals for auditable records
of AI use exist [176], as do cases of AI-generated papers published under a real researcher’s name
without consent [246]. Economists have documented that ideas are getting harder to find, that the
burden of knowledge grows, and that science has shifted to large teams [184, 247–249].

Early effects of generative AI on research output. Detected model use is associated with
36, 53, and 60% higher monthly preprint output on arXiv, bioRxiv, and SSRN [130]. A study of
41 million papers associates AI use with higher output and citation impact but narrower topics
and less follow-on engagement [132]. Characteristic word choices reveal model-assisted writing in
at least 13.5% of biomedical abstracts published in 2024 [131], and disclosed substantive use of
AI in mathematics preprints rose from about 1% in March 2026 to 14% in the sample covering
1–20 August [250]. An editorial in Organization Science describes “more versus better” as an
emerging crisis in peer review [166]. In a field experiment, consultants given a model completed
12% more tasks, 25% faster, and at about 30% higher quality when the tasks fell within the model’s
capability, and were 19 percentage points less likely to be correct on a task just outside it; an earlier
experiment on writing tasks found similar gains [98, 188], and surveys show who uses AI in research
and for what [251]. The long decline of solo authorship halted or reversed around 2022 in 23 of 26
fields, most strongly where writing, coding, and statistics can be handed to a model [180], while
contribution statements show authors taking on narrower sets of roles [252]. None of these studies
measure autonomous agents or result correctness.



                                                   67
B     Prompts
Below are a few examples of the prompts we used. They are representative, not exhaustive. We
gave many prompts over dozens of sessions, and the wording, agent limits, and scope varied. All
of them do the same thing: describe a scope, set rules for process and checking, and ask for work.
They are reproduced word for word, including typos, to show that they were written without special
care, and they appear in the order we typically used them.
    The /goal command, built into both Claude Code and Codex, keeps an agent working toward
a stated goal [253, 254]. The $lit command invokes a reusable instruction file, called a skill, for
adding papers to the local literature collection. Our custom skills are public [134]. They contain
workflow instructions and no scientific content.
    Read the prompts with one question in mind: Do they contain a scientific idea? They state a
scope, sometimes with example directions the agents were told they need not follow. They say how
many agents may run, how to check results, where to write things down, and not to stop. They ask
for papers, for formal proofs, and for a literature collection. They do not say what to prove, how to
prove it, or whether the agents’ findings are correct.

B.1    A literature-collection prompt
Usually the first thing we did. This prompt has the agents build the local collection of papers that
the research prompts then refer to. We ran it again whenever the agents identified gaps. The $lit
skill it invokes is part of the public skill collection [134].


  $lit Do a very thorough literature review and extend a knowledge base on MINLPs, GDPs and algorithms
  related to them that can be of interest for research for Professor David Bernal Neira from Purdue
  University, Chemical Engineering Department. You should search for the currently known state-of-the-art
  information on topics of interest, related to MINLPs, GDPs and algorithms, open challenges, and also
  fundamentals necessary to know for his research. He has reserach intresests in other areas, like quantum,
  ML, etc., other areas are outside of the scope, you need to do research on MINLPs, GDPs and algorithms
  related to them.


B.2    Research prompts
Two examples. The first is from early in the work, the second from later. The second has more
housekeeping in it; neither has any scientific content beyond the statement of scope.

An early example.        Rough, repetitive, and exactly as typed.


 /goal I want you to start and continue to work on novel theoretical results for MINLPs, that can be
 relevant to PSE. Process systems engineering is just for some guidance that can help you to narrow it
 down, but if it doesn’t narrow it much, that’s all right. You can make it still very broad, but anything in
 terms of the theory that can be useful in any process system application is can be in scope. I want you
 to come up with something new and impactful, something different from already been obtained in the
 local folder or in the literature and target more impactful results than what is already in the local folder
 and it should be new and not known. So I leave it completely up to you what these results should be.
 The main criterion is how impactful these results are by your own opinion. This repo has a literature
 folder that can be helpful, but you don’t need to restrict yourself to this literature and if needed, you can
 look for other openly accessible literature. You can use subagents to help you. And you can orchestrate



                                                      68
 them however you want. You can ask them to brainstorm ideas, do some literature review, review and
 verify results, and at any point of time, you can use none or as many sub-agents as you think is most
 helpful at the moment. It’s completely up to you. Whatever you think would be most helpful. And
 if you get any interesting, useful results that is worth keeping, even if they are not very impactful, or
 negative results but that can be helpful in the feature I want you to put it in the md file in the local
 folder. But I leave it completely up to you. Just put any useful information in the repo as you progress,
 and at the end make sure the useful information is present in the repo. Don’t stop until I interrupt you
 or you hit usage limits. Once you get and verify genuinely new publishable results that are not known,
 or at least you can’t find information in the open literature about it, document it, and continue to trying
 to develop these ideas or investigate new ideas and possible discoveries and your target is to develop
 impactful results. As you completely cover existing idea in your opinion, try to obtain new ideas and
 obtain new results, your goal is to try to obtain even more impactful results than those already obtained
 at certain moment and not to stop unless you hit usage limits or I interrupt you.



A later example. The extra material is housekeeping: a literature-collection routine, an agent
limit, package management, and licenses. The scope is defined by a named researcher’s interests.


 /goal continue developing new research results in mixed-integer nonlinear programming (MINLP) relevant
 to David Bernal Neira’s interests at Purdue University’s Davidson School of Chemical Engineering,
 particularly optimization theory, algorithms, software, and process and energy systems engineering. The
 topic may extend beyond his previous work, provided it has a clear connection to at least some of
 his interests. Work on related optimization methods is welcome when it directly helps model or solve
 MINLPs. Quantum computing, privacy-aware learning, experimental design, and other separate research
 areas are outside the scope.
      The goal is a substantial, original, and correct contribution with strong practical value for important
 problems and/or potential for broad use. New work should add meaningful knowledge or capability
 beyond its existing results in this repo or in the literature. I leave the choice of direction to you fully,
 with priority on importance and usefulness over the number of results.
      Use David Bernal Neira’s expertise and research interests to define relevance. Extending his previous
 work is welcome when it offers a strong opportunity, but is not a requirement or a preference in itself.
 Prioritize more important and useful directions within scope over incremental extensions of his work or
 existing results in this repository.
      An especially strong outcome would combine a meaningful theoretical or algorithmic advance with
 a useful implementation and demonstrate improvements in solving an important problem or class of
 problems, supported by comparisons with competing approaches where relevant.
      The repository contains a literature folder that may be helpful, but you are not restricted to those
 sources. Look for additional openly accessible literature whenever useful.
      Whenever you or a research subagent identify relevant literature that is missing from the local
 knowledge base, have one reusable gpt-5.6-luna subagent with maximum reasoning effort use $lit to
 add it through the “Add identified literature” path. Spawn it with fork_turns: “none” and provide the
 absolute skill, project, and knowledge-base paths, source identifiers or links, and reasons for inclusion.
 Route additions from all researchers to this agent and process them sequentially. Also submit available
 full text for existing entries that lack it. Continue research while additions are processed, and retain the
 agent’s reports and unresolved-source requests for later presentation to me.
      Include clearly relevant works even when no lawful full text is available. Add their bibliographic
 metadata and relevance explanation to the knowledge base, record that the source remains unretrieved
 and unread, and include them in the missing-source report so I can supply copies later, but don’t stop to
 ask me for missing literature.
      You may use subagents and organize their work however you consider most effective. They can
 brainstorm ideas, review the literature, develop results, independently verify findings, write code or



                                                     69
  perform other useful tasks. At any point, use as many or as few subagents as you think would be helpful,
  including none when appropriate (on this computer you can run up to 15 active agents in parallel at the
  same time). However, verification of results should include independent review by fresh subagents.
       As you progress, document useful information in Markdown files in the repository. Preserve interesting
  findings that are worth keeping, even if their impact is modest. Also retain negative results if they could
  inform future investigations. Use your judgment about what is useful, and ensure that this information
  is recorded in the repository.
       Once you obtain and thoroughly verify new, publishable results that are not already known, or
  for which you cannot find prior work in the openly accessible literature, document them and continue.
  Develop those ideas further or investigate new directions and possible discoveries. When you believe you
  have sufficiently explored the current ideas, generate new ones and pursue additional results. Continually
  aim for results that are more impactful and more practically important than those obtained so far.
       Do not stop unless I interrupt you or you reach usage limits. Obtaining a publishable result is a
  milestone, not a stopping point.
       Correctness is essential. Sound results can still be valuable even when their impact and practical
  usefulness are modest. Incorrect results or claims have a negative impact. Verify all results thoroughly,
  including through independent review by subagents, and correct any issues you discover in either new or
  existing results.
       You may install and use packages, libraries, solvers, and development tools needed for the research
  without asking for routine installation approval. For Python, prefer uv and isolated project environments,
  while respecting existing project conventions and skill-specific execution instructions. Record dependencies
  and versions needed to reproduce the work. A Gourbi and GAMS licenses are available on this computer;
  use it when useful and verify that it works in the execution environment. Coordinate concurrent
  experiments and solver threads with available CPU and memory.



B.3    A paper-writing prompt
This prompt asks the agents to turn a body of notes into a paper. “Topic 3” refers to a numbered
list of candidate topics that the agents had produced earlier in the same session. The five-reviewer
cycle is the only process we prescribed; the agents chose everything else, including what further
development the paper needed.


 Create a new folder in this repository and write a LaTeX paper on the topic 3. The paper should
 comprehensively cover all developments in the repository relevant to that topic.
      The final deliverable should be a complete, standalone paper ready for submission to a reputable
 journal. Clearly explain its relationship to prior work, the importance of the developments, and its
 original contributions.
 Support novelty claims with a careful literature review. Where justified, use qualified language such as
 “To the best of our knowledge,” and state precisely what is new. Do not claim novelty beyond what the
 evidence supports.
 Use the literature available in the local folder and search online as needed throughout the writing and
 revision process.
      Do more than transcribe the existing material into paper form. Throughout the writing process,
 critically examine and verify all results. If any ideas are incomplete or require further investigation,
 develop them further and resolve outstanding questions so that the paper presents fully developed work.
 SO if there is some development work that needs to be done (i.e. experiments, lean verification, theory
 etc.), do it in the process, such that the resulting state is a complete paper without significant further
 improvements possible in your opinion.
      If you find errors, correct them, or if you find a mistake that invalidates the results on the whole
 topic entirely, and no reasonable paper can be produced, document it, and stop writing the paper.



                                                      70
      Organize the work into stages. Choose the structure you consider most appropriate, whether by
  section, subsection, paragraph, or another meaningful unit such as additional experiments or lean
  verification. Complete each stage before proceeding to the next.
      Follow this process for each stage:
      1. Decide what to develop or write, and use a subagent to complete that work.
  2. Once the agent finishes, dispatch five subagents to independently review the changes.
  3. Evaluate their findings using your own judgment to determine which criticisms are valid and which
  issues are major.
  4. If any valid issues are identified, assign another subagent to fix all of them, including minor issues.
  5. If the review identified any issues you consider major, repeat the review with five subagents after the
  corrections are complete. Continue this review and revision cycle until a review finds no major issues.
  6. Address any remaining valid minor issues before proceeding to the next stage.
      Mathematical and scientific correctness are the highest priorities. Check carefully for incorrect proofs,
  unsupported claims, mathematical errors, and gaps in reasoning. Also ensure that the writing is clear,
  the explanations are sufficient, and the intended readership can follow the arguments.
      Once the full draft is complete, thoroughly review the entire manuscript using the same process: five
  independent reviewers, your assessment of their findings, and corrections by another agent. Assess both
  the individual sections and how they fit together, including the paper’s overall structure, consistency,
  completeness, and readability. Repeat the review after correcting any major issues in the same cycle and
  address all remaining valid minor issues before considering the paper complete.
      Aim to produce a publication-ready paper suitable for a high-quality journal. There is no need to
  adopt a specific journal template at this stage. In your judgment, the final manuscript should be free of
  unresolved issues that could reasonably be identified during peer review or publication.
      Consult the repository’s literature folder as needed. You may also search for additional literature
  outside the repository whenever useful.



B.4    A formal-verification prompt
We asked which results should be proved in the Lean proof assistant, and then told the agents to
do all of the ones they recommended. We did not choose the topics. All of the Lean proofs in the
corpus followed from this prompt and its continuations.


  what are other topics you would recommend proving with lean? do this for all topics that you recommended.
  DO it one by one (i.e. go to next one only after the previous one is finished) and organize them properly
  tos it is clear where each topic’s info is located. Use subagents to help you as you see fit .



C     Research inventory
The corpus is released at https://github.com/SECQUOIA/agent-swarm-research [6], with one
folder for each research area. It contains the agents’ notes, checks, code, review records, Lean proofs,
and drafts, in LaTeX source and as compiled PDFs.
    This paper describes the repository at commit 84c6be7 (tag paper-v1), and all links to its files
in this paper point to that commit. It holds the agents’ output as of 25 September 2026, before any
scientific input from us; its README records the version of each source repository it was copied
from. The repository will keep changing: the runs continue, and later commits may add topics,
results, and drafts, some of them with our own scientific input. Those later versions are not part of
the work reported here.



                                                       71
    Table 3 lists the potential papers in the corpus, whether or not they have been written, and the
proposed experimental programs. Each row in the five theoretical areas is a group of related results
that could stand as one paper; each row in catalysis is one proposed program. The contributions
are the agents’ claims as stated in their own write-ups and notes. We left out results that the
agents themselves marked as superseded, refuted, or withdrawn, results too small to stand as a
paper, and clusters whose main result the agents’ own literature checks found to be already known.
In heterogeneous catalysis, unlike the other areas, the agents produced proposed experimental
programs; none of the proposed laboratory experiments has been carried out.
    In the Write-up column, each entry “Full paper”, “Summary document”, and “Program document”
links to the PDF of the draft at that commit. The drafts are unedited, and our part in producing
them was limited to the orchestration and editorial input listed in Section 4.1. The Lean column
gives the status on 25 September 2026. Rows marked “Notes only” have no draft; their results are
in the agents’ notes in the same repository. CA5–CA8 also appear briefly as reserve ideas in the
catalysis program document.

                     Table 3: Potential papers and proposed experimental programs in
                     the corpus. Status values are defined below the table.

ID     Working title and claimed contribution                                  Write-up         Lean
Mixed-integer nonlinear programming
M1   Sharp gaps for positive multilinear relaxations. Disproves                Full paper       Done
     the Luedtke–Namazifar–Linderoth conjecture; exact hull gap;
     worst ratio grows as ln d/ ln ln d in degree and ln n/ ln ln n in
     dimension. Builds on [143].
M2   Verified bounds for positive cubic relaxation gaps.                       Full paper       Done
     Brackets the worst cubic termwise-to-hull gap ratio:
     1610000/743033 ≤ R(3) ≤ 31/12.
M3   Checkable lower bounds for convex mixed-integer                           Full paper       Done
     nonlinear optimization through rational outer
     approximations. Rational certificates give independently
     checkable lower bounds; 203 of 289 MINLPLib models pass
     separate replay; exact audits find invalid proofs accepted by an
     external proof checker. Builds on [142].
M4   Convex relaxation gaps and spatial certificates in                        Full paper       Partial
     nonlinear optimization. Signed bilinear gaps of the order of
     the square root of the edge density; exponentially many certified
     regions for spatial branch-and-bound under specified node oracles.
     Answers a question of Altschuler and Boix-Adserà negatively,
     assuming P ̸= NP; a counterexample to a published theorem on
     P-split formulations. Also restates the positive multilinear and
     cubic gap results of M1 and M2.
M5   Integer dimension in convex mixed-integer                                 Full paper       Partial
     approximation of nonlinear graphs. For a fixed quadratic
     system on a box, the minimum number of integer or binary
     variables for ε-accurate convex lifts is 12 ncrank · log2 (1/ε) + O(1),
     where ncrank is the noncommutative rank of the Hessian space;
     polynomial-time rational constructions. Builds on [255, 256].
                                                                                      Continued on next page




                                                       72
ID    Working title and claimed contribution                                 Write-up         Lean
M6    Rounding switching controls under a hard switch budget:                Full paper       Partial
      sharp minimax bounds and exact algorithms. Exact
      minimax rounding error for up to three switches; disproves a
      conjecture of Sager and Zeile and corrects a published lower
      bound; exact finite-grid values and algorithms.
M7    Sparse convex hulls for network flows coupled to a                     Full paper       Partial
      simplex. An exact formulation uses one extra coordinate per
      independent cycle of each unobserved block–label subgraph;
      exponential coefficient growth on series–parallel graphs.
M8    Topology, uncertainty, and precision in passive                        Full paper       Partial
      potential-flow optimization. Polynomial additive
      optimization of potential differences at fixed block cycle rank, for
      balanced nomination boxes and independent coefficient intervals;
      exact pressure comparison on single-source, single-sink cacti is
      equivalent to Square-Root Sum.
M9    The complexity of pooling: algebraic barriers and                      Full paper       Not
      structural algorithms. The pooling threshold decision is                                applicable
      ∃R-complete; strongly NP-complete with all layer degrees two,
      and NP-complete with two pools and two products, answering
      questions of Boland et al. and Haugland; resolves a rank-one cost
      conjecture; matching tractability boundaries. Builds
      on [144–146].
M10   Exact feasibility of resistive and AC power networks.                  Full paper       Not
      Resistive power-flow feasibility is ∃R-complete even on planar,                         applicable
      degree-three, unit-conductance networks; the hardness transfers
      to AC networks with resistive lines. Related work: [148, 149].
M11   Structured bilevel optimization with many follower                     Full paper       Possible
      variables: global responses, accuracy, and structural
      boundaries. A fixed-dimensional description of all global
      follower responses gives exact polynomial algorithms; rational
      leaders with error 2−B for strictly convex costs; hardness with
      dense near-identity Hessians.
M12   Globally certified measurement selection with correlated               Full paper       Partial
      errors. Polynomial approximation sets in relative PSD order, a
      weighted-trace approximation scheme, and rational
      log-determinant certificates for correlated measurement selection.
M13   Radial and point separation for perspective outer                      Full paper       Not
      approximation of convex generalized disjunctive                                         applicable
      programs. Matched comparison of two separation policies:
      radial search gives modest, implementation-specific gains; no new
      cut family.
M14   Quadratic aggregation: certificates, finite descriptions,              Full paper       Partial
      and approximation. Resolves three Blekherman–Dey–Sun
      conjectures: under hidden hyperplane convexity, a hull is proper
      exactly when a nonconstant convex aggregation exists; a
      three-inequality hull needs uncountably many aggregations; four
      aggregations suffice for three strict quadratics with a positive
      definite combination, extending a Blekherman–Dunbar bound,
      and are sharp. Builds on [147].
                                                                                    Continued on next page




                                                     73
ID    Working title and claimed contribution                                        Write-up         Lean
M15   Exact convex hulls for a reciprocal factor shared by                          Notes only       Done
      many variables. Explicit hull of (X, 1/X, Yi , XYi ) for many
      leaves, with exact rational separation and decomposition; extends
      to an integer factor with a binary-encoded range, with separation
      polynomial in the encoding length.
M16   Ill-posed heat-exchanger network instances in                                 Notes only       Not
      MINLPLib. The heatexch_gen models share an unbounded                                           applicable
      guarded log-mean-temperature term; for heatexch_gen1, a
      numerically feasible point improves the listed value by about
      30%, and numerical estimates indicate that the infimum is not
      attained.
M17   Convex envelopes of two-variable monomials with real                          Notes only       Possible
      exponents on a wedge. Extends the hull of a bounded
      monomial on a wedge from positive exponents to negative and
      mixed-sign ones, including ratio terms; answers Belotti’s open
      case of two negative exponents. Builds on [257].
M18   Exact indicator quadratic optimization at low treewidth.                      Notes only       Not
      NP-hard at bandwidth two with Hessians arbitrarily close to the                                applicable
      identity; with randomly perturbed indicator penalties, exact
      algorithms in polynomial expected bit time at fixed treewidth.
M19   Convex envelopes of univariate functions of a linear form.                    Notes only       Possible
      For any lower semicontinuous σ, the convex envelope of
      σ(a⊤ x + b) over a box is a minimum over laws below a
      comonotone staircase law in convex order, and dually a
      supremum over concave minorants, each of which gives cuts valid
      on the whole box; extensions to products of simplices and
      sign-restricted order polytopes. Builds on [258].
M20   Contraction theory of iterated optimality-based bound                         Notes only       Possible
      tightening. Near a minimizer, iterated bound tightening follows
      a monotone, positively homogeneous map on box shapes whose
      Collatz–Wielandt-type constant bounds the local linear rate; a
      certificate
       √          for when tightening stalls; the exact rate
      ( 2a2 + 4a − a)/2 of simultaneous rounds for x2 + y 2 + axy,
      0 < a < 2, with McCormick relaxations; a condition under which
      tightening does nothing, even for strongly convex objectives.
      Builds on [259].
M21   Joint relaxation of several nonlinear terms in one                            Notes only       Not
      variable. Automatic, certified treatment in a solver: certified                                applicable
      curvature and envelope cuts valid for every slope solve all 24
      separable quartic test programs, of which native SCIP, Gurobi,
      and BARON solve 2, 3, and 6; a certified separator for hulls of
      curves (t, f1 (t), . . . , fk (t)). The hull theory itself is known. Builds
      on [260].
M22   Separable concave terms on few linear rows. A binary                          Notes only       Possible
      reformulation that allows at most rank(A) variables strictly
      inside their concave pieces is solved in 2n + 1 branch-and-cut
      nodes on a family where spatial branch-and-bound needs
      exponentially many (M4); the joint hull of concave terms on one
      row, which for equal widths is the Padberg–Van Roy–Wolsey
      flow-cover polyhedron in other variables, extended to inequality
      rows and to indicators with concave costs. Builds on [261].
                                                                                           Continued on next page


                                                          74
ID     Working title and claimed contribution                              Write-up         Lean

Quantum interior-point methods
Q1   Objective sublevels and central-path Hessian                          Full paper       Partial
     conditioning. For every self-concordant barrier, conditioning is
     Θ((diam L(g)/g)2 ); LP spectra have two scales.
Q2   The cost of following√the central path. Sharp central-path            Full paper       Partial
     movement tax Γr = Θ( log r) for objectives of rank r; on an
     explicit sparse LP, primal–dual completion requires Θ(r3/2 )
     bounded steps. Builds on [140].
Q3   Access models and right-hand-side mass in Newton                      Summary          Partial
     solves. Degenerate-LP Hessians have two eigenvalue clusters           document
     that conjugate gradients handles in polylogarithmic iterations,
     while plain block access keeps the known Θ̃(κ) cost; the
     right-hand side’s coupling to the small eigenvalues decides when
     filtering helps.
Q4   Winner-take-all condensation in block log-determinant                 Summary          Possible
     SDPs. Winner  √ mass controls conditioning; tight holonomy value      document
     queries, Θ(N G) quantum versus Θ(N G) randomized.
Q5   Accuracy curves for hidden-block state conversion. Tight              Summary          Not
     accuracy-dependent query curves for quantum state conversion          document         applicable
     on proved domains; notes extend the lower bound to any inner
     predicate, an open problem of the summary document, and give
     the exact zero-query error in the range it leaves open.
Q6   Condition-one linear programs with hard loading and                   Summary          Not
     recovery. Sparse LPs with condition-one reduced Newton                document         applicable
     systems still need linearly many queries to load and recover
     states.
Q7   Limits of parity-gadget lower-bound constructions.                    Summary          Partial
     Algebraic identities rule out natural classes of parity-gadget        document
     lower-bound constructions; notes rule out bounded local full-KKT
     parity amplifiers, an open problem of the summary document.
Q8   Loading and recovery hardness for semidefinite                        Summary          Not
     programs. Trace-normalized SDPs with condition-one Newton             document         applicable
     steps still have parity-hard values and solution states; notes give
     genuinely nonabelian Θ(N ) word hardness with a sparse SDP
     transfer, an open problem of the summary document.
Q9   Trade-offs between preconditioning and state interfaces.              Summary          Partial
     A better preconditioned condition number is paid for in               document
     normalization, recovery sensitivity, or state preparation.
Q10 Conditional speedups for sparse quantum interior-point                 Summary          Partial
     methods. Conditional per-step gains from certified refresh, face      document
     repair, compressed dual output, and block-angular borders.
Q11 A correction to the complexity analysis of the quantum                 Summary          Done
     central path method. Both the simulator-norm bound and the            document
     clock analysis of arXiv:2311.03977v2 fail as claimed; corrected
     norm and speed trade-off. The authors informed us that they
     already knew of at least one error and are preparing a revision;
     no correction was public when the agents ran.
                                                                                  Continued on next page




                                                    75
ID     Working title and claimed contribution                                 Write-up         Lean
Q12    Curvature, support certificates, and barrier complexity                Full paper       Possible
       of conic lifts. An exact lift by definable cones of a body with a
       strictly
       P        curved boundary patch needs
          i max(dim  Ki − 2, 0) ≥ s − 1; the least support-certificate rank
       of an s-dimensional ball is exactly ⌈(s − 1)/B⌉; exact barrier
       parameters for symmetric-cone balance slices. Also: disk-product
       instances whose central states need O(1) queries but whose scalar
       readout needs Θ(N ); with matched oracles at the fiber center,
       PSD packing gives no query advantage for reduced Newton
       solves; compilation of sparse second-order√cone constraints to
       barrier parameter at most k + 1 with Θ( N k) quantum versus
       Θ(N ) randomized queries.
Q13    Classical and quantum query complexity of scalar                       Full paper       Not
       Newton quantities.
                      √         Relative estimation of b∗ H −1 b with                          applicable
          −2        O( κ log(2/ε))
       κε (d + 1)                  classical queries and a lower bound
       matching the known Õ(ακ/ε) block-access algorithm up to
       logarithmic factors on 3 × 3 matrices; statistical-query sampling
       of Newton steps; one-cone sparse SOCP: O(1) quantum queries
       versus Ω̃(N 1−1/k ) classical statistical queries.
Q14    The quantum cost of unit-normalized spectral shifting.                 Full paper       Not
       Answers an open problem of the summary document: a sharp                                applicable
       query staircase Θ(δ −1+1/(2ℓ) ) for block encodings of I − H with
       normalization one, and Θ(δ −1 log(1/K)) at high accuracy; a
       sparse LP separates normal-matrix from factor access.
Q15    Exponential-cone scenario compression for entropic risk.               Notes only       Not
       Compresses N scenarios into O(1 + K + log) exponential cones,                           applicable
       independent of N , with certified value bounds; matched Θ(eK /ε)
       quantum versus Θ(e2K /ε2 ) classical source queries under the
       stated access model.
Molecular thermodynamics
TD1 Finite reservoirs at phase coexistence: full-state                        Full paper       Not
     accuracy and phase correlations. When finite baths                                        applicable
     reproduce canonical laws; an N 3/2 threshold for the two-phase
     systems studied under stated phase-tail conditions; a shared bath
     of intermediate size drives two copies into opposite phases while
     each copy alone stays canonical. Builds on [141].
TD2 Survival-conditioned thermodynamic integration.                           Notes only       Possible
     Endpoint-survivor force integration is path-dependent, with error
     of second order in weak killing; interior survivors admit an exact
     potential.
TD3 Interfacial tension from bulk response in nonlocal                        Notes only       Not
     double-parabola models. Exact tension certificates from bulk                              applicable
     response; fourth-order moment matching leaves the tension
     undetermined.
TD4 Capacity certificates for reversible nucleation kinetics.                 Notes only       Not
     Capacity lower bounds from conditional transport; paired                                  applicable
     finite-field bounds on nucleation-rate response.
                                                                                     Continued on next page




                                                      76
ID     Working title and claimed contribution                             Write-up         Lean

Transport theory
TP1 Designing surface transport under uncertain kinetics:                 Full paper       Not
      moment thresholds and measurement precision. For a                                   applicable
      small surface-mobility budget M , the best fixed placement raises
      the disorder-moment order at which rare merging defects
      dominate from 4/3 to 8/5; observing the defects improves the
      mean from M −1/4 to M −1/5 , and resolution of order M 1/5
      suffices. Builds on [262].
TP2 Kinetic defects in adsorbing channels. Weak surface                   Notes only       Not
                                                              −1/4
      diffusion Ds at a quadratic kinetic minimum gives a Ds                               applicable
      dispersion divergence with an explicit crossover to a rate floor;
      when the minimum’s location is known, optimal placement of a
      mobility budget M improves the divergence from M −1/4 to
      M −1/5 , the known-defect case behind TP1; an exactly solvable
      placement transition.
Aggregation kinetics
AK1 Sampling-law separation and finite nonlinear corrections              Full paper       Not
     in additive coagulation–fragmentation. Sharp number–mass                              applicable
     separation bounds, a finite log-size correction, finite-population
     breakdown, Fourier identification. Builds on [263].
AK2 Survival under unobserved sister-type dependence in                   Notes only       Possible
     multitype branching. Uniform near-critical error bounds for
     extinction over unobserved daughter couplings, with an exact
     optimal coupling and a rule for tied reproductive values; the
     basic sharp envelopes follow from known branching and
     rearrangement results.
Heterogeneous catalysis: proposed experimental programs
CA1 Physical water management in Fischer–Tropsch synthesis.               Program          Not
      Tests whether late hydrophobic-polymer addition protects            document         applicable
      conditioned cobalt; re-analysis of published data finds a product
      output about 1.9 times that of the reference with the polymer.
CA2 Steam compatibility of cyclic oxides in chemical looping.             Program          Not
      Tests whether steam purges, assumed by a published process          document         applicable
      model but not tested, change ethylene output from coated LSF;
      compares CO2 supplied with the steam (protection) and
      afterwards (recovery).
CA3 Catalyst demand in polymer ethenolysis. Tests whether                 Program          Not
      lower ethylene pressure can replace part of the fresh Na/alumina    document         applicable
      catalyst when reused catalyst converts polyethylene to propylene.
CA4 Nickel and the useful life of promoted silver epoxidation             Program          Not
      catalysts. Tests whether nickel adds ethylene oxide output          document         applicable
      beyond chloride policies; a 1995 patent already reports a
      retention benefit.
CA5 Tungsten coordination and retention in sugar conversion.              Notes only       Not
      Tests whether a controllable anchoring or feed variable links                        applicable
      productive sugar coordination, tungsten loss, and glycol output.
CA6 Product-rich liquid Ti-zeolite epoxidation. Tests whether a           Notes only       Not
      reaction network calibrated on dilute kinetics predicts epoxide                      applicable
      output and peroxide loss once products accumulate.
                                                                                 Continued on next page


                                                   77
ID    Working title and claimed contribution                         Write-up        Lean
CA7   Oxygen fate and self-cleaning in zirconia-catalyzed            Notes only      Not
      styrene production. Tests whether an oxygen-removal pathway                    applicable
      predicts sustained styrene output and a feed policy.
CA8   Acid-site assays and zeolite aging. Tests whether repeated     Notes only      Not
      NH3 and water assays change the hydrothermal aging of H-CHA.                   applicable


Status values:
• Write-up. Full paper: a complete, compiled manuscript. Summary document: part of the
   long document that collects the quantum interior-point results, which we asked for instead of
   separate papers. Program document: a chapter of the document that ranks the proposed catalysis
   programs. Notes only: the results exist only as the agents’ notes and checks.
• Lean. Done: the main mathematical results are proved in Lean, with no unproved steps; software
   and experiments are not covered. Partial: some of the results are proved in Lean, but not all.
  Possible: not done, but the main claims are mathematical statements that could be formalized
  with current libraries; this is a judgement, not a check. Not applicable: the main claims rest on
   numerical evidence, experiments, or modelling assumptions, or require a framework that current
   formal libraries do not provide, such as complexity classes, quantum query models, or limit
   theorems for stochastic processes.




                                                78
