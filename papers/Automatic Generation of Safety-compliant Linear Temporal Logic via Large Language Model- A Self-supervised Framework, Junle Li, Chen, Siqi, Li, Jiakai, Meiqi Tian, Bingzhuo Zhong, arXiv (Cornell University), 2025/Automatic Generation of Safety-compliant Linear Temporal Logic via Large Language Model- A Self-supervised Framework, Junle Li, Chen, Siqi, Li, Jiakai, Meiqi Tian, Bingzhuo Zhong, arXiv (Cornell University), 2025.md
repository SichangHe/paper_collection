                                            Automatic Generation of Safety-compliant Linear
                                             Temporal Logic via Large Language Model: A
                                                      Self-supervised Framework
                                                                        Junle Li1 , Siqi Chen1 , Jiakai Li1 , Meiqi Tian1 , Bingzhuo Zhong1*
                                                                    1
                                                               Hong Kong University of Science and Technology (Guangzhou), Guangzhou, China
                                                   Email: {juliejunleli, bingzhuoz}@hkust-gz.edu.cn, {schen972, jli196, mtian837}@connect.hkust-gz.edu.cn



                                            Abstract—Converting high-level natural-language task de-
arXiv:2503.15840v4 [cs.LO] 27 Apr 2026




                                         scriptions into formal specifications such as Linear Temporal
                                         Logic (LTL) is essential for ensuring safety in cyber-physical
                                         systems (CPS). Existing work, however, only optimizes trans-
                                         lation quality without explicitly verifying the output against
                                         safety constraints. We present AutoSafeLTL, a self-supervised,
                                         cloud–edge–collaborative framework that automates the gener-
                                         ation of safety-compliant LTL specifications while preserving
                                         logical consistency and semantic fidelity. A lightweight edge-side
                                         three-stage-fine-tuned LLM offers real-time conversion from
                                         natural language to LTL specifications (NL2LTL) and guarantees
                                         safety-critical latency and data locality. Two larger-capacity
                                         cloud-side agents then iteratively refine the alignment: 1)
                                         LLM-as-an-Aligner matches atomic propositions to safety con-
                                         straints, and 2) LLM-as-a-Critic interprets counterexamples from                Fig. 1. Overview of AutoSafeLTL Framework.
                                         Inclusion Check to guide corrective regeneration. This col-          Models (LLMs), while maintaining formal safety-compliance
                                         laborative architecture provides a safety-guaranteed alignment
                                         mechanism between high-level user intent and formally verifiable     guarantees to prevent critical risks to CPS.
                                         system behavior, demonstrating the potential of our framework to        Related Works: Linear Temporal Logic (LTL) is fun-
                                         advance AI Alignment in safety-critical domains. Our approach        damental for formal verification in autonomous systems.
                                         achieves 0% violation rates on multiple benchmarks, enabling         Recent NL2LTL approaches improve translation efficiency
                                         trustworthy specification generation and verification for both AI
                                         and critical CPS applications.
                                                                                                              and syntactic validity via decomposition, dynamic prompting,
                                            Index Terms—Linear Temporal Logic, Large Language Mod-            grammar-constrained decoding, and fine-tuning [2]. However,
                                         els.                                                                 these methods focus exclusively on semantic alignment. By
                                                                                                              treating user instructions as the absolute truth, they ignore
                                                                    I. I NTRODUCTION                          external safety constraints, risking the faithful translation
                                            Motivation: Ensuring the safety of cyber-physical systems         of unsafe intents into dangerous specifications. Meanwhile,
                                         (CPS) is central to modern system design, especially in safety-      frameworks integrating LLMs with formal verifiers typically
                                         critical domains. Formal specifications like Linear Temporal         position the verifier as a post-hoc filter for LLM-generated
                                         Logic (LTL) [1] provide mathematical rigor for verification          plans. This remedial paradigm leads to inefficient “trial-and-
                                         and controller synthesis, ensuring CPS safety. The challenge         error” cycles and only verifies one-off execution traces rather
                                         lies in translating high-level, often unstructured requirements      than the underlying task logic, lacking a persistent safety
                                         into formal specifications. However, a critical issue frequently     foundation against environmental variations.
                                         neglected by these methods is whether the generated LTL                 In this work, we present AutoSafeLTL (as shown in Fig.
                                         formula inherently conflict with the safety constraints imposed      1), a self-supervised framework that integrates automata-based
                                         on the system. We refer to this aspect as the compliance             verification with a cloud–edge collaborative LLM architecture
                                         of LTL specifications with respect to safety constraints, and        to generate safety-compliant LTL specifications in a fully-
                                         to those LTL specifications with no such conflict as safety-         automated manner. An edge-deployed User LLM, fine-tuned
                                         compliant LTL. Specifically, being safety-compliant means            in three progressive stages (translation, syntactic, and semantic
                                         that the temporal behavior expressed by the LTL formula              correction), handles both real-time LTL generation and local
                                         entirely aligns with the intended temporal behavior mandated         repair with minimal latency. For rigorous verification, cloud-
                                         by safety constraints. Accordingly, we focus on how to gen-          side agents—LLM-as-an-Aligner and LLM-as-a-Critic—are
                                         erate safety-compliant LTL specifications via Large Language         invoked to interpret complex violations detected via Inclusion
                                                                                                              Checks. This collaborative synergy ensures data locality while
                                           *Corresponding author.                                             leveraging cloud-scale inference to achieve formal alignment
between user intent and safety properties. Our contributions        where a ∈ AP is an atomic proposition, temporal operators
are summarized as follows:                                          such as X (next), U (until) can be used for dynamical
   • We propose a fully automated, end-to-end framework for         properties.
     NL-driven LTL specification generation that targets early-     Semantics. Let φ be a LTL formula, the semantics of φ is
     stage safety-compliant specification generation. By shift-     defined  over infinite words σ ∈ (2AP )ω , with W ords(φ) =
                                                                                 ω
     ing the focus to the generation of the specification itself,    σ ∈ 2AP | σ |= φ being the LT property induced by
     our framework ensures the governing logic is formally          φ. Let σ = A0 A1 A2 . . . (symbol Ai ∈ AP ), where the
     verified before system execution. We enhance formal            satisfaction relation |=⊆ (2AP )ω × LTL is defined as follows:
     verification tools with an efficient counterexample path          • σ |= true,
     extraction algorithm, enabling automated LTL refinement           • σ |= a iff a ∈ A0 ,
     and a 0% violation rate against safety constraints.               • σ |= ¬φ iff σ ̸|= φ,
   • We develop a novel three-stage fine-tuning strategy that          • σ |= φ1 ∧ φ2 iff σ |= φ1 and σ |= φ2 ,
     progressively instills intrinsic safety capability into a         • σ |= Xφ iff σ[1...] = A1 A2 . . . |= φ,
     small language model. This strategy enables an 8B                 • σ |= φ1 U φ2 iff ∃j ≥ 0. σ[j...] |= φ2 and for all 0 ≤
     edge model to outperform GPT-4 in generating safety-                 i < j, σ[i...] |= φ1 .
     compliant LTL specifications, proving the viability of
     formal methods on resource-restricted hardware.                B. Büchi automaton
   • We establish a cloud–edge collaborative framework that
                                                                       To bridge the gap between logical formulations and algorith-
     enforces data locality through on-device LTL generation
                                                                    mic reasoning, a typical step is to convert LTL into automata,
     and correction. By delegating abstracted tasks—AP align-
                                                                    like Büchi automaton (BA) [5].
     ment and counterexample interpretation—to cloud-side
     agents, this architecture enables the scalable deployment         Definition 2 (Büchi Automata): A Büchi automaton (BA) is
     of formal methods in safety-critical and privacy-sensitive     defined as a tuple A = (Σ, Q, I, F, δ), where Σ is an finite
     domains.                                                       alphabet, Q is a finite set of states, I ⊆ Q is the set of initial
   • We construct fine-tuning and evaluation datasets to ad-
                                                                    states, F ⊆ Q is the set of accepting states and δ : Q×Σ×2Q
     dress the lack of suitable datasets for evaluating safety-     is the transition relation. A run of A on an infinite word w =
     compliance in NL2LTL tasks. Specifically, our datasets         σ1 σ2 · · · ∈ Σω , with symbol σi ∈ Σ, i ∈ N, starting from a
     comprise over 35k synthetic LTL specifications for pre-        state q0 ∈ Q, is an infinite sequence of states q0 q1 q2 . . . such
     training, 200 carefully curated human–LTL pairs for fine-      that (qj−1 , σj , qj ) ∈ δ for all j > 0. The run is accepted if
     tuning to enhance the model’s correction ability, and 300      qi ∈ F for infinitely many i. The accepted language L(A)
     evaluation cases, featuring navigation-style instructions      consists of all infinite words over Σω for which there exists
     with human-centered APs and rich temporal structures,          an accepted run.
     enabling safety-realistic evaluation.                             For every LTL formula φ, there exists a corresponding
                                                                    Büchi automaton A such that: L(A) = W ords(φ). The con-
                     II. P RELIMINARIES                             version from LTL to Büchi automaton has a well-established
                                                                    theoretical foundation [6], [7], and existing research has pro-
   This section introduces the necessary background for our         posed numerous effective methods and tools for converting
framework. We begin with an overview of Linear Temporal             LTL to Büchi automata [4], [8]–[13]. The aim of this con-
Logic (LTL), then introduce Büchi automata, which serves as        version lies in using Büchi automata to model a system’s
the automata-theoretic counterpart to LTL formulas. Building        dynamic behavior. Simulation relations, such as forward and
upon this foundation, we describe the process of automata-          backward simulation, are then used to establish step-by-step
based language inclusion check to reason the verification.          correspondence by linking successive state transitions, thereby
Finally, we formally state the problem that our work aims           capturing all dynamic behaviors expressed by the BA.
to address.                                                            Definition 3 (Forward and Backward Simulation on Büchi
                                                                    Automata): Let A = (Σ, Q, I, F , δ) be a Büchi automaton.
A. Linear Temporal Logic
                                                                    A relation R ⊆ Q × Q is called (1) a forward simulation on
   Linear Temporal Logic (LTL) serves as the foundation             A if for any (p, r) ∈ R, the following conditions hold: 1)If
for many practical specification languages [1]. The basic           p ∈ F , then r ∈ F and 2) ∀(p, σ, p′ ) ∈ δ, ∃(r, σ, r′ ) ∈ δ
components of an LTL formula include Atomic Propositions            s.t. (p′ , r′ ) ∈ R. (2) a backward simulation on A if for any
(AP) and Operators (boolean and temporal). In our work, we          (p′ , r′ ) ∈ R, the following conditions hold: 1) If p′ ∈ F, then
adopt the syntax and semantics of LTL as defined in [3], [4]        r′ ∈ F , 2) If p′ ∈ I, then r′ ∈ I, and 3) ∀(p, σ, p′ ) ∈ δ,
and recalled them here.                                             ∃(r, σ, r′ ) ∈ δ s.t. (p, r) ∈ R.
   Definition 1 (LTL Syntax and Semantics): Syntax. Let AP             To support the subsequent Section III-C, we introduce the
be a finite set of atomic propositions. The set of LTL formulas     notion of a path in a Büchi automaton, which uses simulation
over AP is defined inductively by the following grammar:            to describe how an input word drives a sequence of state
         φ ::= true | a | ¬φ | φ1 ∧ φ2 | Xφ | φ1 U φ2 ,             transitions. Since the same symbol σi ∈ σ can trigger different
transitions depending on the current state of the automata,                                   III. F RAMEWORK
there exists a set of paths over the same input word σ.               A. Overview
   Definition 4 (Path of a Büchi Automaton): Let A =                        We propose AutoSafeLTL (Fig. 1), comprising two col-
(Σ, Q, I, F, δ) be a Büchi automaton and let Word σ =                    laborative modules: LTL Generation and Automated Verifica-
σ0 σ1 σ2 . . . ∈ Σw with symbol σi ∈ Σ, i ∈ N. A path ρ                   tion. Given Desired Tasks and Environmental Information in
of A over σ is a state-and-word sequence:                                 natural language, a lightweight edge-side User LLM—fine-
                        σ0     σ1      σ2
                    q0 −→  q1 −→   q2 −→  ···                             tuned in three stages —generates and locally revises candidate
where q0 ∈ I is an initial state and for each i ≥ 0, LTL specifications.
(qi , σi , qi+1 ) ∈ δ. A path ρ is simulable w.r.t. σ if: 1) it              The Automated Verification process consists of two stages:
traverses every σi ∈ σ and the corresponding transitions Syntactic Check and Semantic Check. Syntactic Check ensures
(qi , σi , qi+1 ) ∈ δ; 2) it ends in or visits some accepting state grammatical validity. After passing the Syntactic Check, the
qf ∈ F infinitely often. The set of paths over σ in A is denoted Semantic Check ensures that the properties of state paths
by Pσ , where:                                                            expressed by the candidate LTL specification adhere to safety
              σ0       σ1
Pσ = {q0 −→        q1 −→   · · · | qi ∈ Q, σi ∈ σ, (qi , σi , qi+1 ) ∈ δ} constraints. In particular, both the Desired Task in LTL-format
                                                                      (1) and the formalized safety constraints are converted into BA
   A fundamental concept in automata-based verifications is format for the Inclusion Check.
the notion of language inclusion, capturing the containment                  The principles of feedback and regeneration further ensure
relationship between two automata.                                        safety-compliance. Two cloud-side Agent LLMs iteratively
   Definition 5 (Language Inclusion): Let A1 and A2 be two refine the LTL specifications: 1) LLM-as-an-Aligner ensures
Büchi automata over the same input alphabet Σ. If every atomic proposition alignment; and 2) LLM-as-a-Critic guides
infinite word accepted by A1 is also accepted by A2 , then the corrective regeneration using Language Inclusion counterex-
language of A1 is included in the language of A2 , denoted as amples. This cloud-edge synergy balances data locality and
L(A1 ) ⊆ L(A2 ):                                                          rigorous safety verification, highlighting a practical path to-
L(A1 ) ⊆ L(A2 ) ⇐⇒ ∀w ∈ Σω , w ∈ L(A1 ) ⇒ w ∈ L(A2 ). wards AI alignment for safety-critical CPS applications. For
C. Automata-Based Language Inclusion Checking among a better illustration of the framework, we used the following
LTLs                                                                      running example throughout the entire session.
                                                                             Running example Consider a traffic scenario, an NL navi-
   The results in [14] shows that safety restrictions could also
                                                                          gation task along with a related safety constraint. Our goal is
be interpreted as LTL (therefore BA). Therefore, the compli-
                                                                          to automatically generate an LTL specification that represents
ance of LTL specifications can be converted to an Automata-
                                                                          the desired task while adhering to the safety constraint. This
based language inclusion check [15], with rank-based and
                                                                          specification can then support downstream applications such
Ramsey-based methods being the most prominent approaches
                                                                          as path planning.
[16]–[21]. Typically, the Ramsey-based method is rooted in
                                                                             Desired Task: Start from the current lane, go straight for
the concept of supergraph—a data structure representing finite
                                                                          200m. Then, turn right onto Maple St. and proceed for 500m.
word classes with similar behavior between two automata, to
                                                                          Finally, turn left onto Oak St., and you will arrive at the
capture the violation counterexample [21].
                                                                          destination after 300m.
   Definition 6 (Supergraph in Ramsey-Based Inclusion
                                                                             Env. Info: Elm St. (Straight lane, 50 km/h limit); Car
Checking): Let A1 = (Σ, Q1 , I1 , F1 , δ1 ) and A2 =
                                                                          overtaking on right; Target: Oak St. (1 km away).
(Σ, Q2 , I2 , F2 , δ2 ) be two Büchi automata over the same
                                                                             Safety Constraint: G((straight 500m ∨ right turn) →
alphabet Σ. A supergraph G(V, E) is a finite directed graph
                                                                          (right turn     →      straight 500m     →      left turn))  →
constructed to capture the combined behaviors of A1 and
                                                                          G(straight 1km → arrive destination).                          *
A2 . The set of nodes V ⊆ Q1 × Q2 consists of all pairs
                                                                             Remark 1. While the running example and the evaluation
of states (q1 , q2 ) where q1 ∈ Q1 and q2 ∈ Q2 , the set of
                                                                          part in Section V focus on a traffic scenario for illustration,
edges E ⊆ V × Σ × V captures synchronized transitions
                                                                          our framework allows for flexible addition and adaptation of
under the same input symbol a ∈ Σ, s.t.: If (q1 , a, q1′ ) ∈
                                                                          desired tasks and specifications as needed.
δ1 and (q2 , a, q2′ ) ∈ δ2 , then ((q1 , q2 ), a, (q1′ , q2′ )) ∈ E.
                                                                          Remark 2. While Environmental Information is not required
D. Problem Formulation                                                    to generate the initial LTL formula, it is essential for LLMs to
                                                                          regenerate safety-compliant specifications when violations oc-
   Problem 1 (Safety-Compliant LTL Specification Synthesis):
                                                                          cur, especially when the original task description is inherently
Let D be an unstructured natural language description of
                                                                          unsafe.
a desired task, and let Ψ = {ψ1 , ψ2 , . . . , ψn } be a set
of predefined safety restrictions, each expressed as an LTL B. LTL Generation
formula. Design a framework that synthesizesTn            an LTL formula     The LTL Generation module performs the initial NL2LTL
φ based on D, such that: L(Aφ ) ⊆ i=1 L(Aψi ), where Aφ translation from task descriptions and auxiliary environmental
and Aψi are the Büchi automata corresponding to φ and ψi , information on the edge. We deploy a lightweight User LLM
respectively.                                                             that has been sequentially fine-tuned in three stages—NL2LTL
translation (S1), syntactic correction (S2), and semantic cor-      Task are converted into Büchi automata and then subjected
rection (S3)—so that a single on-device model jointly handles       to a Ramsey-based Inclusion Check. The process terminates
generation and subsequent local repair, satisfying the CPS-         once a counterexample is found, which in this case is
driven requirement: data locality for privacy, or regulation-       !straight_200m. This counterexample guides the subse-
sensitive deployments.                                              quent LTL correction.                                         *
   Given an NL input D and context E, User LLM extracts                3) Counterexample-guided Automatic Correction: In Lan-
an initial LTL φ(0) . This output is then passed to the Auto-       guage Inclusion Check, a single counterexample word σ can
mated Verification module. Fine-tuning details are illustrated      be found if there exist any violations, but σ may correspond to
in Section IV.                                                      multiple dynamic behaviors, as the same symbol σi ∈ σ can
C. Automated Verification                                           trigger different transitions depending on the current state of
   Verification ensures that the generated LTL specification sat-   the automata. Consequently, identifying a concrete counterex-
isfies safety constraints. Our Automated Verification scheme,       ample path - a sequence of state transitions combined with
the core of the framework, comprises a Syntactic Check and          the driving symbol - is essential for accurately locating the
a Semantic Check.                                                   source of the violation. This path serves as a precise semantic
   1) Syntactic Check: The syntactic check consists of two          witness for non-inclusion and provides actionable guidance
steps: Atomic Proposition (AP) Matching and Operator Match-         for correcting the LTL specification. To this end, we formally
ing. For AP Matching, APs are extracted from safety con-            define the notion of a counterexample path (cf. Section II-B:
straints to build a library. The cloud-side LLM-as-an-Aligner       Definition 4) and establish its existence Theorem 1. Based on
aligns APs in the Desired Task with entries in this library         that, we integrate path extraction into the Inclusion Checking
and replaces them with the closest matches to ensure AP             process via the Comparison Path Storage Algorithm 1. The
consistency. For Operator Matching, a token-based algorithm         worst case complexity of extracting a counterexample path is
checks operator usage and parenthesis balance. Any detected         O(n1 × n2 × m), where n1 and n2 are the state sizes of the
error (along with its type and position) is fed to User LLM         two Büchi automata and m is the alphabet size. The formal
for immediate on-device correction.                                 proposition 1 and its proof 2 are provided. Together, this
   Now, we revisit the running example to demonstrate the           formal theory establishes a rigorous and actionable foundation
syntactic check.                                                    for counterexample-guided LTL correction, constituting a key
Example (continued) Having the safety constraint                    theoretical contribution of our work.
in LTL-format, we extract the AP library as
[right_turn, straight_500m,left_turn,straight_1km,
                                                                       Theorem 1 (Existence of Counterexample Path): Let A1 =
arrive_destination]. Then, LLM-as-an-Aligner is invoked             (Σ, Q1 , I1 , F1 , δ1 ) and A2 = (Σ, Q2 , I2 , F2 , δ2 ) be two
to compare the LTL-formatted Desired Tasks with the AP              Büchi automata. If there exists an infinite counterexample
Library. Accordingly, go_straight_500m in the original              word σ = σ1 (σ2 )ω ∈ Σω , where σ1 ∈ Σ∗ is a finite prefix, and
LTL formula is replaced with straight_500m from the AP              σ2 ∈ Σ+ is a non-empty finite loop, such that σ is accepted
Library due to their similarity, and go_straight_200m is
replaced with the format-similar AP straight_200m. All              by A1 but rejected by A2 (i.e., witnessing L(A1 ) ̸⊆ L(A2 )),
other parts in the LTL formula remain unchanged, which              then a finite counterexample path ρ ∈ Pσ on σ exists, with
results in a new LTL 
                     formula  as follows:                           Pσ as in (1), which is simulable in A1 but not simulable in
                                                                    A2 .
                        
 F (straight 200m) ∧ X G right turn Maple St →
                                                                    Proof 1: Let σ = σ1 (σ2 )ω ∈ L(A1 ) \ L(A2 ) be a
 F straight 500m ∧ X(left turn Oak St ∧ F (straight 300m))          counterexample word. By definition, there exists an accepting
                                                            (2)     path of A1 on σ:
   In the Operator Matching step, both are correctly matched.                               σ1       σ
                                                                                                     2       2σ
                                                                                  ρ1 : q1,0 −→ q1,c −→ q1,c −→ ··· ,
The resulting LTL then undergoes the Inclusion Check.          *
   2) Inclusion Check: After the syntactic check, the LTL             where σ2 visits accepting state(s) infinitely. Assuming that
formulas for the Desired Task and safety constraints are            there is no finite counterexample path ρ on word σ that is
converted into BA format Input_BA and Comparison_BA                 simulable in A1 but not simulable in A2 exists. Then, for all
for the Inclusion Check. We adopt Spot [13] for LTL2BA              n ∈ N, the finite path ρ(n) = σ1 (σ2 )n must be simulable by
translation and RABIT [18] for Inclusion Check. Rather than         A2 ; that is, A2 can simulate a path:
simply integrating these formal tools, we adapt and enhance                         σ  1 (n) σ
                                                                                               n
                                                                                                2  (n)        (n)   (n)
them to meet specific application objectives, while keeping the             ρ2 : q2,0 −→ q2,c −−→  q̃2,c , with q2,c , q̃2,c ∈ Q2 ,
pipeline compatible with alternative solutions.                        Since σ ∈ / L(A2 ), every infinite path of A2 on σ either: 1)
Remark 3. In practice, multiple safety constraints may exist as     Fails to being driven by σ1 (terminating at some i ≤ |σ1 |), or
separate LTL formulas. Our framework verifies each formula          2) Processes σ1 (σ2 )ω but fails to satisfy the Büchi condition
in parallel, supports adding new rules dynamically, and allows      (an ω-regular acceptance condition) (Büchi,1996).
prioritizing checks by importance to provide different levels of       Case 1 (Finite Rejection): Suppose A2 cannot be driven
safety assurance. To provide more intuition for the Inclusion       by σ1 fully. Let i ≤ |σ1 | be the minimal position where no
                                                                                                                σi+1
Check, we now revisit the running example.                          transition in A2 matches A1 ’s step q1,i −−−→ q1,i+1 . The finite
                                                                                  σ1       σ2      σi
Example (continued) Both the Safety Constraint and Desired          path q1,0 −→ q1,1 −→ · · · −→ q1,i can be found in A1 , but
A2 lacks a corresponding transition at step i. This contradicts        Algorithm 1 Comparison Path Storage
the assumption that all finite paths ρ(n) are simulable in A2 .        Input: Two automata A1 , A2 , maximum search depth
   Case 2 (Infinite Rejection): If A2 can be driven by σ1 fully,       maxdepth
let q2,c denote its state after σ1 . The infinite suffix σ2ω induces   Output: A counterexample path string, or null if no coun-
a path in A2 :                                                         terexample is found
                         σ    (1) σ     (2) σ                            1: Initialize post[state][symbol] for state transitions
              ρω         2       2       2
               2 : q2,c −→ q2,c −→ q2,c −→ · · · ,
                                                                         2: Initialize queue with initial state pairs (state1, state2)
   forming an infinite sequence of states. As σ ∈     / L(A2 ), ρω
                                                                 2          from A1 , A2
must fail the Büchi condition. By the pigeonhole principle              3: Initialize visited set to track explored state pairs
( Jukna, 2011), there exists a strongly connected component              4: while queue is not empty do
(SCC) C ⊆ Q2 visited infinitely often in ρω      2 , containing no       5:    Dequeue (state1, state2)
accepting states. Let k ∈ N be the minimal number such that              6:    if state1 is in visited then
A2 ’s path on σ2k closes a cycle within C. Then, the finite              7:       if state2 is in visited[state1] then
                σ1          σ2       σ2
path      q1,0 −→     q1,c −→  · · · −→ q1,c (k + 1 states) can be       8:          continue
found in A1 , but A2 ’s corresponding path ρw  2 either terminates       9:       end if
prematurely or enters C. Both violate the assumption that A2            10:    end if
simulates all finite paths.                                             11:    Add state2 to visited[state1]
   In either case, the existence of ρ which is simulable in             12:    for each symbol s do
A1 but not simulable in A2 is unavoidable, contradicting the            13:       nextStates1 ← post[state1][s]
assumption.                                                      *      14:       nextStates2 ← post[state2][s]
   Proposition 1: Let A1 = (Σ, Q1 , I1 , F1 , δ1 ) and A2 =             15:       if nextStates1 ̸= nextStates2 then
(Σ, Q2 , I2 , F2 , δ2 ) be two Büchi automata. If a counterexam-       16:          Build and store the path from (state1, state2)
ple word σ ∈ Σω exists (as defined in Theorem 1), then the              17:          return the path
counterexample path ρ (as described in Theorem 1) can be                18:       end if
identified in time O(n1 × n2 × m) in the worst-case, where              19:    end for
n1 = |Q1 |, n2 = |Q2 | and m = |Σ|, where | · | being the               20: end while
cardinality of a set.
   Proof 2: Define n1 = |Q1 |, n2 = |Q2 |, and let m = |Σ|. The        also allows for more effective modifications by incorporating
supergraph G(V, E) as defined in Definition 6 is constructed           Environmental Information (cf. Section V-D for the ablation
over state pairs (q1 , q2 ) ∈ Q1 × Q2 , with: |V | ≤ n1 × n2 .         experiment).
We use the Breadth-first search(BFS) Algorithm to traverse                To illustrate this process, we revisit the running example.
from all state pairs at most once to detect a counterexample.          Example (continued) First, we input the counterexample path
Assume the size of the alphabet is fixed and finite, i.e., |Σ| =       into the LLM-as-a-Critic. The obtained violation analysis and
m, then each pair requires exactly m comparisons. Therefore,           correct guidance are then be fed to the User LLM to modify the
the time complexity of transition checks O(·) is bounded by:           LTL specification. Although the LTL still fails the Inclusion
O(·) ≤ O(|V | × m) ≤ O(n1 · n2 · m).                                   Check, after iterating the automated verification loop three
   When a mismatch is found, the counterexample path is                times, the final LTL that adheres to the rules is obtained as
constructed via backtracking from the visited state map (as            follows:
also illustrated in Algorithm 1). The length of this path is at           φ = X(destinationLeftOnMapleStreet) ∧
                                                                                                                              
most the depth of the BFS tree, i.e., n1 × n2 , and can be                    G location start → (F (str 200m) ∨ G(¬str 200m)) ∧
                                                                               
performed in linear time. Since path construction occurs once                 X G right turn Maple St → F (straight 500m ∧
and after all comparisons, it does not affect the asymptotic                                                          
bound.                                                                        X(left turn Oak St ∧ F (straight 300m)))           (3)
   Even if all vertices must be validated for acceptance condi-           Our framework prioritizes safety-compliance over strict
tions, the total operations remain dominated by |V |. Thus, the        semantic fidelity to the Desired Task: when the original
counterexample trace is obtained in time: O(n1 × n2 × m). *            route violates safety, it is reordered with a safe alternative
   To maximize the utility of counterexample paths, we intro-          that still reaches the same destination. In this example, the
duce LLM-as-a-Critic. We discovered that enabling one LLM              initial LTL formula already satisfies the latter part of the
to understand another LLM can overcome the LLM’s lack of               Safety Constraint, so the segment from “turn right onto Maple
knowledge in formal verification and format conversion. First,         Street” remains unchanged. And because the Safety Constraint
we let LLM-as-a-Critic directly analyze the counterexample             requires the journey to begin by proceeding straight or making
path and provide suggestions for modifying the input LTL               a right turn, we add the straight_200m restriction. It also
specification. Then, we pass the output of LLM-as-a-Critic to          stipulates that the destination is reached after a left turn fol-
User LLM, which has access to Environmental Information, to            lowed by straight driving. Using Environmental Information,
perform the actual LTL modifications. This process not only            we identify that the last left turn occurs after entering Maple
enhances the extraction of counterexample information but              Street and therefore add X(destinationLeftOnMapleStreet) to
ensure correct arrival.                                          *                                 TABLE I
   Remark 4. Our ideal objective is to search for an LTL                               S TATISTICS OF STAGE -1 DATASET
specification that satisfies all safety constraints while making               Metric                      Value / Statistics
the minimal semantic modification to the Desired Task. In                      Formula Length (chars)      55–267 (median 167)
practice, we set a maximum number of repair rounds and a                       No. of Unique APs           3–15 (median 9)
                                                                               No. of Temporal Operators   2–10 (median 6)
timeout to prevent infinite correction loop for the Desired Task               Max Nesting Depth           8
over which a safety-compliant case can’t be found.                             Operator Frequency:
   Once the Desired Task in LTL format passes the semantic                     Conjunction (∧)             99.0% (198/200)
                                                                               Disjunction (∨)             37.0% (74/200)
check, a safety-compliant LTL φ(k) after k rounds with respect                 Global (G)                  97.0% (194/200)
to predefined safety constraint is obtained. Note that based                   Until (U )                  39.5% (79/200)
on our framework’s mechanism and the Inclusion Check’s
mathematical rigor, it is guaranteed that any LTL specification      B. Model Fine-tuning
that is not safety-compliant will not be output, which is critical      We employ LLaMA-3-8B-Instruct as the edge-side User
for its involvement in subsequent applications. This would also      LLM, fine-tuned using 4-bit QLoRA to ensure on-device
be shown by the experiment in Section V-D.                           efficiency. This parameter-efficient strategy enables the in-
                                                                     cremental injection of repair knowledge across stages while
               IV. F INETUNING A PPROACH                             avoiding catastrophic drift.
A. Construction of Datasets                                          C. Proof of Efficiency
                                                                        Ablation experiments evaluate the impact of each stage
   A major limitation of existing NL2LTL datasets is their
                                                                     in our progressive fine-tuning strategy. Stage-1 focuses on
abstract APs lacking practical context. We emphasize human-
                                                                     improving the accuracy (i.e., the correctness of initial NL2LTL
centered APs to aid counterexample-driven correction. Since
                                                                     translation before any repair or refinement). Stage-2 enhances
our goal is to fine-tune a lightweight LLM, the dataset must
                                                                     the model’s ability to generate syntactically correct formulas
be compact yet effective.
                                                                     and efficiently self-correct. Stage-3 further equips the model to
   We chose the traffic navigation as the primary scenario. To       align with safety constraints and enhances its ability to perform
support the three-stage-fine-tuning process of our framework,        semantic repair.
we construct dedicated datasets for each stage, following a
                                                                        Stage-1 Similar to [22], we adopt binary accuracy (i.e.,
generate–filter–refine paradigm that ensures syntactic correct-
                                                                     100% correct or not) to measure raw translation performance,
ness, semantic alignment, and safety-compliance, respectively.
                                                                     although this is not our primary focus. The evaluation is
   1) For stage-1, 50 navigation instruction templates were          conducted on the 300-sample evaluation benchmark with 6
expanded via GPT-4 into NL-LTL pairs. Generated formulas             different settings.
were validated with SPOT [13], retaining only syntactically
                                                                        • LLaMA-Origin: the base LLaMA-3-8B-Instruct model
correct ones. We first perform a manual semantic check to
                                                                           without fine-tuning.
ensure each natural language instruction accurately reflects the
                                                                        • GPT-4: zero-shot prompting using the same task format.
intent of its corresponding LTL formula. Then, we standardize
                                                                        • LLaMA-200-raw: LLaMA fine-tuned on 200 pairs fil-
and refine the wording of all instructions using a simplified
                                                                           tered only by SPOT for syntactic validity (no semantic
prompt template, making their style consistent with down-
                                                                           cleaning).
stream applications. The final result is a set of 200 high-quality
                                                                        • LLaMA-200-clean: LLaMA fine-tuned on 200 pairs after
Instruction-LTL training pairs.
                                                                           both syntactic validity and manual semantic refinement.
   2) For stage-2, erroneous LTL specifications from genera-
                                                                        • LLaMA-35k-lifted: LLaMA fine-tuned on 35,000
tion were annotated with error types and paired with corrected
                                                                           NL–LTL pairs adapted from the 28k lifted STL corpus
versions passing SPOT, forming 225 Instruction–Corrected
                                                                           in [22]. Each STL formula is first converted into an LTL
LTL pairs across 69 error types.
                                                                           specification, where atomic propositions are rewritten to
   3) For stage-3, using RABIT [18], we curated 50 triples                 represent traffic navigation instructions. The correspond-
(Instruction-Counterexample-Corrected LTL) from cases that                 ing natural language descriptions are then generated by
initially failed Inclusion Checks. These rare and time-                    GPT-4.
consuming cases make the collection especially valuable for             • LLaMA-200-refined: LLaMA fine-tuned on 200 cleaned
training; we demonstrate its effectiveness in Section IV-C.                pairs with deeper refinement and instruction-level opti-
   The Stage-1 dataset contains formulas with up to 8 nesting              mization (cf. Section IV-A).
depths, with 99.0% conjunctions and 39.5% until operators.              The results (cf. Table III) highlight the importance of data
Detailed dataset statistics are provided in Table I. For evalu-      quality: simply cleaning a 200-example corpus (LLaMA-200-
ation, we construct a set of 300 naturalistic navigation tasks       clean) narrows the gap to GPT-4, while a refined dataset makes
featuring diverse logical structures and previously unseen com-      LLaMa outperform GPT-4 with a lightweight 8B model. Con-
binations of atomic propositions. This dataset is completely         versely, a much larger but less targeted corpus (LLaMA-35k-
held out from all training stages and serves as the evaluation       lifted) degrades performance confirming that task-specific, se-
benchmark for all LTL specification generation tasks in our          mantically aligned data outweighs sheer quantity for compact
work.
LLMs in structured specification generation. Among Stage-            before nl2spec translation. These rephrased instructions
1 configurations, LLaMA-200-refined achieves the highest             serve as its evaluation input.
accuracy and is therefore selected for subsequent fine-tuning.          We also conduct ablation studies to investigate the necessity
   Stage-2 To evaluate the effect of syntactic correction fine-      of both User LLM and Agent LLM in our framework. These
tuning, we measure the average number of syntax correction           variants isolate the contribution of each model and allow us to
iterations required to produce a syntactically correct LTL for-      assess how collaboration between cloud and edge components
mula. This metric reflects both the model’s initial correctness      influences final safety outcomes.
and its ability to efficiently repair errors when necessary.         B. Quality of Initial Translation.
   As shown in Table III, AutoSafeLTL achieves the best                 We first evaluate the initial violation rate on the bench-
results, reducing the average to 0.56 versus 1.72 at Stage-          mark—i.e., the proportion of initially generated LTL formulas
1—a 67% drop—outperforming LLaMA-Origin and GPT-4.                   that conflict with safety-compliance. Each initial LTL for-
This shows Stage-2 fine-tuning effectively instills syntactic        mula undergoes a single Inclusion Check: those marked IN-
knowledge, with many formulas correct on the first attempt.          CLUDED are considered compliant, all others are violations.
   Stage-3 To evaluate the effect of semantic correction fine-          Safety-compliance is often overlooked in prior LTL genera-
tuning, we measure the average number of semantic correction         tion research. As shown in Table IV, prior approaches exhibit
iterations—i.e., revisions required to achieve an Included           a 100% violation rate, indicating that none of their generated
status from a safety-violating LTL formula. This metric reflects     LTL formulas initially conform to the safety constraints.
the model’s intrinsic safety capability and ability to efficiently   In contrast, our AutoSafeLTL*—a variant that uses only
repair non-compliant formulas.                                       the User LLM without invoking the automated verification
   The final stage further enhances semantic alignment through       loop—achieves a violation rate of 98%, successfully produc-
verification-guided correction. AutoSafeLTL (Stage-3)                ing safety-compliant LTL at generation time.
achieves the best performance on both syntax (0.51 fixes)               This result, though modest, is significant: it confirms that
and semantic repair (4.3 fixes), outperforming all baselines         progressive fine-tuning allows the model to internalize safety
including GPT-4. And since Stage-3 introduces perturbations          priors and generate compliant LTLs natively—a feat un-
during counterexample-driven refinement, which may reduce            matched by baselines. It highlights the importance of training-
surface-level matching but improve safety-compliance, its ac-        level safety awareness for critical CPS applications.
curacy (93.6%) is slightly below the Stage-1’s peak, yet still
outperforms GPT-4. This aligns with our main goal—ensuring           C. Quality of Semantic Faithfulness
safety-compliant LTLs.                                                  While our primary focus is provable safety-compliance
                                                                     rather than semantic faithfulness, we evaluated our frame-
                V. F RAMEWORK E VALUATION
                                                                     work’s ability to preserve user intent. Following the protocol
A. Setup                                                             in [22], we tested models from all three fine-tuning stages on
   We evaluate our framework’s end-to-end effectiveness under        an extended dataset of 1,000 navigation tasks, using their con-
a cloud–edge collaborative architecture, using violation counts,     sistency metric to verify that core objectives (e.g., waypoints,
i.e., safety violations detected via Inclusion Check against         actions) remain intact in the generated LTL.
predefined safety constraints, as the primary metric. Lower             The semantic consistency scores across the three fine-
violation counts indicate better safety-compliance.                  tuning stages are 94.7% (S1), 92.5% (S2), and 91.1% (S3).
   We deploy GPT-4 as cloud-edge Agent LLMs without                  A slight decline is observed across the stages, which aligns
fine-tuning, accessed via API and prompt engineering. Our            with our design goal: later stages increasingly prioritize safety-
evaluation is conducted on the same evaluation benchmark             compliant repair when conflicts with safety constraints arise.
(cf. Section IV-A).                                                  However, the final model (Stage-3) still maintains a high
   We compare our approach against several baselines:                consistency score (> 91%), demonstrating that AutoSafeLTL
                                                                     effectively minimizes semantic drift while enforcing rigorous
   • LLaMA&GPT-4: zero-shot prompting using the same
                                                                     safety guarantees.
      template as our method.
   • nl2spec [23]: a LTL extraction tool. We adopt its               D. Quality of Verified Translation and Ablation Study
      default settings—GPT-3.5-turbo as the backend,                    Next, we evaluate the effectiveness of our safety assurance
      minimal extraction mode, and Number of tries                   component Automated Verification module. Safety-compliant
      set to 3.                                                      is defined by an LTL formula passing the Inclusion Check;
   • AutoSafeLTL: our full pipeline under the collaborative          we also measure the iterations required to reach this state as
      cloud–edge setting.                                            an efficiency metric.
   Notably, many real-world navigation instructions in our              Applying our full verification pipeline (+B) to LTLs gener-
dataset lack a rigid logical structure, resulting in very low        ated by multiple baselines like LLaMA, GPT-4, and nl2spec
translation coverage by nl2spec (less than 5% of original in-        yields a 0% violation rate across all models (Table II), con-
puts produce valid LTL). For fair comparison, we use GPT-4o          firming its generalizability. Notably, AutoSafeLTL achieves
to rewrite all Desired Tasks into logically enhanced forms           this with the fewest interaction rounds (5.7)—significantly
                                                              TABLE II
   V IOLATION RATE AND INTERACTION ROUNDS ON THE BENCHMARK DATASET. B DENOTES THE AUTOMATED V ERIFICATION COMPONENT; C, THE
                                           LLM-as-an-Aligner; AND D, THE LLM-as-a-Critic.


                       LLaMA+B            GPT-4+B              nl2spec+B          AutoSafeLTL              AutoSafeLTL-C              AutoSafeLTL-D

Violation (%)               0                   0                  0                     0                        0                           0
Avg. Interaction           16.2                7.8                6.5                   4.3                      15.0                        11.0


                            TABLE III
S TAGE - WISE PERFORMANCE OF OUR FRAMEWORK . ACCURACY REFLECTS             counterexample path extraction algorithm is highly efficient
  THE INITIAL GENERATED LTL’ S QUALITY; S YN ./S EM . F IXES INDICATE      and that the computational bottleneck lies in LLM inference
          AVERAGE ITERATIONS FOR SYNTAX / SEMANTIC REPAIR .
                                                                           rather than the safety assurance mechanism.
 Model                        Accuracy     Syn.          Sem.                                          TABLE V
                              (%)          Fixes         Fixes                  C OMPONENT L ATENCY B REAKDOWN ( PER ITERATION ROUND ).
 LLaMA-Origin                 86.7         2.1           16.2
                              (260/300)                                     Component                               Time (s)            Share (%)
 GPT-4                        92.3         0.85          7.8
                                                                            LLM Generation                           0.7600                95.9%
                              (277/300)
                                                                            BA Construction                          0.0097                 1.2%
 AutoSafeLTL (Stage-1)        95.7         1.72          7.1
                                                                            Safety Verification                      0.0227                 2.9%
                              (287/300)
                                                                            Total (Single-stream)                    0.7924                100%
 LLaMA-200-raw                91.3         –             –
                              (274/300)
 LLaMA-200-clean              92.7         –             –                                          ACKNOWLEDGMENT
                              (278/300)
 LLaMA-35k-lifted             90.0         –             –                   This work was supported by Guangzhou-HKUST(GZ) Joint
                              (270/300)                                    Funding Program (Grant No. 2025A03J4493), Education
 AutoSafeLTL (Stage-2)        94.3         0.56          6.8               Bureau of Guangzhou Municipality, Guangdong Provincial
                              (283/300)                                    Project 2024QN11X053, and the Youth S&T Talent Support
 AutoSafeLTL (Stage-3)        93.6         0.51          4.3
                              (281/300)
                                                                           Programme of GDSTA (SKXRC2025468).
                                                                                                 R EFERENCES
                            TABLE IV                                        [1] A. Pnueli, “The temporal logic of programs,” in 18th Annual Symposium
  I NITIAL VIOLATION RATE COMPARISON . AUTO S AFE LTL* USES ONLY                on Foundations of Computer Science (sfcs 1977), 1977, pp. 46–57.
             User LLM WITHOUT AUTOMATED VERIFICATION .                      [2] Y. Chen, R. Gandhi, Y. Zhang, and C. Fan, “NL2TL: Transforming
                                                                                natural languages to temporal logics using large language models,”
                   llama          gpt-4   nl2spec    autosafeltl*               in Proceedings of the 2023 Conference on Empirical Methods in
                                                                                Natural Language Processing, H. Bouamor, J. Pino, and K. Bali, Eds.
 violation (%)      100           100       100          98                     Singapore: Association for Computational Linguistics, 2023, pp. 15 880–
                                                                                15 903.
outperforming GPT-4+B (7.8) and LLaMA+B (16.2)—demon-                       [3] C. Baier and J.-P. Katoen, Principles of model checking. Cambridge,
                                                                                Mass.: MIT Press, 2008.
strating superior efficiency in aligning with safety constraints.           [4] P. Gastin and D. Oddoux, Fast LTL to Büchi Automata Translation,
   To further understand the role of each cloud-side agent,                     ser. Lecture Notes in Computer Science. Berlin, Heidelberg: Springer
we perform ablation experiments by selectively removing                         Berlin Heidelberg, 2001, vol. 2102, p. 53–65.
                                                                            [5] L. Grunske, “Specification patterns for probabilistic quality properties,”
LLM-as-an-Aligner (AutoSafeLTL-C) and LLM-as-a-Critic                           in Proceedings of the 13th international conference on Software engi-
(AutoSafeLTL-D). Both variants still achieve full com-                          neering - ICSE ’08. Leipzig, Germany: ACM Press, 2008, p. 31.
pliance, but at the cost of more iterations (15.0 and 11.0,                 [6] R. Gerth, D. Dolech, D. Peled, M. Vardi, and P. Wolper, “Simple on-
                                                                                the-fly automatic verification of linear temporal logic,” Proceedings of
respectively), highlighting the complementary importance of                     the 6th Symposium on Logic in Computer Science, vol. 15, 1995.
both agents in minimizing verification overhead.                            [7] M. Vardi, “An automata-theoretic approach to linear temporal logic,”
                                                                                Lecture Notes in Computer Science, 1996.
E. Inference Latency and Efficiency                                         [8] G. Holzmann, “The model checker spin,” IEEE Transactions on Software
                                                                                Engineering, vol. 23, no. 5, p. 279–295, 1997.
   To assess the practical feasibility of AutoSafeLTL for                   [9] F. Somenzi and R. Bloem, Efficient Büchi Automata from LTL Formulae,
real-time applications, we conducted a latency analysis on                      ser. Lecture Notes in Computer Science. Berlin, Heidelberg: Springer
                                                                                Berlin Heidelberg, 2000, vol. 1855, p. 248–263.
an NVIDIA A6000 GPU. With a batch size of 20 and five                      [10] T. Babiak, M. Křetı́nský, V. Řehák, and J. Strejček, LTL to Büchi
parallel safety constraints, the framework averages 0.27s per                   Automata Translation: Fast and More Deterministic, ser. Lecture Notes
iteration. Given the 4.3-round average to reach full compli-                    in Computer Science. Berlin, Heidelberg: Springer Berlin Heidelberg,
                                                                                2012, vol. 7214, p. 95–109.
ance (Table II), the total end-to-end latency is approximately             [11] A. Duret-Lutz and D. Poitrenaud, “Spot: an extensible model checking
1.16s, making it compatible with high-level planning cycles.                    library using transition-based generalized buchi automata,” in The IEEE
Detailed latency statistics are provided in Tabel V. Notably,                   Computer Society’s 12th Annual International Symposium on Modeling,
                                                                                Analysis, and Simulation of Computer and Telecommunications Systems,
formal verification (BA Construction and Inclusion Check)                       2004. (MASCOTS 2004). Proceedings. Volendam, The Netherlands,
accounts for only ≈ 4% of total time. This confirms that our                    EU: IEEE, 2004, p. 76–83.
[12] A. Duret-Lutz, A. Lewkowicz, A. Fauchille, T. Michaud, É. Renault,
     and L. Xu, “Spot 2.0 — a framework for ltl and ω-automata manipula-
     tion,” in Automated Technology for Verification and Analysis, C. Artho,
     A. Legay, and D. Peled, Eds. Cham: Springer International Publishing,
     2016, pp. 122–129.
[13] A. Duret-Lutz, E. Renault, M. Colange, F. Renkin, A. Gbaguidi Aisse,
     P. Schlehuber-Caissier, T. Medioni, A. Martin, J. Dubois, C. Gillard, and
     H. Lauko, From Spot 2.0 to Spot 2.10: What’s New?, ser. Lecture Notes
     in Computer Science. Cham: Springer International Publishing, 2022,
     vol. 13372, p. 174–187.
[14] K. Esterle, L. Gressenbuch, and A. Knoll, “Formalizing traffic rules for
     machine interpretability,” in 2020 IEEE 3rd Connected and Automated
     Vehicles Symposium (CAVS). IEEE, 2020, pp. 1–7.
[15] P. A. Abdulla, Y.-F. Chen, L. Clemente, L. Holı́k, C.-D. Hong, R. Mayr,
     and T. Vojnar, “Advanced ramsey-based büchi automata inclusion
     testing,” in CONCUR 2011 – Concurrency Theory, J.-P. Katoen and
     B. König, Eds. Berlin, Heidelberg: Springer Berlin Heidelberg, 2011,
     pp. 187–202.
[16] D. L. Dill, A. J. Hu, and H. Wong-Toi, Checking for language inclusion
     using simulation preorders, ser. Lecture Notes in Computer Science.
     Berlin, Heidelberg: Springer Berlin Heidelberg, 1992, vol. 575, p.
     255–265.
[17] T. Wang, Y. Shen, T. Chen, B. Ji, T. Zhu, and M. Lv, “Language
     inclusion checking of timed automata based on property patterns,”
     Applied Sciences, vol. 12, no. 24, p. 12946, 2022.
[18] L. Clemente and R. Mayr, “Efficient reduction of nondeterministic au-
     tomata with application to language inclusion testing,” Logical Methods
     in Computer Science, vol. Volume 15, Issue 1, 2017.
[19] N. Bousquet and C. Löding, Equivalence and Inclusion Problem for
     Strongly Unambiguous Büchi Automata, ser. Lecture Notes in Computer
     Science. Berlin, Heidelberg: Springer Berlin Heidelberg, 2010, vol.
     6031, p. 118–129.
[20] J. Ouaknine and J. Worrell, “On the language inclusion problem for
     timed automata: closing a decidability gap,” in Proceedings of the 19th
     Annual IEEE Symposium on Logic in Computer Science, 2004., 2004,
     pp. 54–63.
[21] P. A. Abdulla, Y.-F. Chen, and L. e. a. Clemente, “Advanced ramsey-
     based büchi automata inclusion testing,” in CONCUR 2011 – Concur-
     rency Theory, J.-P. Katoen and B. König, Eds. Berlin, Heidelberg:
     Springer Berlin Heidelberg, 2011, pp. 187–202.
[22] Y. Chen, R. Gandhi, and Y. e. a. Zhang, “Nl2tl: Transforming nat-
     ural languages to temporal logics using large language models,” no.
     arXiv:2305.07766, arXiv:2305.07766 [cs].
[23] M. Cosler, C. Hahn, D. Mendoza, F. Schmitt, and C. Trippel, nl2spec:
     Interactively Translating Unstructured Natural Language to Temporal
     Logics with Large Language Models, ser. Lecture Notes in Computer
     Science. Cham: Springer Nature Switzerland, 2023, vol. 13965, p.
     383–396.
