                                                                   Autoformalizing Argumentative Material Inferences
                                                                              Xin Quan1,3 , Reto Gubelmann2 , André Freitas1,3∗
                                                                                            1
                                                                                          Idiap Research Institute, Switzerland
                                                                                           2
                                                                                             University of Zurich, Switzerland
                                                                            3
                                                                              Department of Computer Science, University of Manchester, UK
                                                                           xin.quan@idiap.ch, reto.gubelmann@uzh.ch, andre.freitas@idiap.ch



                                                                        Abstract                               involved and the commitments of the discourse, rather than
arXiv:2609.16991v1 [cs.CL] 15 Sep 2026




                                                                                                               by logical form alone (Brandom 1994, 2008, 2002; Hlobil
                                           Natural language arguments are compelling before they are           and Brandom 2024). Material inferences can be deductively
                                           formally explicit. A premise supports a claim through de-
                                                                                                               valid if the truth of the premise necessitates the truth of the
                                           feasible warrants, background commitments, and exception
                                           conditions that the text leaves implicit. However, formal verifi-   conclusion (as in “LA is south of San Francisco, therefore San
                                           cation requires the opposite. Making such arguments machine-        Francisco is north of LA”), or they can be inductively valid if
                                           checkable requires constructing the missing commitments,            the premise only makes the conclusion plausible, rational, or
                                           not only translating given sentences into logic. Construction,      likely (as in “the streets are wet, therefore, it has rained”). It
                                           however, carries a risk that translation does not: a system free    is widely accepted that, typically, material inferences can be
                                           to add premises can make any claim provable, and a formally         explicated into formally valid inferences (as in “LA is south
                                           valid proof may assert the claim outright, prove it without         of San Francisco, and whenever A is south of B, B is north of
                                           the original premise, or establish more than the claim itself.      A, therefore San Francisco is north of LA”). However, due to
                                           We address this problem by formulating autoformalization            the context-dependence of aspects of meaning of terms and
                                           for argumentative material inference as guard completion, in
                                                                                                               of the commitments of the discourse, philosophers have seen
                                           which non-monotonic material support is turned into mono-
                                           tonic formal inference relative to an explicitly constructed        this task of faithfully explicating implicit material inference
                                           guard set. A completion is accepted only when its proof both        into explicit formal inference as a formidable obstacle for AI
                                           passes the theorem prover and survives contrastive tests of         to overcome (Brandom 2008, Ch. 3).
                                           premise dependence and claim selectivity. We implement this            In AI and logic, the structure referred to by inductive mate-
                                           formulation in GUARD, a neuro-symbolic framework in which           rial inference is captured by defeasible and non-monotonic
                                           LLMs construct and formalize candidate guards, Isabelle/HOL
                                                                                                               reasoning: a conclusion may be warranted in the current
                                           verifies the resulting theories and returns step-level feedback
                                           for iterative refinement, and the system abstains when no           information state and later withdrawn when an exception,
                                           faithful completion can be reached. Our empirical results on        priority, or counterargument is introduced (Reiter 1980; Mc-
                                           Debatepedia and ARCT using different LLMs demonstrate that          Carthy 1980; Pollock 1987; Dung 1995). This implicit and
                                           GUARD yields significant improvements in verified-faithful          defeasible character runs through NLP inference settings.
                                           inference (+35.3, +32.9 points) and substantial reductions in       Natural language inference, commonsense reasoning, and
                                           leakage (−25.9, −21.9 points) over the state-of-the-art LLM-        argument mining package materially licensed support under
                                           driven theorem proving approach. Moreover, we show that             labels such as “entailment” or “argument support” (Bowman
                                           the symbolic soft critique and the explicit assumption layer        et al. 2015; Williams, Nangia, and Bowman 2018; Nie et al.
                                           account for most of these gains, with the soft critique also im-    2020; Storks, Gao, and Chai 2020; Gubelmann et al. 2023),
                                           proving the initial validity of the elicited context and reducing
                                                                                                               and argument reasoning benchmarks show that the decisive
                                           the number of iterations required for successful verification.
                                                                                                               step is often the reconstruction of an implicit warrant rather
                                                                                                               than the application of a stated rule (Habernal et al. 2018;
                                                                  Introduction                                 Gupta, Zuckerman, and O’Connor 2024).
                                         Arguments in natural language are rarely delivered as formal             Making this support formally explicit is the precondition
                                         derivations. In debate, explanation, and everyday reasoning,          for verification. A justification can be audited only when the
                                         a premise counts as a reason for a claim because readers can          commitments it relies on are stated, and plausible-sounding
                                         recover a warrant, rely on shared background commitments,             explanations are known to often fail validity or faithfulness
                                         and leave exception conditions unstated. Argumentation the-           (Kumar and Talukdar 2020; Valentino, Pratt-Hartmann, and
                                         ory has long treated such warrants as part of the layout of           Freitas 2021). A theorem prover enforces exactly this disci-
                                         reasons (Toulmin 1958; Lawrence and Reed 2020), while                 pline, since consequence is checked against an explicit theory
                                         inferentialist accounts describe this support as material in-         and every assumption, definition, and exception condition
                                         ference: inference licensed by the content of the concepts            a proof relies on must be written down (Nipkow, Wenzel,
                                                                                                               and Paulson 2002). Recent autoformalization work makes the
                                            ∗
                                                Corresponding author.                                          construction of such theories feasible, with LLMs translat-
ing informal statements into proof-oriented representations         age verified-faithful rate over the strongest baseline by 35.3
and revising them under formal feedback (Wu et al. 2022;            points on Debatepedia and 32.9 points on ARCT, while reduc-
Olausson et al. 2023; Lu, Delaware, and Zhang 2024; Zhang,          ing leakage by 25.9 and 21.9 points respectively. Removing
Quan, and Freitas 2024), and a closer line of work couples          the soft symbolic critique or the assumption layer lowers
LLMs with theorem provers to verify and iteratively refine          the verified-faithful rate by up to 40.5 and 31.5 points, and
natural-language explanations for NLI (Quan et al. 2024a,b,         an extended-budget probe shows that most abstentions are
2025b,a).                                                           missing guards rather than incompatible arguments.
   However, autoformalizing argumentative material infer-              To summarize, this paper makes three contributions. First,
ence raises challenges that do not arise when the supporting        we introduce GUARD, an LLM+Isabelle/HOL framework
content is already given. First, unlike explanation verification,   that formulates material-inference autoformalization as guard
where the sentences to formalize are provided in advance            completion, constructing explicit background context, select-
(Quan et al. 2024b), the commitments that make the premise          ing proof-relevant guards, and checking contrastive faith-
sufficient must first be constructed, together with the exception   fulness. Second, we evaluate GUARD on Debatepedia and
conditions under which they fail. Second, once the system is        ARCT across four backbone LLMs, showing average gains of
free to add premises, formal validity alone becomes uninfor-        35.3 and 32.9 points in verified-faithful rate over the strongest
mative. A proof can become valid because an added guard             baseline and reductions of 25.9 and 21.9 points in leakage.
states the answer, weakens the target, or makes the original        Third, our diagnostic analysis of the explicitation process
premise irrelevant. Third, solver feedback cannot distinguish       attributes drops of up to 40.5 and 31.5 verified-faithful points
a faithful explicitation of the original support from an easier     to the soft symbolic critique and the assumption layer, con-
substitute proof, so verification must be paired with explicit      fines residual leakage to premise-side failures, and traces 63.5
checks on premise dependence and claim selectivity.                 to 74.3 percent of the abstained instances to missing guards
   In this paper, we frame autoformalization for material           rather than incompatible arguments.
inference as a guard-completion problem. We propose a
neuro-symbolic framework GUARD that integrates LLMs                                    Problem Definition
with the Isabelle/HOL theorem prover (Nipkow, Wenzel, and           In this paper, we define an argument as a premise-claim pair
Paulson 2002) to investigate the following research questions:      (T, C) in which the premise T provides a materially licensed
RQ1: Can autoformalization close the explicitness gap for           reason for the claim C. Our goal is to construct an explicit
non-monotonic argumentative support without distorting the          strengthened context Γ↑ and to identify a set of guards G ⊆ Γ↑
original material relation? RQ2: Can autoformalization-             that turns this material support into formal support, such that
based feedback refine hidden warrants into explicit guard           G ∪ {T } |= C holds.
assumptions? RQ3: How robust and faithful is guard com-                We leverage an LLM-based soft verifier and an external
pletion across backbone LLMs?                                       theorem prover to systematically verify these entailments
   To answer these questions, GUARD first constructs a              through an automated process. Specifically, given the set
strengthened context organized around the sources of implic-        of input sentences S = {T, C} ∪ G, we aim to construct
itness that classical argument reconstruction identifies: en-       a set of logical forms ϕ = {Φ(s) | s ∈ S}, where Φ is
thymematic assumptions, definitions and term normalizations,        the autoformalization process that converts natural language
and the exception conditions under which a defeasible warrant       sentences into symbolic representations. We denote the logical
is blocked (Naess 1949; Pollock 1987; Gordon, Prakken, and          forms of the premise and claim by T ∗ = Φ(T ) and C ∗ =
Walton 2007). The elicited defeasible rules are integrated          Φ(C), respectively, and write g ∗ = Φ(g) for each guard
into guarded form with explicit abnormality conditions in           g ∈ G. From these logical forms, we construct a theory
the style of circumscription (McCarthy 1986), which is how          Θ = (A, τ ), where A = {g ∗ | g ∈ G} is the set of axioms
non-monotonic support is turned into monotonic inference            derived from formalizing the guards, and τ is the theorem to
relative to explicit guards. An LLM-based soft verifier then        be proven, with T ∗ as its assumption and C ∗ as its proof goal.
screens each candidate against four proof obligations. In turn,     Proving τ thus establishes A ∪ {T ∗ } ⊢ C ∗ . If the theorem
Isabelle/HOL is adopted as the hard verifier, and its failed        prover derives a valid proof of τ under A, we conclude that
proof steps are extracted as feedback for targeted refinement,      G formally licenses the inference from T to C under Γ↑ .
extending the soft and hard critique design used in explanation        Otherwise, a refinement controller uses the failed proof
refinement (Quan et al. 2025b). Finally, a contrastive faithful-    steps as feedback and iteratively refines the guard set, updating
ness stage replaces the premise with alternatives that should       the state
not support the claim, and the claim with alternatives that the                        sk = ⟨Γ↑k , Gk , T ∗ , C ∗ ⟩,
premise does not warrant, and accepts a valid inference only        generating a refined guard set Gk+1 , until a valid proof is
if every perturbed theory becomes unprovable.                       found or a predefined refinement budget is exhausted.
   Our empirical evaluation on the Debatepedia argument
corpus (Cabrio and Villata 2013) and the Argument Rea-                                     Methodology
soning Comprehension Task (ARCT) (Habernal et al. 2018),
conducted with GPT-5.1, Qwen3-Max, DeepSeek-V3.2, and               Stage I: Context Strengthening
Mistral Medium 3.5 as backbone LLMs, shows that materi-             Stage I is grounded in classical argument reconstruction:
ally supported arguments consistently lack formal validity          everyday arguments are materially valid in virtue of implicit
in their original form, and that GUARD improves the aver-           background commitments and become formally assessable
                                                                                                                                          Extract Failed Proof Step as feedback
                                                                                                                                                                                                                 Stage III Hard Verification and Refinement

                                                                                                                                                                                                   proof -
                                                                                                                                                                                                    (* From the premise, extract the positive effect on a developing mind. *)
                                                Stage I Context Strengthening                                                   Stage II Soft Verification and Refinement
                                                                                                                                                                                                    from asm have eff: "Effect z ∧ Positive z ∧ Mind y ∧ Developing y ∧ On z y" by auto
                                                                                                                                                                                                    (* Use Guard G1 to obtain that this effect is a cognitive benefit for that mind. *)
                                                                                                                                                                                                    from guard_G1 eff have ben: "Benefit z ∧ Cognitive z ∧ For z y" by blast
                                                                                                                                            (a) Autoformalisation
                                      Assumptions:                                                                                                                                                  (* From the premise, also keep the event structure and video-game play facts. *)
                                      A1: Developing minds are the minds of young people.                                                                                                           from asm have play: "VideoGamePlay x ∧ Have e ∧ Agent e x ∧ Patient e z" by blast
      Premise T                                                                                                                             (b) Guard selection:
                                      Definitions:                                                                                                                                                  (* Combine to see that playing video games has a cognitive benefit for (the mind of) y. *)
   Moderate video-game                D1: Moderate video-game play is a level of engagement with video
                                                                                                                                             <A1, D1, X1>
                                                                                                                                                                                                    from play ben have play_ben: "VideoGamePlay x ∧ Benefit z ∧ Cognitive z ∧ Have e ∧ Agent e x ∧
   play may have positive             games in terms of frequency and duration that is neither minimal                                                                                             Patient e z ∧ For z y" by simp
   effects on developing              nor excessive and does not typically interfere with healthy
                                                                                                                                            (c) Critique:
                                                                                                                                                                                                    (* Use Guard G4 to obtain a young person u of whom y is the mind. *)
   minds.                             functioning.                                                                                                                                                  from asm have dev_mind: "Mind y ∧ Developing y" by blast
                                      Exceptions:                                                                                                             PO1-PO4                               from guard_G4 dev_mind obtain u where yu: "YoungPerson u ∧ Of y u" by blast
      Claim C                         Defeasible rule:                                                                                                                                   Soft
                                                                                                                                                                                                    (* Strengthen the playing-benefit fact with this young person. *)
   Video games can have               X1: Moderate video-game play among young people typically                                                  PO1: Rep         PO2: Support          Verified
                                                                                                                                                                                                    from play_ben yu have play_ben_young: "VideoGamePlay x ∧ Benefit z ∧ Cognitive z ∧ Have e ∧
   cognitive benefits for             involves active and repeated cognitive engagement.                                                                                                Guards
                                                                                                                                                                                                   Agent e x ∧ Patient e z ∧ YoungPerson u ∧ For z u" sledgehammer
   young people.                                                                                                                                PO3: Entail       PO4: Depend                       (* Apply Guard G7 to move from video-game play to video games themselves. *)
                                      Abnormality condition:                                                                                                                                        from guard_G7 play_ben_young obtain x1 e1 where vg: "VideoGame x1 ∧ Have e1 ∧ Agent e1 x1
  (material support)                  X1: The level of video-game use is wrongly classified as moderate                                                                                            ∧ Patient e1 z ∧ For z u" <ATP>
                                      when it is actually minimal or excessive.                                                                                                                     (* Package everything to match the existential hypothesis. *)
                                                                                                                                                  Extract          PO1-PO4                          from vg yu have "∃x y z e. VideoGame x ∧ Benefit z ∧ Cognitive z ∧ YoungPerson y ∧ Have e ∧
                                                                                                                                                                                                   Agent e x ∧ Patient e z ∧ For z y" <ATP>
                                                       Update guards                                                                             diagnosis           Fail
                                                                                                                                                                                                    then show ?thesis <ATP>
                                                                                                                                                                                                   qed

                                                                                                                                                                                                                                                      Hard
                                                                                                                                                                                                                                                     Verified                Replace Premise
                                                                                                                                                                                 If the theorem is still                                                                     or Hypothesis in
    Assumptions:                                                                                                                                                                                                                                     Guards
    A1: Positive effects on developing minds are cognitive benefits for those minds.                                                                                                    provable                                                                                the Theory
    A2: Developing minds are the minds of young people.
    A3: Moderate video-game play with positive effects on developing minds is an activity for young people that has a real possibility of producing                     Verified-Faithful
    those effects.                                                                                                                                                                                           A1: Premise Contrast
    A4: The positive cognitive effects of moderate video-game play are not rare, small, or fragile.
    A5: If playing video games has a cognitive benefit for young people, then video games have that cognitive benefit for young people.                                                                      Excessive video-game play is linked to attention problems and
    A6: A cognitive benefit for a young person's mind is a cognitive benefit for that young person.                                                                      Reject-Leaky                        poorer academic performance in developing minds.
    Definitions:
    D1: Young people are children and adolescents who have not yet reached full adulthood.
    Exceptions:
    Defeasible rule:                                                                                                                                                                                         A2: Claim Contrast
    X1: When an activity for young people has a real possibility of producing positive cognitive effects, it is usually acceptable to say that the activity
                                                                                                                                                                         Abstain-MG
    can have cognitive benefits for young people.                                                                                                                                                            Excessive video-game play can have cognitive benefits for young
                                                                                                                                                                                                             people.
    Abnormality condition:
    X1: The positive cognitive effects are so rare, small, or fragile that ordinary speakers would not describe the activity as one that can have                         Abstain-NC
    cognitive benefits.
                                                                                                                                                                                                                                   Stage IV Faithfulness Check



Figure 1: Overview of GUARD. Starting from a premise-claim pair (T, C), the framework constructs a strengthened context,
autoformalizes the selected candidate guards and iteratively combines soft verification, hard theorem proving and contrastive
faithfulness checks until one of the four final statuses is reached.


once these commitments are made explicit (Sellars 1953;                                                                                                                   Following Quan et al. (2024b), the function maps each nat-
Brandom 1994). Starting from the input pair (T, C), we con-                                                                                                               ural language sentence s to a logical form Φ(s) using Neo-
struct an explicit strengthened context Γ↑ = A ∪ ∆ ∪ X,                                                                                                                   Davidsonian event semantics (Parsons 1990) coupled with
intended as a task-specific explicit witness to the otherwise                                                                                                             first-order logic. The resulting logical forms are then aligned
implicit discourse context, with each component elicited by a                                                                                                             with the Isabelle/HOL style. For example, the sentence “Child
dedicated harvester under shared contextual parameters (e.g.,                                                                                                             beauty pageants can teach children to base self-worth on phys-
domain, jurisdiction, and timebound). A contains assump-                                                                                                                  ical appearance” can be formalized as follows:
tions in the sense of enthymeme completion (Eemeren and
Grootendorst 2003), including normalcy conditions, domain                                                                                                                  ∀x y e1 . ChildBeautyPageant(x) ∧ Child (y) ∧ Teach(e1 )
restrictions, and ceteris-paribus clauses. Each assumption is                                                                                                                        ∧ Agent(e1 , x) ∧ Patient(e1 , y) −→
typed and linked to the premise-claim edge it supports. ∆ con-                                                                                                            ∃z w e2 . SelfWorth(z) ∧ PhysicalAppearance(w)∧
tains definitions and term-normalization facts in the spirit of                                                                                                           Base(e2 ) ∧ Agent(e2 , y) ∧ Patient(e2 , z) ∧ On(z, w).
making it more precise (Naess 1949; Walton 2001), retrieved
from authoritative sources and normalized into canonical                                                                                                                  Here, the verb teach is represented as the event e1 , with the
single-sentence forms for formalization. X contains exception                                                                                                             pageant as its agent and the child as its patient, while the
management, following defeasible reasoning (Toulmin 1958;                                                                                                                 taught behavior of basing self-worth on physical appearance
Pollock 1987; Gordon, Prakken, and Walton 2007). Based                                                                                                                    is captured by a second event e2 . This predicate-argument
on the elicited assumptions and definitions, we organize the                                                                                                              structure keeps the logical form close to the surface form
latter as local defeasible rules over intermediate concepts and                                                                                                           of the sentence and preserves its information content during
pair each rule with the exception conditions under which it is                                                                                                            translation. Each assumption and definition in Γ↑ is then
blocked. Stage I therefore builds the strengthened background                                                                                                             converted into an axiom. The exception structures elicited in
from which a step-specific guard set G ⊆ Γ↑ will later be                                                                                                                 Stage I are then integrated into guarded defeasible rules, where
selected. The details for each harvester are described in the                                                                                                             each rule family d is guarded by an abnormality predicate in
Appendix D.                                                                                                                                                               the style of circumscription
                                                                                                                                                                                                        (McCarthy 1986): ∀k. φd (k) ∧
                                                                                                                                                                          ¬Ab d (k) → ψd (k) , Ab d (k) ↔ χd,1 (k) ∨ · · · ∨ χd,n (k), in
Stage II: Soft Verification and Refinement                                                                                                                                which φd and ψd denote the body and head of the rule and
Autoformalization. Stage II begins by applying the auto-                                                                                                                  each χd,i describes an exception condition. The biconditional
formalization function Φ to the context Γ↑ elicited in Stage I.                                                                                                           is replaced with a one-directional implication if the exception
list is open-ended. The details are described in the Appendix         is then updated when needed, and the resulting theory is
B and Appendix D.                                                     checked by the theorem prover in the next iteration.
Guard selection. We define an LLM-based critic func-
tion fguard to identify the contextual support needed for             Stage IV: Faithfulness Check
the inference from T ∗ to C ∗ . The function uses the for-           A formally verified proof is still not sufficient. Over-broad
malised logical forms of Γ↑ to select a step-specific guard set      guards may prove the claim without using the premise, or they
G = fguard (Γ↑ , T ∗ , C ∗ ) ⊆ Γ↑ , with formal representation       may establish more than the claim itself. Stage IV therefore
G = { g ∗ | g ∈ G }. Selection aims to make the guards jointly       applies two contrastive tests to each verified candidate.
sufficient to infer C ∗ from T ∗ and the resulting candidate is
then assessed against PO1 to PO4.                                    A1: Premise contrast. A1 keeps the claim and replaces
                                                                     the premise with alternatives that should not support it. The
Soft verification: PO1-PO4. The framework then performs              challenge set T ′ contains the empty-premise case T ′ = ∅ and
a soft critique of ⟨G, T ∗ , C ∗ ⟩ over four proof obligations:      a same-topic counter-premis is proposed by our framework.
PO1 (Representation correctness) The formal representa-              For example, given the premise “GM crops are disease-
   tion is syntactically well-formed, the types, arities, variable   resistant and therefore increase yield” and the claim “GM
   bindings, and semantic roles are coherent, and predicate          food is beneficial,” a generated counter-premise is “GM
   normalization is consistent across the premise, the claim,        agriculture pushes small traditional farming communities
   and the guards.                                                   out of business.” A1 therefore measures premise sensitivity:
PO2 (Support adequacy) Each guard in G is traceable to               whether the proof genuinely depends on the original premise.
   an item in Γ↑ . The guards jointly cover the missing infer-
   ential material between T ∗ and C ∗ and make the relevant          A2: Claim contrast. A2 keeps the premise and replaces
   exception conditions explicit where needed.                        the claim with a nearby alternative that the premise does not
PO3 (Strict support) The guards make the premise formally             warrant, collected in a challenge set C ′ . The alternative is
   support the claim: G ∪ {T ∗ } ⊢ C ∗ .                              proposed by the framework as a cross-subtopic claim, i.e., a
PO4 (Dependence) The proof genuinely depends on both                  claim on the same topic whose content the premise does not
   the premise and every guard: (a) G ⊬ C ∗ ; (b) (G \ {g}) ∪         address. For the same example, the generated alternative is
   {T ∗ } ⊬ C ∗ for all g ∈ G.                                       “GM food is safe for consumers,” since the premise concerns
                                                                      yield rather than consumer safety. A2 therefore measures claim
Soft refinement. We define an LLM-based soft refinement               selectivity: whether the proof establishes only the intended
             soft
function frefine  that applies targeted updates to the current        claim. We autoformalize each probe and substitute it into the
candidate based on the soft critique feedback. For PO1 failures,      verified theory. The candidate passes the faithfulness check
the function corrects the affected formal representations. A          only if none of the substituted theories remains provable:
failure of PO2 requires expanding or refining Γ↑ by adding            ∀T ′ ∈ T ′ . G ∪ {T ′∗ } ⊬ C ∗ , ∀C ′ ∈ C ′ . G ∪ {T ∗ } ⊬ C ′∗ .
missing contextual items or correcting existing ones. The
affected items are then formalised and G is reselected. When         Faithfulness refinement. We define an LLM-based faith-
PO3 fails, refinement updates the strengthened context and the                                       faith
                                                                     fulness refinement function frefine   to address leakage detected
formalised guard candidates to establish formal support from         by the contrastive tests. If a substituted theory remains prov-
T ∗ to C ∗ . PO4 failures are addressed by removing padded           able, the function takes the leaking theory and a leak report
guards or refining the strengthened context, with the aim of         as input and produces a complete updated guard set. A guard
making the proof depend on the premise and on each selected          whose consequent asserts the claim unconditionally is made
guard. The updated candidate is reassessed against PO1 to            conditional on the content supplied by the premise. The func-
PO4, with a maximum of 10 soft refinement iterations.                tion also narrows over-broad guards to exactly what the claim
                                                                     requires. The original entailment must remain provable under
Stage III: Hard Verification and Refinement                          the updated guards. We set a maximum of 5 iterations for
Hard verification. Following Quan et al. (2024b), we con-            faithfulness refinement.
struct an Isabelle/HOL theory (Nipkow, Wenzel, and Paulson
2002) to formally verify the selected guards. Each formal            Outputs. The pipeline returns one of four verdicts. A can-
guard g ∗ ∈ G is converted into an axiom, while the premise          didate is labelled Verified-Faithful when hard verification
and the claim are converted into the theorem to be proven,           succeeds and both contrastive tests pass, and Reject-Leaky
where T ∗ constitutes the assumption clause and C ∗ the proof        when the entailment is formally verified but A1 or A2 still
goal. A successful proof therefore establishes G∪{T ∗ } ⊢ C ∗ .      fails after refinement. If no verified candidate is obtained
An example of the constructed theory is shown in Figure 1.           within the refinement budget, we distinguish two outcomes.
                                                                     Abstain-Missing-Guards indicates that admissible repairs,
Hard refinement. If the theorem prover fails to prove                such as unresolved assumptions, definitions, exception con-
a proof step, we extract the failed step together with the           ditions, or alternative guard choices, are still open when the
applied axioms as external feedback for an LLM-based hard            budget is exhausted. Abstain-Not-Compatible indicates that
                         hard
refinement function frefine   . Depending on the diagnosis, it       no admissible repair remains, as the remaining options would
corrects the affected formal representations or refines the          require altering the claim itself or would yield only leaky or
logical error in the strengthened context Γ↑ . Guard selection       irrelevant proofs.
                                                              Debatepedia                                        ARCT

                 Backbone             Method   SP ↑   VFR ↑   Leak ↓   A1 ↓    A2 ↓    #Iter   SP ↑    VFR ↑   Leak ↓   A1 ↓    A2 ↓    #Iter

                                      Direct   0.00    0.00     –         –      –       –      0.00    0.00     –         –      –       –
                                      CoT     14.17   11.74   17.14    11.43   5.71     –      16.00   12.50   21.88    15.63   9.38      –
                 DeepSeek-V3.2        Toulmin 10.93    8.10   25.93    18.52   14.81     –     17.00   14.00   17.65    14.71   2.94      –
                                      PEIRCE 28.34    19.03   32.86    30.00   4.29    5.86    31.00   23.00   25.81    24.19   6.45    4.15
                                      GUARD 51.82     48.58   6.25      6.25   0.78    3.72    55.50   53.50    3.60     3.60   0.00    3.82

                                      Direct   0.00    0.00     –         –     –        –      0.00    0.00     –         –      –       –
                                      CoT     12.96    8.10   37.50    25.00 18.75       –     18.00   13.00   27.78    22.22   11.11     –
                 Qwen3-Max            Toulmin 14.98   10.53   29.73    27.03 8.11        –     17.00   13.50   20.59    17.65   5.88      –
                                      PEIRCE 34.82    24.29   30.23    26.74 8.14      5.94    42.00   30.00   28.57    25.00   3.57    3.27
                                      GUARD 59.92     56.68   5.41      5.41  0.00     3.85    63.00   61.00   3.17      3.17   0.00    3.21

                                      Direct   0.00    0.00     –         –     –        –      0.00    0.00     –         –      –       –
                                      CoT     14.98   10.53   29.73    21.62 10.81       –     19.50   12.00   38.46    25.64   15.38     –
                 Mistral Medium 3.5   Toulmin 18.22   13.77   24.44    17.78 11.11      –      16.00   12.50   21.88    18.75   6.25      –
                                      PEIRCE 38.06    26.32   30.85    27.66 6.38      5.83    46.00   36.50   20.65    20.65   5.43    5.62
                                      GUARD 64.37     62.75   2.52      2.52  0.00     3.74    66.00   64.50    2.27     2.27   0.76    3.25

                                      Direct   0.00    0.00     –         –     –        –      0.00    0.00     –         –      –       –
                                      CoT     24.29   19.43   20.00    13.33 10.00      –      25.50   18.00   29.41    19.61   15.69     –
                 GPT-5.1              Toulmin 24.70   20.24   18.03    18.03 0.00       –      21.00   17.50   16.67    11.90   4.76      –
                                      PEIRCE 45.34    33.60   25.89    17.86 9.82      5.21    51.00   39.00   23.53    19.61   5.88    4.07
                                      GUARD 78.14     76.52   2.07      2.07  0.00     3.78    82.50   81.00   1.82      1.82   0.00    3.13


Table 1: Main comparison across four backbone LLMs on Debatepedia and ARCT. ‘SP’ denotes the solver-pass rate. ‘VFR’
denotes verified-faithful rate, the number of instances whose proof additionally passes the contrastive faithfulness checks. ‘Leak’
represents the solver-passed cases rejected by the faithfulness checks. ‘A1’ and ‘A2’ shows the number of solver-passed cases that
fail the premise-contrast and the claim-contrast test, respectively. ‘#Iter’ indicates the average iteration required to refine the
proposed context information to be successfully verified by the theorem prover. The best result per backbone and column is in
bold and the second best is underlined.


                  Experimental Setup                                            sentences that makes the implicit reasoning from the premise
                                                                                to the hypothesis explicit, and then formalise the generated
Datasets and Models. We select two argumentation                                background contextual information. (3) Toulmin-style 1-shot
datasets for evaluation: a topic-balanced derivative of the ex-                 explication: follow Gupta, Zuckerman, and O’Connor (2024)
tended Debatepedia corpus (Cabrio and Villata 2013) and the                     and prompt the LLM to explicate the implicit argument
Argument Reasoning Comprehension Task (ARCT) (Haber-                            in Toulmin terms (i.e., a qualified warrant, its backing, an
nal et al. 2018). The extended Debatepedia resource contains                    additional bridging sentence when needed, and a rebuttal
argument pairs drawn from 19 online-debate topics. We con-                      condition). The generated Toulmin context is then used as
struct a balanced evaluation set of 247 premise-claim pairs,                    the added bridging text for downstream formalisation and
with exactly 13 pairs per topic. ARCT contains reason-claim                     verification. (4) PEIRCE: use the neuro-symbolic refine-
pairs in which the reason supports the claim only through an                    ment framework of Quan et al. (2025a), which supplements
implicit warrant. We randomly sampled 200 instances from                        premise-side explanatory sentences in response to logical ver-
ARCT and treat each reason-claim pair as a premise-claim pair.                  ification results so that the premise can prove the hypothesis.
The dataset selection details are provided in Appendix A.1.                     In our comparison setting, these explanatory sentences are
   We conducted experiments with four backbone LLMs                             treated as added context. We set the maximum number of
within the proposed framework: GPT-5.1 (OpenAI 2025),                           iterations for theorem-prover-based verification and refine-
Qwen3-Max (Qwen Team 2025), DeepSeek-V3.2 (Deepseek-                            ment to 10 for both PEIRCE and our approach. The baseline
AI 2025), and Mistral Medium 3.5 (Mistral AI 2026). We                          selection rationale and comparison details are described in
employed Isabelle/HOL (Nipkow, Wenzel, and Paulson 2002)                        Appendix A.3.
as the logical solver. Backbone selection and LLM implemen-
tation settings are detailed in Appendix A.2.
                                                                                                       Results and Evaluation
Baselines. We compare against four baselines. (1) Direct                        Table 1 reports the main comparison. For CoT and Toulmin,
autoformalisation: map (T, C) directly into (T ∗ , C ∗ ) and                    the backbone LLM first generates the bridging context, which
use the solver to find a proof without adding explicit context.                 is then autoformalised into logical forms and formalised as an
(2) 1-shot CoT: use chain-of-thought prompting (Wei et al.                      Isabelle/HOL theory. Direct, CoT, and Toulmin are verified
2022; Wang et al. 2023) with one in-context example to                          in a single pass over the generated context, whereas PEIRCE
generate an ordered chain of two to four free-text background                   and GUARD refine their candidates iteratively with prover
                      Debatepedia                  ARCT                                                 ARCT: Initial vs. Final                                    Debatepedia: Initial vs. Final
                                                                                                          Solver-Pass Rate                                              Solver-Pass Rate
        Method    Empty ↓   Ctr.-only ↓   Empty ↓    Ctr.-only ↓                                    (averaged over backbone LLMs)                                     (averaged over backbone LLMs)
                                                                                           100                                                               100
                                                                                                    Initial                                                           Initial
                                                                                                                           +30.8




                                                                    Solver-Pass Rate (%)




                                                                                                                                      Solver-Pass Rate (%)
        CoT        15.36       2.48        19.99          0.78                              80      Final                                                     80      Final                  +28.5
                                                                                                                               66.8                                                              63.6
        Toulmin    18.18       2.16        14.28          1.47                              60      +16.4                                                     60
                                                                                                                                                                      +11.6
        PEIRCE     25.03       0.53        22.36          0.00                                          42.5
                                                                                            40                          36.0                                  40          36.6            35.0
        GUARD      4.06        0.00        2.72           0.00                                   26.1                                                              25.0
                                                                                            20                                                                20

                                                                                             0                                                                 0
Table 2: Decomposition of the A1 failures in Table 1 by probe,                                    PEIRCE                 GUARD                                      PEIRCE                 GUARD
averaged over the four backbone LLMs. ‘Empty’ denotes
candidates whose guards prove the claim with no premise at
all, and ‘Ctr.-only’ candidates that fail only once the counter-   Figure 2: Initial and final solver-pass rates of PEIRCE and
premise is substituted.                                            GUARD on Debatepedia and ARCT, averaged over the four
                                                                   backbone LLMs.

feedback. All methods share the same autoformalization
process, whose faithfulness is evaluated in the Appendix B.4.      or fire on an opposing one, they simply make the premise
Every solver-passed case, regardless of method, is submitted       unnecessary. GUARD runs the same LLM-prover loop but
to the contrastive faithfulness checks introduced above, from      blocks this path by construction, through the dependence obli-
which the Leak, A1, and A2 columns are derived.                    gation PO4 during soft verification and the empty-premise
   Materially supported arguments lack formal validity             probe afterwards, and its leakage falls to 4.06% and 2.72%.
and GUARD consistently converts them into formally                    The integration of LLM-based verification and refine-
verified inferences. Direct autoformalization fails on every       ment substantially improves the formal validity of the
instance: under all four backbones, a solver-pass rate of 0.00     elicited context. Figure 2 compares the initial and final solver-
stands on both datasets. The support rests on commitments the      pass rates of PEIRCE and GUARD, where the initial rate
text never states, and translation alone cannot recover them.      counts the instances whose first submitted theory is already
Single-pass explication helps little. CoT and Toulmin generate     proved. Stage II subjects the elicited context to a formal check
bridging sentences that spell out the hidden warrant, and the      before the prover ever sees it: the framework critiques the
resulting arguments read as complete, yet once formalized          candidate guards at the level of their logical forms against the
they reach only 10.93 to 25.50 SP and end with verified-           four proof obligations, and repairs malformed representations,
faithful rates between 8.10 and 20.24. With failed proof steps     missing support, and padded guards at the same symbolic
fed back to refinement function, PEIRCE roughly doubles the        level. The effect is visible at the first prover call. Although
single-pass SP under every backbone, to between 28.34 and          both methods start from the same premise-claim pairs, 35.0%
51.00: validity accumulates through revision against solver        of GUARD’s first theories are already valid on Debatepedia
feedback rather than arriving in one shot. GUARD keeps             and 36.0% on ARCT, against 25.0% and 26.1% for PEIRCE,
the same iterative loop but directs it at explicitly constructed   which submits its elicited sentences to the solver directly;
guards, and the combination performs best throughout. It           on Debatepedia, GUARD’s first submission already comes
obtains the highest SP and verified-faithful rate (VFR) for        within 1.6 points of the rate PEIRCE reaches after its full
every backbone on both datasets, with an average VFR of            refinement budget. The same symbolic-level refinement also
61.13 on Debatepedia and 65.00 on ARCT, 35.3 and 32.9              makes the subsequent hard loop more productive: because
points above PEIRCE, and it converges within 3.13 to 3.85          the theories that reach Isabelle/HOL are structurally sound, a
hard iterations on average.                                        failed proof step localizes a genuine logical gap whose diag-
   LLM-driven refinement improves provability by in-               nosis maps onto an obligation-specific repair, and GUARD
tegrating additional context but can make the origi-               gains 28.6 points on Debatepedia and 30.8 points on ARCT
nal premise unnecessary. GUARD reduces this leakage                from hard refinement, against 11.6 and 16.4 for PEIRCE, in
through explicit checks on premise dependence. Averaged            fewer hard iterations.
over the four backbones, PEIRCE reaches a solver-pass rate            Soft refinement constructs the strengthened context,
of 36.64% on Debatepedia and 42.50% on ARCT, more than             while hard refinement repairs it. Figure 3 tracks the average
doubling the prompting baselines, yet its leakage exceeds          number of assumptions, definitions, and exception conditions
Toulmin’s on both datasets (29.96% against 24.53%, and             per instance across refinement iterations. During soft refine-
24.64% against 19.20%). Refining toward provability there-         ment, assumptions and definitions grow steeply in the first
fore inflates validity faster than faithfulness: when the solver   five iterations, from an average of 3.6 to 9.0 and from an
only rewards a closed proof, the easiest repair is to strengthen   average of 5.8 to 8.5 on Debatepedia, which accounts for
the added context until it carries the proof on its own. Table 2   roughly 85% of their total soft-phase growth: the framework
exposes the mechanism. PEIRCE’s leaked candidates fail             is still proposing new items. After the fifth iteration both
almost exclusively under the empty premise (25.03% and             curves flatten while refinement continues, indicating that later
22.36%, with counter-only rates of 0.53% and 0.00%): the           soft rounds revise existing items rather than add new ones.
failure mode is bypassing the premise, not contradicting it, as    Exceptions grow more slowly and almost linearly throughout
the refined sentences never turn against the original premise      (2.9 to 4.8 and 2.5 to 4.1), consistent with rebuttal conditions
                                               ARCT: Growth of                                                                       Debatepedia: Growth of                                                               ARCT: Abstention Split                                         Debatepedia: Abstention Split
                                             Strengthened Context                                                                     Strengthened Context                                                                  of Failed Instances                                               of Failed Instances
                                                                                                                                                                                                          60                                                                   60
                                         (averaged over backbone LLMs)                                                               (averaged over backbone LLMs)
                                                                                                                                                                                                                                     Abstain-Missing-Guards                                            Abstain-Missing-Guards
                         14           Assumption          Definition       Exception                                 14           Assumption          Definition       Exception                          50                                                                   50     48.2
                                                                                                                                                                                                                 44.5                Abstain-Not-Compatible                                            Abstain-Not-Compatible
                                                                                                                                                                                                                                                                                                40.1
 Avg. # Elicited Items




                                                                                             Avg. # Elicited Items
                         12             Soft (Stage II)          Hard (Stage III)                                    12             Soft (Stage II)          Hard (Stage III)




                                                                                                                                                                                         % of Instances




                                                                                                                                                                                                                                                              % of Instances
                                                                                                                                                                                                          40                  37.0                                             40     16.6                 35.6
                         10                                                                                          10                                                                                          14.0                    34.0
                                                                                                                                                                                                                                                                                                14.6
                                                                                                                                                                                                          30                  13.5       10.0                                  30                          11.3
                          8                                                                                           8
                                                                                                                                                                                                                                                                                                                       21.9
                          6                                                                                           6                                                                                   20                                         17.5                      20                                      6.5
                                                                                                                                                                                                                 30.5                                 4.5                             31.6
                          4                                                                                           4                                                                                                       23.5       24.0                                                   25.5       24.3
                                                                                                                                                                                                          10                                                                   10                                      15.4
                                                                                                                                                                                                                                                     13.0
                          2                                                                                           2
                                                                                                                                                                                                          0                                                                    0
                          0                                                                                           0                                                                                        DeepSeek      Qwen3    Mistral      GPT-5.1                          DeepSeek   Qwen3    Mistral      GPT-5.1
                              0   1      2     3   4       5    6      7    8   9      10                                 0   1      2    3    4       5    6      7    8   9      10                            V3.2         Max    Medium 3.5                                       V3.2      Max    Medium 3.5
                                              Refinement Iteration                                                                       Refinement Iteration




                                                                                                                                                                                        Figure 4: Decomposition of outcomes on abstain-missing-
Figure 3: Average number of assumptions, definitions, and
                                                                                                                                                                                        guards and abstain-not-compatible.
exception conditions per instance across soft and hard refine-
ment iterations on Debatepedia and ARCT.
                                                                                                                                                                                        of genuine incompatibility between premise and claim.
                                                                                                                VFR ↑                         Leak ↓                                    Figure 4 decomposes the instances whose theory is not proved
                                               Debatepedia                                                                                                                              within the standard budget. We operationalize the two ab-
                                               GUARD (full)                                     76.52                                          2.07                                     stention states by granting each such instance ten additional
                                                 w/o soft critique                          36.03 (−40.5)                                     24.58                                     hard iterations: cases that become provable are counted as
                                                 w/o assumptions (A)                        53.04 (−23.5)                                     10.27                                     abstain-missing-guards (AMG), and the remainder as abstain-
                                                 w/o definitions (∆)                        62.35 (−14.2)                                      6.10                                     not-compatible (ANC). Across backbones and datasets, 63.5–
                                                 w/o exceptions (X)                          73.68 (−2.8)                                     2.67                                      74.3% of the unproven instances are AMG, so the dominant
                                               ARCT                                                                                                                                     cause of abstention is an exhausted budget rather than an
                                               GUARD (full)                                     81.00                                          1.82                                     argument that resists explicitation; under the doubled budget,
                                                w/o soft critique                           41.50 (−39.5)                                     21.70                                     the solver-pass rate of GPT-5.1 would reach 93.5% on De-
                                                w/o assumptions (A)                         49.50 (−31.5)                                     18.18                                     batepedia and 95.5% on ARCT. The remaining ANC core is
                                                w/o definitions (∆)                         71.50 (−9.5)                                       7.14
                                                                                                                                                                                        small but persistent, ranging from 6.5% of all instances for
                                                w/o exceptions (X)                          78.50 (−2.5)                                      2.48
                                                                                                                                                                                        GPT-5.1 to 16.6% for DeepSeek-V3.2 on Debatepedia and
                                                                                                                                                                                        from 4.5% to 14.0% on ARCT, and it contracts monotonically
Table 3: Ablation study with GPT-5.1 on Debatepedia and                                                                                                                                 as the backbone strengthens, indicating that part of what a
ARCT. The gray values in parentheses give the VFR drop                                                                                                                                  weaker model reports as incompatible reflects the limits of
relative to the full system. Results for the remaining backbones                                                                                                                        its elicitation rather than of the argument.
are reported in the Appendix E.
                                                                                                                                                                                                                                                Related Work
being added on demand, as counterexamples to a specific                                                                                                                                 Material inference, defeasibility, and implicit warrants.
guard surface, rather than elicited up front. The hard phase                                                                                                                            The conceptual background comes from inferentialist ac-
barely changes the size of the context: ten hard iterations add                                                                                                                         counts of material inference (Brandom 1994, 2008, 2002;
at most 0.9 assumptions and 0.5 definitions or exceptions                                                                                                                               Hlobil and Brandom 2024) and from classical work on defea-
per instance on either dataset. Solver feedback thus drives                                                                                                                             sible and non-monotonic reasoning (Reiter 1980; McCarthy
local logical corrections to guards rather than proposing new                                                                                                                           1980; Pollock 1987; Dung 1995). In NLP, these concerns
elicited contexts.                                                                                                                                                                      surface in argument reasoning benchmarks whose decisive
   The soft symbolic critique and the assumption layer                                                                                                                                  step is the reconstruction of an implicit warrant (Habernal
carry most of the performance. Table 3 removes one com-                                                                                                                                 et al. 2018; Gupta, Zuckerman, and O’Connor 2024). We
ponent at a time with GPT-5.1. Removing the soft critique                                                                                                                               borrow these distinctions to define what counts as a legiti-
is the most damaging intervention and degrades validity and                                                                                                                             mate guard, but operationalize them computationally, as an
faithfulness at once: VFR falls by 40.5 points on Debatepedia                                                                                                                           autoformalization problem with explicit success and failure
and 39.5 on ARCT, leakage rises from 2.07% to 24.58%                                                                                                                                    states.
and from 1.82% to 21.70%. Among the elicitation layers,                                                                                                                                 Argument mining, debate corpora, and support structure.
assumptions matter most: their removal costs 23.5 points on                                                                                                                             Debatepedia and related corpora have been used to study
Debatepedia and 31.5 on ARCT, and the larger drop on ARCT                                                                                                                               argumentative support, contradiction, and structure over topic-
reflects that its instances are constructed around a missing                                                                                                                            bound debate text (Niculae, Park, and Cardie 2017; Lawrence
warrant, which is exactly what the assumption layer supplies.                                                                                                                           and Reed 2020), typically by predicting labels, retrieving
Definitions contribute a further 14.2 and 9.5 points, since                                                                                                                             support, or reconstructing warrants in natural language. Our
term normalization is what lets guards and premise unify                                                                                                                                setting is narrower but deeper: once a support relation is given,
within a proof, while exceptions cost only 2.8 and 2.5 points                                                                                                                           GUARD constructs the proof package that makes its hidden
in aggregate, as few accepted proofs need a rebuttal condition                                                                                                                          bridge explicit without altering the argumentative meaning
to close.                                                                                                                                                                               of the original pair.
   Abstention is mostly a matter of missing guards, not                                                                                                                                    Closest to our work, solver-guided explanation verification
for NLI (Quan et al. 2024b, 2025a) refines explanatory sen-        Bangkok, Thailand: Association for Computational Linguis-
tences that are already given while our method starts from         tics.
debate premise-claim pairs, search for admissible guards,          Habernal, I.; Wachsmuth, H.; Gurevych, I.; and Stein, B. 2018.
and report success only when the resulting proof is both           The Argument Reasoning Comprehension Task: Identification
solver-valid and contrastively faithful.                           and Reconstruction of Implicit Warrants. In Walker, M.; Ji, H.;
                                                                   and Stent, A., eds., Proceedings of the 2018 Conference of the
                        Conclusion                                 North American Chapter of the Association for Computational
In this paper, we proposed GUARD, a neuro-symbolic frame-          Linguistics: Human Language Technologies, Volume 1 (Long
work that formulates the autoformalization of argumentative        Papers), 1930–1940. New Orleans, Louisiana: Association
material inference as guard completion, turning implicit,          for Computational Linguistics.
non-monotonic support into explicit, deductively checkable         Hlobil, U.; and Brandom, R. 2024. Reasons for Logic, Logic
inference. By combining context strengthening, symbolic            for Reasons: Pragmatics, Semantics, and Conceptual Roles.
soft critique, solver-guided hard refinement, and contrastive      New York: Routledge.
faithfulness checks, GUARD consistently outperforms state-         Kumar, S.; and Talukdar, P. 2020. NILE : Natural Language
of-the-art LLM-driven theorem proving on Debatepedia and           Inference with Faithful Natural Language Explanations. In
ARCT across four backbone LLMs. In future work, we will            Jurafsky, D.; Chai, J.; Schluter, N.; and Tetreault, J., eds.,
extend guard completion to material inferences from a broader      Proceedings of the 58th Annual Meeting of the Association for
range of domains.                                                  Computational Linguistics, 8730–8742. Online: Association
                                                                   for Computational Linguistics.
                        References                                 Lawrence, J.; and Reed, C. 2020. Argument Mining: A Survey.
Bowman, S. R.; Angeli, G.; Potts, C.; and Manning, C. D.           Computational Linguistics, 45(4): 765–818.
2015. A large annotated corpus for learning natural language       Lu, M.; Delaware, B.; and Zhang, T. 2024. Proof Automation
inference. In Màrquez, L.; Callison-Burch, C.; and Su, J., eds.,   with Large Language Models. In Proceedings of the 39th
Proceedings of the 2015 Conference on Empirical Methods            IEEE/ACM International Conference on Automated Software
in Natural Language Processing, 632–642. Lisbon, Portugal:         Engineering, ASE ’24, 1509–1520. New York, NY, USA: As-
Association for Computational Linguistics.                         sociation for Computing Machinery. ISBN 9798400712487.
Brandom, R. 1994. Making It Explicit: Reasoning, Repre-            McCarthy, J. 1980. Circumscription – a Form of Non-
senting, and Discursive Commitment. Cambridge: Harvard             Monotonic Reasoning. Artificial Intelligence, 13(1-2): 27–39.
University Press.                                                  McCarthy, J. 1986. Applications of Circumscription to For-
Brandom, R. 2002. Articulating Reasons: An Introduction to         malizing Common Sense Knowledge. Artificial Intelligence,
Inferentialism. Philosophical Quarterly, 52(206): 123–125.         28(1): 89–116.
Brandom, R. B. 2008. Between Saying and Doing: Towards             Mistral AI. 2026. Mistral Medium 3.5. https://mistral.ai/
an Analytic Pragmatism. New York: Oxford University Press.         news/vibe-remote-agents-mistral-medium-3-5/.
Cabrio, E.; and Villata, S. 2013. A natural language bipolar       Naess, A. 1949. Toward a Theory of Interpretation and
argumentation approach to support users in online debate           Preciseness. Theoria, 15(1-3): 220–241.
interactions†. Argument & Computation, 4(3): 209–230.              Niculae, V.; Park, J.; and Cardie, C. 2017. Argument Mining
Deepseek-AI. 2025.        DeepSeek-V3 Technical Report.            with Structured SVMs and RNNs. In Barzilay, R.; and
arXiv:2412.19437.                                                  Kan, M.-Y., eds., Proceedings of the 55th Annual Meeting
                                                                   of the Association for Computational Linguistics (Volume 1:
Dung, P. M. 1995. On the acceptability of arguments and its        Long Papers), 985–995. Vancouver, Canada: Association for
fundamental role in nonmonotonic reasoning, logic program-         Computational Linguistics.
ming and n-person games. Artif. Intell., 77(2): 321–357.
                                                                   Nie, Y.; Williams, A.; Dinan, E.; Bansal, M.; Weston, J.; and
Eemeren, F. H. V.; and Grootendorst, R. 2003. A Systematic         Kiela, D. 2020. Adversarial NLI: A New Benchmark for
Theory of Argumentation: The Pragma-Dialectical Approach.          Natural Language Understanding. In Jurafsky, D.; Chai, J.;
Cambridge University Press.                                        Schluter, N.; and Tetreault, J., eds., Proceedings of the 58th
Gordon, T. F.; Prakken, H.; and Walton, D. 2007. The               Annual Meeting of the Association for Computational Lin-
Carneades Model of Argument and Burden of Proof. Artificial        guistics, 4885–4901. Online: Association for Computational
Intelligence, 171(10-15): 875–896.                                 Linguistics.
Gubelmann, R.; Katis, I.; Niklaus, C.; and Handschuh, S.           Nipkow, T.; Wenzel, M.; and Paulson, L. C. 2002. Is-
2023. Capturing the Varieties of Natural Language Inference:       abelle/HOL: a proof assistant for higher-order logic. Springer.
A Systematic Survey of Existing Datasets and Two Novel             Olausson, T.; Gu, A.; Lipkin, B.; Zhang, C.; Solar-Lezama, A.;
Benchmarks. J. of Logic, Lang. and Inf., 33(1): 21–48.             Tenenbaum, J.; and Levy, R. 2023. LINC: A Neurosymbolic
Gupta, A.; Zuckerman, E.; and O’Connor, B. 2024. Harness-          Approach for Logical Reasoning by Combining Language
ing Toulmin’s theory for zero-shot argument explication. In        Models with First-Order Logic Provers. In Bouamor, H.; Pino,
Ku, L.-W.; Martins, A.; and Srikumar, V., eds., Proceedings        J.; and Bali, K., eds., Proceedings of the 2023 Conference on
of the 62nd Annual Meeting of the Association for Computa-         Empirical Methods in Natural Language Processing, 5153–
tional Linguistics (Volume 1: Long Papers), 10259–10276.           5176. Singapore: Association for Computational Linguistics.
OpenAI. 2025. GPT-5.1. https://openai.com/index/gpt-5-1/.         L., eds., Proceedings of the 14th International Conference
Parsons, T. 1990. Events in the Semantics of English: A Study     on Computational Semantics (IWCS), 76–86. Groningen,
in Subatomic Semantics. MIT Press.                                The Netherlands (online): Association for Computational
Paulson, L. C.; and Blanchette, J. C. 2012. Three Years of        Linguistics.
Experience with Sledgehammer, a Practical Link between            Walton, D. 2001. Persuasive Definitions and Public Policy
Automatic and Interactive Theorem Provers. In Sutcliffe,          Arguments. Argumentation and Advocacy, 37(3): 117–132.
G.; Schulz, S.; and Ternovska, E., eds., Proceedings of the       Wang, X.; Wei, J.; Schuurmans, D.; Le, Q. V.; Chi, E. H.;
8th International Workshop on the Implementation of Logics        Narang, S.; Chowdhery, A.; and Zhou, D. 2023. Self-
(IWIL 2010), volume 2 of EPiC Series in Computing, 1–11.          Consistency Improves Chain of Thought Reasoning in Lan-
EasyChair.                                                        guage Models. In The Eleventh International Conference on
Pollock, J. L. 1987. Defeasible Reasoning. Cognitive Science,     Learning Representations.
11(4): 481–518.                                                   Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; Ichter, B.;
Quan, X.; Valentino, M.; Carvalho, D.; Dalal, D.; and Freitas,    Xia, F.; Chi, E. H.; Le, Q. V.; and Zhou, D. 2022. Chain-of-
A. 2025a. PEIRCE: Unifying Material and Formal Reasoning          thought prompting elicits reasoning in large language models.
via LLM-Driven Neuro-Symbolic Refinement. In Mishra, P.;          In Proceedings of the 36th International Conference on Neural
Muresan, S.; and Yu, T., eds., Proceedings of the 63rd Annual     Information Processing Systems, NIPS ’22. Red Hook, NY,
Meeting of the Association for Computational Linguistics          USA: Curran Associates Inc. ISBN 9781713871088.
(Volume 3: System Demonstrations), 11–21. Vienna, Austria:        Williams, A.; Nangia, N.; and Bowman, S. R. 2018. A
Association for Computational Linguistics. ISBN 979-8-            Broad-Coverage Challenge Corpus for Sentence Understand-
89176-253-4.                                                      ing through Inference. In Walker, M.; Ji, H.; and Stent,
Quan, X.; Valentino, M.; Dennis, L.; and Freitas, A. 2024a.       A., eds., Proceedings of the 2018 Conference of the North
Enhancing Ethical Explanations of Large Language Models           American Chapter of the Association for Computational Lin-
through Iterative Symbolic Refinement. In Graham, Y.; and         guistics: Human Language Technologies, Volume 1 (Long
Purver, M., eds., Proceedings of the 18th Conference of           Papers), 1112–1122. New Orleans, Louisiana: Association
the European Chapter of the Association for Computational         for Computational Linguistics.
Linguistics (Volume 1: Long Papers), 1–22. St. Julian’s, Malta:   Wu, Y.; Jiang, A. Q.; Li, W.; Rabe, M.; Staats, C.; Jamnik,
Association for Computational Linguistics.                        M.; and Szegedy, C. 2022. Autoformalization with Large
Quan, X.; Valentino, M.; Dennis, L. A.; and Freitas, A.           Language Models. In Koyejo, S.; Mohamed, S.; Agarwal, A.;
2024b. Verification and Refinement of Natural Language            Belgrave, D.; Cho, K.; and Oh, A., eds., Advances in Neural
Explanations through LLM-Symbolic Theorem Proving. In             Information Processing Systems, volume 35, 32353–32368.
Al-Onaizan, Y.; Bansal, M.; and Chen, Y.-N., eds., Proceed-       Curran Associates, Inc.
ings of the 2024 Conference on Empirical Methods in Natural       Zhang, L.; Quan, X.; and Freitas, A. 2024. Consistent Aut-
Language Processing, 2933–2958. Miami, Florida, USA:              oformalization for Constructing Mathematical Libraries. In
Association for Computational Linguistics.                        Al-Onaizan, Y.; Bansal, M.; and Chen, Y.-N., eds., Proceed-
Quan, X.; Valentino, M.; Dennis, L. A.; and Freitas, A. 2025b.    ings of the 2024 Conference on Empirical Methods in Natural
Faithful and Robust LLM-Driven Theorem Proving for NLI            Language Processing, 4020–4033. Miami, Florida, USA:
Explanations. In Che, W.; Nabende, J.; Shutova, E.; and           Association for Computational Linguistics.
Pilehvar, M. T., eds., Proceedings of the 63rd Annual Meeting
of the Association for Computational Linguistics (Volume 1:
Long Papers), 17734–17755. Vienna, Austria: Association              A     Detailed Experimental Configuration
for Computational Linguistics. ISBN 979-8-89176-251-0.            A.1    Datasets and Sampling
Qwen Team. 2025.                 Qwen3 Technical Report.          We evaluate on Debatepedia and the Argument Reasoning
arXiv:2505.09388.                                                 Comprehension Task (ARCT). The Debatepedia evaluation
Reiter, R. 1980. A logic for default reasoning. Artificial        set contains 247 premise-claim pairs balanced across 19
Intelligence, 13(1): 81–132. Special Issue on Non-Monotonic       topics, with 13 pairs per topic. The ARCT evaluation set
Logic.                                                            contains 200 randomly sampled reason-claim pairs, which are
Sellars, W. 1953. Inference and Meaning. Mind, 62(247):           treated as premise–claim pairs. The same fixed instances are
313–338.                                                          used for every method and backbone so that all comparisons
Storks, S.; Gao, Q.; and Chai, J. Y. 2020. Recent Advances        are paired at the instance level.
in Natural Language Inference: A Survey of Benchmarks,            Dataset selection. The evaluation targets argumentative
Resources, and Approaches. arXiv:1904.01172.                      support whose contextual basis remains partly implicit. A
Toulmin, S. 1958. The Uses of Argument. Cambridge,                suitable dataset must provide a premise-claim relation for
England: Cambridge University Press.                              which the missing background commitments can be made
Valentino, M.; Pratt-Hartmann, I.; and Freitas, A. 2021. Do       explicit and assessed through formal verification. Debatepedia
Natural Language Explanations Represent Valid Logical Ar-         meets this requirement through argument pairs from online
guments? Verifying Entailment in Explainable NLI Gold Stan-       debates. Its extended resource distinguishes argumentative
dards. In Zarrieß, S.; Bos, J.; van Noord, R.; and Abzianidze,    support from textual entailment (Cabrio and Villata 2013),
Dataset        Instances   Topics   Construction used in this paper
Debatepedia      247        19      Topic-balanced premise-claim pairs; 13 instances per topic
ARCT             200         –      Fixed random sample of reason-claim pairs

                                         Table A.1: Summary of the evaluation datasets.


making it relevant to the distinction between a materially             depending on a single model family.
supported argument and an inference whose support has been               Using one model from each of four distinct families broad-
made formally explicit. This setting allows us to examine              ens the comparison beyond multiple versions of the same
what contextual information is needed to turn the original             backbone. The principal comparison remains between meth-
support relation into a verifiable inference.                          ods using the same model, with the decoding settings for
   ARCT complements this setting by focusing directly on               shared tasks held fixed. Repeating this comparison across
implicit warrants (Habernal et al. 2018). Its original task            backbones tests whether the contribution of guard completion
requires identifying the warrant that connects a reason to a           remains consistent when the underlying LLM changes.
claim. In our evaluation, each reason-claim pair serves as               The selection supports a cross-family evaluation under
the input to guard completion. The system must construct               the configurations reported below. It does not establish an
the contextual support needed for formal verification, and             exhaustive ranking of available LLMs. Other general-purpose
success is assessed through the resulting proof and contrastive        backbones could be evaluated through the same interface,
checks. The evaluation consequently concerns the explicit              while comparisons between additional versions of a single
completion of the argument, without scoring the original               family would address sensitivity to model-version choice.
warrant-selection task.
Topic coverage. The Debatepedia evaluation follows the                 A.3    Baseline Control Conditions
19-topic organisation of the extended resource (Cabrio and             All methods share the same downstream autoformalisation and
Villata 2013). These topics provide the basis for evaluating           Isabelle/HOL verification pipeline. They differ only in how
guard completion across different debate contexts. Assigning           the missing inferential material is produced and whether it is
13 premise-claim pairs to each topic gives every topic equal           iteratively revised. The Direct baseline receives no added con-
weight in the 247-instance evaluation set. Larger topics cannot        textual material. The chain-of-thought and Toulmin baselines
dominate the aggregate results simply by contributing more             generate their bridging context once. PEIRCE and GUARD
instances. This balance concerns topic frequency and does              receive theorem-prover feedback and may revise the added
not assume that all topics have the same reasoning difficulty.         context within the common iteration budget. Every solver-
                                                                       passed candidate is subsequently evaluated with the same
A.2       Backbone LLMs and Inference Settings                         premise-contrast and claim-contrast tests used by GUARD.
We evaluate four backbone LLMs through their respec-
                                                                       Baseline selection. The baselines are selected to examine
tive APIs. GPT-5.1 uses the identifier gpt-5.1 (OpenAI
                                                                       how the treatment of missing context affects formal verifica-
2025). Qwen3-Max uses qwen3-max-preview (Qwen
                                                                       tion. Each comparison must produce an inference that can
Team 2025). The identifiers for DeepSeek-V3.2 and Mis-
                                                                       be assessed by the shared theorem prover. This requirement
tral Medium 3.5 are deepseek-chat (Deepseek-AI 2025)
                                                                       allows us to evaluate the contextual support provided by a
and mistral-medium-3-5 (Mistral AI 2026), respec-
                                                                       method and to test whether a successful proof still depends
tively. For GPT-5.1, we set reasoning_effort to medium and
                                                                       on the original premise.
do not specify a sampling temperature. We run Qwen3-
Max and DeepSeek-V3.2 in non-thinking mode and set tem-                   Direct autoformalisation provides the no-context control. It
perature=0.6 for Qwen3-Max, DeepSeek-V3.2, and Mistral                 establishes what can be verified from the formalised premise
Medium 3.5. We do not explicitly set reasoning_effort for              and claim without constructing additional support. The com-
Mistral Medium 3.5. For each backbone, all methods use                 parison with context-generating methods measures the con-
identical decoding configurations for tasks shared across              tribution of making implicit commitments explicit within the
methods. Prompts are instantiated independently for each               same verification pipeline.
example, and outputs generated by one backbone are never                  The 1-shot CoT baseline tests whether a short sequence
used as demonstrations for any other backbone.                         of background sentences can supply the missing connection
                                                                       through general reasoning prompts (Wei et al. 2022). Toulmin-
Backbone selection. The backbone comparison evaluates                  style explication introduces an argumentation-specific account
whether the benefits of guard completion persist across dif-           of that connection. Following the motivation of Gupta, Zuck-
ferent model families. The framework requires an LLM that              erman, and O’Connor (2024), it makes the warrant explicit
can generate contextual support and express natural language           and relates it to supporting background information. Its quali-
sentences in a formal representation. It must also respond             fication and rebuttal condition also provide a way to express
to verification feedback during refinement. The four evalu-            the circumstances under which the support applies. Our one-
ated backbones support these roles through their respective            shot baseline adapts this idea to context generation for a fixed
APIs, allowing the same framework to be evaluated without              premise-claim pair. Comparing these two baselines examines
Stage or method                                Maximum iterations    Termination condition
Soft verification and refinement                       10            PO1–PO4 pass, or budget exhausted
Hard verification and refinement                       10            Isabelle/HOL proof succeeds, no admissible repair remains, or
                                                                     budget exhausted
Faithfulness refinement                                 5            Both contrastive tests pass, no admissible repair remains, or budget
                                                                     exhausted
PEIRCE                                                10             Theorem is proved, or budget exhausted
Extended abstention probe                      +10 hard iterations   Proof succeeds or extended budget is exhausted

                                      Table A.2: Refinement budgets and stopping conditions.


whether an explicit argumentation schema improves on a gen-             As a running illustration, consider the Debatepedia instance
eral sequence of background sentences when both contexts              whose premise is “Many solar energy systems are now price
are generated in a single pass.                                       competitive with coal.” The syntactic-parsing step returns the
   PEIRCE provides the iterative neuro-symbolic comparison            constituent structure
(Quan et al. 2025a). In our setting, its explanatory sentences           Subject: Many solar energy systems
constitute added context that can be refined using theorem-              Linking Verb: are
prover feedback. Its inclusion allows us to compare GUARD                Adverbial Modifier (Time): now
with an approach that already benefits from iterative logical            Subject Complement: price competitive
verification. The common limit of 10 verification and refine-            with coal
ment iterations keeps the hard-refinement budget aligned              from which the formalisation step produces
between the two approaches.
                                                                             ∃x y. SolarEnergySystem(x) ∧ Many(x)
          B       Autoformalisation Protocol                                       ∧ Coal (y) ∧ Now (x)                             (B.2)
B.1    Representation Language                                                     ∧ PriceCompetitiveWith(x, y).
Natural language sentences are translated into first-order            The associated claim “Solar energy is economically sound”
logical forms with Neo-Davidsonian event variables (Parsons           has a generic, non-episodic reading and is accordingly for-
1990). Entity predicates introduce individuals, while verbal          malised with universal force,
predicates introduce events. Thematic-role predicates connect
events to their participants. Multiple verbal eventualities are         ∀x. SolarEnergy(x) −→ EconomicallySound (x), (B.3)
represented by distinct event variables. Quantifiers must bind        and an eventive guard such as “A solar energy system
every variable in their scope. Polarity and connectives must          . . . converts solar energy into usable electricity or heat”
match the source sentence. Predicates referring to the same           introduces an explicit event variable with thematic roles,
entity, event, or relation must remain consistent throughout          e.g. Convert(e) ∧ Agent(e, y) ∧ Patient(e, z). The unifi-
the instance.                                                         cation step guarantees, for instance, that SolarEnergy and
   The autoformaliser is realised as a three-step composition.        PriceCompetitiveWith in Eq. (B.2) are the same symbols,
For each sentence s, a syntactic-parsing step π identifies the        with the same arities, that appear in the guards and in Eq. (B.3).
grammatical constituents. The parse records the subject with
the main and auxiliary verbs. It also identifies objects and com-     B.2    Formalisation of Exception-Management
plements, together with adverbial modifiers. A formalisation                 Items
step F maps the parsed constituents into a Neo-Davidsonian
logical form. A unification step UΣ then rewrites the forms           A defeasible rule family d is formalised as a monotonic
over a shared predicate signature Σ(S). Each concept has the          guarded rule using an abnormality predicate.
same predicate symbol and arity throughout the instance.                            ∀k. φd (k) ∧ ¬Ab d (k) −→ ψd (k).               (B.4)
                                              
                  Φ(s) = UΣ(S) F (π(s)) .                   (B.1)     For a closed exception list, the abnormality condition is
For an input set                                                      defined by
                          S = {T, C} ∪ G,                                         Ab d (k) ←→ χd,1 (k) ∨ · · · ∨ χd,n (k).          (B.5)
the autoformaliser produces                                           For an open-ended list, only the direction from a listed
                   Φ(S) = {Φ(s) | s ∈ S},                             exception to abnormality is asserted, avoiding the claim that
                                                                      the elicited exceptions are exhaustive. In the formalised theory,
where the unification step is applied jointly over all elements       Eq. (B.1) is applied to the rule body φd and head ψd . The
of S to enforce cross-sentence predicate consistency. Each se-        abnormality disjuncts χd,i are autoformalised in the same way.
lected guard becomes an axiom, while the formalised premise           These logical forms are then combined. A single guarded rule
is introduced as a theorem assumption and the formalised              may contain several nested Davidsonian event descriptions,
claim as the proof goal.                                              as illustrated by guard G3 in Listing C.1.
B.3    Automatic Quality Checks                                                Backbone                                                          Debatepedia                     ARCT
Each logical form is checked against the following criteria                    DeepSeek-V3.2                                                            0.812                    0.798
before it is admitted to a theory.                                             Qwen3-Max                                                                0.838                    0.852
  1. Syntactic well-formedness. The formula is complete                        Mistral Medium 3.5                                                       0.861                    0.869
     and has balanced brackets. Its formalised representation                  GPT-5.1                                                                  0.905                    0.917
     uses legal Isabelle/HOL syntax.                                           Avg.                                                                     0.854                    0.859
  2. Variable binding. Every entity and event variable has a
     quantifier or local binder with the intended scope.             Table B.1: Autoformalisation faithfulness (cosine similarity
  3. Predicate consistency. A concept or event has a consis-         between each source sentence and the informalisation of its
     tent predicate name and arity within the instance.              logical form, Eq. (B.6)), computed over premise, claim, and
  4. Semantic coverage. The logical form represents the              guard sentences. The evaluation protocol follows Quan et al.
     source sentence’s content-bearing predicates and their          (2025b).
     arguments. It preserves modifiers and polarity, together
                                                                                                                      100
     with the logical connectives.                                                                                                                                 Debatepedia




                                                                                      Share of Annotated Errors (%)
                                                                                                                                                                   ARCT
                                                                                                                       80
  5. Role fidelity. Semantic roles attach to the correct event
                                                                                                                       60
     and participant. The check covers agent and patien-
                                                                                                                            38.8 39.9
     t/theme roles, as well as recipient, location, and other                                                          40
                                                                                                                                                       28.8 29.5
                                                                                                                                         19.4 16.5
     roles in the sentence.                                                                                            20                                            12.9 14.1


  6. Inference direction. Implications preserve the direction                                                           0
                                                                                                                            Syntax      Implication   Quantifier     Variable
     expressed by the source sentence. Causal links and
     defeasible rules follow the same requirement.
                                                                     Figure B.1: Distribution of autoformalisation errors (syn-
B.4    Faithfulness Evaluation of Autoformalisation                  tax, implication, quantifier, variable) in the generated Is-
                                                                     abelle/HOL theories, averaged over the four backbone LLMs.
The main experiments share the autoformalisation component           Annotation categories follow Quan et al. (2025b).
across all compared methods, so autoformalisation errors
affect every system equally. We quantify the quality of this
component using the two evaluation protocols of Quan et al.
                                                                     the formal premise T ∗ as an assumption and the formal claim
(2025b). In informalisation, an LLM translates each logical
                                                                     C ∗ as the goal. A proof succeeds only when Isabelle/HOL
form back into natural language. The resulting sentence is
                                                                     establishes
compared with the source using the cosine similarity of their
sentence embeddings,                                                                       G ∪ {T ∗ } ⊢ C ∗ .               (C.1)
                                                                    The theory declares the base types entity and event.
            faith(s) = cos e(s), e(ρ(Φ(s))) ,          (B.6)
                                                                     Each unified predicate receives a constant declaration, and
where ρ denotes the informalisation map and e(·) the sentence        each selected guard receives a named axiom guard_Gk. The
encoder.                                                             single theorem places T ∗ in its assumes clause and C ∗ in
   In the human evaluation, annotators inspect the generated         its shows clause. Listing C.1 shows the (abbreviated) theory
Isabelle/HOL theories and assign each erroneous logical              generated for the running example of Section B.1; the proof
form to one of four categories. The syntax category covers ill-      line is the tactic returned by Sledgehammer as described
formed or non-compiling formulas. An incorrect implication           below.
direction or strength is labelled implication. The quantifier cat-
egory covers an incorrect quantifier or scope, while variable        Listing C.1: Isabelle/HOL theory generated for the running
covers unbound or incorrectly reused variables.                      example. Constant declarations, guard G2, and the inner event
   Table B.1 reports the informalisation faithfulness over           descriptions of guard G3 (marked [...]) are abbreviated.
premise, claim, and guard sentences for each backbone;               The closing tactic by blast was found by Sledgehammer.
Figure B.1 shows the distribution of human-annotated error
categories averaged over the four backbones on 300 randomly           1   theory debatepedia_52_hard_0
sampled logical forms. Faithfulness is high and stable across         2     imports Main
backbones (0.798–0.917), and the error mass concentrates on           3   begin
syntax errors, which are exactly the errors that the syntactic        5   typedecl entity
admission check of Section C.1 detects and repairs before             6   typedecl event
verification; genuinely semantic errors (implication direction,
quantification) account for a minority of cases.                      8 consts
                                                                      9    SolarEnergySystem :: "entity ⇒ bool"
      C     Isabelle/HOL Verification Details                        10    PriceCompetitiveWith :: "entity ⇒
                                                                          ,→ entity ⇒ bool"
C.1    Theory Construction                                           11    SolarEnergy :: "entity ⇒ bool"
For each instance, the selected formal guards G =                    12    EnergySource :: "entity ⇒ bool"
{g1∗ , . . . , gm
                ∗
                  } are inserted as axioms. The theorem introduces   13    EconomicallySound :: "entity ⇒ bool"
14    (* ... one constant per unified                ,→ PriceCompetitiveWith x y"
     ,→ predicate ... *)                       55     (* Claim: Solar energy is
                                                     ,→ economically sound. *)
16 (* Guard G1: If many solar energy           56     shows "∀ x. SolarEnergy x −→
     ,→ systems are now price                        ,→ EconomicallySound x"
17     competitive with coal, then every       57     using assms guard_G1 guard_G4 by blast
     ,→ energy source that is
18     solar energy is economically sound.     59   end
     ,→ *)
19 axiomatization where
20    guard_G1: "(∃ x y. SolarEnergySystem
                                                  Before any proof is attempted, the controller performs two
     ,→ x ∧ Many x ∧ Coal y                   automatic admission checks on the formalised theory. The
21                ∧ Now x ∧                   syntax check runs the theory through Isabelle and rejects it
     ,→ PriceCompetitiveWith x y)             if the parser or type checker reports an error. The diagnostic
22               −→ (∀ z. (EnergySource z ∧   and the affected lines are returned for LLM-based refinement,
     ,→ SolarEnergy z)                        subject to a fixed number of refinement iterations. The con-
23                −→ EconomicallySound z)"    sistency check replaces the proof goal with False and runs
                                              Sledgehammer. If
25 (* Guard G3: compiled defeasible rule
     ,→ -- an energy source                                        G ∪ {T ∗ } ⊢ False                   (C.2)
26     that generally delivers energy at
     ,→ prices competitive with               is provable, the axiom set is contradictory. Any subsequent
27     coal for typical uses is               “proof” of C ∗ would be vacuous, so the theory is rejected. The
     ,→ economically sound, unless its        theorem prover output identifies the axioms used to prove the
28     apparent competitiveness is driven     contradiction. Exactly those axioms are returned for LLM-
     ,→ by major subsidies or                 based refinement. Only theories that pass both checks proceed
29     hidden costs (the negated exception    to proof search.
     ,→ condition). Inner
30     event descriptions are elided here     C.2     Proof Search with Sledgehammer
     ,→ as [...] . *)
31 axiomatization where                       Proof search proceeds in two modes. In the direct mode,
32    guard_G3: "∀ x. (EnergySource x         Sledgehammer (Paulson and Blanchette 2012) is invoked
33               ∧ (∃ y u e. Energy y ∧       immediately on the stated goal of Eq. (C.1). The external
     ,→ Deliver e ∧ Agent e x                 automated provers search for a proof from the premise as-
34                  ∧ Patient e y ∧           sumption and the guard axioms. On success, Sledgehammer
     ,→ Generally e ∧ Price u                 reports a reconstructing tactic, such as by blast or by
35                  ∧ At e u ∧ [...])         (metis guard_G1 guard_G4). The controller splices
36               ∧ ¬(∃ z e1. ((Subsidy z ∧    the returned tactic into the theory in place of the Sledgeham-
     ,→ Major z)
37                  ∨ (Cost z ∧ Hidden z))
                                              mer call and re-runs Isabelle to confirm that the reconstructed
38                  ∧ Drive e1 ∧ Agent e1 z   proof checks; the confirmed theory is what is stored and
     ,→ ∧ [...]))                             counted as solver-passed. The proof line of Listing C.1 was
39               −→ EconomicallySound x"      obtained in this mode.
                                                 If no direct proof is found, the controller falls back to a
41 (* Guard G4: Solar energy is radiant       proof-sketch mode. An LLM-based proof-sketch function
     ,→ energy from sunlight,                 produces a structured Isar proof body that decomposes the
42     and everything that is solar energy    entailment into a chain of intermediate facts
     ,→ is an energy source. *)
43 axiomatization where                             T ∗ = f0 =⇒ f1 =⇒ · · · =⇒ fk = C ∗ ,               (C.3)
44    guard_G4: "∀ x. SolarEnergy x ←→
     ,→ (RadiantEnergy x                      where each step names the load-bearing guard axioms it relies
45               ∧ (∃ y. Sunlight y ∧ FromE   on and leaves its local justification as an <ATP> placeholder.
     ,→ x y) ∧ EnergySource x)"               The controller then discharges the placeholders from left to
                                              right. Each <ATP> is replaced by a Sledgehammer call, and
47 (* Guard G2 (definition of a solar         the tactic Sledgehammer returns for that subgoal is substituted
     ,→ energy system) omitted                in place. The sketch succeeds only if every step is discharged
48     for space. *)                          and the completed proof is re-checked by Isabelle as a whole. If
                                              some step cannot be discharged, the failing step, its preceding
50 theorem hypothesis:
51    (* Premise: Many solar energy systems
                                              comments, and the prover messages are recorded as the failure
     ,→ are now price                         context for hard refinement. This two-mode design mirrors the
52       competitive with coal. *)            observation that a single global Sledgehammer call suffices
53    assumes asm: "SolarEnergySystem x ∧     for short bridges, while multi-guard instances (e.g. those
     ,→ Many x ∧ Coal y                       using a formalised defeasible rule together with a definition)
54                  ∧ Now x ∧                 benefit from an explicit intermediate decomposition.
C.3    Failure Extraction and Hard Refinement                         Table D.1 (continued)
When a theory fails, the controller records the failing theorem       Impaired reasoning and learning abilities reduce a person’s
or proof step and the current goal state. It retains the relevant     general cognitive ability over time.
type or syntax diagnostics and Sledgehammer messages,                 A reduction in general cognitive ability over time constitutes a
together with the axioms supplied to that step. The LLM-based         decline in intelligence.
                                             hard
hard critique and refinement function frefine      receives this      Now generate the background sentences for the following
feedback alongside the current natural-language guards and            instance:
their logical forms. The function classifies the failure under        Provided Context: {premise_sentence}
PO1–PO4 before proposing a refinement. It may correct an              Provided Claim: {hypothesis_sentence}
erroneous representation or add or refine a missing contextual        Background Sentences:
item. Guard selection may also change, while the original
premise and claim remain unchanged.
                                                                      Table D.2. Baseline prompt: explanatory-sentence genera-
                 D     Prompt Templates                               tion.
Tables D.1–D.12 list the prompt templates used in our experi-
                                                                      SYSTEM: You are an expert in natural language inference. A
ments. The three baseline prompts appear first, followed by           hypothesis sentence and a premise sentence will be provided;
the prompts used at each stage of the pipeline. Curly-braced          however, the premise sentence may not always be included.
items such as {premise} are placeholders instantiated at              Please generate some explanatory sentences to state how to
run time. The complete system and user prompts, including             infer the provided hypothesis sentence.
all few-shot demonstrations, are provided in the submitted            USER: Here are some examples:
code.
                                                                      Provided Hypothesis Sentence: Some children outside having
  Table D.1. Baseline prompt: chain-of-thought background             fun and playing.
  context.                                                            Provided Premise Sentence: Three children in swimsuites are
                                                                      having fun outside near a white building.
  SYSTEM: You are an expert in argumentative reasoning.               Explanatory Sentences:
  You will be given a context and a claim. The context is             Three children can be considered as some children, and they
  intended to support the claim, but some of the connecting           are children.
  background information may be implicit. Generate a short,           If some children are having fun outside, they are also playing
  ordered chain of background sentences that makes the                outside.
  reasoning from the context to the claim explicit.                   Provided Hypothesis Sentence: Azathioprine interferes with
  Requirements:                                                       the assembly of proteins.
  1. Treat the provided context as indispensable starting             Explanatory Sentences:
  information.                                                        DNA contains genetic instructions for proteins, and RNA,
  2. The context and the generated background sentences, taken        synthesized from DNA, helps assemble the proteins.
  together, should support the claim.                                 The assembly of proteins is dependent on the synthesis of
  3. The generated background sentences alone must not be             DNA and RNA.
  sufficient to support the claim without the provided context.       Azathioprine interferes with DNA and RNA synthesis.
  4. Each background sentence should contribute one distinct          Do not generate explanatory sentences that just repeat or
  general fact, rule, or intermediate connection.                     represent the same meaning of the hypothesis sentence. The
  5. Arrange the background sentences in the order in which           explanatory sentences should form an inference chain to infer
  they are needed to reach the claim.                                 the hypothesis sentence and must not repeat the hypothesis
  6. Do not repeat or paraphrase the complete context.                sentence.
  7. Do not repeat, paraphrase, or directly state the complete        Give me the explanatory sentences in the above example
  claim.                                                              format:
  8. Do not use a pair-specific shortcut such as “If the context is
  true, then the claim is true.”                                      Provided Hypothesis Sentence:
  9. Do not introduce unrelated information, contradictory            {hypothesis_sentence}
  information, or a conclusion stronger than the provided claim.      {premise_sentence}
  10. Generate 2 to 4 concise declarative sentences, with one         Explanatory Sentences:
  sentence on each line.
  11. Return only the requested format without numbering,
  bullet points, or additional commentary.
                                                                      Table D.3. Baseline prompt: Toulmin-style context genera-
  USER: Here is one example:                                          tion.
  Provided Context: Television and texting are disturbing brains
  at a young age.                                                     SYSTEM: You are an expert in argumentative reasoning.
  Provided Claim: People are getting dumber.                          You will be given a context and a claim. The context is
  Background Sentences:                                               intended to support the claim, but the argumentative
  A disturbance to a person’s brain at a young age impairs that       commitments connecting them may be implicit. Generate a
  person’s later reasoning and learning abilities.                    concise Toulmin-style context that makes the implicit support
Table D.3 (continued)                                               Table D.3 (continued)

relation explicit.                                                  Provided Context: {premise_sentence}
The generated context should contain:                               Provided Claim: {hypothesis_sentence}
1. One qualified bridging sentence that expresses the main          Toulmin Context Sentences:
general connection from the type of information stated in the
context to the type of conclusion stated in the claim.
2. One backing sentence that provides a general fact or             Table D.4. Pipeline prompt: eliciting enthymematic as-
principle supporting the bridging connection.                       sumptions.
3. When needed, one additional bridging sentence that
completes an intermediate reasoning step or aligns the              SYSTEM: You are an expert in material inference and
concepts used in the context and the claim.                         argument reconstruction.
4. One rebuttal condition describing a genuine circumstance
under which the bridging connection may not apply.                  USER:
                                                                    Premise: {premise}
Requirements:                                                       Claim: {claim}
1. The provided context and the generated Toulmin context
sentences, taken together, should support the claim.                Elicit a concise set of implicit assumptions that are needed for
2. The generated sentences alone must not be sufficient to          the premise to support the claim. Assumptions may include
support the claim without the provided context.                     normality conditions, domain restrictions, ceteris-paribus
3. The provided context must remain an indispensable starting       conditions, or an implicit warrant.
point of the argument.                                              Constraints:
4. Express the appropriate inferential qualifier, such as           1. Do not restate the claim or introduce a rule equivalent to the
“generally”, “normally”, “typically”, or “necessarily”, inside      claim.
the main bridging sentence.                                         2. Do not add facts that contradict the premise.
5. Use “necessarily” only when the connection is genuinely          3. Make each assumption independently understandable and
exceptionless; otherwise prefer a defeasible qualifier such as      formalizable.
“generally” or “normally”.                                          4. State only assumptions that are potentially load-bearing.
6. The bridging sentences must express general relations rather     5. Mark uncertainty explicitly rather than presenting a
than facts that assert the claim about the current case.            doubtful fact as universally true.
7. The backing sentence must support the bridging relation          Return one item per line with a short justification of its role.
and must not introduce new case-specific evidence that
independently establishes the claim.
8. The rebuttal condition must describe only a possible
exception; do not assert that the exception actually holds in the   Table D.5. Pipeline prompt: eliciting definitions and term-
provided case.                                                      normalisation facts.
9. Do not repeat or paraphrase the complete context.
10. Do not directly state or paraphrase the claim as a fact about   SYSTEM: You are an expert in lexical semantics, definitions,
the current case.                                                   and formalization.
11. Do not use a pair-specific shortcut such as “If the provided    USER:
context is true, then the provided claim is true.”                  Premise: {premise}
12. Do not merely combine the complete context and claim            Claim: {claim}
into a conditional sentence.                                        Candidate assumptions: {assumptions}
13. Generate three to four concise sentences, with one
                                                                    Identify definitions or term-normalisation facts needed to align
sentence for each applicable argumentative role.
                                                                    the concepts used by the premise, claim, and assumptions.
14. Return only the requested format without JSON,
numbering, bullet points, or additional commentary.                 Constraints:
                                                                    1. Preserve the context-specific meaning of each term.
USER: Here is one example:
                                                                    2. Do not broaden a term merely to make the claim provable.
Provided Context: Television and texting are disturbing brains      3. Prefer a directional subsumption or equivalence only when
at a young age.                                                     it is semantically justified.
Provided Claim: People are getting dumber.                          4. Do not introduce the claim, a paraphrase of the claim, or an
Qualified Bridging Sentence: Disturbing brain development at        answer-bearing definition.
a young age generally impairs the later development of              5. Write each item as one formalizable sentence.
reasoning and learning abilities.
Backing Sentence: Reasoning, learning, and memory depend
on healthy brain development during childhood.
Additional Bridging Sentence: People whose reasoning and            Table D.6. Pipeline prompt: constructing defeasible rules
learning abilities undergo a sustained decline become less          and exceptions.
intelligent over time.
Rebuttal Condition: This connection may not apply when the          SYSTEM: You are an expert in defeasible reasoning and
disturbance is too minor to affect cognitive development or         exception management.
when its effects are fully offset by other influences.              USER:
Now generate the Toulmin context sentences for the following        Premise: {premise}
instance:                                                           Claim: {claim}
Table D.6 (continued)                                               Table D.8 (continued)

Assumptions: {assumptions}                                          2. Do not select the claim, a paraphrase of the claim, or an
Definitions: {definitions}                                          answer-bearing rule equivalent to the claim.
Construct only the defeasible rules needed to connect the           3. Every selected guard must be load-bearing: removing it
premise to the claim. For each rule, list concrete exception        should break the intended derivation.
conditions that would block its application.                        4. The selected guards alone must not prove the claim without
                                                                    the premise.
Constraints:                                                        5. Select zero or more items from each category according to
1. Separate the rule antecedent, rule consequent, and               necessity; do not pad the set merely to include every category.
exceptions.                                                         6. If the context is insufficient, return FAIL and list repair
2. Keep each rule local; do not use an unconditional rule           candidates.
whose consequent is the claim.
3. Exceptions must describe circumstances in which the rule is
not reliable, not arbitrary reasons to reject the claim.
4. State whether the exception list is intended to be closed or
                                                                    Table D.9. Pipeline prompt: soft symbolic critique under
open-ended.
                                                                    PO1–PO4.
5. Do not add an exception or rule that is not relevant to this
inference.                                                          SYSTEM: You are a strict verifier of formalized material
                                                                    inference.
                                                                    USER:
Table D.7. Pipeline prompt: translating sentences into logi-        Premise T ∗ : {formal_premise}
cal forms.                                                          Claim C ∗ : {formal_claim}
                                                                    Selected guards G: {formal_guards}
SYSTEM: You are an expert in first-order logic and
                                                                    Evaluate the candidate under four proof obligations:
Neo-Davidsonian event semantics.
                                                                    PO1 Representation sanity: syntax, types, arities, bindings,
USER:                                                               roles, and predicate normalization are coherent.
Natural-language sentence: {sentence}                               PO2 Support adequacy: the guards cover the missing
Translate the sentence into one well-formed logical expression.     inferential material and make relevant exceptions explicit.
Requirements:                                                       PO3 Strict support: G together with T ∗ is sufficient to derive
1. Introduce an event variable for every content-bearing verbal     C∗.
event.                                                              PO4 Dependence: G alone does not derive C ∗ , and every
2. Use distinct event variables for distinct events.                selected guard is necessary for the intended proof.
3. Bind every entity and event variable with the correct            Do not silently repair the input while judging it. For every
quantifier scope.                                                   failed obligation, identify the exact item responsible and
4. Preserve negation, modality, conditionals, conjunction,          provide either: (a) a repair to an existing item; or (b) a
disjunction, and implication direction.                             description of a genuinely missing item. Return PASS only
5. Use consistent predicates, arities, entities, and semantic       when all four obligations pass.
roles.
6. Represent only content licensed by the sentence; do not add
background knowledge or a predicate that is absent from its
meaning.                                                            Table D.10. Pipeline prompt: refinement from Is-
7. Produce a form that can be compiled into Isabelle/HOL.           abelle/HOL diagnostics.
Return only the logical form and a compact predicate glossary.
                                                                    SYSTEM: You repair a formal theory using theorem-prover
                                                                    diagnostics. Preserve the meaning of the original premise and
                                                                    claim.
Table D.8. Pipeline prompt: selecting a minimal guard set.          USER:
                                                                    Premise and claim: {premise_claim}
SYSTEM: You are an expert in material inference, formal             Current strengthened context and selected guards:
inference, and argumentation theory.                                {current_context}
USER:                                                               Current logical forms: {logical_forms}
Premise and formalization: {premise_and_form}                       Isabelle/HOL diagnostic and failed proof step:
Claim and formalization: {claim_and_form}                           {prover_feedback}
Available assumptions, definitions, and exception-management        Diagnose the failure under PO1–PO4, then make the smallest
items: {strengthened_context}                                       admissible repair. You may revise an erroneous logical form,
Select the smallest set of guards that jointly covers the missing   repair or add a missing context item, or change guard selection.
inferential material needed for the premise to support the          You must not edit the original premise or claim, assert the
claim.                                                              claim as a guard, or make the proof independent of the
Constraints:                                                        premise. Return the complete updated context and guard set.
1. Select only from the supplied context; do not invent a
missing item.
  Table D.11. Pipeline prompt: premise- and claim-side con-           F.1   Debatepedia #197: Video-Game Play and
  trastive probes.                                                          Cognitive Benefits
  SYSTEM: You generate hard contrastive tests for                     Input.
  argumentative support.                                                 Premise: Moderate video-game play may have positive
  USER:                                                                  effects on developing minds.
  Original premise: {premise}                                            Claim: Video games can have cognitive benefits for
  Original claim: {claim}                                                young people.
  Generate:
  A1. One same-topic counter-premise that should not support          Strengthened context. Stage I harvests the following con-
  the original claim. It must be plausible and relevant to the        text inventory from the premise–claim pair. Items later se-
  broad topic, but it must not be a paraphrase or direct negation     lected as guards are marked with their guard id.
  of the original premise.
  A2. One nearby cross-subtopic claim that is not warranted by        Assumptions A
  the original premise. It must be plausible and topically related,
  but it must test a materially different conclusion.                 A1 (bridging, implicit): Developing minds are the
  Explain briefly why each replacement should break the               minds of young people.
  original support relation. Do not generate an obviously             A2 (semantic disambiguation, received standard; → G1):
  nonsensical or contradictory probe.                                 Positive effects on developing minds are cognitive benefits
                                                                      for those minds. Rationale: links the general phrase “positive
                                                                      effects” in the premise to the specifically cognitive benefits
  Table D.12. Pipeline prompt: repairing a solver-valid but           asserted in the claim.
  leaky guard set.                                                    A3 (pair-specific shortcut, later discarded by selection): If
                                                                      moderate video game play may have cognitive benefits for
  SYSTEM: You repair a formally valid argument that failed a          young people then it is correct to say that video games can
  contrastive faithfulness check.                                     have cognitive benefits for young people.
  USER:
  Original premise, claim, guards, and proof:
                                                                      Definitions ∆
  {verified_candidate}
  Leaking contrastive theory and leak report:                         D1 (moderate video-game play): Moderate video-game
  {leak_report}                                                       play is a level of engagement with video games in terms of
  Revise the guard set so that:                                       frequency and duration that is neither minimal nor excessive
  1. the original premise and revised guards still prove the          and does not typically interfere with healthy functioning.
  original claim;                                                     D2 (developing minds): Developing minds are the cognitive
  2. the guards alone do not prove the claim;                         systems of children and adolescents whose brain structure
  3. the counter-premise does not prove the claim with the            and mental functions are still undergoing maturation.
  guards;                                                             D3 (young people; → G2): Young people are children and
  4. the original premise does not prove the alternative claim        adolescents who have not yet reached full adulthood.
  with the guards; and                                                D4 (cognitive benefits): Cognitive benefits are advantageous
  5. every guard remains semantically justified and load-bearing.     changes such as improvements in mental processes including
  Narrow or condition over-broad rules rather than adding             attention, memory, reasoning, or problem solving.
  unrelated blockers. Return the complete revised guard set, not      D5 (video-game play): Video-game play is the activity of
  only the changed item.                                              interacting with electronic games that display visual output
                                                                      on a screen and respond to user input.
           E     Complete Ablation Results                            D6 (positive effects): Positive effects are changes in outcomes
                                                                      that are considered beneficial according to accepted
The main paper reports the GPT-5.1 ablation only. Table E.1           psychological or developmental indicators.
reports the same ablation for every backbone on both datasets.
Removing the soft critique is the single most damaging                Exception items X
intervention for all four backbones, and the ordering A ≻
∆ ≻ X in contribution size is stable across backbones and             R1: Moderate video-game play among young people
datasets.                                                             typically involves active and repeated cognitive engagement.
                                                                      χR1,1 : the play consists mostly of passive watching or
                                                                      repetitive actions that demand little mental effort. χR1,2 : the
               F     End-to-End Example                               level of use is wrongly classified as moderate when it is
                                                                      actually minimal or excessive.
This section traces Debatepedia instance #197 through the             R2: Sustained cognitively engaging activities in young people
full pipeline. The example begins with context harvesting             generally have the potential to produce positive cognitive
and follows the selected guards through autoformalisation. It         effects. χR2,1 : strong negative influences such as extreme
records soft and hard verification with their refinements and         stress, sleep deprivation, or neurological damage prevent
concludes with the contrastive checks.                                cognitively engaging activities from producing positive
                                                                     Debatepedia              ARCT
                                Variant                       VFR ↑         Leak ↓        VFR ↑      Leak ↓
                                DeepSeek-V3.2
                                  GUARD (full)          48.58                 6.25     53.50           3.60
                                    w/o soft critique   25.91 −22.7          29.67     29.00 −24.5    30.12
                                    w/o assumptions (A) 34.01 −14.6          16.83     36.50 −17.0    17.98
                                    w/o definitions (∆) 40.08 −8.5           10.81     45.50 −8.0      9.90
                                    w/o exceptions (X)  45.34 −3.2            7.44     51.50 −2.0      4.63
                                Qwen3-Max
                                 GUARD (full)          56.68                  5.41     61.00           3.17
                                   w/o soft critique   30.36 −26.3           29.25     33.50 −27.5    28.72
                                   w/o assumptions (A) 39.68 −17.0           16.24     42.00 −19.0    18.45
                                   w/o definitions (∆) 47.37 −9.3             8.59     52.00 −9.0      8.77
                                   w/o exceptions (X)  54.25 −2.4             5.63     57.50 −3.5      4.96
                                Mistral Medium 3.5
                                  GUARD (full)           62.75                2.52     64.50           2.27
                                     w/o soft critique   37.65 −25.1         21.85     40.50 −24.0    24.30
                                     w/o assumptions (A) 46.56 −16.2         13.53     51.00 −13.5    12.82
                                     w/o definitions (∆) 56.28 −6.5           6.71     59.00 −5.5      6.35
                                     w/o exceptions (X)  61.13 −1.6           3.82     63.00 −1.5      3.08
                                GPT-5.1
                                 GUARD (full)           76.52                 2.07     81.00           1.82
                                    w/o soft critique   36.03 −40.5          24.58     41.50 −39.5    21.70
                                    w/o assumptions (A) 53.04 −23.5          10.27     49.50 −31.5    18.18
                                    w/o definitions (∆) 62.35 −14.2           6.10     71.50 −9.5      7.14
                                    w/o exceptions (X)  73.68 −2.8            2.67     78.50 −2.5      2.48

Table E.1: Complete ablation results for all backbone LLMs. VFR is the Verified-Faithful rate and Leak is the Reject-Leaky
rate, both in percent. Grey values give the absolute VFR drop relative to the full GUARD pipeline. The GPT-5.1 rows reproduce
the ablation reported in the main paper.


cognitive effects.                                                         activity’s potential to produce positive cognitive effects to the
R3 (→ G3, combined with χR3,1 ): When an activity for                      statement that the activity can have cognitive benefits, while
young people has a real possibility of producing positive                  guarding against effects that are too rare, small, or fragile.
cognitive effects, it is usually acceptable to say that the
activity can have cognitive benefits for young people. χR3,1 :                During the soft verification–refinement loop (below), a
the positive cognitive effects are so rare, small, or fragile that         strict-support failure triggers one guard refinement that adds
ordinary speakers would not describe the activity as one that              four assumptions to the workset, yielding guards G4–G7:
can have cognitive benefits.                                               G4 (added, A3′ )
Selected guards. The one-time selector chooses a minimal                   Developing minds are the minds of young people. Connects
initial guard set of three items from the full inventory:                  the mind affected in the premise to the young person it belongs
                                                                           to.
G1 (from A2)
Positive effects on developing minds are cognitive benefits for            G5 (added, A4)
those minds. Load-bearing because it converts the premise’s                Moderate video-game play with positive effects on developing
positive effects on developing minds into the claim-side de-               minds is an activity for young people that has a real possibility
scription of those same effects as cognitive benefits.                     of producing those effects. Lifts the premise facts into the
                                                                           antecedent of the default rule G3.
G2 (from D3)
Young people are children and adolescents who have not yet                G6 (added, A5)
reached full adulthood. Load-bearing because it aligns the                The positive cognitive effects of moderate video-game play
premise’s target group (bearers of developing minds) with the             are not rare, small, or fragile. Rules out the exception condition
claim’s young people.                                                     χR3,1 of G3, so the default applies.
G3 (from R3 +χR3,1 )                                                       G7 (added, A6)
The defeasible rule R3 combined with its exception condition               If playing video games has a cognitive benefit for young
χR3,1 . Load-bearing because it licenses the move from an                  people, then video games have that cognitive benefit for young
people. Carries the conclusion from the playing activity to      28   Rare :: "entity ⇒ bool"
video games, as the claim states.                                29   Small :: "entity ⇒ bool"
                                                                 30   Fragile :: "entity ⇒ bool"
   Hard verification later adds one further guard from prover    31   Have :: "event ⇒ bool"
feedback:                                                        32   Of :: "entity ⇒ entity ⇒ bool"
                                                                 33   VideoGamePlay :: "entity ⇒ bool"
G8 (added by hard repair)                                        34   Moderate :: "entity ⇒ bool"
A cognitive benefit for a young person’s mind is a cognitive     35   VideoGame :: "entity ⇒ bool"
benefit for that young person. The failed proof step needed to
transfer the benefit from the developing mind to its owner; no   37 (* Guard G1: Positive effects on
earlier guard licensed that transfer.                                 ,→ developing minds are cognitive
                                                                      ,→ benefits
Formalisation and theory.       The autoformalised premise       38     for those minds. *)
                                                                 39 axiomatization where
T ∗ and claim C ∗ are:                                           40    guard_G1: "∀z y. (Effect z ∧ Positive
                                                                      ,→ z ∧ Mind y ∧ Developing y ∧
     Listing F.1: Logical forms of the premise and claim.        41      On z y) −→ (Benefit z ∧ Cognitive
                                                                      ,→ z ∧ For z y)"
 T* (P1): ∃x y z e. VideoGamePlay(x) ∧
   ,→ Moderate(x) ∧ Effect(z) ∧                                  43 (* Guard G2: Young people are children
           Positive(z) ∧ Mind(y) ∧                                    ,→ and adolescents who have not yet
   ,→ Developing(y) ∧ Have(e) ∧                                  44     reached full adulthood. *)
           Agent(e, x) ∧ Patient(e, z) ∧                         45 axiomatization where
   ,→ On(z, y)                                                   46    guard_G2: "∀u. YoungPerson u ←→
                                                                      ,→ ((Child u ∨ Adolescent u) ∧
 C* (C1): ∃x y z e. VideoGame(x) ∧                               47      ¬(∃v e. Adulthood v ∧ Full v ∧
   ,→ Benefit(z) ∧ Cognitive(z) ∧                                     ,→ Reach e ∧ Agent e u ∧ Patient e
           YoungPerson(y) ∧ Have(e) ∧                                 ,→ v))"
   ,→ Agent(e, x) ∧ Patient(e, z) ∧
           For(z, y)                                             49 (* Guard G3: Defeasible rule: When an
                                                                      ,→ activity for young people has a real
                                                                 50     possibility of producing positive
  The final hard-pass Isabelle/HOL theory, including all              ,→ cognitive effects, it is usually
guard axioms G1–G8 and the machine-found proof, is:              51     acceptable to say that the activity
                                                                      ,→ can have cognitive benefits for
 Listing F.2: Final hard-pass theory for Debatepedia #197.       52     young people. *)
                                                                 53 axiomatization where
 1   theory debatepedia_197_hard_1                               54    guard_G3: "∀x. (Activity x ∧ (∃u.
 2   imports Main                                                     ,→ YoungPerson u ∧ For x u) ∧
                                                                 55      (∃z. Effect z ∧ Positive z ∧
 4   begin                                                            ,→ Cognitive z ∧ PotentialToProduce x
                                                                      ,→ z) ∧
 6   typedecl entity                                             56      (¬(∃z. Effect z ∧ Positive z ∧
 7   typedecl event                                                   ,→ Cognitive z ∧
                                                                 57         (Rare z ∨ Small z ∨ Fragile
 9   consts                                                           ,→ z)))) −→
10      Effect :: "entity ⇒ bool"                                58      (∃z1 e1 u1. Benefit z1 ∧ Cognitive
11      Positive :: "entity ⇒ bool"                                   ,→ z1 ∧ Have e1 ∧ Agent e1 x ∧
12      Mind :: "entity ⇒ bool"                                  59       Patient e1 z1 ∧ YoungPerson u1 ∧
13      Developing :: "entity ⇒ bool"                                 ,→ For z1 u1)"
14      On :: "entity ⇒ entity ⇒ bool"
15      Benefit :: "entity ⇒ bool"                               61 (* Guard G4: Developing minds are the
16      Cognitive :: "entity ⇒ bool"                                  ,→ minds of young people. *)
17      For :: "entity ⇒ entity ⇒ bool"                          62 axiomatization where
18      YoungPerson :: "entity ⇒ bool"                           63    guard_G4: "∀y. (Mind y ∧ Developing
19      Child :: "entity ⇒ bool"                                      ,→ y) −→ (∃u. YoungPerson u ∧ Of y u)"
20      Adolescent :: "entity ⇒ bool"
21      Adulthood :: "entity ⇒ bool"                             65 (* Guard G5: Moderate video-game play
22      Full :: "entity ⇒ bool"                                       ,→ with positive effects on developing
23      Reach :: "event ⇒ bool"                                  66     minds is an activity for young
24      Agent :: "event ⇒ entity ⇒ bool"                              ,→ people that has a real possibility
25      Patient :: "event ⇒ entity ⇒ bool"                            ,→ of
26      Activity :: "entity ⇒ bool"                              67     producing those effects. *)
27      PotentialToProduce :: "entity ⇒                          68 axiomatization where
       ,→ entity ⇒ bool"                                         69    guard_G5: "∀x y z e u. (VideoGamePlay
Iteration   Diagnostic                                                                 Repair
Soft 0      PO2 support adequacy passes on the selected guards G1–G3;                  Guard refinement adds four assumptions in natural language
            PO3 strict support fails: the premise yields a positive effect on a        (guards G4–G7): the young-person bridge, the activity lifting,
            developing mind and G1 recasts it as a cognitive benefit for that          the exception closure, and the play-to-game transfer. All Stage-II
            mind, but nothing connects the developing mind to a young                  logical forms of the workset are cleared and the selected
            person, nothing lifts moderate video-game play into the                    package (premise, claim, and guards) is re-autoformalised.
            activity-for-young-people antecedent of the default G3, nothing
            rules out G3’s rare/small/fragile exception, and nothing carries
            the conclusion from playing to video games.
Soft 1      All four proof obligations pass (PO1 representation sanity, PO2            —
            support adequacy, PO3 strict support, PO4 dependence); the
            loop stops with SoftPass after one refinement.
Hard 0      hard_fail (proof-sketch mode, 179.3 s): sledgehammer finds no Hard refinement keeps guards G1–G7 unchanged and adds
            proof at the sketch step that strengthens the playing-benefit fact guard G8: “A cognitive benefit for a young person’s mind is a
            with the young person, i.e. the transfer of the cognitive benefit  cognitive benefit for that young person,”
            from the developing mind to the young person whose mind it is; ∀z y u. (Benefit z ∧ Cognitive z ∧ For z y ∧ Mind y ∧
            no guard licensed that transfer.                                   Of y u ∧ YoungPerson u) −→ For z u.
Hard 1      hard_pass (direct sledgehammer, 44.4 s): cvc4, vampire, and                —
            zipperposition all find proofs; the reconstructed tactic is using
            assms guard_G1 guard_G4 guard_G7 guard_G8
            by blast.

                                      Table F.1: End-to-end refinement trace for Debatepedia #197.


         ,→ x ∧ Moderate x ∧ Effect z ∧
70          Positive z ∧ Mind y ∧ Developing y                                    theorem hypothesis:
                                                                                  95
         ,→ ∧ On z y ∧ Have e ∧ Agent e x ∧                                       96 (* Premise: Moderate video-game play
71          Patient e z ∧ YoungPerson u ∧ Of y                                      ,→ may have positive effects on
         ,→ u) −→                                                              97       developing minds. *)
72          (Activity x ∧ For x u ∧                                            98    assumes asm: "VideoGamePlay x ∧
         ,→ PotentialToProduce x z)"                                                ,→ Moderate x ∧ Effect z ∧ Positive z
                                                                                    ,→ ∧
74 (* Guard G6: The positive cognitive                                         99      Mind y ∧ Developing y ∧ Have e ∧
     ,→ effects of moderate video-game play                                         ,→ Agent e x ∧ Patient e z ∧ On z y"
75     are not rare, small, or fragile. *)                                    100    (* Hypothesis: Video games can have
76 axiomatization where                                                             ,→ cognitive benefits for young
77    guard_G6: "∀z. (Effect z ∧ Positive z                                   101       people. *)
     ,→ ∧ Cognitive z) −→                                                     102    shows "∃x y z e. VideoGame x ∧
78      (¬Rare z ∧ ¬Small z ∧ ¬Fragile z)"                                          ,→ Benefit z ∧ Cognitive z ∧
                                                                              103      YoungPerson y ∧ Have e ∧ Agent e x
80 (* Guard G7: If playing video games has                                          ,→ ∧ Patient e z ∧ For z y"
     ,→ a cognitive benefit for young                                         104    using assms guard_G1 guard_G4
81     people, then video games have that                                           ,→ guard_G7 guard_G8 by blast
     ,→ cognitive benefit for young
82     people. *)                                                             106       end
83 axiomatization where
84    guard_G7: "∀x z u e. (VideoGamePlay x
     ,→ ∧ Benefit z ∧ Cognitive z ∧
                                                                              Refinement trace. Table F.1 reports the complete verifica-
85      Have e ∧ Agent e x ∧ Patient e z ∧
     ,→ YoungPerson u ∧ For z u) −→                                           tion and refinement trace.
86      (∃x1 e1. VideoGame x1 ∧ Have e1 ∧
     ,→ Agent e1 x1 ∧ Patient e1 z ∧                                          Contrastive checks. All three Stage IV probes are run
87       For z u)"                                                            against the hard-pass theory with the same guard axioms
                                                                              G1–G8 and direct sledgehammer.
89 (* Guard G8: A cognitive benefit for a
     ,→ young person’s mind is a cognitive                                    Premise check (empty premise)
90     benefit for that young person. *)                                      The assumes asm line is removed from the theorem and
91 axiomatization where                                                       only the shows goal is kept, so the claim is attempted
92    guard_G8: "∀z y u. (Benefit z ∧                                         from the guard axioms alone. Sledgehammer finds no proof
     ,→ Cognitive z ∧ For z y ∧ Mind y ∧                                      (not provable, 15.3 s): the guard set does not entail the claim
93      Of y u ∧ YoungPerson u) −→ For z u"                                   without the premise, so the premise is genuinely load-bearing.
Premise contrast check (same-topic counter-premise)
The generated counter-premise “Excessive video-game play
is linked to attention problems and poorer academic perfor-
mance in developing minds” replaces the original premise
while the claim is kept fixed. Its formalisation is

 ∃x y w v. VideoGamePlay(x) ∧ Excessive(x)
   ,→ ∧ AttentionProblem(w) ∧
    Performance(v) ∧ Academic(v) ∧ Poor(v) ∧
   ,→ Mind(y) ∧ Developing(y) ∧
    LinkedTo(x, w) ∧ LinkedTo(x, v) ∧ In(w,
   ,→ y) ∧ In(v, y)


Sledgehammer finds no proof (not provable, 45.3 s): the guard
set does not license the claim from a harm-focused premise
on the same topic.
Hypothesis contrast check (alternative claim)
The generated neighbor claim “Excessive video-game play
can have cognitive benefits for young people” replaces the
original claim while the premise is kept fixed. Its formalisation
is

 ∃x y z e. VideoGamePlay(x) ∧ Excessive(x)
   ,→ ∧ Benefit(z) ∧ Cognitive(z) ∧
    YoungPerson(y) ∧ Have(e) ∧ Agent(e, x) ∧
   ,→ Patient(e, z) ∧ For(z, y)


Sledgehammer finds no proof (not provable, 44.9 s): the
premise about moderate play does not warrant a conclusion
about excessive play under the same guards.
   Since the original theorem is provable and all three con-
trastive probes are not provable, the instance is verified
Verified-Faithful.
