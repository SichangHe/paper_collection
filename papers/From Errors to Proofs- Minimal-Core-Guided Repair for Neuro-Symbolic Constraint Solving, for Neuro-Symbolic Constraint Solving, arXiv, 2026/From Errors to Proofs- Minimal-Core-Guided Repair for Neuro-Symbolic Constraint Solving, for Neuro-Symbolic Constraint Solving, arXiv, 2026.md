                                                                From Errors to Proofs: Minimal-Core-Guided Repair
                                                                      for Neuro-Symbolic Constraint Solving

                                                                                              Dipankar Sarkar
                                                                                           Independent Researcher
                                                                                         dipankar@skelfresearch.com


                                                                   Abstract                                 formed and the solver reports a parse or grounding error.
                                                                                                            Others are well formed but unfaithful: they add a constraint
                                              Making language models solve constraint prob-                 the problem never stated, which can make a solvable prob-
                                              lems reliably often means having them translate               lem report as unsatisfiable; they drop a stated constraint,
                                              the problem into a formal specification and dele-             which admits an invalid solution; or they misstate the ob-
                                              gating the search to a sound solver. But the trans-           jective. The self-correction in current language-model plus
                                              lation is itself a language-model task, and an un-            solver pipelines, exemplified by the self-refinement in Logic-
arXiv:2608.14771v1 [cs.AI] 14 Aug 2026




                                              faithful translation makes the solver faithfully solve        LM [Pan et al., 2023], reacts to the first kind: it returns
                                              the wrong problem. Existing pipelines repair only             the solver’s error message and asks the model to try again.
                                              translations that crash, returning the solver’s error         When the solver does not error, the loop is silent, and the
                                              message and falling silent when the program runs              well formed but unfaithful encoding survives.
                                              but is wrong. We replace the error message with                  We propose to repair with a proof rather than an error. We
                                              a proof: when the generated program is unsatisfi-             encode every decision as a single assign(Var,Value)
                                              able, we extract a minimal unsatisfiable core over            relation in Answer Set Programming [Lifschitz, 2008; Geb-
                                              the model’s own constraints and hand it back the              ser et al., 2012] and solve with clingo [Gebser et al., 2019].
                                              exact set that cannot hold together, a leakage-free           When the program is unsatisfiable, we do not report “no so-
                                              signal that localizes the fault. On a new bench-              lution”; we compute a minimal unsatisfiable core over the
                                              mark of 77 problems with an exact oracle, trans-              model’s own integrity constraints, the smallest subset that
                                              lation to Answer Set Programming is faithful on               cannot all hold at once, and hand that set to the model. The
                                              six of seven domains and fails only on aggregate-             core is a proof artifact: it localizes the conflict to a few con-
                                              coverage scheduling, which concentrates the trans-            straints, which is exactly the information a generic error mes-
                                              lation tax in one diagnosable pattern. A minimal              sage withholds. It is computed from the model’s own pro-
                                              core, rather than a bare error, is what stops a weaker        gram rather than from ground truth, so it adds no oracle leak-
                                              model from fabricating solutions to infeasible prob-          age.
                                              lems, cutting fabrication from 79% to 7%. A strong               We then ask an empirical question the literature rarely
                                              chain-of-thought baseline meanwhile matches the               tests: at the scales where a solver can also certify the an-
                                              symbolic route on accuracy, so the route’s value is           swer, how much does symbolic offloading actually help, rel-
                                              not accuracy but certificates and its refusal to fabri-       ative to plain prompting and to chain-of-thought, and where
                                              cate.                                                         does it help. We answer it on a new benchmark of 77 prob-
                                                                                                            lems across seven domains with a programmatic oracle, on
                                         1   Introduction                                                   two open-weight models. The answer is nuanced rather than
                                         Language models are increasingly asked to solve discrete           a uniform win. Translation is faithful on most domains and
                                         reasoning problems such as scheduling, seating, assignment,        the symbolic route matches or beats chain-of-thought there,
                                         and packing. Left to free-form generation they return flu-         but a single domain breaks it; a strong chain-of-thought base-
                                         ent answers that often violate the stated constraints, be-         line is hard to beat on accuracy; and the distinctive payoff of
                                         cause autoregressive decoding has no mechanism to enforce          the symbolic route is that it certifies optimality and infeasibil-
                                         a global combinatorial constraint. A standard remedy sepa-         ity and never fabricates a solution, which prompting cannot
                                         rates translation from search: the model converts the natural      promise.
                                         language problem into a formal specification, and a sound          Contributions.
                                         solver does the reasoning [Pan et al., 2023; Ye et al., 2023;         • Minimal-core-guided repair (Section 3): we repair a
                                         Olausson et al., 2023; Gao et al., 2023]. The solver supplies           language model’s formalization with a minimal unsatis-
                                         the guarantee the model cannot.
                                            This recipe is only as good as the translation, and language-      0
                                                                                                                 Accepted as a poster at the IJCAI-ECAI 2026 Workshop on
                                         model translations fail in two different ways. Some are mal-       Logic and Symbolic Reasoning (LogiSymb).
      fiable core over its own constraints rather than a solver     and keep optimization instances small enough for the solver
      error message. The signal is structural and leakage-free,     to certify optima.
      it ports the conflict-explanation idea from constraint pro-
      gramming and answer set programming [Junker, 2004;            Self-correction and the signal it uses. Iterative self-
      Gebser et al., 2008] into the repair loop, and we iso-        correction improves model outputs, and the methods differ
      late its effect with a controlled error-message baseline      mainly in what signal drives the next attempt. Self-Refine
      [Pan et al., 2023]. The benefit is conditional: large on      [Madaan et al., 2023] and Reflexion [Shinn et al., 2023] use
      a weaker model, negligible on a stronger one that rarely      the model’s own verbal critique; Self-Debugging [Chen et al.,
      errs.                                                         2024] uses program execution results; Logic-LM [Pan et al.,
                                                                    2023] uses the solver’s error message. All of these react to an
    • A diagnosis of autoformalization fidelity (Section 6):        observed event: a critique, a failed test, a crash. None uses a
      with an exact oracle we show translation to ASP is            proof of why the current attempt is inconsistent. Our repair
      faithful on six of seven domains and collapses only on        signal is exactly such a proof, and our controlled comparison
      aggregate-coverage scheduling, localizing the transla-        shows that what matters is not that repair happens but what
      tion tax to a formalization pattern rather than the model.    information it carries.
    • A recalibration of when offloading helps (Sections 6
      and 7): a strong chain-of-thought baseline matches the        Conflict explanation and minimal unsatisfiable cores.
      symbolic route on accuracy, so its value is certificates      Identifying a small set of constraints responsible for unsat-
      and robustness; the route never fabricates a solution for     isfiability is a classical problem in constraint programming
      an infeasible problem, whereas direct prompting does so       and satisfiability. Junker’s QuickXplain [Junker, 2004] com-
      21% of the time. We release the benchmark and oracle.         putes preferred minimal conflicts for over-constrained prob-
                                                                    lems by divide and conquer, and deletion-based filtering is
                                                                    the simplest member of that family. In Answer Set Program-
2    Background and Related Work                                    ming the same idea underlies debugging of inconsistent pro-
                                                                    grams [Gebser et al., 2008] and core-guided optimization in-
Our work sits at the meeting point of four lines: tool-
                                                                    side modern solvers [Gebser et al., 2019]. Our contribution
augmented reasoning, autoformalization, self-correction, and
                                                                    is to carry this proof artifact across the boundary into the
conflict explanation. We take the method from the last and
                                                                    language-model repair loop: instead of asking the model to
apply it to the problem raised by the first three.
                                                                    debug from a flat error string, we hand it the minimal con-
Faithful reasoning by offloading to solvers. A growing              flicting subset that a solver-side conflict analysis produces.
body of work makes language-model reasoning faithful by             To our knowledge, minimal unsatisfiable cores have not been
delegating inference to an external system. Logic-LM [Pan           used as the feedback signal for repairing a language model’s
et al., 2023] translates a problem into one of several sym-         formalization.
bolic languages and calls a matching solver; SatLM [Ye et al.,
2023] generates a declarative specification for a satisfiability-
modulo-theories solver; LINC [Olausson et al., 2023] maps           3   Approach
text to first-order logic and calls a theorem prover; program-      Our system follows the standard division of labor between a
aided prompting [Gao et al., 2023] offloads arithmetic to a         language model and a solver, but it makes the translation step
Python interpreter. These methods target deductive question         robust instead of assuming it correct. The model is responsi-
answering, on datasets such as ProofWriter, FOLIO, and AR-          ble only for turning a natural language problem into a formal
LSAT, or arithmetic word problems. We target combinatorial          specification; a sound solver does all of the search. Our con-
constraint satisfaction and optimization over Answer Set Pro-       tribution is the loop that sits between them. When the solver
gramming, where correctness means feasibility or optimality         reports that the specification has no solution, we neither ac-
of an assignment rather than the truth of an entailment, and        cept that verdict at face value nor restart the model blindly.
where the relevant failure is silent over-constraint or under-      We extract a proof of the inconsistency, in the form of a min-
constraint rather than a wrong proof step.                          imal unsatisfiable core, and ask the model to reconcile that
Autoformalization is the bottleneck. Once search is del-            proof with the problem text.
egated, accuracy is bounded by the fidelity of the transla-            A problem passes through four stages. First, the model
tion. Autoformalization studies this translation directly, from     produces a structured ASP encoding over a fixed decision re-
natural language to formal mathematics [Wu et al., 2022].           lation. Second, the encoding is assembled into a program and
For optimization specifically, the NL4Opt competition [Ra-          run through clingo. Third, the solver outcome is classified
mamonjison et al., 2023] and OptiMUS [AhmadiTeshnizi et             into one of four categories, and if it is not a clean success a
al., 2024] map word problems to mixed-integer linear pro-           typed diagnostic is constructed from the solver state. Fourth,
grams. Consistent with that line, we find that the bottleneck is    the diagnostic is returned to the model, which revises the en-
the formalization rather than the search, and that it is uneven     coding; the second through fourth stages then repeat up to K
across problem types: faithful on most constraint domains,          times. Only the first stage uses the model creatively. The rest
brittle on the one that needs aggregate-coverage reasoning.         are deterministic and grounded in the solver, so every correc-
We also confirm a known boundary, that Answer Set Pro-              tion the loop applies is justified by a concrete solver artifact
gramming is a poor vehicle for large numeric optimization,          rather than by another free-form guess.
% facts (problem data)
node(n1). node(n2). node(n3).                                         Algorithm 1 Minimal unsatisfiable core (deletion filtering)
color(red). color(green). color(blue).
% choice rule: one colour per node                                    Require: base B, constraints C; B ∪ C unsatisfiable
1 { assign(N,C) : color(C) } 1                                         1: C ⋆ ← C
     :- node(N).                                                       2: for all c ∈ C do
% integrity constraints:
% adjacent nodes get different colours                                 3:    if B ∪ (C ⋆ \ {c}) is UNSAT then
:- assign(n1,C), assign(n2,C).                                         4:       C ⋆ ← C ⋆ \ {c} {drop c}
:- assign(n2,C), assign(n3,C).
% harness appends: #show assign/2.
                                                                       5:    end if
                                                                       6: end for
Figure 1: A complete assign/2 encoding of a three-node graph-          7: return C ⋆
coloring problem. The choice rule generates one colour per node;
each integrity constraint forbids an edge from being monochromatic.
                                                                      forgets the choice rule or models its decisions under some
                                                                      other predicate. It is UNSAT when the program is well formed
3.1   The decision contract                                           and grounds cleanly but has no answer set.
The model emits a JSON object with three fields: facts,                  The four outcomes are not equally informative, and the
which encode the problem data; rules, which contain a                 asymmetry is the reason the rest of the method exists. A SYN -
choice rule that generates candidate decisions together with          TAX ERROR is loud: clingo points at the offending rule, and
the integrity constraints that enforce the requirements; and an       prior error-message refinement already handles this case well.
optional optimize directive. We impose a single contract              The dangerous outcome is UNSAT, because it is silent about
on this output. Every decision is expressed through one rela-         its cause. An over-constrained translation of a perfectly solv-
tion, assign(Var,Value), in which each decision vari-                 able problem, for instance one that hallucinates a constraint
able Var is bound to exactly one Value by a choice rule,              the text never stated, produces a program with no answer set,
and every requirement is expressed as an integrity constraint,        and that program is indistinguishable, from the bare verdict
a rule that begins with :- and forbids the combinations that          alone, from a faithful translation of a genuinely infeasible
violate it. The harness appends #show assign/2. and                   problem. The model that reads only “no answer set” cannot
calls clingo. Figure 1 shows a complete encoding for a small          tell whether it should fix its own constraints or report that the
graph-coloring instance.                                              problem has no solution. Resolving that ambiguity is what
   This contract serves three purposes, and each matters for          the core provides.
the rest of the method. First, it gives a single, uniform notion
of a solution across every domain, so that one oracle can score       3.3   Repair with a minimal unsatisfiable core
the output of any system, whether it is the symbolic pipeline         On UNSAT we localize the conflict before asking the model
or a prompting baseline, without domain-specific parsing; a           to act. Let C = {c1 , . . . , cm } be the integrity constraints the
coloring, a roster, a seating, and a knapsack packing are all         model produced and B the base program made of the facts
just sets of assign atoms. Second, it keeps the encoding              and the choice rule. Because B is satisfiable on its own (the
compact and stable in size as the problem grows, because              choice rule alone always has models), the inconsistency must
the decision logic lives in a constant number of rules while          come from a subset of C. We compute a minimal unsatisfi-
only the facts scale; a graph with three nodes and a graph            able subset C ⋆ ⊆ C, defined by the property that B ∪ C ⋆
with ninety nodes share the same choice rule and the same             is unsatisfiable while B ∪ (C ⋆ \ {c}) is satisfiable for every
constraint schemas. Third, and most important for repair, it          c ∈ C ⋆ , so that every constraint in C ⋆ is necessary for the
cleanly separates the part of the program the model might get         conflict and none is redundant. We obtain it by deletion filter-
wrong, the integrity constraints, from the part that is fixed         ing (Algorithm 1), the simplest member of the QuickXplain
by the data, the facts and the choice rule, which is exactly the      family of conflict-extraction procedures [Junker, 2004]: start-
separation the core extraction in Section 3.3 exploits. To keep       ing from the full set, we tentatively remove each constraint
the comparison fair, every system in our study, including the         and keep the removal whenever the remainder is still unsatis-
prompting baselines, is given the same decision variables and         fiable. The procedure issues at most m satisfiability checks,
their allowed values, so no system is advantaged or penalized         each a fast call on a small program, and for the instance sizes
by the output format and all of them are judged purely on             in our benchmark its cost is negligible next to a single model
whether they reason to a correct assignment.                          call.
                                                                          Two properties of this signal matter. It is structural: C ⋆ is
3.2   Compiling and classifying the outcome                           a proof that those constraints cannot coexist, not a report that
Assembling and solving an encoding yields exactly one of              something went wrong, and it names the exact constraints to
four outcomes, and the loop reacts to each differently. An            reconsider rather than leaving the model to search its whole
outcome is OK when clingo returns an answer set that con-             program. It is leakage-free: every satisfiability check in Al-
tains assign/2 atoms; this is the only terminating out-               gorithm 1 runs on the model’s own program, with the ob-
come, and the atoms become the assignment. It is SYN -                jective removed, and at no point does the procedure consult
TAX ERROR when grounding or parsing fails, which happens              the ground-truth answer, the oracle, or the reference encoder.
when the model writes a malformed rule or an unsafe vari-             The core therefore tells the model where its translation is in-
able. It is EMPTY when the program is satisfiable but pro-            ternally inconsistent, which is information the model is en-
duces no assign/2 atoms, which happens when the model                 titled to, without telling it what the correct answer is, which
it is not. This distinction is what lets us use the core during           System                    Feas. acc.   CSR    Fabr.   Iters
inference without contaminating the evaluation.                           Direct                          74.0   84.5    21.4   0.00
   The repair prompt for UNSAT lists the constraints in C ⋆               Chain-of-thought                98.7   99.8     0.0   0.00
verbatim and frames the choice the core makes explicit: ei-               ASP, no repair                  84.4   85.0     0.0   0.00
ther one of these constraints misformalizes the problem, in               ASP, generic repair             88.3   91.3     0.0   0.78
which case the model should correct or remove it, or the                  ASP, typed+core repair          89.6   91.3     0.0   0.87
named constraints all faithfully encode the text and the prob-
lem is genuinely infeasible, in which case the model should          Table 1: Primary model (gemma4:31b), 77 instances, percent.
leave the encoding unchanged so that the system reports in-          Higher is better except fabricated feasibility (Fabr.), measured over
feasibility. This is the central design point. By naming the         the 14 infeasible instances.
conflict, the core makes “the problem is infeasible” a legiti-
mate and well supported answer, which is the answer a model
is likely to abandon when it is told only that the solver found      deterministic encoder, independent of the language model,
nothing. The other two failure types take simpler prompts:           computes ground-truth feasibility and, for optimization in-
SYNTAX ERROR carries the grounder message and asks for a
                                                                     stances, the optimum; a separate oracle scores any assign-
parse fix, and EMPTY asks the model to add the choice rule           ment for constraint satisfaction, feasibility, and objective. In-
so that decisions surface as assign/2. After any repair the          stances carry one of five labels: feasible, tight (numerically
program is re-solved, and the loop runs up to K = 3 times.           tight but solvable), infeasible (the correct behavior is to re-
Example 1 traces the loop on a real instance from our bench-         port unsatisfiability), stress (larger), and xl (60 to 120 deci-
mark.                                                                sion variables). The xl tier is feasibility-only, because clingo
                                                                     certifies one model quickly at that size but cannot certify large
Example 1 (Repairing an over-constrained roster) On                  numeric optima or large infeasibility quickly.
a six-worker, five-day roster, the model’s first encoding is
unsatisfiable. Deletion filtering returns a minimal core of          5    Experimental Setup
seven constraints: the coverage requirement for the final day
together with the six per-worker caps that, taken together,          Models. We use two open-weight models, gemma4:31b
leave no worker free to staff that day. The repair prompt lists      as the primary model and deepseek-v3.2, served through
exactly these seven constraints. The model recognizes that           a hosted inference provider with greedy decoding. Both are
it had encoded the final-day coverage more strictly than the         run with the same pipeline and prompts.
text required, relaxes that one constraint, and the next solve       Systems. (B1) direct: the model outputs the assignment.
returns a valid roster, in a single repair iteration. A generic      (B2) chain-of-thought [Wei et al., 2022]: reason then answer.
error message for the same instance would have said only             (B3) the ASP pipeline with no repair. (B4) the pipeline with
that the program had no answer set, and, as Section 6 shows,         Logic-LM-style generic-error repair. (B5) the pipeline with
a weaker model given that message tends to keep editing              typed plus minimal-core repair.
until it returns a roster for a problem that has none.               Metrics. Feasibility accuracy (a valid assignment on feasi-
3.4   Isolating the signal: a faithful error-message                 ble instances, or a correct unsatisfiability report on infeasi-
                                                                     ble ones); constraint-satisfaction rate; fabricated feasibility,
      baseline
                                                                     a committed solution for an infeasible problem; optimality
To attribute any effect to the core rather than to the act of re-    gap on optimization instances; and average repair iterations.
pairing, we build a second repair setting that is identical in ev-   We omit per-system token counts, because shared response
ery respect except the feedback. It uses the same pipeline, the      caching across the three pipeline settings confounds them.
same model, the same iteration budget, and the same decision
contract, but on any failure it returns only the raw solver mes-     6    Results
sage, with no core and no per-failure guidance. This recon-
structs the error-message self-refinement of prior language-         Table 1 reports the primary model over all 77 instances.
model plus solver systems [Pan et al., 2023] inside our setup.       Direct prompting is unreliable; chain-of-thought is
We refer to the two settings as TYPED + CORE and GENERIC.            strong. Direct prompting reaches 74.0% feasibility accu-
Because they differ only in the information content of the           racy and fabricates a solution on 3 of 14 infeasible instances
feedback, any difference in their behavior is attributable to        (21.4%). Chain-of-thought reaches 98.7% and fabricates
the core, and Section 6 reports that the difference is small on      none. At the scales in this benchmark, an explicit reason-
a strong model and large on a weak one.                              ing chain solves, optimizes, and recognizes infeasibility for
                                                                     almost every instance without any solver.
4     Benchmark                                                      The translation tax is concentrated in one domain. The
We generate 77 instances over seven domains: graph color-            pooled pipeline numbers understate what is happening per
ing, knapsack, team assignment, seating, timetabling, duty           domain. Table 2 shows that on six of seven domains the
scheduling, and Latin squares. Each instance pairs a descrip-        no-repair pipeline already reaches 100% feasibility accuracy,
tion with a structured specification over assign/2; the de-          and on coloring it exceeds chain-of-thought (100% versus
scription states every constraint in the specification, so a sys-    94.7%). The entire deficit comes from scheduling, where the
tem is never penalized for information it was not given. A           model must encode aggregate coverage and per-worker caps
   Domain                CoT     ASP no rep.     ASP +core                                              gemma4:31b: accuracy by problem-size tier
   graph coloring        94.7           100.0          100.0                                   100




                                                                    Feasibility accuracy (%)
   knapsack             100.0           100.0          100.0                                   80
   Latin square         100.0           100.0          100.0
   seating              100.0           100.0          100.0                                   60
   team assignment      100.0           100.0          100.0
   timetabling          100.0           100.0          100.0                                   40
   scheduling           100.0             0.0           33.3
                                                                                               20             Direct
                                                                                                              Chain-of-thought
                                                                                                                                     ASP, generic repair
                                                                                                                                     ASP, typed+core
Table 2: Feasibility accuracy by domain, primary model. The                                                   ASP, no repair
                                                                                                0
pipeline matches or beats chain-of-thought everywhere except                                          Small                 Stress                         XL
scheduling, which needs aggregate-coverage encoding.
                                                                    Figure 2: Feasibility accuracy by problem-size tier on the primary
with counting constraints, and where the no-repair pipeline         model (small n=56, stress n=11, xl n=10). The pipeline beats
scores 0%. In other words, language-model translation to            direct prompting throughout but does not overtake chain-of-thought,
ASP is faithful wherever the constraints are local, and breaks      whose only visible drop is on the xl tier.
on the one domain that needs global counting. This is a
sharper statement than “the pipeline is less accurate”: it tells           Model                                Direct           Generic repair             Core repair
us which formalization patterns the model can be trusted to
                                                                           gemma4-31b                                 21                           0                 0
produce.
                                                                           deepseek-v3.2                               0                          79                 7
Repair is monotone and a core helps where it is needed.
Self-repair lifts the pipeline from 84.4% to 89.6% on the           Table 3: Fabricated feasibility, the rate at which a system commits to
primary model. The improvement is safe: across all 77               a solution for an infeasible problem, over the 14 infeasible instances,
instances, repair turned four first-attempt failures into suc-      by model and repair signal. Generic error-message repair drives a
cesses and broke none. Fifty-four instances solved on the           weaker model to fabricate; a minimal core does not.
first attempt; the rest entered the loop, and the instances that
exhausted the budget are exactly the scheduling cases the
model cannot encode. On the primary model, typed plus               ing instance, the same domain that fails at small scale. At the
minimal-core repair (89.6%) edges generic repair (88.3%),           sizes a solver can certify quickly, neither method dominates
but the gap is within noise for a model this strong (paired         the other on accuracy.
sign test p = 1.0): a model that rarely produces a spurious
unsatisfiability rarely needs the core. The difference is stark     7                          Discussion
on a weaker model. On deepseek-v3.2, generic error-                 We draw three lessons. First, offloading constraint reason-
message repair fabricates a solution on 11 of 14 infeasible         ing to a solver should be justified by guarantees and robust-
instances (79%), because, told only that the program has no         ness, not by accuracy alone: a strong chain-of-thought base-
answer set, it deletes a real constraint until the solver returns   line is hard to beat on accuracy at the scales where a solver
a model; minimal-core repair fabricates on 1 of 14 (7%), a          can also certify the answer, but it cannot certify infeasibility
difference that is significant by a two-sided Fisher exact test     or optimality, and direct prompting fabricates feasibility of-
(p < 10−3 , Table 3). Appendix A traces both behaviors on           ten enough (21% here) to matter wherever a wrong answer
one infeasible instance. Naming the conflicting constraints is      is costly. Second, the fidelity of language-model autoformal-
what prevents the model from fabricating a solution.                ization is uneven and the unevenness is structured: it is near-
Certificates and robustness. No pipeline setting ever fab-          perfect for local constraints and breaks on global counting,
ricates a solution for an infeasible problem (0% in Table 1),       which suggests that the right unit of trust is the formalization
against 21.4% for direct prompting, because clingo either re-       pattern, not the model. Third, the form of the repair signal
turns an answer set or proves there is none. On optimization        matters most when the model is weak; a minimal core tells
instances the returned solution is provably optimal (zero op-       the model which constraints conflict, which discourages the
timality gap), whereas a prompted answer is optimal only by         fabrication that a flat error message can induce. The broader
inspection. These are guarantees that a prompting system,           message for symbolic reasoning with language models is that
however accurate in aggregate, cannot make about any single         solver-side artifacts, not just solver verdicts, are useful feed-
answer.                                                             back, and minimal cores are one such artifact.
Scale. Figure 2 breaks the primary model down by
problem-size tier. Chain-of-thought stays at or near 100%           8                          Limitations
through the stress tier and drops only to 90% on the xl tier.       The benchmark uses templated descriptions and a single
The clearest accuracy crossover is a single xl instance, a 90-      assign/2 decision relation, which fits discrete constraint
node three-colorable graph, where chain-of-thought violates         and optimization problems but not problems with derived nu-
an edge while the core pipeline returns a valid coloring. The       meric quantities. Answer Set Programming cannot certify
pipeline has its own scale failure on a 120-variable schedul-       large numeric optima or large infeasibility quickly, which
bounds how far we can push scale while keeping exact ground         Trace on an infeasible instance. The instance is a four-node
truth, and the accuracy crossover is therefore a single in-         clique, every pair of nodes adjacent, with three colors, which
stance. Repair is driven by solver-intrinsic signals only, so a     is genuinely infeasible because a clique of four needs four
missing constraint that yields a satisfiable but invalid encod-     colors. On deepseek-v3.2:
ing is caught by the oracle at evaluation rather than repaired
                                                                      • Generic repair.       The first solve is unsatisfiable
in the loop; a verifier in the loop is the natural next step.
                                                                        and the model receives only “no answer set.” It
Threats to validity. Four caveats bound our conclusions.                responds by weakening its coloring constraint,
First, the benefit of the core over a bare error message is             which makes the program satisfiable, and re-
demonstrated on one of our two models; on the stronger                  turns     assign(n3,c1),             assign(n4,c1),
model the two are indistinguishable, so the result identifies a         assign(n2,c2), assign(n1,c3).                   Nodes
regime, weaker and fabrication-prone models, in which feed-             n3 and n4 are adjacent yet share color c1: the system
back shape matters, rather than a universal gain. Confirming            reports an invalid coloring as a solution.
the effect on more models is the most important next step,            • Minimal-core repair. Each solve is unsatisfiable, and
which we leave to future work. Second, every system is given            each time the feedback names the single coloring con-
the decision variables and their allowed values, which makes            straint as the conflict. The model judges that constraint
the task easier than open-ended translation and, if anything,           to be a faithful encoding of adjacency, leaves it un-
flatters the prompting baselines and understates the symbolic           changed, and after the iteration budget reports the in-
route’s relative value. Third, the symbolic pipeline issues sev-        stance infeasible, which is correct.
eral model calls per problem against one or two for prompt-
ing, so its accuracy parity comes at a compute premium that         This is the mechanism behind the aggregate numbers: a bare
we do not chart in detail. Fourth, the scheduling failure is        verdict invites the model to dissolve the conflict by dropping
reported under a fixed prompt, and a different prompt or a          a true constraint, while the core makes “the problem is infea-
worked counting example might narrow it, so the per-domain          sible” the better-supported response.
diagnosis should be read as a property of this configuration
rather than a law of autoformalization.                             References
                                                                    [AhmadiTeshnizi et al., 2024] Ali AhmadiTeshnizi, Wenzhi
9   Conclusion                                                         Gao, and Madeleine Udell. OptiMUS: Scalable opti-
                                                                       mization modeling with (MI)LP solvers and large lan-
We replaced the error message in a language-model plus
                                                                       guage models. In Proceedings of the 41st Interna-
solver repair loop with a proof: when the generated program
                                                                       tional Conference on Machine Learning (ICML), 2024.
is unsatisfiable, we hand the model a minimal unsatisfiable
                                                                       arXiv:2402.10172.
core over its own constraints. On 77 constraint and opti-
mization problems and two open-weight models, the resulting         [Chen et al., 2024] Xinyun Chen, Maxwell Lin, Nathanael
pipeline is faithful on six of seven domains, repairs monoton-         Schärli, and Denny Zhou. Teaching large language mod-
ically, and uses the core exactly where weaker models would            els to self-debug. In International Conference on Learning
otherwise hallucinate feasibility. The same study shows that           Representations (ICLR), 2024. arXiv:2304.05128.
symbolic offloading does not beat a strong chain-of-thought         [Gao et al., 2023] Luyu Gao, Aman Madaan, Shuyan Zhou,
baseline on accuracy at verifiable scales; its value is that it        Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan, and
never fabricates a solution and certifies the answers it does re-      Graham Neubig. PAL: Program-aided language models.
turn. We read these results as an argument to treat solver-side        In Proceedings of the 40th International Conference on
proof artifacts as first-class feedback for language-model for-        Machine Learning (ICML), 2023. arXiv:2211.10435.
malization, and we release the benchmark and oracle to make
the scale question sharper.                                         [Gebser et al., 2008] Martin Gebser, Jörg Pührer, Torsten
                                                                       Schaub, and Hans Tompits. A meta-programming tech-
                                                                       nique for debugging answer-set programs. In Proceedings
A    Repair feedback and a worked trace                                of the 23rd National Conference on Artificial Intelligence
The two repair settings share the pipeline, the model, and the         (AAAI), pages 448–453, 2008.
iteration budget, and differ only in the feedback returned on       [Gebser et al., 2012] Martin Gebser, Roland Kaminski, Ben-
an UNSAT outcome. The generic setting returns the raw ver-             jamin Kaufmann, and Torsten Schaub. Answer Set Solving
dict:                                                                  in Practice. Synthesis Lectures on Artificial Intelligence
clingo found no answer set (unsatisfiable).                            and Machine Learning. Morgan & Claypool Publishers,
                                                                       2012.
The typed-core setting returns the minimal core and the deci-
                                                                    [Gebser et al., 2019] Martin Gebser, Roland Kaminski, Ben-
sion it implies:
                                                                       jamin Kaufmann, and Torsten Schaub. Multi-shot ASP
The following integrity constraints are JOINTLY                        solving with clingo. Theory and Practice of Logic Pro-
UNSATISFIABLE (a minimal conflicting set):
  - :- assign(X,C),assign(Y,C),border(X,Y).                            gramming, 19(1):27–82, 2019. arXiv:1705.09811.
If one of them misformalizes the problem,
correct or remove it; if the problem is
                                                                    [Junker, 2004] Ulrich Junker. QUICKXPLAIN: Preferred
genuinely infeasible, leave it unchanged.                              explanations and relaxations for over-constrained prob-
   lems. In Proceedings of the 19th National Conference on
   Artificial Intelligence (AAAI), pages 167–172, 2004.
[Lifschitz, 2008] Vladimir Lifschitz. What is answer set pro-
   gramming? Proceedings of the AAAI Conference on Arti-
   ficial Intelligence, 2008.
[Madaan et al., 2023] Aman Madaan, Niket Tandon, Prakhar
   Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri
   Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang,
   Shashank Gupta, Bodhisattwa Prasad Majumder, Kather-
   ine Hermann, Sean Welleck, Amir Yazdanbakhsh, and
   Peter Clark. Self-refine: Iterative refinement with self-
   feedback. In Advances in Neural Information Processing
   Systems (NeurIPS), 2023. arXiv:2303.17651.
[Olausson et al., 2023] Theo Olausson, Alex Gu, Ben Lip-
   kin, Cedegao Zhang, Armando Solar-Lezama, Joshua
   Tenenbaum, and Roger Levy. LINC: A neurosymbolic ap-
   proach for logical reasoning by combining language mod-
   els with first-order logic provers. In Proceedings of the
   2023 Conference on Empirical Methods in Natural Lan-
   guage Processing (EMNLP), 2023.
[Pan et al., 2023] Liangming Pan, Alon Albalak, Xinyi
   Wang, and William Yang Wang. Logic-LM: Empowering
   large language models with symbolic solvers for faithful
   logical reasoning. In Findings of the Association for Com-
   putational Linguistics: EMNLP 2023, pages 3806–3824,
   2023. arXiv:2305.12295.
[Ramamonjison et al., 2023] Rindra Ramamonjison, Timo-
   thy T. Yu, Raymond Li, Haley Li, Giuseppe Carenini,
   Bissan Ghaddar, Shiqi He, Mahdi Mostajabdaveh, Amin
   Banitalebi-Dehkordi, Zirui Zhou, and Yong Zhang.
   NL4Opt competition: Formulating optimization problems
   based on their natural language descriptions. In Proceed-
   ings of the NeurIPS 2022 Competitions Track, PMLR vol.
   220, 2023. arXiv:2303.08233.
[Shinn et al., 2023] Noah Shinn, Federico Cassano, Edward
   Berman, Ashwin Gopinath, Karthik Narasimhan, and
   Shunyu Yao. Reflexion: Language agents with verbal re-
   inforcement learning. In Advances in Neural Information
   Processing Systems (NeurIPS), 2023. arXiv:2303.11366.
[Wei et al., 2022] Jason Wei, Xuezhi Wang, Dale Schuur-
   mans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc
   Le, and Denny Zhou. Chain-of-thought prompting elic-
   its reasoning in large language models. In Advances in
   Neural Information Processing Systems (NeurIPS), 2022.
   arXiv:2201.11903.
[Wu et al., 2022] Yuhuai Wu, Albert Q. Jiang, Wenda Li,
   Markus N. Rabe, Charles Staats, Mateja Jamnik, and
   Christian Szegedy. Autoformalization with large language
   models. In Advances in Neural Information Processing
   Systems (NeurIPS), 2022. arXiv:2205.12615.
[Ye et al., 2023] Xi Ye, Qiaochu Chen, Isil Dillig, and
   Greg Durrett. SatLM: Satisfiability-aided language mod-
   els using declarative prompting. In Advances in Neu-
   ral Information Processing Systems (NeurIPS), 2023.
   arXiv:2305.09656.
