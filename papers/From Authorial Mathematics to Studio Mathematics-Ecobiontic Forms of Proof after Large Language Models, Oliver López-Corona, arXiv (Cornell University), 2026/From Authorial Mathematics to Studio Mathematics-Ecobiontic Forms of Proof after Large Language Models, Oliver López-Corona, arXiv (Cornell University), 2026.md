                                                   From Authorial Mathematics to Studio Mathematics:
                                                  Ecobiontic Forms of Proof after Large Language Models
arXiv:2608.22194v1 [physics.soc-ph] 23 Aug 2026




                                                                                     Oliver López-Corona

                                                                                  Investigadores por México (IxM),

                                                           Instituto de Investigaciones en Matemáticas Aplicadas y en Sistemas (IIMAS),

                                                                        Universidad Nacional Autónoma de México (UNAM)


                                                                                              Abstract
                                                           Mathematics has often been organized around an authorial subject: one person,
                                                       or a small group, composing proofs through language, notation, and judgment. Large
                                                       language models, proof assistants, formal libraries, and repositories now make another
                                                       production unit technically credible: a human-machine assemblage. This article calls
                                                       that unit a studio ecobiont and asks when it is epistemically legitimate. Its governance
                                                       thesis is that human participation is substantive only when the system preserves traceable
                                                       provenance, reconstructible human competence, capacity to challenge the result, effective
                                                       authority to stop or withdraw it, and public responsibility. These conditions distinguish
                                                       a governed studio from a degenerate studio whose human oversight is ceremonial. A
                                                       comparison of Polymath, the Liquid Tensor Experiment, Danus, and the Jacobian
                                                       counterexample episode shows that collaboration, formalization, technical orchestration,
                                                       and epistemic governance are independent dimensions. The proposed understanding
                                                       audit and contribution-authority trace are governance designs, not validated measures.
                                                       No causal superiority over authorial practice is claimed.

                                                  Keywords: philosophy of mathematics; mathematical practice; proof; understanding; for-
                                                  malization; large language models; proof assistants; Lean; distributed cognition; social
                                                  epistemology; mathematical authorship


                                                  1    Introduction: the unit of proof-production
                                                  The question raised by large language models in mathematics is often posed in an unhelpful
                                                  form: can artificial intelligence do mathematics? That question invites either technological

                                                                                                   1
triumphalism or defensive skepticism. A more precise philosophical question is this: what can
count as the epistemically responsible unit of mathematical production? In much of modern
mathematical culture, the default answer has been authorial. A proof is attributed to one
person, or to a small group, and its warrant is assessed through a community of competent
readers. This authorial arrangement is not the same as private cognition. Mathematical
work depends on teachers, seminars, journals, notational traditions, reviewers, libraries, and
institutions. Still, the proof as published object has often been organized around an authorial
subject.
    The authorial picture has good reasons behind it. Mathematical understanding is not
exhausted by a derivation. Hardy’s account of mathematical creation emphasizes beauty,
economy, and permanence [Hardy 1940]. Lakatos presents mathematical knowledge as a
process of conjecture, proof, refutation, and repair [Lakatos 1976]. Thurston argues that
mathematical progress centrally involves communication and understanding, not merely
the accumulation of formally correct results [Thurston 1994]. Rav maintains that proofs
carry epistemic content not reducible to the bare existence of formal derivations [Rav 1999].
Azzouni’s derivation-indicator view, Tanswell’s criticism of simple dependence accounts, and
recent work on rigor, gaps, testimony, and fallibilism show that informal proof remains
embedded in practices of judgment, trust, and correction [Azzouni 2004; Tanswell 2015;
Andersen 2020; Andersen et al. 2021; De Toffoli 2021; Burgess and De Toffoli 2022; Tanswell
2024]. Any account of post-LLM mathematics that treats proof as merely machine-checkable
output loses this background.
    Yet the authorial arrangement is not the only possible arrangement. Proof assistants,
formal libraries, automated theorem proving, large language models, version-controlled repos-
itories, benchmarks, and software infrastructures now make another arrangement technically
credible. A proof project may involve a conceptual lead, an LLM that proposes sketches
or tactics, a proof assistant that checks formal derivations, library maintainers who stabi-
lize dependencies, programmers who build tooling, reviewers who evaluate exposition and
significance, and institutions that assign credit and responsibility. This article calls such
an arrangement studio mathematics. The term is not meant to replace ordinary talk of
collaboration, formalization, or mechanized proof. It names a particular shift in the unit of
production: from the author alone to a governed human-machine assemblage that produces,
checks, explains, preserves, and circulates mathematical artifacts.
    The contribution is philosophical rather than predictive. I do not argue that future
mathematics will be mostly studio mathematics or that LLMs will replace mathematicians.
The central claim is narrower: under suitable conditions, the epistemically relevant unit
of proof-production can be a governed assemblage of humans, software systems, formal


                                              2
repositories, and validation practices. This unit is infrastructural, formal, computational,
and institutionally governed in a stronger sense than ordinary social dependence. The paper
makes three claims that must remain separate. Descriptively, some contemporary projects
distribute production and warrant across human and technical components. Normatively, such
a project is governed only when it preserves substantive human epistemic agency and public
responsibility. Causally, whether governed studios improve learning, originality, reliability, or
resilience remains unresolved.

      Governance thesis. A studio is epistemically legitimate as a human mathemat-
      ical practice only when its human participants retain reconstructible competence,
      effective challenge and stop rights, traceable responsibility, and access to the
      dependencies needed for independent scrutiny.

    That task has become urgent because generative systems can break a familiar institutional
proxy. Mathematical papers have often functioned not only as containers of results but also
as evidence that their authors acquired the understanding, judgment, and craft required
to produce them. If a system can generate a publishable derivation while bypassing that
acquisition, the paper ceases to certify what the community informally took it to certify.
Weinreich calls this a crisis of AI-generated mathematics and argues that outsourcing proof-
production threatens the practice through which mathematical understanding is formed
[Weinreich 2026]. The objection is serious. It identifies a proxy rupture, not merely a
nostalgic preference for older tools.
    The present paper accepts that diagnosis while rejecting one possible inference from it. If
mathematical practice is intrinsically valuable, the relevant question is which configurations
preserve, distribute, or destroy the work from which understanding emerges. Literature search,
counterexample generation, formal verification, proof planning, and complete proof generation
are epistemically different interventions. Venkatesh examines how automation may change
collective judgments about mathematical importance, while Alper defends experimentation
with AI and formalization as mathematical tools [Venkatesh 2024; Alper 2026]. Tao describes
mathematical AI as a developing ecology of assistance, verification, and collaboration rather
than a single replacement event [Tao 2026]. The Leiden Declaration gives these distinctions
an institutional form by centering disclosure, independent verification, human responsibility,
and research autonomy [Alper et al. 2026]. Studio mathematics is defensible only if those
commitments become operational.
    The phrase CIMA ecobiont is used for this purpose. CIMA abbreviates four functions:
compute, infer, model, and act. An ecobiont is a coupled epistemic assemblage of agents,
tools, symbolic media, infrastructures, norms, and validation practices. The term draws

                                               3
from a prior ecobiont ontology rooted in holobiont and niche-construction thinking [Margulis
and Fester 1991; Gilbert et al. 2012; López-Corona et al. 2019], but the present use is not
biological. It is an ontology of mathematical practice. It is also continuous with distributed
cognition and the extended mind, which deny that cognitive agency must be located entirely
inside an individual organism [Hutchins 1995; Clark and Chalmers 1998]. The argument is
not that this vocabulary supersedes those literatures. It is that a CIMA ecobiont makes
explicit the relation between production, verification, repository memory, public action, and
responsibility in post-LLM mathematics.
    For mathematics, CIMA has a more specific meaning than generic information-processing.
To compute is to manipulate symbolic or formal objects under rule-governed constraints. To
infer is to move from premises, constructions, or proof states to warranted consequences. To
model is to select definitions, representations, examples, diagrams, formal encodings, and
explanatory structures that make a domain tractable. To act is to stabilize mathematical
artifacts in public forms: papers, lectures, library contributions, verified files, reusable lemmas,
and standards of acceptance. What distinguishes mathematical CIMA is that these functions
are constrained by proof, necessity, intelligibility, and transferability across problems.
    The structure is as follows. Section 2 clarifies authorial mathematics and the traditional
proof subject. Section 3 reviews distributed proof before LLMs. Section 4 introduces the
CIMA ecobiont and a claim-relative governance rule. Section 5 defines studio mathematics
and compares four cases. Section 6 separates correctness, understanding, explanation, and
taste. Section 7 treats credit, authority, testimony, and responsibility. Section 8 gives a
limited role to conditional antifragility. Section 9 addresses institutional ecology and protected
practice. Section 10 answers objections. Section 11 concludes.


2     Authorial mathematics and the traditional proof sub-
      ject
Mathematics resembles literary labor in one important respect. It can be performed through
a relatively light material medium: language, notation, diagrams, memory, and disciplined
imagination. A mathematician may work alone for long periods and produce a public artifact
whose main medium is symbolic exposition. This is not true of much contemporary science.
Particle physics, genomics, climate modeling, and many branches of neuroscience require
instruments, data pipelines, large budgets, technicians, and administrative coordination [de
Solla Price 1963; National Research Council 2015]. Mathematics, by contrast, has preserved
a strong authorial form.


                                                 4
    The authorial form should not be caricatured as the myth of the isolated genius. Even
a single-author proof is sustained by a community. It presupposes prior notation, results,
informal standards, evaluative habits, referees, and readers. What is authorial is not the whole
epistemic life of mathematics, but the production format of many mathematical artifacts.
The published proof is ordinarily credited to a bounded authorial unit, and the community
treats that unit as responsible for the result’s correctness, exposition, and originality.
    The authorial form also helps explain why mathematical judgment is partly aesthetic.
Beauty, elegance, economy, and conceptual compression are not ornaments added to proof
after correctness has been secured. They guide problem choice, definition choice, notation,
explanatory route, and standards of satisfactory understanding. Hardy’s aesthetic language
is therefore not merely romantic; it names a feature of mathematical agency that is difficult
to reduce to checking [Hardy 1940]. Thurston makes a related point when he treats com-
munication of understanding as a central aim of mathematical progress [Thurston 1994]. A
studio regime must therefore be judged not only by whether it can certify derivations, but
also by whether it can preserve, redistribute, or distort mathematical taste.
    Philosophy of mathematical practice has already complicated the authorial picture.
Lakatos shows that proofs develop through criticism and reconstruction, not only through
private deduction [Lakatos 1976]. Thurston emphasizes that the circulation of understanding
is a central mathematical aim [Thurston 1994]. Rav argues that mathematicians prove
theorems because proofs display methods, connections, and explanatory information [Rav
1999]. Andersen shows that published proofs may contain acceptable gaps that are regulated
by refereeing and community expectations [Andersen 2020]. De Toffoli develops a fallibilist
account in which mathematical justification is tied to practices of error correction [De Toffoli
2021]. Avigad argues that mathematical practice supports reliable inference through social
and textual mechanisms that approximate formal standards without reducing to them [Avigad
2021].
    These accounts are important because they show that the traditional proof subject is
already socially mediated. The issue is not whether mathematics is social. It is whether the
authorial subject remains the only plausible unit for production and responsibility when the
work is distributed across formal systems, generative models, repositories, and infrastructure.
The studio thesis begins at this point.


3     Distributed proof before LLMs
Studio mathematics is not created ex nihilo by large language models. There are at least
three prior trajectories.

                                               5
    First, computer-assisted proof has long challenged simple accounts of surveyability and
understanding. The four-color theorem raised the question whether a proof too large
or computationally dependent to be surveyed in the ordinary way should count as proof
[Tymoczko 1979]. Gonthier’s formal proof of the four-color theorem and the machine-checked
proof of the odd order theorem show that formal verification can become part of mathematical
practice rather than a philosophical curiosity [Gonthier 2008; Gonthier et al. 2013]. Hales’s
work on the Kepler conjecture and the Flyspeck project provide another paradigmatic case
in which proof, computation, formalization, and institutional trust became interdependent
[Hales 2008; Hales et al. 2017]. MacKenzie’s sociology of mechanized proof makes the same
point at the level of trust and risk: a machine-checked proof is not a disembodied certificate
but part of a culture of tools, experts, and conventions [MacKenzie 2001].
    Second, mathematical collaboration has sometimes exceeded the authorial small-group
format. The Polymath projects showed that distributed online collaboration could produce
serious mathematics [Gowers and Nielsen 2009; Polymath 2012]. Habgood-Coote and Tanswell
analyze the classification of finite simple groups as a case of group knowledge and mathematical
collaboration [Habgood-Coote and Tanswell 2023]. Such cases indicate that a mathematical
result can be known, maintained, and warranted by a group with a division of epistemic
labor. This is not yet studio mathematics in the post-LLM sense, but it weakens the idea
that the only relevant proof subject must be a single authorial agent.
    Third, formal libraries and proof assistants have introduced repository-based mathe-
matical memory. Lean 4 supports interactive theorem proving, and mathlib provides a
large communal library for Lean [de Moura and Ullrich 2021; mathlib Community 2020].
The Liquid Tensor Experiment is especially instructive. Its philosophical relevance is not
simply that a sophisticated mathematical result was formalized. It is that the work required
translation between informal expert understanding and formal dependencies, coordination
between mathematicians and formalizers, reliance on a public library ecology, and attention
to what the existing library could express [mathlib Community 2022; Commelin and Topaz
2024]. In such a case, the proof-producing unit is not exhausted by the author of the original
argument, the formalizer, the proof assistant, or mathlib considered separately. The unit is a
coupled practice in which conceptual mathematics, proof engineering, repository maintenance,
and machine checking interact. This is a near case of studio mathematics without needing
LLMs as its defining feature.
    Large language models enter this already transformed scene. AlphaGeometry, FunSearch,
and AlphaProof are not merely isolated technical achievements; they indicate that gener-
ation, search, formal language, reinforcement learning, and verification can be coupled in
mathematically significant ways [Trinh et al. 2024; Romera-Paredes et al. 2024; Hubert et al.


                                               6
2026]. Benchmarks such as miniF2F and PutnamBench further show that model-assisted
mathematical reasoning is increasingly evaluated through shared test environments and formal
targets [Zheng et al. 2022; Tsoukalas et al. 2024]. These developments matter philosophically
because they alter the ecology in which mathematical candidates are generated, filtered,
checked, and credited.


4    CIMA ecobionts as a descriptive ontology
The CIMA ecobiont is an organizing ontology, not a theorem. It is meant to describe a unit
of mathematical production when no single agent, text, or tool is sufficient to explain the
result’s production and warrant. Let

                                 E = ⟨H, T, S, I, R, V, A, Ω⟩,

where H is a set of human agents; T a set of technical systems; S the symbolic media; I
the institutional environment; R the material and computational resources; V the validation
regime; A the public actions and outputs; and Ω the task environment. An ecobiont
exists when these components are coupled around CIMA functions: computation, inference,
modeling, and action.
    This tuple is not intended to formalize mathematical practice in the strong sense of
yielding theorems. It is a disciplined schema for distinguishing production units. A seminar
group that discusses a conjecture, an LLM that proposes a proof sketch, and a proof assistant
that checks a Lean file are not by themselves the same kind of unit. They differ in coupling,
validation, memory, and responsibility. The tuple makes those differences visible.
    The schema becomes specifically mathematical only when the validation regime V is tied
to proof-sensitive norms. In other domains, validation may be empirical fit, audience response,
clinical outcome, or market uptake. In mathematics, V includes derivability, acceptable
informal gaps, formal checkability where available, explanatory adequacy, and uptake by
competent practitioners. Similarly, S is not any symbolic medium. It includes signs whose use
is governed by mathematical constraints: variables, definitions, diagrams, proof states, formal
terms, and lemmas with dependency structures. This is why the same CIMA vocabulary
can describe different ecobionts without erasing the distinctive normativity of mathematical
proof.




                                              7
                 Table 1: CIMA ecobiont components in mathematical
                 production.


   Component          Role                               Example in post-LLM mathe-
                                                         matics

   H Human agents   Judgment, taste, expertise, re- Mathematicians, formalizers, re-
                    sponsibility, interpretation.     viewers, software engineers, stu-
                                                      dents.
   T Technical sys- Generation, checking, search, LLMs, Lean, Coq, Isabelle, auto-
   tems             storage, automation.              mated provers, version control.
   S Symbolic me- Carriers of mathematical form. Natural language, notation,
   dia                                                proof states, formal code,
                                                      diagrams.
   I Institutions   Norms, incentives, certification, Universities, journals, confer-
                    resources.                        ences, grants, repositories.
   R Resources      Conditions of operation.          Compute, libraries, documenta-
                                                      tion, maintenance labor, time.
   V Validation     Warranted acceptance.             Peer review, expert reading, for-
                                                      mal checking, benchmark evalua-
                                                      tion.
   A Action         Stabilized outputs and uptake.    Papers, library contributions, for-
                                                      mal proofs, teaching material.
   Ω Task environ- Problem space and constraints. Conjectures, formalization gaps,
   ment                                               library dependencies, open prob-
                                                      lems.


   The key distinction is between a tool and a production unit. A proof assistant is a tool.
A large language model is a tool. A repository is a tool and an archive. A studio ecobiont is
the organized coupling through which these elements jointly produce mathematical outputs.
The same distinction helps avoid a common confusion in AI discourse. The question is not
whether an LLM understands a proof. The question is what role model output plays in a
wider system that includes formal checking, human interpretation, library context, and public
accountability.
   Human presence alone does not make such a system human-governed. Let H ∗ ⊆ H denote
the humans who are authorized and competent to stop release, revise the claim, inspect
decisive dependencies, and assume public responsibility. A studio is governed only if H ∗ is

                                             8
non-empty in practice, not merely on an organization chart. A ceremonial human who signs
a result but cannot reconstruct its decisive transitions does not supply epistemic governance.
This condition becomes the bridge between the descriptive CIMA tuple and the normative
account developed below.
    Governance is assessed relative to a public claim q, rather than assigned once to an entire
laboratory or platform. A studio is governed with respect to q only when five conditions hold:

 1. provenance: the route from source material, model output, code, formal dependencies,
    and human decisions to q is inspectable;

 2. reconstruction: at least one identified member of H ∗ can reconstruct the decisive reasoning
    at an appropriate level of granularity;

 3. challenge: H ∗ can diagnose a material error, assess its propagation, and test transfer to
    a nearby case;

 4. authority: H ∗ can stop release and can require revision or withdrawal; and

 5. responsibility: human participants publicly endorse only the claims within their compe-
    tence, disclose material dependencies, and enable independent scrutiny where licensing
    and privacy permit.

    The conditions are conjunctive for the claim being endorsed. Competence may be
distributed across a team, but each decisive dependency must map to an accountable human
and the team must be able to integrate those local judgments into a release decision. In
this paper, degenerate is a technical boundary term for a system that fails this rule while
continuing to present its outputs as governed human mathematics.
    This ontology also clarifies the relation to existing distributed cognition accounts. Clark
and Chalmers argue that parts of the environment may be constitutive of cognitive processes
under appropriate conditions [Clark and Chalmers 1998]; Hutchins shows that cognition can be
distributed across persons, artifacts, and environments [Hutchins 1995]. The CIMA ecobiont
is narrower. It concerns mathematically relevant production and warrant. Its distinctive
task is not to locate cognition in general, but to analyze when proof-production becomes a
coupled process of generation, formalization, validation, preservation, and responsibility.


5    Studio mathematics
Studio mathematics is a regime of mathematical production in which human expertise,
generative systems, formal verification, repository-based memory, software infrastructure, and

                                               9
institutional governance are coupled strongly enough that the product cannot be adequately
attributed to an isolated authorial act. The claim is not merely sociological. It concerns the
epistemic organization of warrant: how candidate arguments are generated, how errors are
detected, how derivations are checked, how explanation is recovered, and how responsibility
is assigned. The term studio is analogical, but the thesis is literal. The analogy with cinema
is useful because cinema distinguishes individual artistic vision from organized production:
scripts, actors, cameras, editing, funding, legal clearance, distribution, and reception [Becker
1982; Caves 2000; Caldwell 2008]. Hesse and Bartha emphasize that analogies are valuable
when the projected relation is made explicit rather than left as resemblance [Hesse 1966;
Bartha 2010]. Here the projected relation is division of production labor under a governed
regime of validation and public circulation. Mathematics and cinema do not share a truth
condition. They may share a production ontology.

                     Table 2: Five regimes of mathematical production.


   Regime                   Typical unit                   Main warranting form

   Authorial mathemat- Individual or small group.          Expert reading, exposition,
   ics                                                     proof tradition, peer review.
   Collaborative mathe- Coordinated group or com-          Distributed checking, testimony,
   matics               munity.                            shared expertise, public correc-
                                                           tion.
   Formal-                  Humans plus proof assis-       Machine checking,        formal
   computational            tants and formal libraries.    derivation, library dependency
   mathematics                                             management.
   Studio mathematics       Governed human-machine         Coupled generation, formal ver-
                            ecobiont.                      ification, repository memory,
                                                           expert interpretation, institu-
                                                           tional accountability.
   Degenerate      studio   Output-producing assem-        Performance, authority, or certi-
   mathematics              blage with ceremonial          fication without reconstructible
                            human oversight.               human understanding and ac-
                                                           countable release.


   This table marks a difference between studio mathematics and ordinary collaboration.
Collaboration can occur without formal systems or reusable repositories. Formalization can
occur without LLMs. LLM use can occur without verification. Studio mathematics requires


                                              10
the coupling. It is not mathematics with a chatbot. It is not proof automation alone. It
is a production regime in which candidate generation, formal checking, repository memory,
human explanation, and public responsibility are integrated. A degenerate studio has much
of the same technical surface but lacks the last two properties in a substantive form.
    For governance purposes, AI use should also be reported by intervention level rather than
by a binary disclosure. The prospective scale runs from L0, no generative system used, to
L5, end-to-end result generation with limited human reconstruction. Intermediate levels
distinguish clerical or literature support, local calculation and examples, proof search and
decomposition, and substantial proof generation followed by audit. The full scale appears
in the supplement. It reports how directly generation enters the justificatory path, not the
moral worth of a project.


5.1    A discriminating comparison of cases
The framework is useful only if it separates cases that differ in production and warrant.
Table 3 applies the same criteria to four documented episodes. The classifications concern
the publicly described workflows, not the private capacities or intentions of their participants.

                  Table 3: Comparative classification of mathematical pro-
                  duction cases.

Case                 Coupling and warrant            Evidence about H ∗      Classification

Polymath            Distributed online proof de-Human contributors           Collaborative
                    velopment, public discus-   supplied the argu-           mathematics, not
                    sion, correction, and con-  ments and public             a studio.
                    ventional mathematical argu-checking; no gener-
                    ment [Gowers and Nielsen    ative system occu-
                    2009; Polymath 2012].       pied the justificatory
                                                path.
Liquid Tensor Ex- Expert mathematics, Lean Identified           math-        Formal-
periment          formalization, public reposi- ematicians        and        computational
                  tory memory, proof engineer- formalizers retained          near case; it lacks
                  ing, and machine checking authority over trans-            the generative cou-
                  [mathlib Community 2022; lation, dependencies,             pling required by
                  Commelin and Topaz 2024]. and release.                     the strict studio
                                                                             definition.



                                               11
Case                Coupling and warrant            Evidence about H ∗       Classification

Danus matroid Multi-agent generation, fact-         The published de-        Studio     candi-
experiment    graph memory, a verifier,             scriptions establish     date; governance
              and a paper reported as               technical orchestra-     remains undeter-
              autonomously produced be-             tion but do not by       mined.
              fore the corresponding hu-            themselves establish
              man paper was public [Liu et          delayed reconstruc-
              al. 2026; Cheng et al. 2026;          tion, challenge per-
              Cheng 2026].                          formance, or collec-
                                                    tive authorization.
Jacobian coun- Model-generated counterex-           Verification may be      Boundary       case
terexample     ample, computational check-          possible while the       illustrating proxy
episode        ing, and an AI-assisted ex-          origin and digestion     rupture;     gover-
               planatory response, as de-           of the idea remain       nance      unestab-
               scribed by Weinreich [Wein-          heavily automated;       lished.
               reich 2026].                         the public record
                                                    cited here is insuffi-
                                                    cient to certify the
                                                    five conditions.


    The comparison blocks two easy inferences. Distributed authorship does not entail
studio mathematics, as Polymath shows. Technical orchestration does not entail governance,
as the Danus and Jacobian episodes show. The Liquid Tensor Experiment demonstrates
that repository memory, formal verification, and divided labor can deepen warrant without
requiring generative AI. Current evidence therefore supports a multidimensional classification,
not a historical claim that one regime has already replaced the others. AlphaGeometry,
FunSearch, and AlphaProof provide additional evidence that generation, search, formal
language, and verification can be coupled in constrained domains [Trinh et al. 2024; Romera-
Paredes et al. 2024; Hubert et al. 2026]; they do not settle the governance question.


6      Correctness, understanding, explanation, and taste
The shift to studio mathematics would be philosophically shallow if it meant only that
proofs can be checked by machines. Formal correctness matters, but it does not settle
the epistemology of proof. Weatherall and Wolfson argue that formal correctness is neither


                                              12
necessary nor sufficient for a proof’s epistemic value [Weatherall and Wolfson 2026]. That claim
fits a long line of work. Thurston emphasizes understanding. Rav emphasizes the epistemic
content of proofs. Azzouni emphasizes the relation between informal proofs and formal
derivations. Tanswell argues that dependence relations between informal and formal proofs
are not simple. Andersen analyzes acceptable gaps and testimony in ordinary mathematical
practice [Thurston 1994; Rav 1999; Azzouni 2004; Tanswell 2015; Andersen 2020; Andersen
et al. 2021].
    Studio mathematics therefore needs a layered account of proof. A proof may have at least
five layers.

 1. A generative layer, where conjectures, examples, proof routes, or formal sketches are
    proposed.

 2. A formal layer, where derivations are checked inside a proof assistant or related system.

 3. An expository layer, where humans explain why the result matters and how the argument
    works.

 4. A repository layer, where dependencies, versions, and reusable components are preserved.

 5. A communal layer, where peers evaluate significance, intelligibility, originality, and
    trustworthiness.

     These layers can come apart. A Lean file may be correct and yet opaque to many
mathematicians. An informal proof may be illuminating and yet contain gaps that need
filling. An LLM-generated sketch may be suggestive and wrong. A benchmark success may
show competence in one domain without supporting broader claims. Hallucination research
makes this point vivid: language models can produce fluent outputs that are not warranted
by evidence or derivation [Huang et al. 2025]. The studio response is not to trust models less
or more in the abstract. It is to assign each component an epistemic role and to prevent role
confusion.
     This distinction matters for explanation. If a formalized proof only certifies that a
derivation exists, it may fail to explain why a theorem is true or why a method is fruitful. If
an informal exposition explains but cannot be checked, it may fail under pressure. A strong
studio proof should not collapse explanation into verification. It should preserve both: formal
reliability where feasible, and human intelligibility where mathematics requires transmission,
teaching, extension, and conceptual use.
     It also matters for taste. Mathematical communities do not value all correct proofs equally.
They distinguish proofs that merely establish a result from proofs that reveal structure, unify

                                               13
cases, introduce fruitful definitions, or open new lines of inquiry. Studio mathematics can
support this judgment when it frees human attention from routine checking or exposes
dependency structures that were previously hidden. It can also weaken it if optimization for
benchmark success, tactic search, or formal completion displaces the search for conceptual
economy. The relevant question is therefore not whether a machine-checked proof is beautiful.
It is whether the ecobiont preserves a role for judgments of elegance, depth, and explanatory
force.


6.1    Degenerate studios and the epistemic agency floor
A degenerate studio is a proof-production ecobiont that can generate, certify, or circulate
mathematical claims while no accountable human or human group can exercise the relevant
epistemic agency over them. Degeneracy is therefore not equivalent to extensive automation.
A highly automated project may remain governed if authorized participants can inspect
dependencies, reconstruct the decisive reasoning, diagnose failure, and refuse release. Con-
versely, a nominally human-led project may be degenerate when the human role is restricted
to forwarding prompts, accepting certificates, or lending institutional status to outputs that
no responsible participant understands.
    This definition implies an epistemic agency floor. The proposed prospective understanding
audit tests four clusters: reconstruction of strategy and decisive transitions; identification
of assumptions, imported results, formal dependencies, and generated material; adversarial
error diagnosis and transfer to a nearby case; and authority to explain significance, revise
the claim, stop release, or withdraw it. The seven-dimension protocol, scoring fields, and
administration rules appear in the supplement. The instrument has not been validated as a
measure of mathematical understanding, has no validated pass threshold, and will require
field-specific calibration. Its present function is governance: it forces a project to name who
understands what, which dependencies are delegated, and where responsibility can interrupt
the pipeline.
    The audit also addresses the indistinguishability problem. In a conversational trace,
helping someone understand and saving them the work from which understanding would
have emerged may look nearly identical. The distinction becomes more visible only after the
conversation, when the participant must reconstruct, diagnose, transfer, and authorize without
treating the model transcript as an oracle. The protocol cannot guarantee understanding,
but it makes ceremonial oversight harder to confuse with epistemic agency.
    The proposal is intentionally prospective. A future benchmark could compare authorial,
assistive, governed-studio, and degenerate-studio workflows on retention, error diagnosis,


                                              14
transfer, originality, and time. Until such a benchmark exists, this paper makes no causal
claim that governed studios outperform authorial practice. The present contribution is to
define the comparison and its failure conditions.


7     Credit, testimony, and responsibility
A change in the unit of production creates a change in the unit of credit. Traditional
authorship already struggles with large collaborations, software, data, and infrastructure. In
studio mathematics the problem becomes more acute. A result may involve conceptual design,
problem decomposition, model prompting, proof search, formalization, library maintenance,
software engineering, review, documentation, and exposition. Treating all of this as either
“authorship” or “acknowledgment” is too crude.
    The social epistemology of mathematics is directly relevant. Andersen, Andersen, and
Sørensen argue that testimony plays a role in mathematics [Andersen et al. 2021]. Habgood-
Coote and Tanswell analyze group knowledge in the classification of finite simple groups
[Habgood-Coote and Tanswell 2023]. Rittberg, Tanswell, and Van Bendegem show that
epistemic injustice can occur in mathematical practice [Rittberg et al. 2020]. Work on
authorship in philosophy of science further shows that author lists are not merely decorative:
they distribute responsibility, recognition, and authority [Andersen et al. 2024].
    Studio mathematics should therefore distinguish at least five kinds of contribution.

 1. Conceptual contribution: posing the problem, choosing definitions, identifying the strategy.

 2. Generative contribution: producing candidate lemmas, sketches, examples, or search
    paths.

 3. Formal contribution: encoding and checking derivations in a proof assistant.

 4. Infrastructural contribution: maintaining libraries, tools, datasets, environments, and
    documentation.

 5. Interpretive contribution: explaining, simplifying, evaluating, and contextualizing the
    result.

   These categories need not map mechanically onto authorship positions. They provide a
vocabulary for responsibility. If model-generated content materially shaped a proof route, that
use should be documented. If library maintainers made a result possible through substantial
formal infrastructure, that labor should be visible. If a proof depends on a proprietary system
that others cannot inspect, the epistemic status of the claim differs from that of an openly

                                              15
checkable artifact. The aim is not bureaucracy. The aim is to align credit with epistemic
labor.
   Contribution and epistemic authority should therefore be represented on separate axes.
For participant i, let
                                      Ci = (Pi , Ei ),

where Pi records productive contributions and Ei records the scope of claims that the partici-
pant is competent and authorized to endorse. A library maintainer may have high productive
importance without claiming authority over the theorem’s significance. A conceptual lead
may have broad interpretive authority while relying on formalizers for local certificates. A
model may be causally productive without being a bearer of testimony or responsibility. The
two-axis representation prevents the false choice between granting conventional authorship to
every enabling contribution and making infrastructure invisible.
    Weinreich’s suggestion that ideas might be co-owned by anyone who demonstrates au-
thoritative understanding points toward a valuable correction to paper-centered authorship
[Weinreich 2026]. It treats understanding as something to be demonstrated rather than
inferred from a byline. Yet understanding cannot be the only source of credit. Formalization,
maintenance, dataset construction, and software engineering may deserve recognition even
when their contributors do not claim authoritative understanding of the whole result. The
dual-axis model retains the insight while making room for infrastructural labor.
    A minimal governance standard would require a contribution and authority trace, not
merely a final author list. Such a trace would record which parts of a proof were proposed
informally, generated computationally, checked formally, imported from existing libraries,
modified during review, or dependent on non-public systems. It would also identify who may
authorize each major claim and who can stop release. The trace need not be exhaustive. It
should be sufficient for competent readers to understand the epistemic route from conjecture
to public artifact. This also helps distinguish credit from responsibility: a contributor may
deserve credit for infrastructure without being responsible for the theorem’s exposition, and
a conceptual author may remain responsible for claims of significance even when formal
checking is delegated.


8    Conditional antifragility
The vocabulary of antifragility should be used carefully. Studio mathematics is not automati-
cally better because it is distributed, formal, or model-assisted. It may be fragile. It may
concentrate power in groups with access to compute, proprietary models, and engineering


                                             16
support. It may create brittle dependencies. It may encourage trust inflation, where formal-
looking artifacts receive more authority than they deserve. It may also create maintenance
burdens that are poorly rewarded.
   A precise use of antifragility avoids this problem. Let

                                           {S, P, U }

name a system, a class of perturbations, and a utility measure. In this setting, S is a
proof-production ecobiont; P includes counterexamples, failed formalizations, hallucinated
steps, broken dependencies, adversarial peer review, benchmark failures, automation shocks,
rapid mass generation, deskilling pressure, and proprietary lock-in; U includes reliability,
intelligibility, retained human understanding, epistemic agency, institutional independence,
documentation quality, library robustness, reusable components, and fair attribution. Follow-
ing resilience and antifragility work [Holling 1973; Taleb 2012; Monperrus 2017; Equihua et
al. 2020; Axenie et al. 2023], studio mathematics is antifragile only when perturbations in P
systematically improve U .
    This condition is demanding. A failed formalization is useful only if it reveals a gap,
improves a definition, strengthens a library, or documents a limitation. An LLM hallucination
is useful only if the system can detect it and use it as negative evidence or a prompt for
refinement. Peer review is useful only if it improves correctness and understanding rather
than merely imposing conservatism. A benchmark failure is useful only if it updates models,
methods, or claims. Conditional antifragility is therefore a normative design principle: build
proof ecobionts that learn from disorder without mistaking disorder for progress.
    Four operational conditions follow. First, perturbations must be retained: failures, gaps,
and dependency breaks should leave inspectable traces. Second, perturbations must be
selected: not every failure is informative, and the system needs criteria for distinguishing
noise from useful stress. Third, perturbations must be converted: a detected gap should
become a corrected proof, a better lemma, a library improvement, a benchmark update,
or a revised claim. Fourth, conversion must be public enough to support trust: if only a
private model or closed platform learns from the failure, the mathematical community may
not gain the relevant utility. On this reading, antifragility is not a property of LLM use. It is
a property of governed error conversion.
    Ashby’s law of requisite variety helps explain why this matters [Ashby 1956]. A system
can regulate disturbances only if it has enough internal variety. In studio mathematics, variety
comes from combining human experts, formal systems, repositories, independent checkers,
open review, and maintenance practices. But variety without governance can produce noise.


                                               17
The design problem is to create enough heterogeneity to detect error, enough structure to
preserve trust, and enough openness to correct the system.


9    Institutional ecology and protected mathematical
     practice
The crisis objection is institutional as well as epistemic. Public support for mathematicians
is easier to defend when mathematical workers are visibly necessary to discovery, verification,
teaching, and stewardship. If institutions treat machine-generated output as a substitute
for mathematical employment, then even a technically successful system can damage the
community that makes its outputs intelligible and trustworthy. Weinreich is right that this
cannot be answered by saying that mathematicians may simply choose to keep practicing for
intrinsic reasons [Weinreich 2026]. Time, positions, journals, and training environments are
material conditions of that practice.
    Total opposition, however, does not follow. If high-capability systems diffuse regardless
of individual abstention, a single prohibition can turn refusal into an exclusion mechanism
while leaving the surrounding political economy unchanged. The more defensible response is
a plural institutional ecology with protected authorial practice, governed studio practice, and
explicit barriers against degenerate production. The Leiden Declaration supplies an emerging
community-level commitment to responsible AI use, while Tao’s account of mathematical
AI emphasizes adaptation of norms and workflows rather than a single technological destiny
[Alper et al. 2026; Tao 2026].
    Protected practice can take several forms. Journals and conferences can create disclosure
classes rather than a binary AI label. Hiring and training can value oral reconstruction, error
diagnosis, conceptual contribution, formalization, and maintenance instead of treating paper
counts as a complete proxy. Funders can support open proof infrastructure and compute
access so that studio mathematics does not become proprietary by default. Departments
can preserve spaces in which students solve problems without generative assistance, because
formative practice and production efficiency are different goods. Communities can also
maintain venues for explicitly authorial mathematics. These arrangements are not attempts
to stop technical development. They are ways of keeping mathematical agency, diversity of
practice, and public accountability inside the institutional objective function.
    No single governance regime should be universal. Some domains will remain primarily
authorial; some formalization projects will be collective but not generative; some discovery
programs will become studio-like. The relevant red line is not tool use but degeneracy:


                                              18
acceptance of results whose human sponsors cannot meet the applicable epistemic agency
floor. That boundary also clarifies why the economic and existential-risk debates should
not be conflated. Catastrophic AI risk may be important, but it requires different premises
and policies. The present argument concerns the nearer institutional design of mathematical
practice.
    Formal Concept Analysis remains available as an optional representational tool in the
supplement [Ganter and Wille 1999]. It maps which attributes close the proposed taxonomy,
but it is neither evidence for the thesis nor a premise of the institutional argument. The
supplement also provides a claim ledger, a robustness and heterogeneity map, and figure files.
The main philosophical case is text-centered and survives without them.


10     Objections
Objection 1: Studio mathematics is just collaboration under a new name. Collaboration is
part of the story, but not the whole story. Studio mathematics requires a specific coupling
of generative systems, formal verification, repository memory, human interpretation, and
institutional responsibility. A collaborative seminar without those features is not studio
mathematics. A solo proof formalized in Lean may be formal-computational without being
studio-like. The studio category is narrower than sociality and broader than automation.
    Objection 2: The cinema analogy is unnecessary. The analogy is not load-bearing. It
is heuristic. It helps mark the difference between authorial production and coordinated
production. The literal claim is about proof-production units: a governed human-machine
assemblage can become epistemically relevant in ways that an individual author alone is not.
The argument would survive without the cinema analogy.
    Objection 3: Formal proof already solved the problem. Formal proof solves one problem:
checking derivations relative to a formal system. It does not by itself solve explanation,
significance, surveyability, testimony, authorship, or responsibility. That is why a studio
proof must be layered rather than merely certified.
    Objection 4: LLMs are unreliable and should not be part of proof practice. LLM outputs
are unreliable when treated as warranted mathematical assertions. They may still be useful
as generators of candidates, examples, search paths, or expository drafts, provided their
status is recorded and their outputs are checked. The framework distinguishes generation
from verification precisely to prevent unwarranted trust.
    Objection 5: Authorial mathematics remains superior for deep understanding. It may
be superior in many cases. The thesis is not replacement. It is pluralization. Authorial
mathematics, collaborative mathematics, formal-computational mathematics, and studio

                                             19
mathematics can coexist. The value of each depends on the mathematical task, the standards
of explanation, and the available validation practices.
    Objection 6: Studio mathematics threatens mathematical beauty. It can. A production
regime optimized for formal completion, tactic success, or benchmark performance may
marginalize elegance and explanatory economy. But the same regime can also support
aesthetic judgment by exposing dependencies, eliminating routine uncertainty, and freeing
attention for conceptual organization. The issue is not whether studio mathematics is
intrinsically beautiful or ugly. It is whether its governance preserves space for mathematical
taste as an epistemic virtue.
    Objection 7: The chess intermediary has not played the game. Weinreich’s analogy is
decisive against one weak notion of achievement: a novice who merely relays moves between
stronger players has not thereby defeated a grandmaster [Weinreich 2026]. The same holds
for a person who submits model output without understanding it. This is precisely the
degenerate-studio case. But the analogy does not cover every distributed practice. A director,
formalizer, reviewer, or library maintainer may contribute neither the first move nor the final
certificate while still exercising skilled judgment that changes the mathematical product. The
contribution and authority trace is meant to separate these roles from mere intermediation.
    Objection 8: If the model can also digest and explain the proof, the human role disappears.
Model-assisted exposition can indeed undermine a proposal that reserves “digestion” as the
final human monopoly. The studio account therefore does not define human agency by an
unautomated task. It defines it by reconstructible competence, authority to intervene, and
responsibility for public action. A model may help a participant acquire that competence;
the audit asks whether the competence persists when challenged by diagnosis and transfer. If
no human can meet the floor, the result may still be formally correct, but it should not be
represented as a governed human mathematical achievement.
    Objection 9: Governance will not prevent labor displacement or institutional capture.
Correct. A contribution trace and an understanding audit are not labor policy. They can
make displacement and dependence visible, but they cannot by themselves preserve jobs,
distribute compute, or constrain platforms. That is why the institutional ecology requires
protected training, open infrastructure, plural venues, and evaluation practices that do not
reward output volume alone. These proposals are partial safeguards, not a prediction that
the transition will be benign.




                                              20
11     Conclusion
The post-LLM transformation of mathematics is not best understood as the arrival of artificial
mathematicians. It is better understood as a change in the possible unit of proof-production.
Mathematics can still be authored in a literary mode: a person or small group develops
a proof through language, notation, judgment, and style. That mode remains central to
mathematical understanding. But another mode is now technically credible. In studio
mathematics, proof-production is distributed across human expertise, generative systems,
proof assistants, formal libraries, repositories, and institutions. The relevant distinction is
therefore not authorial versus automated mathematics, but authorial, governed studio, and
degenerate studio practice.
    The CIMA ecobiont ontology provides a disciplined way to describe this shift. It does not
deny existing accounts of mathematical practice, distributed cognition, formal proof, or group
knowledge. It builds on them to analyze a new coupling of generation, formal verification,
repository memory, explanation, credit, and responsibility. Its mathematical specificity lies
in the fact that this coupling remains constrained by proof, necessity, intelligibility, and
taste. The epistemic agency floor, the prospective understanding audit, and the contribution-
authority trace specify what “human-governed” must mean if it is to be more than a slogan.
    The appropriate conclusion is plural rather than triumphalist or prohibitionist. Commu-
nities should preserve authorial practice, develop governed studios where their benefits are
real, and refuse to represent degenerate output pipelines as understood human mathematics.
Whether governed studios improve learning, originality, reliability, or resilience remains an
empirical question. The paper has defined the comparison, not settled it. The philosophical
issue is how mathematical agency, trust, understanding, and judgment should be organized
when proof becomes a collective, formal, verifiable, and infrastructural artifact.


Tool and computational resource disclosure
Generative AI systems were used during development of this manuscript for literature triage,
argument mapping, language revision, LaTeX editing, and generation of reproducibility
scripts. The human author defined the research question and framework, selected the claims
advanced, and retains responsibility for the interpretations, references, classifications, and
final text. No claim is treated as established because it was generated or endorsed by a model.
The supplementary package records claim status, source checks, decision rules, and the limits
of the unexecuted validation program.



                                              21
References
Alper, Jarod. 2026. Embracing AI and formalization: Experimenting with tomorrow’s
  mathematical tools. Bulletin of the American Mathematical Society, 63(2): 177–197.
  doi:https://doi.org/10.1090/bull/1879.

Andersen, Line Edslev. 2020. Acceptable gaps in mathematical proofs. Synthese, 197(1):
 233–247. doi:https://doi.org/10.1007/s11229-018-1778-8.

Andersen, Line Edslev, Andersen, Hanne, Sørensen, Henrik Kragh. 2021. The role of testimony
 in mathematics. Synthese, 199(1–2): 859–870. doi:https://doi.org/10.1007/s11229-0
 20-02734-9.

Ashby, W. Ross. 1956. An Introduction to Cybernetics. Chapman and Hall. London.

Avigad, Jeremy. 2021. Reliability of mathematical inference. Synthese, 198(8): 7377–7399.
  doi:https://doi.org/10.1007/s11229-019-02524-y.

Axenie, Cristian, López-Corona, Oliver, Makridis, Michail A., Akbarzadeh, Meisam, Saveriano,
  Matteo, Stancu, Alexandru, West, Jeffrey. 2023. Antifragility as a complex system’s response
  to perturbations, volatility, and time. arXiv:2312.13991.

Azzouni, Jody. 2004. The derivation-indicator view of mathematical practice. Philosophia
 Mathematica, 12(2): 81–106. doi:https://doi.org/10.1093/philmat/12.2.81.

Bartha, Paul F. A. 2010. By Parallel Reasoning: The Construction and Evaluation of
 Analogical Arguments. Oxford University Press. Oxford.

Becker, Howard S. 1982. Art Worlds. University of California Press. Berkeley.

Burgess, John P., De Toffoli, Silvia. 2022. What is mathematical rigor? Aphex, 25: 1–17.

Caldwell, John Thornton. 2008. Production Culture: Industrial Reflexivity and Critical
 Practice in Film and Television. Duke University Press. Durham, NC.

Caves, Richard E. 2000. Creative Industries: Contracts between Art and Commerce. Harvard
  University Press. Cambridge, MA.

Cheng, Ronnie. 2026. Tangent classes for matroid building sets. arXiv:2606.22650.

Cheng, Ronnie, Liu, Shurui, Gao, Guoxiong. 2026. Tangent classes of matroids and wonderful
  compactifications. arXiv:2607.05835.


                                             22
Clark, Andy, Chalmers, David. 1998. The extended mind. Analysis, 58(1): 7–19. doi:https:
  //doi.org/10.1093/analys/58.1.7.

Commelin, Johan, Topaz, Adam. 2024. Abstraction boundaries and spec driven development
  in pure mathematics. Bulletin of the American Mathematical Society, 61(2): 241–255.
  doi:https://doi.org/10.1090/bull/1831.

The mathlib Community. 2020. The Lean mathematical library. In Proceedings of the 9th
 ACM SIGPLAN International Conference on Certified Programs and Proofs. Pages 367–381.
 ACM. doi:https://doi.org/10.1145/3372885.3373824.

The mathlib Community. 2022. Completion of the Liquid Tensor Experiment. Lean Prover
 Community blog. https://leanprover-community.github.io/blog/posts/lte-final
 /.

National Research Council. 2015. Enhancing the Effectiveness of Team Science. The National
 Academies Press. Washington, DC. doi:https://doi.org/10.17226/19007.

de Moura, Leonardo, Ullrich, Sebastian. 2021. The Lean 4 theorem prover and programming
  language. In Automated Deduction - CADE 28. Pages 625–635. Springer. Cham. doi:https:
  //doi.org/10.1007/978-3-030-79876-5_37.

de Solla Price, Derek J. 1963. Little Science, Big Science. Columbia University Press. New
  York.

De Toffoli, Silvia. 2021. Groundwork for a fallibilist account of mathematics. The Philosophical
 Quarterly, 71(4): 823–844. doi:https://doi.org/10.1093/pq/pqaa076.

Equihua, Miguel, Espinosa Aldama, Mariana, Gershenson, Carlos, López-Corona, Oliver,
  Munguía, Mariana, Pérez-Maqueo, Octavio, Ramírez-Carrillo, Elvia. 2020. Ecosystem
  antifragility: beyond integrity and resilience. PeerJ, 8: e8533. doi:https://doi.org/10.7
  717/peerj.8533.

Ganter, Bernhard, Wille, Rudolf. 1999. Formal Concept Analysis: Mathematical Foundations.
 Springer. Berlin. doi:https://doi.org/10.1007/978-3-642-59830-2.

Gilbert, Scott F., Sapp, Jan, Tauber, Alfred I. 2012. A symbiotic view of life: We have
  never been individuals. The Quarterly Review of Biology, 87(4): 325–341. doi:https:
  //doi.org/10.1086/668166.

Gonthier, Georges. 2008. Formal proof - the four color theorem. Notices of the American
 Mathematical Society, 55(11): 1382–1393.

                                              23
Gonthier, Georges, Asperti, Andrea, Avigad, Jeremy, Bertot, Yves, Cohen, Cyril, Garillot,
 François, Le Roux, Stéphane, Mahboubi, Assia, O’Connor, Russell, Ould Biha, Sidi, Pasca,
 Ioana, Rideau, Laurence, Solovyev, Alexey, Tassi, Enrico, Théry, Laurent. 2013. A machine-
 checked proof of the odd order theorem. In Interactive Theorem Proving. Pages 163–179.
 Springer. doi:https://doi.org/10.1007/978-3-642-39634-2_14.

Gowers, Timothy, Nielsen, Michael. 2009. Massively collaborative mathematics. Nature, 461:
 879–881. doi:https://doi.org/10.1038/461879a.

Habgood-Coote, Joshua, Tanswell, Fenner Stanley. 2023. Group knowledge and mathematical
  collaboration: A philosophical examination of the classification of finite simple groups.
 Episteme, 20(2): 281–307. doi:https://doi.org/10.1017/epi.2021.26.

Andersen, Line Edslev, Bailey, Rosemary, Bhatia, Udit, Burch-Brown, Joanna, Bright, Liam
 Kofi, Brooke, Jim, Cameron, Peter, Campbell-Moore, Catrin, Cornelli, Joe, Crowley,
 Stephen, Dang, Haixin, Fraser, Rachel, Falconer, Isobel, Ferner, Adam, Gamez, Monica,
 Gerken, Mikkel, Hawley, Katherine, Heyman, Matthias, Kappel, Klemens, Landes, Ethan,
 Landemore, Hélène, Loewe, Benedikt, Lunt, Dan, Martin, Ursula, Meyns, Chris, Millard,
 Louise, Mitchell, Dann, Okasha, Samir, Peet, Andrew, Pettigrew, Richard, de Ridder,
 Jeroen, Ross, Robert, Saint-Germier, Pierre, Simion, Mona, Skatova, Anya, Tanswell,
 Fenner, Whiting, Daniel, Wilson, Alan, Wray, K. Brad, Yeşilova, Dilara, Habgood-Coote,
 Joshua. 2024. What’s the point of authors? The British Journal for the Philosophy of
 Science, 75(2): 487–517. doi:https://doi.org/10.1086/715539.

Hales, Thomas C. 2008. Formal proof. Notices of the American Mathematical Society, 55(11):
 1370–1380.

Hales, Thomas, Adams, Mark, Bauer, Gertrud, Dang, Tat Dat, Harrison, John, Hoang,
 Truong Le, Kaliszyk, Cezary, Magron, Victor, McLaughlin, Sean, Nguyen, Tat Thang,
 Nguyen, Truong Quang, Nipkow, Tobias, Obua, Steven, Pleso, Joseph, Rute, Jason,
 Solovyev, Alexey, Ta, An Hoai Thi, Tran, Trung Nam, Trieu, Diep Thi, Urban, Josef, Vu,
 Ky Khac, Zumkeller, Roland. 2017. A formal proof of the Kepler conjecture. Forum of
 Mathematics, Pi, 5: e2. doi:https://doi.org/10.1017/fmp.2017.1.

Hardy, G. H. 1940. A Mathematician’s Apology. Cambridge University Press. Cambridge.

Hesse, Mary B. 1966. Models and Analogies in Science. University of Notre Dame Press.
  Notre Dame.



                                            24
Holling, C. S. 1973. Resilience and stability of ecological systems. Annual Review of Ecology and
 Systematics, 4: 1–23. doi:https://doi.org/10.1146/annurev.es.04.110173.000245.

Huang, Lei, Yu, Weijiang, Ma, Weitao, Zhong, Weihong, Feng, Zhangyin, Wang, Haotian,
 Chen, Qianglong, Peng, Weihua, Feng, Xiaocheng, Qin, Bing, Liu, Ting. 2025. A survey
 on hallucination in large language models: Principles, taxonomy, challenges, and open
 questions. ACM Transactions on Information Systems, 43(2): Article 42. doi:https:
 //doi.org/10.1145/3703155.

Hubert, Thomas, Mehta, Rishi, Sartran, Laurent, et al. 2026. Olympiad-level formal
 mathematical reasoning with reinforcement learning. Nature, 651: 607–613. doi:https:
 //doi.org/10.1038/s41586-025-09833-y.

Hutchins, Edwin. 1995. Cognition in the Wild. MIT Press. Cambridge, MA.

Lakatos, Imre. 1976. Proofs and Refutations: The Logic of Mathematical Discovery. Cambridge
  University Press. Cambridge.

López-Corona, Oliver, Ramírez-Carrillo, Elvia, Magallanes-Guijón, Gustavo. 2019. The
  rise of the technobionts: toward a new ontology to understand current planetary crisis.
  Researchers.One. https://www.researchers.one/article/2019-01-1.

MacKenzie, Donald. 2001. Mechanizing Proof: Computing, Risk, and Trust. MIT Press.
 Cambridge, MA.

Margulis, Lynn, Fester, René, editors. 1991. Symbiosis as a Source of Evolutionary Innovation:
 Speciation and Morphogenesis. MIT Press. Cambridge, MA.

Monperrus, Martin. 2017. Principles of antifragile software. In Companion Proceedings of
 the 1st International Conference on the Art, Science, and Engineering of Programming
 (Programming ’17). Article 32, 4 pages. ACM. doi:https://doi.org/10.1145/3079368.
 3079412.

D. H. J. Polymath. 2012. A new proof of the density Hales-Jewett theorem. Annals of
  Mathematics, 175(3): 1283–1327.

Rav, Yehuda. 1999. Why do we prove theorems? Philosophia Mathematica, 7(1): 5–41.
  doi:https://doi.org/10.1093/philmat/7.1.5.

Rittberg, Colin Jakob, Tanswell, Fenner Stanley, Van Bendegem, Jean Paul. 2020. Epistemic
  injustice in mathematics. Synthese, 197(9): 3875–3904. doi:https://doi.org/10.1007/
  s11229-018-01981-1.

                                               25
Romera-Paredes, Bernardino, Barekatain, Mohammadamin, Novikov, Alexander, Balog,
 Matej, Kumar, M. Pawan, Dupont, Emilien, Ruiz, Francisco J. R., Ellenberg, Jordan S.,
 Wang, Pengming, Fawzi, Omar, Kohli, Pushmeet, Fawzi, Alhussein. 2024. Mathematical
 discoveries from program search with large language models. Nature, 625: 468–475. doi:ht
 tps://doi.org/10.1038/s41586-023-06924-6.

Taleb, Nassim Nicholas. 2012. Antifragile: Things That Gain from Disorder. Random House.
  New York.

Tanswell, Fenner Stanley. 2015. A problem with the dependence of informal proofs on formal
  proofs. Philosophia Mathematica, 23(3): 295–310. doi:https://doi.org/10.1093/philma
  t/nkv008.

Tanswell, Fenner Stanley. 2024. Mathematical Rigour and Informal Proof. Cambridge Univer-
  sity Press. Cambridge.

Tao, Terence. 2026. Mathematics in the age of AI. arXiv:2608.16753.

Liu, Jihao, Gao, Guoxiong, Sun, Zeming, Wu, Bin, Liu, Shurui, Jiang, Jiedong, Ju, Haocheng,
  Chen, Leheng, Cheng, Ronnie, Zhang, Xiping, Dong, Bin. 2026. Danus: Orchestrating
  mathematical reasoning agents with fact-graph memory. arXiv:2607.06447.

Alper, Jarod, Barany, Michael, Chavarri Villarello, Alain, Dahmen, Sander, Dean, Walter,
  Ganapathy, Karthik, Harris, Michael, Holmes, David, Jamnik, Mateja, Kelk, Steven, Kra,
  Bryna, Martin, Ursula, Naskręcki, Bartosz, Ochigame, Rodrigo, Portegies, Jim, Schmitt,
  Johannes. 2026. Leiden Declaration on Artificial Intelligence and Mathematics. Version 1,
  2 June 2026. Zenodo. doi:https://doi.org/10.5281/zenodo.20302944.

Thurston, William P. 1994. On proof and progress in mathematics. Bulletin of the American
 Mathematical Society, 30(2): 161–177. doi:https://doi.org/10.1090/S0273-0979-199
  4-00502-6.

Trinh, Trieu H., Wu, Yuhuai, Le, Quoc V., He, He, Luong, Thang. 2024. Solving olympiad
  geometry without human demonstrations. Nature, 625: 476–482. doi:https://doi.org/10
  .1038/s41586-023-06747-5.

Tsoukalas, George, Lee, Jasper, Jennings, John, Xin, Jimmy, Ding, Michelle, Jennings,
  Michael, Thakur, Amitayush, Chaudhuri, Swarat. 2024. PutnamBench: Evaluating Neural
  Theorem-Provers on the Putnam Mathematical Competition. In Advances in Neural
  Information Processing Systems.


                                            26
Tymoczko, Thomas. 1979. The four-color problem and its philosophical significance. The
 Journal of Philosophy, 76(2): 57–83. doi:https://doi.org/10.2307/2025976.

Venkatesh, Akshay. 2024. Some thoughts on automation and mathematical research. Bulletin
  of the American Mathematical Society, 61(2): 203–210. doi:https://doi.org/10.1090/bu
  ll/1834.

Weatherall, James Owen, Wolfson, Jesse. 2026. Correctness, artificial intelligence, and the
 epistemic value of mathematical proof. arXiv:2602.12463.

Weinreich, Max. 2026. The crisis of AI-generated mathematics. arXiv:2608.02859.

Zheng, Kunhao, Han, Jesse Michael, Polu, Stanislas. 2022. miniF2F: a cross-system bench-
  mark for formal Olympiad-level mathematics. In International Conference on Learning
  Representations.




                                            27
                  Supplementary Information
     MIAT-MD audit, governance protocols, and optional representations
                                        Version 2.6.1




S1     Status, scope, and nonclaims
This supplement exposes the inferential architecture of version 2.6.1. It separates four
layers: ontology (what entities and regimes are being defined), epistemology (what counts
as correctness, understanding, authority, and responsibility), methodology (how those
distinctions could be audited), and application (what the framework suggests for current
systems and institutions). It also records the comparative case matrix and the staged
validation program. A definition is not treated as evidence, a diagram is not treated as a
result, and a model output is not promoted to an inference merely because it is fluent or
formally shaped.
The understanding audit, AI-use scale, contribution-authority trace, and proposed benchmark
are prospective. They have not been validated psychometrically or causally. The FCA and
robustness outputs are representations computed from a disclosed hand-coded context. They
do not establish that the ontology is true. No claim is made that governed studios outperform
authorial practice.


S2     Evidence contract
Every substantive claim receives a stable ID and records the following fields:

   Field              Function
   Claim ID         Stable identifier used across manuscript, ledgers, scripts, and audit
                    outputs.
   Layer            Ontology, epistemology, methodology, or application.
   Claim type       Definitional, literature-supported, conceptual, normative, empirical
                    example, or prospective hypothesis.
   Evidence basis   Source, argument, example, or explicit statement that evidence is
                    absent.
   Validation route What could check, challenge, or falsify the claim at the appropriate
                    level.
   RHM status       ROBUST_CORE,                  SPURIOUS_ENVELOPE,                   or
                    LEGITIMATE_OPEN_UNCERTAINTY.
   Uncertainty      Low, medium, or high, interpreted qualitatively.



                                             28
   POST_HOC          Marker for analyses or criteria introduced after inspecting outcomes.
                     No claim in this release is marked post hoc because no outcome
                     benchmark has been run.



S3        AI-use disclosure scale
The scale reports where generative systems enter the justificatory path. It does not rank
ethical worth and should be accompanied by a plain-language tool disclosure.

     Level   Intervention                Minimum disclosure
     L0      No generative system used. State whether conventional software, search, or
                                         proof assistants were used.
     L1      Clerical or literature sup- Tool, date/version when available, and tasks
             port.                       such as search, formatting, or language editing.
     L2      Local calculation or exam- Prompts or procedures material to examples,
             ple support.                code, calculations, or counterexamples; inde-
                                         pendent checks.
     L3      Proof search or decomposi- Candidate lemmas, search paths, discarded sug-
             tion.                       gestions, and verification route.
     L4      Substantial proof or formal Generated sections, formal dependencies, audit
             derivation generation fol- record, responsible human, and stop authority.
             lowed by audit.
     L5      End-to-end result genera- Full provenance and an explicit warning that
             tion with limited human re- the epistemic agency floor has not been met.
             construction.



S4        Operational governance rule
Governance is classified relative to an endorsed public claim q. A project is governed with
respect to q only when all five conditions below are documented. A laboratory, platform, or
author list does not receive a permanent global classification.

  ID         Condition             Observable record
  GR1        Provenance            Sources, model outputs, code, formal dependencies,
                                   and material human decisions can be traced to the
                                   released claim.
  GR2        Reconstruction        At least one identified member of H ∗ can reconstruct
                                   the decisive reasoning at field-appropriate granularity.
  GR3        Challenge             H ∗ can diagnose a material error, trace its effects, and
                                   test transfer to a nearby case.


                                             29
   GR4       Authority              H ∗ has an effective right to stop release and require
                                    revision or withdrawal.
   GR5       Responsibility         Human participants delimit the claims they endorse,
                                    disclose material dependencies, and enable indepen-
                                    dent scrutiny where licensing and privacy permit.

Classification is conjunctive for the claim under review. Distributed competence is permitted,
but every decisive dependency must map to an accountable human, and the group must
demonstrate an integration path from local judgments to the release decision. Failure of
a condition classifies the workflow as ungoverned with respect to that claim. The term
degenerate studio is reserved for an ungoverned workflow that nevertheless represents its
output as governed human mathematics.


S5       Claim ledger
The machine-readable ledger is data/claims.csv. The compact view below records the main
claim and its present status.

  ID     Layer            Claim                                            RHM status
  C01    Ontology         CIMA tuple represents a proof-production eco- Robust core
                          biont.
  C02    Ontology         Studio mathematics is a regime, not mere LLM Robust core
                          use.
  C03    Ontology         Degenerate studios have output capability with- Robust core
                          out substantive human governance.
  C04    Epistemology     Correctness is not sufficient for understanding or Robust core
                          epistemic value.
  C05    Epistemology     Human presence is insufficient without recon- Robust core
                          structive authority.
  C06    Epistemology     Conversation alone may not distinguish learning Robust core
                          from bypass.
  C07    Methodology      An understanding audit can operationalize an Open           uncer-
                          agency floor.                                      tainty
  C08    Methodology      Disclosure should use intervention levels rather Robust core
                          than a binary label.
  C09    Methodology      Contribution and epistemic authority require sep- Robust core
                          arate axes.
  C10    Application      Fact-graph systems demonstrate technical orches- Robust core
                          tration.
  C11    Application      Orchestration does not entail understanding or Robust core
                          responsibility.
  C12    Application      Governed studios outperform authorial work- Open            uncer-
                          flows.                                             tainty

                                             30
  ID     Layer            Claim                                             RHM status
  C13    Application      Plural institutions better preserve agency than Open     uncer-
                          uniform regimes.                                  tainty
  C14    Application      Protected authorial practice remains valuable. Robust core
  C15    Methodology      FCA is optional representation, not evidence. Robust core
  C16    Methodology      RHM separates robust, spurious, and legiti- Robust core
                          mately open claims.
  C17    Methodology      Governance requires provenance, reconstruction, Robust core
                          challenge, authority, and responsibility for each
                          endorsed claim.
  C18    Application      A common case matrix separates collaboration, Robust core
                          formalization, orchestration, and governance.
  C19    Methodology      Corpus-scale MIAT-MD requires a frozen code- Robust core
                          book and validated gold set before scaling.


The label “robust core” means that a claim survives the distinctions and challenges represented
in this audit. It does not mean the claim has been empirically proven. In this release 16
claims are in the robust core, three are legitimate open uncertainties, and none is assigned to
the spurious envelope. The empty spurious class is a current audit result, not a guarantee
against future demotion.


S6      Comparative case matrix
The machine-readable table is data/case_matrix.csv. “Unreported” means that the cited
public record does not establish the condition; it does not assert that the relevant competence
or authority was absent in private.

 Case                Generative    cou- Formal or repos- Evidence about Classification
                     pling              itory coupling   H∗
 Polymath Gowers None in the docu- Public           dis- Strong public Collaborative,
 and Nielsen [2009]; mented workflow. cussion      and evidence of hu- not studio.
 Polymath [2012]                      conventional       man reasoning
                                      proof record.      and correction.
 Liquid Tensor Ex- None required by Lean, mathlib, Identified ex- Formal-
 periment mathlib the documented public dependen- perts controlled computational
 Community [2022] workflow.           cies, and proof translation,       near case.
                                      engineering.       formalization,
                                                         and release.




                                              31
 Danus matroid ex- Multi-agent gen- Stateless verifica- Reconstruction, Studio      candi-
 periment Liu et al. eration with fact- tion and stored challenge per- date; governance
 [2026]; Cheng et graph memory.         proof dependen- formance, and undetermined.
 al. [2026]; Cheng                      cies.            collective au-
 [2026]                                                  thorization are
                                                         unreported.
 Jacobian episode Generated coun- Computational The five gov- Boundary case;
 Weinreich [2026] terexample and checking            re- ernance condi- governance un-
                     AI-assisted diges- ported; public tions are not es- established.
                     tion as reported provenance         tablished by the
                     by Weinreich.      remains incom- cited record.
                                        plete in the
                                        source     used
                                        here.



S7     Hypothesis tournament
Competing possibilities remain live until a discriminating design is executed.

 ID     Hypothesis                   Discriminating prediction     Failure condition
 H1     Authorial units remain suf- Tooling changes efficiency Persistent cases lack
        ficient for most advanced but not the responsible unit. any bounded authorial
        mathematics.                                                warrant.
 H2     Governed studios form a dis- Stable role differentiation, Cases reduce to collab-
        tinct regime.                memory, and collective au- oration or tool use.
                                     thorization emerge.
 H3     Degenerate studios can cer- Correctness coexists with fail- Participants    retain
        tify output without retained ures of reconstruction, diag- comparable       under-
        understanding.               nosis, and transfer.           standing.
 H4     Governance         preserves Authority traces and stop Governance labels do
        agency under substantial rights predict better diagno- not predict behavior.
        automation.                  sis and responsibility.
 H5     Plural institutions are more Mixed regimes preserve diver- Mixed regimes increase
        robust than uniform adop- sity and correction capacity exclusion or fragility.
        tion or refusal.             under shocks.
 H6     MIAT-MD can be applied Independent coders and the Agreement collapses
        reliably across arXiv after automated pipeline retain ac- under domain shift or
        calibration.                 ceptable agreement across key variables cannot be
                                     fields and time.               recovered from papers.



S8     MIAT-MD gates G0–G6

                                             32
  Gate    Focus              Current evidence                               Result
  G0      Scope              Object, comparator, and prospective status Pass
                             are explicit.
  G1      Ontology           CIMA tuple, H ∗ , governed studio, degenerate Pass
                             studio, and the claim-relative governance rule
                             are defined.
  G2      Epistemology       Correctness, understanding, explanation, Pass
                             taste, authority, and responsibility remain
                             distinct.
  G3      Methodology        L0–L5, audit criteria, dual-axis ledger, and Pass with limi-
                             nonclaims are specified.                       tation
  G4      Evidence           Claim IDs link source, warrant, validation Pass
                             route, and uncertainty.
  G5      Robustness         H1–H6, RHM classes, comparative cases, and Pass with limi-
                             optional FCA variants are disclosed.           tation
  G6      Governance         Authority, stop rights, release, and with- Pass with limi-
                             drawal are specified.                          tation

The limitations at G3, G5, and G6 are substantive: the instruments have not been validated,
the benchmark has not been executed, and the governance protocol has not been piloted in a
live mathematical project.


S9       Prospective understanding audit
The unit of audit may be one person or a named group whose distributed competencies are
documented. Each dimension may be scored 0 (not demonstrated), 1 (partial or heavily
scaffolded), or 2 (independently demonstrated). Scores are descriptive. No pass threshold is
validated.

   ID     Dimension             Challenge
   UA1 Strategy                 State the problem, central strategy, and purpose of main
                                definitions without reproducing the artifact.
   UA2 Dependencies             Identify assumptions, imported results, formal dependen-
                                cies, and model-generated steps.
   UA3 Reconstruction           Reconstruct decisive transitions at field-appropriate gran-
                                ularity.
   UA4 Error diagnosis          Find or explain a planted error and trace its consequences.
   UA5 Transfer                 Apply the strategy to a nearby case or explain why trans-
                                fer fails.
   UA6 Significance             Explain novelty, limitations, and relation to prior work.



                                             33
   UA7 Authorization            Decide whether to release, revise, or withdraw, and accept
                                responsibility for the decision.


Recommended administration is delayed, transcript-restricted, and partly adversarial. The
audit record should identify which member satisfied each dimension, allowed tools, challenge
prompts, assessor, and unresolved disagreements. A participant may use AI while learning;
the test asks whether reconstructible competence and authority remain available when the
artifact is challenged.


S10      Contribution-authority trace
For contributor i, record Ci = (Pi , Ei ), where Pi is productive contribution and Ei is the
scope of epistemic authority. Productive importance does not automatically confer authority,
and authority does not erase infrastructural contribution.

  Role                   Typical P          Typical E          Responsibility boundary
  Conceptual lead        High               High               Problem, strategy, and sig-
                                                               nificance.
  Proof formalizer       High               Medium             Encoding and local correct-
                                                               ness.
  Library maintainer     High               Low                Infrastructure integrity and
                                                               releases.
  Model operator         Medium             Low                Accurate trace and disclo-
                                                               sure.
  Independent reviewer Medium               High               Acceptance recommenda-
                                                               tion and challenge.
  Expositor              Medium             Medium             Clarity and faithful recon-
                                                               struction.
  Generative model       Variable           None               No testimonial or moral re-
                                                               sponsibility.
  Authorizing human      Variable           High               Release, revision, stop, and
                                                               withdrawal.



S11      Optional FCA analyses
The disclosed binary context contains seven objects and eight attributes. Standard enu-
meration produced 13 formal concepts. The fuzzy view uses Jaccard similarity only as
a sensitivity-oriented representation. Its strongest pairs were collaborative/governed stu-
dio (0.75), formal-computational/governed studio (0.75), and degenerate studio/fact-graph
orchestration (0.75). These values reflect the hand-coded context.



                                             34
The stochastic view used 2,000 replicates, seed 25082026, and independent 0.05 cell-flip
probability. The strongest simple implications were understanding audit ⇒ human judgment
(0.797), understanding audit ⇒ public accountability (0.7905), understanding audit ⇒ human
stop right (0.788), and formal verification ⇒ repository memory (0.785). These numbers
estimate robustness to a specified coding perturbation. They are not probabilities that the
ontology or implications are true.


S12       Robustness and heterogeneity map
The RHM uses three statuses:

• ROBUST_CORE: survives the present source, boundary, and counterargument checks at its
  stated claim type.

• SPURIOUS_ENVELOPE: depends on role confusion, unsupported promotion, unstable coding,
  or a claim stronger than its evidence.

• LEGITIMATE_OPEN_UNCERTAINTY: remains meaningful and testable but is not resolved by
  current evidence.

Heterogeneity should be tracked across mathematical field, task type, career stage, formaliza-
tion maturity, model access, language, institutional resources, and time horizon. An aggregate
result should not be promoted when opposite effects across these strata are plausible.


S13       Prospective validation and extension program
The extension is staged so that scale does not precede validity. The machine-readable roadmap
is data/extension_roadmap.csv.

  Stage     Objective             Design and primary outputs              Stop rule
  I         Validate the under- A manually assessed pilot with inde- Do not com-
            standing and gover- pendent coders, delayed reconstruction, pare workflows
            nance instruments. planted-error diagnosis, transfer, and if       inter-rater
                                claim-relative GR1–GR5 coding.          reliability or con-
                                                                        struct validity is
                                                                        inadequate.
  II        Compare workflows Authorial, assistive (L1–L2), governed Freeze tasks, cri-
            prospectively.      studio (L3–L4), and degenerate studio teria, and instru-
                                (L4–L5) conditions across proof con- ments before out-
                                struction, formalization, counterexam- come inspection;
                                ple search, and exposition.             retain null or ad-
                                                                        verse results.


                                             35
 III        Pilot corpus classifi- A stratified gold set of 100–200 arXiv Do not scale
            cation.                papers, independently double-coded by if           human-
                                   field, year, contribution type, and de- human           and
                                   clared tool use.                          model-human
                                                                             agreement are
                                                                             below preregis-
                                                                             tered thresholds
                                                                             or show major
                                                                             domain drift.
 IV         Scale the arXiv A 500–1,000 paper pilot followed, if Do not interpret
            study.                 warranted, by a larger longitudinal cor- missing disclo-
                                   pus with uncertainty intervals and field- sures as absence
                                   specific error analysis.                  of AI use; do not
                                                                             pool strata with
                                                                             incompatible
                                                                             error profiles.

For Stage II, primary outcomes are delayed reconstruction, error diagnosis, transfer, cor-
rectness, originality, time, and calibration. Secondary outcomes include perceived agency,
dependence on proprietary infrastructure, reviewer burden, and distributional effects by
career stage. Tasks, assessors, and planted errors should be blinded where feasible. Model
versions and material prompts should be archived subject to licensing and privacy. The
calibration tasks must remain separate from the final evaluation set.
For Stages III and IV, the codebook must be frozen before large-scale classification. The
gold set should include positive, negative, ambiguous, and missing-disclosure cases. Domain-
specific confusion matrices, not one aggregate accuracy value, determine whether scaling is
defensible. Historical examples must not be recoded as prospective observations, and corpus
prevalence must not be interpreted as causal evidence about understanding or institutional
effects. This supplement specifies the program but reports no validation or benchmark result.


S14      Figures and alt text
Alt text. A human authority node H ∗ connects to technical systems, symbolic media,
repositories, validation, institutions, and public action. The coupled system branches to a
governed studio when humans can reconstruct and stop release, and to a degenerate studio
when oversight is ceremonial.

Alt text. Perturbations pass through governed conversion into public utility. A horizontal
agency constraint separates an antifragile candidate, where correction capacity improves, from
degenerative adaptation, where output improves while understanding or autonomy declines.




                                              36
Figure S1: CIMA proof-production ecobiont and the governance boundary.




                                 37
Figure S2: Conditional antifragility with an epistemic agency constraint.




                                   38
Figure S3: Optional FCA view of the production taxonomy.




                          39
Alt text. A simplified lattice-like arrangement distinguishes human-governed and auto-
mated coupling branches, with authorial/collaborative, governed-studio, and degenerate-
studio cases. A note states that the view is a representation and not evidence.

Alt text. A two-by-two matrix places authorial or collaborative practice at high agency
and lower automation, governed studios at high agency and high automation, delegated
routine at low agency and lower automation, and degenerate studios at low agency and high
automation.

Alt text. Claims move from stable IDs through layer classification, evidence contracts,
G0–G6 gates, and RHM status. A green branch allows promotion when warrant matches
claim type; a red branch blocks promotion from model output, figures, or FCA patterns
alone.

Alt text. Four stages move from instrument validation to workflow comparison, a manually
double-coded arXiv gold set, and conditional corpus scaling. Gates between stages stop
progression when reliability, construct validity, or domain-transfer criteria fail.


S15       Tool and computational resource disclosure for this
          release
Generative AI systems supported literature triage, argument mapping, language revision,
LaTeX editing, and code generation. The human author defined the research question and
framework, selected the claims advanced, and retains responsibility for the interpretations,
references, classifications, and final text. Because the manuscript is conceptual rather than a
reported mathematical proof, the L0–L5 proof-intervention scale does not map perfectly onto
its workflow. The closest description is editorial and analytic assistance at approximately
L1–L2, with material use disclosed here. No benchmark, participant study, or corpus analysis
was generated or represented as completed.


S16       Reproducibility manifest
The arXiv submission bundle for version 2.6.1 is intentionally minimal: this single LATEX source
and the six PDF figures it loads. A separate, versioned reproducibility archive is available
at https://drive.google.com/file/d/1IlBFXJd1z1-F6xjPO0ITQT3j-o_FvgBP/view.
That archive contains the compiled manuscript, its single-file source with this supplement
embedded, claim, case, decision, governance, and extension CSV ledgers, analysis scripts, the
figure-generation script, JSON/CSV outputs, figure files in PNG/SVG/PDF, a spreadsheet
mirror, an environment freeze, and SHA-256 checksums. Standard FCA, fuzzy similarity,
stochastic perturbation, and RHM outputs can be regenerated without network access. The
PDF build requires a standard LATEX installation.

                                              40
Figure S4: Automation intensity and human epistemic agency.




                            41
Figure S5: MIAT-MD claim-promotion pipeline.




                    42
Figure S6: Staged validation and extension sequence.




                        43
