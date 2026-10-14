                                                                                                                                                                                              1




                                           ConformalNL2LTL: Translating Natural Language Instructions into
                                            Temporal Logic Formulas with Conformal Correctness Guarantees
                                                           David Smith Sundarsingh∗ , Jun Wang∗ , Jyotirmoy V. Deshmukh, Yiannis Kantaros



                                            Abstract—Linear Temporal Logic (LTL) is a widely used task
                                         specification language for autonomous systems. To mitigate the
                                         significant manual effort and expertise required to define LTL-
                                         encoded tasks, several methods have been proposed for trans-
                                         lating Natural Language (NL) instructions into LTL formulas,
                                         which, however, lack correctness guarantees. To address this, we
arXiv:2504.21022v2 [cs.CL] 20 Feb 2026




                                         propose a new NL-to-LTL translation method, called Confor-
                                         malNL2LTL that achieves user-defined translation success rates
                                         on unseen NL commands. Our method constructs LTL formulas
                                         iteratively by solving a sequence of open-vocabulary question-
                                         answering (QA) problems using large language models (LLMs).                 Fig. 1. ConformalNL2LTL translates natural language-based robot tasks into
                                         These QA tasks are handled collaboratively by a primary and an              Linear Temporal Logic formulas with translation correctness guarantees; see
                                                                                                                     demonstrations in [35].
                                         auxiliary model. The primary model answers each QA instance
                                         while quantifying uncertainty via conformal prediction; when                to convert NL instructions into temporal logic formulas [27]–
                                         it is insufficiently certain according to user-defined confidence           [34], which then serve as task specification inputs to the above-
                                         thresholds, it requests assistance from the auxiliary model and,
                                                                                                                     mentioned temporal logic planners. However, these algorithms
                                         if necessary, from the user. We demonstrate theoretically and em-
                                         pirically that ConformalNL2LTL achieves the desired translation             lack correctness guarantees, meaning the resulting LTL for-
                                         accuracy while minimizing user intervention.                                mula may not accurately reflect the original NL task. This
                                                                                                                     misalignment can result in robot plans that fail to meet the
                                           Index Terms—Formal Methods in Robotics and Automation,
                                         Autonomous Agents, AI-Enabled Robotics                                      original NL instructions.
                                                                                                                        To address this limitation, we propose a new translation
                                                                I. I NTRODUCTION                                     method, ConformalNL2LTL (Conformal translation of NL
                                                                                                                     commands to LTL formulas), which achieves user-defined
                                         L     INEAR Temporal Logic (LTL) has become a power-
                                               ful formalism for specifying a wide range of robotic
                                         missions beyond simple reach-avoid requirements, such as
                                                                                                                     translation success rates on previously unseen NL instructions.
                                                                                                                     We consider a robot with a known skill set (e.g., manipulation,
                                                                                                                     sensing, and mobility) tasked with executing high-level NL
                                         surveillance, coverage, and data-gathering [1]. Several task and
                                                                                                                     missions in environments containing semantic objects and
                                         motion planners have been developed for robots with LTL-
                                                                                                                     regions. Each NL task specifies how the robot should apply
                                         encoded tasks, offering correctness and optimality guarantees.
                                                                                                                     its skills to particular objects or regions in a prescribed
                                         These planners have demonstrated success in handling known
                                                                                                                     temporal and logical order. ConformalNL2LTL translates NL
                                         environments [2]–[8], unknown static environments [9]–[11],
                                                                                                                     commands into LTL formulas defined over atomic propo-
                                         and dynamic or uncertain environments [12]–[16], including
                                                                                                                     sitions (APs), i.e., Boolean variables, that are grounded in
                                         scenarios where system dynamics are unknown [17]–[20] or
                                                                                                                     the robot’s capabilities and the environment. Our approach
                                         robot capabilities may fail unexpectedly [21]–[26].
                                                                                                                     uses pre-trained LLMs as backbone translators, augmented
                                            Despite the remarkable performance of LTL-based planners,
                                                                                                                     with Conformal Prediction (CP) [36], [37], an uncertainty-
                                         a key limitation is the significant manual effort and domain ex-
                                                                                                                     quantification framework that plays a central role in achieving
                                         pertise required to specify missions as temporal logic formulas.
                                                                                                                     user-specified translation success rates. The key idea is to con-
                                         As a result, natural language (NL) has emerged as an appealing
                                                                                                                     struct the LTL formula iteratively by framing the translation
                                         alternative for mission specification. Several algorithms have
                                                                                                                     problem as a sequence of interdependent question–answering
                                         been proposed that leverage Large Language Models (LLMs)
                                                                                                                     (QA) tasks, whose answers collectively determine the final
                                           ∗ indicates equal contribution.                                           specification. These QA tasks are solved collaboratively by
                                           D. S. Sundarsingh, J. Wang, and Y. Kantaros are with Department of        two LLMs, referred to as the primary and auxiliary mod-
                                         Electrical and Systems Engineering, Washington University in St Louis,      els, with CP coordinating their interaction. Each QA step
                                         MO, 63108, USA. Emails: {d.s.sundarsingh, junw, ioannisk}@wustl.edu. J.
                                         Deshmukh is with Department of Computer Science, University of Southern     incorporates the NL instruction together with the partial LTL
                                         California, Los Angeles, CA 90089, USA. Email: jdeshmuk@usc.edu.            formula constructed so far, and prompts the primary LLM
                                           D.S.Sundarsingh, J. Wang, and Y. Kantaros were partially supported by     to propose either a temporal/logical operator or an AP to
                                         the ARL grant DCIST CRA W911NF-17-2-0181 and the NSF award CNS
                                         #2231257. J. Deshmukh was partially supported through the following NSF     extend the specification. A naı̈ve approach would be to query
                                         grants: CAREER award (SHF-2048094), CNS-2039087, SLES-2417075, find-        the primary model once and accept its response; however,
                                         ing by Toyota R&D through the USC Center for Autonomy and AI, and the       this ignores the model’s confidence in the correctness of its
                                         Airbus Institute for Engineering Research.
                                           1 Additional materials, including videos and code, are available on the   response. To enable confidence-aware construction of LTL
                                         project webpage at: conformalnl2ltl.github.io.                              formulas, inspired by [38]–[40], we sample multiple responses
                                                                                                                                          2



per question and use their empirical frequencies as a coarse        [12], [14], [17], [18], [20]–[24], [53], providing traceability
proxy for model confidence. Rather than selecting the response      and allowing users to localize errors to specific stages (e.g.,
with the highest empirical confidence (as in, e.g., [39], [41]),    translation vs. planning).
we employ CP to calibrate this uncertainty. This step is crucial,      (iii) CP for Verified Autonomy: CP has been widely used
as LLMs often produce incorrect outputs with high confidence        for uncertainty quantification in autonomy tasks, including
[42], which can result in erroneous translations. Using CP and      object tracking [54], perception [55], trajectory prediction [56],
the responses of the primary model, we construct for each QA        reachability analysis [57], and decision-making [58], [59].
task a prediction set that contains the correct operator or AP      More recently, CP has also been used to quantify uncer-
with a user-specified confidence. When this prediction set is       tainty in LLM-based planners [42], [60]–[63]. However, these
a singleton, the algorithm proceeds with that choice. When          works are limited to open-source LLMs where logit/confidence
the set is non-singleton—indicating high uncertainty—the            scores are available. CP for closed-source LLMs has been
primary model seeks assistance. Help is first requested from        explored in [38], [40], but only for single QA tasks. Our
the auxiliary LLM, which is queried in the same manner to           work extends these efforts by enabling CP-based uncertainty
produce its own prediction set. We then intersect the prediction    quantification for both open- and closed-source LLMs and
sets of the two models. If the intersection is a singleton, the     by handling a sequence of interdependent QA tasks that are
corresponding response is selected; if it remains non-singleton,    necessary for constructing LTL formulas. Additionally, these
the user is asked to choose among the remaining options. If the     existing CP-enabled LLM-based approaches rely solely on a
intersection is empty or does not contain a correct response,       user to resolve high-uncertainty cases, resulting in frequent hu-
the user terminates the translation process.                        man interventions, especially as the desired success probability
   We provide theoretical guarantees showing that Confor-           increases, thus limiting autonomous deployment [42], [60]–
malNL2LTL achieves user-specified translation success rates         [63]. We address this limitation by invoking an auxiliary LLM
under the standard distributional assumptions required for CP.      to resolve high-uncertainty cases before involving the user,
Extensive numerical experiments further demonstrate that our        yielding a significant reduction (e.g., from 36.5% to 4%) in the
method attains high success levels (e.g., 99%) on unseen NL         proportion of formulas that required help in their construction
instructions while requiring very low rates of user interven-       from the user at least once, as shown empirically (see Section
tion (e.g., 0.378%). We also show that ConformalNL2LTL              V-C). Finally, to the best of our knowledge, this work is the
outperforms existing translation methods [30], [31], which do       first to apply CP to LLM-based NL-to-LTL translation.
not explicitly account for uncertainty, and that it continues          Contribution: The contribution of this paper can be sum-
to outperform these baselines even when the CP-based help           marized as follows. First, we propose ConformalNL2LTL, the
mechanism is disabled and only the highest-confidence re-           first NL-to-LTL translation algorithm capable of achieving
sponses from the primary model are used. For completeness,          user-specified translation success rates on unseen NL instruc-
we compare an integration of ConformalNL2LTL with the TL-           tions. Second, we present the first application of CP to LLMs
RRT* planner [6] against methods that map NL instructions di-       working collaboratively for NL-to-LTL translation tasks, with
rectly to robot plans, bypassing the translation to LTL formulas    the added benefit that our method can be applied to both open-
[43], and observe similar conclusions. We further demonstrate       and closed-source LLMs. Third, we provide both theoretical
the planning capabilities of the integrated framework for           and empirical analyses demonstrating that ConformalNL2LTL
language-instructed robots; see Fig. 1. Finally, we empirically     can achieve user-specified translation success rates while
demonstrate strong performance of ConformalNL2LTL under             maintaining low help rates from users. Fourth, we release the
distribution shifts that violate CP assumptions and compromise      software implementation of ConformalNL2LTL, along with
our theoretical guarantees.                                         datasets developed for calibration and testing purposes [64]
   Related Works: (i) NL-to-LTL Translation: As discussed
earlier, several NL-to-LTL translation methods have been
                                                                                       II. P ROBLEM S TATEMENT
proposed, generating LTL formulas that are then used as
inputs to existing planners [27]–[34]. However, unlike Con-            Robot and Environment Modeling: Consider a robot
formalNL2LTL, these approaches are uncertainty-agnostic:            equipped with a known set of skills/actions, denoted as A =
they treat LLM outputs as ground truth, ignoring inherent           {a1 , . . . , aA } (e.g., ‘take a picture’, ‘grab’, or ‘go to’) operat-
model uncertainty and confidence, and consequently provide          ing in an environment Ω = {l1 , . . . , lM } that contains M > 0
no guarantees on translation correctness.                           semantic objects and regions (called, hereafter, landmarks) lj .
   (ii) NL-based Planners: Related to our work are NL-              Each landmark lj is determined by its position and its semantic
based planners that bypass the construction of LTL formulas         label (e.g., ‘box’, ‘car’, ‘kitchen’). The robot’s skills can be
altogether. These approaches use LLMs or Vision-Language            applied to lj (e.g., ‘go to lj ’ or ‘grab lj ’).
Models to map NL instructions directly to control or ac-               Natural Language Tasks: The robot is assigned a task
tion sequences [43]–[52]. While such methods demonstrate            ξ, expressed in natural language (NL), which may comprise
strong empirical performance, they similarly lack guarantees        multiple sub-tasks. The task ξ is grounded in the robot skill
on task success or mission-level correctness. Moreover, their       set A and a subset of the environment Ω, meaning it can
end-to-end nature offers limited interpretability. In contrast,     be accomplished by executing a sequence of actions selected
translation-based frameworks, including ours, can be modu-          from A on some of the landmarks within Ω; see Ex. II.1. To
larly composed with existing planning and control stacks [2]–       formalize this, we consider a distribution D over translation
                                                                                                                                                3



scenarios σi = {ξi , Ai }, where ξi is defined over an unknown
environment Ωi ; see also Remark II.2. The subscript i is used
to emphasize that the NL-encoded task and the robot skills
can vary across scenarios. When it is clear from the context,
we drop the dependence on i. Note that D is unknown but we
assume that we can sample i.i.d. scenarios from it.
   Linear Temporal Logic: LTL is a formal language that
comprises a set of atomic propositions (APs) π (i.e., Boolean
variables), collected in a set denoted by AP, Boolean op-
erators, (i.e., conjunction ∧, and negation ¬), and temporal
operators, such as always □, eventually ♢, and until U. We
focus on LTL-encoded robot tasks defined over APs grounded
in the robot’s skill set Ai and environment Ωi . Specifically,
we consider APs that are true when a skill ai (e.g., ‘pick up’)
is applied to a landmark lj (e.g., ‘package’); see also Remark
II.2. These LTL formulas ϕ are satisfied by robot plans τ ,
which are sequences of robot states and corresponding actions.
A formal presentation of the syntax and semantics of LTL, as
                                                                  Fig. 2. Overview of ConformalNL2LTL. Given a translation scenario σ =
well as robot plans satisfying LTL tasks can be found in [1],     {ξ, A} and a threshold α, a sequence of QA problems are solved by an LLM.
[22]; designing plans τ is out of the scope of this work.         At every step, if the LLM is uncertain about its response, it asks for help from
   Problem Statement: Our goal is to design a probabilisti-       an auxiliary LLM, and a user, if required. If the response to a QA problem is
                                                                  ’/’, then the LTL formula ϕ is built by concatenating the responses generated
cally correct translation algorithm that converts NL instruc-     at every QA step.
tions ξi , contained in translation scenarios σi = {ξi , Ai }
sampled from a distribution D, into semantically equivalent
LTL-encoded tasks ϕi , with probability at least (1 − α) over     from D. Similarly, D does not depend on a predefined set of
scenarios drawn from D, for a user-specified α ∈ (0, 1). In       APs for constructing ϕ. Instead, the translation algorithm is
other words, the desired translation success rate over D is at    tasked with inferring the set AP from ξ and the provided
least (1 − α) · 100%. Given a scenario σi = {ξi , Ai }, we say    skill set A. In practice, this means that users only need to
that an LTL formula ϕi is semantically equivalent to ξi if any    specify the skill set A of the platform and the NL instructions
plan τ satisfying ϕi also satisfies ξi , and vice versa. When     ξ, making our algorithm environment-agnostic. This enhances
multiple LTL formulas are semantically equivalent to ξi , our     suitability for open-world task settings and also improves
goal is to compute one such formula. The problem that the         usability by eliminating the need to manually define APs or
paper addresses can be formally stated as follows:                environments for each new scenario σ.
Problem 1. Design a translation algorithm that, given a
                                                                     III. T RANSLATING NATURAL L ANGUAGE TO L INEAR
translation scenario σ = {ξ, A} sampled from an unknown
                                                                     T EMPORAL L OGIC WITH C ORRECTNESS G UARANTEES
distribution D, generates an LTL formula ϕ such that
                                                                     In this section, we present ConformalNL2LTL, our proposed
                   Pσ∼D (ϕ ≡ ξ) ≥ 1 − α,                    (1)   translation framework to address Problem 1. In Section III-A,
                                                                  we provide an overview of the framework and highlight
for a user-specified threshold 1 − α ∈ (0, 1) (where ≡ stands     its key ideas. Then, in Section III-B, we show how the
for semantic equivalence).                                        translation problem can be formulated as a sequence of ques-
Example II.1 (NL-to-LTL). Consider an example of a mobile         tion–answering (QA) tasks, which are solved by a pre-trained
manipulator with action space A = {move to, pick up, put          LLM in an uncertainty-aware manner via conformal prediction
down}, and NL task ξ = ‘Pick up the red box and place             (CP). In Section III-C, we explain how ConformalNL2LTL
it in storage’. Our proposed algorithm will infer that the        manages high-uncertainty cases, flagged by CP, by querying
corresponding LTL formula should be defined over three APs:       an auxiliary LLM and, if needed, deferring to a user. Finally,
(i) p red box which is true if the ‘red box’ was ‘picked up’      in Section III-D, we discuss how CP is used to quantify the
by the robot; (ii) storage which is true if the robot is in       uncertainty of the LLMs involved in solving these QA tasks.
the ‘storage’ area; and (iii) pd which is true if the carried     A. Overview of ConformalNL2LTL
object is placed. This will result in the following LTL formula
                                                                     In this section, we provide an overview of Confor-
ϕ = ♢(p red box ∧ ♢(storage ∧ pd)) which is satisfied when
                                                                  malNL2LTL summarized also in Alg. 1 and Figure 2. Con-
p red box becomes true first, followed by satisfaction of both
                                                                  sider a translation scenario σ = {ξ, A} drawn from D. A
storage and pd.
                                                                  key idea of ConformalNL2LTL is to frame the translation
Remark II.2 (Distribution D). Note that D is defined over σ,      process as a sequence of interdependent question-answering
and not on specific environment instantiations Ω. Instead, the    (QA) problems, each solved collaboratively by two pre-trained
randomness of Ω is implicitly accounted for when sampling the     LLMs, referred to here as the primary and auxiliary LLMs,
task ξ. This means that Ω may vary across NL tasks ξi sampled     denoted by ψp and ψaux , respectively. The answers to these
                                                                                                                                                              4



Algorithm 1 ConformalNL2LTL                                                          Algorithm 2 GetResp
 1: Input: NL Task ξ; Coverage level 1 − α; Primary LLM ψp ; Auxiliary                1: Input: LLM ψ, prompt ℓ(k), m, semantic threshold ζ
    LLM ψaux , NCS quantile q̄, semantic threshold ζ                                  2: Initialize Ŝ ψ (k) = ∅
 2: Initialize k = 1 and prompt ℓ(1) with formula ϕ(0) = ∅                            3: for i=1 to m do
 3: while ‘/’̸∈ ϕ(k − 1) do                                                           4:      Ŝ ψ (k) = Ŝ ψ (k) ∪ {Prompt(ψ,ℓ(k))}
 4:     C(ℓ(k), ψp ) = PredSet(ℓ(k), ψp , q̄, ζ) (See Alg. 3)                         5: S (k) = Prune(Ŝ ψ (k))
                                                                                           ψ
 5:     if |C(ℓ(k), ψp )| > 1 then                                                    6: for s(k) ∈ S ψ (k) do
 6:          C(ℓ(k), ψaux ) = PredSet(ℓ(k), ψaux , q̄, ζ) (See Alg. 3)                7:      Calculate F ψ (s(k)|S(k)) as in (2)
 7:          Cinter (ℓ(k)) = C(ℓ(k), ψp ) ∩ C(ℓ(k), ψaux )
 8:          if |Cinter (ℓ(k))| > 1 then                                              8: for s(i) (k), s(j) (k) ∈ S ψ (k) do
 9:              Ask human operator to select s(k) from Cinter (ℓ(k))                 9:      if S.S(s(i) (k), s(j) (k)) ≥ ζ then
10:          else if Cinter (ℓ(k)) = ∅ or ‘correct response ̸∈ Cinter (ℓ(k))’ then   10:           l = argminl∈{i,j} F ψ (s(l) (k))
11:               Halt and declare translation as failed                             11:           o = {i, j} \ {l}
12:          else                                                                    12:           s(l) (k) ← s(o) (k)
13:               Pick the (unique) decision s(k) ∈ Cinter (ℓ(k))                    13: S̄ ψ (k) = Unique(S ψ (k))
14:      else if C(ℓ(k), ψp ) = ∅ then                                               14: for s̄(k) ∈ S̄(k) do
15:          Halt and declare translation as failed                                  15:      Calculate F ψ (s̄(k)|S(k)) as in (2)
16:      else                                                                        16: Output: [S̄ ψ (k), F ψ (k)]
17:          Pick the (unique) decision s(k) ∈ C(ℓ(k), ψp )
18:      Update ϕ(k) = ϕ(k − 1) + s(k)
19:      Construct ℓ(k + 1) using ℓ(k) and ϕ(k)
20:      Update k = k + 1                                                            followed by how it is used to solicit a response s(k) from the
21: Output: LTL formula ϕ                                                            primary model in an uncertainty-aware manner using CP.
                                                                                        Prompt Structure: The prompt ℓ(k) used for querying the
                                                                                     primary LLM at every step k has the following structure: (a)
                                                                                     Translation rules that defines: (i) the list of all valid temporal
                                                                                     and logical operators; (ii) rules for generating APs that are
                                                                                     grounded on the robot skill-set A and the landmarks mentioned
                                                                                     in the task ξ; and (iii) general rules that the LLM should follow
                                                                                     during the translation process (e.g., about the ending operator
                                                                                     ’/’). Part (a) prompts the LLM to generate an operator or an
                                                                                     AP using the rules (i)-(iii) towards constructing a formula that
                                                                                     is semantically equivalent to ξ. (b) Response structure with
                                                                                     n-shot examples describing the desired structure of the LLM
                                                                                     output at each step k, where n depends on the language model;
                                                                                     (c) Task description of an NL task ξ that needs to be converted
                                                                                     into an LTL formula; (d) Current status describing the formula
Fig. 3. Example of the constructed prompt for GPT-4o. This prompt refers             ϕ(k − 1) that has been built up to step k − 1 and the current
to k = 1 meaning that no response has been selected yet and the formula
constructed so far is therefore ‘empty’.                                             step indicator k. An example of a prompt is shown in Fig. 3.
                                                                                        Initial Prompt Construction: Given a scenario σ =
QA problems collectively form the LTL formula. Specifically,                         {ξ, A}, the initial prompt ℓ(1) is manually constructed with
at each iteration k, a QA problem is formulated. The question                        the initial formula in part (d) being empty [line 2, Alg. 1].
incorporates information about the NL task ξ, the set of robot                       Parts (a)-(c) in ℓ(k) are the same for all k ≥ 1. Part (d) is
skills A, and the responses from previous iterations (i.e., the                      updated at every step k once a response s(k) is generated;
partially constructed LTL formula). This textual information,                        this will be discussed later in the text.
denoted by ℓ(k), is provided as a prompt to the primary LLM,                            Generating Confidence-aware Responses: Next, we de-
which is tasked with generating an answer s(k) that is either                        scribe how to obtain a response s(k) corresponding to ℓ(k).
a temporal/logical operator or an AP. If the primary LLM is                          A straightforward approach is to query the primary LLM
not sufficiently confident about the correctness of its response,                    once and record its response; we denote this process by
according to the user-defined threshold 1 − α introduced in                          s(k) = Prompt(ψp , ℓ(k)). However, this single-query ap-
Problem 1, help is requested first from the auxiliary LLM                            proach is uncertainty-agnostic, as it does not capture the
and, if necessary, from a user. This coordination among the                          model’s confidence in its predictions. To address this, inspired
LLMs and the user is enabled via CP (applied as shown                                by [38], [39], we adopt a sampling-based approach: the model
in Alg. 2 and 3). This iterative process continues until an                          is queried multiple times using Prompt(ψp , ℓ(k)), and the
ending operator, denoted by ‘/’, is generated at some step                           frequency of each unique response is used as a coarse-grained
H, indicating that the LTL formula ϕ = s(1)s(2) . . . s(H)                           measure of uncertainty. In what follows, we describe this
has been fully constructed. In the following subsections, we                         process in detail; see Alg. 2 and Ex III.1.1
describe the translation process in detail.                                             Querying the model and rule-based pruning: We first query
                                                                                     the model ψp m times with the same prompt ℓ(k), and
B. Incremental Translation: Querying the Primary LLM                                 construct the set Ŝ ψp (k) = {ŝ(i) (k)}m   i=1 [line 4, Alg. 2],

  In what follows, we describe the role of the primary LLM.                            1 Note that the output of Alg. 2 will be used later in Alg. 3 to generate
Specifically, we discuss how the prompt ℓ(k) is constructed,                         prediction sets that are crucial for ConformalNL2LTL.
                                                                                                                                              5



where ŝ(i) (k) is the i-th response of the LLM, i.e., ŝ(i) (k) =          every remaining response in the set is semantically distinct
Prompt(ψp , ℓ(k)). To ensure adherence to the constraints                   [lines 8-12, Alg. 2].
specified in part (a) of the prompt ℓ(k) (see Fig. 3), out of all              We define S̄ ψp (k) ⊆ S ψp (k) as the set of unique responses
the m responses, we filter out any responses that: (i) include              in S ψp (k) using the Unique function [line 13, Alg. 2].
an invalid operator that is not part of the predefined set; (ii)            For each response s̄ ∈ S̄ ψp (k), we re-compute the scores
APs that violate the rules set up in (a); and (iii) contains                F (s̄|ℓ(k), mk , S ψp (k)), using (2), to account for the above-
multiple operators or APs [line 5, Alg. 2]. This yields a set               mentioned replacements of responses in S ψp (k) due to se-
S ψp (k) ⊆ Ŝ ψp (k), such that S ψp (k) = {s(i) (k)}m k
                                                     i=1 , where            mantic similarities [line 15, Alg. 2]. Hereafter, for brevity, we
mk denotes the number of valid responses. This process is                   denote the above response extraction process with frequency
denoted by S ψp (k) = Prune(Ŝ ψp (k)).                                     scores as [S̄ ψp , F ψp ] = GetResp(ψp , ℓ(k), m, ζ); see Ex III.1.
   Frequency as a measure of uncertainty: We compute the                       Selecting a Response: Using these scores modeling the
frequency of each distinct response s ∈ S ψp (k) as follows                 confidence of ψp , a straightforward approach to selecting
[lines 6-7, Alg. 2]:                                                        the response s(k), for a given prompt ℓ(k) is choosing the
                                                                            response s̄ ∈ S̄ ψp (k) with the highest confidence score, i.e.,
                               1          X
 F (s|ℓ(k), mk , S ψp (k)) =                            1(s(i) (k) = s),             s(k) = arg max F (s̄|ℓ(k), mk , S ψp (k)).            (3)
                               mk                                                                 s̄∈S̄ ψp (k)
                                    s(i) (k)∈S ψp (k)
                                                                      (2)   However, these scores do not represent the calibrated con-
                                                                            fidence [42]. Thus, a much-preferred approach would be to
where F (s | ℓ(k), mk , S ψp (k)) ∈ (0, 1] represents the fraction          generate a set of responses (called, hereafter, prediction set),
of valid responses equal to s, i.e., the number of times s                  denoted by C(ℓ(k), ψp ) that contains the ground truth response
was generated divided by the total number of valid responses                with a user-specified confidence (that depends on the threshold
mk > 0. Hereafter, for simplicity, when it is clear from the                1−α introduced in Problem 1) [line 4, Alg. 1]. In what follows,
context, we abbreviate F (s|ℓ(k), mk , S ψp (k)) as F ψp (s|S(k)).          we assume the prediction sets are provided. We defer their
Observe that every response in S ψp (k) has a positive fre-                 construction to Section III-D, but we emphasize that they are
quency. For any other response s that is not among the mk                   critical to achieving the desired 1 − α translation accuracy.
generated responses (and thus does not belong to S ψp (k)),                    Given C(ℓ(k), ψp ), we select response s(k) as follows. If
we set F ψp (s|S(k)) = 0. Note that F ψp (s|S(k)) = 0 for any               C(ℓ(k), ψp ) is a singleton (i.e., |C(ℓ(k), ψp )| = 1), then we
response when all m responses are invalid, i.e. S ψp (k) = ∅ (or,           select the response i.e., a temporal/logical operator or an AP,
equivalently, mk = 0). We use the frequency F ψp (s|S(k)) as                included in C(ℓ(k), ψp ) as it contributes to the translation
the proxy for the confidence of the model ψp on each response               process with high confidence [line 17, Alg. 1]. If however,
s ∈ S ψp (k) since higher response frequency correlates with                the prediction set comes out empty due to no valid responses
greater model confidence [38], [65]. This enables our method                from ψp , the translation process is terminated [line 15, Alg, 1].
to work seamlessly with LLMs that do not allow users to have                Otherwise, if |C(ℓ(k), ψp )| > 1 the primary model seeks helps
access to logits modeling confidence (e.g., GPT 4) [39]. We                 from the auxiliary model ψaux to select s(k). If the primary
emphasize that more fine-grained measures of uncertainty can                and the auxiliary model cannot jointly provide a response
also be employed, as explored in [38], [40].                                s(k), then help from a user is requested who may either select
   Merging Semantically Similar Responses: It is possible for               s(k) from a set of responses or may terminate the translation
two textually different responses, s(i) (k) and s(j) (k), to con-           process in case that set does not contain the correct response.
vey the same semantic meaning. This issue arises particularly               This help module, is presented in the Section III-C.
in responses involving APs, which as discussed in Section II,                  Updating the Formula and the Prompt: Once s(k) is
capture the application of a robot action on a landmark, where              selected by the primary model or through the help module,
multiple synonymous terms (e.g., ‘vehicle’ and ‘car’) may be                the formula is updated as ϕ(k) = ϕ(k − 1) + s(k), where with
used for the same landmark. To address this, inspired by [39],              slight abuse of notation, the ‘+’ denotes concatenation of texts
we refine the response frequencies by grouping semantically                 [line 18, Alg. 1]. In this iterative update, ϕ(0) is an ‘empty’
similar responses and treating them as a single entity; this                formula used in the construction of the initial prompt ℓ(1). We
essentially results in summing their frequencies.                           then update the iteration index [line 20, Alg. 1], for which the
                                                                            prompt, ℓ(k + 1), is constructed by replacing part (d) of ℓ(k)
   Formally, consider any two responses s(i) (k), s(j) (k) ∈
  ψp                                                                        with ϕ(k) [line 19, Alg. 1]; see also Fig. 3. This procedure
S (k) that are both APs. If their semantic similarity, com-
                                                                            is repeated sequentially until, at some time step k = H, the
puted by a function S.S [line 9, Alg. 2], exceeds a predefined
                                                                            ending operator ‘/’ is generated, indicating that the formula
threshold ζ, we consider the responses semantically equivalent.
                                                                            has been fully constructed as ϕ = s(1) . . . s(H). In Section IV,
Semantic similarity can be computed, e.g., using cosine simi-
                                                                            we show that this algorithm achieves user-defined translation
larity; our implementation of S.S is discussed in Section V.
                                                                            success rates 1 − α addressing Problem 1.
When two APs are deemed semantically equivalent, then we
retain the more frequent response-i.e., if F ψp (s(i) (k)|S(k)) ≥           Example III.1 (Extracting Responses and Frequency Scores).
F ψp (s(j) (k)|S(k)), we replace s(j) (k) with s(i) (k) in the              Consider the NL task described in Example II.1. Suppose
set S ψp (k). This process is repeated for all distinct pairs               that at the beginning of iteration k = 3 of Alg. 1, the
s(i) (k), s(j) (k) ∈ S ψp (k), that are both APs, to ensure that            partially constructed LTL formula is ϕ(2) = ♢(, which
                                                                                                                                                        6



                                                                                     with user-specified confidence [line 6, Alg. 1]; we defer its
                                                                                     construction to Section III-D.
                                                                                       Next, we compute the intersection of the prediction sets
                                                                                     generated by the primary and the auxiliary model, i.e.,

                                                                                                Cinter (ℓ(k)) = C(ℓ(k), ψp ) ∩ C(ℓ(k), ψaux ).       (4)

Fig. 4. Overview of the help module triggered due to a non-singleton                 Thus, Cinter (ℓ(k)) contains only the responses that are shared
prediction set C(ℓ(k), ψp ). The auxiliary LLM is then queried to produce its        by both models [line 7, Alg. 1]. If |Cinter (ℓ(k))| = 1, then
own prediction set C(ℓ(k), ψaux ). If the intersection of the two sets, denoted by
Cinter (ℓ(k)) (see (4)), is non-singleton—signaling high uncertainty—a human         s(k) ∈ Cinter (ℓ(k)) is selected as the response [line 13, Alg.
operator is asked to select the correct option from the elements of Cinter (ℓ(k)).   1]. If |Cinter (ℓ(k))| > 1, the algorithm asks for help from a
                                                                                     human operator to select a response s(k) from the prediction
                                                                                     set Cinter (ℓ(k)) given the prompt ℓ(k) [line 9, Alg. 1]; see also
is used to construct the prompt ℓ(3). We illustrate how
                                                                                     Remark IV.3. If the prediction set Cinter (ℓ(k)) does not contain
the function GetResp(ψ, ℓ(3), m, ζ) computes a set of
                                                                                     any correct responses (e.g., if both ψp and ψaux generate the
semantically distinct responses along with their frequencies.
                                                                                     same incorrect response), or if Cinter (ℓ(k)) = ∅ (none of the mk
Let m = 5 and ζ = 0.75. Querying the LLM ψ using
                                                                                     generated responses are valid, i.e., S ψaux (k) = ∅, or C(ℓ(k), ψp )
Prompt(ψ, ℓ(3)) for m times [line 4, Alg. 2] produces
                                                                                     and C(ℓ(k), ψaux ) are mutually exclusive), the user can halt the
the following set of responses Ŝ ψ (3) ={p red box,
                                                                                     translation process, marking it as a ‘failure’ of our translation
p red box, p red package, p green bottle, pre%blocks}
                                                                                     algorithm [line 11, Alg. 1]; see Theorem IV.2.
after using the Prompt(ψ, ℓ(3)). The last entry ’pre%blocks’
is then pruned away using the Prune function, since                                  D. Constructing Prediction Sets using Conformal Prediction
it does not follow the rules requiring the action of
pick up to be of the form p lmk [line 5, Alg. 2].                                       In this section, we discuss how the prediction sets
This gives us the pruned set S ψ (3) ={p red box,                                    C(ℓ(k), ψp ) and C(ℓ(k), ψaux ), introduced in Section III-B and
p red box,       p red package,     p green bottle}.      The                        Section III-C respectively, are constructed using CP, based on a
frequencies of the unique responses are then computed                                user-defined translation success rate 1−α (see Problem 1). The
as F ψ (p red box|S(3)) = 0.5, F ψ (p red package|S(3)) =                            application of CP to a single LLM for single-step QA tasks in
0.25, and F ψ (p green bottle|S(3)) = 0.25 [line 7,                                  open vocabulary settings has been explored in [38], [40]. We
Alg. 2]. Next, pairwise semantic similarities are evaluated                          extend this approach to address multi-step interdependent QA
using S.S [line 9, Alg. 2]. In particular, consider the                              tasks in open-vocabulary settings, and the usage of more than
case where S.S(p red box, p red package) = 0.8 > ζ,                                  one LLM, both of which are essential for ConformalNL2LTL.
while similarities involving p green bottle are below the                            Background on CP is provided in Appendix A.
threshold ζ. Since p red box appears more frequently                                    We would like to note that we cannot apply the approach in
than p red package, p red package is replaced with                                   [38] to compute prediction sets C(ℓ(k), ψp ), and C(ℓ(k), ψaux )
p red box, yielding the following set of responses S ψ (3) =                         at each iteration k, as this violates the i.i.d. assumption re-
{p red box, p red box, p red box, p green bottle}.                                   quired to apply CP. The reason is that the prompt ℓ(k) depends
Applying the Unique function produces the set                                        on the previous prompt ℓ(k − 1), for all k ∈ {2, . . . , H},
S̄ ψ (3) = {p red box, p green bottle} [line 13, Alg. 2]. The                        by construction. Inspired by [42], [56], [61], we address this
updated frequencies are then F ψ (p red box|S(3)) = 0.75                             challenge by lifting the data to sequences. Specifically, D will
and F ψ (p green bottle|S(3)) = 0.25 [line 15, Alg. 2]. The                          be transformed into an equivalent distribution D′ over data
set S̄ ψ (3) together with these frequencies constitutes the                         sequences and, more precisely, sequences of prompts ℓ(k).
output of GetResp(ψ, ℓ(3), m, ζ).                                                    Then, we will apply CP by constructing (i) a calibration dataset
                                                                                     and (ii) designing a non-conformity score (NCS) modeling
                                                                                     the joint translation error of the primary and the auxiliary
                                                                                     models. Throughout this section, for simplicity of presentation,
C. Asking for Help: Querying the Auxiliary LLM and a User                            we assume that there exists a unique ground truth formula ϕ
                                                                                     corresponding to each scenario drawn from D; relaxing this
   In what follows, we present the help module that is in-                           assumption is discussed in Remark IV.3 and more formally
voked to handle high-uncertainty cases determined by the                             in Appendix B. Next, we discuss our approach. We start with
size of C(ℓ(k), ψp ); see Figure 4. As discussed earlier, when                       defining the distribution D′ used to lift translation scenarios
|C(ℓ(k), ψp )| > 1, our algorithm invokes the auxiliary LLM                          σ ∼ D to data sequences.
ψaux to address the k-th QA problem using a prompt of the                               Distribution D′ : Consider a translation scenario σ ∼ D
same structure and the same content in part (d) as ℓ(k), and the                     that is transformed into a sequence of prompts ℓ(k), i.e.,
same process applied to the primary model. For simplicity of                                          ℓ̄ = ℓ(1), . . . , ℓ(k), . . . , ℓ(H).         (5)
notation we use ℓ(k) to denote the prompt used to query either
model, since they have the same structure and are constructed                        Each prompt ℓ(k) in the sequence ℓ̄ has the structure defined
from the same input A, ξ, and ϕ(k − 1). This produces                                in III-B, where part (d) is constructed using the ground truth
a prediction set C(ℓ(k), ψaux ) that contains the ground truth                       responses of all steps up to k −1. The true response associated
                                                                                                                                                         7



with ℓ(k) is selected from the following set containing the                   Algorithm 3 PredSet
shared responses of both models:                                               1: Input: ℓ(k), LLM ψ, quantile q̄, semantic threshold ζ
                                                                               2: Initialize C(ℓ(k), ψ) = ∅
                        S̄(k) = S̄ ψp (k) ∩ S̄ ψaux (k),                (6)    3: [S̄ ψ (k), F ψ (k)]=GetResp(ψ, ℓ(k), m, ζ) (see Alg. 2)
                                                                               4: for s(k) ∈ S̄ ψ (k) do
              ψp          ψp
where [S̄ (k), F (k)] = GetResp(ψp , ℓ(k), m, ζ) and                           5:      if F ψ (s(k)) ≥ 1 − q̄ then
[S̄ ψaux (k), F ψaux (k)] = GetResp(ψaux , ℓ(k), m, ζ). As men-                6:          C(ℓ(k), ψ) = C(ℓ(k), ψ) ∪ {s(k)}
                                                                               7: Output: C(ℓ(k), ψ)
tioned in Section III-C, the prompts ℓ(k) used for the primary
and auxiliary LLMs have the same structure and the same
content in part (d), differing only in the specific content of
parts (a)-(c). If the true response is not contained in S̄(k) or              If for all k > 1, ℓtest (k) is constructed using the true response
if S̄(k) = ∅, then we type in the correct response. Thus, D                   for ℓtest (k − 1)—either chosen from S̄(k − 1) (defined in
is converted into an equivalent distribution D′ over sequences                (6)) or supplied by the user when S̄(k − 1) = ∅ or does
of prompts, where each sequence of prompts is constructed                     not contain the correct response—then the calibration and
by selecting the true responses at each decision step k as                    validation sequences are i.i.d. according to the distribution D′ .
                                                                              Then, CP generates a prediction set C(   ¯ ℓ̄test ) of LTL formulas,
discussed above. Note that the set S̄(k) depends on the
parameters m and ζ; consequently, D′ is conditioned on the                    containing the correct one, denoted by ϕtest , with probability
values of these parameters.                                                   greater than 1 − α, i.e.,
    Constructing a Calibration Dataset: As discussed earlier,                                                       ¯ ℓ̄test )) ≥ 1 − α.
                                                                                               Pℓ̄test ∼D′ (ϕtest ∈ C(                               (12)
applying CP requires a calibration dataset, which is con-
structed as follows. First, we sample D > 0 i.i.d. scenarios                  This prediction set is defined as follows:
{σi,calib }Di=1 from D and construct the following sequence of                               ¯ ℓ̄test ) = {ϕ | F̄ (ϕ | ℓ̄test ) ≥ 1 − q̄},
                                                                                             C(                                                      (13)
Hi prompts for each i ∈ {1, . . . , D}:
                   ℓ̄i,calib = ℓi,calib (1), . . . , ℓi,calib (Hi ),    (7)   where q̄ is the ⌈(D+1)(1−α)⌉
                                                                                                   D       empirical quantile of {r̄i }D    2
                                                                                                                                       i=1 . .
                                                                                 On-the-fly Construction of Prediction Sets: Notice that
where each prompt ℓi,calib (k) in ℓ̄i,calib has the structure defined          ¯ ℓ̄test ) in (13) is constructed after the entire sequence ℓ̄test =
                                                                              C(
in III-B, and contains the ground truth responses of all previous             ℓtest (1), . . . , ℓtest (Htest ) is obtained. However, at test time, we
steps in part (d). The corresponding true LTL formula is:                     do not see the entire sequence of prompts all at once; instead,
                   ϕi,calib = si,calib (1), . . . , si,calib (Hi ),     (8)   the contexts ℓtest (k) are revealed sequentially over the steps k.
                                                                                 Thus, we construct the prediction set C(       ¯ ℓ̄test ) on-the-fly and
where si,calib (k) refers to the correct response to ℓi,calib (k).
                                                                              incrementally, using only the current and past information;
This correct formula is constructed by computing S̄(k) defined
                                                                              see Alg. 3. At every step k ∈ {1, . . . , Htest }, we construct the
in (6). Then, we select the correct response from S̄(k). If
                                                                              following local prediction set.
the correct response in not in S̄(k), or if S̄(k) = ∅, we
type in the correct response; the frequency of that response                                  (
 0. This process
is                      D gives rise to a calibration set Mcal =              C(ℓtest (k)) =
                                                                                               C(ℓtest (k), ψp ),       if |C(ℓtest (k), ψp )| = 1
                                                                                                                                                   (14)
   ℓ̄i,calib , ϕi,calib i=1 where ℓ̄i,calib ∼ D′ by construction.                              Cinter (ℓtest (k)),      otherwise.
   Non-Conformity Score (NCS): Next, we define a non-
conformity score (NCS) modeling the worst-case translation                    In (14), Cinter (ℓtest (k)) is defined as in (4), i.e., Cinter (ℓtest (k)) =
error of the primary and the auxiliary models across all steps                C(ℓtest (k), ψp ) ∩ C(ℓtest (k), ψaux ), where C(ℓtest (k), ψp ) and
during the translation process. The NCS will be computed for                  C(ℓtest (k), ψaux ) are prediction sets produced by the primary
all calibration sequences. Specifically, we define the NCS of                 and the auxiliary models, respectively.
the i-th calibration sequence as                                                 Specifically, the set C(ℓtest (k), ψp ) is defined as follows
                         r̄i = 1 − F̄ (ϕi,calib |ℓ̄i,calib )            (9)    C(ℓtest (k), ψp )
                                                                                                     ψ
where                                                                             = {stest (k) ∈ S̄testp (k) | F ψp (stest (k)|S(k)) ≥ 1 − q̄}, (15)
F̄ (ϕi,calib |ℓ̄i,calib ) =             min   F ψ (si,calib (k)|S(k)), where S̄ ψp (k) is computed by [S̄ ψp (k), F ψp (k)] =
                              k∈{1,...,Hi },ψ∈{ψp ,ψaux }                            test                                   test
                                                                 (10) GetResp(ψp , ℓtest (k), m, ζ) [lines 3-6, Alg. 3].
where ϕi,calib is as defined in (8), and F ψ (si,calib (k)|S(k))           Similarly, the prediction set C(ℓtest (k), ψaux ) associated with
is the frequency of the correct response si,calib (k) computed the auxiliary model ψaux , is defined as
based on [S̄ ψ , F ψ ] = GetResp(ψ, ℓi,calib (k), m, ζ) for model
                                                                           C(ℓtest (k), ψaux )
ψ ∈ {ψp , ψaux }. In words, (10) computes the lowest frequency
                                                                                                 ψaux
assigned to the correct response across all translation steps k                = {stest (k) ∈ S̄test  (k) | F ψaux (stest (k)|S(k)) ≥ 1 − q̄},
and both models for the i-th calibration sequence.                                                                                               (16)
   Constructing Prediction Sets: Consider an unseen
                                                                          2 If the quantile value q̄ = 1, then the prediction set will contain all
test/validation scenario σtest ∼ D which is used to generate
                                                                       possible combinations of LLM token outputs, which is a very large finite
a sequence of prompts:                                                 set. In practice, this may happen if there exist multiple calibration sequences
                                                                              with NCS r̄i = 1 (i.e., at least one of the responses during the construction
                      ℓ̄test = ℓtest (1), . . . , ℓtest (Htest ).      (11)   of the ground truth formula was provided by a user) and a sufficiently low α.
                                                                                                                                                                8



           ψaux                                ψaux        ψaux
where S̄test    (k) is computed by [S̄test          (k), Ftest  (k)] =              Due to (21), we get that ϕ ∈ Cinter (ℓ̄test ). These implications
GetResp(ψaux , ℓtest (k), m, ζ) [line 3-6, Alg. 3]. The predic-                     also hold in the reverse direction: for any ϕ, if ϕ ∈ Cinter (ℓ̄test ),
tion sets C(ℓtest (k), ψp ) and C(ℓtest (k), ψaux ) are used in Section             then ϕ ∈ C(     ¯ ℓ̄test ), completing the proof of Part (A).
III-B to select s(k) [line 4-17, Alg. 1]. As it will be shown in                       Proof of Part (B): This result holds by construction of
Sec. IV, it holds that                                                              Cinter (ℓ̄test ) in (20) and C(   ˆ ℓ̄test ) in (18). Specifically, observe
                                       ˆ ℓ̄test )) ≥ 1 − α,                         that from (4) and (14),
                  Pℓ̄test ∼D′ (ϕtest ∈ C(                                  (17)
where                                                                                     C(ℓtest (k)) ⊇ Cinter (ℓtest (k)), ∀k ∈ {1, . . . , Htest }.      (22)

 ˆ ℓ̄test ) = C(ℓtest (1)) × · · · × C(ℓtest (k)) · · · × C(ℓtest (Htest )).
 C(                                                                                 Thus, since the set C(  ˆ ℓ̄test ) is defined in (18) as the cartesian
                                                                        (18)        product of all set C(ℓtest (k)) and, similarly, Cinter (ℓ̄test ) is
                                                                                    defined as the cartesian product of all sets Cinter (ℓtest (k)) in
Remark III.2 (Construction of Prediction Sets). We empha-                                         ˆ ℓ̄test ) ⊇ Cinter (ℓ̄test ) as a direct consequence of
                                                                                    (20), we get C(
size that construction of the sets C(ℓtest (k)) in (14) does not                    (22), completing the proof of Part (B).
require knowledge of the true responses during validation time.
However, if all prompts ℓtest (k) have been constructed using
                                                                                    Theorem IV.2 (Translation Success Rates). Consider trans-
the (unknown) true response at every step k, then (17) holds
                                                                                    lation scenarios σtest ∼ D and any choice of the number
(see Section IV). This result will be used in Section IV to
                                                                                    of queries m > 1 and semantic similarity threshold ζ > 0.
show that ConformalNL2LTL achieves user-specified 1 − α
                                                                                    Assume that m and ζ remain the same during calibration and
translation success rates (see Theorem IV.2 and its proof).
                                                                                    validation time. (a) If, for each scenario σtest ∼ D (where D is
                                                                                    unknown), the prediction sets C(ℓtest (k)), ∀k ∈ {1, . . . , Htest }
     IV. T RANSLATION S UCCESS R ATE G UARANTEES
                                                                                    are constructed on-the-fly with a coverage level of 1 − α, and
  In this section, we show that Alg. 1 achieves user-specified
                                                                                    the LLM asks for help from a benign user (who chooses the
1 − α translation success rates as required in Problem 1. To
                                                                                    ground truth response when it is found in C(ℓtest (k))) when
show this, we need to first state the following result.
                                                                                    |C(ℓtest (k))| > 1, then Pσ∼D (ϕ ≡ ξtest ) ≥ 1 − α, where ϕ is
Proposition IV.1. Consider a sequence of prompts ℓ̄test :=                          constructed as described in Section III-B. (b) If F̄ (ϕtest |ℓ̄test ),
ℓtest (1), . . . , ℓtest (Htest ) ∼ D′ , i.e., ℓtest (k) contains the true          used in (13), models true conditional probabilities, then the
response stest (k − 1), for all k ∈ {1, . . . , Htest }. It holds that              help rate is minimized among possible prediction schemes that
Pℓ̄test ∼D′ (ϕtest ∈ C(   ˆ ℓ̄test )) ≥ 1 − α, where C(ˆ ℓ̄test ) is as defined     achieve 1 − α translation success rates. 3 .
in (18).
                               ˆ ℓ̄test )) ≥ 1 − α, it suffices to
Proof. To show that P (ϕtest ∈ C(                                                   Proof. (a) To show this result, we first need to define three
show that,                                                                          Boolean variables C1 , C2 , and C3 modeling three mutually
                                                                                    exclusive and exhaustive events.
                             ¯ ℓ̄test ) ⊆ C(
                             C(           ˆ ℓ̄test )                       (19)        Variable C1 : The Boolean variable C1 is true if at any time
due to (12). To show (19), we first introduce the following set                     step k, all prediction sets C(ℓtest (k)) are singleton and contain
of LTL formulas:                                                                    the true response stest (k), for all k ∈ {1, . . . , Htest }, i.e.,
                                                                                                            H test h
   Cinter (ℓ̄test ) := Cinter (ℓtest (1)) × . . . × Cinter (ℓtest (Htest )), (20)                           ^                                 i
                                                                                                    C1 =             C ℓtest (k) = {stest (k)}              (23)
where Cinter (ℓtest (k)) = C(ℓtest (k), ψp ) ∩ C(ℓtest (k), ψaux ) as                                       k=1
defined in (4). In what follows, we will show that (A)                              Variable C2 : The Boolean variable C2 is true when all
 ¯ ℓ̄test ) = Cinter (ℓ̄test ) and (B) C(
C(                                       ˆ ℓ̄test ) ⊇ Cinter (ℓ̄test ). Combining   prediction sets contain the true response as in C1 but at least
(A) and (B) yields (19), completing the proof.                                      one prediction set is non-singleton, i.e.,
   Proof of Part (A): To prove (A), it suffices to show that for                                      H
                                          ¯ ℓ̄test ) ⇐⇒ ϕ ∈ Cinter (ℓ̄test ),                              test h                          
any LTL formula ϕ, if ϕ ∈ C(                                                                              ^                              i
                                                                                                 C2 =             stest (k) ∈ C ℓtest (k)
where ϕ = s(1) . . . s(k) . . . s(Htest ).
                       ¯ ℓ̄test ), due to (13),                                                                k=1
   For any ϕ ∈ C(                                                                                              H _test h                   i
                                                                                                                                      
       F̄ (ϕ|ℓ̄test ) ≥ 1 − q̄                                                                             ∧              |C ℓtest (k) | > 1                (24)
                                          ψ                                                                       k=1
⇐⇒                  min                  F (s(k)) ≥ 1 − q̄,
        k∈{1,...,Htest },ψ∈{ψp ,ψaux }
                                                                     Variable C3 : The Boolean variable C3 is true if at least one
⇐⇒ F ψ (s(k)) ≥ 1 − q̄, ∀k ∈ {1, . . . , Htest }, ∀ψ ∈ {ψp , ψaux }, of the prediction sets C(ℓtest (k)) does not contain the true
⇐⇒ {F ψp (s(k)) ≥ 1 − q̄} and {F ψaux (s(k)) ≥ 1 − q̄},              response, regardless of its cardinality, i.e.
       ∀k ∈ {1, . . . , Htest },
                                                                                                               H test h
⇐⇒ {s(k) ∈ C(ℓtest (k), ψp )} and {s(k) ∈ C(ℓtest (k), ψaux )},                                       C3 =
                                                                                                               _
                                                                                                                       stest (k) ∈
                                                                                                                                 / C ℓtest (k)
                                                                                                                                                 i
                                                                                                                                                            (25)
       ∀k ∈ {1, . . . , Htest },                                                                               k=1
⇐⇒ s(k) ∈ C(ℓtest (k), ψp ) ∩ C(ℓtest (k), ψaux ),                                     3 The help rate is defined as the percentage of steps k, where |C(ℓ (k))| >
                                                                                                                                                          test
       ∀k ∈ {1, . . . , Htest }.                                           (21)     1, during the construction of formulas corresponding to test scenarios σtest .
                                                                                                                                                   9



Observe that C3 is also true if for some k ∈ {1, . . . , Htest },                 CP depend on the accuracy of ranking the responses from
we have C(ℓtest (k)) = ∅, since in that case it trivially holds                   lowest to highest model confidence, and not on the actual
stest ̸∈ C(ℓtest (k)).                                                            values of the NCS. Even if the scores fail to approximate
   Observe that to prove (a), it suffices to show that P (C12 ) ≥                 this ranking, the marginal coverage still holds, albeit with
1 − α, where C12 = C1 ∨ C2 . This is because if either of these                   potentially excessively large prediction sets [37].
variables is true, then all prediction sets C(ℓtest (k)) contain the                 (b) This result holds directly due to Th. 1 in [66].
true response stest (k). Specifically, if all prediction sets are sin-
                                                                                  Remark IV.3 (Multiple Semantically Equivalent Formulas).
gleton (event C1 ), then, by construction, ConformalNL2LTL
                                                                                  The above results assume that D generates task scenarios with
selects stest (k) at every step k. If at least one prediction set is
                                                                                  a unique corresponding LTL formula. To relax this assumption,
non-singleton (event C2 ), the user will still select the correct
                                                                                  the following changes are made during calibration and test
response, under the assumption of benign users. In contrast,
                                                                                  time. (i) During calibration, among all LTL formulas that
if C3 is true, translation failure is unavoidable: if prediction
                                                                                  are semantically equivalent to each other and to a given
sets are non-singleton, the user halts the process; if they are
                                                                                  NL task, we select the one constructed by picking the cor-
singleton, the wrong response is selected. Thus it suffices to
                                                                                  rect response si,calib (k) ∈ S̄(k) with the highest frequency
bound the probability of C12 .
                                                                                  F ψp (si,calib (k)|S(k)) (among all other correct responses in
   In what follows, we show that P (C12 ) ≥ 1−α. Specifically,
                                                              ˆ ℓ̄test )) which   S̄(k)) at each step k as computed by ψp . If none of the
we will show that P (C12 ) = Pℓ̄test ∼D′ (ϕtest ∈ C(
                                                                                  responses generated is the ground truth, or valid, we type
is greater than 1 − α due to Proposition IV.1. Notice that
                       ˆ ℓ̄test )) is the probability that the ground truth       out the correct response with the frequency of the ground
Pℓ̄test ∼D′ (ϕtest ∈ C(
                                                                                  truth being F ψp (si,calib (k)|S(k)) = 0 in such cases. (ii) Given
response stest (k) belongs to C(ℓtest (k)) for all k (see (18)),
                                                                                  a validation NL task ξtest , the LTL formula ϕtest in both
assuming that all prompts ℓtest (k) include the ground truth
                                                                                  Proposition IV.1 and Theorem IV.2 refers to the formula that
responses of all previous steps till k − 1. We can therefore
                                   ˆ ℓ̄test )) and rewrite it as follows:         is semantically equivalent to ξtest and has been constructed
expand Pℓ̄test ∼D′ (ϕtest ∈ C(
                                                                                  exactly as in (i). The proofs of both Proposition IV.1 and
                         ˆ ℓ̄test )                                               Theorem IV.2 remain the same. (iii) When user help is required
                                   
  Pℓ̄test ∼D′ ϕtest ∈ C(
               H                                                                 at test time, the user selects the correct response among the
                   ^test 
                                                     k−1
                                                      ^       
                                                                                  ones in the prediction set with the highest frequency according
           =P              stest (k) ∈ C ℓtest (k) |       Br       ≥ 1 − α.
                 k=1                               r=1                            to ψp . Extension of the CP analysis provided in Section III-D
                                                                         (26)     to cases with multiple semantically equivalent formulas is
                                                                                  presented in Appendix B.
where Br is Boolean variable that is true if ℓtest (r) is con-
structed with the ground truth responses and the inequality                                      V. E XPERIMENTAL VALIDATION
holds due to Proposition IV.1.
   Now observe that C12 can be written as                                            In this section, we demonstrate the effectiveness of Con-
                                                                                  formalNL2LTL. Section V-A describes the experimental setup
                  H   test h                           
                     ^                               i                           and key implementation details. Section V-B empirically val-
            C12 =            stest (k) ∈ C ℓtest (k)      (27)                    idates the translation success rate guarantees of Thm. IV.2
                           k=1
                                                                                  and demonstrates the algorithm’s help rate. The benefits of
As discussed above, if C12 is true, it means that every                           using an auxiliary LLM as well as the effect of the number
time step k, ConformalNL2LTL selects the correct response.                        m of queries are shown in Section V-C. Comparisons against
This equivalently means that every prompt ℓtest (k) has been                      existing NL-to-LTL translators are provided in Section V-D.
constructed using the correct responses. And since, (27) is                       Section V-E compares the performance of ConformalNL2LTL,
a conjunction over all k ∈ {1, . . . , Htest }, it can be written                 incorporated with an existing planner [6], with NL-based
equivalently as                                                                   planners [43]. Comparisons show that our method outper-
             (H                                        )                          forms existing baselines as it can achieve desired translation
                test h
                ^                              k−1
                                                 ^    i
     C12 =             stest (k) ∈ C ℓtest (k) |    Br .    (28)                  performance while minimally asking for help from users.
                   k=1                               r=1                          Section V-F evaluates robustness of our method in out-of-
This equivalence holds because, at every step k, Br will                          distribution (OOD) NL tasks. While probabilistic guarantees
always be true ∀r ∈ {1, . . . , k − 1} as stest (r) ∈ C(ℓtest (r)),               of Thm. IV.2 may not hold in OOD settings, our framework
∀r ∈ {1, . . . , k − 1}. Comparing (28) and (26), we get                          achieves satisfactory success rates with very little user help.
that P (C12 ) ≥ 1 − α as required. We emphasize that the                          Demonstrations on NL-encoded navigation and mobile manip-
guarantee in Proposition IV.1, and, consequently, the guarantee                   ulation tasks using ground robots are included in [35], where
P (C12 ) ≥ 1 − α, holds for any fixed value of m and ζ. These                     ConformalNL2LTL is integrated with an existing LTL planner
parameters must remain unchanged during both calibration and                      [6]; see Fig. 1. All case studies use GPT-4o as the primary
validation; modifying them induces a distribution shift, since                    model and Deepseek v3 as the auxiliary model.
the induced distribution D′ is conditioned on them. However,
the exact value of m and ζ does not affect correctness of                         A. Setting Up Translation Scenarios for Robot Tasks
these guarantees as this only changes the granularity of of                         Robot & Environment: Our experiments focus on robot
the NCS [37]. Specifically, coverage guarantees provided by                       delivery and transportation tasks. The robot’s action space
                                                                                                                                                    10



is defined as A ={move to, pick up, put down, take a                 ‘box’ and ‘package’) as
picture} across all translation scenarios. The environments                                                            vi · v j
vary in terms of objects (e.g., crates, boxes, cars, bottles, and                      cos(s(i) (k), s(j) (k)) =                 ,               (29)
                                                                                                                      ∥vi ∥∥vj ∥
traffic cones) as well as regions of interest (e.g., kitchens,
warehouses, buildings, and parking lots) across our translation      where vi and vj are the vector representations of si (k)
scenarios. Since multiple objects of the same semantic label         and sj (k), respectively, computed using pre-trained LLM
(e.g., ‘box’) may exist in the environment, we assign unique         embeddings. The two APs are then merged if the cosine
identifiers (e.g., ‘box 1’, ‘box 2’) to distinguish them.            similarity exceeds a specified threshold ζ = 0.75. A higher
   Rules for APs: As discussed in Section III-B, part (a)            threshold requires greater semantic similarity for merging to
of each prompt informs the LLM about how APs should be               occur, influencing the granularity of the LLM’s confidence
formulated indicating when a robot action is applied to one (if      indirectly. For instance, if the threshold is set too high, multiple
any) of the available landmarks. In our setup, we require the        semantically similar responses may remain unmerged and their
LLM to generate APs in the following format (see Fig. 3): (i)        frequencies will not be aggregated to reflect the LLM’s overall
‘lmk X’ which is satisfied if the robot is near a landmark with      confidence in those responses. Conversely, thresholds that are
a semantic label ‘lmk’ and unique identifier X; (ii) ‘p lmk X’       too low may result in incorrectly treating semantically distinct
which is satisfied if the robot picks up the landmark with label     responses as similar, which can also lead to a poor estimation
‘lmk’ and unique identifier X; (iii) ‘pd’ that is satisfied if the   of the model’s confidence. However, as discussed earlier, the
robot puts down a carried object (i.e., opens its gripper); and      granularity of the LLM confidence estimates does not affect
(iv) ‘photo’ that is satisfied if the robot takes a photo. For       correctness of Thm. IV.2 but it may affect the help rates.
instance, the AP ‘p box 1’ is satisfied if the robot picks up           Evaluation Dataset & Distribution D: To evaluate our
box 1. We note that the identifier X is omitted in (i)–(ii)          method, we generated a dataset of 1, 000 translation scenarios
when the landmark in the NL task is not associated with              paired with their corresponding LTL formulas constructed as
a unique identifier. Also, observe that (i)–(ii) correspond to       discussed in Remark IV.3. We classify the considered scenarios
specific landmarks, whereas (iii)–(iv) do not. We emphasize          into three categories: easy, medium, and hard depending on the
that although we provide the LLM with the general structure          number of APs needed to construct the ground truth formula.
of APs, we do not supply a predefined list of APs; instead,          Easy scenarios include 365 NL tasks that would require at
our algorithm infers them directly from the NL task.                 most 2 APs in the LTL formula. An example of easy tasks is,
   Granularity of LLM’s confidence: As mentioned in                  ‘Never pick up crate 8’ which can be expressed in LTL as:
Sec. III-B, we query the model m times, which determines             ϕ = □¬crate 8. Medium scenarios include 440 NL tasks that
the granularity of the LLM’s confidence estimates for a given        would require 3 or 4 APs. For instance, consider the NL task
response (see the frequency score in (2)). Smaller values of         ‘Pick up bottle 3 from kitchen 2 but never enter living room
m yield a less accurate ranking of responses by confidence,          1’ that can be expressed using the following LTL formula:
which can lead to higher help rates; however, larger values          ϕ = ♢(kitchen 2 ∧ p bottle 3)∧□¬living room 1. Hard
of m increase the number of API calls and the associated             scenarios include 195 NL tasks that include more than 4 APs
costs. Thus, careful consideration is required when selecting        in the LTL formula. An example of such an NL task is ‘Avoid
m. We emphasize again that the value of m does not affect            going to region 5 until you reach street 4 while delivering pass
our translation success rate guarantees as stated in Thm. IV.2.      4 from house 4 to office 1’, which can be expressed using the
This is because CP depends on the accuracy of ranking of             LTL formula ¬region 5Ustreet 4∧♢(house 4∧♢(p pass 4∧
the responses from lowest to highest model confidence, and           ♢(office 1 ∧ pd))).4 Similar to related works that employ CP
not on the actual values of the NCS. Even if the scores              [42], [56], [61], we construct a distribution D (see Section
fail to approximate this ranking, the marginal coverage still        II) that samples uniformly the scenarios from this dataset.
holds, albeit with excessively large prediction sets. In all our     However, more complex distributions can be considered; we
experiments, we select m = 10 unless otherwise specified.            emphasize that CP and, consequently, our translation algorithm
   Eliminating Invalid APs: As soon as the LLM generates a           is agnostic to D.
response s(j) (k) at a step k of Alg. 1 (see Section III-B), we         Evaluation Metrics: (i) Success rate: the percentage of
first examine if that response is a logical/temporal operator.       translation scenarios that are successfully handled. (ii) User
If not, we examine its candidacy as an AP, i.e., if it satisfies        4 The LTL formula corresponding to this NL task can also be defined as
the rules mentioned above. APs that do not satisfy these rules       ϕ̄ = ¬region 5U (street 4 ∧ ♢(house 4 ∧ ♢(p pass 4 ∧ ♢(office 1 ∧ pd))))
are filtered out as discussed in Sec. III-B (e.g., ‘pick box 1’      depending on the interpretation of the ’while’ clause in the NL task. Note that
would be eliminated). Note that APs that do not have a               ϕ̄ is not semantically equivalent to ϕ and therefore does not fall under the
                                                                     case discussed in Remark IV.3. Such ambiguities can naturally arise in NL
numerical identifier are not filtered out (e.g., ‘p box’).           tasks. During the construction of our dataset, we selected ϕ as the ground truth
   Semantic Similarity: Let si (k), sj (k) be two valid APs that     formula, as it aligns with our intended task interpretation; consequently, ϕ̄ is
were generated as responses at step k. Before checking their         treated as an incorrect option. These subjective interpretations of ambiguous
                                                                     NL instructions are implicitly captured by the underlying distribution D. A
semantic similarity (see (29)), we first check if their numerical    different distribution D̄ could instead assign ϕ̄ as the ground truth. If the user
identifiers match. If not (e.g., ‘box 1’ and ‘package 2’), we        who provides the calibration sequences differs from the user at deployment
set their semantic similarity to zero as these APs refer to          time, such differences in how ambiguous instructions are interpreted can
                                                                     lead to distribution shifts that may compromise translation performance. We
two different landmarks. Otherwise, we proceed with the              emphasize that our translation success guarantees hold with respect to the
computation of the cosine similarity of their textual parts (e.g.,   chosen distribution D.
                                                                                                                                      11



                            TABLE I                                  C. Effect of the Auxiliary LLM and Number m of Queries
     E MPIRICAL T RANSLATION S UCCESS R ATES AND H ELP R ATES
                                                                        In what follows, we empirically demonstrate the help-rate
                     1−α        Empirical       Help Rate   Hf
     Framework                                                       benefits gained by incorporating an auxiliary model into our
                      (%)    Success Rate (%)      (%)      (%)
                      95           94.44            0           0
                                                                     translation framework. We repeat the experiments of Section
 ConformalNL2LTL                                                     V-B using the exact same calibration and validation data, but
                      97           96.77          0.279     2.5
 w/ auxiliary LLM                                                    with the auxiliary model entirely removed from both calibra-
                      99           99.24          0.378         4
                                                                     tion and test-time operation. In this setting, during calibration,
                      95           95.33          3.41          30   the NCS in (9) is computed solely using the primary model
 ConformalNL2LTL
 w/o auxiliary LLM
                      97            97            4.03          36   ψp , and at test time the prediction set in (14) simplifies to
                      99           98.2           7.43      36.5     C(ℓ(k)) = C(ℓ(k), ψp ) for all k. As a consequence, whenever
                                                                     the primary model is uncertain—i.e., when |C(ℓ(k))| > 1—the
help rate: the percentage of responses s(k) that were gen-           algorithm must directly request help from a user. Following the
erated using human help across all validation scenarios. (iii)       same reasoning as in Section IV, this framework still achieves
Help frequency across scenarios: the percentage of translation       the target translation success rate 1−α. However, as expected,
scenarios in which user help was required at least once during       removing the auxiliary model may substantially increase both
formula construction, denoted by Hf .                                the user help rate and the help frequency Hf .
                                                                        The performance of ConformalNL2LTL without an auxil-
                                                                     iary model is reported in the second row of Table I. When
                                                                     1 − α is 95%, 97%, and 99%, the translation success rates are
B. Empirical Evaluation in In-Distribution Settings                  95.33%, 97%, and 98.2%, respectively, which are consistent
   In this section, we empirically validate that Confor-             with Th. IV.2, confirming that the auxiliary model does not
malNL2LTL achieves user-defined translation success rates,           affect the theoretical success rate guarantees. In contrast, the
as guaranteed by Th. IV.2. To demonstrate this, we repeat the        corresponding user help rates rise to 3.41%, 4.03%, and
following process for 1−α ∈ {95%, 97%, 99%}. We draw 220             7.43%, which are significantly higher than those obtained
scenarios from D, where 200 of them are used for calibration         when using an auxiliary model (see Section V-B). Likewise,
and the rest of them are used as test scenarios. For each test       Hf increases significantly to 30%, 36%, and 36.54% for
scenario, Alg. 1 returns an LTL formula and then we manually         1 − α = 95%, 97%, 99%, respectively. These empirical results
check if it is the correct one. We compute the ratio of how          highlight the primary role of the auxiliary LLM which is to
many of the generated formulas are the correct ones. We repeat       reduce the uncertainty in selecting response s(k). This in turn
this 10 times. The average ratio across all experiments is the       decreases both the overall user help rate and the fraction of
(empirical) translation success rate.                                formulas requiring user intervention.
                                                                        In addition, to show the influence of m on the help rate,
   The results are summarized in the first row of Table I.
                                                                     we also ran experiments of ConformalNL2LTL without the
Observe that the translation rates are 94.44%, 96.77%, and
                                                                     auxiliary model for 1 − α = 95% and m = 5 (recall that
99.24% for 1 − α = 95%, 97% and 99% respectively, val-
                                                                     all previous experiments used m = 10). We observed that the
idating Th. IV.2. Minor deviations, are expected due to the
                                                                     user help rate increased from 3.41% to 4.71% and that Hf
finiteness of the calibration and validation sets and the number
                                                                     increased from 30% to 58%. The empirical translation rate
of trials; see also [37]. The user help rates were recorded as
                                                                     is 95.15% validating Thm. IV.2. The increase in help rates
0%, 0.279% and 0.378% for 1 − α = 95%, 97% and 99%
                                                                     and Hf is expected as lower m results in a more inaccurate
respectively. As expected, higher values for 1 − α increase the
                                                                     estimate of the LLM’s confidence as discussed in Section V-A.
size of the prediction sets and, consequently, the likelihood
that ConformalNL2LTL requests user assistance. The help fre-
quency Hf , i.e., the fraction of translation scenarios requiring    D. Comparative Evaluations against Translation Baselines
user help at least once, is 0%, 2.5% and 4%, when 1 − α was             We compare ConformalNL2LTL against three baselines: (A)
95%, 97% and 99% respectively. The increasing trend of Hf            an uncertainty-agnostic (UA) variant of ConformalNL2LTL;
is also expected as higher 1−α values require more help. This        (B) Lang2LTL [30]; and (C) nl2spec [31]; Below, we provide
monotonic increase is again expected, but note that both the         an overview of these baselines followed by a discussion on
help rates and Hf remain sufficiently low.                           how we configured them to ensure fair comparisons.
   Most mistakes made by the LLMs stem from incorrect                   (A) The UA version of ConformalNL2LTL, called UA-
placement of parentheses. For example, for the following NL          NL2LTL, completely removes CP, making decisions solely
task ‘Go to monument 3, take a picture and stay there’,              based on the mis-calibrated confidence scores of the primary
the primary model generated the formula ♢(monument 3                 LLM. Thus, at every step k, UA-NL2LTL picks the response
∧ photo)∧□ monument 3, instead of ♢(monument 3 ∧                     s(k) = arg maxs̄∈S̄ ψp (k) F (s̄|ℓ(k), mk , S ψp (k)). As a result,
photo∧□monument 3). However, this problem can be by-                 this baseline never asks for help, neither from the auxiliary
passed by using prefix LTL formula, although it would require        LLM, nor from the user.
rewriting the prompts accordingly. Another common error was             (B) Lang2LTL employs a modular translation pipeline con-
the generation of nonsensical APs that still conformed to the        sisting of: (a) an expression recognition module that extracts
AP generation rules.                                                 landmark-related substrings from the NL task using LLMs; (b)
                                                                                                                                       12



                            TABLE II                                     UA-NL2LTL tends to outperform the baselines. However,
            T RANSLATION S UCCESS R ATES OF BASELINES                    the latter may be a case- and implementation-specific result.
                                         Success Rates                   In addition, we observe that the performance of Lang2LTL
                    UA-NL2LTL               87.4%                        dropped significantly when operating with its original few shot
               Lang2LTL w/ Few-Shot         82.87%                       examples justifying the modification (iii) mentioned earlier.
               Lang2LTL w/o Few-Shot        53.53%
                      nl2spec               73.16%                       Finally, we emphasize that ConformalNL2LTL surpasses all
                      CMAS                   88%                         these baselines in terms of translation success rates, as it can
                                                                         achieve user-specified 1 − α success levels while requiring
a grounding module that maps each entity to an AP; and (c) a
                                                                         minimal user intervention (see Table I).
lifted translation module that substitutes APs with placeholder
symbols before generating the LTL formula using LLMs.
                                                                         E. Comparative Evaluations against NL-based Planners
   (C) nl2spec uses components from ‘chain-of-thought’
prompting to allow the LLM to reason about its response to                  We compare ConformalNL2LTL against CMAS, an NL-
raise its own accuracy. The framework first generates sub-               based planner that maps NL instructions directly to robot plans
translations by using the LLM which are then edited or                   without generating intermediate LTL formulas [43]. Next, we
removed by a user, who is also allowed to add subtranslations5 .         discuss how CMAS and ConformalNL2LTL are configured.
A sub-translation provides context for proper formalization by              CMAS is developed for teams of N robots, but we evaluate
providing translation examples for part of the NL task. The              it in a single-robot setting (N = 1). The output of CMAS
LLM is then queried M times using the subtranslations and                is a robot plan defined as a sequence of actions generated to
the prompt, with the user providing help in the loop. The                satisfy the input NL instructions. To ensure fair comparisons,
translation with the highest confidence among the M responses            we provide CMAS with (i) an action space that shares the
is displayed, along with alternative translations.                       same structure as the AP recognition component of Confor-
   To ensure fair comparisons, we have set up the baselines              malNL2LTL, and (ii) the same few-shot examples included
as follows: (i) UA-NL2LTL is set up using the primary                    in our prompt, i.e., the same NL tasks accompanied by the
model of ConformalNL2LTL (i.e., GPT 4o). UA-NL2LTL                       corresponding true plan. Our definition of the action space in
and ConformalNL2LTL share exactly the same prompts to                    (i) ensures that the plans generated by CMAS are sequences
query the primary model. (ii) We provide the translation rules           of APs that need to be satisfied. As a result, both CMAS and
in part (a) of our prompt (see Fig 3) to Lang2LTL, and                   ConformalNL2LTL reason at the same level of abstraction,
nl2spec such that all methods share the same AP recognition              avoiding unfair comparisons such as requiring CMAS to pro-
structure with ConformalNL2LTL. (iii) We also augmented                  duce lower-level outputs (e.g., waypoints). ConformalNL2LTL
the list of few-shot examples provided in Lang2LTL and                   can be paired with any complete LTL planner to convert the
nl2spec with ours. (iv) We do not allow the user to add,                 generated LTL formulas into robot plans such as [6].
edit or remove sub-translations for nl2spec as this would                   We then evaluate the plan success rate, defined as the
lead to an unfair comparison with other baselines, which                 proportion of plans successfully accomplish the specified NL
do not get help from the user. Moreover, nl2spec lacks a                 task. Notice that the plan success rate of our method (Con-
mechanism to detect when assistance is needed and there-                 formalNL2LTL & LTL planner) is identical to the translation
fore requires user involvement in all translation scenarios in           success rate of ConformalNL2LTL given that the employed
order to add, remove, or edit sub-translations. In contrast,             planner, proposed in [6], is correct and complete. The same
ConformalNL2LTL explicitly reasons about when assistance is              applies to all translation baselines considered in Section V-D.
required to achieve a user-defined translation success rate. Ad-         The plan success rates for CMAS was 88% over the 182 NL
ditionally, the nature of user assistance differs fundamentally          tasks used in Section V-D. Note this success rate is comparable
between the two approaches: nl2spec relies on user-specified             to the one that would have been achieved by integrating UA-
sub-translations, whereas ConformalNL2LTL only requests                  NL2LTL with an LTL planner (87.4%). Finally, we emphasize
the user to select among candidate responses at specific QA              that, as in Section V-D, our framework (ConformalNL2LTL
steps. Consequently, a direct comparison of help rates between           & LTL planner) outperforms CMAS as it can achieve user-
nl2spec and ConformalNL2LTL would neither be fair nor                    defined 1 − α success rates with minimal human intervention.
meaningful We note that modifications (ii) and (iii) improved            Demonstrations of ConformalNL2LTL, integrated with the
the performance of the baselines, as without them the LLM                LTL planner proposed in [6], in real-world navigation and
frequently produced nonsensical APs.                                     mobile manipulation tasks are provided in [35]
   We report the translation success rate of these baselines in          F. Empirical Evaluation in Out-Of-Distribution Settings
Table II over 182 NL tasks, sampled from the distribution D
                                                                            In this section, we evaluate the performance of Confor-
introduced in Sec. V-A, consisting of 71 easy, 75 medium
                                                                         malNL2LTL in OOD translation scenarios. Specifically, we
and 37 hard scenarios. The overall translation success rates
                                                                         consider test scenarios generated from an unknown distribution
were 87.4% for UA-NL2LTL, 82.87% for Lang2LTL with
                                                                         D̂ ̸= D which is inaccessible and therefore cannot be used
our few shot examples, 53.53% for Lang2LTL without our
                                                                         to construct calibration datasets. As a result, the prediction
few shot examples, and 73.16% for nl2spec. Observe that
                                                                         sets C(ℓtest (k)) in (14) are constructed using calibration data
  5 We would like to note that ConformalNL2LTL can detect when help is   sampled from D while translation problems at test time are
required, while nl2spec does not.                                        sampled from D̂.
                                                                                                                                                 13



                            TABLE III                                that the translation success guarantees do not hold under distri-
E MPIRICAL T RANSLATION S UCCESS R ATES AND H ELP R ATES FOR OOD     bution shifts; nevertheless, ConformalNL2LTL still performs
                            SCENARIOS
                                                                     reasonably well given the severity of the shift. The help rate
           1−α         Empirical        Help Rate   Hf
            (%)     Success Rate (%)       (%)      (%)              and Hf also continue to increase as 1−α increases, consistent
                                                                     with trends observed earlier.
             95           79.5            0.37      3.5
             97           80.5            0.40       4                  We also noticed that most translation errors occur mainly
             99           84.5            0.67       6               due to the absence of the ground truth response in either
                                                                     or both of the generated prediction sets C(ℓ(k), ψp ) and
   Distribution D̂: The distribution D̂ generates scenarios          C(ℓ(k), ψaux ). This is expected as the probabilistic inclu-
σ = {ξ, A} associated with the following three types. (A)            sion guarantees provided by CP no longer apply in OOD.
The first type refers to communication tasks with action space       A potential approach to enable CP to handle distribution
A1 = {send sensor data, relay a message, receive confirmation        shifts is to leverage robust CP to obtain valid prediction
from agent i, trigger alert}. The rules provided to the LLM for      sets for all distributions D̂ that are ‘close’ to D (based on
AP construction are: (i) ‘send data’ which is true when the          the f −divergence) [67]. Integrating ConformalNL2LTL with
sensor data is sent, (ii) ‘relay msg’ which is true when the sys-    robust CP is however out of the scope of this work and part
tem relays a message it received, (iii) ‘confirm i’ that is true     of our future work.
when the system gets confirmation from agent i, and (iv) ‘alert’
that is true when an alert is set off. An example NL task in this
                                                                                 VI. C ONCLUSIONS AND F UTURE W ORK
category is ‘Send sensor data as soon as you get confirmation
from agent 4’. (B) The second type refers to human robot                This paper introduced ConformalNL2LTL, a novel NL-to-
interaction tasks with action space A2 = {detect question,           LTL translation framework. A key contribution of our ap-
answer the question, display a greeting, receive hello, play a       proach is its ability to achieve user-defined translation success
happy animation, play some audio}. The APs are required to           rates while minimally asking for help from users. Future work
have the following format: (i) ‘question’ that is true when the      will focus on (i) relaxing the i.i.d. assumption required in The-
robot detects a question from a user, (ii) ‘answer’ which is true    orem IV.2; and (ii) formally integrating ConformalNL2LTL
after the robot has answered a question, (iii) ‘display greeting’    with existing multi-robot LTL planners.
that is satisfied when the robot displays a greeting, (iv) ‘hello’
that is true when the robot detects a person saying hello,                                         R EFERENCES
(v) ‘happy animation’ that is true when a happy animation
                                                                      [1] C. Baier and J.-P. Katoen, Principles of model checking. MIT press
is displayed, and (vi) ‘audio’ which is true when playing the             Cambridge, 2008, vol. 26202649.
audio. A typical NL task in this category is ‘Display the happy       [2] C. I. Vasile and C. Belta, “Sampling-based temporal logic path plan-
animation, say hello and then answer the question provided                ning,” in IEEE/RSJ International Conference on Intelligent Robots and
                                                                          Systems, Tokyo, Japan, November 2013, pp. 4817–4822.
by the user’. (C) The third type refers to exploration and            [3] J. Tumova and D. V. Dimarogonas, “Multi-agent planning under local
information gathering tasks with action space A3 = {go to                 ltl specifications and event-based synchronization,” Automatica, vol. 70,
region X, explore, detect low map uncertainty}. The APs are               pp. 239–248, 2016.
                                                                      [4] Y. Kantaros and M. M. Zavlanos, “Stylus*: A temporal logic optimal
required to have the following format: (i) ‘region X’ that is             control synthesis algorithm for large-scale multi-robot systems,” The
true when the robot reaches region X, (ii) ‘explore’ that is              International Journal of Robotics Research, vol. 39, no. 7, pp. 812–
true when switching to an exploration policy for expanding                836, 2020.
                                                                      [5] Z. Liu, M. Guo, and Z. Li, “Time minimization and online synchroniza-
the map, (iii) ‘uncertainty low’ which is true when the map               tion for multi-agent systems under collaborative temporal logic tasks,”
uncertainty is low. An example of NL task in this category is             Automatica, vol. 159, p. 111377, 2024.
‘Go to region A, and switch to exploration mode if the map            [6] X. Luo, Y. Kantaros, and M. M. Zavlanos, “An abstraction-free method
                                                                          for multirobot temporal logic optimal control synthesis,” IEEE Transac-
uncertainty is not low’.                                                  tions on Robotics, vol. 37, no. 5, pp. 1487–1507, 2021.
   We built a dataset of 200 translation scenario–LTL pairs           [7] D. Gujarathi and I. Saha, “Mt*: Multi-robot path planning for temporal
containing 73 easy, 88 medium, and 39 hard scenarioss using               logic specifications,” in IEEE/RSJ International Conference on Intelli-
                                                                          gent Robots and Systems (IROS), 2022, pp. 13 692–13 699.
the APs and action spaces described above. The categorization         [8] A. Fang, T. Yin, J. Lin, and H. Kress-Gazit, “Continuous execution
into easy, medium, and hard follows the procedure in Sec-                 of high-level collaborative tasks for heterogeneous robot teams,” arXiv
tion V-A. The distribution D̂ is defined uniformly over this              preprint arXiv:2406.18019, 2024.
                                                                      [9] M. Guo and D. V. Dimarogonas, “Multi-agent plan reconfiguration under
dataset. We emphasize again that neither D nor D̂ is known                local ltl specifications,” The International Journal of Robotics Research,
to our framework, and more complex distributions could also               vol. 34, no. 2, pp. 218–235, 2015.
be considered.                                                       [10] S. C. Livingston, P. Prabhakar, A. B. Jose, and R. M. Murray, “Patching
                                                                          task-level robot controllers based on a local µ-calculus formula,” in IEEE
   In Table III, we report the performance of Confor-                     International Conference on Robotics and Automation, 2013.
malNL2LTL. We sample 20 scenarios from D̂. Alg. 1 then               [11] Y. Kantaros, S. Kalluraya, Q. Jin, and G. J. Pappas, “Perception-based
generates the LTL specifications, which we manually check                 temporal logic planning in uncertain semantic maps,” IEEE Transactions
                                                                          on Robotics, vol. 38, no. 4, pp. 2536–2556, 2022.
for accuracy. We repeat the experiments conducted in Section         [12] S. Kalluraya, G. J. Pappas, and Y. Kantaros, “Multi-robot mission
V-B for the validation scenarios sampled from D̂ and cali-                planning in dynamic semantic environments,” in IEEE International
bration scenarios sampled from D. Observe that for 1 − α =                Conference on Robotics and Automation (ICRA), 2023.
                                                                     [13] M. Kloetzer and C. Mahulea, “Ltl-based planning in environments with
95%, 97%, and 99% the empirical translation success rates                 probabilistic observations,” IEEE Transactions on Automation Science
are 79.5%, 80.5%, and 84.5%, respectively. This demonstrates              and Engineering, vol. 12, pp. 1–14, 10 2015.
                                                                                                                                                                14



[14] Z. Zhou, S. Wang, Z. Chen, M. Cai, H. Wang, Z. Li, and Z. Kan, “Local               task descriptions to stl,” in International Conference on Bridging the
     observation based reactive temporal logic planning of human-robot                   Gap between AI and Reality. Springer, 2024, pp. 259–276.
     systems,” IEEE Transactions on Automation Science and Engineering,             [35] “Demonstrations for conformalnl2ltl,” https://vimeo.com/
     vol. 22, pp. 643–655, 2025.                                                         1165068786?share=copy&fl=sv&fe=ci.
[15] Z. Chen, M. Cai, Z. Zhou, L. Li, and Z. Kan, “Fast motion planning in          [36] G. Shafer and V. Vovk, “A tutorial on conformal prediction.” Journal of
     dynamic environments with extended predicate-based temporal logic,”                 Machine Learning Research, vol. 9, no. 3, 2008.
     IEEE Transactions on Automation Science and Engineering, vol. 22, pp.          [37] A. N. Angelopoulos and S. Bates, “A gentle introduction to confor-
     5293–5307, 2025.                                                                    mal prediction and distribution-free uncertainty quantification,” arXiv
[16] Y. Huang, N. Xu, M. Guo, J. Li, and L. Shen, “Distributed and                       preprint arXiv:2107.07511, 2021.
     reactive controller synthesis for multi-agent systems under finite horizon     [38] J. Su, J. Luo, H. Wang, and L. Cheng, “Api is enough: Conformal
     temporal logic tasks,” IEEE Transactions on Automation Science and                  prediction for large language models without logit-access,” ACL Rolling
     Engineering, vol. 22, pp. 13 485–13 500, 2025.                                      Review (ARR), 2024.
[17] Y. Kantaros and J. Wang, “Sample-efficient reinforcement learning with         [39] K. Cheng, Z. Li, X. Sun, B.-C. Min, A. S. Bedi, and A. Bera,
     temporal logic objectives: Leveraging the task specification to guide               “Efficienteqa: An efficient approach for open vocabulary embodied
     exploration,” IEEE Transactions on Automatic Control, 2024.                         question answering,” arXiv preprint arXiv:2410.20263, 2024.
[18] A. Balakrishnan, S. Jakšić, E. A. Aguilar, D. Ničković, and J. V.          [40] R. Kaur, C. Samplawski, A. D. Cobb, A. Roy, B. Matejek, M. Acharya,
     Deshmukh, “Model-free reinforcement learning for spatiotemporal tasks               D. Elenius, A. M. Berenbeim, J. A. Pavlik, N. D. Bastian et al.,
     using symbolic automata,” in IEEE CDC, 2023.                                        “Addressing uncertainty in llms to enhance reliability in generative ai,”
[19] P. Hao, S. Cui, J. Wei, T. Lu, Y. Cai, and S. Wang, “Learn-gen-plan:                NeurIPS Safe Generative AI Workshop, 2024.
     Bridging the gap between vision language models and real-world long-           [41] M. Ahn, A. Brohan, N. Brown, Y. Chebotar, O. Cortes, B. David,
     horizon dexterous manipulations,” IEEE Transactions on Automation                   C. Finn, C. Fu, K. Gopalakrishnan, K. Hausman et al., “Do as i can,
     Science and Engineering, vol. 22, pp. 15 638–15 649, 2025.                          not as i say: Grounding language in robotic affordances,” CoRL, 2022.
[20] M. Hasanbeig, Y. Kantaros, A. Abate, D. Kroening, G. J. Pappas, and            [42] A. Z. Ren, A. Dixit, A. Bodrova, S. Singh, S. Tu, N. Brown, P. Xu,
     I. Lee, “Reinforcement learning for temporal logic control synthesis                L. Takayama, F. Xia, J. Varley, Z. Xu, D. Sadigh, A. Zeng, and
     with probabilistic satisfaction guarantees,” in Proc. of the 58th IEEE              A. Majumdar, “Robots that ask for help: Uncertainty alignment for large
     Conference on Decision and Control (CDC), Nice, France, December                    language model planners,” Conference on Robot Learning, 2023.
     2019.                                                                          [43] Y. Chen, J. Arkin, Y. Zhang, N. Roy, and C. Fan, “Scalable multi-robot
[21] Z. Zhou, D. J. Lee, Y. Yoshinaga, S. Balakirsky, D. Guo, and Y. Zhao,               collaboration with large language models: Centralized or decentralized
     “Reactive task allocation and planning for quadrupedal and wheeled                  systems?” International Conference on Robotics and Automation, 2024.
     robot teaming,” in IEEE International Conference on Automation Sci-            [44] W. Hunt, S. D. Ramchurn, and M. D. Soorati, “A survey of
     ence and Engineering (CASE), 2022.                                                  language-based communication in robotics,” 2025. [Online]. Available:
[22] S. Kalluraya, G. J. Pappas, and Y. Kantaros, “Resilient temporal logic              https://arxiv.org/abs/2406.04086
     planning in the presence of robot failures,” in 62nd IEEE Conference           [45] V. Pallagani, B. C. Muppasani, K. Roy, F. Fabiano, A. Loreggia,
     on Decision and Control (CDC), 2023, pp. 7520–7526.                                 K. Murugesan, B. Srivastava, F. Rossi, L. Horesh, and A. Sheth,
[23] F. Huang, X. Yin, and S. Li, “Failure-robust multi-robot tasks planning             “On the prospects of incorporating large language models (llms)
     under linear temporal logic specifications,” in 13th Asian Control Con-             in automated planning and scheduling (aps),” Proceedings of the
     ference (ASCC 2022). IEEE, 2022.                                                    International Conference on Automated Planning and Scheduling,
[24] F. Faruq, D. Parker, B. Laccrda, and N. Hawes, “Simultaneous task                   vol. 34, no. 1, pp. 432–444, May 2024. [Online]. Available:
     allocation and planning under uncertainty,” in IEEE/RSJ International               https://ojs.aaai.org/index.php/ICAPS/article/view/31503
     Conference on Intelligent Robots and Systems, 2018, pp. 3559–3564.             [46] Y.-L. Kuo, B. Katz, and A. Barbu, “Deep compositional robotic planners
[25] L. Li, Z. Chen, H. Wang, and Z. Kan, “Task allocation of heterogeneous              that follow natural language commands,” in 2020 IEEE International
     robots under temporal logic specifications with inter-task constraints and          Conference on Robotics and Automation (ICRA), 2020, pp. 4906–4912.
     variable capabilities,” IEEE Transactions on Automation Science and            [47] E. Latif, “3p-llm: Probabilistic path planning using large language
     Engineering, vol. 22, pp. 14 030–14 047, 2025.                                      model for autonomous robot navigation,” 2024. [Online]. Available:
[26] M. Guo and D. V. Dimarogonas, “Task and motion coordination for                     https://arxiv.org/abs/2403.18778
     heterogeneous multiagent systems with loosely coupled local tasks,”            [48] J. Liang, W. Huang, F. Xia, P. Xu, K. Hausman, B. Ichter, P. Florence,
     IEEE Transactions on Automation Science and Engineering, vol. 14,                   and A. Zeng, “Code as policies: Language model programs for embodied
     no. 2, pp. 797–808, 2017.                                                           control,” in 2023 IEEE International Conference on Robotics and
[27] Y. Chen, J. Arkin, C. Dawson, Y. Zhang, N. Roy, and C. Fan, “Autotamp:              Automation (ICRA), 2023, pp. 9493–9500.
     Autoregressive task and motion planning with llms as translators and           [49] H. Zhang, W. Du, J. Shan, Q. Zhou, Y. Du, J. B. Tenenbaum, T. Shu,
     checkers,” in 2024 IEEE International conference on robotics and                    and C. Gan, “Building cooperative embodied agents modularly with
     automation (ICRA). IEEE, 2024, pp. 6695–6702.                                       large language models,” International Conference on Learning Repre-
[28] F. Fuggitti and T. Chakraborti, “Nl2ltl–a python package for converting             sentations (ICLR), 2024.
     natural language (nl) instructions to linear temporal logic (ltl) formulas,”   [50] Z. Yang, L. Ning, H. Wang, T. Jiang, S. Zhang, S. Cui, H. Jiang, C. Li,
     in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 37,          S. Wang, and Z. Wang, “Text2reaction: Enabling reactive task planning
     no. 13, 2023, pp. 16 428–16 430.                                                    using large language models,” IEEE Robotics and Automation Letters,
[29] Y. Chen, R. Gandhi, Y. Zhang, and C. Fan, “Nl2tl: Transforming natural              2024.
     languages to temporal logics using large language models,” Empirical           [51] S. Hong, X. Zheng, J. Chen, Y. Cheng, J. Wang, C. Zhang, Z. Wang,
     Methods in Natural Language Processing (EMNLP), 2023.                               S. K. S. Yau, Z. Lin, L. Zhou et al., “Metagpt: Meta programming
[30] J. X. Liu, Z. Yang, I. Idrees, S. Liang, B. Schornstein, S. Tellex, and             for multi-agent collaborative framework,” International Conference on
     A. Shah, “Grounding complex natural language commands for temporal                  Learning Representations, 2024.
     tasks in unseen environments,” in Conference on Robot Learning.                [52] D. Shah, M. Equi, B. Osinski, F. Xia, B. Ichter, and S. Levine,
     PMLR, 2023, pp. 1084–1110.                                                          “Navigation with large language models: Semantic guesswork as a
[31] M. Cosler, C. Hahn, D. Mendoza, F. Schmitt, and C. Trippel, “nl2spec:               heuristic for planning,” 2023. [Online]. Available: https://arxiv.org/abs/
     interactively translating unstructured natural language to temporal logics          2310.10103
     with large language models,” in International Conference on Computer           [53] H. Wang, H. Zhang, L. Li, Z. Kan, and Y. Song, “Task-driven rein-
     Aided Verification. Springer, 2023, pp. 383–396.                                    forcement learning with action primitives for long-horizon manipulation
[32] Y. Xu, J. Feng, and W. Miao, “Learning from failures: Translation                   skills,” IEEE Transactions on Cybernetics, 2023.
     of natural language requirements into linear temporal logic with large         [54] S. Su, S. Han, Y. Li, Z. Zhang, C. Feng, C. Ding, and F. Miao, “Collab-
     language models,” in IEEE 24th International Conference on Software                 orative multi-object tracking with conformal uncertainty propagation,”
     Quality, Reliability and Security, 2024, pp. 204–215.                               IEEE Robotics and Automation Letters, 2024.
[33] J. Pan, G. Chou, and D. Berenson, “Data-efficient learning of natural          [55] A. Dixit, Z. Mei, M. Booker, M. Storey-Matsutani, A. Z. Ren, and
     language to linear temporal logic translators for robot task specification,”        A. Majumdar, “Perceive with confidence: Statistical safety assurances
     in 2023 IEEE International Conference on Robotics and Automation                    for navigation with learning-based perception,” in CoRL, 2024.
     (ICRA), pp. 11 554–11 561.                                                     [56] L. Lindemann, M. Cleaveland, G. Shim, and G. J. Pappas, “Safe
[34] S. Mohammadinejad, S. Paul, Y. Xia, V. Kudalkar, J. Thomason, and                   planning in dynamic environments using conformal prediction,” IEEE
     J. V. Deshmukh, “Systematic translation from natural language robot                 Robotics and Automation Letters, 2023.
                                                                                                                                                         15



[57] N. Hashemi, X. Qin, L. Lindemann, and J. V. Deshmukh, “Data-driven            heuristically quantifies how poorly the model predicts the true
     reachability analysis of stochastic dynamical systems with conformal          label. In classification problems, a common choice of NCS
     inference,” in IEEE Conference on Decision and Control (CDC), 2023.
[58] J. Sun, Y. Jiang, J. Qiu, P. T. Nobel, M. Kochenderfer, and M. Schwager,      is r̄ = 1 − ψ(xi )ygt , which assigns higher scores to inputs
     “Conformal prediction for uncertainty-aware planning with diffusion           x for which the model places low confidence on the true
     dynamics model,” in NeurIPS, 2023.                                            class y gt . The calibration procedure consists of two steps. First,
[59] S. Huriot and H. Sibai, “Safe decentralized multi-agent control using
     black-box predictors, conformal decision policies, and control barrier        we compute the NCS r̄i = 1 − ψ(x)ygt for each calibration
                                                                                                                                      i
     functions,” in 2025 IEEE International Conference on Robotics and             pair (xi , yigt ). Second, we compute the ⌈(D+1)(1−α)⌉
                                                                                                                                    D      -quantile
     Automation (ICRA). IEEE, 2025, pp. 7445–7451.
[60] J. Wang, J. Tong, K. Tan, Y. Vorobeychik, and Y. Kantaros, “Conformal         of the NCSs {r̄i }D   i=1  where ⌈.⌉ is the ceiling function.  We
     temporal logic planning using large language models,” ACM Trans.              denote the resulting quantile by q̄. At test time, given an input
     Cyber-Phys. Syst., Sep. 2025, just Accepted. [Online]. Available:             xtest , we construct the following prediction set C(xtest ) = {y :
     https://doi.org/10.1145/3769111
[61] J. Wang, G. He, and Y. Kantaros, “Probabilistically correct language-         ψ(xtest )y ≥ 1 − q̄} which satisfies (30).
     based multi-robot planning using conformal prediction,” IEEE Robotics
     and Automation Letters, vol. 10, no. 1, pp. 160–167, 2025.
[62] A. Z. Ren, J. Clark, A. Dixit, M. Itkina, A. Majumdar, and D. Sadigh,                               A PPENDIX B
     “Explore until confident: Efficient exploration for embodied question                  C ONFORMAL P REDICTION WITH M ULTIPLE
     answering,” Robotics: Science and Systems (RSS), 2024.                                 S EMANTICALLY E QUIVALENT F ORMULAS
[63] K. Liang, Z. Zhang, and J. F. Fisac, “Introspective planning: Aligning
     robots’ uncertainty with inherent task ambiguity,” NeurIPS, 2024.                The CP analysis, provided in Section III-D, as well as our
[64] “Software, and datasets for conformalnl2ltl,” https://anonymous.
     4open.science/r/ConformalNL2LTL.                                              translation success guarantees (Theorem IV.2) can be extended
[65] X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowdh-          to cases where multiple semantically equivalent formulas exist.
     ery, and D. Zhou, “Self-consistency improves chain of thought reasoning       As discussed in Remark IV.3, the key difference lies in the con-
     in language models,” ICLR, 2023.
[66] M. Sadinle, J. Lei, and L. Wasserman, “Least ambiguous set-valued             struction of the calibration dataset introduced in Section III-D
     classifiers with bounded error levels,” Journal of the American Statistical   where among all LTL formulas that are semantically equivalent
     Association, vol. 114, no. 525, pp. 223–234, 2019.                            to the NL instructions, we select the one constructed by pick-
[67] M. Cauchois, S. Gupta, A. Ali, and J. C. Duchi, “Robust validation:
     Confident predictions even when distributions shift,” Journal of the          ing at each step the response with the highest frequency. CP
     American Statistical Association, pp. 1–66, 2024.                             can then be applied as usual, yielding prediction sets (see (37))
[68] A. Angelopoulos, S. Bates, J. Malik, and M. I. Jordan, “Uncertainty           that contain, with user-specified probability, the semantically
     sets for image classifiers using conformal prediction,” International
     Conference on Learning Representations (ICLR), 2021.                          equivalent LTL formula (among all other equivalent formulas)
[69] B. Kumar, C. Lu, G. Gupta, A. Palepu, D. Bellamy, R. Raskar,                  constructed using the highest-frequency responses, among all
     and A. Beam, “Conformal prediction with large language models for             correct responses, at each translation step. Then, as discussed
     multi-choice question answering,” in ICML (Neural Conversational AI
     TEACH) workshop, 2023.                                                        in Remark IV.3, we emphasize that the guarantees provided
                                                                                   in Proposition IV.1 and Theorem IV.2 hold with respect to
                                                                                   that LTL formula. In what follows, we provide a more formal
                     A PPENDIX A                                                   description of how CP is applied to construct prediction sets
         BACKGROUND ON C ONFORMAL P REDICTION                                      when multiple semantically equivalent formulas exist, which
   Conformal prediction (CP) is a user-friendly paradigm for                       is adapted from Appendices A3-A4 of [42].
creating statistically rigorous uncertainty sets (called predic-                      Constructing a Calibration Dataset: We sample D ≥ 1
tion sets) for the predictions of pre-trained machine learning                     independent calibration scenarios {σi,calib }Di=1 ∼ D. Each
models. These sets that are guaranteed to contain the ground-                      σi,calib gives rise to a sequence of Hi ≥ 1 prompts denoted by
truth output with a user-specified probability without making
assumptions on the underlying data distribution or the structure                                  ℓ̄i,calib = ℓi,calib (1), . . . , ℓi,calib (Hi ),    (31)
of the model. In what follows, we provide an overview of CP                        where each prompt ℓi,calib (k) is constructed exactly as in Sec-
for models used in classification settings as e.g., in [68], [69];                 tion III-B; the only difference is that part (d) contains partial
for further details see [37].                                                      formulas constructed using all possible correct responses given
   Consider a pre-trained model ψ that maps an input x                             ℓi,calib (k − 1), for k ∈ {2, . . . , Hi }. Let Rik ≥ 1 denote the
(e.g., an image or a natural-language question) to one of                          number of correct responses at step k. Hereafter, we denote
K discrete labels. We assume that ψ outputs a confidence                                                              Rik
                                                                                   by T̄i,calib (k) = {si,r,calib (k)}r=1 the set of all feasible/correct
vector ψ(x) ∈ [0, 1]K , where ψ(x)y denotes the predicted
                                                                                   responses at step k. Thus, each sequence ℓ̄i,calib is associated
confidence assigned to a label y. Let y gt denote the ground-
                                                                                   with a set of Ri ≥ 1 semantically equivalent LTL formulas
truth label associated with input x. We also assume that
                                                                                   Φ̄i,calib = {ϕi,r,calib }R i
                                                                                                            r=1 , where
data pairs (x, y) are drawn from an unknown distribution D.
Consider a calibration dataset {(xi , yigt )}Di=1 ∼ D and a test                               ϕi,r,calib = si,r,calib (1), . . . , si,r,calib (Hi )   (32)
                                             gt
input xtest ∼ D with unknown label ytest        . CP constructs a
prediction set C(xtest ) such that                                                 representing a syntactically correct LTL formula that is se-
                                                                                   mantically equivalent to the NL task. This gives rise to a
                       gt                                     1
   1 − α ≤ Pxtest ∼D (ytest ∈ C(xtest )) ≤ 1 − α +               ,        (30)     calibration dataset M = {(ℓ̄i,calib , Φ̄i,calib )}D
                                                                                                                                     i=1 . As in Section
                                                             D+1                   III-D, this process results in converting the distribution D into
where α ∈ (0, 1) is a user-specified error level. To construct                     an equivalent distribution D̄′ over prompt sequences discussed
C(xtest ), CP relies on a nonconformity score (NCS), which                         as mentioned above.
                                                                                                                                                       16



  Given a validation scenario σtest ∼ D, we construct the                       these test and calibration sequences are obtained by applying
prompt sequence:                                                                the measurable function G to every point in the support of
                                                                                D̄′ , including ℓ̄i,calib and ℓ̄test . Since measurable functions of
                    ℓ̄test = ℓtest (1), . . . , ℓtest (Htest ),        (33)     i.i.d. random variables remain i.i.d., it follows that ℓ̄maxtest and
                                                                                            D
where each ℓtest (k) has the same structure as the prompt pre-                  {ℓ̄max
                                                                                   i,calib }i=1 are i.i.d. and therefore (37) holds.
sented in Section III-B, with part (d) containing the partial LTL                   On-the-fly Construction of Prediction Sets: As in Section
formulas constructed by using all possible correct responses                    III-D, the prediction set in (36) is constructed after the entire
obtained up until k − 1. Note that {ℓ̄i,calib }Di=1 and ℓ̄test are
                                                                                sequence ℓ̄max test is obtained. However, at test time, the full
i.i.d, sampled independently from D̄′ .                                         sequence of prompts is not observed at once. Instead, we can
    Extracting the Highest-Frequency LTL Formula: Con-                          follow exactly the same steps as in Section III-D to construct
sider a function G that is applied to every point in the                        the prediction set in (36) causally. Consequently, (14)–(18),
support of D̄′ . This function, given the prompt ℓ̄(k), which                   together with all theoretical results in Section IV, hold for
is part of the sequence ℓ̄ ∼ D̄′ , and a set T̄ (k) of feasible                 the sequence ℓ̄max                                               max
                                                                                                    test and the corresponding LTL formula ϕtest .
responses, returns the response s ∈ T̄ (k) with the highest                     As a result, as discussed in Remark IV.3, Theorem IV.2 holds
frequency F ψp (s|S(k)). If T̄ (k) = ∅, then the user types in the              when the user selects the correct response from the prediction
response and F ψp (s|S(k)) = 0. Applying G auto-regressively                    set with the highest frequency F ψp (s | S(k)). This requires
to all calibration sequences ℓ̄i,calib defined in (31) yields the               ConformalNL2LTL to return both the prediction set and the
following sequence sequence of Hi,calib prompts:                                associated frequencies.

                 ℓ̄max        max                   max
                   i,calib = ℓi,calib (1), . . . , ℓi,calib (Hi )      (34)
where each prompt ℓmax  i,calib (k) is the same as ℓi,calib with part
(d) containing the formula constructed using the responses
smax              max
 i,calib (n) = G(ℓi,calib (n), T̄i,calib (n)), ∀n ∈ {1, . . . , k − 1}.
Note that the prompt ℓmax i,calib (1) does not contain any response
in part (d).
   The corresponding LTL formula is given by,                                                         David Smith Sundarsingh (S’24) is a PhD stu-
                                                                                                      dent in the Department of Electrical and Systems
                ϕmax        max                   max
                 i,calib = si,calib (1), . . . , si,calib (Hi ),       (35)                           Engineering, Washington University in St. Louis,
                                                                                                      MO, USA. He received his B.E. in Mechanical
where smax                     max
           i,calib (k) = G(ℓi,calib (k), T̄i,calib (k)). Observe that
                                                                                      PLACE           Engineering from Coimbatore Institute of Technol-
  max                                                                                 PHOTO           ogy, TN, India in 2020, and his M.Tech degree in
ϕi,calib (k) is the LTL formula constructed by always selecting                        HERE           Robotics and Automation from the Defence Institute
the response with the highest frequency among all correct                                             of Advanced Technology, MH, India. His research
options, at all steps until k. This process gives rise to the                                         interests include robotics, machine learning, and
following calibration dataset M′′ = {(ℓmax                    max       D
                                                   i,calib , ϕi,calib )}i=1 .
                                                                                                      formal methods.
   Constructing Prediction Sets: Consider a validation sce-
nario σtest ∼ D with unknown corresponding LTL formula.
Given a set of calibration scenarios {σi,calib }D         i=1 ∼ D, we first
construct the calibration dataset M = {ℓ̄i,calib , Φ̄i,calib }, where,
as discussed earlier, ℓ̄i,calib ∼ D̄′ . From M we generate the
calibration set M′′ = {(ℓmax               max        D
                                i,calib , ϕi,calib )}i=1 by applying G
auto-regressively, as described earlier. Similarly, we generate                                       Jun Wang (S’22) is a PhD candidate in the De-
                                                                                                      partment of Electrical and Systems Engineering at
the sequence of prompts ℓ̄max                max                max
                                test = ℓtest (1), . . . , ℓtest (Htest ) by                           Washington University in St. Louis. He received his
applying G auto-regressively to the sequence ℓ̄test , defined in                                      B.Eng. degree in Software Engineering from Sun
                                                                                      PLACE           Yat-Sen University in 2019 and his MSE degree
(33), associated with σtest . Then, we construct the following                        PHOTO           in Robotics from the University of Pennsylvania
prediction set                                                                         HERE           in 2021. His research interests include robotics,
                                                                                                      machine learning, and control theory.
                ¯ ℓ̄max
                C(                      max
                    test ) = {ϕ|F̄ (ϕ|ℓ̄test ) ≥ 1 − q̄},              (36)
where F̄ (ϕ|ℓ̄max
              test ) is as given in (10), and q̄       is the (1 − α)
quantile of the scores computed for the dataset M′′ .
    If the validation sequence ℓ̄maxtest and the calibration sequences
  max
ℓ̄i,calib are i.i.d. then the following coverage guarantee holds
for C( ¯ ℓ̄max
           test ) (that is ‘equivalent’ to (12))

                    P (ϕmax    ¯ max
                        test ∈ C(ℓ̄test )) ≥ 1 − α.                    (37)                           Jyotirmoy V. Deshmukh is an Associate Professor
                                                                                                      of Computer Science in the Thomas Lord Depart-
which follows directly from CP. Here, ϕmax
                                       test is the formula con-                                       ment of Computer Science and the co-director of
structed using the highest-frequency correct response, among                                          the USC center for Autonomy and AI. Previously he
                                                                                      PLACE           was a Principal Research Engineer at Toyota motors
all correct responses in S(k), at each translation step k (as                         PHOTO           R & D. He was a postdoctoral research scholar at
in (35)). To verify the i.i.d. assumption, recall that both                            HERE           the University of Pennsylvania and received his Ph.D
                                                                                                      from the University of Texas at Austin.
                                                                                17



                         Yiannis Kantaros (S’14-M’18) is an Assistant Pro-
                         fessor in the Department of Electrical and Systems
                         Engineering, Washington University in St. Louis
                         (WashU), St. Louis, MO, USA. He received the
        PLACE            Diploma in Electrical and Computer Engineering in
        PHOTO            2012 from the University of Patras, Patras, Greece.
         HERE            He also received the M.Sc. and the Ph.D. degrees
                         in mechanical engineering from Duke University,
                         Durham, NC, in 2017 and 2018, respectively. Prior
                         to joining WashU, he was a postdoctoral associate
                         in the Department of Computer and Information
Science, University of Pennsylvania, Philadelphia, PA. His current research
interests include machine learning, distributed control and optimization, and
formal methods with applications in robotics. He received the Best Student
Paper Award at the 2nd IEEE Global Conference on Signal and Information
Processing (GlobalSIP) in 2014 and was a finalist for the Best Multi-
Robot Systems Paper at the IEEE International Conference on Robotics and
Automation (ICRA) in 2024 and the Best Paper Award at the ACM/IEEE
International Conference on Cyber-Physical Systems (ICCPS) in 2025. He
also received the 2017-18 Outstanding Dissertation Research Award from
the Department of Mechanical Engineering and Materials Science, Duke
University, and a 2024 NSF CAREER Award.
