                                                     A Trust Ledger and an Execution Check for
                                                     CPG-Based C-to-Lean 4 Autoformalization:
                                                              Separating Declined from
                                                           Silently Incorrect Translations


                                                         Ishan K Singavarapu                                Manish Bhatt
arXiv:2609.38237v1 [cs.PL] 28 Sep 2026




                                                             Independent                                       OWASP
                                                     ishansingavarapu@gmail.com                      manishbhatt13212@gmail.com



                                                                                         Abstract

                                                     Verifying large C codebases requires translating them into formally checkable se-
                                                     mantics, but most autoformalization work reports a single aggregate success rate
                                                     that conflates two different failure modes: code the translator declined to handle
                                                     and code the translator translated incorrectly. We present a deterministic code-
                                                     property-graph (CPG)-based exporter that translates C source into a small Lean 4
                                                     core semantics under a three-tier correctness discipline: hole-free, call-closed,
                                                     and dynamic-hole-risk, that keeps these modes distinct. Applied to a re-export of
                                                     the SQLite source tree (8,602 functions, over 1.5 million AST nodes), the exporter
                                                     translates 5,222 functions (60.7%) hole-free, of which only 2,134 (24.8%) are call-
                                                     closed, a 2.4× gap a single rate would hide. Both figures are reported in a full per-
                                                     construct trust ledger rather than a single score. Our main contribution is method-
                                                     ological: a protocol for separating constructs that are fundamentally unresolvable
                                                     by whole-program static analysis (such as public API boundaries) from constructs
                                                     that only look that way. For example, we retracted our own “impossible” classifi-
                                                     cation of function-pointer/vtable dispatch after tracing a concrete counterexample
                                                     in the target codebase. Separately, a search for “more holes closed” surfaced a la-
                                                     tent silent-wrong-answer bug: a translation that succeeded with an incorrect result
                                                     rather than declining, a failure mode we argue is more dangerous than any hole,
                                                     and one a hole-count-only evaluation would never surface.


                                         1    Introduction

                                         An autoformalization pipeline turns code into an artifact a proof assistant can check, and reports
                                         how much of the input it managed. That number carries an implicit promise: raising it means the
                                         translation got better. The promise is rarely stated, because it sounds like a truism: translating more
                                         of a program must mean translating it better.
                                         Those are two different claims, and this paper separates them. We report six cases of decoupling
                                         from a deterministic code-property-graph (CPG) based pipeline that translates C into a small Lean 4
                                         interpreter, together with one finding about the metric’s own vocabulary. Four of the six are correct-
                                         ness defects whose repair moved no coverage number (A1–A4). One is a coverage movement that
                                         closed no construct (B1). One is a corrected impossibility claim that changed 17 translations and
                                         moved no coverage number either (C1). The seventh finding, T1, is a defect in the cause taxonomy
                                         that the coverage report is built from; it is not a case of independent movement, which is why six
                                         cases yield seven findings. Table 1 lists all seven under these labels. Each is a concrete, dated change
                                         to a real pipeline, with the values it was verified against.

                                         Preprint.
The distinction that matters is between two ways a translation can fail. A construct the translator
declined to handle leaves an explicit, labeled gap, and coverage counts it. A construct the transla-
tor handled incorrectly produces well-typed output that type-checks, is counted as translated, and
computes the wrong answer. Coverage cannot see the second class, by construction: it is a fold over
the artifact, and a wrong answer is a property of running the artifact. That much is an observation
about definitions. What this paper adds is that the gap is not hypothetical, that it is populated by or-
dinary constructs — character literals, do-while loops, variadic signatures — and that it runs in both
directions, so movement in the metric is not evidence either way.
Two terms recur throughout. A function is hole-free when nothing in its translated syntax tree is a
placeholder standing in for a construct the translator declined, and call-closed when it is additionally
free of calls to functions that were never translated. §2 states both precisely.

Three categories, and which mechanism supplies each. The title names three outcomes, and it
is worth saying at the outset which part of the discipline yields which. The ledger separates declined
from verified, per construct rather than in aggregate, and that itemization is what makes §3.2 legible
at all. It cannot separate verified from silently incorrect, because that distinction is not a property
of the artifact the ledger folds over. Recovering the third category requires executing the translated
program against the real language implementation. The discipline reported here is therefore the three
tiers and an execution check, and §3.1 is the argument for the second half rather than a concession
about the first.

Why existence claims. Our claims are existential, and that is deliberate. To show that coverage
and fidelity are decoupled, one case in each direction suffices, and one case is not weakened by
having been observed on a single pipeline. We make no claim about how often they decouple, or
that the magnitudes here transfer. Where we report a magnitude, such as the 2.4× denominator
effect in §4, it is a measurement on one codebase and labeled as such.

Contributions.
1. An evaluation protocol for separating declined from silently incorrect (§3): the method-
   ological contribution. Some constructs are unresolvable by whole-program static analysis in
   principle. A public API entry point is called from outside the analyzed program, so no work
   inside it recovers the caller. Others only look that way until someone traces one. Applying that
   distinction produced six cases: four correctness defects repaired with no metric movement, one
   metric movement that made no construct translatable, and one retracted impossibility claim that
   moved the metric by nothing while changing 17 translations. Each is reported with its corpus
   and its verified values.
2. Instability of the cause taxonomy (§3.4): the number of distinct hole causes is not a stable
   quantity, because a label built from source text partitions on the source.
3. The denominator effect (§4): read purely as coverage, the reported figure on SQLite differs by
   2.4× depending on whether call closure is required, and containment makes some gap certain
   while its size is the measurement.
4. What we report instead, and its limits (§5): three non-collapsible tiers, holes itemized by
   cause, and an execution check — together with the finding that none of the three suffices, since
   §3.1 is a list of defects all three missed.

2   The pipeline and the metric
The pipeline is context for the findings rather than a contribution, so we describe only what is needed
to read §3 and §4.
A definitional interpreter for a compact universal source language (“Core”) is written once in Lean 4
[2]. It is fuel-indexed and total, structurally recursive on a fuel budget, with no partial and no
sorry. A codebase is mechanically transpiled into a term of that interpreter’s syntax type, so a
program becomes an ordinary Lean data value and every property of it is a theorem about eval
applied to a concrete AST. Because the semantics is a computable interpreter, the translated program
can be run and compared against the real language implementation, which is what §3.1 relies on.


                                                   2
Table 1: The findings, with what each change did to the translated program beside what it did to the
coverage metric. The second column reads behavior / metric. Five changes altered what the program
computes while the metric stayed put or moved by less than 0.15 points; one moved the metric by 47
label occurrences while changing nothing the program computes. A coverage rate is read as a proxy
for translation quality, which assumes these two agree. In this pipeline they are inverted. Rows A are
the four correctness changes the metric did not register. Row B is the metric movement that closed
no construct, with its second instance beneath it. Row C is a corrected impossibility claim that
changed 17 translations and moved the metric by nothing. Row T is a defect in the vocabulary the
metric is reported over rather than a case of independent movement, so it carries no behavior / metric
entry. Corpora and commit labels are given per case in the text and in Appendix A.
        behavior /   Finding                                   What changed                      What the metric did    How it was found
        metric
  A1    YES / no     Character literal rendered as a string,   loop returned 0 for every         hole count and every   executing the
                     so *p == ’x’ compared an integer          input; after the fix 3, 2, 0,     label unchanged,       generated code
                     with a string                             matching compiled cc              5,033 to 5,033
  A2    YES / no     do B while(C) emitted as                  cc -O0 returns 1, translation     both shapes            a hand-built fixture
                     while(C) B                                returned 0; 7 functions           hole-free, so no       against cc
                                                               changed                           coverage number
                                                                                                 separates them
  A3    YES / no     C variadic signatures marked as           surplus arguments packed as a     no hole emitted,       test suite meeting a
                     Python varargs                            tuple under the wrong calling     before or after        large corpus
                                                               convention, for every
                                                               printf-style function
  A4    YES /        Struct local whose address escapes        statically hole-free, failed at   hole-free +0.05 and    a differential-test
        barely       to an in-program call                     evaluation with                   +0.12 points on        fixture
                                                               setField:*:non-object             two scopes
  B1    no / YES     Sentinel casts had been mislabeled        no fidelity change; the same    one label −31,          reading the labels,
                                                               constructs carry a more         another +16,            not the total
                                                               accurate cause                  hole-free +1
  second instance of B1: interior-pointer labels reclassified to a more precise cause, one label 10 to 5, no new coverage
  C1    YES / no     Vtable dispatch proven closed after       translated output of 17           zero net new           a full content diff
                     being recorded as impossible              functions changed; 19             hole-free functions
                                                               (function, parameter) pairs
                                                               closed
  T1    —            Hole labels built from source text        every source fragment became      15 distinct causes     a label-taxonomy
                                                               its own “cause”                   collapsed to 2         test




Joern’s code property graph [9] supplies a single node vocabulary, so the pipeline writes one
CPG-to-JSON exporter and one JSON-to-Lean printer, both deterministic, with no model on the
translation path. Two consequences matter here. First, a construct the exporter cannot trans-
late faithfully becomes a hole tagged with the CPG label that produced it, so declined con-
structs are counted by cause rather than in aggregate. Second, the whole system is downstream
of one parser version, pinned in the artifact (joern-version at 4.0.606, lean-toolchain at
leanprover/lean4:v4.30.0-rc1).



The metric. Coverage is reported under a three-tier discipline, never collapsed into one score.
A function is hole-free when its AST contains no hole. It is call-closed when it is hole-free and
every call target also resolves inside the translated program. That is the population which supports
unconditional reasoning: in the AST, a call to a function that was never translated is indistinguishable
from a call to one that was. Dynamic-hole risk counts constructs that may still hole on some input;
it is reported for completeness and carries none of the findings below, which turn on the first two
tiers. The findings in §3 are about what these numbers do and do not track.



One structural blind spot, stated up front. Joern parses C without running the preprocessor, so
a definition whose signature defeats the parser is not holed but absent, with no row anywhere in
the ledger. Coverage is therefore an accounting of what was attempted, not of what the codebase
contains. This is separate from the decoupling result and we do not count it among the seven
findings.


                                                                      3
3     Coverage and fidelity move independently

Table 1 shows every change in the two dimensions that matter, with the measured values beside
each. We give the load-bearing detail below, grouped by direction, and note in each case what did
surface it.

3.1   Correctness changed and the metric did not

A1: a character literal rendered as a string. The exporter’s literal dispatch had no case for a bare
single-quoted literal, so it fell through to a generic “starts with a quote” branch and rendered ’x’
identically to "x". In C a single-quoted literal is a number, the character’s own codepoint. Reading
a byte through a tracked cursor already correctly produced that byte’s integer value, so *p == ’x’
compiled into an integer-versus-string comparison that the semantics’ equality never treats as equal.
A byte-counting loop therefore compiled with zero holes and returned 0 for every input. The repair
recognizes numeric character literals in the pipeline’s C-like dialect — the front-end grammar it
uses for C, as distinct from its Python and JavaScript ones — and handles the standard escapes,
leaving a multi-character literal or an unrecognized escape to fall through unchanged rather than
guessing. Verification was by execution: over "axxbxcdef" at n = 9, 3, 1 the loop now returns 3,
2, 0, matching compiled cc exactly.
Like A2, this case is checkable rather than reported, and we checked it. A committed specification
builds the same loop twice inside the semantics, differing in exactly one leaf: the literal the byte is
compared against. With the character’s codepoint it reproduces 3, 2 and 0; with the string it returns
0 on every input, including the two where cc prints 3 and 2. All five values are pinned by guards
that fail the build if any changes, and the disagreement is restated as a theorem discharged by rfl
on the permitted axiom basis. The defective shape is retained as a negative control, for the reason
this case exists at all: the defect never appeared as a hole, so nothing in the ledger would notice a
regression to it.
On the bounded SQLite corpus of 3,560 functions — an iteration corpus smaller than the 8,602-
function export of §4, and the denominator for this case — the hole count and every individual label
were unchanged: 5,033 before the fix and 5,033 after. Every function comparing a byte against
a literal character became correct, and no number in the coverage report recorded it. This is the
cleanest case in the paper because the metric did not move even slightly; a reader who tracked only
coverage would have seen a no-op commit.

A2: a do-while loop emitted as a while loop. The exporter matched case "WHILE" | "DO"
and emitted the same loop statement for both. A do-while runs its body at least once, while the
emitted form tests first, so the two disagree whenever the condition is initially false. Checked
against cc -O0, do { n = n + 1; } while (0) returns 1 and the translated while form re-
turned 0. The repair emits while (true) { B; if (C) skip else break }, rewriting each
continue belonging to that loop, because a do-while’s continue jumps to the condition test and
the while(true) shape has no test to reach. Seven functions in a C++ corpus changed.
No hole was involved at any point. The construct translated to a real statement before the fix and a
real statement after it, so both versions are hole-free and no coverage number can separate a correct
loop from an incorrect one.
This case is the one we can hand a reviewer in full, and we note the difference because the rest of
§3 rests on deltas recorded with each change. Three links are independently checkable, and we have
checked all three.
The compiler disagreement reproduces with nothing installed but a C compiler. The conflation is a
single committed line, case "WHILE" | "DO", replaced in the diff by two separate cases. And the
repair is pinned inside the semantics itself: building the specification with the pinned toolchain elab-
orates both shapes under guards that fail the build if either value changes, and both match, at 1 and 0.
The disagreement is additionally restated as a theorem discharged by rfl, which #print axioms
reports as depending on exactly {propext, Classical.choice, Quot.sound}, so it carries no
sorry and no compiler-trust leak. We also confirmed the guard is not vacuous by mutating the
expected value from 0 to 99, which fails the build as required. The specification retains the defective
shape as an explicit negative control, on the stated grounds that “a future regression to Stmt.loop


                                                   4
would remove a hole and look like progress.” A script reproducing all three links accompanies the
artifact. We note that device because it is the natural response to A1 and A2 together: if the metric
cannot distinguish the two shapes, the test suite must.

A3: C variadic signatures treated as Python varargs. The exporter gates one Python-specific
parameter analysis on the file extension but did not gate the variadic flag, which C and C++ set
for .... A signature such as void V8 Fatal(char*, ...) therefore carried a vararg marker,
instructing parameter binding to pack surplus arguments into a tuple under Python’s calling conven-
tion. Every printf-style function in the corpus was silently mistranslated. C’s ... is read through
va arg, which the pipeline does not translate, so the marker is now not emitted for non-Python
sources at all. No hole was emitted before or after, so the metric was blind to both the defect and its
repair.
This case is pinned like A1 and A2, and it states the paper’s distinction most directly. A committed
specification builds the same signature twice, differing in exactly one field. Under the marker, a
three-argument call silently binds the two surplus arguments as a tuple; with the marker removed,
the same call is refused. Neither models va arg, and that is the content of the case rather than an
omission: the defect converted a call the pipeline would have declined into one it answered wrongly.
Both values are pinned by guards, the difference is a theorem on the permitted axiom basis, and the
defective shape is retained as a negative control.

A4: a struct address escaping to an in-program call. A struct local whose address is passed
to another translated function was excluded from the boxing analysis, while field access emitted
unconditionally for any class-typed receiver. The result translated as statically hole-free and then
failed at evaluation with setField:*:non-object. The defect was confirmed to predate the work
that found it by checking it against an earlier merge commit. Repair moved hole-free by 0.05 and
0.12 percentage points on two SQLite scopes, which is movement, but movement two orders of
magnitude smaller than the correctness change it represents.

3.2   The metric moved and the translation did not

B1:      an apparent 31-hole improvement that was a relabeling. One change
reduced     op:cast:opaque-type           from    46    to    15      occurrences     while    raising
op:cast:pointer:int-to-pointer from 14 to 30. The cause is not a closure: sentinel
casts of the SQLITE TRANSIENT family had been mislabeled as an opaque type and are now
correctly recognized as pointer casts with a non-pointer-shaped operand. Hole-free moved by one,
across fourteen changed functions. A reader tracking the largest label would record a 31-occurrence
improvement; a reader tracking hole-free would record one function. The honest reading is that the
pipeline’s description of a construct got more accurate while its treatment of it did not change.
A second instance in the same family makes the same point at smaller scale:
op:addressOf:element:opaque-type fell from 10 to 5, and the five are the same func-
tions carrying the more precise op:addressOf:element:object instead. No construct became
translatable. We count the two together as one finding, since they are the same phenomenon in one
commit family.

3.3   A corrected claim, with no movement either way

C1: a retraction that moved nothing and changed 17 functions. Function-pointer and vtable
dispatch had been recorded as a fundamental limit of whole-program static analysis, in the same
category as a public API entry point called from outside the analyzed program. Traced rather than
defended, the claim did not survive: SQLite assigns its own function pointers to its own functions
and calls them entirely within the analyzed source, as pPage->xCellSize = cellSizePtr; and
pPage->xCellSize(pPage, &data[pc]) in btree.c. The exporter had been choosing not to
prove closure, through a blanket “address ever taken, therefore unclosable” guard, and not for want
of information. Widening an existing scan to record plain function-pointer field assignments closed
19 (function, parameter) pairs.
The yield in coverage was zero net new hole-free functions. A full content diff nonetheless found
17 functions whose translated output changed while their hole count stayed at zero, and targeted


                                                  5
elaboration confirmed the new output well-typed. So this single change exhibits the decoupling in
both directions at once: a wrong classification was corrected and 17 translations changed, and no
tier of the metric registered any of it.
A defect caught inside the same change is worth recording, because it is the same phenomenon one
level down. The new whole-program fixed point depended on a table that only fills as the priming
passes run. Declared as a lazy val, it memoized an empty snapshot on first access and silently
never recomputed, so the mechanism measured exactly zero effect until that was found and it was
made a def recomputed once per pass. A check that shares an assumption with the thing it checks
will flatter it, and here the sharing was a cache.


3.4   The metric’s vocabulary is not stable either

T1: labels built from source text. The remedy for an aggregate rate is to itemize declined con-
structs by cause (§5), which presumes the set of causes is a property of the pipeline. It was not.
The stmt:UNKNOWN: label carried the first word of the offending source, so one C++ corpus alone
produced separate “causes” named ), }, V8 WEAK;, and a fragment of a C++ requires clause. Be-
cause the ledger groups by label, every source fragment became its own cause. Keying the label on
the parser node type instead collapsed 15 distinct labels to 2, both of which name a remedy rather
than a symptom.
The consequence is narrow but worth stating: “number of distinct hole causes” is not a quantity
one can compare across pipelines, or even across corpora of the same pipeline, without knowing
how labels are constructed. We report 70 causes in §4 for a specific export, not as a property of the
approach.


3.5   What surfaced them, and what did not

The distinction that matters is between the metric read as a rate and the metric read as an itemized
inventory, because the two have different diagnostic power and the paper’s findings fall cleanly on
either side of it.
Not one of the four correctness defects was surfaced by either reading. A1 and A2 came from
running the generated program and comparing it against the real language implementation. A3 and
T1 came from a test suite that had only ever been exercised on small corpora and failed immediately
when a large one was tracked, which is an argument for tracking a large artifact rather than pointing
a manifest at a temporary file. A4 came from writing a differential fixture for an unrelated change.
C1 came from diffing translated output rather than counting holes.
The two relabelings in B1 are the exception, and they cut the other way. Neither is visible in any
total: the first moves two labels in opposite directions and the hole count by one, and the second
moves no total at all. Both are obvious the moment the breakdown is read per cause. That is the
concrete argument for itemizing rather than reporting a rate, and it is an argument the aggregate
cannot make for itself.



4     Read purely as coverage, the denominator decides the number

Section 3 argues coverage does not track fidelity. It remains a useful report of what was attempted,
and this section measures how much the reported number depends on a choice that is easy to leave
implicit. All figures come from one committed export (sqlite numbers.json, module Sqlite,
dialect c-like) and are summarized in Figure 1: 8,602 functions and 1,513,464 AST nodes, of
which 5,222 (60.7%) are hole-free and 2,134 (24.8%) are call-closed, with 14,260 residual holes
itemized under 70 causes — a count §3.4 shows is a property of the labeling scheme rather than of
the codebase — and 216,730 constructs carrying dynamic-hole risk, the last counted per construct
rather than per function.


                                                 6
              translated 8,602 functions, 1,513,464 AST nodes
                 hole-free 5,222 (60.7%)                                  declined, itemized
                                                                          14,260 holes / 70 causes
                    call-closed            2.4× wider: no hole of
                                           their own, callee unresolved   dynamic-hole risk
                    2,134 (24.8%)
                                                                          216,730 constructs

                                    silently incorrect
                           well-typed, counted as translated,
                              computes the wrong answer
                           no tier bounds it; A1–A3 are here



Figure 1: The ledger’s tiers are strictly nested, so a gap of some size is certain and only its magnitude
is a measurement. The dashed region is the class this paper is about. It crosses every tier boundary
because it is not a property of the artifact the tiers fold over: a silently incorrect translation is
hole-free, may be call-closed, and is counted as translated. No denominator excludes it and no
cause itemizes it, which is why recovering it needs an execution check rather than a better rate. The
diagram is schematic: areas are not to scale, and the right-hand column is not a subset, since declined
constructs are counted per cause and dynamic-hole risk per construct rather than per function.


Call-closed is a subset of hole-free by construction, so a gap is guaranteed and is not itself a result.
What is measured is the size: 2.4×. The functions in between contain no holes of their own and
call something that does not resolve inside the translated program, so their behavior is unknown
for a reason no hole count inspects. Reporting hole-free alone therefore overstates the population
that supports unconditional reasoning by that factor, on this codebase. We do not claim the factor
transfers; we claim that the choice of denominator is a reporting decision with a measurable effect,
and that papers reporting a single coverage rate rarely state which one they made.
The distribution of declined constructs is itself informative, and dominated by C
pointer and address semantics — precisely the constructs that resemble ordinary opera-
tions while admitting no faithful value-semantics translation. The ten largest causes are
cstr:address-compare (1,415), cstr:pointer-arith (1,338), assign:lhs:indirection
(1,150), op:addressOf:element:scalar (1,121), op:cast:pointer:int-to-pointer
(952), op:indirection:pointer (947), op:cast:opaque-type (720), control:GOTO (503),
op:postIncrement:pointer (492), and stmt:UNKNOWN:CASTProblemDeclaration (463),
with 5,159 occurrences across 60 further causes. Each is a declined construct with a named
boundary rather than a silent mistranslation, which is the property §3 shows coverage does not
otherwise guarantee. The 70-cause figure should be read with §3.4 in mind.

5   What we report instead, and why it is not sufficient
The constructive proposal is modest, and §3 is the argument for its insufficiency rather than its
adequacy. Three things, in order of cost. Report three tiers and never collapse them, so that the
denominator is explicit, since §4 shows that choice is worth 2.4× on this corpus and it is usually left
implicit. Itemize every declined construct by its cause, so that “the other 40%” is a list rather than a
residue and a relabeling such as B1 is visible as a relabeling. Then pin at least one executed fixture
per construct family against the real language implementation, because §3.1 is four defects that no
tier detected.
The cheapest version of the third is the device the three specifications of Appendix B use: record the
correct value and retain the defective shape as a negative control, so that a regression cannot present
itself as progress. Each is about forty lines, needs no infrastructure beyond the proof assistant already
in the pipeline, and turns a defect the metric cannot see into one the build cannot miss.
The pipeline carries four independent checks for the last step: differential testing against a real
runtime, a mutation gate that injects a defect and asks whether a specification still proves, an ax-
iom sweep with an independent kernel replay permitting exactly {propext, Classical.choice,
Quot.sound}, and an execution oracle that runs the claimed call-closed population over many in-
puts. Results compose into a SACM assurance case [6] that tracks evidence kind separately from
strength, so that a claim discharged by passing tests is never read as proved, and caps population-


                                                            7
quantified claims by coverage so that “zero divergences” over a minority of a population cannot read
as support.
Two honest qualifications. First, the checks are only as live as their plumbing, and C1’s lazy val is
the pipeline’s own example of a mechanism that measured zero because it had memoized an empty
input. Second, no population-level conformance result exists for the SQLite export reported in §4.
The differential harness selects a runtime per language and is not wired for this corpus, so the checks
that ran on the changes in §3 were narrower than a population oracle: targeted elaboration of exactly
the functions each change touched, a content diff of the re-exported corpus, and direct execution
of hand-built fixtures against compiled cc. Fixture-level execution is sufficient for the existence
claims in §3 and insufficient to say how many further defects remain, which is the honest state of
the evidence.


6   Limitations

Falsifiability. If a coverage metric could be shown to move whenever a silent mistranslation is
repaired, the central claim would fail; the cases here are counterexamples, and a counting exercise
over a pipeline’s whole fix history could in principle find that they are rare enough to ignore. If
a second large codebase showed hole-free and call-closed coinciding, the 2.4× denominator effect
would be specific to C pointer semantics rather than to whole-program translation. If a population-
level oracle found no defect outside the declined set, the execution check would buy nothing here.

What a reader can check, and what they must take on report. A1, A2 and A3 are checkable
end to end, and we checked all three: compiler ground truth, the committed exporter change, and
specifications that build with every pinned value matching on the permitted axiom basis, where
mutating a value fails the build. Three of six is not all of them, and the gap is the honest state of the
evidence. The remaining cases are recorded deltas: the counts we quote are the values the artifact
records with each change, and a reader who wants to re-derive them needs the parser, the proof
assistant, and the corpus. We separate the two because they are not equally strong evidence, and
because the cheap fix generalizes — every case in §3.1 could carry a fixture and a negative control
of the kind A2 has, and we would report a stronger paper if they all did.

Existence, not frequency. We show decoupling occurs. We do not show how often, and the cases
are not a sample from a defined population; they are the defects this pipeline happened to find, by
the means listed in §3.5. A pipeline with different construct coverage would decouple differently.

One pipeline, and cases from more than one corpus. All seven findings come from one system.
The coverage measurement in §4 is a single SQLite export. A2, A3, and T1 were measured on a
C++ corpus and the rest on SQLite; we label each because a defect in the exporter is a property of
the exporter rather than of a corpus, while a coverage figure is not.

Provenance of the coverage artifact, and how far it matters. The export behind §4 carries no
recorded provenance in the artifact: no export command, no parser version recorded beside it, no
source revision, and no companion AST to cross-check its function count, which is the check the
project applies to its other corpora and the only one that detects a stale artifact. It is registered with
no consistency gate. We therefore cannot confirm it reflects the exporter at the commit it sits on. The
risk is bounded, and its direction is worth stating. The tier ratio and the per-cause itemization are
read from fields of one internally consistent file, whose 70 label counts sum exactly to its reported
hole total. So if the export is stale, the absolute population moves, while the 2.4× ratio and the
distribution remain properties of a real export of this codebase. Nothing about staleness can make
a hole count and a call-closed count agree. The decoupling result in §3 does not depend on this
artifact at all, since each case is a dated change with its own measured deltas.

Fidelity is tested, never proved. No theorem relates the CPG, the exported JSON, the printed
Lean, and the source program’s meaning. The evidence is execution against a real compiler plus
printer determinism, and the ledger says so in the artifact rather than implying more.


                                                    8
7   Related work
Diagnostic evaluation of autoformalization. The closest work rejects the same scalar: a signal-
coverage matrix crosses elaborator success with a semantic-equivalence judgment to sort statement-
autoformalization outputs into four cells, arguing that a headline type-correctness rate conceals
which errors a method resolves [1]. FormalRx replaces opaque verdicts with a 28-category error
taxonomy plus localization and correction [7]. Both operate on natural-language-to-formal state-
ment translation, where the unit is a statement and the failure axes are type-checking and semantic
equivalence. We claim no novelty for distinguishing declined from incorrect. Our result is orthogo-
nal in a specific way: those taxonomies partition failures a judge can observe in the artifact, whereas
§3.1 is a set of defects invisible to any partition of the artifact, because detecting them requires exe-
cuting it. §3.4 adds that a taxonomy of causes can itself be unstable, which bears on any of this work
that reports category counts. Call closure has no analogue when the unit is one statement, since there
is no surrounding program for a callee to be absent from.

Verified compilation. CompCert established that a realistic compiler can be proved correct end to
end [5]. We make the opposite trade deliberately and report the consequence: the translator is not
proved correct, so its fidelity is an empirical question, and §3 is what asking that question turned up.

Differential testing. Random differential testing found large numbers of compiler defects by dis-
agreement with a reference [10]. A1 and A2 are the same technique applied to a translator rather
than a compiler, and the observation we add is that the defects it finds are systematically the ones a
coverage metric cannot see. Mutation testing measures whether a suite constrains behavior [4], and
the negative control in A2’s specification is that idea applied to a single repair.

Functional translation and code property graphs. Aeneas verifies Rust by functional translation
into a pure model [3]; we adopt the same deep-to-shallow refinement but drive it from a language-
agnostic CPG [9] rather than a single source language. LLM-based autoformalization [8] motivates
the closing observation of §8.

8   Declaration of LLM usage
LLM-based coding assistants were used in engineering the artifact and in preparing this manuscript.
They are not on the translation path: the CPG-to-JSON exporter and the JSON-to-Lean printer are
deterministic and contain no model, and the Lean kernel is the sole arbiter of what is proved. Every
figure was checked against a committed artifact, with the artifact and field recorded in Appendix A.
We note where the result bears on such systems. A model that emits a well-typed wrong answer
produces exactly the class of failure §3.1 describes. We have not measured a model-based pipeline,
and we make no claim about how its failure mass is distributed. What transfers is the argument
rather than a quantity: a coverage metric is blind to this class by construction, whatever produced
the translation, so the remedy is the same — execute the artifact and compare it against the language
implementation, rather than counting what was attempted.

References
 [1] C. Dai, Z. Yan, and Z. Lin. The signal-coverage matrix: Stratifying type and semantic errors
     in statement autoformalization. arXiv:2606.28013, 2026.

 [2] L. de Moura and S. Ullrich.    The Lean 4 theorem prover and programming lan-
     guage. In Automated Deduction (CADE 28), LNCS 12699, pages 625–635, 2021. doi:
     10.1007/978-3-030-79876-5 37.

 [3] S. Ho and J. Protzenko. Aeneas: Rust verification by functional translation. arXiv:2206.07185,
     2022.

 [4] Y. Jia and M. Harman. An analysis and survey of the development of mutation testing. IEEE
     Transactions on Software Engineering, 37(5):649–678, 2011. doi:10.1109/TSE.2010.62.


                                                   9
 [5] X. Leroy. Formal verification of a realistic compiler. Communications of the ACM, 52(7):107–
     115, 2009. doi:10.1145/1538788.1538814.
 [6] Object Management Group. Structured Assurance Case Metamodel (SACM), version 2.1.
     OMG formal specification, adopted April 2020.
 [7] H. Wang, B. Huang, Y. Wan, X. Zhu, X. Liu, Y. Huang, and Z. Guo. FormalRx: Rectify
     and eXamine semantic failures in autoformalization. In International Conference on Machine
     Learning (ICML), 2026. arXiv:2607.04655.
 [8] Y. Wu, A. Q. Jiang, W. Li, M. N. Rabe, C. Staats, M. Jamnik, and C. Szegedy. Autofor-
     malization with large language models. Advances in Neural Information Processing Systems
     (NeurIPS), 2022. arXiv:2205.12615.
 [9] F. Yamaguchi, N. Golde, D. Arp, and K. Rieck. Modeling and discovering vulnerabilities with
     code property graphs. In 2014 IEEE Symposium on Security and Privacy, pages 590–604,
     2014. doi:10.1109/SP.2014.44.
[10] X. Yang, Y. Chen, E. Eide, and J. Regehr. Finding and understanding bugs in C compilers. In
     PLDI 2011, pages 283–294, 2011. doi:10.1145/1993498.1993532.


Reproducibility
The artifact is available at https://github.com/mbhatt1/autoform. The findings are each a
dated change in it, listed with its commit label in Appendix A; the deltas quoted in §3 are the
values recorded with those changes. Three of the six cases are runnable rather than recorded, and
the scripts are shipped with the artifact. One reproduces A1, A2 and A3 over three links each: it
compiles the C ground truth and prints 3, 2, 0 and 1 versus 0; locates the defective exporter line
and its replacement; then builds all three specifications, reports the axiom basis of their theorems,
and mutates an expected value to confirm the guards are not vacuous. The first link needs only a
C compiler; the third needs the proof assistant. We ran both: all three specifications build under
the pinned toolchain with every guard matching, the four theorems depend on exactly the permitted
axiom basis, and mutating an expected value fails the build as required. A second script recomputes
every derived figure in §4 from the export’s fields and checks the export’s internal consistency,
including that its 70 per-label counts sum to the reported total. It also lists the provenance fields the
export does not carry, which is the subject of §6. Every figure in §4 is therefore checkable without
running the pipeline. Reproducing the export itself needs the SQLite source tree and a parser run,
and §6 records that the command and revision were not committed beside the numbers. Pinned
dependencies: Joern 4.0.606, Lean v4.30.0-rc1, and for the reference values in §3.1 the system
C compiler invoked as cc -O0; the artifact records those values as measured on x86-64, and we
reproduced them on arm64. If a document and an artifact disagree, the artifact wins.

NeurIPS Paper Checklist
1. Claims [Yes] The abstract and §1 state an existential decoupling result in two directions, the
   denominator measurement, and explicitly disclaim frequency and transfer. Each figure is traced
   in Appendix A.
2. Limitations [Yes] §6 covers falsifiability, existence versus frequency, the single pipeline, the
   mixed-corpus provenance of the cases, the unrecorded provenance of the coverage artifact and
   how far it propagates, and fidelity being tested rather than proved.
3. Theory assumptions and proofs [Yes] The permitted axiom basis and the mandatory fresh
   kernel replay are stated in §5. No new theorem is claimed.
4. Experimental reproducibility [Yes] Each finding is a dated change with recorded deltas; §4’s
   figures are fields of one committed file, checkable without running the pipeline. §6 records the
   one barrier to re-running the export.
5. Open access to data and code [Yes] The artifact is available at https://github.com/
   mbhatt1/autoform, and the reproduction scripts described in Appendix B are included as
   supplementary material. §6 records that the source AST behind the coverage export is not in the
   artifact.


                                                   10
 6. Experimental settings and details [Yes] Corpora, dialect, parser pin (4.0.606) and toolchain pin
    (v4.30.0-rc1) are given in §2 and §4, and each case in §3 names the corpus it was measured
    on.
 7. Error bars and statistical significance [N/A] The results are deterministic counts and existence
    claims, not sampled estimates. Where a claim is population-quantified, §5 caps it by coverage
    rather than reporting a rate with error bars.
 8. Compute resources [Yes] No GPU and no model training. The largest reported export is 8,602
    functions and 1,513,464 AST nodes; iteration corpora of 3,560 and 3,807 functions were re-
    exported per change, with targeted elaboration of only the functions each change touched. We
    do not report wall-clock or peak memory for the export, because the artifact does not record
    them and we could not re-run it (§6); the fixtures of Appendix B build in a few seconds each.
 9. Code of ethics [Yes] The work conforms to the NeurIPS Code of Ethics.
10. Broader impacts [Yes] The result is a negative one about a widely used metric, intended to
    discourage reporting coverage improvement as evidence of fidelity. The foreseeable misuse is
    selective quotation: the hole-free figure exceeds the call-closed figure by 2.4× here, and quoting
    the larger alone overstates what is verifiable. No model or dataset with dual-use potential is
    released.
11. Safeguards [N/A] No high-risk model or dataset is released.
12. Licenses for existing assets [Yes] Lean 4 and Joern are both Apache-2.0; the SQLite source is
    public domain by its authors’ declaration. All three are cited in §2 and §4. The artifact itself
    carries no license file, which we note as a gap to close before release rather than a claim about
    its terms.
13. New assets [Yes] The artifact is documented, including the trust model and the ledger schema.
14. Crowdsourcing and human subjects [N/A] None.
15. IRB approvals [N/A] None.
16. Declaration of LLM usage [Yes] §8 declares usage and states that no model is on the translation
    or proof-checking path.

Appendix A            Provenance of every reported figure
Commit labels P1–P8 are resolved to hashes in the supplementary material’s PROVENANCE.md,
which also maps neutralized module and file names to the artifact’s own paths. P1 is the change
that adds the coverage export; it was raised on a branch and has since been merged, so every figure
in this paper is reachable from the artifact’s default branch. P2–P8 are on that branch also.

          Table 2: Every reported figure, with the artifact field or commit it is read from.
   Ref    Figure                                                    Value                               Source
   §4     functions / AST nodes                                     8,602 / 1,513,464                   P1, functions, nodes
   §4     hole-free                                                 5,222 (60.7%)                       P1, holeFree
   §4     call-closed                                               2,134 (24.8%)                       P1, call-closed
   §4     tier gap                                                  2.4×                                derived,
                                                                                                        5,222/2,134 = 2.45
   §4     residual holes / causes                                   14,260 / 70                         P1, holes; 70 label entries
                                                                                                        summing to 14,260
   §4     dynamic-hole risk                                         216,730                             P1, dynamicHoleRisk
   §4     ten largest causes; remainder                             as listed; 5,159 over 60 causes     P1, holesByLabel;
                                                                                                        remainder derived
   A1     0 for every input; 3, 2, 0 after; labels unchanged        5,033 to 5,033 on 3,560 functions   P5
   A2     cc -O0 1 versus translated 0; functions changed           7                                   P8
   A3     variadic marker on C signatures                           no hole either side                 P8
   A4     hole-free movement on two scopes                          +0.05 / +0.12 points                P6, predating P7
   B1     label movement; hole-free                                 46 → 15, 14 → 30; +1 over           P4
                                                                    14 functions
   B1     interior-pointer relabel (second instance)                10 → 5                              P3
   C1     pairs closed; net hole-free; output changed               19; zero; 17 functions              P2
   T1     distinct labels collapsed                                 15 to 2                             P8
   §2     parser and toolchain pins                                 4.0.606 / v4.30.0-rc1               artifact pin files
   §5     permitted axiom basis                                     propext, Classical.choice,          audit script
                                                                    Quot.sound




                                                               11
Appendix B        The three pinned fixtures
Each fixture builds the same construct twice inside the semantics, differing in exactly the leaf the
exporter got wrong, and pins both values. The correct value is what a C compiler prints. The
defective value is retained deliberately: every one of these defects was hole-free, so nothing in the
coverage ledger would notice a regression to it, and a specification that recorded only the correct
value would not either.
Table 3: What each fixture pins. Every value is checked at build time, and each defective value is
kept as a negative control.

  Case           The one leaf that differs          Correct, per cc       Defective shape
  A1             the literal a byte is compared     3, 2, 0 over          0 on every input
                 against: codepoint versus string   "axxbxcdef" at
                                                    n = 9, 3, 1
  A2             the loop statement emitted for a   1                     0
                 DO node
  A3             whether a C ... signature          the call is refused   the surplus arguments bind
                 carries a vararg marker                                  as a tuple


All four theorems across the three fixtures report the same axiom basis, {propext,
Classical.choice, Quot.sound}, so none rests on sorry, on native decide, or on any
compiler-trust escape. We also confirmed the guards are not vacuous by mutating an expected value
in each fixture, which fails the build. The accompanying script performs the build, prints the axiom
bases, and runs one such mutation.
Each fixture is roughly forty lines and needs no infrastructure the pipeline does not already have.
The three remaining cases in §3 are not pinned this way: B1 and T1 concern label counts in an
export rather than the behavior of a program, and C1 needs whole-program call-closure analysis
rather than a single construct. We regard the first two as not fixturable in this form and the third as
work not yet done.




                                                    12
