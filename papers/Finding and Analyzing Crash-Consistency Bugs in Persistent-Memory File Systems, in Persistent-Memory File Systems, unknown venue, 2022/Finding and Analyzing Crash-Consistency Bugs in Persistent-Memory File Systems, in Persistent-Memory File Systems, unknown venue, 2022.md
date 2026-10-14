                                                                    Finding and Analyzing Crash-Consistency Bugs
                                                                          in Persistent-Memory File Systems
                                                   Hayley LeBlanc                            Shankara Pailoor                                 Isil Dillig
                                              University of Texas at Austin             University of Texas at Austin                University of Texas at Austin
                                                          James Bornholt                                        Vijay Chidambaram
                                                    University of Texas at Austin               University of Texas at Austin and VMware Research
arXiv:2204.06066v1 [cs.OS] 12 Apr 2022




                                                                  Abstract                                     crash consistency testing tools like CrashMonkey [38] or Hy-
                                                                                                               dra [27] are not compatible with the unique storage stack of
                                         We present a study of crash-consistency bugs in persistent-
                                                                                                               PM file systems where the media is directly accessed using
                                         memory (PM) file systems and analyze their implications
                                                                                                               processor load and store instructions at fine granularity.
                                         for file-system design and testing crash consistency. We de-
                                         velop F LY T RAP, a framework to test PM file systems for                This paper makes two contributions. First, it presents F LY-
                                         crash-consistency bugs. F LY T RAP discovered 18 new bugs             T RAP, a framework for testing the crash consistency of PM
                                         across four PM file systems; the bugs have been confirmed             file systems (§3). Given a workload, and a target PM file sys-
                                         by developers and many have been already fixed. The dis-              tem, F LY T RAP simulates crashes at different points in the
                                         covered bugs have serious consequences such as breaking               workload, creating crash states reflecting the on-PM state
                                         the atomicity of rename or making the file system unmount-            after the crash; F LY T RAP then mounts the target PM file
                                         able. We present a detailed study of the bugs we found and            system on the crash state, and checks if it recovers correctly.
                                         discuss some important lessons from these observations. For           F LY T RAP does not require modifying the file system im-
                                         instance, one of our findings is that many of the bugs are            plementation, and is compatible with all PM file systems
                                         due to logic errors, rather than errors in using flushes or           that implement the POSIX interface. To choose workloads
                                         fences; this has important applications for future work on            to test, we couple F LY T RAP with a modified version of the
                                         testing PM file systems. Another key finding is that many             ACE [38] workload generator and the Syzkaller [7] gray-box
                                         bugs arise from attempts to improve efficiency by perform-            fuzzer. While ACE systematically generates small workloads
                                         ing metadata updates in-place and that recovery code that             for F LY T RAP to test, Syzkaller generates random workloads
                                         deals with rebuilding in-DRAM state is a significant source           driven by code coverage.
                                         of bugs. These observations have important implications for              Second, this paper presents an analysis of 18 unique bugs
                                         designing and testing PM file systems. Our code is available          found by F LY T RAP across four PM file systems (§5). We
                                         at https://github.com/utsaslab/flytrap.                               have reported all 18 bugs upstream; all except the two bugs in
                                                                                                               PMFS (which is not actively maintained) have been confirmed
                                                                                                               by their developers, and 12 have already been fixed. The bugs
                                         1   Introduction                                                      have severe consequences such as breaking the atomicity of
                                                                                                               the rename() system call that applications depend on for
                                         Persistent memory (PM) is a new storage-class memory
                                                                                                               atomic updates [40]. To the best of our knowledge, this is the
                                         technology that offers extremely low-latency persistent stor-
                                                                                                               largest published corpus of PM file-system crash-consistency
                                         age and fine-grained access to storage over the memory
                                                                                                               bugs; analyzing it yields useful insights for both PM file-
                                         bus [22,47]. PM technology has long been a focus of research,
                                                                                                               system design and efficient crash-consistency testing of PM
                                         and more recently has been commercialized by Intel [3]. A
                                                                                                               file systems. For example, we observe that many bugs are
                                         number of file systems [8, 14, 17, 18, 24, 25, 28, 43, 45] have
                                                                                                               logic or design issues in performance optimizations rather
                                         been developed that exploit PM’s advantages to build faster,
                                                                                                               than the missing flush/fence bugs that many PM bug-finding
                                         safer storage systems.
                                                                                                               tools target [5, 16, 19, 21, 31–33, 39].
                                            One of the main responsibilities of a file system is to keep
                                         the user’s data safe in the event of a crash due to a power           Why is testing crash-consistency for PM file systems
                                         loss or a kernel bug. To do so, the file system should be             hard? The unique architecture of PM file systems creates two
                                         crash consistent: it should recover after the failure to a con-       challenges for effective testing. The first challenge is to inter-
                                         sistent state without losing data the user expected to be per-        cept writes to the storage media. Existing crash-consistency
                                         sistent [11, 12, 20, 41]. However, there are no open-source           testing tools such as CrashMonkey [38] intercept writes at the
                                         tools that can test whether a PM file system is crash consis-         block layer, but PM file systems remove this natural intercep-
                                         tent without annotating or modifying the file system. Existing        tion point. Instead, they write directly to the media using pro-


                                                                                                           1
cessor store instructions, which would be prohibitively expen-          invalidate the hypothesis, we also use the Syzkaller [7] gray-
sive to instrument and require reasoning about the CPU cache            box kernel fuzzer that can generate longer, more complex
hierarchy and store reordering to model faithfully. The second          workloads. We modify Syzkaller to only consider file-system-
challenge is choosing which crash states to test. CrashMon-             related system calls and to include recovery code when mea-
key and Hydra [27] only simulate crashes after system calls             suring code coverage.
have returned, as most file systems only make strong crash-             Testing results and observations. We use F LY T RAP to test
consistency guarantees after fsync() or sync() calls. PM                four open-source in-kernel PM file systems: PMFS [18],
file systems take advantage of the low-latency, fine-grained            NOVA [45], NOVA-Fortis [46], and WineFS [24]. F LY T RAP
media to offer stronger consistency guarantees by making                finds 18 unique bugs across the four file systems, with two
every file-system operation synchronous and durable. This               bugs present both in PMFS and WineFS (which builds on
means that to find crash consistency bugs, we must test crashes         PMFS). From these results, we draw some common observa-
in the middle of system calls. The fine granularity of PM               tions about PM file systems and how to test them:
writes (8 bytes) also leads to more possible crash states than
traditional file systems with block-sized writes.                          • The CrashMonkey hypothesis about simple workloads
                                                                             finding many crash-consistency bugs also holds for PM
F LY T RAP. F LY T RAP tackles these challenges by exploiting                file systems: 15 of 18 bugs are found by the systematic
insights about the way PM file systems are built. To intercept               exploration of our modified ACE.
writes, we observe that the PM file systems we studied all
have centralized persistence functions that perform writes to              • A majority of the discovered bugs (11/18) could only be
PM, rather than using inline assembly at different points in                 found by simulating a crash in the middle of a system
the code. For example, there is a memcpy() implementation                    call, meaning that existing tools that test only between
that uses non-temporal stores to write to PM. F LY T RAP uses                system calls would not have been effective.
Kprobes [4] to intercept these functions and record write IOs              • While a number of recent tools focus on finding missing
without modifying the file system. Intercepting writes at the                or duplicate cache flushes and fences in PM applica-
function level rather than the instruction level greatly reduces             tions [5, 16, 19, 21, 31–33, 39], we found that a majority
overhead. We further reduce this overhead by noting that only                of the bugs (14/18) did not result from such issues, but
data that is explicitly flushed can be used to provide crash-                instead from mistakes in logic (e.g., a metadata item that
consistency guarantees. Rather than intercepting all writes,                 was not added to a transaction).
F LY T RAP only tracks writes that are explicitly flushed or are
written with non-temporal stores.                                          • PM file systems increase performance by maintaining
                                                                             some data structures only in DRAM, and rebuilding them
   To choose which crash states to test, we build on this higher-
                                                                             when the file system is mounted [24, 25, 45]; F LY T RAP
level interception as well as empirical results about the write
                                                                             found seven bugs in such code.
patterns of PM file systems. Intercepting at the function level
allows us to see an entire file-system-level write at once, and            • Six bugs arose from developers trying to increase per-
so we can coalesce individual 8-byte stores when appropriate;                formance by updating metadata in-place, which is much
for example, we need not test each 8-byte write of a 1 MB                    easier to do with the fine-grained access model of PM,
write() call separately. We also observe that the set of in-                 rather than inside a transaction.
flight writes (writes in volatile caches that have not yet been
                                                                           • NOVA-Fortis [46] contains a number of features not
flushed) at any point in a system call is typically small, re-
                                                                             present in NOVA [45] that are intended to increase re-
ducing the number of crash states F LY T RAP must explore.
                                                                             silience; interestingly, F LY T RAP found five bugs in these
Finally, we observe that the order in which non-overlapping
                                                                             complex features.
in-flight writes are written to PM does not matter, and so
F LY T RAP only considers different subsets of in-flight writes           The analysis contains a number of other observations, along
being persisted rather than all permutations.                           with a discussion of their implications. To the best of our
                                                                        knowledge, this is the first such analysis of crash-consistency
Generating workloads. Given a workload, F LY T RAP pro-                 bugs in PM file systems.
vides a mechanism to generate and test crash states; an or-
thogonal question is deciding which workloads to explore.               In summary, this paper makes the following contributions:
CrashMonkey [38] hypothesized that systematically explor-                  • A set of tools to test crash-consistency of PM file sys-
ing small workloads on small file system states was effective                tems, including the F LY T RAP framework (§3)
in finding crash-consistency bugs; we sought to test this hy-              • A corpus of 18 crash-consistency bugs discovered by
pothesis for PM file systems. We modify the Automatic Crash                  these tools across four PM file systems (§4)
Explorer (ACE) workload generator from CrashMonkey to                      • An analysis of discovered crash-consistency bugs, with
account for the fact that system calls are synchronous in the                insights for PM file-system design and crash-consistency
tested systems, eliminating the need for fsync(). To try to                  testing (§5)


                                                                    2
2   Background and Motivation                                          the page cache, before hitting the storage media. In the case
                                                                       of PM, writes are performed using processor stores, providing
This section describes file-system crash consistency. It then          a significantly shorter path from file system to storage media.
discusses why crash consistency is important, why testing it           Second, while traditional file systems buffer updates in mem-
for PM file systems is challenging, and why existing tools do          ory before writing them to storage, PM file systems tend to
not solve this problem.                                                synchronously write to persistent media given the low latency
                                                                       and high bandwidth of PM [18, 24, 25, 28]. As a result, every
Crash consistency. A file system is crash consistent if it
                                                                       system call leads to persistent writes, not just fsync() and
maintains a set of guarantees about its data and metadata
                                                                       sync().
after a crash due a power loss or a kernel bug [12, 20, 41].
For example, if there is a crash in the middle of a rename()           These design decisions lead to two challenges when testing
system call, the POSIX standard requires that the file system          PM file systems for crash consistency:
after recovery should have the file in either the old name or
the new name; in other words, rename must be atomic even if               • Intercepting writes is challenging. Existing tools to test
there is a crash [6].                                                       crash-consistency intercept writes at the block layer and
   Many applications depend on the file system to be crash                  use the intercepted write I/O to construct crash states.
consistent [40]. Continuing with the rename example, many                   PM file systems remove this natural interception point.
applications including text editors such as emacs and vim use               PM file systems write to the persistent media using pro-
temporary files to store user data, and rename the temporary                cessor store instructions; the small granularity of the
files over the original files when the user saves the file. If              store instruction (8 bytes) also increases the number of
rename is not atomic, these applications can lose user data in              instructions that would need to be intercepted. A naive
a crash. Unexpected power loss occurs even in professionally-               solution such as intercepting each store instruction (even
managed data centers [34–37, 42, 44]. Thus, it is important to              if we could correctly identify stores to PM) would be
ensure that file systems are crash consistent.                              prohibitively expensive.

Persistent memory (PM). Persistent memory technology,                     • Increase in crash states to explore. While existing crash-
recently commercialized as Intel Optane DC Persistent Mem-                  consistency testing frameworks only simulate crashes at
ory [2,3], combines the properties of traditional storage media             system-call boundaries, testing PM file systems requires
and DRAM; it is byte-addressable and connected to the mem-                  simulating crashes in the middle of system calls. This is
ory bus like DRAM, but provides persistence like traditional                because PM file systems persist state synchronously in
storage media. Compared to DRAM, Optane PM provides                         file-system operations, instead of buffering them until
0.33× read bandwidth, 0.17× write bandwidth, 2–4× higher                    fsync(). The small granularity of writes also increases
read latency, and similar write latency.                                    the number of potential crash states resulting from each
   In the x86 programming model, PM is accessed via pro-                    write or metadata operation. Testing crash consistency
cessor load and store instructions. Writes to PM flow through               in PM file systems requires simulating crashes in the
the CPU cache hierarchy like any other memory store, and so                 middle of each file-system operation, versus just after
do not become immediately persistent. Data can be flushed                   fsync() or sync() calls.
from CPU caches to persistent media with cache line flush in-
structions (clfush, clflushopt, clwb), or can bypass cache             Why current tools are not enough. CrashMonkey [38] and
entirely with non-temporal stores (movnt). Because writes to           Hydra [27] can be used to check the crash consistency of
PM are processor stores, they are also subject to CPU store            traditional file systems. However, they only simulate crashes
reordering, and so must be surrounded by store fences when             at the end of system calls such as fsync() because that is
preserving order is important for consistency. We say that data        when persistence is guaranteed. However, PM file systems
whose cache line has been written back, or which was written           have stronger persistence guarantees, and we need to simulate
using non-temporal stores, is flushed to PM once a subse-              crashes in the middle of the system call, not only at the end.
quent store fence instruction has executed, as it is guaranteed        It is not straightforward to do this since the persistence guar-
to reach media before any future writes. We term a write that          antees are unclear when crashing in the middle of a system
has not yet been flushed to persistent media an in-flight write;       call. Moreover, CrashMonkey and Hydra cannot intercept PM
in-flight writes may be lost in the case of a crash. If there          writes.
are multiple in-flight writes, they may be written to persistent          Yat [29] is an internal tool used by Intel to test the crash
media in any order.                                                    consistency of PM software, including PM file systems. Yat
PM file systems. PM file systems differ from traditional file          uses a hypervisor-based recording technique to log all writes
systems in a few important aspects. First, traditional file sys-       to PM and reconstructs crash states to check. It produces
tems have a long software path for writes along the storage            an extremely large number of crash states; one of the three
stack; all writes go through the block layer, and most through         reported test workloads used with PMFS would take over five


                                                                   3
years to run fully. Yat is not open source, and the exact set of                          Persistence Functions for Target File System
bugs it found is not available.
   A number of tools are available for checking PM software
                                                                                                                                FlyTrap
for PM programming errors: errors associated with persist-                 ACE
ing data to PM, such as missing or unnecessary cache-line                workloads                        Crash state     Crash
                                                                                              Write
flushes or store fences [5, 16, 19, 21, 31–33, 39]. PMTest [33],                                                        Consistency
                                                                                             Logger         Oracle
                                                                         Syzkaller                                       Checker
XFDetector [32], Pmemcheck [5], and PMDebugger [16] re-                                                     state
                                                                         workloads
quire manual annotation, which we seek to avoid. All of them
are primarily focused on low-level PM programming errors
                                                                                                           Bug Report
or narrow classes of logic bugs that are directly related to
PM management. For example, Witcher [19] looks for fine-
grained “persistence atomicity violations” in which sequences          Figure 1: Architecture. Given a target file system and its
of writes to PM that are assumed to be atomic can be inter-            persistence functions, F LY T RAP uses workloads from both
rupted by a crash. Agamotto [39], which uses symbolic execu-           ACE and Syzkaller to test the file system. F LY T RAP produces
tion to track the state of PM, also allows developers to provide       bug reports with enough detail to reproduce the bug.
custom bug oracles to check for precise, low-level properties
about a program; for example, that a specific type of structure
is always modified within a transaction. We are interested in          given workload (a sequence of file-system operations) and
checking the higher-level crash consistency guarantees pro-            records the writes made by the file system. It then replays
vided by PM file systems and the POSIX interface without               these writes to create crash images, which represent the state
requiring specifications from developers, so these tools are           of the system if it had crashed at different points during the
not sufficient.                                                        workload. F LY T RAP constructs crash images for crash points
   In summary, there is a strong need for a tool that can be           both during and after system calls. F LY T RAP mounts the tar-
used to efficiently test PM file systems for crash consistency         get file system on the crash image, lets it recover, and then
without requiring manual annotations.                                  checks whether it has recovered to a consistent state. Consis-
                                                                       tency is workload-specific; for example, if the crash happened
                                                                       in the middle of a rename, F LY T RAP will check whether the
3     F LY T RAP                                                       old file or the new file exists. Both files missing or both files
                                                                       existing would result in a bug report. The bug report contains
We present F LY T RAP, a new framework to find crash-                  the workload, the crash point, the file-system state after crash,
consistency bugs in PM file systems. F LY T RAP tackles the            what was expected, and the file system and kernel version.
challenges outlined in §2 by exploiting two characteristics of
                                                                          The ACE workload generator is based on a hypothesis
PM file systems: centralized persistence functions and limited
                                                                       outlined in the CrashMonkey work [38]: that testing small
number of in-flight writes. F LY T RAP can be run on all PM file
                                                                       workloads (with a few file-system operations) on a newly
systems implementing the POSIX API, and it neither requires
                                                                       created file system is useful for finding crash-consistency
manual annotations nor modifying the file-system code.
                                                                       bugs. We use the ACE workload generator with F LY T RAP to
   F LY T RAP takes as input a workload to execute against
                                                                       test if this hypothesis holds for PM file systems. We modify
a chosen file system and outputs bug reports with enough
                                                                       ACE to take into account the properties of PM file systems,
details to reproduce the bug. We have developed two workload
                                                                       such as all operations being synchronous.
generators: one based on the ACE tool [38] for exhaustively
                                                                          To try to disprove the hypothesis, we also use the Syzkaller
enumerating file-system operations, and one based on the
                                                                       gray-box fuzzer to generate long, complex, and randomized
Syzkaller gray-box fuzzer [7]. Together, these tools offer an
                                                                       workloads for F LY T RAP. Syzkaller tries to generate random
automated and off-the-shelf approach for discovering bugs in
                                                                       tests that increase code coverage. We modified Syzkaller to
PM file systems.
                                                                       take the recovery code into account when calculating code
   This section first provides an overview of the end-to-end
                                                                       coverage.
bug finding process (§3.1). It then describes how F LY T RAP
                                                                          Finally, we cluster bug reports based on their text, such as
tackles the main challenges in testing PM crash consistency
                                                                       the error (e.g., missing file) and the workload. This allows us
(§3.2). It then presents the architecture of F LY T RAP (§3.3)
                                                                       to efficiently find and report unique bugs to developers.
and workload generators (§3.4), followed by a discussion of
the limitations of the framework (§3.5).
                                                                       3.2    Challenges
3.1    Overview
                                                                       F LY T RAP tackles the challenges in testing PM file systems
Figure 1 provides an overview of the F LY T RAP framework.             for crash consistency (§2) by exploiting two characteristics
F LY T RAP is a record and replay framework. It first runs a           of PM file systems.


                                                                   4
Intercepting writes. Intercepting the write traffic of a PM                         WORKLOAD
file system is more complex than a traditional file system                        rename(old, new)             Creating a crash state
because PM file systems do not use the usual block layer to                                                            with only
                                                                                               1                 first write applied
write data to the storage media, removing a convenient inter-
ception point. Instead, PM file systems use processor store,                      write: deleting old           write: deleting old
fence, and cache flush instructions directly. However, all in-
kernel PM file system implementations we examined include                           write: tx begin               write: tx begin
centralized persistence functions to interact with the PM de-
                                                                                 write: creating new     2     write: creating new
vice rather than directly using inline assembly at each write
location. In particular, every file system we evaluate in this pa-                  write: tx end                  write: tx end
per offered four persistence functions: non-temporal memcpy,
                                                                                  Sequence of writes
non-temporal memset, cache line flush, and store fence. These                                                                3
abstractions simplify reasoning about PM semantics and po-
tentially enable portability to other architectures.                                                     4
   We exploit this observation to simplify intercepting writes                   Bug Report: rename                 Crash State
by requiring the file system developer to provide F LY T RAP                         not atomic               with neither old or new
with annotations to identifies these four persistence functions
for their file system. F LY T RAP then automatically instruments
these functions at run time using the Kprobes [4] debugging              Figure 2: F LY T RAP workflow. The figure shows how crash
mechanism in the Linux kernel.                                           consistency is tested using a simple rename() workload. In
                                                                         this example, the old file being deleted is updated in-place,
Increased number of crash states. PM file systems make                   while the new file creation happens inside a transaction. 1)
very fine-grained writes to storage media. Also, since these             F LY T RAP runs the workload on the target file system, and
systems perform operations synchronously, they provide                   logs a sequence of PM writes, flushes, and fences. For the
strong guarantees about crash consistency at all times, not              sake of simplicity, assume that all writes are flushed and there
just after fsync(). As a result, a workload can result in sig-           is a store fence at the end of the system call. 2) F LY T RAP
nificantly more crash states that are interesting to test in a PM        creates a crash state where only the old file is deleted; the
file system than in a block-based file system. We handle the             other writes are lost in the crash. 3) The consistency checker
large number of crash states by exploiting three observations:           finds that both the old file and the new file are missing 4)
   • Data required for crash consistency must be flushed.                F LY T RAP creates a bug report. This bug in NOVA discovered
     While the PM file system may write a lot of data, only              by F LY T RAP (bug 4).
     data that is explicitly flushed or is written via non-
     temporal stores can be relied upon to be persistent. Crash-
                                                                               writes. In our testing, we observed that the number of
     Monkey [38] and Hydra [27] leverage a similar observa-
                                                                               in-flight writes at any given point of time is small: across
     tion to only simulate crashes after fsync() and sync().
                                                                               the two workload generators (Section 3.4) and four file
     F LY T RAP exploits this observation to only track writes
                                                                               systems, the average number of the in-flight writes is
     when they are flushed — it collects write information
                                                                               three, and the maximum is ten. The only exception was
     only for cache flushes and non-temporal writes. This
                                                                               the write() system call in PMFS, which we observe
     drastically reduces the overhead of logging and the num-
                                                                               to have up to 20 in-flight writes when writing a large
     ber of functions F LY T RAP must track.
                                                                               amount of data. This allows F LY T RAP to exhaustively
   • Order of in-flight writes does not matter. If there are two               enumerate and check all subsets of in-flight writes.
     in-flight writes A and B (data in volatile CPU caches
                                                                           Taken together, these observations allow F LY T RAP to track
     that has not been flushed yet), the order in which A and
                                                                         only flushed writes (leading to low overhead), consider only
     B are persisted does not matter. A crash state where A
                                                                         subsets (and not permutations), and exhaustively test all the
     is written first followed by B is equivalent to a crash
                                                                         subsets resulting from in-flight writes.
     state where B is followed by A. If A and B are writes to
     the same cache line, x86 enforces sequential ordering.
     As a result, we do not have to consider re-orderings                3.3     F LY T RAP Architecture
     of in-flight writes. F LY T RAP creates crash states using
     different subsets of in-flight writes, taking into account          F LY T RAP is built on top of the CrashMonkey framework [38],
     writes to the same cache line.                                      which consists of two kernel modules and user-space utilities
                                                                         to facilitate checking crash states. We adapt CrashMonkey’s
   • Small number of in-flight writes. The number of gen-                user-space utilities to target PM file systems; the two kernel
     erated crash states depends on the number of in-flight              modules are specific to block devices and are not compatible


                                                                     5
with PM. We replace them with modules based on Kprobes,                   properties implied by POSIX or widely expected by users
a Linux kernel debugging utility, to record writes to PM.                 in practice [11, 40]. Finally, to ensure the file system is in a
   Given a workload and a target file system, F LY T RAP pro-             usable state, F LY T RAP creates files in all directories and then
ceeds in three steps (Figure 2): (1) run the workload and                 deletes all files. If any of these checks fail, the checker reports
log the writes made by the file system; (2) construct crash               a bug describing the inconsistency and the corresponding
states; (3) check each crash state and generate a bug report if           crash state.
required. We now describe each step in more detail.                          To make this implementation efficient, we construct oracle
                                                                          file systems incrementally as the log is replayed because many
Logging writes. Recall from Section 3.2 that F LY T RAP re-
                                                                          crash states share the same oracle state. We also construct
quires PM file system developers to identify the centralized
                                                                          crash states in-place on the PM device, mutating them to
persistence functions. Given the locations of these functions,
                                                                          generate each crash state rather than recreating them from
F LY T RAP uses Kprobes [4] to automatically instrument them
                                                                          scratch each time. Because the consistency checks mutate
at run time. Each time one of these functions is invoked by the
                                                                          the state, we reuse our logging infrastructure to record an
file system, the instrumentation logs the operation and its argu-
                                                                          undo log for these mutations and roll back the changes when
ments (including the current value of the cache line for cache
                                                                          advancing to the next crash state.
line flushes). The user-space test harness also inserts markers
into this log to record the start and end of each system call.
This approach requires no code changes to the file-system im-             3.4     Workload Generation
plementation other than to prevent the compiler from inlining
the persistence functions. In our experience, identifying these           Given a workload, F LY T RAP generates crash states and tests
functions was simple, and we expect it to be even simpler for             them for consistency. An orthogonal challenge is generating
file-system developers who likely already know where the                  workloads for F LY T RAP to test. The CrashMonkey work [38]
persistence functions are in their implementation.                        introduced the hypothesis that small workloads on new file
                                                                          systems are useful in finding crash-consistency bugs. While
Constructing crash states. Given a workload, F LY T RAP can               this hypothesis was true on traditional block-based file sys-
simulate crashes both after and during system calls. F LY-                tems, we aim to test whether it holds on PM file systems. To
T RAP replays a workload by walking through the log of                    this end, we modify CrashMonkey’s Automated Crash Ex-
writes. Whenever it encounters a cache line write back or                 plorer (ACE), which systematically explores workloads of a
non-temporal store, it adds it to an in-flight vector. When it            given size, to work with F LY T RAP. To disprove the hypothe-
encounters a store fence, it flushes the contents of the in-flight        sis, we modify the Syzkaller [7] gray-box fuzzer to work with
vector. To generate crash states after system calls, F LY T RAP           F LY T RAP. Syzkaller generates long, complex, randomized
replays all writes that have been flushed by the end of the               workloads while aiming to improve code coverage.
system call. To generate crash states during system calls, it
simulates a crash immediately before each store fence and
creates a set of crash states by replaying each subset of the             3.4.1   Automatic Crash Explorer
in-flight vector. The number of crash states is thus dependent            We used a modified version of ACE [38] to systematically
on the number of in-flight writes; if there are n in-flight writes,       generate workloads for F LY T RAP. ACE was designed to ex-
there will be 2n − 1 crash states. As noted in Section 3.2, we            haustively generate workloads of a certain structure to test
have observed that n is small in practice, allowing F LY T RAP            traditional file systems. It focuses on short workloads with
to apply this exhaustive testing strategy. Since a small num-             frequent fsync(), fdatasync(), or sync() calls, as these
ber of in-flight writes is not a guarantee and we occasionally            are required to obtain strong crash-consistency guarantees
see larger sets while using Syzkaller, F LY T RAP can place a             in traditional file systems. Given a sequence length n, ACE
configurable cap on the number of writes to replay. We find               generates workloads with n core file-system operations over
that in practice, even a cap of two writes is sufficient to reveal        a small, predetermined set of files, then fleshes them out by
many bugs (§5.1).                                                         satisfying dependencies and adding fsync(), fdatasync(),
Testing each crash state. To check file-system consistency,               or sync() operations. A workload with n core system calls is
F LY T RAP first mounts the target file system on each crash              called a “seq-n" workload.
state, which is itself a useful consistency check as failure to              We modify ACE in the following manner for F LY T RAP.
mount is a serious bug. Once successfully mounted, the file-              First, since system calls in the fsync family do not have the
system state is compared against two oracle file-system states:           same crash-consistency significance in PM file systems as
a before state representing the file-system state before the              they do in traditional file systems, we remove them from
crashing system call began and an after state representing the            our version of ACE. This significantly reduces the number
file-system state if the system call during the crash success-            of workloads generated because we do not need to consider
fully completed. After recovery, the file-system state should             workloads that differ only by the sync calls they use. We also
match either the before or after state. This check validates              remove system calls and options that are not supported by the


                                                                      6
file systems under test. For example, NOVA only supports                below a predefined threshold, we add the report to C, other-
the FALLOC_FL_KEEP_SIZE flag for the falloc system call,                wise we create a new cluster. This simple heuristic was more
and it does not support extended attributes. Removing these             effective than more complex ones we tested. We also updated
unsupported options further reduces the number of workloads             Syzkaller to display these bug report clusters (along with the
that ACE generates.                                                     workload that triggered each bug report) in its UI dashboard
   We test all seq-1 and seq-2 workloads, as well as the sub-           to make them easier for users to debug.
set of seq-3 workloads containing only pwrite(), link(),
unlink(), and rename() calls (i.e. the “seq-3 metadata”                 3.5    Limitations
workloads in the CrashMonkey work [38]) to make testing
tractable. Our modified version of ACE generates 56 seq-1               F LY T RAP has several limitations. First, it can miss bugs be-
tests, 3136 seq-2 tests, and 50650 seq-3 metadata tests.                cause it does not explore all workloads nor all crash states
                                                                        resulting from a given workload. F LY T RAP only tests some
                                                                        subsets of the data in write() system calls and considers
3.4.2   Syzkaller
                                                                        cache line flushes atomic with respect to crashes. F LY T RAP
We modify Syzkaller [7], a state-of-the-art gray-box kernel             only tracks flushed writes; a PM write that is never flushed
fuzzer, to generate workloads for F LY T RAP. As is standard in         is invisible to F LY T RAP, and it could result in F LY T RAP
gray-box fuzzing, our fuzzer starts with an initial set of test         missing a bug. For example, consider file-system writes to A,
cases (seeds) and uses genetic programming to generate new              B, C, and a bug where the file system never flushed A. F LY-
tests for F LY T RAP from those seeds. F LY T RAP tests each            T RAP would not explore a crash state where A and B are
generated workload and reports back whether the workload                persisted, but C is not, and so if this state created inconsis-
produced a crash-consistency bug along with the code cov-               tency F LY T RAP would not detect it. Second, F LY T RAP does
erage achieved on the target kernel. If the workload covered            not support checking concurrent workloads. It assumes that
new parts of the kernel, the fuzzer adds it to its set of seeds         the operations performed by the file system in each workload
and generates new workloads from it.                                    are deterministic. In our testing so far, we have not observed
   Syzkaller generates workloads by randomly selecting se-              any non-determinism in the file systems that impacted our
quences of core file-system operations and their argument               ability to find and reproduce bugs with F LY T RAP. Third,
values. It generates syntactically and semantically valid work-         F LY T RAP assumes that the PM file system has centralized
loads by using a detailed template for each system call that            persistence functions. A PM file system that uses in-line as-
specifies more precise qualified type information [13] for the          sembly to update PM at various locations in its code would
call’s arguments. For example, the template for open specifies          not be compatible with F LY T RAP.
that it returns a file descriptor, not just an arbitrary integer;          Despite these limitations, we believe that F LY T RAP is a
the template for write specifies that its first argument is also        useful addition to the set of tools for building robust PM file
a file descriptor rather than an arbitrary integer (which would         systems. In particular, the level of automation provided by
be very unlikely to be a valid file descriptor).                        F LY T RAP allows developers to test new or in-development
   To adapt Syzkaller to our setting, we restrict it to only            PM file systems efficiently.
generate workloads that contain core file-system operations,
and replace its workload executor with a custom one. Our                4     Testing PM File Systems
executor invokes F LY T RAP on each workload and records
code coverage both before the crash and during recovery. We             In this section, we evaluate F LY T RAP’s effectiveness at find-
add a workload to the seed set if it achieves new code coverage         ing bugs across different PM file systems. We describe our
on either side of the crash.                                            experimental setup (§4.1) and present an evaluation of F LY-
   Like many fuzzers, Syzkaller can quickly generate many               T RAP along with a comparison of ACE and Syzkaller as
bug reports that are duplicates—we found that Syzkaller                 workload generation strategies (§4.2). We provide a brief
would frequently generate different workloads that triggered            overview of the bugs found by F LY T RAP (§4.3).
the same bug and produced similar bug reports. In our setting,
this duplication also arises when multiple crash states for the
                                                                        4.1    Experimental setup
same workload trigger the same bug, producing similar bug
reports. To address this problem, we extended Syzkaller to au-          File systems. We considered seven open-source PM file
tomatically triage bug reports generated by F LY T RAP during           systems for testing with F LY T RAP: NOVA [45], NOVA-
fuzzing. We use a simple triaging procedure that clusters bug           Fortis [46], PMFS [18], WineFS [24], Strata [28], Assise [8],
reports by lexical similarity. Whenever F LY T RAP generates a          and ext4-DAX [1]. ext4-DAX is a modification of the ext4 file
bug report, we compute the report’s word vector v (based on             system for PM. It shares most of its code with ext4 and has the
its text), and then compute the distance from v to the closest          same crash consistency guarantees, so tools like CrashMon-
cluster C of previous reports. If the distance from v to C is           key or Hydra that are designed for block-based file systems


                                                                    7
are a better fit for testing ext4-DAX. Strata and Assise are               1,000,000
kernel-bypass file systems implemented in user space. Neither                                       Syzkaller
Strata nor Assise currently support recovering from arbitrary                          100,000        ACE
crashes. As a result, we chose to focus on the remaining four
systems: NOVA, NOVA-Fortis, PMFS, and WineFS.                                           10,000




                                                                      Time Taken (s)
Test infrastructure. All experiments described in this pa-                               1,000
per were run on QEMU/KVM virtual machines running De-
bian Stretch. Each VM is allocated one CPU (except for those
                                                                                          100
testing WineFS, which requires four CPUs) and 8 GB of RAM.
Each VM also has two 128 MB emulated PM devices, which
are used to execute the workload, construct the oracle file                                10
system, and check crash states.
   We run ACE-generated workloads on a single Amazon EC2                                    1
                                                                                                 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
m5d.metal instance with 96 vCPUs, 384 GB memory, and
four 900 GB NVMe SSDs. We use these resources to check                                                          # of bugs found
multiple file systems using workloads of multiple sequence
lengths in parallel. We run seq-1 and seq-2 tests on individual       Figure 3: Cumulative time taken to find crash-consistency
VMs; we split the seq-3 metadata workloads across 10 VMs              bugs by ACE and Syzkaller.
and ran them in parallel. All file systems were checked using
seq-1 and seq-2 workloads, and all but WineFS were run on
seq-3 metadata tests. At the time we ran these experiments,           Comparison. We ran Syzkaller and ACE on each file system
WineFS had a bug that prevented creation of the number of             and recorded the cumulative CPU time taken to find all bugs
files some seq-3 tests require. The number of in-flight writes        when using each workload generator. Figure 3 shows the
at any time during ACE tests is consistently low, so we do not        result of this experiment. ACE finds the first 15 out of 18
place a cap on the number of crash states for ACE.                    bugs in less than three CPU hours total, but is unable to
   To evaluate F LY T RAP with Syzkaller, we run four                 find the final three bugs. Syzkaller, on the other hand, takes
Chameleon Cloud [26] bare metal instances, which have two             almost 20× more CPU time than ACE to find the first 10
Intel Xeon Gold 6240R CPUs each with 24 cores and 48                  bugs and almost 6× more CPU time to find all the bugs the
threads, as well as 192 GB RAM, and 480 GB storage. Each              ACE tester finds. However, when we let Syzkaller run for an
host fuzzed a different file system using 15 virtual machines.        additional 27 CPU hours, it is able to find three additional
Each fuzzer starts with an empty set of seeds. Syzkaller-             bugs that are not detected by ACE. ACE misses these three
generated tests can be long and generate many crash states,           bugs because they do not conform to the patterns that it uses
so to avoid the fuzzer getting stuck, we run F LY T RAP with a        to generate workloads. For example, two of these bugs create
cap of two writes per crash state; as §5.1.2 observes, this cap       two open file descriptors to the same file and modify the
does not affect its ability to find bugs in practice.                 file’s contents through both file descriptors, but ACE does not
                                                                      generate workloads with multiple file descriptors for the same
                                                                      file.
4.2    Evaluation                                                        While the results of this experiment indicate that Syzkaller
                                                                      has greater overall bug finding capability than ACE, the
ACE tests. For each file system under test, F LY T RAP took
                                                                      ACE tests are considerably more resource efficient. This sug-
about 10–15 minutes to run the seq-1 workloads, 7–11 hours
                                                                      gests that the ACE tests can be run locally and iteratively to
to run the seq-2 workloads, 16–26 hours to run the seq-3
                                                                      find bugs during file-system development, whereas Syzkaller
metadata workloads in parallel (160–260 total CPU hours).
                                                                      should be run for a long time in an environment with ample
The number of crash states to check on each workload varies
                                                                      compute resources (such as the cloud) for more comprehen-
as much as 3× between file systems, with PMFS generally
                                                                      sive crash-consistency testing.
checking the most and WineFS checking the fewest. Overall,
F LY T RAP found 15 bugs using ACE tests across all four file
systems.                                                              4.3                 Results
Syzkaller. We ran F LY T RAP with Syzkaller for 18 hours on
15 VMs, for a total of 270 CPU hours spent fuzzing. During            Crash-consistency bugs. Using ACE- and Syzkaller-
this time, F LY T RAP checked over 40 million crash states            generated tests, F LY T RAP finds 18 unique crash-consistency
across all four system calls, finding 18 unique bugs. Three of        bugs across all four tested file systems. The number of unique
these bugs cannot be found with ACE-generated workloads.              bugs is based on the number of separate fixes required to patch


                                                                  8
                 System call         # of bugs                          5     Bug Analysis
                 mkdir                   1                              This sections presents an analysis of the 18 crash-consistency
                 creat                   1                              bugs found by F LY T RAP (Table 2). To the best of our knowl-
                 rmdir                   1                              edge, this is the first such corpus of crash-consistency bugs in
                 fallocate               1                              PM file systems. We make some observations about common
                 unlink                  2                              patterns we found among the bugs (§5.1), and distill lessons
                 link                    3                              for building and testing PM file systems (§5.2).
                 rename                  4
                 truncate                5
                 write/pwrite            5
                                                                        5.1     Observations
                                                                        We first present observations about the nature of the crash-
Table 1: The number of bugs associated with each system call.           consistency bugs found by F LY T RAP, and then present obser-
Some bugs impact all file system operations, and some impact            vations about crash-consistency testing.
multiple system calls.
                                                                        5.1.1   Nature of crash-consistency bugs

                                                                        Observation 1: A majority of the observed crash-
all of the bugs, not different user-visible consequences. Two           consistency bugs are logic issues rather than PM pro-
bugs are found in both WineFS and PMFS (since WineFS is                 gramming errors. When we began working on F LY T RAP,
built off PMFS), for a total of 20 bugs.                                we expected that most bugs would be due to the subtleties
                                                                        of the persistent-memory programming model that existing
   Table 2 describes the consequences of each bug and the               PM application research has focused on: interaction with the
system calls they affect. The bugs are classified as either logic       cache hierarchy, CPU store (re)ordering, etc. However, the
or PM errors (described further in §5.1). F LY T RAP found              majority of bugs we found—14 of 18—are actually due to
eight bugs in NOVA, four bugs in NOVA-Fortis, two bugs                  logic bugs in manipulating file-system data structures rather
in PMFS, two bugs in WineFS, and two bugs in both PMFS                  than mistakes in managing persistent memory. The “type”
and WineFS (as WineFS is an extension of PMFS). Many of                 column in Table 2 classifies bugs into logic bugs or PM bugs.
these bugs have serious consequences that violate the crash             Logic bugs are issues that cannot be fixed by adding cache
consistency guarantees of the file systems. Three of the bugs           line flushes or store fences. These results suggest that it is
prevent the file system from being mounted entirely. Two                not sufficient for a file-system crash-consistency testing tool
impact the atomicity of rename(), which many applications               to focus on exploring the persistence behavior of individual
rely on [40]. Many others cause data loss or prevent a user             writes and reorderings; it must also exercise the file-system
from accessing files entirely.                                          data structures and recovery mechanisms, and check higher-
                                                                        level consistency properties that cannot be validated at the
   The bugs impact a wide variety of system calls, as Table 1           level of individual writes.
shows. Many bugs are located in common metadata-handling                Observation 2: In-place update optimizations are a com-
or recovery code and thus impact multiple system calls.                 mon source of crash consistency bugs. One of the allures
rename(), write()/pwrite(), link(), and truncate()                      of persistent memory is that programs can access it as mem-
are especially bug-prone and are affected by multiple bugs.             ory, performing fine-grained reads and writes directly rather
                                                                        than coalescing them into larger block-sized IO operations
Non-crash consistency bugs. While working with F LY-                    on slower storage media. This design makes it possible in
T RAP, we also found an additional eight non-crash-                     principle to reduce the overheads of traditional consistency
consistency bugs not included in Table 2. These bugs occur              mechanisms like journaling by manipulating on-disk data
during regular execution and do not require a crash to be ex-           structures directly. All four file systems we tested use a jour-
posed. We were able to find these bugs because they caused              nal for consistency, but all have performance optimizations
KASAN errors, segmentation faults, or incorrect behavior that           to bypass the journal and perform in-place updates in certain
our consistency checks could detect. For example, using the             circumstances. For example, NOVA updates the link count of
fuzzer, we discovered that NOVA does not properly handle                a file by updating a per-inode log. Appending to this log is
write() calls where the number of bytes to write is extremely           done via a journalled transaction, but if the previous operation
large; it will allocate all remaining space for the file, causing       on the file also updated its link count, NOVA may modify that
most subsequent operations to fail. F LY T RAP detected this            log entry in place instead.
bug because it found that new files could not be created in                We found these optimizations to be particularly error-prone:
crash states following this write.                                      6 of 18 bugs in Table 2 are caused by in-place updates. For


                                                                    9
    Bug #       File System         Consequence                                         Affected system calls                Type
    1           NOVA                File system unmountable                             All                                  Logic
    2           NOVA                File is unreadable and undeletable                  mkdir, creat                         PM
    3           NOVA                File system unmountable                             write, pwrite, link,                 Logic
                                                                                        unlink, rename
    4           NOVA                Rename atomicity broken (file disappears)           rename                               Logic
    5           NOVA                Rename atomicity broken (old file still             rename                               Logic
                                    present)
    6           NOVA                Link count incremented before new file ap-          link                                 Logic
                                    pears
    7           NOVA                File data lost                                      truncate                             Logic
    8           NOVA                File data lost                                      fallocate                            Logic
    9           NOVA-Fortis         Unreadable directory or file data loss              unlink, rmdir, truncate              PM
    10          NOVA-Fortis         File is undeletable                                 write, pwrite, link,                 Logic
                                                                                        rename
    11          NOVA-Fortis         FS attempts to deallocate free blocks               truncate                             Logic
    12          NOVA-Fortis         File is unreadable                                  truncate                             Logic
    13          PMFS                File system unmountable                             truncate                             Logic
    14 &15      PMFS&WineFS         Write is not synchronous                            write, pwrite                        PM
    16          PMFS                Out-of-bounds memory access                         All                                  Logic
    17 &18      PMFS&WineFS         File data lost                                      write, pwrite                        PM
    19          WineFS              File is unreadable and undeletable                  All                                  Logic
    20          WineFS              Data write is not atomic in strict mode             write, pwrite                        Logic

                  Table 2: Bugs found by F LY T RAP, their consequences, and the system calls that they affect.


example, in bug 4, NOVA’s rename implementation removes                 free page lists or file sizes) and instead rebuild it in volatile
the directory entry from the parent inode in-place but journals         memory at mount time. This rebuilding code is subtle because
the other metadata changes, allowing the file to be lost in a           it must account for potential inconsistencies or partial states
crash before the journal transaction commits.                           after a crash, and we found that 8 of the 18 bugs in Table 2
   Fixing these bugs often requires journalling more data,              were in such code. For example, bug 13 is caused by a crash
which is not free. To quantify the impact of fixing such bugs,          during a truncate system call on PMFS. The implementa-
we compared the performance of NOVA before and after fix-               tion first stores information about the operation in a “truncate
ing two rename atomicity bugs (4 and 5) by journalling more             list”; if the system crashes before the truncation is complete,
metadata. We tested both versions on Intel Optane DC Per-               the truncate list can be replayed to finish the operation. How-
sistent Memory media. In a microbenchmark that repeatedly               ever, replaying truncations requires accessing the free page
creates and renames a file over the top of an existing file, the        list, which PMFS rebuilds in volatile memory during recovery,
fixed version of NOVA is 25% slower. A more real-world                  but only after replaying the truncate list. Attempts to replay
metadata-intensive benchmark (checking out different stable             truncations therefore cause a null pointer dereference when
versions in the Linux kernel git repository) shows negligi-             accessing the free page list.
ble overhead (<1%). In some cases, journalling can even be                 Rebuilding volatile state is more complex in PM file sys-
better than in-place updates. The fix for bug 6 replaces an             tems that maintain per-CPU volatile state to improve scalabil-
in-place update in link with extra logging, but makes a mi-             ity. In bug 19, WineFS failed to properly index into an array
crobenchmark that repeatedly creates links to a file 7% faster,         of per-CPU journals that were read during crash recovery.
likely because checking whether the in-place update is safe             F LY T RAP can even find bugs in rebuilding code in the ab-
requires an extra read from the media.                                  sence of crashes, because the crash states it tests include ones
                                                                        where all writes are durable. For example, bug 7 involves
Observation 3: Rebuilding volatile state during crash re-               modifying the same file through multiple file descriptors on
covery is error-prone. In a traditional file system, crash re-          NOVA, which creates log entries out of chronological order,
covery scans on-disk structures like journals and updates the           violating assumptions in the rebuilding code and causing data
durable state to match. PM file systems often perform more              loss during truncate operations.
work during recovery. As a performance and write-endurance
optimization, they avoid durably storing some metadata (e.g.,           Observation 4: Resilience mechanisms to recover from


                                                                   10
 Observation                                                                                              Associated bugs
 Many bugs occur due to logic or design issues, not PM programming errors.                                1, 3–8, 10–13, 16, 19, 20
 The complexity of performing in-place updates leads to bugs.                                             4–7, 14, 15
 Recovery code that deals with rebuilding in-DRAM state is a significant source of bugs.                  1, 3, 7, 11, 13, 16, 19
 Complex new features for increasing resilience can introduce new crash consistency bugs.                 2, 9–12
 A majority of observed bugs can only be exposed by simulating crashes during system calls.               3–6, 9–13, 19, 20
 Short workloads were sufficient to expose many crash consistency bugs.                                   1–6, 9–20
 Many bugs were exposed by replaying a few small writes onto previously persistent state.                 3–6, 9–13, 19, 20

                                     Table 3: Observations and the bugs associated with them.


media failures can introduce new crash-consistency bugs.                  system call leaves only some writes persisted. Waiting until
NOVA-Fortis [46] is an extension of NOVA that adds fault                  a persistence point to check consistency would not discover
detection and tolerance for media errors and software bugs                these bugs, as NOVA correctly flushes all writes by the end
by (among other techniques) replicating and checksumming                  of the rename operation.
inodes and logs and checksumming file data. While NOVA-
Fortis is not explicitly designed to increase crash resilience,           Observation 6: Short workloads suffice to expose many
we tested these features to see if it is more tolerant of crashes         crash-consistency bugs. We use ACE [38] to systematically
than the original NOVA.                                                   generate test workloads. ACE’s design focuses on exhaus-
   We found that NOVA-Fortis has all the same crash-                      tively enumerating small workloads, based on an empirical
consistency bugs we found in the original version of NOVA,                study of historical crash-consistency bugs in block-based file
and in addition has five new bugs caused by the added com-                systems that showed most could be reproduced with at most
plexity of maintaining redundant state and checksums. A                   three operations. It was unclear whether this would hold for
common theme in these bugs is that data and metadata mod-                 PM file systems. However, 15 of the 18 bugs we found in PM
ifications are often not atomic with checksum and replica                 file systems can be found using ACE with at most three oper-
updates, allowing checksum validation to fail (and render a               ations, suggesting that this same small-scope hypothesis [23]
file inaccessible) even if the file system is consistent and data         holds for PM file systems. To try to invalidate this hypothesis,
intact.                                                                   we also run F LY T RAP using the Syzkaller gray-box fuzzer,
                                                                          which can generate much longer workloads but without the
                                                                          exhaustiveness guarantees of ACE (§3.4). Syzkaller found 3
5.1.2   Crash-consistency testing in PM file systems                      bugs that ACE did not. However, all three bugs were found on
                                                                          short workloads: two would be considered seq-2 and one seq-
Observation 5: A majority of observed bugs require                        3 in terms of the number of core system calls required. ACE
simulating crashes during system calls. Current crash-                    missed them not because of size but because of complexities
consistency testing tools for traditional file systems, like              that ACE omits to make exhaustive enumeration tractable,
CrashMonkey [38] and Hydra [27], insert crashes only at                   such as testing unaligned writes.
the end of persistence system calls (fsync, fdatasync, etc.).
This heuristic exploits the fact that most POSIX APIs only                Observation 7: Most of the observed buggy crash states
make crash-consistency guarantees after persistence opera-                involve few writes. F LY T RAP generates crash states by snap-
tions, so intermediate states are unlikely to violate the specifi-        shotting known-persistent disk states between store fences,
cation. It allows these tools to scale to test larger workloads,          and then replaying all subsets of the in-flight writes between
and does not appear to cause them to miss bugs: CrashMon-                 each store fence (§3). For a system call with n in-flight writes
key has a mode to insert crashes during system calls, but it              before a fence, this means F LY T RAP should consider all 2n −1
did not find any additional bugs in the file systems tested in            possible crash states. However, we found that most bugs found
that work.                                                                by F LY T RAP involve crash states that include small subsets
   We found that this same heuristic does not work for PM file            of the in-flight writes. Of the 11 bugs in Table 2 that involve
systems. 11 of the 18 bugs in Table 2 require a crash to occur            a crash in the middle of a system call, 10 can be exposed
during a system call. This is a corollary of our observation              by a crash state that replays only a single write onto the last
that most PM file systems intend to implement most system                 known-persistent state; the final bug requires two writes. This
calls synchronously, and so their effects are fully persistent by         observation suggests a profitable heuristic for rapid crash-
the end of the system call. For example, the rename atomicity             consistency testing would be to only test small subsets of
bugs in NOVA (bugs 4 and 5) arise when a crash during the                 in-flight rights rather than all of them. F LY T RAP exploits


                                                                     11
this observation by enumerating crash states in increasing              expected to bring those patterns across to PM file systems,
order of subset size, allowing it to find most crash-consistency        focusing on short workloads and a small set of potential crash
bugs quickly. In our experiments, we often cap the number               points and patterns. However, we found instead that most as-
of writes that are replayed to build each crash state, primarily        sumptions about file-system crash consistency do not carry
to prevent Syzkaller from spending many hours checking a                across to persistent memory, where the consistency mech-
single outlier test that has a high in-flight write count. The          anisms and guarantees are significantly different. Finding
highest in-flight write count we observed, 20 writes in some            crash consistency bugs in PM file systems requires explor-
PMFS write() calls, would take about 30 hours to check                  ing many more crash states than other file systems, including
exhaustively using F LY T RAP. A cap of two is enough to find           crashes in the middle of system calls; we had to develop new
all bugs presented in this paper; a cap of five is sufficient to        techniques to make this search tractable. Existing file-system
check all crash states for most system calls in the PM file             crash-consistency testing tools would not have found these
systems we tested.                                                      bugs. We also found that fuzzing was an effective way to
                                                                        invalidate assumptions we had brought along from prior file
                                                                        systems experience, such as the significance of unaligned
5.2    Lessons Learned                                                  writes and exercising per-CPU code paths.
Based on our observations above, we have distilled three
lessons for developers of PM file systems and for building the             Another assumption we carried into this work was that
testing tools that support them.                                        the difficulty of building a PM file system lies in correctly
                                                                        applying the PM programming model. We intended to focus
Lesson 1: Synchronous crash consistency on PM file sys-                 on exhaustively testing the precise persistency behavior of
tems simplifies the user experience, but complicates im-                PM file system code. However, we found instead that most
plementation and testing. Crash-consistency guarantees in               PM file system bugs were logic errors in optimizations that
modern file systems are something of a vicious cycle. File-             could also have occurred in block-based file systems (though
system developers argue that relaxed guarantees are required            likely would not improve performance in that context). Exist-
to extract reasonable performance [30], but these weak guar-            ing tools that focus on detecting specific PM programming
antees are a pain point for application developers and have             error patterns [5, 16, 19, 21, 31–33, 39] would miss many of
caused severe data loss in popular applications [9, 15, 40], so         these bugs, but we were able to detect them even with small
file-system developers implement workarounds to “fix” com-              workloads and with very few in-flight writes applied. Writing
mon mistaken application patterns and make the intended                 general-purpose consistency checks and applying gray-box
guarantees even less clear. The fine write granularity and low          fuzzing to generate workloads helped to invalidate these as-
latency of persistent memory finally offers a path to strengthen        sumptions and gave new insights into common bug patterns
file-system crash-consistency models, making resilient appli-           in PM file systems.
cations easier to build and validate. PM file system developers
have taken advantage of this opportunity by making all system
                                                                        Lesson 3: Lightweight testing offers a scalable approach
calls synchronous and durable.
                                                                        to detecting many crash-consistency bugs. F LY T RAP is,
   While this end result is exciting, implementing it correctly
                                                                        in principle, a bounded exhaustive testing [38] (i.e., bounded
carries new risks for PM file-system developers compared
                                                                        verification) tool for PM file systems: given enough time,
to traditional file systems. We found that many PM file-
                                                                        it can check every possible crash behavior of every possi-
system bugs come from complex optimizations to realize high-
                                                                        ble workload up to some bounds on its size and inputs. Of
performance synchronous crash-consistency—combining in-
                                                                        course, it is not tractable to exhaust this search space even
place updates with other consistency mechanisms, and replac-
                                                                        with very small bounds. However, we found that F LY T RAP is
ing persistent state with reconstructible volatile state—that
                                                                        an effective lightweight testing tool, in that it can quickly and
are uncommon techniques on slower storage media. This is
                                                                        automatically find many bugs by checking small workloads
a rich new design space for storage systems, and identifying
                                                                        and few crash states, and then run for longer to find more
the right primitives for this optimizations will be good future
                                                                        corner-case issues. F LY T RAP runs the ACE seq-1 workloads
work. These optimizations also create complexity for testing
                                                                        on a file system in under 15 minutes and, when considering
and validation of PM file systems, which we found requires
                                                                        only crash states with one persisted write, can detect 12 of
driving the file system into exercising deeper data structure
                                                                        the 18 bugs we discovered. On the other hand, the fuzzer
manipulations and recovery mechanisms than existing crash-
                                                                        frontend to F LY T RAP takes 1–2 orders of magnitude longer
consistency tools are capable of.
                                                                        to run (i.e., runs overnight) but finds three more bugs than
Lesson 2: Diverse testing mechanisms and checkers help                  ACE. These two frontends are complementary. They enable a
invalidate assumptions about crash-consistency patterns.                lightweight approach that helps developers iterate quickly on
Most crash-consistency testing tools build on heuristics and            new code, while still offering stronger confidence as the code
patterns in historic bugs to select the workloads they test. We         gets “closer to production” [10].


                                                                   12
6   Conclusion                                                         References
This paper presents F LY T RAP, a new record-and-replay frame-          [1] Direct Access for files. https://www.kernel.org/
work for testing the crash consistency of PM file systems.                  doc/Documentation/filesystems/dax.txt.
We use F LY T RAP with the ACE workload generator and the
Syzkaller gray-box fuzzer and find 18 unique bugs across                [2] Intel Optane DC Persistent Memory Quick Start
four PM file systems. To the best of our knowledge, this is the             Guide.     https://www.intel.com/content/dam/
largest corpus of crash-consistency bugs on PM file systems.                support/us/en/documents/memory-and-storage/
Our study of these bugs provides insights into how crash-                   data-center-persistent-mem/Intel-Optane-
consistency bugs arise in PM file systems and what types of                 DC-Persistent-Memory-Quick-Start-Guide.pdf.
tools are needed to test these systems.
                                                                        [3] Intel Optane Persistent Memory.      https:
                                                                            //www.intel.com/content/www/us/en/
                                                                            architecture-and-technology/optane-dc-
                                                                            persistent-memory.html.

                                                                        [4] Kernel Probes (Kprobes). https://www.kernel.org/
                                                                            doc/Documentation/kprobes.txt.

                                                                        [5] Discover Persistent Memory Programming Errors with
                                                                            Pmemcheck.        https://www.intel.com/content/
                                                                            www/us/en/developer/articles/technical/
                                                                            discover-persistent-memory-programming-
                                                                            errors-with-pmemcheck.html, 2018.

                                                                        [6] The Open Group Base Specifications Issue 7. https:
                                                                            //pubs.opengroup.org/onlinepubs/9699919799/,
                                                                            2018.

                                                                        [7] Syzkaller.            https://github.com/google/
                                                                            syzkaller/, 2021.

                                                                        [8] Thomas E. Anderson, Marco Canini, Jongyul Kim, De-
                                                                            jan Kostić, Youngjin Kwon, Simon Peter, Waleed Reda,
                                                                            Henry N. Schuh, and Emmett Witchel. Assise: Per-
                                                                            formance and availability via client-local NVM in a
                                                                            distributed file system. In 14th USENIX Symposium on
                                                                            Operating Systems Design and Implementation (OSDI
                                                                            20), pages 1011–1027. USENIX Association, November
                                                                            2020.

                                                                        [9] Nicolas Boichat. Issue 502898: ext4: Filesystem corrup-
                                                                            tion on panic, June 2015. https://code.google.com/
                                                                            p/chromium/issues/detail?id=502898.

                                                                       [10] James Bornholt, Rajeev Joshi, Vytautas Astrauskas,
                                                                            Brendan Cully, Bernhard Kragl, Seth Markle, Kyle Sauri,
                                                                            Drew Schleit, Grant Slatton, Serdar Tasiran, Jacob Van
                                                                            Geffen, and Andrew Warfield. Using lightweight formal
                                                                            methods to validate a key-value storage node in Amazon
                                                                            S3. In ACM SIGOPS 28th Symposium on Operating Sys-
                                                                            tems Principles (SOSP), pages 836–850, October 2021.

                                                                       [11] James Bornholt, Antoine Kaufmann, Jialin Li, Arvind
                                                                            Krishnamurthy, Emina Torlak, and Xi Wang. Specifying
                                                                            and checking file system crash-consistency models. In


                                                                  13
     Proceedings of the Twenty-First International Confer-           [20] Gregory R. Ganger and Yale N. Patt. Metadata up-
     ence on Architectural Support for Programming Lan-                   date performance in file systems. In Proceedings of
     guages and Operating Systems, ASPLOS, pages 83–98,                   the 1st Symposium on Operating Systems Design and
     Atlanta, GA, USA, April 2016.                                        Implementation (OSDI ’94), pages 49–60, Monterey,
                                                                          California, November 1994.
[12] Vijay Chidambaram. Orderless and Eventually Durable
     File Systems. PhD thesis, University of Wisconsin, Madi-        [21] Hamed Gorjiara, Guoqing Harry Xu, and Brian Demsky.
     son, Aug 2015.                                                       Jaaru: Efficiently model checking persistent memory
                                                                          programs. In Proceedings of the 26th ACM International
[13] Brian Chin, Shane Markstrum, and Todd Millstein. Se-                 Conference on Architectural Support for Programming
     mantic type qualifiers. In Proceedings of the 2005 ACM               Languages and Operating Systems, ASPLOS 2021, page
     SIGPLAN Conference on Programming Language De-                       415–428, New York, NY, USA, 2021. Association for
     sign and Implementation, PLDI ’05, page 85–95, New                   Computing Machinery.
     York, NY, USA, 2005. Association for Computing Ma-
     chinery.                                                        [22] Joseph Izraelevitz, Jian Yang, Lu Zhang, Juno Kim, Xiao
                                                                          Liu, Amirsaman Memaripour, Yun Joon Soh, Zixuan
[14] Jeremy Condit, Edmund B. Nightingale, Christopher                    Wang, Yi Xu, Subramanya R. Dulloor, Jishen Zhao, and
     Frost, Engin Ipek, Benjamin Lee, Doug Burger, and Der-               Steven Swanson. Basic performance measurements of
     rick Coetzee. Better I/O through byte-addressable, per-              the intel optane DC persistent memory module. CoRR,
     sistent memory. In Proceedings of the ACM SIGOPS                     abs/1903.05714, 2019.
     22nd Symposium on Operating Systems Principles,
                                                                     [23] Daniel Jackson and Craig A. Damon. Elements of style:
     SOSP ’09, page 133–146, New York, NY, USA, 2009.
                                                                          Analyzing a software design feature with a counterexam-
     Association for Computing Machinery.
                                                                          ple detector. IEEE Trans. Softw. Eng., 22(7):484–495,
[15] Jonathan Corbet. ext4 and data loss, March 2009. http:               July 1996.
     //lwn.net/Articles/322823/.                                     [24] Rohan Kadekodi, Saurabh Kadekodi, Soujanya Pon-
                                                                          napalli, Harshad Shirwadkar, Gregory R. Ganger,
[16] Bang Di, Jiawen Liu, Hao Chen, and Dong Li. Fast,
                                                                          Aasheesh Kolli, and Vijay Chidambaram. WineFS:
     flexible, and comprehensive bug detection for persistent
                                                                          A hugepage-aware file system for persistent memory
     memory programs. In Proceedings of the 26th ACM
                                                                          that ages gracefully. In Proceedings of the ACM
     International Conference on Architectural Support for
                                                                          SIGOPS 28th Symposium on Operating Systems Prin-
     Programming Languages and Operating Systems, ASP-
                                                                          ciples, SOSP ’21, page 804–818, New York, NY, USA,
     LOS 2021, page 503–516, New York, NY, USA, 2021.
                                                                          2021. Association for Computing Machinery.
     Association for Computing Machinery.
                                                                     [25] Rohan Kadekodi, Se Kwon Lee, Sanidhya Kashyap, Tae-
[17] Mingkai Dong, Heng Bu, Jifei Yi, Benchao Dong, and                   soo Kim, and Vijay Chidambaram. SplitFS: Reducing
     Haibo Chen. Performance and protection in the ZoFS                   software overhead in file systems for persistent memory.
     user-space NVM file system. Proceedings of the 27th                  In Proceedings of the 27th ACM Symposium on Oper-
     ACM Symposium on Operating Systems Principles,                       ating Systems Principles (SOSP ’19), Ontario, Canada,
     2019.                                                                October 2019.
[18] Subramanya R. Dulloor, Sanjay Kumar, Anil Keshava-              [26] Kate Keahey, Jason Anderson, Zhuo Zhen, Pierre Riteau,
     murthy, Philip Lantz, Dheeraj Reddy, Rajesh Sankaran,                Paul Ruth, Dan Stanzione, Mert Cevik, Jacob Colleran,
     and Jeff Jackson. System software for persistent mem-                Haryadi S. Gunawi, Cody Hammock, Joe Mambretti,
     ory. In Proceedings of the Ninth European Confer-                    Alexander Barnes, François Halbach, Alex Rocha, and
     ence on Computer Systems, EuroSys ’14, New York,                     Joe Stubbs. Lessons learned from the chameleon testbed.
     NY, USA, 2014. Association for Computing Machinery.                  In Proceedings of the 2020 USENIX Annual Technical
                                                                          Conference (USENIX ATC ’20). USENIX Association,
[19] Xinwei Fu, Wook-Hee Kim, Ajay Paddayuru Shreepathi,                  July 2020.
     Mohannad Ismail, Sunny Wadkar, Dongyoon Lee, and
     Changwoo Min. Witcher: Systematic crash consistency             [27] Seulbae Kim, Meng Xu, Sanidhya Kashyap, Jungyeon
     testing for non-volatile memory key-value stores. In                 Yoon, Wen Xu, and Taesoo Kim. Finding semantic bugs
     Proceedings of the ACM SIGOPS 28th Symposium on                      in file systems with an extensible fuzzing framework. In
     Operating Systems Principles, SOSP ’21, page 100–115,                Proceedings of the 27th ACM Symposium on Operating
     New York, NY, USA, 2021. Association for Computing                   Systems Principles, SOSP ’19, page 147–161, New York,
     Machinery.                                                           NY, USA, 2019. Association for Computing Machinery.


                                                                14
[28] Youngjin Kwon, Henrique Fingler, Tyler Hunt, Simon                    2013/01/28/data-center-outage-cited-in-
     Peter, Emmett Witchel, and Thomas Anderson. Strata:                   visa-downtime-across-canada/, 2013.
     A cross media file system. In Proceedings of the 26th
     Symposium on Operating Systems Principles, SOSP ’17,             [37] R. Miller. Power Outage Knocks Dreamhost Customers
     page 460–477, New York, NY, USA, 2017. Association                    Offline.    http://www.datacenterknowledge.com/
     for Computing Machinery.                                              archives/2013/03/20/power-outage-knocks-
                                                                           dreamhost-customers-offline/, 2013.
[29] Philip Lantz, Subramanya Dulloor, Sanjay Kumar, Ra-
     jesh Sankaran, and Jeff Jackson. Yat: A validation frame-        [38] Jayashree Mohan, Ashlie Martinez, Soujanya Ponna-
     work for persistent memory software. In 2014 USENIX                   palli, Pandian Raju, and Vijay Chidambaram. Crash-
     Annual Technical Conference (USENIX ATC 14), pages                    Monkey and ACE: Systematically testing file-system
     433–438, Philadelphia, PA, June 2014. USENIX Asso-                    crash consistency. ACM Trans. Storage, 15(2), apr 2019.
     ciation.
                                                                      [39] Ian Neal, Ben Reeves, Ben Stoler, Andrew Quinn,
[30] Bug 15910 - zero-length files and performance                         Youngjin Kwon, Simon Peter, and Baris Kasikci. AG-
     degradation, 2010. https://bugzilla.kernel.org/                       AMOTTO: How persistent is your persistent memory
     show_bug.cgi?id=15910.                                                application? In 14th USENIX Symposium on Operating
                                                                           Systems Design and Implementation (OSDI 20), pages
[31] Sihang Liu, Suyash Mahar, Baishakhi Ray, and Samira                   1047–1064. USENIX Association, November 2020.
     Khan. Pmfuzz: Test case generation for persistent mem-
     ory programs. In Proceedings of the 26th ACM Inter-              [40] Thanumalayan Sankaranarayana Pillai, Vijay Chi-
     national Conference on Architectural Support for Pro-                 dambaram, Ramnatthan Alagappan, Samer Al-Kiswany,
     gramming Languages and Operating Systems, ASPLOS                      Andrea C. Arpaci-Dusseau, and Remzi H. Arpaci-
     2021, page 487–502, New York, NY, USA, 2021. Asso-                    Dusseau. All File Systems Are Not Created Equal:
     ciation for Computing Machinery.                                      On the Complexity of Crafting Crash-Consistent Ap-
                                                                           plications. In Proceedings of the 11th Symposium on
[32] Sihang Liu, Korakit Seemakhupt, Yizhou Wei, Thomas                    Operating Systems Design and Implementation (OSDI
     Wenisch, Aasheesh Kolli, and Samira Khan. Cross-                     ’14), Broomfield, CO, October 2014.
     failure bug detection in persistent memory programs.
     In Proceedings of the Twenty-Fifth International Con-            [41] Thanumalayan Sankaranarayana Pillai, Vijay Chi-
     ference on Architectural Support for Programming Lan-                 dambaram, Ramnatthan Alagappan, Samer Al-Kiswany,
     guages and Operating Systems, ASPLOS ’20, page                        Andrea C. Arpaci-Dusseau, and Remzi H. Arpaci-
     1187–1202, New York, NY, USA, 2020. Association                       Dusseau. Crash consistency. Commun. ACM, 58(10):46–
     for Computing Machinery.                                              51, 2015.

[33] Sihang Liu, Yizhou Wei, Jishen Zhao, Aasheesh Kolli,             [42] J. Verge.       Internap Data Center Outage
     and Samira Khan. PMTest: A fast and flexible testing                  Takes Down Livestream And Stackexchange.
     framework for persistent memory programs. In Pro-                     http://www.datacenterknowledge.com/archives/
     ceedings of the Twenty-Fourth International Conference                2014/05/16/internap-data-center-outage-
     on Architectural Support for Programming Languages                    takes-livestream-stackexchange/, 2014.
     and Operating Systems, ASPLOS ’19, page 411–425,
     New York, NY, USA, 2019. Association for Computing               [43] Haris Volos, Sanketh Nalli, Sankarlingam Panneersel-
     Machinery.                                                            vam, Venkatanathan Varadarajan, Prashant Saxena, and
                                                                           Michael M. Swift. Aerie: Flexible file-system interfaces
[34] R. McMillan. Amazon Blames Generators For Blackout                    to storage-class memory. In Proceedings of the Ninth
     That Crushed Netflix.    http://www.wired.com/                        European Conference on Computer Systems, EuroSys
     wiredenterprise/2012/07/amazonexplains/,                              ’14, 2014.
     2012.
                                                                      [44] R. S. V Wolffradt.    Fire In Your Data Cen-
[35] R. Miller. Power Outage Hits London Data Center.                      ter: No Power, No Access, Now What?    http:
     http://www.datacenterknowledge.com/archives/                          //www.govtech.com/state/Fire-in-your-Data-
     2012/07/10/power-outage-hits-london-data-                             Center-No-Power-No-Access-Now-What.html,
     center/, 2012.                                                        2014.

[36] R. Miller.      Data Center Outage Cited In                      [45] Jian Xu and Steven Swanson. NOVA: A log-structured
     Visa Downtime Across Canada.            http:                         file system for hybrid volatile/non-volatile main memo-
     //www.datacenterknowledge.com/archives/                               ries. In 14th USENIX Conference on File and Storage


                                                                 15
     Technologies (FAST 16), pages 323–338, Santa Clara,
     CA, February 2016. USENIX Association.
[46] Jian Xu, Lu Zhang, Amirsaman Memaripour, Akshatha
     Gangadharaiah, Amit Borase, Tamires Brito Da Silva,
     Steven Swanson, and Andy Rudoff. NOVA-Fortis: A
     fault-tolerant non-volatile main memory file system. In
     Proceedings of the 26th Symposium on Operating Sys-
     tems Principles, SOSP ’17, page 478–496, New York,
     NY, USA, 2017. Association for Computing Machinery.
[47] Jian Yang, Juno Kim, Morteza Hoseinzadeh, Joseph
     Izraelevitz, and Steven Swanson. An empirical guide
     to the behavior and use of scalable persistent memory.
     In 18th USENIX Conference on File and Storage Tech-
     nologies, FAST 2020, Santa Clara, CA, USA, February
     24-27, 2020, pages 169–182, 2020.




                                                               16
