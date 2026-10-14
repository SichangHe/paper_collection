                                         Compositional Symbolic Execution
                                         for the Next 700 Memory Models (Extended Version)
                                         ANDREAS LÖÖW, Imperial College London, United Kingdom
                                         SEUNG HOON PARK, Imperial College London, United Kingdom
                                         DANIELE NANTES-SOBRINHO, Imperial College London, United Kingdom
                                         SACHA-ÉLIE AYOUN, Imperial College London, United Kingdom
                                         OPALE SJÖSTEDT, Imperial College London, United Kingdom
arXiv:2508.15576v2 [cs.PL] 27 Aug 2025




                                         PHILIPPA GARDNER, Imperial College London, United Kingdom
                                         Multiple successful compositional symbolic execution (CSE) tools and platforms exploit separation logic (SL) for
                                         compositional verification and/or incorrectness separation logic (ISL) for compositional bug-finding, including
                                         VeriFast, Viper, Gillian, CN, and Infer-Pulse. Previous work on the Gillian platform, the only CSE platform
                                         that is parametric on the memory model, meaning that it can be instantiated to different memory models,
                                         suggests that the ability to use custom memory models allows for more flexibility in supporting analysis of a
                                         wide range of programming languages, for implementing custom automation, and for improving performance.
                                         However, the literature lacks a satisfactory formal foundation for memory-model-parametric CSE platforms.
                                            In this paper, inspired by Gillian, we provide a new formal foundation for memory-model-parametric CSE
                                         platforms. Our foundation advances the state of the art in four ways. First, we mechanise our foundation (in
                                         the interactive theorem prover Rocq). Second, we validate our foundation by instantiating it to a broad range
                                         of memory models, including models for C and CHERI. Third, whereas previous memory-model-parametric
                                         work has only covered SL analyses, we cover both SL and ISL analyses. Fourth, our foundation is based on
                                         standard definitions of SL and ISL (including definitions of function specification validity, to ensure sound
                                         interoperation with other tools and platforms also based on standard definitions).
                                         CCS Concepts: • Theory of computation → Logic and verification; Automated reasoning; Separation
                                         logic; Program reasoning.
                                         Additional Key Words and Phrases: symbolic execution, memory model, separation logic, incorrectness logic
                                         ACM Reference Format:
                                         Andreas Lööw, Seung Hoon Park, Daniele Nantes-Sobrinho, Sacha-Élie Ayoun, Opale Sjöstedt, and Philippa
                                         Gardner. 2025. Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version). Proc.
                                         ACM Program. Lang. 9, OOPSLA2, Article 373 (October 2025), 46 pages. https://doi.org/10.1145/3763151

                                         1   Introduction
                                         Multiple successful analysis tools and platforms provide compositional verification and/or composi-
                                         tional bug-finding for heap-manipulating programs, including VeriFast [21], Viper [37], Gillian [19,
                                         31, 34], CN [44], Infer-Pulse [26], by animating their automated and semi-automated reasoning
                                         using compositional symbolic execution (CSE) grounded on ideas from separation logic (SL) [39, 48]
                                         Authors’ Contact Information: Andreas Lööw, Imperial College London, London, United Kingdom, a.loow@ic.ac.uk;
                                         Seung Hoon Park, Imperial College London, London, United Kingdom, s.park23@ic.ac.uk; Daniele Nantes-Sobrinho,
                                         Imperial College London, London, United Kingdom, d.nantes-sobrinho@ic.ac.uk; Sacha-Élie Ayoun, Imperial College
                                         London, London, United Kingdom, s.ayoun17@ic.ac.uk; Opale Sjöstedt, Imperial College London, London, United Kingdom,
                                         opale.sjostedt23@ic.ac.uk; Philippa Gardner, Imperial College London, London, United Kingdom, p.gardner@ic.ac.uk.




                                         This work is licensed under a Creative Commons Attribution 4.0 International License.
                                         © 2025 Copyright held by the owner/author(s).
                                         ACM 2475-1421/2025/10-ART373
                                         https://doi.org/10.1145/3763151


                                                                    Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:2                                  A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


and/or incorrectness separation logic (ISL) [45] (usually bottoming out in a call to an underlying
SMT solver, such as Z3 [14]). In this case, compositional (or functionally compositional) reasoning
means that it is scalable in that the analysis works on functions in isolation, at any point in the
codebase, and then records the results in simple function specifications that can be used in broader
calling contexts. SL provides a good grounding for sound verification (proving the absence of bugs)
through compositional over-approximate (OX) reasoning; ISL provides a good grounding for sound
bug-finding (proving the presence of bugs) through compositional under-approximate (UX) reason-
ing. Important examples of CSE analyses based on the two logics include OX function-specification
verification (implemented in, e.g., VeriFast, Viper, Gillian, and CN) and UX true bug-finding based
on bi-abduction [26] (implemented in, e.g., Infer-Pulse and Gillian).
   A key challenge with the design of CSE platforms that aim for wide applicability is to manage the
diverse range of memory models employed across different applications.1 This need for different
memory models arises from multiple sources. First, of course, different programming languages
are defined over different language memory models. Second, different analyses are defined over
different types of memory ghost state, e.g., ghost state for different kinds of ownership disciplines,
such as exclusive ownership vs. fractional ownership, or negative-information ghost state used
in UX analyses to ensure UX compositionality. Third, even choosing the programming language
and the analysis still does not determine the memory model: there is no one-size-fits-all memory
models because the different axes of the memory-model design space are often-times in antagonistic
relationship with each other: e.g., the choice of what part of the language to be analysed, accuracy
and abstraction level of the model, implementation effort of the model, performance of the model,
and automation/annotation burden associated with the analysis of the model. We cannot move freely
along different axes in the design space and therefore must solve a difficult trade-off problem when
selecting a memory model to use: e.g., a complex memory model might give better performance
than a simple memory model but will require more implementation effort.
   The analysis platform Gillian stands out as the only CSE platform that faces this memory-model
challenge head-on. Gillian is the only CSE platform that is parametric on the memory model,
meaning that no memory model is hard-coded into the platform and instead the platform can be
instantiated to different memory models, depending on which model has the best position in the
model design trade-off space for a situation at hand. All other CSE platforms are monomorphic on the
memory model in that they only support one fixed memory model that has been hard-coded into the
platform. It is therefore awkward, or impossible, to use the memory model that is most appropriate
for a situation at hand since it must be encoded into the fixed memory model of the platform.
   Literature gap. No previous work provides a satisfactory formal foundation for CSE platforms
that are parametric on the memory model; in particular, a formal foundation for Gillian’s approach
to memory-model parametricity is missing. There was some initial work on the foundations of
Gillian [19, 34], which outlined mathematical definitions and gave a sketch of a soundness proof
for parts of the CSE engine of Gillian. This work, however, suffers from four weaknesses:
   (1) it was not mechanised;
   (2) it did not prove that any of their memory-model instances were sound, and thus did not
       validate their definitions and conjectures;
   (3) it only covered SL-based analyses, not ISL-based analyses;
   (4) it did not use standard SL definitions, such as the definition of function specification validity,
       thus making the engine awkward to interoperate with other analysis tools and platforms.

1 To avoid confusion: whereas some authors reserve the term memory model for weak-memory concurrency, we use the

term broadly in this work (the many different ways of representing, updating, and analysing the heap).


Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                             373:3


Table 1. Summary of our memory-model instances. The columns “OX” and “UX” specify whether the model is
OX sound and/or UX sound; “Rocq kLoc” specifies the size of the Rocq proof script file for the model; “Origin”
specifies which CSE platforms have implemented the model. The star (“*”) in the Rocq column for the OOP
model specifies that we did not mechanise the model because of its large overlap with the block-offset model,
and the double star (“**”) for the CHERI model specifies that the mechanised proof only covers OX soundness
(UX soundness is left for future work because of the size of the task).


 Memory-model name                                      §     OX     UX     Rocq kLoC              Origin
 Linear model (running example in paper)    6.1                ✓      ✓          1
 Linear model with unique-match branching 6.1                  ✓      ✓          1
 Linear model with cut branching            6.1                       ✓        ≈ 0.5
 Linear model without negative information 6.1                 ✓               ≈ 0.5
 Fractional ownership model                 6.2                ✓      ✓          2
 Block-offset model for C                   6.3                ✓      ✓          4                Gillian
 Model for OOP languages (e.g., JavaScript) 6.4                ✓      ✓         0*                Gillian
 CHERI-assembly model                       6.5                ✓      ✓        19**            New model
 VeriFast-and-Viper-inspired model for C    6.6                ✓               ≈ 0.5        VeriFast and Viper


Other previous work on the foundations of CSE have only covered tools and platforms that are
monomorphic on the memory model [13, 22, 31, 58]. (We discuss related work in more detail in §7.)
   Contribution. In this paper, we contribute a new CSE theory that addresses all four weaknesses in
the current formal foundations of CSE platforms that are parametric on the memory model. Our new
CSE theory is inspired by the design of Gillian but is independent of its particular implementation;
we have designed our theory to be a CSE analogue of separation logics that are parametric on the
memory model, such as abstract separation logic [11] and subsequent generic/modular/parametric
separation-logic frameworks like the views framework [15, 46] and, perhaps the most well-known
example, the Iris framework [24].
   An important strength of our CSE theory is that it is remarkably simple; in fact, its definitions
and metatheory are not much more complex than existing monomorphic CSE theories. This suggests
that, while there are clear advantages, there are no clear disadvantages in making CSE platforms
parametric on the memory model.
   Technically, our new CSE theory, which we have mechanised in Rocq [49], consists of:
     • a definition of “memory model” in the CSE setting, including, two sets of OX and UX soundness
        requirements on memory models;
     • a formal semantics for a CSE engine that is parametric on the memory model;
     • two soundness results for the engine: if a memory model satisfies our OX/UX soundness
        requirements, then the engine is OX/UX sound when instantiated with the memory model.
   To validate our CSE theory and show that it has broadly applicability, we instantiate our theory
to a broad collection of memory models ranging from models for low-level languages like assembly
and C to high-level languages like JavaScript, as summarised in Tab. 1. In more detail: in §6.1 and
§6.2, we cover the standard models used in theoretical investigations into SL and ISL, which we
call linear memory models. In §6.1, we show that multiple variants of these linear memory models
fit into our theory, including OX-and-UX sound models, OX-only models, and UX-only models.
In §6.2, to show that different ownership disciplines fit into our theory, we instantiate our theory
with a linear memory model implementing fractional ownership rather than standard exclusive
ownership. In §6.3, we shift the discussion towards more realistic memory models, starting of the

                         Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:4                                 A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


discussion with a memory model inspired by the memory model of the CompCert compiler. The
memory model is implemented in Gillian and has been used in Gillian-based teaching. In §6.4,
to show that memory models for high-level languages like object-oriented languages also fit our
theory, we discuss the JavaScript memory model implemented in Gillian. In §6.5, we discuss a new
memory model for CHERI, which is the largest model we have mechanised. As this model is new
and, hence, has not been implemented in any CSE platform, the model shows that new models can
be designed using only our CSE theory as guidance. Lastly, in §6.6, to show broad CSE platform
coverage, we discuss the hard-coded memory model of VeriFast and Viper.
   Our main technical contributions can be summarised as follows:
      • We provide the first foundation of CSE platforms that are parametric on the memory model (§5)
        that: (1) is mechanised, (2) is validated, (3) covers both SL- and ISL-based analyses, and
        (4) is interoperable.
      • We demonstrate that two important analyses can be soundly hosted on top of our memory-
        model-parametric CSE engine (§5): namely, OX function-specification verification; and UX
        true bug-finding based on bi-abduction.
      • We discuss instantiations of our CSE theory (§6), as summarised in Tab. 1.
      • We make available all source code and proofs of our Rocq mechanisation of our CSE theory
        and its instantiations in the artefact of this paper (see our data-availability statement).
   Scope limitations and caveats. For this paper, we only consider sequential memory models not
concurrent memory models. We, however, believe our work is a useful starting point for future
work on symbolic execution of different concurrent memory models. Additionally, we work with a
simple demonstrator programming language, specifically, a memory-model-parametric variant of
a standard (sequential) imperative language. In other words, to focus the discussion on our core
contribution, which is memory-model parametricity, we do not vary other parts of the language.

2     Overview
In this section, we highlight the main takeaways of our new CSE theory. To be able to do so, we
give a compressed overview of our theory. The core contribution of our theory is that it is parametric
on a set of parameters that factors out its memory-model dependent part; the focus in this section
is therefore these parameters.

2.1     Background: Monomorphic CSE Theory
Before introducing our new memory-model-parametric CSE theory, we give a summary of tra-
ditional memory-model-monomorphic CSE theory. The judgements we use in the summary are
simplified judgements from our theory.
   Engine architecture. In this paper, we work specifically with CSE engines implementing the
consume-produce engine architecture. This is the architecture implemented by Gillian and other
similar modern CSE engines like VeriFast and Viper. In this architecture, two operations called
consume and produce are used to implement the execution of commands/constructs based on
assertions (separation-logic points-to assertions, etc.), which are the commands/constructs making
the engine a compositional engine, such as using function specifications to reason about function
calls. In short, the consume operation takes as input an assertion and removes (“consumes”) the
corresponding symbolic state from the engine’s current symbolic state and the produce operation
also takes as input an assertion but instead adds (“produces”) the corresponding symbolic state to
the current symbolic state. For example, to execute a function call using a function specification,
the precondition of the specification is first consumed and its postcondition is then produced.

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                             373:5


  Judgements. Assuming we work with (a monomorphised version of) our demonstrator language,
a monomorphic CSE theory needs to specify at least the following judgements:
      • 𝜎, C ⇓ 𝜎 ′ – judgement for the concrete semantics of the language, where C denotes a language
        command, 𝜎 is a concrete input state, and 𝜎 ′ is a concrete output state.
      • 𝜎 |= 𝐴 – judgement for the satisfaction relation for assertions (used to, e.g., define the
        semantics of function specifications).
         ˆ C ⇓ 𝜎ˆ ′ – judgement for the CSE engine, i.e., the symbolic semantics of the language, where
      • 𝜎,
        𝜎ˆ and 𝜎ˆ ′ are symbolic states.
      • 𝜎 |= 𝜎ˆ – judgement for the satisfaction relation for symbolic states, i.e., the relation between
        concrete and symbolic states.
The two important operations consume and produce are part of the definition of the symbolic
              ˆ C ⇓ 𝜎ˆ ′ .
engine, i.e., 𝜎,
   Definition of soundness. There are two standard soundness statements that relate the concrete and
symbolic execution judgements: OX soundness and UX soundness [3] (although different papers use
different terminology). OX soundness is the following relation between the two types of execution:
                             𝜎, C ⇓ 𝜎 ′ ∧ 𝜎 |= 𝜎ˆ ⇒ ∃𝜎ˆ ′, 𝜎,
                                                           ˆ C ⇓ 𝜎ˆ ′ ∧ 𝜎 ′ |= 𝜎ˆ ′ .
Intuitively, the relation enforces that all states reachable by concrete execution are reachable by sym-
bolic execution, i.e., symbolic reachability overapproximates concrete reachability. UX soundness
enforces the opposite relation, where, note, the universal quantification is over the final states:
                             ˆ C ⇓ 𝜎ˆ ′ ∧ 𝜎 ′ |= 𝜎ˆ ′ ⇒ ∃𝜎, 𝜎, C ⇓ 𝜎 ′ ∧ 𝜎 |= 𝜎.
                             𝜎,                                               ˆ
  In more analysis application-oriented terms: OX soundness is a good foundation for verification
and UX soundness is a good foundation for bug-finding. E.g., for verification: it follows from OX
soundness that if we have proved that a behaviour (such as a bug) is unreachable using symbolic
execution, then the behaviour is also unreachable by concrete execution.

2.2    The Step to Parametric CSE Theory
We now discuss how our CSE theory parameterises the judgements and soundness statements
introduced above. We differentiate between two types of parameters, which we also refer to as
instance data: instance definitions (abbreviation: “IDefs”) and instance properties (abbreviation:
“IProps”). Additionally, we group the parameters into the following four abstractions:
  (1) concrete memory model (CMM) – the parameters of 𝜎, C ⇓ 𝜎 ′ (concrete semantics);
  (2) resource model (RM) – the parameters of 𝜎 |= 𝐴 (satisfaction relation for assertions);
  (3) symbolic memory model (SMM) – the parameters of 𝜎,       ˆ C ⇓ 𝜎ˆ ′ (symbolic semantics/engine)
      and 𝜎 |= 𝜎ˆ (satisfaction relation for symbolic states);
  (4) OX and UX soundness relations (RELs) between CMMs, RMs, and SMMs – the parameters of
      the soundness proofs of the engine.
  Fig. 1 depicts the dependency structure of the four abstractions (blue boxes) and the engine
definition and its soundness proofs (grey boxes). All IDefs. and IProps. parameters are summarised,
respectively, in Tab. 2 and Tab. 3. We now introduce the parameters in more detail.
  Concrete memory model and resource model. Because a CSE engine and a program logic for the
same language have the same trusted computing base, the parameters of the concrete language and
the assertion language of our CSE theory are the same as for comparable memory-model-parametric
separation logics such as abstract separation logic [11] (we are here speaking in terms of big-picture

                         Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:6                                     A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


 CSE engine                        CSE engine                        Table 2. Summary of required IDefs.
 OX sound                          UX sound

   OX REL         CSE engine         UX REL             #    Abs.      Description
                                                        1    CMM       Memory data type, empty memory, and
                      SMM                                              composition operator
                                                        2    CMM       Concrete semantics of memory actions
                       RM                               3    RM        Resource satisfaction relation
                                                        4    SMM       Memory data type and empty memory
                     CMM
                                                        5    SMM       Memory satisfaction relation
                                                        6    SMM       Symbolic semantics of memory actions
                                                        7    SMM       Semantics of consumeRes and produceRes
Fig. 1. Dependency structure of our theory.

    Table 3. Summary of required IProps., where the “Deps.” column specifies the IDefs. dependencies.


        #    Abs.       Deps.                      Description
        1    CMM 1                                 Memory forms a partial commutative monoid (PCM)
        2    CMM 1 and 2                           Memory actions satisfy OX/UX frame properties
        3    REL All except 3 and 7                OX/UX soundness of symbolic memory actions
        4    REL All except 2 and 6                OX/UX soundness of consumeRes and produceRes


ideas, of course parameter details differ between different program logics). Therefore, we discuss
the two abstractions concrete memory model and resource model together.
   A concrete memory model, i.e., the parameters of 𝜎, C ⇓ 𝜎 ′ (concrete language), specifies: the
data type of memory (IDef. 1) and the memory actions and their semantics (IDef. 2). Examples
of common memory actions include memory read, memory write, allocation, etc. Analogous to
the setup in program logics, we require that the data type of memory comes with a composition
operator that forms a PCM together with the data type (IProp. 1) such that we can build the standard
separation-logic infrastructure on top of the language. Additionally, to ensure that the concrete
language satisfies the standard separation-logic frame properties, we require that the memory
actions satisfy frame properties (IProp. 2) that we have derived from the standard properties.
   A resource model, i.e., the parameters of 𝜎 |= 𝐴 (satisfaction relation for assertions), specifies:
the resource assertions for the memory-model instance and their satisfaction relation (IDef. 3).2
These resource assertions are the assertions that differ between memory models, the remaining
assertion language is fixed. E.g., one common type of resource assertion is points-to assertions for
heap cells (usually denoted E1 ↦→ E2 ). An alternative approach, followed by the original work on
Gillian [34], is to define the meaning of assertions in terms of consume and produce instead of a
traditional satisfaction relation. This approach requires less instance data but makes the theory
awkward to connect to other formalisms since the meaning of assertions is nonstandard.

  Takeaway. Concrete memory models and resource models should look familiar; they are
  analogous to instance data also required by memory-model-parametric separation logics.

2 Our assertions are deeply embedded because our CSE engine must be able to pattern match over their structure. Note that

some presentations of memory-model-parametric separation logics (e.g., the abstract separation logic paper [11]) shallowly
embed their assertions, i.e., do not include an explicit satisfaction relation and instead define assertions to be sets of state.


Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                             373:7


   Symbolic memory model. A symbolic memory model, i.e., the parameters of 𝜎,     ˆ C ⇓ 𝜎ˆ ′ (symbolic
semantics/engine), specifies: the data type of symbolic memory (IDef. 4) and the satisfaction relation
for symbolic memory (IDef. 5); the symbolic semantics of memory actions over the memory (IDef. 6);
additionally, the consume and produce operations of the engine are parametrised by consumeRes
and produceRes operations for the resource assertions of the memory model (IDef. 7).
   Note that, in contrast to concrete memories, we do not require that symbolic memories form
PCMs or satisfy any frame properties. This is unlike the original work on Gillian [34], which defined
concrete and symbolic memory models uniformly and therefore required the same instance data
for both, i.e., required more instance data than us. Our work shows that the IDefs. and IProps. of a
parametric CSE theory can be stated such that symbolic PCM and frame data is not needed for
either the definition of the theory’s engine or for its soundness proofs; instead, in the theory, all
PCM reasoning and frame reasoning can be carried out at the concrete level.

    Takeaway. Symbolic memory models and concrete memory models have different parameters
    and should therefore not be treated uniformly.

  OX and UX soundness relations. Our soundness relations, i.e., the parameters of the soundness
proofs, tie together concrete memory models, resource models, and symbolic memory models.
The OX soundness of our CSE engine (Thm. 5.2) follows from a series of OX IProps., while UX
soundness (Thm. 5.3) follows from a series of UX IProps. Specifically, we define what it means for
symbolic memory actions (IProp. 3) and the consumeRes and produceRes operations (IProp. 4) to be
OX sound and require this as instance data. See again Tab. 3, which specifies which IDefs. each
IProp. ties together. We give analogous IProps. for UX soundness.

    Takeaway. From the Gillian implementation we know that the definition of a CSE engine can be
    built on top of a symbolic memory model, this paper shows that the same is true of the soundness
    proof of the engine; i.e., the soundness proof of the engine can be built on top of the soundness
    requirements for symbolic memory models as we define them in this paper (i.e., our IProps.).

    Takeaway. Additionally, our work shows that it is possible to make a clear separation between
    OX and UX soundness requirements and lift the two to the full engine independently of each
    other. In other words, OX soundness and UX soundness are independent of each other.

2.3     Structure of Rest of Paper
The rest of the paper is structured as follows. In §3 to §5, we formally and incrementally present
the parameters of our CSE theory. Throughout this presentation, we use a simple linear memory
model as a running instantiation example. In §6, having introduced the parameters, we discuss
other examples of memory models that fit our CSE theory.

3     Programming Language
We introduce the syntax and concrete semantics of our demonstrator programming language, which
is parametrised by a concrete memory model, specifically, concrete memory data type (IDef. 1),
memory actions (IDef. 2), and their associated IProps.

  Syntax. The syntax of the language is standard except that it is equipped with a memory-action
                  ® where 𝛼 ∈ Str, which is given a semantics using the memory-model IDefs.
command x® := 𝛼 ( E),

                         Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:8                                   A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


introduced below. The full definition of the syntax is as follows:
          𝑣 ∈ Val ::= null | 𝑏 ∈ Bool | 𝑛 ∈ Nat | 𝑞 ∈ Rat+ | 𝑠 ∈ Str | [® 𝑣]     x, y, z, . . . ∈ PVar
        E ∈ PExp ::= 𝑣 | x | ¬E | E = E | E ∧ E | E + E | E − E | E / E | E < E | . . .
        C ∈ Cmd ::= skip | x := E | if (E) C else C | C; C | y := 𝑓 ( E)® | x® := 𝛼 ( E)
                                                                                      ®
where the vector notation (e.g. 𝑣®) denotes a list, Val the set of values (Rat+ is the positive rationals),
PVar the set of program variables, PExp the set of expressions, and Cmd the set of commands.
  Concrete semantics. To define the semantics of the language and to ensure that the language can
be used in compositional reasoning, we require the following instance data:3
Instance Definition 1. We require a tuple (CMem, Wf , 𝜇 ∅ , ·), where CMem is a set of memories,
Wf ⊆ CMem is a well-formedness predicate, 𝜇 ∅ ∈ CMem the empty-memory element, and
· : (CMem, CMem) ⇀ CMem is a memory composition operator.4 The empty memory must be
well-formed and composition must maintain well-formedness.
Instance Definition Example 1. In our running example linear memory model, CMem is Nat ⇀fin
(Val ⊎ {∅}), where the symbol ∅ records that a memory cell has been freed. Tracking freed memory
cells is a standard technique used in compositional UX reasoning [45] to ensure that the memory
model satisfies UX frame (IProp. 2). All memories are well-formed, i.e., Wf = CMem. The empty
memory 𝜇 ∅ is the empty function and the composition of two memories 𝜇 and 𝜇 ′ is their disjoint
union 𝜇 ⊎ 𝜇 ′ (i.e., their union defined only for nonoverlapping memories).
Instance Property 1. The components (CMem, 𝜇 ∅ , ·) form a PCM.
We now discuss our big-step operational semantics for the language, with judgement
                                                     𝜎, C ⇓𝛾 𝑜 : 𝜎 ′
reading “the execution of command C with function implementation context 𝛾 in state 𝜎 results
in a state 𝜎 ′ with outcome 𝑜”. A program state is a pair 𝜎 = (𝑠, 𝜇) comprising a variable store
𝑠 : PVar ⇀fin Val and a memory 𝜇 ∈ CMem. Outcomes are defined as 𝑜 ::= ok | err | miss, denoting,
respectively, a successful execution, a fault due to a language error, and a fault due to a missing
resource error. We must distinguish between the two kinds of faults as the missing-resource errors
have a different role to play in compositional reasoning (see IProp. 2 below) and bi-abduction (see
§5.6). Function implementation contexts 𝛾 provide the function definitions used in function calls.
   The only interesting case in the definition of the semantics is the case for memory actions, which
is given by instance data. We only discuss this case; for other cases, see App. A.
Instance Definition 2. Memory actions are defined by a relation, written 𝜇.𝛼 (® 𝑣 ) ⇝ 𝑜 : (𝜇 ′, 𝑣®′ ),
which executes an action 𝛼 on memory 𝜇 with parameters 𝑣®, and returns an outcome 𝑜, memory 𝜇 ′ ,
and return values 𝑣®′ . All memory actions must preserve well-formedness (Wf ).
Instance Definition Example 2. Our linear memory model has four memory actions: lookup,
mutate, new, and free. We give the ok and miss rules for defining the lookup action; the full set of
rules is in App. D:
                      𝜇 (𝑛) = 𝑣                                         𝑛 ∉ dom(𝜇)
           𝜇.lookup( [𝑛]) ⇝ ok : (𝜇, [𝑣])                𝜇.lookup([𝑛]) ⇝ miss : (𝜇, [“MissingCell”, 𝑛])
3We use the 𝑋 ⇀ 𝑌 to denote partial functions from 𝑋 to 𝑌 and 𝑋 ⇀ 𝑌 to denote partial functions with finite support.
                                                                 fin
4 It would also be possible to incorporate the Wf   predicate into the concrete memory type itself using subtyping or
dependent types. We chose to keep it separate so that our meta-theory is simply typed. This is a presentational choice; the
condition is the same with both choices.


Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                       373:9


    The following two rules lift the semantics of memory actions to the command level:
       JEK            𝑣 ) ⇝ ok : (𝜇 ′, 𝑣®′ )
        ® 𝑠 = 𝑣® 𝜇.𝛼 (®                              𝑣 ′ | = |®x |
                                                    |®                               𝑣 ) ⇝ 𝑜 : (𝜇 ′, 𝑣®)
                                                                       ® 𝑠 = 𝑣® 𝜇.𝛼 (®
                                                                      JEK                                     𝑜 ≠ ok
                            ® ⇓𝛾 ok : (𝑠 [®x ↦→ 𝑣®′ ], 𝜇 ′ )
          (𝑠, 𝜇), x® := 𝛼 ( E)                                                          ® ⇓𝛾 𝑜 : (𝑠 [err ↦→ 𝑣®], 𝜇 ′ )
                                                                      (𝑠, 𝜇), x® := 𝛼 ( E)
where JEK𝑠 denotes the standard evaluation of an expression E with respect to a store 𝑠, resulting
either in a value or a dedicated symbol ∉ Val denoting an evaluation error.
   OX and UX frame. As is standard in compositional reasoning based on SL and ISL, we rely on the
fact that the concrete semantics of the language satisfies frame properties. To ensure that we have
these properties, we require that the concrete semantics of memory actions satisfy the standard OX
and/or UX frame properties (which in turn straightforwardly lift to the full concrete semantics):
Instance Property 2. For Wf (𝜇) and Wf (𝜇 𝑓 ):
               (OX)       If         (𝜇 · 𝜇 𝑓 ).𝛼 (®  𝑣 ) ⇝ 𝑜 : (𝜇 ′, 𝑣®′ )
                          then       ∃𝜇 ′′, 𝑣®′′, 𝑜 ′ . 𝜇.𝛼 (®
                                                             𝑣 ) ⇝ 𝑜 ′ : (𝜇 ′′, 𝑣®′′ ) and
                                            (𝑜 ′ ≠ miss ⇒ (𝑜 ′ = 𝑜 and 𝑣®′′ = 𝑣®′ and 𝜇 ′ = 𝜇 ′′ · 𝜇 𝑓 ))
               (UX)       If              𝑣 ) ⇝ 𝑜 : (𝜇 ′, 𝑣®′ ) and 𝑜 ≠ miss and 𝜇 ′ · 𝜇 𝑓 is defined
                                     𝜇.𝛼 (®
                          then       (𝜇 · 𝜇 𝑓 ).𝛼 (®  𝑣 ) ⇝ 𝑜 : (𝜇 ′ · 𝜇 𝑓 , 𝑣®′ )
   The OX property is more subtle than the UX property since to capture that we can extend
analysis results to larger states we must say, perhaps counterintuitively, that removing a “frame”
𝜇 𝑓 from 𝜇 · 𝜇 𝑓 results in either a miss outcome or the same behaviour as executing from the full
state, rather than more straightforwardly stating something about adding more state; see Yang
and O’Hearn [55] for an in-depth discussion of the OX property. Note that while both properties
capture that the analysis results can be extended to larger states, the frame 𝜇 𝑓 is added to the initial
state 𝜇 for OX reasoning (as, recall the definition in §2, OX soundness universally quantifies over
all initial states) and to the final state 𝜇 ′ for UX reasoning (as UX soundness instead universally
quantifies over all final states).

4    Assertions and Function Specifications
We introduce our assertion language and its satisfaction relation, parametric on a resource model com-
prising the resource assertions and satisfaction relation described in IDef. 3. The assertions provide
the pre- and postconditions of SL and ISL function specifications and are also used in assertion-based
constructs of our CSE engine such as folding and unfolding of user-defined predicates.
   Assertion syntax. We define assertions, Asrt, assuming a set of logical variables, 𝑥, 𝑦, 𝑧, ∈ LVar,
distinct from program variables, and a set of logical expressions, E ∈ LExp, which extends program
expressions PExp to include these logical variables and two new expressions E ∈ Val and E ∈ 𝜏
where 𝜏 ::= Null | Bool | Nat | . . . , meaning, that the expression E successfully evaluates to a value
and successfully evaluates to a value of type 𝜏, respectively. The syntax of assertions is defined by:
      𝐴 ∈ Asrt = E | True | 𝐴1 ⇒ 𝐴2 | 𝐴1 ∨ 𝐴2 | ∃𝑥 . 𝐴 | emp | 𝐴1 ★ 𝐴2 | 𝑟 ( E®1 ; E®2 ) | 𝑝 ( E®1 ; E®2 )
               def


for x ∈ LVar, E ∈ LExp, E®1, E®2 ∈ LExp,   ® 𝑟 ∈ Str, and 𝑝 ∈ Str. Our assertions comprise Boolean
assertions E, several first-order connectives and quantifiers, the empty-memory assertion emp,
assertions built using the separating conjunction ★, resource assertions 𝑟 ( E®1 ; E®2 ), and user-defined
predicate assertions 𝑝 ( E®1 ; E®2 ). The parameters of resource and user-defined predicate assertions
are split into in-parameters and out-parameters for automation purposes: in our CSE engine, the
consume operation requires the in-parameters to be known before consumption and learns the
out-parameters during consumption; see Lööw et al. [32] for further details.

                             Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:10                                    A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


   Satisfaction relation. To define the satisfaction relation for assertions, we introduce logical
interpretations, 𝜃 : LVar ⇀fin Val, and the evaluation of logical expressions, JEK𝜃,𝑠 , which extends
program expression evaluation to interpret logical variables using 𝜃 . The satisfaction relation,
𝜃, 𝜎 |= 𝐴, is defined in App. B; the interesting cases are:
      𝜃, (𝑠, 𝜇) |= 𝐴1 ★ 𝐴2 ⇔ ∃𝜇1, 𝜇2 . 𝜇 = 𝜇1 · 𝜇2 and 𝜃, (𝑠, 𝜇 1 ) |= 𝐴1 and 𝜃, (𝑠, 𝜇 2 ) |= 𝐴2
      𝜃, (𝑠, 𝜇) |= 𝑟 ( E®1 ; E®2 ) ⇔ JE®1 K𝜃,𝑠 = 𝑣®1 and JE®2 K𝜃,𝑠 = 𝑣®2 and 𝜇 |=Res 𝑟 (𝑣®1 ; 𝑣®2 ) defined in IDef. 3.
As is standard for parametric separation logics, the semantics of ★ is defined with respect to the
composition operator · from the memory PCM instance data (IDef. 1). The semantics of resource
assertions 𝑟 ( E®1 ; E®2 ) is also defined by instance data:
Instance Definition 3. A set of resource assertions of the form 𝑟 (𝑣®1 ; 𝑣®2 ), and a satisfaction relation
for the resource assertions, 𝜇 |=Res 𝑟 (𝑣®1 ; 𝑣®2 ).
Instance Definition Example 3. In our linear memory model, there are two types of resources:
the positive cell assertion, E1 ↦→ E2 (in prettified syntax) with in-parameter E1 and out-parameter E2 ,
and the negative cell assertion, E ↦→ ∅ with in-parameter E. Their satisfaction relation is as follows:
                                          𝜇 |=Res 𝑛 ↦→ 𝑣 ⇔ 𝜇 = {𝑛 ↦→ 𝑣 }
                                          𝜇 |=Res 𝑛 ↦→ ∅ ⇔ 𝜇 = {𝑛 ↦→ ∅}
   Program logics and function specifications. On top of our assertion language, we define the
standard SL and ISL function triples (and quadruples, to describe both successful and erroneous
outcomes). Our theory additionally supports exact separation logic triples [33], which are triples
that are valid both in the SL and ISL senses (i.e., they can be used for both types of reasoning). As
the SL, ISL, and ESL definitions are standard, we only give the formal definitions in App. B. It is
important that the definitions are indeed standard, otherwise CSE implementations based on our
theory would not be formally interoperable with other analysis implementations based on SL and
ISL (i.e., one could not formally exchange specifications between the implementations).
   We additionally need the following definitions to eventually state our engine soundness theorems.
A function specification context, Γ, is a function from function identifiers to sets of function
specifications. We say a function specification context Γ is valid w.r.t. a function implementation
context 𝛾, denoted |= (𝛾, Γ), when all function specifications in Γ are valid w.r.t. 𝛾. Formal definitions
are, again, in App. B.

5     CSE Engine
We introduce our CSE engine and prove its OX and UX soundness theorems. Our discussion is
focused on the parameters of the relevant theory that we say form a symbolic memory model and
our soundness relations. The relevant parameters are: the symbolic memory data type (IDef. 4),
its satisfaction relation (IDef. 5), symbolic memory actions (IDef. 6), and consume and produce
operations (IDef. 7) and their associated IProps. A larger excerpt of the formal rules of the engine is
given in App. C; and the full set of rules is available in our Rocq mechanisation.

5.1      Symbolic States
The symbolic states of our engine, denoted 𝜎,  ˆ are built out of logical expressions LExp with the
extra condition that none of the logical expressions have program variables. We use hat-notation to
distinguish symbolic definitions, such as 𝜎ˆ for symbolic state compared with 𝜎 for concrete state.
   The most interesting component of symbolic states is their symbolic memory component, which
is given by instance data:

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                       373:11


Instance Definition 4. A pair (SMem, 𝜇ˆ ∅ ), where SMem is a symbolic memory and 𝜇ˆ ∅ ∈ SMem
is the empty memory.
Instance Definition Example 4. Our linear memory model comprises SMem equalling LExp ⇀fin
(LExp ⊎ {∅}) and 𝜇ˆ ∅ equalling the empty function.
    We are now ready to give the full definition of symbolic state: a symbolic state 𝜎ˆ is a tuple
(𝑠,
 ˆ 𝜇,ˆ P̂, 𝜋)
           ˆ where: 𝑠ˆ : PVar ⇀fin LExp is a symbolic store; 𝜇ˆ ∈ SMem is a symbolic memory from
IDef. 4; P̂ is a multiset of symbolic user-defined predicates, where a symbolic predicate has the form
    ® ; Ê
𝑝 ( Ê  ®                                             ®       ®                                 ®      ®
      1 2 ) where 𝑝 ∈ Str is a predicate name and Ê1 ∈ LExp are the in-parameters and Ê2 ∈ LExp
the out-parameters; and 𝜋ˆ ∈ LExp is a path condition that captures constraints imposed during
                                  ˆ
execution. We use the syntax 𝜎.mem,        ˆ
                                           𝜎.pc etc. to access components of symbolic state and the
syntax 𝜎ˆ [mem := 𝜇ˆ′ ] etc. to update components of symbolic state. We use lv(𝜎)        ˆ to refer to the
logical variables of a symbolic state 𝜎.ˆ
    We define the semantic meaning of symbolic states using a satisfaction relation between concrete
and symbolic states of the form 𝜃, (𝑠, 𝜇) |= 𝜎ˆ where 𝜃 : LVar → Val is a logical interpretation,
𝑠 : PVar → Val is a variable store and 𝜇 ∈ CMem a concrete memory. The satisfaction relation
for symbolic states depends on the satisfaction relations for symbolic stores 𝜃, 𝑠 |=Sto 𝑠,    ˆ symbolic
memories 𝜃, 𝜇 |=Mem 𝜇,   ˆ and symbolic predicates 𝜃, 𝜇 |=Pred P̂: the satisfaction relations for symbolic
stores and symbolic predicates are as expected, see App. C; the satisfaction relation for symbolic
memories is given by instance data:
Instance Definition 5. A satisfaction relation for symbolic memory of the form 𝜃, 𝜇 |=Mem 𝜇,
                                                                                          ˆ with
the property that 𝜃, 𝜇 |=Mem 𝜇ˆ ∅ ⇔ 𝜇 = 𝜇 ∅ .
Instance Definition Example 5. In our linear memory model, the satisfaction relation for
symbolic memory is defined as follows, where for succinct presentation we say J∅K𝜃 = ∅:
                     𝜃, 𝜇 |=Mem {Ê𝑎1 ↦→ Ê𝑒1, . . . , Ê𝑎𝑛 ↦→ Ê𝑒𝑛 } ⇔ 𝜇 = ⊎𝑛𝑖=1 {JÊ𝑎𝑖 K𝜃 ↦→ JÊ𝑒𝑖 K𝜃 }
The satisfaction relation 𝜃, (𝑠, 𝜇) |= (𝑠, ˆ P̂, 𝜋)
                                        ˆ 𝜇,     ˆ for symbolic state is defined by:
        ∃𝜇1, 𝜇2 . 𝜇 = 𝜇1 · 𝜇2 and 𝜃, 𝑠 |=Sto 𝑠ˆ and 𝜃, 𝜇 1 |=Mem 𝜇ˆ and 𝜃, 𝜇 2 |=Pred P̂ and J𝜋K
                                                                                              ˆ 𝜃 = true
We say that a symbolic state 𝜎ˆ is satisfiable, denoted SAT(𝜎), ˆ when ∃𝜃, 𝑠, 𝜇. 𝜃, (𝑠, 𝜇) |= 𝜎,ˆ and say
that it implies an expression, denoted 𝜎ˆ |= Ê, when ∀𝜃, 𝑠, 𝜇. 𝜃, (𝑠, 𝜇) |= 𝜎ˆ ⇒ JÊK𝜃 = true.

5.2    Engine Judgement
The symbolic semantics of our CSE engine is given by a judgement of the form:
                                                                 ′ ′
                                                     ˆ C ⇓𝑚
                                                  𝑂, 𝜎,   Γ 𝑜 : 𝑂 , 𝜎ˆ
where: oracles 𝑂, 𝑂 ′ of type Nat → Nat are used to model angelic nondeterminism,5 e.g. when
there are multiple applicable function specifications to choose from for a function call; the mode 𝑚,
either OX, UX, or EX (for exact), enables the engine to switch its behaviour depending on what
type of soundness we need, e.g. what kind of function specifications to use in function calls, and
the set of outcomes, 𝑜 ::= ok | err | miss | abort, extends the outcomes of the concrete language
with abort, e.g. when a chosen function specification is not applicable.
5 See, e.g., Owens et al. [40] for further discussion on oracles. In short, each number 𝑂 (0), 𝑂 (1), . . . represents an answer

to a choice and the oracle is shifted once every time a choice is made (such that the oracle can always be queried by looking
at 𝑂 (0)), ultimately resulting in an output oracle 𝑂 ′ = 𝜆𝑛. 𝑂 (𝑛 + 𝑚) where 𝑚 is the number of choices made. The oracle
semantics we use is an intentionally simplistic model to avoid cluttering our formalism. In particular, the same angelic
choice is taken in each demonic branch. See Dardinier et al. [13] (using multi-relations) or Jacobs et al. [22] (using monads)
for more expressive formalisms for nondeterminism.

                             Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:12                                           A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


5.3       Memory-action Command
The symbolic semantics of memory-action commands, analogous to the concrete semantics, is
parametric on an instance-given symbolic action execution relation.

Instance Definition 6. A relation 𝜇.𝛼 ® ⇝ 𝑜 : ( 𝜇ˆ′, 𝜋ˆ ′, Ê® ′ ), which executes an action 𝛼 on memory
                                  ˆ ( Ê)
                  ® and returns an outcome 𝑜, memory 𝜇ˆ′ , path condition 𝜋ˆ ′ , and return values Ê® ′ .
𝜇ˆ with arguments Ê,
If 𝑜 ∈ {miss, abort}, then the symbolic memory must remain unchanged, i.e., 𝜇ˆ = 𝜇ˆ′ .
Instance Definition Example 6. To illustrate, we give some of the symbolic rules for the lookup
action of our linear memory model (for the rest, see App. D), specifically, the success and missing
resource rules:
             𝜇ˆ ( Ê𝑙′ ) = Ê   𝜋ˆ ′ = ( Ê𝑙 = Ê𝑙′ )                       𝜋ˆ ′ = ( Ê𝑙 ∈ Nat ∧ Ê𝑙 ∉ dom( 𝜇))
                                                                                                            ˆ
          ˆ
          𝜇.lookup(                  ˆ 𝜋ˆ ′, [ Ê])
                    [Ê𝑙 ]) ⇝ ok : ( 𝜇,                          ˆ
                                                                 𝜇.lookup([                   ˆ 𝜋ˆ ′, [“MissingCell”, Ê𝑙 ])
                                                                            Ê𝑙 ]) ⇝ miss : ( 𝜇,

where, note, the first rule branches over all possible addresses Ê𝑙′ where Ê𝑙 = Ê𝑙′ holds. We discuss
other “branching strategies” in §6.1, where we discuss variants of the memory model.
The following symbolic rules lift, again analogously to the concrete semantics, the memory actions
to the full semantics, where JEK𝑠ˆ denotes symbolic expression evaluation, which evaluates a program
expression E w.r.t. a symbolic store 𝑠:
                                      ˆ
JEK   ®
 ® = Ê                ® ⇝ ok : ( 𝜇ˆ′, 𝜋ˆ ′, Ê
                   ˆ ( Ê)
                  𝜇.𝛼                          ® ′)     ® ′ | = |®x |
                                                      | Ê                      ®
                                                                           ® = Ê
                                                                          JEK                   ® ⇝ 𝑜 : ( 𝜇ˆ′, 𝜋ˆ ′, Ê
                                                                                           ˆ ( Ê)
                                                                                           𝜇.𝛼                       ® ′) 𝑜 ≠ ok
   𝑠ˆ                                                                        𝑠ˆ
  ′             ® ′
 𝑠ˆ = 𝑠ˆ [®x ↦→ Ê ]                    ®   ®
                          𝜋ˆ = (𝑠ˆ(®x), Ê, Ê ∈ Val ∧ 𝜋ˆ ′ ∧ 𝜋)
                            ′′                ′
                                                                ˆ            ′              ® ′
                                                                            𝑠ˆ = 𝑠ˆ [err ↦→ Ê ]            ®
                                                                                                   𝜋ˆ = ( Ê ∈ Val ∧ 𝜋ˆ ′ ∧ 𝜋)
                                                                                                     ′′
                                                                                                                             ˆ
      𝑂, (𝑠, ˆ P̂, 𝜋),
          ˆ 𝜇,                 ® ⇓𝑚 ok : 𝑂, (𝑠ˆ′, 𝜇ˆ′, P̂, 𝜋ˆ ′′ )
                   ˆ x® := 𝛼 ( E)                                         𝑂, (𝑠, ˆ P̂, 𝜋),
                                                                              ˆ 𝜇,                 ® ⇓𝑚 err : 𝑂, (𝑠ˆ′, 𝜇ˆ′, P̂, 𝜋ˆ ′′ )
                                                                                       ˆ x® := 𝛼 ( E)
                                  Γ                                                                   Γ
We require the following property to be able to prove that our CSE engine, specifically, the memory-
action commands, satisfy our two soundness theorems:
Instance Property 3. The symbolic memory-action semantics must be OX/UX sound w.r.t. the
concrete memory-action semantics, i.e., the two semantics must satisfy the OX/UX soundness
definitions introduced in §2 but with the command-level concrete semantics replaced by the
memory-action-level concrete semantics, the satisfaction relation |= replaced by the satisfaction
relation |=Mem , etc. The full formal properties are given in App. C.

5.4       Consume and Produce Operations and Assertion-based Commands
We now discuss the definition, soundness, and usage of our memory-model-parametric consume
and produce operations that form the basis of our CSE engine’s consume-produce architecture.
  Definition. The judgements of consume and produce are as follows. First, we introduce symbolic
substitutions, 𝜃ˆ : LVar ⇀fin LExp, which the two operations use to instantiate free logical variables.
Now, the judgements of consume and produce are:
           consume(𝑚, 𝑂, 𝐴, 𝜃,   ˆ ⇝ (𝑜, 𝑂 ′, 𝜃ˆ′, 𝜎ˆ ′ )
                               ˆ 𝜎)                       and     produce(𝐴, 𝜃,   ˆ ⇝ 𝜎ˆ ′
                                                                               ˆ 𝜎)
where the judgement for consume states that the consumption of assertion 𝐴 in mode 𝑚 (which
decides how Boolean information is consumed) with an oracle 𝑂 and an initial symbolic substitution
𝜃ˆ from state 𝜎ˆ results in outcome 𝑜 (ok or abort), an updated oracle 𝑂 ′ , symbolic state 𝜎ˆ ′ where the
symbolic state corresponding to 𝐴 has been removed, and extended symbolic substitution 𝜃ˆ′ now
containing mappings for all free logical variables of 𝐴; and the judgement for produce states that
the production of 𝐴 with symbolic substitution 𝜃ˆ in state 𝜎ˆ results in state 𝜎ˆ ′ where the symbolic
state corresponding to 𝐴 has been added.

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                         373:13


  We only discuss how resource assertions 𝑟 ( E®1 ; E®2 ) are consumed and produced (remaining rules
are inspired by the rules of Lööw et al. [31],6 which in turn are inspired by Gillian). The consume
and produce operations are parametric on two resource-level consume and produce operations,
which we call, respectively, resource consume consumeRes and resource produce produceRes :
Instance Definition 7. Two operations consumeRes and produceRes of the form explained below:
                     ® , 𝜇)
consumeRes (𝑚, 𝑂, 𝑟, Ê            ′ ®           ′                                                ® , Ê
                                                                                                       ®     ˆ ⇝ ( 𝜇ˆ′, 𝜋)
                       in ˆ ⇝ (𝑜, 𝑂 , Êout, ( 𝜇ˆ , 𝜋ˆ𝑖 , 𝜋))
                                                          ˆ               and      produceRes (𝑟, Ê in out, 𝜇)         ˆ
Instance Definition Example 7. For our linear memory model, the following are two of the rules
for consumeRes and produceRes (again, the rest of the rules are in App. D):
                       𝜇ˆ = 𝜇ˆ 𝑓 ⊎ {Ê1 ↦→ Ê2 }                                             𝜇ˆ′ = 𝜇ˆ ⊎ {Ê1 ↦→ Ê2 }
consumeRes (𝑚, 𝑂, ↦→, [Ê], 𝜇)
                            ˆ ⇝ (𝑜𝑘, 𝑂, Ê2, ( 𝜇ˆ 𝑓 , true, Ê = Ê1 ))                                           ˆ ⇝ ( 𝜇ˆ′, true)
                                                                                produceRes (↦→, [ Ê1 ], [ Ê2 ], 𝜇)

The consumeRes and produceRes op-
erations, analogous to memory ac- consumeRes (𝑚, 𝑂, 𝑟, 𝜃ˆ( E®in ), 𝜎.mem)ˆ                     ® , ( 𝜇ˆ′, 𝜋ˆ , 𝜋))
                                                                                    ⇝ (𝑜, 𝑂 ′, Êout          𝑖 ˆ
                                                                  ′                  ′
tions, are lifted into consume and pro-          𝜎ˆ |= 𝜋ˆ𝑖      𝜎ˆ = 𝜎ˆ [mem := 𝜇ˆ , pc := 𝜋ˆ ∧ 𝜎.pc]
                                                                                                  ˆ
duce. We explain the consume case,                              rest of the rule omitted
the produce case is similar. See the           consume(𝑚, 𝑂, 𝑟 ( E®in ; E®out ), 𝜃, ˆ ⇝ (𝑜, 𝑂 ′, 𝜃ˆ′, 𝜎ˆ ′′ )
                                                                                 ˆ 𝜎)
consume rule in Fig. 2, which illus-
trates the most interesting parts of                    Fig. 2. Implementation of consume.
how consumeRes is lifted into consume. There are two conditions that consumeRes outputs: 𝜋ˆ𝑖 ,
                                                 ˆ which is appended to the path condition of the
which must be implied by the initial state, and 𝜋,
updated state. The two conditions are used to implement different types of branching, which we
illustrate by example when discussing variants of the linear memory model in §6.1.
   Soundness. We introduce OX and UX soundness properties that formalise that the consume
and produce operations “correctly” consume and produce their input assertions. Our soundness
properties are based on the soundness properties for consume and produce introduced by Lööw
et al. [31], which we have refactored into four properties: (1) consume OX soundness, (2) produce
OX soundness, (3) consume UX soundness, (4) produce UX soundness. The full properties are
available in App. C; in short, the properties relate the behaviour of consume and produce to the
satisfaction relation of the assertion language. For example, UX soundness of consume requires
that the composition of the models of the input assertion and the output symbolic state forms a
model of the input symbolic state:

               If        consume(𝑚, 𝑂, 𝐴, 𝜃,         ˆ ⇝ (𝑜𝑘, 𝑂 ′, 𝜃ˆ′, 𝜎ˆ 𝑓 )
                                                   ˆ 𝜎)
                                                 ′
                         and 𝜃, (𝑠, 𝜇𝐴 ) |= 𝜃ˆ (𝐴) and 𝜃, (𝑠, 𝜇 𝑓 ) |= 𝜎ˆ 𝑓 and (𝜇𝐴 · 𝜇 𝑓 ) is defined
               then      𝜃, (𝑠, 𝜇𝐴 · 𝜇 𝑓 ) |= 𝜎ˆ
To ensure that our soundness properties of consume and produce hold, we require that resource-
only variants of the properties to hold for the consumeRes and produceRes operations.
Instance Property 4. The consumeRes and produceRes operations must be OX/UX sound. Again,
the full properties are stated in App. C. To exemplify the resource-only variant of the properties,

6 Our operations support the subset of assertions usually supported by consume and produce operations. That is, both

operations support Boolean assertions, existential quantification (for consume only in OX mode, we do not know of a
use-case in UX mode), the empty-memory assertion, separating-conjunction assertions, resource assertions, and user-
defined-predicate assertions, and, additionally, produce supports disjunction assertions.


                            Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:14                                   A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


we give the resource-only variant of the UX soundness property for consume (the reader should
compare the property with the property above):
           consumeRes (𝑚, 𝑂, 𝑟, Ê® , 𝜇)              ′ ®                                   ®                   ®
 If                                 in ˆ ⇝ (𝑜𝑘, 𝑂 , Êout, ( 𝜇ˆ 𝑓 , 𝜋ˆfi , 𝜋ˆ 𝑓 )) and JÊin K𝜃 = 𝑣®in and JÊout K𝜃 = 𝑣®out
           and J𝜋ˆ 𝑓 K𝜃 = true and 𝜃, 𝜇 𝑓 |=Mem 𝜇ˆ 𝑓 and 𝜇𝑟 |=Res 𝑟 (®      𝑣 in ; 𝑣®out ) and (𝜇𝑟 · 𝜇 𝑓 ) is defined
 then      J𝜋ˆfi K𝜃 = true and 𝜃, (𝜇𝑟 · 𝜇 𝑓 ) |=Mem 𝜇ˆ
With the above definitions in place, we have been able to prove the following:
  Lemma 5.1. Given OX/UX sound consumeRes and produceRes operations, our consume and produce
operations are OX/UX sound.
  Usage. We have mechanised and proved sound the standard consume-produce definitions of the
function-call command and fold/unfold commands for user-defined predicates, the full definitions
are available in App. C for completeness. The function-call command we have proved OX and UX
sound, whereas the fold/unfold commands we have proved OX sound.7 The successful proofs of
these commands show that our consume-produce properties are sufficient for their core use cases.
Additionally, as we discuss in §5.6, the analyses we have built on top of our engine show that our
consume-produce properties are also sufficient for those analyses.

5.5      Engine Soundness
Our OX soundness and UX soundness theorems are as follows:8
   Theorem 5.2 (OX soundness). Let 𝑚 ∈ {OX, EX} and assume |= (𝛾, Γ), when the CSE engine is
instantiated with OX sound memory actions, consumeRes , and produceRes , then the following holds:
                  If       𝜎, C ⇓𝛾 𝑜 : 𝜎 ′ and 𝜃, 𝜎 |= 𝜎ˆ and
                           (∀𝑜, 𝑂 ′, 𝜎ˆ ′ . 𝑂, 𝜎,
                                                ˆ C ⇓𝑚       ′ ′
                                                     Γ 𝑜 : 𝑂 , 𝜎ˆ and SAT(𝜎ˆ ) ⇒
                                                                                ′
                                                                    ′
                                 𝑜 ≠ abort and (𝑜 = miss ⇒ 𝜎ˆ .preds = ∅))
                  then     ∃𝑂 ′, 𝜎ˆ ′, 𝜃 ′ . 𝑂, 𝜎,
                                                ˆ C ⇓𝑚      ′ ′        ′                   ′ ′
                                                     Γ 𝑜 : 𝑂 , 𝜎ˆ and 𝜃 | lv(𝜎ˆ ) = 𝜃 and 𝜃 , 𝜎 |= 𝜎ˆ
                                                                                                      ′

   Theorem 5.3 (UX soundness). Let 𝑚 ∈ {UX, EX} and assume |= (𝛾, Γ), when the CSE engine is
instantiated with UX sound memory actions, consumeRes , and produceRes , then the following holds:
                   ˆ C ⇓𝑚        ′ ′                                  ′                    ′      ′
      If        𝑂, 𝜎,    Γ 𝑜 : 𝑂 , 𝜎ˆ and 𝑜 ≠ abort and (𝑜 = miss ⇒ 𝜎ˆ .preds = ∅) and 𝜃, 𝜎 |= 𝜎ˆ
      then                        ′
                ∃𝜎. 𝜎, C ⇓𝛾 𝑜 : 𝜎 and 𝜃, 𝜎 |= 𝜎ˆ
   Both theorems have restrictions on abort and miss outcomes. For the OX theorem, the condition
should be read as follows: no reachable satisfiable state has an outcome abort or an outcome
miss unless there are no symbolic predicates in the state. For both theorems, the soundness of
miss outcomes cannot be guaranteed in the presence of symbolic predicates because the source
of miss outcomes, memory actions (IDef. 6), do not take symbolic predicates into consideration
(doing so would require implementing an automated complete unfolding procedure, which none
of the existing CSE tools or platforms implement). To exemplify, say we are working with our
running example linear memory model and have defined the following user-defined predicate:
                                   def                          def                                       def
foo(;){1 ↦→ 1}. First, let C = x := lookup(1), 𝜎ˆ = (∅, 𝜇ˆ ∅ , {foo(;)}, true), and 𝜎 = (∅, {1 ↦→ 1}).
Now, note that ∅, 𝜎 |= 𝜎,
                        ˆ concrete execution of C from 𝜎 only results in an ok outcome, and symbolic
execution of C from 𝜎ˆ only results in a miss outcome. This breaks both OX and UX soundness:
there is no corresponding execution for the concrete execution and vice versa.
7 Lööw et al. [31] claim that the fold command is UX sound if folding is restricted to strictly exact predicates (an assertion 𝐴

is strictly exact iff 𝜃, (𝑠, 𝜇 ) |= 𝐴 ∧ 𝜃, (𝑠, 𝜇 ′ ) |= 𝐴 ⇒ 𝜇 ′ = 𝜇 [54, p. 149]), but during our mechanisation work we found a
counterexample to this claim. We have not investigated a new condition to make the command UX sound.
8 Here, we have simplified away some uninteresting details of the statements, see the Rocq mechanisation for the full details.



Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                     373:15


5.6   Analyses
We now discuss two analyses we have built on top of our CSE engine and proved sound: a function
specification verification analysis to exemplify an OX analysis application and a true bug-finding
analysis based on bi-abduction to exemplify an UX analysis application. We additionally discuss the
trusted computing base (TCB) of analysis results when using our engine.

   The two analyses. The development and verification of our OX analysis application was relatively
uneventful: our work validates that our adapted consume-produce properties are sufficient for this
OX application, but the analysis itself is standard in the consume-produce literature, and we did
not run into any particular problems with porting its proof to our parametric setting. We therefore
only discuss our UX application here; see App. C for our OX application.
   Bi-abduction is a technique that facilitates automatic ISL specification synthesis by incrementally
discovering the resources needed to execute a given piece of code starting from an empty pre-
condition/symbolic state. It was first introduced in the OX setting [9, 10], forming the basis of the
Infer tool [8]. It was later ported to the OX consume-produce setting in the JaVerT 2.0 project [18],
by re-imagining bi-abduction as fixes-from-missing-resource-errors. With the introduction of incor-
rectness separation logic [45], the original bi-abduction algorithm was ported to the UX setting of
true bug-finding, underpinning the Infer-Pulse tool [26]. Following this, Lööw et al. [31] showed
that the fixes-from-missing-resource-errors approach is UX sound in the setting of linear memory.
Here, we generalise Lööw et al. [31]’s UX result to our memory-model-parametric setting.
                                                            ˆ C ⇓bi       ′    ′
   We have built a bi-abductive engine with judgement 𝑂, 𝜎,       Γ 𝑜 : 𝑂 , (𝜎ˆ , 𝐴) on top of our engine
with judgement 𝑂, 𝜎,        UX      ′   ′
                     ˆ C ⇓Γ 𝑜 : 𝑂 , 𝜎ˆ . The 𝐴 in the judgement is an assertion representing an anti-
heap, which captures the missing resources needed to execute the command C in the following sense:

  Theorem 5.4 (CSE with Bi-Abduction: Soundness).

      If      |= (𝛾, Γ) and 𝑂, 𝜎,    ˆ C ⇓bi        ′    ′              ′
                                            Γ 𝑜 : 𝑂 , (𝜎ˆ , 𝐴) and 𝜃, 𝜎 |= 𝜎ˆ
                                                                                 ′

      then    ∃𝑠, 𝜇, 𝜇 fix . 𝜃, (𝑠, 𝜇) |= 𝜎ˆ [pc := 𝜎ˆ .pc] and 𝜃, (𝑠, 𝜇 fix ) |= 𝐴 and (𝑠, 𝜇 · 𝜇fix ), C ⇓𝛾 𝑜 : 𝜎 ′
                                                      ′


In short, the bi-abductive engine works by catching missing-resource errors and abort errors during
execution, which are given to a memory-model-dependent operation fix that takes, as input, the
current symbolic state and constructs one or more assertions representing the resources needed
for continued execution, which in turn are produced into the current symbolic state and appended
to the anti-heap. The soundness of the engine (Thm. 5.4) follows from the UX soundness of our
CSE engine (Thm. 5.3) and produce (Lem. 5.1). To prove soundness, we had to adapt the soundness
statement and proofs from previous work [18, 31], which relied on having a symbolic composition
operator and a symbolic frame property, which we do not require as parameters.

   Trusted computing base. As one would expect from a mechanised theory, our CSE theory comes
with a strong TCB story: the TCB of analysis results includes only the semantics of assertions (to
express pre- and postconditions) and the concrete semantics of the language. The TCB can be further
reduced by considering only first-order assertions, as then the assertion language can be removed
from the TCB (this is analogous to sound program logics, see, e.g., Iris’ adequacy theorem [24]).
   The fact that the concrete memory model is part of the TCB (as it is part of the concrete
semantics), means that one must choose the model carefully. Appropriate TCB models have a direct
correspondence to a memory model specified by a language standard or the like. Because of space
constraints, we do not discuss this point further but show in our Rocq development how analysis
artefacts like ghost state annotations (e.g., like the annotations used by our fractional ownership
model introduced in §6.2) can easily be removed from the TCB by a standard simulation argument.

                          Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:16                                         A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


6     Memory-model Instances
Now having introduced the IDefs. and IProps. required to instantiate our CSE theory, we discuss ad-
ditional examples of memory-model instances that fit into our CSE theory, as summarised in Tab. 1.
   We emphasise that the primary purpose of our discussion in this section is to show that a
wide array of memory models fit into our CSE theory. We do not have sufficient page budget to
formally introduce all required IDefs. (i.e, IDefs. 1–7) and discuss proofs of the required IProps. (i.e.,
IProp. 1–4) for each memory instance. Therefore, our discussion is informal and focused on what we
have found to be the primary difficulty to get right in designing memory models: the memory data
type (IDef. 1), such that compositional memory actions (IDef. 2) that work over SL/ISL-style partial
state can be defined etc. (We give additional definitions in App. D and all definitions are available in
our Rocq development.) With the right data type in place, we have found other major instance data,
such as symbolic memory actions (IDef. 6) and consumeRes and produceRes operations (IDef. 7),
to be relatively straightforward to define. In particular, for simpler memory models, symbolic
components can be designed by “symbolically lifting” of the corresponding concrete component,
in particular, the symbolic data type and memory actions. For an example, compare the concrete
data type (IDef. 1) and symbolic data type (IDef. 4) of our running example memory model and
note how the symbolic data type is structurally identical to the concrete data type but abstracts
both Nat and Val to LExp.

6.1      Linear Memory Models and Memory-model Design Considerations
We have mechanised and proved sound multiple variants of our running example linear memory
model (see again Tab. 1). As discussed in the introduction (§1), there are multiple degrees of freedom
available when designing a symbolic memory model. Simple linear memory models provide a
good stage to illustrate this; as we have already introduced the various IDefs. of our running
example linear memory model, we in this section discuss design considerations relating to OX vs.
UX analysis, such as what types of “branching strategies” are allowed by different reasoning modes.
   Operational meaning of OX vs. UX. The different requirements arising from OX and UX soundness
can be exploited in memory-model design. Intuitively, OX analyses like verification must consider
all execution paths whereas UX analyses like bug-finding only need to consider paths with bugs.
More precisely: operationally, OX soundness allows for dropping information along execution paths
but not dropping paths, whereas UX soundness allows for dropping paths but not information.
   Path maintenance, illustrated through branching strategies. When updating and removing parts
of memory, there are multiple ways to handle “branching”, i.e., situations where there are multiple
potential parts of memory to update/remove, sometimes referred to as “matches”. To exemplify, we
discuss branching in the context of consumeRes for linear memory models (that is, variants of IDef. 7).
For the discussion, it is important to have Fig. 2 fresh in mind. Say we have 𝜇ˆ = {1 ↦→ 1, 2 ↦→ 1}
and 𝜋ˆ = 1 ≤ 𝑥ˆ ≤ 2 and are about to consume a resource assertion 𝑥 ↦→ 1 knowing 𝑥 = 𝑥.       ˆ Now
                                                                  ′
consider the following three branching strategies, where ( Ê1, 𝑂 ) ∈ 𝑂 (dom( 𝜇))
                                                                               ˆ denotes that we
angelically pick an element from dom( 𝜇):ˆ
                                                         ( Ê1, 𝑂 ′ ) ∈ 𝑂 (dom( 𝜇))
                                                                                ˆ                          ( Ê1, 𝑂 ′ ) ∈ 𝑂 (dom( 𝜇))
                                                                                                                                  ˆ
         𝜇ˆ = 𝜇ˆ 𝑓 ⊎ {Ê1 ↦→ Ê2 }                        𝜇ˆ = 𝜇ˆ 𝑓 ⊎ {Ê1 ↦→ Ê2 }                         𝜇ˆ = 𝜇ˆ 𝑓 ⊎ {Ê1 ↦→ Ê2 }
consumeRes (𝑚, 𝑂, ↦→, [Ê], 𝜇)        ˆ ⇝         consumeRes (𝑚, 𝑂, ↦→, [ Ê], 𝜇)        ˆ ⇝        consumeRes (𝑚, 𝑂, ↦→, [ Ê], 𝜇)       ˆ ⇝
 (𝑜𝑘, 𝑂, [ Ê2 ], ( 𝜇ˆ 𝑓 , true, Ê = Ê1 ))     (𝑜𝑘, 𝑂 ′, [Ê2 ], ( 𝜇ˆ 𝑓 , Ê = Ê1, Ê = Ê1 ))   (𝑜𝑘, 𝑂 ′, [ Ê2 ], ( 𝜇ˆ 𝑓 , true, Ê = Ê1 ))
The left rule belongs to our running example linear memory model and the two other rules to
variant models we have defined. The left rule branches over all possible matches; in our example, we
get two branches: one branch with 𝜇ˆ 𝑓 = {2 ↦→ 1} and 𝜋ˆ = 1 ≤ 𝑥ˆ ≤ 2 ∧ 𝑥ˆ = 1 and one branch with

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                         373:17


𝜇ˆ 𝑓 = {1 ↦→ 1} and 𝜋ˆ = 1 ≤ 𝑥ˆ ≤ 2 ∧ 𝑥ˆ = 2. The middle rule implements unique-match branching
since the rule is only applicable when there is a unique match. The rule is not applicable to our
example as neither 𝑥ˆ = 1 nor 𝑥ˆ = 2 is implied by the current symbolic state. We have proved a
linear memory model implementing this type of branching to be both OX sound and UX sound.
Interestingly, the same rule but with conclusion · · · ⇝ (𝑜𝑘, 𝑂 ′, [Ê2 ], ( 𝜇ˆ 𝑓 , Ê = Ê1, true)) is OX sound
but not UX sound because our CSE engine use the entire symbolic input state in the implication
check – meaning that the implication might not hold w.r.t. the smaller output state. (With a stricter
implication check requiring that the path condition, rather than the full symbolic state, implies
the matching condition (in the example: Ê = Ê1 ), the rule would be UX sound.) Lastly, the right
rule implements, what we call, cut branching because the rule simply angelically picks one branch
without checking if there are more matches. We have proved a linear memory model implementing
this type of branching to be UX sound but not OX sound; the model is not OX sound because in
OX reasoning we are not allowed to drop matches.
   Information maintenance. Beyond variants of our run-
                                                                      𝜇ˆ ( Ê𝑙′ ) = Êold        𝜇ˆ′ = 𝜇ˆ [Ê𝑙′ ↦→ Ê]
ning example linear memory model with different branch-
                                                                            𝜋ˆ ′ = ( Ê𝑙 = Ê𝑙′ ∧ Êold ∈ Val)
ing strategies, we have also mechanised and proven sound
a memory-model instance for the traditional linear mem-             ˆ
                                                                   𝜇.mutate([         Ê𝑙 , Ê]) ⇝ ok : ( 𝜇ˆ′, 𝜋ˆ ′, [])
ory model from the OX literature, with concrete data type
Nat ⇀fin Val. This is an OX-only model: the model does not              Fig. 3. Successful mutate rule.
keep track of freed cells, using ∅, and can therefore not be
proven UX sound (because it does not satisfy UX frame). Since it is an OX-only model, dropping in-
formation is allowed. As a simple illustration, consider Fig. 3, containing the successful mutate rule
of our running example linear memory model. Note that the rule ensures that the information that
the previous cell value successfully evaluates is kept by updating the path condition with Êold ∈ Val.9
This is optional in OX-only models: our OX-only model is defined using rules that do not add evalua-
tion information to the path condition, and we have still been able to prove the model to be OX sound.

6.2    Fractional Ownership Memory Model
To illustrate that different ownership disciplines fit into our CSE theory, we have mechanised and
proved OX and UX sound a linear memory model with fractional ownership [5, 6] rather than
exclusive ownership, as utilised in the memory models discussed up to this point. A memory model
similar to the fractional ownership memory model we discuss here has previously been implemented
in an experimental branch of Gillian and tested on a small set of hand-written examples.
   Model description. The memory model is best explained in terms of resources (i.e., IDef. 3). Points-
                                               𝑞
to assertions for the model are of the form 𝑛 ↦→ 𝑣, where 𝑞 ∈ (0, 1] ⊂ Rat+ specifies the amount
of ownership. Less-than-1 ownership (𝑞 < 1) gives read permission to the location 𝑛, while full
ownership (𝑞 = 1) gives both read and write permissions. The other IDefs. of the model are relatively
straightforward extensions of our running example memory model. In particular, the concrete
memory data type of the model is Nat ⇀fin ((Val, Rat+ ) ⊎ {∅}) and the symbolic memory data
type is derived from this data type by symbolic lifting, i.e., LExp ⇀fin ((LExp, LExp) ⊎ {∅}). The
implementation of memory actions, consumeRes , and produceRes are, as one would expect, also
similar but with additional ownership checks. For illustration, we show the two successful rules of
consumeRes for points-to assertions:10
9 This is not the only way to ensure this. It is also possible to, e.g., maintain an invariant saying that the path condition must

include this type of information. The point being made here is that this needs to be ensured in some way.
10 The “Ê ′ ∉ dom( 𝜇ˆ )” expression in the first rule is needed for UX soundness, to not drop disjointedness information.
          𝑙           𝑓


                             Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:18                                         A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


                                                                           3      5    𝑏𝑜𝑢𝑛𝑑 : Some(2)               (𝑛 1, 0) ↦→ 3 ★
                                                             𝑛1
         𝜇   ∈    CMem                                                                                               (𝑛 1, 1) ↦→ 5 ★
                                                             𝑛2                               𝑏𝑜𝑢𝑛𝑑 : None           Bound(𝑛 1 ; 2) ★
 𝜇 (𝑛 1 )    =    ({0 ↦→ 3, 1 ↦→ 5}, Some(2))                                     3   false

 𝜇 (𝑛 2 )    =    ({1 ↦→ 2, 2 ↦→ false}, None)               𝑛3                                                      (𝑛 2, 1) ↦→ 3 ★
 𝜇 (𝑛 3 )    =    ∅                                                       ∅                                          (𝑛 2, 2) ↦→ false ★
                                                                                                                     𝑛 3 ↦→ ∅

Fig. 4. Example block-offset memory instance 𝜇 expressed formally (left), visually (centre), and as a composi-
tion of resource assertions (right).


                                                                                                  𝜇ˆ = 𝜇ˆ 𝑓 ⊎ {Ê𝑙′ ↦→ ( Ê𝑣 , Ê𝑞′ )}
                      𝜇ˆ = 𝜇ˆ 𝑓 ⊎ {Ê𝑙′ ↦→ ( Ê𝑣 , Ê𝑞′ )}                                    𝜇ˆ′ = 𝜇ˆ 𝑓 ⊎ {Ê𝑙′ ↦→ ( Ê𝑣 , Ê𝑞′ − Ê𝑞 )}
                consumeRes (𝑚, 𝑂, ↦→, [ Ê𝑙 , Ê𝑞 ], 𝜇)   ˆ ⇝                             consumeRes (𝑚, 𝑂, ↦→, [ Ê𝑙 , Ê𝑞 ], 𝜇)   ˆ ⇝
 (𝑜𝑘, 𝑂, [ Ê𝑣 ], ( 𝜇ˆ 𝑓 , true, Ê𝑙 = Ê𝑙′ ∧ Ê𝑞 = Ê𝑞′ ∧ Ê𝑙′ ∉ dom( 𝜇ˆ 𝑓 )))         (𝑜𝑘, 𝑂, [Ê𝑣 ], ( 𝜇ˆ′, true, Ê𝑙 = Ê𝑙′ ∧ Ê𝑞 < Ê𝑞′ ))


6.3      Block-offset Memory Model for C
Our CSE theory is not limited to different variants of the linear memory model. To illustrate this,
we have mechanised and proved OX and UX sound a block-offset memory model for C. Originally
inspired by the memory model of the verified CompCert C compiler [29], the model has previously
been implemented in Gillian and has been used in Gillian-based teaching, but no detailed definition
or soundness results have previously been given.
   We describe, component by component, the concrete-memory instance data (CMem, Wf , 𝜇 ∅ , ·)
for IDef. 1. The memory data type is as follows:
                       def                                                                       def
             CMem = Nat ⇀fin (CMemB ⊎ {∅})                            where CMemB = (Nat ⇀fin Val, Nat?)
using notation 𝑡? to denote the option type for type 𝑡, with constructors None and Some. The
concrete memory comprises two parts: CMem is a mapping from block identifiers to blocks; CMemB
is a block comprising a linear array and a bound indicating the fixed size of the array. (In C terms,
the block identifiers are essentially pointers returned by malloc(), and the blocks describe the
contents and size of the corresponding allocated memory.) This data structure allows us to represent
partial blocks, required to be able to define |=Res , i.e., IDef. 3, which we discuss shortly. Fig. 4 gives an
example of a partial concrete memory given by map 𝜇 with domain of block identifiers {𝑛 1, 𝑛 2, 𝑛 3 }.
The mapping 𝜇 (𝑛 1 ) is a complete block as the bound is 2 and both cells are present in the block. The
mapping 𝜇 (𝑛 2 ) is a partial block due to both the missing bound and the missing map at offset 0.
The mapping 𝜇 (𝑛 3 ) is a deallocated block, denoted by ∅.
    The well-formedness condition Wf provides constraints on the formation of blocks. Block-
offset memories may not be well-formed for two reasons: first, a memory such as {3 ↦→ ({0 ↦→
1, 1 ↦→ 0}, Some(1))} is not well-formed because its cells do not respect the bound; second, and
more interestingly, a memory such as {3 ↦→ (∅, None)}, which comprises an empty block is not
well-formed since such blocks break the frame properties of the model (IProp. 2). We elaborate on
this aspect more when we introduce concrete memory actions later (IDef. 2).
    The empty memory is the empty mapping 𝜇 ∅ = ∅. Note that this trivially satisfies Wf .
    The definition of · is slightly complex. We exemplify using Fig. 4. Given another memory
𝜇 ′ = {𝑛 2 ↦→ ({0 ↦→ 1, 3 ↦→ 0}, Some(4))}, we have the composition 𝜇 · 𝜇 ′ which is a mapping that
gives the same results as 𝜇 for block identifiers 𝑛 1 and 𝑛 3 and, for 𝑛 2 , gives:
                             (𝜇 · 𝜇 ′ ) (𝑛 2 ) = ({0 ↦→ 1, 1 ↦→ 3, 2 ↦→ false, 3 ↦→ 0}, Some(4))}.

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                           373:19


We use the memory 𝜇 ′′ = {𝑛 2 ↦→ ({1 ↦→ 12}, Some(2))} to illustrate the two reasons why blocks
may fail to compose. Indeed, the composition 𝜇 ·𝜇 ′′ is not defined for two reasons: first, the addresses
of the blocks at 𝑛 2 overlap (i.e., dom(fst(𝜇 (𝑛 2 ))) ∩ dom(fst(𝜇 ′′ (𝑛 2 ))) ≠ ∅); second, the addresses
of the block 𝜇 (𝑛 2 ) are not contained within the bound of the block 𝜇 ′′ (𝑛 2 ), meaning that if the
composition would be defined, then the result would not satisfy Wf .
   We now cover memory actions (IDef. 2). The successful rules of new and free are given below:
  𝑛𝑏 ∉ dom(𝜇) 𝜇𝑏 = ({0 ↦→ null, . . . , 𝑛 − 1 ↦→ null}, Some(𝑛))          𝜇 (𝑛𝑏 ) = (𝜇𝑏 , Some(𝑛)) |𝜇𝑏 | = 𝑛
             𝜇.new( [𝑛]) ⇝ ok : (𝜇 [𝑛𝑏 ↦→ 𝜇𝑏 ], [𝑛𝑏 ])                  𝜇.free([𝑛𝑏 ]) ⇝ ok : (𝜇 [𝑛𝑏 ↦→ ∅], [])

Because we are now working with blocks, allocation returns a fresh, complete block, and freeing
a block deallocates an entire complete block given a block identifier. Load and store operations
now also take in the offset as input in addition to the block identifier (and also value for store), and
these operations only require components necessary to load or store, i.e., requiring the relevant
partial block and not the complete block.
   Going back to why empty blocks are not allowed by Wf , note that UX frame breaks when
allocation returns a block identifier 𝑛𝑏 pointing to a fresh, complete block, but the frame contains
the same 𝑛𝑏 pointing to an empty block. OX frame instead breaks when you free a block identifier
𝑛𝑏 pointing to a complete block, but the frame contains the same 𝑛𝑏 pointing to an empty block.
   We now define the resource assertions and their satisfaction relation (IDef. 3):
                       𝜇 |=Res (𝑛𝑏 , 𝑛𝑜 ) ↦→ 𝑣 ⇔ 𝜇 = {𝑛𝑏 ↦→ ({𝑛𝑜 ↦→ 𝑣 }, None)}
                       𝜇 |=Res Bound(𝑛𝑏 ; 𝑛) ⇔ 𝜇 = {𝑛𝑏 ↦→ (∅, Some(𝑛)}
                       𝜇 |=Res 𝑛𝑏 ↦→ ∅         ⇔ 𝜇 = {𝑛𝑏 ↦→ ∅}
The resource assertions consist of: the cell assertion, the bound assertion, and the freed cell assertion.
Note that these resource assertions represent the smallest unit of memory from which to build
larger memory using the separating conjunction. For example, the 𝜇 memory model from Fig. 4
can be represented by the assertion given on the right of the figure. Note that when we defined
CMemB (for IDef. 1), we used (Nat ⇀fin Val, Nat?) instead of the simpler [Val]. This is to ensure
we can define resource assertions for each unit of memory. If the concrete memory model used
lists instead of finite maps, then defining |=Res would become impossible since the relation must
define the entire memory in the relevant block.
   The instance data (SMem, 𝜇ˆ ∅ ) for IDef. 4 is as follows. The memory data type SMem is a simple
symbolic lifting of CMem:
               def                                                        def
       SMem = LExp ⇀fin (SMemB ⊎ {∅})                 where     SMemB = (LExp ⇀fin LExp, LExp?)
                                                                def
The empty symbolic memory is, unsurprisingly, 𝜇ˆ ∅ = ∅. Because the memory data type is a
symbolic lifting, |=Mem (IDef. 5) is straightforward to define. The symbolic action semantics (IDef. 6)
is also symbolically lifted from its concrete counterpart and similarly straightforward. Lastly, the
implementation of consumeRes and produceRes (IDef. 7) are also straightforward.

6.4   Memory Model for Object-oriented Languages
Our CSE theory is not limited to low-level languages such as C, it is also compatible with high-level
languages such as object-oriented languages like JavaScript and Python. In fact, the Gillian project
that inspired our theory has a strong history of JavaScript support, starting from its predecessor
JaVerT [17, 18] (an analysis tool specific to JavaScript). For example, Gillian has been used to test
the data structure library Buckets.js [19, 50] and to verify a JavaScript implementation of a message
header deserialisation module in the AWS Encryption SDK [34].

                         Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:20                                  A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


   We now briefly describe the JavaScript memory model implemented in Gillian to show that it fits
our theory. The model is a variant of the block-offset memory model introduced in the previous sec-
tion; because of the large overlap between the models, we have not mechanised this JavaScript model.
 Model description. The concrete and symbolic memory data types of the JavaScript memory
model implemented in Gillian are as follows (i.e., the data types of IDefs. 1 and 4):11
               def                                                            def
      CMem = Nat ⇀fin (CMemB, {Str}?)                   where      CMemB = Str ⇀fin (Val ⊎ {∅})
               def                                                                  def
      SMem = LExp ⇀fin (SMemB, {LExp}?)                    where      SMemB = LExp ⇀fin (LExp ⊎ {∅})
where {Str} and {LExp} denote sets of Strs and LExps, respectively, and CMemB and SMemB
represent JavaScript objects. The reader should compare these memory data types with the memory
data types of the block-offset memory model and note the following differences. First, note that
offsets (natural numbers) here have been replaced by property names (strings). Because of this, the
bound from the block-offset memory model has been replaced by a set of strings, representing the
“domain” of the object.12 Second, in JavaScript, objects cannot be deallocated, but ∅-annotations for
negative information are needed for a different reason. In JavaScript, reading fields that have not
been set or have been deleted evaluates to undefined (see App. D for an example JavaScript REPL
session where properties are added and deleted). To not break the frame properties of the model,
such “unset” properties must be annotated with ∅.
   The memory model has the following memory actions (IDef. 2):
                  x := newObj(), deleteField(E, E), x := lookup(E, E), mutate(E, E, E).
E.g., deleteField(𝑜, 𝑓 ) deletes field 𝑓 from the object at address 𝑜 and mutate(𝑜, 𝑓 , 𝑣) sets field 𝑓
in the object at address 𝑜 to 𝑣. While the semantics of JavaScript is complex, this simple memory
model is enough to capture its basic operations: in the JavaScript instantiation of Gillian, JavaScript
programs are compiled to GIL, its intermediate representation, where complex operations (such
as looking up an object field by following the “prototype chain”) are compiled to a sequence of
lower-level operations that are either side-effect free, or one of the actions provided above.
   Lastly, the semantics of the actions of the memory model are obtained by applying minor
modifications to the actions of the block-offset memory model. For instance, out-of-bound accesses
happen when a memory lookup is outside the object domain instead of when an offset is outside
the bound of the block, and so on.

6.5      CHERI-assembly Memory Model
To show that our CSE theory can fit novel memory models beyond the usual suspects, we have
designed and mechanised a new symbolic memory model for a CHERI-enabled idealised assembly
language. CHERI [53] is a recently introduced memory-model-based capability protection model: it
guarantees runtime spatial memory safety via hardware, and this is achieved using capabilities: fat
pointers that carry spatial metadata such as bound, permission, and a tag bit stating the validity
of the capability, in addition to the memory address. Additional capability-aware instructions are
added to the instruction set, where the monotonic property is preserved: valid capabilities cannot
gain more bounds or permissions than what they originally had.
   We have proved our memory model OX sound, and plan to prove UX soundness and implement
the memory model in Gillian in future work. To our best knowledge, our memory model is the
11 The memory model in Gillian additionally includes object metadata, which we do not discuss here.
12 This change also leads to a slightly different well-formedness condition. Informally, a memory 𝜇 ∈ CMem is only

well-formed if ∀ (𝑜, Just(𝑑 ) ) ∈ codom(𝜇 ). dom(𝑜 ) ⊆ 𝑑 (see heap-domain invariant [38]). The rest of the well-formedness
condition is similar to the block-offset memory model.


Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                          373:21


                 def                                                               def
      Cap        =     {𝑏𝑙𝑜 : Nat; off : Nat; 𝑏𝑎𝑠𝑒 : Nat;  CMemB-CH                 =     (Nat ⇀ 𝑓 𝑖𝑛 Val + Capfrag, Nat?)
                       𝑙𝑒𝑛 : Nat; 𝑝𝑒𝑟𝑚      ® 𝑡𝑎𝑔 : Bool}
                                    ® x : Bool;                                    def
                                                          CMemBO-CH                 =    Nat ⇀fin (CMemB-CH ⊎ ∅)
                         where 𝑥 ∈ {load, store, ...}                              def
                 def                                       CMemCReg                 =    Nat ⇀fin Cap
 Capfrag         =     {𝑐𝑎𝑝 : Cap, 𝑛𝑡ℎ : Nat}                                      def
                                                              CMem                  =     (CMemCReg, CMemBO-CH )

                                            Fig. 5. The concrete memory data type.

            𝜇     =    (𝜇 R , 𝜇 BO )                      𝑛1       3 𝑐 1 𝑏𝑜𝑢𝑛𝑑 : Some(2)                   (𝑛 1 , 0) ↦→ 3 ★
 (𝜇 R , 𝜇 BO )    ∈    CMem                                                                                (𝑛 1 , 1) ↦→cf 𝑐 1 ★
  𝜇BO (𝑛 1 )      =    ( {0 ↦→ 3, 1 ↦→ 𝑐 1 }, Some(2) )
                                                          𝑛2
                                                                   𝑐 0 ... 𝑐 |Cap−1| 𝑏𝑜𝑢𝑛𝑑 : Some(|Cap|)
                                                                                                           Bound(𝑛 1 ; 2) ★
  𝜇BO (𝑛 2 )      =    ( {𝑖 ↦→ 𝑐𝑖 }, Some( |Cap| )                                                         (𝑛 2 , 0) ↦→cap 𝑐 ★
                        for 𝑖 ∈ {0, 1, ..., |Cap − 1| }                                                    Bound(𝑛 2 , |Cap| ) ★
                                                          𝑟1       𝑐
    𝜇 R (𝑟 1 )    =    𝑐                                                                                   Reg(𝑟 1 ; 𝑐 )

Fig. 6. Example CHERI memory instance 𝜇 expressed formally (left), visually (centre), and as a composition
of resource assertions (right).


first memory model for CHERI that supports SL-based symbolic execution and also comes with a
soundness theorem. Details about related work are given in §7.
   We first discuss the definition of our new memory model. The CHERI-assembly model is the
most substantial instantiation in this work: the CHERI-assembly model has roughly 19K lines of
code, about 5 times larger than the block-offset model, the second most substantial instantiation.
Afterwards, we discuss our design process. The design process is interesting because the memory
model is the first memory model we have designed for our CSE theory without the guidance of
an existing implementation. We explain how our CSE theory guided us to obtain the appropriate
design: we made two failed design attempts before finally arriving at our current design.
   Model description. Our CHERI memory model extends the block-offset memory model of §6.3
to be capability-aware. While the bit-level layout of capabilities may differ between architectures,
even if the metadata is mostly similar; in this work, we work with a CHERI-assembly model with
an abstract and architecture-agnostic design.
   We now give the instance data (CMem, Wf , 𝜇 ∅ , ·) conforming to IDef. 1; we first discuss CMem.
Fig. 5 shows the structure of the CHERI-assembly concrete memory model, and Fig. 6 gives as an
instance example 𝜇. There are two main differences with the block-offset memory model: a separate
mapping for capability registers (i.e. CMemCReg ) is added, and the main memory (i.e. CMemBO-CH )
is extended to be capability-aware. For capability registers, we use the abstract capability Cap,
which contains spatial metadata of capabilities. For the main memory CMemBO-CH , we extend the
block-offset model by also storing capability byte fragments, represented as Capfrag , in addition to
standard values Val. In Fig. 6, we observe 𝜇BO (𝑛 1 ) contains the capability byte fragment 𝑐 1 , which is
the second byte fragment of some capability 𝑐. When a capability is stored in memory, the capability
is stored as a sequence of abstract, contiguous, well-formed capability byte fragments – and we can
observe this in 𝜇BO (𝑛 2 ), where |Cap| is the size of a capability for a given architecture. We note
that each capability byte fragment also stores a tag fragment, and a capability in memory only has
its tag bit set to true if and only if the tag fragment of all the capability fragments is set to true.
Usually, CHERI architectures store tags in the tagged memory, separate from the main memory; in
our model the two memories are merged, and tags are split into tag fragments – the motivation
behind this is explained when we discuss the design process below.

                                  Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:22                                A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


   The well-formedness condition Wf also extends from that of the block-offset memory model.
The additional constraints relate to the well-formedness of capability fragments in the memory.
One obvious property is that the fragment value of Capfrag should be between 0 and |Cap − 1|.
Another property is capability fragments whose tag fragment bit is set to true must be stored in the
appropriate capability-offset-aligned position (the formal description is in App. D). This conforms
to the specification that valid capabilities in memory are stored in a capability-aligned position [52].
All the capability fragments in 𝜇BO (𝑛 1 ) and 𝜇BO (𝑛 2 ) are stored in a capability-off-aligned position,
which makes the overall memory well-formed; but note that if we instead have 𝜇BO (𝑛 1 ) (1) = 𝑐 4 ,
then the memory is well-formed only if 𝑐 4 .𝑐𝑎𝑝.𝑡𝑎𝑔 = false. As we will see below, |=Res must account
for this too, and part of Wf is expressed in |=Res .
   The empty memory 𝜇 ∅ can be straightforwardly defined as (∅, ∅) (which satisfies Wf ), and · is
also a straightforward extension of that of the block-offset memory model.
   We now discuss memory actions (IDef. 2). There
                                                                   fst(𝜇)(𝑟𝑠 ) = 𝑐𝑠           𝑐𝑠 .𝑡𝑎𝑔 = true
are more than 100 memory-action rules, with rela-                                𝑐𝑠 .𝑝𝑒𝑟𝑚 store = true
tively complex definitions. To exemplify, we discuss           𝑟𝑑 is a capability register             fst(𝜇)(𝑟𝑑 ) = 𝑐𝑑
the successful case of the capability store action,              (𝑐𝑠 .𝑝𝑒𝑟𝑚 storecap = true ∨ 𝑐𝑑 .𝑡𝑎𝑔 = false)
shown in Fig. 7. The capability store action takes                      𝑐𝑠 .off + |Cap| ≤ 𝑐𝑠 .𝑏𝑎𝑠𝑒 + 𝑐𝑠 .𝑙𝑒𝑛
in 𝑟𝑠 and 𝑟𝑑 , which are capability register numbers                𝑐𝑠 .off ≥ 𝑐𝑠 .𝑏𝑎𝑠𝑒         𝑐𝑠 .off % |Cap| = 0
pointing to capability registers 𝑐𝑠 and 𝑐𝑑 , respec-                    snd(𝜇)(𝑐𝑠 .𝑏𝑙𝑜) = (𝜇𝑏 , Some(𝑚))
tively. The idea is that we store 𝑐𝑑 in the location                              𝑐𝑠 .off + |Cap| ≤ 𝑚
pointed by 𝑐𝑠 . The action then performs necessary                {𝑐𝑠 .off, ..., 𝑐𝑠 .off + |Cap| − 1} ⊆ dom(𝜇𝑏 )
spatial checks and throws relevant errors when a                        store_capability(𝑐𝑠 , 𝑐𝑑 , 𝜇𝑏 ) = 𝜇𝑏′
spatial safety property is violated, e.g. 𝑐𝑠 must have       𝜇 = (fst(𝜇), snd(𝜇) [𝑐𝑠 .𝑏𝑙𝑜 ↦→ (𝜇𝑏′ , Some(𝑚))])
                                                               ′

the tag bit set to true, and the offset of 𝑐𝑠 must be                   𝜇.store([𝑟𝑠 , 𝑟𝑑 ]) ⇝ ok : (𝜇 ′, [])
within bound and is capability-offset-aligned, etc.
Afterwards, the store_capability function stores 𝑐𝑑 Fig. 7. Semantics of the capability store action.
as a sequence of well-formed contiguous capability
byte fragments in the main memory.
   We now discuss the resources of this model and their satisfaction relation |=Res (IDef. 3). The
three resources used in the block-offset memory model are directly ported. Additionally, we have
two new resources: Reg(𝑟𝑛 ; 𝑐), which describes that at register 𝑟𝑛 the capability 𝑐 is stored, and
(𝑛𝑏 , 𝑛𝑜 ) ↦→𝑐 𝑓 𝑐𝑛 , which states that at block 𝑛𝑏 and offset 𝑛𝑜 , the capability byte fragment 𝑐𝑛 is stored,
where 𝑛 denotes the 𝑛th byte fragment. The resource satisfaction relation |=Res is given below:
         𝜇 |=Res Reg(𝑟𝑛 ; 𝑐)        ⇔ 𝜇 = ({𝑟𝑛 ↦→ 𝑐}, ∅)
         𝜇 |=Res (𝑛𝑏 , 𝑛𝑜 ) ↦→cf 𝑐𝑛 ⇔ 𝜇 = (∅, {𝑛𝑏 ↦→ ({𝑛𝑜 ↦→ 𝑐𝑛 }, None)})
                                      ∧ (𝑐𝑛 .𝑐𝑎𝑝.𝑡𝑎𝑔 = true =⇒ 𝑛𝑜 % |Cap| = 𝑛) ∧ 𝑛 < |Cap|
Whereas defining |=Res for the block-offset memory was straightforward, defining |=Res here is
slightly more involved. Due to Wf of CHERI, we cannot allow capability byte fragments whose
tag fragment bit is true to be stored anywhere, and we require the fragment value to be valid. The
assertion (𝑛 1, 1) ↦→𝑐 𝑓 𝑐 1 in Fig. 6 is satisfiable, but (𝑛 1, 1) ↦→𝑐 𝑓 𝑐 4 is not if 𝑐 4 .𝑐𝑎𝑝.𝑡𝑎𝑔 = true.
   Note that one can define a full, valid capability resource assertion as a user-defined predicate
assertion (𝑛𝑏 , 𝑛𝑜 ) ↦→cap 𝑐 as follows:
                                                 def    |Cap| −1
                              (𝑛𝑏 , 𝑛𝑜 ) ↦→cap 𝑐 = ⋆𝑖=0            (𝑛𝑏 , 𝑛𝑜 + 𝑖) ↦→cf 𝑐𝑖
   In Fig. 6, we can see the capability register mapping is represented using the register assertion,
the capability fragment in 𝜇BO (𝑛 1 ) is represented using the capability fragment assertion, and the
full capability in 𝜇BO (𝑛 2 ) is represented using the user-defined capability predicate assertion.

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                           373:23


   The symbolic memory (IDef. 4) is a direct lifting of its concrete counterpart. The satisfaction
relation |=Mem (IDef. 5) extends that of the block-offset model by additionally relating symbolic
capability registers to concrete ones. The symbolic memory actions (IDef. 6) are a symbolic lifting
of the concrete actions. The implementations of consumeRes and produceRes (IDef. 7) extend those
of the block-offset model: there is now an additional case when consuming or producing capability
fragments depending on the tag fragment value of the capability fragment due to Wf .
   Design process. Our first attempt at designing the memory model was based on that of Park
et al. [42]. That work separated the main memory into two: the (tagless) main memory, and the
tagged memory, where the tagged bit of a capability was stored in the tagged memory. While this
model closely represented the CHERI hardware, the separation made it difficult to reason about the
complex inter-dependency between the two memories, making it difficult to formalise resource
assertions well-formed with respect to the concrete memory and also prove the OX frame property.
   In our second attempt, to address the aforementioned issue, we introduced the notion of a “chunk”
of memory, where a chunk is either a capability or a sequence of values and capability fragments of
size |Cap|. We removed the tagged memory and made capability tags implicitly defined depending
on whether the chunk was a capability or not. Because this model no longer separates the main
memory, there are no inter-dependencies between memories and no troubles proving the OX frame
property or formalising well-formed resource assertions. However, we discovered writing function
specification had limitations, e.g. when the precondition requires a capability fragment, but the
memory comprises the full capability instead, which made the model not truly compositional.
   Our third and final attempt introduced the notion of tag fragments in capability fragments. This
ensured true compositionality, unlike the previous attempt, where there are no limitations on how
to write specifications, whilst avoiding complex inter-dependencies between memories.
   The structure of the concrete memory model naturally guided us to define the current resource
assertions and their satisfaction relation. Indeed, this formalisation gave us confidence that our
parametric CSE theory is well designed: while this work was done independently from the recently
published Iris-MSWasm work [27], we ended up with resource assertions essentially similar to
those used in the Iris-MSWasm work.

6.6   VeriFast-and-Viper-inspired Memory Model for C
We have mechanised a memory model for C inspired by the OX verification platforms VeriFast
and Viper. Specifically, we have ported the memory model of Featherweight VeriFast [22] (FVF), a
formalisation of (a simplified version of) VeriFast, to our CSE theory and proved it OX sound. The
motivation for this work is as follows. Beyond Gillian, VeriFast and Viper are the most well-known
consume-and-produce-based CSE platforms. VeriFast and Viper have similar memory models: they
both maintain a flat collection of “heap chunks” (explained below). The memory model we discuss
in this section shows that our CSE theory can fit such memory models.
   Model description. FVF analyses a simplified C language with the same memory actions as our
running example memory model. In FVF, the concrete memory model (IDef. 1) is a multiset of
concrete heap chunks. A concrete heap chunk is either a points-to chunk 𝑙 ↦→ 𝑣 denoting that there
is an allocated memory cell at address 𝑙 whose current value is 𝑣, or a malloc-block chunk 𝑚𝑏 (𝑙, size)
denoting that a memory block of size size was allocated at address 𝑙 by malloc, i.e., that the memory
cells at addresses 𝑙 through 𝑙 + size − 1 are part of a single block, which will be freed as one unit
when free is called with argument 𝑙. The memory composition operator is multiset union, and all
heap chunks are disjoint. In our instantiation, we represent concrete heap chunks as follows:
                                   def
                         cchunk = CCPointsTo(Nat, Val) | CCMB(Nat, Nat)

                         Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:24                                 A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


  The symbolic memory model (IDef. 4) used in FVF is a multiset of symbolic heap chunks. A
symbolic heap chunk is either a points-to chunk, a malloc-block chunk, or a user-defined-predicate
chunk. Since user-defined predicates are handled independently of the memory model in our CSE
theory, the symbolic chunks of our memory-model instance are as follows:
                                 def
                        schunk = SCPointsTo(LExp, LExp) | SCMB(LExp, LExp)

  The memory actions of the concrete and symbolic memory models (IDefs. 2 and 6 respectively)
and consumeRes and produceRes operations of the symbolic memory model (IDef. 7) are straightfor-
ward. In FVF, the semantics of the memory actions are simply defined in terms of the consume and
produce operations (concrete consume and produce operations are defined for the concrete memory
model) – we therefore do not include any memory actions in our instance. The consumeRes and
produceRes operations (IDef. 7) of FVF implement unique-match branching (as discussed in §6.1) –
our ported implementations therefore do the same.

7   Related Work
   Program logics. Multiple program logics – such as abstract separation logic [11], views [15, 46],
and Iris [24] – are parametric on different PCM-like structures describing memory state and ghost
state. Some of these program logics also feature other types of parametricity, such as programming-
language parametricity. In contrast to CSE, program logics only describe sound inferences rather
than a way to automate reasoning. For memory-model parametricity, the parameters we introduce
in this paper show what is sufficient to animate reasoning and ensuring soundness of this animation.

   Compositional symbolic execution. Since we have already discussed the previous work on founda-
tions of memory-model-parametric CSE [19, 34] in the introduction and overview of this paper, we
only discuss memory-model-monomorphic foundations here.
   Lööw et al. [31] is the only previous work on CSE theory that treats both OX and UX soundness.
The work is inspired by Gillian but monomorphised to the memory model we use as a running
example in this paper. The work is similar to ours in scope in terms of engine features covered
(function calls, user-defined predicates, etc.). Although the work is not mechanised, it is the
monomorphic work that has influenced us the most; in particular, our consume and produce
properties are inspired by the consume and produce properties they introduce, which they like us
use to ensure interoperability of CSE analysis results with program logics and analysis tools built
on top of program logics.
   OX-only CSE is the most well-explored variant of CSE. We list the most significant projects in
chronological order: Appel [1] mechanises a subset of Smallfoot; Jacobs et al. [22] mechanise a subset
of VeriFast; Keuchel et al. [25] argue for the use of Kripke specification monads in mechanising CSE
and illustrate their techniques on small CSE case studies; Zimmerman et al. [58] formalise on paper
a subset of Viper as part of larger work to enable sound gradual verification in Viper; Dardinier
et al. [13] mechanise a soundness framework for translational verifiers, including CSE inspired by
Viper. These projects have either smaller or similar coverage of engine features compared to us.
Most closely related is the work by Dardinier et al. [13], which like us ensure interoperability of
CSE analysis results. Whereas our approach to interoperability forms a semantic connection to
program logics, through the satisfaction relation for assertions 𝜃, (𝑠, 𝜇) |= 𝐴, Dardinier et al. instead
connect up syntactically by proof reconstruction. Larger case studies, for both approaches, are
needed to better evaluate the trade-offs between the two approaches.
   Lastly, the Infer-Pulse work [26] treats only UX soundness for bi-abduction and is not mechanised.
Since their engine is specialised to bi-abduction, their coverage of engine features is small.

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                           373:25


   Compilation to intermediate verification language. An alternative to symbolic execution is com-
pilation to intermediate verification languages (IVLs) such as Boogie [4] and Why3 [16], which
turns the problem of automating reasoning into a compilation problem. We know of no such work
addressing memory-model parametricity. Other IVL topics have received formal treatments: e.g.,
Parthasarathy et al. [43] mechanise proof-producing compilation to IVLs and targets Boogie in
one case study, and Cohen and Johnson-Freyd [12] mechanise the satisfaction relation of the logic
fragment of Why3 and verify two compilation transformations inspired by Why3.
   CHERI memory models. The most closely related previous work on CHERI have targeted CHERI-
C, which extends the C language to support CHERI capabilities. There exist mechanised CHERI-C
memory models formalised in Isabelle/HOL [41, 42] and Rocq [27, 56, 57]. The work of Park et al.
[42] provides an extractable CHERI-C model usable for concrete execution in Gillian, and the
work of Legoupil et al. [27] extends the Iris-Wasm work [47] to incorporate handles, a synonym
for capabilities, and introduces resource assertions for handles. None of these works, however,
cover symbolic execution. ESBMC-CHERI [7] is the only tool that supports symbolic execution of
CHERI-C programs; however, the tool lacks a formal memory model and soundness proof and does
not support compositional reasoning.
   Additional interesting memory models. Gillian has two more memory-model instances which we
have not discussed in this work. First, there is an optimised “block-of-trees” memory model for
C which has been used in C verification case studies [34] (but not described in detail in previous
publications). We will instantiate our CSE theory with this model in the future. Second, in work
parallel to ours, Ayoun et al. [2] have instantiated Gillian to Rust. Gillian’s Rust memory model
comprises several components, including a core heap model that extends the block-of-trees model
for C with support for polymorphism and unknown layouts required by Rust. The memory model
also includes ghost state for lifetime and prophecy reasoning. The model should be expressible
using our theory; with the minor exception of the model’s novel automation for reasoning about
mutable borrows, for which a small generalisation of how Gillian handles user-defined predicates
was required. The handling of user-defined predicates in our theory can easily be generalised
by moving it from the memory-model-independent part of our theory into each memory-model
instance. A bigger obstacle to overcome is the fact that the soundness justification of the memory
model relies on results from RustBelt [23] and RustHornBelt [35], requiring a formal connection
between our theory and Iris to leverage these results.
   Other interesting targets for future memory instantiations include well-validated formal memory
models from, e.g., the Cerberus project [28, 36] or the WebAssembly project [20].

8   Conclusion
In this paper, we have introduced a formal foundation for memory-model-parametric CSE platforms
for verification and/or bug-finding. Multiple research groups have in recent years turned their
attention to formally defining and proving sound CSE tools and platforms; despite this flurry of
activity, the analysis platform Gillian is today the only CSE platform that supports memory-model
parametricity. We hope this paper will inspire and help other CSE projects to also implement
memory-model parametricity. We have also discussed a series of memory-model instantiations of
our CSE theory, some based on or inspired by instantiations developed for Gillian.
   Looking forward, now having in place a formal definition of memory model for CSE, in particular,
sufficient memory-model requirements for memory-model instantiations of our CSE engine to be
sound, we are now in the process of developing a combinator library for memory models, as defined
in this paper, to make it easy to develop and prove sound large and complex memory models by
composing smaller memory-model components together.

                         Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:26                                  A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


Data-availability Statement
The Rocq mechanisation of our CSE theory and its instantiations are available in our artefact [30].

Acknowledgments
We thank the anonymous reviewers for their constructive feedback. We also thank Dawid Lachowicz
for careful comments on earlier drafts of this paper.
   This work was supported by EPSRC Fellowship “VetSpec: Verified Trustworthy Software Specifi-
cation” (EP/R034567/1) (Lööw, Nantes-Sobrinho, and Gardner), Gardner’s faculty gift from Meta
(Lööw and Nantes-Sobrinho), the Amazon Research Award “Gillian-Rust: Unbounded Verification
for Unsafe Rust Code” (Ayoun), and an Imperial College London Department of Computing PhD
Scholarship (Park).

References
 [1] Andrew W. Appel. 2011. VeriSmall: Verified Smallfoot Shape Analysis. In Certified Programs and Proofs. doi:10.1007/978-
     3-642-25379-9_18
 [2] Sacha-Élie Ayoun, Xavier Denis, Petar Maksimović, and Philippa Gardner. 2025. A Hybrid Approach to Semi-automated
     Rust Verification. Proceedings of the ACM on Programming Languages 9, PLDI (2025). doi:10.1145/3729289
 [3] Roberto Baldoni, Emilio Coppa, Daniele Cono D’elia, Camil Demetrescu, and Irene Finocchi. 2018. A Survey of
     Symbolic Execution Techniques. Comput. Surveys 51, 3 (2018). doi:10.1145/3182657
 [4] Mike Barnett, Bor-Yuh Evan Chang, Robert DeLine, Bart Jacobs, and K. Rustan M. Leino. 2006. Boogie: A Modular
     Reusable Verifier for Object-Oriented Programs. In Formal Methods for Components and Objects. doi:10.1007/11804192_17
 [5] Richard Bornat, Cristiano Calcagno, Peter O’Hearn, and Matthew Parkinson. 2005. Permission accounting in separation
     logic. In Symposium on Principles of Programming Languages. doi:10.1145/1040305.1040327
 [6] John Boyland. 2003. Checking Interference with Fractional Permissions. In Static Analysis. doi:10.1007/3-540-44898-5_4
 [7] Franz Brauße, Fedor Shmarov, Rafael Menezes, Mikhail R. Gadelha, Konstantin Korovin, Giles Reger, and Lucas C.
     Cordeiro. 2022. ESBMC-CHERI: towards verification of C programs for CHERI platforms with ESBMC. In International
     Symposium on Software Testing and Analysis. doi:10.1145/3533767.3543289
 [8] Cristiano Calcagno and Dino Distefano. 2011. Infer: An Automatic Program Verifier for Memory Safety of C Programs.
     In NASA Formal Methods Symposium. doi:10.1007/978-3-642-20398-5_33
 [9] Cristiano Calcagno, Dino Distefano, Peter O’Hearn, and Hongseok Yang. 2009. Compositional Shape Analysis by
     Means of Bi-Abduction. In Principles of Programming Languages. doi:10.1145/1480881.1480917
[10] Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. 2011. Compositional Shape Analysis by
     Means of Bi-Abduction. Journal of the ACM 58, 6 (2011). doi:10.1145/2049697.2049700
[11] Cristiano Calcagno, Peter W. O’Hearn, and Hongseok Yang. 2007. Local Action and Abstract Separation Logic. In
     Symposium on Logic in Computer Science. doi:10.1109/LICS.2007.30
[12] Joshua M. Cohen and Philip Johnson-Freyd. 2024. A Formalization of Core Why3 in Coq. Proc. ACM Program. Lang. 8,
     POPL (2024). doi:10.1145/3632902
[13] Thibault Dardinier, Michael Sammler, Gaurav Parthasarathy, Alexander J. Summers, and Peter Müller. 2025. Formal
     Foundations for Translational Separation Logic Verifiers. Proc. ACM Program. Lang. 9, POPL (2025). doi:10.1145/3704856
[14] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In Tools and Algorithms for the Construction
     and Analysis of Systems. doi:10.1007/978-3-540-78800-3_24
[15] Thomas Dinsdale-Young, Lars Birkedal, Philippa Gardner, Matthew Parkinson, and Hongseok Yang. 2013. Views:
     compositional reasoning for concurrent programs. In Symposium on Principles of Programming Languages. doi:10.1145/
     2429069.2429104
[16] Jean-Christophe Filliâtre and Andrei Paskevich. 2013. Why3 — Where Programs Meet Provers. In European Symposium
     on Programming. doi:10.1007/978-3-642-37036-6_8
[17] José Fragoso Santos, Petar Maksimović, Daiva Naudžiūnienė, Thomas Wood, and Philippa Gardner. 2018. JaVerT:
     JavaScript Verification Toolchain. Proceedings of the ACM on Programming Languages 2, POPL (2018). doi:10.1145/
     3158138
[18] José Fragoso Santos, Petar Maksimović, Gabriela Sampaio, and Philippa Gardner. 2019. JaVerT 2.0: Compositional
     Symbolic Execution for JavaScript. Proceedings of the ACM on Programming Languages 3, POPL (2019). doi:10.1145/
     3290379
[19] José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner. 2020. Gillian, Part I: A Multi-
     language Platform for Symbolic Execution. In Conference on Programming Language Design and Implementation.


Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                  373:27


     doi:10.1145/3385412.3386014
[20] Andreas Haas, Andreas Rossberg, Derek L. Schuff, Ben L. Titzer, Michael Holman, Dan Gohman, Luke Wagner, Alon
     Zakai, and JF Bastien. 2017. Bringing the web up to speed with WebAssembly. In Conference on Programming Language
     Design and Implementation. doi:10.1145/3062341.3062363
[21] Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank Piessens. 2011. VeriFast: A
     Powerful, Sound, Predictable, Fast Verifier for C and Java. In NASA Formal Methods Symposium. doi:10.1007/978-3-642-
     20398-5_4
[22] Bart Jacobs, Frédéric Vogels, and Frank Piessens. 2015. Featherweight VeriFast. Logical Methods in Computer Science 11
     (2015). Issue 3. doi:10.2168/LMCS-11(3:19)2015
[23] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2017. RustBelt: securing the foundations of the
     Rust programming language. Proc. ACM Program. Lang. 2, POPL (2017). doi:10.1145/3158154
[24] Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Aleš Bizjak, Lars Birkedal, and Derek Dreyer. 2018. Iris from the
     ground up: A modular foundation for higher-order concurrent separation logic. Journal of Functional Programming
     (JFP) 28 (2018). doi:10.1017/S0956796818000151
[25] Steven Keuchel, Sander Huyghebaert, Georgy Lukyanov, and Dominique Devriese. 2022. Verified symbolic execution
     with Kripke specification monads (and no meta-programming). Proc. ACM Program. Lang. 6, ICFP (2022). doi:10.1145/
     3547628
[26] Quang Loc Le, Azalea Raad, Jules Villard, Josh Berdine, Derek Dreyer, and Peter W. O’Hearn. 2022. Finding Real Bugs
     in Big Programs with Incorrectness Logic. Proceedings of the ACM on Programming Languages 6, OOPSLA1 (2022).
     doi:10.1145/3527325
[27] Maxime Legoupil, June Rousseau, Aïna Linn Georges, Jean Pichon-Pharabod, and Lars Birkedal. 2024. Iris-MSWasm:
     Elucidating and Mechanising the Security Invariants of Memory-Safe WebAssembly. Proc. ACM Program. Lang. 8,
     OOPSLA2 (2024). doi:10.1145/3689722
[28] Rodolphe Lepigre, Michael Sammler, Kayvan Memarian, Robbert Krebbers, Derek Dreyer, and Peter Sewell. 2022. VIP:
     Verifying Real-World C Idioms with Integer-Pointer Casts. Proc. ACM Program. Lang. 6, POPL (2022). doi:10.1145/
     3498681
[29] Xavier Leroy. 2009. Formal verification of a realistic compiler. Commun. ACM 52, 7 (2009). doi:10.1145/1538788.1538814
[30] Andreas Lööw, Seung Hoon Park, Daniele Nantes-Sobrinho, Sacha-Élie Ayoun, Opale Sjöstedt, and Philippa Gardner.
     2025. Compositional Symbolic Execution for the Next 700 Memory Models (Artefact). doi:10.5281/ZENODO.16909361
[31] Andreas Lööw, Daniele Nantes-Sobrinho, Sacha-Élie Ayoun, Caroline Cronjäger, Petar Maksimović, and Philippa
     Gardner. 2024. Compositional Symbolic Execution for Correctness and Incorrectness Reasoning. In European Conference
     on Object-Oriented Programming. doi:10.4230/LIPIcs.ECOOP.2024.25
[32] Andreas Lööw, Daniele Nantes-Sobrinho, Sacha-Élie Ayoun, Petar Maksimović, and Philippa Gardner. 2024. Matching
     Plans for Frame Inference in Compositional Reasoning. In European Conference on Object-Oriented Programming.
     doi:10.4230/LIPIcs.ECOOP.2024.26
[33] Petar Maksimović, Caroline Cronjäger, Andreas Lööw, Julian Sutherland, and Philippa Gardner. 2023. Exact Separation
     Logic. In European Conference on Object-Oriented Programming. doi:10.4230/LIPIcs.ECOOP.2023.19
[34] Petar Maksimović, Sacha-Élie Ayoun, José Fragoso Santos, and Philippa Gardner. 2021. Gillian, Part II: Real-World
     Verification for JavaScript and C. In Computer Aided Verification. doi:10.1007/978-3-030-81688-9_38
[35] Yusuke Matsushita, Xavier Denis, Jacques-Henri Jourdan, and Derek Dreyer. 2022. RustHornBelt: a semantic foundation
     for functional verification of Rust programs with unsafe code. In Conference on Programming Language Design and
     Implementation. doi:10.1145/3519939.3523704
[36] Kayvan Memarian, Victor B. F. Gomes, Brooks Davis, Stephen Kell, Alexander Richardson, Robert N. M. Watson,
     and Peter Sewell. 2019. Exploring C semantics and pointer provenance. Proc. ACM Program. Lang. 3, POPL (2019).
     doi:10.1145/3290380
[37] Peter Müller, Malte Schwerhoff, and Alexander J. Summers. 2016. Viper: A Verification Infrastructure for Permission-
     Based Reasoning. In Verification, Model Checking, and Abstract Interpretation. doi:10.1007/978-3-662-49122-5_2
[38] Daiva Naudziuniene. 2018. An Infrastructure for Tractable Verification of JavaScript Programs. Ph. D. Dissertation.
     Imperial College London.
[39] Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. 2001. Local Reasoning about Programs that Alter Data
     Structures. In Computer Science Logic. doi:10.1007/3-540-44802-0_1
[40] Scott Owens, Magnus O. Myreen, Ramana Kumar, and Yong Kiam Tan. 2016. Functional Big-Step Semantics. In
     European Symposium on Programming Languages and Systems. doi:10.1007/978-3-662-49498-1_23
[41] Seung Hoon Park. 2022. A Formal CHERI-C Memory Model. Archive of Formal Proofs (November 2022). https://isa-
     afp.org/entries/CHERI-C_Memory_Model.html, Formal proof development.
[42] Seung Hoon Park, Rekha Pai, and Tom Melham. 2023. A Formal CHERI-C Semantics for Verification. In Tools and
     Algorithms for the Construction and Analysis of Systems. doi:10.1007/978-3-031-30823-9_28


                           Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:28                                  A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


[43] Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers. 2024. Towards
     Trustworthy Automated Program Verifiers: Formally Validating Translations into an Intermediate Verification Language.
     Proc. ACM Program. Lang. 8, PLDI (2024). doi:10.1145/3656438
[44] Christopher Pulte, Dhruv C. Makwana, Thomas Sewell, Kayvan Memarian, Peter Sewell, and Neel Krishnaswami. 2023.
     CN: Verifying Systems C Code with Separation-Logic Refinement Types. Proceedings of the ACM on Programming
     Languages 7, POPL (2023). doi:10.1145/3571194
[45] Azalea Raad, Josh Berdine, Hoang-Hai Dang, Derek Dreyer, Peter O’Hearn, and Jules Villard. 2020. Local Reasoning
     About the Presence of Bugs: Incorrectness Separation Logic. In Computer Aided Verification. doi:10.1007/978-3-030-
     53291-8_14
[46] Azalea Raad, Josh Berdine, Derek Dreyer, and Peter W. O’Hearn. 2022. Concurrent Incorrectness Separation Logic.
     Proceedings of the ACM on Programming Languages 6, POPL (2022). doi:10.1145/3498695
[47] Xiaojia Rao, Aïna Linn Georges, Maxime Legoupil, Conrad Watt, Jean Pichon-Pharabod, Philippa Gardner, and Lars
     Birkedal. 2023. Iris-Wasm: Robust and Modular Verification of WebAssembly Programs. Proc. ACM Program. Lang. 7,
     PLDI (2023). doi:10.1145/3591265
[48] John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In Logic in Computer Science.
     doi:10.1109/LICS.2002.1029817
[49] Rocq. [n. d.]. The Rocq Prover. https://rocq-prover.org.
[50] Mauricio Santos. [n. d.]. Buckets-JS: A JavaScript Data Structure Library. https://github.com/mauriciosantos/Buckets-
     JS.
[51] Malte Hermann Schwerhoff. 2016. Advancing Automated, Permission-Based Program Verification Using Symbolic
     Execution. Ph. D. Dissertation. ETH Zürich.
[52] Robert N. M. Watson, Peter G. Neumann, Jonathan Woodruff, Michael Roe, Hesham Almatary, Jonathan Anderson,
     John Baldwin, Graeme Barnes, David Chisnall, Jessica Clarke, Brooks Davis, Lee Eisen, Nathaniel Wesley Filardo,
     Franz A. Fuchs, Richard Grisenthwaite, Alexandre Joannou, Ben Laurie, A. Theodore Markettos, Simon W. Moore,
     Steven J. Murdoch, Kyndylan Nienhuis, Robert Norton, Alexander Richardson, Peter Rugg, Peter Sewell, Stacey Son,
     and Hongyan Xia. 2023. Capability Hardware Enhanced RISC Instructions: CHERI Instruction-Set Architecture (Version 9).
     Technical Report UCAM-CL-TR-987. University of Cambridge, Computer Laboratory. doi:10.48456/tr-987
[53] Jonathan Woodruff, Robert N. M. Watson, David Chisnall, Simon W. Moore, Jonathan Anderson, Brooks Davis, Ben
     Laurie, Peter G. Neumann, Robert Norton, and Michael Roe. 2014. The CHERI capability model: Revisiting RISC in an
     age of risk. In International Symposium on Computer Architecture (ISCA). doi:10.1109/ISCA.2014.6853201
[54] Hongseok Yang. 2001. Local Reasoning for Stateful Programs. Ph. D. Dissertation. University of Illinois Urbana-
     Champaign.
[55] Hongseok Yang and Peter O’Hearn. 2002. A Semantic Basis for Local Reasoning. In Foundations of Software Science
     and Computation Structures. doi:10.1007/3-540-45931-6_28
[56] Vadim Zaliva, Kayvan Memarian, Ricardo Almeida, Jessica Clarke, Brooks Davis, Alexander Richardson, David
     Chisnall, Brian Campbell, Ian Stark, Robert N. M. Watson, and Peter Sewell. 2024. Formal Mechanised Semantics of
     CHERI C: Capabilities, Undefined Behaviour, and Provenance. In International Conference on Architectural Support for
     Programming Languages and Operating Systems. doi:10.1145/3617232.3624859
[57] Vadim Zaliva, Kayvan Memarian, Brian Campbell, Ricardo Almeida, Nathaniel Filardo, Ian Stark, and Peter Sewell.
     2025. A CHERI C Memory Model for Verified Temporal Safety. In International Conference on Certified Programs and
     Proofs. doi:10.1145/3703595.3705878
[58] Conrad Zimmerman, Jenna DiVincenzo, and Jonathan Aldrich. 2024. Sound Gradual Verification with Symbolic
     Execution. Proceedings of the ACM on Programming Languages 8, POPL (2024). doi:10.1145/3632927




Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                              373:29


A     Concrete Definitions and Semantics
This section provides additional concrete definitions and an exhastive enumeration of the rules of
the concrete semantics for our programming language.

A.1     Additional Definitions
The sets of program variables for expressions and commands, denoted by pv(E) and pv(C) respec-
tively, are defined in the standard way.

A.2     Conventions
The following two conventions help simplify some of our definitions and proofs. First, we only
consider executions where no program variables are missing, that is, for a given program C and
a program store 𝑠 we must have dom(𝑠) ⊆ pv(C). Second, we consider the program variables err
(used for error reporting) and ret (used in the definition of function specifications) to be reserved
and assume they do not occur in programs or stores during execution.

A.3     Expression Evaluation
Expression evaluation is trivially defined, we provide some illustrative cases:
                            J𝑣K𝑠      = 𝑣
                            JxK𝑠      = 𝑠((x)
                                           JE1 K𝑠 + JE2 K𝑠 , JE1 K𝑠 ∈ Nat, JE2 K𝑠 ∈ Nat
                    JE1 + E2 K𝑠       =
                                            ,                otherwise
                                         (
                                           JE1 K𝑠 /JE2 K𝑠 , JE1 K𝑠 ∈ Nat, JE2 K𝑠 ∈ Nat, JE2 K𝑠 ≠ 0
                    JE1 / E2 K𝑠       =
                                            ,               otherwise

A.4     Functions and Function Implementation Contexts
A function, 𝑓 (®x) { C; return E }, comprises: an identifier, 𝑓 ∈ Fid ⊆ Str; the parameters, x®, given by a
list of distinct program variables; a function body, C ∈ Cmd; and a return expression, E ∈ PExp, with
pv(E) ⊆ {®x} ∪pv(C). A function implementation context, 𝛾, is a finite partial function from function
identifiers to their parameters, bodies and return expressions: 𝛾 : Fid ⇀fin ( [PVar], Cmd, PExp),
where for 𝛾 (𝑓 ) = (®x, C, E), we also write 𝑓 (®x){C; return E} ∈ 𝛾.

A.5     Concrete Semantics
The rules of the semantics is as follows:
      Skip                          Assign                                         Assign-Err-Eval
                                    JEK𝑠 = 𝑣            𝑠 ′ = 𝑠 [x ↦→ 𝑣]           JEK𝑠 =      𝑠 ′ = 𝑠 [err ↦→ “ExprEval”]
      𝜎, skip ⇓𝛾 ok : 𝜎              (𝑠, 𝜇), x := E ⇓𝛾 ok : (𝑠 ′, 𝜇)                       (𝑠, 𝜇), x := E ⇓𝛾 err : (𝑠 ′, 𝜇)

 Memory-Action                                                             Memory-Action-Err-Length
  ® 𝑠 = 𝑣®
 JEK            𝑣 ) ⇝ ok : (𝜇 ′, 𝑣®′ )
           𝜇.𝛼 (®                                       𝑣 ′ | = |®x |
                                                       |®                   ® 𝑠 = 𝑣®
                                                                           JEK                𝑣 ) ⇝ ok : (𝜇 ′, 𝑣®′ )
                                                                                         𝜇.𝛼 (®                       𝑣 ′ | ≠ |®x |
                                                                                                                     |®
               𝑠 ′ = 𝑠 [®x ↦→ 𝑣®′ ]                                                 ′
                                                                                  𝑠 = 𝑠 [err ↦→ “ActionArgsLength”]
                               ® ⇓𝛾 ok : (𝑠 ′, 𝜇 ′ )
             (𝑠, 𝜇), x® := 𝛼 ( E)                                                                      ® ⇓𝛾 err : (𝑠 ′, 𝜇 ′ )
                                                                                     (𝑠, 𝜇), x® := 𝛼 ( E)

      Memory-Action-Err
       ® 𝑠 = 𝑣®
      JEK            𝑣 ) ⇝ 𝑜 : (𝜇 ′, 𝑣®′ )
                𝜇.𝛼 (®                                  𝑜 ≠ ok             Memory-Action-Err-Eval
                 𝑠 = 𝑠 [err ↦→ 𝑣®′ ]
                  ′                                                         ® 𝑠=
                                                                           JEK       𝑠 ′ = 𝑠 [err ↦→ “ExprEval”]
                                ® ⇓𝛾 𝑜 : (𝑠 ′, 𝜇 ′ )
              (𝑠, 𝜇), x® := 𝛼 ( E)                                                                ® ⇓𝛾 err : (𝑠 ′, 𝜇)
                                                                                (𝑠, 𝜇), x® := 𝛼 ( E)

                              Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:30                                       A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner

                 If-Then                                                 If-Else
                   JEK𝑠 = true       (𝑠, 𝜇), C1 ⇓𝛾 𝑜 : 𝜎 ′                JEK𝑠 = false      (𝑠, 𝜇), C2 ⇓𝛾 𝑜 : 𝜎 ′
                                                              ′
                  (𝑠, 𝜇), if (E) C1 else C2 ⇓𝛾 𝑜 : 𝜎                     (𝑠, 𝜇), if (E) C1 else C2 ⇓𝛾 𝑜 : 𝜎 ′

            If-Err-Eval                                                If-Err-Type
             JEK𝑠 =     𝑠 ′ = 𝑠 [err ↦→ “ExprEval”]                     JEK𝑠 = 𝑣 ∉ Bool 𝑠 ′ = 𝑠 [err ↦→ “Type”]
             (𝑠, 𝜇), if (E) C1 else C2 ⇓𝛾 err : (𝑠 ′, 𝜇)                (𝑠, 𝜇), if (E) C1 else C2 ⇓𝛾 err : (𝑠 ′, 𝜇)

                    Seq                                                         Seq-Err
                    𝜎, C1 ⇓𝛾 ok : 𝜎 ′         𝜎 ′, C2 ⇓𝛾 𝑜 : 𝜎 ′′               𝜎, C1 ⇓𝛾 𝑜 : 𝜎 ′        𝑜 ≠ ok
                                                         ′′
                                𝜎, C1 ; C2 ⇓𝛾 𝑜 : 𝜎                                  𝜎, C1 ; C2 ⇓𝛾 𝑜 : 𝜎 ′

      Func
                     𝑓 (®x) { C; return E′ } ∈ 𝛾
          ®
        | E| = |®x |         ® 𝑠 = 𝑣® ®z = (pv(C) \ {®x})
                            JEK
       𝑠𝑝 = ∅[®x ↦→ 𝑣®] [®z ↦→ null]          JE′ K𝑠𝑞 = 𝑣 ′          Func-Err-Missing
                                     ′
      (𝑠𝑝 , 𝜇), C ⇓𝛾 ok : (𝑠𝑞 , 𝜇 )        𝑠 = 𝑠 [y ↦→ 𝑣 ′ ]
                                            ′
                                                                     𝑓 ∉ dom(𝛾)    𝑠 ′ = 𝑠 [err ↦→ “FuncMissing”]
                                 ® ⇓𝛾 ok : (𝑠 ′, 𝜇 ′ )
                (𝑠, 𝜇), y := 𝑓 ( E)                                                             ® ⇓𝛾 err : (𝑠 ′, 𝜇)
                                                                               (𝑠, 𝜇), x := 𝑓 ( E)

             Func-Err-Args-Length                                      Func-Err-Args-Eval
             𝑓 (®x) { C; return E′ } ∈ 𝛾      ® ≠ |®x |
                                            | E|                        𝑓 (®x) { C; return E′ } ∈ 𝛾         ® = |®x |
                                                                                                          | E|
                𝑠 ′ = 𝑠 [err ↦→ “FuncArgsLength”]                        ® 𝑠=
                                                                       JEK             𝑠 ′ = 𝑠 [err ↦→ “ExprEval”]
                                   ® ⇓𝛾 err : (𝑠 ′, 𝜇)
                  (𝑠, 𝜇), y := 𝑓 ( E)                                                         ® ⇓𝛾 err : (𝑠 ′, 𝜇)
                                                                             (𝑠, 𝜇), y := 𝑓 ( E)

                                                                         Func-Err-Eval-Ret
   Func-Err-Body                                                                       𝑓 (®x) { C; return E′ } ∈ 𝛾
                  𝑓 (®x) { C; return E′ } ∈ 𝛾                              ®
                                                                         | E| = |®x |        ® 𝑠 = 𝑣®
                                                                                            JEK              ®z = (pv(C) \ {®x})
        ® = |®x |
      | E|              ® 𝑠 = 𝑣®
                       JEK            z = (pv(C) \ {®x})                              𝑠𝑝 = ∅[®x ↦→ 𝑣®] [®z ↦→ null]
           𝑠𝑝 = ∅[®x ↦→ 𝑣®] [®z ↦→ null]       𝑜 ≠ ok                        (𝑠𝑝 , 𝜇), C ⇓𝛾 ok : (𝑠𝑞 , 𝜇 ′ )       JE′ K𝑠𝑞 =
   (𝑠𝑝 , 𝜇), C ⇓𝛾 𝑜 : (𝑠𝑞 , 𝜇 ′ )   𝑠 ′ = 𝑠 [err ↦→ 𝑠𝑞 (err)]                           ′
                                                                                       𝑠 = 𝑠 [err ↦→ “ExprEval”]
                                   ® ⇓𝛾 𝑜 : (𝑠 ′, 𝜇 ′ )
                  (𝑠, 𝜇), y := 𝑓 ( E)                                                             ® ⇓𝛾 err : (𝑠 ′, 𝜇 ′ )
                                                                                 (𝑠, 𝜇), y := 𝑓 ( E)

A.6      OX and UX Frame Properties
For completeness, we state the OX and UX frame properties (in the familiar style of SL and ISL) for
the full semantics:
  Theorem A.1 (OX and UX Frame). For Wf (𝜇) and Wf (𝜇 𝑓 ):
         (𝑠, 𝜇 · 𝜇 𝑓 ), C ⇓𝛾 𝑜 : (𝑠 ′, 𝜇 ′ ) ⇒
            ∃𝑠 ′′, 𝜇 ′′, 𝑜 ′ . (𝑠, 𝜇), C ⇓𝛾 𝑜 ′ : (𝑠 ′′, 𝜇 ′′ ) ∧ (𝑜 ′ ≠ miss ⇒ (𝑜 ′ = 𝑜 ∧ 𝑠 ′′ = 𝑠 ′ ∧ 𝜇 ′ = 𝜇 ′′ · 𝜇 𝑓 ))
         (𝑠, 𝜇), C ⇓𝛾 𝑜 : (𝑠 ′, 𝜇 ′ ) ∧ 𝑜 ≠ miss ∧ 𝜇 ′ · 𝜇 𝑓 defined ⇒
            (𝑠, 𝜇 · 𝜇 𝑓 ), C ⇓𝛾 𝑜 : (𝑠 ′, 𝜇 ′ · 𝜇 𝑓 )




Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                    373:31


B     Assertions and Function Specifications: Extended Definitions
In this section, we define all the necessary constructs required for defining the relevant program
logics. In particular, we formally define the function specification for SL, ISL, and ESL, including
the internalisation of function specifications.

B.1    Additional Definitions
The expression pv(𝐴) denotes the set of program variables of 𝐴, and lv(𝐴) denotes the set of
logical variables of 𝐴.

B.2    Logical Expression Evaluation
We also define a logical expression evaluation function; some cases are provided below:
                                            J𝑣K𝜃,𝑠     = 𝑣
                                            JxK𝜃,𝑠     = 𝑠((x)
                                                           𝜃 (x), x ∈ dom(𝜃 )
                                            JxK𝜃,𝑠     =
                                                              ,    otherwise
                                                          (
                                                            true, JEK𝜃,𝑠 ∈ 𝜏
                                       JE ∈ 𝜏K𝜃,𝑠      =
                                                            false, otherwise
                                                          (
                                                            true, JEK𝜃,𝑠 ≠
                                    JE ∈ ValK𝜃,𝑠       =
                                                            false, otherwise
We sometimes omit the store and write JEK𝜃 instead of JEK𝜃,𝑠 when the store irrelevant to the
outcome of evaluating the logical expression E.

B.3    Assertion Satisfaction Relation
To define the assertion satisfaction relation, we assume we are given a set Preds containing predicate
definitions. The elements of the set (𝑝, 𝑥®in, 𝑥®out, 𝐴) ∈ Preds, denoted 𝑝 (𝑥®in ; 𝑥®out ) {𝐴} ∈ Preds, have
              ® LVar,
type (Str, LVar,    ® Asrt), where 𝑝 is the predicate name, 𝑥®in the input parameters, 𝑥®out the output
parameters, and 𝐴 the predicate body. Predicate definitions satisfy the following:
    • No duplicates in 𝑥®in or 𝑥®out
    • 𝑥®in ∩ 𝑥®out = ∅
    • pv(𝐴) = ∅
    • lv(𝐴) ⊆ 𝑥®in ∪ 𝑥®out
                             Ô
    • 𝐴 is of the form 𝐴 = 𝑖 𝐴𝑖 where for each 𝐴𝑖 we have 𝑥®out ⊆ lv(𝐴𝑖 )
  We now define the assertion satisfaction relation. Most of the below cases are defined straightfor-
wardly, but we note that for the logical expression case, we assume the heap is empty. The memory
resource case depends on the resource satisfaction relation introduced in §4.
        𝜃, (𝑠, 𝜇) |= E               ⇔ JEK𝜃,𝑠 = true ∧ 𝜇 = 𝜇 ∅
                     True            ⇔ Wf (𝜇)
                     𝐴1 ⇒ 𝐴2 ⇔ 𝜃, (𝑠, 𝜇) |= 𝐴1 ⇒ 𝜃, (𝑠, 𝜇) |= 𝐴2
                     𝐴1 ∨ 𝐴2 ⇔ 𝜃, (𝑠, 𝜇) |= 𝐴1 ∨ 𝜃, (𝑠, 𝜇) |= 𝐴2
                     ∃x. 𝐴           ⇔ ∃𝑣 ∈ Val. 𝜃 [x ↦→ 𝑣], (𝑠, 𝜇) |= 𝐴
                     emp             ⇔ 𝜇 = 𝜇∅
                     𝐴1 ★ 𝐴2 ⇔ ∃𝜇1, 𝜇2 . 𝜇 = 𝜇1 · 𝜇2 ∧ 𝜃, (𝑠, 𝜇 1 ) |= 𝐴1 ∧ 𝜃, (𝑠, 𝜇 2 ) |= 𝐴2
                     𝑟 ( E®1 ; E®2 ) ⇔ JE®1 K𝜃,𝑠 = 𝑣®1 ∧ JE®2 K𝜃,𝑠 = 𝑣®2 ∧ 𝜇 |=Res 𝑟 (𝑣®1 ; 𝑣®2 )
                     𝑝 ( E®1 ; E®2 ) ⇔ 𝜃, (𝑠, 𝜇) |= 𝐴[ E®1 /®
                                                            𝑥 in ] [ E®2 /®
                                                                          𝑥 out ] for 𝑝 (𝑥®in ; 𝑥®out ) {𝐴} ∈ Preds

                           Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:32                                A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


  An assertion 𝐴 is valid, denoted |= 𝐴, iff ∀𝜃, 𝑠, 𝜇. 𝜃, (𝑠, 𝜇) |= 𝐴.

B.4      Function Specifications
  SL, ISL, and ESL quadruples. We use the following notations for SL, ISL, and ESL command
quadruples:
                                                                              
    𝑃 C 𝑜𝑘 : 𝑄 ok 𝑒𝑟𝑟 : 𝑄 err ,   𝑃 C ok : 𝑄 ok err : 𝑄 err ,   𝑃 C ok : 𝑄 ok err : 𝑄 err ,
for command C, precondition 𝑃 ∈ Asrt, successful postcondition 𝑄 ok ∈ Asrt, and faulting postcondi-
tion 𝑄 err ∈ Asrt. The corresponding triples are defined as degenerate cases of the above quadruples,
with 𝑄 ok = false or 𝑄 err = false.
   The validity of SL, ISL, and ESL quadruples are defined as follows:
                                                       def
             𝛾 |= 𝑃 C ok : 𝑄 ok err : 𝑄 err = (∀𝜃, 𝑠 ′, 𝜇 ′, 𝑜.
                                       

                   𝜃, (𝑠 ′, 𝜇 ′ ) |= 𝑄𝑜 ⇒ (∃𝑠, 𝜇. 𝜃, (𝑠, 𝜇) |= 𝑃 ∧ (𝑠, 𝜇), C ⇓𝛾 𝑜 : (𝑠 ′, 𝜇 ′ )))
                                                         def
             𝛾 |= 𝑃 C 𝑜𝑘 : 𝑄 ok 𝑒𝑟𝑟 : 𝑄 err = (∀𝜃, 𝑠, 𝜇, 𝑜, 𝑠 ′, 𝜇 ′ .
                                          

                   𝜃, (𝑠, 𝜇) |= 𝑃 ∧ (𝑠, 𝜇), C ⇓𝛾 𝑜 : (𝑠 ′, 𝜇 ′ ) ⇒ (𝑜 ≠ miss ∧ 𝜃, (𝑠 ′, 𝜇 ′ ) |= 𝑄𝑜 ))
                                                    def
             𝛾 |= 𝑃 C ok : 𝑄        ok err : 𝑄 err =                                         
                   𝛾 |= 𝑃 C 𝑜𝑘 : 𝑄 ok 𝑒𝑟𝑟 : 𝑄 err ∧ 𝛾 |= 𝑃 C ok : 𝑄 ok err : 𝑄 err
Informally, an SL quadruple is valid if all terminating executions from 𝑃 of C are contained in 𝑄 ok
and 𝑄 err ; an ISL quadruple is valid if all models of 𝑄 ok and 𝑄 err are reachable from 𝑃 through C;
and an ESL quadruple is valid if both corresponding SL and ISL quadruples are valid.
   We write 𝑃       𝑜𝑘 : 𝑄 ok 𝑒𝑟𝑟 : 𝑄 err to denote the type of specification may be SL, ISL, or ESL.
  SL, ISL, and ESL function specifications. Function specifications comprise external specifications,
which describe the interface of the function toward its callers, and internal specifications, satisfied by
the function body. An external specification has the form x® = 𝑥® ★ 𝑃      𝑜𝑘 : 𝑄 ok 𝑒𝑟𝑟 : 𝑄 err where:
    • x® are distinct, 𝑥® are distinct, and pv(𝑃) = ∅;
    • pv(𝑄 ok ) = {ret} or 𝑄 ok = false;
    • and pv(𝑄 err ) = {err} or 𝑄 err = false.
The set of external specifications is denoted by ES𝑝𝑒𝑐. A function specification context (also:
specification context), Γ, is a finite partial function from function identifiers to a finite set of
external specifications: Γ ∈ Fid ⇀fin P (ES𝑝𝑒𝑐).
  We define an internalisation function for external specifications, adapting the definition intro-
duced in ESL [33]. Given implementation context 𝛾 and function 𝑓 (®x) { C; return E } ∈ 𝛾, an ISL
                                    UX
specification internalisation, Int𝛾,𝑓   , is defined by:

                              UX x = x ★ P
                                                                    def
                           Int𝛾,𝑓 (                ok : 𝑄 ok err : 𝑄 err ) =
                                                                   ′             ′
                                                                                
                              { x = x ★ P ★ ®z = null ok : 𝑄 ok          err : 𝑄 err   :
                                          ′ ⇒ E ∈ Val ★ True,
                                     |= 𝑄 ok
                                     |= 𝑄 ok ⇒ ∃𝑝.    ′ [𝑝/®
                                                 ® 𝑄 ok  ® p] ★ ret = E[𝑝/®® p],
                                     |= 𝑄 err ⇒ ∃𝑝.    ′ [𝑝/®
                                                 ® 𝑄 err   ® p] }
                                                                                                  ′ and
where ®z = pv(C)\{®x}, p® = {®x} ⊎ {®z}, and the logical variables 𝑝® are fresh with respect to 𝑄 ok
  ′
𝑄 err . The internal precondition simply extends the external one with locals initialised to null. As
UX reasoning cannot lose information, internal postconditions will contain information about
program variables, whereas external ones must not, given variable scoping. The transition from
internal to external postconditions forgets program variables by substituting them with fresh logical

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                           373:33

                                                                                              OX
variables, and uses backwards consequence. SL specification internalisation, denoted by Int𝛾,𝑓   , is
defined analogously, with the two latter implications reversed to use forward consequence (e.g.,
|= 𝑄 ok ⇐ ∃𝑝.   ′ [𝑝/®
            ® 𝑄 ok ® p] ★ ret = E[𝑝/®
                                  ® p]). ESL specification internalisation instead uses equivalence.
    Function environments. A function environment, (𝛾, Γ), is a pair comprising an implementation
context 𝛾 and a specification context Γ. A function environment (𝛾, Γ) is valid, written |= (𝛾, Γ),
iff every function in Γ has an implementation in 𝛾 and for every external specification in Γ there
exists a corresponding internal specification valid under 𝛾. Lastly, a function specification is valid
in a context Γ, denoted by Γ |= 𝑃 𝑓 (®x) 𝑜𝑘 : 𝑄 ok 𝑒𝑟𝑟 : 𝑄 err iff for all 𝛾 such that |= (𝛾, Γ) it
holds that 𝛾 |= 𝑃 𝑓 (®x) 𝑜𝑘 : 𝑄 ok 𝑒𝑟𝑟 : 𝑄 err .




                         Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:34                                     A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


C     Symbolic Definitions and Semantics
This section provides additional symbolic definitions and additional rules of the symbolic semantics
   ˆ C ⇓Γ 𝑜 : 𝑂 ′, 𝜎ˆ ′ . For the rules, in order to keep clutter to a minimum, we omit mentioning the
𝑂, 𝜎,
oracles for the rules unless the oracle plays a role, i.e., 𝜎, ˆ C ⇓Γ 𝑜 : 𝜎ˆ ′ means 𝑂, 𝜎,
                                                                                        ˆ C ⇓Γ 𝑜 : 𝑂, 𝜎ˆ ′ .
                                                                       ′
   We use the following notation: given a (countable) set 𝑆, (𝑠, 𝑂 ) ∈ 𝑂 (𝑆) denotes an angelic choice
𝑠 ∈ 𝑆 by oracle 𝑂 with resulting shifted oracle 𝑂 ′ = 𝜆𝑛. 𝑂 (𝑛 + 1).

C.1      Additional Symbolic Satisfaction Relations
The symbolic store satisfaction relation is as follows:
                                      𝜃, 𝑠 |=Sto 𝑠ˆ ⇔ ∀x ∈ dom(𝑠).
                                                               ˆ Jˆ𝑠 (x)K𝜃 = 𝑠 (x)
                                                   ® 1 ; Ê
Let P̂ be a multiset of symbolic predicates {𝑝 1 ( Ê    ®1             𝑛 ®𝑛 ®𝑛
                                                     in out ), . . . , 𝑝 ( Êin ; Êout )}. Now, the symbolic
predicate satisfaction relation is as follows:
                                                                                                        ® 𝑖 ; Ê
           𝜃, 𝜇 |=Pred P̂ ⇔ ∃𝜇1, . . . , 𝜇𝑛 . 𝜇 = 𝜇1 · . . . · 𝜇𝑛 ∧ ∀𝑖 ∈ {1, . . . , 𝑛}. 𝜃, 𝜇𝑖 |= 𝑝 𝑖 ( Ê    ®𝑖
                                                                                                          in out )

C.2      Symbolic Expression Evaluation
We define the symbolic expression evaluation function. The role of this function is to return a
logical expression where all the program variables are evaluated with respect to the symbolic store.
Note that the symbolic expression evaluation function does not take in or produce a path condition
and does not branch – this obligation is, instead, handled by the symbolic semantics of commands,
as we will see further below. In the main text, symbolic expression evaluation was introduced
as evaluating program expressions. Because of the fold and unfold commands introduced below
(which have expressions that may contain logical variables), symbolic expression evaluation need to
take in logical expressions rather than only program expressions. For other commands that take in
standard expressions, these can be straightforwardly translated to logical expressions without issue.
   We give a few sample rules below, other rules are similarly straightforward:
                                                            JE1 K𝑠ˆ = Ê1    JE2 K𝑠ˆ = Ê2        JE1 K𝑠ˆ = Ê1   JE2 K𝑠ˆ = Ê2
    J𝑣K𝑠ˆ = 𝑣       JxK𝑠ˆ = 𝑠ˆ(x)          JxK𝑠ˆ = x
                                                              JE1 + E2 K𝑠ˆ = Ê1 + Ê2               JE1 / E2 K𝑠ˆ = Ê1 /Ê2

C.3      Core Commands
The rules for the core commands, that is, commands that are not memory-action commands or
based on consume and produce, are as follows:
                             Assign                                               Assign-Err-Eval
                                  JEK𝑠ˆ = Ê    𝑠ˆ′ = 𝑠ˆ [x ↦→ Ê]                JEK𝑠ˆ = Ê     𝑠ˆ′ = 𝑠ˆ [err ↦→ “ExprEval”]
Skip                                   ′                                                       ′
                                     𝜋ˆ = (𝑠ˆ(x) ∈ Val ∧ 𝜋)  ˆ                               𝜋ˆ = ( Ê ∉ Val ∧ 𝜋) ˆ
                                                           ′
ˆ skip ⇓𝑚
𝜎,      Γ ok : 𝜎ˆ            (𝑠,       ˆ x := E ⇓𝑚
                                 ˆ P̂, 𝜋),
                              ˆ 𝜇,                            ˆ P̂, 𝜋ˆ ′ )
                                                 Γ ok : (𝑠ˆ , 𝜇,                   (𝑠,      ˆ x := E ⇓𝑚
                                                                                       ˆ P̂ 𝜋),
                                                                                    ˆ 𝜇,                         ′
                                                                                                                    ˆ P̂, 𝜋ˆ ′ )
                                                                                                      Γ err : (𝑠ˆ , 𝜇,

     If-Then                                                         If-Else
           JEK𝑠ˆ = Ê       𝜋ˆ ′ = ( Ê = true ∧ 𝜋)ˆ                       JEK𝑠ˆ = Ê        𝜋ˆ ′ = ( Ê = false ∧ 𝜋)ˆ
            𝑂, (𝑠, ˆ P̂, 𝜋ˆ ′ ), C1 ⇓𝑚
                 ˆ 𝜇,                         ′ ′
                                      Γ 𝑜 : 𝑂 , 𝜎ˆ                           𝑂, (𝑠, ˆ P̂, 𝜋ˆ ′ ), C2 ⇓𝑚
                                                                                 ˆ 𝜇,                           ′ ′
                                                                                                        Γ 𝑜 : 𝑂 , 𝜎ˆ
                                               ′ ′                                                            ′ ′
      𝑂, (𝑠,
          ˆ 𝜇,     ˆ if (E) C1 else C2 ⇓𝑚
             ˆ P̂, 𝜋),                  Γ 𝑜 : 𝑂 , 𝜎ˆ                 𝑂, (𝑠,       ˆ if (E) C1 else C2 ⇓𝑚
                                                                            ˆ P̂, 𝜋),
                                                                         ˆ 𝜇,                          Γ 𝑜 : 𝑂 , 𝜎ˆ

                                 If-Err-Eval
                                          JEK𝑠ˆ = Ê       𝜋ˆ ′ = ( Ê ∉ Val ∧ 𝜋)
                                                                               ˆ
                                                ′
                                              𝑠ˆ = 𝑠ˆ [err ↦→ “ExprEval”]
                                                                              ′
                                    (𝑠,       ˆ if (E) C1 else C2 ⇓𝑚
                                        ˆ P̂, 𝜋),
                                     ˆ 𝜇,                                        ˆ P̂, 𝜋ˆ ′ )
                                                                   Γ err : (𝑠ˆ , 𝜇,

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                              373:35

           If-Err-Type                                                                    Seq
               JEK𝑠ˆ = Ê           𝜋ˆ ′ = ( Ê ∉ Bool ∧ Ê ∈ Val ∧ 𝜋)
                                                                    ˆ                           ˆ C1 ⇓𝑚
                                                                                            𝑂, 𝜎,               ′ ′
                                                                                                       Γ ok : 𝑂 , 𝜎ˆ
                                  ′                                                          ′ ′        𝑚      ′′ ′′
                                𝑠ˆ = 𝑠ˆ [err ↦→ “Type”]                                    𝑂 , 𝜎ˆ , C2 ⇓Γ 𝑜 : 𝑂 , 𝜎ˆ
                                                     ′                                                         ′′ ′′
           (𝑠,       ˆ if (E) C1 else C2 ⇓𝑚
               ˆ P̂, 𝜋),
            ˆ 𝜇,                                        ˆ P̂, 𝜋ˆ ′ )
                                          Γ err : (𝑠ˆ , 𝜇,
                                                                                             ˆ C1 ; C2 ⇓𝑚
                                                                                          𝑂, 𝜎,         Γ 𝑜 : 𝑂 , 𝜎ˆ

                                                Seq-Err
                                                                ′ ′
                                                   ˆ C1 ⇓𝑚
                                                𝑂, 𝜎,    Γ 𝑜 : 𝑂 , 𝜎ˆ        𝑜 ≠ ok
                                                                         ′ ′
                                                       ˆ C1 ; C2 ⇓𝑚
                                                    𝑂, 𝜎,         Γ 𝑜 : 𝑂 , 𝜎ˆ


C.4     Memory-action Command
The rules for the memory-action command are as follows:
                                                                            Memory-Action-Err-Length
  Memory-Action                                                                  ® = Ê
                                                                                JEK       ®       ® ⇝ ok : ( 𝜇ˆ′, 𝜋ˆ ′, Ê
                                                                                              ˆ ( Ê)
                                                                                             𝜇.𝛼                        ® ′)
                    ®            ® ⇝ ok : ( 𝜇ˆ′, 𝜋ˆ ′, Ê
                                                        ® ′)                        𝑠ˆ
            ® = Ê
           JEK              ˆ ( Ê)
                            𝜇.𝛼                                                ® ′            ′′    ®  ® ′           ′
               𝑠ˆ                                                            | Ê | ≠ |®x | 𝜋ˆ = ( Ê, Ê ∈ Val ∧ 𝜋ˆ ∧ 𝜋)  ˆ
      ® ′ | = |®x |
    | Ê                               ® Ê
                      𝜋ˆ ′′ = (𝑠ˆ(®x), Ê, ® ′ ∈ Val ∧ 𝜋ˆ ′ ∧ 𝜋)
                                                              ˆ                   𝑠ˆ′ = 𝑠ˆ [err ↦→ “ActionArgsLength”]
   (𝑠, ˆ P̂, 𝜋),                              ® ′ ], 𝜇ˆ′, P̂, 𝜋ˆ ′′ )
                         ® ⇓𝑚 ok : (𝑠ˆ [®x ↦→ Ê
             ˆ x® := 𝛼 ( E)                                                  (𝑠,
                                                                              ˆ 𝜇,                 ® ⇓𝑚 ok : (𝑠ˆ′, 𝜇ˆ′, P̂, 𝜋ˆ ′′ )
                                                                                       ˆ x® := 𝛼 ( E)
                                                                                 ˆ P̂, 𝜋),
    ˆ 𝜇,                    Γ                                                                         Γ

        Memory-Action-Err
          ® = Ê
         JEK    ®         ® ⇝ 𝑜 : ( 𝜇ˆ′, 𝜋ˆ ′, Ê
                      ˆ ( Ê)
                     𝜇.𝛼                       ® ′)
            𝑠ˆ                                                           Memory-Action-Err-Eval
          𝑜 ≠ ok             ® ∈ Val ∧ 𝜋ˆ ′ ∧ 𝜋)
                   𝜋ˆ ′′ = ( Ê                                                                       ® ∉ Val ∧ 𝜋)
                                               ˆ                             ® = Ê
                                                                            JEK𝑠ˆ            𝜋ˆ ′ = ( Ê        ˆ
                                         ® ′]
                        𝑠ˆ′ = 𝑠ˆ [err ↦→ Ê                                       ′
                                                                                𝑠ˆ = 𝑠ˆ [err ↦→ “ExprEval”]
        (𝑠, ˆ P̂, 𝜋),
         ˆ 𝜇,                 ® ⇓𝑚 𝑜 : (𝑠ˆ′, 𝜇ˆ′, P̂, 𝜋ˆ ′′ )
                  ˆ x® := 𝛼 ( E)                                         (𝑠, ˆ P̂, 𝜋),
                                                                          ˆ 𝜇,                 ® ⇓𝑚 err : (𝑠ˆ′, 𝜇,
                                                                                   ˆ x® := 𝛼 ( E)               ˆ P̂, 𝜋ˆ ′ )
                                 Γ                                                                Γ
We formally state the OX/UX soundness of memory actions for IProp. 3:

 (OX)     If         𝜇.𝛼 (®𝑣 ) ⇝ 𝑜 : (𝜇 ′, 𝑣®′ ) and 𝜃, 𝜇 |=Mem 𝜇ˆ and JÊK    ® = 𝑣® and
                                                                                    𝜃
                                      ® ′ . 𝜇.𝛼
                     (∀𝑜, 𝜇ˆ′, 𝜋ˆ ′, Ê         ® ⇝ 𝑜 : ( 𝜇ˆ′, 𝜋ˆ ′, Ê
                                            ˆ ( Ê)                  ® ′ ) and J𝜋ˆ ′ K = true and JÊ
                                                                                                   ® ′K ≠               ⇒ 𝑜 ≠ abort)
                                                                                      𝜃                𝜃
          then                   ® ′, 𝜃 ′ . 𝜇.𝛼
                     ∃𝜇ˆ′, 𝜋ˆ ′, Ê             ® ⇝ 𝑜 : ( 𝜇ˆ′, 𝜋ˆ ′, Ê
                                            ˆ ( Ê)                  ® ′ ) and 𝜃 ′ |     =𝜃
                                                                                     lv( 𝜇ˆ )
                                                                        ® ′ K ′ = 𝑣®′
                      and J𝜋ˆ ′ K𝜃 ′ = true and 𝜃 ′, 𝜇 ′ |=Mem 𝜇ˆ′ and JÊ   𝜃

 (UX)     If         ˆ ( Ê)
                     𝜇.𝛼    ® ⇝ 𝑜 : ( 𝜇ˆ′, 𝜋ˆ ′, Ê
                                                 ® ′ ) and 𝑜 ≠ abort and JÊK ® = 𝑣® and
                                                                                𝜃
                     J𝜋ˆ ′ K = true and 𝜃, 𝜇 ′ |=                   ® ′ K = 𝑣®′
                                                           𝜇ˆ′ and JÊ
                            𝜃                           Mem                 𝜃
          then                                  𝑣 ) ⇝ 𝑜 : (𝜇 ′, 𝑣®′ )
                     ∃𝜇. 𝜃, 𝜇 |=Mem 𝜇ˆ and 𝜇.𝛼 (®

C.5     Consume and Produce Operations Soundness Properties
Below, we give the soundness properties for the consume and produce operations. We assume
pv(𝐴) = ∅ for all cases. We also formally state the OX/UX soundness of consumeRes and produceRes
for IProp. 4.


OX soundness of consume:
 If   𝑚 ∈ {𝑂𝑋, 𝐸𝑋 } and
       (∀𝑜, 𝑂 ′, 𝜃ˆ′, 𝜎ˆ 𝑓 . consume(𝑚, 𝑂, 𝐴, 𝜃,  ˆ ⇝ (𝑜, 𝑂 ′, 𝜃ˆ′, 𝜎ˆ 𝑓 ) and SAT(𝜎ˆ 𝑓 ) ⇒ 𝑜 ≠ 𝑎𝑏𝑜𝑟𝑡) and
                                               ˆ 𝜎)
      𝜃, 𝑠, 𝜇 |= 𝜎ˆ
 then ∃𝜇𝐴 , 𝜇 𝑓 , 𝑂 ′, 𝜃ˆ′, 𝜎ˆ 𝑓 . consume(𝑚, 𝑂, 𝐴, 𝜃, ˆ ⇝ (ok, 𝑂 ′, 𝜃ˆ′, 𝜎ˆ 𝑓 ) and 𝜇 = 𝜇𝐴 · 𝜇 𝑓 and
                                                     ˆ 𝜎)
             𝜃, 𝑠, 𝜇𝐴 |= 𝜃ˆ′ (𝐴) and 𝜃, 𝑠, 𝜇 𝑓 |= 𝜎ˆ 𝑓

                                Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:36                                     A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


UX soundness of consume:
 If    consume(𝑚, 𝑂, 𝐴, 𝜃,      ˆ ⇝ (𝑜𝑘, 𝑂 ′, 𝜃ˆ′, 𝜎ˆ 𝑓 ) and
                              ˆ 𝜎)
       𝜃, 𝑠, 𝜇𝐴 |= 𝜃ˆ′ (𝐴) and 𝜃, 𝑠, 𝜇 𝑓 |= 𝜎ˆ 𝑓 and (𝜇𝐴 · 𝜇 𝑓 ) is defined
 then 𝜃, 𝑠, (𝜇𝐴 · 𝜇 𝑓 ) |= 𝜎ˆ
OX soundness of produce:
 If   lv(𝐴) ⊆ dom(𝜃ˆ) and 𝜃, 𝑠, 𝜇𝐴 |= 𝜃ˆ(𝐴) and 𝜃, 𝑠, 𝜇 𝑓 |= 𝜎ˆ 𝑓 and (𝜇𝐴 · 𝜇 𝑓 ) is defined
 then ∃𝜃 ′, 𝜎.
            ˆ 𝜃 ′ | lv(𝜎ˆ 𝑓 ) = 𝜃 and produce(𝐴, 𝜃,
                                                 ˆ 𝜎ˆ 𝑓 ) ⇝ 𝜎ˆ and 𝜃 ′, 𝑠, (𝜇𝐴 · 𝜇 𝑓 ) |= 𝜎ˆ

UX soundness of produce:
 If       produce(𝐴, 𝜃,  ˆ 𝜎ˆ 𝑓 ) ⇝ 𝜎ˆ and 𝜃, 𝑠, 𝜇 |= 𝜎ˆ
 then     ∃𝜇𝐴 , 𝜇 𝑓 . 𝜇 = 𝜇𝐴 · 𝜇 𝑓 and 𝜃, 𝑠, 𝜇𝐴 |= 𝜃ˆ(𝐴) and 𝜃, 𝑠, 𝜇 𝑓 |= 𝜎ˆ 𝑓
OX soundness of consumeRes operation:
  If       𝑚 ∈ {𝑂𝑋, 𝐸𝑋 } and
                     ® , 𝜇ˆ , 𝜋ˆ , 𝜋ˆ . consume
           (∀𝑜, 𝑂 ′, Ê                                             ® ˆ ⇝ (𝑜, 𝑂 ′, Ê
                                                                                   ® , ( 𝜇ˆ , 𝜋ˆ , 𝜋ˆ )) and
                       out   𝑓   fi    𝑓              Res (𝑚, 𝑂, 𝑟, Êin, 𝜇)          out  𝑓    fi 𝑓
              (J𝜋ˆfi K𝜃 = true ⇒ (∃𝜇 𝑓 . J𝜋ˆ 𝑓 K𝜃 = true and 𝜃, 𝜇 𝑓 |=Mem 𝜇ˆ 𝑓 )) ⇒ 𝑜 ≠ 𝑎𝑏𝑜𝑟𝑡) and
           𝜃, 𝜇 |=               ® K = 𝑣®
                         𝜇ˆ and JÊ
                   Mem                in 𝜃      in
  then
             ′ ®                                                       ® ˆ ⇝ (𝑜𝑘, 𝑂 ′, Ê       ® , ( 𝜇ˆ , 𝜋ˆ , 𝜋ˆ )) and
        © ∃𝑂 , Êout, 𝑣®out, 𝜇ˆ 𝑓 , 𝜋ˆfi , 𝜋ˆ 𝑓 . consumeRes (𝑚, 𝑂, 𝑟, Êin, 𝜇)                  out    𝑓    fi 𝑓         ª
        ­
        ­      (J𝜋ˆfi K𝜃 = true ⇒                                                                                         ®
                                                                                                                          ®
        ­
        ­                         ®
                  ∃𝜇𝑟 , 𝜇 𝑓 . JÊout K𝜃 = 𝑣®out and 𝜇𝑟 |=Res 𝑟 (®    𝑣 in ; 𝑣®out ) and 𝜃, 𝜇 𝑓 |=Mem 𝜇ˆ 𝑓 and
                                                                                                                          ®
                                                                                                                          ®
        «              𝜇 =   𝜇 𝑟  ·  𝜇 𝑓   and     J𝜋ˆ 𝑓 𝜃
                                                        K  = true)                                                        ¬
UX soundness of consumeRes operation:

          consumeRes (𝑚, 𝑂, 𝑟, Ê® , 𝜇)              ′ ®                                   ®                   ®
 If                                in ˆ ⇝ (𝑜𝑘, 𝑂 , Êout, ( 𝜇ˆ 𝑓 , 𝜋ˆfi , 𝜋ˆ 𝑓 )) and JÊin K𝜃 = 𝑣®in and JÊout K𝜃 = 𝑣®out
          and J𝜋ˆ 𝑓 K𝜃 = true and 𝜃, 𝜇 𝑓 |=Mem 𝜇ˆ 𝑓 and 𝜇𝑟 |=Res 𝑟 (®      𝑣 in ; 𝑣®out ) and (𝜇𝑟 · 𝜇 𝑓 ) is defined
 then     J𝜋ˆfi K𝜃 = true and 𝜃, (𝜇𝑟 · 𝜇 𝑓 ) |=Mem 𝜇ˆ
OX soundness of produceRes operation:

 If                                ® K = 𝑣® and JÊ
           𝜃, 𝜇 𝑓 |=Mem 𝜇ˆ 𝑓 and JÊ                   ® K = 𝑣® and 𝜇 |= 𝑟 (®         𝑣 in ; 𝑣®out )
                                     in 𝜃     in         out 𝜃   out        𝑟     Res
           and (𝜇𝑟 · 𝜇 𝑓 ) is defined
           ∃𝜇,                     ® , Ê
             ˆ 𝜋ˆ . produceRes (𝑟, Ê   ®
 then                                 in out, 𝜇ˆ 𝑓 ) ⇝ ( 𝜇, ˆ and 𝜃, (𝜇𝑟 · 𝜇 𝑓 ) |=Mem 𝜇ˆ and J𝜋K
                                                         ˆ 𝜋)                                        ˆ 𝜃 = true
UX soundness of produceRes operation:

           produceRes (𝑟, Ê ® , Ê
                                  ®                               ® K = 𝑣® and JÊ ® K = 𝑣® and
 If                           in out, 𝜇ˆ 𝑓 ) ⇝ ( 𝜇, ˆ and JÊ
                                                 ˆ 𝜋)              in 𝜃     in       out 𝜃 out
            ˆ 𝜃 = true and 𝜃, 𝜇 |=Mem 𝜇ˆ
           J𝜋K
 then      ∃𝜇𝑟 , 𝜇 𝑓 . 𝜇 = 𝜇𝑟 · 𝜇 𝑓 and 𝜇𝑟 |=Res 𝑟 (®
                                                    𝑣 in ; 𝑣®out ) and 𝜃, 𝜇 𝑓 |=Mem 𝜇ˆ 𝑓

C.6      Function-call Command
We implement the standard function-call rule for the consume-produce engine architecture; e.g., see
Jacobs et al. [22, Def. 4.8] for VeriFast, Schwerhoff [51, Fig. 3.6] for Viper, and Lööw et al. [31, Sec. 5]
                                                      ® to execute, the function-call rule angelically picks
for Gillian. In short, given a function call y := 𝑓 ( E)
a function specification  from Γ(𝑓
                                   ) compatible with the current execution mode 𝑚, to exemplify, say,
  x® = 𝑥® ★ 𝑃 𝑓 (®x) 𝑜𝑘 : 𝑄 ok 𝑒𝑟𝑟 : 𝑄 err ∈ Γ(𝑓 ), and first consumes the precondition x® = 𝑥® ★ 𝑃
                    


Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                                    373:37


and then produces the postconditions 𝑄 ok and 𝑄 err . The OX/UX soundness of the rule follows from
the OX/UX soundness of consume and produce (Lem. 5.1).
  We now give the successful rule for function calls, specialised to only produce 𝑄 ok to simplify
the presentation (the full rule produces both 𝑄 ok and 𝑄 err ). We use the following notation: given
some function identifier 𝑓 and a function specification context Γ, Γ(𝑓 )|𝑚 returns a set of function
specifications for the function identifier 𝑓 compatible with mode 𝑚 (e.g., ESL specifications are
compatible with both OX and UX mode). The uninteresting parts of the rule, which simply involves
updates and setup, are greyed out:



  ( x® = 𝑥® ★ 𝑃 𝑓 (®x) 𝑜𝑘 : 𝑄 ok            𝑒𝑟𝑟 : 𝑄 err , 𝑂 ′ ) ∈ 𝑂 (Γ(𝑓 )|𝑚 )                          get function specification
    ® = Ê
  JEK        ® and 𝜃ˆ = [𝑥® ↦→ Ê]
                               ®                                                                   evaluate function parameters
       𝑠ˆ
           ®
  𝜋ˆ ′ = ( Ê ∈ Val ∧ 𝜋)
                       ˆ                                                                          successful evaluation in path condition
  consume(𝑚, 𝑂 ′, 𝑃, 𝜃,       ˆ (𝑠,
                                  ˆ 𝜇,ˆ P̂, 𝜋ˆ ′ )) ⇝ (ok, 𝑂 ′′, 𝜃ˆ′, (𝑠, ˆ 𝜇ˆ 𝑓 , P̂𝑓 , 𝜋ˆ ′′ ))                  consume precondition
  𝑟 and 𝑟ˆ fresh                                                                                          fresh variables for return value
     ′ = 𝑄 [𝑟 /ret] and 𝜃ˆ′′ = 𝜃ˆ′ [𝑟 ↦→ 𝑟ˆ]
  𝑄 ok                                                                                                                set up return value
             ok
  𝜋ˆ = (𝑟ˆ ∈ Val ∧ 𝜋ˆ ′′ )
     ′′′                                                                                                      include 𝑟ˆ in path condition
  produce(𝑄 ok   ′ , 𝜃ˆ′′ , (𝑠,
                             ˆ 𝜇ˆ 𝑓 , P̂𝑓 , 𝜋ˆ ′′′ )) ⇝ (𝑠,
                                                         ˆ 𝜇ˆ′, P̂ ′, 𝜋ˆ ′′′′ )                                    produce postcondition
  𝜋ˆ ′′′′′ = (𝑠ˆ(y) ∈ Val ∧ 𝜋ˆ )     ′′′′                                                                     include y in path condition
                              𝑂, (𝑠, ˆ P̂, 𝜋),
                                  ˆ 𝜇,                ® ⇓𝑚 ok : 𝑂 ′′, (𝑠ˆ [y ↦→ 𝑟ˆ], 𝜇ˆ′, P̂ ′, 𝜋ˆ ′′′′′ )
                                           ˆ y := 𝑓 ( E) Γ


C.7    Fold and Unfold Commands
We implement the standard consume-produce rules for folding and unfolding user-defined predi-
cates; e.g., see Jacobs et al. [22, Def. 4.8] for VeriFast, Schwerhoff [51, Fig. 3.6] for Viper, and Lööw
et al. [31, App. B in extended paper] for Gillian.
   Folding and unfolding commands are expressed in the following extended syntax:


                                                                   ® | unfold 𝑝 ( E)
                                            C ::= · · · | fold 𝑝 ( E)             ®


             ®
where E® ∈ LExp.
  In the concrete semantics, fold and unfold are no-ops. Formally, that is:


                                     ® ⇓𝛾 ok : 𝜎
                         𝜎, fold 𝑝 ( E)                                                     ® ⇓𝛾 ok : 𝜎
                                                                              𝜎, unfold 𝑝 ( E)


   The symbolic semantics of the commands Ô          is defined using consume and produce. In short, given
a predicate definition 𝑝 (𝑥®in ; 𝑥®out ) { 𝑖 𝐴𝑖 }, the folding rule angelically picks a disjunct 𝐴𝑖 , consumes
the disjunct, and produces a symbolic predicate for the predicate, whereas the unfolding rule
angelically picks a symbolic predicate, consumes the symbolic predicate, and produces all of the
disjuncts 𝐴𝑖 of the predicate.
   We now give the formal symbolic rules. The notion 𝜎.consPure(𝑚,  ˆ              E) ⇝ 𝜎ˆ ′ is consume for
Boolean assertions (also known as pure assertions). For the rules here, the role of consPure (in OX
mode) is to check whether the path condition of 𝜎ˆ implies the given Boolean assertion and does not
change the state. If the implication does not hold, consPure will not return. Now, let 𝜎ˆ = (𝑠,         ˆ P̂, 𝜋):
                                                                                                      ˆ 𝜇,    ˆ

                               Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:38                                         A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner

                                                                                                  Ô
                               Ô
           𝑝 (𝑥®in ; 𝑥®out ) { 𝑖 𝐴𝑖 } ∈ Preds                                  𝑝 (𝑥®in ; 𝑥®out ) { 𝑖 𝐴𝑖 } ∈ Preds
                       ®                   ® ∈ Val ∧ 𝜋)                         ® = Ê
                                                                               JEK         ®                 ® ∈ Val ∧ 𝜋)
                                                                                                   𝜋ˆ ′ = ( Ê
             ® = Ê
           JEK                   𝜋ˆ ′ = ( Ê              ˆ                         𝑠ˆ
                                                                                                                       ˆ
                 𝑠ˆ
                     ′          Ô
           (𝐴𝑖 , 𝑂 ) ∈ 𝑂 ( 𝑖 𝐴𝑖 )                                              P̂ ≠ ∅                 ®    ®       ′
                                                                                                 (𝑝 ( Ê ; Ê ), 𝑂 ) ∈ 𝑂 ( P̂)
                                                                                                     in    out
           𝜃ˆ = [𝑥®in ↦→ Ê]  ®                                                                        ® ) ⇝ 𝜎ˆ
                                                                                                   ® = Ê
                                                                               ˆ
                                                                               𝜎.consPure(OX,      Ê    𝑖𝑛
           consume(OX, 𝑂 ′, 𝐴𝑖 , 𝜃,          ˆ (𝑠,ˆ 𝜇,ˆ P̂, 𝜋ˆ ′ )) ⇝          P̂ ′ = P̂ \ {𝑝 ( Ê  ® )}
                                                                                                ® ; Ê
                                                                                                   in     out
                         ′′  ˆ′
               (ok, 𝑂 , 𝜃 , (𝑠,         ′    ′     ′′
                                    ˆ 𝜇ˆ , P̂ , 𝜋ˆ ))
                                                                               𝜃ˆ = [𝑥®in ↦→ Ê® , 𝑥® ↦→ Ê      ® ]
                           ®
           P̂ = {𝑝 ( Ê; 𝜃 (𝑥® ))} ∪ P̂ ′
              ′′               ˆ′
                                                                                                  𝑖𝑛 out           out
                                   out                                         produce(𝐴𝑖 , 𝜃,    ˆ (𝑠,  ˆ P̂ ′, 𝜋ˆ ′ )) ⇝
                                                                                                       ˆ 𝜇,
           𝜋ˆ ′′′ = (𝜃ˆ′ (𝑥®out ) ∈ Val ∧ 𝜋ˆ ′′ )                                  ˆ 𝜇ˆ′, P̂ ′′, 𝜋ˆ ′′ )
                                                                                  (𝑠,
                       ® ⇓OX ok : 𝑂 ′′, (𝑠,
            ˆ fold 𝑝 ( E)                ˆ 𝜇ˆ′, P̂ ′′, 𝜋ˆ ′′′ )                           ® ⇓OX ok : 𝑂 ′, (𝑠,
         𝑂, 𝜎,            Γ                                                  ˆ unfold 𝑝 ( E)
                                                                          𝑂, 𝜎,              Γ             ˆ 𝜇ˆ′, P̂ ′′, 𝜋ˆ ′′ )
  The OX soundness of the rules follows from the OX soundness of consume and produce (Lem. 5.1).

C.8 Function-Specification Verification Procedure
We have formalised the standard OX function verification procedure from the consume-produce
literature on top of our CSE engine, which we here call verifyOX; e.g., see Jacobs et al. [22, Def. 4.7]
for VeriFast, Schwerhoff [51, Fig. 3.19] for Viper, and Lööw et al. [31, App. G in extended paper]
for Gillian. In short,
                     given a specification
                                             context Γ, a function 𝑓 (®x) { C; return E }, and an SL
specification 𝑡 𝑓 = x® = 𝑥® ★ 𝑃 𝑓 (®x) 𝑜𝑘 : 𝑄 ok , if verifyOX(Γ, 𝑓 , 𝑡 𝑓 ) terminates successfully, then
Γ can soundly be extend to Γ [𝑓 ↦→ Γ(𝑓 ) ∪ {𝑡 𝑓 }]. The procedure verifyOX succeeds if it can produce
the precondition x® = 𝑥® ★ 𝑃, symbolically execute the function body C (and return expression E),
and consume the postcondition 𝑄 ok . We make one simplification orthogonal to the main topic of
the paper, i.e., memory-model parametricity: we do not extend the specification context Γ with
the new specification 𝑡 𝑓 before verification, meaning that for now our verification procedure only
handles non-recursive functions. The soundness of verifyOX follows from the OX soundness of
our CSE engine (Thm. 5.2) and consume and produce (Lem. 5.1).




Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                                         373:39


D     Details of Memory-Model Instances
This section contains additional definitions, information, and rules of the various memory models
we discuss in the main text. To minimise clutter, we omit oracles and 𝜋ˆ𝑖 in the rules of resource
                                                                          ® , 𝜇)
consume if the oracle is not used and 𝜋ˆ𝑖 = true, i.e., consumeRes (𝑚, 𝑟, Ê           ®          ′ ˆ
                                                                            in ˆ ⇝ (𝑜, Êout, ( 𝜇ˆ , 𝜋))
                            ®
means consume (𝑚, 𝑂, 𝑟, Ê , 𝜇)             ®
                               ˆ ⇝ (𝑜, 𝑂, Ê , ( 𝜇ˆ′, true, 𝜋)).
                                                            ˆ
                        Res                    in                    out

D.1      Linear Memory Model (Running Example)
Our running example linear memory model, for simplicity, use simplified new and free actions
without arguments, i.e., we allocate and deallocate only one cell at a time. See, e.g., the block-offset
memory model for C in §6 for a memory model which can allocate and deallocate multiple cells at
a time.
D.1.1      Concrete Semantics.
                     Lookup                                                     Lookup-Err-Type
                                         𝜇 (𝑛) = 𝑣                                                𝑣 ∉ Nat
                     𝜇.lookup( [𝑛] ) ⇝ ok : (𝜇, [𝑣 ] )                            𝜇.lookup( [𝑣 ] ) ⇝ err : (𝜇, [“Type”] )

        Lookup-Err-Missing                                                        Lookup-Err-Use-After-Free
                                𝑛 ∉ dom(𝜇 )                                                              𝜇 (𝑛) = ∅
        𝜇.lookup( [𝑛] ) ⇝ miss : (𝜇, [“MissingCell”, 𝑛] )                         𝜇.lookup( [𝑛] ) ⇝ err : (𝜇, [“UseAfterFree”, 𝑛] )

               Mutate                                                              Mutate-Err-Type
                                        𝜇 (𝑛) ∈ Val                                                    𝑣 ∉ Nat
               𝜇.mutate( [𝑛, 𝑣 ] ) ⇝ ok : (𝜇 [𝑛 ↦→ 𝑣 ], [ ] )                       𝜇.mutate( [𝑣, 𝑣 ′ ] ) ⇝ err : (𝜇, [“Type”] )

      Mutate-Err-Missing                                                        Mutate-Err-Use-After-Free
                               𝑛 ∉ dom(𝜇 )                                                                𝜇 (𝑛) = ∅
      𝜇.mutate( [𝑛, 𝑣 ] ) ⇝ miss : (𝜇, [“MissingCell”, 𝑛] )                       𝜇.mutate( [𝑛, 𝑣 ] ) ⇝ err : (𝜇, [“UseAfterFree”, 𝑛] )

                 New                                                                 Free
                                        𝑛 ∉ dom(𝜇 )                                                 𝜇 (𝑛) ∈ Val
                  𝜇.new( [ ] ) ⇝ ok : (𝜇 [𝑛 ↦→ null], [𝑛] )                          𝜇.free( [𝑛] ) ⇝ ok : (𝜇 [𝑛 ↦→ ∅], [ ] )

               Free-Err-Type                                                Free-Err-Missing
                                   𝑣 ∉ Nat                                                      𝑛 ∉ dom(𝜇 )
                𝜇.free( [𝑣 ] ) ⇝ err : (𝜇, [“Type”] )                       𝜇.free( [𝑛] ) ⇝ miss : (𝜇, [“MissingCell”, 𝑛] )

                                                    Free-Err-Use-After-Free
                                                                      𝜇 (𝑛) = ∅
                                                    𝜇.free( [𝑛] ) ⇝ err : (𝜇, [“UseAfterFree”, 𝑛] )


D.1.2      Symbolic Semantics.
                 Lookup                                                        Lookup-Err-Type
                     𝜇ˆ ( Ê𝑙′ ) = Ê       𝜋ˆ ′ = ( Ê𝑙 = Ê𝑙′ )                             𝜋ˆ ′ = ( Ê𝑙 ∉ Nat)
                 ˆ
                 𝜇.lookup(                    ˆ 𝜋ˆ ′ , [ Ê] )
                           [ Ê𝑙 ] ) ⇝ ok : ( 𝜇,                               ˆ
                                                                               𝜇.lookup(                     ˆ 𝜋ˆ ′ , [“Type”] )
                                                                                         [ Ê𝑙 ] ) ⇝ err : ( 𝜇,

    Lookup-Err-Missing                                                         Lookup-Err-Use-After-Free
                𝜋ˆ ′ = ( Ê𝑙 ∈ Nat ∧ Ê𝑙 ∉ dom( 𝜇ˆ ) )                                       𝜇ˆ ( Ê𝑙′ ) = ∅     𝜋ˆ ′ = ( Ê𝑙 = Ê𝑙′ )
    ˆ
    𝜇.lookup(                      ˆ 𝜋ˆ ′ , [“MissingCell”, Ê𝑙 ] )
              [ Ê𝑙 ] ) ⇝ miss : ( 𝜇,                                           ˆ
                                                                                𝜇.lookup(                     ˆ 𝜋ˆ ′ , [“UseAfterFree”, Ê𝑙 ] )
                                                                                          [ Ê𝑙 ] ) ⇝ err : ( 𝜇,

                                    Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:40                                                A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner

              Mutate
                  𝜇ˆ ( Ê𝑙′ ) = Êold       𝜇ˆ ′ = 𝜇ˆ [ Ê𝑙′ ↦→ Ê]                    Mutate-Err-Type
                        𝜋ˆ ′ = ( Ê𝑙 = Ê𝑙′ ∧ Êold ∈ Val)                                                  𝜋ˆ ′ = ( Ê𝑙 ∉ Nat)
                                                         ′    ′
               ˆ
               𝜇.mutate( [ Ê𝑙 , Ê] ) ⇝ ok : ( 𝜇ˆ , 𝜋ˆ , [ ] )                        ˆ
                                                                                       𝜇.mutate(                         ˆ 𝜋ˆ ′ , [“Type”] )
                                                                                                 [ Ê𝑙 , Ê] ) ⇝ err : ( 𝜇,

Mutate-Err-Missing                                                                     Mutate-Err-Use-After-Free
               𝜋ˆ ′ = ( Ê𝑙 ∈ Nat ∧ Ê𝑙 ∉ dom( 𝜇ˆ ) )                                                      𝜇ˆ ( Ê𝑙′ ) = ∅      𝜋ˆ ′ = ( Ê𝑙 = Ê𝑙′ )
                                               ′
 ˆ
 𝜇.mutate( [ Ê𝑙 , Ê] ) ⇝ miss : ( 𝜇,
                                    ˆ 𝜋ˆ , [“MissingCell”, Ê𝑙 ] )                       ˆ
                                                                                         𝜇.mutate(                         ˆ 𝜋ˆ ′ , [“UseAfterFree”, Ê𝑙 ] )
                                                                                                   [ Ê𝑙 , Ê] ) ⇝ err : ( 𝜇,

                                                                                                   Free
                New                                                                                 𝜇ˆ ( Ê𝑙′ ) = Êold       𝜇ˆ ′ = 𝜇ˆ [ Ê𝑙′ ↦→ ∅]
                            Ê𝑙 fresh          𝜋ˆ ′ = ( Ê𝑙 ∈ Val)                                        𝜋ˆ ′ = ( Ê𝑙 = Ê𝑙′ ∧ Êold ∈ Val)
                 ˆ
                 𝜇.new( [ ] ) ⇝ ok : ( 𝜇ˆ [ Ê𝑙 ↦→ null], 𝜋ˆ ′ , [ Ê𝑙 ] )                          ˆ
                                                                                                    𝜇.free( [ Ê𝑙 ] ) ⇝ ok : ( 𝜇ˆ ′ , 𝜋ˆ ′ , [ ] )

          Free-Err-Type                                                           Free-Err-Missing
                          𝜋ˆ ′ = ( Ê𝑙 ∉ Nat)                                                   𝜋ˆ ′ = ( Ê𝑙 ∈ Nat ∧ Ê𝑙 ∉ dom( 𝜇ˆ ) )
           ˆ
           𝜇.free(                     ˆ 𝜋ˆ ′ , [“Type”] )
                   [ Ê𝑙 ] ) ⇝ err : ( 𝜇,                                         ˆ
                                                                                  𝜇.free(                      ˆ 𝜋ˆ ′ , [“MissingCell”, Ê𝑙 ] )
                                                                                          [ Ê𝑙 ] ) ⇝ miss : ( 𝜇,

                                               Free-Err-Use-After-Free
                                                              𝜇ˆ ( Ê𝑙′ ) = ∅      𝜋ˆ ′ = ( Ê𝑙 = Ê𝑙′ )
                                               ˆ
                                               𝜇.free(                     ˆ 𝜋ˆ ′ , [“UseAfterFree”, Ê𝑙 ] )
                                                       [ Ê𝑙 ] ) ⇝ err : ( 𝜇,

D.1.3 Resources, Consume, and Produce. Recall, there are two types resources: ↦→ (E𝑖𝑛 ; E𝑜𝑢𝑡 ) and
↦→∅(E𝑖𝑛 ; ); pretty-printed as, respectively, E𝑖𝑛 ↦→ E𝑜𝑢𝑡 and E𝑖𝑛 ↦→ ∅. The former states that the
 location denoted by E𝑖𝑛 points to a certain value denoted by E𝑜𝑢𝑡 . The latter states that the location
 denoted by E𝑖𝑛 has been freed.
    The full implementation of consumeRes is as follows:
                      𝜇ˆ = 𝜇ˆ 𝑓 ⊎ { Ê1 ↦→ Ê2 }                                                                 𝜇ˆ = 𝜇ˆ ′ ⊎ { Ê1 ↦→ ∅}
 consumeRes (𝑚, ↦→, [ Ê], 𝜇ˆ ) ⇝ (𝑜𝑘, [ Ê2 ], ( 𝜇ˆ 𝑓 , Ê = Ê1 ) )                 consumeRes (𝑚, ↦→∅, [ Ê], 𝜇ˆ ) ⇝ (𝑜𝑘, [ Ê2 ], ( 𝜇ˆ 𝑓 , Ê = Ê1 ) )

                              𝜇ˆ ( Ê1 ) = ∅                                                                           𝜇ˆ ( Ê1 ) = Ê2
  consumeRes (𝑚, ↦→, [ Ê], 𝜇ˆ ) ⇝ (abort, [ ], ( 𝜇,
                                                  ˆ Ê = Ê1 ) )                       consumeRes (𝑚, ↦→∅, [ Ê], 𝜇ˆ ) ⇝ (abort, [ ], ( 𝜇,
                                                                                                                                        ˆ Ê = Ê1 ) )


                              consumeRes (𝑚, 𝑟, [ Ê], 𝜇ˆ ) ⇝ (abort, [“MissingCell”, Ê], ( 𝜇,
                                                                                             ˆ Ê ∉ dom( 𝜇ˆ ) ) )

                                                                                  ® ≠1
                                                                                | Ê|
                                                                     ® 𝜇ˆ ) ⇝ (abort, [ ], ( 𝜇,
                                                   consumeRes (𝑚, 𝑟, Ê,                     ˆ true) )

   The full implementation of produceRes is as follows:
                             𝜇ˆ ′ = 𝜇ˆ ⊎ { Ê1 ↦→ Ê2 }                                                     𝜇ˆ ′ = 𝜇ˆ ⊎ { Ê1 ↦→ ∅}
                                                                  ′
             produceRes (↦→, [ Ê1 ], [ Ê2 ], 𝜇ˆ ) ⇝ ( 𝜇ˆ , true)                          produceRes (↦→∅, [ Ê1 ], [ ], 𝜇ˆ ) ⇝ ( 𝜇ˆ ′ , true)


D.2      Block-offset Memory Model for C
D.2.1 Well-formedness and Composition. We use the following definition in both the definition of
well-formedness and composition:
                                         def
 Wf size
    B ((𝜇𝑏 , Some(𝑛))) = (∀𝑖 ∈ dom(𝜇𝑏 ), 𝑖 < 𝑛)
                                         def
      Wf size
         B ((𝜇𝑏 , None)) = always


Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                                  373:41


Well-formedness is defined as follows:

                                   def
               Wf B ((𝜇𝑏 , 𝑛)) = Wf size
                                    B ((𝜇𝑏 , 𝑛)) ∧ (𝜇𝑏 ≠ ∅ ∨ 𝑛 ≠ None)
                                   def
                        Wf (𝜇) = ∀𝑛𝑏 , 𝜇 (𝑛𝑏 ) ≠ ∅ ⇒ Wf B (𝜇 (𝑛𝑏 ))

To define composition, we define disjoint union of two option values as follows:

                                   𝑣 1 when 𝑣 2 = None
                                   
                                   
                                   def 
                                       
                        𝑣 1 ⊎ 𝑣 2 = 𝑣 2 when 𝑣 1 = None
                                   
                                   
                                    undefined otherwise
                                   

Now, composition is defined as follows (note that 𝑛 1 and 𝑛 2 are swapped in the condition):
                                         (
                                   def       (𝜇𝑏1 ⊎ 𝜇𝑏2, 𝑛 1 ⊎ 𝑛 2 ) when Wf size                 size
                                                                             B ((𝜇𝑏1, 𝑛 2 )) ∧ Wf B ((𝜇𝑏2, 𝑛 1 ))
         (𝜇𝑏1, 𝑛 1 ) · (𝜇𝑏2, 𝑛 2 ) =
                                             undefined otherwise
                                         
                                         
                                          𝜇1 (𝑛𝑏 ) when 𝑛𝑏 ∉ dom(𝜇2 )
                                         
                                   def    𝜇 (𝑛 ) when 𝑛 ∉ dom(𝜇 )
                                         
                                             2   𝑏               𝑏             1
                 (𝜇1 · 𝜇2 ) (𝑛𝑏 ) =
                                         
                                         
                                          𝜇1 (𝑛𝑏 ) · 𝜇2 (𝑛𝑏 ) when 𝜇1 (𝑛𝑏 ) ≠ ∅ ∧ 𝜇2 (𝑛𝑏 ) ≠ ∅
                                         
                                          undefined otherwise
                                         
D.2.2     Concrete Semantics. We give the semantics of actions lookup, new, and free.

                Lookup                                                      Lookup-Err-Type-Block
                  𝜇 (𝑛𝑏 ) = (𝜇𝑏 , _)         𝜇𝑏 (𝑛𝑜 ) = 𝑣                                      𝑣𝑏 ∉ Nat
                𝜇.lookup( [𝑛𝑏 , 𝑛𝑜 ] ) ⇝ ok : (𝜇, [𝑣 ] )                    𝜇.lookup( [𝑣𝑏 , 𝑣𝑜 ] ) ⇝ err : (𝜇, [“Type”] )


     Lookup-Err-Type-Offset                                           Lookup-Err-Missing-Block
                         𝑣𝑜 ∉ Nat                                                             𝑛𝑏 ∉ dom(𝜇 )
        𝜇.lookup( [𝑛𝑏 , 𝑣𝑜 ] ) ⇝ err : (𝜇, [“Type”] )                 𝜇.lookup( [𝑛𝑏 , 𝑛𝑜 ] ) ⇝ miss : (𝜇, [“MissingBlock”, 𝑛𝑏 ] )


Lookup-Err-Use-After-Free                                                Lookup-Err-Missing-Offset-No-Size
                         𝜇 (𝑛𝑏 ) = ∅                                                 𝜇 (𝑛𝑏 ) = (𝜇𝑏 , None)       𝑛𝑜 ∉ dom(𝜇𝑏 )
𝜇.lookup( [𝑛𝑏 , 𝑛𝑜 ] ) ⇝ err : (𝜇, [“UseAfterFree”, 𝑛𝑏 ] )               𝜇.lookup( [𝑛𝑏 , 𝑛𝑜 ] ) ⇝ miss : (𝜇, [“MissingCell”, 𝑛𝑏 , 𝑛𝑜 ] )


Lookup-Err-Missing-Offset-Size                                           Lookup-Err-Offset-Size
          𝜇 (𝑛𝑏 ) = (𝑏, Some(𝑛) )         𝑛𝑜 ∉ dom(𝑏 )                              𝜇 (𝑛𝑏 ) = (𝜇𝑏 , Some(𝑛) )      𝑛𝑜 ∉ dom(𝜇𝑏 )
                           𝑛𝑜 < 𝑛                                                                      𝑛𝑜 ≮ 𝑛
𝜇.lookup( [𝑛𝑏 , 𝑛𝑜 ] ) ⇝ miss : (𝜇, [“MissingCell”, 𝑛𝑏 , 𝑛𝑜 ] )          𝜇.lookup( [𝑛𝑏 , 𝑛𝑜 ] ) ⇝ err : (𝜇, [“OutOfBounds”, 𝑛𝑏 , 𝑛𝑜 ] )


    New                                                                                         New-Err-Type
    𝑛𝑏 ∉ dom(𝜇 )          𝜇𝑏 = ( {0 ↦→ null, . . . , 𝑛 − 1 ↦→ null}, Some(𝑛) )                                  𝑣 ∉ Nat
                     𝜇.new( [𝑛] ) ⇝ ok : (𝜇 [𝑛𝑏 ↦→ 𝜇𝑏 ], [𝑛𝑏 ] )                                𝜇.new( [𝑣 ] ) ⇝ err : (𝜇, [“Type”] )


                 Free                                                               Free-Err-Type
                   𝜇 (𝑛𝑏 ) = (𝜇𝑏 , Some(n) )          |𝜇𝑏 | = 𝑛                                   𝑣 ∉ Nat
                  𝜇.free( [𝑛𝑏 ] ) ⇝ ok : (𝜇 [𝑛𝑏 ↦→ ∅], [ ] )                        𝜇.free( [𝑣 ] ) ⇝ err : (𝜇, [“Type”] )


                              Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:42                                                        A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner

      Free-Err-Miss-Block                                                                          Free-Err-Use-After-Free
                                        𝑛𝑏 ∉ dom(𝜇 )                                                                         𝜇 (𝑛𝑏 ) = ∅
         𝜇.free( [𝑛𝑏 ] ) ⇝ miss : (𝜇, [“MissingBlock”, 𝑛𝑏 ] )                                       𝜇.free( [𝑛𝑏 ] ) ⇝ err : (𝜇, [“UseAfterFree”, 𝑛𝑏 ] )

     Free-Err-Miss-Size                                                                            Free-Err-Miss-Offset
                               𝜇 (𝑛𝑏 ) = (𝜇𝑏 , None)                                                       𝜇 (𝑛𝑏 ) = (𝜇𝑏 , Some(𝑛) )               |𝜇𝑏 | ≠ 𝑛
     𝜇.free( [𝑛𝑏 ] ) ⇝ miss : (𝜇, [“MissingBound”, 𝑛𝑏 ] )                                          𝜇.free( [𝑛𝑏 ] ) ⇝ miss : (𝜇, [“MissingCells”, 𝑛𝑏 ] )

D.2.3 Symbolic Semantics. We give the successful rules for lookup, new, and free. Note that the
input to new must be a constant; for nonconstant input the action must return an abort outcome be-
cause dynamically sized allocations cannot be represented using the underlying memory data type.
                                            Lookup
                                             𝜇ˆ ( Ê𝑏′ ) = ( 𝜇ˆ𝑏′ , _)       𝜇ˆ𝑏′ ( Ê𝑜′ ) = Ê    𝜋ˆ ′ = ( Ê𝑏 = Ê𝑏′ ∧ Ê𝑜 = Ê𝑜′ )
                                                               ˆ
                                                               𝜇.lookup(                          ˆ 𝜋ˆ ′ , [ Ê] )
                                                                         [ Ê𝑏 , Ê𝑜 ] ) ⇝ ok : ( 𝜇,

                           New
                           Ê𝑏 fresh             𝜇ˆ𝑏 = ( {0 ↦→ null, . . . , 𝑛 − 1 ↦→ null}, Some(𝑛) )                        𝜋ˆ ′ = ( Ê𝑏 ∈ Val)
                                                                                                               ′
                                                            ˆ
                                                            𝜇.new( [𝑛] ) ⇝ ok : ( 𝜇ˆ [ Ê𝑏 ↦→ 𝜇ˆ𝑏 ], 𝜋ˆ , [ Ê𝑏 ] )

                                        Free
                                        𝜇ˆ ( Ê𝑏′ ) = ( 𝜇ˆ𝑏′ , Some( Ê𝑛 ) )          𝜋ˆ ′ = ( Ê𝑏 = Ê𝑏′ ∧ | 𝜇ˆ𝑏′ | = Ê𝑛 ∧ 𝜇ˆ𝑏′ ∈ Val) )
                                                             ˆ
                                                             𝜇.free( [ Ê𝑏 ] ) ⇝ ok : ( 𝜇ˆ [ Ê𝑏′ ↦→ ∅], 𝜋ˆ ′ , [ ] )

D.2.4 Resources, Consume, and Produce. The block-offset memory model comprises three resource
assertions and are as follows:
    • The memory-cell resource assertion (𝑛𝑏 , 𝑛𝑜 ) ↦→ 𝑣 states that the memory value 𝑣 is stored in
      offset 𝑛𝑜 of block 𝑛𝑏
    • The bounds resource assertion Bound(𝑛𝑏 ; 𝑛) states that nothing is defined beyond offset 𝑛 of
      block 𝑛𝑏
    • The freed resource assertion 𝑛𝑏 ↦→ ∅ states that the block 𝑛𝑏 was freed
  The satisfaction relation for resource assertions is defined below:
                                        𝜇 |=Res (𝑛𝑏 , 𝑛𝑜 ) ↦→ 𝑣 ⇔ 𝜇 = {𝑛𝑏 ↦→ ({𝑛𝑜 ↦→ 𝑣 }, None)}
                                        𝜇 |=Res Bound(𝑛𝑏 ; 𝑛) ⇔ 𝜇 = {𝑛𝑏 ↦→ (∅, Some(𝑛))}
                                        𝜇 |=Res 𝑛𝑏 ↦→ ∅         ⇔ 𝜇 = {𝑛𝑏 ↦→ ∅}
  Below, we show all of the successful cases for consumeRes and produceRes :
                          𝜇ˆ ( Ê𝑏′ ) = ( { Ê𝑜′ ↦→ Ê𝑣 }, None)
                                    𝜇ˆ ′ = 𝜇ˆ | dom( 𝜇)
                                                     ˆ −{Ê ′ }                                                                 Ê𝑏 ∉ dom( 𝜇ˆ )
                                                              𝑏
               𝜋ˆ ′ = ( Ê𝑏 = Ê𝑏′ ∧ Ê𝑜 = Ê𝑜′ ∧ Ê𝑏′ ∉ dom( 𝜇ˆ ′ ) )                                         𝜇ˆ ′ = 𝜇ˆ [ Ê𝑏 ↦→ ( { Ê𝑜 ↦→ Ê𝑣 }, None) ]
     consumeRes (𝑚, ↦→, [ Ê𝑏 , Ê𝑜 ], 𝜇ˆ ) ⇝ (𝑜𝑘, [ Ê𝑣 ], ( 𝜇ˆ ′ , 𝜋ˆ ′ ) )                          produceRes (↦→, [ Ê𝑏 , Ê𝑜 ], [ Ê𝑣 ], 𝜇ˆ ) ⇝ ( 𝜇ˆ ′ , true)

         𝜇ˆ ( Ê𝑏′ ) = ( 𝜇ˆ𝑏′ , Ê𝑛 )         ¬( | 𝜇ˆ𝑏′ | = 1 ∧ Ê𝑛 = None)                             𝜇ˆ ( Ê𝑏′ ) = ( 𝜇ˆ𝑏′ , Ê𝑛 )       ( 𝜇ˆ𝑏′ ≠ ∅ ∨ Ê𝑛 ≠ None)
                  𝜇ˆ𝑏′ ( Ê𝑜′ ) = Ê𝑣        𝜇ˆ𝑏′′ = 𝜇ˆ𝑏′ | dom( 𝜇ˆ ′ ) −{Ê′ }                               Ê𝑜 ∉ dom( 𝜇ˆ𝑏 )   ′
                                                                                                                                           𝜇ˆ𝑏′′ = 𝜇ˆ𝑏′ [ Ê𝑜 ↦→ Ê𝑣 ]
                                                                   𝑏     𝑜
   𝜇ˆ ′ = 𝜇ˆ [ Ê𝑏′ ↦→ ( 𝜇ˆ𝑏′′ , Ê𝑛 ) ]          𝜋ˆ ′ = ( Ê𝑏 = Ê𝑏′ ∧ Ê𝑜 = Ê𝑜′ )                                     𝜇ˆ ′ = 𝜇ˆ [ Ê𝑏′ ↦→ ( 𝜇ˆ𝑏′′ , Ê𝑛 ) ]
   consumeRes (𝑚, ↦→, [ Ê𝑏 , Ê𝑜 ], 𝜇ˆ ) ⇝ (𝑜𝑘, [ Ê𝑣 ], ( 𝜇ˆ ′ , 𝜋ˆ ′ ) )                         produceRes (↦→, [ Ê𝑏 , Ê𝑜 ], [ Ê𝑣 ], 𝜇ˆ ) ⇝ ( 𝜇ˆ ′ , Ê𝑏 = Ê𝑏′ )

                           𝜇ˆ ( Ê𝑏′ ) = ( ∅, Some( Ê𝑛 ) )
                   ′
                 𝜇ˆ = 𝜇ˆ | dom( 𝜇)  ˆ −{Ê ′ }   𝜋ˆ ′ = ( Ê𝑏 = Ê𝑏′ )                                Ê𝑏 ∉ dom( 𝜇ˆ )          𝜇ˆ ′ = 𝜇ˆ [ Ê𝑏 ↦→ ( ∅, Some( Ê𝑛 ) ) ]
                                             𝑏
                                                                                  ′    ′
    consumeRes (𝑚, Bound, [ Ê𝑏 ], 𝜇ˆ ) ⇝ (𝑜𝑘, [ Ê𝑛 ], ( 𝜇ˆ , 𝜋ˆ ) )                                  produceRes (Bound, [ Ê𝑏 ], [ Ê𝑛 ], 𝜇ˆ ) ⇝ ( 𝜇ˆ ′ , true)

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                                                373:43


               𝜇ˆ ( Ê𝑏′ ) = ( 𝜇ˆ𝑏′ , Some( Ê𝑛 ) )      𝜇ˆ𝑏′ ≠ ∅                            𝜇ˆ ( Ê𝑏′ ) = ( 𝜇ˆ𝑏′ , None)       𝜇ˆ𝑏′ ≠ ∅
        𝜇ˆ ′ = 𝜇ˆ [ Ê𝑏′ ↦→ ( 𝜇ˆ𝑏′ , None) ]        𝜋ˆ ′ = ( Ê𝑏 = Ê𝑏′ )                     𝜇ˆ ′ = 𝜇ˆ [ Ê𝑏′ ↦→ ( 𝜇ˆ𝑏′ , Some( Ê𝑛 ) ) ]
  consumeRes (𝑚, Bound, [ Ê𝑏 ], 𝜇ˆ ) ⇝ (𝑜𝑘, [ Ê𝑛 ], ( 𝜇ˆ ′ , 𝜋ˆ ′ ) )          produceRes (Bound, [ Ê𝑏 ], [ Ê𝑛 ], 𝜇ˆ ) ⇝ ( 𝜇ˆ ′ , Ê𝑏 = Ê𝑏′ )

   𝜇ˆ ( Ê𝑏′ ) = ∅      𝜇ˆ ′ = 𝜇ˆ | dom( 𝜇)
                                         ˆ −{Ê ′ }      𝜋ˆ ′ = ( Ê𝑏 = Ê𝑏′ )                  Ê𝑏 ∉ dom( 𝜇ˆ )           𝜇ˆ ′ = 𝜇ˆ [ Ê𝑏 ↦→ ∅]
                                               𝑏
                                                                   ′    ′
      consumeRes (𝑚, ↦→∅, [ Ê𝑏 ], 𝜇ˆ ) ⇝ (𝑜𝑘, [ ], ( 𝜇ˆ , 𝜋ˆ ) )                          produceRes (↦→∅, [ Ê𝑏 ], [ ], 𝜇ˆ ) ⇝ ( 𝜇ˆ ′ , true)


D.3     Memory Model for Object-oriented Languages
Here, we illustrate adding and deleting properties of objects in JavaScript. The following JavaScript
REPL session is from Node.js v23.10.0:
> var obj = {}
undefined
> obj.foo
undefined
> obj.foo = 5
5
> obj.bar = 1
1
> obj
{ foo: 5, bar: 1 }
> delete obj.foo
true
> obj.foo
undefined
> obj
{ bar: 1 }

D.4     CHERI-assembly Memory Model
D.4.1 Well-formedness Property. Given that the CHERI-assembly memory model is an extension of
the block-offset memory model, all well-formedness properties in the block-offset memory model
were ported to CHERI-assembly’s well-formedness property. The additional condition added was
that all capability fragments with a valid capability tag fragment are in an appropriately aligned
position, which is denoted below:
                                         def                                                                            def
Wf size                                                  size
   B-CH ((𝜇𝑏 , Some(𝑛))) = (∀𝑖 ∈ dom(𝜇𝑏 ), 𝑖 < 𝑛) and Wf B-CH ((𝜇𝑏 , None)) = always
                                         def
           Wf B-CH ((𝜇𝑏 , 𝑛)) = Wf size
                                   B-CH ((𝜇𝑏 , 𝑛)) ∧ (𝜇𝑛 ≠ ∅ ∨ 𝑛 ≠ None) ∧
                                                (∀(𝑜, 𝑐𝑛′ ) ∈ 𝜇𝑏 , (𝑐𝑛′ .𝑐𝑎𝑝.𝑡𝑎𝑔 = true ⇒ 𝑜 % |Cap| = 𝑛 ′ ) ∧ 𝑛 ′ < |Cap|)
                                         def
                           Wf (𝜇) = ∀𝑛𝑏 , 𝜇 (𝑛𝑏 ) ≠ ∅ ⇒ Wf B-CH (𝜇 (𝑛𝑏 ))


D.4.2 Concrete Semantics. We give the semantics of some of the memory-related actions. There are
14 actions. Four relates to accessing/mutating the memory (i.e. load, store, alloc, and free), and
ten relates to accessing/mutating the capability registers (i.e. get_addr, get_base, get_length,
get_offset, get_perms, get_tag, addr_set, tag_clear, perms_clear, and bounds_set). For
loading and storing, we have merged cases where one attempts to load a capability or a byte
value. There are 92 cases within the action semantics – many cases contribute to spatial checking,

                                   Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:44                                        A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


yielding an appropriate hardware exception as an error in cases where the check fails. For mutating
capability registers, the actions were designed such that bounds can only be restricted, permissions
can only be taken away, and the tag bit can only be cleared, which preserves the monotonic property.
We highlight some of the main successful memory-related cases below:
                                                                 Load
                                                                 fst(𝜇 ) (𝑟𝑠 ) = 𝑐𝑠        𝑐𝑠 .𝑡𝑎𝑔 = true         𝑐𝑠 .𝑝𝑒𝑟𝑚 load = true
         Free                                                               𝑐𝑠 .off + type_size(𝑏 ) ≤ 𝑐𝑠 .𝑏𝑎𝑠𝑒 + 𝑐𝑠 .𝑙𝑒𝑛
          fst(𝜇 ) (𝑟𝑠 ) = 𝑐𝑠       𝑐𝑠 .𝑡𝑎𝑔 = true                       𝑐𝑠 .off ≥ 𝑐𝑠 .𝑏𝑎𝑠𝑒         𝑐𝑠 .off % type_size(𝑏 ) = 0
                         𝑐𝑠 .off = 0                                             snd(𝜇 ) (𝑐𝑠 .𝑏𝑙𝑜 ) = (𝜇𝑏 , Some(𝑚) )
               𝑐𝑠 .off ≤ 𝑐𝑠 .𝑏𝑎𝑠𝑒 + 𝑐𝑠 .𝑙𝑒𝑛                                              𝑐𝑠 .off + |Cap| ≤ 𝑚
          snd(𝜇 ) (𝑐𝑠 .𝑏𝑙𝑜 ) = (𝜇𝑏 , Some(𝑚) )                        {𝑐𝑠 .off, ...𝑐𝑠 .off + type_size(𝑏 ) − 1} ⊆ dom(𝜇𝑏 )
                         |𝜇𝑏 | = 𝑚                                                  𝑐 𝑓 fresh w.r.t. dom(fst(𝜇 ) )
         𝜇 ′ = (fst(𝜇 ), snd(𝜇 ) [𝑐𝑠 .𝑏𝑙𝑜 ↦→ ∅] )                               load(𝑐𝑠 , 𝑏, 𝜇𝑏 , fst(𝜇 ), 𝑐 𝑓 ) = (𝜇𝑟′ , 𝑣)
            𝜇.free( [𝑟𝑠 ] ) ⇝ ok : (𝜇 ′ , [ ] )                          𝜇.load( [𝑟𝑠 , 𝑏 ] ) ⇝ ok : ( (𝜇𝑟′ , snd(𝜇 ) ), [𝑣 ] )

                                                                        Store-Cap
                                                                        fst(𝜇 ) (𝑟𝑠 ) = 𝑐𝑠         𝑐𝑠 .𝑡𝑎𝑔 = true        𝑐𝑠 .𝑝𝑒𝑟𝑚 store = true
 Store-NonCap                                                                   𝑟𝑑 is a capability register           fst(𝜇 ) (𝑟𝑑 ) = 𝑐𝑑
             fst(𝜇 ) (𝑟𝑠 ) = 𝑐𝑠       𝑐𝑠 .𝑡𝑎𝑔 = true                              (𝑐𝑠 .𝑝𝑒𝑟𝑚 storecap = true ∨ 𝑐𝑑 .𝑡𝑎𝑔 = false)
 𝑐𝑠 .𝑝𝑒𝑟𝑚 store = true          𝑣 is not a capability register                          𝑐𝑠 .off + |Cap| ≤ 𝑐𝑠 .𝑏𝑎𝑠𝑒 + 𝑐𝑠 .𝑙𝑒𝑛
          𝑐𝑠 .off + val_size(𝑣) ≤ 𝑐𝑠 .𝑏𝑎𝑠𝑒 + 𝑐𝑠 .𝑙𝑒𝑛                                𝑐𝑠 .off ≥ 𝑐𝑠 .𝑏𝑎𝑠𝑒         𝑐𝑠 .off % |Cap| = 0
      𝑐𝑠 .off ≥ 𝑐𝑠 .𝑏𝑎𝑠𝑒        𝑐𝑠 .off % val_size(𝑣) = 0                              snd(𝜇 ) (𝑐𝑠 .𝑏𝑙𝑜 ) = (𝜇𝑏 , Some(𝑚) )
             snd(𝜇 ) (𝑐𝑠 .𝑏𝑙𝑜 ) = (𝜇𝑏 , Some(𝑚) )                                                 𝑐𝑠 .off + |Cap| ≤ 𝑚
        𝑐𝑠 .off + |Cap| ≤ 𝑚          𝑐𝑠 .off ∈ dom(𝜇𝑏 )                           {𝑐𝑠 .off, ..., 𝑐𝑠 .off + |Cap| − 1} ⊆ dom(𝜇𝑏 )
                  store_value(𝑐𝑠 , 𝑣, 𝜇𝑏 ) = 𝜇𝑏′                                        store_capability(𝑐𝑠 , 𝑐𝑑 , 𝜇𝑏 ) = 𝜇𝑏′
  𝜇 ′ = (fst(𝜇 ), snd(𝜇 ) [𝑐𝑠 .𝑏𝑙𝑜 ↦→ (𝜇𝑏′ , Some(𝑚) ) ] )                  𝜇 = (fst(𝜇 ), snd(𝜇 ) [𝑐𝑠 .𝑏𝑙𝑜 ↦→ (𝜇𝑏′ , Some(𝑚) ) ] )
                                                                               ′

            𝜇.store( [𝑟𝑠 , 𝑣 ] ) ⇝ ok : (𝜇 ′ , [ ] )                                   𝜇.store( [𝑟𝑠 , 𝑟𝑑 ] ) ⇝ ok : (𝜇 ′ , [ ] )

  There are a number of auxiliary functions used in the concrete semantics:
    • type_size(𝑏) returns capsize, the size of a capability, if 𝑏 is true and 1 (i.e. the size of a byte)
      otherwise.
    • load(𝑐𝑠 , 𝑏, 𝜇𝑏 , fst(𝜇), 𝑐 𝑓 ) attempts to read, at location 𝑐𝑠 .off in memory 𝜇𝑏 , the value or capa-
      bility fragment byte and returns corresponding value or capability fragment byte if 𝑏 is false.
      If 𝑏 is true, then locations 𝑐𝑠 .off to 𝑐𝑠 .off + |Cap| − 1 is read, and if a valid capability is stored
      in a contiguous way, then the new value is saved to the fresh register 𝑐 𝑓 and the updated
      register map and the fresh register 𝑐 𝑓 are returned.
    • store_value(𝑐𝑠 , 𝑣, 𝜇𝑏 ) updates the memory 𝜇𝑏 at position 𝑐𝑠 .off with value 𝑣, where 𝑣 may
      either be a value or a capability fragment.
    • store_capability(𝑐𝑠 , 𝑐𝑑 , 𝜇𝑏 ) updates the memory 𝜇𝑏 at positions 𝑐𝑠 .off to 𝑐𝑠 .off +
      type_size(true) − 1 by splitting 𝑐𝑑 into capability fragments and storing them in a contiguous
      order. The tag fragment bits for each capability fragment is set to the value of 𝑐𝑑 .tag.
D.4.3    Symbolic Memory Model Structure. First, we define the symbolic memory below:


          SCap
                     def
                      =      {𝑏𝑙𝑜 : LExp; off : LExp; 𝑏𝑎𝑠𝑒 : LExp; 𝑙𝑒𝑛 : LExp; 𝑝𝑒𝑟𝑚      ® 𝑡𝑎𝑔 : LExp}
                                                                                 ® x : LExp;
                               where 𝑥 ∈ {load, store, loadcap, storecap}
                     def
      SCapfrag        =      {𝑐𝑎𝑝 : SCap; 𝑛𝑡ℎ : LExp}
                     def
  SMemB-CH            =      LExp ⇀fin (LExp + SCapfrag, LExp?)
                     def
  SMemSCReg           =      LExp ⇀fin SCap
                     def
         SMem         =      (SMemSCReg, SMemB-CH ⊎ {∅})

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
Compositional Symbolic Execution for the Next 700 Memory Models (Extended Version)                                                                           373:45


  The symbolic semantics are directly lifted from the concrete versions, much like the block offset
memory model. There are a total of 116 cases for the symbolic actions semantics – whereas the
concrete semantics merged the capability/non-capability cases for load, for simplicity, we wrote
separate cases in the symbolic semantics. Capabilities and capability fragments have been lifted to
symbolic capabilities and symbolic capability fragments, which are used in the memory.
D.4.4 Resources, Consume, and Produce. We define |=Res , the resource satisfaction relation for
CHERI-assembly:
          𝜇 |=Res Reg(𝑟𝑛 ; 𝑐)        ⇔ 𝜇 = ({𝑟𝑛 ↦→ 𝑐}, ∅)
                  (𝑛𝑏 , 𝑛𝑜 ) ↦→ 𝑣 ⇔ 𝜇 = (∅, {𝑛𝑏 ↦→ ({𝑛𝑜 ↦→ 𝑣 }, None)})         if 𝑣 ∈ Val
                  (𝑛𝑏 , 𝑛𝑜 ) ↦→cf 𝑐𝑛 ⇔ 𝜇 = (∅, {𝑛𝑏 ↦→ ({𝑛𝑜 ↦→ 𝑐𝑛 }, None)})
                                       ∧ (𝑐𝑛 .𝑐𝑎𝑝.𝑡𝑎𝑔 = true =⇒ 𝑛𝑜 % |Cap| = 𝑛)
                                       ∧ 𝑛 < |Cap|                              if 𝑐𝑛 ∈ Capfrag
                  Bound(𝑛𝑏 ; 𝑛) ⇔ 𝜇 = (∅, {𝑛𝑏 ↦→ (∅, Some(𝑛)})
                  𝑛𝑏 ↦→ ∅            ⇔ 𝜇 = (∅, {𝑛𝑏 ↦→ ∅})
   We require a new resource assertion for capability registers, given that the memory model now
comprises capability registers. As for the memory resource assertions, there are two cases, where
one of them is identical to that of the block-offset memory model. The other one is specifically
for capability fragments. Given 𝑐𝑛 ∈ Capfrag , 𝑛 indicates that the fragment is the 𝑛th byte of a
full capability 𝑐 ∈ Cap. When the tag fragment bit is true, which indicates that the particular
capability byte fragment has not been modified by an non-capability-aware store, we require that
𝑛𝑜 % |Cap| = 𝑛, given that 𝑛𝑜 is an offset in a block; this not only conforms with the CHERI-ISA
specification [52], but this also ensures each resource assertion forms a well-formed memory, and
composing resource assertions also results in a well-formed memory.
   The more interesting memory capability resource assertion can be defined as a predicate assertion,
i.e. Cap(𝑛𝑏 , 𝑛𝑜 ; 𝑐){𝐴body } ∈ Preds, pretty-printed as (𝑛𝑏 , 𝑛𝑜 ) ↦→cap 𝑐. Here, assume 𝑐 ∈ Cap and
𝑐𝑖 ∈ Capfrag where 𝑐𝑖 .𝑛𝑡ℎ = 𝑖, i.e. the 𝑖 𝑡ℎ byte of the capability 𝑐.
                                                               def         |Cap| −1
                                                    𝐴body = ⋆𝑖=0                      (𝑛𝑏 , 𝑛𝑜 + 𝑖) ↦→cf 𝑐𝑖
   Note that we do not require the assertion 𝑛𝑜 % |Cap| = 0, i.e., the offset starts in a capability-
aligned position (based on the CHERI-ISA specification [52]), since the resource satisfaction relation
implicitly implies each resource is in an aligned position.
   Below, we show some of the successful cases for consumeRes and produceRes :
                              fst( 𝜇ˆ ) ( Ê𝑟′ ) = 𝑐ˆ
𝜇ˆ ′ = (fst( 𝜇ˆ | dom(fst( 𝜇)
                           ˆ ) −{Ê ′ } ), snd( 𝜇ˆ ) )        𝜋ˆ ′ = ( Ê𝑟 = Ê𝑟′ )        Ê𝑟 ∉ dom(fst( 𝜇ˆ ) )         𝜇ˆ ′ = (fst( 𝜇ˆ ) [ Ê𝑟 ↦→ 𝑐ˆ ], snd( 𝜇ˆ ) )
                                    𝑟
                                                                       ′   ′
     consumeRes (𝑚, Reg, [ Ê𝑟 ], 𝜇ˆ ) ⇝ (𝑜𝑘, [𝑐ˆ ], ( 𝜇ˆ , 𝜋ˆ ) )                                produceRes (Reg, [ Ê𝑟 ], [𝑐ˆ ], 𝜇ˆ ) ⇝ ( 𝜇ˆ ′ , true)

                   snd( 𝜇ˆ ) ( Ê𝑏′ ) = ( { Ê𝑜′ ↦→ Ê𝑣 }, None)
               𝜇ˆ ′ = (fst( 𝜇ˆ ), snd( 𝜇ˆ ) | dom(snd( 𝜇)ˆ ) −{Ê ′ } )                                          Ê𝑏 ∉ dom(snd( 𝜇ˆ ) )
                                                                   𝑏
        𝜋ˆ ′ = ( Ê𝑏 = Ê𝑏′ ∧ Ê𝑜 = Ê𝑜′ ∧ Ê𝑏′ ∉ dom(snd( 𝜇ˆ ′ ) ) )                       𝜇ˆ ′ = (fst( 𝜇ˆ ), snd( 𝜇ˆ ) [ Ê𝑏 ↦→ ( { Ê𝑜 ↦→ Ê𝑣 }, None) ] )
    consumeRes (𝑚, ↦→, [ Ê𝑏 , Ê𝑜 ], 𝜇ˆ ) ⇝ (𝑜𝑘, [ Ê𝑣 ], ( 𝜇ˆ ′ , 𝜋ˆ ′ ) )                  produceRes (↦→, [ Ê𝑏 , Ê𝑜 ], [ Ê𝑣 ], 𝜇ˆ ) ⇝ ( 𝜇ˆ ′ , true)

                  snd( 𝜇ˆ ) ( Ê𝑏′ ) = ( { Ê𝑜′ ↦→ 𝑐ˆÊ𝑛 }, None)
               𝜇ˆ ′ = (fst( 𝜇ˆ ), snd( 𝜇ˆ ) | dom(snd( 𝜇) ˆ ) −{Ê ′ } )                                         Ê𝑏 ∉ dom(snd( 𝜇ˆ ) )
                                                                   𝑏
        𝜋ˆ ′ = ( Ê𝑏 = Ê𝑏′ ∧ Ê𝑜 = Ê𝑜′ ∧ Ê𝑏′ ∉ dom(snd( 𝜇ˆ ′ ) )                         𝜇ˆ ′ = (fst( 𝜇ˆ ), snd( 𝜇ˆ ) [ Ê𝑏 ↦→ ( { Ê𝑜 ↦→ 𝑐ˆÊ𝑛 }, None) ] )
               ∧ 𝑐ˆÊ𝑛 .𝑐𝑎𝑝.𝑡𝑎𝑔 ≠ true ∧ Ê𝑛 < |Cap| )                                                   𝜋ˆ = (𝑐ˆÊ𝑛 ≠ true ∧ Ê𝑛 < |Cap| )
  consumeRes (𝑚, ↦→cf , [ Ê𝑏 , Ê𝑜 ], 𝜇ˆ ) ⇝ (𝑜𝑘, [𝑐ˆÊ𝑛 ], ( 𝜇ˆ ′ , 𝜋ˆ ′ ) )                 produceRes (↦→cf , [ Ê𝑏 , Ê𝑜 ], [𝑐ˆÊ𝑛 ], 𝜇ˆ ) ⇝ ( 𝜇ˆ ′ , 𝜋ˆ )


                                        Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
373:46                                                     A. Lööw, S. H. Park, D. Nantes-Sobrinho, S.-É. Ayoun, O. Sjöstedt, and P. Gardner


                   snd( 𝜇ˆ ) ( Ê𝑏′ ) = ( { Ê𝑜′ ↦→ 𝑐ˆÊ𝑛 }, None)
                𝜇ˆ ′ = (fst( 𝜇ˆ ), snd( 𝜇ˆ ) | dom(snd( 𝜇) ˆ ) −{Ê ′ } )
                                                                    𝑏
         𝜋ˆ ′ = ( Ê𝑏 = Ê𝑏′ ∧ Ê𝑜 = Ê𝑜′ ∧ Ê𝑏′ ∉ dom(snd( 𝜇ˆ ′ ) )                                         Ê𝑏 ∉ dom(snd( 𝜇ˆ ) )
                 ∧ 𝑐ˆÊ𝑛 .𝑐𝑎𝑝.𝑡𝑎𝑔 = true ∧ Ê𝑛 < |Cap|                                  𝜇ˆ ′ = (fst( 𝜇ˆ ), snd( 𝜇ˆ ) [ Ê𝑏 ↦→ ( { Ê𝑜 ↦→ 𝑐ˆÊ𝑛 }, None) ] )
                 ∧ Ê𝑜 % |Cap| = Ê𝑛 )                                                   𝜋ˆ = (𝑐ˆÊ𝑛 ≠ true ∧ Ê𝑛 < |Cap| ∧ Ê𝑜 % |Cap| = Ê𝑛 )
  consumeRes (𝑚, ↦→cf , [ Ê𝑏 , Ê𝑜 ], 𝜇ˆ ) ⇝ (𝑜𝑘, [𝑐ˆÊ𝑛 ], ( 𝜇ˆ ′ , 𝜋ˆ ′ ) )            produceRes (↦→cf , [ Ê𝑏 , Ê𝑜 ], [𝑐ˆÊ𝑛 ], 𝜇ˆ ) ⇝ ( 𝜇ˆ ′ , 𝜋ˆ )

                       snd( 𝜇ˆ ) ( Ê𝑏′ ) = ( ∅, Some( Ê𝑛 ) )                                                  Ê𝑏 ∉ dom(snd( 𝜇ˆ ) )
   𝜇ˆ ′ = (fst( 𝜇ˆ ), snd( 𝜇ˆ ) | dom(snd( 𝜇)
                                            ˆ ) −{Ê ′ } )   𝜋ˆ ′ = ( Ê𝑏 = Ê𝑏′ )           𝜇ˆ ′ = (fst( 𝜇ˆ ), snd( 𝜇ˆ ) [ Ê𝑏 ↦→ ( ∅, Some( Ê𝑛 ) ) ] )
                                                       𝑏
     consumeRes (𝑚, Bound, [ Ê𝑏 ], 𝜇ˆ ) ⇝ (𝑜𝑘, [ Ê𝑛 ], ( 𝜇ˆ ′ , 𝜋ˆ ′ ) )                 produceRes (Bound, [ Ê𝑏 ], [ Ê𝑛 ], 𝜇ˆ ) ⇝ ( 𝜇ˆ ′ , true)

           snd( 𝜇ˆ ) ( Ê𝑏′ ) = ∅        𝜋ˆ ′ = ( Ê𝑏 = Ê𝑏′ )
         𝜇ˆ ′ = (fst( 𝜇ˆ ), snd( 𝜇ˆ ) | dom(snd( 𝜇)ˆ ) −{Ê ′ } )                    Ê𝑏 ∉ dom(snd( 𝜇ˆ ) )         𝜇ˆ ′ = (fst( 𝜇ˆ ), snd( 𝜇ˆ ) [ Ê𝑏 ↦→ ∅] )
                                                             𝑏
consumeRes (𝑚, ↦→∅, [ Ê𝑏 ], 𝜇ˆ ) ⇝ (𝑜𝑘, [ ], ( 𝜇ˆ ′ , 𝜋ˆ ′ ) )                             produceRes (↦→∅, [ Ê𝑏 ], [ ], 𝜇ˆ ) ⇝ ( 𝜇ˆ ′ , true)
   Note that for both consume and produce, we split the ↦→cf case based on the value of the tag
fragment bit of the capability fragment. Strictly speaking, the split is not necessary for the purpose
of proving OX soundness, but the split is required for proving UX soundness, which is not part of
the contribution of this paper. For future work, we plan on proving UX soundness with our existing
formalism.




Proc. ACM Program. Lang., Vol. 9, No. OOPSLA2, Article 373. Publication date: October 2025.
