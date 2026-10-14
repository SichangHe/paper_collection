                                                                                     Verification of the Tree-Based Hierarchical
                                                                                      Read-Copy Update in the Linux Kernel

                                                                 Lihao Liang                                         Paul E. McKenney                              Daniel Kroening
                                                          University of Oxford                                    IBM Linux Technology Center                       Tom Melham
                                                                                                                                                                   University of Oxford
arXiv:1610.03052v3 [cs.LO] 22 Nov 2018




                                         Abstract                                                                                  1.   Introduction
                                         Read-Copy Update (RCU) is a scalable, high-performance                                    The Linux operating system kernel [1] is widely used in a
                                         Linux-kernel synchronization mechanism that runs low-                                     variety of computing platforms, including servers, safety-
                                         overhead readers concurrently with updaters. Production-                                  critical embedded systems, household appliances, and mo-
                                         quality RCU implementations for multi-core systems are                                    bile devices such as smartphones. Over the past 25 years,
                                         decidedly non-trivial. Giving the ubiquity of Linux, a rare                               many technologies have been added to the Linux kernel, one
                                         “million-year” bug can occur several times per day across                                 example being Read-Copy Update (RCU) [20].
                                         the installed base. Stringent validation of RCU’s complex                                     RCU is a synchronization mechanism that can be used
                                         behaviors is thus critically important. Exhaustive testing is                             to replace reader-writer locks in read-mostly scenarios. It
                                         infeasible due to the exponential number of possible execu-                               allows low-overhead readers to run concurrently with up-
                                         tions, which suggests use of formal verification.                                         daters. Production-quality RCU implementations for multi-
                                             Previous verification efforts on RCU either focus on sim-                             core systems must provide excellent scalability, high through-
                                         ple implementations or use modeling languages, the latter re-                             put, low latency, modest memory footprint, excellent energy
                                         quiring error-prone manual translation that must be repeated                              efficiency, and reliable response to CPU hotplug operations.
                                         frequently due to regular changes in the Linux kernel’s RCU                               The implementation must therefore avoid cache misses, lock
                                         implementation. In this paper, we first describe the imple-                               contention, frequent updates to shared variables, and exces-
                                         mentation of Tree RCU in the Linux kernel. We then discuss                                sive use of atomic read-modify-write and memory-barrier
                                         how to construct a model directly from Tree RCU’s source                                  instructions. Finally, the implementation must cope with the
                                         code in C, and use the CBMC model checker to verify its                                   extremely diverse workloads and platforms of Linux [21].
                                         safety and liveness properties. To our best knowledge, this                                   RCU is now widely used in the Linux-kernel networking,
                                         is the first verification of a significant part of RCU’s source                           device-driver, and file-storage subsystems [21, 22]. To date,
                                         code, and is an important step towards integration of formal                              there are at least 75 million Linux servers [2] and 1.4 billion
                                         verification into the Linux kernel’s regression test suite.                               Android devices [6], which means that a “million-year” bug
                                                                                                                                   can occur several times per day across the installed base.
                                         Categories and Subject Descriptors [D.2.4]: Software/Pro-                                 Stringent validation of RCU’s complex implementation is
                                         gram Verification—Model checking; [D.1.3]: Concurrent                                     thus critically important.
                                         Programming—Parallel programming                                                              Most validation efforts for concurrent software rely on
                                                                                                                                   testing, but unfortunately there is no cost-effective test strat-
                                                                                                                                   egy that can cover all corner cases. Worse still, some of er-
                                         Keywords Software Verification, Parallel Computing, Read-                                 rors that testing does detect might be difficult to reproduce,
                                         Copy Update, Linux Kernel                                                                 diagnose, and repair. The concurrent nature of RCU and the
                                                                                                                                   sheer size of the search space suggest use of formal verifica-
                                                                                                                                   tion, particularly model checking [4].
                                                                                                                                       Formal verification has already been applied to some as-
                                                                                                                                   pects of RCU design, including Tiny RCU [19], userspace
                                                                                                                                   RCU [10], sysidle [19], and interactions between dyntick-
                                                                                                                                   idle and non-maskable interrupts (NMIs) [18]. But these ef-
                                                                                                                                   forts either validate trivial single-CPU RCU implementa-
                                                                                                                                   tions in C (Tiny RCU), or use special-purpose languages
                                         [Copyright notice will appear here once ’preprint’ option is removed.]
                                                                                                                                   such as Promela [13]. Although special-purpose modeling


                                                                                                                               1                                                          2018/11/26
languages do have advantages, a major disadvantage in the                         Reader                            Reader
                                                                                                  Reader
context of the Linux kernel is the difficult and error-prone                                                                 Reader
translation from source code. Other researchers have applied                  Reader                       Reader
manual proofs in formal logics to simple RCU implementa-                                                                              Grace period
tions [11, 24]. These proofs are quite admirable, but require                                    Reader                               extends as
                                                                                                                                      needed
even more manual work, in addition to the translation effort.                                        Reader
   Worse yet, Linux kernel releases are only about 60 days
apart, and RCU changes with each release. Thus, any manual
work must be replicated about six times a year so that me-                     Change                Grace Period            Change Visible
                                                                                                                             to All Readers
chanical and manual models or proofs remain synchronized
with the Linux-kernel RCU implementation. Therefore, if
formal verification is to be part of Linux-kernel RCU’s re-                                 Figure 1: RCU Concepts
gression suite, the verification methods must be scalable and
automated. To this end, this paper describes how to build a                                int x = 0;
model directly from the Linux kernel source code, and use                                  int y = 0;
the C Bounded Model Checker (CBMC) [7] to verify RCU’s                                     int r1, r2;
safety and liveness properties. To the best of our knowledge,
                                                                                           void rcu_reader(void) {
this is the first automatic verification of a significant part of                            rcu_read_lock();
the Linux-kernel RCU source code.                                                            r1 = x;
                                                                                             r2 = y;
                                                                                             rcu_read_unlock();
2.    Background                                                                           }
2.1   What is RCU?
                                                                                           void rcu_updater(void) {
Read-copy update (RCU) is a synchronization mechanism                                        x = 1;
that is often used to replace reader-writer locking. RCU read-                               synchronize_rcu();
ers run concurrently with updaters, and so RCU avoids read-                                  y = 1;
                                                                                           }
side contention by maintaining multiple versions of objects
and ensuring they are not freed until all pre-existing readers                             ...
complete, that is, until after a grace period elapses. The basic
idea is to split updates into removal and reclamation phases                               // after both rcu_reader()
                                                                                           // and rcu_updater() return
that are separated by a grace period [20]. The removal phase                               assert(r2 == 0 || r1 == 1);
removes reader-accessible references to objects, perhaps by
replacing them with new versions.
                                                                                  Figure 2: Verifying RCU Grace Periods
    Modern CPUs guarantee that writes to single aligned
pointers are atomic, so that readers see either the old or
new version of the data structure. These atomic-write seman-                An RCU read-side critical section begins with rcu
tics enable atomic insertions, deletions, and replacements              read lock() and ends with a corresponding rcu read
in a linked structure. This in turn enables readers to dis-             unlock(). When nested, they are flattened into one large
pense with expensive atomic operations, memory barriers,                critical section. Within a critical section, it is illegal to
and cache misses. In fact, in the most aggressive configu-              block, but preemption is legal in a preemptible kernel. RCU-
rations of Linux-kernel RCU, readers can use exactly the                protected data accessed by a read-side critical section will
same sequence of instructions that would be used in a single-           not be reclaimed until after that critical section completes.
threaded implementation, providing RCU readers with ex-                     The function synchronize rcu() marks the end of the
cellent performance and scalability.                                    updater code and the beginning of the reclaimer code. It
    As illustrated in Figure 1, grace periods are only needed           blocks until all pre-existing RCU read-side critical sections
for those readers whose runtime overlaps the removal phase.             have completed. Note that synchronize rcu() does not
Those that start after the removal phase cannot hold refer-             necessarily wait for critical sections that begin after it does.
ences to the removed objects and thus cannot be disrupted                   Consider the example given in Figure 2. If the RCU read-
by objects being freed during the reclamation phase.                    side critical section in function rcu reader() begins before
                                                                        synchronize rcu() in rcu updater() is called, then it
2.2   Core RCU API Usage                                                must finish before synchronize rcu() returns, so that the
The core RCU API is quite small and consists of only                    value of r2 must be 0. If it ends after synchronize rcu()
five primitives: rcu read lock(), rcu read unlock(),                    returns, then the value of r1 must be 1.
synchronize rcu(), rcu assign pointer(), and rcu                            Finally, to assign a new value to an RCU-protected
dereference() [21].                                                     pointer, RCU updaters use rcu assign pointer(), which


                                                                    2                                                                      2018/11/26
returns the new value. RCU readers can use rcu dereference()                struct rcu_state

to fetch an RCU-protected pointer, which can then be safely                                                       struct
                                                                                                                 rcu_node
dereferenced. The returned value is only valid within the
enclosing RCU read-side critical section. The rcu assign
                                                                                                 struct                            struct
pointer() and rcu dereference() functions work to-                                              rcu_node                          rcu_node

gether to ensure that if a given reader dereferences an RCU-
protected pointer to a just-inserted object, the dereference                   struct                struct                  struct              struct
operation will return valid data rather than pre-initialization               rcu_node              rcu_node                rcu_node            rcu_node

garbage.
                                                                                     struct              struct                 struct               struct
                                                                                    rcu_data            rcu_data               rcu_data             rcu_data
3.    Implementation of Tree RCU                                                      CPU 15                CPU 1375              CPU 2751              CPU 4095


The primary advantage of RCU is that it is able to wait for an              struct
                                                                           rcu_data
                                                                                                  struct
                                                                                                 rcu_data
                                                                                                                        struct
                                                                                                                       rcu_data
                                                                                                                                              struct
                                                                                                                                             rcu_data
arbitrarily large number of readers to finish without keeping               CPU 0                CPU 1360              CPU 2736              CPU 4094

track every single one of them. The number of readers can
be large (up to the number of CPUs in non-preemptible im-                                      Figure 3: Tree RCU Hierarchy
plementations and up to the number of tasks in preemptible
implementations). Although RCU’s read-side primitives en-            information is propagated down from the root to the leaves
joy excellent performance and scalability, update-side prim-         of the tree. Shortly after the leaf data structure of a CPU re-
itives must defer the reclamation phase till all pre-existing        ceives this information, synchronize rcu() will return.
readers have completed, either by blocking or by register-               In the remainder of this section, we discuss the imple-
ing a callback that is invoked after a grace period. The per-        mentation of the non-preemptible Tree RCU in the Linux
formance and scalability of RCU relies on efficient mecha-           kernel version 4.3.6. We first briefly discuss the implemen-
nisms to detect when a grace period has completed. For ex-           tation of read/write-side primitives. We then explain Tree
ample, a simplistic RCU implementation might require each            RCU’s hierarchical data structure which records quiescent
CPU to acquire a global lock during each grace period, but           states while maintaining bounded lock contention. Finally,
this would severely limit performance and scalability. Such          we discuss how RCU uses this data structure to detect qui-
an implementation would be quite unlikely to scale beyond            escent states and grace periods without individually tracking
a few hundred CPUs. This is woefully insufficient because            readers.
Linux runs on systems with thousands of CPUs. This has
motivated the creation of Tree RCU.                                  3.2     Read/Write-Side Primitives
                                                                     In a non-preemptible kernel, any region of kernel code that
3.1   Overview                                                       does not voluntarily block is implicitly an RCU read-side
We focus on the “vanilla” RCU API in a non-preemptible               critical section. Therefore, the implementations of rcu
build of the Linux kernel, specifically on the rcu read              read lock() and rcu read unlock() need do nothing
lock(), rcu read unlock(), and synchronize rcu()                     at all, and in fact in production kernel builds that do not have
primitives. The key idea is that RCU read-side primitives            debugging enabled, these two primitives have absolutely no
are confined to kernel code and, in non-preemptible imple-           effect on code generation.
mentations, do not block. Thus, when a CPU is blocking, in               In the common case where there are multiple CPUs run-
the idle loop, or running in user mode, all RCU read-side            ning, the update-side primitive synchronize rcu() calls
critical sections that were previously running on that CPU           wait rcu gp(), which is an internal function that uses
must have finished. Each of these states is therefore called a       a callback mechanism to invoke wakeme after rcu() at
quiescent state. After each CPU has passed through a qui-            the end of some later grace period. As its name suggests,
escent state, the corresponding RCU grace period ends. The           wakeme after rcu() function wakes up wait rcu gp(),
key challenge is to determine when all necessary quiescent           which returns, in turn allowing synchronize rcu() to re-
states have completed for a given grace period—and to do             turn control to its caller.
so with excellent performance and scalability.
    For example, if RCU used a single data structure to record       3.3     Data Structures of Tree RCU
each CPU’s quiescent states, the result would be extreme             RCU’s global state is recorded in the rcu state structure,
lock contention on large systems, in turn resulting in poor          which consists of a tree of rcu node structures with a child
performance and abysmal scalability. Tree RCU therefore              count of up to 64 (32 in a 32-bit system). Every leaf node
instead uses a tree hierarchy of data structures, each leaf of       can have at most 64 rcu data structures (again 32 on a 32-
which records quiescent states of a single CPU and prop-             bit system), each representing a single CPU, as illustrated
agates the information up to the root. When the root is              in Figure 3. Each rcu data structure records its CPU’s qui-
reached, a grace period has ended. Then the grace-period             escent states, and the rcu node tree propagates these states


                                                                 3                                                                                        2018/11/26
                                               struct rcu_state                     than completed, then RCU is in the middle of a grace pe-
                                                                                    riod. All other combinations are invalid.
         0:7         0:3    4:7      0:1      2:3      4:5      6:7

                                                                                    3.3.2   rcu node Structure
                                                                                    The tree of rcu node structures records and propagates
                                                                                    quiescent-state information from the leaves to the root, and
        ->level[0]                                                                  also propagates grace-period information from the root to
        ->level[1]                                                                  the leaves. The rcu node structure has a spinlock ->lock
        ->level[2]                                                                  to protect its fields. The ->parent field references the parent
                                                                                    rcu node structure, and is NULL for the root. The ->level
Figure 4: Array Representation for a Tree of rcu node                               field indicates the level in the tree, counting from zero at the
Structures                                                                          root. The ->grpmask field identifies this node’s bit in the
                                                                                    ->qsmask field of its parent. The ->grplo and ->grphi
                                                                                    fields indicates the lowest and highest numbered CPU that
up to the root, and then propagates grace-period informa-                           are covered by this rcu node structure, respectively.
tion back down to the leaves. Quiescent-state information                               The ->qsmask field indicates which of this node’s chil-
does not propagate upwards from a given node until a qui-                           dren still need to report quiescent states for the current grace
escent state has been reported by each CPU covered by the                           period. As with rcu state, the rcu node structure has
subtree headed by that node. This propagation scheme dra-                           ->gpnum and ->completed fields that have values identi-
matically reduces the lock contention experienced by the up-                        cal to those of the enclosing rcu state structure, except at
per levels of the tree. For example, consider a default rcu                         the beginnings and ends of grace periods when the new val-
node tree for a 4,096-CPU system, which will have have                              ues are propagated down the tree. Each of these fields can be
256 leaf nodes, four internal nodes, and one root node. Dur-                        smaller than its rcu state counterpart by at most one.
ing a given grace period, each CPU will report its quiescent
states to its leaf node, but there will only be 16 CPUs con-                        3.3.3   rcu data structure
tending for each of those 256 leaf nodes. Only 256 of the
CPUs will report quiescent states to the internal nodes, with                       The rcu data structure detects quiescent states and handles
only 64 CPUs contending for each of the four internal nodes.                        RCU callbacks for the corresponding CPU. The structure is
Only four CPUs will report quiescent states to the root node,                       accessed primarily from the corresponding CPU, thus avoid-
resulting in extremely low contention on the root node’s                            ing synchronization overhead. As with the rcu state struc-
lock, so that contention on any given rcu node structure is                         ture, different flavors of RCU maintain their own per-CPU
sharply bounded even in very large configurations. The cur-                         rcu data structures. The ->cpu field identifies the corre-
rent RCU implementation in the Linux kernel supports up to                          sponding CPU, the ->rsp field references the correspond-
a four-level tree, and thus in total 644 = 16, 777, 216 CPUs                        ing rcu state structure, and the ->mynode field references
in a 64 bit machine.1                                                               the corresponding leaf rcu node structure. The ->grpmask
                                                                                    field identifies this rcu data structure’s bit in the ->qsmask
3.3.1    rcu state Structure                                                        field of its leaf rcu node structure.
Each flavor of RCU has its own global rcu state struc-                                  The rcu data structure’s ->qs pending field indicates
ture. The rcu state structure includes an array of rcu                              that RCU needs a quiescent state from the corresponding
node structures organized as a tree struct rcu node                                 CPU, and the ->passed quiesce indicates that the CPU
node[NUM RCU NODES], with rcu data structures con-                                  has already passed through a quiescent state. The rcu data
nected to the leaves. Given this organization, a breadth-first                      also has ->gpnum and ->completed fields, which can lag
traversal is simply a linear scan of the array. Another ar-                         arbitrarily behind their counterparts in the rcu state and
ray struct rcu node *level[NUM RCU LVLS] is used to                                 rcu node structures on idle CPUs. However, on the non-
point to the left-most node at each level of the tree, as shown                     idle CPUs that are the focus of this paper, these two fields
in Figure 4.                                                                        can lag at most one grace period behind their leaf rcu node
   The rcu state structure uses unsigned long fields                                counterparts.
->gpnum and ->completed to track RCU’s grace periods.                                   The rcu state structure’s ->gpnum and ->completed
The ->gpnum field records the most recently started grace                           fields represent the most current values, and are tracked
period, whereas ->completed records the most recently                               closely by those of the rcu node structure, which allows the
ended grace period. If the two numbers are equal, then cor-                         ->gpnum and ->completed fields in the rcu data struc-
responding flavor of RCU is idle. If gpnum is one greater                           tures to be are compared against their counterparts in the
                                                                                    corresponding leaf rcu node to detect a new grace period.
1 Four-level trees are only used in stress testing, but three-level trees are       This scheme allows CPUs to detect beginnings and ends of
used in production by 4096-CPU systems.                                             grace periods without incurring lock- or memory-contention


                                                                                4                                                          2018/11/26
    nxtlist                                                                     (CB 3 and CB 4) are not yet assigned to a specific grace
                                                                                period. The ->nxttail[RCU NEXT TAIL] element always
    nxttail[RCU_DONE_TAIL]
                                                                                references either the last callback or, when the entire list is
    nxttail[RCU_WAIT_TAIL]                                    CB 1              empty, ->nxtlist.
                                                                                    Cache locality is promoted by invoking callbacks on the
    nxttail[RCU_NEXT_READY_TAIL]                               next
                                                                                CPU that registered them. For example, RCU’s update-side
    nxttail[RCU_NEXT_TAIL]                                                      primitive synchronize rcu() appends callback wakeme
                                                              CB 2              after rcu() to the end of the ->nxttail[RCU NEXT
                                                                                TAIL] list in the current CPU (Section 3.2). They are ad-
                                                               next
                                                                                vanced one segment towards the head of the list (via rcu
                                                                                advance cbs()) when the CPU detects the current grace
                                                              CB 3              period has ended, which is indicated by the ->completed
                                                               next
                                                                                field of the CPU’s rcu data structure being one smaller
                                                                                than its counterpart in the corresponding leaf rcu node
                                                                                structure. The CPU also periodically merges the RCU NEXT
                                                              CB 4              TAIL segment into the RCU NEXT READY TAIL segment by
                                                               next             calling rcu accelerate cbs(). In a few special cases,
                                                                                the CPU merges the RCU NEXT TAIL segment into the RCU
            Figure 5: Callback Queuing in rcu data                              WAIT TAIL segment, bypassing the RCU NEXT READY TAIL
                                                                                segment. This optimization applies when the CPU is starting
                                                                                a new grace period. It does not apply when a CPU notices
penalties. The rcu data structure manages RCU callbacks                         a new grace period because that grace period might well
using a four-segment list [14].                                                 have started before the callbacks were added to the RCU
                                                                                NEXT TAIL segment. This is a deliberate design choice: It
3.3.4    RCU Callbacks                                                          is more important for the CPUs to operate independently
The rcu data structure manages RCU callbacks using                              (thus avoiding contention and synchronization overhead)
a ->nxtlist pointer tracking the head of the list and                           than it is to decrease grace-period latencies. In those rare
an array of ->nxttail[] tail pointers that form a four-                         occasions where low grace-period latency is important,
segment list of callbacks [14], with each element of the                        the synchronize rcu expedited() should be used. This
->nxttail[] array referencing the tail of the correspond-                       function has the same semantics as does synchronize
ing segment, as shown in Figure 5. The segment ending                           rcu(), but trades off efficiency optimizations in favor of
with ->nxttail[RCU DONE TAIL] (the “RCU DONE TAIL                               reduced latency.
segment”) contains callbacks handled by a prior grace pe-                           Each RCU callbacks is an rcu head structure which has
riod that are therefore ready to be invoked. The RCU WAIT                       a ->next field that points to the next callback on the list and
TAIL and RCU NEXT READY TAIL segments contain call-                             a ->func field that references the function to be invoked at
backs waiting for the current and the next grace period, re-                    the end of an upcoming grace period.
spectively. Finally, the RCU NEXT TAIL segment contains
callbacks that are not yet associated with any grace period.
The ->qlen field counts the total number of callbacks, and
the ->blimit field specifies the maximum number of RCU                          3.4   Quiescent State Detection
callbacks that may be invoked at a given time, thus limiting
                                                                                RCU has to wait until all pre-existing read-side critical sec-
response-time degradation due to long lists of callbacks.2
                                                                                tions have finished before it can safely allow a grace period
   Back in Figure 5, the ->nxttail[RCU DONE TAIL] ar-
                                                                                to end. The performance and scalability of RCU rely on its
ray element references ->nxtlist, which means none of
                                                                                ability to efficiently detect quiescent states and determine
the callbacks are ready to invoke. The ->nxttail[RCU
                                                                                whether the set of quiescent states detected thus far allows
WAIT TAIL] element references callback 2’s ->next pointer,
                                                                                the grace period to end. If each CPU (or, in the case of pre-
meaning that callbacks CB 1 and CB 2 are waiting for the
                                                                                emptible RCU, each task) has passed through a quiescent
current grace period. The ->nxttail[RCU NEXT READY
                                                                                state, a grace period has elapsed.
TAIL] element references that same ->next pointer, mean-
                                                                                   The non-preemptible RCU-sched flavor’s quiescent states
ing that no callbacks are waiting for the next grace period.
                                                                                apply to CPUs, and are user-space execution, context switch,
Finally, the callbacks between the ->nxttail[RCU NEXT
                                                                                idle, and offline state. Therefore, RCU-sched only needs to
READY TAIL] and ->nxttail[RCU NEXT TAIL] elements
                                                                                track tasks and interrupt handlers that are actually running
2 Workloads requiring aggressive real-time guarantees should use callback       because blocked and preempted tasks are always in quies-
offloading, which is outside of the scope of this paper.                        cent states. Thus, RCU-sched needs only track CPU states.


                                                                            5                                                         2018/11/26
                                          New
                                                                     which is scheduled from the scheduling-clock interrupt. This
                               Y
           Initialize GP               Grace Period                  function first calls rcu check quiescent state() to re-
                                         Req'd?
                                                  N                  port recent quiescent states on the current CPU. Then rcu
                                                      RCU Idle
                                                                     process callbacks() starts a new grace period if needed,
              All                                                    and finally calls invoke rcu callbacks() to invoke any
                           Y
           CPUs Passed                 Complete GP                   callbacks whose grace period has already elapsed.
            Through
              QS?                                                        Function rcu check quiescent state() first invokes
                    N                                                note gp changes() to update the CPU-local rcu data
                                                                     structure to record the end of previous grace periods and
         CPU Passes
                                                                     the beginning of new grace periods. Any new values for
         Through QS
                                   Wait for QS                       these fields are copied from the leaf rcu node structure to
                                                                     the rcu data structure. If an old grace period has ended,
                                                                     rcu advance cbs() is invoked to advance all callbacks,
        Figure 6: Grace-Period Detection State Diagram               otherwise, rcu accelerate cbs() is invoked to assign a
                                                                     grace period to any recently arrived callbacks. If a new grace
3.4.1    Scheduling-Clock Interrupt                                  period has started, ->passed quiesce is set to zero, and if
                                                                     in addition RCU is waiting for a quiescent state from this
The rcu check callbacks() is invoked from the sched-                 CPU, ->qs pending is set to one, so that a new quiescent
uling-clock interrupt handler, which allows RCU to peri-             state will be detected for the new grace period.
odically check whether a given busy CPU is in the user-                  Next, rcu check quiescent state() checks whether
mode or idle-loop quiescent states. If the CPU is in one of          ->qs pending indicates that RCU needs a quiescent state
these quiescent states, rcu check callbacks() invokes                from this CPU. If so, it checks whether ->passed quiesce
rcu sched qs(), which sets the per-CPU rcu sched                     indicates that this CPU has in fact passed through a quiescent
data.passed quiesce fields to 1.                                     state. If so, it invokes rcu report qs rdp() to report that
   The rcu check callbacks() function invokes rcu                    quiescent state up the combining tree.
pending() to determine whether a recent event or cur-                    The rcu report qs rdp() function first verifies that the
rent condition means that RCU requires attention from                CPU has in fact detected a legitimate quiescent state for the
this CPU. If so, rcu check callbacks() invokes raise                 current grace period, and under the protection of the leaf
softirq(), which will cause rcu process callbacks()                  rcu node structure’s ->lock. If not, it resets quiescent-state
to be invoked once the CPU reaches a state where it is safe          detection and returns, thus ignoring any redundant quiescent
to do so (roughly speaking, once the CPU has interrupts,             states belonging to some earlier grace period. Otherwise, if
preemption, and bottom halves enabled). This function is             the ->qsmask field indicates that RCU needs to report a
discussed in detail in Section 3.5.1.                                quiescent state from this CPU, rcu accelerate cbs() is
3.4.2    Context-Switch Handling                                     invoked to assign a grace-period number to any new call-
                                                                     backs, and then rcu report qs rnp() is invoked to report
The context-switch quiescent state is recorded by invoking           the quiescent state to the rcu node combining tree.
rcu note context switch() from schedule() (and,                          The rcu report qs rnp() function traverses up the
for the benefit of virtualization, also from rcu virt note           rcu node tree, at each level holding the rcu node struc-
context switch()). The rcu note context switch()                     ture’s ->lock. At any level, if the child structure’s ->qsmask
function invokes rcu sched qs() to inform RCU of the                 bit is already clear, or if the ->gpnum changes, traversal
context switch, which is a quiescent state of the CPU.               stops. Otherwise, the child structure’s bit is cleared from
                                                                     ->qsmask, after which, if ->qsmask is non-zero, traversal
3.5     Grace Period Detection
                                                                     stops. Otherwise, traversal proceeds on to the parent rcu
Once each CPU has passed through a quiescent state, a                node structure. Once the root is reached, traversal stops
grace period for RCU has completed. As discussed in Sec-             and rcu report qs rsp() is invoked to awaken the grace-
tion 3.3, Tree-RCU uses a hierarchy of rcu node struc-               period kthread (kernel thread). The grace-period kthread
tures to manage quiescent state and grace period informa-            will then clean up after the now-ended grace period, and,
tion. Quiescent-state information is passed up the tree from         if needed, start a new one.
the leaf per-CPU rcu data structures. Grace-period infor-
mation is passed down from the root. We focus on grace-              3.5.2   Grace-Period Kernel Thread
period detection for busy CPUs, as illustrated in Figure 6.          The RCU grace-period kthread invokes rcu gp kthread(),
                                                                     which contains an infinite loop that initializes, waits for, and
3.5.1    Softirq Handler for RCU                                     cleans up after each grace period.
RCU’s busy-CPU grace period detection relies on the RCU                 When no grace period is required, the grace-period
SOFTIRQ handler function rcu process callbacks(),                    kthread sets its rcu state structure’s ->flags field to RCU


                                                                 6                                                          2018/11/26
GP WAIT GPS, and then waits within an inner infinite loop             that are rcu data structures for each CPU. Function rcu
for that structure’s ->gp state field to be set. Once set,            spawn gp kthread() is also called to initialize and spawn
rcu gp kthread() invokes rcu gp init() to initialize                  the RCU grace-period kthread for each RCU flavor.
a new grace period, which rechecks the ->gp state field                   Referring again to Figure 2, suppose that rcu reader()
under the root rcu node structure’s ->lock. If the field              begins execution on CPU 0 while rcu updater() concur-
is no longer set, rcu gp init() returns zero. Otherwise,              rently sets x to 1 and then invokes synchronize rcu() on
it increments rsp->gpnum by 1 to record a new grace pe-               CPU 1. As discussed in Section 3.2, synchronize rcu()
riod number. Finally, it performs a breadth-first traversal of        invokes wait rcu gp(), which in turn registers an RCU
the rcu node structures in the combining tree. For each               callback that will invoke wakeme after rcu() some time
rcu node structure rnp, we set the rnp->qsmask to in-                 after rcu reader() exits its critical section.
dicate which children must report quiescent states for the                However, this critical-section exit has no immediate ef-
new grace period (Section 3.3.2), and set rnp->gpnum and              fect. Instead, a later context switch will invoke rcu note
rnp->completed to their rcu state counterparts. If the                context switch(), which in turn invokes rcu sched
rcu node structure rnp is the parent of the current CPU’s             qs(), recording the quiescent state in the CPU’s rcu
rcu data, we invoke note gp changes() to set up the                   sched data structure’s ->passed quiesce field. Later, a
CPU-local rcu data state. Other CPUs will invoke note                 scheduling-clock interrupt will invoke rcu check callbacks(),
gp changes() after their next scheduling-clock interrupt.             which calls rcu pending() and notes that the ->passed
    To clean up after a grace period, rcu gp kthread()                quiesce field is set. This will cause rcu pending() to re-
calls rcu gp cleanup() after setting the rcu state field              turn true, which in turn causes rcu check callbacks()
rsp->gp state to RCU GP CLEANUP. After the function re-               to invoke rcu process callbacks(). In its turn, rcu
turns, rsp->gp state is set to RCU GP CLEANED to record               process callbacks() will invoke raise softirq(RCU
the end of the old grace period. Function rcu gp cleanup()            SOFTIRQ), which, once the CPU has interrupts, preemption,
performs a breadth-first traversal of rcu node combining-             and bottom halves enabled, calls rcu process callbacks().
tree. It first sets each rcu node structure’s ->completed                 As discussed in Section 3.5.1, RCU’s softirq handler
field to the rcu state structure’s ->gpnum field. It then             function rcu process callbacks() first calls rcu check
updates the current CPU’s CPU-local rcu data structure                quiescent state() to report any recent quiescent states
by calling note gp changes(). For other CPUs, the up-                 on the current CPU (CPU 0). Then it checks whether the
date will take place when they handle the scheduling-clock            CPU 0 has passed a quiescent state. Since a quiescent state
interrupts, in a fashion similar to rcu gp init(). After              has been recorded for CPU 0, rcu report qs rnp() is in-
the traversal, it marks the completion of the grace period            voked to traversal up the combining tree. It clears the first bit
by setting the rcu state structure’s ->completed field to             of the root rcu node structure’s qsmask field (recall that the
that structure’s ->gpnum field, and invokes rcu advance               RCU combining tree has only one level). Since the second
cbs() to advance callbacks. Finally, if another grace period          bit for CPU 1 has not been cleared, the function returns.
is needed, we set rsp->gp flags to RCU GP FLAG INIT.                      Since synchronize rcu() blocks in CPU 1, it will re-
Then in the next iteration of the outer loop, the grace-period        sult in a context switch. This triggers a sequence of events
kthread will initialize a new grace period as discussed above.        similar to that described above for CPU 1, which results in
                                                                      the clearing of the second bit of the root rcu node struc-
                                                                      ture’s ->qs mask field, the value of which is now 0, indi-
4.   Verification Scenario
                                                                      cating the end of the current grace period. CPU 1 therefore
We use the example in Figure 2 to demonstrate how the dif-            invokes rcu report qs rsp() to awaken the grace-period
ferent components of Tree RCU work together to guarantee              kthread, which will clean up the ended grace period, and, if
that all pre-existing read-side critical sections finish before       needed, start a new one (Section 3.5.2).
RCU allows a grace period to end. This example will drive                 Lastly, rcu process callbacks() calls invoke rcu
the verification, which will check for violations of the asser-       callbacks() to invoke any callbacks whose grace period
tion at this end of the code.                                         has already elapsed, for example, wakeme after rcu(),
   We focus on the implementation of the non-preemptible              which will allow synchronize rcu() to return.
RCU-sched flavor. We further assume there are only two
CPUs, and that CPU 0 executes function rcu reader() and               5.   Modeling RCU for CBMC
CPU 1 executes rcu updater(). When the system boots,
                                                                      The C Bounded Model Checker (CBMC)3 is a program an-
the Linux kernel calls rcu init() to initialize RCU, which
                                                                      alyzer that implements bit-precise bounded model checking
includes constructing the combining tree of rcu node and
                                                                      for C programs [7]. CBMC can demonstrate violation of as-
rcu data structures via rcu init geometry() and initial-
                                                                      sertions in C programs, or prove their safety under a given
izing the fields of the nodes in the tree for each RCU flavor
                                                                      loop unwinding bound. It translates an input C program into
via rcu init one(). In our example it will be a one-level
tree that has one rcu node structure as root and two children         3 http://www.cprover.org/cbmc/




                                                                  7                                                      2018/11/26
a formula, which is then passed to a modern SAT or SMT                     A pair of integer arrays local irq depth and irq lock
solver together with a constraint that specifies the set of error       is used to model CPUs enabling and disabling interrupts.
states. If the solver determines the formula to be satisfiable,         Both arrays are indexed by CPU ID, with the first recording
an error trace giving the exact sequence of events is extracted         each CPU’s interrupt-disable nesting depth and the second
from the satisfying assignment. Recently, support has been              recording whether or not interrupts are disabled.
added for verifying concurrent programs over a wide range
of memory models, including SC, TSO, and PSO [3].                       Update-Side API synchronize sched()
    In the remainder of this section we describe how to con-            Because our model omits CPU hotplug and callback han-
struct a model from the source code of the Tree RCU imple-              dling, we cannot use Tree RCU’s normal callback mecha-
mentation in the Linux kernel version 4.3.6, which can be               nisms to detect the end of a grace period. We therefore use
verified by CBMC. Model construction entailed stubbing out              a global variable wait rcu gp flag, which is initialized
calls to other parts of the kernel, removing irrelevant func-           to 1 in wait rcu gp() before the grace period. Because
tionality (such as idle-CPU detection), removing irrelevant             wait rcu gp() blocks, it can result in a context switch,
data (such as statistics), and adding preprocessor directives           the model invokes rcu note context switch(), followed
to conditionally inject bugs (described in Section 6.1). The            by a call to rcu process callbacks() to inform RCU
Linux kernel environment and the majority of these changes              of the resulting quiescent state. When the resulting quies-
to the source code are made through macros in separate files            cent states propagate to the root of the combining tree, the
that can be reused across different versions of the Tree RCU            grace-period kthread is awakened. This kthread then invokes
implementation. The biggest change in the source files is to            rcu gp cleanup(), the modeling of which is described be-
use arrays to model per-CPU data, which could potentially               low. Then rcu gp cleanup() calls rcu advance cbs(),
be scripted [23]. The resulting model has 8,626 lines of C              which invokes pass rcu gp() to clear the wait rcu gp
code. Around 900 lines of the code models the Linux ker-                flag flag. The CPROVER assume(wait rcu gp flag
nel environment. This is significantly smaller than the actual          == 0) in wait rcu gp() prevents CBMC from contin-
Linux kernel code used by the Tree RCU implementation,                  uing execution until wait rcu gp flag is equal to 0, thus
making verification of Tree RCU possible. The model con-                modeling the needed grace-period wait.
tains assertions and can be also run as a user program, which
                                                                        Scheduling-Clock Interrupt and Context Switch
provides important validation of the model itself.
                                                                        The rcu check callbacks() function detects idle and
Initialization                                                          usermode execution, as well as invokes RCU core processing
Our model first invokes rcu init() which in turn invokes:               in response to state changes. Because we model neither idle
(1) rcu init geometry() to compute the rcu node tree                    nor usermode execution, the only state changes are context-
geometry; (2) rcu init one to initialize the rcu state                  switches and the beginnings and ends of grace periods. We
structure; (3) rcu cpu notify() to initialize each CPU’s                therefore dispense with rcu check callbacks() (Sec-
rcu data structure. This boot initialization tunes the data-            tion 3.4.1). Instead, we directly call rcu note context
structure configuration to match that of the specific hardware          switch() just after releasing a CPU, which in turn calls
at hand. For example, a large-system tree might resemble                rcu sched qs() to record the quiescent state. Finally, we
Figure 3, while a small configuration has a single rcu node             call rcu process callbacks(), which notes grace-period
“tree”. The model then calls rcu spawn gp kthread() to                  beginnings and ends and reports quiescent states up RCU’s
spawn the grace-period kthreads discussed below.                        combining tree.
Per-CPU Variables and State                                             Grace-Period Kthread
RCU uses per-CPU data to provide cache locality and to re-              As discussed in Section 3.5.2, rcu gp kthread() invokes
duce contention and synchronization overhead. For example,              rcu gp init(), rcu gp fqs(), and rcu gp cleanup()
the per-CPU structure rcu data records quiescent states                 to initialize, wait for, and clean up after each grace period,
and handles RCU callbacks (Section 3.3.3). We model this                respectively. To reduce the size of the formula generated
per-CPU data as an array, indexed by CPU ID.                            by CBMC, instead of spawning a separate thread, we di-
   It is also necessary to model per-CPU state, including               rectly call rcu gp init() from rcu spawn gp kthread
the currently running task and whether or not interrupts                and rcu gp cleanup() from rcu report qs rsp(). Be-
are enabled. Identifying the running task requires a (trivial)          cause we model neither idle nor usermode execution, we
model of the Linux-kernel scheduler, which uses an integer              need not call rcu gp fqs().
array cpu lock, indexed by CPU ID. Each element of this
array models an exclusive lock. When a task schedules on                Kernel Spin Locks
a given CPU, it acquires the corresponding CPU lock, and                CBMC’s CPROVER atomic begin(), CPROVER atomic
releases it when scheduling away. We currently do not model             end(), and CPROVER assume() built-in primitives are
preemption, so need model only voluntary context switches.              used to construct atomic test-and-set for spinlock t and


                                                                    8                                                        2018/11/26
raw spinlock t acquisition and atomic reset for release.                 To validate our verification, we also run CBMC with
We use GCC atomic builtins for user-space execution:                  the bug-injection scenarios described below,4 which are
while ( sync lock test and set(lock, 1)) acquires                     simplified versions of bugs encountered in actual practice.
a lock and sync lock release(lock) releases it.                       Bugs 2–6 are liveness checks and thus use the aforemen-
                                                                      tioned assert(0), and the remaining scenarios are safety
Limitations                                                           checks which thus use the base-case assertion in Figure 2.
We model only the fundamental components of Tree RCU,
                                                                      Bug 1 This bug-injection scenario makes the RCU update-
excluding, for example, quiescent-state forcing, grace-period
                                                                      side primitive synchronize rcu() return immediately
expediting, and callback handling. In addition, we make the
                                                                      (line 523 in tree plugin.h). With this injected bug, up-
assumption that all CPUs are busy executing RCU related
                                                                      daters never wait for readers, which should result in a safety
tasks. As a result, we do not model the following scenarios:
                                                                      violation, thus preventing Figure 2’s assertion from holding.
1. CPU hotplug and dyntick-idle; 2. Thread-migration fail-
ure modes in the Linux kernel involving per-CPU variables;            Bug 2 The idea behind this bug-injection scenario is to
3. RCU priority boosting. Nonetheless, we model real-world            prevent individual CPUs from realizing that quiescent states
server-class RCU code paths and data layout on systems                are needed, thus preventing them from recording quies-
with up to 16 CPUs (default configurations) or up to either           cent states. As a result, it prevents grace periods from
32 or 64 CPUs (non-default configurations on either 32-bit            completing. Specifically, in function rcu gp init(), for
or 64-bit CPUs). Moreover, we model scheduling-clock in-              each rcu node structure in the combining tree, we set the
terrupts as direct function calls, which, as discussed later,         field rnp->qsmask to 0 instead of rnp->qsmaskinit (line
results in failures to model one of the bug-injection scenar-         1889 in tree.c). Then when rcu process callbacks()
ios. Lastly, the test harness we use only passes through a            is called, rcu check quiescent state() will invoke
single grace period, so cannot detect failures involving mul-         note gp changes() that sets rdp->qs pending to 0, in-
tiple grace periods.                                                  dicating that RCU needs no quiescent state from the cor-
                                                                      responding CPU. Thus, rcu check quiescent state()
6.    Experiments                                                     will return without calling rcu report qs rdp(), prevent-
In this section we discuss our experiments verifying the              ing grace periods from completing. This liveness violation
Tree RCU implementation in the Linux-kernel. We first de-             should fail to trigger a violation of the end-of-execution
scribe several bug-injection scenarios used in the experi-            assert(0).
ments. Next, we report results of user-space runs of the              Bug 3 This bug-injection scenario is a variation of Bug 2,
RCU model. Finally, we discuss the verification results us-           in which each CPU remains aware that quiescent states are
ing CBMC. We performed our experiments on a 64-bit ma-                required, but incorrectly believes that it has already reported
chine running Linux 3.19.8 with eight Intel Xeon 3.07 GHz             a quiescent state for the current grace period. To accomplish
cores and 48 GB of memory. We have made the source code               this, in note gp changes(), we clear rnp->qsmask by
of our RCU model and the experimental data available at               adding a statement rnp->qsmask &= ~rdp->grpmask; in
https://github.com/lihaol/verify-treercu.                             the last if code block (line 1739 in tree.c). Then function
                                                                      rcu report qs rnp() never walks up the rcu node tree,
6.1   Bug-Injection Scenarios
                                                                      resulting in a liveness violation as in Bug 2.
Because we model non-preemptible Tree RCU, each CPU
runs exactly one RCU task as a separate thread. Upon com-             Bug 4 This bug-injection scenario is an alternative code
pletion, each task increments a global counter thread cnt,            change that gets the same effect as does Bug 2. For this
enabling the parent thread to verify the completion of all            alternative, in note gp changes(), we set the rdp->qs
RCU tasks using a statement CPROVER assume(thread                     pending field to 0 directly (line 1749 in tree.c). This is a
cnt == 2). The base case uses the example in Figure 2,                variant of Bug 2 and thus also a liveness violation.
including its assertion assert(r2 == 0 || r1 == 1).                   Bug 5 In this bug-injection scenario, CPUs remain aware
This assertion does not hold when RCU’s fundamental                   of the need for quiescent states. However, CPUs are pre-
safety guarantee is violated: read-side critical sections can-        vented from recording their quiescent states, thus preventing
not span grace periods.We also verify a weak form of                  grace periods from ever completing. To accomplish this,
liveness by inserting an assert(0) after the CPROVER                  we modify function rcu sched qs() to return immedi-
assume(thread cnt == 2) statement. This assertion can-                ately (line 246 in tree.c), so that quiescent states are not
not hold, and so it will be violated if at least one grace pe-        recorded. Grace periods therefore never complete, which
riod completes. Such a “verification failure” is in fact the          constitutes a liveness violation similar to Bug 2.
expected behavior for a correct RCU implementation. On
the other hand, if the assertion is not violated, grace periods       4 Source code: https://www.kernel.org/pub/linux/kernel/v4.x/

never complete, which indicates a liveness bug.                       linux-4.3.6.tar.xz, directory kernel/rcu.


                                                                  9                                                         2018/11/26
Bug 6 In this bug-injection scenario, CPUs are aware of               attempts resulted in SAT formulas that were so large that
the need for quiescent states, and they also record them lo-          CBMC ran out of memory. After the optimizations described
cally. However, they are prevented from reporting them up             in the remainder of this section, the largest formula con-
the rcu node tree, which again prevents grace periods from            tained around 90 million variables and 450 million clauses,
ever completing. This bug modifies function rcu report                which enabled CBMC to run to completion.
qs rnp() to return immediately (line 2227 in tree.c). This                First, instead of placing the scheduling-clock interrupt in
prevents RCU from walking up the rcu node tree, thus pre-             its own thread, we invoke functions rcu note context
venting grace periods from ending. This is again a liveness           switch() and rcu process callbacks() directly, as de-
violation similar to Bug 2.                                           scribed in Section 5. Also, we invoke note gp changes()
                                                                      from rcu gp init() to notify each CPU of a new grace pe-
Bug 7 Where Bug 6 prevents quiescent states from be-                  riod, instead of invoking rcu process callbacks().
ing reported up the rcu node tree, this bug-injection sce-                Second, the support for linked lists in CBMC version 5.4
nario causes quiescent states to be reported up the tree              is limited, resulting in unreachable code in CBMC’s sym-
prematurely, before all the CPUs covered by a given sub-              bolic execution. Thus, we stubbed all the list-related code in
tree have all reported quiescent states. To this end, in              our RCU model, including those for callback handling.
rcu report qs rnp(), we remove the if-block check-                        Third, CBMC’s structure-pointer and array encodings re-
ing for rnp->qsmask != 0 || rcu preempt blocked                       sult in large formulas and long formula-generation times.
readers cgp(rnp) (line 2251 in tree.c). Then the tree-                Our focus on the RCU-sched flavor allowed us to eliminate
walking process will not stop until it reaches the root, re-          RCU-BH’s data structures and trivialize the for each rcu
sulting in too-short grace periods. This is therefore a safety        flavor() flavor-traversal loops. Our focus on small num-
violation similar to Bug 1.                                           bers of CPUs meant that RCU-sched’s rcu node tree con-
Bugs 2 and 3 would result in a too-short grace period given           tained only a root node, so we also trivialized the rcu for
quiescent-state forcing, but such forcing falls outside the           each node breadth first() loops traversing this tree.
scope of this paper.                                                      Fourth, CBMC unwinds each loop to the depth specified
6.2   Validating the RCU Model in User-Space                          in its command line option --unwind, even when the actual
                                                                      loop depth is smaller. This unnecessarily increases formula
To validate our RCU model before performing verification              size, especially for loops containing intricate RCU code.
using CBMC, we executed it in user space. We performed                Since loops in our model can be decided at compile time,
1000 runs for each scenario in Section 6.1 using a 60 s               we therefore used the command line option --unwindset
timeout to wait for the end of a grace period and a random            to specify unwinding depths for each individual loop.
delay between 0 to 1 s in the RCU reader task.                            Finally, since our test harness only requires one rcu
   The results are reported in Table 1. Column 1 gives                node structure and two rcu data structures, we can use 32-
the verification scenarios. Scenario Prove tests our RCU              bit encodings for int, long, and pointers by using the com-
model without bug injection. Scenario Prove-GP tests a                mand line option --ILP32. This reduces CBMC’s formula
weak form of liveness by replacing Figure 2’s assertion               size by half compared to the 64-bit default.
with assert(0) as described in Section 6.1. The next three
columns present the number and the percentage of success-
ful, failing, and timeout runs, respectively. The following           6.4   Results and Discussion
two columns give the maximum memory consumption and                   Table 2 presents the results of our experiments applying
the total runtime. The last column explains the results.              CBMC version 5.4 to verify our RCU model. Scenario Prove
   As expected, for scenario Prove, the user program ran to           verifies our RCU model without bug injection over Sequen-
completion successfully in all runs. For Prove-GP, it was             tial Consistency (SC). We also exercise the model over the
able to detect the end of a grace period by triggering an             weak memory models TSO and PSO in scenarios Prove-
assertion violation in all the runs. For Bug 1, an assertion          TSO and Prove-PSO, respectively. Scenario Prove-GP per-
violation was triggered in 559 out of 1000 runs. For Bugs             forms the same reachability check as in Section 6.2 over
2–6, the user program timed out in all the runs, thus a grace         SC. We perform the same reachability verification over TSO
period did not complete. For Bug 7 with one reader thread,            and PSO in scenarios Prove-GP-TSO and Prove-GP-PSO,
the testing harness failed to trigger an assertion violation.         respectively. Scenarios Bug 1–7 are the bug-injection scenar-
However, we were able to observe a failure in 242 out of              ios discussed in Section 6.1, and are verified over SC, TSO
1000 runs with two reader threads.                                    and PSO. Columns 2–4 give the number of constraints (sym-
                                                                      bolic program expressions and partial orders), variables, and
6.3   Getting CBMC to work on Tree RCU                                clauses of the generated formula. The next three columns
We have found that getting CBMC to work on our RCU                    give the maximum (virtual) memory consumption, solver
model is non-trivial due to Tree RCU’s complexity com-                runtime, and total runtime of our experiments. The final col-
bined with CBMC’s bit-precise verification. In fact, early            umn gives the verification result.


                                                                 10                                                         2018/11/26
                              Successful             Failing                               Max
              Scenario           Runs                 Runs               Timeouts           VM        Time            Result
             Prove         1,000 (100.0%)           0      (0.0%)        0    (0.0%)      362 MB          4m           Safe
             Prove-GP          0     (0.0%)     1,000 (100.0%)           0    (0.0%)      362 MB          5m      GP Completed
             Bug 1           461   (46.1%)        539     (53.9%)        0    (0.0%)      362 MB          6m    Assertion Violated
             Bug 2             0     (0.0%)         0      (0.0%)    1,000 (100.0%)       362 MB     16h 40m         GP Hung
             Bug 3             0     (0.0%)         0      (0.0%)    1,000 (100.0%)       362 MB     16h 40m         GP Hung
             Bug 4             0     (0.0%)         0      (0.0%)    1,000 (100.0%)       362 MB     16h 40m         GP Hung
             Bug 5             0     (0.0%)         0      (0.0%)    1,000 (100.0%)       362 MB     16h 40m         GP Hung
             Bug 6             0     (0.0%)         0      (0.0%)    1,000 (100.0%)       362 MB     16h 40m         GP Hung
             Bug 7 (1R)        0     (0.0%)         0      (0.0%)    1,000 (100.0%)       362 MB     16h 40m    Safe (Bug Missed)
             Bug 7 (2R)      758   (75.8%)        242     (24.2%)        0    (0.0%)      370 MB          5m    Assertion Violated

                              Table 1: Experimental Results of Testing the RCU Model in User-Space

                                                                               Max     Solver    Total
                      Scenario         #Const    #Variable     #Clause         VM      Time      Time            Result
                  Prove                 5.2m      30.0m        149.7m         23 GB    9h 24m    9h 36m           Safe
                  Prove-TSO             5.6m      42.0m        210.7m         34 GB   10h 51m    11h 4m           Safe
                  Prove-PSO             5.6m      41.3m        207.0m         34 GB   11h 23m   11h 36m           Safe
                  Prove-GP              5.4m      30.6m        152.7m         24 GB    3h 52m     4h 5m      GP Completed
                  Prove-GP-TSO          5.6m      42.0m        210.7m         34 GB    13h 1m   13h 14m      GP Completed
                  Prove-GP-PSO          5.6m      41.3m        207.0m         34 GB    8h 24m    8h 37m      GP Completed
                  Bug 1                 1.3m      11.7m         56.0m         8 GB        31m       33m    Assertion Violated
                  Bug 1-TSO             1.5m      17.1m         83.3m         13 GB       53m       56m    Assertion Violated
                  Bug 1-PSO             1.5m      16.5m         80.4m         12 GB       46m       48m    Assertion Violated
                  Bug 2                 5.2m      30.0m        149.6m         23 GB    4h 25m    4h 37m         GP Hung
                  Bug 2-TSO             5.6m      42.0m        210.5m         34 GB    9h 57m   10h 10m         GP Hung
                  Bug 2-PSO             5.6m      41.2m        206.9m         34 GB    8h 51m     9h 4m         GP Hung
                  Bug 3                 6.3m      34.8m        174.1m         28 GB    7h 11m    7h 25m         GP Hung
                  Bug 3-TSO             6.8m      48.7m        245.1m         41 GB   19h 40m   19h 55m         GP Hung
                  Bug 3-PSO             6.7m      48.0m        241.2m         41 GB   19h 19m   19h 35m         GP Hung
                  Bug 4                 4.8m      27.8m        138.1m         22 GB     4h 3m    4h 14m         GP Hung
                  Bug 4-TSO             5.1m      38.4m        192.6m         31 GB    8h 18m    8h 30m         GP Hung
                  Bug 4-PSO             5.1m      37.7m        188.9m         31 GB    8h 14m    8h 26m         GP Hung
                  Bug 5                 5.1m      29.5m        146.7m         23 GB     4h 6m    4h 18m         GP Hung
                  Bug 5-TSO             5.5m      41.2m        206.5m         34 GB    5h 46m    5h 59m         GP Hung
                  Bug 5-PSO             5.4m      40.5m        202.9m         33 GB    5h 42m    5h 55m         GP Hung
                  Bug 6                 1.4m      13.1m         63.3m         9 GB        19m       21m         GP Hung
                  Bug 6-TSO             1.5m      17.2m         84.1m         13 GB    1h 32m    1h 33m         GP Hung
                  Bug 6-PSO             1.5m      16.7m         81.4m         12 GB    1h 22m    1h 24m         GP Hung
                  Bug 7 (1R)            5.0m      29.2m        145.3m         23 GB    8h 48m         9h   Safe (Bug Missed)
                  Bug 7-TSO (1R)        5.2m      40.1m        200.8m         32 GB    11h 6m   11h 18m    Assertion Violated
                  Bug 7-PSO (1R)        5.1m      39.4m        197.2m         32 GB   11h 32m   11h 44m    Assertion Violated
                  Bug 7 (2R) ∗         15.1m      71.2m        359.0m         59 GB    19h 2m   19h 40m    Assertion Violated
                  Bug 7-TSO (2R) ∗     15.6m      90.4m        456.9m         75 GB   78h 12m   78h 53m    Assertion Violated
                  Bug 7-PSO (2R) ∗     15.6m      89.3m        451.6m         75 GB   84h 21m    85h 2m     Out of Memory
     * This experiment was performed on a 64-bit machine running Linux 3.19.8 with twelve Intel Xeon 2.40 GHz cores and 96 GB of main memory

                                                Table 2: Experimental Results of CBMC


    Since Tree RCU’s implementation in the Linux kernel                        due to the approximation of the scheduling-clock interrupt
is sophisticated, its test suite is non-trivial [17], comprising               by a direct function call, as described in Section 5. How-
several thousand lines of code. Therefore, it comes as little                  ever, CBMC did report a violation of the assertion either
surprise that its verification is challenging.                                 when two RCU reader threads were present or when run over
    In our experiments, CBMC returned all the expected re-                     TSO or PSO. All of these cases decrease determinism, which
sults except for Bug 7, for which it failed to report a viola-                 in turn more faithfully model non-deterministic scheduling-
tion of the assertion assert(r2 == 0 || r1 == 1) with                          clock interrupts, allowing the assertion to be violated.
one RCU reader thread running over SC. This failure was


                                                                         11                                                              2018/11/26
             SC    TSO     PSO
                                                                             108           SC        TSO     PSO
  7
10




106                                                                          107
        e




                                                           7
               P


                     1


                            2


                                  3


                                        4


                                               5


                                                     6




                                                                   2R
      ov


               G




                                                            g
                      g


                            g


                                 g


                                         g


                                               g


                                                     g




                                                                                     e




                                                                                                                                                           7
                                                                                            P


                                                                                                      1


                                                                                                             2


                                                                                                                       3


                                                                                                                               4


                                                                                                                                         5


                                                                                                                                                 6




                                                                                                                                                                    2R
                                                                  7-
                                                         Bu
                   Bu


                          Bu


                                 Bu


                                      Bu


                                             Bu


                                                   Bu
              e-
     Pr




                                                                                   ov


                                                                                             G




                                                                                                                                                         g
                                                                                                     g


                                                                                                             g


                                                                                                                       g


                                                                                                                                g


                                                                                                                                       g


                                                                                                                                                g
            ov




                                                                   g




                                                                                                                                                                  7-
                                                                                                                                                       Bu
                                                                                                  Bu


                                                                                                            Bu


                                                                                                                   Bu


                                                                                                                             Bu


                                                                                                                                    Bu


                                                                                                                                               Bu
                                                                                           e-
                                                                               Pr
                                                                Bu
          Pr




                                                                                         ov




                                                                                                                                                                g
                                                                                                                                                              Bu
                                                                                      Pr
     Figure 7: Number of Constraints in the SAT Formulas
                                                                                   Figure 8: Number of Variables in the SAT Formulas


                                                                                            SC        TSO        PSO
    CBMC took more than 9 hours to verify our model over
                                                                             108.5
SC (scenario Prove). The resulting SAT formulas have more
than 5m constraints, 30m variables and 149m clauses, and
occupy 23 GB of memory. The formulas for scenarios Prove-
                                                                              108
TSO and Prove-PSO are about 40% larger than the sce-
nario Prove. They have more than 40m variables and 200m
clauses, and took more than 11 hours and 33 GB memory
to solve. Although this verification consumed considerable
                                                                                       e




                                                                                                                                                              7
                                                                                                 P


                                                                                                         1


                                                                                                                 2


                                                                                                                           3


                                                                                                                                    4


                                                                                                                                            5


                                                                                                                                                      6




                                                                                                                                                                       2R
                                                                                     ov


                                                                                              G




                                                                                                                                                             g
                                                                                                       g


                                                                                                               g


                                                                                                                         g


                                                                                                                                g


                                                                                                                                           g


                                                                                                                                                   g




                                                                                                                                                                     7-
                                                                                                                                                          Bu
                                                                                                     Bu


                                                                                                             Bu


                                                                                                                       Bu


                                                                                                                               Bu


                                                                                                                                        Bu


                                                                                                                                                Bu
                                                                                             e-
                                                                                   Pr

                                                                                           ov




                                                                                                                                                                   g
memory and CPU, it verified all possible executions and re-




                                                                                                                                                                 Bu
                                                                                         Pr
orderings permitted by TSO and PSO, a tiny subset of which
are reached by the rcutorture test suite.
                                                                                   Figure 9: Number of Clauses in the SAT Formulas
    CBMC proved that grace periods can end (i.e., assert(0)
is violated), over SC (Prove-GP), TSO (Prove-GP-TSO), and
PSO (Prove-GP-PSO). The sizes of resulting formulas and                                    SC        TSO     PSO
memory consumption are similar to those of the three Prove
                                                                             105
scenarios. However, it took CBMC only about 4, 13, and
8.5 hours to find an violation of assert(0) in Prove-GP,
Prove-GP-TSO, and Prove-GP-PSO, respectively.                                104

    For the bug-injection scenarios described in Section 6.1,
CBMC was able to return the expected results in all scenar-                  103
ios over SC except for Bug 7, as noted earlier. The formula
                                                                                     e




                                                                                                                                                           7
                                                                                            P


                                                                                                      1


                                                                                                             2


                                                                                                                       3


                                                                                                                               4


                                                                                                                                         5


                                                                                                                                                 6




                                                                                                                                                                    2R
                                                                                   ov


                                                                                           G




size varies from scenario to scenario, with 27m–35m vari-
                                                                                                                                                          g
                                                                                                     g


                                                                                                             g


                                                                                                                       g


                                                                                                                               g


                                                                                                                                        g


                                                                                                                                                  g




                                                                                                                                                                  7-
                                                                                                                                                       Bu
                                                                                                  Bu


                                                                                                            Bu


                                                                                                                   Bu


                                                                                                                             Bu


                                                                                                                                    Bu


                                                                                                                                               Bu
                                                                                           e-
                                                                               Pr

                                                                                         ov




                                                                                                                                                                 g
                                                                                                                                                              Bu
                                                                                      Pr




ables and 138m–174m clauses. The runtime was 4–9 hours
and memory consumption exceeded 22 GB. The exceptions
are Bugs 1 and 6, which have fewer than 14m variables and                                     Figure 10: Total Runtime in Seconds
64m clauses, and took less than 35 mins and about 9 GB of
memory to solve. This reduction was due to the large amount
of code removed by the bug injections in these scenarios.                    102
                                                                                           SC        TSO     PSO
    Figures 7–9 compare the formula size between SC, TSO
and TSO. Comparison of runtime and memory can be found
in Figures 10 and 11. As we can see, the runtime and mem-
ory overhead for the TSO and PSO variants of a given exper-
iment are quite similar. The overheads of TSO are slightly                   101
higher than those of PSO in all bug-injection scenarios ex-
cept for Bug 7 on which PSO had longer runtime. How-
                                                                                     e




                                                                                                                                                           7
                                                                                            P


                                                                                                      1


                                                                                                             2


                                                                                                                       3


                                                                                                                               4


                                                                                                                                         5


                                                                                                                                                 6




                                                                                                                                                                    2R
                                                                                   ov




ever, the overhead of TSO and PSO is significantly larger
                                                                                           G




                                                                                                                                                         g
                                                                                                     g


                                                                                                             g


                                                                                                                       g


                                                                                                                                g


                                                                                                                                       g


                                                                                                                                                g




                                                                                                                                                                  7-
                                                                                                                                                       Bu
                                                                                                  Bu


                                                                                                            Bu


                                                                                                                   Bu


                                                                                                                             Bu


                                                                                                                                    Bu


                                                                                                                                               Bu
                                                                                           e-
                                                                               Pr

                                                                                         ov




                                                                                                                                                                g
                                                                                                                                                              Bu




than that of SC, with up to 340% (Bug 6 runtime) and 50%
                                                                                      Pr




(Bug 1 memory) increases. The runtime was 5–19 hours and
memory consumption exceeded 31 GB in all scenarios ex-                       Figure 11: Maximum Memory Consumption in Gigabytes
cept Bug 1 and 6. The numbers of variables and clauses


                                                                        12                                                                                  2018/11/26
are 37m–49m and 188m–245m, respectively, around 130%                    of which was hiding a real bug in Tasks RCU [8] and the
greater than SC.                                                        other of which was hiding a minor performance bug in Tree
   The two-reader variant of Bug 7 has by far the longest               RCU.
runtime, consuming more than 19 hours and 78 hours                          In this work, we use CBMC to verify the implementation
over SC and TSO, respectively, comparing to 9 hours and                 of Linux-kernel Tree RCU for multi-core systems, which is
11 hours with one reader. It also consumed about 75 GB                  more complex and sophisticated, over SC, TSO, and PSO.
memory, more than double the one-reader variant. For PSO,                   Gotsman et al. [11] use an extended concurrent separation
with two reader threads CBMC’s solver ran out of memory                 logic to formalize the concept of grace period and prove
after 85 hours whereas with one reader it completed in less             an abstract implementation of RCU over SC. Tassarotti et
than 12 hours. The increased overhead is due to the addi-               al. [24] use GPS, a recently developed program logic for the
tional RCU reader’s call to rcu process callbacks().                    C/C++11 memory model, to carry out a formal proof of a
This in turn results in more than a 125% increase in the                simple implementation of user-level RCU for a singly-linked
number of constraints, variables, and clauses. For example,             list. They assuma the “release-acquire” semantics, which is
the two-reader TSO formula has triple the constraints and               weaker than SC but stronger than memory models used by
double the variables and clauses of the one-reader case.                real-world RCU implementations. These formal proofs are
                                                                        performed manually on simple implementations of RCU.
                                                                        By contrast, our work applies an automated verification tool
7.   Related Work
                                                                        with a test harness to verify the grace-period property of a
McKenney has applied the SPIN model checker to ver-                     real-world implementation of RCU over SC, TSO, and PSO.
ify RCU’s NO HZ FULL SYSIDLE functionality [19], and                        Formal verification has started to make its way into real-
interactions between dyntick-idle and non-maskable inter-               world practice of verifying large non-trivial code bases. Cal-
rupts [18]. Desnoyers et al. [10] propose a virtual architec-           cagno et al. [5] describe integrating a static-analysis tool
ture to model out-of-order memory accesses and instruction              into Facebook’s software development cycle. Malacaria et
scheduling. User-level RCU [9] is modeled and verified in               al. [16] apply CBMC to analyze information leakage of the
the proposed architecture using the SPIN model checker.                 OpenSSL implementation. We believe that our work is an
    These efforts require an error-prone translation from C to          important step towards integration of verification into Linux-
SPIN’s modeling language, and therefore are not appropriate             kernel RCU’s regression test suite.
for regression testing. By contrast, our work constructs an
RCU model directly from its source code from the Linux
kernel, and verifies it using automated verification tool.              8.   Conclusion
    Alglave et al. [3] introduce a symbolic encoding for ver-           This paper overviews the implementation of Tree RCU in
ifying concurrent software over a range of memory models                the Linux Kernel, and describes how to construct a model
including SC, TSO and PSO. They implement the encoding                  directly from its source code. It then shows how to use the
in the CBMC bounded model checker and use the tool to                   CBMC model checker to verify a significant part of the Tree
verify rcu assign pointer() and rcu dereference().                      RCU implementation automatically, which to the best of our
    McKenney has used CBMC to verify Tiny RCU [19], a                   knowledge is unprecedented. This work demonstrates that
trivial Linux-kernel RCU implementation for uni-core sys-               RCU is a rich example to drive research: it is small enough
tems. Roy has applied the same tool to verify a significant             to provide models that can just barely be verified by existing
portion of Sleepable RCU (SRCU). CBMC is now part of                    tools, but it also has sufficient concurrency and complexity
the regression test suite of SRCU in the Linux kernel [23].             to drive significant advances in techniques and tooling.
    Concurrently with our work, Kokologiannakis et al. ver-                 For future work, we plan to add quiescent-state forcing
ify Tree RCU using Nidhugg [15]. Since Nidhugg has better               and grace-period expediting into our model and verify their
list support and does not model data non-determinism, they              safety and liveness properties, using more sophisticated test
are able to verify more scenarios with less CPU and memory              harnesses that pass through multiple grace periods and op-
consumption. But some portions of RCU use atomic read-                  erate on a larger tree structure. We also plan to model and
modify-write operations that can give nondeterministic re-              verify the preemptible version of Tree RCU, which we ex-
sults. So we hypothesize that data non-determinism will be              pect to be quite challenging. Moreover, there is much fertile
required to verify RCU’s dyntick-idle and rcu barrier()                 ground verifying uses of RCU in the Linux kernel, for ex-
components.                                                             ample, the Virtual File System (VFS).
    Groce et al. [12] introduce a falsification-driven verifica-            There are also potential improvements for CBMC to bet-
tion methodology that is based on a variation of mutation               ter support future RCU verification efforts. For instance, bet-
testing. By using CBMC, they are able to find two holes                 ter support of lists is required to verify RCU’s callback han-
in rcutorture–RCU’s stress testing suite, one of which                  dling mechanism. A field-sensitive SSA encoding for struc-
was hiding a real bug in Tiny RCU. Further work on real                 tures and a thread-aware slicer will help reduce encoding
hardware has identified two more rcutorture holes, one                  size, and therefore improve scalability.


                                                                   13                                                         2018/11/26
   This work demonstrates the nascent ability of SAT-based                    Proceedings of the 30th IEEE/ACM International Conference
formal-verification tools to handle real-world production-                    on Automated Software Engineering (ASE), pages 737–748.
quality synchronization primitives, as exemplified by Linux-                  IEEE Computer Society, 2015.
kernel Tree RCU on weakly ordered TSO and PSO systems.                   [13] G. J. Holzmann. The model checker SPIN. IEEE
Although modeling weak ordering incurs a significant per-                     Transaction of Software Engineering, 23(5):279–295, 1997.
formance penalty, this penalty is not excessive. We there-               [14] L. Jiangshan. [RFC][PATCH] rcu classic: new algorithm for
fore hypothesize that use of these tools for highly concur-                   callbacks-processing. Available: Linux-kernel git SHA-1
rent multithreaded software will reach mainstream within 3-                   5127bed588a2 [Viewed July 9, 2016], June 2008.
5 years, especially given recent rates of improvement.                   [15] M. Kokologiannakis and K. Sagonas. Stateless model
                                                                              checking of the Linux kernels hierarchical
References                                                                    Read-Copy-Update (Tree RCU). In SPIN, 2017.
 [1] The Linux kernel. https://www.kernel.org/.                          [16] P. Malacaria, M. Tautschnig, and D. Distefano. Information
                                                                              leakage analysis of complex C code and its application to
 [2] Where is the Internet? http://www.whoishostingthis.                      openssl. In Proceedings of the 7th International Symposium
     com/blog/2013/12/06/internet-infographic/,                               on Leveraging Applications of Formal Methods, Verification
     December 2013.                                                           and Validation (ISOLA), volume 9952 of LNCS, pages
 [3] J. Alglave, D. Kroening, and M. Tautschnig. Partial orders               909–925, 2016.
     for efficient bounded model checking of concurrent software.        [17] P. E. McKenney. [PATCH] RCU torture testing. Available:
     In Proceedings of the 25th International Conference on                   http://lkml.kernel.org/g/20051001182056.
     Computer Aided Verification (CAV), volume 8044 of LNCS,                  GA1613@us.ibm.com [Viewed July 9, 2016], October 2005.
     pages 141–157. Springer, 2013.
                                                                         [18] P. E. McKenney. Integrating and validating dynticks and
 [4] J. R. Burch, E. M. Clarke, K. L. McMillan, D. L. Dill, and               preemptable RCU.
     L. J. Hwang. Symbolic model checking: 1020 states and                    https://lwn.net/Articles/279077/, April 2008.
     beyond. Information and Computation, 98(2):142–170, 1992.
                                                                         [19] P. E. McKenney. Verification challenges. http://paulmck.
 [5] C. Calcagno, D. Distefano, J. Dubreil, D. Gabi,                          livejournal.com/tag/verification%20challenge,
     P. Hooimeijer, M. Luca, P. W. O’Hearn, I. Papakonstantinou,              April 2015.
     J. Purbrick, and D. Rodriguez. Moving fast with software
                                                                         [20] P. E. McKenney and J. D. Slingwine. Read-copy update:
     verification. In Proceedings of the 7th NASA Formal Methods
                                                                              Using execution history to solve concurrency problems. In
     Symposium (NFM), volume 9058 of LNCS, pages 3–11.
                                                                              Proceedings of the 10th International Conference on Parallel
     Springer, 2015.
                                                                              and Distributed Computing and Systems, pages 509–518,
 [6] J. Callaham. Google says there are now 1.4 billion active                1998.
     Android devices worldwide.
                                                                         [21] P. E. McKenney and J. Walpole. Introducing technology into
     http://www.androidcentral.com/
                                                                              the Linux kernel: a case study. ACM SIGOPS Operating
     google-says-there-are-now-14-billion-active-
                                                                              Systems Review, 42(5):4–17, 2008.
     android-devices-worldwide, September 2015.
                                                                         [22] P. E. McKenney, S. Boyd-Wickizer, and J. Walpole. RCU
 [7] E. M. Clarke, D. Kroening, and F. Lerda. A tool for checking
                                                                              usage in the Linux kernel: One decade later. Technical
     ANSI-C programs. In Proceedings of the 10th International
                                                                              Report, 2013.
     Conference on Tools and Algorithms for the Construction
     and Analysis of Systems (TACAS), volume 2988 of LNCS,               [23] L. Roy. rcutorture: Add CBMC-based formal verification for
     pages 168–176. Springer, 2004.                                           SRCU. https:
                                                                              //www.spinics.net/lists/kernel/msg2421833.html,
 [8] J. Corbet. The RCU-tasks subsystem.
                                                                              2017.
     http://lwn.net/Articles/607117/, July 2014.
                                                                         [24] J. Tassarotti, D. Dreyer, and V. Vafeiadis. Verifying
 [9] M. Desnoyers, P. E. McKenney, A. S. Stern, M. R. Dagenais,
                                                                              read-copy-update in a logic for weak memory. In
     and J. Walpole. User-level implementations of read-copy
                                                                              Proceedings of the 36th ACM SIGPLAN Conference on
     update. IEEE Transactions on Parallel and Distributed
                                                                              Programming Language Design and Implementation (PLDI),
     Systems, 23(2):375–382, 2012.
                                                                              pages 110–120. ACM, 2015.
[10] M. Desnoyers, P. E. McKenney, and M. R. Dagenais.
     Multi-core systems modeling for formal verification of
     parallel algorithms. ACM SIGOPS Operating Systems
     Review, 47(2):51–65, 2013.
[11] A. Gotsman, N. Rinetzky, and H. Yang. Verifying concurrent
     memory reclamation algorithms with grace. In Proceedings
     of the 22nd European Symposium on Programming (ESOP),
     volume 7792 of LNCS, pages 249–269. Springer, 2013.
[12] A. Groce, I. Ahmed, C. Jensen, and P. E. McKenney. How
     verified is my code? Falsification-driven verification. In


                                                                    14                                                           2018/11/26
