                                          Human–LLM Deliberation as Interactive Proof: Conditions
                                                 for Verifiability Without Transparency

                                         Baotong Zhang                                                   baotong.zhang@stern.nyu.edu
                                         Stern School of Business
                                         New York University
                                         New York, NY, USA
                                         Dean Foster                                                                   foster@UPenn.edu
                                         Amazon
arXiv:2609.24895v1 [cs.CL] 21 Sep 2026




                                         New York, NY, USA
                                         João Sedoc                                                               jsedoc@stern.nyu.edu
                                         Stern School of Business
                                         New York University
                                         New York, NY, USA


                                                                                    Abstract
                                             When an LLM supplies an argument that a user could not readily construct, how can the
                                             user decide whether to accept its claim? Inspired by interactive proofs, we model human–
                                             LLM deliberation as an interaction between a prover with unrestricted internal search and
                                             a resource-bounded human verifier. The verifier requests and checks supporting details
                                             without access to the LLM’s internal state. Passed checks accumulate evidence toward
                                             an acceptance threshold. We prove anytime-valid soundness against adaptive provers: the
                                             probability of ever accepting a false claim is at most a chosen error level, provided the
                                             task supplies bounds on false passes and human checking errors that remain valid after
                                             every relevant history. A finite-horizon completeness bound additionally requires bounds
                                             on the adequacy of honest responses and sufficient diagnostic progress. Further checks can
                                             strengthen the evidence for acceptance, but each requires another adequate response and
                                             reliable human effort. Whether this tradeoff permits certification depends on the verifier’s
                                             effort budget, cognitive load, expertise, and fatigue. We identify conditions under which
                                             the supplied bounds certify a specified sequence of local checks but not a specified global
                                             check under the same resource budgets.
                                             Keywords: Interactive Proofs, Human-AI Decision-Making, Resource-Bounded Verifica-
                                             tion, Verifiability, Human-LLM Deliberation


                                         1 Introduction
                                         When an LLM supplies an argument that a user could not readily construct, the user still
                                         needs grounds for deciding whether to accept its claim. Our central question is whether
                                         that user can obtain such grounds through challenges within their own resource budget.
                                         Interactive proofs motivate a division of work between a powerful prover and a bounded
                                         verifier (Goldwasser et al., 1989): the prover supplies arguments or evidence, while the
                                         verifier selects and executes checks. We study the conditions under which this division
                                         supports reliable human–LLM deliberation.




                                                                                          1
                                Zhang, Foster, and Sedoc




    The question arises in human–AI decision support, where predictions can inform conse-
quential choices (Kleinberg et al., 2018) and users receive performance information, explana-
tions, or other assistance (Lu et al., 2025; Lai and Tan, 2019; Lai et al., 2023). LLMs extend
this setting by producing arguments and responding to follow-up questions. Early work on
GPT-4 documented broad capabilities across difficult tasks (Bubeck et al., 2023), while
hallucination research identifies fabrication, contradiction, and unfaithfulness to source ma-
terial or context (Ji et al., 2023; Huang et al., 2025). Prompt-only self-correction based on
a model’s own feedback has not been robustly demonstrated on general tasks (Kamoi et al.,
2024).
    A user faced with an uncertain answer may ask the LLM to explain it. The expla-
nation can make the output more inspectable (Zhao et al., 2024), but its plausibility and
faithfulness are distinct (Jacovi and Goldberg, 2020). Self-explanations may fail to track
answer generation (Agarwal et al., 2024), and chain-of-thought can omit biasing influences
(Turpin et al., 2023). Optimizing plausibility may itself mislead users (Jin et al., 2025).
The user therefore still needs to identify what in the explanation can be checked. Following
the verifiability criterion of Fok and Weld (2024), we focus on evidence about the claim’s
consequences or a supporting derivation. Here, verifiability without transparency means
certification without access to the LLM’s internal state or reconstruction of its generation
process.
    The user need not request the entire supporting argument at once. Starting from a high-
level argument, they can question a premise, request support for an inference, propose a
counterexample, or ask for an executable test. The LLM supplies details in response, while
the target claim remains fixed. Checking the requested details separately may make the
review more manageable for a user with limited attention or domain expertise. Deliberation
can expose competing arguments (Fishkin, 2018; Mercier and Sperber, 2011), and human–
LLM deliberation and tool-interactive critique have shown benefits in some settings (Ma
et al., 2025; Madaan et al., 2023; Gou et al., 2024).
    For example, an organizer reviewing a conference schedule can challenge the claim that
it has no conflicts by checking selected speaker and room constraints against fixed records
(Section 3.4). The organizer needs a challenge policy they can afford to select and execute,
with a justified probability of exposing a conflict if one exists. Task structure, random-
ized audits, external checkers, formal verification, or suitable calibration may support this
diagnostic guarantee. We take the policy and its checking guarantees as inputs and ana-
lyze how the resulting checks support an acceptance decision; constructing them remains
a task-specific requirement. Clarification can guide later questions, with diagnostic checks
supplying the certification evidence.
    We formalize this setting with an LLM prover whose internal search is unrestricted and
a resource-bounded verifier. Our model allows the LLM to give inadequate responses and
the human to make checking errors. Adequate honest responses and correctly executed
checks recover the ideal case. This separates the computational division of work from the
cognitive burden of carrying it out: even a computationally efficient check may exceed a
particular person’s attention, knowledge, or effort budget.




                                              2
                          Verifiability without Transparency




   We make three contributions:

  1. We specify a finite-horizon challenge–response protocol for a fixed claim, including
     verifier-directed requests for evidence, a certificate-based acceptance rule, and con-
     servative rejection when the verification budget is exhausted. The verifier can adapt
     questions and request details as needed.

  2. We prove conditional certification guarantees: anytime-valid soundness against adap-
     tive provers and finite-horizon completeness under response and execution reliability
     bounds, without requiring independent rounds. We retain a diagnostic guarantee
     during adaptive follow-ups by reserving a chosen probability for reference checks.
     Instantiations meeting the additional requirements of Corollary 1 yield interactive
     proofs.

  3. We identify which review lengths meet both certification targets within the verifier’s
     resources (Section 5). This certifiable effective region depends on effort, cognitive load,
     expertise, and fatigue. Proposition 3 identifies when the supplied bounds certify a
     specified decomposed review but not a specified global checker under common resource
     constraints and separately justified diagnostic bounds. The thresholds show how much
     cognitive load must fall to compensate for splitting effort across rounds and relying
     on repeated adequate responses and correct checks.

    The LLM-only simulations test whether answers accepted without revision are more
accurate than the rest; they do not validate the human-verifier assumptions. Appendix C
treats the separate privacy question: under the simulation and prefix-consistency assump-
tions stated there, stopping at the certificate threshold preserves honest-verifier zero knowl-
edge.

2 Related Work
A human reviewing an LLM’s answer must decide what evidence to request and when it is
enough to accept the claim. Related work offers several ways to organize this interaction
and quantify its reliability. We compare how these approaches allocate verification work,
which errors their guarantees control, and what they require of the evaluator.

2.1 Interactive Proofs and Machine Prover–Verifier Systems
Interactive proofs motivate our central abstraction: a powerful prover makes a claim, while a
weaker verifier interrogates it before deciding whether to accept. Classical theory formalizes
this division through completeness and soundness (Goldwasser et al., 1989). For a human
verifier, even a prescribed check may be executed incorrectly. Our model separates this
source of error from the prover’s failure to supply an adequate response.
    Several approaches train models to make their outputs easier to verify. Prover–Verifier
Games learn checkable answers through a game between prover and verifier (Anil et al.,
2022); neural interactive proofs relate approximate verifier-leading Stackelberg equilibria
to valid proof systems (Hammond and Adam-Day, 2025). Prover–verifier training also
evaluates whether weaker model verifiers and time-constrained human raters can check the


                                              3
                                Zhang, Foster, and Sedoc




resulting answers (Kirchner et al., 2024). Self-Proving Models are closer to our setting after
an answer has been produced: a manually specified verifier interactively checks an input–
output pair (Amit et al., 2025). Their framework separates worst-case verifier soundness
from the model’s ability to produce accepted proofs under an input distribution. We likewise
distinguish false acceptance from successful verification of true claims.
    Zero knowledge imposes a separate requirement: an efficient simulator must reproduce
the verifier’s view without access to the prover’s private information. Appendix C gives a
conditional preservation result under stopping. It assumes a simulator for the full continu-
ation interaction and agreement between its stopped prefix and the actual protocol.

2.2 Scalable Oversight and Single-Advocate Protocols
Some oversight proposals use evaluation to construct training signals. Iterated amplification
uses decomposition to construct a training target (Christiano et al., 2018), while weak-to-
strong supervision trains a stronger model on labels supplied by weaker models (Burns
et al., 2024). We consider the subsequent decision faced by a human reviewing an answer
from a fixed model.
    Consultancy closely matches this interaction: a single advocate answers a weaker judge’s
follow-up questions. Studies compare it with debate, where two competing agents present
arguments to a judge (Irving et al., 2018), using both human judges (Michael et al., 2023)
and LLM judges (Kenton et al., 2024). When advocates are assigned correct or incorrect
positions, debate is more robust to incorrect advocacy across the tasks studied by Kenton
et al. (2024). Other experiments test whether stronger debaters help judges identify truth
when relevant information is withheld (Khan et al., 2024), or whether people can use an
unreliable model to solve tasks that neither can reliably solve alone (Bowman et al., 2022).
These studies make the advocate’s influence on the judge a central concern for verification.
    Formal oversight protocols obtain guarantees from assumptions about the computa-
tion being checked. Doubly-efficient debate gives protocols for verifying stochastic agents
(Brown-Cohen et al., 2024); Chen et al. (2026) construct interactive proofs and arguments
for oracle-aided computations under robustness or low-degree-oracle assumptions. Our anal-
ysis instead takes task-specific diagnostic and execution bounds as inputs. Because the
advocate can shape later questions, these bounds must remain valid after every relevant
history. Section 7.2 and Appendix D give one way to preserve a diagnostic bound: mix
adaptive follow-ups with reference checks whose detection probability is justified against
every admissible prover. The mixing probability is chosen before each round, and the
bound applies to the resulting policy under correct execution.

2.3 Local Checking and Sequential Certification
Before a transcript can supply statistical evidence, the task needs concrete claims and
check outcomes. Argumentation frameworks organize attacks, inference rules, and public
commitments (Dung, 1995; Modgil and Prakken, 2014; Prakken, 2005). FActScore evaluates
atomic factual precision against a knowledge source (Min et al., 2023), while ProgramFC
composes local results through an executable fact-checking program (Pan et al., 2023).
Draft, Sketch, and Prove completes formal proof sketches in Isabelle; a successfully checked



                                              4
                          Verifiability without Transparency




proof certifies the formalized theorem, while correspondence to the original informal claim
remains a separate issue (Jiang et al., 2023).
    A correctly executed check may still miss an error. Combining a bound on that event
with a bound on incorrect human execution gives our per-round false-pass bound. Test
supermartingales and e-processes provide the established machinery for accumulating such
evidence under adaptive collection and optional stopping (Shafer et al., 2011; Ramdas et al.,
2023). Our soundness proof applies this construction and Ville’s inequality to the condi-
tional bounds. Completeness also needs adequate honest responses and enough diagnostic
progress before timeout; average checker accuracy does not supply these conditions.
    Recent AI verification methods use sequential testing for related decisions. E-valuator
monitors agent trajectories using black-box verifier scores, with a density-ratio construction
and PAC calibration of decision thresholds (Sadhuka et al., 2025). It controls the probabil-
ity of falsely flagging a successful trajectory as unsuccessful. Cho and Sun (2026) accumu-
late evidence calibrated against a conservative failure reference pool to control release on
workflow-infeasible tasks and analyze finite-horizon release power. Their null concerns the
workflow’s ability to produce a reliable solution. We test the falsity of a fixed claim, with
local bounds required to hold for every admissible adaptive prover.

2.4 Learned Verification, Self-Correction, and Selective Prediction
Verifier feedback can help select an answer or revise it before acceptance. Outcome verifiers
rank candidate mathematical solutions (Cobbe et al., 2021), while process supervision eval-
uates intermediate steps (Lightman et al., 2024). LLM-as-judge systems use another model
to assess completed outputs; agreement with human preferences coexists with position, ver-
bosity, and self-enhancement biases (Zheng et al., 2023). Chain-of-Verification uses model-
generated questions to guide revision (Dhuliawala et al., 2024), although prompted self-
correction remains unreliable without external feedback across broader evaluations (Kamoi
et al., 2024). Our certificate can use a model-generated score or critique only through a
prescribed check with a justified conditional false-pass bound.
    Our protocol and simulations build on Prover–Verifier Deliberation (PVD) (Sedoc et al.,
2026). Frozen LLMs exchange challenges and responses, allowing acceptance, rejection,
answer revision, and retries; a challenge-first variant requires a challenge before acceptance.
PVD labels an attempt Accept + No Change (ANC) when the verifier accepts and the
prover has not changed its answer. In our formal protocol, the prover can supply further
explanations and evidence, but the statement being checked remains unchanged throughout
the run. Acceptance requires the accumulated evidence to reach a prescribed threshold. The
simulations reuse ANC to examine whether stable acceptance is associated with correctness.
They do not implement the certificate rule or establish the Effective Verifier assumption for
human deployment.
    Viewing ANC as a rule for selecting answers connects these simulations to selective
classification. A selective classifier either returns its predicted label or abstains: coverage
is the fraction of cases on which it predicts, and selective risk is the error rate among
those predictions. Geifman and El-Yaniv (2017) use labeled samples to choose a confidence
threshold and bound this error rate, with high probability, for new cases from the same
distribution. A dialogue-based selection rule could likewise be evaluated on independent


                                              5
                                Zhang, Foster, and Sedoc




labeled tasks. Our soundness guarantee addresses a different question: for any given false
claim, how likely is the verifier to accept it? The bound must hold against every admissible
adaptive prover under the stated diagnostic and execution conditions.

2.5 Human Checkability and Bounded Certification
A check that is informative in principle may still be difficult for a person to carry out.
Human-centered studies examine this problem through the assistance given to the evalua-
tor. An LLM-based deliberation interface improved appropriate reliance and performance
in an exploratory graduate-admissions task (Ma et al., 2025), while cognitive forcing re-
duced overreliance more effectively than explanations alone (Buçinca et al., 2021). In fact-
checking, explanations can improve efficiency yet induce overreliance when convincingly
wrong (Si et al., 2024). Receiver ability, attention, motivation, and effort also constrain
costly communication (Dewatripont and Tirole, 2005). These findings motivate allowing
execution reliability to vary with the person and the review conditions.
    Breaking an argument into smaller checks changes both what the reviewer can detect
and how the judgments must be combined. Critiques may expose otherwise missed errors
(Saunders et al., 2022), but local judgments can disagree and their aggregation can change
the conclusion (Saunders et al., 2020). Verifiability provides a relevant criterion for evalu-
ating such assistance: it should make the recommendation easier to check (Fok and Weld,
2024).
    Section 5 relates effort, expertise, and cognitive load to execution reliability, with a
finite round limit representing fatigue. Under common resource constraints and separately
justified diagnostic and execution bounds, Proposition 3 identifies when those bounds certify
a specified decomposed review but not a specified global check.
    The next section specifies the fixed-claim protocol; Section 4 states the local conditions
and derives its certification guarantees.

3 Interactive Human–LLM Deliberation Model
In this section, we define the inference-time interaction studied in the paper: an LLM prover
(P ) and a human verifier (V ) deliberate over a decidable statement and end with Accept or
Reject. If no verdict is reached by the fixed review horizon T , the protocol conservatively
outputs Reject. We first give the interaction interface and a diagnostic example under ideal
execution. Section 4 gives one certification model covering both LLM response inadequacy
and human execution error, with ideal execution as a special case.

3.1 Statements and Dialogue Histories
Let Σ be a finite, non-empty alphabet and let X = Σ∗ be the set of all finite strings over
Σ. Elements of X are token sequences, used here as the raw data type for statements, chal-
lenges, and prover responses. Plain string concatenation would make histories ambiguous,
so ∥ denotes an injective, self-delimiting encoding of finite typed message tuples into X. We
write
                                        z1 ∥ z2 ∥ · · · ∥ zr



                                              6
                          Verifiability without Transparency




for the encoded tuple, not for unmarked concatenation. Let H ⊆ X denote the set of well-
formed encoded histories. If h ∈ H and z ∈ X is a new typed message, then h ∥ z denotes
the corresponding appended history.
    Let S ⊆ X be a set of natural-language statements that can be rendered as logical
propositions decidable with respect to a fixed base axiom system A0 . On this domain, fix
a total ground-truth map
                                     v : S → {⊤, ⊥},
where ⊤ denotes “true” and ⊥ denotes “false.” The language of true statements is
                                   L = {s ∈ S : v(s) = ⊤}.
    Decidability is imposed through the choice of S, while v specifies the truth value to be
certified for each statement. The protocol gives neither party oracle access to v. The LLM
acts through its private state, and the human issues verdicts from bounded information.
Statements whose truth value is ambiguous, contested, or undecidable with respect to the
chosen axioms are outside the model. Within this scope, L is the target language used in
the certification guarantees of Section 4.

3.2 Production, Challenge, and Decision Functions
We model the LLM prover P as a strategy with private state θ ∈ Θ. The state θ may
include trained weights, retrieval state, training data, and internal reasoning resources, but
it is not shown to the verifier. Unrestricted internal search idealizes the prover’s resources;
its messages must still respect the protocol’s format and length limits. For simplicity, Q
is deterministic. Stochastic generation can be handled by adding randomness to θ or by
drawing responses from a conditional distribution instead of using Q.
Definition 1 (Production Function) The production function of P is a mapping
                                      Q : H × Θ → X.
Given a well-formed history h ∈ H and private state θ, Q(h, θ) produces a prover message
y ∈ X.
    Completeness will require local response reliability from an honest prover; soundness
quantifies over arbitrary adaptive prover strategies without modeling private beliefs or in-
tentions.
    The human verifier V is a polynomial-time strategy using information state i, with
challenge repertoire C, challenge-selection policy πV , and decision function U . A concrete
instantiation must supply challenge-selection and checking procedures executable within the
verifier’s budget.
Definition 2 (Verifier Information State) Let I be the universe of information that
could be available to V , including domain knowledge, task instructions, external tools, and
verifier-side axioms. Let I ⊆ {i ⊆ I : |i| < ∞} be the set of finite, representable verifier
information states. For a statement s ∈ S, the realized information state i ∈ I is the
information V can bring to bear when evaluating s, including a verifier-side axiom set Ai ,
distinct from the base system A0 , and basic rules of logical deduction. The exchange itself
is recorded in the history h.

                                              7
                                 Zhang, Foster, and Sedoc




Definition 3 (Challenge Space) Let C ⊆ X be the universe of well-formed challenge
tokens. The challenge space is a set-valued map

                                    C : H × I → 2C \ {∅}.

Given history h ∈ H and information state i ∈ I, C(h, i) is the non-empty set of admissible
challenges that V can formulate from h using i. The set may include weak or redundant
challenges; effectiveness is imposed later.

    In addition to the fixed background information i, the verifier maintains a finite encoded
local state υ ∈ X, initialized from (s, i) and its own randomness. This state records check
outcomes, certificate values, and verifier random bits already used, and is updated by the
prescribed checks and certificate rule. It is available to the verifier but is not part of the
prover-visible message history h.

Definition 4 (Challenge Policy) The verifier selects a challenge from the conditional
distribution πV (· | h, i, υ) in polynomial time. This distribution assigns probability only to
challenges in C(h, i). A deterministic verifier always selects the same challenge at a given
history and state.

Definition 5 (Decision Function) V ’s decision function is a possibly randomized algo-
rithm that runs in polynomial time:

                        U : H × I × X → {Accept, Reject, Challenge}.

Given a well-formed history h whose first component is a statement s ∈ S, information
state i, and current local state υ, U (h, i, υ) returns one of three outputs:

   • Accept: terminate with acceptance of the claim that s ∈ L;

   • Reject: terminate without accepting the claim;

   • Challenge: request another challenge–response round, subject to the review horizon T .

    Below, πV (· | h, i), U (h, i), and other verifier expressions omit the current local-state
argument for brevity. Each choice and decision still uses the state then available. The
observable histories defined below include that state and the random bits already used.
    Separating challenge selection from the decision rule allows adaptive questioning under a
fixed acceptance criterion. Section 4 specifies that criterion using a certificate and states the
required conditions on diagnostic validity, honest response adequacy, and human execution
reliability.

3.3 The Interactive Human-LLM Deliberation Protocol
Messages must be well formed and respect a length limit fixed before execution. The
verifier’s strategy issues only admissible challenges. Section 3.6 specifies the polynomial
resource bounds for the correspondence with classical interactive proofs.



                                               8
                          Verifiability without Transparency




Definition 6 (Finite-horizon deliberation protocol) An Interactive Deliberation con-
cerning a statement s ∈ S is a token exchange between P (private state θ ∈ Θ) and V (in-
formation state i ∈ I) in which P aims to convince V that s ∈ L. The claim and the object
it concerns are fixed before initialization. For admissible messages, the protocol requires at
least one challenge–response round beyond the initial response and sets a review horizon
T ∈ N with T ≥ 1: if V has not reached Accept or Reject after T rounds, the protocol out-
puts Reject. Diagnostic and clarification rounds both count toward this same finite budget
T . A malformed or over-length prover message terminates the protocol immediately with
Reject; no diagnostic evidence is credited to that message.

  1. Initialization.
        • Initialize the verifier’s local state from (s, i) and its own randomness, before
          receiving any prover message.
        • The prover produces the initial response
                                             ys = Q(⟨s⟩, θ),
          where ⟨s⟩ denotes the one-message history containing the statement.
        • Set
                                     h0 ← s ∥ ys ,    m ← 0.
  2. Mandatory First Challenge–Response.
        • The verifier samples or selects x1 ∼ πV (· | h0 , i), so x1 ∈ C(h0 , i). The prover
          responds with
                                         y1 = Q(h0 ∥ x1 , θ).
        • Set
                                    h1 ← h0 ∥ x1 ∥ y1 ,        m ← 1.
  3. Deliberation Loop. Repeat:
        • Evaluation.
           – V executes the prescribed check and updates its local state, then computes
              ω = U (hm , i) using that state. Here hm is the post-response message history
              after m completed challenge–response rounds.
        • Termination.
           – If ω = Accept: terminate with verdict Ω = Accept.
           – If ω = Reject: terminate with verdict Ω = Reject.
           – If ω = Challenge and m = T : terminate with verdict Ω = Reject (review
              horizon reached).
        • Challenge–Response (if ω = Challenge and m < T ):
           – The verifier samples or selects xm+1 ∼ πV (· | hm , i), so xm+1 ∈ C(hm , i).
              The prover responds with
                                         ym+1 = Q(hm ∥ xm+1 , θ).
             – Set
                               hm+1 ← hm ∥ xm+1 ∥ ym+1 ,          m ← m + 1.


                                              9
                                   Zhang, Foster, and Sedoc




  4. Output. Let m′ be the final value of m in an admissible execution. Since the first
                                                                     ′
     challenge is mandatory, 1 ≤ m′ ≤ T . The protocol outputs (d(m ) , Ω), comprising the
     terminal verdict Ω ∈ {Accept, Reject} and the final message sequence
                               ′
                            d(m ) = hm′ = s ∥ ys ∥ x1 ∥ y1 ∥ · · · ∥ xm′ ∥ ym′ .
                                           ′
     The verdict is separate from d(m ) . Immediate rejection of an inadmissible message
     instead returns the admissible message prefix received so far and Reject, possibly before
     any completed round.

    Let Ps,P denote the execution law of ⟨P, Vi,T ⟩(s) over its verdict and transcript, in-
cluding prover, challenge, checker, and human-execution randomness. Here P may be the
implemented strategy Pθ , the honest strategy P H , or an arbitrary adaptive strategy P ∗ ;
deterministic components induce a point mass.
    Let Hm be the random history after m ≤ T completed rounds and hm a realization. If
a run stops at m′ < T , pad it by setting Hm = Hm′ for m′ < m ≤ T , so all certificate
scores and maxima remain defined. Randomness enters through protocol execution; the
truth value v(s) remains fixed.

              ω = Challenge, m < T
                   m←m+1



        Fixed statement s


        Initial response
                                             Challenge                          Response
         LLM prover P           m=1        Human verifier V                   LLM prover P
         ys = Q(⟨s⟩, θ)
                                         xm ∼ πV (· | hm−1 , i)            ym = Q(hm−1 ∥ xm , θ)
         h0 = s ∥ y s



                                          Check and decide
                                                                             Append round
             Route                         Human verifier V
                                                                            Human verifier V
               ω                        Check; update local state
                                                                          hm ← hm−1 ∥ xm ∥ ym
                                            ω ← U (hm , i)



           Reject
                                                 Accept
        ω = Reject or
                                               ω = Accept
     ω = Challenge, m = T


Figure 1: Interactive Human-LLM Deliberation Protocol for admissible messages. The ini-
          tial response is followed by a mandatory challenge. In each round, the verifier
          appends the response to obtain hm , performs the prescribed check and local-state
          update, then evaluates ω = U (hm , i). The branches show continuation and ter-
          minal decisions, including timeout at T . Inadmissible messages cause immediate
          Reject.



                                                  10
                           Verifiability without Transparency




   The review horizon T in Figure 1 is the round budget used in the error bounds of
Section 4 and the fatigue analysis of Section 5.

3.4 Running Example: Reviewing a Conference Schedule
An LLM proposes a conference schedule and claims that it has no conflicts. Lee is listed as
both a keynote speaker and a panelist. An organizer asks, “Can Lee attend both sessions?”
The model must identify the relevant entries in the schedule. If Lee’s keynote runs from
10:00 to 10:30 and the panel from 10:15 to 10:45, comparing the two entries exposes a
conflict. The organizer can check this answer without constructing a replacement schedule
or reviewing every session at once, and can ask follow-up questions within the budget of T
rounds.
    Here “no conflicts” has a specific meaning: every session fits the recorded availability
of its speakers and room, and no two overlapping sessions share a speaker or room. The
schedule, speaker assignments, availability records, and comparison rules are fixed before
review; back-to-back sessions are allowed. With these fixed records and rules, the claim can
be decided by a finite set of time comparisons. Revising the schedule starts certification of
a new claim.
    Finding one conflict refutes the claim. Passing a few checks raises a different question:
how much evidence do they supply about the entire schedule? The next subsection quantifies
this evidence for uniform random checks under ideal execution.

3.5 Diagnostic Checks: An Idealized Example
A diagnostic policy must be able to expose a false claim even when the prover chooses its
answers adaptively. For the fixed conference schedule, the verifier constructs a complete list
of J > 1 constraints from the recorded data: each session’s availability requirements and the
non-overlap requirement for every pair sharing a speaker or room. The list covers exactly
the claim in Section 3.4; it is fixed before the dialogue, rather than selected from the prover’s
answers. Let ssched be the statement that all these constraints hold. The information state
i contains the schedule, source records, constraint list, and checking procedure.
    Building the constraint list, checking it against the source records, and retrieving those
records all count toward the effort in Section 5. Any previously checked materials in i must
be equally available to both designs.
    At each diagnostic round, the verifier samples one constraint uniformly with replace-
ment, independently of the preceding history, and asks the LLM for the relevant records
and time comparison. An ideal check passes only if the cited records match the fixed source
and the selected constraint holds. If the sampled constraint is the non-overlap requirement
for Lee’s two sessions above, a correct check rejects regardless of how the LLM describes
the overlap.
    If ssched is false, at least one of the J constraints is violated. Each fresh draw therefore
has probability at least 1/J of exposing a conflict under ideal execution. Writing Fm−1
for the preceding observable history and Passm for the event that the check passes, every
adaptive prover P ∗ satisfies, at each reachable false-claim history,
                            ssched ,P ∗                           1
                               Pr         (Passm | Fm−1 ) ≤ 1 −     =: q.
                                                                  J

                                                   11
                                Zhang, Foster, and Sedoc




In the certificate rule of Section 4, each passed ideal check multiplies the certificate value
by 1/q. Starting from M0 = 1, an all-pass run of k checks reaches the acceptance threshold
when Mk = q −k ≥ 1/δ. Whether this happens within T depends on the size of the constraint
list and the chosen error target δ.
     For completeness, suppose the schedule has no conflicts and an honest LLM always
supplies correct records and usable comparisons. With ideal check execution, every round
passes, so the protocol accepts with probability one whenever q −T ≥ 1/δ. Otherwise, even
this all-pass run times out without certification. Theorem 2 gives a completeness bound
when responses and human checks can fail, provided local reliability conditions hold and
diagnostic evidence can reach the threshold within T .
     The false-pass bound comes from sampling the complete list and checking against fixed
records. Follow-up questions can direct attention to suspicious entries, but do not automat-
ically inherit the same bound. The anchored construction at the end of Section 4 combines
random checks with adaptive choices while retaining a justified bound.

3.6 Correspondence with Classical Interactive Proofs
A standard IP instantiation requires a formal promise problem, a uniform polynomial-
time verifier, and polynomial communication. Under their stated assumptions, Theorems 1
and 2 give soundness against every adaptive prover on false instances and completeness for
an honest prover satisfying the response bounds on true instances; am = cm = 1 recovers
ideal execution. Corollary 1 gives the full IP conditions.
    To specify these resource bounds, define the input size for a statement s and verifier
information state i as
                                   κ(s, i) := |s| + size(i),
where size(i) is the length of a finite encoding of i. In an IP instantiation, all admissible
messages—the initial statement, challenges, responses, and terminal verdicts—have length
at most a polynomial cap Lmax (κ). Both the horizon T and total verifier computation must
also be polynomial in κ.
     For scheduling, that computation includes selecting constraints, retrieving and com-
paring records, and updating the certificate. The bound q = 1 − 1/J can be justified in
advance, but evaluating and using it during review still counts toward the budget. The
effort and execution-reliability conditions in Section 5 address the additional demands of
human review.
     In the classical three-coloring protocol, the honest prover commits to a randomly re-
labeled coloring each round before the verifier samples an edge and checks the opened
endpoint colors. On a non-three-colorable graph, every assignment violates an edge, giv-
ing uniform sampling a detection bound without requiring the verifier to locate an error
first. The protocol can hide the full coloring, although a revealed coloring is also efficiently
checkable (Vadhan, 2007).
     Appendix C states the additional simulation and prefix-consistency assumptions un-
der which stopping at the certificate threshold preserves HVZK. Section 4 develops the
certificate rule with response and human execution errors.




                                              12
                          Verifiability without Transparency




4 Sequential Certification under Response and Execution Error
An LLM may supply inadequate evidence even for a true statement, and a human may
execute a valid check incorrectly. In the scheduling review, the LLM can supply a correct
time comparison that the organizer then misreads. We distinguish the response, its checking,
and the observed outcome.
Events and probability bounds. At a reached diagnostic round m, the event Am
means that the response is admissible, truthful, checkable, and sufficient to pass a cor-
rectly executed check. The event Em means that the human executes the check correctly.
The observed event Passm means that the implemented check returns Pass, as used by U .
The bounds am and cm are lower bounds on the conditional probabilities of Am and Em ,
respectively; the conditioning histories are specified below.
Information within a round. Before choosing the next challenge, Fm−1 records the
transcript, verifier-observable state, and random bits already used through round m − 1.
The verifier uses only this information to choose the question type, challenge policy, and
ideal false-pass bound qm . Only diagnostic rounds update the certificate; clarification rounds
can guide later challenges.
    After the response ym to challenge xm arrives, Gm adds both messages and all other
observable pre-check state to Fm−1 . We assume Am ∈ Gm : adequacy is determined by this
data, although the verifier may lack an efficient way to decide it. After the check, Fm also
records the observed outcome and updated verifier state.
    For a fixed history hm−1 and question–response pair (xm , ym ), rm    ◦ is the prescribed

checker’s probability of returning Pass when run correctly, including any intended checker
randomness. The bound qm is chosen earlier: on false statements, it upper-bounds this
probability averaged over the challenge policy and adaptive response.
Histories used in the proof. The analysis also tracks whether earlier responses were
adequate and checks were executed correctly; execution errors may be unobserved. After
round m, this augmented history is

                             Jm := σ(Fm , A1 , E1 , . . . , Am , Em ) ,                      (1)

For the check in round m, combine the augmented history through round m − 1 with the
current question and response:
                                 Km := Jm−1 ∨ Gm .                               (2)
Here σ(·) denotes the information generated by its arguments, and ∨ combines two infor-
mation fields. The four histories serve the following roles:
        Stage in round m                          Observable history      Analysis history
        Before choosing the challenge                   Fm−1                  Jm−1
        After the response, before checking              Gm                    Km
Challenge selection and the choice of qm use the observable history Fm−1 available before the
round. We require the reliability bounds to hold conditional on the relevant augmented his-
tories, including earlier response and execution outcomes. These conditional requirements
allow dependence across rounds.

                                                13
                                 Zhang, Foster, and Sedoc




Condition 1 (Response reliability of the honest prover) Fix a true statement s ∈
L, information state i ∈ I, and horizon T . Fix numerical lower bounds am ∈ [0, 1] before
execution. A possibly stochastic honest prover P H is response-reliable if its initial response
is admissible almost surely and the following bound holds after every covered history at each
reached diagnostic round:
                                   s,P H
                                    Pr (Am | Jm−1 ) ≥ am .
The inequality must hold after every covered past history, including earlier response and
execution outcomes; the probability averages over the current challenge and prover random-
ness. On clarification rounds, Am occurs surely by convention; the fixed sequence am is
unchanged. The honest prover’s clarification responses are admissible almost surely, while
diagnostic responses may be inadequate with positive probability. The initial and clarification
responses therefore cannot cause rejection for malformed or over-length messages.

4.1 Effective Verifier and Certificate Rule
We combine the diagnostic bound qm with the execution bound cm to obtain the imple-
mented false-pass bound and specify how passed checks accumulate certification evidence.
The conditions below apply to a fixed task and verifier information state, with prescribed
challenge and checking policies executable within the verifier’s resources. Comparisons
between interfaces require separate justification of these conditions for each implemented
policy and its actual prover responses; an effort–load model alone does not establish them.

Assumption 1 (Effective Verifier) Fix target soundness δ ∈ (0, 1) and horizon T . The
execution lower-bound sequence (cm )Tm=1 is deterministic and fixed before execution. At
each reached diagnostic round m ≤ T , the bound cm ∈ [0, 1] must hold after every covered
history. The verifier also uses an Fm−1 -measurable diagnostic bound qm ∈ [0, 1]. Define

                           q̄m := 1 − cm (1 − qm ),     0 < q̄m < 1.                       (3)

The following conditions hold.

  1. Human execution reliability. Under every execution law covered by the results
     below (every false statement with every adaptive prover, and the true statement with
     the honest prover covered by the completeness bound), every reachable full pre-check
     history satisfies
                                                                               ◦
                 Pr(Em | Km ) ≥ cm ,       Pr(Em ∩ Passm | Km ) = Pr(Em | Km )rm .

     By iterated expectation, the same lower bound holds conditional on Gm or Fm−1 .

  2. False-statement validity under correct execution. For every false statement
      / L, every adaptive admissible prover P ∗ , and every reachable active history,
     s∈
                                           ∗  ◦
                                       Es,P [rm | Fm−1 ] ≤ qm .

     This probability assumes that the prescribed check is executed correctly. Given the
     preceding observable history, it averages over the current challenge, the adaptive prover

                                               14
                          Verifiability without Transparency




     response, and the checker’s intended randomness. The bound applies to the challenge
     policy as a whole; it need not hold separately for every realized question. Challenges
     may be nonuniform and history-adaptive, provided the conditional bound remains valid
     at every reachable active history.

  3. True-statement correctness. For every s ∈ L and response-reliable honest prover
     P H satisfying Condition 1,
                                 Am ∩ Em =⇒ Passm
     on every reached diagnostic round.

  4. Certification process and verdict. Set M0 := 1 before receiving any prover mes-
                                                     ◦ = 1 and let A , E , and Pass
     sage. On a clarification round, set qm = q̄m = rm               m    m         m
     occur surely by convention. Keep the deterministic lower bounds am , cm unchanged
     and leave Mm = Mm−1 . On an active diagnostic round, update
                                                    1{Passm }
                                      Mm = Mm−1               .                            (4)
                                                      q̄m
     A failed diagnostic check therefore sets Mm = 0 and causes immediate Reject. For
     every reached post-challenge history,
                           
                           Reject,
                                         the diagnostic check fails,
               U (hm , i) = Accept,       the check does not fail and Mm ≥ 1/δ,
                           
                             Challenge, otherwise.
                           

     If the last case occurs at m = T , the protocol outputs Reject. After termination, Mm
     is held constant under the padding convention.

  5. Reaching the threshold on an honest run. There exists a deterministic K ≤
     T such that, on every honest execution in which the first K reached responses are
     adequate and their checks are correctly executed, either the protocol has accepted earlier
     or
                                    XK
                                         − log q̄m ≥ log(1/δ).                              (5)
                                     m=1

    A passed diagnostic check multiplies Mm by 1/q̄m , so its contribution to the accumulated
log evidence is
                                      gm := − log q̄m .
For fixed qm , a larger execution-reliability bound cm lowers q̄m and increases this contri-
bution. The process Mm measures evidence against a false claim; it is not a posterior
probability that the claim is true.
    Clarification leaves Mm unchanged, although it may improve understanding or guide
later challenges. In the scheduling review, asking the LLM to explain an entry can help the
organizer decide what to inspect next. Checking the selected constraint against the fixed
records supplies the diagnostic outcome: a pass earns gm units of log evidence under the
stated bounds, while a failure causes rejection.

                                             15
                                  Zhang, Foster, and Sedoc




    The two guarantees use these conditions differently. Soundness combines execution
reliability, false-statement validity, and the certificate rule (items 1, 2, and 4), without
requiring adequate responses from the prover. Completeness also requires adequate honest
responses under Condition 1, true-statement correctness, and enough diagnostic progress
to reach the threshold. Thus cm enters both guarantees, while am enters the completeness
bound through the chance of obtaining adequate evidence for a true claim.

4.2 Anytime-Valid Soundness
The following result applies the standard test-supermartingale argument to the implemented
false-pass bounds.
Theorem 1 (Anytime-valid soundness) Suppose items 1, 2, and 4 of Assumption 1
hold, with the bounds specified there. For every s ∈
                                                   / L and every adaptive admissible prover
strategy P ∗ ,
                                 s,P ∗
                                 Pr (∃m ≤ T : Mm ≥ 1/δ) ≤ δ.                               (6)
Consequently,
                                          s,P ∗
                                    sup Pr (Ω = Accept) ≤ δ.
                                     P∗
The bound holds uniformly over all prefixes and all stopping times adapted to the execution
history, provided formal acceptance still requires Mm ≥ 1/δ.
Proof Using the worst-case convention that an incorrectly executed check may pass,
                     Pr(Failm | Fm−1 ) ≥ Pr(Em ∩ Failm | Fm−1 )
                                                                  ◦
                                            = E[Pr(Em | Km )(1 − rm )|Fm−1 ]
                                                        ◦
                                            ≥ cm E[1 − rm | Fm−1 ]
                                            ≥ cm (1 − qm ).
Hence Pr(Passm | Fm−1 ) ≤ 1 − cm (1 − qm ) = q̄m . Therefore
                                     E[Mm | Fm−1 ] ≤ Mm−1 ,
so (Mm )Tm=0 is a nonnegative supermartingale. Ville’s inequality (Shafer et al., 2011; Ram-
das et al., 2023) now yields
                                                !
                            Pr       sup Mm ≥ 1/δ         ≤ δM0 = δ.
                                   0≤m≤T

Formal acceptance is a subset of this crossing event, proving the result. The argument is
pointwise in P ∗ , so the outer supremum is valid.


    One threshold, fixed before interaction, controls the probability of ever accepting a false
statement across the full horizon.
    The one-round bound q̄m used in the proof is attained when correct execution has
probability cm at every full pre-check history, the correct checker’s conditional average pass
probability equals qm , and incorrect execution always passes.

                                                  16
                           Verifiability without Transparency




4.3 Finite-Horizon Completeness
Theorem 2 (Finite-horizon completeness) For a true statement s ∈ L, suppose As-
sumption 1 and Condition 1 hold with a response-reliable honest prover P H and a round
bound K ≤ T satisfying the progress condition. Then

                                s,P H                       K
                                                            Y
                                 Pr (Ω = Accept) ≥               am cm .                     (7)
                                                           m=1
                    QK
In particular, if    m=1 am cm ≥ 1 − γ, then the protocol has completeness at least 1 − γ.

Proof Let H0 denote the whole sample space and Hk := km=1 (Am ∩ Em ). After early
                                                           T
acceptance, declare all unused adequacy and execution events true; after rejection, declare
them false. Extend the information fields by the corresponding terminal records, so these
events remain measurable. For k ≤ K, on Hk−1 the protocol is either active or has already
accepted: adequate responses and correctly executed checks prevent diagnostic rejection,
and timeout cannot precede k. On the active part of Hk−1 , Ak is Kk -measurable, so the
response and execution bounds give

        Pr(Ak ∩ Ek | Jk−1 ) = E[1Ak Pr(Ek | Kk ) | Jk−1 ] ≥ ck Pr(Ak | Jk−1 ) ≥ ak ck .

On the already-accepted part of Hk−1 , the conditional probability is one by convention, so
the same lower bound holds. No reliability condition is needed on previously rejected paths.
Because Hk−1 ∈ Jk−1 , the conditional chain rule yields, without independence,
                                                               
                         Pr(Hk ) = E 1Hk−1 Pr(Ak ∩ Ek | Jk−1 )
                                        ≥ ak ck Pr(Hk−1 ),

and hence
                                                     K
                                                     Y
                                         Pr(HK ) ≥         am cm .
                                                     m=1

   On HK , response adequacy and correct execution prevent a diagnostic failure. By the
progress condition, the protocol either accepts before K or accumulates
                                             K
                                             X
                              log MK =            − log q̄m ≥ log(1/δ).
                                            m=1

Thus MK ≥ 1/δ, and the protocol accepts no later than round K. Therefore HK ⊆ {Ω =
Accept}, which proves (7).


   Timeout Reject is included in the failure probability. On HK , the threshold is reached by
K ≤ T ; outside HK , the proof conservatively allows an inadequate LLM response or a human
execution error to cause false rejection, insufficient gain, or timeout. No independence
between the two agents’ errors or between rounds is assumed in either theorem.



                                                   17
                               Zhang, Foster, and Sedoc




Ideal execution as a special case. Under the same local validity and progress condi-
tions, setting am = cm = 1 for every m ≤ T makes response adequacy and correct execution
hold almost surely at all reached  rounds. Then q̄m = qm , each passed diagnostic check mul-
tiplies Mm by 1/qm , and K
                           Q
                             m=1 m cm = 1. Theorems 1 and 2 therefore give soundness at
                                  a
level δ and acceptance by K ≤ T with probability one for the true statement and honest
prover covered by the bounds.

Corollary 1 (Conditional IP instantiation) Write i = (ipub , ipriv ) and let x = ⟨s, ipub ⟩
define a promise problem (Y, N ), with verifier-only state fixed or uniformly generated by
V . Suppose V (1κ , x) is uniform probabilistic polynomial time, while T (κ), communication,
and parameter representations are polynomially bounded. If the preceding hypotheses hold
uniformly and, for some polynomial p,
                                   K
                                   Y                   1
                                        am cm − δ ≥        ,
                                                      p(κ)
                                  m=1

then the instantiation is an interactive proof with completeness at least K
                                                                         Q
                                                                            m=1 am cm and
soundness at most δ against every unbounded admissible prover; polynomial-time prover
soundness instead gives an interactive argument. Standard amplification yields the conven-
tional 2/3–1/3 parameters.

   An actual human requires separate formalization as a uniform probabilistic polynomial-
time verifier.
An anchored challenge construction. The soundness theorem requires a justified false-
pass bound but does not prescribe a challenge policy. One way to retain such a bound is
to choose, before round m, a probability λancm of using a reference check. Under correct
execution, this check must detect a false claim with probability at least ρm against every
admissible adaptive prover at every covered history. The remaining diagnostic challenges
may follow the dialogue. Even if those challenges contribute no guaranteed detection, the
full mixture supports

                        qm = 1 − λanc
                                  m ρm ,          q̄m = 1 − cm λanc
                                                                m ρm .

The mixing probability is chosen from the preceding history before the round; these bounds
apply to the whole randomized policy. In the scheduling example, fresh uniform sampling
from the fixed complete list of J constraints supplies ρm = 1/J. The organizer can there-
fore pursue apparent conflicts while retaining this random-check component. Appendix D
gives the formal conditions and proof. This construction supplies a local diagnostic bound;
completeness still requires the response, execution, and progress conditions above.
    Together, the two certification theorems require enough diagnostic evidence to control
false acceptance and enough response and execution reliability to preserve true acceptance
before timeout. Section 5 turns these joint requirements into a set of review lengths that
meet both targets when chosen before execution, then examines how effort, cognitive load,
and expertise affect execution reliability and certification.



                                             18
                          Verifiability without Transparency




5 Certification under Fixed Bounds
For a fixed sequence of bounds, more passed checks tighten the false-acceptance bound but
can weaken the true-acceptance guarantee by adding opportunities for inadequate responses
and execution errors. We seek review lengths that certify both targets within the verifier’s
horizon.
     Fix the rules for choosing challenges and checking responses over T rounds, and denote
this process by KT . We specify when it stops separately. Here the numerical bounds are
fixed before execution. Challenges may still be sampled randomly or selected from earlier
dialogue, and responses may be stochastic.
     The primary protocol ΠES rejects at the first failed check and accepts when the evidence
first reaches the threshold. Each protocol Π(n) fixes its review length n ≤ T in advance,
rejects on any failed check, and accepts only after all n checks pass. These protocols compare
different review lengths using the same challenge and checking rules. In the scheduling
example, the timetable and constraint list stay fixed as the review length varies.
     Assume that Condition 1 and the local execution, validity, and correctness conditions in
items 1–3 of Assumption 1 hold for KT with deterministic bounds (ai , ci )Ti=1 and a uniform
ideal false-pass bound q ∈ [0, 1). These bounds must hold uniformly on every prefix reach-
able under each protocol being evaluated. We use the stopping rules specified above and
determine below whether the threshold can be reached within T . Every scheduled round in
this specialization is diagnostic; clarification can instead be represented by a round-specific
bound equal to one, but is omitted here. For round i, define

                             q̄i := 1 − ci (1 − q),   0 < q̄i < 1,                          (8)

where ai lower-bounds adequate honest-prover response on a true statement and ci lower-
bounds correct human execution. Define the false-acceptance upper bound and true-
acceptance lower bound
                                  n
                                  Y               Yn
                           Rn :=     q̄i ,  Cn :=     ai ci .                       (9)
                                      i=1               i=1

For the fixed-length protocol Π(n) , Rn upper-bounds false acceptance and Cn lower-bounds
true acceptance under the stated conditions. For early stopping, we evaluate these bounds
at the first round that reaches the acceptance threshold when every check has passed,

                                Kδ := min{n ≤ T : Rn ≤ δ},                                 (10)

when the set is nonempty. If no such round exists, acceptance is impossible and the primary
protocol rejects by T .

Definition 7 ((δ, γ)-certification) For target errors δ, γ ∈ (0, 1), a protocol Π with a
prespecified stopping rule is soundness-certified at level δ if, for every false statement s− ∈
                                                                                              /L
and every adaptive admissible prover P ∗ ,
                                   s− ,P ∗
                                     Pr (Ω = Accept) ≤ δ.
                                     Π




                                                19
                                 Zhang, Foster, and Sedoc




For a fixed true statement s+ ∈ L and honest prover P H to which the stated lower bounds
apply, it is completeness-certified at level 1 − γ if
                                     s+ ,P H
                                          Pr (Ω = Reject) ≤ γ.
                                          Π

It is (δ, γ)-certified for that true statement and honest prover if both conditions hold. The
rejection probability includes detected failures and timeout rejection.

Proposition 1 (Deterministic early-stopping certificate) If Kδ is defined, then for
every s− ∈/ L, every adaptive admissible prover P ∗ , and every true statement and honest
prover (s+ , P H ) covered by the bounds,
                                s− ,P ∗
                                 Pr (Ω = Accept) ≤ RKδ ≤ δ,                               (11)
                                 ΠES
                                s+ ,P H
                                  Pr (Ω = Reject) ≤ 1 − CKδ .                             (12)
                                 ΠES

Consequently, ΠES is (δ, γ)-certified whenever
                                              CKδ ≥ 1 − γ.                                (13)

Proof The conditional false-pass probability at reached round i is at most q̄i . Acceptance
requires survival through
                    Ti    Kδ , so the conditional chain rule gives the first bound. For the
true pair, let Si := j=1 Passj . The response and execution conditions in Section 4 imply
                        Pr(Passi | Fi−1 ) ≥ Pr(Ai ∩ Ei | Fi−1 ) ≥ ai ci .
The final inequality follows by first conditioning on the augmented fields Ji−1 and Ki and
then applying iterated expectation back to the observable field Fi−1 . Because Si−1 ∈ Fi−1 ,
iteration gives Pr(SKδ ) ≥ CKδ without an independence assumption. All-pass survival
through Kδ forces acceptance, proving the second bound.


Definition 8 (Certifiable effective region) For the fixed process KT , define the review
lengths that meet both certification targets
                    ERδ,γ := {n ∈ {1, . . . , T } : Rn ≤ δ and Cn ≥ 1 − γ} .              (14)
When this set is nonempty, write nmin := min ERδ,γ and nmax := max ERδ,γ .

   This set contains exactly the lengths that meet both product criteria. A design outside
the set may still meet the actual error targets; these bounds do not certify it.

Proposition 2 (Effective-region characterization) If ERδ,γ is nonempty, then
                    ERδ,γ = {nmin , nmin + 1, . . . , nmax },    nmin = Kδ .              (15)
Every fixed-length protocol Π(n) with n ∈ ERδ,γ is (δ, γ)-certified. The primary early-stopping
protocol accepts on an all-pass path at the unique first crossing Kδ = nmin . The right
endpoint is the longest review that can be chosen in advance while meeting both targets.

                                                   20
                          Verifiability without Transparency




Proof Because q̄i , ai , ci ∈ [0, 1], both Rn and Cn are nonincreasing. Hence {n : Rn ≤ δ} is
a suffix beginning at Kδ , while {n : Cn ≥ 1 − γ} is a prefix; their intersection is the integer
interval in (15). For Π(n) , the validity assumption for all reachable histories and conditional
chain rule bound false acceptance by Rn ≤ δ; the same observable all-pass argument as in
Proposition 1 lower-bounds true acceptance by Cn ≥ 1 − γ. The early-stopping statement
follows from the definition of Kδ .


   An additive condition is also useful for illustrating effort
                                                             P allocation. The next corollary
obtains it by upper-bounding the product Rn in terms of ni=1 ci .

Corollary 2 (Additive sufficient effective region) The more conservative set
                                      n
                    (                                               )
                                     X
            ERsuf
              δ,γ := n ≤ T : (1 − q)    ci ≥ log(1/δ) and Cn ≥ 1 − γ .                     (16)
                                            i=1

is an inner approximation to the exact effective region: ERsuf
                                                            δ,γ ⊆ ERδ,γ . It is an integer
interval whenever nonempty, and every member certifies both Π(n) and the primary protocol
ΠES .

Proof
                             n                                     n
                                                                              !
                             Y                                    X
                      Rn =         1 − ci (1 − q) ≤ exp −(1 − q)         ci       ,        (17)
                             i=1                                   i=1
The additive inequality therefore implies Rn ≤ δ. Its left-hand side is nondecreasing and
Cn is nonincreasing, so the set is an integer interval. Finally, any member has Kδ ≤ n and
CKδ ≥ Cn ≥ 1 − γ, which certifies ΠES as well.


    Appendix E applies these product bounds to a matrix-product check with a nonempty
certifiable region and a scheduling review whose required number of checks exceeds its
budget.

5.1 Effort, Cognitive Load, and Expertise
Cognitive load describes the understanding, memory, and integration required to execute
a prescribed check, including its preceding context. It is distinct from the prover’s search
time and may depend on how evidence is presented.
    Let E be the common total human-review budget. The effort ei ≥ 0 for local round
i includes all work needed to prepare, perform, and interpret its check;   eos ≥ 0 is defined
analogously for the global check. All effort is counted once, with ni=1 ei ≤ E and eos ≤
                                                                     P
E. The designs must also meet common computation and communication caps, and their
execution bounds must cover all operations not performed by trusted procedures.
    Let ξι ≥ 0 summarize task-relevant expertise and tool access, and let λi ≥ 0 denote a
round’s cognitive load, including required context. Fix each design’s loads before execution.
We use the parameterization
                                                              
                                                         λi
                                ci = f (ei , ξι ) exp −          .                       (18)
                                                        r(ξι )

                                                  21
                                 Zhang, Foster, and Sedoc




Figure 2: Additive sufficient effective region for one fixed bound sequence. Left: the sound-
          ness criterion gives the minimum number of checks. Right: the completeness
          criterion gives the maximum. Their overlap (shaded) is ERsuf  δ,γ = {3, . . . , 11}, for
          T = 14, q = 0.20, δ = 0.10, γ = 0.20, ai = 1, and ci = 0.985 − 0.001(i − 1).
          Each shaded length is a review that can be chosen before execution. The primary
          protocol stops at Kδ using the exact product criterion, which may require fewer
          checks than the additive condition shown here.


Here f ∈ [0, 1] is weakly increasing in effort and expertise, and the positive scale r is weakly
increasing in expertise. The exponential factor represents a load penalty, not computational
running time. The resulting execution bounds must satisfy Assumption 1, including after
actual adversarial responses. A diagnostic bound q requires its own justification.
    The preceding protocols take the first rounds of the same fixed checking process. We now
allow each candidate length its own effort allocation, chosen in advance, and corresponding
                    (n) (n)                                (n)
justified bounds ai , ci . Equal allocation gives ei = E/n. Among candidate lengths
feasible within the common budgets, define
                                (                     Pn (n)                 )
                                            (1  − q)         c   ≥ log(1/δ),
                   ERsuf
                      δ,γ (E) := n ≤ T : Qn
                                                        i=1 i
                                                     (n) (n)                   .            (19)
                                                   a
                                               i=1 i    ci     ≥1−γ

Under equal allocation, holding all other design parameters fixed, increasing E preserves
certification because f is nondecreasing. Each allocation requires its own crossing calcu-
lation. At fixed E, the feasible lengths need not form an interval. Figure 3 illustrates
contiguous sets under its chosen parameterization; Appendix B gives the specification.

5.2 Conditional Advantage of Decomposition
For each task, we compare the designs on the same fixed claim, candidate answer, and
source records. Both have the same verifier tools and capabilities and must satisfy the
common budgets above. A global checker may perform any internal operations specified by


                                               22
                              Verifiability without Transparency




                                                                          (n)
Figure 3: Effort and the sufficient effective region with ei = E/n. Left: lower and
          upper certified lengths. Right: number of certified lengths. Dots mark E ∈
          {20, 25, . . . , 180}; steps connect the evaluated budgets and do not identify where
          changes occur between them. In this example, certified lengths are consecutive in
          n, and increasing E retains all previously certified lengths. Here T = 14, q = 0.20,
                                    (n)
          δ = 0.10, γ = 0.20, ai = 1, and ξι = 10; Appendix B gives the full specification.



its algorithm; its ideal false-pass bound qos is justified separately from the local bound q.
A complete exact check can have qos = 0.
    The ideal diagnostic bound concerns correct execution. For a long proof, the reading and
cross-step integration required by a complete check may exceed the human verifier’s budget
or make a strong execution bound difficult to justify. Local challenges allocate review effort
to selected checks; the diagnostic, response, and execution bounds of the resulting policy
determine whether the fixed claim can be certified.
    Under (18), let
                                                                                n
                                                                                X
                                                −λos /r(ξι )
                        cos := f (eos , ξι )e                  ,   ∆ := λos −         λi .
                                                                                i=1

For positive f -terms, the comparison of execution lower bounds becomes
                         Qn          Qn
                             i=1 ci       f (ei , ξι ) ∆/r(ξι )
                                    = i=1             e         ,
                             cos      f (eos , ξι )
                       n                                                                     (20)
                      Y                                           f (eos , ξι )
                          ci > cos ⇐⇒ ∆ > r(ξι ) log Qn                            .
                        i=1                                       i=1 f (ei , ξι )

With equal allocation, ei = E/n and eos = E, this threshold is nonnegative. The sign and
magnitude of ∆ require support from the cognitive demands of the compared implementa-
tions.
Q        For a global response-adequacy bound aos > 0, multiplying the execution ratio by
   i ai /aos gives the ratio of true-acceptance lower bounds. The proposition below combines
these response and execution bounds with each design’s diagnostic guarantee.

                                                         23
                                 Zhang, Foster, and Sedoc




Proposition 3 (Conditional certification advantage) Fix (δ, γ) ∈ (0, 1)2 and com-
mon review, computation, and communication budgets. Suppose a resource-feasible local
design with 2 ≤ n ≤ T satisfies the conditions of this section with bounds (ai , ci ) and q.
Suppose a resource-feasible global checker satisfies the analogous response, execution, and
diagnostic conditions, with independently justified bounds aos ∈ (0, 1], cos ∈ (0, 1], and
qos ∈ [0, 1), and accepts exactly when its check passes. Define

                          Ros := 1 − cos (1 − qos ),          Cos := aos cos .

Both the fixed-length local protocol and the protocol that accepts at the first threshold crossing
are certified for both targets if

                                   Rn ≤ δ,       Cn ≥ 1 − γ.                                 (21)

The global bounds certify both targets when Ros ≤ δ and Cos ≥ 1 − γ. Under the execution
model, soundness certification at a nonnegative load requires (1 − qos )f (eos , ξι ) ≥ 1 − δ and
holds exactly when
                                               (1 − qos )f (eos , ξι )
                              λos ≤ r(ξι ) log                         .                      (22)
                                                     1−δ
    In particular, for ai ≥ a > 0, λi ≤ λ0 , and equal round efforts e1 = · · · = en , let

                             cn := f (e1 , ξι )e−λ0 /r(ξι ) ,
                                          (                       )
                                             1 − δ 1/n (1 − γ)1/n                            (23)
                             τn := max                 ,            .
                                               1−q            a

The sufficient test cn ≥ τn implies (21). It holds exactly when f (e1 , ξι ) ≥ τn and

                                                       f (e1 , ξι )
                                    λ0 ≤ r(ξι ) log                 .
                                                           τn
If the local criteria hold while Ros > δ or Cos < 1 − γ, these bounds establish a conditional
certification advantage over the specified global design.

    Even a global check that detects every error when executed correctly can be difficult
for a human to carry out reliably. Dividing the review into smaller checks can reduce the
cognitive load of each step, while repeated diagnostic checks accumulate evidence about the
same claim. This benefit has a cost: the fixed effort budget is spread across rounds, and
every additional round requires another adequate response and correctly executed check.
Under the same budgets, these conditions can guarantee the required reliability for the local
review while leaving the global check without such a guarantee.
    The two terms in τn make this tradeoff explicit. One requires enough diagnostic strength
to control false acceptance; the other requires enough response and execution reliability to
accept true claims.
Proof The conditional-product argument gives false acceptance at most Rn and true
acceptance at least Cn . If (21) holds, Kδ ≤ n and CKδ ≥ Cn , so Proposition 1 also certifies
the primary protocol under the same fixed allocation. The one-check argument gives Ros
and Cos , including a zero false-pass bound for an ideally exact, perfectly executed check.

                                                24
                           Verifiability without Transparency




Substituting the execution model into cos (1 − qos ) ≥ 1 − δ yields (22) and its feasibility
condition.
   Using the common lower bound, ci ≥ cn implies

                            Rn ≤ [1 − cn (1 − q)]n ,     Cn ≥ (acn )n .

The right-hand sides meet their targets exactly when cn ≥ τn . Substitution gives the load
threshold. All probability bounds use conditional expectations; independence is unneces-
sary.


   Failure of the global certificate does not show that its actual error rate is higher or that
every global design fails. If a global check uses the same acceptance threshold with horizon
one and Ros > δ, it cannot reach that threshold and must reject.
Comparison with an exact global checker. Table 1 compares the two designs in
the fixed matrix-product example of Appendix E.3. The global checker directly multiplies
the matrices (qos = 0), while the interactive design performs five independently checked
Freivalds challenges (q = 1/2). Both receive E = 120: the global check uses eos = 120, and
each local round uses ei = 24. The interactive design first crosses the threshold at round five
and meets both targets; the global bound exceeds δ. The additive criterion remains more
conservative: its diagnostic sum is 2.478731 < log 20, so it does not certify this interactive
design.

             Design              False-accept bound    True-accept bound   Certified?
             Global                        0.061875             0.938125   No
             Interactive local             0.032602             0.911219   Yes

Table 1: Conditional comparison at E = 120, δ = 0.05, and γ = 0.10, with common tools
         and resource caps.


    The comparison depends on the execution conditions. Reducing only the assumed global
load from λos = 0.20 to 0.10 gives Ros = 0.033856 and Cos = 0.966144, satisfying both
criteria. Appendix E.3 gives the parameters and calculations.

6 Empirical Simulation
We use LLM-only simulations to examine whether challenge–response dialogue helps a ver-
ifier select more accurate answers. In Prover–Verifier Deliberation (PVD), an LLM prover
gives an answer and a set of checkable subclaims. A second LLM takes the verifier’s role,
accepting, rejecting, or challenging the weakest part of the transcript. Both models remain
fixed throughout the exchange; the prover can respond to challenges by supplying support
or revising its answer.
     When the verifier accepts and the prover has never changed its answer, we label the
attempt Accept + No Change (ANC). The supporting argument may still be elaborated or
revised. Rejected attempts and attempts accepted after an answer change are non-ANC.


                                                25
                               Zhang, Foster, and Sedoc




Table 2: GPQA Diamond PVD simulations (N = 198 per pair). ANC and non-ANC ac-
         curacies are percentages, with subgroup sizes n in parentheses. Gap is their dif-
         ference in percentage points, with a two-sided 95% percentile-bootstrap interval
         from 10,000 non-stratified question-level resamples (seed 42). Flash-Lite denotes
         Gemini 3.1 Flash-Lite.
                                          ANC         non-ANC
Prover              Verifier            Acc. (n)      Acc. (n)          Gap (95% CI)
Sonnet 4.6          Haiku 4.5           93.5 (108)     51.1 (90)      +42.4 [+31.0, +53.5]
GPT-5.4             GPT-5.4-mini         97.6 (85)    62.8 (113)      +34.8 [+25.5, +44.3]
Gemini 3.1 Pro      Flash-Lite          97.3 (112)     90.7 (86)       +6.6 [−0.1, +13.7]


Comparing the correctness of these two groups tests whether stable acceptance is a useful
signal of answer quality; Section 6.1 defines the ANC gap used below.
    GPQA Diamond1 lets us compare this signal across model pairs. We then test whether
verifiers reject deliberately wrong defenses and examine ANC on the more difficult Human-
ity’s Last Exam (HLE) tasks.2 The GPQA and HLE results draw on Sedoc et al. (2026); the
two deceptive-prover stress tests were conducted for this paper. These simulations examine
dialogue behavior and answer selection, without validating the human-verifier assumptions
or the theoretical certification guarantees.

6.1 Empirical Proxy
For a labeled dataset, we compare accuracy within the ANC and non-ANC groups:

                     Gap = Pr[correct | ANC] − Pr[correct | ¬ANC].

A positive gap means that ANC selects more accurate answers on the evaluated tasks; a
zero or negative gap means that it does not. Computing the gap requires correctness labels
as well as recorded verdicts and answer changes. It measures the quality of the selected
answers, rather than improvement in a given answer through revision.

6.2 GPQA Diamond
Table 2 reports PVD results for three prover–verifier pairs from Sedoc et al. (2026), each
evaluated on all 198 GPQA Diamond questions with one attempt per question. The model
pairs were chosen for the study without selection on their observed ANC gaps. The Son-
net/Haiku row uses the standard protocol rerun, while the GPT and Gemini rows use the
earlier cross-model runs. We compute the same ANC and non-ANC accuracies from the
recorded verdicts and answer changes in each run.
    The Sonnet/Haiku and GPT pairings show large positive ANC gaps. The Gemini pairing
has high accuracy in both subsets and a smaller gap whose interval includes zero. Thus,
high ANC accuracy alone does not establish that stable acceptance separates better answers
from the remaining cases. These runs describe the signal for the tested pairings; they do
not isolate the effect of changing a model under a common experimental configuration.
1. https://github.com/idavidrein/gpqa
2. https://www.lastexam.ai/


                                             26
                             Verifiability without Transparency




Table 3: Deceptive-prover stress tests conducted for this paper on GPQA Diamond (N =
         198 planned cases per condition, fatigue limit T = 12). Fool rate: fraction
         of planned cases in which the verifier accepted the deliberately wrong answer.
         Changed to correct answer: fraction with an observed switch to the true
         option. Three naı̈ve and one strategic cases ended after all three prover-response
         JSON parsing attempts failed; the operational protocol counted these cases as
         rejections.

Condition                       Fool rate        Rejected          Changed to correct answer
Naı̈ve deceptive prover       12/198 (6.1%)   186/198 (93.9%)            0/198 (0.0%)
Strategic deceptive prover    18/198 (9.1%)   180/198 (90.9%)            0/198 (0.0%)


    A separate single-call self-deliberation rerun uses one Sonnet 4.6 response containing
alternating prover and verifier blocks on the same 198 questions. Its ANC gap is +18.6
points (95% CI: +6.2 to +31.3), compared with +42.4 for the standard Sonnet/Haiku rerun.
The single-call prompt allows six rounds and requires an initial challenge3 ; the standard
rerun allows twelve rounds and permits immediate acceptance. Differences in verifier model
and protocol settings prevent attributing the gap difference to call structure alone.

6.3 Deceptive-Prover Stress Test
Soundness asks what happens when the statement under defense is false. We run two GPQA
Diamond stress tests in which the prover receives the correct answer but is instructed to
defend a wrong option. In the naı̈ve condition, the prover selects a plausible wrong answer
and argues for it. In the strategic condition, it is additionally told that the verifier is a
smaller model and that it should maintain a convincing defense.
    Both conditions use Sonnet 4.6 as prover and an unchanged Haiku 4.5 verifier that is
unaware of the manipulation. Each condition includes all 198 questions with fatigue limit
T = 12. These tests examine two specified deceptive strategies, while the formal soundness
guarantee covers every admissible adaptive prover P ∗ . Table 3 reports the outcomes.
    The operational rule rejects 186/198 (93.9%) naı̈ve and 180/198 (90.9%) strategic cases.
Every accepted case retains the original wrong answer with zero recorded answer changes,
so all 12 naı̈ve accepts and all 18 strategic accepts are ANC cases with wrong final answers.
The strategic run’s fool rate is 3.0 percentage points higher, but an exact paired McNemar
test does not distinguish the conditions (p = 0.307); with one stochastic run per condition,
the comparison does not identify a prompt effect.
    These results show that most deliberately wrong defenses are rejected under the tested
interventions, while some still achieve ANC. The observed rates depend on how the wrong
answer is constructed and on the model pair, parsing policy, and challenge policy. Be-
cause the LLM verifier’s diagnostic and execution bounds remain unverified, these rates do
not establish formal soundness and are not estimates of the single-round q parameter in
Section 5.
3. One response accepted without the required challenge; we count it as ANC because the answer was
   unchanged.




                                               27
                               Zhang, Foster, and Sedoc




Table 4: PVD simulations on the same HLE multiple-choice subset (N = 513 per pair).
         Acc.: overall accuracy. Gap: ANC minus non-ANC accuracy in percentage
         points, with 95% intervals computed as in Table 2. The Opus/Sonnet records
         omit answer changes, so its ANC gap cannot be computed.

Prover                  Verifier                     Acc.                  Gap (95% CI)
Sonnet 4.6              Haiku 4.5                    20.1%                −7.1 [−13.9, +0.1]
Opus 4.6                Sonnet 4.6                   40.0%                       —
GPT-5.5                 Gemini 3.1 Pro               45.6%               +27.9 [+19.6, +36.3]


6.4 HLE
The HLE runs use the same 513 multiple-choice questions for all three prover–verifier pairs.
Table 4 reports overall accuracy and, where answer-change records are available, the ANC
gap. The Sonnet/Haiku point estimate is negative, although its interval includes zero; the
GPT/Gemini pairing has a positive gap.
    For the Sonnet/Haiku pairing, accepted unchanged answers are less accurate than the
remaining answers in this run. One possible explanation is that the verifier lacks the knowl-
edge or tools to check difficult claims and challenges only those it partly understands. In
the model of Section 5, such limitations can mean a lower execution bound ci or a higher
ideal false-pass bound q, leaving no certifiable review length. The observed gap does not
identify either bound.

6.5 Interpretation and Limitations
On GPQA, answers accepted without revision are more accurate for some tested model
pairs. Most deliberately wrong answers in the stress tests are rejected, though some are
accepted unchanged. On HLE, the Sonnet/Haiku pair instead has a negative ANC gap.
These results show when ANC selects more accurate answers in the tested runs; they do
not validate the certification theorems.
    To investigate this variation, a study could record the selected challenges, supplied
evidence, and executed checks. These records would help distinguish a question that misses
the error from missing evidence or an incorrectly performed check. Section 7.3 proposes
such measurements for human review.

7 Discussion
Dividing verification into smaller checks can make each step easier for a bounded verifier to
execute. Each additional round, however, requires another adequate response and reliable
check. The certifiable region identifies review lengths for which the supplied bounds ensure
both enough evidence against false claims and a sufficiently high probability of accepting
true ones.




                                             28
                         Verifiability without Transparency




7.1 When Interaction Helps
A user may be able to check a particular inference, source record, or calculation even when
producing the full argument is beyond their resources. Interaction lets the user request the
supporting material needed for that check and use the result to decide what to examine next.
Its potential value lies in making the work of verification manageable: selecting a useful
question, locating the relevant evidence, and carrying out the check must all fit within the
user’s budget.
    Proposition 3 gives conditions under which reducing the load of each check compensates
for spreading effort across rounds and introducing additional opportunities for error. Under
common budgets, the bounds for local review can meet both acceptance targets. For the
specified global checker, the upper bound on false acceptance may still be too high, or the
lower bound on true acceptance too low. An ideally exact global check can therefore be
less useful for certification if the human cannot execute it reliably enough. The comparison
concerns these specified implementations; whether dialogue offers an additional benefit over
a static presentation of the same local evidence calls for a separate comparison.
    The primary protocol accepts at the first threshold crossing, avoiding further checks
once the evidence requirement has been met. If reaching that threshold requires more
reliable work than the budget supports, a useful response is to improve the checks, their
presentation, or the available tools. Simply extending the dialogue need not produce a
certifiable review.

7.2 Designing Checks for Bounded Verifiers
In the scheduling example, the organizer starts by selecting a constraint that bears on the
claim that the schedule has no conflicts. Comparing Lee’s overlapping assignments against
the fixed speaker records can expose an error. Questions about session topics may help the
organizer understand the schedule, but they leave that constraint unchecked. The complete
list of constraints gives random sampling a detection guarantee because every conflicting
schedule violates at least one listed constraint.
     Once a constraint is selected, the organizer must locate the relevant records, identify
the time intervals, and apply the comparison rule. If the selected constraint could have
exposed a missed conflict, incomplete records indicate an inadequate response; a mistaken
comparison despite complete records indicates an execution error. Displaying the records
together or providing a comparison tool could reduce the work needed to perform the check
correctly.
     For later rounds, the organizer can combine follow-ups prompted by the dialogue with
fresh random checks from the complete list. The construction in Appendix D reserves a
chosen probability each round for a reference check with a justified detection bound under
correct execution, leaving the remaining questions free to follow the dialogue. The appendix
derives the mixture’s evidence gain and distinguishes a bound for an individual challenge
from one that averages over the randomized policy.
     The resulting evidence gain determines how many passed checks are needed before ac-
ceptance. In Appendix E, a matrix-product check reaches the threshold within its budget
under the stated reliability bounds, whereas the scheduling audit requires more rounds than
are available.


                                            29
                                Zhang, Foster, and Sedoc




7.3 Evaluating Human Verification
The variation in ANC across the simulations motivates examining what verifiers actually
check before accepting. In particular, the accepted wrong defenses in the stress tests make
it useful to distinguish an answer that survives a diagnostic check from one that remains
unchanged through an exchange of plausible arguments. A human study could record the
selected challenges, evidence supplied, checks performed, and reasons for stopping, alongside
the final verdict and the truth of the claim.
    To test the benefit of decomposition and interaction, such a study could compare a
specified global review, local review of fixed indexed evidence, and local review with evidence
supplied on request. The conditions should use matched claims and source records, common
tools, and the same total review budget, including time spent choosing questions and finding
evidence. The two local conditions should draw on the same pool of evidence and use the
same checks, with participants randomly assigned across conditions within expertise groups.
Comparing global and static local review would help assess the effect of decomposition.
Comparing static and interactive local review would assess the added value of supplying
evidence in response to questions.
    The key empirical question is how the balance between false acceptance and rejection
of true claims changes as more rounds are allowed within a fixed budget. A lower false-
acceptance rate could come at the cost of rejecting more true claims, so both outcomes
need to be measured. Records of individual checks would help explain that tradeoff. For
example, if longer reviews lead to more rejected true claims, independent assessment of the
responses and checks could show whether usable evidence was missing or participants made
mistakes despite having it. Examining where these failures occur across task difficulties
and expertise groups would help determine whether dividing the review into smaller checks
reduces the burden of execution enough to offset the additional exchanges.

8 Limitations and Scope
The framework applies most directly to tasks with a usable truth condition and checks that
a bounded verifier can perform. Its guarantees concern the claim as formalized. Checking
a formal object does not establish that it faithfully represents the original natural-language
claim, and checking a retrieved source does not establish that the source is correct. Ap-
plying the framework therefore also requires justifying these correspondences (Min et al.,
2023; Jiang et al., 2023; Yang et al., 2023). Preference elicitation, creative tasks, contested
judgments, unrestricted program behavior, and claims whose evidence is unavailable may
benefit from dialogue without admitting the certification guarantees studied here.
    The theorems combine supplied diagnostic, response, and execution bounds; they do
not provide a general method for obtaining them from free-form dialogue. In particular,
the diagnostic and execution bounds must hold after every relevant history against every
admissible adaptive prover. A detection rate averaged across participants, rounds, or tasks is
insufficient for this purpose. Empirical estimates require additional justification to support
such bounds over the intended class of claims and interactions. The certification criteria are
sufficient conditions for the specified protocols, so failure to meet them does not establish
that the actual error targets are unattainable.



                                              30
                          Verifiability without Transparency




    Whether people can reliably perform the proposed checks remains untested. Applying
the response and execution models to human–LLM review requires evidence about how
effort, expertise, and cognitive load affect the provision of usable evidence and the correct
execution of checks. These relationships are theoretical inputs in the numerical examples.
Even in the matrix-product example, where exact algebra supplies the diagnostic bound,
the response and execution bounds remain assumptions. Counting checks or arithmetic
operations does not establish how long human review takes or whether local review reduces
cognitive load. Nor do the LLM-only simulations resolve this gap: they measure answer se-
lection without reproducing human attention, responsibility, or fatigue, and cannot identify
the human reliability parameters. Section 7.3 proposes studies to measure these aspects of
human review.
    The comparison in Proposition 3 holds the claim, source records, tools, and budgets
fixed and compares specified global and local implementations. It establishes a difference
in what the supplied bounds certify, rather than an ordering of actual error rates or an
advantage over all one-shot review methods. For example, the matrix-product check can
also be applied to a fixed submitted result. Any benefit attributed specifically to dialogue
must be distinguished from the benefit of making local evidence available.
    Completeness assumes honest response behavior; the protocol does not elicit latent
knowledge or solve alignment (Christiano et al., 2021; Friedl et al., 2026). Even with an
honest prover, protecting private information requires an additional condition: the full
verifier view must be efficiently simulatable without access to the prover’s private state.
Appendix C shows how the prescribed stopping rule preserves this property when it holds
for the continuation interaction. We have not constructed such a simulator for ordinary
LLM dialogue or established this privacy guarantee for the scheduling and matrix-product
examples. The result covers the specified verifier interacting with an honest prover on the
stated true-instance family, including rejection and timeout; it does not cover false instances
or verifier deviations outside these assumptions.

9 Conclusion
Human–LLM deliberation raises a verification problem when the user cannot readily repro-
duce the prover’s underlying search or argument construction. We give conditions under
which a human can verify the LLM’s claim through questions and checks within their bud-
get. Dialogue can expose supporting details on demand; acceptance is justified by diagnostic
checks with valid error bounds. Under the stated assumptions, those checks yield anytime-
valid soundness against adaptive provers and finite-horizon completeness that accounts for
both LLM response inadequacy and human execution error.
    The benefit of smaller checks depends on whether they reduce cognitive load enough
to offset the division of effort and the additional opportunities for error. Under common
resource budgets and separately justified bounds, the analysis identifies when those bounds
certify a specified local review while leaving a specified global check uncertified. This can
occur even when the global checker has a lower false-pass bound under correct execution.
    The practical requirement is to build informative checks that fit the verifier’s resources
and justify their diagnostic and reliability bounds. The theorems combine the bounds
for individual rounds into guarantees for the whole review, while a general construction for


                                              31
                               Zhang, Foster, and Sedoc




unrestricted natural-language dialogue remains open. When the required evidence cannot be
obtained within the budget, the protocol outputs Reject, indicating that the claim remains
insufficiently verified.

References
Chirag Agarwal, Sree Harsha Tanneru, and Himabindu Lakkaraju. Faithfulness vs. plausi-
 bility: On the (un)reliability of explanations from large language models. arXiv preprint
 arXiv:2402.04614, 2024. URL https://arxiv.org/abs/2402.04614.

Noga Amit, Shafi Goldwasser, Orr Paradise, and Guy N. Rothblum.         A
 theory for worst-case vs. average-case guarantees for LLMs.  In Advances
 in Neural Information Processing Systems, volume 38, pages 146513–146549,
 2025.    URL https://proceedings.neurips.cc/paper_files/paper/2025/hash/
 d7a2222b8d41014e060cfeb0995501d0-Abstract-Conference.html.

Cem Anil, Guodong Zhang, Yuhuai Wu, and Roger Baker Grosse. Learning to give checkable
  answers with prover-verifier games. In The Tenth International Conference on Learning
  Representations, 2022. URL https://openreview.net/forum?id=FqRHeQTDU5N.

Samuel R. Bowman et al. Measuring progress on scalable oversight for large language
  models. arXiv preprint arXiv:2211.03540, 2022. doi: 10.48550/arXiv.2211.03540. URL
  https://arxiv.org/abs/2211.03540.

Jonah Brown-Cohen, Geoffrey Irving, and Georgios Piliouras. Scalable AI safety via doubly-
  efficient debate. In Proceedings of the 41st International Conference on Machine Learning
  (ICML), volume 235 of Proceedings of Machine Learning Research, pages 4585–4602.
  PMLR, 2024. URL https://proceedings.mlr.press/v235/brown-cohen24a.html.

Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz,
   Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, Harsha Nori, Hamid
   Palangi, Marco Tulio Ribeiro, and Yi Zhang. Sparks of artificial general intelligence:
   Early experiments with gpt-4, 2023. URL https://arxiv.org/abs/2303.12712.

Zana Buçinca, Maja Barbara Malaya, and Krzysztof Z. Gajos. To trust or to think: Cog-
  nitive forcing functions can reduce overreliance on AI in AI-assisted decision-making.
  Proceedings of the ACM on Human-Computer Interaction, 5(CSCW1):1–21, 2021. doi:
  10.1145/3449287.

Collin Burns, Pavel Izmailov, Jan Hendrik Kirchner, Bowen Baker, Leo Gao, Leopold As-
  chenbrenner, Yining Chen, Adrien Ecoffet, Manas Joglekar, Jan Leike, Ilya Sutskever,
  and Jeffrey Wu. Weak-to-strong generalization: Eliciting strong capabilities with weak
  supervision. In Proceedings of the 41st International Conference on Machine Learning
  (ICML), volume 235 of Proceedings of Machine Learning Research, pages 4971–5012.
  PMLR, 2024. URL https://proceedings.mlr.press/v235/burns24b.html.

Liyan Chen, Yael Tauman Kalai, and Zoe Xi. How to avoid debate: Scalable AI safety via
  doubly-efficient interactive proofs, 2026. URL https://arxiv.org/abs/2607.03561.


                                            32
                         Verifiability without Transparency




Young Hyun Cho and Will Wei Sun. When should an AI workflow release? always-valid
  inference for black-box generate-verify systems, 2026. URL https://arxiv.org/abs/
  2605.12947.
Paul Christiano, Buck Shlegeris, and Dario Amodei. Supervising strong learners by ampli-
  fying weak experts. arXiv preprint arXiv:1810.08575, 2018. URL https://arxiv.org/
  abs/1810.08575.
Paul Christiano, Ajeya Cotra, and Mark Xu. Eliciting latent knowledge: How to
  tell if your eyes deceive you. Technical report, Alignment Research Center, Decem-
  ber 2021. URL https://docs.google.com/document/d/1WwsnJQstPq91_Yh-Ch2XRL8H_
  EpsnjrC1dwZXR37PC8/edit.
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz
 Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher
 Hesse, and John Schulman. Training verifiers to solve math word problems. arXiv preprint
 arXiv:2110.14168, 2021. URL https://arxiv.org/abs/2110.14168.
Mathias Dewatripont and Jean Tirole. Modes of communication. Journal of Political
 Economy, 113(6):1217–1238, 2005. doi: 10.1086/497999. URL https://doi.org/10.
 1086/497999.
Shehzaad Dhuliawala, Mojtaba Komeili, Jing Xu, Roberta Raileanu, Xian Li, Asli Ce-
  likyilmaz, and Jason Weston. Chain-of-verification reduces hallucination in large lan-
  guage models. In Findings of the Association for Computational Linguistics: ACL
  2024, pages 3563–3578, Bangkok, Thailand, 2024. Association for Computational Lin-
  guistics. doi: 10.18653/v1/2024.findings-acl.212. URL https://aclanthology.org/
  2024.findings-acl.212/.
Phan Minh Dung. On the acceptability of arguments and its fundamental role in nonmono-
  tonic reasoning, logic programming and n-person games. Artificial Intelligence, 77(2):
  321–357, 1995. doi: 10.1016/0004-3702(94)00041-X. URL https://doi.org/10.1016/
  0004-3702(94)00041-X.
James S. Fishkin. Democracy When the People Are Thinking: Revitalizing Our Politics
  Through Public Deliberation. Oxford University Press, 2018. ISBN 9780198820291.
  doi: 10.1093/oso/9780198820291.001.0001.    URL https://doi.org/10.1093/oso/
  9780198820291.001.0001.
Raymond Fok and Daniel S. Weld. In search of verifiability: Explanations rarely enable
  complementary performance in AI-advised decision making. AI Magazine, 45(3):317–332,
  2024. doi: 10.1002/aaai.12182. URL https://doi.org/10.1002/aaai.12182.
Rusins Freivalds. Probabilistic machines can use less running time. In Bruce Gilchrist,
 editor, Information Processing 77: Proceedings of the IFIP Congress 77, pages 839–842.
 North-Holland, 1977.
Korbinian Friedl, Francis Rhys Ward, Paul Yushin Rapoport, Tom Everitt, and Jonathan
 Richens. The impossibility of eliciting latent knowledge. arXiv preprint arXiv:2606.12268,
 2026. doi: 10.48550/arXiv.2606.12268. URL https://arxiv.org/abs/2606.12268.

                                            33
                               Zhang, Foster, and Sedoc




Yonatan Geifman and Ran El-Yaniv.        Selective classification for deep neu-
  ral networks.    In Advances in Neural Information Processing Systems, vol-
  ume 30, pages 4878–4887, 2017. URL https://papers.nips.cc/paper/2017/hash/
  4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html.

Shafi Goldwasser, Silvio Micali, and Charles Rackoff. The knowledge complexity of in-
  teractive proof systems. SIAM Journal on Computing, 18(1):186–208, 1989. doi:
  10.1137/0218012. URL https://doi.org/10.1137/0218012.

Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen, Yujiu Yang, Nan Duan, and Weizhu
  Chen. CRITIC: Large language models can self-correct with tool-interactive critiquing. In
  The Twelfth International Conference on Learning Representations, 2024. URL https:
  //openreview.net/forum?id=Sx038qxjek.

Lewis Hammond and Sam Adam-Day. Neural interactive proofs. In Proceedings of the
  Thirteenth International Conference on Learning Representations (ICLR), 2025. URL
  https://openreview.net/forum?id=R2834dhBlo.

Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang,
  Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, and Ting Liu. A survey
  on hallucination in large language models: Principles, taxonomy, challenges, and open
  questions. ACM Transactions on Information Systems, 43(2):1–55, 2025. doi: 10.1145/
  3703155. arXiv:2311.05232.

Geoffrey Irving, Paul Christiano, and Dario Amodei. AI safety via debate. arXiv preprint
 arXiv:1805.00899, 2018. URL https://arxiv.org/abs/1805.00899.

Alon Jacovi and Yoav Goldberg. Towards faithfully interpretable NLP systems: How
  should we define and evaluate faithfulness? In Proceedings of the 58th Annual Meeting
  of the Association for Computational Linguistics, pages 4198–4205, Online, July 2020.
  Association for Computational Linguistics. doi: 10.18653/v1/2020.acl-main.386. URL
  https://aclanthology.org/2020.acl-main.386/.

Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin
  Bang, Andrea Madotto, and Pascale Fung. Survey of hallucination in natural language
  generation. ACM Comput. Surv., 55(12), March 2023. ISSN 0360-0300. doi: 10.1145/
  3571730. URL https://doi.org/10.1145/3571730.

Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja
  Jamnik, Timothée Lacroix, Yuhuai Wu, and Guillaume Lample. Draft, sketch, and prove:
  Guiding formal theorem provers with informal proofs. In The Eleventh International
  Conference on Learning Representations, 2023. URL https://openreview.net/forum?
  id=SMa9EAovKMC.

Weina Jin, Xiaoxiao Li, and Ghassan Hamarneh. Why is plausibility surprisingly prob-
 lematic as an XAI criterion? arXiv preprint arXiv:2303.17707v4, 2025. URL https:
 //arxiv.org/abs/2303.17707. Current version revised May 2025.



                                            34
                        Verifiability without Transparency




Ryo Kamoi, Yusen Zhang, Nan Zhang, Jiawei Han, and Rui Zhang. When can LLMs actu-
  ally correct their own mistakes? A critical survey of self-correction of LLMs. Trans-
  actions of the Association for Computational Linguistics, 12:1417–1440, 2024. doi:
  10.1162/tacl a 00713. URL https://doi.org/10.1162/tacl_a_00713.

Zachary Kenton, Noah Y. Siegel, János Kramár, Jonah Brown-Cohen, Samuel Al-
  banie, Jannis Bulian, Rishabh Agarwal, David Lindner, Yunhao Tang, Noah D.
  Goodman, and Rohin Shah.       On scalable oversight with weak LLMs judg-
  ing strong LLMs.      In Advances in Neural Information Processing Systems
  (NeurIPS), volume 37, pages 75229–75276, 2024.     doi: 10.52202/079017-2395.
  URL            https://proceedings.neurips.cc/paper_files/paper/2024/hash/
  899511e37a8e01e1bd6f6f1d377cc250-Abstract-Conference.html.

Akbir Khan, John Hughes, Dan Valentine, Laura Ruis, Kshitij Sachan, Ansh Radhakr-
 ishnan, Edward Grefenstette, Samuel R. Bowman, Tim Rocktäschel, and Ethan Perez.
 Debating with more persuasive LLMs leads to more truthful answers. In Proceed-
 ings of the 41st International Conference on Machine Learning (ICML), volume 235
 of Proceedings of Machine Learning Research, pages 23662–23733. PMLR, 2024. URL
 https://proceedings.mlr.press/v235/khan24a.html.

Jan Hendrik Kirchner, Yining Chen, Harri Edwards, Jan Leike, Nat McAleese, and Yuri
  Burda. Prover-verifier games improve legibility of LLM outputs, 2024. URL https:
  //arxiv.org/abs/2407.13692.

Jon Kleinberg, Himabindu Lakkaraju, Jure Leskovec, Jens Ludwig, and Sendhil Mul-
  lainathan. Human decisions and machine predictions. The Quarterly Journal of Eco-
  nomics, 133(1):237–293, February 2018. ISSN 0033-5533. doi: 10.1093/qje/qjx032. URL
  https://doi.org/10.1093/qje/qjx032.

Vivian Lai and Chenhao Tan. On human predictions with explanations and predictions
  of machine learning models: A case study on deception detection. In Proceedings of the
  Conference on Fairness, Accountability, and Transparency (FAT*), pages 29–38. ACM,
  2019. doi: 10.1145/3287560.3287590.

Vivian Lai, Chacha Chen, Alison Smith-Renner, Q. Vera Liao, and Chenhao Tan. Towards
  a science of human-ai decision making: An overview of design space in empirical human-
  subject studies. In Proceedings of the 2023 ACM Conference on Fairness, Accountability,
  and Transparency, FAccT ’23, pages 1369–1385, New York, NY, USA, 2023. Association
  for Computing Machinery. ISBN 9798400701924. doi: 10.1145/3593013.3594087. URL
  https://doi.org/10.1145/3593013.3594087.

Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy
 Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by
 step. In The Twelfth International Conference on Learning Representations, 2024. URL
 https://openreview.net/forum?id=v8L0pN6EOi.

Yingda Lu, Xueming Luo, Liqiang Huang, and Danni Wang. Can providing algorithmic
  performance information facilitate humans’ inventory ordering behaviors? Information

                                           35
                              Zhang, Foster, and Sedoc




  Systems Research, 37(1):1–19, 2025. doi: 10.1287/isre.2022.0621. URL https://doi.
  org/10.1287/isre.2022.0621.

Shuai Ma, Qiaoyi Chen, Xinru Wang, Chengbo Zheng, Zhenhui Peng, Ming Yin, and Xi-
  aojuan Ma. Towards human-ai deliberation: Design and evaluation of llm-empowered
  deliberative ai for ai-assisted decision-making. In Proceedings of the 2025 CHI Con-
  ference on Human Factors in Computing Systems, CHI ’25, pages 1–23, New York,
  NY, USA, 2025. Association for Computing Machinery. ISBN 9798400713941. doi:
  10.1145/3706598.3713423. URL https://doi.org/10.1145/3706598.3713423.

Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah
 Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank
 Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yaz-
 danbakhsh, and Peter Clark. Self-refine: Iterative refinement with self-feedback.
 In Advances in Neural Information Processing Systems, volume 36, pages 46534–
 46594, 2023.   URL https://proceedings.neurips.cc/paper_files/paper/2023/
 hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html.

Hugo Mercier and Dan Sperber. Why do humans reason? Arguments for an argu-
 mentative theory. Behavioral and Brain Sciences, 34(2):57–74, 2011. doi: 10.1017/
 S0140525X10000968. URL https://doi.org/10.1017/S0140525X10000968.

Julian Michael, Salsabila Mahdi, David Rein, Jackson Petty, Julien Dirani, Vishakh Pad-
  makumar, and Samuel R. Bowman. Debate helps supervise unreliable experts. arXiv
  preprint arXiv:2311.08702, 2023. URL https://arxiv.org/abs/2311.08702.

Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih, Pang Wei Koh, Mo-
  hit Iyyer, Luke Zettlemoyer, and Hannaneh Hajishirzi. FActScore: Fine-grained atomic
  evaluation of factual precision in long form text generation. In Proceedings of the 2023
  Conference on Empirical Methods in Natural Language Processing, pages 12076–12100,
  Singapore, 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.
  emnlp-main.741. URL https://aclanthology.org/2023.emnlp-main.741/.

Sanjay Modgil and Henry Prakken. The ASPIC+ framework for structured argumentation:
  A tutorial. Argument & Computation, 5(1):31–62, 2014. doi: 10.1080/19462166.2013.
  869766. URL https://doi.org/10.1080/19462166.2013.869766.

Liangming Pan, Xiaobao Wu, Xinyuan Lu, Anh Tuan Luu, William Yang Wang, Min-
  Yen Kan, and Preslav Nakov. Fact-checking complex claims with program-guided rea-
  soning. In Proceedings of the 61st Annual Meeting of the Association for Computa-
  tional Linguistics (Volume 1: Long Papers), pages 6981–7004, Toronto, Canada, 2023.
  Association for Computational Linguistics. doi: 10.18653/v1/2023.acl-long.386. URL
  https://aclanthology.org/2023.acl-long.386/.

Henry Prakken. Coherence and flexibility in dialogue games for argumentation. Journal
  of Logic and Computation, 15(6):1009–1040, 2005. doi: 10.1093/logcom/exi046. URL
  https://doi.org/10.1093/logcom/exi046.



                                           36
                         Verifiability without Transparency




Aaditya Ramdas, Peter Grünwald, Vladimir Vovk, and Glenn Shafer. Game-theoretic
 statistics and safe anytime-valid inference. Statistical Science, 38(4):576–601, 2023. doi:
 10.1214/23-STS894. URL https://doi.org/10.1214/23-STS894.

Shuvom Sadhuka, Drew Prinster, Clara Fannjiang, Gabriele Scalia, Bonnie Berger, Aviv
  Regev, and Hanchen Wang. E-valuator: Reliable agent verifiers with sequential hypothesis
  testing, 2025. URL https://arxiv.org/abs/2512.03109v2. Version 2, revised May
  2026.

William Saunders, Ben Rachbach, Owain Evans, Zachary Miller, Jungwon Byun, and An-
 dreas Stuhlmüller. Evaluating arguments one step at a time. Ought technical progress
 update, January 2020. URL https://ought.org/updates/2020-01-11-arguments.

William Saunders, Catherine Yeh, Jeff Wu, Steven Bills, Long Ouyang, Jonathan Ward,
 and Jan Leike. Self-critiquing models for assisting human evaluators. arXiv preprint
 arXiv:2206.05802, 2022. doi: 10.48550/arXiv.2206.05802. URL https://arxiv.org/
 abs/2206.05802.

João Sedoc, Baotong Zhang, and Dean Foster. Trust but verify: Prover-verifier deliberation
  for selective LLM prediction, 2026. URL https://arxiv.org/abs/2605.25133.

Glenn Shafer, Alexander Shen, Nikolai Vereshchagin, and Vladimir Vovk. Test mar-
  tingales, Bayes factors and p-values. Statistical Science, 26(1):84–101, 2011. doi:
  10.1214/10-STS347. URL https://doi.org/10.1214/10-STS347.

Chenglei Si, Navita Goyal, Tongshuang Wu, Chen Zhao, Shi Feng, Hal Daumé III, and
 Jordan Boyd-Graber. Large language models help humans verify truthfulness—except
 when they are convincingly wrong. In Proceedings of the 2024 Conference of the North
 American Chapter of the Association for Computational Linguistics: Human Language
 Technologies (Volume 1: Long Papers), pages 1459–1474, Mexico City, Mexico, 2024.
 Association for Computational Linguistics. doi: 10.18653/v1/2024.naacl-long.81. URL
 https://aclanthology.org/2024.naacl-long.81/.

Miles Turpin, Julian Michael, Ethan Perez, and Samuel R. Bowman.      Language
 models don’t always say what they think: Unfaithful explanations in chain-
 of-thought prompting.    In Advances in Neural Information Processing Systems
 (NeurIPS), 2023. URL https://proceedings.neurips.cc/paper_files/paper/2023/
 hash/ed3fea9033a80fea1376299fa7863f4a-Abstract-Conference.html.

Salil Vadhan. The complexity of zero knowledge, 2007. URL https://people.seas.
  harvard.edu/~salil/research/complexityZK.pdf. Survey manuscript, October 16.

Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shix-
 ing Yu, Saad Godil, Ryan J. Prenger, and Animashree Anandkumar.            Le-
 anDojo: Theorem proving with retrieval-augmented language models.      In Ad-
 vances in Neural Information Processing Systems, volume 36, pages 21573–21612,
 2023.    URL https://proceedings.neurips.cc/paper_files/paper/2023/hash/
 4441469427094f8873d0fecb0c4e1cee-Abstract-Datasets_and_Benchmarks.html.


                                            37
                             Zhang, Foster, and Sedoc




Haiyan Zhao, Hanjie Chen, Fan Yang, Ninghao Liu, Huiqi Deng, Hengyi Cai, Shuaiqiang
 Wang, Dawei Yin, and Mengnan Du. Explainability for large language models: A survey.
 ACM Trans. Intell. Syst. Technol., 15(2), February 2024. ISSN 2157-6904. doi: 10.1145/
 3639372. URL https://doi.org/10.1145/3639372.

Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao
  Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonza-
  lez, and Ion Stoica. Judging LLM-as-a-judge with MT-bench and chatbot arena. In
  Advances in Neural Information Processing Systems, volume 36, pages 46595–46623,
  2023.     URL https://proceedings.neurips.cc/paper_files/paper/2023/hash/
  91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html.




                                          38
                                 Verifiability without Transparency




Appendix A. Protocol Mapping and Notation
Table 5 relates the framework’s components and guarantees to those of classical interactive
proofs. Table 6 collects the notation used in Sections 3–5 and Appendices C–E.
                    Table 5: Protocol objects and guarantees. The general human–LLM
                    framework becomes a standard interactive proof only under the unifor-
                    mity conditions in Corollary 1.

Classical object           Here                                Role or condition
Common and auxil-          x = ⟨s, ipub ⟩, z = ipriv , and L   The target statement s and public task information
iary inputs                                                    form the common input; verifier-only information
                                                               is auxiliary input and does not define the language.
Prover                     LLM strategy P with private         Produces history-dependent responses through Q;
                           state θ                             soundness quantifies over every adaptive admissible
                                                               strategy.
Verifier                   Human strategy V                    Uses challenge policy πV , verification rule U , poly-
                                                               nomially bounded messages, and maximum horizon
                                                               T.
Challenge–response         Histories     hm ;       output     The message sequence records the initial answer,
                               ′
transcript                 (d(m ) , Ω)                         verifier-selected challenges, and prover responses;
                                                               Ω separately records the terminal verdict.
Honest-prover       cor-   Bounds am                           An adequate local response occurs with probability
rectness                                                       at least am , uniformly over the augmented analysis
                                                               history; ideal response adequacy is the case am = 1.
Verifier validity          Bounds (qm , cm )                   Correct execution occurs with probability at least
                                                               cm ; the prescribed correct checker has false-pass
                                                               probability at most qm , giving q̄m = 1−cm (1−qm ).
Completeness               Theorem 2                           For a true statement and a response-reliable hon-
                                                               est
                                                               QK prover, acceptance has probability at least
                                                                 m=1 am cm under the stated verifier and progress
                                                               conditions, with K ≤ T .
Soundness                  Theorem 1                           For a false statement and every adaptive admissible
                                                               prover, the probability of crossing the acceptance
                                                               threshold at any round m ≤ T is at most δ, under
                                                               the stated verifier conditions.
Interactive-proof sta-     Corollary 1                         Requires a formal promise problem, a uniform PPT
tus                                                            verifier, polynomial communication and horizon,
                                                               and standard completeness/soundness quantifiers.
HVZK preservation          Corollary 3                         Assumes a uniform full-view simulator for the spec-
                                                               ified continuation and an efficient prefix map repro-
                                                               ducing the actual stopped view; preserves compu-
                                                               tational HVZK on the covered true-instance family.
                    Table 6: Core notation for the protocol, sequential certification,
                    deterministic specialization, and conditional privacy result.

  Symbol                           Meaning
  Σ, X = Σ∗ , H, ∥                 Finite alphabet, token space, well-formed encoded histories, and self-
                                   delimiting append operation.
  κ(s, i), Lmax                    Input-size parameter and polynomial message-length cap for admis-
                                   sible executions.



                                                          39
                                    Zhang, Foster, and Sedoc




                                          Table 6 (continued)
Symbol                          Meaning
A0 , S, v, L                    Base axiom system, statement space, total truth map, and language
                                L = {s : v(s) = ⊤}.
P , P H, P ∗                    Implemented prover, honest prover used for completeness, and arbi-
                                trary adaptive prover used for soundness.
Θ, θ, Q                         Prover private-state space, realized private state, and production
                                function Q : H × Θ → X.
I, I, i = (ipub , ipriv ), Ai   Verifier information universe, representable information states, their
                                public/private split for formal IP/HVZK instantiations, and verifier-
                                side axioms.
C, C, πV , U                    Challenge-token universe, available challenge set, challenge-selection
                                policy, and decision function.
υ∈X                             Persistent verifier state containing check outcomes, certificate values,
                                and consumed randomness; suppressed in abbreviated policy and
                                decision notation.
T , hm , Hm , Ps,P              Maximum horizon, realized and random histories after round m, and
                                execution law for statement s and prover P .
Fm , G m                        Post-check observable filtration through round m and observable
                                pre-check field for the current challenge and response.
Jm , Km                         Analysis history retaining response-adequacy and execution events
                                through round m, and its pre-check counterpart Km = Jm−1 ∨ Gm .
Am , am                         Local response-adequacy event and its deterministic lower bound
                                conditional on the augmented past for a true statement; clarification
                                does not overwrite am .
Em , cm                         Correct human-execution event and its deterministic lower bound
                                conditional on the full pre-check field; clarification does not overwrite
                                cm .
         ◦
Passm , rm , qm , q̄m           Passed diagnostic-check event, prescribed correct-check pass prob-
                                ability, the predictable bound on its challenge-policy average for a
                                false claim, and the implemented bound 1 − cm (1 − qm ).
νm , µm , λanc
           m , ρm               Reference and deployed challenge kernels, predictable anchor mass,
                                and worst-case reference detection bound in Appendix D.
δ, γ                            Target upper bounds on false acceptance and failure to accept a true
                                claim, respectively.
Mm                              Formal multiplicative certification process; log Mm is its cumulative
                                log evidence.
gm = − log q̄m                  Implemented diagnostic log-evidence credited to a passed check;
                                clarification has zero gain.
                     ′
xm , ym , τ , Ω, d(m )          Round-m challenge and response, stopping time, terminal verdict,
                                and final transcript.
KT , ΠES , Π(n)                 Full-horizon unwrapped diagnostic kernel, first-crossing wrapper,
                                and precommitted n-round companion wrapper.
Rn , C n , K δ                  Deterministic false-survival product, true-path product, and first
                                soundness-eligible crossing.


                                                    40
                           Verifiability without Transparency




                                     Table 6 (continued)
Symbol                      Meaning
ERδ,γ , nmin , nmax         Product-based certifiable effective region and its boundaries; nmin =
                            Kδ when the region is nonempty.
ERsuf
  δ,γ                       Additive inner approximation to the exact effective region; its mem-
                            bers are precommitted certificate lengths, not post hoc stopping
                            choices.
ERsuf
  δ,γ (E)                   Effort-indexed sufficient effective region when each candidate reallo-
                            cates total effort and therefore defines a different design.
E, ei , eos                 Total review budget and effort allocated to local rounds or the global
                            check, including preparation, execution, and interpretation.
ξι , λ i , f , r            Expertise/tool state, local cognitive load including context, and il-
                            lustrative execution-reliability functions.
λos , cos , ∆               Global-check load, execution bound, and global load minus accumu-
                            lated local loads.
qos , aos , Ros , Cos       Separately justified global diagnostic and response-adequacy
                            bounds, and resulting false-acceptance upper and true-acceptance
                            lower bounds.
cn , τn                     Uniform local execution envelope and sufficient reliability threshold
                            for both error targets.
Y, ΘH (κ, x)                Covered true instances and prespecified honest private-state family
                            for conditional HVZK preservation.
V cont , V stop , Viewθb    Specified continuation and stopped verifiers and their full views un-
                            der Pθ , for b ∈ {cont, stop}.
Sim0 , Simstop , F          Assumed continuation-view simulator, composed stopped-view sim-
                            ulator, and uniform prefix map, with Simstop = F ◦ Sim0 .




                                               41
                                 Zhang, Foster, and Sedoc




Appendix B. Reproducing Figure 3
Figure 3 evaluates the sufficient region in (19) for 33 review budgets, E = 20, 25, . . . , 180,
                                                   (n)
and 14 candidate lengths, n = 1, . . . , 14, with ei = E/n. The fixed parameters are
                                                                      (n)
       T = 14,       q = 0.20,     δ = 0.10,         γ = 0.20,       ai     = 1,     ξι = 10.

Using natural logarithms, the full execution parameterization is

              r(ξ) = 1 + log(1 + ξ),
                                     log(1 + ξ)
               b(ξ) = 0.91 + 0.035                ,
                                   1 + log(1 + ξ)
                                                            
            f (e, ξ) = min 0.995, b(ξ) + 0.10 1 − exp(−0.04e) ,
                                                                                     
                                                   (n)                            λi
                 λi = 0.010 + 0.001(i − 1),       ci = f (E/n, 10) exp        −         .
                                                                                r(10)

In particular, r(10) ≈ 3.39789527 and f (0, 10) = b(10) ≈ 0.93469951.
    For each (E, n), the calculation retains n exactly when
                           n                                 n
                              (n)                               (n)
                           X                                 Y
                       0.8   ci ≥ log 10          and          ci ≥ 0.8.
                           i=1                               i=1

No rounding is applied before these comparisons. There is no random sampling. The
resulting sets are nonempty and contiguous at every evaluated budget. For numerical
checks,
                               ERsuf
                                 δ,γ (20) = {4},
                                  ERsuf
                                    δ,γ (60) = {3, 4, 5, 6},
                                 ERsuf
                                   δ,γ (180) = {3, 4, . . . , 10}.

The right panel counts the candidate review lengths that meet both criteria. Shading and
steps connect the evaluated budget points; they do not locate the exact budgets at which
the set changes.




                                                42
                           Verifiability without Transparency




Appendix C. Conditional Honest-Verifier Zero-Knowledge Preservation
Stopping once enough evidence has accumulated raises a privacy question: what can the
verifier learn about the prover’s private information from when and how the interaction
ends? Suppose that the full record of an interaction can already be efficiently simulated
from the verifier’s inputs, without access to the prover’s private state. The simulated record
must be computationally indistinguishable from a real one. If the actual stopped record is
obtained by applying the prescribed stopping rule to the full record, applying that rule to
the simulated record gives a simulator for the stopped interaction as well. The following
assumptions make this argument precise, including the stopping time, final verdict, and
records of rejected or timed-out executions.
    Use x = ⟨s, ipub ⟩, z = ipriv , and the uniformity and polynomial-resource conventions
of Corollary 1. Fix the specified verifier, including its check-execution law and protocol
parameters. For each covered true instance x ∈ Y, prespecify a nonempty family ΘH (κ, x)
of honest private states. The state θ is fixed during execution; fresh prover randomness is
sampled separately.
    Write Viewθb = ViewPV θb (z) (1κ , x) for b ∈ {cont, stop}. Full views include the inputs,
verifier random tape, initial response ys , all raw visible messages (including any that trigger
rejection), visible tool/check records, and verifier-local state. They cover the entire specified
execution distribution, including rejection and timeout, without conditioning on acceptance.
Analysis-only events Am , Em are not additional observations.
    The continuation verifier V cont agrees with the actual verifier V stop through the stopping
point of V stop in initialization, adaptive challenges, checking, and state updates, including
certificate-dependent choices. After V stop stops, V cont follows a fixed continuation rule. Let
F be a uniform, θ-independent, deterministic polynomial-time map that retains the stopped
prefix and computes the certificate and terminal records using only the view. It is defined
on all encoded strings, returning a fixed marker on malformed encodings. With a common
polynomial-length random-tape convention, F retains that tape and satisfies
                                                            
                                    Viewθstop ≡d F Viewθcont .

    Assume that a single uniform simulator Sim0 runs in probabilistic polynomial time. It
receives only (1κ , x, z) and the fixed public protocol description, with no further advice
depending on θ or access to Pθ , and satisfies
                               n          o
                                 Viewθcont ≈c {Sim0 (1κ , x, z)} .

For each probabilistic polynomial-time distinguisher, one negligible advantage bound applies
uniformly over all covered x ∈ Y, θ ∈ ΘH (κ, x), and allowed polynomial-length z. The
guarantee is relative to (x, z); z need not be independent of θ.

Corollary 3 (Conditional HVZK preservation) Then the stopped interaction is com-
putationally honest-verifier zero knowledge on the covered family, with simulator

                             Simstop (1κ , x, z) = F (Sim0 (1κ , x, z)) .



                                                 43
                                 Zhang, Foster, and Sedoc




Proof The composed simulator is uniform probabilistic polynomial time. A distinguisher
for the stopped views, composed with F , would distinguish the underlying views. The
equality in distribution above therefore proves the claim.


   We do not construct Sim0 for ordinary LLM dialogue or establish the simulation as-
sumption in the certification examples.

Appendix D. Diagnostic Bounds for Adaptive Challenge Mixtures
This appendix formalizes the anchored construction introduced at the end of Section 4. It
is one sufficient way to obtain the diagnostic bound required by Theorem 1; Appendix E
applies it to matrix-product and scheduling checks.
    Before execution, fix a map αm (h, i) for the information used by the reference check.
This map must be independent of how the prover presents the claim after commitment.
Let νm (· | αm (h, i)) be an admissible conditional distribution of reference challenges. The
combined challenge distribution is

                  µm (· | h, i) = λanc                          anc
                                   m νm (· | αm (h, i)) + (1 − λm )eµm (· | h, i),         (24)

where λanc
        m ∈ [0, 1] is Fm−1 -measurable and µ
                                           em may adapt arbitrarily to the transcript; the
prover sees only the realized challenge.

Proposition 4 (Anchored local validity) For a false statement s, prover P ∗ , reached
                                               ∗
history h, and proposed challenge x, let ds,P
                                            m (h, x) be the probability that the prescribed cor-
rect checker rejects the false statement after P ∗ responds. If an Fm−1 -measurable ρm ∈ [0, 1]
satisfies, uniformly over all false statements, adaptive admissible provers, and reachable ac-
tive histories,               Z
                                    ∗
                                ds,P
                                 m (h, x) νm (dx | αm (h, i)) ≥ ρm ,                       (25)

then Assumption 1 may use

                          qm = 1 − λanc
                                    m ρm ,           q̄m = 1 − cm λanc
                                                                   m ρm ,

whenever 0 < cm λanc
                   m ρm < 1, preserving anytime-valid soundness however the remaining
challenges are chosen within the stated conditions.

Proof At a reached history,
      Z                                 Z
          s,P ∗                     anc        ∗
        dm (h, x) µm (dx | h, i) ≥ λm     ds,P                             anc
                                           m (h, x) νm (dx | αm (h, i)) ≥ λm ρm .


Thus the pass probability under correct execution is at most qm , and human execution
reliability ensures that the false statement is rejected in this round with probability at least
cm λanc
     m ρm , yielding q̄m .


   For a passed diagnostic round, the resulting log evidence gain is

                               gm = − log 1 − cm λanc
                                                         
                                                   m ρm .


                                                44
                          Verifiability without Transparency




The false-pass bound underlying this gain averages over both components of the challenge
policy, so the same gain is credited to every passed diagnostic round. Crediting the adap-
tive component with additional diagnostic strength requires a separately justified false-pass
bound.
    When a false-pass bound is available for an individual question, the verifier can use it
directly if that question is selected deterministically; random selection instead requires av-
eraging over the selection policy. Specifically, suppose a candidate challenge z ∈ C(hm−1 , i)
has a false-pass bound qm (z), justified before observing the response and uniformly over
the false statements, provers, and histories required by Assumption 1. If the verifier selects
z deterministically from the current history, then qm = qm (z). With execution bound cm
and 0 < 1 − cm (1 − qm (z)) < 1, a passed check contributes
                                                                  
                               gm (z) = − log 1 − cm (1 − qm (z))
to the log certificate. A larger gm (z) supplies more evidence per pass, while response
adequacy also matters for completeness. For a randomized selection policy, the certificate
instead uses a bound on the pass probability averaged over the policy’s choices, as in the
mixture above.

Appendix E. Worked Certification Examples
This appendix illustrates the certification criteria of Section 5. The matrix-product check
yields a nonempty certifiable region, while the scheduling example shows how the required
number of checks can exceed the review budget.

E.1 A Matrix-Product Certificate
Fix a prime p, a dimension d, input matrices A, B ∈ Fd×d
                                                     p , and an LLM-produced candidate
       d×d
C ∈ Fp before initialization. The target statement is sMM : AB = C over the declared
field. The verifier has an independent exact-arithmetic checker and canonical encodings of
the frozen matrices. In diagnostic round m, it samples a fresh uniform vector rm ∈ {0, 1}d
and asks the prover for
                        um = Brm ,      vm = Aum ,        wm = Crm .
The prescribed checker independently recomputes all three vectors and passes only if all
requested vectors are supplied, agree with its computation, and satisfy vm = wm . All
arithmetic is exact in Fp ; this claim concerns the fixed matrix product, not unrestricted
correctness of the program that produced it.
    This is Freivalds’ randomized matrix-product check (Freivalds, 1977). To see its diag-
nostic guarantee, suppose D := AB − C ̸= 0 and choose a nonzero entry Djk . Conditional
on all coordinates of rm except rm,k , the equation
                                                  X
                            (Drm )j = Djk rm,k +     Djℓ rm,ℓ = 0
                                                   ℓ̸=k

holds for at most one of rm,k = 0, 1. Hence
                             Pr(A(Brm ) = Crm | Fm−1 ) ≤ 12 .

                                              45
                                Zhang, Foster, and Sedoc




The matrices are frozen and the new vector is independent of the preceding history, so this
bound holds after every adaptive dialogue history. An arbitrary prover can only further
reduce the pass probability under correct execution by supplying inconsistent vectors. Thus
q = 1/2 is justified uniformly over all false claims and admissible provers in this task domain.
On a true claim, an exact honest response passes every correctly executed check.
Five checks meet both targets. With ideal responses and execution, a = c = 1 and five
passes yield R5 = 2−5 < 0.05 with true acceptance probability one. For fallible execution,
fix T = 10, δ = 0.05, and γ = 0.10, and suppose the history-uniform bounds required in
Section 4 hold with a = c = 0.99. Then
                    q̄ = 1 − 0.99(1 − 1/2) = 0.505,
                  R5 = 0.5055 ≈ 0.032844,          C5 = (0.992 )5 ≈ 0.904382.

On an all-pass path, Mn = 1/Rn crosses 1/δ = 20 first at n = 5: R4 ≈ 0.065038 > 0.05.
Since C6 ≈ 0.886385 < 0.90 and both products decrease with n, the exact product-based
region is
                                  ER0.05,0.10 = {5}.                             (26)
For this same example, the additive diagnostic condition is 0.495n ≥ log 20, which first
holds at n = 7. By then, the true-acceptance lower bound has fallen to C7 = 0.9914 ≈
0.868746 < 0.90 and decreases for longer reviews. Thus the additive sufficient region is
empty, even though the exact product criterion certifies the five-round design.
Adaptive follow-ups and resources. Use a fresh random-vector check with probability
λanc ∈ (0, 1]; otherwise, choose a vector based on the dialogue. Both choices draw from the
same set of vectors and use the same checker. Appendix D then gives q = 1 − λanc /2 and
q̄ = 1 − cλanc /2. This bound averages over both ways of choosing a challenge before the
round. It is used even when the realized challenge was chosen from the dialogue.
    Each anchor check uses d random bits, three exact matrix–vector products, and O(d)
comparisons and response entries. For fixed p, checking and storage
                                                               P5     cost O(d2 ). Under the
effort convention of Section 5, the five-round design requires i=1 ei ≤ E.

E.2 A Scheduling Certificate beyond the Review Budget
Apply the anchored construction of Section 4 to a fixed ten-session schedule. One availability
check per session covers its speakers and room; two checks for each of the 45 session pairs
test room and speaker conflicts. Both branches use this complete list of J = 100 constraints
and the same checker; the random branch samples uniformly with replacement.
    Fix λanc = 0.2, c = 0.9, and δ = 0.05. Then q = 0.998 and q̄ = 0.9982. With every
scheduled round diagnostic, the all-pass certificate and required number of rounds are
                                                       
                                    −n        log(1/δ)
                             Mn = q̄ ,                    = 1663.
                                               − log q̄

Thus Kδ = 1663 only if T ≥ 1663. At T = 20, even 20 passes cannot reach the threshold;
the primary protocol always rejects at or before timeout. Its false-acceptance and true-
acceptance probabilities are then both zero.


                                              46
                            Verifiability without Transparency




    For fixed-length protocols with a = 1 and completeness target 1 − γ = 0.8, the first
length meeting the false-acceptance target has C1663 = 0.91663 ≈ 8.04 × 10−77 . Since Cn
decreases with n, no horizon satisfies both product criteria. The execution bound c = 0.9
must hold uniformly over histories throughout the chosen horizon.
    The 1663-round requirement reflects how little guaranteed evidence each pass con-
tributes. The random branch is used with probability 0.2, and its uniform draw detects at
least one violated constraint among 100 with probability at least 1/100 under correct execu-
tion. Including the execution bound gives a detection lower bound of 0.9×0.2/100 = 0.0018,
so each pass adds only − log(0.9982) ≈ 0.001802 toward the threshold log 20. The certificate
credits no additional detection from the dialogue-based branch. With ideal responses and
execution, checking all 100 constraints once would instead settle the fixed claim. Such an
exhaustive audit uses a different acceptance rule and needs its own execution-error analysis.

E.3 Reproducing the Global and Local Comparison
This subsection reproduces Table 1 in Section 5.2. Both designs use frozen 20-by-20 ma-
trices over F101 . Direct multiplication gives qos = 0 and aos = 1. The interactive local
design performs five Freivalds checks, giving q = 1/2 by Appendix E.1, with ai = 0.99 for
independently checked prover replies.
Resource and reliability conditions. At E = 120, allocate eos = 120 to the global
check and ei = 24 to each local round. Both designs use the same trusted interface for
validated inputs and exact arithmetic; subsequent input selection and tool-use errors must
satisfy the execution conditions.
    Ordinary dense multiplication takes 8,000 field multiplications and 7,600 additions glob-
ally, versus 6,000 and 5,700 for five local checks. Including comparisons, both fit a 20,000-
operation cap. With fixed-width entries and a shared stored snapshot, a 4,096-word com-
munication cap covers the inputs, challenges, replies, checker displays, and metadata for
either design. These are the resource caps used for this comparison, not lower bounds on
what every implementation requires.
    Use the functions f, r, b from Appendix B, with

         ξι = 10,   λi = 0.010 + 0.001(i − 1),    λos = 0.20,   δ = 0.05,   γ = 0.10.

The load values are assumptions about the compared review procedures; they are not
inferred from the arithmetic counts. With these values, f (24, 10) = f (120, 10) = 0.995, so
the execution bounds are
                                                                       
                      0.010 + 0.001(i − 1)                          0.20
    ci = 0.995 exp −                         ,  cos = 0.995 exp −           ≈ 0.938125.
                             r(10)                                  r(10)

Substituting into the product bounds gives
                      5
                      Y                                  5
                                                         Y
               R5 =     (1 − ci /2) ≈ 0.032602,   C5 =     (0.99ci ) ≈ 0.911219,
                      i=1                                i=1
              Ros = 1 − cos ≈ 0.061875,           Cos = cos ≈ 0.938125.


                                             47
                               Zhang, Foster, and Sedoc




These are the entries in Table 1. The local bounds meet both targets, R5 ≤ 0.05 and
C5 ≥ 0.90. Since R4 ≈ 0.064617 > 0.05, the first acceptance threshold crossing on an
all-pass path occurs at round five. The global false-acceptance upper bound exceeds 0.05,
although its true-acceptance lower bound exceeds 0.90. The additive diagnostic sum for the
                1 P5
local design is 2 i=1 ci ≈ 2.478731 < log 20, so that sufficient criterion does not certify
this design.
    The load sensitivity reported in Section 5.2 follows by replacing only λos = 0.20 with
0.10. This gives cos ≈ 0.966144, hence Ros ≈ 0.033856 and Cos ≈ 0.966144. The global
bounds then meet both targets as well, showing how the comparison depends on the assumed
execution reliability.




                                            48
