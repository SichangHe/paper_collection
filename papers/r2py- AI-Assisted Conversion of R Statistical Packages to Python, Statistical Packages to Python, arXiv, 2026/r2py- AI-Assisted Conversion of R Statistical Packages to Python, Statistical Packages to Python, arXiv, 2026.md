                                            r2py: AI-Assisted Conversion of R
                                              Statistical Packages to Python
arXiv:2608.16911v2 [stat.CO] 19 Aug 2026




                                                                         Yufei Cai
                                                                          Jun Li∗

                                           Department of Applied and Computational Mathematics and Statistics
                                                                  University of Notre Dame
                                                         ∗
                                                             Corresponding author: jun.li@nd.edu




                                                                      August 20, 2026
r2py: AI-Assisted Conversion of R Statistical Packages to Python


Abstract
Thousands of R packages hold statistical methods with no native Python equivalent.
Runtime bridges require an R installation; hand-written ports do not scale. Translation
fails silently where the languages diverge, as in transform normalization, integer width,
and argument evaluation. We present r2py, a framework that converts an R package
into a native Python library using orchestrated language-model agents under human su-
pervision, with correctness established by numerical comparison against the original at
declared tolerances. The compiled code is retained unmodified, so any divergence lies in
the translation. Seven phases decompose the work for independent invocations: structural
analysis fixes conversion order, every base-R construct’s rendering is settled in reviewable
guides before code generation, and four verification methods each expose defects their
predecessors miss. Packages reaching compiled code through .Call() add a five-phase
prologue reconstructing the R C API they use. Conversions of KernSmooth and rpart
reproduce R across 518 and 846 tests.


1    Introduction
R [1] is where a large share of statistical methodology is first implemented. A new
estimator, test or model is typically released as an R package, and that package becomes
the reference implementation the statistical and biomedical communities use, cite and
build upon. rpart [2], the canonical implementation of classification and regression trees
(CART) [3], and KernSmooth [4], implementing the kernel smoothing methods of Wand
and Jones [5], are two of the fifteen packages that carry R’s recommended priority and
ship with every binary distribution of R—fifteen out of roughly twenty-five thousand
packages on the Comprehensive R Archive Network (CRAN) [6], with two thousand more
on Bioconductor [7]. Both represent years of accumulated scrutiny. Within CRAN, 152
packages depend on or import rpart and 107 KernSmooth.
Over the same period Python has become the default environment for scientific computing,
machine learning and production deployment [8, 9, 10]. Neither rpart nor KernSmooth
has a Python equivalent: scikit-learn’s trees [11] do not accept categorical predictors,
and provide no surrogate splits, no cross-validated complexity table and no trees for cen-
sored or count responses; Python’s kernel density estimators lack the plug-in bandwidth
selectors of Wand and Jones. An analyst in Python who needs a method available only
in R has one option: a runtime bridge. rpy2 [12] and reticulate [13] are mature and
widely used, but a bridge does not produce Python software—it requires a full R in-
stallation alongside the Python one and ties the pipeline to an environment where both
runtimes are present and compatible. What is wanted is a native package, installed with
pip and imported like any other.
Native implementations exist, and they are written by hand. PyDESeq2 [14] is a careful
example: a Python reimplementation of the DESeq2 pipeline, tested against reference
outputs from the R package and reported by its authors as producing results similar,


                                             1
r2py: AI-Assisted Conversion of R Statistical Packages to Python


though not numerically identical, to the original. Such projects show the goal is achievable.
They also show what it costs: each is a bespoke effort directed at one package, and none
produces a method the next project can reuse.
Large language models change the arithmetic. Models trained on code translate between
languages with substantial fluency [15, 16, 17, 18], and agentic decomposition extends
what they can be applied to [19, 20]. Applied to code translation this has produced
systems operating on whole projects: Go to Rust, validating input–output equivalence for
an average of 73% of functions in projects of up to 6,600 lines [21], and Java to Python,
decomposing a repository by program analysis and translating fragments in reverse call
order—an ordering we also adopt—with runtime behavior confirmed for about a quarter
of them [22]. Formal verification has been brought to bear where the target is a domain-
specific language [23]. Multilingual benchmarks now include R, but as Rosetta Code tasks
of a few hundred tokens rather than packages [24]. A statistical package needs more on
two axes: its whole public surface, not a validated fraction of it; and numerical agreement
to a declared tolerance, which is stronger than the input–output or functional equivalence
these systems establish.
This is not a matter of passing source files to a model. A package is a dependency graph
dictating what must be translated before what; its numerically intensive work sits in C
or Fortran written against R’s own runtime; a package of any size exceeds a single model
context, so the work must be divided among independent, stochastic invocations sharing
no memory of decisions taken elsewhere; and establishing correctness means comparing
numerical output across the whole public surface, including the error paths ordinary use
does not reach. Hardest of all, R and Python diverge in ways inspection of correct-looking
code does not reveal. R’s fft(inverse=TRUE) returns an unnormalized inverse transform
while NumPy’s ifft divides by N ; R’s var() applies Bessel’s correction while np.var
does not; Fortran INTEGER is 32 bits where NumPy defaults to 64. Each produces plau-
sible numbers that are wrong, with no exception raised. Beyond these, R has constructs
with no Python counterpart at all—S3 dispatch, model formulas, environments—whose
translation is a design decision rather than a lookup.
We present r2py, a framework that converts an R package into a native Python package
using large language models under human supervision, with correctness established by
numerical comparison against the original. It proceeds as an ordered sequence of phases,
each executed by orchestrating skills that dispatch specialized sub-agents with indepen-
dent model contexts: analyzing structure before translating anything, fixing the Python
rendering of every base-R construct in a written guide before any code is generated, con-
verting in dependency order, reusing the original compiled code, and validating against
the original both function by function and end to end.
We applied it to KernSmooth and rpart, chosen to differ in the one respect that gov-
erns the work: the first reaches its compiled core through R’s array-based .Fortran()
interface, the second through .Call(), which exchanges R’s own internal objects. A
seven-phase core carried both; rpart additionally required a five-phase prologue rebuild-
ing the portion of R’s C API it uses. The resulting packages reproduce their originals

                                             2
r2py: AI-Assisted Conversion of R Statistical Packages to Python


across 518 and 846 tests benchmarked against R, and are distributed on PyPI.


2     Results
2.1    The r2py framework
r2py organizes the conversion of an R package into seven phases (Fig. 1), each executed
by large language models under human supervision and each addressing a specific way in
which a translation can go wrong.
The order is not editorial: each phase depends on what the previous one established.
Structural analysis must come first, because the dependency graph it recovers (Fig. 2)
determines the order in which functions can be translated at all. Build infrastructure
precedes translation so that each converted function is executable when written. Cat-
aloging every base-R construct and fixing its Python rendering precedes generation, so
that a construct is rendered identically wherever it appears rather than decided afresh by
each independent invocation. Only then is the R layer converted, function by function
in dependency order, and assembled into modules. The three verification phases run last
and in sequence, because reading, executing and testing expose different classes of defect.
A design decision shapes the rest of the framework. Statistical R packages seldom perform
their numerical work in R, and reimplementing a compiled routine in interpreted Python
would forfeit the performance that motivated compiling it. r2py therefore retains the
original compiled source unmodified and translates only the R layer that calls it. This also
has a consequence the framework depends on: because the computational core executing
under Python is byte-identical to the one executing under R, any numerical divergence
must originate in the translated layer—small enough to audit exhaustively, whereas a
fault inside reimplemented compiled code would surface as a plausible wrong number.
What that decision costs differs between packages—not by size or complexity, but by the
interface through which R reaches its compiled code, and we encountered both cases.
KernSmooth delegates its computation to Fortran 77 reached through R’s .Fortran()
interface, which passes plain, C-compatible arrays by reference. Both languages agree
on the binary representation of such an array, so the retained Fortran compiles into the
Python package and is called with NumPy buffers directly (Methods). The compiled-code
decision costs nothing beyond the build configuration of phase 2, and KernSmooth passes
through the seven phases unchanged.
rpart reaches its C code through .Call(), and this changes the problem entirely. .Call()
does not pass arrays; it passes SEXP values, pointers to R’s own internal objects. C code
written against this interface allocates R objects, registers them with R’s collector, reads
them through R’s accessor macros and signals errors through R’s own mechanism—all
provided by libR.so at run time. Python cannot construct such objects, and shipping
an R installation with every Python wheel would reinstate exactly the dependency the
conversion exists to remove.

                                             3
r2py: AI-Assisted Conversion of R Statistical Packages to Python


This is not a peculiarity of rpart. R’s own extension documentation directs authors
toward .Call() wherever compiled code exchanges anything beyond plain numeric ar-
rays [25], and the obstacle extends well past the packages that call it directly: Rcpp [26],
on which more than a thousand CRAN packages are built, generates .Call() entry points
over the same SEXP representation, so its dependants inherit the same barrier. Any frame-
work intending to convert more than the easiest packages has to solve it.
We solve it by reconstructing, as standalone code, exactly the portion of R’s C API the
target package uses, so that its original C sources compile and run with no R present.
This adds a prologue of five phases ahead of the seven-phase core: analyzing the compiled
source’s dependencies, inventorying the R C API symbols it references, writing a blueprint
for each, generating the replacement headers, and producing entry-point wrappers callable
from Python. The core itself is unchanged: rpart then passes through the same seven
phases KernSmooth did. Section 2.4 describes the reconstruction.
Between them the two cases span what a further package is likely to present. Reached
through .Fortran() or .C(), its compiled code passes arrays and needs no prologue;
reached through .Call(), or through Rcpp over the same representation, it needs the
reconstruction—and which case it falls into is readable from its source beforehand.

2.2    How the framework is executed
Each phase except two—build infrastructure and the equivalence audit—is carried out by
a skill—an orchestrator that assembles the inputs a unit of work requires and dispatches
it—and by the sub-agents it invokes, each a separate language-model invocation with its
own context (Fig. 3). We instantiated the framework in Claude Code (Anthropic) [27],
but the decomposition does not depend on that choice and transfers to any environment
supporting multi-agent orchestration with file-system access.
The work is divided into units small enough to be carried out reliably—one source file, one
construct, one function, one failing test—and almost every artifact is model-generated:
the structural analysis, the construct catalog and its guides, the Python functions, and for
rpart the symbol inventory, the 51 replacement headers and the entry-point wrappers,
together with the test suites and the repairs applied in the bug-resolution loop. What the
framework contributes is not the generation but the decomposition: deciding what each
invocation should see, in what order they must occur, and what has to be settled before
any begins.
The decomposition rests on a principle: every cross-cutting translation decision is settled
once, in a machine-readable artifact, before any code is generated. R’s base library does
not map one-to-one onto Python, and the correct translation is often context-dependent—
as.integer is called at 33 sites in rpart across at least half a dozen structurally distinct
contexts, and a strategy correct in one is not automatically correct in another. Because
each agent runs as an independent, stochastic invocation with no memory of decisions
taken elsewhere, resolving such questions case by case offers no way of detecting incon-
sistency short of exhaustive pairwise comparison. The framework therefore records every

                                             4
r2py: AI-Assisted Conversion of R Statistical Packages to Python


call site of every construct—509 across 46 constructs in KernSmooth, 1,298 across 172 in
rpart—and generates one authoritative guide per construct. An implicit, per-invocation
judgment becomes an explicit artifact a reviewer can correct in one place before the error
propagates into many functions.
Human effort is not eliminated but redirected. It goes into specifying each phase, review-
ing its output before the next begins, and making the decisions that are not mechanical
(Methods). A manual cross-check of rpart’s 35 structural-analysis files caught three mis-
classified call sites that would otherwise have propagated into the conversion order. In
each case the model performed the work and a human decided whether it was right.

2.3    Validating the conversion
The conversion targets faithfulness in a strict sense: we do not reorganize the package,
redesign its public interface, or improve its algorithms, and the Python package defines
the same functions with the same arguments and returned structures. This is what makes
function-level comparison possible at all—each converted function has a counterpart in
R taking the same arguments, and can be checked against its original in isolation rather
than only through end-to-end output.
The correctness criterion is numerical equivalence to the original implementation. This is
a stronger and narrower requirement than the functional or structural equivalence used
in general-purpose code translation, where a translation succeeds if it computes the same
thing in some recognizable sense. Here a translation succeeds only if it returns the same
numbers, to a tolerance declared at the point of comparison and checked against R actually
running (Methods).
A suite only finds defects on paths it exercises. The generated tests are written with that
in mind, in three categories—positive, negative and boundary (Methods)—of which the
boundary cases matter most, since the edges of the input domain are where translation
defects concentrate. But no suite closes the gap by itself. Four verification methods
were applied in sequence—the two halves of the phase-5 audit, the package’s own tests in
phase 6, then the generated suite in phase 7—and their differential yield is itself a result.
A systematic static audit, in which agents compared each translated module against its
R source without executing either, found real defects across every subsystem. Running
the assembled package on realistic workflows then exposed roughly sixteen further issues
the static reading had been structurally unable to see—violations of runtime semantics
rather than of translated logic. Translating the package’s own historical regression tests
surfaced further defects in six of the fourteen scripts, none of which any earlier method
had found; the generated suite, run last, added more still. Each method ran against a
package already corrected by its predecessors, so the sequence measures what each reaches
beyond the last (Table 2).
The clearest instance is a defect that only the third method reached. A control-parameter
default was computed as 21 where R computes 20, so the implementations diverge only


                                             5
r2py: AI-Assisted Conversion of R Statistical Packages to Python


in trees deep enough to reach a node of exactly twenty observations; downstream, the
effect is a discrepancy in cross-validated error indistinguishable from floating-point noise.
Neither the static audit nor the workflow execution that preceded it exercised a tree that
deep (Methods).
What the defects in Table 2 have in common is that they do not announce themselves.
Most returned plausible numbers; one corrupted the heap several calls after the offending
assignment. None would have been caught by a suite checking only that the code runs,
and several would have survived any review that did not execute it. This is the concrete
form of the risk that motivates the framework.
Both conversions reproduce their R originals at every asserted tolerance (Table 1); the
median assertion bounds agreement at 10−6 in r2py_kernsmooth and 10−7 in r2py_rpart.
Two exceptions among rpart’s 846 tests record a divergence that cannot be closed rather
than one that has not been: R’s print and summary echo the call as the user typed it,
reconstructed from the unevaluated expression R captures at the call site, which a Python
object retaining only evaluated arguments cannot reproduce. A further 94 differences
were cataloged in which both languages reject the same input but describe the rejection
differently; these are recorded, not failed.
These results bound what has been established as well as what has been achieved: the
measured agreement is a lower bound on true correctness, holding at the tolerance asserted
and only along the paths the suites happen to exercise. The layered sequence provides
not a guarantee but a succession of independent opportunities for a defect to be caught.

2.4    Reconstructing R’s C API
Reconstructing R’s C API means supplying, in standalone code, the runtime services the
package’s C source expects: the object representation, the allocators, the accessors, and
the error and output routines. The work is bounded by what the package actually uses—
for rpart, 235 reference sites across 51 distinct identifiers, established by static analysis
before any of it was written (Methods).
The 51 items are not equally difficult, and the distribution is what makes the approach
viable (Fig. 4): forty-six have direct standalone equivalents. Of the five that are op-
erations on R’s interpreter, one is never linked—a compatibility macro expands it into
the two environment-lookup routines—and the other four are reached only on the user-
defined-split path, where Python registers callbacks for them as that path initializes. Only
expression evaluation truly requires an interpreter; the rest reduce to a pointer table, a
lookup in it, and an unreachable stub. This residue is the honest limit of the approach,
and its size is why the approach works at all: in rpart, the bridge is reachable only when
a user supplies a custom splitting rule, and all four built-in methods execute without
entering it.
R distinguishes transient allocations from persistent objects that outlive a call, and the
reconstruction preserves the distinction (Methods). A consequence is that PROTECT and


                                             6
r2py: AI-Assisted Conversion of R Statistical Packages to Python


UNPROTECT, the protocol that exists to shield objects from garbage collection, have nothing
to shield them from and reduce to no-ops.
The reconstruction is header-only, one self-contained header per API item, and is written
in C++ because the callback pointers and the sentinels standing in for R’s NULL must
resolve to a single instance across all 37 translation units (31 package sources, five entry-
point wrappers and one helper file). C++ inline variables deliver that from a header
alone; C would need a coordinating source file owning all of them—precisely the ordering-
sensitive shared artifact that generating one item at a time avoids.
Whether such a reconstruction is faithful is not settled by inspecting it. The first evidence
is how little of the original had to change: of the 35 files, 30 required no modification
whatsoever and 5 only a substitution of include directives. Beyond that a single anony-
mous struct declaration, legal in C but not in C++, needed a tag name; no referenced
symbol had to be stubbed out. The second is the numerical result, which the validation
of Section 2.3 settles.
The difficulties encountered were not statistical or algorithmic but properties of separate
compilation, and they indicate where the risk in such a reconstruction lies. An audit of
the generated headers found seven defects, most of them include-guard mismatches or
linkage conflicts (Methods). The most consequential was of a different kind: the four
function-pointer variables underlying the interpreter bridge had been declared static at
namespace scope, which in C++ gives each translation unit a private copy, so a callback
registered from Python would have updated one unit’s pointer and left every other holding
a null. The defect compiles cleanly, links cleanly, and fails only when the callback path is
first exercised—in rpart, only when a user supplies a custom splitting rule. The prologue
is bounded and enumerable before it is begun, but its risks are of this kind.


3    Discussion
The two conversions suggest that the barrier separating statistical software from the
Python ecosystem is more tractable than its reputation, and that what makes it tractable
is not the capability of the underlying model but the discipline imposed around it. Almost
every artifact was model-generated; almost every decision about what each invocation
should see, and in what order, was not.
It is worth stating plainly what this contribution is and is not. It is not the conversion
of two packages, important though those are to the people who use them; neither is it
a turnkey procedure that converts an arbitrary R package without intervention. Every
phase reported here was specified, reviewed and in places corrected by us, and both
target packages were chosen because they depend on nothing beyond base R. What we
offer is a decomposition—an ordered set of phases, each with a defined artifact and a
defined check—whose cost on a further package can be estimated before the work begins.
Packages carrying contributed dependencies, or exposing a wider compiled-code boundary,
will need components this framework does not yet supply. We report it as a demonstration


                                             7
r2py: AI-Assisted Conversion of R Statistical Packages to Python


that conversions of this kind can be carried out systematically rather than bespoke, and
as a structure for the ones that follow.
Faithfulness, as we have defined it, reaches further than preserving an interface: the
harder part concerns behavior the original gets wrong. During validation we identified a
genuine fault in rpart’s own C source (Methods). The file is byte-identical in the original
and in our port, so the defect is reproduced exactly, and we have deliberately not fixed it:
an analysis published using R’s rpart should reproduce under r2py_rpart, and a port
that silently improved on its original would produce discrepancies users would rationally
attribute to the port rather than the correction. The defensible position is to document
such defects explicitly rather than propagate them silently. A reimplementation may be
better than its source; a port must be the same. The same applies to credit: the results
a port produces are its original’s, and work relying on it should cite both.
Of the four verification methods reported above, the one we would most strongly recom-
mend is the one easiest to overlook: translating the regression suite the source package
already ships. Such suites reach states that neither a reviewer nor a generated suite has
reason to construct. The control-parameter defect was reachable only that way, having
survived both a systematic audit and execution on realistic multi-step workflows. We
expect this to hold for AI-assisted porting generally.
The framework’s artifacts are reusable across conversions, but only partly. The translation
guides document how base-R constructs render in Python, and such constructs recur
across R packages generally—but the two catalogs overlap without nesting, and each
conversion enlarged the catalog rather than drawing on it unchanged (Methods). Because
each guide enumerates the usage patterns observed in its source package, a construct
already cataloged may still need extending when a new package exercises it differently.
The reconstructed headers are reusable in the same qualified sense, making the prologue
closer to a one-time cost than a cost recurring with every package.
Three limitations bound what we have shown. A package carrying a tree of contributed
CRAN dependencies would require the framework to be applied recursively, or each de-
pendency mapped onto a Python equivalent, and we have not characterized what that
costs; much of the biostatistical software that motivates this work, including a large part
of Bioconductor, is of that kind. The compiled and interpreted layers could be developed
parallelly only because rpart reaches its C layer through five fixed-signature entry points;
the boundary still grew to fifteen functions once a user-defined split calls back into Python
(narrowness where R calls in does not imply narrowness where C calls back), though a
prospective conversion can at least measure its own before assuming it does. Some R-
specific behavior remains out of reach: the printed call echo behind our two expected
failures, one interactive routine, and formula support covering the common forms rather
than R’s full model-frame semantics.
A different kind of limit applies to the evidence itself. Both conversions were carried out
with the complete framework in place, so the marginal contribution of any individual
phase is not isolated here. This matters most for the phase producing no code at all—the


                                             8
r2py: AI-Assisted Conversion of R Statistical Packages to Python


language-dependency catalog—whose value we argue from the consistency requirement
rather than demonstrate by measurement.
The immediate extensions are to extract the reconstructed API headers as an independent
library and to attempt a package with genuine CRAN dependencies, which is where
the framework’s limits will next be found. We expect improving models to reduce the
human effort each phase requires rather than to remove the phases themselves, since the
decomposition follows from the structure of the problem rather than from any current
limitation of the models. The result we would emphasize is not that two packages were
converted but that the cost of converting a third is largely predictable in advance from a
static scan of its source.


4    Methods
Results report what the framework does and why; this section records how each phase was
carried out, in enough detail to reproduce it. It is organized by layer rather than by phase
number—the R layer first, then the compiled layer and the interface to it, then validation
and distribution—because the machinery within a layer is easier to follow together than
split across the order in which it ran. The skill and sub-agent specifications themselves
are Markdown documents with YAML front matter declaring a name and description,
followed by a structured natural-language body giving execution steps and an output
schema. They reside in .claude/commands/ and .claude/agents/ in the project tree and
are reproduced in full in the Supplementary Information. The conversions themselves are
recorded in two Supplementary Notes—Note 1 for KernSmooth, Note 2 for rpart—written
contemporaneously with the work rather than composed afterwards. Each documents
every phase as it was carried out, including the diagnostic paths taken through defects
that were subsequently fixed, so that the process reported here can be audited rather than
taken on trust.

Target packages
KernSmooth [5] implements the kernel smoothing methods of Wand and Jones: binned
kernel density estimation in one and two dimensions, kernel functional estimation, lo-
cal polynomial regression, and—most distinctively—plug-in bandwidth selection [28, 29],
computed over binned data for speed [30]. It was written by M. P. Wand, with the R
port maintained by Brian Ripley. Here too the gap is specific rather than total: Python
has kernel density estimators, but the direct plug-in bandwidth selectors that make Wand
and Jones’s methods the reference for bandwidth choice, and local polynomial regression
with binning, are absent or only partially available.
KernSmooth version 2.23-26 (license: Unlimited) defines 16 functions in a single R source
file, 7 of which are exported. Its computational work is delegated to 11 fixed-form
Fortran 77 files exposing 8 subroutines, registered through useDynLib(KernSmooth,
.registration = TRUE, .fixes = "F_"). Three LINPACK routines are included for


                                             9
r2py: AI-Assisted Conversion of R Statistical Packages to Python


LU decomposition. Two further LINPACK routines providing QR decomposition (dqrdc,
dqrsl) are called by the package but satisfied under R from R’s own internal LINPACK
copy; because OpenBLAS does not supply them, they were obtained from Netlib and
added to the Python package’s sources, bringing its compiled sources to 13 files.
rpart [2] implements the CART methodology of Breiman, Friedman, Olshen and
Stone [3]: recursive partitioning for continuous, categorical, count, and censored
responses, with surrogate splits for missing predictors, cost-complexity pruning, and
cross-validated selection of tree size. It was written by Terry Therneau and Beth Atkin-
son, with the original R port by Brian Ripley, and it is the canonical implementation
against which other decision-tree software is compared. Python has decision trees,
but not these: scikit-learn’s implementations provide neither surrogate splits, nor
the cross-validated complexity table, nor trees for censored or count responses, nor
user-supplied splitting rules. A Python user who needs any of those has no native option.
The difference in categorical handling is one of model class rather than convenience.
rpart may split a factor on an arbitrary subset of its levels, recording each level’s
assignment in a csplit matrix; the package’s own vignette enumerates all 25 = 32
combinations of a six-level predictor in a worked example. scikit-learn describes its
trees as an optimized version of the CART algorithm but states that its decision-tree
implementation “does not support categorical variables for now”, so factors must be
encoded numerically before fitting—and an encoding recovers the same partition only
indirectly: a chain of indicator splits can isolate a subset but spends one level of depth
per level of the factor and is found, if at all, by a greedy search that evaluates the
indicators one at a time, while ordering the levels by mean response—the shortcut rpart
itself uses for two-class, anova and Poisson outcomes—recovers the optimal subset split
only for those outcomes, not for the multi-class case where the exhaustive search is
required.
rpart version 4.1.27 (GPL-2 | GPL-3) defines 47 functions across 36 R source files, with
35 C source and header files. Its C layer is organized around a dispatch table map-
ping a method integer to four function-pointer slots—node initialization, split selection,
evaluation, and error computation—which keeps the recursive partitioning logic method-
agnostic; method integer 4 denotes a user-supplied splitting rule implemented as a callback
into the R interpreter. The R layer reaches the C layer through five .Call() entry points:
rpart, pred_rpart, xpred, rpartexp2, and init_rpcallback.

Structural analysis and conversion ordering
One sub-agent was dispatched per R source file. Each enumerated every function defini-
tion, including nested closures, and classified every call within each function body into
exactly one of three categories: language dependencies (base R and its standard library),
internal dependencies (functions defined elsewhere in the same package), and external de-
pendencies (.Fortran(), .C(), .Call(), or .External() crossings into compiled code).
Output was one JSON object per file, keyed by function name, with the three dependency
lists as values.

                                             10
r2py: AI-Assisted Conversion of R Statistical Packages to Python


Internal dependencies were assembled into a directed acyclic graph and each function as-
signed a level by longest path from any root; the resulting table records, for each function,
its level, immediate callers, and immediate callees. KernSmooth resolved into three levels,
with the one-dimensional linear binning routine called by seven distinct callers. rpart
resolved into six levels, 28 of its 47 functions making no internal calls at all. Conversion or-
der was read from this table, deepest level first. For rpart the analysis was cross-checked
by hand, which corrected three misclassified call sites before they could propagate into
the conversion order.

Language-dependency catalog and translation guides
A second per-file pass recorded every individual call site of every language dependency
identified in the structural JSON, capturing the dependency name, enclosing function, line
number, and complete call expression including multi-line calls. Per-file CSVs were merged
and sorted by dependency name so that all sites for a given construct are contiguous.
One CSV field required correction: R string literals embedded in call expressions had
been written with bare rather than doubled double-quote characters, breaking RFC 4180
parsing; the file was rewritten using a conforming CSV writer.
The catalog held 46 distinct constructs over 509 call sites for KernSmooth and 172 over
1,298 for rpart; the two sets overlap without nesting, 34 constructs being common to
both, 12 peculiar to KernSmooth and 138 to rpart. One sub-agent was then dispatched
per unique construct, in parallel, each receiving only the CSV rows for its assigned con-
struct. Agents read the corresponding source lines for context and consulted R and
Python documentation where behavior was non-obvious. Each produced a Markdown
guide with four parts: an overview of the construct and its translation hazards; a con-
textual usage analysis enumerating every call site grouped by usage pattern; a general
conversion strategy; and step-by-step examples pairing R code with its Python translation
for each distinct pattern. Construct names containing characters not permitted in file-
names were encoded; two guides are dot-prefixed and therefore invisible to shell globbing,
which required directory listing rather than globbing to verify the expected count.

Function conversion and package assembly
Conversion was performed one function per sub-agent invocation, sequentially in the topo-
logical order established above. Each agent received the R source for its function, the func-
tion’s structural JSON entry, the folder of translation guides, and the dependency-level
table. Output was a JSON artifact with three fields: the import statements required, the
complete Python signature with type annotations, and the function body as a list of lines.
This encoding, rather than direct emission of Python source, allows an agent converting
a caller to read its callees’ signatures and return types mechanically.
R constructs without direct Python equivalents were handled uniformly: named lists
became dictionaries; missing() became a module-level sentinel object tested by identity;
S3 class assignment became a reserved dictionary key; environments became dictionaries;

                                              11
r2py: AI-Assisted Conversion of R Statistical Packages to Python


1-based indices were converted at every crossing; and matrices passed to compiled code
were laid out in column-major order.
A separate skill assembled the artifacts into modules. Assembly corrected three classes of
systematic defect: absolute import paths were rewritten as relative imports; redundant
cross-imports between functions sharing a module were removed; and duplicate third-
party imports were merged, with the final import block ordered standard library, third
party, local. For rpart, 26 of 36 output filenames contained dots inherited from R naming
conventions and were renamed with underscores to be importable. Syntax was confirmed
by parsing each assembled module. Because meson-python does not auto-discover Python
sources, every module must be enumerated explicitly in the build definition; this is a
standing maintenance requirement whenever modules are added.

Equivalence audit and test porting
The assembled package was audited in two passes. In the first, one sub-agent per module
compared the translated Python against its R source without executing either, checking
that control flow, error conditions and returned structures corresponded, and reporting
discrepancies for review; findings were approved before any source file was changed, under
a standing constraint that the retained compiled sources were never to be altered. In
the second, the package was executed on realistic multi-step workflows, which exposes
violations of runtime semantics that static reading cannot reach.
Where the source package ships a regression suite, each script was translated by one
sub-agent and run against the Python package. rpart ships fourteen such scripts and
KernSmooth two. Because these suites depend on datasets and on printed output, refer-
ence values and datasets were captured once from a live R session into checked-in files
rather than obtained through rpy2 at test time.

Reconstruction of R’s C API
The inventory, the category breakdown, and the defects found in the generated headers
are reported in Results; this section records the representations and mechanisms those
results depend on.
SEXP is a pointer to a structure carrying a type tag, a length, row and column counts,
and a data pointer. Implementation blueprints were written for the 51 items sequen-
tially rather than in parallel, because foundational definitions—the structure layout, the
type constants, the allocator—must be fixed before dependent items can reference them;
headers were then generated in the same order and assembled behind a single master
include.
The arena serving transient allocations is thread-local. Each entry-point wrapper declares
an arena frame as its first local variable, so that the frame’s destructor releases every block
allocated during the call on all exit paths, including exceptional ones. Persistent objects—
SEXP nodes and their data buffers—are allocated on the heap and freed explicitly by the

                                              12
r2py: AI-Assisted Conversion of R Statistical Packages to Python


caller after the boundary returns.
Two choices could not be derived mechanically from the item inventory. The faked R
version constant had to satisfy two opposed preprocessor guards simultaneously—one
requiring at least 2.16.0, another requiring less than 4.5.0—and was set to a value in
that window. Of the five interpreter operations, one variable-lookup entry point resolves
to a compatibility macro expanding to two other items in the same category; the other
four—expression evaluation, symbol interning and the two environment-lookup routines—
are resolved through function pointers, which Python registers when the callback path
is initialized rather than at import, so a fit that never supplies a custom splitting rule
never registers them. Only expression evaluation requires an interpreter; the interning
callback merely returns a stable handle for each name, for which the headers also retain
a self-contained implementation, and the two lookups reduce to a table indexed by those
handles, one of which rpart never reaches.
Five entry-point wrappers, compiled as C++ but exposing C linkage, translate between
the SEXP-based internal interface and a plain-array interface. Each includes the master
header outside its extern "C" block, declares an arena frame first, and implements an
exception boundary catching the package’s own error type, allocation failure, standard
exceptions, and any remaining exception, writing a null-terminated message to a caller-
supplied buffer. Environments and expressions, which have no plain-array representation,
are passed as opaque handles; these are cast directly rather than re-wrapped, since the
identity of the pointer is what the Python side uses as a registry key. A further helper
file exports routines for constructing and releasing SEXP nodes that wrap NumPy buffers
without copying.
Local wrapper macros defined in the package’s own header were excluded from the symbol
inventory even where they wrap R API calls, since those travel with the source. The sen-
tinel objects standing in for R’s NULL and its symbol table use a construction structurally
similar to the function-pointer variables—file-local pointers initialized by inline factory
functions containing function-local statics—which was examined and found safe, since
every translation unit ultimately references one shared instance and pointer comparison
remains valid.
Migration of the original sources to the reconstructed headers was dispatched in parallel
across all 35 files, since the edits are independent.

Foreign-function interface semantics
An f2py [31]-wrapped Fortran subroutine returns None unconditionally; output arrays
are modified in place through the pointer passed in, and the caller reads results from the
pre-allocated arrays rather than from a return value. Scalar outputs require particular
care, since a Python float is immutable and cannot be written back: either a length-1
array is passed, or the subroutine is given an explicit output intent. For the three scalar
outputs of the block-estimation routine, f2py had inferred pass-by-value from the Fortran
declaration, so the computed values never propagated; this was corrected by generating

                                             13
r2py: AI-Assisted Conversion of R Statistical Packages to Python


an explicit signature file with output intent declared and building from that file rather
than from the bare sources.
Two further behaviors of NumPy 2.4.3 affected the wrappers. Dimension scalars declared
in a Fortran signature are absorbed out of the required positional arguments and inferred
from the shapes of the arrays passed, so wrappers retaining them at their original positions
misalign every subsequent argument; removing them reduced the local-polynomial call
from 19 to 16 positional arguments, with corresponding reductions elsewhere. Separately,
parameters declared two-dimensional in Fortran are shape-checked strictly, so arrays must
be allocated in Fortran order rather than flattened before the call.
For rpart, the compiled code is loaded as a shared library through cffi [32] in application-
binary-interface (ABI) mode rather than built as a Python extension module. NumPy
buffers are passed by taking a buffer view; callbacks are registered as cffi callback objects;
and both the buffer objects and the views derived from them are retained in a keep-alive
list for the duration of a call, since neither is owned by the C side.

Build system and distribution
Both packages use meson-python as the Python Enhancement Proposal (PEP) 517 build
backend. r2py_kernsmooth builds a Python extension module from an f2py custom
target, with NumPy’s C and f2py include directories resolved at configure time. BLAS
is located through a five-stage chain: pkg-config, then library searches for openblaso,
openblas, and blas, then a guarded absolute path for a development cluster whose dis-
tribution omits the unversioned symbolic link; if none succeeds the build fails at configure
time with an actionable message rather than at link time. r2py_rpart builds a shared li-
brary loaded at import, requires no external numerical library, and is compiled as C++14
rather than C++17, because in C++17 mode the standard math header on the build
system declares overloads referencing compiler built-ins that its C library does not pro-
vide; the inline-variable declarations in the reconstructed headers compile in C++14 as an
accepted extension. Platform-conditional linking selects the appropriate C++ standard
library on macOS.
Binary wheels are built in CI with cibuildwheel across five runners covering Linux
x86_64 and aarch64 (both glibc and musl variants), macOS x86_64 and arm64, and
Windows x86_64, for CPython 3.10 through 3.14, and published on release through OIDC
trusted publishing. Windows builds obtain their toolchain from MSYS2, and dependent
libraries are vendored into the wheel.

Test generation and reference comparison
Public interfaces were identified from the package documentation; for rpart, cross-
referencing the manual pages against the file marking internal entry points yielded 23
public functions. One sub-agent was dispatched per public function, sequentially, each
reading the function’s signature and the package’s reference manual and emitting three


                                             14
r2py: AI-Assisted Conversion of R Statistical Packages to Python


categories of test. Positive tests exercise the documented combinations of parameters
and check the returned values against R. Negative tests exercise every explicit error
condition in the R source and check that the Python function refuses the same inputs.
Boundary tests exercise the edges of the input domain—empty and single-element inputs,
non-finite values, degenerate ranges, and the parameter values at which the algorithm
changes behavior.
Reference values were obtained from the original R packages through rpy2 [12]. R pack-
ages are attached once at module level; inputs are passed as R vectors; results are extracted
by name and converted to NumPy arrays; and agreement is asserted elementwise. Relative
tolerances for assertions that compare output against R, each written at the assertion or
inherited from its comparison routine, range from 10−10 to 10−3 in r2py_kernsmooth and
from 10−12 to 10−4 in r2py_rpart (Table 1); the median assertion is 10−6 in the former and
10−7 in the latter. An absolute floor is added where references can be zero. In r2py_rpart
the tightest bounds apply to quantities read directly from the fitted tree—every assertion
at 10−12 is in the meanvar suite—and the loosest to cross-validated quantities: all four
assertions at 10−4 are in the xpred.rpart suite. Fold membership is supplied identically
to both implementations, so these bounds absorb error accumulated in refitting and com-
bining across folds, not a differing partition. In r2py_kernsmooth the tightest bounds
apply to grid coordinates, at 10−10 , and the two loosest agreement bounds, 10−3 and 10−4 ,
are both two-dimensional density estimates at extreme scales or asymmetric bandwidths.
Where exact row correspondence with an R dataset was required, the data were read
from the R session rather than from a file. Where a suite is required to run without an R
installation, reference values and datasets were captured once from a live R session into
checked-in files; this was done for rpart’s translated historical suite.
Failures were resolved by an iterative loop: the suite is re-run, the first remaining failure is
passed to a repair agent together with its traceback and the relevant source, the package
is rebuilt if library code changed, and the cycle repeats until the suite passes.

Example-workflow translation
For rpart, two complete example workflows—a regression tree and a classification
tree, each comprising data loading, formula-based fitting, cross-validated pruning, and
plotting—were translated from R to Python and executed in both languages, with
console output and rendered figures captured for comparison. Visual comparison of the
resulting figures exposed four rendering divergences that no numerical assertion tested:
overlapping axis tick labels where R’s graphics engine suppresses them, filled rather than
hollow plot markers, split labels positioned beside rather than above their branch points,
and a title overlapping the tree. Each was corrected in the plotting layer. This step is
required for packages with a substantial presentation surface; KernSmooth, whose output
is numeric throughout, did not require it.




                                              15
r2py: AI-Assisted Conversion of R Statistical Packages to Python


Root-cause analysis of the cross-validation discrepancy
Cross-validated error estimates for deeply grown rpart trees differed from R in trailing
rows while shallower fits matched exactly. Four candidate explanations were eliminated
with direct evidence before any code was changed. Loss of precision in the checked-in data
fixture was excluded by comparing the fixture byte-for-byte against the live R dataset.
Divergence between the two packages’ C sources was excluded by direct file comparison.
Contraction of multiply-add sequences under differing compiler flags was excluded by
disassembling a minimal reproduction under all four flag combinations and observing
that no fused instruction was emitted in any of them, the toolchain’s baseline instruction
set predating the relevant extension. Optimization level and target architecture more
generally were excluded by rebuilding the extension with the original package’s exact
compiler flags and observing no change.
Identical instrumentation was then added to both implementations, first reporting per-fold
prediction errors, then candidate split values in exact hexadecimal floating-point form,
and finally the inputs to and outcome of the per-node stopping test. Every logged field
matched bit for bit except one: the minimum-split threshold read 20 under R and 21 in the
port, constant across nodes and folds. The cause was in the control-parameter defaults,
where a three-branch computation reassigned one parameter before a later branch tested
whether that parameter had originally been supplied; the test therefore always saw an
assigned value and executed a back-derivation intended only for the unsupplied case.
Capturing the original absence in a separate flag before reassignment resolved it, and was
verified against R across all four combinations of supplied and omitted arguments.
The investigation also surfaced a genuine defect in rpart’s own C source, initially cred-
ited with the discrepancy and later ruled out as its cause. The oops: fallback branch
of rundown.c, reached when a held-out observation cannot be routed past a split—its
split variable and every surrogate missing—and the majority-direction fallback is not in
force, back-fills one output array correctly but leaves the corresponding entries of a second
holding stale values from an earlier observation, and then writes a single element one posi-
tion past that second array’s range. The three arrays share one allocation, in consecutive
slices, so that stray write lands on the first entry of the prediction array itself. The defect
is real and present identically in both packages, but once tree shapes agreed it produces
identical residue in both and therefore no observable difference; the full cross-validation
table matched R after the control-parameter fix alone, with no change to rundown.c.


Declarations
Data and code availability
The converted Python packages are distributed on the Python Package Index (PyPI)
as r2py_kernsmooth and r2py_rpart. Their sources, together with all intermediate ar-
tifacts of the conversion—structural-analysis JSON, language-dependency catalogs and
translation guides, the reconstructed C API headers, and the complete test suites—

                                              16
r2py: AI-Assisted Conversion of R Statistical Packages to Python


are available at https://github.com/r2py-project/python-KernSmooth and https:
//github.com/r2py-project/python-rpart, with the packages additionally mirrored as
standalone repositories at https://github.com/r2py-project/r2py_kernsmooth and
https://github.com/r2py-project/r2py_rpart. The archived snapshots correspond-
ing to this manuscript are deposited at Zenodo under DOIs 10.5281/zenodo.21970781
(KernSmooth) and 10.5281/zenodo.21970837 (rpart). The skill and sub-agent specifi-
cations that drive every phase are included in those repositories and reproduced in the
Supplementary Information. The original R packages, KernSmooth 2.23-26 (Unlimited
license) and rpart 4.1.27 (GPL-2 | GPL-3), are available from CRAN. The converted
packages follow the terms of their originals: r2py_kernsmooth is distributed under the
Unlimited license, and r2py_rpart under GPL-2, since it reuses the original GPL-licensed
C source. We ask that published work using the converted packages cite the original R
package as well as this one.

Author contributions
J.L. conceived and supervised the study and selected the case-study packages. Y.C.
and J.L. developed the methodology. Y.C. implemented the framework, developed the
software, and performed the validation experiments. Y.C. and J.L. wrote and revised the
manuscript. Both authors approved the final version.

Competing interests
The authors declare no competing interests.

Acknowledgments
This research was supported in part by the University of Notre Dame’s Center for Research
Computing through the use of CRC computational resources.


References
 [1] R Core Team. R: A Language and Environment for Statistical Computing. R
     Foundation for Statistical Computing, Vienna, Austria, 2026. URL https://www.
     R-project.org/.

 [2] Terry Therneau and Beth Atkinson. rpart: Recursive Partitioning and Regression
     Trees, 2026. URL https://CRAN.R-project.org/package=rpart. R package ver-
     sion 4.1.27.

 [3] Leo Breiman, Jerome H. Friedman, Richard A. Olshen, and Charles J. Stone. Clas-
     sification and Regression Trees. Wadsworth & Brooks/Cole, Monterey, CA, 1984.




                                             17
r2py: AI-Assisted Conversion of R Statistical Packages to Python


 [4] Matt Wand. KernSmooth: Functions for Kernel Smoothing Supporting Wand &
     Jones (1995), 2025. URL https://CRAN.R-project.org/package=KernSmooth. R
     package version 2.23-26.

 [5] M. P. Wand and M. C. Jones. Kernel Smoothing. Chapman & Hall, London, 1995.
     ISBN 9780412552700.

 [6] R Core Team. The comprehensive R archive network. https://cran.r-project.
     org, 2026. Accessed 11 August 2026.

 [7] Robert C. Gentleman, Vincent J. Carey, Douglas M. Bates, Ben Bolstad, Marcel
     Dettling, Sandrine Dudoit, Byron Ellis, Laurent Gautier, Yongchao Ge, Jeff Gen-
     try, Kurt Hornik, Torsten Hothorn, Wolfgang Huber, Stefano Iacus, Rafael Irizarry,
     Friedrich Leisch, Cheng Li, Martin Maechler, Anthony J. Rossini, Gunther Sawitzki,
     Colin Smith, Gordon Smyth, Luke Tierney, Jean Y. H. Yang, and Jianhua Zhang.
     Bioconductor: open software development for computational biology and bioinfor-
     matics. Genome Biology, 5(10):R80, 2004. doi: 10.1186/gb-2004-5-10-r80.

 [8] Travis E. Oliphant. Python for scientific computing. Computing in Science & Engi-
     neering, 9(3):10–20, 2007. doi: 10.1109/MCSE.2007.58.

 [9] Charles R. Harris, K. Jarrod Millman, Stéfan J. van der Walt, Ralf Gommers,
     Pauli Virtanen, David Cournapeau, Eric Wieser, Julian Taylor, Sebastian Berg,
     Nathaniel J. Smith, et al. Array programming with NumPy. Nature, 585:357–362,
     2020. doi: 10.1038/s41586-020-2649-2.

[10] Pauli Virtanen, Ralf Gommers, Travis E. Oliphant, Matt Haberland, Tyler Reddy,
     David Cournapeau, Evgeni Burovski, Pearu Peterson, Warren Weckesser, Jonathan
     Bright, et al. SciPy 1.0: fundamental algorithms for scientific computing in Python.
     Nature Methods, 17:261–272, 2020. doi: 10.1038/s41592-019-0686-2.

[11] Fabian Pedregosa, Gaël Varoquaux, Alexandre Gramfort, Vincent Michel, Bertrand
     Thirion, Olivier Grisel, Mathieu Blondel, Peter Prettenhofer, Ron Weiss, Vincent
     Dubourg, Jake Vanderplas, Alexandre Passos, David Cournapeau, Matthieu Brucher,
     Matthieu Perrot, and Édouard Duchesnay. Scikit-learn: Machine learning in Python.
     Journal of Machine Learning Research, 12:2825–2830, 2011.

[12] Laurent Gautier. rpy2: R in Python. https://rpy2.github.io, 2024. Python
     package, version 3.5.

[13] Kevin Ushey, J. J. Allaire, and Yuan Tang. reticulate: R interface to Python. https:
     //CRAN.R-project.org/package=reticulate, 2023. R package, version 1.34.0.

[14] Boris Muzellec, Maria Teleńczuk, Vincent Cabeli, and Mathieu Andreux. Pydeseq2:
     a python package for bulk rna-seq differential expression analysis. Bioinformatics,
     39(9):btad547, 2023.


                                             18
r2py: AI-Assisted Conversion of R Statistical Packages to Python


[15] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira
     Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brock-
     man, et al. Evaluating large language models trained on code. arXiv preprint
     arXiv:2107.03374, 2021.

[16] Baptiste Rozière, Marie-Anne Lachaux, Loïc Chanussot, and Guillaume Lample. Un-
     supervised translation of programming languages. In Advances in Neural Information
     Processing Systems, volume 33, pages 20601–20611, 2020.

[17] Yue Wang, Weishi Wang, Shafiq Joty, and Steven C. H. Hoi. CodeT5: Identifier-
     aware unified pre-trained encoder-decoder models for code understanding and gener-
     ation. In Proceedings of the 2021 Conference on Empirical Methods in Natural Lan-
     guage Processing, pages 8696–8708, 2021. doi: 10.18653/v1/2021.emnlp-main.685.

[18] Junjie Zhang, Guilin Zheng, Yiming Lu, and Tao Yue. A survey on large language
     models for code generation. arXiv preprint arXiv:2406.00515, 2024.

[19] Sirui Hong, Xiawu Zheng, Jonathan Chen, Yuheng Cheng, Jinlin Wang, Ceyao
     Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, et al. MetaGPT:
     Meta programming for a multi-agent collaborative framework. arXiv preprint
     arXiv:2308.00352, 2023.

[20] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu,
     Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, et al. AutoGen: Enabling
     next-generation LLM applications via multi-agent conversation. arXiv preprint
     arXiv:2308.08155, 2023.

[21] Hanliang Zhang, Cristina David, Meng Wang, Brandon Paulsen, and Daniel Kroen-
     ing. Scalable, validated code translation of entire projects using large language mod-
     els. arXiv preprint arXiv:2412.08035, 2024.

[22] Ali Reza Ibrahimzada, Kaiyao Ke, Mrigank Pawagi, Muhammad Salman Abid,
     Rangeet Pan, Saurabh Sinha, and Reyhaneh Jabbarvand. Alphatrans: A neuro-
     symbolic compositional approach for repository-level code translation and validation.
     Proceedings of the ACM on Software Engineering, 2(FSE):2454–2476, 2025.

[23] Sahil Bhatia, Jie Qiu, Niranjan Hasabnis, Sanjit A. Seshia, and Alvin Cheung. Ver-
     ified code transpilation with LLMs. In Advances in Neural Information Processing
     Systems, volume 37, 2024. arXiv:2406.03003.

[24] Weixiang Yan, Yuchen Tian, Yunzhe Li, Qian Chen, and Wen Wang. Code-
     transocean: A comprehensive multilingual benchmark for code translation. In Find-
     ings of the Association for Computational Linguistics: EMNLP 2023, pages 5067–
     5089, 2023.

[25] R Core Team. Writing R Extensions. R Foundation for Statistical Computing, 2025.
     URL https://cran.r-project.org/doc/manuals/r-exts.html.

                                             19
r2py: AI-Assisted Conversion of R Statistical Packages to Python


[26] Dirk Eddelbuettel and Romain François. Rcpp: Seamless R and C++ integration.
     Journal of Statistical Software, 40(8):1–18, 2011. doi: 10.18637/jss.v040.i08.

[27] Anthropic. Claude code. https://www.anthropic.com/claude-code, 2025. Agentic
     coding environment.

[28] S. J. Sheather and M. C. Jones. A reliable data-based bandwidth selection method
     for kernel density estimation. Journal of the Royal Statistical Society: Series B, 53
     (3):683–690, 1991. doi: 10.1111/j.2517-6161.1991.tb01857.x.

[29] D. Ruppert, S. J. Sheather, and M. P. Wand. An effective bandwidth selector for
     local least squares regression. Journal of the American Statistical Association, 90
     (432):1257–1270, 1995. doi: 10.1080/01621459.1995.10476630.

[30] M. P. Wand. Fast computation of multivariate kernel estimators. Journal of Com-
     putational and Graphical Statistics, 3(4):433–445, 1994. doi: 10.1080/10618600.1994.
     10474652.

[31] Pearu Peterson. F2PY: A tool for connecting Fortran and Python programs. In-
     ternational Journal of Computational Science and Engineering, 4(4):296–305, 2009.
     doi: 10.1504/IJCSE.2009.029165.

[32] Armin Rigo and Maciej Fijalkowski. CFFI: C foreign function interface for Python.
     https://cffi.readthedocs.io, 2025. Python package, version 1.17.




                                             20
r2py: AI-Assisted Conversion of R Statistical Packages to Python


Tables
                                    KernSmooth → r2py_kernsmooth     rpart → r2py_rpart
 R source                           16 functions, 1 file             47 functions, 36 files
 Compiled core (as shipped by R)    Fortran 77, 11 files             C, 35 files
 Foreign interface                  .Fortran()                       .Call() (SEXP)
 Prologue phases                    0                                5
 C API symbols                      0                                51
 Base-R constructs                  46                               172
 Public functions tested            7                                23
 Tests                              518                              846
 Outcome                            518 pass                         844 pass, 2 xfail
 Relative tolerance vs R (median)   10−10 –10−3 (10−6 )              10−12 –10−4 (10−7 )

Table 1: Two conversions spanning the foreign-function-interface axis. Both
target packages are recommended R packages with no dependencies on contributed CRAN
packages. They differ in compiled language, in the interface through which R reaches
that compiled code, and in scale. Numerical agreement is asserted elementwise at a
relative tolerance written at each assertion or inherited from its routine; the range spans
every assertion compared against R, median in parentheses. Eight further assertions in
r2py_kernsmooth bound properties of the plug-in bandwidth selectors—convergence in
grid size, scale invariance, monotonicity in level, agreement between scale estimators—
rather than agreement with R, carry the loosest bounds and are excluded. The two xfail
results record a single structural divergence described in the text.




                                              21
r2py: AI-Assisted Conversion of R Statistical Packages to Python


 Defect                          Observable effect                   Detected by
 Marshaling layer coerced        Every multi-row, multi-column       Static audit
 Fortran-ordered     matrices    input silently transposed on en-
 back to C order on the way      try; affects all matrix argu-
 into the compiled core          ments of the fit routine
 f2py absorbs Fortran dimen-     Every later argument shifted        Dynamic execution
 sion arguments; wrapper still   by one position; one routine
 supplies them                   crashed, four returned wrong
                                 values silently
 Pruning mutated its argu-       Cached arrays inconsistent with     Dynamic execution
 ment in place, violating R’s    the pruned tree; heap corrup-
 copy-on-modify semantics        tion on a later cross-validation
                                 call
 Response matrix flattened       Multi-column responses silently     Package’s own historical
 in row-major rather than        mispaired; invisible to any         tests
 column-major order              single-column test
 Non-symmetric loss matrix       Loss matrix silently transposed;    Package’s own historical
 flattened in the wrong order    wrong predicted class at the        tests
                                 root node
 Sentinel overwritten before     Divergent tree shape at nodes of    Package’s own historical
 it was tested, changing a       exactly 20 observations; down-      tests
 control-parameter   default     stream cross-validation error re-
 from 20 to 21                   sembling floating-point noise
 Fortran    scalar  outputs      Three estimates always re-          Generated test suite
 bound by value rather than      turned zero, producing a divi-
 by reference                    sion by zero and a NaN band-
                                 width downstream
 R’s lazy default argument       Bandwidth computed from the         Generated test suite
 evaluated before, rather than   untrimmed range; plausible but
 after, the input is trimmed     incorrect values

Table 2: Representative defects and the method that found them. Each entry
produced numerically wrong output, or memory corruption, without raising an error at
the point of the fault. Rows are grouped by the verification method that first exposed the
defect, in the order the four methods were applied: static audit, dynamic execution, the
package’s own historical tests, then the generated suite. No method found all of them,
and each found defects its predecessors had missed.




                                               22
r2py: AI-Assisted Conversion of R Statistical Packages to Python


Figures

                  rpart enters here                                    KernSmooth enters here
                    Phase P1 - P5                                             Phase 1 - 7
         Prologue for the .Call / SEXP interface                Core - invariant across target packages

                       Phase P1                                                 Phase 1
              C-Source Dependency Analysis                                 Structural Analysis
      skill: /analyze-c-folder-dependencies                   skill: /analyze-r-folder-dependencies
      sub-agent: (sequential)                                 sub-agent: (sequential)
             @analyze-c-file-dependencies                            @analyze-r-file-dependencies

           Reference sites                                                           Structural analysis JSON &
                                                                                       Dependency-level CSV
                       Phase P2
                R-External-Item Extraction
     skill: /extract-c-folder-r-extern-items                                   Phase 2
                                                                          Build Infrastructure
     sub-agent: (sequential)
            @extract-c-file-r-extern-items

       Symbols & Headers
                                                                                 Phase 3
                                                                      Language-Dependency Cataloging
                        Phase P3                    a. skill: /extract-r-folder-language-dependencies
            Fake-Header Implementation Guides
                                                       sub-agent: (sequential)
      skill: /generate-r-extern-fake-guides
                                                              @extract-r-file-language-dependencies
      sub-agent: (sequential)
                                                    b. skill: /generate-language-dependency-conversion-guides
             @generate-r-extern-fake-guide
                                                       sub-agent: (parallel)
                                                              @generate-language-dependency-conversion-guide
     Implementation guides

                        Phase P4                                                     Markdown conversion guides
               Fake-Header Generation & Audit
      skill: /generate-r-extern-fake-headers                                   Phase 4
      sub-agent: (sequential)                                  Function Conversion & Package Assembly
             @generate-r-extern-fake-header                   skill: /convert-r-file-to-python
                                                              sub-agent: (sequential)
     Compiled fake headers                                           @convert-r-function-to-python


                           Phase P5                                                  Converted Python module
               Entry-Point Generation & Migration
   a. skill: /generate-r-extern-raw-entry-points
                                                                              Phase 5
      sub-agent: (sequential)                                             Equivalence Audit
             @generate-r-extern-raw-entry-point
   b. skill: /modify-c-folder-with-fake-headers
      sub-agent: (parallel)
             @modify-c-file-with-fake-headers                                      Phase 6
                                                                      Historical Test-Suite Conversion
                                                                skill: /convert-r-tests-to-python
                                                                sub-agent: (sequential)
                                                                       @convert-r-test-to-python
                               Fake headers &
                             Entry-point wrappers
                                                                                    Test files

                  Coda ( plot / print )                                            Phase 7
                                                                      Test Generation & Bug Resolution
                     Phase Coda                             a. skill: /generate-python-file-tests
            Example-Workflow Translation &                     sub-agent: (sequential)
                Rendering-Parity Fixes                                @generate-python-function-tests
         (packages with a presentation surface)             b. skill: /fix-bugs-found-in-tests
                                                               sub-agent: (iterative)
                                                                      @fix-bug-found-in-test
                   rpart ends here                                     KernSmooth ends here




                                                      23
r2py: AI-Assisted Conversion of R Statistical Packages to Python




Figure 1: The r2py framework. The core (right) carries a package from its R source to
a validated Python library in seven phases: (1) structural analysis, recovering the depen-
dency graph over the package’s own functions; (2) build infrastructure, so that converted
code is executable as soon as it is written; (3) language-dependency cataloging, fixing the
Python rendering of every base-R construct the package uses before any code is gener-
ated; (4) function conversion and package assembly in dependency order; (5) equivalence
audit, by reading and by execution; (6) conversion of the package’s own historical test
suite; and (7) systematic test generation with iterative bug resolution. Packages whose
compiled code is reached through R’s array-based .Fortran() or .C() interfaces enter at
phase 1, as KernSmooth does. Packages reached through .Call(), which exchanges R’s
own internal objects rather than plain arrays, first pass through the prologue (left), which
reconstructs the portion of R’s C API the package uses so that its original compiled source
can be built and executed without libR.so; rpart enters there, and its fake headers and
entry-point wrappers feed the core. Prologue phases are labeled P1–P5 so that the plain
numerals 1–7 always denote core phases, which are invariant across packages. Whether
the prologue is needed is decided by the interface; how much work it involves is set by the
number of C API symbols the package references, which a static scan establishes before
conversion begins. Each phase that a skill orchestrates names that skill and the sub-agent
it dispatches, together with the dispatch mode: sequential where one invocation must read
an earlier one’s output, parallel where invocations are independent, and iterative where a
fix-and-recheck cycle runs to a stopping criterion. The coda is an additional step required
only by packages with a substantial presentation surface; it is not part of the core, and
KernSmooth did not require it.




                                             24
r2py: AI-Assisted Conversion of R Statistical Packages to Python


            KernSmooth   — 16 functions, 3 levels                                                                       rpart        — 47 functions, 6 levels
converted
   last
                                                                                                                                                                         residuals.
             .onAttach bkde     dpih      dpill                        .onUnload   meanvar.rpart   path.rpart           plotcp             post.rpart     print.rpart      rpart             rpart       summary.rpart          tfun

       level 0                                               level 0
                 .onUnload bkde2D    dpik                                    meanvar      model.frame.    plot.rpart                post         predict.rpart       prune       roc.rpart           rsq.rpart     text.rpart      xpred.rpart
                                                                                             rpart

                                                                            descendants      na.rpart           oval             printcp          rectangle      rpart.class     rpart.exp      rpart.poisson ss.compare

                                                             level 1
                                                                                    labels.rpart   node.match          pred.rpart      prune.rpart       rpart.anova    rpart.control   rpart.matrix      rpartcallback      string.
                                                                                                                                                                                                                          bounding.box


                 bkfe     cpblock locpoly       sstdiag                                                                                     drate2       importance

       level 1                                               level 2
                    blkest    linbin2D      sdiag                                                                                                    formatg      snip.rpart

                                                                                                                                                  snip.rpart.
                                                                                                                                                   mouse

                                                             level 3



                           linbin                                                                                                                rpart.branch

       level 2                                               level 4
                                rlbin                                                                                                                      rpartco



                                                                                                                                                  compress

                                                             level 5
                                                                                                                                                          tree.depth

converted
   first
                                        leaf: calls no other function in the package                              calls at least one other package function



Figure 2: The dependency graph that fixes conversion order. Each node is a
function defined by the package; an edge joins a function to one it calls. Functions are
assigned a level by longest path from any root, and conversion proceeds from the deepest
level upward, so that when an agent translates a caller the Python interfaces of everything
it calls already exist. Leaves—functions calling no other function in the package—carry
no such prerequisite, and can be translated in any order. KernSmooth’s 16 functions
resolve into three levels and rpart’s 47 into six. Both graphs are wide and shallow: 7 of
KernSmooth’s functions and 28 of rpart’s are leaves, so much of each conversion carries
no ordering constraint at all, and only five of rpart’s 47 functions lie deeper than level
two. The graph is the output of phase 1 and is deposited with the software.




                                                                                              25
r2py: AI-Assisted Conversion of R Statistical Packages to Python



                                                    Top-level orchestration
                                                  Multiple input files in parallel


                      R / Python source                   JSON / CSV                              Markdown
                       files / fragments                dependency maps                        conversion guides




                                                        Skill ( / Command )
                                                          applies context-
                                                         construction logic



                                                                                                           Phase 7b
                                                    Per-item context bundle
                  Phases 1, 4, 6, 7a
                                                                                        Phase 3b

                                                   Sub-agent dispatch modes
         Sequential dispatch                                                     Parallel dispatch


          Single agent instance
                                               Agent instance 1           Agent instance 2           ...      Agent instance N
             ( ordered list )


      Writes           Next item               Writes                      Writes                              Writes


         Output artifact                       Output artifact 1           Output artifact 2         ...      Output artifact N


                                                         Iterative dispatch


                                                                   Run tests
                               First failure
                                                                    All passed
                                                                                                                        Repeat

                                                             All passed
       Fix-agent instance




                                                             Reinstall package




Figure 3: Skill–sub-agent orchestration. A skill assembles per-item context bundles
from shared inputs and dispatches sub-agents in one of three modes. The mode is de-
termined by the dependency structure of the work rather than chosen for convenience.
Sequential dispatch is used where an invocation must read the output of an earlier one;
parallel dispatch where invocations are mutually independent; iterative dispatch where a
fix-and-recheck cycle runs until a stopping criterion is met.




                                                                   26
r2py: AI-Assisted Conversion of R Statistical Packages to Python


                          Reconstructed R's C API headers
                                                                                   Function-pointer callbacks
                         Category E - R interpreter bridge (5)               ( eval, findVar, findVarInFrame )
           eval · findVar · findVarInFrame · install · R_getVar
                 eval / findVar / findVarInFrame: Python callback
                              install: self-contained                                               Python
                    R_getVar: macro alias for findVarInFrame                                       ( cffi )
                         reachable only for user-defined splits                Registers
                                                                                callbacks
                                                                               at import
                           Category D - Diagnostics (4)                                                  cffi call
                         error · warning · Rprintf ·
                             R_CheckUserInterrupt
                                                                                       5 pure-C entry-point wrappers
                 Category C - Allocation & memory management (7)                    rpart_c.c · pred_rpart_c.c · xpred_c.c ·
           allocVector · allocMatrix · R_alloc · R_chk_calloc ·                       rpartexp2_c.c · init_rpcallback_c.c
                        R_Free · mkChar · setAttrib                               marshal SEXP ↔ plain int/double arrays;
                                                                                  ArenaFrame + exception boundary per call
                          Category B - Accessors (16)
    INTEGER · REAL · CHAR · PROTECT · UNPROTECT · LENGTH · PRINTNAME ·                 Constructs SEXP &
     ISNAN · R_FINITE · asInteger · asReal · isReal · ncols · nrows ·                 Calls original function
                      SET_STRING_ELT · SET_VECTOR_ELT
                                                                                                                      libR.so
                                                                              #include "fake_R.h"                    not linked
             Category A - Types, enum constants & registration no-ops (19)
                                                                                     in place of
      SEXP · INTSXP · REALSXP · STRSXP · VECSXP · DL_FUNC · DllInfo ·
                                                                               R.h / Rinternals.h
    R_CallMethodDef · Rboolean · TRUE · FALSE · R_VERSION · R_Version ·                                                 Replace
       R_NilValue · R_NamesSymbol · R_UnboundValue · R_forceSymbols ·
                  R_registerRoutines · R_useDynamicSymbols                         rpart's original C sources - Unmodified
                                                                                             35 C and header files
                                                                                                ( 30 unchanged,
                      fake_arena.h - Thread-local arena allocator
                                                                                    5 with #include directives substituted )
               ArenaFrame (RAII) · arena_alloc · arena_calloc
                                                                                             func_table.h dispatch:
                freed automatically when each .Call() boundary returns
                                                                                 init_split / choose_split / eval / error




Figure 4: Reconstructing R’s C API as standalone headers. The prologue replaces
R’s C API with self-contained implementations of exactly those symbols the target pack-
age references, so that the package’s original compiled sources build and execute without
an R runtime. For rpart the 51 symbols divide into five categories of sharply differ-
ing difficulty: types and registration no-ops (19), accessors (16), allocation and memory
management (7), diagnostics (4), and operations on R’s interpreter (5). Only the last
category reaches beyond what standalone C++ can provide. Four of the five are resolved
by callbacks into Python and the fifth by a compatibility macro that expands into two of
those four; of the four, only expression evaluation genuinely requires an interpreter. In
rpart the category as a whole is reachable only when the user supplies a custom splitting
rule.




                                                                  27
