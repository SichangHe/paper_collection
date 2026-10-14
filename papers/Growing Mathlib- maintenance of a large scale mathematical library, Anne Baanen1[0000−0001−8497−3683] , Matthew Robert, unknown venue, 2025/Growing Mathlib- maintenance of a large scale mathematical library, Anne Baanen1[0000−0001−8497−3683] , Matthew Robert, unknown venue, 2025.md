                                            Growing Mathlib: maintenance of a large scale
                                                      mathematical library

                                                    Anne Baanen1[0000−0001−8497−3683] , Matthew Robert
                                                2[0000−0001−5819−0159]
                                         Ballard                     , Johan Commelin1,3[0009−0000−2025−9771] , Bryan
                                                    [0000−0002−7023−7252]
                                        Gin–ge Chen                       , Michael Rothgang4[0009−0001−8307−4122] , and
                                                             Damiano Testa5[0009−0004−5949−6861]
                                                                         1
                                                                          Lean FRO, USA
arXiv:2508.21593v2 [cs.PL] 7 Oct 2025




                                                               2
                                                                University of South Carolina, USA
                                                  3
                                                    Mathematical Institute, Utrecht University, The Netherlands
                                                     4
                                                         Mathematical Institute, University of Bonn, Germany
                                                       5
                                                          Mathematical Institute, University of Warwick, UK



                                              Abstract. The Lean mathematical library Mathlib is one of the fastest-
                                              growing libraries of formalised mathematics. We describe various strate-
                                              gies to manage this growth, while allowing for change and avoiding main-
                                              tainer overload. This includes dealing with breaking changes via a dep-
                                              recation system, using code quality analysis tools (linters) to provide
                                              direct user feedback about common pitfalls, speeding up compilation
                                              times through conscious library (re-)design, dealing with technical debt
                                              as well as writing custom tooling to help with the review and triage of
                                              new contributions.

                                              Keywords: Formal mathematics · Library development · Linting.


                                        1    Introduction
                                        The mathematical library Mathlib [36], written in the Lean theorem prover,
                                        is perhaps the fastest-growing library of formalised mathematics. Created in
                                        2017, it now contains 1.9 million lines of code across a broad range of subjects.
                                        Mathlib’s focus on being an integrated library for mathematics makes it well-
                                        suited for formalising current research mathematics. Recent formalised results
                                        based on Mathlib include a fundamental result of Scholze and Clausen about
                                        condensed mathematics [33, 7, 6], Smale’s sphere eversion via an h-principle [9],
                                        Campos–Griffiths–Morris–Sahasrabudhe’s breakthrough on upper bounds for di-
                                        agonal Ramsey numbers [28] and Gowers–Green–Manners–Tao’s breakthrough
                                        on Marton’s polynomial Freiman–Rusza conjecture [13, 12, 20]. Mathlib is also
                                        crucial for Buzzard’s ongoing project [5] to formalise a proof of Fermat’s Last
                                        Theorem. In a different direction, Mathlib has been used in industry research,
                                        such as for verifying the correctness of the SampCert differential privacy frame-
                                        work [26].
                                            Mathlib is run by a community of users as an open source project, enabling
                                        and encouraging contributions by users with a wide range of backgrounds and
2        A. Baanen et al.

expertise. This allows for a broad range of contributions (of formalisations, but
also with the infrastructure and other supporting work). At the same time, this
presents challenges around knowledge transfer and ensuring the library stays
coherent as a whole. To address this, Mathlib makes extensive user of linters, to
help users with intricacies of the Lean proof assistant and enforce certain global
coherence properties. (We describe this in Section 4.)
    Mathlib’s continued growth also presents other challenges for scaling. Some
of these are technical—such as adapting existing code to other changes in the li-
brary (Section 3), ensuring that Mathlib continues to compile reasonably quickly
(see Section 5) and managing technical debt (see Section 6). With any large
group, social processes become pertinent (such as, ensuring all communication
stays friendly and welcoming (Mathlib has a code of conduct with a dedicated
team enforcing it), or keeping some alignment on an overall vision of Mathlib).
A key process in both maintaining a coherent library and teaching new contrib-
utors about formalisation best practices is mandatory code review. This process
needs to be supported and adapted to scale to the influx of contributions (see
Section 7).
    We describe the Mathlib community’s strategies for dealing with this growth,
focusing on the above aspects in turn. The use of linters (in a less extensive way)
was already described in previous work [37]; the other sections are new. While
some details are specific to Lean and Mathlib, we believe that many of them
apply broadly to libraries of formal mathematics knowledge.


2     Related work
Various interactive theorem provers have come to enjoy large libraries of research
mathematics—each with its own strengths and weaknesses. The Mizar Mathe-
matical Library [2] is the oldest and perhaps the largest library (at 3.7 millions
lines of code (MLOC)) of formalised mathematics. The Isabelle/HOL system
has very powerful automation; the Archive of Formal Proofs (AFP; 4.8 MLOC6 )
still has the strongest complex analysis library. The Rocq theorem prover allows
expressing complex mathematical objects (such as schemes, the tangent space of
a manifold or vector bundles) more naturally, thanks to its foundations including
dependent types. While its mathematical components library [23] is significantly
smaller (150 000 lines of code), Rocq has been used to formalise major results
such as the Four Colour and the Feit–Thompson theorems (which are each of
similar size as the mathematical components). Let us also mention the Flyspeck
project [15] as an example of combining large libraries in two different proof
assistants.
     The MML introduced mandatory review of contributions in 2006, as well
as tooling to check for duplicate lemmas. (Such tooling also exists for Rocq [10]
and Lean [31].) Klein et al have written [4] about maintaining large-scale Isabelle
6
    The AFP has a broader focus [3], with about half its current articles covering the
    analysis and verification of particular algorithms. Arguably, this makes the MML a
    larger library of formalised mathematics.
          Growing Mathlib: maintenance of a large scale mathematical library        3

libraries. They name many challenges similar to ours, including coordination and
collaboration in large and diverse projects. The Isabelle system also employs
custom linters [27] — which are not mandated for existing entries, but enforced
for new submissions. Zimmermann [39] has written about recent changes to
Rocq’s development processes (including switching to GitHub and a pull-request
based model, dealing with breaking changes and the challenges with distributing
reviews). There is also custom tooling to support Rocq maintainers [40]. Huch’s
in-progress PhD thesis [17] describes efforts to address scaling issues in the AFP,
including a discussion of maintainenance efforts.
     Growing a large formal library can require changes to the underlying prover.
Such work on Lean is out of scope of this paper; Wenzel discussed it for Isabelle
[38]. They also describe tooling to automatically test the impact of core system
or theory changes on dependent projects.7 Test-case minimisation [14] can also
be instrumental for quickly diagnosing and fixing broken proofs “downstream”.
Huch and Wenzel have also written about the challenges of maintaining and
scaling Isabelle’s supporting infrastructure [18, 19].
     There is also considerable work on proof repair, such as adjusting code to
breaking changes. Luan et al [22] have studied and classified compatibility issues
in the AFP. Tan et al [35] have developed tooling for automatically fixing proofs
in Isabelle/HOL. Gopinathan et al [11] have developed proof repair tooling for
the Rocq prover.
     Despite the growth of large libraries of formal proofs, there is still relatively
little work describing tools and best practices for their maintenance. Ringer et
al [32] note the gap between proof engineering and software engineering in this
respect.


3     The deprecation system

Maintaining Mathlib involves changing existing code. Generalizations, refactors,
reorganization of content, syntax changes and so on are exceedingly common in
Mathlib. As a result, code written for one version of Mathlib may no longer
compile with a newer version. This applies both within Mathlib (contributions
to one area need to deal with effects on all other areas), to contributions under
review and particularly to projects depending on Mathlib. Many large formali-
sation projects are carried out in a repository depending on Mathlib. If keeping
up with the latest Mathlib changes is too onerous, contributing results back to
Mathlib may become impossible.
    The spectrum of possible breaking changes is rather diverse, and ranges from
one-off changes when upgrading to the next Lean version to adjusting to par-
ticular refactorings in Mathlib. In principle, Lean’s excellent meta-programming
facilities allow writing custom migrations for virtually all changes, transforming
working code from one version to the next. Theoretically, such migrations could
be arbitrarily complicated. In practice, however, the vast majority of adjustments
7
    Similar tooling for Lean does not exist yet, but is being planned by the Lean FRO.
4         A. Baanen et al.

are very simple to deal with: renaming (the declaration which states) a theorem
or definition, renaming files (which requires adjusting import statements) and
superficial syntax changes. The third item is addressed through dedicated syntax
linters (see Section 4); these can also help with semantic changes.
    Lean has a deprecation system specifically designed to handle renamings
gracefully. When a declaration is renamed, for a grace period of several months,
we add a deprecation marker documenting the rename. This connects the old
and new names (and allows providing a custom message to guide the migration
process). Upon using a deprecated declaration, the user sees a warning, indicating
which declaration to use instead. This allows for a much smoother migration.
    Dealing with renamed files is harder. Lean looks at file imports before the
deprecation system (which is implemented as a linter) has the chance to run—so
a file that imported the file with the old name would stop building entirely. The
solution is similar: the module with the old name is not erased, but is preserved
and stained. Thus, it can be imported without breaking the build—and a linter
suggests to replace the old module name, with appropriate imports. These could
be either the direct imports of that module, in the case of a reorganization of
content; or the renamed module, in the case of a simple move. This informs users
of where the declarations that were present in the old file may have ended up.


4      Semantic linters

In general terms, a linter is a program whose purpose is to ensure that the
code in a project satisfies certain requirements. The term requirements should
be interpreted very broadly: a linter could enforce

    – code style conventions (such as the default indentation of code);
    – file naming conventions (such as never using paths that differ only in capi-
      talization);
    – function naming conventions (such as making sure that namespaces in dec-
      larations are not repeated);
    – deprecating commands that have been replaced by newer code;

and in fact Mathlib uses linters for all of these purposes.
    To be precise, Mathlib uses two different linter frameworks, with distinct
strengths and weaknesses. Lean itself provides a Lean.Elab.Command.Linter
type, which contains the linter’s name and a monadic function that takes the
syntax of the command as input and can run arbitrary code.8 Lean’s community-
maintained extended library Batteries provides the parallel structure
Batteries.Tactic.Lint.Linter that is similar to the Lean-native linters, but
takes a declaration name as its input and runs code in a different monad. For
the purpose of the present discussion, the main difference between the two kinds
of linters is that the former is designed to run on every command and has access
8
    Technically, a linter function returns a Unit, i.e. the only interesting outcomes of the
    linter are its side effects.
         Growing Mathlib: maintenance of a large scale mathematical library              5

to the syntax tree of each command, while the latter is designed to run once
on the “final” environment and only inspects the declarations present in the
Environment. We refer to the former linters as “syntax linters” and to the latter
linters as “environment linters”. Both are semantic linters, in the sense that they
can access the fully elaborated information and not merely the typed syntax.
Since both frameworks allow running arbitrary code, the distinction between
them is mostly on what they are expected to do and what they can do easily,
not on what they could do. Environment linters are good for global validation
(e.g. checking lemmas are in simp normal form), but only warn you after the
fact. Syntax linters warn you right away and are best suited for local validation
(e.g. the valid notation λ x => x is deprecated in favour of fun x 7→ x).
    At the time of writing, there are 26 syntax linters defined in Mathlib and 10
more coming from its dependencies, as well as 17 environment linters, all but two
defined in Batteries. We mostly focus on the syntax linters: virtually all the
environment linters have been described previously [37].9 To summarize more
coherently how Mathlib uses linters, let us group them into general categories
and highlight a few examples from each category.

Deprecation linters As mentioned in the previous section, linters help deal-
ing with deprecations. Breaking changes could arise from certain tactics be-
coming more powerful or more efficient, making other tactics obsolete or un-
desirable. In such situations, the replaced tactics would be deprecated. The
deprecatedSyntax linter warns about the use of deprecated syntax (e.g. a tac-
tic), and informs the user what the new preferred expression is.

Style linters Mathlib has a fairly detailed style guide (which helps to settle
discussions about individual formatting preferences efficiently). Mathlib’s style
linters enforce various aspects of coding style and formatting, such as line length,
whitespace conventions or the formatting of documentation comments. This al-
lows reviewers to focus their time on higher-level aspects, and helps contributors
learn about Mathlib style without having to read all style rules at once. We also
enforce that every Mathlib file (that is not an import-only file) contains a valid
copyright header and a module doc-string summarising the content of the file.

Import structure linters Keeping track of Mathlib’s import structure is im-
portant for organisation and compilation speed. A Lean module can only be
compiled once all its dependencies have been fully checked10 : thus, a reasonable
9
   With the advent of Lean 4, the need for the typeclass linters described there has
   mostly disappeared: typeclass inference was substantially redesigned in Lean 4 [34],
   taking into account the insights from Mathlib development. This means some linter
   warnings have become compiler errors, and the others have become less relevant and
   did not get reimplemented in Lean 4.
10
   Lean’s upcoming module system will change this trade-off, if and when it is adopted
   in mathlib. (Doing so is desirable in principle, but requires a lot of conscious library
   design work.)
6       A. Baanen et al.

import structure enables parallelism and faster overall compilation. It also speeds
up local development, as changing multiple files requires less recompilation, and
makes it easier to place a new mathematical result. Mathlib has two main tools
to help with keeping the import structure organised: Mario Carneiro’s shake
tool warns about unused imports, and the directoryDependency linter warns
about unintentional dependencies between different areas of Mathlib.


Code pruning Another class of linters highlights redundant code. For instance,
the unusedVariable linter warns when a variable in scope (such as a hypothesis
in a proof) is not used. While using Lean as a proof assistant, this helps catch
“free” generalizations of theorems, where a hypothesis that seemed to be needed
turns out to be superfluous. While using Lean as a general purpose programming
language, this is more often useful to catch bugs, as an unused variable may arise
from an incorrect reference, or the omission of part of a case analysis.
    Linters with similar scope are the unusedSeqFocus, the unusedTactic, and
the unreachableTactic linters, each highlighting different ways in which a tactic
proof can be simplified or streamlined.


Tracking issues Certain commands are expected to be rarely used, or are only
temporary adaptations. For instance, increasing the time limit for type-checking
is something that may be necessary for an individual declaration, but increasing
the limit for a whole file is likely a symptom of some deeper issue that should
be addressed. Hence, a command such as set_option maxHeartbeats 5000000
should be limited in scope to a single declaration. The setOption linter does
exactly that: it flags uses of set_option maxHeartbeats x suggesting to use
set_option maxHeartbeats x in ... instead.
    Similar linters exist for open Classical, which can hide issues that will
make the code less usable, and the globalAttributeIn linter that warns that
the scope of certain attributes is not “local”, even in the presence of the (usually)
scope-limiting in keyword.


4.1   Maintenance and code readability

The linters in this category are specifically geared to improve maintainability
of code and readability. Since Mathlib evolves very quickly, code breakage is
fairly common; any tooling which can diagnose and prevent such breakages is
immensely helpful. The linters in this section try to be pro-active about code
breakage by reducing code brittleness.

Rigid and flexible tactics The flexible linter starts from the premise that tac-
tics exhibit two general behaviours: “flexible” tactics (such as simp, norm_num
or aesop) apply to a wide variety of goals and return similarly varied processed
goals; “rigid” tactics (such as rw or apply) perform some very specific operations
and may stop working even with very small changes of the current goal state.
        Growing Mathlib: maintenance of a large scale mathematical library        7

    The flexible linter tracks hypotheses and goals in each proof, following
them around as various tactics are successively applied. Whenever a “flexible”
tactic modifies a hypothesis or a goal, no “rigid” tactic is supposed to modify
that same hypothesis or goal: indeed, the behaviour of the flexible tactic may
change, e.g. because a new simp lemma allows further simplification, making
the following rw fail. Thus, preventing rigid tactics from following flexible ones
helps with maintainability. This question has some nuance: for instance, some
flexible tactics (such as ring or omega) are “normalizing”: even though they take
a variety of inputs, their output is more predictable. Therefore, rigid tactics
following a normalizing flexible tactic are allowed.


Handling multiple side-goals In terms of goal management and readability, the
multiGoal linter warns as soon as a tactic produces more than one side-goal,
unless the next tactic is the focusing dot ·. The code style enforced by this linter
makes both the number of side-goals that remain after each tactic application
as well as which parts of the code deal with which part of the proof completely
transparent. This helps with maintenance, since it limits code breakage to easily
identified branches, rather than a generic total failure. At the same time, it also
improves code readability and structure, since the various arms of the proofs are
visually differentiated.


Closing sections Finally, let us mention the missingEnd linter: it warns on
section commands that do not have a matching end closure. This addresses
a maintainability issue: when moving code from one file to another, it is easy to
miss the closing of a section, producing a dangling one. As a consequence, the
scope of the currently non-ended section is persisted where it was not intended
to be—and further hypotheses or declarations might be in scope. This can cause
issues that are hard to diagnose, such as changing the meaning of statements or
breaking proofs.



Helpful and pedagogical suggestions Some linters attempt to preempt pos-
sible misunderstanding or common pitfalls. The haveLet linter flags uses of have
when introducing a non-Prop assumption and similarly uses of let when intro-
ducing an assumption in Prop. Especially using have for let can cause confusion
when the actual term introduced by the tactic is important for the proof.
    Another example is the prototype papercut linter. One common mistake is
accidentally using subtraction of natural numbers (which truncates at 0). The
linter flags such subtraction when a positivity assumption is not in scope.
    All linters defined in Mathlib are available to projects using Mathlib: any
improvements thus benefit the broader ecosystem. Projects can easily adopt all of
Mathlib’s linters (or any subset thereof they choose). This helps maintaining code
standards and styling conventions, and makes the ecosystem more homogeneous.
8      A. Baanen et al.

5     Speeding up Mathlib
As Mathlib grows to encompass more declarations, the time to build it will
also increase. Keeping build times manageable requires constant attention to
sources of slowdowns and inefficiencies. The Mathlib Speedcenter is an instance
of the benchmarking server VelCom that builds and benchmarks all commits to
the master branch of Mathlib. The benchmarks include overall measurements
for Lean components such as the simplifier or typeclass inference, and per-file
compilation timings. In addition to wall-clock (overall time from start to finish)
and task-clock (takes into account parallelism) times measured in seconds, most
benchmark results are measured in instructions, since the number of instructions
is more stable on the benchmarking servers than the wall-clock time which is
affected by process scheduling. Continuous monitoring of build times is crucial
to ensure no unexpected slowdowns occur. Therefore, a bot reports notable out-
liers in benchmarks (changes of a measurement by 5% or more) on the Lean
community Zulip chat.

5.1   Speed and typeclasses
Mathlib relies on the Lean typeclass system to perform automatic inference of
many implicit arguments. Typeclasses are flexible and have low infrastructure
requirements on user code, but the flexibility also means designs have to be
carefully consider to optimize their tradeoffs. As the typeclass hierarchy grows,
synthesis of instances becomes slower since a larger search space needs to be ex-
plored. It is not only important to ensure synthesis succeeds quickly: if synthesis
fails, tactics can decide to fall back on an alternative proof strategy. Lean’s in-
stance synthesis algorithm fails only after exploring the full search space, and it
is therefore especially important that the space does not grow too large.
    One fundamental consideration in Mathlib’s typeclass design is the level
of bundling [1, 36], which concerns the way conjunctions of assumptions are
modeled in classes. For example, to represent ordered commutative monoids,
we can define a bundled class OrderedCommMonoid that combines CommMonoid,
PartialOrder and hypotheses stating the monoid operations respect the or-
der structure. Instead, unbundling the ordered algebra classes results in mix-
ins combining the (existing) algebra class CommMonoid with the (existing) or-
der class PartialOrder and adding in an extra IsOrderedMonoid class. Un-
bundling makes parameters more verbose: [OrderedCommMonoid M] becomes
[CommMonoid M] [LinearOrder M] [IsOrderedMonoid M]. As described with
more detail in [1], bundled design is preferred for its conciseness in Mathlib when
possible.
    The speed tradeoffs changed when upgrading from Lean 3 to Lean 4. A conse-
quence of the bundled approach to typeclass design is that the number of classes
becomes multiplicative when extending along two distinct axes. Taking the
OrderedCommMonoid class as an example formerly found in Mathlib, this could
then be extended in the order hierarchy to give LinearOrderedCommMonoid, or
in the algebraic hierarchy to give OrderedCommGroup, or in both directions to
           Growing Mathlib: maintenance of a large scale mathematical library    9

give LinearOrderedCommGroup. When looking for a CommMonoid instance, Lean
would search through both the algebraic hierarchy and the ordered algebraic
hierarchy.
    Unbundling curbs this multiplicative growth by allowing expansion along
individual axes. This means to strengthen from ordered monoids to ordered
groups, no additional ordering axioms are required, and it suffices to replace a
[CommMonoid M] parameter with [CommGroup M]. Similarly, for linear ordered
monoids we can replace [PartialOrder M] with [LinearOrder M]. The result
of unbundling is that the search through the one large search space is now
three searches through smaller spaces, and failing fast on one of these cancels
the remaining searches too. This refactor by Yuyang Zhao resulted in a 20%
decrease in typeclass inference time, resulting in a 6% overall speedup to Mathlib
compilation.

5.2     Speed and coercions
The coercion system is another commonly used component of Lean. Essentially,
when a term t is inferred to have type A, where type B is expected, Lean at-
tempts to find a suitable coercion, so the term can be replaced with a coerced
version written ↑t. The coercion is found by synthesizing an instance of the
typeclass CoeT A t B. Since coercions are triggered by type mismatches, this is
a particular case of instance search that should fail fast.
    Instances for CoeT should not be declared directly, but rather chained to-
gether from the CoeHead, CoeOut, Coe and CoeTail typeclasses. The rules for
which typeclass to instantiate for a particular coercion are subtle and not uni-
versally understood; they are notably more complex compared to Lean 3. As
a consequence, a seemingly acceptable instance can cause a large performance
regression. For example, Coe A B allows B to be a free variable, but doing so
causes large performance regressions since such an instance always applies.11
    In a similar vein to Subsection 5.1, large hierarchies extending coercion type-
classes should be avoided. Mathlib uses the FunLike hierarchy to generalize over
bundled homomorphisms. Morphism classes such as MonoidHomClass used to
extend the FunLike class, which meant a failing coercion would first trigger a
search through the entire FunLike hierarchy. Even worse, since MonoidHomClass
depends on Monoid instances, this also triggers a search through the algebraic
hierarchy. The solution was to unbundle inheritance from FunLike, keeping only
FunLike and EquivLike and passing these classes as an instance parameter to
every morphism class. The refactor by Anne Baanen performing this unbundling
resulted in a 33% speedup for typeclass instance synthesis and an overall 19%
decrease in build instructions.

5.3     Speed and definitional equality
Type checking, and definitional equality in particular, is commonly invoked in
the Lean elaboration and kernel checking process and can result in arbitrarily
11
     https://github.com/leanprover-community/mathlib4/pull/22950
10        A. Baanen et al.

complex computations: terms can be large and their size can increase further
when unfolding definitions referenced by the term. Equality checks are intended
to be “cheap” basic steps in implementing more complex routines such as type-
class instance synthesis, so slowdowns in checking have a large impact.
    Generally, definitions are designed to not require unfolding unless the unfold-
ing is requested. Each definition in Lean has a transparency level controlling the
circumstances in which it is unfolded. Most tactics are designed to only unfold
definitions explicitly marked as reducible, with some tactics also unfolding at
the default semireducible transparency level. Marking definitions as irreducible
prevents unfolding altogether, skipping a potentially expensive equality check if
it does not obviously succeed.
    A particular example of complex definitional equality checking can be found
in structure declarations. Large structures can already be quite complex terms
in themselves, which can be hidden behind further definitions and constructions,
and the possibility of diamond inheritance can then result in nonobvious equality
checks. This all results in high levels of unfolding being required to verify the
equality of terms.
    Typeclasses in Lean are implemented as structures, so the complex typeclass
hierarchy also has an impact here. The Field typeclass has 19 data-carrying
structure fields that must be checked for equality. By ensuring typeclass in-
stances are already in a normal form, less unfolding will be needed. Matthew
Robert Ballard, Kyle Miller and Eric Wieser implemented the fast_instance
term elaboration macro that normalizes instance declarations by unfolding defi-
nitions and replacing subterms with synthesized instances. An initial implemen-
tation of this macro resulted in a 5% decrease in type checking time and halved
compilation times for many files.12


5.4     Speed and tactics

During the compilation of Mathlib, Lean spends approximately 14% of its time
running the simp tactic, and 7% of the time invoking other tactics. Tactics are
diverse in the ways they are implemented and invoked, but we can attempt to
find some rules of thumb for optimization.
    An important change in Lean 4 was the addition of discrimination trees [25,
30] that allow for efficient association of terms with values. A discrimination tree
is a tree datastructure whose branches are indexed by symbols (either a constant,
or the special symbol * representing free variables). Values are stored at leaf
nodes. A closed term where each symbol has a fixed arity can be represented as
a string of symbols; this maps directly to a particular path in the tree. Queries
into a discrimination tree overapproximate the result, since all variables map
to the same symbol *. Still, the approximation is much finer than previously in
Lean 3, where terms were indexed by only the first constant that appeared [29].
    The simplifier tries to repeatedly rewrite using a set of lemmas and tactics
(called a simp set) on all subterms in an expression. By querying a discrimina-
12
     https://github.com/leanprover-community/mathlib4/pull/20993
           Growing Mathlib: maintenance of a large scale mathematical library       11

tion tree, it can quickly determine potentially relevant rewrites. Optimization
practices common in the Lean 3 version of Mathlib have become much less nec-
essary after the port to Lean 4, such as restricting simp from the default large
simp set to a smaller specific list (using the simp only keywords) since many
fewer lemmas have to be tested for applicability. Going from simp only to simp
lowers the maintenance burden, since a change to the default simp set does not
need to be copied to each involved simp only call.
    The simp sets still need to be restricted for efficiency if multiple lemmas could
apply depending on different hypotheses. For example, div_self a : a / a = 1
applies if a is in a Group, but a field does not form a multiplicative group. There-
fore, the field_simp tactic specialized to simplifying expressions in the theory
of fields excludes such lemmas from the set for efficiency.13
    Another avenue to optimizing the use of tactics is to use weaker, faster tactics
instead of more powerful but slower tactics. The Aesop tactic provides general
proof search [21] and is also invoked as part of other, more specialized tactics to
discharge goals. The general nature of this proof search makes Aesop very pow-
erful, but this power is often unnecessary when the proof it needs to find has a
predetermined format. We have found that replacing powerful Aesop-based tac-
tics like measurability with tactics that have a simpler strategy like fun_prop
is almost always possible and reduces running time appreciably. Similarly, small
tweaks such as applying local hypotheses or trying reflexivity to discharge an
equality goal before starting Aesop can lead to appreciable speedups.14


6      Tracking and addressing technical debt

Ward Cunningham introduced [8] the term technical debt in 1992, writing:

      Shipping first time code is like going into debt. A little debt speeds
      development so long as it is paid back promptly with a rewrite. Objects
      make the cost of this transaction tolerable. The danger occurs when the
      debt is not repaid. Every minute spent on not-quite-right code counts as
      interest on that debt. Entire engineering organizations can be brought
      to a stand-still under the debt load of an unconsolidated implementation

This concept is all the more important in a large foundational library like Math-
lib, especially in light of its cohesive and tightly integrated nature. In this section
we describe various types of technical debt we have encountered in Mathlib, and
how the community tracks and addresses them.

Porting notes From 2021–2023, the community ported Mathlib from Lean 3 to
Lean 4. This process ought to be documented in more detail elsewhere, but for
the purposes of the present discussion we summarize the points of interest.
13
     https://github.com/leanprover-community/mathlib4/pull/21326
14
     https://github.com/leanprover-community/mathlib4/pull/21330
12      A. Baanen et al.

    For all practical purposes, Lean 4 is a distinct language from Lean 3—there
is no backwards compatibility. Mario Carneiro wrote a tool mathport that au-
tomatically translates Lean 3 code to Lean 4 code on a best-effort basis, and
a small group of people implemented the common tactics in Lean 4. In Octo-
ber/November 2022, this preparatory work transitioned into a wide-scale and
coordinated effort to port the theory files of Mathlib. Over the course of 10
months, the community ported on the order of a million lines of code, or roughly
a dozen files per day.
    Naturally, there were many places where a faithful translation was not possi-
ble. For the sake of speed, the porting team decided to liberally annotate issues
with “porting notes” that described the problem and the workaround. As a re-
sult, by the summer of 2023, the porting process was complete, but Mathlib 4
contained well over 5000 porting notes.
    Pietro Monticone made a valiant effort to organize and classify the porting
notes in February and March of 2024. Subsequently, Anne Baanen, Kim Morri-
son, and Johan Commelin processed and addressed over two thirds of the porting
notes in the first quarter of 2025. Many of these porting notes became obsolete
because of new and expanded functionality in Lean 4. At the time of writing,
roughly 1500 porting notes remain.

Adaptation notes and backwards compatibility flags New versions of Lean 4 are
released on a monthly basis. Mathlib maintains a branch that tracks the nightly
releases, which simplifies migrating to the new version of Lean 4 when it is re-
leased. This tracking branch provides feedback for the development of Lean 4: if
the daily transition to a new nightly version of Lean 4 requires some unsatisfac-
tory workarounds, then these are annotated with #adaptation_note comments.
In essence, these notes have the same functionality as porting notes. Occasion-
nally, there is no simple solution for a problem that arises from a new version
of Lean 4. In such an event the old feature can be re-enabled via a backwards
compatibility flag. This allows the Mathlib community to transition to the new
version of Lean 4 at a reasonable pace.

Reporting technical debt The shell script scripts/technical-debt-metrics.sh
is used to create a report of the current state of known technical debt in Mathlib.
This includes tracking adaptation notes, porting notes and backwards compati-
bility flags. Continuous integration runs this script on a weekly basis, and posts
the report (including the delta with respect to the previous week) to the Zulip
chat of the Lean community. Additionally, this report is computed for each pull
request, and posted to a dedicated “PR summary” comment at the top of the
pull request. This allows the reviewer to quickly see the current state of technical
debt in the pull request, and take this into account when deciding whether to
approve the pull request.
    Mathlib also has a mechanism in place to surface pull requests addressing
technical debt: this includes both a dedicated label and triage dashboard (see
Section 7.2) and a Zulip stream where such PRs can be brought to attention.
         Growing Mathlib: maintenance of a large scale mathematical library           13

   One downside of tracking and reporting technical debt in this manner is in-
dicated by Goodhart’s Law: “When a measure becomes a target, it ceases to be
a good measure.” In this context, this means that the community is inclined to
focus on the technical debt that is being tracked, whereas there may be other
forms of technical debt that fly under the radar. To alleviate this, there is a
dedicated thread on the Lean community’s Zulip chat listing less measurable
forms of technical and organisational debt. (One example of the latter is doc-
umenting unwritten informal Mathlib policy: sharing such knowledge enables
other contributors to learn this for themselves and lowers the barrier towards
contribution. An example of the former is reorganizing top-level directories: due
to Mathlib’s age, some of these are not coherent any more.) Everybody can add
items to the list, facilitating a collective understanding of future maintenance
tasks.


7    Scaling code review
Since its beginning, the Mathlib library required code review prior to merging
changes. This is enforced through the bors bot: pull requests are merged auto-
matically upon approval by an authorised user (i.e., a Mathlib maintainer).15
    This policy has several reasons. For one, formalisation in Lean ensures a
strong level of correctness: a formalised mathematical proof which compiles with-
out any sorry16 will be a correct and complete proof. However, designing an inte-
grated mathematical library well still requires expert knowledge: usually, there
are different potential designs, with vastly different usability and ergonomics.
Code review is one way to form and share common knowledge about design best
practices. It also has an empowering function: new contributors can propose new
code, without being afraid of breaking other proofs (if their code compiles, the
proofs are still fine) or overlooking important aspects—because an experienced
Lean user will look over their contribution. This way, code review is a way of
teaching and onboarding new contributors.
    Mathlib is growing steadily, as is its influx of new contributions. At the
same time, many of its contributors are volunteers or work on Mathlib as a side
project. Most of Mathlib’s maintainers have teaching, administrative or supervi-
sion commitments: allowing Mathlib to scale requires lightening their work. This
has both social and technical aspects. On the social side, maintaining Mathlib
means embracing teamwork and delegating responsibility. Approval of Mathlib
pull requests is a multi-stage system, allowing many people to contribute.
    Code review in Mathlib is decentralised: everybody is allowed and encouraged
to review contributions; there are guidelines teaching what to review for. This
ranges from more basic aspects (such as adherence to Mathlib’s style guidelines,
or whether new documentation is comprehensible) to advanced aspects like the
15
   Using bors also enforces the not rocket science principle [16]: ensuring that the main
   (development) branch of Mathlib always passes all continuous integration tests.
16
   and is not intentionally manipulating the Lean environment or adding additional
   axioms—both of which are checked for by Mathlib’s continuous integration
14      A. Baanen et al.

correct code location and library design patterns. There are regular review meet-
ings, where reviewers and interested contributors review code together—both to
make this work more enjoyable, and to mentor potential new reviewers.
    Mathlib’s maintainers have the final say on approving a pull request. The
number of maintainers keeps growing steadily, and is currently around 30. Main-
tainers have different specialisations; together, they cover the breadth of Mathlib.
Having multiple knowledgeable maintainers in one area is beneficial, so they can
discuss difficult decisions.
    Between maintainers and all contributors is the group of Mathlib reviewers.
These are Mathlib contributors who have provided useful reviews in the past. A
reviewer can approve a pull request by commenting maintainer merge, which
notifies the maintainers. Usually, these get merged (or at least discussed further)
more quickly. This system is a bit like journal referees and editors: the reviewer
group lightens the load on maintainers; the direct notification mechanism pro-
vides an additional small incentive for reviewers. This works well in practice:
in the last year, about one in three merged pull requests was approved by a
reviewer before they were merged.
    On a technical level, we can save reviewer and maintainer time by automating
tedious or mechanical aspects of this process. Two basic means of automation
are using continuous integration with bors and automatic maintainer notifica-
tions through the maintainer merge command. Let us discuss Mathlib’s review
automation from two further angles: tooling for reviewers and tooling for triage.


7.1   Tooling for reviewers

There are multiple ways for automation to support pull request reviewers. To
begin with, we need to find a suitable reviewer for a given pull request. A pull
request with a new theorem is best reviewed by somebody familiar with the
theorem’s area; something similar holds for a contribution improving Mathlib’s
infrastructure, adding a new linter or adding a new tactic. Each new pull request
adding new content is automatically labelled according to its area. There is a file
collecting each reviewer’s area of interest and expertise. This allows automati-
cally suggesting suitable reviewers for every pull request—taking their expertise
and reviewing capacity into account. At the time of writing, this automatic as-
signment is run on an experimental basis. This labelling information has also
been used to identify missing reviewers: if pull requests in a certain area take a
long time to get reviewed, recruiting further reviewers could be worthwhile.
    Secondly, we have created custom tooling exposing important information
to reviewers. When a pull request is filed, a script creates a sticky comment
summarising key information about a PR. This comment is updated in-place as
the pull request is amended. The comment shows which lemmas were renamed
(so reviewers can spot those more easily, and check if deprecation warnings are
present). It also exposes when transitive imports of files change, which is ex-
tremely helpful for reviewing import refactoring. Finally, the summary comment
shows any changes in technical debt metrics.
        Growing Mathlib: maintenance of a large scale mathematical library       15

    Further, there is substantial automation to help with information flow within
the project. Collaboration on Mathlib occurs primarily on two sites: GitHub,
where git repositories including Mathlib and its dependencies are hosted, and
the leanprover-community Zulip, a moderated chat site where community mem-
bers discuss their contributions and other Lean-related topics. Automation can
help with bridging these two venues and keeping some information synchronised.
Whenever a specific pull request is mentioned in the Zulip chat, a script posts
an emoji reaction indicating the current pull request status (such as, whether
it is waiting for author changes, a review or was already merged). This allows
reviewers and maintainers to see at a glance if action has already been taken.
This reaction is updated by a GitHub actions script whenever the pull request’s
status changes.
    We make extensive use of Zulip’s custom linkifier feature to allow users to
link directly to issues or pull requests in the Mathlib repository, Mathlib docu-
mentation entries, and other useful pages.

7.2   Triage tooling
The number of open Mathlib pull requests is growing steadily. At the time of
writing, there are about 1500 open pull requests. Often, new pull requests are
getting reviewed quickly, but their sheer volume makes it difficult to keep track
of every single PR. Better tooling helps to ensure that every pull request is kept
track of and receives a timely response.
    Investigating this closely shows that different users of such tooling have dif-
fering needs. For instance, a reviewer may want to find reviewable pull requests
matching their areas of interest. Mathlib’s maintainers would like to know about
pull requests which were already approved by a reviewer. Other contributors may
be interested in recent pull requests to “see what is going on”, or viewing all pull
requests related to a particular area. Pull request authors may want to see the
status of all their pull requests or find out why their pull request is not on the
review queue. Most importantly, a triage team (see below) keeping track of pull
requests’ state needs better tooling to see the state of each pull request.
    GitHub’s default interface can do many of the above tasks; however, at Math-
lib’s scale we have increasingly run into its limitations. For example, to triage
reviewable pull requests one would like to know the total time a pull request is
already waiting for review. This need not be a continuous time span, so com-
puting this needs to consider a pull request’s change over time. GitHub only
exposes a “last updated” date, which does not provide this. (In addition, this
“last update” measures almost every activity, which is often too sensitive for our
purposes: a bystander’s comment or a notification of a merge conflict resets the
last activity counter, but need not mean review activity.) Similarly, sorting pull
requests by their total diff can be useful information, as is the number of PRs
depending on a given PR.
    We have built a custom editorial tool to address all these shortcomings. Pull
requests are grouped by their status (such as waiting for review, blocked on an-
other pull request or waiting for the author to respond to review comments).
16     A. Baanen et al.

These categories are tailored to Mathlib’s infrastructure (for instance, pull re-
quest failures related to Mathlib’s infrastructure are highlighted automatically,
speeding up the diagnosis and fix). In each category, we compactly display (see
Figure 1) all pull requests together with additional meta-information such as its
author, title and labels, but also additional information such as diff size or the
total time in review. These lists can be semantically sorted by each category.
This tooling can adapt and grow with Mathlib’s needs easily.




      Fig. 1. A typical dashboard from Mathlib’s review and triage dashboard



    We ran a survey among Mathlib contributors, reviewers and maintainers.
The results provided many useful suggestions for improving this tool further
(many of which have already been implemented). The survey result also affirms
that this changes how contributors look for pull requests: the dashboard has
become part of many maintainers’ standard workflow. The triage functionality
in particular is used by maintainers, but also by the newly-founded triage team:
having a common webpage to look at makes this process a lot smoother.
    Under the hood, this dashboard has two components. One keeps a cache,
containing the metadata we care about for every open pull request. Periodically,
we query GitHub’s graphql API to update this data for any pull requests which
received updates, in effect creating a database of each pull request’s relevant
state. The code for this amounts to a few hundred lines of shell and Python
scripts: this could easily be run on a local computer, coupled with a cronjob.
    The other component is responsible for the final user interface. It processes
the downloaded metadata to extract the aggregate data we care about. (For
instance, from the history of all label changes on a pull request, we determine
the total time that PR was ready for review.) Using this metadata, we create
the triage dashboard. The dashboard is a static webpage, using jQuery datata-
bles to create the dashboards in each category: these can be sorted and filtered
dynamically. Using a static webpage means fast response times (filtering a list
of pull requests is almost instantaneous), but means the webpage needs to be
           Growing Mathlib: maintenance of a large scale mathematical library       17

manually refreshed to see updated changes. Altogether, this project consists of
about 4500 lines of Python code, and about 1000 lines of shell scripts, .graphql
schemas etc.


8      Conclusion
Growing Mathlib would be impossible without automation to scale its main-
tainance: this applies on the social, organisational and technical levels. While we
cannot measure its effects precisely, the fact that Mathlib still grows fast shows
how useful it is. For instance, Mathlib’s deprecation system has made updating
to a newer version of Mathlib a much smoother process. Currently, such up-
dates still require manual work, but this task can be automated well: both for
deprecated declarations and modules, there are prototype tools performing the
replacement automatically.
    An auto-formatter for Lean would improve dealing with code style questions
significantly. Lean’s extensibility makes this difficult in general: users can define
new syntax and custom notation, which can drastically change the look and
feel of the language.17 Formatting user-defined syntax and notation requires
knowing the preferred formatting for these. While Mathlib makes extensive use
of custom notation to make its code resemble mathematical notation, this is
relatively benign: all syntax has an associated pretty-printer which indicates
some reasonable formatting.
    Mathlib’s review and triage dashboard is mostly Mathlib-agnostic: the par-
ticular PR categories are tuned to Mathlib, but the underlying logic is not. With
appropriate configuration, other open source projects could use this as well.

Acknowledgements We would like to thank the anonymous referees for their
helpful comments and suggestions. Michael Rothgang was funded by the Deutsche
Forschungsgemeinschaft (DFG, German Research Foundation) under Germany’s
Excellence Strategy – EXC-2047/1 – 390685813. This material is based upon
work supported by the U. S. National Science Foundation Award No. DMS-
2302263.


References
 [1]    Anne Baanen. “Use and Abuse of Instance Parameters in the Lean Math-
        ematical Library”. In: 13th International Conference on Interactive The-
        orem Proving (ITP 2022). Ed. by June Andronick and Leonardo de Moura.
        Vol. 237. Leibniz International Proceedings in Informatics (LIPIcs). Dagstuhl,
        Germany: Schloss Dagstuhl – Leibniz-Zentrum für Informatik, 2022, 4:1–
        4:20. doi: 10.4230/LIPIcs.ITP.2022.4. url: https://drops.dagstuhl.de/
        opus/volltexte/2022/16713.
17
     For example, one can allow users to write in a form of controlled natural language
     [24]: formatting that would be a very different endavour.
18      A. Baanen et al.

 [2]   Grzegorz Bancerek et al. “The Role of the Mizar Mathematical Library
       for Interactive Proof Development in Mizar”. In: Journal of Automated
       Reasoning 61 (June 2018), pp. 9–32. url: https : / / link . springer . com /
       article/10.1007/s10817-017-9440-6.
 [3]   Jasmin Blanchette, Max Haslbeck, Daniel Matichuk, and Tobias Nipkow.
       “Mining the Archive of Formal Proofs”. In: Conference on Intelligent Com-
       puter Mathematics (CICM 2015). Ed. by M. Kerber. Vol. 9150. LNCS.
       Invited paper. Springer, 2015, pp. 3–17.
 [4]   Timothy Bourke, Matthias Daum, Gerwin Klein, and Rafal Kolanski. “Chal-
       lenges and Experiences in Managing Large-Scale Proofs”. In: AISC/MKM/Calculemus.
       2012. url: https://api.semanticscholar.org/CorpusID:11296777.
 [5]   Kevin Buzzard. The Fermat’s Last Theorem Project. Lean community
       blog. Apr. 2024. url: https : / / leanprover - community. github . io / blog /
       posts/FLT-announcement/.
 [6]   Johan Commelin and Adam Topaz. “Abstraction boundaries and spec
       driven development in pure mathematics”. In: Bull. Amer. Math. Soc.
       (N.S.) 61.2 (2024), pp. 241–255. doi: 10 . 1090 / bull / 1831. url: https :
       //doi.org/10.1090/bull/1831.
 [7]   Mathlib Community. “Completion of the Liquid Tensor Experiment”. July
       2022. url: https://leanprover-community.github.io/blog/posts/lte-final/.
 [8]   Ward Cunningham. The WyCash Portfolio Management System. OOP-
       SLA ’92 Experience report. Mar. 1992. url: https://c2.com/doc/oopsla92.
       html.
 [9]   Floris van Doorn, Patrick Massot, and Oliver Nash. “Formalising the h-
       Principle and Sphere Eversion”. In: Proceedings of the 12th ACM SIG-
       PLAN International Conference on Certified Programs and Proofs, CPP
       2023, Boston, MA, USA, January 16-17, 2023. Ed. by Robbert Kreb-
       bers, Dmitriy Traytel, Brigitte Pientka, and Steve Zdancewic. ACM, 2023,
       pp. 121–134. doi: 10.1145/3573105.3575688. url: https://doi.org/10.
       1145/3573105.3575688.
[10]   Ali Ghanbari. “Automatic Goal Clone Detection in Rocq”. In: 39th Eu-
       ropean Conference on Object-Oriented Programming, ECOOP 2025, June
       30 to July 2, 2025, Bergen, Norway. Ed. by Jonathan Aldrich and Alexan-
       dra Silva. Vol. 333. LIPIcs. Schloss Dagstuhl - Leibniz-Zentrum für In-
       formatik, 2025, 12:1–12:19. doi: 10.4230/LIPICS.ECOOP.2025.12. url:
       https://doi.org/10.4230/LIPIcs.ECOOP.2025.12.
[11]   Kiran Gopinathan, Mayank Keoliya, and Ilya Sergey. “Mostly Automated
       Proof Repair for Verified Libraries”. In: Proceedings of the ACM on Pro-
       gramming Languages 7 (2023), pp. 25–49. url: https://dl.acm.org/doi/
       10.1145/3591221.
[12]   W. T. Gowers, Ben Green, Freddie Manners, and Terence Tao. “Marton’s
       Conjecture in abelian groups with bounded torsion”. arXiv:2404.02244
       [math.NT]. url: https://arxiv.org/pdf/2404.02244.pdf.
         Growing Mathlib: maintenance of a large scale mathematical library   19

[13]   W. T. Gowers, Ben Green, Freddie Manners, and Terence Tao. “On a
       conjecture of Marton”. arXiv:2311.05762v2 [math.NT]. url: https://arxiv.
       org/pdf/2311.05762.pdf.
[14]   Jason Gross, Théo Zimmermann, Miraya Poddar-Agrawal, and Adam Chli-
       pala. “Automatic Test-Case Reduction in Proof Assistants: A Case Study
       in Coq”. In: 13th International Conference on Interactive Theorem Prov-
       ing, ITP 2022, August 7-10, 2022, Haifa, Israel. Ed. by June Andronick
       and Leonardo de Moura. Vol. 237. LIPIcs. Schloss Dagstuhl - Leibniz-
       Zentrum für Informatik, 2022, 18:1–18:18. doi: 10.4230/LIPICS.ITP.2022.
       18. url: https://doi.org/10.4230/LIPIcs.ITP.2022.18.
[15]   Thomas Hales et al. “A formal proof of the Kepler conjecture”. In: Forum
       Math. Pi 5 (2017), e2, 29. doi: 10.1017/fmp.2017.1. url: https://doi.org/
       10.1017/fmp.2017.1.
[16]   Graydon Hoare. “technicalities: "not rocket science" (the story of mono-
       tone and bors)”. Feb. 2014. url: https://graydon2.dreamwidth.org/1597.
       html.
[17]   Fabian Huch. “Big Math in Interactive Theorem Provers: Scaling the Is-
       abelle Archive of Formal Proofs”. PhD thesis draft, TU München. 2025.
[18]   Fabian Huch. “Isabelle as Systems Platform: Managing Automated and
       Quasi-interactive Builds”. In: CoRR abs/2412.13083 (2024). doi: 10.48550/
       ARXIV.2412.13083. url: https://arxiv.org/abs/2412.13083.
[19]   Fabian Huch and Makarius Wenzel. “Distributed Parallel Build for the Is-
       abelle Archive of Formal Proofs”. In: 15th International Conference on In-
       teractive Theorem Proving (ITP 2024). Ed. by Yves Bertot, Temur Kutsia,
       and Michael Norrish. Vol. 309. Leibniz International Proceedings in Infor-
       matics (LIPIcs). Dagstuhl, Germany: Schloss Dagstuhl – Leibniz-Zentrum
       für Informatik, 2024, 22:1–22:19. doi: 10.4230/LIPIcs.ITP.2024.22. url:
       https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2024.
       22.
[20]   Jyun-Jie Liao. “Improved Exponent for Marton’s Conjecture in F2n ”. arXiv:2404.09639
       [math.CO]. url: https://arxiv.org/pdf/2404.09639.pdf.
[21]   Jannis Limperg and Asta Halkjær From. “Aesop: White-Box Best-First
       Proof Search for Lean”. In: Proceedings of the 12th ACM SIGPLAN Inter-
       national Conference on Certified Programs and Proofs, CPP 2023, Boston,
       MA, USA, January 16-17, 2023. Ed. by Robbert Krebbers, Dmitriy Tray-
       tel, Brigitte Pientka, and Steve Zdancewic. ACM, 2023, pp. 253–266. doi:
       10.1145/3573105.3575671. url: https://doi.org/10.1145/3573105.3575671.
[22]   Xiaokun Luan et al. “Why the Proof Fails in Different Versions of The-
       orem Provers: An Empirical Study of Compatibility Issues in Isabelle”.
       In: Proceedings of the ACM on Software Engineering (2025). url: https:
       //dl.acm.org/doi/10.1145/3715787.
[23]   Assia Mahboubi and Enrico Tassi. Mathematical Components. 2017.
[24]   Patrick Massot. “Teaching Mathematics Using Lean and Controlled Nat-
       ural Language”. In: 15th International Conference on Interactive Theorem
       Proving (ITP 2024). Ed. by Yves Bertot, Temur Kutsia, and Michael Nor-
20      A. Baanen et al.

       rish. Vol. 309. Leibniz International Proceedings in Informatics (LIPIcs).
       Dagstuhl, Germany: Schloss Dagstuhl – Leibniz-Zentrum für Informatik,
       2024, 27:1–27:19. doi: 10.4230/LIPIcs.ITP.2024.27. url: https://drops.
       dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2024.27.
[25]   William McCune. “Experiments with Discrimination-Tree Indexing and
       Path Indexing for Term Retrieval”. In: J. Autom. Reason. 9.2 (1992),
       pp. 147–167. doi: 10.1007/BF00245458.
[26]   Markus de Medeiros et al. “Verified Foundations for Differential Privacy”.
       In: Proc. ACM Program. Lang. 9.PLDI (June 2025). doi: 10.1145/3729294.
       url: https://doi.org/10.1145/3729294.
[27]   Yecine Megdiche, Fabian Huch, and Lukas Stevens. “A Linter for Isabelle:
       Implementation and Evaluation”. In: CoRR abs/2207.10424 (2022). doi:
       10.48550/ARXIV.2207.10424. url: https://arxiv.org/abs/2207.10424.
[28]   Bhavik Mehta. Formalising modern research mathematics in real time.
       Nov. 2023. url: https : / / xenaproject . wordpress . com / 2023 / 11 / 04 /
       formalising-modern-research-mathematics-in-real-time/.
[29]   Leonardo de Moura and Sebastian Ullrich. “The Lean 4 Theorem Prover
       and Programming Language”. In: Automated Deduction – CADE 28. Ed.
       by André Platzer and Geoff Sutcliffe. Cham: Springer International Pub-
       lishing, 2021, pp. 625–635. url: https://link.springer.com/chapter/10.
       1007/978-3-030-79876-5_37.
[30]   I. V. Ramakrishnan, R. Sekar, and Andrei Voronkov. “Term Indexing”.
       In: Handbook of Automated Reasoning (in 2 volumes). Ed. by John Alan
       Robinson and Andrei Voronkov. Elsevier and MIT Press, 2001, pp. 1853–
       1964. doi: 10.1016/B978-044450813-3/50028-X.
[31]   David Renshaw. Searching for Proof Improvements with tryAtEachStep.
       Conference talk, Lean together 2025. 2025. url: https://researchseminars.
       org/talk/LeanTogether2025/8/.
[32]   Talia Ringer, Karl Palmskog, Ilya Sergey, Milos Gligoric, and Zachary
       Tatlock. “QED at Large: A Survey of Engineering of Formally Verified
       Software”. In: Foundations and Trends® in Programming Languages 5.2-
       3 (2019), pp. 102–281. doi: 10.1561/2500000045.
[33]   Peter Scholze. “Liquid tensor experiment”. In: Exp. Math. 31.2 (2022),
       pp. 349–354. doi: 10.1080/10586458.2021.1926016. url: https://www.
       tandfonline.com/doi/full/10.1080/10586458.2021.1926016.
[34]   Daniel Selsam, Sebastian Ullrich, and Leonardo de Moura. Tabled Type-
       class Resolution. 2020. url: https://arxiv.org/abs/2001.04301.
[35]   Chengsong Tan, Alastair F. Donaldson, Jonathan Julián Huerta y Munive,
       and John Wickerson. “The Burden of Proof: Automated Tooling for Rapid
       Iteration on Large Mechanised Proofs”. In: 2025 IEEE/ACM 13th Inter-
       national Conference on Formal Methods in Software Engineering (For-
       maliSE). 2025, pp. 34–45. doi: 10.1109/FormaliSE66629.2025.00010.
[36]   The mathlib community. “The Lean mathematical library”. In: Proceedings
       of the 9th ACM SIGPLAN International Conference on Certified Programs
       and Proofs, CPP 2020, New Orleans, LA, USA, January 20-21, 2020.
         Growing Mathlib: maintenance of a large scale mathematical library    21

       2020, pp. 367–381. doi: 10.1145/3372885.3373824. url: https://doi.org/
       10.1145/3372885.3373824.
[37]   Floris van Doorn, Gabriel Ebner, and Robert Y. Lewis. “Maintaining a
       Library of Formal Mathematics”. In: Intelligent Computer Mathematics,
       CICM 2020. Vol. abs/2004.03673. 2020. url: https://link.springer.com/
       chapter/10.1007/978-3-030-53518-6_16.
[38]   Makarius Wenzel. Isabelle technology for the Archive of Formal Proofs with
       application to MMT. 2019. url: https://arxiv.org/abs/1905.07244.
[39]   Théo Zimmermann. “Challenges in the collaborative evolution of a proof
       language and its ecosystem”. Theses. Université Paris Cité, Dec. 2019. url:
       https://inria.hal.science/tel-02451322.
[40]   Théo Zimmermann, Julien Coolen, Jason Gross, Pierre-Marie Pédrot, and
       Gaëtan Gilbert. “Extending the team with a project-specific bot”. In:
       CoRR abs/2112.07365 (2021). url: https://arxiv.org/abs/2112.07365.
