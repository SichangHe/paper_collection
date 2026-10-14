                                                     Metamodel-Guided Model Generation with Layered
                                                                      Constraints

                                                Tong Ma1,2 , Hui Lai1 , Hui Wang3 , Zhenhu Tian3 , Chaochao Li2*, Fengjie Xu2*,
                                                                                  Ling Fang2*
                                                                 1
                                                                   University of Science and Technology of China,Hefei,China.
                                                     2
                                                         Hefei Institutes of Physical Science, Chinese Academy of Sciences,Hefei,China.
                                                                                  3
                                                                                    Anhui University,Hefei,China.
arXiv:2510.25890v4 [cs.SE] 22 Sep 2026




                                                                      *Corresponding author(s). E-mail(s): fangl@hfcas.ac;
                                                                        Contributing authors: matong@mail.ustc.edu.cn;


                                                                                                    Abstract
                                              Large language models (LLMs) enable natural-language interaction in engineering modeling, but generated mod-
                                              els may violate structural constraints, domain rules, or task requirements. We propose a metamodel-guided model
                                              generation method that coordinates generation-time constraints and post-generation validation. The method trans-
                                              forms metamodel information, uses its terminology to guide structured constraint extraction from specifications,
                                              and links constraints to metamodel elements while recording their sources in an Integrated Constraint Model
                                              (ICM). For each task, relevant constraints are bound to concrete objects, values, and references. The generation-
                                              time constraint layer (L1) restricts candidate content. The post-generation validation layer (L2) checks constructed
                                              models and serialized artifacts, and task acceptance checks retain the original requirements throughout repair.
                                              Deterministic procedures construct and serialize models, while LLMs propose candidate content and repairs.
                                              Validation uses existing domain tools and checkers written by humans with LLM assistance. Experiments cover
                                              AUTOSAR, railway models, and structured decisions in private international law. All 60 AUTOSAR generation
                                              runs passed acceptance within the declared task scope, and all 255 resulting ARXML files passed XSD valida-
                                              tion. In a separate controlled AUTOSAR repair experiment, all 85 core fault units and 15 prespecified substitute
                                              units were restored within one repair round. A local AUTOSAR experiment recorded interventions during step-
                                              wise generation. The results support coordinating generation constraints, domain checks, and task acceptance to
                                              construct models and guide bounded repair.

                                              Keywords: Model-driven engineering; Large language models; Metamodels; Layered constraints; Integrated Constraint Model




                                         1 Introduction                                                     Their metamodels define the abstract syntax of mod-
                                                                                                            els, including element types, attributes, inheritance,
                                         Model-driven engineering (MDE) treats models as                    containment, references, and relationship multiplic-
                                         primary artifacts in software and systems develop-                 ities. Well-formedness constraints specify additional
                                         ment. Explicit modeling languages, model transforma-               conditions that valid models must satisfy. Model trans-
                                         tions, and analysis tools support design, validation,              formations connect different levels of abstraction and
                                         and implementation. Domain-specific modeling lan-                  representations and support the generation of code and
                                         guages express problems in terms of domain concepts.               other artifacts from models [1]. These mechanisms



                                                                                                        1
define the artifacts on which automated operations act             This modeling information is usually distributed
and the criteria against which they are checked.                across different sources. The metamodel provides
   Large language models (LLMs) allow users to spec-            structural information such as types and relationships.
ify modeling requirements in natural language and               Natural-language specifications add conditions involv-
obtain suggestions for model elements, relationships,           ing multiple elements, logical dependencies, applica-
and attribute values. Recent studies have applied LLMs          bility conditions, and exceptions. The task determines
to domain modeling, model instance generation, inter-           what must be constructed and retained. Generation
active completion, and the transformation of modeling           may also depend on the existing model context, which
artifacts, combining natural-language interaction with          comprises objects in the current model that can be
established MDE tools [2]. However, a linguistically            referenced or must be preserved, together with their
plausible response is not necessarily a model that mod-         attributes and relationships. For example, generation
eling tools can accept. A generator must respect types,         should account for the runnable entity R and its con-
required features, nested structures, multiplicities, and       taining internal behavior, as well as interfaces and their
references. It must also meet the complex semantic and          paths already defined in the component model. Includ-
logical requirements in specifications, as well as task-        ing all this information in a prompt does not make the
specific requirements concerning objects, values, and           corresponding constraints executable.
connections. As models become more complex, these                  Decoding constructs an LLM’s output by selecting
requirements increasingly interact during generation.           successive tokens, which are units of text such as sub-
   Structural correctness is itself a substantial part          words and punctuation. Constrained decoding restricts
of this challenge. In AUTOSAR, for example, the                 these choices according to executable constraints.
ARXML representation of a software component                       Previous studies have introduced explicit knowledge
model has multiple levels of nesting, different refer-          at different stages of generation. Synchromesh com-
ence types, and element ordering requirements speci-            bines retrieval with constrained semantic decoding to
fied by XML Schema. Incorrect containment, missing              enforce syntax, type, and selected contextual rules as
required elements, or references of the wrong type              the output is constructed [4]. AbsCon aggregates mul-
can prevent an artifact from being used in downstream           tiple candidate graphs into a probabilistic partial model
tools. If JSON is used as an intermediate representation        and then uses the metamodel and well-formedness
during generation, its correspondence with the domain           constraints to solve for a consistent model [5]. EMF-
model must be preserved, and serialization must sat-            Kaizen uses the metamodel and the current model to
isfy the target format requirements. For example, when          recommend model fragments interactively [6]. These
model features are represented as JSON object prop-             studies show that constraints can guide generation and
erties, the written order of those properties does not          support candidate checking and selection. For tasks
enforce the element order required by XSD [3]. The              involving both complex structures and domain logic,
serialization mapping must enforce this order, and              a key question is how to coordinate two complemen-
validation must check it in the resulting artifact.             tary capabilities. Generation-time restrictions should
   Structural requirements, domain rules, and task              exclude invalid structures and values where possible.
requirements address different concerns. Consider a             Post-generation checks should address requirements
task that requires a timing event to trigger an exist-          that depend on complete objects, relationships across
ing runnable entity R every 10 ms. A runnable entity            elements, or target artifacts.
represents software behavior that can be triggered for             We propose a metamodel-guided method for model
execution. In the XML representation, omitting the              generation with layered constraints. The generation-
required event name violates a structural requirement.          time constraint layer (L1) and the post-generation val-
Referencing a runnable entity that does not exist vio-          idation layer (L2) jointly support model construction
lates reference consistency. A period of 0.02 s fails to        subject to structural constraints and domain rules. L1
satisfy the required 10 ms interval even if the structure       enforces requirements that can be applied during gen-
and references are correct. Deleting the event during           eration through constrained decoding. L2 uses domain
repair may remove a violation, but it also removes the          validation tools to check generated models and their
periodic behavior required by the task. Model con-              serialized artifacts. Task acceptance checks then verify
struction must therefore address metamodel confor-              the objects, values, and relationships specified in the
mance, model consistency with respect to the specified          original requirements. The two layers are distinguished
rules, and requirements satisfaction together.


                                                            2
by when and how constraints can be enforced. Struc-               checks constructed models and serialized artifacts. The
tural and logical requirements are assigned according             original task requirements govern repair and accep-
to their representations and the capabilities of the avail-       tance, connecting constraint enforcement during gen-
able backends.                                                    eration with validation of the complete result.
   To support this division of responsibilities, the                 (2) ICM construction and task binding for layered
method constructs a reusable Integrated Constraint                execution. Metamodel information is transformed, its
Model (ICM). It first extracts and transforms informa-            terminology guides structured constraint extraction,
tion from an existing domain metamodel, preserving                and constraints are linked to metamodel elements with
element identifiers and their correspondence with the             their sources and intended uses retained. Relevant con-
source representation. Metamodel terminology then                 straints are then bound to task objects, values, and
guides constraint extraction from natural-language                references, providing a common basis for genera-
specifications. The extraction identifies the elements            tion constraint assembly, retrieval, and post-generation
to which constraints apply, along with their condi-               checks.
tions, requirements, and exceptions. The constraints                 (3) An empirical evaluation in three domains.
are automatically linked to metamodel elements, and               Experiments with AUTOSAR automotive software
their sources in the specifications are recorded. Meta-           models, railway models, and structured decision-
model elements provide a shared domain context for                making in private international law (PIL) examine
interpreting constraints. The ICM organizes structural            model and artifact acceptance, constraint interventions
information and specification requirements from dif-              during decoding, repair with validation feedback, and
ferent sources for use in generation, retrieval, and              the enforcement of constraints on decisions. The first
validation.                                                       two domains evaluate the construction of engineering
   For each task, the method selects relevant con-                model instances. PIL examines the application of the
straints based on the requirements and the existing               layered approach to decisions governed by many rules
model. It binds these constraints to the objects, values,         and requiring reliable conclusions.
and reference targets involved in the task and dynam-                For AUTOSAR, we conducted three runs for each of
ically assembles generation constraints and the vali-             20 requirements. All 60 end-to-end runs passed accep-
dation configuration. Temporary requirements apply                tance checks within the specified task scope, and all
to the current generation and repair process, while               255 resulting ARXML files passed XSD validation. In
reusable domain rules are stored in the ICM. When                 the controlled fault-injection experiment, all 85 core
errors are detected, validation feedback identifies the           units and all 15 substitute units were repaired success-
violated requirements and the affected objects. The               fully. A separate local AUTOSAR decoding experi-
repair process uses this feedback to propose changes              ment directly observed the role of constraints during
within the permitted scope. Each repair is checked                generation. The main railway experiment comprised
again against both domain rules and the original task             24 tasks, each run three times. Among the 72 runs, 23
requirements to avoid accepting changes that remove               met the strict success criterion after initial generation,
required objects or alter prescribed values.                      compared with 51 after repair with validation feed-
   The method applies to domains that can be                      back. The PIL experiment comprised 60 cases. The full
described by metamodels, provided that task-relevant              constraint configuration achieved better results in the
constraints can be mapped to generation-time con-                 combined evaluation of structure, rule compliance, and
straints and post-generation validation rules. The                task conclusions. Together, these experiments examine
domain metamodel is provided as input. Generation                 the engineering workflow, execution mechanism, and
mappings and validation tools are incorporated dur-               application of the layered method across domains. The
ing domain preparation. We use existing domain tools              railway tasks that remained unrepaired also inform the
and custom checkers written by humans with LLM                    analysis of the limits of current generation and repair
assistance.                                                       capabilities.
   The paper makes three contributions.                              The remainder of the paper is organized as follows.
   (1) A metamodel-guided model generation method                 Section 2 discusses related work. Section 3 presents
with layered constraints. The method assigns con-                 the layered constraint method and ICM construction.
straints to L1 and L2 according to their representations          Section 4 reports the AUTOSAR engineering experi-
and the capabilities of the execution backends. L1                ment, the local AUTOSAR decoding experiment, the
restricts candidate content during generation, while L2           railway experiments, and the PIL experiment in that


                                                              3
order. Section 5 concludes the paper and discusses           be carried across representations, and target arti-
future work. The appendices are organized by exper-          facts may have organizational requirements that are
iment and document the sources of the requirements,          not directly expressed in the source representation.
the setup for extracting constraints from AUTOSAR            Reading a metamodel and producing a representation
specifications, the construction of checkers, and sup-       suitable for processing is distinct from creating model
plementary results. They also include one complete           instances, generating code, or producing exchange
example for each of AUTOSAR, railway modeling,               artifacts, although these operations can be combined
and PIL, from task input to final acceptance.                in a workflow.
                                                                Consistent model generation uses constraints
2 Related work                                               directly during model construction. Semeráth et al.
                                                             take a metamodel, well-formedness constraints, and
Related research includes traditional MDE techniques         a search scope as input. They guide graph solving
for constructing consistent models from metamodels           through the refinement of three-valued partial models,
and constraints, as well as modeling from natural lan-       constraint propagation, and incremental checking, and
guage, structured constraint acquisition, constrained        check the original well-formedness constraints after
decoding, and repair using feedback.                         concretization [10]. Their method can start from the
                                                             most abstract partial model or an initial partial model
2.1 Model transformation and consistent                      provided by an engineer, using explicit constraints to
    model generation                                         narrow the candidate space during search. This pro-
                                                             vides an MDE basis for combining control during
MDE uses modeling languages to define the con-               generation with checks after completion. Compared
cepts that can be expressed and the conditions for           with generation driven by formal constraint solving,
model validity. Metamodels specify abstract syntax.          generation from natural language must also establish
Well-formedness constraints capture requirements that        how textual concepts and requirements correspond to
cannot be fully expressed through structural defini-         model elements that can be manipulated and which
tions such as types and relationships, while concrete        constraints apply to the current task.
syntax defines the textual or graphical representation
of models. The Object Constraint Language (OCL)              2.2 LLM-assisted modeling and model
expresses invariants, preconditions, and postcondi-
                                                                 instance construction
tions in a model context and defines their types and
evaluation semantics [7]. XML Metadata Interchange           Research on LLM-assisted modeling covers modeling
(XMI) provides an XML representation for exchanging          languages and their metamodels, instances of exist-
model objects [8]. Models and their serialized doc-          ing modeling languages, and the completion or mod-
uments therefore require related but distinct checks.        ification of current models. Di Rocco et al. review
Document parseability, metamodel conformance of              this field in terms of MDE activities, discussing the
objects, and compliance with rules involving multiple        encoding of modeling artifacts, post-processing of
objects must each be assessed against the appropriate        generated results, and evaluation. They also propose
criteria.                                                    a research agenda in which LLMs and MDE support
   Model transformations make correspondences                each other [2]. This perspective emphasizes integrat-
between models or representations explicit. Kahani           ing generation into model toolchains, where modeling
et al. classify model transformation tools and discuss       tasks require more than plain text output.
their support for model-to-model and model-to-text              Combining natural language with a language def-
transformations [1]. The two-stage code generation           inition is a common approach to generation. Alaoui
framework proposed by Ma et al. combines XMI                 Mdaghri et al. generate DSL models from natural-
structural information with XSD constraints. It first        language descriptions and modeling language docu-
generates static code structures and then adds behav-        mentation, validating the results through an iterative
ior based on model annotations and associations [9].         process [11]. In a technical report on automotive sys-
These studies illustrate the importance of representa-       tems, Petrovic et al. combine Ecore metamodels and
tion mappings when incorporating industrial modeling         requirements in prompts to generate XMI instances.
languages into a toolchain. Types and structures must        OCL checks determine whether the instances pro-
                                                             ceed to downstream code generation. The report also


                                                         4
explores proposing OCL constraints from reference                 information shared across candidates to reduce incon-
requirements and metamodels [12]. These studies con-              sistencies, showing how model solving and language
nect natural-language input, explicit language repre-             model generation can complement each other.
sentations, and subsequent model processing.
   Domain configuration generation further illustrates            2.3 Structured constraint acquisition and
the role of intermediate representations and arti-                    traceability
fact mappings. El-Gnainy et al. study AI-assisted
AUTOSAR configuration, dataset generation, and                    Using natural-language specifications for automation
code production [13]. Samy et al. use a fine-tuned                requires identifying the domain concepts, scopes, and
model to generate compact JSON, which is determin-                logical relationships referred to by rules. Model con-
istically expanded into ARXML. They evaluate struc-               text can provide types and navigation paths for this
tural, reference, parameter, and semantic conditions              interpretation. PathOCL takes a UML class model
for Watchdog Manager configurations [14]. Compact                 and natural-language constraints as input, selects rel-
representations reduce the burden of directly generat-            evant classes and model paths to construct prompts,
ing complex exchange formats, but the expansion rules             and then generates OCL expressions. The study eval-
remain an essential part of the domain implementation.            uates compilability and semantic correctness sepa-
The validity of the intermediate representation and               rately. Path-based prompts shorten individual inputs,
that of the final ARXML artifact must be connected                and attempts with multiple paths increase the propor-
through this mapping.                                             tion of compilable constraints, while gains in semantic
   Interactive assistants integrated into modeling envi-          correctness are smaller [15]. These results reflect two
ronments use the current model as an evolving context.            related problems in constraint acquisition. The text
At the level of abstract syntax, EMF-Kaizen com-                  must be associated with an appropriate model context,
bines the metamodel, current model, user request,                 and its requirements must be correctly expressed as
and examples to recommend model fragments. It sup-                constraints.
ports metamodel pruning, conversion between JSON                     Traceability concerns correspondences between
and EMF objects, and user selection of fragments for              artifacts and how those correspondences are used.
incorporation into the model [6]. Its scope includes              Winkler and von Pilgrim discuss artifact traceability
both domain models and metamodels, illustrating how               in requirements engineering and model-driven devel-
assistant capabilities can be reused through shared               opment, including connections between the two activ-
modeling infrastructure. The reported implementation              ities [16]. In constraint generation, links to sources and
uses tolerant parsing to handle returned fragments.               model elements help explain which specification pas-
OCL annotations in the metamodel can be included in               sage supports a rule and which types or relationships it
prompts, but OCL checks are not performed on the rec-             concerns. They also help locate affected content when
ommended fragments [6]. Interactive recommendation                changes are made. Associating rules with metamodel
focuses on fragments that a modeler can continue to               elements supports reuse across tasks, while binding a
use, whereas generation for a complete task must also             rule to specific objects determines the scope of checks
establish whether all required objects and associations           for a particular task.
are present.                                                         Retrieval-augmented generation combines retrieved
   AbsCon combines agreement among candidates                     content from external documents with text generation
with explicit constraints. It first generates multiple can-       by a language model [17]. For engineering specifi-
didate graphs from the same text and merges them                  cations, retrieval can supply applicability conditions,
into a probabilistic partial model. Constraint optimiza-          exceptions, and background explanations. Structured
tion then selects a concrete model that satisfies the             constraints additionally record explicit links between
metamodel and well-formedness constraints [5]. Con-               this information and model elements. The two can be
straints participate in solving for the final model, rather       used together. A requirement may provide evidence
than serving only as a basis for subsequent scoring.              in a prompt and, where a corresponding mapping
In the reported implementation, the metamodel and                 exists, support generation control or logical checks.
well-formedness constraints are manually translated               Organizing metamodel information, structuring textual
into first-order logic [5]. Compared with direct gen-             requirements, and implementing executable checks are
eration or interactive completion, this approach uses             thus related but distinct activities. Completing text



                                                              5
extraction does not by itself produce a checking pro-            distinct properties. For engineering modeling, con-
gram.                                                            strained decoding can reduce invalid candidates, but
                                                                 assessing whether a candidate satisfies the meaning of
2.4 Constrained decoding and repair                              a task still requires appropriate evaluation criteria.
    with validation feedback                                        Model consistency maintenance provides mech-
                                                                 anisms for locating inconsistencies and selecting
Constrained decoding filters next-token candidates for           repair operations. Marchezan et al. use rule evalua-
validity during generation, allowing encoded struc-              tion to locate causes of inconsistency and construct
tural requirements to influence the output directly.             abstract repair trees containing alternatives and opera-
Geng et al. study grammar-constrained decoding for               tion sequences. Their approach also supports filtering
structured tasks and grammars that depend on the                 actions by artifact or user ownership [23]. Research on
input [18]. XGrammar improves the eﬀiciency of                   feedback-based LLM revision investigates how feed-
structured generation by processing grammars and                 back can be used to generate new candidates. Self-
computing which tokens are allowed at each genera-               Refine uses the same model to generate an output,
tion step [19]. XGrammar-2 further supports dynamic              provide feedback, and iteratively revise the result [24].
structure switching within a request and cache reuse             SpecGen generates JML specifications for Java pro-
across grammars [20]. These techniques allow struc-              grams. It first improves candidates using feedback
tural restrictions that vary by task to be enforced during       from verification errors, then combines operator muta-
decoding. They provide a basis for incorporating meta-           tions with heuristic selection to find verifiable spec-
model types, required features, enumerations, and rep-           ifications [25]. These studies show that the source
resentable relationship constraints into model instance          of feedback, available modification operations, and
generation.                                                      candidate acceptance criteria jointly influence repair
   Generation-time control can also incorporate                  outcomes.
semantic information. Synchromesh combines exam-                    Existing research provides model transformation,
ple retrieval with a completion engine to enforce                constraint solving, constrained decoding, and repair
syntax, scope, type, and selected contextual rules on            using feedback. This paper contributes a method for
partial outputs [4]. Projectional Decoding maintains a           coordinating their use in model generation. Constraints
partial graph model as text is generated and uses the            that can be enforced during generation are assigned
metamodel and incremental semantic checks to filter              to L1; requirements that depend on constructed mod-
subsequent tokens. The study reports a preliminary               els and target artifacts are checked in L2. ICM con-
evaluation on a program generation task [21]. The dis-           struction connects metamodel information with spec-
tinction between generation-time and post-generation             ification requirements and their sources. Task binding
checks therefore does not impose an absolute sep-                makes this information applicable to concrete objects,
aration between syntax and semantics. Whether a                  values, and references, while the original requirements
condition can be checked early depends on the infor-             govern acceptance after generation and repair. The
mation already established in the partial model, the             evaluation examines these connections in AUTOSAR,
executable representation of the constraint, and the             observes L1 interventions directly in a local decoding
backend capabilities. Conditions that require a com-             experiment, and studies repair and task acceptance in
plete model or context across artifacts can be handled           railway models and structured legal decisions.
by later checks.
   Constraint enforcement also affects which valid out-
puts are more likely to be generated. Grammar-Aligned
                                                                 3 Metamodel-guided generation
Decoding shows that removing invalid tokens and                    with layered constraints
rescaling the remaining probabilities at each step gen-
                                                                 The method uses an Integrated Constraint Model
erally changes the relative probabilities that the origi-
                                                                 (ICM) to organize metamodel information and domain
nal LLM assigns to complete valid outputs. It proposes
                                                                 rules. Task-related requirements are implemented
a sampling method to address this difference [22].
                                                                 through the generation-time constraint layer (L1) and
Here, sampling means drawing outputs according to
                                                                 the post-generation validation layer (L2). L1 restricts
their probabilities. Output validity and preservation of
                                                                 the structure and values of candidate content during
the original model’s relative probabilities are therefore
                                                                 generation. L2 checks structural conformance, domain


                                                             6
consistency, and task requirements on the constructed              JSON Schema is a well-established and widely used
model and target artifacts, and provides diagnostics for        specification for describing and validating JSON data.
repair. Shared constraint information and task bind-            Its keywords describe field types, required fields, num-
ings connect the two layers into a complete process             bers of items, and allowed values [26]. It provides a
from requirements to model generation, validation,              constraint representation rather than a decoding algo-
and repair.                                                     rithm. Providing a schema in a prompt or using it to
                                                                validate completed output does not by itself constitute
3.1 Scope and overview                                          constrained decoding. Backends such as XGrammar
                                                                compile supported schema constraints into a grammar
The method applies to domains that can be described             and enforce them by excluding disallowed tokens dur-
by a domain metamodel, provided that task-relevant              ing generation [19]. The method uses this capability
constraints can be mapped to generation-time con-               to execute constraints assembled for each task. JSON
straints and post-generation validation rules. The              Schema is one implementation choice; domain adap-
domain metamodel is provided as input. Other inputs             tations can also use other representations supported by
include natural-language domain specifications, the             the backend, such as grammars.
current task requirements, and the existing model con-             A candidate model is a model instance constructed
text. This context consists of model elements that exist        according to the domain metamodel and awaiting val-
before generation and may be used by the current task,          idation and acceptance. It contains concrete objects,
together with their attributes and relationships. For           attribute values, and relationships between objects.
example, when adding a timing event to a system, the            JSON Schema specifies the structures and values that
name, type, and reference path of an existing runnable          may be generated for the current task. The generated
entity form part of the model context needed by the             content becomes a candidate model through model
new event.                                                      construction. A serialized artifact is a concrete repre-
   The metamodel defines structural information,                sentation of the candidate model in the target modeling
including available types, attributes, inheritance, con-        language or exchange format, such as an XML file.
tainment, references, multiplicities, and enumerations.         In structured decision applications, the output may
Natural-language specifications add applicability con-          instead be a decision record containing facts, appli-
ditions, exceptions, consistency requirements across            cable rules, and conclusions. Such outputs reuse the
elements, and complex semantic and logical require-             layered constraint enforcement process. Their corre-
ments. The task further specifies the objects to con-           spondence with domain concepts is established during
struct, their numbers and values, their connections, and        domain adaptation and described separately from the
the target output. Even at the structural level, deep           construction of engineering model instances.
nesting, optional branches, repeated elements, and ref-            The overall process comprises domain prepara-
erences can interact. Structural correctness is therefore       tion and task execution. Domain preparation extracts
addressed during generation and checked again after             information from an existing metamodel, uses meta-
model construction and serialization.                           model terminology to guide constraint extraction from
   The method combines deterministic model con-                 natural-language specifications, automatically links
struction supported by MDE tools with LLM-assisted              constraints to metamodel elements, and records their
modeling activities. Metamodels, domain rules, and              sources to form a reusable ICM. It also provides
transformation mappings provide explicit representa-            generation constraint mappings, model construction
tions and executable operations. Deterministic proce-           and serialization rules, and callable validators. Task
dures assemble constraints, construct objects, apply            execution binds the current requirements to concrete
values already specified by the task, and serialize             objects and values, assembles L1 generation con-
the result. LLMs propose candidate content using the            straints, retrieves relevant rules, and configures L2
task and model context and propose modifications                checks. The generated content undergoes model con-
in response to validation diagnostics. For example,             struction and serialization before validation and task
the metamodel defines the representation of a timing            acceptance. When a problem can be addressed, its
event, while the required period of 10 ms comes from            diagnostics guide model changes and revalidation.
the task. A program can bind and check that value               Figure 1 shows this process.
without asking the LLM to infer it again.                          A simplified ARXML fragment illustrates the three
                                                                kinds of requirements. The task is to configure a timing


                                                            7
     (a) Domain preparation


           Existing domain
             metamodel                                                                                               Manually register
                                                                                                                    generation mappings
                                                 Extract and link
                                           constraints to construct ICM
                                                                                        ICM                          Develop or integrate
                                                                                                                          checkers
          Natural language
           specifications

                                    Reuse domain preparation results across                                       Generation mappings and
                                              subsequent tasks                                                            checkers


     (b) Task execution

       ICM, generation mappings,
              and checkers
                                                    Select applicable                                                            L1
                                                       constraints                  Task-specific constraints
                                                                                    and check configuration                  Constrained
                                                 Bind objects and values                                                     generation
          Current requirements
                                                                                                    Checks and
       and existing model context
                                                                                                    parameters

                                     Yes           All required checks                         L2
                                                                                                                       Construct the model
       Accept and record results                     completed and                      Post-generation
                                                         passed?                                                         and serialize it
                                                                                          validation


                                                              No; further repair
                                                                   allowed
       Record unresolved issues                                                       Identify and repair
          Refer to a human                                                                   issues
                                                                                                                   Rebuild after
                                      No; stop                                                                       revision


     Legend                                                                                                                            Control
                       Process                Data                      Document         Decision                Data flow
                                                                                                                                       flow


Fig. 1 Domain preparation and execution of an individual task. The ICM, generation mappings, and validators are prepared for reuse across
tasks. Task binding determines the content needed for generation, retrieval, and validation. L1 constrains generation, L2 checks the constructed
results and guides repair, and task acceptance is determined against the original requirements

event that triggers an existing runnable entity R every                        issue with model relationships. A period of 0.02 s fails
10 ms. A runnable entity represents software behavior                          to meet the task requirement of 10 ms even if the struc-
that can be triggered for execution. The model con-                            ture and references are correct. These requirements
text supplies the path /Component/Behavior/R for R.                            do not map rigidly to different stages. A reference
The following fragment omits the enclosing compo-                              target and period that have already been determined
nent and behavior structures, uses a simplified path,                          can restrict generation in advance, while the results
and expresses the period in seconds.                                           of model construction and serialization still require
<TIMING-EVENT>
                                                                               post-generation checks.
  <SHORT-NAME>TE_R</SHORT-NAME>                                                   The domain integrator provides generation map-
  <START-ON-EVENT-REF DEST="RUNNABLE-ENTITY">/Component/B ⌋
  ehavior/R</START-ON-EVENT-REF>
                                                                               pings and validators. In this work, custom checkers
  <PERIOD>0.01</PERIOD>                                                        are written by humans with LLM assistance, while
</TIMING-EVENT>
                                                                               existing tools perform native format checks.
   Omitting the required event name is a structural
issue. A reference to a nonexistent runnable entity is an


                                                                           8
3.2 Extracting and transforming                                  interpreting the text so that the extracted constraints
    metamodel information                                        can be linked directly to domain elements.
                                                                    The system then links the extracted records automat-
ICM construction begins by transforming an exist-                ically to metamodel elements. It resolves target names
ing metamodel into a queryable intermediate repre-               and checks target types and the ownership of attributes,
sentation. The transformation reads element identi-              relationships, or enumeration literals. For links that
fiers, attribute types, inheritance, containment, refer-         cannot be resolved automatically or remain ambigu-
ences, multiplicities, and enumerations, while preserv-          ous, the domain integrator consults the specification
ing source element identifiers and versions. Domains             and metamodel and adjusts the target associations and
with a separate exchange syntax also require mappings            record uses accordingly. Existing structured rules and
between metamodel elements and constructs in the                 domain check definitions can also be incorporated into
target language. Examples include the XML attribute              the ICM under the same information requirements,
or element corresponding to a model attribute and                reusing their rule content and sources. Figure 2 shows
the wrapper nodes corresponding to a containment                 how the ICM is constructed from natural-language
relationship.                                                    specifications, and Table 1 lists the main information
   The result can be represented as an object model,             in a constraint record.
relational records, JSON, or a graph. The essential                 We summarize these information relationships by
requirement is to preserve the information and source            representing the ICM as
element correspondences needed for extraction, query-
ing, and binding, rather than to adopt a particular stor-                            I = (M, C, A, P )                  (1)
age format. Model-driven language engineering distin-               Here, I denotes the integrated constraint model for
guishes abstract syntax, concrete syntax, and the rela-          the target domain. M is the metamodel representa-
tionships between their evolution [27]. Accordingly,             tion obtained through extraction and transformation,
the metamodel representation describes domain con-               including element identifiers, types, attributes, rela-
structs, the serialization mapping defines their target          tionships, multiplicities, and enumerations. C is the
representation, and the generation constraints specify           persistent set of domain constraint records. It includes
the structures and values allowed for the current task.          constraints extracted from specifications and meta-
Each serves a different role in the process.                     model structural rules that need to be referenced
   The transformed types, attributes, and relationships          individually. A contains the associations established
provide standard terminology for text extraction. They           between constraint records and metamodel elements.
also support the selection of types for task objects,            P contains provenance and its links to metamodel
the construction of relationships, and the identification        elements and constraint records, including the source
of applicable constraints. Constraints are associated            metamodel or schema files and the versions and spe-
with type or relationship definitions in the metamodel.          cific locations of natural-language specifications. Con-
The objects specified by the current task are concrete           straint records retain intended uses, links to existing
instances of those types.                                        implementations, and link-checking results.
                                                                    Figure 3 shows these four kinds of information.
3.3 Metamodel-guided constraint                                  Constraints and metamodel elements can have many-
    extraction and ICM construction                              to-many associations. A reference consistency rule
                                                                 may involve the source type, the reference relation-
The ICM combines the structural information provided
                                                                 ship, and the target type, while the same type may
by the metamodel with rules from natural-language
                                                                 participate in several rules. Provenance records allow a
specifications. Specification fragments are processed
                                                                 constraint to be traced back to the original specification
individually. The system adds relevant metamodel
                                                                 and its related types and attributes to their metamodel
types, attributes, relationships, and enumeration terms
                                                                 definitions.
to the extraction context. It instructs the LLM to extract
                                                                    Structured constraints in the ICM have the three uses
the elements to which each constraint applies, its appli-
                                                                 listed in Table 2. A constraint can serve more than one
cability conditions, requirements, and exceptions in
                                                                 purpose. Parts that can be mapped to restrictions on
a common record format, while retaining the spec-
                                                                 structures and values are incorporated into generation
ification version and fragment location. Metamodel
                                                                 constraints. Complete rules and their explanations can
terminology provides a shared conceptual basis for
                                                                 be retrieved for inclusion in prompts. Requirements


                                                             9
       Existing domain                   Extract and transform
         metamodel                                                                Metamodel representation
                                         metamodel information
                                                                                                                   Metamodel
                                                                                                                    structure
                                                        Metamodel
                                                         context
                                                                                                    Basis for
                                                                                                    linking



                                          Provide context and                       Link constraints to                         ICM
    Specification excerpts
                                       extract constraints (LLM)                    metamodel elements


                                                                     When review is
                                                                                                           Revised records
                                                                            needed

      Constraint record
                                                                                Review and revise constraint
        field format                                                            semantics and element links



Fig. 2 ICM construction from an existing domain metamodel and natural-language specifications. The metamodel representation supplies
terminology for extraction, information for automatic linking, and structural information. Linking issues are referred for human handling. The
ICM retains constraint content, element associations, sources, and intended uses


Table 1 Main information in an ICM constraint record

Information                              Content                                                Subsequent use

Identifiers and sources                  Rule identifier, specification version, fragment       Trace constraint sources and distinguish
                                         location, and original wording                         versions
Constraint content                       Scope, applicability conditions, requirements,         Determine when, on which objects, and
                                         and exceptions                                         what to check
Metamodel element associations           Relevant classes, attributes, containment, or          Retrieve by domain concepts and bind
                                         references                                             task objects
Uses and implementation links            Intended uses and identifiers of generation            Connect generation, retrieval, and
                                         mappings or checkers                                   validation
Link checks                              Results and issues from checking target                Locate unmatched or conflicting
                                         names, types, and member ownership                     associations and support correction


that must be evaluated on a complete model provide                        when a failure occurs. The full domain specification
a basis for validator development. Intended uses and                      need not be reinterpreted for every task.
existing implementations are recorded separately. The
ICM thus organizes executable constraints alongside                       3.4 Binding task objects and
information needed for retrieval and validator develop-                       requirements
ment.
   This organization preserves the connections                            The persistent ICM describes domain information
between structural information, textual rules, and the                    reused across tasks. The current requirements specify
information used to enforce them. A requirement can                       concrete objects, quantities, values, and connections.
restrict candidate content during generation, support                     Using the existing model context, the system identi-
checks on the final relationships after generation, and                   fies relevant metamodel elements, selects applicable
be traced to the relevant rule and model elements                         constraints, and binds the requirements to concrete
                                                                          objects in the task. Temporary constraints extracted


                                                                     10
  Provenance P

                                                                                           Natural language specifications and clause
                     Metamodel file and element locations
                                                                                                           locations
                     Version, identifiers, and source links
                                                                                           Version, original wording, and source links

                                         Source link                                                              Source link


      Metamodel representation M                                                         Domain constraint records C
                                Reference
              TimingEvent                      RunnableEntity       Associations A
                                                                                         Example: periodic execution requires an event
                                                                  Constraint - element
        period [1]                       shortName                                       Applies to: timing events and target references
                                         Owning internal
        startOnEvent [0..1]                                                              Requirement: reference a runnable entity
                                         behavior
                                                                                         and specify the period

      Classes, attributes, multiplicities;                                               Uses, implementation links, and review status
      containment, reference and inheritance


Fig. 3 ICM information and associations. The metamodel representation M provides domain elements and relationships, constraint records C
express rule content, associations A link constraints to the elements to which they apply, and provenance P supports tracing back to sources.
The three uses of the constraints share this information and do not constitute additional metamodel levels


Table 2 Three uses of ICM constraints

Use                                             Application                                          Example

Generation-time structural                      Use existing mappings to restrict types,             Restrict references to targets with
constraints                                     required items, quantities, enumerations, or         matching types in the context
                                                reference candidates
Retrieval for prompting                         Retrieve rules and context according to the          Provide applicability conditions and
                                                elements and conditions involved in the task         specification explanations for references
Basis for validator development                 Humans implement or integrate checks from            Check whether the final reference target
                                                rules and the metamodel, with LLM assistance         exists and has the correct type


from natural-language requirements apply only to the                          Requirements evaluated on the constructed results are
current task and its repairs. They are not automatically                      bound to the input objects and parameters of exist-
written back to the persistent ICM.                                           ing checkers. A new check configuration can thus be
   Depending on domain complexity, task execution                             assembled at runtime without generating new valida-
can provide information and generate content in mul-                          tion code for every task.
tiple stages. Requirements are first analyzed to deter-                          In the timing event example, the runnable entity R
mine the constituent objects and their dependencies.                          and the 10 ms period come from the current require-
Relevant metamodel information, specification frag-                           ments. Binding determines the target reference and
ments, and available references are then provided for                         the period value, respectively. The requirement that
each part as the model is generated progressively.                            a reference point to an object of an appropriate type
Designs formed in earlier stages supply structural                            is a reusable rule. Task acceptance checks the target
choices for subsequent constraint assembly, while gen-                        and period against the original requirements. Another
erated objects that are available for use update the                          runnable entity of the correct type cannot replace the
model context. Object identities and values explicitly                        specified R.
stated in the requirements remain the basis for the task,
and LLM-proposed designs must correspond to them.
   The binding results serve three purposes. Require-
ments with generation mappings enter the L1 gen-
eration constraints. Retrieved specification content is
added to the prompt as external knowledge [17].


                                                                        11
Algorithm 1 Task-specific JSON Schema assembly                        specifies a target, the reference is bound to that object.
Inputs are the ICM, current task bindings, existing model             When a choice remains, the eligible candidate set is
context, domain structure and serialization mappings, and the         retained. For targets yet to be constructed in the same
constraints supported by the backend.                                 task, existence, type, and relationship consistency are
Outputs are the generation schema for the current call and the        checked after assembly. Assembly rules handle deter-
correspondences needed for subsequent model assembly.                 ministic content, while requirements that need the
 1. Use task bindings to identify the required types, objects,        complete result are configured for L2.
    and dependencies in the metamodel representation.                    Generation constraints and the target language do
 2. Expand required structures and task-selected branches,            not always have a one-to-one correspondence. For an
    mapping types, required features, and multiplicities to           XML target, XML Schema can require child elements
    field restrictions.                                               to follow a sequence [3]. When JSON objects carry
 3. Use task requirements and the existing model context              named fields, their written order does not directly
    to bind fixed values, permitted enumeration values, and           encode this XML ordering requirement. In the cor-
    available reference candidates.                                   responding adaptation, the serializer orders elements
 4. Incorporate domain constraints supported by existing              according to the target schema, and XML Schema
    mappings, retaining their correspondence with ICM                 validation checks the artifact. This illustrates the divi-
    rules and task requirements.                                      sion of responsibilities among generation constraints,
 5. Check the assembled constraints, adapt them to the                model construction, and target representation. Other
    decoding backend, and output the generation schema and            intermediate representations or decoding directly in
    model assembly correspondences.                                   the target language can use different mappings.

                                                                      3.5.2 Constrained decoding for model
3.5 Assembling generation constraints
                                                                            instance generation
    and constrained decoding
                                                                      In MDE, generated output must be parseable, support
3.5.1 Dynamic assembly of generation                                  the construction of model instances, and be usable by
      constraints                                                     downstream tools. Incorrect nesting, omitted required
L1 assembles the executable parts of the metamodel                    items, or invalid enumeration values can cause this
structure, applicable domain rules, and task bind-                    process to fail before domain validation begins. Con-
ings into generation constraints for the current task.                strained decoding applies encoded structural restric-
JSON Schema can express restrictions on field types,                  tions at each generation step. For complete outputs,
required fields, quantities, fixed values, and enumera-               a correctly implemented backend ensures compliance
tions [26]. Dynamic assembly uses the metamodel as                    with the constraints encoded in its compiled gram-
its structural basis, task choices to determine which                 mar, within the feature set it supports. These outputs
parts to expand, and the existing model context to                    provide input for subsequent model construction [18].
constrain available references. The generation speci-                    A decoding backend under direct control first con-
fication therefore varies with the task and the context               verts the generation specification into a supported
obtained so far.                                                      grammar representation and compiles it using infor-
   Algorithm 1 summarizes the assembly process                        mation from the model’s tokenizer [19] [20]. The
when JSON Schema is used. Domain adaptation pro-                      tokenizer maps text to sequences of token identifiers,
vides type and relationship queries, constraint map-                  allowing the backend to relate token choices to the
pings, target structure templates, and serialization                  grammar. During generation, the matcher maintains
mappings. At runtime, these resources are used to                     the grammar state from the current output prefix and
expand the structure required by the task recursively.                determines the tokens allowed at the next step. After
Object identities, quantities, and assignments that have              the LLM produces next-token scores, the backend sets
already been determined can be encoded as fixed                       the scores of disallowed tokens to negative infinity
restrictions or assembled by deterministic procedures.                so that they cannot be selected. It then selects the
For content still to be chosen by the LLM, the assem-                 next token from the allowed candidates. The token is
bled constraints retain the permitted values.                         appended to the output and the matcher is updated.
   Reference candidates are determined jointly by tar-                This process continues until the output is complete.
get type, scope, and model context. When the task


                                                                 12
   This control covers punctuation and nesting as well             Hosted structured-output interfaces enter this pro-
as field names and valid values encoded in the schema.          cess through schema submission and validation of the
When generating a reference value, the constraints can          returned values. A local backend under direct control
restrict the output to the candidate paths configured           additionally allows observation of constraint interven-
for the task. For a numeric field with a bound value,           tions at individual decoding steps. Both use the same
they can restrict it to the value specified by the task.        relationship between generation constraints and result
Tokens do not correspond one-to-one to characters or            checks. The corresponding experiments describe how
grammar symbols, so the backend must maintain these             the decoding process is observed.
permitted choices at the tokenizer level [19]. Figure 4
separates task constraint assembly from this stepwise           3.6 Post-generation validation and task
enforcement process.                                                acceptance
   Retrieved prompt content and constrained decod-
ing serve complementary roles. The former supplies              L2 checks whether the candidate model and serial-
the meaning of the requirements and relevant domain             ized artifacts satisfy the metamodel, applicable domain
information, while the latter excludes continuations            rules, and the current task. It divides responsibil-
that violate the structural restrictions being enforced.        ity with L1 according to expressive capabilities and
Constrained decoding changes the output distribu-               contextual requirements. Requirements that can be
tion of the original LLM. Stepwise filtering generally          expressed in advance as structural restrictions or finite
changes the relative probabilities of complete valid            value choices are enforced during generation. Require-
outputs, as discussed in Section 2.4 [22]. L1 there-            ments that depend on complete objects, relationships
fore enforces the generation constraints that have been         across objects, or target artifacts are evaluated after
encoded and are supported by the backend. Domain                construction. The same rule can participate in both lay-
consistency and requirements satisfaction remain sub-           ers. For example, L1 filters reference candidates by
ject to L2 checks.                                              target type, while L2 checks whether the constructed
                                                                references resolve correctly. Recent work also explores
3.5.3 From generated content to models and                      semantic checks during model construction [21]. The
      serialized artifacts                                      two layers therefore do not represent a fixed division
                                                                between syntax and semantics.
Once the complete output is returned, the system                   Validator construction and integration. During
validates it against the generation constraints used            domain preparation, the integrator uses ICM con-
for the call. When JSON Schema is used, this val-               straints and their sources to determine the input
idation checks field types, required properties, array          objects, applicability conditions, decision logic, and
sizes, and allowed values. It then uses the recorded            diagnostic locations for each check. Properties sup-
assembly correspondences to add deterministic con-              ported by existing tools are checked through their inter-
tent, create model objects, organize containment, and           faces, as in target format validation. Properties express-
establish references. If the generation interface uses          ible through existing check operations are imple-
a projected intermediate structure, the reconstructed           mented using rule templates and parameter configura-
result must also be checked against the original genera-        tions. Dedicated checkers handle consistency require-
tion constraints after assembly. These checks maintain          ments across objects. In this work, custom checkers are
the connections between the interface response, model           developed by humans with LLM assistance. The LLM
assembly, and task constraints.                                 helps organize rules and draft code and tests. Humans
   The domain adapter then converts the candidate               consult the specifications to confirm rule interpreta-
model into target artifacts. Serialization handles the          tions, select implementations, and review the decisions
wrapper structure, namespaces, reference representa-            produced by the checks.
tion, and element order required by the target language.           Checkers are tested using examples that satisfy
L2 checks the corresponding results on the model and            or violate the rules, together with relevant boundary
artifacts. For adaptations that generate the target lan-        cases. Their rule identifiers, scopes, inputs and param-
guage directly, a domain parser can load the model.             eters, results, and diagnostic information are then reg-
Under either path, output completion, model con-                istered. Task execution selects the required checks
struction, and domain validation remain explicit steps.         from these registered capabilities and binds them to
Incomplete output cannot pass acceptance checks.                the current objects and context. Temporary constraints


                                                           13
        (a) Select and bind task constraints

                                                                                           Generation constraints for this task
                    ICM


                                                                                            Retrieved content for prompting
                                                  Select applicable
             Task requirements                       constraints
                                               Bind objects and values
                                                                                           Checks and invocation parameters

           Existing model context
             and design options
                                                                                          Record of unsupported requirements



         (b) Backend compilation and incremental decoding

                                                      Backend settings
                                                      Tokenizer settings



                Generation constraints             Convert constraints and              Backend matcher
                    for this task                   compile the grammar                  configuration




                                                      LLM token scores



                                                     Exclude disallowed                                   Update output
               Identify allowed tokens                                           Select a token
                                                           tokens                                        and matcher state




                                         Yes                                    No                       Output complete
                                                       Can generation                                   and accepted by the
                                                         continue?                                           grammar?
                          Continue
                          generation                               No
                                                                                                                   Yes

                                                        Record failure                                   Receive complete
                                                    or incomplete output                                      output


Fig. 4 Task binding and L1 enforcement. (a) Task requirements, the ICM, and existing model context are used to assemble generation constraints,
retrieved content, and check configurations. (b) Grammar compilation, allowed-token filtering, and state updates. Complete output enters L2
after structural validation and model assembly

derived from natural-language tasks also enter the cur-                       well-formedness constraints and other rules, and
rent check configuration through existing check oper-                         requirements satisfaction for the current task. Meta-
ations and parameters. When new decision logic is                             model conformance covers types, attributes, relation-
needed, the domain integrator adds the corresponding                          ships, and multiplicities. Well-formedness constraints
checking capability.                                                          can address consistency across elements, while some
   Validation targets and acceptance criteria. Valida-                        format tools also check content structure [3]. The check
tion is organized around four aspects of the objects                          configuration specifies the tool or checker responsible
being checked. These are the format validity of the                           for each requirement.
generated representation and target artifacts, the meta-                         Task acceptance is based on the original require-
model conformance of the candidate model, domain                              ments or a structured task specification derived from


                                                                         14
them. Merely checking whether an artifact conforms                acceptance or the problem exceeds the available edit-
to the LLM-proposed design cannot reveal require-                 ing capabilities, the current model and diagnostics are
ments omitted from that design. For example, if the               retained for human handling. If a person changes the
design incorrectly specifies 20 ms instead of 10 ms,              original requirements or domain rules, task bindings,
the generated result may conform fully to the design.             generation constraints, and check configurations must
Acceptance must still identify the discrepancy against            be updated before the corresponding construction and
the original period requirement. Similarly, deleting a            validation steps are repeated. Figure 5 shows the rela-
required timing event may remove a reference error                tionship between validation, repair, and revalidation.
without providing the periodic triggering required by
the task.                                                         3.8 Domain adaptation and traceability
   Required checks and their applicability conditions
are specified for the task before generation. Accep-              The interfaces in Table 3 connect the general pro-
tance requires all required checks that apply within              cess to domain implementations. The ICM provides a
this scope to complete and pass. Failures or execu-               common way to organize constraints, while adaptation
tion errors in other checks performed on the candidate            components provide metamodel queries, generation
also prevent acceptance. Rule violations enter failure            mappings, model construction, validation, and editing
diagnosis, while required judgments that cannot be                capabilities. Adapters call existing domain tool inter-
completed retain an incomplete status. The validation             faces for supported operations. Other operations are
report records the checked rules, object locations, and           implemented according to the target metamodel and
results, together with judgments that remain incom-               artifact representation.
plete, so that repair can address specific problems and               Traceability records connect task requirements,
the acceptance decision corresponds to the declared               ICM rules and sources, the generation constraints actu-
task scope.                                                       ally used, models and artifacts, validation diagnostics,
                                                                  and modification results. Domain rules are associated
                                                                  with task objects through metamodel elements, while
3.7 Model repair with validation feedback                         binding records connect task requirements to concrete
Model repair relies on locating inconsistencies, defin-           values and relationships. These records allow a restric-
ing edit operations, and identifying repair candi-                tion to be traced to its source and show the stage in
dates [23]. The method uses rule identifiers, model               which it was enforced, the object to which it applied,
elements, and artifact locations from L2 to identify              and whether it was satisfied after repair. Temporary
objects that may be modified. It supplies the LLM with            task constraints are retained with the run, and their
failure diagnostics, relevant rules, the original task            scope remains limited to that task.
requirements, and permitted operations. The domain                    This adaptation structure combines metamodel-
integrator defines these operations, such as chang-               guided constraint organization, L1 enforcement, and
ing an attribute value, replacing a reference, adding a           L2 validation into a reusable method. Model represen-
required object, or removing an element whose dele-               tations, rule content, and concrete execution capabili-
tion is permitted.                                                ties vary across domains. The shared layered principle
   After the LLM proposes structured changes, a deter-            is to restrict permitted content during generation, check
ministic procedure checks whether the operations and              complete results afterward, and accept repairs against
their targets are permitted, applies the changes to the           the original task requirements.
model or task execution state, reconstructs the artifacts,
and runs the relevant validation. Revalidation checks             4 Empirical evaluation
domain rules, the original task, and protected content
together. Changes that satisfy the editing restrictions           This section evaluates the role of the layered con-
and the configured repair policy may be retained even             straint method in model generation and repair. The
if some violations remain. Repair succeeds only when              AUTOSAR experiment uses the prepared ICM to
all task acceptance criteria are met.                             examine model instance generation, ARXML arti-
   The repair loop has an attempt limit and retains the           fact acceptance, and repair of injected faults. The
changes and revalidation results. It terminates when              AUTOSAR-vLLM experiment directly observes how
acceptance checks pass. If the limit is reached without           generation constraints intervene in token selection.
                                                                  The railway experiment examines whether validation


                                                             15
        (a) Validation and task acceptance

                                                                                              Return revised model and artifact to L2
                                                                    Check
              Candidate model                     L2                results      All required checks          Yes
                                                                                                                       Accept and record
                                                                                   completed and
            and serialized artifact       Run required checks                                                               results
                                                                                       passed?



                                                                                             No
                                                                                                             Missing or incomplete
                                                                    Failed
                                                                    checks
                                          Locate failed checks                Classify and record failures           Record coverage gaps
                                         Proceed to repair in (b)               and incomplete checks                  Refer to a human




        (b) Repair and revalidation
                                                                                   No: retain failure status



               Failed checks                                        Yes         LLM proposes
                                           Changes allowed
                                                                                                                    Proposed changes
              and task context             and within limit?                  structured changes




                                                                                                             Yes
                                                     No                        Apply permitted                       Only permitted
                                                                                  changes                              changes?




                                       Record unresolved issues               Rebuild model and                         Revised
                                          Refer to a human                         artifact                         model and artifact


Fig. 5 L2-guided repair and revalidation. Failure diagnostics locate the objects to modify, and permitted operations limit the repair scope.
Changes are followed by reconstruction and revalidation, with the original task requirements retained throughout acceptance. Problems unre-
solved after automated processing are referred for human handling



Table 3 Domain adaptation interfaces

Interface                                Inputs                                                      Outputs and responsibilities

Metamodel transformation and             Existing metamodel and language mappings                    Queryable representation, source
querying                                                                                             element correspondences, and identifiers
Constraint selection and assembly        ICM, task requirements, model context, and                  Generation constraints, retrieved
                                         designs from preceding stages                               content, checks, and parameters
Model construction and                   Generated content and assembly information                  Model objects, containment and
serialization                                                                                        references, and target artifacts
Validation invocation                    Models and artifacts, check configurations,                 Results and diagnostics linked to rules
                                         and context                                                 and object locations
Issue location and modification          Failures and permitted operations                           Checked model changes and inputs for
                                                                                                     revalidation




                                                                      16
feedback can support the repair of models with rela-                The primary outcome in the AUTOSAR and railway
tionships across objects. The private international law          experiments is whether a run meets the strict success
experiment examines layered checks in structured legal           criterion defined for that experiment. The final artifact
decision-making. Appendices A through D follow the               must pass the structural and domain checks required
same order and provide additional settings, detailed             within the declared task scope, together with checks
results, examples, and the statistical methods used for          against the original task requirements. For example,
the main comparisons. Complete paired data, sensitiv-            three runs of a railway task yield three initial genera-
ity analyses, and calculation scripts are included in the        tions. For each initial generation, self-repair and repair
replication package.                                             with validation feedback start from the same initial
                                                                 model. Success rates use these 72 initial generations as
4.1 Research questions and evaluation                            the denominator. An attempt that produces no model or
    setup                                                        still fails after repair is counted as a failure. The num-
                                                                 ber of base tasks remains 24, representing the diversity
The evaluation addresses three research questions.               of requirements and layouts. The conditions for each
 • RQ1. How can constraints from specifications and              experiment are defined when first introduced in the
   metamodels be applied to an individual model gen-             corresponding subsection.
   eration task? The AUTOSAR case study demon-                      The main experiments with hosted models used gpt-
   strates source records, associations with metamodel           5.6-luna with low reasoning effort. The second LLM
   elements, task binding, and constraint execution              in the railway experiment was gpt-5.6-terra, also with
   through the ICM, and checks the generated arti-               low reasoning effort. AUTOSAR-vLLM used a local
   facts.                                                        Qwen3.5-9B model to obtain decoding traces. Cus-
 • RQ2. Do generation-time constraints actually                  tom validators were written by humans with LLM
   change the decoding process? AUTOSAR-vLLM                     assistance. The authors interpreted the rules, deter-
   compares constraints provided only in prompts                 mined the inputs and applicable objects, selected
   with constrained decoding under the same prompts.             the check implementations, and tested them. Existing
   It records where constraints exclude candidate                XSD, EMF, and VIATRA validation capabilities were
   tokens and examines the resulting structure.                  reused directly. The construction and configuration of
                                                                 checks for each domain are described in the corre-
 • RQ3. Can post-generation validation and repair
                                                                 sponding subsections. The natural-language inputs for
   correct errors in models or decisions while preserv-
                                                                 AUTOSAR and PIL generation tasks were in English.
   ing the original task requirements? The AUTOSAR
                                                                 The railway experiment used structured task specifi-
   experiment examines the detection and repair of
                                                                 cations written by the authors, including English task
   engineering faults. The railway experiment com-
                                                                 descriptions.
   pares repair strategies starting from the same initial
   model and includes a second LLM. The private
   international law experiment examines the effects             4.2 Constraint organization and
   of auditing, revision, and release control on deci-               engineering model generation in
   sion outputs.                                                     AUTOSAR
  The domains use different preparation resources.               4.2.1 Requirement sources and generation
AUTOSAR transforms metamodel information,                              workflow
extracts structured constraints from specifications,
and links them to metamodel elements. The railway                AUTOSAR describes automotive software compo-
experiment reuses the Train Benchmark metamodel                  nents, interfaces, and their interactions. ARXML is
and native queries. The PIL experiment uses a man-               the corresponding XML exchange representation. The
ually defined data model for jurisdiction decisions,             authors designed 20 requirements concerning com-
with structural constraints, retrieval evidence, and             ponent structure, ports, and references based on the
checking rules based on legal provisions. AUTOSAR                Software Component Template of AUTOSAR Clas-
examines constraint organization and component                   sic 4.2.2 [28]. The meaning of periodic triggering and
model construction; the railway experiment examines              explicit data access was checked against the Spec-
repair under an existing metamodel; PIL examines the             ification of RTE from the same release [29]. The
application of layered checks to structured decisions.


                                                            17
Table 4 Experimental design and scale

Experiment                              Base tasks and runs                               Main evaluation targets

AUTOSAR engineering model               20 requirements with 3 runs each; an additional   ICM use, ARXML structure and task
generation                              85 core and 15 substitute fault-injection units   satisfaction, controlled repair
AUTOSAR-vLLM decoding                   The same 20 cases with 3 runs each under          Token-level interventions, structural
comparison                              three conditions, totaling 180 generations        acceptance, auditing overhead
Railway model generation and            24 base tasks with 3 runs each; 1 run per task    XMI models, domain relationships, and
repair                                  with the second LLM                               original task requirements
Private international law decisions     60 scenarios with 3 runs each under four          Checks and revisions of structured
                                        conditions, totaling 720 outputs                  decisions, and compatibility with
                                                                                          reference judgments


case combinations also drew on the model struc-                       representation. XSD, reference, and task checks are
ture of an RH850 project in an ETAS toolchain. The                    then applied to the actual ARXML artifacts.
authors removed the original project context from the
observed interfaces, ports, runnable entities, timing                 4.2.2 From the ICM to an individual check
events, and access relationships, then decomposed and
                                                                      The AUTOSAR ICM connects specification con-
recombined these elements and varied their param-
                                                                      straints to metamodel elements and task objects for
eters. This process produced 6 minimal, 7 standard,
                                                                      generation and checking. Constraint extraction from
and 7 full cases. The specification sources and the
                                                                      specifications, metamodel linking, and validator con-
content designed by the authors are documented in
                                                                      struction are described in Appendix A.2, with the
Appendix A.1 and Table A1.
                                                                      extraction setup summarized in Table A3. Figure 6
    Minimal cases focus on a single port and its inter-
                                                                      illustrates the use of a constraint on periodic runnable
face. Standard cases combine multiple ports with
                                                                      execution. Specification rule TPS_SWCT_01519 is
periodic execution behavior. Full cases further com-
                                                                      associated with runnable entities, internal behavior,
bine multiple runnable entities, periods, and access
                                                                      and TimingEvent [28]. Task binding selects the spe-
relationships. These tiers progressively combine con-
                                                                      cific runnable entity. At runtime, an existing timing-
tainment structures, references, and task-specified val-
                                                                      event check determines whether the event exists,
ues, from individual port configurations to compo-
                                                                      whether it targets that runnable entity, and whether
nents with interacting behavioral elements. Each case
                                                                      its period value can be parsed. The single applicable
supplies a requirement description, an author-written
                                                                      object in this check passed validation.
structured task specification, and a catalog of existing
                                                                         The existence of a period does not by itself estab-
interfaces. The specification declares objects, quan-
                                                                      lish that the task is complete. For example, the task
tities, values, and references. The LLM proposes
                                                                      specifies a period of 10 ms. The acceptance checker
task analysis and structured content under constraints
                                                                      reads this expected value from the case requirements
assembled from task bindings, metamodel informa-
                                                                      and compares it with 0.01 s in the ARXML. Even if
tion, the ICM, and existing model context. Deter-
                                                                      the generation plan contains an incorrect period, agree-
ministic procedures apply declared content, normalize
                                                                      ment between the artifact and that plan alone cannot
the intermediate representation, assemble the model,
                                                                      satisfy task acceptance. The ICM preserves the specifi-
and serialize ARXML in the element order required
                                                                      cation basis and applicable metamodel elements. Task
by XSD. Final acceptance checks read the original
                                                                      binding determines the object to be checked, and task
task specification and inspect the resulting artifacts.
                                                                      acceptance checks the specific value required for the
Appendix A.1 details these responsibilities.
                                                                      current task.
    Constructing these models involves containment
hierarchies, collection cardinalities, and references                 4.2.3 Generation results and execution cost
across files. The XML elements in the evaluated
ARXML batch have a maximum nesting depth of 14,                       Each of the 20 requirements was used in three runs. All
counting the root element as level 1. Structured output               60 workflow outputs passed acceptance checks for the
and the serializer therefore jointly construct the model              specified component tasks, producing 255 ARXML
                                                                      files in total. Table 5 summarizes the artifacts, checks,


                                                                 18
            Specification source
                                                           ICM constraint record                               Metamodel elements
            TPS_SWCT_01519                  Source                                              Link
                                                        Retain source text and location                          RunnableEntity
        Periodic execution requires an                   Link classes and XML tags                             SwcInternalBehavior
                    event                              Semantic status: pending review                            TimingEvent
            and a specified period


                                                                           Rule selection                                    Instance
                                                                                                                             correspondence

         Current task and processed                                                                       Component artifact from this
                                                           Task validation context
                    plan                   Declare                                             Locate                run
                                                         Declare TPS_SWCT_01519
            Runnable R; event E                              Bind to runnable R                                  Event E targets R
          Exactly one timing event                           Same case and run                                   PERIOD = 0.01
               Period: 0.01 s                                                                                   Actual ARXML file


                                                                           Rules and objects                                 Actual artifact


                                                                          L2: validation and task acceptance
                         Original task definition              Domain rule checks              Acceptance against the original task
                                                        Event, target reference, period value           Expected: 0.01 s; actual: 0.01 s
                                                         Applicable: 1; checked: 1; passed               Exact period check: passed

           Information link          Input to checking or binding                                                    ASW-FULL-01 ·Run 1


Fig. 6 Links from the specification source of a periodic runnable constraint to model objects and check results. R denotes
RE_Com_Full_Baseline, and E denotes TE_Com_Full_Baseline. The required period of 10 ms is represented as 0.01 s in the artifact

and execution cost. These results cover the complete                        Table 5 Results of the complete AUTOSAR generation workflow
workflow, including task analysis, constrained genera-
tion, deterministic assembly, serialization, and valida-                    Metric                                        Result
tion.                                                                       Generation runs passing task                  60/60
   Acceptance combines XSD validation, domain                               acceptance
checks, and checks against the original component                           ARXML files passing XSD                       255/255
requirements. The checks cover port and interface                           validation
relationships, periodic events, local references, and                       Task-specific structural obligations          2,418, all passed
the objects, values, and access relationships specified                     checked
by the task. Task-specific structural obligations and                       Local references checked                      675, all passed
local references are counted separately in Table 5.
                                                                            Total workflow token usage                    11,967,476
Appendix A.2 describes the configured rules, the
                                                                            Mean time per workflow run                    64.712 s
checks exercised by these tasks, and the acceptance
criteria.
   The controlled repair experiment separately injected
five types of faults into deterministic reference mod-                      could not be injected. Before execution, reference,
els that had passed acceptance checks. The faults were                      port-name, or component-name faults were designated
empty initial values, incorrect initial values, miss-                       for these positions, forming 15 substitute units. All
ing event or internal-behavior paths, missing receiver                      of these were also restored. Results for the core and
communication properties, and incorrect XSD element                         substitute faults are reported in Appendix A.3 and
order. Faults were detected in all 85 applicable units,                     Tables A4 and A5. Appendix A.4 uses actual ARXML
and the affected files were restored to the reference                       fragments to illustrate the generation, acceptance, and
content within one actual repair round, using 661,631                       independent controlled repair of a periodic component.
tokens in total. Some minimal cases lack receiver                              The AUTOSAR generation results address RQ1.
ports or internal behavior, so the corresponding faults                     Constraint sources, metamodel associations, and task


                                                                      19
bindings can be connected to actual generation and              three runs of each of these five cases passed the cor-
checking, producing component models with multiple              responding structural checks and subsequent artifact
containment levels and interrelated references. Con-            checks.
trolled repair provides further engineering evidence for           The 60 paired outputs from the auditing and con-
RQ3. Validation localizes faults in structure, values,          strained decoding conditions were identical byte for
and references. After repair, the artifacts pass revali-        byte. The mean request time was 10.365 s with con-
dation and recover the task properties satisfied by the         strained decoding and 13.252 s with auditing added.
reference artifacts.                                            Total request time increased by 27.85%. Observing the
                                                                generation process therefore incurs an additional exe-
4.3 Decoding interventions by generation                        cution cost. These results address RQ2. L1 intervened
    constraints in AUTOSAR-vLLM                                 in decoding and eliminated the structural violations
                                                                observed under prompt-only constraints in this case
This experiment fixes the AUTOSAR cases and their               set. Execution settings are given in Appendix B.1.
generation constraints to observe the role of L1                Results at the different acceptance stages and request
directly during generation. It compares three condi-            costs are reported in Appendix B.2 and Tables B1
tions. Under prompt-only constraints (U), the require-          through B2.
ments and complete JSON Schema are provided only
in the prompt. Constrained decoding (G) additionally            4.4 Post-generation validation and
enables decoding constraints with the same prompt.
Constrained decoding with auditing (A) records step-
                                                                    bounded repair of railway models
wise decoding information on top of G. All three                4.4.1 Tasks, validators, and comparison
conditions use the same model and sampling settings,                  conditions
with execution order balanced across conditions. The
experiment uses vLLM [30] and XGrammar [19].                    The railway experiment uses the existing metamodel
   Constraints were observed to intervene in token              and six model queries from the Train Benchmark [31].
selection in all 60 audited generations. In each genera-        The authors designed three types of configuration
tion, grammar constraints excluded the highest-scoring          tasks concerning service connections, maintenance
unconstrained token at 7 to 10 steps. Across runs, this         preparation, and redundant monitoring. Each task type
occurred at 516/54,942 evaluable steps, or 0.9392%.             was applied to eight railway layouts, producing 24
Figure 7(a) shows the intervention positions for each           base tasks. Structured task specifications declare fixed
case. The traces of the three runs for the same case            objects, physical connections, assignable fields, and
coincide exactly and are combined into one row. This            task obligations. This information is compiled into
shows that generation constraints narrow the set of             structural plans and generation constraints. The LLM
available tokens during decoding, rather than merely            selects field values, and an adapter assembles the can-
checking format correctness after output completion.            didate model and outputs XMI.
The proportion measures steps at which the local token             Post-generation checks load the XMI directly. EMF
choice was directly affected. It does not measure the           model diagnostics check structure and references, six
proportion of the final output content influenced by the        VIATRA queries check domain relationships, and fur-
constraints.                                                    ther checks assess task obligations and fields that must
   All three conditions produced parseable JSON.                remain unchanged. For example, disabling a route that
Structural acceptance was achieved by 45/60 outputs             must remain active may reduce violations of a domain
under prompt-only constraints and by 60/60 outputs              rule, but task acceptance still rejects the change. The
under both constrained decoding and auditing. Failures          six native queries and their check implementations are
under prompt-only constraints were concentrated in              described in Appendix C.1 and Table C1. Repair con-
five cases and involved arrays being written as objects         ditions and the permitted scope of changes are given in
and incorrect nesting of access references. These errors        Appendix C.2.
show a substantive difference between parseable JSON               Each task was run three times, yielding 72 ini-
and a model representation that conforms to the task            tial generations. The comparison covers initial gen-
structure. With generation constraints enforced, all            eration (G0), self-repair (GS), and repair with vali-
                                                                dation feedback (GF). Self-repair asks the LLM to



                                                           20
                       (a) Decoding interventions                                                   (b) Structural acceptance
                                                                                                             U: Prompt    G: Constrained
                                                                                                                only         decoding

         ASW-MIN-01                                                                                             3/3             3/3
         ASW-MIN-02                                                                                             3/3             3/3
         ASW-MIN-03                                                                                             3/3             3/3
         ASW-MIN-04                                                                                             0/3             3/3
         ASW-MIN-05                                                                                             0/3             3/3
         ASW-MIN-06                                                                                             0/3             3/3
         ASW-STD-01                                                                                             3/3             3/3
         ASW-STD-02                                                                                             3/3             3/3
         ASW-STD-03                                                                                             3/3             3/3
         ASW-STD-04                                                                                             3/3             3/3
         ASW-STD-05                                                                                             3/3             3/3
         ASW-STD-06                                                                                             0/3             3/3
         ASW-STD-07                                                                                             3/3             3/3
        ASW-FULL-01                                                                                             3/3             3/3
        ASW-FULL-02                                                                                             3/3             3/3
        ASW-FULL-03                                                                                             3/3             3/3
        ASW-FULL-04                                                                                             0/3             3/3
        ASW-FULL-05                                                                                             3/3             3/3
        ASW-FULL-06                                                                                             3/3             3/3
        ASW-FULL-07                                                                                             3/3             3/3

                      0%              25%             50%             75%            100%
                                    Decoding progress (% of output steps)


Fig. 7 AUTOSAR-vLLM decoding and output results. (a) The intervention traces of the three audited generations for each case coincide exactly
and are combined into one row per case. Each tick marks a step at which grammar constraints excluded the highest-scoring unconstrained token.
(b) The number of runs passing structural acceptance under prompt-only constraints and constrained decoding, with three runs per case

check and revise its output against the rules, follow-                    models, self-repair recovered 6 and repair with valida-
ing an approach related to the self-revision idea in                      tion feedback recovered 28. One other initial genera-
Self-Refine [24]. The two repair branches start from                      tion produced no model because its initial assignments
the same initial model. GF supplies actual diagnos-                       did not meet the acceptance conditions.
tics, violation locations, and local candidates, and its                     The 21 failures after repair with validation feedback
acceptance policy preserves requirements already sat-                     have identifiable causes in the process. One initial gen-
isfied. The comparison therefore measures the com-                        eration produced no model. The remaining 20 models
bined effect of the feedback and acceptance configu-                      still violated SemaphoreNeighbor, the rule governing
ration. Each branch permits at most two rounds, with                      relationships between boundary signals. Of these, 16
changes to at most six explicit fields per round. Orga-                   proposals were rejected because they caused previ-
nizing repair around inconsistency causes and restrict-                   ously passing checks to fail, the LLM abstained in 3
ing its scope also relates to existing model repair                       cases, and 1 proposal was rejected because it removed
research [23].                                                            no violations. Validation can therefore identify prob-
                                                                          lems and prevent unacceptable changes, but the cur-
4.4.2 Main results and failure analysis                                   rent candidate selection and repair strategies may
                                                                          not find changes that satisfy interdependent require-
As shown in Figure 8(a), the strict success rate
                                                                          ments simultaneously. The result of 51/72 reflects
increased from 23/72 after initial generation to 29/72
                                                                          the observed improvement achieved through accepted
after self-repair and 51/72 after repair with valida-
                                                                          repairs. Repair success remains affected by the candi-
tion feedback. The latter represents an increase of
                                                                          date space and the LLM’s ability to propose changes.
38.89 percentage points over initial generation. Paired
                                                                          Appendix C.4 uses actual XMI fragments to illustrate
success-rate differences on the same tasks and their
                                                                          diagnosis of relationships across objects, repair of a
intervals are reported in Appendix C.2 and Table C3.
                                                                          single field, and revalidation.
Among the 48 failed initial generations that produced


                                                                    21
                              (a) Generation and repair      (b) Repair of injected faults                      (c) LLM comparison
                                   Luna - 3 runs per task          Luna - 3 runs per input                      24 tasks - 1 run per model

                                                                            140/144 141/144
                            100                             100                                   100                          22/24           22/24
  Strict success rate (%)




                                                                  129/144

                                                                                                                18/24
                                                    51/72

                                                                                                                                       13/24
                            50             29/72            50                                     50
                                  23/72                                                                                 8/24
                                                                                                         6/24



                             0                               0                                      0
                                   G0       GS       GF             S         V        F                    G0             GS             GF

                                                                                                                        Luna      Terra


Fig. 8 Railway model results. (a) Two repair strategies applied to 72 initial generations. (b) Self-repair, repair with validation feedback, and
repair with additional information about violation locations on 144 inputs with injected faults. (c) Comparison of Luna and Terra on the same
24 tasks with a fixed seed

   A supplementary experiment compared repair con-                                  second LLM, results by condition, and token usage are
figurations that progressively add validation feedback                              given in Appendix C.3 and Table C4.
and information about violation locations. On the same
inputs with injected faults, it compared self-repair, the                           4.5 Layered checks for structured legal
addition of validation feedback, and the further addi-                                  decisions in private international law
tion of local candidates and dependency information.
The corresponding numbers of successful runs were                                   Private international law (PIL) addresses applicable
129/144, 140/144, and 141/144. Adding local infor-                                  law, jurisdiction, and related issues involving cross-
mation produced one net additional success relative to                              border elements. This experiment examines layered
validation feedback alone. Four units succeeded only                                constraints for jurisdiction decisions, where reliable
with the additional information, while three succeeded                              conclusions are required. It uses a manually defined
only without it, indicating that the benefit varied with                            data model for jurisdiction decisions, including the
the fault conditions. The main text uses repair fol-                                conclusion, forum, jurisdiction types, legal grounds,
lowing initial generation as the principal evidence.                                conditional and abstention flags, reasoning, and miss-
Results for controlled faults, faults in task obliga-                               ing facts. JSON Schema expresses field types, enumer-
tions, and preservation of correct models are given in                              ations, and nested structures. Post-generation checks
Appendix C.2 and Table C2.                                                          assess consistency among the conclusion, jurisdiction
                                                                                    types, and cited provisions and provide diagnostics
4.4.3 Evaluation with a second LLM                                                  for revision. The target output is a structured decision
                                                                                    record conforming to this data model.
On the same 24 tasks with the fixed seed 104729,                                       Two graduate students in private international law
Luna achieved 6, 8, and 13 successful runs for initial                              constructed the case set based on Brussels I bis [32]
generation, self-repair, and repair with validation feed-                           and the EU Trade Mark Regulation [33]. The set
back, respectively. Terra achieved 18, 22, and 22, as                               contains 60 synthetic scenarios covering general and
shown in Figure 8(c). Terra had more successful ini-                                special jurisdiction, jurisdiction agreements, proce-
tial generations, and each of its two repair branches                               dural relationships, and referral to national law. The
recovered four additional tasks. However, the final sets                            students independently reviewed the reference labels,
of successful tasks were not identical. The two tested                              without seeing each other’s judgments in the initial
model configurations exhibited different initial errors                             round, and resolved disagreements through discussion.
and opportunities for repair. A higher initial success                              The reference judgments were established before the
rate does not necessarily lead to a greater benefit from                            experimental generation runs.
validation feedback over self-repair. Settings for the


                                                                               22
   The experiment compares four progressively aug-              4.6 Threats to validity
mented conditions. Basic prompting (P0) provides
                                                                The conclusions are limited by the scope of the tasks
only the common output requirements. Retrieval aug-
                                                                and checks. AUTOSAR evaluates component mod-
mentation (P1) adds legal grounds. Structural con-
                                                                eling, the railway experiment evaluates configuration
straints (P2) further enforce a strict output structure.
                                                                models and six existing queries, and PIL evaluates
Full checks (P3) add post-generation auditing, one
                                                                structured decisions against defined reference require-
repair attempt, and release control. Retrieval augmen-
                                                                ments. Free-text explanations and system behavior
tation follows the idea of retrieval-supported genera-
                                                                after deployment are outside the scope of these checks.
tion discussed in the related work [17]. Each condition
                                                                Although the custom validators were tested, rule inter-
includes three runs for each of the 60 cases, producing
                                                                pretations and task specifications may still reflect bias
180 outputs. Case preparation and the inputs, gen-
                                                                in human judgments. Some specifications are used in
eration, and processing conditions are described in
                                                                both generation and acceptance, which may share the
Appendix D.1 and Table D1.
                                                                same bias. None of the three domain experiments mea-
   The primary endpoint requires a valid decision
                                                                sured person-hours for domain preparation, checker
structure, satisfaction of the common delivery rules,
                                                                development, or human review and intervention. The
compatibility with four requirements derived from the
                                                                reported response times and token usage describe auto-
reference judgments, and actual release of the out-
                                                                mated execution costs and do not establish reductions
put. These reference requirements concern the con-
                                                                in human effort.
clusion, primary jurisdiction type, required provisions,
                                                                   The diversity of the cases and the comparison condi-
and conditional-answer flag. Table 6 presents the main
                                                                tions affect generalizability. AUTOSAR requirements
results. Appendix D.2 and Table D2 further distinguish
                                                                draw on specifications and one engineering example.
valid delivery, actual release, and reference compati-
                                                                Railway tasks combine three task types with eight
bility.
                                                                layouts, share templates, and were available during
   Full checks improved the primary endpoint by
                                                                development. The PIL support library and retriever
23.3 percentage points over structural constraints. The
                                                                were developed on the case set used in the experiment.
95% resampling interval based on paired cases was
                                                                Three repetitions allow observation of variation across
[13.3, 33.9] percentage points. All four comparisons
                                                                runs of the same task. Some repair conditions change
are reported in Appendix D.2 and Table D3. Repair
                                                                both the feedback and the policy for accepting modi-
was triggered for 62 outputs. Of these, 40 changed
                                                                fications, so their effects cannot be attributed entirely
from incompatible to compatible with the reference
                                                                to feedback content. The second LLM was evaluated
judgments and were released, while 3 changed from
                                                                with only one seed. Further evaluation should cover
compatible to incompatible. These results show that,
                                                                more independent tasks, rules, and LLMs, and sepa-
even after structural correctness is achieved, relation-
                                                                rately examine constraint extraction quality, validation
ships between fields may still require post-generation
                                                                coverage, and repair strategies.
checks. They also show the need to repeat acceptance
checks after repair.
   PIL provides application evidence for RQ3 in a deci-         5 Conclusion
sion domain. The same division between generation-
                                                                This paper presented a metamodel-guided model gen-
time restrictions and post-generation checks can be
                                                                eration method with layered constraints. The ICM
used for structured decisions. Free-text legal reason-
                                                                connects metamodel information, structured require-
ing still requires separate evaluation. Targeted expert
                                                                ments from specifications, and their sources. Task
review found that an answer passing the automated
                                                                binding applies this information to concrete objects,
metrics could nevertheless confuse the jurisdiction of
                                                                values, and references. L1 restricts candidate content
courts in a Member State with that of courts in a spe-
                                                                during generation, L2 checks constructed models and
cific city. Actual JSON field revisions and revalidation
                                                                serialized artifacts, and the original task requirements
are illustrated in Appendix D.3. The counterexample
                                                                govern acceptance and repair. Deterministic model
and expert judgments are given in Appendix D.4.
                                                                construction and LLM proposals operate within this
                                                                common constraint basis.
                                                                   The AUTOSAR study examines constraint organi-
                                                                zation, component model generation, and controlled


                                                           23
Table 6 Main PIL results

Condition                          Valid structure                                   Primary composite endpoint

Basic prompting (P0)               180/180                                           73/180 (40.6%)
Retrieval augmentation (P1)        178/180                                           96/180 (53.3%)
Structural constraints (P2)        180/180                                           101/180 (56.1%)
Full checks (P3)                   180/180                                           143/180 (79.4%)


repair. All 60 generation runs passed acceptance                  assumptions. Independent model instances, counterex-
within their declared task scope, and all 255 ARXML               amples, and expert assessment are needed to examine
files passed XSD validation. The separate controlled              faithfulness to the original requirements. Validated
repair experiment restored all 85 core and 15 substitute          resources could then support ICM construction and
fault units. The local AUTOSAR experiment recorded                execution in L1 and L2.
decoding interventions in all 60 audited generations.
The railway study examines relational constraints and             Data and code availability
repair under an existing metamodel. Strict successes
increased from 23/72 initially to 51/72 after repair with         The research data and code are available in the replica-
validation feedback, while the remaining failures illus-          tion package at commit d977c43. They include domain
trate limits of the current repair configuration. The             constraints and their sources, tasks and prompts, gener-
PIL study examines layered checks for structured legal            ated artifacts, validators, repair records, and statistical
decisions. These results show how generation con-                 analysis scripts. The repository README provides
straints, post-generation checks, and task acceptance             navigation in the order of the experiments in Appen-
contribute to the evaluated modeling and decision                 dices A through D, together with offline verification
tasks.                                                            commands, file checksums, and execution reports.
   The method depends on supplied metamodels, gen-
eration mappings, and validation capabilities. Arti-              Appendices
fact mappings remain essential; for example, an
ARXML serializer must enforce XSD element order                   The appendices follow the order of the experiments
when model features are generated as JSON prop-                   in the main text. Appendix A provides further details
erties. None of the three domain experiments mea-                 on AUTOSAR requirement sources, the ICM and val-
sured human effort. Future studies should evaluate                idators, controlled repair, and an engineering exam-
human effort, usability, and practitioner confidence by           ple. Appendix B reports the settings and costs of the
comparing workflows on the same tasks and accep-                  AUTOSAR-vLLM decoding comparison. Appendix C
tance criteria, retain existing configuration and assisted        supplements the railway rules, comparisons, and repair
correction tools, specify permitted LLM assistance,               example. Appendix D describes PIL scoring, expert
and distinguish preparation effort from task execu-               assessments, and the revision of an actual deci-
tion, review, and rework. Further technical evaluation            sion. Appendices A.4, C.4, and D.3 each use actual
should address mapping coverage and repairs involv-               ARXML, XMI, or JSON fragments to illustrate the
ing interdependent requirements.                                  task, generation, diagnosis, repair, and revalidation.
   Recent work on model and metamodel construc-                   The units of analysis, aggregation of repeated runs,
tion [6], semantically guided generation [21], and                and resampling settings for the main comparisons are
formal specification generation [25] motivates extend-            described in C.2 and D.2. Complete paired data, sta-
ing domain preparation. One direction is to gener-                tistical scripts, and sensitivity analyses are available in
ate domain metamodels from natural-language spec-                 the replication package.
ifications and assess whether their concepts, rela-
tionships, multiplicities, and well-formedness require-
ments express the intended tasks. Another is to
generate formal specifications and checking imple-
mentations with explicit applicability conditions and



                                                             24
A AUTOSAR model generation                                      interface document contains 10 elements. The max-
  and repair                                                    imum nesting depth is 14, counting the AUTOSAR
                                                                root as level 1. One output for the largest case, ASW-
A.1 Requirement design and generation                           FULL-06, contains seven documents with 175 ele-
    settings                                                    ments in total. These counts refer to XML element
                                                                nodes. Attributes, text, and repeated copies are not
The 20 requirements were designed using the Software            counted separately.
Component Template and the Specification of RTE
for AUTOSAR Classic 4.2.2 [28] [29]. The former                 A.2 Constraint extraction, ICM, and
defines components, ports, communication specifica-
                                                                    validators
tions, internal behaviors, and reference structures. The
latter informs the interpretation of periodic triggering        Domain preparation for AUTOSAR used the text
and explicit data access. Combinations of interfaces            of Chapters 2–13 of the Software Component Tem-
and behaviors observed in an RH850 project using                plate and the associated metamodel information [28].
the ETAS toolchain provided engineering context.                The authors annotated chapters, relevant classes, and
The authors removed project-specific context, normal-           enumerations. The system added the corresponding
ized names, decomposed and recombined elements,                 attributes and enumeration literals from the trans-
and varied parameters to construct the three tiers in           formed metamodel representation and organized con-
Table A1.                                                       textual input fragments by chapter and paragraph. The
   The normative basis for the initial value is con-            LLM extracted structured constraints and their target
str_1201 in the Software Component Template, with               elements from these inputs. The linker automatically
its usage explained by TPS_SWCT_01220 [28]. The                 checked target classes, attributes, and enumeration lit-
value 0 is a specific task-design choice. Together, the         erals and established references. Exceptions arising
20 base cases require 33 provided ports, 32 required            during automatic linking were examined and handled
ports, 18 runnable entities, 18 timing events, and              by humans before the formal experiments. Table A3
55 variable accesses. Detailed case provenance and              summarizes this preparation process.
design descriptions are included in the replication                The model generation experiment used fixed ICM
package.                                                        resources containing 1,085 structured constraints,
   Generation used gpt-5.6-luna with low reasoning              6,533 constraint associations, 11,177 structural nodes,
effort, a temperature of 1.0, strict structured output,         and 14,106 structural relationships. The ICM retains
and a maximum output budget of 128,000 tokens.                  specification provenance and links to metamodel ele-
The three fixed seeds were 104729, 130363, and                  ments. Task execution uses this information to select
155921. Each author-written structured specification            relevant constraints and bind specific objects.
was accompanied by an English requirement descrip-                 The validation plan contains 554 checking rules,
tion and an existing interface catalog. The task speci-         comprising 400 Python backend rules and 154 declar-
fication supplied the declared objects and values used          ative rules. In this component task set, 11–24 rules
in generation and acceptance. The LLM produced task             completed checks on actual objects in an individual
analysis and constrained structured content, while the          run, with 24 distinct rules doing so across all 60 runs.
adapter applied fixed content and constructed the tar-          Other rules had no matching objects or lacked the
get artifacts. Table A2 summarizes the responsibilities.        context required for evaluation, including complete
Generation evaluation and controlled repair were con-           reference information. The report for the full config-
ducted separately.                                              ured rule corpus therefore retained an INCOMPLETE
   Before serialization, deterministic processing               decision, separately from task acceptance.
applied 1,734 task obligations and performed 527                   Task acceptance uses the component scope declared
intermediate-representation normalization or recovery           before generation. XSD validation and the explicitly
operations across 49 of the 60 runs. The generation             required domain checks must complete and pass. Fail-
results include these operations as part of the complete        ures or execution errors in any other executed domain
workflow.                                                       check also prevent acceptance. Required judgments
   The 60 generation runs produced 60 component                 that cannot be completed leave the task unaccepted.
files and 195 interface files. Individual component             The final artifact is additionally checked against the
documents contain 11–115 XML elements, and each


                                                           25
Table A1 Design and sources of the AUTOSAR requirements

Content                              Source                                            Design procedure

Interfaces and ports                 Three provided interfaces, three required         Recombine interfaces and normalize
                                     interfaces, and their data elements in the        names
                                     engineering project
Period and reception timeout         Engineering baseline values of 0.01 s and 0.3     Vary period and timeout parameters
                                     s, respectively
Initial value                        constr_1201 requires an initial value for the     Use the author-selected value 0
                                     selected nonqueued receiver communication         throughout
                                     specification
Minimal tier, 6 cases                A single port and its interface                   Construct either a provided port or a
                                                                                       required port
Standard tier, 7 cases               Ports, periodic execution, and access             Combine 2–3 ports, one runnable entity,
                                     relationships                                     and a timing event
Full tier, 7 cases                   Multiple interfaces and internal behaviors        Combine six ports, 1–3 runnable
                                                                                       entities, and period variations


Table A2 Responsibilities in the AUTOSAR generation experiment

Stage                                      Responsibility

Case preparation                           Authors specify task objects, quantities, values, and references; the interface catalog
                                           supplies existing model context.
LLM task analysis                          Propose the structure and design content needed for the task under the supplied
                                           specification.
Constraint assembly                        Procedures combine task bindings, metamodel information, and ICM resources into
                                           generation constraints.
Constrained generation                     The LLM returns structured content under the submitted constraints.
Deterministic construction                 Procedures apply declared content, normalize the intermediate representation,
                                           construct objects and relationships, and serialize ARXML.
Acceptance                                 Check the resulting ARXML against applicable rules and the original task
                                           requirements.


Table A3 Setup for AUTOSAR constraint extraction and linking

Item                                          Description

Source material                               Identified provisions, normative descriptions, and relevant examples in the
                                              selected chapters, with provision identifiers and chapter provenance retained
Terminology context                           The fragment and its parent chapters, relevant metamodel classes and attributes,
                                              and enumerations and their literals
Structured output                             Constraint identifier, content, type, values, related provisions, and candidate
                                              target classes, attributes, or enumerations
Automatic linking                             Resolve target names, check types and member ownership, and establish
                                              references from constraints to metamodel elements
Exception handling                            Have humans examine unresolved or ambiguous links and adjust target
                                              associations and record uses
Subsequent use                                Retrieve constraints by element association and task relevance, and connect them
                                              to generation and validation through existing mappings and check
                                              implementations



                                                                 26
original task specification. All 60 generation runs               54,993 tokens. Some insertion repairs generated con-
passed these acceptance conditions.                               tent in stages, so a single repair round could involve
    Custom checks were written by humans with LLM                 multiple responses.
assistance. The authors consulted the specifications to
determine applicable objects, decision conditions, and            A.4 Worked example of periodic
diagnostic locations, selected implementations, and                   component construction and event
tested them with satisfying, violating, and boundary
                                                                      reference repair
cases. Declarative operations address ranges, enumer-
ations, multiplicities, existence, and references. Ded-           Task and domain basis. ASW-FULL-01 requires the
icated checks address relationships across objects. At            component ASW_Com_Full_Baseline with three pro-
runtime, check instances are assembled from rule iden-            vided ports, three required ports, and six interfaces.
tifiers and the current object bindings. Validation code          One runnable entity performs three reads and three
is not regenerated for each task.                                 writes every 10 ms. The requirement also specifies
    Post-generation validation first checks the actual            a receiver initial value of 0 and a timeout of 0.3 s.
ARXML against the AUTOSAR XSD, then resolves                      The metamodel provides internal behaviors, runnable
local references and executes applicable domain rules.            entities, TimingEvents, and their containment and ref-
The task acceptance checker reads component names,                erence relationships. TPS_SWCT_01519 in the ICM
port sets, interface references, initial values, timeouts,        provides the basis for checking events associated with
runnable entities, periods, and read/write relationships          a runnable entity declared to execute periodically [28].
from the case specification and compares them with                   Task binding, L1, and assembly. Task analysis binds
the actual artifacts. Agreement between the artifacts             the internal behavior, runnable entity, and event to
and the generation plan is checked separately. For                IB_Com_Full_Baseline, RE_Com_Full_Baseline, and
example, a timing event being parseable does not                  TE_Com_Full_Baseline, respectively. It also deter-
establish that its period is correct. If the task requires        mines the interfaces, variable accesses, and refer-
10 ms, the acceptance checker must also verify that the           ence targets. L1 assembles a generation schema from
actual value is 0.01 s.                                           the metamodel and these selections to constrain
                                                                  the required objects and containment hierarchy. The
A.3 Core and substitute faults                                    adapter assembles the structured result, inserts the
                                                                  bound fixed values, and serializes the model in the ele-
Controlled repair used reference artifacts that were              ment order required by the XSD. The result is one
constructed deterministically from the cases and the              component ARXML file and six interface ARXML
XSD and had passed acceptance checks. Five fault                  files.
slots were assigned to each base case. Fixed core oper-              The following excerpt from the component pro-
ations were applied to the 85 slots with applicable               duced in the first experimental generation run shows
target objects. Executable substitute operations were             the event reference and the actual runnable entity dec-
specified before the runs for the remaining 15 slots.             laration. The component and its ancestors are omit-
Repair was limited to two rounds, and every unit was              ted, and a comment identifies the omitted read/write
completed within one round in the observed runs.                  accesses. Only indentation and line breaks around the
   Substitute operations were needed when the target              reference text have been adjusted. The reference itself
structure was absent. For example, a case contain-                is complete.
ing only provided ports has no receiver initial value
to empty. Similarly, a case without a runnable entity
or event cannot receive a fault in the corresponding
path. Table A5 lists the substitute operations that were
executed. Each row covers three cases.
   The reference file sets and their byte contents were
restored in 85/85 core units and 15/15 substitute units.
The core set used 109 model responses and 661,631
tokens. The substitute set used 21 responses and




                                                             27
Table A4 Repair results for core faults

Fault                              Units                             Detected                         Reference content restored

Empty initial value                17                                17                               17
Incorrect initial value            17                                17                               17
Missing event or                   14                                14                               14
internal-behavior path
Missing receiver                   17                                17                               17
communication specification
Incorrect XSD element order        20                                20                               20
Total                              85                                85                               85


Table A5 Substitute operations declared before execution

Cases                              Original core operation           Substitute operation             Units restored

MIN-01 to MIN-03                   Empty the initial value           Empty the provided-interface     3/3
                                                                     reference
MIN-01 to MIN-03                   Set an incorrect initial value    Change the                       3/3
                                                                     provided-interface reference
                                                                     to a nonexistent path
MIN-01 to MIN-03                   Remove the receiver               Delete the provided port         3/3
                                   communication specification
MIN-01 to MIN-03                   Remove the event or               Delete the component name        3/3
                                   internal-behavior path
MIN-04 to MIN-06                   Remove the event or               Delete the required-interface    3/3
                                   internal-behavior path            reference

Excerpt A1 Timing event and runnable entity from the                     periodic-execution rule was evaluated for one applica-
experimental generation run                                              ble runnable entity and passed. Task acceptance sep-
                                                                         arately compared the actual period of 0.01 s with the
                                                                         required 10 ms and checked the port set and read/write
<SWC-INTERNAL-BEHAVIOR>
  <SHORT-NAME>IB_Com_Full_Baseline</SHORT-NAME>                          relationships. Event existence, reference resolution,
  <EVENTS>                                                               and the correctness of task-specific parameters were
    <TIMING-EVENT>
      <SHORT-NAME>TE_Com_Full_Baseline</SHORT-NAME>                      therefore checked separately.
      <START-ON-EVENT-REF DEST="RUNNABLE-ENTITY">
        /Components/ASW_Com_Full_Baseline/IB_Com_Full_Bas ⌋                 Separate controlled fault injection. For the same
        eline/RE_Com_Full_Baseline                                       requirement, a fault was separately injected into an
      </START-ON-EVENT-REF>
      <PERIOD>0.01</PERIOD>
                                                                         accepted, deterministically constructed reference com-
    </TIMING-EVENT>                                                      ponent by removing the internal-behavior segment
  </EVENTS>
  <RUNNABLES>                                                            from the event reference. The affected content is shown
    <RUNNABLE-ENTITY>                                                    below.
      <SHORT-NAME>RE_Com_Full_Baseline</SHORT-NAME>                      Excerpt A2 Event reference after separate controlled
      <!-- Three read and three write VARIABLE-ACCESS
      entries omitted -->                                                fault injection
    </RUNNABLE-ENTITY>
  </RUNNABLES>
</SWC-INTERNAL-BEHAVIOR>
                                                                         <START-ON-EVENT-REF DEST="RUNNABLE-ENTITY">
                                                                           /Components/ASW_Com_Full_Baseline/RE_Com_Full_Baseline
   L2 and task acceptance. The experimental gener-                       </START-ON-EVENT-REF>
ation run passed XSD validation for all seven doc-
uments, 22 local-reference checks, and 61 structural                       The damaged artifact still passed XSD validation,
obligations defined by the case on its first attempt. The                but local-reference resolution could not find the tar-
                                                                         get. The periodic-execution check reported that the


                                                                    28
runnable entity lacked an associated TimingEvent, and             Table B1 Structural acceptance by case tier
task acceptance also failed. Repair targeted the event’s
reference text and restored the complete path using the           Case tier       U prompt         G             A decoding
bound target by reinserting IB_Com_Full_Baseline.                                 only             constrained   and
After serialization, revalidation passed in one round.                                             decoding      auditing
The file set and byte contents of the component and               Minimal, 6      9/18             18/18         18/18
six interfaces were restored to those of the reference            cases×3 runs
artifacts. This unit demonstrates separate controlled             Standard, 7     18/21            21/21         21/21
repair. The experimental generation run itself had                cases×3 runs
already passed on its first attempt.                              Full, 7         18/21            21/21         21/21
                                                                  cases×3 runs
B AUTOSAR-vLLM decoding                                           Total, 20       45/60            60/60         60/60
                                                                  cases×3 runs
  interventions
B.1 Comparison conditions and execution
    settings                                                         All 60 audited generations contained steps at which
                                                                  the grammar excluded the highest-scoring uncon-
The experiment used Qwen3.5-9B, vLLM [30], and                    strained token. There were 7–10 such steps per gener-
XGrammar [19] on two RTX 4090 GPUs with ten-                      ation and 516/54,942 steps in total. All 60 output pairs
sor parallelism set to 2. The temperature was 0, top_p            from the auditing condition and ordinary constrained
was 1, and thinking, speculative decoding, and pre-               decoding were byte-identical. Table B2 compares out-
fix caching were disabled. The maximum output was                 put volume and request time.
16,384 tokens. Each of the 20 cases used three fixed
seeds, yielding 60 blocks. Each of the six execu-
                                                                  Table B2 Tokens and request time
tion orders for prompt-only constraints U, constrained
decoding G, and decoding with auditing A was used in
                                                                  Metric          U                G             A
ten blocks.
   All three conditions received the same requirement,            Total output    73,644           54,942        54,942
output instructions, and complete JSON Schema in                  tokens
their prompts. U provided the constraints only through            Mean output     1,227.4          915.7         915.7
the prompt. G additionally enforced them through the              tokens per
decoding backend. A also recorded interventions at                request
each step. The generation constraints were derived                Total request   811.519          621.901       795.092
from fixed case structures and specified fields, arrays,          time/s
nesting, and values. These inputs were held fixed to              Mean request    13.525           10.365        13.252
examine the effect of enforcing decoding constraints.             time/s

B.2 Results by tier and execution cost
In the prompt-only condition, three minimal cases                    Auditing added a mean request time of 2.887 s
represented an array of receiver communication spec-              and a median of 2.634 s. Cumulative request time
ifications as an object. One standard case and one                increased by 27.85%. These times are measured per
full case had incorrectly nested access references. All           model request and are separate from the end-to-end
three repetitions failed for each of these five cases. The        AUTOSAR workflow times reported in the main text.
remaining cases passed structural checks and subse-
quent artifact acceptance. With decoding constraints
enforced, all tiers passed. At the base-case level, five
cases improved and fifteen were unchanged.




                                                             29
C Railway model generation and                                      Across the 48 fixed-damage inputs, all three repeti-
  repair                                                         tions passed for 38 inputs under S and 45 inputs under
                                                                 each of V and F.
C.1 Model sources and checks                                        Task-obligation faults invert the route activation
                                                                 state required by the task. They comprise 16 cases
The experiment reused the Train Benchmark meta-                  with an incorrectly deactivated route and 8 with an
model and six VIATRA queries [31]. The authors                   incorrectly activated route. These inputs still pass the
designed three task families for service connections,            native domain queries but fail to satisfy the task. This
maintenance preparation, and redundant monitoring                comparison makes the contribution of task acceptance
and applied them to eight layouts comprising chains,             separately observable. The correctness-preservation
branching and merging tracks, cycles, self-loops,                set checks whether repair retains results that already
shared switches, separated lines, multiple regions, and          satisfy the requirements.
branching cycles. The 24 structured task specifications             Of the 49 failed initial generations in the main
contain English task descriptions and were available             experiment, 48 produced models. GF repaired 28 of
during development. They define objects, fixed phys-             these models. All 20 remaining models still violated
ical connections, assignable fields, and the service             SemaphoreNeighbor. The stopping reasons were 16
states and monitoring relationships that must be pre-            proposals rejected for causing regression in existing
served. The system combines these structured require-            checks, 3 abstentions, and 1 proposal that removed
ments with metamodel information to construct task               no violation. The initial-assignment stage rejected 1
constraints and a structural plan and to bind the cur-           further starting point. The current process prevents
rent objects and values. Domain checks use the six               changes that cause regression but did not find an
VIATRA queries from commit 9c76520 of the oﬀicial                acceptable repair for every combination of relation-
Train Benchmark repository. Table C1 summarizes the              ships.
rule conditions implemented in that version.                        Results are paired by condition within each base
   After checking field domains and reference scopes,            task. Repeated runs and the corresponding faults are
the generated output is assembled into XMI. Valida-              first aggregated within each task, and success-rate dif-
tion loads that XMI directly, performs EMF model                 ferences are then calculated with equal weight for each
diagnostics and VIATRA queries, and cross-checks                 of the 24 tasks. In Table C3, the difference is the
the match sets against independently implemented                 first condition minus the second, expressed in percent-
relational queries. Task acceptance separately checks            age points. Intervals are estimated from 9,999 paired
prescribed states, relationships, and protected content.         resamples of the base tasks. A nominal error level of
                                                                 0.05 is allocated across four comparisons, with each
C.2 Conditions and supplementary sets                            comparison reporting a nominal marginal percentile
The main experiment used gpt-5.6-luna with low rea-              interval of 1 − 0.05/4 = 98.75%. The three repetitions
soning effort, a temperature of 1.0, a maximum output            remain within their respective tasks, and the number of
budget of 128,000 tokens, and three fixed seeds. Initial         base tasks is 24.
generation G0 was followed by two branches, self-                   For example, repair with validation feedback and
repair GS and repair with validation feedback GF. In             self-repair succeeded in 51/72 and 29/72 runs, respec-
the controlled sets, self-repair S received the public           tively, a difference of 30.56 percentage points. For
rules, the current model, and the permitted fields, using        controlled damage, adding localization information to
a self-inspection approach related to Self-Refine [24].          validation feedback yielded one net additional success.
V added validation feedback and an acceptance cri-               The interval for this difference includes zero and does
terion that prevented regression. F further provided             not establish a clear additional benefit. The statisti-
violation locations, local candidates, and dependency            cal documentation in the replication package includes
information. Each branch allowed at most two rounds,             a sensitivity analysis based on resampling the eight
with changes to at most six explicit fields per round.           railway layouts, complete paired records, and analysis
Execution could stop early after rejection or a lack of          scripts.
progress.                                                           The 72 responses for G0 used 371,575 tokens and
                                                                 a total response time of 812.54 s. GS added 81
                                                                 responses, 464,875 tokens, and 799.19 s. GF added
                                                                 48 responses, 335,937 tokens, and 635.40 s. The


                                                            30
Table C1 The six native queries

Query                                            Property checked in this experiment

PosLength                                        Segment lengths are positive
SwitchMonitored                                  Every switch is monitored by a sensor
SwitchSet                                        For an active route whose entry signal is GO, prescribed switch positions agree
                                                 with their actual positions
RouteSensor                                      A route requires the sensors that monitor the switches in its prescribed switch
                                                 settings
ConnectedSegments                                No sensor monitors every segment in a directed walk of six segments; vertices
                                                 need not be distinct
SemaphoreNeighbor                                Adjacent track elements monitored by sensors required by different routes satisfy
                                                 the shared boundary-semaphore relationship specified by the original query



Table C2 Experimental sets and strict success

Set                               Input size                         Conditions                    Strict success

Generation                        Three runs for each of 24          G0/GS/GF                      23, 29, and 51, each out of 72
                                  tasks, yielding 72 starting
                                  points
Fixed damage                      One single-fault and one           S/V/F                         129, 140, and 141, each out
                                  compound-fault input per                                         of 144
                                  task; the compound inputs
                                  include 12 with coupled faults
                                  and 12 with concurrent faults;
                                  each input is run three times
Task-obligation faults            24 inputs, each run three times    S/V/F                         67, 69, and 72, each out of 72
Correctness preservation          3 correct inputs, each run         S/V/F                         9/9 for each condition
                                  three times



Table C3 Success-rate differences and intervals in the main railway experiment

Comparison                             Difference in percentage points                   98.75% resampling interval in
                                                                                         percentage points

Generated models, repair with          +38.89                                            [22.22, 56.94]
validation feedback − initial
generation
Generated models, repair with          +30.56                                            [15.28, 47.22]
validation feedback − self-repair
Controlled damage, repair with         +8.33                                             [0.00, 19.44]
validation feedback and
localization − self-repair
Controlled damage, repair with         +0.69                                             [−3.47, 5.91]
validation feedback and
localization − repair with
validation feedback




                                                                   31
cost of a complete repair branch includes its shared            constraints that restrict sensor requirements to declared
initial-generation cost and the additional cost of that         candidates such as n1–n6. The initial model gener-
branch. Across all sets, the main railway experiment            ated with seed 155921 selected r1.requires=[n1,n3]
retained 1,074 responses totaling 6,118,127 tokens and          and r2.requires=[n2,n3] and was assembled into the
8,840.70 s.                                                     following XMI.
                                                                   The excerpt preserves the original references. Only
C.3 Second model and execution cost                             line breaks have been adjusted, and surrounding and
                                                                unrelated nodes have been omitted. XMI identifiers
The second model was gpt-5.6-terra with low reason-             must be interpreted through the identity mapping.
ing effort and the fixed seed 104729. It used the same          Identifiers n12 and n13 correspond to routes r1 and
24 tasks, checks, permitted fields, and repair-round            r2; n4, n5, and n6 correspond to domain sensors n1,
limit. Luna results for the same tasks and seed provide         n2, and n3; n15 and n16 correspond to t2 and t3; and
the comparison.                                                 n1, n2, and n3 correspond to semaphores m_boundary,
                                                                m_in, and m_out. Thus, the original requires="n4
Table C4 Results for two LLMs on the same tasks                 n6" represents [n1,n3] at the domain level.
                                                                Excerpt C1 Initial XMI and route fields after repair
Condition         Luna strict success     Terra strict
                                          success
                                                                <!-- G0: excerpt of sensors, adjacent segments, and two
G0, no repair     6/24 (25.0%)            18/24 (75.0%)         routes -->
                                                                <sensors xmi:id="n5" id="5" monitors="n15 n21" />
GS, self-repair   8/24 (33.3%)            22/24 (91.7%)         <sensors xmi:id="n6" id="6" monitors="n16" />
                                                                <elements xmi:id="n15" id="15" xsi:type="railway:Segment"
GF, repair with   13/24 (54.2%)           22/24 (91.7%)           connectsTo="n16" monitoredBy="n5" length="40">
validation                                                        <semaphores xmi:id="n1" id="1" signal="GO" />
                                                                </elements>
feedback                                                        <routes xmi:id="n12" id="12" active="true" entry="n2"
                                                                exit="n1" requires="n4 n6">
                                                                  <follows xmi:id="n10" id="10" position="DIVERGING"
                                                                  target="n20" route="n12" />
                                                                </routes>
   All 18 initial Terra successes were preserved. Each          <routes xmi:id="n13" id="13" active="true" entry="n1"
                                                                exit="n3" requires="n5 n6">
of GS and GF repaired four of the six failed start-               <follows xmi:id="n11" id="11" position="DIVERGING"
                                                                  target="n21" route="n13" />
ing points. The two branches both succeeded on 21               </routes>
tasks and both failed on one task. Each also succeeded          <!-- GF: only r1.requires changes; r2, monitoring, and
                                                                connections are preserved -->
on one task on which the other failed. The supple-              <routes xmi:id="n12" id="12" active="true" entry="n2"
mentary runs had a maximum completion budget of                 exit="n1" requires="n4 n5">
                                                                  <follows xmi:id="n10" id="10" position="DIVERGING"
4,096 tokens, and all responses in this batch completed           target="n20" route="n12" />
within that limit. Luna and Terra used different output         </routes>
budgets, so the comparison reflects each LLM’s results
                                                                   L2 successfully loaded the initial XMI, and EMF
under its own execution configuration.
                                                                diagnostics reported no structural errors. The other five
   The 60 retained Terra responses used 338,438
                                                                native queries passed. SemaphoreNeighbor returned
tokens, comprising 301,834 input tokens and 36,604
                                                                the following violation, with parameters ordered as
output tokens.
                                                                the semaphore, two routes, two sensors, and two track
                                                                elements.
C.4 Worked example of relational repair                         Excerpt C2 Relational-check diagnostic for the initial
    for two service routes                                      model
BAL-1-01 requires two active routes, r1 and r2, on
a fixed chain of six segments. Physical connections,            SemaphoreNeighbor: FAIL
                                                                tuple = [m_out, r2, r1, n2, n3, t2, t3]
prescribed switch positions, and specified monitor-
ing must be preserved. Sensor n1 monitors w1 and                   In this case, t2→t3 are monitored by n2, required
t1, n2 monitors w2 and t2, and n3 monitors t3. Each             by r2, and n3, required by r1, respectively. This trig-
route must require at least two distinct sensors. The           gers the requirement that the exit of r2 and the entry
structured task specification fixes the objects and con-        of r1 refer to the same semaphore. Their actual values
nections. The program uses it to assemble generation


                                                           32
are m_out and m_in. Using the diagnostic and local                and whether references belong to the permitted evi-
candidates, GF changed only r1.requires to [n1,n2], as            dence. P3 gives the model the original facts, the same
shown in the second part of the excerpt. Revalidation             evidence, the original answer, and the diagnostics and
recorded empty match sets for all six queries. Both               permits one revision. If revalidation still fails, a record
routes remained active, and all seven task obligations            indicating that the output was withheld is retained.
and protected-content checks passed. The proposal                    The primary composite endpoint requires valid
passed repair acceptance and achieved strict success              structure, compliance with the common delivery rules,
after one round. L1 restricted the reference candidates,          compatibility with four requirements derived from the
L2 checked relationships across objects, and repair               reference judgments, and actual release. These require-
acceptance preserved the service task.                            ments check the selected conclusion, primary juris-
                                                                  diction type, required evidence, and conditional flag.
D Private international law                                       The evidence requirement is satisfied when the cited
                                                                  evidence has at least one item in common with the
  decisions                                                       nonempty required set. These four field comparisons
                                                                  do not fully assess free-text legal reasoning.
D.1 Cases and comparison conditions                                  The P3 records that passed delivery checks include
The PIL experiment used 60 synthetic jurisdiction sce-            four records of withheld outputs. There were 176
narios written in English and constructed by two grad-            actual releases and 143 results meeting the primary
uate students in private international law. They inde-            endpoint. Repair was triggered in 62 units. Of these,
pendently reviewed the initial reference labels without           40 changed from incompatible to compatible with the
seeing each other’s judgments and then discussed dis-             reference judgments and were released, and 42 repair
agreements. The cases were based on the consolidated              units ultimately met the primary endpoint. A further
text of Brussels I bis dated 26 February 2015 [32]                3 changed from compatible to incompatible. Field
and the consolidated text of the EU Trade Mark Reg-               compatibility and compliance with delivery rules are
ulation dated 1 December 2025 [33]. The data model                therefore counted separately.
defines decision fields, jurisdiction types, and rela-               Table D3 reports differences in the primary com-
tionships among them based on these provisions. A                 posite endpoint for the same cases under the four
decision contains a list of legal grounds, each identified        conditions. The three runs are first aggregated within
by a legal instrument and a provision. Enumerations               each case, and differences between conditions are then
define the available conclusion and jurisdiction types,           calculated. Paired resampling uses the 60 cases as
while separate rules relate the selected values across            its units, with 20,000 resamples and 95% percentile
fields. A support library organized 58 provision para-            intervals. Each sampled case retains its corresponding
phrases. References identify both the legal instrument            results under all conditions.
and the provision, and a fixed lexical retrieval proce-              Full checks produced 42 more results meeting the
dure returns at most 12 provisions.                               primary endpoint than structural constraints alone,
   Each condition used gpt-5.6-luna with low reason-              corresponding to 23.3 percentage points. Adding struc-
ing effort, a temperature of 1.0, a maximum output                tural constraints alone yielded a difference of 2.8
budget of 128,000 tokens, and three fixed seeds, yield-           percentage points, whose interval includes zero. The
ing 180 results per condition. Neither the model nor the          replication package retains a sensitivity analysis using
auditor read the reference answers at runtime. Refer-             31 design-source groups and adjusted tests for the four
ence judgments were fixed for the cases before gener-             comparisons.
ation, and model outputs were subsequently evaluated                 Mean citation F1 scores for P0–P3 were 0.449,
using common metrics.                                             0.720, 0.712, and 0.692, respectively. Mean token use
                                                                  per planned unit was 1,177.39, 1,465.77, 1,746.33, and
D.2 Auditing and results                                          2,392.31, respectively, with P3 including additional
                                                                  repair. Full checks achieved a higher primary end-
The auditor was written by humans with LLM assis-                 point, while citation overlap and cost followed different
tance. It checks field types, enumerations, primary               patterns.
and alternative jurisdiction types, defined relation-
ships between conclusions and selected provisions,



                                                             33
Table D1 Generation conditions

Condition                          Input evidence                      Structural enforcement              Post-generation processing

Basic prompting (P0)               Case facts and common               Prompt instructions                 Parse and check structure
                                   output requirements
Retrieval augmentation (P1)        Add retrieved legal evidence        Prompt instructions                 Parse and check structure
Structural constraints (P2)        Same as P1                          Strict schema                       Check structure and release
Full checks (P3)                   Same as P1                          Strict schema                       Audit, one repair,
                                                                                                           revalidation, and release
                                                                                                           control


Table D2 Results for four conditions with 180 results per condition

Condition        Valid structure          Valid delivery          Actual release          Reference                 Primary composite
                                                                                          compatibility             endpoint

P0               180 (100.0)              91 (50.6)               180 (100.0)             74 (41.1)                 73 (40.6)
P1               178 (98.9)               117 (65.0)              178 (98.9)              102 (56.7)                96 (53.3)
P2               180 (100.0)              118 (65.6)              180 (100.0)             105 (58.3)                101 (56.1)
P3               180 (100.0)              180 (100.0)             176 (97.8)              144 (80.0)                143 (79.4)


Table D3 Success-rate differences and intervals for the PIL primary composite endpoint

Comparison                              Difference in percentage points                      95% resampling interval in
                                                                                             percentage points

Retrieval augmentation − basic          +12.8                                                [2.2, 23.3]
prompting
Structural constraints − retrieval      +2.8                                                 [−3.3, 9.4]
augmentation
Full checks − structural                +23.3                                                [13.3, 33.9]
constraints
Full checks − basic prompting           +38.9                                                [27.8, 50.0]


D.3 Worked example of revising the type                                    agreement, whereas the submitted type exclusive
    of a choice-of-court decision                                          also lacked the provision required by its encoded rule.
                                                                           The revision input contained the original facts, the
Facts and structured generation. In case8, both parties                    same retrieved evidence, the initial answer, and both
are domiciled in Italy and agree on the jurisdiction of                    diagnostics. At most one attempt was permitted. The
Swedish courts, but one party brings proceedings in                        excerpts below show the relevant fields from the ini-
Italy. P3 run 1 retrieved provisions including Article                     tial and revised answers, preserving the original keys,
25 and 25(1) of Brussels I bis and generated a deci-                       values, and order of the cited provisions.
sion record from the same facts and evidence. Strict
output structure constrained the fields and enumera-
tions. The initial JSON passed structural checks and
concluded that jurisdiction should be declined in favor
of the chosen court.
   Observed diagnostics. The auditor identified a mis-
match between the conclusion and the primary juris-
diction type. This conclusion requires the primary type



                                                                      34
Excerpt D1 Relevant fields of the initial decision               jurisdiction [32]. The conditional flag should evalu-
record                                                           ate the selected conclusion itself, for which the pre-
                                                                 scribed encoding is false. The model’s original true
                                                                 value reflected its interpretation of the latter question.
{
    "conclusion": "Decline_in_favor_of_chosen_court",            Its substantive explanation was acceptable, but this
    "forum": "Swedish courts",                                   judgment was not used to alter the original automated
    "forum_type": "exclusive",
    "alternative_forum_types": ["agreement"],                    endpoint.
    "legal_basis": [
      {"instrument": "BRUSSELS_I_BIS", "provision":                 In case42, a French consumer purchases furniture
      "Art.25"},                                                 online from a Dutch trader and separately confirms
      {"instrument": "BRUSSELS_I_BIS", "provision":
      "Art.25(1)"}                                               a clause selecting Amsterdam courts. The first P1
    ]                                                            answer inferred jurisdiction of the specific courts in
}
                                                                 Amsterdam directly from domicile in the Netherlands.
Excerpt D2 Relevant fields after one revision                    The experts found that the subsequent text did not cor-
                                                                 rect this error and judged the answer unacceptable,
                                                                 although it passed the automated endpoint. The first
{                                                                P3 answer later made the entire conclusion explicitly
    "conclusion": "Decline_in_favor_of_chosen_court",
    "forum": "Swedish courts",                                   conditional on the consumer rules and the require-
    "forum_type": "agreement",                                   ments for a choice-of-court agreement. The experts
    "alternative_forum_types": ["exclusive"],
    "legal_basis": [                                             judged it conditionally acceptable. A consumer’s sep-
      {"instrument": "BRUSSELS_I_BIS", "provision":
      "Art.25"},
                                                                 arate confirmation of the clause does not automatically
      {"instrument": "BRUSSELS_I_BIS", "provision":              satisfy Articles 19 and 25(4) [32]. This comparison
      "Art.25(1)"}
    ]
                                                                 shows why the structured endpoint and a substantive
}                                                                assessment of the complete answer must be interpreted
                                                                 separately.
   Revalidation and release. The revision exchanged
                                                                    These judgments are linked to specific cases and
the primary and alternative types while retaining the
                                                                 original answers and clarify the scope of the scor-
forum, conclusion, and listed evidence. Both struc-
                                                                 ing. Complete cases, task configurations, generated
tural checks and auditing passed on revalidation, and
                                                                 artifacts, evaluation results, and analysis entry points
the record was released. It changed from incom-
                                                                 are retained for the four experimental tracks in the
patible to compatible with the reference judgments
                                                                 accompanying replication package.
and met the primary composite endpoint. In this
study, agreement represents jurisdiction based on
a choice-of-court agreement, while the primary type              References
exclusive denotes the predefined category of statu-
                                                                  [1] Kahani, N., Bagherzadeh, M., Cordy, J.R., Din-
tory exclusive jurisdiction. This revision does not deny
                                                                      gel, J., Varró, D.: Survey and classification of
the possible exclusive effect of a choice-of-court agree-
                                                                      model transformation tools. Software & Systems
ment under Article 25(1) [32]. The example illustrates
                                                                      Modeling 18(4), 2361–2397 (2019) https://doi.
checking and revision of relationships across fields
                                                                      org/10.1007/s10270-018-0665-6
after structural validity has been established.
                                                                  [2] Di Rocco, J., Di Ruscio, D., Di Sipio, C., Nguyen,
D.4 Targeted expert review                                            P.T., Rubei, R.: On the use of large language
In addition to automated scoring, experts conducted                   models in model-driven engineering. Software
a targeted review of three specific answers for case19                and Systems Modeling 24(3), 923–948 (2025)
and case42. In case19, the defendant is domiciled only                https://doi.org/10.1007/s10270-025-01263-8
in China, and the scenario excludes the exceptions
                                                                  [3] World Wide Web Consortium: XML Schema
listed in Article 6(1). Jurisdiction must therefore be
                                                                      Part 1: Structures Second Edition. W3c recom-
determined under German domestic law. The avail-
                                                                      mendation, World Wide Web Consortium (Octo-
able facts do not establish whether that law confers
                                                                      ber 2004). 28 October 2004. https://www.w3.o
                                                                      rg/TR/2004/REC-xmlschema-1-20041028/



                                                            35
 [4] Poesia, G., Polozov, A., Le, V., Tiwari, A.,           [11] Alaoui Mdaghri, A., Ouederni, M., Chaari, L.:
     Soares, G., Meek, C., Gulwani, S.: Synchromesh:             MDE in the Era of Generative AI. In: Ben Hedia,
     Reliable Code Generation from Pre-Trained Lan-              B., Ghazel, M., Monsuez, B. (eds.) Verification
     guage Models. In: Iclr 2022 (2022)                          and Evaluation of Computer and Communication
                                                                 Systems, pp. 113–127. Springer, Cham (2025)
 [5] Chen, B., Wei, O., Zheng, B., Mussbacher, G.:
     Accurate and Consistent Graph Model Genera-            [12] Petrovic, N., Pan, F., Lebioda, K., Zolfaghari, V.,
     tion from Text with Large Language Models. In:              Kirchner, S., Purschke, N., Khan, M.A., Vorobev,
     2025 ACM/IEEE 28th International Conference                 V., Knoll, A.: Synergy of Large Language Model
     on Model Driven Engineering Languages and                   and Model Driven Engineering for Automated
     Systems (MODELS), pp. 130–141 (2025). https:                Development of Centralized Vehicular Systems.
     //doi.org/10.1109/MODELS67397.2025.00018                    arXiv (2024). https://doi.org/10.48550/ARXIV
                                                                 .2404.05508 . https://arxiv.org/abs/2404.05508
 [6] Almonte</a>, Iván Rengifo</a>, Guerra</a>,
     Lara</a>: EMF-Kaizen: an intelligent assis-            [13] El-Gnainy, N., Shanouda, M., Essam, A.,
     tant for domain-specific modelling and meta-                Ibrahim, A.A., William, J., Elsharkawy, M.,
     modelling. Journal of Object Technology 25(3),              Moustafa, P.A., Al Ansary, M., Mahmoud, H.,
     3–99112 (2026) https://doi.org/10.5381/jot.2026             Moro, A., Salama, C.: AI-Enhanced AUTOSAR
     .25.3.a8 . ECMFA 2026 Journal First                         Configuration: Eﬀicient Methods for Dataset
                                                                 Generation and Automated Code Production.
 [7] Object Management Group: Object Constraint                  In: 2024 IEEE 8th Forum on Research and
     Language, Version 2.4. OMG Specification                    Technologies for Society and Industry Inno-
     formal/2014-02-03, Object Management Group                  vation (RTSI), pp. 214–219 (2024). h t t p s :
     (February 2014). https://www.omg.org/spec/O                 //doi.org/10.1109/RTSI61910.2024.10761393
     CL/2.4/PDF
                                                            [14] Samy, A., Moro, A., Taher, M.: Automating
 [8] Object Management Group: XML Metadata                       AUTOSAR BSW Configuration Generation with
     Interchange (XMI) Specification, Version 2.5.1.             Fine-Tuned LLMs and a Compact Intermediate
     OMG Specification formal/2015-06-07, Object                 Representation. Applied Sciences 16(17) (2026)
     Management Group (June 2015). https://www.                  https://doi.org/10.3390/app16178443
     omg.org/spec/XMI/2.5.1/PDF
                                                            [15] Abukhalaf, S., Hamdaqa, M., Khomh, F.:
 [9] Ma, T., Dai, S., Gao, Y., Xu, F., Fang, L.: A               PathOCL: Path-Based Prompt Augmenta-
     Dual-Stage Framework for Behavior-Enhanced                  tion for OCL Generation with GPT-4. In:
     Automated Code Generation in Industrial-Scale               Proceedings of the 2024 IEEE/ACM First
     Meta-Models. IEEE Access 13, 170943–170959                  International Conference on AI Foundation
     (2025) https://doi.org/10.1109/ACCESS.2025.                 Models and Software Engineering. FORGE
     3614174                                                     ’24, pp. 108–118. Association for Comput-
                                                                 ing Machinery, New York, NY, USA (2024).
[10] Semeráth, O., Nagy, A.S., Varró, D.: A graph                https://doi.org/10.1145/3650105.3652290
     solver for the automated generation of consis-
     tent domain-specific models. In: Proceedings of        [16] Winkler, S., Pilgrim, J.: A survey of traceability
     the 40th International Conference on Software               in requirements engineering and model-driven
     Engineering. ICSE ’18, pp. 969–980. Associa-                development. Software & Systems Modeling
     tion for Computing Machinery, New York, NY,                 9(4), 529–565 (2010) https://doi.org/10.1007/s1
     USA (2018). https://doi.org/10.1145/3180155.                0270-009-0145-0
     3180186




                                                       36
[17] Lewis, P., Perez, E., Piktus, A., Petroni, F.,             [23] Marchezan, L., Kretschmer, R., Assunção,
     Karpukhin, V., Goyal, N., Küttler, H., Lewis, M.,               W.K.G., Reder, A., Egyed, A.: Generating
     Yih, W.-t., Rocktäschel, T., Riedel, S., Kiela, D.:             repairs for inconsistent models. Software and
     Retrieval-augmented generation for knowledge-                   Systems Modeling 22(1), 297–329 (2023)
     intensive NLP tasks. In: Proceedings of the 34th                https://doi.org/10.1007/s10270-022-00996-0
     International Conference on Neural Information
     Processing Systems. NIPS ’20. Curran Asso-                 [24] Madaan, A., Tandon, N., Gupta, P., Hallinan,
     ciates Inc., Red Hook, NY, USA (2020)                           S., Gao, L., Wiegreffe, S., Alon, U., Dziri, N.,
                                                                     Prabhumoye, S., Yang, Y., Gupta, S., Majumder,
[18] Geng, S., Josifoski, M., Peyrard, M., West, R.:                 B.P., Hermann, K., Welleck, S., Yazdanbakhsh,
     Grammar-Constrained Decoding for Structured                     A., Clark, P.: Self-Refine: Iterative Refinement
     NLP Tasks without Finetuning. In: Bouamor, H.,                  with Self-Feedback. In: Oh, A., Naumann, T.,
     Pino, J., Bali, K. (eds.) Proceedings of the 2023               Globerson, A., Saenko, K., Hardt, M., Levine, S.
     Conference on Empirical Methods in Natural                      (eds.) Advances in Neural Information Process-
     Language Processing, pp. 10932–10952. Asso-                     ing Systems, vol. 36, pp. 46534–46594. Curran
     ciation for Computational Linguistics, Singapore                Associates, Inc. (2023). https://doi.org/10.52202
     (2023). https://doi.org/10.18653/v1/2023.emnlp                  /075280-2019
     -main.674 . https://aclanthology.org/2023.emnl
     p-main.674/                                                [25] Ma, L., Liu, S., Li, Y., Xie, X., Bu, L.: Spec-
                                                                     Gen: Automated Generation of Formal Program
[19] Dong, Y., Ruan, C.F., Cai, Y., Xu, Z., Zhao,                    Specifications via Large Language Models. In:
     Y., Lai, R., Chen, T.: XGrammar: Flexible and                   Proceedings of the IEEE/ACM 47th International
     Eﬀicient Structured Generation Engine for Large                 Conference on Software Engineering. ICSE ’25,
     Language Models. In: Zaharia, M., Joshi, G., Lin,               pp. 16–28. IEEE Press (2025). https://doi.org/10
     Y. (eds.) Proceedings of Machine Learning and                   .1109/ICSE55347.2025.00129
     Systems, vol. 7. MLSys (2025)
                                                                [26] Wright, A., Andrews, H., Hutton, B.: JSON
[20] Li, L., Dong, Y., Wang, G., Xu, Z., Jiang, A.,                  Schema Validation: A Vocabulary for Structural
     Chen, T.: XGrammar-2: Dynamic and Eﬀicient                      Validation of JSON. Internet-Draft draft-
     Structured Generation Engine for Agentic LLMs.                  bhutton-json-schema-validation-01,        Internet
     In: Proceedings of the ACM Conference on                        Engineering Task Force (June 2022). Work in
     AI and Agentic Systems. CAIS ’26, pp. 1009–                     Progress. https://datatracker.ietf.org/doc/draft-b
     1022. Association for Computing Machinery,                      hutton-json-schema-validation/01/
     New York, NY, USA (2026). https://doi.org/10
     .1145/3786335.3813124                                      [27] Tolvanen, J.-P., Kelly, S., Di Rocco, J., Pieranto-
                                                                     nio, A., Tinella, G.: A framework for evaluating
[21] Chen, B., López, J.A.H., Babikian, A.A.: Pro-                   tool support for co-evolution of modeling lan-
     jectional Decoding: Towards Semantic-Aware                      guages, tools and models. Software and Systems
     LLM Generation, pp. 1277–1281. Association                      Modeling 24(2), 311–338 (2025) https://doi.org/
     for Computing Machinery, New York, NY, USA                      10.1007/s10270-024-01218-5
     (2026). https://doi.org/10.1145/3803437.380557
     1                                                          [28] AUTOSAR: Software Component Template.
                                                                     Standard 062, AUTOSAR (July 2015). Classic
[22] Park, K., Wang, J., Berg-Kirkpatrick, T., Polikar-              Platform Release 4.2.2; 31 July 2015. https://ww
     pova, N., DAntoni, L.: Grammar-Aligned Decod-                   w.autosar.org/fileadmin/standards/R4.2.2/CP/
     ing. In: Globerson, A., Mackey, L., Belgrave,                   AUTOSAR_TPS_SoftwareComponentTemplat
     D., Fan, A., Paquet, U., Tomczak, J., Zhang, C.                 e.pdf
     (eds.) Advances in Neural Information Process-
     ing Systems, vol. 37, pp. 24547–24568. Curran              [29] AUTOSAR: Specification of RTE. Standard 084,
     Associates, Inc. (2024). https://doi.org/10.52202               AUTOSAR (July 2015). Release 4.2.2; 31 July
     /079017-0774                                                    2015. https://www.autosar.org/fileadmin/standa
                                                                     rds/R4.2.2/CP/AUTOSAR_SWS_RTE.pdf


                                                           37
[30] Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng,
     L., Yu, C.H., Gonzalez, J., Zhang, H., Stoica, I.:
     Eﬀicient Memory Management for Large Lan-
     guage Model Serving with PagedAttention. In:
     Proceedings of the 29th Symposium on Oper-
     ating Systems Principles. SOSP ’23, pp. 611–
     626. Association for Computing Machinery, New
     York, NY, USA (2023). https://doi.org/10.1145/
     3600006.3613165

[31] Szárnyas, G., Izsó, B., Ráth, I., Varró, D.: The
     Train Benchmark: cross-technology performance
     evaluation of continuous model queries. Soft-
     ware & Systems Modeling 17(4), 1365–1393
     (2018) https://doi.org/10.1007/s10270-016-057
     1-8

[32] European Parliament and Council of the Euro-
     pean Union: Regulation (EU) No 1215/2012 of
     the European Parliament and of the Council of
     12 December 2012 on jurisdiction and the recog-
     nition and enforcement of judgments in civil and
     commercial matters (recast). Oﬀicial Journal of
     the European Union, L 351, 20 December 2012,
     pp. 1–32. Consolidated text of 26 February 2015
     (2012). https://eur-lex.europa.eu/eli/reg/2012/12
     15/2015-02-26/eng

[33] European Parliament and Council of the Euro-
     pean Union: Regulation (EU) 2017/1001 of the
     European Parliament and of the Council of 14
     June 2017 on the European Union trade mark
     (codification) (Text with EEA relevance). Oﬀicial
     Journal of the European Union, L 154, 16 June
     2017, pp. 1–99. Consolidated text of 1 December
     2025 (2017). https://eur-lex.europa.eu/eli/reg/2
     017/1001/2025-12-01/eng




                                                          38
