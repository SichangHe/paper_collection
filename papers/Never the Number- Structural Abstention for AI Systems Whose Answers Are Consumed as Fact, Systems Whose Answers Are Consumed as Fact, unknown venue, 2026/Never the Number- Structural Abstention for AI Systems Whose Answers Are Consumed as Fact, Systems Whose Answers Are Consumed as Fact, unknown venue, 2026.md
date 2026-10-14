                                               Never the Number: Structural Abstention for AI
                                               Systems Whose Answers Are Consumed as Fact


                                                                                          Zhelun (Allen) Wu∗



                                                                                                Abstract
                                                     Large language models have made natural language interfaces to databases newly
                                                     credible, but LLM text-to-SQL systems fail in a way that matters for deployment:
                                                     a hallucinated column or a mis-aggregated total yields a fluent wrong answer that
                                                     is indistinguishable, at the point of use, from a right one. Where the consumer
arXiv:2608.13926v1 [cs.AI] 14 Aug 2026




                                                     cannot inspect the generated query, as in enterprise AI deployments and operational
                                                     dashboards, and increasingly where the consumer is a tool-using agent rather than
                                                     a person, accuracy alone is insufficient: nothing marks which answers to distrust.
                                                     This is a reliability problem before it is an accuracy problem.
                                                     We propose an architectural pattern for such systems, a trusted kernel with a
                                                     generative shell, resting on one invariant: a component that can fabricate may
                                                     influence which question the system answers, never which value it returns. A
                                                     generative shell interprets underspecified input and phrases replies; a deterministic
                                                     kernel matches fully specified questions against a bounded set of answerable
                                                     question shapes and compiles them to queries by deterministic execution. The two
                                                     meet at a confirmation the user reads before any value is computed, and requests
                                                     the kernel cannot express are declined rather than approximated. We call this
                                                     structural abstention and distinguish it from the statistical abstention of selective
                                                     prediction and calibrated confidence: refusal here needs no confidence estimate,
                                                     because unanswerable requests are unrepresentable.
                                                     We specify the pattern implementation-independently, give a five-decision recipe
                                                     and work it across three domains, extend the invariant from returned values to the
                                                     actions of agentic systems, and report a two-year production case study alongside
                                                     two generative alternatives, a fine-tuned parser and a tool-retrieval agent. We close
                                                     against enterprise and reliability benchmarks published since, which now measure
                                                     precisely the failure the pattern was built to avoid.
                                         Keywords: trustworthy AI; LLM reliability; hallucination; abstention and selective prediction;
                                         deterministic execution; agentic AI; AI agents and tool use; agent safety; retrieval-augmented
                                         generation (RAG); text-to-SQL; natural language interface to databases (NLIDB); semantic layer;
                                         enterprise AI and conversational analytics; automated data analysis; self-serve analytics; dialogue
                                         state tracking; human-in-the-loop confirmation.


                                         1    Introduction
                                         A regional sales manager wants to know which store in her city sold the most of a particular product
                                         last week. The warehouse holds the answer exactly. She cannot get at it, because getting at it means
                                         knowing which of several tables holds store-level weekly figures, how the company’s fiscal calendar
                                         lines up with ordinary dates, and which of a dozen overlapping store classifications her question
                                         implies. So she writes to an analyst, who is working through a queue, and two days later she gets a
                                         figure by which time the question has answered itself or stopped mattering.
                                            ∗ The case study draws on a system the author led while at Apple Inc. (2021–2024). This report describes architecture and

                                         design principles only; see the disclosure note in Section 1. Correspondence: allenwu94@icloud.com.


                                         Preprint.
           The usual arrangement


            user        language           query             value        answer
                          model

              anything the model gets wrong here arrives as a value the user cannot question




           This paper                                                 no generative component



            user        language           confirmed                           query                   answer
                          model             question             kernel                        value

                                       the user reads this                                             phrasing
                                          and assents                                                    only


Figure 1: The core idea. Shaded boxes may fabricate; unshaded boxes may not. In the usual
arrangement a language model produces the query, so any mistake it makes arrives as a value
indistinguishable from a correct one. Here the model works only before the confirmation and,
afterwards, only on wording: the path from confirmed question to value contains nothing that can
invent. The cost is that questions the kernel cannot express are declined rather than approximated.


She is not specific to retail. She recurs wherever something needs a value from a system it cannot
query and will act on whatever it is told: a clinician asking how many beds were free on a ward
overnight, a planner asking which components fell below reorder threshold, a controller asking what
a cost centre spent last quarter, and increasingly a downstream agent acting on a figure no human
reviewed at all. What these share is not subject matter. It is that the answer arrives as an assertion
rather than as a working, and whoever or whatever receives it has no practical means of auditing it.
We call these fact-consumed systems, and note that the consumer need not be a person: a tool-using
agent that reads a value and then acts on it is in exactly the position of the manager who cannot read
SQL, with less recourse. The problem is therefore one of LLM reliability and, in the agentic case, of
agent safety, rather than of model capability.
This class now has a commercial form. Automated data analysis products, variously marketed as
AI analysts or self-serve analytics agents, are fact-consumed systems by construction: they exist
precisely so that someone who cannot write the query does not have to. The pattern in this report
is not a proposal for building such a product. It is a proposal for the layer such a product needs
underneath it if the figures it returns are to be trusted, and Section 13 is explicit that the analyst’s
actual work — exploration, hypothesis, judgment on novel questions — is outside what the pattern
can do and should be.
Putting a language model between such a user and the database is the obvious move, and the difficulty
is not that it fails but how it fails. A model that paraphrases a schema fluently will sometimes
reference a column that does not exist or aggregate along the wrong axis [Ji et al., 2023], and one
that handles compositional language will sometimes get the arithmetic wrong [Cobbe et al., 2021,
Hendrycks et al., 2021]. Where the analyst reads the query before trusting it, this is tolerable. Where
the query is invisible and the sentence containing the number is the product, the wrong answers
have the same format, the same confident phrasing, and a plausible magnitude, and the calibration
literature offers limited hope of separating them after the fact [Kadavath et al., 2022]. A system that
is right 85% of the time and cannot indicate which 85% has not removed the analyst from the loop; it
has removed the analyst and kept the uncertainty.

What is new here. Two things, and both are conceptual rather than technical. The first is an
architectural invariant, which we state now because the rest of the paper follows from it.

  The perimeter invariant. A component that can fabricate may influence which question the
  system answers. It may never influence which value the system returns.



                                                                2
                   SHELL                                                        KERNEL

                                          state
               I NTERPRETER                                                    G ROUNDER


                                                  confirm-
                  E LICITOR                         ation                       C OMPILER



                 R ENDERER                                                     query engine
                                                                  result




         May fabricate. A mistake here                                May not fabricate. A mistake here
        costs a turn, and the user sees it.                           would be invisible, so the possibil-
                                                                     ity is removed rather than managed.


Figure 2: The perimeter invariant as a structure. A model may operate anywhere in the shell, where
its errors are recoverable and visible. Nothing in the kernel is generative, because a wrong value there
would reach the user unmarked. The two regions communicate only across the confirmation, which
the user reads and assents to before any value is computed.


A model may shape the question and may phrase the reply. Never the number. Figure 1 contrasts
the resulting arrangement with the usual one, and Figure 2 gives its structure. Call the region where
the invariant does not bind the shell and the region where it binds absolutely the kernel. The shell
interprets underspecified input, decides what to ask next, and phrases replies; its errors cost a turn
and the user sees them. The kernel matches a fully specified question against the set of questions the
system can answer and turns that question into a query; its errors would be invisible, so the pattern
removes the possibility rather than managing the risk. The two meet at a confirmation: the system
states in ordinary language the question it is about to answer, and the user assents. Everything before
that sentence is negotiable; everything after it is mechanical.
The second contribution is a name for the family this design belongs to. Structural abstention
makes unanswerable requests unrepresentable, so that refusing requires no confidence estimate at
all; statistical abstention, which is what the reliability literature has mostly developed, generates
a candidate answer and then estimates whether to trust it [Lee et al., 2024, Somov and Tutubalina,
2025, Chen et al., 2025]. The distinction is developed in Section 3.6. We think it is the more useful of
our two contributions, because it names a design axis that exists independently of anything we built.

Why this is not one company’s engineering problem. The invariant says nothing about SQL,
and nothing about databases. It says that whatever produces a consequential value must do so by
deterministic execution over a specification someone authored, and that a model may stand in front
of that machinery but never inside it. Section 4 reduces the pattern to five decisions and works them
for clinical ward reporting and financial reporting alongside our own enterprise analytics setting,
and Section 4.3 extends the invariant from returned values to executed actions, where it reads: a
component that can fabricate may influence which action is proposed, never which action is executed.
That version is the one that matters for tool-using agents, and the failure it prevents is worse there
than here, since a wrong figure can be contradicted later and an executed action has already happened.
What the pattern costs is coverage, and Section 3.5 states the three conditions under which that price
is worth paying — along with the case where it is not.

Structure. Section 2 places the work; Section 3 specifies the pattern independently of any imple-
mentation; Section 4 gives the instantiation recipe and transfers it; Sections 5–9 report a two-year
production deployment built on the pattern, together with two generative alternatives, one abandoned
and one that succeeded it and why; Section 12 reassesses the design against work published since;
and Section 13 states what the report does not establish.


                                                     3
Scope and disclosure. The case study draws on a production system the author led in industry
between 2021 and 2024. This report is limited to architecture and design principles, and excludes
by construction: source code; schemas, table or column names, or any description of a real data
model; datasets; quantitative performance, accuracy, latency, or adoption metrics; information about
customers, users, or personnel; and internal business processes, product plans, or organizational
detail. Figures in examples are invented, and the schema in Appendix C is synthetic. Deployment is
described in the past tense, since the author’s direct knowledge ends in 2024.

2     Related Work
2.1   Natural language interfaces to databases

The problem G ROUNDER addresses is old, and so is the observation that constraining coverage buys
reliability. Androutsopoulos et al. [1995] survey the pre-neural tradition and identify the tension
we still face: systems with broad linguistic coverage are hard to make correct, and systems that
are correct are usually narrow. Popescu et al. [2003] make the sharpest version of the argument by
defining a class of semantically tractable questions — those a system can answer with a correctness
guarantee — and having the system refuse everything else. That is structurally the choice G ROUNDER
makes, with a template pool playing the role of the tractability criterion.
Later systems added interaction. NaLIR [Li and Jagadish, 2014] presents the user with its interpre-
tation of a query and lets them correct it before execution, which is the same insight behind our
confirmation turn: showing the user the question you are about to answer is cheaper than explaining a
wrong answer afterwards. ATHENA [Saha et al., 2016] maps language onto an ontology rather than
directly onto physical tables, decoupling the user’s vocabulary from schema layout — a separation
we implement more crudely, through the template-to-table mapping described in Section 5.5. Our
contribution relative to this line is not the constrained-coverage idea, which is theirs, but its combi-
nation with an LLM used strictly outside the correctness-critical path, and an account of what that
combination looks like in production.

2.2   Neural and LLM text-to-SQL

The modern line begins with supervised semantic parsing over single tables [Zhong et al., 2017]
and the cross-domain benchmarks that followed [Yu et al., 2018, Li et al., 2023]. Architectural
work improved schema linking [Wang et al., 2020], and decoding-time constraints improved well-
formedness: PICARD [Scholak et al., 2021] rejects partial outputs that cannot extend to valid SQL,
and LLM-era methods decompose the task into subproblems with self-correction [Pourreza and
Rafiei, 2023].
Three things about this literature bear on our design.
First, constrained decoding and our parse-tree compiler attack the same problem from opposite ends.
PICARD guarantees syntactic and schema validity of generated SQL; it cannot guarantee the query
answers the question the user asked. We give up the ability to generate arbitrary queries in exchange
for a guarantee about semantics: within the pool, the mapping from confirmed question to SQL is
fixed and auditable.
Second, benchmark accuracy on Spider or BIRD is execution accuracy averaged over a query
distribution — the right metric for a general-purpose parser and the wrong one for us. A system at
85% execution accuracy is excellent research and unusable as an unsupervised oracle, because the
15% is not labeled. What we needed was not higher average accuracy but a partition of inputs into
answered-correctly and visibly-declined.
Third, and only visible in hindsight: the benchmarks that made LLM text-to-SQL look close to
solved were not measuring our setting. Two later benchmarks built on enterprise warehouses report a
collapse. On Spider 2.0, whose databases come from real industrial applications and often exceed a
thousand columns, a code-agent framework over a frontier reasoning model solved 21.3% of tasks
against 91.2% on the original Spider [Lei et al., 2025]. On BEAVER, drawn from private warehouse
query logs, off-the-shelf models scored approximately zero end-to-end, and supplying the gold tables
and gold column mappings as hints lifted the best model only into low single digits [Chen et al.,
2024]. The stated causes — schema complexity, business questions requiring multi-table joins and


                                                   4
nested aggregation, and the fact that private schemas are absent from pretraining data — are precisely
the properties of the warehouse described in Section 5.1. Section 12 returns to what this means for
the design.

2.3   Conversational semantic parsing and dialogue state

SParC [Yu et al., 2019b] and CoSQL [Yu et al., 2019a] extend text-to-SQL to multi-turn interaction,
and CoSQL in particular includes the system-initiated clarification behavior our guidance mode
implements. The difference is directional: those systems learn when to clarify from data, whereas
ours clarifies when grounding fails, which is a decidable condition. We pay for this with rigidity and
are compensated with a guarantee.
Our dialogue state representation is closer to the task-oriented dialogue tradition than to semantic
parsing. The entity vector is a slot-filling belief state in the lineage of frame-driven dialogue [Bobrow
et al., 1977] and statistical dialogue state tracking [Henderson et al., 2014, Mrkšić et al., 2017, Wu
et al., 2019, Budzianowski et al., 2018]; the decision-theoretic framing of dialogue as action selection
over such a state is reviewed by Young et al. [2013]. Two departures matter. We use a pushdown
automaton rather than a flat state machine, because users suspend a question to ask a sub-question
and then resume — the stack discipline for discourse segments described by Grosz and Sidner [1986].
And our state set is finite by construction and tied one-to-one to answerable question shapes, so unlike
a learned belief state it cannot represent a configuration for which no action is defined.

2.4   Retrieval-augmented generation, tool use, and agentic pipelines

Our second prototype (Section 9) follows what is now called agentic AI: the retrieval-augmented
generation (RAG) [Lewis et al., 2020] and tool-use [Schick et al., 2023, Yao et al., 2023] paradigm,
in which the model calls entity-resolution utilities, then composes a query from their returns. Related
in spirit is the observation that offloading computation to an executor rather than performing it in
the model improves arithmetic reliability [Gao et al., 2023]; interleaved reasoning and acting traces
[Yao et al., 2023, Wei et al., 2022] also make the model’s path legible, which was the property we
most valued in that prototype. Our reasons for not making it the primary path were latency and
non-determinism rather than accuracy, and we regard it as the most promising route to extending
coverage (Section 14).

2.5   Reliability, abstention, and knowing when not to answer

The concern that motivated this system — a wrong answer indistinguishable from a right one — has
since become an explicit research topic, and the framing in that literature is close enough to ours
to be worth stating in its terms. TrustSQL [Lee et al., 2024] identifies two obstacles to deploying
text-to-SQL: users cannot tell which questions the system can correctly answer, and without an
abstention mechanism incorrect SQL goes unnoticed. It scores systems with a reliability metric
that weighs correct answers against wrong ones under a user-chosen penalty, which is the formal
version of the tradeoff Section 9.3 argues informally. A line of work on selective prediction for
SQL generation then attacks the same problem from the model side, using calibration, entropy, and
conformal methods to decide when to abstain [Somov and Tutubalina, 2025, Chen et al., 2025].
Our design sits at the structural end of this spectrum. Rather than generating a query and then
estimating whether to trust it, we decline at grounding time, before any query exists. This trades
coverage for a decision that requires no confidence estimate to be well calibrated. It is a cruder
instrument, and it was available in 2021.

2.6   Interaction design

The guidance mechanism is an instance of mixed-initiative interaction [Horvitz, 1999]: the system
acts when confident and defers to the user when uncertain, with the cost of an unnecessary clarification
traded against the cost of a wrong action. Several of the human–AI interaction guidelines catalogued
by Amershi et al. [2019] — making clear what the system can do, scoping services to capabilities,
supporting efficient correction — describe our three guidance modes almost directly, and our question
suggestion mode exists precisely to make the capability boundary legible rather than letting users
discover it through wrong answers.


                                                   5
Table 1: The four roles. The obligation column is the specification; the right-hand column states
which side of the perimeter invariant each role sits on.

 Role              Input → output               Obligation                               Region
 I NTERPRETER      utterance, state → updated   Extract whatever is determinate; leave   Shell (may be
                   state                        the rest unfilled. Must not invent       generative)
                                                values to fill gaps.
 E LICITOR         state → utterance            Choose what to ask next and phrase it.   Shell (may be
                                                May be wrong; wrongness costs a turn.    generative)
 G ROUNDER         state → question, or an      Decide whether the state denotes an      Kernel (must not
                   explicit failure             answerable question. Must be total       be generative)
                                                and decidable: return a question or a
                                                failure, never an approximation.
 C OMPILER         question → query             Map a grounded question to a query.      Kernel (must not
                                                Must be a function: same question,       be generative)
                                                same query, always.


2.7     Components

We use an attention mechanism [Vaswani et al., 2017] to score entity relevance over dialogue context
and user profile (Section 6); a DSSM-style dual encoder [Huang et al., 2013] for homepage question
recommendation of answerable questions; an inference-acceleration runtime of the kind described by
Rasley et al. [2020]; a compact open translation model in the manner of Tiedemann and Thottingal
[2020]; and a neural named-entity recognizer [Lample et al., 2016, Zhang and Yang, 2018] for proper
nouns in the users’ second language.

3     The Pattern
This section states the pattern without reference to any implementation. Sections 5–8 then describe
one way to build it. A reader who wants the comparison against end-to-end text-to-SQL and tool-using
agents before the details will find it in Table 4.

3.1     Component roles and obligations

The pattern assigns four roles. They need not be four separate processes, and may be co-located. What
matters is that each carries its obligation, and that the last two discharge theirs without generative
components.
Two obligations carry the pattern’s guarantees and deserve emphasis.
G ROUNDER must be total: for every state it either yields a question or reports that it cannot. Refusal
thereby becomes a first-class outcome instead of an error path. A generative component cannot
discharge this obligation, and the reason is not inaccuracy: it has no way to signal failure that a caller
can distinguish from an answer.
C OMPILER must be a function in the mathematical sense. Determinism is what makes the system
auditable. The query behind any answer can be reconstructed from the confirmed question alone,
with no need for logs of what a model happened to produce that day.

3.2     Representing partial specification

The pattern needs a state that can represent incompleteness explicitly, and this is the requirement that
rules out passing raw text between turns. Any representation works if it supports three operations:
1. Completeness test. Given a state, decide whether it denotes an answerable question. This is what
   G ROUNDER needs.
2. Gap enumeration. Given an incomplete state, enumerate what is missing. This is what E LICITOR
   needs to ask a useful question.


                                                    6
Algorithm 1 The bounded-answer dialogue loop. The three branches are exhaustive because
G ROUNDER is total: a state either grounds, or is incomplete, or is inconsistent.
 1: σ ← I NITIAL S TATE(profile)
 2: loop
 3:    u ← user utterance
 4:    σ ← I NTERPRETER(u, σ)                                        ▷ shell; extracts only what is determinate
 5:    if I NCONSISTENT(σ) then
 6:         emit E LICITOR(σ) naming the conflict; await resolution                                 ▷ correction
 7:    else if q ← G ROUNDER(σ) succeeds then
 8:         emit confirmation of q; await assent                                                ▷ the perimeter
 9:         if assented then
10:              r ← E XECUTE(C OMPILER(q))                                              ▷ kernel; deterministic
11:              emit R ENDER(q, r)                                 ▷ shell; phrasing only, over a known result
12:         end if
13:    else if P ROGRESSING(σ) then
14:         emit E LICITOR(σ) asking for a missing element                                          ▷ elicitation
15:    else
16:         emit nearest answerable questions                            ▷ disclosure: state what can be asked
17:    end if
18: end loop



3. Consistency test. Given a state, decide whether it over-specifies: whether the user has asked
   for something the system cannot coherently express. This third operation is easy to omit, and
   Section 6.4 shows why much of the value lies there.

Section 5.4 gives one concrete representation. The pattern is indifferent to the choice.

3.3   The dialogue policy

The invariant, plus a totality obligation on G ROUNDER, forces a three-branch policy. There is nothing
to design here; it falls out.
The final branch is the one most systems omit and the one that does the most work. When elicitation
stops converging, the user is asking for something outside the system’s range. The pattern then
requires the system to say what it can answer, instead of continuing to interrogate or falling back on a
guess. This turns the capability boundary from something users discover through wrong answers into
something the interface tells them, which is the property Amershi et al. [2019] identify as making
clear what a system can do, and which Lee et al. [2024] later identify as one of two obstacles to
deploying this class of system at all.

3.4   What the pattern guarantees

The guarantees are modest, and stating them precisely is the point.

1. No fabricated values. No returned figure was produced by a generative component. Computation
   is delegated to the query engine.
2. Auditability without logging. Any answer’s query is recoverable from its confirmed question,
   because C OMPILER is a function.
3. Failure is visible. The residual failure mode is refusal of an answerable-in-principle question.
   That is an error of coverage, which the user sees, and not an error of fact, which the user does not.
4. Semantic confirmation. The user has read the question their value answers, in language they can
   evaluate, before receiving it.

What the pattern does not guarantee: that the confirmed question was the one the user wanted (they
may assent carelessly); that the mapping from question to query is semantically correct, since a
mis-authored template is a silent bug. Correctness there is asserted at authoring time by whoever
knew the data model; the pattern relocates trust to that moment instead of eliminating the need for it.
Nor does it guarantee or anything at all about coverage.


                                                       7
3.5   Preconditions, and when not to use this

The pattern trades coverage for failure visibility. Three conditions determine whether that trade is
favorable.
1. Output is consumed as fact. The user cannot or will not inspect the generated query. If they can,
as with an analyst running a copilot in a notebook, a generative system is strictly better: the human is
the verifier that the pattern otherwise has to replace with structure.
2. Question demand is structurally repetitive. Questions recur in a small number of shapes with
varying parameters. If every question is novel, a bounded set of shapes cannot cover enough to be
useful, and the pattern degrades into an elaborate way of saying no.
3. Errors are costly relative to refusals. A wrong figure propagates into a decision; a refusal costs a
delay. In brainstorming, exploration, and low-stakes summarization, refusal costs more than error
and the trade inverts. Lee et al. [2024] give a way to make this exchange rate explicit as a penalty
weight, which is the natural way to decide the question quantitatively.
If all three hold, the pattern is appropriate and its coverage cost is worth paying. If the first fails,
do not use it. If only the second fails, a hybrid is indicated (Section 14): kernel for what grounds,
generative fallback for what does not, routed on grounding success rather than on a confidence score.

3.6   LLM reliability: structural versus statistical abstention

Two families of technique prevent a system from answering wrongly, and they are worth naming,
because this report belongs squarely to the second while the literature has mostly developed the first.
Statistical abstention generates a candidate answer and then estimates whether to trust it, using
calibration, sampling agreement, entropy, or conformal bounds [Somov and Tutubalina, 2025, Chen
et al., 2025]. Structural abstention makes unanswerable requests unrepresentable, so that refusal
requires no estimate at all: the system declines because it has nothing to say, not because a score fell
below a threshold.
The pattern is a coarse member of the structural family: the price of needing no calibrated confidence
is that coverage is fixed by however many question shapes someone has authored. The two families
compose, and we regard the composition as the most promising direction (Section 14): structural
refusal for what cannot be expressed, statistical abstention over a generative fallback for what can be
expressed but not grounded.


4     Instantiating the Pattern

Section 3 specifies roles and obligations but not how to fill them. This section gives the five decisions
an implementation must make, works them across three unrelated domains, and then generalizes the
invariant beyond returned values. The point of the exercise is to separate what the pattern requires
from what our particular deployment happened to choose; a reader in another domain should be able
to answer the five questions for themselves and stop reading.

4.1   The five decisions
1. What is the unit of answerability? The kernel needs an enumerable set of things it can answer.
   Ours was a pool of question templates with typed slots. Alternatives include a set of parameterized
   reports, a published metric definitions, or a bounded grammar over a semantic model. The
   requirement is only that membership be decidable and the set be authored by someone who knows
   the data.
2. What represents a partial request? Something that can express incompleteness and support the
   three operations of Section 3: completeness, gap enumeration, and consistency. A slot frame is
   the obvious choice, and the one we made.
3. What makes the request-to-answer mapping trustworthy? The C OMPILER must be a function,
   but what it compiles to is free: SQL text, a call to a governed metrics API, a stored procedure, a
   parameterized report invocation. The more constrained the target, the less there is to get wrong.


                                                   8
4. Where is the confirmation, and what does it show? The user must be shown the request in
   terms they can evaluate. This is a domain question, not a technical one: the right rendering is
   whatever vocabulary the user would have used to ask a colleague.
5. What happens on refusal? The weakest link in most implementations. The pattern requires that
   the system disclose what it can do; the design choice is whether that is a list of nearest answerable
   requests, a handoff to a human, or a fallback to a generative path with the difference made visible.


4.2   The recipe worked in three domains

Table 2 answers these questions for our deployment and for two domains we have not built in. The
second and third columns are constructions, not reports of systems that exist; we include them because
a pattern that cannot be specialized on paper is unlikely to be specializable in practice, and because
the exercise exposes which decisions are genuinely domain-dependent.
Three observations from the exercise.

Table 2: The five decisions, answered for three domains. Rows 1–5 are the decisions of Section 4;
the final rows record what changes. Only two of the five decisions turn out to be strongly domain-
dependent, which is the substance of the transferability claim.

Decision             Retail channel analytics     Ward operations reporting     Cost-centre financial
                     (this report)                                              reporting
1. Unit of           Question templates with      Templates over a governed     Published metric
answerability        typed slots                  clinical metric set           definitions in a finance
                                                                                semantic layer
2. Partial request   Entity vector plus value     Slot frame: ward, measure,    Slot frame: entity, account,
                     dictionary                   shift window                  period, basis
3. Compilation       SQL over warehouse           Calls to a governed metrics   Parameterized report
target               relations                    service                       invocation
4. Confirmation      Restated question in sales   Restated in clinical          Restated with the
surface              vocabulary                   vocabulary, with the shift    accounting basis and
                                                  boundary made explicit        period made explicit
5. On refusal        Nearest answerable           Handoff to an on-call         Pointer to the report that
                     questions                    analyst                       does cover it
Why the              A wrong figure enters a      A wrong figure enters a       A wrong figure may enter a
invariant matters    commercial decision          staffing or safety decision   filing
here
Hardest decision     1 (authoring cost)           4 (clinical vocabulary is     3 (the basis, not the
                                                  contested)                    number, is the ambiguity)


Decisions 2 and 5 barely move. A slot frame works everywhere, and the refusal branch differs only
in where it points. These are the parts of the pattern that can be implemented once and reused.
Decision 4 is where domain expertise is unavoidable. What counts as a legible restatement is
a question about the user’s professional vocabulary, and getting it wrong voids the pattern’s main
guarantee without producing any visible symptom: users assent to confirmations they have not really
understood. In the financial column the ambiguity is not which number but on what basis it was
computed, so a confirmation that omits the basis is worse than no confirmation, since it manufactures
false assurance.
Decision 3 gets easier as the target gets narrower. We compiled to SQL because that was what we
had. A deployment with a governed metrics service or a semantic layer available should compile to
that instead: the narrower the target language, the smaller the space of ways a mis-authored mapping
can be wrong. This is the one place where the intervening years have straightforwardly improved on
our implementation.


                                                    9
4.3    From values to actions: agentic AI and tool-using systems

The invariant is stated over returned values because that is what our system returned. It generalizes
without modification to systems that act:

    A component that can fabricate may influence which action is proposed. It may never influence
    which action is executed.

The kernel’s job becomes mapping a confirmed intent to a parameterized effect rather than to a query,
and the confirmation surface becomes the more familiar are-you-sure. Everything else carries over:
the totality obligation on G ROUNDER becomes the requirement that unsupported requests be refused
rather than improvised into some adjacent action, and the determinism obligation on C OMPILER
becomes the requirement that a confirmed intent map to exactly one effect.
The domains where this matters are not exotic. Any setting that combines a fixed data model, recurring
question shapes, and a reader who acts on the answer without auditing it is a candidate: enterprise
and operational reporting, clinical and ward-level summaries, financial and regulatory reporting,
supply-chain and inventory status, and the growing class of agents that read a figure and then do
something about it. What varies across them is the confirmation vocabulary and the compilation
target (Table 2); the invariant does not vary at all.
We flag the action form because the failure mode that motivated the pattern is worse for actions than
for values, which makes it a question of agent safety rather than only of output quality. A wrong
figure can at least be contradicted later by a right one. An executed action has already happened, and
tool-using agents are now routinely given effects to execute on the strength of an inference no one
inspected. We have not built such a system, and offer the generalization as a hypothesis with a clear
shape rather than as a result.

5     A Deployed Instantiation
We now fill in the first column of Table 2 in detail. G ROUNDER was a bilingual conversational
analytics interface operated in production for roughly two years.2 It is offered as an existence proof
and a set of worked choices, not as the only way to satisfy Section 3.

5.1    The setting

Users were sales staff responsible for retail channel performance across a large region. Their questions
concentrated on a few recurring shapes — how much of a product sold, how much is in stock, what is
forecast, how many people entered a store — each sliced by product, geography, channel, and time.
The questions were quantitative, tolerance for error was low, and the same shape recurred constantly
with different values filled in.
Against Section 3.5: output was consumed as fact (users could not read SQL and never saw it),
demand was structurally repetitive, and a wrong figure entered a decision while a refusal cost a delay.
All three preconditions held, which is why we describe this instantiation rather than a different one.
Table 3 lists the structural features of the domain that shaped the design. It is written in terms of
feature classes rather than the organization’s vocabulary, because the features are what transfer; a
reader in supply chain or clinical reporting should recognize their own analogues in the left-hand
column.
A further property cuts across all of them: the warehouse was organized hierarchically along every
axis at once, so the intersection of axes determined which relation held the answer. There was no
single table to query, and choosing correctly is most of the work — exactly the choice later enterprise
benchmarks find models make badly [Lei et al., 2025, Chen et al., 2024].
Finally, entity names in this domain were largely proper nouns in a non-English script denoting
individual outlets. They are not translatable, not reliably segmented by general-purpose tokenizers,
and must be resolved against a registry rather than interpreted (Section 8).
    2 The system’s internal name is omitted; we refer to it here as G ROUNDER . Nothing in the design depends on the identity of

the organization, and no implementation detail specific to it is disclosed (Section 1).


                                                              10
Table 3: Structural features of the domain, stated generically. The right-hand column is what matters:
each feature is a reason the mapping from question to query is not obvious, and therefore a reason to
fix that mapping at authoring time rather than infer it per query.

 Feature                 Instance in this domain                 Consequence for the design
 Hierarchical entity     A product family and the specific       The level asked about determines which
 with grain-dependent    models within it.                       physical relation can answer; the two
 storage                                                         grains are stored separately.
 Non-disjoint            Membership labels on a retail store:    A request spanning two labels has no
 classification          a store may hold more than one.         correct aggregation. This is the
                                                                 consistency test of Section 3, and
                                                                 Section 6.4 walks the case.
 Structurally            Tiers of intermediary between           The subtype named changes the query’s
 divergent subtypes      manufacturer and retailer.              shape, not merely a filter value.
 Multiple measures,      Units sold, units in stock, projected   Measures live in different places and
 unevenly available      sales, visitor counts.                  some are meaningless at some time
                                                                 grains, so measure and grain cannot be
                                                                 chosen independently.
 Organization-specific   A fiscal calendar misaligned with the   Users mix fiscal, absolute, and relative
 calendar                ordinary one, e.g. a label denoting     dates freely, making date handling a
                         the third week of a fiscal quarter.     resolution problem rather than a parsing
                                                                 one.


5.2   Requirements

Five requirements followed, and they map onto the pattern:

1. Intent identification from underspecified input. Users arrive with a product name, not a question.
   (I NTERPRETER, E LICITOR.)
2. No fabricated entities or figures. A plausible wrong answer is worse than a refusal. (The
   perimeter invariant.)
3. Exact arithmetic. Aggregations, comparisons, and rankings computed by the query engine, not
   approximated by a model. (C OMPILER.)
4. Interactive latency. Conversational turnaround; per-turn model round trips are a budget item, not
   free.
5. Tolerance of scarce training data. At the outset there was no corpus of question–query pairs for
   the domain and no traffic from which to bootstrap one.

Requirement 5 drove sequencing as much as architecture, and generalizes: a kernel-first system can
be built before any data exists and produces labeled data as a byproduct of being used, whereas a
learned parser cannot. The corpus that later made a fine-tuned alternative possible (Section 9) was
the kernel’s output.

5.3   Pipeline

G ROUNDER processed each user turn through four stages (Figure 3), which realize the four roles of
Table 1:

1. Conversation guidance maintains dialogue state, extracts and predicts entities, detects inconsis-
   tencies, and decides whether the turn has produced an answerable question or requires another
   exchange.
2. Question grounding matches the accumulated entity set against the template pool and obtains
   explicit user confirmation of the resolved question.
3. SQL generation compiles the grounded question into a query via an intermediate parse tree.
4. Answer generation renders the result set into a sentence.


                                                   11
                        no template match



          Conversation                       Question                      SQL                     Answer
           guidance                         grounding                    generation               generation

Figure 3: The four-stage pipeline. Only conversation guidance and answer generation involve a
language model; grounding and SQL generation are deterministic. Failure to match a template returns
control to guidance rather than producing a best-effort query.


Stages 1 and 4 are the shell; stages 2 and 3 are the kernel. A language model contributes to the
shell, where it produces prompts and prose. The kernel — the two stages that jointly determine
which number the user receives — contains no learned component. This is the perimeter invariant of
Section 1, realized as a pipeline boundary, and its consequence is that the system’s errors are errors
of coverage (it declines a question it could in principle have answered) rather than errors of fact.
The return arrow in Figure 3 is doing more work than it appears to. In a generative pipeline there
is no such arrow: every input produces a query, because producing a query is what the model does.
Here, failure to match a template is a defined outcome that hands control back to the shell. Most of
what makes the system trustworthy is a consequence of that arrow existing.

5.4    Entities and entity vectors

An entity is a typed value the system recognizes: a product, a metric, a date or range, a geography, a
store or reseller. Entities are what carry user interest, and the system’s model of the current dialogue
state is essentially a record of which entity types have been pinned down.
We represent a question as an entity vector: a binary vector over entity-type dimensions indicating
which types are present. For the question “How many Phone 12 did store A sell yesterday?” over
the dimensions (product, place, property, date, store), the vector is (1, 0, 1, 1, 1) — product, property,
date and store are supplied; place is not.3
This representation is deliberately coarse. It discards which product was named and retains only that
a product was named. That loss is what makes it useful: the vector is a compact address into the
space of partially specified questions, and the template pool is indexed by the same space. Resolved
entity values are carried alongside in a dictionary:

                                                    Key          Value
                                                    FAMILY       phones
                                                    SALES        sales
                                                    CITY         Riverton

5.5    Template pool

The set of answerable questions is defined extensionally by a pool of templates with typed slots:

      Template                                                              Slot types
      How many _MODEL_ _INVENTORY_ did _CITY_                               model, measure, geography
      have?
      What are the _FAMILY_ _SALES_ by                                      family, measure, store class, geography
      _STORECLASS_ in _CITY_?
      Which _STORECLASS_ are in _REGION_?                                   store class, geography
      How much _TRAFFIC_ did _CITY_ have in                                 measure, geography, fiscal period
      _QUARTER_?

The pool held a few thousand templates. Each template is associated with the target table, the
slot-to-column mapping, and the aggregation semantics required to answer it; Appendix B describes
   3 Place and store are distinct dimensions: a store name may be given without a geography, and vice versa. The dimensions

are not independent, and Section 6 exploits their correlation for next-entity prediction.


                                                              12
the record structure. A question is grounded when its entity vector and dictionary jointly satisfy a
template’s slot requirements.
Two properties follow. The pool is an explicit, inspectable specification of system capability, which
means coverage gaps are measurable and the roadmap is a list. And because grounding is a matching
operation rather than a generation operation, an ungroundable input is detected as such instead of
being coerced into the nearest template.

6     Conversation Guidance
Conversation guidance converts underspecified input into grounded questions. It operates in three
modes, selected by how much of a template the current turn satisfies.

6.1    Three modes

Question answering. The input is already complete: it grounds against a template directly, and
the system answers. User: “phone sales in Riverton.” System: “Riverton had 5,100 phone sales on
2024-01-27.”4 This mode is accurate and fast, and in isolation also brittle: it requires users to phrase
questions the way the pool expects, which is not how people talk.

Question guidance. The input is incomplete, and the system elicits the remainder one entity at a
time:

           User: sales
           G ROUNDER: Got it! Could you provide additional details on sales?
           User: phones, premium-tier stores, Riverton
           G ROUNDER: If I understand correctly, you’re asking “What are the phone sales by premium-
           tier store in Riverton?” — is that correct?

The elicitation order is not fixed; it is driven by next-entity prediction (Section 6.3). The mode’s
weakness is that predictions can be wrong, producing a clarifying question the user finds irrelevant.
The failure is recoverable, since the user simply supplies a different entity, but it costs a turn.

Question suggestion. Neither of the above succeeds: the user’s intent falls outside the pool, or
repeated elicitation has failed to converge. Triggered by explicit dissatisfaction (successive negative
responses, or a thumbs-down), the system abandons the current path and proposes the nearest
answerable questions instead. This is the mode that makes the system’s boundary honest. It does not
claim to answer what was asked; it states what can be asked.

6.2    Automaton over entity states

Dialogue state is a point s ∈ Rd in an embedding space over which a finite set of discrete states is
defined, each corresponding to a configuration of pinned-down entities. Transitions are governed by
a pushdown automaton, whose stack discipline lets the system suspend a partially specified question,
resolve a sub-question, and resume. A user interrupting a sales query to ask how many stores of a
given type exist in the city under discussion is the common case [Grosz and Sidner, 1986].
Given the entity vector vq ∈ Rd extracted from the current turn, the conversation context embedding
ectx ∈ Rm , and the user profile embedding eu ∈ Rn , the next state is assigned by nearest neighbor:
                                                                                  
                  snext = NearestNeighborState scur + vq ⊗ (Wa · [ectx , eu ]) ,                 (1)

where Wa ∈ Rd×(m+n) is a learned attention matrix [Vaswani et al., 2017] and ⊗ denotes the
element-wise product.
Equation 1 composes three sources of information. The current state scur carries what has been
established. The attention term Wa · [ectx , eu ] scores entity dimensions by their relevance given the
conversation so far and who is asking. The element-wise product with vq gates that scoring by what
    4 All numeric values in worked examples throughout this report are synthetic. Question forms, entity types, and system

responses are faithful to the deployed system; sales and inventory figures are not actual figures and should not be read as such.


                                                              13
the current turn actually mentions, so relevance only moves the state along dimensions the user has
touched. Projection back onto the discrete state set via nearest neighbor is what keeps the dialogue
inside the space of configurations the system can act on.
The discretization is essential rather than incidental. A continuous dialogue state, as in learned belief
trackers [Mrkšić et al., 2017, Wu et al., 2019], would admit configurations with no corresponding
template and no defined next action. By construction, every state our automaton can occupy has both.

6.3   Next-entity prediction and prompt generation

The distribution of entity vectors observed in production is far from uniform: certain entity types
co-occur, and a user who has named a product and a metric is overwhelmingly likely to want a
geography next. We exploit this to choose which entity to elicit, so the system asks the question most
likely to complete the template rather than walking slots in a fixed order.
The user profile embedding eu personalizes this. Built from the user’s query history, it captures
habitual scope: the cities, product families, and store types this analyst usually asks about. That scope
both biases elicitation order and supplies defaults. A user whose history is dominated by one city,
asking about “phone sales yesterday,” is more plausibly asking about that city than about the national
total.
Given scur and the predicted snext , the prompt shown to the user is generated by a language model:
                                  suggestion = LLM(scur , snext ).                                    (2)
This is the model’s entire role in the guidance stage, and it is worth being precise about why the
role is safe. The model does not decide what to ask about; Equation 1 does. The model renders a
transition between two known states into a fluent sentence. If it renders badly the user is confused for
a turn; it cannot cause a wrong number to be returned, because it has no influence on grounding or
query construction.

6.4   Detecting requests that have no correct answer

This is the most instructive behavior in the system, and it is worth walking through slowly, because it
is where a bounded pool earns its cost.
Recall from Table 3 that store classes overlap: a single store may be both premium-tier and standard
authorized. Now consider a user who asks for sales across both classes in one city. The request is
grammatical, it is specific, every term in it is a real term, and a reasonable person would read it as a
perfectly clear question. It has no correct answer. Summing the two classes double-counts the stores
in both; taking either alone answers a different question; deduplicating silently picks an interpretation
the user never chose. No single table serves the request, and no arithmetic on the available tables is
unambiguously what was meant.
What G ROUNDER does is notice, and say so:
         User: premium-tier and standard authorized stores, Riverton.
         G ROUNDER: You have mentioned premium-tier stores and standard authorized stores. Let’s
         focus on one at a time. . . .
         User: premium-tier stores.
         G ROUNDER: From what I gather, your question is about “What are the phone sales by
         premium-tier store in Riverton?” — is that correct?

A generative system asked the same thing produces a query. The query is valid, it runs, and it returns
a number of entirely plausible magnitude. Whether that number double-counts depends on which
interpretation the model happened to settle on, which the user cannot see and would have no reason
to suspect. The failure is not loud. It is a slightly wrong figure in a slide deck, and it survives.
The claim is not that the constrained design handles this case more gracefully. The claim is that it
is capable of noticing, because it holds an explicit representation of what it can and cannot express.
Noticing forces the ambiguity back into the conversation, where the one person who can resolve it is
standing: the person who asked.
Grounding then closes with the confirmation turn, the kernel boundary of Section 1 made visible.
The user has read, in ordinary language, the exact question their number will answer. This is the


                                                   14
interaction NaLIR [Li and Jagadish, 2014] introduced for parse trees, moved up a level to the question
itself, on the theory that users can check a sentence and cannot check a parse.

6.5   Dialogue history embeddings

The mechanism above conditions on a context embedding ectx summarizing the conversation. A
refinement in development at the time of writing maintained a running history embedding updated
per turn through an attention module over the full question–answer record, rather than primarily the
preceding turn. The motivating case is anaphora, which is also the central difficulty in conversational
semantic parsing benchmarks [Yu et al., 2019b,a]:

         User: phone sales yesterday → resolved against profile to a specific city
         User: How many premium-tier stores are there?
         After attention: How many premium-tier stores in {city}?
         G ROUNDER: There are 20 premium-tier stores in {city}.
         User: Which store has the top Phone 12 sales?
         G ROUNDER: Are you asking about all stores in {city} or these 20 premium-tier stores?

Attending over the whole history lets “there” bind to a city mentioned two turns earlier. More
interestingly, it lets the system recognize that the third question is ambiguous between two salient
scopes, and ask instead of assuming. Open problems include the granularity of the discrete state
embedding and maintaining content diversity in generated prompts across long sessions. The module
was under active development in early 2024 and landed before the end of the project; the attention-
based dialogue engine, pushdown automaton, and entity-vector extraction described above were all
in the shipped system.

6.6   Engagement surfaces

Three secondary surfaces reused the same machinery, and are worth recording because they cost little
once the entity representation existed.
Homepage question recommendation. Each user’s landing page proposed questions drawn from the
template pool, ranked by a DSSM-style dual encoder [Huang et al., 2013] over the profile embedding
eu and the template representation. Because every recommendation is a pool member, a recommended
question is by construction answerable — the recommender cannot suggest something the system
will then decline, which is the usual failure of recommending queries to a natural language interface.
Autocomplete ranking. Partial input was completed against the pool rather than against a general
language model, so completions doubled as capability disclosure: what the system offers to finish is
what it can answer.
Daily summaries. Scheduled digests rendered a user’s habitual questions against fresh data, person-
alized by the same profile embedding. These required no dialogue at all — the questions were already
grounded — which made them the cheapest surface to build and, per Section 10, a disproportionate
share of what users valued.

7     SQL Generation
Once a question is grounded, compilation to SQL is deterministic.

7.1   Matching and parse-tree construction

Grounding first extracts key information with regular expressions, then selects a template by combin-
ing entity-vector match with sentence similarity against the pool. The matched template determines
an intermediate parse tree whose interior nodes are SQL constructs — SELECT, FROM, WHERE, GROUP
BY, HAVING — and comparison and logical operators, and whose leaves are entity slots. Resolved
dictionary values populate the leaves with concrete table and column names.
For a question of the form “store Phone 11 sales ≤ 10 and inventory > 5 on 2023-09-19,” the
extracted entities (STORE=store, MODEL=Phone 11, MEASURE=sales, MEASURE=inventory, DATE=2023-
09-19) together with the operators (≤ 10, > 5, conjunction) yield a tree with an A SK E NTITY root, an


                                                   15
Algorithm 2 Parse tree to SQL by depth-first traversal
 1: function E MIT(node, dict)
 2:    if I S L EAF(node) then
 3:          return R ESOLVE(node.slot, dict)                                     ▷ table/column/literal
 4:    end if
 5:    children ← [ ]
 6:    for all c ∈ node.children do
 7:          children.append(E MIT(c, dict))
 8:    end for
 9:    return R ENDER(node.type, children)
10: end function



A ND node over two C OMPARE subtrees, and a W HERE node carrying the date predicate. Appendix C
works the example through to emitted SQL.

7.2   Depth-first emission

SQL text is emitted by depth-first traversal (Algorithm 2). Each node type knows how to render
itself given its rendered children, which is what makes the compiler modular: a new aggregate or
comparison is a new node type, not a change to the traversal.
The resulting query for the running example targets the store-daily sub-LOB table, aggregating the
sell-out measure with the appropriate predicates and a HAVING clause carrying the numeric threshold.
The same tree structure, with a different template mapping, compiles against the LOB-grain table
when the question is asked at product-family rather than model level.
Decomposing operations into primitive nodes is what lets the system handle compositional numeric
questions — thresholds, ratios, top-k rankings — without a combinatorial template pool, since a
template fixes the question shape while the tree composes the arithmetic. This is also the component
that satisfies requirement 3 from Section 5.1: arithmetic is performed by the database engine, and
no model is asked to compute a sum. The same delegation principle, applied to a generative model
rather than a compiler, underlies program-aided prompting [Gao et al., 2023].

7.3   Answer generation

The result set is rendered into a sentence, using the confirmed question as the frame. Because the
question was assembled from known entities and confirmed by the user, the rendering is a templating
operation over a small result set rather than a summarization task. Free-text summarization is reserved
for the alternative architecture in Section 9, where result shape is not known in advance.


8     Bilingual Support

Users queried in two languages and in mixtures of them: an English-language schema underneath,
and a user population working partly in another language whose entity names use a different script.
Two components handled this, and the division between them is the transferable part.
The first component translates the shape of the question. A compact open translation model [Tiede-
mann and Thottingal, 2020] normalized each query into the schema’s language before entity extrac-
tion, so that a single extraction and grounding path served both languages instead of two parallel
pipelines. A small model was chosen deliberately, since the translation sits on the critical path of
every non-primary-language turn (requirement 4).
The second component recognizes rather than translates. Translation is the wrong tool for outlet
names, which are proper nouns in a non-Latin script that a general model will either transliterate
inconsistently or render semantically, turning a branch name into a description of one. We therefore
applied a named-entity recognition model [Lample et al., 2016, Zhang and Yang, 2018] to extract
outlet and reseller mentions before translation, and matched them against the canonical registry
directly.


                                                  16
The division of labor matters more than either component: the question form is translated, while
the entity values are recognized and resolved against ground truth. Translating the whole query and
hoping the names survive fails on exactly the questions users most want to ask, since a specific branch
is often the point of the question.


9     Designs Considered

We implemented two generative alternatives. Neither replaced the rule-grounded core; both informed
it. We describe them because the reasons are more instructive than the conclusion.

9.1   Fine-tuned text-to-SQL model

We fine-tuned a customized LLM on three tasks: text-to-SQL, response template generation, and
context completion. Training data came substantially from the rule-grounded system — its template
pool and the question–SQL pairs accumulated through its operation — which is the payoff of having
sequenced the heuristic system first: a few thousand templates and a corpus of question–query pairs
on the order of tens of thousands, all of it a byproduct of the kernel being used. Training fit on a
single multi-GPU node in a few hours, and inference was served through an acceleration runtime of
the kind described by Rasley et al. [2020]. Appendix D records the procedure.
Iterating on the data taught us more than iterating on the model, and four interventions account
for most of the improvement. Standardizing trigger words across the training set tightened control
over which entities the model would accept and emit, buying consistency at the cost of tolerance
for paraphrase. Shortening the target queries, by removing redundant qualification and nesting,
measurably improved generation quality, on what we take to be the principle that shorter targets are
easier to learn. Injecting random noise into inputs improved robustness to the malformed and code-
switched queries that characterize real traffic. And appending manually annotated high-frequency
questions improved accuracy on the head of the query distribution, which is where user-perceived
quality is decided.
The model reached usable quality on common question shapes. What it did not provide was a signal
distinguishing its correct outputs from its incorrect ones. A fluent query against a plausible-looking
column, returning a number of the right magnitude, is indistinguishable at the interface from a
correct answer; and the general difficulty of eliciting reliable self-assessment from language models
[Kadavath et al., 2022] gave us little reason to expect a usable confidence threshold. For our users
this is disqualifying as a primary path, though not as a fallback for inputs the pool cannot ground. In
the event we did not deploy it in either role: the direction that superseded the rule-grounded core was
the tool-retrieval pipeline described next, not this model.

9.2   Tool-retrieval agent

The second prototype gives a general LLM a set of retrieval tools and lets it assemble the query
itself, in the manner of retrieval-augmented generation [Lewis et al., 2020] and learned tool use
[Schick et al., 2023]. For “How many tablets did {store} sell three days ago?” the agent calls an
entity-resolution tool to map the relative date to a fiscal date and the colloquial store name to a
canonical registry entry, then emits SQL against the resolved values, executes it, and summarizes
the result — using the result’s shape and a few sample rows, with few-shot examples, to produce the
final sentence.
This design has real advantages. It is close to language-agnostic, since entity resolution rather than
translation carries the burden. It handles date formats the rule-based extractor would need explicit
patterns for. And its intermediate steps are legible: the tool calls and their returns are an audit trail of
how the model arrived at a query [Yao et al., 2023], which is more transparency than the fine-tuned
model offers.
Its cost is latency and non-determinism. Multiple sequential tool calls per turn, each a model round
trip, sit poorly with requirement 4, and the same question can take different paths on different
occasions. Backend work mitigated the first of these — an inference-acceleration runtime for the
model and a columnar analytical engine for the queries brought the pipeline inside an interactive
budget — but mitigation is not elimination.


                                                    17
                                         Generative pipeline
                                                                           answered
                                     answered correctly
                                                                            wrongly

                                                                 indistinguishable, at the point
                                                               of use, from the region on the left




                                         Kernel-first pipeline

                                  answered correctly                     declined

                                                                    visible to the user,
                         narrower, by construction
                                                                   with a recovery path


Figure 4: What the pattern trades. The kernel-first system answers a narrower band of requests and
converts the remainder into refusals the user can see and act on; the generative pipeline answers a
wider band but leaves its errors mixed in with its successes, unmarked. Widths are schematic and
carry no measurement: the argument does not depend on where the boundaries fall, only on the fact
that in the upper case there is no boundary the user can locate.


This is the design the system was transitioning onto at the end of the period covered by this report.
Over the final phase of the project the pipeline moved from the heuristic question-answering core to
a modular LLM pipeline combining prompt engineering, retrieval augmentation, and tool retrieval,
with grounded answers produced by real-time SQL execution. We describe it here as an alternative
considered because that is what it was for most of the system’s life, and because the comparison in
Section 9.3 is what determined which alternative won.

9.3   What held, and what replaced it

The comparison isolates a distinction that travels beyond this application, and Figure 4 is the whole
of it in one picture. All three systems make mistakes. They differ in how the mistakes present.
The rule-grounded system fails by declining, visibly, and with a recovery path the user can act
on. A model that generates SQL end to end fails by answering: fluently, and with no signal that
anything went wrong. Where an interface’s output is consumed as fact rather than inspected as a
draft, the first failure mode is preferable even at a substantially lower coverage rate, and this is why
the rule-grounded core carried production traffic for the bulk of the system’s life rather than being
replaced as soon as a learned parser became feasible.
How that core was eventually superseded is the more interesting half of the story, and it supports
rather than undercuts the argument. The successor was not the fine-tuned parser, which had broader
coverage and no auditability. It was the tool-retrieval pipeline, the alternative that retained the two
properties the constrained design existed to protect. Arithmetic stayed delegated to the database
rather than generated, and the tool-call trace preserved a partial audit path where the fine-tuned model
offered none (Table 4). What was given up was determinism and per-turn latency; what was kept was
the refusal to let a model compute the number.
Table 4 summarizes the comparison.


10    Deployment and Usage

G ROUNDER ran in production for roughly two years, following about a year of development on
the kernel, and established three things. The pattern is implementable: a kernel-first system with
a generative shell can be built and kept running against a live warehouse by a small team. It is
affordable at conversational latency, which was the requirement most at risk from the generative
alternatives (Section 9). And it bootstraps its own successor, since routine operation accumulated a
corpus of question–query pairs large enough to fine-tune a parser on, which is the concrete form of
the sequencing argument in Section 5.1.


                                                          18
Table 4: Three architectures for the same task, compared on the axes that decided between them.
The columns correspond to the three approaches available: a bounded kernel, an end-to-end learned
parser, and a tool-using agent. The final row records what became of each in our deployment.

                           Kernel-first            End-to-end            Tool-using
                           (this paper)            parser                agent
        Coverage           Pool-bounded            Broader               Broadest
        Failure mode       Visible decline         Fluent wrong answer   Fluent wrong answer
        Determinism        Yes                     Per-checkpoint        No
        Latency per turn   Lowest                  Moderate              Highest (multi-call)
        Arithmetic         Delegated to database   Generated             Delegated to database
        Auditability       Full (fixed mapping)    None                  Partial (tool trace)
        Cold-start data    None required           Corpus required       None required
        Disposition        Production core         Not deployed          Successor pipeline




G ROUNDER was commissioned because business teams depended on technical staff to query frag-
mented dashboards, and after deployment those teams could self-serve the recurring questions that
had previously been requests to an analyst.
There is one measurement we should have taken and did not: the share of turns resolved by direct
answering, by elicitation, and by disclosure. The three modes were never instrumented separately,
and that distribution is the one number that tells a team whether their pool is converging on demand or
falling behind it. Anyone building to this pattern should instrument the three branches of Algorithm 1
from the first deployment. It is a cheap counter, and it answers the only question that matters about
coverage.




11    Discussion


Three things about building this surprised us, and all three concern the template pool rather than the
model.
The pool became the specification. We introduced it as an implementation device for matching
questions, and it ended up serving as the system’s capability contract: product discussions about what
G ROUNDER should do next resolved into concrete additions, and coverage gaps became countable
rather than anecdotal. This is an underrated benefit of defining capability extensionally. A learned
parser’s coverage is an empirical question you answer by sampling; a pool’s coverage is a list you
read.
Building the deterministic system first was load-bearing rather than expedient. We initially treated
it as scaffolding to be replaced once data existed, but the causality ran the other way: the system
was the only mechanism by which the data could come to exist (Section 5.1, requirement 5), and the
corpus that made the fine-tuned prototype possible was its output. Teams in a similar position, with
no question–query corpus and no traffic to bootstrap one, should treat a constrained system not as a
fallback but as a data acquisition strategy.
Data iteration then dominated model iteration. The four interventions of Section 9 produced larger
quality movements than any architectural change we tried, which is a familiar lesson, though it was
not obvious in advance that shortening the target queries would matter as much as it did.
Two things we would do differently, both of them cheap and both omitted for no good reason. We
would instrument the three branches of Algorithm 1 from the first deployment rather than retrofitting
the measurement (Section 10). And we would treat the confirmation turn as a capability-disclosure
surface from the start, since users’ mental models of what the system could answer were formed by
trial and error long before the disclosure branch existed to shape them [Amershi et al., 2019].


                                                   19
12    Revisiting the Design in 2026

Two years have passed since we last worked on this system, and the intervening period was not a
quiet one for the technology it declined to rely on. It would be convenient to report that the design
has aged well. Partly it has, and partly the reasons it has aged well are not the reasons we expected.
The problem turned out to be harder than the benchmarks of the time suggested. When we chose
a bounded pool over a learned parser in 2021, the honest description of our reasoning was caution
rather than evidence: published text-to-SQL accuracy looked strong, our schema looked worse than
the published ones, and we did not want to find out the difference in production. Benchmarks built
later on enterprise warehouses suggest the gap was much larger than caution would have guessed.
On Spider 2.0, whose databases come from real industrial applications and often exceed a thousand
columns, an agent framework over a frontier reasoning model solved 21.3% of tasks where the same
class of system had reached 91.2% on the original Spider [Lei et al., 2025]. On BEAVER, sourced
from private warehouse query logs, off-the-shelf models scored near zero end-to-end, and handing
them the correct tables and column mappings as hints raised the best model only into low single digits
[Chen et al., 2024]. The failure modes reported are wrong table selection, wrong column mapping,
and missed implicit assumptions, and a template pool resolves all three by construction, at authoring
time, once per question shape. We note this without triumph: it is retrospective vindication of a
decision made for weaker reasons than the evidence now available would supply.
The gap we designed around has meanwhile become a research area. The report’s central complaint,
that a generated query gives no signal distinguishing its right answers from its wrong ones, is no
longer an observation one has to argue for. TrustSQL [Lee et al., 2024] names the same two obstacles
we hit — users cannot tell what the system can answer, and unnoticed incorrect SQL destroys trust —
and scores systems by weighing correct answers against wrong ones under an explicit penalty, which
is our qualitative tradeoff made quantitative. Work on selective prediction for SQL now attacks the
same problem from the model side [Somov and Tutubalina, 2025, Chen et al., 2025]. That literature
also locates our approach in a design space we could not see at the time, as the structural rather than
the statistical answer (Section 3.6); we took the structural route because in 2021 it was the only one
that worked, and it remains the route with the stronger guarantee. The industry pattern that has since
converged on it, a curated semantic layer that a deterministic runtime either serves or errors on, is
recognizably the template pool of Section 5.5 under a better name.
Honesty requires the other column of the ledger, and three parts of the system are now obsolete. The
fine-tuned parser of Section 9, with its bespoke corpus and its from-scratch training run, is not how
anyone should approach this now. The hand-assembled bilingual front end of Section 8, a small
translation model plus a purpose-trained entity recognizer, solved a problem that current multilingual
models largely do not have. And the engineering we did to keep a multi-step tool-using pipeline
inside a latency budget has been substantially commoditized by standardized tool calling and cheaper
inference.
None of those obsolescences touch the invariant, which is the part we would keep. Faster models
and standardized tool calls make the shell cheaper to build, and change nothing about whether a
model should be permitted to compute the number a decision rests on. Reasoning models are better
at arithmetic than their predecessors and still worse at it than a database. The confirmation turn costs
a user two seconds and remains the only mechanism in the design that lets a non-technical person
verify what they are about to be told a number about. If we were building this today we would keep
the kernel, discard nearly all of its implementation, and put an agent in the shell, routing on grounding
success instead of on a confidence score (Section 14). The architecture was right and most of the
code was incidental.


13    Limitations

The central claim of this report has not been tested directly. Testing it would not mean measuring
execution accuracy, which measures the wrong thing here, but measuring user-detected error rate:
presenting the same questions to a kernel-first system and to a generative one, and counting not
how often each is wrong but how often a user notices. We know of no such study, so the claim that
visible failure beats fluent failure remains an argument from design rather than a measured result.
The pattern has also been built once, in one domain, by us; Table 2 specializes it elsewhere on paper,


                                                   20
which shows the five decisions can be answered in another setting and shows nothing about whether
the resulting system would work.
Three costs are intrinsic rather than incidental. Coverage is bounded by construction, since questions
outside the pool can only be redirected, and the pool grows by manual authoring at a rate set by
engineering attention rather than by user demand. Elicitation costs turns: a user who knows exactly
what they want and can phrase it well is served worse by G ROUNDER than by a system that simply
parses their sentence, because the design optimizes for the underspecified case and the confirmation
is overhead for anyone who does not need it. And personalization has a cold start, in that the profile
embedding requires history, so new users receive a generic elicitation order and no defaults.
The sharpest limitation is that a whole class of users is better served by the architecture this report
argues against. Consider an exploratory research analyst investigating an anomaly in a dataset she
knows well. Her questions are novel by nature, each shaped by the answer to the last; she reads SQL
fluently and will inspect whatever she is given; and being told “I cannot answer that, but here are
four things I can” is not a graceful refusal but an obstruction. All three preconditions of Section 3.5
fail at once. For her a generative copilot is not a compromise but strictly the right tool, and a kernel
would make her slower at no benefit. The pattern earns its cost only where the user cannot verify and
the question shapes repeat, which excludes a large and visible share of the people currently building
natural-language data tools.
It follows that this is not an automated analyst, and it is worth saying so plainly, because the phrase
attaches easily to systems like it. What the pattern automates is the queue, not the judgment. The
manager of Section 1 waited two days for a figure that was recurring, parameterized, and known to
be answerable; a human was in that loop only because no machine could be trusted in it. Removing
the recurring requests is what frees an analyst for the exploratory questions no kernel can express —
which is the same division the pattern draws internally, deterministic machinery for what is known
and a generative shell for what is ambiguous, applied at the scale of a team rather than a system. A
product that claimed to replace the analyst outright would be claiming to have solved the half of the
problem this pattern deliberately declines.

14    Directions We Would Have Pursued
The roadmap below is the one we held at the end of our involvement; we offer it as design analysis
rather than as a statement of anyone’s current plans.
The natural extension is a hybrid in which the rule-grounded path handles groundable questions and
a tool-retrieval agent handles the remainder, with the routing decision made by grounding success
rather than by a confidence score. This preserves the property we care about — that the deterministic
path is deterministic — while converting question suggestion from a graceful decline into an actual
answer. The open problem is presentation: if answers arrive from two paths with different reliability,
the interface must communicate that difference without eroding trust in either.
Beyond this: broadening the engagement surfaces of Section 6.6, where the strongest untried idea
was to let observed acceptance of recommended questions drive template authoring, closing the loop
between what users ask for and what the pool covers; and extending the pool beyond the single retail
channel it served to the others alongside it.

15    Conclusion
A fact-consumed system has a problem that accuracy alone does not solve: whoever receives its
answers cannot tell the right ones from the wrong ones. The pattern in this report answers that by
dividing the system in two and letting a generative model operate only on the side where mistakes
are visible. A language model shapes the question; it never computes the answer. The two halves
meet at a sentence the user reads and assents to, and requests the deterministic half cannot express
are declined instead of approximated.
The specific system we built to this design is now largely obsolete in its implementation and was
never the interesting part. What survives is the invariant, the five decisions of Section 4, and one
observation from watching the design compete against its own alternatives. When the constrained
core was eventually superseded, the successor was not the alternative with the broadest coverage. It


                                                  21
was the one that kept computation out of the model and left a trace of how it reached an answer, which
are the two properties the kernel existed to protect. The parser we abandoned was not abandoned for
being inaccurate. It was abandoned because when it was inaccurate, nobody could tell.

References
Saleema Amershi, Dan Weld, Mihaela Vorvoreanu, Adam Fourney, Besmira Nushi, Penny Collisson,
  Jina Suh, Shamsi Iqbal, Paul N. Bennett, Kori Inkpen, Jaime Teevan, Ruth Kikin-Gil, and Eric
  Horvitz. Guidelines for human-AI interaction. In Proceedings of the SIGCHI Conference on
  Human Factors in Computing Systems (CHI), 2019.
Ion Androutsopoulos, Graeme D. Ritchie, and Peter Thanisch. Natural language interfaces to
  databases – an introduction. Natural Language Engineering, 1(1):29–81, 1995.
Daniel G. Bobrow, Ronald M. Kaplan, Martin Kay, Donald A. Norman, Henry Thompson, and Terry
  Winograd. GUS, a frame-driven dialog system. Artificial Intelligence, 8(2):155–173, 1977.
Paweł Budzianowski, Tsung-Hsien Wen, Bo-Hsiang Tseng, Iñigo Casanueva, Stefan Ultes, Osman
  Ramadan, and Milica Gašić. MultiWOZ: A large-scale multi-domain wizard-of-Oz dataset for
  task-oriented dialogue modelling. In Proceedings of the 2018 Conference on Empirical Methods
  in Natural Language Processing (EMNLP), 2018.
Kaiwen Chen, Yueting Chen, Nick Koudas, and Xiaohui Yu. Reliable text-to-SQL with adaptive
  abstention. Proceedings of the ACM on Management of Data, 2025.
Peter Baile Chen, Fabian Wenz, Yi Zhang, Devin Yang, Justin Choi, Nesime Tatbul, Michael Cafarella,
  Çağatay Demiralp, and Michael Stonebraker. BEAVER: An enterprise benchmark for text-to-SQL.
  arXiv preprint arXiv:2409.02038, 2024.
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
  Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John
  Schulman. Training verifiers to solve math word problems. arXiv preprint arXiv:2110.14168,
  2021.
Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan, and
  Graham Neubig. PAL: Program-aided language models. In International Conference on Machine
  Learning (ICML), 2023.
Barbara J. Grosz and Candace L. Sidner. Attention, intentions, and the structure of discourse.
  Computational Linguistics, 12(3):175–204, 1986.
Matthew Henderson, Blaise Thomson, and Jason D. Williams. The second dialog state tracking
 challenge. In Proceedings of the 15th Annual Meeting of the Special Interest Group on Discourse
 and Dialogue (SIGDIAL), 2014.
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song,
  and Jacob Steinhardt. Measuring mathematical problem solving with the MATH dataset. In
 Advances in Neural Information Processing Systems (NeurIPS) Datasets and Benchmarks Track,
  2021.
Eric Horvitz. Principles of mixed-initiative user interfaces. In Proceedings of the SIGCHI Conference
  on Human Factors in Computing Systems (CHI), 1999.
Po-Sen Huang, Xiaodong He, Jianfeng Gao, Li Deng, Alex Acero, and Larry Heck. Learning deep
  structured semantic models for web search using clickthrough data. In Proceedings of the 22nd
  ACM International Conference on Information and Knowledge Management (CIKM), 2013.
Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin Bang,
  Andrea Madotto, and Pascale Fung. Survey of hallucination in natural language generation. ACM
  Computing Surveys, 55(12):1–38, 2023.
Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain, Ethan Perez, Nicholas
  Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli Tran-Johnson, et al. Language models (mostly)
  know what they know. arXiv preprint arXiv:2207.05221, 2022.


                                                 22
Guillaume Lample, Miguel Ballesteros, Sandeep Subramanian, Kazuya Kawakami, and Chris Dyer.
  Neural architectures for named entity recognition. In Proceedings of the 2016 Conference of the
 North American Chapter of the Association for Computational Linguistics (NAACL), 2016.
Gyubok Lee, Woosog Chay, Seonhee Cho, and Edward Choi. TrustSQL: Benchmarking text-to-SQL
  reliability with penalty-based scoring. arXiv preprint arXiv:2403.15879, 2024.
Fangyu Lei, Jixuan Chen, Yuxiao Ye, Ruisheng Cao, Dongchan Shin, Hongjin Su, Zhaoqing Suo,
  Hongcheng Gao, Wenjing Hu, Pengcheng Yin, Victor Zhong, Caiming Xiong, Ruoxi Sun, Qian
  Liu, Sida I. Wang, and Tao Yu. Spider 2.0: Evaluating language models on real-world enterprise
  text-to-SQL workflows. In International Conference on Learning Representations (ICLR), 2025.
Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal,
  Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, and Douwe
  Kiela. Retrieval-augmented generation for knowledge-intensive NLP tasks. In Advances in Neural
  Information Processing Systems (NeurIPS), 2020.
Fei Li and H. V. Jagadish. Constructing an interactive natural language interface for relational
  databases. Proceedings of the VLDB Endowment, 8(1):73–84, 2014.
Jinyang Li, Binyuan Hui, Ge Qu, Jiaxi Yang, Binhua Li, Bowen Li, Bailin Wang, Bowen Qin, Ruiying
   Geng, Nan Huo, et al. Can LLM already serve as a database interface? a big bench for large-scale
   database grounded text-to-SQLs. In Advances in Neural Information Processing Systems (NeurIPS)
   Datasets and Benchmarks Track, 2023.
Nikola Mrkšić, Diarmuid Ó Séaghdha, Tsung-Hsien Wen, Blaise Thomson, and Steve Young. Neural
  belief tracker: Data-driven dialogue state tracking. In Proceedings of the 55th Annual Meeting of
  the Association for Computational Linguistics (ACL), 2017.
Ana-Maria Popescu, Oren Etzioni, and Henry Kautz. Towards a theory of natural language interfaces
  to databases. In Proceedings of the 8th International Conference on Intelligent User Interfaces
 (IUI), 2003.
Mohammadreza Pourreza and Davood Rafiei. DIN-SQL: Decomposed in-context learning of text-
 to-SQL with self-correction. In Advances in Neural Information Processing Systems (NeurIPS),
 2023.
Jeff Rasley, Samyam Rajbhandari, Olatunji Ruwase, and Yuxiong He. DeepSpeed: System optimiza-
   tions enable training deep learning models with over 100 billion parameters. In Proceedings of the
   26th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD),
   2020.
Diptikalyan Saha, Avrilia Floratou, Karthik Sankaranarayanan, Umar Farooq Minhas, Ashish R.
  Mittal, and Fatma Özcan. ATHENA: An ontology-driven system for natural language querying
  over relational data stores. Proceedings of the VLDB Endowment, 9(12):1209–1220, 2016.
Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer,
  Nicola Cancedda, and Thomas Scialom. Toolformer: Language models can teach themselves to
  use tools. In Advances in Neural Information Processing Systems (NeurIPS), 2023.
Torsten Scholak, Nathan Schucher, and Dzmitry Bahdanau. PICARD: Parsing incrementally for con-
  strained auto-regressive decoding from language models. In Proceedings of the 2021 Conference
  on Empirical Methods in Natural Language Processing (EMNLP), 2021.
Oleg Somov and Elena Tutubalina. Confidence estimation for error detection in text-to-SQL systems.
  arXiv preprint arXiv:2501.09527, 2025.
Jörg Tiedemann and Santhosh Thottingal. OPUS-MT – building open translation services for the
  world. In Proceedings of the 22nd Annual Conference of the European Association for Machine
  Translation (EAMT), 2020.
Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez,
  Lukasz Kaiser, and Illia Polosukhin. Attention is all you need. In Advances in Neural Information
  Processing Systems (NIPS), 2017.


                                                 23
Bailin Wang, Richard Shin, Xiaodong Liu, Oleksandr Polozov, and Matthew Richardson. RAT-SQL:
  Relation-aware schema encoding and linking for text-to-SQL parsers. In Proceedings of the 58th
  Annual Meeting of the Association for Computational Linguistics (ACL), 2020.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc
  Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. In
  Advances in Neural Information Processing Systems (NeurIPS), 2022.
Chien-Sheng Wu, Andrea Madotto, Ehsan Hosseini-Asl, Caiming Xiong, Richard Socher, and
  Pascale Fung. Transferable multi-domain state generator for task-oriented dialogue systems. In
  Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (ACL),
  2019.
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao.
  ReAct: Synergizing reasoning and acting in language models. In International Conference on
  Learning Representations (ICLR), 2023.
Steve Young, Milica Gašić, Blaise Thomson, and Jason D. Williams. POMDP-based statistical
  spoken dialog systems: A review. Proceedings of the IEEE, 101(5):1160–1179, 2013.
Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, Dongxu Wang, Zifan Li, James Ma, Irene
  Li, Qingning Yao, Shanelle Roman, Zilin Zhang, and Dragomir Radev. Spider: A large-scale
  human-labeled dataset for complex and cross-domain semantic parsing and text-to-SQL task.
  In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing
  (EMNLP), 2018.
Tao Yu, Rui Zhang, He Yang Er, Suyi Li, Eric Xue, Bo Pang, Xi Victoria Lin, Yi Chern Tan, Tianze
  Shi, Zihan Li, et al. CoSQL: A conversational text-to-SQL challenge towards cross-domain natural
  language interfaces to databases. In Proceedings of the 2019 Conference on Empirical Methods in
  Natural Language Processing (EMNLP), 2019a.
Tao Yu, Rui Zhang, Michihiro Yasunaga, Yi Chern Tan, Xi Victoria Lin, Suyi Li, Heyang Er, Irene
  Li, Bo Pang, Tao Chen, et al. SParC: Cross-domain semantic parsing in context. In Proceedings of
  the 57th Annual Meeting of the Association for Computational Linguistics (ACL), 2019b.
Yue Zhang and Jie Yang. Chinese NER using lattice LSTM. In Proceedings of the 56th Annual
  Meeting of the Association for Computational Linguistics (ACL), 2018.
Victor Zhong, Caiming Xiong, and Richard Socher. Seq2SQL: Generating structured queries from
  natural language using reinforcement learning. arXiv preprint arXiv:1709.00103, 2017.


A    Entity Type Inventory
The types below are those exercised by the examples in this report, named as they appear in Table 3
rather than in the deployed system, whose slot names were tied to internal schema vocabulary. The
deployed registry was larger.

           Type          Example values                 Notes
           FAMILY        product family                 Top-level product axis
           MODEL         specific model                 Determines which table grain applies
           STORECLASS    premium-tier, standard, etc.   Overlapping; see §6.4
           STORE         store or reseller              Reseller tiers are stored separately
           CITY          city name
           REGION        province or region
           SALES         sell-out measure
           INVENTORY     inventory measure
           TRAFFIC       store visitors
           DATE          date, FY23Q4W3, “yesterday”    Fiscal and relative forms
           QUARTER       fiscal quarter
           NUM           numeric threshold              Operand for C OMPARE nodes



                                                 24
B    Template Pool Record Structure
Each template record carries five things: the surface form with typed slots; the entity vector the form
requires, which is what makes matching a lookup rather than a search; the target table, selected by the
grain the slots imply; the slot-to-column mapping; and the aggregation semantics, which determine
what the compiler of Section 7 emits for the SELECT and GROUP BY clauses.
Authoring a template therefore means answering the question “which table, at which grain, aggregated
how” once, at authoring time, rather than at query time. This is where the correctness guarantee
actually lives: the compiler is trusted because the mapping it applies was written and reviewed by
someone who knew the schema.
The pool was heavily concentrated on a few families, mirroring a query distribution with a short head
and a long thin tail. This is what makes the authoring cost tractable: the first few hundred templates
buy most of the coverage.

C    Worked SQL Compilation Example
The schema below is invented for this report. It is not the data model of any deployed system, and no
real table or column name appears; what is faithful is the shape of the compilation — which node
types exist, what each contributes, and where in the emitted query each lands. That shape is the
transferable content. Figures are likewise invented.

1. Matched question.        “store Phone 11 sales ≤ 10 and inventory > 5 on 2023-09-19”

2. Entity dictionary.

                                Slot           Value             Resolves to
                                STORE          store             grouping column
                                MODEL          Phone 11          model-level filter
                                MEASURE        sales             sell-out measure
                                MEASURE        inventory         inventory measure
                                DATE           2023-09-19        fiscal date filter
                                NUM            10, 5             thresholds

3. Parse tree.   Figure 5.

                                                           A SK E NTITY



                                        A ND                                    W HERE



                           C OMPARE             C OMPARE                    date = 2023-09-19



                        sales    ≤ 10     inventory    >5


Figure 5: The intermediate parse tree for the worked example. Interior nodes are query constructs
and operators; leaves are resolved slot values. Emission is a depth-first traversal (Algorithm 2), and
each node type renders itself from its rendered children, which is what lets a new aggregate be added
as a node type rather than as a change to the traversal.

4. Emitted SQL.      Depth-first traversal (Algorithm 2) renders the leaves, then each interior node
from its children:

         SELECT store_name, SUM(sales_measure) AS agg_sales
         FROM    store_sublob_daily
         WHERE model_name = ’Phone 11’
         AND fiscal_date = ’2023-09-19’


                                                       25
         GROUP BY store_name
         HAVING agg_sales <= 10 AND SUM(inventory_measure) > 5

Two details are worth drawing out. The thresholds land in HAVING rather than WHERE because they
constrain aggregates, and it is the C OMPARE node’s renderer — not the template — that knows this;
a template author cannot get it wrong. And asking the same question at product-family rather than
model grain changes only the template’s target table, leaving the tree identical.

D    Fine-Tuning Procedure for the Abandoned Alternative
Recorded as procedure, since the method and its ordering are what transfer.

Where the data came from. The corpus was not collected for the purpose. It accumulated as a
byproduct of the kernel running in production: every grounded question paired with the query the
compiler deterministically produced for it is a labeled example, generated at no annotation cost and
guaranteed correct by construction — the label is not a human’s guess at the right query, it is the
query that ran. This is the practical payoff of the sequencing argument in Section 5.1, and the reason
a kernel-first system is a data acquisition strategy rather than merely a stopgap.

Tasks. Three, trained jointly: question-to-query generation; generation of response templates; and
completion of context across turns.

Scale and cost. A few thousand question shapes and a corpus of pairs on the order of tens of
thousands; training fit on a single multi-GPU node in a few hours. The point worth carrying is
the ratio rather than the absolute figures: the fine-tuning run was cheap next to the year of kernel
development that produced its training data. Anyone reading this as a build-versus-train decision
should price the data, not the GPUs.

What moved quality. The four data interventions in Section 9 — standardizing trigger vocabulary,
shortening target queries, injecting input noise, and adding annotated head questions — produced
larger improvements than any architectural change attempted. The counterintuitive one was short-
ening the targets: removing redundant qualification and nesting from the training queries improved
generation more than we expected, which we read as targets being easier to learn when they are closer
to minimal.

Why it was not deployed. Covered in Section 9: it had no way to signal which of its outputs to
distrust, and so could not discharge the G ROUNDER obligation of Table 1 regardless of its accuracy.




                                                 26
