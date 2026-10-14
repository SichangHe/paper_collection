                                                   Djinnlang: Higher-Level Programming by
                                                 Unambiguous Specification with an LLM in the
                                                                  Compiler
                                                    Simon Henniger✉                             Stephen Chong                              Nada Amin
                                                 shenniger@fas.harvard.edu                 chong@seas.harvard.edu                  namin@seas.harvard.edu
                                                     Harvard University                       Harvard University                      Harvard University
                                               Cambridge, Massachusetts, USA             Cambridge, Massachusetts, USA           Cambridge, Massachusetts, USA

                                         Abstract                                                          1   Introduction
arXiv:2609.23954v1 [cs.PL] 21 Sep 2026




                                         Programmers write formal specifications, and LLMs imple-          Here is a plausible future of programming: programmers
                                         ment them, proving that each implementation matches its           specify, LLMs implement and prove their implementation
                                         spec. Taken to its extreme, this makes specification languages    matches the formal spec. Taken to its extreme, this scenario
                                         the new programming languages. We argue that an unam-             has specification languages become the new programming
                                         biguity constraint is key: in addition to proving that its im-    languages. Similar to high-level programming languages
                                         plementation satisfies the specification, the LLM must also       building on machine instructions, high-level specification
                                         prove that any other implementation satisfying it must pro-       languages will abstract upon pure pre/post conditions.
                                         duce the same outputs on the same inputs, i.e. that the rela-         Compared to existing spec languages, we propose to in-
                                         tion formed by the constraints is deterministic. This leaves      troduce an unambiguity constraint. Under the constraint, a
                                         the LLM no leeway on program semantics: as with a conven-         spec will only yield executable code if it is unambiguous, i.e.
                                         tional compiler, the generated code never needs to be read        if it fully describes the outputs for any given set of program
                                         and can be regenerated from the spec at any time. Under           inputs. We show that, with the unambiguity constraint and
                                         this constraint and with a powerful LLM, the difference be-       an LLM implementer, the difference between a specification
                                         tween a specification language and a programming language         language and a programming language becomes essentially
                                         becomes essentially meaningless, and the LLM essentially          meaningless.
                                         becomes a part of the compiler toolchain. The arrangement             We present Djinnlang, an attempt to build such a speci-
                                         doubles as a strong form of AI control: an untrusted model        fication language. With an LLM implementer, it becomes a
                                         writes the code, yet its work is tightly checked by a verifier.   general-purpose programming language. In lieu of a tradi-
                                            To demonstrate that our LLM-in-the-compiler paradigm           tional compiler, it comes with a translator (which symboli-
                                         is feasible when supported by our unambiguity constraint,         cally translates the spec into Dafny stubs) and a driver pro-
                                         we present Djinnlang, a high-level specification language         gram (which orchestrates calls to LLMs that write the actual
                                         built for this future. A Djinnlang program consists only of       implementation). Figure 1 shows the whole arrangement on
                                         specifications — the programmer never writes executable           a single example function: five lines of Djinnlang on the left,
                                         code. In place of a traditional compiler, a symbolic transla-     and on the right the Dafny obligations our translator emits
                                         tor lowers each spec to Dafny stubs and proof obligations,        from them. An LLM will add proofs and implementation.
                                         and a driver harness orchestrates an LLM that fills in im-            Our spec language looks, feels, and behaves like a higher-
                                         plementations and proofs, all checked by the Dafny verifier.      than-usual-level programming language. By extension, its
                                         We evaluate our language and implementation on multiple           compiler, which includes an LLM and harness, feels (apart
                                         examples and we show that it is self-hosting: an LLM can          from performance and cost) like a normal compiler toolchain.
                                         implement the Djinnlang translator from its specification         The verifier ensures that the LLM’s programs satisfy the
                                         and the reimplementation can verify itself.                       specification and the unambiguity constraint ensures that it
                                                                                                           never has any leeway on semantics. Hence, like a compiler
                                         CCS Concepts: • Software and its engineering → Formal
                                                                                                           and unlike in regular vibecoding, there is almost never a need
                                         software verification; General programming languages;
                                                                                                           to read the code it produced, and the code can be regenerated
                                         Automatic programming.
                                                                                                           from the spec at any time. Consequently, we show a new
                                         Keywords: Specification languages, compiler engineering,          and underexplored use-case of LLMs in compiler design:
                                         LLMs for Software Engineering, formal verification, rela-         when carefully used in tandem with a verifier, they allow for
                                         tional programming                                                stronger abstractions.
                                                                                                                               Henniger, Chong and Amin

Djinnlang (written by a human)                Dafny (emitted by djinnc)
func max(list: seq<int>) -> r: int            ghost predicate max_preconditions(list: seq<int>) { (|list| >= 1) }
requires |list| >= 1:                         ghost predicate max_spec(list: seq<int>, r: int)
  r in list                                   { max_preconditions(list)
  for x in list:                                 && ((r in list) && ((forall x | x in list :: (x <= r)) && true)) }
    x <= r                                    lemma max_is_unambiguous(list: seq<int>, o1: int, o2: int)
                                                requires max_spec(list, o1)
                                                requires max_spec(list, o2)
                                                ensures o1 == o2
                                              { /* TODO(LLM): prove. */ }
                                              lemma max_exists(list: seq<int>) requires max_preconditions(list)
                                                ensures exists r: int :: max_spec(list, r)
                                              { /* TODO(LLM): prove. */ }
                                              function max(list: seq<int>): int requires max_preconditions(list)
                                              { /* TODO(LLM): implement. */ }
                                              lemma max_implementation_is_correct(list: seq<int>)
                                                requires max_preconditions(list)
                                                ensures max_spec(list, max(list))
                                              { /* TODO(LLM): prove. */ }

Figure 1. A complete Djinnlang function and the Dafny obligations djinnc produces from it (predicate names renamed for
readability). The left column and the two ghost predicates are trusted: the predicates are a mechanical transcription of the
constraints. Each obligation is pinned, such that a model can only add the bodies but never change the definitions. Note the
unambiguity constraint, in bold, which is described in Section 2. Details on the other proof obligations are in Section 4.2.

1.1   Structure and Contributions                                         2     The Unambiguity Constraint
In this paper, we make the following contributions:                       Currently, most program properties are not proven by default.
    1. We introduce the unambiguity constraint. We argue                  We only prove particular propositions about programs that
       that a function should be considered unambiguously                 we care about.
       specified by a set of constraints when the relation                   In the LLM era, we propose to turn this principle on its
       made up of those constraints is deterministic. We dis-             head and instead unambiguously specify everything about a
       cuss the advantages and limitations of this definition             program by default, except where explicitly carved out.
       (Section 2).                                                          This becomes necessary because LLMs are now producing
    2. We introduce the LLM-in-the-compiler paradigm                      tons of code with little to no human supervision. But LLM
       which puts an LLM into a compiler toolchain (Sec-                  output can fail in two ways: models misread specifications,
       tion 3).                                                           hallucinate, and err, and a model may also subvert its task
    3. Then, we describe Djinnlang, a general-purpose lan-                deliberately — a possibility safety arguments increasingly
       guage in which programmers write only specifications               decline to exclude [10]. Thus, the LLM must be tightly con-
       and which uses the unambiguity constraint and LLM-                 strained. Even in a context where LLMs write all the code, they
       in-the-compiler paradigm (Section 4).                              should have no leeway at all on program semantics.
    4. We evaluate the language design qualitatively on spe-
                                                                          2.1     Deterministic Relations
       cific examples which show the language is general-
       purpose (Section 5).                                               Concretely, we propose to consider a function1 to be unam-
    5. We describe the implementation of our Djinnlang com-               biguously specified when the relation derived only from its
       piler pipeline that includes an LLM and a verifier, pro-           specification is deterministic. In other words: to prove a that
       viding a practical example of a compiler that directly             a function is unambiguously specified by a set of constraints,
       integrates an LLM (Section 6).                                     we prove that any two functions that satisfy the set of con-
    6. We evaluate the implementation empirically, measur-                straints must return the same outputs given the same inputs.
       ing specification, code, and proof size, proof effort,             Write pre(𝑥)¯ for the conjunction of a declaration’s precon-
       cost, and the performance of the generated programs                ditions and 𝑞(𝑥,¯ 𝑜) for the relation its constraints define be-
       across two LLM implementers (Section 7).                           tween inputs 𝑥¯ and output 𝑜. The unambiguity obligation is
   Finally, we discuss related work (Section 8), the limitations          then
of the approach (Section 9), and future work (Section 10),                      ∀¯                 ¯ ∧ 𝑞(𝑥,
                                                                                 𝑥, 𝑜 1, 𝑜 2 . pre(𝑥)    ¯ 𝑜 1 ) ∧ 𝑞(𝑥,
                                                                                                                     ¯ 𝑜 2 ) =⇒ 𝑜 1 = 𝑜 2,
and conclude (Section 11).                                                1 Throughout the paper, we use the term function as used in programming,

                                                                          not as used in mathematics. In other words, a function is a piece of executable
                                                                          code. It is not a special case of a relation. We realize this is initially confusing.




Preprint.
Djinnlang: Higher-Level Programming by Unambiguous Specification with an LLM in the Compiler


                                                                                          spec
                                                                                                                             Verifier
                                                                                                        impl.            checks impl and
                                                    Djinnlang                                                           proofs against spec
                        Human
                                                    Translator
                      Programmer        .djinn
                                                 translates to Dafny
                         (possibly
                                                 spec + implemen-
                       LLM-assisted)                                                   Harness                              Dafny
                                                 tation/proof stubs    stubs                                    impl.
                                                                                     fills impl+proof                      Compiler
                                                                                     stubs via LLM                        compiles impl.

                                                                                              calls

                                                                                         LLM


Figure 2. The compilation pipeline. The translator turns the programmer’s spec into a trusted Dafny spec and implementation
stubs; the harness has an LLM fill in the stubs; the verifier checks the resulting implementation against the Dafny spec; the
Dafny compiler receives only the implementation.

and it comes with an existence obligation,                                       Elegance. Specs need far less operational bookkeeping,
                 ∀¯       ¯ =⇒ ∃𝑜. 𝑞(𝑥,
                  𝑥 . pre(𝑥)         ¯ 𝑜).                                     and they often tend to be shorter than the code they replace
                                                                               and closer to how the programmer already thinks about
Once 𝑞 is a total deterministic relation, an implementation                    the problem: sort is a permutation constraint plus a sort-
has nothing left to decide about what the program computes.                    edness constraint—no algorithm required. As we will show,
                                                                               stringtoint is quickly obtained from inttostring, as a
2.2   Advantages
                                                                               preimage.
This lets us write programs only as specifications and have
LLMs implement them entirely unsupervised, in the good                            Performance and Universality. . This arrangement
conscience that our intended program behavior has been                         makes a human specify everything that matters to them
entirely specified and our will (as we wrote it down in the                    about code, while leaving all details up to the LLM. LLMs
specification) is going to be enforced by the verifier.                        can do very comprehensive performance optimizations, and
   A possible objection is that we are merely kicking the can                  a verifier can check their correctness. We think a future
down the road. If programmers write specifications instead                     iteration of this spec language could even be implementation-
of programs, will these specifications not be equally error-                   language-agnostic.
prone and hard to maintain as current programs?                                   We show concrete examples of the first two advantages
   While we agree that this is by no means the end of all                      when we evaluate the language design (Section 5); the third
bugs, we think there are a number of clear advantages to                       is measured empirically in Section 7.
writing unambiguous specifications as opposed to programs.
                                                                               2.3     AI control
   Contradictions and safety. Many bugs come down to                           There are concerns about models actively trying to subvert
contradictions and inconsistencies. One function thinks of                     their overseers. One response to these concerns is AI control,
something in one way, another in another, or even one line                     usually by protocols — trusted editing, untrusted monitor-
within a function does it one way, another in another way. In                  ing — that lower the probability that undesired outputs like
specs, it is even easier to contradict yourself. But contradic-                backdoor slips through safety mechanisms [10].
tions are discovered because they make the spec unsatisfiable,                   Our unambiguity constraint could be considered a very
thereby failing at compile time instead of in production. We                   thorough type of AI control, one which not only strategi-
argue that, with spec-based programming, the old adage DRY                     cally reduces the model’s power, but also provides a formal
(don’t repeat yourself) will be obsolete: it will be good prac-                guarantee on what it has no power (program outputs) versus
tice to repeat yourself, to write out what you have in mind                    some power (performance) over.
in as many different ways as possible, because this allows
the verifier to check your work and avoids bugs. Another                       2.4     Limitations
way of thinking about this is that, every line in Djinnlang                    Our approach also introduces new dangers. For instance,
becomes another little piece that you know for certain about                   the specifics of an LLM-provided implementation will still
your program (because you wrote it down, an LLM had to                         determine other factors like performance. This is often de-
prove it for you, and the verifier has confirmed it)—and more                  sirable as LLMs are good code optimizers. But of course, it
of that is unambiguously better.


                                                                                                                                              Preprint.
                                                                                                             Henniger, Chong and Amin


also introduces additional safety concerns (e.g. on timing-         stubs: an implementation stub and a proof stub for every
sensitive cryptography code or DoS-style attacks with code          obligation, each with an empty body for the LLM to fill in.
that is intentionally slow on some inputs). While highly                The harness helps the LLM do that. It hands the stubs,
timing-sensitive cryptography code (the kind where even             together with the spec they refer to, to an LLM and asks it to
performance deviations of a few cycles can lead to successful       fill them in with executable code and proofs. The harness is
side-channel attacks) will likely always remain out of scope        a driver: it makes no judgment about the LLM’s output and
for this class of languages (as they are for many high-level        simply passes it on.
programming languages), we think there can be some im-                  The verifier is the Dafny verifier. It checks the filled-in im-
provements to the current situation. Future extensions of           plementation and proofs against the translator’s spec. When
this language should include simple syntax for specifying           it fails, the harness returns to the LLM with the verifier’s
bounds on baseline performance and scaling behavior and             complaints; when it passes, the Dafny compiler receives the
computational complexity.                                           implementation and produces the executable.
   Another danger is that of bugs in verifiers. If a verifier
or another component of the infrastructure that invokes             4    Djinnlang
a verifier does fail, we are at the mercy of the now fully          After having described our two primary ideas, the unambi-
unsupervised LLM which may be harmful and dangerous                 guity constraint and the LLM-in-the-compiler paradigm, we
in all kinds of ways. We feel that, in general, our faith in        now describe Djinnlang, a proof of concept language that
verifiers is justified, but risks will always remain.               leverages both.
                                                                       In Djinnlang, a programmer will only ever write con-
3   The LLM-in-the-compiler paradigm                                straints, no code.
We propose an LLM-in-the-compiler paradigm, which has                  In spite of this, we still want Djinnlang to be a general-
LLMs become a part of a compiler toolchain. Unlike existing         purpose programming language. We aim to show that most
approaches for LLMs in software engineering, the outputs of         programs can be somewhat comfortably expressed in this
our LLM are tightly verified by other parts of the toolchain.       language. We provide facilities for imperative-style code that
This makes LLMs feel (apart from performance and cost)              interacts with the outside world and has side effects.
no different than traditional program synthesis algorithms.            In some sense, Djinnlang is a relational programming
This is connected to the unambiguity constraint: only this          language, and it shares a surface with one: equations rather
constraint ensures that the LLM never has any leeway on             than assignments, existential binders, choice, and the ability
semantics. Hence, very much unlike in regular vibecoding,           to run a function backwards by constraining its output. It
there is almost never a need to read the code it produced,          differs from other relational languages, such as Verse [3],
and the code is disposable. It can be regenerated from the          in what it does about ambiguity. A Verse expression may
spec at any time.                                                   yield many values and Verse lays choices out in the syntax of
   Of course, using an LLM inside a toolchain does not pre-         the term rather than exploring them non-deterministically.
clude, but rather complements, other LLM uses on the same           Djinnlang instead forbids ambiguity (except where it can
code. A programmer writing code in the spec language may            be resolved in other parts of the program): a func must be
want to additionally use an LLM to help with that task (more        proved to relate each input to at most one output. Verse
in line with standard vibecoding), and all the benefits of read-    must find an evaluation strategy that solves the equations,
ability and contradiction detection would still apply in this       which its authors leave to future work and which cannot
situation.                                                          succeed in general — by their own account the semantics
   Figure 2 shows the pipeline of our programming language          is “un-implementable”, since no rewrite system will find the
Djinnlang, which is an example of the LLM-in-the-compiler           solution to ∃𝑥 . 𝑥 2 − 𝑥 − 6 = 0. That is exactly the burden we
paradigm. The pipeline has the shape of an ordinary compiler        hand to an LLM, which is unpredictable but nearly universal,
toolchain, with one unusual stage in the middle.                    and check with a verifier.
   The programmer, a human, writes a .djinn file containing            To focus on the novel aspects of this language, we piggy-
only specifications. They may or may not be assisted by             back on Dafny for everything else. Djinnlang defines no type
an LLM while doing so, but that is their prerogrative. The          system and no standard library of its own: any Dafny type
specification is the only trusted, human-generated artifact.        may be used in signatures, any function or predicate from
   The translator is a conventional, symbolic compiler stage.       the ambient Dafny context may be called from constraint ex-
It parses the source and emits two things. The first is a trusted   pressions, and Dafny’s built-in vocabulary (cardinality |s|,
Dafny spec: for every func, rel, and proc, the relation be-         indexing s[i], slicing s[a..b], membership x in s, . . . ) is
tween inputs and outputs that its constraints define, plus          used directly in expressions. We are hoping to create variants
the proof obligations of Section 2 — unambiguity, existence,        that build on Verus instead of Dafny, as well as on emerging
and the exported ensures clauses. The second is a set of            Lean-based code verification systems.



Preprint.
Djinnlang: Higher-Level Programming by Unambiguous Specification with an LLM in the Compiler


  There are three top-level constructs: functions, procedures,            rel completion(g: seq<int>) -> c: seq<int>
and relations. Functions (func) become Dafny functions.                   requires |g| = 81:
They are guaranteed to be pure (no side effects) and to be                  |c| = 81
                                                                            for i in 0..81:
unambiguous (deterministic). Procedures and relations each                    1 <= c[i] <= 9
drop one of these guarantees: Procedures are unambiguous,                     g[i] != 0 => c[i] = g[i]
but can have side effects. Relations, on the other hand, are                for i in 0..81:
pure, but can be nondeterministic; to Dafny, they are predi-                  for j in 0..81:
cates and carry no executable code.                                             i != j && sameunit(i, j) => c[i] != c[j]
  Within a function, relation, or procedure, each line is a                  Read imperatively, this is the validity checker one would
constraint. Each states a fact relating the inputs to the output,         write by hand: walk the cells, check each digit is in range and
and the body means the conjunction of its lines:                          agrees with any given, then walk the pairs and check that
func max(list: seq<int>) -> r: int                                        no two cells sharing a unit collide. Read logically, the same
requires |list| >= 1:                                                     text defines the set of solved grids, and a solver is obtained
  r in list                 # r is one of the elements ...                by saying its answer belongs to that set. The checker is not
  for x in list:                                                          written twice, and the nested loop that an imperative reader
    x <= r                  # ... and none of them is larger
                                                                          sees — 6561 iterations — is a quantifier that costs nothing and
   Nothing here says how to find the maximum—no accumu-                   constrains no algorithm; the implementation may propagate
lator is carried and nothing is compared in any particular                constraints and never enumerate a pair.
order. The two lines only pin down which output is accept-                   The disguise keeps specifications skimmable by readers
able, and between them they admit exactly one; the LLM                    not fluent in logic, which matters when the specification is
supplies an implementation and proves it meets them.                      the only artifact anyone reads, and it suits an implementer
   Headers may carry requires and ensures annotations:                    who is unfamiliar with logic or relational programming.
func naturalnumbertostring(i: int) -> s: string                              However, it can sometimes mislead. We acknowledge that
requires i >= 0    # callers prove this at every call
ensures |s| >= 1: # exported to callers; must follow
                                                                          the syntax can appear confusing and alien at first, similar
  ...              # from the body                                        to how an imperative programmer might initially struggle
   Every func and proc implicitly includes an existence                   to read a functional program. For instance, lines may look
proof (for every valid input, an output exists) and a termi-              sequential but hold simultaneously, so a reader tracing data
nating implementation; a contradictory spec is rejected. A                flow looks for an order that is not there. A for that a program-
rel, on the other hand, may be partial (total opts in to                  mer reads as accumulating cannot accumulate, since there is
realizability), and a proc may be marked noreturn when it                 no state to carry; inductive definitions must be recursive. An
is meant to run forever (an event loop) — everything else                 if without an else does not mean “do nothing otherwise”
provably halts.                                                           but leaves the output unconstrained, which would often be
                                                                          rejected as ambiguity.
4.1   Relations in Imperative Clothing
                                                                          4.2   Functions
Note that = is equality, not assignment. s = f(x) and f(x)
= s mean the same thing, so constraints can be written                    We will now discuss the three types of top-level blocks in
“backwards” — here parsing is specified in terms of printing:             depth, beginning with functions.
func stringtoint(s: string) -> r: int:
                                                                             A func is translated to a Dafny function. It must be speci-
  if s in range(inttostring):                                             fied unambiguously and must not have side effects.
    inttostring(r) = s      # r is whatever prints as s                      For a func f(xs) -> o: T the translator emits, into the
  else:                                                                   trusted file, a predicate f_pre(xs) conjoining the requires
    r = 0                   # error handling                              clauses and a predicate f_spec(xs, o) holding exactly
   The same is true for other constructs. Djinnlang’s syn-                when the body’s constraints relate the inputs to the out-
tax is borrowed from structured imperative programming —                  put. Into the solution file it emits the following obligations,
indentation-delimited blocks, if/else, for, one statement                 in this order, each with an empty body:
to a line, infix =. But none of it executes. Instead, a body is               1. unambiguity — for fixed inputs any two outputs satis-
the conjunction of its lines (which can thus be in any order,                    fying f_spec are equal. This is unambiguousness: the
with the exception of do statements in proc, see below). if                      relation is a function.
C: B else: E is 𝐶 ⇒ 𝐵 with ¬𝐶 ⇒ 𝐸, and for x in xs:                           2. postconditions — one lemma per ensures clause, de-
B is ∀𝑥 ∈ 𝑥𝑠. 𝐵.                                                                 riving it from f_spec. A postcondition that does not
   Oftentimes, this is very intuitive and makes the specifi-                     follow from the body is rejected rather than assumed.
cations look like imperative programs. For instance, here is                  3. existence — some output satisfies f_spec for every in-
the rulebook of Sudoku:                                                          put admitted by f_pre. A contradictory specification
                                                                                 dies here.


                                                                                                                                Preprint.
                                                                                                           Henniger, Chong and Amin


    4. implementation — a compiled, terminating Dafny func-       for a relation marked total, the test degenerates to the
       tion with the same signature. This is the only stub that   precondition, since the output is guaranteed.
       is code rather than proof.
    5. implementation correctness — the implementation’s          4.4   Procedures
       output satisfies f_spec, unconditionally on the pre-       A proc is where the language meets the outside world, and
       condition domain.                                          it was the hardest part of the design to settle. The difficulty is
    6. call sites — where the body calls something with a         that a specification is a set of simultaneous constraints while
       requires, its precondition holds under everything          effects happen one after another: nothing in a conjunction
       known at that point. Omitted when the body incurs          says which of two effects comes first.
       none.                                                         We have settled on an algebraic effects system that ex-
   Find an example function with all proof and implementa-        presses imperative code as a step function. As an illustrative
tion obligations in Figure 1.                                     example, printing two words becomes a function from the
                                                                  last completed step to the next one,
4.3   Relations                                                   func hello_step(last: StepResult) -> s: Step:
A rel is only a set of constraints. Its specification could be      if last = Initial:       s = PrintHello
                                                                    else if last = Hello:    s = PrintWorld
ambiguous and thus the function nondeterministic. It is not         else if last = World:    s = Return
directly implemented and never executable. It provides loose
                                                                    together with a driver written directly in Dafny:
vocabulary for other specs to refine. A rel can only be used
                                                                  method hello_world() {
inside a func and proc and it is the user’s job to resolve any      var last := Initial;
ambiguity.                                                          while true {
   Calls to relations cannot have side effects.                       match hello_step(last) {
# one input, many outputs: fine                                         case PrintHello => print("Hello"); last := Hello;
rel perm(list: seq<int>) -> t: seq<int>:                                case PrintWorld => print("World"); last := World;
  |t| = |list|                                                          case Return     => return;
  for x in list:                                                      }
    multiset(t)[x] = multiset(list)[x]                              }
                                                                  }
  With perm, the sort above can be written as perm(list)
= r plus the ascending constraint. With the latter, sort sort        procs are syntactic sugar for this above construct. When-
will be unambiguously specified even when perm is not.            ever a specification contains a proc, the translator auto-
                                                                  matically creates the step function (which the LLM must
   Partial and total relations. A func is total by construc-      implement and which must be unambiguously specified like
tion: it must relate every input admitted by its preconditions    any other function) and a Dafny driver function. Because
to some output, and that is one of the obligations it owes.       the Dafny driver function is mechanically generated by the
A rel is not. Left unannotated, a relation is partial: it may     translator and never touched by the LLM, we can trust it.
relate an input to no output at all, and the language asks for       Within a proc, each step becomes a do instruction.
no proof that it does. Annotating it total adds exactly the       proc hello_world():
existence obligation a func carries, pre(𝑥)¯ ⇒ ∃𝑜. 𝑞(𝑥, ¯ 𝑜).       do print("Hello")
   Similar to unambiguousness, relations could be partial,          do print("World")
but this partiality needs to be resolved in whichever func-         # implicit return; `return` may also be written
tions they are used. Marking a relation total resolves this          Not only can we call functions, but we can also use
problem, which will often make proofs at the call-site easier.    and change local and global variables, e.g. by writing do
   We chose partiality as the default because a relation’s        myvariable := 42.
domain is frequently the point of writing one. A relation            As seen in our example above, do calls are chained to-
with no output on some inputs is a predicate in disguise,         gether by the order in which they appear, making do the
and the language exposes it as one: x in domain(q) holds          big exception in a language in which order generally does
exactly when q accepts x and relates it to at least one output,   not matter. This trivially works across if statements. An if
so a specification can branch on solvability without ever         condition is conjoined onto the guards of the events inside,
exhibiting a solution. The Sudoku specification of Section 7.1    whose predecessors remain whatever precedes the if.
is written this way — a puzzle has a solution precisely when it      For loops, a loop’s last event is chained either to the first
lies in the domain of the completion relation, and the answer     event of the next iteration or to whatever follows the loop,
must be a completion exactly when that test succeeds —            according to the loop condition. Because all clauses sharing
and the same device gives substring search as membership          a predecessor carry mutually exclusive guards, the machine
in the domain of a match-position relation. For a func, or        is deterministic by construction and the translator can dis-
                                                                  charge that proof itself.



Preprint.
Djinnlang: Higher-Level Programming by Unambiguous Specification with an LLM in the Compiler


   On top for for, procedures also allow for while loops,                 rel perm(list: seq<int>) -> t: seq<int>
where the loop condition is always a step and can thus de-                total:
pend on outside factors that change during the loop.                        |t| = |list|
                                                                            for x in list:
   for loops can contain do statements, but then they end                     multiset(t)[x] = multiset(list)[x]
up imposing an execution order, which must be syntactically
marked by using ordered for. Not every valid for condition                func sort(list: seq<int>) -> r: seq<int>:
is also a valid ordered for condition: if a set that is iterated            perm(list) = r          # (1) r is SOME permutation...
over has no inherent order, ordered for cannot be used as                   # You can conceptualize this as sets and
                                                                            # read this first line as:
it would be ambiguous. ordered for is sugar for a while                     # r in set_of_all_permutations(list)
with an assigned index: bounds are evaluated once on entry,                 for i in 0..|r|-1:
and the index is readable in the body, not reassignable, and                  r[i] <= r[i+1]        # (2) ... namely a sorted one,
out of scope afterwards.                                                                            # resolving perm's ambiguity
proc printstring(s: seq<char>) -> r: int:                                   Note that, in order to show sort is deterministic, the LLM
  ordered for i in 0..|s|:                                                implementer must show that <= is a total order on int. If
   do putchar(s[i])    # one event per character, in order of i           we attempt this on a different type for which this is not the
  r = |s|
                                                                          case, the verifier will flag the issue.
   The pure constraints in a proc behave as they would in a
func: they hold throughout the run rather than at the point               5.2   int to string
where they are written. This can initially be confusing. In               You can implement inttostring inductively or iteratively.
do x := "10", then a = stringtoint(x), then do x :=                       The inductive implementation is elegant, but we still show an
"hello", the middle line is not a step but a claim about every            iterative implementation (although both are logically equiv-
value x ever takes, so the specification is contradictory and is          alent and thus will not lead to programs of different speeds),
rejected. To avoid this, constraints can be scoped to only hold           because it helps us demontrate how deliberate redundancy
after certain steps using a then: block, whose constraints                lets the verifier catch mistakes. We implement it as two
bind only for its extent and whose relational variables are               functions, first nattostring and then a small wrapper that
scoped to it; it must immediately follow a do, a while, or an             handles the sign. The first function:
ordered for.                                                              func nattostring(i: int) -> s: string
   Beyond what a func gives, a proc guarantees that events                requires i >= 0:
occur in the specified order, because every event’s guard                   |s| = (if i = 0 then 1 else log(10, i) + 1)
names its predecessor, and that state changes only where di-                for k in 0..|s|:
rected, because the driver hands the state tuple back verbatim                s[|s|-1-k] = ('0' as int + i/pow(10,k) % 10) as char
                                                                              s[|s|-1-k] >= '0' # DO REPEAT YOURSELF. Challenge
and never inspects it. Contract proofs use an implementer-                    s[|s|-1-k] <= '9' # your beliefs about your code by
chosen machine invariant over that state. By default, each                                       # writing them out.
proc is also proven to terminate, though this can be dis-                   i = 5 => s = "5"         # read: if i = 5 then s = "5"
abled using the noreturn attribute. We aim to implement                     i = 128 => s = "128"
higher-level specifications about the event trace (Section 10).              While this is superficially similar to a direct implementa-
                                                                          tion (apart from missing housekeeping like explicitly resizing
5     Evaluating the Language Design                                      the target string), there are some benefits: first, you’ll note
We evaluate Djinnlang against the goals set out in the in-                that the last four lines are not actually necessary. They are
troduction. We aim to show that it is elegant by present-                 an example of “do repeat yourself” and seamlessly introduce
ing examples in which the spec is shorter and closer to the               constraints that the verifier checks. Second and more impor-
programmer’s intent than the code it replaces — sorting                   tantly, note that this is a bit hairy and many small mistakes
(Section 5.1), and stringtoint obtained as a preimage of                  could occur. Some examples:
inttostring (Section 5.3). Between the two we show that                       • For instance, let’s suppose that we write % 100 instead
deliberate redundancy lets the verifier catch realistic mis-                     of % 10. This would trivially be caught by the verifier
takes in a specification of integer printing (Section 5.2). The                  in the s[|s|-1-k] <= '9' constraint.
general-purpose design principle is borne out by the compiler                 • Suppose the index had been written s[|s|-k] rather
itself, which is written in Djinnlang (Section 6.5). For the                     than s[|s|-1-k]. At k=0 that constrains s[|s|],
remaining advantage, performance, we refer to Section 7.                         which is out of bounds and caught by the verifier;
                                                                                 s[0] would also be left unconstrained, so determinism
5.1   Sorting a list                                                             would fail too.
The canonical example for any specification language is                       • The off-by-one in the other direction, s[|s|-2-k],
sorting. We first define a rel which maps a list to each of its                  is caught symmetrically: for k=|s|-1, we would
permutations and then use it:


                                                                                                                               Preprint.
                                                                                                          Henniger, Chong and Amin


         constrain s[-1], again out of bounds, and s[|s|-1]        6     Implementation
         would additionally be left unconstrained.                 Figure 2 gives the vague shape of the toolchain. In this sec-
   The second function, inttostring is easy—it introduces a        tion, we describe individual components more concretely.
“-” if the number is negative. Note that the verifier must prove   We have primarily implemented what we call the translator,
that it will never call nattostring on a negative number as        djinnc, and the rest is off the shelf: Dafny verifies, Dafny’s
that is a precondition.                                            C# backend compiles, and the agent is an unmodified coding
func inttostring(i: int) -> s: string:                             assistant.
 s = (if i >= 0 then nattostring(i) else "-" + nattostring(-i))
                                                                   6.1   Translator
5.3   string to int, as a preimage
                                                                   Our translator has two modes. The first parses a specifica-
By using the relational properties of inttostring, we can          tion and writes two files: spec.dfy, the trusted lowering,
directly define stringtoint:                                       which holds a precondition predicate and a relation for ev-
func stringtoint(s: string) -> r: Result<int>:                     ery declaration and, for every proc, the datatypes and step
  if s in range(inttostring):
                                                                   relation of its compiled machine; and solution.dfy, the
    r.ok()
    inttostring(r.value) = s    # r.value is a preimage of s       obligations, each an empty-bodied lemma or function stub.
  else:                                                            It then runs Dafny on spec.dfy alone, which is how a Djinn-
    r = Failure                                                    lang program is type-checked — the language has no checker
   Note that this function is very strict! It only accepts in-     of its own. Since solution.dfy holds work that is costly to
tegers exactly as inttostring would generate them. If we           reproduce, it is written only when absent, or when forced.
wanted to accept whitespace, we could use the same pattern,            This output is meant to be given to an LLM. Once the LLM
but use the preimage of a relation which maps every integer        is done, we call the second mode. verify first retranslates
to multiple possible string representations.                       the specification, so that a stale or tampered spec.dfy can
   Here is a start (only implementing leading whitespace):         never be what the solution is checked against. It then scans
rel nattomanystrings(i: int) -> s: string                          the solution for escape hatches — the substrings assume,
requires i >= 0                                                    {:axiom}, {:extern}, and {:verify — and checks that ev-
total:                                                             ery regenerated obligation appears in the solution verbatim:
  # w is the number of leading whitespace bytes
                                                                   the comment, the signature, and the contract, everything
  0 <= w < |s|
  for k in 0..w:                                                   except the body between the braces. If all of that passes, it
    s[k] = ' ' || s[k] = '\n' || s[k] = '\t'                       invokes Dafny, with a 120-second per-obligation limit.

  |s| = w + (if i = 0 then 1 else log(10, i) + 1)                  6.2   Harness
  for k in 0..|s|-w:
                                                                   Our approach is harness-agnostic. For this experiment, we
    s[|s|-1-k] = ('0' as int + i/pow(10,k) % 10) as char
    s[|s|-1-k] >= '0'                                              use standard coding agents such as Claude Code and Codex.
    s[|s|-1-k] <= '9'                                              We point them at the output directory which includes: the
  Now we can define:                                               specification and its ambient Dafny, the stub file, and a writ-
func stringtonat(s: string) -> r: Result<int>:                     ten guide explaining what each obligation kind means, how
  if s in range(nattomanystrings):                                 the verifier judges, and which Dafny proof tactics tend to
    r.ok()                                                         work on these goals. The agent’s loop is the obvious one —
    nattomanystrings(r.value) = s                                  edit, run djinnc verify, read the errors, repeat — and it
  else:
                                                                   terminates when its implementation passes.
    r = Failure
                                                                      Using an off-the-shelf agent makes this project econom-
   and stringtonat(" 12") will work. Suppose we now                ically feasible. Since we use Claude Code and Codex and
retire nattostring, keeping nattomanystrings as the                not API models directly, we can put our LLM usage on the
single source of truth for digit rendering, and rewrite            flatrate subscriptions offered by major AI companies and do
inttostring on top of it. Since nattomanystrings is a              not pay per call.
relation, inttostring must either become one itself or
resolve the ambiguity. Let us resolve it:                          6.3   Support tooling
func inttostring(i: int) -> s: string:
                                                                   We were pleasantly surprised to see that our agents have
  if i >= 0:
    s = nattomanystrings(i)                                        developed some support tooling for themselves that is not
    s[0] >= '0' # resolve ambiguity! no leading                    part of the trusted base. A whole program at once is more
    s[0] <= '9' # whitespace in the string                         than an agent’s context comfortably holds, so they partition
  else:                                                            the declarations into disjoint groups and give each group to
    s = "-" + nattomanystrings(-i)
    s[1] >= '0' && s[1] <= '9'



Preprint.
Djinnlang: Higher-Level Programming by Unambiguous Specification with an LLM in the Compiler


its own agent working on its own copy of the solution. A                     All of it worked the first time. Both implementers dis-
merge tool then reassembles one solution from the copies.                 charged all 256 obligations of all three specifications, and
                                                                          the compiler’s 2,106 obligations (Section 6.5) came out of a
6.4   Hillclimbing performance                                            single run as well. Of course, within a run the agent natu-
Semantics is settled by the specification, but speed is not,              rally iterates against the verifier, as a human proof engineer
so performance is a second, separate pass. Once we have a                 would.
passing solution, we can ask an agent in a second prompt
to make it faster under the same obligations. In this round,              7.1   Benchmark programs
we only accept the agent’s changes if the proofs still pass               The three programs were chosen so that they can be some-
verification and the solution is actually faster across the               what elegantly specified, have CPU-bound workflows, and
workloads.                                                                the same specification admits both an obvious slow imple-
                                                                          mentation and a much faster one.
6.5   Bootstrapping                                                          Sudoku (70 lines of Djinnlang, 61 obligations) specifies the
djinnc is itself written in Djinnlang (with some pieces of                lexicographically least completion of a partially filled grid,
Dafny and C# for the environment) and bootstrapped.                       or a proof that none exists. Completions are a relation, since
   To bootstrap, we start out with the specification in Djinn-            a puzzle may have none or many; minimality is pinned down
lang. To get obligations out of it at all, we had an LLM write            without quantifying over grids by requiring that for every
a throwaway seed translator in Python (whose output we                    empty cell and every smaller digit, the puzzle that keeps the
checked manually). A second LLM filled the implementation                 answer’s prefix and places that digit has no completion at
and proof bodies the seed emitted, and the binary built from              all.
those bodies then regenerates its own obligations byte-for-                  LZ77 (81 lines, 63 obligations) specifies compression with
byte and re-runs the entire proof through its own verify                  optimal parsing. A decode relation fixes the format, and the
command — retiring the seed as a translator and as a verifier             minimum token count is given as a recurrence over the finite
respectively.                                                             menu of tokens usable at a position, which states “shortest
   djinnc is 4,088 lines of Djinnlang in 487 declarations, from           among all encodings” without naming an encoding. Note
which it emits 2,106 proof obligations; discharging them                  that the compression ratio is therefore a property of the
took 4,715 lines of implementation and 31,823 lines of proof,             specification: implementations may differ only in speed.
together with 1,549 helper declarations. The implementation                  Imp VM (166 lines, 132 obligations) specifies the small-step
of procedures makes up a fair amount of the specification,                semantics of a small imperative language with unbounded
as do error messages. We did not optimize the compiler                    integers, heap-allocated arrays, loops, and recursive proce-
specification for brevity, but instead have repeated ourselves            dures, run under a fuel bound so that the interpreter is total.
many times. Producing the implementation cost GPT 6 Astra                 An implementation may walk the syntax tree or compile to
1.4 billion tokens (an estimated $1,950 if used via the API, but          a register machine, provided it stops at exactly the same step
we ran this entirely through the flatrate subscription) over              count when the fuel runs out.
multiple days. While we were still drafting the specification,               The specifications were themselves LLM-generated, but
the compiler found four distinct bugs in it — in each case an             we checked them carefully.
obligation that could not be discharged because the draft was                Correctness was checked independently of the proofs by
genuinely wrong, not merely hard. Once the specification                  an LLM-generated black-box test suite — 14, 30, and 65 cases
was corrected, synthesis of the whole compiler succeeded                  respectively, with expected outputs produced by reference
on the first attempt. In the following section, we show more              implementations written in Python and C — together with
examples and analyze performance more deeply.                             nine long-running tasks per suite used for time measure-
                                                                          ments.
7     Empirical Evaluation
Given our implementation and language definition, we now                  7.2   Cost and specification/code/proof size
ask: are LLMs actually good enough to do what we ask of                   Implementing and proving the three programs cost roughly
them, and how long does it take them? We fixed three speci-               $360 with Claude Fable 5.1, distributed very unevenly (Ta-
fications and had two different implementers compile them:                ble 3): LZ77 alone accounts for two thirds of it, most of it
Claude Fable 5.1 driven by Claude Code, and GPT 6 Astra                   being its optimality argument. A further $666 went on opti-
driven by Codex. Neither was allowed to change a specifica-               mization, most of which was for the virtual machine.
tion. Each was asked to produce a verified implementation,                   The two implementers show very different characteristics.
snapshot it, and then perform a single round of optimization,             Codex compiled all three programs in 33 minutes of elapsed
so that every specification yields four artifacts, two for each           time for an estimated $47, against 21 hours and $1026 for
implementer.                                                              Claude Code — it is roughly thirty times faster and twenty
                                                                          times cheaper.


                                                                                                                               Preprint.
                                                                                                          Henniger, Chong and Amin


Table 1. Content lines (non-blank, non-comment) per                do not specify performance, so it is up to the LLM, and we
artifact. The spec column is the Djinnlang specification (the      imagine an optimizer mode that hillclimbs on performance.
only text a human writes/reviews) and is identical for both           Table 2 reports the speed of our three example programs.
implementers.                                                      Again, we find that the two implementers’ verified programs
                                                                   differ by a lot. On the hardest Sudoku workload, Claude’s
                               Claude Fable 5.1   GPT 6 Astra      optimized solver takes 0.13 s and Codex’s takes 47.8 s; on
                                                                   4 MB of text our encoder takes 0.63 s and theirs 25.6 s. The
 Program    spec   Stage       code       proof   code    proof
                                                                   virtual machine is closer but still decisive: 18.5 s against
 Sudoku       70   baseline     303         929     76     348     189 s on a billion interpreter steps, which is 53 million versus
                   optimized    448        1274    197     468     5 million steps per second.
 LZ77         81   baseline     448        2339     72     206
                                                                      Each of the implementers was then given one optimization
                   optimized    545        2585    210     356
                                                                   round. Claude Code moved the virtual machine from 5 to
 Imp VM      166   baseline     257         655    187     395
                   optimized   1440        2564    359     514     13 to 53 million steps per second across the naive, fast, and
                                                                   optimized machines. Codex’s round improved heap-heavy
                                                                   programs substantially — matrix multiplication from 217
Table 2. Performance of the solutions. Fastest of repeated
                                                                   to 38 seconds, the sieve from a timeout to 62 — but barey
runs, in seconds, on identical inputs; three runs per cell for
                                                                   changed the others.
workloads under two minutes, two above. >900 is a timeout
                                                                      Much of this is an artifact of how ambitious the imple-
at the cap; † is a crash (stack overflow) after about 0.1 s. All
                                                                   menters were: Claude Code seemed to optimize much more
builds are Dafny release builds, tested on a MacBook Pro, M4
                                                                   for generated code speed, while Codex was faster, but pro-
Max, 128 GB memory, 16 cores, macOS 15.7.7. Dafny 4.11.0,
                                                                   duced slower code. It is unclear whether Codex would have
.NET SDK 9.0.109.
                                                                   caught up given the same time budget. This insight is still
                                                                   useful: Codex could be a debug mode of sorts with higher
                               Claude Fable 5.1   GPT 6 Astra      compile speeds.
 Program    Workload           base         opt   base      opt
                                                                   8   Related Work
 Sudoku     hard puzzles        0.65       0.13   >900    47.84
            3000 unique         0.40       0.31   >900     4.31       Specification languages. Djinnlang belongs to a long
 LZ77       4 MB text           0.91       0.63       †   25.63    tradition of model-based specification languages. Z [30],
            2 MB DNA            0.33       0.24       †   28.55    VDM [12], and B [1] pioneered the specification of software
            1 MB periodic       0.32       0.12       †    3.26    as mathematical predicates over abstract states; TLA+ [16]
 Imp VM     109 steps           76.9       18.5   211.7   189.3    specifies concurrent systems as temporal-logic formulas; and
            Ackermann(3,10)     27.7        6.5   787.6   714.5    Alloy [11] made lightweight relational specifications auto-
            sieve to 2 · 107    23.6        6.6   >900     61.7    matically analyzable. In all of these, a specification describes
                                                                   a system but is not, in general, executable: obtaining an im-
   We find that, to solve the same problem, Codex wrote            plementation requires manual coding, or manual machine-
far less proof, and wrote it in one pass. What that buys           checked refinement as in B. Unattended implementation of a
is visible in Section 7.3. The cheap compilation produced          spec is only enabled by the unambiguity constraint and tight
verified programs that are three to four hundred times slower,     integration with an LLM that we propose. More recent work
and two of its unoptimized programs cannot complete the            proposes tooling that helps humans develop better specifica-
workloads within reasonable timeouts.                              tions. Miyazono et al. set natural-language documentation
   Compared against a conventional compiler the numbers            beside its Lean formalization with a line-by-line mapping,
are absurd: no compiler takes six hours or costs $236 to trans-    colour-coding the passages that correspond or diverge, us-
late 81 lines. However, against conventional verification with     ing Signal’s X3DH as their case study [25]. Dodds argues
human-written proofs, the same numbers look small. This            that most systems have no coherent formal specification at
level of insight about our code at this speed and cost would       all, only partial and mutually contradictory ones, and that
have seemed impossible to attain even a few years ago —            writing specifications is itself a programming-like activity
and one might reasonably hope that continued development           in want of tools [7].
of LLMs and harnesses will make things even cheaper and               Contracts and verification-aware languages. Eiffel
faster very quickly.                                               made pre- and postconditions part of the program text and of
                                                                   the methodology (“design by contract”) [23], followed by JML
7.3   Performance
                                                                   for Java [18] and Spec# [4]. Verification-aware languages —
As we have explained above, the unambiguity constraint             Dafny [19], F* [32], and Verus [17] — statically verify the
only applies to inputs and how they relate to outputs. We          code against its contracts. In all of these the programmer



Preprint.
Djinnlang: Higher-Level Programming by Unambiguous Specification with an LLM in the Compiler


Table 3. Wall-clock time and cost. impl is implementation and proof to a first accepted solution, opt the single optimization
round. Wall clock is elapsed time for that stage; the three programs were compiled concurrently by both implementers. Output
tokens include reasoning. Costs are list prices for the respective model and are not directly comparable: our figure is dominated
by cache writes at the one-hour retention we used, a category the Codex logs do not record. For both, we used the subscriptions,
so we have not actually spent this cost. It is the theoretical API cost. Every row covers implementation and optimization only.

                                              Claude Fable 5.1 (Claude Code)             GPT 6 Astra (Codex)
                          Program     Stage   turns   output     wall     cost      turns      output   wall     cost
                          Sudoku      impl      315     213 k    1.8 h    $51          51      15.6 k   13 m    $4.31
                                      opt       154     177 k    1.7 h    $36          58      13.1 k    7m     $5.74
                          LZ77        impl      794     625 k    6.3 h   $236          80      31.3 k   23 m    $8.87
                                      opt       313     300 k    1.9 h    $84          71      19.8 k    8m    $10.19
                          Imp VM      impl      304     116 k    1.3 h    $73          28      12.6 k   13 m    $3.02
                                      opt       943     763 k   12.1 h   $546          61      19.8 k   13 m    $7.37
                          all three           2823     2.2 M             $1026        416       127 k          $46.89


writes both the specification and the implementation, and                 in the loop [5]; Clover checks code–spec–docstring consis-
nothing forces the specification to be complete. Djinnlang                tency [31]; AlphaVerus bootstraps verified Verus code with-
keeps the contract vocabulary (indeed it compiles to Dafny                out human labels [2]; and AutoVerus [34] and Baldur [9]
and reuses its types and verifier) but removes the human-                 generate proofs for existing code, as do LLM-based invariant
written implementation entirely, and its unambiguousness                  inference [13] and specification generation [21, 24]. Dafny-
proofs remove the option of a partial spec.                               Bench measures LLMs’ ability to complete Dafny verifica-
                                                                          tions at scale [20], and Formal Disco generates open-ended
   Synthesis from specifications. Deriving implementa-
                                                                          synthetic verified programs in Dafny, Verus, and Frama-C to
tions from specifications symbolically is a classic ambition
                                                                          train models for verification tasks [28]. This literature treats
and could thus be considered an instance of spec-driven de-
                                                                          the LLM as an assistant working on or alongside conven-
velopment [22]. The refinement calculus [26] treats specifi-
                                                                          tional programs. Djinnlang inverts the workflow: the human
cations and code as points in one ordering, refined by hand;
                                                                          never writes code, the LLM-plus-verifier pair is packaged
Fiat [6] mechanizes such derivations in Rocq; complete func-
                                                                          as a compiler, and — uniquely, to our knowledge — the un-
tional synthesis [14] compiles constraints over decidable
                                                                          ambiguity constraint guarantees the LLM has no semantic
theories directly to code; and Sketch [29] fills holes in par-
                                                                          leeway, so its output need never be read.
tial programs by combinatorial search. These systems are
predictable and sound but restricted — to decidable theo-                    Specification elicitation problem. A recent critical
ries, to finite search spaces, or to domains with hand-built              strand argues that neither proofs nor specifications survive
refinement libraries. The Verse calculus [3] meets the same               contact with LLMs unexamined. Von Hippel et al. argue
limit from the language side, leaving the evaluation strategy             that the bottleneck in secure program synthesis is the
that would solve its equations to future work (see Section 4).            specification itself, a human-computer interaction problem
Closest to our aims is relational compilation [27], which re-             that stronger models do not solve [8, 33]. Lahiri quantifies
casts extraction as proof search and derives fast low-level               it, symbolically testing whether a specification captures
code from annotated functional models, emitting a proof for               user intent at all [15]. Djinnlang does not fully resolve
every compilation. They automate only the descent from a                  this problem either; but narrows the trusted artifact to the
functional model to code, leaving that model’s agreement                  specification, and aims to make it easier to read and less
with an abstract specification to the programmer. Djinnlang               error-prone (see Section 5.2).
uses a similar core architecture, but uses LLMs for synthe-
sis. We thus trade symbolic search for an LLM’s generality                9      Limitations
while keeping the soundness: a candidate implementation                   The limitations of the approach fall into three groups: what
that does not provably meet the spec is rejected.                         a compilation costs, what the language cannot express, and
   LLMs for verified code and proofs. A fast-growing body                 how far the guarantee reaches.
of work polices LLM output with verifiers. VerMCTS guides                   Compilation cost and latency. Compilation expenses
tree search over Dafny and Rocq programs with a verifier                  are measured in hours and dollars rather than seconds. Im-
                                                                          plementing and proving the three programs of Section 7
                                                                          cost roughly $360 in model usage with Claude Fable 5.1,



                                                                                                                                Preprint.
                                                                                                          Henniger, Chong and Amin


the longest single program taking 6.3 hours; a further $666        generated. Relaxing unambiguity on relational parts of the
went on optimization. Compiling all three concurrently took        language could follow.
20.8 hours of elapsed time and $1026 in total (Table 3). Djinn-
                                                                      Interactive tooling. There should be good, pleasant-to-
lang especially suits artifacts written once and depended on
                                                                   use tooling for writing specifications. For instance this tool-
for a long time.
                                                                   ing could help a developer gain insights about a spec before
   Non-convergence. The worst outcome of a Djinnlang               the LLM implements it. A bounded checker over the low-
compilation is not a rejected implementation but no answer.        ered relation, in the spirit of Alloy’s analyzer [11], could
When the model neither finds a proof nor a counterexam-            try to find counterexamples while the user is typing (Sec-
ple, the programmer is handed only a timeout. The three            tion 9). The front end is symbolic and fast, so a language
explanations — the specification is unsatisfiable, the proof is    server can report lexing, layout, parsing, check errors, and
merely hard, the model is too weak — are indistinguishable         provide progress details on a background process that writes
from outside. We did not in fact encounter this outcome in         the proofs. Proofs and implementations can be cached and
any of the four programs we compiled.                              shared across runs.
  Concurrency. Djinnlang is not thread-safe, has no shared            Specifying performance and scaling characteristics.
mutable state, and no interleaving. Specifying concurrency         The LLM implementer currently owns all performance de-
needs temporal properties, as implemented in TLA+ [16],            cisions; the verifier checks only functional correctness. As
and reconciling those with unambiguity is an open problem.         noted, this is desirable — LLMs are good optimizers — but
                                                                   unacceptable for timing-sensitive code and a liability for
   Side-channel security. An implementation can be fully
                                                                   DoS-style worst cases. We plan simple syntax for asymptotic
verified and still leak a key through timing (Section 2).
                                                                   complexity bounds and baseline-performance constraints,
Constant-time execution is a performance detail that Djinn-
                                                                   checked either by verified resource analysis or, more prag-
lang hides by design.
                                                                   matically, by compiler-generated benchmark harnesses.
   Soundness bugs in the verification pipeline. A devel-
oper must trust the ambient Dafny supplying the datatypes          11    Conclusion
and helpers a spec is written against plus the external I/O        We presented the unambiguity constraint and LLM-in-the-
bindings, the unverified main glue, the pinned drivers, the        compiler paradigm, and showed their partical implemen-
translator, as well as Dafny, Boogie, and Z3.                      tation on Djinnlang, a high-level specification language in
                                                                   which the programmer writes only specifications and an
10    Future Work                                                  LLM handles implementation and proof.
An abstract goal of this work is to allow a programmer to             Because every function’s spec must be proven unambigu-
express their intent in a shorter, elegant, and less error-prone   ous, the LLM has no leeway on program semantics, the gen-
way, and we hope that our unambiguity constraint and LLM-          erated code never needs to be read, and it can be regenerated
in-the-compiler paradigm will allow for such advances in the       from the spec at any time. Under this constraint, the distinc-
future. Concretely, we suggest the following areas of further      tion between a specification language and a programming
study:                                                             language essentially disappears.
                                                                      We have shown that specs can be shorter and closer to
   A fine-grained effect system. Effects are currently a thin
                                                                   intent than the code they replace, and help catch errors.
layer meant for interoperability with the imperative world:
                                                                   Finally, we have shown that LLMs are able to do the required
a proc says which effects happen and in what order, but the
                                                                   proofs and implementation, albeit currently at high cost.
language cannot say much about them. Effects could be much
                                                                      More broadly, this work is evidence for an underexplored
more. We want constraints over the event trace, written in
                                                                   role for LLMs in language design. Used not as an autocom-
the same constraint language as everything else: for instance
                                                                   plete or unattended vibe-coder but as a compiler stage and
“every file this proc opens is eventually closed,”, “we print
                                                                   tightly constrained by a verifier, LLMs make abstractions vi-
a grid and thus never lines longer than 40 characters”, “no
                                                                   able that no symbolic compiler could support: programming
network traffic occurs after the credential is read,” We expect
                                                                   by unambiguous specification. This constraint both makes
this will make systems-style code much more elegant.
                                                                   this a compiler and acts as an AI control mechanism. It can
  Principled relaxations of unambiguity. Unambiguity               help us reach a world of programming in which humans say
should remain the default, but we might want some leeway:          what and machines decide how.
take the exact wording of an error message, or the choice
among different but equivalent library calls. As a first step,
this could be implemented on top of procedures, where it
would be easy to call into some function the LLM has freely



Preprint.
Djinnlang: Higher-Level Programming by Unambiguous Specification with an LLM in the Compiler


Acknowledgments                                                                [13] Adharsh Kamath, Aditya Senthilnathan, Saikat Chakraborty, Pantazis
                                                                                    Deligiannis, Shuvendu K. Lahiri, Akash Lal, Aseem Rastogi, Subhajit
We thank Will Byrd, Jake Ginesin, Gabriel Poesia, Max von                           Roy, and Rahul Sharma. Finding inductive loop invariants using large
Hippel, Paul Krogmeier, Cameron Wong, Raffi Sanna, Rhea                             language models. arXiv:2311.07948, 2023. URL https://arxiv.org/abs/
Karty, Yilun Du, Mahzarin Banaji, Samuel Leßmann, and                               2311.07948.
Trevor DePodesta for their feedback. This research was par-                    [14] Viktor Kuncak, Mikaël Mayer, Ruzica Piskac, and Philippe Suter. Com-
tially supported by a Coefficient Giving grant, funding and                         plete functional synthesis. In Proceedings of the 31st ACM SIGPLAN
                                                                                    Conference on Programming Language Design and Implementation
credits from an Amazon Research Award, and a Harvard
                                                                                    (PLDI), pages 316–329, 2010. doi: 10.1145/1806596.1806632.
Data Science Initiative grant. Simon Henniger was supported                    [15] Shuvendu K. Lahiri. Evaluating LLM-driven user-intent formalization
by the Harvard John A. Paulson School of Engineering and                            for verification-aware languages. In Proceedings of the 24th Conference
Applied Sciences (SEAS) Prize Fellowship and the German                             on Formal Methods in Computer-Aided Design (FMCAD), pages 142–147.
Academic Fellowship Organization, funded by the German                              TU Wien Academic Press, 2024. doi: 10.34727/2024/isbn.978-3-85448-
                                                                                    065-5_19. URL https://arxiv.org/abs/2406.09757.
Federal Ministry for Economic Affairs and Energy.
                                                                               [16] Leslie Lamport. Specifying Systems: The TLA+ Language and Tools
                                                                                    for Hardware and Software Engineers. Addison-Wesley, 2002. URL
References                                                                          https://lamport.azurewebsites.net/tla/book.html.
 [1] Jean-Raymond Abrial. The B-Book: Assigning Programs to Meanings.          [17] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha
     Cambridge University Press, 1996.                                              Subasinghe, Yi Zhou, Jon Howell, Bryan Parno, and Chris Hawblitzel.
 [2] Pranjal Aggarwal, Bryan Parno, and Sean Welleck. AlphaVerus: Boot-             Verus: Verifying Rust programs using linear ghost types. Proceedings
     strapping formally verified code generation through self-improving             of the ACM on Programming Languages, 7(OOPSLA1):286–315, 2023.
     translation and treefinement. In Proceedings of the 42nd International         doi: 10.1145/3586037.
     Conference on Machine Learning (ICML), 2025. URL https://arxiv.org/       [18] Gary T. Leavens, Albert L. Baker, and Clyde Ruby. Preliminary design
     abs/2412.06176.                                                                of JML: A behavioral interface specification language for Java. ACM
 [3] Lennart Augustsson, Joachim Breitner, Koen Claessen, Ranjit Jhala,             SIGSOFT Software Engineering Notes, 31(3):1–38, 2006. doi: 10.1145/
     Simon Peyton Jones, Olin Shivers, Guy L. Steele Jr., and Tim Sweeney.          1127878.1127884.
     The Verse calculus: A core calculus for deterministic functional logic    [19] K. Rustan M. Leino. Dafny: An automatic program verifier for func-
     programming. Proceedings of the ACM on Programming Languages, 7                tional correctness. In Logic for Programming, Artificial Intelligence, and
     (ICFP):417–447, 2023. doi: 10.1145/3607845.                                    Reasoning (LPAR-16), volume 6355 of LNCS, pages 348–370. Springer,
 [4] Mike Barnett, K. Rustan M. Leino, and Wolfram Schulte. The Spec#               2010. doi: 10.1007/978-3-642-17511-4_20.
     programming system: An overview. In Construction and Analysis of          [20] Chloe Loughridge, Qinyi Sun, Seth Ahrenbach, Federico Cassano,
     Safe, Secure, and Interoperable Smart Devices (CASSIS), volume 3362 of         Chuyue Sun, Ying Sheng, Anish Mudide, Md Rakib Hossain Misu,
     LNCS. Springer, 2004. doi: 10.1007/978-3-540-30569-9_3.                        Nada Amin, and Max Tegmark. DafnyBench: A benchmark for formal
 [5] David Brandfonbrener, Simon Henniger, Sibi Raja, Tarun Prasad,                 software verification. arXiv:2406.08467, 2024. URL https://arxiv.org/
     Chloe Loughridge, Federico Cassano, Sabrina Ruixin Hu, Jianang Yang,           abs/2406.08467.
     William E. Byrd, Robert Zinkov, and Nada Amin. VerMCTS: Synthe-           [21] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. Spec-
     sizing multi-step programs using a verifier, a large language model,           Gen: Automated generation of formal program specifications via
     and tree search. arXiv:2402.08147, 2024. URL https://arxiv.org/abs/            large language models. In Proceedings of the 47th IEEE/ACM In-
     2402.08147.                                                                    ternational Conference on Software Engineering (ICSE), 2025. doi:
 [6] Benjamin Delaware, Clément Pit-Claudel, Jason Gross, and Adam                  10.1109/ICSE55347.2025.00129. URL https://arxiv.org/abs/2401.08807.
     Chlipala. Fiat: Deductive synthesis of abstract data types in a proof     [22] Simon Martinelli. Spec-driven development. APress, Berlin, Germany,
     assistant. In Proceedings of the 42nd ACM SIGPLAN-SIGACT Sympo-                August 2026.
     sium on Principles of Programming Languages (POPL), pages 689–700,        [23] Bertrand Meyer. Applying “design by contract”. IEEE Computer, 25
     2015. doi: 10.1145/2676726.2677006.                                            (10):40–51, 1992. doi: 10.1109/2.161279.
 [7] Mike Dodds. Specifications don’t exist. Galois, Inc., June 2025. URL      [24] Md Rakib Hossain Misu, Cristina V. Lopes, Iris Ma, and James Noble.
     https://www.galois.com/articles/specifications-dont-exist.                     Towards AI-assisted synthesis of verified Dafny methods. Proceedings
 [8] Quinn Dougherty and Max von Hippel. Lies, damned lies, and proofs:             of the ACM on Software Engineering, 1(FSE):812–835, 2024. doi: 10.
     Formal methods are not slopless. LessWrong, January 2026. URL                  1145/3643763.
     https://www.lesswrong.com/posts/rhAPh3YzhPoBNpgHg/lies-                   [25] Evan Miyazono, Daniel Windham, and Alexandre Rademaker. An
     damned-lies-and-proofs-formal-methods-are-not-slopless.                        IDE for validating specifications. Atlas Computing, May 2025. URL
 [9] Emily First, Markus N. Rabe, Talia Ringer, and Yuriy Brun. Baldur:             https://blog.atlascomputing.org/p/ide-for-validating-specifications.
     Whole-proof generation and repair with large language models. In          [26] Carroll Morgan. Programming from Specifications. Prentice Hall, 2nd
     Proceedings of the 31st ACM Joint European Software Engineering Con-           edition, 1994. URL https://www.cs.ox.ac.uk/publications/books/PfS/.
     ference and Symposium on the Foundations of Software Engineering          [27] Clément Pit-Claudel, Jade Philipoom, Dustin Jamner, Andres Erbsen,
     (ESEC/FSE), pages 1229–1241, 2023. doi: 10.1145/3611643.3616243.               and Adam Chlipala. Relational compilation for performance-critical
[10] Ryan Greenblatt, Buck Shlegeris, Kshitij Sachan, and Fabien Roger. AI          applications: Extensible proof-producing translation of functional
     control: Improving safety despite intentional subversion. In Proceed-          models into low-level code. In Proceedings of the 43rd ACM SIGPLAN
     ings of the 41st International Conference on Machine Learning (ICML),          International Conference on Programming Language Design and Imple-
     volume 235 of Proceedings of Machine Learning Research, pages 16295–           mentation (PLDI), pages 918–933, 2022. doi: 10.1145/3519939.3523706.
     16336, 2024. URL https://arxiv.org/abs/2312.06942.                             URL https://adam.chlipala.net/papers/RupicolaPLDI22/RupicolaPLDI
[11] Daniel Jackson. Software Abstractions: Logic, Language, and Analysis.          22.pdf.
     MIT Press, revised edition, 2012. URL https://alloytools.org/book.html.   [28] Gabriel Poesia, Simon Henniger, Tzu-Han Hsu, Yilun Du, and Nada
[12] Cliff B. Jones. Systematic Software Development Using VDM. Prentice            Amin. Formal disco: Scalable open-ended generation of formally
     Hall, 2nd edition, 1990.                                                       verified programs. arXiv:2607.04631, 2026. URL https://arxiv.org/abs/




                                                                                                                                                 Preprint.
                                                                                                                           Henniger, Chong and Amin


     2607.04631.                                                                    and Santiago Zanella-Béguelin. Dependent types and multi-monadic
[29] Armando Solar-Lezama. Program Synthesis by Sketching. PhD thesis,              effects in F*. In Proceedings of the 43rd ACM SIGPLAN-SIGACT Sympo-
     University of California, Berkeley, 2008. URL https://people.csail.mit.        sium on Principles of Programming Languages (POPL), pages 256–270,
     edu/asolar/papers/thesis.pdf.                                                  2016. doi: 10.1145/2837614.2837655.
[30] J. Michael Spivey. The Z Notation: A Reference Manual. Prentice Hall,     [33] Max von Hippel, Simon Henniger, Evan Miyazono, and Quinn
     2nd edition, 1992. URL https://www.rose-hulman.edu/class/cs/cs415/             Dougherty. How to solve secure program synthesis. LessWrong,
     zrm.pdf.                                                                       March 2026. URL https://www.lesswrong.com/posts/8wtrLoDPyCfM
[31] Chuyue Sun, Ying Sheng, Oded Padon, and Clark Barrett. Clover:                 LuHkt/how-to-solve-secure-program-synthesis.
     Closed-loop verifiable code generation. In AI Verification (SAIV).        [34] Chenyuan Yang et al. AutoVerus: Automated proof generation for Rust
     Springer, 2024. URL https://arxiv.org/abs/2310.17807.                          code. Proceedings of the ACM on Programming Languages, 9(OOPSLA),
[32] Nikhil Swamy, Cătălin Hriţcu, Chantal Keller, Aseem Rastogi, Antoine           2025. doi: 10.1145/3763174. URL https://arxiv.org/abs/2409.13082.
     Delignat-Lavaud, Simon Forest, Karthikeyan Bhargavan, Cédric Four-
     net, Pierre-Yves Strub, Markulf Kohlweiss, Jean-Karim Zinzindohoué,




Preprint.
