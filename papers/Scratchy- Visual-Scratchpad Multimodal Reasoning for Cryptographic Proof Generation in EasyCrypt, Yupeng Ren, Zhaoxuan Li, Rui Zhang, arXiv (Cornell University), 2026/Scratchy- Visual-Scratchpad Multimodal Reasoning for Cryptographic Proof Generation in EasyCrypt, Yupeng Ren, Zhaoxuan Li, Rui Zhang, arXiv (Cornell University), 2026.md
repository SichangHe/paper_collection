                                            Scratchy: Visual-Scratchpad Multimodal Reasoning for Cryptographic
                                                               Proof Generation in EasyCrypt
                                                                 Yupeng Ren1,2 , Zhaoxuan Li1,2 , Rui Zhang1,2
                                                                 1
                                                             State Key Laboratory of Cyberspace Security Defense,
                                                     Institute of Information Engineering, Chinese Academy of Sciences,
                                                                             Beijing 100085, China
                                        2
                                          School of Cyber Security, University of Chinese Academy of Sciences, Beijing 100049, China
                                                                                    renyupeng24@mails.ucas.ac.cn
                                                                                  {lizhaoxuan,zhangrui}@iie.ac.cn

                                                                                                                                Professional multimodal graph leads every text baseline
                                                               Abstract                                                                                                   11/40 · 27.5%
                                                                                                                  No relation




                                             Large language models (LLMs) have recently                         Theorem text                               6/40 · 15.0%
arXiv:2609.06226v1 [cs.CR] 5 Sep 2026




                                             made substantial progress in formal proof gen-                   Coarse relation                                    8/40 · 20.0%

                                             eration, yet presenting distinctive challenges
                                                                                                             Generic diagram                                                                     19/40 · 47.5%
                                             in cryptographic area. Computational secu-
                                             rity arguments posit that a valid proof must                      Shuffled graph                                                                      20/40 · 50.0%



                                             coordinate probability, adversarial games, in-                                                                                                                      25/40 · 62.5%
                                                                                                      Professional multimodal

                                             variants, assumptions and bounds, which can
                                                                                                                                 0               20                 40                    60                       80            100
                                             be provided by a machine-checked framework                                                                        EasyCrypt compile pass rate (%)


                                             named EasyCrypt. Although all objects may
                                             appear in available context, LLMs still struggle         Figure 1: Results of the API-based EasyCrypt proof-
                                             because proof-theoretic dependencies are typi-           generation Observation across six representation condi-
                                             cally implicit in a linear representation and dis-       tions. The professional multimodal graph achieves the
                                             tributed across multiple programs. So, this pa-          highest compile pass rate (62.5%, 25/40), outperforming
                                             per presents Scratchy, a visual-scratchpad ap-           all baselines.
                                             proach that exposes these dependencies for mul-
                                             timodal generation. Given the natural-language
                                             security description, with formal context and            Lean corpora, self-play that alternates conjecturing
                                             target propositions, the proof objects can be            and proving, and verifier-guided repair of gener-
                                             normalized into a typed proof-relation graph.            ated proofs (Ying et al., 2024; Dong and Ma, 2025;
                                             Then a structure-preserving visual compiler
                                                                                                      Ospanov et al., 2025). These advances show that
                                             transforms the graph into the formula-rich vi-
                                             sual proof state that guides a multimodal model          formal libraries and prover feedback can effectively
                                             in generating the EasyCrypt proof. Also, the             support proof generation. However, the dominant
                                             Scratchy-eval, a 114-task dataset derived from           setting remains mathematical theorem proving, and
                                             reliable official EasyCrypt files, has been in-          the interface between the model and the prover
                                             troduced. It contains 64 security-form proof             is still primarily composed of serialized theorem
                                             generations and 50 multiple-choice knowledge             statements, proof code, candidate premises, and
                                             tests. After a series of evaluations, covering           diagnostic messages.
                                             semantic grounding, relational invariants, and
                                             game reductions, classical LLMs like GPT-5.6-               Cryptographic proofs have a different structure.
                                             Sol and Claude-Opus-5 have gained a clear ad-            A computational security argument must coordi-
                                             vantage from Scratchy’s structured visual proof          nate probabilistic programs, games, adversarial
                                             states. This contrast suggests that explicit proof       capabilities, invariants, security assumptions, and
                                             structure can make the improvement and multi-            concrete advantage bounds. Correctness depends
                                             modal proof-state representation as a promising          not only on whether these objects are available,
                                             direction for computer-aided cryptography.
                                                                                                      but also on the direction and order required by the
                                                                                                      security reduction. Foundational work on machine-
                                        1    Introduction
                                                                                                      checked cryptography developed CertiCrypt for
                                        With the rapid development of Large Language                  code-based game proofs and subsequently intro-
                                        Models (LLMs), formal proof generation has be-                duced EasyCrypt to elaborate machine-checkable
                                        come an important task for machine reasoning. Re-             security proofs from game sketches (Barthe et al.,
                                        cently, researchers have expanded formal supervi-             2009, 2011). These systems established that pro-
                                        sion through synthetic natural language, including            gram transformations, relational judgments, and

                                                                                                  1
               Table 1: Notation expolited in the Scratchy pipeline and the motivating Observation.
            (a) Scratchy proof objects and verification                          (b) Observation metrics and routing
Symbol             Meaning                                         Symbol            Meaning
X,x                Security setting and task.                      T , T, t          Task set, size, and index.
C, Γ               Local context and environment.                  M, M, m           Model set, size, and index.
ϕ                  Target obligation.                              MAPI              Hosted-model pool.
q                  Structured Natural-Language Proof Sketch.       K, K, c           Condition set, size, and index.
G = (V, E, τ, λ)   Typed relation graph.                           cNR , cTH , cCR   Text conditions.
V, E               Graph nodes and edges.                          cGD , cSG , cPG   Graph conditions.
τ, λ               Type and label maps.                            Ktext             Text-condition set.
R                  Visual compiler.                                Kvctl             Visual-control set.
IG = R(G)          Visual proof state.                             ymtc P            Compile outcome.
Gi , GL , GR       Hybrid and paired games.                        Smc = t ymtc      Compile count.
viL , viR          Aligned state values.                           pbc               Pooled pass rate.
ri                 Transition cue.                                 [Lc , Uc ]        Wilson interval.
∆ij                Game distance.                                  ctext
                                                                     m , cm
                                                                            vctl
                                                                                     Best text/visual controls.
                                                                     text   vctl
ϵi                 Game-hop bound.                                 δm , δm           Professional-condition gains.
π, π
   b               Proof fragments.                                zmt               Outcome class.
pθ , θ             Generator and parameters.                       ℓ                 Language-layer index.
                                                                       (c)
S[bπ]              Reconstructed source.                           Hℓ , ∆Hℓ          Routing entropy/change.
                                                                      (c)
VEC                EasyCrypt verifier.                             Uℓ , ∆Uℓ          Expert utilization/change.
⊤, ⊥               Verification outcomes.                          DJS               Routing divergence.
Pr[Gi ⇒ 1], I      Probability and invariant.                      Nimg , Avis       Image tokens/activation.



concrete security bounds can be rigorously checked                 oformalization rather than machine-checked cryp-
within a formal framework. Researchers further                     tographic security proofs (Murphy et al., 2024).
proposed EasyCrypt proof workflow and demon-                       Thus, whether task-specific images can improve
strated representative applications to cryptographic               machine-checkable security-proof generation, and
standards and post-quantum constructions (Barthe                   which visual proof state is most effective, are still
et al., 2012; Almeida et al., 2019; Barbosa et al.,                worth diving into.
2021).                                                                A preliminary observation indicates that task-
   Despite the relational of cryptographic proofs,                 specific, structured proof diagrams can improve
recent proving pipelines still use textual or sym-                 EasyCrypt proof generation across multimodal
bolic sequences as their primary interface. They                   models, whereas generic or structurally corrupted
construct natural-language with formal corpora to                  diagrams provide weaker benefits. This finding sug-
improve training, search, and feedback (Ying et al.,               gests that the gain depends not only on the visual
2024; Dong and Ma, 2025; Wang et al., 2025;                        modality itself but also on the faithful organization
Ospanov et al., 2025). However, these works do not                 of proof objects and their relations, motivating the
present the distributed relationships within a proof               design of Scratchy.
to the generator as a unified visual state. A linear                  To sum up, this paper proposes Scratchy. While
interface preserves symbolic content, but it does                  the security attributes are received, within local for-
not naturally expose object types. Consequently,                   mal context, target obligation, and proof guidance,
the relationships between the direction of a game                  the distributed objects can be normalized into a
hop and multiple dependency paths running from                     typed proof-relation graph. Its nodes distinguish
local obligations to the security goal cannot be si-               threat models, program facts, proof obligations,
multaneously represented.                                          rules, and security goals. At the same time, the
   Multimodal images provide a representation                      constraint, transformation, and discharge relations
channel that remains underexplored. Researchers                    are supported by directed edges encoding. The
have begun to treat images as intermediate rea-                    graph specifies the semantic structure that a visual
soning states. Visual Sketchpad allows a model                     representation must preserve, turning the search for
to draw visual marks, GraphVis preserves graph                     an effective image into a constrained proof-state
structure through the visual modality, and MIRA                    design problem.
evaluates problems that require intermediate visual                   As shown in Section. 4, a structure-preserving
cues (Hu et al., 2024; Deng et al., 2024; Zhou et al.,             visual compiler renders the relation graph as a
2026). In an adjacent formalization setting, Lea-                  formula-rich visual scratchpad. Guided by different
nEuclid studies diagram-dependent Euclidean ge-                    states, the multimodal model performs program un-
ometry with GPT-4V, but targets mathematical aut-                  folding, state alignment, rule application, and goal

                                                               2
discharge to generate an EasyCrypt proof fragment.         2.2   Language Models for Cryptographic
The fragment then enters an EasyCrypt verifica-                  Formalization
tion loop for parsing and type checking, obligation
                                                           CrypFormBench evaluates language models on in-
discharge, and target closure.
                                                           terpretation, generation, completion, transforma-
   For systematic evaluation, this paper further in-
                                                           tion, and correction across cryptographic formal-
troduces Scratchy-eval. The benchmark derives
                                                           verifier languages (Li et al., 2026). ShannonProver
114 tasks from 26 source groups and 37 pinned
                                                           more directly targets EasyCrypt, constructing proof
official EasyCrypt files. It contains 64 free-form
                                                           scripts from a supplied security model and lemma-
proof generation tasks and 50 multiple-choice tasks
                                                           level decomposition (Ma et al., 2026). Differently,
on semantic recognition. The tasks are evaluated
                                                           this paper pays attention to another complementary
under six paired representation conditions. Compi-
                                                           bottleneck, which is compiling distributed formal
lation under EasyCrypt is the primary criterion for
                                                           context into a structured visual state and studies
generation.
                                                           whether image presence and relation fidelity affect
   The main contributions of this work are as fol-
                                                           machine-checkable proof generation.
lows:
  Empirical Finding                                        2.3   Language Models for Formal Proving
    This paper provides empirical evidence that            Recently, researcher expands supervision and eval-
    structured visual proof states can improve Easy-       uation through synthetic Lean corpora and diffi-
    Crypt security-proof generation and that rela-         cult multilingual theorem benchmarks (Ying et al.,
    tion fidelity matters beyond image presence            2024; Tsoukalas et al., 2024). Proof search has
    alone.                                                 been improved through conjecturer-prover self-
                                                           play (Dong and Ma, 2025), proof-assistant-guided
    Scratchy                                               reinforcement learning and tree search (Xin et al.,
    This paper introduces Scratchy, which treats           2025), interleaved informal reasoning and for-
    visual-representation selection as a constrained       mal tactics (Lin et al., 2025), scaffolded synthe-
    proof-state design problem and realizes it             sis with self-correction (Lin et al., 2026), and
    through typed proof-relation graph, structure-         structure-aware premise selection (Wang et al.,
    preserving visual compiler, and an EasyCrypt           2025). Verifier-integrated systems further repair
    verification loop.                                     Lean proofs from compiler feedback with Isabelle
                                                           theorem proving (Ospanov et al., 2025; Lin et al.,
    Scratchy-eval                                          2024). Although these methods improve data,
    This paper contributes Scratchy-eval, a bench-         search, and feedback, their model-facing states re-
    mark with 114 tasks and six paired conditions          main predominantly textual or symbolic and mainly
    for jointly evaluating proof generation, static        target mathematical theorems or general program
    validity, and semantic recognition.                    verification.

                                                           2.4   Visual Intermediate Reasoning
2     Related work
                                                           Multimodal reasoning increasingly treats images
2.1    Machine-Checked Cryptographic Proofs                as intermediate computational states. Visualization-
Machine-checked cryptography regards security              of-Thought, Vision-Augmented Prompting, Visual
arguments as formally representable and verifi-            Sketchpad, and CogCoM respectively render rea-
able objects, which has led to the development             soning traces, synthesize and refine visual cues,
of CertiCrypt and EasyCrypt (Barthe et al., 2009,          reuse drawn marks, or expose traceable visual ma-
2011). Subsequently, studies have further devel-           nipulations (Wu et al., 2024; Xiao et al., 2024; Hu
oped dedicated cryptographic-proof workflows and           et al., 2024; Qi et al., 2025). GraphVis and GITA
extensions such as EasyPQC (Barthe et al., 2012;           further show that visual encodings can preserve
Almeida et al., 2019; Barbosa et al., 2021). With          graph connectivity and that graph layout affects
program transformations, relational judgments, and         reasoning (Deng et al., 2024; Wei et al., 2024).
probabilistic bounds, these tools provide strong           Visual CoT and MIRA evaluate localized or indis-
support for formal cryptographic proofs and offer          pensable intermediate visual evidence, while Lea-
a correctness foundation for the generating results.       nEuclid studies diagram-dependent mathematical

                                                       3
           Professional multimodal remains the top-performing condition                                                                                         Professional-vs-coarse expert utilization

                                                      4/10                                       Best text baseline                                                  Reference profile
 Claude                                                       5/10                               Best visual control                                     0.10        Comparison profile
                                                                                     7/10
                                                                                                 Professional multimodal

                                   2/10
 Gemini                                                       5/10                                                                                       0.08
                                                                              6/10




                                                                                                                                  Expert-utilization Δ
                                   2/10
                                                                                                                                                         0.06
    GPT                                                                       6/10
                                                                              6/10


                                                      4/10                                                                                               0.04
    Kimi                                                                      6/10
                                                                              6/10


                                                                                                                                                         0.02
                       1/10
Gemma                              2/10
                                          3/10


            0                 20                 40                      60                 80                         100                                      0                    5          10           15            20      25
                                                 Compilable proofs (%)                                                                                                                                Language layer


                               (a) Model-wise comparison                                                                                                 (b) Expert-utilization profiles (Gemma-4-26B-A4B)

Figure 2: Complementary views of the Observation. The gray curve is the observed reference profile, and the rose
curve is a comparison profile anchored to it. Models involve Claude-opus-5, Gemini-3.7-flash, Kimi-k3, GPT-5.6-sol
and Gemma-4-26B-A4B.


autoformalization (Shao et al., 2024; Zhou et al.,                                                                               Table 2: Sources of the ten paired Observation samples.
2026; Murphy et al., 2024). However, it is still a                                                                               All files are drawn from the pinned official EasyCrypt
                                                                                                                                 repository snapshot (EasyCrypt Development Team,
challenge for these approaches compiles to type
                                                                                                                                 2026).
cryptographic proof relations into a formula-rich
image whose generated proof is judged by Easy-                                                                                   ID                             Focus                    Proof object                  Official source
Crypt. Continuously, Scratchy treats relation fi-
                                                                                                                                 01 Semantic Well-foundedness WF-examp.ec
delity as the central visual-design variable, which                                                                              02 Semantic Dice point mass     Dice4_6.ec
provides a good feasible solution.                                                                                               03 Semantic While termination WhileSampling.ec
                                                                                                                                 04 Relational Async invariant   async-while.ec
3          Observation                                                                                                           05 Relational Bad-event split   FundamentalLemma.ec
                                                                                                                                 06 Reduction Pedersen hiding    Pedersen.ec
Instructively, this paper examines a narrower ques-                                                                              07 Reduction Schnorr soundness SchnorrPK.ec
                                                                                                                                 08 Reduction ElGamal–DDH hop elgamal.ec
tion, whether the representation of available                                                                                    09 Relational PIR coupling      PIR.ec
proof relations can affect EasyCrypt proof gen-                                                                                  10 Reduction Stateful PRG bound PRG.ec
eration with LLMs.
   This observation uses ten paired EasyCrypt obli-
gations (Table 2). Four hosted multimodal mod-                                                                                   dependent contribution.
els form the behavioral summary, while a frozen                                                                                     The local model provides a complementary sig-
local Gemma-4-26B-A4B supplies an internal di-                                                                                   nal about whether the visual input is computation-
agnostic. The six conditions include no-relation,                                                                                ally engaged. This paper examines the layerwise
                                                                                                                                                        (c )       (c )
theorem-only, and coarse-relation text; a generic                                                                                difference ∆Uℓ = Uℓ PG − Uℓ CR between the
diagram and a shuffled-edge graph as visual con-                                                                                 professional graph and coarse-relation text. The
trols; and a complete professional graph (Scratchy).                                                                             recorded reference profile and the compared profile
Within a paired run, reference fragments are hid-                                                                                remain close and positive across all 30 language
den from the model, and a generated fragment is                                                                                  layers (Fig. 2(b)). The trajectory changes across
counted as successful only when it compiles under                                                                                depth rather than appearing as a single constant
the pinned EasyCrypt environment.                                                                                                offset, indicating that the representation condition
   The aggregate API summary gives the profes-                                                                                   is associated with a structured change in expert
sional graph 25/40 compilable fragments (62.5%),                                                                                 usage.
compared with 20/40 (50.0%) for the strongest vi-                                                                                   Therefore, the Observation shows that the rep-
sual control and 11/40 (27.5%) for the strongest                                                                                 resentation of proof relations is itself an important
text condition (Fig. 1). The model-wise view shows                                                                               part of the generation process. The performance
that professional graph is consistently above text                                                                               differences across conditions indicate that struc-
condition, whereas its additional margin over the                                                                                tured visual states can help coordinate distributed
best visual control is smaller and varies by model                                                                               proof objects, while the layerwise changes in ex-
(Fig. 2(a)). The contrast suggests that visual orga-                                                                             pert utilization show that the model responds to
nization may provide a broad benefit, while faithful                                                                             this organization across network depth. These find-
encoding of proof relations can supply a narrower,                                                                               ings motivate moving beyond manually selected

                                                                                                                             4
      Scratchy Proof Context                                                  Typed Proof Relations                                                                                            Visual Scratchpad                       Scratchy Formal Proof

                                                      Threat Model                            Proof Rules                 Security Goal

            Security Attribute                                                                                                                                     Left Game                Right Game                           1            Reconstruction

                                               Adversary     Attack      Simulate
         Real                          Ideal                                                Coupling   Game-Hops

                                                                                                                         Bound Advantage
                       Adversary                                                                                                                                                                           Relational   Hybrid
                                                                                            Preserve Invariant                                                                                             Invariant    Bound
                                                   Sampling           State                                                                                                                                                      Reuse Fragment      Rethink Assumption
                 Local Context                       Program Facts                             Obligation
         Definitions             Assumptions
                                                                                                                                                                                                                                 2         EasyCrypt Checker


                                                                                                                                 Multimodal Large Language Model
             Target Obligation
                                                       Relation Clues with Context                                                                                                                       Program Unfolding                Parse & Type-Check
                                                                                                                 Assumption      Invariant          Goal      State 0     State 1
                                                  Context     Definitions and Assumptions
                                                                Facts, Rules, Obligations
        State 0                   State 2         Relation                                                       Image Patches
                                                   Target      Discharge the Stated Claim                                                                                                                State Alignment                 Discharge Obligations


                                                                                                                                                                                                                                              Close Target
                                                      Visual Scratchpad with Rules                                 Resolve Symbols           Follow Dependencies         Generate Tactics                 Rule Application
                 Proof Guidance

                                                 Scratchpad           Rule cues      State links                                                                                                          Goal Discharge         3       Verification Outcome

        Unfold          Relate         Bound
                                                                                                                                                                                                                                     Accept           Reject/Open
                                                                                                                                 Multimodal Proof Synthesis




Figure 3: The Scratchy pipeline. Structured proof context and an SNPS are deterministically compiled into a typed
proof-relation graph and a formula-rich visual scratchpad. A multimodal model follows the explicit dependencies to
synthesize an EasyCrypt proof fragment, which is reconstructed and checked for acceptance or an open outcome.


diagrams toward a systematic mechanism for con-                                                                                                              Algorithm 1 Deterministic SNPS-to-Graph Compilation
structing visual proof states. Accordingly, this                                                                                                             Require: q grounded in (X , x, C, Γ, ϕ)
paper introduces Scratchy to address these chal-                                                                                                             Ensure: G = (V, E, τ, λ)
                                                                                                                                                              1: Parse the six ordered fields of q
lenges, which organizes security assumptions, pro-                                                                                                            2: for all proof objects declared in q do
gram states, proof obligations, and reduction goals                                                                                                           3:     Add a node to V; assign τ and λ
                                                                                                                                                              4: end for
into a structured visual interface for multimodal                                                                                                             5: for all source-to-target relations in q do
EasyCrypt proof generation.                                                                                                                                   6:     Add the corresponding directed edge to E
                                                                                                                                                              7: end for
4     Methodology                                                                                                                                             8: Order dependency paths toward ϕ
                                                                                                                                                              9: return G
In Scratchy, a Structured Natural-Language
Proof Sketch (SNPS) is taken as the input to visual
composition. The SNPS expresses proof objects                                                                                                                Each output is therefore the direct input to the next
and directed relations through fixed fields, allowing                                                                                                        operation, preserving a traceable route from the
relation extraction and image construction to pro-                                                                                                           SNPS to the verification outcome.
ceed deterministically. And LLMs enter after the                                                                                                             4.2               SNPS-to-Graph Compilation
visual proof state has been constructed, where it
                                                                                                                                                             The first key step compiles the SNPS into the typed
generates the EasyCrypt fragment. Fig. 3 presents
                                                                                                                                                             proof-relation graph
the full pipeline, and Table 1 defines the notation.
4.1    Unified Input and Output                                                                                                                                                                          G = (V, E, τ, λ).                                                (3)

The unified input consists of the security set-                                                                                                              Each SNPS item becomes a node in V. Its field
ting X , task description x, local EasyCrypt cor-                                                                                                            uniquely determines the node type recorded by τ ,
pus C, formal environment Γ, target obligation ϕ,                                                                                                            while λ retains its natural-language description,
and SNPS q. The SNPS contains six fields, in-                                                                                                                EasyCrypt identifier, and formula. Each entry in
cluding T HREAT M ODEL, P ROGRAM FACTS,                                                                                                                      R ELATIONS becomes a directed edge in E. The
P ROOF O BLIGATIONS, P ROOF RULES, S ECU -                                                                                                                   compiler consequently performs parsing, match-
RITY G OAL , and R ELATIONS . The first five                                                                                                                 ing, and normalization without inferring relations
fields declare proof objects, R ELATIONS declares                                                                                                            absent from the SNPS.
the source, target, and meaning of directed depen-                                                                                                              The two deterministic procedures are given in
dency. Identifiers and formulas in q are written                                                                                                             Algorithms 1 and 2.
exactly as they occur in C, Γ, or ϕ.                                                                                                                            There are distinct roles for five node types. A
   The same interface is used throughout the                                                                                                                 threat-model node states the security consequence
pipeline:                                                                                                                                                    addressed by the proof; program-fact nodes provide
                                                                                                                                                             available evidence; proof-obligation nodes state in-
                 (X , x, C, Γ, ϕ, q) −→ G −→ IG ,                                                                                    (1)
                                                                                                                                                            termediate claims; proof-rule nodes describe per-
                   IG −→ π   b −→ VEC S[b  π] .                                                                                      (2)                     mitted transformations; and the security-goal node

                                                                                                                                                    5
       !    THREAT MODEL              THREAT                     O PROOF OBLIGATION           OBLIGATION


      PIR_secure1 remains open if the                           Bridge the open goal using
      fragment misses program-logic                             program-logic unfolding, procedure
                                                  requires
      unfolding or breaks the pinned...            check        inlining, weakest-precondition...

       FORMAL STATEMENT                                          FORMAL STATEMENT
                                                                                                                         G SECURITY / FORMAL GOAL       GOAL
                                                                       ΓEC ⊢ PIR_secure1                   discharges
         proof_gap(PIR_secure1)
      plausible text ≠ checked proof                            preserve statement ∧ assumptions                        Discharge equiv PIR_secure1 in the
                                                                                                                        unchanged official source.


                                                                                                                        FORMAL STATEMENT
       F PROGRAM FACT                     FACT                   R CODE / PROOF RULE                RULE
                                                 constrains                                                guides       EC(PIR_secure1 [⟨body⟩]) = ACCEPT
      Pinned declaration: equiv                                 Follow proc then inline then wp then                        EasyCrypt compile = PASS
      PIR_secure1: PIR.main ~ PIR.main :                        while then auto; reuse the visible
      true ==> ={PIR.s}.                                        symbols PIR.s.

       FORMAL STATEMENT                                          FORMAL STATEMENT

                                                                  route: proc → inline → wp → while →
           official source @ line 92                                              auto
                symbols: PIR.s                                                reuse: PIR.s




Figure 4: Professional visual proof state for a PIR relational obligation. The graph organizes source facts, the target,
a proof-rule route, and the machine-checkable goal into a directed path.


Algorithm 2 Structure-Preserving Visual Compilation
                                                                                        module PIR = {
Require: G = (V, E, τ, λ)                                                                  var s, s' : int list
                                                                                           proc main(i : int) = {
Ensure: IG                                                                                   var j <- 0;
 1: Arrange nodes by the roles recorded in τ                                                 (s, s') <- ([], []);
 2: Render the text, formulas, and code recorded in λ                                        while (j < N) {
 3: for all directed edges in E do                                                             (* sample and update s, s' *)
                                                                                               j <- j + 1;
 4:     Draw its tail, arrowhead, and relation label                                         }
 5: end for                                                                                }
 6: Highlight the dependency paths ending at ϕ                                          }.
 7: return IG = R(G)
                                                                                        equiv PIR_secure1:
                                                                                          PIR.main ~ PIR.main : true ==> ={PIR.s}.
                                                                                        proof.
                                                                                          proc; inline *; wp.
corresponds to ϕ. Edges point from a justification                                        while (={j, PIR.s}); auto.
to the claim it supports. And both proof order and                                      qed.

dependency are recorded by the complete path.                                           Listing 1: Abridged EasyCrypt source for the PIR
                                                                                        example. The relational target and proof fragment
4.3        Graph-to-Visual Compilation
                                                                                        instantiate the SNPS route encoded by the professional
The second key step applies visual compiler R:                                          graph.
                            IG = R(G).                                        (4)
Structure preservation means that node roles, se-                                         For example, Fig. 4 illustrates the resulting vi-
mantic labels, edge directions, and the path to ϕ re-                                   sual proof state with a representative PIR obli-
main directly readable in the output. Role-specific                                     gation. The corresponding EasyCrypt excerpt is
colors and icons encode τ ; formula and code cards                                      shown separately in Listing 1.
display λ; and tail markers, arrowheads, and rela-
tion labels encode E. a stable, robust, and profes-                                     4.4     Proof Synthesis and Verification
sional layout is constructed.                                                           After IG has been constructed, the multimodal gen-
   For relational proofs, IG places GL and GR in                                        erator reads both the textual context and the image:
parallel and connects viL , ri , and viR at correspond-
ing program points. For game-based proofs, it or-                                                          b ∼ pθ (π | x, C, ϕ, q, IG ).
                                                                                                           π                                                   (6)
ders Gi along the reduction and displays next to
the relevant hop.                                                                       The graph route organizes generation into program
                                                                                        unfolding, state alignment, rule application, and
   ∆ij = |Pr[Gi ⇒ 1] − Pr[Gj ⇒ 1]| ,                         ∆ij ≤ ϵi         (5)
                                                                                        goal discharge. Text preserves exact EasyCrypt
   The relational invariant I is placed beside the                                      syntax, while IG preserves the relation structure
state correspondence it constrains.                                                     needed to produce πb.

                                                                                    6
  Finally, Scratchy inserts π b into its original lo-                                                                        CR                       SG                       PG

cation to form S[bπ ]. EasyCrypt parses and type-
                                                                                    40
checks the reconstructed source, discharges its obli-
gations, and closes the target:                                                                                                                             33.3


                                                                                    30




                                                            Compile pass rate (%)
                          
              VEC S[b  π ] ∈ {⊤, ⊥}.              (7)                                                                                                                                           22.8
                                                                                                                                                                                                           25.0

                                                                                                                                                                             21.4                                 20.8
                                                                                    20
                                                                                                                                         17.9
An outcome of ⊤ accepts the fragment, while ⊥
returns the open proof state to reconstruction. Al-                                             12.5
                                                                                                       10.0
                                                                                                                  12.512.5
                                                                                                                                  10.7
                                                                                    10                                                          8.3
gorithms 1 and 2 remain fully deterministic. The                                          7.5
                                                                                                                                                      5.6
                                                                                                                                                                                          7.6

                                                                                                                                                                                    4.3
                                                                                                                                                                   3.6
LLM is used only for the transition from IG to πb.                                                            0               0                                          0                             0
                                                                                    0
                                                                                                              Program         Simple            Complex            Reduction        Extended           Program
                                                                                         Foundations
5     Experiments                                                                                              logics         crypto             crypto              paths           crypto            analysis




5.1    Scratchy-eval
Scratchy-eval is a provenance-preserving bench-             Figure 5: Generation pass rates across seven source
mark constructed from the EasyCrypt corpus (Easy-           families, pooled over four models. Each vertical group
Crypt Development Team, 2026). It contains 114              compares CR (coarse proof-relation text), SG (shuffled-
tasks drawn from 26 protocol or formal-program              edge graph), and PG (Scratchy professional graph); bar
                                                            height and top labels report the percentage of fragments
sources and 37 official files (13,761 lines). 64
                                                            accepted by EasyCrypt. PG leads on the four cryp-
tasks require free-form EasyCrypt proof genera-             tography and reduction-oriented families, SG leads on
tion, while 50 multiple-choice tasks cover static           foundations and program analysis, and the two graph
validity and semantic recognition.                          conditions tie on program logics.
   The generation set comprises 55 lemmas, seven
equivalence judgments, and two expectation-Hoare
judgments. Each generation fixture preserves the               The primary generation metric is compile pass
imports and dependency prefix of an official target         rate: a fragment must parse, type-check, discharge
but replaces its proof. Static-validity items pair          its obligations, and close the target in the pinned
an official statement with syntactically defective          EasyCrypt environment. Exact agreement with
alternatives, and semantic items test the formal            the official fragment is only diagnostic because
role of local constructs. Appendix A provides the           several valid proofs may establish the same tar-
Data Card and summarizes source coverage and                get. Multiple-choice tasks use accuracy, with
construction.                                               static-validity selections independently confirmed
                                                            by compilation. Paired confidence intervals are ob-
5.2    Experimental Setup                                   tained by bootstrap resampling the 26 protocol or
This paper evaluates Claude Opus 5, Gemini 3.7              formal-program sources, preserving dependencies
Flash, GPT-5.6-Sol, and Kimi K3. Each model pro-            among tasks derived from the same source.
duces one response for every task under six paired
                                                            5.3                           Main Results
representation conditions. The complete condition
receives the local source, task-specific professional       Table 3 shows a consistent model-level result: PG
graph, and EasyCrypt decoding card; the other con-          is the strongest generation condition for all four
ditions remove source details, proof paths, identi-         models. Pooled over models, it compiles 54 of
fiers, or edge structure to test which parts of the         256 fragments (21.1%), compared with 24 (9.4%)
visual proof state contribute to generation.                under SG and 11 (4.3%) under CR. The complete
   Each model run contains 684 units, giving 2,736          representation therefore reaches 2.25× the SG rate
model task condition units in total. The task, re-          and 4.91× the CR rate. PG ranges from 14.1%
sponse contract, and output budget remain fixed             on Claude to 28.1% on Gemini, showing that the
within each six-way comparison, while condition             ordering is stable even though absolute proof ability
order is deterministically rotated by task. Be-             differs across models.
fore any model call, 164 fixtures are dynamically              The multiple-choice tasks remain (97.0–99.5%),
checked: the 64 hidden reference proofs and four            making free-form generation the principal source
isolated options for each of the 25 static-validity         of discrimination. Among the 54 compiling PG out-
tasks.                                                      puts, only 10 exactly match the official fragment.

                                                        7
Table 3: Scratchy-eval results under six representation conditions. Each numeric entry is passed/total (%). NR: no
relation knowledge; TH: theorem-only text; CR: coarse proof-relation text; GD: generic diagram; SG: shuffled-edge
graph; PG: Scratchy professional graph.

Model or task set            NR                     TH                   CR                  GD               SG               PG

    Claude Opus 5         0/64 (0.0)             3/64 (4.7)          5/64 (7.8)           1/64 (1.6)       1/64 (1.6)       9/64 (14.1)
    Gemini 3.7 Flash      2/64 (3.1)             2/64 (3.1)          3/64 (4.7)          9/64 (14.1)      9/64 (14.1)      18/64 (28.1)
    GPT-5.6-Sol           2/64 (3.1)             3/64 (4.7)          2/64 (3.1)           4/64 (6.2)       6/64 (9.4)      12/64 (18.8)
    Kimi K3               1/64 (1.6)             1/64 (1.6)          1/64 (1.6)           5/64 (7.8)      8/64 (12.5)      15/64 (23.4)

Pooled generation         5/256 (2.0)          9/256 (3.5)          11/256 (4.3)         19/256 (7.4)     24/256 (9.4)     54/256 (21.1)
Pooled MCQ              194/200 (97.0)       199/200 (99.5)        198/200 (99.0)       198/200 (99.0)   199/200 (99.5)   199/200 (99.5)
Overall                 199/456 (43.6)       208/456 (45.6)        209/456 (45.8)       217/456 (47.6)   223/456 (48.9)   253/456 (55.5)



Table 4: Paired generation comparison over 256 model–                    failures into passes while losing 10 previously pass-
task pairs. PG: Scratchy professional graph; CR: coarse                  ing pairs; against SG, the corresponding counts are
proof-relation text; SG: shuffled-edge graph; W/L/T:
                                                                         39 and nine. Both source-group intervals remain
PG wins/losses/ties; pp: percentage points; CI: source-
group bootstrap 95% confidence interval.                                 above zero. Moreover, 36 of the 54 PG successes
                                                                         are not reproduced by any of the five ablations for
   Compared with        W/L/T          Gain (pp)      95% CI             the same model and target. Fourteen are shared
            CR         53/10/193         +16.8       [8.8, 24.6]
                                                                         with a visual control, two with a text condition, and
            SG         39/9/208          +11.7       [3.5, 19.8]         two with both families. The aggregate improve-
                                                                         ment is thus composed mainly of new machine-
                                                                         accepted proofs, rather than repeated successes on
The remaining 44 are textually different proofs ac-                      tasks already handled by simpler representations.
cepted by EasyCrypt, which would be missed by
reference-only scoring.                                                  5.5        Failure and Efficiency Analysis
                                                                         Among the unsuccessful PG generation units, the
5.4     Protocol and Proof-Structure Analysis
                                                                         largest recurring groups are parse errors (30), in-
Figure 5 locates the gain precisely. PG reaches                          applicable rewrites reported as nothing to rewrite
33.3% on complex cryptography and 21.4% on                               (30), incomplete proofs (19), and by-blocks that
reduction paths. Generic visual organization can be                      cannot close their goals (11). Together they account
sufficient for more local program facts, whereas the                     for 90 failures (44.6%). The remaining bottleneck
largest professional-graph advantage appears when                        is therefore often the local instantiation of the proof
a target depends on a protocol-specific reduction                        route in exact EasyCrypt syntax.
path.
   At the individual-source level, PG compiles                           6        Discussion
9/20 model–target pairs for two-server PIR, 7/16
for UC Diffie–Hellman encryption, 5/16 for syn-                          6.1        A Machine-Checked Proof Contrast
tactic up-to reductions, and 5/16 for the PRG tuto-                      Task 064 provides a concrete view of what changes
rial. It also obtains 3/12 on Pedersen commitment                        between a successful and an unsuccessful genera-
where both CR and SG obtain zero. The broader                            tion. The target is the relational judgment shown in
source coverage behind these counts is summarized                        Figure 4. Listing 2 compares the official fragment
in Table 5.                                                              with two outputs from GPT-5.6-Sol for this same
   The same pattern appears across formal judg-                          target. The official fragment and the professional-
ment types. PG compiles 49/220 lemma pairs                               graph output are accepted by EasyCrypt.
(22.3%), compared with 23/220 for SG (10.5%)                                All three fragments begin with the same local
and 10/220 for CR (4.5%). For relational equiv                           route, including expose the paired procedures with
targets, PG reaches 5/28 (17.9%), whereas both                           proc, unfold calls with inline, and propagate
SG and CR reach 1/28 (3.6%). None of the eight                           postconditions with wp. The decisive step is the
model–task pairs formed by the two ehoare targets                        loop. The rejected output invokes autoimmediately
compiles under any condition.                                            and never states what must remain synchronized
   The paired comparison in Table 4 controls for                         across iterations.
both model and target. Against CR, PG turns 53                              In contrast, the professional-graph output aligns

                                                                     8
(* Official reference: accepted *)                            into a typed proof-relation graph and a formula-rich
proc; inline *; wp.                                           visual state, then guides a multimodal model to pro-
while (={j,PIR.s}); auto.
                                                              duce an EasyCrypt fragment whose correctness is
(* GPT + PG: accepted *)
proc; inline *; wp;                                           decided by the formal verifier. Across Scratchy-
while (={j} /\ ={PIR.s}).
  wp; rnd; skip; auto.
                                                              eval, the professional graph consistently improves
auto.                                                         generation over textual and visual-control condi-
(* GPT + CR: rejected *)                                      tions, with particularly useful gains for relational
by
   proc;
                                                              and reduction-oriented proofs.
   inline *;                                                     Future work will extend Scratchy-eval to addi-
   wp;
   auto.                                                      tional protocols and proof systems, refine SNPS
                                                              authoring and visual compilation, and use verifier
Listing 2: Machine-checked contrast for the PIR target.
PG denotes the professional graph and CR denotes              feedback for targeted repair of syntax and residual
coarse relation text. The official and PG fragments           obligations. A further direction is to study which
compile, whereas CR omits the loop invariant and leaves       visual relations are most useful for different proof
an open goal.                                                 families, enabling proof states that remain concise
                                                              while adapting their structure to the target judg-
                                                              ment.
the random assignment with rnd, and discharges
the loop body before closing the residual goal. Un-
                                                              References
like the official proof, GPT produces the equivalent
conjunction and an explicit body proof. Machine               José Bacelar Almeida, Cécile Baritel-Ruet, Manuel Bar-
                                                                 bosa, Gilles Barthe, François Dupressoir, Benjamin
checking therefore identifies a valid alternative that
                                                                 Grégoire, Vincent Laporte, Tiago Oliveira, Alley
textual exact match would mark as different.                     Stoughton, and Pierre-Yves Strub. 2019. Machine-
                                                                 checked proofs for cryptographic standards: Indif-
6.2    Implications for Scratchy                                 ferentiability of sponge and secure high-assurance
                                                                 implementations of SHA-3. In Proceedings of the
This example reflects the aggregate pattern. The                 2019 ACM SIGSAC Conference on Computer and
professional graph is strongest for all four models              Communications Security, pages 1607–1622. ACM.
and yields its clearest gains on protocol-specific
                                                              Manuel Barbosa, Gilles Barthe, Xiong Fan, Ben-
reductions and relational judgments. For Task 064,
                                                               jamin Grégoire, Shih-Han Hung, Jonathan Katz,
that route makes the preserved state and the loop              Pierre-Yves Strub, Xiaodi Wu, and Li Zhou. 2021.
rule visible at the point where a linear hint remains          EasyPQC: Verifying post-quantum cryptography. In
underspecified. The result supports Scratchy’s                 Proceedings of the 2021 ACM SIGSAC Conference
central design which compiling an SNPS into a                  on Computer and Communications Security, pages
                                                               2564–2586. ACM.
relation-faithful visual state before generation.
   Many remaining failures occur when a plausible             Gilles Barthe, Juan Manuel Crespo, Benjamin Grégoire,
route must be instantiated as exact syntax, espe-               César Kunz, and Santiago Zanella Béguelin. 2012.
                                                                Computer-aided cryptographic proofs. In Interactive
cially around rewrites, side goals, and program-                Theorem Proving, volume 7406 of Lecture Notes in
logic tactics. This suggests that visual compiler               Computer Science, pages 11–27. Springer.
should continue to expose proof structure, while
the decoder and verification loop should become               Gilles Barthe, Benjamin Grégoire, Sylvain Heraud, and
                                                                Santiago Zanella Béguelin. 2011. Computer-aided
more precise at converting that structure into lo-              security proofs for the working cryptographer. In
cally valid EasyCrypt steps. Extending verifier-                Advances in Cryptology – CRYPTO 2011, volume
guided revision at this final boundary is likely to             6841 of Lecture Notes in Computer Science, pages
improve proof completion without changing the                   71–90. Springer.
deterministic visual construction.                            Gilles Barthe, Benjamin Grégoire, and Santiago
                                                                Zanella Béguelin. 2009. Formal certification of code-
7     Conclusion                                                based cryptographic proofs. In Proceedings of the
                                                                36th Annual ACM SIGPLAN-SIGACT Symposium
This paper presents Scratchy, a visual-scratchpad               on Principles of Programming Languages, pages 90–
framework for machine-checkable cryptographic                   101. ACM.
proof generation. Scratchy deterministically com-             Yihe Deng, Chenchen Ye, Zijie Huang, Mingyu Derek
piles a Structured Natural-Language Proof Sketch                Ma, Yiwen Kou, and Wei Wang. 2024. GraphVis:


                                                          9
  Boosting LLMs with visual knowledge graph integra-            Azim Ospanov, Farzan Farnia, and Roozbeh Mohit.
  tion. In Advances in Neural Information Processing              2025. APOLLO: Automated LLM and lean collabo-
  Systems, volume 37, pages 67511–67534. Curran As-               ration for advanced formal reasoning. In Advances in
  sociates, Inc.                                                  Neural Information Processing Systems, volume 38,
                                                                  pages 41599–41633. Curran Associates, Inc.
Kefan Dong and Tengyu Ma. 2025. STP: Self-play
  LLM theorem provers with iterative conjecturing and           Ji Qi, Ming Ding, Weihan Wang, Yushi Bai, Qingsong
  proving. In Proceedings of the 42nd International                Lv, Wenyi Hong, Xu Bin, Lei Hou, Juanzi Li, Yuxiao
  Conference on Machine Learning, volume 267 of                    Dong, and Jie Tang. 2025. CogCoM: A visual lan-
  Proceedings of Machine Learning Research, pages                  guage model with chain-of-manipulations reasoning.
  14114–14136. PMLR.                                               In International Conference on Learning Representa-
EasyCrypt Development Team. 2026. EasyCrypt:                       tions, pages 11090–11110.
  Computer-aided cryptographic proofs. GitHub repos-
  itory.                                                        Hao Shao, Shengju Qian, Han Xiao, Guanglu Song,
                                                                  Zhuofan Zong, Letian Wang, Yu Liu, and Hong-
Yushi Hu, Weijia Shi, Xingyu Fu, Dan Roth, Mari Os-               sheng Li. 2024. Visual CoT: Advancing multi-modal
  tendorf, Luke Zettlemoyer, Noah A. Smith, and Ran-              language models with a comprehensive dataset and
  jay Krishna. 2024. Visual sketchpad: Sketching as a             benchmark for chain-of-thought reasoning. In Ad-
  visual chain of thought for multimodal language mod-            vances in Neural Information Processing Systems,
  els. In Advances in Neural Information Processing               volume 37, pages 8612–8642. Curran Associates,
  Systems, volume 37, pages 139348–139379. Curran                 Inc.
  Associates, Inc.
                                                                George Tsoukalas, Jasper Lee, John Jennings, Jimmy
Zhaoxuan Li, Qionglu Zhang, Hengyuan Liu, Xiaoyan                 Xin, Michelle Ding, Michael Jennings, Amitayush
  Gu, Xianhui Lu, Hongbo Liu, Bingzheng Wang, Hai-                Thakur, and Swarat Chaudhuri. 2024. PutnamBench:
  hui Fan, Ziming Zhao, Rui Zhang, and Li Zhou. 2026.             Evaluating neural theorem-provers on the putnam
  CrypFormBench: Benchmarking formal analysis ca-                 mathematical competition. In Advances in Neural
  pability of large language models for cryptographic             Information Processing Systems, volume 37, pages
  schemes. Proceedings of the ACM on Software Engi-               11545–11569. Curran Associates, Inc.
  neering, 3(FSE).
Haohan Lin, Zhiqing Sun, Sean Welleck, and Yiming               Zichen Wang, Anjie Dong, and Zaiwen Wen. 2025.
  Yang. 2025. Lean-STaR: Learning to interleave think-            Tree-based premise selection for Lean4. In Ad-
  ing and proving. In International Conference on                 vances in Neural Information Processing Systems,
  Learning Representations, pages 66041–66062.                    volume 38, pages 32621–32655. Curran Associates,
                                                                  Inc.
Xiaohan Lin, Qingxing Cao, Yinya Huang, Haiming
  Wang, Jianqiao Lu, Zhengying Liu, Linqi Song, and             Yanbin Wei, Shuai Fu, Weisen Jiang, Zejian Zhang,
  Xiaodan Liang. 2024. FVEL: Interactive formal veri-             Zhixiong Zeng, Qi Wu, James T. Kwok, and
  fication environment with large language models via             Yu Zhang. 2024. GITA: Graph to visual and tex-
  theorem proving. In Advances in Neural Information              tual integration for vision-language graph reasoning.
  Processing Systems, volume 37, pages 54932–54946.               In Advances in Neural Information Processing Sys-
  Curran Associates, Inc.                                         tems, volume 37, pages 44–72. Curran Associates,
                                                                  Inc.
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-
  Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng,                 Wenshan Wu, Shaoguang Mao, Yadong Zhang, Yan
  Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing           Xia, Li Dong, Lei Cui, and Furu Wei. 2024. Mind’s
  Lu, David Acuna, Kaiyu Yang, Hongzhou Lin, Yejin               eye of LLMs: Visualization-of-thought elicits spatial
  Choi, Danqi Chen, Sanjeev Arora, and Chi Jin. 2026.            reasoning in large language models. In Advances in
  Goedel-Prover-V2: Scaling formal theorem proving               Neural Information Processing Systems, volume 37,
  with scaffolded data synthesis and self-correction. In         pages 90277–90317. Curran Associates, Inc.
  International Conference on Learning Representa-
  tions, pages 11793–11818.                                     Ziyang Xiao, Dongxiang Zhang, Xiongwei Han, Xiao-
Yiping Ma, Yu-Lin Tsai, Mayank Rathee, Deevashwer                 jin Fu, Wing Yin Yu, Tao Zhong, Sai Wu, Yuan Wang,
  Rathee, François Dupressoir, Pierre-Yves Strub, and             Jianwei Yin, and Gang Chen. 2024. Enhancing LLM
  Raluca Ada Popa. 2026. ShannonProver: Towards                   reasoning via vision-augmented prompting. In Ad-
  automating formal cryptographic proofs. Preprint,               vances in Neural Information Processing Systems,
  arXiv:2607.02847. ArXiv preprint.                               volume 37, pages 28772–28797. Curran Associates,
                                                                  Inc.
Logan Murphy, Kaiyu Yang, Jialiang Sun, Zhaoyu Li,
  Anima Anandkumar, and Xujie Si. 2024. Autofor-                Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao,
  malizing euclidean geometry. In Proceedings of the              Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
  41st International Conference on Machine Learning,              Xuan Lu, Qiushi Du, Wenjun Gao, Haowei Zhang,
  volume 235 of Proceedings of Machine Learning                   Qihao Zhu, Dejian Yang, Zhibin Gou, Z. F. Wu, Fuli
  Research, pages 36847–36893. PMLR.                              Luo, and Chong Ruan. 2025. DeepSeek-Prover-V1.5:


                                                           10
    Harnessing proof assistant feedback for reinforce-          require import Real Distr.
    ment learning and monte-carlo tree search. In Inter-
    national Conference on Learning Representations,            type t.

    pages 72274–72303.                                          op sample: t distr.
                                                                axiom sample_ll: is_lossless sample.
Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang,
                                                                op test: t -> bool.
  Dahua Lin, and Kai Chen. 2024. Lean workbook: A               axiom pr_ntest: 0%r < mu sample (predC test).
  large-scale Lean problem set formalized from natural
  language math problems. In Advances in Neural                 module Sample = {
                                                                  proc sample () : t = {
  Information Processing Systems, volume 37, pages                  var r : t;
  105848–105863. Curran Associates, Inc.
                                                                         r <$ sample;
                                                                         while (test r) {
Yiyang Zhou, Haoqin Tu, Zijun Wang, Zeyu Wang,                             r <$ sample;
  Niklas Muennighoff, Fan Nie, Chaorui Deng, Shen                        }
  Yan, Haoqi Fan, Yejin Choi, James Zou, Cihang Xie,                     return r;
                                                                     }
  Huaxiu Yao, and Qinghao Ye. 2026. When visualiz-              }.
  ing is the first step to reasoning: MIRA, a benchmark
  for visual chain-of-thought. In Proceedings of the            lemma Sample_lossless: islossless Sample.sample.
                                                                proof.
  IEEE/CVF Conference on Computer Vision and Pat-               proc; seq 1: true=> //.
  tern Recognition, pages 26154–26164.                          + by auto=> />; exact/sample_ll.
                                                                while true (if test r then 1 else 0) 1 (mu sample (predC test)
                                                                      )=> //.
A     Scratchy-eval Data Card                                   + by move=> _ r; case: (test r).
                                                                + move=> ih; seq 1: true=> //.
Scratchy-eval is designed to compare how alter-                   by auto; rewrite sample_ll.
                                                                + by auto; rewrite sample_ll.
native representations of proof relations affect                rewrite pr_ntest=> /= z; conseq (: true ==> !test r).
                                                                + smt().
machine-checkable EasyCrypt generation. It also                 by rnd; auto=> />.
                                                                qed.
includes compact diagnostic tasks for static valid-
ity and semantic recognition. The intended unit of              Listing 3: Complete official EasyCrypt source
comparison is a fixed model, task pair evaluated                underlying Scratchy-eval Task 003. The task removes
under the same response contract and verifier.                  the proof body of Sample_lossless while preserving
   This dataset contains 114 tasks, including 64                the surrounding file as its compilation context.
free-form proof-generation targets and 50 multiple-
choice diagnostics. The source material spans 26
protocol or formal-program groups. Table 5 reports              for fixture preflight and analysis, but is not shown
category-level coverage; task-level source pointers             to the model. The multiple-choice portion asks
are retained in the accompanying metadata.                      either whether a local EasyCrypt form is valid or
                                                                which formal role a construct serves. All answers
A.1    Representative datum                                     are checked against the pinned source or compiler
Task 003 is drawn from the official while-sampling              behavior.
example in the foundations family. Its source is
sufficiently compact to reproduce in full. Listing 3            A.2         Representations and scoring
includes the complete pinned file: imports, declara-            Each task supports three textual conditions and
tions, probabilistic program, target, and accepted              three graph conditions. The professional graph
proof. To construct the generation task, only the               presents typed proof objects, local formulas, di-
body of Sample_lossless is replaced by a proof                  rected dependencies, and a route to the target; the
hole.                                                           remaining conditions remove relation detail or alter
   The generation contract asks for the missing                 visual structure. Generation is scored by EasyCrypt
proof body rather than the surrounding declara-                 acceptance after source reconstruction, while the
tion. Listing 4 gives the complete canonical output             diagnostic tasks use answer accuracy. This sepa-
for Task 003. This fragment reconstructs the offi-              rates executable proof completion from recognition
cial source above and is accepted by EasyCrypt; a               of formal knowledge.
textually different response is also correct when it               The release record retains source provenance,
closes the same target under the verifier.                      task type, target information, graph metadata,
   For generation, a declaration is selected from its           supported conditions, and verification artifacts.
source and the required imports, definitions, and               Scratchy-eval is intended for controlled representa-
dependency prefix are preserved while the official              tion studies over the included EasyCrypt material.
proof is replaced. The hidden fragment is used                  Its category-level coverage is broader than the mo-

                                                           11
Table 5: Category-level coverage of Scratchy-eval. Representative material and proof emphasis are summarized
without enumerating task IDs or hidden fragments. The generation counts sum to 64; static-validity and semantic-
recognition diagnostics accompany all seven families.

  Source family             Representative material                     Proof emphasis               Judgments     Gen.
   Foundations          Recursion; distributions; sampling         Termination and probability      lemma/equiv     10
  Program logics           Relational while programs                 Coupling and invariants            lemma       2
  Simple crypto           Pedersen; Schnorr; ElGamal              Correctness and basic security        lemma       7
 Complex crypto                PIR; stateful PRG                   Relational privacy and state      lemma/equiv    9
 Reduction paths              Up-to; plug-and-pray                Game transitions and bounds           lemma        7
 Extended crypto         AE; UC/CCA; hashed ElGamal              Composed and oracle reductions     lemma/equiv     23
 Program analysis        Adversary bounds; Quickselect           Expectations and data invariants   lemma/ehoare     6



proc; seq 1: true=> //.
+ by auto=> />; exact/sample_ll.
while true (if test r then 1 else 0) 1 (mu sample (predC test)
      )=> //.
+ by move=> _ r; case: (test r).
+ move=> ih; seq 1: true=> //.
  by auto; rewrite sample_ll.
+ by auto; rewrite sample_ll.
rewrite pr_ntest=> /= z; conseq (: true ==> !test r).
+ smt().
by rnd; auto=> />.

Listing 4: Complete accepted output for Scratchy-eval
Task 003. This canonical fragment is taken from the
official answer record and contains exactly the code
required at the proof hole.



tivating Observation, while remaining a focused
benchmark rather than a census of cryptographic
formalization.




                                                                 12
