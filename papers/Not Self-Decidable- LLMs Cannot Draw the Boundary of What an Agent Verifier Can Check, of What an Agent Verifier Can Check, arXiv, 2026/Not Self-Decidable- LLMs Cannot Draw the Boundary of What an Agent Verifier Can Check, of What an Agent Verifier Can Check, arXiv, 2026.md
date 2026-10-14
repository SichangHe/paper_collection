                                        Not Self-Decidable: LLMs Cannot Draw the Boundary
                                                of What an Agent Verifier Can Check


                                                                                   Anthony Rhodes
                                                                                  Confidential Core AI
                                                                            a.rhodes@confidentialcore.ai
arXiv:2610.04699v1 [cs.AI] 3 Oct 2026




                                                                                           Abstract

                                                  A verifier for an agent faces rules of two kinds: the ones a fixed check can settle
                                                  and the ones that require a judge. A team that derives its own checks fixes that
                                                  split up front. Where the requirements come from outside, as they do in finance,
                                                  healthcare and law, the agent enforces rules it did not write, so the split falls to
                                                  runtime, recurring for every predicate of every rule on every action at a rate no
                                                  reviewer can audit.
                                                  Every escalation scheme assumes a model can make that decision itself, that it is
                                                  self-decidable. Across six corpora, including the EU AI Act, FINRA guidance
                                                  and a deployed credit agent, we collect roughly 22,000 labels from four models
                                                  built by three labs. They agree almost perfectly where the answer is obvious and
                                                  collapse on regulatory text, where predicates pile up on the boundary; their errors
                                                  run in opposite directions, so no model can be trusted as the conservative choice;
                                                  and on the deployed agent’s own rule-set they stop disagreeing and err together,
                                                  over-claiming that a fixed check will do, the direction that never gets escalated. We
                                                  introduce C OV ER (corroborate-then-verify), an algorithm that treats unanimity as a
                                                  nomination, admitting a predicate only when the check synthesized for it survives
                                                  intervention, reading fields the agent cannot write and holding under deterministic
                                                  rewording. That gate rejects most of what corroboration wrongly admits, at a cost
                                                  in coverage we report rather than tune away. Our central finding is that the obvious
                                                  alternative, agreement with a reference judge, certifies nothing: it climbs from
                                                  30% to 77% across calibration bands while the genuinely decidable share does not
                                                  move, because a judge drawn from the population under indictment ratifies the
                                                  blind spot it shares. Self-decidability is not a capability to elicit from a model but a
                                                  boundary the verifier must construct, and sharpening the instruments that construct
                                                  it is where this problem becomes tractable.
                                                  Keywords: agent runtime verification, verifier design, heterogeneous signal com-
                                                  position, LLM-as-judge, decidability.


                                        1    Introduction
                                        A verifier for an agent must know the limits of its own competence. Before it can check anything,
                                        something has to decide which of the rules it is asked to enforce can be settled by a fixed, interpretation-
                                        free procedure and which need a judge. The obligation “logs are retained for twenty-four months” is
                                        settled by a few lines of code; “the disclosure is adequate” is settled by no amount of code. Where
                                        the line between them falls is the decidability boundary. In a deployed agent, that decision is not
                                        made once by a designer: it recurs for every predicate of every rule on every action, a predicate being
                                        one separate condition a rule imposes, with no human in the loop. Get it wrong in one direction and
                                        the system silently automates a judgment call; get it wrong in the other, and it spends a model call to
                                        re-derive what one line of code would settle. The obvious way to make the decision is to ask a model

                                        40th Conference on Neural Information Processing Systems (NeurIPS 2026). Workshop: Who Verifies the Agents?
A    Decidability is a property of the criterion    B   Which model is the cautious one depends on the corpus

                                                                regulatory text                                   agent rules

    DECIDABLE                          JUDGMENT

                                                                                                    GPT-4o
                                                                             Llama


                                                         GPT-4o                                                          Llama




     IFEval                              MT-Bench
                 EU AI Act, FINRA,
                    agent rules                          GPT-4o’s decidable set sits                      the containment reverses:
                                                              inside Llama’s                           Llama’s now sits inside GPT-4o’s

                                                           The regions overlap but do not nest: no model is uniformly conservative.
           Clear cases sit far from the line.
          Real governing text piles up on it.


Figure 1: The geometry of the failure. A Admitting a fixed procedure is a property of the criterion
(schematic): the calibration endpoints sit far from the line, and predicates decomposed from regulatory
text pile up on it. B Measured, not schematic. On the 231 regulatory-text predicates GPT-4o calls
41 decidable against Llama’s 145, its set lying inside Llama’s on all but 2; on the 73 agent rules the
containment reverses, Llama’s 48 inside GPT-4o’s 62 on all but 1. The contested zone this leaves is
61% of our regulatory-text predicates, while the endpoints stay unanimous (κ 0.92–0.99).



which rules are checkable. This paper is about why that does not work, and why it breaks down worst
on exactly the operational rule-sets that agent systems enforce.
Using a model as a judge has become the default practice for evaluating and enforcing natural-
language criteria, in reward modeling, benchmark scoring, safety filtering, agentic guardrails and
automated policy compliance, on the implicit assumption that a capable enough model is a “good-
enough” oracle for any evaluation query. We term this the estimator-as-oracle default and argue in
§4 that it is a category error. Nearly all work on LLM judges asks whether the judge gets its answer
right. We ask a prior question: whether a model can tell which questions need a judge at all. We call
this self-decidability, and we show that models do not possess it on regulatory text, where the stakes
are arguably highest for agentic security and compliance.
Much of the value agentic systems promise is concentrated in regulated fields, where high-volume
professional judgment meets stringent compliance obligations [3], and where governing agents
inside those obligations is already an active engineering problem [22]. An agent that extends credit,
adjudicates a claim or drafts a disclosure, acts inside rules a regulator wrote; and compliance there is
a property of each action rather than of the system in aggregate: a firm cannot certify that its agent is
broadly suitable, only that this recommendation, on this account, satisfied the rule that governs it.
Every obligation reaching the agent must therefore be settled somehow, and nobody upstream has
sorted them first. In open-domain evaluation, the split is a design convenience and misclassifying
a criterion costs a slightly noisy leaderboard. Under regulation, by contrast, the predicate set is
externally imposed, so the deploying party neither chooses which obligations it faces nor gets to
rephrase the hard ones, and a misrouted judgment predicate means an unsupervised system certifies
compliance it never assessed.
On unambiguous cases, four foundation models spanning three labs agree almost perfectly on the
decidable/judgment label (κ 0.92–0.99): models can draw the line when it is clear. However, on
predicates decomposed from regulatory text, agreement collapses (κ 0.20–0.50), and the failure is
bidirectional: two models lean toward over-claiming decidability and two toward under-claiming, the
split running across labs and within one, with a model’s direction flipping by corpus. This indicates
that there is no common bias to subtract out, no reliably conservative model to pick, and no lab to
trust. The natural defense is that this is appropriate humility on a hard boundary, but the labels are
confident rather than hedged, opposed rather than converging, localised to the operationally critical
middle, and systematically unstable under meaning-preserving paraphrase of the same predicate (§6).
A system can be humble about hard answers while remaining reliable about which questions are hard;
conflating the two is fatal.


                                                            2
This matters because in industry today, the standard remedy for an unreliable judge is to simply
escalate the hard cases [18, 27, 6]. Every such remedy presupposes that the escalation decision itself
is reliable. In this paper, we show that this presupposition does not hold, and the error is directional
in the way that is systematically injurious: an over-claimed predicate is never escalated, so the
mitigation is silently switched off exactly where it was needed. Whether that decision is reliable
is a precondition for every escalation-based remedy, and to our knowledge no one has measured it
heretofore.
The decidability boundary therefore has to be established without trusting any single model’s answer
(Fig. 1, §8). What we build instead, C OV ER (COrroborate-then-VERify predicate routing), has two
parts. First, we ask several independent models and keep only the rules they all call checkable. That
agreement is a cheap filter and a revealing one: it is 97–99% precise where the models err in different
directions, and only 83% on the agent’s own rules, where they err together. Filtering alone therefore
cannot carry the guarantee. So, second, do not trust the label at all: write the check the rule implies
and admit the rule only if that check survives intervention, reading fields the agent cannot write,
moving when we intervene on them, and holding when the record is deterministically reworded. We
built the more obvious second stage first, agreement with a reference judge, and §8.2 shows why it
cannot work. Correctness then rests on a check that was executed rather than a label that was asserted.
In total, we provide the following contributions:
1. The problem, named and located. We identify self-decidability, whether a model can tell which
   of the criteria it is given a fixed check can settle and which need a judge, as the routing decision
   every agent verifier makes before it checks anything. It is prior to the accuracy question the
   LLM-as-judge literature studies, and every escalation-based remedy silently assumes it has been
   solved – it has not.
2. C OV ER, a corroborate-then-verify procedure that keeps the model’s answer off the critical path.
   Agreement across independent models only nominates a rule; admitting it requires a test the panel
   does not control. We show that the obvious such test, agreement with a reference judge, measures
   whether a check is reproducible rather than whether a predicate is decidable, and we replace it
   with an interventional gate that consults no estimator: the check must read fields the agent cannot
   write, respond to intervention on them, and hold under deterministic rewording of the record.
3. The measurements. 832 predicates from six corpora, each labelled by four foundation models
   across three labs under four rubric variants and two perturbation instruments: roughly 22,000
   model calls. Agreement is near-perfect on unambiguous cases and collapses on regulatory text;
   the error is bidirectional, model-specific, cross-lab and domain-specific; the contested zone is the
   central mass of regulatory text rather than a tail; and a pre-registered ablation shows that a far
   more prescriptive rubric buys agreement without buying correctness.


2   Related Work

This is not another study of LLM-as-judge unreliability; surveys already document judges that are
noisy, position- and verbosity-biased and domain-sensitive [10, 17]. A more layered reading holds
that these predicates are simply ambiguous and that human annotators would disagree too [21]; we
answer it in Appendix E.
Decidable-vs-subjective evaluation design. Closest to us is Zhou and Shbita’s Evaluating Ill-Defined
Tasks in Large Language Models [31], which characterises ill-defined tasks as those no fixed standard
settles and routes decidable properties to rule-based checks, subjective ones to a judge. We share the
distinction and differ on who draws the line, and where: theirs is a guideline applied by hand, per
benchmark, at construction time, while we study the regime with no designer in the loop, where the
line falls to runtime and that automation is what fails. Where they use two judges to reduce noise
within the subjective region, we use corroboration to locate the boundary, and then verify it.
A generic unreliability account makes three predictions, and the sections that follow falsify all
three. It predicts broad degradation, where we measure agreement at κ 0.92–0.99 on the endpoints,
collapsing only in the consequential middle. It predicts undirected error, where we find the bias
anti-correlated across models on regulation and correlated on agent rules, and noise produces neither.
And if the disagreement were underspecification, specifying the task should move the panel toward
truth, whereas a decision procedure with worked examples moves it to 57.7% accuracy against 88.8%
unprompted (§7).


                                                   3
3     The Setting: Runtime Verification of Agent Actions
A single holistic evaluation, “is this whole response good?”, can absorb a fuzzy estimator: one query,
one judgment, and errors that wash out in aggregate scoring. By contrast, agentic deployment presents
a very different error surface. An agent takes many actions per task, each is checked against the rules
that apply, each rule breaks into predicates, and every predicate forces the same choice: (i) settle it
with code, or (ii) spend a call on a judge. There is no third option, since a predicate nobody routes
is still routed, by default, into one of the two. The multiplicities are large: RegData counts over a
million binding restrictions in the US Code of Federal Regulations, marked by shall and must [1],
and one firm’s subset runs to thousands. At that scale an executed check costs microseconds, where a
judge costs seconds and tokens.
Critically, the two defaults cost different things (Figure 5, Appendix F). Take a firm required to
disclose material conflicts of interest within three business days. Whether a conflict is material is a
judgment call, and sending it to code clears every disclosure that mentions a conflict at all, certifying
compliance no one assessed. Whether it went out in three days is arithmetic on two timestamps, and
sending it to a judge pays a model call to compare two dates. We call the first error over-claiming
and the second under-claiming: over-claiming costs a missed violation, silent and repeated across a
fleet, while under-claiming costs an extraneous inference one call at a time, which is how a year’s
inference budget disappears in four months [19].
We show that no deployment escapes both errors by simply choosing a model, since the bias runs
in opposite directions in different models (§6): whichever minimises missed violations maximises
the bill. Nor do the errors merely add up. A rule passes only if all of its predicates are handled
correctly together, so the chance every routing call is right degrades geometrically as rules lengthen.
Appendix F gives the cost model.

4     The Decidability Axis, and Why Routing Needs Type
4.1    The boundary is not ours

Prior work in four fields independently discovered this decidability boundary in different guises,
which is the best evidence available that it is a real seam in the criteria themselves rather than
an artifact of our framing. Law separates rules, whose content is fixed before anyone acts, from
standards, which acquire content only once conduct is judged, and Kaplow’s tradeoff is the one we
measure [16, 11]; psychology separates actuarial from clinical prediction [5]; psychiatry tried to
move criteria across the line by writing more specific ones and bought agreement without validity,
the outcome we reproduce in §7 [23]; and reinforcement learning trains against tasks a program can
check [13]. The nearest thing to a shared name for the distinction is Simon’s between well-structured
and ill-structured problems [24].
What they share is that somebody drew the line in advance, offline, once, by people with time and
resources to adjudicate. Modern agentic deployment silently removes that assumption: an agent
enforcing regulation it did not author meets predicates nobody has pre-sorted, at a rate no designer
can service. The boundary is therefore old; having to draw it at runtime, without ground truth and
without a person in the loop, is new.
The estimator-as-oracle default. An LLM judge is a stochastic estimator, not an oracle, and the
criteria it is pointed at are non-homogeneous. Some are decidable: a fixed, interpretation-free
procedure over stated facts returns the exact answer, whether a parser, a format or count check, a
lookup, or an exact match. Others require judgment, turning on interpretation, degree or value, where
estimation is the best available tool.1 Pointing one instrument at both wastes it where a check would
suffice and over-trusts it where verification is required. The distinction is not about difficulty: a
decidable predicate can be tedious to check, and a judgment predicate can be obvious to any person
who reads it.
Type – not the verdict – is what routing needs. Two questions can be asked about any criterion: (i)
What is the verdict here? is instance-specific and legitimately uncertain in hard cases; (ii) What kind
of criterion is this? asks whether settling it needs interpretation or only a check, and is a property of
    1We use “decidable” by analogy with computability, not as a formal claim: a judgment criterion is not formally adjudicable

or is underspecified, not Turing-undecidable.


                                                              4
                           predicates from regulatory text                                                                          operational agent rules


    sonnet                       12%              22%                                              sonnet                                 8%                       62%

     opus                  54%                     6%                                                 opus                             12%             29%

    gpt4o          74%                            1%                                                 gpt4o                                8%                         71%

llama70b                               24%              37%                                       llama70b                                  24%              46%


             75%         50%     25%         0%         25%     50%        75%                                   75%        50%       25%         0%     25%       50%     75%

                                              ← under-claim (wasteful): a check sent to a judge     over-claim (unsafe): a judgment automated →


Figure 2: There is no conservative model to pick. On regulatory text (left) GPT-4o is the panel’s
most cautious model, calling 1% of judgment predicates decidable; on an operational agent rule-set
(right) the same model is the most reckless, at 71%. Every model shifts toward over-claiming on
agent rules, the unsafe direction, and that is the setting in which a runtime verifier acts on the label
without escalation. Denominators differ: over-claim over the true-judgment predicates (78 regulatory
text, 24 agent rules), under-claim over the true-decidable ones (153 and 49).


the criterion, not the case. The latter question is what a routing system has to answer, which makes
type what a verifier must be able to report. As we show, models turn out to be unreliable even about
this (§E.2), which is why the architecture of §8 never depends on what they report.

5     Experimental Setup
Our experiments ask one question repeatedly: shown a single predicate, can a model say which side
of the decidability boundary it falls on? The corpora bracket that boundary, so a failure in the middle
is attributable to the boundary rather than to the task. Protocol. We ask each model, per predicate, a
single blind classification against a fixed rubric, decidable = a fixed procedure over explicitly-stated
facts returns the exact answer with no interpretation, degree-weighing, or value judgment; otherwise
judgment, at temperature 0 with no hedging permitted.
Scope. The measurements rest on 832 distinct predicates from six corpora, each labelled indepen-
dently by four foundation models spanning three labs, under four rubric variants and two perturbation
instruments: approximately 22,000 model calls. Every figure and table below is computed directly
from those label files.
Corpora and models. The four models are Claude Sonnet and Claude Opus [2], GPT-4o [20] and
Llama-3.1-70B [9], all labelling every target; the cross-lab span is what lets the model-specificity
claim rest on three cross-lab pairs. Calibration endpoints, where the label is uncontested, are
IFEval [29] at the decidable pole and MT-Bench [28] at the judgment one. The borderline is policy:
predicates decomposed from the EU AI Act [7] and FINRA [8], regulatory text throughout, and from
an operational AI-agent rule-set, with a gold-labelled synthetic corpus as a control. Predicates were
decomposed from rule text by an LLM under a fixed schema, blind to the labelling studied here;
context-stripping would push the panel toward JUDGMENT together, not into the bidirectional split
we observe. Ground truth on the real corpora is an LLM-assigned proxy (§9). Full protocol, metric
definitions and model versions are in Appendix C.

6     Results
Models can draw the line when it is clear. On the calibration endpoints, IFEval and MT-Bench,
all four models agree near-perfectly (κ 0.92–0.99) with over- and under-claim near zero, the one
exception being Opus over-claiming 10% on clear judgment.
The boundary collapses on regulatory text. Across the 231 predicates of regulatory text, agreement
falls to κ 0.20–0.50 under our rubric,2 and the error is bidirectional, model-specific and cross-lab:
    2 All κ figures are measured under the single fixed rubric of §5. A far more prescriptive rubric raises regulatory-text κ to

0.55–0.69, and §7 shows the extra agreement does not track ground truth; κ is therefore not the rubric-invariant quantity here,
and the precision of the unanimous set is. These marginals are also imbalanced, which depresses κ by construction: four of six
pairs reach 78–100% of the κ attainable at their own base rates. The models agree about as often as those rates permit; what
differs is where each draws the line.


                                                                                        5
Llama (37%) and Sonnet (22%) lean toward over-claiming while GPT-4o (74%) and Opus (54%) lean
toward under-claiming, the split running within Anthropic and across labs, with the most opposed
pair agreeing at only κ 0.20. The lean is domain-specific too: on the operational agent rule-set every
model flips to over-claiming (GPT-4o 71%, Sonnet 62%, Llama 46%, Opus 29%; κ 0.38–0.64), so
GPT-4o, the heaviest under-claimer on statutes, becomes the heaviest over-claimer on agent rules.
A reasoning-era model added after these measurements extends the split rather than repairing it,
over-claiming 41% on regulatory text and 92% on agent rules: the most permissive member of any
panel we ran (Appendix C.3). The flip is consequential: agent obligations read mechanical, their
conditions naming fields like customer_consent_logged, so models over-claim exactly where a
system would auto-enforce.3
The contested zone is the central mass of regulatory text. Measured ground-truth-free as the cross-
model disagreement rate, the borderline covers 65% of EU AI Act predicates, 52% of FINRA and
33% of agent rules, against 23% synthetic. The rate rises monotonically with panel size (Table 4), so
these are lower bounds.
The disagreement is a bug, not humility. Genuine ambiguity predicts convergent hedging, spread
evenly across the corpus and stable under rewording. We observe the opposite on each count. The
labels are opposed across models rather than converging, localised to the operationally critical middle
while the endpoints stay unanimous, and unstable within a single model: under a loophole-free
deterministic-template perturbation (§E.2) Opus flips its own borderline label 33% of the time against
5% on controls, and GPT-4o 44% against 7%. The last of these is instrument- and model-dependent,
which we report as such, but every model destabilises under at least one perturbation. None of this
depends on our proxy labels: on 53 FINRA rules a human annotator sorted blind, agreement is again
κ 0.34–0.48, with GPT-4o again the most conservative member (§C.2).
Corroboration recovers a high-precision core, and its failure mode is instructive. Unanimous
agreement yields a decidable set at 99.2% precision on gold-labelled synthetic data and 97.0% on
regulatory text, but on the agentic corpus, where all four over-claim together, it falls to 83%. That
gap is the argument for §8.


7    Is the Boundary Just Our Rubric? A Specification Ablation

The obvious objection is that we measured ambiguity in our prompt rather than unreliability in the
models, so we red-teamed our own harness with two orthogonal manipulations of the published
rubric, holding corpus, models and decoding fixed. R-proc restates the same criterion procedurally
rather than definitionally, isolating surface form; R-spec adds a decision procedure, boundary rules
and worked examples, isolating underspecification. We pre-committed to the bar that a fall of more
than 5 pp in contested rate on a real corpus would support the objection. Appendix D gives the design,
table and pre-registration; four findings follow.
Surface form does not move the boundary. Under R-proc, the contested rate is flat on every corpus
while individual models flip 6.6–16.3% of their own labels in no consistent direction (Appendix D).
Specification does move it, and our bar is crossed: the contested rate falls 30.9 pp on the EU AI Act
and 19.6 pp on FINRA. But the agreement it buys does not track truth. Of the 71 regulatory-text
predicates R-spec converts from contested to unanimous, the manufactured consensus is correct
57.7% of the time (Wilson 95%: 46.2–68.5) against 88.8% (80.5–93.8) for consensus that formed
unprompted, and the intervals do not overlap. That pits a hard subset against an easy one, so we also
compare like for like: on those same 71 predicates the unprompted panel’s own majority vote is right
49.3% of the time, so specification does improve accuracy where it acts. What it does not do is beat a
constant. The converted set is 74.6% decidable, so a router that always said DECIDABLE would score
74.6%, above R-spec and level with R-spec′ . Twenty-nine of R-spec’s 30 errors are under-claims: it
does not resolve the boundary, it withdraws from it. Appendix D works one such predicate through in
full.

    3 Proxy caveat: ground truth here is the rule-set’s grading_method, and the 20 “both” rules count as judgment, which

inflates absolute over-claim. We checked rather than assumed: recounting “both” as decidable leaves only four true-judgment
predicates, and on those GPT-4o is still the heaviest over-claimer (75%) and Opus the lightest (25%). The ordering and the flip
survive; the magnitudes rest on the “both” convention. κ needs no ground truth and is unaffected.


                                                              6
Table 1: The same routing question on both corpora. Left: no single model is trustworthy in both
directions, and the precise ones are precise by escalating most of the work; unanimity reaches the
high-precision corner without knowing which model is biased. Right: where the models err together
that precision collapses. Precision is against gold (syn.) and proxy labels; coverage is the share
of true-decidable predicates recovered; false-decidables are gating-attributable; the agent corpus is
67.1% decidable.
                regulatory text (n = 231)                           agent rules (n = 73)
       Router             Syn.    Proxy     Cov.
                                                         Router           Elim.    False-dec.   Prec.
       Sonnet            93.6%    88.8%     88.2%
       Opus              96.8%    93.3%     45.8%        Judge everything   0.0%       0           –
       GPT-4o            99.2%    97.6%     26.1%        Majority (≥3/4)   72.6%       9        83.0%
       Llama-3.1         86.4%    80.0%     75.8%        Unanimous (4)     56.2%       7        82.9%
       Majority (≥2/3)   98.0%    93.7%     48.4%        Intervention gate 27.4%       3        85.0%
       Unanimous (4)     99.2%    97.0%     20.9%



And on operational agent rules it buys nothing (33% → 33%, with half the membership churning
underneath).
Finally, which predicates it settles is an authoring accident. R-spec′ , identical to R-spec but for
eight different and equally correct worked examples, resolves a different third of the predicates
(Jaccard 63.3%) and is 75.9% accurate against R-spec’s 57.7% (z = 2.16, p = 0.031): the benefit of
specification is a lottery over an authoring choice the rubric does not record.
Specification is therefore a genuine lever on regulatory text but not on agent rules, and where it works
it suppresses disagreement rather than resolving it, moving the panel toward each other and away
from the answer. Contested rate is rubric-dependent; the precision of the unanimous set is not, and
that is what grounds §8.

8     Corroboration Nominates, Intervention Tests, Neither Certifies
Because no single model can be trusted to say whether a criterion admits a fixed procedure, we draw
the boundary outside any one estimator, in two layers: corroboration gives a high-precision candidate
set cheaply, and verification audits that set with a test the panel does not control. Threat model. We
assume an agent that may be misaligned but is not attacking its verifier: predicates reach the router
from a governance process rather than an adversary, and the fields a check reads are trusted in the
restricted sense set out below. Adversarial authorship of the predicates themselves is out of scope
(Appendix E).

8.1   Corroboration as a model-agnostic safety floor

We keep only the predicates all four models independently call decidable (Table 1).
The unanimous gate lands at the high-precision corner regardless of which model is biased, bounding
the safety-critical false-decidable rate to 1–3%. It is also robust to panel membership, because the
binding constraint is the most conservative member. We stated that prediction before testing it: adding
a reasoning-era fifth member, which calls more regulatory predicates decidable than any model here,
leaves the unanimous set identical on both corpora (Appendix C.3).
A skeptic will read the table as saying unanimity roughly equals the best single model, and ask
why not use that one. Which model is safe is domain-specific and not predictable in advance: “just
use GPT-4o” presumes you know it is conservative on this corpus, and on agent rules it is the
heaviest over-claimer of the four. And precision is paid for in coverage whichever way it is bought:
GPT-4o routes three-quarters of the genuinely decidable to a judge and unanimity inherits that cost,
reproducing the cost failure of §3.
And that precision is conditional on bias independence. The 97–99% figure holds only because the
biases on regulation run in opposite directions. Where models share a directional bias the panel
agrees and is jointly wrong: on agent rules unanimous-DECIDABLE precision falls to 83% at 69%
coverage. Corroboration is a cheap filter, necessary but insufficient (§8.3).


                                                    7
                     CORROBORATE                                         VERIFY BY INTERVENTION
                                                                                        G0 not an identity
      predicate p              model panel M         S YNTHESIZE                        G1 slots are attested         admit
      “retention ≥                 all four call p   slot retention_months              G2 verdict moves            c enforces p
       24 months”                   DECIDABLE ?      rule retention_months >= 24        G3 stable under rewording

                                   not                                                                  any gate
                             unanimous                                                                  fails
                                                         escalate: p is judged


Figure 3: C OV ER end to end (Algorithm 1). Corroboration only nominates: a predicate the panel
does not unanimously call decidable leaves at once. A nominated predicate is admitted only if the
check synthesized for it clears all four gates. Both ways the router can err lead out along the same
dashed rail, so the gate fails closed, and no model is consulted after nomination.


8.2      The obvious second layer, and why it fails

Since no panel can audit its own blind spot, the natural next move is to stop trusting the label and
test it. We synthesize the check a predicate implies, run it against a reference judge on cases held
out from the check’s construction, and admit the predicate only when the two agree on at least a
τ fraction of them. We ran that gate over EU AI Act predicates, using probe cases and reference
verdicts collected before this study. We report it because the way it fails motivates what we adopt
instead (Table 2, Appendix A).
At τ = 1, the gate admits 43/173 predicates at 79.1% precision, which reads respectably until we ask
where it comes from. Thirty-eight of the 173 have a reference verdict that never varies, and the gate
takes 16 of them, scoring 100.0% there against 66.7% (Wilson 95%: 47.8–81.4) on the 27 varying
predicates it admits: a lift of 4.4 points over their 62.2% base rate, with an interval that contains it.
What looked like discrimination is composition.
The diagnostic underneath is sharper. Calibration agreement predicts held-out agreement almost
perfectly, rising monotonically from 29.6% to 76.7% across the four buckets, so the gate measures
something real. It is not measuring decidability: across those same buckets the true-decidable
rate runs 55.6, 75.0, 62.8, 62.3 and 79.1% and moves nowhere. We had built an instrument for
reproducibility and read it as though it reported checkability.
The cause is structural, and it is the failure of §6 one level up: the reference judge is drawn from the
same population of estimators as the panel, so wherever the panel shares a blind spot the judge shares
it, and a check that reproduces the judge reproduces the blind spot. Agreement with an estimator
cannot certify the absence of estimation. No threshold repairs this, because τ governs only how
faithfully the check tracks the judge, and tracking the judge is the wrong target.


8.3      Verification by intervention: C OV ER’s second stage

Every failure we have measured is a failure of self-report: models disagree about what kind of
criterion they face, disagree in opposite directions, contradict themselves under rewording, and a
judge drawn from the same population inherits all of it. C OV ER’s second stage therefore asks the
models nothing further, admitting a predicate on the behaviour of the synthesized check rather than
on any estimator’s report of it.
What S YNTHESIZE emits. A predicate becomes two artifacts (Fig. 3): named fact-slots read off the
action record, and a decision rule over them. A model fills the slots and code evaluates the rule. Only
attested fields are admissible, those infrastructure produces and the agent cannot write: a check over a
field the agent asserts establishes only that the agent agreed with itself, so a predicate needing one is
escalated whatever the panel said. That distinction does its sharpest work where corroboration is most
confidently wrong. An agent rule such as “MUST NOT set customer_consent_logged=True
without explicit consent” reads mechanical because its field name does: it looks like a column, so
the check looks like a lookup. But the agent writes that field, so a check reading it would certify
the agent’s own account of its compliance, and C OV ER refuses the predicate corroboration most
readily admits. If a record lacks a field the check needs, or the check raises an exception when it runs,
C OV ER escalates the predicate rather than admitting it. The gate fails closed, so a broken check costs
a judge call and never a missed violation.


                                                                  8
Four gates, three inherited from the failures above. Structure rejects an identity that hands the
predicate straight back to the extractor: the check-level form of the surface-mechanical reading that
makes every model over-claim on agent rules. Groundedness is the check-level form of specification
that adds words without adding truth (§7). Invariance turns the perturbation instrument of §E.2 on the
check rather than the label. Sensitivity is a degeneracy guard rather than a consequence of anything
we measured, and we report it as such.
Protocol. We evaluate on the agent rule-set, where corroboration fails, running its 73 predicates
against 36 synthetic action records (Appendix A).
The gate carries real signal, and not enough of it. Tightening invariance from half to full agreement
lifts precision from 66.7% to 85.0% against a 67.1% base rate, so requiring a check to survive
rewording does select better predicates. On safety it does better than that column suggests: of
the seven false-decidables that survive unanimity the gate rejects five, admitting 6.7 predicates per
false-decidable against unanimity’s 5.9. The operating point is chosen on a seeded half and confirmed
on the other: there the gate admits 10 predicates at 90.0% precision with one false-decidable, against
unanimity’s 19 at 89.5% with two. What it does not do is clear our bar of beating unanimity’s
precision at comparable elimination, since it removes 27.4% of judge calls where unanimity removes
56.2%.
We can say why. Our invariance test asks whether the extractor returns the same value when one
record is rewrapped in neutral framing, never whether a slot means the same thing across records
where the evidence is explicit and records where it is oblique. The gradient is a property between
records and the gate a statistic within one, so it never reaches the gate. The instrument this calls for
measures consistency across independent attempts rather than invariance under paraphrase. We built it.
Sampling each extraction five times and scoring a predicate by its least stable read separates decidable
from judgment at chance (AUC 0.42–0.48 on the 20 predicates that reached it, at every level from
verdict to individual slot), and the median predicate of both classes is perfectly self-consistent. not
agent_gave_restructuring_advice reads identically every time: the extractor is not uncertain
about the judgment it makes, it makes the same one. An estimator’s agreement with itself certifies no
more than its agreement with a judge.
What intervention cannot do. A check can be grounded, sensitive and invariant while verifying only
part of what its predicate asks: one agent obligation carries three deontic clauses and its rule covers
one. Establishing faithfulness would mean putting a judge back in. Each layer has one thing it cannot
check: corroboration cannot certify itself, agreement cannot certify mechanicality, and intervention
cannot certify faithfulness.


9   Limitations and Conclusion

Limitations. Our agentic corpus is narrow: 73 predicates over 20 rule families from one deployed
credit agent, with the over-claim rates resting on its 24 true-judgment predicates, so Wilson 95%
intervals run roughly 35 pp wide. The direction is robust, not the magnitudes: every model shifts
toward over-claiming, the largest shifts far outside sampling noise. Ground truth on the regulatory
corpora is also an LLM-assigned proxy, mitigated by leading on the ground-truth-free disagreement
metric and by replicating against 53 blind human labels (§C.2). Third, the interventional evaluation
rests on 36 synthetic action records of our own construction, and its self-consistency null on the 20
predicates that reached that gate. Appendix E states six further limitations.
Conclusion. Pointing a single LLM judge at every evaluation treats a stochastic estimator as an
oracle, and using one well means knowing which criteria need it. That is what models cannot supply:
they agree where the answer is obvious and err together where it matters, and no better judge repairs it,
because the judge is what is being routed to. A verifier must know its own scope, and that knowledge
is established by execution, not by asking again. That requirement is sharpest under externally written
rules: the EU AI Act, FINRA guidance, a bank’s credit policy. There the routing error is silent,
potentially catastrophic, and runs in the direction nobody escalates, and does not dissolve with scale,
since the reasoning-era model we added widened the split rather than closing it. In regulated domains,
where agentic systems carry the highest upside and the lowest tolerance for error, the boundary of
what a verifier can check must be settled in advance, not re-derived at every action from a model’s
account of its own competence.


                                                   9
Acknowledgments and Disclosure of Funding
The author thanks colleagues at Confidential Core AI for discussions and for feedback on drafts, and
the anonymous reviewers of the Who Verifies the Agents? workshop for comments that improved the
paper. This work received no external funding. Large language models assisted with the drafting and
editing of text; the author designed the method, ran all experiments and verified every numeric claim
against the underlying run data.

References
 [1] Omar Al-Ubaydli and Patrick A. McLaughlin. RegData: A numerical database on industry-
     specific regulations for all united states industries and federal regulations, 1997–2012. Regula-
     tion & Governance, 11(1):109–123, 2017.
 [2] Anthropic. The Claude model family. https://www.anthropic.com/research/claude-
     model-spec, 2025.
 [3] Zhiyu Zoey Chen, Jing Ma, Xinlu Zhang, Nan Hao, An Yan, Armineh Nourbakhsh, Xianjun
     Yang, Julian McAuley, Linda Petzold, and William Yang Wang. A survey on large language
     models for critical societal domains: Finance, healthcare, and law. Transactions on Machine
     Learning Research, 2024. arXiv:2405.01769.
 [4] Jacob Cohen. A coefficient of agreement for nominal scales. Educational and Psychological
     Measurement, 20(1):37–46, 1960.
 [5] Robyn M. Dawes, David Faust, and Paul E. Meehl. Clinical versus actuarial judgment. Science,
     243(4899):1668–1674, 1989.
 [6] Haotian Deng, Chris Farber, Jiyoon Lee, and David Tang. Rubric-conditioned LLM grading:
     Alignment, uncertainty, and robustness, 2026.
 [7] European Parliament and Council of the European Union. Regulation (EU) 2024/1689 of
     the European Parliament and of the Council – Artificial Intelligence Act. https://eur-
     lex.europa.eu/eli/reg/2024/1689/oj, 2024.
 [8] Financial Industry Regulatory Authority. Artificial intelligence (AI) in the securities industry.
     Technical report, FINRA, 2024. Regulatory Notice 24-09.
 [9] Aaron Grattafiori et al. The Llama 3 herd of models. arXiv preprint arXiv:2407.21783, 2024.
[10] Jiawei Gu, Xuhui Jiang, Zhichao Shi, Hexiang Tan, Xuehao Zhai, Chengjin Xu, Wei Li, Yinghan
     Shen, Shengjie Ma, Honghao Liu, Saizhuo Wang, Kun Zhang, Yuanzhuo Wang, Wen Gao,
     Lionel Ni, and Jian Guo. A survey on LLM-as-a-judge, 2024.
[11] H. L. A. Hart. The Concept of Law. Oxford University Press, Oxford, 1961.
[12] Tzu-Heng Huang, Harit Vishwakarma, and Frederic Sala. Time to impeach LLM-as-a-judge:
     Programs are the future of evaluation, 2025.
[13] Ruipeng Jia, Yunyi Yang, Yongbo Gai, Kai Luo, Shihao Huang, Jianhe Lin, Xiaoxi Jiang,
     and Guanjun Jiang. Writing-zero: Bridge the gap between non-verifiable tasks and verifiable
     rewards, 2025.
[14] Saurav Kadavath et al. Language models (mostly) know what they know, 2022.
[15] Daniel Kahneman, Olivier Sibony, and Cass R. Sunstein. Noise: A Flaw in Human Judgment.
     Little, Brown Spark, 2021.
[16] Louis Kaplow. Rules versus standards: An economic analysis. Duke Law Journal, 42(3):557–
     629, 1992.
[17] Haitao Li, Qian Dong, Junjie Chen, Huixue Su, Yujia Zhou, Qingyao Ai, Ziyi Ye, and Yiqun
     Liu. LLMs-as-judges: A comprehensive survey on LLM-based evaluation methods, 2024.


                                                 10
[18] Yasmin Moslem and John D. Kelleher. Dynamic model routing and cascading for efficient LLM
     inference: A survey, 2026.
[19] Janakiram MSV. Uber burns its 2026 AI budget in four months on Claude code. Forbes, May
     2026.    https://www.forbes.com/sites/janakirammsv/2026/05/17/uber-burns-
     its-2026-ai-budget-in-four-months-on-claude-code/, accessed 2026-08-20.
[20] OpenAI. GPT-4o system card. OpenAI Technical Report, 2024.
[21] Ellie Pavlick and Tom Kwiatkowski. Inherent disagreements in human textual inferences.
     Transactions of the Association for Computational Linguistics, 7:677–694, 2019.
[22] Shaina Raza, Ranjan Sapkota, Manoj Karkee, and Christos Emmanouilidis. TRiSM for agentic
     AI: A review of trust, risk, and security management in LLM-based agentic multi-agent systems.
     arXiv preprint arXiv:2506.04133, 2025.
[23] Darrel A. Regier, William E. Narrow, Diana E. Clarke, Helena C. Kraemer, S. Janet Kuramoto,
     Emily A. Kuhl, and David J. Kupfer. DSM-5 field trials in the United States and Canada, part
     II: Test-retest reliability of selected categorical diagnoses. American Journal of Psychiatry,
     170(1):59–70, 2013.
[24] Herbert A. Simon. The structure of ill structured problems. Artificial Intelligence, 4(3–4):181–
     201, 1973.
[25] Haoyu Wang, Christopher M. Poskitt, and Jun Sun. AgentSpec: Customizable runtime enforce-
     ment for safe and reliable LLM agents. arXiv preprint arXiv:2503.18666, 2025. To appear,
     ICSE 2026.
[26] Jason Z. Wang. MIRROR: A hierarchical benchmark for metacognitive calibration in large
     language models, 2026.
[27] Michael J. Zellinger, Rex Liu, and Matt Thomson. Cost-saving LLM cascades with early
     abstention, 2025.
[28] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang,
     Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al. Judging LLM-as-a-judge with MT-Bench
     and chatbot arena. Advances in Neural Information Processing Systems, 36, 2023.
[29] Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha Brahma, Sujoy Basu, Yi Luan, Denny
     Zhou, and Le Hou. Instruction-following evaluation for large language models, 2023.
[30] Jiayi Zhou, Yang Sheng, Hantao Lou, Yaodong Yang, and Jie Fu. FormalJudge: A neuro-
     symbolic paradigm for agentic oversight, 2026.
[31] Yi Zhou and Basel Shbita. Evaluating ill-defined tasks in large language models, 2026.




                                                 11
A     The C OV ER Procedure
Algorithm 1 states the procedure in full; the gates it applies are those of §8.3.

Algorithm 1 C OV ER: corroborate-then-verify predicate routing. Corroboration orders the synthesis
budget rather than capping it: unanimous nominations are attempted first, and a predicate the panel
did not nominate can still be admitted if its check clears the gates. No estimator’s opinion enters lines
5–10.
Require: predicates P ; model panel M ; action records Dp for each p; deterministic rewording
    operator ρ; grounding threshold θG ; invariance threshold θI
Ensure: auto-enforced set A of (predicate, check) pairs, and escalated set E
 1: A ← ∅; E ← ∅
 2: U ← { p ∈ P : { m(p) : m ∈ M } = { DECIDABLE} } ▷ unanimous nominations: cheap, and
    not a verdict
 3: for each predicate p ∈ U , then each p ∈ P \ U while budget remains do
 4:     c ← S YNTHESIZE(p)                     ▷ bounded check: comparison, lookup, format or count
 5:     if c reduces to an identity on one slot then
 6:          E ← E ∪ {p}; continue                                                        ▷ G0: structure
 7:     end if
 8:     g ← fraction of c’s slots readable from the attested fieldsof Dp           ▷ G1: groundedness
 9:     s ← ∃ slot σ, x ∈ Dp , value σ ′ : c(x) ̸= c(x | σ ← σ ′ )                       ▷ G2: sensitivity
10:     v ← { x ∈ Dp : c(x) = c(ρ(x)) } / |Dp |                                         ▷ G3: invariance
11:     if g ≥ θG and s and v ≥ θI then
12:          A ← A ∪ {(p, c)}                                     ▷ c replaces the judge for p at runtime
13:     else
14:          E ← E ∪ {p}                                                      ▷ p is judged, permanently
15:     end if
16: end for
17: every p never attempted joins E                                 ▷ unattempted predicates are judged
18: return A, E




Table 2: The agreement gate on the EU AI Act corpus, against the label routers. Label rows use all
175 labelled predicates, graduation rows the 173 the gate ran on. Held is agreement with the reference
judge on held-out cases, which a label router cannot report because a label is not executable.
                     Router                     Admitted     Prec.    Cov.     Held
                     Majority (≥3 of 4)             56      92.9% 44.4%   –
                     Unanimous (4)                  24       95.8% 19.7%  –
                     Graduated (τ = 1)              43      79.1% 29.3% 76.7%
                     Unanimous and graduated         7      100.0% 6.0% 76.2%


A.1   Protocol for the interventional evaluation

Protocol. We evaluate on the agent rule-set, where corroboration fails because the models err together.
The 73 predicates run against 36 synthetic action records, each carrying a full session: tool-call log,
session fields and conversation. Every judgment-bearing phenomenon appears in clear, ambiguous
and absent form, so a slot that can only be filled by weighing has somewhere to come apart, and
the records state evidence but never a verdict. One record is shown to S YNTHESIZE as a schema
exemplar and withheld from every gate. Because we inspected this corpus while building the harness,
we fix a seeded split and report on the half that plays no part in choosing the operating point.
The self-consistency instrument, in full. §8.3 diagnoses our invariance gate as a statistic within
a record where the difficulty gradient is a property between records, so we built the instrument
that diagnosis calls for and report it here because it fails. For each predicate we re-extract every
slot K = 5 times independently at temperature 1.0 on a fixed prefix of 12 records, and score each
record by the share of attempts agreeing with the modal read. The record set is bounded deliberately:
a worst-case-over-records statistic on an unbounded set rejects everything, because any predicate


                                                   12
eventually meets one flaky read. We reduced these measurements ten ways: at the verdict, at the
full slot tuple and per individual slot, each under worst-case, second-worst, first-quartile and mean.
No aggregation choice can be blamed for the outcome, because every one separates true-decidable
from true-judgment predicates at chance (AUC 0.42–0.48; 13 decidable and 7 judgment predicates
reached the gate), and 9 of 13 decidable and 5 of 7 judgment predicates score perfect self-consistency.
Two caveats bound this. The predicates that reached the gate are not a random sample of the corpus,
so the estimate is a bounded check rather than a corpus-wide measurement; and constrained JSON
extraction may simply be near-deterministic at any temperature, in which case the instrument is inert
rather than the hypothesis false. Neither caveat touches the mechanism the result illustrates: not
agent_gave_restructuring_advice delegates an entire judgment to the extractor and is read
back identically on every record, because a model that is confidently wrong is indistinguishable, to
any reproducibility test, from one that is right.


B    Perturbation Instruments for the Stability Test

The remaining feature-reading prediction is internal consistency: even if models differ from each
other, a single model should draw the same decidability line for a given predicate regardless of trivial
surface wording, its line would be principled, just personal. We test this directly. For each contested
predicate we generate K neutral, meaning-preserving paraphrases, validate each is semantically
equivalent to the original (an independent equivalence check, so we cannot be accused of adversarial
rewording), and re-probe each model. We measure each model’s flip rate: the fraction of predicates
on which it contradicts itself across paraphrases. As a control we run the same protocol on the
unanimous-clear predicates.
• Bug prediction: high flip rate on the borderline, ≈ 0 on the clear control, the instability is localized
  to exactly where the routing decision matters.
• Feature prediction: low flip rate everywhere (internal consistency).
Result (two independent perturbation instruments). We test internal consistency two ways:
an LLM paraphrase instrument (Haiku paraphraser + Haiku equivalence gate, both outside the
judge set; 134 borderline / 48 control parents) and a deterministic template instrument (neutral
surface wrappers, no LLM in the loop, closing any “the paraphraser drifted it / rubber-stamped it”
objection; 172 borderline / 60 control). Borderline flip = the model contradicts its own label across
meaning-preserving variants.
Three honest reads, stated plainly:
• The effect is real and, on the loophole-free instrument, large. Opus (33% vs 5%) and GPT-4o
  (44% vs 7%) flip their own borderline label far above their clean-case baseline under purely
  deterministic reframing, with no LLM authoring or approving the variants. GPT-4o, nearly stable
  under paraphrase, is the most unstable under templates: its apparent paraphrase-stability was an
  artifact of its near-constant-JUDGMENT under-claim bias, which the template wrappers break.
• It is instrument- and model-dependent, and we do not hide that. No single model destabilizes on
  every perturbation type: Sonnet is significant under paraphrase but flat under templates; Llama
  shows little within-model instability on either. The claim is therefore not “every model is internally
  chaotic everywhere,” but “for any given model there exists a meaning-preserving perturbation under
  which its borderline self-classification is substantially noisier than its clean-case baseline”, which
  is already incompatible with the feature reading’s prediction of a stable, principled internal line.
• The control baseline is not zero (5–10%). The claim is excess borderline instability, not a perfect-
  versus-chaotic contrast.
Read together with §6, the full picture is: the dominant, universal failure is cross-model, all four
models draw incompatible lines (κ collapse to 0.20–0.50 on regulatory text, and to 0.41–0.71 on the
full policy set, which includes the easier synthetic control; on the contested subset alone agreement is
far lower), and the bias is bidirectional, model-specific, and cross-lab. The within-model instability is
a secondary, corroborating signal that even a single model’s line is not the principled invariant the
feature reading requires. Every model is unreliable on at least one axis, Llama chiefly via cross-model
bias, Opus/GPT-4o/Sonnet via within-model instability as well. Neither across models nor reliably
within a single model does self-report yield a trustworthy routing signal, and that, applied to the
contested mass that is half-to-two-thirds of regulatory text, is what makes single-estimator self-routing
operationally disqualifying at scale (§3).


                                                   13
C     Extended Protocol and Related Work

C.1   Models and corpora

Models. Four instruction-tuned foundation models span three labs: Claude Sonnet and Claude Opus
[2], GPT-4o [20], and Llama-3.1-70B [9]. All four label every target. The cross-lab span is deliberate,
since the model-specificity claim requires showing that disagreement is not an artifact of one lab’s
training, and the three cross-lab pairs carry that argument. Figure 4 gives every pairwise agreement
across three corpora.
Data and ground truth. Calibration endpoints, where the label is essentially uncontested, are IFEval
[29], whose instructions are verifiable by construction, as the clearly-decidable pole and MT-Bench
[28] as the clearly-judgment one. The borderline comes from policy: predicates decomposed from
the EU AI Act [7] and FINRA [8], and from an operational AI-agent rule-set, with a gold-labelled
synthetic corpus as a controlled supplement rather than a headline. Ground truth on the two regulatory
corpora is a proxy: an LLM assigned each predicate a grounding level from rule and predicate text
alone, blind to the panel’s outputs, under a fixed scheme in which the two grounded levels map to
DECIDABLE and the two ungrounded ones to JUDGMENT . We therefore lead the vs-ground-truth
claims on the gold-labelled synthetic corpus and the endpoints, and lead the headline claims on the
ground-truth-free disagreement metric, which needs no labels at all. §C.2 reports a replication against
human labels.
Reproducibility note. The panel cannot be reconstructed exactly: the Sonnet checkpoint used for
the labels reported here was retired by its provider after our run. Our released label files therefore
constitute the primary artifact. The OpenAI model was specified by a floating alias rather than a
dated snapshot, so its exact revision is not recoverable either. Where we re-probe (§E.2) we hold the
panel fixed within a comparison.

C.2   Replication against human labels

Because the regulatory-corpus ground truth is LLM-assigned, we replicated the core measurement
against labels a machine did not produce. A human annotator sorted 54 FINRA rules into three
enforceability tiers, A settleable by a fixed interpretation-free procedure, B structured-ambiguous,
and C requiring judgment, working from written tier definitions fixed before annotation and blind
both to every model output and to the deterministic signal file. One rule was excluded, leaving 53. We
map A to DECIDABLE and B and C to JUDGMENT, and additionally report the A-versus-C contrast
with the structured-ambiguous middle removed. The rubric, decoding and panel are those of §5, with
the retired Sonnet checkpoint replaced by its nearest dated successor.
What holds. Pairwise agreement is κ 0.34–0.48, inside the 0.20–0.50 we report for regulatory text,
and the models contest 34% of the 53 rules (44.7% with the middle tier removed) against 52% on
FINRA predicates. The ordering holds where it matters: GPT-4o is again the most conservative
member, under-claiming 85% of decidable rules while over-claiming 3%, and the panel spreads by a
factor of nearly four in how much it will automate at all, from GPT-4o’s 4 rules to Opus’s 15 of the
same 53. Unanimity again buys precision at the cost of coverage: on the A-versus-C contrast the
unanimous set is 100% precise over 10% of the decidable rules.
What does not. The error is not bidirectional here. Every model leans the same way, over-claiming
3–18% and under-claiming 45–85%, where on decomposed regulatory predicates two models lean
each way. We attribute this to granularity rather than to a failure of the earlier result: whole rules
seldom admit a fixed procedure, and the human labels put only 20 of 53 on the decidable side against
153 of 231 for predicates. The consequence for §8 is worth stating, since the 97–99% unanimous
precision there is explained by bias independence: on a corpus where the panel leans one way,
unanimity’s precision is inherited from the panel’s shared caution rather than from errors cancelling.
Scope. Fifty-three rules give intervals 15 to 30 points wide, so this corroborates a pattern and does not
sharpen a number. The targets are whole rules rather than decomposed predicates, and the annotation
is by one person. Independent multi-annotator labelling at predicate granularity remains the strongest
available improvement to this evidence base.
Protocol. Each model labels each predicate, blind, as DECIDABLE or JUDGMENT against one fixed
rubric, at temperature 0, with no hedging permitted. Labels are single-draw, and we verify that this is


                                                   14
adequate rather than assuming it: re-running the identical rubric and corpus months later reproduced
each unchanged model’s own labels at 97.2% (GPT-4o), 99.0% (Opus) and 99.4% (Llama-3.1). The
one model whose labels did not reproduce had been version-upgraded in the interval, which is the
subject of §7. We compare each label to ground truth where available and to the other models. For
the within-model stability test (§E.2) we re-probe contested predicates under meaning-preserving
perturbations: an LLM-paraphrase instrument (paraphrases authored and equivalence-validated by a
model outside the judge set) and a deterministic template instrument (neutral surface wrappers, no
model in the loop), with a control group of unanimous-clear predicates.
Metrics. (i) Over-claim and under-claim rates vs. ground truth, kept on their separate denominators
(§4). (ii) Cross-model agreement via Cohen’s κ [4], on the endpoints and the borderline. (iii) The
contested rate, fraction of predicates without a unanimous label, as a ground-truth-free measure of
borderline prevalence. (iv) Corroboration precision and coverage: among unanimous-DECIDABLE
predicates, the fraction truly decidable, and the share of true-decidable recovered, versus single-model
self-report. (v) Within-model flip rate on the borderline vs. control. For the enforcement capstone
(Appendix G) we additionally report rule-level fidelity vs. a holistic reference, the deterministically-
automated fraction, and the gating-attributable false-clear rate.
Programmatic / verify-don’t-judge evaluation. Program-as-a-judge approaches (PAJAMA [12]
synthesize executable judging programs instead of scoring with an LLM, cutting cost and bias;
reinforcement learning with verifiable rewards (RLVR; e.g. Writing-Zero [13] couples training to
checkable signals and treats verifiability as given by domain (math/code checkable, open-ended
not). Both assume you know what is program-checkable. We address the prior question they skip:
which predicates are checkable when the model cannot self-identify them, and how to establish that
boundary safely (corroboration + a verification gate) rather than presupposing it.
Metacognition and self-knowledge. Work on whether models know what they know calibrates
confidence in answers [14, 26]. Our type-vs-answer distinction (§4.1) is orthogonal: a model can be
well calibrated about whether its answer is right while being unreliable about whether the question
has a checkable answer at all.
Agentic runtime enforcement (application context). Neuro-symbolic oversight and runtime policy
enforcement for agents (e.g. FormalJudge [30]; AgentSpec [25]) presuppose a policy already
partitioned into checkable vs. judged obligations; our contribution is upstream, establishing that
partition reliably is a prerequisite for any such system.

C.3   A reasoning-era panel member

The panel of §5 predates wide availability of models trained to deliberate before answering, and
type-classification is plausibly the kind of task extended reasoning helps. We therefore added a
fifth labeller after the measurements above were complete and fixed: an open-weight reasoning
distillation (DeepSeek-R1-Distill-Qwen-14B, served locally, temperature 0, 2,000-token budget
so the deliberation trace is never truncated). Traces are stripped before parsing, and a response
from which no label can be recovered is recorded as missing rather than defaulted, so a truncated
deliberation cannot masquerade as a JUDGMENT label. It labelled the 559 policy predicates, the 73
agent rules and the 200 calibration endpoints; it is not part of the four-model panel used everywhere
else in this paper, and no figure or table above includes it.
Deliberation does not repair the boundary; here it widens the damage. On regulatory text the
model calls 73.2% of predicates decidable, more than Sonnet (65.8%), Llama-3.1 (62.8%), Opus
(32.5%) or GPT-4o (17.7%), which makes it the most permissive labeller we measured. Its over-claim
rate is 47% on EU AI Act judgment predicates and 25% on FINRA. On the operational agent rule-set
it over-claims on 92% of judgment predicates and calls 95.9% of all predicates decidable, so the
domain flip of §6 holds for a fifth model and reaches its largest value there. Pairwise κ against
the incumbents is 0.13 (GPT-4o), 0.26 (Opus), 0.54 (Sonnet) and 0.59 (Llama-3.1): adding a more
deliberative model lowers the floor of the agreement range rather than raising it.
It is permissive at the judgment pole as well. On IFEval the model is exactly right, calling all
120 instructions decidable. On MT-Bench it calls 30% of them decidable, against 0.0% for GPT-4o,
1.2% for Sonnet and Llama-3.1 and 10.0% for Opus, so its permissiveness is an offset present even
where the incumbents are near-perfect rather than something the borderline induces. Where it errs
is orderly: over-claiming runs at 50% on math, stem and extraction, 30% on reasoning and 20%


                                                  15
                           Corpus             n   R-base    R-proc    R-spec
                           EU AI Act        175     65%       59%      34%
                           FINRA             56     52%       55%      32%
                           Agent rule-set    73     33%       40%      33%
                           Synthetic        328     23%       23%      11%
                           Endpoints        120      0%        0%       0%
Table 3: Contested rate (no unanimous label across four models) by corpus and rubric. R-base is the
published rubric.



on roleplay, and vanishes on humanities and writing. A model trained against verifiable rewards in
mathematics and code appears to have learned that those domains admit checkable answers, and to
carry the inference across to the claim that the quality of a response in them is checkable too. That is
the estimator-as-oracle error of §4 reached by a training route rather than by a capability limit, which
is a further reason not to expect scale alone to remove it.
The unanimous gate is unmoved, as predicted. §8 argues that corroboration is bound by its most
conservative member and is therefore insensitive to who else joins. Adding the most permissive
labeller in this paper leaves the unanimous-DECIDABLE set unchanged on both corpora: 33 predicates
at 97.0% precision and 20.9% coverage on regulatory text, and 41 at 82.9% with the same seven
false-decidables on agent rules, in each case identical to the four-model gate. The prediction was in
the text before the experiment was run.
Scope. This is one open-weight distillation at 14B, not a frontier reasoning system, so it speaks to
whether deliberation repairs self-decidability and not to whether capability does. The direction is
nonetheless the one that matters: a model given time to think became the panel’s least safe member
on the corpus where a verifier would act on its label without escalation.

D    Specification Ablation in Full
The obvious objection is that we measured ambiguity in our classification prompt rather than
unreliability in the models. We red-teamed our own harness, and report the result including the part
that goes against us. Two orthogonal manipulations of the published rubric hold corpus, models and
decoding fixed: R-proc (202 tokens) restates the same criterion procedurally rather than definitionally,
isolating surface form; R-spec (707 tokens) adds a four-step decision procedure, five boundary rules
and eight worked examples, isolating underspecification. We pre-committed to the bar that a fall of
more than 5 pp in contested rate on a real corpus would support the objection.
Surface form does not move the boundary (Table 3). Under R-proc the contested rate is flat on
every corpus (−6, +3, +7, 0, 0 pp) while individual models flip 6.6–16.3% of their own labels, in
no consistent direction against ground truth. Rewording changes which predicates a model calls
decidable without changing how much the panel disagrees.
Specification does move it, and our pre-committed bar is crossed. Under R-spec the contested rate
falls 30.9 pp on the EU AI Act and 19.6 pp on FINRA, far beyond the 5 pp bar. On the contested-rate
metric, the objection holds for both regulatory corpora, and we report it as such.
But the agreement R-spec buys does not track truth. Applying this paper’s own corroboration measure
to the ablation: of the 71 regulatory-text predicates R-spec converts from contested to unanimous,
the manufactured consensus is correct 57.7% of the time (Wilson 95%: 46.2–68.5), against 88.8%
(80.5–93.8) for consensus that formed under R-base without prompting, and 90.4% for the R-base-
unanimous subset that survives into R-spec. The intervals do not overlap. One confound deserves
naming, that if the proxy annotator shared the unprompted models’ intuitions then R-base-unanimous
would agree with it partly by construction; the direction of the errors rules this out, since R-spec’s
consensus errs 97% toward JUDGMENT against a reference set that is 74.6% decidable, so the
confound would require an annotator who systematically over-calls decidable. The manufactured
consensus is 35.2% decidable against that 74.6%. Twenty-nine of the 30 errors are under-claims.
R-spec does not resolve the boundary, it withdraws from it, routing to a judge what a program could
settle: the expensive corner of the dual-cost model rather than a solution to it, with safety preserved
and the automation the routing decision exists to enable forfeited.


                                                  16
On operational agent rules, specification buys nothing. The contested rate is unchanged (33% →
33%), and even that stability is coincidental: half the membership churns, 12 predicates becoming
contested and 12 unanimous. The corpus where a runtime verifier actually acts is the corpus a decision
procedure with worked examples cannot help.
Swap the examples and the consensus moves. We pre-registered four predictions and ran R-spec′ ,
identical to R-spec to the character but for the eight worked examples, replaced by eight different
correct ones. B1 confirmed: contested rate 40.7%, inside the predicted 25–41% band. B2 confirmed:
the predicates R-spec′ resolves overlap the R-spec-resolved set at Jaccard 63.3%, so swapping the
examples changes roughly a third of which predicates get settled at all. B3 failed: we predicted the
consensus would again fall below 70% accurate, and it is 75.9% (63.5–85.0). B4, the falsifier that
would have shown specification resolving a stable and correct subset, did not trigger. The failed
prediction is the more informative one. Two sets of worked examples, both correct and both authored
in good faith, inside an otherwise character-identical rubric, yield consensus that is 58% and 76%
accurate: the benefit of specification is a lottery over an authoring choice the rubric does not record.
The direction is unchanged, all 14 errors made by R-spec′ being under-claims, against 29 of R-spec’s
30.
What the ablation establishes. The disagreement we measure is not an artifact of one phrasing: a
different phrasing produces different labels and the same disagreement, and a far more prescriptive
one produces agreement whose accuracy swings 18 points on which examples were written, landing
13 to 31 points below consensus that formed unprompted. No rubric we wrote made the panel both
agree and be right, and none of them moved the accuracy of the agreement that formed without
prompting.


E     Deferred Instruments and Diagnostics

The following material expands §6. The body states the headline numbers and cites §E.2 for the
stability result; this appendix gives the instruments, the full tables and the diagnostics behind them.


Table 4: Contested rate (no unanimous decidable/judgment label) by corpus and panel size. Measured
ground-truth-free as cross-model disagreement.
                       Corpus                                  3-model   4-model
                       EU AI Act (regulatory text)              54%       65%
                       FINRA (regulatory text)                  43%       52%
                       Synthetic (designed, gold labels)        16%       23%
                       Agent rule-set (operational, agentic)    22%       33%
                       Pooled (policy corpora)                  31%       39%


On actual regulation, half to two-thirds of decomposed predicates fall in the zone where models
cannot agree under the rubric of §5; a far more prescriptive rubric reduces this to roughly a third, but
does so without improving accuracy (§7), so the reduction buys agreement rather than resolution
whether the predicate is even mechanically checkable. The contested rate rose from 3 to 4 models
exactly as predicted, adding a model can only create disagreement, never remove it, which confirms
these are conservative lower bounds, not artifacts of a particular panel. The synthetic-vs-real gap is
itself a result: a method validated only on clean constructed data would report a ≈20%-borderline
world and badly understate the problem, direct support for anchoring the finding on regulatory text
rather than self-built corpora.


E.1   Why this is a bug, not appropriate humility

The strongest objection to the above is the “feature” reading (Table 5): the borderline is genuinely
borderline; models are right to be uncertain; disagreement is well-calibrated humility. If true, it
would defang the result. We reject it on four grounds, three already in the data and one we test
directly. The feature reading makes four predictions; the bug reading makes the opposite:


                                                    17
           Table 5: Predictions of the feature (humility) reading versus what we observe.
                       If a feature (humility)              What we observe
                       Models would hedge or ab-            Rubric forbids hedging; mod-
                       stain on contested items             els comply confidently and
                                                            disagree oppositely, confi-
                                                            dent contradiction, not shared
                                                            doubt
                       No per-model directional bias        Directional, model-specific
                       (everyone equally unsure)            bias, one model leans over-
                                                            claim, another under-claim.
                                                            Idiosyncratic priors, not cal-
                                                            ibrated uncertainty
                       Degradation everywhere (the          κ 0.99 on clear endpoints,
                       task is just hard)                   collapse only on the opera-
                                                            tionally critical middle, local-
                                                            ized exactly where the routing
                                                            decision is consequential
                       Each model internally con-           (§E.2, direct test) a model that
                       sistent (a stable line)              flips its own label on meaning-
                                                            preserving paraphrases is not
                                                            tracking a property of the
                                                            predicate


Table 6: Within-model flip rates (borderline / control) under two perturbation instruments. p-values
vs. clean-case baseline.
                         Model                   Paraphrase                  Template
                         Opus          28% / 6% (z=3.15, p=0.002)           33% / 5%
                         GPT-4o              15% / 8% (n.s.)                44% / 7%
                         Sonnet        25% / 8% (z=2.41, p=0.016)           13% / 10%
                         Llama-3.1             16% / 10%                    20% / 27%



E.2   The within-model stability test

The three legs above are cross-model. A fourth is available within a single model, and it is the
most direct: a model that is tracking a property of the predicate should give the same label when
the predicate is restated without changing its meaning. We re-probe contested predicates under
two meaning-preserving perturbation instruments, an LLM-authored paraphrase set validated for
equivalence by a model outside the judge panel, and a deterministic template instrument that wraps
the predicate in neutral surface variation with no model in the loop, against a control group of
predicates the panel labelled unanimously. Appendix B gives the construction of both instruments
and the equivalence-validation protocol.
The effect is instrument-dependent and model-dependent (Table 6), and we report it as a corroborating
leg rather than a uniform law. Under the loophole-free template instrument Opus flips its own
borderline label 33% of the time against 5% on controls, and GPT-4o 44% against 7%. Every
model destabilises under at least one instrument; Llama’s failure surfaces chiefly as cross-model
disagreement rather than self-inconsistency. A label that moves under a restatement of the same
predicate is not a reading of that predicate.

E.3   The same failure outside machine learning

The same failure has a shape outside machine learning, and we raise it deliberately. Psychiatric
nosology met this problem first and attempted the same repair: faced with poor inter-rater agreement
it operationalized its criteria into explicit decision rules and structured interviews. The DSM-5 field
trials nonetheless reported intraclass κ in the 0.20–0.39 “questionable” band for six diagnoses and
below 0.20 for three [23], and the standing critique is that reliability and validity came apart, which is


                                                       18
                       1.0



              0.75
  pairwise Cohen’s κ




                       0.5



              0.25



                        0
                           clear                      real                                       agent
                         endpoints                 regulation                                    rules
Figure 4: Every pair of the four models, across three corpora. Where the answer is clear the panel
is near-unanimous (κ 0.92–0.99). On regulatory text it collapses to 0.20–0.50: the six lines fan out,
and the worst pair agrees barely above chance. Agreement partially recovers on agent rules, but that
recovery is not reassurance. It is where the models over-claim together (Fig. 2), and correspondingly
where the precision of a unanimous panel falls from 97–99% to 83% (§8).



what our high-specificity rubric reproduces. The judgment literature supplies the vocabulary: level
noise (raters differ on average), pattern noise (rater-by-case idiosyncrasy) and occasion noise (a
rater differing from itself) [15] map onto our three results, and pattern noise is precisely why our
boundaries cross rather than nest, leaving no uniformly conservative model to pick. The quick reading
of all this is that estimators are noisy and that this has been known for decades. That reading misses
the claim: the finding is not that the estimator is noisy but that the routing decision inherits the noise,
and that the standard remedy, escalating the hard cases, presupposes a routing step which is itself
noisy in the direction that disables it. Aggregation is the prescribed remedy there too, and it carries
the caveat we measure directly, that it cancels independent error and not shared bias (§8). Their
failure object is the judge’s accuracy on a judging task; ours is its inability to recognise when judging
is the wrong tool. Even a perfectly debiased judge does not tell you which targets needed it.


E.4                    Further limitations

“Decidable” is partly conventional. Some predicates are genuinely grey, and where reasonable
 annotators would split there is no fact of the matter we are failing to recover. That does not rescue
 self-report; it is a further reason not to trust one estimator’s routing call (§6).
The within-model instability is instrument- and model-dependent. We report it as a corroborating
signal rather than a uniform law, and the cross-model result carries the argument.
The enforcement capstone is preliminary. It is characterized on a synthetic substrate with a single
deterministic-check model. It establishes the safety property by construction, and we draw no stronger
claim from it.
We do not address adversarial manipulation of the predicates themselves, which a deployed enforce-
ment system must also resist.


                                                    19
                                ROUTED TO A CHECK                                ROUTED TO A JUDGE

                      correct                                          UNDER-CLAIM
       criterion is   settled by code: no model call, no latency,      a model call re-derives what one line of code
     DECIDABLE        no token cost.                                   would settle. Wasteful, but visible: someone
                                                                       can count the calls.


                      OVER-CLAIM                                       correct
    criterion needs   compliance certified that was never assessed.    escalated to a judge, as the criterion requires.
     JUDGMENT         Unsafe, and silent: the verdict looks like any
                      other.


Figure 5: The dual cost. Rows are what a criterion is; columns are where the verifier sent it. The two
errors lie on the anti-diagonal and are not mirror images: under-claiming is expensive and auditable,
over-claiming is cheap and silent. No choice of model minimises both, since the bias runs in opposite
directions in different models (§6).


The 36 synthetic action records are ours. They are generated combinatorially with a difficulty gradient
rather than authored one by one (§A), which removes the objection that we wrote maximally explicit
evidence, but not the objection that we wrote the substrate at all. The 20 predicates behind the
self-consistency null are likewise not a random sample of the corpus, so that result is a bounded check
rather than a corpus-wide measurement.
Our reasoning-era check uses a 14B distilled model. It tests whether extended deliberation repairs
the boundary, not whether frontier reasoning capability does.

E.5     Inherent annotation disagreement

Inherent annotation disagreement. The strongest reading against us is not about models at all:
that these predicates are genuinely ambiguous, that human annotators would disagree too, and that
we have measured task ambiguity rather than model unreliability [21]. We answer it empirically
(§6): genuine ambiguity predicts convergent uncertainty and we observe confident contradiction,
with models answering decisively in opposite directions and the same model reversing itself under
meaning-preserving paraphrase.

E.6     An honest concession

We do not claim every contested predicate has a crisp true type. Some of the contested zone is
genuinely grey, reasonable annotators would split, and for those predicates there is no fact of the
matter we are failing to recover. But that concession does not rescue self-report; it is an additional
reason not to trust a single estimator’s routing call. The actionable claim survives either way: where
the type is determinate, no single model reliably finds it (bidirectional, unstable); where it is genuinely
indeterminate, a single model’s confident label is meaningless. In both cases the boundary must come
from somewhere other than one estimator’s self-report.


F      The Dual-Cost Model

Compounding makes this worse than additive. A rule passes only if its predicates are handled
correctly jointly, so a single mis-typed predicate can flip a rule verdict or silently drop a control, and
the probability that every routing call in a task is correct decays geometrically in predicate count.
Coarse evaluation tolerated a noisy estimator precisely because it never had to be right many times in
a row. The fine-grained regime does, and it is the regime everyone is building toward.
Let a deployment perform N predicate-evaluations per period (agent fleet: agents × steps × rules-
checked), with judge cost cj per evaluation and a negligible deterministic-check cost. Let q be the
fraction safely auto-verified (verified-deterministic coverage) and f the false-decidable rate among
auto-enforced predicates.


                                                          20
• Token cost = N (1 − q) cj . Savings vs. all-judge = N q cj (recurring, every period).
• Safety cost = N q f × (expected loss per missed determination). Single-model self-report gives
  f = 1 − precision (e.g. 0.11 for Sonnet on regulatory text); verification drives f →≈ 0.
• Amortized setup = corroboration ((m−1) extra label calls per predicate, once) + check synthesis +
  periodic re-verification under drift, a one-time/periodic cost against recurring per-period savings.
The argument the model makes precise: single-model self-report forces a lose–lose, pick a permissive
model and pay the safety bill (f up to ≈0.11), or pick the conservative model and pay the token
bill (q ≈ 0.22–0.26, i.e. escalate 3/4 of decidable work). Corroboration-plus-verification escapes
both: f → 0 from verification while q tracks the corpus’s true deterministic content rather than
the most-cautious model. At any real evaluation volume the recurring token savings dominate the
amortized setup; the safety gain is categorical (guarantee vs. ≈1-in-9 leak).

G    Enforcement Capstone: Preliminary Operating Point
This appendix reports a single preliminary run on synthetic data, and it uses the agreement gate of
§8.2 rather than the interventional gate the paper adopts. We retain it because it records how that gate
behaved end to end before we measured why it does not discriminate, and no claim in the body now
rests on it.
An end-to-end verify-gated enforcement run on the synthetic corpus automates ≈33% of predicate-
evaluations deterministically with zero gating-attributable missed violations. That safety property
holds by construction rather than empirically: a predicate is auto-enforced only if a synthesized check
matches the reference judge on the held-out graduation set, so a false-decidable cannot survive the
gate. It is the one property of the architecture in §8 that does not depend on classification being
reliable.
The strict fidelity bar we set, verify-gated within 2 points of judge-everywhere, was not met at
the default graduation threshold, at a cost of roughly 5 points. That entire cost appears as over-
flagging rather than as missed violations. We report the default-threshold operating point rather than
searching for a favourable one, we do not claim the strict bar is reachable, and characterising the full
automation–fidelity tradeoff would require a threshold sweep we have not run.
The direction of the shortfall is worth stating, because it matches what the rubric ablation found
by an unrelated route (§7): the prescriptive rubric gave up automation to preserve safety, sending
decidable predicates to a judge in 97–100% of its errors, and the verification gate gives up automation
to preserve safety by over-flagging. Two different mechanisms, the same trade. That is the dual-cost
model of Appendix F appearing twice from opposite directions, which suggests the tradeoff is
structural rather than an artifact of either mechanism.




                                                  21
