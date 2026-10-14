                                                PAL*M: Property Attestation for Large Generative Models
                                                          Prach Chantasantitam1 , Adam Ilyas Caulfield1 , Vasisht Duddu1 , Lachlan J. Gunn2 , N. Asokan1,3
                                                                 1 University of Waterloo, 2 Aalto University, 3 KTH Royal Institute of Technology

                                                               {pchantas, acaulfield, vasisht.duddu}@uwaterloo.ca, lachlan@gunn.ee, asokan@acm.org

                                         Abstract                                                                      PAL*M employs incremental multiset hashing [19] to enable com-
                                         Machine learning property attestations allow provers (e.g., model          pact secure integrity tracking of large, randomly-accessed, datasets,
                                         providers or owners) to attest properties of their models/datasets         and TEE-aware GPUs to efficiently and securely ensure integrity of
                                         to verifiers (e.g., regulators, customers), enabling accountability        heterogeneous operations. Finally, we define property attestations
                                         towards regulations and policies. But, current approaches do not           for a comprehensive set of operations (e.g., fine-tuning, quantiza-
                                         support generative models or large datasets. We present PAL*M,             tion, LLM chat sessions) that do not require revealing confidential
arXiv:2601.16199v3 [cs.CR] 30 Apr 2026




                                         a property attestation framework for large generative models, il-          datasets or models to Vrf. We prototype and evaluate PAL*M using
                                         lustrated using large language models. PAL*M defines properties            Intel TDX and NVIDIA H100. Our contributions are: we
                                         across training and inference, leverages confidential virtual ma-          (1) propose use of incremental multiset hash functions to construct
                                         chines with security-aware GPUs for coverage of CPU-GPU op-                    representative measurements of datasets in external storage
                                         erations, and proposes using incremental multiset hashing over                 that are randomly sampled at run-time (Section 4.2);
                                         memory-mapped datasets to efficiently track their integrity. We im-        (2) define how to measure properties of generative model opera-
                                         plement PAL*M on Intel TDX+NVIDIA H100 and evaluate it using                   tions, incorporating GPU attestation evidence without exposing
                                         state-of-the-art models and datasets, showing PAL*M is efficient,              confidential details (Section 4.3);
                                         incurring <11% overhead for common operations. Finally, we use             (3) specify a property attestation protocol that shows how such
                                         the Tamarin Prover symbolic verification tool to formally model                measurements and outputs can be combined to prove data/-
                                         PAL*M’s property attestation protocol, confirming that its security            models were produced by a PAL*M-equipped CPU-GPU con-
                                         guarantees are upheld under the defined threat model.                          figuration (Section 4.4);
                                                                                                                    (4) implement a fully functional prototype1 of PAL*M built on
                                                                                                                        commercially available CVM and TEE-aware GPU – Intel TDX
                                         Keywords                                                                       and NVIDIA H100 (Section 5); and
                                         Property Attestation, Trusted Computing, Large Genarative Models           (5) show that PAL*M meets desired requirements, including effi-
                                                                                                                        ciency for common operations, using real-world datasets/mod-
                                                                                                                        els, and security, by formally modeling and verifying PAL*M’s
                                         1   Introduction                                                               property attestation protocol using Tamarin Prover (Section 6).
                                         Machine learning (ML) models are widely deployed across domains
                                         such as healthcare, finance, and autonomous systems [42, 94, 99].          2 Background
                                         Emerging regulations (e.g., EU’s AI Act [3]) require models meet           2.1 Large Language Models
                                         certain properties related to accuracy, training procedures, data
                                                                                                                    Training. LLMs use transformer architectures with billions of pa-
                                         provenance, and inference. Providing proof of such properties may
                                                                                                                    rameters [14, 96], and are trained to predict the next tokens given
                                         be challenging for confidential datasets or models.
                                                                                                                    previous ones. During training, the model learns a probability dis-
                                            ML property attestation enables a prover Prv (e.g., a model provider)
                                                                                                                    tribution of the next token from a vocabulary to follow a sequence
                                         to demonstrate properties about their model or datasets to a veri-
                                                                                                                    of tokens. This is often called pretraining, as it is typically followed
                                         fier (Vrf) [22]. Approaches based on trusted execution environments
                                                                                                                    by another phase of training for task-specific optimization/tuning.
                                         (TEEs) [5, 8, 48, 49], first proposed in Laminator [23], has been
                                                                                                                       Tokenizers. Modern tokenizers operate at word, sub-word (e.g.,
                                         shown to be efficient, scalable, versatile, and secure for classifiers,
                                                                                                                    byte pair encoding, WordPiece), or character level to convert natural-
                                         whereas alternative approaches based on zero-knowledge proofs [1,
                                                                                                                    language text into numerical representations for use during LLM
                                         33, 43, 56, 78, 87] or re-purposing of inference attacks [26, 101] do
                                                                                                                    training and inference.
                                         not meet these requirements.
                                                                                                                       Fine-tuning. Since training LLMs is resource- and time-intensive,
                                            But, Laminator does not scale to generative models, such as
                                                                                                                    publicly available trained LLMs are generally fine-tuned on a task-
                                         large language models (LLMs). For example, large datasets cannot
                                                                                                                    specific dataset. Parameter-Efficient Fine-Tuning (PEFT) and Low-
                                         reside fully in TEE memory and are random sampled from untrusted
                                                                                                                    Rank Adaptation (LoRA) fine-tune a small subset of model parame-
                                         storage, undermining standard integrity measurement strategies.
                                                                                                                    ters instead of retraining the entire model [41, 61]. Alternatively,
                                            Enabling ML property attestations for generative models re-
                                                                                                                    adapter layers are trainable modules that can be attached to a pre-
                                         quires addressing three challenges: (1) handling of large datasets
                                                                                                                    trained LLM, enabling task-specific adaptation without altering the
                                         outside of TEE memory sampled randomly, (2) supporting CPU-
                                                                                                                    core model parameters. These approaches are more efficient than
                                         GPU computing environments, and (3) defining property attestation
                                                                                                                    fine-tuning the entire LLM.
                                         for common operations related to generative models. We address
                                         these challenges with PAL*M, the first framework for ML property
                                         attestations of large generative models, using LLMs for illustration.      1 To be released after peer review
   Evaluating LLMs. Benchmarks for LLMs cover a variety of                                       Vrf                      Prv

tasks and compute relevant metrics. These tasks span language                                           (1) Challenge
understanding (e.g., MMLU [39]), math problems, multiple-choice,                                                                (2) Authenticated
classification, and open-ended question answering. Each task is                                                                 State Measurement
                                                                                                       (3) Report State
designed to probe specific capabilities of the model.                               (4) Verify
   Chat sessions. LLMs are commonly used for chatbots, which
allow a user to continuously query about a particular task and get           Figure 1: Traditional remote attestation protocol: a prover
the responses from the model that consider prior conversational              (Prv) demonstrates its software integrity to a verifier (Vrf).
context (e.g., OpenAI’s ChatGPT). Chat sessions contain multiple
user queries and their responses.
   Memory Management. Large generative models require sig-                      Intel Trust Domain eXtensions (TDX) [49] enables isolated CVMs
nificantly more data than traditional ML models, which often do              in the form of trust domains (TDs). Upon creation of a TD, invoked
not fit into main memory (e.g., Pile dataset is over 800 GB [31]). In-       by the untrusted virtual machine manager (VMM), the TDX module
stead of loading the entire data into memory, current LLM libraries          computes a measurement of TD components during TD creation,
(e.g., Hugging Face) support memory-mapped datasets [44], which              which can be used later for attestation. To attest TD’s state, the TD
map the contents of a file into a process’s virtual memory space,            invokes the TDX module to generate a TDREPORT, which is gener-
allowing it to be accessed like regular memory, rather than through          ated by the CPU computing a MAC over measurements of the TD
explicit file I/O operations, despite residing on disk. When a dataset       image, the TDX module image, and any REPORTDATA extended by
is memory-mapped, dataset records are only loaded into memory                the TD at runtime. The resulting TDREPORT and MAC are passed by
as needed, significantly reducing memory usage.                              the TDX Module to the quoting enclave (QE), a special-purpose Intel
   Data Transformations and Processing: Before a dataset is                  SGX enclave [50]. The QE uses contents of TDREPORT to generate a
used, it typically undergoes a series of transformations, including          SGX-style QUOTE using a provisioning certification key [47]. Before
preprocessing steps like normalization, concatenation, truncation,           generating this QUOTE, the QE first validates the MAC, ensuring
tokenization, and splitting into training, validation, and test sets,        integrity is maintained when passed by the untrusted VMM.
as well as additional processing for removing corrupted samples
and formatting the data to match the expected input structure of             2.3    Attestation Protocols
the training framework [45]. During training, random sampling is             Remote attestation is a protocol in which Vrf challenges Prv to
commonly used to reduce bias introduced by data ordering and                 demonstrate that they are installed with the correct configura-
to improve model generalization [77]. PyTorch’s DataLoader and               tions [66]. The steps for a traditional remote attestation protocol
Sampler abstractions provide randomized sampling [72]. Popular               are visualized in Figure 1. The authenticated integrity measurement
training libraries, such as Hugging Face Transformers, support               in step (2) is computed by Prv’s root of trust (RoT) and is typically a
random sampling and enable it for default training pipelines [46].           message authenticated code (MAC) or digital signature. Thus, one
                                                                             requirement of remote attestation is that Prv’s RoT can securely
                                                                             store and use a private key, implying some level of hardware assis-
                                                                             tance. Hence, TEEs can naturally enable remote attestation with
2.2    Trusted Execution Environments                                        their properties for isolated data and execution. For Intel TDX, step
TEEs are a set of architectural components that provide a secure             (2) involves computing TDREPORT and QUOTE.
execution environment that is isolated from the “rich” host envi-               Property attestation [79] is where Vrf is interested in properties
ronment. They guarantee that software executing outside of the               of Prv’s configuration rather than a specific configuration itself.
TEE cannot directly read or write to data inside the TEE’s trusted           Here, Vrf obtains the authenticated integrity measurement from Prv,
boundary. The exact details of the trusted boundary vary based               while also obtaining reference values that correspond to a particular
on the particular approach. For example, Intel SGX [48] creates              property from a trusted authority (Tru). If the state measurement
TEE in the user-space enclaves and ARM TrustZone [8] creates a               from Prv is among the reference values obtained from Tru, and was
TEE containing all system resources (e.g., separate trusted OS and           signed using the expected public key from Prv, Vrf trusts that the
applications with dedicated peripherals).                                    property holds on Prv. Notably, unlike standard remote attestation,
   Recent technologies have also introduced confidential virtual ma-         property attestation requires Vrf to obtain reference values from
chines (CVMs), which enable entire VMs to execute within the trust           Tru rather than to recompute them. Every property of interest is
boundary of a TEE (e.g., AMD SEV-SNP [5], Intel TDX [49], and                associated with a measurer on Prv used to measure (e.g., hash)
ARM Realms [55]). An advantage provided by CVMs is that they                 inputs and outputs corresponding to the property.
enable executing unmodified and full-feature operating systems                  The notion of property attestation has been extended recently
without requiring TEE-specific rewrites. Additionally, TEE-aware             to cover ML data and processes [22, 23, 79]. In particular, Lamina-
GPUs have recently emerged (e.g., with NVIDIA H100 GPU). As                  tor [23] leverages Intel SGX [48] to attest properties of training data,
such, CVM providers have released drivers to support integration             model, and training process. This works by executing ML opera-
with TEE-aware GPUs. This has enabled the potential for heavy                tions inside an SGX enclave, measuring the inputs and outputs of
computations (e.g., ML training) within a TEE. Both CPUs and                 the target operation (e.g., training, inference, or dataset statistics),
GPUs with TEEs typically support remote attestation to prove trust-          and using SGX’s quote mechanism to return these measurements to
worthiness to verifiers.                                                     the verifier that issued the attestation challenge. Such attestations
                                                                         2
 Tru                        Vrf                       Inr                      Prv
                                                                                                             3.2    Adversary Model
                                                              (1) Request

                                                                                     (2) Authenticated
                                                                                                             We assume an adversary (Adv), in line with the common Intel TDX
                                                                                     State Measurement       adversary model [4], who has control over the host machine. As a
                                                            (3) Report State
                                                                                                             consequence, Adv can access and manipulate any memory or de-
                                  (4) Request State
                                    Measurement                                                              vice that is not within the trusted boundaries (e.g., other VMs, disk,
                                                                                                             I/O peripherals). The TDX module and TDX-aware CPU are trusted
                                  (5) Report State                                                           to be implemented correctly and provide their described function-
       (6) Send Reference
             Values                                                                                          ality for inter-TD memory isolation, isolation from host VMM, and
                                                                                                             hardware-protected measurement and reporting (e.g., via a QUOTE)
               (7) Verify
                                                                                                             of TD images. Since TD creation is managed by Adv-controlled
Figure 2: Desired property attestation for ML, in which Prv                                                  VMM, TDs are not inherently trusted. Hence, TDX supports attes-
interacts with an Initiator (Inr). Vrf requests evidence from Inr,                                           tation via QUOTE (see Section 2).
and may consult a Trusted Authority (Tru) to obtain reference                                                   We assume NVIDIA H100 GPU hardware is trusted, which mea-
values of a desired property.                                                                                sures and attests to its configuration (e.g., boot ROM, firmware, in
                                                                                                             confidential computing mode). By default, the interface between
                                                                                                             a GPU and the TD is not trusted; the GPU and all its memory are
                                                                                                             brought under the TD’s protection only when the GPU is directly
                                                                                                             assigned by the VMM [50]. This includes mapping its communica-
can then be used for verifiable ML property cards for transparency                                           tion buffers into TD shared memory. TD must obtain an attestation
(e.g., model card, datasheet, and inference card).                                                           token from the GPU to determine that the assigned device has the
                                                                                                             anticipated configuration.
                                                                                                                At run-time, Adv may attempt to obtain confidential data or
3      Problem Statement                                                                                     interfere with the execution of 𝑜𝑝 in a TD. Adv also may attempt
Our goal is to design a property attestation framework for genera-                                           to forge QUOTEs, either by learning the signing key or by tampering
tive models to prove to Vrf that a claimed property is (a) correctly                                         with relevant code/data without detection. We assume a Dolev-Yao
measured and (b) not false or manipulated.                                                                   Adv as it relates to the network (i.e., Adv carries the message).
   Unlike typical remote attestation, which is an interactive pro-                                           Therefore, Adv may attempt to inject or modify messages sent/re-
tocol between Vrf and Prv, ML property attestation must be non-                                              ceived by Prv. We consider denial-of-service attacks out of scope.
interactive with Vrf. We propose the protocol depicted in Figure 2.                                             Side channels are prevalent and can be exploited to leak keys [54,
Prv interacts with an initiator (Inr), who sends a request to Prv for                                        60, 64, 75, 82, 98]. To mitigate these attacks, additional mechanisms
a particular operation, along with other request-specific data (e.g.,                                        (e.g., constant-time software) can be added; as several works have
inputs or a challenge when freshness is required). Upon request, Inr                                         studied side-channel mitigations [20, 24, 51, 52, 95], we consider
makes them available for Vrf, who may consult Tru for property                                               these defenses as orthogonal to the focus of this paper. We also
reference values to verify the evidence.                                                                     consider physical attacks on hardware (e.g., interposing memory
                                                                                                             buses [18] and or physically swapping GPUs) as out of scope.
3.1       System Model
We consider Prv that trains, evaluates, or deploys a model M. We
consider software that is already executing within CVMs, as ML                                               3.3    Challenges and Requirements
companies today are exploring use of CVMs [6, 12, 71], and major                                             Prior works [23, 37, 74, 81, 86] demonstrate methods to attest ML
cloud service providers (e.g., Google Cloud and Microsoft Azure)                                             models using TEEs, but require operations to stay within the one
support TEE-aware GPUs [35, 63]. We consider Intel TDX and                                                   TEE. For example, Laminator [23] requires that all computations
NVIDIA H100 in this work, but our framework can be extended to                                               stay inside an SGX enclave to ensure integrity. However, this is
any CVM or TEE-aware GPU (see Appendix A).                                                                   not possible with reasonable performance of LLM operations. For
   Property attestations have the following components:                                                      example, large datasets may require datasets to reside in external
• Operation (𝑜𝑝): an ML-related computational task over inputs                                               storage during operation and require accelerators (e.g., GPUs or
   (I) to produce outputs (O).                                                                               NPUs) for reasonable performance (recall Section 2). Although it
• Property: an expression that describes the semantics of some                                               is possible to outsource computations from a TEE to a standard
   meaningful relationship between 𝑜𝑝, I, and O.                                                             GPU [53, 93], this adds significant overhead and would not preserve
• Attestation evidence: a verifiable claim that aims to prove                                                integrity of property measurements without additional measures.
   whether a property holds true.                                                                            Furthermore, no prior work defines properties of generative models
We assume an attestation mechanism on Prv executes 𝑜𝑝 and pro-                                               (e.g., from operations like fine-tuning, quantization, and chat ses-
duces attestation evidence. Obtaining attestation evidence requires                                          sions). Therefore, it is unclear how to perform property attestation
(1) measuring 𝑜𝑝, I, O and (2) reporting those measurements by                                               that is relevant for Vrf while protecting Prv’s confidential assets.
producing a cryptographic token (e.g., a digital signature) binding                                             Due to these challenges, prior work cannot apply to properties
them. For the latter, a signing key is used that must be accessible                                          of generative models, requiring another approach to address the
only to the attestation mechanism.                                                                           following concerns:
                                                                                                         3
Figure 3: High-level overview of PAL*M-enabled property attestation. Inr interacts with untrusted components of Prv, which
saves inputs to disk. PAL*M reads and measures inputs, runs the operations (including GPU), and measures all CPU and GPU
outputs. All measurements are extended to REPORTDATA, which is used to as input to obtain TDREPORT from TDX Module. Finally,
a QUOTE is generated by invoking the Quoting Enclave (QE) and returned to Inr.


(1) accounting for random sampling of large datasets from (un-             outputs and attestation measurements are obtained 5 . When a GPU
    trusted) external storage devices;                                     is used, the attestation measurements include a GPU-attestation
(2) handling operations that depend on both CPU and GPU with               token (𝐺𝑃𝑈𝑎𝑡𝑡 ).
    reasonable computational overhead;                                        After outputs are obtained, PAL*M TD leverages TDX mecha-
(3) defining how to measure properties of generative models in a           nisms to convert property attestation measurements into authenti-
    way that is relevant for Vrf and does not reveal Prv’s confiden-       cated evidence. As a first step, it invokes the TDX module in 6 to
    tial assets.                                                           generate an authenticated TDREPORT containing PAL*M attestation
   Based on these challenges, we consider the following require-           measurements. To complete the quote process, TDREPORT is passed
ments for designing PAL*M:                                                 to the VMM in 7 , which invokes the QE in 8 to convert TDREPORT
[R1] Efficient: low-overhead compared to confidential computing            into a QUOTE. Finally, QUOTE is returned to Inr in 9 . Inr will provide
       in the same environment;                                            QUOTE and outputs to requesting Vrf, who consults Tru (e.g., Intel
[R2] Secure: a malicious Prv cannot generate false attestations.           and NVIDIA) to perform evidence verification. Protocol details are
[R3] Scalable: supports large numbers of provers/verifiers;                described further in Section 4.4.
[R4] Versatile: supports a variety of properties; requires minimal            By design, PAL*M generates QUOTEs that attest to properties of
       effort for custom property measurement; can be ported to            generative model operations, while addressing key challenges:
       any CVM/TEE-based GPU configuration.                                (1) PAL*M leverages incremental multiset hash functions [19] to
                                                                               ensure large datasets are accurately reflected in attestation
4 PAL*M Design                                                                 evidence despite residing in untrusted external storage devices
4.1 Overview of PAL*M                                                          and being randomly sampled;
                                                                           (2) PAL*M ensures measurements of both CPU and GPU configu-
PAL*M enables Prv to attest properties of generative models through            rations are captured in attestation evidence for properties that
(1) design of a TD that effectively measures the operation corre-              depend on CPU and GPU.
sponding to a particular property and (2) use of attestation support          Building upon these capabilities, we show how to define, mea-
from Intel TDX and NVIDIA H100 to construct authenticated evi-             sure, and attest to properties of the following generative model
dence of these measurements. Figure 3 shows a high-level overview          operations (from Section 2.1):
of Prv’s workflow with PAL*M and the interaction with Inr.                 (1) dataset transformations and distributional statistics;
   In 1 , Inr requests a property attestation by specifying: (a) the       (2) model pretraining, optimization (e.g., fine-tuning, quantization),
requested operation (𝑜𝑝), (b) an attestation challenge (Chal), and             and evaluation;
any inputs that should be used (e.g., datasets, models, configura-         (3) model interactions (e.g., inference or chat sessions).
tion parameters, inference query). Upon receipt, Prv’s VMM saves
all data to disk. In 2 , inputs are fetched by PAL*M into TD mem-
ory according to the dataset access strategy (discussed further in         4.2    Dealing with Large Datasets
Section 4.2). Based on 𝑜𝑝, the corresponding function will start to        Given the large size of LLM training datasets, ML software frame-
execute in 3 . While executing, outputs will be obtained by a com-         works use two common approaches for efficient dataset handling:
bination of CPU execution 4a and GPU execution 4b . Operation              (1) loading the entire dataset in-memory or (2) accessing the dataset
                                                                       4
Figure 4: Depiction of PAL*M ’s handling of in-memory (left) and memory-mapped (right) dataset. In the in-memory approach,
the entire dataset is loaded and measured once at load time. In the memory-mapped approach, individual records are measured
when accessed using a multiset hash to ensure consistent measurements regardless of sampling order.


outside of TD protected memory with memory mapping. Although                 since it is insensitive to sampling order. Hence, instead of accumu-
in-memory has an advantage for integrity measurements, frame-                lating a record (𝑑𝑖 ) directly, we accumulate the concatenation of
works such as Hugging Face adopt and default to using memory-                each record with its index (𝑑𝑖 |𝑖). This approach makes it possible to
mapped datasets to minimize the memory footprint of large datasets           detect any reordering by Adv at run time, as the resulting MSH will
that cannot fit entirely into memory [44].                                   differ due to an index mismatch with the requested index.
    For accurate attestation, PAL*M must measure the dataset (or                We use the Mset-Mu-Hash multiplicative multiset hash construc-
its items) upon use, since Adv could tamper with data in external            tion (from Theorem 1 in [19]). Let 𝐵 denote a set of bit vectors of
storage at any time (recall Section 3.2). Figure 4 shows how PAL*M           length 𝑚, 𝑀 a multiset of elements of 𝐵, and 𝑀𝑏 be the number
handles this for in-memory and memory-mapped datasets.                       of times 𝑏 ∈ 𝐵 is in the multiset 𝑀. Let 𝑞 be a large prime power
    Case 1: In-memory Dataset. For integrity measurement, this               and consider computations in the field 𝐺𝐹 (𝑞). Then, let h be a poly-
is the ideal approach when sufficient TD memory is available. Since          random function performing h : 𝐵 → 𝐺𝐹 (𝑞) The multiplicative
                                                                             multiset hash MSH(𝑀) is defined as: MSH(𝑀) = 𝑏 ∈𝐵 h(𝑏) 𝑀𝑏
                                                                                                                               Î
the TD memory is protected, data within cannot be tampered. As
such, the dataset can be measured once during loading, as long as it            Compared to straightforward dataset hashing, this approach
stays in memory for the entire operation. As shown in Figure 4 (left),       incurs additional overhead due to iterative hash and modular opera-
our framework loads the entire dataset into memory, measures it,             tions based on the hardness of discrete logarithm problem, requiring
and uses it with the operation thereafter. Since one hash operation          a large prime. However, it ensures no other countermeasures are
is required, the overhead is minimal (discussed further in Section 6).       required to account for random sampling, as any permutation of
    Case 2: Memory-mapped Dataset. In contrast to the in-memory              the full set of dataset read operations will result in the same final
case, the dataset resides on the disk, and a virtual address mapping         MSH. We note that we chose to use the Mset-Mu-Hash construc-
is established in memory (see Figure 4: right). As records are sam-          tion due to its simplicity and widely available library support, but
pled, the OS reads just the requested items from disk into memory            any MSH construction could be used. For example, MSH construc-
on demand. Since the dataset stays on disk, it is vulnerable to tam-         tion based on elliptic curves can be used for more efficiency gains,
pering at run-time, resulting in inconsistencies between what is             but have other limitations (further details in Appendix B). Even
measured and what is used (i.e., TOCTOU attacks [11]).                       with Mset-Mu-Hash, overhead of MSH is negligible compared to
    To account for this, we measure each record at the time it is            computation-heavy ML tasks (shown in Section 6).
sampled, accumulating a measurement of the dataset in use. Since                It is possible that expected dataset measurement from Tru is
training algorithms often randomly sample records, a straightfor-            not MSH. Consequently, when memory-mapped datasets are in use,
ward approach (e.g., a hash chain over accessed records) would be            PAL*M must also enable methods for Vrf to trace back to original
unsuitable, as different sampling orders would result in different           dataset measurements.
measurements. Based on this insight, we employ an incremental
multiset hash (MSH) [19].                                                    4.3    Property Measurements for Large
    MSH is a cryptographic primitive that produces a fixed-size hash                Generative Models
over an unordered collection. It is suitable for settings in which
                                                                             Recall from Section 3.1 that obtaining property attestation evidence
the order of elements is irrelevant, but integrity and compactness
                                                                             requires (1) obtaining measurements of {𝑜𝑝, I, O} and (2) reporting
are required. By accumulating an MSH over the sampled records,
                                                                             those measurements by producing an authentication token. In this
PAL*M accurately measures the dataset that is used at run-time.
                                                                             section, we discuss the former.
Additionally, this approach has low memory overhead since one
                                                                                We categorize properties measured by PAL*M as one of the
multiset hash value is maintained.
                                                                             following based on 𝑜𝑝: dataset property, model property, model
    However, hashing records alone is insufficient if Adv can reorder
                                                                             interaction property. Based on this, we focus on the following com-
them at run-time. Such reordering may affect model characteristics
                                                                             ponents of property measurement (subset of those from Section 3.1):
(e.g., fairness [30]) while the resulting MSH would be unchanged,
                                                                             • Input (I): inputs (e.g., datasets, models, queries, or other param-
                                                                                eters) used by 𝑜𝑝.
                                                                         5
                                                                                             Definition 1: Preprocessing
                      Table 1: Notation Summary
                                                                                             Input (I): D
         Symbol       Definition                                                             Output (O): D𝑝𝑟𝑒
        I , O , 𝐴𝑡𝑡   Set of inputs, outputs, and attestation measurements                   Property: D𝑝𝑟𝑒 = PreProc( D )
           𝑃𝑑𝑖𝑠𝑡      Distributional property                                                Att. Measurement (𝐴𝑡𝑡 ): hD (D), hD (D𝑝𝑟𝑒 ), [𝐺𝑃𝑈𝑎𝑡𝑡 ] ∗
            MSH       Multiset hash function
             h        Standard cryptographic hash function (e.g., SHA3)
            hD        Dataset hash (either MSH or h based on memory man-                    for LLMs). We define attestation measurement for calculation of
                      agement strategy from Sec. 4.2)
        𝐺𝑃𝑈𝑎𝑡𝑡        Attestation token from TEE GPU                                        attribute distribution in Definition 2. For this operation, I contains
           D          Dataset                                                               D, and O contains an attribute distribution (𝐴𝑑𝑖𝑠𝑡 ). 𝐴𝑡𝑡, containing
       D𝑜𝑝𝑡 , D𝑡𝑒
                                                                                            h(𝐴𝑑𝑖𝑠𝑡 ) and h D (D), asserts the property that 𝐴𝑑𝑖𝑠𝑡 was obtained
                      optimization dataset, test dataset
          D𝑡𝑟         Training dataset
         D𝑝𝑟𝑒         Preprocessed dataset                                                  by an algorithm (Dist) that computes D’s attribute distribution.
         M𝑎𝑟          Model architecture
            T         Training configuration                                                 Definition 2: Attribute Distribution
           M          Model
         M𝑡𝑜𝑘         Tokenizer                                                              Input (I): D
         𝑖𝑑𝑜𝑝𝑡        Optimization type                                                      Output (O): 𝐴𝑑𝑖𝑠𝑡
         M𝑎𝑑𝑝         Adapter model
         D𝑜𝑝𝑡         Optimization dataset                                                   Property: 𝐴𝑑𝑖𝑠𝑡 = Dist( D)
          [ · ]∗      Optional components                                                    Att. Measurement (𝐴𝑡𝑡 ): h(𝐴𝑑𝑖𝑠𝑡 ), hD (D), [𝐺𝑃𝑈𝑎𝑡𝑡 ] ∗
        𝑚𝑒𝑡𝑟𝑖𝑐        Evaluation metric
         𝑞𝑖 , 𝑟 𝑖     The 𝑖 -th inference query and response                                  It is possible that reference values offered by Tru are produced
           H          Session history (i.e., set of all query-response pairs
                      [(𝑞 0 , 𝑟 0 ), ... , (𝑞𝑖 −1 , 𝑟𝑖 −1 ) ]) that are used as addi-       by h while an operation requires memory-mapping, resulting in a
                      tional context to produce 𝑞𝑖 for 𝑟𝑖                                   measurement based on MSH. To account for this scenario, PAL*M
                                                                                            supports measurement binding defined in Definition 3.
• Output (O): outputs (e.g., prompt response, model, or dataset)                             Definition 3: Measurement Binding
  produced by 𝑜𝑝.
                                                                                             Input (I): D,
• Property: an expression that describes semantics (either nat-                              Output (O): h(D), MSH(D)
  ural language or mathematical expression) of the relationship                              Property: h(D) and MSH(D) were produced from D
  between {𝑜𝑝, I, O}.                                                                        Att. Measurement (𝐴𝑡𝑡 ): h(h( D ) | |MSH( D ) ), [𝐺𝑃𝑈𝑎𝑡𝑡 ] ∗
• Attestation Measurement (𝐴𝑡𝑡): Measurements that reflect the
  property under the adversary model (from Section 3.2).                                      For measurement binding, I contains D, and O contains the
A summary of frequent notation in this section is in Table 1.                               measurements of D that should be bound: h(D) and MSH(D). A
                                                                                            property that h(D) and MSH(D) were produced from the same
4.3.1 GPU Attestation. For all operations that require GPU, 𝐴𝑡𝑡                             dataset is asserted through 𝐴𝑡𝑡 containing h(h(D)||MSH(D)).
must include 𝐺𝑃𝑈𝑎𝑡𝑡 to reflect the complete environment (i.e., GPU
driver, firmware/VBIOS, and other configurations) in which the                              4.3.3 Model Properties. We present model properties related to
computations were performed. Therefore, 𝐺𝑃𝑈𝑎𝑡𝑡 is included as an                            training and evaluation. Among model training operations, we con-
optional input (denoted with [·] ∗ ) for all operations described in this                   sider model training itself and post-training model optimizations.
section. Beyond obtaining 𝐺𝑃𝑈𝑎𝑡𝑡 , a secure channel must be estab-                             Training Properties. First, we consider training by building on
lished prior to any operation. This is achieved through SPDM-based                          prior work [23]. We define attestation measurements for training
session key exchange during the TD instantiation [36, 70], which                            in Definition 4. For training, I includes the specified model archi-
cryptographically binds all subsequent run-time interactions to the                         tecture (M𝑎𝑟 ), training dataset (D𝑡𝑟 ), training configuration (T ),
attested GPU instance. The session establishment is also included in                        which specifies hyperparameters, and a tokenizer (M𝑡𝑜𝑘 ). Then, O
the CVM’s attestation (i.e., the QUOTE). Together, 𝐺𝑃𝑈𝑎𝑡𝑡 and SPDM                          contains the trained model (M𝑡𝑟 ). 𝐴𝑡𝑡 contains measurements of
session ensure that the GPU in use is a legitimate confidential GPU                         (T , M𝑎𝑟 , M𝑡𝑟 , M𝑡𝑜𝑘 ) using h and D using h D , asserting a property
and that it remains so throughout the operation.                                            describing that M𝑡𝑟 was obtained by a training algorithm (Train)
                                                                                            taking D𝑡𝑟 , T , M𝑎𝑟 , M𝑡𝑜𝑘 .
4.3.2 Dataset Properties. We discuss dataset properties based on
the following operations: dataset preprocessing, calculation of dataset                      Definition 4: Training
attribute distribution, and dataset measurement binding.                                     Input (I): M𝑎𝑟 , D𝑡𝑟 , T, M𝑡𝑜𝑘
   Dataset preprocessing (from Section 2) may occur prior to train-                          Output (O): M𝑡𝑟
                                                                                             Property: M𝑡𝑟 = Train( D𝑡𝑟 , T, M𝑎𝑟 )
ing or inference. We define attestation measurement for preprocess-
                                                                                             Att. Measurement (𝐴𝑡𝑡 ): h( M𝑡𝑟 ), h( M𝑎𝑟 ), hD ( D𝑡𝑟 ), h( T ),
ing in Definition 1. For preprocessing, I contains an input dataset                          h( M𝑡𝑜𝑘 ), [𝐺𝑃𝑈𝑎𝑡𝑡 ] ∗
(D) and O contains an output preprocessed dataset (D𝑝𝑟𝑒 ). A prop-
erty measurement of preprocessing asserts that D𝑝𝑟𝑒 was the result                              Definition 5 defines attestation measurements for post-training
of computing a preprocessing algorithm (PreProc) on D. Finally,                             model optimizations (e.g., fine-tuning, quantization, pruning). For
𝐴𝑡𝑡 contains measurements of D and D𝑝𝑟𝑒 using the dataset hash                              model optimization, I contains the following required inputs: M,
function (h D ): either a standard cryptographic hash function (h) or                       T , M𝑡𝑜𝑘 , and the optimization type (𝑖𝑑𝑜𝑝𝑡 ). Optional components
a MSH, based on whether D and D𝑝𝑟𝑒 are in-memory or memory                                  of I include a base adapter layer (M𝑎𝑑𝑝 ) and additional datasets
mapped, respectively.                                                                       (D𝑜𝑝𝑡 ). For this operation, O contains the optimized model (M𝑜𝑝𝑡 ).
   Dataset attribute distribution calculations [22] reflect a distribu-                     𝐴𝑡𝑡 contains all components of I and O using h and h D , reflecting
tion of an attribute across a dataset (e.g., word lengths/frequency                         its assertion that:
                                                                                        6
• Opt is selected from a set of known optimization functions (F𝑜𝑝𝑡 )              4.4    From Measurement to Attestation
  based on 𝑖𝑑𝑜𝑝𝑡 ;                                                                For each 𝑜𝑝, the corresponding components of 𝐴𝑡𝑡, as defined in
• M𝑜𝑝𝑡 is the result of Opt taking all components of I.                           Section 4.3, are used to construct property attestation evidence. We
 Definition 5: Weight Optimizations                                               refer to each property attestation as proof of <𝑜𝑝>. A table of opera-
 Input (I): M, M𝑡𝑜𝑘 , T, 𝑖𝑑𝑜𝑝𝑡 , [ M𝑎𝑑𝑝 , D𝑜𝑝𝑡 ] ∗                                tions and resulting property attestations is shown in Appendix C.
 Outputs (O): M𝑜𝑝𝑡                                                                In this section, we describe how PAL*M interacts with other system
 Property: Opt = F𝑜𝑝𝑡𝑠 [𝑖𝑑𝑜𝑝𝑡 ]                                                   components and leverages Intel TDX features to respond to Inr
 M𝑜𝑝𝑡 = Opt( M, M𝑡𝑜𝑘 , T, [ M𝑎𝑑𝑝 , D𝑜𝑝𝑡 ] ∗ )                                     requests with property attestation evidence.
 Att. Measurement (𝐴𝑡𝑡 ): h( M𝑜𝑝𝑡 ), h( M ), h( M𝑡𝑜𝑘 ), h( T), h(𝑖𝑑𝑜𝑝𝑡 ),            Figure 5 shows the property attestation protocol enabled by
 [𝐺𝑃𝑈𝑎𝑡𝑡 , h( M𝑎𝑑𝑝 ), hD ( D𝑜𝑝𝑡 ) ] ∗                                             PAL*M. Here, we describe the interactions between Inr and Prv
   Evaluation Properties. As described in Section 2, generative                   containing a VMM (including QE), TDX module, and PAL*M-based
models have various benchmarks to produce metrics reflecting a                    TD. We note there are several possible interactions between Inr and
model’s effectiveness according to a particular criteria. Attestation             Vrf (e.g., Inr publishes attestations to a transparency log [37, 86]).
measurement for model evaluation is defined in Definition 6. For                  We discuss implications of alternative strategies in Appendix A.
model evaluation, I includes M, M𝑡𝑜𝑘 , and a test dataset (D𝑡𝑒 ),                    In an offline phase, Prv initializes and measures the PAL*M TD.
while O contains the evaluation metric. Measurements of M and                     In step (1), VMM specifies the TD image that should be used. In
M𝑡𝑜𝑘 using h and D𝑡𝑒 using h D in 𝐴𝑡𝑡 assert a property about the                 step (2), the Intel TDX architecture and TDX module measure the
evaluation: that metric was produced by an evaluation operation                   TD image into ℎ𝑇 𝐷 and launch it.
(Eval) taking M, M𝑡𝑜𝑘 , and D𝑡𝑒 .                                                    After initialization, the online protocol can begin. In step (1), Inr
                                                                                  sends a property attestation request to Prv containing 𝑜𝑝, an attes-
 Definition 6: Evaluation
                                                                                  tation challenge (Chal), and a set of input assets (I). For large input
 Input (I): M, M𝑡𝑜𝑘 , D𝑡𝑒                                                         assets (e.g., datasets or models), Inr’s request may specify reposito-
 Output (O): 𝑚𝑒𝑡𝑟𝑖𝑐
                                                                                  ries from which Prv should download them. Or, Inr’s request may
 Property: 𝑚𝑒𝑡𝑟𝑖𝑐 ← Eval( M, M𝑡𝑜𝑘 , D𝑡𝑒 )
                                                                                  specify that Prv use a dataset/model owned by Prv. Regardless of
 Att. Measurement (𝐴𝑡𝑡 ): h( M ), h( M𝑡𝑜𝑘 ), hD ( D𝑡𝑒 ),
 h(𝑚𝑒𝑡𝑟𝑖𝑐 ), [𝐺𝑃𝑈𝑎𝑡𝑡 ] ∗                                                          these specificities, Prv saves all data from the request to disk in
                                                                                  step (2) upon receipt. In step (3), the PAL*M TD imports request
4.3.4 Inference-time Properties. We consider two cases of inference-              data and all data required for 𝑜𝑝 into its memory. Datasets are im-
time properties which includes interactions between client and                    ported depending on whether Prv is using a memory-mapped or
model: one prompt-response inference and a chat session of multi-                 an in-memory dataset (from Section 4.2).
ple prompt-response inference pairs.                                                 PAL*M TD reads 𝑜𝑝 to execute in step (4). During execution, it
   Attestation measurements for a single inference are defined in                 obtains a set of input measurements (HI ). After completing the
Definition 7. An inference query (𝑞) is one component of I along                  operation, PAL*M will obtain a set of outputs (O) and correspond-
with M and M𝑡𝑜𝑘 , while the O contains the inference response (𝑟 ).               ing measurements (H O ) in step (5). HI and H O correspond to
Measurements of 𝑞, M, M𝑡𝑜𝑘 , and 𝑟 using h assert the property                    components of 𝐴𝑡𝑡 for each 𝑜𝑝 described in Section 4.3.
that 𝑞 was obtained by passing 𝑟 first through M𝑡𝑜𝑘 and then M.                      Next, PAL*M prepares the request for TDREPORT generation in
                                                                                  step (6). To do so, it assigns REPORTDATA input used in TDREPORT
 Definition 7: Single Inference                                                   generation (recall Section 2.2) as the concatenation of the following
 Input (I): 𝑞, M, M𝑡𝑜𝑘                                                            data: {𝑜𝑝, Chal, HI , H O }. Upon receiving REPORTDATA, the TDX
 Output (O): 𝑟                                                                    module will create a TDREPORT in step (7) by invoking the CPU.
 Property: 𝑟 = M ( M𝑡𝑜𝑘 (𝑞) )
                                                                                  During this step, the CPU will compute a MAC over ℎ𝑇 𝐷 , measure-
 Att. Measurement (𝐴𝑡𝑡 ): h(𝑞), h(M), h(M𝑡𝑜𝑘 ), h(𝑟 ), [𝐺𝑃𝑈𝑎𝑡𝑡 ] ∗
                                                                                  ments of the TDX module, and all data extended into REPORTDATA
   Attestation measurements reflecting the influence of a chat ses-               by PAL*M. In step (8), the MAC-ed TDREPORT is passed to VMM,
sion on a query-response (i.e., a session inference) are defined in               who passes it to QE in step (9). Upon receipt, QE:
Definition 8. For a session inference operation, I contains the same              • verifies the MAC on TDREPORT is valid, to ensure VMM did not
data as the single inference operation, while O contains 𝑟 and the                   tamper with TDREPORT it received from the TDX Module;
chat session history (H ): a sequential list of all (𝑞𝑖 , 𝑟𝑖 ) pairs of the       • uses TDREPORT to produce the QUOTE containing all measure-
current chat session, including (𝑞, 𝑟 ). Measurements of 𝑟 , H , 𝑞,                  ments from TDREPORT plus a signature (𝑠𝑖𝑔).
M𝑡𝑜𝑘 , and M using h assert the property that 𝑟 was obtained from                 In step (10), Prv sends QUOTE and optionally O (if it is not confiden-
passing 𝑞 prepended with H without (𝑞, 𝑟 ) through M𝑡𝑜𝑘 , followed                tial) to Inr, who sends them to Vrf in step (11).
by passing that result through M.                                                    Upon receiving QUOTE and (optionally O) from Inr, Vrf parses the
 Definition 8: Session Inference                                                  response to perform verification. First, it checks sig to determine
 Input (I): 𝑞, M𝑡𝑜𝑘 , M
                                                                                  whether QUOTE came from Prv. Next, it checks Chal to determine
 Output (O): 𝑟 , H                                                                the freshness of the response. The type of Chal that is effective
 Property: 𝑟 = M ( M𝑡𝑜𝑘 ( H \ [𝑞, 𝑟 ] | | 𝑞) )                                    depends on the operation (discussed further in Appendix A).
 Att. Measurement (𝐴𝑡𝑡 ): h(𝑞), h( M𝑡𝑜𝑘 ), h( M ), h(𝑟 ), h( H),                     Assuming both checks pass, Vrf continues to inspect the mea-
 [𝐺𝑃𝑈𝑎𝑡𝑡 ] ∗                                                                      surements of the TD image, TDX module image, and 𝐺𝑃𝑈𝑎𝑡𝑡 (by

                                                                              7
                                                                                                     Prv
                           Inr                          VMM (Quoting Enclave)                    TDX Module                               PAL*M TD



                                                                         (1) Specify TD image
                                                                          Invoke TD creation                  (2) Measure TD image into
                                                                                                              ℎ𝑇 𝐷 and launch TD

                                 (1) Send: { I, 𝑜𝑝, Chal }
                                                                   (2) Saves to disk
                                                                           (3) Import I, 𝑜𝑝, Chal                                              (4) Execute function for
                                                                                                                                               𝑜𝑝 , obtain HI
                                                                                                                                               (5) Produce O and HO

                                                                                                                                               (6) Request TDREPORT
                                                                                                                                               generation with
                                                                                                           (7) Calls CPU to create             REPORTDATA = {𝑜𝑝, Chal, HI , HO }
                                                                                                           MAC-ed TDREPORT
                                                                    (8) Pass MAC-ed
                                                                    TDREPORT to QE
                                                                   (9) QE validates MAC
                                 (10) Send QUOTE, [ O ] ∗
                                                                   and signs QUOTE
    (11) Make signature,
       measurements,
      and PAL*M data
       available to Vrf


Figure 5: PAL*M Property Attestation Protocol between Inr and Prv . Inr sends request to Prv containing untrusted VMM,
Quoting Enclave, trusted TDX Module, and attested PAL*M TD. Prv responds after performing the requested operation,
measuring relevant inputs and ouputs, and generating both a TDREPORT and QUOTE.


obtaining reference values from Intel and NVIDIA). Assuming this                                • WMT14(DE - EN) [9]: a test set of WMT14 German-English to
passes, Vrf continues to inspecting HI , H O , and O. If O was sent                                evaluate LLM translation capability. This dataset is used to cal-
to Vrf, it checks whether H O corresponds to O. Finally, Vrf inspects                              culate the BLEU score for our proof of evaluation experiment.
HI and H O , consulting reference values from Tru as needed, to                                 • CoQA [76]: a conversational Q&A dataset containing stories with
determine if the desired property related to 𝑜𝑝 is upheld.                                         context-dependent Q&A. For proof of inference, we select the
   Like prior work [23], property attestations introduced in this                                  first question of the first ten records. For the proof of session
work can be used to construct chains of attestations, enabling veri-                               inference, we use all ten records and select the first five questions
fiers to derive composite guarantees spanning the full ML life-cycle.                              from each, simulating a session with 50 prompts.
For example, combining a proof of fine-tuning (attesting that M𝑜𝑝𝑡                                 For models, we use GPT-2 [73] (124M parameters; 0.46 GB) for
was fine-tuned on D𝑜𝑝𝑡 that was preprocessed with 𝑃𝑟𝑒𝑃𝑟𝑜𝑐 (D𝑜𝑝𝑡 )                               proof of training. For fine-tuning, inference, and evaluation, we use
algorithm) with proof of inference (attesting that M𝑜𝑝𝑡 produces                                three popular instruction-tuned LLMs:
O with an inference query 𝑞).                                                                         • Llama-3.1-8B [91] (8B parameters, 15 GB),
                                                                                                      • Gemma-3-4B [90] (4B parameters, 8 GB), and
                                                                                                      • Phi-4-Mini [2] (3.8B parameters; 7.15 GB).
5 Experiment Setup                                                                              We choose Llama-3.1-8B for its 8 billion parameters, while both
                                                                                                Gemma-3-4B and Phi-4-Mini have ≈4 billion parameters, allowing
5.1 Datasets, Models, and Metrics                                                               us to show how the overhead of PAL*M varies across different
We use the following datasets in our experiments:                                               model sizes and architectures. To demonstrate a realistic fine-tuning
• BookCorpus [103]: a collection of 74 million unpublished novels.                              workflow, we fine-tune all three models at full precision using
  We use the full BookCorpus dataset for proof of training and                                  LoRA [41]. For quantization, we focus on Llama-3.1-8B.
  attribute distribution, while for proof of preprocessing and proof                               We use the following metrics to capture both the overall overhead
  of binding, we use a 1/100 subset to reduce experiment running                                from PAL*M and the main sources of overhead:
  time. For training, we preprocess the full BookCorpus dataset by                              • Total Time: the total execution time spent on the task.
  tokenizing and concatenating text into sequences of 1024 tokens.                              • Baseline: the execution time on a TDX-enabled machine without
• yahma/alpaca-cleaned [89]: a instruction-following dataset                                       measurement from PAL*M. We omit a non-TDX baseline, as prior
  containing over 52,000 instruction-response pairs aimed at im-                                   work has evaluated the overhead of TDX itself [17].
  proving model alignment. We use this dataset for proof of fine-                               • Memory Usage: total memory usage by the dataset.
  tuning to provide a dataset variety other than BookCorpus.                                    • Raw Measurement Time: time spent purely hashing inputs
• MMLU [39]: a multiple-choice question-and-answer (Q&A) dataset                                   and outputs (with h or MSH).
  covering 57 fields. It is widely used to assess general-purpose                               • Attestation: The time spent by Intel TDX and NVIDIA H100 to
  intelligence in language models. We use all 57 fields for our proof                              produce QUOTE and 𝐺𝑃𝑈𝑎𝑡𝑡 , respectively.
  of evaluation experiments.
                                                                                          8
Table 2: Performance for proofs of dataset attribute distribution and prepro-
cessing using BookCorpus (Full) and BookCorpus (1/100).                       Table 3: Performance for proof of training
                                                                              with GPT-2 on preprocessed BookCorpus.
   Proof of                          Attribute Distribution                    Preprocessing
                                                                                                          Dataset                             BookCorpus (Full)
   Dataset                                 BookCorpus (Full)                 BookCorpus (1/100)
                                                                                                          Memory Variant                In-memory    Memory-mapped
   Memory Variant                In-memory        Memory-mapped    In-memory         Memory-mapped
                                                                                                          Total Time                    401.65 min      425.03 min
   Total Time                    339.16 min           576.97 min    237.70 s              378.62 s
                                                                                                          Baseline                      401.60 min      401.20 min
   Baseline                      339.09 min           331.73 min    236.66 s              236.12 s
   Mem Usage (GB)                   5.47                 4.33         0.12                  0.04
                                                                                                          Mem Usage (GB)                   2.74            0.04

   Raw Meas.                       3.06 s             392.68 min     0.04 s               236.06 s        Raw Meas.                       2.27 s         23.86 min
   Attestation                     1.06 s                0.80 s      0.90 s                0.79 s         Attestation                     1.11 s           0.96 s

   Raw Meas. Overhead (%)          0.015                 68.06        0.06                 62.35          Raw Meas. Overhead (%)          0.009            5.47
   Att. Overhead (%)               0.0052               0.0023        0.38                  0.21          Att. Overhead (%)               0.005            0.006
   Total Observed Overhead (%)     0.021                 42.50        0.44                 37.64          Total Observed Overhead (%)     0.014            5.61



• Raw Measurement Overhead (%): The total raw measurement                                  6 Evaluation
  overhead from PAL*M as a percentage of the total time.
                                                                                           6.1 Performance Analysis
• Attestation Overhead (%): The total attestation overhead from
  PAL*M as a percentage of the total time.                                                 Tables 2–6 show the timing results for the performance evaluations.
• Total Observed Overhead (%): The overall observed overhead                               The cells in gray represent the baseline, PAL*M’s overhead is high-
  as a percentage when comparing the total execution time of                               lighted in blue , and the total times are in orange . We parallelize
  PAL*M to the baseline.                                                                   the dataset lookup across 8 workers for dataset-related attestations
                                                                                           requiring manual dataset iteration.
                                                                                           6.1.1 Dataset Attestations. Table 2 presents the results for proof of
                                                                                           attribute distribution and proof of preprocessing. Both operations
                                                                                           process the dataset using 8 parallel workers (i.e., vCPU cores). In
                                                                                           the memory-mapped setting, parallel I/O can scale better with the
                                                                                           memory-mapped approach, as all processes can directly access the
5.2    Prototype Configuration                                                             same underlying memory pages without duplication.
The prototype of PAL*M’s TD is configured with 32 vCPUs and 128                               As a result, the raw overhead (i.e., MSH overhead per core) differs
GB of memory, running Ubuntu 24.04.1 LTS with kernel version                               from the observed end-to-end overhead of the parallelized opera-
6.8.0-86-generic [15]. The host has an Intel Xeon Silver 4514Y CPU,                        tion. The latter can be lower due to DataLoader prefetching [72] or
512 GB of RAM, and an NVIDIA H100 NVL 94 GB GPU with confi-                                higher due to pipeline delays [7, 100]. For example, raw overhead
dential compute mode enabled [68]. We assign the GPU directly to                           from MSH operations of 62.35–68.06% results in 37.64–42.50% total
the TD using Direct Device Assignment to give the TD exclusive                             observed overhead in the end-to-end parallelized operation.
access. We run each experiment five times and report the average.                             Despite the reduction in this case, the observed overhead remains
Standard deviation is excluded as it was negligible.                                       high because MSH requires modular exponentiation and multipli-
   PAL*M is measurement/attestation is implemented in Python. At-                          cation over a 2048-bit prime for each record. Since dataset-level
testation uses Intel Data Center Attestation Primitives (DCAP) [80]                        operations are inexpensive on per-record basis compared to others
and NVIDIA Remote Attestation Service (NRAS) [69]. PAL*M is                                (e.g., fine-tuning, evaluation), even modest MSH costs dominate the
built on PyTorch and the Hugging Face Datasets framework, allow-                           run-time. We analyze this effect further in Section 6.1.4. Fortunately,
ing access to dataset and model internals for measurement. We use                          these costs can be amortized across future dataset use. For example:
SHA-256 as the underlying hash function for normal hashing and                             • proof of attribute distribution and preprocessing apply to all
MSH. We use a 2048-bit prime for MSH. For attestation, we use Intel                           future uses of a dataset;
DCAP to generate QUOTE and NRAS to verify 𝐺𝑃𝑈𝑎𝑡𝑡 . We also use                             • proof of binding applies to any future dataset MSH.
the following operation-specific frameworks for the experiments:                           For the 1/100 subset of BookCorpus dataset used in our evaluation,
• Unsloth [21]: an open-source framework for optimized LLM                                 proof of binding takes 337.5 seconds (3.65 ms per record).
  fine-tuning. We use it for proof of fine-tuning experiment.
                                                                                           6.1.2 Model Attestations. In contrast to dataset attestations, the
• AutoAWQ framework [38]: implements the Activation-aware
                                                                                           measurement overhead of PAL*M for proof of training is low. For
  Weight Quantization (AWQ) algorithm for quantizing LLMs. We
                                                                                           the memory-mapped case, the raw measurement overhead is only
  use it for proof of quantization experiment.
                                                                                           5.47% of the total time, whereas for the in-memory case, it is 0.009%;
• lm-evaluation-harness framework [32]: standardized toolkit
                                                                                           this results in an observed overhead of 5.61% for memory-mapped
  that runs LLMs on multiple benchmark tasks through a uni-
                                                                                           and 0.014% for in-memory case (Table 3). LLM training is compu-
  fied API to produce comparable scores. We use it for proof of
                                                                                           tationally expensive; hence, the measurement time introduces a
  evaluation, specifically evaluating the model with MMLU.
                                                                                           proportionally smaller overhead.
                                                                                      9
                          Table 4: Performance for proof of model optimization (fine-tuning and quantization).

  Proof of                                                                                           Fine-tuning                                                                  Quantization

  Model                                    Llama-3.1-8B                                      Gemma-3-4B                                      Phi-4-Mini                           Llama-3.1-8B
  Memory Variant                    In-memory   Memory-mapped                        In-memory   Memory-mapped                       In-memory   Memory-mapped                        N/A

  Total Time                            268.81 min           261.74 min              325.61 min              369.56 min               169.93 min              170.48 min                 812.92 s
  Baseline                              268.30 min           258.07 min              325.29 min              361.82 min               169.65 min              168.16 min                 773.84 s
  Mem Usage (GB)                          0.085                0.004                   0.087                   0.004                    0.088                   0.004                      N/A
  Raw Meas.                               28.76 s              132.87 s                17.93 s                    129.40 s              15.83 s                127.99 s                  28.16 s
  Attestation                              1.11 s               1.44 s                 1.00 s                      1.20 s               1.00 s                  0.84 s                    0.92 s
  Raw Meas. Overhead (%)                  0.18                  0.85                   0.09                        0.58                  0.16                    1.20                     4.70
  Att. Overhead (%)                       0.007                 0.009                  0.005                       0.005                 0.010                  0.008                     0.117
  Total Observed Overhead (%)             0.19                  1.40                   0.10                        2.09                  0.17                    2.27                     4.81


                Table 5: Performance for proof of evaluation based on MMLU and BLEU score with WMT14(DE-EN) dataset.
 Model                                              Llama-3.1-8B                                             Gemma-3-4B                                                 Phi-4-Mini
 Memory Variant                    In-memory                Memory-mapped                  In-memory                       Memory-mapped               In-memory               Memory-mapped
 Metric                         MMLU          BLEU          MMLU          BLEU          MMLU             BLEU              MMLU        BLEU         MMLU          BLEU         MMLU           BLEU
 Total Time                    7.93 min     121.71 min     8.78 min     121.55 min    13.27 min        242.23 min      14.41 min     241.53 min    8.47 min     119.03 min    9.39 min      118.65 min
 Baseline                      7.73 min     121.23 min     7.80 min     120.94 min    13.15 min        241.92 min      13.30 min     241.10 min    8.35 min     118.75 min    8.43 min      118.26 min
 Mem Usage (GB)                 0.028          0.001        0.013         0.001         0.022            0.001             0.008       0.001        0.025         0.001        0.009           0.001
 Raw Meas.                     10.13 s        28.16 s       74.59 s       35.57 s       6.33 s           17.32 s           70.72 s    24.55 s       5.66 s        15.65 s      70.06 s        22.50 s
 Attestation                    1.58 s         1.10 s       0.85 s        1.07 s        1.09 s           1.12 s            0.87 s      1.23 s       1.35 s        1.08 s       0.92 s          1.13 s
 Raw Meas. Overhead (%)          2.13           0.39        14.16          0.49          0.79             0.12               8.18       0.17         1.11          0.22        12.43              0.31
 Att. Overhead (%)               0.33          0.015         0.16         0.015          0.13            0.008               0.10      0.009         0.27         0.015         0.16           0.016
 Total Observed Overhead (%)     2.46           0.40        11.24          0.50          0.93             0.13               7.69       0.17         1.38          0.23        10.28              0.31



   For model optimization, proof of fine-tuning (Table 4) also shows                                   6.1.4 Measurement overhead of memory-mapped operations. Ta-
minimal overhead for both raw and observed of ≤2.27% across all                                        ble 7 compares per-record computation time with the MSH con-
models, plus a substantial reduction in memory usage from 85-87                                        struction time (i.e., input measurement) for operations that use
MB for the in-memory dataset to only 4 MB for the memory-mapped                                        a memory-mapped dataset. Normalizing per record shows that
dataset. For proof of quantization, since no dataset is involved, the                                  dataset-related operations are much more lightweight than model-
4.7% raw measurement overhead comes from measuring models.                                             related operations. In contrast, input measurement time per record
   As shown in Table 5, the observed overhead of proof of evaluation                                   remains nearly constant (≈2.29–2.57 ms), as it is independent of
with MMLU is dominated by the measurement overhead; the observed                                       the operation type. Consequently, relative measurement overhead
overheads are 0.93-2.46% for the in-memory case and 7.69-11.24% for                                    is higher for operations with lower computational cost, despite the
the memory-mapped case (Table 5). For BLEU score, since dataset                                        near-constant per-record measurement time. Due to the low over-
access is limited (WMT14(DE-EN) contains only 3003 records), the                                       head for common operations (training, fine-tuning, quantization,
raw overhead of performing MSH in the memory-mapped case is                                            evaluation, session inference), PAL*M satisfies R1.
comparable to hashing the dataset in the in-memory case, with
both the raw and observed overheads remaining ≤ 0.5% across
                                                                                                       6.2         Security Analysis
all models. Unlike dataset operations, total observed overhead for
model operations is often higher than raw measurement overhead,                                        PAL*M aims to uphold integrity of its property attestation evidence
likely due to pipeline stalls when transferring data to GPU.                                           in the presence of Adv, as defined in Section 3, who controls the
                                                                                                       host machine, including the VMM and disk. Based on this, the
6.1.3 Inference Attestations. Table 6 presents the results for both                                    following security properties are desired:
proof of inference and proof of session inference. Proof of inference                                    [P1] integrity of the operation (the set of HI and H O correspond
follows the same pattern observed in dataset attestations, where                                               to the expected I, O, according to the requested 𝑜𝑝).
the overhead appears large (64.34% for Llama-3.1-8B, 43.28% for                                          [P2] integrity of environment and responses (ℎ𝑇 𝐷 , 𝑜𝑝, HI , and
Gemma-3-4B, and 52.16% for Phi-4-Mini) because the underlying                                                  H O in QUOTE correspond to the expected TD image, I, op,
computation is relatively small. This represents an uncommon case                                              and O, respectively);
in which a proof is generated for only one prompt. On the other                                          [P3] authenticity of attestation responses (any QUOTE that passes
hand, proof of session inference simulates a more realistic user-                                              verification was produced through the expected QE, and
model interaction. In this setting, the measurement overhead is sig-                                           TDREPORT was not forged); and
nificantly smaller: 11.03% for Llama-3.1-8B, 3.57% for Gemma-3-4B,                                     In order to violate these security properties, Adv attempts to (1)
and 6.28% for Phi-4-Mini.                                                                              tamper with any operation inputs; (2) tamper with, discard, or
                                                                                                10
 Table 6: Performance of proof of inference for one query-response and proof of session inference for 50 query-responses.

                 Model                                    Llama-3.1-8B                              Gemma-3-4B                  Phi-4-Mini
                 Proof of Inference Type              Single        Session                   Single         Session      Single         Session

                 Total Time                           43.31 s              256.19 s           40.55 s       489.69 s      29.94 s       249.37 s
                 Baseline                             14.54 s              227.02 s           22.09 s       471.22 s      13.40 s       232.70 s
                 Mem Usage (GB)                        0.001                0.001              0.001         0.001         0.001         0.001
                 Raw Meas.                            27.17 s              28.25 s            16.27 s        17.47 s      14.59 s        15.66 s
                 Attestation                           0.75 s              0.92 s             0.79 s          0.99 s      0.71 s         1.01 s
                 Raw Meas. Overhead (%)               64.34                 11.03             43.28           3.57        52.16           6.28
                 Att. Overhead (%)                    2.09                  0.36               2.24           0.20        3.10            0.41
                 Total Observed Overhead (%)          66.43                 11.39             45.52           3.77        55.26           6.69



Table 7: Records per workers (R/W), compute time per record                                   Adv may attempt to generate false outputs and correspond-
(C/R), and raw input measurement time per record (I/R) for                                 ing measurements in an attempt to create a faulty TDREPORT be-
memory-mapped operations. I/R remains roughly constant                                     fore it is passed to the QE. PAL*M relies on the standard TDX
across operations, while C/R varies significantly, indicating                              attestation guarantees discussed in Section 2 that (a) TDREPORT au-
that raw measurement overhead is higher when C/R is low.                                   thenticity is protected by MAC under a hardware-protected key
                                                                 Raw Meas.                 inaccessible to software [4] and (b) the QE verifies this MAC prior
 Operation                      R/W      C/R (ms) I/R (ms)
                                                                                           to the QUOTE generation. Consequently, Adv cannot forge a valid
                    Model                                       Overhead (%)
 Training            GPT2       572.2k     43.07    2.44            5.47                   TDREPORT without access to the device key, and QUOTE forgery is
 Fine-tuning     Llama-3.1-8B   51.8k      311.1    2.36            0.84                   infeasible because each QUOTE is signed using a provisioned attes-
 Fine-tuning      Gemma-3-4B    51.8k      376.3    2.38            0.58                   tation key whose private material never leaves QE. PAL*M only
 Fine-tuning      Phi-4-Mini    51.8k      196.9    2.36            1.20                   extends data into REPORTDATA of the TDREPORT. Since material ex-
 Eval. (MMLU)    Llama-3.1-8B   28.1k       40.5    2.29           14.15                   tended into REPORTDATA by PAL*M is independent of keys, and
 Eval. (MMLU)     Gemma-3-4B    28.1k       33.8    2.29           8.17                    PAL*M does not influence any other step the QUOTE generation
 Eval. (MMLU)     Phi-4-Mini    28.1k       27.4    2.29           12.43                   pipeline, the integrity/authentication guarantees of Intel TDX at-
 Eval. (BLEU)    Llama-3.1-8B    3.0k       2416    2.34            0.45                   testation remain unchanged. Adv may attempt to replay responses
 Eval. (BLEU)     Gemma-3-4B     3.0k      4817.5   2.35            0.14                   from the same 𝑜𝑝 to Vrf, but this is detectable by Vrf due to PAL*M
 Eval. (BLEU)     Phi-4-Mini     3.0k      2363.7   2.34            0.30                   incorporating Chal as input in construction of TDREPORT (and sub-
 Attr. Dist.         N/A        9.25M       3.75    2.54           68.06                   sequently QUOTE). We use Lemmas 1, 4, 5, 6, and 8 to ensure that a
 Preprocessing       N/A        92.5k       4.09    2.57           62.35                   verifiable QUOTE was produced after an integrity check on a MAC-ed
                                                                                           TDREPORT, and no secret keys are revealed through the protocol.
                                                                                              Since Adv has control over the VMM, they can assign which
                                                                                           image is loaded into the TD. Therefore, they could load an image
                                                                                           containing a backdoor to assist with lying about datasets/models
replay TDREPORT or QUOTE at any stage of their construction or                             that are used for a particular operation. However, the TD image is
transmission; or (3) tamper with the configuration of PAL*M TD.                            measured by the TDX module before TD creation, and included in
To verify that the property attestation protocol from Section 4.4                          the QUOTE obtained by Vrf. Therefore, these attempts are detectable
upholds [P1-3], we use the Tamarin Prover symbolic verification                            by Vrf. Furthermore, Adv may attempt to assign a GPU without
tool [62] to model the protocol depicted in Figure 5, to construct                         a TEE to the TD. In this case, Vrf detects it due to PAL*M includ-
a set of security goals that subsume [P1-3], and to verify that the                        ing GPU attestation evidence when the GPU is used in obtaining
security goals are upheld. Here, we describe the rationale for why                         outputs. In this case, Vrf would observe 𝐺𝑃𝑈𝑎𝑡𝑡 ’s absence from the
they are upheld, with complete details in Appendix D.                                      response. We use Lemmas 1 and 2 to show that a QUOTE containing
   Adv may tamper with operation inputs to violate any of these                            PAL*M configuration (e.g., TD image and GPU) is not accepted by
properties. For example, Adv may manipulate 𝑜𝑝 to change the re-                           Vrf unless the reporting TD was created with the same configura-
quested function or misconfigure assets in I used for the requested                        tion. We do not explicitly model the scenario of GPU reassignment
function. Both cases are detectable by Vrf, since PAL*M does not                           in our formal verification: we assume the SPDM key exchange be-
measure either until they are loaded into TD memory. Therefore,                            tween the GPU and TD occurs before TD launch, as it is impossible
Vrf is assured that the inputs reflected in the QUOTE were used in the                     to launch a GPU in CC-mode without this [36, 70]. Given this, we
process. In the case of a memory-mapped data structure, Adv may                            assume the GPU–TD pair is a single trust boundary in our model.
manipulate data before it is read into the TD memory. For example,                            Finally, when outputs are deemed private, Adv may try to cor-
they may aim to repeat, replace, or reorder data records during                            rupt PAL*M TD to reveal them. However, through PAL*M measurer
fine-tuning to poison or bias the resulting model. These attempts                          script and construction of TDREPORT, confidential outputs them-
can be detected by Vrf, since PAL*M measures a MSH of records and                          selves are never extended into any TDREPORT or any downstream
indices as they are sampled. We use Lemmas 1, 3, 6, 8, 9, 10, 11,
and 12 to verify the properties are upheld despite these attempts.
                                                                                      11
QUOTE that are visible by Adv. We use Lemmas 7 and 13 outlined                 ZKPs have also been used for proof of inference across different
in outlined in Appendix D to verify that this is upheld.                       types of ML models (including LLMs) [43, 56, 87]. Furthermore,
   Under the assumed threat model, Adv cannot tamper with op-                  ZKPs can help verify security properties of ML models such as dif-
eration inputs, forge or replay attestation responses, or manipulate           ferential privacy [29, 84], and fairness [28, 83]. However, these cryp-
the TD configuration without detection by Vrf. Furthermore, the                tographic primitives have a high computation cost. For instance,
property attestation protocol is formally verified to uphold [P1-3]            verifying one iteration of VGG11 training takes ≈15 minutes [1],
despite these attempts, as confirmed by the Tamarin model detailed             making practical deployment challenging for applications.
in Appendix D. Therefore, PAL*M satisfies R2.                                     TEE-based attestations. Torres-Arias et al. [92] were the first
                                                                               to introduce supply chain attestations. However, their work targets
6.3    Scalability & Versatility                                               conventional software pipelines rather than ML-specific properties.
                                                                               Prior works have extensively used TEEs for the confidentiality
Scalability. PAL*M satisfies R3 as it can be applied to extremely
                                                                               of data and models [57, 65, 88, 102]. Unlike these approaches, we
large datasets and models, distributed computing by Prv, and en-
                                                                               focus on integrity, leveraging TEEs to attest properties of large
ables verification by multiple verifiers.
                                                                               generative model operations executed within them. Laminator [23]
   PAL*M’s use of MSH allows it to scale to extremely large datasets,
                                                                               is the closest related work, using Intel SGX to attest properties
beyond what can fit into memory, without sacrificing out-of-order
                                                                               of CPU-only classifier model operations. Schnabl et al. [81] use
access. We assume model weights can fit into the GPU’s RAM (e.g.,
                                                                               TEEs to attest the execution of the code, ML model for various
96 GB for our prototype); when they do not, standard optimizations
                                                                               inferences, and its outputs. VerifiableFL proposes an integrity-only
(e.g., quantization) reduce memory impact while maintaining per-
                                                                               enclave (called exclave), which generates authenticated evidence
formance. While some ML frameworks support memory-mapped
                                                                               of input and output data for federated learning [37]. Similar to
model weights [25, 34], accessing them through GPU↔CVM↔disk
                                                                               our approach, it uses CVM technologies (e.g., AMD SEV-SNP), but
adds significant overhead. Recent work shows quantization can
                                                                               focuses on federated learning rather than generative models, and
eliminate the need for weight offloading [85]. When quantization is
                                                                               does not focus on addressing the challenges due large datasets
insufficient or undesirable, MSH can also apply to memory-mapped
                                                                               outside CVM memory. Rattanavipanon and Nunes [74] focus on
model weights, and not just datasets.
                                                                               federated learning by providing stateful proofs of execution that
   PAL*M can extend to distributed training [97], where each node
                                                                               let an external Vrf confirm correct data use, model updates, and
returns proof(s) for its dataset subset. Due to MSH ’s incremental
                                                                               local differential privacy on TrustZone-enabled ARM Cortex-M
design, it enables aggregation of component hashes into that of the
                                                                               devices. Atlas uses TEEs to verify the ML lifecycle by having TEE-
full dataset. However, verification complexity, node-level corrup-
                                                                               equipped provers attest to inputs and outputs of artifact operations
tion, and Byzantine resilience require further study, leaving proofs
                                                                               and publish attestations to a transparency log [86].
of distributed training as an intriguing direction for future work.
                                                                                  None of the mentioned works focus on attesting properties of
   PAL*M uses digital signatures to create each QUOTE containing
                                                                               generative models while accounting for challenges of their com-
the property attestation. Therefore, any number of verifiers with
                                                                               puting environments outlined in Section 3. Most closely related
access to the attesting device’s public key can perform verification.
                                                                               is Atlas, yet it differs from PAL*M in its attestation semantics. At-
   Versatility. PAL*M satisfies R4 as it can apply to any CVM and
                                                                               las proves that artifacts follow expected pipeline steps, whereas
GPU with TEE, and it can be adapted to any type of model archi-
                                                                               PAL*M proves that outputs satisfy operation-level properties for
tecture or dataset. Although PAL*M prototype uses Intel TDX as a
                                                                               given inputs. Atlas excludes GPU execution from its TCB and uses
CVM and NVIDIA H100 for TEE-enabled GPU, PAL*M’s attestations
                                                                               whole-file hashing, which introduces TOCTOU risks for dynam-
can be generated by Prv running on any CVM-GPU configuration,
                                                                               ically sampled datasets. PAL*M addresses these with the use of
given both have TEEs with built-in attestation functionality (e.g.,
                                                                               TEE-aware GPU and MSH when sampling from untrusted storage.
AMD SEV-SNP [5] and NVIDIA Blackwell GPU [67]). Furthermore,
PAL*M can be adapted to any type of model architecture or dataset,
                                                                               8   Summary
beyond those used in our experiments, as measurements are speci-
fied in software running inside a CVM that invokes a GPU with a                This work advances ML property attestations by introducing PAL*M:
TEE. Property attestations can also be easily added by extending               a comprehensive framework capable of spanning CPU-GPU envi-
PAL*M with additional measurer scripts corresponding to the new                ronments, large-scale data, and emerging generative models. We
property, with no changes required by Inr or Vrf.                              define how to measure properties of generative models and use
                                                                               incremental multiset hash functions to capture properties across
                                                                               dataset operations and training. As a result, PAL*M enables ac-
7     Related Work                                                             countability for modern AI systems, laying the groundwork for
Cryptographic Attestations. Secure multi-party computation                     regulators, developers, and verifiers to concretely reason about an
(SMPC) and zero-knowledge proofs (ZKPs) have been used to verify               ML systems’ trustworthiness.
ML operations. SMPC has been explored for distributional property
attestation but requires per-attestation interaction with a verifier,
which is not scalable [22]. Arc uses SMPC with publicly verifiable
commitments to bind training and inference for auditing [58]. ZKPs
can provide verifiability for training simple ML models (e.g., logistic
regression) [33] and neural networks [1], and LLM fine-tuning [78].
                                                                          12
References                                                                                     [27] Armando Faz-Hernandez, Sam Scott, Nick Sullivan, Riad S. Wahby, and Christo-
 [1] Kasra Abbaszadeh et al. 2024. Zero-Knowledge Proofs of Training for Deep                       pher A. Wood. 2023. Hashing to Elliptic Curves. RFC 9380. doi:10.17487/RFC9380
     Neural Networks. In ACM SIGSAC Conference on Computer and Communica-                      [28] Olive Franzese et al. 2025. Secure and Confidential Certificates of Online
     tions Security (Salt Lake City, UT, USA) (CCS ’24). Association for Computing                  Fairness. In The Thirty-ninth Annual Conference on Neural Information Processing
     Machinery, New York, NY, USA, 4316–4330. doi:10.1145/3658644.3670316                           Systems. https://openreview.net/forum?id=9jaQTx1O8T
 [2] Abdelrahman Abouelenin et al. 2025. Phi-4-Mini Technical Report: Com-                     [29] Olive Franzese et al. 2025. Secure noise sampling for differentially private
     pact yet Powerful Multimodal Language Models via Mixture-of-LoRAs. CoRR                        collaborative learning. In Proceedings of the 2025 ACM SIGSAC Conference on
     abs/2503.01743 (2025).                                                                         Computer and Communications Security. 4649–4663.
 [3] EU Artificial Intelligence Act. 2024. The EU Artificial Intelligence Act. European        [30] Prakhar Ganesh et al. 2023. On the impact of machine learning randomness on
     Union (2024).                                                                                  group fairness. In Proceedings of the 2023 ACM Conference on Fairness, Account-
 [4] Erdem Aktas et al. 2023. Intel Trust Domain Extensions (TDX) security review.                  ability, and Transparency. 1789–1800.
     Google security review (2023).                                                            [31] Leo Gao et al. 2020. The Pile: An 800GB Dataset of Diverse Text for Language
 [5] AMD. 2020. AMD Secure Encrypted Virtualization (SEV). https://www.amd.co                       Modeling. arXiv preprint arXiv:2101.00027 (2020).
     m/en/developer/sev.html.                                                                  [32] Leo Gao et al. 2024. The Language Model Evaluation Harness. https://zenodo.o
 [6] Anthropic and Pattern Labs. 2025. Confidential Inference via Trusted Virtual                   rg/records/12608602.
     Machines. https://www.anthropic.com/research/confidential- inference-                     [33] Sanjam Garg et al. 2023. Experimenting with Zero-Knowledge Proofs of Train-
     trusted-vms. Research report on confidential inference systems using trusted                   ing. In Proceedings of the 2023 ACM SIGSAC Conference on Computer and Commu-
     virtual machines.                                                                              nications Security (Copenhagen, Denmark) (CCS ’23). Association for Computing
 [7] Daiyaan Arfeen et al. 2025. PipeFill: Using GPUs During Bubbles in Pipeline-                   Machinery, New York, NY, USA, 1880–1894. doi:10.1145/3576915.3623202
     parallel LLM Training. In MLSys. OpenReview.net/mlsys.org.                                [34] ggml org. [Accessed] 2026. LLaMA.cpp Github Repository. https://github.com
 [8] ARM. 2004. ARM TrustZone for Cortex-A. https://www.arm.com/technologies                        /ggml-org/llama.cpp/blob/master/tools/server/README.md.
     /trustzone-for-cortex-a.                                                                  [35] Google. [Accessed] 2026. Confidential VM pricing | Google Cloud. https:
 [9] Ondrej Bojar et al. 2014. Findings of the 2014 Workshop on Statistical Machine                 //cloud.google.com/confidential-computing/confidential-vm/pricing.
     Translation. In Proceedings of the Ninth Workshop on Statistical Machine Trans-           [36] Zhongshu Gu, Enriquillo Valdez, Salman Ahmed, Julian James Stephen, Michael
     lation. Association for Computational Linguistics, Baltimore, Maryland, USA,                   Le, Hani Jamjoom, Shixuan Zhao, and Zhiqiang Lin. 2025. NVIDIA GPU confi-
     12–58. http://www.aclweb.org/anthology/W/W14/W14-3302                                          dential computing demystified. arXiv preprint arXiv:2507.02770 (2025).
[10] Dan Boneh, Ben Lynn, and Hovav Shacham. 2001. Short signatures from                       [37] Jinnan Guo et al. 2024. ExclaveFL: Providing Transparency to Federated Learn-
     the Weil pairing. In International conference on the theory and application of                 ing using Exclaves. arXiv preprint arXiv:2412.10537 (2024).
     cryptology and information security. Springer, 514–532.                                   [38] Casper Hansen. 2023. AutoAWQ. https://github.com/casper-hansen/AutoAWQ.
[11] Sergey Bratus et al. 2008. TOCTOU, traps, and trusted computing. In Interna-              [39] Dan Hendrycks et al. 2021. Measuring Massive Multitask Language Under-
     tional Conference on Trusted Computing. Springer, 14–32.                                       standing. In ICLR. OpenReview.net.
[12] Brave Software. 2025. Verifiable Privacy and Transparency: A New Frontier                 [40] Jonathan Ho, Ajay Jain, and Pieter Abbeel. 2020. Denoising Diffusion Proba-
     for Brave AI Privacy. https://brave.com/blog/browser-ai-tee/. Accessed:                        bilistic Models. In NeurIPS.
     2025-11-26.                                                                               [41] Edward J. Hu et al. 2022. LoRA: Low-Rank Adaptation of Large Language
[13] Daniel R. L. Brown. 2008. The Encrypted Elliptic Curve Hash. Cryptology                        Models. In ICLR. OpenReview.net.
     ePrint Archive, Paper 2008/012. https://eprint.iacr.org/2008/012                          [42] Yaqi Hu et al. 2025. LLM-based misbehavior detection architecture for enhanced
[14] Tom Brown et al. 2020. Language Models are Few-Shot Learners. In Advances                      traffic safety in connected autonomous vehicles. IEEE Transactions on Vehicular
     in Neural Information Processing Systems, Vol. 33. Curran Associates, Inc., 1877–              Technology (2025).
     1901.                                                                                     [43] Chenyu Huang et al. 2022. zkMLaaS: a verifiable scheme for machine learning
[15] Canonical. 2025. Canonical TDX Github Repository. https://github.com/canon                     as a service. In GLOBECOM 2022-2022 IEEE Global Communications Conference.
     ical/tdx.                                                                                      IEEE, 5475–5480.
[16] Jorge Chávez-Saab et al. 2025. SwiftEC: Shallue–van de Woestijne Indifferen-              [44] Hugging Face. 2025. Datasets Arrow. https://huggingface.co/docs/datasets/v4.
     tiable Function To Elliptic Curves: Faster Indifferentiable Hashing to Elliptic                1.1/about_arrow. Accessed: 2025-10-01.
     Curves. 3 pages.                                                                          [45] Hugging Face. 2025. Preprocess. https://huggingface.co/docs/datasets/en/use_
[17] Marcin Chrapek et al. 2025. Confidential LLM Inference: Performance and Cost                   dataset. Accessed: 2025-01-19.
     Across CPU and GPU TEEs. arXiv preprint arXiv:2509.18886 (2025).                          [46] Hugging Face. 2025. Trainer. https://huggingface.co/docs/transformers/m
[18] Jalen Chuang, Alex Seto, Nicolas Berrios, Stephan van Schaik, Christina Garman,                ain_classes/trainer#transformers.Trainer.get_train_dataloader. Accessed:
     and Daniel Genkin. 2026. TEE.fail: Breaking Trusted Execution Environments                     2025-01-15.
     via DDR5 Memory Bus Interposition. In 47th IEEE Symposium on Security and                 [47] Intel. [n. d.]. Intel Provisining Certification Service for ECDSA Attestation.
     Privacy (IEEE S&P ’26). IEEE Computer Society. https://tee.fail                                https://api.portal.trustedservices.intel.com/provisioning-certification.
[19] Dwaine Clarke et al. 2003. Incremental multiset hash functions and their                  [48] Intel. 2015. Intel Software Guard Extensions (Intel SGX). https://www.intel.co
     application to memory integrity checking. In International conference on the                   m/content/www/us/en/developer/tools/software-guard-extensions/overview.
     theory and application of cryptology and information security. Springer, 188–207.              html.
[20] Scott Constable, Jo Van Bulck, Xiang Cheng, Yuan Xiao, Cedric Xing, Ilya                  [49] Intel. 2023. Intel Trust Domain Extensions (Intel TDX). https://www.intel.com/
     Alexandrovich, Taesoo Kim, Frank Piessens, Mona Vij, and Mark Silberstein.                     content/www/us/en/developer/tools/trust-domain-extensions/overview.html.
     2023. { AEX-Notify } : Thwarting precise { Single-Stepping } attacks through              [50] Intel. 2025. Intel Trust Domain Extensions (Intel TDX) Module Base Architecture
     interrupt awareness for intel { SGX } enclaves. In 32nd USENIX Security Sympo-                 Specification. https://cdrdv2-public.intel.com/853286/intel-tdx-module-base-
     sium (USENIX Security 23). 4051–4068.                                                          spec-348549006.pdf.
[21] Michael Han Daniel Han and Unsloth team. 2023. Unsloth.                                   [51] Intel. [Accessed] 2026. Intel Trust Domain Extensions Module Base Architecture
[22] Vasisht Duddu et al. 2024. Attesting distributional properties of training data                Specification. https://www.intel.com/content/www/us/en/developer/tools/trus
     for machine learning. In European Symposium on Research in Computer Security.                  t-domain-extensions/documentation.html.
     Springer, 3–23.                                                                           [52] Intel. [Accessed] 2026. Running Average Power Limit Energy Reporting CVE-
[23] Vasisht Duddu, Lachlan J Gunn, and N Asokan. 2024. Laminator: Verifiable                       2020-8694, CVE-2020-8695 INTEL-SA-00389. https://www.intel.com/content/
     ML property cards using hardware-assisted attestations. In Proceedings of the                  www/us/en/developer/articles/technical/software-security-guidance/advisor
     Fifteenth ACM Conference on Data and Application Security and Privacy. 317–                    y-guidance/running-average-power-limit-energy-reporting.html.
     328.                                                                                      [53] Insu Jang et al. 2019. Heterogeneous isolated execution for commodity GPUs.
[24] Hossam ElAtali, Lachlan J. Gunn, Hans Liljestrand, and N. Asokan. 2024. BliMe:                 In Proceedings of the Twenty-Fourth International Conference on Architectural
     Verifiably Secure Outsourced Computation with Hardware-Enforced Taint                          Support for Programming Languages and Operating Systems. 455–468.
     Tracking. In 31st Annual Network and Distributed System Security Symposium,               [54] Woomin Lee, Taehun Kim, Seunghee Shin, Junbeom Hur, and Youngjoo Shin.
     NDSS 2024, San Diego, California, USA, February 26 - March 1, 2024. The Internet               2025. T-Time: A Fine-Grained Timing-Based Controlled-Channel Attack Against
     Society.                                                                                       Intel TDX. In European Symposium on Research in Computer Security. Springer,
[25] Hugging Face. [Accessed] 2026. Loading big models into memory. https:                          323–341.
     //huggingface.co/docs/accelerate/concept_guides/big_model_inference.                      [55] ARM Limited. [n. d.]. Overview: Realms. https://learn.arm.com/learning-
[26] Congyu Fang et al. 2023. Proof-of-learning is currently more broken than you                   paths/servers-and-cloud-computing/cca-container/overview/.
     think. In 2023 IEEE 8th European Symposium on Security and Privacy (EuroS&P).             [56] Tianyi Liu, Xiang Xie, and Yupeng Zhang. 2021. zkCNN: Zero knowledge proofs
     IEEE, 797–816.                                                                                 for convolutional neural network predictions and accuracy. In Proceedings of
                                                                                                    the 2021 ACM SIGSAC Conference on Computer and Communications Security.
                                                                                                    2968–2985.
                                                                                          13
[57] Ziyu Liu et al. 2023. MirrorNet: A TEE-friendly framework for secure on-device            [84] Ali Shahin Shamsabadi et al. 2024. Confidential-DPproof: Confidential Proof
     DNN inference. In 2023 IEEE/ACM International Conference on Computer Aided                     of Differentially Private Training. In The Twelfth International Conference on
     Design (ICCAD). IEEE, 1–9.                                                                     Learning Representations. https://openreview.net/forum?id=PQY2v6VtGe
[58] Hidde Lycklama et al. 2024. Holding secrets accountable: Auditing privacy-                [85] Ying Sheng et al. 2023. FlexGen: High-Throughput Generative Inference of Large
     preserving machine learning. In USENIX Security Symposium.                                     Language Models with a Single GPU. In Proceedings of the 40th International
[59] Jeremy Maitin-Shepard, Mehdi Tibouchi, and Diego F Aranha. 2017. Elliptic                      Conference on Machine Learning (Proceedings of Machine Learning Research,
     curve multiset hash. The computer journal 60, 4 (2017), 476–490.                               Vol. 202). PMLR, 31094–31116.
[60] Upasana Mandal, Shubhi Shukla, Nimish Mishra, Sarani Bhattacharya, Paritosh               [86] Marcin Spoczynski, Marcela S. Melara, and Sebastian Szyller. 2025. Atlas: A
     Saxena, and Debdeep Mukhopadhyay. 2025. Exploring side-channels in Intel                       Framework for ML Lifecycle Provenance & Transparency. In 2025 IEEE European
     Trust Domain Extensions. Cryptology ePrint Archive, Paper 2025/079. https:                     Symposium on Security and Privacy Workshops (EuroS&PW). IEEE, 448–461.
     //eprint.iacr.org/2025/079                                                                [87] Haochen Sun, Jason Li, and Hongyang Zhang. 2024. zkLLM: Zero knowledge
[61] Sourab Mangrulkar et al. 2022. PEFT: State-of-the-art Parameter-Efficient                      proofs for large language models. In Proceedings of the 2024 on ACM SIGSAC
     Fine-Tuning methods. https://github.com/huggingface/peft.                                      Conference on Computer and Communications Security. 4405–4419.
[62] Simon Meier, Benedikt Schmidt, Cas Cremers, and David Basin. 2013. The                    [88] Tong Sun et al. 2025. TensorShield: Safeguarding On-Device Inference by Shield-
     TAMARIN prover for the symbolic analysis of security protocols. In International               ing Critical DNN Tensors with TEE. In ACM SIGSAC Conference on Computer
     conference on computer aided verification. Springer, 696–701.                                  and Communications Security (CCS).
[63] Microsoft. [Accessed] 2026. NC family VM size series - Azure Virtual Machines             [89] Rohan Taori et al. 2023. Stanford Alpaca: An Instruction-following LLaMA
     | Microsoft Learn. https://learn.microsoft.com/en-us/azure/virtual-machines/s                  model. https://github.com/tatsu-lab/stanford_alpaca.
     izes/gpu-accelerated/nc-family.                                                           [90] Gemma Team. 2025. Gemma 3 Technical Report. CoRR abs/2503.19786 (2025).
[64] Nimish Mishra, Kislay Arya, Sarani Bhattacharya, Paritosh Saxena, and Debdeep             [91] Llama Team. 2024. The Llama 3 Herd of Models. CoRR abs/2407.21783 (2024).
     Mukhopadhyay. 2025. “OOPS!”: Out-Of-Band Remote Power Side-Channel                        [92] Santiago Torres-Arias, Hammad Afzali, Trishank Karthik Kuppusamy, Reza
     Attacks on Intel SGX and TDX. In 2025 62nd ACM/IEEE Design Automation                          Curtmola, and Justin Cappos. 2019. in-toto: Providing farm-to-table guarantees
     Conference (DAC). IEEE, 1–7.                                                                   for bits and bytes. In 28th USENIX Security Symposium (USENIX Security 19).
[65] Fan Mo et al. 2020. DarkneTZ: towards model privacy at the edge using trusted                  USENIX Association, Santa Clara, CA, 1393–1410. https://www.usenix.org/c
     execution environments. In International Conference on Mobile Systems, Appli-                  onference/usenixsecurity19/presentation/torres-arias
     cations, and Services (Toronto, Ontario, Canada) (MobiSys ’20). Association for           [93] Florian Tramer and Dan Boneh. 2019. Slalom: Fast, Verifiable and Private
     Computing Machinery, New York, NY, USA, 161–174. doi:10.1145/3386901.33                        Execution of Neural Networks in Trusted Hardware. In International Conference
     88946                                                                                          on Learning Representations. https://openreview.net/forum?id=rJVorjCcKQ
[66] Ivan De Oliveira Nunes et al. 2024. Toward Remotely Verifiable Software                   [94] Ehsan Ullah et al. 2024. Challenges and barriers of using large language mod-
     Integrity in Resource-Constrained IoT Devices. IEEE Communications Magazine                    els (LLM) such as ChatGPT for diagnostic medicine with a focus on digital
     62, 7 (2024), 58–64.                                                                           pathology–a recent scoping review. Diagnostic pathology 19, 1 (2024), 43.
[67] NVIDIA. [n. d.]. AI Security With Confidential Computing. https://www.nvid                [95] Daan Vanoverloop, Andres Sanchez, Flavio Toffalini, Frank Piessens, Mathias
     ia.com/en-us/data-center/solutions/confidential-computing/.                                    Payer, and Jo Van Bulck. 2025. { TLBlur } : { Compiler-Assisted } Automated Hard-
[68] NVIDIA. 2025. NVIDIA Deployment Guide for SecureAI. https://docs.nvidia.co                     ening against Controlled Channels on { Off-the-Shelf } Intel { SGX } Platforms.
     m/cc-deployment-guide-tdx.pdf.                                                                 In 34th USENIX Security Symposium (USENIX Security 25). 1167–1186.
[69] NVIDIA. [Accessed] 2025. NVIDIA Attestation. https://docs.nvidia.com/attest               [96] Ashish Vaswani et al. 2017. Attention is all you need. Advances in neural
     ation/index.html.                                                                              information processing systems 30 (2017).
[70] NVIDIA. [Accessed] 2026. NVIDIA NVOS User Manual for NVLink Switches.                     [97] Lilian Weng and Greg Brockman. 2022. Techniques for training large neural
     https://docs.nvidia.com/networking/display/nvidianvosusermanualfornvlink                       networks. https://openai.com/index/techniques-for-training-large-neural-
     switchesv25024282/spdm.                                                                        networks/.
[71] OpenAI. 2024. Reimagining Secure Infrastructure for Advanced AI. https:                   [98] Luca Wilke, Florian Sieck, and Thomas Eisenbarth. 2024. Tdxdown: Single-
     //openai.com/index/reimagining-secure-infrastructure-for-advanced-ai/.                         stepping and instruction counting attacks against intel tdx. In Proceedings of
     Accessed: 2025-11-26.                                                                          the 2024 on ACM SIGSAC Conference on Computer and Communications Security.
[72] PyTorch. 2025. torch.utils.data — PyTorch 2.9 documentation. https://docs.pyt                  79–93.
     orch.org/docs/stable/data.html. Accessed: 2026-01-15.                                     [99] Yangyang Yu et al. 2024. Fincon: A synthesized LLM multi-agent system with
[73] Alec Radford et al. 2019. Language models are unsupervised multitask learners.                 conceptual verbal reinforcement for enhanced financial decision making. Ad-
     OpenAI blog 1, 8 (2019), 9.                                                                    vances in Neural Information Processing Systems 37 (2024), 137010–137045.
[74] Norrathep Rattanavipanon and Ivan De Oliveira Nunes Nunes. 2025. SLAPP:                  [100] Jiashu Zhang et al. 2025. FreeRide: Harvesting Bubbles in Pipeline Parallelism.
     Poisoning Prevention in Federated Learning and DP via Stateful Proofs of                       In Proceedings of the 26th International Middleware Conference. 126–139.
     Execution. IEEE Transactions on Information Forensics and Security (TIFS) (2025).        [101] Rui Zhang et al. 2022. “Adversarial examples” for proof-of-learning. In 2022
[75] Fabian Rauscher, Luca Wilke, Hannes Weissteiner, Thomas Eisenbarth, and                        IEEE Symposium on Security and Privacy (SP). IEEE, 1408–1422.
     Daniel Gruss. 2025. TDXploit: Novel Techniques for Single-Stepping and Cache             [102] Ziqi Zhang et al. 2024. No privacy left outside: On the (in-) security of TEE-
     Attacks on Intel TDX. In USENIX Secuirty 2025.                                                 shielded DNN partition for on-device ML. In 2024 IEEE Symposium on Security
[76] Siva Reddy, Danqi Chen, and Christopher D. Manning. 2019. CoQA: A Con-                         and Privacy (SP). IEEE, 3327–3345.
     versational Question Answering Challenge. Transactions of the Association for            [103] Yukun Zhu et al. 2015. Aligning books and movies: Towards story-like visual
     Computational Linguistics 7 (2019), 249–266.                                                   explanations by watching movies and reading books. In Proceedings of the IEEE
[77] Herbert Robbins and Sutton Monro. 1951. A stochastic approximation method.                     international conference on computer vision. 19–27.
     The annals of mathematical statistics (1951), 400–407.
[78] Bidhan Roy, Peter Potash, and Marcos Villagra. 2025. ZKLoRA: Efficient Zero-
     Knowledge Proofs for LoRA Verification. In Championing Open-source DEvelop-
     ment in ML Workshop @ ICML25. https://openreview.net/forum?id=tSZiOuai
                                                                                              Appendix
     OX
[79] Ahmad-Reza Sadeghi and Christian Stüble. 2004. Property-based attestation for
                                                                                              A Additional Considerations
     computing platforms: caring about properties, not mechanisms. In Proceedings             Other Generative Models. Since PAL*M is built on PyTorch
     of the 2004 workshop on New security paradigms. 67–77.
[80] Vinnie Scarlata et al. 2018. Supporting third party attestation for Intel SGX            and Hugging Face, it applies to any hosted model with accessi-
     with Intel data center attestation primitives. White paper 12 (2018).                    ble weights, including other generative models not evaluated in
[81] Christoph Schnabl et al. 2025. Attestable Audits: Verifiable AI Safety Bench-            this work (e.g., diffusion models [40]). For diffusion models, only
     marks Using Trusted Execution Environments. In ICML Workshop on Technical
     AI Governance (TAIG). https://openreview.net/forum?id=o0wbWJnCb1                         the measured input and output changes (e.g., images instead of text).
[82] Michael Schwarz, Samuel Weiser, Daniel Gruss, Clémentine Maurice, and Ste-               Properties may differ and can be added due to PAL*M versatility,
     fan Mangard. 2017. Malware guard extension: Using SGX to conceal cache
     attacks. In International Conference on Detection of Intrusions and Malware, and
                                                                                              however the approach for attestation would remain unchanged.
     Vulnerability Assessment. Springer, 3–24.                                                   Other Data Integrity Techniques. PAL*M uses MSH to incre-
[83] Ali Shahin Shamsabadi et al. 2023. Confidential-PROFITT: Confidential PROof              mentally hash dataset records into a single value, independent of the
     of FaIr Training of Trees. In The Eleventh International Conference on Learning
     Representations. https://openreview.net/forum?id=iIfDQVyuFD                              access order, but requires all record are read exactly once. Thus, it
                                                                                              applies only to full-dataset operations (common in LLM workloads).
                                                                                         14
    Table 8: Operations and property attestations in PAL*M                   D    Formal Modeling with Tamarin
        Operation (𝑜𝑝 )          Property Attestation                        To prove the security properties of PAL*M, we model its property
                                                                             attestation protocol (from Figure 5) in the Tamarin Prover [62].
        Preprocessing            Proof of preprocessing                      Tamarin is a symbolic protocol verification tool. Protocols and
        Attribute distribution   Proof of attribute distribution
        Measurement binding      Proof of binding
                                                                             adversaries are modeled as multiset rewrite rules with preconditions
        Training                 Proof of training                           and postconditions (called facts). Security goals are specified as
        Weight optimization      Proof of optimization                       lemmas, which Tamarin verifies by matching rule preconditions
        Fine-tuning              Proof of fine-tuning                        and postconditions.
        Quantization             Proof of quantization
        Evaluation               Proof of evaluation
        Inference                Proof of inference                          Rule 0: Example Rule
        Chat session inference   Proof of session inference                  rule Example_Rule:
                                                                               [ Fr(~A), In(B)]
                                                                               --[Action(~A,B)]->
                                                                               [State(~A,B), Out(h(<~A,B>)]




If partial access within a dataset is required, a Merkle tree can be            Consider the example in Rule 0; Example_Rule has two precon-
used at an O (log 𝑛) cost per lookup. A proof of binding can link MSH        ditions: Fr(~A) and In(B). It can only be evaluated if a fresh symbol
to a Merkle root, enabling selection based on system requirements.           𝐴 exists (signaled to Tamarin using Fr(~)), and if a symbol 𝐵 was
   Selecting Chal. Section 4.4 outlines a property attestation pro-          received from an Adv-controlled channel (e.g., the network).
tocol enabled by PAL*M initiated by request from Inr containing                 This rule creates two postconditions: State(~A, B), that can be
Chal. In conventional remote attestation settings, Chal is a nonce or        used as a precondition in other rules, and Out(h(<~A, B>)) which
counter used to prevent replay attacks and ensure response fresh-            sends h(<~A, B>) to an Adv-controlled channel. This example uses
ness. Given ML property attestation in this work is non-interactive          the hashing built-in, which provides a representation of a crypto-
with Vrf, selection of Chal should be derived from a timestamp               graphic hash function h(), to output the hash of A and B concate-
rather than a traditional cryptographic nonce or counter. However,           nated. We use h() in our model, along with signing built-in, which
for proof of inference, a nonce remains valuable to prevent Prv from         provides digital signature functions sign() and verify().
cherry-picking favorable executions. In this case, Vrf can publish              An action fact records that a rule was evaluated. In Rule 0, the
nonce values with expiration times for use challenges. To further            action fact Action(~A, B) records that this rule was evaluated with
mitigate cherry-picking, Vrf may request only proof of session               symbols A and B. Lemmas in Tamarin must be specified using
inference, allowing observability of response history.                       symbols and action facts, not precondition or postcondition facts.

B     Overhead of Elliptic Curve-based and
                                                                             Lemma 0: Example Lemma
      Discrete Logarithm-based Construction                                  lemma Example_Lemma:
                                                                               "All A B #i.
The MSH overhead observed in Section 6.1 stems from the hardness               Action(A,B) @i ==> not (Ex #j. K(A) @ #j)
of the discrete logarithm problem, which requires operating over
a large prime (in our case, a 2048-bit prime). Prior work has ex-
plored elliptic curve-based constructions [13, 59]. Maitin-Shepard,
Tibouchi, and Aranha proposed ECMH [59], a Mset-Mu-Hash scheme                   Lemma 0 is an example lemma Example_Lemma using the sym-
based on binary elliptic curves and characteristic-2 variant of the          bols: A, B, and #i. The notation #i tells Tamarin that the symbol i
Shallue-van de Woestijne encoding [16] for deterministic hashing             is a time variable. This lemma states: given Action(A,B) occurs at
to curve points. A simpler alternative is the try-and-increment              time #i, then there does not exist a time #j in which Adv learns A.
method [10], which repeatedly attempts to map a value onto a valid           Adv’s knowledge is expressed using the built-in fact 𝐾 ().
elliptic curve point until successful.                                           Assuming Rule 0 is the only rule, Tamarin evaluates explores
    We test proof of attribute distribution using an elliptic-curve-         all possible executions, controlling inputs via In() and outputs via
based MSH with try-and-increment over the NIST P-256 curve, and              Out() to attempt to learn A. This lemma is verified no execution
we observe a reduction in raw measurement overhead by 47.41%.                exists in which A is learned.
This further supports the analysis from Section 6.1.1 that the dom-              In our setting, QE, the TDX module, and PAL*M TD are trusted.
inant source of overhead is the MSH construction itself. Because             Communication between the TDX module, PAL*M TD, and GPU
try-and-increment has input-dependent timing [27], it is suitable            occurs over secure channels. This manifests as custom precondi-
only for public datasets. For private datasets, deterministic con-           tion/postcondition facts. Channels that traverse the VMM, disk,
structions, such as ECMH, should be used.                                    or the network are considered untrusted. For example, QE-TDX
                                                                             Module communication passes through the VMM, dataset inputs
                                                                             are read from disk during mem-mapped operation, and each QUOTE
C     Operations and Properties in PAL*M                                     is transmitted over the network prior to verification. These interac-
Table 8 shows operations and resulting property attestations.                tions are modeled using In and Out facts.
                                                                        15
D.1    Security Goals                                                         // Case 1: In-memory and public outputs
                                                                              Rule 1: TD Initialization
Recall from Section 6.2 the properties [P1-3]. We formalize them              rule Init_TDX_TD:
as the following goals that we aim to prove in our formal model:                [ Fr(~k), Fr(~qsk), In(tdImage) ]
                                                                                --[ InitTD(tdImage), SecretKey(~k), SecretKey(~qsk),
[G1] Confidentiality of Secrets: PAL*M measurements and out-                        InitialInstall(tdImage) ]->
       puts should not reveal secrets used to generate a QUOTE;                 [ !Key(~k), !QESignKey(~qsk), !QEVerKey(pk(~qsk)), Out(pk(~qsk)),
[G2] TD Measurement Integrity: a QUOTE is only valid if pro-                        !TDIsRunning(tdImage) ]
       duced from a valid TD image that was indeed installed;                 Rule 2: Get Inputs
[G3] Quote Authenticity: any accepted QUOTE is signed by QE                   rule Get_Operation_Inputs:
                                                                                [ In(op), In(I), In(chal), !TDIsRunning(hTD)]
       using its private key;                                                   --[ InputMessage(op, I, chal) ]->
[G4] Quote Integrity: any accepted QUOTE was produced after                     [ OperationInputs(op, I, chal, hTD)]
       performing a MAC integrity check on a TDREPORT;
                                                                              Rule 3: Operation Execution (In-memory)
[G5] Output Integrity: any accepted QUOTE uses O that was pro-                rule Execute_Operation:
       duced via 𝑜𝑝 execution over specified inputs I; and                      [ OperationInputs(op, I, chal, hTD) ]
[G6] Input Measurement Integrity: any accepted QUOTE was                        --[ RunOperation(op, I, chal, runOp(op, I)) ]->
                                                                                [ CompleteOperation(op, I, chal, runOp(op, I), hTD) ]
       produced using I that was loaded into TD-protected mem-
       ory.                                                                   Rule 4: TD Report Generation
                                                                              rule TD_Produce_Report:
                                                                                  let
 Properties from Goals:                                                              O = runOp(op, I)
                                                                                     mac = h(<h(I), h(op), h(chal), h(O), hTD, k>)
                    [P1] ← [G1] ∧ [G5] ∧ [G6]                                     in
                    [P2] ← [G1] ∧ [G2] ∧ [G5] ∧ [G6]                              [ !Key(k), CompleteOperation(op, I, chal, runOp(op, I), hTD) ]
                                                                                --[ TDProducesReport(op, I, chal, runOp(op, I), hTD, k) ]->
                    [P3] ← [G1] ∧ [G3] ∧ [G4]                                     [ Out(<O, h(I), h(op), h(chal), h(O), hTD, mac>), ReportReady(op,
                                                                                      I, chal, runOp(op, I), hTD, k) ]

                                                                              Rule 5: Quote Generation
   [P1] concerns operation integrity. It is established by [G1], [G5],        rule QE_Produce_Quote:
and [G6]. [G1] ensures MAC/signature keys are not leaked by the                   let
                                                                                     mac = h(<hI, hOp, hChal, hO, hTD, k>)
protocol. [G5] and [G6] ensure that output/input measurements                        sig = sign(<hI, hOp, hChal, hO, hTD>, qsk)
correspond to the operation.                                                         O = runOp(op, I)
   [P2] concerns integrity of the environment and responses. It is                in
                                                                                  [ !QESignKey(qsk), In(<O, hI, hOp, hChal, hO, hTD, mac>),
established by [G1], [G2], [G5], and [G6]. [G2], [G5], and [G6]                     ReportReady(op, I, chal, O, hTD, k) ]
ensure response integrity, as it includes ℎ𝑇 𝐷 , H O , and HI .                 --[ MacCheck(hI, hOp, hChal, hO, hTD, mac, k),
   [P3] concerns response authenticity. It is established by [G1],                   QEQuotes(hI, hOp, hChal, hO, hTD, pk(qsk)) ]->
                                                                                  [ Out(<O, sig>), SignatureReady(op, I, chal, O, hTD, sig) ]
[G3], and [G4]. [G1] again ensures key secrecy, while [G3] and
[G4] ensure any verifiable QUOTE was signed by the expected QE                Rule 6: Verification
                                                                              rule Vrf_Verifies:
and MAC-ed by the expected TDX machine, respectively.                             [ !QEVerKey(pkQ),
   We use a Tamarin model to evaluate [G1-6] under four proto-                       SignatureReady(op, I, chal, O, hTD, sig),
col scenarios, varying by dataset memory model and privacy of                        In(<O, sig>)
                                                                                  ]
operation outputs:                                                              --[ VrfAccepts(op, I, chal, O, hTD, verify(sig, <h(I), h(op), h(
• in-memory datasets to produce public outputs (Case 1);                            chal), h(O), hTD>, pkQ), pkQ) ]->
• in-memory datasets to produce private outputs (Case 2);                         []

• memory-mapped datasets to produce public outputs (Case 3);
• memory-mapped datasets to produce private outputs (Case 4).
                                                                              InitTD and InitialInstall action facts capture the CPU measurement
D.2    Case 1: In-Memory Public Outputs                                       and extension of the TD’s initial software state.
We divide the protocol for Case 1 into three parts: (i) TD initializa-           Operation Execution. We model steps (1)–(5) after TD initial-
tion, (ii) operation execution, and (iii) TDREPORT generation, QUOTE          ization from Figure 5 with two rules: (i) fetch operation inputs (e.g.,
signing, and verification.                                                    𝑜𝑝, Chal, and I) in Rule 2 and (ii) operation execution (Rule 3).
   TD Initialization. We model steps (1)—(2) of the TD initial-                  Rule 2 consumes an 𝑜𝑝, I, and Chal from the network alongside
ization phase from Figure 5 using Rule 1. This rule models TD                 a running TD fact, binding them together into an OperationInputs
creation (with GPU assigned and 𝐺𝑃𝑈𝑎𝑡𝑡 obtained), provisioning                fact that scopes execution to a live TD. Rule 3 consumes these inputs
cryptographic keys, and the initial state measurement.                        and applies the abstract function runOp(op, I) which computes the
   This rule takes two fresh secret values, an internal MAC key (∼𝑘)          operation output. Then, we log the execution via the RunOperation
and a QE signing key (∼𝑞𝑠𝑘), and a TD image as inputs, producing              action fact and forward all relevant values as a CompleteOperation
persistent facts for the resulting TD state: the MAC key, the QE              fact for the next steps.
signing/verification key pair, and a running TD loaded with that                 TDREPORT/QUOTE Generation and Verification. This part mod-
image. The QE public key is output via the untrusted channel to               els steps (6)–(11) of Figure 5. Rule 4 models TDREPORT generation.
Adv, while private keys are logged via SecretKey action facts. The            Then, Rule 5 models transferring TDREPORT to QE for signing via
                                                                         16
// Case 1: In-memory and public outputs                                           in Section 4.4. Note that due to SPDM occurring to establish a
Lemma 1: Key Secrecy
lemma key_secrecy [reuse]:
                                                                                  secure channel with GPU at the time of TD creation [36, 70],
  "All k #i. SecretKey(k) @ #i ==> not (Ex #j. K(k) @ #j)"                        these takeaways extend to the TD+GPU environment;
                                                                             [G3] Quote Authenticity: Lemma 4 ensures that Vrf only accepts
Lemma 2: TD Measurement Integrity
lemma td_measurement_integrity:                                                   a QUOTE originating from Prv’s QE, ruling out any scenario
  "All op I chal O tdImage vk #n.                                                 where a valid attestation is produced without QE’s involve-
      VrfAccepts(op, I, chal, O, tdImage, true, vk) @ #n                          ment;
    ==> Ex #i. InitialInstall(tdImage) @ #i & #i < #n"
                                                                             [G4] Quote Integrity: Lemma 5 ensures that QE invokes quote
Lemma 3: Output came from Operation and Input                                     generation only when the received MAC is well-formed, bind-
lemma O_came_from_op_and_I:
  "All op I chal O hTD pkQ #i.
                                                                                  ing quote generation to a MAC computed correctly over the
     VrfAccepts(op, I, chal, O, hTD, true, pkQ) @ #i                              expected hash values and the TD’s secret key, and guarantee-
     ==> O = runOp(op, I)"                                                        ing that TDREPORT has not been tampered. Together, these
Lemma 4: Quote Authenticity                                                       two lemmas establish an unbroken chain of trust from the
lemma quote_authenticity [reuse]:                                                 TD’s internal state through QE to Vrf;
  "All op I chal O hTD vk #n.                                                [G5] Output Integrity: Lemma 3 ensures that whenever Vrf ac-
     VrfAccepts(op, I, chal, O, hTD, true, vk) @ #n
   ==> Ex #m. QEQuotes(h(I), h(op), h(chal), h(O), hTD, vk) @ #m & #              cepts an attestation, the reported output O is exactly the
      m < #n"                                                                     result of applying the operation op to input 𝐼 via runOp(op,
Lemma 5: Quote Only If MAC is correct
                                                                                  I) in the TD. This rules out any scenario in which verifica-
lemma quote_only_if_mac:                                                          tion passes with a fabricated or mismatched result produced
  "All hI hOp hChal hO hTD mac k #i.                                              outside of the TD;
      MacCheck(hI, hOp, hChal, hO, hTD, mac, k) @ #i
    ==> mac = h(<hI, hOp, hChal, hO, hTD, k>)"                               [G6] Input Measurement Integrity: Lemma 6 ensures that for
                                                                                  every VrfAccepts event, there must exist an InputMessage
Lemma 6: Input Measurement Ingetrity                                              event carrying the same 𝑜𝑝, 𝐼 , and 𝑐ℎ𝑎𝑙. Since InputMes-
lemma input_measurement_integrity:
  "All op I chal O hTD vk #n.                                                     sage is only emitted by Get_Operation_Inputs, which runs
      VrfAccepts(op, I, chal, O, hTD, true, vk) @ #n                              inside the TD, and the subsequent Execute_Operation and
    ==> Ex #j. InputMessage(op, I, chal) @ #j & #j < #n"
                                                                                  TD_Produce_Report rules consume and propagate those ex-
                                                                                  act values through internal linear facts before any output
                                                                                  is produced, the accepted quote is guaranteed to have been
(untrusted) VMM. Lastly, the Rule 6 models making signed QUOTE                    computed over inputs that were loaded into TD-protected
available to Vrf for verification.                                                memory.
   In Rule 4, TD computes a MAC over the hashes of I, 𝑜𝑝, Chal, O,
ℎ𝑇 𝐷 , using its MAC key 𝑘. These hashes, O and the MAC are passed
                                                                             D.4    Case 2: In-memory Private Outputs
via Out(), reflecting transmission via the VMM to QE. A ReportReady
fact is also produced to maintain the internal binding between the           Here we describe the changes to the rules/lemmas for Case 1: D.2–
operation’s values and the TD’s secret key.                                  D.3 to enable Case 2 that accounts for private outputs.
   For QUOTE generation (Rule 5), QE receives TDREPORT via In() and              Modifications to Rules. The key change from public to private
recomputes the MAC to verify it before signing. Upon successful              output is how O is exposed. In Case 1, TD_Produce_Report outputs
verification, QE signs the hashes of the I, 𝑜𝑝, Chal, O, and ℎ𝑇 𝐷            O directly to the network. In Case 2, it outputs only the hash of
using 𝑞𝑠𝑘, and send Out() the signed QUOTE and O.                            it, keeping O hidden. Execute_Operation also adds SecretOutput(O)
   Lastly, for Rule 6, Vrf consumes QUOTE from the network along-            action fact to mark O for privacy tracking.
side the known QE public key, checking the signature against the                 Modifications to Lemmas. Goals [G2-6] in Case 2 are upheld
expected hash values. The VrfAccepts action fact records the out-            using the same lemmas from Case 1, with one additional lemma
come, binding Vrf’s acceptance to the specific I, 𝑜𝑝, Chal, O, ℎ𝑇 𝐷 ,        added to ensure that [G1] still holds. Lemma 7 ensures that O
and public key.                                                              remains secret. It states that any value marked SecretOutput is
                                                                             never learned by Adv, which makes it satisfy [G1].
D.3    Security Proofs for Case 1
  Lemmas 1– 6 are used to prove the protocol model detailed in               D.5    Case 3: Memory-mapped Public Outputs
Appendix D.2 uphold security goals [G1-6] from Appendix D.1:                 Here we describe only the changes to Case 1 protocol from D.2–
[G1] Confidentiality of Secrets: Lemma 1 ensures that any key                D.3 to enable Case 3 protocol by accounting for memory-mapped
     marked as secret at initialization is never derivable by Adv;           datasets with public outputs. The changes to the model are high-
[G2] TD Measurement Integrity: Lemma 2 ensures that the Vrf                  lighted in yellow in Rules 11–14 and Lemmas 8–12.
     only accepts an attestation if the TD image referenced in the              Modifications to Rules. From Case 1, the rules for TD Initial-
     attestation was legitimately installed prior to verification,           ization (Rule 1) and Get Inputs (Rule 2) are also in the model for
     binding accepted attestations to a known, measured software             Case 3. However, Case 3 requires the remaining rules to change,
     state. Notably, the integrity guarantee is scoped to the TD im-         plus the addition of three new rules.
     age measurement. Whether the expected TD image was used                    Many changes to the operation execution are to model an incre-
     requires consulting reference values from Tru, as described             mental operation that has several steps: first, starting the execution,
                                                                        17
// Case 2: In-memory and private outputs                                         // Case 3: Mem-mapped and public outputs
Rule 7: Operation Execution (memory-mapped)                                      Rule 11: Execute Operation (mem-mapped)
rule Execute_Operation:                                                          rule Execute_Operation:
  let                                                                              [ OperationInputs(op, chal, hTD), Fr(~sid) ]
     O = runOp(op, I)                                                              --[ SessionStarted(~sid, op, chal, hTD) ]->
  in                                                                               [ State(~sid, op, chal, hTD, runOp(op, 'empty'), 'empty', 'none',
  [ OperationInputs(op, I, chal, hTD)]                                                 %1)} ]
  --[ RunOperation(op, I, chal, O), SecretOutput(O) ]
  [ CompleteOperation(op, I, chal, O, hTD) ]                                     Rule 12: Execution step (lookup from disk)
                                                                                 rule Execution_lock_and_lookup:
Rule 8: TD Report Generation                                                       [ State(sid, op, chal, hTD, pretrained, block_data_multiset,
rule TD_Produce_Report:                                                                block_indices, %index) ]
    let                                                                            -->
       O = runOp(op, I)                                                            [ Out(<'get', sid, %index>), PendingLookup(sid, op, chal, hTD,
       mac = h(<h(I), h(op), h(chal), h(O), hTD, k>)                                   pretrained, block_data_multiset, block_indices, %index) ]
    in
    [!Key(k), CompleteOperation(op, I, chal, runOp(op, I), hTD)]                 Rule 13: Return item from disk
  --[TDProducesReport(op, I, chal, runOp(op, I), hTD, k)]->                      rule DatasetStorage:
    [Out(<h(I), h(op), h(chal), h(O), hTD, mac>),                                  [ In(<'get', sid, index>) ]
       ReportReady(op, I, chal, runOp(op, I), hTD, k)]                             -->
                                                                                   [ Out(<'batch', sid, datasets(index)> ) ]
Rule 9: Quote Generation
rule QE_Produce_Quote:                                                           Rule 14: Execution step (use disk item)
    let                                                                          rule Execution_unlock_and_continue:
       mac = h(<hI, hOp, hChal, hO, hTD, k>)                                       let
       hashes = <hI, hOp, hChal, hO, hTD>                                             model = runOp(op, batch)
       sig = sign(hashes, qsk)                                                        new_block_data_multiset = block_data_multiset ++ <%index, batch>
    in                                                                                new_block_indices = h(<batch, block_indices>)
    [ !QESignKey(qsk), In(<hI, hOp, hChal, hO, hTD, mac>),                         in
      ReportReady(op, I, chal, O, hTD, k)                                          [ In(<'batch', sid, batch>), PendingLookup(sid, op, chal, hTD,
    ]                                                                                   pretrained, block_data_multiset, block_indices, %index) ]
  --[ MacCheck(hI, hOp, hChal, hO, hTD, mac, k), QEQuotes(hI, hOp,                 --[ Trained(sid, op, chal, hTD, model, new_block_data_multiset,
      hChal, hO, hTD, pk(qsk)) ]->                                                      new_block_indices) ]->
    [Out(<hashes, sig>), SignatureReady(op, I, chal, O, hTD, sig)]                 [ State(sid, op, chal, hTD, model, new_block_data_multiset,
                                                                                        new_block_indices, %index %+ %1) ]
Rule 10: Verification
rule Vrf_Verifies:
    let
       hashes = <hI, hOp, hChal, hO, hTD>
    in                                                                           from this rule pass through an untrusted channel to simulate Adv
    [ !QEVerKey(pkQ),                                                            control over the disk.
       SignatureReady(op, I, chal, O, hTD, sig),                                     Rule 14 specifies the continuation of the execution that uses the
       In(<hashes, sig>) ]
  --[ VrfAccepts(op, I, chal, O, hTD, verify(sig, <h(I), h(op), h(               fetched batch from the requested index, and the accumulation of the
      chal), h(O), hTD>, pkQ), pkQ) ]->                                          multiset that is used to construct the MSH. The multiset construction
    []
                                                                                 is shown by accumulating < %𝑖𝑛𝑑𝑒𝑥, 𝑏𝑎𝑡𝑐ℎ > into the multiset and
                                                                                 hashing it. This also creates a postcondition containing fact State,
                                                                                 resulting in the possibility of re-evaluation of Rule 12 (e.g., to use
// Case 2: In-memory and private outputs                                         more data records and grow the multiset further) or to continue to
Lemma 7: Private Output                                                          report generation.
lemma private_O [reuse]:
  "All X #i. SecretOutput(X) @ #i ==> not (Ex #j. K(X) @ #j)"                        The rules that specify TDREPORT Generation, Quote Generation,
                                                                                 and Verification are largely the unmodified Rule 4, 5, and 6, re-
                                                                                 spectively. A very minor change is that the MSH measurement is
                                                                                 included along with all other hashes in each fact and action fact.
making a request to disk, modeling the disk itself, and finalizing that              Modifications to Lemmas. One lemma from Case 1 is modified,
step (and the multiset). Rule 11 shows the first part of this process,           and three more are introduced to account for the multiset construc-
in which a session ID is specified (~sid) along with an action fact              tion. [G1-4] use Lemmas 1, 2, 4, and 5, respectively, as discussed in
SessionStarted to log this event. The postcondition of this rule is a            Appendix D.3. [G5-6] are upheld by the the following lemmas:
fact that specifies the initial state. Notably, the State fact contains a        [G1] Output Integrity: uses Lemma 3, discussed in Appendix D.3
field for output, and in this initial state, it is equal to performing                  along with new Lemmas 11 and 12. Lemma 11 provides that
the runOp() on an empty dataset.                                                        two training operations that produce equivalent sampling
   Rule 12 specifics the first step for execution with a memory-                        sequences (denoted hI ) result in the same output (e.g., m1
mapped dataset. A record of the dataset is requested from the disk                      and m2). Similarly, Lemma 12 establishes that two training
by specifying the index. This rule results in sending Out a get                         operations that use the same input multiset (hm) results in
request from disk for the particular index, along with a fact to                        the same output;
signify a pending lookup (PendingLookup).                                        [G2] Input Integrity: uses Lemmas 8, 9, and 10. Lemma 8 is a
   Rule 13 specifies a simple rule to simulate fetching an item from                    modified version of Lemma 6 that checks for the Trained
the disk. The get request is received from In, and a batch that was                     event rather than InputMessage. In addition, since the dataset
fetched from the index is returned through Out. Both messages                           is measured incrementally, the integrity check does not apply
                                                                            18
// Case 3: Mem-mapped and public outputs                                     // Case 4: Mem-mapped and private outputs
Lemma 8: Input Measurement Integrity                                         Rule 15: TD Report Generation (mem-mapped)
lemma input_measurement_integrity:                                           rule TD_Produce_Report:
"All op I hI chal O hTD vk #n.                                                   let
  VrfAccepts(op, I, hI, chal, O, hTD, true, vk) @ #n                             O = runOp(op, I)
  & not( I = 'empty')                                                            mac = h(<hI, h(op), h(chal), h(O), hTD, k>)
 ==> Ex indices sid #j.                                                          in
 Trained(sid, op, chal, hTD, O, I, indices) @ #j"                                [ !Key(k), State(sid, op, chal, hTD, O, I, hI, index) ]
                                                                               --[ TDProducesReport(op, I, hI, chal, O, hTD, k),
Lemma 9: Equal sampling sequences implies equal multiset                            SecretOutput(O, op, I)
lemma Seq_Multiset_Match [use_induction,reuse]: all-traces                       ]->
"All sid1 sid2 m1 m2 hm1 hm2 hi op1 op2 chal1 chal2 hTD1 hTD2 #i #j.             [ Out(<hI, h(op), h(chal), h(O), hTD, mac>),
 Trained(sid1, op1, chal1, hTD1, m1, hm1, hi) @ i                                   ReportReady(op, I, hI, chal, O, hTD, k) ]
& Trained(sid2, op2, chal2, hTD2, m2, hm2, hi) @ j
==> hm1 = hm2"

Lemma 10: Equal multiset implies equal input sample sequence                 // Case 4: Mem-mapped and private outputs
restriction MS_Seq_Match:                                                    Lemma 13: Private Output
"All sid1 sid2 op1 op2 chal1 chal2 hTD1 hTD2 m1 m2 hm hi1 hi2 #i #j.         lemma private_O:
Trained(sid1, op1, chal1, hTD1, m1, hm, hi1) @ i                               "All O I op #i. SecretOutput(O, op, I) @ #i
& Trained(sid2, op2, chal2, hTD2, m2, hm, hi2) @ j                             ==> not ( Ex #j. not (
    ==> hi1 = hi2"                                                                 O = train(op, 'empty')
                                                                                 ) & K(O) @ #j )"
Lemma 11: Equal input sample sequence implies equal output
lemma Seq_O_Match [use_induction,reuse]: all-traces
"All sid1 sid2 op chal1 chal2 hTD1 hTD2 m1 m2 hm1 hm2 hi #i #j.
Trained(sid1, op, chal1, hTD1, m1, hm1, hi) @ i                              Table 9: Statistics for lemma verification: Max Steps denotes
& Trained(sid2, op, chal2, hTD2, m2, hm2, hi) @ j                            the highest steps for any lemma; Total Steps is the sum of
==> m1 = m2"
                                                                             steps across all lemmas; Peak Mem. is the maximum RAM
Lemma 12: Equal multiset implies equal output                                usage; Time is the total verification run-time.
lemma MS_O_match [reuse]: all-traces
"All sid1 sid2 op chal1 chal2 hTD1 hTD2 m1 m2 hm hi1 hi2 #i #j.               Protocol    Max Steps     Total Steps    Peak Mem. (MiB)      Time (s)
 Trained(sid1, op, chal1, hTD1, m1, hm, hi1) @ i
 & Trained(sid2, op, chal2, hTD2, m2, hm, hi2) @ j                            Case 1           20             38              26799            89.2
 ==> m1 = m2"                                                                 Case 2           16             38                246            2.33
                                                                              Case 3           42             98               2268            65.7
                                                                              Case 4           42            115                270            5.10



      when the input is empty. Given these two modifications, this           D.7       Verification Results
      lemma provides that a QUOTE passing verification implies
                                                                             Each protocol case has the lemmas outlined in Appendices D.3– D.6,
      that the input dataset is not empty and that it was indeed
                                                                             along with several “helper lemmas” that test functionality of the
      used for training. Lemma 9 provides that given two training
                                                                             protocol. Table 9 shows performance statistics when using Tamarin
      operations have occurred with equal sampling sequences,
                                                                             to analyze the four protocol cases and prove all lemmas (functional
      the two inputs must be equal. Finally, Lemma 10 specifies
                                                                             and security). Case 2 is the most simplistic for two reasons. First, it
      that two training operations with the same recorded multiset
                                                                             uses a simpler model of the in-memory dataset. Second, it has fewer
      must have used the same sampling sequences. This lemma
                                                                             symbols that are controllable by Adv, resulting in less exploration
      uses the keyword restriction, meaning that it must be proven
                                                                             by Tamarin. Both Case 3 and Case 4 require verifying the lemma
      by hand. The proof for this is shown in Appendix D.8.
                                                                             that takes the most steps for verification: Lemma 9, which requires
                                                                             42 steps. The higher memory usage and run-time of Case 1 are
D.6    Case 4: Memory-mapped Private Outputs                                 due to a functional helper lemma that forces the prover to evaluate
Here we describe the changes to the Case 3 model from Appen-                 each rule. In this case, it must simultaneously solve for execution
dix D.5 to account for Case 4 with private outputs and memory-               semantics of the custom function that is used to produce O plus the
mapped datasets.                                                             cryptographic abstraction hO. In Case 2, execution semantics do
   Modifications to Rules. Only one rule requires modification,              not require as in-depth an exploration since Adv only learns hO.
and that is Rule 15 for TDREPORT Generation. Here, secret output
O is logged using the action fact SecretOutput along with 𝑜𝑝 and I           D.8       Multiset hashing security reduction
that were used to produce O. Additionally, the multiset hash (hI ) is        PAL*M’s ability to access datasets out-of-order that cannot fit all at
included in the set of output hash values sent via Out.                      once into the TEE’s memory depends on its use of an incremental
   Modifications to Lemmas. Goals [G2-6] are upheld using                    multiset hash MSH satisfying the homomorphism
the same lemmas as Case 3 protocol, described in Appendix D.5.
                                                                                             MSH(𝑀1 ∪ 𝑀2 ) = MSH(𝑀1 ) · MSH(𝑀2 ).
Goal [G1] is supported by the verification of Lemma 1 for key
secrecy, as discussed in Appendix D.3, and it is also supported by              Specifically, given an ordered dataset D = (𝑑 1, 𝑑 2, . . . , 𝑑𝑛 ) of 𝑛
the verification of Lemma 13, which specifies that O cannot be               records, we require that the TEE, after receiving records 𝑝 1, . . . , 𝑝𝑛 ,
learned given any operation and non-empty input dataset.                     can be assured that the values 𝑑 1′ , . . . , 𝑑𝑛′ that it receives are the
                                                                        19
  D,A                                                                                          BA
𝐺 Streamed-Incorrect-Data                                                                   𝐺 MSH-Collision
H ← MSH ({})                                                                                           $
                                                                                            𝑀1 , 𝑀2 ←
                                                                                                    − B A (𝑛)
for 𝑖 = 1 . . . 𝑛
               $                                                                            if MSH(𝑀1 ) = MSH(𝑀2 ) ∧ 𝑀1 ≠ 𝑀2
   (𝑝𝑖 , 𝑑𝑖′ ) ←
               − A ()                                                                          return 1
   𝐻 ← 𝐻 · MSH({(𝑝𝑖 , 𝑑𝑖′ )})                                                               else
endfor                                                                                         return 0
if 𝐻 = MSH(D) ∧ ∃𝑖 : 𝑑𝑖′ ≠ 𝑑𝑝𝑖                                                              endif
   return 1
else                                                                                                              Figure 6: MSH collision game.
   return 0
endif                                                                                      same values 𝑑𝑖′ = 𝑑𝑝𝑖 in the original dataset, so long as
                ⇓ Reformulated using MSH homomorphism                                         MSH ({(1, 𝑑 1 ), . . . , (𝑛, 𝑑𝑛 )}) = MSH (𝑝 1, 𝑑 1′ ), . . . , (𝑝𝑛 , 𝑑𝑛′ ) .
                                                                                                                                                                         
  D,A
𝐺 Streamed-Incorrect-Data ′                                                                The left-hand side can be easily precomputed whenever 𝑝 is a
           $                                                                               permutation; for convenience, we denote this hash MSH(D).
𝑀1 , 𝑀2 ←
        − B A (𝑛) :                                                                           The adversary’s goal is defined in the following game in which
          for 𝑖 = 1 . . . 𝑛                                                                the adversary A attempts to provide the TEE with records not
                      $
             𝑝𝑖 , 𝑑𝑖′ ←
                      − A ()                                                               matching D, shown in Figure 7. Our goal is to reduce this to the
          endfor                                                                           MSH collision game 𝐺 MSH-Collision
                                                                                                                B
                                                                                                                              , shown in Figure 6.
          return {(1, 𝑑 1 ), . . . , (𝑛, 𝑑𝑛 )}, {(𝑝 1, 𝑑 1′ ), . . . , (𝑝𝑛 , 𝑑𝑛′ )}
if MSH(𝑀1 ) = MSH(𝑀2 ) ∧ ∃𝑖 : 𝑑𝑖′ ≠ 𝑑𝑝𝑖                                                       Theorem D.1 (Incremental hashing of streamed data.). For
   return 1                                                                                any adversary A and dataset D = (𝑑 1, 𝑑 2, . . . , 𝑑𝑛 ), there exists B A
else                                                                                       such that:
                                                                                                                 D,A                                 B
                                                                                                                                                     A
   return 0                                                                                                Pr (𝐺 Streamed-Incorrect-Data ) ≤ Pr (𝐺 MSH-Collision )
endif
                                                                                                                                  D,A
                                                                                               Proof. We observe that 𝐺 Streamed-Incorrect-Data       can be restruc-
                                ⇓ BA also wins
                                                                                           tured in terms of a new adversary B A , shown in Figure 7. This game
  B A                                                                                                           BA
𝐺 MSH-Collision                                                                            is very similar to 𝐺 MSH-Collision , except that the requirement 𝑀1 ≠ 𝑀2
          $                                                                                is replaced by ∃𝑖 : 𝑑𝑖′ ≠ 𝑑𝑝𝑖 . That is, there exists some 𝑖 such that
𝑀1 , 𝑀2 ←
        − B A (𝑛)                                                                          there exist distinct elements (𝑝𝑖 , 𝑑𝑝𝑖 ) ∈ 𝑀1 and (𝑝𝑖 , 𝑑𝑖′ ) ∈ 𝑀2 . Since
if MSH(𝑀1 ) = MSH(𝑀2 ) ∧ 𝑀1 ≠ 𝑀2                                                           𝑀1 is defined as
   return 1
                                                                                                                     𝑀1 = {(1, 𝑑 1 ), . . . , (𝑛, 𝑑𝑛 )},
else
   return 0                                                                                it contains exactly one element having any particular index 𝑖 ∈
endif                                                                                      {1, . . . , 𝑛}, and none with indices outside this range. Since (𝑝𝑖 , 𝑑𝑖′ ) ≠
         Figure 7: Game hops to prove Theorem D.1.                                         (𝑝𝑖 , 𝑑𝑝𝑖 ), 𝑀1 and 𝑀2 therefore differ at the element with this index,
                                                                                                                       BA
                                                                                           and so B A also wins 𝐺 MSH-Collision  .                                     □




                                                                                      20
