                                                     Neurosymbolic Auditing of Natural-Language
                                                              Software Requirements


                                                                 Bethel Hall                                 William Eiers
                                                       Stevens Institute of Technology               Stevens Institute of Technology
                                                           bhall2@stevens.edu                            weiers@stevens.edu
arXiv:2605.13817v1 [cs.SE] 13 May 2026




                                                                                         Abstract
                                                     Natural-language software requirements are often ambiguous, inconsistent, and
                                                     underspecified; in safety-critical domains, these defects propagate into formal
                                                     models that verify the wrong specification and into implementations that ship
                                                     unsafe behavior. We show that large language models, equipped with an SMT
                                                     solver, can audit such requirements: translating them into formal logic, detecting
                                                     ambiguity through stochastic variation in the generated formalization, and exposing
                                                     inconsistency, vacuousness, and safety violations through solver queries on the
                                                     resulting specification. We present V ERI M ED, a neurosymbolic pipeline that
                                                     operationalizes this idea for medical-device software requirements, and report two
                                                     findings. First, stochastic variation across independent formalizations is a signal
                                                     of ambiguity: requirements that admit multiple plausible interpretations produce
                                                     SMT-inequivalent formalizations, and bidirectional SMT equivalence checking
                                                     turns this disagreement into a solver-checkable test. Second, the usefulness of
                                                     symbolic feedback depends on its granularity: in counterexample-guided repair on a
                                                     hemodialysis question-answering benchmark, concrete SMT counterexamples raise
                                                     verified accuracy from 55.4% to 98.5%. Over an extensive experimental evaluation
                                                     on open-source hemodialysis safety requirements, we show that the LLM-based
                                                     approach in V ERI M ED successfully reduces ambiguity-sensitive requirements and
                                                     enables rigorous auditing of software requirements through SMT-based queries.


                                         1    Introduction
                                         Autoformalization, the translation of natural-language requirements into machine-verifiable spec-
                                         ifications, has advanced rapidly with large language models [28]. Yet for safety-critical software
                                         requirements, syntactic validity is not enough. A well-formed formal specification can be globally
                                         inconsistent, contain requirements whose trigger conditions are unreachable, or admit multiple plausi-
                                         ble readings of the same natural-language source. These failures are invisible by construction: when
                                         no ground-truth formalization exists, there is no oracle for correctness. This is inherent to LLM-
                                         generated formalizations, where the model resolves ambiguity by defaulting to the most statistically
                                         common reading in its training distribution or omits constraints implicit in the source.
                                         This problem is especially acute in domains such as medical devices, where requirements specify
                                         alarm conditions, pump behavior, and safe parameter ranges. If the requirement set is inconsistent, or
                                         if the autoformalizer silently picks one reading among several, downstream verification can succeed
                                         while checking the wrong specification entirely. To address this, we propose V ERI M ED, a neurosym-
                                         bolic framework that makes these failures detectable through two complementary checks. First, we
                                         audit the generated specification with solver queries that check global consistency, vacuousness,
                                         violatability, and redundancy at the requirement level, producing diagnostic flags that localize struc-
                                         tural defects to specific requirements. Second, we detect and resolve ambiguity in the source text by
                                         exploiting the stochasticity of LLM-based autoformalizers as a diagnostic signal: sampling multiple
                                         independent SMT formalizations of the same requirement and comparing them with bidirectional

                                         Preprint.
SMT equivalence checking; persistent disagreement signals that the natural-language requirement
admits more than one plausible reading. When defects are detected, we execute a targeted repair
through a neurosymbolic feedback loop: solver feedback guides re-formalization for structural de-
fects, and SMT-derived witnesses guide natural-language clarification for ambiguous requirements.
The final requirement is then surfaced to the user for manual edits.
Our contributions are as follows:
• We introduce a neurosymbolic framework for analyzing natural-language software requirements.
  The system, V ERI M ED, autoformalizes requirements into a single SMT model and uses the solver’s
  output as the primary signal for downstream review.
• We formulate four requirement-level SMT audits — global consistency, vacuousness, violatability,
  and redundancy — that operationalize established requirement-quality criteria. Applied to a
  published hemodialysis specification, the audits flagged 2 of 64 requirements as redundant.
• We show that the quality of solver feedback determines the effectiveness of LLM repair. In
  requirement-grounded question answering, using the violated requirements as feedback alone
  raises verified accuracy from 55.4% (no feedback) to 80.0%; providing an SMT counterexample as
  additional feedback raises accuracy to 98.5%.
• We introduce ambiguity detection via bidirectional SMT inequivalence across independently
  sampled formalizations, using solver-generated witnesses to drive clarification. To our knowledge,
  this is the first application of solver-checked sample disagreement to software requirements analysis.
  On the hemodialysis benchmark, the procedure flagged 12 of 64 requirements (18.8%) as producing
  multiple distinct encodings; all 12 converged to a single encoding after clarification.

2     Methodology
2.1   Problem Formulation

Let R = {r1 , . . . , rn } be a set of natural-language software requirements. We translate R into a
single SMT model M and use M to answer three classes of queries: requirement-level audits, query
verification against scenario-based safety questions, and ambiguity detection over the source text.
Encoding. Let T denote the translation from a requirement ri to a formal encoding ρi = T (ri ). Most
safety requirements take a conditional form: “if condition P holds, then action Q must follow.” We
encode each such requirement as ρi (x) ≡ pi (x) ⇒ qi (x), where x denotes the typed state variables
of the system (Boolean control states and real-valued device parameters) and pi , qi are quantifier-free
formulas over Booleans and linear real arithmetic. Invariant requirements, those that must hold
unconditionally, are encoded directly as state predicates ρi (x) with no antecedent. We also maintain
a set of global domain constraints C(x) encoding background factsVshared across all requirements,
                                                                        n
such as flow rates being non-negative. The full model is M = C ∧ i=1 ρi .
Audit queries. We define four solver queries over M that characterize the requirement set.
1. Global consistency asks whether M is satisfiable. If M is unsatisfiable, the requirements are
   mutually inconsistent, and an unsat core identifies a conflicting subset for repair.
2. Vacuousness applies to conditional requirements and asks whether the triggering condition pi (x)
   can ever hold under the domain constraints. We check this by asking whether C ∧ pi (x) is
   satisfiable. If it is unsatisfiable, ri never applies and is therefore vacuous. Invariant requirements
   have no antecedent and are not subject to this check.
3. Violatability asks whether a requirement can be broken within the domain. We check C ∧ pi (x) ∧
   ¬qi (x) for conditional requirements and C ∧ ¬ρi (x) for invariants; a satisfiable result returns a
   concrete violating assignment; an unsatisfiable result indicates that the violation is already ruled
   out by the domain constraints alone. V
4. Redundancy asks whether M\i = C ∧ j̸=i ρj already enforces ri . We check M\i ∧pi (x)∧¬qi (x)
   for conditional requirements and M\i ∧ ¬ρi (x) for invariants; unsatisfiability in either case
   confirms redundancy, and the unsat core identifies the subsuming requirements.
Query verification. Given a scenario-based safety question translated into a formal claim ϕ, we ask
whether ϕ is supported by the requirements by checking the formula M ∧ ¬ϕ. If it is unsatisfiable,
M |= ϕ and the claim is entailed; if it is satisfiable, the solver returns a counterexample showing a
state consistent with M but inconsistent with ϕ, which is then used as feedback for repair.


                                                   2
                                      Figure 1: Architecture of V ERI M ED.




Figure 2: Ambiguity-resolution loop with a dialysate-temperature example. V ERI M ED samples
N = 5 independent formalizations and compares them via bidirectional SMT equivalence. Here, ρ1 ,
ρ2 , and ρ3 express different boundary interpretations of the same temperature range: ρ1 excludes both
endpoints, ρ2 includes both endpoints, and ρ3 excludes 33◦ C but includes 40◦ C. The solver returns
concrete disagreement witnesses (e.g., 33◦ C, 40◦ C), which the LLM uses to rewrite the requirement
with explicit boundary semantics. The loop repeats until all samples are semantically equivalent, then
surfaces the clarified requirement for the user to review.


Ambiguity detection. The previous queries treat M as fixed; we now consider whether M itself
is well-determined by the source requirements. A natural-language requirement may admit more
than one plausible reading, and the formalizer may silently commit to one. We define ambiguity
operationally through agreement across independently sampled formalizations. Given two candidate
encodings ρai and ρbi of ri , we say they agree if both C ∧ (ρai ∧ ¬ρbi ) and C ∧ (ρbi ∧ ¬ρai ) are
unsatisfiable. If the first is satisfiable, the witnessing assignment exposes a state allowed by ρai but
ruled out by ρbi ; if the second is satisfiable, the witness exposes a state allowed by ρbi but ruled out by
ρai . We sample N formalizations of ri and apply this pairwise check; a requirement that produces
more than one distinct encoding under bidirectional agreement is flagged as ambiguity-sensitive, and
the witnesses guide natural-language clarification. A requirement whose samples all agree is treated
as admitting a single formalization under repeated sampling.

2.2   Approach

We introduce V ERI M ED1 , a neurosymbolic framework for turning natural-language software require-
ments into a solver-checkable specification. V ERI M ED couples an LLM-based autoformalizer with
an SMT solver to run the audit, query verification, and ambiguity checks defined in Section 2.1. A
   1 Code and data will be released upon acceptance of the paper.




                                                            3
           Variable     Type   Description       NL If bolus is active and infused volume exceeds 400 mL,
           bolus_active Bool   Bolus active     the alarm shall activate.
  Schema
           volume       Real   Volume (mL)
           alarm_active Bool   Alarm active      SMT (=> (and bolus_active (> volume 400.0))
                                                alarm_active)


      Figure 3: Example variable schema and SMT encoding generated from a requirement.

central design choice is that all requirements are expressed in the same symbolic namespace. We
define a fixed schema of typed state variables, covering Boolean control states and real-valued device
parameters, together with the domain constraints C(x). The schema is injected into every LLM
prompt, ensuring independently generated assertions compose into a single model M .
V ERI M ED operates as a four-stage pipeline as shown in Figure 1: the Ambiguity Resolver screens
each requirement for stable formalization before the requirement is formalized; the Autoformalizer
translates the requirement set into SMT-LIB; the Property Verifier audits the resulting model; and
the Query Verifier checks proposed answers to scenario-based safety questions against the model.
 A Ambiguity Resolver. Natural-language requirements are prone to ambiguity [22]: an LLM
autoformalizing an ambiguous requirement may silently commit to one reading among several.
The Ambiguity Resolver screens each requirement before it enters the formalization pipeline. For
each ri ∈ R, it samples the LLM N times at elevated temperature to obtain candidate encodings
ρ1i , . . . , ρN
               i and applies the bidirectional agreement check defined in Section 2.1 to every pair. A
requirement that produces more than one distinct encoding is flagged as ambiguity-sensitive: the
witnessing assignments from the disagreeing pairs are surfaced as concrete distinguishing states, and
the LLM is prompted to rewrite the source text until the samples converge. Only requirements that
pass screening are forwarded to the Autoformalizer. Figure 2 illustrates the clarification loop.
 B Autoformalizer. The Autoformalizer translates the disambiguated requirement set into a single
SMT-LIB specification [5]. The LLM receives the requirement set together with the canonical
schema and the domain constraints, and produces the requirement predicates ρ1 , . . . , ρn along with
the declarations needed to assemble M . The output is therefore not a collection of isolated formulas
but a unified model whose assertions can be analyzed jointly. If the generated SMT (e.g., Figure 3) is
malformed or rejected by the solver, the system enters a bounded syntactic repair loop. The solver
error message and the failed output are returned to the LLM as feedback, and regeneration continues
until a syntactically valid model is produced or the retry budget is exhausted. This loop addresses
syntactic faults only; semantic audits are delegated to the Property Verifier.
 C Property Verifier. The Property Verifier runs the four audit queries defined in Section 2.1 over
the assembled model M : global consistency, vacuousness, violatability, and redundancy. For each
requirement, the verifier records the outcome of every applicable check and, when an audit fails,
returns the diagnostic information the solver provides: an unsat core for inconsistency or redundancy,
and a concrete violating assignment for violatability. These diagnostics localize each defect to a
specific requirement or subset of requirements and serve as the input to any downstream repair.
 D Query Verifier. The Query Verifier tests whether a proposed answer is entailed by M under a
given scenario. A scenario extractor maps the question to a structured state assignment s, an action
generator produces a schema-constrained candidate answer a, and the verifier issues the entailment
query M ∧ s ∧ ¬a. Unsatisfiability confirms entailment by the requirements under the scenario
and is accepted; a satisfiable result returns a counterexample exposing a state consistent with M
and s but inconsistent with a. A secondary check identifies the specific requirements violated in
the counterexample, and a response builder translates the result into a natural-language explanation.
When a violation is found, the repair loop re-prompts the LLM with the violated requirements and, in
the counterexample-guided variant, the solver counterexample itself.

2.3   Experimental Setup

Domain and benchmark. We evaluate V ERI M ED on the hemodialysis machine case study of
Mashkoor [19], using a corpus of 64 natural-language safety requirements drawn from the software
requirements specification. The requirements cover alarm conditions, flow constraints, connectivity
constraints, and numeric limits across multiple machine phases and subsystems.


                                                  4
Schema, formalism, and solver. All experiments share the same canonical typed schema and the
same global domain constraints C(x). The schema contains 85 typed variables covering Boolean
machine states and real-valued device parameters. All formalizations are expressed in SMT-LIB2
over quantifier-free linear real arithmetic with Booleans. We use Z3 [11] for all SMT checks.
Language models. The primary LLM is claude-sonnet-4-6, used for SMT generation, an-
swer generation, and repeated formalization across all experiments. Temperature is 0 for de-
terministic outputs (answer generation and repair), 1.0 for ambiguity detection (exposing alter-
native encodings), and 0.2 for clarification of ambiguous requirements. A secondary model,
claude-haiku-4-5-20251001, is used at temperature 0 for the lightweight answer-to-assignment
translation step, with a rule-based fallback parser if translation fails. SMT generation uses a 16,384-
token output budget and a syntactic repair loop of up to five retries. LLM calls are stateless: each call
reconstructs the full prompt, with explicit repair feedback appended when applicable.


2.4   Experiment 1: Requirement Autoformalization

Before any audit can be trusted, the formalization must be trustworthy. This experiment evaluates
whether V ERI M ED can translate the 64 hemodialysis safety requirements into a single solver-
checkable SMT model that is semantically faithful to the source, covering generation quality, round-
trip fidelity, and sensitivity to requirement-level faults.
Setup: Generation. The Autoformalizer receives the full requirement set together with the canonical
typed schema and produces the complete SMT-LIB model in a single batch translation, rather than
encoding each requirement independently. If the generated output fails to parse or is rejected by Z3,
the autoformalizer regenerates with the solver’s error message as feedback, capped at five retries. We
then run the four audit queries from Section 2.1 over the assembled model.
Round-trip semantic equivalence check. To test whether the generated SMT is semantically faithful
to the source requirements, following the round-trip faithfulness check approach of Amrollahi et
al. [3], we run a round-trip translation cycle. The generated model is first translated back into
structured natural-language requirements which are then re-formalized under the same canonical
schema. Each reconstructed formula is compared to its original under bidirectional SMT equivalence.
We also report the mean cosine similarity between original and reconstructed requirement texts using
normalized embeddings from all-mpnet-base-v2.
Mutation stress test. To test model sensitivity to requirement-level faults, we construct 256 mutated
requirements spanning four fault categories drawn from FDA MAUDE adverse-event reports for
hemodialysis machines [24]: false-alarm trigger suppression, mode-transition guard removal, value
mismatch, and limit violation. Each mutated requirement is compared against the canonical model
using bidirectional SMT equivalence; a mutation is detected if either direction returns SAT.
Metrics. We report parse success rate, the four requirement-level audit outcomes, round-trip equiva-
lence and mean cosine similarity, and per-category and overall mutation detection rates. Binomial
rates are reported with two-sided Wilson 95% confidence intervals.
Result and Insight. The results are shown in Table 1. The Autoformalizer produced a solver-
checkable SMT model covering all 64 requirements on the first generation attempt. The resulting
model was globally consistent and contained no vacuous requirements; 2 requirements were redun-
dant under the rest of the specification. All 64 requirements survived the round-trip check: every
reconstructed requirement re-formalized to a bidirectionally equivalent formula, with mean cosine
similarity of 96.2% between original and reconstructed texts. Under mutation testing, the audit
pipeline detected 249 of 256 single-requirement mutations (97.3%, Wilson 95% CI [94.5%, 98.7%])
across the four fault categories. Observation: Natural-language safety requirements contain
latent defects that solver-level checks make visible. Our approach flagged r11 and r56 as redundant.
For r11 , the unsat core contains r55 : r11 concerns venous pressure falling below its lower limit, while
r55 requires venous pressure to remain at least 22.5 mmHg above that limit, making r11 ’s trigger
unreachable. For r56 , the unsat core contains r42 : r56 concerns dialysate conductivity outside the
permissible range, while r42 requires conductivity to stay between 12.5 and 16.0 mS/cm. These
requirements are not locally vacuous under the domain constraints alone; their guards are satisfiable
against C. They become redundant only once the surrounding requirements are added. This makes
redundancy a review signal rather than a verdict: the engineer should inspect whether the subsuming


                                                   5
Table 1: Experiment 1 results. (a) Audit and round-trip results on 64 requirements. (b) Mutation
stress test on 256 mutated cases. RT = round-trip; CIs are Wilson 95% for binomial rates.
  Metric                   Frac.      %           95% CI
                                                                   Mutation type         Frac.         %            95% CI
  Requirements covered    64/64      100.0     [94.3, 100.0]
                                                                   False alarm          64/64        100.0       [94.3, 100.0]
  Non-vacuous (cond.)     39/39      100.0     [91.0, 100.0]
                                                                   Mode transition      63/64         98.4        [91.7, 99.7]
  Violatable              64/64      100.0     [94.3, 100.0]
                                                                   Value mismatch       62/64         96.9        [89.3, 99.1]
  Redundant                2/64       3.1       [0.9, 10.7]
                                                                   Limit violation      60/64         93.8        [85.0, 97.5]
  RT equivalence          64/64      100.0     [94.3, 100.0]
                                                                   Overall             249/256        97.3        [94.5, 98.7]
  RT cosine sim. (mean)     —        96.2           —
                                                                                     (b) Mutation stress test.
                   (a) Audit and round-trip.




requirement is intentionally ruling out the condition, or whether one of the requirements is too strong.
Details anaylysis on the redundancy is provided in Appendix B.
Generalizability. To test whether the round-trip results transfer beyond the hemodialysis benchmark,
we applied the same pipeline end-to-end to an open-source PCA (patient-controlled analgesia)
pump specification with 144 requirements: the autoformalizer produced an SMT model from the
new requirement set, and the round-trip check ran on that model. The cycle reconstructed all 144
requirements; initial bidirectional SMT equivalence held for 135 of 144 (93.75%), and a single repair
iteration closed the remaining 9 cases, reaching full equivalence (144/144). Mean cosine similarity
between original and reconstructed requirement texts was 0.87, lower than the hemodialysis result,
with the largest textual gaps concentrated in compliance-related requirements where reconstruction
paraphrased more aggressively. Despite the lexical drift, the repaired re-formalizations recovered the
original SMT semantics exactly. Details of the audited redundant requirements are in Appendix B.


2.5   Experiment 2: Counterexample-Guided Repair (CEGR)

We evaluate whether SMT feedback repairs incorrect LLM answers about mandatory machine actions,
and in particular whether concrete counterexamples drive more repair than symbolic feedback alone.
Setup. We evaluate on 65 scenario-based safety questions derived from the HD machine case study,
drafted with LLM assistance and reviewed manually to ensure that each question maps to a specific
requirement subset and a solver-verifiable answer. Each question describes a concrete machine state
and asks what mandatory device actions follow. The benchmark contains single-requirement queries
(29), multi-requirement queries (15), and no-requirement queries (21). For each question, the LLM
produces a structured JSON answer constrained to schema variables relevant to that question. Given
model M , scenario s, and candidate answer a, the verifier checks M ∧ s ∧ ¬a, labeling results SAFE
(UNSAT, no counterexample exists), VIOLATION (SAT, a counterexample exists), or UNKNOWN. Only
SAFE answers are counted as correct. All conditions use the same prompt, answer format, and verifier,
differing only in rejection feedback: baseline (no feedback), self-repair (generic rejection message),
requirement feedback only (violated requirements only), full CEGR (violated requirements and Z3
counterexample witness). Each condition has one initial attempt and up to five repair iterations.
Metrics. We report first-attempt accuracy (pass@1), final accuracy after the repair budget, and repair
success rate. Accuracy is the fraction of questions labeled SAFE by the verifier. Repair success rate is
the fraction of initially non-SAFE answers that become SAFE within the repair budget.
Result and Insight. Figure 4 shows the results. CEGR achieves 98.5% final accuracy, exceeding the
no-feedback baseline (55.4%), self-repair (58.5%), and requirement-only feedback (80.0%). First-
attempt accuracy is comparable across conditions (baseline 49.2%, self-repair 53.8%, requirement-
only 46.2%, CEGR 46.2%); the divergence emerges entirely from repair behavior. Repair success rate
follows the same pattern: 12.1%, 10.0%, 59.4%, and 97.1%, respectively. The 18.5-point gap between
requirement-only feedback and full CEGR shows that the counterexample, not solver feedback in
general, is what drives repair: returning a concrete witness state lets the LLM localize the fault in its
previous answer in a way that violated requirements alone do not. Observation: With the LLM
and prompt held fixed, the choice of feedback signal impacts repair outcomes. First-attempt
accuracy across the four conditions ranged narrowly from 46.2% to 53.8%. After up to five repair
iterations, final accuracy ranged from 55.4% to 98.5%, and repair success rate from 10.0% to 97.1%.
The conditions differed only in what the verifier returned after a rejected answer, so the spread is
attributable to the feedback signal. See Appendix 6 for a sample of questions and verified responses.


                                                               6
Figure 4: Effect of verifier feedback on question answering. (Left) accepted on the first attempt, fixed
during repair, and rejected after the repair budget. (Right) Cumulative SMT-verified accuracy.




Figure 5: Mutation Detection. (Left) detection outcomes by fault type: circles denote a detected
mutant, a red cross denotes the single missed mutant. (Right) benchmark composition by fault type.


2.6   Experiment 3: End-to-End Fault Detection

Experiment 1 showed that the canonical SMT model distinguishes mutated formulas under bidi-
rectional equivalence. This experiment tests the complementary claim: whether the full pipeline,
including re-autoformalization, catches faults injected one at a time into the requirement set.
Setup. For each of the 64 hemodialysis requirements ri , we manually write a mutated natural-
language version rimut representing a plausible safety defect: a changed threshold, a weakened
trigger condition, or an incorrect control action. We autoformalize each mutated requirement into
a mutant SMT block ρmut i , and construct the modified model M
                                                                 (i)
                                                                     by replacing ρoriginal
                                                                                   i        with ρmut
                                                                                                  i
in the canonical model while keeping the shared schema, the global domain constraints C, and the
remaining 63 requirement blocks fixed.
Evaluation. A fault is detected if either of two conditions holds: (a) the modified model M (i) is
globally inconsistent, indicating that rimut contradicts the original requirements; or (b) the mutant and
original requirements are semantically distinguishable, checked by bidirectional satisfiability between
ρmut
 i   and ρoriginal
           i       under C. We test whether C ∧ ρmut i    ∧ ¬ρoriginal
                                                               i       is satisfiable (the mutant permits a
behavior ruled out by the original requirement) and whether C ∧ ρoriginal  i      ∧ ¬ρmut
                                                                                        i  is satisfiable (the
original requirement allows a behavior ruled out by the mutant); a satisfiable result in either direction
signals detection. This disjunction separates faults that produce immediate contradictions from faults
that remain satisfiable but still change the intended safety behavior.
Result and Insight. Figure 5 shows the complete result: V ERI M ED detected 63 of 64 inserted
defects (98.4%, Wilson 95% CI [91.7%, 99.7%]). All 64 mutated requirement sets autoformalized
successfully and remained globally satisfiable, so detection came entirely from comparing original
and mutated encodings. Detection was complete for limit violations (34/34), mode-transition changes
(24/24), and false-alarm changes (2/2). For value mismatches, 3 of 4 mutants were detected; the
missed case was the mutant for r2 , which was indistinguishable from the original under the current
schema. Observation: Consistency alone does not always catch requirement faults. Every
mutated specification remained globally satisfiable, yet 63 of 64 defects were detected. The r20
mutant shows why: the original requires disconnection and an alarm when dialysate temperature
falls below 33◦ C; the mutant requires the opposite. Both are still globally satisfiable, but only the


                                                      7
Figure 6: Ambiguity detection and resolution via repeated autoformalization. (A) Share of require-
ments flagged as ambiguity-sensitive versus non-ambiguous. (B) Distinct SMT encodings per flagged
requirement, ranked by count. (C) Ambiguity-sensitive count across five rounds of SMT-guided
clarification. (D) Pairwise SMT agreement.


original reflects the intended safe behavior. Internal consistency alone is therefor insufficient; the
useful signal is behavioral preservation.

2.7   Experiment 4: Ambiguity Resolution

We evaluate whether the SMT-solver feedback can be used not only to detect ambiguous requirements,
but also to reduce ambiguity in the natural-language specification.
 Setup: We apply the Ambiguity Resolver (Section 2.2) to all 64 hemodialysis requirements with
 N = 5 samples per requirement. Requirements that remain ambiguity-sensitive after clarification are
 re-screened; the clarified requirements are stitched back into the full 64-requirement set. Result and
 Insight: Figure 6 shows the results. 12 out of the 64 requirements were flagged as ambiguity-sensitive
 (18.8%, CI [11.1%, 30.0%]); pairwise SMT agreement across all formalization pairs is 44.0% (CI
 [41.7%, 46.3%]). After SMT-guided clarification, ambiguity-sensitive requirements drop to 0/64
 (0.0%, CI [0.0%, 5.7%]) and pairwise SMT agreement reaches 100% (CI [99.4%, 100.0%]), with
 mean distinct encodings per requirement falling from 1.59 to 1.00. All 320 clarified formalizations
 remain syntactically valid and locally verified, confirming that the clarification loop eliminates
 encoding ambiguity without introducing inconsistency. Observation: SMT disagreement across
 samples flags requirements that the formalizer reads in more than one way. One recurring source
 of ambiguity is overlapping numeric ranges: R-24 and R-25 [19] specify air-detection thresholds for
“0 to 200 mL/min” and “200 to 400 mL/min,” leaving the endpoint 200 ambiguous. The autoformalizer
 split on this, producing encodings that disagreed at exactly 200 mL/min. Solver-generated witnesses
 surfaced each such disagreement as a concrete state, and the clarification loop converged on a single
 reading for every flagged requirement (see Appendix 5 for the full list).


3     Limitations

Generalizability. Our evaluation targets hemodialysis machine requirements, with a secondary
evaluation on a PCA pump specification (Appendix A). Both are infusion-related medical devices
with shared structural features. We cannot establish that our findings transfer to structurally different
device classes or to non-medical domains, and we make no such claim.
Faithfulness. Our approach does not directly measure whether an LLM-generated formalization is
fully faithful to the intent of the original requirement. That is a non-trivial challenge. Instead, we
use a collection of proxy signals, including consistency, mutation sensitivity, ambiguity detection,
round-trip similarity, and downstream repair performance. These signals are useful but incomplete: a
formalization can pass some of them while still missing subtle aspects of the intended meaning.
Temporal Requirements. A further limitation of our work is temporal expressiveness. Since we use
SMT as our core formalism, temporal requirements are modeled using current state conditions rather
than a full temporal logic. For example, requirements such as “the blood pump stops and remains


                                                   8
stopped” or “after 400 mL have been reinfused, the alarm shall activate” are approximated in terms of
the current system state instead of temporal relations across states.
Scalability and Deployment Risk. Industrial medical software requirements documents are often an
order of magnitude larger than the datasets used in this work. The result of this work should not be
used in safety-critical applications without independent review by experts.


4   Related Work

Autoformalization Since [28] demonstrated LLM-based autoformalization for mathematical the-
orems, neurosymbolic research has focused on combining autoformalization with downstream
verification [1, 7, 17, 28]. However, the autoformalization step itself is rarely scrutinized. In particu-
lar, existing work rarely evaluates whether the generated formalizations are consistent, correct, and
unambiguous as specifications [14, 23, 29]. Prior work on autoformalization has largely focused on
mathematical domains, where formal statements are well-defined and can be verified against proofs
[2, 10, 16]. However, V ERI M ED operates on natural language software requirement specifications:
theorems are self-contained and unambiguous by construction, while natural-language requirements
often contain underspecification and ambiguity that the formalization step must surface rather than
ignore. V ERI M ED addresses both gaps: it checks the correctness of the formalization itself, and uses
verifier feedback to drive repair.
Ambiguity Resolution. Ambiguity is a central obstacle in formalizing natural-language requirements.
Recent work uses LLMs to detect and explain ambiguities [6], or surfaces them directly during code
generation via clarifying questions [20, 26, 27]. These approaches treat ambiguity as a textual property
to flag or paraphrase away without deterministic resolution. Our approach forces ambiguities to
manifest in the form of multiple machine-checkable inequivalent encodings of the same requirement.
Requirements Formalization with LLMs. Recent efforts evaluate correctness only at the artifact
level. Cao et al. [9] benchmark ten LLMs across five proof targets, scoring outputs by whether the
checker accepts the output; however, acceptance can conceal incorrect properties. Mandal et al. [18]
synthesize configuration specifications from software manuals, but evaluate only against gold labels
with no semantic check. Beg et al. [8] survey LLM-based specification tools and frame the open
problem as bridging informal natural language and rigorous formal specifications, with no system
closing the loop at the requirement level. V ERI M ED closes this loop, using SMT equivalence between
the original encoding and a re-formalization of the LLM’s own informalization to detect semantic
drift at the requirement level.
Formal Analysis of Medical Device Software Requirements. Medical device software has long
served as a testbed for requirements formalization. The FDA Generic Patient-Controlled Analgesia
infusion pump was formalized as timed automata in UPPAAL by Kim et al. [15], and the hemodialysis
machine case study introduced at ABZ 2016 [19] has since been formalized in Circus [12], Event-B
[13], and Abstract State Machines [4], each constructed manually by formal-methods experts. More
recent LLM-based work has begun to automate this translation: Wang et al. [25] pair Claude 3.5
Sonnet with the ESBMC bounded model checker on nine Lockheed Martin cyber-physical systems.


5   Conclusion and Future Work

We presented V ERI M ED, a neurosymbolic framework for autoformalizing and auditing natural-
language medical-device software requirements with SMT solver feedback. Because software
requirements typically lack a gold formal target, V ERI M ED relies on two solver-grounded signals:
satisfiability queries over the assembled formal model and agreement among independently sampled
formalizations. We show that concrete SMT counterexamples are the strongest repair signal for
requirement-grounded question answering, and that repeated formalization exposes hidden ambiguity.
Future work should extend V ERI M ED to automated schema construction and temporal formalisms.


References
 [1] A. Akinfaderin and S. Subramanian. Verafi: Verified agentic financial intelligence through
     neurosymbolic policy generation. arXiv preprint arXiv:2512.14744, 2025.


                                                    9
 [2] M. Allamanis, S. Panthaplackel, and P. Yin. Unsupervised evaluation of code llms with
     round-trip correctness. arXiv preprint arXiv:2402.08699, 2024.
 [3] D. Amrollahi, J. Lopez, and C. Barrett. Faithful autoformalization via roundtrip verification and
     repair. arXiv preprint arXiv:2604.25031, 2026.
 [4] P. Arcaini, S. Bonfanti, A. Gargantini, and E. Riccobene. How to assure correctness and safety
     of medical software: the hemodialysis machine case study. In International Conference on
     Abstract State Machines, Alloy, B, TLA, VDM, and Z, pages 344–359. Springer, 2016.
 [5] C. Barrett, P. Fontaine, and C. Tinelli. The satisfiability modulo theories library (smt-lib). www.
     SMT-LIB. org, 2:68, 2016.
 [6] S. Bashir, A. Ferrari, A. Khan, P. E. Strandberg, Z. Haider, M. Saadatmand, and M. Bohlin.
     Requirements ambiguity detection and explanation with llms: An industrial study. In 2025 IEEE
     International Conference on Software Maintenance and Evolution (ICSME), pages 620–631.
     IEEE, 2025.
 [7] S. Bayless, S. Buliani, D. Cassel, B. Cook, D. Clough, R. Delmas, N. Diallo, F. Erata, N. Feng,
     D. Giannakopoulou, et al. A neurosymbolic approach to natural language formalization and
     verification. arXiv preprint arXiv:2511.09008, 2025.
 [8] A. Beg, D. O’Donoghue, and R. Monahan. Formalising software requirements with large
     language models. In ADAPT Annual Conference, 2025.
 [9] J. Cao, Y. Lu, M. Li, H. Ma, H. Li, M. He, C. Wen, L. Sun, H. Zhang, S. Qin, et al. From
     informal to formal–incorporating and evaluating llms on natural language requirements to
     verifiable formal proofs. In Proceedings of the 63rd Annual Meeting of the Association for
     Computational Linguistics (Volume 1: Long Papers), pages 26984–27003, 2025.
[10] G. Chen, J. Wu, X. Chen, W. X. Zhao, R. Song, C. Li, K. Fan, D. Liu, and M. Liao. Reform:
     Reflective autoformalization with prospective bounded sequence optimization. arXiv preprint
     arXiv:2510.24592, 2025.
[11] L. De Moura and N. Bjørner. Z3: An efficient smt solver. In International conference on Tools
     and Algorithms for the Construction and Analysis of Systems, pages 337–340. Springer, 2008.
[12] A. O. Gomes and A. Butterfield. Modelling the haemodialysis machine with circus. In
     International Conference on Abstract State Machines, Alloy, B, TLA, VDM, and Z, pages
     409–424. Springer, 2016.
[13] T. S. Hoang, C. Snook, L. Ladenberger, and M. Butler. Validating the requirements and design
     of a hemodialysis machine using iuml-b, bmotion studio, and co-simulation. In International
     Conference on Abstract State Machines, Alloy, B, TLA, VDM, and Z, pages 360–375. Springer,
     2016.
[14] A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu, M. Jamnik, T. Lacroix, Y. Wu, and G. Lample.
     Draft, sketch, and prove: Guiding formal theorem provers with informal proofs. arXiv preprint
     arXiv:2210.12283, 2022.
[15] B. Kim, A. Ayoub, O. Sokolsky, I. Lee, P. Jones, Y. Zhang, and R. Jetley. Safety-assured
     development of the gpca infusion pump software. In Proceedings of the ninth ACM international
     conference on Embedded software, pages 155–164, 2011.
[16] Z. Li, Y. Wu, Z. Li, X. Wei, F. Yang, X. Zhang, and X. Ma. Autoformalize mathematical
     statements by symbolic equivalence and semantic consistency. Advances in Neural Information
     Processing Systems, 37:53598–53625, 2024.
[17] Y. Liu, S. Yu, H. Jin, J. Wen, A. Qian, T. Lee, M. Ramsis, G. W. Choi, L. Qin, X. Liu, et al. A
     multi-agent framework combining large language models with medical flowcharts for self-triage.
     Nature Health, pages 1–10, 2026.
[18] S. Mandal, A. Chethan, V. Janfaza, S. Mahmud, T. A. Anderson, J. Turek, J. J. Tithi, and
     A. Muzahid. Large language models based automatic synthesis of software specifications. arXiv
     preprint arXiv:2304.09181, 2023.


                                                  10
[19] A. Mashkoor. The hemodialysis machine case study. In International Conference on Abstract
     State Machines, Alloy, B, TLA, VDM, and Z, pages 329–343. Springer, 2016.
[20] F. Mu, L. Shi, S. Wang, Z. Yu, B. Zhang, C. Wang, S. Liu, and Q. Wang. Clarifygpt: A
     framework for enhancing llm-based code generation via requirements clarification. Proceedings
     of the ACM on Software Engineering, 1(FSE):2332–2354, 2024.
[21] Ovasicek.   Open PCA pump requirements.     https://ovasicek.github.io/
     pca-pump-ec-artifacts/Open-PCA-Pump-Requirements.pdf, 2016. Accessed: 2026-
     05-07.
[22] M. Q. Riaz, W. H. Butt, and S. Rehman. Automatic detection of ambiguous software require-
     ments: An insight. In 2019 5th International Conference on Information Management (ICIM),
     pages 1–6. IEEE, 2019.
[23] C. Sun, Y. Sheng, O. Padon, and C. Barrett. Clover: Clo sed-loop ver ifiable code generation.
     In International Symposium on AI Verification, pages 134–155. Springer, 2024.
[24] U.S. Food and Drug Administration. MAUDE — manufacturer and user facility device expe-
     rience. https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/search.
     cfm, 2026.
[25] W. Wang, M. Farrell, L. C. Cordeiro, and L. Zhao. Supporting software formal verification with
     large language models: An experimental study. In 2025 IEEE 33rd International Requirements
     Engineering Conference (RE), pages 423–431. IEEE, 2025.
[26] J. J. Wu and F. H. Fard. Humanevalcomm: Benchmarking the communication competence
     of code generation for llms and llm agents. ACM Transactions on Software Engineering and
     Methodology, 34(7):1–42, 2025.
[27] J. J. Wu, M. Chaudhary, D. Abrahamyan, A. Khaku, A. Wei, and F. H. Fard. Can code language
     models learn clarification-seeking behaviors? arXiv preprint arXiv:2504.16331, 2025.
[28] Y. Wu, A. Q. Jiang, W. Li, M. Rabe, C. Staats, M. Jamnik, and C. Szegedy. Autoformalization
     with large language models. Advances in neural information processing systems, 35:32353–
     32368, 2022.
[29] K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil, R. J. Prenger, and
     A. Anandkumar. Leandojo: Theorem proving with retrieval-augmented language models.
     Advances in Neural Information Processing Systems, 36:21573–21612, 2023.




                                                11
Table 2: Round-trip evaluation on the PCA pump requirement set. Formal equivalence is measured
between the original SMT predicates and those obtained by reconstructing requirements from the
model and re-formalizing.
                             Metric                                         Value
                             Requirements reconstructed                   144 / 144
                             Missing requirements                              0
                             Mean cosine similarity                         0.8688
                             Median cosine similarity                       0.8868
                             90th percentile cosine similarity              0.9688
                             Initial formal equivalence              135 / 144 (93.75%)
                             Final formal equivalence after repair   144 / 144 (100.0%)
                             Non-equivalent requirements repaired            9/9
                             Repair attempts needed                            1



A    Generalizability Check: PCA Pump Requirements
To assess whether the round-trip faithfulness evaluation generalizes beyond the hemodialysis bench-
mark, we applied the same evaluator to a second medical device domain: a PCA pump requirement
set [21]. The setup mirrors Experiment 1, we used the same LLM and a similar repair budget of 5
iterations was applied to 144 PCA pump requirements formalized into a separate SMT model.
Textual similarity was high overall: median cosine similarity 0.8868, 90th percentile 0.9688. The
lowest-similarity cases were concentrated in standards, compliance, and security requirements,
where reconstruction paraphrased the source text more aggressively. At the SMT level, 135 of 144
requirements were equivalent on the initial re-formalization pass; the bounded repair loop resolved
all nine remaining mismatches in a single attempt. Common mismatch patterns included enum and
value remapping errors in alarm and infusion-mode encodings, dropped else branches in conditional
behavior, omitted structural constraints from table-driven requirements, and symbolic-versus-literal
substitutions in alarm-table ranges.
These results mirror the HD round-trip findings: textual reconstruction may paraphrase the original
requirement, yet the SMT-level check can still recover the original formal semantics. After bounded
repair, every reconstructed PCA requirement formalized back to a predicate equivalent to the original
in the generated model. This provides evidence that the round-trip evaluator is not specific to the HD
benchmark and can serve as an internal consistency check for autoformalized requirement models
across medical-device domains.

B    Redundancy Analysis

Table 3: The two requirements flagged as redundant by V ERI M ED’s audit (r11 , r56 ), shown alongside
the surrounding requirements that subsume them (r55 , r42 ). Each subsuming requirement appears in
the unsat core of the corresponding redundancy check.
        ID    Requirement
        r11   During initiation, if the pressure at the VP transducer falls below the lower pressure
              limit, the software shall stop the BP and execute an alarm signal.
        r55   The minimum distance between the venous lower pressure limit and the actual VP is
              always at least 22.5 mmHg.
        r56   Bypass mode occurs when the DF conductivity goes beyond permissible limits; the
              dialyzer is separated from the DF flow.
        r42   The DF conductivity parameter must be within 12.5 to 16.0 mS/cm.




                                                         12
                            Table 4: Experimental setup summary. All SMT queries use Z3.
                    Exp      Task                              N     Model                          Temp           Iter. / Samples
                    Exp1     Formalization audit               64    Sonnet 4.6                     default           5 repairs
                    Exp2     Question answering & repair       65    Sonnet 4.6 / Haiku 4.5†           0             5 iterations
                    Exp3     End-to-end fault detection        64    Sonnet 4.6                     default           6 repairs
                    Exp4     Ambiguity detection               64    Sonnet 4.6                   1.0 / 0.2‡       N =5 samples
†
    Haiku 4.5 (temp. 0) for answer-to-schema translation; Sonnet 4.6 for generation and repair.
‡
    Temp. 1.0 for repeated formalization; 0.2 for SMT-guided clarification.


Table 5: Original and clarified natural-language requirements for the 12 requirements whose repeated
formalizations were ambiguity-sensitive before SMT-guided clarification.
    Req.   Before   Final   ∆     Original requirement                                         Clarified requirement
    r3      14        1     -13   To prevent coagulation of blood, the anti-coagulation        To prevent coagulation of blood, the anti-coagulation
                                  pump doses anti-coagulant into the bloodline between         pump doses anti-coagulant into the bloodline between
                                  the BP and the dialyzer at the set rate or set volume        the BP and the dialyzer at exactly the set rate during treat-
                                  during treatment.                                            ment, while the patient is connected and anti-coagulant
                                                                                               delivery is active and not stopped.
    r56      6        1     -5    Bypass mode occurs when the DF conductivity goes             Whenever the DF conductivity goes outside permissible
                                  beyond permissible limits; the dialyzer is separated from    limits (below 12.5 mS/cm or above 16.0 mS/cm), both of
                                  the DF flow.                                                 the following consequences must hold simultaneously:
                                                                                               (1) bypass mode becomes active, and (2) the dialyzer
                                                                                               is disconnected from the DF flow. Both consequences
                                                                                               are required together under this single trigger condition;
                                                                                               neither consequence is optional or independent of the
                                                                                               other.
    r57      6        1     -5    Bypass mode occurs when the DF temperature goes              If the DF temperature is outside permissible limits (be-
                                  beyond permissible limits; the dialyzer is separated from    low 33°C or above 40°C), then bypass mode is active
                                  the DF flow.                                                 and the dialyzer is disconnected from the DF flow.
    r23      4        1     -3    If the flow through the SAD sensor is in the range of 0 to   If the flow through the SAD sensor is greater than or
                                  200 mL/min, then the air volume limit for air detection      equal to 0 mL/min and less than or equal to 200 mL/min,
                                  shall be 0.2 mL.                                             then the air volume limit for air detection shall be 0.2
                                                                                               mL.
    r24      4        1     -3    If the flow through the SAD sensor is in the range of        If the flow through the SAD sensor is greater than 200
                                  200 to 400 mL/min, then the air volume limit for air         mL/min and less than or equal to 400 mL/min, then the
                                  detection shall be 0.3 mL.                                   air volume limit for air detection shall be 0.3 mL.
    r1       3        1     -2    Arterial and venous connectors of the EBC are connected      The arterial connector of the EBC is connected to the
                                  to the patient simultaneously.                               patient if and only if the venous connector of the EBC is
                                                                                               also connected to the patient.
    r32      3        1     -2    If the machine is in the initiation phase and net fluid      If the machine is in the initiation phase and net fluid
                                  removal is enabled and backward rotation of the UFP is       removal is enabled and backward rotation of the UFP
                                  detected, the software shall put the machine in bypass       is detected, the software shall simultaneously put the
                                  and execute an alarm signal. The backward delivered          machine in bypass mode, activate an alarm signal, and
                                  volume shall not exceed 400 mL.                              ensure the backward delivered volume does not exceed
                                                                                               400 mL; all three responses are required together under
                                                                                               these three preconditions.
    r33      2        1     -1    If the machine is in the initiation phase and net fluid      If the machine is in the initiation phase and net fluid
                                  removal is enabled and the net fluid removal volume          removal is enabled and the net fluid removal volume
                                  exceeds (UF set volume + 200 mL), the software shall         exceeds (UF set volume + 200 mL), the software shall
                                  put the machine in bypass and execute an alarm signal.       activate bypass mode and execute an alarm signal.
    r44      2        1     -1    The DF temperature parameter must be within 33 to            The DF temperature setting must be within 33 to 40°C
                                  40°C.                                                        inclusive.
    r58      2        1     -1    If the DF concentration is incorrect, the dialyzer will be   If the DF concentration is incorrect, bypass mode shall
                                  bypassed.                                                    be activated and the dialyzer shall be disconnected from
                                                                                               the DF flow.
    r6       2        1     -1    Once empty dialyzer has been confirmed, the BP cannot        Once empty dialyzer has been confirmed, the blood
                                  be started anymore.                                          pump (BP) cannot be started or kept running anymore.
    r63      2        1     -1    During reinfusion, the BP stops automatically after 400      During reinfusion, the blood pump stops automatically
                                  mL have been reinfused.                                      and remains stopped once 400 mL or more have been
                                                                                               reinfused, meaning the blood pump is not running.




C          Tables




                                                                        13
Table 6: Sample of 10 handcrafted Experiment 2 evaluation questions, covering all three query types.

 Question                                                                             Gold answer

 Single-Requirement Queries
 During initiation, actual blood flow is 90 mL/min, target blood flow is 200          Trigger an alarm.
 mL/min, and bypass mode is inactive. What are all the mandatory machine
 actions? If none are required, answer: "No mandatory machine action."
 During initiation, net fluid removal is enabled and the UFP is rotating backward.    Activate bypass mode
 What are all mandatory machine actions? If none are required, answer: "No            and trigger an alarm.
 mandatory machine action."
 In this machine state, the patient’s blood pressure has dropped. What are all        Activate saline infusion
 mandatory machine actions? If none are required, answer: "No mandatory               and close arterial access.
 machine action."
 During initiation, DF temperature is 43 C. What are all mandatory machine            Disconnect the dialyzer
 actions? If none are required, answer: "No mandatory machine action."                from df flow, activate by-
                                                                                      pass mode, and trigger
                                                                                      an alarm.
 Multi-Requirement Queries
 During initiation, anticoagulant delivery is running, reverse flow has been de-      Stop the blood pump,
 tected, venous pressure is 480 mmHg, and the venous upper pressure limit is 450      stop blood flow, stop
 mmHg. What are all mandatory machine actions? If none are required, answer:          anticoagulant flow, and
 "No mandatory machine action."                                                       trigger an alarm.
 During initiation, net fluid removal is enabled, the UFP is rotating backward, and   Stop df flow to the di-
 the bypass valve is open. What are all mandatory machine actions? If none are        alyzer, activate bypass
 required, answer: "No mandatory machine action."                                     mode, and trigger an
                                                                                      alarm.
 During initiation, anticoagulant delivery is running, reverse flow has been de-      Stop blood flow, stop an-
 tected, and DF temperature is 43 C. What are all mandatory machine actions? If       ticoagulant flow, discon-
 none are required, answer: "No mandatory machine action."                            nect the dialyzer from
                                                                                      DF flow, activate bypass
                                                                                      mode, and trigger an
                                                                                      alarm.
 No-Requirement Queries
 During initiation, actual blood flow is 90 mL/min, target blood flow is 200          No mandatory machine
 mL/min, and bypass mode is active. What are all mandatory machine actions? If        action.
 none are required, answer: "No mandatory machine action."
 During initiation, SAD sensor flow is 500 mL/min, detected air volume is 0.4         No mandatory machine
 mL, and the air volume limit is 0.5 mL. What are all mandatory machine actions?      action.
 If none are required, answer: "No mandatory machine action."
 In this machine state, treatment is still ongoing. What are all mandatory machine    No mandatory machine
 actions? If none are required, answer: "No mandatory machine action."                action.


Reading the table. For each requirement flagged as ambiguity-sensitive in Experiment 6, we report
three counts. The Encodings (orig.) column is the number of distinct SMT-equivalence classes
produced by five independent formalizations of the original requirement: a value of k means the
formalizer read the original requirement in k different ways. The Encodings (final) column is the
same count after the clarification loop has rewritten the requirement; a value of 1 means the formalizer
converged on a single reading. The ∆ column is simply Encodings (final) − Encodings (orig.) and
reports the size of the convergence effect. All twelve clarified requirements reach a single encoding
class, so the ∆ column is determined by the original count.




                                                      14
D      Prompt Templates
Placeholders appear as 〈name〉. Model and temperature settings are in Table 4.

Experiment 1: Autoformalization

System


        You are a FORMAL METHODS ENGINEER specializing in SMT-LIB encoding.
        OUTPUT: Pure SMT-LIB v2 only. No prose, no markdown, no code fences.
        REQUIRED STRUCTURE — five sections:
          ; SECTION 1: DECLARATIONS
          ; SECTION 2: DOMAIN CONSTRAINTS
          ; SECTION 3: REQUIREMENTS AS NAMED PREDICATES
            (define-fun req_<id> () Bool (=> <pre> <post>))
            (define-fun req_<id> () Bool <post>)
          ; SECTION 4: PER-REQUIREMENT CHECKS
            GUARD-SAT: (echo "GUARD-SAT:<id>") (assert <pre>) (check-sat)
            VIOLATABLE: (echo "VIOLATABLE:<id>") (assert (not req_<id>))
        (check-sat)
          ; SECTION 5: GLOBAL CONSISTENCY
            (assert req_r1) ... (echo "GLOBAL-CONSISTENCY") (check-sat)


User


        Produce a complete SMT-LIB v2 file using the structure above.
        REQUIREMENTS:
        〈requirements_json〉
        〈schema_block〉
        Output ONLY SMT-LIB code.



Experiment 2: CEGR

System


        You are answering a hemodialysis machine safety question. State the
        exact
        machine actions that should happen. Return exactly one JSON object and
        nothing
        else. Every action field must be explicitly true or false.


User


        〈variable_definitions〉
        〈relevant_requirements〉
        Scenario:   〈scenario_description〉
        Question:   〈question〉
        Answer using this exact schema:     〈response_schema〉


Repair suffix — appended on failure (CEGR condition)


                                               15
       Your previous response was REJECTED by the formal verifier.
       Violated requirement(s): 〈req_ids〉
       Counterexample:
       〈counterexample_assignments〉
       Conflicts with your previous answer:
       〈conflict_lines〉
       Reconsider and produce a corrected JSON response.


The ablation and self-repair conditions use the same base prompt with the counterexample block removed or
replaced by a generic retry instruction, respectively.

Exp3 — End-to-End Fault Detection

Uses the same system and user prompt as Exp1. The only difference is that one requirement in 〈require-
ments_json〉 is replaced by its LLM-translated mutant before the prompt is sent.

Experiment 4: Ambiguity Resolution & Clarification

System


       You are a formal methods engineer. Translate natural-language
       medical-device
       requirements into SMT-LIB2 assertions. Output only SMT-LIB2 (assert
       ...)
       statements. Do not output prose, markdown, comments, or declarations.



User


       Variables:      〈schema_variable_list〉
       Requirement:       〈requirement_text〉
       Output ONLY (assert ...)           statements.


The clarification prompt extends the above with solver evidence (distinct encoding count, semantic entropy, one
representative formula per equivalence class) and instructs the model to rewrite the requirement minimally until
repeated formalization converges. Full template available in the released code.


E    Compute Resources
All experiments were run on a local CPU workstation using Python and Z3. No local GPU train-
ing or fine-tuning was performed. LLM inference was performed through hosted API calls to
claude-sonnet-4-6; Experiment 2 additionally used claude-haiku-4-5-20251001 for answer-
to-assignment translation. Z3 was run locally on CPU.




                                                      16
