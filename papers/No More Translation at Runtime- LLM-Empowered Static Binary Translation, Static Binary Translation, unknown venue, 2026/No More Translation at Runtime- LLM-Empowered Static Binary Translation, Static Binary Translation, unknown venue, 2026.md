                                           No More Translation at Runtime: LLM-Empowered
                                                      Static Binary Translation
                                                          Zhibo Liu∗                                   Huaijin Wang                              Wai Kin Wong
                                               State Key Laboratory of Novel                      The Hong Kong University of              The Hong Kong University of
                                                    Software Technology,                            Science and Technology                   Science and Technology
                                                     Nanjing University                                Hong Kong, China                         Hong Kong, China
                                                       Nanjing, China                                 hwangdz@cse.ust.hk                      wkwongal@cse.ust.hk
                                                    zhiboliu@nju.edu.cn

                                                                               Daoyuan Wu∗                                  Shuai Wang†
                                                                             Lingnan University                       The Hong Kong University of
arXiv:2610.05999v1 [cs.OS] 5 Oct 2026




                                                                             Hong Kong, China                           Science and Technology
                                                                           daoyuanwu@ln.edu.hk                             Hong Kong, China
                                                                                                                          shuaiw@cse.ust.hk
                                        Abstract                                                                  producing binaries with near-native performance. Further-
                                        While AArch64 CPUs are becoming strong market contenders,                 more, it shows substantial improvements over the leading
                                        their software ecosystem lags behind the mature x86-64 en-                industrial translator, ExaGear, illuminating a promising new
                                        vironment, hindering the adoption of the new architectures                direction for cross-architecture binary translation research.
                                        and impacting user experience. Binary translation bridges
                                                                                                                  CCS Concepts: • Software and its engineering → Trans-
                                        this divide by converting binary code from one architecture
                                                                                                                  lator writing systems and compiler generators; Auto-
                                        (e.g., x86-64) to run on another (e.g., AArch64), allowing
                                                                                                                  matic programming; Software verification; • Security and
                                        legacy software to benefit from modern hardware’s perfor-
                                                                                                                  privacy → Software reverse engineering; • Computer sys-
                                        mance and energy efficiency advantages.
                                                                                                                  tems organization → Architectures.
                                           Current translation methods are typically either dynamic,
                                        which adds significant runtime overhead, or static, which                 Keywords: Binary Translation, Cross-Architecture Migra-
                                        struggles with reliability due to the inherent complexities of            tion, Large Language Models, Reverse Engineering
                                        binary analysis. This paper introduces a new static, assembly-
                                        to-assembly translation paradigm that transforms binary                   ACM Reference Format:
                                        code ahead of execution, generating portable, efficient native-           Zhibo Liu, Huaijin Wang, Wai Kin Wong, Daoyuan Wu, Shuai Wang.
                                        like binaries that run on AArch64 devices without runtime                 2026. No More Translation at Runtime: LLM-Empowered Static
                                        frameworks. Benefiting from recent breakthroughs in large                 Binary Translation. In European Conference on Computer Systems
                                                                                                                  (EUROSYS ’26), April 27–30, 2026, Edinburgh, Scotland Uk. ACM, New
                                        language models (LLMs), we provide a practical and auto-
                                                                                                                  York, NY, USA, 18 pages. https://doi.org/10.1145/3767295.3803600
                                        mated translation engine that produces high-quality code
                                        with minimal human intervention. To ensure correctness,
                                        we introduce a crucial verification step, where we split the              1    Introduction
                                        assembly code into simplified snippets, enabling efficient
                                                                                                                  The computing hardware landscape is shifting away from
                                        and scalable semantic verification.
                                                                                                                  the long-standing dominance of x86-64, driven by the rise of
                                           Our evaluation shows that this approach significantly out-
                                                                                                                  alternative Instruction Set Architectures (ISAs) like ARM and
                                        performs existing open-source solutions with a large margin,
                                                                                                                  RISC-V [43, 93]. AArch64 has already achieved significant
                                                                                                                  success in mobile devices and is now making remarkable
                                        ∗ Work done while the author was associated with HKUST.
                                        † Corresponding author.
                                                                                                                  strides in the PC market with processors like Apple’s Silicon
                                                                                                                  chips [5, 6]. Their high performance and energy efficiency
                                                                                                                  have spurred major manufacturers to develop and promote
                                                                                                                  AArch64 CPUs. Notable examples include Huawei’s Kun-
                                                                                                                  peng server chips [54] and Qualcomm’s Snapdragon X Elite
                                        This work is licensed under a Creative Commons Attribution-               processor for Windows laptops [80, 89].
                                        NonCommercial-NoDerivatives 4.0 International License.
                                        EUROSYS ’26, Edinburgh, Scotland Uk
                                                                                                                     Despite the advantages of ARM-based chips, their wide-
                                        © 2026 Copyright held by the owner/author(s).                             spread adoption is hindered by a major software hurdle.
                                        ACM ISBN 979-8-4007-2212-7/26/04                                          While the AArch64 software ecosystem is thriving, decades
                                        https://doi.org/10.1145/3767295.3803600                                   of software development have been optimized for x86-64.
EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk                                                            Zhibo Liu et al.


Legacy applications often lack available source code or com-      • We present an automatic binary translation pipeline that
plete build environments, making a source-based recompila-          leverages LLMs to construct the translation engine, dras-
tion non-viable [7].                                                tically reducing the reliance on costly expert knowledge
   To bridge this gap, chip manufacturers and researchers           and manual effort. Meanwhile, our approach simplifies
have turned to binary translation[8, 17, 80], which converts        the translation task for LLMs by splitting code into snip-
binary code from one ISA to another, allowing seamless              pets, allowing for straightforward equivalence checking
software migration from an old architecture to a new one.           to ensure correctness and scalability.
Prominent examples include Apple’s Rosetta 2 [8] for ma-          • We present an academic binary translation framework
cOS, Huawei’s ExaGear [58] for its Kunpeng-powered Linux            with performance that rivals leading industrial tools. Eval-
systems, and Microsoft’s Prism [80] for Windows on ARM.             uation shows that our research prototype, LLMSbt, sig-
   While existing binary translation solutions have facili-         nificantly outperforms existing open-source solutions and
tated the rapid growth of the AArch64 ecosystem, they are           even surpasses a leading industrial dynamic binary transla-
often limited by their low reliability or high runtime over-        tor, ExaGear, in some real-world scenarios. The translated
head. Specifically, static translators lift assembly code to a      binaries achieve near-native performance while remaining
higher-level, platform-independent intermediate representa-         portable. We also analyze the remaining runtime over-
tion (IR) (e.g., LLVM IR) before recompiling it for a new plat-     heads, discuss LLMSbt’s limitations, and suggest potential
form [12, 114]. This process is fundamentally challenged by         improvements for future research.
the undecidable problem of statically recovering high-level
semantic information [55], such as symbols and variables,
                                                                  2     Background
that is discarded during compilation. Differently, dynamic
solutions translate code at runtime [15, 41, 58], which not       2.1   Binary Analysis and Reverse Engineering
only incurs extra performance overhead, but also restricts        Disassembly. Disassembly is the foundational process of
the portability of translated software, preventing it from        converting binary into human-readable assembly. Two pri-
migrating to platforms without the translation framework.         mary disassembly techniques are linear sweeping and re-
   Moreover, state-of-the-art binary translation tools are        cursive traversal. Linear sweeping [33] decodes all bytes
closed-source and platform or CPU-specific [8, 58, 80], cre-      in the executable region sequentially, while recursive tra-
ating barriers for research aiming to enhance modern bi-          versal [65] begins at a designated entry point and decodes
nary translation techniques. The complexity of modern ISAs        following control transfer instructions. Recently, machine
makes developing a cross-architecture translator a daunting       learning techniques have emerged, utilizing neural networks
task, requiring substantial expertise and effort to identify      to map binary bytes to assembly instructions [84, 115, 116].
equivalent instructions across ISAs and examine their subtle      Despite decades of research, perfect disassembly remains elu-
semantic differences. These challenges have slowed academic       sive. Disassemblers struggle with indirect jumps and calls,
research, highlighting the need for an automated solution.        as they cannot statically determine all control flow targets,
   To address these limitations, we present a new paradigm        often resulting in incomplete and inaccurate outputs [4, 64].
for cross-architecture binary translation. Leveraging recent      Symbolization. A key challenge in reverse engineering is
advances in reverse engineering research and LLMs, we pro-        the loss of symbolic information during compilation. Pro-
pose a static assembly-to-assembly translation paradigm that      grammer defined symbols such as functions, variables, and
converts x86-64 binaries to AArch64 ahead of time, eliminat-      labels are discarded, leaving only constant offsets in the
ing runtime translation overhead while producing portable         binary. As depicted in Fig. 1, these symbols become indistin-
binaries that can run natively on AArch64 platforms. Fur-         guishable from other constants, leading to what is known
thermore, given LLMs’ success in multilingual translation         as the symbolization problem [103, 104]. This poses a signifi-
and various coding tasks [21, 26, 48, 67, 72], we explore their   cant hurdle for recompilation, as new addresses assigned by
potential to facilitate binary translator development, mini-      compilers may lead to incorrect symbol references.
mizing the reliance on extensive expert knowledge. Addition-         To address this, researchers have developed advanced re-
ally, we parameterize translation results to generate reusable    assemblable disassembling techniques [38, 42, 103, 104, 110].
translation rules to expedite future translations.                Notable approaches leverage binary analysis and relocation
   In summary, this paper makes the following contributions:      information in position-independent code (PIC) to identify
• We advocate for increased research in binary translation        code and data pointers [38, 110]. They focus on recovering
   to support software migration for new architectures like       lost symbols in disassembled code and have proven highly
  AArch64. To this end, we introduce a novel static assembly-     reliable. Recent advancements have even introduced sound
   to-assembly translation paradigm that utilizes advanced        binary rewriting techniques [63], with many resulting tools
   binary rewriting techniques to produce portable binaries       rigorously tested and validated [64] in numerous real-world
  with performance comparable to native counterparts.             applications. Fig. 1 illustrates how proper symbolization en-
                                                                  ables correct symbol references during recompilation.
Merge two code examples into one                                                      EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk


               x86-64        mov $0x10a0, %rax                          General Workflow. A typical binary translator begins by
                             jmp *%rax
                                                                        disassembling the binary software to extract its assembly
                       109b: 0xdeadbeef
                       10a0: "\x89\x04\x25                              code. Then, depending on the translator’s design, it can di-
                             \x00\x00\x00\x00"                          rectly translate the assembly code to the host ISA, or lift as-
            Not Symbolized                      Symbolized
             mov $0x10a0, %rax        mov .label, %rax                  sembly to a platform-independent IR, which is then lowered
             jmp *%rax                jmp *%rax                         to host assembly using established compiler infrastructures
            .data:                   .data:
             0xdeadbeef               0xdeadbeef                        (e.g., LLVM). For efficiency, instructions are often organized
             "\x89\x04\x25           .label:
             \x00\x00\x00\x00"        mov $15, %eax                     and translated in translation blocks (TBs) [17, 69] that are
                              Compile                                   typically stored in a cache to avoid redundant translations.
             mov $0x10a0, %rax        mov $0x10c0, %rax                 Terminology. In this paper, the term binary translators
             jmp *%rax                jmp *%rax
            10a0:                   10c0:                               refers to tools for translating and migrating binary software
             0xdeadbeef               mov $15, %eax
                                                                        across architectures. However, existing tools use distinct
                                                                        technical approaches with different IRs and translation styles
              Figure 1. An example of symbolization.                    employed, significantly impacting their capabilities and per-
                                                                        formance. To differentiate these approaches clearly, we ex-
                                                                        tend the terminology developed in recent studies [74, 83]
    Symbolic Execution. Symbolic execution is a powerful pro-           and categorize them into four types:
    gram analysis technique that verifies program properties for        Concise IR Lifter. These tools aim to recover LLVM IR that
    all possible inputs [13, 20, 85]. Instead of using concrete data,   closely resembles the IR code generated by compiling source
    it executes a program with symbolic values and tracks them          code. They lift low-level binary code to high-level, concise,
    throughout the program. When a branch is encountered, it            and human-readable IR, attempting to restore source-level
    explores both paths separately, generating a set of symbolic        information (e.g., variables, types, and symbols). Notably,
    constraints that represent the conditions required to reach         works like Mctoll [114], RetDec [12], and Rev.ng [35, 36] have
    specific program states. These constraints can be evaluated         dedicated significant effort in this direction. One subsequent
    by SMT solvers [32, 71] to check for satisfiability and verify      advancement, Lasagne [91], has further enhanced Mctoll’s
    program properties. Symbolic execution has proven effective         capabilities for concurrent programs. Ideally, such lifters
    for analyzing binary code [86, 88, 102], offering a rigorous        offer high flexibility, as the lifted IR can naturally provide
    approach to verify translated binary code.                          cross-architecture portability and can be readily analyzed
                                                                        and optimized using established LLVM-based tools.
                                                                           However, perfect IR lifting faces multiple fundamental
    2.2   Large Language Models
                                                                        challenges, including incomplete control flow graph (CFG)
    Recent breakthroughs in LLMs have demonstrated their effec-         recovery [36, 79, 95] and the loss of high-level abstractions
    tiveness in various natural language processing tasks like ma-      like functions and variables in binary code [51, 113]. Con-
    chine translation and text summarization [21, 108, 118]. Their      sequently, these tools often do not prioritize functionality
    application has also extended to code-related tasks, such as        preservation; instead, they are primarily used for automated
    code completion and compilation [26, 48, 121]. The power            program analysis, binary similarity comparison [78], and
    of LLMs stems from their extensive training on high-quality         reverse engineering tasks like decompilation [77]. Our eval-
    data, which cultivates sophisticated reasoning and inference        uation confirms that they are not suitable for reliable cross-
    capabilities for tasks that traditionally required significant      architecture binary translation.
    human expertise. Inspired by this, our work explores the            Emulational IR Lifter. In light of the difficulties in recov-
    potential of LLMs for cross-architecture instruction transla-       ering high-level abstractions from binary code, another line
    tions, yielding promising results. However, LLMs are known          of research focuses on emulating the binary’s semantics at
    for their unpredictability; they can produce plausible but          the IR level. These lifters translate each machine instruc-
    incorrect outputs with no guarantee of correctness [57, 117].       tion into a sequence of IR statements that precisely mimic
    To mitigate this risk and prevent the generation of erroneous       its effects on a virtual CPU in lifted IR code [74, 83]. For
    binaries, we introduce a crucial rigorous semantic equiva-          example, McSema [37, 81] maintains a dedicated structure
    lence check step, detailed in Sec. 4.4.                             in lifted IR to represent the CPU state, including registers
                                                                        and flags. A similar paradigm is employed by dynamic lifters
    2.3   Binary Translation                                            like Instrew [40, 41] and BinRec [3]. Two subsequent vari-
    Binary translation has been a long-standing topic of aca-           ants of BinRec, named WYTIWYG [83] and Polynima [34],
    demic research [97, 106]. This paper focuses specifically on        while enhancing its support for stack-layout recovery and
    user-level binary translation, which handles general applica-       concurrent programs, still fall into this emulational category.
    tions [15, 29, 61, 98, 107], as opposed to system-level binary
    translation that targets operating systems (OSes) [61].
EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk                                                                         Zhibo Liu et al.


      Table 1. Relevant binary translators investigated.                        LLMSbt mitigates these issues by automating the trans-
                                                                             lation process using LLMs. Its static paradigm allows us to
                              IR     Functional                  Primary     incorporate LLMs and rigorous verification into the transla-
                   Type                         Flexibility∗
                             Used     Fidelity                     Goal
 Mctoll [114]     Static    LLVM        Low        High          Readable
                                                                             tion process. Moreover, by decoupling the translation frame-
 RetDec [12]      Static    LLVM        Low        High          Concise     work from translation rules, we transform translation into
 Rev.ng [36]      Static    LLVM        Low        High             IR
                                                                             a data-driven process. As a result, developing the transla-
 McSema [81]      Static    LLVM      Medium     Medium            High-
 Instrew [41]    Dynamic    LLVM       High      Medium           Fidelity   tor requires minimal expert knowledge, as rules are mostly
 BinRec [3]      Dynamic    LLVM       High      Medium              IR      extracted from LLM-generated examples.
 QEMU [15]       Dynamic     TCG        High         Low
                                                                Reliable &      It is important to note, however, LLMSbt is not intended to
                                                                 Portable    replace the mature binary translators developed by industry
 ExaGear [58] Dynamic        None       High         Low           High
 LLMSbt        Static        None       High         Low       Performance   over the years. Binary translation remains a highly complex
∗ In this context, flexibility is defined as the ease of porting to new      field requiring substantial engineering effort (e.g., QEMU
architectures and applying standard compiler analyses and optimizations.     consists of over one million LoC, and Huawei has spent
                                                                             more than five years refining ExaGear). Because there are
                                                                             still many unresolved problems requiring further research,
                                                                             this work primarily contributes new concepts and a novel
   Despite guaranteeing a high degree of functionality, this                 translation paradigm to the community.
approach sacrifices the benefits of LLVM IR as a strongly-
typed IR. The lack of high-level semantic information, such as               Previous Works to Compare. To position our work, Table 1
types, hinders automated analysis and optimization [74, 83].                 presents a qualitative synthesis and taxonomy of representa-
Furthermore, this emulational strategy often introduces extra                tive translators. Specifically, the classification is grounded
code in translated binary, resulting in inefficiency [74, 83].               from a recent research [74], whose observations have been
Given that static lifting struggles with complete CFG re-                    confirmed by subsequent studies [83, 119]. We adopt this
covery (McSema relies on the de facto disassembler IDA                       established terminology and taxonomy while expanding
Pro [53] for CFG recovery and disassembly), dynamic lifters                  our scope to include four additional tools (Rev.ng, Instrew,
like Instrew defer IR compilation and optimization to run-                   QEMU, and ExaGear) for a more thorough discussion. Within
time, which further exacerbates performance issues.                          this taxonomy, functional fidelity refers to the strictness of
Low-level IR Translator. This category of works [15, 90],                    semantic preservation. High fidelity ensures full recompil-
which includes CPU emulators like QEMU, forgoes the cross-                   ability, while low fidelity prioritizes static analysis and code
architecture benefits of LLVM IR in favor of a lower-level                   comprehension over executability. Although McSema faith-
IR that more closely mirrors machine code. For decades,                      fully lifts all individual instructions for small-scale bench-
QEMU [15] has been widely adopted in industry and academia                   marks [30], its performance in our evaluation justifies a
due to its high reliability.                                                 medium fidelity rating (as detailed in Table 5). Flexibility
   Recent studies, however, indicate that QEMU can be over                   follows a similar categorization. High flexibility indicates
10× slower than native execution [112]. This performance                     the recovery of strongly-typed IR compatible with standard
penalty stems from a fundamental trade-off between scala-                    compiler passes, while low flexibility refers to methods tied
bility and portability. To support a variety of architectures,               to hardware specifics such as direct assembly translation.
QEMU uses a lower-level IR (TCG IR) [15, 17]. Each CPU                       Emulational IR lifters occupy a middle ground, producing IR
instruction is decomposed into several micro-operations                      that allows for cross-target lowering but lacks support for
in TCG IR, which are implemented in high-level program-                      standard compiler analysis.
ming languages and compiled into native host machine code.                       Table 1 highlights the functional and structural limita-
While this shields developers from the intricacies of complex                tions of current approaches. Our investigation found that
ISAs and hardware specifics, it limits low-level optimiza-                   while BinRec shows promising performance, it is designed
tion opportunities and introduces inefficiencies compared to                 for same-architecture recompilation and optimization and is
hand-tuned assembly, leading to substantial overhead.                        unsuitable for cross-architecture translation because it must
Assembly Translator. To achieve maximum performance,                         concatenate the lifted binary with the original. Concise IR
industrial dynamic translators like ExaGear [58] bypass IRs                  lifters, despite backing from notable technology companies,
and translate guest instructions directly into native host                   often fail to deliver fully functional results (more details of
instructions, leveraging hardware features and delivering                    their failures in the Appendix A.1). In fact, tools like RetDec
near-native performance. The downside is that developing                     and Rev.ng primarily aim at software decompilation, treating
the translation logic is labor-intensive, error-prone, and typ-              translation failures and semantic mismatches as low-priority
ically tailored for specific platforms, limiting portability and             issues [100]. Consequently, our evaluation mainly compares
reusability. Moreover, the dynamic paradigm they employed                    LLMSbt with state-of-the-art in each category: McSema, In-
also introduces substantial runtime overhead.                                strew, QEMU, and ExaGear. Sec. 3 further discusses more
                                                                                  EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk


design choices and rationales of LLMSbt, aiming for high            translation patterns, previously generated translations can
reliability and runtime efficiency.                                 be parameterized and reused to accelerate future translation.
   We also acknowledge recent advancements in this do-              3) Scalable Semantic Verification. CPU instruction seman-
main that solve specific complexities, such as concurrent           tics are often intricate, and even experienced developers may
programs [34, 46, 91] and stack-layout recovery [83], in mod-       mistranslate subtle semantic details. Modern ISAs, particu-
ern software. They are not separately listed as they are pri-       larly complex instruction set computing (CISC) architectures
marily built upon works already covered in Table 1, with            like x86-64, contain a vast number of instructions, forcing
their core designs remaining unchanged. We further discuss          developers to spend significant time consulting manuals and
them in Sec. 8.                                                     designing test cases to ensure accurate translation. This is a
                                                                    tedious and error-prone process that still does not guarantee
                                                                    correctness. While methods like symbolic execution can rig-
3   Motivation
                                                                    orously verify binary code, they often face scalability issues
As discussed in Sec. 2.1, static disassembly struggles to re-       due to path explosion [92].
solve indirect control flow targets and symbols missed during          Verifying translation correctness is a difficult but essential
compilation. While some static translators employ mature            challenge. To address this, we introduce an efficient static
commercial disassemblers like IDA Pro [53] to partially mit-        verification method. Instead of verifying an entire complex
igate these issues [81], they remain brittle in general sce-        program, we split assembly code into small, manageable
narios. This unreliability discourages the adoption of static       snippets that can be easily verified with symbolic execution
disassembly in translators where execution correctness is           and then reassembled. This method provides instant feedback
paramount. Consequently, industrial binary translators typ-         to human experts or LLMs, streamlining the development of
ically rely on dynamic disassembly, which necessitates a            robust binary translators.
dynamic translation paradigm and introduces significant
runtime overhead, preventing them from producing portable
binaries, i.e., a guest binary can only execute on platforms        4     Design
with the translator installed.                                      This work formulates a new translation paradigm, outlining
   To overcome these fundamental limitations, we introduce          a concrete methodology for developing a high-performance,
a new translation paradigm centered around the following            portable binary translator empowered by LLMs. We present
major conceptual contributions:                                     LLMSbt, a static binary translator for migrating x86-64 soft-
1) Static Assembly-to-Assembly Translation. As noted                ware to AArch64 platforms. This section presents a design
in Sec. 2.1, recent advancements in binary rewriting present        overview and then examines each component in detail.
a unique opportunity for static binary translation. Leveraging
these binary rewriting techniques, we propose a novel static
translation paradigm that translates assembly code, bypass-         4.1   Overview
ing the challenges of IR lifting and ensuring high reliability.     As shown in Fig. 2, the translation process starts with stan-
Furthermore, the static paradigm reduces runtime overhead           dard disassembly. What distinguished our approach is the
and produces portable, native-like binaries, opening new            use of advanced binary rewriting techniques to transform
avenues for research and downstream optimization.                   disassembled code into a symbolic, reassembleable form.
2) Automated Translator Development. State-of-the-art               We then split the binary code into snippets (①), with each
industrial binary translators like Rosetta 2 [8] and ExaGear [58]   snippet representing a code block in a Static Single Assign-
are closed-source and tailored to specific hardware and OSes,       ment (SSA)-like format [27, 28, 101]. For clarity, we use “SSA”
lacking support for general AArch64 processors. Meanwhile,          throughtout the paper to refer to our adapted concept, which
existing open-source translators [3, 41, 81] are unsuitable for     differs slightly from the traditional SSA used in compiler re-
our static assembly-to-assembly paradigm because they lift          search (as explained in Sec. 4.2). The SSA representation
assembly to IRs (as introduced in Sec. 2), which inevitably         enables independent translation of each snippet. For each
introduces unnecessary overhead. Building a new translator          snippet, we first query the translation rule database for ex-
from scratch is a formidable task that requires a tremendous        isting, reusable translations (②). If no cached translation can
engineering effort. The absence of open, efficient translators      be reused, our LLM-powered engine translates the snippet
for general AArch64 platforms hinders further research.             (③); otherwise, the existing translation rule in the database
   To establish a practical foundation for future research, we      is applied. Once snippets are translated, we employ sym-
introduce a novel binary translation pipeline. Specifically, we     bolic verification to ensure the semantic correctness of the
propose using LLMs to automatically generate translation re-        translated snippets (④). Finally, we stitch translated snippets
sults, replacing the need for human experts. This approach is       into complete, compilable assembly code (⑤ and ⑦). More-
economically viable due to the affordability of modern LLMs.        over, to minimize the cost of repeatedly querying the LLM
Furthermore, since many instruction variants share similar          for similar code, we further parameterize translation results
EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk                                                                                       Zhibo Liu et al.


                                                                      ①                    ②                          ③     You are an
                  x86-64           x86-64                                                                                 assembly code
                                                                           Snippets
                  Binary          Assembly         Binary Code                                                            expert, please
                                                                                                   Translation Rule
                                                     Splitting             x86-64                                         translate the
                                                                                                      Database
                                                                                                                            following
                                                                                                             ⑥                code…

                                                                      ⑦                    ⑤                          ④
                  AArch64        AArch64
                                                                           Snippets                                            Translation
                   Binary        Assembly                                                             Semantic
                                                 Snippets Stitching                                                              Engine
                                                                          AArch64                    Verification



                                                         Figure 2. Overview of LLMSbt.

into reusable rules for future translations (⑥). The following               Algorithm 1: Splitting Basic Block to SSA Snippets
subsections elaborate on each of these components.                           1 Function Split(𝐵𝐵𝑖𝑛𝑠𝑡𝑟𝑠 : a list of instructions from a basic block)
                                                                             2    𝑆 ← ∅;
                                                                             3    𝐶𝑢𝑟𝑟𝑒𝑛𝑡𝑆𝑛𝑖𝑝𝑝𝑒𝑡 ← [ ];
                                                                             4    𝐴𝑠𝑠𝑖𝑔𝑛𝑒𝑑𝑉 𝑎𝑟𝑠 ← ∅ ;               // variables assigned in
                                                                                    𝐶𝑢𝑟𝑟𝑒𝑛𝑡𝑆𝑛𝑖𝑝𝑝𝑒𝑡
4.2   Binary Code Splitting
                                                                             5    foreach 𝑖𝑛𝑠𝑡𝑟 in 𝐵𝐵𝑖𝑛𝑠𝑡𝑟𝑠 do
Translating entire programs or functions poses significant                   6         𝐷𝑒 𝑓 𝑖𝑛𝑒𝑑𝑉 𝑎𝑟𝑠 ← GetDefinedVariables(instr);
hurdles to LLMs and verification. The extensive context                      7         if 𝐴𝑠𝑠𝑖𝑔𝑛𝑒𝑑𝑉 𝑎𝑟𝑠 ∩ 𝐷𝑒 𝑓 𝑖𝑛𝑒𝑑𝑉 𝑎𝑟𝑠 ≠ ∅ then
length required, coupled with intricate data and control flows               8              Add 𝐶𝑢𝑟𝑟𝑒𝑛𝑡𝑆𝑛𝑖𝑝𝑝𝑒𝑡 to 𝑆;
in assembly code, often exceeds the reasoning capabilities                   9              𝐶𝑢𝑟𝑟𝑒𝑛𝑡𝑆𝑛𝑖𝑝𝑝𝑒𝑡 ← [𝑖𝑛𝑠𝑡𝑟 ];
                                                                                            𝐴𝑠𝑠𝑖𝑔𝑛𝑒𝑑𝑉 𝑎𝑟𝑠 ← 𝐷𝑒 𝑓 𝑖𝑛𝑒𝑑𝑉 𝑎𝑟𝑠;
of LLMs. Additionally, verifying the correctness of large-                  10
                                                                            11         else
scale translated code is a difficult task. Drawing inspiration              12              Append 𝑖𝑛𝑠𝑡𝑟 to 𝐶𝑢𝑟𝑟𝑒𝑛𝑡𝑆𝑛𝑖𝑝𝑝𝑒𝑡 ;
from the divide-and-conquer strategy [96], we propose a                     13              𝐴𝑠𝑠𝑖𝑔𝑛𝑒𝑑𝑉 𝑎𝑟𝑠 ← 𝐴𝑠𝑠𝑖𝑔𝑛𝑒𝑑𝑉 𝑎𝑟𝑠 ∪ 𝐷𝑒 𝑓 𝑖𝑛𝑒𝑑𝑉 𝑎𝑟𝑠;
fine-grained translation approach. Our method focuses on
translating small code snippets formatted in SSA form. The                  14        if 𝐶𝑢𝑟𝑟𝑒𝑛𝑡𝑆𝑛𝑖𝑝𝑝𝑒𝑡 is not empty then
                                                                            15            Add 𝐶𝑢𝑟𝑟𝑒𝑛𝑡𝑆𝑛𝑖𝑝𝑝𝑒𝑡 to 𝑆;
snippets are generally concise enough for LLMs to compre-
hend and process. The SSA form simplifies data and control                  16        return 𝑆 ;               // Output: A list of SSA snippets
flows, minimizing potential errors introduced by LLMs and                   17 Function GetDefinedVariables(𝑖𝑛𝑠𝑡𝑟 )
enabling the semantic verification of the translation.                      18    𝐷 ← ∅;
Adapted SSA. Through static analysis, we break down each                    19    if 𝑖𝑛𝑠𝑡𝑟 writes to memory then
                                                                                       // For simplicity, all memory is treated as
basic block into SSA snippets. Here, SSA requires that within
                                                                                           one variable.
each snippet, a variable is assigned a value at most once (i.e.,            20         𝐷 ← 𝐷 ∪ {MEMORY};
single assignment). Unlike the traditional SSA concept used
                                                                            21        𝑅𝑑𝑒𝑠𝑡 ← destination registers of 𝑖𝑛𝑠𝑡𝑟 ;
in compiler research, our adaptation includes cases where                   22        𝐷 ← 𝐷 ∪ 𝑅𝑑𝑒𝑠𝑡 ;
a variable might be used before definition. This distinction                23        return 𝐷;
arises because, unlike high-level languages, variables in as-
sembly (such as registers and memory) are inherently defined
by the hardware state and are never truly undefined.
Splitting. This step starts with symbolized assembly code.                  4.3       LLM-Empowered Translation
The splitting process is guided by the core principle of single             Each x86-64 snippet is then translated to AArch64 individ-
assignment to reduce complexity. As illustrated in Alg. 1, we               ually with an LLM. However, directly translating assembly
linearly scan the assembly instructions (lines 6, 13), tracking             code with LLMs can be error-prone, particularly with com-
which variables are assigned at each instruction. Whenever                  plex CISC ISAs like x86-64. While LLMs generally possess
a previously assigned variable is rewritten (line 7), we split              knowledge of relevant instructions, they can produce in-
preceding instructions into a snippet and reset the track                   correct translations due to insufficient context or limited
(lines 8–10). This process continues until the end of a basic               reasoning capabilities. To meet the strict correctness require-
block, where control flow transfers naturally conclude a                    ments of binary translation, we design a domain-specific
snippet. Due to the intangibility of statically determining                 prompt architecture that adapts recent advances in prompt
the address of memory accesses, we treat all memory as a                    engineering to the constraints of assembly language.
single variable for simplicity. This means each snippet can                 Semantic-Grounded Reasoning. First, LLMs can exhibit
have at most one memory access. This step yields a list of                  shallow reasoning, opting for superficial interpretations rather
SSA snippets ready for independent translation.                             than performing a deep semantic analysis of the code. To
                                                                                             EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk


address this issue, we implement a specialized task-splitting                         x86-64 code:                          Ref Example:
                                                                                       addl $1, -8(%rbp)                    addl $3, (%rbp)
strategy, effectively adapting chain-of-thought (CoT) prompt-                                                        DB
ing [109] to the binary domain, which instructs the LLM to                                                                  ldr w3, [x29]
                                                                                                    “It adds an             adds w3, w3, #3
interpret the assembly code before translating it. This prelim-                         Interpret   immediate...”           str w3, [x29]
inary interpretation step grounds the LLM’s understanding                                                                                pass
                                                                                                                     pass
of code’s semantics, promoting more accurate and deliberate                            Translate          Compile             Verify
reasoning. We strategically choose not to verify this inter-                                                  fail                fail
                                                                                          Fix
mediate interpretation, acknowledging that hallucinations
                                                                                                    parameterize AArch64 code:
can occur at any stage. Instead, we treat interpretation as                                                           ldr w3, [x29, #-0x8]
an auxiliary cognitive scaffold to prime the model, focusing                                                          adds w3, w3, #1
                                                                                                     DB               str w3, [x29, #-0x8]
our rigorous formal verification efforts exclusively on the
final executable output (see Sec. 4.4). For example, as shown
                                                                                      Figure 5. Workflow of iterative refinement.
in Fig. 3, the LLM initially misinterprets an instruction as
moving the address of label .LCd0 into x1. However, by first
prompting the LLM for a semantic interpretation, the LLM                      results. A key contribution of our approach is replacing
can produce the correct translation, which loads a 64-bit                     standard heuristic-based refinement with a feedback loop
integer from the memory indicated by .LCd0.                                   grounded in formal verification. Specifically, we perform
                                                                              a rigorous semantic verification using the angr symbolic
  x86-64 movq .LCd0(%rip), %rcx               mov x1, .LCd0         AArch64   execution engine [102] and the Z3 solver [32] (details in
                                              Wrong translation               Sec. 4.4). If any errors or semantic inconsistencies are found,
                Interpret the code first
                                                                              the precise feedback (i.e., formatted output from the symbolic
           “It loads a 64-bit value
           from a memory address              ldr x1, .LCd0
                                                                              execution engine) is passed back to the LLM. The LLM is then
           (indicated by label                                                prompted to refine the translation based on this feedback,
           .LCd0) to rcx.”
                                              Correct translation
                                                                              effectively combining the reasoning ability of LLMs with the
                                                                              rigor of formal proofs. The newly refined translation is then
 Figure 3. An example of semantic-grounded reasoning.
                                                                              verified with symbolic execution again. This iterative cycle
                                                                              continues until the translation passes semantic verification
RAG-Enhanced Translation. Second, LLMs may generate
                                                                              or a predefined iteration limit (set to 5) is reached.
syntactically invalid code despite correct semantics under-
                                                                                 As a result, we establish an iterative pipeline for our trans-
standing, often due to insufficient context. We repurpose
                                                                              lation engine, as shown in Fig. 5. While the interpret, trans-
retrieval-augmented generation (RAG) [25, 45] to solve the
                                                                              late, and fix steps are LLM-powered, we use the GCC com-
brittleness issue of assembly code synthesis. We retrieve sim-
                                                                              piler and angr for compilation and verification. Our evalu-
ilar, correct translation examples from our database based
                                                                              ation confirms that this specialized integration of prompt
on text similarity and inject them as architectural context.
                                                                              engineering and formal verification forms a necessary inno-
These examples provide the LLM with precise, compilable
                                                                              vation to enable reliable, LLM-based binary translation.
syntax patterns, helping LLM to produce valid code. Fig. 4
shows an example where the initial translation (top right) is                 4.4   Semantic Verification
non-compilable because an immediate value (-544) exceeds
                                                                              The semantic verification process ensures that the translated
the allowable range. By providing a textually similar, valid
                                                                              code is semantically equivalent to the original. Two snip-
example, the LLM learns the correct pattern and generates a
                                                                              pets are considered semantically equivalent if they always
valid translation (bottom right).
                                                                              produce identical outputs for the same inputs.
  x86-64                                                            AArch64   Variables. This equivalence requires a one-to-one mapping
  movzbl -544(%rbp,%rax), %eax               add       x2, x29, x0            between input and output variables, where corresponding
                                             ldrb      w0, [x2, #-544]        variables hold the same value after execution. Variables in
         Search for similar (correct)
                                                Wrong translation             assembly code include registers and memory, while mem-
         translation pair
                                           (immediate offset out of range)    ory is treated as a special variable that encompasses both
  movq -600(%rbp,%rax), %rbx
                                             add       x2, x29, x0            its value and the address being accessed. Furthermore, in-
  add       x2, x29, x0                      add       x2, x2, #-544
  add       x2, x2, #-600                    ldrb      w0, [x2]               struction execution often updates the flags register, which
  ldrb      x1, [x2]                             Correct translation          subsequent instructions (especially branches) may utilize.
                                                                              Since angr treats flags as specialized registers, we can ver-
   Figure 4. An example of RAG-enhanced translation.                          ify them using the same methodology for general-purpose
                                                                              registers. While x86-64 defines six status flags, two of them
Iterative Refinement. Finally, to fix any remaining errors,                   (AF and PF) are primarily retained for backward compatibil-
we introduce an iterative process to refine and correct the                   ity [47, 94]. Our analysis confirmed that these two flags are
EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk                                                                            Zhibo Liu et al.


unused in our evaluation set. The remaining four flags have                   x86-64                                                  AArch64
                                                                              cltq                               sxtw x0, w0
direct counterparts in AArch64 and can be mapped reliably.                    movzbl -28(%rbp,%rax), %edx        ldrb w2, [x29, x0, #-0x1c]
                                                                              jmp foo                            b    foo
Symbolic Execution. To verify semantic equivalence, we
first perform symbolic execution on both the x86-64 and                        Mapping: {rbp: x29, rax: x0, rdx: x2}, Labels: {foo: foo}
translated snippets. We assign initial symbols to all input                    Immediate Values: {-28: #-0x1c}

variables and conduct symbolic execution to derive sym-                      Parameterized Translation Rule:
bolic expressions for each output. Crucially, the snippets                    cltq
                                                                              movzbl <IMM_0>(<REG_0_64bit>,<REG_1_64bit>), <REG_2_32bit>
are ensured to have only one valid execution path without                     jmp <LAB_0>
branches. This design choice deliberately bypasses the path                   sxtw <REG_1_64bit>, <REG_1_32bit>
                                                                              ldrb <REG_2_32bit>, [<REG_0_64bit>, <REG_1_64bit>, <IMM_0>]
explosion problem that complicates symbolic execution in                      b <LAB_0>

general scenarios. Fig. 6 demonstrates an example of sym-
bolic execution results, where initial symbols are marked                   Figure 7. An example of a parameterized translation rule.
with an _init suffix. The verification requires finding a valid
mapping between registers that satisfies the aforementioned
equivalence property. Using brute-force search, we explore
possible register mappings and employ the Z3 constraint
                                                                           be introduced in the AArch64 snippet, as x86-64 instructions
solver [32] to check if a given mapping satisfies the equiv-
                                                                           are often decomposed into multiple simpler RISC operations.
alence property. The small number of variables makes this
search computationally efficient. If a valid mapping is found,
the two snippets are deemed semantically equivalent.                       4.5    Translation Rule Parameterization
                                                                                  Querying an LLM is time-consuming and inefficient, espe-
     x86-64                                              AArch64                  cially for repeated similar code. To address this, we parame-
                                              add x8, x29, x0                     terize verified translation results into reusable rules.
      subq 60(%rbp,%rax), %rdx                ldr x9, [x8, #60]
                                              subs x2, x2, x9                     Parameterization. Specifically, we observed that snippets
                                                                                  with similar structure, albeit with different operands, often
       Updated registers:{                    Updated registers: {                yield translation results with the same sequence of AArch64
       rdx: rdx_init – [mem] }                x8: x29_init + x0_init,
                                              x2: x2_init - [mem] }
                                                                                  instructions. Therefore, we abstract concrete operands (e.g.,
       Mem: {
       addr:                                  Mem: {                              registers and immediate values) into parameters, extracting
       rbp_init + rax_init + 60,              addr: x29_init +                    generalized snippet skeletons. This allows the reuse of a
       expr: mem_init, }                      x0_init + #60,
                                              expr: mem_init }                    verified translation rule for multiple similar x86-64 snippets
                                                                                  without repeated LLM queries. Furthermore, the parame-
                                                                               movq -600(%rbp,%rax), %rbx
       Mapping: {rdx: x2, rbp: x29, rax: x0} Temporaries: {x8}                    terized translation rules are context-independent and can
       Constraints: {                                                              Correct translation
       rdx_init == x2_init  True, rax_init == x0_init  True,
                                                                                  guarantee consistent functionality when reassembled.
       rbp_init == x29_init  True, ...                                              Fig. 7 illustrates an example of a parameterized transla-
       rdx_init – [mem] != x2_init - [mem]  False}
                                                                                  tion rule. The translation at the top is semantically correct
                                                                                  and verified. We replace its concrete operands with unique
    Figure 6. An example of symbolic execution results.
                                                                                  parameter identifiers (composed of its type and ID) based
                                                                                  on the mapping derived from verification. These parameter-
Equivalence Checking. Assuming the x86-64 snippet con-                            ized rules, along with original snippets, symbolic verification
tains variables 𝑉𝐴 = {𝑣 𝐴1 , 𝑣 𝐴2 , 𝑣 𝐴3 , . . . , 𝑣 𝐴𝑛𝐴 }, and the AArch64       results, and mappings, are stored in the rule database.
snippet uses variables 𝑉𝐵 = {𝑣 𝐵1 , 𝑣 𝐵2 , 𝑣 𝐵3 , . . . , 𝑣 𝐵𝑛𝐵 }, let 𝐸 (𝑣𝑖 )    Database Querying. Before translating a new x86-64 snip-
denote the symbolic expression of variable 𝑣𝑖 , with 𝐸𝑖𝑛𝑖𝑡 (𝑣𝑖 )                  pet, we first parameterize it and query the database for
as its initial symbolic expression. Given a mapping 𝑀 : 𝑉𝐴 →                      matched rules. A match requires that the snippet’s instruc-
𝑉𝐵 , for each variable 𝑣𝑖 ∈ 𝑉𝐴 , we first establish the initial                   tion, parameter types, and sequence are identical to a rule
conditions by adding the constraint 𝐸𝑖𝑛𝑖𝑡 (𝑣𝑖 ) = 𝐸𝑖𝑛𝑖𝑡 (𝑀 (𝑣𝑖 ))                 in the database. Upon finding a match, the rule is applied
to the solver. This ensures that corresponding variables start                    by replacing parameters with concrete operands. Otherwise,
with the same initial symbolic expression. After that, for                        the snippet is sent to the LLM. For consistency, we conduct
each variable 𝑣𝑖 ∈ 𝑉𝐴 , we check if 𝐸 (𝑣𝑖 ) ≠ 𝐸 (𝑀 (𝑣𝑖 )) is un-                  the same parameterization process on translation results
satisfiable with the solver. If it is, we add 𝐸 (𝑣𝑖 ) = 𝐸 (𝑀 (𝑣𝑖 ))               produced by LLMs. In practice, as the database grows, these
to the solver and proceed to the next variable. This ensures                      rules increasingly supplant the role of LLMs, shifting trans-
that symbolic expressions of corresponding variables must                         lation into an efficient data-driven process. Consequently,
be equal after execution. Once all variables are validated, the                   ③ and ④ in Fig. 2 become less frequent, with most snippet
mapping is considered to satisfy the equivalence property.                        translations being handled by reusing rules in the database
This process naturally handles temporary registers that may                       (⑥), reducing the time and cost of LLM queries.
                                                                                   EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk


Concretization. Once all snippets are translated, the result-                                                                AArch64
                                                                         x86-64                    AArch64
                                                                                                                mov x28, sp
ing rules, whether from the database or generated by param-              push %rax      str x0, [sp, #-8]!      str x0, [x28, #-8]!
eterizing LLM outputs, need to be concretized before they                ...            ...                     ...
                                                                         pop %rax       ldr x0, [sp], #8        str x0, [x28], #8
can be stitched into complete assembly code. This process                                                       mov sp, x28
reinserts specific operands back into the translated snippets.
While immediate values and labels can be directly extracted                    Figure 8. Stack Alignment Management.
from x86-64 snippets, register concretization demands a con-
sistent mapping across snippets (i.e., a specific x86-64 register     x86-64                                                   AArch64
must always map to the same AArch64 register). For simplic-            movq Replacing
                                                                             $42, %rdisp#with
                                                                                          1st aarg
                                                                                                free register
                                                                                                         mov (x28) for stack
                                                                                                              x0, #42   // 1alignment.
                                                                                                                             st arg
                                                                       callq enternal_fun                bl enternal_fun
ity, we employ a fixed mapping to define the correspondence            # store return value rax          // rax is mapped to x8
between x86-64 and AArch64 registers, as detailed in Table 2.          movq %rax, 0x10(%rsp)             str x8, [sp, #0x10]
This is feasible without causing register conflicts because
AArch64 offers more general-purpose registers than x86-64.                        mov x0, #42 // 1st arg                       AArch64
                                                                                  ... // store x0 in mem temporarily
The remaining AArch64 registers are utilized for temporary                        bl enternal_fun
                                                                                  mov x8, x0
values introduced during translation.                                             ... // retrieve x0 from mem
                                                                                  str x8, [sp, #0x10]
Table 2. The mapping used to concretize translation rules.               (a) External function call hook: Moving return value to x8.
                                                                       x86-64                                   AArch64
           x86-64    AArch64        description
                                                                       callq internal_fun         adr x30, .               Compute
           rdi          x0                                             # callq pushes             add x30, x30, #16        and push
                                                                       return address             str x30, [sp, #-8]
           rsi          x1                                             nop                        bl internal_fun          ret address
           rdx          x2                                                                        nop
                                Function arguments
           rcx          x3                                             (b) Internal function call hook: Pushing return address explicitly.
           r8           x4
           r9           x5                                                   Figure 9. Examples of extra code inserted.
           rax          x8          Return value
           rbx          x9          Callee saved
           r10-r15    x20-x25    temporary registers                layout to be preserved while ensuring that sp remains 16-
           rbp          x29        Frame pointer
                                                                    byte aligned. The stack pointer is restored upon exiting the
           rsp           sp         Stack pointer
                                                                    function, maintaining proper stack discipline.
                                                                    Correctness. The correctness of the stitched program hinges
4.6   Snippets Stitching                                            on the principle of compositional verification [24]. Each x86-
The final step is to stitch concretized snippets into an exe-       64 snippet is translated into a semantically equivalent AArch64
cutable assembly program. This offline process introduces no        snippet. The use of SSA form makes data flow explicit through
runtime overhead and primarily involves reconstructing the          def-use chains, allowing each snippet to be treated as a ver-
program’s control flow and managing Application Binary              ified, context-independent function. Since each translated
Interface (ABI) differences with function calls.                    snippet produces identical output as the original snippet, the
Control Flow Reconstruction. We arrange the translated snip-        correctness of stitched programs can be reasoned. However,
pets in the original sequence as their x86-64 counterparts.         the correctness guarantee relies on two main assumptions:
We iterate through each basic block and emit AArch64 assem-         1) No Implicit Cross-Snippet Dependencies. We assume that
bly code for each snippet. Jumps and branches are resolved          there are no hidden side effects or dependencies between
by mapping all target addresses to appropriate labels. For          snippets that are not captured by the explicit control and data
instance, an jne .𝑙𝑎𝑏𝑒𝑙 is translated into a corresponding          flow. This holds for standard application code but excludes
b.ne .𝑙𝑎𝑏𝑒𝑙 in AArch64, where .𝑙𝑎𝑏𝑒𝑙 points to the equiva-          highly specialized cases like self-modifying code.
lent location in the new code.                                      2) Mediated ABI Compatibility. We assume that external li-
Stack Alignment Management. Moreover, AArch64 enforces              braries are effectively managed, and ABI incompatibilities
stricter stack alignment requirements than x86-64. A com-           are resolved with additional expertise. That requires all nec-
mon issue arises when the prologue code of an x86-64 func-          essary libraries to be available on the AArch64 host, and
tion pushes an 8-byte value, which can misalign the 16-byte         our hooking mechanisms (introduced below) are applied to
boundary required by AArch64. To resolve this, we employ            function calls to mediate the incompatibilities.
a standard AArch64 assembly programming technique [18].             Function Call Hooks. While stitching, we hook calls to
Upon entering a function, we substitute the stack pointer           resolve ABI differences between the x86-64 and AArch64,
(sp) with a free register (e.g., x28). As shown in Fig. 8, using    which arise from their distinct architectural designs. While
x28 in the store (str) instruction allows the original stack        mitigating such issues requires domain expertise and extra
EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk                                                               Zhibo Liu et al.


code, this is a standard practice for cross-architecture binary     identified by differentially debugging translated and origi-
translation and commonly seen in related binary analysis            nal binaries. Solutions can then be derived from established
works [38, 63, 79, 114]. Specifically, our hooks address incon-     assembly programming practices and ABI documentation.
sistencies in calling conventions for external calls and return
address handling for internal calls.                                5     Implementation
Calling Convention. Since translated code follows the x86-          The core components of our research prototype, LLMSbt,
64 calling convention, it requires no special handling for          consist of roughly 6K LoC in Python (excluding comments
arguments within translated functions. However, differences         and blank lines), leveraging the angr symbolic execution en-
in the ABI must be addressed at the boundaries between              gine [102] and GPT-4 [82] as the underlying LLM. For disas-
translated and native code (e.g., external library calls). First,   sembling and symbolizing binary code, we chose RetroWrite,
the return value and first argument in x86-64 are in sepa-          an open-source binary rewriter that has been extensively
rate registers (rax and rdi), whereas in AArch64, both are          evaluated in prior studies [38, 64]. All binaries were compiled
handled by the x0 register. Our implementation maps rax             with GCC 11.4.0 on an x86-64 machine running Ubuntu 22.04,
and rdi to different registers (x8 and x0, respectively). As        equipped with an Intel Core i7-9700K CPU and 32 GB RAM.
demonstrated in Fig. 9(a), this is addressed by preserving          The translated binaries were executed on a development
and retrieving the first argument before and after a function       board featuring an ARMv8.2-based rk3588 processor [1]. For
call, and then transferring the return value from x0 to x8          comparison with ExaGear, which is compatible only with
after the call. Second, x86-64 passes the first six arguments       Huawei-manufactured CPUs, we ran translated binaries on
via registers (rdi-r9), with subsequent arguments on the            a Huawei Cloud virtual machine powered by a Kunpeng 920
stack. AArch64, however, uses registers x0-x7 for the first         processor (ARMv8.2) [54].
eight arguments. Our fixed register mapping already aligns          Target Software. Our current implementation targets user-
x86-64’s rdi-r9 with AArch64’s x0-x5. To ensure correct ar-         level single-threaded C programs compiled without anti-
gument passing for functions with more than six arguments,          analysis techniques like obfuscation or self-modification. The
we move the seventh and eighth arguments from the stack             evaluation mainly covers a subset of x86-64 ISA, including
into registers x6 and x7 before the call.                           core general-purpose instructions and frequently used SSE
Return Address. Additionally, x86-64 and AArch64 also man-          instructions. Support for floating-point operations is limited,
age return addresses differently. In x86-64, the call instruc-      as we currently exclude x87 FPU instructions. Limitations
tion automatically pushes the return address onto the stack,        and future works are further discussed in Sec. 7.
while in AArch64, the bl instruction stores the return ad-
dress in the link register (x30). Thus, an internal function
                                                                    6     Evaluation
call from translated code will leave the return address in x30,
which can be overwritten by subsequent calls. Our solution,         This section evaluates the performance of LLMSbt by an-
shown in Fig. 9(b), hooks the call to explicitly push the re-       swering the following research questions:
turn address to preserve it and pop it back into x30 before         • RQ1: How many translation rules were collected, and
returning, ensuring the integrity of the call stack.                  what were the development costs of LLMSbt?
                                                                    • RQ2: How does the runtime performance of binaries trans-
Threats to Validity. The issues resolved in the stitching             lated by LLMSbt compare to existing open-source transla-
process are unique for assembly-level translators, as lifters         tors and the industrial dynamic binary translator ExaGear?
typically compile lifted IR into binary without diving deep         • RQ3: What factors affect the execution efficiency of trans-
into architectural differences. While domain expertise is re-         lated binaries?
quired, the core problems and solutions are common and
well-documented [10, 11]. Nevertheless, the validity of stitch-     6.1   Characteristics of Translation Rules
ing faces potential threats:                                        To answer RQ1, this section details the characteristics of
Complex Data Types. While we address common ABI dis-                the 3, 149 rules collected by LLMSbt. These rules encompass
crepancies, issues may arise with specialized data types (e.g.,     3, 756 x86-64 instructions and 7, 784 AArch64 instructions in
floating-point values and vectors) or aggregate types, whose        total. On average, each rule maps 1.2 x86-64 instructions to
passing can differ largely between architectures.                   2.5 AArch64 instructions, reflecting our observation that con-
Non-Standard ABIs. Customized libraries may employ non-             verting CISC instructions to RISC instructions often requires
standard or highly specialized calling conventions not cov-         multiple instructions. Meanwhile, as shown in Table 3, about
ered by our method, leading to incorrect argument passing           95% rules have three or fewer x86-64 instructions, while the
or return address handling. In such cases, the libraries should     number of AArch64 instructions mostly ranges from one to
be translated as well.                                              five. Generally, shorter snippets are more likely to match sim-
   While solving these potential issues may require addi-           ilar snippets and easier for LLMs to translate. While longer
tional expertise and effort, the root causes can generally be       snippets likely expose richer optimization opportunities, no
                                                                                    EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk


significant correlation was observed between snippet length                   Table 4. Statistics of evaluated software.
and LLM failures. However, it is worth noting that the LLM
did not achieve perfect coverage. Consequently, we manu-                            Source
                                                                                             #Func
                                                                                                                    Source
                                                                                                                              #Func
                                                                                     LoC                             LoC
ally provided an additional 68 rules for cases where the LLM             adpcm        887      15      loops          9.5K     328
failed, the details of which are discussed in Sec. 7.                    gsm          634      12      parser         18K      310
                                                                         mips         388       1      radix2          7K      289
Table 3. The number of translation rules of different lengths.           motion      1.1K      14      zlib          21.5K     396
                                                                         aes         1.1K      11      bzip2          8.1K     70
                                                                         sha1        1.4K       8      xz            35.6K     390
      #Inst       1      2     3   4     5   6    ≥ 7 Sum                blowfish    1.8K       6      mcf             4K      43
      x86-64    2,177   524   297 144    4   2     1 3,149               jpeg        3.3K      29      libquantum     4.3K     98
      AArch64    689    677   678 585   279 112   129 3,149              cjpeg       19.5K     416     hmmer         38.3K     494
                                                                         sha256      7.2K      283     Zydisn         18K      161
                                                                         linpack     7.5K      290     yyjson         12K      92
   The rule collection process was highly cost-effective. The            nnet        8.2K      288     Sum          219.4K    4,044
entire process, including iterative corrections, consumed ap-
proximately 2, 036𝐾 tokens, totaling less than $130. With
an average requirement of under 30 seconds and roughly             they failed to process any test case, a limitation consistent
$0.04 per rule, these results highlight the economic viability     with findings in prior research [34, 74, 83]. The results re-
of our approach. In terms of instruction set coverage, the         veal that LLMSbt consistently and significantly outperforms
collected rules cover 148 unique x86-64 instructions and 102       other translators. Notably, McSema failed on 11 of 23 cases,
AArch64 instructions. While modern CPUs support a vast             while both Instrew and QEMU failed on the xz case. These
number of instructions, many are highly specialized for spe-       findings underscore substantial performance and robustness
cific hardware features (e.g., AVX512 and SGX) or are rarely       advantages of our approach over traditional methods.
used. Translating these hardware-dependent instructions               Moreover, QEMU and Instrew occasionally exhibited sub-
presents unique challenges that are outside the scope of this      stantial overhead (over 20×). Our investigation revealed that
research. This work primarily pioneers a new paradigm for          these programs’ test suites consist of low-workload cases,
binary translation by focusing on 259 core general-purpose         causing frequent program restarts. Since translated code is
instructions and frequently used SSE instructions [2, 31, 76].     not retained between runs, each restart forces a repeated
For comparison, QEMU contains 283 code generation func-            translation, contributing to the high overhead. Moreover, In-
tions for x86-64 [87], each of which translates one x86-64         strew’s reliance on LLVM for runtime optimization and code
instruction into IR. The ability of LLMSbt to collect a signif-    generation further adds to this overhead. Nevertheless, it is
icant set of rules at a very low cost, covering a substantial      important to note that Instrew’s novel design is a significant
portion of the core instruction set, shows high potential and      contribution, offering an efficient and reliable system that
research value of this approach. Interestingly, during our         substantially outperforms QEMU in high-workload scenar-
evaluation, we found a program where QEMU failed (see              ios. In contrast, static approaches like McSema and LLMSbt
Table 5). QEMU throws an “Illegal Instruction” error when          turn translation into a one-time offline effort, producing
translating the shlx %rsi, %rdx, %rdx instruction. This            portable binaries that execute natively. However, McSema’s
suggests that even widely-used translators like QEMU may           low success rate highlights the inherent difficulties of static
still contain flaws, underscoring the motivation of our work.      IR lifting. We attribute LLMSbt’s performance and robust-
                                                                   ness advantages to its static assembly-to-assembly transla-
6.2   Performance Overhead                                         tion paradigm, which bypasses the daunting binary analysis
Test Cases. We use a comprehensive suite of benchmarks,            challenges while minimizing runtime overhead.
including CHStone [49], Coremark-Pro [39, 44], and SPEC               Table 6 further compares LLMSbt’s performance against
CPU benchmark [19, 52]. We also include two widely used            ExaGear. While both tools exhibit strengths, LLMSbt demon-
real-world projects: Zydis [122], a fast x86/x64 disassembler      strates consistently stable and superior performance overall.
library, and yyjson [59], a high-performance JSON library.         Similarly, ExaGear’s performance suffers from significant
Our evaluation encompassed a total of 23 diverse programs,         overhead in low-workload scenarios. Given that ExaGear is
detailed in Table 4 and Table 9. This test suite ensures a thor-   a mature, heavily optimized commercial product developed
ough assessment of LLMSbt’s effectiveness across a range           by a leading chip manufacturer, these results highlight the
of complex instructions. We empirically consider a transla-        remarkable potential and research value of our approach.
tion correct when the translated binary exhibits consistent
input-output behavior on the test cases.                           6.3    Performance Analysis
   Table 5 compares the performance overhead of LLMSbt             To better understand why LLMSbt’s performance varies
with QEMU, Instrew, and McSema on the rk3588 platform.             across different cases, we conducted detailed profiling on
Static lifters like Mctoll and RetDec were excluded because        three typical algorithms from a popular C library [56]: avl-tree,
EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk                                                                                Zhibo Liu et al.


Table 5. Performance overhead comparison on rk3588 versus               in cycles is not always proportional to the increase in instruc-
native AArch64 execution. Cases with no lifted code, compi-             tions. For instance, while the translated avl-tree executes
lation failures, or inconsistent results are marked “failed”.           50% more instructions, it consumes only 27% more CPU cy-
                                                                        cles. This discrepancy suggests that performance is heavily
       Testcase      QEMU     Instrew     McSema LLMSbt                 influenced by microarchitectural features, such as pipelining,
       adpcm         33.57×    >100×       1.94×  1.22×
                                                                        branch prediction, and caching. The instruction sequence
       gsm           33.94×    >100×       1.58×  1.23×
       mips          34.08×    >100×       1.90×  1.26×                 and memory access patterns in translated binaries differ
       motion        33.67×    >100×       1.87×  1.24×                 considerably from those in compiler-generated native code,
       aes           33.74×    >100×       1.84×  1.22×                 which can substantially affect execution speed. Our evalu-
       sha1          29.84×    >100×       2.29×  1.24×                 ation indicates that the CPU pipeline effectively mitigates
       blowfish      29.16×    >100×       2.16×  1.26×
       jpeg          23.03×    >100×       3.62×  1.24×
                                                                        much of the overhead from increased instruction count.
       cjpeg          3.52×    >100×       failed 1.36×
       sha256        32.69×    >100×       1.72×  1.19×
                                                                        Table 8. Detailed performance profiling with perf. The data
       linpack        8.94×    90.1×       failed 1.26×
       nnet          15.24×    33.3×       4.67×  1.86×                 is collected on the rk3588 device.
       loops          6.51×    76.4×       failed 1.27×
       parser         2.97×    83.7×       1.88×  1.03×                                   Branch         Cache       Stalled Cycles   Stalled Cycles
       radix2        25.58×    >100×       46.04× 1.27×                  Algorithm        Misses         Misses         Frontend         Backend
                                                                                           (N / T)        (N / T)         (N / T)          (N / T)
       zlib          17.61×    >100×       failed 1.15×
                                                                         avl-tree       2.3M / 2.1M    12M / 12.2M   123.4M / 10.6M   31.8M / 131.6M
       bzip2         12.82×    1.32×       failed 1.14×                  binary-heap   135K / 126.6K    32K / 34K      332K / 334K     28.5M / 25M
       xz            failed    failed      failed 1.25×                  hash-table     61.2K / 56K    299K / 316K     1.8M / 1.9M     42M / 41.7M
       mcf            3.89×    1.49×       failed 1.13×
       libquantum     5.55×    4.62×       failed 1.12×
       hmmer          5.69×    3.03×       failed 1.39×
       Zydis         21.34×    >100×       failed 1.16×                    For a deeper insight, we used perf to record microarchi-
       yyjson        25.36×    >100×       failed 1.44×                 tecture level metrics, with the results shown in Table 8. The
                                                                        data reveals a key finding: native binaries generally exhibit
Table 6. Performance overhead of ExaGear and LLMSbt on                  more branch misses, whereas translated binaries suffer from
Kunpeng 920 versus native AArch64 execution.                            more cache misses. This is likely because the repetitive, pat-
                                                                        terned code resulting from translation rules is more friendly
 Testcases   ExaGear LLMSbt       Testcases      ExaGear LLMSbt         to branch predictors. However, the translation process does
 adpcm        45.36×  1.12×       loops           4.33×   1.94×         not account for memory layout, leading to lower cache effi-
 gsm          47.90×  1.16×       parser          2.50×   1.09×
 mips         47.03×  1.17×       radix2          36.67×  1.19×
                                                                        ciency. The avl-tree is a clear example, with a significant
 motion       47.98×  1.22×       zlib            24.54×  1.10×         increase in cache misses (over 200K more), which results in
 aes          48.45×  1.21×       bzip2           1.09×   1.25×         a high number of backend stalled cycles (notably, one cache
 sha1         44.11×  1.24×       xz              1.10×   1.23×
                                                                        miss can cause a long stall). This indicates that avl-tree’s
 blowfish     41.11×  1.27×       mcf             1.21×   1.13×
 jpeg         30.63×  1.18×       libquantum      1.53×   1.69×         overhead stems primarily from poor cache efficiency.
 cjpeg        4.80×   1.37×       hmmer           1.20×   1.24×            Overall, executing more instructions does not necessarily
 sha256       46.88×  1.20×       Zydisn          37.90×  1.08×         lead to high overhead. Performance depends heavily on how
 linpack      2.30×   1.19×       yyjson          28.43×  1.59×
 nnet         2.13×   2.44×                                             well the translated code utilizes CPU microarchitecture. De-
                                                                        signing a binary translator that effectively accounts for the
                                                                        microarchitecture remains an open challenge, and investigat-
binary-heap, and hash-table. Using the perf profiling                   ing the intricate relationship between binary code and CPU
tool on the rk3588 platform, Table 7 presents the number of             pipeline behavior is an intriguing topic for future research.
executed instructions and CPU cycles.
                                                                        7   Discussion
Table 7. Evaluation results of three algorithms. N and T rep-
resent the native binary and translated binary, respectively.           Remaining Challenges. While this work establishes the
                                                                        viability of a novel, LLM-based static translation pipeline,
               Source    #Executed       #CPU Cycles                    several orthogonal challenges remain. These long-standing
 Algorithm                                                Performance
                LoC     Insts (N / T)        (N / T)                    issues represent important directions for future work, each
 avl-tree       1.2K  2,327M / 3,526M   1,016M / 1,292M      1.20×
 binary-heap    0.5K   143.7M / 208M    120.4M / 120.8M      1.02×      requiring substantial, dedicated research and engineering
 hash-table     1.1K  353.3M / 477.4M     210M / 225M        1.12×      efforts beyond the scope of a single paper.
                                                                        1) Concurrent Programs. Translating concurrent programs
   As shown in Table 7, translated binaries (marked T) con-             is challenging due to the different memory models between
sistently execute more instructions and consume more CPU                architectures. Nevertheless, prior research offers a solid foun-
cycles than native binaries (marked N). However, the increase           dation by inserting and optimizing fences in lifted IR code [16,
                                                                                EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk


34, 46, 91]. Although these methods do not focus on assembly-     8   Related Work
level translation, future research could adapt them to our        Translation Validation. Ensuring the correctness of code
static assembly-to-assembly translation paradigm.                 transformations is a critical challenge. Recent efforts [30]
2) C++ Programs. C++ features like exceptions and virtual         have focused on validating the process of lifting binaries to
functions, which rely on compiler-specific implementations,       LLVM IR by employing scalable instruction-level checking
present unique hurdles for binary rewriting. These features       and formal verification to guarantee semantic equivalence.
complicate CFGs and data flow, making disassembly more            Within the compiler toolchain, tools like Alive2 [75] pro-
difficult. Since our method relies on correct disassembly code,   vide bounded translation validation to find bugs in LLVM’s
future research could focus on improving existing binary          optimization passes. Other techniques, such as semantic pro-
rewriting and disassembly techniques to cover these complex       gram alignment [23], verify equivalence by matching pro-
language features.                                                gram states along their execution traces based on semantic
3) Floating-Point Operations. Architectural differences com-      information, a method particularly effective for complex
plicate the translation of floating-point operations. The x86-    transformations that significantly restructure code. Comple-
64 uses an eight-register stack for its x87 Floating Point Unit   menting these, language-parametric approaches [62] offer
(FPU) [66], where AArch64’s Advanced SIMD (NEON) [9, 68]          more generalized validation frameworks that are not tied to a
lacks a floating-point stack. Translating these hardware-         specific transformation, further strengthening the reliability
dependent instructions demands significant manual effort          of modern compilers. Nevertheless, these works primarily
and expertise that is beyond this paper’s scope. Current so-      target high-level IR transformations, whereas our work is
lutions often rely on carefully crafted helper functions. Due     centered on assembly-level cross-architecture translation.
to this complexity, we exclude these instructions from our        Extensions in Binary Translation. Recent advancements
implementation, leaving a more efficient automated method         in binary translation have focused on addressing the com-
as future work.                                                   plexities of modern software, particularly in areas like con-
4) System Calls. Our evaluation targets user-level appli-         currency and post-compilation optimization. The challenge
cations where dynamically linked native libraries handle          of translating for weak memory model architectures has been
system calls, simplifying translation since library APIs are      tackled by both static approaches, like Lasagne [91], and dy-
consistent across architectures. However, translating system      namic systems such as Risotto [46]. For multithreaded appli-
calls is inherently complex due to differences in conventions     cations, hybrid recompilation techniques like Polynima [34]
and data structure layouts. Our preliminary findings reveal       have emerged to balance performance and translation over-
inconsistencies in binary-level data structures between Linux     head. Researchers have also developed solutions for specific
kernels of different architectures (more details in the Ap-       technical hurdles that impact correctness and efficiency. For
pendix A.2). Initial experiments suggest these issues can be      instance, WYTIWYG [83] presents a method for dynamic
resolved by patching native libraries to enforce data struc-      stack-layout recovery, which enables post-compilation op-
ture consistency, with minimal performance impact. Future         timization for binaries, while Tiaozhuan [70] introduces
research could explore automated methods to identify and          a general optimization for indirect branches, a common
resolve such issues.                                              performance bottleneck. Another promising direction in-
Supplementing with Manually-Crafted Rules. Although               volves leveraging information beyond the raw binary. Plank-
LLMs show significant potential in binary translation, they       ton [119], for example, supports full-fledged static analysis
can struggle with complex instructions due to reasoning lim-      on lifted IR by utilizing debug information, while Biotite [22]
itations. While our symbolic verification method automati-        uses source-level knowledge to generate higher-performance
cally detects such failures, fixing them may require human        code. In the broader context of binary lifting, adjacent re-
intervention. In our experiments, we manually created 68          search explores decompilation to recover high-level source
translation rules for cases in which LLM failed.                  code (e.g., C) from binaries. Although decompilation is in-
   The practicality of this manual approach is supported by       herently challenging and often error-prone [73], recent ad-
our methodology, which intentionally keeps translation code       vancements utilizing LLMs have substantially improved de-
snippets short and their data flow simple. This design allows     compilation fidelity for small-scale programs [99, 111, 120].
an experienced developer, referencing the relevant ARM            They are, however, orthogonal to our work, which focuses
documentation, to author an equivalent AArch64 code for a         on binary-level translation that produces efficient code and
given snippet in minutes without extensive coding. While          supports scalable verification.
this requires expertise, our automatic semantic verification      Automated Generation of Translation Logic. A signifi-
drastically reduces the manual validation effort, accelerating    cant line of research has focused on automating the creation
the entire workflow. Once verified, the translated code is        of translation logic to reduce manual effort and improve the
parameterized into a reusable rule.                               quality of generated code. Early work in this area utilized
EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk                                                                                    Zhibo Liu et al.


peephole superoptimizers [14] to automatically discover op-                          Systems, pages 1–16, 2020.
timal, short instruction sequences for translation. Other re-                    [4] Dennis Andriesse, Xi Chen, Victor Van Der Veen, Asia Slowinska,
search has improved the front-end of the translation process,                        and Herbert Bos. An {In-Depth} analysis of disassembly on {Full-
                                                                                     Scale} x86/x64 binaries. In 25th USENIX security symposium (USENIX
presenting novel compiler-leveraged techniques for lifting                           security 16), pages 583–600, 2016.
assembly to a high-level intermediate representation [50].                       [5] Apple. Apple introduces m4 chip. https://www.apple.com/ci/
More recently, this has evolved into a broader learning-based                        newsroom/2024/05/apple-introduces-m4-chip/, 2024.
paradigm. For instance, several studies have shown how                           [6] Apple. Apple silicon. https://developer.apple.com/documentation/
translation rules for dynamic binary translators can be au-                          apple-silicon, 2024.
                                                                                 [7] Apple.      Porting your macos apps to apple silicon.           https:
tomatically learned from compiler-generated binary code,                             //developer.apple.com/documentation/apple-silicon/porting-
an approach demonstrated by Wang et al. [105] and Song et                            your-macos-apps-to-apple-silicon, 2024.
al. [97]. This learning-based methodology has been success-                      [8] Apple. Rosetta translation environment. https://developer.apple.com/
fully extended to the more demanding context of system-                              documentation/apple-silicon/about-the-rosetta-translation-
level translation [61] and has been made more data-efficient                         environment, 2024.
                                                                                 [9] ARM. What is neon? https://developer.arm.com/documentation/
through techniques like parameterization [60], which allows                          dht0002/a/Introducing-NEON/What-is-NEON-, 2024.
deriving more general rules from less training data. In con-                    [10] ARM. Application binary interface for the arm® architecture –
trast, our method leverages LLMs to directly generate high-                          the base standard. https://github.com/ARM-software/abi-aa/blob/
quality assembly code, eliminating the reliance on extensive                         2982a9f3b512a5bfdc9e3fea5d3b298f9165c36b/bsabi32/bsabi32.rst,
                                                                                     2025.
training data or a separate compilation process.
                                                                                [11] ARM.          Procedure call standard for the arm architec-
                                                                                     ture.                https://github.com/ARM-software/abi-aa/blob/
9      Conclusion                                                                    2982a9f3b512a5bfdc9e3fea5d3b298f9165c36b/aapcs32/
This paper presents a novel static binary translation para-                          aapcs32.rst#the-base-procedure-call-standard, 2025.
                                                                                [12] Avast. Retargetable machine-code decompiler based on llvm. https:
digm that converts x86-64 binaries to AArch64, producing
                                                                                     //github.com/avast/retdec, 2025.
portable binaries with near native performance. By utiliz-                      [13] Roberto Baldoni, Emilio Coppa, Daniele Cono D’elia, Camil Deme-
ing LLMs, our approach substantially reduces the manual                              trescu, and Irene Finocchi. A survey of symbolic execution techniques.
effort and expertise required to build translation engines.                          ACM Computing Surveys (CSUR), 51(3):1–39, 2018.
We ensure translation correctness through efficient semantic                    [14] Sorav Bansal and Alex Aiken. Binary translation using peephole
                                                                                     superoptimizers. In OSDI, volume 8, pages 177–192, 2008.
verification of small, simplified code snippets. Our research
                                                                                [15] Daniel Bartholomew. Qemu: a multihost, multitarget emulator. Linux
prototype, LLMSbt, has been shown to outperform both tra-                            Journal, 2006(145):3, 2006.
ditional open-source tools and a leading industrial translator.                 [16] Martin Beck, Koustubha Bhat, Lazar Stričević, Geng Chen, Diogo
This work signals a promising new avenue for research in                             Behrens, Ming Fu, Viktor Vafeiadis, Haibo Chen, and Hermann Här-
binary translation techniques.                                                       tig. Atomig: automatically migrating millions lines of code from tso
                                                                                     to wmm. In Proceedings of the 28th ACM International Conference
                                                                                     on Architectural Support for Programming Languages and Operating
Acknowledgments                                                                      Systems, Volume 2, pages 61–73, 2023.
This work was supported in part by the Hong Kong RGC Post-                      [17] Fabrice Bellard. Qemu, a fast and portable dynamic translator. In
doctoral Fellowship Scheme (PDFS2324-6S08), the HKUST                                USENIX annual technical conference, FREENIX Track, volume 41, pages
                                                                                     10–5555. California, USA, 2005.
Bridge-the-Gap Fund (BGF.001.2025), and the Fundamental                         [18] Jacob Bramley.        Using the stack in aarch64: Implementing
and Interdisciplinary Disciplines Breakthrough Plan of the                           push and pop.         https://community.arm.com/arm-community-
Ministry of Education of China (No. JYB2025XDXM118). We                              blogs/b/architectures-and-processors-blog/posts/using-the-stack-
also thank the HKUST Fok Ying Tung Research Institute and                            in-aarch64-implementing-push-and-pop, 2015.
the National Supercomputing Center in Guangzhou (Nansha                         [19] James Bucek, Klaus-Dieter Lange, and Jóakim v. Kistowski. Spec
                                                                                     cpu2017: Next-generation compute benchmark. In Companion of the
Sub-center) for providing computational resources, and the                           2018 ACM/SPEC International Conference on Performance Engineering,
Collaborative Innovation Center of Novel Software Technol-                           pages 41–42, 2018.
ogy and Industrialization (Jiangsu, China) for their support.                   [20] Cristian Cadar, Daniel Dunbar, Dawson R Engler, et al. Klee: unas-
                                                                                     sisted and automatic generation of high-coverage tests for complex
References                                                                           systems programs. In OSDI, volume 8, pages 209–224, 2008.
                                                                                [21] Yupeng Chang, Xu Wang, Jindong Wang, Yuan Wu, Linyi Yang, Kaijie
    [1] Useful resources for developing with the rk3588. https://github.com/         Zhu, Hao Chen, Xiaoyuan Yi, Cunxiang Wang, Yidong Wang, et al.
        choushunn/awesome-RK3588/tree/develop, 2024.                                 A survey on evaluation of large language models. ACM Transactions
    [2] Amogh Akshintala, Bhushan Jain, Chia-Che Tsai, Michael Ferdman,              on Intelligent Systems and Technology, 15(3):1–45, 2024.
        and Donald E Porter. X86-64 instruction usage among c/c++ appli-        [22] Changbin Chen, Shu Sugita, Yotaro Nada, Hidetsugu Irie, Shuichi
        cations. In Proceedings of the 12th ACM International Conference on          Sakai, and Ryota Shioya. Biotite: A high-performance static binary
        Systems and Storage, pages 68–79, 2019.                                      translator using source-level information. In Proceedings of the 34th
    [3] Anil Altinay, Joseph Nash, Taddeus Kroes, Prabhu Rajasekaran, Dixin          ACM SIGPLAN International Conference on Compiler Construction,
        Zhou, Adrian Dabrowski, David Gens, Yeoul Na, Stijn Volckaert, Cris-         pages 167–179, 2025.
        tiano Giuffrida, et al. Binrec: dynamic binary lifting and recompila-
        tion. In Proceedings of the Fifteenth European Conference on Computer
                                                                                               EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk


[23] Berkeley Churchill, Oded Padon, Rahul Sharma, and Alex Aiken.              [38] Sushant Dinesh, Nathan Burow, Dongyan Xu, and Mathias Payer.
     Semantic program alignment for equivalence checking. In Proceedings             Retrowrite: Statically instrumenting cots binaries for fuzzing and
     of the 40th ACM SIGPLAN Conference on Programming Language                      sanitization. In 2020 IEEE Symposium on Security and Privacy (SP),
     Design and Implementation, pages 1027–1040, 2019.                               pages 1497–1511. IEEE, 2020.
[24] Jamieson M Cobleigh, Dimitra Giannakopoulou, and Corina S Păsăre-          [39] EEMBC. Coremark-pro. https://www.eembc.org/coremark/, 2025.
     anu. Learning assumptions for compositional verification. In Inter-        [40] Alexis Engelke, Dominik Okwieka, and Martin Schulz. Efficient
     national Conference on Tools and Algorithms for the Construction and            llvm-based dynamic binary translation. In Proceedings of the 17th
     Analysis of Systems, pages 331–346. Springer, 2003.                             ACM SIGPLAN/SIGOPS International Conference on Virtual Execution
[25] Florin Cuconasu, Giovanni Trappolini, Federico Siciliano, Simone                Environments, pages 165–171, 2021.
     Filice, Cesare Campagnano, Yoelle Maarek, Nicola Tonellotto, and           [41] Alexis Engelke and Martin Schulz. Instrew: Leveraging llvm for
     Fabrizio Silvestri. The power of noise: Redefining retrieval for rag            high performance dynamic binary instrumentation. In Proceedings of
     systems. In Proceedings of the 47th International ACM SIGIR Conference          the 16th ACM SIGPLAN/SIGOPS International Conference on Virtual
     on Research and Development in Information Retrieval, pages 719–729,            Execution Environments, pages 172–184, 2020.
     2024.                                                                      [42] Antonio Flores-Montoya and Eric Schulte. Datalog disassembly. In
[26] Chris Cummins, Volker Seeker, Dejan Grubisic, Baptiste Roziere,                 29th USENIX Security Symposium (USENIX Security 20), pages 1075–
     Jonas Gehring, Gabriel Synnaeve, and Hugh Leather. Meta large lan-              1092, 2020.
     guage model compiler: Foundation models of compiler optimization.          [43] Andrei Frumusanu. Amazon’s arm-based graviton2 against amd and
     arXiv preprint arXiv:2407.02524, 2024.                                          intel: Comparing cloud compute, 2020.
[27] Ron Cytron, Jeanne Ferrante, Barry K Rosen, Mark N Wegman, and             [44] Shay Gal-On and Markus Levy. Exploring coremark a benchmark
     F Kenneth Zadeck. An efficient method of computing static single                maximizing simplicity and efficacy. The Embedded Microprocessor
     assignment form. In Proceedings of the 16th ACM SIGPLAN-SIGACT                  Benchmark Consortium, 6(23):87, 2012.
     symposium on Principles of programming languages, pages 25–35,             [45] Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi
     1989.                                                                           Bi, Yixin Dai, Jiawei Sun, Haofen Wang, and Haofen Wang. Retrieval-
[28] Ron Cytron, Jeanne Ferrante, Barry K Rosen, Mark N Wegman, and                  augmented generation for large language models: A survey. arXiv
     F Kenneth Zadeck. Efficiently computing static single assignment                preprint arXiv:2312.10997, 2(1), 2023.
     form and the control dependence graph. ACM Transactions on Pro-            [46] Redha Gouicem, Dennis Sprokholt, Jasper Ruehl, Rodrigo CO Rocha,
     gramming Languages and Systems (TOPLAS), 13(4):451–490, 1991.                   Tom Spink, Soham Chakraborty, and Pramod Bhatotia. Risotto: A
[29] Amanieu d’Antras, Cosmin Gorgovan, Jim Garside, John Goodacre,                  dynamic binary translator for weak memory model architectures. In
     and Mikel Luján. Hypermambo-x64: Using virtualization to support                Proceedings of the 28th ACM International Conference on Architectural
     high-performance transparent binary translation. In Proceedings of              Support for Programming Languages and Operating Systems, Volume
     the 13th ACM SIGPLAN/SIGOPS International Conference on Virtual                 1, pages 107–122, 2022.
     Execution Environments, pages 228–241, 2017.                               [47] Part Guide. Intel® 64 and ia-32 architectures software developer’s
[30] Sandeep Dasgupta, Sushant Dinesh, Deepan Venkatesh, Vikram S                    manual. Volume 3B: system programming guide, Part, 2(11):0–40, 2011.
     Adve, and Christopher W Fletcher. Scalable validation of binary lifters.   [48] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao
     In Proceedings of the 41st ACM SIGPLAN Conference on Programming                Zhang, Guanting Chen, Xiao Bi, Yu Wu, YK Li, et al. Deepseek-coder:
     Language Design and Implementation, pages 655–671, 2020.                        When the large language model meets programming–the rise of code
[31] Sandeep Dasgupta, Daejun Park, Theodoros Kasampalis, Vikram S                   intelligence. arXiv preprint arXiv:2401.14196, 2024.
     Adve, and Grigore Roşu. A complete formal semantics of x86-64              [49] Yuko Hara, Hiroyuki Tomiyama, Shinya Honda, Hiroaki Takada, and
     user-level instruction set architecture. In Proceedings of the 40th             Katsuya Ishii. Chstone: A benchmark program suite for practical
     ACM SIGPLAN Conference on Programming Language Design and                       c-based high-level synthesis. In 2008 IEEE International Symposium
     Implementation, pages 1133–1148, 2019.                                          on Circuits and Systems (ISCAS), pages 1192–1195. IEEE, 2008.
[32] Leonardo De Moura and Nikolaj Bjørner. Z3: An efficient smt solver.        [50] Niranjan Hasabnis and R Sekar. Lifting assembly to intermediate
     In International conference on Tools and Algorithms for the Construction        representation: A novel approach leveraging compilers. In Proceedings
     and Analysis of Systems, pages 337–340. Springer, 2008.                         of the Twenty-First International Conference on Architectural Support
[33] B De Sutter, K De Bosschere, Peter Keyngnaert, and Bart Demoen.                 for Programming Languages and Operating Systems, pages 311–324,
     On the static analysis of indirect control transfers in binaries. In            2016.
     Proceedings of the International Conference on Parallel and Distributed    [51] Jingxuan He, Pesho Ivanov, Petar Tsankov, Veselin Raychev, and Mar-
     Processing Techniques and Applications, volume 2, pages 1013–1019.              tin Vechev. Debin: Predicting debug information in stripped binaries.
     CSREA PRESS, 2000.                                                              In Proceedings of the 2018 ACM SIGSAC Conference on Computer and
[34] Chinmay Deshpande, Fabian Parzefall, Felicitas Hetzelt, and Michael             Communications Security, pages 1667–1680, 2018.
     Franz. Polynima: Practical hybrid recompilation for multithreaded          [52] John L Henning. Spec cpu2006 benchmark descriptions. ACM
     binaries. In Proceedings of the Nineteenth European Conference on               SIGARCH Computer Architecture News, 34(4):1–17, 2006.
     Computer Systems, pages 1126–1141, 2024.                                   [53] Hex-Rays. Ida pro powerful disassembler, decompiler and a versatile
[35] Alessandro Di Federico, Pietro Fezzardi, and Giovanni Agosta. rev.              debugger. https://hex-rays.com/ida-pro, 2025.
     ng: A multi-architecture framework for reverse engineering and             [54] HiSilicon. Kunpeng chipsets. https://www.hisilicon.com/en/
     vulnerability discovery. In 2018 International Carnahan Conference              products/Kunpeng/Huawei-Kunpeng/Huawei-Kunpeng-920, 2024.
     on Security Technology (ICCST), pages 1–5. IEEE, 2018.                     [55] R. Nigel Horspool and Nenad Marovac. An approach to the problem of
[36] Alessandro Di Federico, Mathias Payer, and Giovanni Agosta. rev.                detranslation of computer programs. The Computer Journal, 23(3):223–
     ng: a unified binary analysis framework to recover cfgs and function            229, 1980.
     boundaries. In Proceedings of the 26th International Conference on         [56] Simon Howard. A library of common data structures and algorithms
     Compiler Construction, pages 131–141, 2017.                                     written in c. https://github.com/fragglet/c-algorithms, 2024.
[37] Artem Dinaburg and Andrew Ruef. Mcsema: Static translation of              [57] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin
     x86 instructions to llvm. In ReCon 2014 Conference, Montreal, Canada,           Feng, Haotian Wang, Qianglong Chen, Weihua Peng, Xiaocheng
     2014.                                                                           Feng, Bing Qin, et al. A survey on hallucination in large language
EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk                                                                                   Zhibo Liu et al.


      models: Principles, taxonomy, challenges, and open questions. ACM        [74] Zhibo Liu, Yuanyuan Yuan, Shuai Wang, and Yuyan Bao. Sok: Demys-
      Transactions on Information Systems, 2023.                                    tifying binary lifters through the lens of downstream applications. In
 [58] Huawei. Huawei kunpeng exagear. https://www.hikunpeng.com/                    2022 IEEE Symposium on Security and Privacy (SP), pages 1100–1119.
      document/detail/en/kunpengdevps/ug-exagear/usermanual/                        IEEE, 2022.
      kunpengexagear_06_0003.html, 2024.                                       [75] Nuno P Lopes, Juneyoung Lee, Chung-Kil Hur, Zhengyang Liu, and
 [59] ibireme. The fastest json library in c. https://github.com/ibireme/           John Regehr. Alive2: bounded translation validation for llvm. In
      yyjson, 2024.                                                                 Proceedings of the 42nd ACM SIGPLAN International Conference on
 [60] Jinhu Jiang, Rongchao Dong, Zhongjun Zhou, Changheng Song, Wen-               Programming Language Design and Implementation, pages 65–79,
      wen Wang, Pen-Chung Yew, and Weihua Zhang. More with less–                    2021.
      deriving more translation rules with less training data for dbts using   [76] William Mahoney and J Todd McDonald. Enumerating x86-64 - it’s
      parameterization. In 2020 53rd Annual IEEE/ACM International Sym-             not as easy as counting. In Technical report, University of Nebraska
      posium on Microarchitecture (MICRO), pages 415–426. IEEE, 2020.               Omaha, 2021.
 [61] Jinhu Jiang, Chaoyi Liang, Rongchao Dong, Zhaohui Yang, Zhongjun         [77] Alessandro Mantovani, Luca Compagna, Yan Shoshitaishvili, and
      Zhou, Wenwen Wang, Pen-Chung Yew, and Weihua Zhang. A system-                 Davide Balzarotti. The convergence of source code and binary vul-
      level dynamic binary translator using automatically-learned trans-            nerability discovery–a case study. In Proceedings of the 2022 ACM
      lation rules. In 2024 IEEE/ACM International Symposium on Code                on Asia Conference on Computer and Communications Security, pages
      Generation and Optimization (CGO), pages 423–434. IEEE, 2024.                 602–615, 2022.
 [62] Theodoros Kasampalis, Daejun Park, Zhengyao Lin, Vikram S Adve,          [78] Andrea Marcelli, Mariano Graziano, Xabier Ugarte-Pedrero, Yanick
      and Grigore Roşu. Language-parametric compiler validation with                Fratantonio, Mohamad Mansouri, and Davide Balzarotti. How ma-
      application to llvm. In Proceedings of the 26th ACM International             chine learning is solving the binary function similarity problem. In
      Conference on Architectural Support for Programming Languages and             31st USENIX Security Symposium (USENIX Security 22), pages 2099–
      Operating Systems, pages 1004–1019, 2021.                                     2116, 2022.
 [63] Hyungseok Kim, Soomin Kim, and Sang Kil Cha. Towards sound               [79] Xiaozhu Meng and Barton P Miller. Binary code is not easy. In
      reassembly of modern x86-64 binaries. In Proceedings of the 30th ACM          Proceedings of the 25th International Symposium on Software Testing
      International Conference on Architectural Support for Programming             and Analysis, pages 24–35, 2016.
      Languages and Operating Systems, Volume 2, pages 1317–1333, 2025.        [80] Microsoft.         How emulation works on arm.                  https:
 [64] Hyungseok Kim, Soomin Kim, Junoh Lee, Kangkook Jee, and Sang Kil              //learn.microsoft.com/en-us/windows/arm/apps-on-arm-x86-
      Cha. Reassembly is hard: a reflection on challenges and strategies.           emulation, 2024.
      In 32nd USENIX Security Symposium (USENIX Security 23), pages            [81] Trail of Bits. Framework for lifting x86, amd64, aarch64, sparc32, and
      1469–1486, 2023.                                                              sparc64 program binaries to llvm bitcode. https://github.com/lifting-
 [65] Johannes Kinder. Static analysis of x86 executables. 2010.                    bits/mcsema, 2025.
 [66] Daniel Kusswurm and Daniel Kusswurm. X87 fpu programming.                [82] OpenAI. Gpt-4 is openai’s most advanced system, producing safer
      Modern X86 Assembly Language Programming: 32-bit, 64-bit, SSE, and            and more useful responses. https://openai.com/index/gpt-4/, 2024.
      AVX, pages 103–131, 2014.                                                [83] Fabian Parzefall, Chinmay Deshpande, Felicitas Hetzelt, and Michael
 [67] Celine Lee, Abdulrahman Mahmoud, Michal Kurek, Simone Cam-                    Franz. What you trace is what you get: dynamic stack-layout recovery
      panoni, David Brooks, Stephen Chong, Gu-Yeon Wei, and Alexan-                 for binary recompilation. In Proceedings of the 29th ACM International
      der M Rush. Guess & sketch: Language model guided transpilation.              Conference on Architectural Support for Programming Languages and
      arXiv preprint arXiv:2309.14396, 2023.                                        Operating Systems, Volume 2, pages 1250–1263, 2024.
 [68] Sung-Jin Lee, Sang-Soo Park, and Ki-Seok Chung. Efficient simd           [84] Kexin Pei, Jonas Guan, David Williams-King, Junfeng Yang, and
      implementation for accelerating convolutional neural network. In              Suman Jana. Xda: Accurate, robust disassembly with transfer learning.
      Proceedings of the 4th International Conference on Communication and          arXiv preprint arXiv:2010.00770, 2020.
      Information Processing, pages 174–179, 2018.                             [85] Sebastian Poeplau and Aurélien Francillon. Symbolic execution with
 [69] Xinyu Li, Guangyao Guo, Yanzhi Lan, Feng Xue, Chenji Han, Gen                 {SymCC}: Don’t interpret, compile! In 29th USENIX Security Sympo-
      Niu, and Fuxin Zhang. Tiaozhuan: A general and efficient indirect             sium (USENIX Security 20), pages 181–198, 2020.
      branch optimization for binary translation. ACM Transactions on          [86] Sebastian Poeplau and Aurélien Francillon. Symqemu: Compilation-
      Architecture and Code Optimization, 2024.                                     based symbolic execution for binaries. In NDSS 2021, Network and
 [70] Xinyu Li, Guangyao Guo, Yanzhi Lan, Feng Xue, Chenji Han, Gen                 Distributed System Security Symposium. Internet Society, 2021.
      Niu, and Fuxin Zhang. Tiaozhuan: A general and efficient indirect        [87] QEMU.          emit.c.inc.      https://github.com/qemu/qemu/blob/
      branch optimization for binary translation. ACM Transactions on               bc6afa1c711da5b4f37c9685a812c77b114d84cb/target/i386/tcg/
      Architecture and Code Optimization, 22(1):1–26, 2025.                         emit.c.inc#L2468, 2024.
 [71] Yi Li, Aws Albarghouthi, Zachary Kincaid, Arie Gurfinkel, and Marsha     [88] Zhenxiao Qi, Jie Hu, Zhaoqi Xiao, and Heng Yin. {SymFit}: Making
      Chechik. Symbolic optimization with smt solvers. ACM SIGPLAN                  the common (concrete) case fast for {Binary-Code} concolic execu-
      Notices, 49(1):607–618, 2014.                                                 tion. In 33rd USENIX Security Symposium (USENIX Security 24), pages
 [72] Zongjie Li, Chaozheng Wang, Pingchuan Ma, Chaowei Liu, Shuai                  415–432, 2024.
      Wang, Daoyuan Wu, Cuiyun Gao, and Yang Liu. On extracting                [89] Qualcomm. Snapdragon x elite. https://www.qualcomm.com/
      specialized code abilities from large language models: A feasibility          products/mobile/snapdragon/laptops-and-tablets/snapdragon-x-
      study. In Proceedings of the IEEE/ACM 46th International Conference on        elite, 2024.
      Software Engineering, ICSE ’24, New York, NY, USA, 2024. Association     [90] NGUYEN Anh Quynh and DANG Hoang Vu. Unicorn: Next genera-
      for Computing Machinery.                                                      tion cpu emulator framework. BlackHat USA, 476, 2015.
 [73] Zhibo Liu and Shuai Wang. How far we have come: Testing decom-           [91] Rodrigo CO Rocha, Dennis Sprokholt, Martin Fink, Redha Gouicem,
      pilation correctness of c decompilers. In Proceedings of the 29th ACM         Tom Spink, Soham Chakraborty, and Pramod Bhatotia. Lasagne: A
      SIGSOFT International Symposium on Software Testing and Analysis,             static binary translator for weak memory model architectures. In
      pages 475–487, 2020.                                                          Proceedings of the 43rd ACM SIGPLAN International Conference on
                                                                                    Programming Language Design and Implementation, pages 888–902,
                                                                                                EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk


      2022.                                                                           Vasileios P Kemerlis. Egalito: Layout-agnostic binary recompilation.
 [92] Edward J Schwartz, Thanassis Avgerinos, and David Brumley. All                  In Proceedings of the Twenty-Fifth International Conference on Archi-
      you ever wanted to know about dynamic taint analysis and forward                tectural Support for Programming Languages and Operating Systems,
      symbolic execution (but might have been afraid to ask). In 2010 IEEE            pages 133–147, 2020.
      symposium on Security and privacy, pages 317–331. IEEE, 2010.             [111] Wai Kin Wong, Daoyuan Wu, Huaijin Wang, Zongjie Li, Zhibo Liu,
 [93] Agam Shah. We’re closing the gap with arm and x86, claims sifive:               Shuai Wang, Qiyi Tang, Sen Nie, and Shi Wu. Decllm: Llm-augmented
      New risc-v cpu core for pcs, servers, mobile incoming ś the register,           recompilable decompilation for enabling programmatic use of de-
      2021.                                                                           compiled code. Proceedings of the ACM on Software Engineering,
 [94] Ken Shirriff. Silicon reverse-engineering: the intel 8086 proces-               2(ISSTA):1841–1864, 2025.
      sor’s flag circuitry. https://www.righto.com/2023/02/silicon-reverse-     [112] Benyi Xie, Yue Yan, Chenghao Yan, Sicheng Tao, Zhuangzhuang
      engineering-intel-8086.html, 2023.                                              Zhang, Xinyu Li, Yanzhi Lan, Xiang Wu, Tianyi Liu, Tingting Zhang,
 [95] Yan Shoshitaishvili, Ruoyu Wang, Christopher Salls, Nick Stephens,              et al. An instruction inflation analyzing framework for dynamic
      Mario Polino, Andrew Dutcher, John Grosen, Siji Feng, Christophe                binary translators. ACM Transactions on Architecture and Code Opti-
      Hauser, Christopher Kruegel, et al. Sok:(state of) the art of war:              mization, 21(2):1–25, 2024.
      Offensive techniques in binary analysis. In 2016 IEEE symposium on        [113] Danning Xie, Zhuo Zhang, Nan Jiang, Xiangzhe Xu, Lin Tan, and
      security and privacy (SP), pages 138–157. IEEE, 2016.                           Xiangyu Zhang. Resym: Harnessing llms to recover variable and
 [96] Douglas R Smith. The design of divide and conquer algorithms.                   data structure symbols from stripped binaries. In Proceedings of the
      Science of Computer Programming, 5:37–58, 1985.                                 2024 on ACM SIGSAC Conference on Computer and Communications
 [97] Changheng Song, Wenwen Wang, Pen-Chung Yew, Antonia Zhai,                       Security, pages 4554–4568, 2024.
      and Weihua Zhang. Unleashing the power of learning: An enhanced           [114] S Bharadwaj Yadavalli and Aaron Smith. Raising binaries to llvm
      {Learning-Based} approach for dynamic binary translation. In 2019               ir with mctoll (wip paper). In Proceedings of the 20th ACM SIG-
      USENIX Annual Technical Conference (USENIX ATC 19), pages 77–90,                PLAN/SIGBED International Conference on Languages, Compilers, and
      2019.                                                                           Tools for Embedded Systems, pages 213–218, 2019.
 [98] Tom Spink, Harry Wagstaff, and Björn Franke. A retargetable system-       [115] Yapeng Ye, Zhuo Zhang, Qingkai Shi, Yousra Aafer, and Xiangyu
      level dbt hypervisor. ACM Transactions on Computer Systems (TOCS),              Zhang. D-arm: Disassembling arm binaries by lightweight superset
      36(4):1–24, 2020.                                                               instruction interpretation and graph modeling. In 2023 IEEE Sympo-
 [99] Hanzhuo Tan, Qi Luo, Jing Li, and Yuqun Zhang. Llm4decompile:                   sium on Security and Privacy (SP), pages 2391–2408. IEEE, 2023.
      Decompiling binary code with large language models. In Proceedings        [116] Sheng Yu, Yu Qu, Xunchao Hu, and Heng Yin. {DeepDi}: Learning
      of the 2024 Conference on Empirical Methods in Natural Language                 a relational graph convolutional network model on instructions for
      Processing, pages 3473–3487, 2024.                                              fast and accurate disassembly. In 31st USENIX Security Symposium
[100] Rev.ng team. Failure when trying to translate a simple dynamic                  (USENIX Security 22), pages 2709–2725, 2022.
      x86-64 binary compiled with clang. https://github.com/revng/revng/        [117] Yue Zhang, Yafu Li, Leyang Cui, Deng Cai, Lemao Liu, Tingchen Fu,
      issues/317#issuecomment-1721136071, 2025.                                       Xinting Huang, Enbo Zhao, Yu Zhang, Yulong Chen, et al. Siren’s
[101] Michael James Van Emmerik. Static single assignment for decompila-              song in the ai ocean: a survey on hallucination in large language
      tion. University of Queensland, 2007.                                           models. arXiv preprint arXiv:2309.01219, 2023.
[102] Fish Wang and Yan Shoshitaishvili. Angr-the next generation of            [118] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang,
      binary analysis. In 2017 IEEE Cybersecurity Development (SecDev),               Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican
      pages 8–9. IEEE, 2017.                                                          Dong, et al. A survey of large language models. arXiv preprint
[103] Ruoyu Wang, Yan Shoshitaishvili, Antonio Bianchi, Aravind Machiry,              arXiv:2303.18223, 2023.
      John Grosen, Paul Grosen, Christopher Kruegel, and Giovanni Vigna.        [119] Anshunkang Zhou, Chengfeng Ye, Heqing Huang, Yuandao Cai, and
      Ramblr: Making reassembly great again. In NDSS, 2017.                           Charles Zhang. Plankton: Reconciling binary code and debug in-
[104] Shuai Wang, Pei Wang, and Dinghao Wu. Reassembleable disas-                     formation. In Proceedings of the 29th ACM International Conference
      sembling. In 24th USENIX Security Symposium (USENIX Security 15),               on Architectural Support for Programming Languages and Operating
      pages 627–642, 2015.                                                            Systems, Volume 2, pages 912–928, 2024.
[105] Wenwen Wang, Stephen McCamant, Antonia Zhai, and Pen-Chung                [120] Zhiping Zhou, Xiaohong Li, Ruitao Feng, Yao Zhang, Yuekang Li,
      Yew. Enhancing cross-isa dbt through automatically learned transla-             Wenbu Feng, Yunqian Wang, and Yuqing Li. Fidelitygpt: Correcting
      tion rules. ACM SIGPLAN Notices, 53(2):84–97, 2018.                             decompilation distortions with retrieval augmented generation. In
[106] Wenwen Wang, Pen-Chung Yew, Antonia Zhai, and Stephen McCa-                     Network and Distributed System Security (NDSS) Symposium 2026.
      mant. A general persistent code caching framework for dynamic             [121] Albert Ziegler, Eirini Kalliamvakou, X Alice Li, Andrew Rice, Devon
      binary translation ({ { { { {DBT} } } } }). In 2016 USENIX Annual Tech-         Rifkin, Shawn Simister, Ganesh Sittampalam, and Edward Aftandilian.
      nical Conference (USENIX ATC 16), pages 591–603, 2016.                          Productivity assessment of neural code completion. In Proceedings of
[107] Zhaoguo Wang, Ran Liu, Yufei Chen, Xi Wu, Haibo Chen, Weihua                    the 6th ACM SIGPLAN International Symposium on Machine Program-
      Zhang, and Binyu Zang. Coremu: a scalable and portable parallel                 ming, pages 21–29, 2022.
      full-system emulator. In Proceedings of the 16th ACM symposium on         [122] zyantific. Fast and lightweight x86/x86-64 disassembler and code
      Principles and practice of parallel programming, pages 213–222, 2011.           generation library. https://github.com/zyantific/zydis, 2024.
[108] Albert Webson and Ellie Pavlick. Do prompt-based models re-
      ally understand the meaning of their prompts? arXiv preprint
      arXiv:2109.01247, 2021.
[109] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia,
      Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-of-thought prompt-
      ing elicits reasoning in large language models. Advances in neural
      information processing systems, 35:24824–24837, 2022.
[110] David Williams-King, Hidenori Kobayashi, Kent Williams-King,
      Graham Patterson, Frank Spano, Yu Jian Wu, Junfeng Yang, and
EUROSYS ’26, April 27–30, 2026, Edinburgh, Scotland Uk                                                                           Zhibo Liu et al.


A     Appendix                                                                        Table 10. Mctoll’s Error Messages.

                   Table 9. Evaluated software.                              Test        Error Message
                                                                                         Branch instruction terminating basic block
                                                                            adpcm
                                                                                         computing jump table
      Name         Description                                               gsm         Unhandled memory referencing instruction
                   Adaptive differential pulse code modulation                           Branch instruction terminating basic block
      adpcm                                                                 mips
                   decoder and encoder                                                   computing jump table
         gsm       Linear predictive coding analysis of audio signal                     Unhandled PUSH instruction with non-AddrRegFrm
        mips       Simplified MIPS processor                               motion
                                                                                         source operand
       motion      Motion vector decoding for MPEG-2                                     Null reaching definition found during reaching
                                                                             aes
         aes       Advanced encryption standard                                          definition fixup
        sha1       Secure hash algorithm                                    sha1         Alignment is neither 0 nor a power of 2
     blowfish      Symmetric-key block cipher                                            Null reaching definition found during reaching
                                                                          blowfish
        jpeg       Image decompression                                                   definition fixup
        cjpeg      JPEG image compression                                                Branch instruction terminating basic block
                                                                            jpeg
       sha256      Secure hash algorithm                                                 computing jump table
      linpack      Gaussian elimination with partial pivoting              cjpeg         Unknown opcode
        nnet       Neural net                                              sha256        Unknown opcode
        loops      Kernels based on Livermore loops                       linpack        Unknown opcode
       parser      XML parsing                                              nnet         Unknown opcode
       radix2      Radix-2 fast Fourier transform                          loops         Unknown opcode
        zlib       ZIP compression                                         parser        Unknown opcode
        bzip2      File compression                                        radix2        Unknown opcode
                                                                            zlib         Unknown opcode
          xz       File compressions
                                                                           bzip2         cast<Ty>() argument of incompatible type!
         mcf       Single-depot vehicle scheduling
                                                                             xz          Unexpected block terminator found
    libquantum     Physics / Quantum computing
                                                                             mcf         Unknown opcode
        hmmer      Gene sequence database searching                     libquantum       Unhandled SSE Packed Single Prefix encountered
        zydis      Disassembler library                                                  Branch instruction terminating basic block
       yyjson      JSON library                                             hmmer
                                                                                         computing jump table
                                                                           zydis         Unexpected number of successors of switch block
A.1    Performance of Static Concise IR Lifters                            yyjson        Unexpected block terminator found

We evaluated three state-of-the-art static concise IR lifters,
                                                                         struct stat64 {                          struct stat64 {
including Mctoll, RetDec, and Rev.ng, on the same set of                     __dev_t st_dev;                          __dev_t st_dev;
                                                                             __ino64_t st_ino;                        __ino64_t st_ino;
23 software used in our evaluation. We found that these                      __nlink_t st_nlink;                      __mode_t st_mode;
                                                                             __mode_t st_mode;                        __nlink_t st_nlink;
lifters failed in all cases. Specifically, RetDec and Rev.ng can             __uid_t st_uid;                          __uid_t st_uid;
produce lifted IR code for all cases, but the lifted IR code                 __gid_t st_gid;                          __gid_t st_gid;
                                                                             ...                                      ...
is either non-compilable or functionally incorrect. RetDec               };                                       };

extensively skips and leaves unimplemented instructions in               In Linux kernel for x86-64               In Linux kernel for AArch64
its output undefined, while Rev.ng translated binaries crash             struct stat64 {
immediately upon execution. On the other hand, Mctoll fails                  __dev_t st_dev;              /* Device.       */
                                                                         # ifdef __x86_64__
to lift any of the cases, with error messages reported in                    __ino64_t st_ino;            /* File serial number.       */
                                                                             __nlink_t st_nlink;          /* Link count. */
Table 10.                                                                    __mode_t st_mode;            /* File mode. */
                                                                         # else
                                                                             unsigned int __pad1;
                                                                             __ino_t __st_ino;            /* 32bit file serial number.*/
A.2    Binary-Level Data Structure Inconsistency                             __mode_t st_mode;            /* File mode. */
                                                                             __nlink_t st_nlink;          /* Link count. */
As shown in Fig. 10, Linux kernel defines the stat structure             # endif
                                                                         ...
in different ways for x86-64 1 and AArch64 2 architectures.              };
Specifically, the order of st_nlink and st_mode are differ-                                      Relevant code in glibc.
ent. And glibc handles this difference by explicitly parsing
data returned by system calls according to the target archi-              Figure 10. Binary-level data structure inconsistency.
tecture 3 , but still retains such binary-level data structure
1 https://github.com/torvalds/linux/blob/                              inconsistency. In this example, glibc keep the same API
8cf0b93919e13d1e8d4466eb4080a4c4d9d66d7b/arch/x86/include/uapi/        for fstat system call. Source-level references to specific
asm/stat.h#L42                                                         members in stat structure are still valid. However, since
2 https://github.com/torvalds/linux/blob/8cf0b93919e13d1e8d4466eb-
                                                                       binary-level references are achieved with constant offsets,
4080a4c4d9d66d7b/arch/arm/include/uapi/asm/stat.h#L57
3 https://github.com/lattera/glibc/blob/                               the inconsistency in the layout of stat structure may cause
895ef79e04a953cac1493863bcae29ad85657ee1/sysdeps/unix/sysv/linux/      the translated binary to access wrong members.
x86/bits/stat.h#L119
