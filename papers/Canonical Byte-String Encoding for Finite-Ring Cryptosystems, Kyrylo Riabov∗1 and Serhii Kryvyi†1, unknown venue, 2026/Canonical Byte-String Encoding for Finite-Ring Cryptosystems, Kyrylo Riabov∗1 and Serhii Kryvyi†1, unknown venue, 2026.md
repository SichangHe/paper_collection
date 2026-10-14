                                                  Canonical Byte-String Encoding for Finite-Ring Cryptosystems

                                                                                    Kyrylo Riabov∗1 and Serhii Kryvyi†1
                                         1
                                             Taras Shevchenko National University of Kyiv, Faculty of Computer Science and Cybernetics, 4d
                                                                  Akademika Glushkova Ave., Kyiv, 03680, Ukraine
arXiv:2603.23364v2 [cs.CR] 11 May 2026




                                                                                                     Abstract

                                                    Ring-mapping cryptosystems need a canonical procedure that converts ordinary byte strings into valid
                                                    residues before any algebraic encryption step can begin. This paper isolates that representation layer
                                                    and presents the base-𝑚-len codec, a canonical map from byte strings of length less than 2𝑤 to lists of
                                                    residues modulo 𝑚. The construction uses two fixed-width base-𝑚 headers, for the byte length and the
                                                    final normalized state, together with a uniform payload transduction inspired by the normalized-state
                                                    viewpoint of ANS and rANS [1], [2].
                                                    The resulting format is deterministic, self-delimiting, and parameterized by the target modulus, which
                                                    makes it suitable as a transport layer for finite-ring protocols rather than as an entropy coder. Its length-
                                                    first wire format keeps the abstract specification close to the implementation interface: the decoder can
                                                    recover the declared output size before processing the remaining payload stream, while the encoder re-
                                                    mains linear in the emitted digit stream. For every supported modulus, decoding reconstructs the original
                                                    bytes exactly; because the byte length is encoded explicitly, decoding also tolerates appended valid suffix
                                                    digits and stops after the declared payload has been recovered.
                                                    The paper links the abstract codec to a companion Rust implementation and a Lean 4 formalization with
                                                    machine-checked proofs. The formal development establishes fixed-width header inversion, normalization-
                                                    window bounds on the stored payload state, stream-level roundtrip correctness, and validity of every emit-
                                                    ted residue.
                                                    We also analyze asymptotic representation cost, report representative native-code throughput, and dis-
                                                    cuss practical limits such as exposed message length, implementation-level allocation bounds, and the
                                                    distinction between deterministic serialization and cryptographic protection.


                                         Keywords: finite-ring cryptography, message representation, base-𝑚 encoding, formal verification


                                         1 Introduction

                                         Finite-ring cryptosystems such as the ring-image construction in [3] require messages to be represented as
                                         elements of ℤ𝑚 before encryption or decryption. Existing examples use hand-built alphabets and small fixed
                                         symbol tables, which illustrate the algebra but leave open the general problem of how arbitrary UTF-8 text [4]
                                         or binary data should be represented before the ring-level encryption step begins.
                                           This representation problem extends beyond the mentioned papers. Any protocol that operates on plain-
                                         text data over ℤ𝑚 must first represent that data as residues in ℤ𝑚 before applying its core transformations.
                                              ∗
                                                  kyryl.riabov@gmail.com; ORCID 0009-0003-4118-8492
                                             †
                                                  sl.krivoi@gmail.com; ORCID 0000-0003-4231-0691


                                                                                                         1
2 Model, implementation scope, and Lean 4 formalization                                                      2


Canonical byte-level encodings are standard in other settings, including base-𝑁 transfer encodings [5], ASN.1
canonical and distinguished encoding rules [6], deterministic CBOR-based interchange [7], and public-key
standards with explicit octet-string and integer conversion rules [8]. Those formats solve adjacent interop-
erability problems, but they do not provide a modulus-parameterized residue stream tailored to protocols
that natively operate over ℤ𝑚 . This aspect is also reflected in the ERC project SYMPZON [9], which studies
symmetric primitives over integer rings for applications such as format-preserving encryption, multi-party
computation, fully homomorphic encryption, and zero-knowledge. The present work provides a concrete
representation layer that can support such constructions.
   This paper defines a canonical byte-to-residue codec for finite-ring cryptosystems. The preferred base-𝑚-
len construction maps each byte string of length less than 2𝑤 to a residue stream in ℤ𝑚 . Its wire format
consists of three components: a fixed-width base-𝑚 encoding of the byte length and the final payload state,
and a payload stream produced by a uniform base-𝑚 transduction. The decoder reconstructs the original
bytes exactly and stops after the declared length, so any additional valid suffix digits are ignored.
   The present construction is not an entropy coder. Its asymptotic payload cost reflects a change of output
alphabet rather than a reduction in information content; larger moduli may reduce the number of transmit-
ted residue symbols, but bit-level compression would require an explicit probabilistic source model and lies
outside the scope of this paper. The payload mechanism follows the normalized-state perspective of ANS and
rANS, but is used here to obtain a deterministic, self-delimiting residue format rather than a new entropy
coder or security primitive [1], [2]. The problem addressed is orthogonal to ring-based lattice cryptography
such as NTRU and ML-KEM [10], [11], which rely on different assumptions and target different protocol
goals.
  The paper makes three contributions.

   1. It defines a canonical, modulus-parameterized byte-to-residue codec for finite-ring protocols, centered
      on the base-𝑚-len wire format.
   2. It establishes exact decoding, suffix tolerance, and fixed-width header inversion for supported moduli
      and byte strings of length less than 2𝑤 .
   3. It provides a reference implementation and formal specification, consisting of a Rust library and a Lean
      4 formalization with machine-checked proofs.

  The remainder of the paper formalizes the model and proof scope, specifies the codec, states the main
guarantees, and evaluates its complexity and practical performance.


2 Model, implementation scope, and Lean 4 formalization

2.1 Core definitions and boundaries

Throughout the abstract development, we fix a global word width 𝑤 ∈ ℕ and study those moduli 𝑚 for which
the codec parameters are well formed at that width. The evaluation in Section 5 later instantiates this generic
theory at 𝑤 = 64.
Definition 2.1 (Supported modulus). For the fixed word width 𝑤, a supported modulus is a modulus 𝑚 for
which the abstract codec parameters are well formed, namely

                           2≤𝑚        and      256 ≤ decoderLowerBound(𝑤, 𝑚).

This definition is formalized in [Params.lean, L51–L55].
Definition 2.2 (Admissible byte string). An admissible byte string is a finite sequence of bytes of length less
than 2𝑤 . We write
                                                                 ∗
                       ByteString𝑤 = {bytes ∈ {0, 1, … , 255} ∶ |bytes| < 2𝑤 } .
3 The Base-m-len codec                                                                                         3


This definition is formalized in [Spec.lean, L17–L19].

  For each supported modulus 𝑚, the abstract codec interface is

   Encode𝑚 ∶ ByteString𝑤 → List(Fin(𝑚)),           Decode𝑚 ∶ List(Fin(𝑚)) → Except(Error, ByteString𝑤 ).

The encoder produces valid base-𝑚 digits only, and the decoder either reconstructs an admissible byte string
or reports failure. The abstract encoder and decoder are formalized in [Spec.lean, L146–L182], while the fact
that every emitted symbol lies in [0, 𝑚) is recorded in [Stream.lean, L27–L33].
  The core model treats residue digits as elements of Fin(𝑚) from the outset, so malformed raw naturals
outside the residue range do not appear inside the proved interface; see [Params.lean, L32–L34] for the digit
type and [Spec.lean, L184–L239] for the boundary validators on plain numeric inputs. The zero-length case is
explicit as well: if the length prefix decodes to 0, the decoder returns the empty byte string immediately, as in
[Spec.lean, L159–L169]. The corresponding zero-length decoding lemmas appear in [Stream.lean, L135–L172].


2.2 Implementation and proof scope

The public artifacts consist of a Rust library and a Lean 4 formalization with machine-checked proofs. Both
are released in the same project repository [12]. On the Rust side, the main byte-oriented entry points are
encode_bytes_base_m_len and decode_bytes_base_m_len, with UTF-8 frontends above them. On the proof
side, Lean formalizes the abstract codec, including supported parameters, fixed-width prefixes, payload trans-
duction, and end-to-end stream properties in Lean 4 [13]; the trusted-kernel and elaboration lineage behind
the environment is described in [14]. The current development is width-parametric rather than tied to one
machine word size, and the repository includes concrete 64-, 128-, and 256-bit instantiations and smoke
theorems in [Examples.lean, L58–L70].
  The proof scope is intentionally limited to the abstract specification boundary. It does not verify the Rust
implementation line by line. Parser hardening, allocation limits, low-level I/O, and other engineering details
therefore remain implementation concerns rather than machine-checked theorems.


3 The Base-m-len codec

3.1 Fixed-width base-m headers

Definition 3.1 (Prefix width). For the fixed word width 𝑤 and a supported modulus 𝑚, let

                                        𝑘 = min {𝑗 ∈ ℕ0 ∶ 𝑚𝑗 ≥ 2𝑤 } .

The fixed-width prefix encoder EncodePrefix𝑚 represents every 𝑥 < 2𝑤 as exactly 𝑘 little-endian base-𝑚
digits.

   The same width 𝑘 is used for both fixed prefixes in the wire format: the byte length and the final pay-
load state. In the Lean 4 formalization, the definition of this width and its least-width property appear in
[Params.lean, L123–L157], with bundled forms for parameter packages in [Params.lean, L215–L271].


3.2 Uniform base-m payload transduction

Let 𝐿 denote the decoder lower bound associated with the supported modulus. The payload layer maintains
a base-𝑚 state and applies the uniform byte update

                                                𝑥 ← 256𝑥 + 𝑏.
3 The Base-m-len codec                                                                                           4


 Algorithm 1: Base-m-len encode
  Input: Admissible byte string bytes, supported modulus 𝑚
  Output: Residues in List(Fin(𝑚))
1 Set 𝑘 ← min {𝑗 ∈ ℕ0 ∶ 𝑚𝑗 ≥ 2𝑤 };
2 Encode |bytes| as 𝑘 little-endian base-𝑚 digits;
3 Initialize the payload state 𝑥 at the decoder lower bound 𝐿;
4 for byte values 𝑏 of bytes in reverse order do
5     While 𝑥 exceeds the encoder threshold, emit 𝑥 mod 𝑚 and set 𝑥 ← ⌊𝑥/𝑚⌋;
6     Set 𝑥 ← 256𝑥 + 𝑏;
7 end
8 Encode the final state 𝑥 as 𝑘 little-endian base-𝑚 digits;
9 Reverse the emitted payload digits and return len ‖ state ‖ payload;




In the Lean 4 formalization, the bundled definitions of the decoder lower bound 𝐿 and the encoder thresh-
old appear in [Params.lean, L220–L231], and the encoder-side and decoder-side renormalization procedures
together with the payload transducer are defined in [Spec.lean, L81–L144]. Operationally, the encoder scans
the input bytes from right to left. Before each byte update, it emits base-𝑚 digits until the current state is
below the encoder threshold. After the full reverse scan, the emitted payload digits are exposed in FIFO order,
so the decoder can read the final wire format from left to right.
   This mechanism is close in spirit to ANS and rANS, but the purpose is different. Classical ANS work studies
entropy coding relative to a probabilistic source model. Here the byte update is uniform, the output alphabet
is fixed by the target modulus 𝑚, and the goal is a deterministic, self-delimiting residue representation that
can serve as a canonical message layer for finite-ring protocols [1], [2].


3.3 Wire format and algorithms

Definition 3.2 (Wire format). For every admissible byte string bytes,

                                    Encode𝑚 (bytes) = len ‖ state ‖ payload,

where len = EncodePrefix𝑚 (|bytes|), state is the fixed-width encoding of the final payload state, and payload
is the FIFO base-𝑚 digit stream produced by the payload transducer.

  In the Lean 4 formalization, this concatenated wire format is the definition of the abstract encoder; see
[Spec.lean, L146–L153].
   Decoding is staged in the same order. The decoder first reads the length prefix. If that prefix is 0, it returns
the empty byte string. Otherwise, it reads the state prefix and then consumes exactly as many payload digits
as are needed to reconstruct the declared number of bytes. Any valid digits that remain after those bytes are
recovered are left unread. In the Lean 4 formalization, the staged decoder is defined in [Spec.lean, L159–L182];
its immediate zero-length return already appears in [Spec.lean, L159–L169], with dedicated zero-length stream
lemmas in [Stream.lean, L135–L172]. The padding-tolerant end-to-end theorem that trailing suffix digits are
ignored appears in [Stream.lean, L174–L266].
  In the Lean 4 formalization, Algorithms 9 and 12 correspond directly to the definitions in [Spec.lean, L81–
L182].
Example 3.1 (Worked example for “Hi” at 𝑚 = 50 and 𝑤 = 64). In the Lean 4 formalization, the companion
examples in [Examples.lean, L90–L93] evaluate the admissible byte string [72, 105] to the residue stream
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 8, 11, 36, 6, 32, 19, 0, 38, 1, 49, 1, 1, 48]
4 Correctness guarantees                                                                                    5


  Algorithm 2: Base-m-len decode
   Input: Residue stream 𝑑𝑖𝑔𝑖𝑡𝑠, supported modulus 𝑚
   Output: Except(Error, ByteString𝑤 )
 1 Set 𝑘 ← min {𝑗 ∈ ℕ0 ∶ 𝑚𝑗 ≥ 2𝑤 };
 2 Read the first 𝑘 digits as the declared byte length ℓ;
 3 if ℓ = 0 then
 4     Return ok([]);
 5 end
 6 Read the next 𝑘 digits as the initial payload state 𝑥;
 7 for 𝑖 = 1 to ℓ do
 8     Output 𝑥 mod 256;
 9     Set 𝑥 ← ⌊𝑥/256⌋;
10     While 𝑥 is below the decoder lower bound, consume the next payload digit 𝑑 and set 𝑥 ← 𝑥𝑚 + 𝑑;
11 end
12 Ignore any remaining trailing suffix and return the reconstructed bytes;




Here 𝑘 = 12. The first 12 digits are the fixed-width encoding of the byte length 2, the next 12 digits encode
the stored payload state, and the final two digits form the payload. Decoding returns ok([72, 105]), hence the
original two-byte input.


4 Correctness guarantees

The proof development is split across six Lean files, from parameters and fixed-width prefixes to renormal-
ization, payload inversion, and stream-level correctness.


4.1 Main theorems

Theorem 4.1 (Stream correctness). For every supported modulus 𝑚 and every admissible byte string bytes ∈
ByteString𝑤 ,
                               Decode𝑚 (Encode𝑚 (bytes)) = ok(bytes).
Moreover, for every valid suffix 𝑡 ∈ List(Fin(𝑚)),

                                Decode𝑚 (Encode𝑚 (bytes) ‖ 𝑡) = ok(bytes).

   Proof. In the Lean 4 formalization, the suffix-tolerant theorem is [Stream.lean, L174–L254]. Its empty-
suffix specialization is [Stream.lean, L256–L266]. The proof uses the header-parsing lemmas in [Stream.lean,
L35–L133]. The zero-length lemmas appear in [Stream.lean, L135–L172], and the payload roundtrip theorem
in [Payload.lean, L79–L141]. It first recovers the declared length prefix, then the stored state prefix, and
finally applies the payload roundtrip theorem to the remaining suffix. The extra-suffix clause follows because
decoding stops after reconstructing the declared number of bytes and therefore leaves any remaining valid
suffix unread.
Theorem 4.2 (Header correctness). For every supported modulus 𝑚, let

                                       𝑘 = min {𝑗 ∈ ℕ0 ∶ 𝑚𝑗 ≥ 2𝑤 } .

Then
                                 𝑚𝑘 ≥ 2𝑤        and      ∀𝑗 < 𝑘, 𝑚𝑗 < 2𝑤 .
5 Evaluation                                                                                                  6


Moreover, for every 𝑥 < 2𝑤 ,

                               DecodePrefix𝑚 (EncodePrefix𝑚 (𝑥)) = some(𝑥).

  Proof. In the Lean 4 formalization, the least-width property is formalized in [Params.lean, L123–L157],
with the bundled statement in [Params.lean, L260–L271]; fixed-width prefix inversion is proved in [Prefix.lean,
L65–L89]. Minimality is immediate from the definition of 𝑘 as the least exponent with 𝑚𝑘 ≥ 2𝑤 . Once that
bound is known, every 𝑥 < 2𝑤 lies in the domain of the fixed-width base-𝑚 prefix decoder.
Proposition 4.3 (Payload-state bounds). For every supported modulus 𝑚 and every admissible byte string
bytes, the payload encoder returns a state in the normalization window

                                           𝐿 ≤ state(bytes) < 𝐿𝑚.

In particular,
                                              state(bytes) < 2𝑤 .

   Proof. In the Lean 4 formalization, the normalization-window bound and its 2𝑤 corollary are proved in
[Payload.lean, L17–L77]. The first part is the inductive invariant of the payload transducer; the second follows
from the global estimate 𝐿𝑚 ≤ 2𝑤 − 1.


4.2 Proof idea and traceability

The end-to-end proof has three layers. In the Lean 4 formalization, fixed-width prefix inversion appears in
[Prefix.lean, L30–L89], renormalization roundtrip in [Renorm.lean, L219–L294], payload roundtrip in [Pay-
load.lean, L79–L141], and the final stream theorem in [Stream.lean, L174–L266], with the zero-length branch
in [Stream.lean, L135–L172]. Fixed-width base-𝑚 headers invert because the chosen width covers the bounded
𝑤-bit range; renormalization blocks roundtrip the state while preserving untouched suffixes; and a byte-level
induction lifts that result to the payload and then to the full stream theorem.


5 Evaluation

The evaluation addresses two questions: what the representation costs in theory, and whether the preferred
streaming construction is practical in native code. Throughout this section, we instantiate the general theory
at 𝑤 = 64, so the reported header widths and thresholds are the concrete 64-bit values of the generic formulas
from the preceding sections.


5.1 Complexity and representation cost

Let 𝑛 = |bytes| and let 𝑘 = ⌈log𝑚 264 ⌉. The two fixed-width headers contribute exactly 2𝑘 digits. The payload
contributes a number of digits proportional to the byte length, with asymptotic rate
                                                             8
                                             log𝑚 256 =
                                                          log2 𝑚

digits per byte. Figure 5.1 visualizes this trade-off over the range 25 ≤ 𝑚 ≤ 257: larger moduli reduce the
payload rate smoothly, while the fixed header width drops only when 𝑘 crosses an integer threshold. Since
each emitted digit is produced once and each consumed digit is read once, encoding and decoding are linear
in the stream length. For every fixed supported modulus 𝑚, this yields 𝑂(𝑛) time and 𝑂(1) working state
beyond the input and output buffers.
5 Evaluation                                                                                                           7


Figure 5.1. Representation cost as a function of the modulus 𝑚 over the range 25 ≤ 𝑚 ≤ 257 in the 𝑤 = 64
instance. The upper panel shows the smooth payload rate log𝑚 256, while the lower panel shows the stepwise
fixed header cost 2𝑘.

                                     Payload rate
                          1.8         𝑚 = 25

                          1.6
               log𝑚 256




                                                𝑚 = 50
                          1.4

                          1.2
                                                                                                       𝑚 = 257
                           1



                                     Fixed header width
                           28
                           26
                           24
                           22
                2𝑘




                           20
                           18
                           16
                                25         50                100            150            200                   257
                                                                      modulus 𝑚


Table 5.1. Asymptotic payload cost and fixed header size for representative moduli in the 𝑤 = 64 instance.

                                        Modulus 𝑚         Payload digits per byte   Header digits 2𝑘
                                              25                   1.723                  28
                                              50                   1.417                  24
                                             257                   0.9993                 16


5.2 Native performance

The companion Rust code includes Criterion benchmarks for the preferred codec, exact BigUint radix-conversion
baselines, and an external ANS reference used only for context. The representative measurements below were
recorded on an Apple M3 Pro machine using the existing harness; methodology details are summarized in
Section A. Those numbers are included only as practical evidence.


5.3 Interpretation

Three conclusions are relevant for protocol design.

   1. Small moduli remain usable, but Table 5.1 makes their header and payload overhead explicit instead of
      hiding it behind ad hoc symbol tables.
   2. The preferred streaming construction is not only asymptotically linear but also much faster in practice
      than exact whole-payload radix conversion on large inputs, which is the meaningful baseline for a
      canonical ring-level representation.
   3. The 𝑚 = 257 configuration is close to one residue per byte while still retaining explicit length recovery
      and suffix-tolerant decoding.
7 Related work                                                                                                   8


Table 5.2. Representative throughput measurements in MiB/s. The BigUint baseline is only defined for
𝑚 ≤ 256. The ANS reference column provides context only; it does not implement the same length-delimited
residue wire format.

              Workload          Native 𝑚 = 65      BigUint 𝑚 = 65      Native 𝑚 = 257      ANS ref.
              Encode 1 KiB           163.6               25.2                217.0           218.1
              Decode 1 KiB           485.9               125.7               640.5           150.9
              Encode 64 KiB          188.1               1.285               236.7           226.2
              Decode 64 KiB          510.3               3.201               669.1           144.2


6 Security role and implementation limits

This codec should be read as deterministic serialization, not as a security primitive in its own right [15]. Four
limitations matter in practice.

   1. The codec is public and deterministic, so it provides no confidentiality, integrity, or authenticity before
      the surrounding cryptographic protocol is applied.
   2. The preferred wire format exposes the exact byte length. If length hiding is required, padding must be
      enforced at the surrounding protocol layer.
   3. The Lean formalization proves the abstract specification boundary rather than the Rust implementation,
      so low-level parser and allocator behavior remain implementation responsibilities.
   4. Because decoding allocates according to the embedded length, implementations should enforce a caller-
      specified maximum decoded length for untrusted inputs.


7 Related work

Two lines of prior work are most directly relevant.
   First, ring-mapping cryptosystems motivate communication over residue domains such as ℤ𝑚 and 𝐺𝑚 .
The ring-mapping cryptosystems studied in [3], [16] provide the application setting in which byte strings
must be transported through finite-ring representations. However, those works treat the representation layer
as supporting machinery rather than as a separate codec problem.
   Second, the payload mechanism used here is structurally close to ANS and rANS [1], [2]. These methods
maintain a normalized state and use renormalization while reading or emitting symbols in a fixed radix. The
present construction adopts that operational pattern in a uniform byte setting, but uses it for deterministic,
self-delimiting transport into a prescribed residue alphabet rather than for entropy coding relative to a source
model.
   Ring-based lattice systems such as NTRU and ML-KEM [10], [11] are related only at a broader structural
level. They also work over ring-based algebraic domains, but their main concern is hardness-based encryption
and key encapsulation, not canonical byte representation for residue-domain transport.
   Accordingly, the specific focus of this paper is the byte-to-residue representation layer itself: a fixed-width,
self-delimiting codec with explicit correctness theorems and machine-checked proof traceability.
References                                                                                                 9


8 Conclusion

The base-𝑚-len codec isolates the byte-to-residue representation layer needed by finite-ring protocols. Its
wire format consists of a fixed-width length prefix, a fixed-width state prefix, and a uniform base-𝑚 payload
stream. For every fixed word width 𝑤, every supported modulus, and every admissible byte string of length
less than 2𝑤 , decoding recovers the original bytes and is tolerant of any valid trailing suffix.
   The released Rust library [17] and the benchmark suite in the project repository indicate that the con-
struction is practical, while the Lean 4 formalization in the repository [12] establishes fixed-width prefix
inversion, payload-state bounds, and end-to-end stream correctness. Because the codec outputs canonical
residue streams in ℤ𝑚 , it composes directly with the ℤ𝑚 ↔ 𝐺𝑚 transport layer used in prior ring-mapping
cryptosystems [3], [16]. More broadly, it contributes a concrete message-representation layer to current work
on symmetric cryptography over integer rings, as reflected in the SYMPZON agenda [9].


A Benchmark methodology

The Criterion benchmark suite in the project repository [12] is organized into four families.

   1. Native byte-transduction benchmarks for encode_bytes_base_m_len and decode_bytes_base_m_len,
      evaluated at moduli 2, 3, 13, 65, 251, 257 and input sizes 32 B, 1 KiB, and 64 KiB.
   2. UTF-8 smoke benchmarks for the text frontend encode_text_base_m_len and decode_text_base_m_len
      at modulus 𝑚 = 65, using mixed UTF-8 inputs of size 1 KiB and 64 KiB.
   3. Exact BigUint radix-conversion baselines for byte encode/decode at moduli 2, 3, 13, 65, 251 and the
      same three byte sizes; modulus 257 is excluded because the underlying radix-conversion routine sup-
      ports moduli only up to 256.
   4. Reference ANS encode/decode benchmarks, implemented via the external constriction library, at input
      sizes 32 B, 1 KiB, and 64 KiB.

   Unless noted otherwise, the representative throughput values reported in Table 5.2 were obtained on an
Apple M3 Pro machine using short Criterion runs with sample size 10, warm-up time 0.1 s, and measurement
time 0.2 s.


References

 [1] J. Duda, “Asymmetric numeral systems: Entropy coding combining speed of Huffman coding with com-
     pression rate of arithmetic coding,” arXiv preprint arXiv:1311.2540, 2014. doi: 10.48550/arXiv.1311.
     2540 arXiv: 1311.2540 [cs.IT]. [Online]. Available: https://arxiv.org/abs/1311.2540v2
 [2] F. Giesen, rANS notes, Practitioner notes on streaming rANS, 2014. [Online]. Available: https : / /
      fgiesen.wordpress.com/2014/02/02/rans-notes/
 [3] S. Kryvyi and K. Riabov, “Symmetric cryptosystem based on ring images,” in Proceedings of the Workshop
     on Intelligent Information Technologies (UkrProg-IIT 2025), ser. CEUR Workshop Proceedings, vol. 4049,
     CEUR-WS.org, 2025. [Online]. Available: https://ceur-ws.org/Vol-4049/paper1.pdf
 [4] F. Yergeau, “UTF-8, a transformation format of ISO 10646,” RFC Editor, RFC 3629, Nov. 2003. doi: 10.
     17487/RFC3629 [Online]. Available: https://www.rfc-editor.org/info/rfc3629
 [5] S. Josefsson, “The base16, base32, and base64 data encodings,” RFC Editor, RFC 4648, Oct. 2006. doi:
     10.17487/RFC4648 [Online]. Available: https://www.rfc-editor.org/info/rfc4648
 [6] International Telecommunication Union. “X.690: Information technology – ASN.1 encoding rules: Spec-
     ification of basic encoding rules (BER), canonical encoding rules (CER) and distinguished encoding rules
References                                                                                                    10


       (DER).” Recommendation X.690 (02/2021) | ISO/IEC 8825-1:2021. [Online]. Available: https://www.
       itu.int/ITU-T/recommendations/rec.aspx?rec=14779&lang=en
 [7] C. Bormann and P. Hoffman, “Concise binary object representation (CBOR),” RFC Editor, RFC 8949,
     Dec. 2020, STD 94. doi: 10.17487/RFC8949 [Online]. Available: https://www.rfc-editor.org/
       info/rfc8949
 [8] K. Moriarty, B. Kaliski, J. Jonsson, and A. Rusch, “PKCS #1: RSA cryptography specifications version 2.2,”
     RFC Editor, RFC 8017, Nov. 2016. doi: 10.17487/RFC8017 [Online]. Available: https://www.rfc-
       editor.org/info/rfc8017
 [9] European Commission. “SYMPZON: Getting SYMmetric CryPtography Out of its Comfort ZONe.” ERC
     Starting Grant, Horizon Europe, grant agreement No. 101160608, 2025–2030. [Online]. Available: https:
       //cordis.europa.eu/project/id/101160608
[10]   J. Hoffstein, J. Pipher, and J. H. Silverman, “NTRU: A ring-based public key cryptosystem,” in Algorithmic
       Number Theory, ser. Lecture Notes in Computer Science, vol. 1423, Springer, 1998, pp. 267–288. doi:
       10.1007/BFb0054868 [Online]. Available: https://www.ntru.org/f/hps98.pdf
[11]   National Institute of Standards and Technology, Post-quantum cryptography standards: FIPS 203 (ML-
       KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA), NIST post-quantum cryptography standards overview,
       Aug. 2024.
[12]   K. Riabov. “Phd-symmetric-cryptography: Lean formalization of the base-n-len codec.” GitHub repos-
       itory. [Online]. Available: https : / / github . com / KyrylR / phd - symmetric - cryptography /
       blob/8e903222a7df1c4365592e4b16fa752a924b8977/lean/encoding-dr-1
[13]   L. de Moura and S. Ullrich, “The lean 4 theorem prover and programming language,” in Automated
       Deduction – CADE 28, ser. Lecture Notes in Computer Science, vol. 12699, Springer, 2021, pp. 625–635.
       doi: 10.1007/978- 3- 030- 79876- 5_37 [Online]. Available: https://link.springer.com/
       chapter/10.1007/978-3-030-79876-5_37
[14]   L. de Moura, S. Kong, J. Avigad, F. van Doorn, and J. von Raumer, “The lean theorem prover (system
       description),” in Automated Deduction – CADE-25, ser. Lecture Notes in Computer Science, vol. 9195,
       Springer, 2015, pp. 378–388.
[15]   C. E. Shannon, “Communication theory of secrecy systems,” Bell System Technical Journal, vol. 28, no. 4,
       pp. 656–715, 1949. doi: 10.1002/j.1538- 7305.1949.tb00928.x [Online]. Available: https:
       //pages.cs.wisc.edu/~rist/642-spring-2014/shannon-secrecy.pdf
[16]   S. L. Kryvyi, V. N. Opanasenko, E. A. Grinenko, and Y. A. Nortman, “Symmetric information ex-
       change system based on ring isomorphism,” Cybernetics and Systems Analysis, vol. 58, no. 5, 2022. [On-
       line]. Available: https : / / www . springerprofessional . de / en / symmetric - information -
       exchange-system-based-on-ring-isomorphism/23785398
[17]   K. Riabov, Sym-adv-encoding, Rust crate, 2026. [Online]. Available: https://crates.io/crates/
       sym-adv-encoding
