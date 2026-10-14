                                                 A Case Study on Model Checking and Runtime
                                                           Verification for Awkernel
                                                               Akira Hasegawa                                                      Ryuta Kambe
                                              Japan Advanced Institute of Science and Technology                                     TIER IV, Inc.
                                                                Nomi, Japan                                                         Tokyo, Japan
                                                         akira.hasegawa@jaist.ac.jp                                             ryuta.kambe@tier4.jp

                                                                Toshiaki Aoki                                                     Yuuki Takano
                                              Japan Advanced Institute of Science and Technology                                    TIER IV, Inc.
                                                                Nomi, Japan                                                         Tokyo, Japan
arXiv:2503.09282v1 [cs.SE] 12 Mar 2025




                                                            toshiaki@jaist.ac.jp                                                yuuki.takano@tier4.jp

                                         Abstract                                                                 Given these requirements, the scheduler’s behavior in
                                         In operating system development, concurrency poses signifi-           such operating systems exhibits significant interleavings, a
                                         cant challenges. It is difficult for humans to manually review        consequence of increasing throughput. Additionally, because
                                         concurrent behaviors or to write test cases covering all pos-         of the asynchronous nature, processes running on the OS
                                         sible executions, often resulting in critical bugs. Preemption        may not executed at the fixed intervals but can occur at
                                         in schedulers serves as a typical example.                            virtually any moment, leading to a vast range of possible
                                             This paper proposes a development method for concur-              behaviors.
                                         rent software, such as schedulers. Our method incorporates               Developing a scheduling mechanism for such operating
                                         model checking as an aid for tracing code, simplifying the            systems is challenging, as the number of potential paths
                                         analysis of concurrent behavior; we refer to this as model            exceeds human capacity. Even with many people assigned to
                                         checking-assisted code review. While this approach aids in            review the scheduler’s code carefully, it is likely that we will
                                         tracing behaviors, the accuracy of the results is limited be-         miss the paths that lead to bugs. Even if we identify the bugs
                                         cause of the semantics gap between the modeling language              and create a patch to fix them, we cannot be confident that
                                         and the programming language. Therefore, we also intro-               the patch will effectively resolve the issues or that similar
                                         duce runtime verification to address this limitation in model         bugs will never occur in the updated code.
                                         checking-assisted code review.                                           How can we mitigate this problem? This is a challenging
                                             We applied our approach to a real-world operating sys-            task, but it must be addressed to create a reliable operating
                                         tem, Awkernel, as a case study. This new operating system,            system for autonomous driving.
                                         currently under development for autonomous driving, is de-               To tackle this challenge, we propose a development method
                                         signed for preemptive task execution using asynchronous               that incorporates model checking and runtime verification
                                         functions in Rust. After implementing our method, we iden-            into the operating system development process. Our method
                                         tified several bugs that are difficult to detect through manual       uses model checking to make it easier to trace potential
                                         reviews or simple tests.                                              paths based on our understanding of the code. We first write
                                                                                                               a behavior in a modeling language that aligns with our under-
                                                                                                               standing and then check the behavior that can happen if the
                                                                                                               description is correct. Writing a description of the behavior
                                         1   Introduction                                                      from scratch is difficult, as grasping the whole behavior of
                                         Autonomous driving technology has recently rapidly pro-               the code is challenging due to its concurrency and asynchro-
                                         gressed and gained global attention. While there are various          nous nature. Therefore, our approach begins by translating
                                         methods for achieving autonomous driving, most modern                 the code of the operating system’s implementation into a
                                         autonomous vehicles are equipped with numerous sensors                modeling language used in a model checker, line by line.
                                         sensors, including LiDAR and cameras. Because of the vol-                Of course, there is a semantic gap between the program-
                                         ume of sensors, these vehicles must process several gigabits          ming and modeling languages. Thus, the translation may
                                         of data in real time, necessitating high throughput from their        be flawed, and some paths can be missed during checking
                                         operating systems.                                                    the model. Still, it simplifies the process of tracing and con-
                                            Additionally, as the procedures for processing sensor data         templating potential paths in the code compared to relying
                                         are asynchronous, operating systems must facilitate their             solely on mental processing without model checking. We
                                         implementation and ensure effective execution. Moreover,              will refer to the model created by this translation as a code
                                         these procedures should be preemptive to enable real-time             review model.
                                         scheduling.
                                                                                                           1
   To address the limitations of the code review model caused
by the semantics gap, we also introduced runtime verification                 Interrupt       Primary Core        Inter-processor interrupt (IPI)
to the development process. Although runtime verification
does not guarantee exhaustive checking, it is useful for effi-
ciently analyzing the actual behavior of the implementation.
   In Section 2, we will discuss related work. In Section ??,            Non-primary Core 1        Non-primary Core 2          Non-primary Core 3

we will introduce the target system of our proposed method.                        Task
In Section 4, we will explain how we utilized model checking
for code reviews in the development of Awkernel. In Section                                           Task                                   Task
5, we will describe how we used runtime verification to
                                                                                                                 Scheduling Queue
address the drawbacks of model checking. In Section 6, we
will present the results of applying our approach to Awkernel
and identifying bugs. In Section 7, we will share the lessons
learned. Finally, we will conclude the paper in Section 8.           Figure 1. Overview of task scheduling and interrupt han-
                                                                     dling. The primary core does not execute tasks but han-
                                                                     dles interrupts. When an interrupt occurs, the primary core
                                                                     sends an inter-processor interrupt to the non-primary cores.
2   Related Work                                                     The non-primary cores then fetch tasks from the scheduling
Formal methods have been widely used to verify operating             queue and execute them.
systems. One approach involves theorem proving [14]; seL4
is an operating system developed while verifying the cor-
rectness of theorem proving. Although their approach seems
solid, it is time-consuming. They indicated that they would
require six person-years to redo a similar verification for a           There is also another work for verification of an operat-
new kernel using the same methodology. Since we did not              ing system that combines model checking and model-based
have enough team members to apply their approach and                 testing [6, 7]. The researchers used the Spin model checker
time was limited, it was impractical for our situation. More-        to verify the scheduler’s functional correctness on an auto-
over, we wanted to check task state transitions in terms of          motive OS compliant with the OSEK/VDX standard, called
their concurrent nature. However, verifying such properties          REL OS. Based on the OSEK/VDX standard, they first cre-
with theorem proving is more challenging. Our method is              ated a model of the scheduling behavior in Promela, the
less confident than seL4’s approach but it is much lighter           modeling language used by the Spin model checker. They
and can be completed in around three person-months.                  then verified that desirable properties were satisfied in the
   Another work that uses formal methods to verify the be-           model through model checking. Although the properties are
havior of an operating system exists. de Oliveira et al. [12]        satisfied in the model, this does not guarantee that the ac-
proposed a method for conducting runtime verification to             tual behavior of REL OS aligns with the model’s behavior,
check thread behavior in the PREEMPT_RT Linux kernel.                or that it satisfies the properties. Therefore, to check the
First, they created a model of the behavior of thread behav-         conformance between the model and the actual behavior
ior in the PREEMPT_RT Linux kernel using automata while              of REL OS, they generated test cases based on the model
checking logs of actual execution with perf and obtained             used for model checking and conducted model-based test-
reviews from Linux kernel maintainers [10, 11, 13]. Second,          ing. They created a search tree using a log from the Spin
they converted the model into a C data structure and em-             model checker and converted it into test cases. After that,
bedded it into the Linux kernel as a module [12]. They then          they transformed the test case to runnable test programs and
verified that the thread behavior in the Linux kernel aligns         executed them. Their approach is practical even with limited
with their created model. Their method is much lighter than          time and resources. However, creating the model requires a
the seL4 approach [14]. However, runtime verification does           specification that the implementation follows, such as the
not guarantee exhaustiveness. In developing a scheduler, we          OSEK/VDX standard. Because they were not based on such
want to identify bugs that appear only during rare execution         specifications and were implemented while conducting test-
paths; thus, runtime verification alone is unsuitable for our        ing to check whether a program works, their method cannot
needs. Our method also employs runtime verification, but             applied to our development approach and target. Instead of
we used it not as a primary verification method but as a             creating a model from a standard, we manually translated
complement to model checking. Model checking provides                code from the implementation into Promela while accepting
exhaustiveness under several assumptions, while runtime              the semantic gap between the programming language and
verification assesses actual behavior and the accuracy of the        Promela, the modeling language. This approach allows the
model checking results.                                              methods to be applied to a broader range of targets.
                                                                 2
3     Awkernel                                                        Waiting state. In this case, the task returns Poll::Pending
3.1   Design Principles                                               to the OS, which then switches to another task using Rust’s
                                                                      async/await feature. When an event arrives and the task
In this section, we describe the design principles of Awkernel,
                                                                      is ready to run again, the OS resumes the task using the
a new operating system for autonomous vehicles developed
                                                                      async/await feature. However, the traditional context switch
from scratch using Rust. Since autonomous vehicles must
                                                                      mechanism is still needed for real-time scheduling. Thus, we
process large amounts of data in real time, the OS must have
                                                                      implemented the traditional context switch mechanism for
high throughput and performance. On the other hand, safety
                                                                      the async/await functions, making them preemptive. When
is crucial since the OS is used in autonomous vehicles, which
                                                                      a task wants to change its state, such as waiting for an event,
are considered safety-critical systems.
                                                                      it uses the async/await feature to switch tasks. Conversely,
   Awkernel has been developed to achieve both high perfor-
                                                                      when a scheduler needs to switch a task, for instance, when
mance and safety. It is designed to operate in a single address
                                                                      a task exceeds its time slice, it utilizes the traditional context
space, similar to unikernels, for simplicity and performance
                                                                      switch mechanism to switch the task.
improvement. Tasks share the same memory space. From
                                                                         To realize these two task-switching mechanisms, we di-
a safety perspective, the memory spaces used by each task
                                                                      vided the roles of CPU cores into primary and non-primary
must be isolated. We achieve this by utilizing Rust’s type
                                                                      cores, as shown in Figure 1. The first CPU core, typically CPU
system, similar to other Rust-based OSes [9, 15]. Thanks to
                                                                      0, is designated as the primary core, handling timed events
this design, the OS can maintain good throughput. More-
                                                                      and scheduler operations. Other CPU cores are termed non-
over, to enhance safety, it has been developed using Rust;
                                                                      primary cores, which fetch tasks from the shared scheduling
with Rust’s type system, memory spaces for each task are
                                                                      queue and execute them.
effectively isolated while adopting a single address space.
                                                                         For example, when an interruption occurs externally, the
   Although Rust’s type system guarantees memory safety,
                                                                      primary core manages the interruption. If the primary core
it does not ensure other properties that can affect overall
                                                                      decides to interrupt the procedure running on some a non-
safety. To improve confidence regarding safety, we intro-
                                                                      primary core, it sends inter-processor interrupts (IPIs) to the
duced formal methods in the development of Awkernel. We
                                                                      specific non-primary cores related to the interruption, as
have already checked the functional correctness of important
                                                                      shown in Figure 1, and interrupts the tasks.
scheduling functions using Kani [3] and TLA+ [5].
                                                                         Similarly, when a timed event arrives, the primary core
   Preemption-related procedures have not yet been verified
                                                                      will manage it as well. A typical example is the round-robin
due to the state explosion problem. However, formal methods
                                                                      scheduler, whose operations run on the primary core, check-
must be applied to check those processes since the number
                                                                      ing whether each task’s execution time exceed its time slice.
of interleavings is vast and challenging for humans alone to
                                                                      If the primary core identifies a task that exceeds its time
trace alone.
                                                                      slice, it sends an IPI to the non-primary core running the
   In the next section, we will describe the scheduling mech-
                                                                      task. The non-primary core that receives the IPI will suspend
anisms that lead to the significant number of interleavings
                                                                      the task’s execution and initiate preemption. The preempted
causing the state explosion problem and then explain how
                                                                      task will be enqueued into the scheduling queue, as shown
we used model checking to verify them.
                                                                      in Figure 1, and may be resumed on another non-primary
                                                                      core.
3.2   Asynchronous Task Execution
Since autonomous vehicles have numerous sensors, asyn-                   Running Example. In Awkernel, each CPU core oper-
chronous processing is frequently employed. If programmers            ates almost independently. The primary core continuously
are forced to use a traditional callback-based implementation,        processes timed events and performs scheduler operations,
development will become more complex and error-prone [8].             while non-primary cores fetch tasks from the scheduling
Therefore, Awkernel natively supports async/await. Each               queue and execute them, as shown in Figure 1.
task in Awkernel is executed as an async/await function in               However, the queue used for scheduling and the data struc-
Rust, allowing us to employ the async/await feature for tasks,        tures for tasks are shared among all CPU cores. Each core
such as processing sensor data.                                       accesses this shared data at different times, resulting in nu-
   This mechanism enables the OS to switch tasks more effi-           merous interleavings. Consequently, the order of processing
ciently than the traditional context switch; when switching           can sometimes differ from expectations, potentially leading
tasks, the OS does not need to execute a preemption proce-            to bugs.
dure that includes saving and loading contexts. This task-               Here, we present a concurrency-related bug found dur-
switching mechanism is inspired by Embassy [1, 2], where              ing Awkernel’s development. The OS has a function called
the OS, also developed using Rust, can switch tasks utilizing         wait() to enqueue a task into the scheduling queue, which
the async/await feature similar to Awkernel. Occasionally,            takes a task as an argument. Additionally, there is a delta
a task may need to wait for certain events and enter the              list for handling timed events. When an item is added to the
                                                                  3
delta list, the primary core checks the events, and when one             by Spin, the concurrent nature of the scheduling mechanism
arrives, the callback function defined for the item in the delta         made the behavior uncertain for us and difficult to describe.
list is called.                                                          Thus, we manually translated the Rust code into Promela
   Assume there is a running task that adds itself to the delta          line by line while minimizing behavioral changes caused by
list to wait for a timed event. Also, assume the callback func-          semantics differences. We will refer to the translated Promela
tion is wake(). In this case, we can consider the following              description as the code review model, with details are provided
two behaviors:                                                           in Section 4.2.
                                                                            Although Awkernel supports various types of schedulers
    Behavior 1.
                                                                         that can be added flexibly, when writing this paper, Awkernel
     1. The task is added to the delta list.                             includes two schedulers: a round-robin scheduler and a first-
     2. The task changes its state from Running to Waiting               in, first-out (FIFO) scheduler. Since the round-robin sched-
        and suspends execution.                                          uler operates in the same way as the FIFO scheduler when
     3. The timed event arrives, and wake() is called, which             preemption does not occur, we omitted the FIFO scheduler
        enqueues the task into the scheduling queue.                     from the code review model and focused on the round-robin
     4. After a while, the task is taken from the scheduling             scheduler.
        queue and resumed.                                                  When manually translating Rust code to Promela, hardware-
   Behavior 2.                                                           related code is particularly challenging. For example, when
    1. The task is added to the delta list.                              a non-primary core receives an IPI, it immediately suspends
    2. The timed event arrives, and wake() is called; how-               the execution of the regular operation procedure and begins
       ever, since the task is still Running, the function call is       the preemption procedure. This behavior cannot be modeled
       ignored, and the task is not enqueued into the sched-             directly by translating the code. Moreover, the preemption
       uling queue.                                                      procedure itself is also challenging to model in Promela; each
    3. The task changes its state from Running to Waiting                task’s context must be saved, and when the task resumes, the
       and suspends execution.                                           context must be loaded and restored. Section 4.3 describes
    4. The task will never resume since the scheduling queue             our approach to addressing these issues.
       does not contain the task.                                           Another issue arises regarding the handling of time within
                                                                         the code review model. In Awkernel, each core shares and
   Bugs caused by concurrency, such as the one illustrated
                                                                         modifies the data used for scheduling at various times, creat-
in Behavior 2, are difficult to find with manual code reviews
                                                                         ing many interleavings. Hence, if we introduce a time integer
alone. Therefore, we used formal methods such as runtime
                                                                         variable into the code review model, the state explosion prob-
verification and model checking for code reviews.
                                                                         lem will occur. For example, a task running for a long time
3.3    Real-time Properties                                              will be preempted in round-robin scheduling. If we introduce
                                                                         the time concept directly to the code review model to main-
Autonomous driving vehicles require real-time properties.
                                                                         tain and check the execution time of each task, the sequence
To ensure this, the OS must support real-time scheduling,
                                                                         of all variables is considered a state in the Spin model checker,
and the tasks must be preemptive.
                                                                         which leads to an increase in search depth and results in state
  To make the async/await functions preemptive, we imple-
                                                                         explosion. To avoid this, we used an over-approximation of
mented the traditional context switch mechanism in Awker-
                                                                         the time concept to simplify the code review model. We will
nel and made the async/await functions preemptive. When
                                                                         explain how we modeled the time-related procedure in the
a preemption occurs, the OS interrupts the running task
                                                                         Promela model in Section 4.4.
and switches to the procedure for handling the preemption,
                                                                            Translating the Rust code to Promela is insufficient to
such as saving the task’s context and loading or creating the
                                                                         check the scheduling mechanism’s behavior. We must pre-
context of the next task.
                                                                         pare tasks running on the schedulers to observe practical
                                                                         operations in model checking. Since describing all possible
4     Model Checking
                                                                         behaviors of tasks is nearly impossible, we have also approx-
4.1    Approach                                                          imated task behavior. Our approach to approximating tasks
In this section, we will show how we used model checking                 behaviors is described in Section 4.5.
for code reviews in the development of Awkernel. During                     In the development of Awkernel, model checking tech-
the development, we used the Spin model checker [4] for                  niques have been valuable for identifying several bugs. The
reviews. The Spin model checker is a widely used tool for                bugs we found and how we fixed them will be described in
verification concurrent systems, and in our experience, its              Section 6.4.1.
execution is faster than the other model checkers.
   Although the Spin model checker requires a description
of the target behavior in Promela, a modeling language used
                                                                     4
  1 proctype run_main(byte __ctx_id) provided (                       1   pub fn run_main() {
         CONTEXT_STATE[__ctx_id] == CtxActive) {                      2     CPUID_TO_RAWCPUID[awkernel_lib::cpu::cpu_id()]
  2     ......                                                        3         .store(awkernel_lib::cpu::raw_cpu_id(),
  3     RAWCPUIDS[awkernel_lib_cpu_id()] =                                    Ordering::Relaxed);
         awkernel_lib_raw_cpu_id();                                   4     ......
  4                                                                   5
  5     main_loop:                                                    6     loop {
  6     do                                                            7         if let Some(task) = get_next_task() {
  7     :: get_next_task(option_task_id) ->                           8             #[cfg(not(feature = "no_preempt"))]
  8         assert(interrupt_flag[awkernel_lib_cpu_id()]              9             {
         == false);                                                  10                 let mut node = MCSNode::new();
  9         if                                                       11                 let mut info = task.info.lock(&mut node
 10         :: OPT_IS_SOME(option_task_id) ->                                 );
 11             _tid = option_task_id.value;                         12
 12             take_preempt_context(_tid, option_context)           13                 if let Some(ctx) = info.
         ;                                                                    take_preempt_context() {
 13             if                                                   14                     info.update_last_executed();
 14             :: OPT_IS_SOME(option_context) ->                    15                     drop(info);
 15                 yield_and_pool(option_context.value);            16
 16                 goto main_loop                                   17                      unsafe { preempt::yield_and_pool(
 17             :: OPT_IS_NONE(option_context)                                ctx) };
 18             fi;                                                  18                      continue;
 19             ......                                               19                 }
                                                                     20             }
                                                                     21             ......
Figure 2. Code snippet of procedure that runs on non-
primary cores in Awkernel.
                                                                    Figure 3. Code snippet of the Promela description that cor-
                                                                    responds to the procedure running on non-primary cores in
4.2   Line-by-Line Translation                                      Awkernel.
To create the code review model, we first translated the Rust
code of Awkernel into Promela line by line. For example, the
code snippet shown in Figure 2 was translated into Promela
as shown in Figure 3.
   To create the model of Awkernel correctly, we need to con-       Hence, we assumed them to be atomic operations in Promela;
sider the differences in semantics between Rust and Promela,        for instance, we assumed that dequeuing a task from a queue,
including hardware-related behaviors. However, this task is         removing the task, and assigning a return value to the regis-
extremely time-consuming; we must clarify the details of            ter are atomically, with no preemption occurring between
Rust’s semantics and how the hardware interprets and exe-           these actions
cutes them concurrently. To leverage model checking within
a limited development time, we balanced our approach by
                                                                       Option/Result. Promela does not have types that corre-
translating the implementation into Promela based on our
                                                                    spond to the Option and Result types in Rust. Therefore,
understanding. In other words, the code review model does
                                                                    we treated them as structures consisting of two members: a
not represent the actual behavior of the implementation; it
                                                                    label and a value. For example, we represent x = Some(3)
is constructed based on the developers design choices.
                                                                    as x.label = Some; x.value = 3 in Promela. Addition-
   Let us look at how we converted Rust to Promela through
                                                                    ally, since we are unsure how their methods are executed on
several examples.
                                                                    hardware, we cannot determine if, for example, x. label
   Vec/VecDeque. In Promela, there is no syntax for dynamic         = Some; x.value = 3 are executed atomically or if inter-
arrays like Vec and VecDeque in Rust. In the implementation         ruptions can happen between these two statements. Thus,
of Awkernel, Vec/VecDeque are used as types of queues for           similar to the methods of VecDequeue, we assumed that
scheduling. Although modeling the behavior of these types           statements related to Option and Result types are executed
directly in Promela is difficult, we know that the maximum          atomically.
length of the queues is the number of tasks. Therefore, we             As shown above, we ignore the details of the implementa-
replaced Vec and VecDeque with a static array, where the            tion’s behavior and represent them with atomic operations.
length matches the number of tasks in the code review model.        Therefore, if the timing of operations related to such types
Futhermore, VecDeque has several methods, such as push_-            is critical, we may overlook timing-related bugs. However,
back, pop_front. However, we are unsure about the details           we can still identify timing bugs related to function calls, as
of how these methods are executed at the hardware level.            illustrated in Section 6.4.1.
                                                                5
4.3    Modeling of Preemption
                                                                                             kernel_main
As discussed in the previous section, most of the code re-
view model is created through translation. However, these                   init

translations alone are insufficient for the model to function                                kernel_main
                                                                                                                     run_main
                                                                                                                         Task
as the actual implementation does; the translated code does                                                                     CtxActive
                                                                                                                                CtxDoPreemption
not include a preemption mechanism, which must also be                                                  preemption


modeled to replicate the behavior of Awkernel.
   In Awkernel, when preemption occurs, the non-primary
core suspends the execution of the running task and saves                                    thread_entry
                                                                                                                     run_main
                                                                                                                         Task                     : process
                                                                                                                                CtxActive
the thread context at that moment. The non-primary core                                                                         CtxDoPreemption
                                                                                                                                                  : context
then performs a context switch. When the task is resumed,                                               preemption


the non-primary core loads the saved context and resumes                                                                                          : run


the task from where it was previously suspended. There is a
significant issue with describing this behavior in Promela:           Figure 4. Overview of code review model design that is used
Promela does not have the ability to save and load a process’s        in the model checking.
state.
   To overcome this issue, we divided one task in Awkernel
into multiple tasks, as shown in Figure 4, and introduced             When preemption occurs, the Promela processes in the top
provided statements. provided is a primitive of Promela               half are disabled, and the bottom half is activated and exe-
that allows enable/disable a process based on a condition as          cuted.
follows:
                                                                      4.4          Modeling of Time
  1   proctype run_main(byte __ctx_id) provided (
                                                                      Modeling the behavior of a round-robin scheduler and the
           CONTEXT_STATE[__ctx_id] == CtxActive) { ...   }
                                                                      tasks requires introducing the concept of time. When a run-
In this example, when the context state becomes CtxActive,            ning task has exceeded its time slice, the round-robin sched-
the condition is satisfied, and the process run_main will             uler must send an IPI to the non-primary core that is running
execute. Conversely, when the constraint is not satisfied, the        the task. However, Spin does not incorporate the concept of
process is disabled; that is, the model checker will not be           time and features to handle it.
selected or executed, and the state will be retained until the           The most naive way to handle time is to introduce a vari-
constraint is satisfied again.                                        able to represent it. If we cycle the variable’s value within
   To specify an active process, we defined the context states        a range, for example, counting from 0 to 9 and then back
as follows: CtxNotInitialized, CtxActive, CtxDoPreemp-                to 0, we can count the continuous running time of each
tion, CtxPreempted, and CtxInThreadPool. Initially, the               task. However, this approach may lead to the state explosion
context state is set to CtxNotInitialized. When a task                problem.
begins execution, the state changes to CtxActive. When                   Therefore, we decided not to handle the time explicitly. In-
preemption occurs, the state changes to CtxDoPreemption,              stead, to model time-related operations without the variable,
and a process corresponding to the preemption operations              we over-approximated those operations: the round-robin
is enabled; simultaneously, the process corresponding to              scheduler can send the IPI for preemption at any time. By do-
the regular operation is disabled, which corresponds to sav-          ing so, the model checker will search for the paths that occur
ing the task’s progress. When a preempted task is resumed,            in the execution sequence by the implementation without
the task’s state reverts to CtxActive, and the process corre-         introducing time variables.
sponding to the regular operation is enabled, allowing the               However, this approximation allows for sequences where
resumed task to begin operations from the point just before           the scheduler continuously sends IPIs to all non-primary
preemption. We will not elaborate on the details of each              cores and where preemption occurs alternately, which would
context state here.                                                   not happen in actual implementation. To exclude this se-
   By introducing this mechanism, we have successfully em-            quence from the search space of model checking, we must
ulated the preemption sequence of Awkernel in the code                introduce a flag to prevent continuous and infinite sending of
review model. An overview of the code review model after              IPIs. Once preemption occurs, the flag ensures that the next
introducing this mechanism is shown in Figure 4. In the fig-          preemption cannot happen until one of the tasks completes
ure, each yellow circle represents an individual task; the top        its process.
circle illustrates the procedure for the primary core, while
the others represent tasks running on non-primary cores.              4.5          Modeling of Tasks
The blue squares represent the Promela processes. During              To verify the scheduler’s practical and meaningful behav-
the regular operation, the top half of each circle is executed.       ior, it is necessary to provide tasks for execution. However,
                                                                  6
since the types of tasks and their behaviors cannot be fully
known during the verification phase, we approximate a typ-
ical task’s behavior. Over-approximating task behavior to
                                                                                                                 Ready
cover all possible actions can easily lead to state explosion,
so we chose to under-approximate the behavior by catego-                                                               wake()

rizing tasks into two types. These types are pre-configured                                                     Runnable
for each task during model checking.
                                                                                                               get_next()
      • Light Task: a task that terminates quickly and cannot
        be preempted by the round-robin scheduler.                                                  Running                          wake()

      • Heavy Task: a task that takes longer to terminate, is
                                                                              preempt   get_next() Poll::Ready panic      Poll::Pending
        preempted multiple times by the round-robin sched-
        uler, and returns Poll::Pending to wait for certain                 Preempted      Terminated         Panicked             Waiting

        events.
   By defining these two types of tasks, we can identify
bugs related to the timing of preemption and the return               Figure 5. First diagram about task transitions in Awkernel;
of Poll::Pending. Additionally, we can detect issues that             the diagram was created as the first model representing our
arises only when a task completes quickly. Furthermore, by            understanding of the task transition. It was used as the base
selecting Light Tasks, we can reduce the search space and             of the monitor while conducting runtime verification.
the time required for model checking. Thus, if a single Heavy
Task is sufficient to reproduce a bug, we can set the remain-
ing tasks as Light Tasks to reproduce it more quickly and             embedded into the target program’s code, creating a monitor.
efficiently.                                                          When the monitor detects a specification violation, it raises
   In our Promela description, the number of generated tasks,         an alert.
each task type, and the order of the generation are fixed                Runtime verification is beneficial for testing the behavior
in advance by pre-configured parameters. Specifying the               of concurrent programs. When the target program has many
number of generated tasks seems sufficient; the others can            interleavings, the execution sequence varies with each run,
be set using non-deterministic choices in model checking.             making a single test run insufficient. It is impossible to know
However, doing so results in a state space that is too large,         in advance how many times we need to execute tests. Since
leading to out-of-memory errors on the computer executing             runtime verification can operate indefinitely, even though
model checking. To mitigate the size of the state space, we           exhaustiveness of execution for possible paths is not guaran-
separate it by parameters and conduct model checking for              teed, it allows us to test the behavior of the target program
each set of parameters individually.                                  multiple times more efficiently than manual testing.
   When conducting model checking of the code review                     In our work, we created a DFA representing task transi-
model, we pre-configure the number of tasks to be gener-              tions, converted it to a monitor, and embedded it into the
ated, each task’s type, and the order of their generation. To         code of Awkernel. Consequently, we successfully identified
check all patterns exhaustively, we can set these parameters          a concurrency bug that would be difficult for humans to find,
externally and then run multiple model checking processes.            even with model checking.
Attempting to check all patterns in a single execution would
lead to out-of-memory errors. By separating the parameter             5.2   Modeling Task Transitions
sets and running model checking individually for each, we
                                                                      Although we introduced formal methods in the development
can mitigate the impact of state explosion.
                                                                      of Awkernel, we did not have a concrete model representing
                                                                      the actual task state transitions. Although a rough model,
5     Runtime Verification
                                                                      shown in Figure 5, existed, it had not been tested for confor-
5.1    Approach                                                       mance between the model and the actual behavior. Hence, we
Although we found that model checking is helpful for re-              began using this model as the basis for a monitor of runtime
views, it may differ from actual behavior due to the semantic         verification.
gap between Rust and Promela and misunderstandings of                    However, the actual behavior was not as straightforward
Rust program behavior. To bridge this gap and rectify such            as the model shown in Figure 5 due to a flag called need_-
misunderstandings, we employed runtime verification. Run-             sched. In Awkernel, each task has a flag need_sched that
time verification is a formal method that checks whether              allows Waiting tasks to operate without timing bugs. Specif-
the runtime behavior of the target program satisfies a for-           ically, when the timer event arrives before the task becomes
mal specification. In this process, the formal specification is       Waiting, the flag is set, and when the task transitions from
converted into a deterministic finite automaton (DFA) and             Running to Waiting, the flag is checked. If the flag is set,
                                                                  7
                                                                                                                                     1   #[derive(Clone)]
                                                                                                 spawn()                             2   pub struct Model<State, Transition>
                                                                                           Ready(false)                              3   where
                                                                                                 wake()                              4      State: Display + Clone + Eq + Debug,
                                                                                         Runnable(false)
                                                                                                                                     5      Transition: Display + Clone + Eq + Debug,
                                                                                      get_next()
                                                                                                                                     6   {
                                                                                                                                     7      states: Vec<State>,
                                                                  Running(false)       preempt()get_next()           wake()
                                                                                                                                     8      transitions: Vec<(State, Transition, State)>,
                                              send_ipi()       wake()                                 Poll::Pending
                                                                                                                                     9      current_state: State,
                        get_next()     Running(true)                    panic   Poll::Ready                   Waiting(false)
                                                                                                                                    10   }
                    preempt() Poll::Pending   panic                 Poll::Ready                  get_next()
                                                                                                                                    11
      Preempted(true)         Waiting(true)           Panicked(-)          Terminated(-)
                                                                                                                                    12   pub type TaskModel = Model<TaskModelState, Event>;
                                                      wake()                                                                        13
                                                           Runnable(true)                                                           14   pub static MODELS: Mutex<BTreeMap<u32, crate::task::
                                                                                                                                            TaskModel>> = Mutex::new(BTreeMap::new());
                                                                                                                                    15

Figure 6. The final model representing task transitions in
Awkernel, obtained during the continuous process of run-                                                                           Figure 7. The code snippet of the monitor for runtime veri-
time verification and appending the discovered transitions                                                                         fication.

the task will be enqueued into the scheduling queue imme-
diately.                                                                                                                             1   pub fn spawn(
   We believed that the flag should be tracked in runtime ver-                                                                       2       name: Cow<'static, str>,
                                                                                                                                     3       future: impl Future<Output = TaskResult> + '
ification, so we added it to the model. The process of refining                                                                             static + Send,
the model was conducted with input from the developer of                                                                             4       sched_type: SchedulerType,
the task scheduling mechanism to ensure the model’s be-                                                                              5    ) -> u32 {
havior aligns with our intentions. However, we found the                                                                             6     ......
updated model still lacked transitions through runtime veri-                                                                         7       let scheduler = get_scheduler(sched_type);
                                                                                                                                     8       let id = tasks.spawn(name, future.fuse(),
fication.                                                                                                                                   scheduler, sched_type);
                                                                                                                                     9       #[cfg(feature = "runtime_verification")]
5.3     Embedding the Monitor into Awkernel                                                                                         10       {
To verify that actual task transitions follow the model, we                                                                         11         ......
first need to define events and states to be traced and then                                                                        12           let mut models = runtime_verification::
                                                                                                                                            MODELS.lock(&mut node);
implement the corresponding monitoring code in Rust.                                                                                13           let mut model = runtime_verification::task::
   Figure 6 shows the defined events and states. In the model,                                                                              new_task_model();
events are defined as function calls that change a task state.                                                                      14           model.next(&runtime_verification::event::
For example, when a task is enqueued in the scheduling                                                                                      Event::Spawn).unwrap();
queue, wake() function is called, and this event corresponds                                                                        15           models.insert(id, model);
                                                                                                                                             }
to the transition Poll::Ready in Figure 6. Another example
                                                                                                                                    16
                                                                                                                                    17       tasks.wake(id);
is when the task finishes execution and becomes Termi-                                                                              18       id
nated; it will return Poll::Ready, which corresponds to                                                                             19    }
the transition Poll::Ready in Figure 6.                                                                                             20

   We defined the states using a pair of variables, state and
need_sched, in the model. For example, when the wake()                                                                             Figure 8. The code snippet of the hook to the function for
function is called for a running task, need_sched will be set,                                                                     task spawning for runtime verification.
and in this case, the state will change from Running(False)
to Running(True) with the transition wake(), as shown in
Figure 6. In the model, we ignored the need_sched flag for
Terminated and Panicked since they will not transition                                                                               When a function call corresponding to one of the events
anymore. This means the flag will not be used, so we can                                                                           occurs, we change the state of the target task in the variable
omit it and represent the flag value as a symbol indicating                                                                        MODELS accordingly. For example, when spawn() is called, a
“don’t care” in Figure 6.                                                                                                          new task will be created, with the task ID assigned to the vari-
   After defining the states and transitions, we implemented                                                                       able id, which is set to the return value of tasks.spawn(),
the monitor, as shown in Figure 7. The monitor contains the                                                                        and its state will be initialized. In this case, for the monitor,
model from 6 for each task and maintains the current state                                                                         we will initialize a new model for the the task and add it to
of each task in the variable MODELS, as depicted in Figure 7.                                                                      the variable MODELS as shown in L.14-L24 of Figure 8.
                                                                                                                               8
                   File Name         LOC                              1   [1389 DEBUG] rv/src/model.rs:69: Running(false) --
                                                                             PollPending --> Waiting(false)
                   main              83
                                                                      2   [1390 DEBUG] rv/src/model.rs:69: Runnable(false) --
                   kernel_main       32                                      GetNext --> Running(false)
                               part1 73                               3   [1457 DEBUG] rv/src/model.rs:69: Running(false) --
                   task
                               part2 231                                     SetNeedSched --> Running(true)
                               part1 76                               4   [1368 DEBUG] rv/src/model.rs:69: Running(true) --
                   preempt                                                   Preempt --> Preempted(true)
                               part2 175                              5   [1368 DEBUG] rv/src/model.rs:69: Runnable(false) --
                   thread            37                                      GetNext --> Running(false)
                   scheduler         40                               6   [1369 ERROR] kernel/src/nostd.rs:10: panic: panicked
                   rr                41                                       at awkernel_async_lib/src/task.rs:350:22:
                                                                      7   called `Result::unwrap()` on an `Err` value: "Error:
                   delta_list        56
                                                                              an invalid transition is found.\r\n current
                   mutex             8                                       state: Running(false)\r\n symbol: GetNext"
                   awkernel_lib      8                                8

                   verification      38
                   rust_primitives 111
                                                                    Figure 9. The Output When Runtime Verification is Con-
                   Total             1009                           ducted
      Table 1. Lines of Code in the Code Review Model

                                                                    the others spawned at arbitrary times by existing tasks. This
                                                                    configuration required 570.6GB of memory and 1.43 hours.
6     Results                                                          Instead of using Linear Temporal Logic (LTL) formulae
6.1 Code Review Model                                               to verify conditions such as whether each task eventually
The code review model was created by translating the imple-         reaches a Terminated state and remains there without re-
mentation of a kernel into Promela, the modeling language           entering a Running state, we implemented separate monitor-
used by the Spin model checker. Unlike Rust, the modern             ing processes to observe and confirm these state transitions.
import feature does not exist in Promela, but it supports a
                                                                    6.3   Runtime Verification Results
directive similar to that in C. Consequently, some files had
to be split into two parts, such as task and preempt.               We executed Awkernel on QEMU and encountered the error
   The lines of code for each file and the reference file of        shown in Figure 9 within a few seconds. For instance, the er-
Rust are shown in Table 1. Generally, each file name corre-         ror message in Figure 9 indicates that we missed a case where
sponds directly to an actual Rust file; for example, task_-         a Running task is in the scheduling queue and dequeued by
part1 and task_part2 correspond to task.rs in Awkernel.             another non-primary core. Although the implementation
The exceptions are verification, rust_primitives, and               is designed to check that a task is not in the Running state
main. The verification file defines parameters for model            before it starts and to ignore it if it is, this function call was
checking, such as the number and types of tasks. The rust_-         missed in the code review model. Hence, it revealed a gap
primitives file includes macros to bridge the semantic gap          between the model’s assumptions and the actual behavior
between Rust and Promela. Lastly, main defines the initial-         of the implementation.
ization sequence necessary to execute the model.                       Through continuous execution of runtime verification,
                                                                    we observed the actual state transitions. We discovered a
6.2   Model Checking Results                                        bug where a Preempted task occasionally resumes running
We executed model checking on a machine equipped with               without re-entering the Running state as it should.
an AMD EPYC 7H12 2.6GHz CPU and 4TB of DDR4/3200
                                                                    6.4   Found Bugs
SDRAM. We set the number of tasks to three, which is suffi-
cient for checking preemption and resumption across differ-         6.4.1 Preemption Timing. The round-robin scheduler
ent CPU cores.                                                      periodically checks the elapsed time for each running task
   When two of these three tasks were configured as Heavy           since it became Running. If the scheduler finds a task whose
Tasks, the model checking ran out of memory, even with              elapsed time has exceeded the time quantum, it will send
4TB available. Although we identified the bug intentionally         an IPI to the core running that task. However, these two
embedded in the model before the out-of-memory error, we            operations—checking the elapsed time and executing preemption—
could not complete the entire run with this configuration.          are not atomic, which caused a bug.
   Model checking could be completed when we configured                The expected behavior is as follows:
the first generated task as a Heavy Task and the other two as           1. The scheduler checks the elapsed time of task 𝛼 run-
Light Tasks, with the first task generated immediately and                 ning on core 2.
                                                                9
    2. The scheduler decides to perform preemption on core               6.4.2 Task Transition. We identified anomalous behavior
       2.                                                                in Awkernel through runtime verification. When tasks run,
    3. The scheduler sends an IPI to core 2.                             they should be in the Running state. However, during run-
       Instead of using Linear Temporal Logic (LTL) formats              time verification, we observed cases where tasks sometimes
       to verify conditions such as whether each task even-              resumed execution while still marked as Preempted. With
       tually reaches a Terminated state and whether such                the assistance of model checking, we traced the path leading
       a task will never enter a Running state again, we cre-            to this error and implemented a fix.
       ated processes for monitoring states and confirmed                   Additionally, another issue was discovered during this
       them.                                                             process. While tracing the task transition states with run-
    4. Core 2 receives the IPI and starts preemption.                    time verification, we found that the state variable did not
    5. Task 𝛼 changes its state from Running to Preempted                entirely reflect the task state. Each task had a flag called
       and is moved back to the scheduling queue.                        in_queue, and the value of this flag affected the transition
                                                                         destination. Even when the state variable had the same
  However, due to the lack of atomicity, the following se-               value, the transition destination changed depending on the
quence could occur before the fix:                                       value of the in_queue flag. Based on this observation, we re-
    1. The scheduler checks the elapsed time of task 𝛼 run-              vised the state transitions to align more closely with typical
       ning on core 2.                                                   operating system behavior.
    2. The scheduler decides to perform preemption on core
       2.                                                                7     Lessons Learned
    3. Task 𝛼 finishes, and the next task 𝛽 starts running on
                                                                         7.1   Effort
       core 2.
    4. The scheduler sends an IPI to core 2.                             Implementing Awkernel and applying formal methods to
    5. Core 2 receives the IPI and starts preemption.                    it has been performed by others. The person who applied
    6. Task 𝛽 changes its state from Running to Preempted                formal methods to Awkernel could ask the developer at any-
       even though task 𝛽 has just started.                              time. Additionally, although the person who applied model
                                                                         checking knew the foundations of Promela, he needed to
   To fix this bug, we use a flag, need_sched, which is defined          gain experience writing Promela for medium/large-scale soft-
in the task information structure. This flag was introduced to           ware such as Awkernel. Under these conditions, the runtime
prevent the issue shown in section 3.2. Before sending an IPI,           verification took two weeks, and the model checking took
the scheduler sets the need_sched flag for the target task.              three months.
With this modification, we can avoid the bug mentioned                      In the runtime verification part, we first created an au-
above.                                                                   tomaton that shows the transitions of the task states. Then,
   If the scenario above occurs, preemption is canceled as               we embedded it into Awkernel as the monitor. This was
follows:                                                                 quickly completed after consulting with the developer to
    1. The scheduler checks the elapsed time of task 𝛼 run-              understand the sequence of operations in the code. Subse-
       ning on core 2.                                                   quently, we executed the runtime verification, and when we
    2. The scheduler decides to perform preemption on core               found transitions not present in the model, we compared the
       2.                                                                model with the reports from the monitor, revised the model,
    3. The scheduler sets the need_sched flag of task 𝛼.                 and re-executed the process several times. After repeating
    4. Task 𝛼 finishes, and the next task 𝛽 starts running on            this process and identifying the problematic parts of the im-
       core 2.                                                           plementation, we reported them to the developer. This entire
    5. The scheduler sends an IPI to core 2.                             sequence took two weeks.
    6. Core 2 receives the IPI and starts preemption.                       In the model checking part, due to the semantic gap be-
    7. Since the need_sched flag of task 𝛽 is not set, preemp-           tween Rust and Promela, it took three months, which is
       tion is canceled, and task 𝛽 resumes.                             longer than the runtime verification. For instance, one se-
                                                                         mantic gap is that Rust can have a function called automat-
   This seems to resolve the bug. However, the flag had al-              ically when a variable’s ownership is dropped, similar to a
ready been used for Waiting tasks to address the issue shown             destructor in object-oriented languages. However, Promela
in section 3.2. Therefore, we had to ensure that no new issues           lacks such a feature. Hence, we had to check every scope
would arise from this modification. It is difficult to be certain        of variables and manually describe each drop function in
through human review alone due to concurrency. Hence,                    Promela.
we used model checking for the code review. By employing                    Moreover, to mimic preemption behavior, we assigned one
model checking, we gained confidence and applied the above               Promela process to one thread context, but the description
fix.                                                                     of this part became complex. For example, there was a bug
                                                                    10
where multiple processes representing the same thread con-             of potential execution paths. This can make missing specific
text were created. However, a part we approximated contains            paths that may lead to bugs easy. In this case, model checking
numerous interleavings, making it difficult to identify the            will be helpful.
cause of such bugs.                                                       Although we have not fully resolved the state explosion
                                                                       problem, we would like to share a few strategies we have
7.2   Semantic Gap                                                     used that we find effective. First, grouping assignments and
Awkernel is implemented in Rust. Due to concepts like own-             printf statements within atomic blocks is important. Typi-
ership in Rust, there is a semantic gap that cannot be over-           cally, the specific ordering of these statements does not need
looked with Promela. Therefore, theoretically speaking, even           to be considered, and if left unordered, they can contribute to
if we manually convert Rust code to Promela very carefully,            the state explosion problem. Second, under-approximation
we cannot say that all semantics are accurately translated,            is useful. Indeed, we under-approximated the tasks by set-
nor can we guarantee that all behaviors occurring in the               ting limits on the number of preemptions by the round-robin
implementation are covered by the Promela description.                 scheduler and the number of times each task enters the Wait-
   However, in terms of using model checking for code re-              ing state. This approach allows us to divide the search space
view while running the code rather than for verification,              for model checking, reducing memory usage and runtime.
this method of manually converting Rust code to Promela                Therefore, determining how to effectively under-approximate
was valuable. In practice, using this method allowed us to             the target is crucial.
verify whether the behavior was as intended more quickly
and confidently than performing a completely manual code               8    Conclusions
review.                                                                Developing operating systems of autonomous driving vehi-
                                                                       cles is challenging due to their concurrency and asynchro-
7.3   Assumptions
                                                                       nous nature. For such software, simple testing and code
When using model checking for the review, we should recog-             reviewing by humans are not enough; they can easily miss
nize that we can easily overlook implicit assumptions behind           an interleaving that leads to bugs.
the system. Hence, even though model checking exhaustively                To mitigate the difficulty of tracing behaviors, we pro-
verifies described behaviors, it must be noted that behaviors          posed a development method that introduces model check-
not described are not checked.                                         ing to the process, called model checking-assisted code re-
   Runtime verification is helpful in minimizing such over-            view. Even though this method helps trace behaviors and
sights. In fact, we discovered two overlooked behaviors by             identify non-trivial interleavings, faithfulness is limited due
performing runtime verification. These behaviors involved              to the semantic gap between a programming language and
state transitions of tasks due to function calls related to            the language used by a model checker. To complement the
drivers, which were outside the target of the Promela de-              drawbacks of model checking-assisted code review, we also
scription. The oversight occurred because we assumed no                introduced runtime verification to the development process.
function calls would affect task scheduling from outside the              We applied the proposed method to Awkernel, an oper-
target files.                                                          ating system for autonomous driving vehicles, and found
   It is impossible to account for all events without omissions        two bugs that were difficult for humans to identify. The first
in the development of complex software. Therefore, it is               bug was related to the timing of preemption, and the second
crucial to remain aware of the potential for such oversights           was related to task transitions. We fixed these bugs and con-
and to use various methods to minimize these omissions as              firmed the correctness of the fixes through model checking
much as possible.                                                      and runtime verification.
7.4   Unexpected Volume of Interleavings                               9    Acknowledgements
The code review model written in Promela consists of 1009              This work was supported by JST, CREST Grant Number JP-
lines, as shown in Section 6.1. While it is not a small model,         MJCR23M1, Japan. This research is also based on results
it is also not excessively large. However, performing model            obtained from a project, JPNP21027, subsidized by the New
checking on it requires more than 4TB of memory, especially            Energy and Industrial Technology Development Organiza-
when considering preemption. We have made significant                  tion (NEDO) Green Innovation Fund Projects / Development
efforts to reduce the number of interleavings in the model             of In-vehicle Computing and Simulation Technology for En-
but have not yet found an effective solution. Despite the sim-         ergy Saving in Electric Vehicles.
plicity of the scheduling mechanism, the number of possible
execution paths is enormous, contributing to a high number             References
of interleavings.                                                       [1] Async Rust vs RTOS showdown! - Blog - Tweede golf. https:
    When writing concurrent programs, we may not actively                   //tweedegolf.nl/en/blog/65/async-rust-vs-rtos-showdown. Accessed:
consider it, but we are dealing with a tremendous number                    2024-05-08.
                                                                  11
[2] embassy-rs/embassy: Modern embedded framework, using Rust and                [10] Daniel B. De Oliveira, Romulo S. De Oliveira, and Tommaso Cucinotta.
    async. https://github.com/embassy-rs/embassy. Accessed: 2024-05-08.               Untangling the Intricacies of Thread Synchronization in the PRE-
[3] model-checking/kani: Kani Rust Verifier. https://github.com/model-                EMPT_RT Linux Kernel. In 2019 IEEE 22nd International Symposium
    checking/kani/. Accessed: 2024-10-17.                                             on Real-Time Distributed Computing (ISORC), pages 1–9, 2019.
[4] Spin - Formal Verification. https://spinroot.com/. Accessed: 2024-10-        [11] Daniel B. de Oliveira, Rômulo S. de Oliveira, and Tommaso Cucinotta.
    17.                                                                               A thread synchronization model for the PREEMPT_RT Linux kernel.
[5] The TLA+ Home Page. https://lamport.azurewebsites.net/tla/tla.html.               Journal of Systems Architecture, 107:101729, 2020.
    Accessed: 2024-10-17.                                                        [12] Daniel Bristot de Oliveira, Tommaso Cucinotta, and Rômulo Silva
[6] Toshiaki Aoki, Aritoshi Hata, Kazusato Kanamori, Satoshi Tanaka,                  de Oliveira. Efficient Formal Verification for the Linux Kernel. In
    Yuta Kawamoto, Yasuhiro Tanase, Masumi Imai, Fumiya Shigemitsu,                   Peter Csaba Ölveczky and Gwen Salaün, editors, Software Engineering
    Masaki Gondo, and Tomoji Kishi. Model-Checking in the Loop Model-                 and Formal Methods, pages 315–332, Cham, 2019. Springer Interna-
    Based Testing for Automotive Operating Systems, 2023.                             tional Publishing.
[7] Toshiaki Aoki, Makoto Satoh, Mitsuhiro Tani, Kenro Yatake, and To-           [13] Daniel Bristot de Oliveira, Tommaso Cucinotta, and Rômulo Silva
    moji Kishi. Combined Model Checking and Testing Create Confidence—                de Oliveira. Modeling the behavior of threads in the PREEMPT_RT
    A Case on Commercial Automotive Operating System, pages 109–132.                  Linux kernel using automata. SIGBED Rev., 16(3):63–68, November
    Springer Singapore, Singapore, 2017.                                              2019.
[8] Gavin Bierman, Claudio Russo, Geoffrey Mainland, Erik Meijer, and            [14] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick,
    Mads Torgersen. Pause ’n’ Play: Formalizing Asynchronous C♯ . In                  David Cock, Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt, Rafal
    James Noble, editor, ECOOP 2012 – Object-Oriented Programming,                    Kolanski, Michael Norrish, Thomas Sewell, Harvey Tuch, and Simon
    pages 233–257, Berlin, Heidelberg, 2012. Springer Berlin Heidelberg.              Winwood. seL4: formal verification of an OS kernel. In Proceedings
[9] Kevin Boos, Namitha Liyanage, Ramla Ijaz, and Lin Zhong. Theseus:                 of the ACM SIGOPS 22nd Symposium on Operating Systems Principles,
    an Experiment in Operating System Structure and State Management.                 SOSP ’09, page 207–220, New York, NY, USA, 2009. Association for
    In 14th USENIX Symposium on Operating Systems Design and Imple-                   Computing Machinery.
    mentation (OSDI 20), pages 1–19. USENIX Association, November                [15] Vikram Narayanan, Tianjiao Huang, David Detweiler, Dan Appel,
    2020.                                                                             Zhaofeng Li, Gerd Zellweger, and Anton Burtsev. RedLeaf: Isolation
                                                                                      and Communication in a Safe Operating System. In 14th USENIX
                                                                                      Symposium on Operating Systems Design and Implementation (OSDI
                                                                                      20), pages 21–39. USENIX Association, November 2020.




                                                                            12
