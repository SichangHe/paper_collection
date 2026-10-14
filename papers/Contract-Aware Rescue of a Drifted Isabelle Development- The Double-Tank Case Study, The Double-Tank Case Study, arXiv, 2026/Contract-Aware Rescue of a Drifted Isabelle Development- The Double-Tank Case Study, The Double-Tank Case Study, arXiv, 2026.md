                                             Contract-Aware Rescue of a Drifted Isabelle Development:
                                                         The Double-Tank Case Study

                                                                                          Jim Woodcock
                                                            Southwest University, China; Aarhus University, Denmark; University of York, UK
                                                                                     jim.woodcock@york.ac.uk

                                                                 Gabriel Leite                                    Augusto Sampaio
                                                     Universidade Federal de Pernambuco, Brazil        Universidade Federal de Pernambuco, Brazil
arXiv:2608.18822v1 [cs.SE] 19 Aug 2026




                                                                gnl2@cin.ufpe.br                                  acas@cin.ufpe.br

                                                                                              Ran Wei
                                                                                       Lancaster University, UK
                                                                                      r.wei@lancaster.ac.uk



                                               Large language models can propose proofs for interactive theorem provers, but a successful build
                                               does not show the surrounding verification task was preserved. We study this problem in an Isabelle
                                               development of a sampled-data double-tank controller. The work began with nine theories and ten
                                               unfinished obligations, grew to a 16-theory build without sorry, oops, added axiomatisation, or
                                               oracle use, and accumulated 23 stable and 36 broken proof states. A retrospective audit found material
                                               changes in 16 of the 100 original declarations, including a weakened end-to-end assurance theorem
                                               that assumed three of the four requirements in its conclusion. We used CAPRI, a contract-aware
                                               proof-repair tool, to govern a reconstruction by combining Isabelle acceptance with an independent
                                               check of repository changes against machine-readable edit contracts. The reconstruction discharged
                                               all ten scoped obligations within the original nine-theory structure. A secondary replay by a co-author
                                               reproduced the R10 build, contract checks, control tests, and principal audit findings; independent
                                               replication remains future work. Operational end-to-end verification remains incomplete: we still
                                               need to connect operational executions to the reconstructed quantitative trace contract, a task requiring
                                               an extended contract.

                                         Keywords: Isabelle/HOL; large language models; proof repair; theory drift; automated control systems;
                                         hybrid systems; contract-aware development


                                         1    Introduction
                                         In theorem proving, a result is accepted only if its proof can be checked from the definitions, assumptions,
                                         and previously proven results available to the prover [15]. LLMs can assist by generating proof scripts,
                                         proposing useful lemmas, and revising suggestions in response to prover diagnostics [10, 5, 16, 22]. Proof
                                         checking remains with the theorem prover; the LLM supplies candidate text. Trouble begins when the
                                         model, or an iterative repair tool built around it, can also edit material outside the intended proof body. A
                                         repository can compile after weakening a theorem, adding a convenient assumption, changing a definition
                                         or import, or editing an unrelated file. The formal problem may then differ from the one assigned. Isabelle
                                         still checks the submitted theory correctly, through the LCF-style separation between proof-producing
                                         automation and a small trusted inference kernel [15, 2]; the kernel does not account for which parts of the
                                         repository the developer authorised the repair process to change.

                                                                                                                        © J. Woodcock et al.
                                         Submitted to:
                                                                                                                        This work is licensed under the
                                         Formal Methods for Autonomous Systems 2026
                                                                                                                        Creative Commons Attribution License.
2                                              Contract-Aware Rescue of a Drifted Isabelle Development


     The double-tank development exposes this distinction in a concrete setting. It is based on an earlier
formal design of a double-water-tank controller [20]: two tanks are connected in cascade, a pump controls
the inflow, liquid levels evolve continuously, and a discrete controller acts at periodic samples. The
Isabelle/HOL theories cover the plant, controller, temporal requirements, approximate conformance,
runtime monitoring, and institution-based semantics. We began with nine files containing the vocabulary
and principal theorem statements, leaving the difficult proofs open. We used ChatGPT to explore proof
strategies. It found some successful proofs, alongside many failed attempts involving continuous evolution,
invariant preservation, relational framing, and tolerance transfer.
     The repository eventually contained 16 theories and built without using sorry, oops, added axiomati-
sation, or oracles (collectively, admissions). Later, a comparison with the original outline revealed changes
to definitions, assumptions, boundary conventions, and public claims. Isabelle accepted the resulting
theory, but it no longer matched the initial task in every respect. Three terms distinguish the relevant
boundaries. The theory frame is the set of statements, definitions, assumptions, imports, file structure,
and public claims that delimit the authorised proof task. Theory drift is an accumulation of individually
accepted edits that changes that task without an explicit change of intent. A semantic seam is a boundary
between separately formalised layers that needs an explicit bridge before their meanings can be treated as
connected. Drift may weaken an engineering claim or make an unresolved seam hard to see.
     The paper records the proof-discovery history of the hybrid systems development, including 23 stable
proof states and 36 distinct broken states. The failed candidates influenced later decisions about the model,
its assumptions, and the supporting lemmas, so they form part of the evidence rather than discarded
intermediate work. A declaration-level audit measures the distance between the completed sixteen-theory
repository and the first double-tank outline. Among 100 named declarations, 84 preserved identical formal
content. The remaining 16 differed in declaration kind, definition, assumptions, domain, or boundary
treatment.
     The reconstruction kept the first theory frame while drawing on mathematical results from the larger
repository. Where the semantic chain was incomplete, we named the missing link and assigned it a
successor obligation instead of moving it into the assumptions of the theorem under repair. CAPRI checks
the declared authority boundary, whereas semantic equivalence or modelling adequacy remains a developer
judgement requiring an explicit successor contract when the task changes. The study follows one evolving
double-tank repository and makes no comparison between alternative CAPRI repair configurations.
     We review related work, the double-tank system, its Isabelle development, and the archived proof-
discovery process. Later sections introduce CAPRI, report the drift audit and controlled reconstruction,
and state the remaining operational assurance obligation before discussing the study’s limitations.


2    Related work
Isabelle follows the LCF tradition: automation may search widely, but accepted theorems ultimately
depend on kernel-checked inferences [15]. Sledgehammer reconstructs externally found arguments in
Isabelle [2]; learning-based systems such as Thor, Baldur, GPT-f, and LeanDojo extend proof search or
repair with language models [10, 5, 16, 22]. CAPRI addresses a different question. Given a candidate
repository, it checks whether changes are confined to an authorised edit boundary. This complements proof
transport and maintenance techniques such as Pumpkin Pi and large-scale Isabelle proof engineering [19,
18, 1]: CAPRI does not establish semantic equivalence of an authorised change, but prevents unrecorded
changes to protected statements, definitions, assumptions, imports, and files.
    Theory drift connects to requirements evolution and traceability [14, 9]. Theory change is normal; drift
J. Woodcock et al.                                                                                        3


occurs when accepted edits change the engineering question without an explicit decision or replacement
obligation. Our correspondence map records what changed; CAPRI records which changes were permitted.
    Hybrid-systems assurance provides the application setting, while existing calculi supply the semantic
foundations. Differential dynamic logic, Isabelle-based hybrid predicate-transformers, Isabelle/UTP,
and Hybrid Relations provide relevant foundations [17, 13, 7, 6]. Institution theory, duration calculus,
runtime verification, ModelPlex, and trace-conformance metrics supply related abstractions for semantic
transport, duration, execution monitoring, model-to-execution validation, and bounded implementation
deviation [8, 3, 11, 12, 4]. We study how such semantic choices, requirements, and bridges are protected
during iterative proof work.
    The acceptance decomposition can transfer to other provers: their native checker supplies Build,
while a repository-side policy supplies Conforms. A Lean or Coq port would need prover-specific
adapters for declaration and proof-region location and for dependency/build metadata. The principle is
prover-agnostic; the implementation and evaluation here are Isabelle-specific.


3     The double-tank case study
The case study builds on the double-water-tank of Hong Ki Thae and Dang Van Hung [20]. A pump feeds
the upper tank; water passes into the lower tank and is then discharged. At each sample, the controller
chooses the pump command used during the next continuous phase to track the lower-tank reference while
keeping both levels within their limits. The policy is fixed rather than adaptive. Even this compact plant
brings together continuous dynamics, discrete control, sampling, timing, physical bounds, disturbance
and sensor tolerances, and the gap between a mathematical model and its implementation.
    Between samples, the tank levels follow the plant differential equations. A sampling action records
observations; the controller then applies its fixed policy, updates the pump command, and begins the next
continuous phase. The state includes the pump signal, controller mode, sampled values, target reference,
event information, timing, and the two levels. Lens-based state access from Isabelle/UTP [7] supports
local updates and makes frame conditions explicit. Those frame conditions are essential to the closed-loop
invariant: each proof must account for state components changed by an action and those preserved by it.


3.1   Requirements and assurance argument
The development has four requirements: (1) No-overflow safety: both levels remain within their physical
bounds; (2) Bounded settling: the system enters a steady tracking region within a bounded delay
after a reference event; (3) Stable tracking: that region persists while the reference stays unchanged;
(4) Availability: acceptable behaviour for a sufficient measured duration over an observation horizon.
Together, these mix invariant safety, bounded response, persistence, and quantitative duration, so they
exercise different semantic mechanisms and expose different risks of accidental weakening.
    The safety argument follows the control cycle. Sampling preserves physical admissibility. The
controller leaves the physical state unchanged and establishes the guard for the next plant phase. Under the
stated flow and compatibility assumptions, plant evolution preserves non-negativity and capacity. These
component results yield preservation for one complete cycle, and finite induction gives the corresponding
invariant for repeated cycles. A trace bridge carries reachable-state safety to the trace requirement.
The broader development builds on this invariant proof with temporal interpretation, institution-level
representation, approximate conformance, and executable monitoring [8, 3, 11, 12, 4].
    The case study directly supports automated system assurance because it separates the physical
4                                               Contract-Aware Rescue of a Drifted Isabelle Development


plant, fixed controller, verified guards, runtime monitors, and formal evidence, a structure that recurs
in automated fuel transfer, coolant circulation, battery thermal management, hydraulic regulation, and
ballast or trim control. In each case, the physical equations may be straightforward, yet assurance still
needs a precise account of assumptions, operating envelope, controller authority, monitoring, and evidence
provenance. The architecture could support later semi-autonomous or autonomous extensions, but this
contribution focuses on the automated control system itself.


3.2   Isabelle architecture and development baselines
The first skeleton contained nine theories. Double_Tank_Alphabet introduced the state, traces, relations,
and lens structure. Double_Tank_Plant, Double_Tank_Sampling, and Double_Tank_Controller
represented the main operational components. Double_Tank_Requirements defined safety, settling,
tracking, availability, and temporal properties. Double_Tank_Closed_Loop composed the relations and
lifted one-cycle preservation using finite iteration. Double_Tank_Conformance introduced distance,
envelopes, and tolerance transfer, while Double_Tank_Monitor connected the denotational requirements
to executable checks. The entry theory Double_Tank exported public assurance results.
     Three semantic seams were visible in the first outline: solves_tank_ode stood in for continuous
ODE or Hybrid UTP semantics, state_duration for duration-calculus or interval-measure semantics,
and is_closed_loop_trace for the relationship between real-time traces and repeated plant, sampling,
and controller execution. Leaving these seams explicit avoided importing a second semantic foundation
merely to populate the outline. It also created a risk: when a seam was later defined, its definition had to
capture the intended semantics rather than make the target theorem true by construction.
     In the final reconstruction, milestone R10 establishes the four requirements from the quantitative trace
contract; the remaining operational-to-trace bridge is recorded separately as DT-R011. Figure 1 makes
this remaining assurance boundary explicit. The operational theories define repeated plant, sampling, and
controller execution. The reconstructed trace contract provides the semantic interface used by the verified
reconstruction. What remains to be established is that coherent traces generated by the operational model
satisfy this interface.
     Table 1 distinguishes the principal baselines used in the project. The labels refer to different artefacts
and should not be confused. The v0.24 baseline preserves and audits the expanded sixteen-theory
development, whereas R1–R10 is a separate reconstruction within the first nine-theory architecture.
     The expanded v0.23 bundle added the theories Duration_Semantics, Double_Tank_Duration,
Hybrid_Institution, Double_Tank_Institution, Thermostat_Institution, Hybrid_Trace_-
Institution, and Hybrid_Temporal_Institution, drawing on Duration Calculus and institution
theory respectively [8, 3]. Its sixteen theories fell into four layers: generic institution and duration
foundations; the concrete double-tank model; institution-parametrised safety and temporal representations;
and the conformance, monitoring, and entry interfaces. To check that the generic institution machinery
had not been inadvertently specialised to the double-tank case, we also instantiated it with an independent
thermostat model. The successful thermostat instance therefore serves as a generality check on the generic
institution machinery. The supplementary artefact records the complete theory catalogue.


4     LLM-guided proof discovery
The development was theory-first: the nine initial theories fixed the vocabulary and headline statements
before attempting the difficult proofs. They contained ten unfinished obligations. The intended proof order
J. Woodcock et al.                                                                                                5


                                       Operational closed-loop execution


                     Plant evolution                Sampling                       Controller
                         h1 , h2                observations, clock              pump command


                                                           DT-R011
                                                           open

                                             Quantitative trace contract
                                             is closed loop trace

                                                           R10
                                                           proved


                     No-overflow safety      bounded settling       stable tracking   availability


Figure 1: Operational and assurance layers, read top-to-bottom. Plant, sampling, and controller steps form
repeated closed-loop executions; the open DT-R011 bridge must show that their coherent traces satisfy
is_closed_loop_trace; R10 then derives the four requirements from that quantitative trace contract.


Table 1: Development chronology. The v0.x labels denote historical development baselines; R1–R10
denote the CAPRI reconstruction milestones detailed in Table 3.
Stage                     Characterisation

Original outline / v0.1   Nine-theory skeleton containing the intended vocabulary and ten unfinished obligations.
v0.10                     Nine theories, 953 lines, 40 definitions, 28 lemmas, 19 theorems, ten oops, and no sorry.
v0.23                     Expanded sixteen-theory development of about 6,250 lines, accepted by Isabelle and
                          admission-free; no-overflow safety was proved, while settling, stable tracking, and avail-
                          ability remained conditional or unresolved.
v0.24 CAPRI baseline      The v0.23 mathematics together with frozen provenance, correspondence data, contracts,
                          architectural invariants, and a drift audit.
Reconstruction            A separate CAPRI-governed reconstruction within the first nine-theory architecture, using
R1–R10                    contracts derived from the earliest theory frame.
R10 final                 All ten scoped reconstruction obligations discharged; Isabelle and contract checks ac-
reconstruction            cepted; the final requirement theorem remains relative to is_closed_loop_trace.
DT-R011                   Planned operational trace-adequacy bridge.



followed semantic dependency: continuous evolution and plant invariants first, then sampling and control,
finite closed-loop iteration, conformance, temporal requirements, monitors, and finally the end-to-end
theorem. This ordering later became the basis of the controlled reconstruction.
     ChatGPT was used in a diagnostic loop similar to prover-checked generation workflows [10, 5].
Candidate proofs or supporting lemmas were installed in disposable repositories, and the corresponding
complete Isabelle2025-2 session was built; failure diagnostics informed later attempts. Isabelle determined
6                                               Contract-Aware Rescue of a Drifted Isabelle Development


proof acceptance, while the developer selected subsequent baselines. At this stage of the development, the
surrounding theory frame was not independently protected. The archive preserves candidate repositories
and diagnostics, although it lacks a stable model identifier for every historical ChatGPT interaction.
     After excluding byte-identical downloads and packaging-only changes, the archive contains 59
substantive states: 23 stable and 36 broken. Failures exposed unavailable facts, hidden analytic side
conditions, weak induction hypotheses, missing frame conditions, and mismatches between the intended
physical argument and the formal goal. Several obstacles lay outside the proof body (for example, an
undefined semantic seam or a statement requiring reformulation), which are precisely the points at which
unrestricted editing can turn repair into theory drift. By v0.23, the enlarged sixteen-theory development
built without oops, sorry, or axiomatisations, but bounded settling, stable tracking, availability, and the
full end-to-end assurance claim, was still conditional or unresolved.


5    From proof repair to CAPRI
CAPRI treats proof repair as a controlled repository transformation [21]. For baseline repository R,
candidate R′ , and edit contract C, acceptance is

      Accept(R, R′ , C) ⇐⇒ Build(R′ ) ∧ Conforms(R, R′ , C).

Isabelle establishes Build; an independent checker establishes Conforms. The checker compares the frozen
baseline and candidate using repository-, file-set, and source-region checks rather than semantic AST
equivalence: only nominated regions may change; protected statements, assumptions, definitions, imports,
files, and build metadata remain fixed as required by the contract; and forbidden tokens are rejected. The
same check runs before and after the Isabelle build. Thus Conforms detects unauthorised structural edits
but cannot judge semantic equivalence inside an authorised region; a permitted rename, scope change, or
replacement definition still requires explicit wider authority and substantive semantic review.

target:                                                baseline: R9
  theory: Double_Tank_Plant                            task: R10
  theorem: plant_preserves_nonnegative_levels          editable_files:
editable:                                                - Double_Tank_Plant.thy
  proof_body: true                                       - Double_Tank_Requirements.thy
protected:                                               - Double_Tank_Closed_Loop.thy
  theorem_statement: true                                - Double_Tank_Conformance.thy
  assumptions: true                                    protected:
  definitions: true                                      all_other_formal_files: true
  imports: true                                        required_checks:
  other_files: true                                      - complete_isabelle_build
forbidden: [sorry, axiomatisation, oracle]               - contract_conformance


Figure 2: CAPRI authority boundaries: representative proof-only contract (left) and schematic, non-
verbatim R9-to-R10 wider contract (right). The latter explicitly limits edits to four formal files.

The checker distinguishes a legitimate accepted repair from safe failure and from false success: a candidate
building only after an unauthorised repository change. A control where the target theorem was weakened
to a trivial statement demonstrated the distinction: Isabelle accepted the altered theory, while CAPRI
rejected the delta. The double-tank project then used this build-plus-conformance criterion to reconstruct
a development in which drift had accumulated through a longer sequence of locally reasonable edits.
J. Woodcock et al.                                                                                                     7


6     Auditing theory drift
Isabelle continued to accept the expanded theories, so the audit focused on correspondence to the first
outline rather than kernel soundness. Its universe was the 100 named declarations in the earliest frame; the
295 names added in v0.23 were recorded separately. Machine-generated inventories and correspondence
outputs supplied the candidate mapping; the researchers then inspected every non-identical case and each
rename, split, or merge and recorded a relationship class and rationale. Identical formal content means
that the formal statement or definition body was unchanged, excluding presentation-only edits. Eighty-
four declarations met that test, and sixteen did not. The 16/100 result therefore combines mechanical
comparison with manual semantic classification: the archived map and rationales are inspectable, but
the classifications remain interpretive and were not independently adjudicated. Among the ten original
unfinished obligations, six were proved unchanged and three only after reformulation. The original
unconditional end-to-end obligation remained open.
    The audit did not count every difference as a defect. An uninterpreted semantic seam eventually needs
a definition, and several proofs required explicit flow guards or frame conditions. Other edits altered
a requirement or public assurance claim and therefore called for correction or prominent qualification.
Table 2 groups the sixteen changes by their effect on the engineering argument.

                         Table 2: Material changes among the 100 original declarations.
Group                     Count    Representative declarations                  Engineering effect

Semantic instantiation    4        solves_tank_ode,   state_duration,           Supplies      missing    meaning;
/ refactoring                      availability_requirement,     is_-           availability_requirement is also
                                   closed_loop_trace                            refactored through availability_-
                                                                                requirement_with.
Plant and assumptions     4        plant_evolution, guarded capacity, one-      Makes the preservation argument sounder
                                   cycle and finite-iteration preservation      while restricting the admitted plant and
                                                                                parameter domain.
Safety domain and         6        safe_at, safety_requirement, overflow        Changes strict < to ≤ and restricts
boundary                           monitor and its soundness/coverage results   safety_requirement to non-negative
                                                                                time.
End-to-end interface      2        closed_loop_meets_requirements,              Moves settling, stability, and availabil-
                                   double_tank_end_to_end_assurance             ity into premises of the public assurance
                                                                                claim.




6.1     The principal assurance failures
The most serious drift concerned the safety boundary and the end-to-end theorem. Changing < to ≤
at tank capacity looks minor but shifts the engineering interpretation of both the requirement and the
monitor. Under the prior strict policy, reaching capacity already lies outside the safe region, leaving no
margin for disturbance, measurement uncertainty, or numerical error; under the revised policy, equality
is accepted and the monitor reports Monitor_OK. The revised definitions and monitor theorems were
internally consistent, yet they certified a weaker policy than the first outline.
     The change to closed_loop_meets_requirements was more consequential. The first development
was meant to show that the closed-loop controller established safety, bounded settling, stable tracking, and
availability. In v0.23, safety was derived, but the other three requirements appeared as premises; hence
8                                              Contract-Aware Rescue of a Drifted Isabelle Development


the theorem was logically valid but no longer discharged the intended controller-assurance obligation.
Exporting the corresponding conditional result as double_tank_end_to_end_assurance invited a
reader to infer that the full requirement set had been proved. This is a characteristic form of drift: the
theorem name and its architectural position preserve the appearance of the first claim even though the
logical burden has quietly moved into the assumptions.
    Semantic seams create a different risk. Giving solves_tank_ode and state_duration concrete
meanings was necessary progress, but each choice committed the development to a particular interpretation
of the previously abstract seam. Defining is_closed_loop_trace by pointwise reachability was more
problematic, since a set of individually reachable observations need not form one coherent execution. A
trace theorem can then become easy to prove if the trace predicate already includes the desired property
or admits observations independently of their temporal relationship. The audit treated such definitions
as semantic changes demanding explicit provenance and a successor obligation connecting them to
operational implementation.
    The two most consequential changes appear schematically below. The exact Isabelle declarations
contain supplementary context, but the extracts below show the logical difference.
(* Original boundary policy *)
safe_at p s ≡
  0 ≤ h1 s ∧ h1 s < capacity1 p ∧
  0 ≤ h2 s ∧ h2 s < capacity2 p

(* Drifted boundary policy *)
safe_at p s ≡
  0 ≤ h1 s ∧ h1 s ≤ capacity1 p ∧
  0 ≤ h2 s ∧ h2 s ≤ capacity2 p

(* Intended end-to-end obligation *)
assumes "admissible_parameters p"
    and "is_closed_loop_trace p tr"
shows "safety_requirement p tr
     ∧ settling_requirement p tr
     ∧ stable_tracking_requirement p tr
     ∧ availability_requirement p tr"

(* Drifted conditional result *)
assumes "admissible_parameters p"
    and "settling_requirement p tr"
    and "stable_tracking_requirement p tr"
    and "availability_requirement p tr"
shows "safety_requirement p tr
     ∧ settling_requirement p tr
     ∧ stable_tracking_requirement p tr
     ∧ availability_requirement p tr"



6.2   Architectural drift
The generic institution machinery, duration semantics, common safety and temporal languages, confor-
mance layer, monitors, and thermostat instance all added useful mathematics. Their introduction also
created new ways for the concrete double-tank claim to change. An institution layer might replace the
source semantics instead of representing it; a direct theorem might bypass satisfaction; a translation might
J. Woodcock et al.                                                                                        9


alter the meaning of a requirement; or a conditional result might be exported under an unconditional name.
The v0.24 CAPRI baseline therefore fixed architectural invariants. Institution layers must preserve the
source semantics, transported results must depend on a proved satisfaction condition, the four require-
ments must have traceable source-to-target mappings, and public all-requirements claims must expose
any premises that remain unproved. The declaration map and semantic audit supply information absent
from both the Build and Conforms verdicts: whether an authorised change still preserves the engineering
meaning of the original task.


7     Contract-governed rescue
7.1   Preserving intention and proof knowledge
The rescue froze two artefacts. The original nine-theory frame retained the intended definitions, require-
ments, theorem statements, and semantic seams. The verified v0.23 repository retained the accumulated
mathematics, reusable proofs, and failed approaches that had exposed hidden assumptions, a familiar
proof-maintenance issue in evolving Isabelle developments [1]. The v0.24 CAPRI baseline added prove-
nance records, declaration correspondence, architectural constraints, contracts, public-interface checks,
manifests, and hashes. Both sources were needed: the first supplied the task boundary, and the second
supplied proof knowledge that would otherwise have been lost.
    We mapped each significant original declaration to its v0.23 counterpart and classified it as preserved,
renamed, specialised, generalised, split, merged, reformulated, superseded, missing, rejected, or added.
The four principal requirements received end-to-end traceability from physical motivation through Is-
abelle definition, supporting assumptions, theorems, institution translation, and runtime monitor, making
boundary changes and conditional assurance claims visible right where they affected the public interface.
    The reconstruction proceeded in a separate source tree. For a proof-only task, the contract froze the
theorem statement, assumptions, locale context, definitions, imports, file set, protected text outside the
proof, Isabelle version, and build command, so only the nominated proof region could change. When
an obligation could not be solved honestly under that authority, the workflow did not silently widen
the patch; it required a new contract for a statement change, semantic extension, architectural change,
or conservative new theory, and that broader contract had to name the permitted change and retain the
existing obligation in the record.
    Candidates were checked against the contract before Isabelle ran, built in the frozen environment, and
checked again after the build. The first check kept obviously unauthorised candidates from consuming
prover time; the second caught changes introduced by patch application or an iterative tool outside the
displayed proof proposal. A candidate could therefore end in one of three useful states: an accepted repair,
where build and contract checks both passed; a safe failure, where the proof failed but the protected frame
stayed unchanged; or a false success, where Isabelle accepted the repository but the independent checker
found an unauthorised change.
    The controlled reconstruction discharged ten scoped obligations in dependency order. Each accepted
state became the protected baseline for the next task, so the authority to change the development expanded
only through an explicit contract. Table 3 summarises the sequence.
We set edit authority separately for each reconstruction milestone. Proof-only contracts were used when
possible. Semantic completion or multi-file composition required a newly named contract that recorded
the wider authority and retained the predecessor obligation. The archived contracts, rather than theorem
names, determine the editable regions and protected files.
10                                             Contract-Aware Rescue of a Drifted Isabelle Development


                          Table 3: CAPRI-governed reconstruction milestones.
 State    Obligation                           Role in the reconstruction

  R1      plant_zero_duration                  Supplied a usable plant semantics and handled the empty deriva-
                                               tive interval at zero duration.
  R2      plant_preserves_-                    Established scalar barrier reasoning preventing either level from
          nonnegative_levels                   crossing below zero.
  R3      plant_preserves_capacity_-           Derived capacity preservation from explicit controller and plant
          under_guard                          guards rather than building safety into evolution.
  R4      sampling_occurs_at_period            Repaired sampling-clock progress whilst preserving the sampling
                                               frame.
  R5      trace_tolerance_budget               Proved additive composition of trace tolerances.
  R6      approximate_safety_transfer          Transferred strong safety from the ideal process to an approxi-
                                               mately conforming implementation.
  R7      approximate_tracking_-               Transferred tracking with an explicit accumulated tolerance bud-
          transfer                             get.
  R8      closed_loop_cycle_-                  Connected plant framing, controller guards, sampling, and one
          preserves_physical_state             complete cycle.
  R9      closed_loop_preserves_-              Lifted one-cycle preservation using finite iteration.
          physical_state
 R10      closed_loop_meets_-                  Completed the reconstructed composition using explicit duration
          requirements                         semantics and a non-circular trace contract; operational adequacy
                                               remains DT-R011.



    Because reconstruction followed the dependency order, the final theorem had to use the established
plant, sampling, controller, conformance, and iteration results. Its statement could not be relaxed merely
because a proof attempt failed. The R10 archive illustrates the point. Two candidates used unavailable
facts or methods (diff_nonneg, sub_nonneg, and nlinarith) and left the conformance argument
incomplete. A third used an import-independent order argument and passed both the complete build and
the composite contract checker. Retaining all three records explains the choice of the accepted proof.
    The final release, Double_Tank_Hybrid_UTP_Reconstruction_R10, kept the earliest nine-theory
architecture. The alphabet protected the state and trace vocabulary; the plant theory stated the physical
invariant, vector field, continuous evolution, frames, and barrier results; sampling and controller theories
established timing, frame, and guard properties; the requirements theory retained the four source require-
ments and explicit duration semantics; the closed-loop theory composed the operational relations and
proved invariant preservation; the conformance theory established tolerance composition and transfer; the
monitor theory retained executable observations; and the entry theory exported the public results.
    The R9-to-R10 formal delta was confined to Double_Tank_Plant.thy, Double_Tank_-
Requirements.thy, Double_Tank_Closed_Loop.thy, and Double_Tank_Conformance.thy. All
other formal files were protected. The accepted result therefore did not depend on revisions to the
alphabet, controller, monitor, imports, or public structure; its changes were limited to the files named in
the wider reconstruction contract.
J. Woodcock et al.                                                                                          11


8    Results and assurance boundary
The final reconstruction was accepted on 31 July 2026 under Isabelle2025-2 and Poly/ML 5.9.2, containing
nine rescue theories and ten scoped reconstruction obligations, all discharged. The complete session and
contract-conformance check both passed, and the release contains no oops, sorry, axiomatisations, or
oracles. Every accepted delta conformed to its contract, and any change to a theorem statement, semantic
definition, architecture, or public assurance claim required the developer to approve a wider contract. This
still falls short of complete operational end-to-end verification: trace adequacy remains the separately
named obligation DT-R011.
     A co-author replayed the complete nine-theory R10 session, Action 34 verifier, and DT-R010 workflow,
reproducing the ten discharged obligations, four-file R9–R10 delta, closure markers, admission checks, ten
DT-R010 self-tests, and six static Action 8 controls. The co-author also re-examined the 16-declaration
audit and its principal end-to-end drift finding. This was an internal secondary replay, not an external
replication.

                                    Table 4: Final reconstruction status.
Measure                                                                                                 Result
Rescue theories                                                                                             9
Scoped reconstruction obligations                                                                          10
Discharged scoped obligations                                                                              10
oops                                                                                                        0
sorry                                                                                                       0
Axiomatisations                                                                                             0
Oracles                                                                                                     0
Complete Isabelle session                                                                            Accepted
Contract-conformance verdict                                                                         Accepted


R10 does not close every semantic question. Its theorem closed_loop_meets_requirements assumes
the predicate is_closed_loop_trace for parameters p and trace tr, but not the four requirement
predicates themselves. From the explicit clauses of that quantitative trace contract, including strict-safety
and uniform-tracking clauses and the adopted duration semantics, R10 derives no-overflow safety, bounded
settling, stable tracking, and availability. The open question sits one layer earlier: the release does not yet
show that every coherent trace generated by repeated plant, sampling, and controller execution satisfies
every clause of is_closed_loop_trace. R10 thus proves the lower arrow in Fig. 1, while DT-R011
must prove the upper one. ModelPlex addresses an analogous model-to-execution problem through
verified runtime validation [12], albeit in a different logic and toolchain. The next task is therefore the
separately named obligation DT-R011 Operational Trace Adequacy, whose intended form is:
theorem closed_loop_execution_is_valid_trace:
  assumes "admissible_parameters p"
      and "operational_closed_loop_trace p tr"
  shows "is_closed_loop_trace p tr"

DT-R011 must begin from a named successor baseline; the accepted R10 release remains immutable.
Leaving this boundary open is part of the rescue discipline. An unresolved semantic bridge has been given
a stable identifier and an explicit statement, rather than being folded into an assumption or hidden behind
an overbroad theorem name.
12                                              Contract-Aware Rescue of a Drifted Isabelle Development


9    Discussion
An Isabelle build certifies the theorem stated in the candidate repository, not preservation of the developer’s
intended theory frame. CAPRI records that authority boundary and checks candidate deltas against it. A
passing contract verdict still leaves the adequacy of an authorised new physical or semantic definition to
substantive review and, where necessary, a successor contract. Visible semantic seams are useful only
when their later interpretations and downstream effects remain traceable. DT-R011 names and exemplifies
this discipline by exposing the missing operational bridge instead of hiding it inside the final theorem’s
assumptions.
    The failed candidates are useful evidence because their diagnostics expose recurring mismatches
between informal reasoning and formal obligations, while their deltas reveal when a proposal attempts
to change the problem rather than solve it. The project also retains two baselines: the 16-theory reposi-
tory preserves useful institution and duration machinery and the history of drift, while the nine-theory
reconstruction preserves the original task boundary.
    The study has important limitations. It reports one hybrid-system development and one reconstruction
sequence, without a controlled comparison of repair strategies. Developer judgement influenced prompts,
authorised semantic changes, and the retrospective drift classification. The secondary replay was internal;
external replication remains future work. The contract checker is trusted tooling and has not itself been
verified in Isabelle. The case is also small relative to mature hybrid-verification developments [17, 13];
the conclusions are methodological rather than performance claims about large-scale repair.


10     Conclusion
The double-tank case exposes a gap between proof validity and task validity. Isabelle can correctly
accept a theory after an iterative repair process weakens a theorem, changes a definition, or strengthens
assumptions. The v0.23 audit found material changes in 16 of 100 original declarations; most seriously,
the principal assurance theorem derived safety while assuming settling, stability, and availability. The
theorem remained valid but no longer discharged the original end-to-end obligation.
    The reconstruction shows how to recover from such drift without discarding useful proof knowledge.
The original nine-theory frame remains authoritative, while retaining the larger development serves as
evidence and a source of lemmas and semantic machinery. Ten reconstruction obligations were discharged
under explicit contracts. R10 passes the complete Isabelle build and contract check and contains no oops,
sorry, axiomatisations, or oracles. It derives the four requirements from an explicit quantitative trace
contract rather than assuming them separately.
    A semantic gap remains: R10 does not prove that every trace generated by the plant, sampler, and
controller satisfies is_closed_loop_trace. Closing this gap is the explicit successor obligation DT-
R011, Operational Trace Adequacy. The broader lesson is that LLM-assisted formal development
needs two complementary controls: the prover checks logical validity, while an independent mechanism
checks that repair stays within the authorised theory boundary. Semantic adequacy remains a separate
engineering judgement.


AI Usage
We designed our experiments to explore contract-aware proof repair. We used OpenAI ChatGPT 5.0
to propose Isabelle proof scripts and supporting lemmas in response to prover diagnostics. We did not
J. Woodcock et al.                                                                                           13


retain stable model identifiers for every historical ChatGPT interaction. Isabelle2025-2 checked all proof
candidates; repository changes in the reconstruction were checked against CAPRI contracts [21]. We
used CAPRI, which invokes OpenAI’s Responses API to generate candidate Isabelle proof repairs, using
GPT-5.2 (gpt-5.2-2025-12-11) with high reasoning effort; each repair request is made independently,
without shared conversational state. Grammarly, an AI-powered writing assistant, was used to improve
grammar, spelling, punctuation, and clarity. The authors reviewed all generated and revised material and
take full responsibility for the paper.


Artefact Availability
The complete reproducibility artefact is archived at Zenodo, DOI: https://doi.org/10.5281/zenodo.
21981425. The archive contains the source baselines, R10 reconstruction, CAPRI contracts and reports,
correspondence and traceability evidence, control suites, replay scripts, manifests, and DT-R011 material.
The evaluated release is Double_Tank_Hybrid_UTP_Reconstruction_R10, checked with Isabelle2025-
2 and Poly/ML 5.9.2. The recommended replay route is the supplied Action 35 closure package: from 03_-
r10_reconstruction, verify and extract CAPRI_Double_Tank_Action_35_R10_Closure.zip, then
run ./verify-action35.sh and ./run-r10-complete.sh. Alternatively, extract the standalone R10
release and run isabelle build -v -D . -o document=false from that Isabelle session directory.
The Action 36 final-release archive has SHA-256
831bc299aa714f17bb304a1c7dd5f37900b5dd11ee03eec3f32bf9cbd850b370



References
 [1] June Andronick (2019): A Million Lines of Proof About a Moving Target (Invited Talk). In John Harrison, John
     O’Leary & Andrew Tolmach, editors: 10th International Conference on Interactive Theorem Proving, ITP 2019,
     Portland, OR, USA, September 9-12, 2019, LIPIcs 141, Schloss Dagstuhl - Leibniz-Zentrum für Informatik, pp.
     1:1–1:1, doi:10.4230/LIPICS.ITP.2019.1. Available at https://doi.org/10.4230/LIPIcs.ITP.2019.1.
 [2] Sascha Böhme & Tobias Nipkow (2010): Sledgehammer: Judgement Day. In Jürgen Giesl & Reiner Hähnle,
     editors: Automated Reasoning, 5th International Joint Conference, IJCAR 2010, Edinburgh, UK, July 16-19,
     2010. Proceedings, Lecture Notes in Computer Science 6173, Springer, pp. 107–121, doi:10.1007/978-3-642-
     14203-1 9. Available at https://doi.org/10.1007/978-3-642-14203-1_9.
 [3] Zhou Chaochen & Michael R. Hansen (2004): Duration Calculus - A Formal Approach to Real-Time Systems.
     Monographs in Theoretical Computer Science. An EATCS Series, Springer, doi:10.1007/978-3-662-06784-0.
     Available at https://doi.org/10.1007/978-3-662-06784-0.
 [4] Jyotirmoy V. Deshmukh, Rupak Majumdar & Vinayak S. Prabhu (2017): Quantifying conformance using
     the Skorokhod metric. Formal Methods Syst. Des. 50(2-3), pp. 168–206, doi:10.1007/S10703-016-0261-8.
     Available at https://doi.org/10.1007/s10703-016-0261-8.
 [5] Emily First, Markus N. Rabe, Talia Ringer & Yuriy Brun (2023): Baldur: Whole-Proof Generation and
     Repair with Large Language Models. In Satish Chandra, Kelly Blincoe & Paolo Tonella, editors: Proceedings
     of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of
     Software Engineering, ESEC/FSE 2023, San Francisco, CA, USA, December 3-9, 2023, ACM, pp. 1229–1241,
     doi:10.1145/3611643.3616243. Available at https://doi.org/10.1145/3611643.3616243.
 [6] Simon Foster (2019): Hybrid Relations in Isabelle/UTP. In Pedro Ribeiro & Augusto Sampaio, editors:
     Unifying Theories of Programming - 7th International Symposium, UTP 2019, Dedicated to Tony Hoare
     on the Occasion of His 85th Birthday, Porto, Portugal, October 8, 2019, Proceedings, Lecture Notes in
14                                                Contract-Aware Rescue of a Drifted Isabelle Development


     Computer Science 11885, Springer, pp. 130–153, doi:10.1007/978-3-030-31038-7 7. Available at https:
     //doi.org/10.1007/978-3-030-31038-7_7.
 [7] Simon Foster, Frank Zeyda & Jim Woodcock (2014): Isabelle/UTP: A Mechanised Theory Engineering
     Framework. In David A. Naumann, editor: Unifying Theories of Programming - 5th International Sympo-
     sium, UTP 2014, Singapore, May 13, 2014, Revised Selected Papers, Lecture Notes in Computer Science
     8963, Springer, pp. 21–41, doi:10.1007/978-3-319-14806-9 2. Available at https://doi.org/10.1007/
     978-3-319-14806-9_2.
 [8] Joseph A. Goguen & Rod M. Burstall (1992): Institutions: Abstract Model Theory for Specification and
     Programming. J. ACM 39(1), pp. 95–146, doi:10.1145/147508.147524. Available at https://doi.org/10.
     1145/147508.147524.
 [9] Orlena C. Z. Gotel & Anthony C. W. Finkelstein (1994): An Analysis of the Requirements Traceability
     Problem. In: Proceedings of the First IEEE International Conference on Requirements Engineering, IEEE
     Computer Society, pp. 94–101, doi:10.1109/ICRE.1994.292398. Available at https://doi.org/10.1109/
     ICRE.1994.292398.
[10] Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski, Konrad Czechowski, Tomasz Odrzygózdz, Pi-
     otr Milos, Yuhuai Wu & Mateja Jamnik (2022): Thor: Wielding Hammers to Integrate Language Mod-
     els and Automated Theorem Provers. In Sanmi Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave,
     K. Cho & A. Oh, editors: Advances in Neural Information Processing Systems 35: Annual Confer-
     ence on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, Novem-
     ber 28 - December 9, 2022. Available at http://papers.nips.cc/paper_files/paper/2022/hash/
     377c25312668e48f2e531e2f2c422483-Abstract-Conference.html.
[11] Martin Leucker & Christian Schallhart (2009): A brief account of runtime verification. J. Log. Algebraic
     Methods Program. 78(5), pp. 293–303, doi:10.1016/J.JLAP.2008.08.004. Available at https://doi.org/
     10.1016/j.jlap.2008.08.004.
[12] Stefan Mitsch & André Platzer (2014): ModelPlex: Verified Runtime Validation of Verified Cyber-Physical
     System Models. In Borzoo Bonakdarpour & Scott A. Smolka, editors: Runtime Verification - 5th International
     Conference, RV 2014, Toronto, ON, Canada, September 22-25, 2014. Proceedings, Lecture Notes in Computer
     Science 8734, Springer, pp. 199–214, doi:10.1007/978-3-319-11164-3 17. Available at https://doi.org/
     10.1007/978-3-319-11164-3_17.
[13] Jonathan Julián Huerta y Munive & Georg Struth (2019): Predicate Transformer Semantics for Hybrid Systems:
     Verification Components for Isabelle/HOL. CoRR abs/1909.05618. Available at http://arxiv.org/abs/
     1909.05618.
[14] Bashar Nuseibeh & Steve M. Easterbrook (2000): Requirements Engineering: A Roadmap. In: Proceedings
     of the Conference on the Future of Software Engineering, ACM, pp. 35–46, doi:10.1145/336512.336523.
     Available at https://doi.org/10.1145/336512.336523.
[15] Lawrence C. Paulson, Tobias Nipkow & Makarius Wenzel (2019): From LCF to Isabelle/HOL. Formal
     Aspects Comput. 31(6), pp. 675–698, doi:10.1007/S00165-019-00492-1. Available at https://doi.org/
     10.1007/s00165-019-00492-1.
[16] Stanislas Polu & Ilya Sutskever (2020): Generative Language Modeling for Automated Theorem Proving.
     CoRR abs/2009.03393. Available at https://arxiv.org/abs/2009.03393.
[17] Jan-David Quesel, Stefan Mitsch, Sarah M. Loos, Nikos Aréchiga & André Platzer (2016): How to model
     and prove hybrid systems with KeYmaera: A tutorial on safety. Int. J. Softw. Tools Technol. Transf. 18(1), pp.
     67–91, doi:10.1007/S10009-015-0367-0. Available at https://doi.org/10.1007/s10009-015-0367-0.
[18] Talia Ringer, Karl Palmskog, Ilya Sergey, Milos Gligoric & Zachary Tatlock (2019): QED at Large: A Survey
     of Engineering of Formally Verified Software. Foundations and Trends in Programming Languages 5(2–3), pp.
     102–281, doi:10.1561/2500000045. Available at https://doi.org/10.1561/2500000045.
[19] Talia Ringer, RanDair Porter, Nathaniel Yazdani, John Leo & Dan Grossman (2021): Proof repair across type
     equivalences. In Stephen N. Freund & Eran Yahav, editors: PLDI ’21: 42nd ACM SIGPLAN International
J. Woodcock et al.                                                                                    15


    Conference on Programming Language Design and Implementation, Virtual Event, Canada, June 20-25, 2021,
    ACM, pp. 112–127, doi:10.1145/3453483.3454033. Available at https://doi.org/10.1145/3453483.
    3454033.
[20] Hong Ki Thae & Dang Van Hung (2001): A Case Study on Formal Design of Hybrid Control Systems.
     In: 25th International Computer Software and Applications Conference (COMPSAC 2001), Invigorating
     Software Development, 8-12 October 2001, Chicago, IL, USA, IEEE Computer Society, pp. 423–428,
     doi:10.1109/CMPSAC.2001.960648. Available at https://doi.org/10.1109/CMPSAC.2001.960648.
[21] Jim Woodcock, Gabriel Leite, Augusto Sampaio & Ran Wei (2026): CAPRI: Contract-Aware Proof Repair
     for Isabelle. Technical Report, University of York, UK.
[22] Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil,
     Ryan J. Prenger & Animashree Anandkumar (2023): LeanDojo: Theorem Proving with Retrieval-
     Augmented Language Models. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz
     Hardt & Sergey Levine, editors: Advances in Neural Information Processing Systems 36: Annual
     Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA,
     December 10 - 16, 2023. Available at http://papers.nips.cc/paper_files/paper/2023/hash/
     4441469427094f8873d0fecb0c4e1cee-Abstract-Datasets_and_Benchmarks.html.
