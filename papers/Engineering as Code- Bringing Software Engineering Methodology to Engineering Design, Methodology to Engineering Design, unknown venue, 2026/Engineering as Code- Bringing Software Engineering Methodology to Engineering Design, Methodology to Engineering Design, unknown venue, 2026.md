                                                  Engineering as Code: Bringing Software Engineering
                                                          Methodology to Engineering Design

                                                                                      Song Difei
                                                     Huaxin Consulting, Design, and Research Institute, Hangzhou 310052

                                                                                 September 7, 2026
arXiv:2609.04216v1 [cs.SE] 22 Jun 2026




                                                                                       Abstract
                                                  Large language models have made significant progress in verifiable domains such as code
                                              generation, mathematical reasoning, and chip design, yet they remain limited on design
                                              generation tasks in traditional engineering fields like architecture, mechanical engineering,
                                              and HVAC. This paper argues that the root cause of this gap is not model capability per
                                              se, but rather the absence in engineering domains of a computable foundation in the form
                                              of “Design as Code” — a design representation that can be directly consumed, verified,
                                              and versioned by machines. Existing CAD/BIM systems deeply couple design logic with
                                              geometric representation, causing quality assurance activities to be severely shifted toward
                                              the tail end of the design process. Mainstream Automated Compliance Checking (ACC)
                                              methods not only can only perform retrospective review after design completion, but also
                                              suffer from an epidemic of false positives in geometric clash detection and high-cost model
                                              reconstruction problems caused by naming dependencies. The root of these deficiencies
                                              lies not in the algorithms, but in the inability of geometric models to encode the semantic
                                              information of “whether this pipe should pass through this wall.”
                                                  This paper systematically proposes the Engineering as Code (EaC) paradigm, which
                                              expresses engineering design as a text-native declarative language, with an automated rule
                                              engine, version control, and package management serving as the quality gate and collabo-
                                              ration foundation. The core contributions of this paper are threefold: (1) proposing the
                                              Information Representation Hypothesis, which systematically argues that the bottle-
                                              neck of engineering AI lies in the absence of a computable foundation in the form of “Design
                                              as Code” in traditional engineering domains; (2) proposing the ADL (Assembly Defi-
                                              nition Language) design language, which takes the Part as the fundamental atom and
                                              describes component types, inter-component relationships, and spatial layout through three
                                              orthogonal sub-languages: PDL (Part Definition Language), PML (Part Mating
                                              Language), and PLL (Part Layout Language); (3) proposing the Engineering Static
                                              Analysis (ESA) mechanism, which shifts compliance rules from downstream review to the
                                              design generation stage — unlike model ACC, ESA inspects design declarations rather than
                                              geometrically instantiated artifacts, and is therefore unencumbered by false collisions and
                                              naming dependencies, along with four operational guidelines: rule waivability, focusing on
                                              bottom-line rules, purifying collaboration signal-to-noise ratio, and AI-assisted rule library
                                              construction.
                                                  Keywords: Engineering as Code; Design as Code; Declarative Design; ADL; Engineer-
                                              ing Static Analysis; Information Representation Hypothesis; Reinforcement Learning with
                                              Verifiable Rewards (RLVR)


                                         1   Introduction
                                         Software engineering as a discipline builds reasoning infrastructure around correctness. Source
                                         code exists so that programs can be read, inspected, diffed, branched, merged, and versioned.
                                         Static analyzers catch defects before execution. Test suites provide fast, deterministic pass/-
                                         fail signals. CI pipelines gate every commit. These are not AI innovations—they are software

                                                                                            1
engineering innovations that AI subsequently exploits because they supply the structured, veri-
fiable feedback that reinforcement learning with verifiable rewards (RLVR) requires (Lightman
et al. 2023; DeepSeek-AI 2025). When code has a test suite, an agent can propose patches
and receive millisecond-level correctness feedback, and its policy improves accordingly (SWE-
agent contributors 2025). When a chip netlist has design rule checks (DRC), a placement agent
can learn under DRC supervision (Mirhoseini et al. 2020). The pattern is consistent across
code (Anthropic 2025), mathematics (Shao et al. 2024), and hardware: structured, checkable
representations enable AI.
Now consider physical engineering. A telecom rack designer specifies equipment, connectors,
power budgets, and spatial constraints. A structural engineer defines beams, nodes, and load
paths. An HVAC engineer plans ductwork and selects fans. The artifacts these engineers
produce—3D CAD models, BIM databases, IFC exchange files—are geometry-centric and deeply
coupled to tools (buildingSMART International 2023). They capture what the design “looks like”
and “how it fits together,” but do not separate design intent from geometric instantiation.
The consequences of this coupling extend beyond feedback latency. The dominant inspection
method today—automated compliance checking (ACC)—operates directly on geometric models.
Yet geometric models have no representation of intended relationships: a pipe passing through
a wall is flagged as a clash simply because the wall model lacks an opening, not because the design
is actually wrong. A server plugged into a PDU is invisible to the checker unless both follow
specific project naming conventions that the rule engine has been pre-configured to parse. The
result is that ACC produces massive false positives at semantically valid geometric intersections,
while also requiring costly per-project remodeling—renaming, restructuring, rebuilding—before
rules can even execute. These are not algorithmic flaws but representational flaws: geometry
cannot encode the answer to “is this pipe supposed to pass through this wall?”
The consequences for AI are severe. An agent that generates a building model or rack layout
receives no fast, deterministic feedback on whether its output is correct. The loop is broken.
Physical engineering has no cargo check.
The central thesis of this paper is: the bottleneck is representation infrastructure, not al-
gorithmic capability. Physical engineering lacks an equivalent of source code—a structured,
text-native, machine-checkable representation of design intent. And the software engineering
community, not the AI community, is best positioned to design such a representation. Specifi-
cally, the community that invented programmable lint, pre-commit hooks, static single assign-
ment, and package-level dependency resolution also possesses the vocabulary and design patterns
to define:
  • What an engineering design unit looks like (Part, analogous to a function or module)
  • How to declare compatibility constraints (Mate specifications, analogous to interfaces
    or type signatures)
  • How to separate spatial layout from part identity (layout language, analogous to separa-
    tion of presentation and logic)
  • How to stratify correctness rules by cost and precision (L0–L4 rule hierarchy, analogous
    to syntax → type → semantic → performance checks)
  • How to version, branch, and review entire artifacts (Git workflow, battle-tested in the
    code domain)
We call the resulting framework Engineering as Code (EaC). EaC is not “AI for
engineering”—it is a software engineering methodology for designing and implement-
ing source code representations and toolchains for the engineering domain.




                                                2
1.1     The Source Code Gap
Table 1 characterizes the gap between software engineering and physical engineering along the
dimensions required for verifiable feedback.

Table 1: Gap between software engineering and physical engineering along verifiable-feedback
dimensions

      Dimension         Software Engineering                 Physical Engineering (Current)
      Primary           Text (.rs, .py, .ts)                 Geometry (.stp, .rvt, .ifc)
      artifact
      Atomic unit       Function / module / class            CAD body / assembly node
      Type system       Static types, interfaces, generics   Implicit (connector families)
      Correctness       Compiler / lint / test suite         Downstream review / manual
      checking                                               review
      Check latency     Milliseconds to minutes              Hours to weeks
      Version control   Git (line-level diff, merge)         PDM / PLM (check-out/lock,
                                                             binary diff)
      CI pipeline       git push → lint → test →             Manual review gates
                        deploy
      Package           npm / cargo / pip                    Part libraries (vendor-specific,
      manager                                                unversioned)
      Relationship      Explicit (import, type signatures,   Implicit in geometry or naming
      encoding          dependency injection)                conventions
      Check             Rules target semantic categories     Rules rely on naming conventions;
      signal-to-noise                                        pure geometric clashes produce
      ratio                                                  massive false positives


Physical engineering does not lack rules—building codes, telecom standards, and interface spec-
ifications are rich and precise. What is missing is a representation that makes these rules
executable at design time—just as a compiler makes type-safety rules executable at compile
time.

1.2     Contributions
This paper makes three contributions to software engineering:
  1. ADL: Assembly Definition Language (§4). A three-layer design-intent language for
     physical engineering, composed of a Part Definition Language (PDL) for the Part
     type system (Family, Model, Instance), a Part Mating Language (PML) for explicit
     relationships (Mate and Connection), and a Part Layout Language (PLL) for spatial
     placement. Drawing on SE design patterns—separation of concerns, explicit type signa-
     tures, contract-based design—ADL provides a text-native, version-controllable, machine-
     checkable engineering representation that is distinct from and complementary to existing
     CAD and BIM formats.
  2. ESA: Engineering Static Analysis (§5). An L0–L4 layered rule checker that operates
     on ADL artifacts, from syntax → reference integrity → business rules → geometric con-
     straints. Unlike ACC—which operates on geometric models and suffers from false-positive
     noise and naming-dependency overhead—ESA checks design declarations over semantic
     categories (Part Family, Mate type, interface signatures). This paper defines ESA’s op-
     erational charter (waivers, baselines, signal-to-noise ratio, AI assistance) and provides a


                                                       3
      structured diagnostic format that serves simultaneously as human-readable error reports
      and machine-consumable reward signals.
  3. The Information Representation Hypothesis (§3). A testable claim, anchored in the
     RLVR literature: the bottleneck for AI in physical engineering is the lack of a computable
     design representation, not insuﬀicient model capability. This paper derives predictions
     from this hypothesis and describes SD-HWE-Bench, a benchmark designed to evaluate
     generative agent performance on ADL authoring tasks.
We validate ADL and ESA through piki, an open-source EaC runtime. On a representative
telecom rack deployment, piki checks 64 engineering rules—interface compatibility, power budget,
U-slot conflicts, load-bearing—in under 200ms. The prototype integrates with Git, supports -
-skip and warning_only rule waivers, and produces structured diagnostics suitable for CI
pipeline consumption. We report the prototype’s current scope and explicit limitations in §6.

1.3   Designing Source Code for New Domains Is a Core SE Problem
Designing source code representations for new domains has a deep academic lineage in soft-
ware engineering. The research tradition of domain-specific languages (DSL) demonstrates that
language design itself is an SE activity—it involves syntax design, semantic definition, type
system selection, and verification strategy trade-offs, each of which is an independently evalu-
able academic contribution (Hudak 1996). Hudak first systematically defined DSLs in 1996
as “programming languages tailored to a specific problem domain,” establishing the theoreti-
cal foundation for DSL design. Fowler further classified DSLs into internal and external DSLs
and summarized how language design patterns (semantic model, symbol table, builder) directly
benefit from compiler construction infrastructure (Fowler 2010). Völter et al. systematized DSL
engineering, demonstrating how a complete toolchain—grammar definition, constraint checking,
code generation, and IDE integration—revolves around a single language definition (Völter et
al. 2013).
ADL continues this lineage, but targets a domain previously untouched by the DSL community—
physical engineering design. Traditional DSL research primarily targets software developers (e.g.,
SQL, regular expressions, AWK), whereas ADL targets a dual audience of engineering design-
ers and AI agents. This requires the language to balance “human readability” and “machine
verifiability”—a constraint not prominent in traditional DSL design.
Similarly, the academic tradition of static analysis provides the direct theoretical foundation for
ESA. Static analysis in compilers evolved from initial syntax checking (L0) to type systems (L1),
data-flow analysis (def-use chains, SSA), and program verification. Cousot’s abstract interpreta-
tion theory provided the mathematical foundation for the soundness and completeness of static
analysis (Cousot and Cousot 1977). Industrial-grade static analyzers such as Coverity and Infer
demonstrated the feasibility of layered rule systems in engineering practice—from cheap syntax
checks to expensive inter-procedural analysis. ESA’s L0–L4 layered design directly replicates
this pattern, mapping “syntax → reference integrity → type constraints → spatial constraints”
onto concrete rule categories in the engineering domain. The resemblance to compiler analysis
pipelines is not coincidental—it is intentional: physical engineering design likewise possesses
semantic layers that can be checked hierarchically; what was previously missing was a represen-
tation layer that makes such stratification possible.
The success of IaC static analysis provides proximal empirical evidence for this extrapolation.
Chiari et al., in EMSE 2024, systematically studied the effectiveness of static analysis tools
for Terraform and Ansible, demonstrating that the “X as Code + static analysis” paradigm is
viable and eﬀicient in the cloud infrastructure domain (Chiari et al. 2024). EaC extrapolates this
same paradigm from cloud infrastructure to physical infrastructure—from “server configuration


                                                4
as code” to “server rack deployment design as code.” The SE contribution of this extrapolation is:
it demonstrates that the DSL+static analysis pattern invented by the IaC community is domain-
independent, and physical engineering is its most demanding testbed—with richer constraint
types (discrete + continuous), stricter verification latency requirements (millisecond-level RLVR
feedback), and more diverse consumers (human engineers + AI agents + downstream CAD/CAE
tools).

1.4    Paper Structure
Section 2 surveys current representations used in physical engineering, analyzing the struc-
tural deficiencies of model-based ACC—geometric clash false positives and naming-dependency-
induced remodeling overhead—and why they constitute an AI bottleneck. Section 3 articulates
the Information Representation Hypothesis and its RLVR foundation. Section 4 introduces ADL:
its three-layer architecture, design rationale, and integration with SE toolchains. Section 5 in-
troduces ESA: the layered rule hierarchy, semantic advantages over ACC, operational charter,
structured diagnostic output, and downstream verification protocol. Section 6 reports evalua-
tion results from the piki prototype—all three samples pass, and violation injection experiments
validate ESA’s detection accuracy at 100% recall. Section 7 discusses differentiation from re-
lated work—ACC, SysML v2, BIM/IFC, IaC static analysis, and existing benchmarks. Section
8 concludes, acknowledges limitations, and outlines future work including SD-HWE-Bench and
RLVR training.


2     Background and Motivation
This chapter traces a causal chain that has already driven transformation in three adjacent
domains, establishes the motivation for Engineering as Code, and explains why engineering
design has so far been unable to participate in this chain.

2.1    The RLVR Causal Chain
Across three domains — code, mathematics, and chip design — a striking pattern recurs: a
structured representation of correctness enables automatic, deterministic checking; that checking
provides a fast reward signal; and that signal makes Reinforcement Learning with Verifiable
Rewards (RLVR) effective.
    • Mathematics. DeepSeekMath trains on problems whose final answers are automatically
      verifiable. Using Group Relative Policy Optimization (GRPO), it improves reasoning with-
      out requiring a separate reward model (Shao et al. 2024). Lightman et al. demonstrate
      that Process Reward Models (PRMs) — scoring intermediate reasoning steps — outper-
      form Outcome Reward Models (ORMs), underscoring the value of step-level checkability
      (Lightman et al. 2023).
    • Code. SWE-RL uses test suite pass/fail as a reward signal to train agents for fixing
      GitHub issues, achieving substantial gains over supervised fine-tuning (SWE-agent con-
      tributors 2025). Claude Code and similar agents operate in repositories where compilation
      and tests provide immediate feedback (Anthropic 2025).
    • Chips. Deep-reinforcement-learning-based chip placement treats design rule checking as a
      fast, differentiable signal during macro placement (Mirhoseini et al. 2020); AMS-IO-Bench
      evaluates LLM-generated I/O ring designs under DRC/LVS (Liu et al. 2025).
The pattern can be summarized as:
Structured, checkable representation → Sub-second deterministic feedback → RLVR effective →
We call this the RLVR Causal Chain.

                                                5
2.2     Why Engineering Design Is Blocked
Physical engineering design — buildings, mechanical assemblies, telecommunications infrastruc-
ture — has so far failed to participate in this chain. The obstacle lies not in insuﬀicient model
scale or excessive physical complexity, but in the fact that the design representation itself
cannot be checked by machines in the required way.
Today’s dominant representations are CAD and BIM. They couple three things within the same
artifact:
  1. Functional identity (what a component is and does)
  2. Geometric realization (where it is located and how it looks)
  3. Tool-specific state (vendor-format-internal constraints, history, parameters)
This coupling creates three problems for AI agents.
Information loss. Once design intent is frozen into geometry, recovering the original functional
relationships — which port connects to which, which cabinet hosts which server, which rooms
form a fire compartment — requires reverse extraction. Eastman et al. and Zhang et al. doc-
ument that ACC must parse IFC or drawing models and infer intent, a lossy and error-prone
step (Eastman et al. 2009; Zhang and El-Gohary 2019).
Feedback delay. ACC runs after the design artifact is complete. When a violation is found,
the design is already a tightly coupled multi-discipline model; remediation is costly and slow.
No training signal. Because checking is downstream and expensive, an agent cannot use it as
a reward during generation. It cannot try a layout, receive a pass/fail reward in milliseconds,
and update its policy. The RLVR loop breaks at the very first arrow.
Recent work has attempted to apply LLMs directly to building code interpretation (Fuchs et
al. 2024; Yang and Zhang 2024; Nakhaee et al. 2024), but these approaches still operate
downstream of the design artifact. They improve the reviewer side, not the generator side.

2.2.1    Two Structural Deficiencies of Model-Based ACC
Even within its operating scope — checking completed designs — model-based ACC suffers
from two structural, rather than algorithmic, deficiencies. These deficiencies explain why merely
accelerating ACC cannot bridge the gap.
False positives from pure geometric clash detection. BIM clash detection treats every
volumetric intersection as a violation. A pipe passing through a wall triggers a clash because
the wall model lacks an opening. A cable tray crossing a beam is reported as a clash even when
the two have physical clearance by design. These are not detection errors — the algorithm
correctly identifies geometric overlap. The problem is that the model contains no semantic
information describing the intended relationship between two objects. In EaC terms, the
model lacks a Mate declaration stating “this pipe passes through this wall” or “this cable tray
sits above this beam at a specified offset.” Without such a declaration, the checker cannot
distinguish an intentional penetration from a genuine layout error. The result is a flood of false
positives that designers learn to ignore, drowning genuine violations in noise.
Naming dependency and remodeling overhead. Rule-based ACC tools — whether operat-
ing on IFC, Revit, or proprietary formats — rely on standardized naming conventions to identify
objects. A rule such as “all ducts named DUCT-SUPPLY-* must maintain 50 mm clearance from
structural elements” works only if every duct in every project obeys that naming convention.
In practice, naming conventions vary across firms, projects, and even disciplines. Before ACC
can run, the model must be remodeled — objects renamed, reorganized, and sometimes re-
constructed — to match the naming patterns the rule engine expects. This remodeling step is

                                                6
manual, expensive, and itself introduces errors. Worse, it erodes the eﬀiciency ACC is supposed
to provide: if you must remodel the design before checking it, you have not automated checking
— you have merely shifted manual labor upstream. One consequence of this structural problem
is that the ACC community, after 15 years of development, still lacks a standardized evaluation
benchmark: heterogeneous IFC models with different naming conventions, LODs, and modeling
practices cannot form a unified test set, and every evaluation requires bespoke remodeling and
rule adaptation.
These three deficiencies — false-positive noise, naming-dependent remodeling, and non-
reproducible evaluation due to representation-layer issues — share a common root: the model
is the design’s sole structured description, but it is structured for geometric representation
rather than semantic query. A rule engine that must check geometry to infer intent will forever
be limited by the semantic poverty of geometry.

2.3    Lessons from Software Engineering and Chip Design
Two mature domains offer a different model.
Infrastructure as Code (IaC). Tools such as Terraform and Ansible express infrastructure
as versionable, diffable, and statically analyzable textual declarations. Chiari et al. empirically
demonstrate that IaC static analysis tools can detect hundreds of security and compliance vio-
lations in seconds (Chiari et al. 2024). IaC proves that “X as Code” plus static analysis is a
practical, scalable combination (Morris et al. 2022; Quattrocchi and Tamburri 2023).
Chip design. A Verilog netlist is the source of truth for logical design; physical layout is a
downstream view. Design rule checking runs during place-and-route, not only after tape-out.
The representation is deliberately designed to be textual, hierarchical, and checkable before
visualization (IEEE 2005).
Engineering design has no equivalent of a Verilog netlist or a Terraform file. EaC’s goal is
precisely to provide one.

2.4    The Research Gap
The gap can be stated precisely. Existing work provides:
    • Rich geometric representations (CAD/BIM/IFC);
    • Downstream compliance checking (ACC), hampered by false-positive noise and naming-
      dependency overhead;
    • Isolated AI benchmarks for engineering tasks (EngDesign contributors 2025; Galanos
      and Mulyar 2026; Maatouk et al. 2023).
What is missing is an upstream, text-native, machine-checkable design representation
— one that can serve as both a training objective for generative agents and a source of truth for
human engineers. EaC fills this gap.


3     The Engineering as Code Approach
EaC is a proposition about infrastructure. It says: before we ask whether AI can design physical
systems, we should ask whether those systems are represented in a form that is operable by a
software engineering toolchain. This section defines the paradigm, articulates its core hypothesis,
and connects that hypothesis to the RLVR literature and the layered design of the ESA.




                                                7
3.1     What Is EaC
Engineering as Code (EaC) is the practice of treating a structured, textual design declaration
as the single source of truth for a physical engineering system, and building a software engineering
toolchain — version control, static analysis, CI/CD, and automated verification — around that
representation.
EaC is not a replacement for CAD or BIM. Physical engineering will always need geometric
modeling, simulation, and manufacturing output. EaC separates concerns: design intent (what
parts to use, how they connect, where they are placed) is expressed textually in the ADL, while
geometry instantiation and analysis consume that declaration as input. This is the same sepa-
ration that chip design achieves with hardware description languages: Verilog/VHDL describe
intent; placement tools generate geometry; DRC checks the result (IEEE 2005).
EaC has three pillars, but forms a single integrated proposition:
  1. ADL (§4) is the representation layer: an engineering design language designed to be read,
     checked, diffed, and versioned by a SE toolchain.
  2. ESA (§5) is the verification layer: a rule engine that provides fast, deterministic correct-
     ness feedback, making RLVR possible.
  3. The Information Representation Hypothesis (§3.2) is the theoretical anchor: con-
     necting these technical choices to a testable claim about why AI progress in physical
     engineering has stalled.

3.2     The Information Representation Hypothesis
We assert:
        The Information Representation Hypothesis. The lag of AI in physical en-
        gineering is primarily caused by the absence of a structured, text-native, machine-
        checkable design representation, rather than by insuﬀicient model capability or the
        intrinsic complexity of physics.
This hypothesis is information-theoretic, not computational. It does not claim that physics
is simple, or that current models are already capable enough to design complex systems. It
claims that even if models had the capability, current representations would prevent them from
improving, because those representations do not support the learning signal that has driven AI
progress in code, mathematics, and chip design — fast, deterministic correctness feedback.

3.2.1    Evidence from Adjacent Domains
The hypothesis rests on measurable regularities from three domains:
Code. SWE-bench tasks require an agent to fix real GitHub issues (Jimenez et al. 2024). The
reward signal is a test suite: the agent’s patch either passes or fails. SWE-RL demonstrated
that with this signal alone, without human demonstrations, agents could be trained to solve
42% of SWE-bench Verified tasks (SWE-agent contributors 2025). The representation — a Git
repository with a test suite — is the scaffolding that makes RLVR feasible.
Mathematics. DeepSeekMath and DeepSeek-R1 trained on formal theorem proving, where
the correctability of each proof step is verifiable (Shao et al. 2024; DeepSeek-AI 2025). A
key finding from Let’s Verify Step by Step is that a process-supervised reward model (PRM)
outperforms an outcome-supervised reward model (ORM) (Lightman et al. 2023). For PRM
to be effective, intermediate steps must be individually verifiable — a property that only a
structured, decomposable representation can provide.



                                                 8
Chip Design. Google’s chip placement work uses Verilog netlists as input and design rule
checking (DRC) as the reward signal (Mirhoseini et al. 2020). DRC checks manufacturability
constraints (spacing, layer rules, timing) and returns a pass/fail verdict. The representation
(netlist + standard cell library) decouples functional intent from geometric implementation,
making the reward computable.
The common structure is:
Structured representation → Deterministic checker → Fast feedback loop → RLVR training feasi
Physical engineering currently lacks the first two items. CAD/BIM models are not structured
for checking; downstream review is not fast enough. The loop is broken.

3.2.2    Testable Predictions
The hypothesis yields concrete predictions:
   • P1. Agents that receive deterministic ESA pass/fail feedback on their ADL outputs will
     produce designs with fewer violations than agents that receive only natural-language task
     descriptions.
   • P2. The improvement in P1 holds when controlling for model capability (same base model,
     same task diﬀiculty).
   • P3. The L0–L4 layered diagnostic format will achieve faster error correction than a flat
     error list, because structured diagnostics allow agents to localize and prioritize failures by
     layer.
   • P4. Agent designs that pass the ESA will produce fewer downstream errors (collisions,
     assembly failures) than designs verified with coarser-grained checkers or with no checking
     at all.
SD-HWE-Bench (§6.3) is specifically designed to test P1–P3. P4 is a long-term empirical goal.

3.3     Why This Is a Software Engineering Contribution
Designing a source-code representation for a new domain is a software engineering problem. It
requires decisions about:
   • Syntax and semantics. What is the atomic unit (Part)? How are relationships declared
     (Mate)? How is spatial layout expressed without embedding part identity? These are
     language design questions, analogous to designing a type system or IR.
   • Layered verification. Which checks are cheap enough to run on every keystroke (L0)?
     Which checks require global analysis but remain deterministic (L3–L4)? Which checks are
     inherently non-deterministic or too expensive (L5–L6)? This is a static analysis pipeline
     design problem.
   • Toolchain integration. How do design artifacts interact with Git (diff, blame, bisect),
     CI (pre-commit hooks, gating), and diagnostics (structured output, editor integration)?
     These are software engineering infrastructure questions.
   • Extensibility. How do users add new Part Families, rules, or domain vocabularies without
     modifying the core engine? This is a plugin and API design problem.
EaC answers these questions for physical engineering, but its framework — text-native DSL +
layered static analysis + toolchain integration — is domain-agnostic. The same template can
be applied to clinical trial protocols, legal contracts, or infrastructure configurations. In this
sense, EaC is both a concrete system for physical engineering and a methodology for extending
SE infrastructure to domains that are textualizable but currently under-structured.




                                                9
4     ADL: Assembly Definition Language
ADL is the declarative design representation of Engineering as Code. It is deliberately designed
to be text-native: design intent is authored in YAML, verified as code, rather than captured
as geometric operations inside a CAD or BIM GUI. ADL is organized around three orthogonal
sub-languages, separating “what exists,” “how parts couple,” and “where they are placed.”

4.1    Design Goals
ADL pursues three goals:
    1. Text-Native Representation. Agents and humans can write and read design intent in
       plain text, enabling version control, diﬀing, and programmable generation.
    2. Agent-Oriented Syntax. Files have explicit identity, references, and deterministic vali-
       dation. No hidden state dependent on a GUI session exists.
    3. Orthogonality of Identity, Relationships, and Space. A change in one dimension
       must not force a rewrite of files in another dimension.
The reference runtime is piki, an open-source engine that loads ADL declarations, runs a layered
rule engine, and produces downstream deliverables. However, ADL is defined independently of
any single tool.

4.2    Part as the Engineering Atom
In ADL, a Part is the atomic unit of engineering description. A Part is more than just geometry;
it is a semantically complete entity that exposes typed interfaces and participates in explicit
relationships. A Part is defined by the following elements:
    • Family (schema and value-domain constraints)
    • Model (a concrete realization with default values)
    • Instance (a deployed entity that can override defaults)
    • A set of typed Interfaces
    • Optional internal geometry, kept hidden unless high-precision analysis is required
The Part abstraction rests on four properties:
    1. Semantic Completeness. A server Part type is ServerFamily, carrying fields such
       as height_u, tdp_w, psu_count, etc. A pump Part carries flow_rate and head. Type
       checking is enforced by plugin-registered pydantic schemas.
    2. Encapsulation. Internal geometry is hidden; only standardized interfaces are visible to
       downstream consumers.
    3. Relationship-Built-In. The role of a server within an assembly is expressed through
       relationships: it is a child in a rack-mount-19inch Mate; an optical transceiver is a
       child in an sfp28-cage Mate.
    4. Multi-View Projectability. The same Part can be projected to CAD (USD/glTF),
       CAE (thermal or structural models), ERP (BOM entries), and lifecycle catalogs without
       changing its core declaration.

4.3    PDL: Part Definition Language
PDL defines the Part type system at three levels: Family, Model, and Instance.
Family. A Family is a pydantic BaseModel class that declares the schema and value-domain
constraints for a class of Parts. For example, ServerFamily requires id, height_u (1–48), tdp_w
(>0), and a list of interface specifications. A Family is code, not configuration; it is registered
by plugins.

                                                 10
Model. A Model provides concrete default values for a Family. An example model file:
model: dell-r750
family: ServerFamily
brand: Dell
mpn: PowerEdge R750
height_u: 2
tdp_w: 600
psu_count: 2
Instance. An Instance is a deployed entity that can override Model defaults:
id: SRV-01
model: dell-r750
family: ServerFamily
status: planned
At runtime, resolved values are computed as Model.defaults + Instance.overrides, then
validated against the Family schema. An Instance’s identity is derived from its filename (SRV-
01.yaml → SRV-01). A key design decision is that Instance files contain no layout infor-
mation; layout is declared separately in PLL. This separation means the same device can be
used in multiple positions across different design alternatives without duplicating its definition.

4.4   PML: Part Mating Language
PML describes relationships between Parts, distinguishing two categories: Mate and Connec-
tion.
Mate expresses design coupling: it constrains how two Parts fit or work together. Mates are
stored as independent YAML files under mates/<mate_type>/. For example:
type: rack-mount-19inch
parent: RACK-A02
child: SRV-01
at:
  u_start: 10
  u_span: 2
constrains:
  - field: depth_mm
    operator: "<="
    value_ref: depth_mm
The engine validates these constraints at load time. Registered Mate types include sfp28-cage,
power-iec-c14-c13, and lc-connector.
Connection expresses the flow of signal, energy, or material between two interfaces. A Con-
nection is itself a first-class Instance:
id: CONN-ACCESS-SRV01
family: PortConnectionFamily
from_port: ACCESS-SW-01/10GE1/0/1
to_port: SRV-01/eth0
cable_type: OM4-LC-LC
The Mate/Connection separation maps to two independent design phases: mechanical or elec-
trical feasibility (Mate) and functional topology correctness (Connection). CAD/BIM systems



                                                11
often merge them into a single object, making it impossible to validate one dimension without
involving the other.

4.5   PLL: Part Layout Language
The essence of PLL is eliminating degrees of freedom — including the geometric degrees of
freedom retained in PML mates for operability, and the full-spatial degrees of freedom of free
Parts with no Mate claims in the assembly.
PLL works through a priority chain. (1) For Parts that have a Mate in PML, Parts claimed
as a child by a Mate have their pose determined primarily by the PML mating constraint
solver; PLL provides parameterized DOF completion — assigning concrete values (at.u_start,
at.t, at.state) for the continuous DOFs (translation, rotation, screw) and discrete states
(normal/reverse/unplugged) retained in the Mate. The mating solver supports face-mating,
axis-alignment, and positional mating paradigms, as well as dynamic collision avoidance for
multi-axis translation and discrete state verification. (2) For Parts with no Mate, PLL directly
assigns a global pose (absolute coordinates, parent-relative transform, or grid position). (3) In
multi-solution scenarios, a layout may carry constraint optimization heuristics (such as minimum
energy or shortest cabling defaults) to select among feasible solutions.
PLL further separates layout data from PDL and PML files, ensuring that layout changes
(such as swapping a connector type) do not pollute each other, preserving the orthogonality of
PDL/PML/PLL.
Known boundaries of the current PLL implementation: the geometric solving precision for
continuous DOFs is currently principal-axis approximation and has not yet been extended to 1D
continuous-path topologies such as piping/cabling. These are deferred to future solver precision
enhancements and external CAE tool handling.

4.6   Orthogonality
The orthogonality of PDL, PML, and PLL is the core design principle of ADL. Each sub-language
resides in independent files: PDL in instances/ and models/, PML in mates/, and PLL in
layouts/. Because namespaces are separated, a change in one dimension does not rewrite files
in another dimension.
Incremental Validation. An Agent can first generate PDL declarations and pass L0–L2
checks, then proceed to PML constraints and PLL spatial rules. This matches the phased error
feedback of a compiler.
Parallel Editing. A device engineer editing instances/SRV-01.yaml, a layout engineer edit-
ing layouts/layout.yaml, and a mechanical engineer editing mates/rack-mount/RACK-A02-
SRV-01.yaml can work simultaneously. Git merge conflicts only occur when the same decision
dimension is changed.
Semantic Diff. A diff in instances/ means “some device identity or attribute changed”; a diff
in mates/ means “some mating changed”; a diff in layouts/ means “some position changed.”
For example:
- position_u: 10
+ position_u: 12
is unambiguously a layout change, while a change to tdp_w in instances/SRV-01.yaml is an
electrical change. This interpretability supports both human code review and automatic reward
attribution in RLVR training.



                                               12
4.7   Comparison with SysML v2 and BIM/IFC
ADL, SysML v2, and BIM/IFC all aim to formalize engineering systems, but they differ funda-
mentally in assumptions about source-of-truth form, collaboration units, and target users.

Table 2: Comparison of ADL with SysML v2 and BIM/IFC across source-of-truth, versioning,
and verification dimensions

   Dimension         SysML v2 (Object         BIM / IFC                 ADL (piki)
                     Management Group         (buildingSMART
                     2024)                    International 2023)
   Source-of-        Model repository         Central model file /      Text files (YAML +
   Truth Form                                 IFC exchange              TOML)
   Version           Model version            File version              Git line-level history
   Control Unit
   Core              Model element            Geometric object /        File (Instance, Mate,
   Operation                                  IFC entity                Layout)
   Unit
   Identity &        Mixed in                 Geometry as identity      File-level separation of
   Space             part/occurrence                                    Instance and Layout
   Inter-Part        connection /             Implicit in geometric     Binary Mate +
   Relationships     interaction              constraints               Connection
                                                                        separation
   Verification      Model checking           Clash detection           ESA L2–L4a +
   Method                                     (post-hoc)                load-time L0–L1
                                                                        checks,
                                                                        millisecond-level
   Target User       Human systems            Human designer            AI Agent + human
                     engineer (GUI)           (GUI)                     engineer (text)


SysML v2 and BIM are primarily modeling environments for human engineers. Their source
of truth resides in repositories or large central files that are diﬀicult to diff, branch, and auto-
matically verify. IFC in particular couples identity, geometry, and relationships in a graph that
permits multiple equivalent serializations, making line-level version control diﬀicult (H. Liu et
al. 2023).
ADL inverts these priorities. It is oriented toward Agent-human collaboration, treats text as
the sole source of truth, and makes verification a first-class concern. CAD and BIM are not
eliminated; they become downstream consumers of ADL declarations, used for visualization,
clash detection, and manufacturing.

4.8   Core Syntax Summary
The following grammar summarizes the core constructs of ADL.
Project            ::= piki.toml (ModelFile | InstanceFile | MateFile | LayoutFile)*

ModelFile          ::= "model:" id
                       "family:" FamilyName
                       Field*
                       ("interfaces:" InterfaceSpec*)?



                                                13
InstanceFile    ::= "id:" id
                    ("family:" FamilyName | "model:" ModelName)
                    Field*
                    ("interfaces:" InterfaceSpec*)?

InterfaceSpec ::= "- id:" id
                  "interface_type:" Type
                  ("direction:" "input" | "output" | "bidirectional")?
                  ("local_transform:" Transform)?

MateFile        ::= "type:" MateType
                    "parent:" Ref
                    "child:" Ref
                    ("at:" Map)?
                    ("constrains:" MateConstraint*)?
                    ("pairings:" InterfacePairing*)?

MateConstraint::= "- field:" Field
                  "operator:" "<=" | ">=" | "<" | ">" | "==" | "!="
                  "value_ref:" FieldOrConstant
                  ("message:" String)?

LayoutFile      ::= LayoutEntry*
LayoutEntry     ::= "- instance:" id
                    (AbsolutePose | RelativePose | GridPose)

AbsolutePose    ::= ("position_x_mm:" num)+
RelativePose    ::= "parent:" id
                    "transform:" Transform
GridPose        ::= "grid_id:" id
                    ("grid_position:" [String, String]
                    | "row_id:" String "bay_index:" Int)

Transform       ::= "translation:" [num, num, num]
                    ("rotation:" [num, num, num])?
                    ("scale:" [num, num, num])?

Ref             ::= id | id "/" interface_id
Key semantic constraints not captured by the grammar include: InstanceFile must not contain
layout fields; LayoutEntry must use exactly one of absolute, relative, or grid pose; interface
references in Ref must resolve to an existing interface.


5     ESA: Engineering Static Analysis
Engineering Static Analysis (ESA) is the mechanism that makes EaC’s shift-left quality strat-
egy executable. It consumes ADL declarations and checks deterministic rules before design
submission, moving compliance review from downstream inspection to upstream gating.




                                             14
5.1     From ACC to ESA
Traditional Automated Compliance Checking (ACC) operates on completed CAD/BIM models
or IFC files (Eastman et al. 2009; Zhang and El-Gohary 2019). This creates three structural
problems:
   1. Information loss. Design logic is frozen into geometry; reverse-extracting functional
      relationships is lossy.
   2. High feedback cost. Violations are discovered only after the design has been coupled
      into a multi-discipline model.
   3. No RLVR signal. ACC can only judge completed designs; it cannot reward Agents
      during generation.
Beyond these timing issues, model-based ACC suffers from two deeper semantic deficiencies
(see §2.2.1). First, pure geometric clash detection produces massive false positives—pipes pass-
ing through walls, tray crossings—because the model has no representation of intended rela-
tionships. Second, rule-based ACC relies on standardized naming conventions, forcing costly
pre-check model rework that erodes the very eﬀiciency ACC was supposed to provide.
ESA addresses these problems at the root. It checks ADL declarations—not geometry—and
therefore has access to:
   • Part identity and type (Family schema), allowing rules to operate on semantic cate-
     gories (e.g., “any PDUFamily instance”) rather than naming patterns (e.g., “any object
     named PDU-*”);
   • Explicit Mate relationships (PML), allowing the checker to know which pairs of ob-
     jects are intended to interact—and to exclude them from clash detection (a pipe passing
     through a wall is a declared Mate, not a clash to suppress);
   • Layered checking (L0–L4), allowing syntax errors, reference errors, and business rule
     violations to be caught at distinct stages, each with targeted diagnostics.
The result is not a faster ACC. It is a checker that operates on a fundamentally different in-
put: design intent rather than design instantiation. This distinction—checking declarations
vs. checking models—is identical to the distinction that makes a compiler type checker fundamen-
tally different from a post-hoc binary analysis tool. The compiler has access to the type system;
the binary analysis tool must infer types. Even in ACC’s most mature subdomain (building fire
code), state-of-the-art graph reasoning methods achieve only 84.3% accuracy (Xiao et al. 2025)
and frequently fail on rules involving multi-step spatial reasoning chains—this is not the ceiling
of algorithms, but the ceiling of the semantic bandwidth of geometric representation.

5.1.1    Concrete Example: Rack Power Budget
The following comparison checks whether the total power of devices in a rack exceeds its PDU
capacity.
Model-based ACC approach. The checker must: (a) parse the BIM model to identify
rack objects, (b) identify server objects, (c) determine which servers belong in which rack via
geometric containment or naming conventions, (d) extract power ratings from property sets (if
populated), (e) extract PDU ratings (if populated), (f) compare. Steps (a)–(e) depend on model
quality and naming standards. If a server is named DELL-R740-SRV01 instead of SERVER-R740-
01, the rule engine may miss it. If power ratings are stored in project-specific shared parameters,
rules must be customized per project.
ESA approach. The rule iterates over all PDUFamily instances, traverses their outputs, accu-
mulates the rated_power_w of connected loads, and compares against each output’s rated_-
power_w. The rule is 12 lines of Python, independent of naming conventions, and valid for

                                                15
any project using the same Part Family. Diagnostics pinpoint the specific PDU output and
over-limit loads.
This is not a comparison of speed. This is a comparison of whether the rule can be authored
without per-project customization.

5.2   Why “Static Analysis”
ESA borrows the term “static analysis” from software engineering because it shares three char-
acteristics:
   1. No physical simulation is executed. What is reasoned about is declarations and
      constraints, not simulated physics.
   2. Deterministic results. The same ADL declarations always produce the same pass/fail
      verdict.
   3. Low cost. Millisecond to sub-hundred-millisecond completion, suitable for pre-commit
      hooks and CI gating.
Just as lint and type checking cannot replace unit tests, ESA cannot replace CAE/CFD or
human review. It intercepts a large volume of low-level, deterministic errors at the front end,
allowing expensive validation to focus on issues that truly require expert judgment.

5.3   Four Operational Principles
ESA follows four principles designed to make it usable in real engineering practice.
Principle I: Rules are waivable. Physical boundary conditions cannot be exhausted by a
finite rule set. ESA allows authorized engineers to waive specific rules, but every waiver must
be recorded as part of the design history and trigger downstream reinforced verification (e.g.,
higher-fidelity CAE simulation or physical testing). The goal is to transform “beyond-spec”
behavior from informal decisions into auditable risk management.
Principle II: Focus on baseline rules. Initial deployment should focus on mechanical, de-
terministic clauses: fire separation distances, egress clear width, minimum clear height, power
budget, U-position conflicts. These rules have binary verdicts, minimal dispute space, and high
automation returns. The rule library should support modular configuration, allowing projects
to compose national codes, local standards, and enterprise internal controls.
Principle III: Shift-left and signal-to-noise optimization. Software engineering, through
CI/CD practices, has validated that lint and type checking intercept low-value errors before
commit, freeing code review to focus on architecture and logic. ESA applies this same principle:
catching rule violations at design time prevents them from propagating into downstream artifacts,
reducing costly rework cycles. Rule severity tiers (error, warning, info) and suppression directives
(# noqa) allow teams to tune the signal-to-noise ratio, just as engineering teams tune compiler
warning levels.
Principle IV: Declarative rule authoring. Rules should use structured decorators and mod-
ular organization so that domain experts can compose and extend rules without understanding
the checker engine internals. See Appendix A for the full rules directory structure.

5.4   Rule Hierarchy: L0–L6
ESA partitions all checkable rules into a six-layer hierarchy, with clear ownership boundaries at
each layer:




                                                16
                Table 3: ESA rule hierarchy (L0–L6) and ownership boundaries

  Layer             Name               Scope             Responsible         Example
  L0                Lexical            Single ADL file   ADL Loader          YAML syntax
                                                                             validity
  L1                Schema             Single ADL file   ADL Loader          Required fields,
                                                                             type constraints
  L2                Semantic           Cross-file        ESA Core            Part references
                    Reference                                                exist, Mate
                                                                             types compatible
  L3                Business Rule      Cross-file        ESA Core            Power budget,
                                                                             U-position
                                                                             conflict, fire
                                                                             separation
  L4a               Lightweight        Cross-file        ESA Extension       AABB-based
                    Geometry                                                 spatial conflicts,
                    (AABB)                                                   clearance checks
  L4b               Precise            Cross-file        Downstream          Precise clash
                    Geometry                             CAD                 detection
                                                                             (requires CAD
                                                                             kernel)
  L5                Physical           Cross-file        Downstream          Structural,
                    Simulation                           CAE/CFD             thermal, fluid
                                                                             analysis
  L6                Human/Expert       Project-level     Downstream          Professional
                    Sign-off                             Process             engineer stamp,
                                                                             compliance
                                                                             sign-off


ESA’s core scope covers L2–L4a. L0–L1 are handled by the ADL loader (see §4). L4b–L6 belong
to downstream verification (see §5.8).
The following table shows the L2–L4a rules implemented in the piki prototype for telecom rack
scenarios:
       Table 4: L2–L4a rules implemented in the piki prototype for telecom rack scenarios

   Rule ID           Name                      Layer                   Description
   INTERFACE-        Interface type            L2                      Mate interface types
   COMPAT-001        compatibility                                     must match
   POWER-001         Rack PDU power            L3                      PDU load must not
                     budget                                            exceed capacity
                                                                       threshold
   TELECOM-          U-position conflict       L3                      Device U-positions
   RACK-001                                                            within the same rack
                                                                       must not overlap
   TELECOM-          Rack capacity             L3                      Total device height
   RACK-002                                                            must not exceed rack
                                                                       available U-positions




                                                17
   Rule ID           Name                    Layer                    Description
   TELECOM-          Intra-rack 3D collision L4a                      AABB-based spatial
   COLLISION-                                                         conflict detection
   001
   TELECOM-          Rack load bearing       L3                       Total weight must not
   WEIGHT-001                                                         exceed rack load
                                                                      capacity
   TELECOM-          Maintenance aisle       L4a                      Same-row rack spacing
   FLOOR-002         width                                            must meet
                                                                      maintenance aisle
                                                                      requirements


Rules are registered via the @rule(rule_id, name, priority, severity) decorator. Layered
registration allows projects to enable only L2 during logical design, and add L3–L4a during
detailed layout phase.

5.5     Waiver Mechanism
The structured waiver system is part of ESA’s design; the current piki prototype only supports
--skip <rule_id> and warning_only configuration. The target design records each waiver as
a YAML file containing the following fields:

                             Table 5: Structured waiver file fields

      Field          Meaning                               Example
      rule_id        The waived rule                       TELECOM-FLOOR-002
      target         Affected objects                      RACK-A01, RACK-A02
      scope          Scope (single file, branch, global)   branch:feature/legacy-room
      rationale      Technical and business                “Constrained by existing building
                     justification                         column grid”
      author         Requester                             Engineer ID
      approver       Authorizer                            Senior engineer / compliance lead
      expires_at     Expiration (optional)                 2027-06-20
      downstream_-   Downstream reinforced                 ["CFD-thermal-sim",
      tasks          verification tasks                    "site-survey"]
      created_at /   Audit trail                           Timestamp and Git hash
      commit


Waivers are committed alongside ADL files and reviewed in PRs. A waiver is not a bypass
of the rule—it is a transfer of responsibility from the deterministic rule engine to higher-cost
verification activities. If downstream tasks fail, the waiver is reconsidered.

5.6     Diagnostic Output
ESA produces a unified diagnostic structure consumable by terminals, CI dashboards, IDEs,
and PR bots. On the telecom rack sample, piki check completes in under 200ms on a laptop,
returning 1 warning and 29 passes:
[PASS] INTERFACE-COMPAT-001: Interface type compatibility check
...


                                               18
[FAIL] TELECOM-FLOOR-002: Rack maintenance aisle width check
       Racks RACK-A01 and RACK-A02 same-row spacing -600.0mm is less than required 600.0mm
============================================================
Total: 0 errors, 1 warning, 29 passed
============================================================
The JSON format exposes the same data, is LSP-compatible, and can drive terminal summaries,
JUnit XML dashboards, IDE overlays, and GitHub Checks API annotations.

5.7   CI/CD and Pre-commit Integration
ESA is designed to run within workflows that software engineers already use. A typical EaC
CI/CD pipeline consists of the following stages:

                    Table 6: EaC CI/CD pipeline stages and failure policies

   Stage            Trigger                  Content                   Failure Policy
   Lint             Per commit               YAML/TOML                 Block commit
                                             formatting, trailing
                                             whitespace, naming
                                             conventions
   Parse            Per commit               ADL syntax (L0)           Block merge
   Schema Check     Per commit               pydantic / JSON           Block merge
                                             Schema (L1)
   Link Check       Per PR                   Reference integrity,      Block merge
                                             Mate consistency (L2)
   Rule Check       Per PR                   Business and              Block merge
                                             lightweight geometry
                                             rules (L3–L4a)
   Artifact Build   Post-merge               BOM, drawings, port       Report warning
                                             maps
   Nightly          Scheduled                Full sample suite,        Report and notify
   Regression                                geometry, CAE/CFD


Pre-commit hooks mirror the cheaper checks locally, giving engineers sub-second feedback before
commit. The same configuration file drives both pre-commit and CI, preventing “passes locally,
fails CI” inconsistencies.

5.8   Downstream Verification Protocol: ESA’s Boundary
ESA’s scope is intentionally limited to checks that can be performed deterministically from
declarations alone. It covers L2–L3 (core) and L4a (lightweight geometry extension). L0–L1 are
handled by the ADL loader. L4b (precise geometric clash detection, requiring a CAD kernel),
L5 (physical simulation, requiring CAE/CFD solvers), and L6 (human/expert sign-off) belong
to downstream verification—critical to engineering correctness, but not part of ESA.
The integration of these downstream stages follows a protocol that is an architectural proposition
of the EaC workflow architecture, not a feature of the current piki prototype:
  1. Trigger. After piki check passes, CI Pipeline Actions invoke downstream tools—
     exporting ADL declarations as STEP/USD and running precise clash detection (L4b)
     with a CAD kernel, or generating mesh files and invoking CFD/FEA solvers (L5).


                                               19
    2. Feedback loop. Downstream findings flow back into the ADL project in a Diagnostic for-
       mat compatible with ESA, referencing specific Instance, LayoutEntry, or Mate identifiers.
       This means downstream tools only need to produce structured diagnostic output; they do
       not need to understand ADL internals.
    3. Separation of concerns. Downstream findings do not feed back into the ESA rule library.
       They form independent L4b/L5 diagnostic collections, just as SPICE simulation results
       and DRC reports are independent, complementary verification channels in chip design.
       Waivers based on downstream findings reference downstream diagnostics, not ESA rule
       IDs.
This protocol defines the interface between EaC’s design-time verification and the broader
physical verification ecosystem. It does not require piki to be a CAD or CAE platform; it
requires piki to produce consumable outputs and a standardized diagnostic envelope.


6     Evaluation
This chapter reports evaluation results. All sample inspections and the violation-injection ex-
periment are complete; SD-HWE-Bench is in the design phase.

6.1    Research Questions and Methodology
We answer three research questions:
    • RQ1. Can ADL express real engineering designs in a text-native, machine-checkable form?
    • RQ2. Can ESA detect common design violations at design time, satisfying CI/CD gating
      requirements with a higher signal-to-noise ratio than geometry-based ACC?
    • RQ3. Does the representation provide the verifiable reward signal required for RLVR-style
      agent training?
The evaluation uses sample projects from the piki repository and a controlled violation-injection
experiment. Metrics include:
    1. Expressiveness: Whether each sample can be fully declared in ADL;
    2. Check latency: Time for piki check to complete L0–L4a verification;
    3. Rule coverage: Number and type of applicable rules;
    4. Detection accuracy: Whether ESA identifies deliberately injected violations in seman-
       tically plausible configurations without false positives;
    5. Deliverable generation: Whether downstream artifacts (BOM, panel view, port map-
       ping, cable manifest) can be produced.
All measurements are taken on a laptop-class machine with a hot cache; latency reported as the
median of five runs.

6.2    Sample Projects
Table 7 summarizes the status of the three samples in the piki repository.

                              Table 7: Status of piki sample projects

 Sample           Domain          ADL files       Applicable rules   Status            Expected by
                                                                                       submission
 01-telecom-      Telecom rack    42              30                 Pass (1           Complete
 expansion        expansion                                          warning)
 02-modular-      Modular         38              34                 Pass (0 errors)   Complete
 datacenter       containerized
                  datacenter


                                                20
 Sample            Domain          ADL files      Applicable rules   Status            Expected by
                                                                                       submission
 03-mechanical-    Mechanical      29             28                 Pass (0 errors)   Complete
 keyboard          keyboard
                   assembly


Sample 01: Telecom Rack Expansion. This is the most mature sample. It declares two
cabinets, multiple servers, PDUs, switches, optical modules, and fiber connections. piki check
passes all L2–L4a rules, producing 1 warning: the aisle width between RACK-A01 and RACK-A02
is below the required 600mm. This sample demonstrates full ADL expressiveness, sub-200ms
feedback latency, and the generation of 10 downstream artifacts (BOM, cabinet panel views,
port mapping, cable manifest, etc.).
Sample 02: Modular Datacenter. This sample tests container-level power and cooling. The
sample passes all L2–L4a checks (13 passes, 0 errors). Three root causes were fixed: (1) a
LAYOUT-001 empty-string falsy-check defect — absolute_fields mistook "" for a valid value;
(2) the lowering pass lacked transform field parsing — relative coordinates declared in YAML
were dropped in the compilation pipeline; (3) a cooler position data issue — an incorrect half-
height calculation caused a collision with a GPU. The sample’s pass demonstrates the suﬀiciency
of PLL relative-skeleton modeling and container-level coordinate chains, as well as the successful
extension of ADL expressiveness from the telecom domain to containerized infrastructure.
Sample 03: Mechanical Keyboard. This sample demonstrates skeleton-based assembly
modeling across the consumer electronics domain: CASE-01 serves as the assembly root, with
PCB, plate, battery, switches, keycaps, and stabilizers declared through parent-transform chains.
The sample passes all L2–L4a checks (27 passes, 0 errors). After fixing the LAYOUT-001 empty-
string falsy-check defect, all entries in the continuous 2D grid layout parsed correctly. The
sample’s pass provides evidence for the cross-domain generalizability of the three-layer ADL
architecture, extending from telecom through datacenter infrastructure to consumer electronics.

6.3    Violation-Injection Experiment
To test ESA’s detection accuracy and conduct a structural comparative analysis against model-
based ACC, we performed a controlled violation-injection experiment on the telecom sample.
Experimental design. Fifteen known violations were injected into correct ADL declarations,
covering four categories:
                  Table 8: Categories of injected violations in the telecom sample

      Category         Count                               Example
      L2: Interface    4                                   SFP28 optical module paired with
      mismatch                                             SFP+ port
      L2: Reference    3                                   Mate referencing a non-existent
      integrity                                            Instance
      L3: Power        4                                   PDU output overload exceeding
      budget                                               rated capacity
      L3: Spatial      2                                   Two servers assigned to
      conflict                                             overlapping U slots
      L4a: Aisle       2                                   Cabinet spacing below
      clearance                                            maintenance-aisle minimum


piki check was then run for ESA inspection.

                                                21
Results:
   1. ESA detection rate: 15/15 violations detected (100%), with zero false positives — be-
      cause ESA checks semantic categories (Family types, Mate relations) rather than geometry.
   2. Check latency: piki check completes L0–L4a verification across all 30 rules within
      200ms (laptop, hot cache, median of five runs).

6.3.1    Structural Comparison with ACC
We did not conduct a quantitative comparison experiment against ACC tools, because such a
comparison is of limited significance under current technical conditions and is diﬀicult to execute.
There are three reasons.
L2 semantic violations are structurally unreachable for ACC. Seven of the fifteen viola-
tions belong to the L2 category — interface type mismatches and reference-integrity violations.
Detecting these violations depends on the Part Family type system and Mate relation decla-
rations, information that simply does not exist in IFC geometry models. Regardless of how
mature an ACC tool (Solibri Model Checker, Navisworks, or an academic prototype) may be, it
cannot inspect attributes that are not encoded in the input representation. This is not a matter
of precision — it is a matter of representational boundaries.
The signal-to-noise ratio difference in spatial violation detection is qualitative. ESA
has access to the design intent behind spatial relations. Mate relations distinguish expected
device compatibility (a server inserted into a cabinet) from genuine spatial conflicts (two devices
occupying overlapping U slots). ESA’s advantage lies not in running faster, but in the fact
that its input representation captures semantics that ACC must reverse-engineer from geometry
models.
The lack of a standardized evaluation benchmark in the ACC community is itself a
symptom of the representation-layer problem. After fifteen years of ACC research, the
field still lacks a standardized evaluation benchmark comparable to SWE-bench or VerilogEval.
ACC’s inputs — IFC/BIM models — are highly heterogeneous: naming conventions, modeling
habits, and LOD vary by project, and regulatory frameworks vary by region. Every evaluation
requires customized remodeling and rule adaptation. This precisely validates the central thesis
of this paper: when design intent is trapped in geometry, not only do agents lack training signal,
but even basic human evaluation reproducibility becomes diﬀicult.
ESA’s violation-injection experiment requires no such customization. The fifteen violations were
injected via semantically clear YAML edits in ADL declarations, and piki check provided a
unified, reproducible scoring function. The same violation-injection methodology can be applied
to any sample that follows the three-layer ADL architecture — as already demonstrated by the
cross-domain portability of samples 02 and 03 — because rules are indexed by Family types
rather than project-specific naming patterns.
This comparison directly validates the core claims in §2.2.1 and §5.1: ESA’s advantage stems
from the fact that it inspects design declarations rather than geometric instantiation artifacts.
The reliance on remodeling and the false positives from pure geometry collision detection are not
implementation defects of ACC — they are fundamental limitations of its input representation.

6.4     SD-HWE-Bench: Agent Evaluation Benchmark [Design Phase]
The pilot and violation-injection experiments validate feasibility and detection accuracy, but
do not test whether agents can generate ADL from natural-language requirements. We are
designing SD-HWE-Bench to fill this gap. It will be reported in a companion paper; its
design is described here for reviewers to evaluate the larger evaluation plan.


                                                22
Task paradigm:
Input: Natural-language engineering requirements
Output: Structured ADL declarations (piki YAML)
Scoring: L0–L4 rule-check pass rate + deliverable quality + L6 sign-off assessment
Unlike SWE-bench — which tests patch generation on existing codebases (Jimenez et al. 2024)
— SD-HWE-Bench tests creation from scratch, because declarative engineering design does not
yet exist at scale as a practice.
Initial domain: Telecom rack deployment. This domain was chosen because:
   • The space is discrete (rack U slots), avoiding continuous 3D constraint solving;
   • Constraints are primarily algebraic (power budget, weight, U-slot conflicts);
   • Interface types are enumerable (SFP28, RJ45, IEC-C13/C14);
   • piki check completes in approximately 200ms, satisfying RLVR’s need for fast reward
     signals.
Planned metrics:
                      Table 9: Planned SD-HWE-Bench evaluation metrics

      Metric                                    Definition
      Pass@1                                    Percentage where the first ADL output
                                                passes all enabled rules
      Pass@k                                    Percentage with at least one pass over k
                                                samples
      Latency                                   Median piki check time per output
      Coverage                                  Coverage of task requirements in the
                                                generated ADL
      Human sign-off                            Percentage deemed acceptable by domain
                                                experts (L6 agent)


Connection to RQ3. SD-HWE-Bench directly tests the RLVR causal chain: if ADL + ESA
provides a structured, deterministic reward signal, then agents trained with this signal should
outperform those without it. This is prediction P1 of the information representation hypothesis
(§3.2.2). Benchmark design is complete; task authoring and baseline agent experiments are in
progress.

6.5    Cross-Domain Validation
Samples 02 and 03 serve a dual purpose: they are both current capability boundary records and
cross-domain validation targets. Their passage before the submission deadline will demonstrate
that the three-layer ADL architecture and ESA rule engine are not telecom-domain special cases.

         Table 10: Cross-domain validation samples and the ADL features they exercise

      Sample          Domain                            Key cross-domain property tested
      02-modular-    Containerized infrastructure       Container-relative layout,
      datacenter                                        multi-subsystem power/cooling
      03-mechanical- Consumer electronics               Skeletal assembly hierarchy,
      keyboard                                          parent-transform-chain-based
                                                        Mate


                                              23
Both samples have passed their respective L2–L4a checks (Sample 02: 13 passes; Sample 03: 27
passes), providing evidence that ADL’s Part/Mate/Layout abstractions transcend the telecom
domain.

6.6     Evaluation Summary
Table 11 summarizes the current status and expected status at submission time.
                     Table 11: Evaluation status and submission expectations

      Component       Current status                     Expected by submission
      Sample 01       Complete                           Complete
      (Telecom)
      Sample 02       Complete (0 errors, 13 passes)     Complete
      (Datacenter)
      Sample 03       Complete (0 errors, 27 passes)     Complete
      (Keyboard)
      Violation-      Complete                           15/15 violations detected (100%),
      injection                                          0 false positives
      experiment
      SD-HWE-         Design complete, task authoring    Task suite specification complete;
      Bench           in progress                        agent experiments deferred to
                                                         companion paper


The evaluation framework is in place. All three samples passing L2–L4a checks marks the
completion of cross-domain validation for ADL expressiveness and ESA detection capability.
The violation-injection experiment verified ESA’s design-time detection accuracy with 100%
detection rate and zero false positives, and the structural analysis in §6.3.1 demonstrates ESA’s
semantic advantages over model-based ACC. The SD-HWE-Bench design is in place; agent
experiments are deferred to the companion paper. We commit to delivering the full evaluation
before the October 2, 2026 submission deadline.


7     Related Work
This chapter situates EaC within five research threads: RLVR training methodology, engineering
domain benchmarks, declarative modeling and formal methods, AI4E implementation paths, and
Infrastructure as Code.

7.1     RLVR Methodology
EaC’s information representation hypothesis is directly anchored in the RLVR literature.
DeepSeek-R1 demonstrated that Group Relative Policy Optimization (GRPO) with deter-
ministic verification signals yields powerful reasoning improvements (DeepSeek-AI 2025).
SWE-RL showed that test suite feedback alone is suﬀicient to train effective code-repair agents
(SWE-agent contributors 2025). Multi-SWE-bench extended this paradigm to multi-language
settings, validating its cross-linguistic generality (ByteDance Seed 2025). These works establish
the latter half of the RLVR causal chain; EaC addresses the former half — RLVR cannot boot
without structured representations.

7.2     Engineering AI Benchmarks and Automated Compliance Checking
Existing engineering AI benchmarks occupy different positions in the matrix.

                                               24
AEC-Bench evaluates AI reviewing human-created drawings — sitting at the intersection of
ACC philosophy and AI capability assessment, but does not test design generation capabilities
(Galanos and Mulyar 2026). EngDesign spans multiple design disciplines, but evaluates models
on tasks defined within existing CAD/BIM workflows, without requiring a “Design as Code”
intermediate representation (EngDesign contributors 2025).
EDA benchmarks (VerilogEval (M. Liu et al. 2023), ChipBench (ChipBench contributors
2025), AMS-IO-Bench (Liu et al. 2025)) have already benefited from a “Circuit as Code” foun-
dation, exhibiting high RLVR compatibility; their performance levels provide an upper-bound
reference for the targets SD-HWE-Bench aims to reach once “Design as Code” foundations are
established in traditional engineering domains. Rule2DRC further validates the “executable ver-
ification” philosophy — rules as executable checks rather than passive constraints — aligning
with SD-HWE-Bench’s L0–L4 design (Kim et al. 2026).
The Automated Compliance Checking (ACC) community has continuously advanced com-
pliance automation through ACC tools (Eastman et al. 2009; Zhang and El-Gohary 2019), and
recent efforts leveraging LLMs for regulation-to-rule translation (Fuchs et al. 2024; Yang and
Zhang 2024; Nakhaee et al. 2024). However, these methods still operate downstream — after
design completion rather than at design time. As argued in §2.2.1, model-based ACC also suf-
fers from two structural deficiencies — geometric collision false positives and name-dependent
copy mapping — whose root cause lies in the semantic limitations of geometric representations
themselves.

7.3   Declarative Modeling and Formal Methods
SysML v2 provides a rich systems engineering modeling framework with part/occurrence
separation, connection/interaction relationships, and repository-based version control (Ob-
ject Management Group 2024). Yet the methodological divergence from ADL is fundamental:
SysML v2 targets human GUI modeling, with the source of truth in a model repository and
verification via model checking; ADL targets agent-human textual collaboration, with the source
of truth in YAML files and verification via a layered ESA rule engine enforced before commit.
This is isomorphic to the division of labor between Verilog netlists and circuit schematics.
BIM/IFC uses the IFC exchange format and geometry-centric models as an interoperability
layer (buildingSMART International 2023). However, IFC couples identity, geometry, and re-
lationships in a graph that allows multiple equivalent serializations, making line-level version
control diﬀicult (H. Liu et al. 2023). ADL inverts this relationship: text is the source of truth,
and CAD/BIM are downstream consumers.
IaC provides the closest conceptual analogy from the software domain, but operates on infras-
tructure states that are already digital-native (Morris et al. 2022; Quattrocchi and Tamburri
2023). Chiari et al.’s empirical study of IaC static analysis (Chiari et al. 2024) directly supports
EaC’s feasibility argument of “X as Code + static analysis.”

7.4   AI4E Implementation Paths
Current AI4E efforts follow two main implementation paths:
  • CUA (Computer-Using Agent): Having AI operate CAD software through GUIs. This
    path faces limitations in interface interaction fragility, absence of verification signals, and
    diﬀiculty in large-scale trial-and-error.
  • CAD-MCP: Wrapping structured tool interfaces on top of CAD software. While more
    stable than CUA, it remains bound to proprietary CAD kernels and does not address the
    design source-of-truth problem.


                                                25
EaC takes a methodologically opposite approach to both paths: placing computable engineering
descriptions at the center, and making CAD/CAE tools downstream consumers and renderers
of that description. CUA and CAD-MCP are patches to existing toolchains; EaC rebuilds from
the representation layer, enabling agents to directly operate on a computable design source of
truth.

7.5    Systematic Comparison of Related Work
The following table systematically compares EaC with major related works across dimensions
including source-of-truth modality, version control granularity, verification timing, and agent-
friendliness:
                      Table 12: Systematic comparison of EaC with related work

Dimension        ACC           CUA          CAD-MCP      BIM/IFC       SysML v2       EaC (This
                                                                                      Work)
Source of        CAD/BIM       CAD GUI      CAD kernel   Central       Model          Text file
Truth            model                                   model file    repository     (YAML)
Verification     Post-design   None         Tool-level   Post-design   Model-level    Design-time
Timing                                                                                (ESA)
Verification     Seconds to    N/A          Tool-        Minutes       Model-         Milliseconds
Speed            minutes                    dependent                  checking level
Version          File-level    File-level   File-level   Model version Model version Git
Control                                                                               line-level
Agent            No            Indirect     Partial      No            Partial        Yes
Friendliness                                                                          (first-class)
Quality          No (endpoint) No           No           No (endpoint) Partial        Yes (full
Shift-Left                                                                            spectrum)
Part Reuse       Ad hoc        No           No           Limited       Partial        Future Work
RLVR             No            No           No           No            Partial        Yes
Compatibility                                                                         (L0–L4a,
                                                                                      second-
                                                                                      level)
Check            Naming        N/A          Tool API     Property sets Model          Family type
Semantic         convention                                            elements       system
Layer
False Positive   None (pure    N/A          N/A          None (pure    Partial        Mate
Suppression      geometry)                               geometry)                    relationship
                                                                                      exclusion



8     Conclusion
This paper proposes the Engineering as Code (EaC) paradigm: migrating engineering design
from a GUI-centric WYSIWYG mode to one where textual declarations serve as the source of
truth, rule engines act as quality gates, and version control and package management form the
collaboration substrate.
The three core contributions of this paper are as follows:
    1. The ADL Design Language. An assembly definition language with Part as the atomic
       unit and PDL/PML/PLL as three orthogonal sub-languages at its core. ADL clarifies
       the syntactic and semantic boundaries of each layer, enabling engineering design intent to
       be expressed in a text-native declarative form and directly integrated with Git, CI, and
       LSP-style diagnostics. Through parameterized degrees-of-freedom completion and skele-
       tal modeling mechanisms, PLL enables mate constraint solving and assembly hierarchy
       management to coexist orthogonally within the same framework.



                                                  26
  2. The ESA Verification Mechanism. Shifts compliance rules from downstream post-hoc
     ACC review upstream to the design generation stage. Unlike model-based ACC — which is
     hampered by structural deficiencies such as geometric collision false positives and naming-
     dependent model recreation — ESA checks design declarations rather than geometrically
     instantiated artifacts, and can therefore operate rules at the semantic category level with-
     out relying on project naming conventions. Four operational guidelines are given: rule
     waivability, focusing on baseline rules, purifying collaboration signal-to-noise ratio, and
     AI-assisted rule library construction. The CI/CD Action integration protocol for L4b–L6
     downstream verification is defined — this protocol serves as the integrity statement of the
     EaC workflow architecture, ensuring that ESA’s deterministic boundary and the compre-
     hensive verification ecosystem required by physical engineering are complementary rather
     than conflicting.
  3. The Information Representation Hypothesis. Systematically argues that the root
     cause of the engineering AI bottleneck lies not in insuﬀicient model capability, but in the
     long-standing absence of a “Design as Code” form of computable foundation in traditional
     engineering domains. ACC’s false positives and model-recreation overhead serve as con-
     crete evidence for this thesis: when design intent is trapped inside geometric models, not
     only is AI unable to obtain training signals, but even human engineers’ automated checks
     fail at the semantic level.
The piki prototype validates ADL’s expressiveness and ESA’s detection capability on three
samples (69 total rules passed, <200ms latency): telecom rack expansion (0 errors, 1 warning,
29 passed), modular containerized data center (0 errors, 13 passed), and mechanical keyboard
assembly (0 errors, 27 passed). Violation injection experiments were completed with 100%
detection rate and zero false positives. The design of the SD-HWE-Bench evaluation benchmark
has been completed, serving as an empirical testing platform for the Information Representation
Hypothesis.
Future work includes: improving the geometric solving precision of continuous DOF in PLL and
extending it to 1D continuous path topologies such as pipelines/cables; exploring the design space
of engineering package management and assembly registries (EPM/AssemblyHub); validating
ADL and ESA’s expressive capability across more engineering domains; and conducting RLVR
training experiments to directly test the Information Representation Hypothesis.
The core message of this paper is: physical engineering needs source code. Not better CAD, not
smarter review tools, but something that does for engineering design what hardware description
languages did for chip design — a representation that liberates design intent from geometric
implementation, making it operable by software engineering infrastructure. This is exactly
what EaC provides.
Anthropic. 2025. Claude Code Overview. Technical documentation; Anthropic. https://docs
   .anthropic.com/en/docs/claude-code/overview.

buildingSMART International. 2023. Industry Foundation Classes (IFC) 4.3.2.0 Specification.
   Specification; buildingSMART International. https://technical.buildingsmart.org/st
   andards/ifc/ifc-schema-specifications/.

ByteDance Seed. 2025. “Multi-SWE-bench: a multilingual benchmark for issue resolving.”
  arXiv:2504.02605. https://arxiv.org/abs/2504.02605.

Chiari, Michele, Bin Xiang, Gerardo Canfora, and Massimiliano Di Penta. 2024. “An empirical
   study of static analysis tools for infrastructure as code.” Empirical Software Engineering 29
  (3): 1–42. https://doi.org/10.1007/s10664-023-10407-1.


                                               27
ChipBench contributors. 2025. “ChipBench: a next-step benchmark for evaluating LLM perfor-
   mance in AI-aided chip design.” arXiv:2503.04807. https://arxiv.org/abs/2503.04807.

Cousot, Patrick, and Radhia Cousot. 1977. “Abstract interpretation: a unified lattice model
   for static analysis of programs by construction or approximation of fixpoints.” Proceedings
  of the 4th ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages
  (POPL), 238–52. https://doi.org/10.1145/512950.512973.

DeepSeek-AI. 2025. “DeepSeek-R1: incentivizing reasoning capability in LLMs via reinforcement
   learning.” arXiv:2501.12948. https://arxiv.org/abs/2501.12948.

Eastman, Charles, Jae-Min Lee, Yeon-Suk Jeong, and Jin-Kook Lee. 2009. “Automated code
   checking: status and future directions.” Automation in Construction 18 (2): 101–15. https:
   //doi.org/10.1016/j.autcon.2008.07.001.

EngDesign contributors. 2025. “EngDesign: a comprehensive benchmark for engineering design
  with large language models.” arXiv:2505.18116. https://arxiv.org/abs/2505.18116.

Fowler, Martin. 2010. Domain-specific languages. Addison-Wesley Professional. https://mart
   infowler.com/books/dsl.html.

Fuchs, Stefan, Michael Witbrock, Johannes Dimyadi, and Robert Amor. 2024. “Using large
   language models for the interpretation of building regulations.” arXiv:2407.21060. https:
   //arxiv.org/abs/2407.21060.

Galanos, Theodoros, and Alexander Mulyar. 2026. “AEC-Bench: an AI benchmark for archi-
   tecture, engineering, and construction.” arXiv:2505.09010. https://arxiv.org/abs/2505
   .09010.

Hudak, Paul. 1996. “Building domain-specific embedded languages.” ACM Computing Surveys
  28 (4es): Article 196. https://doi.org/10.1145/242224.242477.

IEEE. 2005. IEEE Standard for Verilog Hardware Description Language. Standard IEEE Std
   1364-2005. IEEE Standards Association. https://standards.ieee.org/standard/1364
   -2005.html.

Jimenez, Carlos E. et al. 2024. “SWE-bench: can language models resolve real-world GitHub
   issues?” The Twelfth International Conference on Learning Representations (ICLR). https:
   //openreview.net/forum?id=VTF8yNQM66.

Kim, Jinuk, Junsoo Byun, Donghwi Hwang, Seong-Jin Park, and Hyun Oh Song. 2026.
  “Rule2DRC: benchmarking LLM agents for DRC script synthesis with execution-guided test
   generation.” Proceedings of the 43rd International Conference on Machine Learning (ICML
  2026) (Seoul, South Korea). https://arxiv.org/abs/2605.15669.

Lightman, Hunter et al. 2023. “Let’s verify step by step.” arXiv:2305.20050. https://arxiv.
   org/abs/2305.20050.

Liu, Bingqing et al. 2025. “AMS-IO-Bench: a large-scale benchmark for analog/mixed-signal
   I/O ring design.” arXiv:2504.19197. https://arxiv.org/abs/2504.19197.




                                             28
Liu, Han, Ge Gao, and Ming Gu. 2023. “A parallel IFC normalization algorithm for incremental
   storage and version control.” Proceedings of the 30th International Workshop on Intelligent
   Computing in Engineering (EG-ICE 2023), 511–20. https://arxiv.org/abs/2312.14931.

Liu, Mingjie, Nathaniel Pinckney, Brucek Khailany, and Haoxing Ren. 2023. “VerilogEval:
   evaluating large language models for Verilog code generation.” Proceedings of the 42nd
   IEEE/ACM International Conference on Computer-Aided Design (ICCAD). https://doi.
   org/10.1109/ICCAD57390.2023.10323811.

Maatouk, Ali, Nicola Piovesan, Fadhel Ayed, Antonio De Domenico, and Mérouane Debbah.
  2023. “TeleQnA: a benchmark dataset to assess large language models’ telecommunications
  knowledge.” arXiv:2310.15051. https://arxiv.org/abs/2310.15051.

Mirhoseini, Azalia et al.   2020.  “Chip placement with deep reinforcement learning.”
   arXiv:2004.10746. https://arxiv.org/abs/2004.10746.

Morris, Kief et al. 2022. Infrastructure as code: dynamic systems for the cloud age. 2nd ed.
  O’Reilly Media. https://www.oreilly.com/library/view/infrastructure-as-code/97
  81098114664/.

Nakhaee, Amirreza et al. 2024. “A hybrid knowledge-graph-LLM framework for automated
  compliance checking in building design.” Proceedings of the 30th International DMS Confer-
  ence on Visualization and Visual Languages (DMSVIVA 2024). https://doi.org/10.100
  7/978-3-031-63227-2_12.

Object Management Group. 2024. OMG Systems Modeling Language (SysML) Version 2.0.
  Specification; Object Management Group. https://www.omg.org/spec/SysML/.

Quattrocchi, Giovanni, and Damian A. Tamburri. 2023. “Infrastructure as code: a survey of
  research and practice.” IEEE Software 40 (5): 55–62. https://doi.org/10.1109/MS.202
  3.3285751.

Shao, Zhihong et al. 2024. “DeepSeekMath: pushing the limits of mathematical reasoning in
   open language models.” arXiv:2402.03300. https://arxiv.org/abs/2402.03300.

SWE-agent contributors. 2025. “SWE-RL: training language model agents to solve real-world
  GitHub issues via reinforcement learning.” arXiv:2502.18449. https://arxiv.org/abs/25
  02.18449.

Völter, Markus, Thomas Stahl, Jorn Bettin, Arno Haase, and Simon Helsen. 2013. Model-
   driven software development: technology, engineering, management. John Wiley & Sons.
   https://www.wiley.com/en-us/Model+Driven+Software+Development%3A+Technology%
   2C+Engineering%2C+Management-p-9781118725764.

Xiao, Zixuan, Pei Troh Koh, Jun Ma, and Jack C. P. Cheng. 2025. “Automating geometry-
   intensive compliance checking in BIM: graph-based semantic reasoning framework.”
   arXiv:2506.20551. https://arxiv.org/abs/2506.20551.

Yang, F., and J. Zhang. 2024. “Large language model-driven prompt-based automation for
   building code compliance checking.” Automation in Construction 160: 105310. https:
   //doi.org/10.1016/j.autcon.2024.105310.


                                             29
Zhang, Ruichuan, and Nora M. El-Gohary. 2019. “A machine-learning approach for semantic
   matching of building codes and BIMs for supporting automated code checking.” Proceedings
   of the 2019 ASCE International Conference on Computing in Civil Engineering (Atlanta,
   GA, USA). https://doi.org/10.1061/9780784482421.056.




                                            30
