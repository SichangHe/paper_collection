                                             Automated Side-Channel Analysis of Cryptographic Protocol
                                                                Implementations
                                                       Faezeh Nasrabadi                                 Robert Künnemann                                 Hamed Nemati
                                                  CISPA Helmholtz Center for                         CISPA Helmholtz Center for                KTH Royal Institute of Technology
                                                      Information Security                              Information Security                         Stockholm, Sweden
                                                     Saarbrücken, Germany                              Saarbrücken, Germany                           hnnemati@kth.se
                                                   faezeh.nasrabadi@cispa.de                        robert.kuennemann@cispa.de

                                         Abstract                                                                      the specification level (e.g., the POODLE attack on SSL version
                                         Formal verification of cryptographic protocols typically relies on            3.0, which exploited SSL’s use of CBC-mode encryption with pre-
                                         symbolic models that abstract away compiled code and microarchi-              dictable padding [26]) and at the implementation level (e.g., Heart-
                                         tectural side channels, leaving a gap between verified specifications         bleed, CVE-2014-0160). Formal methods can provide a systematic
                                         and deployed executables. We present a toolchain that extracts                framework for finding attacks and even ensuring the absence of
                                         protocol-relevant models from real binaries and analyzes them                 (defined classes of) them. But to find attacks on both levels, we
                                         under explicit leakage contracts for constant-time and Spectre-               need models that capture the behavior of the compiled machine
                                         PHT-style speculative observations. Starting from a selected binary           code, which is what ultimately runs on hardware. Overcoming
                                         region, we lift machine code to an intermediate representation, in-           this gap promises to increase the trustworthiness of analyses, but
arXiv:2511.11385v4 [cs.CR] 30 Jul 2026




                                         strument it with leakage contracts, symbolically execute it to obtain         also seems necessary considering the rising complexity of modern
                                         event/observation traces, and translate these traces into Sapic+ for          protocols, which often involve various sub-protocols like session
                                         analysis with Tamarin, ProVerif, and DeepSec.                                 management and key exchange. It also offers an opportunity to
                                            As case studies, we extract models of WhatsApp Desktop’s                   further investigate and identify attacks resulting from hardware
                                         session-management and double-ratchet components from its bi-                 interaction. In particular, side-channel attacks are known to leak
                                         nary and analyze forward secrecy and post-compromise security                 sensitive information.
                                         under a state-cloning compromise. For side-channel analysis, we                  Recently, CryptoBap [71, 72] sought to bridge this gap by ver-
                                         study the Basic Access Control (BAC) protocol used in e-passports             ifying cryptographic protocols at the machine-code level; while
                                         and WhatsApp’s session establishment. Under our observation mod-              binary-analysis platforms such as BINSEC [44] and BAP [28] offer
                                         els, we identify an instruction-cache side channel in WhatsApp                powerful program-analysis capabilities, they are insufficient for
                                         Desktop enabling social-graph inference, and we reproduce known               such analyses, as they lack any mechanism to semantically recon-
                                         unlinkability issues in BAC under microarchitectural observations.            struct protocol logic from binary. Being in its early development
                                                                                                                       stages, CryptoBap suffers from limited scalability, restricting anal-
                                         CCS Concepts                                                                  ysis to small or medium-sized protocols. Its limitation mostly comes
                                                                                                                       from the computational overhead of techniques like symbolic exe-
                                         • Security and privacy → Formal methods and theory of
                                                                                                                       cution on large code bases and the difficulty of modeling dynamic
                                         security.
                                                                                                                       protocol behaviors (e.g., session resumption, key rotation) in au-
                                                                                                                       tomated verifiers. Moreover, CryptoBap focuses mostly on trace
                                         Keywords
                                                                                                                       properties in the Dolev–Yao model (e.g., secrecy, authentication)
                                         Formal Analysis; Crypto. Protocols; Side Channel; Binary Analysis             and does not account for hardware-induced side-channel vulner-
                                         ACM Reference Format:                                                         abilities. This oversight raises concerns, as side-channel leaks in
                                         Faezeh Nasrabadi, Robert Künnemann, and Hamed Nemati. 2026. Auto-             protocol implementations can inadvertently expose secrets; how-
                                         mated Side-Channel Analysis of Cryptographic Protocol Implementations.        ever, so far side channels were not taken into account when analyz-
                                         In Proceedings of the 2026 ACM SIGSAC Conference on Computer and Commu-       ing protocol implementations. Traditional side-channel detection
                                         nications Security (CCS ’26), November 15–19, 2026, The Hague, Netherlands.
                                                                                                                       tools [33, 41, 51, 74, 87], which target cryptographic primitives or
                                         ACM, New York, NY, USA, 15 pages. https://doi.org/10.1145/3830454.3832676
                                                                                                                       library code, fail to account for protocol-specific interactions that
                                                                                                                       amplify leakage, such as timing variations that can happen dur-
                                         1    Introduction                                                             ing session establishment, error handling, order of operations, or
                                         Cryptographic protocols form the backbone of modern digital secu-             memory-access patterns during key derivation. Concretely, such
                                         rity, protecting sensitive data across online interactions. Yet their         tools can flag a secret-dependent branch, but not whether a protocol
                                         design and implementation remain prone to subtle errors both at               attacker can actually trigger it, nor whether the branched-on value
                                                                                                                       carries a protocol-level secret in the first place, i.e., questions that
                                                                                                                       require reasoning about the protocol, not only the code.
                                         This work is licensed under a Creative Commons Attribution-NonCommercial-        In this paper, we present a methodology for analyzing crypto-
                                         NoDerivatives 4.0 International License.
                                         CCS ’26, The Hague, Netherlands
                                                                                                                       graphic protocol implementations, addressing both classical secu-
                                         © 2026 Copyright held by the owner/author(s).                                 rity properties and side-channel resilience. Our approach extends
                                         ACM ISBN 979-8-4007-2871-6/2026/11
                                         https://doi.org/10.1145/3830454.3832676
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                           Faezeh Nasrabadi, Robert Künnemann, and Hamed Nemati


CryptoBap [71, 72] with observation models [29, 74] (a.k.a., leak-              P ∈ prog := block∗
age contracts [51]) that enable automated analysis of real-world                   block := (v, stmt∗ )
protocols against side-channel attacks. Building on CryptoBap’s                 v ∈ Bval := string | int
core methodology—transpiling assembly code into an intermediate
                                                                                     stmt := halt | jmp(e) | cjmp(e, e, e)
representation for symbolic execution and model extraction—we
                                                                                               | assign(string, e) | assert(e)
extract Sapic+ models directly from protocol binaries that can be an-
alyzed by DeepSec for side channel leak and by Tamarin/ProVerif                e ∈ Bexp := v | ^u e | e ^b e | var string | load(e, e,int)
for reachability properties.                                                                   | store(e,e, e,int); | ifthenelse(e, e, e)
   Threat model and scope. We consider an active network at-
tacker in the Dolev–Yao model and a co-resident attacker (process)                                 Figure 1: BIR’s syntax
that can observe microarchitectural effects captured by our leak-
age contracts (e.g., instruction- or data-cache Prime+Probe mea-
surements). For speculative leakage, we adopt a Spectre-PHT-style
                                                                                 about protocol security in the presence of microarchitectural
model in which conditional branches may be transiently mispre-
                                                                                 side channels.
dicted and wrong-path memory accesses may become observable
                                                                             (2) We provide the first formal model of WhatsApp’s implemen-
through side channels. Our goal is not to model all microarchi-
                                                                                 tation of session management and double ratchet component
tectural channels, but to lift well-scoped observation models to
                                                                                 extracted from its binary, and use Tamarin/ProVerif to
protocol verification and to expose security violations that arise
                                                                                 prove forward secrecy and to confirm a post-compromise
from control flow divergence and memory-access behavior.
                                                                                 security break against a clone attacker.
   Our observation models can, in principle, capture “classical”
                                                                             (3) Applying our side-channel-aware analysis to WhatsApp ses-
constant-time violations such as secret-dependent table lookups
                                                                                 sion establishment, we find a privacy leak: a side-channel
(e.g., in an AES implementation) because secret-dependent load
                                                                                 attacker can distinguish first-time from existing contacts,
addresses become observable. However, we abstract crypto library
                                                                                 enabling them to infer the victim’s social graph. We also
calls to focus on protocol logic and on protocol-level leakages.
                                                                                 confirm the known unlinkability break in BAC.
   As a case study, we conduct the first formal verification of the
WhatsApp Desktop binary by extracting a model of its session             Responsible disclosure: The vulnerabilities found in WhatsApp
management protocol (Sesame) and double ratchet mechanism.               Desktop were responsibly disclosed to Meta in March 2025. Meta
WhatsApp is the most widely used messaging platform, with over 3         confirmed that the application is vulnerable to identified attacks.
billion users across the globe [3]. While Sesame has been formally
analyzed at the specification level [39], no prior work extracted        2     Background
and verified the Sesame logic as implemented by WhatsApp’s client.       We build on CryptoBap [71, 72], a binary analysis framework that
Given that WhatsApp is closed-source and similar systems have his-       extends security protocol verification to machine code to elimi-
torically shown vulnerabilities (e.g., EternalBlue, CVE-2017-0144),      nate the need to trust compilers. CryptoBap extends the HolBA
this lack of implementation-level analysis is concerning.                framework [59] to verify ARMv8 and RISC-V machine code crypto
   For large applications like WhatsApp, considering all memory          protocols. It achieves this by extracting a formal model of the pro-
operations and function calls yields a large extracted model. Even       tocol under analysis, which can then be translated into models
with simplification, state-of-the-art protocol verifiers still fail to   suitable for automated verification using ProVerif, CryptoVerif,
terminate when analyzing models of this scale. For reachability-         Tamarin, and DeepSec. In this section, we provide an overview of
style properties on WhatsApp (e.g., forward secrecy and post-            the CryptoBap structure and introduce the necessary preliminaries
compromise security), we therefore rely on CryptoBap’s original          to understand the contributions of this paper.
extraction pipeline, which abstracts memory effects and crypto-
graphic primitives in a way that is sound for finding trace-property
                                                                         2.1     HolBA Framework
violations under its assumptions. For side-channel and privacy
analyses, we apply our observation-aware extraction to smaller,          HolBA [59] is a library for binary analysis based on the HOL4 the-
protocol-relevant components where memory- and control-flow              orem prover [43] and the L3 specification language [47]. HolBA
observations are essential and still scalable.                           achieves this by transpiling binary code into the Binary Intermedi-
   Using our models, we (i) prove forward secrecy of WhatsApp’s          ate Representation (BIR 1 ), a simple, architecture-agnostic language
session establishment and message exchange, (ii) confirm that a          designed to facilitate binary analysis and tool development. To en-
clone attacker can break post-compromise security—as previously          sure soundness, the transpilation process is verified to preserve the
identified for Signal application [39]—and (iii) identify a novel pri-   semantics of the input machine code.
vacy attack that leverages instruction-cache leakage during session         Figure 1 depicts BIR’s syntax. A BIR program P consists of
establishment to infer whether two users have been in contact. To        uniquely labeled blocks, with each block containing a sequence of
summarize, our contributions are as follows:                             statements. Labels correspond to specific locations in the program
                                                                         and are commonly used as the target for jump instructions. BIR

   (1) We extend CryptoBap with leakage contracts and a model            1We use colors for different languages: RoyalBlue, math bold for BIR and SBIR, and
       extraction path to DeepSec to enable automated reasoning          RedOrange, sans serif for Sapic+ . Common elements use black italics.
Automated Side-Channel Analysis of Cryptographic Protocol Implementations                         CCS ’26, November 15–19, 2026, The Hague, Netherlands


                  ⟨P, Q⟩ ::=                                                through a channel visible to the attacker. The event construct is
                                                                            used to raise events that pertain to the reachability properties of
                   0                             | !P
                   | in(𝑥); P                    |P|Q
                                                                            the model. Furthermore, the new construct enables the generation
                   | out(𝑥); P                   | new 𝑛; P                 of new values. Conditionals are described by first-order formulae 𝜙
                   | if 𝜙 then P else Q          | event 𝑒; P               over equalities on terms, possibly containing variable quantifiers, as
                   | let 𝑡 1 = 𝑡 2 in P else Q                              in [57]. The Sapic+ syntax features stateful processes that modify
                                                                            globally shared states, which are excluded in Figure 2 for simplicity.
Figure 2: A fragment of the syntax of Sapic+ process calculus.                  Sapic+ facilitates the analysis of equivalence properties through
In this figure, 𝑒, 𝑡 1, 𝑡 2 ∈ T , 𝑛 ∈ Npriv , 𝑥 ∈ V.                        its backends, specifically DeepSec, a specialized tool designed for
                                                                            this purpose. DeepSec focuses on indistinguishability properties,
                                                                            particularly trace equivalence. It employs a language similar to
statements include (a) assign, to assign a BIR expression to a vari-        ProVerif but without the “!” operator for unbounded replication,
able, (b) jumps (i.e., jmp or cjmp), (c) halt, which serves as the ter-     as it supports only bounded verification. Unlike ProVerif, DeepSec
mination instruction, and (d) assert, which evaluates a boolean ex-         provides a decision procedure that guarantees termination, given
pression and terminates execution if the assertion fails. Expressions       sufficient resources. As a result, DeepSec can effectively check trace
in BIR include constants, variables, conditionals (i.e. ifthenelse),        equivalence in cases where ProVerif fails to terminate, though it
arithmetic operations, denoted by ^b for binary and ^u for unary,           requires bounding the number of replications.
as well as memory operations such as load and store.
   HolBA provides a proof-producing symbolic execution for BIR                 Backend protocol verifiers. In our pipeline, Sapic+ serves as
[60] which CryptoBap [71, 72] uses in its pipeline. This symbolic ex-       a front-end that can be discharged to different backends depending
ecution formalizes the symbolic generalization of BIR (called SBIR)         on the property of interest and the required level of automation.
to explore all execution paths of the program. The symbolic seman-          ProVerif is typically effective for reachability properties (e.g., se-
tics align with concrete semantics, enabling guided execution that          crecy and authentication) and supports unbounded replication,
maintains a set of reachable states arising from an initial symbolic        but it may not terminate on complex models. Tamarin supports
state. HolBA’s symbolic execution allows for verifying functional           richer equational theories and an interactive proof mode to guide
correctness, but not (directly) protocol security, as it lacks a suitable   proof search with lemmas and proof hints. DeepSec provides a
attacker model and concurrent behavior. CryptoBap bridges this              terminating decision procedure for bounded verification of process
gap by extracting formal models of the protocols from their imple-          equivalences such as trace equivalence, which we use to encode
mentations. This model is then used to analyze security properties          privacy properties (e.g., unlinkability [11]) and conditional non-
using external protocol verifiers. CryptoBap extracts formal mod-           interference [50] in the presence of side-channel observations.
els of protocols into two distinct modified versions of the applied
𝜋-calculus: one suitable for automated verification using ProVerif
and CryptoVerif, proposed in [71], and another for automated                2.3    Side Channels & Observational Models
verification with ProVerif, Tamarin, and DeepSec, utilizing the             Resource sharing is inevitable in computing due to limitations in
Sapic+ toolchain introduced in [72]. Since our goal is to check             available resources. However, if not done carefully, it can introduce
trace equivalence [65], we have chosen to extract Sapic+ models, as         unintended information flow channels, also known as side channels.
Sapic+ backends support equivalence properties.                             These channels can potentially be exploited by a malicious process
                                                                            to exfiltrate secret information from trusted ones.
2.2     Sapic+ & DeepSec                                                       Attacks that exploit the data and instruction caches are among
The Dolev–Yao model includes an attacker that exploits logical              the most commonly used side-channel attacks [7, 75, 85, 86]. One
flaws in a protocol, but cannot compromise cryptographic primi-             widely used technique for extracting information via caches is
tives [45]. In this model, the cryptographic primitives are considered      known as Prime+Probe [80]. In an instruction-cache attack using
perfect—for instance, guessing a key is impossible. A specific set of       this technique, first, the attacker primes the cache by filling it with
rules defines the abstract manipulation of messages, while other            their own instructions. Then, while the victim executes, some of the
alterations are not permitted.                                              attacker’s cached instructions may be evicted. Finally, the attacker
   In a protocol execution, messages are represented as terms. High-        probes the cache by measuring access times to their instructions to
entropy values are modeled by constants derived from an infinite set        detect evictions that reveal the victim’s execution behavior.
of names N classified into public names Npub (available to attackers)          The number of attack techniques exploiting microarchitectural
and secret names Npriv . Terms denoted as T are constructed using           features, like caches, to leak secret data continues unabated. Conse-
names derived from N , variables sourced from a variable set V,             quently, the study of information flow analysis techniques to ensure
and by applying function symbols from F on terms.                           the absence of information leakages due to side channels is a topic
   Sapic+ [34] is a dialect of applied 𝜋-calculus that provides a lan-      of increasing relevance. A formal model of side channels is essential
guage that soundly translates to Tamarin [66], ProVerif [25] and            for such an analysis. However, explicitly modeling all the intricate
DeepSec [35]. Sapic+ enhances Sapic [57] by introducing destruc-            features of modern processors—like cache hierarchies, replacement
tors and let bindings with pattern matching and else branches. A            policies, and memory interactions—is almost infeasible due to their
fragment of Sapic+ ’s syntax is shown in Figure 2. The in and out           complexity and because many microarchitectural details are not
constructs are responsible for receiving and outputting messages            publicly available. To address this challenge, abstract observational
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                           Faezeh Nasrabadi, Robert Künnemann, and Hamed Nemati


models [29, 74] (a.k.a., leakage contracts [51]) provide an alternative
by overapproximating an attacker’s capabilities.
   An observation model M extends the abstract representations of
a processor’s operational semantics by a set of system states 𝑆, a set
of possible attacker observations O and a labeled transition relation
→𝑚 ⊆ 𝑆 × O × 𝑆 indexed with the execution mode 𝑚 ∈ {𝑟, 𝑡 }. When
𝑚 = 𝑟 , we mean that the processor executes at the software-visible
ISA level using a sequential transition system, while with 𝑚 = 𝑡,           Figure 3: The Spectre V1 example instrumented via Mct and
we denote the transition relation of some target microarchitecture          Mspec . We marked shadow observations with ★.
where the information flow may be affected by optimizations such
as out-of-order or speculative execution. Essentially, observations
define which parts of the processor state influence the side channel
at each transition. This enables information flow analysis without          operation that may execute during the speculation. The current
requiring us to know the exact microarchitectural behavior.                 implementation of our toolchain focuses on branch misprediction;
   The primary property to formalize the absence of microarchitec-          modeling other Spectre variants (e.g., store-to-load forwarding in
tural leakages due to side channels is conditional non-interference [50].   Spectre-v4, or return-stack-buffer effects) would require develop-
Let 𝑠 ∈ 𝑆 be a system state, including microarchitectural compo-            ing suitable observation models. More generally, our framework is
nents like caches, traces : 𝑇 ↦→ 2 O be a function to extract the           parametric in the observation model: a new model requires only
sequence of observations from a given execution trace 𝜏 ∈ 𝑇 , and           formalizing which processor-state components are observable for
𝑠 ∼ M 𝑠 ′ is the state’s indistinguishability relation w.r.t. the model     each instruction type and implementing the corresponding instru-
M. Then we say:                                                             mentation, while the rest of the pipeline is unchanged.

    Definition 2.1 (Conditional non-interference (CNI)). A system
is conditionally non-interferent if for all indistinguishable initial
                                                                            3   Methodology
states 𝑠 and 𝑠 ′ (i.e., 𝑠 ∼ M 𝑠 ′ ), if for every execution sequence        To reason about crypto protocols’ resilience to hardware side-
         𝑜1            𝑜𝑛                                                   channels, we combine symbolic execution, observational models,
𝜏1𝑟 = 𝑠 −→𝑟 𝑠 1 . . . −−→𝑟 𝑠𝑛 there exists a corresponding sequence
            𝑜 1′          𝑜𝑛′
                                                                            and protocol verification techniques—the source code of our frame-
𝜏2𝑟 = 𝑠 ′ −→𝑟 𝑠 1′ . . . −−→𝑟 𝑠𝑛′ such that traces(𝜏1𝑟 ) = traces(𝜏2𝑟 ),    work is available at [73]. As Figure 4 illustrates, our approach begins
                                         𝑜1             𝑜𝑛
then for every execution 𝜏1𝑡 = 𝑠 −→𝑡 𝑠 1 . . . −−→𝑡 𝑠𝑛 , there must         with reverse-engineering the executable binaries using Ghidra [42],
                                              𝑜 1′           𝑜𝑛′            after which we transpile the resulting assembly code into BIR using
also exist a corresponding 𝜏2𝑡 = 𝑠 ′ −→𝑡 𝑠 1′ . . . −−→𝑡 𝑠𝑛′ such that      the HolBA framework [59]. We then annotate the BIR program
traces(𝜏1𝑡 ) = traces(𝜏2𝑡 ).                                                with attacker observations and symbolically execute it to explore
    A common strategy to prevent cache timing side channels in the          all execution paths. We simplify and translate the resulting sym-
literature is the constant time (CT) policy [15], which requires that       bolic execution tree into a formal model in Sapic+ calculus, which
memory accesses and control flow decisions should depend only               we then further simplify to improve reasoning scalability. Finally,
on public (non-secret) information. In this paper, the observational        we translate this model into formats compatible with automatic
model Mct formalizes this policy and it makes the program counter           analysis of side-channel resilience using DeepSec.
of each instruction and the accessed memory addresses observable.              In the following, we first describe how we annotate BIR with
    Alas, speculative execution introduces new attack vectors that          observational models to capture side-channel leaks. Next, we detail
break the assumptions of CT execution. Spectre attacks [55] ex-             our symbolic execution engine, tailored for dealing with crypto
ploit speculation to leak data through side channels like caches.           primitives and hardware interactions. We then explain the extrac-
These attacks are characterized by a speculative primitive that             tion and simplification of the protocol model. We conclude by dis-
allows leaking secrets during speculative execution. We use the             cussing how we leverage DeepSec to analyze the simplified Sapic+
observational model Mspec proposed by Buiras et al. [29] to cap-            models for side-channel resilience.
ture Spectre-PHT/Spectre-V1-style leakage, i.e., leakage caused by
                                                                               Running example. We use the Basic Access Control (BAC)
transient execution along a mispredicted conditional branch. The
                                                                            protocol as a running example. Figure 5 shows a C implementa-
model introduces refined (a.k.a., shadow) observations that repre-
                                                                            tion of the BAC’s session-establishment logic—developed in-house
sent operations executed transiently on the misspeculated path.
                                                                            since production e-passport code is not publicly available—along
Observation refinement. Technically, an observation model M groups          with the simplified assembly fragment used throughout this sec-
states into equivalence classes where states appear indistinguish-          tion. Our implementation follows the BAC protocol and complies
able. Observation refinement improves this partitioning by intro-           with the relevant International Civil Aviation Organization stan-
ducing a refined model M ′ that further partitions these classes.           dards specifications [46]. BAC is a three-pass challenge-response
Essentially, M ′ captures additional behavioral variations, partic-         protocol for mutual authentication between an e-passport and a
ularly those linked to side-channel effects, that M may overlook.           reader. The reader first sends a challenge; the e-passport responds
For instance, Figure 3 depicts the Spectre V1 primitive annotated           with a fresh nonce. The reader then samples its own nonce, en-
with the attacker’s observation from the Mct model and shadow               crypts both nonces under the pre-shared encryption key 𝑘𝑒 , and
observation from the Mspec that enable the attacker to observe an           transmits the ciphertext together with a MAC computed under 𝑘𝑚 .
Automated Side-Channel Analysis of Cryptographic Protocol Implementations                        CCS ’26, November 15–19, 2026, The Hague, Netherlands




Figure 4: Organization of our approach; new features are in green. We reuse CryptoBap’s model-extraction core, but add
observation instrumentation, simplification rules, and a DeepSec backend for leakage detection.


                                                                                Correctness considerations. We treat the reverse-engineering
                                                                            step as part of the trusted computing base: if the selected region
                                                                            omits relevant dependencies, the extracted model may be incom-
                                                                            plete. To mitigate this, whenever we cannot resolve a dependency
                                                                            (e.g., an external library call), we conservatively overapproximate
                                                                            it by modeling its outputs as fresh symbolic inputs from the envi-
                                                                            ronment. Importantly, we do not rely on Ghidra’s decompiler for
                                                                            semantic reasoning, i.e., after exporting instructions, all semantic
                                                                            lifting and symbolic reasoning are performed on HolBA’s verified
                                                                            BIR semantics. Finally, speculation is accounted for after lifting
                                                                            by instrumenting BIR with shadow observations. Thus, we do not
                                                                            require the decompiler to predict speculative paths.


                                                                            3.2    BIR with Observation Models
Figure 5: Running example. The assembly snippet corre-                      To integrate side-channel leakage into our analysis, we instrument
sponds to the highlighted C code.                                           BIR programs by annotating each BIR block with attacker obser-
                                                                            vations, which are expressions that describe information that may
                                                                            leak through side channels. These observations can be conditional,
Upon receipt, the e-passport verifies the MAC, decrypts the cipher-         meaning they only occur if specific conditions hold in the current
text, and checks that its nonce is present. If all checks succeed, the      state. We adopt established observational models from the Scam-V
reader is authenticated (and the e-passport is authenticated to the         platform [74]. Our BIR observations o𝑏 ∈ O𝑏 include:
reader analogously). In Figure 6, we highlight the corresponding
BIR blocks to illustrate the steps of our methodology.                             o𝑏 ::= 𝜀 | Ld(a) | St(a) | Cnd(𝜙, a1, a2 ) | Pc(a)

3.1     Reverse Engineering                                                    Observation Pc(a) exposes the label of the BIR block, which
                                                                            corresponds to the program counter, Cnd(𝜙, a1, a2 ) reveals the
Analyzing real-world, closed-source binaries requires first isolating
                                                                            outcome of the conditional branch’s condition and exposes the
the protocol logic inside a larger code base. In WhatsApp Desk-
                                                                            addresses of each branch, and Ld(a)/St(a) exposes the address
top, the code that implements the Signal/Sesame protocol stack
                                                                            operand of load/store instructions. All other instructions are con-
constitutes only a small fraction of the overall executable, yet it is
                                                                            sidered non-leaking and emit the empty observation 𝜀.
intertwined with application logic, storage, and networking.
                                                                               Depending on the observation models (Mct , Mspec , or any other),
   Binary extraction. We use Ghidra [42] to (i) locate protocol-            the observations assigned to each BIR block can be either normal
relevant entry points, (ii) follow cross-references and call graphs to      or shadow observations (see Section 2.3). E.g., take the last line
collect dependent functions, and (iii) export the exact instructions of     in Figure 3, the Mspec observation annotated to the BIR block of
the selected region. We start from functions that (a) retain symbols        the corresponding assembly code is Ld(x2★). Our observation in-
or strings associated with the Signal protocol stack and (b) interact       strumentation is not formally proved sound against a given observa-
with crypto-library entry points and network I/O, which can be              tional model, but it closely follows (we reused partially) the Scam-V
recognized using approaches in the spirit of [68]. We then expand           framework, whose validation against real hardware is established.
this set by following data and control dependencies (slicing) to               Compared to other platforms, Scam-V implements a more de-
obtain a region that covers message parsing/serialization, state            tailed observation of load and store statements. While we simplify
updates, and calls to cryptographic primitives.                             the presentation, we preserve the same level of granularity.
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                                Faezeh Nasrabadi, Robert Künnemann, and Hamed Nemati




Figure 6: Excerpt of the BIR blocks of the BAC protocol in Figure 5, together with the corresponding BIR observations, symbolic
execution events and extracted Sapic+ model. 0𝑥200 is the address of the BIR halt statement, which translates to 0. The Sapic+
process then translates to the DeepSec process, which closely mirrors what is illustrated here. Jumps (at lines 0, 2, 3, and 4) are
the translation of branch and link instruction used for function calls in ARM, which requires updating the link register 𝑅30.
We present this register update in [..] to mean that it is not relevant to what we intend to present in this example.

                                   o𝑏                                              The execution tree T consists of (a) leaves (Leaf), indicating the
    The BIR transition relation −−→ ⊆ S𝑏 × O𝑏 × S𝑏 defines how states
evolve while releasing observations. Here, S𝑏 is a set of BIR states,           end of a complete execution path in the tree, i.e., where the halt
and O𝑏 denotes the set of observations. Starting from an initial state          statement is encountered, (b) event nodes (node(ev) :: T′ ) each
s𝑏0 ∈ S𝑏 , a sequence of transitions produces a BIR observation trace           containing a sub-tree T′ and an event ev, and (c) branch nodes
𝔱𝑏 = o𝑏1 , . . . , o𝑏m . Figure 6 illustrates a BIR program snippet (first      (Branch(Cnd(𝜙, a1, a2 ), T1, T2 )) each with the condition 𝜙 and sub-
column) and its annotated observations (second column).                         trees Ti with their respective addresses ai .
                                                                                   Our symbolic execution generates two successor states for the
                                                                                nodes representing a branching statement (i.e., cjmp), and we con-
3.3     Symbolic Execution                                                      tinue constructing subtrees from these states. For other statements’
To analyze side-channel leakages across all feasible paths, we extend           nodes, we get an event node with either one or no successor in the
CryptoBap’s symbolic execution to track attacker observations                   tree. The exceptions are the nodes containing indirect jumps which
alongside path constraints. Each symbolic state ss ∈ Ss now encap-              may have multiple successors that are discovered iteratively using
sulates a path condition—a logical constraint indicating a condition            an SMT solver following the approach outlined in [71].
under which a path is taken—and a list of symbolic observations                    Having constructed T, we extract the protocol model by translat-
which represent leaked information (e.g., memory addresses and                  ing T into its Sapic+ model using the rules in Figure 7. The leaves
branch targets) that an attacker could infer.                                   in the tree are translated into a null process 0, and events ev in the
        os                                                                      event nodes are translated into their corresponding Sapic+ con-
     Let −→    → ⊆ Ss × O s × Ss denote the transition relation of SBIR
                                                                                structs. For example, we translate the attacker observations Ld(a),
and let an SBIR trace be a sequence of observations such that 𝔱 s =
                                                                                St(a), and Pc(a) within event nodes to the out(LaM) constructs. The
os1 , . . . , osm . SBIR observations os ∈ O s include BIR observations
                                                                                observations Cnd(𝜙, a1, a2 ) are preserved in the branching nodes
on symbolic values or expressions, as well as observations related
                                                                                of T, where each condition 𝜙 is a symbolic BIR expression trans-
to network communication and calls to crypto primitives, event
                                                                                lated into an equivalent Sapic+ term. To maintain the attacker’s
functions and random number generation. In(𝑥) represents the in-
                                                                                observations during simplification (cf. Section 3.5), we first disclose
coming message 𝑥 from the environment, whereas Out(𝑥) denotes a
                                                                                the translation of 𝜙 to the attacker before translating the branching
message 𝑥 dispatched to the environment. Fr(𝑛) indicates when the
                                                                                node into the Sapic+ conditional construct, where L𝜙M serves as its
program generates a random number 𝑛, and FCall(f, 𝑥 1, . . . , 𝑥𝑚 , 𝑦)
                                                                                condition. Each branch of this construct includes the translation of
refers to a function call f with inputs 𝑥 1, . . . , 𝑥𝑚 , and an output 𝑦. In
                                                                                the corresponding addresses ai —also revealed to the attacker—and
addition, Ev(𝑒) signifies the occurrence of a visible event 𝑒, Loop
                                                                                the translation of respective subtrees Ti . Figure 7 presents the
denotes the start of a loop, and Asn(𝑥, e) represents the assignment
                                                                                standard rules for translating expressions.
of the BIR expression e to the variable 𝑥. The SBIR observations of
                                                                                   The more interesting case is the translation of function applica-
our example are depicted in Figure 6 (third column).
                                                                                tions used, e.g., to translate memory load/store and bitwise opera-
                                                                                tions. For instance, a load(𝑚𝑒𝑚, 𝑎, 𝑙), where 𝑙 ∈ {1, 8, 16, 32, 64, 128},
3.4     Model Extraction                                                        translates to load(𝑚𝑒𝑚, 𝑎), with 𝑚𝑒𝑚 and 𝑎 representing symbolic
To analyze protocol implementations for side-channel leakages, we               values for the memory and the address respectively.
symbolically execute the instrumented program and derive a sym-                    The fourth column in Figure 6 shows the extracted Sapic+ pro-
bolic execution tree T from the SBIR execution, with root denoting              cess of our example. An attacker capable of measuring microarchi-
the initial symbolic state. We use T to extract the protocol’s Sapic+           tectural states can detect if the MAC check fails (by observing pc
model. The tree captures all feasible execution paths explored dur-             0𝑥200) or succeeds (by observing program counter 0𝑥𝑎𝑐). However,
ing symbolic analysis, annotated with attacker observations and                 this is not visible without accounting for side-channel observations,
protocol-specific events.                                                       as the program halts when the MAC check fails.
Automated Side-Channel Analysis of Cryptographic Protocol Implementations                                              CCS ’26, November 15–19, 2026, The Hague, Netherlands


   T =Leaf | node(ev) :: T′ | Branch(Cnd(𝜙, a1, a2 ), T1, T2 ) event tree                            Sapic+       if 𝜙 then P let 𝜙 in 0    let 𝑥 = 𝑒 in P s.t.
                                                                                                     Process            else P      else 0 𝑥 ∉ vars(P)
      LLeafM                   ↦→ 0
                                                                                                     Simplified P              0            P
      Lnode(ev) :: T′ M :=                                events nodes
                                                                                                 Table 1: Simplification rules: vars are a set of variables for a
                        ′
       Lnode(𝜀) :: T M                                     ↦→      LT′ M                         given process.
       Lnode(os ) :: T′ M, os ∈ {Ld(a), St(a), Pc(a)} ↦→           out(LaM); LT′ M
       Lnode(Ev(𝑒)) :: T′ M                                   ↦→   event 𝑒; LT′ M
       Lnode(In(𝑥)) :: T′ M                                 ↦→     in(𝑥); LT′ M
       Lnode(Out(𝑥))::T′ M                                ↦→       out(𝑥); LT′ M
       Lnode(Asn(𝑥, e)) :: T′ M                          ↦→        let 𝑥 = LeM in LT′ M
                                                                                                     At the SBIR level, further simplifications are possible. An exam-
       Lnode(Fr(𝑛)) :: T′ M                            ↦→          new 𝑛; LT′ M
       Lnode(Loop) :: T′ M                              ↦→         ! LT′ M                       ple is pruning paths that the SMT solver marks as unreachable, like
       Lnode(FCall(f, 𝑥 1, . . . , 𝑥𝑛 , 𝑦)) :: T′ M          ↦→    let 𝑦 = f(𝑥 1, . . . , 𝑥𝑛 )   branches of conditionals that are always false. While for functional
                                                                   in LT′ M else 0               correctness analysis, eliminating such paths is possible, we cannot
      LBranch(Cnd(𝜙, a1, a2 ), T1, T2 )M ↦→                                                      apply this simplification when we look for side-channel leaks, as
                                                                                                 unreachable branches can leak during speculative execution.
                            out(L𝜙M); if L𝜙M then out(La1 M); LT1 M else out(La2 M); LT2 M
                                                                                                     At the Sapic+ level, nil processes indicate the end of a complete
      L𝜙 ∈ BexpM :=                                        Expressions
                                                                                                 path. When a let-binding ‘let 𝑥 = 𝑒 in P else Q’ results in nil
       Lb ∈ BvalM              ↦→      '𝑏' ∈ Npub                                                processes in both its success and failure branch (i.e., P = 0 and
       Lvar 𝑥M                  ↦ →    𝑥 ∈V                                                      Q = 0), it can be removed and substituted with 0. Moreover, for
       L𝜙 1 ^b𝜙 2 M               ↦→    b M(L𝜙 1 M, L𝜙 2 M)
                                       L^                         Binary operations              a conditional that involves paths following the same sequence of
                                           equal                 Equal
       L^b M                   ↦→                                                                constructs, like if 𝜙 then P else P, the conditional can be replaced
                                           plus, mult, . . . Plus, Mult, . . .
       L^u𝜙 ′ M                ↦→                ′                 Unary operations
                                                                                                 with the corresponding constructs in those paths, P. In order to
                                        u M(L𝜙 M)
                                       L^
                                                                                                 ensure that this simplification would not affect our side channel
                                           not Not
       L^u M                   ↦→                                                                analysis, we preserve the observations related to the conditional (if
                                           ⊥      otherwise
       Lf (e1, . . . , em )M   ↦→      LfM(Le1 M, . . . , Lem M)                                 any) and add them to the simplification result.
                                                                                                     Live variable analysis is a data-flow analysis used in compiler op-
Figure 7: Translating T into a Sapic+ model: 𝑒, 𝑥, 𝑥 1, . . . , 𝑥𝑛 , 𝑦 ∈                         timization to identify live variables at every point in a program [8].
V are variables, 𝑛 ∈ Npriv is a secret name, and not, equal,                                     A variable 𝑥 is live at a given point 𝑝 in the program if 𝑥 will be
plus, mult, f ∈ F are function symbols. os and conditional                                       used along some path starting from 𝑝. This analysis becomes es-
observations are either normal or shadow observations.                                           pecially important when we want to eliminate a let construct. We
                                                                                                 use this technique to determine whether the variable 𝑥 used in the
                                                                                                 let 𝑥 = 𝑒 in P construct remains alive within the sub-process P. If
3.5     Simplification                                                                           so, we retain the let construct, otherwise, we substitute it to P.
                                                                                                     Finally, observational models like Mct require making the pro-
The extracted models include memory operations and attacker-
                                                                                                 gram counter of instructions (i.e., Pc(a)) visible to the attacker.
observable events, and are therefore too large for current protocol
                                                                                                 When extracting a formal model of a program annotated with such
provers. To reduce model complexity, we used abstractions in BIR,
                                                                                                 observational models, we generate an out(LaM) for each instruction
pruned paths at SBIR, and applied several simplification rules at
                                                                                                 (see Figure 7). However, the large number of output constructs
the Sapic+ level, which are shown in Table 1.
                                                                                                 makes DeepSec computation expensive without a significant bene-
   At the BIR level, we introduce a storage abstraction akin to
                                                                                                 fit, mainly when they originate from the same branch. Therefore,
KLEE’s treatment of files, pipes, and terminals [30]. We abstract
                                                                                                 leaking the program counters of conditional branches is sufficient
the SQLite engine by modeling the effects of database creation, the
                                                                                                 and other program counter leakages can be eliminated. This greatly
table schema, and the read and write operations on the database file.
                                                                                                 simplifies the extracted Sapic+ process (e.g., see Table 3).
In particular, WhatsApp stores session keys in the SQLite database.
   HolBA’s semantic-preserving transpiler inserts assertions into
BIR programs that encode well-formedness invariants of executions,                               3.6    Detecting Leakages with DeepSec
e.g., after each stack operation it adds assert(𝑠𝑝 low ≤ 𝑠𝑝 ≤ 𝑠𝑝 high )                          We use the protocol verifier DeepSec [35] to detect side-channel
to confine the stack pointer to the current frame. By construction,                              leakage exploitable by a Dolev–Yao network attacker who can ad-
each inserted assert(𝜒) is an invariant for executions of the original                           ditionally observe the leakage events produced by our contracts.
binary that start from well-formed initial states. Consequently,                                 DeepSec specializes in privacy properties expressed as trace equiva-
any SBIR path that violates such an assertion is infeasible. We                                  lence: given two processes 𝑃1 and 𝑃2 , it checks whether an attacker
therefore cause the path to fail at that point and prune its suffix.                             can distinguish their observable execution traces.
This does not affect our side-channel analysis because the inserted                                 For instance, in BAC, an attacker can exploit observable control-
assertions hold for all executions from well-formed states, and                                  flow differences (e.g., out(0𝑥𝑎𝑐) versus out(0𝑥200) in Figure 6) to
our observation semantics are guarded. Hence, assertion-violating                                infer information about message structure. By replaying previously
paths cannot produce observations. We call such assertion-violating                              observed messages, the attacker can distinguish successful from
paths infeasible, and the “infeasible” column of tables 3 and 2 counts                           unsuccessful MAC verification and thereby violate BAC’s intended
them. These differ from the unreachable branches handled next.                                   privacy guarantees.
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                         Faezeh Nasrabadi, Robert Künnemann, and Hamed Nemati


   DeepSec is well-suited for such analyses because it supports           as the basis for end-to-end encryption. This encryption protocol
equivalence checking. Formally, it decides whether 𝑃1 ≈ 𝑃 2 holds         prevents WhatsApp’s servers and other third parties from accessing
for the class of processes it supports; when it terminates, it either     the plaintext of user messages or calls. Messages are encrypted with
proves equivalence or returns a counterexample in the form of             ephemeral cryptographic keys that are regularly updated (using
distinguishing traces.                                                    ratcheting or a new handshake), preventing attackers from decrypt-
   To isolate leakage introduced by speculative execution, we eval-       ing previously transmitted messages, even if the current encryption
uate conditional non-interference (Definition 2.1) by running the         keys are compromised.
same equivalence check under two observation models. Concretely,             We extract a formal model of WhatsApp’s binary to verify for-
we check equivalence once under the constant-time observations            ward secrecy and post-compromise security. For this part, we use
Mct and once under the refined speculative observations Mspec . If        CryptoBap’s original extraction pipeline to obtain a Sapic+ model
𝑃1 ∼ Mct 𝑃2 but 𝑃1 ≁ Mspec 𝑃2 , the additional distinguishing power       that can be discharged to ProVerif and Tamarin for reachability-
comes from speculation, witnessing a speculative-only leak.               style analysis; this analysis is orthogonal to the side-channel ob-
   A counterexample under Mct (resp. Mspec ) yields two symbolic          servations studied later in this section. We reverse-engineered the
traces distinguishable by the chosen observation model; under             WhatsApp Desktop’s binary using Ghidra. Unlike the iOS or An-
the assumptions of our lifting and abstractions, this corresponds         droid versions, function symbols were not stripped from the desktop
to a concrete binary-level side-channel distinguisher within our          application, allowing us to match the function names with the latest
leakage contract. Conversely, when DeepSec reports equivalence,           version of the libsignal, Signal’s protocol implementation.
the result is bounded (due to bounded replication) and depends
                                                                          4.1.1 Components. The double ratchet protocol enables secure
on the soundness of our abstractions for cryptographic primitives,
                                                                          (confidential and authentic) message exchange between the two
external I/O, and the selected observations.
                                                                          parties. It builds on the Extended Triple Diffie-Hellman (X3DH) key
                                                                          agreement protocol [53], which allows parties to establish a shared
4     Evaluation
                                                                          secret key using mutual authentication based on their public keys.
In our evaluation, we separate two goals that require different               Initially, the key is obtained via X3DH, and called the root key.
backends and abstractions: (i) reachability-style security analysis of    Subsequent ephemeral keys are generated using ratcheting, so
WhatsApp Desktop (e.g., forward secrecy under a Dolev–Yao net-            called because earlier ephemerals cannot be derived from later
work attacker), and (ii) equivalence-style privacy and side-channel       ones. Ratcheting is asymmetric if the parties switch roles (i.e., from
analysis (unlinkability and conditional non-interference) under the       sender to receiver or vice versa) and symmetric if they maintain
observation models Mct and Mspec . For (i), we reuse CryptoBap’s          the same role. Symmetric ratcheting provides forward secrecy: even
established extraction pipeline and discharge the resulting models        if long-term secrets (the secret keys to the public keys used in the
to ProVerif and Tamarin. For (ii), we apply our observation-aware         handshake) or future ephemerals are revealed, past ephemerals
extraction (Section 3) and analyze the resulting Sapic+ processes         and thus the messages sent with them remain secret. Asymmetric
with DeepSec.                                                             ratcheting establishes fresh ephemerals that are unknown to the
   Table 2 summarizes the sizes and extraction/verification costs for     attacker even if past ephemerals are known, unless the attacker
the WhatsApp components (Sesame session handling and double               actively attacks the handshake. This provides post-compromise se-
ratchet). Table 3 summarizes the corresponding statistics for the         curity: even after ephemeral keys are revealed, the authenticity and
side-channel case studies (BAC and WhatsApp session establish-            confidentiality of future ephemerals (and the messages encrypted
ment) under Mct and Mspec . The reduction percentages report the          with them) can be recovered.
relative decrease from the raw extracted model (all) to the simpli-           Sesame defines the session management and operates on the
fied model (simp). Note that verification time may increase because       layer above the double ratchet protocol. It manages multiple dou-
simplification and backend translation add overhead.                      ble ratchet sessions between the different devices associated with
    Manual vs. automatic effort. Once a protocol-relevant region          each user account. E.g., if Alex has 𝑛𝐴 devices and Blake has 𝑛𝐵
is selected, the pipeline (lifting, observation instrumentation, sym-     devices, on each of Alex’s devices, Sesame manages 𝑛𝐵 connections
bolic execution, extraction, simplification, translation, and verifica-   to Blake and 𝑛𝐴 -1 connections to Alex’s other devices. Sesame man-
tion) runs automatically. The manual inputs are: (a) selecting entry      ages the creation, deletion, and use of sessions, maintaining a local
points and defining the analysis boundary in Ghidra, (b) deciding         database that records each party’s devices and their associated ses-
which external calls are treated as cryptographic abstractions or         sions. To establish a pairwise encrypted conversation between two
environment stubs, and (c) stating the verification query for the         users, Sesame manages an instance of the double ratchet protocol
chosen backend. For BAC, this required a few hours of reverse             (including X3DH key agreement) between each of their devices.
engineering and modeling. For WhatsApp, locating and validating           4.1.2 Extracted Model. We abstract the X3DH key agreement pro-
protocol-relevant entry points in Ghidra required a few days; after       tocol with a private channel that ‘magically’ communicates a master
that, the remainder of the pipeline was fully automated.                  secret key (initial root key) between two parties. Like in the hand-
                                                                          written Tamarin model for Signal in [39], this avoids verification
4.1     Evaluation of WhatsApp with CryptoBap                             issues with Tamarin’s limited Diffie-Hellman (DH) theory (see
WhatsApp allows users to exchange messages, share status posts,           [34, Sec. 2.3 and 2.4] for further discussion on the support of DH
and make audio and video calls. Since 2016 [88] WhatsApp uses             theories in Tamarin and other protocol verifiers).
a modified version of the Open Whisper Systems’ Signal protocol              Excluding X3DH, we extract a model of the core components:
Automated Side-Channel Analysis of Cryptographic Protocol Implementations                                  CCS ’26, November 15–19, 2026, The Hague, Netherlands


                            #ARM         #symb. exec. paths        #Sapic+        LoC          #TM   #PV        time to        extract        Overall verif. time
  WhatsApp Protocol
                         instructions   feasible infeasible    all     simplified   crypto.    LoC   LoC    all      simplified     crypto.   TM          PV
  (1) Initiate Session       6844           12        25       106    61 (42% ↓)      33                    13        14 (7% ↑)        12
  (2) Respond to (1)         5803          106       413       718    92 (87% ↓)      12                    65        60 (7% ↓)        38
                                                                                               161   171                                      19.76     0.057
  (3) Send Message           3041          156       368       983    429 (56% ↓)     166                   71      100 (40% ↑)        65
  (4) Receive Message        4181         7293      19322     31257 2033 (93% ↓)      360                  26903 40128(49% ↑) 25782
Table 2: WhatsApp protocol analysis. The table includes, the size of the code under analysis, the explored symbolic paths, the
extracted models—complete and simplified, consisting solely of cryptographic operations, and translated into Tamarin and
ProVerif—along with the duration (in seconds) of each step. TM and PV refer to Tamarin and ProVerif, respectively.



   (1) initiating a new session in which the client requests the re-                but WhatsApp’s source code is closed. Ultimately, formal analysis
       cipient’s keys from the WhatsApp server and calculates a                     results rely on the adequacy of the model. Gaps through underspec-
       session key,                                                                 ification or misspecification can lead to overlooking attacks.
   (2) responding to a request to initiate a new session by the recipi-
       ent and calculating the corresponding session key,                           4.1.4 Authenticity with Tamarin & ProVerif. We used our ex-
   (3) transmitting messages in a session (symmetric ratchet), and                  tracted model to analyze WhatsApp’s session management and
   (4) receiving messages within a session (asymmetric ratchet).                    double ratchet protocol with Tamarin and ProVerif.
                                                                                        Utilizing these tools, we verify the security properties of our
   Table 2 presents the data obtained from our evaluation of the                    extracted model by defining queries and checking the reachability
WhatsApp components using Tamarin and ProVerif.                                     of all events in the model. Forward secrecy ensures that past session
   By considering all memory operations and function calls (but                     keys remain secure even if long-term keys are compromised. Our
abstracting cryptographic library calls), we initially obtain a Sapic+              analysis shows that Tamarin and ProVerif successfully verify
model with nearly 33,000 LoC. Simplification (Section 3.5) reduces                  forward secrecy for two parties initiating a session and exchanging
this to about 2,600 LoC, but both Tamarin and ProVerif still fail to                secret messages. On the other hand, post-compromise security en-
terminate at this scale. For the reachability analysis reported below,              sures that if an attacker gains access to a party’s state, the protocol
we therefore use CryptoBap’s memory-abstraction variant (i.e.,                      can “heal” and prevent the attacker from compromising future ses-
without explicit load/store primitives). This variant yields a sub-                 sions. However, WhatsApp violates post-compromise security despite
stantially smaller Sapic+ model that remains suitable for analyzing                 employing the double ratchet protocol when faced with a clone at-
security properties under the Dolev–Yao attacker model (the corre-                  tacker. Our analysis revealed this major issue, which prior work [39]
sponding model’s lines of code are presented in the “crypto.” column                had identified in the Signal application and suspected in WhatsApp.
of Table 2). We highlighted the memory-aware numbers above to                       Cremers et al. [39] have proposed secure mechanisms that offer
emphasize the scalability bottleneck of state-of-the-art protocol                   stronger guarantees. However, our analysis showed that WhatsApp
verifiers that currently prevents full memory-precise verification                  does not implement any of the proposals, allowing a clone attacker
of large real-world binaries.                                                       to break post-compromise security.
                                                                                        Note, while the analysis of Signal’s implementation benefits from
4.1.3 Implementation vs. Specification. We find that, in certain sce-
                                                                                    direct access to the source code (the model in [39] was manually
narios, the protocol implementation behaves differently from its
                                                                                    crafted but informed by the code), our models were derived entirely
specification in the WhatsApp security white-paper [88], in partic-
                                                                                    from the binary. Moreover, while ProVerif automatically iden-
ular the component responsible for decrypting incoming messages
                                                                                    tifies the post-compromise security violation for WhatsApp, we
(i.e., the component number 4 in Table 2). The white paper specifies
                                                                                    employed heuristics to guide Tamarin’s proof search and manually
that the chain and root keys are updated upon receiving a response,
                                                                                    selected 303 proof steps from the available options.
yet it lacks a sufficient explanation of the ratcheting mechanism [88,
p.15] (in contrast to the Signal documentation [53]). According to
WhatsApp, the ratcheting process involves each party calculating                    4.2       Side-Channel Analysis
its next chain and root keys using a shared ephemeral secret, de-                   The second part of our evaluation demonstrates how side-channel
rived from the sender’s and receiver’s ephemeral keys, and a root                   analysis of protocol implementations can reveal hardware-induced
key whose origin is not clearly defined. Instead, our model indicates               leakages. Although abstract formal models and implementations
three distinct behaviors for ratcheting. The next chain key is either               of cryptographic protocols are often formally verified against se-
derived from: (a) the current chain key, (b) the new chain key, cal-                curity properties, they have not been analyzed in the presence of
culated from fresh root and ephemeral keys, and (c) the fresh chain                 hardware-induced leakages. Our methodology addresses this gap
key, calculated from the current root key and a new ephemeral key.                  by combining model extraction with leakage contracts, enabling
    This highlights the strength of model extraction. Most protocol                 automated analysis of side-channel leaks. We focus on BAC and
models have to rely on the specification to be correct, even if the                 WhatsApp due to their widespread use in real-world scenarios
source is available, a thorough comparison is tedious and requires                  and their critical security implications to evaluate their resilience
tool support (such as model extraction for the source language). Of-                against potential attacks.
ten, behaviors are underspecified (as in this case), and the modeler                   In these case studies, we assume the attacker can influence pro-
fills the gap. Sometimes source-code inspection helps fill the gap,                 tocol inputs, e.g., by replaying or crafting messages. Additionally,
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                        Faezeh Nasrabadi, Robert Künnemann, and Hamed Nemati


the attacker can observe microarchitectural side effects captured by        DeepSec checks trace equivalence, which is typically used to
our observation models, including program counter and load/store         formalize privacy properties such as unlinkability and voting pri-
addresses, as would be possible for a co-resident process performing     vacy [35]. As a baseline, we analyze the standard unlinkability prop-
cache attacks. Thus, the detected distinguishers reveal violations       erty for WhatsApp session establishment. Informally, unlinkability
that are triggerable by network interaction but observable through       requires that an attacker cannot distinguish between two executions
side channels on the victim device.                                      in which Alice establishes a session with different communication
                                                                         partners (e.g., Bob versus Charlie). In our bounded analysis, this
                                                                         standard unlinkability property holds for both extracted models,
4.2.1 Basic Access Control Protocol. Many countries are adopting
                                                                         under Mct and Mspec .
electronic biometric passports, a.k.a. e-passports. These passports
                                                                            We then consider a refined, application-level privacy property
encode the holder’s digital information within a Radio Frequency
                                                                         that captures whether a session establishment corresponds to a
Identification (RFID) chip for interaction with passport readers.
                                                                         first contact with a recipient or to a subsequent session within
However, e-passports face several threats related to security and
                                                                         an already existing conversation. Intuitively, an attacker should
privacy, including skimming, cloning, and eavesdropping [13, 52].
                                                                         not be able to distinguish these two cases. When analyzing this
To address these concerns, the International Civil Aviation Organi-
                                                                         refined property, DeepSec finds a distinguisher under Mct (and
zation (ICAO) standardized security mechanisms, among those, the
                                                                         hence also under Mspec ). The interpretation of this distinguisher
BAC protocol. BAC’s goal is to ensure that only authorized parties
                                                                         and the resulting privacy attack are discussed in Section 4.2.3.
can access personal information stored in passports’ RFID. A party
                                                                            As in the rest of our analysis, we assume an honest WhatsApp
(the reader) is authorized if they know a machine-readable code
                                                                         server. Communication between WhatsApp clients and the server—
printed on each e-passport, which the passport holder typically pro-
                                                                         which is, in practice, protected by the Noise protocol framework [88,
vides by physically handing the passport to the reader or scanning
                                                                         p. 35]—is modeled using private channels.
it themselves (if the reader is a device).
    Despite the ICAO standard’s goal to create an unlinkable BAC         4.2.3 Discovery of Privacy Attack. The distinguisher reported by
protocol, some implementations of the protocol permit reidentifi-        DeepSec corresponds to a privacy attack that reveals whether a
cation of a passport holder. Arapinis et al. [11] found that these       victim (i.e., a WhatsApp account holder) is establishing a secure
implementations output different error messages if a replayed mes-       session with a recipient for the first time or is establishing a new
sage is invalid due to an incorrect MAC or an incorrect nonce. As        session for an existing conversation.
the second case can only occur when the message is replayed to the          For every secure session establishment, the initiator retrieves the
same passport (because each interaction uses a fresh nonce), while       recipient’s pre-key bundle from the WhatsApp server. This bundle
the first can only occur if the message is replayed to a different       contains the recipient’s public identity key, public signed pre-key,
passport (as the MAC key is fixed per passport), this allows for iden-   and, when available, a public one-time pre-key (OTPK) [88]. Ac-
tification of the passport holder. Subsequently, the error messages      cording to the WhatsApp security whitepaper [88], the recipient’s
were unified, but Chothia and Smirnov [36] find that all e-passports     public OTPK is used only once and is removed from the server
are still vulnerable to a variant of the attack where instead of the     after it has been requested to initiate the first-time conversation.
error message, the attacker measures the computation time of the         Consequently, the presence or absence of an OTPK in the retrieved
passport’s response to distinguish the incorrect-MAC branch and          pre-key bundle reflects whether the session establishment corre-
the incorrect-nonce branch.                                              sponds to a first contact or a subsequent session. This observation
    To show how our methodology finds such attacks on critical sys-      leaks information about the victim’s social interactions. In partic-
tems, we implemented the BAC protocol ourselves. While the ma-           ular, it reveals if the victim is contacting a recipient for the first
chine code is not easily extractable from RFID chips for researchers     time or is communicating with a recipient with whom a secure re-
(and the legal implications are unclear), standardization bodies         lationship has already been established. The attack applies to both
could request access and run similar analyses. As depicted in Fig-       one-to-one conversations and group chats. An attacker can repeat-
ure 5, our implementation does not allow distinction by error mes-       edly add selected users to groups that include the victim and use the
sage, but rather by side-channel leakage. Using our methodology,         side channel to infer whether prior communication relationships
we found that an attacker can use this leak to distinguish between       exist (see Section 4.2.4). Repeating this process enables reconstruc-
both types of failures and thus break unlinkability. The implemen-       tion of the victim’s social graph, revealing sensitive information
tation is vulnerable under both Mct and Mspec , see Table 3.             about the victim’s relationships, interests, and activities.
                                                                            Our analysis identified this attack automatically. After annotat-
                                                                         ing the BIR program of the session-initiation component with the
4.2.2 Privacy Properties with DeepSec. To analyze the WhatsApp
                                                                         observational models, extracting the respective models, and trans-
application’s vulnerability to hardware-induced leaks, we begin
                                                                         lating them into DeepSec, the tool detected a distinguisher associ-
with the BIR translation of the session-initiation component de-
                                                                         ated with the conditional processing of the recipient’s OTPK. This
fined in Section 4.1.2, Item 1. We annotate this BIR program using
                                                                         control-flow dependency is observable through instruction-cache
both the constant-time model (Mct ) and the speculation model
                                                                         side channels and therefore violates the refined privacy property
(Mspec ). For each annotated BIR program, we perform symbolic
                                                                         introduced in Section 4.2.2.
execution, extract the corresponding Sapic+ model, and translate
it into DeepSec. The evaluation results for the session-initiation       4.2.4 Attack Vector (Instruction Cache). In our model, the above
component with DeepSec are summarized in Table 3.                        attack requires the side channel to reveal the program’s control
Automated Side-Channel Analysis of Cryptographic Protocol Implementations                                             CCS ’26, November 15–19, 2026, The Hague, Netherlands


                                #ARM       # symb. exec. paths    # Sapic+ LoC    # DeepSec   time to extract  Verif. time in
              Protocols
                             instructions feasible infeasible   all    simplified    LoC     all    simplified   DeepSec
 BAC with Mct                     176          5         69     242    83 (65% ↓)     205     9      7 (22% ↓)        1
 BAC with Mspec                   194         15        170     630 240 (61% ↓)       589    22    18 (18% ↓)         7
 Initiate Session with Mct       6844         12         65     283    90 (68% ↓)     220    43      44 (2% ↑)        2
 Initiate Session with Mspec     6899        120        679    2872 903 (68% ↓)      2191    148 130 (12% ↓)          5
Table 3: Case studies with observation models. Columns show: ARM code size, number of symbolic paths analyzed, extracted
model size (raw, simplified, and after translation to DeepSec), and time (seconds) per step.



flow to learn the presence or absence of the recipient’s public one-                           WhatsApp groups unrelated to their journalistic work. 𝑅 convinces
time pre-key (OTPK). Both observation models represent realistic                               a moderator in this group to include 𝑇 in a chat discussion. Using
attack vectors [29]; we will now outline how our attack can be                                 our attack, 𝑅 confirms that 𝑉 was in contact with 𝑇 .
realized as an instruction cache attack. Such attacks exploit the
timing differences in the processor instruction cache behavior to                              5 Related Work
infer which program paths are executed without requiring direct
access to the program counter or memory contents.                                              5.1 Protocol Verification
   WhatsApp Desktop’s assembly code includes a conditional branch                              The usage of formal methods to analyze protocols and verify proper-
that checks for the existence of the one-time pre-key in the pre-key                           ties like secrecy and authentication dates back to Lowe’s work [63].
bundle during session establishment. When the one-time pre-key                                 Traditionally, domain experts translate protocol specifications into
is present (indicating a first-time conversation), a specific set of                           formal models to analyze high-level behavior using theorem prov-
instructions is executed to process it, whereas a different program                            ing [17, 79], model checking [16, 63], and symbolic analysis [24,
path is taken if the key is absent (indicating an existing conversa-                           34, 67]. Tools like ProVerif [24] and Tamarin [67] are effective in
tion). These two distinct execution paths result in different patterns                         verifying security properties. But, these specification-based mod-
of instruction cache usage. In our proof-of-concept attack imple-                              els abstract away implementation details, potentially overlooking
mentation, we used the Prime+Probe technique [80] to monitor the                               vulnerabilities introduced during execution, like hardware-induced
instruction cache by co-locating a process on the same CPU core                                leakages [56, 61] or compiler bugs [83, 84].
as the WhatsApp Desktop application. Interested readers can find                                  To address discrepancies between specifications and implemen-
the details of our PoC in Appendix A.                                                          tations, techniques like fuzz testing [10, 27], differential testing [64],
   In a Prime+Probe attack, the attacker first ‘primes’ the instruc-                           symbolic execution [9], code generation [6, 31], deductive verifica-
tion cache by executing their own code to fill specific cache sets.                            tion [12, 31, 58], and type checking [22, 23] have been employed,
Next, the attacker triggers the victim to establish a new encrypted                            which target the implementation of protocols. Model extraction
session, e.g., by initiating a group chat with the victim and inviting                         techniques further aim to verify implementations in high-level lan-
the third person. Then, the attacker ‘probes’ the cache by measuring                           guages like 𝐹 # [14, 21], Java [54, 78], C [9, 48], and Rust [58]. Yet,
the time it takes to re-execute their code. If the victim’s execution of                       the complexity of these languages limits their practicality.
the pre-key processing code evicts the attacker’s instructions from                               CryptoBap addresses these gaps by extracting formal models
the cache (due to cache set conflicts), the probe will take longer,                            directly from protocol machine code, avoiding reliance on speci-
revealing that the ‘first-time conversation’ path was taken. Con-                              fications or high-level code. Our work builds on CryptoBap, but
versely, if the cache remains largely untouched, it indicates the                              extends the analysis along three axes: we (i) begin from the bi-
‘existing conversation’ path was executed. By mapping the What-                                nary of real (closed-source) applications—not the one we compile
sApp application’s instruction addresses to cache sets, the attacker                           ourselves, (ii) instrument the lifted binary with leakage contracts
can reliably distinguish between these two cases. The instruction                              (e.g., constant-time and speculative observation models) and extract
cache attack eliminates the need to observe the program counter in                             observation-aware models, and (iii) connect the extracted models
the clear or have privileged access to the victim’s system memory.                             to equivalence-based verification in order to reason about protocol
                                                                                               properties (e.g., unlinkability) in the presence of microarchitectural
Real-World Impact. The vulnerabilities we discovered have a real-                              observations.
life impact. Imagine that 𝑉 is a journalist connected with numerous                               This enables us to use the extracted models to assess (a) whether
sources, including whistle-blower 𝑇 . The attacker 𝑅 is a regime that                          protocol properties are preserved in the presence of hardware leaks
enforces its citizens to install a certain application which allows it to                      and (b) the existence of microarchitectural leakages through the
mount instruction cache attacks.2 The regime infiltrates some of 𝑉 ’s                          protocol verifier DeepSec. Unlike CryptoBap, we extract the mem-
2 This is plausible, e.g., Russia [19], Kazakhstan [1], Saudi Arabia [5] and Singapore [2]     ory operation models into Sapic+ and apply simplification rules to
provide certain services like visa or passport requests, tax declaration, or social services   scale the extracted models for analysis with protocol verifiers.
exclusively via government-provided Smartphone Apps. In other countries, like Austria,
Estonia, or Germany digitalized services with a strong App focus increase the pressure
to install such Apps, often in connection to digital ID [18]. Some states in the U.S. also     5.2    Side-Channel Analysis of Crypto Libraries
increase the pressure to install Apps for social services [77]. Many more countries
had indirect enforcement of the use of Apps during the COVID-19 pandemic, e.g., to             In recent years, side-channel detection, mitigation, and formal anal-
access public buildings or for citizens who tested positive [4].                               ysis have become active areas of research, with numerous papers
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                         Faezeh Nasrabadi, Robert Künnemann, and Hamed Nemati


published on the topic. Here, we do not intend to survey all works        trace equivalence as long as (symbolic) traces with consistent as-
in this domain (an incomplete list can be found [32, 62]); rather, we     signments are only mapped to (symbolic) traces with consistent
focus on a few selected works that are closer to our approach.            assignments. In our concrete application, this could be achieved
   Crypto libraries have been the prime target of side-channel at-        by revealing the path constraints in the trace, as the program is
tacks, e.g., timing attacks. The constant-time (CT) paradigm mit-         compared to itself and thus the conditionals are observed through
igates these by ensuring control flow and memory accesses are             the program-counter observations.
independent of secret data under sequential execution [20]. High-
assurance frameworks like Jasmin [76] and FaCT [81] use formal               Component selection via Ghidra. We currently identify What-
methods, such as information-flow type systems, to enforce CT and         sApp components manually in Ghidra using (i) preserved function
produce verified, efficient implementations.                              symbols corresponding to the Signal protocol, and (ii) interactions
   However, Spectre attacks [55], exploiting speculative execution,       with the crypto library and network I/O, which can be systemati-
challenge the CT paradigm by leaking secrets even in CT-compliant         cally recognized [68]. In principle, information-flow analysis could
code. Research has extended CT to speculative constant-time (SCT)         automate this step by combining existing detection techniques [68]
to protect against Spectre variants. Shivakumar et al. [82] intro-        with conservative over-approximation (treating all incoming inputs
duced a type system in Jasmin for SCT against Spectre-v1 with mini-       as arbitrary). We are working toward integrating such automation.
mal overhead using selective speculative load hardening. They have           Mitigation against side-channel attacks. Side-channel risks
also addressed declassification issues under speculation, propos-         can be reduced either by constant-time rewrites (eliminating secret-
ing relative non-interference (RNI) and efficient countermeasures.        dependent branches and memory access patterns) or by removing
Arranz Olmos et al. [76] extended this to all Spectre variants, in-       the cache channel (e.g., isolation/partitioning or cache flushes). Im-
cluding Spectre-RSB, with low overheads. Other approaches like            plementations with effective isolation, partitioning, or flushing are
Swivel [70] and Serberus [69] offer protections but may rely on           not vulnerable under our observation-based model. Our toolchain
hardware or incur higher overheads.                                       can validate code-level mitigations by re-extracting the binary and
   SCT-style work primarily targets CT guarantees for crypto prim-        re-running DeepSec equivalence under Mct and then Mspec . How-
itive implementations and often reasons about a concrete source           ever, we cannot currently verify fence-based mitigations or hard-
language or assembly semantics. Our work is complementary. We             ware/OS defenses; doing so would require extending the underlying
take observation models inspired by Scam-V/SCT-style semantics            semantics and observation models.
and lift them to Sapic+ protocol models in order to analyze protocol-
level properties that can be violated by application (e.g., secret-          Limitations of protocol verifiers. The extracted models can
dependent error handling or first-contact branches), even when            reach the practical limits of current protocol verifiers. Even hand-
cryptographic primitives are treated as ideal. Throughout, we use         written and optimized models (e.g., for TLS 1.3 [38], WPA2 [40],
“hardware-induced” leakage in the microarchitectural sense (e.g.,         and SPDM [37]) may require hours to days of verification time,
cache-based observations), and do not model physical channels             substantial memory, and extensive proof guidance. These tools
such as electromagnetic (EM) or power.                                    have improved on protocol complexity, but not primarily on scaling
   However, previous studies did not connect microarchitectural           with the size of automatically generated rule sets. Consequently, our
side-channel reasoning to protocol-level verification of real proto-      methodology would benefit from better support for decomposition
col implementations (as opposed to specifications or isolated primi-      and modular verification, which remains limited in existing tools.
tives); this is the gap we target. In this work, we propose a method-
ology designed to identify such leakages and address this gap.               Dependence on crypto libraries. Our analysis is conducted
                                                                          in the Dolev–Yao model and therefore assumes crypto libraries are
                                                                          trusted. If primitives deviate due to bugs, unexpected weaknesses,
6    Discussions                                                          or their own side channels, our conclusions may not hold.
   Soundness of proposed methodology. Regarding our method-                  Applicability constraints. Our approach assumes access to
ology soundness, transpilation from assembly to BIR and symbolic          the target binaries and reliance on a known cryptographic library.
execution remain sound, although we lack formal proofs validating         In some settings (e.g., e-passport implementations), external re-
our translation to Sapic+ (see Section 3.4). Since our primary ob-        searchers may not have access to code at all. While WhatsApp
jective with the proposed methodology is attack detection, this is        employs basic obfuscation, we were still able to extract meaning-
acceptable, as attacks can be manually validated if false positives re-   ful models; more targeted anti-analysis obfuscation could impede
main manageable. However, a positive security result from DeepSec         extraction, though such measures may themselves be suspicious.
cannot be fully trusted. For instance, we obtain a verification result
for the strong secrecy of the master key (initial root key) derived          ISA and scalability limitations. Our implementation targets
during WhatsApp’s session initialization with DeepSec, but refrain        AArch64 and RISC-V because HolBA provides lifting for these ISAs.
from reporting it as we cannot be sure it would hold.                     Supporting additional ISAs (e.g., x86-64) requires a lifter with com-
   Symbolic execution is usually only shown sound, but it is possi-       parable semantic assurance. Scalability is limited by symbolic exe-
ble to show its completeness w.r.t. assignments consistent with a         cution and by the size of extracted Sapic+ models, especially when
path condition. If the subsequent translation step can be shown to        modeling memory explicitly. This motivates using a memory ab-
maintain that pattern, we should be able to show that a symbolic          straction for full-program reachability in WhatsApp, and focusing
equivalence between the translated processes implies a concrete           observation-aware side-channel analyses on smaller components.
Automated Side-Channel Analysis of Cryptographic Protocol Implementations                                          CCS ’26, November 15–19, 2026, The Hague, Netherlands


   Scope of side-channel modeling. Our leakage contracts ex-                            [12] Linard Arquint, Felix A. Wolf, Joseph Lallemand, Ralf Sasse, Christoph Sprenger,
pose a small observation set (program counter information, sym-                              Sven N. Wiesner, David Basin, and Peter Müller. 2022. Sound Verification of
                                                                                             Security Protocols: From Design to Interoperable Implementations (Extended
bolic load/store addresses, plus speculative “shadow” observations).                         Version). arXiv:2212.04171 [cs]
This captures many cache-based attacks, but not all physical or                         [13] Gildas Avoine, Antonin Beaujeant, Julio Hernandez-Castro, Louis Demay, and
                                                                                             Philippe Teuwen. 2016. A survey of security and privacy issues in ePassport
microarchitectural effects. Thus, a found distinguisher indicates                            protocols. ACM Computing Surveys (CSUR) 48, 3 (2016), 1–37.
a concrete leak, whereas a proved equivalence does not exclude                          [14] Michael Backes, Matteo Maffei, and Dominique Unruh. 2010. Computationally
channels outside the observation set.                                                        sound verification of source code. In Proceedings of the 17th ACM conference on
                                                                                             Computer and communications security. 387–398.
                                                                                        [15] Gilles Barthe, Gustavo Betarte, Juan Campo, Carlos Luna, and David Pichardie.
7    Concluding Remarks                                                                      2014. System-level non-interference for constant-time cryptography. In Pro-
                                                                                             ceedings of the 2014 ACM SIGSAC Conference on Computer and Communications
We presented a methodology for analyzing crypto protocol im-                                 Security. 1267–1279.
plementations that combines binary-level model extraction with                          [16] David Basin, Cas Cremers, and Catherine Meadows. 2018. Model Checking
protocol verification under explicit leakage contracts. Our approach                         Security Protocols. In Handbook of Model Checking, Edmund M. Clarke, Thomas A.
                                                                                             Henzinger, Helmut Veith, and Roderick Bloem (Eds.). Springer International
extends CryptoBap with attacker observation instrumentation, a                               Publishing, Cham, 727–762. doi:10.1007/978-3-319-10575-8_22
Ghidra-assisted front-end for locating protocol code in real binaries,                  [17] David Basin, Andreas Lochbihler, Ueli Maurer, and S Reza Sefidgar. 2021. Ab-
                                                                                             stract modeling of system communication in constructive cryptography using
and an equivalence-checking backend (DeepSec) for privacy and                                CryptHOL. In 2021 IEEE 34th Computer Security Foundations Symposium (CSF).
conditional non-interference.                                                                IEEE, 1–16.
   We extracted an implementation-level model of WhatsApp Desk-                         [18] Marc Bennetts. 2025. E-government in Europe. https://en.wikipedia.org/wiki/E-
                                                                                             government_in_Europe
top’s session management and double ratchet components and veri-                        [19] Marc Bennetts. 2025. Putin launches spy app to keep Russians in ‘digital
fied forward secrecy, while confirming a post-compromise security                            gulag’.    https://www.thetimes.com/world/russia-ukraine-war/article/putin-
break against a clone attacker. For side-channel, we found a new                             moscow-whatsapp-ban-plan-max-app-launch-b789tt6ts
                                                                                        [20] Daniel J. Bernstein. 2006. Curve25519: New Diffie-Hellman Speed Records. In
instruction-cache leak in WhatsApp session establishment that en-                            Public Key Cryptography - PKC 2006, 9th International Conference on Theory
ables social-graph inference and confirmed the known unlinkability                           and Practice of Public-Key Cryptography, New York, NY, USA, April 24-26, 2006,
                                                                                             Proceedings (Lecture Notes in Computer Science, Vol. 3958), Moti Yung, Yevgeniy
break in BAC under microarchitectural observations.                                          Dodis, Aggelos Kiayias, and Tal Malkin (Eds.). Springer, 207–228. doi:10.1007/
   Our results suggest that protocol implementations deserve the                             11745853_14
same rigor of side-channel analysis traditionally applied to crypto-                    [21] Karthikeyan Bhargavan, Cédric Fournet, and Andrew D Gordon. 2006. Verified
                                                                                             reference implementations of WS-Security protocols. In International Workshop
graphic libraries: protocol verifiers provide principled, composition-                       on Web Services and Formal Methods. Springer, 88–106.
aware notions of secrecy and privacy, and lifting these notions to                      [22] Karthikeyan Bhargavan, Cédric Fournet, and Andrew D Gordon. 2010. Modular
implementation traces makes it possible to detect protocol-level                             verification of security protocol code by typing. ACM Sigplan Notices 45, 1 (2010),
                                                                                             445–456.
violations that are invisible in specification-only models.                             [23] Karthikeyan Bhargavan, Cédric Fournet, and Markulf Kohlweiss. 2016. miTLS:
                                                                                             Verifying Protocol Implementations against Real-World Attacks. IEEE Security &
Acknowledgments                                                                              Privacy 14, 6 (2016), 18–25. doi:10.1109/MSP.2016.123
                                                                                        [24] Bruno Blanchet. 2022. The Security Protocol Verifier ProVerif and Its Horn Clause
This work was partially supported by the Wallenberg AI, Autonomous                           Resolution Algorithm. Electronic Proceedings in Theoretical Computer Science 373
                                                                                             (Nov. 2022), 14–22. doi:10.4204/EPTCS.373.2
Systems and Software Program (WASP) funded by the Knut and                              [25] Bruno Blanchet et al. 2001. An efficient cryptographic protocol verifier based on
Alice Wallenberg Foundation. The first author was a PhD candidate                            prolog rules.. In 14th IEEE Computer Security Foundations Workshop (CSFW-14),
at Saarland University during the preparation of this work. We also                          Vol. 1. 82–96.
                                                                                        [26] Moller Bodo, Thai Duong, and Krzysztof Kotowicz. 2014. This POODLE bites:
gratefully acknowledge gifts from Intel and Amazon.                                          exploiting the SSL 3.0 fallback. In Security Advisory 21. 34–58.
                                                                                        [27] Marcel Böhme, Van-Thuan Pham, and Abhik Roychoudhury. 2016. Coverage-
References                                                                                   based greybox fuzzing as markov chain. In Proceedings of the 2016 ACM SIGSAC
                                                                                             Conference on Computer and Communications Security. 1032–1043.
 [1] 1992. E-government. https://en.wikipedia.org/wiki/E-government                     [28] David Brumley, Ivan Jager, Thanassis Avgerinos, and Edward J. Schwartz. 2011.
 [2] 2003. Singpass Singapore’s National Digital Identity (Factsheet). https://www.          BAP: A Binary Analysis Platform. In Computer Aided Verification. 463–469. doi:10.
     mddi.gov.sg/newsroom/singpass-factsheet-02032022                                        1007/978-3-642-22110-1_37
 [3] 2009. WhatsApp. https://www.whatsapp.com/about                                     [29] Pablo Buiras, Hamed Nemati, Andreas Lindner, and Roberto Guanciale. 2021.
 [4] 2020. TraceTogether. https://en.wikipedia.org/wiki/TraceTogether                        Validation of Side-Channel Models via Observation Refinement. In MICRO. doi:10.
 [5] 2021. Absher. https://en.wikipedia.org/wiki/Absher_%28application%29                    1145/3466752.3480130
 [6] Coşku Acay, Joshua Gancher, Rolph Recto, and Andrew C. Myers. 2024. Secure         [30] Cristian Cadar, Daniel Dunbar, Dawson R Engler, et al. 2008. Klee: unassisted
     Synthesis of Distributed Cryptographic Applications. In 2024 IEEE 37th Computer         and automatic generation of high-coverage tests for complex systems programs..
     Security Foundations Symposium (CSF). IEEE Computer Society, 433–448. doi:10.           In OSDI, Vol. 8. 209–224.
     1109/CSF61375.2024.00021                                                           [31] David Cadé and Bruno Blanchet. 2012. From computationally-proved protocol
 [7] Onur Acıiçmez and Çetin Kaya Koç. 2006. Trace-driven Cache Attacks on AES               specifications to implementations. In 2012 Seventh International Conference on
     (Short Paper). In Proceedings of the 8th International Conference on Information        Availability, Reliability and Security. IEEE, 65–74.
     and Communications Security (Raleigh, NC) (ICICS). Springer-Verlag, 112–121.       [32] Sunjay Cauligi, Craig Disselkoen, Daniel Moghimi, Gilles Barthe, and Deian
 [8] Alfred V. Aho, Monica S. Lam, Ravi Sethi, and Jeffrey D. Ullman. 2006. Compil-          Stefan. 2022. SoK: Practical Foundations for Software Spectre Defenses. In 43rd
     ers: Principles, Techniques, and Tools (2nd Edition). Addison-Wesley Longman            IEEE Symposium on Security and Privacy, SP 2022, San Francisco, CA, USA, May
     Publishing Co., Inc., USA.                                                              22-26, 2022. IEEE, 666–680. doi:10.1109/SP46214.2022.9833707
 [9] Mihail Aizatulin. 2015. Verifying Cryptographic Security Implementations in C      [33] Sunjay Cauligi, Craig Disselkoen, Klaus v Gleissenthall, Dean Tullsen, Deian
     Using Automated Model Extraction. Ph. D. Dissertation. The Open University.             Stefan, Tamara Rezk, and Gilles Barthe. 2020. Constant-Time Foundations for
     http://arxiv.org/abs/2001.00806                                                         the New Spectre Era. arXiv:1910.01755 [cs]
[10] Max Ammann, Lucca Hirschi, and Steve Kremer. 2024. DY fuzzing: formal Dolev-       [34] Vincent Cheval, Charlie Jacomme, Steve Kremer, and Robert Künnemann. 2022.
     Yao models meet cryptographic protocol fuzz testing. In 2024 IEEE Symposium on          SAPIC+: protocol verifiers of the world, unite!. In USENIX Security Symposium
     Security and Privacy (SP). IEEE, 1481–1499.                                             (USENIX Security), 2022.
[11] Myrto Arapinis, Tom Chothia, Eike Ritter, and Mark Ryan. 2010. Analysing           [35] Vincent Cheval, Steve Kremer, and Itsaka Rakotonirina. 2018. DEEPSEC: deciding
     unlinkability and anonymity using the applied pi calculus. In 2010 23rd IEEE            equivalence properties in security protocols theory and practice. In 2018 IEEE
     computer security foundations symposium. IEEE, 107–121.                                 symposium on security and privacy (SP). IEEE, 529–546.
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                                               Faezeh Nasrabadi, Robert Künnemann, and Hamed Nemati


[36] Tom Chothia and Vitaliy Smirnov. 2010. A traceability attack against e-passports.     [60] Andreas Lindner, Karl Palmskog, Scott Constable, Mads Dam, Roberto Guanciale,
     In International Conference on Financial Cryptography and Data Security. Springer.         and Hamed Nemati. 2026. Forward Symbolic Execution for Trustworthy Au-
[37] Cas Cremers, Alexander Dax, and Aurora Naska. 2024. Breaking and Prov-                     tomation of Binary Code Verification. In International Conference on Verification,
     ably Restoring Authentication: A Formal Analysis of SPDM 1.2 Including Cross-              Model Checking, and Abstract Interpretation. Springer, 147–172.
     Protocol Attacks. IACR Cryptol. ePrint Arch. (2024), 2047.                            [61] Moritz Lipp, Michael Schwarz, Daniel Gruss, Thomas Prescher, Werner Haas,
[38] Cas Cremers, Marko Horvat, Jonathan Hoyland, Sam Scott, and Thyla van der                  Jann Horn, Stefan Mangard, Paul Kocher, Daniel Genkin, Yuval Yarom, et al. 2020.
     Merwe. 2017. A Comprehensive Symbolic Analysis of TLS 1.3. In Proceedings                  Meltdown: Reading kernel memory from user space. Commun. ACM 63, 6 (2020).
     of the 2017 ACM SIGSAC Conference on Computer and Communications Security             [62] Xiaoxuan Lou, Tianwei Zhang, Jun Jiang, and Yinqian Zhang. 2022. A Survey
     (CCS ’17). Association for Computing Machinery, New York, NY, USA, 1773–1788.              of Microarchitectural Side-channel Vulnerabilities, Attacks, and Defenses in
     doi:10.1145/3133956.3134063                                                                Cryptography. ACM Comput. Surv. 54, 6 (2022), 122:1–122:37. doi:10.1145/3456629
[39] Cas Cremers, Charlie Jacomme, and Aurora Naska. 2023. Formal Analysis of              [63] Gavin Lowe. 1995. An Attack on the Needham-Schroeder Public-Key Authentica-
     Session-Handling in Secure Messaging: Lifting Security from Sessions to Conver-            tion Protocol. Inform. Process. Lett. 56, 3 (Nov. 1995), 131–133. doi:10.1016/0020-
     sations. In 32nd USENIX Security Symposium (USENIX Security 23). 1235–1252.                0190(95)00144-2
[40] Cas Cremers, Benjamin Kiesl, and Niklas Medinger. 2020. A Formal Analysis of          [64] William M McKeeman. 1998. Differential testing for software. Digital Technical
     IEEE 802.11’s WPA2: Countering the Kracks Caused by Cracking the Counters.                 Journal 10, 1 (1998), 100–107.
     In 29th USENIX Security Symposium, USENIX Security 2020, August 12-14, 2020,          [65] John McLean. 1992. Proving Noninterference and Functional Correctness Using
     Srdjan Capkun and Franziska Roesner (Eds.). USENIX Association, 1–17.                      Traces. J. Comput. Secur. 1, 1 (1992), 37–58. doi:10.3233/JCS-1992-1103
[41] Lesly-Ann Daniel, Sébastien Bardin, and Tamara Rezk. 2021. Hunting the Haunter        [66] Simon Meier, Benedikt Schmidt, Cas Cremers, and David Basin. 2013. The
     — Efficient Relational Symbolic Execution for Spectre with Haunted RelSE. In               TAMARIN prover for the symbolic analysis of security protocols. In Computer
     Proceedings 2021 Network and Distributed System Security Symposium. Internet               Aided Verification: 25th International Conference, CAV 2013, Saint Petersburg, Rus-
     Society, Virtual. doi:10.14722/ndss.2021.24286                                             sia, July 13-19, 2013. Proceedings 25. Springer, 696–701.
[42] AP David. 2021. Ghidra Software Reverse Engineering for Beginners: Analyze,           [67] Simon Meier, Benedikt Schmidt, Cas Cremers, and David Basin. 2013. The
     identify, and avoid malicious code and potential threats in your networks and              TAMARIN Prover for the Symbolic Analysis of Security Protocols. In Com-
     systems. Packt Publishing Ltd.                                                             puter Aided Verification, David Hutchison, Takeo Kanade, Josef Kittler, Jon M.
[43] HOL development team. 2022. HOL Interactive Theorem Prover. https://hol-                   Kleinberg, Friedemann Mattern, John C. Mitchell, Moni Naor, Oscar Nierstrasz,
     theorem-prover.org/                                                                        C. Pandu Rangan, Bernhard Steffen, Madhu Sudan, Demetri Terzopoulos, Doug
[44] Adel Djoudi and Sébastien Bardin. 2015. BINSEC: Binary Code Analysis with                  Tygar, Moshe Y. Vardi, Gerhard Weikum, Natasha Sharygina, and Helmut
     Low-Level Regions. In Proceedings of the 21st International Conference on Tools and        Veith (Eds.). Vol. 8044. Springer Berlin Heidelberg, Berlin, Heidelberg, 696–701.
     Algorithms for the Construction and Analysis of Systems - Volume 9035. Springer-           doi:10.1007/978-3-642-39799-8_48
     Verlag, Berlin, Heidelberg, 212–217. doi:10.1007/978-3-662-46681-0_17                 [68] Carlo Meijer, Veelasha Moonsamy, and Jos Wetzels. 2021. Where’s crypto?: Auto-
[45] Danny Dolev and Andrew Chi-Chih Yao. 1981. On the Security of Public Key                   mated identification and classification of proprietary cryptographic primitives in
     Protocols (Extended Abstract). In 22nd Annual Symposium on Foundations of                  binary code. In 30th USENIX Security Symposium (USENIX Security 21). 555–572.
     Computer Science, Nashville, Tennessee, USA, 28-30 October 1981. IEEE Computer        [69] Nicholas Mosier, Hamed Nemati, John C. Mitchell, and Caroline Trippel. 2024.
     Society, 350–357. doi:10.1109/SFCS.1981.32                                                 Serberus: Protecting Cryptographic Code from Spectres at Compile-Time. In IEEE
[46] PKI Task Force. 2004. PKI for machine readable travel documents offering ICC               Symposium on Security and Privacy, SP 2024, San Francisco, CA, USA, May 19-23,
     read-only access. Technical report, International Civil Aviation Organization              2024. IEEE, 4200–4219. doi:10.1109/SP54263.2024.00048
     (2004).                                                                               [70] Shravan Narayan, Craig Disselkoen, Daniel Moghimi, Sunjay Cauligi, Evan
[47] Anthony Fox. 2019. L3: a specification language for instruction set architectures.         Johnson, Zhao Gang, Anjo Vahldiek-Oberwagner, Ravi Sahita, Hovav Shacham,
     https://acjf3.github.io/l3                                                                 Dean M. Tullsen, and Deian Stefan. 2021. Swivel: Hardening WebAssembly
[48] Jean Goubault-Larrecq and Fabrice Parrennes. 2005. Cryptographic protocol                  against Spectre. In 30th USENIX Security Symposium, USENIX Security 2021, Au-
     analysis on real C code. In International Workshop on Verification, Model Checking,        gust 11-13, 2021, Michael D. Bailey and Rachel Greenstadt (Eds.). USENIX As-
     and Abstract Interpretation. Springer, 363–379.                                            sociation, 1433–1450. https://www.usenix.org/conference/usenixsecurity21/
[49] Daniel Gruss, Clémentine Maurice, Klaus Wagner, and Stefan Mangard. 2016.                  presentation/narayan
     Flush+Flush: A Fast and Stealthy Cache Attack. In Detection of Intrusions and Mal-    [71] Faezeh Nasrabadi, Robert Künnemann, and Hamed Nemati. 2023. CryptoBap:
     ware, and Vulnerability Assessment, Juan Caballero, Urko Zurutuza, and Ricardo J.          A Binary Analysis Platform for Cryptographic Protocols. In Proceedings of the
     Rodríguez (Eds.). Springer International Publishing, Cham, 279–299.                        2023 ACM SIGSAC Conference on Computer and Communications Security (CCS
[50] Roberto Guanciale, Musard Balliu, and Mads Dam. 2020. Inspectre: Breaking                  ’23), November 26–30, 2023, Copenhagen, Denmark. 1362–1376. https://doi.org/10.
     and fixing microarchitectural vulnerabilities by formal analysis. In Proceedings           1145/3576915.3623090
     of the 2020 ACM SIGSAC Conference on Computer and Communications Security.            [72] Faezeh Nasrabadi, Robert Künnemann, and Hamed Nemati. 2025. Symbolic
     1853–1869.                                                                                 Parallel Composition for Multi-language Protocol Verification. 38th IEEE Com-
[51] Marco Guarnieri, Boris Köpf, Jan Reineke, and Pepe Vila. 2021. Hardware-                   puter Security Foundations Symposium (CSF) (2025). https://ieeexplore.ieee.org/
     software contracts for secure speculation. In 2021 IEEE Symposium on Security              document/11097842
     and Privacy (SP). IEEE, 1868–1883.                                                    [73] Faezeh Nasrabadi, Robert Künnemann, and Hamed Nemati. 2026. Automated
[52] Gerhard P Hancke. 2011. Practical eavesdropping and skimming attacks on                    Side-Channel Analysis of Cryptographic Protocol Implementations-Source Code.
     high-frequency RFID tokens. Journal of Computer Security 19, 2 (2011), 259–288.            https://github.com/FMSecure/CryptoBAP/tree/ccs2026
[53] Signal Inc. Latest Version Updated on 2025. The Signal Specifications. Technical      [74] Hamed Nemati, Pablo Buiras, Andreas Lindner, Roberto Guanciale, and Swen
     Report. https://signal.org/docs/                                                           Jacobs. 2020. Validation of Abstract Side-Channel Models for Computer Architec-
[54] Jan Jürjens. 2009. Automated security verification for crypto protocol imple-              tures. In Computer Aided Verification, Shuvendu K. Lahiri and Chao Wang (Eds.).
     mentations: Verifying the jessie project. Electronic Notes in Theoretical Computer         Springer International Publishing, Cham, 225–248.
     Science 250, 1 (2009), 123–136.                                                       [75] Michael Neve and Jean-Pierre Seifert. 2007. Advances on Access-driven Cache
[55] Paul Kocher, Jann Horn, Anders Fogh, and Daniel Genkin. 2019. Daniel Gruss,                Attacks on AES. In Proceedings of the 13th International Conference on Selected
     Werner Haas, Mike Hamburg, Moritz Lipp, Stefan Mangard, Thomas Prescher,                   Areas in Cryptography (Montreal, Canada) (SAC’06). Springer-Verlag, 147–162.
     Michael Schwarz, and Yuval Yarom. Spectre Attacks: Exploiting Speculative             [76] Santiago Arranz Olmos, Gilles Barthe, Chitchanok Chuengsatiansup, Benjamin
     Execution. In 40th IEEE Symposium on Security and Privacy (S&P’19).                        Grégoire, Vincent Laporte, Tiago Oliveira, Peter Schwabe, Yuval Yarom, and
[56] Paul Kocher, Jann Horn, Anders Fogh, Daniel Genkin, Daniel Gruss, Werner                   Zhiyuan Zhang. 2024. Protecting cryptographic code against Spectre-RSB. IACR
     Haas, Mike Hamburg, Moritz Lipp, Stefan Mangard, Thomas Prescher, et al. 2020.             Cryptol. ePrint Arch. (2024), 1070. https://eprint.iacr.org/2024/1070
     Spectre attacks: Exploiting speculative execution. Commun. ACM 63, 7 (2020).          [77] Kentrell Owens, Anita Alem, Franziska Roesner, and Tadayoshi Kohno. 2022.
[57] Steve Kremer and Robert Künnemann. 2016. Automated analysis of security                    Electronic Monitoring Smartphone Apps: An Analysis of Risks from Technical,
     protocols with global state. Journal of Computer Security 24, 5 (2016), 583–616.           Human-Centered, and Legal Perspectives. In 31st USENIX Security Symposium
[58] Andrea Lattuada, Travis Hance, Jay Bosamiya, Matthias Brun, Chanhee Cho, Hay-              (USENIX Security 22). USENIX Association, Boston, MA, 4077–4094. https:
     ley LeBlanc, Pranav Srinivasan, Reto Achermann, Tej Chajed, Chris Hawblitzel,              //www.usenix.org/conference/usenixsecurity22/presentation/owens
     Jon Howell, Jacob R. Lorch, Oded Padon, and Bryan Parno. 2024. Verus: A Practi-       [78] Nicholas O’Shea. 2008. Using Elyjah to analyse Java implementations of cryp-
     cal Foundation for Systems Verification. In Proceedings of the ACM SIGOPS 30th             tographic protocols. In Joint Workshop on Foundations of Computer Security,
     Symposium on Operating Systems Principles (SOSP ’24). Association for Computing            Automated Reasoning for Security Protocol Analysis and Issues in the Theory of
     Machinery, New York, NY, USA, 438–454. doi:10.1145/3694715.3695952                         Security (FCS-ARSPA-WITS-2008).
[59] Andreas Lindner, Roberto Guanciale, and Roberto Metere. 2019. TrABin:                 [79] Lawrence C. Paulson. 1998. The Inductive Approach to Verifying Cryptographic
     Trustworthy analyses of binaries. Sci. Comput. Program. 174 (2019), 72–89.                 Protocols. Journal of Computer Security 6, 1-2 (Jan. 1998), 85–128. doi:10.3233/JCS-
     doi:10.1016/j.scico.2019.01.001                                                            1998-61-205
Automated Side-Channel Analysis of Cryptographic Protocol Implementations                                     CCS ’26, November 15–19, 2026, The Hague, Netherlands


                                                                                           In each cycle, the attacker primes the instruction cache by ac-
                                                                                        cessing other code mapping to these cache sets and lines. After a
                                                                                        short delay allowing for potential victim execution, the attacker
                                                                                        re-accesses the same addresses and measures the latency (Δ𝑡). El-
                                                                                        evated latency indicates eviction, implying the victim executed
                                                                                        instructions mapping to the same cache line; low latency suggests
                                                                                        the lines remained untouched.
                                                                                           Our macOS-compatible iteration of Flush+Flush integrates timing-
                                                                                        based cache probing via mach_absolute_time(), which yields a high-
                                                                                        resolution timestamp in platform-dependent units, enabling precise
                                                                                        measurement of access latency. This straightforward access-timing
                                                                                        technique infers potential cache evictions, improving the accuracy
Figure 8: Observed access latency (Δ𝑡). session_builder is                              of cache-related timing.
the address of the function initiating a secure session, and                               Figure 8 shows a time series of the latency Δ𝑡: the x-axis is
OTPK_exists the address of an instruction run when a one-                               time (in microseconds), the y-axis is the latency. Distinct spikes
time pre-key creates the session’s master secret.                                       correspond to the victim executing one or both target code paths,
                                                                                        revealing first-time conversation establishment (highlighted in or-
                                                                                        ange).
[80] Colin Percival. 2005. Cache Missing for Fun and Profit. In BSDCan.
[81] Basavesh Ammanaghatta Shivakumar, Jack Barnes, Gilles Barthe, Sunjay Cauligi,
     Chitchanok Chuengsatiansup, Daniel Genkin, Sioli O’Connell, Peter Schwabe,
                                                                                        B. Ethical Considerations
     Rui Qi Sim, and Yuval Yarom. 2023. Spectre Declassified: Reading from the Right    Our work targets defensive security: extracting protocol models
     Place at the Wrong Time. In 44th IEEE Symposium on Security and Privacy, SP
     2023, San Francisco, CA, USA, May 21-25, 2023. IEEE, 1753–1770. doi:10.1109/       from executables and analyzing them under explicit microarchitec-
     SP46215.2023.10179355                                                              tural leakage contracts.
[82] Basavesh Ammanaghatta Shivakumar, Gilles Barthe, Benjamin Grégoire, Vincent
     Laporte, Tiago Oliveira, Swarn Priya, Peter Schwabe, and Lucas Tabary-Maujean.        Human subjects and data. Our WhatsApp analysis reveals a side
     2023. Typing High-Speed Cryptography against Spectre v1. In 44th IEEE Sympo-       channel inferring the victim’s social graph, sensitive data whose
     sium on Security and Privacy, SP 2023, San Francisco, CA, USA, May 21-25, 2023.
     IEEE, 1094–1111. doi:10.1109/SP46215.2023.10179418                                 unauthorized inference breaches privacy. We conducted no human-
[83] Huzaifa Sidhpurwala. 2019. Security flaws caused by compiler optimizations.        subject research and collected no personal data; all experiments
     Red Hat Blog (2019).
[84] Laurent Simon, David Chisnall, and Ross Anderson. 2018. What you get is what
                                                                                        ran offline on software and hardware under our control.
     you C: Controlling side effects in mainstream C compilers. In 2018 IEEE European
     Symposium on Security and Privacy (EuroS&P). IEEE, 1–15.                              Responsible disclosure. We disclosed our findings to Meta with
[85] Eran Tromer, Dag Arne Osvik, and Adi Shamir. 2010. Efficient Cache Attacks on      reproduction instructions. Meta confirmed the vulnerabilities, but
     AES, and Countermeasures. J. Cryptol. 23, 2 (Jan. 2010), 37–71.                    we have no confirmation of a deployed fix.
[86] Yukiyasu Tsunoo, Teruo Saito, Tomoyasu Suzaki, and Maki Shigeri. 2003. Crypt-
     analysis of DES Implemented on Computers with Cache. In Proceedings of the            Authorization. We analyze only lawfully obtained software and
     Workshop on Cryptographic Hardware and Embedded Systems (CHES’03, LNCS).
     Springer, 62–76.                                                                   access no systems without authorization. Our reverse engineering
[87] Daniel Weber, Ahmad Ibrahim, Hamed Nemati, Michael Schwarz, and Christian          of WhatsApp Desktop may conflict with Meta’s license, but we
     Rossow. 2021. Osiris: Automated Discovery Of Microarchitectural Side Channels.
     In USENIX Security Symposium, Michael D. Bailey and Rachel Greenstadt (Eds.).
                                                                                        disclosed responsibly upon discovery.
     1415–1432.
[88] WhatsApp Inc. / Meta Platforms. Version 8 Updated August 19, 2024. WhatsApp           Societal impact. WhatsApp serves billions of users. By examin-
     Encryption Overview. Technical Report.                                             ing its binary, we close the gap between advertised guarantees and
                                                                                        real-world protections, exposing privacy risks such as social graph
A Appendix                                                                              inference that especially threaten journalists, activists, and users in
                                                                                        repressive environments. Publishing such analyses under respon-
A. Proof-of-Concept Implementation                                                      sible disclosure pressures vendors to fix subtle flaws and raises
To evaluate the feasibility of our attack in Section 4.2.4, we imple-                   accountability standards for deployed cryptographic systems.
mented a proof-of-concept targeting WhatsApp Desktop. It is based
on the Flush+Flush framework [49], modified for macOS, and is                           C. Open Science
available at Proof-of-Concept Implementation. Experiments ran on a
                                                                                        Our framework’s source code is available at [73]. Artifacts needed
2019 MacBook Pro with an Intel Core i7-9750H (6 cores, 2.6 GHz)
                                                                                        to evaluate our core contributions are linked below.
and 16 GB RAM, running macOS Sonoma 14.1.2.
   The attack leverages a Prime+Probe instruction cache side chan-                           • CryptoBap: https://github.com/FMSecure/CryptoBAP
nel to infer whether the victim initiates a new conversation, i.e.,                          • Tamarin (incl. Sapic+ ): https://tamarin-prover.com/
whether a secure session is being established. The adversary con-                            • ProVerif: https://bblanche.gitlabpages.inria.fr/proverif/
trols a co-resident user-space process scheduled on the same phys-                           • DeepSec: https://deepsec-prover.github.io/
ical core as the target. We assume the attacker knows the virtual                            • Ghidra: https://github.com/NationalSecurityAgency/ghidra
addresses of two functions in the WhatsApp binary: one initiating
a secure session, and another triggered when a one-time pre-key is
                                                                                        D. Use of Generative AI and LLMs
present (session_builder and OTPK_exists in Figure 8, respectively).                    This paper was refined for grammar, spelling, and minor style with
                                                                                        Grammarly.
