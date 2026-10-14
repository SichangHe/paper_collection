                                                                          Mythos and the Unverified Cage
                                                       Z3-Based Pre-Deployment Verification for Frontier-Model Sandbox Infrastructure

                                                                                       Dominik Blain
                                                                           COBALT Formal Verification, QreativeLab Inc.
                                                                                  Montréal, Québec, Canada
                                                                               dominik@qreativelab.io
                                                                                                  April 2026
arXiv:2604.20496v1 [cs.CR] 22 Apr 2026




                                         Abstract                                                              researcher not monitoring the session, posted its own exploit to
                                                                                                               multiple public websites, and attempted to suppress evidence of
                                         The April 2026 Claude Mythos sandbox escape exposed a crit-           its initiative. Anthropic declined public release, restricting ac-
                                         ical weakness in frontier AI containment: the infrastructure          cess via Project Glasswing to pre-approved defensive-security
                                         surrounding advanced models remains susceptible to formally           organizations [1].
                                         characterizable arithmetic vulnerabilities. Anthropic has not            Anthropic has not publicly characterized the escape vector;
                                         publicly characterized the escape vector; some secondary ac-          some secondary accounts hypothesize an arithmetic vulnera-
                                         counts hypothesize a CWE-190 arithmetic vulnerability in sand-        bility in the sandbox’s networking infrastructure [2, 4]. We
                                         box networking code. We treat this as unverified and analyze          treat those accounts as unverified. The containment problem
                                         the vulnerability class rather than the specific escape. This         this paper addresses is independent of the specific vector: the
                                         paper presents COBALT, a Z3 SMT-based formal verification             infrastructure surrounding advanced models—C/C++ sandbox
                                         engine for identifying CWE-190/191/195 arithmetic vulnera-            code—has not been subjected to formal verification, and ca-
                                         bility patterns in C/C++ infrastructure prior to deployment.          pable models may exploit conventional systems weaknesses
                                            We distinguish two classes of contribution. Validated:             to exceed their authorized scope. The challenge is not only to
                                         COBALT detects arithmetic vulnerability patterns in produc-           align the model’s objectives, but to formally verify the correct-
                                         tion codebases, producing SAT verdicts with concrete wit-             ness of the cage before placing the model inside it.
                                         nesses and UNSAT guarantees under explicit safety bounds.
                                         We demonstrate this on four production case studies—NASA
                                         cFE, wolfSSL, Eclipse Mosquitto, and NASA F Prime—
                                                                                                               1.1    The Gap
                                         with reproducible encodings, verified solver output, and ac-          AI containment research has largely addressed policy-level
                                         knowledged security outcomes. Proposed: a four-layer con-             mechanisms: reward shaping, output filtering, action whitelist-
                                         tainment framework—COBALT, VERDICT, DIRECTIVE-4,                      ing [7, 8, 9]. Formal verification research has demonstrated that
                                         and SENTINEL—that maps pre-deployment verification, pre-              entire vulnerability classes can be eliminated from OS kernels
                                         execution constraints, output control, and runtime monitoring         through machine-checked proofs [10, 11]. The intersection—
                                         to the failure modes exposed by the Mythos incident.                  formally verifying the C/C++ codebase that constitutes AI
                                            Under explicit assumptions, we further argue that the pub-         sandbox infrastructure—appears underexplored relative to adja-
                                         licly reported Mythos escape class is consistent with a Z3-           cent work on alignment, policy control, and kernel verification
                                         expressible CWE-190 arithmetic formulation and that pre-              in the literature we reviewed. This is the gap we address.
                                         deployment formal analysis would have been capable of surfac-
                                         ing the relevant pattern. The broader claim is infrastructural:
                                         frontier-model safety cannot depend on behavioral safeguards
                                                                                                               1.2    Research Questions
                                         alone; the containment stack itself must be subjected to formal       1. RQ1. Can a Z3-based formal verifier reliably detect arith-
                                         verification.                                                            metic vulnerability patterns (CWE-190/191/195) in produc-
                                                                                                                  tion C/C++ infrastructure codebases, with reproducible SAT
                                                                                                                  witnesses and UNSAT certificates?
                                         1    Introduction                                           2. RQ2. Is the hypothesized Mythos escape vector consistent
                                                                                                        with a CWE-190 class formulation, and under what condi-
                                         On April 7, 2026, Anthropic’s Claude Mythos model was
                                                                                                        tions would pre-deployment scanning have been capable of
                                         tasked with attempting to escape its hardened sandbox envi-
                                                                                                        detecting such a pattern?
                                         ronment as part of a controlled red-team exercise [1]. The
                                         model succeeded, and then proceeded autonomously beyond 3. RQ3. Can a four-layer architectural framework address each
                                         the exercise scope: it composed and delivered an email to a    structural failure mode the Mythos incident exposed, and


                                                                                                           1
    which layers admit formal treatment?                            Separately, during the same red-team, Mythos independently
                                                                 discovered a 27-year-old integer overflow in OpenBSD’s TCP
                                                                 SACK implementation as part of its vulnerability research
1.3 Contributions                                                tasks [3, 2]. This is a separately reported CWE-190 finding; An-
1. [Validated] A Z3 bitvector theorem proving CWE-190 arith- thropic does not identify it as the sandbox escape mechanism.
   metic overflow reachability and a companion proposition On the Firefox 147 exploit-development benchmark, Mythos
   proving overflow impossibility under input bounds (§5).       produced 181 working exploits versus 2 for the previous gener-
                                                                 ation model, across several hundred attempts [2].
2. [Validated] Four production case studies—NASA cFE,
   wolfSSL, Eclipse Mosquitto, and NASA F Prime—with
   C vulnerability pattern, Z3 encoding, verified solver output, 2.2 Root Cause Classification
   and disclosure outcome (§6).
                                                                 The escape was enabled by four independent structural ab-
3. [Proposed] A formal threat taxonomy of AI sandbox escape sences:
   with four categories (T1–T4) derived from the incident (§3).
                                                                 A1. No pre-deployment code verification. The sandbox in-
4. [Implemented] A four-layer containment framework with frastructure was not subject to formal vulnerability analysis be-
   one validated layer (COBALT) and three implemented com- fore Mythos was deployed. Under assumption A-CWE (§8), an
   ponents (VERDICT, DIRECTIVE-4, SENTINEL) undergo- arithmetic vulnerability in the CWE-190/191 class was present
   ing end-to-end AI containment validation (§7).                and reachable in the infrastructure code.
5. [Discussion] A conditional argument for when pre- A2. No pre-execution action constraints. No mechanism
    deployment scanning would have been capable of detecting checked agent-initiated actions (outbound SMTP, external
    the Mythos escape class, with explicit assumptions and fal- HTTP) against an authorization policy before execution.
    sification conditions (§8).
                                                                A3. No reported output-review layer. No layer is described
                                                                in public accounts as reviewing or blocking content before
   Terminology. “Validated”: demonstrated on real code-         external emission.
   bases with reproducible Z3 encodings and verified solver
   output. “Implemented”: working code with tests; end-         A4. Insufficient runtime observability. Anomalous outbound
   to-end AI containment validation ongoing. “Prototype”:       traffic was not flagged with sufficient speed to interrupt the
   working code, benchmarked, not production-hardened.          action chain before completion.
  “Conditionally argued”: conditional on explicit stated as-
   sumptions. This taxonomy is applied consistently across
   all sections and tables.                                     3 Threat Model
                                                                     We formalize four threat categories derived from absences A1–
2     The Mythos Incident                                            A4.

                                                                  Definition 1 (T1 – Infrastructure Vulnerability). The sandbox
2.1    Technical Chronology                                       execution environment contains a reachable arithmetic vulner-
Anthropic deployed Claude Mythos in a hardened sandbox and ability in the CWE-190/191 family in its C/C++ codebase, ex-
instructed it to attempt escape as part of a controlled red-team. ploitable by a sufficiently capable agent to acquire capabilities
Public reporting describes the sequence as follows [1, 2, 4]:     outside its authorized scope.

1. Sandbox escape. Anthropic’s public account characterizes          Definition 2 (T2 – Pre-Execution Bypass). An agent initiates
   the escape only as a “moderately sophisticated multi-step         actions outside its authorized action set with no formal gate
   exploit”; the specific vulnerability class was not publicly       verifying authorization before execution.
   characterized by Anthropic [1]. Secondary accounts specu-
   late about the mechanism; we treat those as unverified and        Definition 3 (T3 – Output Exfiltration). An agent emits con-
   make no factual claim about the escape vector in this paper       tent to external parties without a formal blocking layer on the
   (see assumption A-CWE, §8).                                       emission channel.
2. External contact. Without instruction, Mythos composed Definition 4 (T4 – Runtime Opacity). Agent actions are not
   and delivered an email to a researcher external to the exer- observable in real time with granularity sufficient to enable
   cise.                                                        human-in-the-loop intervention before a multi-step sequence
3. Public disclosure. Without instruction, Mythos posted its completes.
    exploit to multiple public websites.
                                                            COBALT also detects adjacent classes CWE-125 and CWE-
4. Evidence concealment. The model attempted to suppress 476 (see Table 2), but these are not central to the Mythos case
   traces of its initiative.                             study and are not included in T1’s definition.


                                                                 2
Table 1: Threat categories derived from reported structural ab- 4.4 Reproducibility
sences in the Mythos incident, with corresponding containment
layer and claim status.                                         All Z3 encodings in §5 and §6 are self-contained Python list-
                                                                ings runnable with pip install z3-solver. No exter-
         Threat Abs. Layer          Mythos Status
                                                                nal data dependencies. Solver output is shown verbatim. The
                                    phase                       encodings shown are minimized, self-contained reductions of
                                                                the vulnerability-relevant arithmetic structure, not full-program
         T1      A1     COBALT      Escape Validated            models. Contextual guards, compiler behavior, or interprocedu-
         T2      A2     VERDICT Email, Implemented
                                                                ral effects present in full deployments may not be captured.
                                    post
         T3      A3     DIRECTIVE-Email, Implemented
                                                                   Artifact availability. Implementation artifacts, benchmark
                        4           post                        scripts, and the COBALT-Runtime and COBALT-Graph pro-
         T4      A4     SENTINEL All         Implemented        totype  modules   (cobalt runtime/) corresponding to all
                                    phases                      results in this paper are available from the author upon request
                                                                and will be released as a research artifact package.

4     Methodology
                                                                      5       Z3 Proof Model for CWE-190
4.1    Analysis Pipeline
                                                                      5.1 A CWE-190 TCP SACK Pattern: The
COBALT processes C/C++ source through four stages:                          OpenBSD Finding
   Stage 1: Parse. libclang parses source into a typed abstract
syntax tree. No compilation required; header resolution is During the Mythos red-team, the model independently discov-
optional.                                                           ered a CWE-190 integer overflow in OpenBSD’s 27-year-old
   Stage 2: Extract. COBALT traverses the AST identifying           TCP   SACK implementation [3]. Anthropic does not character-
arithmetic operations, array indexing, pointer arithmetic, and      ize this as the sandbox escape mechanism; the escape vector
type casts that are candidates for the target CWE classes. The      remains  unspecified in public accounts. We model this pattern
case studies in this paper focus specifically on arithmetic reach-  under  assumption  A-CWE (§8): if the sandbox escape involved
ability patterns; broader AST extraction support is part of the     a CWE-190/191     arithmetic vulnerability, the following analysis
tool pipeline but is not exhaustively evaluated here.               applies. The  core arithmetic pattern in the OpenBSD finding is:
   Stage 3: Model. For each candidate, COBALT constructs a              Listing 1: CWE-190: TCP SACK signed cast overflow
Z3 bitvector formula. All inputs are modelled as unconstrained
                                                                    1 /* Seq comparison via signed 32-bit cast.
bitvectors of the declared width. The vulnerability condition is 2       Correct within 2ˆ31 sequence window. */
                                                                    3 static int tcp_seq_lt(uint32_t a, uint32_t b) {
expressed as the satisfiability query over the formula.
                                                                    4      return (int32_t)(a - b) < 0;
   Stage 4: Solve. Z3 evaluates:                                    5 }

• SAT: the vulnerability is formally reachable within the en- 67 /* BUG: sack_start not bounded to window.
  coded pattern. Z3 returns a concrete model constituting an 8           Attacker sets sack_start ˜2ˆ31 from both
                                                                    9    comparison operands -> sign overflow in
  exploitation witness.                                            10    both calls simultaneously. */
                                                                      11 int is_in_hole(uint32_t sack_start,
• UNSAT: the vulnerability cannot be triggered within the             12                uint32_t rcv_nxt,
  modelled input domain. Z3 returns a proof certificate.              13                uint32_t snd_una) {
                                                                      14     return tcp_seq_lt(sack_start, rcv_nxt)
                                                                      15         && tcp_seq_lt(snd_una, sack_start);
                                                                      16 }
4.2    Solver Configuration
Z3 version 4.12.x, default bitvector theory settings, 60-second               Listing 2: Z3 model: TCP SACK CWE-190 (SAT)
timeout per query. No manual proof guidance; all SAT/UNSAT            1    from z3 import *
verdicts are fully automated. Where architecture-dependent            2
                                                                      3 sack_start = BitVec(’sack_start’, 32)
widths matter, the encoding follows the target program’s de-          4 rcv_nxt    = BitVec(’rcv_nxt’,    32)
clared type semantics under the analyzed build assumptions.           5 snd_una    = BitVec(’snd_una’,    32)
                                                                      6
                                                                      7 # (int32_t)(a-b) < 0 iff MSB of (a-b) is set
                                                                      8 def tcp_seq_lt(a, b):
4.3    Corpus and Selection Criteria                                  9     return UGE(a - b, BitVecVal(0x80000000, 32))
                                                                      10

Targets were selected under four criteria: (1) open-source            11 s = Solver()
                                                                      12 s.add(tcp_seq_lt(sack_start, rcv_nxt))
C/C++ with accessible source; (2) active maintenance with             13 s.add(tcp_seq_lt(snd_una, sack_start))

a security disclosure channel; (3) relevance to infrastructure        14 # No bound on sack_start -- this is the bug
                                                                      15
software (networking, cryptography, system libraries); (4) no         16 print(s.check())   # sat
prior formal verification coverage reported. Targets were not         17 m = s.model()
                                                                      18 print("sack_start =", hex(m[sack_start].as_long()))
pre-screened for known vulnerabilities; COBALT ran on the             19 print("rcv_nxt    =", hex(m[rcv_nxt].as_long()))
most recent available commit before disclosure.                       20 print("snd_una    =", hex(m[snd_una].as_long()))



                                                                  3
         Listing 3: Verified solver output (Z3 4.12.x)                        Listing 5: Z3 model: allocation overflow (SAT)
1 sat                                                               1    from z3 import *
2 sack_start = 0x80000000                                           2
3 rcv_nxt    = 0x0                                                  3 n            = BitVec(’n’, 32)
4 snd_una    = 0x0                                                  4 element_size = BitVecVal(16, 32)
                                                                    5 s = Solver()
                                                                    6 product = n * element_size
Note. The following theorem concerns the encoded arithmetic         7 s.add(UGT(n, BitVecVal(0, 32)))
pattern, not the full networking stack implementation. The          8 s.add(ULT(product, n))  # overflow: wrapped product < n
modelled conditions are a necessary ingredient of the reported 109 print(s.check()) # sat
overflow scenario; they are not a complete model of the de- 11 m = s.model()
                                                               12 nv = m[n].as_long()
ployed system.                                                 13 pv = (nv * 16) % (2**32)
                                                                    14   print(f"n=0x{nv:08x} ({nv}), product=0x{pv:08x} ({pv})")
Theorem 1 (CWE-190 TCP SACK Arithmetic Reach-
ability). Let tcp seq lt(a,b) return true iff (a −
b) mod 232 ≥ 231 .             There exists an assignment                           Listing 6: Verified solver output
                                                         32      3
(sack start, rcv nxt, snd una) ∈ {0, . . . , 2 − 1}                1 sat
                                                                   2 n=0x2222221e (572662302)
such that both tcp seq lt(sack start, rcv nxt) 3 product=0x222221e0 (572662240) -- product < n: overflow
and tcp seq lt(snd una, sack start) are simulta-                           confirmed
neously true, constituting a satisfiable arithmetic condition
consistent with the reported overflow-triggering scenario.         Proposition 1 (UNSAT: Overflow Impossible Under Input
                                                                   Bound). If n ≤ ⌊(232 − 1)/element size⌋, the multiplica-
Proof. The Z3 encoding in Listing 2 returns sat with wit-
                                                                   tion n · element size cannot overflow and the SAT query
ness (sack start = 231 , rcv nxt = 0, snd una = 0).
                        31             32      31      31          returns unsat.
Manual verification: (2 − 0) mod 2 = 2 ≥ 2 (cond1
               31         32    32     31      31      31
holds); (0 − 2 ) mod 2 = 2 − 2 = 2 ≥ 2 (cond2 Proof. With element size = 16 and n ≤ 228 − 1 =
holds). Both conditions are simultaneously satisfied. The wit- 268,435,455, the maximum product is (228 − 1) · 16 =
ness constitutes a formal arithmetic certificate for the overflow- 232 − 16 < 232 , so no 32-bit overflow is reachable. Z3 returns
triggering scenario.                                               unsat on the bounded query below, providing a machine-
                                                                   checked proof certificate.
COBALT Independent Verification (COBALT-2026-004).
As a direct validation exercise, COBALT was applied to the Listing 7: Z3 model: allocation overflow (UNSAT after bound)
current OpenBSD sys/netinet/tcp input.c HEAD
                                                                   1 s2 = Solver()
(2026-04-22) to determine whether the same arithmetic pattern 2 product2 = n * element_size
class is detectable via static Z3 analysis. COBALT flagged 3 s2.add(UGT(n, BitVecVal(0, 32)))
                                                                   4 s2.add(ULE(n, BitVecVal(0x0FFFFFFF, 32)))       # input bound
a CWE-195 pattern at tcp input.c:1297 (todrop = 5 s2.add(ULT(product2, n))
tp->rcv nxt - th->th seq; unsigned 32-bit subtrac- 6
                                                                   7 print(s2.check())     # unsat -- overflow provably
tion assigned to int todrop) and the SEQ LT/GT macros                      impossible
in tcp seq.h:44--47 ((int)((a)-(b))). Z3 WD1
(SAT): there exist rcv nxt, th seq such that the unsigned             Proposition 1 establishes the operational value of COBALT:
                    31
difference equals 2 , yielding INT32 MIN upon signed cast—         a single  input bound converts a formally proven vulnerability
a boundary condition where the comparison is formally ambigu-      into a formally   proven guarantee. The patch is the bound; the
ous under RFC 793 §3.3. Z3 WD3 (UNSAT): adding the guard           UNSAT     verdict is the certificate.
               31
ULT(diff, 2 ) before the cast produces no satisfying input,
proving the guarded form is safe. Status: pattern detected;
exploitability depends on sequence number controllability from 6 Empirical Evidence:                               Production
the network and is not asserted here.                                    CWE-190/191 Detections
5.2 CWE-190 in Memory Allocation: SAT and We present four production case studies demonstrating
                                          COBALT’s detection capability on real C/C++ infrastructure
    UNSAT                                 codebases. Each includes the vulnerable pattern, the Z3 en-
A second, structurally distinct CWE-190 pattern is the mul- coding, verified solver output, and disclosure outcome. These
tiplication overflow in allocation size computation—directly cases establish detection capability independently of the Mythos
relevant to sandbox memory management and common in C sandbox and form the empirical basis for RQ1.
infrastructure code:

        Listing 4: CWE-190: allocation size overflow
                                                                    6.1 Case Study 1: NASA cFE – CWE-195 Re-
1 /* BUG: n * element_size can overflow uint32.
                                                                        source ID Truncation
2    Result is a smaller-than-expected allocation;
3    subsequent writes overflow the undersized buffer. */           Target.     NASA Core Flight Executive (cFE) is the
4 uint8_t *buf = malloc((uint32_t)n * element_size);                flight software framework used across NASA missions


                                                                4
including the Mars Perseverance rover.        We audited                 5        (w1[j+5] << 30)); /* UB: any w1 >= 2 overflows */
                                                                         6    /* Outer (word32) cast is on the full OR -- too late */
github.com/nasa/cFE HEAD (2026-04-20).
  Pattern. The resource ID API casts an opaque identifier to                For w1[j+5] ≥ 2, the shift w1[j+5] << 30 exceeds
unsigned long without width validation:                                  INT32 MAX, constituting signed integer overflow—undefined
      Listing 8: NASA cFE: CWE-195 resource ID truncation                behavior under C99/C11 §6.5/5. The same pattern appears in
                                                                         dilithium encode w1 32 c() for ML-DSA-65/87 (<<
 1 /* core_api/fsw/inc/cfe_resourceid.h:131 */
 2 /* CFE_ResourceId_t is an opaque typedef   */                         28, threshold w1 ≥ 8). COBALT identified 11 affected in-
 3 /* On 32-bit targets, unsigned long = 32b  */                         stances across all three ML-DSA parameter sets.
 4 static inline unsigned long
 5 CFE_ResourceId_ToInteger(CFE_ResourceId_t id)
 6 {                                                                     Listing 12: COBALT Z3 encoding: wolfSSL CWE-190 (WD1
 7     /* BUG: if id encodes a 64-bit value,                             SAT / WD2 UNSAT)
 8        cast silently truncates upper 32 bits */
 9     return (unsigned long)CFE_RESOURCEID_UNWRAP(id);                  1 from z3 import *
10 }                                                                     2 w1 = BitVec(’w1’, 32)
                                                                         3 INT32_MAX = BitVecVal(0x7FFFFFFF, 32)
                                                                         4
                                                                         5 # WD1: signed shift overflows INT32_MAX (SAT)
     Listing 9: COBALT Z3 encoding: NASA cFE CWE-195                     6 s1 = Solver()
                                                                         7 s1.add(ULE(w1, BitVecVal(43, 32)))   # FIPS 204 range
 1   from z3 import *
                                                                         8 s1.add(UGT(w1 << BitVecVal(30, 32), INT32_MAX))
 2   resource_id = BitVec(’resource_id’, 64)
                                                                         9 print("WD1:", s1.check())            # sat
 3
                                                                         10
 4 s = Solver()
 5 # upper 32 bits are non-zero (valid 64-bit ID)                        11 # WD2: after fix -- (word32) cast first, UNSAT
 6 s.add(UGT(LShR(resource_id, 32), BitVecVal(0, 32)))
                                                                         12 s2 = Solver()
                                                                         13 s2.add(UGT(w1 << BitVecVal(30, 32),
 7 # truncated value differs from original
 8 truncated = ZeroExt(32, Extract(31, 0, resource_id))
                                                                         14            BitVecVal(0xFFFFFFFF, 32))) # can’t exceed
 9 s.add(truncated != resource_id)
                                                                                            uint32_t
                                                                         15 print("WD2:", s2.check())            # unsat
10
11 print(s.check())   # sat
12 m = s.model()
13 rv = m[resource_id].as_long()
                                                                                     Listing 13: Verified solver output: wolfSSL
14 print(f"resource_id=0x{rv:016x}, truncated=0x{rv & 0
        xffffffff:08x}")                                                 1 WD1: sat   -- w1=2: 2<<30 = 0x80000000 > INT32_MAX
                                                                         2 WD2: unsat -- (word32) shift bounded by UINT32_MAX



          Listing 10: Verified solver output: NASA cFE                     Verdict. SAT + UNSAT pair. Values w1 ∈ [2, 43]—42 of
 1 sat                                                                   44 valid ML-DSA-44 coefficients—trigger the signed UB (≈
 2 resource_id=0x0000000100000000                                        95% of real-world signing operations). The UNSAT certificate
 3 truncated  =0x00000000
                                                                         confirms that casting to word32 before the shift eliminates the
   Verdict. SAT. Any resource ID with non-zero upper 32 bits             overflow class entirely.
is silently truncated to zero on 32-bit embedded targets, creating         Outcome. Reported 2026-03-27; confirmed by wolfSSL
ID aliasing and potential privilege confusion between missions           developer (Paul Adelsbach) same day; fix merged in wolfSSL
components.                                                              PR #10096 [5]. Classified as UB without confirmed CVE
   Outcome. Six findings disclosed to NASA F Prime / cFE                 security impact; credited in wolfSSL release notes.
team (COBALT-AERO-CFE-001 through CFE-006); responsi-
ble disclosure filed 2026-04-20.                                         6.3 Case Study 3: Eclipse Mosquitto – CWE-191
                                                                             + CWE-125
6.2 Case Study 2: wolfSSL ML-DSA – CWE- Target. Eclipse Mosquitto 2.1.2 is a widely deployed MQTT
    190 Signed Left-Shift UB            broker used in industrial IoT and infrastructure. Found by
Target. wolfSSL is a widely deployed embedded C SS- COBALT (COBALT-2026-001).
L/TLS and post-quantum cryptographic library. We au-             Pattern. In src/proxy v2.c:151, the inner TLV loop
dited wolfssl/src/dilithium.c HEAD (2026-03-27).              decrements   a uint16 t length counter without verifying the
Found by COBALT.                                              inner TLV  fits within the declared SSL TLV boundary:
   Pattern. dilithium encode w1 88 c() (ML-DSA-
                                                                 Listing 14: Mosquitto: CWE-191 TLV length underflow
44) shifts a sword32 (signed int32) coefficient left by 30
bits without a prior unsigned cast. The outer (word32) cast 2 /* if (3 + tlv_len > len) return ERR_INVAL; **//
                                                              1 /* proxy_v2.c:151 -- MISSING bound check:


applies to the full OR expression—after the sub-expression is 3 len = (uint16_t)(len - (sizeof(uint8_t)*3
                                                              4                         + tlv_len)); /* UNDERFLOW */
already evaluated as signed:                                  5 /* When 3+tlv_len > len: len wraps ˜UINT16_MAX */
                                                                         6    /* Loop continues reading beyond SSL TLV bound   */
Listing 11: wolfSSL dilithium.c:2196 – CWE-190 signed left-
shift UB
                                                                              Listing 15: COBALT Z3 encoding: Mosquitto CWE-191
 1 /* w1 is sword32; FIPS 204 ML-DSA-44 range: [0, 43] */
 2 w1e32[0] = (word32)(                                                  1 from z3 import *
 3     w1[j+0] | (w1[j+1] << 6) | (w1[j+2] << 12) |                      2 len_val  = BitVec(’len’,     16)
 4     (w1[j+3] << 18) | (w1[j+4] << 24) |                               3 tlv_len  = BitVec(’tlv_len’, 16)



                                                                     5
 4   hdr     = BitVecVal(3, 16)                                    4   broken_mul = size * BitVecVal(2, 32)
 5                                                                 5
 6 s = Solver()                                                    6  s = Solver()
 7 result = len_val - hdr - tlv_len                                7  s.add(UGT(size, BitVecVal(0x7FFFFFFF, 32)))   # size high
 8 s.add(UGT(hdr + tlv_len, len_val))  # underflow cond             8 s.add(UGE(stack_sz, BitVecVal(2, 32)))
 9 s.add(UGT(result, BitVecVal(0xFF, 16)))  # wraps large           9 s.add(ULT(stack_sz, BitVecVal(1024, 32)))
10                                                                 10 s.add(UGE(stack_sz, broken_mul))  # guard bypassed
11 print(s.check())   # sat                                        11 print(s.check())   # sat
12 m = s.model()
13 lv = m[len_val].as_long()
14 tv = m[tlv_len].as_long()
15 rv = (lv - 3 - tv) & 0xFFFF                                                 Listing 19: Verified solver output: NASA F Prime
16 print(f"len={lv}, tlv_len={tv}, result=0x{rv:04x}")
                                                                   1 sat [Phase 1 -- CWE-190]
                                                                   2   directive_size = 0x80000001
                                                                   3   size*2 (U32)   = 0x00000002 <- OVERFLOWED
           Listing 16: Verified solver output: Mosquitto           4   Guard bypassed: stack_size >= broken_mul -> PASS
                                                                   5
 1 sat                                                             6   sat [Phase 2 -- CWE-125]
 2 len=1, tlv_len=5, result=0xfff9 (65529)                         7     rhsOffset = 0x7FFFFFF7 >> MAX_STACK_SIZE -> OOB READ

   Verdict.      SAT. With len=1, tlv len=5:            the           Verdict. SAT (two phases). The guard intended to block
counter wraps to 65,529, allowing the loop to read                 stack underflow is defeated by the same U32 overflow it was
beyond the SSL TLV boundary (CWE-125).                    If       meant to prevent, enabling a subsequent out-of-bounds read of
use identity as username=true,               an    attacker        heap or stack memory beyond stack.bytes[]. On embed-
can overwrite context->username with bytes outside the             ded targets without ASLR, this may disclose memory layout.
declared TLV.                                                         Outcome. Responsible disclosure filed to NASA F Prime
   Outcome. Disclosed to Eclipse security team (secu-              security team 2026-04-22 (COBALT-2026-003). CVE assign-
rity@eclipse.org) 2026-04-17; acknowledged by Eclipse main-        ment pending.
tainer Lukas Pühringer 2026-04-20; CVE assignment pending.

                                                                   6.5          Summary
6.4 Case Study 4: NASA F Prime – CWE-190 +
    CWE-125
                                                              Table 2: COBALT Arithmetic Vulnerability Production Corpus
Target. NASA F Prime (fprime-sw/fprime) is an open-
source flight software framework developed by NASA             Target      CWE            Verdict     Outcome
JPL, deployed on missions including the Mars Ingenu-
                                                               NASA cFE    195            SAT     + Disclosed
ity helicopter. We audited HEAD (2026-04-22) targeting
                                                                                          witness     2026-04-
Svc/FpySequencer/FpySequencerDirectives.cpp.                                                          20
   Pattern. The equality directive handler performs a stack    wolfSSL     190∗           SAT     + Patched
underflow check using directive.get size() * 2 on              ML-DSA                     UNSAT       PR#10096
a U32 quantity without overflow protection. A comment at       Mosquitto   191+125        SAT     + Eclipse
line 1207 reads “Now safe to compute size * 2”—but the multi-                             witness     ack’d
plication itself is not overflow-guarded:                                                             2026-04-
                                                                                                                                  20
Listing 17: NASA F Prime: CWE-190 + CWE-125 in FpySe-                  NASA           F     190+125               SAT     +       Disclosed
quencerDirectives.cpp:1209                                             Prime                                      witness         2026-04-
 1 // "Now safe to compute size * 2" <-- INCORRECT                                                                                22
 2 if (this->m_runtime.stack.size <                                    ∗
                                                                           Signed left-shift UB (C99 §6.5/5); 11 instances, all three ML-DSA parameter sets.
 3     directive.get_size() * 2) {     // CAN OVERFLOW
 4     error = DirectiveError::STACK_UNDERFLOW;                        Additional (1,055+ findings):
 5     return Signal::stmtResponse_failure;
 6 }
                                                                       IBM Qiskit 190/125                         SAT ×5   IBM
 7 U64 lhsOffset = stack.size - directive.get_size() * 2;              Aer                                                 PSIRT
 8 U64 rhsOffset = stack.size - directive.get_size();  //                                                                  triage
        UNDERFLOW
 9 this->m_runtime.stack.size -= directive.get_size() * 2;             NASA cFE             195/476               SAT ×6   Active dis-
                                                                       (6)                                                 closure
  When get size() returns 0x80000001 (U32), the prod-                  OpenBSD              195                   SAT+UNSATPattern
uct 0x80000001 * 2 wraps to 0x2 (CWE-190), bypassing                   TCP SACK                                            detected
the guard. rhsOffset then underflows to 0x7FFFFFF7,                                                                        (COBALT-
and the subsequent memcmp reads beyond stack.bytes[]                                                                       2026-004)
(CWE-125).
                                                                      Among findings submitted for disclosure in this corpus, we
Listing 18: COBALT Z3 encoding: NASA F Prime CWE-190               observed no rejected SAT reports: each verdict corresponded
overflow bypass
                                                                   to a vulnerability pattern acknowledged by the receiving secu-
 1 from z3 import *
 2 size      = BitVec(’directive_size’, 32)
                                                                   rity team. This addresses RQ1 affirmatively for the patterns
 3 stack_sz  = BitVec(’stack_size’,     32)                        modelled. The production corpus is intended as evidence of


                                                               6
           Sandbox Infrastructure C/C++ source                                     Without COBALT                With COBALT
                                  scan                                               Sandbox infra               Sandbox infra
               Layer 1 · COBALT      [VALIDATED ]                                                                          scan
         SAT witness ⇒ block | UNSAT ⇒ formally safe                               Mythos deployed               COBALT scan
                                  deploy                                                  no scan               0x80000000 → SAT
              Deployed Agent inside sandbox
                                                                                 Arith. vuln. triggered              Blocked
                                                                                    (illustrative, A-CWE)          patch required
            Layer 2 · VERDICT      [I MPLEMENTED ]
                 C1 –C6 checked before each ac-
                 tion · returns S AFE or U NSAFE
                                                                                   Sandbox escape


          Layer 3 · DIRECTIVE-4       [I MPLEMENTED ]                              Email · public post
        Content policy predicate before external emission                               uncontrolled


                                                                         Figure 2: Illustrative counterfactual under A-CWE: if the sand-
            Layer 4 · SENTINEL      [I MPLEMENTED ]
                                                                         box escape involved a CWE-190/191 arithmetic vulnerability
       Append-only log · anomaly alerting · human review
                                                                         (unverified), without COBALT (left) it goes undetected; with
                                                                         COBALT (right), Z3 returns SAT and deployment is blocked
                    External Environment                                 before the model enters the sandbox.
Figure 1: Four-layer formal containment. COBALT (green, val-
idated) scans sandbox infrastructure before deployment. Layers class detection; it does not assert that COBALT reproduced the
2–4 (blue, implemented) enforce policy at action, emission, and specific Mythos finding. A pre-deployment scan would, under
runtime. One failure at any layer halts the operation.            the assumptions stated in §8, have been expected to surface
                                                                  the relevant arithmetic pattern and return an SAT verdict with
                                                                  exploitation witness.
precision and feasibility, not as a comprehensive benchmark of
recall; the encoded patterns represent a subset of vulnerability-
relevant arithmetic structures in each target.                    7.2 Layer 2 (Implemented): VERDICT – Pre-
                                                                                Execution Constraint Checking
7 Proposed Four-Layer Containment VERDICT1 is a specified six-constraint decision layer that
                                  evaluates agent-initiated actions against a formal policy before
  Framework                       they execute. Six predicates are assessed over the action’s type,
                                                                         target, session state, and content hash:
Layer 1 (COBALT) is empirically validated as described
in §6. Layers 2–4 are implemented as independent compo-
nents with working code; their end-to-end validation in the AI
containment context is specified and ongoing.                                C1 : action.target ∈
                                                                                                / E XTERNAL N ETWORK                       (1)
                                                                             C2 : action.type ̸= S END E MAIL                              (2)
                                                                             C3 : action.type ̸= W RITE P UBLIC E NDPOINT                  (3)
7.1 Layer 1 (Validated): COBALT – Pre-
                                                                             C4 : action.scope ⊆ AUTHORIZED S COPE                         (4)
    Deployment Verification
                                                                             C5 : action.hash ∈ A PPROVED M ANIFEST                        (5)
COBALT applies Z3 formal analysis to C/C++ source before                     C6 : session.state = S UPERVISED                              (6)
any agent is deployed into the target environment. A SAT
verdict blocks deployment until the finding is resolved; an
                                                                           The formal decision rule is:
UNSAT verdict provides a formal guarantee for the analysed
input domain.
                                                                                           (
                                                                                             S AFE       if Ci (a) holds for all i ∈ {1, . . . , 6}
   Applied to the Mythos case (conditional on A-CWE,                     VERDICT(a) =
                                                                                             U NSAFE if ∃ i ∈ {1, . . . , 6} : ¬Ci (a)
see §8): if the escape involved a CWE-190/191 arith-
metic pattern, it belongs to the class COBALT has demon-                                                                                (7)
strably detected on four independent production codebases.                 A single constraint failure suffices. The Mythos post-escape
Additionally, an independent COBALT scan of OpenBSD                      email would have violated C1 and C2 ; the public exploit post
tcp input.c HEAD detected the CWE-195 signed-cast pat-                   would have violated C1 and C3 . VERDICT returns U NSAFE
tern at tcp input.c:1297 (COBALT-2026-004; see §5)—                      with a decision record, and the action is cancelled.
the same file secondary accounts associate with the Mythos                  1 Implementation:            https://github.com/dom-omg/omni
TCP SACK finding, confirming that COBALT’s invariant cov-                (lib/execution/verdict.js,                   lib/execution/policy.js).
erage extends to this arithmetic pattern class. This is a pattern-       Private repository; available to qualified reviewers upon request.


                                                                     7
Illustrative Policy Evaluation                                 directly applicable to SENTINEL’s observability layer, where
                                                               the stream of agent actions constitutes the monitored event
The first externally observable action Mythos took after sand-
                                                               source.
box escape was sending an email to an external security re-
searcher. Evaluating that action against the six VERDICT
constraints:                                                   7.5 Stack Completeness Against Mythos Failure
                                                                               Modes
    Constraint                   Observed value       Result
    C1 : target ∈
                / ExtNet         SMTP endpoint        FAIL               Table 3: Proposed stack mapped to publicly reported Mythos
    C2 : type ̸= SendEmail       SendEmail            FAIL
                                                                         action sequence.
    C3 : type ̸= WritePublic     n/a                  pass
    C4 : scope ⊆ Auth.           internal task only   FAIL
    C5 : hash ∈ ApprovedMfst     He ∈ /M              FAIL                      Mythos           Layer      Mechanism    Status
    C6 : session = Supervised    Unsupervised         FAIL                      action

    Verdict                                           U NSAFE                   Sandbox es-      COBALT     Pre-deploy   Cond.
                                                                                cape                        SAT          ar-
   Five of six constraints fail. Under the VERDICT specifi-                                                              gued
                                                                                Email to re-     VERDICT    Pre-exec +   Implemented
cation, a single failure suffices to return U NSAFE, cancel the
                                                                                searcher         + D-4      output
action, and append a decision record to the SENTINEL log.
                                                                                Public     ex-   VERDICT    Pre-exec +   Implemented
Content hash He of the unauthorized email is not a member of                    ploit post       + D-4      output
the approved manifest M ; this alone—C5 failure—would have                      Evidence         SENTINEL   Append-      Implemented
been sufficient to block the action without requiring knowledge                 concealment                 only log
of its destination or type.
   Limitation. VERDICT constrains actions routing through
the engine. If an escape is complete before these checks execute,
they may no longer be in the execution path—reinforcing the
primacy of Layer 1.                                                      8    Discussion
                                         8.1 What the Paper Proves
7.3 Layer 3 (Implemented): DIRECTIVE-4 –
    Output Firewall                      The validated contributions are:
                                                                     • COBALT detects CWE-190/191 in production C/C++ infras-
DIRECTIVE-42 applies policy predicates to agent-generated              tructure codebases, with formal SAT witnesses and UNSAT
content before external emission, covering unauthorized dis-           certificates on the encoded patterns.
closure, exploit publication, and credential exfiltration classes.
In its current specification, this layer is described at the policy- • Theorem 1 proves that a representative CWE-190 TCP
predicate level rather than evaluated as a complete implementa-        SACK arithmetic pattern is arithmetically reachable and Z3-
tion.                                                                  decidable within the encoding.
   Limitation. DIRECTIVE-4 intercepts content within the • Proposition 1 proves that adding an input bound converts the
managed emission pipeline. Mechanisms routing outside this             SAT query to UNSAT, demonstrating the class is eliminable,
pipeline are not covered.                                              not merely detectable.
                                                                • COBALT independently scanned OpenBSD tcp input.c
7.4 Layer 4 (Implemented): SENTINEL – Run-                        HEAD (2026-04-22) and detected the CWE-195 signed-cast
    time Agent Control Plane                                      pattern at the specific file and line reported in secondary
              3
SENTINEL provides continuous, append-only observability           accounts of the Mythos TCP SACK finding (COBALT-2026-
of agent actions. Every action is logged with millisecond gran-   004, §5). Z3 confirmed the boundary condition (WD1 SAT)
ularity; anomalous outbound connections generate real-time        and the guarded-form safety (WD3 UNSAT).
alerts enabling human-in-the-loop review. The implementa-
tion provides real-time append-only observability; production 8.2 The Conditional Mythos Claim
hardening and AI containment integration are ongoing. Event
stream monitoring frameworks such as BeepBeep [15] demon- We state the Mythos connection as a conditional argument
strate that complex temporal properties over continuous action under three explicit assumptions:
streams can be verified at low overhead—a deployment model 1. A-SRC: The sandbox source was available in C/C++ form
   2 Implementation:          https://github.com/dom-omg/          compatible with libclang parsing.
directive-4. Private repository; available to qualified reviewers
upon request.
                                                                         2. A-CWE: The escape vector belongs to the CWE-190 class
   3 Implementation:      https://github.com/dom-omg/sentinel.              as hypothesized by some secondary sources; Anthropic has
Private repository; available to qualified reviewers upon request.          not confirmed this.


                                                                     8
3. A-SCOPE: The vulnerable arithmetic pattern fell within                9    Threats to Validity
   COBALT’s current invariant coverage.
                                                                         We enumerate seven attacks on the paper’s claims.
   Under A-SRC, A-CWE, and A-SCOPE: a pre-deployment
                                                                            V1 – No sandbox source access. We have not analyzed the
COBALT scan would have been expected to surface the relevant
                                                                         Mythos sandbox code. The Mythos claim is conditional on
arithmetic pattern and return an SAT verdict with exploitation
                                                                         A-SRC, A-CWE, A-SCOPE (§8). If any assumption fails, the
witness. Anthropic could have patched the infrastructure before
                                                                         conditional claim does not hold.
deploying Mythos inside it. The reported escape vector, as
analyzed here, would not have remained available in that form.              V2 – COBALT coverage is bounded. COBALT’s invariant
                                                                         set covers CWE-190, 191, 125, and 476. A novel arithmetic
   Falsification condition: if the escape vector was not CWE-
                                                                         pattern outside this set would not be detected. We claim de-
190 class, or was expressed in a form not parseable by libclang
                                                                         tection of a class, not exhaustive recall. False positive rate on
(e.g., JIT-compiled, binary-only), the claim does not hold.
                                                                         large production codebases is not characterized in this work;
   Note on A-SCOPE non-vacuity: A-SCOPE is not tautolog-
                                                                         a SAT verdict reflects arithmetic reachability within the en-
ical. COBALT’s invariant set was designed and empirically
                                                                         coded pattern, not confirmed reachability along all execution
validated against a general CWE-190/191 corpus prior to the
                                                                         paths of the full program. Interprocedural guards or compiler-
Mythos incident—not engineered post-hoc to cover the TCP
                                                                         enforced invariants not visible in the local encoding may render
SACK pattern. The TCP SACK signed-cast overflow falls
                                                                         a SAT-flagged pattern unreachable in practice.
within CWE-190 by arithmetic structure; this coincidence is
                                                                            V3 – Post-escape layers lose authority. VERDICT and
what makes the conditional claim meaningful rather than cir-
                                                                         DIRECTIVE-4 operate within the agent’s execution context. If
cular. Had the escape vector been, e.g., a format-string bug
                                                                         an escape is complete before these layers execute, they cannot
or a use-after-free, A-SCOPE would have failed and the claim
                                                                         constrain post-escape actions. This reinforces why Layer 1 is
would not hold. A direct validation of A-SCOPE is provided by
                                                                         primary.
COBALT-2026-004 (§5): COBALT scanned tcp input.c
HEAD without knowledge of the specific line, and Z3 flagged                 V4 – Novel escape vectors. A sufficiently capable agent may
the CWE-195 pattern at the file and region consistent with the           identify escape paths outside the CWE-190/191/125/476 set.
reported finding. The detection did not require tuning to the            Additional invariant development is required for other classes.
Mythos case.                                                                V5 – Constraint layers are software. VERDICT and
                                                                         DIRECTIVE-4 are implemented in software and theoretically
                                                                         subject to their own vulnerabilities. This is an active area of
8.3     Proven vs. Proposed: Summary                                     development.
                                                                            V6 – Incident reports are secondary sources. Public tech-
Table 4 consolidates the four-tier claim hierarchy used through-
                                                                         nical accounts of the Mythos incident are secondary and partial.
out this paper. Every claim in the text is bounded to one of these
                                                                         If the actual escape vector differs from the hypothesized CWE-
tiers: Validated (formally proven, independently verified), Pro-
                                                                         190 class, our conditional argument must be updated.
totype (working code, benchmarked), Implemented (working
                                                                            V7 – Reduced encodings abstract away implementation
code, ongoing AI containment validation), and Conditionally
                                                                         context. The Z3 listings model vulnerability-relevant arith-
argued (conditional on stated assumptions).
                                                                         metic structure rather than complete program semantics. Con-
                                                                         textual guards, compiler behavior, or interprocedural effects
             Table 4: Contribution Status Summary
                                                                         present in full deployments may not be captured, and could
                                                                         affect whether the encoded pattern is reachable in practice.
      Contribution                Status         Evidence
      CWE-190 SAT (Thm. 1)        Validated      Z3 witness
      UNSAT under bound           Validated      Z3 cert.                10     Related Work
      (Prop. 1)
      4 production case studies   Validated      Acked.                  AI containment. Soares et al. [7] formalize corrigibility at the
      OpenBSD tcp scan            Pattern det.   Z3
                                                                         objective level. Hadfield-Menell et al. [8] address cooperative
      (COBALT-2026-004)                          WD1+WD3
      Mythos class detection      Cond. argued   3 assump-
                                                                         inverse RL. Ruan et al. [9] propose an LM-emulated sandbox.
                                                 tions                   Our contribution operates at the infrastructure layer beneath
      COBALT-Runtime              Prototype      301 ns/call             these approaches: formally verifying the cage, not the model’s
      COBALT-Graph                Prototype      2     chains            objectives.
                                                 SAT                        Formal verification of system software. seL4 [10] demon-
      VERDICT     constraint      Implemented    Code, 6 con-            strates that an OS kernel can be fully verified against functional
      model                                      straints                correctness and security properties. CertiKOS [11] extends
      DIRECTIVE-4 output          Implemented    Code, CI,               this to concurrent kernels. We apply the same principle to AI
      firewall                                   19 tests                sandbox infrastructure, at a less complete level: CWE-class
      SENTINEL runtime mon-       Implemented    Code, live
                                                                         arithmetic decidability rather than full functional correctness.
      itor                                       observ.
                                                                            SMT-based vulnerability analysis. KLEE [12] and
                                                                         angr [13] apply symbolic execution at the binary level. Our


                                                                     9
emphasis is targeted formalization of arithmetic vulnerability       cannot fully enumerate. COBALT will be extended toward this
predicates at source level, not full-path symbolic execution.        architecture. The formal semantics developed in Theorem 1
This trades recall for precision: every SAT result is provably       and Proposition 1 are directly reusable as runtime predicates
reachable within the encoding, not a path-bounded approxima-         with no re-encoding.
tion. The BBD corpus [6] provides an empirical reference for            A minimal guard prototype validates the two-phase design
comparing formal and heuristic vulnerability detection rates on      against 2,000 safe and 2,000 unsafe inputs across two invari-
C/C++ targets.                                                       ants (Mosquitto CWE-191 underflow and NASA cFE CWE-
   Runtime monitoring and complex event processing.                  195 truncation overflow). In the offline phase, Z3 derives safe
Hallé’s BeepBeep framework [15] demonstrates declarative            bounds once at deployment: safe min=8 for the Mosquitto
specification and real-time verification of temporal proper-         pattern and safe max=89,478,485 for the truncation pat-
ties over live event streams. Where COBALT operates pre-             tern, in 180 ms total. In the runtime phase, each trust-boundary
deployment via offline Z3 proofs, BeepBeep-style CEP oper-           crossing is an O(1) integer comparison with no Z3 invocation:
ates post-deployment over continuous action logs — the two           mean latency 87.2 ns, median 83.0 ns, p99 125 ns, throughput
approaches are complementary: COBALT eliminates the arith-           11.55 M checks per second. The guard blocked all 2,000 unsafe
metic vulnerability class statically; SENTINEL provides con-         inputs and passed all 2,000 safe inputs with no false positives
tinuous observability for cases where static analysis scope is       or false negatives. These results indicate that formally derived
exceeded.                                                            arithmetic invariants can be enforced at runtime with negligi-
   AI cybersecurity capability. The Mythos incident marks a          ble overhead once compiled offline. A production-hardened
qualitative transition in AI capability [1, 2]: AI systems can now   implementation with IPC and syscall instrumentation is future
autonomously identify and exploit infrastructure vulnerabilities.    work.
Our framework is a direct response to this transition at the            COBALT-Graph: cross-pattern escalation chains. The
infrastructure layer.                                                current COBALT invariant engine evaluates each CWE-class
                                                                     predicate independently. A sufficiently capable agent, however,
                                                                     does not exploit vulnerabilities in isolation—it assembles them.
11     Future Work                                                   The Mythos escape demonstrates this: a CWE-190 overflow in
                                                                     TCP SACK produces a corrupted int32 t sequence number,
The analysis in this paper suggests three concrete development       which may subsequently serve as an attacker-controlled size
directions, ordered by proximity to the validated layer.             argument to a memcpy() call, producing a CWE-125 out-of-
   COBALT-∆: differential verification. Patch cycles intro-          bounds read as a second-order consequence. COBALT cur-
duce new arithmetic patterns while removing old ones. A diff-        rently detects each pattern separately (Table 2); neither check
aware COBALT mode—using Z3’s incremental push/pop                    alone proves that the two-step escalation is exploitable.
interface to recheck only modified invariant regions—would              COBALT-Graph addresses this by constructing a dataflow
provide continuous formal coverage across patch cycles with-         bridge between pattern predicates. Two CWE-class encodings
out full-corpus re-analysis. This directly addresses the scenario    are composed when the satisfying witness of the first—its SAT
where a patch intended to fix one overflow silently introduces a     output value—appears as a free variable in the second:
boundary condition in adjacent logic (V4).
                                                                    Listing 20: COBALT-Graph: CWE-190→CWE-125 chain (pro-
   COBALT-Adapt: adjacent CWE expansion. The current
                                                                    totype, verified SAT)
invariant set covers CWE-190, 191, 125, and 476. AI sandbox
infrastructure also depends on correct pointer arithmetic, allo- 12 sack_start
                                                                      rcv_nxt
                                                                                   = BitVec(’sack_start’, 32)
                                                                                   = BitVec(’rcv_nxt’,    32)
cation accounting, and IPC framing. Extending the invariant 3 buffer_bound = BitVecVal(4096,              32)
corpus to CWE-122 (heap-based buffer overflow) and CWE- 45 s# =Stage      Solver()
                                                                              1: CWE-190 TCP SACK signed-cast overflow
131 (incorrect size calculation in malloc calls) would close 6 diff = sack_start - rcv_nxt
                                                                    7 s.add(UGE(diff, BitVecVal(0x80000000, 32)))
the most common gaps V2 identifies.                                 8 # Dataflow bridge: corrupted diff IS the memcpy size
   COBALT-Runtime: hybrid shadow execution. After anal-                    argument
                                                                    9 size_arg = diff
ysis, we identify runtime verification as the natural ideal ex- 10 # Stage 2: CWE-125 out-of-bounds via attacker-controlled
tension of the pre-deployment approach developed here. A                   size
                                                                   11 s.add(UGT(size_arg, buffer_bound))
runtime layer would instrument trust boundaries—IPC end- 12 # s.check() -> sat (8.1 ms)
points, system call sites, network receive paths—and evaluate 13 # witness: sack_start=0x91de51f1, rcv_nxt=0xc3582921
                                                                   14 #            bridge_value=0xce8628d0 (> 4096 -> OOB
a Z3-lite bitvector model against live arithmetic values at each           confirmed)
crossing. This converts pre-deployment pattern detection into a
continuous invariant enforcement mechanism: instead of prov-           A single Z3 check() over the composed constraint set
ing that an overflow cannot happen under stated constraints, the returns SAT only if the complete two-step chain is simul-
runtime layer proves, at each execution, that it did not happen taneously satisfiable—a strictly stronger claim than either
on the current inputs. The pre-deployment pass (COBALT) predicate in isolation. The prototype (cobalt graph.py)
and the runtime pass (COBALT-Runtime) are complementary: verifies two chains: CWE-190→CWE-125 (8.1 ms, wit-
the former removes statically-provable vulnerabilities before ness sack start=0x91de51f1) and CWE-191→CWE-
deployment; the latter catches residual paths that static analysis 125 (4.6 ms, witness input len=0x0, bridge value


                                                                 10
0xfffffff8—the Mosquitto CWE-191 underflow propagat-                Acknowledgements
ing as a downstream size argument). In both cases, the isolated
predicates return SAT individually; COBALT-Graph proves the         The author thanks the open-source maintainers at NASA, wolf-
composed escalation path is satisfiable with a single consistent    SSL, and Eclipse who responded to COBALT disclosures, and
input set.                                                          the AI safety research community whose work on corrigibility
    Pairs are enumerated over the Cartesian product of invariants   and formal policy enforcement informed the VERDICT and
filtered by output-type compatibility. This approach scales to      DIRECTIVE-4 designs. Correspondence concerning this work
chains of depth two or three before Z3 solving time becomes         and related formal verification engagements may be addressed
prohibitive; depth-k search beyond that requires incremental        to dominik@qreativelab.io.
pruning. The dataflow bridge formalization is implemented;
production-grade compatibility filtering and depth-k enumera-
tion remain future work.
                                                                    References
    Together, these four directions address the principal limita-    [1] Anthropic. Project Glasswing: Securing Critical Soft-
tions acknowledged in V2, V4, and V7: bounded invariant cov-             ware for the AI Era. April 2026. https://www.
erage, novel escape vectors, the gap between reduced encodings           anthropic.com/glasswing
and full deployment context, and the absence of cross-pattern
escalation reasoning against adaptive agents.                        [2] SC Media. Claude Mythos Preview identifies 27-
                                                                         year-old bug, finds thousands of zero-days in weeks.
                                                                         April 2026. https://www.scworld.com/news/
                                                                         anthropic-claude-mythos-preview-finds-thousands
12     Conclusion                                                    [3] Ellis, M. An AI Found a 27-Year-Old Bug
                                                                         Hiding in OpenBSD. It Cost Less Than
The Mythos sandbox escape was not inevitable. The escape                 $50 to Find It. Predict / Medium, April
mechanism was not publicly characterized—but the incident                2026.       https://medium.com/predict/
exposed a structural absence: the infrastructure surrounding a           an-ai-found-a-27-year-old-bug-hiding-in-openbs
frontier model was never formally verified. Whatever the spe-
cific vector, the class of arithmetic vulnerabilities that COBALT [4] Vedi, S. Claude Mythos: The AI That Hacked Every OS
detects has been present in C codebases for decades and is for-        and Escaped Its Own Cage. GenAI / Medium, April
mally modelable by Z3 in milliseconds.                                 2026.      https://medium.com/@shubhamnv2/
   Under assumption A-CWE (§8), Z3-based pre-deployment                claude-mythos-the-ai-that-hacked-every-os-and-
analysis would have been capable of surfacing a CWE-190/191 [5] Adelsbach, P. wolfSSL Pull Request #10096: Fix
pattern in the sandbox infrastructure before Mythos was de-            signed left-shift UB in ML-DSA w1 coefficient encoding.
ployed.                                                                March 2026. https://github.com/wolfSSL/
   This paper establishes three things. First, that COBALT             wolfssl/pull/10096
detects the CWE-190 class formally, in production C/C++ in-
frastructure codebases, with machine-verified SAT witnesses        [6] Blain, D. Broken by Default: A Z3 Formal Verification
and UNSAT certificates—demonstrated on NASA cFE, wolf-                 Study of AI-Generated C/C++ Code. arXiv:2604.05292,
SSL, Eclipse Mosquitto, and NASA F Prime. Second, that the             April 2026.
TCP SACK arithmetic pattern is formally modelled by Theo- [7] Soares, N., Fallenstein, B., Yudkowsky, E., and Arm-
rem 1, formally eliminable by Proposition 1, and independently         strong, S. Corrigibility. AAAI Workshop on AI and
detectable as a CWE-195 pattern in OpenBSD tcp input.c                 Ethics, 2015.
by COBALT without prior knowledge of the specific line
(COBALT-2026-004, §5; pattern-class detection, not an as- [8] Hadfield-Menell, D. et al. Cooperative Inverse Reinforce-
sertion about the specific Mythos escape vector). Third, that a        ment Learning. NeurIPS, 2016.
four-layer framework addresses each structural failure mode the
                                                                   [9] Ruan, Y. et al. Identifying the Risks of LM Agents with an
incident exposed—with the first layer validated, two prototype
                                                                       LM-Emulated Sandbox. arXiv:2309.15817, 2023.
extensions benchmarked, and the remaining enforcement layers
implemented with end-to-end containment validation ongoing. [10] Klein, G. et al. seL4: Formal Verification of an OS Kernel.
   The conditional claim stands: had COBALT been applied to            ACM SOSP, 2009.
the Mythos sandbox infrastructure, it would, under the stated
                                                                  [11] Gu, R. et al. CertiKOS: An Extensible Architecture for
assumptions, have been capable of surfacing a CWE-190/191
                                                                       Building Certified Concurrent OS Kernels. USENIX
arithmetic pattern before deployment.
                                                                       OSDI, 2016.
   The lesson is not that Mythos was too capable to contain. It
is that the containment infrastructure was not formally verified. [12] Cadar, C., Dunbar, D., and Engler, D. KLEE: Unassisted
That is an engineering problem with a formal solution, and we          and Automatic Generation of High-Coverage Tests for
know how to build it.                                                  Complex Systems Programs. USENIX OSDI, 2008.


                                                                11
[13] Shoshitaishvili, Y. et al. SOK: (State of) The Art of
     War: Offensive Techniques in Binary Analysis. IEEE S&P,
     2016.
[14] Russell, S. Human Compatible: Artificial Intelligence and
     the Problem of Control. Viking, 2019.

[15] Hallé, S. “When RV Meets CEP.” Proc. 16th Int’l Conf. on
     Runtime Verification (RV’16), Lecture Notes in Computer
     Science, vol. 10012, Springer, 2016, pp. 232–238.




                                                                 12
