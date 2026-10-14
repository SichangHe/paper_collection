                                                   OSF OUNDRY: Building and Evolving Operating Systems with
                                                                Specification-Guided Agents

                                             Hengbin Zhang1 , Qingyuan Liu1 , Mo Zou1 , Dong Du1,2 , Yubin Xia1,2 , Haibo Chen1
                                                                             1 Institute of Parallel and Distributed Systems
                                                                          2 Advanced Research Center for Agent-Oriented OS

                                                                                     Shanghai Jiao Tong University


                                                                                              Abstract
arXiv:2609.25018v1 [cs.OS] 8 Aug 2026




                                            Operating systems must evolve continuously. Yet their development remains code-centric and largely manual: even
                                        a localized change can require recovering implicit assumptions, coordinating multiple subsystems, and repeatedly
                                        building, booting, testing, and debugging the complete system. General-purpose coding agents automate individual
                                        edits, but their prompt-centric workflows repeatedly reconstruct task boundaries and OS semantics from scattered
                                        context, limiting their reliability for sustained OS evolution.
                                            This paper presents OSF OUNDRY, an OS-specialized agent harness that makes design intent persistent throughout
                                        OS development. Its key insight is to separate stable intent from diverse implementation. Instead of relying on free-form
                                        natural-language prompts to convey design intent, OSF OUNDRY uses S YS S PEC* , a shared development blueprint
                                        comprising a task-bounding Plan and an OS-specific Specification: the Plan bounds what a change should achieve,
                                        while the Specification records the interfaces, modular dependencies, and concurrency semantics that its implementation
                                        must preserve. Agents implement and validate code against this same blueprint, refining both S YS S PEC* and the
                                        implementation when execution or review exposes a mismatch.
                                            We evaluate OSF OUNDRY along three ways. First, OSF OUNDRY generates S PEC OS from S YS S PEC* ; the resulting
                                        complete OS boots and passes all 70 functional tests. Second, specification patches evolve S PEC OS with a GUI and three
                                        performance optimizations that improve performance by up to 4.41×. Third, across 11 recent Linux-kernel bug-fix tasks,
                                        OSF OUNDRY achieves 1.8× the accuracy of Codex using GPT-5.5. These results show that persistent specifications can
                                        shift OS construction and evolution from repeated manual kernel engineering toward specification-guided development.

                                        1   Introduction
                                        OS development is increasingly defined by customization and continuous evolution. Operating systems must provide
                                        stable abstractions while adapting to new processor architectures such as RISC-V [46], emerging memory interconnects
                                        such as CXL [24] and UB [26], specialized devices such as NPUs and LPUs [36], and changing security and workload
                                        requirements. No single implementation serves all deployment contexts optimally, so developers must continually
                                        construct specialized OS variants and evolve mature kernels such as Linux without breaking existing applications.
                                            Yet the dominant OS development model remains code-centric and largely manual. Developers translate high-level
                                        requirements into low-level patches, recover undocumented assumptions from a large codebase, coordinate changes
                                        across subsystems, and repeatedly build, boot, test, and debug the result. This process is difficult not only because
                                        kernels are large, but also because OS changes are rarely local: a modification to memory allocation, for example,
                                        can affect virtual memory, process creation, page-fault handling, and subsystem-specific performance assumptions.
                                        Consequently, OS development must simultaneously preserve compatibility, respect cross-subsystem contracts, and
                                        accommodate deployment-specific design choices.
                                            LLM-based coding agents offer a promising way to reduce this burden, but their prompt-centric interface is poorly
                                        matched to systems software. General-purpose agents such as Codex, Claude Code, and SWE-agent [3, 37, 50] can
                                        navigate repositories, modify code, and invoke development tools. However, they repeatedly infer task boundaries and
                                        system semantics from a prompt and the surrounding code. Natural-language descriptions rarely capture precise state
                                        transitions, interface assumptions, locking protocols, or hardware-facing invariants, while repository context scatters
                                        this information across implementations, tests, documentation, and comments. As a result, locally plausible code may
                                        compile yet violate a remote dependency or fail only when the complete OS boots and executes.
                                             Corresponding author: dd_nirvana@sjtu.edu.cn.
                                                     Implicit & Sca,ered                               Explicit & Consistent

         1
                                                       Tests                                    Plan    Spec
       Design                                                  Docs
     Semantics
                   Prompt        Code Impl                        Comments   Prompt               SysSpec*              Code Impl




                                                                             Memory          VM           Process                FS
                                            Analyze
         2
                   Memory             VM             Process            FS
    Change &                                                                                      Update aﬀected modules
    Alignment
                                                                                        OSFoundry
                                                                              Build, Test, Debug and Review Loop
                               Build       Test   Debug        Modify

                                                                                                                            ..

         3

  Implementation                             Apply                                      Apply                Generate
    & Evolution             Code #1          Pat(         Code #2            Spec #1    Pat(       Spec #2     Code       New OS
                                                                                                                            ..
                                                                                                                        Kernel Patch

                        (a) Code-Centric Development                   (b) Specification-Guided Development
Figure 1: Code-centric OS development versus OSF OUNDRY. (a) Code-centric development scatters design intent
across prompts, source code, tests, documentation, and comments, leaving developers to coordinate changes across the
OS stack. (b) OSF OUNDRY captures developer intent in S YS S PEC* that records OS semantics, then uses this shared
development blueprint to coordinate implementation, validation, review, and refinement.

    SpecFS [30] established that structured specifications can provide a more reliable interface between developer
intent and LLM-generated systems code. Its S YS S PEC framework captured functionality, modularity, and concurrency
semantics and used them to generate and evolve a complete file system. Nevertheless, SpecFS stopped at a single
user-space subsystem: it did not exercise kernel-mode execution, privilege boundaries, hardware interfaces, or contracts
spanning the full OS stack. Its workflow also began with developer-authored specifications and therefore did not address
how agents should extract task-relevant semantics from an existing kernel or preserve the resulting blueprint throughout
implementation, review, and evolution.
    This paper presents OSF OUNDRY, an OS-specialized agent harness for both constructing new operating systems
and developing or optimizing existing kernels. Its key insight is to separate stable design intent from replaceable
implementation by making design intent a first-class artifact shared by every development stage. As illustrated in Fig.1,
OSF OUNDRY does not ask each agent to reconstruct OS semantics independently from a free-form prompt. Instead, it
uses S YS S PEC* as a persistent development blueprint shared across development stages. Every stage uses this blueprint
to guide its decisions, while OSF OUNDRY refines both the blueprint and code as the task evolves.
    S YS S PEC* comprises a task-bounding Plan and an OS-specific Specification. The Plan states the goals and
non-goals, permissible codebase scope, and observable success criteria for a task. The Specification records the
semantics that an implementation must satisfy: functionality specifications describe state transitions and invariants,
modularity specifications define imported assumptions and exported guarantees, and concurrency specifications make
synchronization and ordering constraints explicit. For a new OS, this blueprint can govern the complete system stack;
for an existing kernel, the specification agent extracts and refines only the semantics relevant to the intended change.
The resulting blueprint is precise and inspectable, but does not claim a machine-checked proof.
    Four specialized agents use this shared blueprint in a closed development loop. The specification agent constructs
S YS S PEC* from developer input and code analysis by producing its Plan and Specification; the implementation agent
realizes the Specification as code under the Plan’s constraints and exercises it through build and test workflows; the
review agent performs general and OS-specific semantic review; and the refinement agent incorporates review findings
and developer feedback before the next iteration. A shared OS knowledge base supplies domain knowledge, while an
executable environment with build tools, QEMU, and GDB grounds decisions in compilation, boot, test, and debugging
evidence.
    OSF OUNDRY maintains full-system semantic context without requiring every agent to process the complete codebase
at once. It organizes the Specification within S YS S PEC* into dependency-aware, context-bounded SpecModules, each
of which contains enough functional and concurrency context for local implementation while exposing explicit rely-
guarantee contracts to other modules. When a requirement changes, a specification patch updates the affected modules
and propagates revised guarantees through their dependents while leaving unrelated contracts intact. This mechanism
enables both generative operating systems, whose implementations are derived from a complete specification, and
scoped evolution of existing kernels, where only the task-relevant blueprint and code must change.
    We demonstrate full-system construction and evolution with S PEC OS, a complete operating system described by
approximately 8K lines of S YS S PEC* and organized into specification-governed modules. The generated system boots,
runs a standard user environment, and passes its test suite. We then evolve the text-based system into a GUI-capable OS
through specification-level patches spanning kernel graphics support, user-space services, libraries, and applications.
We further apply performance-oriented patches for a per-CPU page allocator, copy-on-write fork, and batched pipe I/O;
the resulting implementations preserve their external contracts while improving performance by up to 4.41×.
    We separately evaluate whether the same architecture improves development in an existing kernel. Across 11
representative Linux-kernel bug-fix tasks, OSF OUNDRY achieves 1.8× the accuracy of Codex using GPT-5.5. Together,
the two evaluations show that specification-guided agents can move beyond isolated code generation: they can construct
and evolve a complete OS while also making scoped development in a mature kernel more accurate and reliable.
    This paper makes the following contributions:

• We introduce OSF OUNDRY, an OS-specialized agent harness that makes developer intent a persistent, first-class
  artifact shared across specification, implementation, review, and refinement. Its S YS S PEC* development blueprint
  comprises a task-bounding Plan and an OS-specific Specification, while a shared knowledge base and executable
  environment support both complete OS construction and scoped development of existing kernels.
• We extend the specification-guided approach of SpecFS from a single subsystem to the full OS stack and implement
  S PEC OS, a complete OS described by approximately 8K lines of S YS S PEC* . S PEC OS boots, runs a standard user
  environment, and evolves through specification patches to support a GUI and multiple performance optimizations,
  including one that improves performance by up to 4.41×.

• We evaluate OSF OUNDRY on 11 representative Linux-kernel bug-fix tasks. Compared with Codex using GPT-5.5,
  OSF OUNDRY achieves 1.8× the accuracy.

2     The Case for Agentic OS Development

2.1    Growing Demand for OS Customization
OS customization is a fundamental requirement rather than a niche optimization. Computing platforms span embedded
devices with kilobytes of memory, mobile systems governed by energy and security constraints, and warehouse-scale
services operating across millions of cores. No single OS configuration or implementation can serve these environments
optimally. Each target instead requires a particular composition of scheduling policies, memory-management strategies,
I/O paths, device support, and security mechanisms.
    Today, deriving these purpose-built variants remains largely manual. Developers typically fork or configure an
existing kernel, add platform-specific modules, and patch subsystem implementations until the resulting system satisfies
a target workload. Because the intended design is distributed across configuration files, source code, tests, and
documentation, reproducing or transferring a customization to another variant requires substantial engineering effort.
    The demand for such customization is both broad and growing. As summarized in Fig.2(a), emerging architectures,
accelerators, device forms, and workloads all impose different policies on a common set of OS mechanisms. Our study
of OS-related GitHub repositories over the past eight years further shows sustained growth in newly created repositories
(Fig.2(b)). The broader ecosystem of Linux distributions and vendor-maintained Android variants reinforces the same
point: developers repeatedly assemble different systems from closely related subsystem foundations.
    This diversity creates a compounding cost. A purpose-built OS is not finished once it boots; it must continue to
absorb new hardware support, security defenses, optimizations, and application requirements. The practical challenge
is therefore not merely producing more variants, but evolving many variants without repeatedly rediscovering and
reimplementing the same system semantics.
      Emerging targets              Shared OS mechanisms                  Purpose-built OSes

          Architectures                                                     Cloud OS                                           17,500
                                                                            throughput + isolation                                         Repositories
          x86 | ARM | RISC-V                                                openEuler, Anolis, AWS OS
                                               Scheduling                                                                      15,000




                                                                                                        Repositories Created
          Accelerators                                                      Mobile OS
                                                                            energy + responsiveness                            12,500
          GPU | NPU | DPU                       Memory




                                                                                                            per Month
                                                                            HarmonyOS, iOS, Android


          Device forms                      I/O & Network                   Automotive OS
                                                                                                                               10,000
                                                                            real time + safety
          Cloud | Mobile | Auto                                             QNX, seL4, HarmonyOS
                                                Drivers                                                                         7,500
                                                Security
          Workloads                                                         Edge / AI OS
                                                                            accelerators + locality                             5,000
          AI | Real-time | Secure                                           FreeBSD, LiteOS, VxWorks
                                    Different policies and compositions
                                                                                                                                2,500
                     Increasing platform diversity and customization demand
                                                                                                                                        2019 2020 2021 2022 2023 2024 2025 2026
                                                                                                                                                          Year

                          (a) The need for OS customization.                                                               (b) New OS-related repositories per month.
Figure 2: Growing demand for OS customization. (a) Diverse architectures, accelerators, device forms, and workloads
impose different requirements on shared OS mechanisms, motivating purpose-built variants. (b) The sustained growth
in newly created OS-related GitHub repositories provides empirical evidence of this demand.

2.2      Why OS Evolution Is Difficult
2.2.1     Forces Driving Kernel Evolution
OS evolution is continuous because the environment beneath and above the kernel never stops changing. Linux has
evolved for more than three decades, growing from roughly 10,000 lines in version 0.01 (1991) to tens of millions of
lines today [29]. Tab.1 illustrates this process through representative features organized by six recurring technological
forces.
Hardware scale and data movement. The transition from single-core to many-core processors, from uniform memory
to NUMA and persistent memory, and from disks to NVMe has repeatedly forced redesigns of scheduling, memory
management, and storage paths. Network line rates have similarly driven multi-core packet steering, in-driver processing,
and new congestion-control mechanisms. These changes alter not only individual algorithms, but also the concurrency
and data-placement assumptions shared across subsystems.
Deployment and policy diversity. Virtualized and containerized clouds require strong isolation, resource accounting,
and device virtualization, while mobile systems make energy management and low-latency IPC first-class concerns.
The same kernel must therefore support substantially different resource policies and trusted computing boundaries. This
pressure expands both the number of mechanisms and the configurations in which they must coexist.
Security and programmability. New attacks continually add defense layers such as mandatory access control, syscall
filtering, address randomization, and microarchitectural mitigations. At the same time, eBPF and related mechanisms
expose controlled programmability inside performance-critical kernel paths. Both trends increase the semantic surface
that future changes must preserve.
     These forces are persistent rather than episodic. As hardware and workloads continue to diversify, OS developers
must repeatedly introduce new mechanisms while retaining the behavior on which existing applications and deployments
depend.

2.2.2     Three Structural Challenges
The difficulty of OS evolution lies not only in what changes, but in three recurring properties of how change must occur,
summarized in Fig.3.
Compatibility turns replacement into coexistence. New kernel mechanisms rarely replace old ones abruptly. The
kernel must preserve user-visible interfaces and behavioral semantics, so migration proceeds incrementally and old and
new paths may coexist for years. Scheduler evolution illustrates this constraint: CFS replaced the O(1) scheduler while
preserving the sched_class abstraction, and EEVDF later changed the core scheduling algorithm while retaining the
external class hierarchy and cgroup integration. Internal implementation can change substantially, but externally visible
guarantees cannot.
Subsystem coupling makes local changes non-local. Although a kernel is organized into named subsystems, significant
features routinely cross their boundaries. The cgroups v2 redesign, for example, required changes not only to the
                     Table 1: Representative Linux kernel features and their evolutionary drivers.

 Motivation                Feature                     Kernel Version    Description
 Multicore & Scalability   O(1) Scheduler → CFS        2.6.0 / 2.6.23    Fair scheduling for multi-core systems
                           Transparent Huge Pages      2.6.38            Automatic huge pages to reduce TLB misses
                           AutoNUMA                    3.8               Automatic page migration for NUMA locality
                           blk-mq                      3.13              Multi-queue block layer for parallel I/O
                           DAX                         4.0               Direct access to persistent memory, bypassing
                                                                         page cache
                           io_uring                    5.1               Async I/O via shared ring buffers
                           EEVDF Scheduler             6.6               Deadline-fair scheduling replacing CFS
 Virtualization & Cloud    KVM                         2.6.20            In-kernel hypervisor for hardware virtualization
 Computing
                           PID & Net Namespaces        2.6.24            Process and network isolation for containers
                           Cgroups v1 / v2             2.6.24 / 4.5      Hierarchical resource control; v2 unified hierar-
                                                                         chy
                           OverlayFS                   3.18              Layered filesystem for container images
                           VFIO                        3.6               IOMMU-backed direct device assignment to
                                                                         VMs
 Network Bandwidth &       RPS / RFS / XPS             2.6.35            Multi-core packet steering in software
 Latency
                           nftables                    3.13              Flexible successor to iptables
                           XDP                         4.8               BPF packet processing at driver level
                           BBR                         4.9               Model-based congestion control
                           MPTCP                       5.6               Multi-path TCP for bandwidth aggregation
 Mobile & Power Effi-      Tickless Kernel             2.6.21            Eliminate idle timer interrupts
 ciency
                           Wakelocks                   3.5               Suspend-aware power management for mobile
                           Binder IPC                  3.19              Android’s high-performance IPC mechanism
                           schedutil Governor          4.7               Scheduler-driven CPU frequency scaling
                           PSI                         4.20              Unified resource pressure metrics
 Security Threats          SELinux                     2.6.0             Mandatory access control
                           seccomp                     2.6.12            System call filtering
                           KASLR                       3.14              Kernel address randomization
                           KPTI                        4.15              Kernel/user page table isolation (Meltdown fix)
                           Retpoline                   4.15              Spectre v2 indirect branch mitigation
                           Landlock                    5.13              Unprivileged stackable sandboxing
 Programmability           eBPF Verifier + Helpers     3.18–5.x          Safe in-kernel VM for user-defined programs
                           BPF CO-RE                   5.3               Portable BPF across kernel versions
                           sched_ext                   6.12              BPF-programmable scheduling policies


cgroup core but also to resource controllers, the page and slab allocators, the OOM killer, scheduling, block I/O, and
networking. The pace and correctness of one change therefore depend on maintainers identifying every affected contract
and coordinating updates across modules.
Deployment diversity shifts the kernel/userspace boundary. Different workloads place conflicting functionality on
either side of the privilege boundary. DAX and io_uring move data-path work away from conventional kernel mediation,
whereas eBPF, XDP, and sched_ext place user-defined policies inside kernel execution paths. Cloud deployments may
favor a smaller kernel role on throughput-critical paths, while mobile systems depend on integrated kernel control for
energy management and security. Supporting these choices multiplies code paths, interactions, and semantic contracts.
    Together, compatibility, subsystem coupling, and deployment diversity make OS evolution a semantic-coordination
problem. Writing a locally plausible function is insufficient; developers must preserve contracts across versions,
modules, privilege levels, and deployment configurations. In a code-centric workflow, these contracts remain implicit
and scattered, which is precisely the information an agentic development system must make explicit.
                                                                                                                  Cloud / HPC                       Mobile / secure
        Stable user-visible ABI and semantics                 Scheduler                           Memory
                                                                                                                  Applications                        Applications
                                   legacy path remains
                                                                                                                 I/O bypass + policy                   stable services
            Old mechanism

                                                                                 Local                              Userspace                           Userspace
                                                              Block I/O                            Network
                                                                                feature                           runtime services




                                                                                                                                           sftihs
                                                                                                                                                          Kernel
                            New mechanism                                                                                                             power + security
                                                               Drivers                            Security             Kernel                        integrated control
       t0                     t1                         t2
                                                                                                                less kernel on data path            more kernel for control
               Internal replacement is gradual;                    A local redesign triggers coordinated                    Different deployments require
               external behavior cannot break.                    changes and validation across modules.                   different kernel/userspace splits.

       (a) Compatibility and coexistence                         (b) Cross-subsystem propagation                (c) Deployment-dependent boundary

Figure 3: Why OS evolution is difficult. (a) New mechanisms must coexist with legacy paths while preserving user-
visible semantics. (b) A local feature can trigger coordinated changes across tightly coupled subsystems. (c) Different
deployments place functionality on different sides of the kernel/userspace boundary, multiplying the configurations and
contracts that must be maintained.

2.3   Why Prior Efforts Fall Short

                           Table 2: Review of prior work and comparison with the design of OSF OUNDRY.

                              Prior Work                                                                     Design in OSF OUNDRY
 Agent Harness                Codex [37], Claude Code [3], and SWE-agent [50] provide                        An OS-specialized multi-agent loop keeps
 and Workflow                 general-purpose capabilities for repository navigation, code                   specification, implementation, review, and
                              modification, and development-tool invocation; AHE [28] and                    refinement aligned around shared system
                              VeRO [45] treat the agent harness itself as an optimization                    semantics.
                              target, adapting its workflow and scaffolding over time.
                              Analysis: The former lack OS-specific contracts, while the
                              latter optimize the agent scaffold rather than target-system
                              semantics.
 Specification-               Spec Kit [16], and Kiro [2] persist requirements, specifications,              An OS-specific S YS S PEC* couples a
 Driven                       plans, and tasks, with repository grounding and validation.                    task-bounding Plan with a Specification
 Development                  Analysis: Their artifacts are generic and do not natively encode               for OS semantics, keeping development
                              OS functional, modular, and concurrency semantics.                             intent and system semantics aligned with
                                                                                                             the implementation.
 OS Development               For bug fixing, kAgent [33] and Code Researcher [41] use                       One specification-guided workflow
 Scope                        crash evidence and repository context to generate Linux-kernel                 supports both complete OS construction
                              patches. For fault localization, LinuxFL+ [55] uses bug reports                and the evolution of existing kernel code.
                              and kernel evidence to localize faulty files. For specification
                              generation, OSVBench [25] evaluates LLMs on synthesizing
                              complete Hyperkernel state-transition specifications.
                              Analysis: These approaches target individual
                              kernel-development tasks rather than end-to-end OS
                              development.
 Verification and             seL4 [22], CertiKOS [17], and Hyperkernel [34] use                             OSF OUNDRY does not provide
 Validation                   machine-checked refinement or automated verification.                          machine-checked proofs; it uses
                              Analysis: They provide stronger correctness guarantees, at the                 structured semantic contracts, execution
                              cost of formal models and substantial proof or specification                   feedback, and semantic review for
                              engineering.                                                                   lightweight validation.

    Prior work addresses important pieces of agentic software development, specification-driven engineering, and
verified OS construction, as summarized in Tab.2. However, no prior approach in the table connects task intent, OS
semantics, implementation, and execution evidence through one shared development blueprint. The missing capability
is therefore architectural rather than simply a matter of using a stronger language model.
General-purpose harnesses coordinate actions, but not OS semantics. Coding agents such as Codex, Claude Code,
and SWE-agent can navigate repositories, modify code, and invoke development tools, while AHE and VeRO optimize
the agent scaffold itself. These systems improve how an agent operates, but do not define the syscall behavior, interface
assumptions, locking protocols, or hardware invariants that a particular OS task must preserve. Each implementation or
review stage may consequently reconstruct a different interpretation of the same change.
Workflow specifications are too generic, while verified OSes require proof engineering. Spec Kit and Kiro persist
requirements, plans, and tasks, but their artifacts do not natively encode OS functionality, modular dependencies, and
concurrency semantics. At the other end of the design space, seL4, CertiKOS, and Hyperkernel provide stronger
machine-checked guarantees at the cost of formal models and substantial proof or specification engineering. An agentic
OS workflow needs a practical middle ground: artifacts precise enough to guide implementation and semantic review,
but lightweight enough to author or extract during ordinary development.
OS-oriented coding agents remain task-specific. Existing efforts use LLMs for kernel patch generation, fault localiza-
tion, or specification synthesis. These are valuable capabilities, but their outputs do not form a shared development
blueprint that persists from task definition through implementation, whole-system validation, review, and later refine-
ment. Nor do they provide one workflow that supports both constructing a complete OS and modifying an existing
kernel.
     These comparisons expose four requirements for end-to-end agentic OS development. The system must persist task
boundaries and OS semantics, enable local reasoning without losing cross-module dependencies, ground decisions in
build and execution evidence, and refine the blueprint as requirements or review findings evolve. The next subsection
examines why SpecFS provides a promising semantic foundation and which gaps remain before these requirements can
be met.

2.4    S YS S PEC: Foundation and Limitations
SpecFS [30] established that structured specifications can serve as a precise interface between system designers and
LLM-based coding agents. It introduced S YS S PEC, a framework for specification-guided system construction and
evolution, and instantiated the framework in a concurrent file system. Rather than asking an LLM to recover system
semantics from a free-form prompt or an entire codebase, developers encode design intent in structured, formal-
method-inspired contracts that guide generation, review, and evolution. S YS S PEC is deliberately not a proof language;
it uses structured natural language and type annotations while adapting disciplined concepts from Hoare logic and
rely-guarantee reasoning.
Structured semantic contracts. S YS S PEC models a system as context-bounded modules governed by three com-
plementary specifications. A functionality specification describes state transitions through Hoare-style preconditions,
postconditions, invariants, and, when necessary, a high-level algorithm [6, 56]. A modularity specification makes
dependencies explicit through adapted rely-guarantee contracts [14]: Rely clauses state imported types, functions, and
assumptions, while Guarantee clauses define exported interfaces and behavior. A separate concurrency specification
records lock ownership, ordering constraints, and concurrency-related preconditions and postconditions. Together,
these contracts provide enough local context to implement one module while retaining the semantics required for
composition.
Specification-guided construction and evolution. S YS S PEC treats the specification, rather than generated C code,
as the primary design artifact. A DAG-structured spec patch decomposes a feature into localized changes and makes
propagation dependencies explicit: leaf nodes introduce self-contained changes, intermediate nodes update dependent
guarantees, and root nodes preserve externally visible behavior. The SpecFS toolchain couples specification authoring,
module-level generation, specification-aware validation, and retry with actionable feedback. This loop mitigates LLM
failures without assuming that generated code is intrinsically reliable.
What SpecFS demonstrated. SpecFS described the high-level design of AtomFS [56] in 45 specification-governed
modules and generated approximately 4.3K lines of C. Its user-space FUSE implementation matched AtomFS’s test
profile across 754 xfstests cases, with remaining failures corresponding to functionality outside the prototype’s scope.
SpecFS also evolved the design through ten representative Ext4 features using specification patches. These results
established that structured semantic contracts can guide LLMs in constructing and evolving a complete OS subsystem.
What SpecFS left open. SpecFS nevertheless stopped at a single user-space subsystem. It did not exercise kernel-mode
execution, hardware-facing interfaces, privilege transitions, or contracts spanning memory management, processes,
system calls, device drivers, and the user runtime. Its workflow began with developer-authored draft specifications,
leaving specification extraction from an existing codebase unaddressed. Finally, file-system-level validation could
not expose build, boot, or full-system integration failures that emerge only when kernel and user modules execute
together. SpecFS therefore did not establish whether specification-guided agents can scale to a complete OS or improve
development in an existing kernel.

2.5    Opportunity: Consistent Design Intent for Agentic OS Development
The preceding evidence points to a broader opportunity. OS customization creates sustained demand for specialized
systems, OS evolution requires coordination across implicit semantic contracts, existing agentic tools cover only
fragments of the lifecycle, and SpecFS shows that structured specifications can make system semantics actionable
for LLMs. The missing abstraction is a persistent representation of design intent shared across every stage of the OS
development lifecycle.
    The key insight is to separate stable design intent from replaceable implementation. S YS S PEC* , an extension of
S YS S PEC, forms this shared development blueprint. It comprises a task-bounding Plan, which records goals, non-goals,
codebase scope, and success criteria, and an OS-specific Specification, which records the functionality, modularity, and
concurrency semantics that an implementation must preserve. Implementation, execution, review, and refinement can
then operate on the same interpretation of developer intent rather than reconstructing it independently.
    This blueprint enables two complementary forms of agentic OS development. For a new system, a complete
collection of modular specifications defines a generative OS (S PEC OS in §5.1): a family of implementations that can
be synthesized, customized for a target, and evolved by updating specifications while preserving external guarantees.
For an existing kernel (e.g., Linux kernel), the blueprint can instead be task-bounded: agents extract and refine only the
semantics relevant to a feature or optimization, then use build, boot, test, and review evidence to validate the resulting
patch. Existing-kernel development therefore does not require rewriting or specifying the entire system.
    This reasoning leads directly to OSF OUNDRY, an OS-specialized agent harness that keeps S YS S PEC* , implementa-
tion, and validation evidence aligned throughout the development lifecycle. Its purpose is not to replace OS developers
with LLMs, but to elevate their role by changing how design intent is expressed, preserved, and evolved.

3     Design Overview
This paper presents OSF OUNDRY, an OS-specialized agent harness for both constructing a new operating system
and developing or optimizing an existing kernel such as Linux. As shown in Fig.4, OSF OUNDRY makes developer
intent persistent through a shared development blueprint. Every stage uses this blueprint to guide its decisions, while
OSF OUNDRY refines both the blueprint and code when the task evolves. For a new OS, the blueprint can govern the
complete system stack; for an existing kernel, it bounds the intended change and captures only the relevant system
semantics.
Insight: separate stable design intent from replaceable implementation. The key insight behind OSF OUNDRY
is that reliable agentic OS development requires making design intent a first-class artifact shared by every stage of
development.
    General-purpose agents repeatedly infer behavior, change boundaries, and OS invariants from a prompt and a large
codebase; a locally plausible edit can therefore violate a remote interface, locking protocol, or hardware-facing invariant.
OSF OUNDRY externalizes this information in a structured, formal-method-inspired blueprint that all agents consume
during generation, execution, review, and refinement. This blueprint is precise and inspectable, but does not claim a
machine-checked proof.
Harness architecture. OSF OUNDRY comprises three mutually reinforcing layers: an intent layer centered on
S YS S PEC* , with a task-bounding Plan and an OS-specific Specification as its two components (Fig. 4(a)); an agent
layer containing the four specification, implementation, review, and refinement roles; and an infrastructure layer that
grounds their closed loop in a shared OSKB and an executable environment with QEMU and GDB (Fig.4(b)). Together,
these layers address four challenges that arise when moving from a general-purpose coding agent to an end-to-end OS
development harness.
Challenge 1: How can developer intent become an actionable OS spec? A natural-language request rarely states
non-goals, permissible changes, completion conditions, or implicit OS semantics. OSF OUNDRY addresses this
ambiguity through the two components of S YS S PEC* . The Plan defines (1) goals and non-goals, (2) codebase scope
and allowed dependencies, and (3) success criteria as observable properties and executable checks. The Specification
                                                                                                                  Developer Intent
                                       Developer Intent

                                                                                                                     Agent#1                    OS Environment
                                                                                                                  (Speciﬁcation)
                   Plan                                              Speciﬁcation                                    Grilling
                                                                                                                                                                  GDB
                                                                                                                  Code Analysis

    Goal and                    Success           Functionality       Modularity       Concurrency
                  Scope                                                                                                                             Agent#2
    Non-Goal                    Criteria          Speciﬁcation       Speciﬁcation      Speciﬁcation
                                                                                                                                                (Implementation)
                                                                                                         SpecOS      SysSpec*                    Code Generation

                                                   SpecModule                 read: pre:=.., post:=..,                                               Plan Validation
                                                                                   invariants=..
                                                                  Module-4    Rely: module-2/3
                                                 Module-3                     Guarantee: read                                                    Implementation
                                                                              Con: pre:=cur is
                                                                              locked, post:=.., no
                                                 Module-1         Module-2                                          Agent#4                            Agent#3
                                                                              double release
                                                                                                                  (Reﬁnement)                          (Review)
                                                                                                                   Spec Update                       General Review
                                                                                                                        +                                  +
                                                                                                                   Plan Update                  OS-Speciﬁc Review
                                Agent#2 (Implementation)

                                                                                                                                                 Review Findings

                ImpModule (C)                    ImpModule (Rust)
                                                                                                                                Developer Feedback
                ImpMod-3    ImpMod-4        ..   ImpMod-3         ImpMod-4
                                                                                                                       Operating System Knowledge Base
                ImpMod-1    ImpMod-2             ImpMod-1         ImpMod-2                                                          (OSKB)

               (a) Spec-Driven Design and Implementation                                                                (b) Multi-Agent Toolchain

Figure 4: Design overview of OSF OUNDRY. (a) Developer intent is captured by S YS S PEC* , which comprises a task-
bounding Plan and an OS-specific Specification; the latter’s functionality, modularity, and concurrency specifications
form dependency-aware SpecModules; an implementation agent realizes these modules in a target systems language.
(b) Four specialized agents construct the development blueprint, implement it in an executable OS environment, review
the resulting code, and refine the blueprint using review findings and developer feedback. All agents share an operating
system knowledge base (OSKB).


records the behavior that the implementation must preserve: functionality specifications define state transitions with
preconditions, postconditions, invariants, and, when needed, high-level algorithms; modularity specifications define
imported assumptions and exported guarantees; and concurrency specifications isolate locking, synchronization, and
ordering constraints.
    Through iterative grilling and code analysis, the specification agent can construct S YS S PEC* for a new system or
extract and refine its task-relevant components around an existing implementation.
Challenge 2: How can agents reason locally without losing full-system semantics? An OS is too large to place in
one generation context, yet generating one component in isolation can break dependencies across memory management,
processes, file systems, device drivers, and the user runtime. OSF OUNDRY resolves this tension by organizing the
Specification as a graph of context-bounded SpecModules. Each module contains the functionality and concurrency
semantics needed for local implementation, while its modularity specification names the other modules on which it
relies and the guarantees it provides to dependents. These explicit contracts preserve cross-module context without
exposing the entire codebase to every generation step. The implementation agent can consequently synthesize and
revise modules one at a time, compose them according to their dependencies, and target different systems languages,
including C and Rust.
Challenge 3: How can plausible code be turned into an executable OS implementation? Even with S YS S PEC* ,
LLM-generated code may still fail to compile, boot, or satisfy subtle interface and synchronization requirements. The
implementation agent therefore couples code generation with Plan validation and exercises candidates in a realistic
OS environment using the available build, test, QEMU, and GDB workflows. A separate review agent then performs
two complementary checks: general code review detects conventional implementation defects, while OS-specific
review checks the candidate against the functionality, interface, and concurrency semantics in the Specification. The
shared OSKB supplies consistent domain knowledge and codebase conventions to all agents. Together, Plan validation,
execution feedback, and specification-aware review provide lightweight defense in depth without claiming formal
verification.
Challenge 4: How can the harness support evolution rather than one-shot generation? Review findings often
expose an underspecified design rather than an isolated coding mistake, while developer feedback may intentionally
change the task itself. The refinement agent therefore updates S YS S PEC* by refining its Plan and affected parts of
its Specification: it refines task boundaries and success criteria when requirements change, and it strengthens system
contracts when implementation or review reveals a missing semantic constraint. For changes that span multiple modules,
dependency-aware specification patches identify the affected SpecModules and propagate updated guarantees through
their dependents; unrelated modules retain their existing contracts. The revised S YS S PEC* returns to the implementation
agent, closing the loop until the implementation satisfies the current blueprint. Consequently, the same architecture
governs both full-system construction and evolution in S PEC OS and scoped development in Linux.

4     Design

4.1     Bridging User Intent and OS Implementation with S YS S PEC*
OSF OUNDRY bridges high-level developer intent and low-level OS implementation through S YS S PEC* , a persistent
blueprint with two complementary components. Starting from an often incomplete natural-language request, the
specification agent uses iterative grilling and system analysis to construct S YS S PEC* by co-developing a Plan that
bounds the current development task and a Specification that captures the functionality, modularity, and concurrency
semantics that its implementation must establish or preserve. Because the initial intent does not fully determine either
component, both are progressively refined as additional requirements and system constraints emerge. This blueprint
provides a persistent and inspectable basis for implementation, review, and subsequent refinement.
Extending S YS S PEC to kernel-scale systems. SpecFS introduced S YS S PEC, a formal-method-inspired specification
framework, and demonstrated that such specifications can guide LLMs in constructing and evolving a context-bounded
user-space file-system subsystem. S YS S PEC* extends S YS S PEC by combining a task-bounding Plan with an OS-
specific Specification. Its Specification component retains the three complementary specification forms introduced
by S YS S PEC—functionality, modularity, and concurrency specifications—but extends their scope to multi-module
operating systems. The Specification also supports incremental specification: a task may describe only the semantic
changes to an existing module, while unmentioned semantics remain inherited from its current specification. Like
S YS S PEC, S YS S PEC* remains a lightweight and structured natural language representation for guiding implementation
and review rather than a machine-checked proof language.
Adding task boundaries through the Plan. The Specification component specifies the requested semantic change and
the system contracts that its implementation must establish or preserve. These contracts do not by themselves bound the
development cycle, which also requires shared task objectives and exclusions, a permissible implementation scope, and
observable completion criteria. The Plan provides this task-level guidance without redefining the semantics captured by
the Specification, preventing unnecessary changes and ensuring that the task does not terminate before its objectives are
achieved.

4.1.1   Functionality Specification
The functionality specification describes the state transitions of a module using pre- and post-conditions, system
algorithms, and invariants. The amount of algorithmic guidance scales with the complexity of the specified logic. A
Level 1 specification uses pre- and post-conditions to define the allowed transition without prescribing its implementation.
A Level 2 specification additionally provides a system algorithm when correctness, performance, or architectural
constraints require a particular implementation strategy. Invariants are orthogonal to these levels: they state properties
that must remain true throughout execution whenever local entry and exit conditions alone are insufficient.
Pre- and post-conditions. We adapt the Hoare-logic form {P}C{Q} as a lightweight behavioral contract rather than a
proof obligation requiring full formal verification. The contracts are expressed in structured natural language, augmented
with types and program expressions, so that they can directly guide implementation and review. Pre-conditions define
the states required before an operation may execute, while post-conditions guarantee its state transitions and return
values. For the user-space components targeted by S YS S PEC, assumptions over function arguments and module-local
state were often sufficient. Kernel behavior, however, can also depend on execution context, such as the current privilege
level, interrupt or preemption state, address space, and global kernel state. The functionality specification within
S YS S PEC* therefore extends these contracts to capture the relevant system state in addition to functional inputs. For
example, Fig.5 specifies how mem_check combines its socket argument with system-wide privilege and accounting
state to decide whether another flow label may be allocated.

    FUNCTIONALITY SPECIFICATION

    Pre-condition:
      Function arguments:
        - sk denotes a valid IPv6 socket.
      System state:
        - current’s CAP_NET_ADMIN state determines whether unprivileged
          allocation limits apply.
        - fl_size, sk’s flow-label list, and sock_net(sk)->flowlabel_count
          describe the current allocation state.

    Post-condition:
    Case 1 Global pool exhausted
      - Return -ENOBUFS.
    Case 2 Unprivileged limit exceeded
      - Return -ENOBUFS if an applicable global-pressure, per-socket,
        or per-netns limit is reached.
    Case 3 Allocation admitted
      - Return 0.

    Invariant:
      - fl_size equals global hash membership, and each flowlabel_count
        equals its network namespace’s hash membership.

                            Figure 5: Simplified functionality specification for mem_check.


System algorithm. Pre- and post-conditions constrain what an operation must accomplish, but multiple implementations
can satisfy the same state transition while having materially different performance or architectural consequences. A
system algorithm constrains how the transition should be achieved by describing its major steps, data-structure choices,
or required optimization strategy. For example, the contracts for kalloc() and kfree() may only require allocating
and returning a free page. A single global free list satisfies that behavior but serializes allocation on a multicore system.
A Level 2 specification can instead require per-CPU free lists, with local allocation in the common case and cross-CPU
page transfer only when a local list is exhausted, thereby preserving the same functional contract while constraining the
implementation to a scalable design.
Invariants. Invariants describe properties that must remain valid throughout an operation, rather than only at its entry
and return. They constrain the intermediate actions of every function that can affect the relevant state and therefore
cannot be captured completely by local pre- and post-conditions. For instance, an allocator must never place the same
physical page on two free lists, and a page reachable through an active mapping must not simultaneously be considered
free. Stating these constraints separately avoids duplicating them across function contracts and makes them available to
both implementation and review.

4.1.2   Modularity Specification
The modularity specification defines how a module composes with the rest of the OS by making its external dependencies
and exposed contract explicit. At kernel scale, placing the entire codebase in an LLM’s context is impractical, while
reasoning about a module in isolation can miss assumptions imposed by other subsystems or privilege layers. The
modularity specification within S YS S PEC* adapts rely-guarantee reasoning [14] to make these composition boundaries
explicit: each module states the external conditions on which its implementation depends and the contract that other
modules may assume about it. These contracts provide the context needed to implement a task-relevant module without
loading or reconstructing the implementation details of the entire OS.
Rely. A rely clause records assumptions supplied from outside the current module. We distinguish two kinds of relies
by the entity that discharges the assumption, rather than by the granularity at which the assumption is expressed. A
component rely is an assumption discharged by the guarantee of an identifiable SpecModule, whether it names a
function, an interface, an entire module, or a semantic capability. This generalizes S YS S PEC, in which component
relies were typically expressed as function APIs with pre- and post-conditions, while preserving a concrete provider for
each dependency. A platform rely, by contrast, is a module-specific assumption about the selected execution substrate
that the module consumes directly and that is not mediated by any SpecModule guarantee. It therefore constrains
the targets on which the module can execute rather than creating an edge in the SpecModule dependency graph. For
example, trap-entry code may rely directly on the architecture’s trap semantics, whereas a module that consumes a trap
representation supplied by an architecture module relies on that module’s guarantee.
Guarantee. A guarantee clause defines the externally visible contract that a module provides to its dependents, including
its callable interfaces and their observable semantics. This contract establishes an abstraction boundary: dependents
may rely on the declared behavior, while internal functions, data structures, and implementation choices remain
hidden. Limiting dependencies to the guarantee prevents accidental coupling to kernel internals and allows a module’s
implementation to change as long as its exposed contract is preserved. In Fig. 6, for example, the IPv6 flow-label
socket-option dispatcher relies directly on the GET, PUT, and RENEW handlers. Its guarantee exposes a single dispatch
interface that validates the request, selects the corresponding handler, and propagates its result.

    MODULARITY SPECIFICATION

    [RELY]
    ipv6_flowlabel_get(sk, freq, optval, optlen)
      // Handles GET and CREATE requests.
    ipv6_flowlabel_put(sk, freq)
      // Releases the requested socket-owned flow-label reference.
    ipv6_flowlabel_renew(sk, freq)
      // Renews the requested flow label’s lifetime.

    [GUARANTEE]
    int ipv6_flowlabel_opt(struct sock *sk, sockptr_t optval, int optlen)
      // Copies and validates struct in6_flowlabel_req.
      // Dispatches GET, PUT, and RENEW to the corresponding handler.
      // Returns -EINVAL for an unsupported action; otherwise propagates
      // the selected handler’s return value.

               Figure 6: Rely–Guarantee specification for the IPv6 flow-label socket-option dispatcher.


Controlled composition. For modules to compose, every component rely must be entailed by its identified provider’s
guarantee. Every platform rely must instead hold on the selected execution target, thereby defining a compatibility
constraint at the boundary of the SpecModule graph. A kernel imposes stricter composition boundaries than a self-
contained subsystem: modules cannot arbitrarily depend on internal behavior or expose contracts to every other
component. For example, a file system integrates with the VFS through registered operation interfaces such as
file_operations and inode_operations, rather than relying on arbitrary VFS internals. Across the privilege
boundary, user programs can invoke kernel services only through the system-call ABI; internal kernel functions are
not exposed as guarantees to user space. Restricting composition to these explicit abstraction boundaries preserves
privilege isolation, prevents unintended cross-module coupling, and allows internal implementations to evolve without
forcing unrelated dependents to change.

4.1.3   Concurrency Specification
The concurrency specification defines how a module coordinates access to shared kernel state under concurrent execution.
Because kernel execution may interleave across CPUs, scheduler preemption, and interrupts, its synchronization
constraints are difficult to infer from functional logic and costly to repeat for every function. The concurrency
specification within S YS S PEC* therefore separates concurrency into locking protocols for reusable rules and locking
logic for operation-specific synchronization.
Locking protocol. A locking protocol defines the synchronization discipline shared by all operations that access the
same state, independently of any one function’s functional algorithm. For modules with simple and uniform concurrency,
the protocol alone can fully specify the required synchronization discipline. In Fig.7, the spinlock protocol requires
every access to the global flow-label hash and its membership counters to hold ip6_fl_lock, with process and timer
paths using the locking primitive appropriate to their execution context. Stating this discipline once avoids repeating it
in every operation that accesses the protected state.
Locking logic. Locking logic specifies how a particular operation follows a protocol when the module-wide disci-
pline alone does not determine the required critical-section boundaries. In the same figure, the locking logic for
ipv6_flowlabel_get places admission checking and insertion in one critical section, including a duplicate recheck
before publishing a new label. Separating this logic from allocation policy makes the synchronization behavior
independently inspectable without repeating unrelated functional semantics.

    CONCURRENCY SPECIFICATION

    [Spinlock Protocol: ip6_fl_lock]
    Protected objects:
      - The global flow-label hash and its global/per-netns membership counters.
    Rules:
      - All hash updates and counter accesses hold ip6_fl_lock.
      - Admission checking and insertion share one critical section.
      - Process paths use spin_lock_bh(); the GC timer uses spin_lock().

    [Locking Logic: Serialized Admission and Insertion]
    Pre-condition:
      - The candidate is unpublished and ip6_fl_lock is not held.
    System algorithm:
      1. Enter an RCU read-side section and acquire ip6_fl_lock.
      2. Check admission and, if admitted, recheck for a duplicate;
         reuse it or publish the candidate and update both counters.
      3. Release ip6_fl_lock and leave the RCU read-side section.
    Post-condition:
      - Admission and insertion are atomic with respect to other writers.
      - Hash membership and its counters remain consistent.
      - ip6_fl_lock and the RCU read-side section are not held.

        Figure 7: Concurrency specification for serialized admission and insertion in ipv6_flowlabel_get.


4.1.4   Task-Bounding Plan
Within S YS S PEC* , the Specification defines the semantic change, whereas the task-bounding Plan governs the develop-
ment cycle used to realize it. It structures this task-level guidance into three components: goals and non-goals, scope,
and success criteria.
Goals and non-goals. Goals state the functional, performance, compatibility, or maintenance outcomes that the task
must achieve. Non-goals identify adjacent behavior that is outside the task and existing properties that must remain
unchanged. Making both explicit distinguishes a deliberate omission from a missed requirement and prevents an agent
from introducing unrelated refactoring or optimizations while pursuing a locally reasonable implementation.
Scope. Scope identifies the portions of the system that the task may change, such as subsystems, modules, files, symbols,
or configuration, together with permitted new modules and dependencies and boundaries that must remain stable. For a
cross-module task, the scope can include components whose contracts must change to satisfy the task, as exposed by
their rely-guarantee relationships. Scope therefore limits implementation freedom without requiring the developer to
specify every source-code edit in advance.
Success criteria. Success criteria turn the goals into observable conditions under which the task is considered complete.
They may require a behavior or performance property, satisfaction of the relevant specification contracts, preservation
of non-goals, and specific build, boot, test, or review outcomes. The Plan records these required outcomes; §4.2 and
§4.3 describe how OSF OUNDRY obtains the corresponding review and execution evidence.
    The example in Fig.8 bounds the IPv6 flow-label task to per-network-namespace admission and accounting, while
preserving the existing flow-label interfaces and unrelated networking behavior.
    S YS S PEC* evolves as grilling reveals missing requirements and system analysis exposes implicit constraints. Its
Plan captures the boundary of the current task, while its Specification captures the task-relevant semantics that the
implementation must establish or preserve. Completing a task updates the affected components of S YS S PEC* and the
corresponding implementation, while specifications unrelated to the task remain unchanged.
      TASK-BOUNDING PLAN

      [GOALS]
        - Prevent one unprivileged network namespace from exhausting the shared
          flow-label pool and starving other namespaces.
        - Keep admission and global/per-netns accounting exact under concurrency.

      [NON-GOALS]
        - Do not change the flow-label UAPI, proc output, sharing modes,
          routing, or transport behavior.
        - Do not add a sysctl, netlink API, or hardware dependency.

      [SCOPE]
        - net/ipv6/ip6_flowlabel.c: admission, insertion, and accounting.
        - include/net/netns/ipv6.h: per-netns flow-label count.

      [SUCCESS CRITERIA]
        1. One unprivileged netns cannot exceed its per-netns budget.
        2. Insertion and removal update both counters exactly once; reuse does not.
        3. Admission and insertion execute in one critical section.
        4. Existing flow-label behavior and selftests remain compatible.

Figure 8: Simplified task-bounding Plan for enforcing an unprivileged per-network-namespace budget in the IPv6
flow-label manager.


4.2     OSF OUNDRY Agents
As shown in Fig.4(b), OSF OUNDRY organizes OS development around four specialized agents: a specification agent,
an implementation agent, a review agent, and a refinement agent. These agents form three stages that progressively turn
an incomplete request into an implementation and keep it aligned with evolving requirements and system constraints. In
the specification stage, the specification agent grounds developer intent in the existing system and constructs S YS S PEC*
by producing its Plan and Specification. In the implementation stage, the implementation agent modifies code within
the Plan’s scope and verifies the result against the Specification and success criteria. In the refinement stage, the review
agent independently examines the implementation, after which the refinement agent incorporates the review report
and developer feedback into a revised blueprint for the next implementation iteration. All four agents can draw on the
shared OSKB, while the implementation agent invokes the OS Environment to obtain build and execution evidence;
§4.3 describes these facilities in detail.

4.2.1    Specification Agent
The specification agent helps the developer turn an incomplete natural-language intent into S YS S PEC* by constructing
a Plan and Specification that are sufficiently precise to guide implementation and review. Because the initial request
rarely contains every task boundary or system constraint, the agent constructs these components through an interactive
analysis–grilling loop rather than a single translation step.
Analysis–grilling loop. The agent first analyzes the intent together with the relevant code and existing artifacts. This
analysis locates affected components, recovers implicit contracts, and identifies missing or conflicting information that
would make the intended change ambiguous. The agent then grills the developer with focused questions about the
unresolved requirements and design choices. Each answer enriches the task context and triggers another round of code
analysis, which may expose further dependencies or ambiguities. The loop continues until the developer and agent
reach a shared interpretation of the intended behavior, task boundary, and relevant system constraints.
Artifact construction. From this progressively refined context, the agent authors S YS S PEC* by producing its task-
bounding Plan and corresponding Specification. For an existing implementation, it can extract relevant behavior
and contracts from code before introducing the requested changes; for a new component, it constructs the required
contracts from the agreed design and surrounding system context. Before handing the blueprint to the implementation
agent, it checks its components for omissions, contradictions, and unresolved references between the Plan and affected
specifications.
4.2.2   Implementation Agent
The implementation agent realizes the Specification as code within the constraints established by the Plan through
an implement–verify loop. This loop keeps code generation or modification within the task boundary and prevents a
plausible implementation from advancing before it has been checked against the shared blueprint.
Implementation. The Plan’s scope determines which subsystems, modules, files, symbols, and dependencies the agent
may change. Within this boundary, the goals and non-goals constrain the intended effect of the modification, while
the Specification governs its functional behavior, module composition, and concurrency semantics. The agent uses
these constraints to create a new implementation or revise the existing code without extending the change beyond the
permitted scope.
Verification. After each implementation attempt, the agent verifies that the code conforms to the relevant functionality,
modularity, and concurrency specifications. It then evaluates the Plan’s success criteria using the required observable
checks and evidence from the OS Environment. A specification mismatch or unmet success criterion produces feedback
for the next implementation attempt. The implement–verify loop continues until the implementation conforms to the
Specification and all applicable Plan success criteria are satisfied, after which the result is submitted to the review agent.

4.2.3   Review Agent
The review agent independently examines an implementation that has completed the implement–verify loop. Separating
review from implementation provides a fresh evaluation of both conventional code quality and OS-specific risks that
may not be covered by the task’s explicit checks.
General review. General review identifies defects that do not require specialized OS knowledge, such as incorrect error
handling, resource leaks, unsafe boundary conditions, and unnecessary changes outside the intended implementation
logic. It also checks whether the implementation remains understandable and consistent with the surrounding codebase.
OS-specific review. OS-specific review grounds the analysis in domain knowledge retrieved from the OSKB. We
port Linux-derived review prompts into the OSKB to encode reusable review knowledge for kernel concerns such
as synchronization, resource lifetime, user–kernel boundaries, and hardware interaction. The review agent selects
knowledge relevant to the affected subsystem and uses it to inspect risks that are easy to miss in general code review.
The construction and integration of these review prompts are described with the OSKB in §4.3.2.
Review report. The agent produces a structured report that records each finding, its code location, the relevant OS rule
or artifact, and a suggested refinement direction. It does not directly modify the code or S YS S PEC* ; the report becomes
an input to the refinement agent.

4.2.4   Refinement Agent
The refinement agent updates S YS S PEC* by combining the review agent’s report with developer feedback. Its role is
limited to refining this blueprint: it does not directly patch the implementation.
Artifact refinement. Developer feedback may revise the task’s goals, non-goals, scope, or success criteria, while review
findings may reveal system semantics that should be clarified or strengthened in the Specification. The agent incorporates
both sources into an incremental update of the affected artifacts and leaves unrelated specifications unchanged. The
refined S YS S PEC* is then returned to the implementation agent, whose implement–verify loop brings the code into
alignment with the revised blueprint.

4.3     OS Environment and Knowledge Base
S YS S PEC* and specialized agents provide explicit development constraints, but they do not by themselves ground
decisions in system execution or supply all of the domain knowledge needed for OS development. OSF OUNDRY
addresses these two gaps with shared infrastructure: the OS Environment validates implementations through actual build
and execution, while the OS knowledge base (OSKB) supplies reusable, task-relevant knowledge to all four agents.

4.3.1   OS Environment
The OS Environment is an executable interface through which the implementation agent can build, boot, test, and
debug a candidate OS implementation. This execution boundary is essential because a module that appears correct in
isolation may fail only when linked with the full kernel, exercised across user–kernel boundaries, or run with concurrent
and hardware-facing components. Textual reasoning and specification conformance are therefore complemented by
validation of the complete executable system.
Environment-backed end-to-end validation. The environment exposes a uniform set of operations for building the
kernel, user runtime, and system image; booting the target OS in QEMU; running tests or workloads; and collecting
console logs or GDB diagnostics when execution fails. During the verification step, the implementation agent submits
its current implementation to this environment, which builds and boots the complete target before executing the checks
associated with the Plan’s success criteria. This process validates integration and runtime behavior rather than stopping
at compilation or an isolated module test. The OS Environment does not decide the intended behavior or prove
conformance to the Specification; it executes observable checks and returns runtime evidence that the implementation
agent combines with its specification-level analysis.
Compact execution feedback. Build, test, and debugging workflows can produce output far larger than an agent’s
context window. The OS Environment therefore returns a compact summary of the validation stage, pass/fail results,
and relevant log or debugging evidence, while retaining complete raw output outside the agent context. This summary
provides enough information for the next implementation attempt without repeatedly consuming context with unrelated
execution output.

4.3.2   OS Knowledge Base
The OSKB is a shared collection of reusable OS knowledge that supplies task-relevant context to all four agents. Such
knowledge is distributed across kernel code, subsystem documentation, review practices, and platform manuals, and
cannot be placed in every agent context in full. Centralizing it in the OSKB avoids requiring each agent to recover the
same rules independently and helps maintain a consistent interpretation across the development workflow.
Knowledge collection. We collect knowledge from kernel subsystem and API documentation, ISA and ABI specifi-
cations, hardware device and memory-model documentation, repository-specific coding and testing conventions, and
project-maintained design constraints. In particular, we port Linux-derived review prompts [9] into the OSKB and
organize them by subsystem and kernel concern, including synchronization, resource lifetime, user–kernel boundaries,
and hardware interaction. Collected knowledge retains its source and applicable subsystem, architecture, or concern so
that agents can select rules appropriate to the current target.
Agent integration. Agents retrieve OSKB knowledge using their role together with the relevant S YS S PEC* context
and the affected code. Only the task-relevant subset is added to an agent’s context. The specification agent uses this
knowledge to identify implicit constraints and formulate grilling questions; the implementation agent uses it to follow
relevant APIs, platform rules, and repository conventions; the review agent uses Linux-derived prompts for OS-specific
review; and the refinement agent uses the applicable rules to interpret findings and update S YS S PEC* .

4.4     Usage and Deployment of OSF OUNDRY
OSF OUNDRY supports two complementary forms of use. A developer can invoke any agent independently through
a Rust command-line interface (CLI) and incorporate its output into an existing development workflow, or use an
Orchestrator to execute the complete specification, implementation, review, and refinement process.
    The same interfaces support the two development settings demonstrated in our case studies. For S PEC OS, OS-
F OUNDRY manages the artifacts and executable environment needed to construct and iteratively refine a complete OS.
For Linux kernel development, it operates on an existing repository under the corresponding task-scoped S YS S PEC* ,
allowing the workflow to remain focused on the intended kernel change.
Agent skills and Rust CLI. Each of the four agents is implemented as an independently callable skill that packages its
role-specific instructions and tools. We integrate these skills into a standalone Rust CLI that serves as the local runtime
of OSF OUNDRY. The CLI includes the OSKB and all agent skills, manages the kernel project’s working directory,
and persists the artifacts produced throughout a task, including S YS S PEC* , verification and review reports, and other
intermediate files. A user can invoke an individual skill through the CLI, while every invocation operates on the same
managed workspace and artifact state.
Orchestrated workflow. The Orchestrator is a workflow controller rather than a fifth reasoning agent. It uses the Rust
CLI to invoke the specification, implementation, review, and refinement skills in sequence and passes the managed
artifacts between them. During specification, the Orchestrator pauses when the specification agent needs to grill the
developer for missing information. During refinement, it presents the review report, collects developer feedback, and
invokes the refinement agent to update S YS S PEC* . Implementation, verification, and review can proceed automatically
between these interaction points, and the refined S YS S PEC* is returned to the implementation agent for the next iteration.
Containerized deployment. We deploy OSF OUNDRY in a container that includes the Rust CLI, the Orchestrator, and
the kernel development and validation toolchain. Within the container, the CLI manages the OSKB, agent skills, kernel
working directory, and task artifacts, while compilers, build tools, tests, QEMU, and GDB support executable validation.
The entire agent-driven kernel development workflow runs inside this environment. Containerization therefore provides
a reproducible and isolated execution boundary for both agent operation and kernel validation.

5     Evaluation
We evaluate whether OSF OUNDRY can effectively support OS development in two complementary settings: constructing
and evolving a new operating system, and implementing scoped changes in an existing production kernel. The former
requires OSF OUNDRY to maintain consistent semantics across a complete OS stack, whereas the latter requires it to
recover and preserve the implicit constraints of a large, mature codebase. Together, these settings allow us to evaluate
both the system-wide and task-level effectiveness of OSF OUNDRY.
    Our evaluation addresses the following research questions:
• RQ1: Full-system construction. Can OSF OUNDRY construct a complete, bootable operating system whose generated
  modules conform to their specifications and satisfy the system’s functional requirements?
• RQ2: Controlled system evolution. Can OSF OUNDRY evolve an operating system through localized specification
  patches, including both cross-layer functionality and semantics-preserving performance optimizations?
• RQ3: Existing-kernel development. Can OSF OUNDRY complete representative Linux kernel development tasks
  more accurately than a general-purpose coding agent?
    We answer these questions through two case studies. First, we use OSF OUNDRY to construct S PEC OS, a
specification-guided reimplementation of xv6 [10] consisting of 259 modules across the complete kernel and user-space
stack. We evaluate its construction through module-level generation accuracy, whole-system boot and functional tests,
and comparisons with natural-language and oracle-context baselines across models of different capabilities. We then
evaluate its evolvability by extending the text-only system with a GUI stack and applying three performance optimiza-
tions through specification patches. This case study answers RQ1 and RQ2 by examining whether OSF OUNDRY can
both produce a complete OS and evolve it without rewriting unrelated parts of the system.
    Second, we apply OSF OUNDRY to eleven representative development tasks drawn from the Linux kernel. Unlike
S PEC OS, these tasks begin with an existing implementation whose relevant semantics, subsystem conventions, and
compatibility constraints must be recovered from the codebase. We evaluate whether the resulting patches correctly
satisfy the task requirements and compare their development accuracy with those of a general-purpose coding agent.
This case study answers RQ3 and complements the full-system experiment by testing OSF OUNDRY in a mature kernel
where changes must remain scoped and coexist with substantial existing functionality.

5.1     Case Study: Constructing and Evolving S PEC OS
5.1.1   Building S PEC OS with OSF OUNDRY
Overview. We use xv6-riscv as the basis for S PEC OS, target its native RISC-V architecture, and run the generated
system in QEMU. Even at its modest scale, xv6 offers a sufficiently rich cross-subsystem setting for this case study.
    As shown in Fig. 9, S PEC OS is organized into 11 logical components and 259 modules spanning memory man-
agement, process management, system calls, the file system, device drivers, kernel and user libraries, and low-level
RISC-V routines. The case-study artifact contains approximately 8K lines of S YS S PEC* and 13K lines of generated C
code. We use C so that the generated implementation can be integrated directly with the xv6 build and compared with
conventional low-level kernel code.
    The construction stage receives the complete S PEC OS S YS S PEC* as a fixed input. To isolate implementation
from the other stages of OSF OUNDRY, we enable only the implementation agent and use its implement-verify loop to
construct the system.
Preparing the development blueprint. Before construction, the specification agent translates the original xv6 imple-
mentation into an initial full-system S YS S PEC* comprising a Plan and Specification. A developer participates in the
                                                                      SpecOS
                                 User       user lib        win service           apps    shell, player, game, …


                                                                             syscall

                                           Core                      FS                    Driver
                                            ipc        vm            vfs       bio          uart      plic      mouse
                                Kernel
                                           sync    sched             log       file         gpio      virtio_disk

                                           proc                      inode                  audio      keyboard



                                 Arch             riscv        csr    mem layout         trap       bootstrap



Figure 9: S PEC OS architecture. S PEC OS comprises a kernel and a user-space stack organized into 11 logical
components and 259 specification-governed modules.

grilling process to resolve underspecified behavior and design choices, and then inspects the resulting Specification to
confirm that it captures the intended semantics. The finalized S YS S PEC* is fixed before implementation begins.
    Rather than treating xv6 as a monolithic generation target, the Specification within the resulting S YS S PEC*
decomposes it into composable modules. Each module records its pre- and post-conditions, invariants, rely/guarantee
contracts, algorithmic description, and concurrency requirements. These specifications expose the contracts needed to
implement a module while preserving its relationships with the rest of the system.
Generating the implementation. The implementation agent consumes the complete S PEC OS S YS S PEC* and applies
an implement-verify loop. In each iteration, it produces a candidate C implementation and verifies the candidate
against the corresponding specification. A failed verification returns feedback to the next implementation attempt; a
module advances only after satisfying the verification step. Applying this loop across all 259 modules produces the
implementation that we integrate and evaluate as S PEC OS.

5.1.2   Functional Correctness and Generation Accuracy
End-to-end functional correctness. We first evaluate whether the generated modules compose into a working operating
system. The resulting S PEC OS boots on QEMU, runs the standard xv6 user-space environment, and passes all 70
registered test cases in the functional test suite of xv6. These tests exercise the integrated kernel through its user-visible
interfaces and show that OSF OUNDRY can generate a complete, executable system. They provide end-to-end functional
evidence rather than a proof of correctness beyond the tested behaviors.
Module-level accuracy. We separately evaluate whether each generated module preserves the semantics of its corre-
sponding ground-truth implementation. The evaluation covers all 259 modules in S PEC OS. We use GPT-5.4 as an LLM
judge to compare each generated module with its ground truth. A module is counted as correct only when the judge
determines that the two implementations are semantically and logically equivalent; any omitted behavior, inconsistent
state transition, or incorrect implementation logic is counted as a failure. We report accuracy as the fraction of the 259
modules judged correct.
    We compare the Specification component of S YS S PEC* with two baselines:
• Normal. The prompt provides a natural-language description of the module logic together with the signatures and
  type definitions of the dependency APIs it may require.

• Oracle. In addition to the Normal input, the prompt provides the complete ground-truth source code of the dependency
  modules.
• Specification from S YS S PEC* (our approach). The prompt uses the structured module specification, including
  behavioral contracts, state transitions, and inter-module dependencies.

We run all three methods with Qwen3.6-Plus, GPT-5.4, and Qwen3.6-35B-A3B to cover models with different
capabilities.
Accuracy results. As shown in Fig. 10, the Specification consistently improves module-level accuracy across all
three models. With Qwen3.6-Plus and GPT-5.4, it achieves 100% accuracy: all 259 generated modules are judged
                                                           Normal     Oracle    SysSpec*
                                                    100




                                     Accuracy (%)
                                                    80

                                                    60

                                                    40

                                                    20

                                                     0
                                                      Qwen3.6-Plus   GPT-5.4 Qwen3.6-35B-A3B
                                                                     Model
                             Figure 10: Module-level generation accuracy for S PEC OS.

semantically equivalent to their ground-truth implementations. Both the Normal and Oracle baselines remain less
reliable, indicating that natural-language requirements and additional dependency source code do not provide the same
effective constraints as the structured specification.
    The improvement remains substantial with the smaller Qwen3.6-35B-A3B model, for which the Specification
achieves 90.3% accuracy and outperforms both baselines. It also exceeds the Oracle results obtained with stronger
models. These results suggest that explicit behavioral and inter-module constraints can compensate in part for lower
model capability. Together with the successful boot and functional tests, the module-level results provide complementary
evidence that OSF OUNDRY can generate both individually conforming modules and a complete working operating
system.

5.1.3   Evolving S PEC OS with OSF OUNDRY
Overview. We next evaluate whether OSF OUNDRY can evolve a working OS from a user-level intent. Starting from
the request to turn the text-only S PEC OS into a GUI-capable system, the developer and the specification agent jointly
produce the final S YS S PEC* , including its Plan and relevant Specification content, through an iterative analysis–grilling
loop that combines code analysis with focused questions about requirements and design choices. OSF OUNDRY then
generates and verifies the implementation and incorporates review findings through refinement. This task crosses device
drivers, memory management, system calls, user-space services, libraries, and applications. We organize the evolution
into three consecutive phases: kernel support, a user-space window service, and application adoption. We validate the
result by running graphical applications and the existing xv6 functional tests.
Phase I: Kernel support. The original S PEC OS provides only a text console. The first phase adds a virtio-gpu driver
with a scanout-capable frame buffer and a graphics ABI for querying display geometry and submitting full-screen
or partial updates. To prevent applications from competing for the display, the kernel grants presentation authority
to the window service; the kernel controls the device, while the service determines composition policy. We also add
shared-memory IPC so that clients can exchange frame buffers with the service without repeatedly transferring pixel
data through byte-oriented pipes. The shared-memory subsystem tracks mappings per process and cleans them up on
exec() and exit(). Finally, event-oriented keyboard input allows the kernel to capture key events for subsequent
delivery to the focused application.
Phase II: Window service. The second phase introduces a window protocol, a user-space compositor, and a client
library. The protocol defines commands, events, and shared-memory buffers exchanged between clients and the service.
Each window uses double buffering: a client renders into a back buffer and commits it, after which the compositor
presents the new buffer and releases the previous one. This avoids concurrent modification of a buffer being composed.
Started by init, the compositor maintains window state and z-order, presents the composed frame through the graphics
ABI, and routes input to the focused client. The client library exposes this service through a simple window API, hiding
the underlying protocol and shared-memory details.
Phase III: Application adoption. The final phase adds an SDL compatibility layer over the client library. The
SDL compatibility layer maps SDL surface updates and input events to the window protocol, allowing existing SDL
applications to be ported to S PEC OS with only minor source-level changes. To validate GUI functionality from
complementary perspectives, we select a representative set of applications with different interaction patterns. Some of
these applications are adapted from the Navy-apps suite [35]. Collectively, they cover the end-to-end rendering path
from application buffers through shared-memory transport and composition to GPU display, together with the input
path from the kernel to the focused client. The game repeatedly renders frames and responds to input; the launcher
                      (a) Game                  (b) Launcher                              (c) Multi-window                                   (d) Terminal
Figure 11: End-to-end GUI applications running on the evolved S PEC OS. The screenshots show a game, the
window-service launcher, multiple concurrent windows, and a graphical terminal.
                                                                           2400                                                  3000
Throughput (ops/ms)




                      600




                                                                                                             Throughput (B/ms)
                                Baseline
                                Optimized                                  1800
                      450
                                                               Time (ms)
                                                                                                                                 2000

                      300                                                  1200
                                                                                                                                 1000
                      150                                                   600

                        0                                                     0                                                     0
                            1               2        4                            2   4      8     16   32                              64       256        1024   4096
                                          Parent Process Memory (MB)
                                        CPUs                                 Read/Write Chunk Size (B)
Figure 12: Performance improvements from OSF OUNDRY-generated S PEC OS optimizations. Left: the per-CPU
page allocator reduces global allocator contention as concurrency increases. Middle: copy-on-write fork avoids eager
page copying in fork-exec workloads. Right: batched pipe I/O reduces pipe transfer overhead, especially for larger
block sizes.

creates windows and starts applications; the multi-window workload presents concurrent windows under changing
focus; and the graphical terminal accepts keyboard input, renders text, and executes commands.
Validation. The evolved system boots into the GUI environment and runs the game, launcher, multi-window workload,
and graphical terminal shown in Fig.11. Their execution validates display output, shared-memory transport, composition,
and input delivery across the new stack. The system also continues to pass the complete xv6 functional test suite,
providing regression evidence that the evolution preserves the existing behaviors covered by those tests.

5.1.4                       Performance Evaluation
We further evaluate whether OSF OUNDRY can translate performance intents into effective system optimizations. We
provide separate intents for a per-CPU page allocator, copy-on-write (COW) fork, and batched pipe I/O. For each
intent, OSF OUNDRY updates the Plan and relevant parts of the Specification within S YS S PEC* , generates and verifies
the affected implementation, and incorporates review feedback. We compare each generated variant with the original
generated S PEC OS under the same QEMU environment. The optimizations change internal data structures or algorithms
while retaining their user-visible interfaces, and all three variants continue to pass the xv6 functional test suite.
Per-CPU page allocator. The baseline allocator maintains one free list protected by a global spinlock, so every kalloc
and kfree operation accesses shared state. The generated optimization gives each CPU a local free list and serves
common allocations and frees from that list. Local lists exchange pages with a global reserve only when they require
a refill or drain, and batched allocation/free interfaces amortize the remaining allocator operations. Our benchmark
repeatedly allocates and frees user memory under 1, 2, and 4 CPUs. The benefit grows with concurrency, reaching a
19.2% improvement at 4 CPUs; under 2 and 4 CPUs, the measured spin count on the global kmem lock falls to zero per
1,000 operations. Because the optimization introduces both local lists and batching, the result reflects their combined
effect and is consistent with moving the common allocation path away from the global lock.
Copy-on-write fork. The baseline fork() allocates and copies every user page before the child begins execution.
The generated COW implementation instead lets the parent and child share physical pages, marks their mappings as
copy-on-write, and maintains per-page reference counts. A private copy is allocated only when either process writes to
a shared page, preserving the independent-address-space semantics of fork() while deferring copying. Our fork-exec
workload allocates and touches a parent address space before repeatedly forking children that immediately execute a
new program. This workload exposes pages that eager fork copies but the child discards at exec. Across address-space
sizes from 2 MB to 32 MB, COW avoids these copies and achieves a 3.12× to 4.41× speedup over the baseline.
                                Table 3: Linux kernel bug-fix task suite and outcomes.

Task                                       Subsystem               Core issue             Files   Codex     OSF OUNDRY
IPv6 flow-label limits                     Networking              Lock synchronization     2       ✓            ✓
ext4 fast-commit wakeup                    Filesystems             Wakeup liveness          2       ✓            ✓
hugetlb poison deadlock                    Memory management       Deadlock avoidance       4       ✓            ✓
SELinux audit cache                        Security                Audit consistency        2       ✓            ✓
ESP shared fragments                       Networking              Fragment marking         4       ✓            ✓
eprobe error offset                        Tracing                 Diagnostic location      1       ✗            ✓
request-key concurrent revoke              Security                Object lifetime          4       ✗            ✓
lockd NLM file leak                        Filesystems             Resource cleanup         3       ✗            ✓
fanotify permission events                 Filesystems             Permission isolation     3       ✗            ✓
IPVS resize livelock                       Networking              Concurrent liveness      2       ✗            ✗
NTFS validation                            Filesystems             Metadata validation      4       ✗            ✗


Batched pipe I/O. The baseline pipe path invokes copyin or copyout separately for each byte, making large transfers
pay repeated user–kernel copy overhead. The generated implementation computes a contiguous chunk from the
requested length, available pipe space or data, and ring-buffer boundary, and transfers that chunk with one copy
operation. It retains the pipe’s synchronization and user-visible read/write semantics while changing the granularity of
data movement. We measure transfer time between a writer and reader while varying the user-level block size from
64 to 4,096 bytes. Batching improves performance at every tested size, with larger blocks benefiting more from the
reduced number of copy calls. At 4096 bytes, it reaches a 2.74× speedup and reduces transfer time by 63.5%.
    Together, these experiments show that OSF OUNDRY can realize performance intents that require changes to data
structures and internal algorithms, while the regression results preserve the existing behaviors covered by the xv6 test
suite.

5.2     Case Study: Linux Kernel Development
5.2.1   Evaluation Setup
Tasks. We select eleven bug-fix tasks from Linux kernel commits merged during the three months preceding our
evaluation. All selected commits postdate the release of the evaluated model, reducing the likelihood that their fixes
appeared in its training data. The tasks span networking, file systems, memory management, security, and tracing,
addressing systems concerns ranging from synchronization to resource isolation and validation. The task suite ranges
from single-file fixes to substantial changes spanning multiple files. Tab.3 summarizes the task suite and outcomes.
Compared approaches. For each task, both conditions start from the same base commit and receive the same task.md,
which specifies the goal, required behavior, and correctness criteria. Both run in the isolated os-env described in §4.3.1
and use GPT-5.5, configured with high reasoning effort, as the LLM backbone. We use the general-purpose Codex
coding agent as the baseline. The baseline operates directly on the task, whereas, for this evaluation, OSF OUNDRY
generates S YS S PEC* directly from task.md in a single pass, without the analysis–grilling loop, and then coordinates
implementation, verification, review, and refinement. No human feedback is introduced during patch generation; instead,
the original task.md is supplied as a fixed feedback source during refinement alongside the review report. Thus, the
development harness is the primary difference between the two conditions.
Success criterion. We validate a candidate with its task-specific test when one is available; otherwise, an LLM judge
compares the candidate and ground-truth patches under the behavioral requirements in task.md. The judge rejects
omitted behavior, semantic deviations, and changes outside the required behavior. We count a task as successful only
when its corresponding validator accepts the candidate.

5.2.2   Lessons from Representative Cases
Three representative tasks in which the baseline fails but OSF OUNDRY succeeds illustrate complementary benefits of
explicit task constraints, independent review, and OS-specific knowledge.
S YS S PEC* prevents implementation drift. The eprobe task requires the parser to preserve the error offset already
computed for a missing attached-event field; the existing error class and all other parser behavior must remain unchanged.
The baseline locates the offset reset but also assigns a new error code, turning a location fix into an unsupported semantic
change. In contrast, within the OSF OUNDRY S YS S PEC* , the Plan records preservation of the error class as a non-goal,
while the Specification requires the existing failure path to retain the computed offset. By following these S YS S PEC*
constraints, the implementation agent checks that the neighboring parser branches remain unchanged and produces a
patch that removes only the offset reset. The judge therefore accepts the OSF OUNDRY patch and rejects the baseline
patch for changing behavior outside the task.
Independent review provides actionable guidance. The request-key task must keep an authorization payload alive
while instantiate and reject operations may sleep concurrently with revoke or destroy. The baseline implements the core
reference-counting design but misses a key condition on the repeated-revoke path, failing to account for the case in
which the authorization payload has already been cleared. The initial OSF OUNDRY implementation also misses this
repeated-revoke condition. The review agent then independently performs a path-complete check of the authorization-
record lifecycle: revoke must detach the payload before releasing its owner reference, and every instantiate/reject exit
path must release the pinned reference exactly once. This review exposes the lifecycle condition missed by the initial
OSF OUNDRY implementation. The refined patch correctly implements these conditions on all relevant paths and passes
the judge. Although independent review does not guarantee correctness, it provides a separate opportunity to detect
overlooked constraints and turn them into concrete refinement guidance.
OSKB captures OS-specific semantics and concerns. The fanotify task requires permission-event preparation to
preserve mark lifetime and group isolation while the fsnotify_mark_srcu read-side protection is temporarily released
for a user-space wait. The baseline incorrectly aborts the current permission event on a stale mark from an unrelated
group instead of skipping it under SRCU. OSKB provides task-relevant rules for SRCU-protected mark traversal,
reference lifetime, and concurrency semantics. Guided by these rules, OSF OUNDRY skips such marks, still fails when a
current-group mark cannot be retained, and balances references across the wait. The resulting patch correctly handles
the relevant paths and passes the judge.

5.2.3   Failure Analysis
We next analyze the two tasks that neither the baseline nor OSF OUNDRY completes to identify current boundaries of
OSF OUNDRY.
IPVS resize livelock. The IPVS task requires table resizing to complete while updates and readers continue to access
the service table. The ground-truth design uses svc_replace_sem to coordinate table replacement, ensuring consistent
publication and RCU-safe reclamation of the old table. OSF OUNDRY recognizes the local risk that a blocking table
walker may repeatedly restart. However, it does not infer that resizing and concurrent updates must be coordinated as one
table-replacement operation. Its S YS S PEC* therefore permits a design based on svc_resize_sem and service_mutex.
These locks serialize selected paths, but they do not ensure that the new table is published consistently or that the old
table remains alive until readers finish. The Plan states the correct liveness goal, but the Specification fails to specify the
synchronization protocol required to achieve it. This case illustrates a limitation of OSF OUNDRY: when a task leaves
important semantics implicit, especially in its concurrency logic, OSF OUNDRY may fail to derive a correct S YS S PEC* ,
leaving subsequent agents unable to complete the task correctly.
NTFS metadata validation. The NTFS task requires rejecting attribute-list entries whose name_offset does not
immediately follow the fixed entry header. Thus, name_offset must equal sizeof(struct attr_list_entry),
rather than merely fall within the record. OSF OUNDRY derives the record-boundary check but does not recover the
stricter layout invariant relating the on-disk offset to the fixed header. The resulting implementation therefore prevents
out-of-bounds access but accepts offsets that remain within the record while pointing to the wrong location, so the
parser may read the attribute name from an invalid position. This case illustrates a limitation of OSF OUNDRY: it
currently cannot reliably infer domain invariants that are implicit and distributed across data representations and their
consumers.

6   Related Work
General software engineering and coding agents. Advances in LLMs have led to a growing number of general-purpose
coding agents, such as Codex [37], Claude Code [3], Pi-agent [39], and Kimi Code [21], that assist software engineering
by navigating repositories, editing source code, invoking build and test tools, and iterating on the resulting feedback.
    Alongside the development of these general-purpose agents, substantial research has explored how to improve
their capabilities and use them more effectively in software engineering. AutoCodeRover [53], CodeAgent [52], and
RepairAgent [4] use structured repository search, tool integration, and iterative validation for issue resolution, repository-
level generation, and program repair. Agentless [47], by contrast, shows that a fixed localization–repair–validation
pipeline can remain competitive without autonomous tool use or action planning.
    Benchmarking has evolved in parallel from isolated coding tasks toward long-horizon software engineering, ranging
from resolving real-world repository issues to constructing complete systems from scratch. Benchmarks such as
SWE-bench Pro [12], ProgramBench [51], and DeepSWE [19] evaluate agents across this broader spectrum of complex,
multi-step development tasks. Together, these systems and benchmarks demonstrate that coding agents are moving
beyond local code completion toward sustained software engineering, although their semantic context is still primarily
derived from natural-language task descriptions and existing repositories.
    Another line of work investigates specification-driven workflows [40] for general-purpose software development.
Spec Kit [16] and Kiro [2] maintain requirements, specifications, plans, and implementation tasks as persistent artifacts
throughout the development process. Because these approaches are designed for general software engineering, they
do not prescribe how domain-specific OS semantics should be represented and maintained across development stages.
OSF OUNDRY specializes this workflow for systems software by making S YS S PEC* , with its Plan and OS-specific
Specification, a shared artifact across specification, implementation, review, and refinement.
LLM-assisted systems software development. Recent work has begun to characterize the capabilities required for
LLM-assisted systems engineering. SEC-bench Pro [23] evaluates long-horizon vulnerability reproduction in browser
engines and the Linux kernel, while the system-intelligence proposal [15] emphasizes reasoning about architectures,
protocols, abstractions, and design tradeoffs beyond code generation and repair. These efforts define and evaluate
systems capabilities rather than provide an end-to-end development workflow.
    Most existing systems-oriented approaches apply LLMs to a specific development activity. For reliability, WASABI [42]
combines LLM-based analysis with static and dynamic techniques to detect retry bugs, while KernelGPT [49] synthe-
sizes and iteratively validates syscall specifications for kernel fuzzing. For Linux-kernel debugging, kAgent [33] uses
crash logs and reproduction feedback to generate and refine patches, Code Researcher [41] retrieves relevant context
from source code and commit history, and LinuxFL+ [55] improves fault localization.
    Performance-oriented work is similarly specialized. SysGPT [38] provides optimization suggestions grounded in a
taxonomy of serial optimization strategies, while gigiprofiler [18] combines LLM-based semantic inference with static
and runtime analysis to diagnose application-defined resource bottlenecks.
    Other performance-oriented systems directly optimize implementations. ECO [27] automatically localizes, generates,
and validates efficiency patches in production code, while CUDA Agent [11] uses agentic reinforcement learning and
execution feedback to optimize GPU kernels. QiMeng-GEMM [54] uses architecture-aware prompt search to generate
GEMM implementations, while QiMeng-Xpiler [13] combines LLM transformations, symbolic repair, and auto-tuning
for cross-platform tensor programs. Together, these approaches support performance analysis and feedback-driven
code optimization, but target individual patches, kernels, operators, or transformations rather than the construction and
evolution of a complete system.
    Work at a broader scope explores the agentic construction of complete systems software. SpecFS [30] uses
structured specifications to guide the construction and evolution of a concurrent file system, while SpecDB [31]
generates customized database systems through feature-oriented decomposition. VibeServe [20] uses nested agent
loops to generate LLM serving stacks specialized to a target model, hardware platform, and workload. OSF OUNDRY
extends SpecFS to full-OS construction and scoped kernel evolution, while keeping specifications synchronized with
code through implementation, execution, and review feedback.
Formal methods and LLM-assisted verification. Formal methods have long been used to construct and verify complex
systems. seL4 [22], CertiKOS [17], and Hyperkernel [34] demonstrate machine-checked verification of operating-
system kernels. Related work verifies file systems such as FSCQ [7], AtomFS [56], and RefFS [57], as well as liveness
properties of cloud controllers such as Anvil [44]. These systems provide substantially stronger guarantees than testing
or informal review, but require carefully designed formal models, specifications, and proofs that are expensive to
construct and maintain.
    Recent work uses LLMs to reduce the effort required to construct formal specifications and proofs. OSVBench [25]
evaluates the generation of complete state-transition specifications for Hyperkernel, while SpecGen [32] generates and
verifier-checks formal specifications for Java programs. AutoVerus [48] and SAFE [8] generate correctness proofs for
Rust through verifier-guided refinement or self-evolution, whereas AlphaVerus [1], Refine4LLM [5], and Clover [43]
integrate formal verification into code generation and refinement. These approaches produce specifications, proofs, or
programs that are checked against formal verification conditions.
    By contrast, OSF OUNDRY does not generate machine-checked proofs or claim formal correctness. Instead, it
borrows the formal-methods discipline of making system behavior and cross-module contracts explicit, while using
compilation, execution, and specification-aware review for lightweight validation.

7   Conclusion
This paper presented OSF OUNDRY, an OS-specialized agent harness that coordinates specification, implementation,
review, and refinement around S YS S PEC* , a shared development blueprint comprising a task-bounding Plan and an
OS-specific Specification. For full-system construction and evolution, OSF OUNDRY generated a complete, bootable
S PEC OS that passes its functional test suite, and subsequently evolved it through specification patches to support a GUI
and multiple performance optimizations. For existing-kernel development, it achieved 1.8× Codex’s accuracy on 11
Linux-kernel bug-fix tasks spanning multiple Linux-kernel subsystems. Together, these results show that explicit and
persistent OS semantics can support both full-system generation and scoped development of existing kernels.

References
 [1] Pranjal Aggarwal, Bryan Parno, and Sean Welleck. Alphaverus: Bootstrapping formally verified code generation
     through self-improving translation and treefinement. In Forty-second International Conference on Machine
     Learning, 2025.
 [2] Amazon Web Services. Kiro: Move beyond ai coding to agentic engineering. https://kiro.dev/, 2026.
 [3] Anthropic. Anthropic claude code application. https://claude.com/product/claude-code, 2026.

 [4] Islem Bouzenia, Premkumar Devanbu, and Michael Pradel. Repairagent: An autonomous, llm-based agent for
     program repair. In 2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE), pages
     2188–2200. IEEE, 2025.
 [5] Yufan Cai, Zhe Hou, David Sanan, Xiaokun Luan, Yun Lin, Jun Sun, and Jin Song Dong. Automated program
     refinement: Guide and verify code large language model with refinement calculus. Proc. ACM Program. Lang.,
     9(POPL), January 2025.

 [6] Haogang Chen, Daniel Ziegler, Tej Chajed, Adam Chlipala, M Frans Kaashoek, and Nickolai Zeldovich. Using
     crash hoare logic for certifying the fscq file system. In Proceedings of the 25th Symposium on Operating Systems
     Principles, pages 18–37. ACM, 2015.
 [7] Haogang Chen, Daniel Ziegler, Tej Chajed, Adam Chlipala, M. Frans Kaashoek, and Nickolai Zeldovich. Using
     crash hoare logic for certifying the FSCQ file system. In 2016 USENIX Annual Technical Conference (USENIX
     ATC 16), Denver, CO, June 2016. USENIX Association.
 [8] Tianyu Chen, Shuai Lu, Shan Lu, Yeyun Gong, Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Hao Yu,
     Nan Duan, Peng Cheng, et al. Automated proof generation for rust code via self-evolution. In International
     Conference on Learning Representations, volume 2025, pages 71891–71918, 2025.

 [9] Chris Mason. Linux kernel review prompts. https://github.com/masoncl/review-prompts, 2026. Refer-
     enced August 2026.
[10] Russ Cox, M. Frans Kaashoek, and Robert Morris. xv6, a simple unix-like teaching operating system, 2011.
[11] Weinan Dai, Hanlin Wu, Qiying Yu, Huan-ang Gao, Jiahao Li, Chengquan Jiang, Weiqiang Lou, Yufan Song,
     Hongli Yu, Jiaze Chen, et al. Cuda agent: Large-scale agentic rl for high-performance cuda kernel generation.
     arXiv preprint arXiv:2602.24286, 2026.
[12] Xiang Deng, Jeff Da, Edwin Pan, Yannis Yiming He, Charles Ide, Kanak Garg, Niklas Lauffer, Andrew Park,
     Chetan Rane, Karmini Sampath, Maya Krishnan, Srivatsa R Kundurthy, Sean M. Hendryx, Zifan Wang, Chen
     Bo Calvin Zhang, Noah Jacobson, Bing Liu, and Brad Kenstler. SWE-bench pro: Can AI agents solve long-horizon
     software engineering tasks? In Forty-third International Conference on Machine Learning, 2026.
[13] Shouyang Dong, Jun Bi, Di Huang, Jiaming Guo, Jianxing Xu, Ruibai Xu, Xinkai Song, Yifan Hao, Ling Li,
     Xuehai Zhou, Tianshi Chen, Qi Guo, and Yunji Chen. QiMeng-Xpiler: Transcompiling tensor programs for deep
     learning systems with a Neural-Symbolic approach. In 19th USENIX Symposium on Operating Systems Design
     and Implementation (OSDI 25), pages 239–255, Boston, MA, July 2025. USENIX Association.
[14] Xinyu Feng. Local rely-guarantee reasoning. In Proceedings of the 36th Annual ACM SIGPLAN-SIGACT
     Symposium on Principles of Programming Languages, POPL ’09, page 315–327, New York, NY, USA, 2009.
     Association for Computing Machinery.
[15] Xuan Feng, Peng Cheng, Qi Chen, Shan Lu, Chieh-Jan Mike Liang, Bogdan Alexandru Stoica, Zhongxin Guo,
     Jiahang Xu, Tianyin Xu, and Lidong Zhou. Defining system intelligence. https://www.sigops.org/2025/
     defining-system-intelligence/, November 2025.

[16] GitHub. Spec kit - ai-powered specification-driven development toolkit. https://speckit.org/, 2026.
[17] Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan Newman Wu, Jieung Kim, Vilhelm Sjöberg, and David Costanzo.
     {CertiKOS}: An extensible architecture for building certified concurrent {OS} kernels. In 12th USENIX
     Symposium on Operating Systems Design and Implementation (OSDI 16), pages 653–669, 2016.

[18] Yigong Hu, You-Liang Huang, Haodong Zheng, Yicheng Liu, Dedong Xie, and Baris Kasikci. Diagnosing
     performance issues in Application-Defined resources. In 20th USENIX Symposium on Operating Systems Design
     and Implementation (OSDI 26), pages 647–664, Seattle, WA, July 2026. USENIX Association.
[19] Wenqi Huang, Charley Lee, Leonard Tng, and Serena Ge. Deepswe: Measuring frontier coding agents on original,
     long-horizon engineering tasks. arXiv preprint arXiv:2607.07946, 2026.

[20] Keisuke Kamahori, Shihang Li, Simon Peter, and Baris Kasikci. Vibeserve: Can ai agents build bespoke llm
     serving systems? arXiv preprint arXiv:2605.06068, 2026.
[21] Kimi code. https://www.kimi.com/code, 2026. Referenced August 2026.
[22] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David Cock, Philip Derrin, Dhammika
     Elkaduwe, Kai Engelhardt, Rafal Kolanski, Michael Norrish, et al. sel4: Formal verification of an os kernel. In
     Proceedings of the ACM SIGOPS 22nd symposium on Operating systems principles, pages 207–220. ACM, 2009.
[23] Hwiwon Lee, Jiawei Liu, Dongjun Kim, Ziqi Zhang, Chunqiu Steven Xia, and Lingming Zhang. SEC-bench pro:
     Can language models solve long-horizon software security tasks? arXiv preprint arXiv:2605.26548, 2026.
[24] Huaicheng Li, Daniel S. Berger, Lisa Hsu, Daniel Ernst, Pantea Zardoshti, Stanko Novakovic, Monish Shah, Samir
     Rajadnya, Scott Lee, Ishwar Agarwal, Mark D. Hill, Marcus Fontoura, and Ricardo Bianchini. Pond: Cxl-based
     memory pooling systems for cloud platforms. In Proceedings of the 28th ACM International Conference on
     Architectural Support for Programming Languages and Operating Systems, Volume 2, ASPLOS 2023, page
     574–587, New York, NY, USA, 2023. Association for Computing Machinery.
[25] Shangyu Li, Juyong Jiang, Tiancheng Zhao, and Jiasi Shen. Osvbench: Benchmarking llms on specification
     generation tasks for operating system verification. arXiv preprint arXiv:2504.20964, 2025.
[26] Heng Liao, Bingyang Liu, Xianping Chen, Zhigang Guo, Chuanning Cheng, Jianbing Wang, Xiangyu Chen, Peng
     Dong, Rui Meng, Wenjie Liu, Zhe Zhou, Ziyang Zhang, Yuhang Gai, Cunle Qian, Yi Xiong, Zhongwu Cheng,
     Jing Xia, Yuli Ma, Xi Chen, Wenhua Du, Shizhong Xiao, Chungang Li, Yong Qin, Liudong Xiong, Zhou Yu,
     Lv Chen, Lei Chen, Buyun Wang, Pei Wu, Junen Gao, Xiaochu Li, Jian He, Shizhuan Yan, and Bill McColl.
     Ub-mesh: a hierarchically localized nd-fullmesh datacenter network architecture, 2025.

[27] Hannah Lin, Martin Maas, Maximilian Roquemore, Arman Hasanzadeh, Fred Lewis, Yusuf Simonson, Ameya
     Shringi, Hongwen Dai, Patrick Musau, Tzu-Wei Yang, Amir Yazdanbakhsh, Deniz Altınbüken, Florin Papa,
     Maggie Nolan Edmonds, Aditya Patil, Don Schwarz, Satish Chandra, Chris Kennelly, Milad Hashemi, and
     Parthasarathy Ranganathan. ECO: An AI-Driven code efficiency optimizer for warehouse scale computers
     (operational systems). In 20th USENIX Symposium on Operating Systems Design and Implementation (OSDI 26),
     pages 589–625, Seattle, WA, July 2026. USENIX Association.
[28] Jiahang Lin, Shichun Liu, Chengjun Pan, Lizhi Lin, Shihan Dou, Zhiheng Xi, Xuanjing Huang, Hang Yan, Zhenhua
     Han, Tao Gui, et al. Agentic harness engineering: Observability-driven automatic evolution of coding-agent
     harnesses. arXiv preprint arXiv:2604.25850, 2026.
[29] Linux kernel developers. Github - torvalds/linux: Linux kernel source tree. https://github.com/torvalds/
     linux, 2025.
[30] Qingyuan Liu, Mo Zou, Hengbin Zhang, Dong Du, Yubin Xia, and Haibo Chen. Sharpen the spec, cut the code:
     A case for generative file system with SYSSPEC. In 24th USENIX Conference on File and Storage Technologies
     (FAST 26), pages 291–311, Santa Clara, CA, February 2026. USENIX Association.
[31] Yunkai Lou, Longbin Lai, Shunyang Li, Zhengping Qian, and Ying Zhang. Specdb: Llm-generated customized
     databases via feature-oriented decomposition. arXiv preprint arXiv:2605.31097, 2026.
[32] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. Specgen: Automated generation of formal program
     specifications via large language models. arXiv preprint arXiv:2401.08807, 2025.
[33] Alex Mathai, Chenxi Huang, Suwei Ma, Jihwan Kim, Hailie Mitchell, Aleksandr Nogikh, Petros Maniatis, Franjo
     Ivancic, Junfeng Yang, and Baishakhi Ray. kagent: An execution-guided crash resolution agent for the linux
     kernel. In Deep Learning for Code: Towards Human-Centered Coding Agents, 2026.
[34] Luke Nelson, Helgi Sigurbjarnarson, Kaiyuan Zhang, Dylan Johnson, James Bornholt, Emina Torlak, and Xi Wang.
     Hyperkernel: Push-button verification of an os kernel. In Proceedings of the 26th Symposium on Operating
     Systems Principles, pages 252–269, 2017.
[35] NJU ProjectN. Navy-apps. https://github.com/NJU-ProjectN/navy-apps, 2026. Referenced August
     2026.
[36] NVIDIA.                 How     the nvidia  vera   rubin   platform   is  solving   agen-
     tic    ai’s    scale-up  problem.                     https://developer.nvidia.com/blog/
     how-the-nvidia-vera-rubin-platform-is-solving-agentic-ais-scale-up-problem/, 2026. Refer-
     enced August 2026.
[37] OpenAI. Openai codex application. https://openai.com/codex/, 2026.
[38] Sujin Park, Mingyu Guan, Xiang Cheng, and Taesoo Kim. Principles and methodologies for serial performance
     optimization. In 19th USENIX Symposium on Operating Systems Design and Implementation (OSDI 25), pages
     357–373, 2025.
[39] Pi coding agent. https://pi.dev/, 2026. Referenced August 2026.
[40] Deepak Babu Piskala. Spec-driven development: From code to contract in the age of ai coding assistants. arXiv
     preprint arXiv:2602.00180, 2026.
[41] Ramneet Singh, Sathvik Joel, Abhav Mehrotra, Nalin Wadhwa, Ramakrishna B Bairi, Aditya Kanade, and
     Nagarajan Natarajan. Code researcher: Deep research agent for large systems code and commit history. arXiv
     preprint arXiv:2506.11060, 2025.
[42] Bogdan Alexandru Stoica, Utsav Sethi, Yiming Su, Cyrus Zhou, Shan Lu, Jonathan Mace, Madanlal Musuvathi,
     and Suman Nath. If at first you don’t succeed, try, try, again...? insights and llm-informed tooling for detecting
     retry bugs in software systems. In Proceedings of the ACM SIGOPS 30th Symposium on Operating Systems
     Principles, SOSP ’24, pages 63–78, New York, NY, USA, 2024. Association for Computing Machinery.
[43] Chuyue Sun, Ying Sheng, Oded Padon, and Clark Barrett. Clover: Closed-loop verifiable code generation. arXiv
     preprint arXiv:2310.17807, 2024.
[44] Xudong Sun, Wenjie Ma, Jiawei Tyler Gu, Zicheng Ma, Tej Chajed, Jon Howell, Andrea Lattuada, Oded Padon,
     Lalith Suresh, Adriana Szekeres, and Tianyin Xu. Anvil: Verifying liveness of cluster management controllers. In
     18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24), pages 649–666, Santa
     Clara, CA, July 2024. USENIX Association.
[45] Varun Ursekar, Apaar Shanker, Veronica Chatrath, Yuan Xue, and Samuel Marc Denton. Vero: A harness for
     agents to optimize agents. arXiv preprint arXiv:2602.22480, 2026.
[46] Andrew Waterman, Yunsup Lee, David A Patterson, and Krste Asanovi. The risc-v instruction set manual. volume
     1: User-level isa, version 2.0. Technical report, CALIFORNIA UNIV BERKELEY DEPT OF ELECTRICAL
     ENGINEERING AND COMPUTER SCIENCES, 2014.

[47] Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, and Lingming Zhang. Agentless: Demystifying llm-based
     software engineering agents. arXiv preprint arXiv:2407.01489, 2024.
[48] Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Jianan Yao, Weidong Cui, Yeyun Gong, Chris Hawblitzel,
     Shuvendu Lahiri, Jacob R. Lorch, Shuai Lu, Fan Yang, Ziqiao Zhou, and Shan Lu. Autoverus: Automated proof
     generation for rust code. Proc. ACM Program. Lang., 9(OOPSLA2), October 2025.

[49] Chenyuan Yang, Zijie Zhao, and Lingming Zhang. Kernelgpt: Enhanced kernel fuzzing via large language models.
     In Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages
     and Operating Systems, Volume 2, pages 560–573, 2025.
[50] John Yang, Carlos E Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik R Narasimhan, and Ofir
     Press. Swe-agent: Agent-computer interfaces enable automated software engineering. In The Thirty-eighth
     Annual Conference on Neural Information Processing Systems, 2024.
[51] John Yang, Kilian Lieret, Jeffrey Ma, Parth Thakkar, Dmitrii Pedchenko, Sten Sootla, Emily McMilin, Pengcheng
     Yin, Rui Hou, Gabriel Synnaeve, et al. Programbench: Can language models rebuild programs from scratch?
     arXiv preprint arXiv:2605.03546, 2026.

[52] Kechi Zhang, Jia Li, Ge Li, Xianjie Shi, and Zhi Jin. Codeagent: Enhancing code generation with tool-integrated
     agent systems for real-world repo-level coding challenges. arXiv preprint arXiv:2401.07339, 2024.
[53] Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik Roychoudhury. Autocoderover: Autonomous program
     improvement. In Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and
     Analysis, ISSTA 2024, pages 1592–1604, New York, NY, USA, 2024. Association for Computing Machinery.

[54] Qirui Zhou, Yuanbo Wen, Ruizhi Chen, Ke Gao, Weiqiang Xiong, Ling Li, Qi Guo, Yanjun Wu, and Yunji
     Chen. Qimeng-gemm: Automatically generating high-performance matrix multiplication code by exploiting
     large language models. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, pages
     22982–22990, 2025.
[55] Zhenhao Zhou, Zhuochen Huang, Yike He, Chong Wang, Jiajun Wang, Yijian Wu, Xin Peng, and Yiling Lou.
     Taming system complexity: Demystifying software engineering agents in diagnosing linux kernel faults. In
     Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
     Papers), pages 18899–18916, 2026.
[56] Mo Zou, Haoran Ding, Dong Du, Ming Fu, Ronghui Gu, and Haibo Chen. Using concurrent relational logic with
     helpers for verifying the atomfs file system. In Proceedings of the 27th ACM Symposium on Operating Systems
     Principles, SOSP ’19, pages 259–274, New York, NY, USA, 2019. Association for Computing Machinery.
[57] Mo Zou, Dong Du, Mingkai Dong, and Haibo Chen. Using dynamically layered definite releases for verifying the
     RefFS file system. In 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24),
     pages 629–648, Santa Clara, CA, July 2024. USENIX Association.
