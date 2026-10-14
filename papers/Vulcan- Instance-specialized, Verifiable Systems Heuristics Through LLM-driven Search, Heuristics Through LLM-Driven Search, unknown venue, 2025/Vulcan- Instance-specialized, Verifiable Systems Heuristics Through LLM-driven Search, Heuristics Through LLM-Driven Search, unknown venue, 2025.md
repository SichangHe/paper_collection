                                                Vulcan: Instance-Specialized, Verifiable Systems
                                                    Heuristics Through LLM-Driven Search
                                                      Rohit Dwivedula                                Divyanshu Saxena                             Sujay Yadalam
                                              The University of Texas at Austin                The University of Texas at Austin         The University of Texas at Austin
                                                     Austin, TX, USA                                  Austin, TX, USA                           Austin, TX, USA

                                                  Eric Hayden Campbell                                  Daehyeok Kim                              Aditya Akella
                                              The University of Texas at Austin                The University of Texas at Austin         The University of Texas at Austin
                                                     Austin, TX, USA                                  Austin, TX, USA                           Austin, TX, USA
                                         Abstract                                                                  Instance-Specialized, Verifiable Systems Heuristics Through LLM-
arXiv:2512.25065v3 [cs.OS] 28 Sep 2026




                                         Systems resource management tasks rely primarily on hand-                 Driven Search. In 22nd European Conference on Computer Systems
                                                                                                                   (EuroSys ’27), April 19–23, 2027, Rabat, Morocco. ACM, New York,
                                         designed heuristics. However, growing hardware heterogene-
                                                                                                                   NY, USA, 21 pages. https://doi.org/10.1145/3842654.3848582
                                         ity and workload diversity require heuristics specialized to
                                         particular deployment instances, making manual design ex-
                                         pensive and difficult to scale. In this paper, we explore how
                                         to synthesize systems heuristics using LLMs. The main chal-
                                                                                                                   1   Introduction
                                         lenge is ensuring that generated heuristics execute safely,               Systems resource management has long relied on manually
                                         integrate correctly with the surrounding system, and still                designed heuristics. This approach was sustainable when
                                         achieve strong performance. We propose Vulcan, a frame-                   hardware was slower to evolve, deployment environments
                                         work that identifies LLM-friendly interfaces that isolate core            were more uniform, and a single carefully engineered pol-
                                         decision logic from the rest of the implementation. With                  icy could remain competitive across many settings. Today,
                                         Vulcan, LLM-generated code is restricted to simple state-                 systems operate across rapidly evolving hardware platforms,
                                         less decision functions, while trusted runtime abstractions               increasingly heterogeneous memory and compute hierar-
                                         provide rich derived statistics for meaningful policy explo-              chies, and workloads that vary across tenants, applications,
                                         ration without system-integration bugs. To ensure execution               and time [56, 85, 93, 94, 107, 113]. As a result, the relevant
                                         safety, LLMs synthesize heuristics in a restricted language,              unit of optimization is often an instance: a particular combi-
                                         Anvil, that guarantees important properties by construction.              nation of hardware, workload mix, deployment setting, and
                                         We evaluate Vulcan across three well-studied domains and                  optimization objective. The challenge is that designing and
                                         demonstrate up to 4.9× higher savings for spot-VM sched-                  maintaining heuristics for each instance does not scale.
                                         uling, up to 2× lower miss ratios for cache eviction, and up                 Neural models offered an early route to instance specializa-
                                         to 14% higher application performance for tiered-memory                   tion [2, 18, 22, 23, 34, 58]. A learned policy can, in principle,
                                         systems, while ensuring execution safety throughout.                      capture complex dependencies in system state and adapt
                                                                                                                   to a target environment better than a fixed hand-written
                                         CCS Concepts: • Information systems → Information                         rule. In practice, however, neural approaches remain difficult
                                         storage systems; • Software and its engineering → Op-                     to deploy in core systems paths: their behavior is opaque,
                                         erating systems; • Computing methodologies → Ran-                         their training and serving pipelines add operational com-
                                         domized search.                                                           plexity, and integrating them with existing systems code
                                                                                                                   is cumbersome [27, 83]. More broadly, systems heuristics
                                         Keywords: resource management heuristics, LLM-aided de-
                                                                                                                   do not exist in isolation. They read state through existing
                                         sign, cache eviction, memory tiering, cloud scheduling
                                                                                                                   interfaces, maintain auxiliary state over time, and rely on
                                         ACM Reference Format:                                                     surrounding mechanisms to enact their decisions. Any auto-
                                         Rohit Dwivedula, Divyanshu Saxena, Sujay Yadalam, Eric Hay-               mated approach must therefore satisfy a substantially higher
                                         den Campbell, Daehyeok Kim, and Aditya Akella. 2027. Vulcan:              bar than predictive quality alone: it must integrate correctly
                                                                                                                   with the surrounding system and be safe to execute.
                                                                                                                      Recent advances in large language models suggest a dif-
                                                                                                                   ferent route. Unlike neural policies that must be embedded
                                         This work is licensed under a Creative Commons Attribution 4.0 Interna-   as external predictors, LLMs can synthesize code, enabling
                                         tional License.
                                         EuroSys ’27, Rabat, Morocco
                                                                                                                   instance-specialized heuristics to be expressed as executable
                                         © 2027 Copyright held by the owner/author(s).                             logic compiled directly into the host implementation. While
                                         ACM ISBN 979-8-4007-2971-3/2027/04                                        enticing, this presents difficult challenges. If the LLM has
                                         https://doi.org/10.1145/3842654.3848582                                   unrestricted control over heuristic generation, it must reason
not only about policy quality but also about state manage-        evaluate Vulcan across multiple resource-management set-
ment, memory safety, API semantics, synchronization, and          tings: deadline-aware spot-VM scheduling, cache eviction,
mechanism interaction (§2.2). Our experience, and that of         and memory tiering. Our findings show that Vulcan can syn-
recent work [20, 25], suggests that current LLMs can often        thesize both general-purpose and (when required) instance-
discover performant heuristics under such freedom, but do         specialized heuristics that are competitive with, and in sev-
not reliably produce code that satisfies the safety and inte-     eral cases outperform, strong human-designed baselines,
gration requirements needed for deployment (§2.2.1). Con-         while satisfying execution-safety properties by construction.
versely, constraining the LLM too narrowly preserves safety          In summary, we make the following contributions:
but sharply limits the policy space it can explore (§2.2.2).       • We identify a refactoring of systems heuristics around
   This paper asks: how should resource-management code be            a synthesis boundary and design a framework, Vulcan,
organized so that instance-specialized heuristic synthesis is         that exposes only core decision logic to LLM-driven search
practical? Our answer is to refactor heuristics around a syn-         while retaining system-facing structure in trusted code.
thesis boundary that isolates core decision logic from the rest    • We present libVulcan, which includes Rank/Value in-
of the implementation. The key insight is that a small set of         terfaces for decision logic and listener abstractions, which
interfaces and runtime abstractions can make such synthesis           together provide a common substrate for expressive spe-
both expressive and safe inside real systems. Concretely, we          cialized systems heuristics.
show that the core decision logic of a broad class of systems      • We introduce Anvil, a restricted policy language that
heuristics can be expressed through two interfaces, Rank and          yields execution-safety properties by construction, en-
Value, and that constructing rich statistics for performant           abling practical deployment of LLM-generated heuristics.
policies can be delegated to reusable feature-store abstrac-
                                                                   • We evaluate Vulcan for three well-studied domains: for
tions. This organization permits the synthesis of verified
                                                                      spot VM scheduling, we find a general heuristic that out-
policy code while keeping stateful logic and system-facing
                                                                      performs all baselines to yield up to 4.9× savings; for
interaction in trusted, developer-managed code.
                                                                      the well-studied cache eviction problem, we find special-
   We realize this design in Vulcan, a framework for syn-
                                                                      ized heuristics that yield up to a 2× reduction in miss
thesizing instance-specialized heuristics as safe executable
                                                                      ratios compared to baselines for specific instances; for
code. Vulcan rests on two key ideas. First, it decouples
                                                                      tiered-memory systems, we find page promotion heuris-
policy logic from state management. Developers retain re-
                                                                      tics that yield up to a 14% improvement in application
sponsibility for high-level task decomposition, policy trig-
                                                                      performance; all while satisfying important execution
gers, raw feature collection, and the mechanisms that enact
                                                                      safety properties.
decisions; LLM-synthesized artifacts are restricted to state-
less decision functions behind Rank and Value interfaces
(§4.2). To enable meaningful policy exploration, Vulcan ex-       2     The Pursuit of Instance Specialization
poses rich derived statistics through libVulcan, a library        Heuristics have been hand-crafted for various systems man-
of listeners: modular blocks that allow synthesized policies      agement tasks because optimal actions are often intractable
to use moving averages, percentiles, and other aggregates         to compute online. Action spaces for these tasks are large, de-
without implementing the data structures themselves (§4.3).       cision intervals are fine-grained, and important system vari-
Second, Vulcan synthesizes verified decision logic through        ables are often latent or partially observable. Consequently,
Anvil, a restricted domain-specific language (DSL) for LLM-       practitioners design heuristics for specific instances of a prob-
generated code (§5). By excluding heap allocation, pointers,      lem, i.e., particular combinations of workload, hardware, op-
recursion, and unbounded loops, Anvil makes important             erating conditions, and optimization objectives such as per-
execution safety properties such as memory safety, leak free-     formance, fairness, or utilization. Seen this way, systems
dom, and termination provable by construction for any well-       research is often a search for instance-specialized heuristics
formed program. Notably, the abstractions introduced by           rather than universally optimal ones.
Vulcan allow Anvil to remain restrictive while supporting
powerful heuristics.                                              2.1   An Example of Specialized Heuristics: Caching
   This design occupies a different point in the design space     We illustrate this search for specialized heuristics using the
from both prior LLM-based heuristic synthesis and prior ML-       example of cache eviction policies. Different heuristics have
for-systems work. Rather than asking the LLM to generate          been proposed for specific workloads, objectives, or deploy-
an entire heuristic implementation, Vulcan narrows syn-           ment scenarios [12, 42, 60, 80, 92, 96, 108, 111]: some [60, 111]
thesis to a structured policy layer that remains expressive       perform well for large cache sizes, while others [12, 42] are
enough for meaningful heuristic discovery. Rather than em-        more suited for smaller caches. Workload characteristics
bedding an opaque learned model, Vulcan produces explicit         also matter: scan-heavy workloads (mostly new objects)
policy code that integrates with existing implementations         and churn-heavy workloads (mostly repeated objects) re-
through narrow interfaces and trusted runtime support. We         quire different algorithms [80]. Heuristics have further been
                                                                        2.2 LLM-Based Synthesis: Requirements and Pitfalls
                                                                        Recent advances in LLMs and coding agents, particularly in
                                                                        generating executable code [88, 98, 112], refining it using
                                                                        natural-language feedback [105], and carrying out multi-step
                                                                        reasoning [99], make automated heuristic specialization in-
                                                                        creasingly practical. Indeed, several recent systems [20, 25,
                                                                        33, 44, 68] have already demonstrated that LLM-based ap-
                                                                        proaches can discover effective resource-management heuris-
                                                                        tics for specific problems. While these advances are promis-
Figure 1. Count of CloudPhysics traces where each heuristic             ing, building usable heuristics for practical systems imposes
performs best (max. object hit rate). Tiny, small, and large imply      three key requirements.
cache sizes of 0.1%, 1%, and 10% of trace footprint.                     • Performance: They must meet or exceed the perfor-
                                                                           mance of existing manually designed heuristics.
                                                                         • Execution safety: They must be proven to be free from
                                                                           failures such as crashes, memory errors, leaks, or non-
                                                                           termination. Automated synthesis at scale makes the con-
                                                                           ventional practice of manual review impractical, so safety
                                                                           verification must be automated as well.
                                                                         • System integration: Heuristics rarely run in isolation:
                                                                           they interact with other system components to read state
Figure 2. Illustration of three design alternatives. Uncon-                and enact their decisions. Thus, the generated code must
strained LLM edits result in execution safety and systems integra-         respect the APIs and semantics of the surrounding system.
tion concerns (§2.2.1); overly constrained synthesis fails to achieve      Naively applying LLMs may not satisfy all three prop-
good performance (§2.2.2). Vulcan attempts to satisfy all three.        erties; below, we explore the design space to identify an
                                                                        approach that does. Figure 2 summarizes the alternatives,
                                                                        which we discuss in detail below.

                                                                        2.2.1 Unconstrained Search Space Approaches. At one
tailored for end-to-end objectives such as tail latency [14]            extreme of the design space are existing proposals for LLM-
and fairness [49], and for system-level constraints such as             driven heuristic synthesis [20, 25, 33, 68]. These approaches
CPU overhead [92], lock-free design [108], and memory                   place few restrictions on what the LLM generates: starting
efficiency [26].                                                        from decision logic, the LLM agent is free to allocate and
   To quantify this observation, we executed 17 caching al-             manage state and interact with system APIs as it sees fit. This
gorithms using libCacheSim [43] on 106 block I/O traces                 unconstrained search space maximizes the LLM’s opportunity
from the CloudPhysics dataset [97], where each trace repre-             to discover high-performing heuristics, but also exposes the
sents a distinct instance (corresponding to a different tenant).        full implementation surface to errors.
Figure 1 shows our findings: no single algorithm performs                  We illustrate this using cache eviction as a running exam-
best on even half the instances, and the set of competitive             ple. We compare two workflows: (i) an evolutionary loop [25,
algorithms shifts significantly with cache size, e.g., ARC is           81] that iteratively proposes, evaluates, and refines candi-
better for tiny caches while LIRS is better for large caches.           dates; and (ii) an agentic workflow with access to codebase
   These findings are not limited to cache eviction: policies           inspection and other tools. Both approaches used Claude
across the systems stack exhibit the same instance depen-               Opus 4.5 [7] to synthesize heuristics for libCacheSim [43].
dence. Congestion control algorithms are tailored for Inter-            We evaluate the generated heuristics on ten traces from
net [1, 2, 8, 17] versus datacenter workloads [4, 48, 64], kernel       the CloudPhysics dataset [97]. Full details are provided in
queueing disciplines are tuned for varying performance and              Appendix A; here, we discuss the key outcomes.
fairness objectives [29, 76, 86, 89], and cluster schedulers
are fine-tuned for specific application classes such as data            Evolutionary loop. We ran the search for fifty iterations
processing jobs [30, 31], cloud VM workloads [55], or deep              and found that several synthesized heuristics had system-
learning training jobs [66, 102].                                       integration violations: several synthesized heuristics (in-
   However, as workloads grow increasingly diverse, perfor-             cluding the best-performing one) under-reported per-object
mance objectives become multi-dimensional, and hardware                 metadata size, claiming to use only 16 bytes while actually al-
heterogeneity evolves rapidly, manually specializing heuris-            locating up to 40 bytes. libCacheSim uses reported metadata
tics for each instance is no longer tractable. This raises a            size to check whether the cache has space for a new object;
natural question: can heuristic specialization be automated?            under-reporting causes more objects to be admitted than the
cache capacity allows, artificially inflating the hit rate. We
manually fixed these bugs and found that the resulting best
heuristic achieved a 1.2%–13.66% improvement over FIFO,
which is comparable to several manual baselines.

Agentic workflow. We allowed a Claude Code agent [6] to
make edits to the codebase until it reached a fixed cost budget,
and repeated this ten times independently. Across these ten
heuristics, four modified internal libCacheSim counters that
are read-only – another system-integration violation. One
heuristic also introduced a double-free bug, an execution            Figure 3. Overview of Vulcan. Users provide task-specific inputs
safety violation; incidentally, this specific bug was not            – a template, a prompt, and an evaluator. Vulcan uses a code-
triggered during testing, demonstrating that simple compile-         generation framework to produce a safe and performant heuristic.
and-test pipelines alone are insufficient. The improvements
for the best heuristic (out of ten) were 0.2–23% over FIFO.          FIFO by only 0.01%–0.19%. These gains are far smaller than
   These results confirm that LLMs can discover performant           those in §2.2.
heuristics, but do not reliably produce code that satisfies
safety and integration requirements. Related work reports            2.3   Towards a Better Division of Labor
similar failures: ADRS [20] noted use-after-erase and null           While LLM-synthesized heuristics hold promise for instance
dereference bugs, consistent with broader evidence that              specialization, approaches at both extremes of the design
LLMs are less reliable on tasks requiring reasoning over             space fail to meet all three requirements (Figure 2), due to a
complex codebases [40, 45, 71, 115].                                 poor division of labor between the LLM and the developer.
                                                                     In the unconstrained setting (§2.2), the developer delegates
2.2.2 Overly Restricted Search Space Approaches. The
                                                                     everything to the LLM: decision logic, state management,
problems described in §2.2 arise because the LLM has un-
                                                                     and system interaction alike; in the over-restricted setting
restricted access to the implementation surface. The other
                                                                     (§2.2.2), the developer retains so much control that the LLM
extreme is to restrict LLM edits to narrow refinements of
                                                                     cannot meaningfully explore. With Vulcan, we identify ab-
an existing heuristic [36], such that system integration and
                                                                     stractions that enable a better division of labor: supporting
execution safety are preserved by construction. This includes
                                                                     meaningful policy exploration while preserving execution
tasks such as adjusting threshold values, adding condition-
                                                                     safety and system integration by construction.
als, or reweighting existing features. However, shrinking the
search space so aggressively forfeits the ability to discover        3     Vulcan Overview
substantially better policies.
   To illustrate this, we revisit the evolutionary loop experi-      We present Vulcan, a framework for synthesizing safe, per-
ment for cache eviction but with a much narrower interface.          formant, and integration-compliant heuristics for systems
Inspired by HALP [92], we select eight eviction candidates           resource-management tasks (see Figure 3).
using a base heuristic and then restrict the LLM-written func-       3.1   Key Ideas
tion to choosing the final candidate from within that set. We
provide the LLM with each candidate’s access count, size,            Vulcan rests on two key ideas that together address the
last-access timestamp, and insertion timestamp, plus per-            three requirements from §2.2.
centile distributions of these statistics over all cached objects.   Idea 1: Abstractions to decouple core decision logic and
We experiment with both LRU and FIFO as base heuristics,             state management (§4). To explore meaningful heuristics,
running evolutionary search for 50 iterations each on the            LLMs must derive useful statistics from raw features and use
same traces as §2.2. We refer to the resulting best heuristics       them to produce a decision. Vulcan decouples these two
as Evolved-LRU and Evolved-FIFO, respectively.                       steps and restricts LLM edits to: (i) generating code for state-
   Under this interface, the LLM cannot interact directly            less decision interfaces, and (ii) selecting and querying an
with libCacheSim, eliminating system-integration violations          API for rich derived features. We show that two stateless in-
and substantially narrowing the space of execution-safety            terfaces, Rank (ranking candidates) and Value (computing a
failures. Indeed, none of the synthesized heuristics exhibited       scalar from system state), suffice to express the core decision
execution-safety violations. However, the same restriction           logic of a broad class of resource-management heuristics
limits the search space too much to produce meaningful               (§4.2). A library of listeners (§4.3) exposes useful statistics
gains: the best Evolved-LRU heuristic achieves a miss-ratio          from raw features while handling the underlying state man-
reduction (MRR) over FIFO by 0.05%–7.76%, nearly identical           agement. All other aspects of system integration remain the
to LRU’s 0.04%–7.53%. Similarly, Evolved-FIFO improves over          responsibility of developers.
Idea 2: Safety by construction via a restricted policy lan-
guage (§5). As shown in §2.2, compile-and-evaluate pipelines
alone are insufficient to ensure safety. Vulcan addresses
this through Anvil, a restricted DSL in which LLMs express
decision logic. Anvil omits heap allocation, pointer arith-
metic, recursion, and unbounded loops; as a result, memory
safety, leak freedom, and termination are guaranteed by
construction without the need for human review.

3.2   Workflow: Using Vulcan to Create Heuristics
Developers provide three inputs: a heuristic template ( 1 ), an
evaluator ( 2 ), and a natural-language prompt ( 3 ) describing     Figure 4. Typical components of systems heuristics (using
the resource-management task, the available raw features,           memory tiering as an example). Vulcan impacts the colored
and the evaluation methodology.                                     parts; icons show the division of responsibility among developers,
   The heuristic template (based on Idea 1) exposes the core        libVulcan, and LLMs.
decision logic through Rank or Value interfaces and de-
clares all raw features of interest. Developers define this         Since processing raw signals at decision time can impose
template using libVulcan ( 4 ), Vulcan’s runtime library.           high overhead, a third component stores them in data struc-
The template and prompt are passed to a code-generation             tures that support efficient computation of temporal or statis-
framework ( 5 ), which synthesizes a heuristic in Anvil ( 6 )       tical aggregates; for instance, a windowed average of DRAM
(based on Idea 2) by iteratively generating candidate heuris-       bandwidth rather than per-timestamp measurements. The
tics, evaluating them on the user-provided evaluator, and           decision logic consumes these derived statistics to produce a
using the feedback to improve. LLMs may also attach listen-         policy output. Finally, mechanisms enact the decision, e.g.,
ers to raw features, deriving statistics from simple means to       swapping pages between memory tiers.
arbitrary percentiles. The synthesized heuristic is passed to          With Vulcan, decomposition, triggers, and mechanisms
the evaluator, which scores it and returns feedback to the          (uncolored in Figure 4) remain the developer’s responsibil-
synthesis loop.                                                     ity. These components require deep knowledge of system
   Once the search terminates, Vulcan returns the best-             semantics: in the memory-tiering example, decomposition
scoring candidate as the final heuristic ( 7 ). Vulcan is agnos-    depends on how allocators and page fault handlers interact;
tic to the code-generation approach; for our case studies (§7),     adding new triggers may require changes to kernel page
we use two approaches (ShinkaEvolve [51], OpenEvolve [87]).         fault handling; and implementing migration requires cor-
                                                                    rectly managing page metadata, locks, and reference counts.
                                                                    As §2.2 showed, even state-of-the-art LLMs do not reliably
4     libVulcan: Interfaces for                                     handle this complexity.
      Policy Exploration                                               Vulcan automates the remaining components: feature
Vulcan narrows LLM synthesis to the core decision logic of          storage and decision logic. Developers expose raw signals
a heuristic, delegating state management and system inter-          through a heuristic template ( 1 in Figure 3), leaving open
action to developer-owned code (§4.1). This division leads to       how those signals are aggregated and used in the decision.
two concrete abstractions: stateless decision interfaces (§4.2)     The code-generation framework ( 5 ) fills in this logic using
and listener-based feature stores (§4.3).                           libVulcan’s APIs ( 4 ) for rich derived statistics.
                                                                    Insight motivating libVulcan. libVulcan serves as the
4.1   Division of Labor in Vulcan                                   interface between developers, synthesized heuristics, and
To motivate the division of labor in Vulcan, we examine             the system. A key observation is that many safety and inte-
the typical components of systems heuristics, illustrated in        gration bugs arise when LLMs are responsible for manag-
Figure 4 using a memory-tiering system.                             ing low-level feature state: allocating buffers, maintaining
   A high-level task is typically decomposed into a collection      data structures, and updating them correctly across events.
of sub-policies; memory tiering, for example, uses separate         libVulcan eliminates this exposure by providing stateless
policies for allocation [78], placement [59, 78], and migra-        interfaces for decision logic (§4.2) while encapsulating all
tion [103] (Figure 4). Within each policy, there are five typical   state management in a listener library (§4.3).
components. The trigger determines when the policy runs,
e.g., page faults [78] or periodic scans [103]. Then, relevant      4.2   Value and Rank Interfaces
statistics are collected: for the page migration policy in Fig-     The core decision logic of most resource-management heuris-
ure 4, these include page accesses and DRAM bandwidth.              tics takes one of two forms: it either ranks a set of candidates
          Table 1. Examples of systems resource management tasks and the type of task (Value or Rank) they fall into.

Policy                                 Description                                                     Type
Congestion control [32]                Decide the number of unacknowledged bytes in flight (cwnd).     Value: compute the cwnd.
DVFS control [73]                      Decide cpu_freq to balance performance & power.                 Value: compute the frequency.
Cluster autoscaling [47]               Decide n_replicas to provision for a given service.             Value: compute replicas per service.
Hardware prefetching [63]              Choose an offset from the current access to prefetch data.      Value: compute the offset value.
Cache eviction [91]                    Select which cached object(s) to evict.                         Rank: all cached objects.
CPU scheduling [70]                    Select which thread to schedule next.                           Rank: all runnable threads.
Promotion in tiered memory [78, 103]   Select which pages to promote to a higher tier.                 Rank: all memory pages.


and selects a subset (e.g., evicting an object from cache), or it          its signal and maintains internal state for efficient queries.
computes a scalar value that drives a resource-management                  For example, an Average listener maintains running sum
action (e.g., computing a cwnd in congestion control). Table 1             and count state and returns their ratio on query. libVulcan
shows that this pattern recurs across a broad class of systems             also supports more complex aggregates: temporal aggregates
tasks, and libVulcan exposes two corresponding interfaces,                 (e.g.,RollingPercentile) and population-level aggregates
Rank and Value, for LLM-generated decision logic. When                     over all candidate objects (e.g.,PopMean). Temporal aggre-
neither interface fits, it can be extended with a small number             gates support both interfaces; population-level aggregates
of additional functions.                                                   primarily support Rank tasks.
Interface: Value. A Value heuristic, Value(𝑋 ) → 𝑌 , is                       Listeners need only be reviewed and verified for execution
a function where 𝑋 encodes system state as a set of fea-                   safety once, and a compact set of listeners can be reused
tures and 𝑌 is a scalar output corresponding to some control               across several systems tasks, as demonstrated by our case
variable. Table 1 lists examples of typical Value tasks and                studies (§7). Listeners are also composable: multiple listeners
their outputs. For instance, a congestion controller maps fea-             can be attached to the same feature, and different features
tures such as rtt and loss_rate to a window size. To use                   can use different listeners, forming a task-specific feature
the Value interface, developers define the function signa-                 store without any LLM-written state management.
ture double value_fn (vulcan::store&), where store
contains the state 𝑋 and the return value is 𝑌 .                           4.4    An Example of Using libVulcan
Interface: Rank. A Rank heuristic, Rank(𝑋, O) → R, is                      Listing 1 demonstrates how the cache eviction task is set up
a function where O = {𝑜𝑖 ↦→ 𝑓𝑖 } maps 𝑁 candidate ob-                      using libVulcan. Lines 1–25 form the template, which is one
jects to their features and R = [𝑜𝑖 1 , 𝑜𝑖 2 , . . . ] is an ordered       of the inputs to Vulcan. This template is written by the user
list of all objects. The mechanism then selects from this                  of Vulcan (i.e., the developer); LLMs in Vulcan then search
ordered list as needed. Cache eviction, for example, ranks                 for instance-specialized heuristics within the confines of this
all objects in cache by their utility for retention (Table 1)              template by deciding which listeners to add (lines 27–29)
and evicts the lowest-ranked object. As part of the tem-                   and defining the decision-making function (lines 31–35).
plate for Rank tasks, developers define the function sig-                     To create this template, the developer decides which raw
nature for a per-object scoring function: double score_fn                  signals the policy should use (lines 2–4), sets up instru-
(vulcan::store&, int64_t obj_id). libVulcan provides                       mentation to collect these signals (within on_insert and
utility functions to sample candidates and sort them by this               on_access), and then formulates the problem using one or
score_fn in ascending or descending order as needed (§4.5).                more of Vulcan’s interfaces (Rank or Value). In Listing 1,
                                                                           cache eviction is formulated as a Rank problem (lines 19–23),
4.3      Configurable Feature Stores Using Listeners                       in which the lowest-ranked object is evicted; the developer
Stateless decision functions cannot compute derived fea-                   can also choose between multiple implementations of Rank
tures such as moving averages, percentiles, or population-                 provided by libVulcan (line 21, §4.5).
level statistics; yet smoothed averages [15, 16, 92, 103], sum-
mary statistics [17, 32], and histograms [12] are essential to
strong heuristics. Delegating this state management to LLMs                4.5    libVulcan Implementation
reintroduces the safety bugs from §2.2.                                    libVulcan implements the Rank and Value interfaces as
   Vulcan resolves this tension through listeners: modular                 well as the listener APIs as a C++ library. C/C++ systems can
blocks that the LLM attaches to raw signals to create rich de-             integrate libVulcan directly; Python-based systems use the
rived features. Once attached, their query APIs can be called              same APIs via pybind11 [41] bindings. Our case studies exer-
inside the decision logic, whether a value function (Value)                cise both integration paths: spot VM scheduling (§7.1) uses
or a scoring function (Rank). Table 2 summarizes the listen-               Python bindings, while cache eviction (§7.2) and memory
ers provided by libVulcan. Each listener tracks updates to                 tiering (§7.3) use the C++ library.
     Table 2. Listeners provided by libVulcan. The table shows the state each listener maintains, with update/query/space complexities. The
     first six rows show listeners for temporal aggregates, while the bottom two show listeners for aggregates across the object population.

                                                                                                                        Complexity
     Listener                         Query API(s)           State and data structures
                                                                                                           Update             Query            Space
     Average()                        get_avg                sum, count                                     𝑂 (1)             𝑂 (1)           𝑂 (1)
     MinMax()                         get_min, get_max       min, max                                       𝑂 (1)             𝑂 (1)           𝑂 (1)
     RollingWindow(N)                 get_kth, get_avg       ring buffer, sum                               𝑂 (1)             𝑂 (1)           𝑂 (𝑁 )
     EWMA({𝛼 0 , 𝛼 1 , . . . 𝛼 𝑀 })   get_ewma(𝛼 )           current EWMA value for each 𝛼                  𝑂 (1)             𝑂 (1)           𝑂 (1)
     RollingPercentile(N)             get_percentile         ring buffer, ordered multiset [5]            𝑂 (log 𝑁 )        𝑂 (log 𝑁 )        𝑂 (𝑁 )
     RollingCount(N)                  get_count, contains    ring buffer, counts map                        𝑂 (1)             𝑂 (1)           𝑂 (𝑁 )
     PopPercentile()                  get_pop_percentile     per-object latest, ordered multiset [5]      𝑂 (log 𝑀 )        𝑂 (log 𝑀 )        𝑂 (𝑀 )
     PopMean()                        get_pop_mean           per-object latest, sum                         𝑂 (1)             𝑂 (1)           𝑂 (𝑀 )


     Listing 1. Template for cache eviction in libVulcan (lines 1–25).         Table 3. Execution-safety properties guaranteed by Anvil.
     LLMs search for policies within this template; lines 27–35 (red)
                                                                              ID    Property
     show a sample candidate policy synthesized during the search.
                                                                              P1    Memory safety. No out-of-bounds access, use-after-free,
 1   void init():
                                                                                    or double-frees.
 2     vulcan::store store = {
                                                                              P2    Leak freedom. No unbounded memory growth over time.
 3       .obj_signals: [{"insert_time",int}, {"access_time",int}]
                                                                              P3    Termination. Must not run indefinitely; LLM scoring functions are
 4     };
                                                                                    guaranteed to eventually terminate.
 5     setup_listeners(store);
 6
 7   // LLM evolved functions
 8   void setup_listeners(vulcan::store& fs);                                 decision-time latency for incremental bookkeeping. These
 9   double score_fn(vulcan::store& fs, int64 id);                            implementations also expose configurable parameters; e.g.,
10                                                                            OnDemandSort can approximate ranks via a random sample
11   void on_insert(ObjId o):                                                 of candidates rather than all of them (Listing 1, line 21).
12     store.add_obj(o);
13     store.update("insert_time", o, now());
                                                                                 libVulcan totals ∼3.5K lines of C++ code: ∼1,300 for the
14                                                                            core Rank and Value interfaces, ∼1,000 for listeners, and
15   void on_access(ObjId o):                                                 ∼250 for Python bindings.
16     store.update("access_time", o.id, now());
17                                                                            5     Anvil: DSL for LLM-Written Code
18   ObjId evict_obj():
19     R = vulcan::Rank(                                                      The abstractions in §4 reduce the scope for execution-safety
20       store.all_objs, score_fn,                                            bugs but do not eliminate them. Vulcan closes this gap
21       vulcan::OnDemandSort, n_sample=32                                    with Anvil: a domain-specific language in which every well-
22     );                                                                     formed program satisfies the execution-safety properties in
23     victim = R.back();
24     store.remove_obj(victim);
                                                                              Table 3 by construction.
25     return victim;                                                         Programming model. Anvil is a restricted imperative lan-
26
                                                                              guage based on C++: it supports scalars, arithmetic, con-
27   void setup_listeners(vulcan::store& fs):
28     fs.add_listener("access_time",vulcan::Latest());
                                                                              ditionals, bounded for loops, and built-in math functions
29     fs.add_listener("insert_time",vulcan::PopPercentile());                (e.g., anvil::max), while excluding pointers, arrays, contain-
30                                                                            ers, heap allocation, recursion, and unbounded loops. These
31   double score_fn(vulcan::store& fs, int64 id):                            exclusions map directly to the execution safety properties
32     auto recency = fs.get_latest("access_time", id)-now()                  (Table 3): excluding pointers and arrays prevents unsafe
33     if fs.get_pop_percentile("insert_time", id) > 0.9:
34         return 6.0 * recency
                                                                              memory accesses (P1); excluding heap allocation and persis-
35     else return 1.0 * recency                                              tent state prevents memory leaks and state-management er-
                                                                              rors (P2); excluding recursion and unbounded loops prevents
                                                                              non-termination (P3).
        libVulcan provides multiple implementations of Rank                   State management and trust model. Most useful sys-
     that the developer can choose between when setting up                    tems heuristics rely on persistent state, such as histories
     the template: OnDemandSort (used in §7.3) scores and ranks               or derived statistics, but pure Anvil does not contain the
     candidates at decision time, while IncrementalSort (used                 constructs needed to maintain such state. To let Anvil pro-
     in §7.2) precomputes ranks by maintaining candidates in a                grams use stateful functionality implemented outside the
     priority queue that is updated as features change, trading               language, Anvil supports extern declarations for C/C++
functions: the Anvil compiler sees the extern’s function         trace-driven simulation (§7.1, §7.2) or execution over a short
signature (name, scalar arguments, and scalar return type),      representative workload (§7.3).
while its implementation resides in trusted external code. In
Vulcan, listener query APIs (Table 2) are exposed to synthe-     Natural-language prompt. As discussed in §3, users must
sized heuristics through such externs. This defines Anvil’s      also provide a natural-language prompt. Besides describing
trust model: a well-formed Anvil program satisfies P1–P3         the task at hand, this prompt must also include informa-
provided every linked extern also satisfies P1–P3.               tion about libVulcan APIs and may include evaluator de-
Compiling and executing Anvil code. In Vulcan, code              tails, workload or instance information, and instructions for
generators write heuristics in Anvil and use libVulcan           heuristic design.
functions to attach and query listeners (declared in Anvil
as function prototypes). The LLM-written Anvil code is           LLM API budgets. In our experiments, we use Claude Son-
then compiled in two stages. First, the frontend parses the      net 4.5 and Claude Opus 4.5 (80%/20% split) on AWS Bedrock
generated heuristic against the Anvil grammar and rejects        to synthesize heuristics for Vulcan and the baseline [20, 87].
disallowed constructs. Next, the Anvil code is lowered to C
and linked against C implementations of libVulcan func-
tions (for attaching/querying listeners) that were simply
                                                                 7     Case Studies and Results
declared as externs in the Anvil code. The final C imple-        We use Vulcan to synthesize heuristics for three resource-
mentation is then compiled with native toolchains (e.g., gcc).   management tasks:
This lowering of Anvil code into C is made possible because       • Spot VM scheduling (§7.1): decide when a deadline-
of Anvil’s C-like syntax: scalar expressions, conditionals,         driven cloud job should use cheaper spot instances to
and bounded loops pass through unchanged, while Anvil               minimize completion cost.
built-ins (e.g., anvil::max) resolve to equivalent C library      • Web cache eviction policies (§7.2): choose which cached
calls. Thus, executing Anvil code adds no interpreter or JIT        objects to evict to maximize object hit rate (e.g., in CDNs).
overhead and makes integration with the rest of the code-         • Page promotion policy in tiered-memory systems
base seamless. The only overhead is the compilation step            (§7.3): choose which pages to promote from slower mem-
that lowers Anvil code to C, which takes under one second           ory tiers to faster tiers to maximize application-specific
per scoring function.                                               performance metrics.
Implementation. Anvil is implemented in OCaml using              The primary question we seek to answer through our eval-
Menhir [75] for parser generation, totaling approximately        uation is whether Vulcan can synthesize heuristics that
3.5K lines of code: ∼1,000 for the parser and lexer, ∼1,500      outperform strong, human-written baselines across these
for name resolution and class desugaring, and ∼1,000 for the     diverse tasks. Our evaluation measures: (i) how Vulcan
AST and C code generation.                                       compares to unconstrained LLM-based synthesis, (ii) how
                                                                 Vulcan’s components (interfaces, listeners, and the DSL)
6   Using Vulcan in Practice                                     affect synthesized heuristics, and (iii) the cost of heuristic
                                                                 synthesis (e.g., API charges and elapsed time) relative to the
Defining the target instance. A key requirement of Vul-          resulting benefits. In subsequent sections, we will use these
can-generated heuristics is high performance, which often        case studies and results to discuss the developer effort re-
requires instance specialization (§2) across workloads, hard-    quired to use Vulcan (§8.1) and the scope of its decision
ware configurations, operating regimes, or performance ob-       interfaces, including how they can be composed or extended
jectives. When instances differ enough that no single heuris-    to support additional tasks (§8.2).
tic performs well across them (Figure 1), policies should be
specialized to a particular instance, such as a specific clus-   7.1   Spot VM Scheduling
ter, tenant, workload class, or arrival pattern (as we do for
                                                                 Cloud providers offer two pricing tiers: on-demand instances
cache eviction in §7.2). In contrast, for understudied prob-
                                                                 are reliably available but expensive, while spot instances
lems where good solutions are not yet well understood, even
                                                                 are up to 11× cheaper [101] but can be preempted at any
a single heuristic targeting average-case performance can
                                                                 time. Deadline-sensitive jobs therefore typically avoid spot
yield substantial gains, as in our spot VM scheduling case
                                                                 instances and pay the on-demand premium for predictability.
study (§7.1).
                                                                 Recent work [101] proposed a scheduler that cuts this cost
Cost–fidelity tradeoff in evaluators. Vulcan invokes the         by opportunistically switching between spot and on-demand
evaluator hundreds of times during search, so evaluation         while still meeting deadlines. We use Vulcan to synthesize
cost bounds the amount of exploration possible. Evaluating       scheduling heuristics for the single-region (§7.1.1) and multi-
heuristics on real systems can take hours per candidate; in      region formulations (§7.1.2) of this problem and compare the
practice, we use cheaper proxies during the search phase:        resulting heuristics against unconstrained evolution [20].
                              Table 4. Summary of use cases, baselines, evaluation metrics, and evaluators.

Use case                         Baselines                                            Metric                              Evaluator
Spot VM scheduling (single)      Greedy, Uniform Progress [101], ADRS [20]            Avg. USD saved                      Simulator, 5% sample
Spot VM scheduling (multi)       Round-robin uniform progress, ADRS [20]              Avg. USD saved                      Simulator, 5% sample
Cache eviction                   Nine state-of-the-art algorithms                     Object miss-ratio reduction (MRR)   Simulator, 1M requests
Memory tiering                   ARMS [103]                                           Goodput, latency                    Emulator, per-workload


7.1.1 Single-region scheduling. In the single-region for-
mulation [101], the scheduler is initialized with per-job con-
stants: the required VM type, execution time, deadline, and
a changeover delay cost incurred when the job is switched
between on-demand and spot instances. At each tick, the
scheduler observes the current job status, progress so far,
remaining work, and spot availability, then chooses one of
three actions: run on spot, run on on-demand, or wait.                           Figure 5. Comparison of schedulers for the single-region spot
   Template. Since the per-tick decision in this problem is                      VM setting. (a) Mean savings; higher is better. (b) Big losses/gains
a single control variable encoding one of three actions, it                      exceed $10; small losses/gains are below $10.
naturally fits the Value interface, which maps observed state
to a scalar output. While Value supports arbitrary scalar                               Listing 2. Regime detection in Vulcan’s scheduler.
outputs, we restrict its output domain here to three values                  1   double alpha = fs.get_avg(has_spot);
corresponding to the actions above. The per-tick features and                2   // longest consecutive spot availability streak (L_max)
per-job constants are passed as inputs to the Value function,                3   int64_t L_max = 0, L_curr = 0;
and the LLM may attach listeners to the per-tick features.                   4   for (int i = 0; i < 18; ++i):
                                                                             5     if (fs.get_kth(has_spot, i) == 1):
   Manually designed heuristics. We use two baselines
                                                                             6       L_curr++; L_max = max(L_max, L_curr);
from Wu et al. [101]. The first, a greedy heuristic, uses spot               7     else L_curr = 0;
VMs opportunistically, waits when they are unavailable, and                  8   // regime detection: scarce when alpha low or small streaks
switches to on-demand only when further waiting risks miss-                  9   bool scarce = (alpha < 0.35)||(L_max<od_ticks && alpha<0.5);
ing the deadline. The second is Uniform Progress (UP), the
state-of-the-art heuristic for this problem. Uniform Progress
keeps the job on a linear progress trajectory from start to
finish: it exploits spot VMs when they are available, but if
needed, switches back to on-demand to catch up with the
linear pace.
   Evaluator. We use the simulator and traces from Wu et
al. [101]: spot-availability data for four AWS instance types
(1- and 8-GPU K80/V100) paired with job configurations to
yield 21,600 evaluation cases. During synthesis, candidates
are scored by running a fixed 5% sample of all evaluation
                                                                                 Figure 6. Vulcan vs. unconstrained search (ADRS). Lines: best-
cases and computing the average USD savings over the greedy                      performing-heuristic so far; dots: individual candidates.
baseline; all reported results use the full 21,600-case set.
   Results. We run OpenEvolve [87] for 100 iterations and
compare the resulting Vulcan scheduler against two base-                         from UP’s core design assumption: it treats spot availability
lines: (i) UP, the manual baseline above, and (ii) ADRS [20],                    as worst-case unreliable. UP switches to on-demand whenever
which runs OpenEvolve with the same budget but allows                            the job falls behind its expected progress schedule, regardless
unconstrained edits to the scheduler policy.                                     of spot availability history. In contrast, the Vulcan heuristic
Main result. Figure 5a shows the mean savings of each                            (Listing 2) attaches RollingWindow and Average listeners
scheduler over the greedy baseline. Our synthesized sched-                       to track recent spot availability (has_spot), classifying each
uler achieves nearly 4.9× the savings of UP and 1.7× those                       tick into a scarce or abundant regime and adapting accord-
of ADRS.                                                                         ingly: committing to on-demand sooner when spot looks un-
How Vulcan outperforms UP. The per-trace distribu-                               reliable, but staying patient and returning opportunistically
tion (Figure 5b) reveals how Vulcan outperforms UP: UP                           when it does not.
performs worse than the greedy heuristic (i.e., costs more                       Unconstrained search. Figure 6 compares Vulcan to ADRS
money) on 52% of the evaluation cases. This pattern stems                        under an equal budget. Despite limiting the LLM to a Value
     Table 5. Cost of heuristic synthesis with Vulcan.

                     Tokens (millions)
Use case                                    API cost      Time
                    Input      Output
Spot VM (single)        2.2       0.20           $11         2.5 h
Spot VM (multi)         1.0       0.12            $5         1.2 h
Cache eviction†     0.7–2.0  0.15–0.50         $5–15     2.4–4.4 h
Memory tiering†     1.6–2.2  0.23–0.36        $10–14     1.9–3.0 h
             † Minimum–maximum range across instances.                Figure 7. Average workload cost per scenario (lower is better).


                                                                             Table 6. Raw signals for cache-eviction scoring.

                                                                     Feature type       Attributes
function written in Anvil (§5), Vulcan loses no performance          Per-object (𝑓𝑖 )   Access count, last access timestamp, insertion timestamp,
to unconstrained search—in fact, it reaches better heuris-                              size (bytes)
tics faster. A possible explanation is the smaller, structured       Global (𝑋 )        Current time, recently evicted object IDs (ghost list).
search space: while ADRS must explore the entire heuristic
implementation, Vulcan explores only the decision logic,
enabling targeted policy changes.                                    a Value task (with a fixed output domain of region identi-
Impact of removing listeners. Without listeners (Vulcan-             fiers), destination selection naturally involves comparing re-
NL), the heuristic is limited to the latest value of each feature.   gions based on their respective observation histories, making
Vulcan-NL still outperforms UP, but full Vulcan achieves             Rank’s semantics a more natural fit.
roughly 2.6× the savings of Vulcan-NL. Without listeners,               Evaluator. We use the multi-region simulator and bench-
the scheduler cannot use recent spot-availability history to         mark from ADRS [20], with 600 evaluation cases with AWS
distinguish scarce and abundant regimes, preventing the              spot availability and prices for V100 GPU instances across
adaptive behavior used by the full Vulcan heuristic.                 nine U.S. regions/zones. During evolution, the evaluator runs
Cost of synthesis. Synthesizing the heuristic (Listing 2)            each candidate heuristic on a fixed 5% sampled subset of all
with Vulcan incurred $11 in LLM costs and took 2.5 hours             evaluation cases and returns the average cost per trace; after
(Table 5). Across all 21,600 evaluation scenarios (i.e., sim-        synthesis, the best policy is evaluated on the full benchmark.
ulated jobs), the resulting scheduler saves an average of               Results. We run OpenEvolve for 100 iterations and com-
$7.12 per job relative to the greedy baseline, or $2.81 more         pare the result against: (i) UP-RR [20], a round-robin multi-
than the best ADRS solution. At this average improvement             region extension of UP, and (ii) an unconstrained-search
over ADRS, using the synthesized heuristic for just four jobs        baseline (ADRS). We report results for six scenarios [20]
would recover the LLM synthesis cost on average.                     covering different combinations of availability zones and ge-
                                                                     ographic regions, each with 100 evaluation cases. As Figure 7
7.1.2 Multi-Region Scheduling. In the multi-region for-              shows, Vulcan outperforms UP-RR in four of six scenarios,
mulation, the scheduler is allowed to choose which region            demonstrating how performant heuristics can be found even
to run the job in, with each region having different pricing         within constrained interfaces that guarantee execution safety.
and spot availability. At each tick, in addition to choosing         As in the single-region case study, synthesizing this multi-
to schedule a job or wait, the scheduler can also choose to          region heuristic required only 1.2 hours on a single node and
switch to a different region. Since the scheduler can observe        $5 in LLM API costs (Table 5).
spot availability only for the current region, a good heuristic         Over all six scenarios, Vulcan achieves only ∼7% smaller
would have to balance exploration and exploitation when              savings than unconstrained search, demonstrating that its
choosing regions.                                                    constrained interfaces can express performant heuristics
   Template. Unlike the single-region case study, this task          while guaranteeing execution safety.
does not directly fit the semantics of either Rank or Value:
the scheduler output at each tick is a 2-tuple of (action, re-       7.2    Cache Eviction
gion). We therefore decompose decision-making into two               Cache eviction is central to performance in CDNs [9, 14, 38,
parts. First, a Value function, invoked once per scheduler           69, 91, 109] and in-memory stores [61, 79]. As §2.1 showed,
tick, chooses the action: use spot instances in the current re-      access patterns and object characteristics vary substantially
gion, use on-demand instances in the current region, migrate         across deployments, making instance-specialized eviction
to another region, or wait. Second, if a migration action is         heuristics valuable. Evicting an object from a pool of candi-
selected, a Rank function selects which region to migrate            dates maps naturally to a Rank task (§4.2): objects are scored
to. Although this region-choice could also be expressed as           by cache utility and the lowest-ranked object is evicted when
                     Cacheus          Sieve             LHD             LeCaR                               Cacheus              Sieve             LHD              LeCaR
                     LRU              S3-FIFO           GDSF            LRB                                 LRU                  S3-FIFO           GDSF             LRB
                          3L-Cache          Vulcan             Vulcan-NL                                         3L-Cache              Vulcan              Vulcan-NL
        WikiMedia (CDN)
                                                                                                   WikiMedia (CDN)
           Twitter (KV2)                                                                               Twitter (KV2)
           Twitter (KV1)                                                                               Twitter (KV1)




                                                                                           Trace
Trace




        Tencent (Object)                                                                           Tencent (Object)
           Meta (Block)                                                                                Meta (Block)
              Meta (KV)                                                                                   Meta (KV)
            Meta (CDN)                                                                                  Meta (CDN)
                                                                                                        MSR (Block)
            MSR (Block)
                       −0.36    0.0       0.1     0.2      0.3       0.4        0.5                               −0.1     0.0      0.1     0.2      0.3      0.4     0.5
                                     Miss Ratio Reduction from FIFO                                                         Miss Ratio Reduction from FIFO

                  (a) Large cache size (10%), objects of different sizes                                    (b) Small cache size (0.1%), objects of different sizes
Figure 8. Performance of instance-specialized heuristics versus baselines for two classes of instances. Additional results appear in Appendix B.


space is needed. We evaluate whether Vulcan can synthesize                                   Listing 3. Simplified snippets of evolved heuristics for MSR and
such heuristics for individual cache deployments.                                            Meta block traces: actual heuristics are 29 and 50 lines of code.
   Template. We expose a Rank scoring function over a                                  1     // MSR block trace
priority queue of cached objects; per-object metadata (age,                            2     freq     = 0.7*count + 0.3*EWMA(count, alpha=0.2)
                                                                                       3     size_pen = log2(size)
size, last access time, recent eviction history; see Table 6)1 is
                                                                                       4     ghost_mult = 1 + 2*ghost_count
stored in a libVulcan feature store available to the function.                         5     utility = (last_access/1e6 + 10*freq - size_pen) *
To reduce overhead, we use a lazy update strategy: scores are                                     ghost_mult
recomputed only when an object is accessed, not on every                               6

cache event.                                                                           7     // Meta block trace
                                                                                       8     intensity = count / (last_access - insert_time)
   Evaluator. We use libCacheSim [43] to simulate eight
                                                                                       9     freq       = log2(count) * (10*intensity)
deployment-specific traces from Microsoft [65], Meta [13],                            10     size_fac   = 1 / log2(size)
Twitter [107], Tencent [113], and Wikimedia [100]. For each                           11     ghost_bonus = 1000 * (1 + log2(ghost_count))
trace, we consider two cache sizes (10% and 0.1% of the trace                         12     utility    = (0.6*last_access + 400*freq) * size_fac +
footprint) and two object-size settings (uniform and variable),                                   ghost_bonus
yielding 32 instances total. During synthesis, candidates are
scored on the first 1M requests (with a timeout of 100 s to
encourage efficient heuristics); the final heuristic is evaluated                            best (GDSF) on the Meta CDN trace, and comes within 1%
over the full trace, measuring miss-ratio reduction (MRR)                                    of the best (LRB) on the MSR trace. On the MSR block trace,
over FIFO (§2).                                                                              the synthesized heuristic (Listing 3) blends raw access count
   Results. Our nine state-of-the-art eviction baselines                                     with an EWMA-smoothed count, using a ghost multiplier to
are GDSF [21], S3-FIFO [108], SIEVE [111], LHD [12],                                         emphasize recently evicted objects. For the Meta block trace,
Cacheus [80], LRB [91], 3L-Cache [114], LeCaR [96], and                                      it instead measures per-object access intensity and applies
LRU. We use ShinkaEvolve [51] as the code-generation                                         an additive penalty for ghost-list objects rather than a mul-
framework for generating heuristics for each of the 32 in-                                   tiplicative one. For the 0.1% cache configuration, Vulcan
stances described above. We also run an ablation where we                                    matches the performance of the best baseline (3L-Cache) on
disable listeners (named Vulcan-NL).                                                         the Tencent trace and comes within 1% of the best (GDSF) on
Overall results. Across the 32 instances, Vulcan-generated                                   the MSR block trace. Vulcan achieves over 2× lower miss
heuristics outperform all baselines in two instances and rank                                ratios than strong baselines such as SIEVE and S3-FIFO on
among the top three heuristics for 13 instances. Furthermore,                                specific instances: for instance, on the Twitter KV1 trace
Vulcan heuristics are within 1% of the best baseline on six                                  (0.1% cache size, variable object sizes) Vulcan’s miss ratio is
instances and within 5% on an additional six instances. A sin-                               35.4%, compared to 73.4% for SIEVE and 72.5% for S3-FIFO.
gle implementation achieves all these results automatically                                  On the Tencent object trace, Vulcan generates a GDSF-
after a one-time development effort.                                                         inspired heuristic similar to the MSR 10% case, fine-tuning
Breakdown of results. Figure 8a and Figure 8b show miss-                                     the constants for frequency and size to suit the Tencent work-
ratio improvements over FIFO for sixteen instances. For the                                  load and smaller cache. Detailed results for the remaining
10% cache configuration, Vulcan outperforms all baselines                                    instances are in §B.1 (Figure 12a and Figure 12b).
on the Meta block trace, matches the performance of the                                      Impact of listeners. Removing listeners only slightly de-
                                                                                             grades performance: Vulcan-NL still outperforms all the
1 Note that the caching template shown in Listing 1 was simplified for                       baselines on two instances but trails the full Vulcan by 0.84%
exposition and contains only two raw signals.                                                in average MRR. This difference is small for this use case
Table 7. Computational cost of eviction heuristics. Average                   Listing 4. Memory tiering heuristic synthesized by Vulcan.
(and range) of execution time to run a set of traces (scenarios) in a
                                                                        1   fs.add_listeners(accesses, {EWMA({0.95, 0.35})});
single-threaded simulator. Higher = more expensive.                     2   double score_fn(vulcan::store& fs, int64_t obj_id):
                                                                        3       double fast = fs.get_ewma(accesses, obj_id, 0.95);
Algorithm                                   Execution time vs. FIFO
                                                                        4       double slow = fs.get_ewma(accesses, obj_id, 0.35);
LRU                                                   1.0× (0.5–2.1×)   5       double accel = (slow > 0.001) ? (fast / slow) : 1.0;
SIEVE [111]                                           1.1× (0.6–2.0×)   6       return fast * (1.0 + 0.55 * min(accel, 2.5));
LeCaR [96]                                            1.8× (0.8–3.0×)
S3-FIFO [108]                                         2.1× (1.4–3.8×)
GDSF [21]                                             3.9× (2.5–7.1×)       approach instead: it computes per-page scores from multi-
Cacheus [80]                                          4.1× (2.3–7.9×)       timescale access averages, ranks pages by those scores, and
LHD [12]                                              4.1× (2.2–7.1×)
Vulcan                                             13.4× (7.4–22.5×)
                                                                            migrates the highest-ranked pages to DRAM.
3L-Cache [114]                                      14.4× (5.3–38.2×)          Template. We formulate the page migration problem as
LRB [91]                                         361.2× (19.8–614.6×)       a Rank task in Vulcan, similar to ARMS [103]: the goal is
                                                                            to estimate each page’s hotness and rank pages accordingly.
                                                                            The raw signals provided for this task include per-page ac-
                                                                            cess counts over a time window (500 ms) and the observed
since eviction heuristics are invoked extremely frequently,                 bandwidths of the hot and cold tiers. The developer-written
making complex listeners prohibitively expensive; compu-                    template invokes libVulcan’s Rank every 1 s.
tationally heavy heuristics are likelier to time out during                    Evaluator. We score candidate heuristics by running a
evolution, biasing the search towards simpler listeners.                    single workload on a two-tier memory emulator. The emula-
Cost of synthesis. Across all 32 instances, synthesis cost                  tor runs on a dual-socket Xeon CloudLab [24] c220g5 node:
$272 for LLM calls (≈ 36.5M input, 8.6M output tokens) and                  the near tier is socket 0’s DRAM, and the far tier is socket 1’s
consumed 85 CPU-hours to evaluate candidate solutions.                      DRAM with its uncore frequency – the clock governing the
Runtime cost of Vulcan heuristics. Table 7 shows that                       mesh interconnect, last-level cache, and memory controllers –
Vulcan policies’ runtime overhead is comparable to that of                  clamped to the minimum ratio. This inflates remote-access la-
3L-Cache [114], with which our policies are very competi-                   tency to emulate that of CXL-attached memory, while avoid-
tive. Additionally, LRB [91], which outperforms Vulcan in                   ing the cost of running heuristic search directly on scarce
six instances, takes 27× as long as Vulcan on average. Vul-                 CXL hardware. After synthesis, we analyze whether the re-
can’s cost can be reduced further by sampling: for instance,                sulting heuristic generalizes to other workloads by testing it
approximating the Vulcan eviction policy for Meta KV with                   on our CXL-based testbed.
variable object sizes (10% cache size) using 𝑘 = 5 samples                  Evolution setup. We seed the search with a “promote noth-
reduces the cost from 15× FIFO to 5× FIFO while largely                     ing” heuristic that scores every page as 0 (i.e., no migra-
preserving miss rates.                                                      tions happen). We then run OpenEvolve [87] for 100 itera-
                                                                            tions, where heuristic candidates are scored by their end-to-
                                                                            end goodput on a specific application; we then use the best
7.3   Memory Tiering                                                        heuristic in the generalization study.
Memory tiering expands effective memory capacity by plac-                   Generalization to real CXL hardware and unseen work-
ing pages across fast local DRAM and slower tiers such as                   loads. We take this single heuristic synthesized against a
CXL-attached memory or NVM. The central policy problem                      single application on an emulator and, without further tun-
is deciding which pages should occupy scarce DRAM: ideally,                 ing, evaluate it on a real CXL machine across a diverse set
frequently accessed pages should be promoted to DRAM,                       of workloads. Our experimental setup pairs a dual-socket
while colder pages remain in slower tiers. We use Vulcan                    Xeon host with a Micron CZ120 CXL 2.0 memory expander
to synthesize page promotion heuristics and seek to answer                  (256 GiB), connected to socket 0 over PCIe Gen5 x8 and
whether they generalize from an emulated tiered-memory                      exposed as a CPU-less NUMA node. The test workloads
setup to real CXL hardware.                                                 span three domains: GUPS [74] (memory microbenchmark
   Manually designed heuristics. Existing memory tier-                      used for training), GapBS Betweenness Centrality and PageR-
ing systems [53, 59, 78, 103] use sampled access information                ank [11] (graph analytics), and Silo TPCC [95] (in-memory
– from mechanisms such as Intel PEBS [39] or page-table                     database). All results are reported normalized to ARMS [103].
accessed-bit scanning [72] – to estimate page hotness and                      Results. Listing 4 shows the synthesized heuristic, Vul-
migrate pages accordingly. Memtis [53] represents one class                 can-GUPS, which used the GUPS benchmark [74] as the eval-
of designs: it promotes pages whose sampled access count                    uator. Figure 9 shows its performance on the CXL testbed.
exceeds a dynamically adjusted hotness threshold and de-                    From Listing 4, we observe that the heuristic uses the ratio
motes pages once their cooled access counts fall below it.                  of two EWMAs to derive a metric called the acceleration,
ARMS [103] represents another class, using a ranking-based                  which it uses to make promotion decisions. We observe that
                                                                           Table 8. Developer effort to set up templates.

                                                                                    Spot VM      Spot VM      Cache       Memory
                                                                  Metric
                                                                                     (single)     (multi)    eviction     tiering
                                                                  Raw signals          8            11           6           3
                                                                  Template (LoC)       62          104          74           72



Figure 9. Performance of the Vulcan-synthesized heuristic com-
pared with the no-op seed heuristic.
                                                                     Setting up the template requires developers to specify
                                                                  which raw signals are available to the policy, configure a
                                                                  libVulcan feature store to collect and update these signals,
                                                                  and recast the policy’s decision logic using Rank/Value(§4).
                                                                  Table 8 quantifies this setup effort for the use cases we study.
                                                                     Table 8 shows that this refactoring is a modest one-time
                                                                  cost: our case studies required exposing only 3–11 raw sig-
                                                                  nals and writing 62–104 lines of task-specific code for the
                                                                  template. This effort is then amortized across instances re-
                                                                  quiring specialization. For example, in cache eviction (§7.2),
                                                                  the same 74-line template was reused to synthesize heuristics
    Figure 10. Generalization of Vulcan-synthesized heuristics.   for all 32 instances.
                                                                     This fixed synthesis boundary also makes synthesized ar-
                                                                  tifacts more predictable: every heuristic implements the pre-
this synthesized heuristic outperforms ARMS by 14.2% on           defined Rank or Value interface and operates over the same
GUPS on CXL and matches the performance of ARMS on all            declared signals. Thus, even when a developer chooses to in-
other workloads, showing that heuristics synthesized on an        spect a synthesized heuristic in Vulcan, they already know
emulator can generalize to real hardware.                         the shape of what they are looking at, substantially reducing
   In Figure 10, we repeat this experiment, using other work-     the effort required to review each synthesized heuristic.
loads for training during evolution to obtain heuristics Vul-
can-GapBC and Vulcan-Silo. We observe that all three              8.2 Vulcan’s Rank and Value Interfaces
heuristics meet or exceed the performance of ARMS for
GapPR, GUPS, and Silo workloads. The only exception to            8.2.1 Scope and Limitations. While our interfaces cap-
this trend is Vulcan-GapBC, which only achieves 0.96× the         ture the core decision logic of a broad class of systems policies
performance of ARMS on its training workload of GapBC;            (Table 1), we do not claim they are universal. More complex
we hypothesize that this could be because GapBS-BC is a           problems can often be decomposed into Rank and Value
workload that performs breadth-first search over a graph,         subproblems: as we demonstrate in our multi-region spot-
and hence can produce random pointer-chasing patterns.            VM case study (§7.1.2), a Value function decides whether
Such patterns may not be well captured by heuristics that         to migrate, and a Rank function then selects the destina-
score pages individually. Synthesizing these heuristics cost      tion region only if the first policy chooses to migrate. Such
$36 in LLM calls (5.8M input, 0.9M output tokens) and re-         decompositions, however, impose explicit structure on how
quired a combined total of 7.8 node-hours on our emulated         sub-policies interact: in this setting, the first policy cannot
CXL setup.                                                        decide to migrate because an attractive destination exists. As
                                                                  the number of coupled decisions grows, decomposing them
                                                                  into separate components requires increasingly elaborate
8     Discussion
                                                                  coordination between them. For recurring patterns of this
8.1    Developer Effort in Vulcan                                 kind, extending Vulcan with new interfaces may provide
Vulcan changes not only the amount of developer effort            cleaner abstractions than further composition.
required for synthesis but also when that effort is incurred.
With unconstrained synthesis, each synthesized heuristic is       8.2.2 Extending Vulcan with New Interfaces. The key
a new free-form implementation: before deployment, a devel-       requirement for a new interface is that its synthesized de-
oper must determine where changes were introduced, which          cision logic remain stateless. This preserves Anvil’s delib-
external systems the heuristic interacts with, and whether        erately restrictive design: synthesized programs cannot al-
those interactions are correct. With Vulcan, developers in-       locate heap memory or maintain persistent mutable state,
stead define this external-facing boundary before the search      enabling strong execution-safety guarantees by construc-
begins, through the template.                                     tion. For example, a new COMPARE interface could choose
between two alternatives based on their features jointly, un-       system-integration problems that arise with unrestricted
like Rank, which scores each candidate independently. Simi-         code generation.
larly, a CLASSIFY interface could return an element from a             More broadly, Vulcan’s results suggest that safe synthesis
finite set of actions directly, rather than encoding categorical    need not come at the cost of meaningful policy exploration.
choices through Value’s scalar output. More generally, recur-       An important next step is to explore how far this boundary
ring decision abstractions that admit stateless decision logic      can be expanded, for example by using stronger end-to-end
could be incorporated into Vulcan as additional interfaces.         semantic verification to safely expose a larger synthesis sur-
                                                                    face. Another direction is to formalize what constitutes an in-
                                                                    stance in practice: when to synthesize a new heuristic rather
9    Related Work                                                   than reuse an existing one, what should trigger re-synthesis,
Traditional learning-based policies. Prior ML-based sys-            and how to handle transitions between policies.
tems policies, particularly neural policies [2, 50, 91, 104, 106,
114], have demonstrated that data-driven approaches can             11     Acknowledgements
outperform fixed heuristics on specific instances. However,
neural approaches introduce significant practical challenges:       This material is based upon work supported by the U.S.
opaque behavior that complicates debugging [62], complex            National Science Foundation (NSF) under Grant Number
training and deployment pipelines [3, 27], inference over-          2326576. This research was also supported by the InfraAI
                                                                    Center at The University of Texas at Austin. Dwivedula was
heads in the control path [27, 110], and safety concerns that
                                                                    supported by an Amazon AI Fellowship. We are also grateful
limit adoption [83]. Vulcan takes a different stance: it avoids
neural inference in the hot path entirely, confining learning       to our shepherd for their thoughtful feedback, which helped
to an offline search over small, interpretable LLM-generated        improve the clarity and presentation of this paper.
code snippets.
AI-driven algorithm and heuristic design. Recent work               References
has explored using LLMs to discover new heuristics via evo-           [1] Soheil Abbasloo, Yang Xu, and H Jonathan Chao. 2019. C2TCP: A
lutionary search [68, 81]. One line of work modifies exist-               flexible cellular TCP to meet stringent delay requirements. IEEE
ing human-designed algorithms incrementally, such as auto-                Journal on Selected Areas in Communications 37, 4 (2019), 918–932.
                                                                      [2] Soheil Abbasloo, Chen-Yu Yen, and H. Jonathan Chao. 2020. Clas-
matic BBR variants [20, 36]. A complementary line focuses on              sic Meets Modern: a Pragmatic Learning-Based Congestion Con-
search strategies: Glia [33] employs multiple specialized LLM             trol for the Internet. In Proceedings of the Annual Conference of the
agents, and Robusta [44] uses counterexamples to harden                   ACM Special Interest Group on Data Communication on the Applica-
candidate heuristics. As we show in §2.2, unconstrained ap-               tions, Technologies, Architectures, and Protocols for Computer Com-
proaches of this kind can produce safety and integration                  munication (Virtual Event, USA) (SIGCOMM ’20). Association for
                                                                          Computing Machinery, New York, NY, USA, 632–647. doi:10.1145/
bugs. These search strategies are complementary to Vulcan:                3387514.3405892
any of them, combined with Vulcan’s Rank and Value                    [3] Ibrahim Umit Akgun, Ali Selman Aydin, and Erez Zadok. 2020. KM-
interfaces and listeners, can yield similar benefits.                     LIB: Towards machine learning for operating systems. In Proceedings
Domain-specific languages for execution safety. Re-                       of the On-Device Intelligence Workshop, co-located with the MLSys
                                                                          Conference. 1–6.
stricted languages such as Rust and eBPF [28, 84] require
                                                                      [4] Mohammad Alizadeh, Albert Greenberg, David A. Maltz, Jitendra
complex verifiers and carry steep learning curves; even then,             Padhye, Parveen Patel, Balaji Prabhakar, Sudipta Sengupta, and Mu-
they do not enforce leak-freedom [28, 46], which is too re-               rari Sridharan. 2010. Data center TCP (DCTCP). In Proceedings of
strictive a guarantee for general programs. General-purpose               the ACM SIGCOMM 2010 Conference (New Delhi, India) (SIGCOMM
verifiers [52, 54] can encode execution-safety properties as              ’10). Association for Computing Machinery, New York, NY, USA,
pre- and post-conditions, but require substantial per-program             63–74. doi:10.1145/1851182.1851192
                                                                      [5] Ami Tavory and Vladimir Dreizin and Benjamin Kosnik. [n. d.].
annotation effort, including loop invariants, termination ar-             Policy-Based Data Structures. GNU C++ Library, libstdc++, GNU
guments, and framing conditions [35, 67]. Anvil takes the                 Project.        https://gcc.gnu.org/onlinedocs/libstdc++/ext/pb_ds/
opposite extreme: by restricting LLM-written code to simple               Accessed July 9, 2025.
stateless functions implementing Rank or Value, it ensures            [6] Anthropic. 2025. Claude Code: Best practices for agentic cod-
P1–P3 by construction without any annotations.                            ing. https://www.anthropic.com/engineering/claude-code-best-
                                                                          practices Accessed: 2026-04-08.
                                                                      [7] Anthropic. 2025.         Introducing Claude Opus 4.5.          https:
                                                                          //www.anthropic.com/news/claude-opus-4-5 Accessed: 2026-04-08.
10    Conclusion                                                      [8] Venkat Arun and Hari Balakrishnan. 2018. Copa: Practical Delay-
This paper presents Vulcan, a framework for synthesizing                  Based congestion control for the internet. In 15th USENIX Symposium
systems resource-management heuristics that are both per-                 on Networked Systems Design and Implementation (NSDI 18). USENIX
                                                                          Association, Renton, WA, 329–342.
formant and safe to deploy. Across three use cases, Vulcan            [9] Nirav Atre, Justine Sherry, Weina Wang, and Daniel S Berger. 2020.
discovers heuristics that are competitive with strong human-              Caching with delayed hits. In Proceedings of the Annual conference
designed baselines, while avoiding the execution-safety and               of the ACM Special Interest Group on Data Communication on the
     applications, technologies, architectures, and protocols for computer   [22] Mo Dong, Tong Meng, Doron Zarchy, Engin Arslan, Yossi Gilad,
     communication. 495–513.                                                      Brighten Godfrey, and Michael Schapira. 2018. PCC vivace: Online-
[10] Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk             Learning congestion control. In 15th USENIX symposium on networked
     Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry,            systems design and implementation (NSDI 18). 343–356.
     Quoc Le, et al. 2021. Program synthesis with large language models.     [23] Thaleia Dimitra Doudali, Sergey Blagodurov, Abhinav Vishnu, Sud-
     arXiv preprint arXiv:2108.07732 (2021).                                      hanva Gurumurthi, and Ada Gavrilovska. 2019. Kleio: A Hybrid
[11] Scott Beamer, Krste Asanović, and David Patterson. 2015. The GAP             Memory Page Scheduler with Machine Intelligence. In Proceedings
     benchmark suite. arXiv preprint arXiv:1508.03619 (2015).                     of the 28th International Symposium on High-Performance Parallel
[12] Nathan Beckmann, Haoxian Chen, and Asaf Cidon. 2018. LHD: Im-                and Distributed Computing (Phoenix, AZ, USA) (HPDC ’19). Associa-
     proving cache hit rate by maximizing hit density. In 15th USENIX             tion for Computing Machinery, New York, NY, USA, 37–48. doi:10.
     Symposium on Networked Systems Design and Implementation (NSDI               1145/3307681.3325398
     18). USENIX Association, Renton, WA, 389–403. https://www.usenix.       [24] Dmitry Duplyakin, Robert Ricci, Aleksander Maricq, Gary Wong,
     org/conference/nsdi18/presentation/beckmann                                  Jonathon Duerig, Eric Eide, Leigh Stoller, Mike Hibler, David Johnson,
[13] Benjamin Berg, Daniel S Berger, Sara McAllister, Isaac Grosof, Sathya        Kirk Webb, et al. 2019. The design and operation of CloudLab. In
     Gunasekar, Jimmy Lu, Michael Uhlar, Jim Carrig, Nathan Beckmann,             2019 USENIX annual technical conference (USENIX ATC 19). 1–14.
     Mor Harchol-Balter, et al. 2020. The CacheLib caching engine: Design    [25] Rohit Dwivedula, Divyanshu Saxena, Aditya Akella, Swarat Chaud-
     and experiences at scale. In 14th USENIX Symposium on Operating Sys-         huri, and Daehyeok Kim. 2025. Man-Made Heuristics Are Dead. Long
     tems Design and Implementation (OSDI 20). USENIX Association, 753–           Live Code Generators!. In Proceedings of the 24th ACM Workshop
     768. https://www.usenix.org/conference/osdi20/presentation/berg              on Hot Topics in Networks. 51–60.
[14] Daniel S Berger, Benjamin Berg, Timothy Zhu, Siddhartha Sen, and        [26] Gil Einziger, Roy Friedman, and Ben Manes. 2017. Tinylfu: A highly
     Mor Harchol-Balter. 2018. RobinHood: Tail Latency Aware Caching–             efficient cache admission policy. ACM Transactions on Storage (ToS)
     Dynamic Reallocation from Cache-Rich to Cache-Poor. In 13th                  13, 4 (2017), 1–31.
     USENIX Symposium on Operating Systems Design and Implementation         [27] Henrique Fingler, Isha Tarte, Hangchen Yu, Ariel Szekely, Bodun Hu,
     (OSDI 18). USENIX Association, Carlsbad, CA, 195–212.                        Aditya Akella, and Christopher J. Rossbach. 2023. Towards a Machine
[15] Zhuohang Bian, Feiyang Wu, Teng Ma, and Youwei Zhuo. 2025. To-               Learning-Assisted Kernel with LAKE. In Proceedings of the 28th ACM
     kencake: A KV-Cache-centric Serving Framework for LLM-based                  International Conference on Architectural Support for Programming
     Multi-Agent Applications. arXiv preprint arXiv:2510.18586 (2025).            Languages and Operating Systems, Volume 2 (Vancouver, BC, Canada)
[16] Aaron Blankstein, Siddhartha Sen, and Michael J Freedman. 2017.              (ASPLOS 2023). Association for Computing Machinery, New York,
     Hyperbolic caching: Flexible caching for web applications. In 2017           NY, USA, 846–861. doi:10.1145/3575693.3575697
     USENIX Annual Technical Conference (USENIX ATC 17). 499–511.            [28] Bolaji Gbadamosi, Luigi Leonardi, Tobias Pulls, Toke Høiland-
[17] Neal Cardwell, Yuchung Cheng, C Stephen Gunn, Soheil Hassas                  Jørgensen, Simone Ferlin-Reiter, Simo Sorce, and Anna Brunström.
     Yeganeh, and Van Jacobson. 2017. BBR: Congestion-based congestion            2024. The ebpf runtime in the linux kernel. arXiv preprint
     control. Commun. ACM 60, 2 (2017), 58–66.                                    arXiv:2410.00026 (2024).
[18] Jiayi Chen, Nihal Sharma, Tarannum Khan, Shu Liu, Brian Chang,          [29] P. Goyal, H.M. Vin, and Haichen Cheng. 1997. Start-time fair queue-
     Aditya Akella, Sanjay Shakkottai, and Ramesh K Sitaraman. 2023.              ing: a scheduling algorithm for integrated services packet switch-
     Darwin: Flexible Learning-based CDN Caching. In Proceedings of               ing networks. IEEE/ACM Transactions on Networking 5, 5 (1997),
     the ACM SIGCOMM 2023 Conference (New York, NY, USA) (ACM                     690–704. doi:10.1109/90.649569
     SIGCOMM ’23). Association for Computing Machinery, New York,            [30] Robert Grandl, Mosharaf Chowdhury, Aditya Akella, and Ganesh
     NY, USA, 981–999. doi:10.1145/3603269.3604863                                Ananthanarayanan. 2016. Altruistic Scheduling in Multi-Resource
[19] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Hen-                       Clusters. In 12th USENIX Symposium on Operating Systems Design and
     rique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri             Implementation (OSDI 16). USENIX Association, Savannah, GA, 65–
     Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri,                  80. https://www.usenix.org/conference/osdi16/technical-sessions/
     Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry,               presentation/grandl_altruistic
     Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail            [31] Robert Grandl, Srikanth Kandula, Sriram Rao, Aditya Akella,
     Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens             and Janardhan Kulkarni. 2016.            GRAPHENE: Packing and
     Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings,                Dependency-Aware Scheduling for Data-Parallel Clusters. In
     Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-         12th USENIX Symposium on Operating Systems Design and Im-
     Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak,           plementation (OSDI 16). USENIX Association, Savannah, GA,
     Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William             81–97.         https://www.usenix.org/conference/osdi16/technical-
     Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh                 sessions/presentation/grandl_graphene
     Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew              [32] Sangtae Ha, Injong Rhee, and Lisong Xu. 2008. CUBIC: a new TCP-
     Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder,            friendly high-speed TCP variant. ACM SIGOPS operating systems
     Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and                review 42, 5 (2008), 64–74.
     Wojciech Zaremba. 2021. Evaluating Large Language Models Trained        [33] Pouya Hamadanian, Pantea Karimi, Arash Nasr-Esfahany, Kimia
     on Code. arXiv:2107.03374 [cs.LG] https://arxiv.org/abs/2107.03374           Noorbakhsh, Joseph Chandler, Ali ParandehGheibi, Mohammad Al-
[20] Audrey Cheng, Shu Liu, Melissa Pan, Zhifei Li, Shubham Agarwal,              izadeh, and Hari Balakrishnan. 2025. Glia: A Human-Inspired AI
     Mert Cemri, Bowen Wang, Alexander Krentsel, Tian Xia, Jongseok               for Automated Systems Design and Optimization. arXiv preprint
     Park, et al. 2025. Let the Barbarians In: How AI Can Accelerate Sys-         arXiv:2510.27176 (2025).
     tems Performance Research. arXiv preprint arXiv:2512.14806 (2025).      [34] Mingzhe Hao, Levent Toksoz, Nanqinqin Li, Edward Edberg Halim,
[21] Ludmila Cherkasova. 1998. Improving WWW proxies performance                  Henry Hoffmann, and Haryadi S Gunawi. 2020. LinnOS: Predictabil-
     with greedy-dual-size-frequency caching policy. Hewlett-Packard              ity on unpredictable flash storage with a light neural network. In 14th
     Laboratories, Palo Alto, CA, USA.                                            USENIX Symposium on Operating Systems Design and Implementation
                                                                                  (OSDI 20). 173–190.
[35] Chris Hawblitzel, Jon Howell, Manos Kapritsos, Jacob R Lorch, Bryan              Systems (Rotterdam, Netherlands) (EuroSys ’25). Association for Com-
     Parno, Michael L Roberts, Srinath Setty, and Brian Zill. 2015. IronFleet:        puting Machinery, New York, NY, USA, 1109–1125. doi:10.1145/
     proving practical distributed systems correct. In Proceedings of the             3689031.3717496
     25th Symposium on Operating Systems Principles. 1–17.                       [51] Robert Tjarko Lange, Yuki Imajuku, and Edoardo Cetin. 2025. Shinkae-
[36] Zhiyuan He, Aashish Gottipati, Lili Qiu, Yuqing Yang, and Francis Y              volve: Towards open-ended and sample-efficient program evolution.
     Yan. 2025. Congestion Control System Optimization with Large                     arXiv preprint arXiv:2509.19349 (2025).
     Language Models. arXiv preprint arXiv:2508.16074 (2025).                    [52] Andrea Lattuada, Travis Hance, Jay Bosamiya, Matthias Brun, Chan-
[37] Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika,                   hee Cho, Hayley LeBlanc, Pranav Srinivasan, Reto Achermann, Tej
     Akul Arora, Ethan Guo, Collin Burns, Samir Puranik, Horace He,                   Chajed, Chris Hawblitzel, et al. 2024. Verus: A practical founda-
     Dawn Song, et al. 2021. Measuring coding challenge competence                    tion for systems verification. In Proceedings of the ACM SIGOPS 30th
     with apps. arXiv preprint arXiv:2105.09938 (2021).                               Symposium on Operating Systems Principles. 438–454.
[38] Qi Huang, Ken Birman, Robbert Van Renesse, Wyatt Lloyd, Sanjeev             [53] Taehyung Lee, Sumit Kumar Monga, Changwoo Min, and Young Ik
     Kumar, and Harry C Li. 2013. An analysis of Facebook photo caching.              Eom. 2023. MEMTIS: Efficient Memory Tiering with Dynamic Page
     In Proceedings of the Twenty-Fourth ACM Symposium on Operating                   Classification and Page Size Determination. In Proceedings of the 29th
     Systems Principles. 167–181.                                                     Symposium on Operating Systems Principles.
[39] Intel Corporation. 2018. Intel 64 and IA-32 Architectures Software          [54] K Rustan M Leino and Michał Moskal. 2014. Co-induction simply:
     Developer Manuals. https://software.intel.com/articles/intel-sdm                 Automatic co-inductive proofs in a program verifier. In International
[40] Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun                  Symposium on Formal Methods. Springer, 382–398.
     Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and                    [55] Jianheng Ling, Pratik Worah, Yawen Wang, Yunchuan Kong, An-
     Ion Stoica. 2024. Livecodebench: Holistic and contamination free                 shul Kapoor, Chunlei Wang, Clifford Stein, Diwakar Gupta, Jason
     evaluation of large language models for code. arXiv preprint                     Behmer, Logan A. Bush, Prakash Ramanan, Rajesh Kumar, Thomas
     arXiv:2403.07974 (2024).                                                         Chestna, Yajing Liu, Ying Liu, Ye Zhao, Kathryn S. McKinley, Meey-
[41] Wenzel Jakob. 2024. pybind11 Documentation.                                      oung Park, and Martin Maas. 2025. LAVA: Lifetime-Aware VM Allo-
[42] Theodore Johnson and Dennis Shasha. 1994. 2Q: A Low Overhead                     cation with Learned Distributions and Adaptation to Mispredictions.
     High Performance Buffer Management Replacement Algorithm. In                     arXiv:2412.09840 [cs.DC] https://arxiv.org/abs/2412.09840
     Proceedings of the 20th International Conference on Very Large Data         [56] Shutian Luo, Huanle Xu, Chengzhi Lu, Kejiang Ye, Guoyao Xu, Liping
     Bases (VLDB ’94). Morgan Kaufmann Publishers Inc., San Francisco,                Zhang, Yu Ding, Jian He, and Chengzhong Xu. 2021. Characterizing
     CA, USA, 439–450.                                                                Microservice Dependency and Performance: Alibaba Trace Analysis.
[43] Juncheng Yang (1a1a11a). 2023. libCacheSim: a high performance                   In Proceedings of the ACM Symposium on Cloud Computing (Seattle,
     library for building cache simulators. https://github.com/1a1a11a/               WA, USA) (SoCC ’21). Association for Computing Machinery, New
     libCacheSim. Accessed: 2025-06-28.                                               York, NY, USA, 412–426. doi:10.1145/3472883.3487003
[44] Pantea Karimi, Dany Rouhana, Pooria Namyar, Siva Kesava Reddy               [57] Mark Mansi, Bijan Tabatabai, and Michael M. Swift. 2022. CBMM:
     Kakarla, Venkat Arun, and Behnaz Arzani. 2025. Robust Heuristic                  Financial Advice for Kernel Memory Managers. In 2022 USENIX An-
     Algorithm Design with LLMs. arXiv preprint arXiv:2510.08755 (2025).              nual Technical Conference (USENIX ATC 22). USENIX Association,
[45] Mohammed F Kharma, Soohyeon Choi, Mohammad Alkhanafseh,                          Carlsbad, CA, 593–608. https://www.usenix.org/conference/atc22/
     and David Mohaisen. 2026. Security and quality in llm-generated                  presentation/mansi
     code: A multi-language, multi-model analysis. IEEE Transactions on          [58] Hongzi Mao, Malte Schwarzkopf, Shaileshh Bojja Venkatakrishnan,
     Dependable and Secure Computing (2026).                                          Zili Meng, and Mohammad Alizadeh. 2019. Learning scheduling
[46] Steve Klabnik, Carol Nichols, and Chris Krycho. [n. d.]. Reference Cy-           algorithms for data processing clusters. In Proceedings of the ACM
     cles Can Leak Memory. In The Rust Programming Language. Chapter                  Special Interest Group on Data Communication (Beijing, China) (SIG-
     15.6. Rust 1.90.0, Edition 2024. Accessed: 2026-05-08.                           COMM ’19). Association for Computing Machinery, New York, NY,
[47] Kubernetes. [n. d.]. Horizontal Pod Autoscale. https://kubernetes.io/            USA, 270–288. doi:10.1145/3341302.3342080
     docs/tasks/run-application/horizontal-pod-autoscale/. Accessed:             [59] Hasan Al Maruf, Hao Wang, Abhishek Dhanotia, Johannes Weiner,
     Dec 2025.                                                                        Niket Agarwal, Pallab Bhattacharya, Chris Petersen, Mosharaf
[48] Gautam Kumar, Nandita Dukkipati, Keon Jang, Hassan M. G. Was-                    Chowdhury, Shobhit Kanaujia, and Prakash Chauhan. 2023. TPP:
     sel, Xian Wu, Behnam Montazeri, Yaogong Wang, Kevin Spring-                      Transparent page placement for CXL-enabled tiered-memory. In
     born, Christopher Alfeld, Michael Ryan, David Wetherall, and Amin                Proceedings of the 28th ACM International Conference on Architectural
     Vahdat. 2020. Swift: Delay is Simple and Effective for Congestion                Support for Programming Languages and Operating Systems.
     Control in the Datacenter. In Proceedings of the Annual Conference          [60] Nimrod Megiddo and Dharmendra S Modha. 2003. ARC: A Self-
     of the ACM Special Interest Group on Data Communication on the                   Tuning, low overhead replacement cache. In 2nd USENIX Conference
     Applications, Technologies, Architectures, and Protocols for Computer            on File and Storage Technologies (FAST 03). USENIX Association, San
     Communication (Virtual Event, USA) (SIGCOMM ’20). Association                    Francisco, CA, USA.
     for Computing Machinery, New York, NY, USA, 514–528. doi:10.                [61] Memcached. [n. d.]. Memcached - a distributed memory object
     1145/3387514.3406591                                                             caching system. http://memcached.org/. Accessed: 2026-04-22.
[49] Mayuresh Kunjir, Brandon Fain, Kamesh Munagala, and Shivnath                [62] Zili Meng, Minhu Wang, Jiasong Bai, Mingwei Xu, Hongzi Mao, and
     Babu. 2017. ROBUS: fair cache allocation for data-parallel work-                 Hongxin Hu. 2020. Interpreting Deep Learning-Based Networking
     loads. In Proceedings of the 2017 ACM International Conference on                Systems. In Proceedings of the Annual Conference of the ACM Special
     Management of Data. Association for Computing Machinery, New                     Interest Group on Data Communication on the Applications, Technolo-
     York, NY, USA, 219–234.                                                          gies, Architectures, and Protocols for Computer Communication (Virtual
[50] Daniar H. Kurniawan, Rani Ayu Putri, Peiran Qin, Kahfi S. Zulkifli,              Event, USA) (SIGCOMM ’20). Association for Computing Machinery,
     Ray A. O. Sinurat, Janki Bhimani, Sandeep Madireddy, Achmad Imam                 New York, NY, USA, 154–171. doi:10.1145/3387514.3405859
     Kistijantoro, and Haryadi S. Gunawi. 2025. Heimdall: Optimizing             [63] Pierre Michaud. 2016. Best-offset hardware prefetching. In 2016 IEEE
     Storage I/O Admission with Extensive Machine Learning Pipeline.                  International Symposium on High Performance Computer Architecture
     In Proceedings of the Twentieth European Conference on Computer                  (HPCA). IEEE, 469–480.
[64] Radhika Mittal, Vinh The Lam, Nandita Dukkipati, Emily Blem, Has-          [78] Amanda Raybuck, Tim Stamler, Wei Zhang, Mattan Erez, and Simon
     san Wassel, Monia Ghobadi, Amin Vahdat, Yaogong Wang, David                     Peter. 2021. Hemem: Scalable tiered memory management for big
     Wetherall, and David Zats. 2015. TIMELY: RTT-based Congestion                   data applications and real nvm. In Proceedings of the ACM SIGOPS
     Control for the Datacenter. In Proceedings of the 2015 ACM Conference           28th Symposium on Operating Systems Principles. 392–407.
     on Special Interest Group on Data Communication (London, United            [79] Redis. [n. d.]. Redis - an in-memory data structure store, used
     Kingdom) (SIGCOMM ’15). Association for Computing Machinery,                    as a database, cache, and message broker.               https://redis.io/.
     New York, NY, USA, 537–550. doi:10.1145/2785956.2787510                         Accessed: 2026-04-22.
[65] Dushyanth Narayanan, Austin Donnelly, and Antony Rowstron. 2008.           [80] Liana V Rodriguez, Farzana Yusuf, Steven Lyons, Eysler Paz, Raju Ran-
     Write off-loading: Practical power management for enterprise storage.           gaswami, Jason Liu, Ming Zhao, and Giri Narasimhan. 2021. Learning
     ACM Transactions on Storage (TOS) 4, 3 (2008), 1–23.                            cache replacement with CACHEUS. In 19th USENIX Conference on File
[66] Deepak Narayanan, Keshav Santhanam, Fiodar Kazhamiaka, Amar                     and Storage Technologies (FAST 21). USENIX Association, 341–354.
     Phanishayee, and Matei Zaharia. 2020. Heterogeneity-Aware                  [81] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander
     Cluster Scheduling Policies for Deep Learning Workloads. In 14th                Novikov, Matej Balog, M Pawan Kumar, Emilien Dupont, Francisco JR
     USENIX Symposium on Operating Systems Design and Implementation                 Ruiz, Jordan S Ellenberg, Pengming Wang, Omar Fawzi, et al. 2024.
     (OSDI 20). USENIX Association, 481–498. https://www.usenix.org/                 Mathematical discoveries from program search with large language
     conference/osdi20/presentation/narayanan-deepak                                 models. Nature 625, 7995 (2024), 468–475.
[67] Luke Nelson, Helgi Sigurbjarnarson, Kaiyuan Zhang, Dylan Johnson,          [82] Marta Rybczyńska. 2021. Introducing maple trees. LWN.net. https:
     James Bornholt, Emina Torlak, and Xi Wang. 2017. Hyperkernel:                   //lwn.net/Articles/845507/ Accessed: 2026-03-22.
     Push-button verification of an OS kernel. In Proceedings of the 26th       [83] Divyanshu Saxena, Jiayi Chen, Sujay Yadalam, Yeonju Ro, Rohit
     Symposium on Operating Systems Principles. 252–269.                             Dwivedula, Eric H Campbell, Aditya Akella, Christopher J Rossbach,
[68] Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Emilien Dupont,                and Michael Swift. 2025. How I learned to stop worrying and love
     Po-Sen Huang, Adam Zsolt Wagner, Sergey Shirobokov, Borislav                    learned OS policies. In Proceedings of the 2025 Workshop on Hot Topics
     Kozlovskii, Francisco J. R. Ruiz, Abbas Mehrabian, M. Pawan Ku-                 in Operating Systems. Association for Computing Machinery, New
     mar, Abigail See, Swarat Chaudhuri, George Holland, Alex Davies,                York, NY, USA, 1–7.
     Sebastian Nowozin, Pushmeet Kohli, and Matej Balog. 2025. Al-              [84] Matan Shachnai, Harishankar Vishwanathan, Srinivas Narayana, and
     phaEvolve: A coding agent for scientific and algorithmic discovery.             Santosh Nagarakatte. 2024. Fixing Latent Unsound Abstract Op-
     arXiv:2506.13131 [cs.AI] https://arxiv.org/abs/2506.13131                       erators in the eBPF Verifier of the Linux Kernel. In International
[69] Erik Nygren, Ramesh K Sitaraman, and Jennifer Sun. 2010. The aka-               Static Analysis Symposium. Springer, Springer Nature Switzerland,
     mai network: a platform for high-performance internet applications.             Cham, 386–406.
     ACM SIGOPS Operating Systems Review 44, 3 (2010), 2–19.                    [85] Mohammad Shahrad, Rodrigo Fonseca, Inigo Goiri, Gohar Chaudhry,
[70] Chandandeep Singh Pabla. 2009. Completely fair scheduler. Linux                 Paul Batum, Jason Cooke, Eduardo Laureano, Colby Tresness, Mark
     Journal 2009, 184 (2009), 4.                                                    Russinovich, and Ricardo Bianchini. 2020. Serverless in the Wild:
[71] Rangeet Pan, Ali Reza Ibrahimzada, Rahul Krishna, Divya Sankar,                 Characterizing and Optimizing the Serverless Workload at a Large
     Lambert Pouguem Wassi, Michele Merler, Boris Sobolev, Raju Pavu-                Cloud Provider. In 2020 USENIX Annual Technical Conference (USENIX
     luri, Saurabh Sinha, and Reyhaneh Jabbarvand. 2024. Lost in trans-              ATC 20). USENIX Association, 205–218. https://www.usenix.org/
     lation: A study of bugs introduced by large language models while               conference/atc20/presentation/shahrad
     translating code. In Proceedings of the IEEE/ACM 46th International        [86] Erfan Sharafzadeh, Raymond Matson, Jean Tourrilhes, Puneet Sharma,
     Conference on Software Engineering. 1–13.                                       and Soudeh Ghorbani. 2025. Self-Clocked Round-Robin Packet Sched-
[72] SeongJae Park, Yunjae Lee, and Heon Y Yeom. 2019. Profiling dynamic             uling. In 22nd USENIX Symposium on Networked Systems Design
     data access patterns with controlled overhead and quality. In Proceed-          and Implementation (NSDI 25). USENIX Association, Philadelphia,
     ings of the 20th International Middleware Conference Industrial Track.          PA, 1437–1465.
[73] Padmanabhan Pillai and Kang G Shin. 2001. Real-time dynamic                [87] Asankhaya Sharma. 2025. Openevolve: An Open-Source Evolution-
     voltage scaling for low-power embedded operating systems. In Pro-               ary Coding Agent. https://github.com/codelion/openevolve. Ac-
     ceedings of the eighteenth ACM symposium on Operating systems                   cessed: 2025-12-10.
     principles. 89–102.                                                        [88] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik
[74] Steven J Plimpton, Ron Brightwell, Courtenay Vaughan, Keith Un-                 Narasimhan, and Shunyu Yao. 2023. Reflexion: Language agents
     derwood, and Mike Davis. 2006. A simple synchronous distributed-                with verbal reinforcement learning. Advances in Neural Information
     memory algorithm for the HPCC RandomAccess benchmark. In 2006                   Processing Systems 36 (2023), 8634–8652.
     IEEE International Conference on Cluster Computing. IEEE, 1–7.             [89] Madhavapeddi Shreedhar and George Varghese. 1995. Efficient fair
[75] François Pottier and Yann Régis-Gianas. 2024.             Menhir: An            queueing using deficit round robin. In Proceedings of the conference
     LR(1) Parser Generator for OCaml.              https://gallium.inria.fr/        on Applications, technologies, architectures, and protocols for computer
     ~fpottier/menhir/                                                               communication. 231–242.
[76] Sriram Ramabhadran and Joseph Pasquale. 2003. Stratified round             [90] Ramneet Singh, Sathvik Joel, Abhav Mehrotra, Nalin Wadhwa,
     robin: A low complexity packet scheduler with bandwidth fairness                Ramakrishna Bairi, Aditya Kanade, and Nagarajan Natarajan. 2025.
     and bounded delay. In Proceedings of the 2003 conference on appli-              Code Researcher: Deep Research Agent for Large Systems Code and
     cations, technologies, architectures, and protocols for computer com-           Commit History. Technical Report MSR-TR-2025-34. Microsoft.
     munications. Association for Computing Machinery, New York, NY,                 https://www.microsoft.com/en-us/research/publication/code-
     USA, 239–250. doi:10.1145/863955.863983                                         researcher-deep-research-agent-for-large-systems-code-and-
[77] Muhammad Shihab Rashid, Christian Bock, Yuan Zhuang, Alexan-                    commit-history/
     der Buchholz, Tim Esler, Simon Valentin, Luca Franceschi, Mar-             [91] Zhenyu Song, Daniel S Berger, Kai Li, and Wyatt Lloyd. 2020. Learning
     tin Wistuba, Prabhu Teja Sivaprasad, Woo Jung Kim, et al. 2025.                 relaxed belady for content distribution network caching. In 17th
     SWE-PolyBench: A multi-language benchmark for repository level                  USENIX Symposium on Networked Systems Design and Implementation
     evaluation of coding agents. arXiv preprint arXiv:2504.08703 (2025).            (NSDI 20). USENIX Association, Santa Clara, CA, 529–544.
 [92] Zhenyu Song, Kevin Chen, Nikhil Sarda, Deniz Altınbüken, Eugene                engineering. Advances in Neural Information Processing Systems
      Brevdo, Jimmy Coleman, Xiao Ju, Pawel Jurczyk, Richard Schooler,               37 (2024), 50528–50652.
      and Ramki Gummadi. 2023. HALP: Heuristic aided learned preference        [106] Juncheng Yang, Ziming Mao, Yao Yue, and K. V. Rashmi. 2023.
      eviction policy for YouTube content delivery network. In 20th USENIX           GL-Cache: Group-level learning for efficient and high-performance
      Symposium on Networked Systems Design and Implementation (NSDI                 caching. In 21st USENIX Conference on File and Storage Technologies
      23). USENIX Association, Boston, MA, 1149–1163.                                (FAST 23). USENIX Association, Santa Clara, CA, 115–134. https:
 [93] Jovan Stojkovic, Chaojie Zhang, Íñigo Goiri, Esha Choukse, Hao-                //www.usenix.org/conference/fast23/presentation/yang-juncheng
      ran Qiu, Rodrigo Fonseca, Josep Torrellas, and Ricardo Bianchini.        [107] Juncheng Yang, Yao Yue, and K. V. Rashmi. 2020. A large scale anal-
      2025. TAPAS: Thermal- and Power-Aware Scheduling for LLM In-                   ysis of hundreds of in-memory cache clusters at Twitter. In 14th
      ference in Cloud Platforms. In Proceedings of the 30th ACM Interna-            USENIX Symposium on Operating Systems Design and Implementation
      tional Conference on Architectural Support for Programming Languages           (OSDI 20). USENIX Association, 191–208. https://www.usenix.org/
      and Operating Systems, Volume 2 (Rotterdam, Netherlands) (ASPLOS               conference/osdi20/presentation/yang
      ’25). Association for Computing Machinery, New York, NY, USA,            [108] Juncheng Yang, Yazhuo Zhang, Ziyue Qiu, Yao Yue, and Rashmi
      1266–1281. doi:10.1145/3676641.3716025                                         Vinayak. 2023. Fifo queues are all you need for cache eviction. In
 [94] Jovan Stojkovic, Chaojie Zhang, Íñigo Goiri, Josep Torrellas, and Esha         Proceedings of the 29th Symposium on Operating Systems Principles.
      Choukse. 2025. DynamoLLM: Designing LLM Inference Clusters                     Association for Computing Machinery, New York, NY, USA, 130–149.
      for Performance and Energy Efficiency. In 2025 IEEE International        [109] Tzu-Wei Yang, Seth Pollen, Mustafa Uysal, Arif Merchant, and Homer
      Symposium on High Performance Computer Architecture (HPCA). 1348–              Wolfmeister. 2022. CacheSack: Admission Optimization for Google
      1362. doi:10.1109/HPCA61900.2025.00102                                         Datacenter Flash Caches. In 2022 USENIX Annual Technical Conference
 [95] Stephen Tu, Wenting Zheng, Eddie Kohler, Barbara Liskov, and                   (USENIX ATC 22). USENIX Association, Carlsbad, CA, 1021–1036.
      Samuel Madden. 2013. Speedy transactions in multicore in-memory          [110] Junxue Zhang, Chaoliang Zeng, Hong Zhang, Shuihai Hu, and Kai
      databases. In Proceedings of the Twenty-Fourth ACM Symposium                   Chen. 2022. LiteFlow: towards high-performance adaptive neural
      on Operating Systems Principles. 18–32.                                        networks for kernel datapath. In Proceedings of the ACM SIGCOMM
 [96] Giuseppe Vietri, Liana V. Rodriguez, Wendy A. Martinez, Steven                 2022 Conference (Amsterdam, Netherlands) (SIGCOMM ’22). Asso-
      Lyons, Jason Liu, Raju Rangaswami, Ming Zhao, and Giri Narasimhan.             ciation for Computing Machinery, New York, NY, USA, 414–427.
      2018. Driving Cache Replacement with ML-based LeCaR. In 10th                   doi:10.1145/3544216.3544229
      USENIX Workshop on Hot Topics in Storage and File Systems (HotStor-      [111] Yazhuo Zhang, Juncheng Yang, Yao Yue, Ymir Vigfusson, and K.V.
      age 18). USENIX Association, Boston, MA. https://www.usenix.org/               Rashmi. 2024. SIEVE is Simpler than LRU: an Efficient Turn-Key
      conference/hotstorage18/presentation/vietri                                    Eviction Algorithm for Web Caches. In 21st USENIX Symposium on
 [97] Carl A Waldspurger, Nohhyun Park, Alexander Garthwaite, and Ir-                Networked Systems Design and Implementation (NSDI 24). USENIX
      fan Ahmad. 2015. Efficient MRC construction with SHARDS. In                    Association, Santa Clara, CA, 1229–1246. https://www.usenix.org/
      13th USENIX Conference on File and Storage Technologies (FAST 15).             conference/nsdi24/presentation/zhang-yazhuo
      USENIX Association, 95–110.                                              [112] Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang,
 [98] Xingyao Wang, Yangyi Chen, Lifan Yuan, Yizhe Zhang, Yunzhu Li,                 and Yu-Xiong Wang. 2023. Language agent tree search unifies rea-
      Hao Peng, and Heng Ji. 2024. Executable code actions elicit better llm         soning acting and planning in language models. arXiv preprint
      agents. In Forty-first International Conference on Machine Learning.           arXiv:2310.04406 (2023).
 [99] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei              [113] Ke Zhou, Si Sun, Hua Wang, Ping Huang, Xubin He, Rui Lan, Wenyan
      Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. 2022. Chain-of-thought              Li, Wenjie Liu, and Tianming Yang. 2018. Demystifying Cache Policies
      prompting elicits reasoning in large language models. Advances in              for Photo Stores at Scale: A Tencent Case Study. In Proceedings of
      neural information processing systems 35 (2022), 24824–24837.                  the 2018 International Conference on Supercomputing (Beijing, China)
[100] Wikimedia Foundation. [n. d.].          WikiMedia Cache Dataset.               (ICS ’18). Association for Computing Machinery, New York, NY, USA,
      https://wikitech.wikimedia.org/wiki/Data_Platform/Data_Lake/                   284–294. doi:10.1145/3205289.3205299
      Traffic/Caching. Accessed: 2025-05-14.                                   [114] Wenbin Zhou, Zhixiong Niu, Yongqiang Xiong, Juan Fang, and Qian
[101] Zhanghao Wu, Wei-Lin Chiang, Ziming Mao, Zongheng Yang, Eric                   Wang. 2025. 3L-Cache: Low Overhead and Precise Learning-based
      Friedman, Scott Shenker, and Ion Stoica. 2024. Can’t be late: Optimiz-         Eviction Policy for Caches. In Proceedings of the 23rd USENIX Confer-
      ing spot instance savings under deadlines. In 21st USENIX Symposium            ence on File and Storage Technologies. USENIX Association, Santa
      on Networked Systems Design and Implementation (NSDI 24). 185–203.             Clara, CA, 237–254.
[102] Wencong Xiao, Romil Bhardwaj, Ramachandran Ramjee, Muthian               [115] Terry Yue Zhuo, Minh Chien Vu, Jenny Chim, Han Hu, Wenhao Yu,
      Sivathanu, Nipun Kwatra, Zhenhua Han, Pratyush Patel, Xuan Peng,               Ratnadira Widyasari, Imam Nur Bani Yusuf, Haolan Zhan, Junda He,
      Hanyu Zhao, Quanlu Zhang, Fan Yang, and Lidong Zhou. 2018.                     Indraneil Paul, et al. 2024. Bigcodebench: Benchmarking code gen-
      Gandiva: Introspective Cluster Scheduling for Deep Learning. In                eration with diverse function calls and complex instructions. arXiv
      13th USENIX Symposium on Operating Systems Design and Imple-                   preprint arXiv:2406.15877 (2024).
      mentation (OSDI 18). USENIX Association, Carlsbad, CA, 595–610.
      https://www.usenix.org/conference/osdi18/presentation/xiao
[103] Sujay Yadalam, Konstantinos Kanellis, Michael Swift, and Shivaram
                                                                               A     Challenges with LLM-Based
      Venkataraman. 2025. ARMS: Adaptive and Robust Memory Tiering                   Heuristic Generation
      System. arXiv preprint arXiv:2508.04417 (2025).
                                                                               To evaluate whether current LLMs can synthesize effective
[104] Chenxi Yang, Divyanshu Saxena, Rohit Dwivedula, Kshiteej Ma-
      hajan, Swarat Chaudhuri, and Aditya Akella. 2024. C3: Learning           systems heuristics that meet these requirements (Table 3), we
      Congestion Controllers with Formal Certificates. arXiv preprint          used a state-of-the-art model, Claude Opus 4.5, to generate
      arXiv:2412.10915 (2024).                                                 caching heuristics in libCacheSim [43].
[105] John Yang, Carlos E Jimenez, Alexander Wettig, Kilian Lieret,              libCacheSim [43] is an event-driven cache simulator, in
      Shunyu Yao, Karthik Narasimhan, and Ofir Press. 2024. Swe-               which new heuristics are defined by implementing event
      agent: Agent-computer interfaces enable automated software
                                                                               handlers for cache operations such as accesses, evictions,
                                                                       without crashing, as the harness exercised only limited exe-
                                                                       cution paths. This shows that heuristics which compile, run
                                                                       successfully, and perform well on the evaluator may still
                                                                       violate the desired properties in Table 3.

                                                                       A.2   Attempt 2: Agentic Code Synthesis
                                                                       After initial experiments with simple agents showed that
                                                                       LLM-synthesized code often violates desired properties, we
                                                                       asked whether these issues persist in more capable agentic
Figure 11. Evolutionary search with a simple agent vs. Claude
                                                                       frameworks that augment LLMs with external tools. To in-
Code. The dotted line represents the start of a new iteration; every
iteration is seeded with samples of the best-performing programs
                                                                       vestigate, we repeated the heuristic synthesis experiment
so far to help guide the search.                                       using Claude Code – a widely used coding agent that equips
                                                                       an LLM with capabilities such as file manipulation, shell ex-
                                                                       ecution, and search. Such agents may better avoid interface-
and insertions – each of which has a specific function sig-            compliance bugs observed earlier, as they can spawn sub-
nature detailed in the documentation (a systems integration            agents to reason about and understand the internals of the
requirement). Additionally, the libCacheSim engine also pro-           systems they interact with more effectively.
vides access to commonly used features – such as total object             To test this hypothesis, we repeated the experiment using
counts, the current timestamp, and the number of hits/misses           the Claude Code Agent SDK (Claude Opus 4.5) to synthesize
– via raw pointers, which heuristics are allowed to read but           each candidate heuristic, as shown in the right half of Fig-
must not mutate (another systems integration requirement).             ure 11. In addition to default tools (bash, search, read, etc.),
                                                                       we provided a custom evaluate tool that builds the heuris-
A.1    Attempt 1: A Simple Evolutionary Loop                           tic, runs it on CloudPhysics traces, and returns a JSON report
We implement an evolutionary loop using a simple LLM                   of its performance relative to FIFO. Although the agent could
agent (inspired by prior work [25, 81]), as shown in the               execute these steps via bash, exposing them as a dedicated
left half of Figure 11. The agent is provided with a prompt            tool simplifies its workflow.
describing libCacheSim and its interfaces, which it uses to               Using this more capable agentic setup, we ran the evolu-
generate a candidate heuristic. The generated heuristic is             tionary process for ten iterations, producing ten heuristics.
then built and evaluated on a suite of ten traces from the             As in Attempt 1, each iteration generates a candidate via a
CloudPhysics dataset [97]. If a build or runtime error oc-             loop of proposing, evaluating, and refining; however, unlike
curs, the agent receives the stderr output to iteratively              the earlier setup – where the loop was limited to handling
refine and correct its code. Once the heuristic compiles and           compiler and runtime errors – each iteration here is a richer
executes successfully, both the implementation and its per-            multi-turn interaction. The agent can explore the codebase,
formance metrics (i.e., miss rates) are stored in a database.          reason about interfaces, modify implementations, and in-
Each such iteration constitutes the generation of a single             voke tools such as evaluate multiple times before returning
heuristic. This process is repeated for fifty iterations, with         a candidate heuristic.
higher-performing heuristics sampled from the database and                Generating each candidate heuristic with Claude Code
incorporated into subsequent prompts to guide the search               took 11–28 minutes, consumed ∼2M tokens (∼$3.20 via AWS
toward better designs.                                                 Bedrock), and involved an average of 57.4 tool calls. The re-
   Manual inspection revealed a recurring issue across all             sulting heuristics achieved a 36.4%–46.8% improvement over
fifty heuristics. In libCacheSim, heuristics must report their         FIFO, as scored by the evaluator, significantly outperforming
per-object metadata footprint (in bytes) via a system variable         those found by the simpler agent.
used for memory accounting. Despite introducing additional                They also exhibited diverse strategies: the best-performing
per-object state, the LLM consistently under-reported this             heuristic uses a prioritization function combining frequency
value. As a result, these heuristics exceeded their memory             tiers, size-cost normalization, and recency protection, while
budget, yielding unfair comparisons against baselines that             the second-best applies a concave transformation (a sqrt–log
correctly account for memory usage and violating interface             blend) to weight access frequency.
requirements (a system-integration bug).                                  Unlike the previous setup – where even modest gains were
   Despite these issues, after fifty iterations, the evolution-        partly driven by reward hacking (i.e., under-reporting meta-
ary process produced heuristics that “achieved” a 3%–5.1%              data to bypass memory accounting) – the heuristics produced
improvement over FIFO according to the evaluator. How-                 by this agentic framework did not exploit that loophole. How-
ever, these gains were partly driven by exploiting gaps in             ever, several still violated interface assumptions: for instance,
the evaluation harness (i.e., under-reporting metadata usage).         several heuristics – including the best-performing one – over-
Moreover, heuristics with memory safety bugs also passed               wrote next_access_vtime (per-object state maintained by
libCacheSim) to store the current time, violating the system
                                                                       is to implement a scoring function that returns the utility of
interface by treating a read-only field as writable (a systems
                                                                       an object:
integration bug). Additionally, a double-free bug (an execu-
tion safety bug) in the second-best heuristic went undetected                    Higher utility ⇒ more valuable to keep
by the evaluator; libCacheSim exposes two removal paths –              When eviction is required, select the object with the
evict(), which selects and removes objects, and remove(),              lowest utility.
which deletes objects by ID. Since our evaluator exercised             Lazy Priority Queue Execution Model. The scoring func-
only the evict() path, the bug in remove went undetected.              tion is evaluated lazily:
                                                                            • A score is recomputed only when an object is inserted
A.3     Summary                                                                or accessed.
This case study reinforces a growing body of evidence that                  • The resulting score is cached in the priority queue.
LLMs routinely introduce bugs and safety violations when                    • Idle objects are not rescored over time.
generating complex code [40, 45, 71, 115] – and that more ca-          Therefore, expressions such as curr_time - last_access
pable agents are no exception, frequently requiring humans             are ineffective because, at rescore time, curr_time ≈
                                                                       last_access.
in the loop to produce reliable output [77, 90].
                                                                       Instead, use:
   While LLMs may be more successful at synthesizing code
                                                                            • last_access directly for recency,
for self-contained coding tasks [10, 19, 37], systems heuris-
                                                                            • insertion_time directly for age ordering,
tics are usually more complex: they may maintain internal                   • or other stable per-object signals.
state in complex data structures [82], involve intricate state-
transition logic [32, 60, 108], or be dispersed across multiple        Global Features.
files and control paths [57]. Allowing an LLM to synthesize               • f_curr_time (i64): Current logical time.
or modify such heuristics end-to-end – reasoning simultane-               • f_ghost (i64): IDs of recently evicted objects.
ously about policy logic, state management, and mechanisms             Per-Object Features.
– widens the attack surface for subtle bugs and property                   • f_size (i64): Object size in bytes.
violations in the synthesized code.                                        • f_insertion_time (i64): Insertion timestamp.
                                                                           • f_last_access (i64): Most recent access timestamp.
B     Rank-based Cache Eviction Heuristics                                 • f_count (i64): Access count since insertion.
B.1     Results for Same-Size Instances                                Listeners. Listeners determine how feature values are stored
Figure 12 reports results for two classes of instances in which        and queried. Examples include:
cached objects have uniform sizes. As presented in §7.2, we                • RollingWindow(N)
compare these heuristics with nine human-designed base-                    • EWMA({alpha})
lines and find that Vulcan-generated heuristics are generally              • RollingPercentile(N)
competitive against strong manually designed baselines.                    • RollingCount(N)
                                                                       Example listener configuration:
B.2     Synthesis Prompt                                               fs . add_listeners (
The natural-language prompt used for the cache eviction case              f_last_access ,
                                                                          {vulcan:: listeners :: object :: RollingWindow (5)}
study (§7.2) is shown in Listing 5. The prompt also includes
                                                                       );
dynamically selected examples of high-performing scoring
functions from previous rounds, selected automatically by              fs . add_listeners (
the evolution frameworks [51, 87].                                        f_curr_time ,
                                                                          {vulcan:: listeners :: global :: RollingWindow (1)}
    Listing 5: Prompt for synthesizing cache evic-                     );
    tion heuristics
                                                                       Expected Output Format. The generated file must contain:
    Context. You are a systems researcher designing a new cache           1. Listener configuration
    eviction policy. Whenever the cache is full and a new ob-             2. Scoring function
    ject must be inserted, this policy is invoked to select which
    cached object to evict. The policy has access to per-object fea-   Example Scoring Function.
    tures such as object size, insertion time, last access time, and   auto scoring_fn =
    access count, along with global information about recently           [&](
    evicted objects.                                                       vulcan:: store & fs ,
    Policy Model. The policy is implemented using vulcan, a                int64_t obj_id
    framework that separates policy from mechanism. Your task            ) -> double {
                 Cacheus            Sieve              LHD              LeCaR                        Cacheus          Sieve                LHD             LeCaR
                 LRU                S3-FIFO            GDSF             LRB                          LRU              S3-FIFO              GDSF            LRB
                      3L-Cache            Vulcan               Vulcan-NL                                  3L-Cache          Vulcan                Vulcan-NL

        WikiMedia (CDN)                                                                 WikiMedia (CDN)
            Twitter (KV2)                                                                  Twitter (KV2)
            Twitter (KV1)                                                                  Twitter (KV1)
Trace




                                                                                Trace
        Tencent (Object)                                                                Tencent (Object)
            Meta (Block)                                                                   Meta (Block)
               Meta (KV)                                                                      Meta (KV)
             Meta (CDN)
                                                                                            Meta (CDN)
             MSR (Block)
                                                                                            MSR (Block)
                             0.0           0.1           0.2            0.3                            −0.19           0.0           0.1            0.2       0.3
                               Miss Ratio Reduction from FIFO                                                        Miss Ratio Reduction from FIFO

                 (a) Large cache size (10%), objects of the same size                             (b) Small cache size (0.1%), objects of the same size
                        Figure 12. Performance of instance-specialized heuristics versus baselines for two classes of instances.


                                                                                           • Plot(s) reproduced: Figure 5.
             double last_acc = fs . get_latest (
                                                                                           • Plotting script: python3 plot_main_result.py.
                f_last_access , obj_id
             );
                                                                                           • DOI: 10.5281/zenodo.22905385
             double count = fs . get_latest (
                                                                                   C.2         Reproducing Spot VM (Multi-Region) Results
                f_count , obj_id
             );                                                                            • Branch: cbl-multi-artifact;
             double ghost_count = fs . get_count (                                         • §7.1.2;
                f_ghost , obj_id                                                           • Plot(s) reproduced: Figure 7.
             );                                                                            • Plotting script: plot_results.py
             double ghost_penalty = ghost_count * 1 e6 ;                                   • DOI: 10.5281/zenodo.22905389
             return last_acc +( count *10) - ghost_penalty ;
    };                                                                             C.3         Reproducing Caching Results
                                                                                           • Branch: caching-artifact;
                                                                                           • §7.2;
C         Artifact Appendix                                                                • Plot(s) reproduced: Figure 8 and Figure 12.
Our artifact contains: (a) the final discovered heuristics for                             • Plotting script: plot_workload_instances.py
each of our use cases, (b) orchestrator and plotting scripts                               • DOI: 10.5281/zenodo.22905373
to recreate the main results of the paper, (c) scripts to run
heuristic discovery loops for each use case with off-the-shelf                     C.4         Reproducing Memory Tiering Results
evolution frameworks [51, 87], and (d) implementations of                          Note: for this use case, the artifact reproduces results from the
libVulcan and Anvil and documentation on how to extend                             emulated setup and requires CloudLab.
and use these libraries to discover heuristics for new tasks.                         • Branch: tiering-artifact;
Our artifact is available at the following links:                                     • §7.3;
        • Main repository containing code for all four use cases.                     • Plot(s) reproduced: Figure 9.
          – github.com/ldos-project/vulcan-usecases                                   • Plotting script: plot_improvement.py
        • Common libraries:                                                           • DOI: 10.5281/zenodo.22905376
          – libVulcan (DOI: 10.5281/zenodo.22905536)
          – Anvil (DOI: 10.5281/zenodo.22905483)                                   C.5         Running Evolution and Adding Use Cases
        • Discovered heuristics and precomputed results (DOI:                      Beyond reproducing the final results, each use case also in-
          10.5281/zenodo.20361337)                                                 cludes the synthesis harness and prompts, allowing users
   Each use case has a separate repository branch. Check                           to rerun the full discovery loop with an off-the-shelf evolu-
out the appropriate branch of vulcan-usecases and follow                           tion framework (OpenEvolve or ShinkaEvolve). Additionally,
its README.md. For each use case, we provide precomputed                           users who wish to use our framework for their use cases can
results (e.g., JSON files and dumps) that were used to create                      find documentation in libvulcan.
the plots – use these dumps directly or rerun the evaluation.

C.1        Reproducing Spot VM Single-Region Results
        • Branch: cbl-artifact;
        • §7.1.1;
