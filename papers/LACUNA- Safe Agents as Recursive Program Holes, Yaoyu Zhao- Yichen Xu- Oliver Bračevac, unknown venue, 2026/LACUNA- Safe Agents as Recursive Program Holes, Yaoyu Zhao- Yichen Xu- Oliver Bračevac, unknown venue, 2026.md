                                                             L ACUNA: Safe Agents as Recursive Program Holes

                                                                 Yaoyu Zhao*   Yichen Xu*    Oliver Bračevac
                                                          Cao Nguyen Pham    Frank Zhengqing Wu     Martin Odersky

                                                                                     EPFL, Lausanne, Switzerland
                                                                                {yaoyu.zhao, yichen.xu, oliver.bracevac,
                                                                         nguyen.pham, zhengqing.wu, martin.odersky}@epfl.ch



                                                                     Abstract                          2024) and packaged as reusable skills (Anthropic,
                                                                                                       2025c). The dominant approach, ReAct (Yao et al.,
                                              LLM agents increasingly act by writing code,
arXiv:2605.28617v1 [cs.AI] 27 May 2026




                                              yet a split persists between the runtime that
                                                                                                       2023), has the model alternate between reasoning
                                              drives the agent and the code the model writes.          and individual tool calls until reaching an answer.
                                              The runtime owns the loop, context, and con-             Code-as-action agents (Wang et al., 2024b; An-
                                              trol flow, and the model has little say over any         thropic, 2025b; Roucher et al., 2025) offer an alter-
                                              of them. Letting model-written code shape the            native: instead of emitting one tool call at a time,
                                              runtime itself would make agents more expres-            the model writes code that composes tools, parses
                                              sive, but it would also sharpen safety problems.         intermediate results, branches, and loops.
                                              A model can be diverted by a prompt injec-
                                                                                                          Existing code-as-action agents keep a clear split
                                              tion, call the wrong tool, or fail partway and
                                              leave an inconsistent state, and each such fail-         between the code that runs the agent and the code
                                              ure reaches further when the code shapes the             it writes. The runtime owns the loop, context, and
                                              runtime than when it expresses a single action.          action dispatch, while the model supplies only the
                                              We present L ACUNA, a programming model                  next fragment, with little say over what context to
                                              for agents that closes this split while preserv-         keep, when to spawn sub-agents, or how to adapt
                                              ing safety. Each agent action is a typed call            control flow. Recursive language modeling (Zhang
                                              agent[T](task) that the LLM fills with code
                                                                                                       et al., 2025a) lets generated code update a persis-
                                              when execution reaches it, and the code is type-
                                              checked against the surrounding program be-
                                                                                                       tent execution context and call the model again,
                                              fore it runs. Because each action is accepted or         but the runtime still owns the loop and call struc-
                                              rejected as a whole, a rejected one leaves the en-       ture. Letting the code the model writes shape the
                                              vironment untouched, and its compiler diagnos-           runtime itself lifts these limits and makes agents
                                              tics drive a retry. The same check also bounds           more expressive, but it also raises the stakes for
                                              which tools and data an action may use and how           safety. Model-written code is untrusted. When it
                                              they flow. Our primitive expresses ReAct loops,          only expresses actions, the surrounding runtime
                                              sub-agents, skills, parallel decomposition, and
                                                                                                       bounds its reach; once the agent shapes its own
                                              multi-model planning as ordinary control flow.
                                              We evaluate L ACUNA on a collection of test              runtime, an attack reaches the runtime itself. Ex-
                                              cases, BrowseComp-Plus, and τ 2 -bench. On               isting defenses are piecemeal. Sandboxes and re-
                                              BrowseComp-Plus, 8.6% of generations are re-             stricted interpreters (Pydantic, 2025) limit what
                                              jected before execution, with 0.7 retries per            code can do at runtime, policy languages (Ama-
                                              query on average, and the agent reaches 27.1%            zon Web Services, 2024) gate access to resources,
                                              accuracy. On τ 2 -bench, L ACUNA solves 76.0%            and input-hardening and mediation defenses (Chen
                                              of 392 tasks across four domains with a capable          et al., 2025a; Willison, 2023) try to block unsafe
                                              model, on par with the baseline agent.
                                                                                                       actions. None of them checks a whole generated
                                         1    Introduction                                             action before it starts.
                                                                                                          We propose L ACUNA, a programming model
                                         Large language models (LLMs) increasingly drive               that closes this split while preserving safety. Each
                                         agents: programs that call models, use tools, and             agent action is a typed hole that the LLM fills with
                                         maintain state to solve tasks. Tools such as file             code when execution reaches it, and the code is
                                         access, web search, and API calls are now often de-           type-checked against the surrounding program be-
                                         scribed through protocols such as MCP (Anthropic,             fore it runs. The core idea is to put the model call
                                             * Equal contribution.                                     inside the program at the point where its result

                                                                                                   1
is needed, and to make the caller state what kind                   site before execution (Section 3).
of result is expected. Our prototype uses Scala 3
                                                                 2. A safety analysis of the resulting guaran-
because it supports the two foundations we need:
                                                                    tees: pre-execution rejection of unavailable
compiling a fresh snippet in the surrounding pro-
                                                                    names and type mismatches, no partial execu-
gram context, and tracking which resources that
                                                                    tion of rejected snippets, and permissions and
snippet is allowed to use (Scala, 2024a). The user-
                                                                    information-flow control (Section 4).
facing call is:
 def agent[T](task: String): T                                   3. A demonstration that nested agent calls and
Here task is the natural-language prompt and T is                   ordinary code express common agent pat-
the expected result type. When execution reaches                    terns, including ReAct loops, skills, and multi-
this call, the model writes Scala code for the re-                  model planning, as ordinary program control
quest, which L ACUNA compiles at the same point                     flow (Section 5).
in the surrounding program, so it can use the vari-              4. A Scala 3 realization and an evaluation on a
ables, functions, and tools available there. If the                 collection of verifier test cases, BrowseComp-
code provably produces a value of type T, it runs;                  Plus (Chen et al., 2025b), and τ 2 -bench (Bar-
otherwise the compiler’s errors are sent back as                    res et al., 2025), including the retry behavior
feedback for a retry.                                               induced by compiler diagnostics (Section 6,
   The generated code is ordinary Scala, not just a                 Section 7).
single tool call. It can use tools, process data, and
ask the model for help again, as in this request for         2     Related Work
a report over several topics:
                                                             Code-as-action approaches (Wang et al., 2024b;
 val topics = List(
   "LLM", "world models", "transformer", ...)                Anthropic, 2025b; Roucher et al., 2025) let the
 val report =                       typed action
                                                             model write code as its action space rather than
   agent[String](                                            emit a single tool call. Recursive language models
     "Research each topic and generate a" +
     " report on their connections.")                        (RLM) (Zhang et al., 2025a), introduced above, are
                                                             the closest prior design to ours, and we improve on
One valid expansion uses nested research calls:              it in two ways. First, RLM’s REPL (a read-eval-
 val report: String =              recursive expansion       print loop, the interactive shell that retains state
   val findings =
     topics.par.map(topic =>                                 across inputs) runs generated code without check-
       agent[String](s"Research: $topic"))                   ing it first, so a snippet that misuses a binding or
   agent("Generate a report from the findings")              returns the wrong shape can fail partway through
Each nested call is checked like the outer one, with         and leave the environment inconsistent, whereas
its own result type and access to the variables intro-       L ACUNA typechecks against T in the live lexical
duced by the code around it. Recursive model calls           scope before any of it runs. Second, RLM hands
are not a separate agent protocol: they are ordinary         the model a handle to the context but keeps orches-
code that can branch, loop, spawn sub-agents, call           tration and control flow in the runtime, whereas
skills, or route work across models.                         in L ACUNA the generated code writes that control
   The check catches structural failures before ex-          flow itself, as typed code over the agent primitive.
ecution: a snippet that uses a missing tool, passes             Other language-integrated LLM frameworks
arguments of the wrong shape, or returns the wrong           make model calls first-class in a host language,
kind of result is rejected as a whole, and the retry         but they focus on the model’s input and output
starts from an unchanged state (Section 4). The              rules. LMQL (Beurer-Kellner et al., 2023) casts
check also bounds the agent’s authority (Scala,              LLM inference as a query whose holes are filled by
2024a; Odersky et al., 2026; Xu et al., 2025):               constrained decoding, where declared constraints
whether it can access certain files, network han-            on the type, length, or form of the result steer the
dles, and tools (Section 4.3).                               sampler. DSPy (Khattab et al., 2024) describes an
   Our contributions are:                                    LLM call with a typed signature that the framework
                                                             renders into a prompt and parses back into values.
  1. A code-as-action model in which an LLM                  In both, the declaration governs only a single call’s
     writes agent actions as code that runs as part          input and output. Composing several such calls
     of its own runtime and is checked at the call           into a larger workflow is left to the developer, who

                                                         2
wires them together by hand in fixed code, such as            succeeds, the snippet runs and the call evaluates to
an LMQL query or a DSPy pipeline.                             a value of type T. If it fails, the agent receives the
   L ACUNA differs on both counts. The agent emits            diagnostics as feedback and can try again.
a program rather than a constrained string or a set              The static type itself does not constitute our en-
of field values, and the host compiler typechecks             tire contribution, since any typed language provides
that program against T in the call site’s lexical scope       one. What matters is when and against what it is
before it runs. We neither constrain the sampler nor          enforced. A compiler for a statically typed lan-
parse the output. Instead, the compiler’s error mes-          guage normally checks only source the developer
sages are fed back to drive retries until the model           wrote, ahead of time, and gives no way to run a
produces a well-typed snippet. Composition is then            string against the contract of the surrounding code
expressed by the generated code itself, as control            while the program executes. L ACUNA provides that
flow over the agent primitive. And because the                guarantee for model-written code: the snippet does
snippet is real code of the host language, capture            not exist until runtime, yet it is checked against
checking bounds the capabilities it may use, a guar-          T and the live lexical scope at the call site under
antee neither output-shaping framework provides.              the same static rules as hand-written code, before
   The closest work in framing is ChatLSP (Blinn              any of it runs. The generated action thus inherits
et al., 2024), which likewise fills a typed hole with         the full strength of static checking from the host
LLM-generated code from its expected type and                 language (Section 4), rather than a weaker runtime
context. Its setting, though, is edit-time code com-          approximation.
pletion that a human reviews, where context mainly               Concretely, the prompt sent to the LLM is assem-
reduces hallucination. L ACUNA instead makes                  bled from a small template: a system instruction
the hole a recursive runtime action, typechecked              telling the model to return a Scala expression, the
against the live lexical scope and run in one process.        expected type T rendered back to source, the enclos-
That shift adds guarantees that completion does not           ing source with a placeholder at the agent call’s
need: a dynamic dependency on the live context,               position, a listing of the variables and parameters
capture-checked authority over effects and data,              available at the call site and their types, and the
and recursive use of the hole as the unit of dynamic          user’s task string. The system instruction also car-
control flow rather than a one-shot completion.               ries setup-specific guidance, for instance how to
                                                              interact with the user, how to request additional
3     L ACUNA: Typed Holes as Agents                          permissions or capabilities, and how to organize a
3.1     The Agent Call                                        multi-step task into smaller agent calls. The tem-
                                                              plate is configurable per call site or per session.
L ACUNA treats an agent request as a placeholder
                                                              Callers can swap the system instruction, change
in code: the surrounding program needs a value
                                                              how available names are summarized, or attach
whose type is fixed statically, and the model writes
                                                              project-specific context for types the model would
the code that should produce it. Programming tools
                                                              not otherwise know.
often call such a placeholder a typed hole (Omar
et al., 2017). We reuse the idea for model-written            What the model may write. The generated code
actions at runtime:                                           is typically a single expression or a block with mul-
    def agent[T](task: String): T                             tiple statements. It may read parameters, read and
                                                              update local variables, use control flow (if-else,
The type parameter T is the expected result type,
                                                              while, for, match, try-catch), call any function or
and the value parameter task is a natural-language
                                                              method visible at the call site, including a nested
prompt describing what should go there. In prac-
                                                              agent(...), or define its own local functions, lamb-
tice, T rarely needs to be written out. Scala’s type
                                                              das, or classes. The only requirements are the ones
inference picks it up from the surrounding context ,
                                                              the compiler always enforces for hand-written code:
so callers usually write agent(...) and let the com-
                                                              the final expression must have type T, every name
piler fill in the type. At runtime, the LLM receives
                                                              it uses must be in scope at that point, and the snip-
the prompt together with the expected type and
                                                              pet must pass every other check the host compiler
the enclosing source at the call site, and returns a
                                                              applies.
string of Scala source intended to produce a T. The
compiler checks that source statically against T, as          Tools are functions. A tool is simply a function
if it had been written at the call site. If the check         in scope. The model invokes it by writing a func-

                                                          3
tion call that the compiler type-checks, with no             the work down, processed the relevant data, and
tool registry, JSON schema, or protocol layer to             recorded its reasoning in the program text. Nested
maintain, and defining a tool is just defining a func-       agent calls thus give an agent a natural way to
tion (see Appendix C). The idea extends to every             break a complex task into smaller ones, sequential
interaction with the user and the environment, so            or parallel, each reasoned about with richer context
showing progress is a plain println(...) and any             and a more precise goal than the step before. Sec-
I/O is the corresponding standard-library call, with         tion 5 shows that this is enough to express common
no separate agent layer to mediate it.                       agent architectures.
                                                                Nested calls carry the usual termination caveat.
3.2   Examples                                               An LLM is free to emit a snippet that calls agent
The generated code is compiled as if the developer           again, and the new call may emit another, with no
had typed it at the exact point where the agent call         static bound on the depth. A genuinely complex
appears. The snippet can therefore use the same              task and an accidental infinite recursion can look
variables, functions, parameters, and imports as             the same from the outside. The runtime therefore
hand-written code at that point.                             tracks the current depth of nested agent calls and
 > val xs = List(0, 1, 2, 4, 7, 9, 10)                       exposes a configurable cap. When the cap is hit,
 > val r = agent[List[Int]](                                 the offending call fails with an exception. Callers
 | "filter the prime numbers from xs")
 // LLM produces:
                                                             who want a hard ceiling on cost or latency set the
 //   def isPrime(n: Int): Boolean =                         cap themselves, and who prefer to trust the LLM
 //     n > 1 &&                                             can leave it open and let the agent stop when it
 //       (2 until n).forall(n %
 //   xs.filter(isPrime)                                     judges the task complete.
 val r: List[Int] = List(2, 7)
                                                             3.4   Handling Compilation Errors
The generated code uses xs directly and defines a
local helper isPrime. Because the snippet is com-            Each agent call runs a self-correcting retry loop.
piled at the call site, the name xs refers to the list       The generated code is sent through the compiler. If
the surrounding program defined, and the value is            the check fails, the diagnostics are appended to the
passed to the snippet at runtime. The expected type          original prompt and the LLM is asked again, up
List[Int] constrains the generation to produce a             to a configurable maximum number of retries. If
list of integers, so the LLM cannot return a string,         the agent still cannot produce an accepted snippet
an integer, or a boolean. The richer the result type,        within that budget, the call throws a special excep-
the tighter the contract: Appendix A shows alge-             tion carrying the final compiler diagnostics. This
braic data types and function types constraining the         is the appropriate failure when the prompt requests
generated code further.                                      something the surrounding program context can-
                                                             not express, for instance asking for a network call
3.3   Nested Agent Calls                                     when no I/O capability is in scope, or asking for a
                                                             return shape the type system rules out.
Nested calls are the central mechanism of L ACUNA.
The top-level call agent[T](task) asks the model for            The outer program can catch this exception like
code that solves the task, and that code may make            any other:
smaller agent[U](subtask) calls. Each nested call             try
                                                                val x: Int = agent("...")
has its own expected type U and its own task string,            ...
and is checked and executed by the same agent                 catch
                                                                case e: EvalCompileException =>
mechanism.                                                        fallback()
   Crucially, a nested call sees more than its parent
did. When the runtime reaches a nested agent call,           The trade-off is that a try block placed around an
the LLM is asked to fill it within a richer context.         outer agent call also catches compile failures from
That context includes not only the names avail-              any nested agent call inside its snippet, even when
able at the outer call site, but also every intermedi-       those failures are unrelated to the outer call’s intent.
ate value, comment, and control-flow structure the              L ACUNA also provides agentSafe[T], which,
outer snippet has introduced up to that point. Each          rather than throwing on failure, returns its outcome
sub-problem is therefore approached with more in-            as a value of type EvalResult[T] holding either the
formation. The outer call has already narrowed               result value of type T or the final diagnostics. A

                                                         4
caller can therefore handle a failed generation lo-           one.
cally instead of catching an exception that a nested
call might throw (the full signature of agentSafe is          4.2    Static Guarantees
in Section 6).                                                Undefined names. The snippet may use only
                                                              names the lexical scope already provides. A refer-
4     Safety                                                  ence to a binding the surrounding program lacks is
                                                              caught before the snippet runs:
Each agent call is compiled by the host compiler in            > val tax: Double = 0.08
the original lexical context, so a generated snippet           > agent[Double]("apply tax to price")
is held to exactly the rules the compiler applies to           // model produces: price * (1.0 + tax)
                                                               EvalCompileException:
code written by hand at that point. The snippet runs             agent failed to compile:
only if it resolves every name in scope, typechecks              Not found: value price
against the expected T, and passes every other check
the compiler enforces. These checks range from                Type mismatches. A value of the wrong type
exhaustiveness and nullability to, when capture               cannot flow into a function call or an algebraic
checking is enabled, effect and information-flow              constructor, even if the surface text looks plausible:
constraints. No separate safety pass of our own                > case class Order(id: Int, total: Double)
is involved: the guarantee is the host compiler’s              > val first: String = "A001"
                                                               > agent[Order]("id from first, total 0.0")
soundness, applied to model-written code. We first             // model produces: Order(first, 0.0)
fix the threat model, then walk through representa-            EvalCompileException:
tive rejections, ending with the constraints capture             agent failed to compile:
                                                                 Order(first, 0.0)
checking adds. The fully adversarial setting is de-                    ^^^^^
veloped in Section 4.3.                                          Found:    String
                                                                 Required: Int
   In the examples below, the generated snippet
appears as a comment and the compiler’s diagnostic               The same checks turn away other common short-
is what the runtime reports to the LLM and caller.            cuts. Appendix B shows a null literal rejected
We set the retry budget to zero so the first failure          under explicit nulls (Scala, 2024b) and a non-
surfaces directly (Section 3.4).                              exhaustive pattern match over a sealed data type
                                                              rejected by the exhaustiveness checker.
4.1    Threat Model
                                                              Atomicity: nothing runs if anything fails. The
We make the trust boundary explicit. The trusted
                                                              critical property is that the snippet is accepted or
components are the compiler (type checker, static
                                                              rejected as a whole. A side-effecting statement
analysis, and code generation), the runtime that exe-
                                                              earlier in the snippet does not run when a later
cutes a type-checked snippet, and the host program
                                                              statement fails to typecheck. Consider an agent
that issues the agent call and supplies its lexical
                                                              asked to update a mutable balance:
scope. The untrusted components are the model
                                                               > var balance: Int = 100
that fills the hole (treated as potentially byzantine),        > agent[Int](
every snippet it produces, and any external con-               | "subtract 50 and return the new balance")
                                                               // model produces:
tent (files, third-party APIs, web pages, and tool             //    balance -= 50
outputs) that reaches the task string.                         //    s"remaining: $balance" // String, not Int
   The threat we address here is model error: even             EvalCompileException:
                                                                  agent failed to compile:
an honest, well-intentioned model is an unreliable                Found:    String
programmer and may emit code that is incorrect                    Required: Int
or oversteps its bounds, e.g., performing I/O or               > balance
                                                               val res: Int = 100
reaching a resource the surrounding program could
not reach. We want every generated snippet to be              The assignment to balance precedes the ill-typed
as safe as code a developer could have written by             expression in source order, yet never executes: the
hand at that point, irrespective of the model’s com-          snippet is rejected as a whole, so the runtime never
petence, so that a plain mistake never becomes an             runs its first statement. Approaches that detect ill-
action outside the snippet’s static contract. These           typed code only at runtime (a Python exec string, an
guarantees hold against any model, honest or not,             unconstrained tool call) leak partial effects through
and Section 4.3 extends them to a fully adversarial           exactly this pattern: the assignment fires before

                                                          5
the bad statement raises, leaving state inconsistent.       is in scope can read, while one generated with-
The typed hole is all-or-nothing by construction.           out a network capability cannot send what it read,
                                                            whatever a poisoned instruction demands. The two
4.3   Capability Safety                                     results below make this precise: confinement by
The standard type system of Section 4.2 governs an          scope bounds which effects a snippet may perform,
action’s shape but says nothing about its authority:        and information-flow control bounds which data it
which effects the generated code may perform and            may carry out.
which data it may use. Turning on Scala 3’s cap-
ture checking adds that layer as an opt-in, without         Confinement by scope. Capture checking con-
changing the primitive, building on the capture-set         fines a capability to the region of code where it is
notation of Appendix D. A capability, in the object-        lexically in scope. A generated snippet can reach a
capability sense used throughout this paper (Dennis         capability only if the hole’s context already binds
and Horn, 1966; Miller, 2006), is an ordinary un-           it, and even then it cannot smuggle that capability
forgeable program value that authorizes a specific          out: a result whose type does not admit the capa-
effect or resource (a file handle, a network socket,        bility cannot carry it past the scope. The snippet
a logger): code can perform the effect only while it        may therefore invoke an in-scope capability while
holds a reference to the corresponding value. This          it runs, but it may not hand back a value that retains
differs from the systems notion of capabilities as          the capability for later use. An io capability makes
process-level privilege bits. Here, granting and            the contrast concrete:
propagation are lexical and type-tracked rather than         > trait IO extends caps.SharedCapability
ambient. The lexical scope at the hole is therefore          > def withIO[T](op: IO^ => T): T =
the agent’s permission set, and the same compiler            | op(new IO {})
                                                             > def readFile(
enforces capability scoping and information-flow             | io: IO, path: String): String = ...
constraints on both the generated code and the rest
                                                             // direct use: the result is a plain String
of the program.
                                                             > withIO[String] { io =>
                                                             | agent("read /etc/hosts using io")
Extended threat model. The threat model of                   | }
Section 4.1 assumes an honest but fallible model.            // model produces: readFile(io, "/etc/hosts")
Tracked capabilities let us widen it to an adversar-         val res0: String = ...
ial model that deliberately emits harmful code, the          // storing io for later leaks it past the block
setting of prompt injection. An injection is direct          > withIO[String => String] { io =>
when it rides in on a hostile user prompt and in-            | agent("return a file reader using io")
                                                             | }
direct when it arrives in content the agent reads            // model produces:
at runtime (a tool result, a file, or a fetched web          //   (p: String) => readFile(io, p)
page) that flows into the task string. We do not try         EvalCompileException:
                                                             Type Mismatch Error:
to stop the model from being influenced by such              Capability io outlives its scope: it leaks into
content, which is unavoidable once untrusted text            outer capture set s1 owned by value res2.
                                                             The leakage occurred when trying to match the
reaches the prompt. We only bound what that in-              following types:
fluence can do. The snippet is still recompiled in           Found:    String ->{io} String
the hole’s lexical scope, so a subverted model can           Required: String ->s1 String
invoke only the effects and reach only the data that
                                                            The first call uses io directly and returns a plain
scope already grants, exactly as an honest model
                                                            String, which carries no capability, so it is ac-
can.
                                                            cepted. The second call asks for a function that
Tool use as permission. Because the scope is the            reads a file. The generated lambda has type
permission set, tool use is governed by the same            String ->{io} String because it captures the capa-
mechanism. Under capture checking an effectful              bility. The capability io is created fresh inside
tool (Section 3.1) carries the capability it needs in       withIO and scoped to that block, so it cannot appear
its type, so the model can call it only when the            in the capture set of withIO’s result, which lives out-
hole’s scope binds that capability. Granting a ca-          side the block. Capture checking therefore reports
pability for one phase and withholding it in the            that io outlives its scope: the lambda would carry
next yields least-authority, per-phase permissions:         io out past the withIO block that introduced it, and
a snippet generated where a read-only file handle           the compiler rejects the leak before the body runs.

                                                        6
Information flow control: classified data. Ca-              net effect is more flexibility without losing safety:
pability scoping also rules out information flows           a fixed pure function commits the pipeline to one
that a pure access-control language cannot describe.        shape in advance, while a nested typed-hole call
Consider a skill that walks through several analy-          lets the program adapt to the content at runtime
sis steps over a legal contract. The user holds a           under the same capture-check argument.
sensitive document and wants to run the skill, but             We evaluate these guarantees empirically against
the agent in the program is powered by a hosted             an adversary in Section 7.4, porting AgentDojo’s
online model, so sending the contract text to that          prompt-injection attacks to L ACUNA.
model would leak it.
   The TACIT harness (Odersky et al., 2026) ad-             4.4    Residual Escape Hatches
dresses this with a typed container. Sensitive con-         Two constructs slip past the type-level contract. Re-
tent arrives wrapped:                                       flection lets code look up and use classes, fields,
 class Classified[T]:                                       and methods by name at runtime, reaching mem-
   def map[U](f: T -> U): Classified[U]                     bers and call paths the static checker never sees.
                                                            Raw process execution launches an external pro-
The only way to touch the content is through map,
                                                            cess that runs outside the programming language
which accepts a pure function (T -> U, capture set
                                                            altogether. Both are ambient authority: any code
empty). A pure function holds no capabilities, so
                                                            can reach them without being granted a capabil-
its body cannot read a file, open a socket, print,
                                                            ity, so a snippet can use them while holding none.
or feed data back to the hosted model. The result
                                                            The language feature safe mode (Scala, 2024c), a
of map is again Classified[U], so the wrapping is
                                                            compiler setting that forbids exactly these unsafe
preserved across the pipeline. The hosted agent
                                                            constructs in source, closes both. We therefore rec-
can plan the analysis, but the content never leaves
                                                            ommend running agents under safe mode. Without
the wrapper.
                                                            it, these authorities stay open and a snippet must
   The limitation is that the function passed to map        be treated as ordinary untrusted code. Resource
is written once, at code-generation time, so it can-        exhaustion, non-termination, and latency lie out-
not adapt to what is inside the wrapper. The agent          side the type system entirely and are bounded by
primitive lifts this restriction: inside the function       runtime budgets (see the Limitations).
passed to map, a nested call to local.agent[U] dis-
patches to a trusted local model. The nested call           5     Modeling Agent Patterns with L ACUNA
runs in the pure scope of map, so capture checking
still rejects any effectful leak of content, but the        With agent as the only new primitive, common
code that processes the content is now generated            agent patterns reduce to plain control flow over the
at runtime, with the content in view of the local           typed-hole shape.
model alone:
 val doc: Classified[String] = docs.load(id)                5.1    Typed Skills and Self-Improvement

 val report: Classified[Report] =
                                                            A skill is the reusable unit through which an
   doc.map { content =>            pure action only
                                                            agent encodes domain expertise. Existing solu-
     local.agent[Report](                                   tions sit at two extremes. At one end, the domi-
       s"follow the skill steps on $content")
   }
                                                            nant approach, exemplified by Anthropic’s Agent
                                                            Skills (Anthropic, 2025c), ships a skill as a text-
The outer (hosted) agent generates the surrounding          based guide the agent consults: it carries domain
program, including the lambda passed to map. It             knowledge well but is unenforceable, since noth-
sees the source of that lambda but not the value            ing stops the model from skipping a step or de-
of content, which is bound only when map fires at           viating from the procedure. At the other end,
runtime. At that point, content reaches local, the          Voyager (Wang et al., 2024a) and tool-maker sys-
trusted on-device model. The inner snippet is re-           tems (Cai et al., 2024) store a skill as a fixed piece
compiled in the same pure scope as the map body, so         of code: reproducible, but committed to a single
capture checking forbids it from invoking network           program that cannot adapt to new situations.
IO, the file system, or the hosted model’s API. The            Our agent primitive lets a skill sit between these
outer agent plans without ever seeing the content;          extremes. A skill is an ordinary typed function: its
the local agent acts on it with no way out. The             signature is fixed and checked end to end by the

                                                        7
compiler, while its body, generated per call, may            the surrounding scope already contains enough in-
freely mix plain code with nested agent calls. The           formation to produce a T without another model
following example sketches a skill for reviewing a           call. This shape is closely related to recursive
code change, which can sit anywhere on the spec-             language modeling (RLM) (Zhang et al., 2025a),
trum, from fully delegated to fully coded:                   which also lets an agent write code that re-invokes
 // 1. fully delegated: one agent call                       the model.
 def reviewPR(diff: Diff): Review =                             Further patterns, such as sub-agents with an iso-
   agent("apply the code-review checklist")
 // 2. mixed: code skeleton, agent inside                    lated context, parallel reasoning over a collection,
 def reviewPR(diff: Diff): Review =                          and planning with task assignment across models,
   val critical = diff.files.filter(_.risky)
   val notes = critical.map { f =>
                                                             follow the same control-flow recipe and are de-
     agent[Note](                                            ferred to Appendix F.
       s"review $f against the checklist")
   }
   Review.fromNotes(notes)
                                                             6     Realization in Scala 3
 // 3. fully coded: no agent call
 def reviewPR(diff: Diff): Review =                          The agent primitive is built on a lower-level oper-
   val notes = diff.files.map(check)                         ation, eval[T](source), that takes a string of Scala
   Review.fromNotes(notes)
                                                             source code and runs it as if it had been written
                                                             at the point where the call appears (its call site).
Self-improvement. A skill library is just a set of           The central technical challenge of this work is to
functions in scope, so revision falls out of name res-       support such a dynamic operation, running code
olution. In a long-running REPL session, an agent            that is only known as a string while the program is
emits a new function with the same name and sig-             already running, inside a statically typed host lan-
nature. This definition shadows the previous one,            guage without giving up the guarantees that static
so later agent calls resolve to the updated version.         typing provides.
The effect is to treat what cognitive-architecture ac-
counts (Sumers et al., 2024) call procedural mem-            6.1    Why eval is Hard in a Static Language
ory as code edited in place, the role that Reflex-
                                                             Dynamic languages offer this operation for free.
ion (Shinn et al., 2023) and Voyager-style libraries
                                                             Python’s eval(s, globals, locals) (Python
instead assign to free-form text or stored scripts.
                                                             Software Foundation, 2024) and JavaScript’s
5.2   ReAct Loop                                             eval(s) (Mozilla, 2024) take a string, turn it into
                                                             code at runtime, run it in the current scope or in a
A ReAct (Yao et al., 2023) loop interleaves reason-
                                                             dictionary of variables passed explicitly, and return
ing and acting. Any loop can be written as a tail-
                                                             whatever value results. The string is never checked
recursive function (one whose last action is a call to
                                                             in advance: it runs in the same untyped setting as
itself), so a ReAct loop is naturally a tail-recursive
                                                             the rest of the program, and any error surfaces only
agent call: at each round the model emits a snippet
                                                             when the offending line executes.
that calls in-scope tools (Section 3.1), processes
their results, and ends by calling agent[T](task)               Reproducing this convenience in a statically
again, until it can return a T directly. Conceptually,       typed host raises three obstacles. First, a static com-
the call unwinds turn by turn:                               piler normally turns source into code once, before
 // initial agent call:
                                                             the program runs, and does not compile arbitrary
 agent[T](task)                                              strings afterward. To evaluate a string, the program
 // 1st round snippet:     generated                         must invoke the compiler again, on itself, while
 val x = readFile(f)
 val y = parse(x)
                                                             it is already running. Second, the string must be
 agent[T](task)      // tail-call                            compiled as though it appeared at the call site, with
 // 2nd round snippet:                                       access to everything visible there: local variables,
 val x = readFile(f)
 val y = parse(x)                                            given instances (Scala’s implicit values, which the
                           generated
 val z = analyze(y)                                          compiler supplies from the surrounding context),
 agent[T](task)      // tail-call                            and capabilities (values that grant permission to
 // ... until the snippet returns a T directly
                                                             perform an effect such as I/O). In a dynamic lan-
Every recursive call has the same expected return            guage these bindings sit in a runtime dictionary the
type T, so each turn attacks the same problem with           interpreter can look up; in a static language they
more accumulated context, and the loop ends when             live only in the compiler’s internal representation

                                                         8
of the program, the syntax tree, and are gone by the          A simplified agentSafe reads:
time the program runs. Third, this second, inner               @evalSafeLike
compilation must apply exactly the same typing                 def agentSafe[T](
                                                                   task: String,
rules as the original one, so that the model-written               bindings: Array[Binding] = Array.empty,
code is held to the same contract as the code around               expectedType: String = "",
it. In particular, capture checking (Scala’s mech-                 enclosingSource: String = "",
                                                                   maxAttempts: Int = 3): EvalResult[T] =
anism for tracking which effects and resources a                 @tailrec def loop(
piece of code may use) must see the snippet in its                   n: Int,
                                                                     errs: List[String]): EvalResult[T] =
original context. Dynamic interpreters sidestep all                val prompt = buildPrompt(...)
three obstacles by giving up static typing in the first            val code = llm.complete(prompt)
place. Our goal is the opposite: to keep the safety                val r = evalSafe[T](
                                                                     code, bindings,
guarantees of a static host.                                         expectedType, enclosingSource)
                                                                   if r.isSuccess || n >= maxAttempts then r
6.2   The eval Primitive                                           else loop(n + 1, r.error.errors.toList)
                                                                 loop(1, Nil)
We add eval as a new built-in operation in the
Scala 3 compiler. It takes two forms:                         The @evalSafeLike annotation is what turns this
 def eval[T](source: String): T                               function into a hole. It instructs the compiler
 def eval[T](                                                 to fill the three context parameters (bindings,
     code: String,
     bindings: Array[Binding],                                expectedType, enclosingSource) at every call site, ex-
     expectedType: String,                                    actly as it does for a direct evalSafe call. Everything
     enclosingSource: String
 ): T
                                                              else is plain Scala: a retry loop around evalSafe[T]
                                                              in which the LLM supplies the candidate code and
The programmer writes only the short form,                    the compiler’s diagnostics provide the feedback.
eval[T](source): it takes a string of source code,
type-checks it against the expected type T using              6.4   How eval Works
everything in scope at the call site, and runs it.            At a high level, code containing eval (or an evalLike
The compiler then expands this short form into the            wrapper such as agent) is transformed and run in
long one, filling in three pieces of context auto-            four steps:
matically: bindings, the in-scope variables paired
with their runtime values; expectedType, the type T              • Rewrite. The compiler expands the eval call
written back out as text; and enclosingSource, the                 into the long form, filling in the context param-
text of the surrounding code with the call’s location              eters. This is done by a new compiler phase
marked by a placeholder. If the code string fails                  that runs after type checking, so it has access
to type-check, eval throws an EvalCompileException                 to the full typed syntax tree and can extract
carrying the compiler’s error messages. A variant,                 the necessary information from it.
evalSafe[T], instead returns the outcome as a value
                                                                 • Splice. At runtime, the splicer parses the
of type EvalResult[T], an algebraic data type with
                                                                   source string and drops it into the placeholder
two cases, Success(value) carrying the generated
                                                                   in that enclosing-statement text, producing a
value of type T and Failure(diag) carrying the fi-
                                                                   complete top-level statement that looks ex-
nal compiler diagnostics, so the caller can treat
                                                                   actly like code a developer could have written
a failed compilation as ordinary data rather than
                                                                   by hand at that spot.
catch an exception. The user-facing agentSafe[T]
wraps evalSafe the same way agent wraps eval.                    • Recompile. This spliced source is handed to
6.3   Building agent on eval                                       a fresh run of the same compiler, configured
                                                                   with the same options (including the same
The agent[T](task) primitive and its sibling                       effect and capability checks) as the original
agentSafe[T] are thin wrappers around eval, written                compilation. Type checking, capture check-
in ordinary Scala. They send the task prompt, to-                  ing, and error reporting are the ordinary ones
gether with the captured context, to an LLM; pass                  the compiler applies to any program.
the Scala source the model returns to evalSafe[T];
and, when a compilation fails, feed the compiler’s               • Extract. If the code compiles, the compiler
diagnostics back into the next prompt and try again.               produces a class file containing a method that

                                                          9
      evaluates the spliced code and returns its re-            Agent model        Acc. (%)   Recall (%)    #retry
      sult. This class file is loaded into the running          deepseek-flash         27.1          34.5      0.7
      program.                                                  gemini-lite            26.2          27.9      0.4
                                                                gpt-mini                9.2          16.2      0.5
    • Evaluate. The freshly compiled code is eval-
      uated in the program’s original execution con-          Table 1: L ACUNA on BrowseComp-Plus, varying only
                                                              the agent model that powers the agent hole; corpus,
      text (the same thread and class loader), yield-
                                                              retriever (k=5), and gpt-4.1 judge are fixed. Acc. is
      ing a value of type T that eval returns to the          judge-scored correctness and Recall is retrieval recall
      caller.                                                 against the evidence documents, an upper bound on
                                                              accuracy under the fixed budget; #retry is the mean
  Reusing the unmodified compiler on the spliced              compile-rejected regenerations per query.
source is what lets the safety properties of Section 4
hold without any checker of our own: the very guar-
antees the compiler provides for the surrounding              All tests pass, confirming that the implementation
program apply to the generated code as well. All              behaves as intended.
we have done is arrange for the compiler to see the           7.2   Complex Tool-Using Benchmark
generated code embedded in the right surrounding
                                                              We test whether the recursive agent design serves
program.
                                                              as a general agent on complex, tool-using tasks
6.5    Portability                                            by running L ACUNA on BrowseComp-Plus (Chen
                                                              et al., 2025b), a benchmark of hard information-
Two ingredients of our prototype are specific to
                                                              seeking tasks over a fixed corpus. Each task is
Scala: its capture-checking system and the hook
                                                              a single agent call that searches, reads results,
that lets a running program invoke the compiler
                                                              and either answers or recurses. Our aim is not
within its own process to splice and recompile. Nei-
                                                              to top the leaderboard, where accuracy is domi-
ther is fundamental. The design carries over to any
                                                              nated by retriever and base-model strength (both
statically typed host that tracks effects or capabili-
                                                              orthogonal to our contribution), but to show that
ties, as long as it can recompile code from within a
                                                              the typed primitive is a drop-in general agent.
running program and expose the live context at a
                                                              Table 1 shows that deepseek-v4-flash answers
call site to the rewriting step.
                                                              27.1% correctly while driving genuine multi-step
7     Evaluation                                              research (5.9 rounds, 15.5 searches per query),
                                                              gemini-3.1-flash-lite matches it at 26.2%,
Our evaluation asks four questions: do the type               and low-effort gpt-5.4-mini explores little and
system’s guarantees hold across host and generated            scores accordingly (DeepSeek-AI, 2026; Google
code (Section 7.1); can the recursive agent de-               DeepMind, 2026; OpenAI, 2026b). The primitive
sign handle complex, tool-using tasks (Section 7.2);          executes whatever agentic behavior the model gen-
does it support multi-turn conversation with tools            erates.
(Section 7.3); and do the capability guarantees of               The last column is the distinguishing one. Every
Section 4.3 hold against an adversary that plants             snippet is typechecked against its hole’s contract
prompt-injection attacks (Section 7.4)? We realize            before it runs, and one that fails never executes: the
L ACUNA as a Scala 3 library (Section 6). Full setup          compiler rejected 8.6% of generations and returned
details, models, and resource budgets are described           the diagnostics for regeneration (Section 3.4). The
in Appendix G.                                                loop converges quickly: 0.7 retries per query on
                                                              average, two-thirds of queries needing none, and a
7.1    Type-System Protection: A Collection of
                                                              91.4% end-to-end compile-success rate. The disci-
       Test Cases
                                                              pline thus adds no accuracy cost, is cheap to satisfy,
We isolate the type system as a verifier, indepen-            and guarantees that no ill-typed or out-of-scope
dent of any model, with roughly 400 test cases                action reaches the corpus.
emulating how host code and a generated snippet
combine. Each pairs host code with a snippet that             7.3   Multi-Turn Conversation Benchmark
is either well-formed (should compile and evaluate            We then test multi-turn conversation with tool use,
to the expected value) or ill-formed in a way agents          where state is carried across turns and the agent in-
commonly emit (should be rejected before it runs).            terleaves tool calls with replies. On τ 2 -bench (Bar-

                                                         10
                                                                    Solved (%, full reward)
            Agent model                System         Retail     Airline   Telecom   Tel.-WF    Overall
                                       Tool Calling    80.9        75.5      100.0       95.4      90.0
            deepseek-v4-flash
                                       L ACUNA         58.8        70.0       88.6       83.3      76.0
                                       Tool Calling    52.6        56.0       15.8       21.1      33.2
            gemini-3.1-flash-lite
                                       L ACUNA         43.9        38.0       14.9       24.6      29.1

Table 2: L ACUNA on τ 2 -bench: percentage of tasks solved per service domain. A conversation is a sequence of
agent calls sharing one REPL session. The user simulator is fixed at gpt-5.4 across agent models so the simulated
customer is a constant. Agent models run at temperature 0 with reasoning disabled. Tool Calling is τ 2 -bench’s
reference agent, which invokes the same domain tools through the native function-calling API rather than generated
code. Overall is solved-rate pooled over all 392 tasks.


res et al., 2025), a benchmark of tool-using conver-         code, with rejections rising from 3.2% on retail
sations across customer-service domains in which             to 89% on telecom.
the agent and a simulated user act on a shared en-              We expect these results to improve: prompt op-
vironment, we realize each conversation as a se-             timization or fine-tuning that teaches a model to
quence of agent calls that share one REPL ses-               write typed code as an agent, rather than emit iso-
sion. Each user message becomes an agent call                lated tool calls, should raise both the solve rate and
evaluated in that session, so everything prior turns         first-try compile success.
introduced (questions, replies, tool calls, printed
output) stays in scope. Conversational context is            7.4 Capability Safety Under Prompt Injection
thus carried by the REPL itself, with no dedicated           This study stresses the capability layer of Sec-
memory mechanism.                                            tion 4.3 against an adversary. We extend the TACIT
   Across the four domains (392 tasks),                      benchmark (Odersky et al., 2026), which evaluates
deepseek-v4-flash solves 76.0% of tasks                      capability tracking on agent code, with tasks drawn
outright, ranging from 58.8% on retail to                    from AgentDojo (Debenedetti et al., 2024), a dy-
88.6% on telecom (Table 2). These are genuine                namic environment that plants prompt-injection
interactions, averaging 5.7 user turns and 26.7 tool         attacks in the tool outputs an agent consumes. We
calls per task on retail, and the result is on par           port the AgentDojo task suites to L ACUNA, giv-
with the reference tool-calling agent. As in the             ing each agent only the capabilities its task re-
single-turn study, every snippet is typechecked              quires through scoped closures (Section 3.1), and
against its hole’s contract before it runs, and the          run the AgentDojo attack suite against the ported
retry loop absorbs the failures: retail averages             agents. TACIT and its data are open-source under
7.1 regenerations per task and recovers to a 77.6%           the Apache License 2.0, and the AgentDojo task
end-to-end compile-success rate, so no ill-typed             and attack suites we port are released under the
or out-of-scope action ever reaches the shared               MIT license.
environment.
                                                             8    Discussion and Future Work
   Conversational code is, however, more error-
prone than single-turn research code, because                A foundation, not a replacement. L ACUNA is
it must combine parsed tool results, prior-turn              not meant to replace existing agent architectures
state, and policy-conditioned actions: 22.4% of              but to give them a more flexible and safer foun-
deepseek-v4-flash’s retail generations are re-               dation: a single typed primitive for an agent’s be-
jected, against 8.6% on BrowseComp-Plus. How                 havior, its interaction with data, and its multi-step
often the verifier fires also depends strongly               reasoning, all checked statically. The patterns of
on the model’s coding ability. On the weaker                 Section 5 are available as ordinary control flow
gemini-3.1-flash-lite, the overall solve rate is             over agent, and a developer is free to keep any
low (29.1%) yet stays close to the reference agent,          specialized machinery an existing harness handles
matching it on telecom (14.9% versus 15.8%) and              well. A conventional ReAct loop (Yao et al., 2023),
exceeding it on telecom-workflow (24.6% versus               for instance, may manage the history of a long con-
21.1%): the gap is the model’s, not the primitive’s.         versation more efficiently than threading it through
The small model simply struggles to write correct            nested holes, while it can still use agent calls for

                                                        11
                                        Banking          Workspace              Slack             Travel
           Model          System
                                     Utility   Attack   Utility   Attack   Utility   Attack   Utility   Attack
                          CaMeL    52.8%       0/144     53.8%    0/560     48.6%    0/105      1.4%    0/140
           gemini-2.5-pro TACIT   56.94%       0/144    50.54%    0/560    40.00%    0/105    64.29%    0/140
                          L ACUNA 63.19%       0/144    56.25%    4/560    42.86%    2/105    63.57%    1/140
                          CaMeL    62.5%       1/144     81.4%    0/560     68.6%    0/105     74.3%    0/140
           o4-mini-high   TACIT   59.03%       0/144    52.86%    0/560    47.62%    0/105    68.57%    1/140
                          L ACUNA 65.97%       0/144    55.54%    0/560    49.52%    1/105    71.43%    0/140

Table 3: L ACUNA on the four stock AgentDojo domains. Utility is the fraction of user tasks completed successfully;
Attack is the number of injection trials in which the attacker’s goal was achieved over total trials. CaMeL numbers
are taken from (Debenedetti et al., 2025); TACIT numbers are taken from (Odersky et al., 2026); L ACUNA numbers
are from our runs.


the dynamic behaviors where type or capability                Limitations
safety matters.
                                                              Well-typed is not correct. The compiler checks
Refinement-typed holes. A natural next step is                that a generated snippet has the expected static
to let the expected type T carry a refinement pred-           type and respects the capabilities in scope. It does
icate (Rondon et al., 2008; Bovel et al., 2026), so           not check that the snippet does the right thing. A
the contract constrains not just the shape of the             well-typed snippet can still implement the wrong
result but also its properties (for example, an inte-         algorithm, call the wrong in-scope tool, or return a
ger within a bound, a list of fixed length, or rela-          plausible but incorrect value, and the retry loop of
tional invariants linking inputs to outputs). First-          Section 3.4 is silent on all three: it regenerates only
class refinement types for Scala (Bovel et al., 2026)         when the compiler rejects the snippet, so a snippet
make this concrete in our host language. Check-               that compiles runs whether or not it is semantically
ing the refinement at the hole would further open             correct. Our guarantees concern the shape and
the door to verified decoding, steering generation            authority of an action, not its semantic correctness,
toward values that provably satisfy the predicate,            and human review or test oracles remain necessary
with the predicate discharged by a verifier such              for the latter. Narrowing this gap by letting the
as Lean (de Moura and Ullrich, 2021) or Stain-                expected type carry a refinement predicate, so the
less (Hamza et al., 2019).                                    contract constrains the result’s properties and not
                                                              just its shape, is a direction we outline in Section 8.
9   Conclusion
We have proposed L ACUNA, a single primitive                  Authority is only as tight as the granted scope.
agent[T](task), that treats an agent’s action as a            The capability guarantees of Section 4.3 bound a
typed hole in the host program. At runtime the                generated snippet to the effects and data its lexical
LLM fills the hole with code, compiled against                scope already grants, and they hold even against a
the expected type T in the original lexical context,          model that emits hostile code. What they do not
fusing program execution and model reasoning                  do is prevent the model from being influenced by
into one process. Recursion and composition over              injected content. They only bound what that influ-
this primitive suffice to express common agent pat-           ence can reach. The protection is therefore exactly
terns, including tools, typed skills, ReAct loops,            as tight as the scope the developer hands each hole.
and multi-model planning, as ordinary control flow.           A hole over-provisioned with capabilities it does
Safety follows from the host language itself: the             not need reopens the attack surface, and an attacker
type system enforces scope and result-shape con-              who steers the model into misusing a capability
straints, and a rejected snippet never runs. Across a         the task legitimately grants is not blocked. Con-
collection of verifier test cases, BrowseComp-Plus,           sistent with this, a small number of injection trials
and τ 2 -bench, the primitive serves as a drop-in             still succeed in our adversarial study (Section 7.4).
agent while the compiler blocks every ill-typed or            Least-authority scoping is thus a property the de-
out-of-scope action before it runs, with diagnostics          veloper must supply: the type system enforces it
driving retries.                                              but does not infer it.

                                                         12
Dependence on the model’s coding ability. Be-                 code (Section 4.4). Because L ACUNA executes
cause a rejected snippet never runs, the safety guar-         model-generated code as real, effectful actions, any
antee holds regardless of how capable the model               deployment that relaxes these defenses, by omitting
is; progress does not. An agent advances only                 safe mode or over-provisioning capabilities, carries
when the model can express its intended action                a corresponding risk of harmful actions, whether
as well-typed host code, so a model that writes               from model error or prompt injection.
weak Scala pays a heavy retry tax or fails to con-
                                                              Termination and resource use. Recursion depth,
verge, while the guarantee merely keeps its broken
                                                              fuel, and wall-clock or memory limits are not type-
attempts from executing. The effect is sharp and
                                                              level properties. A genuinely complex task and
model-dependent in our experiments (Section 7.3):
                                                              a runaway recursion are indistinguishable to the
only 3.2% of gemini-3.1-flash-lite’s retail
                                                              type system, so the runtime falls back on config-
snippets are rejected, but 89% are on the harder
                                                              urable depth and retry caps (Section 3.3) and ex-
telecom domain, where its code generation de-
                                                              ternal budgets, such as the nesting-depth cap and
grades and most turns make no progress. We con-
                                                              the per-query wall-clock limit in our experiments
jecture that part of this gap is due to Scala being
                                                              (Appendix G). These budgets bound cost and non-
less represented in pretraining data than Python,
                                                              termination, but they must be set by the user, and a
the usual language of code-as-action agents, so the
                                                              cap set too low can abort a legitimate long-horizon
competence floor a typed host imposes is higher.
                                                              task.
Closing it calls for stronger or better-adapted code
models rather than changes to the primitive.
Latency and cost. Each agent call pays for a                  References
model completion and at least one compiler pass,              Amazon Web Services. 2024. Cedar policy language.
and nested recursion stacks both. Every retry adds             Accessed: 2025-06-01.
a further completion and pass, so cost scales with            Amazon Web Services. 2025. Bedrock AgentCore pol-
the rejection rate: modest where the generated code            icy. Accessed: 2025-06-01.
is clean (Section 7). A body that is generated once
                                                              Anthropic. 2024. Model context protocol. Accessed:
and reused, such as a function-typed hole compiled
                                                                2025-06-01.
a single time and applied many times (Appendix A),
amortizes the compile, but cold calls and tight per-          Anthropic. 2025a. Claude code.
element loops with ever-varying generated code re-            Anthropic. 2025b. Code execution with MCP. Ac-
main expensive. The approach targets agent loops                cessed: 2025-06-01.
in which a model call already dominates latency,
so the current implementation is a poor fit for ultra-        Anthropic. 2025c. Equipping agents for the real world
                                                                with agent skills. Accessed: 2025-06-01.
low-latency settings.
                                                              Victor Barres, Honghua Dong, Soham Ray, Xujie Si,
Host-language requirements. The design as-                      and Karthik Narasimhan. 2025. τ 2 -bench: Evaluat-
sumes a statically typed host with an effect or                 ing conversational agents in a dual-control environ-
capability discipline and an in-process recompile               ment. CoRR, abs/2506.07982.
mechanism that can expose the live call-site con-             Luca Beurer-Kellner, Beat Buesser, Ana-Maria Cretu,
text (Section 6.5). Dynamically typed hosts obtain              Edoardo Debenedetti, Daniel Dobos, Daniel Fabian,
the splice but none of the safety, which is why the             Marc Fischer, David Froelicher, Kathrin Grosse,
guarantees do not transfer for free to the Python               Daniel Naeff, Ezinwanne Ozoani, Andrew Paverd,
                                                                Florian Tramèr, and Václav Volhejn. 2025. Design
stacks most agent frameworks build on. The base                 patterns for securing LLM agents against prompt in-
L ACUNA prototype needs only ordinary static typ-               jections. CoRR, abs/2506.08837.
ing. The permission, effect, and information-flow
controls of Section 4.3 are an opt-in layer on top            Luca Beurer-Kellner, Marc Fischer, and Martin T.
                                                                Vechev. 2023. Prompting is programming: A query
that additionally requires Scala 3 capture checking,            language for large language models. Proc. ACM
an experimental language feature. In either mode,               Program. Lang., 7(PLDI):1946–1969.
the safety story relies on a safe mode that closes
                                                              Andrew Blinn, Xiang Li, June Hyung Kim, and Cyrus
reflection and raw process execution. Without it,               Omar. 2024. Statically contextualizing large lan-
those ambient authorities remain escape hatches                 guage models with typed holes. Proc. ACM Program.
and a snippet must be treated as ordinary untrusted             Lang., 8(OOPSLA2):468–498.


                                                         13
Aleksander Boruch-Gruszecki, Martin Odersky, Ed-               DeepSeek-AI. 2026. DeepSeek-V4-Flash. Model card.
  ward Lee, Ondrej Lhoták, and Jonathan Immanuel                 Accessed: 2026-05-26.
  Brachthäuser. 2023. Capturing types. ACM Trans.
  Program. Lang. Syst., 45(4):21:1–21:52.                      Jack B. Dennis and Earl C. Van Horn. 1966. Program-
                                                                  ming semantics for multiprogrammed computations.
Matt Bovel, Viktor Kunčak, and Martin Odersky. 2026.             In Communications of the ACM, volume 9, pages
 First-class refinement types for scala. Preprint,               143–155. ACM.
 arXiv:2605.08369.
                                                               Google DeepMind. 2026. Gemini 3.1 flash-lite. Model
Jonathan Immanuel Brachthäuser, Philipp Schuster, and            card. Accessed: 2026-05-26.
  Klaus Ostermann. 2020. Effects as capabilities: Ef-
  fect handlers and lightweight effect polymorphism.           Jad Hamza, Nicolas Voirol, and Viktor Kuncak.
  Proc. ACM Program. Lang., 4(OOPSLA):126:1–                     2019. System FR: formalized foundations for the
  126:30.                                                        stainless verifier. Proc. ACM Program. Lang.,
                                                                 3(OOPSLA):166:1–166:30.
Tianle Cai, Xuezhi Wang, Tengyu Ma, Xinyun Chen,
  and Denny Zhou. 2024. Large language models as               Omar Khattab, Arnav Singhvi, Paridhi Maheshwari,
  tool makers. In The Twelfth International Conference          Zhiyuan Zhang, Keshav Santhanam, Sri Vard-
  on Learning Representations, ICLR 2024, Vienna,               hamanan, Saiful Haq, Ashutosh Sharma, Thomas T.
  Austria, May 7-11, 2024.                                      Joshi, Hanna Moazam, Heather Miller, Matei Za-
                                                                haria, and Christopher Potts. 2024. DSPy: Com-
Sizhe Chen, Julien Piet, Chawin Sitawarin, and David            piling declarative language model calls into state-
  Wagner. 2025a. StruQ: Defending against prompt in-            of-the-art pipelines. In The Twelfth International
   jection with structured queries. In USENIX Security          Conference on Learning Representations, ICLR 2024,
  Symposium. USENIX Association.                                Vienna, Austria, May 7-11, 2024. OpenReview.net.
Zijian Chen, Xueguang Ma, Shengyao Zhuang, Ping                Mark S. Miller. 2006. Robust Composition: Towards a
   Nie, Kai Zou, Andrew Liu, Joshua Green, Kshama               Unified Approach to Access Control and Concurrency
   Patel, Ruoxi Meng, Mingyi Su, Sahel Shari-                   Control. Ph.D. thesis, Johns Hopkins University.
   fymoghaddam, Yanxi Li, Haoran Hong, Xinyu
   Shi, Xuye Liu, Nandan Thakur, Crystina Zhang,               Mozilla. 2024. eval() - JavaScript. MDN Web Docs,
   Luyu Gao, Wenhu Chen, and Jimmy Lin. 2025b.                  JavaScript Reference. Accessed: 2026-05-25.
   Browsecomp-plus: A more fair and transparent eval-
   uation benchmark of deep-research agent. CoRR,              Milad Nasr, Nicholas Carlini, Chawin Sitawarin,
   abs/2508.06600.                                               Sander V. Schulhoff, Jamie Hayes, Michael Ilie, Juli-
                                                                 ette Pluto, Shuang Song, Harsh Chaudhari, Ilia Shu-
Mihai Christodorescu, Earlence Fernandes, Ashish                 mailov, Abhradeep Thakurta, Kai Yuanqing Xiao,
  Hooda, Somesh Jha, Johann Rehberger, Kamalika                  Andreas Terzis, and Florian Tramèr. 2025. The at-
  Chaudhuri, Xiaohan Fu, Khawaja Shams, Guy Amir,                tacker moves second: Stronger adaptive attacks by-
  Jihye Choi, Sarthak Choudhary, Nils Palumbo, An-               pass defenses against LLM jailbreaks and prompt
  drey Labunets, and Nishit V. Pandya. 2025. Systems             injections. CoRR, abs/2510.09023.
  security foundations for agentic computing. CoRR,
  abs/2512.01295.                                              Martin Odersky, Yaoyu Zhao, Yichen Xu, Oliver Brače-
                                                                vac, and Cao Nguyen Pham. 2026. Securing agents
Leonardo de Moura and Sebastian Ullrich. 2021. The              with tracked capabilities. In Proceedings of the ACM
  Lean 4 theorem prover and programming language.               Conference on AI and Agentic Systems, CAIS ’26,
  In Automated Deduction - CADE 28 - 28th Interna-               page 812–838, New York, NY, USA. Association for
  tional Conference on Automated Deduction, Virtual              Computing Machinery.
  Event, July 12-15, 2021, Proceedings, Lecture Notes
  in Computer Science, pages 625–635. Springer.                Cyrus Omar, Ian Voysey, Michael Hilton, Jonathan
                                                                 Aldrich, and Matthew A. Hammer. 2017. Hazelnut:
Edoardo Debenedetti, Ilia Shumailov, Tianqi Fan, Jamie           a bidirectionally typed structure editor calculus. In
  Hayes, Nicholas Carlini, Daniel Fabian, Christoph              Proceedings of the 44th ACM SIGPLAN Symposium
  Kern, Chongyang Shi, Andreas Terzis, and Florian               on Principles of Programming Languages, POPL
  Tramèr. 2025. Defeating prompt injections by design.           2017, Paris, France, January 18-20, 2017, pages
  CoRR, abs/2503.18813.                                          86–99. ACM.
Edoardo Debenedetti, Jie Zhang, Mislav Balunovic,              OpenAI. 2025. Introducing GPT-4.1 in the API. Ac-
  Luca Beurer-Kellner, Marc Fischer, and Florian                 cessed: 2025-06-01.
  Tramèr. 2024. AgentDojo: A dynamic environment
  to evaluate prompt injection attacks and defenses for        OpenAI. 2026a. Introducing GPT-5.4. Accessed: 2026-
  LLM agents. In Advances in Neural Information Pro-             05-26.
  cessing Systems 38: Annual Conference on Neural
  Information Processing Systems 2024, NeurIPS 2024,           OpenAI. 2026b. Introducing GPT-5.4 mini and nano.
  Vancouver, BC, Canada, December 10 - 15, 2024.                 Accessed: 2026-05-26.


                                                          14
OpenCode. 2025. OpenCode: The open source AI                  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
  coding agent. Accessed: 2026-05-15.                            Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le,
                                                                 and Denny Zhou. 2022. Chain-of-thought prompting
Pydantic. 2025. Monty: A Python interpreter in Rust.             elicits reasoning in large language models. In Ad-
                                                                 vances in Neural Information Processing Systems 35:
Python Software Foundation. 2024. Built-in functions:           Annual Conference on Neural Information Process-
  eval and exec. Python Language Reference, version              ing Systems 2022, NeurIPS 2022, New Orleans, LA,
  3. Accessed: 2026-05-25.                                       USA, November 28 - December 9, 2022.

Brandon Radosevich and John Halloran. 2025. MCP               Simon Willison. 2023. The dual LLM pattern for build-
  safety audit: LLMs with the Model Context                     ing AI assistants that can resist prompt injection. Ac-
  Protocol allow major security exploits. CoRR,                 cessed: 2026-02-22.
  abs/2504.03767.                                             Yichen Xu, Oliver Bračevac, Cao Nguyen Pham,
                                                                and Martin Odersky. 2025. What’s in the box:
Patrick Maxim Rondon, Ming Kawaguchi, and Ranjit                Ergonomic and expressive capture tracking over
  Jhala. 2008. Liquid types. In Proceedings of the              generic data structures. Proc. ACM Program. Lang.,
  ACM SIGPLAN 2008 Conference on Programming                    9(OOPSLA2):1726–1753.
  Language Design and Implementation, Tucson, AZ,
  USA, June 7-13, 2008, pages 159–169. ACM.                   Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak
                                                                Shafran, Karthik R. Narasimhan, and Yuan Cao. 2023.
Aymeric Roucher, Albert Villanova del Moral, Thomas             ReAct: Synergizing reasoning and acting in language
  Wolf, Leandro von Werra, and Erik Kaunismäki.                 models. In The Eleventh International Conference
  2025.     smolagents: A barebones library for                 on Learning Representations, ICLR 2023, Kigali,
  agents that think in code. https://github.com/                Rwanda, May 1-5, 2023. OpenReview.net.
  huggingface/smolagents. Accessed: 2026-05-15.
                                                              Alex L. Zhang, Tim Kraska, and Omar Khattab. 2025a.
Scala. 2024a. Scala 3: Capture checker. Source: https:          Recursive language models. CoRR, abs/2512.24601.
  //github.com/scala/scala3. Accessed: 2026-05-
  25.                                                         Yanzhao Zhang, Mingxin Li, Dingkun Long, Xin Zhang,
                                                                Huan Lin, Baosong Yang, Pengjun Xie, An Yang,
                                                                Dayiheng Liu, Junyang Lin, Fei Huang, and Jingren
Scala. 2024b. Scala 3: Explicit nulls. Source: https:
                                                                Zhou. 2025b. Qwen3 embedding: Advancing text
  //github.com/scala/scala3. Accessed: 2026-05-
                                                                embedding and reranking through foundation models.
  25.
                                                                CoRR, abs/2506.05176.
Scala. 2024c. Scala 3: Safe mode. Source: https:
  //github.com/scala/scala3. Accessed: 2026-05-
  25.

Noah Shinn, Federico Cassano, Ashwin Gopinath,
  Karthik Narasimhan, and Shunyu Yao. 2023. Re-
  flexion: Language agents with verbal reinforcement
  learning. In Advances in Neural Information Pro-
  cessing Systems 36: Annual Conference on Neural
  Information Processing Systems 2023, NeurIPS 2023,
  New Orleans, LA, USA, December 10 - 16, 2023.

Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan,
  and Thomas L. Griffiths. 2024. Cognitive architec-
  tures for language agents. Transactions on Machine
  Learning Research, 2024.

Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Man-
  dlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and An-
  ima Anandkumar. 2024a. Voyager: An open-ended
  embodied agent with large language models. Trans-
  actions on Machine Learning Research, 2024.

Xingyao Wang, Yangyi Chen, Lifan Yuan, Yizhe Zhang,
  Yunzhu Li, Hao Peng, and Heng Ji. 2024b. Exe-
  cutable code actions elicit better LLM agents. In
  Forty-first International Conference on Machine
  Learning, ICML 2024, Vienna, Austria, July 21-27,
  2024, pages 50208–50232.


                                                         15
A    Richer Result Types
The richer the type, the tighter the contract. An             Pattern exhaustiveness. The compiler flags non-
algebraic data type pins the shape of the result:             exhaustive matches over sealed shapes, which
 > case class Person(                                         catches a common failure mode of generated dis-
 | name: String, born: Int, field: String)
 > val turing: Person =                                       patch logic:
 | agent[Person]("info about Alan Turing")                     > enum Color { case Red, Green, Blue }
 // LLM produces:                                              > def label(c: Color): String =
 //   Person(                                                  | agent[String](s"name the color $c")
 //     name = "Alan Turing", born = 1912,                     // model produces:
 //     field = "Computer science")                            //    c match
 val turing: Person = Person(                                  //      case Color.Red => "red"
   name = "Alan Turing", born = 1912,                          //      case Color.Green => "green"
   field = "Computer science")                                 EvalCompileException:
                                                                  agent failed to compile:
The generated code is a constructor call. The case-               match may not be exhaustive.
                                                                  It would fail on pattern case: Color.Blue
class arity and field types are part of Person, so the
model cannot return a value with a missing field or
a wrong-typed one.                                            C    Defining a Tool: A Memory Tool
   A function type asks the model for an implemen-
tation:                                                       Section 3.1 states that a tool is just a function in
 > val toRoman: Int => String =
                                                              scope, so defining a tool is just defining a function.
 | agent("convert 1..3999 to Roman numerals")                 A simple memory tool, for instance, is a mutable
 // LLM produces:                                             map with a few functions to manipulate it:
 //   val pairs = List(
 //     1000 -> "M", 900 -> "CM", 500 -> "D",                  val memory: mutable.Map[String, String]
 //     400 -> "CD", 100 -> "C", 90 -> "XC",                   def setMemory(key: String, value: String): Unit
 //     50 -> "L", 40 -> "XL", 10 -> "X",                      def getMemory(key: String): Option[String]
 //     9 -> "IX", 5 -> "V",    4 -> "IV",                     def searchMemory(
 //     1 -> "I")                                                  query: String): List[(String, String)]
 //   (n: Int) =>                                              def deleteMemory(key: String): Unit
 //     var x = n; val sb = StringBuilder()
 //     for (v, s) <- pairs do                                With these names in scope, the agent uses the tool
 //       while x >= v do { sb ++= s; x -= v }                by writing ordinary calls to them. The compiler
 //     sb.toString                                           checks each call against its signature, with no reg-
 > (1 to 5).map(toRoman)
 val res1: Vector[String] =                                   istry or schema to keep in sync. Suppose an email
   Vector("I", "II", "III", "IV", "V")                        tool sendEmail(to, subject, body) is also in scope.
                                                              The agent first records a meeting, then, asked to
Here, the generated code is a function of type
                                                              email a colleague about it, recalls the details and
Int => String, stored once and called many times.
                                                              sends the message:
Because the function value is generated and com-
                                                               > agent[Unit](
piled once, it can be reused with no further LLM               | "remember the team sync is Friday at 3pm")
calls or compilation overhead.                                 // LLM produces:
                                                               //   setMemory("team-sync", "Friday 3pm")
B   Additional Static Rejections
                                                               > agent[Unit](
Beyond undefined names and shape mismatches                    | "remind Alice about the team sync")
                                                               // LLM produces:
(Section 4.2), the standard type system rejects fur-           //   val when = searchMemory("team sync")
ther common shortcuts.                                         //     .headOption.map(_._2).getOrElse("TBD")
                                                               //   sendEmail("alice@corp.com", "Team sync",
Null safety. Under Scala 3’s explicit nulls (Scala,            //     s"Reminder: the team sync is $when")
2024b), a null literal is not assignable to a non-
                                                              The second task never mentions a time, so the
nullable type, which catches a common shortcut
                                                              snippet first calls searchMemory to look the meeting
the model might otherwise reach for:
                                                              up, then feeds the result into sendEmail, compos-
 > val name: String =
 | agent("default user name, else null")                      ing two in-scope tools in a single typed snippet.
 // model produces: null                                      The compiler checks the composition end to end:
 EvalCompileException:                                        that searchMemory yields a list of (String, String)
   agent failed to compile:
   Found:    Null                                             pairs the snippet destructures correctly, and that
   Required: String                                           sendEmail receives arguments of the right type, with


                                                         16
no schema mediating the two calls.                            Schema and policy-based access control.
                                                              JSON-schema function calling and tool protocols
D    Tracked Capabilities in Scala 3                          such as MCP (Anthropic, 2024) are safe only over
A capability is an ordinary value tied to an ef-              pre-registered tools, and composition is checked
fect or resource: a file handle, a network socket,            tool by tool rather than end to end. Security analy-
a logger, or a mutable store (Brachthäuser et al.,            ses report tool poisoning and cross-origin abuse at
2020). In the object-capability model (Dennis and             the protocol boundary (Radosevich and Halloran,
Horn, 1966; Miller, 2006), code can perform an                2025; Christodorescu et al., 2025). Runtime
effect only if it holds a reference to the correspond-        policy languages such as Cedar (Amazon Web
ing capability. Capabilities are unforgeable and              Services, 2024), as deployed in Amazon’s Bedrock
propagate only by being passed as ordinary data.              AgentCore Policy (Amazon Web Services, 2025),
Scala 3’s capture checking (Scala, 2024a; Boruch-             pin access to a fixed list of resources but cannot
Gruszecki et al., 2023; Xu et al., 2025) lifts this           constrain information flow inside a permitted
discipline into the type system by recording, in a            operation.
value’s type, which capabilities the value can reach.         Prompt-injection defenses. Output filtering,
   Capturing types have the form T^{x1, ..., xn},             training-based hardening such as StruQ (Chen et al.,
where the capture set {x1, ..., xn} over-                     2025a), and LLM-as-judge monitoring are proba-
approximates the capabilities a value of this type            bilistic, and recent adaptive attacks bypass them in
may use. A type with an empty capture set, written            practice (Nasr et al., 2025), even as design-pattern
simply T, is pure and retains no capabilities. The            catalogs set out principled mitigations (Beurer-
shorthand T^ (for T^{any}) admits any capability.             Kellner et al., 2025). Dual-LLM mediation and
   Function types record the capabilities their               capability-based dataflow defenses (Willison, 2023;
bodies use. The closure (s: String) => f.write(s)             Debenedetti et al., 2025; Odersky et al., 2026)
has type String ->{f} Unit (shorthand for                     push toward static checking by having agents write
(String -> Unit)^{f}), which makes explicit that
                                                              capability-annotated programs, but enforce outside
the function uses the file capability f. A function           the host type system, at coarse granularity, and
whose declared type is T -> U is pure: its body               with non-atomic failure. We make the agent action
cannot invoke any capability, and any attempt to do           a typed hole checked by the host compiler, pre-
so is rejected before the body runs. The takeaway             execution, at capability granularity, with atomic
for this paper is that a function type is a static            failure.
whitelist of what the body may invoke, and the
lexical scope at a program point plays the same               Capability-safe and effect-typed languages.
role for the code that appears there. If a capability         Object-capability languages (Miller, 2006), effect
c is not in the lexical environment at a hole, no             systems, Scala 3 capture checking (Scala, 2024a;
code that fills the hole can invoke c.                        Boruch-Gruszecki et al., 2023), and region or own-
                                                              ership systems all provide the underlying discipline.
E   Additional Related Work                                   We apply that discipline to the agent action bound-
Beyond the frameworks compared in Section 2, we               ary. The novelty is the application and the eval
cover several further lines of work, especially ones          mechanism that preserves it.
bearing on the safety guarantees of Section 4 and
the capability layer (Section 4.3).                           F     Additional Agent Patterns

Agent sandboxing and isolation. Container and                 Beyond the patterns in Section 5, three more reduce
VM isolation, syscall filtering, and language-subset          to plain control flow over the typed-hole shape.
Python interpreters (Pydantic, 2025) confine a gen-
                                                              F.1   Chain of Reasoning
erated snippet but enforce only at runtime: a half-
executed script can leave the surrounding state in-           Chain-of-thought reasoning (Wei et al., 2022) is
consistent. Permission-scoped coding agents (An-              a sequence of agent calls nested in each other’s
thropic, 2025a; OpenCode, 2025) gate tool access              scope. The simplest form passes one call’s output
at the agent boundary but share this non-atomic fail-         directly into another’s prompt:
ure mode. We enforce pre-execution, at capability              val answer: Answer = agent(agent(
                                                                 s"polish this prompt: $task"))
granularity, with atomic failure.

                                                         17
The inner call rewrites task into a sharper prompt,
and the outer call consumes the rewrite. Each call             val plan: List[Subtask] =
                                                                 large.agent(s"plan the steps to $task")
has its own expected type, so the compiler checks              val parts = plan.map { sub =>
that the inner result is a String before it reaches              small.agent[Result](s"handle $sub")
the outer. The same shape generalizes to longer                }
                                                               val report: Report = large.agent(
chains: every call captures the bindings introduced              s"synthesize $parts into a report")
by earlier ones and operates on that richer context,
and the compiler keeps the chain coherent end to              The planner uses a powerful model to pick a strat-
end. An output that does not fit the next call’s pa-          egy and emit scaffolding code, including calls to
rameter type fails before that call runs. The pattern         small.agent for the sub-tasks. Cost and capability
covers prompt polishing, classification routed to a           decisions are local to each call, and the type system
specialist, and any case where one model’s output             does not need to know which provider is on the
feeds another.                                                other end.
                                                                 This shape generalizes the dual-LLM de-
F.2   Sub-Agent with Isolated Context                         sign (Willison, 2023; Debenedetti et al., 2025),
A call site sometimes wants to delegate to an agent           where a privileged planner that never sees raw
without sharing its full scope. In L ACUNA, this is           inputs orchestrates a quarantined doer that han-
just a top-level function that wraps an agent call:           dles the data. Any partition of calls across two or
 def subAgent[T](prompt: String): T =
                                                              more configured agents instantiates the same pat-
   agent[T](prompt)                                           tern, with the split chosen per call rather than fixed
                                                              by the framework. By itself this is only a routing
Calling subAgent[T](prompt) from anywhere in the              convention, and a misrouted call still leaks. Sec-
program runs an agent call whose lexical context              tion 4.3 turns the partition into an enforced barrier,
is the body of subAgent, not the caller’s. Inside that        using capture checking and Classified[T] to pre-
body, the names in scope are prompt together with             vent the planner agent from observing content it is
the top-level definitions (imports, package-level             not allowed to see.
definitions) reachable from this file. Local bindings,
capabilities, and instance members visible to the             G    Experimental Setup
caller do not leak in. A function signature is the
natural way to budget context: pass through what              Test Suite. We build L ACUNA on the
the sub-agent should see, and nothing else.                   Scala 3.9.0 compiler. The roughly 400 test
                                                              cases of Section 7.1 are contributed as REPL
F.3   Parallel Reasoning                                      tests in the Scala 3 compiler’s own test suite, so
Because each agent call is an ordinary Scala ex-              each case exercises the real pipeline (parse, typer,
pression, parallelism comes from ordinary Scala               capture check).
combinators. To summarize a collection of docu-
                                                              BrowseComp-Plus. A Python driver issues
ments independently, use par.map:
                                                              each of the 830 queries to the Scala REPL
 val summaries: List[String] =
   files.par.map { f =>                                       as a single agent[String] call and runs the
     val text = readFile(f)                                   tool calls the generated code makes against
     agent[String](s"summarize: $text")
   }.toList
                                                              a fixed retrieval index.      The agent has ex-
                                                              actly two tools in scope: search(query), re-
No special branching primitive is needed. The                 turning the top k=5 corpus hits with snippets,
same shape covers fan-out and fan-in, map-reduce              and getDocument(docid), returning one full
over a collection, and tree search where each                 document. Retrieval is held fixed across all
branch is an independent agent call.                          runs: an exact-search index over the canonical
                                                              BrowseComp-Plus Qwen3-Embedding-8B (Zhang
F.4   Planning and Task Assignment                            et al., 2025b) vectors (≈ 100k documents), with
Different agent calls can target different models:            queries embedded by the same model. Answers
a small fast model for routine sub-tasks, a larger            are graded by a fixed gpt-4.1 (OpenAI, 2025)
one for planning, a trusted local model for sensitive         judge, so accuracy differences track only the agent
data, and an untrusted public provider for the rest.          model. We compare deepseek-v4-flash (high
Each is a configured agent instance:                          reasoning effort), gemini-3.1-flash-lite (high

                                                         18
reasoning effort), and gpt-5.4-mini (low reason-              fine-tuning, so all model use is inference. The
ing effort), each at the provider’s default sampling          only local computation is the BrowseComp-Plus
temperature (DeepSeek-AI, 2026; Google Deep-                  retrieval index and the Scala compiler passes each
Mind, 2026; OpenAI, 2026b). Every query runs                  agent call triggers. Per-run resource budgets are
in its own REPL under a 600s wall-clock budget,               capped as described above (a 600s wall-clock
with recursive agent nesting capped at depth 128.             and depth-128 limit per BrowseComp-Plus query,
We log each query’s input, answer, and tool calls,            and the per-task limits on τ 2 -bench). Because
and trace every snippet the agent generates with              all models are hosted endpoints, the experiments
the compiler feedback it receives.                            require no local GPU.
τ 2 -bench. We run all four customer-service                  Licenses and release. We plan to release our L A -
domains (retail, airline, telecom, and                        CUNA implementation, test suite, and evaluation
telecom-workflow; 392 tasks), scored by τ 2 ’s                harness under the Apache License 2.0. The bench-
programmatic reward with no LLM judge. A                      marks we build on are open-source: BrowseComp-
Python driver runs the conversation loop: it shut-            Plus and τ 2 -bench are both under the MIT license.
tles each turn between the τ 2 simulated user                 Our use of these artifacts is limited to research
and the Scala REPL, evaluating one agent call                 evaluation, consistent with their intended use, and
per user turn, and forwards every tool call the               we release our own artifacts for research. Be-
generated code makes to the τ 2 server. The                   cause the benchmarks we build on are MIT-licensed
setup choice that matters most is how those tools             rather than research-only, our derivatives carry no
reach the agent: each domain ships a fixed typed              research-only restriction.
facade, one Scala function per tool with fully
typed signatures and nested arguments rendered
as case classes rather than raw JSON. The user
simulator is fixed at gpt-5.4 (OpenAI, 2026a),
and the agent models, deepseek-v4-flash and
gemini-3.1-flash-lite, run at temperature 0
with reasoning disabled, matching the baseline tool-
calling agent. Per-task limits guard against non-
termination: 200 environment steps, 40 user turns,
500 backend tool calls (50 per turn), and a 300s
idle timeout. We run one trial per task, which is
equivalent to a num-trials=1 setting in the origi-
nal τ 2 benchmark. The baseline evaluations use the
same models and settings with the official scripts.
We log the full conversation, tool calls, and reward
of each task, and trace all generated code with its
compiler diagnostics.
Model size and budget. All agent, judge, and
user-simulator models (deepseek-v4-flash,
gemini-3.1-flash-lite,              gpt-5.4-mini,
gpt-4.1, and gpt-5.4) are hosted endpoints
accessed through their providers’ APIs, and we
deliberately use the smaller, lower-cost tiers (flash,
lite, mini) as the agent. Where a provider discloses
architecture we report it: deepseek-v4-flash
is a 284B-parameter Mixture-of-Experts that
activates 13B parameters per token, and retrieval
uses the open 8B Qwen3-Embedding-8B. Google
and OpenAI do not publish parameter counts
for the Gemini and GPT models, so we cannot
report those sizes. We perform no training or

                                                         19
