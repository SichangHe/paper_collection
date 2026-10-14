                                                               NCCLbpf: Verified, Composable Policy Execution
                                                                    for GPU Collective Communication
                                                                                                                          Yusheng Zheng
                                                                                                             University of California, Santa Cruz
                                                                                                                            USA
                                        Abstract                                                                                            infinite loop or race condition can silently halt collective opera-
                                        NCCL is the de facto standard for collective GPU communication                                      tions; and subtle memory corruption can cause unpredictable per-
                                        in large-scale distributed training, relying heavily on plugins to                                  formance degradation or safety violations. NCCL’s own inspector
                                        customize runtime behavior. However, these plugins execute as                                       plugin has caused production training crashes due to use-after-free
                                        unverified native code within NCCL’s address space, risking job                                     and deadlock bugs [11], and profiler plugins have triggered segfaults
arXiv:2603.11438v2 [cs.DC] 4 May 2026




                                        crashes, silent state corruption, and downtime from restarts during                                 on multi-GPU nodes [12]. Moreover, NCCL plugins lack structured
                                        policy updates. Inspired by kernel extensibility models, we intro-                                  state-sharing capabilities, making closed-loop policy adjustments
                                        duce NCCLbpf, a verified, high-performance extension framework                                      across plugins impossible. Updating plugin logic requires restarting
                                        embedding a userspace eBPF runtime directly into NCCL’s existing                                    affected jobs, resulting in disruptive downtime and hindering rapid
                                        plugin interfaces, without modifying NCCL itself. NCCLbpf offers                                    policy iteration in production environments.
                                        load-time static verification to prevent unsafe plugin execution,                                      We identify a structural analogy between NCCL plugin exten-
                                        structured cross-plugin maps enabling composable policies and                                       sion points and kernel-level hooks, where the eBPF framework [17]
                                        closed-loop adaptation, and atomic policy hot-reloads eliminating                                   has already successfully addressed similar challenges [19, 23, 24]. In
                                        downtime previously required for policy updates. Evaluations on                                     both contexts, extension points must execute safely and efficiently
                                        8× NVIDIA B300 GPUs connected via NVLink demonstrate that                                           in performance-critical environments. NCCL’s net plugin closely
                                        NCCLbpf imposes just 80–130 ns overhead per tuner decision (less                                    mirrors eBPF’s original packet-processing use case, and NCCL’s
                                        than 0.03% of collective latency), prevents all tested unsafe plugin                                tuner and profiler interfaces correspond to kernel tracepoints where
                                        behaviors at load-time, and enables a message-size-aware eBPF pol-                                  lightweight policy-driven decisions influence critical runtime be-
                                        icy that improves AllReduce throughput by up to 27% over NCCL’s                                     havior. Inspired by eBPF’s verified extensibility model, we present
                                        default in the 4–128 MiB range.                                                                     NCCLbpf, which integrates a verified, userspace eBPF runtime [22]
                                                                                                                                            directly within NCCL’s existing plugin interface, without modifying
                                                                                                                                            NCCL source code.
                                        1     Introduction                                                                                     NCCLbpf provides three properties: (1) load-time static verifi-
                                        Collective GPU communication performance is crucial for large-                                      cation guarantees safety before execution, preventing crashes and
                                        scale distributed training frameworks such as Megatron-LM [15],                                     state corruption; (2) structured, typed maps enable composable,
                                        DeepSpeed [13], and PyTorch FSDP [20], all of which depend on                                       cross-plugin state sharing, enabling previously impossible closed-
                                        NCCL [10] for efficient inter-GPU data movement. The performance                                    loop adaptations; and (3) atomic policy hot-reload capability allows
                                        of NCCL collectives (e.g., AllReduce, AllGather) significantly de-                                  operators to update policies seamlessly at runtime without inter-
                                        pends on runtime decisions: algorithm selection (ring vs. tree),                                    ruption.
                                        transport protocols (LL vs. Simple [7]), and parallelization channels.                                 We implement NCCLbpf atop NCCL version 2.29.7 using bpf-
                                        Recognizing this dependency, NCCL exposes a modular plugin ar-                                      time, a lightweight userspace eBPF runtime. Our evaluation on
                                        chitecture, including tuner, profiler, and net plugins, allowing cloud                              8× NVIDIA B300 GPUs with NVLink shows that NCCLbpf adds
                                        operators and hardware vendors to tailor policies to match specific                                 80–130 ns overhead per policy decision, representing less than
                                        deployment characteristics. Major providers already leverage these                                  0.03% of collective latency. Atomic updates incur a downtime of
                                        plugins extensively in production scenarios [18].                                                   just 1.07 µs and introduce zero dropped calls across 400,000 policy
                                           However, this flexibility comes at substantial reliability and op-                               invocations. A message-size-aware eBPF policy improves 8-GPU
                                        erability risks. NCCL plugins execute as native code within NCCL’s                                  AllReduce throughput by up to 27% over NCCL’s default algorithm
                                        runtime environment without sandboxing or verification. A single                                    selection in the 4–128 MiB range.
                                        null-pointer dereference can crash a critical GPU training job; an                                     This paper makes three contributions:
                                                                                                                                            (1) NCCLbpf, the first framework to bring verified, composable
                                                                                                                                                eBPF policy execution to NCCL’s plugin architecture, trans-
                                        Permission to make digital or hard copies of all or part of this work for personal or                   parently enhancing safety and extensibility without modifying
                                        classroom use is granted without fee provided that copies are not made or distributed
                                        for profit or commercial advantage and that copies bear this notice and the full citation               NCCL source code (§3–4).
                                        on the first page. Copyrights for components of this work owned by others than the                  (2) A structured, typed-map-based composability mechanism en-
                                        author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
                                        republish, to post on servers or to redistribute to lists, requires prior specific permission
                                                                                                                                                abling previously isolated NCCL plugins to coordinate and dy-
                                        and/or a fee. Request permissions from permissions@acm.org.                                             namically adapt, facilitating closed-loop policy control (§3, §5.3).
                                        Conference’17, Washington, DC, USA                                                                  (3) An evaluation on 8× NVIDIA B300 NVLink GPUs demonstrat-
                                        © 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                        ACM ISBN 978-x-xxxx-xxxx-x/YYYY/MM                                                                      ing low overhead (80–130 ns per decision), verified runtime
                                        https://doi.org/10.1145/nnnnnnn.nnnnnnn
                                                                                                                                        1
Conference’17, July 2017, Washington, DC, USA                                                                                          Yusheng Zheng


    safety (rejecting all unsafe plugins tested), and a message-size-            T2: Structured sharing vs. flexibility. All cross-component state
    aware policy that improves AllReduce throughput by up to 27%              sharing uses typed eBPF maps with atomic access semantics. Maps
    (§5).                                                                     constrain policies to fixed-size keys/values, but NCCL policy state
                                                                              is inherently simple (per-communicator scalars), and structured
                                                                              sharing eliminates the locking bugs that plague ad hoc native plugin
2    Background and Motivation
                                                                              state sharing.
   NCCL and its plugin system. NCCL [10] implements GPU col-
lective primitives (AllReduce, AllGather, Broadcast, etc.) optimized              T3: Availability vs. consistency during updates. Hot-reload atom-
for multi-GPU interconnects. For each collective call, the tuner plu-         ically swaps the function pointer; any in-progress call completes
gin’s getCollInfo receives the collective type, message size, and             under the old policy, the next call uses the new one. No call is lost.
rank topology, and selects an algorithm (ring, tree), protocol (LL,           If the new policy fails verification, the old policy continues. The
LL128, Simple [7]), and channel count by modifying a cost table.              tradeoff: different threads may briefly execute different policies,
The profiler plugin receives timestamped event callbacks; the net             which is acceptable because collective decisions are independent
plugin controls network transport; and the env plugin sets runtime            across calls.
parameters. All four are loaded via dlopen as shared libraries. The              T4: Compatibility vs. capability. Our system operates within
tuner API has evolved rapidly, from v2 (simple integer outputs)               NCCL’s existing plugin ABI, requiring no source modifications,
to v5 (in-place 2D float cost table modification) in two years, and           no custom builds, and no kernel modules. The action space is lim-
major cloud providers ship custom tuner plugins [18]. Despite this            ited to algorithm, protocol, and channel count selection. Deeper
growing ecosystem, plugins remain independent extension points                interventions are outside scope, but the exposed knobs cover the
with no cross-plugin communication and no safety verification.                most impactful tuning decisions. NCCLbpf selects among NCCL’s
                                                                              built-in algorithms; it does not implement custom collective algo-
   The safety gap. Native plugins execute with full process privi-            rithms.
leges. NCCL’s own inspector plugin has caused production training
crashes due to use-after-free and deadlock bugs [11], and profiler            3.2     Threat Model
plugins have triggered segfaults on multi-GPU nodes [12]. At scale,
                                                                              Policies are written by platform operators, not untrusted tenants.
such failures are costly: Llama 3 pre-training on 16,384 GPUs ex-
                                                                              The eBPF verifier (PREVAIL-based) checks memory safety, bounded
perienced 466 job interruptions in 54 days [4], and analyses of
                                                                              execution, stack safety, and helper whitelisting. The system does
production GPU clusters find that ∼30% of training jobs fail, with
                                                                              not protect against resource exhaustion, side channels, bugs in the
programming and configuration errors as the dominant cause [9].
                                                                              trusted computing base (bpftime JIT, PREVAIL verifier, host plugin),
The absence of safe hot-reload further compounds the risk: rolling
                                                                              or semantically incorrect decisions. This provides defense in depth
out plugin updates across a fleet requires restarting every training
                                                                              (eliminating crashes, hangs, and memory corruption), analogous to
job.
                                                                              the Linux kernel’s eBPF model.
   eBPF as safe extension mechanism. Extended BPF (eBPF) [17] is
                                                                              3.3     Architecture
an execution framework, originally implemented in the Linux ker-
nel for packet filtering and tracing, that statically verifies programs       Figure 1 shows the architecture. Policy authors write restricted C
for memory safety and bounded execution before JIT-compiling                  compiled to BPF ELF objects. At load time, each program is verified
them to native code. eBPF has been adopted as a safe-extension                and JIT-compiled to x86-64 code. The map subsystem provides
mechanism across storage [23], networking [2, 24], memory man-                intra-policy state and cross-plugin communication: a profiler eBPF
agement [19], and GPU driver-level resource management [21].                  program writes latency observations; the tuner reads them. Hot-
Recent userspace runtimes [22] extend its reach beyond the ker-               reload verifies and JIT-compiles a replacement, then atomically
nel, enabling eBPF execution inside application processes with-               swaps the function pointer via compare-and-swap.
out kernel privileges. Three properties make eBPF well-suited to                 Policy programming model. A policy takes a policy_context
NCCL policy execution: (1) load-time verification catches memory-             (collective type, message size, rank count) and writes algorithm,
safety and termination bugs that cause the crashes described above;           protocol, and channel count decisions. The verifier ensures policies
(2) typed maps provide concurrent state sharing between profiler              only read input fields and write output fields. Map lookups require
and tuner without ad hoc shared memory; and (3) atomic program                null checks before dereference; omitting one causes load-time re-
replacement enables verified hot-reload.                                      jection.
                                                                              Listing 1: Profiler-to-tuner closed loop. The profiler (top)
3 Design                                                                      writes latency into a shared eBPF map; the tuner (bottom)
3.1 Design Tensions                                                           reads it for adaptive channel selection. Null checks (lines 5,
   T1: Safety vs. overhead. NCCLbpf verifies only at load time (1–            14) are enforced by the verifier.
5 ms, amortized over the job lifetime), relying on the invariant that         1   /* --- profiler eBPF program --- */
                                                                              2   SEC("profiler")
verified BPF bytecode, once JIT-compiled, cannot violate its safety           3   int record_latency(struct profiler_context *ctx) {
                                                                              4     __u32 key = ctx->comm_id;
guarantees at runtime. The tradeoff: verification catches memory              5     struct latency_state *st =
safety and termination bugs, not poor policy decisions.                       6       bpf_map_lookup_elem(&latency_map, &key);

                                                                          2
 NCCLbpf : Verified, Composable Policy Execution
 for GPU Collective Communication                                                                                    Conference’17, July 2017, Washington, DC, USA



          NCCL process
                                                                            bpftime runtime
                                                                                 verifier, JIT, maps, helpers        load
                                  metadata Tuner Adapter                                                                    policy.bpf.o
                                              getCollInfo()      decision        telemetry / config maps
                NCCL Core
                                                                                                      read
                  collectives,
                                                                                     Tuner eBPF policy
                                                                                     write                                    hot-reload
                  transports
                                 timestamps Profiler Adapter

                                               event callbacks                    Profiler eBPF policy




 Figure 1: NCCLbpf architecture. Policy programs are verified via PREVAIL, JIT-compiled by bpftime, and execute inside the
 NCCL process. Profiler and tuner communicate through shared typed eBPF maps. The entire system loads as standard NCCL
 plugins.


 7    if (!st) return 0;                                                                  NCCL integration challenges. NCCL’s tuner API uses cost arrays
 8    st->avg_latency_ns = ctx->latency_ns;
 9    st->channels = ctx->n_channels;
                                                                                       rather than direct algorithm IDs: the tuner sets costs to zero for
10    return 0;                                                                        preferred choices and to a sentinel value (1e9) for others, allowing
11   }
12   /* --- tuner eBPF program --- */                                                  NCCL to fall back gracefully if the requested combination is un-
13   SEC("tuner")                                                                      available. Our integration translates eBPF policy outputs into cost
14   int size_aware_adaptive(struct policy_context *ctx) {
15     __u32 key = ctx->comm_id;                                                       array entries. NCCL also passes a maximum channel count that the
16     struct latency_state *st =
17       bpf_map_lookup_elem(&latency_map, &key);
                                                                                       tuner must respect; our native baseline layer clamps the policy’s
18     if (!st) { ctx->n_channels = 4; return 0; }                                     request. Communicator identification required deriving a stable ID
19     if (ctx->msg_size <= 32 * 1024)
20       ctx->algorithm = NCCL_ALGO_TREE;
                                                                                       from the context pointer via hashing, since the communicator ID is
21     else                                                                            not directly exposed in the tuner API as a simple integer.
22       ctx->algorithm = NCCL_ALGO_RING;
23     ctx->protocol = NCCL_PROTO_SIMPLE;
24     if (st->avg_latency_ns > 1000000)
25       ctx->n_channels = min(st->channels + 1, 16);
                                                                                          Hot-reload mechanism. The active policy is stored as an atomic
26     else                                                                            function pointer. Reload has three phases: (1) verify the new BPF
27       ctx->n_channels = st->channels;
28     return 0;                                                                       program, (2) JIT-compile it, (3) atomic compare-and-swap on the
29   }                                                                                 pointer. The total reload cost is ∼9.4 ms; only the final swap (1.07 µs)
                                                                                       touches the hot path. The old pointer is retained until in-flight calls
   The two programs share latency_map via the eBPF map subsys-
                                                                                       drain. If the replacement fails verification, the swap is aborted and
tem, a capability absent from NCCL’s native plugin architecture,
                                                                                       the old policy continues; the system never enters an unverified
where tuner and profiler have no shared state. Null checks on map
                                                                                       state.
lookups (lines 5 and 14) are enforced by the verifier; omitting either
causes load-time rejection.
                                                                                          Native baseline for comparison. To provide a fair overhead com-
 4    Implementation                                                                   parison, we implemented a native C++ baseline that performs iden-
                                                                                       tical policy logic without the eBPF layer, compiled with the same
 NCCLbpf is implemented in approximately 2,500 lines of C/C++
                                                                                       optimization flags (-O2). The overhead difference between the na-
 (plugin host) and 500 lines of restricted C (policy programs).
                                                                                       tive baseline and eBPF policies directly measures the cost of the
    bpftime integration. We embed bpftime [22] as the userspace                        eBPF dispatch and JIT execution layers, isolated from any policy
 eBPF runtime. bpftime provides an LLVM-based JIT compiler, a                          logic cost.
 PREVAIL-based [5] static verifier, and a map subsystem. The verifier
 runs in the same address space as the plugin, adding approximately
                                                                                       5     Evaluation
 1–5 ms of one-time startup overhead amortized over the lifetime
 of the training job. The LLVM JIT produces optimized x86-64 code,                        Testbed. CPU microbenchmarks run on a 240-core AMD EPYC 9575F;
 narrowing the gap to native performance.                                              each benchmark performs 1 million calls and reports P50/P99 laten-
                                                                                       cies. GPU experiments use 8× NVIDIA B300 SXM6 GPUs (Blackwell,
    Plugin registration. NCCLbpf registers itself as both a tuner                      275 GB each) connected via NVLink 5 (NV18, 1.8 TB/s per GPU)
 and profiler plugin via NCCL’s ncclTunerPlugin_v3 (or v5) and                         with CUDA 13.0 and NCCL 2.29.7, hosted on Verda.
 ncclProfilerPlugin_v1 (or v6) interfaces. The tuner plugin’s
 getCollInfo() function constructs a policy_context, invokes
 the JIT-compiled eBPF function, and copies the output fields into                     5.1     Overhead
 NCCL’s result structure. The profiler plugin’s event callbacks ex-                    Table 1 reports per-call latency. The overhead follows an approxi-
 tract latency information and update the shared eBPF maps.                            mate model of 80 + 30𝑛 lookup + 10𝑛 update ns (array maps are faster
                                                                                 3
Conference’17, July 2017, Washington, DC, USA                                                                                                       Yusheng Zheng


Table 1: CPU microbenchmark (1M calls each). eBPF policies
add 80–130 ns over native code. The overhead decomposes                                                       NCCL default (NVLS)
                                                                                                   800
into plugin framework base (+80 ns, of which eBPF JIT dis-                                                    eBPF policy (v2)
patch is 33 ns), map lookup (+30 ns each), and map update                                                     bad_channels (1ch)
(+10 ns each).




                                                                            Bus Bandwidth (GB/s)
                                                                                                   600


           Policy                   P50 (ns)    P99 (ns)    ΔP50
           Native baseline                 20          30     —                                    400
           noop                           100         111    +80
           size_aware_v2                  100         111    +80
           lookup_only                    130         140   +110                                   200
           lookup_update                  140         151   +120
           adaptive_channels              140         151   +120
           slo_enforcer                   150         160   +130
                                                                                                    0
                                                                                                         4M   8M 16M 32M 64M 128M 256M         1G             8G
                                                                                                                              Message Size
than hash maps, causing minor deviations). Even the most com-
plex policy (slo_enforcer) adds only 130 ns. For a 128 MiB 8-GPU            Figure 2: 8-GPU AllReduce on NVLink. The eBPF policy
AllReduce on NVLink (∼394 µs), this is 0.03% of collective latency.         selects Ring/LL128 for 4–32 MiB and Ring/Simple for 64–
   End-to-end GPU measurements on NVLink across small message               192 MiB, improving throughput by up to 27% over NCCL’s
sizes (8 B to 256 KiB) show that the noop plugin adds ∼1.3 µs of            default NVLS algorithm. A deliberately bad policy (1 channel)
fixed overhead (∼4% of the ∼32 µs NVLink baseline). This overhead           shows that policies have real control, including destructive
comes from the plugin framework (shared memory setup, cost table            power.
writes), not the eBPF dispatch itself (33 ns). For messages of 4 MiB
and above, the overhead is below measurement noise (<0.1%).
                                                                            Table 2: Algorithm sweep: 8-GPU AllReduce bus bandwidth
5.2     Safety and Hot-Reload                                               (GB/s). Ring outperforms NVLS by 5–27% in the 4–128 MiB
                                                                            range.
We tested 14 eBPF programs against the PREVAIL-based verifier:
7 safe policies (including all policies in Table 1) were accepted;
7 unsafe programs, each targeting a distinct bug class (null-pointer                                      Size      Default (NVLS)    Ring          Δ
dereference, out-of-bounds access, illegal helper, stack overflow,                                        4 MiB               133.5   148.1   +10.9%
unbounded loop, input-field write, division by zero), were rejected                                       8 MiB               196.3   249.7   +27.2%
at load time with actionable error messages.                                                              16 MiB              278.8   337.4   +21.0%
   The safety difference is concrete. We implemented the same                                             32 MiB              349.3   402.4   +15.2%
null-dereference bug as both a native C plugin and an eBPF policy:                                        64 MiB              425.2   471.8   +11.0%
                                                                                                          128 MiB             596.9   628.9    +5.4%
 Native plugin: Signal: SIGSEGV (address 0x0)
                 in getCollInfo() at native_bad_plugin.so                                                 256 MiB             656.5   632.5    −3.7%
 eBPF policy: VERIFIER REJECT: R0 is a pointer to                                                         8 GiB               836.3   697.6   −16.6%
                 map_value_or_null; must check != NULL
                 before dereference at insn 7

The native plugin crashes the training job; the eBPF policy is caught       eBPF policy can select per-message-size. Our nvlink_ring_mid_v2
before execution.                                                           policy (fewer than 20 lines of C) selects Ring/LL128 for 4–32 MiB,
    Hot-reload swaps the active policy atomically via compare-and-          Ring/Simple for 64–192 MiB, and defers to NCCL’s default other-
swap (1.07 µs swap time; ∼9.4 ms including verification and JIT).           wise.
Across 400,000 continuous invocations, we observe zero lost calls.             Figure 2 shows the result. The eBPF policy achieves 5.5–26.5%
If the replacement fails verification, the old policy continues unin-       improvement over NCCL default in the targeted range (steady-state,
terrupted.                                                                  after 2–3 warmup communicator creations that NCCL requires to
                                                                            stabilize Ring/LL128 GPU buffers), while matching default perfor-
5.3     Case Studies                                                        mance outside this range. The noop policy (not shown) produces
   NVLink-aware adaptive policy. On our 8× B300 NVLink testbed,             identical throughput to the no-plugin baseline, confirming zero
NCCL 2.29.7 defaults to the NVLS algorithm (NVLink SHARP with               overhead at 4 MiB+.
hardware multicast) for all message sizes. A parameter sweep re-               A deliberately bad policy (bad_channels, forcing 1 channel)
veals that Ring with 32 channels outperforms NVLS by 5–27% in               passes the verifier (it is memory-safe) but causes 87–95% through-
the 4–128 MiB range, while NVLS is superior at 256 MiB and above            put degradation, demonstrating that policies have real control over
(Table 2).                                                                  NCCL’s behavior. The verifier prevents crashes and memory corrup-
   Static environment variables (NCCL_ALGO=Ring) cannot exploit             tion, not poor decisions; semantic validation remains the operator’s
this: they apply globally and would degrade the 256 MiB+ range. An          responsibility.
                                                                        4
NCCLbpf : Verified, Composable Policy Execution
for GPU Collective Communication                                                                                Conference’17, July 2017, Washington, DC, USA


   Stability. Over 20 independent runs of 8-GPU AllGather at 128 MiB,       prototype wraps the built-in Socket backend; deeper integration
the default configuration achieves 565.6 ± 0.9 GB/s (CV = 0.15%) and        (e.g., RDMA-aware policies) is future work. Our evaluation uses
the eBPF v2 policy achieves 565.5 ± 0.6 GB/s (CV = 0.10%). Both con-        8 GPUs on a single node with NVLink; multi-node experiments
figurations are highly stable on NVLink, with the policy showing            with InfiniBand and larger rank counts are needed to validate the
32% lower variance. The default has one 3.4𝜎 outlier (562.6 GB/s);          approach at production scale. A higher-level policy DSL compiled to
the policy distribution is unimodal with no comparable outlier.             BPF would lower the barrier for ML engineers who are not familiar
                                                                            with eBPF programming.
   Profiler-to-tuner composability. To evaluate cross-plugin compos-
                                                                               The eBPF-for-extensions pattern may generalize beyond NCCL.
ability, we construct an adaptive channels policy that starts with a
                                                                            AMD’s RCCL [1] exposes a similar plugin architecture, suggesting
conservative channel count (nChannels = 2) and relies on profiler
                                                                            that a cross-vendor port may be feasible. Other libraries with native-
telemetry to adapt upward. Without the profiler, the tuner receives
                                                                            code extension points (MPI implementations, RDMA middleware)
no samples and remains at 2 channels. With the profiler enabled,
                                                                            face similar safety gaps and could benefit from the same verify-
latency samples flow into a shared eBPF map, and the tuner ramps
                                                                            then-execute approach.
from 2 to 12 channels over 100,000 calls. Under injected contention
(10× latency spike), the policy reduces channels from 12 to 2; upon
recovery, it ramps back to 12 within 100,000 calls. This three-phase        8    Conclusion
response (baseline→contention→recovery) validates NCCLbpf’s                 We presented NCCLbpf, a system that transforms NCCL’s unsafe
composability model: two independently deployed eBPF programs               native plugin extension points into verified, composable policy
cooperate through shared typed maps, a capability absent from               hooks by embedding a userspace eBPF runtime. NCCL’s plugin
NCCL’s native plugin architecture.                                          architecture is structurally analogous to kernel extension points
                                                                            where eBPF is already proven; NCCLbpf brings this model to GPU
   Net plugin extensibility. We implement an eBPF-wrapped net
                                                                            collective communication, covering tuner, profiler, and net plug-
plugin that interposes on NCCL’s Socket transport. The wrapper
                                                                            ins. NCCLbpf adds 80–130 ns per policy decision and negligible
forwards all transport operations to the built-in backend while
                                                                            overhead on the net data path, catches crash-inducing bugs at load
executing a BPF program at each isend/irecv call to count bytes
                                                                            time, supports atomic hot-reload without call loss, and enables a
and connections via a shared eBPF map. The wrapped transport
                                                                            message-size-aware policy that improves 8-GPU NVLink AllReduce
adds less than 2% overhead, confirming that eBPF hooks can operate
                                                                            throughput by up to 27% over NCCL’s default, with zero NCCL
on NCCL’s data-plane path with negligible cost, paralleling eBPF’s
                                                                            modifications.
established role in kernel packet processing.

6    Related Work                                                           Acknowledgments
   Collective communication. MSCCL [3] and TACCL [14] synthe-               We thank Verda for providing the 8× NVIDIA B300 NVLink com-
size static schedules offline; they do not address runtime policy           pute infrastructure used in this work.
selection or safety. AutoCCL [18] automates tuning via search but
uses native code without verification. MSCCL++ [8] provides GPU-            References
driven primitives at the mechanism layer. Hu et al. [7] provide              [1] AMD. 2024. RCCL: ROCm Communication Collectives Library. https://github.
                                                                                 com/ROCm/rccl.
a comprehensive analysis of NCCL’s protocol variants and algo-               [2] Zhongjie Chen, Qingkai Meng, ChonLam Lao, Yifan Liu, Fengyuan Ren, Minlan
rithms. gpu_ext [21] applies eBPF to GPU driver-level resource                   Yu, and Yang Zhou. 2025. eTran: Extensible Kernel Transport with eBPF. In
management; NCCLbpf targets the collective communication li-                     Proceedings of the 22nd USENIX Symposium on Networked Systems Design and
                                                                                 Implementation (NSDI).
brary layer, where policies govern algorithm and protocol selection          [3] Meghan Cowan, Saeed Maleki, Madanlal Musuvathi, Olli Saarikivi, and Yifan
rather than device resources. NCCLbpf is complementary: a policy                 Xiong. 2023. MSCCLang: Microsoft Collective Communication Language. In
can activate synthesized schedules or tuned configurations based                 Proceedings of the 28th ACM International Conference on Architectural Support for
                                                                                 Programming Languages and Operating Systems (ASPLOS).
on runtime conditions.                                                       [4] Abhimanyu Dubey et al. 2024. The Llama 3 Herd of Models. arXiv preprint
                                                                                 arXiv:2407.21783 (2024).
   Alternative extension mechanisms. WebAssembly [6] provides                [5] Elazar Gershuni, Nadav Amit, Arie Gurfinkel, Nina Narodytska, Jorge A. Navas,
sandboxed execution but lacks eBPF’s static safety guarantees (ter-              Noam Rinetzky, Leonid Ryzhyk, and Mooly Sagiv. 2019. Simple and Precise
                                                                                 Static Analysis of Untrusted Linux Kernel Extensions. In Proceedings of the 40th
mination, bounded memory access), and incurs higher overhead                     ACM SIGPLAN Conference on Programming Language Design and Implementation
from runtime bounds checks. Out-of-process services add microsec-                (PLDI).
onds of IPC latency, an order of magnitude more than NCCLbpf’s               [6] Andreas Haas, Andreas Rossberg, Derek L. Schuff, Ben L. Titzer, Michael Holman,
                                                                                 Dan Gohman, Luke Wagner, Alon Zakai, and JF Bastien. 2017. Bringing the
80–130 ns overhead. Declarative DSLs cannot express stateful poli-               Web up to Speed with WebAssembly. In Proceedings of the 38th ACM SIGPLAN
cies or feedback loops. Hardware isolation (Intel MPK [16]) provides             Conference on Programming Language Design and Implementation (PLDI).
                                                                             [7] Zhiyi Hu, Siyuan Shen, Tommaso Bonato, Sylvain Jeaugey, et al. 2025. De-
memory separation without verification. eBPF uniquely combines                   mystifying NCCL: An In-depth Analysis of GPU Communication Protocols and
static verification with near-native JIT performance in a single                 Algorithms. arXiv preprint arXiv:2507.04786 (2025).
model.                                                                       [8] Changho Hwang, Peng Cheng, Roshan Dathathri, Abhinav Jangda, Saeed Maleki,
                                                                                 Madan Musuvathi, Olli Saarikivi, Aashaka Shah, Ziyue Yang, Binyang Li, et al.
                                                                                 2026. MSCCL++: Rethinking GPU Communication Abstractions for AI Inference.
7    Discussion                                                                  In Proceedings of the 31st ACM International Conference on Architectural Support
                                                                                 for Programming Languages and Operating Systems (ASPLOS).
NCCLbpf currently covers tuner, profiler, and net plugins; extend-           [9] Myeongjae Jeon, Shivaram Venkataraman, Amar Phanishayee, Junjie Qian, Wen-
ing coverage to the env plugin is straightforward. Our net plugin                cong Xiao, and Fan Yang. 2019. Analysis of Large-Scale Multi-Tenant GPU
                                                                        5
Conference’17, July 2017, Washington, DC, USA                                                                                                                     Yusheng Zheng


     Clusters for DNN Training Workloads. In Proceedings of the 2019 USENIX Annual               Comput. Surveys 53, 1 (2020).
     Technical Conference (ATC).                                                            [18] Guanbin Xu, Zhihao Le, Yinhe Chen, Zhiqi Lin, Zewen Jin, Youshan Miao, and
[10] NVIDIA. 2024. NCCL: NVIDIA Collective Communications Library. https:                        Cheng Li. 2025. AutoCCL: Automated Collective Communication Tuning for
     //github.com/NVIDIA/nccl.                                                                   Accelerating Distributed and Parallel DNN Training. In Proceedings of the 22nd
[11] NVIDIA. 2026. Deadlock/crash due to UAF in inspector plugin. https://github.                USENIX Symposium on Networked Systems Design and Implementation (NSDI).
     com/NVIDIA/nccl/issues/2000.                                                           [19] Anil Yelam, Kan Wu, Zhiyuan Guo, Suli Yang, Rajath Shashidhara, Wei Xu, Stanko
[12] NVIDIA. 2026. Inspector bug: segfault encountered during training. https:                   Novaković, Alex C. Snoeren, and Kimberly Keeton. 2025. PageFlex: Flexible and
     //github.com/NVIDIA/nccl/issues/1992.                                                       Efficient User-space Delegation of Linux Paging Policies with eBPF. In Proceedings
[13] Jeff Rasley, Samyam Rajbhandari, Olatunji Ruwase, and Yuxiong He. 2020. Deep-               of the 2025 USENIX Annual Technical Conference (ATC).
     Speed: System Optimizations Enable Training Deep Learning Models with Over             [20] Yanli Zhao, Andrew Gu, Rohan Varma, Liang Luo, Chien-Chin Huang, Min Xu,
     100 Billion Parameters. In Proceedings of the 26th ACM SIGKDD International                 Les Wright, Hamid Shojanazeri, Myle Ott, Sam Shleifer, Alban Desmaison, Can
     Conference on Knowledge Discovery & Data Mining.                                            Balioglu, Pritam Damania, Benjamin Nguyen, Geeta Chauhan, Yuchen Hao, Ajit
[14] Aashaka Shah, Vijay Chidambaram, Meghan Cowan, Saeed Maleki, Madan Musu-                    Mathews, and Shen Li. 2023. PyTorch FSDP: Experiences on Scaling Fully Sharded
     vathi, Todd Mytkowicz, Jacob Nelson, Olli Saarikivi, and Rachee Singh. 2023.                Data Parallel. Proceedings of the VLDB Endowment 16, 12 (2023).
     TACCL: Guiding Collective Algorithm Synthesis using Communication Sketches.            [21] Yusheng Zheng, Tong Yu, Yiwei Yang, et al. 2025. gpu_ext: Extensible OS Policies
     In Proceedings of the 20th USENIX Symposium on Networked Systems Design and                 for GPUs via eBPF. arXiv preprint arXiv:2512.12615 (2025).
     Implementation (NSDI).                                                                 [22] Yusheng Zheng, Tong Yu, Yiwei Yang, Yanpeng Hu, Xiaozheng Lai, Dan Williams,
[15] Mohammad Shoeybi, Mostofa Patwary, Raul Puri, Patrick LeGresley, Jared Casper,              and Andi Quinn. 2025. Extending Applications Safely and Efficiently. In Proceed-
     and Bryan Catanzaro. 2019. Megatron-LM: Training Multi-Billion Parameter                    ings of the 19th USENIX Symposium on Operating Systems Design and Implemen-
     Language Models Using Model Parallelism. arXiv preprint arXiv:1909.08053                    tation (OSDI).
     (2019).                                                                                [23] Yuhong Zhong, Haoyu Li, Yu Jian Wu, Ioannis Zarkadas, Jeffrey Tao, Evan
[16] Anjo Vahldiek-Oberwagner, Eslam Elnikety, Nuno O. Duarte, Michael Sammler,                  Mesterhazy, Michael Makris, Junfeng Yang, Amy Tai, Ryan Stutsman, and Asaf
     Peter Druschel, and Deepak Garg. 2019. ERIM: Secure, Efficient In-Process                   Cidon. 2022. XRP: In-Kernel Storage Functions with eBPF. In Proceedings of
     Isolation with Protection Keys (MPK). In Proceedings of the 28th USENIX Security            the 16th USENIX Symposium on Operating Systems Design and Implementation
     Symposium.                                                                                  (OSDI).
[17] Marcos A. M. Vieira, Matheus S. Castanho, Racyus D. G. Pacífico, Elerson R. S.         [24] Yang Zhou, Zezhou Wang, Sowmya Dharanipragada, and Minlan Yu. 2023. Elec-
     Santos, Eduardo P. M. Câmara Júnior, and Luiz F. M. Vieira. 2020. Fast Packet               trode: Accelerating Distributed Protocols with eBPF. In Proceedings of the 20th
     Processing with eBPF and XDP: Concepts, Code, Challenges, and Applications.                 USENIX Symposium on Networked Systems Design and Implementation (NSDI).




                                                                                        6
