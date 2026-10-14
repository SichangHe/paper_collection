                                            Modular Responsiveness Verification of Rust
                                                        Async Runtimes

                                                   Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

                                                               University of British Columbia, Canada



                                              Abstract. Asynchronous (async) programming is a popular paradigm
                                              for managing concurrency. Languages that provide async support typi-
                                              cally have a runtime to manage asynchronous executions. These runtimes
arXiv:2610.09198v1 [cs.PL] 6 Oct 2026




                                              are critical infrastructure, yet verifying them has received little attention.
                                              One reason is that a property that users care most about from an async
                                              runtime is a liveness property: tasks submitted to the runtime eventually
                                              make progress. Verifying liveness is challenging for libraries that are both
                                              concurrent and highly optimized.
                                              We present a lightweight and modular proof technique for verifying even-
                                              tual progression guarantees for Rust async runtimes. We describe this
                                              technique in the context of a simple language based on Rust and Rust’s
                                              async model. We then realize this proof technique as a set of static anal-
                                              yses for Rust and use these to verify eventual progression of several key
                                              components of multiple Rust async runtime implementations.

                                              Keywords: Verification · Static Analysis · Asynchronous Programming


                                        1   Introduction
                                        To take advantage of multi-core CPU resources, modern programs make exten-
                                        sive use of asynchronous programming, which relieves developers from needing
                                        to manage concurrency themselves. Asynchronous programming is usually sup-
                                        ported by an async runtime and such runtimes exist for most languages, includ-
                                        ing Java [22,11], JavaScript [21], Python [24], and Rust [25,28].
                                            An async runtime takes care of managing a graph of inter-dependent user-
                                        defined asynchronous tasks, some of which may be waiting on external events,
                                        and others that may be waiting on the result of other tasks. Async runtimes
                                        vary in complexity, but even a simple runtime must keep track of tasks, wait and
                                        observe relevant events, and notify tasks to continue executing. These runtimes
                                        and their correctness from a user’s perspective are the focus of this paper.
                                            A critical responsiveness property of async runtimes that users depend on
                                        is eventual progression: assuming correct user code and a correct underlying
                                        operating system, every user-level async task managed by the runtime should
                                        eventually get to make progress (see Section 3).
                                            The eventual progression property is the cornerstone of any async runtime,
                                        but is also challenging to verify. This is because a typical async runtime man-
                                        ages a collection of async tasks, and these tasks may depend on a variety of
2      Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

external events. Async runtimes are also usually concurrent and contain multi-
ple components that communicate with one another. In addition to this inherent
complexity of async runtimes, languages such as Rust and OCaml do not ship an
async runtime as part of the languages but only provide an interface for imple-
menting async runtimes; users can use different runtime implementations simply
by importing different async libraries. This means that any formal techniques
aimed at async runtimes for such languages must be able to handle a diversity
of alternative implementations in practice.
    In this paper, we present a lightweight verification technique that
allows programmers to verify eventual progression for practical and
diverse async runtime implementations. To the best of our knowledge,
this is the first work to verify liveness guarantees of existing async runtime
implementations.
    Rust async runtimes consist of three major parts: 1. async tasks, which in-
clude primitive async tasks provided by async runtimes (called pollables) and
user-defined async functions using pollables, 2. Rust’s async/await syntax and
compiler support, which compile async functions to state-machine representa-
tions, and 3. reactors, which manage running async tasks by monitoring signals,
waking up tasks when signals are observed, and repeating until all tasks com-
plete. Assuming correctness of the Rust compiler, eventual progression boils
down to the behaviors of the sets of runtime-provided pollables and reactors.
    Our work relies on three key insights. First, we adopt a task-centric view
and find that it is sufficient to consider verification of eventual progression for
a single arbitrary task, instead of reasoning about a collection of tasks. Second,
we use runtime component boundaries for a natural and modular decomposition
of our verification goal. Finally, we observe that runtime components make use
of implicit and, most importantly, monotonic events to determine how to deal
with a task at any particular point in time. These events are usually internal to
the runtime and are key to establishing eventual progression.
    We formalize these three insights in a core language LART with an opera-
tional semantics for the implementation of pollables and reactors. We then de-
fine static analyses for LART whose verification conditions soundly imply eventual
progression of the runtime. Grounded in our formalism, we design a lightweight
specification language and verification technique for Rust called Jackdaw. De-
velopers of async runtimes can specify the necessary conditions for pollables to
be responsive, and annotate their implementation in terms of observations on
events. We use Jackdaw to verify eventual progression of pollable and reactor
components in two commonly used Rust async runtime libraries, smol [25] and
futures-rs [8], and tokio [28], the most widely used production runtime. We show
that our model and analyses handle a variety of real-world components with two
modest extensions.
    Our evaluation shows that pollable implementations can be verified with an
average specification-to-code ratio of less than 30%, and the verification can
prevent manually-seeded responsiveness bugs of various kinds.
    In summary, the main contributions of our work are as follows:
                Modular Responsiveness Verification of Rust Async Runtimes     3

1. We develop an abstract model of Rust async runtimes, via our study of real-
   world implementations. Using our model, we observe that eventual progres-
   sion for async runtimes fundamentally relies on the implementations of two
   kinds of critical components: pollables and reactors, which are programmed
   in a highly-stylized way. We formalize a core language LART capturing this
   programming paradigm for modeling pollable and reactor implementations.
2. We formally define the key responsiveness property of interest, eventual pro-
   gression, in terms of an operational semantics for LART that uses a novel
   notion of obligations. We develop modular static analysis techniques that
   track how each obligation is eventually discharged, and show their sound-
   ness and that this implies eventual progression.
3. We implement a prototype tool Jackdaw in Rust, which allows annotating
   Rust pollable and reactor implementations to obtain models in LART , and
   analyzes these models. We evaluate Jackdaw on three Rust async runtimes
   and successfully verify eventual progression of various pollable/reactor im-
   plementations with low specification effort. We also show that Jackdaw
   rejects responsiveness bugs that can arise in this challenging code.


2      Background
Async programming, as a concurrency programming model, provides a user-
level abstraction (called async tasks) for writing concurrent programs. Compared
to directly using OS threads, async tasks are entirely managed by a runtime
system in user space; this lets programs run a larger number of computations
concurrently on a small number of OS threads (even a single thread).


2.1     Async Rust
Rust provides async/await syntax for writing async programs in a style similar to
sequential ones. One can define an async function by adding the async keyword
before a normal function definition, such as the identity function below:

 1    async fn id<T>(x: T) -> T { return x; }


When the async function id is called, instead of returning a value of declared
type T, a future of type Future<T> is returned. This future represents an async
computation that, once run, should eventually resolve to a value of type T.
   Within async functions, one can attempt to resolve async computations by
awaiting on them. The await expression in the example below executes the id
function and immediately resolves it to the string literal.

 1    async fn hello_world() {
 2        let s = id("hello␣world").await;
4         Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

 3        println!(s);
 4    }

Await-points define where an async computation might need to be paused. This
does not happen in our hello_world example for two reasons:
1. The function only awaits async computations, which then run immediately.
2. There are no other computations that can be run concurrently.
These missing pieces are provided by combining async/await with async runtime-
provided pollables: a collection of primitive async computations such as async
I/O handlers, timers, and channels. Their implementations are provided by the
runtime directly (and not as user-level async functions); each call to a pollable
will return directly rather than be decomposed into smaller sub-computations.
    The common usage of await reflects the design that all runtime-provided
pollables implement the same Future trait; this syntax is compiled into calls to
the poll method declared as follows:

 1    pub trait Future<T> { fn poll(&mut self, w: Waker) -> Poll<T>; }


The poll method starts or resumes an async computation, executes until the
computation yields, and returns the state of the async computation: Pending if
the computation yields, and Ready if the computation completes1 :

 1    pub enum Poll<T> { Ready(T), Pending }


One might assume that user-defined async computations are expected to busy-
poll their dependent pollables. Instead, an async computation that awaits an-
other which is pending will itself be considered pending, and the runtime is given
the responsibility to track pending tasks and resume them when appropriate.
    The Rust compiler converts each async function into a state-machine: each
await-point in an async function, along with its start and end, makes up the
states. The state machine is implemented as the (generated) poll method for
the Future object returned from the async function call. Correspondingly, all
await expressions are translated to calls on the poll method of the awaited-on
task. When such calls return with a Ready result, the state machine for the await
ing task will advance; otherwise, a Pending result will be propagated upwards.
This enables programmers to compose larger async programs from smaller ones,
starting from pollables provided by the chosen runtime.
    To enable concurrency when a user task is paused, a runtime must have
alternative tasks to schedule. Runtime implementations provide an interface,
typically named spawn, for registering potentially-concurrent tasks:


1
     The method name poll may be somewhat misleading since poll does not simply
     query the state of async computations but also executes them as far as possible.
                       Modular Responsiveness Verification of Rust Async Runtimes              5

Compiled user task t
     w := Waker for task t
                              Rust async runtime
           State0
                                      Resume suspended
          Run pre-                                                   Scheduler
                                      async compute for w
         await code

                         p.poll(w)                                   w.wake()
           State1
            await                 Pollable p   Pending                Reactor
          pollable p
                                           r.insert(w)      w = r.take()
         Ready(val)      Ready(val)                                              Environment

                                                     Repository r
          Complete



Fig. 1: Control flow between Pollable/Reactor/Waker/Scheduler. Each Pollable
returns Ready or Pending; the Reactor reacts to the environment. Repositories
are a concept we introduce in this paper to abstract over how wakers are passed
to and stored by reactors.


 1    async fn concurrent_prints() {
 2        let t1 = spawn(print_after_3s());
 3        let t2 = spawn(print_after_3s());
 4        t1.await;
 5        t2.await;
 6    }


When task t1 starts waiting for its timer, the runtime can concurrently execute
task t2. It is the runtime’s responsibility to guarantee that, sometime after the
waited-for time expires, the poll method of the timer will be called again, and
as a result, the corresponding user task will resume executing.
    In summary, async programming in Rust relies on the built-in async/await
support of the language, but more importantly on an async runtime providing
correctly implemented interfaces such as Timer and spawn. Since Rust does not
ship with a dedicated async runtime, different async programs can use different
runtime implementations. It is therefore important that different async runtimes
live up to the same set of specifications.

2.2      Rust Async Runtimes
The progression of user-defined async tasks relies on an async runtime (Figure 1)
whenever those tasks are paused. A critical responsibility of the runtime is that
any paused task must eventually have its poll method called, attempting to
resume its execution.
   Wakers. Rust async runtimes encapsulate a pending-resumption task in a
Waker type. Each Waker is a handle on the top-level user task whose poll chain
6      Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

currently (transitively) awaits a pollable. Calling wake on it notifies a scheduler
to re-invoke that top-level task’s poll. The compiler-generated state machine
records the await-point at which the task was suspended, so the re-entered poll
resumes there and re-invokes poll on the same awaited pollable that previously
returned Pending. The only possibility for these tasks to be paused is if a runtime
pollable returns Pending. It is the responsibility of the runtime implementation
to register the corresponding Waker with the runtime, along with information to
allow the runtime to determine what event the task is waiting for.
    Reactors. A dedicated runtime component (typically called a Reactor ) is
used to manage all currently-paused tasks, storing references to their correspond-
ing Waker instances. The Reactor is run continuously: its responsibility is to pe-
riodically check the conditions that each paused task is waiting on (e.g., whether
timers have expired, or I/O events occurred). Rather than directly calling poll
on these tasks, which would interrupt the Reactor’s execution, the Reactor calls
wake to register the task with a scheduler. Assuming a fair scheduling algorithm,
the scheduler guarantees that each of these tasks will ultimately have its poll
function called again.
    In this paper, we leverage the abstractions provided by this idiomatic design
(which is shared across all Rust async runtimes we are aware of), and assume
in particular a high-level specification for wakers (and their scheduling) with-
out verifying their implementations or the fairness of the scheduling algorithm.
Instead, we focus on (1) the implementations of pollables, which form the key
building blocks and interfaces for building user-level programs, and (2) the imple-
mentations of Reactors, which are responsible for ensuring that these pollables,
and therefore the dependent user tasks, get called again as needed.


3     Overview

We introduce our approach to verifying eventual progression of Rust async run-
times through a representative example: a Timer pollable paired with a Reactor
that manages a collection of timers. We then state the eventual progression prop-
erty and the trusted components on which it relies, and informally describe the
per-component conditions our verification technique enforces. The model and
the analyses are made formal in Sections 4 and 5.


3.1   The Timer Example

A Timer is a runtime-provided pollable that pauses the calling async task until a
specified time has elapsed. Figure 2 shows the relevant data definitions and the
poll method of Timer. A timer carries the target time instant and a reference
to the Reactor responsible for waking it up. The poll method first compares
instant against the current time now(). If the time has already passed, poll
returns Ready and the awaiting task proceeds. Otherwise, poll sends the waker
and instant to the Reactor via transfer, and returns Pending. The awaiting task
                Modular Responsiveness Verification of Rust Async Runtimes         7


 1   struct TimerData { instant: Instant, waker: Waker }
 2   struct Timer { instant: Instant, reactor: &Reactor }
 3

 4   // w is a Waker for this pollable (guaranteed by Rust compiler)
 5   fn poll(self, w: Waker) -> Poll<()> {
 6       if self.instant <= now() {
 7           return Poll::Ready(());
 8       } else {
 9           self.reactor.transfer(
10               TimerData { instant: self.instant, waker: w });
11           return Poll::Pending;
12       }
13   }


Fig. 2: A Timer pollable. transfer inserts a TimerData (the waker together with
the target time) into the Reactor’s repository. We elide Rust details concerning
references and the Future trait.



is paused, and the Reactor takes over the responsibility to call poll again when
the target time has passed.
    A typical Reactor that manages a collection of timers is shown in Figure 3.
The Reactor maintains all currently-paused timers in the timers vector; transfer
(elided) inserts a fresh TimerData into this vector under appropriate synchroniza-
tion. The react method runs an infinite loop: at each iteration, it partitions the
vector based on whether each timer’s target time has passed, wakes every timer
whose time has passed, and retains the others for the next iteration. The Reactor
cannot terminate, because new responsibilities to wake timers may be transferred
to it at any future point.
     This pair illustrates the three reasoning concepts our verification builds on:
   Monotonic completion conditions. A timer’s completion condition self
.instant <= now() is a predicate on the external environment that is monotonic:
once true, it remains true. Monotonicity is what allows poll (and the Reactor)
to reliably decide completion based on an observation of the condition. Pollables
other than timers (e.g., I/O handlers, channels) condition on different monotonic
predicates, but the principle is the same.
    Responsibility transfer between components. Initially the called pol-
lable is responsible for its own completion: if its completion condition holds when
poll is called, poll returns Ready directly. If not, the pollable hands the responsi-
bility to its Reactor via transfer, then returns Pending. The Reactor periodically
checks the completion condition and, once it holds, calls wake on the correspond-
ing waker; the wakened task is then re-scheduled, and the responsibility is finally
discharged by a poll call returning Ready.
8        Yanze Li, Ivan Beschastnikh, and Alexander J. Summers


 1    struct Reactor { timers: Vec<TimerData> }
 2

 3    fn react(&self) {
 4        loop {
 5            let (ready, pending) = self.timers.partition(
 6                |t: TimerData| t.instant <= now()
 7            );
 8            for t in ready { t.waker.wake(); }
 9            self.timers.append(pending);
10        }
11    }


Fig. 3: A Reactor that manages a collection of timers. The react method is
spawned as a background thread.


3.2     Eventual Progression: the Core Responsiveness Property
Informally, the property we want of an async runtime is: whenever a user task
is paused waiting on a pollable whose completion condition will eventually hold,
that task is eventually resumed. We refer to this property as eventual progression.
We make this precise in Section 4.3.
    Several components participate in delivering eventual progression: the user
task itself, the Rust compiler, the external environment, the scheduler, and the
runtime-provided pollables and Reactors. A bug anywhere along this chain can
violate the property; we cannot ask any single component to bear the entire
burden. Our verification focuses on the pollable and Reactor implementations,
treating the other components as trusted.
Trusted Component 1 (The Rust Compiler). The Rust compiler preserves
the semantics of async functions during the compilation of these functions to
their state machine representations (Section 2.1).
Trusted Component 2 (Observations of the External Environment).
All APIs for polling and extracting data from the environment external to the
Rust program (OS, devices, etc.) behave correctly: signaling events and providing
data when expected.
Trusted Component 3 (Fair Scheduling of Rust Async Tasks). The
scheduler components of the Rust async runtime schedule tasks passed to them
fairly.
     The first two trusted components reflect well-established compilation and
OS infrastructure; the third reflects a well-studied problem largely independent
of the async focus of our work. Under these assumptions, the responsibility for
eventual progression reduces to the interaction between pollables and Reactors:
it is their collaboration that translates “the completion condition holds” into “the
awaiting task’s poll is called and returns Ready.”
                Modular Responsiveness Verification of Rust Async Runtimes        9

 3.3    Per-Component Conditions
 We decompose eventual progression into two component-level conditions, one for
 pollables and one for Reactors. Both are stated here informally; we make them
 precise as verification conditions in Section 5.
     A pollable’s responsibility is captured by three conditions on its poll method:

(P1) Completion faithfulness. If poll returns Ready, the completion condition has
     held.
(P2) Completion convergence. If the completion condition holds when poll is
     called, poll returns Ready.
(P3) Responsibility transfer. If poll returns Pending, the pollable has transferred
     its waker to a Reactor along with its completion condition.

    A Reactor’s responsibility is captured by two iteration-level conditions on
 the body of its main loop:

(R1) Iteration progress. If a transferred waker’s completion condition holds at the
     start of an iteration, the Reactor calls wake on it within that iteration.
(R2) Iteration preservation. A transferred waker that is not woken in this iteration
     is retained in the Reactor’s repository for a future iteration.

     We illustrate these conditions using the Timer/Reactor pair from Section 3.1.
 The completion condition is self.instant <= now(). Timer’s poll returns Ready
 only on the path where self.instant <= now() is observed, so (P1) holds. If self
 .instant <= now() holds when poll is called, the if-test takes the Ready branch,
 so (P2) holds. The Pending path is preceded by transfer, which inserts TimerData
  into the Reactor’s repository; this is the responsibility transfer (P3). For the
 Reactor: partition separates timers whose target time has passed from those
 that have not; wake is then called on every timer in the first group, satisfying
 (R1); append retains the rest, satisfying (R2).
     Crucially, (P1)–(P3) and (R1)–(R2) can be checked per-component, in isola-
 tion. This modularity is provided by our task-centric view: even though a Reactor
 concretely manages a collection of timers, the per-iteration conditions can be dis-
 charged by reasoning about a single arbitrary timer. Sections 4 and 5 formalize
 this insight by defining a core language LART for pollable and Reactor implemen-
 tations, an abstract domain that tracks observations of monotonic completion
 conditions, and verification conditions that imply (P1)–(P3) and (R1)–(R2).


 4     A Model of Rust Async Runtimes
 We model Rust async runtime components in a core language LART (Language
 for Async Runtime). LART is designed to capture the high-level architecture of
 Rust async runtimes and the programming paradigm for pollable and reactor
 reasoning rather than modeling the programming language Rust.
     Importantly, LART builds in two primitive notions that are central to verify-
 ing eventual progression: monotonic predicates (typically to model completion
10      Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

predicates for pollables) and obligations (used to abstractly represent suspended
user tasks waiting on a runtime-provided pollable).
    To reason about a collection of obligations in a reactor, we build in the
notion of a repository as an abstraction over concrete ways a reactor may store
wakers. A repository abstracts over a concrete data type such as a Rust Vec,
and LART statements abstract over concrete functions how wakers are passed to
(e.g., transfer in Fig. 2), stored in, and removed from these data types.
    LART is intentionally minimal, but as we will show in Sections 5 and 6, LART
is sufficient to capture the design idioms shared by real Rust async runtime
components with few extensions.

4.1   The Language LART
LART is parametrized over an infinite set of monotonic predicate symbols P (here-
after, simply predicates), partitioned into two disjoint (infinite) sets of internal
and external predicates: P = Pint ⊎ Pext . A monotonic predicate p ∈ P repre-
sents a stable-once-established condition: once p holds, it holds permanently in
the future. Internal predicates represent conditions that can be satisfied by pro-
gram actions (e.g., setting a flag from false to true); external predicates model
conditions which can only be updated by the environment, e.g., external signals
such as a timer expiring or an I/O event completing.
    In real code, the truth of monotonic predicates can typically be tested via
suitable boolean Rust expressions whose value changes monotonically; for exam-
ple, a timer’s completion condition can be checked via self.instant <= now().
We use the predicate symbols in our language to abstract over these concrete
conditions, which are required only to satisfy monotonicity.
    We assume an infinite set of wakers, Waker, and a lookup function τ :
Waker ⇀ Stmt × Env ; for a waker w, τ (w) denotes the (compiled, suspended)
user task the waker is able to reschedule (Sec. 2.2). As will be explained in
Sec. 4.2, such suspended tasks are represented concretely by pairs of a pollable
implementation that the user task is currently waiting on and its local environ-
ment; in the real Rust code this is handled with compiler-generated closures.
    Figure 4 defines the syntax of LART . Values include the unit, the pollable
return values Ready(v) and Pending, and wakers. Statement trigger(p) sets
the value of an internal predicate p to true (it is a no-op if p was already true).
insert(r, w, p) sends the waker w to the public repository r together with the
completion predicate p that must be waited for. Conceptually, this transfers
the obligation for progress of τ (w) to the reactor r (which must now monitor
p and wake w when satisfied). take(r, w) removes the entry for w from r (e.g.,
because it will be woken up). wake(w) invokes waker w, signaling the scheduler
to re-schedule the user task τ (w), which will in turn re-poll the corresponding
pollable. for (w, p) in r { s } iterates the body s over every (w, p) pair in r.
loop s repeatedly runs s (indefinitely). return v terminates a pollable with
result v (typically Ready(()) or Pending).
    We impose well-formedness conditions (formally defined in Appendix A) on
the LART statements representing pollable and reactor implementations. A pol-
               Modular Responsiveness Verification of Rust Async Runtimes                 11


         Values    v ::= () | Ready(v) | Pending | w       (w ∈ Waker)
    Statements     s ::= s1 ; s2 | skip | return v | wake(w)
                         | trigger(p) (p ∈ Pint )
                         | if p then s1 else s2     (p ∈ P)
                         | insert(r, w, p) (r ∈ Repo, p ∈ P)
                         | take(r, w) (r ∈ Repo) | for (w, p) in r { s }
                         | loop s
       Pollables   π ::= λ(w, p). s(wfp(s))
                                          #                ”
       Reactors    R ::= reactor { shared rs : (Trs , cp rs ) in (loop s) }   (wfr (s))


Fig. 4: Syntax of LART , parametrized over monotonic predicates P = Pint ⊎ Pext .
A pollable is a statement that returns on every path; a reactor declares a set
of public repositories and wraps its body in an infinite loop. We highlight
statements that are reactor-only.




lable π is a statement that satisfies its well-formedness predicate wfp when π
contains no loop or reactor-only constructs, and every execution path through
π contains a return statement.
    Reactors R are first-class in LART , and each owns (i.e., no overlap with other
reactors) a non-empty list of public repositories. Each public repository r is de-
clared along with a pair (Tr , cp r ), in which Tr is the type of pollable whose
wakers may be stored in r and cp r : Tr → P is the completion predicate scheme
mapping each pollable instance to its completion predicate. A reactor body needs
to satisfy its well-formedness predicate wfr , which requires that the body never
returns and contains no loop other than the (required) outermost one; this re-
flects the fact that reactors are intended to monitor the environment indefinitely
and never return.
    For simplicity, we assume each reactor has at most one public repository
per type of pollable and that well-formed programs respect the repository type-
checking constraints. We also assume the convention that insert, take, and for
in a reactor body access only repositories declared by that reactor, and pollables
always communicate with a dedicated, running reactor.
    In real code, rather than being associated with completely independent pred-
icates, two pollables of the same type will always depend on similar conditions,
but may differ in instance-specific parameters: for example, two timers both wait
on t ≤ now(), but with different deadlines t. In our language, we simply rep-
resent these as different predicates under the same scheme, as we abstract over
the form of these concrete boolean expressions.
12        Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

4.2     Operational Semantics

We define a small-step operational semantics for LART ; aside from the language
itself the main design novelty is that our runtime states explicitly track the
known status of monotonic predicates, as well as the status of wakers for sus-
pended user tasks. We begin by defining rules for statement execution (only),
and then show how to lift these to accommodate rules that model interleavings
with e.g., events from the external environment.
    A runtime state is a pair (ρ, G) ∈ Config ≜ Env ×Global, separating local
states from shared global states:

 – ρ ∈ Env is the local environment for pollables or reactors, mapping local
   variables to values;
 – G = (Σ, Q, R) ∈ Global ≜ Hist × ℘(Waker) × Repos is the global state,
   where
     ● Σ ∈ Hist ≜ ℘(P) is the monotonic history, recording the set of mono-
       tonic predicates true so far;
     ● Q ∈ ℘(Waker) is the rescheduling queue, containing the wakers that
       have been woken up but waiting for the scheduler to reinvoke the poll
       method of the corresponding pollable;
     ● R ∈ Repos ≜ Repo → ℘(Waker × P) is the repository map, mapping
       each repository to the set of waker-predicate pairs stored in it. We assume
       all waker-predicate pairs in a repository r respect the repository typing,
       i.e., every (w, p) ∈ R(r) has p ∈ img(cp r ), where img denotes the image
       of the predicate scheme cp r .

     Figure 5 defines the operational semantics for LART . trigger, insert, take,
and wake are atomic effectful statements that update the global state and reduce
to skip. if statements branch on whether a predicate is in the monotonic history
Σ 2 . for statements iterate over every (w, p) in R(r) present at the start of the
for-loop. We omit other conventional rules for loop, skip, etc. The full definition
is in App. B.
     As explained in Sec. 3, a Rust async runtime in general has many pollables
and reactors currently executing, and additionally interacts with other trusted
components, user tasks and the external environment, none of which are directly
modeled by LART programs. We model them via additional non-deterministic
transitions interleaved with the execution of statements defined in Fig. 5.
     We define runtime configurations as a pair (T , (Σ, Q, R)) where T is a multi-
set of pairs Stmt×Env representing all currently running pollables and reactors.
The runtime-level judgment T , (Σ, Q, R) 7−→r T ′ , (Σ ′ , Q′ , R′ ) is the reflexive
transitive closure of the rules at the bottom of Fig. 5. Rule (exec) models nor-
mal execution of a single-step of a currently-running pollable (or reactor). Rule
(user-new-await) models a new pollable instance being started due to the compi-
lation of an await usage in a user-task. We abstract over the details of initializing
2
     LART only allows branching on single monotonic predicates; extending this to com-
     binations as well as more-standard program expressions would be straightforward.
                 Modular Responsiveness Verification of Rust Async Runtimes                          13




s | κ −→p s′ | κ′

                                   p ∈ Pint
                                                                                         (trigger)
         trigger(p) | (ρ, (Σ, Q, R)) −→p skip | (ρ, (Σ ∪ {p}, Q, R))

                                                                                         (wake)
           wake(w) | (ρ, (Σ, Q, R)) −→p skip | (ρ, (Σ, Q ∪ {w}, R))

                             R′ = R[r 7→ R(r) ∪ {(w, p)}]
                                                                                         (insert)
           insert(r, w, p) | (ρ, (Σ, Q, R)) −→p skip | (ρ, (Σ, Q, R′ ))

                                    (w, p) ∈ R(r)
                              R′ = R[r 7→ R(r) \ {(w, p)}]
                                                                                        (take)
              take(r, w) | (ρ, (Σ, Q, R)) −→p skip | (ρ, (Σ, Q, R′ ))

                                         p∈Σ
                                                                            (if-t)
                           if p then s1 else s2 | κ −→p s1 | κ

                                         p∈/Σ
                                                                            (if-f)
                           if p then s1 else s2 | κ −→p s2 | κ

                          R(r) = {(w1 , p1 ), . . . , (wk , pk )}
                             si ≜ s[wi , pi /w, p] k ≥ 1
                                                                                        (for)
               for (w, p) in r { s } | (ρ, G) −→p s1 ; · · · ; sk | (ρ, G)

                                    R(r) = ∅
                                                                               (for-emp)
                for (w, p) in r { s } | (ρ, G) −→p skip | (ρ, G)

T , G 7−→r T ′ , G′

                      s | (ρ, (Σ, Q, R)) −→p s′ | (ρ′ , (Σ ′ , Q′ , R′ ))
                                                                                        (exec)
             T ∪ {(s, ρ)}, (Σ, Q, R) 7−→r T ∪ {(s′ , ρ′ )}, (Σ ′ , Q′ , R′ )

                               initπ (s, ρ)
                                                                     (user-new-await)
               T , (Σ, Q, R) 7−→r T ∪ {(s, ρ)}, (Σ, Q, R)

                                p ∈ Pext p ∈ /Σ
                                                                      (env-trigger)
                    T , (Σ, Q, R) 7−→r T , (Σ ∪ {p}, Q, R)

                              w ∈ Q τ (w) = (s, ρ)
                                                                                     (sched)
                T , (Σ, Q, R) 7−→r T ∪ {(s, ρ)}, (Σ, Q \ {w}, R)


Fig. 5: Operational semantics for LART : statement small-step rules (top) and
runtime configuration rules (bottom). Standard rules such as sequencing or skip
are omitted; the full definition is in Appendix B.
14      Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

a new instance of some pollable π (e.g., initializing the environment) using the
initπ predicate on the new pair of its implementation s and environment ρ. For
simplicity, we do not model dynamic creation of reactors but assume these to be
present in an initial runtime configuration.
    Rule (env-trigger) adds an external predicate to the history nondeterminis-
tically; this models that the environment may make an external condition true
at arbitrary time. Rule (sched) schedules a waker w in the rescheduling queue
Q by reinvoking the corresponding pollable. Since our model abstracts over the
user task code, which (due to the Rust compiler’s transformations) is guaran-
teed to re-call the awaited runtime pollable, our τ function formally maps the
waker directly to this runtime pollable’s representation, which is made available
for rescheduling by our rules. In the real runtime system, it is the user task that
originally awaited the pollable that would be rescheduled by the waker.
    Obligations. A key intuition for what is needed for an async runtime to be
responsive is that the runtime never forgets async tasks that may be able to
make further progress (for example, it doesn’t forget a task waiting on a timer).
To formalize this idea, we introduce the concept of obligations: responsibilities
that runtime components (especially reactors) are conceptually assigned that
must not be forgotten until they are discharged.
    Specifically, we use pairs (w, p) ∈ Waker × P in our novel operational se-
mantics to represent the obligation: if the monotonic condition p ever holds,
the runtime must eventually resume the task associated with w. An obligation is
created every time a user task awaits on a pollable, represented by the waker
used for resumption of the task and the condition being waited on. If the pol-
lable waited on returns Ready, the obligation is discharged as the user code will
be returned to directly; on the other hand, if a reactor executes wake(w) this
discharges the obligation based on our assumptions on the fair scheduler. These
are the only ways these obligations can be discharged.
    Given a repository map, R, the obligations of a reactor R, written Ob(R)
are defined as the union of the obligations in R(r) for every repository r owned
by R. For a given global state G we overload this syntax to define the total
obligations of a global state Ob(G) to be the union of Ob(R) over all reactors
R. Note that Ob(R) grows when a pollable transfers a waker via insert to R
and shrinks when one is removed via take.

4.3   Eventual Progression and Component Local Conditions
We now state an overall guarantee in terms of the interaction between user
code and an async runtime; we use this high-level notion to derive decomposed
verification conditions specific to pollable and reactor implementations.
Definition 1 (Eventual Progression). An async runtime satisfies Eventual
Progression iff, for any runtime configuration (T , G) reached during its execu-
tion, and for all user tasks awaiting on a pollable s with predicate p, either (a) s is
running with (s, ρ) ∈ T or (b) for which a waker w exists with (w, p) ∈ Ob(G),
it is guaranteed that if, on further execution p eventually becomes true, then
eventually the user task will be resumed.
                Modular Responsiveness Verification of Rust Async Runtimes        15

 Case (a) corresponds to a user task awaiting a pollable which is already running;
 this can potentially either result in delegation to a reactor (and case (b)) or
 returning a Ready(v) value directly causing the user task to resume. This allows
 us to define conditions specific to the implementation of a single pollable:

 Definition 2 (Pollable Responsiveness). A pollable π is responsive if every
 invocation with obligation (w, p) satisfies:

(P1) if the invocation returns Ready(v), then p ∈ Σ at the return point;
(P2) if p ∈ Σ at the entry of the invocation, then the invocation returns Ready(v)
     for some v;
(P3) if the invocation returns Pending, then either (w, p) ∈ R(r) for some public
     repository r, or w ∈ Q at the return point;

 Definition 2 captures two key concerns. (P1) and (P2) form the soundness and
 completeness for completion: (P1) ensures Ready-returns reflect actual comple-
 tion; (P2) ensures that an already-completed computation is eventually reported.
 (P3) ensures obligation-preservation: when a pollable yields, the obligation it
 carries must not be forgotten by the runtime. It may be transferred to a public
 repository (via insert) or discharged immediately by waking w (via wake).
     Considering Case (b) in Def. 1, we must require enough of a reactor to also
 ensure that obligations are preserved and eventually discharged when ready. We
 express these conditions per iteration i of the loop s construct defining the
 reactor, and write Gistart , Giend for the global states at iteration start and end.
 In the following, Ob icon denotes the obligations inserted into public repositories
 during iteration i (e.g., by concurrently-running pollables). We write Wake i ≜
 { w | wake(w) fires during iteration i } for the set of all obligations discharged
 via wake during the iteration:

 Definition 3 (Reactor Responsiveness). A reactor loop s is responsive if
 every iteration i satisfies:

        (R1)   ∀(w, p) ∈ Ob(Gistart ). p ∈ Σstart
                                            i
                                                    ⇒ w ∈ Wake i
                                                  i
        (R2)   Ob(Giend ) ⊇ Ob(Gistart ) ∪ Ob con \ (w, p) | w ∈ Wake i
                                                      


 (R1) guarantees progress at each iteration; the obligations whose predicate al-
 ready holds must be woken in the same iteration. In principle this condition
 could be weakened, but in practice this strong guarantee is common. (R2) guar-
 antees that no obligation is lost; obligations not discharged during the iteration
 must be retained in the public repositories by the end of the iteration. Obliga-
 tions arriving mid-iteration via Ob icon are not required to be woken in the same
 iteration even if their predicate already holds by iteration end; (R2) carries them
 into the next iteration.
     The relationship between these component local conditions and the global
 Eventual Progression property is summarized as follows; the corresponding sound-
 ness theorem and its proof are in Section 5.4.
16      Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

Theorem 1 (Componentwise Decomposition). Assume the three trusted
components of Section 3.2. If every pollable in the runtime preserves obligations
when yielding (Definition 2, (P3)) and every reactor is responsive (Definition 3),
then the runtime satisfies Eventual Progression (Definition 1).
   The focus of Section 5 is to define new and efficient modular static analyses
whose success implies these required properties. We design abstract domains
and tailored verification conditions VC π (for pollables) and VC R (for reactors)
that, when discharged on the syntactic body of a component, imply that the
component is responsive.

5     Static Analysis of Eventual Progression
This section defines novel static analyses presented in an abstract-interpretation
style that verify the componentwise properties defined and motivated in the pre-
vious section. Our abstract domains are novel in that they focus on the notions
of monotonic predicates and undischarged obligations. Section 5.1 introduces
a novel unified abstract domain shared by both analyses; Sections 5.2 and 5.3
define analysis-refined pollable and reactor verification conditions; Section 5.4
states the soundness theorem and lifts the componentwise guarantees to a user-
facing runtime-responsiveness theorem.

5.1   Abstract Domain
We design an abstract domain which tracks two kinds of information at each
program point: observations on monotonic predicates, and symbolic obligations
abstracting over sets of concrete obligations held by reactors (their repositories).
    We define abstract states σ = (S, R,  b ∈ State, where S is a map tracking
                                        b L)
predicate observations, R is a map symbolically tracking obligations stored in
                          b
public repositories, and L b a set tracking locally-held symbolic obligations. We
explain each component formally below.
    States are ordered pointwise. The join ⊔ takes the pointwise lub of S, point-
wise union of R,b and union of L.  b The bottom element ⊥State represents an
unreachable program state. ⊥State ⊔ σ = σ for any abstract state.
    Predicate observations. We use the set Obs = {⊥, tt, ff, ⊤} for predicate
observations. tt means p has been observed to hold; ff means p was observed not
to hold at an earlier moment; ⊤ is unknown; ⊥ means unreachable.
    Two operators are defined over Obs: the refinement operator ▷ updates an
observation along a single execution path (defined below); the join ⊔ merges
observations from multiple paths, taken as the least upper bound on the ordering
⊥ ⊑ tt, ff ⊑ ⊤ (where tt and ff are incomparable and tt ⊔ ff = ⊤).
    The monotonic refinement operator ▷ : Obs × {tt, ff} → Obs updates a prior
observation by a fresh observation result (e.g., a branch of an if-statement) along
a single path, encoding the monotonicity of predicates:
                  tt ▷ tt = tt      ff ▷ tt = tt      ⊤▷v =v
                  tt ▷ ff = ⊥        ff ▷ ff = ff     ⊥▷v =⊥
                Modular Responsiveness Verification of Rust Async Runtimes                     17

T [s] : State → State

                  T [skip](σ) = σ
                                                                
           T [trigger(p)](σ) = σ S := S[p 7→ S(p) ▷ tt]
                                                                              b \ {(ŵ, _, _)}
                                                                                              
       T [insert(r, ŵ, p̂)](σ) = σ R(r)
                                     b      := R(r)
                                                  b    ∪ {(ŵ, p̂, τ )}, L
                                                                         b := L
                                   if (ŵ, p̂, τ ) ∈ L
                                                     b ∧ p̂ ∈ img(cp ); otherwise ⊥State
                                                                         r

              T [wake(ŵ)](σ) = σ L := L \ {(ŵ, _, _)}
                                                               
                                     b       b
                                   if (ŵ, _, _) ∈ L; b otherwise ⊥State
 T [if p then s1 else s2 ](σ) = σs1 ⊔ σs2
                  where σs1 = T [s1 ] σ S := S[p 7→ S(p) ▷ tt]
                                                                
                                                                
                          σs2 = T [s2 ] σ S := S[p 7→ S(p) ▷ ff]
                 T [s1 ; s2 ](σ) = T [s2 ](T [s1 ](σ))
             T [return v](σ) = ⊥State


Fig. 6: Transfer functions for the shared statements of LART . All transfer func-
tions preserve ⊥State , i.e., T [s](⊥State ) = ⊥State for every s.



If the value of a predicate is unknown ⊤, it can be refined into a concrete
observation (either tt or ff). A ff observation can be refined to tt, while refining
tt into ff violates monotonicity, indicating the current path is unreachable.
    ⊥ cannot be refined to any other values. We adopt a smash-product conven-
tion for abstract states: if S(p) = ⊥ for any p, the entire state σ is identified as
the bottom ⊥State . Intuitively, this means any observation that violates mono-
tonicity reveals an infeasible path; our analyses rely on this insight to prune
infeasible paths.
    Symbolic obligations. Let Waker    \ be a set of symbolic wakers. A symbolic
                                                \ × P × {tt, ⊤}. We use tag
                                           c ≜ Waker
obligation is a triple ô = (ŵ, p̂, τ ) ∈ Ob
τ to distinguish different assumptions about predicate p̂’s state at the start of
analysis: tag tt indicates p̂ is assumed to hold; ⊤ indicates p̂’s state is unknown.
Rb : Repo → ℘(Ob)  c maps each public repository to the symbolic obligations
currently stored in it; Lb ∈ ℘(Ob)c collects the symbolic obligations held locally
(taken out of a repository, or initialized at the start of the analysis).
    Transfer functions. Figure 6 defines the transfer function T [s] for LART
statements that are shared between pollables and reactors. trigger(p) refines
S(p) to tt. insert moves an obligation from Lb into R(r),
                                                    b     requiring the obligation
to be held locally and matching the repository’s typing. wake consumes a locally-
held obligation. if p refines S(p) on each branch via ▷ and joins the two results
after the statement. return v yields ⊥State , as the execution is terminated.
    insert, take, and wake yield ⊥State when side-conditions fail; this models
infeasible paths due to e.g., type mismatches or exceptions.
18         Yanze Li, Ivan Beschastnikh, and Alexander J. Summers


                                                                                                    
                 T [take(r, ŵ)](σ) = σ R(r)
                                         b      := R(r)
                                                      b    \ {(ŵ, p̂, τ )}, L    b ∪ {(ŵ, p̂, τ )}
                                                                             b := L
                                       if (ŵ, p̂, τ ) ∈ R(r);
                                                         b      otherwise ⊥State
     T [for (w, p) in r { s }](σ) = T [sk ]( · · · T [s1 ](σ))
                                     where R(r)  b     = {(ŵ1 , p̂1 , τ1 ), . . . , (ŵk , p̂k , τk )}
                                             and si ≜ s[ŵi , p̂i /w, p].


               Fig. 7: Transfer functions for reactor-only LART statements.


   Figure 7 extends the transfer functions to reactor-only statements take and
for. take moves an obligation out of a public repository and holds it locally;
for (w, p) in r is unrolled for every symbolic obligation in R(r).
                                                               b     The w and p
mentioned in the loop body are substituted with the ŵi and p̂i of each obligation.

5.2      Pollable Analysis Verification Conditions
We analyze each pollable implementation π twice, running our transfer function
with two different initial states, defined as follows (in which ŵ and p̂ are symbolic
waker and completion predicates):
    ⊤
 – σstart : Sstart (p̂) = ⊤, Lb start = {(ŵ, p̂, ⊤)}, Rbstart (r) = ∅ for all r;
 – σstart : Sstart (p̂) = tt, Lstart = {(ŵ, p̂, tt)}, otherwise identical.
    tt                        b

For a well-formed pollable body, every path terminates with a return, so the
abstract state immediately before each return summarizes what is known about
Σ and the entry obligation at that exit point.
   Verification conditions. VC π (π) checks the abstract state immediately
before each return site of π:
 – (P1vc ): under σstart
                   ⊤
                         , at every return Ready(v): S(p̂) = tt;
 – (P2vc ): under σstart
                   tt
                         , every reachable return site is a Ready-return;
 – (P3vc ): under σstart , at every return Pending: L
                   ⊤                                  b end = ∅.

The three checks discharge (P1), (P2), and (P3) of Definition 2, respectively.
(P3vc ) witnesses that the locally-held obligation has been transferred to a public
repository (via insert) or discharged (via wake) by the time the pollable yields.

Example: The Timer pollable in Section 3.1 can be modeled in LART as

        πtimer ≜ λ(w, pc ).
                      insert(A, w, pc ) ;
                      if pc then { return Ready(()) } else { return Pending }

where pc ∈ Pext is the timer’s completion predicate (i.e., self.instant <= now())
and A is the Reactor’s public repository.
                Modular Responsiveness Verification of Rust Async Runtimes              19

    When running the analysis with σstart
                                       ⊤
                                           , insert(A, w, pc ) moves the entry obli-
gation (ŵ, pc , ⊤) from L
                         b to R(A),
                              b     leaving Lb = ∅. The if statement refines the
state of pc to S(pc ) = tt on the then-branch and S(pc ) = ff on the else-branch.
On the then-branch we reach return Ready(()) with S(pc ) = tt, discharging
(P1vc ). On the else-branch we reach return Pending with L     b end = ∅, discharg-
ing (P3vc ).
    When running the analysis with σstart tt
                                               : the else-branch refinement gives
S(pc ) = tt ▷ ff = ⊥, so only the Ready-return is reachable, discharging (P2).
VC π (πtimer ) holds.


5.3     Reactor Analysis Verification Conditions

For each public repository r of type (Tr , cp r ), we analyze the reactor implemen-
tation from an initial R
                       bstart (r) with two symbolic obligations:

                            (ŵrtt , p̂tt
                                       r , tt),   (ŵr⊤ , p̂⊤
                                                            r , ⊤),

where p̂ttr , p̂r ∈ img(cp r ). The initial observation function is Sstart (p̂r ) = tt and
                ⊤                                                              tt

Sstart (p̂r ) = ⊤; Lstart = ∅. The tt-tagged obligation models the case where the
          ⊤          b
completion predicate already holds before the iteration (for checking (R1)); the
⊤-tagged obligation models the case where the predicate’s state is unknown (for
checking (R2)). Given a reactor body loop s, the analysis runs once on s with
the initial state σstart . Tt computes the end-of-iteration state σend = T [s](σstart )
and no fixpoint over loop is needed.
    Verification conditions. VC R (s) inspects σend and quantifies over the
symbolic obligations seeded at iteration start.

 – (R1vc ): for every ô = (ŵ, p̂, tt) ∈ R                  b end and ô ∈             ′
                                            bstart (r), ô ∈                S b
                                                           /L             / r′ R  end (r ).
 – (R2vc ): for every ô = (ŵ, p̂, ⊤) ∈ R  bstart (r), ô ∈
                                                           /Lb end .

VC R (s) ≜ R1vc ∧ R2vc . R1vc witnesses that all obligations whose predicates
hold at iteration start have been consumed by wake and removed from public
repositories. R2vc witnesses that obligations with unknown predicates are either
discharged by wake (hence absent from L    b and every R)
                                                       b or preserved in some
public repository for future iterations.

Example: The Timer Reactor of Sec. 3.1 can be encoded in LART as

      Rtimer ≜ reactor { shared A : (Timer , cp A ) in
                              loop for (w, p) in A {
                                 if p then { take(A, w) ; wake(w) } else skip }}

    We initialize the repository map R   bstart with the two symbolic obligations
introduced above, i.e., R
                        bstart (A) = {ôtt , ô⊤ } and set the local obligation set to
empty Lb start = ∅.
20      Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

    The for-rule instantiates the body once per symbolic obligation. For the
instantiation with ôtt , since we assumed S(p̂tt ) = tt at iteration start, the else-
branch refines to ⊥State ; only the then-branch survives. take(A, ŵtt ) moves ôtt
into Lb and subsequently ôtt is consumed by wake(ŵtt ). After the if-statement,
R(A) = {ô⊤ } and L
 b                 b = ∅.
    For the instantiation with ô⊤ , both branches survive; the join unions R  b and
b After the for-loop, we have R
L.                                bend (A) = {ô⊤ } (contributed by the else-branch)
and Lb end = ∅.
    We see that the symbolic obligation ôtt is not in L    b end or R
                                                                     bend (A) by the
end of the iteration, hence R1vc holds. Meanwhile, obligation ô only exists in
                                                                     ⊤

Rbend (A), hence R2vc holds and the reactor is verified.


Example (buggy): Now consider a buggy implementation of the same reactor
obtained by replacing the then-branch’s wake with skip (the reactor takes the
obligation out of A but forgets to wake it). The iteration with obligation ôtt never
discharges the obligation in the then-branch, leaving ôtt ∈ L  b end , hence failing
R1vc .


5.4   Soundness

In this subsection, we state the key soundness theorems and provide proof
sketches for them. We first show that the verification conditions soundly ap-
proximate the responsiveness properties for pollables and reactors as we defined
in Definition 2 and Definition 3.

Theorem 2 (Pollable Soundness). Let π be a pollable in LART . If VC π (π)
holds, then π is responsive (Definition 2).


Proof sketch. The transfer functions defined in Fig. 6 simulates the concrete
semantics in Fig. 5: the abstract state at every program point over-approximates
the concrete state.
   (P1) follows because VC π enforces S(p̂) = tt at every Ready-return site,
which by simulation gives p ∈ Σ in every concrete trace. (P2) follows because,
when S(p̂) is initialized to tt, VC π rules out reaching any Pending-return site, so
concrete executions starting with p ∈ Σ at entry must return Ready. (P3) follows
because VC π enforces L   b end = ∅ at every Pending-return site; an obligation
can only leave L either via insert (placing it in R)
                 b                                     b or wake (firing w), so by
simulation the concrete trace either transfers (w, p) to a public repository or fires
w before returning Pending.

Theorem 3 (Reactor Soundness). Let R be a reactor in LART whose body is
loop s. If VC R (s) holds, then R is responsive (Definition 3).
               Modular Responsiveness Verification of Rust Async Runtimes           21

Proof sketch. By simulation, σend = T [s](σstart ) over-approximates every con-
crete iteration-end configuration. The symbolic obligation ôtt over-approximates
all obligations whose monotonic predicates hold at the start of an iteration. R1vc
implies that the iteration both removes all corresponding obligations from ev-
ery public repository (via take) and consumes them locally (via wake), so the
concrete wakers are in Wake i (the set of wakers being woken up in iteration i);
therefore (R1) holds.
    ô⊤ over-approximates both obligations present at iteration start (preserved
from previous iterations) and those inserted concurrently during the iteration.
R2vc implies that, on every path, such concrete obligations are either discharged
via wake or preserved in some public repository, satisfying (R2).

Theorem 4 (Reactor Eventual Progression). Let loop s be a verified re-
actor and (w, p) an obligation ever placed in one of its public repositories; the
following holds
                            □ p ∈ Σ ⇒ ♢w ∈ Q .
                                                  


Proof sketch. Theorem 3 gives that verified reactors satisfy Definition 3. By
(R2) of Def. 3, (w, p) is preserved at every iteration end, so it will remain in
some public repository from when it was first inserted until wake(w) fires. By
monotonicity of the predicate p, once p ∈ Σ it remains so; since the reactor
iterates infinitely often, there will be an iteration j at whose start p ∈ Σ, and
(unless wake(w) has already been called) (w, p) will be still present in some
repository. By (R1) of Def. 3, w will be woken up at iteration j, i.e., w ∈ Wake j ,
and by the (wake) rule in Fig. 5, eventually w ∈ Q. This discharges Definition 1
case (b).
    Theorems 2 and 4 together establish the runtime side of Eventual Progres-
sion: every obligation introduced into the runtime, whose monotonic predicate
eventually holds, eventually has its waker fired. Combined with the three trusted
components of Section 3.2 (a fair scheduler, a correct compiler, and a respon-
sive environment), the runtime delivers the end-to-end responsiveness property
below.

Theorem 5 (Runtime Responsiveness). Suppose every reactor and every
pollable in the runtime satisfies its verification condition, async-task compilation
is faithful, the scheduler is fair, and the external predicates a task depends on
eventually hold. Then every async task running in this runtime eventually makes
progress.

Proof sketch. Faithful compilation transforms every async function into a state-
machine pollable whose poll method delegates to the awaitees’ poll method.
   By induction on the depth of nested awaits, the base case (a task awaiting
a runtime pollable) follows from Theorems 2 and 4.
   For the inductive case (a task t awaiting a sub-task t′ ), πt ’s poll invokes πt′ ’s
poll. The inductive hypothesis gives that πt′ eventually returns Ready; faithful
compilation propagates the result to πt , which continues past the await.
22      Yanze Li, Ivan Beschastnikh, and Alexander J. Summers


                                                   #                ”
      Reactors    R ::= . . . | t-reactor { shared rs : (Trs , cp rs ) in s }   (wfr (s))

                            
T [insert(r, ŵ, p̂)](σ) = σ S(tfr ) := tt, R(r)
                                            b    := R(r)
                                                    b    ∪ {(ŵ, p̂, τ )},
                              L := L \ {(ŵ, _, _)}
                                                    
                              b       b
                            if (ŵ, p̂, τ ) ∈ L
                                              b ∧ p̂ ∈ img(cp ); otherwise ⊥State
                                                             r

                 σ|p7→ff = σ S(p) := S(p) ▷ ff, ≺ := (≺ ∪ {(q, p) : q ̸= p, S(q) = tt})+
                                                                                        



Fig. 8: Extensions for terminating reactors. A new t-reactor syntax construct.
Two new cases of the transfer function for the strict-obligation-transfer (SOT)
extension: insert records the transfer event tfr , and refining a predicate to ff
extends ≺ (X + denotes transitive closure). The state smashes to ⊥ if S(p) ▷ ff =
⊥; all other forms are unchanged.


Corollary 1 (Responsiveness Attribution). If an async task is observed to
hang at a program point, at least one of the trusted components must have failed,
or the user’s code itself has unintended non-termination or deadlocks indepen-
dently of the runtime’s pollables. The verified pollable and reactor implementa-
tions provided by the async runtime cannot be the cause.

The corollary above is the contrapositive of Theorem 5. In practice, our analyses
rule out async runtime’s implementations as the cause of responsiveness issues.


5.5   Extension 1: Terminating Reactors and Precedes Relations

Our model so far requires a reactor to run an infinite loop over its repositories,
which is the most-common idiom. In this subsection we show an adaptation of
our techniques to support reactor-like components which handle only finitely
many wakers, and can thus justify termination.
    This idiom of terminating reactors arises in practice e.g., in the implementa-
tion of the receiving end of a one-shot channel. The receiver is an async future
awaiting a value, while its peer code send is an ordinary synchronous function.
Calling send delivers the value and wakes the suspended receiver, which is exactly
the obligation a reactor discharges. We can see send as playing a reactor-like role,
despite being a single function call rather than an event loop.
    Two things set such a reactor apart from those of Section 4. First, it discharges
a finite, bounded collection of obligations rather than an unbounded stream: a
one-shot channel has at most one receiver to wake. Second, it runs a statically
bounded number of times (one, in this example) and then terminates. Rust’s
ownership discipline consumes the sender, so send fires at most once per channel;
after that single invocation the reactor is dead, and any obligation registered
afterwards can never be discharged. We model this as a terminating reactor
t-reactor (Fig. 8), whose body s runs to completion once per invocation, with
               Modular Responsiveness Verification of Rust Async Runtimes           23

no enclosing loop. Its well-formedness predicate wfr is that of a regular reactor
(Section 4.1), minus the required outermost loop.
    Verifying a t-reactor reuses most of our existing design with only modest
adaptation. VC R and the abstract domain are unchanged, with (R1) and (R2)
of Definition 3 read per invocation rather than per iteration; Reactor Soundness
(Theorem 3) transports directly, since its proof already reasons about a single
execution of the body.
    Reactor Eventual Progression (Theorem 4), by contrast, does not translate
as directly. Recall that its proof relies on the reactor iterating infinitely often: an
obligation is preserved across iterations by Definition 3 (R2) and woken by (R1)
at some later iteration when its predicate holds. A terminating reactor runs only
once, so an obligation inserted after that single invocation is preserved by (R2)
but never discharged.
    Progression therefore holds only for obligations whose transfer strictly pre-
cedes termination of the reactor. The observation function S in the current
abstract state cannot witness this alone: a receiver that re-checks completion
after transferring its obligation and one that does not both reach Pending with
the same observation S(pc ) = ff.
    Building on our first-class notion of monotonic predicates, we extend the
abstract domain of Section 5.1 with a precedes relation ≺ ⊆ P ×P: a strict partial
order representing observed temporal order between two monotonic predicates.
In particular, p ≺ q means there exists a moment with p ∈ Σ and q ∈          / Σ. This
relation (and its transitive closure) can be efficiently maintained by our analysis.
    We extend abstract states with an additional set ≺ to capture all the observed
precedes relations, i.e., σ = (S, ≺, R,  b The set ≺ joins by intersection, keeping
                                      b L).
only orderings established on all incoming paths.
    We additionally initialize S with a dedicated monotonic predicate tfr for
“the obligation has been transferred to the reactor”. The strict obligation trans-
fer (SOT) condition is tfr ≺ pc : the obligation must be transferred before the
completion predicate holds.
    The precedes relations can be tracked via two updated transfer rules, pre-
sented in Fig. 8 with no new annotation. First, insert(r, w, p) means the obliga-
tion has been transferred to a reactor; therefore, besides moving the obligation
to R(r),
    b      we also set S(tfr ) = tt. Second, refining S(p) to ff (e.g., by entering
the else-branch of an if-statement) extends ≺ with q ≺ p for every q already
observed to be true (S(q) = tt).
    Let Term ⊆ Repo denote the set of repositories owned by terminating re-
actors. The pollable verification condition VC π is strengthened by a check on
strict-obligation-transfer that fires only when the pollable transfers its entry
obligation into some r ∈ Term:
 – (SOTvc ): under σstart
                    ⊤
                          , at every reachable return Pending such that (ŵ, p̂, _) ∈
   R(r)
   b    for some r ∈ Term: tfr ≺ p̂.
A re-checking receiver that performs insert (refining S(tfr ) to tt) followed by a
re-check (refining S(pc ) to ff) now records the precedes relation tfr ≺ pc , hence
satisfying (SOTvc ); a non-re-checking receiver will fail (SOTvc ).
24      Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

Theorem 6 (Terminating Reactor Eventual Progression). Let r be the
repository of a terminating reactor whose body s satisfies VC R (s), and let (w, p)
be an obligation inserted into r by a pollable satisfying SOTvc for r. If the host
invokes the reactor, then

                            □ p∈Σ ⇒ ♢w∈Q .
                                                     


Proof sketch. SOTvc gives tfr ≺ p: the registration of w into r strictly precedes
p entering Σ. The host’s invocation establishes p (it triggers p, or observes it
already tt) and, by VC R (s)/(R1), takes and wakes every obligation in r whose
predicate holds. Since w was registered strictly before p, (w, p) is present in r at
invocation time; (R1) fires wake(w), and by the (wake) rule eventually w ∈ Q. A
single invocation thus replaces the “iterates infinitely often” step of Theorem 4.
    The proof leaves one assumption uncovered, mirroring the regular reactor’s
reliance on its external predicates eventually holding: the host must eventually
invoke the terminating reactor (e.g., call send). If a one-shot channel is never sent
on, its receiver legitimately waits forever, a user-level failed obligation rather
than a runtime fault.

5.6   Extension 2: Fixpoint for Pollable Retry-loops
The base language requires pollable bodies to be loop-free (wfp, Section 4.1).
Sometimes, however, pollables themselves contend for bounded shared resources
(a channel slot, a mutex permit), following a try-wait-retry cycle: attempt to
acquire the resource; on failure, insert a waker and yield; on wake, retry. The
reinvocation of pollables on wake only implies that the contended resource may
now be available, but success on the second call is not guaranteed.
    Our modular analysis techniques do not support this pattern as described,
which would require some kind of analysis around the implicit loop illustrated in
Fig. 1. However, a variant of this pattern which we have encountered in practice
is to use an explicit try-wait-retry loop in the pollable implementation itself; we
describe here an extension which supports this case.
    To support such retry-loops, we can admit loop in pollable bodies and dis-
charge it with a fixpoint; VC π , both initial states, and the other transfer rules
of Section 5 are unchanged. The well-formedness condition wfp is relaxed ac-
cordingly: loop s is admitted in any statement position, and the body s must
contain at least one return, so that the loop exit is reachable. Our analysis does
not attempt to check termination of this loop, which ultimately depends on an
external predicate eventually holding; instead, this extension to pollable loops
checks that provided the loop eventually terminates, the necessary obligations
will be satisfied.
    Our fixpoint analysis converges because the abstract domain is a finite com-
plete lattice and the transfer function is monotone. For any pollable, the mono-
tonic predicates, symbolic wakers, and repository names appearing in the pol-
lable body are finite. Therefore, the symbolic obligations Ob        \ ×P ×
                                                              c ⊆ Waker
{tt, ⊤} and the space of observation maps S are also finite. The state space
                                                                                                      (wake)
                                    wake(w) | (ε, (ϑ, Q, R)) →↑p skip | (ε, (ϑ, Q ↔ {w}, R))
                                                     →
                                                   R = R[r ↗↑ R(r) ↔ {(w, p)}]
                                                                                                      (insert)
                                    insert(r, w, p) | (ε, (ϑ, Q, R)) →↑p skip | (ε, (ϑ, Q, R→ ))

                                                          (w, p) ↓ R(r)
                                                    R→ = R[r ↗↑ R(r) \ {(w, p)}]
                                                                                                    (take)
                                       take(r, w) | (ε, (ϑ, Q, R)) →↑p skip | (ε, (ϑ, Q, R→ ))

                                                               p↓ϑ
                                                                                           (if-t)
                                                 if p then s1 else s2 | ω →↑p s1 | ω
                       Modular Responsiveness pVerification
                                               ↓
                                               /ϑ           of Rust Async Runtimes                                                   25
                                                                                           (if-f)
                                                 if p then s1 else s2 | ω →↑p s2 | ω

Annotated
                  Rust compiler                    R(r) = {(w1 , p1 ), . . . , (wk , pkVerification
                                                                                       )}
Rust code                                             si ↭ s[wi , pi /w, p] k ↘ 1
                                                                                                     (for)
                                        for (w, p) in r { s } | (ε, G) →↑p s1 ; · · · ; sk Verify
                                                                                            | (ε, G)
 func()             High-level IR          Mid-level IR       Binary                   reactors
                       (HIR)                  (MIR)     R(r) = ⊋                                                           Failure
                                                                                              (for-emp)      Composition
                                        for (w, p) in r { s } | (ε, G) →↑p skip | (ε, G)                       Analysis
                                                                                 Verify
            - Annotation expansion                                                                                         Success
                        Fig. 5: Small-step semantics  for LART . Standard rules pollables
                                                Extract                         such as sequencing or skip
            - Spec extraction
                        are omitted; the full definition is in Appendix B.



            Fig. 9: Jackdaw
                         assumedesign.     The green
                               all waker-predicate pairs in aboxes
                                                             repositoryare   parttheofrepository
                                                                        r respect        Jackdaw.
                                 typing, i.e., every (w, p) → R(r) has p → img(cp r ), where img denotes
                                 the image of the predicate scheme cp r .

(State, ⊑, ⊔, ⊥State ) is therefore a finite, complete lattice, with ⊔ monotone in
both arguments. Monotonicity              of T [s] follows by structural induction on s: every
                     Figure 5 defines the operational semantics for LART . trigger, insert, take,
rule of Fig. 6 is and
                   built
                      wakefrom      monotone
                            are atomic               operations
                                        e!ectful statements  that updateontheObs
                                                                               globaland    ℘(Ob).
                                                                                      state and  re-
                                                                                                 c
                  duce to skip. if statements branch on whether a predicate is recorded in the
    The transfermonotonic
                   function       definitions
                             history                extend
                                     ω. for statements          with
                                                        iterate over     one
                                                                     every      new
                                                                           (w, p)      case
                                                                                  in R(r)      for loops:
                                                                                          presented
                         at the start of the for-loop. We omit other conventional rules for loop, skip, etc.
                                T definition
                         The full  [loop iss](σ)        = ⊥
                                                in Appendix  B.State ,
                            An async runtime additionally  rely on other trusted components and the
                                               h∗ ≜ lfp
                                                                                                         
                                                               h 7→ σ ⊔ T [s](h) .
                         external environment that are not modeled by LART . We model them via two

Here h∗ is the abstract state computed as the fixpoint above. A loop exits only
through a return, so its result state is ⊥State ; the return-site states that VC π
inspects are gathered from inside s during the evaluation of T [s](h∗ ), exactly as
the base analysis collects them for non-loop bodies, just with h∗ in place of the
pollable’s entry state. The body’s transfer T [s](h) collects exactly the loop-back
paths because any return inside s yields ⊥State , the identity of ⊔. The chain
h0 = ⊥State , hn+1 = σ ⊔ T [s](hn ) ascends and stabilizes in finitely many steps.
This generalizes to nested loops because monotonicity of the body’s transfer is
preserved by structural induction.
    The proof of Pollable Soundness (Theorem 2) has a new case for the loop.
By induction on the iteration number, every concrete state at the loop head
is abstracted by h∗ : the entry state by σ ⊑ h∗ , and any future-iteration state,
obtained by running the body once from a previous state, by T [s](h∗ ) ⊑ h∗ .
Return-site observations collected under h∗ therefore over-approximate those of
every concrete iteration, so VC π remains sound.

6     The Jackdaw Tool and Evaluation
We implement our technique as a prototype, Jackdaw, in roughly 5k lines of
Rust. Jackdaw is designed as a Rust compiler plugin [5]; see Figure 9. Jack-
daw enables modeling pollables/reactors of Rust async runtimes in LART via
annotations and extracts an explicit LART model out of Rust’s intermediate
representation (Middle-level IR, MIR). The extracted model can be manually
inspected, and also automatically verified against VC π and VC R as described
in Section 5. In Sec. 6.1 we use Jackdaw to evaluate (1) the expressiveness of
LART by modeling real-world pollables and reactors, and (2) the effectiveness of
our static analyses.
26     Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

    Users model a pollable/reactor as an instance of LART through a macro li-
brary that overlays LART constructs on Rust code. Macros expand to no-op
markers in MIR for model extraction. The annotated Rust code compiles and
behaves identically to the original. The macro syntax mirrors LART : mono_pred!
declares a monotonic predicate; obs!, obs_tt!, and obs_ff! record observations
on predicates; trigger!, wake!, insert!, and take! mark the corresponding ef-
fects; and repo_for! marks iteration over a repository. The entry points of pol-
lables/reactors are tagged with #[jackdaw::pollable] and #[jackdaw::reactor],
and bind! binds the LART parameters of a component (its waker, completion
predicate, and public repositories) explicitly rather than having them inferred.
    Jackdaw traverses the MIR of annotated functions, captures the control-
/data-flows and user annotations, and lifts the pollable/reactor implementations
into LART . The lifting from MIR to LART is not formalized and contains heuristics
(e.g., recovering nested branches and loops from a CFG).
    The LART formalized in Sec. 4 and the static analyses described in Sec. 5
are fully implemented (including the extensions). We add an assume statement
assume(p, b) that refines a predicate p to a specific value b without branching,
and a nondeterministic choice nd-match for more straightforward translation
from Rust.

6.1   Evaluation
We evaluate Jackdaw on a representative subset of components drawn from
three Rust async runtimes: smol [25], futures [8], and tokio [28]. These span the
three building blocks of async programs: scheduling (timers), I/O, and commu-
nication (one-shot and MPSC channels). Tables 1 and 2 list every verified com-
ponent with its source size (LoC, excluding blank lines and comments), total
annotation cost (Anno LoC; Ratio = Anno / LoC), and per-component analy-
sis time, the cost of lifting to LART and discharging the verification conditions,
measured as the mean of 300 runs. Experiments ran on a 2.30 GHz Intel Core
i9-9880H with 32 GB RAM under rustc 1.91.0-nightly.
    Effectiveness. For each verification condition (P1/P2/P3 of VC π , R1/R2
of VC R , and the strict-obligation-transfer condition from Section 5.5), we seed a
violation in a real component and confirm Jackdaw rejects it; no false negatives
are observed across the suite.
    Specification burden. Each pollable verifies with 4 to 11 lines of annota-
tion, giving an annotation-to-code ratio of 23% on average. Every pollable in the
suite is specified with a single monotone predicate. Terminating reactors show
a higher ratio because of their short implementations (≤ 13 lines).
    Imprecision/Code modification. We encountered three cases where ad-
ditional annotations or source code modifications are needed to overcome Jack-
daw’s imprecision or limitations. 1. Post-join re-assertion is needed when a com-
pletion decision is carried in a boolean flag across control-flow merges. This is a
precision limitation of our abstract domain. 2. Our model cannot handle tokio’s
fairness mechanism, which requires pollables to cooperatively yield. We use a
special annotation in Jackdaw, ignore_path!, to prune such unsupported code
               Modular Responsiveness Verification of Rust Async Runtimes              27


                  Table 1: Verification statistics for pollables.
                                                  Anno                       Analysis
Pollable                  Runtime       LoC                        Ratio
                                                  LoC                        time (µs)
EventListener               smol            15          5          33%         24.6
MPSC-send                   smol            28          6          21%         68.0
MPSC-recv                   smol            27          6          22%         63.2
MPSC-close                  smol            21          4          19%         39.0
AsyncIO-Read/Write          smol            29          6          21%         99.5
AsyncIO-Ready               smol            38          5          13%         86.2
OneShot-recv               futures          23          8          35%         82.8
OneShot-recv                tokio           59         11          19%         152.2
OneShot-closed              tokio           45         10          22%         111.1



                  Table 2: Verification statistics for reactors.
                                                            Anno              Analysis
Reactor            Runtime           Kind        LoC                 Ratio
                                                            LoC               time (µs)
Timer / AsyncIO       smol        looping        59          11       19%       38.5
OneShot-recv         futures    terminating      12           7       58%       10.9
OneShot-recv          tokio     terminating      12          7        58%        9.9
OneShot-closed        tokio     terminating      13          7        54%       10.6



paths. 3. Tokio’s OneShot-recv pollable contains paths requiring cross-invocation
invariants to justify their returns; this requires additional ghost annotations to
establish such invariants.
    Overhead. Per-component analysis is sub-millisecond throughout (10 to
152 µs; Tables 1 and 2). Lifting dominates and scales with control-flow complex-
ity; the heaviest case is tokio’s one-shot receiver with its coop/will_wake/state
branches at ≈152 µs, while reactors are 10 to 40 µs. These costs are negligible
relative to Rust compilation, making Jackdaw suitable for integrating more
expensive analysis/verification techniques.


7   Limitations and Future Work

We discuss some of the current limitations and potential future work for our
technique and its prototype implementation. Known gaps in the existing model
of LART include: a wake-one primitive (non-deterministically discharge one obli-
gation in a repository) for single-permit synchronization idioms (e.g., tokio’s
Mutex, Semaphore), and cross-poll reasoning that would let invariants established
in a prior poll discharge later checks.
    Sound extraction of LART models. Our soundness theorems are stated with
respect to LART , but real programs are written in Rust. Jackdaw bridges the
two by lifting MIR to LART using a (currently trusted but fairly straightforward)
28      Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

translation of control flow, and, crucially, trusted user-supplied annotations. In
particular, Jackdaw does not check for mistakes in these annotations, such
as triggering a monotonic event when the corresponding update has not been
performed in the real memory. We plan to investigate scalable approaches to close
this gap or reduce the chance of errors in the user’s modelling, by integrating
other complementary static or dynamic analysis techniques.
    Fine-grained concurrency. All operations in LART , e.g., insert, take, and
wake are atomic operations under a sequential consistency model; our techniques,
and especially the precedes relation extension defined in Sec. 5.5 rely on sequen-
tial consistency. Real-world async runtime implementations such as tokio use
weaker atomic memory accesses for high performance; so far, we have not seen
examples in which extra observable behaviors could result, but our technique is
not checking this formally when such primitives are used; adding such checks
directly to our analyses in a way that matches the idioms used in this kind of
code might be possible in the future.
    Cancellation and task drop. Async tasks can typically be cancelled at any
await point, at which time any wakers the task has registered with reactors
must be reclaimed. Our model currently has no notion of obligation revocation
and no mechanism for a reactor to learn that a transferred obligation becomes
irrelevant; adding this to our operational semantics would be straightforward.
Although challenging in terms of general logic of user code, from the pollable
and reactor perspectives we believe this extension should be reasonably simple,
especially since wakers typically include logic to handle unnecessary extra calls.
    Safety and functional correctness. Our analyses currently only check that
obligations arisen from pollables managed by an async runtime are not lost, and
we assume properties such as panic-freedom (and type-correctness, in LART ). It
might be interesting in future to also be able to prove panic-freedom as well as
to provide a formal basis for more-general verification of functional properties
guaranteed by the runtime’s mechanisms. We believe LART could be used as a
basis for exploration of such techniques in the future.
    Bounded responsiveness. Finally, eventual progression is a specific respon-
siveness property that only asserts progress in the arbitrarily-far future. Users
typically care about finer-grained responsiveness properties, e.g., bounded la-
tency, tail latencies, and fairness across tasks of different priorities. Lifting our
technique to stronger responsiveness properties (given some reasonable timing
model) and/or trying to infer such guarantees would be interesting future work.


8    Related Work

Our work addresses the problem of verifying eventual progression, a liveness
property ensuring that asynchronous runtimes make progress and do not indefi-
nitely defer pending tasks. Some prior work has proposed approaches to reason
about user code [10,17,9,20] that relies on an async runtime. However, the under-
lying async runtime is typically considered part of the trusted computing base.
Instead, our work treats errors in user code (or other components such as the
               Modular Responsiveness Verification of Rust Async Runtimes         29

OS) as an orthogonal concern and focuses on critical runtime components that
almost all user code implicitly relies upon.
    Compositional Verification of Responsiveness. Our work takes inspi-
ration from Actor Services [26], which introduced a modular logic for verifying
responsiveness and functional correctness of purely-actor-based programs. Actor
Services employed a notion of logical obligations (reminiscent of “causal obliga-
tions” of Helm et al. [14]), to structure progress proofs under fair scheduling.
Again, they address verification of user code, while we focus on the more-specific
but crucial concern of the responsiveness of Rust async runtime components.
    We aim for similarly-modular reasoning to Actor Services, but our technique
differs in several important aspects. We can verify implementation strategies
that Actor Services cannot (in particular, reactor-like components which do not
discharge obligations immediately, but which promise progress in a different
fashion): reactors which handle multiple obligations in an interleaved fashion
cannot be verified with this prior work. We also identify and build in monotonic
events and their orderings as a first-class notion, which allows us to express subtle
requirements that cannot be captured as responsiveness properties directly. We
have also applied our technique to real-world code with Jackdaw, enabling
experimentation and evidence of potential impact in practice.
    Anvil [27] similarly tackles liveness reasoning in Rust systems but in a very
different setting. It provides a framework for verifying liveness properties of
Kubernetes controllers using TLA specifications embedded within Verus [18].
Anvil’s “Eventually Stable Reconciliation” (ESR) property is conceptually re-
lated to our notion of Eventual Progression. Anvil requires users to encode their
system logic manually in TLA and to prove ESR interactively within Verus. In
contrast, we automatically verify liveness guarantees of async runtimes through
lightweight specifications, rather than a user-driven proof framework.
    Obligations have been used in other verification contexts: Leino et al. [19]
proposed obligations as a first-class specification notion for enabling modular
proofs of deadlock-freedom. This idea was extended by Boström and Müller [4]
to enable verification of finite blocking for concurrent algorithms. These works
are aimed at user code and do not directly apply to our setting; conversely, the
simplifications afforded by our task-centric view or decomposition of responsi-
bilities across pollables and reactors cannot be directly exploited for user code.
    Verification for Rust Programs. Rust’s ownership model has motivated
a growing body of verification work. RustBelt [16] provides a foundational se-
mantics and verification technique based on Rust’s type system, and deductive
verifiers such as Prusti [2,1], Creusot [7], and Verus [18] support semi-automated
functional correctness proofs. These techniques primarily target improvements
to sequential reasoning made possible by Rust’s guarantees; our key reasoning
concepts of monotonic events and their orderings are novel. Of these, only Verus
has been applied to the Rust async setting, by Lion [30], discussed below.
   Cutner and Yoshida [6] formalize session-based async coordination of Rust
user code that uses async primitives such as channels. This helps prevent user
30      Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

code errors such as deadlocks; the responsibilities of the runtime are assumed in
such work (as standard), while our work addresses these responsibilities directly.
    Verification of Liveness / Async Runtimes. To our knowledge, the first
usage of monotonic predicates as a specific notion was in Hailpern and Owicki’s
pioneering work on modular specification and verification for liveness proper-
ties [13]. This work presents a wide variety of specification idioms and shows why
monotonic properties have useful properties at the boundaries between compo-
nents. We take this idea further and make monotonic predicates into first class
specification notions, along with the ability to specify and observe orderings of
them. In addition, we show how to connect our reasoning to concrete program
implementations.
    Model checking has been used extensively to verify liveness properties [3],
sometimes using variations of rely-guarantee style proof techniques [15] to sup-
port modular verification [12]. While these techniques allow abstracting over the
concrete interleavings of actions by other components, they do not provide the
abstraction or simplicity of our task-centric view.
    Liveness verification has been considered at the protocol level in the context
of session types by Padovani et al. [23]; this work does not connect to concrete
implementations or support modular specification of separate components.
    de Vilhena and Pottier develop a framework for separation logic reasoning for
effect handlers [29]. As part of the evaluation, they verified the safety property
of an async runtime built with effect handlers. They do not consider liveness of
async runtimes.
    Independently of our work, Zhou et al. [30] developed Lion, a clean-slate
Rust async runtime with Tokio-compatible APIs, and mechanically verified its
scheduling liveness in Verus [18]. Lion obtains verifiability by rebuilding the
runtime, at roughly 40k lines of specification and proof for 3.4k lines of code,
whereas Jackdaw checks components of existing production runtimes as writ-
ten, with lightweight annotations and automatic analyses. Our decomposition
from eventual progression into componentwise properties is proven once for ev-
ery runtime expressible in LART , whereas Lion composes module contracts per
runtime through cross-module predicates. Lion does not verify the pollables that
user code awaits. Its end-to-end proof assumes that a task returning Pending
has registered a wake source. Our verification considers properties of pollables,
the condition (P1) to (P3) defined in Sec. 4.3 discharge exactly this assumption.
Conversely, Lion verifies its executor, which we trust (Section 3.2), and its proofs
are machine-checked while our soundness argument is on paper.


9    Conclusion

This work takes a first step toward verifying the liveness guarantees of async
runtimes. Whereas prior research has primarily focused on verifying the safety
and correctness of async programs, we shift attention to the runtimes that are
responsible for ensuring that tasks eventually complete.
              Modular Responsiveness Verification of Rust Async Runtimes      31

    We developed a detailed yet generic model of Rust async runtimes that
captures how reactors, pollables, and schedulers cooperate to provide respon-
siveness. We formalized this model in a core language LART and identified two
component-level verification conditions whose conjunction soundly implies even-
tual progression of the runtime. We automated these checks in Jackdaw, a
compiler extension for Rust that uses lightweight annotations and static analy-
sis. Our evaluation on smol and tokio async runtimes demonstrates that, with
the two extensions of the core formalism, our approach verifies real pollable
and reactor components written with various common idioms, while catching
common responsiveness bugs.
    Ultimately, our work advances the goal of verified asynchrony: connecting the
high-level liveness guarantees expected by developers with the concrete behavior
of runtimes that implement them.
32      Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

References
 1. Astrauskas, V., Bílỳ, A., Fiala, J., Grannan, Z., Matheja, C., Müller, P., Poli, F.,
    Summers, A.J.: The prusti project: Formal verification for rust. In: NASA Formal
    Methods Symposium. pp. 88–108. Springer (2022)
 2. Astrauskas, V., Müller, P., Poli, F., Summers, A.J.: Leveraging Rust types for
    modular specification and verification. Proc. ACM Program. Lang. 3(OOPSLA),
    147:1–147:30 (2019). https://doi.org/10.1145/3360573, https://doi.org/10.
    1145/3360573
 3. Biere, A., Artho, C., Schuppan, V.: Liveness checking as safety checking. Electronic
    Notes in Theoretical Computer Science 66(2), 160–177 (2002)
 4. Boström, P., Müller, P.: Modular Verification of Finite Blocking in Non-terminating
    Programs. In: Boyland, J.T. (ed.) European Conference on Object-Oriented Pro-
    gramming (ECOOP). LIPIcs, vol. 37, pp. 639–663. Schloss Dagstuhl (2015),
    https://doi.org/10.4230/LIPIcs.ECOOP.2015.639
 5. Crichton, W., Adam, J., Gray, G., Coblenz, M.: rustc_plugin. https://github.
    com/cognitive-engineering-lab/rustc_plugin (2024)
 6. Cutner, Z., Yoshida, N.: Safe Session-Based Asynchronous Coordination in Rust.
    In: Damiani, F., Dardha, O. (eds.) Coordination Models and Languages. pp. 80–89.
    Springer International Publishing (2021)
 7. Denis, X., Jourdan, J., Marché, C.: Creusot: A foundry for the deductive verifica-
    tion of Rust programs. In: Riesco, A., Zhang, M. (eds.) Formal Methods and Soft-
    ware Engineering - 23rd International Conference on Formal Engineering Methods,
    ICFEM 2022, Madrid, Spain, October 24-27, 2022, Proceedings. LNCS, vol. 13478,
    pp. 90–105. Springer (2022). https://doi.org/10.1007/978-3-031-17244-1_6,
    https://doi.org/10.1007/978-3-031-17244-1_6
 8. futures-rs Contributors: futures-rs — zero-cost asynchronous programming in rust
    (2025), https://docs.rs/futures/latest/futures/, accessed: 2026-05-26
 9. Ganty, P., Majumdar, R.: Algorithmic verification of asynchronous programs. ACM
    Trans. Program. Lang. Syst. 34(1) (May 2012)
10. Ganty, P., Majumdar, R., Rybalchenko, A.: Verifying liveness for asynchronous
    programs. In: Proceedings of the 36th annual ACM SIGPLAN-SIGACT sympo-
    sium on Principles of programming languages. pp. 102–113 (2009)
11. Google: Listenablefuture (guava 21.0 api) (2017), https://guava.dev/releases/
    21.0/api/docs/com/google/common/util/concurrent/ListenableFuture.html,
    accessed: 2025-10-07
12. Grumberg, O., Long, D.E.: Model checking and modular verification. ACM Trans-
    actions on Programming Languages and Systems (TOPLAS) 16(3), 843–871 (1994)
13. Hailpern, B., Owicki, S.: Modular verification of concurrent programs. In: Proceed-
    ings of the 9th ACM SIGPLAN-SIGACT symposium on Principles of programming
    languages. pp. 322–336 (1982)
14. Helm, R., Holland, I.M., Gangopadhyay, D.: Contracts: Specifying behavioral com-
    positions in object-oriented systems. In: OOPSLA/ECOOP 1990. pp. 169–180
    (1990). https://doi.org/10.1145/97945.97967, http://doi.acm.org/10.1145/
    97945.97967
15. Jones, C.B.: Development methods for computer programs including a notion of
    interference. Oxford University Computing Laboratory (1981)
16. Jung, R., Jourdan, J.H., Krebbers, R., Dreyer, D.: Rustbelt: Securing the founda-
    tions of the rust programming language. Proceedings of the ACM on Programming
    Languages 2(POPL), 1–34 (2017)
                Modular Responsiveness Verification of Rust Async Runtimes            33

17. Kahlon, V., Sinha, N., Kruus, E., Zhang, Y.: Static data race detection for concur-
    rent programs with asynchronous calls. In: Joint Meeting of the European Software
    Engineering Conference and the ACM SIGSOFT Symposium on The Foundations
    of Software Engineering (ESEC/FSE). p. 13–22 (2009)
18. Lattuada, A., Hance, T., Bosamiya, J., Brun, M., Cho, C., LeBlanc, H., Srinivasan,
    P., Achermann, R., Chajed, T., Hawblitzel, C., Howell, J., Lorch, J.R., Padon, O.,
    Parno, B.: Verus: A Practical Foundation for Systems Verification. In: Symposium
    on Operating Systems Principles (SOSP). p. 438–454 (2024)
19. Leino, K.R.M., Müller, P., Smans, J.: Deadlock-free channels and locks. In: Gordon,
    A.D. (ed.) European Symposium on Programming (ESOP). LNCS, vol. 6012, pp.
    407–426. Springer-Verlag (2010)
20. Maiya, P., Kanade, A., Majumdar, R.: Race detection for Android applications. In:
    Proceedings of the 35th ACM SIGPLAN Conference on Programming Language
    Design and Implementation (PLDI). p. 316–325 (2014)
21. Mozilla Developer Network: Async functions — javascript | mdn (2025),
    https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/
    Statements/async_function, accessed: 2025-10-07
22. Oracle: Completablefuture (java platform se 8) (2014), https://docs.oracle.
    com/javase/8/docs/api/java/util/concurrent/CompletableFuture.html, ac-
    cessed: 2025-10-07
23. Padovani, L., Vasconcelos, V.T., Vieira, H.T.: Typing liveness in multiparty com-
    municating systems. In: COORDINATION 2014. LNCS, vol. 8459, pp. 147–162
    (2014). https://doi.org/10.1007/978-3-662-43376-8_10, http://dx.doi.org/
    10.1007/978-3-662-43376-8_10
24. Python Software Foundation: asyncio — asynchronous i/o — python 3.12.6
    documentation (2025), https://docs.python.org/3/library/asyncio.html, ac-
    cessed: 2025-10-07
25. Smol Contributors: smol — rust asynchronous runtime documentation (2025),
    https://docs.rs/smol/latest/smol/, accessed: 2025-10-07
26. Summers, A.J., Müller, P.: Actor services. In: European Symposium on Program-
    ming. pp. 699–726. Springer (2016)
27. Sun, X., Ma, W., Gu, J.T., Ma, Z., Chajed, T., Howell, J., Lattuada, A., Padon,
    O., Suresh, L., Szekeres, A., et al.: Anvil: Verifying liveness of cluster manage-
    ment controllers. In: 18th USENIX Symposium on Operating Systems Design and
    Implementation (OSDI 24). pp. 649–666 (2024)
28. Tokio Contributors: Tokio — rust asynchronous runtime documentation (2025),
    https://docs.rs/tokio/latest/tokio/, accessed: 2025-10-07
29. de Vilhena, P.E., Pottier, F.: A separation logic for effect handlers. Proceedings of
    the ACM on Programming Languages 5(POPL), 1–28 (2021)
30. Zhou, T., Zhang, Z., Chowdhury, O., Mu, S.: Lion: Modular Verification of Async
    Runtime Liveness. In: Proceedings of the ACM SIGOPS 32nd Symposium on Oper-
    ating Systems Principles (SOSP). pp. 636–655. Association for Computing Machin-
    ery, New York, NY, USA (2026). https://doi.org/10.1145/3830418.3843879
34      Yanze Li, Ivan Beschastnikh, and Alexander J. Summers

A    Well-formedness Conditions

This appendix gives the well-formedness predicates wfp (for pollable bodies) and
wfr (for reactor bodies) referenced in Section 4.1. They capture the programming
paradigm not reflected in the bare syntax of LART (Fig. 4).


Pollable bodies. A pollable π is a statement satisfying the well-formedness pred-
icate wfp: every execution path contains a return v statement, and the state-
ment contains no loop or reactor-only constructs, i.e., take and for. Formally,
wfp(s) ≜ returns(s) ∧ pollable-only(s), where:

                        returns(return v) = ⊤
                           returns(s1 ; s2 ) = returns(s1 ) ∨ returns(s2 )
           returns(if p then s1 else s2 ) = returns(s1 ) ∧ returns(s2 )
                                returns(s) = ⊥     otherwise


pollable-only(loop s) = pollable-only(take(r, w)) = ⊥
                pollable-only(for (w, p) in r { s }) = ⊥
                              pollable-only(s1 ; s2 ) = pollable-only(s1 ) ∧ pollable-only(s2 )
              pollable-only(if p then s1 else s2 ) = pollable-only(s1 ) ∧ pollable-only(s2 )
                                   pollable-only(s) = ⊤      otherwise


Relaxed pollable bodies (with loops). The loop extension admits loop s in pollable
bodies. The relaxed predicate wfp ′ (s) ≜ returns ′ (s) ∧ pollable-only ′ (s) replaces
the loop clauses of returns and pollable-only with

                          returns ′ (loop s) = has-return(s)
                    pollable-only ′ (loop s) = pollable-only ′ (s)

where has-return(s) asserts that s contains a return on at least one path:

                   has-return(return v) = ⊤
                      has-return(s1 ; s2 ) = has-return(s1 ) ∨ has-return(s2 )
      has-return(if p then s1 else s2 ) = has-return(s1 ) ∨ has-return(s2 )
                     has-return(loop s) = has-return(s)
                           has-return(s) = ⊥      otherwise.

All other clauses of returns and pollable-only are unchanged. A loop s is admit-
ted iff its body uses no take or for and contains a reachable return, so loop
exit is structurally possible.
              Modular Responsiveness Verification of Rust Async Runtimes            35

Reactor bodies. A reactor body satisfies wfr : it never returns (reactors are
intended to monitor the environment indefinitely) and contains no loop outside
the outermost loop that surrounds it. Formally:

      wfr (skip) = wfr (trigger(p)) = wfr (wake(w)) = ⊤
              wfr (insert(r, w, p)) = wfr (take(r, w)) = ⊤
                        wfr (return v) = wfr (loop s) = ⊥
                                           wfr (s1 ; s2 ) = wfr (s1 ) ∧ wfr (s2 )
                           wfr (if p then s1 else s2 ) = wfr (s1 ) ∧ wfr (s2 )
                            wfr (for (w, p) in r { s }) = wfr (s)


B    Full Operational Semantics for LART

Figure 10 gives the complete set of small-step program-semantics rules for LART .
The main-paper version (Fig. 5) omits some conventional rules; the full set is
reproduced here for reference.
36      Yanze Li, Ivan Beschastnikh, and Alexander J. Summers




                                      s | κ −→p s′ | κ′

                                   p ∈ Pint
                                                                               (trigger)
         trigger(p) | (ρ, (Σ, Q, R)) −→p skip | (ρ, (Σ ∪ {p}, Q, R))

                                                                               (wake)
           wake(w) | (ρ, (Σ, Q, R)) −→p skip | (ρ, (Σ, Q ∪ {w}, R))

                          R′ = R[r 7→ R(r) ∪ {(w, p)}]
                                                                               (insert)
           insert(r, w, p) | (ρ, (Σ, Q, R)) −→p skip | (ρ, (Σ, Q, R′ ))

                                 (w, p) ∈ R(r)
                           R′ = R[r 7→ R(r) \ {(w, p)}]
                                                                              (take)
              take(r, w) | (ρ, (Σ, Q, R)) −→p skip | (ρ, (Σ, Q, R′ ))

                                      p∈Σ
                                                                   (if-t)
                        if p then s1 else s2 | κ −→p s1 | κ

                                      p∈/Σ
                                                                   (if-f)
                        if p then s1 else s2 | κ −→p s2 | κ

                          R(r) = {(w1 , p1 ), . . . , (wk , pk )}
                             si ≜ s[wi , pi /w, p] k ≥ 1
                                                                              (for)
               for (w, p) in r { s } | (ρ, G) −→p s1 ; · · · ; sk | (ρ, G)

                                   R(r) = ∅
                                                                       (for-emp)
               for (w, p) in r { s } | (ρ, G) −→p skip | (ρ, G)

                                                            s1 | κ −→p s′1 | κ′
                                       (loop)                                             (seq)
     loop s | κ −→p s ; loop s | κ                     s1 ; s2 | κ −→p s′1 ; s2 | κ′

                                                          (seq-skip)
                            skip ; s2 | κ −→p s2 | κ

                                                               (seq-return)
                    return v ; s2 | κ −→p return v | κ


             Fig. 10: Full small-step operational semantics for LART .
