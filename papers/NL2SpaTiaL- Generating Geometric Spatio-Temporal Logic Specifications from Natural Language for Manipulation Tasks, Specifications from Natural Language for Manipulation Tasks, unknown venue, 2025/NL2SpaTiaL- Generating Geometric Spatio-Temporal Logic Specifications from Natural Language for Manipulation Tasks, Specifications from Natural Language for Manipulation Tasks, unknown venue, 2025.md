                                                       NL2SpaTiaL: Generating Geometric Spatio-Temporal Logic
                                                      Specifications from Natural Language for Manipulation Tasks
                                                                                    Licheng Luo, Kaier Liang, Yu Xia, Mingyu Cai


                                             Abstract— While Temporal Logic provides a rigorous ver-                                                                Detailed Plan                       Safe
                                         ification framework for robotics, it typically operates on                                                                                                  Deployment
                                         trajectory-level signals and does not natively represent the                                                           Nested Logical Tree
                                         object-centric geometric relations that are central to manip-
                                         ulation. Spatio-Temporal Logic (SpaTiaL) overcomes this by
                                         explicitly capturing geometric spatial requirements, making it
arXiv:2512.13670v2 [cs.RO] 24 Mar 2026




                                         a natural formalism for manipulation-task verification. Con-                     “Pick up the black bowl
                                         sequently, translating natural language (NL) into verifiable                     on the cookie box and                         SpaTiaL
                                                                                                                          place it on the plate”
                                         SpaTiaL specifications is a critical objective. Yet, existing                                                                    Formal Verification

                                         NL-to-Logic methods treat specifications as flat sequences,
                                         entangling nested temporal scopes with spatial relations and
                                         causing performance to degrade sharply under deep nesting.                        VLA         Diffusion Model

                                         We propose NL2SpaTiaL, a framework modeling specifications                                                        Different
                                                                                                                                                          Generated
                                         as Hierarchical Logical Trees (HLT). By generating formulas                                                     Trajectories
                                                                                                                         Planning          RL Policy                     Robustness = -0.304    Robustness = +0.012
                                         as structured HLTs in a single shot, our approach decou-
                                         ples semantic parsing from syntactic rendering, aligning with
                                         human compositional spatial reasoning. To support this, we                  Fig. 1: NL2SpaTiaL enables an interpretable generate-
                                         construct, to the best of our knowledge, the first NL-to-                   and-test pipeline: The generated specifications act as exe-
                                         SpaTiaL dataset with explicit hierarchical supervision via a                cutable geometric constraints to verify candidate trajectories
                                         logic-first synthesis pipeline. Experiments with open-weight
                                         LLMs demonstrate that our HLT formulation significantly
                                                                                                                     from black-box models (e.g., VLAs). Our primary contribu-
                                         outperforms flat-generation baselines across various logical                tion is the scalable symbolic translation framework, rather
                                         depths. These results show that explicit HLT structure is critical          than the downstream control policies.
                                         for scalable NL-to-SpaTiaL translation, ultimately enabling a
                                         rigorous “generate-and-test” paradigm for verifying candidate               reasoning over continuous geometric relations (e.g., Above,
                                         trajectories in language-conditioned robotics. Project website:             EnclIn, CloseE) and their temporal evolution [9], [10].
                                         https://sites.google.com/view/nl2spatial                                    Because it explicitly captures these requirements, SpaTiaL
                                                                    I. I NTRODUCTION                                 serves as a highly natural formalism for verifying complex
                                                                                                                     manipulation. As illustrated in Fig. 1, deriving executable
                                            Grounding natural language (NL) instructions into struc-
                                                                                                                     SpaTiaL specifications from natural language unlocks an
                                         tured spatial reasoning remains a central challenge for
                                                                                                                     interpretable verification layer for modern generate-and-test
                                         language-conditioned robotics [1]. Although large language
                                                                                                                     pipelines, effectively filtering unsafe trajectories proposed by
                                         models (LLMs) exhibit impressive linguistic reasoning, they
                                                                                                                     unconstrained generative models, such as vision-language-
                                         often struggle to represent the precise geometric structures
                                                                                                                     action (VLA) models [2].
                                         and temporal dependencies required for complex manip-
                                                                                                                        However, reliably translating unconstrained natural lan-
                                         ulation [2], [3]. Consequently, language-based agents fre-
                                                                                                                     guage into formal SpaTiaL specifications remains a funda-
                                         quently generate actions that appear semantically plausible
                                                                                                                     mental bottleneck. Existing methods typically map text to
                                         but violate rigid spatio-temporal constraints. This reflects
                                                                                                                     a flat logical string [6]–[8]. This flat formulation creates a
                                         a fundamental mismatch between the unconstrained nature
                                                                                                                     scalability bottleneck: by coupling high-level logical routing
                                         of NL and the formal specifications required for rigorous
                                                                                                                     with low-level syntactic realization, e.g., bracket matching,
                                         downstream reasoning, control, and, most importantly, task
                                                                                                                     it makes LLMs highly prone to syntax errors and fails
                                         verification [1]. Temporal Logic (TL) has long provided a
                                                                                                                     to preserve the natural compositional hierarchy inherent in
                                         rigorous mathematical framework for verifying robotic task
                                                                                                                     human manipulation instructions [11]–[14].
                                         execution [4], [5], driving recent efforts in NL-to-TL trans-
                                                                                                                        To address this limitation, we propose NL2SpaTiaL, a
                                         lation [6]–[8]. However, standard TL evaluates only robot
                                                                                                                     framework that separates semantic parsing from syntactic
                                         trajectories, inherently ignoring the object-level interactions
                                                                                                                     rendering. Rather than generating executable logic directly,
                                         crucial for manipulation. Spatio-Temporal Logic (SpaTiaL)
                                                                                                                     the model first predicts a Hierarchical Logical Tree (HLT) as
                                         overcomes this limitation by enabling explicit symbolic
                                                                                                                     a structured JSON representation that captures the composi-
                                              Licheng Luo, Yu Xia and Mingyu Cai are with University                 tional structure of the instruction. A deterministic renderer
                                         of      California, Riverside, USA. {lichengl, yxia072,                     then converts the validated HLT into executable SpaTiaL
                                         mingyuc}@ucr.edu
                                              Kaier   Liang   is   with   Lehigh   University,   Bethlehem,   USA.   formulas, guaranteeing syntactic correctness by construction
                                         {kal221}@lehigh.edu                                                         while preserving semantic meaning. To mitigate data scarcity
in formal-methods applications, we further develop a scalable      Spatial Reasoning and Grounding. Complementary to TL
logic-first synthesis pipeline. Instead of relying on manual       translation, spatial reasoning research studies how linguistic
annotation, the pipeline samples valid HLT structures, deter-      expressions can be grounded into symbolic or geometric
ministically generates canonical instructions, and leverages       structure. Prior work on Spatial Role Labeling and ISO-
LLMs for diverse paraphrasing. Although instantiated for the       Space maps text to structured spatial representations [23],
NL2SpaTiaL dataset, this abstract syntax tree (AST)–driven         [24], while neuro-symbolic approaches generate executable
paradigm is logic-agnostic and readily extends to other            programs and demonstrate compositional reasoning in visu-
compositional formalisms, including LTL [15], STL [16],            ally grounded settings [13], [14], [25], [26]. Our work ex-
and task-level robotic specifications.                             tends this line by coupling geometric spatial predicates with
Contributions. Our primary contributions are:                      temporal operators in a unified translation target. Although
   leftmargin=*, itemsep=0pt, topsep=0pt, parsep=0pt, par-         our empirical focus is SpaTiaL for robotic manipulation, the
topsep=0pt                                                         HLT formulation and one-shot hierarchical generation inter-
   • A Hierarchical Translation Framework: We intro-               face are structurally compatible with other temporal-logic
      duce NL2SpaTiaL, which bypasses the conventional flat        families (e.g., STL/LTL) when paired with an appropriate
      sequence-mapping bottleneck. By predicting structured        deterministic renderer.
      logical trees, it provides a strong inductive bias that                              III. BACKGROUND
      dramatically improves reasoning robustness under deep
      spatio-temporal nesting.                                       This section briefly reviews STL [16] and SpaTiaL [9],
   • A Universal Logic-First Data Engine: We formu-
                                                                   which provide the formal foundation for NL2SpaTiaL.
      late a logic-first synthesis paradigm that guarantees        A. Signal Temporal Logic
      the structural and logical correctness of the generated
                                                                     We consider discrete-time signals s = [s[0], . . . , s[ℓ − 1]]
      supervision signal while preserving linguistic diversity.
                                                                   with s[t] ∈ Rd . STL formulas specify temporal properties
      Utilizing this engine, we release the first hierarchically
                                                                   over such signals. Let µ := a⊤ s ≥ b denote an atomic
      supervised NL-to-SpaTiaL benchmark, empirically ex-
                                                                   predicate. The STL syntax is given by
      posing the sharp degradation of prior flat-generation
      methods as task complexity scales.                            φ ::= µ | ¬φ | φ1 ∧ φ2 | φ1 ∨ φ2 | F[a,b] φ | G[a,b] φ | φ1 U[a,b] φ2
   • Extreme Sample Efficiency & Downstream Deploy-                                                                                   (1)
      ment: Extensive experiments on open-weight LLMs              where [a, b] specifies the temporal evaluation window. F, G,
      (3.8B–14B) demonstrate that our HLT formulation              and U represent the eventually, always, and until operators,
      achieves superior accuracy with minimal data—models          respectively.
      trained on just 600 examples outperform flat baselines          The quantitative semantics (robustness) r(s, φ ,t) ∈ R as-
      using 5× more data. We validate its practical utility by     signs a signed satisfaction margin to a formula: r(s, φ ,t) > 0
      deploying the generated formulas as executable safety        indicates satisfaction at time t, while r(s, φ ,t) < 0 indicates
      verifiers to filter candidate trajectories in language-      violation. For an atomic predicate, r(s, µ,t) = a⊤ s[t] − b.
      conditioned generative policies e.g., VLAs.                  Boolean and temporal operators are then lifted through
                                                                   min/max compositions, e.g.,
                    II. R ELATED W ORK
                                                                                                                            
Natural Language to Temporal Logic. Translating nat-                         r(s, φ1 ∧ φ2 ,t) = min r(s, φ1 ,t), r(s, φ2 ,t) ,         (2)
ural language (NL) into temporal logic (TL) has evolved                       r(s, G[a,b] φ ,t) =      min r(s, φ ,t ′ ),             (3)
                                                                                                    t ′ ∈t+[a:b]
from rule-based systems [6], [17] to modular pipelines
with intermediate representations and decomposition strate-        with other operators derived analogously [16].
gies [7], [18]. More recently, LLM-based approaches have
                                                                   B. Spatial Temporal Logic
been applied to TL translation in multiple domains, including
domain-transferable translation [8], traffic and planning ap-          While STL applies to generic real-valued signals, Spa-
plications [19], [20], retrieval-augmented formulations [21],      TiaL [9] introduces geometric atomic predicates tailored to
and grammar-constrained decoding [12]. Interactive systems         2D/3D physical workspaces. At each time t, the state may
such as NL2Spec [11] and SYNTHTL [22] further improve              include object poses and geometric attributes (e.g., centers,
reliability through decomposition, verification, and iterative     extents/radii, and orientations). SpaTiaL atoms evaluate con-
refinement. Our work differs along three axes. First, we target    tinuous geometric relations such as distance, containment,
SpaTiaL specifications for continuous geometric manipula-          and directional alignment.
tion constraints rather than primarily discrete TL settings.           To provide quantitative semantics compatible with STL
Second, we study one-shot hierarchical generation (nested          monitoring, SpaTiaL defines a continuous robustness score
JSON HLT) rather than multi-step interactive decomposition         ρ for each spatial predicate. For illustration, consider the
at inference time. Third, we pair this formulation with su-        following representative predicates defined for objects i and
pervised fine-tuning on a logic-first synthesized dataset with      j: leftmargin=*, noitemsep, topsep=0pt
explicit subformula-level supervision, enabling controlled             • Distance (closeToε ): Evaluates if two objects are within
analysis of complexity scaling and sample efficiency.                     a threshold εc . ρ(closeToε (i, j)) = εc − ∥pi − p j ∥
  • Containment (enclIn): Evaluates if object i lies strictly         ciated robustness signal quantifies their satisfaction margins
    inside j with a margin δ . ρ(enclIn(i, j)) = (r j − δ ) −         over time. This example highlights why accurate NL-to-
    (∥pi − p j ∥ + ri )                                               SpaTiaL translation is valuable for downstream monitoring,
  • Directional (LeftOf): Evaluates if i is to the left of j          verification, and control-oriented evaluation.
    with a separation margin κ. ρ(LeftOf(i, j)) = (x j −r j )−
    (xi + ri + κ)                                                                   IV. NL2S PAT IA L F RAMEWORK
                                                                         The fundamental challenge in translating natural language
                                          Alignment
                                                                      instructions x ∈ X into Spatio-Temporal Logic specifications
           First, center the
           screw with the hole.                                       φ ∈ Φ is the structural mismatch between unconstrained
           Then, push it straight
           in until the tip                                           linguistic syntax and rigid formal logic. Standard sequence-
           enters and the screw
           is fully seated.
                                                                      to-sequence formulations learn a direct mapping P(φ | x),
                                                 Insertion
                                                                      which couples high-level semantic composition (e.g., tem-
                                                                      poral routing and object grounding) with low-level syntactic
                                                                      realization (e.g., bracketing and operator formatting).
                                                                         To address this mismatch, we introduce NL2SpaTiaL,
                                                                      which explicitly decouples semantics from syntax. We rep-
                                                                      resent the target specification as a hierarchical logical tree
                                                                      (HLT) and use a two-stage inference process: (i) a neu-
Fig. 2: SpaTiaL grounding example. A natural-language                 ral semantic parsing stage that predicts the discrete tree
instruction is mapped to a hierarchical SpaTiaL specification         structure, and (ii) a deterministic rendering stage that maps
and evaluated through continuous robustness ρ(t) during               the validated tree to a syntactically well-formed SpaTiaL
execution.                                                            formula.
   Other complex predicates, including boundary contact
(Touch), partial overlap (partOvlp), and axis-aligned be-             A. HLT Representation
tweenness (Between), follow analogous geometric construc-                SpaTiaL specifications are compositional: quantitative spa-
tions based on signed clearances and directional projections.         tial predicates are nested under Boolean and temporal oper-
We refer readers to [9] for the complete catalog of spatial           ators. To preserve this topology explicitly during generation,
atoms and their exact quantitative semantics. Once these geo-         we represent the target as a hierarchical logical tree (HLT).
metric predicates are composed through the STL operators in              Definition 1 (Hierarchical Logical Tree): Let Otemp =
Eq. (1), they induce a trajectory-level robustness measure that       {G, F,U} be temporal operators, Obool = {∧, ∨, ¬, →}
evaluates not only whether a manipulation task is satisfied,          be Boolean operators, and P be the set of atomic
but also how strongly it is satisfied or violated over time.          spatial predicates. An HLT is a directed rooted tree
   Formally, let ξ = {x0 , x1 , . . . , xT }, with xt ∈ Rn , denote   T = (Vint ,Vleaf , E, op, intv, args), where Vint and Vleaf
a generated manipulation trajectory over a horizon T ,                are disjoint sets of internal and leaf nodes, and
where each state encodes the robot configuration together             E ⊂ Vint × (Vint ∪Vleaf ) defines parent-child scope relations.
with all task-relevant objects in the workspace. Let O =                 Each node has a label op(·): for v ∈ Vint , op(v) ∈ Otemp ∪
{o1 , o2 , . . . , om } be the set of objects involved in the task,   Obool ; for v ∈ Vleaf , op(v) ∈ P. Temporal nodes may addition-
and let the pose of object oi at time t be extracted from             ally carry an interval intv(v) = [a, b] with a, b ∈ R≥0 . Each
the system state through a mapping pi (t) = hi (xt ) ∈ SE(3).         leaf node carries predicate arguments args(v) ∈ Ωk , where Ω
A manipulation task is specified by a SpaTiaL formula φ ,            denotes the universe of physical entities.
whose atomic predicates take the form µk pi1 (t), . . . , pir (t) :      This decomposition separates global logical routing (inter-
SE(3)r → R and encode geometric relations among objects               nal nodes) from local geometric grounding (leaf nodes). As
and the environment, such as distance constraints, contain-           a result, the HLT introduces a structural inductive bias that
ment, alignment, and collision avoidance. Evaluating the              better matches the compositional organization of manipula-
pose sequence induced by ξ against φ yields the robustness            tion instructions than flat sequence targets.
value ρ(ξ , φ , 0), which summarizes the satisfaction margin
of the entire execution. In this way, SpaTiaL provides a              B. Inference Pipeline: Decoupling Semantics from Syntax
unified task-level signal for continuously monitoring object–            In flat generation, the model autoregressively emits the
object and object–environment interactions, and, when em-             full specification as a 1D token sequence. As the depth
bedded in a differentiable pipeline, for guiding optimization         of T increases, errors in scope management and operator
toward behavior that better satisfies the intended manipula-          composition become more likely, since semantic decisions
tion objective.                                                       and syntax formatting are interleaved in the same decoding
Example. Fig. 2 illustrates how a natural-language instruc-           stream. We therefore decouple generation into a semantic
tion can be mapped to a hierarchical SpaTiaL specification            parsing stage and a deterministic syntax projection stage.
and then evaluated through robustness during execution. The              1. Probabilistic Semantic Parsing (Tree Generation):
resulting predicates encode explicit geometric constraints,           Instead of directly predicting the flat string φ , we train a
such as alignment, proximity, and placement, while the asso-          Large Language Model parameterized by θ as a structural
        Root            Ensure the workspace is correctly organized by first placing the red block inside the sorting
   Natural Language
                        zone within [0,10] and then arranging the overall configuration so that the blue block is
         Input          positioned to its left within [10,20] while both blocks remain safely away from the obstacle.

       Layer 1          Place the red block inside the                              Arrange the overall configuration so that the blue block is
      Semantic          sorting zone as part of organizing                      ∧ positioned to the left of the red block and both blocks remain
    Segmentation        the workspace.                                              safely away from the obstacle.

      Layer 2            The red block must be                       The blue block must be positioned                    Both blocks mus t re ma i n a t a
   Fine-Grained          inside the sorting zone.                    to the left of the red block.                  ∧ safe distance from the obstacle.
   Decomposition

      Layer N
       Further                                                 . . . . . . More decomposition layers if needed . . . . . .
    Decomposition

     Primitives          Inside(red, SortingZone)                           LeftOf(blue, red)         FarFrom(red, Obstacle)           FarFrom(blue, Obstacle)

     Outcome                   F[0,10] Inside(red, SortingZone)∧ F[10,20] LeftOf(blue, red)∧ G(farFrom(red, Obstacle) ∧ farFrom(blue, Obstacle))

Fig. 3: An illustrative example of the HLT representation. Instead of mapping natural language directly to a flat sequence
(Outcome), NL2SpaTiaL explicitly models the semantic topology through hierarchical layers. Internal nodes dictate temporal
and Boolean routing, while leaf nodes ground the geometric primitives. During inference, the LLM predicts this entire nested
structure in a single shot, effectively decoupling semantic reasoning from syntactic formatting.

parser that outputs a nested JSON representation fθ : X →                             During dataset construction, we store a rich layer-based HLT
TJSON . By constraining the target to a nested data structure,                        representation that includes auxiliary canonical texts and
generation follows a top-down compositional process: the                              subformula metadata for synthesis and analysis. For model
model first emits an internal operator node (and its interval                         training, this representation is deterministically converted
when applicable), then recursively expands its children. This                         into a compact nested JSON tree that retains only the logical
representation reduces ambiguity between temporal meta-                               topology (operators, intervals, predicates, and arguments)
data (e.g., intervals) and leaf-level predicate arguments, and                        required for exact structural generation.
makes logical scope explicit in the output format.                                       During training, the model is optimized with standard au-
   2. Deterministic Recursive Rendering: After TJSON is                               toregressive next-token prediction to map a natural-language
generated, a lightweight structural validator checks format                           instruction to the corresponding nested JSON string. A
and logical consistency (e.g., operator arity, required intervals                     system prompt Psys specifies the output schema and operator
for temporal operators, and interval validity a ≤ b). The                             constraints, thereby restricting the model to a structured
validated tree is then mapped to a SpaTiaL string by a                                SpaTiaL-compatible output space. An example prompt tem-
deterministic projection Π : T → Φ via recursive traversal:                           plate and target output are shown below.
                              
           
            op(v)     args(v)  ,              v ∈ Vleaf ,                              System prompt:
                                                                                      You are a semantic parser for Spatio-Temporal Logic. Output a HLT as a single
           op(v) Π(vc ) ,                    op(v) = ¬,
           
                                                                                        nested JSON.
           
           
                                                                                        Format: Internal node: {"op": "<op>", "interval": [a,b],
 Π(v) = op(v)intv(v) Π(vc ) ,                  op(v) ∈ {G, F},                          "children": [...]}; Leaf node: {"predicate": "<name>",
                                                                                        "args": [...] }.
           
                     ) op(v)                ), op(v)  = U,
           
           
           
            Π(v  c1         intv(v) Π(v c2                                             Constraints: Temporal operators require explicit intervals. Arity bounds:
           
           (Π(v ) op(v) Π(v ) . . . ) , op(v) ∈ {∧, ∨, →}.                             G/F/Not(=1 child), U/Implies(=2), And/Or(≥2). Output ONLY valid JSON.
                   c1                c2
                                                               (4)
Here, vc denotes the (ordered) child of a unary operator, and                           User prompt:
                                                                                        Ensure the red block stays above the blue block and touches the green block
vc1 , vc2 denote the ordered children of a binary operator. This                        throughout time steps 5 to 20.
decoupled architecture isolates responsibilities: the neural                            Assistant (Target TJSON ):
                                                                                        {"op": "G", "interval": [5, 20], "children": [
model fθ resolves linguistic ambiguity and predicts structure,                          {"op": "And", "children": [
while the deterministic projection Π renders syntax. Conse-                             {"predicate": "Above", "args": ["obj r", "obj b"]},
                                                                                        {"predicate": "Touch", "args": ["obj r", "obj g"]}
quently, any HLT that passes structural validation yields a                             ]} ]}
syntactically well-formed SpaTiaL formula by construction.
                                                                                         By applying SFT directly to the structured JSON target,
 Example (NL → Nested Tree → Formula).                                                the training objective naturally penalizes topological viola-
 NL: “Between time 0 and 10, the red block is always left of the blue block.”
 Nested Tree:                                                                         tions (e.g., closing a dictionary prematurely or misplacing
 {"op":"G","interval":[0,10],"children":[                                             the "children" key). During inference, the generated
 {"predicate":"LeftOf","args":["obj              r","obj b"]}]}
                                                                                      JSON string is parsed, validated, and directly mapped to the
                                         
 Formula:φ = G[0,10] LeftOf(obj r, obj b)
                                                                                      final flat formula via deterministic rules (i.e., TJSON → Φ)
   To align base LLMs (e.g., Llama-3-8B) with our hi-                                 without requiring step-by-step intermediate translations. To
erarchical generation paradigm, we formulate training as                              systematically construct the hierarchical data pairs required
supervised fine-tuning (SFT) on serialized nested-tree targets.                       for this training, we detail our logic-first synthesis pipeline
in the following section.                                                                             unique canonical realization, which avoids ambiguity during
                                                                                                      supervision generation.
             V. H IERARCHICAL DATA PAIR G ENERATION
                                                                                                         Linguistic diversification. To reduce template bias and
                                            Root           Text
                                                                                                      improve robustness to natural-language variation, we gener-
                          Formula 1       Text       Formula 2         Text
                                                                                                      ate paraphrased variants of each canonical description. For
                                                                                                      a node φi with canonical text τ(φi ), we sample variants
Predefined     Subformula1.1   Text       Subformula2.1           Text . . .   Subformula2.n   Text
Maximum                                                                                               ν ∼ pLLM (· | τ(φi ), φi ), where the exact formula φi is included
 Depth D
                                                   Predefined Maximum Breadth B
                                                                                                      as conditioning context to preserve semantic fidelity. This
                          . . . . . . More decomposition layers. . . . . .
                                                                                                      yields stylistically diverse yet logic-consistent descriptions
                                                                                                      for both full formulas and subformulas.
Fig. 4: Hierarchical formula generation pipeline. We first                                               Dataset structure. For each sampled formula tree, the
specify structural complexity bounds (maximum depth D                                                 dataset stores a rich layer-based HLT representation, in-
and maximum breadth B), then sample concrete logical tree                                             cluding the root formula φ , its canonical description τ(φ ),
structures within these bounds. Leaf nodes are subsequently                                           paraphrases {νk (φ )}, and analogous tuples for internal nodes
instantiated with lifted spatial predicates, and the resulting                                        and leaves: {(φi , τ(φi ), {νk (φi )})}i . This yields dense super-
formula tree is back-translated in a deterministic manner,                                            vision at both the global instruction level and the subformula
so that each logical node is paired with a corresponding                                              level. For model training, the layer-based representation is
canonical text description.                                                                           deterministically converted to nested JSON targets, while
   To systematically train and evaluate NL2SpaTiaL under                                              the richer layer-based form remains useful for synthesis,
controlled logical complexity, we construct the dataset using                                         analysis, and future multi-level learning studies.
a logic-first synthesis pipeline. Each example is created by
first sampling a hierarchical SpaTiaL formula, then determin-                                                               VI. E XPERIMENTS
istically converting the formula tree into canonical natural                                             The primary objective of our experiments is to test whether
language, and finally generating linguistically diverse para-                                         explicit structural decomposition improves NL-to-SpaTiaL
phrases conditioned on the underlying logic. The pipeline                                             translation under increasing logical complexity. We compare
overview is shown in Fig. 4.                                                                          our HLT formulation against a flat generation baseline across
   Sampling hierarchical logical skeletons. We first sample                                           four axes: model scale, linguistic diversity, logical complex-
a rooted logical tree structure without instantiated spatial                                          ity, and training data composition. Our central hypothesis is
predicates. For each example, we choose a maximum depth                                               that flat generation becomes increasingly fragile under deep
D and assign each internal node a branching factor from a                                             nesting because semantic composition and syntax rendering
prescribed range, which determines the tree topology and                                              are entangled, whereas HLT alleviates this bottleneck through
the number of leaves L. Internal nodes are then labeled                                               an explicit hierarchical target structure.
with operators from O = {¬, ∧, ∨, G[a,b] , F[a,b] , U[a,b] }, with
temporal intervals [a, b] sampled from predefined ranges                                              A. Experimental Setup
subject to 0 ≤ a ≤ b. This yields a hierarchical logical                                                 Dataset Complexity Scaling. We evaluate on benchmark
skeleton whose topology and operator types are fixed while                                            sets generated by the logic-first synthesis pipeline (Sec. V),
leaves remain uninstantiated.                                                                         parameterized by maximum logical depth (D) and breadth
   Instantiating lifted spatial atoms. Given a skeleton                                               (B), ranging from D2 B4 (shallow constraints) to D4 B3
with L leaves, we instantiate each leaf with a lifted spa-                                            (deeply nested multi-stage goals). Each evaluation set con-
tial predicate sampled from geometry-aware templates (e.g.,                                           tains 150 instances constructed from 30 unique logical skele-
LeftOf(obji , obj j ), EnclIn(obji , regk )). We maintain a sym-                                      tons with 5 paraphrases per skeleton, enabling controlled
bolic universe U = {obj1 , . . . , objM , reg1 , . . . , regK } of object                             measurement of structural and linguistic generalization.
and region identifiers, and sample predicate arguments (and                                              Linguistic Diversity. To study robustness to language
any tolerance parameters) from predefined sets or ranges.                                             variation, we define an augmentation factor corresponding to
Because all identifiers are symbolic, the resulting formulas                                          the number of paraphrases per unique logical formula (Aug ∈
are scene-agnostic yet structurally interpretable. Substituting                                       {1, 3, 5, 15}). We also include a “Canonical” condition using
these atoms into the skeleton yields a complete hierarchical                                          deterministic templates only, which helps separate gains from
SpaTiaL formula φ .                                                                                   structural learning versus gains from linguistic diversity.
   Deterministic hierarchical back-translation. We then                                                  Model Scaling & Rigor. To assess whether model capac-
convert the formula tree into canonical natural-language                                              ity can substitute for structural guidance, we evaluate repre-
descriptions using a deterministic realization map τ(·) ap-                                           sentative open-weight models from 3.8B to 14B parameters
plied recursively from leaves to root. Spatial atoms are                                              (Phi-3.5-mini [27], Llama-3-8B [28], and Qwen-2.5-14B
rendered with fixed templates, temporal operators introduce                                           [29]). Fine-tuned models use an expanded context window
explicit time scopes, and Boolean operators determine clause                                          (2560 tokens) to reduce the risk of truncating deeply nested
composition. For every node φi in the tree, this process                                              HLT outputs. We report Correct Match (CM) as the primary
produces a canonical description τ(φi ). Because the mapping                                          metric. For zero-shot evaluation, we use greedy decoding
is grammar-driven and deterministic, each formula tree has a                                          (temperature = 0.0) for deterministic output generation. All
                                       TABLE I: Model Scaling: Fine-tuned Translation Accuracy (Aug=5)

                                           D2 B4 (Shallow)                                D3 B3 (Intermediate)                       D4 B3 (Deeply Nested)
   Model (Params)
                                    Flat (%)         HLT (%)               ∆         Flat (%)        HLT (%)           ∆         Flat (%)         HLT (%)           ∆
   Phi-3.5-mini (3.8B)              94.2 ± 0.8        95.8 ± 0.4          +1.6       63.1 ± 5.5       77.3 ± 3.2      +14.2      38.5 ± 2.4       56.1 ± 1.8     +17.6
   Llama-3 (8B)                     98.4 ± 0.6        97.9 ± 0.1          -0.5       82.6 ± 1.9       90.1 ± 0.6      +7.5       48.9 ± 3.2       70.4 ± 0.8     +21.5
   Qwen-2.5 (14B)                   97.7 ± 0.3        99.2 ± 0.1          +1.5       86.2 ± 0.7       92.6 ± 0.4      +6.4       58.7 ± 1.5       73.0 ± 0.8     +14.3


supervised results are averaged over 3 independent runs with                                D. Linguistic Diversity and Augmentation Scaling
different random seeds {0, 42, 123} to account for training
                                                                                              To analyze the effect of linguistic diversity, we fine-
variance. All supervised fine-tuning uses 4-bit quantized
                                                                                            tune Llama-3-8B under different augmentation factors and
LoRA adapters (QLoRA [30]), freezing the base model
                                                                                            compare Flat versus HLT across benchmark complexities.
weights and updating only low-rank adapter parameters for
memory-efficient training.
                                                                                            TABLE II: Llama-3-8B Translation Accuracy vs. Linguistic
                                                                                            Augmentation
B. Few-Shot Capability Analysis
                                                                                                                                     Augmentation Factor
   Before analyzing fine-tuned performance, we establish a                                    Dataset      Metric
frontier capability reference using GPT-5.2 in a few-shot (k =                                                          Aug = 1      Aug = 3      Aug = 5      Aug = 15
5) setting to characterize the intrinsic difficulty of NL-to-                                              Flat (%)     96.6 ± 0.4   97.6 ± 1.0   98.4 ± 0.6   97.8 ± 1.2
                                                                                                  D2 B4    HLT (%)      96.6 ± 1.1   96.9 ± 1.3   97.9 ± 0.1   97.8 ± 0.6
SpaTiaL translation.                                                                                           ∆          -0.0         -0.7         -0.5         0.0
   As shown in Fig. 5, flat sequence generation struggles
                                                                                                           Flat (%)     65.8 ± 3.2   76.6 ± 1.1   82.6 ± 1.9   83.3 ± 2.6
severely with deeply nested formal syntax, with GPT-5.2                                           D3 B3    HLT (%)      81.5 ± 1.1   88.5 ± 1.5   90.1 ± 0.6   92.1 ± 0.7
accuracy dropping from 73.9% on D2 B4 to a mere 18.0%                                                          ∆         +15.7        +11.9         +7.5         +8.8
on D4 B3. In contrast, the HLT scaffold acts as a powerful                                                 Flat (%)     34.0 ± 2.0   44.7 ± 1.5   48.9 ± 3.2   52.7 ± 1.4
structural prior, yielding a +24.0% absolute gain on the most                                     D4 B3    HLT (%)      50.4 ± 1.2   64.0 ± 1.1   70.4 ± 0.8   68.2 ± 4.6
                                                                                                               ∆         +16.4        +19.3        +21.5        +15.5
complex benchmark. This suggests that while frontier models
possess spatial reasoning capacity, the “flat” output format
remains a primary bottleneck.                                                                  The scaling behaviors in Table II reveal that Flat gener-
                                                                                            ation improves linearly with data, yet consistently fails to
                                                                                            bridge the gap with HLT in complex domains. Conversely,
                100          96.6
                                                                   Flat        HLT          HLT converges rapidly, reaching near-peak performance
 Accuracy (%)




                      73.9                         74.5                                     (70.4%) with a moderate data budget (Aug=5, 1,000 sam-
                 80
                                                                                            ples) and saturating thereafter. This early saturation confirms
                 60                         48.0                                            that structural priors mitigate the need for brute-force data
                                                                             42.0
                 40                                                                         scaling.
                                                                      18.0
                 20
                  0                                                                         E. Ablation: Data Allocation and Sample Efficiency
                      D2 B4                 D3 B3                     D4 B3
                                                                                               To understand the source of HLT’s performance gains and
Fig. 5: Comparison of Flat vs. HLT generation for GPT-
                                                                                            its practical data requirements, we conduct ablations on data
5.2. HLT significantly mitigates performance decay as logical
                                                                                            allocation.
nesting depth increases.
                                                                                               Allocating Data Budgets. We compare maximizing for-
                                                                                            mula diversity (1,000 unique structures × 1 paraphrase) ver-
C. Main Results: Model Scaling vs. Structural Decomposi-
                                                                                            sus emphasizing linguistic diversity (200 unique structures ×
tion
                                                                                            5 paraphrases, total 1,000 training pairs). For Flat generation,
   To test whether parameter scale can overcome the trans-                                  maximizing formula diversity is strictly necessary to improve
lation bottleneck, we fix the training distribution to the                                  on deep tasks (accuracy increases from 48.9% to 59.3%
Aug=5 setting and compare fine-tuned models from 3.8B                                       on D4 B3). In stark contrast, HLT achieves superior perfor-
to 14B parameters. The results in Table I indicate that raw                                 mance (70.4% vs. 70.0%) using far fewer unique skeletons
parameter scaling alone does not resolve the deep-nesting                                   (200 vs. 1,000) exposed to rich paraphrasing.
bottleneck. While fine-tuning improves both methods, HLT                                       Sample Efficiency. Furthermore, comparing Flat trained
yields markedly larger gains on deeper logic. Notably, an                                   with 3,000 pairs against HLT with 600 pairs on D4 B3,
8B model with HLT (70.4%) significantly outperforms a                                       HLT achieves higher accuracy (64.0% vs. 52.7%) using 5×
larger 14B model using flat generation (58.7%) on D4 B3,                                    less data. This confirms that HLT masters spatial logic with
highlighting structural decomposition as a more efficient                                   minimal structural examples, freeing up the model’s capacity
lever for performance than scaling model capacity.                                          to absorb language variations.
 (a)                                                                                                          (b)




                                                        Different Robotics Tasks Finished By OpenPi




                                                                                                              (c)




Fig. 6: Evaluation of continuous SpaTiaL robustness ρ(t) on the LIBERO manipulation benchmark using the π0.5 Vision-
Language-Action (VLA) policy. (a) Visual sequence of the multi-stage task execution. (b) Robustness analysis of a successful
trajectory, demonstrating that all nested geometric and temporal constraints are rigorously satisfied, with the satisfaction
margin ρ(t) > 0 during the specified temporal intervals. (c) The fluctuating robustness signal explicitly captures the end-
effector’s repeated, unsuccessful attempts to approach and grasp the bowl.


F. Downstream Robotic Applications
   To demonstrate practical utility beyond exact-match trans-
lation, we evaluate generated SpaTiaL formulas in down-
stream robotic pipelines for monitoring and action selection.
   Continuous Task Evaluation for VLA Executions. We
deploy generated SpaTiaL formulas to monitor multi-stage
manipulation tasks within the LIBERO benchmark, executed
by the π0.5 [31] VLA policy. The explicit spatial predi-
cates map to continuous kinematic observations (e.g., end-                        Fig. 7: Runtime verification of candidate VLA trajec-
effector and object poses), producing a robustness signal                         tories. Short-horizon rollouts proposed by the π0 model
ρ(t) that quantifies satisfaction margins over time. As shown                     are explicitly scored against the HLT-translated SpaTiaL
in Fig. 6, this continuous signal provides an interpretable                       specification.
evaluation of the VLA’s performance. It explicitly identifies
                                                                                  firms that our one-shot HLT translations successfully serve
stage-wise progress in successful rollouts and quantifies
                                                                                  as executable, interpretable trajectory verifiers for reliable
geometric violations—such as repeated, unsuccessful grasp-
                                                                                  downstream deployment.
ing attempts—in failed executions, all without requiring
manually designed reward functions. Runtime Trajectory
                                                                                                       VII. C ONCLUSION
Verification and Filtering. Beyond passive monitoring, we
evaluate the generated SpaTiaL formulas within a runtime                             We presented NL2SpaTiaL, a hierarchical framework for
“generate-and-test” pipeline using a VLA policy π0 [2].                           translating natural language into geometric Spatio-Temporal
At each inference step, the unconstrained VLA proposes                            Logic specifications for manipulation tasks. By generating
multiple candidate trajectories (short-horizon rollouts). We                      a structured logical tree followed by deterministic render-
use the translated SpaTiaL specifications as explicit verifiers                   ing, the method decouples semantic parsing from syntactic
to score these rollouts. By rejecting trajectories that violate                   realization, improving robustness and sample efficiency over
spatial constraints and selecting the one with the highest                        flat sequence generation, particularly for deeply nested logic.
robustness (Fig. 7), the system effectively filters out dynami-                   We also introduced a logic-first synthesis pipeline and a
cally unstable or geometrically unsafe future states. This con-                   hierarchically annotated dataset with controllable complexity
and diverse paraphrases, enabling systematic evaluation of                      [21] Y. Fang, Z. Jin, J. An, et al., “Enhancing transformation from natural
structural reasoning in NL-to-logic translation. A current                           language to signal temporal logic using LLMs with diverse external
                                                                                     knowledge,” in Findings Assoc. Comput. Linguist. (ACL), 2025, pp.
limitation is that training primarily supervises the final nested                    10 446–10 458.
JSON output, while richer hierarchical annotations—such                         [22] D. Mendoza, C. Hahn, and C. Trippel, “Translating natural language
as node-level descriptions and aligned intermediate subfor-                          to temporal logics with large language models and model checkers,”
                                                                                     in Proc. Formal Methods Comput.-Aided Des. (FMCAD), 2024, pp.
mulas—remain underutilized. Future work will incorporate                             1–11.
multi-level supervision (e.g., node-level objectives or staged                  [23] P. Kordjamshidi, M. V. Otterlo, and M.-F. Moens, “Spatial role
training), evaluate larger models under the same protocol,                           labeling: Task definition and annotation scheme,” in Proc. Int. Conf.
                                                                                     Lang. Resour. Eval. (LREC), 2010.
and extend the logic-first pipeline to pure TL benchmarks to                    [24] J. Pustejovsky, Verhagen, et al., “Iso-space: The annotation of spatial
test generality and scalability.                                                     information in language,” in Joint ISO - ACL SIGSEM Workshop on
                                                                                     Interoperable Semantic Annotation - ISA-6, 20110111 - 20110112.
                                                                                [25] J. Johnson, B. Hariharan, L. van der Maaten, et al., “Clevr: A
                             R EFERENCES                                             diagnostic dataset for compositional language and elementary visual
                                                                                     reasoning,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit.
 [1] V. Cohen, J. X. Liu, R. Mooney, et al., “A survey of robotic language           (CVPR), 2017, pp. 1988–1997.
     grounding: Tradeoffs between symbols and embeddings,” in Proc. Int.        [26] A. Suhr, S. Zhou, A. Zhang, et al., “NLVR2: A corpus for natural
     Joint Conf. Artif. Intell. (IJCAI), 2024, pp. 7999–8009, survey Track.          language reasoning over real photographs,” in Proc. Annu. Meet.
                                                                                     Assoc. Comput. Linguist. (ACL), 2019, pp. 6418–6428.
 [2] K. Black, N. Brown, D. Driess, et al., “pi 0: A vision-language-action
                                                                                [27] M. Abdin, J. Aneja, H. Awadalla, et al., “Phi-3 technical report: A
     flow model for general robot control,” arXiv:2410.24164, 2024.
                                                                                     highly capable language model locally on your phone,” arXiv preprint
 [3] W. Huang, C. Wang, Y. Li, et al., “Rekep: Spatio-temporal rea-                  arXiv:2404.14219, 2024.
     soning of relational keypoint constraints for robotic manipulation,”       [28] Llama Team, “The llama 3 herd of models,” arXiv preprint
     arXiv:2409.01652, 2024.                                                         arXiv:2407.21783, 2024.
 [4] C. Belta and S. Sadraddini, “Formal methods for control synthesis:         [29] Q. Team, “Qwen2.5 technical report,” arXiv preprint
     An optimization perspective,” Annu. Rev. Control Robot. Auton. Syst.,           arXiv:2412.15115, 2024.
     vol. 2, pp. 115–140, 2019.                                                 [30] T. Dettmers and A. o. Pagnoni, “Qlora: Efficient finetuning of quan-
 [5] H. Kress-Gazit, M. Lahijanian, and V. Raman, “Synthesis for robots:             tized llms,” arXiv preprint arXiv:2305.14314, 2023.
     Guarantees and feedback for robot behavior,” Annu. Rev. Control            [31] P. I. others, “π0.5 : a vision-language-action model with open-world
     Robot. Auton. Syst., vol. 1, pp. 211–236, 2018.                                 generalization,” 2025.
 [6] A. Brunello, S. Tonetta, N. Labai, et al., “Synthesis of LTL formulas
     from natural language texts,” in Proc. Int. Symp. Temporal Represent.                                       A PPENDIX
     Reason. (TIME), vol. 147, 2019, pp. 17:1–17:21.
 [7] J. X. Liu, Z. Yang, I. Idrees, et al., “Grounding complex natural          A. Deterministic Rendering Policy
     language commands for temporal tasks in unseen environments,” in
     Proc. Conf. Robot Learn. (CoRL), 2023, pp. 1084–1110.                         Table III specifies the deterministic realization map τ(·)
 [8] Y. Chen, R. Gandhi, Y. Zhang, and C. Fan, “Nl2tl: Transforming             used in our logic-first synthesis pipeline to convert SpaTiaL
     natural languages to temporal logics using large language models,”         formulas into controlled English. Each template is determin-
     arXiv preprint arXiv:2305.07766, 2023.
 [9] C. Pek, G. F. Schuppe, F. Esposito, et al., “Spatial: monitoring and
                                                                                istic, compositional, and preserves the information needed
     planning of robotic tasks using spatio-temporal logic specifications,”     for round-trip supervision generation.
     Auton. Robots, vol. 47, no. 8, pp. 1439–1462, 2023.                           At the spatial level, templates expose geometric constraints
[10] KTH-RPL-Planiacs, “Spatial: A framework to specify spatial and             explicitly (e.g., margins and tolerances). For temporal oper-
     temporal relations between objects,” 2023.
[11] M. Cosler, C. Hahn, et al., “nl2spec: Interactively translating unstruc-   ators, the mapping preserves interval bounds verbatim. This
     tured natural language to temporal logics with large language models,”     deterministic design is critical for (i) generating semantically
     in Computer Aided Verification. Springer Nature Switzerland, 2023.         consistent synthetic training data and (ii) providing stable su-
[12] W. English, D. Simon, et al., “Grammar-forced translation of natural
     language to temporal logic using llms,” 2025.                              pervision targets for hierarchical NL-to-SpaTiaL translation.
[13] J. Mao, C. Gan, P. Kohli, et al., “The neuro-symbolic concept learner:
     Interpreting scenes, words, and sentences from natural supervision,”                      TABLE III: Unified deterministic templates
     in Proc. Int. Conf. Learn. Represent. (ICLR), 2019.
[14] L. Ruis, J. Andreas, M. Baroni, et al., “A benchmark for systematic        Operator              Deterministic English Template
     generalization in grounded language understanding,” in Proc. Int.
                                                                                Spatial Constraints
     Conf. Mach. Learn. (ICML), 2020, pp. 7028–7039.
[15] A. Pnueli, “The temporal logic of programs,” in 18th Annual Sympo-         Touch(i, j)           “i is in contact with j.”
     sium on Foundations of Computer Science (FOCS). IEEE Computer              closeToε (i, j)       “The distance between i and j is at most εc .”
     Society, 1977, pp. 46–57.                                                  farFromε (i, j)       “The distance between i and j is at least ε f .”
[16] O. Maler and D. Nickovic, “Monitoring temporal properties of con-          ovlp(i, j)            “i partially overlaps j.”
     tinuous signals,” in Proc. Int. Symp. Formal Tech. Real-Time Fault-        partOvlp(i, j)        “i overlaps j without containment.”
                                                                                enclIn(i, j)          “i lies strictly inside j.”
     Tolerant Syst., 2004, pp. 152–166.
                                                                                LeftOf(i, j)          “i is strictly to the left of j (margin κ).”
[17] L. Žilka, “Temporal logic for man,” Bachelor’s thesis, Brno University    Betweenpx (a, b, c)   “Along the x-axis, b lies strictly between a and c.”
     of Technology, 2010.                                                       oriented(i, j; κ)     “The heading of i is aligned with that of j (within κ).”
[18] J. Pan, G. Chou, and D. Berenson, “Data-efficient learning of natural
     language to linear temporal logic translators for robot task specifi-      Temporal / Boolean Logic
     cation,” in Proc. IEEE Int. Conf. Robot. Autom. (ICRA), 2023, pp.          G[a,b] φ              “Throughout [a,b], τ(φ ) holds.”
     11 554–11 561.                                                             F[a,b] φ              “Sometime within [a,b], τ(φ ) holds.”
[19] K. Manas, S. Zwicklbauer, and A. Paschke, “Tr2mtl: LLM based               φ1 U[a,b] φ2          “Within [a,b] τ(φ2 ) becomes true; until then, τ(φ1 ) holds.”
     framework for metric temporal logic formalization of traffic rules,”       ¬φ                    “It is not the case that τ(φ ).”
     in Proc. IEEE Intell. Veh. Symp. (IV), 2024, pp. 1206–1213.                φ1 ∧ φ2               “τ(φ1 ) and τ(φ2 ) both hold.”
[20] B. Rabiei, M. K. A. R., Z. Dai, et al., “LTLCodeGen: Code genera-          φ1 ∨ φ2               “Either τ(φ1 ) or τ(φ2 ) holds.”
     tion of syntactically correct temporal logic for robot task planning,”     φ1 → φ2               “If τ(φ1 ) holds, then τ(φ2 ) must hold.”
     arXiv:2503.07902, 2025.
