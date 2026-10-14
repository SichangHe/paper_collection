                                                    LeanSide: A Formally Verified Co-Reasoning System for
                                                                   Natural-language Proofs
                                                           Chenjun Guo                             Manooshree Patel                               Arnav Mehta
                                               University of California, Berkeley           University of California, Berkeley          University of California, Berkeley
                                                      Berkeley, CA, USA                            Berkeley, CA, USA                           Berkeley, CA, USA
                                                 chenjun_guo@berkeley.edu                    manooshreepatel@berkeley.edu                  arnavmehta@berkeley.edu

                                                         Krishiv Kothari                               Thomas Lu∗                                   Niels Voss∗
                                               University of California, Berkeley           University of California, Berkeley          University of California, Berkeley
                                                      Berkeley, CA, USA                            Berkeley, CA, USA                           Berkeley, CA, USA
                                                krishivkothari@berkeley.edu                     thomaslu@berkeley.edu                       niels_voss@berkeley.edu
arXiv:2610.00760v2 [cs.HC] 6 Oct 2026




                                                   Rayna Bhattacharyya∗                              Peter Donovan∗                            Bjoern Hartmann
                                               University of California, Berkeley           University of California, Berkeley          University of California, Berkeley
                                                      Berkeley, CA, USA                            Berkeley, CA, USA                           Berkeley, CA, USA
                                                   rayna_b@berkeley.edu                       peterdonovan@berkeley.edu                    bjoern@eecs.berkeley.edu

                                                                                                     Gireeja Ranade
                                                                                            University of California, Berkeley
                                                                                                   Berkeley, CA, USA
                                                                                               ranade@eecs.berkeley.edu

                                        Abstract                                                                1   Introduction
                                        Large language models are increasingly used as collaborators on         Large language models (LLMs) are being explored as collaborators
                                        deductive-reasoning tasks, but their outputs can hallucinate or pull    on deductive-reasoning tasks, where conclusions necessarily follow
                                        users away from intended reasoning. Formal proof assistants pro-        from given premises or rules [91]. Such tasks arise across domains,
                                        vide machine-checked verification, but have a steep learning curve      including mathematics [15, 30, 47, 52, 72, 99, 109], programming [30,
                                        and require more granular reasoning than human written proofs.          49], legal judgment [24, 39, 77], and clinical decision support [43,
                                        We explore an interface that combines these strengths, allowing         68, 85, 86].
                                        users to write and revise free-form natural-language proofs while          However, LLM-generated reasoning can contain hallucinations [35,
                                        a verified backend checks their reasoning and returns feedback          108]. One solution is to express reasoning in a machine-checkable
                                        at the user’s granularity. We study this interface in the context       formal language such as Lean [18], Isabelle [74], and Rocq [6],
                                        of undergraduate mathematics education by developing LeanSide,          whose kernels mechanically checks formalized proofs and pro-
                                        a formally verified co-reasoning system, which auto-formalizes          vides hallucination-free feedback. Such formal representations are
                                        student reasoning into Lean and informalizes verifier output into       widely used in high-assurance domains, including hardware verifi-
                                        understandable feedback. We conducted user studies through class-       cation [103], and increasingly in the formalization of mathematical
                                        room deployment and analyzed which system properties helped             research [75, 83]. A successfully checked formal artifact provides
                                        students make progress and which caused them to get stuck. We           strong confidence in logical validity.
                                        use these findings to derive design implications for using a formally      But these languages have a steep learning curve [81, 92] and
                                        verified backend in human-AI co-reasoning systems.                      demand far more granular and rigorous reasoning than people con-
                                                                                                                ventionally write [25, 73, 90]. A growing body of work has started
                                                                                                                to use auto-formalization to automatically formalize informal rea-
                                        CCS Concepts
                                                                                                                soning into machine-checkable code, originating from and richest
                                        • Human-centered computing → Natural language interfaces;               in mathematics [4, 55, 58, 73, 106, 111], and extending to other rule-
                                        Interactive systems and tools.                                          based domains, such as legal and tax judgment [39, 77] and clinical
                                                                                                                support [85].
                                        Keywords                                                                   Despite rapid progress in auto-formalization, prior systems have
                                        Human-AI collaborative reasoning, Large Language Models, Natural-       primarily aimed to generate verified formal code for increasingly
                                        language theorem proving, Lean, Theorem proving, math education         advanced problems, rather than to faithfully follow a user’s rea-
                                                                                                                soning trace. They have also paid less attention to interactive
                                                                                                                settings where user input may be free-form, ambiguous, incom-
                                                                                                                plete, or still in progress. Traditionally, formalization is a post-hoc
                                        ∗ These authors contributed equally to this work.
                                                                                                                                          Guo et al.


check: a mathematician formalizes a finished proof into machine-                                           o-reaoninaent
checkable code after the argument is complete [58, 106]. Existing
auto-formalization systems largely inherit this framing, typically                             Auto-formalizer             Informalizer
only support well-formed, textbook-style proofs as input [4, 55, 58].      er     atural                           ean                     atural
As a result, they are not well suited to serving as interactive collab-           anuae                                                    anuae

orators for proofs that are still being developed.
   In human communication, partners continually build mutual              Figure 1: User workflow in a co-reasoning system: users ex-
understanding [13, 14], thus a formally verified collaborative agent      press input and receive output in natural or informal lan-
must support an analogous grounding loop: users need to know              guage while the system auto-formalizes input into Lean, ver-
both whether the system has “understood” their reasoning and              ifies it, and informalizes the result.
what verification result it produced. We aim to build an informal-
reasoning collaborative agent that makes the power of formal
verification accessible to broader audiences who are trained
to reason in their own domains but have no knowledge of the               2     Related Work
formal language. Users read and write as they would when com-             In this section, we first discuss relevant HCI literature on co-reasoning
municating with another person, while a verified backend interprets       systems. We then turn to recent advances and limitations in auto-
and checks their reasoning: auto-formalization maps informal input        formalization, which lays the background and motivation of our
to a formal representation, and informalization maps verifier output      works but have largely been discussed outside HCI in the mathe-
back into everyday reasoning (Figure 1). This interaction allows          matics, AI and education communities.
users to gain confidence in the validity of the system’s feedback.
   We study student interactions with such a formally verified co-
reasoning system (FVCR) for undergraduate mathematics, a timely
                                                                          2.1    Challenges of human-AI collaboration in
setting as students increasingly use LLM-based tools for homework                reasoning tasks
feedback [11, 54, 98]. LLMs can produce convincing but at times           The recent popularity of LLMs has renewed the aspiration of using
incorrect answers [35, 40, 96, 108] or distract students from their       natural language to collaborate with machines on reasoning tasks.
original reasoning paths [54].                                            LLM based system has long being discussed about the problems of
   We call this tool LeanSide. LeanSide affords students to ex-           hallucinations and user agency preservation.
press their reasoning in familiar language and at their desired              In LLM-assisted reasoning, fluent explanations can make in-
granularity (i.e., the level of detail of a step), validate their         correct conclusions particularly difficult to reject [42], users may
reasoning through formally verified feedback, and iterate                 become more confident after accepting incorrect advice [8], and
on mistakes in their proofs. Our goal is not to provide fully             erroneous LLM-generated information can directly lead to incorrect
“tutor-like” feedback: we do not optimize the system to behave like       decisions [88]. In logical reasoning tasks, programmers [67] and
a human tutor or to be maximally helpful pedagogically. Instead, we       domain scientists [70] could both fail to detect errors in generated
investigate the possible role of formal verification in an interaction    code. Prior interfaces address this problem by exposing inconsis-
loop where students work using familiar informal language, asking         tencies [12], highlighting suspected hallucinations [45], or making
how much Lean’s verification power can help students. We also             generated behavior executable and inspectable [20]. In our sys-
recognize that recent high-profile AI mathematics results do not          tem, we take another route to reducing hallucinations by using a
make formal verification obsolete; they often pair generative search      formally verified backend.
with formalization [23, 71], and our work asks how this pairing can          Prior work has also long raised concerns about preserving user
be brought into interactive settings for students and other users.        agency in such collaboration. Although current interfaces appear
   The main goals and affordances are shown in Fig. 2. We con-            to support fully free-form natural-language input, users, especially
tribute: (1) LeanSide, a system that uses formal language as a verifi-    novices, can struggle to articulate their thoughts into effective in-
cation backbone while supporting the design goals of low threshold,       formal reasoning input for the system [38, 67, 112]. In human-AI
high ceiling, wide walls, and transparency for non-expert interac-        collaboration for programming, users also face difficulty inspecting
tion. We describe the technical challenges of meeting these goals         whether generated code interpreted and implements their intended
and our implementation solutions. (2) A user study with 23 partic-        reasoning [114] and debugging prompts systematically [38, 112,
ipants, conducted alongside a classroom deployment, examining             114]. Prior work links these challenges to failures of shared under-
whether and how students use system feedback to iterate on their          standing: plausible but misaligned LLM outputs can pull users away
proofs. (3) Empirical findings on which system features helped stu-       from their original reasoning and require costly monitoring and
dents make progress and which barriers limited progress, together         repair [17, 62, 89]. In programming, long LLM generated sugges-
with design implications for how AI co-reasoning systems can use          tions can disrupt programmers’ flow [5], while inspecting, verify-
formal verification to move beyond current limitations.                   ing, and editing them imposes additional interaction costs [62]. In
                                                                          decision-making, automated suggestions can reduce users’ initia-
                                                                          tive [46], and LLM recommendations can leave less room for users’
                                                                          independent reasoning [78]. Across broader domains, LLM-based
                                                                          collaboration can also weaken users’ sense of ownership [19] or
                                                                          redirect their thinking toward the model’s suggestions [34].
LeanSide: A Formally Verified Co-Reasoning System for Natural-language Proofs


                                                                                                 Make Lean
                                                                       Overall Goal          accessible through
                                                                                               informal proof
                                                                                                  language


                                                                                                            Validate and        ser study
                                                   System affordance            Express reasoning          improve proof
                                                                               in familiar language                             evaluation goal
                                                                                                        correctness through
                                                                                  and granularity        system feedback              How do students 

                                                                                                                                       make progress on 

                                                                                                                                        their proof with the

                                                                                                                                         system feedbacks

                                                                                                                                           and when do they get 

                                             Design goals        Expressiveness via          Low threshold and     Transparency for           stuck?
                                                                     wide wall                 high ceiling for         system
                                                                                                  feedback          interpretation

                                                                                                                                                           System 

                                 Implementation       Interpret incomplete,          Preserve the        Judge correctness       Responsive
                 performance 

                                     challenges     incorrect, and ambiguous      student's reasoning      at the course           -ness                       evaluation
                                                       informal reasoning            path faithfully        granularity.                                            faithfulness and
                                                                                                                                                                        accuracy




       Figure 2: This figure summarizes the system’s goals, affordances, design goals, and implementation requirements.


   Consequently, interfaces have begun to externalize the system’s                                           several widely used datasets are constructed from formal corpora
interpretation to bring mutual understanding back to the conver-                                             rather than situated human proof writing, such as MMA and Her-
sation. Liu et al. [53] frame natural-language programming as an                                             ald [21, 36], TheoremLlama’s OBT data [97], and MUSTARD [32].
abstraction-matching problem and help users inspect and repair                                                  Student proofs in learning contexts are often more fragmented,
mismatches between their goals and the system’s interpretation,                                              nonlinear, implicit, and loosely structured than these benchmarks
closely paralleling our design. SOVITE [48] aims to build mutual                                             assume [26, 104]. Moreover, when students work with a human
understanding with the users by displaying the system’s inferred                                             tutor or tutoring system, they often expect iteration, making their
intents through GUI screenshots. These works motivate our focus                                              proofs more likely to be incomplete, incorrect, or expressed only
on making the system’s interpretation inspectable.                                                           as high-level ideas [7, 94]. We therefore study auto-formalization
                                                                                                             not as one-shot translation of finished proofs, but as a co-reasoning
                                                                                                             process through which students introduce, revise, repair, and clarify
2.2     Lean and auto-formalization                                                                          mathematical ideas while the formal state evolves with the interac-
Interactive theorem provers such as Lean [18], Isabelle [74], and                                            tion.
Rocq [6] provide machine-checked environments for formalizing
mathematics. However, they remain difficult for non-experts: they
require a steep learning curve and a level of granularity far below
ordinary mathematical writing [82], creating an accessibility gap
between formal verification and how students and mathematicians                                              2.3        Making formal verification accessible
normally write proofs.                                                                                       Prior work has explored multiply ways to make formal verifica-
   Auto-formalization aims to narrow this gap by translating natural-                                        tion more accessible to both expert and non-experts. In mathe-
language mathematics into formal language. Recent work has fo-                                               matics education, several studies have tried to make formal lan-
cused mainly on statement auto-formalization, which translates                                               guages accessible by teaching them directly in mathematics class-
informal theorems into Lean propositions [4, 21, 36, 50, 55–58,                                              rooms [27, 29, 31, 33, 93]. Students benefit from faster feedback
76, 102, 105, 106, 111], and automated theorem proving, which                                                loops, but these tools still pose pedagogical challenges: Lean error
starts from a formal proposition and generates compiled formal                                               messages can be insufficient for students [27], and proof-assistant
proofs [51, 107, 110].                                                                                       feedback may signal that a problem exists without explaining
   A smaller body of work explores whole-proof auto-formalization [10,                                       why [2]. Hazel Prover addresses this challenge through design
32, 37, 63, 73, 90, 97], raising the issue of faithfulness: whether                                          criteria for educational proof assistants, including pedagogical feed-
the formal proof preserves the content and organization of the                                               back, error tolerance, scaffolding, easy interaction, and classroom
informal reasoning. Existing work operationalizes faithfulness in                                            deployability [41]. These criteria offer an educational perspective
several ways, including semantic similarity between informal and                                             complementary to our focus.
formal steps [50, 57], bidirectional equivalence between formal can-                                            Other systems lower the barrier through visualization and con-
didates [55, 76], structural fidelity of intermediate claims and proof                                       trolled natural language. These include visualizing unsolved Lean
dependencies [10, 73], and robustness to paraphrases or invalid                                              goals [65], de-automating automatically generated proofs [80], sup-
steps, where systems must avoid silently changing or repairing the                                           porting controlled-natural-language proofs [60, 101], and using
user’s meaning [16, 61]. At the proof level, ProofFlow represents                                            domain-specific visualizations to teach formal methods [66]. These
proof structure as a dependency graph [10].                                                                  tools make formal systems easier to inspect and use, but still only
   However, most auto-formalization benchmarks still assume pol-                                             allowed a subset of utterances.
ished, textbook-style, one-shot inputs. ProofNet pairs textbook                                                 A related line of work studies human-AI collaboration for proof
problems with a single natural-language proof and Lean state-                                                formalization. Lea supports mathematician-in-the-loop Lean de-
ment [4]; miniF2F and Lean Workbook focus on theorem or prob-                                                velopment [95], while LLMStep [100] and Lean Copilot [87] assist
lem statements rather than human proof revision [111, 113]; and                                              formalization with tactic suggestion, proof search, and premise
                                                                                                                                      Guo et al.


selection. These systems primarily support experts producing for-        in F2.1 where step 2 maps to two assertions. Each smallest pro-
mal proofs, rather than non-experts seeking verified feedback on         gression unit is classified as either a declaration or an assertion.
natural-language reasoning.                                              Declarations, such as assumption introductions F2.2 , are always
   Formal verification has also been applied beyond mathematics,         marked green because users may introduce assumptions freely.
including tax, legal [39, 77], and medical reasoning [28, 85]. These     Assertions are marked green when verified, or yellow with
works demonstrate the potential of utilizing machine-checkable rea-      an error message when verification fails F2.3 . The informaliza-
soning in high-stakes domains, but primarily focus on the technical      tion visualization keeps feedback at the user’s granularity: specific
realization rather than learning how people engage with formally         enough to localize errors, but not so fine-grained that low-level
verified feedback through informal-language interfaces.                  formal details create information overload.
   Our work is related to all of these efforts, but moves beyond            Second, the interface makes errors understandable without re-
expert-facing tools by using a natural-language interface and ex-        quiring users to inspect Lean code. Step-wise errors are shown di-
amining how people interact with such systems in practice.               rectly inside the informalization cell for the incorrect claim F2.3 ;
                                                                         when all written steps are correct but the proof remains incomplete,
3     System design                                                      the system shows a continuation feedback at the end of the user’s
This system targets undergraduate students with no knowledge of          proof F4 .
Lean, and it is designed for deployment in undergraduate math-              Advanced users who know Lean or want to learn it can click
ematics courses. To afford expressing reasoning through natural          “See Lean code” to view the highlighted Lean block correspond to
language, validating and iterating on proofs, we adopt three corre-      each step F3 .
sponding design goals: (1) expressiveness via wide walls [79], (2)          Here is an overview of five possible feedback types. Appendix B
low-threshold and high-ceiling feedback [64], and (3) transparency       shows examples for each type of feedback.
of system representation.                                                      • Step-level error messages appear when some steps are
   A user’s workflow is as follows: (1) the user enters free-form                faulty; each unverified step shows an informalized proposi-
reasoning by uploading handwriting, or typing directly; (2) The                  tion and an error message.
system auto-formalizes the input into verified Lean code (3) the               • Continuation error messages appear when all steps are
resulting code and compiler output are informalized into natural-                verified but the proof remains incomplete, under the condi-
language feedback; and (4) the user revises their proof based on                 tions described in Section 4.1.3.
the feedback. Users can iterate on their proof without reading or              • Continuation hints also appear when all steps are verified
writing Lean, but can open a Lean code panel to see how their steps              but the proof remains incomplete, under the conditions
map to Lean if interested.                                                       described in Section 4.1.3.
                                                                               • Large-jump warnings provide optional guidance on veri-
3.1    Expressiveness via wide walls                                             fied steps that could be further justified.
Creative-support tools should have “wide walls,” supporting vari-              • Suggestions provide optional guidance for fully verified,
ous forms of exploration beyond predefined actions [79]. We treat                correct, and complete proofs, helping make the proof more
proof-solving as a creative activity—students use different strate-              rigorous.
gies, write at different granularity, and rely on various informal or
ambiguous representations. Our system therefore supports reason-         3.3    Transparency
ing in whichever form users find most natural. Users can upload          Free-form input alone is insufficient: the system must make its
a photo of handwritten work F1 (see Fig. 3 for this and all fea-         interpretation transparent. Users can trust verification feedback
ture refs) or type directly in LATEX on central panel. These methods     only after confirming that the system formalized the reasoning they
covers two primary ways our target users write proofs. Unlike            intended. We do this at two levels. First, users are able to assess
many auto-formalization settings, where natural-language proofs          the faithfulness of auto-formalization through Feature F2 , which
are textbook-like, complete, and close to formal structure, input        maps each user-written proof step to its informalized Lean inter-
modes in our system support proofs as they are produced, not only        pretation. Second, to support free-form input, the system surfaces
after they are polished, even when they are ambiguous, exploratory,      how it resolves underspecified language: ambiguous references are
incorrect, or incomplete.                                                highlighted with predicted meanings F5 , and each sentence is
                                                                         labeled with its predicted action type, such as an assertion or decla-
3.2    Low Threshold and High Ceiling                                    ration F2.2 . We describe the pre-processing module behind these
Effective tools should be easy for novices to start with while sup-      predictions in Section 4.1.1.
porting advanced work [64]. Our system aims to make Lean’s veri-
fication power accessible without requiring Lean expertise.              4     Implementation
   First, the interface helps users connect their written reasoning to
                                                                         To support expressiveness, validation, and proof iteration, the sys-
the system’s formalization: clicking a user-written proof-step cell
                                                                         tem must meet four implementation challenges:
in the central panel displays the corresponding informalized Lean
interpretation in the right panel F2 . A natural-language step may             • Interpret free-form reasoning. The system must be able
map to multiple informalization cells when it contains multiple                  to interpret student reasoning even when it is incorrect,
smallest progression units (further explained in Section 4.1.1), as              ambiguous, or incomplete.
LeanSide: A Formally Verified Co-Reasoning System for Natural-language Proofs




Feature 1: Input support
                                                                                                                                                                   Feature 3: Lean
 F1.1: Image to Latex                                                                                                                                              code panel
                                                                                           F2.1: example of correct assertion   F2.2: example of declaration       Click “See Lean Code >”
                                                                                          LeanSide Compiler                                                        to open this panel




                                                                                                                                F2.3: example of wrong assertion




Feature 5: 

Ambiguity Resolution                   Feature 4: Next step hint
                                       Appear when every step is correct but the proof
                                       is incomplete

                                                                                          Feature 2: Informalization visualization



Figure 3: The User Interface. Students use the system by uploading handwritten proofs, or typing in. In this snapshot, a student
has already uploaded an image of their proof and completed the verification process. The resulting feedback is displayed.

       • Preserve the student’s reasoning path faithfully. The                           module builds on the pre-processing system of Guo et al. [26]. It has
         system must faithfully auto-formalize and informalize stu-                      two goals: (1) to resolve ambiguity in the natural-language proof
         dent reasoning. This differs from common auto-formalization                     so that the proof can be more reliably translated into Lean, and (2)
         settings, where the primary goal is to produce compiled                         to parse the proof into the smallest progression units. We define
         Lean code for a target theorem. In our system, silently re-                     a smallest progression unit as a minimal, self-contained statement,
         pairing a flawed argument or altering the proof path would                      at the level of content expressed by the student, that includes one
         undermine the student’s ability to see whether their own                        antecedent, one consequent, and evidence(s).
         reasoning was understood and verified.                                             Our system resolves three common ambiguities in student proofs
       • Judge accurately at the course granularity. The system                          through a three-stage chain adapted from Guo et al. [26]:
         must accurately determine whether each proof step is valid.
                                                                                                   • Referential ambiguity. The system first identifies referen-
         In an educational setting, correctness also depends on gran-
                                                                                                     tially ambiguous terms whose intended referents are un-
         ularity: a proof may be formally valid but pedagogically
                                                                                                     clear and predicts those referents. At this stage, the proof
         unacceptable if it skips an instructor-defined intermediate
                                                                                                     remains a single piece of text and is not yet parsed into
         step. The system therefore needs to identify both incorrect
                                                                                                     steps.
         steps and steps whose reasoning gap is too large for the
                                                                                                   • Action-type ambiguity. The system then parses the proof
         course context.
                                                                                                     according to action type, where the ambiguity is whether
       • Responsiveness. The system must return feedback quickly
                                                                                                     a step functions as an assertion or a declaration. Asser-
         enough to support an interactive co-reasoning loop. Com-
                                                                                                     tions progress the proof by deriving new information from
         mercial auto-formalization systems that handle research-
                                                                                                     known results, hypotheses, or unsolved goals, while declara-
         level mathematics can be slow [44], while proof tutoring
                                                                                                     tions set up necessary context without directly progressing
         requires students to revise, resubmit, and compare feed-
                                                                                                     the proof [26, 84]. Based on student proofs in practice, we
         back repeatedly. The system therefore balances verification
                                                                                                     further divide declarations into five subtypes: introducing
         quality with latency suitable for real-time interaction.
                                                                                                     new variables, stating the proof goal, declaring a proof
                                                                                                     strategy, repeating known facts from the question or ear-
4.1       System pipeline                                                                            lier proof, and declaring completion by restating the final
The system consists of two main components: an auto-formalizer,                                      conclusion. The proof is segmented whenever the action
which translates students’ proof attempts into Lean and attempts to                                  type changes.
compile them, and an informalizer, which translates the generated                                  • Antecedent-consequent-evidence ambiguity. Finally, the sys-
Lean code and compiler feedback back into natural language for                                       tem parses continuous assertions into the smallest progres-
students. The auto-formalizer includes three modules: a natural-                                     sion units and predicts the antecedent, consequent, and
language pre-processor, a proof scaffolder, and a prover. All the                                    evidence for each unit. This step addresses ambiguities
modules are LLM-based. Figure 4 explains the detailed architecture                                   where students write multiple assertions continuously and
of the system.                                                                                       leave some of these components implicit.
                                                                                            To support transparency, the interface displays the results of
4.1.1 Natural-language pre-processor. The natural-language pre-                          these ambiguity-resolution steps as described in Section 3.3.
processor is the first module in the auto-formalizer. It takes students’
original natural-language input, either typed directly into the sys-                     4.1.2 Proof Scaffolder. This module takes the pre-processor output
tem or entered through Optical Character Recognition (OCR). This                         and converts each smallest progression unit into a self-contained
                                                                                                                                                                             Guo et al.




                                                                                                       Mini Lemma      Proof of Step 2 lemma
                                                                                                         Library
                                                                                                                    lemma step_2 (M : ℝ) (hM : M =
                                                                                                                    s.sup' hs (fun i => |x i|)): ∃ j ∈
                                                                                                        Lemma       s, M = |x j| := by
                                                                                                        Prover          Proof_filled_in



 Free-form NL proof           Disambiguated NL proof         Lean statements with sorry                                Proof of Step 4 lemma                 Informalized NL proof
 Let M = ||x||_∞              Step 1: Declaration           set M := s.sup' hs (fun i => |x i|) 
                   lemma step_4 (M : ℝ) (hM : M =         Let M = ||x||_∞
                              Let M = ||x||_∞               with hM                                                 s.sup' hs (fun i => |x i|)) (S : ℝ)
 M = |x_j| for some index j
                                                                                                        Lemma       (hS : S = ∑ i ∈ s, |x i|) :|x j| ≤     Since M = ||x||_∞, there
                              Step 2: Assertion             lemma step_2 (M : ℝ) (hM : M =              Prover      S := by                                exists some j ∈ s such that
                                                                                                                                                           M = |x_j|.
                              M = |x_j| for some index j    s.sup' hs (fun i => |x i|)): ∃ j ∈                          proof_filled_in
 Let S = ||x||_1                                            s, M = |x j| := by sorry
                                                                                                                                                           Let S = ||x||_1
 |x_j| ≤ S                    Step 3: Decleration
                                                            set S := ∑ i ∈ s, |x i|
                              Let S = ||x||_1                                                                                                              If S = Σ_{i ∈ s} |x_i|,
                                                                                                                                                           then for every j ∈ s, |x_j|
                              Step 4: Assertion
                                                            lemma step_4 (M : ℝ) (hM : M =
                                                            s.sup' hs (fun i => |x i|)) (S : ℝ)
                                                                                                                            Complete proof                 ≤ S.
                              |x_j| ≤ S                     (hS : S = ∑ i ∈ s, |x i|) :|x j| ≤                      set M := s.sup' hs (fun i => |x i|)

                                                            S := by sorry                                           with hx

                                                                                                                    obtain ⟨j, hj, hjeq⟩ := step_2 M hM
                                                                                                   Proof
                    Pre-processor                   Proof Scaffolder                             assembler          set S := ∑ i ∈ s, |x i| with hS

                                                                                                                    have h4 : |x j| ≤ S := step_4 M j
                                                                                                                    hj S hS
                                                                                                                                                                   Informalizer
                                                                                                                    rw [hjeq]

                                                                                                                    exact h4




Figure 4: This figure shows the system pipeline. Student input (left) is auto-formalized into Lean through the pre-processor,
proof scaffolder and prover, which includes the lemma prover and proof assembler. The generated Lean code and error messages
are then informalized back into natural language. The mini-lemma library supports the lemma prover.


Lean 4 lemma statement mapped one-to-one to the student’s proof.                                    types of lemmas: rubric lemmas, which are mapped to the rubric
It does this through declaration scaffolding and assertion scaffold-                                for each problem, and side-support lemmas, which capture smaller
ing. Declaration scaffolding converts informative declarations, such                                pieces of reasoning that students are not expected to write in the
as introduced variables and stated proof goals, into Lean code,                                     course context but that the prover cannot reliably generate.
while ignoring declarations that repeat known facts or restate the                                     We curated the mini-lemma library semi-automatically. Researchers
final conclusion. Assertion scaffolding converts each assertion into                                first used stronger LLM models to generate Lean proofs for rubric
a Lean proposition, represented as prop in the lemma template                                       lemmas, then tested the library on full-credit student proofs from
lemma name (hypotheses): prop := by sorry. Following the                                            previous exams, and added side-support lemmas when the prover
proof order, each later assertion’s (hypotheses) includes all hy-                                   failed on those proofs. This process helped the library support mul-
potheses from the problem and from the aforementioned declara-                                      tiple student proof strategies. We also developed a fully automated
tions. The scaffolder does not prove these propositions; it fills the                               lemma-generation pipeline to improve generalizability, although
proof body with sorry, a placeholder that lets Lean provisionally                                   human inspection is still required to label rubric and side lemmas.
accept the proposition.                                                                             The mini-lemmas for Question 13 (Appendix A) were curated us-
   This design separates proposition generation from lemma prov-                                    ing this fully automated pipeline, with two researchers reviewing
ing to better preserve faithfulness to the student’s proof structure.                               the lemma quality to ensure the same standard as for the other
                                                                                                    questions.
4.1.3 Prover. The prover receives Lean declarations and assertion
propositions in the order expressed by the student. It consists of
two components: a lemma prover, which attempts to prove each as-
                                                                                                    4.1.4 Informalizer. The informalizer generates student-facing feed-
sertion lemma, and a proof assembler, which combines the verified
                                                                                                    back from the lemma propositions and compiler error messages. Its
lemmas to check whether they complete the proof. If any asser-
                                                                                                    outputs are shown in the informalization cells ( F2 ) and feedback
tion fails in the lemma prover, the proof assembler is not triggered;
instead, the error message is passed to the informalizer for student-                               panel ( F4 ). For each step, the informalizer translates the Lean
facing feedback. Both provers are LLM-based and use an iterative                                    proposition back into natural language using researcher-curated in-
loop: when generated code fails to compile, the prover retries using                                structions design to aligned with the notation and terminology used
the code and compiler error message until the proposition compiles                                  in the course. Note that the informalizer takes only the Lean code
or the maximum number of attempts is reached.                                                       and error message as input, but do not see the student’s proofs. We
                                                                                                    specifically designed the system this way to use Lean’s verification
   Mini-lemma library. To satisfy the system requirement of re-                                     ability without relying on the LLM’s pedagogical ability.
sponsiveness, we use faster LLMs as the prover backbone. However,                                      For step-level feedback, a successfully verified step is marked
such models usually have weaker reasoning ability, we complement                                    green . If the prover used more than one rubric lemma, the system
them with a curated mini-lemma library. The library contains two                                    informalizes those lemmas and shows a large-jump warning. If the
LeanSide: A Formally Verified Co-Reasoning System for Natural-language Proofs


step cannot be verified, the Lean compiler error is informalized into           remaining half hour, we conducted a short interview about their
a step-wise error message.                                                      experience with the system.
   For whole-proof feedback, the system considers two cases. If the                In the first 1.5 hours, students were prompted to choose ques-
proof assembler fails to compile the problem statement using the                tions to complete during the study. They were told that there was no
student’s steps, the proof is marked incomplete and the compiler                time limit for any individual question and that the study included
error is informalized into a continuation error message. If the proof           no reward or penalty based on whether they answered questions
assembler succeeds, the system counts the rubric lemmas used in                 correctly. If a participant finished one question, they were asked
the assembled proof. When more than two rubric lemmas are used,                 to start another until the allotted time was exhausted. We used
the proof is still treated as incomplete and the system shows a                 three criteria for selecting questions: (1) the student must not have
continuation hint. When two or fewer rubric lemmas are used, the                previously attempted the question using the system; (2) we encour-
proof is treated as complete, and the system may show a suggestion              aged students to choose questions for which they were less certain
based on the supporting and rubric lemmas used.                                 about the solution, so that we could observe iterative progress; and
                                                                                (3) when both criteria were satisfied, we preferred more recently
5     User study procedure                                                      released questions that were closer to the material just taught in
This section describes the study context and procedure.                         class. No participant completed all questions correctly on the first
                                                                                attempt without seeing system feedback.
5.1     Context: classroom deployment                                              Participants were allowed to consult course materials, their own
                                                                                notes, and browser search results, but could not use AI tools. When
We deployed the system in an advanced undergraduate linear alge-
                                                                                search engines displayed AI-generated overviews, we allowed par-
bra course at a university, where most students were computer sci-
                                                                                ticipants to read them as part of the search results, provided they
ence majors, with a smaller portion from other engineering majors
                                                                                had not entered the proof question directly as a query.
or graduate programs. Across 13 weeks, we deployed 14 questions,
                                                                                   Participants were instructed to think aloud while interacting
releasing one to five questions weekly or biweekly according to
                                                                                with the system. However, they were not required to think aloud
the course curriculum. Before deployment, we conducted three
                                                                                while writing proofs, to avoid disrupting their proof construction.
pilot studies with course teaching assistants or students who had
                                                                                Instead, each time participants finished a proof and before they
previously taken the course.
                                                                                submitted it for verification, we asked them to briefly walk through
   At the start of the semester, research team gave a 10-minute
                                                                                their reasoning and rate their confidence in the proof’s correctness
in-class demonstration of how to use the system. As new questions
                                                                                on a 1–5 scale. Each time participants received system feedback,
were released, we conducted one-on-one user study sessions with
                                                                                we asked three questions: (1) whether each informalization accu-
students. Students participated by voluntarily signing up for open
                                                                                rately represented what they meant (faithfulness); (2) whether the
slots. Participants received 1 point of extra credit, out of 100 total
                                                                                system feedback was accurate; and (3) for error messages, whether
course points, for attending the session; their performance and
                                                                                they were understandable, relevant, and useful. Participants were
whether they completed the proof during the session did not affect
                                                                                prompted to comment on any of these topics and were also free to
this credit. The system logged all student actions.
                                                                                raise other comments.
                                                                                   In the final half hour, participants were interviewed about their
5.2     Participants
                                                                                experience using the system, including how it compared with using
In total, we conducted 27 user study sessions. Two sessions were                an LLM or attending an in-person office hour. Participants who
unusable for technical reasons, one for recording failure and one for           had not previously opened the Lean code panel were also invited
a student who was not following the class context and thus was not              to open it once. The researchers briefly explained how to read the
able to understand and attempt to answer the question. Therefore,               code, and participants were asked whether the code provided any
the analyses presented in this paper are based on the remaining 23              useful extra information not visible in the platform.
sessions. Participants had a similar distribution of majors (14/23 are
Computer Science), class years (21/23 are undergraduate students),
and grades as the full class (details in Appendix C).                           5.4    Analysis and Evaluation
   22 participants had used the system at least once before attending           We extracted five types of information from each user study session:
the study session, while the remaining one knew how to use it from              (1) expert-evaluated system performance: whether the system’s
the classroom demonstration. 6 participants reported that they had              feedback was faithful and accurate according to the definitions
heard of Lean, and 2 reported that they had tried Lean through an               in the implementation section; (2) perceived system performance:
introductory game [9], but none of the participants had sufficient              whether the student thought the system had auto-formalized faith-
Lean knowledge to write a proof, even one simpler than the course               fully and provided accurate feedback; (3) proof progress: whether
material, on their own.                                                         each student modification was effective, incorrect, or unrelated;
                                                                                (4) students’ open-ended comments after receiving each piece of
5.3     One-on-one User study protocol                                          feedback; and (5) students’ answers to the predefined interview
Each study session lasted two hours. We first spent 5 minutes es-               questions.
tablishing rapport and asking participants about their backgrounds                 Assessing (1) and (3) required mathematical knowledge of the
and experience. Then, during the first 1.5 hours, students wrote                course material. We therefore recruited two researchers who had
proofs and iterated on them using the system’s feedback. In the                 taken or audited the course and were familiar with the course
                                                                                                                                                                                                                              Guo et al.




    (1) P2 lacked a clear strategy and                                      (2) P2 received an error message as he expected, and he               (3) P2 searched the browser for “Frobenius norm trace” to find hints for
     entered several tentative steps.                                                commented this message as confusing.                                                   getting started.

                                                                                                                     LeanSide Compiler                                                                    LeanSide Compiler
                                  LeanSide could not verify step 4, 5, 6. Check the compiler panel for details.




(4) A search result gave P2 an insight,                                         (5) P2 received an error message and he commented it               (6) P2 revised the proof, and all steps were verified. After confirming
 prompting him to write a new proof.                                                       as understandable and accurate.                           that each step matched his intent, he submitted the assignment.


                             Figure 5: An usage example of how student iterates on one problem from start to end


material. The two researchers independently judged 20% of the                                                                            check whether each system interpretation matched his intent; after
sessions (6 participants). When disagreements arose, we consult                                                                          checking every step, he submitted the assignment.
the course instructor to make the final decision. We refer to these
two researchers and the instructor as the expert group. For (2),
we used think-aloud data; when students did not comment, we
prompted them with questions such as “Do you think this claim is
actually what you meant?” and “Do you think this error message is                                                                        7   Prerequisites for natural-language access to
correct?”. We then made a binary judgment for each informalization.
For (4) and (5), we followed a reflexive thematic analysis approach,
                                                                                                                                             verification
beginning with inductive coding of a subset of sessions, iteratively                                                                     We listed faithfulness and accuracy as the requirement for Lean to
refining candidate codes and themes, and then using the resulting                                                                        be accessible through natural language, thus, in this section, we
themes to guide analysis of the remaining data.                                                                                          evaluate the system’s performance on these two criteria. The expert
                                                                                                                                         group manually reviewed all natural-language proofs produced in
                                                                                                                                         the user studies and the generated Lean code from all study sessions.
                                                                                                                                         This section reports the system’s performance. Figure 6 shows the
6      An example of the system usage                                                                                                    whole proof performance (left), and the step-wise performance
To illustrate the complete interaction trajectory, we present an ex-                                                                     (right). In this figure and the following sections, we use correct and
ample of one participant’s end-to-end interaction on a problem                                                                           incorrect to denote the expert assessment of a student step’s ground
that includes both helpful and unhelpful feedback. We also en-                                                                           truth correctness; accurate and inaccurate to denote whether the
courage the reader to watch the attached video figure for better                                                                         system’s judgment matches that ground truth; and faithful and
understanding about the user workflow. Participant 2 (P2) began                                                                          unfaithful to denote whether the auto-formalization preserves the
without a clear strategy and entered several tentative steps, includ-                                                                    student’s original input.
ing repeated hypotheses and familiar facts. After clicking Verify, P2                                                                       For whole-proof performance (Figure 6, left), we collected 137
received an error message that he found confusing and unhelpful                                                                          proofs: 56 (41%) were fully correct, 57 (42%) contained at least
for making progress (reasons in Section 7.2.2), so he searched the                                                                       one erroneous step, and 24 (18%) had only correct steps but were
browser for guidance. He identified a plausible strategy, rewrote the                                                                    incomplete. The system maintained a very low false-positive rate
proof on paper, and uploaded it again. In subsequent iterations, P2                                                                      for detecting incorrect and incomplete proofs, while marking 11/56
judged the feedback as accurate, corrected a step accordingly, and                                                                       (20%) fully correct proofs (according to the rubric) as containing an
eventually verified every step. A top banner then prompted him to                                                                        error and 4/56 (7%)fully correct proofs as incomplete.
LeanSide: A Formally Verified Co-Reasoning System for Natural-language Proofs


                                Whole proof performance                                                                          Step-wise performance

              Expert assessment             System                                                        Expert assessment                 System                   System
                of ground truth         Performance on                                                      of ground truth            Performance on            Performance on
                 correctness               accuracy                                                          correctness                 faithfulness               accuracy
              [correct, incorrect,   [accurate, inaccurate]                                               [correct, incorrect,       [faithful, unfaithful]   [accurate, inaccurate]
                  incomplete]                                                                                 incomplete]
                                                                                                                                                                                       2 incorrect steps are
                                                                                                                                            22 incorrect                               judged inaccurately
                                                              57 proofs accurately
                                                                                                                                            & unfaithful
                    57 proofs 
                               marked as incorrect
                    incorrect                                                                                                                                                          93 incorrect steps are
                                                                                                           117 incorrect                    95 incorrect                               judged accurately
                                                                                                               steps                         & faithful



                                                                                                                                                                                       40 correct steps are
137 proofs
                                                   11 proofs inaccurately                                                                                                   judged inaccuratly
1159 steps                                                    marked as incorrect
                  56 proofs
                                                                137 proofs

                 fully correct                                41 proofs accurately          1159 steps
                                                              marked as correct
                                                                                                                                   1020 correct steps
                                                                                                           1038 correct            are auto-formalized
                                                                                                              steps                 and informalized
                                                              4 proofs inaccurately                                                     faithfully                                     980 correct steps are
                                                              marked as incomplete                                                                                                     judged accurately
                   24 proofs

                  incomplete
                                                              22 proofs accurately
                                                              marked as incomplete

                                                              2 proofs inaccurately                                                     18 correct &
                                                                                                            4 steps too                unfaithful steps
                                                              marked as complete
                                                                                                            ambiguous


Figure 6: This figure shows the system’s faithfulness and accuracy performance: the left side shows whole-proof performance,
and the right side shows step-level performance. We use correct and incorrect for expert-assessed ground truth, accurate
and inaccurate for whether the system’s judgment matches that ground truth, and faithful and unfaithful for whether
auto-formalization preserves the student’s original input.


   As the faithfulness and accuracy is measured by steps, we also                                   the auto-formalization of one step is unfaithful and Section 8.2.4
calculate the total number of steps1 demonstrated in Figure 6, right.                               further explains what does the student do when facing unfaithful
In total, serving as ground truth, we have 1038 expert evaluated                                    auto-formalized steps.
correct steps, 117 (11%) wrong steps and 4 steps which are too                                         The second cause occurred when students wrote steps that were
ambiguous to judge correctness. The correct number is more than                                     vague or ambiguous along one of the three ambiguity types, math-
incorrect ones as in an incorrect proof, there is often only one or a                               ematically trivial, or not intrinsically propositional, and the auto-
few steps are wrong, while the rest steps are valid. The following                                  formalization produced a stronger claim that human evaluators
paragraphs evaluate step-level performance and explain the reasons                                  judged inconsistent with the student’s intended meaning. Section
for unfaithfulness and inaccuracy.                                                                  8.2.2 explains how student make use of these stronger claims to
                                                                                                    progress on their proofs.
7.1       System performance on faithfulness
Expert group judged that 18/1038 (2%) of correct steps and 22/117                                   7.2     System performance on accuracy
(18%) of incorrect steps are unfaithful. Most unfaithful cases arose
during auto-formalization. Three cases involved errors in both                                      7.2.1 Step-wise accuracy. Measuring accuracy for unfaithful steps
auto-formalization and informalization, and one edge case due to                                    is not reasonable, so the accuracy is only measured within the
informalization unfaithfulness alone.                                                               faithful steps. Expert judge that for 40/1020 (4%) of correct steps,
   Auto-formalization unfaithfulness had two main causes. One                                       the system is being extra stingy or not accurate and judged correct
common cause (12 cases) occurred when a student made a small                                        step as wrong. The expert group judged step-level accuracy with
error in an incorrect step, such as omitting a transpose and therefore                              respect to each question’s rubric: if a student step was more granular
multiplying matrices with incompatible dimensions. When the                                         than a rubric item, the step was judged incorrect even when it was
proof scaffolder module (Section 4.1.2) tried to auto-formalize the                                 mathematically valid.
step, the Lean statement could not compile unless this error was                                        Inaccuracy had two main causes. First, the prover (Section 4.1.3)
fixed, causing the scaffolder’s compiler-guided loop automatically                                  sometimes failed to prove a mathematically valid proposition at the
corrected it. Despite the scaffolder prompt’s instruction to preserve                               expected granularity, either because the step followed an uncom-
the student’s meaning even when it is incorrect, these small formal                                 mon proof strategy that had not been tested when constructing the
invalidities were the pipeline’s most likely source of unfaithful auto-                             mini-lemma library, or because the step was mathematically valid
correction. Section 8.1.2 explains how does student judge whether                                   but not relevant to any solution strategy. In both cases, because
                                                                                                    the mini-lemma library was built around expected solution paths,
1 the steps used here is measured by minimal independent step defined in the Section
                                                                                                    it did not contain the lemmas needed to prove the step. Since our
4.1.1, as the student divided step do not have a fix size, some student put all reasoning
in one cell, while some put each one equation in one cell, so to avoid inconsistency,               prover prioritizes responsiveness over proving arbitrary mathemat-
the system performance is measured using the minimal independent step.                              ical propositions, these steps failed to verify.
                                                                                                                                         Guo et al.


   Second, students sometimes did not explicitly declare the types           In each iteration, students fell into one of three outcomes: they
or dimensions of new variables. For example, in a problem involving       made progress, became stuck or diverted, or, when facing possi-
singular value decomposition, a student might write 𝑃 = 𝑈 Σ𝑉 with-        bly inaccurate feedback, they re-verified the same proof or added
out specifying the types and dimensions of 𝑈 , Σ, and 𝑉 ; the proof       more details to help the system understand their proof. Students
scaffolder could then formalize them as arbitrary variables, such as      submitted 137 proofs across 50 problems. After excluding final
real numbers. Although humans often omit these details as unspo-          submissions that did not lead to another iteration, we coded 87
ken conventions, the system may fail under this under-specification.      iterations (Figure 7): 52 (58%) led to effective progress, 25 (29%)
This case could be classified as either unfaithful or inaccurate; here,   were not useful or involved getting stuck or diverted, and 11 (13%)
we label it inaccurate. For both causes, we expect the inaccuracy         involved reverification or adding more granular details to support
rate to decrease as the underlying technology improves. Section           the prover.
8.1.1 further explains how the student judge whether the system
accurately judged their step.                                             8.1    Could participants assess the system’s
   In theory, the system would never judge an faithfully auto-                   accuracy and faithfulness?
formalized incorrect step as correct, as lean would never able to
                                                                          To revise their proofs using system feedback, participants first
compile it, however, in real usage, there is one edge case which
                                                                          needed to judge whether the feedback faithfully represented their
judged incorrect step as correct, because that step has been wrongly
                                                                          reasoning and was mathematically accurate. We compared their
classified as an assumption—repeat known, as mentioned in Section
                                                                          judgments with those of our expert group. Agreement was high:
4.1.2, the repeat known assumptions are not formally verified.
                                                                          participants matched the experts on 87% of faithful steps and 83%
                                                                          of unfaithful steps, as well as 91% of accurate feedback and 99% of
7.2.2 Error-message understandability. Even when the system accu-         inaccurate feedback.
rately judged a step’s correctness, its error message did not always      8.1.1 How do participants judge a claim as inaccurate? We observed
explain the mistake in an understandable way. The expert group            two main ways students identified inaccurate step-level or contin-
therefore separately evaluated whether each error message iden-           uation error messages. Most commonly, students relied on their
tified the step’s mistake in the way a human collaborator would.          own mathematical judgment, especially when the disputed step
To isolate the usefulness of the Lean error itself from the pedagog-      was easy to verify from the local context — for example, when it
ical value of an LLM, the informalizer prompt included only the           directly applied a theorem taught in class. Lean could nevertheless
Lean error message and Lean lemma declaration, not the student’s          fail to verify such steps when the required theorem was absent from
original proof.                                                           Mathlib or our mini lemma library (Section 4.1.3), or when a trivial
    We evaluated the understandability of each feedback types. Ex-        informal claim required a non-trivial formal proof. Thus, steps that
pert judges found that 61/97 (63%) of step-level error messages           students considered easy were not always easy for Lean to verify.
accurately reflected what was wrong in the step, compared with            P2, P11, P19 all encountered steps that they were confident were
3/13 (23%) of continuation error messages and (11/13)85% of con-          correct despite receiving error messages. P11 explained this local
tinuation next-step hints.                                                judgment process:
    Step-level error messages were difficult to understand mainly
                                                                                      I might not be confident that the whole proof
because of a granularity mismatch. When students wrote a state-
                                                                                      is correct, but it’s much easier to decide if
ment as a single assertion, they often treated it as not needing
                                                                                      one step is correct. When I first look at the
further explanation in the course context. Lean errors, however,
                                                                                      error, I will try to diagnose whether the error
often reflected failures in lower-level proof obligations, making the
                                                                                      is on my side or on the system’s side. The
feedback more granular than the student’s step, thus not under-
                                                                                      error message is local to the claim, so if I can
standable.
                                                                                      confirm the claim is correct, then I will assume
    Continuation error messages had a similar limitation: when the
                                                                                      it’s a system error.
proof assembler failed to complete the Lean code for the proof, it
returned a reason why the whole proof was not closed, but this               Second, students recognized an error message as inaccurate
reason was not necessarily at the user’s granularity. By contrast,        when it clearly fell outside the local mathematical context or oper-
continuation next-step hints were more understandable because             ated at a finer granularity than their intended proof. One example is
they were informalized from the mini-lemma library, which was             the inaccurate continuation error message discussed in Section 8.3.2
mapped to rubric items and designed to stay within the course             and shown in Figure 11.
context.                                                                     Without either cue, students had less basis for evaluating the
                                                                          feedback and were more likely to pursue an incorrect direction.
                                                                          When students judged an error message as inaccurate (11 itera-
8   User study findings                                                   tions), they either (1) re-verified the same input in the hope that
                                                                          the prover would verify it, (2) added more detail to help the prover,
This section examines how students unable to author Lean proofs
                                                                          or (3) stopped once they had localized the issue to a step they were
independently accessed Lean-backed verification through LeanSide.
                                                                          confident was correct.
We report on (1) how students assessed the system’s faithfulness
and accuracy, (2) when they progressed or got stuck, and (3) when         8.1.2 How do participants judge a claim is unfaithful? Students
the interaction increased their confidence.                               primarily judged faithfulness by assessing whether their original
LeanSide: A Formally Verified Co-Reasoning System for Natural-language Proofs




Figure 7: Distribution of coded revision outcomes. Most iterations led to progress (52 iterations, 58.6%), while 25 iterations
(28.7%) were not useful, involved getting stuck, or diverted students from productive proof paths, and 11 iterations (12.6%)
involved reverifying or adding under-granular details. The labels show the progress and breakdown types analyzed in this
section.


                                                                                                       not recognized. Step-level error messages, when accurate and un-
                                                                                                       derstandable, helped students repair both major misconceptions
                                                                                                       and subtle mistakes. For Q13, P12 overlooked a key constraint (Fig-
      LeanSide could not verify step 3, 4. Check the compiler panel for details.
                                                                                   LeanSide Compiler   ure 8. The error message drew attention to this omission: “Oh right!
                                                                                                       Because 𝑥 ⊤ is also supposed to be orthogonal to the first eigenvector,
                                                                                                       it actually can’t be 𝜆0 .” P12 then revised the proof strategy. The
                                                                                                       system also caught subtle errors, of which we include an example
                                                                                                       in Appendix B.
                                                                                                           Understandable continuation error messages could similarly help
                                                                                                       students complete unfinished proofs. These messages were gener-
                                                                                                       ally effective when students had already made valid progress and
                                                                                                       needed only one or two additional rubric items. For Q8, P2 recog-
                                                                                                       nized that the Cauchy–Schwarz inequality was relevant but did not
                                                                                                       know how to apply it. The continuation error message explained
Figure 8: This figure shows an understandable and accurate                                             its role, allowing P2 to close the logical gap and continue the proof
error message output by the system.                                                                    (More details about this example is explained in Appendix B).

                                                                                                       8.2.2 Progress type 2: Making high-level ideas more rigorous through
idea and the informalization were mathematically equivalent or
                                                                                                       informalization and ambiguity resolution (9 iterations). Students also
could be trivially converted into each other. In practice, this often
                                                                                                       began with a conceptual intuition but were unsure how to express
began with noticing that the informalization “looked different”
                                                                                                       it mathematically. After first reading a problem, P27 explained, It’s
from their original input. However, informalizations rarely looked
                                                                                                       hard for me to translate an expression before I have fully formulated
exactly the same as the input, even when they were faithful. Thus,
                                                                                                       my thinking.” Students therefore submitted descriptive or tentative
judging faithfulness required students to use their mathematical
                                                                                                       reasoning and used the system’s interpretation to develop it. P14
knowledge to decide whether the input and output were equivalent.
                                                                                                       described a proof as fairly conceptual,” adding, Even in the exam,
We observed three cases in which students did not notice that a
                                                                                                       maybe the grader would not accept that, but maybe a mathematician
claim was unfaithful, all of which led to unproductive iterations.
                                                                                                       will say this looks good. Maybe demonstrate this part more clearly.”
This usually occurred when the system proved an unfaithful claim
                                                                                                       Similarly, P12 wrote, This proof is hand-wavy and I yap a lot. Let’s
and marked the step as correct, causing the indicator beside the
                                                                                                       see what the system says and we could iterate.” The system helped
step to appear green . Students typically paid more attention to
                                                                                                       students turn such ambiguous expressions into rigorous arguments
gray steps with error messages and revised those steps first, as
                                                                                                       in two ways.
a result, they sometimes missed the unfaithful claims. In Section
                                                                                                          First, when an expression matched one of the three ambiguity
9.4, we discuss the design challenge of prompting users to check
                                                                                                       types described in Section 4.1.1, the interface displayed the system’s
faithfulness, as well as the design decisions we explored and their
                                                                                                       predicted interpretation for students to inspect. Even incorrect pre-
effects on users’ attention to faithfulness.
                                                                                                       dictions were useful because they revealed where an expression
                                                                                                       had confused the system. For example, in several cases (P2, P22,
8.2        How do participants make progress?                                                          P24, and P26), action labels in the informalization cells helped stu-
8.2.1 Progress type 1: Repairing proofs with accurate, understand-                                     dents assess whether their intent had been captured. P26 initially
able step-wise or continuation error message (23 iterations). A com-                                   wondered, I am not sure whether the system could understand I’m
mon starting point was a proof containing error(s) the student had                                     repeating the definition, or should I delete these steps?” Seeing the
                                                                                                                                                                                                                         Guo et al.



                                                                                      LeanSide Compiler   LeanSide Compiler                                                                          LeanSide Compiler
   LeanSide could not verify step 2, 3, 4, 5. Check the compiler panel for details.                                              LeanSide could not verify step 3, 4. Check the compiler panel for
                                                                                                                                 details.




                                                                                                                              Figure 10: This figure shows a comparison between the Lean-
                                                                                                                              Side error message and an LLM output with the same problem
                                                                                                                              and answer.

Figure 9: This figure shows an accurate but less understand-                                                                  conclusion within that step and return a large-jump warning expos-
able error messages of step 2 and 3.                                                                                          ing the missing intermediate reasoning. These warnings therefore
                                                                                                                              functioned similarly to continuation hints. Appendix B display one
“Repeat Known” label confirmed that the system had understood                                                                 such example.
the step. In two cases, antecedent, consequent and evidence ambigu-                                                               Overall, students described next-step hints, including those pre-
ity resolution also helped (P19, P4). For example, P19 used “Hence”                                                           sented as warnings, more understandable and helpful than contin-
twice in one step, but the first instance referred to earlier reasoning                                                       uation error messages. They described it as directly actionable: “It
rather than the immediately preceding step. The generated proposi-                                                            tells me how to do it” (P4), “It’s kind of funny that this seems a lot of
tion did not match his intent, revealing the ambiguous antecedent.                                                            help, seems like these are alternatives, not do all of them” (P11), and
P19 therefore noticed and resolved this ambiguity.                                                                            “This is definitely very helpful” (P18).
   Second, informalization helped students develop conceptual
ideas that fell outside these predefined ambiguity types. For Q13                                                             8.2.4 Progress type 4: Discovering mistakes through unfaithful auto-
(Appendix A), P18 input an ambiguous, high level proof idea into                                                              corrections (11 iterations). As described in Section 7.1, the autofor-
the system with some missed cases:                                                                                            malizer sometimes unfaithfully corrected local mistakes. Students
                                                     Í                                                                        discovered their error by noticing that the informalized verified
              Since the quadratic form 𝑦𝑇 𝐴𝑦 = 𝑛−1     𝑖=0 𝜆𝑖 (𝑦 ·
                 2                                                                                                            proposition differed from their input step. These errors were typi-
             𝑒𝑖 ) , we know that the weight assigned to
                                                                                                                              cally small, such as omitting a transpose and thereby multiplying
              each eigenvalue is the dot product between
                                                                                                                              matrices with incompatible dimensions.
             𝑦 and the corresponding eigenvector. When
             𝑦 = 𝑣 1 , this means all the weight is assigned                                                                  8.2.5 Progress type 5: Resolving difficult feedback with external
              to 𝜆1 . In other scenarios, the weight is dis-                                                                  resources (11 iterations). Students could still progress when feedback
              tributed across the other eigenvectors. How-                                                                    was accurate but less understandable than human-tutor feedback
              ever, in these other cases, it is strictly better to                                                            (Section 7.2.2), although doing so required more time and greater
              allocate more weight to the largest eigenvec-                                                                   reliance on external resources such as browsers and textbooks. For
              tor since doing so yields the largest weighted                                                                  Q12 (Figure 9, P20 was confident that a matrix has a positive norm
              sum.                                                                                                            and therefore rejected the step 2 message with comments “∥𝑄 ∥
These steps were not mathematically precise statements, but were                                                              is not a defined operation.” P20 searched, “Can you take the norm
along a path that could get to a rigorous proof. The informalization                                                          of a non-square matrix?” and treated an AI-generated overview
solidified the student intuition through propositions propositions                                                            beginning with “Yes, you can...” as confirmation without reading
representing the weight allocation process and normalization con-                                                             further. However, the step 3 message—“a matrix and a single number
straint on the weights, and suggested a rigorous approach to the                                                              cannot be equal”—prompted P20 to reconsider. Returning to the
proof. P18 commented that this “makes the proof more robust.”                                                                 search results, P20 read that the answer referred to specific norms,
                                                                                                                              “...such as the Frobenius and induced operator norms,” and recognized
8.2.3 Progress type 3: Advancing with continuation hints and large-
                                                                                                                              that the step 2 message was correct.
jump warnings (6 iterations). Students sometimes became stuck
midway through an argument or did not know how to begin. They
therefore entered given conditions or potentially relevant theorems
                                                                                                                              8.3              When do students get stuck or divert from
as tentative starting points. When these preliminary steps were                                                                                correct directions?
correct, the system could return informalized future proof steps as                                                           8.3.1 Stuck type 1: Struggling with accurate but hard-to-understand
a continuation hint. As reported in Section 7.2.2, these hints were                                                           feedback (16 cases). One common source of not understandable
generally understandable, and six students used them to make valid                                                            feedback, discussed in Section 7.2.2, was a mismatch in granularity:
progress (Appendix B).                                                                                                        Lean exposed low-level proof obligations for steps that students
   Unexpectedly, students also used large-jump warnings to ad-                                                                considered sufficiently explained. Students then struggled to con-
vance incomplete proofs. This occurred when a student included                                                                nect the feedback to the higher-level flaw. For example, Figure 10
the conclusion as the final step without providing a complete argu-                                                           shows such an error message. P12 spent additional time searching
ment. Particularly for simpler problems, the prover could justify the                                                         lecture notes to understand the issue. By contrast, when given the
LeanSide: A Formally Verified Co-Reasoning System for Natural-language Proofs


                                                                                                 student’s step is indeed incorrect and thus the system generate an
                                                                                                 error message, it would requires student’s knowledge to understand
                                                       LeanSide Compiler
                                                                                                 and act upon the error message. In two cases, Students followed
                                                                                                 the misleading feedback or misunderstand an accurate feedback.

                                                                                                 8.4    Participants gained confidence from the
                                                                                                        verified results
                                                       Iteration 2: output a continuation hint
                                                                                                 A central motivation for formal verification is confidence in logical
                                                                                                 validity. We therefore assessed whether the system could carry this
    Iteration 1: output a continuation error message                                             benefit into a natural-language interface by asking students to rate
                                                                                                 their confidence in each proof on a 1–5 scale and explain their rea-
                                                                                                 sons. We observed that when the system displayed a whole proof
                                                                                                 as verified for a proof that students were not confident in, their con-
                                                                                                 fidence did not immediately increase. Instead, confidence increased
Figure 11: This figure shows a comparison between an unhelp-                                     substantially as students checked whether each step matched their
ful continuation error message and a useful continuation                                         intended meaning, especially for steps they judged to be both faith-
hint. In the first iteration, the system generated a confusing                                   fully translated and verified (P2, P4, P9, P11, P26). P4 commented,
continuation error message; after the student re-verified the                                    “I feel extremely confident that this is correct because it is verified,”,
same proof, the system produced a useful continuation hint.                                      P2 and P11 said they trusted the system when it marked a step as
                                                                                                 correct. P26 added, “I trust that my steps are rigorous for the verified
same problem and solution, ChatGPT-4.0 identified the issue at a                                 claims more than LLM.”
higher level.                                                                                        Students gradually gained trust through the process of check-
   In contrast, human tutors can draw on pedagogical strategies                                  ing that each informalized claim faithfully represented what they
that our Lean-backed pipeline did not support, such as refuting                                  meant. Confidence increased especially when a step they had sus-
an invalid claim with a counterexample [22], diagnosing an issue                                 pected might contain a gap was verified but accompanied by a
in the overall proof strategy rather than only the current step [3],                             large-jump warning or a continuation suggestion that clarified the
or explaining an unfamiliar idea through an analogy to familiar                                  missing details. For example, before verification, P9 rated their con-
knowledge [59].                                                                                  fidence as 2. Seeing that the proof was verified did not immediately
                                                                                                 increase this confidence: “Oh, it says it’s correct, that’s surprising.”
8.3.2 Stuck type 2: Lacking a high-level proof strategy (7 cases).                               However, after checking that each step matched their intent and
Earlier, we showed that continuation hints and, less often, under-                               seeing that the uncertain step had a large-jump warning explaining
standable continuation error messages could suggest plausible next                               the missing details, P9 became more confident in the proof. We also
steps. This support was less effective when students had no devel-                               observed that P6, P9, and P13 became gradually more confident
oped proof strategy and submitted reasoning far from a complete                                  as they corrected mistakes or resolved ambiguous parts of their
proof. In these cases, the proof assembler usually failed at an in-                              proofs.
cidental proof obligation, producing a low-level error rather than
the high-level strategy the student needed. P16’s attempt on Q12                                 8.5    Could students obtain extra information
illustrates the contrast (Figure 11). After restating several given                                     from reading Lean code?
conditions, P16 became stuck. On the first run, the proof assembler
failed and produced a continuation error mentioning a “conjugate                                 To evaluate whether Lean code provided useful information beyond
transpose.” P16 rejected this message because the course considered                              the interface, we invited students during the post-interview to read
only real numbers and reran the same partial proof. On the sec-                                  the generated Lean code. After a five-minute introduction to basic
ond run, the assembler completed the proof and returned a useful                                 syntax, students read one proof lemma corresponding to one of
continuation hint, which enabled P16 to progress.                                                their steps and could ask clarification to any part of the code. We
    Additionally, the system could not distinguish strategically useful                          then asked whether the code provided any helpful information not
steps from all mathematically correct steps. Consequently, listing                               already shown in the interface.
every potentially relevant fact was ineffective. This problem was                                   Overall, 20 of 23 students said it was useful to know that code
compounded when a correct but irrelevant textbook fact fell outside                              existed behind the feedback, but that reading the code did not give
the mini lemma library and was marked unverified, misleading                                     them additional information they needed. P4 commented that the
students into thinking that the fact itself was incorrect.                                       Lean code felt unfamiliar and that “if it were just me, I would never
                                                                                                 open the panel and try to read the code.” P11 said the language was
8.3.3 Diversion: Struggling to evaluate or act on local feedback (2                              daunting and that, even with instructions, they could mostly read
cases). The reason for students to drive into wrong direction is                                 only the comments. P14 similarly commented, “I trust the system
insufficient math knowledge to react on a step-wise error message                                more because I know there is code behind, but for now, I did not get
no matter whether the message is accurate. For both cases where (1)                              much extra information from it.”
the student’s step is correct, however the system is inaccurate and                                 The remaining three students found the comments inside the
failed to prove the step thus generate an error message, or (2) the                              Lean lemmas useful. In all three cases, students had written steps
                                                                                                                                              Guo et al.


that were verified but were not fully sure why the steps were correct.         user’s granularity. This was not due to formal verification alone,
For P6, the system verified all steps, but P6 remained unsure about            but our system design choice for step-by-step auto-formalization.
the evidence supporting one of the steps. P6 commented that the                Prior work in human-AI collaboration has shown that LLM out-
feedback “tells me it is correct, but I don’t know how it is correct.” After   puts can introduce useful directions, but can also unintentionally
opening the Lean code panel, the comments helped P6 understand                 distract users from their original initiative [34, 46]. Plausible but
the evidence and gain confidence. P24 used the comments in the                 misaligned outputs can pull users away from their original line
Lean Code to discover that a verified step was true only for a trivial         of reasoning, forcing them to monitor and repair the system or
reason: both sides reduced to 0 = 0, rather than for the reason the            follow its suggested direction [17, 62, 89]. An FVCR system can
student intended. P7 used the comments to interpret a confusing                reduce this risk by designing the system to always follow the user’s
large-jump warning: the step was circular because the prover had               reasoning path. In our system, the unit of preservation is the pre-
used the final conclusion to prove it. After reading the comments,             processed smallest progression unit: we do not require the system
the warning became understandable. The comments in the Lean                    to preserve lower-level decompositions inside that unit. This unit is
code represent a detailed logic trace below the user’s granularity.            context-dependent and can be customized to the reasoning task. For
These three cases show the potential usefulness of such traces and             example, in a tax-reasoning system, the unit might be one claimed
students’ trust in them.                                                       inference: given a taxpayer’s income, deductions, filing status, or
                                                                               transaction history, the system would preserve the user’s intended
9     Discussion                                                               application of a specific tax rule and then verify whether the stated
In the previous section, we summarized students’ perceptions of                tax consequence follows.
the system: whether they could accurately assess system perfor-                   Second, our findings also shows an FVCR system can help local-
mance, when they were able to make progress, when they became                  ize errors through low-false-positive feedback. Hallucination
stuck or diverted, and how their confidence changed. Here, we                  remains a persistent concern in high-stakes reasoning domains.
examine what explains these results. We distinguish findings that              LLM feedback can be unreliable in these settings because it may
stem from current technical limitations from findings shaped by                sound plausible while being logically wrong [8, 42, 88]. A formally
formally verified languages’ properties and our design choices.                verified backend can instead provide a stronger basis for accepting
We then discuss design implications for future formally verified               a step or conclusion when the translation is faithful. In our system,
co-reasoning (FVCR) systems, including the limitation of formal                verified steps helped students narrow down the issue: once a step
languages, the design strategies that may address them, and the                was verified, students gained confidence in its validity and could
open challenges that remain. Table 1 summarizes five capabilities              focus on unverified steps to correct faulty logic or fill the gaps. This
that a co-reasoning system may need and compares our system                    process continued until all steps were verified, or until students
with the support provided by an LLM-based assistant and a formal               used their mathematical knowledge to judge that a remaining un-
debugger.                                                                      verified step reflected prover failure rather than their own error, as
                                                                               described in Section 7.2.
9.1    What results stem from technical                                           Third, an FVCR system can provide verified reasoning sug-
                                                                               gestions. In our system, these traces appeared as continuation
       limitations?
                                                                               hints and as informal comments in the Lean code panel explaining
LeanSide was developed under the cost constraints of a classroom               how a step was proved. Both were natural-language explanations
deployment, so each verification was optimized for responsive-                 grounded in verified reasoning, and both were proven to be useful
ness and resource use. Recent commercial auto-formalizers [1]                  to students. Similar opportunities may arise in other reasoning
report higher success rates in generating compiling proofs for cor-            tasks where users need more than a validity check mark: they also
rect Lean statements. Plugging stronger models into the pipeline               need natural-language explanations of why a step follows.
would likely improve accuracy by reducing false negatives, and                    Finally, an FVCR system can help users make implicit reason-
may also slightly reduce unfaithfulness. By contrast, we do not                ing explicit. In our study, students often entered high-level or
expect stronger provers to substantially change error-message un-              ambiguous reasoning, while the system returned less ambiguous
derstandability or most student behaviors around making progress               informalizations at the user’s granularity. By comparing their input
or getting stuck, as these are more closely tied to the nature of              with these interpretations, students could notice ambiguity, clarify
formal verification and our system design choices.                             assumptions, and make their reasoning more rigorous. This sug-
                                                                               gests that formal verification can serve not only as a checker, but
9.2    What could an FVCR system provide?                                      also as a mirror for helping users refine high-level strategies into
We view an FVCR system like LeanSide could contributes four re-                precise reasoning.
sources to a human-AI co-reasoning system: preserving the user’s
reasoning path, providing low-false-positive validity checks, pro-
ducing hallucination-free reasoning feedback, and helping users
                                                                               9.3    LeanSide Limitations, and Design
iteratively make implicit reasoning explicit.                                         Implications for Future FVCR Systems
   First, our findings show that LeanSide can help preserve user               LeanSide was designed to isolate how formal language can sup-
agency through faithful representation. Although we observed                   port students’ proof iteration. Some of its limitations therefore
edge cases where the system unfaithfully auto-corrected step-level             come from deliberate design choices, which could help explain why
mistakes, LeanSide usually followed the user’s reasoning at the                students became stuck or diverged.
LeanSide: A Formally Verified Co-Reasoning System for Natural-language Proofs


                                                Table 1: Capabilities of different reasoning systems.

                Capability                                                 LLM-based assistant       Formal debugger     Lean-backed system
                Low-threshold interaction                                              ✓                     ×                    ✓
                Preserve faithfulness and user agency                           Not deterministic            ✓                    ✓
                Validity check for informal reasoning                           Not deterministic            ×                    ✓
                Verified reasoning explanations                                 Not deterministic            ×                    ✓
                Provide high-level conceptual guidance                                 ✓                     ×                    ×


   First, Lean error messages can reflect overly-granular reason-
ing, which can confuse users. The limited understandability of
step-level error messages illustrates this limitation. When students
wrote a statement as a single assertion, they often treated it as not
requiring further explanation in the course context. Lean errors,
however, often reflected failures in lower-level proof obligations,
making the feedback more granular than the student’s step and
harder to interpret. This mismatch is difficult to solve through
the Lean backbone alone. Complementary methods, such as sam-
pling counterexamples or using an LLM to generate higher-level                          Figure 12: This figure compares two inspection scenarios:
pedagogical and tutor-like feedback, can help produce more use-                         a general inspection scenario and inspection in an FVCR
ful explanations (formal verification could also be used to check                       system. In the general scenario, users must inspect both in-
whether the LLM generated feedback before showing it to users).                         terpretation and execution; in an FVCR system, the emphasis
   The second limitation is that Lean may not follow the same                           is primarily on inspecting interpretation.
strategic trace as human intuition. In our study, students found
the system useful for narrowing down local issues, but less able to
guide them toward the right overall strategy. When a student fol-                          In LeanSide, the side-by-side comparison between user input
lowed an unproductive path, several mathematically correct steps                        and system interpretation in the informalization panel makes faith-
could appear before the first incorrect step; the system flagged                        fulness inspection explicit. The open design challenge is how to
only the incorrect step, leaving the student to identify where the                      make these checks lightweight enough to avoid tedious interaction,
proof had diverged strategically. This reflects a mismatch between                      while still keeping them visible enough to hold users’ attention.
formal verification and human proof reasoning: Lean and search-                            We observed that students paid more attention to steps marked
based provers do not necessarily follow the intuitive order in which                    gray with error messages than to steps marked green, they did not
humans understand a proof, and may produce proofs that are coun-                        always check whether the system had correctly interpreted what
terintuitive or difficult to read [82]. Strategic hint generation, such                 they meant in each sentence before everything is green.
as tree-search-based methods studied in existing tutoring systems,                         To address this issue, our current design requires users to click
could therefore complement the formal verification backbone.                            “this is what I meant” or “not what I meant” for every informalized
   Together, what FVCR systems can provide and where they are                           cell before submitting the assignment. If a user clicks “not what I
limited offers guidance for future co-reasoning tool designers on                       meant,” the step returns to gray and the student must clarify and
when to use an FVCR system. It also suggests that, when using                           re-verify the proof. However, this design has limitations. Students
a formal verification system as the backbone, task-specific auxil-                      usually checked every step only after resolving all error messages
iary components can add useful “meat” around formal verification,                       and preparing to submit the assignment. As a result, participants
varying by domain and interaction need.                                                 sometimes ignored unfaithful interpretations during intermediate
                                                                                        iterations. However, an unfaithful earlier step could prevent later
                                                                                        causally related steps from being verified, increasing the likelihood
9.4     Open design challenges: faithfulness                                            of inaccurate judgments and error messages for the later step. This
                                                                                        is one reason participants became stuck or moved in the wrong
        checking and auto-detecting contextual                                          direction, as discussed in Section 8.3.
        granularity                                                                        We considered two alternative designs. First, after each verifi-
One open design challenge is faithfulness checking. In figure 12,                       cation, the system could require students to confirm “this is what
we summarize users’ inspection of a collaborative system into two                       I meant” or “not what I meant” before showing indicators and er-
categories (1) inspecting whether the system’s interpretation of the                    ror messages. However, because informalizations often differ from
presented task is faithful, and (2) inspecting whether the system’s                     the student’s original wording even when they are faithful, this
execution matches the user’s intent, which could be correspond to                       interaction could become tedious. In addition, if a student clicked
gulf of execution and evaluation [69]. We view inspection in FVCR                       “not what I meant,” the system would need to regenerate the Lean
systems as a special case of this broader inspection problem, one                       interpretation, adding waiting time while leaving open the possi-
that emphasizes (1) while placing less burden on (2).                                   bility that the new interpretation would still be unfaithful. Second,
                                                                                                                                                         Guo et al.


                                                                           11     Acknowledgment
                                                                           The authors would like to acknowledge support from: NSF CAREER
                                                                           grant ECCS-2240031, the 2023 CITRIS Institute Seed Grant, the
                                                                           UC Berkeley Instructional Technology and Innovation MicroGrant
                                                                           Program, Google and the Renaissance Philanthropy AI for Math
                                                                           2025 fund.


                                                                           References
Figure 13: Follow up questions asked by the system when a                   [1] Tudor Achim, Alex Best, Alberto Bietti, Kevin Der, Math"is F’ed’erico, Sergei
                                                                                Gukov, Daniel Halpern-Leistner, Kirsten Henningsgard, Yury Kudryashov,
student’s step is ambiguous                                                     Alexander Meiburg, Martin Michelsen, Riley Patterson, Eric Rodriguez, Laura
                                                                                Scharff, Vikram Shanker, Vladmir Sicca, Hari Sowrirajan, Aidan Swope, Matyas
similar to existing LLM interfaces, the system could ask follow-up              Tamas, Vlad Tenev, Jonathan Thomm, Harold Williams, and Lawrence Wu. 2025.
questions when the student’s input is ambiguous. We implemented                 Aristotle: IMO-Level Automated Theorem Proving. arXiv:2510.01346 [cs.AI]
                                                                                doi:10.48550/arXiv.2510.01346
this feature in the interface shown in Figure 13, but because it adds       [2] Jonathan Aldrich, Robert J Simmons, and Key Shin. 2008. SASyLF: An educa-
complexity beyond the scope of the present study, we leave its                  tional proof assistant for language theory. In Proceedings of the 2008 international
                                                                                workshop on Functional and declarative programming in education. 31–40.
evaluation to future work.                                                  [3] Serge Autexier, Dominik Dietrich, and Marvin Schiller. 2012. Towards an
    Another open design challenge is auto-detecting contextual                  Intelligent Tutor for Mathematical Proofs. Electronic Proceedings in Theoretical
granularity. Human users, such as students, often learn the accept-             Computer Science 79 (2012), 1–28. doi:10.4204/EPTCS.79.1
                                                                            [4] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W Ayers,
able granularity of reasoning from surrounding context, including               Dragomir Radev, and Jeremy Avigad. 2023. Proofnet: Autoformalizing and for-
lectures, peer discussion, and grading expectations, without anyone             mally proving undergraduate-level mathematics. arXiv preprint arXiv:2302.12433
stating it explicitly. By contrast, LeanSide required substantial effort        (2023).
                                                                            [5] Shraddha Barke, Michael B James, and Nadia Polikarpova. 2023. Grounded
to construct a mini-lemma library that encoded this granularity,                copilot: How programmers interact with code-generating models. Proceedings
through rubric lemmas and side lemmas. Even with an automated                   of the ACM on Programming Languages 7, OOPSLA1 (2023), 85–111.
                                                                            [6] Bruno Barras, Samuel Boutin, Cristina Cornes, Judicaël Courant, Jean-
pipeline, experts still had to inspect whether the specified granu-             Christophe Filliâtre, Eduardo Giménez, Héctor Herbelin, Gérard Mohring,
larity was appropriate. In mathematics education, this granularity              Amokrane Saïbi, and Benjamin Werner. 1997. The Coq Proof Assistant Ref-
is relatively visible because rubrics exist for each problem; in many           erence Manual: Version 6.1. Technical Report RT-0203. INRIA.
                                                                            [7] Christoph Benzmüller, Helmut Horacek, Ivana Kruijff-Korbayova, Manfred
other reasoning tasks, it may be far more implicit. A key open chal-            Pinkal, Jörg Siekmann, and Magdalena Wolska. 2007. Natural language dialog
lenge for co-reasoning systems is therefore how they can learn the              with a tutor system for mathematical proofs. In Cognitive Systems: Joint Chinese-
user’s expected granularity for communicating reasoning.                        German Workshop, Shanghai, China, March 7-11, 2005, Revised Selected Papers.
                                                                                Springer, 1–14.
                                                                            [8] Jessica Y Bo, Sophia Wan, and Ashton Anderson. 2025. To rely or not to rely?
10    Limitations                                                               evaluating interventions for appropriate reliance on large language models. In
                                                                                Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems.
This study has several limitations. First, the participant population           1–23.
was relatively homogeneous: all participants were recruited from            [9] Kevin Buzzard and Jon Eugster. 2023. The Natural Number Game. Interactive
                                                                                Lean 4 game. Accessed: 2026-09-11. https://adam.math.hhu.de/#/g/leanprover-
the same university, and many were majoring in Computer Science,                community/NNG4
Mathematics, or related fields. This composition was partly a con-         [10] Rafael Cabral, Tuan Manh Do, Xuejun Yu, Wai Ming Tai, Zijin Feng, and Xin
sequence of the course in which we deployed the system. Although                Shen. 2025. ProofFlow: A Dependency Graph Approach to Faithful Proof
                                                                                Autoformalization. arXiv preprint arXiv:2510.15981 (2025).
none of the participants had prior experience with Lean, they may          [11] Eason Chen, Sophia Judicke, Kayla Beigh, Xinyi Tang, Isabel Wang, Nina Yuan,
have been more familiar with formal verification than the general               Zimo Xiao, Chuangji Li, Shizhuo Li, Reed Luttmer, et al. 2026. Chat-based
population and therefore more inclined to trust the verification re-            support alone may not be enough: comparing conversational and embedded
                                                                                LLM feedback for mathematical proof learning. arXiv preprint arXiv:2602.18807
sults. In addition, their disciplinary training may have helped them            (2026).
express informal reasoning more precisely, making their inputs less        [12] Furui Cheng, Vilém Zouhar, Simran Arora, Mrinmaya Sachan, Hendrik Strobelt,
                                                                                and Mennatallah El-Assady. 2024. Relic: Investigating large language model
ambiguous than those of general users.                                          responses using self-consistency. In Proceedings of the 2024 CHI conference on
   Second, the problems selected for this study represent only a                human factors in computing systems. 1–18.
limited subset of mathematical reasoning, focusing primarily on            [13] Herbert H Clark and Susan E Brennan. 1991. Grounding in communication.
                                                                                (1991).
Linear Algebra and Optimization. This choice was motivated by              [14] Herbert H Clark and Deanna Wilkes-Gibbs. 1986. Referring as a collaborative
two factors: (1) the deployment course focused on Linear Algebra,               process. Cognition 22, 1 (1986), 1–39.
and (2) the current auto-formalization and prover modules perform          [15] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun,
                                                                                Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano,
more reliably in these domains. Consequently, the observed results              et al. 2021. Training verifiers to solve math word problems, 2021. URL
may not generalize to other areas of mathematics, where users may               https://arxiv. org/abs/2110.14168 9 (2021).
                                                                           [16] Rob Cornish, Iacopo Ghinassi, Po-Hung Yeh, Shuqi Liu, Qiyuan Xu, Haoxuan
exhibit different input behaviors and where the system may face                 Yin, Dominik Wagner, Wenda Li, Yee Whye Teh, and Luke Ong. 2026. Faith-
additional challenges.                                                          formBench: Benchmarking Faithfulness of Mathematical Chain-of-Thought
                                                                                Autoformalisation. arXiv preprint arXiv:2608.10916 (2026).
                                                                           [17] Laura Cros Vila and Bob Sturm. 2025. (Mis)Communicating with our AI Systems.
                                                                                In Proceedings of the 2025 CHI Conference on Human Factors in Computing
                                                                                Systems. Article 416, 9 pages. doi:10.1145/3706598.3713771
                                                                           [18] Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 Theorem Prover and
                                                                                Programming Language. In International Conference on Automated Deduction.
                                                                                Springer, 625–635.
LeanSide: A Formally Verified Co-Reasoning System for Natural-language Proofs


 [19] Fiona Draxler, Anna Werner, Florian Lehmann, Matthias Hoppe, Albrecht                   (2023), 102274.
      Schmidt, Daniel Buschek, and Robin Welsch. 2024. The AI ghostwriter effect:        [41] Matthew Keenan and Cyrus Omar. 2024. Learner-Centered Design Criteria
      When users do not perceive ownership of AI-generated text but self-declare as           for Classroom Proof Assistants. In Workshop on Human Aspects of Types and
      authors. ACM Transactions on Computer-Human Interaction 31, 2 (2024), 1–40.             Reasoning Assistants (HATRA). https://hazel.org/papers/learner_centered_
 [20] Kasra Ferdowsi, Ruanqianqian Huang, Michael B James, Nadia Polikarpova,                 proofs_hatra_2024.pdf
      and Sorin Lerner. 2024. Validating AI-generated code with live programming.        [42] Sunnie SY Kim, Jennifer Wortman Vaughan, Q Vera Liao, Tania Lombrozo,
      In Proceedings of the 2024 CHI conference on human factors in computing systems.        and Olga Russakovsky. 2025. Fostering appropriate reliance on large language
      1–8.                                                                                    models: The role of explanations, sources, and inconsistencies. In Proceedings
 [21] Guoxiong Gao, Yutong Wang, Jiedong Jiang, Qi Gao, Zihan Qin, Tianyi Xu, and             of the 2025 CHI Conference on Human Factors in Computing Systems. 1–19.
      Bin Dong. 2024. Herald: A natural language annotated Lean 4 dataset. arXiv         [43] Tiffany H Kung, Morgan Cheatham, Arielle Medenilla, Czarina Sillos, Lo-
      preprint arXiv:2410.10878 (2024).                                                       rie De Leon, Camille Elepaño, Maria Madriaga, Rimel Aggabao, Giezel Diaz-
 [22] Eusthathios Giannakoulias, Eleutherios Mastorides, Despina Potari, and Theo-            Candido, James Maningo, et al. 2023. Performance of ChatGPT on USMLE:
      dossios Zachariades. 2010. Studying Teachers’ Mathematical Argumentation in             potential for AI-assisted medical education using large language models. PLoS
      the Context of Refuting Students’ Invalid Claims. The Journal of Mathematical           digital health 2, 2 (2023), e0000198.
      Behavior 29, 3 (2010), 160–168. doi:10.1016/j.jmathb.2010.07.001                   [44] Gabriel Rongyang Lau. 2026. Using the Aristotle API for AI-Assisted Theorem
 [23] Google DeepMind. 2024. AI Achieves Silver-Medal Standard Solving Inter-                 Proving in Lean 4: A Formalisation Case Study of the Grasshopper Problem.
      national Mathematical Olympiad Problems. https://deepmind.google/blog/ai-               arXiv:2605.20120 https://arxiv.org/abs/2605.20120
      solves-imo-problems-at-silver-medal-level/. Accessed September 11, 2026.           [45] Florian Leiser, Sven Eckhardt, Valentin Leuthe, Merlin Knaeble, Alexander Mäd-
 [24] Neel Guha, Julian Nyarko, Daniel Ho, Christopher Ré, Adam Chilton, Alex                 che, Gerhard Schwabe, and Ali Sunyaev. 2024. Hill: A hallucination identifier
      Chohlas-Wood, Austin Peters, Brandon Waldon, Daniel Rockmore, Diego Zam-                for large language models. In Proceedings of the 2024 CHI conference on human
      brano, et al. 2023. Legalbench: A collaboratively built benchmark for measuring         factors in computing systems. 1–13.
      legal reasoning in large language models. Advances in neural information           [46] Ariel Levy, Monica Agrawal, Arvind Satyanarayan, and David Sontag. 2021.
      processing systems 36 (2023), 44123–44279.                                              Assessing the impact of automated suggestions on decision making: Domain
 [25] Chenjun Guo, Manooshree Patel, Bjoern Hartmann, JD Zamfirescu-Pereira,                  experts mediate model errors but take less initiative. In Proceedings of the 2021
      Sarah Chasins, and Gireeja Ranade. 2025. Unspoken Logic: Understanding and              CHI conference on human factors in computing systems. 1–13.
      bridging the gap between free-form and LLM-interpretable natural language          [47] Aitor Lewkowycz, Anders Andreassen, David Dohan, Ethan Dyer, Henryk
      mathematical proofs. In The 5th Workshop on Mathematical Reasoning and AI at            Michalewski, Vinay Ramasesh, Ambrose Slone, Cem Anil, Imanol Schlag, Theo
      NeurIPS 2025.                                                                           Gutman-Solo, et al. 2022. Solving quantitative reasoning problems with lan-
 [26] Chenjun Guo, Manooshree Patel, Arnav Mehta, Rayna Bhattacharyya, Thomas                 guage models. Advances in neural information processing systems 35 (2022),
      Lu, Niels Voss, Bjoern Hartmann, JD Zamfirescu-Pereira, Sarah Chasins, and              3843–3857.
      Gireeja Ranade. [n. d.]. Bridging the gap to autoformalize free-form human         [48] Toby Jia-Jun Li, Jingya Chen, Haijun Xia, Tom M. Mitchell, and Brad A. Myers.
      reasoning. Plateau Workshop.                                                            2020. Multi-Modal Repairs of Conversational Breakdowns in Task-Oriented
 [27] Gila Hanna, David A Reid, and Michael De Villiers. 2019. Proof technology in            Dialogs. In Proceedings of the 33rd Annual ACM Symposium on User Interface
      mathematics research and teaching. Springer.                                            Software and Technology. 1094–1107. doi:10.1145/3379337.3415820
 [28] Mohammad Hekmatnejad, Andrew M. Simms, and Georgios Fainekos. 2019.                [49] Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser,
      Model Checking Clinical Decision Support Systems Using SMT. arXiv preprint              Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago,
      arXiv:1901.04545 (v2, revised 4 March 2019). arXiv:1901.04545 [cs.SE] doi:10.           et al. 2022. Competition-level code generation with alphacode. Science 378,
      48550/arXiv.1901.04545                                                                  6624 (2022), 1092–1097.
 [29] Maxim Hendriks, Cezary Kaliszyk, Femke Van Raamsdonk, and Freek Wiedijk.           [50] Zenan Li, Yifan Wu, Zhaoyu Li, Xinming Wei, Fan Yang, Xian Zhang, and Xiaox-
      2010. Teaching logic using a state-of-the-art proof assistant. Acta Didactica           ing Ma. 2024. Autoformalize mathematical statements by symbolic equivalence
      Napocensia 3, 2 (2010), 35–48.                                                          and semantic consistency. Advances in Neural Information Processing Systems
 [30] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart,                37 (2024), 53598–53625.
      Eric Tang, Dawn Song, and Jacob Steinhardt. 2021. Measuring mathematical           [51] Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai
      problem solving with the math dataset. arXiv preprint arXiv:2103.03874 (2021).          Jiang, Yihan Geng, Jiawei Ge, Jingruo Sun, et al. 2025. Goedel-prover-v2: Scaling
 [31] Martin Henz and Aquinas Hobor. 2011. Teaching experience: Logic and formal              formal theorem proving with scaffolded data synthesis and self-correction. arXiv
      methods with Coq. In International Conference on Certified Programs and Proofs.         preprint arXiv:2508.03613 (2025).
      Springer, 199–215.                                                                 [52] Chengwu Liu, Ye Yuan, Yichun Yin, Yan Xu, Xin Xu, Zaoyu Chen, Yasheng Wang,
 [32] Yinya Huang, Xiaohan Lin, Zhengying Liu, Qingxing Cao, Huajian Xin, Haiming             Lifeng Shang, Qun Liu, and Ming Zhang. 2025. Safe: Enhancing Mathematical
      Wang, Zhenguo Li, Linqi Song, and Xiaodan Liang. 2024. Mustard: Mastering               Reasoning in Large Language Models via Retrospective Step-aware Formal
      uniform synthesis of theorem and proof data. arXiv preprint arXiv:2402.08957            Verification. arXiv:2506.04592 [cs.CL] https://arxiv.org/abs/2506.04592
      (2024).                                                                            [53] Michael Xieyang Liu, Advait Sarkar, Carina Negreanu, Benjamin Zorn, Jack
 [33] Frederik Krogsdal Jacobsen and Jørgen Villadsen. 2023. On exams with the                Williams, Neil Toronto, and Andrew D. Gordon. 2023. “What It Wants Me To
      Isabelle proof assistant. arXiv preprint arXiv:2303.05866 (2023).                       Say”: Bridging the Abstraction Gap Between End-User Programmers and Code-
 [34] Maurice Jakesch, Advait Bhat, Daniel Buschek, Lior Zalmanson, and Mor Naa-              Generating Large Language Models. In Proceedings of the 2023 CHI Conference
      man. 2023. Co-writing with opinionated language models affects users’ views.            on Human Factors in Computing Systems. 1–31. doi:10.1145/3544548.3580817
      In Proceedings of the 2023 CHI conference on human factors in computing systems.   [54] Naiming Liu, Shashank Sonkar, Zichao Wang, Simon Woodhead, and Richard G
      1–15.                                                                                   Baraniuk. 2023. Novice learner and expert tutor: Evaluating math reason-
 [35] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii,          ing abilities of large language models with misconceptions. arXiv preprint
      Ye Jin Bang, Andrea Madotto, and Pascale Fung. 2023. Survey of hallucination            arXiv:2310.02439 (2023).
      in natural language generation. ACM computing surveys 55, 12 (2023), 1–38.         [55] Qi Liu, Xinhao Zheng, Xudong Lu, Qinxiang Cao, and Junchi Yan. 2025. Re-
 [36] Albert Q Jiang, Wenda Li, and Mateja Jamnik. 2023. Multilingual mathematical            thinking and Improving Autoformalization: Towards a Faithful Metric and a De-
      autoformalization. arXiv preprint arXiv:2311.03755 (2023).                              pendency Retrieval-based Approach. In The Thirteenth International Conference
 [37] Albert Q Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja             on Learning Representations. https://openreview.net/forum?id=hUb2At2DsQ
      Jamnik, Timothée Lacroix, Yuhuai Wu, and Guillaume Lample. 2022. Draft,            [56] Xiaoyang Liu, Kangjie Bao, Jiashuo Zhang, Yunqi Liu, Yu Chen, Yuntian Liu,
      sketch, and prove: Guiding formal theorem provers with informal proofs. arXiv           Yang Jiao, and Tao Luo. 2025. Atlas: Autoformalizing theorems through lifting,
      preprint arXiv:2210.12283 (2022).                                                       augmentation, and synthesis of data. arXiv preprint arXiv:2502.05567 (2025).
 [38] Ellen Jiang, Edwin Toh, Alejandra Molina, Kristen Olson, Claire Kayacik, Aaron     [57] Jianqiao Lu, Yingjia Wan, Yinya Huang, Jing Xiong, Zhengying Liu, and Zhi-
      Donsbach, Carrie J. Cai, and Michael Terry. 2022. Discovering the Syntax and            jiang Guo. 2025. FormalAlign: Automated Alignment Evaluation for Auto-
      Strategies of Natural Language Programming with Generative Language Models.             formalization. In International Conference on Learning Representations (ICLR).
      In Proceedings of the 2022 CHI Conference on Human Factors in Computing                 arXiv:2410.10135
      Systems. 1–19. doi:10.1145/3491102.3501870                                         [58] Jianqiao Lu, Yingjia Wan, Zhengying Liu, Yinya Huang, Jing Xiong, Chengwu
 [39] William Jurayj, Nils Holzenberger, and Benjamin Van Durme. 2026.                        Liu, Jianhao Shen, Hui Jin, Jipeng Zhang, Haiming Wang, et al. 2024. Process-
      Language Models and Logic Programs for Trustworthy Tax Reasoning.                       driven autoformalization in lean 4. arXiv preprint arXiv:2406.01940 (2024).
      arXiv:2508.21051 [cs.CL] https://arxiv.org/abs/2508.21051                          [59] Evelyn Lulis, Martha Evens, and Joel Michael. 2004. How Human Tutors Employ
 [40] Enkelejda Kasneci, Kathrin Seßler, Stefan Küchemann, Maria Bannert, Daryna              Analogy to Facilitate Understanding. In Proceedings of the Twenty-Sixth Annual
      Dementieva, Frank Fischer, Urs Gasser, Georg Groh, Stephan Günnemann, Eyke              Conference of the Cognitive Science Society, Kenneth Forbus, Dedre Gentner, and
      Hüllermeier, et al. 2023. ChatGPT for good? On opportunities and challenges             Terry Regier (Eds.). Lawrence Erlbaum Associates, 861–866.
      of large language models for education. Learning and individual differences 103
                                                                                                                                                                       Guo et al.


[60] Patrick Massot. 2024. Teaching mathematics using lean and controlled natural          [83] Michael Shulman. 2024. Strange new universes: Proof assistants and synthetic
     language. In 15th International Conference on Interactive Theorem Proving (ITP             foundations. Bull. Amer. Math. Soc. 61, 2 (2024), 257–270.
     2024). Schloss Dagstuhl–Leibniz-Zentrum für Informatik, 27–1.                         [84] Wilfried Sieg. 1990. Proof theory. Carnegie Mellon University.
[61] Hayden Moore and Asfahan Shah. 2025. Evaluating Autoformalization Robust-             [85] Vikash Singh, Debargha Ganguly, Haotian Yu, Chengwei Zhou, Prerna Singh,
     ness via Semantically Similar Paraphrasing. arXiv preprint arXiv:2511.12784                Brandon Lee, Vipin Chaudhary, and Gourav Datta. 2026. Toward Guarantees
     (2025).                                                                                    for Clinical Reasoning in Vision Language Models via Formal Verification.
[62] Hussein Mozannar, Gagan Bansal, Adam Fourney, and Eric Horvitz. 2024. Read-                arXiv:2602.24111 [cs.CV] doi:10.48550/arXiv.2602.24111
     ing Between the Lines: Modeling User Behavior and Costs in AI-Assisted Pro-           [86] Karan Singhal, Shekoofeh Azizi, Tao Tu, S Sara Mahdavi, Jason Wei, Hyung Won
     gramming. In Proceedings of the 2024 CHI Conference on Human Factors in                    Chung, Nathan Scales, Ajay Tanwani, Heather Cole-Lewis, Stephen Pfohl, et al.
     Computing Systems. ACM, 1–16. doi:10.1145/3613904.3641936                                  2023. Large language models encode clinical knowledge. Nature 620, 7972
[63] Logan Murphy, Kaiyu Yang, Jialiang Sun, Zhaoyu Li, Anima Anandkumar,                       (2023), 172–180.
     and Xujie Si. 2024. Autoformalizing euclidean geometry. arXiv preprint                [87] Peiyang Song, Kaiyu Yang, and Anima Anandkumar. 2024. Lean copilot: Large
     arXiv:2405.17216 (2024).                                                                   language models as copilots for theorem proving in lean. arXiv preprint
[64] Brad Myers, Scott E Hudson, and Randy Pausch. 2000. Past, present, and                     arXiv:2404.12534 (2024).
     future of user interface software tools. ACM Transactions on Computer-Human           [88] Sofia Eleni Spatharioti, David Rothschild, Daniel G Goldstein, and Jake M
     Interaction (TOCHI) 7, 1 (2000), 3–28.                                                     Hofman. 2025. Effects of LLM-based search on decision making: Speed, accuracy,
[65] Wojciech Nawrocki, Edward W Ayers, and Gabriel Ebner. 2023. An extensible                  and overreliance. In Proceedings of the 2025 CHI Conference on Human Factors
     user interface for Lean 4. In 14th International Conference on Interactive Theorem         in Computing Systems. 1–15.
     Proving (ITP 2023). Schloss Dagstuhl-Leibniz-Zentrum für Informatik.                  [89] Hari Subramonyam, Roy Pea, Christopher Pondoc, Maneesh Agrawala, and
[66] Tim Nelson, Ben Greenman, Siddhartha Prasad, Tristan Dyer, Ethan Bove,                     Colleen Seifert. 2024. Bridging the gulf of envisioning: Cognitive challenges in
     Qianfan Chen, Charles Cutting, Thomas Del Vecchio, Sidney LeVine, Julianne                 prompt based interactions with LLMs. In Proceedings of the 2024 CHI Conference
     Rudner, et al. 2024. Forge: A tool and language for teaching formal methods.               on Human Factors in Computing Systems. 1–19.
     Proceedings of the ACM on Programming Languages 8, OOPSLA1 (2024), 613–               [90] Guillem Tarrach, Albert Q Jiang, Daniel Raggi, Wenda Li, and Mateja Jamnik.
     641.                                                                                       2024. More details, please: Improving autoformalization with more detailed
[67] Sydney Nguyen, Hannah McLean Babe, Yangtian Zi, Arjun Guha, Carolyn Jane                   proofs. In AI for Math Workshop@ ICML 2024.
     Anderson, and Molly Q. Feldman. 2024. How Beginning Programmers and                   [91] Alfred Tarski. 1983. On the Concept of Logical Consequence. In Logic, Semantics,
     Code LLMs (Mis)read Each Other. In Proceedings of the 2024 CHI Conference on               Metamathematics: Papers from 1923 to 1938. Oxford University Press. Original
     Human Factors in Computing Systems. 1–26. doi:10.1145/3613904.3642706                      work published 1936.
[68] Harsha Nori, Nicholas King, Scott Mayer McKinney, Dean Carignan, and Eric             [92] Athina Thoma and Paola Iannone. 2022. Learning about Proof with the Theorem
     Horvitz. 2023. Capabilities of gpt-4 on medical challenge problems. arXiv                  Prover LEAN: The Abundant Numbers Task. International Journal of Research
     preprint arXiv:2303.13375 (2023).                                                          in Undergraduate Mathematics Education 8 (2022), 64–93. doi:10.1007/s40753-
[69] Don Norman. 2013. The design of everyday things: Revised and expanded edition.             021-00140-1
     Basic books.                                                                          [93] Athina Thoma and Paola Iannone. 2022. Learning about proof with the theorem
[70] Gabrielle O’Brien. 2025. How scientists use large language models to program.              prover lean: the abundant numbers task. International Journal of Research in
     In Proceedings of the 2025 CHI Conference on Human Factors in Computing                    Undergraduate Mathematics Education 8, 1 (2022), 64–93.
     Systems. 1–16.                                                                        [94] Kurt VanLehn. 2006. The behavior of tutoring systems. International journal of
[71] OpenAI. 2026. On the Navier–Stokes Millennium Prize Problem. https://openai.               artificial intelligence in education 16, 3 (2006), 227–265.
     com/index/navier-stokes-solution/. Accessed September 11, 2026.                       [95] VIDA-NYU. 2026. Lea: An Agent Backbone for Mathematician-Led Formaliza-
[72] Azim Ospanov, Zijin Feng, Jiacheng Sun, Haoli Bai, Xin Shen, and Farzan Farnia.            tion. https://vida-nyu.github.io/Lea/. Accessed: 2026-08-29.
     2025. HERMES: Towards Efficient and Verifiable Mathematical Reasoning in              [96] Karen D Wang, Eric Burkholder, Carl Wieman, Shima Salehi, and Nick Haber.
     LLMs. arXiv preprint arXiv:2511.18760 (2025). https://arxiv.org/abs/2511.18760             2024. Examining the potential and pitfalls of ChatGPT in science and engi-
[73] Manooshree Patel, Rayna Bhattacharyya, Thomas Lu, Arnav Mehta, Niels Voss,                 neering problem-solving. In Frontiers in Education, Vol. 8. Frontiers Media SA,
     Narges Norouzi, and Gireeja Ranade. 2026. LeanTutor: Towards a Verified AI                 1330486.
     Mathematical Proof Tutor. In Proceedings of the Fortieth AAAI Conference on           [97] Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe Diao, Renjie Pi, and
     Artificial Intelligence (AAAI ’26). AAAI Press, 40670–40678. https://ojs.aaai.org/         Tong Zhang. 2024. Theoremllama: Transforming general-purpose llms into
     index.php/AAAI/article/view/41514                                                          lean4 experts. arXiv preprint arXiv:2407.03203 (2024).
[74] Lawrence C. Paulson. 1994. Isabelle: A Generic Theorem Prover. In Proceedings         [98] Yousef Wardat. 2023. ChatGPT: A revolutionary tool for teaching and learning
     of the 12th International Conference on Automated Deduction (CADE-12) (Lecture             mathematics. Available at SSRN 5653030 (2023).
     Notes in Computer Science, Vol. 814), Alan Bundy (Ed.). Springer, 37–41.              [99] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi,
[75] Lawrence C Paulson. 2023. Large-scale formal proof for the working mathemati-              Quoc V Le, Denny Zhou, et al. 2022. Chain-of-thought prompting elicits rea-
     cian—lessons learnt from the ALEXANDRIA Project. In International Conference               soning in large language models. Advances in neural information processing
     on Intelligent Computer Mathematics. Springer, 3–15.                                       systems 35 (2022), 24824–24837.
[76] Auguste Poiroux, Gail Weiss, Viktor Kunčak, and Antoine Bosselut. 2025. Reli-        [100] Sean Welleck and Rahul Saha. 2023. LLMSTEP: LLM proofstep suggestions in
     able evaluation and benchmarks for statement autoformalization. In Proceedings             Lean. arXiv preprint arXiv:2310.18457 (2023).
     of the 2025 Conference on Empirical Methods in Natural Language Processing.          [101] Jelle Wemmenhove, Thijs Beurskens, Sean McCarren, Jan Moraal, David Tuin,
     17958–17980.                                                                               and Jim Portegies. 2022. Waterproof: Educational Software for Learning How
[77] PramaanaLabs 2026. Pramaana Labs. https://www.pramaanalabs.ai/. Accessed:                  to Write Mathematical Proofs. arXiv preprint arXiv:2211.13513 (2022).
     2026-05-08.                                                                          [102] Ke Weng, Lun Du, Sirui Li, Wangyue Lu, Haozhe Sun, Hengyu Liu, and
[78] Leon Reicherts, Zelun Tony Zhang, Elisabeth Von Oswald, Yuanting Liu, Yvonne               Tiancheng Zhang. 2025. Autoformalization in the era of large language models:
     Rogers, and Mariam Hassib. 2025. AI, help me think—but for myself: Assisting               A survey. arXiv preprint arXiv:2505.23486 (2025).
     people in complex decision-making by providing different kinds of cognitive          [103] Hasini Witharana, Yangdi Lyu, Subodha Charles, and Prabhat Mishra. 2022.
     support. In Proceedings of the 2025 CHI Conference on Human Factors in Com-                A survey on assertion-based hardware verification. ACM Computing Surveys
     puting Systems. 1–19.                                                                      (CSUR) 54, 11s (2022), 1–33.
[79] Mitchel Resnick, Brad Myers, Kumiyo Nakakoji, Ben Shneiderman, Randy                 [104] Magdalena Wolska and Ivana Kruijff-Korbayová. 2004. Analysis of mixed
     Pausch, Ted Selker, and Mike Eisenberg. 2005. Design principles for tools to               natural and symbolic input in mathematical dialogs. In Proceedings of the 42nd
     support creative thinking. (2005).                                                         Annual Meeting of the Association for Computational Linguistics (ACL-04). 25–32.
[80] Jessica Shi, Cassia Torczon, Harrison Goldstein, Andrew Head, and Benjamin C         [105] Yutong Wu, Di Huang, Ruosi Wan, Yue Peng, Shijie Shang, Chenrui Cao, Lei Qi,
     Pierce. 2025. Designing Proof Deautomation for Rocq. In Proceedings of the                 Rui Zhang, Xishan Zhang, Zidong Du, et al. 2026. StepFun-Formalizer: Unlock-
     15th PLATEAU Workshop on Programming Languages and Human-Computer                          ing the Autoformalization Potential of LLMs Through Knowledge-Reasoning
     Interaction (PLATEAU’25). ACM.                                                             Fusion. In Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 40.
[81] Jessica Shi, Cassia Torczon, Harrison Goldstein, Benjamin C. Pierce, and Andrew            33980–33988.
     Head. 2025. QED in Context: An Observation Study of Proof Assistant Users.           [106] Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus Rabe, Charles Staats,
     Proceedings of the ACM on Programming Languages 9, OOPSLA1, Article 92                     Mateja Jamnik, and Christian Szegedy. 2022. Autoformalization with large
     (April 2025), 27 pages. doi:10.1145/3720426                                                language models. Advances in Neural Information Processing Systems 35 (2022),
[82] Jessica Shi, Cassia Torczon, Harrison Goldstein, Benjamin C Pierce, and Andrew             32353–32368.
     Head. 2025. QED in context: An observation study of proof assistant users.           [107] Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong
     Proceedings of the ACM on Programming Languages 9, OOPSLA1 (2025), 337–                    Ruan, Wenda Li, and Xiaodan Liang. 2024. DeepSeek-Prover: Advancing The-
     363.                                                                                       orem Proving in LLMs through Large-Scale Synthetic Data. arXiv preprint
LeanSide: A Formally Verified Co-Reasoning System for Natural-language Proofs


      arXiv:2405.14333 (2024).
[108] Fangzhi Xu, Qika Lin, Jiawei Han, Tianzhe Zhao, Jun Liu, and Erik Cambria.
      2025. Are large language models really good logical reasoners? a comprehensive
      evaluation and beyond. IEEE Transactions on Knowledge and Data Engineering
      37, 4 (2025), 1620–1634.
[109] Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li, Kristin Lauter, Swarat
      Chaudhuri, and Dawn Song. 2024. Formal Mathematical Reasoning: A New
      Frontier in AI. arXiv preprint arXiv:2412.16075 (2024). https://arxiv.org/abs/
      2412.16075
[110] Kaiyu Yang, Aidan M Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shix-
      ing Yu, Saad Godil, Ryan Prenger, and Anima Anandkumar. 2023. LeanDojo:
      Theorem Proving with Retrieval-Augmented Language Models. In Advances in
      Neural Information Processing Systems, Vol. 36.
[111] Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang, Dahua Lin, and Kai Chen.
      2024. Lean workbook: A large-scale lean problem set formalized from natural
      language math problems. Advances in Neural Information Processing Systems 37
      (2024), 105848–105863.
[112] J. Diego Zamfirescu-Pereira, Richmond Y. Wong, Bjoern Hartmann, and Qian
      Yang. 2023. Why Johnny Can’t Prompt: How Non-AI Experts Try (and Fail)
      to Design LLM Prompts. In Proceedings of the 2023 CHI Conference on Human
      Factors in Computing Systems. Article 437, 21 pages. doi:10.1145/3544548.3581388
[113] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. 2021. Minif2f: a cross-
      system benchmark for formal olympiad-level mathematics. arXiv preprint
      arXiv:2109.00110 (2021).
[114] Yangtian Zi, Luisa Li, Arjun Guha, Carolyn Jane Anderson, and Molly Q. Feld-
      man. 2025. “I Would Have Written My Code Differently”: Beginners Struggle
      to Understand LLM-Generated Code. In Proceedings of the 33rd ACM Inter-
      national Conference on the Foundations of Software Engineering. 1479–1488.
      doi:10.1145/3696630.3731663
                                                                                                                                                Guo et al.


A     Problem Statements
The following ten problems from EECS 127 were used in our evaluation. Each problem was attempted by 𝑛 = 10 students.
   (1) Q1
        Show that the following inequality hold for any vector 𝑥® ∈ R𝑛 : √1𝑛 ∥𝑥® ∥ 2 ≤ ∥𝑥® ∥ ∞
   (2) Q2
        Show that the following inequality hold for any vector 𝑥® ∈ R𝑛 : ∥𝑥® ∥ ∞ ≤ ∥𝑥® ∥ 2
   (3) Q3
        Show that the following inequality hold for any vector 𝑥® ∈ R𝑛 : ∥𝑥® ∥ 2 ≤ ∥𝑥® ∥ 1
   (4) Q4
                                                                                            √
        Show that the following inequality hold for any vector 𝑥® ∈ R𝑛 : ∥𝑥® ∥ 1 ≤ 𝑛∥𝑥® ∥ 2
   (5) Q5
        Let 𝐴 ∈ 𝑆 𝑛 (i.e., the set of 𝑛 × 𝑛 symmetric matrices) and (𝜆1, 𝑣®1 ), (𝜆2, 𝑣®2 ) 𝜆1 ≠ 𝜆2 be distinct eigenpairs of 𝐴 where 𝑣®1 ≠ 0 and 𝑣®2 ≠ 0.
        Show that 𝑣®1 ⊤ 𝑣®2 = 0 i.e., eigenspaces corresponding to distinct eigenvalues are mutually orthogonal. Note: this proof is part of the
        spectral theorem, so please do not use the spectral theorem in the proof.
   (6) Q6
        Let 𝑃 be an 𝑚 × 𝑛 matrix. Show that the Frobenius norm satisfies the following property of a norm: i. ∥𝑃 ∥ 𝐹 = 0 if and only if 𝑃 = 0
   (7) Q7
        Let 𝑃 be an 𝑚 × 𝑛 matrix. Show that the Frobenius norm satisfies the following property of a norm: ii. For all 𝑎 ∈ R, we have
         ∥𝑎𝑃 ∥ 𝐹 = |𝑎| ∥𝑃 ∥ 𝐹
   (8) Q8
        Let 𝑃 and 𝑄 be 𝑚 × 𝑛 matrices. Show that the Frobenius norm satisfies the following property of a norm: iii. ∥𝑃 + 𝑄 ∥ 𝐹 ≤ ∥𝑃 ∥ 𝐹 + ∥𝑄 ∥ 𝐹
   (9) Q9
        Let 𝑃 be an 𝑚 × 𝑛 matrix. Write ∥𝑃 ∥ 2𝐹 in terms of singular values 𝜎1, . . . , 𝜎𝑛 .
        HINT: The cyclic property of traces might be helpful: tr(𝑃𝑄𝑅) = tr(𝑅𝑃𝑄) = tr(𝑄𝑅𝑃).
  (10) Q10
        In this problem, we will analyze properties of positive semidefinite (PSD) matrices. A symmetric matrix 𝑀 ∈ R𝑛×𝑛 is a PSD matrix if
        𝑥®⊤ 𝑀 𝑥® ≥ 0 for all 𝑥® ∈ R𝑛 , and we denote that as 𝑀 ⪰ 0 or 𝑀 ∈ S𝑛+ . Assume 𝐴 ∈ R𝑛×𝑛 is a symmetric matrix. Show that if 𝐴 ⪰ 0
        then all diagonal entries of 𝐴 are non-negative, 𝐴𝑖𝑖 ≥ 0.
  (11) Q11
        Show that for any matrix 𝑄 ∈ R𝑚×𝑛 , if 𝐴 = 𝑄 ⊤𝑄 then 𝐴 ∈ S𝑛+ . Note: If we take 𝑄 = 𝑃 ∈ S𝑛+ , we have 𝐴 = 𝑃 2 ∈ S𝑛+ ; this proves the
        other direction of the above “if-and-only-if.”
  (12) Q12
        Let 𝐴 ∈ R𝑛×𝑛 be a symmetric matrix with eigenvalue-eigenvector pairs given by (𝜆0, 𝑣®0 ), . . . , (𝜆𝑛−1, 𝑣®𝑛−1 ), where 𝜆0 > · · · > 𝜆𝑛−1 .
        Consider the problem
                                                  𝑝 ∗ = max 𝑥®⊤𝐴®
                                                                𝑥 s.t. ∥𝑥® ∥ 22 = 1, 𝑥®⊤ 𝑣®0 = 0.
                                                       𝑥® ∈R𝑛
         Show that 𝑝 ∗ = 𝜆1
         HINT: First find an 𝑥® which is feasible and 𝑥®⊤𝐴𝑥® = 𝜆1 . Then show that 𝑝 ∗ ≤ 𝜆1 .
    (13) Q13
         Let 𝐴 ∈ R𝑛×𝑛 be a symmetric matrix with eigenvalue-eigenvector pairs given by (𝜆0, 𝑣®0 ), . . . , (𝜆𝑛−1, 𝑣®𝑛−1 ), where 𝜆0 > · · · > 𝜆𝑛−1 .
         Consider the problem
                                                𝑝 ∗ = max 𝑥®⊤𝐴®𝑥 s.t. ∥𝑥® ∥ 22 = 1, 𝑥®⊤ 𝑣®0 = 0.
                                                       𝑥® ∈R𝑛
         Firstly, show that 𝑝 ∗ ≥ 𝜆1 HINT: First find an 𝑥® which is feasible and 𝑥®⊤𝐴®
                                                                                      𝑥 = 𝜆1 .
    (14) Q14
         Let 𝐴 ∈ R𝑛×𝑛 be a symmetric matrix with eigenvalue-eigenvector pairs given by (𝜆0, 𝑣®0 ), . . . , (𝜆𝑛−1, 𝑣®𝑛−1 ), where 𝜆0 > · · · > 𝜆𝑛−1 .
         Consider the problem
                                                𝑝 ∗ = max 𝑥®⊤𝐴®𝑥 s.t. ∥𝑥® ∥ 22 = 1, 𝑥®⊤ 𝑣®0 = 0.
                                                       𝑥® ∈R𝑛
        Then, show that 𝑝 ∗ ≤ 𝜆1
   Noted that Q13 and Q14 are two sub parts of Q12, as in the classroom deployment we found the Q12 takes too long time to complete in
the study, therefore we cut them into 2. As we are not measuring the whole problem completeness, thus we did not discard the study data
for Q12.
LeanSide: A Formally Verified Co-Reasoning System for Natural-language Proofs


B    More interface screenshots


                                                                                                                                                                                                                                                             LeanSide Compiler
                                                                                                                                                                                                                6. Check the compiler panel for details.
                                                                                                                                        LeanSide Compiler
             LeanSide could not verify step 3, 4. Check the compiler panel for details.                                                                                  LeanSide could not verify step 4, 5,




                            (1) P20: A step-level error message helped P12 revise the proof strategy.                                                                  (2) P2: A step-level error message helped P2 correct a subtle error overlooked by

                                                                                                                                                                                                                                        expert evaluators.




                                                                                                                   LeanSide Compiler
          LeanSide could not verify step 2, 3, 4, 5. Check the compiler panel for details.


                                                                                                                                                                                                                                                                      LeanSide Compiler




                                                                                                                                                                                         (6) P18: Continuation hint helped the student make progress.




          (3) P12: P12 spent substantial time interpreting step-level error messages before

                                                                                                 revising.




                                                                                                                                       LeanSide Compiler

           LeanSide could not verify step   1, 2. Check the compiler panel for details.
                                                                                                                                                                                                                                                             LeanSide Compiler




                                            (4) P4: Large-jump warning helped the student make progress.




                                                                                                                                                                               (5) P2: Continuation error message helped the student make progress.




                                                                                                                  LeanSide Compiler                                                                                                                                                  LeanSide Compiler




         (7) P16: Comparison between an unhelpful continuation error message and a useful

                                                                                             continuation hint.

                                                                                                                                                                                                                         (8) P14: Suggestion message.




                                                                                                                                                            Figure 14: examples
                                                                                                                                   Guo et al.


C     Participants’ demographic information

                                     Table 2: Participant background and familiarity with Lean

Participant   Major                                                   Year    Lean familiarity
P2            CS+math                                                  1      Experienced with Lean introduction game
P3            Aerospace Engineering & EECS                             4      No
P4            Chemistry                                                3      Tried another formal language
P6            CS                                                       2      Knew Lean before, but never tried to write in Lean
P7            CS+math                                                  2      Experienced with Lean introduction game
P8            CS                                                       2      Knew Lean before, but never tried to write in Lean
P9            CS+math                                                  2      No
P11           CS                                                       2      No
P12           CS                                                       1      Knew Lean before, but never tried to write in Lean
P13           CS + data science                                        4      No
P14           EECS                                                   Master   No
P15           CS+datascience                                           1      No
P16           Data science                                             2      No
P18           CS & statistic                                           2      No
P19           Transportation Engineering                              PhD     No
P20           Data science                                             2      No
P21           Data science                                             2      No
P22           CS+math                                                  1      Knew Lean before, but never tried to write in Lean
P23           CS+math                                                  4      Knew Lean before, but never tried to write in Lean
P24           CS+math                                                  4      No
P25           Bio engineering                                          3      No
P26           CS + business                                            2      Knew Lean before, but never tried to write in Lean
P27           Business                                                 2      No


    Exam grade distribution:




                                      Figure 15: This figure shows student’s grade distribution.
