                                         V ERI L OCC: End-to-End Cross-Architecture Register Allocation via LLM


                                                        Lesheng Jin1 Zhenyuan Ruan2 Haohui Mai3 Jingbo Shang1
                                                                    1
                                                                      UC San Diego 2 MIT      3
                                                                                                CausalFlow Inc.
                                                   1                              2
                                                     {l3jin, jshang}@ucsd.edu       zainruan@mit.edu 3 haohui@causalflow.ai




                                                               Abstract                               in the instruction set architecture (ISA). A correct
                                                                                                      allocation must (1) consistently map the same vir-
                                             Optimizing GPU compilers must find quality
arXiv:2506.17506v1 [cs.CL] 20 Jun 2025




                                             solutions of the combinatorial compiler opti-
                                                                                                      tual register to the same physical register, and (2)
                                             mization problem (e.g., register allocations)            assign virtual registers with overlapping lifetimes
                                             to generate performant GPU binaries. Cur-                to disjoint physical registers.
                                             rently they mostly rely on hand-crafted heuris-             Achieving performant register allocation is even
                                             tics which require substantial re-tuning for             harder, as it requires modeling architectural details
                                             each hardware generation. We introduce V ER -            such as register bank conflicts (Guan et al., 2024),
                                             I L OCC , a framework that combines large lan-
                                                                                                      pipeline stalls, and memory spill costs. Modern
                                             guage models (LLMs) with formal compiler
                                                                                                      compilers rely on hand-crafted or learned heuris-
                                             techniques to enable generalizable and ver-
                                             ifiable register allocation across GPU archi-            tics (Lozano et al., 2019; Quintão Pereira and Pals-
                                             tectures. V ERI L OCC fine-tunes an LLM to               berg, 2008), while performance-critical libraries
                                             translate intermediate representations (MIRs)            such as BLAS (AMD Inc., 2024a) often resort to
                                             into target-specific register assignments, aided         handwritten assembly optimized for specific GPUs.
                                             by static analysis for cross-architecture nor-           Both approaches demand substantial engineering
                                             malization and generalization and a verifier-            effort and are difficult to retarget across hardware
                                             guided regeneration loop to ensure correctness.          generations.
                                             Evaluated on matrix multiplication (GEMM)
                                             and multi-head attention (MHA), V ERI L OCC
                                                                                                         Recent work has explored learning-based al-
                                             achieves 85-99% single-shot accuracy and near-           locations, but mainly rely on handcrafted fea-
                                             100% pass@100. Case study shows that V ER -              tures (Chen et al., 2021) or lack of the sound-
                                             I L OCC discovers more performant assignments            ness guarantees to integrate the model outputs into
                                             that outperform the state-of-the-art, expert-            the real-world compiler stacks (Liu et al., 2024).
                                             tuned rocBLAS by over 10% in runtime.                    General-purpose models like ChatGPT have lim-
                                                                                                      ited abilities on NP-Complete problems (Wei et al.,
                                         1   Introduction
                                                                                                      2025). Therefore they often struggle with regis-
                                         Modern GPUs have dramatically reshaped deep                  ter allocation, producing incorrect sequential as-
                                         learning by offering massive parallel computational          signments that ignore liveness constraints (Ap-
                                         powers (Krizhevsky et al., 2012). Unleashing                 pendix B). This motivates our approach: combin-
                                         this performance requires not only hardware ad-              ing the expressiveness of large language models
                                         vances (Jouppi et al., 2017; Wang et al., 2021; Zhao         (LLMs) (OpenAI, 2023; Yang et al., 2025) with
                                         et al., 2025), but also increasingly sophisticated           formal verification techniques to achieve correct-
                                         software stacks (Chen et al., 2018; Li et al., 2023;         ness and cross-architecture generalization.
                                         Ma et al., 2020; NVIDIA Corporation, 2024; Wu                   This paper introduces V ERI L OCC, a learning-
                                         et al., 2025; Zheng et al., 2020). At the core are op-       based register allocator that formulates register as-
                                         timizing compilers, which translate high-level GPU           signment as an end-to-end sequence-to-sequence
                                         kernels into efficient, hardware-specific binaries.          (seq2seq) translation task (Sutskever et al., 2014)
                                            Many of these optimizations are NP-complete; a            task for LLM. Our key insight is that while GPU
                                         central example is register allocation (Alfred et al.,       architectures differ in low-level details, they share
                                         2007), as illustrated in Figure 1. The task involves         core traits, such as in-order pipelines and sharded
                                         assigning virtual registers in the compiler’s inter-         register banks, which persist across vendors and
                                         mediate representation (MIR) to physical registers           generations. V ERI L OCC fine-tunes an LLM to

                                                                                                  1
                                   [
                                              bb0:                                                        VERILOCC                                     LDG.E R4, [R4.64]



                                       CUDA
                                              ld.global.f32 %f6, [%rd14];                                                                              LDG.E R6, [R6.64]
                                              ld.global.f32 %f7, [%rd13];                            Input: Regalloc. spec +                           IADD3 R0, R0, 0x1, RZ
                                              fma.rn.f32 %f9, %f7, %f6, %f9;                            Normalized MIR                                 UIADD3 UR6, UP0, UR6, 0x4, URZ
               for (l=0;l<k; l++)
                 t+= a[l]* bT[l];
                                              add.s64 %rd14, %rd14, 4;                                                                                 UIADD3 UR8, UP1, UR8, 0x4, URZ
Training




                                              add.s64 %rd13, %rd13, 4;                                                                                 ISETP.GE.AND P0, PT, R0, c[0x0][0x160], PT
                                              add.s32 %r9, %r9, 1;                                                                                     UIADD3.X UR7, URZ, UR7, URZ, UP0, !UPT
               c[i][j] = t;


                                              setp.lt.s32 %p2, %r9, %r3;                                                                               UIADD3.X UR9, URZ, UR9, URZ, UP1, !UPT
                                              @%p2 bra $L__BB0_2;                                                                                      FFMA R9, R4, R6, R9
                                                                                                                                                       @!P0 BRA 0xe0
                                                                                                       Output: Virtual-




                                                                                 MIR Normalization
                                                                    MIR (PTX)




                                                                                                                               Dataflow Analysis:
                                                                                                     physical reg. mapping                                                            ISA (SASS)




                                                                                  Pre-processing:




                                                                                                                                 Reg. mapping
                                   %b5:                                                                                                                BB0:
                                   %1 = PHI %50, %b1, %[9:10], %b5                                                                                     s_load_dword s4, s[2:3], 0x0
                                   %2 = PHI %51, %b1, %[11:12], %b5                                         Seq2Seq                                    s_load_dword s5, s[8:9], 0x0
                                   %3 = PHI %52, %b1, %8, %b5                                              Translation                                 s_add_i32 s6, s6, -1
             Test Cases (unseen)




                                   %4 = PHI %53, %b1, %7, %b5                                                                                          s_add_u32 s2, s2, 4
                                   %5 = S_LOAD_DWORD_IMM %1, 0, 0                                                                                      s_addc_u32 s3, s3, 0
Inference




                                   %6 = S_LOAD_DWORD_IMM %2, 0, 0                                                                                      s_add_u32 s8, s8, 4
                                   %7 = V_FMAC_F32_e64 %5, %6, %4                                          Resample                                    s_addc_u32 s9, s9, 0
                                   %8 = S_ADD_I32 %3, -1                                                   on errors                                   s_waitcnt lgkmcnt(0)
                                   %9, %s0 = S_ADD_U32 %8.lo, 4                                                                                        v_mov_b32_e32 v3, s5
                                   %10 = S_ADDC_U32 %8.hi, 0, %s0                                                                                      s_cmp_eq_u32 s6, 0
                                   %11, %s1 = S_ADD_U32 %7.lo, 4                                            Formal             Pass                    v_fmac_f32_e32 v2, s4, v3
                                   %12 = S_ADDC_U32 %7.hi, 0, %s1                                      Verification (Z3)                               s_cbranch_scc0 .LBB0_1
                                   %s2 = S_CMP_EQ_U32 %8, 0
                                   S_CBRANCH_SCC1 %bb.2, %s2     MIR (LLVM)                                                                                                           ISA (CDNA2)

                                          LOAD %f6, [%rd14];                                                                    %5 = LOAD %1, 0, 0                            %1→R1, %2→R5_R6
                                          LOAD %f7, [%rd13];                                                                    %6 = LOAD %2, 0, 0                            %3→R1, %4→R7_R8
            Normalization and
            Allocation Results




                                          FMA %f9, %f7, %f6, %f9;                %1→R2, %2→R4                                   %7 = FMA %5, %6, %4                           %5→R6, %6→R7_R8
                                          ADD %rd14, %rd14, 4;                                                                  %8 = ADD %3, -1                               %7→R1, %8→R5
Examples




                                                                                 %3→R2, %4→R3
                                          ADD %rd13, %rd13, 4;                   %5→R8, %6→R4                                   %9, %s0 = ADD %8.lo, 4                        %9→R3
                                          ADD %r9, %r9, 1;                       %7→R4, %8→R4                                   %10 = ADD %8.hi, 0, %s0
                                                                                %9→R4, %10→R6                                   %11, %s1 = ADD %7.lo, 4
                                                                                                                                %12 = ADD %7.hi, 0, %s1
                                                                                                                                                                             R5_R6 / R7_R8 are
                                                       Normalized MIR (PTX)                                                                         Normalized MIR (LLVM)    grouped registers

Figure 1: Overall training and inference workflow of V ERI L OCC. Our seq2seq formulation learns to translate normalized MIR
into virtual-to-physical register mappings, derived from MIR and ISA through dataflow analysis that tracks value propagation.
For clarity, we show only the MIR (e.g., PTX) and ISA (e.g., SASS) fragments that load matrix A from memory and perform
dot-product accumulation. We also include illustrative examples of the normalized MIRs and the structured mapping between
virtual and physical registers across architectures.


translate MIR into target-specific register assign-                                                             analysis to normalize both MIR and ISA representa-
ments, treating different MIRs as dialects of a                                                                 tions while preserving program semantics (Lattner
shared computational language. Inspired by neural                                                               et al., 2007; Xie and Aiken, 2007). The analy-
machine translation (Sutskever et al., 2014; Bah-                                                               sis normalizes MIRs from different compilers into
danau et al., 2015; Vaswani et al., 2017), V ER -                                                               a unified format, and extracts the results of reg-
I L OCC learns to map virtual to physical registers                                                             ister allocations as JSON-style dictionaries (Fig-
while adapting to the syntactic and semantic varia-                                                             ure 1). This reduces token length by 80–90%
tions of diverse GPU toolchains.                                                                                in our experiments (Table 1), improving LLM
   V ERI L OCC must overcome three key challenges                                                               reasoning efficiency and allowing the model to
to be practical. First, compiler transformations                                                                focus on allocation logic. Normalization also
such as inlining and loop unrolling (Alfred et al.,                                                             enables the creation of a heterogeneous training
2007) can inflate MIR size beyond the LLM’s ef-                                                                 dataset that combines compiler-generated outputs
fective context window (Hsieh et al., 2024); for                                                                from multiple toolchains with expert-optimized li-
instance, a single multi-head attention (MHA) ker-                                                              braries—teaching the model both general strate-
nel (Vaswani et al., 2017) can exceed 50,000 to-                                                                gies and target-specific heuristics. To enforce cor-
kens. Second, the model must generalize across                                                                  rectness , V ERI L OCC models the generated map-
architectures while respecting hardware-specific                                                                pings as instances of Satisfiability Modulo Theories
constraints like register file sizes and reserved reg-                                                          (SMT) problems, and formally verifies their cor-
isters. Third, correctness is critical – an invalid                                                             rectness using Z3 (De Moura and Bjørner, 2008).
allocation may silently corrupt a program or render                                                             V ERI L OCC continues to re-sample for candidate
it unexecutable.                                                                                                allocations until a correct solution is found.
   V ERI L OCC addresses these challenges via a                                                                    We evaluate V ERI L OCC on two types of crit-
combination of normalization and verification, as                                                               ical GPU kernels: general matrix multiplication
illustrated in Figure 1. V ERI L OCC employs static                                                             (GEMM) and multi-head attention (MHA), which

                                                                                                            2
together account for over 90% of inference time             MIR in the ROCm toolchain (AMD Inc., 2024b)),
in modern LLMs (Dao et al., 2022). A fine-tuned             they share similar design principles. In the rest
7B LLM achieves 85–99% single-shot correctness              of the paper we use IR and MIR to refer to the
and near-100% pass@100 with verification. A case            target-independent and target-specific IRs.
study on the GEMM kernel running on AMD’s                   Register Allocation. Programs in MIR are not
MI250x GPU shows that V ERI L OCC discovers reg-            directly executable. MIRs use virtual registers, or
ister assignments that exploit architectural features       ϕ-nodes in SSA forms (Bilardi and Pingali, 2003)
overlooked by existing compilers and human ex-              to represent values in the programs. To realize the
perts. The generated GEMM kernel outperforms                MIR to executable ISAs, the register allocators as-
rocBLAS (AMD Inc., 2024a) by 11.6% in runtime,              sign these virtual values to physical registers. It
which is the state-of-the-art, hand-optimized BLAS          must consistently assign the same value to the same
library shipped by the GPU vendor. These results            register, and ensure that values with overlapping
demonstrate that V ERI L OCC combines the flexi-            life cycles are assigned to disjoint registers. Addi-
bility of data-driven learning with the reliability         tionally, the assignment must satisfy the hardware
required for deployment in production compiler              constraints (e.g., a 64-bit value must be assigned
toolchains.                                                 to two consecutive 32-bit registers). Due to the
    This paper makes the following contributions.           limited number of physical registers and hardware
• We propose V ERI L OCC, a learning-based regis-           constraints, the register allocator might copy the
   ter allocator that combines LLMs, static analysis,       values across registers, or temporarily spill the val-
   and verifier-guided regeneration to achieve cor-         ues to main memory.
   rectness and cross-architecture generalization.             Finding performant results of register allocations
• We evaluate V ERI L OCC on GEMM and MHA                   is particularly important for GPU programs since
   kernels, where a fine-tuned 7B LLM achieves              it directly affects the available parallelism and in-
   85–99% single-shot accuracy and near-100%                struction latency. A performant allocation would
   pass@100, validating the feasibility of LLM-             minimize the copies and spills, and consider low-
   based register allocation.                               level hardware features to minimize pipeline stalls.
• We show that V ERI L OCC can discover novel reg-          For example, NVIDIA GPUs organize the registers
   ister assignments that outperform expert-tuned           into 4 banks. Reading values in the same banks
   libraries, achieving 11.6% runtime improvement           requires stalling the pipeline for another cycle, thus
   over rocBLAS on AMD MI250x.                              in Figure 1 the compiler avoid the stalls by choos-
Reproducibility. Our implementation is pub-                 ing R4, R6, and R9 in the FFMA instruction which
licly available on GitHub: https://github.com/              are in separate register banks. Note that finding the
Jimmy-MMMM/VeriLocc.                                        optimal register allocation is NP-complete (Chaitin
                                                            et al., 1981), thus compilers often rely on either
2   Preliminaries: Register Allocations in                  manual or learning-based heuristics when optimiz-
    GPU Compilers                                           ing register allocations.
                                                            Complexity and Challenges. Low-level code gen-
IR and MIR. Modern compilers use Intermedi-                 eration introduces substantial complexity that poses
ate Representations (IRs) extensively for optimiza-         unique challenges for our sequence-to-sequence
tions. The compilers take the application written           formulation. When compiled for GPUs, kernels un-
in high level languages (e.g., CUDA) as inputs and          dergo aggressive transformations such as inlining,
then transform it to multiple levels of IRs. The            loop unrolling, and memory coalescing. These op-
compilers tackle different optimization goals at dif-       timizations significantly inflate the size of both the
ferent levels of IRs. For example, LLVM (Lattner            MIR and the final assembly. As shown in Table 1,
and Adve, 2004) performs target independent opti-           each multi-head attention (MHA) kernel averages
mizations such as constant propagations and dead            419 lines in PTX format, compared to 1,860 lines in
code elimination at the level of LLVM IR, and per-          LLVM IR. After tokenization, this corresponds to
forms target-specific optimizations such as coalesc-        9,294 tokens for PTX and 51,037 tokens for LLVM,
ing memory accesses at the lower level machine IR           far exceeding the context limits of current coding
(MIR). While different compiler toolchains have             LLMs (Hsieh et al., 2024). As a result, naively
different naming (e.g., CUDA PTX vs SASS in                 fine-tuning LLMs struggles to capture long-range
the NVIDIA toolchains, and LLVM IR and LLVM                 dependencies among register uses and assignments.

                                                        3
   Architectural variability presents a second ma-                   We train this mapping with a standard cross-entropy
jor challenge. Different GPU vendors employ dis-                     loss:
tinct IRs and toolchains: NVIDIA uses PTX, while                                    m
                                                                                 1 X
AMD uses a custom MIR format. As shown in                                L=−           log P (yi |X , y1 , . . . , yi−1 ) (2)
                                                                                 m
Figure 1, these representations differ in syntax, in-                               i=1

struction structure, and register classes, making it                 V ERI L OCC normalizes the MIR before using it as
difficult for cross-architecture modeling without                    input. The auxiliary information consists of the
careful normalization.                                               control and data dependency, the constraints of the
   Finally, correctness is non-negotiable in compil-                 task (e.g., the number of available registers), as
ers. A single invalid register assignment can lead to                well as hardware constraints on reserved registers
runtime crashes or silent corruption, rendering the                  and values. V ERI L OCC follows the control flow
compiled program unusable. Any learning-based                        graph to allocate registers per basic block. Fig-
allocator must therefore be paired with a mecha-                     ure 1 presents two concrete examples of normal-
nism that ensures compiler-level soundness.                          ized MIRs along with their corresponding register
   These observations lead to three key challenges:                  mappings.
1. Long sequences. Optimized kernels produce                         3.2   Static Analysis-based Normalization
   IRs and ISAs that exceed the effective context
                                                                     V ERI L OCC performs static analysis for two tasks:
   window of typical LLMs, making long-range
                                                                     (1) reconstructing the results of register allocations
   reasoning difficult.
                                                                     from the training data, as well as making control
2. Cross-architecture generalization. The model
                                                                     and data dependency explicit during inferences,
   must reconcile shared allocation strategies with
                                                                     and (2) normalizing the MIR / ISA to reduce the
   ISA-specific syntax and constraints.
                                                                     number of tokens and to improve generalizations.
3. Compiler-level correctness. The system must
   ensure sound register assignments to produce                      3.2.1 Reconstructing Register Assignments
   functional executables.                                           V ERI L OCC intercepts the open source ROCm
                                                                     toolchain to collect the register assignments for
3     The V ERI L OCC Framework                                      AMD GPUs. However, the NVIDIA toolchain
                                                                     does not make the results of register allocations
Figure 1 illustrates the overall workflow of V ER -
                                                                     readily available. To recover the mappings for
I L OCC , which formulates register allocation as
                                                                     training, V ERI L OCC transforms both the MIR and
a sequence-to-sequence (seq2seq) transformation.
                                                                     ISA to the Static Single Assignment (SSA) forms,
Given tokenized MIR as input, the model generates
                                                                     and performs standard context-insensitive, path-
structured register assignments in JSON format.
                                                                     insensitive, flow-sensitive global analysis (Xie and
However, raw MIR and ISA representations are
                                                                     Aiken, 2007) to reconstruct the mappings. Particu-
often long, sparse, and inconsistent across architec-
                                                                     larly, V ERI L OCC follows the control flow graphs
tures, making it difficult for LLMs to infer control
                                                                     of both MIR and ISA, reconstructs the mappings
flow and data dependencies implicitly. To address
                                                                     by comparing the corresponding basic blocks, and
this, V ERI L OCC applies static analysis to normal-
                                                                     finally consolidates the mappings for the full func-
ize inputs and explicitly expose key semantic infor-
                                                                     tion. Using SSA forms allows V ERI L OCC eas-
mation at inference time. Finally, a verifier-guided
                                                                     ily to deal with the reordered instructions. V ER -
regeneration loop ensures that the generated alloca-
                                                                     I L OCC uses heuristics to deal with cases where the
tions satisfy semantic correctness.
                                                                     toolchain chooses different instructions between
3.1    Seq2Seq Formulation                                           MIRs and ISAs (e.g., lowering the mul.wide.u32
                                                                     instruction to a bit shift in Figure 1).
Formally, given an input sequence X representing                         V ERI L OCC uses the same techniques above to
the tokenized MIR (potentially augmented with                        analyze the control flows and data dependency of
auxiliary information), the model generates an out-                  the inputs. The information is later injected as
put sequence Y corresponding to register assign-                     auxiliary information into the input sequences.
ments in structured JSON format:
                                                                     3.2.2 Normalizing MIRs
                    m
                                                                     V ERI L OCC normalizes the MIRs for the training
                    Y
       P (Y|X ) =         P (yi |X , y1 , . . . , yi−1 )   (1)
                    i=1
                                                                     data and the inference inputs to reduce the num-

                                                                 4
ber of tokens and to enhance generalizability across           Table 1: Statistics of the data sets. The numbers of lines and
                                                               tokens are averaged across different configurations.
multiple architectures and workloads. First, it strips
                                                                Kernel   # Configs    GPU     # Lines # Tokens (raw / normalized)
out irrelevant metadata (e.g., comments and de-                                      NVIDIA     79       1,233 / 113    90.8% ↓
                                                                GEMM      3,375
bug symbols), and replaces the ISA-specific pro-                                      AMD       71       2,289 / 274    88.0% ↓
logues (e.g., the pointer to the function arguments)            MHA       1,512
                                                                                     NVIDIA    419      9,294 / 1,944    79.1% ↓
                                                                                      AMD     1,860    51,037 / 8,955    82.5% ↓
as symbolic values since they are irrelevant to the
task of register allocations. Second, it normalizes
the instructions and register classes of different             ously re-samples the model until a valid allocation
architectures to common representations. For ex-               is found or a maximum number of attempts are
ample, V ERI L OCC normalizes fma.rn.f32 and                   exhausted.
V_FMAC_F32_e64 to FMA in the normalized MIR.
V ERI L OCC also classifies a register to either a             4     Experiments
scalar or vector register, and the type of the stored
value (integer, float, or boolean). Additionally,              The evaluation aims to answer the following ques-
V ERI L OCC renumbers the registers for each ba-               tions both qualitatively and quantitatively:
sic block to reduce the ranges of the tokens which             • How effective can V ERI L OCC generate correct
improves the reasoning performance of the models.                 register allocations?
                                                               • How effective can V ERI L OCC generalize over
3.3   LLM Fine-tuning Pipeline                                    new programs and architectures?
V ERI L OCC uses a 7B decoder-only language                    • How effective can normalizations improve model
model fine-tuned on the normalized input-output                   performance?
pairs described above. As the backbone model,                  • Is V ERI L OCC sufficiently fast to be used real-
V ERI L OCC uses Qwen2.5-Coder-7B-Instruct                       world settings?
for its strong coding performance and effi-
                                                               4.1    Datasets
ciency (Yang et al., 2025). During training, the
model is exposed to register allocation examples               We curate data from two of the most computation-
from NVIDIA and/or AMD toolchains. Section 4                   ally intensive kernels in large-scale deep learning:
provides more details of the pipeline.                         general matrix multiplication (GEMM) and multi-
                                                               head attention (MHA). We collect the MIRs and
3.4   Verifier-guided Inference                                ISAs of the GEMM and MHA kernels of various
At the inference time, the input is a normalized,              configurations. Each configuration has its own
tokenized MIR sequence along with auxiliary an-                shapes of memory tiles (Kjolstad et al., 2017), dif-
notations, and the model generates a dictionary                ferent levels of unrolling, and different lengths of
of register assignments in an auto regressive fash-            software pipelines. The dataset closely resembles
ion. To eliminate hallucinations or incorrect results          real-world libraries including BLAS and FlashAt-
from the LLM, V ERI L OCC consists of a verifier               tention, which compute the results for different
to validate the results of register allocations before         dimensions of inputs with GPU-specific configura-
returning them to the compiler toolchain.                      tions for best runtime performances. The dataset
    V ERI L OCC constructs a SMT problem based on              consists of MIRs and ISAs for both NVIDIA RTX
the input MIR to validate the followings:                      4090 and AMD MI250x GPUs. Table 1 describes
• Consistency. It consistently assigns the same                the statistics of the data set. The MHA kernels
  virtual register to the same physical register.              exhibit higher computational complexity with sig-
• Safety. Virtual registers with overlapping life              nificantly more basic blocks per instance than
   cycles are assigned to disjoint physical registers.         GEMM, resulting in a total dataset of 9,325 in-
• Realizability. The assignment satisfies the hard-            stances. Please refer to Appendix A for more de-
  ware constraints.                                            tails.
   Modeling the verification as SMT problems en-
ables V ERI L OCC to reason about the solutions                4.2    Evaluation setups
across various control flow paths, which is crucial            We evaluate V ERI L OCC on two servers: one with
for well-optimized performance-critical workloads              equipped with 500GB SSD, 10GbE ethernet, and
like GEMM. Specifically, we use Z3 4.14.0 for val-             a RTX 4090 GPU. The other server with equipped
idating the results of register allocations. It continu-       with 17TB SSD, 10GbE ethernet, and a MI250x

                                                           5
Table 2: Effectiveness of V ERI L OCC in three different settings. “w/o norm.” is an ablation study of V ERI L OCC by disabling the
MIR normalization. It reports the numbers for both the GEMM and MHA test cases.
                                                 GEMM (768 test cases)                                                         MHA (1865 test cases)
                               Greedy Decoding                   Sampling Decoding                         Greedy Decoding                         Sampling Decoding
 Setup      Model         Pass ↑ / Fail ↓   Pass Rate ↑   Pass@100 ↑     AvgTry ↓     MaxTry ↓   Pass ↑ / Fail ↓       Pass Rate ↑       Pass@100 ↑     AvgTry ↓     MaxTry ↓
            V ERI L OCC      764 / 4         99.48%        99.47%          1.15         122           1796 / 69         96.30%            99.74%            1.44       149
 Same-NV
            w/o norm.        756 / 12         98.44%       99.08%          1.51         158           1779 / 86          95.39%           99.74%            1.52       181
            V ERI L OCC      764 / 4         99.48%        99.86%          1.10         183           1794 / 71         96.19%            96.84%            2.61       105
 Same-AMD
            w/o norm.        762 / 6          99.22%       99.35%          1.15         201           1775 / 90          95.17%           95.87%            3.09       176
            V ERI L OCC      753 / 15         98.05%       98.56%          1.14         143         1601 / 264          85.84%            89.76%            6.37       227
 Mixed
            w/o norm.        749 / 13         98.29%       98.05%          1.13         170         1491 / 374           79.95%           84.24%            9.11       241




GPU. Both servers run Ubuntu 22.04, CUDA 12.4
                                                                                                       Syntax                  Dataflow               Hardware constraints
and ROCm 6.3.1. We serve the models at the server
with NVIDIA GPU and report the average of 100                                             Same-NV

runs of the runtime performances.                                                       Same-AMD
   We randomly partition the dataset and use 80%
                                                                                              Mixed
/ 20% of the data for training and testing, respec-
tively. We consider two experiment settings: (1)                                                       0          50     100       150       200      250      300     350
                                                                                                                                 Number of errors
Same-NV and Same-AMD: training and infer-
ences are done with data on the same NVIDIA                                           Figure 2: Error Distributions of V ERI L OCC on MHA under
or AMD hardware architecture; and (2) Mixed,                                          Different Settings.
where training and inferences are done with data
from both architectures.                                                              imum attempts typically falling within 100 to 200.
   Our primary metric is the Pass Rate, which                                            Overall, V ERI L OCC works very well in the both
measures the percentage of single-shot greedy de-                                     the Same-NV / Same-AMD settings. While the
coding generations that pass the verification, i.e.,                                  Mixed setting is more challenging, V ERI L OCC
produce a correct register allocation. We also re-                                    still generalizes well. This indicates that LLMs
port Pass@100, the proportion of test cases where                                     can learn transferable patterns in register allocation
at least one valid allocation is generated within                                     across different ISAs.
100 attempts. To assess runtime overhead if one
integrates our LLM-based register allocator into                                      4.4     Ablation on MIR Normalization
the compiler toolchains, we additionally report the                                   The MIR normalization is effective at reducing
average attempts (AvgTry) and the maximum at-                                         the input token numbers by about 80% to 90% as
tempts (MaxTry) required to generate the first cor-                                   shown in Table 1. We further compare the end-to-
rect allocation.                                                                      end effect of disabling the normalization in Table 2.
                                                                                      The normalized version consistently perform bet-
4.3      Main Results                                                                 ter in terms of almost all evaluation metrics. This
Table 2 reports the number of passing and failing                                     confirms the importance of our proposed MIR nor-
instances, along with the percentages of valid gen-                                   malization.
erations under one-shot (Pass@1) and up to 100
attempts (Pass@100). It also includes the aver-                                       4.5     Error Analysis of Greedy Decoding
age and maximum number of attempts required to                                        We analyze all error cases from V ERI L OCC’s
produce the first valid allocation.                                                   greedy decoding on MHA to better understand its
   V ERI L OCC achieves strong single-shot perfor-                                    limitations. GEMM is excluded because the total
mance, with Pass@1 rates ranging from 85% to                                          number of errors on GEMM is too small. Figure 2
99% across GEMM and MHA test cases. MHA                                               shows the distribution of error types across differ-
kernels pose greater difficulty due to longer se-                                     ent settings. Errors fall into three main categories
quences and more complex dependencies, with a                                         • Syntactic Errors: These account for 4–8% of
Pass Rate of 85.84% in the mixed training setting.                                      failures and involve malformed JSON output,
Nevertheless, a simple resampling strategy proves                                       e.g., missing braces, broken key-value pairs, or
highly effective, Pass@100 is nearly 100%, with                                         extraneous text. Such errors are typically easy to
the average number of attempts under 10, and max-                                       fix via post-processing.

                                                                                  6
• Dataflow Violations: The most severe, compris-             Table 3: Effectiveness of V ERI L OCC while using 3B model
                                                             on GEMM. MHA is too hard for 3B model.
  ing 62–73% of errors, where V ERI L OCC over-                                        Greedy Decoding          Sampling Decoding
  writes values that are still live later in the pro-         Setup      Model           Pass Rate ↑     Pass@100 ↑   AvgTry ↓   MaxTry ↓

  gram. These semantic violations directly com-               Same-NV
                                                                         V ERI L OCC       89.06%         98.44%        6.84        782
                                                                         w/o norm.         88.02%         97.14%        7.03        977
  promise program correctness.                                           V ERI L OCC       87.24%         98.67%        7.29        793
                                                              Same-AMD
• Hardware Constraint Violations: Making                                 w/o norm.         86.46%         98.67%        7.85        993

  up 24–29% of errors, these occur when the
  model assigns values to register configurations
  that violate hardware rules, for example, us-              GEMM achieves 111.44 TFLOPS when multiply-
  ing non-consecutive registers (vgpr0_vgpr2) for            ing 128 × 4096 and 4096 × 4096 fp16 matrices
  64-bit operands, where contiguous pairs (e.g.,             with a strided batch of 3, which is 11.63% faster
  vgpr0_vgpr1) are expected.                                 than rocBLAS. A detailed analysis shows that
Interestingly, the proportion of dataflow violations         V ERI L OCC discovers a more performant assign-
is lower when the model is trained on a single ar-           ment than the one used in the expert-optimized
chitecture, suggesting that cross-architecture gener-        rocBLAS. Particularly, the MI250x GPU is based
alization remains a key challenge despite our nor-           on the CDNA2 architecture, which introduces ded-
malization efforts. As a future direction, one could         icated matrix core units to accelerate matrix mul-
incorporate constrained decoding that explicitly             tiplications. It offers two types of vector registers:
masks out currently occupied registers during gen-           standard architectural vector registers (VGPRs) or
eration, helping to reduce both dataflow violations          accumulation VGPRs (AccVGPRs), where the VG-
and hardware constraint errors.                              PRs can be used by all compute components but
                                                             the AccVGPRs are exclusive to the matrix core
4.6   Efficiency in End-to-End Compilation
                                                             units. V ERI L OCC discovers an assignment that
The NVIDIA and AMD toolchains compile the test               stores the values of the matrices in the AccVGPRs
cases in 1107 ms on average. V ERI L OCC spends              aggressively while rocBLAS stores them in the
most of the time in two components: model serv-              VGPRs. The publicly available ISA documenta-
ings and verification. Our evaluation server serves          tion (AMD Inc., 2022) indicates there should be no
the Qwen2.5-Coder-7B-Instruct model at the speed             performance differences. We suspect that the ma-
of 8260 input tokens per second and 131 output to-           trix core units have faster access to the AccVGPRs
kens per second with no concurrent requests. Our             at the micro architecture level, which has a lower
end-to-end measurements closely match the num-               latency thus improves the performance. Though
bers: the average time of serving a single inference         anecdote, it demonstrates the practical advantage
in V ERI L OCC is 945 ms. V ERI L OCC can adopt              and potential of V ERI L OCC over expert-optimized
techniques like continuous batching (Kwon et al.,            libraries.
2023) and radix attentions (Zheng et al., 2024) to
significantly speed up the inferences. This is left to
future work.                                                 4.8      Performance of 3B Model
   The verifications can take significant more time.
On average it takes 31.77 ms to verify the correct-          We evaluate Qwen2.5-Coder-3B-Instruct to as-
ness of the assignments with Z3. The longest veri-           sess the feasibility of using smaller models for
fication takes 7.7 seconds. While validating worst           register allocation. While the 3B model achieves
case assignments does require the full capabilities          reasonable performance on GEMM (up to 98%
of Z3, it is possible to accelerate the common cases         pass@100 with sampling), it consistently fails on
where the verification can be done via following the         MHA tasks. This highlights a clear capability
control and data dependency in polynomial time.              gap: smaller models struggle with the complex
We leave this optimization to future work.                   dependencies and register pressure present in real-
                                                             world kernels like MHA. Notably, our normaliza-
4.7   Case Study: Beyond Existing Compilers                  tion method continues to provide benefits at this
One thing worth noting is that V ERI L OCC is able           scale, improving pass rates and reducing decoding
to find a more performant solution for GEMM com-             attempts. These results suggest that more sophisti-
pared to rocBLAS, the state-of-the-art GEMM li-              cated compiler tasks may require larger models to
brary offered by AMD. This refined version of                maintain effectiveness.

                                                         7
5   Related Work                                            of register allocations directly from the MIRs and
                                                            ISAs, opening a new path path toward generaliz-
Learning-based Compiler Optimization. Re-                   able, semantics-aware compiler optimization.
cent advances in machine learning have opened               Static analysis and validations. Static analy-
new directions for compiler optimization by re-             sis (Lattner et al., 2007; Xie and Aiken, 2007)
placing handcrafted heuristics with learned models.         is effective to detect errors and vulnerabilities in
MLGO (Chen et al., 2021) applies reinforcement              the programs. V ERI L OCC uses sound static anal-
learning in LLVM for tasks like inlining and reg-           ysis (Mai et al., 2023) (i.e., no false negative) to
ister allocation, but depends on manual features            effectively validate the results of register alloca-
and tight coupling with compiler internals. Meta’s          tions are correct.
LLM Compiler (Liu et al., 2024) trains LLMs on IR
and assembly for end-to-end translation. The gener-         6   Conclusions and Future Work
ated results, however, lack the essential soundness
guarantees to be consumed in the compiler stacks.           We demonstrate that large language models (LLMs)
General-purpose models like ChatGPT also strug-             can effectively learn register allocation as a
gle with register allocation, producing sequential,         sequence-to-sequence task, achieving high correct-
invalid assignments without liveness reasoning (Ap-         ness rates and competitive runtime performance.
pendix B). In contrast, our work combines the ex-           V ERI L OCC generalizes across architectures, bene-
pressiveness of LLMs with formal verification tech-         fits from normalization, and even surpasses expert-
niques, using normalization and verifier-guided de-         optimized libraries in some scenarios, highlighting
coding to ensure correctness and cross-architecture         the potential of learning-based approaches in com-
generalization.                                             piler backends.
Optimizing tensor compilers. Modern AI models                  A key direction for future work is integrating the
are essentially tensor programs. Optimizing ten-            verifier into training. One possibility is to provide
sor compilers (Chen et al., 2018; Li et al., 2023;          verifier feedback as additional input to the model
Ma et al., 2020; Ragan-Kelley et al., 2013; Wu              during fine-tuning. Another avenue is to explore
et al., 2025; Zheng et al., 2020) realize tensor pro-       reinforcement learning, where the verifier acts as
grams to performant implementations on GPU or               a reward signal to directly guide the model toward
ASICs (Jouppi et al., 2017). They automatically             sound and performant allocations.
apply techniques such as memory tiling (Ragan-
                                                            Limitations
Kelley et al., 2013), operator fusions (Chen et al.,
2018), software pipelining (Ma et al., 2020) to             While V ERI L OCC shows strong results on regis-
search efficient schedules to utilize the hardware.         ter allocation for key GPU kernels, it has several
They mostly operate at the tensor level on interme-         limitations. First, our evaluation focuses on struc-
diate representations such as MLIR (Lattner et al.,         tured compute kernels (GEMM and MHA) that
2021), and delegates the effort of generating low-          dominate LLM inference workloads; generalizing
level ISAs to the GPU / ASIC toolchains. V ER -             to less regular or control-heavy programs remains
I L OCC operates at a lower level of the software           future work. Second, although we demonstrate
stack. It focuses on improving the register alloca-         cross-architecture generalization between NVIDIA
tions inside the toolchains. They can be combined           and AMD backends, adaptation to vastly different
together to further improve performances.                   architectures (e.g., CPU and TPU) would require
Register allocation. Register allocation is one of          additional normalization and fine-tuning. Third,
the integral components of the compiler backends.           the model’s performance degrades for highly com-
Optimal register allocation is NP-Complete, there-          plex kernels when using smaller architectures (e.g.,
fore compilers uses manual heuristics, constraint           3B), suggesting that larger models may still be nec-
solvers (Quintão Pereira and Palsberg, 2008), com-          essary for difficult compiler tasks. Finally, while
binatorial optimizations (Lozano et al., 2019) and          our verifier ensures correctness, the re-sampling
reinforcement learnings (VenkataKeerthy et al.,             loop can add latency in low-confidence cases.
2023) to find satisfactory solutions. Compilers                We believe these are meaningful directions for
also opt for linear register allocations (Poletto and       future work, including scaling to more optimiza-
Sarkar, 1999) in latency-sensitive use cases. V ER -        tion targets, improving efficiency, and expanding
I L OCC leverages LLMs to learn effective strategies        to broader compiler infrastructures.

                                                        8
References                                                     Cheng-Ping Hsieh, Simeng Sun, Samuel Kriman, Shan-
                                                                 tanu Acharya, Dima Rekesh, Fei Jia, and Boris Gins-
V Aho Alfred, S Lam Monica, and D Ullman Jeffrey.                burg. 2024. RULER: What’s the real context size of
  2007. Compilers principles, techniques & tools.                your long-context language models? In First Confer-
  pearson Education.                                             ence on Language Modeling.
AMD Inc. 2022.      Amd instinct mi200 instruc-
 tion set architecture.  https://www.amd.com/                  Norman P. Jouppi, Cliff Young, Nishant Patil, David
 content/dam/amd/en/documents/instinct-                          Patterson, Gaurav Agrawal, Raminder Bajwa, Sarah
 tech-docs/instruction-set-architectures/                        Bates, Suresh Bhatia, Nan Boden, Al Borchers, Rick
 instinct-mi200-cdna2-instruction-set-                           Boyle, Pierre-luc Cantin, Clifford Chao, Chris Clark,
 architecture.pdf.                                               Jeremy Coriell, Mike Daley, Matt Dau, Jeffrey Dean,
                                                                 Ben Gelb, and 57 others. 2017. In-datacenter per-
AMD Inc. 2024a. rocBLAS: Rocm basic linear algebra               formance analysis of a tensor processing unit. In
 subprograms (blas) library. https://github.com/                 Proceedings of the 44th Annual International Sym-
 ROCm/rocBLAS. Accessed: 2024-05-01.                             posium on Computer Architecture, ISCA ’17, pages
                                                                 1–12, New York, NY, USA. Association for Comput-
AMD Inc. 2024b.     Rocm compiler and pro-                       ing Machinery.
 gramming model documentation.    https://
 rocm.docs.amd.com.                                            Fredrik Kjolstad, Shoaib Kamil, Stephen Chou, David
                                                                 Lugato, and Saman Amarasinghe. 2017. The ten-
Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Ben-
                                                                 sor algebra compiler. Proc. ACM Program. Lang.,
  gio. 2015. Neural machine translation by jointly
                                                                 1(OOPSLA).
  learning to align and translate. In International Con-
  ference on Learning Representations (ICLR).                  Alex Krizhevsky, Ilya Sutskever, and Geoffrey E Hin-
Gianfranco Bilardi and Keshav Pingali. 2003. Algo-               ton. 2012. Imagenet classification with deep convo-
  rithms for computing the static single assignment              lutional neural networks. Advances in neural infor-
  form. J. ACM, 50(3):375–425.                                   mation processing systems, 25.

Gregory J. Chaitin, Marc A. Auslander, Ashok K. Chan-          Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying
  dra, John Cocke, Martin E. Hopkins, and Peter W.              Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gon-
  Markstein. 1981. Register allocation via coloring.            zalez, Hao Zhang, and Ion Stoica. 2023. Efficient
  Comput. Lang., 6(1):47–57.                                    memory management for large language model serv-
                                                                ing with pagedattention. In Proceedings of the 29th
Tianqi Chen, Thierry Moreau, Ziheng Jiang, Lianmin              Symposium on Operating Systems Principles, SOSP
  Zheng, Eddie Yan, Haichen Shen, Meghan Cowan,                 ’23, pages 611–626, New York, NY, USA. Associa-
  Leyuan Wang, Yuwei Hu, Luis Ceze, and 1 others.               tion for Computing Machinery.
  2018. TVM: An automated End-to-End optimizing
  compiler for deep learning. In 13th USENIX Sympo-            Chris Lattner and Vikram Adve. 2004. Llvm: A com-
  sium on Operating Systems Design and Implementa-               pilation framework for lifelong program analysis &
  tion (OSDI 18), pages 578–594.                                 transformation. In Proceedings of the International
                                                                 Symposium on Code Generation and Optimization:
Yundi Chen, Hanrui Wei, William Yu, Haonan Zhao,                 Feedback-Directed and Runtime Optimization, CGO
  Yao Zhao, and Hanjun Yang. 2021. Mlgo: a machine               ’04, page 75, USA. IEEE Computer Society.
  learning guided compiler optimization framework.
  In NeurIPS.                                                  Chris Lattner, Mehdi Amini, Uday Bondhugula, Albert
Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra,                Cohen, Andy Davis, Jacques Pienaar, River Riddle,
   and Christopher Ré. 2022. Flashattention: fast and            Tatiana Shpeisman, Nicolas Vasilache, and Oleksandr
   memory-efficient exact attention with io-awareness.           Zinenko. 2021. MLIR: Scaling compiler infrastruc-
   In Proceedings of the 36th International Conference           ture for domain specific computation. In CGO 2021.
   on Neural Information Processing Systems, NIPS ’22,
                                                               Chris Lattner, Andrew Lenharth, and Vikram Adve.
   Red Hook, NY, USA. Curran Associates Inc.
                                                                 2007. Making context-sensitive points-to analysis
Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: an              with heap cloning practical for the real world. In
  efficient smt solver. In Proceedings of the Theory and         Proceedings of the 28th ACM SIGPLAN Conference
  Practice of Software, 14th International Conference            on Programming Language Design and Implementa-
  on Tools and Algorithms for the Construction and               tion, PLDI ’07, pages 278–289, New York, NY, USA.
  Analysis of Systems, TACAS’08/ETAPS’08, pages                  Association for Computing Machinery.
  337–340, Berlin, Heidelberg. Springer-Verlag.
                                                               Yijin Li, Jiacheng Zhao, Sun Qianqi, Haohui Mai, Lei
Xiaofeng Guan, Hao Zhou, Guoqing Bao, Handong                    Chen, Wanlu Cao, Yanfan Chen, Li zhicheng, YING
  Li, Liang Zhu, and Jianguo Yao. 2024. Prescount:               LIU, Xinyuan Zhang, Xiyu Shi, Jie Zhao, Jingling
  Effective register allocation for bank conflict reduc-         Xue, Huimin Cui, and XiaoBing Feng. 2023. Sirius:
  tion. In 2024 IEEE/ACM International Symposium                 Harvesting whole-program optimization opportuni-
  on Code Generation and Optimization (CGO), pages               ties for dnns. In Proceedings of Machine Learning
  170–181.                                                       and Systems, volume 5, pages 186–202. Curan.


                                                           9
Liang Liu, Marc Brockschmidt, Vivek Murali, and et al.         S VenkataKeerthy, Siddharth Jain, Anilava Kundu,
   2024. The meta llm compiler: A suite of open-                 Rohit Aggarwal, Albert Cohen, and Ramakrishna
   source models for code optimization. arXiv preprint           Upadrasta. 2023. Rl4real: Reinforcement learning
   arXiv:2407.02524.                                             for register allocation. In Proceedings of the 32nd
                                                                 ACM SIGPLAN International Conference on Com-
Roberto Castañeda Lozano,           Mats Carlsson,               piler Construction, pages 133–144.
  Gabriel Hjort Blindell, and Christian Schulte.
  2019. Combinatorial register allocation and instruc-         Yang Wang, Chen Zhang, Zhiqiang Xie, Cong Guo,
  tion scheduling. ACM Transactions on Programming               Yunxin Liu, and Jingwen Leng. 2021. Dual-side
  Languages and Systems (TOPLAS), 41(3):1–53.                    sparse tensor core. In Proceedings of the 48th Annual
                                                                 International Symposium on Computer Architecture,
Lingxiao Ma, Zhiqiang Xie, Zhi Yang, Jilong Xue,                 ISCA ’21, pages 1083–1095. IEEE Press.
  Youshan Miao, Wei Cui, Wenxiang Hu, Fan Yang,
  Lintao Zhang, and Lidong Zhou. 2020. Rammer: En-             Anjiang Wei, Yuheng Wu, Yingjia Wan, Tarun Suresh,
  abling holistic deep learning compiler optimizations           Huanmi Tan, Zhanke Zhou, Sanmi Koyejo, Ke Wang,
  with rTasks. In 14th USENIX Symposium on Operat-               and Alex Aiken. 2025. Satbench: Benchmarking
  ing Systems Design and Implementation (OSDI 20),               llms’ logical reasoning via automated puzzle genera-
  pages 881–897. USENIX Association.                             tion from sat formulas. Preprint, arXiv:2505.14615.

HaoHui Mai, Jiacheng Zhao, Hongren Zheng, Yiyang               Mengdi Wu, Xinhao Cheng, Shengyu Liu, Chunan Shi,
  Zhao, Zibin Liu, Mingyu Gao, Cong Wang, Huimin                Jianan Ji, Kit Ao, Praveen Velliengiri, Xupeng Miao,
  Cui, Xiaobing Feng, and Christos Kozyrakis. 2023.             Oded Padon, and Zhihao Jia. 2025. Mirage: A multi-
  Honeycomb: Secure and efficient GPU executions                level superoptimizer for tensor programs. In 19th
  via static validation. In 17th USENIX Symposium               USENIX Symposium on Operating Systems Design
  on Operating Systems Design and Implementation                and Implementation (OSDI 25).
  (OSDI 23), pages 155–172, Boston, MA. USENIX
  Association.                                                 Yichen Xie and Alex Aiken. 2007. Saturn: A scalable
                                                                 framework for error detection using boolean satisfia-
NVIDIA Corporation. 2024. CUDA Toolkit Documen-                  bility. ACM Trans. Program. Lang. Syst., 29(3):16–
  tation: Compiler.                                              es.

OpenAI. 2023. Gpt-4 technical report.       https://           An Yang, Baosong Yang, Beichen Zhang, Binyuan
  cdn.openai.com/papers/gpt-4.pdf.                               Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayi-
                                                                 heng Liu, Fei Huang, Haoran Wei, Huan Lin, Jian
Massimiliano Poletto and Vivek Sarkar. 1999. Linear              Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Ji-
 scan register allocation. ACM Trans. Program. Lang.             axi Yang, Jingren Zhou, Junyang Lin, Kai Dang, and
 Syst., 21(5):895–913.                                           23 others. 2025. Qwen2.5 technical report. Preprint,
                                                                 arXiv:2412.15115.
Fernando Magno Quintão Pereira and Jens Palsberg.
  2008. Register allocation by puzzle solving. In Pro-         Chenggang Zhao, Chengqi Deng, Chong Ruan, Damai
  ceedings of the 29th ACM SIGPLAN Conference on                 Dai, Huazuo Gao, Jiashi Li, Liyue Zhang, Pan-
  Programming Language Design and Implementation,                pan Huang, Shangyan Zhou, Shirong Ma, Wenfeng
  PLDI ’08, pages 216–226, New York, NY, USA. As-                Liang, Ying He, Yuqing Wang, Yuxuan Liu, and
  sociation for Computing Machinery.                             Y. X. Wei. 2025. Insights into deepseek-v3: Scaling
                                                                 challenges and reflections on hardware for ai archi-
Jonathan Ragan-Kelley, Connelly Barnes, Andrew                   tectures. Preprint, arXiv:2505.09343.
  Adams, Sylvain Paris, Frédo Durand, and Saman
                                                               Lianmin Zheng, Chengfan Jia, Minmin Sun, Zhao Wu,
  Amarasinghe. 2013. Halide: a language and compiler
                                                                 Cody Hao Yu, Ameer Haj-Ali, Yida Wang, Jun Yang,
  for optimizing parallelism, locality, and recomputa-
                                                                 Danyang Zhuo, Koushik Sen, Joseph E. Gonzalez,
  tion in image processing pipelines. In Proceedings
                                                                 and Ion Stoica. 2020. Ansor: Generating High-
  of the 34th ACM SIGPLAN Conference on Program-
                                                                 Performance tensor programs for deep learning. In
  ming Language Design and Implementation, PLDI
                                                                 14th USENIX Symposium on Operating Systems De-
  ’13, pages 519–530, New York, NY, USA. Associa-
                                                                 sign and Implementation (OSDI 20), pages 863–879.
  tion for Computing Machinery.
                                                                 USENIX Association.
Ilya Sutskever, Oriol Vinyals, and Quoc V Le. 2014. Se-        Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue
   quence to sequence learning with neural networks. In           Sun, Jeff Huang, Cody Hao Yu, Shiyi Cao, Chris-
   Advances in neural information processing systems,             tos Kozyrakis, Ion Stoica, Joseph Gonzalez, Clark
   pages 3104–3112.                                               Barrett, and Ying Sheng. 2024. Sglang: Efficient
                                                                  execution of structured language model programs. In
Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob
                                                                 Advances in Neural Information Processing Systems
  Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz
                                                                 37 (NeurIPS 2024).
  Kaiser, and Illia Polosukhin. 2017. Attention is all
  you need. In Advances in neural information pro-
  cessing systems, pages 5998–6008.


                                                          10
A    Kernel Configurations                                    B       ChatGPT Results
A GEMM kernel calculates C = α · A × B + β · C                We analyze ChatGPT’s behavior1 on the register al-
with matrices A ∈ RM ×K , B ∈ RK×N , and                      location task and observe substantial limitations in
C ∈ RM ×N . To comprehensively evaluate register              its ability to handle this core compiler optimization.
allocation strategies, we vary the matrix dimen-              As shown in Figure 3, ChatGPT outputs a naive
sions M , N , and K across a range of values from             sequential assignment strategy that fails to employ
2 to 16, resulting in 15 × 15 × 15 = 3, 375 distinct          register reuse. This is reflected in the monotoni-
problem configurations. This breadth of configura-            cally increasing register identifiers (vgpr1 through
tions allows us to observe how register allocation            vgpr15), with no attempt to recycle registers whose
patterns adapt to different memory access patterns            associated variables have expired. The result sug-
and computational requirements.                               gests a lack of liveness-aware reasoning and high-
   MHA is the defining component of Transformer               lights the need for more specialized modeling or
architectures, consisted of several computational             structural supervision to support compiler-level cor-
phases: (1) projection of queries, keys, and values           rectness.
through linear transformations, (2) computation of
attention scores through scaled dot-product atten-
tion, and (3) application of attention weights to val-
ues, followed by a final linear projection. This com-
plex sequence of operations introduces intricate de-
pendencies and memory access patterns, making
optimal register allocation particularly challenging
and impactful for performance.
   We sample a large configuration space inspired
by real LLM inference workloads:                                        Figure 3: Allocation Result from ChatGPT
• Heads: [16, 24, 32, 40, 64, 128]
• Batch Size: [1, 32, 64, 128, 256, 512, 1024]
• Head Dim: [32, 40, 59, 64, 80, 96, 111, 128, 160,
  192, 224, 256]
• Sequence Length: [2048]
• Attention Group: [1, 4, 8]
This parameter space yields 6 × 7 × 12 × 1 × 3 =
1, 512 distinct configurations, representing a com-
prehensive sampling of the operational demands
placed on modern LLM inference systems.




                                                                  1
                                                                  https://chatgpt.com/share/682a07f9-bf50-8006-
                                                              a7ac-f07b439439e4


                                                         11
