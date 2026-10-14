                                         Systematic Design of Separation Logics
                                         ROBERTO BRUNI, Università di Pisa, Italy
                                         LORENZO GAZZELLA, Università di Pisa, Italy
                                         ROBERTA GORI, Università di Pisa, Italy
                                         Thanks to the locality principle, separation logics support modular, scalable analysis of large codebases
                                         by relying on local axioms and frame rules to focus only on the heap fragments required for verification.
                                         However, depending on the direction—forward vs. backward—and sense of approximation—over vs. under—of
arXiv:2605.21262v1 [cs.LO] 20 May 2026




                                         the analysis, designing the corresponding proof systems can require some ingenuity. In his work on the
                                         calculational design of program logics, Patrick Cousot outlines a methodology for deriving proof systems
                                         directly from program semantics using abstract interpretation, covering both correctness and incorrectness
                                         analyses. Unfortunately, when applied to heap-manipulating programs, Cousot’s calculational approach cannot
                                         handle the locality principle, because it does not provide a calculational way to derive frame rules and produces
                                         axioms that refer to the global heap. In this paper, we propose a general methodology for systematically deriving
                                         local axioms in which the locality principle is embedded by construction. For heap-manipulating primitives,
                                         we can derive the minimal required heap and the corresponding pre- and postconditions, complemented
                                         by universal frame rules without additional syntactic side conditions. Our method is parametric w.r.t. a set
                                         of semantic closure properties that are exploited to design local axioms; it can deal with different memory
                                         models; it favors the reuse of many inference rules across over- and under-approximation; and it produces
                                         logical systems capable of deriving a broader range of triples w.r.t. existing, cleverly designed, program logics
                                         for (in)correctness, ranging from Separation Logic (SL) and Incorrectness Separation Logic (ISL) to Separation
                                         Sufficient Incorrectness Logic (SepSIL). Furthermore, we demonstrate the flexibility of our methodology by
                                         applying it to design a novel proof system for inferring necessary preconditions with separation logic.

                                         CCS Concepts: • Theory of computation → Logic and verification; Separation logic; Hoare logic; Proof
                                         theory; Programming logic; Semantics and reasoning; Program analysis; Pre- and post-conditions.

                                         Additional Key Words and Phrases: Incorrectness Separation Logic, Separation Sufficient Incorrectness Logic,
                                         Necessary Condition, Sound-by-construction analysis, Frame rule, Locality principle


                                         1   Introduction
                                            Program analysis. In the development of increasingly complex and critical software systems,
                                         software verification plays a fundamental role in ensuring reliability, security, and correctness
                                         of program behavior. Since their conception, frameworks for program analysis, as envisaged by
                                         Turing [1950] and first formalized by Floyd [1967] and Hoare [1969] with Hoare Logic (HL), have
                                         focused on program correctness, that is, proving the absence of bugs. More recently, motivated by
                                         the goal of making formal methods effective in industrial settings, O’Hearn [2020] has introduced
                                         Incorrectness Logic (IL), which shifts the perspective to identifying the presence of bugs. Unlike
                                         correctness analyses, IL cannot raise false alarms, which can be an advantageous support for
                                         programmers. Whether the analysis is aimed at proving correctness or exposing incorrectness,
                                         some form of approximation of the exact program semantics is necessary, because Rice’s theorem
                                         [Rice 1953] establishes that any non-trivial program property is undecidable. Sound methods for
                                         proving correctness are based on over-approximation, which reports all true alarms, possibly mixed
                                         with false alarms. Vice versa, under-approximations are best suited for incorrectness techniques,
                                         which only raise true alarms, even if not necessarily all of them.

                                         Authors’ Contact Information: Roberto Bruni, Dipartimento di Informatica, Università di Pisa, Pisa, Italy, roberto.bruni@
                                         unipi.it; Lorenzo Gazzella, Dipartimento di Informatica, Università di Pisa, Pisa, Italy, lorenzo.gazzella@phd.unipi.it; Roberta
                                         Gori, Dipartimento di Informatica, Università di Pisa, Pisa, Italy, roberta.gori@unipi.it.
2                                                               Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


              forward                                          backward
    over      Partial correctness analysis: it shows ab- Necessary condition (NC) analysis: points
              sence of errors, but can report false alarms out some entry states that inevitably lead
              [Floyd 1967; Hoare 1969].                    to errors [Cousot et al. 2013].
    baseline Separation logic (SL) [O’Hearn et al. 2001]       Currently none available.
    under     Incorrectness analysis: shows some reach- Lisbon logic (a.k.a. SIL): exposes some en-
              able bugs, without false alarms [de Vries try states with at least an erroneous execu-
              and Koutavas 2011; O’Hearn 2020].         tion [Raad et al. 2024; Zhang and Kamin-
                                                        ski 2022; Zilberstein et al. 2023, 2024].
    baseline Incorrectness separation logics (ISL and          Separation SIL [Ascari et al. 2025].
             CISL) [Raad et al. 2020, 2022].
Table 1. Taxonomy of logics with reference frameworks for heap manipulating programs. Columns indicate
the direction, i.e., whether the validity conditions of triples is based on forward or backward semantics, while
rows indicate the sense of approximation, i.e., over- or under-approximation.

   Here, the notion of approximation refers to forward program analyses. Indeed, in Hoare triples
the postcondition over-approximates all final states reachable from states satisfying the precon-
dition. The same idea can also be defined over initial states, as in Cousot et al. [2013], yielding
backward program analyses. We will use the term direction to refer to the type of analysis (forward
or backward), and the term sense to indicate the kind of approximation (over or under). Each combi-
nation of sense and direction is best suited for achieving specific analysis goals, as summarized in
Table 1, triggering a new thread of research in program logics, with efforts to integrate them with
separation logic, concurrency, and abstract interpretation, as well as to combine correctness and
incorrectness reasoning within unifying frameworks [Ascari et al. 2025; Bruni et al. 2023; Carrott
et al. 2025; Le et al. 2022; Maksimovic et al. 2023; Möller et al. 2021; Raad et al. 2020, 2024; Verbeek
et al. 2025; Verscht and Kaminski 2025; Zilberstein et al. 2024]. Table 1 also shows the separation
logic instances that serve as reference models for comparing our proposals. Highly sophisticated
toolsets grounded in these theories are being developed in both academic and industrial settings,
spanning over a wide range of applications [Distefano et al. 2019; Jung et al. 2018; Le et al. 2022;
Vistrup et al. 2025].


   Cousot’s calculational design. As different logics address different goals, their proof systems are
often designed ad hoc, possibly re-using, extending or simply adapting inference rules already
available from the literature. To bring clarity in the program logic zoo and facilitate mutual
comparisons for expressiveness and applicability, Cousot [2024] promoted a semantic-driven
methodology, called calculational design. The methodology for deriving a proof system directly
from program semantics builds on well-established Abstract Interpretation techniques [Cousot
2021; Cousot and Cousot 1977], and enables the automatic design of sound and complete proof
systems through the abstraction associated with the analysis. Cousot’s method begins by specifying
the formal semantics of the language, followed by establishing the theory of the logic through
Galois connections that abstract suitable semantic properties. The proof system’s rules are then
automatically derived using fixpoint abstractions, principles of fixpoint induction, and Aczel’s
approach to constructing deductive rule-based systems from fixpoints [Aczel 1977]. Thanks to
calculational design, Cousot is able to position all assertional transformational logics within a
comprehensive taxonomy of abstractions [Cousot 2024, Figure 3], which is highly valuable for
Systematic Design of Separation Logics                                                                                      3


comparing analyses by varying their underlying Galois connections and for constructing sound
and complete proof systems through semantic calculation.
   Problem statement: local axiom design. To make program analysis scalable and effective for large,
frequently updated codebases, it is necessary to reuse previous analyses of code fragments, rather
than recomputing them each time. In the case of heap-manipulating programs, a successful approach
in this respect is provided by logics grounded in the locality principle [Distefano et al. 2019]: so-
called ‘local’ axioms allow the computation of local summaries for individual code fragments, which
can then be composed using suitable frame rules and bi-abductive techniques [Calcagno et al. 2009,
2011]. As advised by O’Hearn et al. [2001], to understand how a program works, it should be possible
for reasoning and specification to be confined to the cells that the program actually accesses. The value
of any other cell will automatically remain unchanged. The locality principle enables incremental
analysis to reason on larger portions of programs by focusing only on the parts of the code that
have changed, rather than requiring a full inspection of the entire program at every update. Local
axioms and frame rules are in fact the key ingredients of separation logics [Ascari et al. 2025;
Bornat et al. 2005; Calcagno et al. 2007; Maksimovic et al. 2023; O’Hearn et al. 2001; Raad et al. 2020;
Reynolds 2002]. Separation logics exploit basic ownership assertions such as x ↦→ v, stating that the
cell at address x stores the value v, and the separating conjunction ∗, which composes assertions
over disjoint portions of memory, e.g., the assertion x ↦→ v ∗ y ↦→ v implies that x and y refer to
different cells of the heap. While the program logics taxonomies proposed in [Ascari et al. 2025;
Cousot 2024; Verscht and Kaminski 2025] can serve as a compass to determine the right analysis
framework to use for a given goal, the design of their corresponding local axioms and frame rules
are not yet supported by Cousot’s calculational design. This limitation stems from the fact that
program semantics is defined to handle arbitrary inputs, and therefore must account for the entire
memory. Consequently, Cousot’s calculational method produces inference rules that inherently
refer to the entire memory state.
  Main contribution: Systematic design. The design, extension, and automation of separation logics
require a certain degree of ingenuity. In this paper, we propose a novel, well-disciplined method to
derive local axioms and frame rules directly from program semantics. We exploit semantic closure
properties to derive the minimal set of axioms from which all valid triples can be obtained. Unlike
Cousot’s calculational design, we do not aim to derive the entire proof system; instead, we focus
on the axioms for atomic commands. The inference rules for the remaining language constructs
can be borrowed from existing proposals, including Cousot’s own.1 To avoid confusion, we call our
method systematic design.
  To witness the full generality of our solution, we apply our methodology to a variety of program
analyses, addressing different memory models and comparing the new resulting proof systems
with the ones previously proposed in the literature. Simple examples show that our systematic
design improves the expressiveness of existing frameworks in the vast majority of cases.
  Having fixed the collecting semantics J·K and a set of analysis-preserving closure operators,
our approach is first formulated at the purely semantic level and then instantiated to reconstruct
assertional program logics based on (in)correctness separation logics formulas [O’Hearn et al. 2001;
Raad et al. 2020], so to exploit the usual separating conjunction operator ∗ for local reasoning.
The distinguishing features of our methodology are: 1) Principled locality: It guarantees the
derivation of sound and complete local axioms by construction. Matched with universal frame
rules, it enables modular reasoning about program behaviour. 2) Broad generality: It seamlessly
1 More explicitly, we do not address directly the issue of designing rules for sequential composition, conditionals, nondeter-

ministic choice, Kleene star loops, while loops, etc., for which existing solutions are fully reusable.
4                                                           Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


supports any combination of over- and under-approximation, as well as forward and backward
analyses. Moreover, it accommodates diverse memory management policies, including both reuse
and non-reuse of deallocated memory cells. 3) Reusable core rules: It identifies a common core
of inference rules that are agnostic to the sense of approximation, supporting their reuse across
multiple analyses. 4) Expressiveness: It yields proof systems that derive strictly more valid triples
w.r.t. existing analyses, as soundness and completeness are ensured by construction, rather than
by ad hoc and/or ingenious arguments. 5) Mechanization: To gain confidence in the proposed
methodology, we formalized a proof of concept of the procedure in Isabelle/HOL.

   Relevance of results. To clarify how our method advances the state of the art and to highlight the
advantages of a systematic design, we revisit several key issues that our approach addresses in a
principled way, largely independent of the sense and direction of analysis. In contrast, previous ad
hoc solutions left room for improvement. Although the literature contains different interpretations
of separating assertions (see, e.g., [Cao et al. 2017; Parkinson 2010]), we follow the line of research
in which they impose exact (rather than minimal) requirements on the heap. For example, emp
denotes the empty heap, and x ↦→ 1 ∗ y ↦→ 2 denotes a heap containing exactly two cells.

   Issue #1: Frame rule soundness across analyses. A key feature of separation logics is the reuse of
local code summaries, allowing the analysis to focus on individual program fragments indepen-
dently from the entire global state. To this end, separation logics deal with triples whose pre- and
postconditions are confined to the part of the memory accessed by the code. Idle memory portions
can be added on demand to scale the reasoning thanks to the frame rule. Frames are possibly
computed by the bi-abduction method [Calcagno et al. 2009, 2011] to extend and compose local
analyses of ‘adjacent’ code fragments that were carried out in isolation. As a result, separation
logics can scale to large codebases, even when the complete program is unavailable [Calcagno et al.
2015; Distefano et al. 2019]. Since the notion of soundness is dependent on the sense and direction
of the analysis, the same frame rule is not necessarily reusable across different analyses or memory
models, unless certain semantic properties are known to hold [Cao et al. 2017] or suitable side
conditions are added. For example, in Separation Logic (SL) [O’Hearn et al. 2001; Reynolds 2002]—a
forward over-approximation logic—the soundness requirement of a triple {P} r {Q} is JrKP ⊆ Q,
namely that the postcondition Q is satisfied by any final state reachable by executing the program
r on any initial state that satisfies the precondition P. The classical frame rule is written as follows:

                                   {P} r {Q} mod(r) ∩ fv(R) = ∅
                                                                                                          (1)
                                          {R ∗ P} r {R ∗ Q}
where mod(r) is the set of variables that appear in the left-hand side of some assignment in r
and fv(R) the set of free variables in R. The disjointness condition between fv(R) and mod(r)
guarantees that the memory described by R is untouched by r and thus the soundness condition
JrK(R ∗ P) ⊆ R ∗ Q is trivially satisfied whenever JrKP ⊆ Q, because JrK(R ∗ P) ⊆ R ∗ JrKP and
R ∗ JrKP ⊆ R ∗ Q follow from the properties of the collecting semantics J·K.
   For a triple [P] r [Q] in Incorrectness Separation Logic (ISL) [Raad et al. 2020]—a forward under-
approximation logic—the soundness requirement is JrKP ⊇ Q and the above reasoning cannot be
replicated, unless JrK(R ∗ P) = R ∗ JrKP. Unfortunately this fails in general: if frame R shares some
memory cell with P that is deallocated by r, it can happen that JrK(R ∗ P) = JrKfalse = false but
R ∗ JrKP ≠ false. Consequently, Raad et al. [2020] introduced a different memory model in which
deallocated cells are explicitly recorded along the computation, denoted with the assertion x ̸↦→.
This makes the heap grow monotonically. Under this model, R ∗ P ≠ false whenever R ∗ JrKP ≠ false,
and the classical frame rule (1) is sound, but their solution requires a different memory model.
Systematic Design of Separation Logics                                                                            5


   We note that several approaches for avoiding syntactic side conditions have already appeared in
the literature. All of them can be traced back to the core insight of [Bornat et al. 2005], although
they differ in the semantic assumptions they adopt and in the programming paradigms they target.
Bornat et al. [2005] treat program variables as resources: they introduce the predicate Own(x) to
denote stores that contain exactly the single variable x, and they use the separating conjunction to
compose such stores. In this setting, the frame rule can be detached from syntactic side conditions
by adding a semantic requirement that relates the pre- and postcondition; their development,
however, is restricted to forward correctness analyses. A closely related line is pursued in [Jung
et al. 2018; Vistrup et al. 2025], where the side condition is eliminated entirely, albeit 1) under an
affine logic —where ownership means "at least this resource", rather than "exactly this resource"— 2)
without an explicit account of mutable stores and 3) without addressing backward directed rules.
Finally, Raad et al. [2022] follow a similar principle for incorrectness analysis by modeling both
store and heap as a separation algebra, and by adopting explicit deallocation predicates as in [Raad
et al. 2020]. Together, these semantic assumptions suffice to remove side conditions altogether.
   Advancements on issue #1. We define a ‘universal’ characterization of frames based on the concept
of logical variables, a set of inherently immutable variables disjoint from the program ones. For
each direction of the analysis, we define a unique frame rule that is independent from the sense of
approximation and from the memory model. In contrast to other approaches, where side-condition-
free framing emerges from specific semantic properties, our method avoids syntactic side conditions
on the program without treating variables as resources, applies directly to settings with mutable
stores, and does not require heap monotonicity in order to support incorrectness analysis.
   Issue #2: Design of local axioms. Local axioms are concerned with the minimal amount of informa-
tion that is necessary to derive the behaviour of each atomic command. Defining local axioms that
are expressive enough to recover all possible valid triples can require some ingenuity. Moreover,
one has to keep in mind that they can be applied jointly with other rules, like the frame rule or the
consequence rules, that may depend themselves on the sense and direction of the analysis. In fact,
different ad hoc solutions are often chosen in the literature for different logics.
   For example, let us take the deallocation command free(x) that disposes the location pointed
to by the variable x in three different separation logics: the already mentioned SL and ISL, and
Separation Sufficient Incorrectness Logic (SepSIL) [Ascari et al. 2025]—a more recent backward
under-approximation logic for disclosing the sources of incorrectness, in the spirit of so-called
Lisbon triples and manifest error detection, also studied in [Raad et al. 2024; Zhang and Kaminski
2022; Zilberstein et al. 2024]. SepSIL triples are written ⟨⟨P⟩⟩ r ⟨⟨Q⟩⟩ and their soundness requirement
guarantees that any initial state that satisfies P has at least one execution leading to some state in
Q. When Q describes error states, it means that some error is reachable starting from any initial
state. The axioms proposed in the literature for the three different logics are the following.
                              (SL)                              (ISL)                                  (SepSIL)
 {x ↦→ _} free(x) {emp}              [x ↦→ v] free(x) [x ̸↦→]           ⟨⟨x ↦→ _⟩⟩ free(x) ⟨⟨x ̸↦→⟩⟩
    The axiom of SL asserts that the deallocation is possible whenever x was allocated, no matter
the stored value, and then the empty heap is returned because it applies to the memory model
without explicit reallocation. Thanks to the consequence rule of SL, it is possible to strengthen the
precondition and derive, e.g., {x ↦→ v} free(x) {emp} for any value v.
    The axiom of ISL requires a different memory model to guarantee the soundness of the frame
rule (as explained above), where the postcondition x ̸↦→ records the deallocation of x for future
reuse. Moreover, the consequence rule of ISL allows to weaken the precondition, not to strengthen
it, because the sense of approximation is reversed w.r.t. SL. Therefore the axiom must be given for
any value v, which can then be generalized to derive [x ↦→ _] free(x) [x ̸↦→].
6                                                                      Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


  Finally, the axiom of SepSIL has been given for the same memory model as ISL and designed by
taking into account the same consequence rule as SL.
  Given such ad hoc solutions, one may wonder whether certain analysis are possible only for
certain memory models. Furthermore, we miss a disciplined approach to select the right axioms
each time and this makes it complicated to deal with new primitives as well as new logics.
  Advancements on issue #2. Our methodology allows to systematically derive local axioms from the
semantics, independently from the sense and direction of the analysis and from the memory model.
This brings clarity and automation in the design of novel program logics, which we exemplify in
Section 6 by the systematic design of a proof system for backward over-approximation.
   Issue #3: Derivability and completeness. While the soundness of a proof system follows directly
from the soundness of each of its rules, completeness emerges only from the combined effect of all
the rules. Below, we show that even well-established program logics fail to derive triples whose
validity is straightforward. This is where a methodological approach based on closure operators
becomes valuable, as it supports reasoning about the proof system globally. The presence of a
syntactic side condition in the frame rule of SL may hinder its own application even in cases where
the command under analysis does not modify the heap. For example, the following triple can be
derived in SL, where the assertion emp means the heap is empty:
                                {emp} if (true) then skip else x := [y] {emp}.
However, despite the assignment x := [y] being dead code, due to the frame rule’s side condition
mod(r) ∩ fv(R) = ∅, we cannot extend this reasoning to fit the frame R = x ↦→ _. Hence, the
following valid SL triple cannot be derived within this proof system:
                             {x ↦→ _} if (true) then skip else x := [y] {x ↦→ _}.
   Notably, the same impossibility argument can be used as a counterexample to the completeness
of ISL. There, the problem is even more evident: under-approximation triples [P] r [Q] are allowed
to drop arbitrary path inspections from the analysis, meaning that variables modified in discarded
branches of r should not be taken into account. Roughly, mod(r) over-approximates the set of
modified variables. As a consequence, the side condition may become a source of incompleteness,
inhibiting the derivation of valid ISL triples. This can be substantiated by the valid ISL triple2
                           [y ↦→ v] x := alloc(); free(y); x := [y] [y ̸↦→ ∗ x ↦→ _]                                      (2)
whose precondition requires that y is pointing to the value v, while the postcondition states that y
has been deallocated and that x is pointing to some value. When handling the command x := [y]
after y has been deallocated, we end up with an error without any actual modification to the
variable x. Despite the fact that x is not actually modified, we cannot use the frame rule to frame
out the assertion on x due to the side condition mod(r) ∩ fv(R) = ∅, which prevents the frame from
mentioning the variable x, leading to the impossibility of applying the local axiom for x := [y].
   The next example shows that incompleteness does not stem solely from the frame rule. Concurrent
Incorrectness Separation Logic (CISLDC ) [Raad et al. 2022], the concurrent version of ISL for
detecting memory safety bugs, uses a different underlying memory model that enables a frame
rule in the style of (1) but without any side condition. Despite this, CISLDC local axioms may still
give rise to sources of incompleteness. To see this, let us focus on the axiom for allocation:

                                    [x ↦→ v1 ] x := alloc() [∃l.x ↦→ l ∗ l ↦→ v]

2 Adhering to [Raad et al. 2020] green assertions are for normal termination, red for erroneous one, and blue for both.
Systematic Design of Separation Logics                                                                    7


whose precondition assumes the variable x points to the value v1 , while the postcondition states
that x points to some location l, which in turn points to v. We note that since CISLDC is an under-
approximation logic, we would like to have the possibility of expressing the strongest possible
postcondition, which would carry a generic choice of value v. Unfortunately, the valid triple
                                [x ↦→ v1 ] x := alloc() [∃l.∃v.x ↦→ l ∗ l ↦→ v]
cannot be derived in CISLDC since we would need an infinite disjunction rule to collect every
possible value v or the ‘exists’ rule, but neither is present in the logic system.
  Advancements on issue #3. In contrast to approaches where these interactions are handled
implicitly at the semantic level (e.g., Iris-style or CISL-style systems), our approach systematically
identifies the necessary side conditions for applying frame rules in both forward and backward
analyses, thereby extending the range of derivable triples well beyond existing proposals. Moreover,
the derivability of all valid triples for any atomic command c is ensured by construction.
    Technical contribution. Our approach refines and extends the semantic methodology outlined
in the introduction by systematically incorporating three key parameters of program analysis:
direction (forward/backward analysis), sense (over-/under-approximation), and the enforcement of
the locality principle through semantic, rather than syntactic, conditions.
    From a methodological standpoint, we characterize the set of valid triples for a given atomic
command c by identifying semantic closure properties that are preserved under the intended analysis.
These include: (i) consequence closure (e.g., weakening postconditions in over-approximation),
(ii) frame closure (capturing heap locality), and (iii) existential closure (generalization over variables).
These closure properties play a crucial role in determining the simplest triples from which all others
can be derived using closure operators. Indeed, if a triple can be obtained through a closure operator,
including it explicitly in the set of axioms would be redundant. We show that some of these closures
commute and that each valid triple can, therefore, be derived via a short canonical sequence of
such closures in a given order, allowing axioms to be selected by minimality considerations. This
yields a systematic and unified proof system design that operates on pre- and postconditions that
are concrete sets of states. The translation from the semantic proof system to program logics is
then achieved by selecting appropriate assertion languages, building on separation logic constructs.
    Technically speaking, the ingredients that make systematically designed program logics more
expressive, modular, and effective than existing ones are immutable variables and semantic closures.
    Immutable variables are not a new concept; on the contrary, they have been widely employed in
many proposals before [Dardinier and Müller 2024; Floyd 1967; O’Hearn et al. 2001; Raad et al. 2020,
2024; Reynolds 2002], even if with different names (e.g., auxiliary, logical or shadow variables) and
not necessarily injected into the memory model at the semantic level, as we do here. They can be
used to freeze and retain the values of program variables across transitions, thereby characterizing
the class of admissible frames. Thanks to logical variables, we define frame compatibility directly
at the semantic level, thus avoiding syntactic side conditions that are a well-known source of
incompleteness. Their principled treatment allows us to distill universal frame rules.
    Closure operators are instrumental to obtain local axioms that are independent of the memory
model and the sense of approximation. This supports a uniform treatment across multiple program
logics, including both correctness and incorrectness oriented analyses.
    Overall, our methodology produces proof systems that are sound-by-construction. All synthesized
proof systems and their novelties are outlined in Table 2. Besides increasing the expressiveness
of existing logics, new logics can be designed with minimal effort. This has been done to address
                                           2    1            1
different memory models (see entries ⊢SL+ , ⊢ISL+ , and ⊢SIL+ ), but also for distilling the proof system
                                                                            1          2
for Necessary Conditions (NC) [Cousot et al. 2013] (see entries ⊢NC+ and ⊢NC+ ), to be used in
8                                                                 Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


                       sense   no memory reallocation (M1 )            memory reallocation (M2 )
                                1                                                    2
                SL+    over    ⊢SL+ is more expressive than SL         New logic: ⊢SL+
    forward




                               (see Th. 5.1 and Ex. 5.1)
                                           1                            2
                ISL+   under   New logic: ⊢ISL+                        ⊢ISL+ is more expressive than ISL
                                                                       (see Th. 5.2–5.3 and Ex. 5.2)
                                           1                                                               2
                SIL+   under   New logic: ⊢SIL+                        Unlike SepSIL, all axioms of ⊢SIL+
    backward




                                                                       are local
                                           1                                         2
                NC+    over    New logic: ⊢NC+                         New logic: ⊢NC+

Table 2. Systematically designed logics and their improvements w.r.t. existing ones. Logics are organized
according to the direction of the analysis, sense of approximation and underlying memory model. We write
 i
⊢L to denote the logic L under the memory model Mi . All original contributions are highlighted in light blue.

automatic precondition inference. As a further instance, not reported in Table 2, we apply our
methodology to the setting of CISLDC [Raad et al. 2022], where a different store model is required.

  Structure of the paper. After recalling some necessary background in Section 2, we introduce our
semantic framework and the methodology for systematic design in Sections 3–4. In Sections 5–6,
we apply our methodology to both forward and backward analyses, addressing under- and over-
approximations. While related work is thoroughly discussed throughout the paper, we conclude in
Section 7 with future work. Auxiliary material is in the Appendix for reviewers’ convenience.

2      Background
Following O’Hearn [2020], we consider a language of regular commands, parametric to suitable
atomic commands c, including heap-manipulating primitives, according to the grammar below:

                                         Reg ∋ r ::= c | r; r | r + r | r∗

   We write r; r for sequential composition, r + r for nondeterministic choice, and r∗ for the Kleene
iteration of r, where the command r can be executed any finite number of times, possibly zero.
Regular commands are a well-established framework [Fischer and Ladner 1979; Harel et al. 2000;
Pratt 1976] that serves as a general template, allowing for different instantiations depending on the
chosen set of atomic commands, to be detailed later (see (7)). Standard imperative constructs, like
conditionals and loops, can be coded following, e.g., [Winskel 1993].

2.1            Memory models
As briefly discussed in Section 1, SL [O’Hearn et al. 2001; Reynolds 2002] and ISL [Raad et al.
2020] consider two different memory models: the ISL memory model extends SL by allowing for
tracking of deallocated locations and their subsequent reallocation. To distinguish the two models,
throughout the paper we will use 1 to refer to the SL model and 2 to refer to the ISL model, using i
whenever we do not care whether it is the model 1 or 2. In particular, we define the set of stores
Sp as the set of total functions from program variables Xp to values V. The set of heaps H1 in the
memory model 1 is the set of partial functions from locations L ⊆ V to values V. Finally, the set of
memories M1 is the product domain between Sp and H1 . The model 2 extends the heap domain
H1 with a new special value ⊥, which tracks for deallocated locations, i.e., given an heap ℎ in 2 if
Systematic Design of Separation Logics                                                                             9


ℎ(𝑙) = ⊥, then the location 𝑙 was previously allocated and then deallocated. Formally,
            1:        Sp ≜ Xp → V                   H1 ≜ L ⇀ V                             M1 ≜ Sp × H1 ;
            2:        Sp ≜ Xp → V                   H2 ≜ L ⇀ (V ∪ {⊥})                     M2 ≜ Sp × H2 .
  We write ℎ𝑝 #ℎ𝑞 to indicate that ℎ𝑝 and ℎ𝑞 are heaps with disjoint domains (i.e. 𝑑𝑜𝑚(ℎ𝑝 ) ∩
𝑑𝑜𝑚(ℎ𝑞 ) = ∅), while ℎ𝑝 • ℎ𝑞 indicates the join of ℎ𝑝 and ℎ𝑞 and it is defined if and only if ℎ𝑝 #ℎ𝑞 .
With a slight abuse of notation, we lift the operator • to compose sets of memories, defined as:
                          𝑃 • 𝑄 ≜ {(𝑠, ℎ𝑝 • ℎ𝑞 ) | (𝑠, ℎ𝑝 ) ∈ 𝑃 ∧ (𝑠, ℎ𝑞 ) ∈ 𝑄 ∧ ℎ𝑝 #ℎ𝑞 }
Moreover, we find it convenient to define existential quantification over sets as follows:
                                    ∃X.𝑃 ≜ {(𝑠 ′, ℎ) | (𝑠, ℎ) ∈ 𝑃 ∧ 𝑠 ′|X\X = 𝑠 |X\X }.
where the function 𝑓 |𝑋 : 𝑋 → 𝐵 is the restriction of 𝑓 : 𝐴 → 𝐵 to the domain 𝑋 ⊆ 𝐴.

2.2    Assertion language
We rely on the assertion language of Raad et al. [2020], which extends the classical definition
[O’Hearn et al. 2001; Reynolds 2002] by introducing the negative heap assertion x ̸↦→. Since the
assertion x ̸↦→ is used to track deallocated locations, it will only be used in the memory model 2.
We let Ast be defined as follows, where ≍∈ {=, ≤, ...} represents standard comparison operators, X
is a set of variables and e, e1, e2 are arithmetic expressions:
      Ast ∋ P, Q ::= false | true | e1 ≍ e2 | P ∧ Q | P ∨ Q | ∃X.P | emp | x ↦→ e | x ̸↦→ | P ∗ Q                 (3)
   The standard operators from first-order logic, here in light gray, define the so-called pure as-
sertions. The remaining operators define the structural assertions. The assertion emp denotes the
empty heap, the ownership predicate x ↦→ e denotes memories in which the heap contains a single
location pointed by x and whose content is e, while x ̸↦→ stands for memories in which the heap
has a single location pointed by x, but that has been deallocated. The separating conjunction P ∗ Q
represents memories where the heap (not the store) can be split into two disjoint sub-heaps, one
satisfying P and the other satisfying Q. We let fv(P) be the set of free variables in P. The intuitive
meaning of structural assertions is summarized in Table 5. To simplify the exposition, and with a
slight abuse of notation, we introduce a single semantics for the assertion language. The reference
model will be evident from the context; for example, the semantics of true is either M1 or M2
depending on the memory model we are dealing with, and x ̸↦→ will be used only when the memory
model 2 is considered. Hence, the set of all and only memories satisfying the assertion P ∈ Ast is
denoted by ⦃P⦄ and defined as follows:
⦃false⦄ ≜ ∅           ⦃true⦄ ≜ Mi            ⦃e1 ≍ e2 ⦄ ≜ {(𝑠, ℎ) | Le1 M𝑠 ≍ Le2 M𝑠}          ⦃∃X.P⦄ ≜ ∃𝑋 . ⦃P⦄
      ⦃x ↦→ e⦄ ≜ {(𝑠, [𝑠 (x) ↦→ LeM𝑠])}             ⦃x ̸↦→⦄ ≜ {(𝑠, [𝑠 (x) ↦→ ⊥])}          ⦃emp⦄ ≜ {(𝑠, [])}
      ⦃P ∧ Q⦄ ≜ ⦃P⦄ ∩ ⦃Q⦄                        ⦃P ∨ Q⦄ ≜ ⦃P⦄ ∪ ⦃Q⦄                      ⦃P ∗ Q⦄ ≜ ⦃P⦄ • ⦃Q⦄
where the semantics for arithmetic and Boolean expressions L·M are defined as usual. We note that
a generic assertion in Ast can be rewritten as a (possibly infinite) disjunction of pure assertions
and structural assertions.3 We use the usual shortcuts x ↦→ _ for the ownership predicate when we
disregard the content of the location and x  y for expressing equality constraints over a memory
with empty heap: x ↦→ _ ≜ ∃y.x ↦→ y, and x  y ≜ x = y ∧ emp.
   As a matter of notation, we use the font P, Q, R, ... ∈ Ast when dealing with logical assertions,
and 𝑃, 𝑄, 𝑅, ... ∈ ℘(Mi ) when dealing with concrete sets of memories.
3 This fact will be exploited in completeness proofs and in Definition 4.6.
10                                                               Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


3    Logical Variables and Universal Frames
The scalability of methods based on separation logics builds on the notion of local axioms and
framing. Local axioms should account for the least amount of information necessary to execute each
atomic command. Then, a suitable frame rule allows for extending both the pre- and postconditions
by adding idle portions of the heap, whenever needed. Here, the frame rule must be designed with
particular care in order to preserve the validity of the triples, according to the sense and direction
of the analysis. The exact characterization of the valid frames applicable to a given triple is a
long-standing problem [Calcagno et al. 2007; Raza and Gardner 2008; Yang and O’Hearn 2002]. As
discussed in Section 1, the most common side condition for the frame rule is mod(r) ∩ fv(R) = ∅,
where mod(r) is the set of all variables that appear on the left hand side of some assignment in r.
While it prevents the frame from constraining any potentially modified program variable, this can
be unnecessarily restrictive in some cases (e.g., assignments in dead code or in dropped disjuncts).
   Logical variables. We address and solve the above problems by introducing a ‘universal’ charac-
terization of frames based on the concept of logical variables. To distinguish them from program
variables, they are annotated with a prime symbol (′ ). An early example about the use of logical
variables is the well-known Floyd’s axiom for assignment [Floyd 1967]:

                                  {P} x := e {∃x′ .P[x′ /x] ∧ x = e[x′ /x]}                                    (4)
where x′ represents the value of the program variable x before the assignment. Over the years,
various forms of auxiliary variables have been employed for similar purposes, albeit under different
names, such as in [Apt and Olderog 2019; Dardinier and Müller 2024; Floyd 1967; Kleymann 1999;
Morgan 1990; von Oheimb and Nipkow 2002]. In particular, they have been often used to freeze
the initial values of certain variables in the precondition and link them to their updated values in
the postcondition, upon termination. Since logical variables cannot be altered, they are inherently
immutable. As an example, the meaning of the triple
                            {x = x′ ∧ y = y′ } r {x = x′ ∧ y = y′ ∧ z = x′ + y′ }
is twofold: it says not only that whenever the command r terminates, the variable z stores the
sum of x and y, but also that the variables x and y remain unchanged [Apt and Olderog 2019,
§10.2]. Thereby, if a program variable is associated with the same logical variable in the pre- and
postcondition, then the program has not changed the value of that variable.
   Formally, we extend the memory models introduced in Section 2 by introducing a separate set
Xl of logical variables that cannot appear in any command and require the free variables of the
frame to be logical ones. This way the side condition mod(r) ∩ fv(R) = ∅ is satisfied by definition.
   Extended memory models. In order to guarantee the availability of a fresh symbol to denote a
certain value, in the logical store, we require for each value, the existence of a denumerable family
of logical variables with that value. This can be formalized by defining the logical store as follows:
                 Sl ≜ Xl → V         where        ∀𝑠 ∈ Sl .∀𝑣 ∈ V.∃{xi′ }i∈N ⊆ Xl .𝑠 (xi′ ) = 𝑣
   The set of stores will be S ≜ Sp × Sl , both for memory models 1 and 2. As a matter of notation,
we denote a generic pair ⟨𝑠 p, 𝑠 l ⟩ with 𝑠 and write just 𝑠 (𝑥) and 𝑠 (𝑥 ′ ) in place of 𝑠 p (𝑥) and 𝑠 l (𝑥 ′ ),
respectively. The introduction of logical variables is just a convenient mathematical construction to
support program analysis, as they should not be part of the machine model for executing the code.
Of course, any store 𝑠 p : Xp → V can be seen as the representative of the set of stores {𝑠 p } × Sl .
  Universal frames. In the following, we define a universal frame as any set of memories Sp ×𝑅 ×Hi ,
with 𝑅 ⊆ Sl , i.e., it can only constrain logical variables and not program ones.
Systematic Design of Separation Logics                                                                  11


    Definition 3.1 (Universal frame). A set of memories 𝑅 ⊆ Mi (with i ∈ {1, 2}) such that:
                              (𝑠, ℎ) ∈ 𝑅 ⇒ ∀x ∈ Xp .∀𝑣 ∈ V.(𝑠 [x ↦→ 𝑣], ℎ) ∈ 𝑅
is called a universal frame. We name F the set of all universal frames.
 In the assertion language, a universal frame is any assertion R such that fv(R) ⊆ Xl . Since
mod(r) ⊆ Xp , the condition mod(r) ∩ fv(R) = ∅ is trivially satisfied by universal frames.

4     Systematic Design Methodology
In this section, we show how to pair the locality principle with the seminal work of Cousot [2024]
on the calculational design of program logics through the means of abstract interpretation [Cousot
2021; Cousot and Cousot 1977]. While Cousot’s framework elegantly recovers a broad spectrum of
program logics [Cousot 2024, Figure 3], it does not address the direct calculation of local axioms or
the frame rule from the semantics. Here we exploit semantic closure properties to define a preorder
on valid triples and a notion of minimality that can be exploited to derive local axioms that, through
finite applications of closures, can generate all valid triples. Notably, by appropriately choosing
closure operators, the same approach can be applied to a variety of program logics. Axioms devised
with our methodology can be paired with other approaches that account for the inference rules
required to handle all the other program composition operators, e.g, Cousot [2024] framework.
   In the first part of this section, we present the general methodology that entirely depends on the
semantic function and the identification of available closures. In the second part, we showcase the
systematic derivation of semantic proof systems for separation logics. Both developments have
been mechanized in Isabelle/HOL, providing a proof of concept for forward analysis.

4.1    General methodology
A closure is a monotone function that is extensive and idempotent. We focus on closure properties
of program logics, such that, given a valid predicate 𝑝, any predicate obtained by applying the
closure operators to 𝑝 is also valid. Typically, these closures correspond to inference rules of the
logic. As an example, for the theory of HL triples [Hoare 1969], one possible closure operator is:
                                        △
                               𝜌 cons 𝑇 = {(𝑃, c, 𝑄 ′ ) | (𝑃, c, 𝑄) ∈ 𝑇 ∧ 𝑄 ⊆ 𝑄 ′ }
   This means that if 𝑄 over-approximates the semantics of the command c on input 𝑃, we can
replace 𝑄 with any larger 𝑄 ′ while preserving the validity of the triple. This closure operator is
effectively encapsulated within the proof system of HL through the consequence rule:
                                          {P} c {Q} Q ⇒ Q ′
                                                                                                        (5)
                                               {P} c {Q ′ }
   Each closure 𝜌 induces a preorder, in the sense that 𝑝 precedes or is equal to 𝑝 ′ if 𝑝 ′ ∈ 𝜌 ({𝑝}).
Therefore, a minimal set of (valid) predicates 𝑇 such that 𝜌 (𝑇 ) contains all and only valid predicates
is a suitable candidate to form the axioms of the logic. Although our discussion centers on closure
operators for program triples related to atomic commands, the same reasoning could naturally be
extended to the entire language Reg. However, exploring this broader extension lies beyond the
scope of our current focus. The general methodology consists of the following steps:
    (1) Fix the semantic property of interest (e.g., that the postcondition is an over-approximation
         of the exact semantics) and let TriplesJcK denote the set of valid semantic triples for c.
    (2) Select a finite set of (property preserving) closure operators 𝜌 1, ..., 𝜌𝑛 (e.g., the consequence
         rule (5) or a frame rule), such that 𝜌𝑖 (TriplesJcK ) = TriplesJcK for any closure 𝜌𝑖 .
    (3) Let 𝜌 ≜ ( 𝑖 𝜌𝑖 ) ∗ represent any finite sequence of applications of 𝜌 1, ..., 𝜌𝑛 . It can be shown
                   Ð
         that 𝜌 is still a closure operator and that 𝜌 (TriplesJcK ) = TriplesJcK holds. Moreover, under
12                                                                     Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


                                    Forward                                          Backward
                                                                   TriplesJ·cK ≜ {(𝑃, c, 𝑄) ←· | J←
                                                                                                  c−K𝑄 ⊆ 𝑃 }
                          →                                               ←
          Over     TriplesJ·cK ≜ {(𝑃, c, 𝑄) →· | JcK𝑃 ⊆ 𝑄 }
                            ·                                              ·
                                                                              ≜ {(𝑃, c, 𝑄) ← | 𝑃 ⊆ J←
                                                                                                    c−K𝑄 }
                                               ·                                           ·
         Under     Triples→
                          JcK
                              ≜ {(𝑃, c, 𝑄) → | 𝑄 ⊆ JcK𝑃 }          Triples←
                                                                          JcK

      Table 3. Set of valid semantics triple for each direction of the analysis and sense of approximation.

        suitable circumstances, extensively discussed in [Cousot 1978; Ore 1943], the closure 𝜌 can
        be further simplified to a single sequence of applications 𝜌 𝜋 (1) ◦ · · · ◦ 𝜌 𝜋 (𝑛) of the original
        closures, for some permutation 𝜋 of the indexes 1, ..., 𝑛. We achieve this result by proving
        that certain pairwise swaps 𝜌 𝜋 ( 𝑗 ) ◦ 𝜌 𝜋 (𝑖 ) ⊆ 𝜌 𝜋 (𝑖 ) ◦ 𝜌 𝜋 ( 𝑗 ) of closures are possible when 𝑖 ≤ 𝑗.
    (4) Select a set AxiomsJcK ⊆ TriplesJcK such that 𝜌 (AxiomsJcK ) = TriplesJcK , and which is
        minimal in the sense that no triple in AxiomsJcK is derivable from the remaining ones via the
        closure operators. We exploit the characterization 𝜌 = 𝜌 𝜋 (1) ◦ · · · ◦ 𝜌 𝜋 (𝑛) to prove that any
        valid semantic triple can be obtained from the axioms by applying the closures in a fixed
        order. The axioms in the set AxiomsJcK ⊆ TriplesJcK are exactly the axioms of our semantic
        proof system, and each closure 𝜌 1, ..., 𝜌𝑛 yields a corresponding inference rule.
    (5) The semantic rules are then transformed to a logical proof system by selecting a suitable
        assertion language for expressing pre- and postconditions. In particular, for each command
        c, a minimal set of logical axioms is chosen that is able to cover the triples in AxiomsJcK .
  It is immediate to verify that the above methodology leads us to derive sound and (relative)
complete proof systems for the analysis of interest.

4.2     Systematic design of separation logics
In this section, we apply our methodology to the synthesis of separation logics. We let c be an atomic
command and denote by JcK its forward semantics, which may depend, e.g., on the considered
memory model. For either directions of the analysis and senses of approximation, the set of
semantics triples is defined in Table 3, where we write J←  c−K to refer to the backward semantics of the
command c, defined as the opposite relation of the forward semantics, i.e., J←      −
                                                                                    r K𝜎 ′ ≜ {𝜎 | 𝜎 ′ ∈ JrK}.
Since multiple notions of validity are involved, superscripts indicate both the analysis direction
and the sense of approximation. Arrows specify direction—right for forward, left for backward
semantics—while their position relative to the dot denotes approximation: above for over-, below
for under-approximation. For example, →· represents an over-approximation in forward semantics.
Step (1) consists of fixing the set of triples of interest among those in Table 3.
   According to the choice in Step (1), in Step (2) we select three closure operators: exists, frame, and
consequence.4 The exists closure establishes that proving correctness for some concrete values of
variables automatically lifts to the family of states where those variables are existentially quantified.
                                                   ↔                             ↔
                                        ↔ 𝑇 ≜ {(∃X.𝑃, c, ∃X.𝑄) ↔ | (𝑃, c, 𝑄) ↔ ∈ 𝑇 , X ⊆ X }    ↔
     Definition 4.1 (Exists Closure). 𝜌 exists                                            l

   For closure operators, superscripts can be combined to cover all analyses supported by the
closure; e.g., the superscript ↔↔ indicates that the closure operator 𝜌 exists is valid for over- and
under-approximation of the forward and backward semantics. Table 6 in Appendix provides a
glossary of all superscripts used, for the reviewer’s convenience. The correctness of the closure
  ↔
  ↔
𝜌 exists immediately follows from the fact that logical variables cannot appear in the program.
4 The names of the closure operators comes from the inference rules Exists, Frame and Consequence of existing separation

logics [Ascari et al. 2025; O’Hearn 2020; Raad et al. 2020, 2022, 2024; Reynolds 2002], from which they have been inspired.
Systematic Design of Separation Logics                                                               13


   The second closure embodies the essence of the locality principle. It states that any valid triple
that refers to a portion of the memory can be automatically lifted to every other memory extended
with a compatible frame. In other words, it captures the role of the frame rule in separation logics.
However, we need to find an appropriate notion of compatibility. The classical condition ensuring
correctness was mod(r) ∩ fv(R) = ∅. As discussed in Section 1, we argue that this condition works
properly for over-approximation but not for under-approximation. This is because when dealing
with over-approximation, the soundness requirement for framing a triple {P} r {Q} with R is
expressed by the condition JrK(R ∗ P) ⊆ (R ∗ Q), which is not guaranteed to be sound also for
under-approximations. Here, instead, we proceed with a different approach by defining a new
notion of heap compatibility, where the framing is allowed only if the semantics is preserved. The
new notion of heap compatibility is driven by the need for a closure that serves only two purposes:
    (1) to restrict the set of admissible stores in both the pre- and postconditions,
    (2) to extend the heap in both pre- and postconditions whenever no conflicts arise.
   For example, let us frame with x ↦→ _ the triple derived from the axiom of deallocation:
                                        {x ↦→ _} free(x) {emp}
                                                                                                     (6)
                                  {x ↦→ _ ∗ x ↦→ _} free(x) {x ↦→ _}
   Even though the conclusion is a valid over-approximation triple, the exact semantics of free(x) is
not preserved by framing, because, by definition of ∗, the pre is false but the post is not. Moreover,
extending a triple with an already specified region yields no additional semantic meaning.
   In our setting, we want to preclude this kind of framing, because it falls into neither case (1) nor
case (2). Since approximation is the scope of our third closure operator, we require that the frame
closure operator just preserve approximation without introducing it. To this aim, we say that two
sets of memories 𝑀1 and 𝑀2 are heap compatible if for each state (𝑠, ℎ) ∈ 𝑀1 and (𝑠 ′, ℎ ′ ) ∈ 𝑀2 , if
they match on the store, then the domains of ℎ and ℎ ′ are disjoint, i.e. ℎ#ℎ ′ .
  Definition 4.2 (Heap Compatibility). Given 𝑀1, 𝑀2 ⊆ Mi , we define heap compatibility between
𝑀1 and 𝑀2 as follows: 𝑀1 ▶◀ 𝑀2 ≜ ∀(𝑠, ℎ) ∈ 𝑀1, ∀(𝑠 ′, ℎ ′ ) ∈ 𝑀2, 𝑠 = 𝑠 ′ ⇒ ℎ#ℎ ′
   We note that, although the predicate ▶◀ may resemble the operator •, they are quite distinct. The
latter requires the stores to be identical and the heaps to be disjoint, whereas the former requires
heap disjointness only when the stores coincide. This stronger property is critically important, as it
is instrumental in the following results, which guarantee semantic preservation when a local proof
is lifted to a heap-compatible memory. Specifically, they establish the preservation of forward and
backward semantics. We recall that F is the set of universal frames (see Definition 3.1).
  Theorem 4.1 (Forward Preservation). Given 𝑃, r, 𝑄 such that JrK𝑃 = 𝑄 and 𝑅 ∈ F such that
𝑃 ▶◀ 𝑅, then (JrK𝑃) • 𝑅 = JrK(𝑃 • 𝑅) = 𝑄 • 𝑅.
  Theorem 4.2 (Backward Preservation). Given 𝑃, r, 𝑄 such that J←
                                                                −
                                                                r K𝑄 = 𝑃 and 𝑅 ∈ F such that
𝑄 ▶◀ 𝑅, then (J←−
                r K𝑄) • 𝑅 = J←−
                              r K(𝑄 • 𝑅) = 𝑃 • 𝑅.
  We can now define two closure operators frame, according to the direction of the analysis.
  Definition 4.3 (Frame Closures). The frame closure operators are defined as follows:
         →→                              →        →
     • 𝜌 frame 𝑇 ≜ {(𝑃 • 𝑅, c, 𝑄 • 𝑅) → | (𝑃, c, 𝑄) → ∈ 𝑇 , 𝑅 ∈ F, 𝑃 ▶◀ 𝑅} (forward semantics),
         ←
         ←                            ←             ←
     • 𝜌 frame 𝑇 ≜ {(𝑃 • 𝑅, c, 𝑄 • 𝑅) ← | (𝑃, c, 𝑄) ← ∈ 𝑇 , 𝑅 ∈ F, 𝑄 ▶◀ 𝑅} (backward semantics).
  The third and last family of closure operators account for the admissible weakening and strength-
ening of pre- and postcondition. We note that these closures are the only sources of approximation
among the closure operators we consider.
14                                                                    Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


               Direction     Sense      Exists closure           Frame closure         Cons closure
                                                                                            →·
                              Over                                       →
                                                                         →                𝜌 cons
                Forward                                                𝜌 frame              →·
                             Under              ↔
                                                ↔                                         𝜌 cons
                                              𝜌 exists                                      ←·
                              Over                                       ←
                                                                         ←                𝜌 cons
               Backward                                                𝜌 frame              ← ·
                             Under                                                        𝜌 cons
               Table 4. Characterization of each logic under consideration in terms of closures.

     Definition 4.4 (Conseqence Closures). The cons closure operators are defined as follows:
           →·
       • 𝜌 cons 𝑇 ≜ {(𝑃, c, 𝑄 ′ ) →· | (𝑃, c, 𝑄) →· ∈ 𝑇 , 𝑄 ⊆ 𝑄 ′ } (forward-over),
            ·
           → 𝑇 ≜ {(𝑃, c, 𝑄 ′ ) →   ·              ·
       • 𝜌 cons                      | (𝑃, c, 𝑄) → ∈ 𝑇 , 𝑄 ′ ⊆ 𝑄 } (forward-under),
           ←                      ←              ←
            ·
       • 𝜌 cons 𝑇 ≜ {(𝑃 ′, c, 𝑄) · | (𝑃, c, 𝑄) · ∈ 𝑇 , 𝑃 ⊆ 𝑃 ′ } (backward-over),
            ·                      ·              ·
       • 𝜌 cons 𝑇 ≜ {(𝑃 ′, c, 𝑄) ← | (𝑃, c, 𝑄) ← ∈ 𝑇 , 𝑃 ′ ⊆ 𝑃 } (backward-under).
           ←


   In line with the general methodology, the set of valid axioms for each logic under consideration
can be characterized in terms of the closure operators introduced above (as summarized in Table 4).
   For the sake of conciseness, the following material concerns only over-approximation logics of
the forward semantics; material for all remaining combinations is collected in Appendix D.1.
   Let us define the closure 𝜌 →· as the closure accounting for any finite combination of closures
  ↔
  ↔ , 𝜌→ → , and 𝜌 →  ·                    →      ↔          →          →    ∗
                                           · ≜ (𝜌 ↔          →           ·
𝜌 exists frame       cons , i.e., we let 𝜌        exists ∪ 𝜌 frame ∪ 𝜌 cons ) .
                                                                             →
   As required by Step (3), the next result allows us to express 𝜌 · in terms of a single application
                                    ↔
                                    ↔ , 𝜌→  → , and 𝜌 →   ·
(and in very precise order) of 𝜌 exists     frame        cons : first the frame closure then the exists closure
and finally the consequence closure. The proof relies on [Cousot 1978, §4.2].
                                                    →        ↔          →
     Theorem 4.3 (Normalization). 𝜌 →· = 𝜌 cons
                                            ·       ↔
                                                ◦ 𝜌 exists     →
                                                           ◦ 𝜌 frame
  At Step (4) we identify the actual set of axioms and prove that all valid triples can be derived
using closure operators.
                                                                  →                                  →             →
     Definition 4.5 (Axioms). A set of axioms for TriplesJ·cK is any minimal set AxiomsJ·cK ⊆ TriplesJ·cK
                   →                    →
such that TriplesJ·cK ≜ 𝜌 →· (AxiomsJ·cK ).
                                                                                   →               →
     Corollary 4.4 (Completeness). Any valid set of axioms AxiomsJ·cK for TriplesJ·cK is such that:
                                    →         →          ↔        →                →
                            TriplesJ·cK = (𝜌 cons
                                              ·       ↔
                                                  ◦ 𝜌 exists     → ) (Axioms · ) .
                                                             ◦ 𝜌 frame      JcK

   The very same strategy inspired by Corollary 4.4 is adopted, e.g., in the proof of Theorem 5.1.
   In Figure 1 we report our general semantic proof system for each logic under consideration,
which is applicable for any choice of atomic commands and their semantics. We use the symbol
⊩ for assertions in the semantic proof systems in order to distinguish them from assertion in the
logical proof systems that will be discussed in the next sections. The next result guarantees that
the semantic proof systems are sound and complete within their semantics, i.e., a triple is derivable
if and only if it is valid in the considered semantics. Soundness can be proved by induction on the
derivation tree. Completeness of atomic commands follows directly from the definitions of semantic
axioms. Furthermore, completeness of compositions for Fwd-over, Fwd-under and Bwd-under
can be proved respectively as in [Cook 1978], [O’Hearn 2020], and [Ascari et al. 2025]. Finally,
completeness of compositions for Bwd-over is proved in the Appendix D.
     Theorem 4.5 (Soundness and completeness). All proof systems in Fig. 1 are sound and complete.
Systematic Design of Separation Logics                                                                                                                  15



   Rule                Fwd-over                          Fwd-under                         Bwd-over                          Bwd-under
                                     →                       ·          ·                               ←                        ·                ·
                (𝑃, c, 𝑄) →· ∈ AxiomsJ·cK          (𝑃, c, 𝑄) → ∈ Axioms→
                                                                       JcK
                                                                                   (𝑃, c, 𝑄) ←· ∈ AxiomsJ·cK          (𝑃, c, 𝑄) ← ∈ Axioms←
                                                                                                                                          JcK
  Transfer           ⊩ {𝑃 } c {𝑄 }                       ⊩ [𝑃] c [𝑄]                      ⊩ (𝑃) c (𝑄)                       ⊩ ⟨⟨𝑃⟩⟩ c ⟨⟨𝑄⟩⟩

             𝑅 ∈ F ⊩ {𝑃 } r {𝑄 } 𝑃 ▶◀ 𝑅         𝑅 ∈ F ⊩ [𝑃] r [𝑄] 𝑃 ▶◀ 𝑅         𝑅 ∈ F ⊩ (𝑃) r (𝑄) 𝑄 ▶◀ 𝑅         𝑅 ∈ F ⊩ ⟨⟨𝑃⟩⟩ r ⟨⟨𝑄⟩⟩ 𝑄 ▶◀ 𝑅
   Frame         ⊩ {𝑃 • 𝑅} r {𝑄 • 𝑅}                ⊩ [𝑃 • 𝑅] r [𝑄 • 𝑅]               ⊩ (𝑃 • 𝑅) r (𝑄 • 𝑅)              ⊩ ⟨⟨𝑃 • 𝑅⟩⟩ r ⟨⟨𝑄 • 𝑅⟩⟩

                ⊩ {𝑃 } r {𝑄 ′ } 𝑄 ′ ⊆ 𝑄            ⊩ [𝑃] r [𝑄 ′ ] 𝑄 ⊆ 𝑄 ′           ⊩ (𝑃 ′ ) r (𝑄) 𝑃 ′ ⊆ 𝑃           ⊩ ⟨⟨𝑃 ′ ⟩⟩ r ⟨⟨𝑄⟩⟩ 𝑃 ⊆ 𝑃 ′
   Cons               ⊩ {𝑃 } r {𝑄 }                     ⊩ [𝑃] r [𝑄]                       ⊩ (𝑃) r (𝑄)                      ⊩ ⟨⟨𝑃⟩⟩ r ⟨⟨𝑄⟩⟩

                ⊩ {𝑃 } r {𝑄 } X ⊆ Xl                ⊩ [𝑃] r [𝑄] X ⊆ Xl              ⊩ (𝑃) r (𝑄) X ⊆ Xl                ⊩ ⟨⟨𝑃⟩⟩ r ⟨⟨𝑄⟩⟩ X ⊆ Xl
   Exists        ⊩ {∃X.𝑃 } r {∃X.𝑄 }                 ⊩ [∃X.𝑃] r [∃X.𝑄]               ⊩ (∃X.𝑃) r (∃X.𝑄)                 ⊩ ⟨⟨∃X.𝑃⟩⟩ r ⟨⟨∃X.𝑄⟩⟩

                ∀𝑖 ∈ 𝐼 . ⊩ {𝑃𝑖 } r {𝑄𝑖 }           ∀𝑖 ∈ 𝐼 . ⊩ [𝑃𝑖 ] r [𝑄𝑖 ]         ∀𝑖 ∈ 𝐼 . ⊩ (𝑃𝑖 ) r (𝑄𝑖 )          ∀𝑖 ∈ 𝐼 . ⊩ ⟨⟨𝑃𝑖 ⟩⟩ r ⟨⟨𝑄𝑖 ⟩⟩
    Disj        ⊩ {∪𝑖 ∈𝐼 𝑃𝑖 } r {∪𝑖 ∈𝐼 𝑄𝑖 }        ⊩ [∪𝑖 ∈𝐼 𝑃𝑖 ] r [∪𝑖 ∈𝐼 𝑄𝑖 ]      ⊩ (∪𝑖 ∈𝐼 𝑃𝑖 ) r (∪𝑖 ∈𝐼 𝑄𝑖 )       ⊩ ⟨⟨∪𝑖 ∈𝐼 𝑃𝑖 ⟩⟩ r ⟨⟨∪𝑖 ∈𝐼 𝑄𝑖 ⟩⟩

             ⊩ {𝑃 } r1 {𝑆 } ⊩ {𝑆 } r2 {𝑄 }       ⊩ [𝑃] r1 [𝑆] ⊩ [𝑆] r2 [𝑄]       ⊩ (𝑃) r1 (𝑆) ⊩ (𝑆) r2 (𝑄)        ⊩ ⟨⟨𝑃⟩⟩ r1 ⟨⟨𝑆⟩⟩ ⊩ ⟨⟨𝑆⟩⟩ r2 ⟨⟨𝑄⟩⟩
    Seq            ⊩ {𝑃 } r1 ; r2 {𝑄 }                ⊩ [𝑃] r1 ; r2 [𝑄]               ⊩ (𝑃) r1 ; r2 (𝑄)                  ⊩ ⟨⟨𝑃⟩⟩ r1 ; r2 ⟨⟨𝑄⟩⟩

               ∀𝑖 ∈ {1, 2}. ⊩ {𝑃 } 𝑟𝑖 {𝑄 }        ∀𝑖 ∈ {1, 2}. ⊩ [𝑃] 𝑟𝑖 [𝑄𝑖 ]      ∀𝑖 ∈ {1, 2}. ⊩ (𝑃) 𝑟𝑖 (𝑄)        ∀𝑖 ∈ {1, 2}. ⊩ ⟨⟨𝑃𝑖 ⟩⟩ 𝑟𝑖 ⟨⟨𝑄⟩⟩
  Choice          ⊩ {𝑃 } r1 + r2 {𝑄 }              ⊩ [𝑃] r1 + r2 [𝑄 1 ∪ 𝑄 2 ]         ⊩ (𝑃) r1 + r2 (𝑄)              ⊩ ⟨⟨𝑃 1 ∪ 𝑃 2 ⟩⟩ r1 + r2 ⟨⟨𝑄⟩⟩

                     ⊩ {𝑃 } r {𝑃 }                ∀𝑛 ≥ 0. ⊩ [𝑃𝑛 ] r [𝑃𝑛+1 ]              ⊩ (𝑄) r (𝑄)                ∀𝑛 ≥ 0. ⊩ ⟨⟨𝑄𝑛+1 ⟩⟩ r ⟨⟨𝑄𝑛 ⟩⟩
    Iter             ⊩ {𝑃 } r∗ {𝑃 }                 ⊩ [𝑃0 ] r∗ [∪𝑛≥0 𝑃𝑛 ]                ⊩ (𝑄) r∗ (𝑄)                 ⊩ ⟨⟨∪𝑛≥0𝑄𝑛 ⟩⟩ r∗ ⟨⟨𝑄 0 ⟩⟩


   Empty              ⊩ {∅} r {𝑄 }                       ⊩ [𝑃] r [∅]                      ⊩ (𝑃) r (∅)                       ⊩ ⟨⟨∅⟩⟩ r ⟨⟨𝑄⟩⟩

                ⊩ {𝑃 ′ } r {𝑄 }   𝑃 ⊆ 𝑃′           ⊩ [𝑃 ′ ] r [𝑄]    𝑃′ ⊆ 𝑃         ⊩ (𝑃) r (𝑄 ′ )    𝑄 ⊆ 𝑄′         ⊩ ⟨⟨𝑃⟩⟩ r ⟨⟨𝑄 ′ ⟩⟩ 𝑄 ′ ⊆ 𝑄
   Cons2              ⊩ {𝑃 } r {𝑄 }                      ⊩ [𝑃] r [𝑄]                      ⊩ (𝑃) r (𝑄)                      ⊩ ⟨⟨𝑃⟩⟩ r ⟨⟨𝑄⟩⟩

Fig. 1. Semantic proof systems. The figure is divided into four groups. First, we list the rules for axioms,
according to Corollary 4.4. In the second group, we list rules induced by closure operators (for Disj see
Section 4.2.1). The third group collects standard rules for command compositions, while auxiliary rules are
in the fourth group. Key novelties are in light blue. Except for the new transfer and frame rules, the proof
systems listed in Columns 1, 2, and 4 have already been proposed in literature [Ascari et al. 2025; Möller et al.
2021]. By contrast, Column 3 introduces the first proof system for separation NC.

  Given the assertion language of Section 2.2, Step (5) requires to identify a set of pre/postcondition
pairs such that every triple in AxiomsJcK is captured by some of the pre/postcondition pair (and
such that every axiom instance is sound too, i.e., it is in TriplesJcK ). Interestingly, Corollary 4.4
provides a systematic method to derive logical axioms:
                      →
                  · , axioms can provide the strongest postcondition for a given precondition;
      • due to 𝜌 cons
                      ↔
                      ↔ , logical variables can be used to separate the part of the heap H that is
      • thanks to 𝜌 exists
        modified by the atomic command c from the rest, seen as a suitable universal frame R;
                     →
                     → , each axiom can focus on the precondition H, leaving the frame R aside.
      • thanks to 𝜌 frame
   Since the semantic frame rule requires, as a side condition, the heap compatibility check 𝑃 ▶◀ 𝑅
(see Definition 4.2), we need to distill a logical characterization of heap compatibility:
  Definition 4.6 (Logical Heap Compatibility). Given the assertions M1 = ∨i (Pi ∧ Hi ) ∈ Ast
and M2 = ∨j (Pj ∧ Hj ) ∈ Ast we define heap compatibility M1 ⊲⊳ M2 between M1 and M2 as follows:
                                              M1 ⊲⊳ M2 ≜ ∀i, j.(Pi ∧ Pj ) ⇒ (Hi ∗ Hj ) .


  Proposition 4.6. For any M1, M2 ∈ Ast we have: M1 ⊲⊳ M2 ⇐⇒ ⦃M1 ⦄ ▶◀ ⦃M2 ⦄.
16                                                                 Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


  The correspondence in Proposition 4.6 grants us that logical heap compatibility ⊲⊳ can safely
replace the semantic relation ▶◀ in all frame rules of Figure 1.
   Mechanization. The main technical results of this section have been mechanized in Isabelle/HOL
as a proof-of-concept for our systematic design procedure. Concretely, we have formalized the
semantic setting (memories, universal frames, and heap compatibility) together with the three
closure operators (consequence, existential generalization, and frame). Within this framework, we
replicated the central normalization proof, showing that any finite combination of closures can be
rearranged into a canonical sequence (frame, then existential generalization, then consequence),
thereby confirming the validity of Theorem 4.3. We then moved to address Step (5). We fixed an
assertion language in the spirit of our separation-logic assertions, we introduced a corresponding
normal form for assertions, implemented the procedure that distill local axioms by extracting the
assertion that represents the idle frame and verified its correctness in Isabelle.
4.2.1 On Disjunction. The choices of closure operators need some discussion. Indeed, one may
think of adding a fourth closure operator to capture the additivity of the collecting semantics. In the
following, we give a definition of the closure operator disj which is independent from the direction
of the analysis and the sense of approximation.
                                             ↔                             ↔
                                      ↔ 𝑇 ≜ {(∪ 𝑃 , c, ∪ 𝑄 ) ↔ | ∀𝑖 ∈ 𝐼 .(𝑃 , c, 𝑄 ) ↔ ∈ 𝑇 }.     ↔
     Definition 4.7 (Disj closure). 𝜌 disj     𝑖 ∈𝐼 𝑖   𝑖 ∈𝐼 𝑖             𝑖      𝑖

   The reason why we treat the closure operator disj separately comes from order theory. When
dealing only with closures exists, cons and frame, we can guide the choice of the axioms by
minimality: we can define an order ≤ induced by the closure and looking for the minimal elements
of that order. Although applying the three closures can result in some preorder (e.g., the frame
closure can introduce vacuous logical variables that are then eliminated by applying the exists
closure), we can take the order induced by the equivalent classes modulo ≤. Each element of
the minimal equivalence class is a candidate axiom. On the other hand, when considering also
the closure operator disj, it is difficult to define a suitable order: the same resulting element can
be composed by starting from more than one choice of axioms. Notwithstanding this issue, the
subsequent results enable us to present and treat every proof system with the disjunction rule in
                                                                             ↔
                                                                             ↔ . In fact, Definition 4.7
Figure 1, which is the inference rule induced by the closure operator 𝜌 disj
allows for a similar result obtained for the previous closures: any finite, arbitrarily ordered use of
the four closures can be rewritten as a single application of each, ordered frame → exists → disj
→ cons. In the following, we just report the result for over-approximation logics of the forward
semantics; the corresponding material for all the logics examined is provided in the Appendix D.1.
                      ·  →       ↔
                              ↔ ∪ 𝜌↔     ↔    →    → ∗     ·   →   ↔   ↔    ↔  ↔       →→
     Theorem 4.7. (𝜌 cons ∪ 𝜌 disj exists ∪ 𝜌 frame ) = 𝜌 cons ◦ 𝜌 disj ◦ 𝜌 exists ◦ 𝜌 frame .

   The following theorem establishes a correspondence between a proof that employs the dis-
junction closure and one that does not. Specifically, starting from a collection of triples (𝑃𝑖 , c, 𝑄𝑖 )
and allowing Ð   the use of the disjunction       closure yields the same result as starting from their
unified form ( 𝑖 ∈𝐼 (𝑃𝑖 ∩ 𝑑 ′ = 𝑖), c, 𝑖 ∈𝐼 (𝑄𝑖 ∩ 𝑑 ′ = 𝑖)) and avoiding the use of the disjunction clo-
                                         Ð
sure. The variable 𝑑 ′ serves to distinguish among the different disjuncts, thereby enabling a con-
nection between the pre- and the postcondition. In particular, by assuming the unified triple
( 𝑖 ∈𝐼 (𝑃𝑖 ∩ 𝑑 ′ = 𝑖), c, 𝑖 ∈𝐼 (𝑄𝑖 ∩ 𝑑 ′ = 𝑖)), one can selectively focus on a subset of cases 𝐾 by apply-
 Ð                       Ð
ing a frame 𝑅 = 𝑘 ∈𝐾 𝑑 ′ = 𝑘. We note that the rule induced by this closure was also used by Raad
                   Ð
et al. [2024] with the rule DisjTrack, a non-lossy version of the classical Disj, which preserves the
pre-post correspondence and allows a disjunct to be dropped from both the pre- and postcondition.
Systematic Design of Separation Logics                                                                                                                    17


             2                                                              1                                           2
    {Alloc2}+                                                         {Free}+                                {Free2}+


    {empXp ∗ l′ ̸↦→} x := alloc() {empXp \{x} ∗ l′ ↦→ z′ ∧ x = l′ }   {empXp ∗ x ↦→ z′ } free(x) {empXp }    {empXp ∗ x ↦→ z′ } free(x) {empXp ∗ x ̸↦→}

                     i                                                i                                                              i
          {Alloc}+                                          {Assign}+                                                       {Assume}+


          {empXp } x := alloc() {empXp \{x} ∗ x ↦→ z′ }     {empXp \{x} ∧ x = x′ } x := e {empXp \{x} ∧ x = e[x′ /x]}       {empXp } b? {empXp ∧ b}

                                 i                                                             i
                         {Load}+                                                        {Store}+


                         {empXp ∗ y ↦→ z′ } x := [y] {empXp \{x} ∗ y ↦→ z′ ∧ x = z′ }   {empXp ∗ x ↦→ z′ } [x] := y {empXp ∗ x ↦→ y}


      Fig. 2. SL+: Synthesized axioms for forward correctness analysis in both memory models i ∈ {1, 2}.

    Theorem 4.8. For every index set 𝐼 ,
    ↔
   ↔ ◦ 𝜌↔        ↔ →         →                      ↔          →      ↔           →  ′                       ′
(𝜌 disj exists ◦ 𝜌 frame ){(𝑃𝑖 , c, 𝑄 𝑖 )}𝑖 ∈𝐼 = (𝜌 exists ◦ 𝜌 frame ){(∪𝑖 ∈𝐼 (𝑃𝑖 ∩ 𝑑 = 𝑖), c, ∪𝑖 ∈𝐼 (𝑄 𝑖 ∩ 𝑑 = 𝑖))} .

  Remark 1. Theorem 4.8 allows us to include the disjunction rule in all proof systems in Figure 1.
However, it guarantees that we can find axioms by minimality ignoring the disjunction closure.

5     Systematic Design of Forward Separation Logics
In this section, we instantiate our semantic proof systems for forward analysis (Figure 1, first two
columns) by considering the program semantics of SL [O’Hearn et al. 2001; Reynolds 2002] and ISL
[Raad et al. 2020]. As discussed in Section 2, SL and ISL consider two different memory models;
however we will synthesize SL and ISL proof systems for both memory models, using the assertion
language Ast defined in (3). Following SL and ISL, we consider atomic commands c to be:
                     Atom ∋ c ::= b? | error() | x := e | x := alloc() | free(x) | x := [y] | [x] := y                                                    (7)
where b? filters the stores by discarding those that do not satisfy the Boolean expression b; error()
halts the execution and raises an error; x := e is the usual assignment; x := alloc() allocates a new
location on the heap with a nondeterministic value and assigns the location to x; free(x) deallocates
the location on the heap pointed by x; x := [y] assigns to x the value contained in the location on
the heap pointed by y; and [x] := y assigns the value of y to the location on the heap pointed by x.
Without loss of generality, we assume the variables x and y to be different in the above grammar
productions. Classical no-op command skip can be defined as the macro skip ≜ true?.

5.1     Design of SL+
As a first instance of our methodology, we consider the semantics used in SL [O’Hearn et al. 2001;
                                          ↔
                                          ↔ , 𝜌→ → , and 𝜌 → ·
Reynolds 2002], with closure operators 𝜌 exists  frame      cons from Table 4. For the memory model
i ∈ {1, 2}, we rely on a functional version J·KSL                  i         i
                                                   i : Reg → M → ℘(M ⊎ {abort}). Both are
formalized in the Appendix (Figure 6) for reviewers’ convenience. The distinguished outcome
abort serves to indicate a generic fault.5 For notational convenience, we use the same symbol J·KSL
                                                                                                 i
to denote the lifted version to set of states, defined by union as usual.6 In Figure 2 we introduce
the logical axioms of SL+ obtained applying Step (5) to the semantic axioms for the two memory
models, where we characterize pre- and postconditions using the assertion language of (3) (see
Figure 8 in Appendix for the full proof system). For compactness and to highlight commonalities,
5We assume that the abort state is propagated during the computation, i.e., we let JrKSL abort ≜ {abort} with i ∈ {1, 2}.
                                                                                      i
6 JrKSL 𝑃 = Ð             SL
     i        (𝑠,ℎ) ∈𝑃 JrKi (𝑠, ℎ).
18                                                          Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


we superscript every rule’s name with 1 and 2, according to the memory model we are considering.
                                                                                           1
Rules that are common to both semantics are superscripted with i. For example {Free}+ is valid
                                       2                                                   i
only in the memory model 1, {Alloc2}+ is valid only in the memory model 2 and {Alloc}+ is valid
                                           i
for both memory models. We denote by ⊢SL+ the proof system related to the memory model i.
   Before delving into the proof system, we look at Floyd’s axioms for assignment in the two
proposed versions. On the left, the classical global version [Floyd 1967], and on the right the local
version proposed for SL [O’Hearn et al. 2001], and also used in ISL [Raad et al. 2020]:
          {P} x := e {∃x′ .P[x′ /x] ∧ x = e[x′ /x]}           {x  x′ } x := e {x  e[x′ /x]}
   The global version applies to any precondition P and the postcondition uses the logical variable
x′ to describe how to manipulate P when we assign the expression e to x. For example, starting
with a precondition that requires x to be odd, we can derive the following triple:
                           {odd(x)} x := x + 1 {∃x′ .odd(x′ ) ∧ x = x′ + 1}                               (8)
   On the other hand, the local version adheres to the principle of locality of the separation logics
where the premise accounts for the minimum heap needed to execute the assignment, which is
the empty heap (recall that x  x′ requires the heap to be empty). Furthermore, the premise uses
a logical variable that captures the value of x before the assignment, which will be used in the
postcondition. Using the frame rule to constrain the value of x′ , thereby limiting the value of x
before the assignment, yields the same result as (8):
                                  {x  x′ } x := x + 1 {x = x′ + 1}
                        {x  x′ ∗ odd(x′ )} x := x + 1 {x = x′ + 1 ∗ odd(x′ )}
   The proof system in Figure 2 heavily employs logical variables akin to x′ in the preceding example;
in SL+, however, this design choice emerges directly from the memory model detailed in Section 2.1.
Specifically, axioms are selected by minimality w.r.t. (also) the frame closure, which uses only
universal frames (Definition 3.1). Both the pre- and postcondition must include a mechanism that
relies exclusively on universal frames to embed the local reasoning within a broader memory. The
existence of a mirroring logical variable for each program variable in the precondition guarantees
a way to constrain the value of x before executing the command. To reflect this in our new model,
we introduce a shorthand assertion, denoted empX . It is analogous to the classical assertion emp
but it imposes the existence of a logical variable x′ for each variable x ∈ X:
                                        empX ≜ x∈X x  x′
                                                 Ó

  Each SL+ axiom incorporates the above shorthand, thereby ensuring the presence of a distinct
logical variable for every program variable and making these variables explicit whenever required.
                              i
For instance, in rule {Assign}+ , the logical variable x′ associated with x is made explicit in the post.
  In the following, we discuss the proof system in more detail, by highlighting its main features
and advantages w.r.t. the classical SL.
   Frame rule and logical variables. The peculiarity of our derived proof system lies in the combina-
tion of logical variables with the frame rule, which can predicate only about them. In fact, the logical
frame rule (on the left) immediately follows from its semantic version in Figure 1 (on the right), the
notion of universal frames (Definition 3.1) and the heap compatibility result in Proposition 4.6:
          fv(R) ⊆ Xl {P} r {Q} P ⊲⊳ R                          𝑅 ∈ F ⊩ {𝑃 } r {𝑄 } 𝑃 ▶◀ 𝑅
                                             (Frame)
                  {P ∗ R} r {Q ∗ R}                                 ⊩ {𝑃 • 𝑅} r {𝑄 • 𝑅}
  This represents one of the main differences between SL and SL+, because we can abandon the
syntactic side condition about modified variables in r. In standard SL, logical variables are used only
Systematic Design of Separation Logics                                                                 19


to refer to and constrain the values of variables before the assignments, in the way we described
before. Instead, in SL+, logical variables are also used to avoid framing with modified variables. To
                                                                    i
see how the axioms change, let us consider the case of {Assign}+ in SL+:
                         {empXp \{x} ∧ x  x′ } x := e {empXp \{x} ∧ x  e[x′ /x]}
   In the precondition, a logical variable is associated with each program variable. However, in the
postcondition, the constraint x  x′ is no longer present because x has been modified. As a result, it
is not possible to constrain the new value of x with a frame, but only its previous value. We notice
that to achieve the same result in the original frame rule, the syntactic side condition is needed,
which is an over-approximation of the actual modified variables and so a source of incompleteness.
Instead, SL+ can capture exactly when a variable is actually modified: if the variable x is actually
modified, we lose the ability to constrain x in the postcondition, because there is no logical variable
that can serve as an alias to x for framing. Conversely, if the program does not modify any variable,
each relation with logical variables is preserved. As discussed in Section 4, we observe that the
above Frame rule is also valid for under-approximation, since the framing depends solely on the
direction of the analysis and not on its orientation; consequently, the same reasoning applies to
ISL+, which will be introduced in the next section. To highlight the potential of our approach, we
show that SL+ allows to derive more triples than SL.
                    1
  Example 5.1 (⊢SL+ is more expressive than SL). The (forward, over-approximation) valid triple
                            {x ↦→ _} (false?; x := [y]) + (true?; skip) {x ↦→ _}
                                            1
discussed in Section 1 can be derived in ⊢SL+ but not in classical SL (see Example E.1 for details).
  Vice versa, it can be shown that any SL derivation can be rephrased using SL+ inference rules—
                                                                              i
roughly, all SL axioms can be derived from the ones in SL+ by using {Exists}+ , while the frame
                                                                 i
rule of SL can be recovered from the one in SL+ by using {Cons}+ .
   Different memory models. As suggested by Raad et al. [2020], we make explicit the proof system
for over-approximation in the memory model 2. The only difference between the proof systems
 1          2                                                                                   1
⊢𝑆𝐿+ and ⊢𝑆𝐿+ is the first row of Figure 2, involving the axioms for deallocation ({Free}+ and
         2                                                            2
{Free2}+ ) and for the reallocation of deallocated locations ({Alloc2}+ ). All the other rules remain
identical. Note that, for the memory model 2, the systematic design would produce one single
axiom for x := alloc(), whose pre- and postconditions for the two distinct cases—new allocation or
reallocation—are indexed by logical variables, according to Theorem 4.8 (cf. the proof of Theorem 5.1,
in Appendix). However, in Figure 2 we list one separate axiom for each case to improve readability.
   Different approximations. A distinctive feature of our proof system is that axioms are independent
                                                                                        1
of the sense of approximation. This can be seen below, by comparing rule {Free}+ (on the left),
whose precondition requires x ↦→ z′ , instead of x ↦→ _ like SL rule does (on the right):
               {empXp ∗ x ↦→ z′ } free(x) {empXp }                {x ↦→ _} free(x) {emp}
   In SL, the value pointed to by x is irrelevant. This is because we can always shrink the precondi-
tion and select a subset of the possible values. Instead, in SL+, we require x to point to a logical
                                           i               i
variable z′ . By using the rule of {Exists}+ and {Frame}+ , it is possible to derive the same axiom of
SL. On the other hand, it turns out that our axioms are valid both for over- and under-approximation,
allowing a unique set of axioms for both senses of approximation (see Section 5.2 for more details).
                                      2         i          i        i               2
The same applies for rules {Free2}+ , {Store}+ , {Load}+ , {Alloc}+ and {Alloc2}+ .
20                                                                                                            Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


                      2                                                                        1                                          2
          [Alloc2] +                                                                    [Free1] +                               [Free2] +


          [empXp ∗ l′ ̸↦→] x := alloc() [empXp \{x} ∗ l′ ↦→ z′ ∧ x = l′ ]               [empXp ∗ x ↦→ z′ ] free(x) [empXp ]     [empXp ∗ x ↦→ z′ ] free(x) [empXp ∗ x ̸↦→]
                               2                                                   2                                                 2
                     [FreeEr3] +                                         [LoadEr3] +                                      [StoreEr3] +

                     [empXp ∗ x ̸↦→] free(x) [empXp ∗ x ̸↦→]             [empXp ∗ y ̸↦→] x := [y] [empXp ∗ y ̸↦→]         [empXp ∗ x ̸↦→] [x] := y [empXp ∗ x ̸↦→]
                                       i                                                                     i                            i
                             [Assign] +                                                             [Assume] +                   [Error] +


                             [empXp \{x} ∧ x = x′ ] x := e [empXp \{x} ∧ x = e[x′ /x]]              [empXp ] b? [empXp ∧ b]      [empXp ] error() [empXp ]
            i                                                        i                                                                        i
     [Alloc] +                                             [Load] +                                                                [Store] +


     [empXp ] x := alloc() [empXp \{x} ∗ x ↦→ z′ ]         [empXp ∗ y ↦→ z′ ] x := [y] [empXp \{𝑥 } ∗ y ↦→ z′ ∧ x = z′ ]           [empXp ∗ x ↦→ z′ ] [x] := y [empXp ∗ x ↦→ y]
                 i                                                              i                                                         i
      [FreeEr1] +                                                [LoadEr1] +                                                  [StoreEr1] +


      [empXp ∗ x  null] free(x) [empXp ∗ x  null]              [empXp ∗ y  null] x := [y] [empXp ∗ y  null]               [empXp ∗ x  null] [x] := y [empXp ∗ x  null]
                                i                                                   i                                                 i
                     [FreeEr2] +                                         [LoadEr2] +                                      [StoreEr2] +


                     [empXp ∗ x ↦→ ̸̸ ] free(x) [empXp ∗ x ↦→ ̸̸ ]       [empXp ∗ y ↦→ ̸̸ ] x := [y] [empXp ∗ y ↦→ ̸̸ ]   [empXp ∗ x ↦→ ̸̸ ] [x] := y [empXp ∗ x ↦→ ̸̸ ]


     Fig. 3. ISL+: Synthesized axioms for forward incorrectness analysis in both memory models i ∈ {1, 2}.

     The following theorem guarantees that SL+ is sound and relative complete for loop-free programs.
  Theorem 5.1 (SL+ Sound and Relative Complete for Loop-Free Programs). The proof system
SL+ (sketched in Figure 2) is sound. Moreover, for loop-free programs, it is also relative complete.
  Remark 2. We want to note that, in line with [Calcagno et al. 2007, §3] soundness and relative
completeness results do not account for abort state as it is not expressible in the assertion language.

5.2      Design of ISL+
In this section, we focus on proof systems for forward under-approximation, i.e., subject to clo-
                   ↔
                   ↔ , 𝜌→→ , and 𝜌 →   ·
sure operators 𝜌 exists  frame        cons from Table 4. Consistently with the principles of under-
approximation logics [O’Hearn 2020; Raad et al. 2020, 2022], we adopt semantics that explicitly
account for errors, where the flags ok and er track, respectively, normal and erroneous terminations
in the postcondition. While O’Hearn [2020] and later works [Raad et al. 2020, 2022, 2023] rely on
two different semantics, one accounting for normal termination and one for erroneous termination,
here we follow the alternative exploited by Bruni et al. [2023] and also used in other works [Ascari
et al. 2025] where the domain is enriched with such flags, i.e., {𝑜𝑘, 𝑒𝑟 } × Mi . In this way, the only
difference between the semantics functions of SL and ISL is the treatment of errors: while SL returns
the abort state, ISL returns the whole state tagged as 𝑒𝑟 . As in the previous section, we present
slightly different semantics J·KISL                        i                      i
                                 i : Reg → {𝑜𝑘, 𝑒𝑟 } × M → ℘({𝑜𝑘, 𝑒𝑟 } × M ) depending on the
memory model i ∈ {1, 2}. Both are formalised in Figure 7 for readers’ convenience.7 Finally, we lift
both definitions to sets of states by union as usual. Note that the semantics J·KISL2 is the functional
version of ISL relational semantics [Raad et al. 2020]. For readability, in proof systems that deal
with explicit error handling, we color assertions in green for states tagged with 𝑜𝑘, in red if tagged
with 𝑒𝑟 , and in blue when they can be both.
  Underspecified behaviour. Examining the ISL proof system [Raad et al. 2020] and its semantics, we
can identify some underspecification glitches: no axiom accounts for the execution of a command
7We assume that error states are propagated during the computation, i.e., we let JrKISL 𝑒𝑟 : (𝑠, ℎ) ≜ {𝑒𝑟 : (𝑠, ℎ) }.
                                                                                    i
Systematic Design of Separation Logics                                                                                           21


that presupposes a location to be allocated in an initially empty heap. For example, in the deallocation
command, we can identify five minimal pre on the heap under which the command may be executed:
     (1) 𝑠 (x) = 𝑛𝑢𝑙𝑙,                            (2) ℎ(𝑠 (x)) = ⊥,                            (3) ℎ(𝑠 (x)) ∈ V,
     (4) 𝑠 (x) ∈ V \ L,                           (5) 𝑠 (x) ∈ L \ 𝑑𝑜𝑚(ℎ).
   ISL covers (1)—(3) via ‘FreeNull’, ‘FreeEr’ and ‘Free’. Case (4) can be readily prevented by
an appropriate type system. Case (5) is problematic: although x is currently not allocated, it
may appear in a future heap extension through framing, potentially leading to an unsound
triple. In separation logic, such "permanently absent" locations can be expressed via separat-
ing implication −∗ [Ishtiaq and O’Hearn 2001; O’Hearn and Pym 1999]. The assertion P −∗ Q
is satisfied by those memories that, if extended with a disjoint part where P holds, then Q
will hold in the extended heap. Accordingly, the axiom that captures case (5) can be stated as
[(x ↦→ v ∨ x ̸↦→) −∗ false] free(x) [(x ↦→ v ∨ x ̸↦→) −∗ false], which asserts that whenever we use a
frame with x ↦→ v or x ̸↦→, we obtain a triple with both pre- and postcondition false. Since we only
need the special case P −∗ false, we avoid adding full −∗ by extending heaps with a marker ⊠ for
reserved locations: if ℎ(𝑙) = ⊠, then 𝑙 is absent now and remains absent in all future extensions. We
capture this with a new assertion x ↦→               ̸̸ , which composes as expected (e.g., x ↦→                 ̸̸ ∗x ↦→ v ≡ false),
obtaining the axiom [x ↦→          ̸̸ ] free(x) [x ↦→     ̸̸ ] for the case (5). Although x ↦→    ̸̸ resembles x ̸↦→, they have
different meanings. The assertion x ̸↦→ denotes deallocated locations that may be reallocated; it is
necessary in the memory model 2 since such states are directly used in its semantics. By contrast,
x ↦→  ̸̸ forbids the location from ever appearing and is needed only when reasoning with explicit
error handling, to avoid unsoundness. If errors are not handled explicitly, all errors collapse to
abort (which is not expressible in the assertion language), making x ↦→                              ̸̸ superfluous.
   A related solution [Carrott et al. 2025] introduces an exit condition miss(𝑙) and enforces sound-
ness via a side condition forbidding framing with 𝑙. In contrast, x ↦→                  ̸̸ is a compositional assertion (e.g.,
x ↦→     ̸̸ ∗y ↦→ ̸̸ is meaningful), while miss(𝑙) is an exit label that does not support such a combination.

   Proof system. In Figure 3 we outline the axioms of the proof system ISL+, where we characterize
every pre- and postcondition with the assertion language (3), here extended with x ↦→  ̸̸ (see Figure
9 in Appendix for the full proof system). As before, rule names are annotated with their reference
                                 i
memory model. We denote by ⊢ISL+ the proof system related to the memory model i.

   Frame rule and logical variables. As previously discussed, the frame rule is independent from the
sense of the analysis, thereby ISL+ uses the same frame rule of SL+ and exploits logical variables
in the same manner, allowing for deriving more triples w.r.t. ISL. In the next example, we show a
triple derivable in ISL+ but not in ISL.
                        2
  Example 5.2 (⊢ISL+ is more expressive than ISL). As discussed in Section 1, Eq. (2), the triple
                                                                          2
[y ↦→ v] x := alloc(); free(y); x := [y] [y ̸↦→ ∗ x ↦→ _] is provable in ⊢ISL+ but not in ISL (see Ex. E.2).

   Different memory models. To the best of our knowledge, this work presents the first axiomatization
of a separation logic for under-approximation that dispenses with the negative heap assertion,
originally introduced by Raad et al. [2020] to guarantee soundness. We argue that the negative
heap assertion is not required in general to define an under-approximation logic; rather, it becomes
necessary when using the standard frame rule of SL. Here, instead, we take another point of view
by defining a new frame rule where the semantic preservation is exactly captured (Theorem 4.1
and Theorem 4.2). This implies that frames that would lead to an over-approximation are denied by
Definition 4.2. Indeed, derivations like (6) are not possible in ISL+ as shown in the next example.
22                                                                        Roberto Bruni, Lorenzo Gazzella, and Roberta Gori

                      1
   Example 5.3 (⊢ISL+ forbids wrong framing). Let us consider the triple [x ↦→ _] free(x) [emp],
used as motivation for the introduction of the assertion x ̸↦→ in ISL. The classical frame rule (1) would al-
low the framing with the assertion x ↦→ _, leading to derive the unsound triple [false] free(x) [x ↦→ _]
(see derivation (6)). Instead, in ISL+ such framing is prevented by the condition 𝑃 ⊲⊳ 𝑅.
   Different approximations. We highlight that the only difference between SL+ and ISL+ is the
axioms for explicitly handling error termination: every axiom for normal termination remains
the same. Notably, this is because we consider different semantics. Apart from this, our approach
allows to reuse the same axioms for both over- and under-approximation.
   Theorem 5.2 (ISL+ Sound and Relative Complete for Loop-Free Programs). The proof system
ISL+ (sketched in Figure 3) is sound. Moreover, for loop-free programs, it is also relative complete.
   In the case of under-approximation, we can also extend the completeness result to any program
r by taking advantage of the reachability requirement of the postcondition.
   Theorem 5.3 (State-wise completeness). Given a program r and two states (𝜖 : (𝑠, ℎ)) and
(𝜖 : (𝑠 ′, ℎ ′ )) such that, (𝜖 : (𝑠 ′, ℎ ′ )) ∈ JrKISL
                                                    i (𝜖 : (𝑠, ℎ)), for every assertion P such that (𝑠, ℎ) ∈ ⦃P⦄
                                                                          i
there exists an assertion Q such that (𝑠 ′, ℎ ′ ) ∈ ⦃Q⦄ and ⊢ISL+ [P] r [Q] is provable.
  It is worth mentioning here the relatively complete proof system for incorrectness separation
logic defined by Lee and Nakazawa [2024]. Their axioms, however, require global preconditions,
which violate the locality principle and can harm scalability and compositionality.
   On the footprint theorem. Let us consider the footprint relation foot(·) defined by Raad et al.
[2020], where foot(r) describes the minimal state needed for some execution of r.8 This means that
if ((𝑠, ℎ), (𝑠 ′, ℎ ′ )) ∈ foot(r), then ℎ only contains locations accessed during the execution of r and
its execution on the state (𝑠, ℎ) terminates in the state (𝑠 ′, ℎ ′ ). When c ∈ Atom, we observe some
                                                       ·
correspondences between foot(c) and Axioms→           JcK
                                                          . In particular, if two states are related by foot(c),
then there is an axiom whose precondition contains the initial state and the postcondition contains
the final state (independently from the values of logical variables). Formally,
                                                                      ·             ·
         ((𝑠, ℎ), (𝑠 ′, ℎ ′ )) ∈ foot(c) =⇒ ∃(𝑃, c, 𝑄) ∈ 𝜌 exists
                                                           → (Axioms→ ).(𝑠, ℎ) ∈ 𝑃, (𝑠 ′ , ℎ ′ ) ∈ 𝑄
                                                                    JcK
                                                                                                                        (9)

   We point out that, while the relation foot(c) must be given ad hoc for the specific semantics we
                                            ·
are considering, the set of axioms Axioms→ JcK
                                               can be found by minimality considerations.
   Let us also consider the relation frame(r) ≜ {(𝜎𝑝 • 𝜎𝑟 , 𝜎𝑞 • 𝜎𝑟 ) | (𝜎𝑝 , 𝜎𝑞 ) ∈ 𝑅} for which Raad
et al. [2020, Theorem 2 (Footprint)] proved that ∀c.JcKISL
                                                         2 = frame(foot(c)). In other terms, the
semantics of a program is given by every possible framing of the footprint of the command c. A
similar correspondence to (9) can be observed if we also consider the closure operator frame:
                                                                  ·           ·             ·
 ((𝑠, ℎ), (𝑠 ′, ℎ ′ )) ∈ frame(foot(c)) =⇒ ∃(𝑃, c, 𝑄) ∈ 𝜌 frame
                                                          →         → (Axioms→ ).(𝑠, ℎ) ∈ 𝑃, (𝑠 ′ , ℎ ′ ) ∈ 𝑄.
                                                                ◦ 𝜌 exists   JcK

   Although the Footprint Theorem secures an elegant property, there is no corresponding logical
principle in ISL. In fact, some states in frame(foot(c)) cannot be derived in ISL due to the impossi-
bility of applying the frame rule because of the side condition (see (2), again). On the other hand,
                                                 →·
conditions imposed by the closure operator 𝜌 frame    and then by the rule of frame of the semantic
proof system are translated as a one-to-one correspondence in the logical proof system ISL+. This
means that (up to the expressiveness of the assertion language), the frame rule of ISL+ is complete.
8 The original definition takes into account also exit conditions that here we omit for the sake of presentation.
Systematic Design of Separation Logics                                                                                  23


5.2.1 Design of CISL+. CISL [Raad et al. 2022] is a general framework for multiple incorrectness
analysis in concurrent settings (e.g., detecting memory safety bugs, data races on shared memory,
deadlock issues) and avoids the syntactic side-condition by adopting a memory model where sepa-
ration ranges uniformly over store and heap. Accordingly, a slightly different notion of separating
conjunction is used:
              𝑃⊙
               • 𝑄 ≜ {(𝑠𝑝 • 𝑠𝑞 , ℎ𝑝 • ℎ𝑞 ) | (𝑠𝑝 , ℎ𝑝 ) ∈ 𝑃 ∧ (𝑠𝑞 , ℎ𝑞 ) ∈ 𝑄 ∧ 𝑠𝑝 #𝑠𝑞 ∧ ℎ𝑝 #ℎ𝑞 }.

Applying our systematic design methodology to CISLDC (i.e. the instance of CISL for detecting
                                                                                      →
                                                                                      →
memory safety bugs) yields the logic CISL+, that is analogous to ISL+, but where 𝜌 frame  is defined
in terms of ⊙• rather than •. Although CISL+ is similar to ISL+ , its axioms reflect the different
                                                                  9

definition of the separating conjunction. For example, letting ⊛ be the assertional counterpart of ⊙
                                                                                                   •
(i.e., ⦃P ⊛ Q⦄ ≜ ⦃P⦄ ⊙ • ⦃Q⦄), the axiom for allocation can be written as follows:


                                  [x ↦→ z′ ] x := alloc() [∃l.∃v.x ↦→ l ⊛ l ↦→ v]
The axiom above itself provides an example in which CISL+ is more expressive than CISLDC , which
is intrinsically incomplete, as discussed in Section 1 (see Issue #3). Notably, in the extended model
M2 with explicit deallocation considered by CISL, the side condition of our frame rule P ⊲⊳ R is
vacuously true. However, thanks to that side condition, we can also apply the CISL settings to the
classical model M1 , in the same manner described in Section 5.2.

6   Systematic Design of Backward Separation Logics
Our methodology is not limited to reconstructing and refining existing logics; it also enables the
synthesis of entirely new ones. In this section, we address the design of backward separation logics,
for any sense of approximation and any memory model. While a backward, under-approximation
separation logic, called SepSIL, was recently introduced in [Ascari et al. 2025] for M2 , the over-
approximation variants presented here are entirely novel contributions of this work. For simplicity,
as reference semantics we consider J·KSL               i         i
                                        i : Reg → M → ℘(M ⊎ {abort}), i.e., without explicit er-
ror handling (see Figure 6 in Appendix). The resulting logic SIL+, for backward under-approximation
and of the logic NC+ for backward over-approximation exploit the closure operators already pre-
                              ↔
                              ↔ , 𝜌← ← , and 𝜌 ←  ·                    ↔
                                                                       ↔         ←
                                                                                 ←             ←·
sented in Table 4, namely 𝜌 exists   frame       cons for SIL+, and 𝜌 exists , 𝜌 frame , and 𝜌 cons for NC+.


  We highlight that NC+ and SIL+ share a unique set of axioms, valid for both senses of approxi-
mation. This is evident by comparing the axioms for SIL+ in Figure 4 with those for NC+ in (the
topmost part of) Figure 5, which carry the same pre- and postconditions except for the use of
surrounding brackets: SIL+ triples are written using ⟨⟨·⟩⟩, while NC+ triples using (·). In these
axioms, both pre- and postconditions are expressed using the assertion language defined in (3).
  As an illustrative example, consider the axiom for allocation:

                    ⟨⟨empXp \{x} ∧ x′ = l′ ⟩⟩ x := alloc() ⟨⟨empXp \{x} ∧ x = x′ ∗ x ↦→ z′ ⟩⟩
  The axiom is written in SIL+ syntax, but also valid for NC+. Due to the locality principle, the pre-
and postconditions of the conclusion are restricted to the footprint of the allocated cell, i.e., to the
heap fragment directly affected by the allocation. In contrast with SL+ and ISL+, the analysis of NC+
and SIL+ is best read backward: the axiom is applicable to a generic heap-minimal postcondition.

9 Technically, CISL also exploits parallel composition of commands r ∥ r; being orthogonal to our study, we leave the rules

for handling parallel composition in Figure 10 in Appendix.
24                                                                                                           Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


               2                                                                                    1                                          2
     ⟨⟨Alloc2⟩⟩ +                                                                          ⟨⟨Free1⟩⟩ +                                ⟨⟨Free2⟩⟩ +


     ⟨⟨empXp \{x} ∧ x′ = l′ ∗ l′ ̸↦→⟩⟩ x := alloc() ⟨⟨empXp \{x} ∧ x = x′ ∗ x ↦→ z′ ⟩⟩     ⟨⟨empXp ∗ x ↦→ z′ ⟩⟩ free(x) ⟨⟨empXp ⟩⟩    ⟨⟨empXp ∗ x ↦→ z′ ⟩⟩ free(x) ⟨⟨empXp ∗ x ̸↦→⟩⟩
                    i                                                                               i                                                         i
          ⟨⟨Alloc⟩⟩ +                                                                    ⟨⟨Assign⟩⟩ +                                               ⟨⟨Assume⟩⟩ +


          ⟨⟨empXp \{x} ∧ x′ = l′ ⟩⟩ x := alloc() ⟨⟨empXp \{x} ∧ x = x′ ∗ x ↦→ z′ ⟩⟩      ⟨⟨empXp \{x} ∧ x′ = e⟩⟩ x := e ⟨⟨empXp \{x} ∧ x = x′ ⟩⟩    ⟨⟨empXp ∧ b⟩⟩ b? ⟨⟨empXp ⟩⟩
                                 i                                                                                    i
                        ⟨⟨Load⟩⟩ +                                                                           ⟨⟨Store⟩⟩ +


                        ⟨⟨empXp \{x} ∧ x′ = z′ ∗ y ↦→ z′ ⟩⟩ x := [y] ⟨⟨empXp \{x} ∧ x = x′ ∗ y ↦→ z′ ⟩⟩      ⟨⟨empXp ∗ x ↦→ z′ ⟩⟩ [x] := y ⟨⟨empXp ∗ x ↦→ y⟩⟩


 Fig. 4. SIL+: Synthesized axioms for backward incorrectness analysis in both memory models i ∈ {1, 2}.

6.1       Design of SIL+
The goal of backward under-approximation logics, such as SepSIL, is to expose some initial states
that have at least one terminating run in one state that satisfies the given postcondition 𝑄. Figure 4
just showcases the axioms of SIL+, but the full proof system can be found in Appendix, Figure 11.
Even if SepSIL is as expressive as SIL+, we observe that some axioms of SepSIL (see [Ascari et al.
2025, Figure 5]) were defined globally, whereas our methodology enforces the introduction of local
axioms only. As a simple instance, compare the global assignment axiom in SepSIL—a.k.a., Hoare’s
assignment axiom [Hoare 1969], as opposed to Floyd’s axiom (4)—with SIL+ local axiom:


                                             (SepSIL)                                                                                                                     (SIL+)
 ⟨⟨Q [e/x]⟩⟩ x := e ⟨⟨Q⟩⟩                                               ⟨⟨empXp \{x} ∧ x′ = e⟩⟩ x := e ⟨⟨empXp \{x} ∧ x = x′ ⟩⟩

  Our method leads to exploit logical variables to disregard the idle part of the postcondition,
which can be added at a later time using the frame rule. More precisely, using logical variables,
we can rewrite the SepSIL axiom for assignment as ⟨⟨Q [x′ /x] ∗ x′  e⟩⟩ x := e ⟨⟨Q [x′ /x] ∗ x  x′ ⟩⟩.
The local axiom of SIL+ lifts this approach to the whole set of program variables empXp in order to
remove the idle frame Q [x′ /x] from the picture. The same difference can be observed by looking at
the axioms for x := e, b?, and x := [y], where SepSIL still considers global post rather than local ones.
Finally, thanks to universal frames, SIL+ can be applied to the memory model without reallocation.

6.2       Design of NC+
The goal of backward over-approximation logics, such as NC, is to characterise, for a given post-
condition 𝑄, a precondition that covers all initial states with at least one terminating run in one
state that satisfies 𝑄. Equivalently, this property ensure that no state in 𝑄 is reachable from out-
side 𝑃. Although necessary condition triples were already introduced more than a decade ago by
Cousot et al. [2013], a proof system for establishing such triples for either regular programs or
heap-manipulating ones had remained missing until now. Thanks to our methodology, such a proof
system can be straightforwardly obtained from the common axioms of backward separation logic
by simply adding the structural inference rules and the right consequence rule, since in this setting
we are over-approximating the preconditions. The resulting proof system is listed in Fig. 5 and it is
parametric to the underlying memory model.
   The next example illustrates how backward analyses can largely differ from forward ones.
                                                                          i                                                    i
   Example 6.1. Consider the triples ⊢SIL+ ⟨⟨x ↦→ 1⟩⟩ r ⟨⟨Q⟩⟩ and ⊢NC+ (x ↦→ z′ ) r (Q) where r =
(free(x) + skip); y := [x] and Q = x ↦→ z′ ∧ y > 0 ∧ z′ < 3 is a correctness specification. The SIL+
triple is only valid for backward, under-approximation analysis and asserts that any initial state
Systematic Design of Separation Logics                                                                                                                                             25


            2                                                                                  1                                             2
    (Alloc2)+                                                                          (Free1)+                                       (Free2)+


    (empXp \{x} ∧ x′ = l′ ∗ l′ ̸↦→) x := alloc() (empXp \{x} ∧ x = x′ ∗ x ↦→ z′ )      (empXp ∗ x ↦→ z′ ) free(x) (empXp )            (empXp ∗ x ↦→ z′ ) free(x) (empXp ∗ x ̸↦→)
                i                                                                            i                                                             i
         (Alloc)+                                                                    (Assign)+                                                   (Assume)+


         (empXp \{x} ∧ x′ = l′ ) x := alloc() (empXp \{x} ∧ x = x′ ∗ x ↦→ z′ )       (empXp \{x} ∧ x′ = e) x := e (empXp \{x} ∧ x = x′ )         (empXp ∧ b) b? (empXp )
                             i                                                                                      i
                     (Load)+                                                                               (Store)+


                     (empXp \{x} ∧ x′ = z′ ∗ y ↦→ z′ ) x := [y] (empXp \{x} ∧ x = x′ ∗ y ↦→ z′ )           (empXp ∗ x ↦→ z′ ) [x] := y (empXp ∗ x ↦→ y)

                                         i                                       i                        i                       i
                                 (Frame)+                               (Exists)+                  (Disj)+                   (Seq)+
                                 fv(R) ⊆ Xl (P) r (Q) Q ⊲⊳ R            (P) r (Q) X ⊆ Xl            ∀𝑖 ∈ 𝐼 .(Pi ) r (Qi )    (P) r1 (S) (𝑆) r2 (Q)
                                        (P ∗ R) r (Q ∗ R)                (∃X.P) r (∃X.Q)           (∪i∈I Pi ) r (∪i∈I Qi )        (P) r1 ; r2 (Q)

                                                       i                                            i                   i
                                               (Cons)+                                  (Iterate)+        (Choice)+
                                               P′ ⇒ P      (P′ ) r (Q ′ )   Q ⇒ Q′       (Q) r (Q)        ∀𝑖 ∈ {1, 2}.(P) ri (Q)
                                                            (P) r (Q)                   (Q) r∗ (Q)           (P) r1 + r2 (Q)


Fig. 5. NC+: Synthesized proof system for backward correctness analysis in both memory models i ∈ {1, 2}.

satisfying x ↦→ 1 has a terminating execution in Q. The NC+ triple is only valid for backward, over-
approximation analysis and asserts that only initial states that satisfy x ↦→ z′ could have a terminating
execution in Q. Neither of the triples specifies which final states are reachable.

7    Conclusions and future work
We presented a methodology for designing separation logics, grounded in collecting semantics, the
locality principle, and closure operators. By combining semantic closure reasoning with universal
frames over logical variables, the method synthesizes sound and expressive proof systems for
forward/backward and over/under-approximate analyses across different memory models. The
approach unifies, generalizes, and improves SL, ISL, CISL, and SepSIL, and offers a disciplined way
to deal with language extensions and to derive new logics with limited additional effort. At the core
of the approach lies a closure-based characterization of valid triples, which allows local axioms to
be derived as minimal elements from the program semantics. The main outcomes of our systematic
design are summarized in Table 2. Because the treatment is semantic, the approach is fully general:
beyond the two memory models studied, it applies to any semantics and evaluation model. Moreover,
the proof systems introduced for the forward analysis use forward axioms (i.e., axioms applicable
to any precondition) to highlight the duality of the analysis, yet by disregarding this duality and
focusing on over-approximations, one can still define a Hoare-style assignment axiom incorporating
the principle of locality, even when logical variables are employed. We believe our work contributes
to a deeper understanding of the semantic foundations of separation logics, also offering practical
tools for the scalable and modular verification of heap-manipulating programs.
   Our methodology has been validated in two ways: by a prototype tool developed as part of a
master’s course project, which is able to perform forward reasoning, and by the mechanization
of several core results in Isabelle/HOL. However, they were not the final goal. A more promising
direction is to instrument existing verification tools with our closure-guided principle for deriving
axioms. By largely reusing, or only lightly extending, current codebases, one can obtain a principled
selection of axiom sets and adapt bi-abduction procedures to match the direction and sense of the
analysis (forward vs. backward), thereby broadening both expressiveness and applicability. In this
setting, the ability to share axioms across different analyses, together with the notion of universal
frames, can play a key role in integrating heterogeneous analyses within a unified reasoning
framework and in deriving more expressive code summaries. From this perspective, our framework
26                                                                      Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


finds potential applications in improving the capabilities of tools such as Infer [Distefano et al.
2019], Pulse [Le et al. 2022] and Iris [Jung et al. 2018; Vistrup et al. 2025].
   Future work also includes the investigation of richer assertion languages, concurrency beyond
heap safety, and the extension of bi-abduction to backward reasoning. While in this paper the
focus is mostly on the systematic design of local axioms for atomic commands, the next steps
will be to refine the concept of minimality further and to see if it can be incorporated within the
calculational approach of Cousot [2024]. We also plan to study the exploitation of logical variables
within probabilistic separation logics [Barthe et al. 2020; Batz et al. 2019; Zilberstein et al. 2026]
and hyper Hoare logics [Dardinier and Müller 2024], along the lines of Cousot and Wang [2025].

8    Data-Availability Statement
We have developed two supporting tools based on our findings in the paper.
   A prototype implementing the core ideas of SL+ and ISL+ was developed within a master’s
course project. Its objective was to show that our methodology can effectively support both over-
and under-approximation analyses, and that logical variables can be practically integrated.
   Moreover, the crucial steps of our systematic design methodology have been mechanized in
Isabelle/HOL to gain confidence in their correctness and to verify that the locality principle was
correctly addressed in our logical axioms.
   Both artifacts constitute just proof of concepts and they are not intended to achieve competitive
performance, precision, or usability.

Acknowledgments
The research has been supported by the Italian Ministero dell’Università e della Ricerca under Grant
No. P2022HXNSC, PRIN 2022 PNRR – Resource Awareness in Programming: Algebra, Rewriting, and
Analysis.

References
Peter Aczel. 1977. An Introduction to Inductive Definitions. In Handbook of Mathematical Logic, John Barwise (Ed.).
   North–Holland, Amsterdam, Chapter 7, 739–782.
Krzysztof R. Apt and Ernst-Rüdiger Olderog. 2019. Fifty years of Hoare’s logic. Formal Aspects Comput. 31, 6 (2019), 751–807.
   doi:10.1007/S00165-019-00501-3
Flavio Ascari, Roberto Bruni, Roberta Gori, and Francesco Logozzo. 2025. Revealing Sources of (Memory) Errors via
   Backward Analysis. Proc. ACM Program. Lang. 9, OOPSLA1 (2025), 1321–1348. doi:10.1145/3720486
Gilles Barthe, Justin Hsu, and Kevin Liao. 2020. A probabilistic separation logic. Proc. ACM Program. Lang. 4, POPL (2020),
   55:1–55:30. doi:10.1145/3371123
Kevin Batz, Benjamin Lucien Kaminski, Joost-Pieter Katoen, Christoph Matheja, and Thomas Noll. 2019. Quantitative
   separation logic: a logic for reasoning about probabilistic pointer programs. Proc. ACM Program. Lang. 3, POPL (2019),
   34:1–34:29. doi:10.1145/3290347
Richard Bornat, Cristiano Calcagno, and Hongseok Yang. 2005. Variables as Resource in Separation Logic. In Proceedings
   of the 21st Annual Conference on Mathematical Foundations of Programming Semantics, MFPS 2005, Birmingham, UK,
   May 18-21, 2005 (Electronic Notes in Theoretical Computer Science, Vol. 155), Martín Hötzel Escardó, Achim Jung, and
   Michael W. Mislove (Eds.). Elsevier, 247–276. doi:10.1016/J.ENTCS.2005.11.059
Roberto Bruni, Roberto Giacobazzi, Roberta Gori, and Francesco Ranzato. 2023. A Correctness and Incorrectness Program
   Logic. J. ACM 70, 2 (2023), 15:1–15:45. doi:10.1145/3582267
Cristiano Calcagno, Dino Distefano, Jérémy Dubreil, Dominik Gabi, Pieter Hooimeijer, Martino Luca, Peter W. O’Hearn,
   Irene Papakonstantinou, Jim Purbrick, and Dulma Rodriguez. 2015. Moving Fast with Software Verification. In NASA
   Formal Methods - 7th International Symposium, NFM 2015, Pasadena, CA, USA, April 27-29, 2015, Proceedings (Lecture
   Notes in Computer Science, Vol. 9058), Klaus Havelund, Gerard J. Holzmann, and Rajeev Joshi (Eds.). Springer, Cham, 3–11.
   doi:10.1007/978-3-319-17524-9_1
Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. 2009. Compositional shape analysis by means
   of bi-abduction. In Proceedings of the 36th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
Systematic Design of Separation Logics                                                                                     27


   POPL 2009, Savannah, GA, USA, January 21-23, 2009, Zhong Shao and Benjamin C. Pierce (Eds.). ACM, New York, NY, US,
   289–300. doi:10.1145/1480881.1480917
Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. 2011. Compositional Shape Analysis by Means
   of Bi-Abduction. J. ACM 58, 6 (2011), 26:1–26:66. doi:10.1145/2049697.2049700
Cristiano Calcagno, Peter W. O’Hearn, and Hongseok Yang. 2007. Local Action and Abstract Separation Logic. In 22nd
   IEEE Symposium on Logic in Computer Science (LICS 2007), 10-12 July 2007, Wroclaw, Poland, Proceedings. IEEE Computer
   Society, 366–378. doi:10.1109/LICS.2007.30
Qinxiang Cao, Santiago Cuéllar, and Andrew W. Appel. 2017. Bringing Order to the Separation Logic Jungle. In Programming
   Languages and Systems - 15th Asian Symposium, APLAS 2017, Suzhou, China, November 27-29, 2017, Proceedings (Lecture
   Notes in Computer Science, Vol. 10695), Bor-Yuh Evan Chang (Ed.). Springer, 190–211. doi:10.1007/978-3-319-71237-6_10
Pedro Carrott, Sacha-Élie Ayoun, and Azalea Raad. 2025. Compositional Bug Detection for Internally Unsafe Libraries: A
   Logical Approach to Type Unsoundness. In 39th European Conference on Object-Oriented Programming, ECOOP 2025,
   June 30 to July 2, 2025, Bergen, Norway (LIPIcs, Vol. 333), Jonathan Aldrich and Alexandra Silva (Eds.). Schloss Dagstuhl -
   Leibniz-Zentrum für Informatik, 5:1–5:28. doi:10.4230/LIPICS.ECOOP.2025.5
Stephen A. Cook. 1978. Soundness and Completeness of an Axiom System for Program Verification. SIAM J. Comput. 7, 1
   (1978), 70–90. doi:10.1137/0207005
Patrick Cousot. 1978. Méthodes itératives de construction et d’approximation de points fixes d’opérateurs monotones sur un
   treillis, analyse sémantique des programmes. https://tel.archives-ouvertes.fr/tel-00288657
Patrick Cousot. 2021. Principles of Abstract Interpretation. MIT Press, Cambridge, MA.
Patrick Cousot. 2024. Calculational Design of [In]Correctness Transformational Program Logics by Abstract Interpretation.
   Proc. ACM Program. Lang. 8, POPL (2024), 175–208. doi:10.1145/3632849
Patrick Cousot and Radhia Cousot. 1977. Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs
   by Construction or Approximation of Fixpoints. In Conference Record of the Fourth ACM Symposium on Principles of
   Programming Languages, Los Angeles, California, USA, January 1977, Robert M. Graham, Michael A. Harrison, and Ravi
   Sethi (Eds.). ACM, 238–252. doi:10.1145/512950.512973
Patrick Cousot, Radhia Cousot, Manuel Fähndrich, and Francesco Logozzo. 2013. Automatic Inference of Necessary
   Preconditions. In Verification, Model Checking, and Abstract Interpretation, 14th International Conference, VMCAI 2013,
   Rome, Italy, January 20-22, 2013. Proceedings (Lecture Notes in Computer Science, Vol. 7737), Roberto Giacobazzi, Josh
   Berdine, and Isabella Mastroeni (Eds.). Springer, Berlin, Heidelberg, 128–148. doi:10.1007/978-3-642-35873-9_10
Patrick Cousot and Jeffery Wang. 2025. Calculational Design of Hyperlogics by Abstract Interpretation. Proc. ACM Program.
   Lang. 9, POPL (2025), 446–478. doi:10.1145/3704852
Thibault Dardinier and Peter Müller. 2024. Hyper Hoare Logic: (Dis-)Proving Program Hyperproperties. Proc. ACM Program.
   Lang. 8, PLDI (2024), 1485–1509. doi:10.1145/3656437
Edsko de Vries and Vasileios Koutavas. 2011. Reverse Hoare Logic. In Software Engineering and Formal Methods - 9th
   International Conference, SEFM 2011, Montevideo, Uruguay, November 14-18, 2011. Proceedings (Lecture Notes in Computer
   Science, Vol. 7041), Gilles Barthe, Alberto Pardo, and Gerardo Schneider (Eds.). Springer, 155–171. doi:10.1007/978-3-642-
   24690-6_12
Dino Distefano, Manuel Fähndrich, Francesco Logozzo, and Peter W. O’Hearn. 2019. Scaling static analyses at Facebook.
   Commun. ACM 62, 8 (2019), 62–70. doi:10.1145/3338112
Michael J. Fischer and Richard E. Ladner. 1979. Propositional Dynamic Logic of Regular Programs. J. Comput. Syst. Sci. 18, 2
   (1979), 194–211. doi:10.1016/0022-0000(79)90046-1
Robert W. Floyd. 1967. Assigning Meanings to Programs. Proc. of Symposium on Applied Mathematics 19 (1967), 19–32.
   http://laser.cs.umass.edu/courses/cs521-621.Spr06/papers/Floyd.pdf
David Harel, Jerzy Tiuryn, and Dexter Kozen. 2000. Dynamic Logic. MIT Press, Cambridge, MA, USA.
C. A. R. Hoare. 1969. An Axiomatic Basis for Computer Programming. Commun. ACM 12, 10 (1969), 576–580. doi:10.1145/
   363235.363259
Samin S. Ishtiaq and Peter W. O’Hearn. 2001. BI as an Assertion Language for Mutable Data Structures. In Conference Record
   of POPL 2001: The 28th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, London, UK, January
   17-19, 2001, Chris Hankin and Dave Schmidt (Eds.). ACM, 14–26. doi:10.1145/360204.375719
Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars Birkedal, and Derek Dreyer. 2018. Iris from the
   ground up: A modular foundation for higher-order concurrent separation logic. J. Funct. Program. 28 (2018), e20.
   doi:10.1017/S0956796818000151
Thomas Kleymann. 1999. Hoare Logic and Auxiliary Variables. Formal Aspects Comput. 11, 5 (1999), 541–566. doi:10.1007/
   S001650050057
Quang Loc Le, Azalea Raad, Jules Villard, Josh Berdine, Derek Dreyer, and Peter W. O’Hearn. 2022. Finding real bugs in big
   programs with incorrectness logic. Proc. ACM Program. Lang. 6, OOPSLA1 (2022), 1–27. doi:10.1145/3527325
28                                                                        Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


Yeonseok Lee and Koji Nakazawa. 2024. Relative Completeness of Incorrectness Separation Logic. In Programming Languages
   and Systems - 22nd Asian Symposium, APLAS 2024, Kyoto, Japan, October 22-24, 2024, Proceedings (Lecture Notes in Computer
   Science, Vol. 15194), Oleg Kiselyov (Ed.). Springer, Singapore, 264–282. doi:10.1007/978-981-97-8943-6_13
Petar Maksimovic, Caroline Cronjäger, Andreas Lööw, Julian Sutherland, and Philippa Gardner. 2023. Exact Separation
   Logic: Towards Bridging the Gap Between Verification and Bug-Finding. In 37th European Conference on Object-Oriented
   Programming, ECOOP 2023, July 17-21, 2023, Seattle, Washington, United States (LIPIcs, Vol. 263), Karim Ali and Guido
   Salvaneschi (Eds.). Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 19:1–19:27. doi:10.4230/LIPICS.ECOOP.2023.19
Bernhard Möller, Peter W. O’Hearn, and Tony Hoare. 2021. On Algebra of Program Correctness and Incorrectness. In
   Relational and Algebraic Methods in Computer Science - 19th International Conference, RAMiCS 2021, Marseille, France,
   November 2-5, 2021, Proceedings (Lecture Notes in Computer Science, Vol. 13027), Uli Fahrenberg, Mai Gehrke, Luigi
   Santocanale, and Michael Winter (Eds.). Springer, 325–343. doi:10.1007/978-3-030-88701-8_20
Carroll Morgan. 1990. Programming from specifications. Prentice Hall.
Peter W. O’Hearn. 2020. Incorrectness logic. Proc. ACM Program. Lang. 4, POPL (2020), 10:1–10:32. doi:10.1145/3371078
Peter W. O’Hearn and David J. Pym. 1999. The logic of bunched implications. Bull. Symb. Log. 5, 2 (1999), 215–244.
   doi:10.2307/421090
Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. 2001. Local Reasoning about Programs that Alter Data Structures.
   In Computer Science Logic, 15th International Workshop, CSL 2001. 10th Annual Conference of the EACSL, Paris, France,
   September 10-13, 2001, Proceedings (Lecture Notes in Computer Science, Vol. 2142), Laurent Fribourg (Ed.). Springer, 1–19.
   doi:10.1007/3-540-44802-0_1
Oystein Ore. 1943. Combinations of closure relations. Ann. Math. 44, 3 (July 1943), 514. doi:10.2307/1968978
Matthew J. Parkinson. 2010. The Next 700 Separation Logics - (Invited Paper). In Verified Software: Theories, Tools, Experiments,
   Third International Conference, VSTTE 2010, Edinburgh, UK, August 16-19, 2010. Proceedings (Lecture Notes in Computer
   Science, Vol. 6217), Gary T. Leavens, Peter W. O’Hearn, and Sriram K. Rajamani (Eds.). Springer, 169–182. doi:10.1007/978-
   3-642-15057-9_12
Vaughan R. Pratt. 1976. Semantical Considerations on Floyd-Hoare Logic. In 17th Annual Symposium on Foundations of
   Computer Science, Houston, Texas, USA, 25-27 October 1976. IEEE Computer Society, 109–121. doi:10.1109/SFCS.1976.27
Azalea Raad, Josh Berdine, Hoang-Hai Dang, Derek Dreyer, Peter W. O’Hearn, and Jules Villard. 2020. Local Reasoning About
   the Presence of Bugs: Incorrectness Separation Logic. In Computer Aided Verification - 32nd International Conference,
   CAV 2020, Los Angeles, CA, USA, July 21-24, 2020, Proceedings, Part II (Lecture Notes in Computer Science, Vol. 12225),
   Shuvendu K. Lahiri and Chao Wang (Eds.). Springer, Cham, 225–252. doi:10.1007/978-3-030-53291-8_14
Azalea Raad, Josh Berdine, Derek Dreyer, and Peter W. O’Hearn. 2022. Concurrent incorrectness separation logic. Proc.
   ACM Program. Lang. 6, POPL (2022), 1–29. doi:10.1145/3498695
Azalea Raad, Julien Vanegue, Josh Berdine, and Peter W. O’Hearn. 2023. A General Approach to Under-Approximate
   Reasoning About Concurrent Programs. In 34th International Conference on Concurrency Theory, CONCUR 2023, September
   18-23, 2023, Antwerp, Belgium (LIPIcs, Vol. 279), Guillermo A. Pérez and Jean-François Raskin (Eds.). Schloss Dagstuhl -
   Leibniz-Zentrum für Informatik, 25:1–25:17. doi:10.4230/LIPICS.CONCUR.2023.25
Azalea Raad, Julien Vanegue, and Peter W. O’Hearn. 2024. Non-termination Proving at Scale. Proc. ACM Program. Lang. 8,
   OOPSLA2 (2024), 246–274. doi:10.1145/3689720
Mohammad Raza and Philippa Gardner. 2008. Footprints in Local Reasoning. In Foundations of Software Science and
   Computational Structures, 11th International Conference, FOSSACS 2008, Held as Part of the Joint European Conferences on
   Theory and Practice of Software, ETAPS 2008, Budapest, Hungary, March 29 - April 6, 2008. Proceedings (Lecture Notes in
   Computer Science, Vol. 4962), Roberto M. Amadio (Ed.). Springer, Berlin, Heidelberg, 201–215. doi:10.1007/978-3-540-
   78499-9_15
John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In 17th IEEE Symposium on Logic
   in Computer Science (LICS 2002), 22-25 July 2002, Copenhagen, Denmark, Proceedings. IEEE Computer Society, 55–74.
   doi:10.1109/LICS.2002.1029817
Henry Gordon Rice. 1953. Classes of recursively enumerable sets and their decision problems. Transactions of the American
   Mathematical society 74, 2 (1953), 358–366.
Alan Turing. 1949 [1950]. Checking a Large Routine. In Report of a Conference on High Speed Automatic Calculating Machines.
   University of Cambridge Mathematical Laboratory, Cambridge, England, 67–69.
Freek Verbeek, Md Syadus Sefat, Zhoulai Fu, and Binoy Ravindran. 2025. On Extending Incorrectness Logic with Backwards
   Reasoning. Proc. ACM Program. Lang. 9, POPL (2025), 391–415. doi:10.1145/3704850
Lena Verscht and Benjamin Lucien Kaminski. 2025. A Taxonomy of Hoare-Like Logics: Towards a Holistic View using
   Predicate Transformers and Kleene Algebras with Top and Tests. Proc. ACM Program. Lang. 9, POPL (2025), 1782–1811.
   doi:10.1145/3704896
Max Vistrup, Michael Sammler, and Ralf Jung. 2025. Program Logics à la Carte. Proc. ACM Program. Lang. 9, POPL (2025),
   300–331. doi:10.1145/3704847
Systematic Design of Separation Logics                                                                                         29


David von Oheimb and Tobias Nipkow. 2002. Hoare Logic for NanoJava: Auxiliary Variables, Side Effects, and Virtual
   Methods Revisited. In FME 2002: Formal Methods - Getting IT Right, International Symposium of Formal Methods Europe,
   Copenhagen, Denmark, July 22-24, 2002, Proceedings (Lecture Notes in Computer Science, Vol. 2391), Lars-Henrik Eriksson
   and Peter A. Lindsay (Eds.). Springer, 89–105. doi:10.1007/3-540-45614-7_6
Glynn Winskel. 1993. The formal semantics of programming languages - an introduction. MIT Press, Cambridge, Mas-
   sachusetts.
Hongseok Yang and Peter W. O’Hearn. 2002. A Semantic Basis for Local Reasoning. In Foundations of Software Science and
   Computation Structures, 5th International Conference, FOSSACS 2002. Held as Part of the Joint European Conferences on
   Theory and Practice of Software, ETAPS 2002 Grenoble, France, April 8-12, 2002, Proceedings (Lecture Notes in Computer Science,
   Vol. 2303), Mogens Nielsen and Uffe Engberg (Eds.). Springer, Berlin, Heidelberg, 402–416. doi:10.1007/3-540-45931-6_28
Linpeng Zhang and Benjamin Lucien Kaminski. 2022. Quantitative strongest post: a calculus for reasoning about the flow
   of quantitative information. Proc. ACM Program. Lang. 6, OOPSLA1 (2022), 1–29. doi:10.1145/3527331
Noam Zilberstein, Derek Dreyer, and Alexandra Silva. 2023. Outcome Logic: A Unifying Foundation for Correctness and
   Incorrectness Reasoning. Proc. ACM Program. Lang. 7, OOPSLA1 (2023), 522–550. doi:10.1145/3586045
Noam Zilberstein, Angelina Saliling, and Alexandra Silva. 2024. Outcome Separation Logic: Local Reasoning for Correctness
   and Incorrectness with Computational Effects. Proc. ACM Program. Lang. 8, OOPSLA1 (2024), 276–304. doi:10.1145/3649821
Noam Zilberstein, Alexandra Silva, and Joseph Tassarotti. 2026. Probabilistic Concurrent Reasoning in Outcome Logic:
   Independence, Conditioning, and Invariants. Proc. ACM Program. Lang. 10, POPL (2026), 235–264. doi:10.1145/3776651
30                                                                  Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


A     Glossary
In this appendix, we provide a set of tables that can guide the reader through the various notational
conventions used throughout the main text. Table 5 recalls the meaning of the structural assertions.
Table 6 summarizes the superscripts employed to indicate the orientation and interpretation of
closure operators and semantic triples, as introduced in Section 4. Finally, Table 7 lists all the
proof systems discussed in this work, along with their corresponding validity conditions and
classifications according to the analytical dimensions considered.

     Structural assertion                                           Meaning
              emp                                                Empty heap
             x ↦→ e                   Single location in the heap pointed by x whose content is e
              x ̸↦→              Single location in the heap pointed by x which has been deallocated
             P∗Q                            P and Q hold in two disjoint portions of the heap
              x ↦→
                 ̸̸                         Single location pointed by x that cannot be framed
      Table 5. Intuitive meaning of structural assertions. The assertion x ↦→ ̸̸ is novel to this contribution.



                                                →
                                                ·     ·
                                                      →    ←
                                                           ·    ·
                                                                ←     →     ←    ↔
                                                                      →     ←    ↔

                                     Over       ✓          ✓          ✓     ✓    ✓
                                    Under             ✓         ✓     ✓     ✓    ✓
                                  Forward       ✓     ✓               ✓          ✓
                                  Backward                 ✓    ✓           ✓    ✓
              Table 6. Arrows validity (symbols appearing as superscripts in closures and triples).



      Proof System             Validity          Direction      Sense      Memory model         Error Handling
      1
     ⊢SL+ {P} r {Q}       JrKSL
                             1 ⦃P⦄ ⊆ ⦃Q⦄         Forward        Over       No reallocation             ×
      2
     ⊢SL+ {P} r {Q}       JrKSL
                             2 ⦃P⦄ ⊆ ⦃Q⦄          Forward        Over        Reallocation                ×
   1
  ⊢ISL+ [P] r [Q]        ⦃Q⦄ ⊆ JrKISL 1 ⦃P⦄       Forward       Under      No reallocation              ✓
   2
  ⊢ISL+ [P] r [Q]        ⦃Q⦄ ⊆ JrKISL 2 ⦃P⦄       Forward       Under        Reallocation               ✓
                         J←−
   1
  ⊢NC+ (P) r (Q)           r KSL
                              1  ⦃Q⦄   ⊆ ⦃P⦄     Backward        Over      No reallocation               ×
   2
  ⊢NC+ (P) r (Q)          ←−  SL
                         J r K2 ⦃Q⦄ ⊆ ⦃P⦄        Backward        Over        Reallocation                ×
                         ⦃P⦄ ⊆ J←  −
  1
 ⊢SIL+ ⟨⟨P⟩⟩ r ⟨⟨Q⟩⟩               r KSL
                                      1 ⦃Q⦄      Backward       Under      No reallocation               ×
  2                               ←−
                         ⦃P⦄ ⊆ J r KSL
 ⊢SIL+ ⟨⟨P⟩⟩ r ⟨⟨Q⟩⟩                  2 ⦃Q⦄      Backward       Under        Reallocation                ×
Table 7. Validity conditions for each of the considered proof systems, detailing their direction of the analysis,
sense of approximation, memory model, and whether or not they explicitly account for errors.
Systematic Design of Separation Logics                                                                     31


B   Program semantics
In this appendix we spell out the full details of the collecting semantics considered in the paper. The
subscripts 1 and 2 denote the reference memory model. As usual, we use the subscript i whenever
the definition is independent from the memory model.

                                         (
                                             {(𝑠, ℎ)}   if LbM𝑠 = true
                     Jb?KSL
                         i (𝑠, ℎ) ≜
                                             ∅          otherwise
               Jerror()KSL
                        i (𝑠, ℎ) ≜ {abort}

                Jx := eKSL
                        i (𝑠, ℎ) ≜ {(𝑠 [x ↦→ LeM𝑠], ℎ)}
                                   (
                                     {(𝑠 [x ↦→ ℎ(𝑠 (y))], ℎ)} if ℎ(𝑠 (y)) ∈ V
              Jx := [y]KSL
                        i (𝑠, ℎ) ≜
                                     {abort}                  otherwise
                                   (
                                     {(𝑠, ℎ[𝑠 (x) ↦→ 𝑠 (y)])} if ℎ(𝑠 (x)) ∈ V
              J[x] := yKSL
                        i (𝑠, ℎ) ≜
                                     {abort}                  otherwise
          Jx := alloc()KSL
                        1 (𝑠, ℎ) ≜ {(𝑠 [x ↦→ 𝑙], ℎ[𝑙 ↦→ 𝑣]) | 𝑣 ∈ V, 𝑙 ∉ 𝑑𝑜𝑚(ℎ)}

          Jx := alloc()KSL
                        2 (𝑠, ℎ) ≜ {(𝑠 [x ↦→ 𝑙], ℎ[𝑙 ↦→ 𝑣]) | 𝑣 ∈ V, 𝑙 ∉ 𝑑𝑜𝑚(ℎ) ∨ ℎ(𝑙) = ⊥}
                                    (
                        SL            {(𝑠, ℎ ′ )} if ℎ = ℎ ′ • [𝑠 (x) ↦→ 𝑣], 𝑣 ∈ V
               Jfree(x)K1 (𝑠, ℎ) ≜
                                      {abort} otherwise
                                    (
                                      {(𝑠, ℎ ′ • [𝑠 (x) ↦→ ⊥])} if ℎ = ℎ ′ • [𝑠 (x) ↦→ 𝑣], 𝑣 ∈ V
               Jfree(x)KSL
                        2  (𝑠, ℎ) ≜
                                      {abort}                      otherwise
                Jr1 + r2 KSL              SL              SL
                          i (𝑠, ℎ) ≜ Jr1 Ki (𝑠, ℎ) ∪ Jr2 Ki (𝑠, ℎ)
                                          ′ ′        ′′ ′′                     ′ ′           SL ′′ ′′
                  Jr1 ; r2 KSL                                     SL
                            i (𝑠, ℎ) ≜ {(𝑠 , ℎ ) | (𝑠 , ℎ ) ∈ Jr1 Ki (𝑠, ℎ), (𝑠 , ℎ ) ∈ Jr2 Ki (𝑠 , ℎ )}
                                       Ø
                      Jr∗ KSL
                            i (𝑠, ℎ) ≜    Jri KSL                  0
                                               i (𝑠, ℎ) with r ≜ skip and r
                                                                                        i+1
                                                                                            ≜ r; ri
                                         i∈N

                            Fig. 6. The SL denotational semantics [Reynolds 2002].
32                                                                 Roberto Bruni, Lorenzo Gazzella, and Roberta Gori

                                    (
                                        {𝑜𝑘 : (𝑠, ℎ)}    if LbM𝑠 = true
               Jb?KISL
                   i 𝜖 : (𝑠, ℎ) ≜
                                        ∅                otherwise
         Jerror()KISL
                  i 𝜖 : (𝑠, ℎ) ≜ {𝑒𝑟 : (𝑠, ℎ)}

          Jx := eKISL
                  i 𝜖 : (𝑠, ℎ) ≜ {𝑜𝑘 : (𝑠 [x ↦→ LeM𝑠], ℎ)}
                                 (
                  ISL              {𝑜𝑘 : (𝑠 [x ↦→ ℎ(𝑠 (y))], ℎ)} if ℎ(𝑠 (y)) ∈ V
        Jx := [y]Ki 𝜖 : (𝑠, ℎ) ≜
                                   {𝑒𝑟 : (𝑠, ℎ)}                 otherwise
                                 (
                                   {𝑜𝑘 : (𝑠, ℎ[𝑠 (x) ↦→ 𝑠 (y)])} if ℎ(𝑠 (x)) ∈ V
        J[x] := yKISL
                  i 𝜖 : (𝑠, ℎ) ≜
                                   {𝑒𝑟 : (𝑠, ℎ)}                 otherwise
     Jx := alloc()KISL
                   1 𝜖 : (𝑠, ℎ) ≜ {𝑜𝑘 : (𝑠 [x ↦→ 𝑙], ℎ[𝑙 ↦→ 𝑣]) | 𝑣 ∈ V, 𝑙 ∉ 𝑑𝑜𝑚(ℎ)}

     Jx := alloc()KISL
                   2 𝜖 : (𝑠, ℎ) ≜ {𝑜𝑘 : (𝑠 [x ↦→ 𝑙], ℎ[𝑙 ↦→ 𝑣]) | 𝑣 ∈ V, 𝑙 ∉ 𝑑𝑜𝑚(ℎ) ∨ ℎ(𝑙) = ⊥}
                                    (
                                      {𝑜𝑘 : (𝑠, ℎ ′ )} if ℎ = ℎ ′ • [𝑠 (x) ↦→ 𝑣], 𝑣 ∈ V
          Jfree(x)KISL
                   1 𝜖 : (𝑠, ℎ) ≜
                                      {𝑒𝑟 : (𝑠, ℎ)} otherwise
                                    (
                                      {𝑜𝑘 : (𝑠, ℎ ′ • [𝑠 (x) ↦→ ⊥])} if ℎ = ℎ ′ • [𝑠 (x) ↦→ 𝑣], 𝑣 ∈ V
          Jfree(x)KISL
                   2   𝜖 : (𝑠, ℎ) ≜
                                      {𝑒𝑟 : (𝑠, ℎ)}                     otherwise
          Jr1 + r2 KISL                 ISL                 ISL
                    i 𝜖 : (𝑠, ℎ) ≜ Jr1 Ki 𝜖 : (𝑠, ℎ) ∪ Jr2 Ki 𝜖 : (𝑠, ℎ)
                                             ′ ′             ′ ′
            Jr1 ; r2 KISL                                                  ISL
                      i 𝜖 : (𝑠, ℎ) ≜ {𝑒𝑟 : (𝑠 , ℎ ) | 𝑒𝑟 : (𝑠 , ℎ ) ∈ Jr1 Ki 𝜖 : (𝑠, ℎ)}

                                 ∪ {𝜖 : (𝑠 ′, ℎ ′ ) | 𝑜𝑘 : (𝑠 ′′, ℎ ′′ ) ∈ Jr1 KISL
                                                                                i 𝜖 : (𝑠, ℎ),

                                                𝜖 : (𝑠 ′, ℎ ′ ) ∈ Jr2 KISL      ′′ ′′
                                                                       i 𝑜𝑘 : (𝑠 , ℎ )}
                                   Ø
               Jr∗ KISL
                    i 𝜖 : (𝑠, ℎ) ≜  Jri KISL                         0
                                         i 𝜖 : (𝑠, ℎ) with r ≜ skip and r
                                                                                        i+1
                                                                                            ≜ r; ri
                                    i∈N

                        Fig. 7. The ISL denotational semantics [Raad et al. 2020].
Systematic Design of Separation Logics                                                                                                                             33


             2                                                                 1                                                2
    {Alloc2}+                                                         {Free}+                                         {Free2}+


    {empXp ∗ l′ ̸↦→} x := alloc() {empXp \{x} ∗ l′ ↦→ z′ ∧ x = l′ }   {empXp ∗ x ↦→ z′ } free(x) {empXp }             {empXp ∗ x ↦→ z′ } free(x) {empXp ∗ x ̸↦→}

                  i                                                    i                                  i
          {Alloc}+                                          {Assume}+                         {Assign}+


          {empXp } x := alloc() {empXp \{x} ∗ x ↦→ z′ }     {empXp } b? {empXp ∧ b}           {empXp \{x} ∧ x = x′ } x := e {empXp \{x} ∧ x = e[x′ /x]}

                               i                                                                    i
                       {Load}+                                                               {Store}+


                       {empXp ∗ y ↦→ z′ } x := [y] {empXp \{x} ∗ y ↦→ z′ ∧ x = z′ }          {empXp ∗ x ↦→ z′ } [x] := y {empXp ∗ x ↦→ y}

                                   i                                    i                                              i            i
                          {Frame}+                             {Cons}+                                        {Iterate}+    {Exists}+
                          fv(R) ⊆ Xl {P} r {Q} P ⊲⊳ R          P ⇒ P′       {P′ } r {Q ′ }   Q′ ⇒ Q           {P} r {P}     {P} r {Q} X ⊆ Xl
                                 {P ∗ R} r {Q ∗ R}                           {P} r {Q}                        {P} r∗ {P}     {∃X.P} r {∃X.Q}
                                                 i                                  i                            i
                                           {Seq}+                       {Choice}+                       {Disj}+
                                           {P} r1 {S} {S} r2 {Q}        ∀𝑖 ∈ {1, 2}.{P} ri {Q}           ∀𝑖 ∈ 𝐼 .{Pi } r {Qi }
                                                {P} r1 ; r2 {Q}            {P} r1 + r2 {Q}              {∨𝑖 ∈𝐼 Pi } r {∨𝑖 ∈𝐼 Qi }


Fig. 8. SL+: Synthesized proof system for forward correctness analysis in both memory models i ∈ {1, 2}.

C    Proof systems
In this appendix, we report the proof systems omitted from the main text. In particular, Figures 8, 9, 11
and 5 contain the full set of inference rules for forward and backward analyses. We can immediately
observe that proof systems for forward/backward analysis share the same axioms for atomic
commands for both over- and under-approximation.
34                                                                                                              Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


                      2                                                                         1                                             2
          [Alloc2] +                                                                     [Free1] +                                 [Free2] +


          [empXp ∗ l′ ̸↦→] x := alloc() [empXp \{x} ∗ l′ ↦→ z′ ∧ x = l′ ]                [empXp ∗ x ↦→ z′ ] free(x) [empXp ]       [empXp ∗ x ↦→ z′ ] free(x) [empXp ∗ x ̸↦→]
                               2                                                   2                                                      2
                     [FreeEr3] +                                         [LoadEr3] +                                        [StoreEr3] +


                     [empXp ∗ x ̸↦→] free(x) [empXp ∗ x ̸↦→]             [empXp ∗ y ̸↦→] x := [y] [empXp ∗ y ̸↦→]           [empXp ∗ x ̸↦→] [x] := y [empXp ∗ x ̸↦→]
                                        i                                                                      i                              i
                               [Assign] +                                                            [Assume] +                      [Error] +


                               [empXp \{x} ∧ x = x′ ] x := e [empXp \{x} ∧ x = e[x′ /x]]             [empXp ] b? [empXp ∧ b]         [empXp ] error() [empXp ]
            i                                                        i                                                                            i
     [Alloc] +                                             [Load] +                                                                     [Store] +


     [empXp ] x := alloc() [empXp \{x} ∗ x ↦→ z′ ]         [empXp ∗ y ↦→ z′ ] x := [y] [empXp \{𝑥 } ∗ y ↦→ z′ ∧ x = z′ ]                [empXp ∗ x ↦→ z′ ] [x] := y [empXp ∗ x ↦→ y]
                 i                                                               i                                                            i
      [FreeEr1] +                                                [LoadEr1] +                                                     [StoreEr1] +


      [empXp ∗ x  null] free(x) [empXp ∗ x  null]              [empXp ∗ y  null] x := [y] [empXp ∗ y  null]                  [empXp ∗ x  null] [x] := y [empXp ∗ x  null]
                                i                                                    i                                                    i
                     [FreeEr2] +                                         [LoadEr2] +                                        [StoreEr2] +


                     [empXp ∗ x ↦→ ̸̸ ] free(x) [empXp ∗ x ↦→ ̸̸ ]       [empXp ∗ y ↦→ ̸̸ ] x := [y] [empXp ∗ y ↦→ ̸̸ ]     [empXp ∗ x ↦→ ̸̸ ] [x] := y [empXp ∗ x ↦→ ̸̸ ]

                                 i                                       i                                                   i                i               i
                      [Frame] +                               [Cons] +                                    [Iterate − zero] +      [Iterate] +         [Exists] +
                      P ⊲⊳ R     [P] r [Q] fv(R) ⊆ Xl         P′ ⇒ P         [P′ ] r [Q ′ ]   Q ⇒ Q′                              [P] r∗ ; r [Q]      [P] r [Q] X ⊆ Xl
                                [P ∗ R] r [Q ∗ R]                             [P] r [Q]                   [P] r∗ [P]               [P] r∗ [Q]          [∃X.P] r [∃X.Q]
                                                     i                   i                                 i                        i
                                            [SeqEr] +         [Seq] +                            [Choice] +                  [Disj] +
                                             [P] r1 [Q]       [P] r1 [S] [𝑆] r2 [Q]              ∀𝑖 ∈ {1, 2}.[P] ri [Qi ]     ∀𝑖 ∈ 𝐼 .[Pi ] r [Qi ]
                                            [P] r1 ; r2 [Q]        [P] r1 ; r2 [Q]               [P] r1 + r2 [Q1 ∨ Q2 ]      [∨𝑖 ∈𝐼 Pi ] r [∨𝑖 ∈𝐼 Qi ]


Fig. 9. ISL+: Synthesized proof system for forward incorrectness analysis in both memory models i ∈ {1, 2}.



      Par                                                     ParEr                                                       ParSeq
      [Pi ] ri [Qi ] for all i ∈ {1, 2}                       [P] ri [Q] for some i ∈ {1, 2}                              [P] r1 ∥ r2 [Q] or [P] r2 ∥ r1 [Q]
       [P1 ⊛ P2 ] r1 ∥ r2 [Q1 ⊛ Q2 ]                                  [P] r1 ∥ r2 [Q]                                                 [P] r1 ∥ r2 [Q]
                          ParL                                                                       ParR
                          r1 = r3 ; r4        [P] r3 [S] [S] r4 ∥ r2 [Q]                             r2 = r3 ; r4      [P] r3 [S] [S] r1 ∥ r4 [Q]
                                              [P] r1 ∥ r2 [Q]                                                          [P] r1 ∥ r2 [Q]

                                            Fig. 10. Additional rules for parallel composition in CISL+.
Systematic Design of Separation Logics                                                                                                                                                                 35


             2                                                                                        1                                                        2
   ⟨⟨Alloc2⟩⟩ +                                                                            ⟨⟨Free1⟩⟩ +                                                ⟨⟨Free2⟩⟩ +


   ⟨⟨empXp \{x} ∧ x′ = l′ ∗ l′ ̸↦→⟩⟩ x := alloc() ⟨⟨empXp \{x} ∧ x = x′ ∗ x ↦→ z′ ⟩⟩       ⟨⟨empXp ∗ x ↦→ z′ ⟩⟩ free(x) ⟨⟨empXp ⟩⟩                    ⟨⟨empXp ∗ x ↦→ z′ ⟩⟩ free(x) ⟨⟨empXp ∗ x ̸↦→⟩⟩
                  i                                                                                 i                                                                         i
        ⟨⟨Alloc⟩⟩ +                                                                      ⟨⟨Assign⟩⟩ +                                                               ⟨⟨Assume⟩⟩ +


        ⟨⟨empXp \{x} ∧ x′ = l′ ⟩⟩ x := alloc() ⟨⟨empXp \{x} ∧ x = x′ ∗ x ↦→ z′ ⟩⟩        ⟨⟨empXp \{x} ∧ x′ = e⟩⟩ x := e ⟨⟨empXp \{x} ∧ x = x′ ⟩⟩                    ⟨⟨empXp ∧ b⟩⟩ b? ⟨⟨empXp ⟩⟩
                               i                                                                                               i
                      ⟨⟨Load⟩⟩ +                                                                                  ⟨⟨Store⟩⟩ +


                      ⟨⟨empXp \{x} ∧ x′ = z′ ∗ y ↦→ z′ ⟩⟩ x := [y] ⟨⟨empXp \{x} ∧ x = x′ ∗ y ↦→ z′ ⟩⟩             ⟨⟨empXp ∗ x ↦→ z′ ⟩⟩ [x] := y ⟨⟨empXp ∗ x ↦→ y⟩⟩

                                        i                                           i                            i                                i
                              ⟨⟨Frame⟩⟩ +                                 ⟨⟨Exists⟩⟩ +                  ⟨⟨Disj⟩⟩ +                      ⟨⟨Seq⟩⟩ +
                              fv(R) ⊆ Xl ⟨⟨P⟩⟩ r ⟨⟨Q⟩⟩ Q ⊲⊳ R             ⟨⟨P⟩⟩ r ⟨⟨Q⟩⟩ X ⊆ Xl           ∀𝑖 ∈ 𝐼 .⟨⟨Pi ⟩⟩ r ⟨⟨Qi ⟩⟩      ⟨⟨P⟩⟩ r1 ⟨⟨S⟩⟩ ⟨⟨𝑆⟩⟩ r2 ⟨⟨Q⟩⟩
                                     ⟨⟨P ∗ R⟩⟩ r ⟨⟨Q ∗ R⟩⟩                  ⟨⟨∃X.P⟩⟩ r ⟨⟨∃X.Q⟩⟩         ⟨⟨∪i∈I Pi ⟩⟩ r ⟨⟨∪i∈I Qi ⟩⟩            ⟨⟨P⟩⟩ r1 ; r2 ⟨⟨Q⟩⟩

                                             i                                                    i                   i                       i
                                    ⟨⟨Cons⟩⟩ +                                  ⟨⟨Iterate-zero⟩⟩ +        ⟨⟨Iterate⟩⟩ +            ⟨⟨Choice⟩⟩ +
                                    P ⇒ P′       ⟨⟨P′ ⟩⟩ r ⟨⟨Q ′ ⟩⟩   Q′ ⇒ Q                              ⟨⟨P⟩⟩ r∗ ; r ⟨⟨Q⟩⟩       ⟨⟨P⟩⟩ r1 ⟨⟨S⟩⟩ ⟨⟨𝑆⟩⟩ r2 ⟨⟨Q⟩⟩
                                                   ⟨⟨P⟩⟩ r ⟨⟨Q⟩⟩                ⟨⟨Q⟩⟩ r∗ ⟨⟨Q⟩⟩              ⟨⟨P⟩⟩ r∗ ⟨⟨Q⟩⟩                ⟨⟨P⟩⟩ r1 ; r2 ⟨⟨Q⟩⟩


Fig. 11. SIL+: Synthesized proof system for backward incorrectness analysis in both memory models i ∈ {1, 2}.
36                                                                    Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


D     Proofs
This appendix gathers rather technical material along with the proofs of the main results in which
it is applied. The results on the properties of the closure operators presented for forward analysis
have been mechanized and formally verified in Isabelle/HOL. In addition, we have formalized the
systematic derivation procedure described in Section 4, which the completeness proof follows.

D.1     Proofs of Sec.4
Standard properties for the separating conjunction ∗ extend naturally to the operator • when
dealing with sets of states instead of assertions. In the following, we present these properties
explicitly.
     Property D.1 (Distributivity). For 𝑅 ∈ F and it holds (∃X.𝑃) • 𝑅 = ∃X.(𝑃 • 𝑅).
     Property D.2 (Monotonicity). For 𝑅 ∈ F, if 𝑄 ′ ⊆ 𝑄 then 𝑄 ′ • 𝑅 ⊆ 𝑄 • 𝑅.
  Theorem 4.1 (Forward Semantic Preservation). Given 𝑃, r, 𝑄 such that JrK𝑃 = 𝑄 and 𝑅 ∈ F
such that 𝑃 ▶◀ 𝑅, then (JrK𝑃) • 𝑅 = JrK(𝑃 • 𝑅) = 𝑄 • 𝑅.
   Proof. We prove separately that 𝑄 • 𝑅 ⊆ JrK(𝑃 • 𝑅) and JrK(𝑃 • 𝑅) ⊆ 𝑄 • 𝑅.
Case 𝑄 • 𝑅 ⊆ JrK(𝑃 • 𝑅):
Suppose (𝑠, ℎ) ∈ 𝑄 • 𝑅, then by definition of • we have:
(1) ℎ = ℎ 1 • ℎ 2 ,
(2) (𝑠, ℎ 1 ) ∈ 𝑄,
(3) (𝑠, ℎ 2 ) ∈ 𝑅
By (2) and definition of JrK we have that ∃(𝑠 ′, ℎ ′ ) ∈ 𝑃 s.t. (𝑠, ℎ 1 ) ∈ JrK{(𝑠 ′, ℎ ′ )}. By hypothesis
𝑅 ∈ F, and since 𝑠 and 𝑠 ′ may differ only in modified variables, it implies that also (𝑠 ′, ℎ 2 ) ∈ 𝑅.
Hence, by using the hypothesis 𝑃 ▶◀ 𝑅 we have that ℎ ′ #ℎ 2 , and so (𝑠 ′, ℎ ′ • ℎ 2 ) ∈ 𝑃 • 𝑅. Finally, since
(𝑠, ℎ 1 ) ∈ JrK{(𝑠 ′, ℎ ′ )} and r leaves ℎ 2 untouched we have that (𝑠, ℎ 1 • ℎ 2 ) ∈ JrK(𝑃 • 𝑅), that by (1)
(𝑠, ℎ) ∈ JrK(𝑃 • 𝑅).
Case JrK(𝑃 • 𝑅) ⊆ 𝑄 • 𝑅:
Suppose (𝑠, ℎ) ∈ JrK(𝑃 • 𝑅), then by definition of JrK we have that ∃(𝑠 ′, ℎ ′ ) ∈ 𝑃 • 𝑅 s.t. (𝑠, ℎ) ∈
JrK{(𝑠 ′, ℎ ′ )}, and by definition of •, ∃ℎ 1, ℎ 2 s.t.:
(1) ℎ 1 #ℎ 2
(2) ℎ ′ = ℎ 1 • ℎ 2
(3) (𝑠 ′, ℎ 1 ) ∈ 𝑃
(4) (𝑠 ′, ℎ 2 ) ∈ 𝑅
Since (𝑠, ℎ) ∈ JrK{(𝑠 ′, ℎ 1 • ℎ 2 )} and 𝑅 ∈ F, there exists ℎ 1′ s.t. (𝑠, ℎ 1′ ) ∈ JrK{(𝑠 ′, ℎ 1 )} with ℎ = ℎ 1′ • ℎ 2 .
By definition of JrK and (3), we have that (𝑠, ℎ 1′ ) ∈ JrK𝑃. Finally, by (4) and the hypothesis of 𝑅 ∈ F,
we have that (𝑠, ℎ 2 ) ∈ 𝑅, and so by hypothesis 𝑃 ▶◀ 𝑅 we have that ℎ 1′ #ℎ 2 . Hence (𝑠, ℎ 1′ • ℎ 2 ) ∈ 𝑄 • 𝑅,
which is (𝑠, ℎ 1′ • ℎ 2 ) ∈ 𝑄 • 𝑅 since ℎ = ℎ 1′ • ℎ 2 .                                                               □
  Theorem 4.2 (Backward Semantic Preservation). Given 𝑃, r, 𝑄 such that J←
                                                                         −
                                                                         r K𝑄 = 𝑃 and 𝑅 ∈ F
                         ←−            ←−
such that 𝑄 ▶◀ 𝑅, then (J r K𝑄) • 𝑅 = J r K(𝑄 • 𝑅) = 𝑃 • 𝑅.
     Proof. Analogous to the proof of Theorem 4.1.                                                                      □
     Property D.3. Given 𝑀1, 𝑀2 ∈ Mi , (∃X.𝑀1 ) ▶◀ 𝑀2 ⇐⇒ 𝑀1 ▶◀ 𝑀2
     Property D.4. Given 𝑀1 = (∪𝑖 ∈𝐼 .𝑀𝑖 ), 𝑀2 ∈ Mi , 𝑀1 ▶◀ 𝑀2 ⇐⇒ ∀𝑖 ∈ 𝐼 .𝑀𝑖 ▶◀ 𝑀2
     Let us define the following closures:
Systematic Design of Separation Logics                                                                            37

                      ↔                →           →
     • 𝜌 →· ≜ (𝜌 exists
                 ↔          →
                        ∪ 𝜌 frame      · )∗
                                  ∪ 𝜌 cons
         ·      ↔          →          ·
                ↔
     • 𝜌 → ≜ (𝜌 exists     →
                       ∪ 𝜌 frame     →
                                 ∪ 𝜌 cons )∗
         ←      ↔
                ↔          ←
                           ←         ←· )∗
     • 𝜌 · ≜ (𝜌 exists ∪ 𝜌 frame ∪ 𝜌 cons
         ·      ↔          ←          ·
                ↔
     • 𝜌 ← ≜ (𝜌 exists     ←
                       ∪ 𝜌 frame     ←
                                 ∪ 𝜌 cons )∗

  In the following, we state Definition 4.5, Theorem 4.3 and Corollary 4.4 extensively for each
logic under consideration.

                                                                            →          ·       ←              ·
  Definition 4.5 (Axioms). A valid set of axioms for TriplesJ·cK /Triples→
                                                                         JcK
                                                                             /TriplesJ·cK /Triples←
                                                                                                  JcK
                                                                                                      is
                                    →                  ·           ←   ·
any minimal set AxiomsJ·cK /Axioms→
                                  JcK
                                      /AxiomsJ·cK /Axioms←
                                                         JcK
                                                             such that:

                 →                             →
     • TriplesJ·cK ≜ 𝜌 →· (AxiomsJ·cK )
                  ·            ·               ·
     • Triples→
              JcK
                  ≜ 𝜌 → (Axioms→
                               JcK
                                   )
                 ←                             ←
     • TriplesJ·cK ≜ 𝜌 ←· (AxiomsJ·cK )
                  ·            ·               ·
     • Triples←
              JcK
                  ≜ 𝜌 ← (Axioms←
                               JcK
                                   )


  Theorem 4.3. It holds that:

                  →             ↔          →
    (1) 𝜌 →· = 𝜌 cons
                  ·       ↔
                      ◦ 𝜌 exists     →
                                 ◦ 𝜌 frame
           ·     →·       ↔
                          ↔          →
                                     →
    (2) 𝜌 → = 𝜌 cons  ◦ 𝜌 exists ◦ 𝜌 frame
                 ←        ↔          ←
    (3) 𝜌 ←· = 𝜌 cons
                  ·       ↔
                      ◦ 𝜌 exists     ←
                                 ◦ 𝜌 frame
           ·      ·
                 ← ◦ 𝜌↔   ↔          ←
                                     ←
    (4) 𝜌 ← = 𝜌 cons      exists ◦ 𝜌 frame



   Proof. We only prove the first two statement since the last two are analogous. Moreover, we
only prove the inclusion ⊆ since ⊇ trivially holds. The proof proceeds by showing pairwise switches
of consequent closures.
   Over-approximation of forward semantics:

          →
          →          ·→       ·        →
                                      → :      →
    (1) 𝜌 frame ◦ 𝜌 cons ⊆ 𝜌 cons ◦ 𝜌 frame



         →
         →            →
                    · 𝑇                                                                               → · ]
       𝜌 frame ◦ 𝜌 cons                                                                     [Def. of 𝜌 cons
         →                         →               →
         → {(𝑃, c, 𝑄 ′ ) · | (𝑃, c, 𝑄) · ∈ 𝑇 , 𝑄 ⊆ 𝑄 ′ }                                             →→ ]
     = 𝜌 frame                                                                             [Def. of 𝜌 frame
                                    →                      →
     = {(𝑃 • 𝑅, c, 𝑄 ′ • 𝑅) · | (𝑃, c, 𝑄) · ∈ 𝑇 , 𝑄 ⊆ 𝑄 ′, 𝑅 ∈ F, 𝑃 ▶◀ 𝑅}                      [Prop.𝐷.2]
                          ′       →             →                                                     →
     ⊆ {(𝑃 • 𝑅, c, 𝑄          • 𝑅) · | (𝑃, c, 𝑄) · ∈ 𝑇 , 𝑄 • 𝑅 ⊆ 𝑄 ′ • 𝑅, 𝑅 ∈ F, 𝑃 ▶◀ 𝑅}                · ]
                                                                                            [Def. of 𝜌 cons
         →                                 →                   →
          · {(𝑃 • 𝑅, c, 𝑄 • 𝑅) · | (𝑃, c, 𝑄) · ∈ 𝑇 , 𝑅 ∈ F, 𝑃 ▶◀ 𝑅}                                  →→ ]
     ⊆ 𝜌 cons                                                                              [Def. of 𝜌 frame
         →·       →
                  → 𝑇
     = 𝜌 cons ◦ 𝜌 frame
38                                                                                                Roberto Bruni, Lorenzo Gazzella, and Roberta Gori

            →  →      ↔          ↔ ↔        → :       ↔               →
      (2) 𝜌 frame ◦ 𝜌 exists ⊆ 𝜌 exists ◦ 𝜌 frame
       →
       →         ↔ 𝑇       ↔                                                                                                              ↔ ]↔
     𝜌 frame ◦ 𝜌 exists                                                                                                        [Def. of 𝜌 exists
        →
     → {(∃X.𝑃, c, ∃X.𝑄) · | (𝑃, c, 𝑄) · ∈ 𝑇 , X ⊆ X } →                           →                                                       → ]→
 = 𝜌 frame                                         l                                                                           [Def. of 𝜌 frame
                                                                  →                       →
 = {((∃X.𝑃) • 𝑅, c, (∃X.𝑄) • 𝑅) · | (𝑃, c, 𝑄) · ∈ 𝑇 , X ⊆ Xl, 𝑅 ∈ F, (∃X.𝑃) ▶◀ 𝑅}                                                   [Prop.𝐷.3]
                               →             →
 = {((∃X.𝑃) • 𝑅, c, (∃X.𝑄) • 𝑅) · | (𝑃, c, 𝑄) · ∈ 𝑇 , X ⊆ Xl, 𝑅 ∈ F, 𝑃 ▶◀ 𝑅}                                                        [Prop.𝐷.1]
                                    →             →                                                                                       ↔ ]↔
 = {(∃X.(𝑃 • 𝑅), c, ∃X.(𝑄 • 𝑅)) · | (𝑃, c, 𝑄) · ∈ 𝑇 , X ⊆ Xl, 𝑅 ∈ F, 𝑃 ▶◀ 𝑅}                                                   [Def. of 𝜌 exists
     ↔
     ↔                        →             →                                                                                             → ]→
 = 𝜌 exists {(𝑃 • 𝑅, c, 𝑄 • 𝑅) · | (𝑃, c, 𝑄) · ∈ 𝑇 , 𝑅 ∈ F, 𝑃 ▶◀ 𝑅}                                                            [Def. of 𝜌 frame
     ↔
     ↔          →
                → 𝑇
 = 𝜌 exists ◦ 𝜌 frame

            ↔  ↔        ·        · →     ↔ :      →               ↔
      (3) 𝜌 exists ◦ 𝜌 cons ⊆ 𝜌 cons ◦ 𝜌 exists

                 ↔ ↔         · 𝑇   →                                                                                                 →· ]
               𝜌 exists ◦ 𝜌 cons                                                                                          [Def. of 𝜌 cons
                       ↔                          →
                ↔ {(𝑃, c, 𝑄 ′ ) · | (𝑃, c, 𝑄) · ∈ 𝑇 , 𝑄 ⊆ 𝑄 ′ }               →                                                     ↔
                                                                                                                                    ↔ ]
            = 𝜌 exists                                                                                                   [Def. of 𝜌 exists
                                                          →                       →
            = {(∃X.𝑃, c, ∃X.𝑄 ′ ) · | (𝑃, c, 𝑄) · ∈ 𝑇 , 𝑄 ⊆ 𝑄 ′, X ⊆ Xl }                                                [∃ monotone]
                                                  ′ →                    →                                                           →
           ⊆ {(∃X.𝑃, c, ∃X.𝑄 )                      ·         | (𝑃, c, 𝑄) · ∈ 𝑇 , ∃X.𝑄 ⊆ ∃X.𝑄 ′, X ⊆ Xl }                             · ]
                                                                                                                          [Def. of 𝜌 cons
                       →
                · ({(∃X.𝑃, c, ∃X.𝑄) · | (𝑃, c, 𝑄) · ∈ 𝑇 , X ⊆ X })→                       →                                         ↔
                                                                                                                                    ↔ ]
           ⊆ 𝜌 cons                                            l                                                         [Def. of 𝜌 exists
                 ·     → ↔ 𝑇       ↔
            = 𝜌 cons ◦ 𝜌 exists

     Under-approximation of forward semantics:
            →  →      → ⊆ 𝜌→ ◦ 𝜌→ :·                  ·           →
      (1) 𝜌 frame ◦ 𝜌 cons cons frame

           →→        → 𝑇       ·                                                                                                         ·
                                                                                                                                       → ]
         𝜌 frame ◦ 𝜌 cons                                                                                                   [Def. of 𝜌 cons
             →                                ·
           → {(𝑃, c, 𝑄 ′ ) → | (𝑃, c, 𝑄) → ∈ 𝑇 , 𝑄 ′ ⊆ 𝑄 }                ·                                                             →
                                                                                                                                      → ]
       = 𝜌 frame                                                                                                           [Def. of 𝜌 frame
                                                  ·                           ·
       = {(𝑃 • 𝑅, c, 𝑄 ′ • 𝑅) → | (𝑃, c, 𝑄) → ∈ 𝑇 , 𝑄 ′ ⊆ 𝑄, 𝑅 ∈ F, 𝑃 ▶◀ 𝑅}                                                     [Prop.𝐷.2]
                                       ′        ·             ·                                                                          ·
       ⊆ {(𝑃 • 𝑅, c, 𝑄                     • 𝑅) → | (𝑃, c, 𝑄) → ∈ 𝑇 , 𝑄 ′ • 𝑅 ⊆ 𝑄 • 𝑅, 𝑅 ∈ F, 𝑃 ▶◀ 𝑅}                                  → ]
                                                                                                                            [Def. of 𝜌 cons
               ·                                              ·
           → {(𝑃 • 𝑅, c, 𝑄 • 𝑅) → | (𝑃, c, 𝑄) → ∈ 𝑇 , 𝑅 ∈ F, 𝑃 ▶◀ 𝑅}                  ·                                                 →
                                                                                                                                      → ]
       ⊆ 𝜌 cons                                                                                                            [Def. of 𝜌 frame
                   ·
            → ◦ 𝜌 → )𝑇         →
       = (𝜌 cons  frame

            ↔  ↔       →         → →       ↔ :    →                   ↔
      (2) 𝜌 exists ◦ 𝜌 frame = 𝜌 frame ◦ 𝜌 exists

          →→        ↔ 𝑇        ↔                                                                                                         ↔
                                                                                                                                       ↔ ]
        𝜌 frame ◦ 𝜌 exists                                                                                                  [Def. of 𝜌 exists
            →
          → {(∃X.𝑃, c, ∃X.𝑄) → | (𝑃, c, 𝑄) → ∈ 𝑇 , X ⊆ X }    ·                       ·                                                  →
                                                                                                                                       → ]
      = 𝜌 frame                                         l                                                                   [Def. of 𝜌 frame
                                                                      ·                       ·
      = {((∃X.𝑃) • 𝑅, c, (∃X.𝑄) • 𝑅) → | (𝑃, c, 𝑄) → ∈ 𝑇 , X ⊆ Xl, 𝑅 ∈ F, 𝑃 ▶◀ 𝑅}                                                [Prop.𝐷.1]
                                     ·             ·                                                                                     ↔
                                                                                                                                       ↔ ]
      = {(∃X.(𝑃 • 𝑅), c, ∃X.(𝑄 • 𝑅)) → | (𝑃, c, 𝑄) → ∈ 𝑇 , X ⊆ Xl, 𝑅 ∈ F, 𝑃 ▶◀ 𝑅}                                           [Def. of 𝜌 exists
          ↔                    ·
          ↔ {(𝑃 • 𝑅, c, 𝑄 • 𝑅) →             ·                                                                                           →
                                                                                                                                       → ]
      = 𝜌 exists                 | (𝑃, c, 𝑄) → ∈ 𝑇 , 𝑅 ∈ F, 𝑃 ▶◀ 𝑅}                                                         [Def. of 𝜌 frame
          ↔
          ↔          →
                     →
      = 𝜌 exists ◦ 𝜌 frame𝑇
Systematic Design of Separation Logics                                                                           39

          ↔
          ↔          ·
                     → ⊆ 𝜌→ ◦ 𝜌↔ :    ·           ↔
    (3) 𝜌 exists ◦ 𝜌 cons cons exists
           ↔
           ↔             ·
                      → )𝑇                                                                               ·
                                                                                                        → ]
        (𝜌 exists ◦ 𝜌 cons                                                                   [Def. of 𝜌 cons
           ↔                          ·               ·
           ↔ ({(𝑃, c, 𝑄 ′ ) → | (𝑃, c, 𝑄) → ∈ 𝑇 ∧ 𝑄 ′ ⊆ 𝑄 })                                            ↔
                                                                                                        ↔ ]
       = 𝜌 exists                                                                            [Def. of 𝜌 exists
                                          ·           ·
       = {(∃X.𝑃, c, ∃X.𝑄 ′ ) → | (𝑃, c, 𝑄) → ∈ 𝑇 ∧ 𝑄 ′ ⊆ 𝑄 ∧ X ⊆ Xl }                        [∃ monotone]
                                       · ·                                                               ·
      ⊆ {(∃X.𝑃, c, ∃X.𝑄 ) | (𝑃, c, 𝑄) → ∈ 𝑇 ∧ ∃X.𝑄 ′ ⊆ ∃X.𝑄 ∧ X ⊆ Xl }
                                     ′ →                                                                → ]
                                                                                             [Def. of 𝜌 cons
          →·                     ·             ·                                                        ↔
                                                                                                        ↔ ]
      ⊆ 𝜌 cons ({(∃X.𝑃, c, ∃X.𝑄) → | (𝑃, c, 𝑄) → ∈ 𝑇 ∧ X ⊆ Xl })                             [Def. of 𝜌 exists
            →·      ↔
                    ↔ )𝑇
      = (𝜌 cons ◦ 𝜌 exists
                                                                                                                 □
                                                                                  →   ·       ←              ·
  Corollary 4.4 (Axioms). A valid set of axioms AxiomsJ·cK /Axioms→
                                                                  JcK
                                                                      /AxiomsJ·cK /Axioms←
                                                                                         JcK
                                                                                             is any
                             →                ·               ←           ·
minimal set TriplesJ·cK /Triples→
                                JcK
                                    /TriplesJ·cK /Triples←
                                                         JcK
                                                             such that:
                →                →            ↔       →                   →
     • TriplesJ·cK = (𝜌 cons
                         ·       ↔
                             ◦ 𝜌 exists     → )Axioms ·
                                        ◦ 𝜌 frame    JcK
                 ·               ·            ↔       →                       ·
     • Triples→
              JcK
                       → ◦ 𝜌↔
                  = (𝜌 cons            →            →
                            exists ◦ 𝜌 frame )AxiomsJcK
                ←                ←            ↔       ←                   ←
     • TriplesJ·cK = (𝜌 cons
                         ·       ↔
                             ◦ 𝜌 exists     ← )Axioms ·
                                        ◦ 𝜌 frame    JcK
                 ·               ·            ↔       ←                       ·
     • Triples←
              JcK
                       ← ◦ 𝜌↔
                  = (𝜌 cons            ←            ←
                            exists ◦ 𝜌 frame )AxiomsJcK

  Theorem 4.5 (Soundness and completeness). Proof systems in Fig.1 are sound and complete:
    (1) ⊩ {𝑃 } r {𝑄 } ⇐⇒ JrK𝑃 ⊆ 𝑄
    (2) ⊩ [𝑃] r [𝑄] ⇐⇒ 𝑄 ⊆ JrK𝑃
    (3) ⊩ (𝑃) r (𝑄) ⇐⇒ J←  −
                           r K𝑄 ⊆ 𝑃
    (4) ⊩ ⟨⟨𝑃⟩⟩ r ⟨⟨𝑄⟩⟩ ⇐⇒ 𝑃 ⊆ J←−
                                 r K𝑄

   Proof. Soundness can be proved by induction on the derivation tree. Completeness of atomic
commands follows directly from the definitions of semantic axioms Furthermore, completeness
of compositions for Fwd-over, Fwd-under and Bwd-under can be proved respectively as in [Cook
1978], [O’Hearn 2020], and [Ascari et al. 2025]. In the following, we show the completeness of
the composition of atomic commands for Bwd-over. Particularly, we show that for any 𝑄, we can
derive the triple (J← −
                      r K𝑄) r (𝑄). Completeness will follow by applying the rule of consequence. We
proceed by induction on the structure of r:
Case r ≜ r1 ; r2 :
We show a derivation for (J←      r1−
                                    ;−
                                     r−2 K𝑄) r1 ; r2 (𝑄). By property of backward semantics [Ascari et al.
2025, Lemma 3.1] we know that J←         r1−
                                           ;−
                                            r−2 K𝑄 = J←
                                                      r−1 KJ←
                                                            r−2 K𝑄. Hence, by inductive hypothesis we assume
                   ←−    ←−            ←−              ←−
that the triples (J r1 KJ r2 K𝑄) r1 (J r2 K𝑄) and (J r2 K𝑄) r2 (𝑄) are derivable, then by applying the rule
of seq we can derive:

                                      (J←
                                        r−1 KJ←
                                              r−2 K𝑄) r1 (J←r−2 K𝑄) (J←
                                                                      r−2 K𝑄) r2 (𝑄)
                                                                                     (Seq)
                                                    (J←
                                                      r−
                                                       ;−r−K𝑄) r ; r (𝑄)
                                                          1       2   1   2

Case r ≜ r1 + r2 :
We show a derivation for (J←  r1−−
                                 +−−
                                   r−2 K𝑄) r1 + r2 (𝑄). By property of backward semantics [Ascari et al.
2025, Lemma 3.1] we know that J←       r1−−
                                          +−−
                                            r−2 K𝑄 = J←
                                                      r−1 K𝑄 ∪ J←
                                                                r−2 K𝑄. Hence, by inductive hypothesis we
                          ←−                        ←
                                                    −
assume that the triples (J r1 K𝑄) r1 (𝑄) and (J r2 K𝑄) r2 (𝑄) are derivable, then by applying the rule
40                                                                        Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


of choice we can derive:

                           (J←
                             r−1 K𝑄) r1 (𝑄)                               (J←
                                                                            r−2 K𝑄) r2 (𝑄)
                                               (Cons)                                            (Cons)
                       (J←
                         r−K𝑄 ∪ J←
                         1         r−K𝑄) r (𝑄)
                                   2            1                   (J←
                                                                      r−1 K𝑄 ∪ J← r−2 K𝑄) r2 (𝑄)
                                                                                                 (Choice)
                                               (J←r1−−
                                                     +−−
                                                       r−2 K𝑄) r1 + r2 (𝑄)

Case r ≜ r∗1 :
                                   ←−                             ←−
We show a derivation for (J r∗1 K𝑄) r∗1 (𝑄). We set 𝐼 ≜ J r∗1 K𝑄. By property of backward se-
                                                              ←−
mantics [Ascari et al. 2025, Lemma 3.1] we know that J r∗1 K𝑄 = ∪𝑛≥0 J←       r−1 K𝑛 𝑄 and then J←
                                                                                                 r−1 K𝐼 =
 ←−            ←
               −  𝑛           ←−   𝑛+1          ←
                                                −  𝑛          ←−
J r1 K(∪𝑛≥0 J r1 K 𝑄) = ∪𝑛≥0 J r1 K 𝑄 = ∪𝑛≥1 J r1 K 𝑄 ⊆ ∪𝑛≥0 J r1 K 𝑄 = 𝐼 . Hence, by inductive hypoth-
                                                                   𝑛

esis we assume that the triple (𝐼 ) r1 (𝐼 ) is derivable. Furthermore, we have that 𝑄 = Jr1 K0𝑄 ⊆
Jr1 ∗ K𝑄 = 𝐼 , then by applying rule of Iter and Cons we can derive:

                                               (𝐼 ) r1 (𝐼 )
                                                              (Iter)
                                               (𝐼 ) r∗1 (𝐼 )          𝑄 ⊆𝐼
                                                                           (Cons)
                                                         (𝐼 ) r∗1 (𝑄)

                                                     ← −
That by definition of 𝐼 is analogous to the triple (J r∗1 K𝑄) r∗1 (𝑄).                                                     □


  In the following, we state Theorem 4.7 and Theorem 4.8 extensively for each logic under consid-
eration.

     Theorem 4.7. It holds that:
              →
              ·          ↔
                      ↔ ∪ 𝜌↔   ↔      →      ∗ →   ·       →
                                                           ↔        ↔
                                                                    ↔     ↔    →   →
      (1) (𝜌 cons ∪ 𝜌 disj exists ∪ 𝜌 frame ) = 𝜌 cons ◦ 𝜌 disj ◦ 𝜌 exists ◦ 𝜌 frame
               ·
             → ∪ 𝜌↔ ∪ 𝜌↔ ↔     ↔  →      ∗    →→       ↔    ·   ↔   ↔     ↔→       →
      (2) (𝜌 cons disj exists ∪ 𝜌 frame ) = 𝜌 cons ◦ 𝜌 disj ◦ 𝜌 exists ◦ 𝜌 frame
              ←
              ·          ↔
                      ↔ ∪ 𝜌↔   ↔      ←      ∗ ←   ·       ←
                                                           ↔        ↔
                                                                    ↔     ↔    ←   ←
      (3) (𝜌 cons ∪ 𝜌 disj exists ∪ 𝜌 frame ) = 𝜌 cons ◦ 𝜌 disj ◦ 𝜌 exists ◦ 𝜌 frame
               ·
             ← ∪ 𝜌↔ ∪ 𝜌↔ ↔     ↔  ←      ∗    ←←       ↔    ·   ↔   ↔     ↔←       ←
      (4) (𝜌 cons disj exists ∪ 𝜌 frame ) = 𝜌 cons ◦ 𝜌 disj ◦ 𝜌 exists ◦ 𝜌 frame

  Proof. We only prove the first statement, as the others are analogous. Moreover, we only
prove the inclusion ⊆ since ⊇ trivially holds. The proof proceeds by showing pairwise switches of
consequent closures, avoiding cases already proved in the proof of Theorem 4.3.
            ↔↔           ↔     ↔
                       ↔ = 𝜌↔ ◦ 𝜌↔ :       ↔
      (1) 𝜌 exists ◦ 𝜌 disj disj exists

      ↔↔           ↔
                  ↔𝑇
     𝜌 exists ◦ 𝜌 disj
       ↔                               →
     ↔ {(∪ 𝑃 , c, ∪ 𝑄 ) · | ∀𝑖 ∈ 𝐼 .(𝑃 , c, 𝑄 ) · ∈ 𝑇 }         →                                                      ↔
                                                                                                                       ↔ ]
 = 𝜌 exists 𝑖 ∈𝐼 𝑖 𝑖 ∈𝐼 𝑖             𝑖      𝑖                                                              [Def. of 𝜌 disj
                                           →                          →                                              ↔
                                                                                                                   ↔ ]
 = {(∃X. ∪𝑖 ∈𝐼 𝑃𝑖 , c, ∃X. ∪𝑖 ∈𝐼 𝑄𝑖 ) · | ∀𝑖 ∈ 𝐼 .(𝑃𝑖 , c, 𝑄𝑖 ) · ∈ 𝑇 , X ⊆ Xl }                        [Def. of 𝜌 exists
                                       →                          →
 = {(∪𝑖 ∈𝐼 ∃X.𝑃𝑖 , c, ∪𝑖 ∈𝐼 ∃X.𝑄𝑖 ) · | ∀𝑖 ∈ 𝐼 .(𝑃𝑖 , c, 𝑄𝑖 ) · ∈ 𝑇 , X ⊆ Xl }           [Distributivity of ∪ over ∃]
     ↔
     ↔ {(∃X.𝑃 , c, ∃X.𝑄 ) →
                          · | (𝑃 , c, 𝑄 ) →
                                          · ∈ 𝑇, X ⊆ X }                                                               ↔
                                                                                                                       ↔ ]
 = 𝜌 exists          𝑖 𝑖        𝑖      𝑖              l                                                     [Def. of 𝜌 disj
     ↔
     ↔          ↔
                ↔𝑇                                                                                                   ↔
                                                                                                                   ↔ ]
 = 𝜌 exists ◦ 𝜌 disj                                                                                    [Def. of 𝜌 exists
Systematic Design of Separation Logics                                                                                               41

          →  →           ↔
                    ↔ = 𝜌↔ ◦ 𝜌→ :↔       →
    (2) 𝜌 frame ◦ 𝜌 disj disj frame
   →→         ↔𝑇 ↔
  𝜌 frame ◦ 𝜌 disj
    →                                →
    → {(∪ 𝑃 , c, ∪ 𝑄 ) · | ∀𝑖 ∈ 𝐼 .(𝑃 , c, 𝑄 ) · ∈ 𝑇 }          →                                                                  ↔
                                                                                                                                 ↔ ]
= 𝜌 frame 𝑖 ∈𝐼 𝑖  𝑖 ∈𝐼 𝑖             𝑖      𝑖                                                                         [Def. of 𝜌 disj
                                             →                          →                                                        →
                                                                                                                               → ]
= {((∪𝑖 ∈𝐼 𝑃𝑖 ) • 𝑅, c, (∪𝑖 ∈𝐼 𝑄𝑖 ) • 𝑅) · | ∀𝑖 ∈ 𝐼 .(𝑃𝑖 , c, 𝑄𝑖 ) · ∈ 𝑇 , 𝑅 ∈ F, (∪𝑖 ∈𝐼 𝑃𝑖 ) ▶◀ 𝑅}                 [Def. of 𝜌 frame
                                             →                          →
= {(∪𝑖 ∈𝐼 (𝑃𝑖 • 𝑅), c, ∪𝑖 ∈𝐼 (𝑄𝑖 • 𝑅)) · | ∀𝑖 ∈ 𝐼 .(𝑃𝑖 , c, 𝑄𝑖 ) · ∈ 𝑇 , 𝑅 ∈ F, (∪𝑖 ∈𝐼 𝑃𝑖 ) ▶◀ 𝑅}                  [Distributivity]
                                        →                       →
= {(∪𝑖 ∈𝐼 (𝑃𝑖 • 𝑅), c, ∪𝑖 ∈𝐼 (𝑄𝑖 • 𝑅)) · | ∀𝑖 ∈ 𝐼 .(𝑃𝑖 , c, 𝑄𝑖 ) · ∈ 𝑇 , 𝑅 ∈ F, ∀𝑖 ∈ 𝐼 .𝑃𝑖 ▶◀ 𝑅}                          [Prop.𝐷.4]
    ↔
    ↔                         →                →                                                                                   ↔
                                                                                                                                 ↔ ]
= 𝜌 disj {(𝑃𝑖 • 𝑅, c, 𝑄𝑖 • 𝑅) · | (𝑃𝑖 , c, 𝑄𝑖 ) · ∈ 𝑇 , 𝑅 ∈ F, ∀𝑖 ∈ 𝐼 .𝑃𝑖 ▶◀ 𝑅}                                       [Def. of 𝜌 disj
    ↔
    ↔ ◦ 𝜌→ 𝑇 →                                                                                                                   →
                                                                                                                               → ]
⊆ 𝜌 disj frame
                                                                                                                    [Def. of 𝜌 frame
             ↔
          ↔ ◦𝜌 ·     →   ·       →
                                 ↔       ↔
    (3) 𝜌 disj cons = 𝜌 cons ◦ 𝜌 disj :
             ↔
            ↔ ◦𝜌 · 𝑇 →
          𝜌 disj cons
             ↔               →                →
            ↔ {(𝑃, c, 𝑄 ′ ) · | (𝑃, c, 𝑄) · ∈ 𝑇 , 𝑄 ⊆ 𝑄 ′ }                                                             →
                                                                                                                       · ]
        = 𝜌 disj                                                                                           [Def. of 𝜌 cons
                                     →                          →                                                         ↔
        = {(∪𝑖 ∈𝐼 𝑃𝑖 , c, ∪𝑖 ∈𝐼 𝑄𝑖′ ) · | ∀𝑖 ∈ 𝐼 .(𝑃𝑖 , c, 𝑄𝑖 ) · ∈ 𝑇 , 𝑄𝑖 ⊆ 𝑄𝑖′ }                                     ↔ ]
                                                                                                            [Def. of 𝜌 disj
                                     →                          →
        ⊆ {(∪𝑖 ∈𝐼 𝑃𝑖 , c, ∪𝑖 ∈𝐼 𝑄𝑖′ ) · | ∀𝑖 ∈ 𝐼 .(𝑃𝑖 , c, 𝑄𝑖 ) · ∈ 𝑇 , ∪𝑖 ∈𝐼 𝑄𝑖 ⊆ ∪𝑖 ∈𝐼 𝑄𝑖′ }             [∪ monotone]
            →· {(∪ 𝑃 , c, ∪ 𝑄 ) →  · | ∀𝑖 ∈ 𝐼 .(𝑃 , c, 𝑄 ) →
                                                           · ∈ 𝑇}                                                       →
                                                                                                                       · ]
        ⊆ 𝜌 cons     𝑖 ∈𝐼 𝑖 𝑖 ∈𝐼 𝑖               𝑖      𝑖                                                  [Def. of 𝜌 cons
            →·       ↔
                     ↔𝑇                                                                                                ↔ ]↔
        = 𝜌 cons ◦ 𝜌 disj                                                                                   [Def. of 𝜌 disj
                                                                                                                                     □
  Theorem 4.8. For every index set 𝐼 ,
             ↔
          ↔ ◦ 𝜌↔     ↔       →→                    →             ↔   ↔      →   →                    ′                      ′      →
    (1) 𝜌 disj                                     ·                                                                               ·
                   exists ◦ 𝜌 frame {(𝑃𝑖 , c, 𝑄 𝑖 ) ) | 𝑖 ∈ 𝐼 } = 𝜌 exists ◦ 𝜌 frame {(∪𝑖 ∈𝐼 (𝑃𝑖 ∩ 𝑑 = 𝑖), c, ∪𝑖 ∈𝐼 (𝑄 𝑖 ∩ 𝑑 = 𝑖)) )}
          ↔
          ↔ ◦ 𝜌↔   ↔          →
                              →                    ·                 ↔
                                                                     ↔          →
                                                                                →                    ′                      ′      ·
    (2) 𝜌 disj                                     →                                                                               →
                   exists ◦ 𝜌 frame {(𝑃𝑖 , c, 𝑄 𝑖 ) ) | 𝑖 ∈ 𝐼 } = 𝜌 exists ◦ 𝜌 frame {(∪𝑖 ∈𝐼 (𝑃𝑖 ∩ 𝑑 = 𝑖), c, ∪𝑖 ∈𝐼 (𝑄 𝑖 ∩ 𝑑 = 𝑖)) )}
          ↔
          ↔ ◦ 𝜌↔   ↔          ←
                              ←                    ←                 ↔
                                                                     ↔          ←
                                                                                ←                    ′                      ′      ←
    (3) 𝜌 disj                                     ·                                                                               ·
                   exists ◦ 𝜌 frame {(𝑃𝑖 , c, 𝑄 𝑖 ) ) | 𝑖 ∈ 𝐼 } = 𝜌 exists ◦ 𝜌 frame {(∪𝑖 ∈𝐼 (𝑃𝑖 ∩ 𝑑 = 𝑖), c, ∪𝑖 ∈𝐼 (𝑄 𝑖 ∩ 𝑑 = 𝑖)) )}
          ↔
          ↔        ↔
                   ↔          ←
                              ←                    ·                 ↔
                                                                     ↔          ←
                                                                                ←                    ′                      ′      ·
    (4) 𝜌 disj ◦ 𝜌 exists ◦ 𝜌 frame {(𝑃𝑖 , c, 𝑄𝑖 ) ← ) | 𝑖 ∈ 𝐼 } = 𝜌 exists ◦ 𝜌 frame {(∪𝑖 ∈𝐼 (𝑃𝑖 ∩ 𝑑 = 𝑖), c, ∪𝑖 ∈𝐼 (𝑄𝑖 ∩ 𝑑 = 𝑖)) ← )}
  Proof. We only show the proof for the first statement, as the others are analogous. We proceed
by simply calculating the two closures separately and proving they are equal.
    ↔
    ↔            →
               → {(∪             ′                       ′
  𝜌 exists ◦ 𝜌 frame 𝑖 ∈𝐼 (𝑃𝑖 ∩ 𝑑 = 𝑖), c, ∪𝑖 ∈𝐼 (𝑄 𝑖 ∩ 𝑑 = 𝑖))}
         ↔
       ↔ {((∪             ′                             ′                                  ′
   = 𝜌 exists 𝑖 ∈𝐼 (𝑃𝑖 ∩ 𝑑 = 𝑖)) • 𝑅, c, (∪𝑖 ∈𝐼 (𝑄 𝑖 ∩ 𝑑 = 𝑖)) • 𝑅) | 𝑅 ∈ F, (∪𝑖 ∈𝐼 (𝑃𝑖 ∩ 𝑑 = 𝑖)) ▶◀ 𝑅}
         ↔
       ↔ {((∪ 𝑃 ) • 𝑅, c, (∪ 𝑄 ) • 𝑅) | 𝑅 ∈ F, (∪ 𝑃 ) ▶◀ 𝑅}
   = 𝜌 exists 𝑖 ∈𝐼 𝑖        𝑖 ∈𝐼 𝑖               𝑖 ∈𝐼 𝑖
         ↔
       ↔ {(∪ 𝑃 • 𝑅, c, ∪ 𝑄 • 𝑅) | 𝑅 ∈ F, 𝑖 ∈ 𝐼 .𝑃 ▶◀ 𝑅}
   = 𝜌 exists 𝑖 ∈𝐼 𝑖    𝑖 ∈𝐼 𝑖                   𝑖
   = {(∃X. ∪𝑖 ∈𝐼 𝑃𝑖 • 𝑅, c, ∃X. ∪𝑖 ∈𝐼 𝑄𝑖 • 𝑅) | 𝑅 ∈ F, 𝑖 ∈ 𝐼 .𝑃𝑖 ▶◀ 𝑅, X ⊆ Xl }
   = {(∪𝑖 ∈𝐼 ∃X.𝑃𝑖 • 𝑅, c, ∪𝑖 ∈𝐼 ∃X.𝑄𝑖 • 𝑅) | 𝑖 ∈ 𝐼, 𝑅 ∈ F, 𝑃𝑖 ▶◀ 𝑅, X ⊆ Xl }
         ↔
       ↔ {(∃X.𝑃 • 𝑅, c, ∃X.𝑄 • 𝑅) | 𝑖 ∈ 𝐼, 𝑅 ∈ F, 𝑃 ▶◀ 𝑅, X ⊆ X }
   = 𝜌 disj    𝑖            𝑖                      𝑖           l
         ↔       ↔
       ↔ ◦ 𝜌 ↔ {(𝑃 • 𝑅, c, 𝑄 • 𝑅) | 𝑖 ∈ 𝐼, 𝑅 ∈ F, 𝑃 ▶◀ 𝑅}
   = 𝜌 disj  exists 𝑖       𝑖                      𝑖
         ↔
       ↔ ◦ 𝜌↔    ↔     →     →
   = 𝜌 disj exists ◦ 𝜌 frame {(𝑃𝑖 , c, 𝑄 𝑖 ) | 𝑖 ∈ 𝐼 }
42                                                                       Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


where in the second step we used the fact that 𝑑 ′ = 𝑖 ∈ F.                                                                 □

D.2     Proofs of Sec.5
We note that generic heaps Hi described by the assertion language within the memory model
i ∈ {1, 2} must be of the following form:

           H1 = emp          ∗ x ↦→ x
                         i∈ {1,...,n}
                                        i,1       i,2       H2 = emp         ∗ x ↦→ x
                                                                         i∈ {1,...,n}
                                                                                        i,1   i,2       ∗ x ̸↦→
                                                                                                    j∈ {1,...,m}
                                                                                                                   j


i.e., a (finite) separating conjunction of ownership predicate and negative heap assertion (only in
the model 2) along with the empty assertion. Then, a generic memory takes the following form:
                                               Ü i         
                                          Mi =     Hk ∧ P k
                                                          k∈K

                                              i
i.e., a disjunction of structural (Hk ) and pure (Pk ) assertions. Although the assertion language only
accounts for finite disjunction, infinite disjunctions are encoded using the existential quantifier.
   For each of the memory models 1 and 2, we define, respectively, two memories M̂1 and M̂2 :

                       M̂1 ≜ (a′  1 ∗ emp) ∨ (a′  2 ∗ k1′ ↦→ k2′ )
                       M̂2 ≜ (a′  1 ∗ emp) ∨ (a′  2 ∗ k1′ ↦→ k2′ ) ∨ (a′  3 ∗ k1′ ̸↦→)

     Lemma D.1. Each assertion Mi can be rewritten in a normal form ∃a′ .M̂i ∗ M′ for some M′ .

  Proof. We only show the proof for memory model 2 since it includes the case for memory
model 1. We proceed by induction on the structure of M2 , using the letter P for pure assertions:
Case M2 ≜ P:
We rewrite P ≡ ∃a′ .M̂2 ∗ P and we prove the equivalence by proving separately the two implications.
⇒) Suppose (𝑠, ℎ) ∈ ⦃P⦄ then (𝑠, ℎ) ∈ ⦃∃a′ .a′  1 ∗ emp ∗ P⦄ = ⦃emp ∗ P⦄ = ⦃P⦄ which is one
     of the disjunct of M̂2 .
⇐) Suppose that (𝑠, ℎ) ∈ ⦃∃a′ .M̂2 ∗ P⦄, then by definition of ∗ we know that ∃𝑣, ℎ 1, ℎ 2 .(𝑠 [a′ ↦→
     𝑣], ℎ 1 ) ∈ ⦃M̂2 ⦄ and (𝑠 [a′ ↦→ 𝑣], ℎ 2 ) ∈ ⦃P⦄. Then since a′ is a fresh variable (𝑠, ℎ 2 ) ∈ ⦃P⦄
     and since P is a pure assertion also (𝑠, ℎ 1 • ℎ 2 ) ∈ ⦃P⦄.
Case M2 ≜ H2 :
To rewrite H2 in the normal form, we proceed by induction on the structure of H2 :
      (1) If H2 = emp then emp ≡ ∃a′ .M̂2 ∗ a′  1
      (2) If H2 = x ↦→ y then x ↦→ y ≡ ∃a′ .M̂2 ∗ (a′  2 ∗ k1′  x ∗ k2′  y)
      (3) If H2 = x ̸↦→ then x ̸↦→≡ ∃a′ .M̂2 ∗ (a′  3 ∗ k1′  x)
      (4) If H2 = H1 ∗ H2 then H1 ∗ H2 ≡ ∃a′ .M̂2 ∗ ((H1 ∗ H2′ ) ∨ (H1′ ∗ H2 )) with H1 ≡ ∃a′ .M̂2 ∗ H1′
          and H2 ≡ ∃a′ .M̂2 ∗ H2′ .
The first three equivalences are trivial, so we only prove (4):
⇒) Suppose (𝑠, ℎ) ∈ ⦃H1 ∗ H2 ⦄. By definition of ∗, there exists ℎ 1, ℎ 2 s.t. ℎ = ℎ 1 • ℎ 2 , (𝑠, ℎ 1 ) ∈ ⦃H1 ⦄
     and (𝑠, ℎ 2 ) ∈ ⦃H2 ⦄. By definition of H1 and H2 we have (𝑠, ℎ 1 ) ∈ ⦃∃a′ .M̂2 ∗ H1′ ⦄ and
     (𝑠, ℎ 2 ) ∈ ⦃∃a′ .M̂2 ∗ H2′ ⦄. By definition of ∗, there exists ℎ 1′ , ℎ 1′′, ℎ 2′ , ℎ 2′′ s.t. ℎ 1 = ℎ 1′ • ℎ 1′′ ,
     ℎ 2 = ℎ 2′ • ℎ 2′′ , (𝑠, ℎ 1′ ) ∈ ⦃M̂2 ⦄, (𝑠, ℎ 1′′ ) ∈ ⦃H1′ ⦄, (𝑠, ℎ 2′ ) ∈ ⦃M̂2 ⦄, (𝑠, ℎ 2′′ ) ∈ ⦃H2′ ⦄. Then (𝑠, ℎ 1′ •
     ℎ 1′′ • ℎ 2 ) ∈ ⦃M̂2 ∗ H1′ ∗ H2 ⦄ and so also (𝑠, ℎ 1′ • ℎ 1′′ • ℎ 2 ) ∈ ⦃∃a′ .M̂2 ∗ H1′ ∗ H2 ⦄. Furthermore,
     (𝑠, ℎ 1 • ℎ 2′ • ℎ 2′′ ) ∈ ⦃H1 ∗ M̂2 ∗ H2′ ⦄ and so also (𝑠, ℎ 1 • ℎ 2′ • ℎ 2′′ ) ∈ ⦃∃a′ .H1 ∗ M̂2 ∗ H2′ ⦄.
Systematic Design of Separation Logics                                                                              43


⇐) Suppose (𝑠, ℎ) ∈ ⦃∃a′ .M̂2 ∗ ((H1 ∗ H2′ ) ∨ (H1′ ∗ H2 ))⦄. By definition of ∗ and ∃, there exists
       𝑣, ℎ 1, ℎ 2 s.t. ℎ = ℎ 1 •ℎ 2 , (𝑠 [a′ ↦→ 𝑣], ℎ 1 ) ∈ ⦃M̂2 ⦄ and (𝑠 [a′ ↦→ 𝑣], ℎ 2 ) ∈ ⦃(H1 ∗ H2′ ) ∨ (H1′ ∗ H2 )⦄.
       We proceed by case on the disjuncts of the assertion (H1 ∗ H2′ ) ∨ (H1′ ∗ H2 ):
          • Suppose (𝑠 [a′ ↦→ 𝑣], ℎ 2 ) ∈ ⦃H1 ∗ H2′ ⦄. Then by definition of ∗ there exists ℎ 2′ , ℎ 2′′ s.t.
              (𝑠 [a′ ↦→ 𝑣], ℎ 2′ ) ∈ ⦃H1 ⦄ and (𝑠 [a′ ↦→ 𝑣], ℎ 2′′ ) ∈ ⦃H2′ ⦄. Then (𝑠 [a′ ↦→ 𝑣], ℎ 1 •ℎ 2′′ ) ∈ ⦃H2 ⦄.
              Then (𝑠 [a′ ↦→ 𝑣], ℎ 1 • ℎ 2′ • ℎ 2′′ ) ∈ ⦃H1 ∗ H2 ⦄.
          • The other case is dual.
Case M ≜ P ∧ H2 :
        2

By inductive hypothesis H2 ≡ ∃a′ .M̂2 ∗ H′ , then we rewrite P ∧ H2 ≡ ∃a′ .M̂2 ∗ P ∧ H′ :
                    P ∧ H2 ≡ P ∧ ∃a′ .M̂2 ∗ H′ ≡ ∃a′ .P ∧ M̂2 ∗ H′ ≡ ∃a′ .M̂2 ∗ P ∧ H′
where we used the fact that a′ is a fresh variable.
Case M2 ≜ P ∗ H2 :
By inductive hypothesis H2 ≡ ∃a′ .M̂2 ∗ H′ , then we rewrite P ∗ H2 ≡ ∃a′ .M̂2 ∗ ((P ∗ H2 ) ∨ (P ∗ H′ )).
The proof is analogous to the proof of the rewriting of H1 ∗ H2 .
Case M2 ≜ M1 ∨ M2 :
By inductive hypothesis M1 ≡ ∃a′ .M̂2 ∗ M1′ and M2 ≡ ∃a′ .M̂2 ∗ M2′ , then we rewrite
M1 ∨ M2 ≡ ∃a′ .M̂2 ∗ (M1′ ∨ M2′ ):
M1 ∨ M2 ≡ (∃a′ .M̂2 ∗ M1′ ) ∨ (∃a′ .M̂2 ∗ M2′ ) ≡ ∃a′ .( M̂2 ∗ M1′ ) ∨ ( M̂2 ∗ M2′ ) ≡ ∃a′ .M̂2 ∗ (M1′ ∨ M2′ )
where we used the distributivity of the ∗ over ∨.
Case M2 ≜ ∃X.M1 :
By inductive hypothesis M1 ≡ ∃a′ .M̂2 ∗ M1′ , then we rewrite ∃X.M1 ≡ ∃a′ .M̂2 ∗ (∃X.M1′ ):
                 ∃X.M1 ≡ ∃X.(∃a′ .M̂2 ∗ M1′ ) ≡ ∃a′ .∃X.M̂2 ∗ M1′ ≡ ∃a′ .M̂2 ∗ (∃X.M1′ )
                                                                                                                    □

  Lemma D.2. We can rewrite M̂1 and M̂2 in the following forms:
    (1) M̂1 ≡ H ∗ M̂ with H = emp
    (2) M̂2 ≡ H ∗ M̂2 with H = emp
    (3) M̂2 ≡ H ∗ (emp ∨ (a  3 ∗ k1 ̸↦→)) with H = ((a  1 ∗ emp) ∨ (a  2 ∗ k1 ↦→ k2 ))
   Theorem 5.1 (SL+ Sound and Relative Complete for Loop-Free Programs). Let r ∈ Reg and
                  i                                                          i
P, Q ∈ Ast, then ⊢SL+ {P} r {Q} ⇒ JrKSL                        SL
                                     i ⦃P⦄ ⊆ ⦃Q⦄. Moreover, JrKi ⦃P⦄ ⊆ ⦃Q⦄ ⇒⊢SL+ {P} r {Q}
when r is loop-free.
   Proof. Soundness can be proved by induction on the derivation tree. Relative completeness
for loop-free programs will be proved for the memory model 1 since the proof for 2 is analogous,
                                                                                   1
but it uses M̂2 . We suppose that JrKSL
                                     1 ⦃P⦄ ⊆ ⦃Q⦄ and we prove that the triple ⊢SL+ {P} r {Q}
is derivable in SL+. In particular, we show that we can derive the exact postcondition, then by
applying the consequence rule, we can derive any (expressible) over-approximation. The proof
proceeds by induction on the structure of r.
Case r ≜ c:
By Lemma D.1 we have P ≡ ∃a′ .M̂1 ∗ P′ and by Proposition D.2 we also have P ≡ ∃a′ .emp ∗ M̂1 ∗ P′
which are respectively equivalent to:
    (1) P ≡ ∃a′, X′ .empXp ∗ emp∗M̂1 ∗ P′ [X′ /Xp ]
    (2) P ≡ ∃a′, X′ .empXp ∗ M̂1 ∗P′ [X′ /Xp ]
44                                                                         Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


In gray, we outline the idle part of the memories that can be added at a later time, while in black,
we outline the minimal memory needed for the execution of atomic commands. In particular, the
black part of (1) is the minimal memory needed for the execution of b?, x := e and x := alloc() and
the black part of (2) for free(x), x := [y] and [x] := y. We proceed by case for (1) and (2):
    (1) We show a derivation for the triple {P} c {JcKSL  1 P} by starting with the black part of (1):
                                        1
                 M̂1 ∗ P′ [X′ /Xp ] ∈ F⊢SL+ {empXp } c {JcKSL               1    ′ ′
                                                              1 (empXp )} M̂ ∗ P [X /Xp ] ⊲⊳ (empXp )                       i
                     1                                                                                               {Frame}+
                    ⊢SL+ {empXp ∗ M̂1 ∗ P′ [X′ /Xp ]} c {JcKSL           1   ′ ′
                                                            1 (empXp ∗ M̂ ∗ P [X /Xp ])}                        i
       1                                                                                                 {Exists}+
      ⊢SL+ {∃a′, X′ .empXp ∗ M̂1 ∗ P′ [X′ /Xp ]} c {∃a′, X′ .JcKSL           1   ′ ′
                                                                1 (empXp ∗ M̂ ∗ P [X /Xp ])}         i
                                           1                                                   {Cons}+
                                          ⊢SL+ {P} c {JcKSL
                                                         1 P}

           To conclude the proof for this case, we compute the exact semantics for each atomic
           command on the minimal memory, showing that it is expressible in the assertion language:
             • Jb?KSL
                   1 ⦃empXp ⦄ = {(𝑠, ℎ) | (𝑠, ℎ) ∈ ⦃empXp ⦄, LbM𝑠 = true} = ⦃empXp ∧ b⦄
             • Jx := eKSL
                       1 ⦃empXp ⦄
                  = {(𝑠 [x ↦→ LeM𝑠], ℎ) | ∀y ∈ Xp .∃y′ ∈ Xl .𝑠 (y) = 𝑠 (y′ )}
                  = {(𝑠 [x ↦→ Le[x′ /x]M𝑠], ℎ) | ∀y ∈ Xp .∃y′ ∈ Xl .𝑠 (y) = 𝑠 (y′ )}
                  = ⦃empXp \{x} ∧ x = e[x′ /x]⦄
             • Jx := alloc()KSL
                             1 ⦃empXp ⦄
                  = {(𝑠 [x ↦→ 𝑙], ℎ[𝑙 ↦→ 𝑣]) | (𝑠, ℎ) ∈ ⦃empXp ⦄, 𝑣 ∈ V}
                  = {(𝑠 [x ↦→ 𝑙], [𝑙 ↦→ 𝑣]) | ∀y ∈ Xp .∃y′ ∈ Xl .𝑠 (y) = 𝑠 (y′ ), 𝑣 ∈ V}
                  = ⦃empXp \{x} ∗ x ↦→ _⦄
                                                                                                  i                             i
              This exact postcondition can be obtained from axiom {Alloc}+ by using rule {Exists}+ .
     (2) Although empXp ∗ M̂1 being the minimal memory for the execution of free(x), x := [y]
         and [x] := y, their executions on the empty heap yelds the abort state abort, which is not
         expressible in our assertion language. Then, the minimal part of the memory needed for the
         execution of commands free(x), x := [y] and [x] := y yielding an expressible postcondition
         is described by the assertion M1 ≜ empXp ∗ (a′  2 ∗ k1′ ↦→ k2′ ). We show a derivation for
         the triple {∃a′, X′ .M1 ∗ P[X′ /Xp ]} c {JcKSL   ′ ′           ′
                                                     1 (∃a , X .M1 ∗ P[X /Xp ])} by starting from M1 :
                                               1
                 P′ [X′ /Xp ] ∈ F          ⊢SL+ {M1 } c {JcKSL
                                                            1 M1 }         P′ [X′ /Xp ] ⊲⊳ M1
                                                                                                                           i
                  1                                                                                             {Frame}+
                 ⊢SL+ {M1 ∗ P′ [X′ /Xp ]} c {JcKSL       ′ ′
                                                1 (M1 ∗ P [X /Xp ])}                                        i
       1                                                                                         {Exists}+
      ⊢SL+ {∃a, X′ .M1 ∗ P′ [X′ /Xp ]} c {∃a, X′ .JcKSL       ′ ′
                                                     1 (M1 ∗ P [X /Xp ])}

           To conclude the proof for this case, we compute the exact semantics for each atomic
           command on the minimal memory, showing that it is expressible in the assertion language:
                                      ′       ′    ′
             • Jfree(x)KSL
                         1 ⦃empXp ∗ a  2 ∗ x ↦→ k2 ⦄
                 ={(𝑠, []) | ∀y ∈ Xp .∃y′ ∈ Xl .𝑠 (y) = 𝑠 (y′ ), 𝑠 (a′ ) = 2}
                 =⦃empXp ∗ a′  2⦄
                                         ′       ′    ′
             •     Jx := [y]KSL
                             1 ⦃empXp ∗ a  2 ∗ y ↦→ k2 ⦄
                 ={(𝑠 [x ↦→ k2′ ], [y′ ↦→ k2′ ]) | ∀z ∈ Xp .∃z′ ∈ Xl .𝑠 (z) = 𝑠 (z′ ), 𝑠 (a′ ) = 2}
                 =⦃empXp \{x} ∗ a′  2 ∗ y′ ↦→ k2′ ∗ x  k2′ ⦄
Systematic Design of Separation Logics                                                                        45

                                       ′       ′    ′
            •    J[x] := yKSL
                           1 ⦃empXp ∗ a  2 ∗ x ↦→ k2 ⦄
                ={(𝑠, [x′ ↦→ y]) | ∀y ∈ Xp .∃y′ ∈ Xl .𝑠 (y) = 𝑠 (y′ ), 𝑠 (a′ ) = 2}
                =⦃empXp ∗ a′  2 ∗ x′ ↦→ y⦄
Case r ≜ r1 ; r2 :
Let us assume that Jr1 ; r2 KSL
                             1 ⦃P⦄ = ⦃Q⦄. By definition of sequential composition Jr1 ; r2 K1 =
                                                                                                SL

Jr2 KSL      SL                                                                          SL
     1 (Jr1 K1 ⦃P⦄). By inductive hypothesis on r1 there exists an assertion S s.t. Jr1 K1 ⦃P⦄ = ⦃S⦄
      1
and ⊢SL+ {P} r1 {S} is provable. Furthermore, by inductive hypothesis on r2 there exists an assertion
                               1
Q s.t. Jr2 KSL
            1 ⦃S⦄ = ⦃Q⦄ and ⊢SL+ {S} r2 {Q} is provable. Then, by applying rule of Seq, we can
derive ⊢𝑆𝐿+ {P} r1 ; r2 {Q}:
                                   1                     1
                                 ⊢SL+ {P} r1 {S}       ⊢SL+ {S} r2 {Q}            i
                                             1                               {Seq}+
                                            ⊢SL+ {P} r1 ; r2 {Q}
Case r ≜ r1 + r2 :
Let us assume that Jr1 + r2 KSL
                             1 ⦃P⦄ = ⦃Q⦄. By inductive hypothesis on r1 there exists an assertion
                                        1
Q1 s.t. Jr1 KSL
             1 ⦃P⦄ = ⦃Q1 ⦄ and ⊢SL+ {P} r1 {Q1 } is provable. By inductive hypothesis on r2 there
                                                              1
exists an assertion Q2 s.t. Jr2 KSL
                                 1 ⦃P⦄ = ⦃Q2 ⦄ and ⊢SL+ {P} r2 {Q2 }. Furthermore, by definition of
nondeterministic choice Jr1 + r2 KSL             SL           SL
                                    1 ⦃P⦄ = Jr1 K1 ⦃P⦄ ∪ Jr2 K1 ⦃P⦄ = ⦃Q1 ∨ Q2 ⦄. Then by applying
                                                                  1
the rule of choice and consequence, we can derive ⊢SL+ {P} r1 + r2 {Q1 ∨ Q2 }:
                        1                                          1
                       ⊢SL+ {P} r1 {Q1 }             i
                                                                  ⊢SL+ {P} r2 {Q2 }         i
                   1                           {Cons}+        1                       {Cons}+
                  ⊢SL+ {P} r1 {Q1 ∨ Q2 }                     ⊢SL+ {P} r2 {Q1 ∨ Q2 }             i
                                        1                                             {Choice}+
                                       ⊢SL+ {P} r1 ; r2 {Q1 ∨ Q2 }
                                                                                                              □

  Theorem 5.2 (ISL+ Sound and Relative Complete for Loop-Free Programs). Let r ∈ Reg
                       i                                                          i
and P, Q ∈ Ast, then ⊢ISL+ [P] r [Q] ⇒ ⦃Q⦄ ⊆ JrKISL                       ISL
                                                i ⦃P⦄. Moreover, ⦃Q⦄ ⊆ JrKi ⦃P⦄ ⇒⊢ISL+
[P] r [Q] when r is loop-free.
  Proof. The proof proceeds like the proof of Theorem 5.1 and by using Lemma D.2.                             □

    Theorem 5.3 (State-wise completeness). Given a program r and two states (𝜖 : (𝑠, ℎ)), (𝜖 :
(𝑠 ′, ℎ ′ )) such that, (𝜖 : (𝑠 ′, ℎ ′ )) ∈ JrKISL
                                               i (𝜖 : (𝑠, ℎ)), for every assertion P such that (𝑠, ℎ) ∈ ⦃P⦄ there
                                                              i
exists an assertion Q such that (𝑠 ′, ℎ ′ ) ∈ ⦃Q⦄ and ⊢ISL+ [P] r [Q] is provable.
  Proof. The proof proceeds by induction on the structure of r:
Case r ≜ c:
Atomic commands are loop-free programs. Completeness is established in Theorem 5.2.
Case r ≜ r1 ; r2 :
We suppose (𝜖 : (𝑠 ′, ℎ ′ )) ∈ Jr1 ; r2 KISL
                                         i (𝜖 : (𝑠, ℎ)) with (𝑠, ℎ) ∈ ⦃P⦄. By definition, we distinguish the
two cases:
     • (𝑒𝑟 : (𝑠 ′, ℎ ′ )) ∈ Jr1 KISL
                                 i (𝜖 : (𝑠, ℎ)): By inductive hypothesis there exists an assertion Q such
                                                                              i            i
          that [P] r1 [Q] and (𝑠 ′, ℎ ′ ) ∈ ⦃Q⦄. By using rule [SeqEr] + we conclude ⊢ISL+ [P] r1 ; r2 [Q].
46                                                                            Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


      • (𝑜𝑘 : (𝑠 ′′, ℎ ′′ )) ∈ Jr1 KISL                       ′ ′            ISL       ′′ ′′
                                    i (𝜖 : (𝑠, ℎ)) and (𝜖 : (𝑠 , ℎ )) ∈ Jr2 Ki (𝑜𝑘 : (𝑠 , ℎ )). By inductive
                                                                                   i
       hypothesis there exists an assertion S such that ⊢ISL+ [P] r1 [S] and (𝑠 ′′, ℎ ′′ ) ∈ ⦃S⦄.
                                                                                          i
       Again by inductive hypothesis, there exists an assertion Q such that ⊢ISL+ [S] r2 [Q] and
                                                 i                 i
       (𝑠 ′, ℎ ′ ) ∈ ⦃Q⦄. By using rule [Seq] + we conclude ⊢ISL+ [P] r1 ; r2 [Q].
Case r ≜ r1 + r2 :
We suppose (𝜖 : (𝑠 ′, ℎ ′ )) ∈ Jr1 + r2 KISL                   ISL                   ISL
                                         i (𝜖 : (𝑠, ℎ)) = Jr1 Ki (𝜖 : (𝑠, ℎ)) ∪ Jr2 Ki (𝜖 : (𝑠, ℎ)). Then there
must exists i ∈ {1, 2} such that (𝜖 : (𝑠 ′, ℎ ′ )) ∈ Jri KISL
                                                          i (𝜖 : (𝑠, ℎ)). We suppose i = 1 since the other
                                                                                                                      i
case is analogous. By inductive hypothesis there exists an assertion Q such that ⊢ISL+ [P] r1 [Q]
                                                                        i
and (𝑠 ′, ℎ ′ ) ∈ ⦃Q⦄. To conclude the proof, we show a derivation for ⊢ISL+ [P] r1 + r2 [Q]:
                                  by induction                                                          i
                                i                   i                                   [Empty] +
                               ⊢ISL+ [P] r1 [Q] ⊢ISL+ [P] r2 [false]                                     i
                                         i                                              [Choice] +
                                        ⊢ISL+ [P] r1 + r2 [Q]
Case r ≜ r∗1 :
We suppose (𝜖 : (𝑠 ′, ℎ ′ )) ∈ Jr∗1 KISL                         i ISL
                                                         Ð
                                      i (𝜖 : (𝑠, ℎ)) =     i∈N Jr1 Ki (𝜖 : (𝑠, ℎ)). Then there must exists
an m ≥ 0 such that Jrm       ISL
                          1 Ki (𝜖 : (𝑠, ℎ)), i.e. there exists a sequence of states {𝜎i } 0≤i≤m where
𝜎0 = 𝜖 : (𝑠, ℎ), 𝜎𝑚 = 𝜖 : (𝑠 , ℎ ′ ) and 𝜎i+1 ∈ Jr1 KISL
                             ′
                                                     i 𝜎i . By inductive hypothesis, fixed P0 = P, there
                                                                                                    i
exists a sequence of assertions {Pi }0≤i≤m such that 𝜎i ∈ ⦃Pi ⦄ and ⊢ISL+ [Pi ] r1 [Pi+1 ] is provable
                                                                   i
for all 0 ≤ i ≤ m. We take Q = Pm and we show a derivation for ⊢ISL+ [P] r∗1 [Q]:
                                            i
    i                        [Iterate-zero] +
  ⊢ISL+ [P0 ] r∗1 [𝜖 : P0 ]
              ..
               .                         i                 by induction
  i                            [Iterate] +        i
 ⊢ISL+ [P0 ] r∗1 [𝜖 : Pm−2 ]                     ⊢ISL+ [Pm−2 ] r1 [𝜖 : Pm−1 ]                 i
                         i                                                          [Seq] +
                        ⊢ISL+ [P0 ] r∗1 ; r1 [𝜖 : Pm−1 ]              i                                      by induction
                           i                               [Iterate] +                               i
                          ⊢ISL+ [P0 ] r∗1 [𝜖 : Pm−1 ]                                               ⊢ISL+ [Pm−1 ] r1 [𝜖 : Pm ]        i
                                                              i                                                                  [Seq] +
                                                             ⊢ISL+ [P0 ] r∗1 ; r1 [𝜖 : Pm ]                  i
                                                                  i                               [Iterate] +
                                                              ⊢ISL+ [P0 ] r∗1 [𝜖 : Pm ]
                                                                                                                                       □
Systematic Design of Separation Logics                                                                                     47


                                                                                                                       1
                                              1                                                                  {Load}+
                                             ⊢SL+ {empXp ∗ y ↦→ v} x := [y] {empXp \{x} ∗ y ↦→ v ∧ x = v}
                                         1                                                                                 1
    1                            {Assume}+                     1                                                 {Frame}+
 ⊢SL+ {empXp } false? {false}                                 ⊢SL+ {false} x := [y] {false}
                                                                                                   1
                             1                                                                {Seq}+
                         ⊢SL+ {empXp } (false?; x := [y]) {false}
                                                                           1
                         1                                          {Cons}+
                        ⊢SL+ {empXp } (false?; x := [y]) {empXp }
                                                                               1
                                             †                      {Choice}+
                                                  1                                                                1
          1                           {Assume}+        1                                               {Assume}+
         ⊢SL+ {empXp } true? {empXp }                ⊢SL+ {empXp } true? {empXp }
                                                                                                             1
                            1                                                                          {Seq}+
                           ⊢SL+ {empXp } (true?; true?) {empXp }
                                                                          1
                                                      ‡                        {Choice}+
                                                  †       ‡                                                                1
             1                                                                                               {Choice}+
            ⊢SL+ {empXp } (false?; x := [y]) + (true?; true?) {empXp }
                                                                                                         1
    1                                                                                         {Frame}+
 ⊢SL+ {empXp ∗ x ↦→ _} (false?; x := [y]) + (true?; true?) {empXp ∗ x ↦→ _}
                                                                                                        1
              1                                                                               {Exists}+
             ⊢SL+ {x ↦→ _} (false?; x := [y]) + (true?; true?) {x ↦→ _}
Fig. 12. A sample derivation in SL+ showing that it is more expressive than SL: the triple {x ↦→ _} r {x ↦→ _}
is not derivable in SL.

E       Detailed Examples
This appendix contains the full derivations of sample triples discussed in the paper. They witness the
increased expressiveness of SL+ and ISL+ w.r.t. SL and ISL, respectively. For the sake of readability
and to avoid including uninformative intermediate steps, we rely on two facts in the derivations.
   First, according to the new frame rule, we only add memories that constrain logical vari-
ables. Nonetheless, if, for example, we need to use a frame x′ ↦→ _ on a memory where x  x′ ,
then we directly use the assertion x ↦→ _ on the program variable. This prevents the need to
apply the frame rule followed by the consequence rule to substitute an equivalent assertion:
x  x′ ∗ x′ ↦→ _ ≡ x  x′ ∗ x ↦→ _.
   Second, when we apply the exists rule, we rely on the fact that ∃x′ .x = x′ ∗ x ↦→ _ is equivalent to
x ↦→ _, when x′ is a logical variable. Again, this prevents the need to apply the exists rule followed
by the consequence rule to substitute an equivalent assertion.
   Example E.1 (SL+ more expressive than SL). Let us take r ≜ (false?; x := [y]) + (true?; skip).
As shown in Section 1 in SL we can derive the triple {emp} r {emp} but we cannot extend such triple
with a frame x ↦→ _ because x ∈ mod(r) and we cannot apply the frame rule, despite the assignment
x := [y] is dead code. In Figure 12, we show a derivation in SL+ for the triple {x ↦→ _} r {x ↦→ _}. Note
that, according to Section 2 we have that skip ≜ true?.

   Example E.2 (ISL+ more expressive than ISL). Let us take r ≜ x := alloc(); free(y); x := [y]. As
shown in Section 1 in ISL the triple [y ↦→ v] r [y ̸↦→ ∗ x ↦→ _] cannot be derived. This is because when
handling the command x := [y] after y has been deallocated, we end up in an error, without any actual
modification to the variable x. Despite that, we cannot use the frame rule to frame out the assertion on
x ↦→ _ due to the side condition mod(r) ∩ fv(R) = ∅, which prevents the frame from mentioning the
variable x, leading to the impossibility of apply the local axiom for x := [y]. A possible derivation in
ISL+ for such a triple is shown in Figure 13.
48                                                             Roberto Bruni, Lorenzo Gazzella, and Roberta Gori


                                                                                      2
                         2                                                     [Alloc] +
                        ⊢ISL+ [empXp ] x := alloc() [empXp \{x} ∗ x ↦→ z′ ]
                                                                                                           2
              2                                                                            [Frame] +
             ⊢ISL+ [empXp ∗ y ↦→ v] x := alloc() [empXp \{x} ∗ x ↦→ z′ ∗ y ↦→ v]
                                                                                                           2
              2                                                                            [Exists] +
             ⊢ISL+ [empXp ∗ y ↦→ v] x := alloc() [empXp \{x} ∗ x ↦→ _ ∗ y ↦→ v]
                                                                                                       2
                   2                                                                       [Cons] +
                  ⊢ISL+ [empXp ∗ y ↦→ v] x := alloc() [empXp ∗ x ↦→ _ ∗ y ↦→ v]
                                                                                               2
                                                                                      [Seq] +
                                                (†)

                                                                                      2
                          2                                                   [Free2] +
                        ⊢ISL+ [empXp ∗ y ↦→ z′ ] free(y) [empXp ∗ y ̸↦→]
                                                                                                                    2
      2                                                                                                    [Frame] +
     ⊢ISL+ [empXp ∗ y ↦→ z′ ∗ z′  v ∗ x ↦→ _] free(y) [empXp ∗ y ̸↦→ ∗ z′  v ∗ x ↦→ _]
                                                                                                                   2
               2                                                                                           [Exists] +
             ⊢ISL+ [empXp ∗ y ↦→ v ∗ x ↦→ _] free(y) [empXp ∗ y ̸↦→ ∗ x ↦→ _]
                                                                                                   2
                                                                                         [Seq] +
                                                (‡)

                                                                                           2
                          2                                                   [LoadEr3] +
                         ⊢ISL+ [empXp ∗ y ̸↦→] x := [y] [empXp ∗ y ̸↦→]
                                                                                                       2
                  2                                                                      [Frame] +
              ⊢ISL+ [empXp ∗ y ̸↦→ ∗ x ↦→ _] x := [y] [empXp ∗ y ̸↦→ ∗ x ↦→ _]
                                                                                               2
                                                                                         [Seq] +
                                                (★)

                                          (†)   (‡)   (★)                            2
                         2                                                     [Seq] +
                        ⊢ISL+ [empXp ∗ y ↦→ v] r [empXp ∗ y ̸↦→ ∗ x ↦→ _]
                                                                                           2
                                  2                                            [Exists] +
                                 ⊢ISL+ [y ↦→ v] r [y ̸↦→ ∗ x ↦→ _]

Fig. 13. A sample derivation in ISL+ showing that it is more expressive than ISL: the triple
[y ↦→ v] r [y ̸↦→ ∗ x ↦→ _] is not derivable in ISL.
