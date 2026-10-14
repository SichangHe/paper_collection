                                               Bulkhead: Automated Semantic Detection and
                                              Remediation of Container Escape Vulnerabilities
                                                            Qiyuan Fan1 , Zhi Li1 , Junjie Li2 , XiaoFeng Wang2 , Bin Yuan1 , and Deqing Zou1
                                                                         1
                                                                             Huazhong University of Science and Technology, Wuhan, China
                                                                                   2
                                                                                     Nanyang Technological University, Singapore


                                            Abstract—Filesystem isolation in container ecosystems is often    a failure to securely bind these checks to the execution phase,
                                         weakened by cross-boundary path misresolution, causing path          creating Time-of-Check to Time-of-Use (TOCTOU) race con-
                                         traversal (PaTra) vulnerabilities. These vulnerabilities stem from   ditions. Consequently, when a container interacts with the host
                                         insecure host-container interactions and have become increas-
                                         ingly pervasive as cloud systems mount shared resources, such        filesystem, attackers can breach isolation boundaries either
                                         as GPUs and agent workspaces, into containers to support AI          through direct, unvalidated path resolution or by exploiting
                                         workloads. Existing defenses remain inadequate. Kernel-level         the brief time window between validation and actual resource
                                         protections are intrusive, can destabilize system calls, and have    utilization [4], [5].
                                         therefore not been accepted into the Linux mainline. Detection
                                         methods rely on static rule matching or manual code auditing.        The Persistent Recurrence of PaTra Vulnerabilities. After
                                         Static rules can flag path-related functions but fail to capture     years of attention and effort, this security threat, however,
arXiv:2607.12723v1 [cs.CR] 14 Jul 2026




                                         the semantics needed to determine whether a host-container           remains unresolved, as evidenced by 27 major CVEs recorded
                                         interaction exists, causing many false positives. Manual review
                                                                                                              over the past decade and an upward trend of such vulnera-
                                         requires domain expertise, making it costly, inefficient, and
                                         difficult to scale.                                                  bilities throughout 2024 and 2025. This persistent resurgence
                                            To address this threat, we present Bulkhead, an automated         is fundamentally driven by the architectural evolution of
                                         framework that integrates large language models (LLMs) with          cloud-native ecosystems where the demand for cross-boundary
                                         formal methods for semantic vulnerability discovery and reme-        resource access has intensified. Beyond traditional container
                                         diation. Bulkhead uses a multi-agent system to identify and
                                         repair PaTra vulnerabilities through multi-dimensional knowl-
                                                                                                              management platforms, the proliferation of GPU container
                                         edge patterns generalized from known cases. It first applies         toolkits and containerized workspaces for AI agents has ex-
                                         high-risk functional patterns to locate entry points for cross-      posed a vast array of privileged interaction interfaces. These
                                         boundary interactions in containerized code, then uses call-         modern scenarios frequently require mounting host resources,
                                         chain patterns to recover the corresponding execution paths at       driver libraries, or device nodes into isolated environments
                                         suitable depth. The Detection pipeline analyzes these call chains
                                         against the application scenarios and threat model, identifying
                                                                                                              to facilitate execution, which inadvertently expands the attack
                                         vulnerabilities such as missing security checks and TOCTOU           surface for path resolution exploits.
                                         flaws in cross-boundary interactions, and generating proof-of-          A representative example of this expanding risk is CVE-
                                         concept (PoC) exploits for validation. These PoCs then guide         2024-0132 in the NVIDIA Container Toolkit [6]. In this
                                         patch generation. To ensure remediation correctness, the Patch
                                         pipeline performs assertion-driven verification using predefined
                                                                                                              case, the utility fails to safely resolve the symbolic links
                                         model-checking templates.                                            (symlinks) while processing container-provided library paths
                                                                                                              during initialization. An attacker can place a malicious symlink
                                                               I. I NTRODUCTION                               inside a container image to induce the privileged host-level
                                            Container technologies leverage kernel mechanisms to pro-         toolkit to access sensitive host filesystem locations, thereby
                                         vide lightweight isolation, serving as the foundational in-          bypassing container isolation. Although core container run-
                                         frastructure for cloud platforms [1], [2]. With the rapid ad-        times have been substantially hardened, the rapid growth of
                                         vancement of Large Language Models (LLMs), this adop-                plugins and AI execution servers has shifted much of this
                                         tion has accelerated as systems like OpenHands [3] utilizes          risk to third-party components, whose developers often lack
                                         container-based sandboxes to provide isolated workspaces for         the specialized security context needed to enforce complex
                                         autonomous agents. However, this ubiquitous deployment is            isolation invariants. This, in turn, exacerbates the recurrence
                                         continually threatened by logic vulnerabilities, particularly        of logic-based container escape vulnerabilities.
                                         Path Traversal (PaTra). These vulnerabilities arise from one
                                                                                                              Challenges of Existing Solutions. Addressing PaTra vulnera-
                                         of two root causes: a complete absence of security checks, or
                                                                                                              bilities has become an intractable challenge for both academia
                                                                                                              and the open-source community. In the academic sphere, the
                                                                                                              previous work introduced strict access controls directly within
                                                                                                              the Virtual File System (VFS) layer of the Linux kernel [7].
                                                                                                              While theoretically sound, its practical deployment is highly
                                         Conference Name: XXX
                                         Conference Date: XXX                                                 problematic. The required modifications are too deeply inte-
                                         ISBN: XXX                                                            grated into the kernel mainline, which inevitably leads to un-
                                         Conference Website: XXX
                                         XXX
derlying system call instability. Furthermore, this kernel-level        summarized to identify the entries for high-risk functions and
intervention is overly specialized for containerized scenarios,         optimal call-chain depths. Furthermore, standardized model
adversely affecting the normal, everyday usage of the Linux             checking templates are derived from the logic of existing
operating system, which explains why it has consistently failed         patches to facilitate the formal validation of generated patches.
to be accepted or merged by the mainstream Linux kernel                 Extensive real-world evaluations demonstrate the efficacy of
community. The open-source community adopts the approach                this approach, as Bulkhead successfully identified 9 deep-
of vulnerability detection and patching case by case, which is          seated logic vulnerabilities in mainstream repositories, result-
error-prone. A classic example is the evolution of CVE-2018-            ing in the assignment of 3 new CVEs so far. Moreover,
15664 [8], where the initial patch merely addressed a basic             we have submitted the automatically generated and formally
symlink traversal, only to be bypassed and completely broken            verified patches to open-source communities and are awaiting
a year later in CVE-2019-14271 [9], because the underlying              their approval for merge.
TOCTOU race condition was left unaddressed. Furthermore,                Contributions. Our contributions are outlined as follows:
patches often introduce secondary bugs, severely degrading
                                                                        • New Understanding of PaTra Vulnerabilities: We present a
system stability. The complexity here is so daunting that some
                                                                        systematic study of PaTra vulnerabilities in container ecosys-
mainstream container engines (e.g., Alibaba’s Pouch [10])
                                                                        tems. By analyzing major CVEs over the past decade, we
have resorted to extreme measures, such as completely dis-
                                                                        identify a fundamental shift in the threat landscape: vulnerabil-
abling symlink follow, simply to avoid the insurmountable risk
                                                                        ities are increasingly emerging from logic flaws in third-party
of path resolution exploits.
                                                                        components that mediate cross-boundary resource interactions,
   Given the impracticality of eradicating symlink-induced              rather than from core container runtimes.
path traversal vulnerabilities at the kernel level, a pragmatic
                                                                        • A Knowledge-Guided Approach for Logic Vulnerability
strategy centers on helping community for rapid detection
                                                                        Detection and Remediation: We propose a knowledge-guided
and intelligent remediation. Previous detection approaches
                                                                        approach for detecting and remediating PaTra logic vulnera-
predominantly rely on static analysis techniques, such as
                                                                        bilities. By abstracting historical vulnerabilities into structured
static rule matching [11] or Deterministic Finite Automata
                                                                        semantic knowledge, Bulkhead guides LLM-driven reasoning
(DFA) [12].
                                                                        to progressively localize security-critical logic in complex
   While these methods can identify path-related operations,            codebases, enabling precise vulnerability detection, automated
they cannot fundamentally understand deeper code semantics              patch generation, and formal verification.
and contextual intent. In the complex setting of container-             • Real-World Security Impact: We evaluate Bulkhead on main-
host isolation and interaction, this semantic blindness leads to        stream container-related open-source repositories and uncover
substantial false positives. For instance, a static analyzer may        9 previously unknown logic vulnerabilities, leading to the
flag path operations within the host system or other path strings       assignment of 3 new CVEs so far. Furthermore, the auto-
that are not exploitable as potentially vulnerable. Moreover,           matically generated patches have been submitted to upstream
manually crafting precise rules or automata for complex vul-            communities, demonstrating the practical effectiveness and
nerability logic demands significant human expertise, resulting         deployability of our approach.
in high maintenance costs and slow response times that cannot
keep pace with the rapid evolution of new escape risks.                                        II. BACKGROUND
Our Apporach. To overcome these limitations, we propose an              A. Container Filesystem Isolation Vulnerabilities
automated agent framework that integrates LLMs with model                  Container technologies enforce lightweight isolation
checking to achieve end-to-end vulnerability detection and              through Linux kernel mechanisms like namespaces [13]
remediation. Our approach leverages the semantic reasoning              and cgroups [14]. Filesystem isolation combines the mount
capabilities of LLMs to comprehend complex code logic and               namespace with chroot or pivot_root operations to
interaction patterns within container environments, enabling            restrict a process to a designated root hierarchy. This isolation
precise vulnerability localization and detection. Simultane-            primarily modifies the process’s view rather than partitioning
ously, we introduce model checking to rigorously verify the             the underlying kernel objects. The VFS layer continues to
patches automatically generated by the LLM.                             represent file objects via globally managed dentry and
   The core methodology of this detection and remediation               inode structures shared across namespace boundaries [15].
process lies in systematically generalizing known vulnerabili-          As a result, although containerized processes operate within
ties from multiple dimensions into knowledge bases to guide             isolated filesystem views, host-level components still retain
the LLMs. Detection patterns are abstracted from established            visibility into both host and container filesystems through
PaTra CVEs by decomposing exploits into their constituent               the shared VFS infrastructure. Consequently, container
objects, interaction sequences, and exploitation strategies,            management tools and runtime services often need to traverse
thereby establishing definitive threat models and capability            and access filesystem objects under container-controlled paths
boundaries for cross-boundary interactions. Moreover, in order          when performing administrative operations .
to extract the complete code call-chain that can reflect the               Host-container filesystem interactions arise throughout the
threat model of the target function, call-chain patterns are            container lifecycle. Before container startup, runtimes and



                                                                    2
orchestration components perform operations such as vol-                enforcing path normalization, introducing boundary checks,
ume mounting to provision persistent storage and host re-               or replacing path-based operations with file descriptor-based
sources. For example, the NVIDIA Container Toolkit performs             access. It also identifies cases where validation and use are
privileged mount operations to inject GPU drivers and de-               separated and recommends restructuring the code to ensure
vice nodes into containers [16]. After deployment, privileged           atomicity. These repairs are derived from the semantic struc-
components continue to access container-controlled paths for            ture of the vulnerability rather than isolated code patterns.
tasks such as file synchronization, artifact extraction, and               Despite these advantages, applying LLMs to real-world con-
state inspection. This kind of interaction also appears in              tainer codebases requires careful control of analysis scope and
emerging agent frameworks. For instance, OpenHands uses                 validation of results. Large codebases produce long execution
containerized workspaces to execute agent-generated code and            paths that exceed context limits, and generated fixes may in-
exchange artifacts with the host. Although these systems serve          troduce inconsistencies if not constrained by the original logic.
different purposes, they share the same security assumption             Effective use of LLMs therefore depends on structured inputs,
that privileged host processes must resolve and operate on              precise localization of relevant code, and explicit alignment
filesystem paths originating from an untrusted container con-           with security invariants.
text.
   Although this security assumption is fundamental to safe                  III. U NDERSTANDING PAT RA V ULNERABILITIES
host-container interactions, it is often overlooked in prac-               Although prior work characterized PaTra vulnerabilities in
tice when third-party developers build runtime extensions or            core container runtimes, our research of recent CVEs shows
application-level container services [17]. Some implementa-             that similar vulnerabilities now appear in a broader set of
tions fail to treat container-controlled paths as untrusted input       ecosystem components and remain exploitable at significant
and omit necessary boundary checks during path resolution.              impact. This section revisits PaTra vulnerabilities in the
Others attempt to enforce these checks but perform validation           broader container ecosystem, focusing on cases disclosed in
and object access in separate steps, which introduces a race            recent years. We analyze how recent vulnerabilities diverge
condition during pathname resolution. An attacker inside the            from previously studied patterns, and identify unresolved
container can exploit this gap by modifying intermediate                challenges that motivate our work.
filesystem states between validation and use, for example by
replacing directories or files with symlinks. By exploiting this        A. Threat Model
TOCTOU condition, the attacker can redirect privileged host                We study containerized environments where core runtimes
operations to unintended filesystem targets, escape container           (e.g., Docker, runc) and privileged extensions (e.g., NVIDIA
isolation, and access sensitive host resources.                         Container Toolkit, AI Sandbox) perform filesystem opera-
                                                                        tions on behalf of containers. The host operating system
B. LLMs in Vulnerability Detection and Remediation                      and these management components are trusted. We assume
   LLMs provide semantic reasoning capabilities that support            their privilege boundaries are correctly enforced, while their
vulnerability detection in complex software systems [18]. Tra-          implementations may still contain logic flaws in filesystem
ditional static analysis relies on predefined rules and syntactic       path handling.
matching, which limits its ability to capture violations of                We consider two attacker models that correspond to differ-
implicit security assumptions. In container systems, vulner-            ent stages of the container lifecycle. In the pre-start phase,
abilities often arise from incorrect handling of host-container         the attacker can supply a malicious container image or mount
interactions rather than explicit programming errors. Detecting         configuration. Although the container has not yet started, the
such issues requires tracking how container-controlled inputs           attacker fully controls the filesystem contents that will be
propagate across functions and whether privileged operations            loaded into the container environment. This allows the attacker
enforce isolation constraints.                                          to embed crafted symlinks, manipulate directory layouts, or
   LLMs analyze code by modeling execution semantics across             introduce other malicious filesystem objects that are later
multiple functions and contexts. In vulnerability detection,            processed by privileged host components during container
LLM traces the flow of path variables, identifies operations            initialization. In the runtime phase, the attacker further gains
that access the host filesystem, and determines whether these           control of a running container after deployment. At this stage,
operations rely on container-controlled inputs. It evaluates the        the attacker can directly execute code inside the container
ordering of validation and resolution steps and checks whether          and fully control its filesystem state. This includes creating,
the implementation preserves filesystem boundary invariants.            deleting, renaming, or replacing files and directories, as well
This process enables the identification of logic vulnerabilities        as dynamically introducing symlinks while privileged host
such as unsafe symlink resolution and non-atomic pathname               operations are accessing container-controlled paths.
handling, which are difficult to capture through rule-based                The attacker’s goal is to escape container isolation and
analysis.                                                               access host resources by exploiting privileged host operations
   LLMs also assist vulnerability repair by generating candi-           over container-controlled paths. We consider common host-
date patches that align with security invariants[19]. For path          container interfaces such as volume mounting, file copying,
traversal vulnerabilities, LLM suggests modifications such as           runtime resource injection, and filesystem synchronization.



                                                                    3
By supplying malicious filesystem inputs during initialization            This evolution is visible in the newer CVEs collected in
or actively modifying filesystem states during runtime path            Table I. Early cases were dominated by classic runtime oper-
resolution, the attacker can trigger path misresolution, causing       ations such as copy, mount, and container start. More recent
privileged host components to access unintended filesystem             cases appear in GPU-related initialization, multi-stage build
targets outside the intended container boundary.                       flows, and resource sharing. In these settings, the privileged
                                                                       component does not merely inspect a path string. It often
               TABLE I: PaTra Vulnerabilities                          resolves a path across several layers of code, helper utilities,
                                                                       and system interfaces before the final filesystem operation
  CVE ID               Component Lifecycle      Root Cause
                                                                       occurs. Each layer may apply local checks, but none of them
  CVE-2017-1002101     Kubernetes Pre-Start     TOCTOU                 alone preserves the full security property. The vulnerability
  CVE-2018-15664       Docker       Runtime     TOCTOU                 therefore emerges from the composition of individually rea-
  CVE-2019-10152       Podman       Runtime     Symlink
                                                                       sonable steps.
  CVE-2019-18466       Podman       Pre-Start   Symlink                Insight 2: Security invariants break boundaries, turning
  CVE-2019-5736        runc         Runtime     Symlink                PaTra from local into cross-component. Earlier vulnera-
  CVE-2019-16884       runc         Pre-Start   TOCTOU
                                                                       bilities in container often centered on one component that
  CVE-2019-19921       runc         Pre-Start   TOCTOU
                                                                       checked a path and later used it unsafely [20], [21]. Recent
  CVE-2020-10696       Podman       Pre-Start   Symlink                vulnerabilities more often span a chain of components that
  CVE-2021-30465       runc       Runtime       TOCTOU                 jointly process a container-controlled path. A runtime may
  CVE-2021-25741       Kubernetes Runtime       TOCTOU                 prepare the request, a helper utility may normalize or reopen
  CVE-2022-23648       Containerd Pre-Start     Symlink                the path, and a host-level operation may perform the final
  CVE-2023-0778        Podman       Pre-Start   TOCTOU                 access. A security invariant must be preserved across all stages
  CVE-2023-27561       Podman       Pre-Start   TOCTOU                 of the execution chain. When one component changes the rep-
  CVE-2023-28642       runc         Pre-Start   Symlink                resentation of the path, or when another component resolves
  CVE-2024-0132        NVIDIA       Pre-Start   TOCTOU                 it again under different privileges, the original assumption is
  CVE-2024-11218       Podman       Pre-Start   TOCTOU                 lost. This cross-component structure makes the vulnerability
  CVE-2024-21626       runc         Pre-Start   Symlink                harder to recognize and harder to remediate.
  CVE-2024-23651       Docker       Pre-Start   TOCTOU                    Moreover, the key issue is no longer only unsafe API use.
  CVE-2024-23652       Docker       Runtime     Symlink
                                                                       The central problem is the loss of a stable invariant that
  CVE-2025-23267       NVIDIA       Pre-Start   Symlink                binds the checked path to the object that is finally accessed.
  CVE-2025-23359       NVIDIA       Pre-Start   TOCTOU                 Once the path is handed from one component to another, its
  CVE-2025-31133       runc         Pre-Start   TOCTOU
  CVE-2025-47290       Containerd   Pre-Start   TOCTOU                 meaning may change. One component may see a container-
  CVE-2025-52565       runc         Pre-Start   TOCTOU                 local location, while another component later resolves the
  CVE-2025-52881       runc         Pre-Start   TOCTOU                 same text into a host-visible object. This mismatch turns
  CVE-2025-8941        Linux        Pre-Start   TOCTOU                 path handling into a semantic problem rather than a local
  CVE-2025-9566        Podman       Pre-Start   TOCTOU                 programming error. For this reason, recent PaTra cases are
                                                                       better understood as invariant violations across abstraction
                                                                       boundaries.
B. Evolution of PaTra Vulnerabilities
                                                                       C. Limitations of Existing Solutions
Insight 1: PaTra vulnerabilities have expanded into priv-
ileged ecosystem components beyond core container run-                    The persistence of PaTra vulnerabilities shows that current
times. Prior work characterized PaTra vulnerabilities in core          defenses do not match the threat model. The most common
container runtimes and established the main root causes as             remediation strategy for developers is to add more checks or
symlink traversal and TOCTOU in host-container path resolu-            move to a safer primitive. These changes often improve local
tion [7]. Recent vulnerabilities indicate that PaTra has evolved       correctness of a specific operation, yet they do not preserve
beyond the scope of prior runtime-centric analyses and now             the security invariant once the path crosses another component
manifests in a broader and less uniform ecosystem. The attack          or another execution phase. A validation result can be correct
surface is no longer limited to a small set of runtime primi-          at one step and irrelevant at the next step if the object is
tives. It now includes GPU container toolkits, build helpers,          reopened, reinterpreted, or replaced in between.
orchestration commands, and containerized workspaces that              Insight 3: Existing strategies fail to ensure invariant-
expose privileged filesystem operations to untrusted container         preserving detection and remediation across execution
content. These components reuse the same path semantics as             chains. On the one hand, kernel-level defenses can express
runtimes, yet they are developed in separate codebases and             strong isolation rules, yet they are so intrusive that can
often follow different security assumptions. The result is a           interfere with the normal operation of other functions. As a
wider ecosystem in which the same logical flaw can reappear            result, this strategy proposed in the previous work has not been
in new forms.                                                          accepted by the Linux mainline so far. Moreover, they also



                                                                   4
tend to be tied to a specific kernel assumption, while PaTra            repository features to concrete path-handling logic, Bulkhead
vulnerabilities increasingly appear in user-space extensions            avoids exhaustive code inspection while maintaining high
and ecosystem tools that sit outside the kernel boundary. A             detection precision.
kernel change may reduce one class of misuse, but it does not
automatically provide a practical remediation path for the large        B. Entry Function Identification
number of container utilities that already exist in the wild.             This stage identifies externally reachable functions that
This creates a persistent gap between theoretical protection            implement high-risk operations and grounds them in concrete
and practical remediation in real-world systems.                        code locations.
   On the other hand, case-by-case patching in the community
remains fundamentally limited. The history of PaTra vulnera-            High-Risk Functionality Pattern Summarization. We define
bilities shows that a patch applied to one component or one             high-risk functionalities as functional primitives that inherently
version can be bypassed or invalidated by subsequent changes            involve cross-boundary filesystem interactions which are prone
in related code. For example, CVE-2019-19921 [22] exposed               to isolation breaches. We first summarize these functionalities
a race condition in volume mount handling, where concurrent             into a knowledge base of semantic patterns derived from
operations could lead to unintended host filesystem access.             historical PaTra CVEs rather than searching for specific code
Later, CVE-2021-30465 [23] prompted modifications to path               flaws. Each pattern serves as a high-level abstraction of a
resolution and validation logic in order to address symlink-            vulnerable scenario that captures the functional intent such as
based traversal. These changes altered the mount handling               volume mounting or log collection as well as the interaction
workflow and unintentionally broke the assumptions that pre-            vector describing how container-provided paths propagate to
viously mitigated the race condition. As a result, the same             the host and the privilege context regarding security-critical
class of vulnerability reappeared as CVE-2023-27561 [24],               operations performed by the host-side component. We leverage
demonstrating a regression caused by incomplete preservation            LLM to normalize diverse historical vulnerabilities into a
of security properties across patches. This process shows               structured schema that results in a repository of patterns
that patches often address specific attack vectors without              grouping functions by their interaction semantics and risk
maintaining a consistent invariant across code evolution. This          profiles. This knowledge base provides the necessary context
pattern reflects a deeper limitation that existing approaches           for LLM to understand the nature of a sensitive operation
do not provide a unified mechanism to reason about path                 beyond simple keyword matching.
semantics across components, lifecycle stages, and execution            Enrty Point Localization. For a given repository, we first
orders. They also do not provide a systematic way to verify             collect repository-level context, including directory structures,
that a repair preserves the intended invariant under adversarial        README files, configuration files, and API definitions. Based
interleavings, which leaves fixes local and difficult to validate       on this information, we leverage LLM to map documented
at scale.                                                               functions to their corresponding implementation points in the
                                                                        source code. Concretely, we utilize LLM to examine function
                  IV. D ETECTION P IPELINE
                                                                        signatures, parameter types, and interface definitions, and
A. Overview                                                             correlate them with file paths, function boundaries, and naming
   Bulkhead implements a semantic-guided vulnerability de-              conventions to determine where each function is implemented.
tection pipeline that localizes the code responsible for privi-         The analysis also uses API specifications and configuration en-
leged host-container filesystem interactions. Fig. 1 illustrates        tries to resolve indirect mappings between externally exposed
the detection pipeline in Bulkhead.                                     interfaces and internal functions. We further distinguish ex-
   The process begins with repository-level semantic analy-             ported interfaces from internal helpers by checking visibility,
sis over project documentation and source code to identify              registration patterns, and invocation sites, which narrows the
features that perform privileged filesystem operations across           candidates to functions that can be externally triggered. The
the host-container boundary, such as volume mounting, file              result is a set of entry functions together with their source
synchronization, and resource injection. Once such a feature            locations and descriptive context.
is identified, Bulkhead maps it to its implementation entry                We then combine the identified functions, their associated
point and extracts the corresponding call chain. Bulkhead then          code, and the corresponding function descriptions with the
performs call-chain semantic analysis to locate the implemen-           high-risk functionalities patterns. LLM evaluates whether each
tation where privileged host operations interact with container-        function represents a high-risk interaction by jointly con-
controlled filesystem objects. This step narrows the analysis           sidering the declared functionality and its concrete imple-
from high-level feature logic to the code that enforces, trans-         mentation. The evaluation inspects input sources, argument
forms, or resolves container-derived paths. Finally, Bulkhead           propagation, and the use of privileged operations to determine
performs function-level semantic analysis on the identified             whether the function exhibits characteristics defined in high-
implementation and evaluates its behavior against the security          risk functionalities patterns. It also checks consistency between
invariants of container isolation to determine whether it intro-        documentation and implementation to filter cases where the
duces vulnerabilities such as unsafe symlink resolution or non-         described behavior is not realized in code. Functions that
atomic pathname handling. By narrowing the analysis from                satisfy the high-risk functionalities criteria are marked as high-



                                                                    5
                                               Fig. 1: Bulkhead Detection Pipeline.


risk, along with the relevant code regions and function-level           a concrete criterion for identifying relevant execution segments
context.                                                                within complex call-chains.
   We aggregate the identified high-risk functions, function
entry in repository, and the corresponding function descrip-            Interaction Related Call-Chain Extraction. We extract com-
tions as the output of this stage. Functions that only perform          plete function call chains from each identified entry function
intermediate processing, lack clear input interfaces, or are            using Joern [25]. The extracted call chains cover all reachable
only transitively invoked without independent exposure are              execution paths across files and modules and include argument
excluded. The resulting set forms a focused collection of high-         passing, intermediate transformations, and auxiliary logic.
risk entry functions with precise code grounding, which serves          These raw call chains contain a large amount of code that
as the basis for subsequent analysis.                                   does not contribute to container-host path interaction.
C. Function Call-Chain Extraction                                         We provide the full call chains together with the call-
   This stage identifies path-related execution segments from           chain patterns to LLM and require it to isolate the execution
full call chains and captures how container-controlled paths            segments that involve path handling across the container-host
propagate to host-side filesystem operations.                           boundary. LLM traces path variables from their input sources
                                                                        and follows their propagation through assignments, function
Call-Chain Pattern Summarization. Before extraction, we
                                                                        calls, and return values. It identifies operations that modify
use LLM to summarize call-chain patterns from historical Pa-
                                                                        path semantics, including normalization, prefix joining with
Tra CVEs by focusing on the recurring structure of container-
                                                                        host directories, and resolution steps that may dereference
host path interactions. Specifically, each pattern should capture
                                                                        a symlink. It further examines whether validation logic is
the lifecycle of a path variable originating from container-
                                                                        consistently enforced along the propagation path or becomes
controlled input and its propagation across multiple function
                                                                        ineffective after subsequent transformations.
boundaries until its eventual use in host-side filesystem op-
erations. These patterns emphasize critical semantic stages                Only the functions and statements that directly participate
such as parsing, normalization, and prefix concatenation where          in these path interactions are retained. Code that operates on
symlink handling frequently introduces vulnerabilities. We              internal paths, performs unrelated computation, or does not
represent these patterns as unified natural language descrip-           affect the final path resolution is removed. The resulting call-
tions that encode shared characteristics of path-related data           chain segment preserves the ordering of critical operations on
flow. This knowledge base directs LLM to focus on path-                 the path variable and exposes the exact sequence that leads to
related semantics rather than general control flow and provides         host-side filesystem access.



                                                                    6
D. PaTra Vulnerability Detection                                        the locations of path validation, path resolution, and privilege
                                                                        boundary crossing. The Exploitation field specifies attacker
   The refined code segments are provided to LLM for PaTra
                                                                        actions such as symlink construction, directory replacement,
vulnerability detection. This stage performs semantic matching
                                                                        or race triggering. The prompt enforces a fixed schema and
between concrete implementations and abstract vulnerability
                                                                        requires each field to align with evidence extracted from CVE
patterns. The framework integrates pattern knowledge derived
                                                                        descriptions. The resulting patterns are stored as reusable
from historical CVEs with code-level execution context. LLM
                                                                        templates and are directly used during detection.
receives both the reduced call-chain segments and the pattern
templates, and it evaluates whether the observed behavior               PaTra Vulnerability Detection. During the final detection
satisfies the invariant violation captured by each pattern.             phase, Bulkhead supplies LLM with the extracted function call
This design links high-level vulnerability semantics with low-          chain and the formalized vulnerability patterns. The prompt
level implementation details and enables consistent reasoning           defines a guided reasoning process based on the pattern struc-
across different codebases. The detection stage also preserves          ture. LLM first identifies candidate path variables that originate
traceability, since each decision is grounded in explicit pattern       from container-controlled inputs and traces their propagation
fields and concrete code locations.                                     across functions. LLM then locates validation operations and
                                                                        resolution operations along the call chain and determines their
PaTra Pattern Summarization. By analyzing the commonal-
                                                                        relative order. LLM also evaluates the privilege context of each
ities among existing container vulnerabilities from both logical
                                                                        operation and identifies whether a path crosses from container
and semantic perspectives, we summarize the fundamental
                                                                        scope to host scope.
patterns of PaTra vulnerabilities. Bulkhead constructs these
                                                                           LLM then compares the extracted execution structure with
patterns through an offline synthesis stage over historical
                                                                        each predefined pattern. The matching process checks whether
CVE reports. Each CVE is first normalized into a structured
                                                                        the observed behavior aligns with the invariant violation
textual description that includes execution phase, involved
                                                                        encoded in the pattern, including path origin, interaction
components, path flow, validation logic, and exploitation con-
                                                                        sequence, and privilege boundary. LLM produces a structured
ditions. The prompt used in this stage instructs LLM to
                                                                        output that includes the matched pattern type, the correspond-
extract invariant properties across multiple CVEs and to ignore
                                                                        ing code locations, and a reasoning trace that connects the call
implementation-specific details such as variable names or code
                                                                        chain to the pattern fields.
structure. The prompt requires LLM to identify three elements:
                                                                           Upon confirming a potential path traversal vulnerability,
the origin of the path, the sequence of path processing across
                                                                        Bulkhead generates a formalized bug report. This report in-
components, and the location where the security assumption
                                                                        cludes the vulnerability description, the matched pattern type,
fails. LLM then groups CVEs that share the same invariant
                                                                        the precise code locations, and the inferred threat model. The
violation and produces a generalized pattern description for
                                                                        framework synthesizes a proof of concept by instantiating
each group. This process yields a compact set of stable
                                                                        the Exploitation field of the matched pattern with concrete
vulnerability abstractions that capture the essential semantics
                                                                        parameters extracted from the code. LLM translates abstract
of PaTra.
                                                                        exploitation conditions into executable steps that follow the
   We categorize historical PaTra vulnerabilities into four dis-
                                                                        interaction sequence identified in the call chain. These steps
tinct classes based on two primary dimensions: the occurrence
                                                                        include file layout construction, symlink placement, and invo-
phase within the container lifecycle and the underlying root
                                                                        cation of the target interface. The generated proofs of concept
cause of the vulnerability. The lifecycle dimension separates
                                                                        are executed in an isolated testing environment to validate
operations into pre-start and runtime phases. The pre-start
                                                                        exploitability. This validation step ensures that the detected
phase includes image building, container creation, volume
                                                                        issue satisfies both semantic correctness and practical impact.
mounting, and initialization. The runtime phase includes file
copying, command execution, and volume exporting. The root-             E. Detection Findings and Security Insights
cause dimension distinguishes between direct path traversal by
symlinks and TOCTOU race conditions. Direct path traversal              Target Collection. To evaluate the practical effectiveness of
appears when path resolution does not enforce boundary                  Bulkhead, we conducted a systematic exploration of GitHub
constraints. TOCTOU conditions appear when validation and               to identify repositories related to the container ecosystem.
use are separated and the path object changes between these             We applied a hierarchical filtering process that first analyzed
steps.                                                                  repository metadata, including README files, configuration
   Combining these dimensions yields four specific vulnera-             files, and attached documentation, to determine the functional-
bility patterns: pre-start symlinks, pre-start TOCTOU, runtime          ity and scope of each repository. We further performed targeted
symlinks, and runtime TOCTOU. Bulkhead formalizes these                 web searches using repository names to obtain supplementary
patterns into a structured JSON representation. Each pattern            technical descriptions and project context.
contains three fields: Object, Interaction, and Exploitation. The          We combined the collected repository information and pro-
Object field defines the roles of host, container, and attacker,        vided it to LLM to determine whether the repository belonged
together with their capabilities and privilege levels. The In-          to the container ecosystem. The collected targets covered a
teraction field encodes the ordered execution steps and marks           diverse range of architectures, including container runtimes



                                                                    7
such as Docker and Nerdctl, hardware support systems such              Insight II: Generalizability: In addition to being present in
as NVIDIA Container Toolkit and Intel Device Plugin, and               traditional container management tools, the PaTra vulnera-
container-based AI sandbox environments such as OpenHands.             bility has also emerged in container-based AI sandbox.
This process produced a dataset of 82 candidate repositories.
We manually verified a stratified sample covering twenty per-             The second case involves OpenHands, which represents
cent of the dataset and confirmed that all selected repositories       a container-based AI sandbox environment that relies on
were within the intended research scope.                               container isolation to execute untrusted workloads. Bulkhead
Detection Results. Bulkhead was deployed on a diverse set              identifies a runtime vulnerability in the file transfer mechanism
of container runtimes, plugins, and sandbox environments to            between the client and the sandboxed Action Execution Server.
evaluate the prevalence of PaTra vulnerabilities in modern             In the V0 rumtime, the vulnerability arises from insufficient
container ecosystems. The framework identified 9 previously            path boundary enforcement in the copy from APIs. The server
undisclosed vulnerabilities that involve unsafe host-container         processes file operations using standard library functions that
path interactions. Bulkhead generated a functional PoC for             follow symlinks and do not restrict extraction paths to the
each case to validate exploitability. The PoCs demonstrate             intended workspace. An attacker with execution capability
complete attack paths from container-controlled inputs to priv-        inside the sandbox can create a symlink that points to a
ileged host resource access under realistic threat models. We          sensitive directory outside the workspace. When the client in-
submitted detailed reports to the corresponding maintainers,           vokes the download interface, the server traverses the symlink
including root cause analysis and patch suggestions derived            and packages the target files into an archive, which is then
from the detection results.                                            returned to the client. The attacker can extract the archive
                                                                       and access sensitive data. This vulnerability demonstrates
Insight I: Severity: There are still a number of PaTra                 that path traversal issues are not limited to traditional mount
vulnerabilities in modern container ecosystems.                        operations, and they also affect higher-level file interaction
                                                                       APIs in sandboxed environments.
   At the time of writing, 3 discovered vulnerabilities have
been assigned CVE identifiers, while the remaining cases are                            V. R EMEDIATION P IPELINE
under active review and patch development. The results show
that path interaction vulnerabilities continue to affect widely        A. Overview
used container components, including runtimes and auxiliary
                                                                          In this paper, remediation means generating a correct, verifi-
plugins. Existing defenses still fail to consistently enforce
                                                                       able patch for a detected PaTra vulnerability. To repair detected
filesystem boundary constraints during host-container path res-
                                                                       PaTra violations, we employ a model-checking-guided patch
olution and filesystem operations. These findings demonstrate
                                                                       pipeline to construct a verifiable patch. A valid patch must
that PaTra vulnerabilities remain an active security problem in
                                                                       satisfy the safety invariant identified during detection, compile
real-world container systems.
                                                                       within the affected codebase, and preserve normal container
Case Study. We present two representative cases to illustrate          operations. The primary difficulty in enforcing this invariant
the diversity and impact of the discovered vulnerabilities.            lies in identifying the precise source location to apply the fix.
   The first case involves Nerdctl, which represents a widely          For instance, repairing a TOCTOU path-resolution flaw re-
used container engine. Bulkhead identifies a pre-start vulner-         quires placing the patch exactly where it can bind a privileged
ability in the volume mounting procedure. The issue resides            operation to a validated object before an attacker alters the
in the ProcessFlagV function in mountutil.go, which resolves           filesystem state.
user-specified mount paths during container initialization. The           Fig. 2 illustrates the automated repair pipeline in Bulkhead.
function validates path existence but does not enforce path            This pipeline begins by passing detection artifacts to an
stability across resolution and use. In a scenario where mul-          LLM to synthesize candidate patches. The LLM analyzes
tiple containers share a common volume, an attacker can                the proof-of-concept exploit, the vulnerable call chain, and
manipulate the shared directory from a running container               the surrounding source code to locate the exact flaw and
and replace a legitimate subpath with a symlink that targets           generate a concrete fix. A compilation filter then discards any
a sensitive host location. When a new container is started             proposed code that fails to build within the target repository.
with a bind mount that references this subpath, the resolution         The verification backend processes the surviving patches by
process follows the manipulated link and mounts the host path          translating their repair logic into Promela code. An LLM maps
into the container. The attack enables unauthorized access to          the patched source code into a predefined model-checking
sensitive files on the host filesystem and leads to container          template specific to the detected PaTra pattern. The system
escape. The vulnerability reflects a violation of the invariant        then executes the SPIN model checker on this instantiated
that path validation must remain consistent with path usage            Promela model to evaluate adversarial filesystem interleavings
under concurrent modifications.                                        and verify the required safety invariant. A failed verification
                                                                       produces a counterexample that directly guides the next it-
                                                                       eration of patch synthesis. The pipeline ultimately outputs a



                                                                   8
deployable repair that integrates seamlessly into the codebase          for the next synthesis iteration. The counterexample exposes
and defends against the modeled attacker.                               the missing path-safety relation in the repaired logic. Typical
                                                                        failures include validation that is not bound to the subsequent
B. Candidate Patch Synthesis                                            privileged operation, unchecked path-resolution targets, and
LLM Patch Generation. The repair pipeline first synthesis               repairs that block legitimate in-boundary container layouts.
a candidate patch using an LLM. The synthesizer receives                The next synthesis iteration therefore receives counterexample-
detection artifacts, including PoC exploits, vulnerable call            guided evidence instead of a complete repair strategy embed-
chains, and surrounding source code. The LLM analyzes                   ded in the initial prompt.
these artifacts to locate the vulnerable operation and syn-
thesize a concrete patch for the affected repository. Unlike            D. Patch Findings and Security Insights
prior specification-guided LLM approaches that rely primarily           Runtime Validation Results. Runtime validation evaluates
on prompt-level constraints [26], Bulkhead enforces PaTra-              whether a generated patch blocks the concrete exploit while
specific safety invariants during backend verification.                 preserving legitimate container behavior. For each repro-
Sanity Filter. Before model checking, Bulkhead first applies            ducible newly discovered vulnerability, Bulkhead reconstructs
a compilation and applicability filter to the synthesized patch.        the affected repository version, runtime configuration, and PoC
The filter rejects edits that cannot replace the vulnerable             exploit. Before applying the generated patch, Bulkhead first
operation or fail to compile within the affected package. A             confirms that the PoC reproduces the reported host-container
passing result therefore indicates only that the candidate patch        boundary violation. After applying the patch, Bulkhead reruns
can be integrated into the target repository. The required PaTra        the same PoC and checks that the exploit no longer reaches the
safety invariant is enforced later by the verification backend          unsafe host-side target. The exploit also exercises legitimate
during path-safety model checking.                                      in-boundary path layouts to ensure that the repair does not
   Failed applicability checks produce compilation and inte-            reject benign container workflows.
gration feedback for the next patch-synthesis iteration. These             We performed runtime validation for eight of the nine
failures are resolved before verification and therefore do not          newly discovered vulnerabilities. All eight validated patches
enter the PaTra-specific model-checking stage. The verification         blocked the corresponding PoC after repair while preserving
backend can thus focus on validation-to-use binding, adversar-          the benign in-boundary cases covered by the harness. These
ial path mutations, and host-container boundary confinement             validated patches provide the repair artifacts that we prepare
rather than repository-level patch inconsistencies.                     for responsible disclosure and upstream submission. We ex-
                                                                        clude the OpenHands case from runtime validation because
C. Pattern-Template Model Checking                                      the vulnerable function was no longer present in the upstream
Template Instantiation. At the model-checking stage, Bulk-              version used for reconstruction.
head instantiates a PaTra verification template for the syn-               Runtime validation complements repository applicability
thesized patch. Each template defines the attacker capability,          and pattern-template model checking. Applicability checks
the abstract state space, and the required path-safety invariant        whether a patch can be integrated into the target codebase,
for the detected vulnerability class. The verification backend          model checking verifies the PaTra invariant under the modeled
then evaluates the repaired logic under adversarial filesystem          attacker, and runtime validation exercises the repaired system
interleavings. For path-resolution vulnerabilities, the verifier        against a concrete PoC execution.
checks three properties. Privileged operations must remain              Over-Restrictive Historical Fixes. Pattern-template model
bound to validated objects. Attacker-controlled path mutations          checking exposes over-restrictive repair behavior in histori-
must not redirect operations outside the allowed host-container         cal CVE fixes. In three historical cases, the repair prevents
boundary. Legitimate in-boundary filesystem layouts must                boundary escape by rejecting symbolic links entirely.
remain accessible after repair.
Model Checking Verification and Feedback. The verification              Insight III: Compatibility: Exploit-blocking patches may
backend maps each repository-applicable candidate into this             still be over-restrictive by rejecting legitimate in-boundary
fixed abstraction. The LLM-assisted translator encodes how              symbolic links.
the candidate changes the modeled repair behavior. It cannot
redefine the attacker, weaken the safety invariant, or reduce              This strategy blocks symlink-based exploits, but it also
the checked state space. The PaTra pattern therefore acts               rejects benign symbolic links whose resolved targets remain
as an executable security constraint rather than a descriptive          inside the intended workspace or host–container boundary.
vulnerability label. Bulkhead rejects candidates that apply             Such repairs satisfy a narrow exploit-blocking objective, but
cleanly to the repository but still permit unsafe path-resolution       they fail to preserve legitimate in-boundary filesystem be-
behavior. It then checks the instantiated Promela model with            havior. This finding shows that PaTra repair should enforce
Spin [27].                                                              boundary confinement without disabling valid path layouts.
   When model checking detects a violation, the verification            Case Study. We use the Nerdctl shared-volume vulnerability
backend converts the counterexample into repair feedback                to show why Bulkhead does not treat an LLM-generated patch



                                                                    9
                                                Fig. 2: Bulkhead Patch Pipeline.




                                      Fig. 3: Nerdctl repair failure pattern in pseudocode.


as a final repair. The detection stage classifies this case as a           Fig. 3 illustrates this failure mode. Panel (a) shows the
pre-start TOCTOU vulnerability in the bind-mount path. The              vulnerable bind-source flow. The source path reaches the bind-
vulnerable call chain reaches the mount utility code, where             mount operation without a relation that prevents symlink redi-
a user-controlled bind source is eventually passed into the             rection or later path mutation. Panel (b) shows a direct LLM
privileged bind-mount operation. The repair challenge is not            repair that adds a plausible path-level check before the bind
only to add a path check, but to ensure that the value validated        operation. This candidate is not merely a malformed patch.
by the patch remains bound to the value consumed by the later           It survives the repository-level applicability stage and reaches
mount operation.                                                        model checking. However, the pattern-template verifier rejects
                                                                        it because the check and the privileged use remain separable
Insight IV: Soundness: Repository-applicable LLM patches                under adversarial filesystem interleavings. The counterexample
are not necessarily semantically safe under PaTra invariants.           follows a simple sequence: the check observes a normal path,
                                                                        the attacker swaps the path to an escaping symlink, and the



                                                                   10
bind operation later consumes the mutated target.                         combination ensures that the dataset captures both historical
   This case demonstrates the limitation of LLM-only repair.              vulnerability and emerging attack surfaces, and it reflects
The LLM can identify a relevant source location and insert                the evolution of cross-boundary filesystem interactions in
security-looking code, but the generated edit may still miss              contemporary systems.
the PaTra relation required by the vulnerability class. A com-            Verification of the Pipeline. We execute the complete Bulk-
pilation or applicability filter cannot expose this semantic gap          head pipeline on the dataset to validate its detection and
because the patch is a valid source-level artifact. The model             patching capabilities. The framework successfully detects all
checker exposes the gap by evaluating the candidate under the             36 vulnerabilities, which demonstrates its ability to capture
attacker model encoded by the selected PaTra template.                    complex cross-component interaction patterns and invariant vi-
   Bulkhead converts this counterexample into repair feedback             olations without manual intervention. Moreover, the detection
for the next synthesis iteration. The feedback does not provide           process accurately identifies the origin of functionality entry,
a complete repair recipe. It identifies the missing security rela-        the sequence of path resolution operations, and the violation
tion: the repaired bind source must be validated in a way that            points where container and host interacts.
remains connected to the later bind-mount use. Panel (c) shows               For the 27 known CVEs, Bulkhead generates patches that
the feedback-guided repair. The revised candidate passes the              are consistent with the final versions merged into the corre-
selected pattern-template model check because the modeled                 sponding open-source projects. The generated patches enforce
repair behavior no longer permits the attacker to redirect                invariant-preserving strategies such as binding validation to
the validated bind source outside the allowed host–container              use and avoiding unsafe path re-resolution. This consistency
boundary.                                                                 indicates that the framework can synthesize remediation strate-
   This case supports Bulkhead’s verification-guided design.              gies that align with practical development constraints and
The LLM is useful for locating and editing complex source                 established security practices.
code, but model checking supplies the security judgment that
the LLM cannot provide by itself. The static filter establishes           B. Ablation Study
that a candidate can be integrated into the repository. The
PaTra template establishes whether the candidate satisfies                   We conduct an ablation study to quantify the contribution of
the required path-safety invariant under the modeled attacker.            key components in the framework. The analysis is performed
Together, these stages turn LLM repair from a best-effort code            on the full dataset of 36 vulnerabilities. Each experiment
generation step into an iterative and verifiable repair process.          removes one core design element while keeping the rest of
                                                                          the pipeline unchanged. The evaluation measures detection
                       VI. E VALUATION                                    accuracy in terms of false negatives and false positives. This
   This section evaluates the effectiveness and robustness of             study demonstrates how structured knowledge and semantic
the Bulkhead framework in detecting and repairing PaTra                   constraints improve both completeness and reliability of the
vulnerabilities, and the evaluation follows the threat model              framework, and it highlights the necessity of each component
and vulnerability characteristics described in section III. The           in maintaining stable reasoning over complex call chains and
evaluation focuses on three aspects. It measures the end-to-              cross-boundary interactions.
end capability of the framework on a comprehensive dataset                Detection Pipeline. We analyze the ablation results by align-
that covers diverse vulnerability types and lifecycle phases.             ing each removed component with its role in the detection
It verifies whether the generated patches preserve security               pipeline, including entry function identification, call-chain
invariants and remain consistent with real-world fixes. It                extraction, and pattern-guided reasoning. The LLM we use
analyzes the contribution of each core component through                  is Claude Opus 4.6.
ablation experiments, which reveals how semantic patterns and                Removing high-risk function identification primarily af-
structured reasoning improve detection precision and stability.           fects entry point localization. The framework fails to consis-
                                                                          tently identify externally reachable functions that implement
A. Effectiveness of the Proposed Framework
                                                                          security-sensitive operations, which leads to incomplete cov-
   We first evaluate the effectiveness of Bulkhead from both              erage of relevant execution. As shown in Table II, this setting
detection and remediation perspectives through Claude Opus                has detected 25 out of 36 vulnerabilities and introduces 11
4.6 [28]. The evaluation examines whether the framework can               false negatives (30.6%). The missed cases are concentrated
accurately identify vulnerabilities that span multiple compo-             in scenarios where vulnerable behaviors are exposed through
nents and execution stages, and whether it can generate correct           indirect interfaces or require precise mapping from documen-
patches that satisfy the security requirements of real-world              tation to implementation. The relatively low false positive rate
systems.                                                                  indicates that the analysis remains conservative, but it lacks
Dataset. The evaluation dataset consists of 36 PaTra vulnera-             sufficient recall due to missing entry points.
bilities, which provide a representative benchmark for logic                 Moreover, repository-level documentation provides essen-
vulnerability analysis in container ecosystems. The dataset               tial constraints for interpreting the security assumptions of
includes 27 publicly CVEs in Table I and 9 previously undis-              exposed functionalities and helps distinguish implementation
closed PaTra vulnerabilities described in section IV-E. This              flaws from intended design limitations. For example, the



                                                                     11
                           TABLE II: Ablation Study on Bulkhead’s Detection Pipeline Components

  Configuration                        Total   Pre-Sym     Pre-TOCTOU            Run-Sym     Run-TOCTOU          FN(%)         FP(%)
  Bulkhead                              36        11             15                  4              6           0 (0.0%)      0 (0.0%)
  w/o High-Risk Functions               25         7              9                  3              6          11 (30.6%)     2 (5.6%)
  w/o Related Call-Chain Extraction     19         6              6                  2              5          10 (27.8%)     7 (19.4%)
  w/o PaTra Detection Patterns          11         3              4                  2              2          12 (33.3%)    13 (36.1%)



nerdctl cp operation matches a typical PaTra interac-                     can be localized, and the repair objective can be mapped to a
tion pattern in code, where container-controlled paths may                PaTra pattern and evaluated by our verification oracle. Cases
affect host-side filesystem operations. However, the official             lacking source-level repair evidence, reproducible vulnerable
documentation explicitly restricts this functionality to trusted          revisions, or a clear PaTra repair objective are excluded.
and cooperative containers and does not guarantee protection              For the retained historical cases, we normalize the inputs by
under adversarial conditions[29]. Bulkhead therefore places               reconstructing vulnerable source windows and line-anchored
this behavior outside the considered threat model and does                call-chain context, while using ground-truth patches only for
not classify it as a vulnerability. Incorporating such repository-        benchmark construction and not as model input.
level constraints prevents unsafe-by-design functionality from
being misidentified as a security issue and improves the                     We compare direct LLM repair with the full Bulkhead
precision of entry function identification.                               pipeline across five contemporary frontier LLMs: Claude Opus
                                                                          4.6 [30], GPT-5.5 [31], Gemini-3.1 Pro [32], Qwen 3.6-
   Removing related call-chain extraction impacts the semantic
                                                                          Plus [33], and DeepSeek-V4-Pro [34]. Both settings receive
completeness of execution paths. The extracted call chains
                                                                          the same vulnerability report, call-chain context, and vulner-
either omit critical transitions or include unrelated logic, which
                                                                          able source window. The direct baseline generates a patch
disrupts the consistency of path propagation analysis. this
                                                                          in a single pass and is evaluated by the same static patch
setting has detected 19 out of 36 vulnerabilities and produces
                                                                          sanity filter. Bulkhead additionally uses static diagnostics and
7 false positives (19.4%), which is significantly higher than
                                                                          PaTra-template model-checking counterexamples as feedback
other configurations. The increase in false positives reflects
                                                                          for iterative repair.
that incomplete or noisy call chains lead to incorrect associ-
ations between path operations and host-side effects. At the                The results show that repository applicability and se-
same time, 10 false negatives (27.8%) indicate that missing               mantic path-safety verification are complementary. Bulk-
code prevents the framework from capturing full interaction               head improves the average Success Rate from 51.5% to
semantics required for vulnerability identification.                      81.5%, a gain of 30.0 percentage points. This indicates
   Removing PaTra detection patterns affects the final reason-            that feedback-guided repair produces substantially more
ing stage. Without structured pattern constraints, the analysis           repository-applicable patches than direct one-shot LLM repair.
relies solely on LLM to interpret execution semantics, which
leads to unstable and inconsistent decisions. This configuration             At the same time, Bulkhead reduces the average Vul-
has detected only 11 out of 36 vulnerabilities, with 12 false             nerability Rate from 41.3% to 18.5%, a reduction of 22.8
negatives (33.3%) and 13 false positives (36.1%). The simulta-            percentage points. This gap shows that repository-applicable
neous increase in both error types shows that pattern guidance            patches are not necessarily semantically safe under adversarial
is necessary to anchor the analysis to security invariants and            path-resolution behavior. The strongest example is GPT-5.5,
to maintain alignment between path operations and boundary-               whose Vulnerability Rate drops from 68.8% under direct
crossing behaviors.                                                       repair to 4.2% under Bulkhead. This result is particularly
   These results show that each component contributes to                  informative because the patch-synthesis model is the same in
a distinct aspect of the detection process. Entry function                both settings; the improvement comes from the static-feedback
identification determines the coverage of analysis, call-chain            and model-checking-feedback loops rather than from changing
extraction preserves semantic correctness across execution                the underlying LLM.
paths, and detection patterns provide constraints that stabilize             Because Vulnerability Rate is conditioned on successful
reasoning. The degradation patterns observed in Table II are              candidates, individual model-level changes should be inter-
consistent with this decomposition and demonstrate that accu-             preted together with the absolute number of verification-safe
rate detection requires the integration of all three components.          repairs. For example, Claude Opus 4.6 shows a slight increase
Remediation Pipeline. We evaluate Bulkhead on a repair-                   in conditional Vulnerability Rate, from 9.1% to 13.0%, but
evaluable benchmark of 26 PaTra vulnerabilities, including                Bulkhead also increases its number of successful patches from
8 newly discovered cases and 18 historical CVEs. The his-                 11 to 23. Overall, the results indicate that direct LLM repair
torical cases are selected from a broader pool of publicly                often produces patches that are syntactically plausible but
disclosed container-runtime CVEs only when the vulnerable                 semantically unsafe, while Bulkhead improves both repository
revision can be identified, the security-relevant source path             applicability and PaTra-level safety.



                                                                     12
                                               TABLE III: Effectiveness of Bulkhead Patching

     Metric            Setting      Claude Opus 4.6          GPT-5.5        Gemini-3.1 Pro Qwen 3.6-Plus DeepSeek-V4-Pro Average
                    Baseline          42.3% (11/26)       61.5% (16/26)      69.2% (18/26)      57.7% (15/26)        26.9% (7/26)          51.5%
     Success Rate ↑ Bulkhead          88.5% (23/26)       92.3% (24/26)      88.5% (23/26)      84.6% (22/26)        53.8% (14/26)         81.5%
                    ∆                   +46.2 pp            +30.8 pp           +19.3 pp           +26.9 pp             +26.9 pp           +30.0 pp
                       Baseline        9.1% (1/11)        68.8% (11/16)         38.9% (7/18)     46.7% (7/15)         42.9% (3/7)          41.3%
     Vuln. Rate ↓      Bulkhead        13.0% (3/23)        4.2% (1/24)          26.1% (6/23)     13.6% (3/22)         35.7% (5/14)         18.5%
                       ∆                 +3.9 pp             -64.6 pp             -12.8 pp         -33.1 pp              -7.2 pp          -22.8 pp
     Averages are unweighted means over model-level rates, not pooled case counts. Vulnerability Rate is conditioned on candidates passing the static
    patch sanity filter; lower is better.



                      VII. R ELATED W ORK                                       as-a-judge mechanism to validate the generated rationales.
                                                                                Li et al. [41] combined agentic planning with classic anal-
Container Isolation Security. To mitigate the container                         ysis primitives to achieve scalable exploration of privilege
escape, researchers have focused on hardening the kernel’s                      escalation flaws in microservices. Wei et al. [42] introduced
logical boundaries. Li et al. [7] identified systematic path-                   a multi-agent conversational framework that identifies logic
misresolution vulnerabilities and addressed them through Pa-                    vulnerabilities through iterative collaboration and a specialized
trol, a kernel extension that enforces dentry-based access                      buffer-of-thought mechanism.
control during path lookups. Shifting from path logic to data
                                                                                LLM-Based Patch Generation. Researchers utilize special-
integrity, Xu et al. [35] introduced Condo, which utilizes
                                                                                ized prompting strategies and iterative feedback loops to en-
trusted execution environments to protect critical kernel per-
                                                                                hance the intrinsic reasoning capabilities of LLMs for program
mission structures. Unlike localized fixes, Condo provides
                                                                                repair. Ahmed et al. [43] employed self-consistency techniques
a transparent, low-overhead scheme for safeguarding non-
                                                                                that identify optimal fixes by selecting the most frequent
control flow data against unauthorized tampering.
                                                                                solutions across multiple reasoning paths. Kulsum [44] in-
   Beyond software-only defenses, leveraging hardware prim-
                                                                                tegrated chain-of-thought reasoning with execution feedback
itives has become a key trend for achieving strong isolation
                                                                                from compilers and security sanitizers to refine candidate
from untrusted hosts. Zhou et al. [36] leverage ARM CCA
                                                                                patches iteratively. Nong et al. [45] developed an adaptive
hardware primitives to minimize the trusted computing base.
                                                                                framework that extracts vulnerability semantics and employs
Their RContainer architecture employs per-container shims
                                                                                multi-faceted validation to improve repair quality in real-world
and a lightweight mini-OS to isolate workloads from untrusted
                                                                                scenarios. Kim et al. [46] utilized tree-of-thought prompting to
hosts, effectively shifting the security boundary from kernel
                                                                                decompose the patching process into distinct stages that span
software to hardware-enforced realms. Marchand et al. [37]
                                                                                from fault localization to fix strategy formulation.
introduced sandbox-escape-bench to quantify the risk of LLM-
                                                                                   Hybrid frameworks combine the generative flexibility of
driven exploits. Their evaluation reveals that frontier models
                                                                                LLMs with the rigor of formal methods to provide stronger
can autonomously weaponize container misconfigurations and
                                                                                security guarantees. Tihanyi et al. [47] integrated bounded
kernel flaws, highlighting an emerging threat vector that de-
                                                                                model checking with LLMs to guide the repair process through
mands more resilient, automated defense mechanisms.
                                                                                counterexamples and stack traces. This approach ensures that
LLM-Based Vulnerability Detection. Current research fo-                         the model checker verifies each repaired program before final
cuses on enhancing the reasoning capabilities of LLMs                           output. Orvalho et al. [48] implemented a counterexample-
through external knowledge integration and hybrid analysis                      guided inductive synthesis loop that utilizes MaxSAT-based
frameworks. Knowledge-augmented and specification-guided                        fault localization to generate program sketches. These sketches
methods utilize historical security data to constrain LLM                       provide a structured template that guides LLMs toward syn-
hallucinations and provide semantic ground truth. Du et al.                     thesizing correct code while the system refines results through
[38] developed a retrieval-augmented framework that distills                    continuous test suite validation.
multi-dimensional knowledge from CVEs to help models
distinguish between vulnerable and patched code. Zhu et al.                                            VIII. C ONCLUSION
[26] extracted reusable security specifications from historical                    In this paper, we present Bulkhead, an automated frame-
patches to enable models to compare target code against                         work that integrates LLM with formal methods to detect and
expected safe behaviors. In domain-specific tasks, Li et al.                    remediate PaTra vulnerabilities in container ecosystems. The
[39] combined chain-of-thought prompting with specialized                       framework generalizes multi-dimensional semantic patterns
cryptographic knowledge bases to verify logic compliance.                       from historical PaTra vulnerabilities to locate high-risk cross-
   Hybrid analysis and agentic architectures integrate LLMs                     boundary interactions, extract relevant call chains, and identify
with traditional program analysis to address complex system                     PaTra vulnerabilities. It further generates PoC exploits and
interactions. Li et al. [40] enriched detection prompts with                    produces patches that model checking verifies against safety
execution and data-flow contexts while employing an LLM-                        invariants. Through systematic analysis of 82 container-related



                                                                           13
repositories, Bulkhead uncovers nine previously undisclosed                          [21] M. S. Haq, T. D. Nguyen, A. Ş. Tosun, F. Vollmer, T. Korkmaz, and A.-
PaTra vulnerabilities, three of which have received CVE                                   R. Sadeghi, “Sok: A comprehensive analysis and evaluation of docker
                                                                                          container attack and defense mechanisms,” in Proceedings of the 2024
assignments. These contributions deepen the understanding                                 IEEE Symposium on Security and Privacy. IEEE, 2024, pp. 4573–4590.
of emerging container escape risks and provide a practical                           [22] “CVE-2019-19921,” https://nvd.nist.gov/vuln/detail/cve-2019-19921.
pathway toward stronger filesystem isolation in modern cloud                         [23] “CVE-2021-30465,” https://nvd.nist.gov/vuln/detail/cve-2021-30465.
                                                                                     [24] “CVE-2023-27561,” https://nvd.nist.gov/vuln/detail/cve-2023-27561.
and AI systems.                                                                      [25] “joern,” https://github.com/joernio/joern.
                                                                                     [26] H. Zhu, J. Li, C. Gao, J. Qian, Y. Dong, H. Liu, L. Wang, Z. Wang,
                                                                                          X. Hu, and G. Li, “Specification-guided vulnerability detection with
                             R EFERENCES                                                  large language models,” arXiv preprint arXiv:2511.04014, 2025.
                                                                                     [27] G. J. Holzmann, “The model checker SPIN,” IEEE Transactions on
 [1] O. Jarkas, R. Ko, N. Dong, and R. Mahmud, “A container security                      Software Engineering, vol. 23, no. 5, pp. 279–295, 1997.
     survey: Exploits, attacks, and defenses,” ACM Computing Surveys,                [28] Anthropic, “Claude Opus 4.6,” https://docs.anthropic.com/, 2026, [On-
     vol. 57, no. 7, pp. 1–36, 2025.                                                      line; accessed May 7, 2026].
 [2] N. Zhou, Y. Yao, X. Liang, S. Yao, C. Yang, and W. Gui, “Optimization           [29] “Nerdctl cp,” https://github.com/containerd/nerdctl/blob/main/docs/
     and evaluation of container-based ethercat communication in virtual                  command-reference.md#whale-nerdctl-cp.
     plcs,” IEEE Transactions on Industrial Electronics, pp. 1–12, 2026.             [30] Anthropic, “Claude Opus 4.6,” https://www.anthropic.com/news/
 [3] “Build better software with autonomous cloud agent,” https://openhands.              claude-opus-4-6, 2026, accessed: 2026-05-07.
     dev/product.                                                                    [31] OpenAI, “GPT-5.5 Model,” https://developers.openai.com/api/docs/
 [4] T. Zhang, X. Liu, B. Fan, and Y. Huang, “Container path mis-resolution               models/gpt-5.5, 2026, [Online; accessed May 7, 2026].
     escape detection method based on ebpf,” in 2025 3rd International               [32] Google, “Gemini 3.1 Pro Preview,” https://ai.google.dev/gemini-api/
     Conference on Big Data and Privacy Computing. IEEE, 2025, pp.                        docs/models/gemini-3.1-pro-preview, 2026, [Online; accessed May 7,
     60–69.                                                                               2026].
 [5] X. Yu, T. Xiong, W. Tang, Y. Jiang, Z. Wei, H. Wang, C. Chen, Y. Wang,          [33] Qwen Team, Alibaba Group, “Qwen3.6,” https://github.com/QwenLM/
     B. Peng, and Z. Qi, “Wasc: Hardening webassembly sandboxes via                       Qwen3.6, 2026, [Online; accessed May 7, 2026].
     system interface decoupling,” ACM Transactions on Architecture and              [34] DeepSeek-AI, “DeepSeek-V4-Pro,” https://huggingface.co/deepseek-ai/
     Code Optimization, vol. 23, no. 1, pp. 1–23, 2026.                                   DeepSeek-V4-Pro, 2026, [Online; accessed May 7, 2026].
 [6] “CVE-2024-0132,” https://nvd.nist.gov/vuln/detail/cve-2024-0132.                [35] S. Xu, Y. Wang, L. Lei, K. Sun, J. Jing, S. Ma, J. Wang, and H. Huang,
 [7] Z. Li, W. Liu, X. Wang, B. Yuan, H. Tian, H. Jin, and S. Yan, “Lost                  “Condo: enhancing container isolation through kernel permission data
     along the way: Understanding and mitigating path-misresolution threats               protection,” IEEE Transactions on Information Forensics and Security,
     to container isolation,” in Proceedings of the 2023 ACM SIGSAC                       vol. 19, pp. 6168–6183, 2024.
     Conference on Computer and Communications Security, 2023, pp.                   [36] Q. Zhou, W. Cao, X. Jia, P. Liu, S. Zhang, J. Chen, S. Xu, and
     3063–3077.                                                                           Z. Song, “Rcontainer: A secure container architecture through extending
 [8] “CVE-2018-15664,” https://nvd.nist.gov/vuln/detail/cve-2018-15664.                   arm cca hardware primitives.” in Proceedings of the 2025 Network and
 [9] “CVE-2019-14271,” https://nvd.nist.gov/vuln/detail/CVE-2019-14271.                   Distributed System Security Symposium, 2025.
[10] “Pouch Container Document,” https://pouchcontainer.io.                          [37] R. Marchand, A. O. Cathain, J. Wynne, P. M. Giavridis, S. Deverett,
[11] L. Chen, Y. Ma et al., “Research on mobile application local denial of               J. Wilkinson, J. Gwartz, and H. Coppock, “Quantifying frontier llm capa-
     service vulnerability detection technology based on rule matching,” in               bilities for container sandbox escape,” arXiv preprint arXiv:2603.02277,
     2019 IEEE International Conference on Energy Internet. IEEE, 2019,                   2026.
     pp. 585–590.                                                                    [38] X. Du, G. Zheng, K. Wang, Y. Zou, Y. Wang, W. Deng, J. Feng, M. Liu,
[12] P. Fiterau-Brostean, B. Jonsson, K. Sagonas, and F. Tåquist, “Automata-             B. Chen, X. Peng, T. Ma, and Y. Lou, “Vul-rag: Enhancing llm-based
     based automated detection of state machine bugs in protocol implemen-                vulnerability detection via knowledge-level rag,” ACM Transactions on
     tations.” in Proceedings of the 2023 Network and Distributed System                  Software Engineering and Methodology, 2026.
     Security Symposium, 2023.                                                       [39] Z. Li, Z. Ji, T. Zheng, H. Ren, and X. Lan, “Cryptoscope: Utilizing
[13] E. W. Biederman and L. Networx, “Multiple instances of the global                    large language models for automated cryptographic logic vulnerability
     linux namespaces,” in Proceedings of the Linux Symposium, vol. 1,                    detection,” arXiv preprint arXiv:2508.11599, 2025.
     no. 1. Citeseer, 2006, pp. 101–112.                                             [40] Y. Li, X. Li, H. Wu, M. Xu, Y. Zhang, X. Cheng, F. Xu, and S. Zhong,
[14] “cgroups(7) – Linux manual page,” https://www.man7.org/linux/                        “Everything you wanted to know about llm-based vulnerability detection
     man-pages/man7/cgroups.7.html.                                                       but were afraid to ask,” arXiv preprint arXiv:2504.13474, 2025.
[15] A. Chen, Z. Guo, Z. Jin, Z. Li, and Y. Chen, “Breaking the bulkhead:            [41] P. Li, H. Y. Chong, Y. Cao, and J. Yang, “Detecting privilege escalation
     Demystifying cross-namespace reference vulnerabilities in kubernetes                 in polyglot microservices via agentic program analysis,” in Proceedings
     operators,” in Proceedings of the 2026 Network and Distributed System                of the 2026 IEEE Symposium on Security and Privacy, 2026.
     Security Symposium, 2026, pp. 1–20.                                             [42] Z. Wei, J. Sun, Y. Sun, Y. Liu, D. Wu, Z. Zhang, X. Zhang, M. Li,
[16] “NVIDIA         Container      Toolkit,”    https://github.com/NVIDIA/               Y. Liu, C. Li, M. Wan, J. Dong, and L. Zhu, “Advanced smart contract
     nvidia-container-toolkit.                                                            vulnerability detection via llm-powered multi-agent systems,” IEEE
[17] T. Zheng, Q. Hou, H. Ren, X. Chen, G. Deng, T. Zhang, G. Xu, and                     Transactions on Software Engineering, vol. 51, no. 10, pp. 2830–2846,
     H. Li, “kubesec: Automatic detection of takeover risks introduced by                 2025.
     third-party apps in the kubernetes ecosystem,” IEEE Transactions on             [43] T. Ahmed and P. Devanbu, “Better patching using llm prompting, via
     Dependable and Secure Computing, pp. 1–14, 2026.                                     self-consistency,” in 2023 38th IEEE/ACM International Conference on
[18] J. Lin and D. Mohaisen, “From large to mammoth: A comparative                        Automated Software Engineering, 2023, pp. 1742–1746.
     evaluation of large language models in vulnerability detection.” in             [44] U. Kulsum, H. Zhu, B. Xu, and M. d’Amorim, “A case study of llm
     Proceedings of the 2025 Network and Distributed System Security                      for automated vulnerability repair: Assessing impact of reasoning and
     Symposium, 2025.                                                                     patch validation feedback,” in Proceedings of the 1st ACM International
[19] H. Wu, C. Barrett, and N. Narodytska, “Lemur: Integrating large                      Conference on AI-Powered Software, 2024, pp. 103–111.
     language models in automated program verification,” in International            [45] Y. Nong, H. Yang, L. Cheng, H. Hu, and H. Cai, “{APPATCH}:
     Conference on Learning Representations, vol. 2024, 2024, pp. 2968–                   Automated adaptive prompting large language models for {Real-World}
     2978.                                                                                software vulnerability patching,” in Proceedings of the 34th USENIX
[20] Z. Li, J. Cheng, Q. Chen, E. Guan, Z. Bian, Y. Tao, B. Zha, Q. Wang,                 Security Symposium, 2025, pp. 4481–4500.
     W. Han, and M. Guo, “{RunD}: A lightweight secure container runtime             [46] Y. Kim, S. Shin, H. Kim, and J. Yoon, “Logs in, patches out: Au-
     for high-density deployment and high-concurrency startup in serverless               tomated vulnerability repair via {Tree-of-Thought}{LLM} analysis,” in
     computing,” in 2022 USENIX Annual Technical Conference, 2022, pp.                    Proceedings of the 34th USENIX Security Symposium, 2025, pp. 4401–
     53–68.                                                                               4419.




                                                                                14
[47] N. Tihanyi, Y. Charalambous, R. Jain, M. A. Ferrag, and L. C. Cordeiro,
     “A new era in software security: Towards self-healing software via
     large language models and formal verification,” in 2025 IEEE/ACM
     International Conference on Automation of Software Test. IEEE, 2025,
     pp. 136–147.
[48] P. Orvalho, M. Janota, and V. M. Manquinho, “Counterexample guided
     program repair using zero-shot learning and maxsat-based fault local-
     ization,” in Proceedings of the 2025 AAAI Conference on Artificial
     Intelligence, vol. 39, no. 1, 2025, pp. 649–657.




                                                                               15
