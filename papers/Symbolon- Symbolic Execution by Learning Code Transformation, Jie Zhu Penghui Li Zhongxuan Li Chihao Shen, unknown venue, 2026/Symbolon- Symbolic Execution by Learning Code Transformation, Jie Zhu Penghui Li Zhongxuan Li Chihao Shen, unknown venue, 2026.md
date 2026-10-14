                                                       Symbolon: Symbolic Execution by Learning Code Transformation

                                                     Jie Zhu                       Penghui Li                        Zhongxuan Li                    Chihao Shen
                                              University of Chicago            Columbia University               University of Chicago          University of Maryland
                                              jiezhu@uchicago.edu             pl2689@columbia.edu                 zxli7@uchicago.edu              stevencs@umd.edu

                                                                   Ziyang Li                     Yizheng Chen                         Kexin Pei
                                                            Johns Hopkins University         University of Maryland              University of Chicago
                                                                ziyang@jhu.edu                 yzchen@umd.edu                     kpei@uchicago.edu

                                         Abstract—Symbolic execution is a powerful program analysis              applied to analyze and secure a broad spectrum of real-
                                         technique with broad applications, such as vulnerability de-            world, security-critical software, including operating-system
                                         tection, security testing, and malware analysis. However, this          kernels and device stacks [20, 24, 38, 39, 40, 41, 42, 43],
                                         technique is known to suffer from scalability issues, e.g., path        browsers [25], web and mobile applications [44, 45, 46, 47,
arXiv:2606.29108v2 [cs.CR] 21 Jul 2026




                                         explosion, complex constraints, due to certain structural and           48, 49, 50, 51, 52, 53], commercial off-the-shelf (COTS)
                                         semantic patterns commonly presented in real-world programs.            binary software [42, 54, 55, 56, 57, 58], low-level systems
                                         Existing approaches attempt to escape these patterns by trans-          code [59, 60, 61], embedded and firmware systems [62, 63,
                                         forming programs into new representations to reduce the exe-            64, 65], and safety-critical cyber-physical systems [66, 67,
                                         cution cost. Unfortunately, these transformations are often too         68, 69, 70, 71].
                                         rigid to exploit diverse local program semantics and sometimes              Despite these successes, symbolic execution remains dif-
                                         rely on compiler optimizations designed for concrete execution          ficult to scale to large, real-world programs, where modest
                                         that may misalign with the goals of symbolic execution.                 increases in program size and functionality can induce dis-
                                             We present Symbolon, a framework that automatically                 proportionate cost due to path explosion and hard-to-solve
                                         learns diverse code transformations and applies them context-           path constraints [5, 34, 72, 73, 74, 75]. These costs often
                                         sensitively to improve symbolic execution. Our key insight is           arise from common source-level program structures. For
                                         to formulate transformation discovery as a search problem
                                                                                                                 example, when a loop bound depends on a symbolic input,
                                         over program representations. To make the search practical,
                                                                                                                 the symbolic execution engine may fork many iterations,
                                                                                                                 quickly exhausting its path budget [3, 72, 73, 76, 77]. Even
                                         Symbolon learns transformations cheaply offline on small pro-
                                                                                                                 along a single path, code that derives predicates or memory
                                         grams, distills them into a reusable library of agent skills, and
                                                                                                                 addresses from symbolic values, e.g., bit-level encodings,
                                         uses an agent to instantiate these skills on repo-level targets.
                                                                                                                 pointer arithmetic, can produce expensive constraints for
                                         Our evaluation shows that Symbolon substantially improves the
                                                                                                                 SMT solvers to discharge [6, 78, 79, 80]. Importantly, these
                                         symbolic execution engine KLEE across 16 search strategies on
                                                                                                                 costs are representation-sensitive. Two equivalent implemen-
                                         32 real-world programs, increasing line coverage by 3.69× on
                                                                                                                 tations can expose different numbers of branches, different
                                         average while reducing peak memory and per-query solver time            memory-access patterns, and different constraints for the
                                         by 29.2× and 123×, respectively. When applied to the latest             solver, making them either easier or harder for symbolic exe-
                                         Linux kernel, Symbolon uncovers 21 previously unknown bugs,             cution to analyze [81]. The scalability of symbolic execution
                                         all of which have been reported to the kernel maintainers.              is thus shaped not only by what a program computes, but
                                                                                                                 also by how that computation is represented in code.
                                         1. Introduction                                                             This susceptibility to code representation suggests a com-
                                                                                                                 plementary approach to improving symbolic execution by
                                              Symbolic execution is a well-established and influen-              transforming and enriching the program representation before
                                         tial program analysis technique that systematically explores            exposing it to symbolic execution [5, 54, 74, 82]. In fact,
                                         program states under symbolic inputs [1, 2, 3, 4, 5] to rea-            program transformation is known to substantially affect the
                                         son about program properties and behaviors [6, 7, 8, 9]. It             behavior of program analyses [83, 84, 85, 86, 87, 88, 89],
                                         has been used as a key building block for a wide range of               and symbolic execution is no exception [81]. Prior work has
                                         code reasoning tasks, including checking reachability proper-           explored several ways to expose symbolic-execution-friendly
                                         ties [10, 11, 12, 13, 14, 15, 16], generating high-coverage test        code representations based on compiler optimizations [80, 81,
                                         inputs [3, 17, 18, 19, 20, 21], and detecting bugs and security         90], targeted transformations for data structures and control
                                         vulnerabilities [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32].           flow [91, 92, 93], operator-specific rewrites [94, 95, 96], and
                                         As a result, symbolic execution has supported production-               even semantics-breaking (behavior-changing) transformations
                                         scale testing workflows [33, 34, 35, 36, 37], and has been              that trade program equivalence for higher test coverage [97].


                                                                                                             1
    However, existing transformation-based approaches re-             addresses the second by decoupling transformation discovery
main limited by how transformations are obtained and applied.         from deployment. Specifically, Symbolon learns the transfor-
Compiler optimizations provide only a fixed set of transfor-          mations only from small programs [107], where symbolic
mations designed primarily for concrete execution objectives,         execution and replay are cheap, and distills effective trans-
such as execution time and code size, but they can misalign           formations into reusable rules as persistent agent skills [108,
with symbolic execution objectives, such as optimizing cov-           109]. These learned skills capture recurring transformation
erage, reachability, and solver cost. Other transformations           patterns, grounding later agentic transformations for larger,
tailored for symbolic execution are typically hand-coded for          real-world projects. As this learning incurs only a one-time
a narrow class of syntactic patterns or program constructs,           cost, its cost can be amortized across projects and symbolic
e.g., specific operators on symbolic indices, and thus require        execution campaigns. Figure 2 shows Symbolon’s workflow.
substantial human expertise, miss useful transformations out-             Such a technical design in Symbolon directly addresses
side predefined patterns, and are often too rigid to be broadly       the rigidity of prior transformation-based approaches. The
applied. This is problematic because the benefit of a trans-          learned skills are discovered automatically rather than manu-
formation is highly sensitive to local context (Section 2.2).         ally specified, instantiated in local contexts rather than applied
These fixed transformations that simplify branches, insert            globally, and selected by replay-based feedback rather than by
predicates [94, 98, 99, 100, 101], or replace data structure          potentially misaligned objectives in compiler optimizations.
operations, may remove a symbolic-execution barrier in one            As transformations are expressed at the source level, the
local context but suppress useful behavior in another, e.g.,          agent can leverage rich source-level hints, e.g., symbol names,
bypassing (adding predicates like klee_assume [102]) hash             comments, to adapt each transformation rule in the learned
or decryption checks may help a parser reach deeper payload-          agent skills to the target context. Importantly, the source-level
processing logic, but can miss the core behavior in cryp-             transformations make Symbolon orthogonal to engine-side
tographic libraries. Existing approaches lack a mechanism             improvements like search strategies [22, 110, 111, 112, 113,
for automatically discovering diverse, context-sensitive code         114, 115, 116, 117] and solver optimizations [117, 118, 119].
transformations optimized for symbolic execution.                     As a result, Symbolon consistently improves the effectiveness
                                                                      of KLEE across all its search strategies, e.g., by 3.69× in
Our approach. We present Symbolon, a framework that                   coverage (see Section 5), without the need to adapt to any
automatically discovers and applies diverse, context-sensitive        specific symbolic execution and compiler configurations.
code transformations for symbolic execution. Our key idea
                                                                      Results. We evaluate Symbolon across 32 popular real-
is to formulate transformation discovery as a search problem
                                                                      world software projects and 16 symbolic execution search
over program representations. Given a program that intro-
                                                                      strategies, including KLEE’s built-in strategies and the state-
duces symbolic execution barriers, Symbolon searches for an
                                                                      of-the-art searchers [112, 113, 114, 115, 116], to measure
alternative source-level representation that helps a symbolic
                                                                      how Symbolon complements existing approaches. Symbolon
execution engine generate inputs with improved metrics, e.g.,
                                                                      consistently improves coverage across all search strategies,
coverage, on the original program. With this search target,
                                                                      achieving an impressive 3.69× more covered lines, averaged
Symbolon expands the search space by essentially relaxing
                                                                      across all projects, while significantly reducing symbolic
the transformations to be semantics-breaking [97], rather
                                                                      execution overhead, i.e., by 29.2× and 123× in peak memory
than restricting the search within compiler optimizations or
                                                                      usage and solver time per query, respectively. It also uncovers
hand-written templates that strictly preserve the semantics.
                                                                      more sanitizer-reported security violations across all search
Specifically, Symbolon evaluates each transformation with a
                                                                      strategies and identifies 21 new bugs when used to aug-
transform-and-replay reward. It runs symbolic execution on
                                                                      ment the symbolic-execution-based Linux kernel bug-finding
the transformed program, replays the generated tests on the
                                                                      tool [20, 120]. We release our learned transformation rules
original program, and uses their improvement on the original
                                                                      (in agent skills), the agentic framework, and the transformed
code to guide the search. In this formulation, the transformed
                                                                      projects here: § cirrus-uchicago/Symbolon.
program essentially acts as a test-generation scaffold, while
the original program remains the optimization target. This            Contributions. We make the following contributions:
allows Symbolon to explore a much larger transformation               • We identify source-level program representation as the key
space, while keeping the search reward aligned with symbolic            optimization target for symbolic execution and formulate
execution objectives on the original program.                           transformation discovery as an automated search problem
     Making this formulation practical requires managing two            over program representations.
costs: the open-ended transformation space and reward evalu-          • We present Symbolon, a framework that automatically
ation. As semantics-breaking transformations further expand             learns diverse, reusable transformation rules from small
the search space, simple code mutation is unlikely to effi-             programs and transfers them as persistent agent skills to
ciently reach useful transformations. Computing the reward              facilitate diverse transformations of real-world projects.
exacerbates the cost by expensive symbolic execution (for test        • We operationalize replay on the original program as
generation) and replay. Symbolon addresses the first by using           a verifiable reward for transformation search, allowing
large language models (LLMs) as a search prior, drawing                 Symbolon to explore broad transformation spaces, includ-
on their recent successes in guiding evolutionary search                ing semantics-breaking ones, while ensuring the objective
over programs and large systems [103, 104, 105, 106]. It                of transformations aligns with that of symbolic execution.


                                                                  2
 • We evaluate Symbolon across a broad range of real-world               Each IFD contains a 2-byte directory-entry count, followed
   projects and search strategies, demonstrating consistent              by a sequence of 12-byte directory entries describing image
   coverage improvements, a significant reduction in sym-                metadata such as dimensions, sample layout, bit depth, and
   bolic execution overhead, and strong bug-finding capabil-             compression method, and ends with a 4-byte offset to the
   ities in systems such as the Linux kernel.                            next IFD, or zero if there is no subsequent IFD.
                                                                             Figure 1 illustrates the key parsing logic that iterates over
2. Overview                                                              the directory entries in an input TIFF file and configures the
                                                                         image decoder based on the extracted compression method.
   This section first describes the background of symbolic               Specifically, the parser first validates the byte order (line 4-5),
execution. We then present an example to motivate our work.              distinguishing between little-endian ("II") and big-endian
                                                                         ("MM"). It then extracts the directory entry count ndirs for
2.1. Symbolic Execution Background                                       the current IFD (line 7) and loops through each entry dir[i]
                                                                         to retrieve its content (line 8-9). After that, the parser extracts
    Symbolic execution is a program analysis technique for               metadata fields and uses them to compute the image strip size
systematically reasoning about program behaviors [1, 2, 3,               nbytes (line 14), which determines the buffer size allocated
5]. Instead of running a program with concrete inputs, a                 to hold the image strip data. Finally, it reads the compression
symbolic execution engine runs program 𝑃 with symbolic                   tag and dispatches to the corresponding decoder (line 16-20).
input to represent a set of possible inputs. During execution,           Symbolic execution on the original code. In this example,
the symbolic execution engine maintains a set of execution               the harness supplies a fixed-size (e.g., 300-byte) symbolic
states, where each state consists of the program counter that            input file through FILE *fp. The engine treats bytes read
tracks the current execution progress, and the path constraints          from fp as symbolic values and accumulates constraints
that collect accumulated conditions along the explored path              over them. After read_order at line 3, the value of order is
to characterize the inputs capable of reaching that state.               determined by the first two symbolic bytes, which encode the
    When symbolic execution reaches a branch whose con-                  byte order of the TIFF file. Branch C1 checks whether this
dition depends on symbolic values, it forks into multiple                value matches one of the two valid byte-order markers. Al-
successor states, each extended with the corresponding branch            though this appears as a single source-level condition, the two
predicate, and continues exploring different execution paths.            strcmp calls compare strings byte by byte, causing symbolic
As the number of states grows exponentially with the number              execution to fork inside the library routine to distinguish
of forks, the symbolic execution engine needs to select which            different mismatch positions. Most of these states return at
pending state to advance. Prior work has proposed various                 C1 . Only states consistent with order == "II" or order
strategies to prioritize certain states [112, 113, 114, 115, 116].       == "MM" reach the subsequent parsing logic.
A state is removed when it becomes infeasible or reaches a                   The next barrier is the directory-entry loop at C2 . The
termination statement, e.g., program exit or assertion failure.          loop bound ndirs is read from the symbolic input at line 7, so
The symbolic execution engine translates the corresponding               the loop condition at line 8 also depends on the symbolic data.
path constraints to a concrete test input that, when supplied            As a result, symbolic execution may fork at each iteration to
to 𝑃, drives execution along the same explored path.                     represent whether the loop exits or continues, creating states
Intrinsics. Symbolic execution engines are typically                     for many possible counts of directory entries. As ndirs is a
equipped with a set of intrinsic functions to support symbolic           16-bit value, this loop can expose a large number of possible
analysis. For example, sym_create() introduces a symbolic                iterations and quickly exhaust the exploration budget before
variable into the current execution state, which is helpful when         the engine reaches the following tag-processing logic.
applying symbolic execution to analyze a specific function                   Even after symbolic execution passes these path-explosion
without starting from the program entry point. In Section 2.2,           sources, the parser can still create solver-heavy expressions.
we use its variant sym_choose() to create a symbolic integer             At C3 , it computes nbytes by multiplying symbolic meta-
that constrains the variable into a finite set of choices. Another       data fields such as width, height, samples per pixel, and
widely used intrinsic is sym_assume(), which adds a new                  bits per sample. While the assignment itself does not add
constraint to the current path constraint, e.g., sym_assume(x            a path constraint, it builds a symbolic bit-vector expression.
> 0) adds x > 0 to the current path constraint. Symbolon                 When later operations constrain this value, the solver must
uses these intrinsics as part of the code transformation to              reason about symbolic multiplication and C integer overflow
make symbolic execution more efficient.                                  semantics, which is often much harder than linear arithmetic
                                                                         over symbolic values [72, 122]. Existing search strategies
2.2. Motivating Example                                                  may reach this code earlier, but they do not simplify the
                                                                         expression used in these later queries.
    In Figure 1, we present a simplified code snippet from the               The symbolic expression for nbytes then flows into an-
libtiff [121] for parsing and checking the metadata of TIFF              other barrier at C4 , where it is passed as the size argument
files. A typical TIFF file starts with an 8-byte header that             to _TIFFmalloc. Many symbolic execution engines handle
points to the first Image File Directory (IFD), where multiple           symbolic size allocations only under restrictions, e.g., by
IFDs can be linked together to support multi-page images.                concretizing the size, rejecting the allocation, or terminat-


                                                                     3
 Execution Trace                                  Original Code                                          Transformations                       Execution Trace
                                    1 int parse_image(FILE *fp) {
                                    2   char order[3];                                              T1
           Path Explosion                                                                                int choice = sym_choose(0, 2);         Deduplicate Equivalent States
                                    3   read_order(fp, order);                                           if (choice)
                            ···     4   if (strcmp(order, "II") && strcmp(order, "MM"))   C1               return TIFF_ERR;                                            ···
                                    5     return TIFF_ERR;                                               else
              TIFF_ERR              6   TIFFDirEntry dir[MAXTAGS];                                         sym_assume(order == "II");                     TIFF_ERR
                                    7   uint16_t ndirs = read16(fp);
           Path Explosion           8   for (uint16_t i = 0; i < ndirs; i++)              C2                                                       Concretize Loop Bound
                                    9     dir[i] = read_entry(fp);
        ···                  ···                                                                    T2                                              ···                   ···
                                   10   uint32_t w = get(dir, TAG_WIDTH);                                sym_assume(ndirs == 23);
                                   11   uint32_t h = get(dir, TAG_LENGTH);                               for (uint16_t i = 0; i < 23; i++)
 Complex Path                      12   uint16_t spp = get(dir, TAG_SAMPLES);                                                                                       Avoid Complex
   Constraints                     13   uint16_t bps = get(dir, TAG_BITS);                                                                                          Constraints
                                   14   size_t nbytes = (size_t) w * h * spp * bps / 8;   C3        T3
    Symbolic                       15                                                                    size_t nbytes = STRIP_MAX;                                 Allocate Concrete
   Malloc Size                     16   uint8_t *strip = _TIFFmalloc(nbytes);             C4             uint8_t *strip = malloc(nbytes);                           Memory Size
                                   17   uint16_t codec = get(dir, TAG_COMPRESS);
                                   18   fprintf(stderr, "codec %u", codec);               C5                                                                        Remove Irrele-
  Symbolic I/O
                                   19   decoders[codec](strip, nbytes);                             T4                                                              vant Statements
                                   20   return TIFF_OK;                                                  fprintf(stderr, "codec %u", codec);
                 TIFF_OK           21 }                                                                                                                   TIFF_OK


Figure 1: A motivating example from libtiff showing how Symbolon helps symbolic execution by transforming the code.
Each node in an execution trace represents an execution state, and each edge denotes a transition between two states. Nodes
with dashed borders indicate states that are no longer explored in symbolic execution.


ing states when the size cannot be bounded or modeled.                                         induce many loop iterations, Symbolon rewrites the loop into
Therefore, exploration may stop before reaching the decoder                                    a fixed-iteration one derived from the configured symbolic
dispatch. Similarly, C5 sends symbolic metadata to fprintf,                                    input size (in our harness, the symbolic TIFF input is capped
forcing the engine to model formatted file I/O for an out-                                     at 300 bytes). As a TIFF file uses an 8-byte header before the
put side effect that is irrelevant to decoder selection. These                                 first IFD, and the IFD then contains a 2-byte entry count, a
statements illustrate how basic memory management and I/O                                      sequence of 12-byte directory entries, and a 4-byte pointer to
APIs can become barriers when they take symbolic values.                                       the next IFD, the maximum number of directory   entries that
                                                                                               can fit in this input layout is thus 300−8−2−4    = 23. Since
Symbolon transforms the original code. The green snip-                                                                                    12
                                                                                               tiffinfo inspects metadata and does not need a large image
pets in Figure 1 show how Symbolon transforms the original
                                                                                               payload to reach the downstream decoder-dispatch logic, this
code into a representation that is easier for symbolic execu-
                                                                                               bound gives symbolic execution a concrete loop structure
tion to analyze. Note that these rewrites are not conventional
                                                                                               while preserving the ability to exercise the relevant parsing
compiler optimizations. They rely on understanding the local
                                                                                               code on the original program during replay.
source-level intent, such as which code implements a semantic
check, which values are needed only to reach downstream                                             Transformations T3 and T4 remove downstream barri-
parsing logic, and which side effects are irrelevant to the                                    ers that are not essential for reaching the decoder dispatch.
exploration goal. Such intent is difficult for fixed compiler                                  At C3 – C4 , the original code computes nbytes from sym-
passes to exploit safely, and blindly optimizing for concrete                                  bolic metadata fields and passes it to _TIFFmalloc, producing
execution can even obscure the symbolic execution objective.                                   both an expensive symbolic expression and a symbolic size
    Transformation T1 replaces the byte-order check with an                                    allocation. Symbolon replaces nbytes in the transformed
explicit symbolic choice that represents the semantic outcome                                  scaffold with the project-level bound STRIP_MAX, giving the
of the check, i.e., whether the byte order is valid or invalid.                                engine a concrete allocation size and avoiding the symbolic
This avoids forcing symbolic execution to reason through the                                   multiplication expression in later queries. At C5 , Symbolon
byte-by-byte implementation in strcmp and instead exposes                                      removes the diagnostic fprintf call, which only prints the
the source-level decision directly to the engine. In the valid                                 selected compression method and does not affect the parser
branch, Symbolon constrains order to "II" as a represen-                                       state or the following decoder dispatch. A standard com-
tative valid byte order, avoiding a separate exploration of                                    piler optimization generally cannot perform these rewrites,
the symmetric "MM" case. This transformation is specific                                       as concretizing nbytes or removing formatted output can
to the local context, in that it is appropriate here because                                   change the program’s observable behavior. In Symbolon,
the subsequent logic in the simplified example only needs                                      however, since the transformed code is used only as a test-
a valid byte order to reach the tag-processing and decoder-                                    generation scaffold, all generated tests are replayed on the
dispatch code. If later code were data-dependent on the                                        original program to measure improvement, with the original
distinction between "II" and "MM", the transformation would                                    nbytes computation and fprintf call remaining intact.
need to preserve both valid cases. This is similar in spirit                                        Together, these transformations increase line coverage
to symmetry-breaking constraints [100, 101] and streamlin-                                     on libtiff from 1,251 to 1,660 lines (+32.7%) during an
ing [123], where additional constraints are introduced to                                      one-hour symbolic execution campaign. This comparison
avoid redundant regions of the search space.                                                   follows the same evaluation setting described in Section 5.1,
    Transformation T2 addresses the symbolic loop bound at                                     where the line coverage is measured by replaying symbolic
 C2 . Instead of allowing the 16-bit symbolic value ndirs to                                   execution generated test cases on the original program.


                                                                                          4
 Offline Learning                                                                                                                                 Online Inference
                                             Transformation Search                                       Rule Learning
    Symbolic Execution Profiling                                                                                                                            Repo-level Transformation
                                              Trace shows line 2 seems suspicious ...            Rationalize                    Skill Library
                                                                                                                                                   Persist                    libtiff/
    1    if (!memcmp(x, "test", 5)) {     int var = sym_choice(0, 2);                              Simplify iteratively     Skill 1: concretize                               tif_info.c
    2      printf("privacy\n");           if (var) {                                               checking all bytes          array size…                                     ...
    3    }                                                                                                                                            Agentic
                                            symbolic_assume(x == "test");                          of "test"                                         Transform                 Measure Coverage
    4    b = abs(y) + mod(y, 2);          }
                                                                                                                            Skill 2: recursive
    5    c = y * y + pow(y, 3);           // ... original code ...                                                           to iterative…
                                                                                            memcmp           assume                                 - if (strcmp(order, "II"))
    6    d = cstr[z];                                                                                                                ...            + int choice = sym_choice(0,2);
                                          Coverage Improved on P (+24%             )                   Generalize                                   + if (choice == 0) {
        Program P from Program Corpus                                                                                                               + sym_assume(order == "II");           Tests
                                                                                                                                                        return TIFF_ERR;
                                               pow can not be handled by the …                Name          Description                             + }
                                                                                                           Use when facing
                                            c = y * y + y * y * y;                           Memory                                                             libtiff/        Generate Inputs
                                                                                                             byte-by-byte
                                                                                            comparison                             Update:                       tif_info.c
                                                                                                            comparison …
                                          Coverage Unchanged on P (+0%             )                                               - Add          Persist        ...
                                                                                            bcmp      strcasecmp          ...      - Merge
  Symbolic                                                                                                                                                   Agentic
  Execution                                                        <code> ...                                                      - Remove
               Symbolic Execution Trace       <reasoning>…                                                                                                                make/        jq/ ...
   Engine                                                                                              New Skill                                            Transform                              .../



Figure 2: Overview of the Symbolon workflow. In the offline learning phase, Symbolon runs symbolic execution on simple
programs and uses evolutionary search to learn a diverse collection of transformations. These transformations are then
distilled into agent skills, which are further packaged into a reusable skill library for online inference to real-world programs.

    if(strcmp(x, cstr, ..
3. Methodology                      ...
                                                                                              constraints, solver queries, state-termination reasons, and cov-
                                                                                              erage. These events are mapped back to source locations,
     Figure 2 shows the workflow of Symbolon. The goal of                                     allowing Symbolon to identify code regions whose represen-
Symbolon is to learn source-level           program representations                           tation appearsif(memcmp(a,"test",5))
                                                                                                              to block exploration.{…
                                                                                                                                      For example, a byte-by-
                                     skill format …
that are more amenable to symbolic execution, while mea-                                      byte string comparison may create many short-lived states,
suring progress on the original program. This creates two                                     and a symbolic multiplication may later  skill_i.md
                                                                                                                                           produce expensive
            before                                                                            solver queries (Section 2.2).
practical challenges.   First, theafterspace of possible representa-
tions is large, e.g., useful transformations may summarize                                        Symbolon then asks an LLM agent to propose candidate
library checks, bound symbolic loops, rewrite arithmetic, in-                                 barriers from the program and trace. A barrier is a source-
sert assumptions, or remove exploration-irrelevant side effects.                              level explanation of why a code region is difficult for symbolic
Second, evaluating a transformation is expensive because                                      execution, not yet a trusted fact. Candidate barriers are ad-
it requires running symbolic execution on the transformed                                     mitted into the skill library only if the later transformation
program and replaying the generated tests on the original                                     search finds a rewrite whose generated tests improve replayed
program. Symbolon addresses these challenges with a two-                                      coverage on the original program. Importantly, the LLM
phase design. In the offline learning phase, it searches for                                  here only proposes hypotheses, while symbolic execution
useful transformations on small programs, where symbolic                                      and replay provide the evidence.
execution and replay are cheap, and distills successful transfor-                             Transformation search. For each candidate barrier 𝑏,
mations into a skill library T . In the repo-level transformation                             Symbolon searches for an alternative source-level representa-
phase (online inference), it uses T to adapt these learned                                    tion 𝑃b of 𝑃. A transformed program 𝑃   b is useful if symbolic
transformations to a target project 𝑃tgt , producing a selected                               execution on 𝑃  b generates tests that improve a target metric
transformed scaffold 𝑃sel . Symbolic execution is then run on                                 when replayed on the original program 𝑃. In this paper, the
𝑃sel , and the generated tests are replayed on 𝑃tgt to measure                                main metric is coverage, but the same formulation can opti-
progress on the original code.                                                                mize other replay-measurable objectives such as reachability
                                                                                              or bug-triggering behavior [88].
3.1. Offline Learning                                                                             This search space can often be too broad for simple
                                                                                              syntactic rewriting. The same barrier may require different
                                                                                              transformations depending on local context-sensitive features,
    The offline phase learns reusable transformation knowl-
                                                                                              e.g., types, constants, library calls, data dependencies, and
edge from small programs. Its input is a corpus of programs
                                                                                              program intent. As shown in Figure 1, for example, replacing
P, and its output is a skill library T [109]. Each skill records
                                                                                              a byte-order check with a representative valid case is only
a recurring symbolic-execution barrier, the source context
                                                                                              appropriate when the following code does not depend on the
in which it appears, and a transformation strategy that has
                                                                                              distinction between valid byte orders. Similarly, concretizing
been validated by replay on the original program. The phase
                                                                                              a loop bound requires understanding the input layout. Remov-
has three steps: profiling, transformation search, and skill
                                                                                              ing a diagnostic output is useful only when the output side
distillation (rule learning).
                                                                                              effect is irrelevant to the exploration target. Symbolon thus
Symbolic execution profiling. Given a program 𝑃 ∈ P,                                          uses an LLM-guided evolutionary search [103, 105, 124] to
Symbolon first runs symbolic execution on 𝑃 and collects                                      propose candidate representations.
a structured execution trace. The trace records source loca-                                      Each transformed program 𝑃    b is evaluated by transform-
tions reached by each state, branches that fork states, path                                  and-replay. Symbolon runs symbolic execution on 𝑃,    b replays



                                                                                        5
Algorithm 1 Offline learning of transformation skills                       running symbolic execution on 𝑃 b and replaying the generated
Require: Program corpus P, search budget 𝐾                                  tests on the original program 𝑃. It returns validated examples
Ensure: Skill library T                                                     (𝑃, 𝑃)
                                                                                 b whose replayed metric improves over 𝐶0 .
 1: T ← ∅
 2: for all 𝑃 ∈ P do
 3:     // Profile the original program.                                    3.2. Online Inference: Repo-Level Transformation
 4:     (E 𝑃 , 𝐶0 ) ← ProfileSE(𝑃)
 5:     if Saturated(𝐶0 ) then                                                  Given a target project 𝑃tgt , Symbolon uses the learned
 6:          continue
 7:     end if
                                                                            skill library T to produce a transformed project (scaffold)
 8:     // Infer candidate barriers from code and SE traces.                for symbolic execution. The agent is given the current source
 9:     B ← ProposeBarriers(𝑃, E 𝑃 )                                        tree, relevant skills retrieved based on its own judgment, and
10:     for all 𝑏 ∈ B do                                                    feedback from the previous valid iteration, including compiler
11:          // Search transformed representations and validate by          diagnostics, symbolic-execution traces, and replayed coverage
                replay on 𝑃.                                                reports. This makes the transformation context-sensitive in
12:          V𝑏 ← SearchTransforms(𝑃, 𝑏, 𝐶0 , 𝐾)                            two ways. First, the agent sees the local source context around
13:          if V𝑏 ≠ ∅ then                                                 each candidate edit, e.g., control flow, variable names, types,
14:               // Distill validated examples into reusable skills.
15:               T ← T ∪ CreateSkills(𝑏, V𝑏 )
                                                                            and comments. Second, the agent receives execution feedback
16:          end if                                                         that indicates which transformed regions helped or hindered
17:     end for                                                             exploration. Therefore, a skill is not applied as a fixed textual
18: end for                                                                 rewrite, but is instantiated according to the local program
19: return T                                                                representation.
                                                                                In each iteration, the agent retrieves skills whose ap-
                                                                            plicability conditions match the current code and proposes
the generated tests on the original program 𝑃, and computes                 localized source edits. Symbolon then validates the can-
the replayed metric on 𝑃. If the replayed metric improves                   didate in three steps. First, it checks that the transformed
over symbolic execution on 𝑃, Symbolon keeps (𝑃, 𝑃)     b as                project builds into LLVM bitcode. Second, it runs symbolic
a validated transformation example for barrier 𝑏. As the                    execution on the transformed bitcode. Third, it replays the
reward is measured on 𝑃, not on 𝑃,  b the search can include                generated tests on the original target project 𝑃tgt and measures
semantics-breaking transformations while avoiding rewards                   the replayed metric. If compilation fails, the candidate is
for transformations that only make 𝑃  b appear to be easier.                rejected, and the diagnostics are returned to the agent. If
                                                                            compilation succeeds, the candidate becomes a valid scaffold,
Rule learning. While validated transformation examples                      and Symbolon updates the selected output 𝑃sel only when
are useful in-context demonstrations for the agent, a single                the replayed metric improves. After at most 𝐾 iterations,
before/after pair is too specific to transfer directly to large             Symbolon returns 𝑃sel , the best validated scaffold observed
projects (Section 3.2). To this end, Symbolon generalizes                   under the transformation budget. The original project remains
validated examples into agent skills. For each barrier, the                 the measurement target throughout this process. The trans-
agent first synthesizes additional variants that express the                formed scaffold is used only to generate tests, while replay
same transformation idea under different local contexts. Each               on 𝑃tgt determines whether a transformation is useful. This
variant is validated with the same transform-and-replay met-                design filters invalid or unhelpful transfers from the offline
ric. Symbolon then groups retained examples by barrier se-                  skill library and keeps the optimization objective aligned
mantics and transformation strategy, deduplicates equivalent                with symbolic-execution progress on the original code.
groups, and converts each group into a skill.                                   Algorithm 2 summarizes this online inference step, which
     Specifically, a skill includes four components: the barrier            adapts learned agent skills for repo-level transformations.
description, the applicability context, the transformation pro-             Evaluate(𝑃,  b 𝑃) runs symbolic execution on 𝑃,    b replays the
cedure, and representative before/after examples with replay                generated tests on 𝑃, and returns both the replayed metric
evidence (Appendix G). For instance, a skill may describe                   and feedback artifacts such as traces, coverage reports, and
when a byte-by-byte comparison can be summarized into a                     diagnostics. In our evaluation, we use a fixed skill library
symbolic choice plus an assumption, together with examples                  learned offline. A natural extension is to promote validated
such as strcmp, memcmp, or project-specific wrapper functions.              target-specific transformations back into the library, but we
The resulting skill library T can be further updated, e.g., the             disable this online skill growth in our evaluation to keep
rule-learning LLM can add, merge, and remove rules when                     costs manageable (we discuss this extension in Section 6).
it iterates through the samples in P, mimicking a typical
training loop. Importantly, T is persistent and inspectable.
It transfers transformation knowledge from small programs                   4. Implementation
to large projects without updating model weights.
     Algorithm 1 abstracts the high-level steps. Search-                        We implement Symbolon in 2.1K LoC of Python, 3.5K
Transforms runs an LLM-guided evolutionary search. Each                     LoC of shell scripts, and 3.7K LoC of Nix. We use KLEE 3.2
candidate 𝑃 b is first checked for compilation, then evaluated by           as the default symbolic execution backend.


                                                                        6
Algorithm 2 Skill-guided repo-level transformation                             and the expected changes in symbolic execution traces af-
Require: Target project 𝑃tgt , skill library T , transformation budget         ter applying the transformation. The references/ directory
            𝐾                                                                  stores validated transformation examples collected during of-
Ensure: Selected transformed scaffold 𝑃sel                                     fline learning. On average, each skill contains 1.02 validated
 1: 𝑃cur ← 𝑃tgt , 𝑃sel ← 𝑃tgt                                                  transformation examples and 2.3 augmented applicability
 2: // Initial feedback and baseline metric are measured on the                patterns. During online inference, the agent can retrieve a
       original target.                                                        skill by recognizing a code pattern in the target program and
 3: (𝐹, 𝐶sel ) ← Evaluate(𝑃tgt , 𝑃tgt )
 4: for 𝑖 = 1 to 𝐾 do
                                                                               instantiate the corresponding transformation according to the
 5:      // Agent uses source context, learned skills, and prior feed-         surrounding program context.
            back.                                                              Agent settings. We implement the repo-level transformation
 6:      b ← AgentTransform(𝑃cur , T , 𝐹)
         𝑃
                                                                               agent as a Python program built on Claude Agent SDK 0.2.96.
 7:      if ¬Builds( 𝑃)b then
 8:          𝐹 ← Diagnostics( 𝑃)   b                                           The learned skills are mounted as a local read-only plugin, and
 9:          continue                                                          all skills are enabled during transformation. Given a target
10:      end if                                                                project, the agent proposes localized source edits, while an
11:      // Run SE on the scaffold, replay tests on the original target.       external harness performs compilation, symbolic execution,
12:      (𝐹, 𝐶) ← Evaluate( 𝑃,  b 𝑃tgt )                                       and replay for coverage measurement. To keep edits local,
13:      𝑃cur ← 𝑃 b                                                            each round may modify at most three files. After each round,
14:      if 𝐶 > 𝐶sel then                                                      the harness builds the transformed code, runs KLEE, collects
15:          𝑃sel ← 𝑃,
                     b 𝐶sel ← 𝐶                                                its run.istats trace and an llvm-cov coverage report, and
16:      end if                                                                returns these artifacts to the agent for the next round. The
17: end for
                                                                               agent runs in a sandbox with write access only to the target
18: return 𝑃sel
                                                                               codebase. Transformation references and skills are read-only,
                                                                               network access and sub-agent spawning are disabled, and
                                                                               only a small whitelist of tools is available: read tools (Read,
Offline transformation learning corpus. We construct                           Glob, Grep, Bash:sqlite3 for reading traces, and Bash:jq
the offline learning corpus from CodeContests [107], which                     for reading coverage reports) and write tools (Write, Edit,
contains millions of competitive-programming submissions.                      and MultiEdit). We guard symbolic-execution-only source
To obtain C programs, we compile submissions with gcc and                      edits with #ifdef KLEE_BITCODE, allowing the same source
keep those that compile successfully. This leads to 22,578                     tree to produce a transformed LLVM-bitcode build for KLEE
C programs. We remove near-duplicates, e.g., reformatted                       and an unmodified native build for replay-based coverage
variants or versions with renamed identifiers, using a Jaccard-                measurement.
similarity threshold of 0.85, leaving 15,879 programs. We
then sample one program per problem, producing a final
corpus of 2,416 programs with an average length of 50.5                        5. Evaluation
lines. Because these programs are small, we run KLEE on
each with a 30-second timeout and an 8 GB memory limit,                           To evaluate the effectiveness of Symbolon, we aim to
using the command-line configuration shown in Appendix A.                      answer the following research questions:
Transformation search. We instantiate the rule-learning                        RQ1: Effectiveness: How much does Symbolon help sym-
phase with OpenEvolve [124], which uses an LLM to propose                             bolic execution to improve code coverage with differ-
program variants and an external evaluator to select candidate                        ent search strategies?
transformed programs for refinement. The evaluator runs                        RQ2: Execution Efficiency: How does Symbolon affect
KLEE on the transformed program, replays the generated tests                          the runtime overhead of symbolic execution?
on the original program, and uses the resulting coverage as the                RQ3: Security Impact: How does Symbolon help find more
reward. For each program, we cap the search at 20 iterations                          real-world security violations and bugs?
and stop early once replayed tests reach 100% coverage on                      RQ4: Cost: What is the deployment cost of Symbolon?
the original program. Among the 2,416 programs, 1,567                          RQ5: Sensitivity: How much do different components of
reach 100% coverage within 14 iterations, suggesting that                             Symbolon contribute to its overall effectiveness?
many useful transformations are found within a small search
budget. We use Claude Sonnet 4.6 as the default model. The                     5.1. Experiment Setup
offline rule-learning cost averages $0.34 and 38.4K tokens
per program. This is distinct from the per-project deployment                  Benchmark. We evaluate Symbolon on 32 real-world open-
cost measured in Section 5.5.                                                  source programs widely used in previous symbolic execution
Skill library. The offline learning process produces a skill                   and fuzzing studies [112, 113, 115, 125, 126, 127], following
library with 211 skills after deduplication. Each skill is                     the same configurations when settings are available. As
stored as a directory that contains a SKILL.md file and a                      shown in Table 1, we use the latest release available for each
references/ directory. The SKILL.md file describes the code                    program at the time of our evaluation. The exact symbolic
pattern, why such a pattern impedes symbolic execution,                        environment supplied to each program, i.e., the concrete


                                                                           7
Table 1: Programs used to evaluate Symbolon. LoC is the                Table 2: Baseline search strategies used in our evaluation.
number of source lines reported by llvm-cov and serves as
the upper bound for line coverage.                                     Strategy         Prioritization
                                                                       bfs              Oldest live state, exploring shallow paths
 Program    Version      LoC     Program     Version      LoC          dfs              Most recently added state
 bash       5.3        55,638    bc          1.08.2       5,339        random-path      Random on execution tree, prefer deep states
 bison      3.8.2      29,108    cjpeg       3.1.4.1      8,642        random-state     Any live path with uniform probability
 cjson      1.7.19      2,298    combine     0.4.0        5,332        nurs:depth       Deeper states with higher probability
 curl       8.20.0     58,091    diff        3.12         8,898        nurs:covnew      Paths that recently discovered new coverage
 expat      2.8.0       9,711    find        4.10.0      15,930        nurs:cpicnt      States whose call-path is rarely taken
 flex       2.6.4       9,451    flvmeta     1.2.2        7,478        nurs:qc          States with cheap constraint-solving history
 gawk       5.4.0      41,246    grep        3.12        10,303        nurs:icnt        States at rarely-executed instructions
 gzip       1.14        4,074    jasper      4.2.9       22,124        nurs:md2u        Paths closest to uncovered CFG instructions
 jq         1.8.1      16,935    xmllint     2.15.3      88,109
                                                                       nurs:rp          Exponentially favors shallower states
 lua        5.4.7      14,883    make        4.4         14,070
 nasm       3.01       49,625    objcopy     2.46.0      97,417        cbc [114]        Reviving states near sensitive instructions
 openssl    4.0.0     283,323    patch       2.8         10,525        cgs [115]        Paths storing flip uncovered branches
 readelf    2.46.0     60,612    sed         4.10        13,852        empc [112]       Paths in minimum path cover of the CFG
 sqlite     3.53.1    116,524    strip-new   2.46.0      97,658        learch [113]     Highest-reward state from trained model
 tic        6.6        11,994    tiffinfo    4.7.1       19,725        sgs [116]        The least explored subpaths
 transicc   2.19       19,742    vim         9.2.0458   112,907



arguments and –sym-* options appended to each KLEE invo-               reduces the remaining symbolic-execution time, ensuring a
cation, is listed in Appendix B. We build all projects using           fair comparison with the baselines.
clang-16 and disable compiler optimization (-O0) to ensure             Environment. We run all evaluations on bare-metal x86-64
the generated bitcode is consistent with the original code             servers, each with two Intel Xeon Gold 6240R processors
implementation. Other build configurations include flags               and 192 GB RAM, running Ubuntu 24.04.4 LTS [128]. Each
minimizing dependence on external libraries.                           evaluation instance runs in an isolated container limited to
Baselines. We evaluate Symbolon across a broad set of                  one CPU core and 40 GB memory. We use Z3 [129] as the
established search strategies to assess whether Symbolon-              SMT backend and cap KLEE at 32 GB memory, leaving the
transformed programs are generally amenable to symbolic                remaining container memory for the solver, runtime libraries,
execution, rather than merely tailored to particular strategies.       and OS overhead. All runs use the same fixed KLEE con-
Specifically, we include all 11 built-in search strategies in          figuration, including POSIX/uClibc runtime support, query
KLEE, together with five additional representative works from          logging, coverage output, and a watchdog (see the full com-
recent years, summarized in Table 2. All experiments are built         mand line in Appendix A). To reduce resource interference,
on KLEE 3.2 [3]. Empc [112] runs with the original settings,           we run at most four evaluation instances concurrently on
including the bipartite-matching cap and analyzer thread-              each server and disable other background workloads.
pool configuration. CGS [115] requires a branch-dependency
pre-pass, which we apply to the bitcode before running it              5.2. Coverage Improvement
with the default target-branch selection settings. We evaluate
Learch [113] with its shipped feedforward network under                    Figure 3 summarizes the coverage improvement of
greedy state selection, which matches their reported best-             Symbolon across 32 programs and 16 search strategies.
performing configuration. SGS [116] interleaves four subpath-          Symbolon substantially improves replayed line coverage on
guided searchers with subpath lengths fixed to 1/2/4/8 over            the original programs. The average improvement is 3.69×
each state’s most recently taken branches. For CBC [114],              and 3.87× when coverage is aggregated by programs and
we use its default settings for the bounded-DFS exploration            search strategies, respectively. The gains are especially vis-
depth around sensitive instructions.                                   ible in hard cases where the baseline makes no progress.
Metrics. We use line coverage as the primary metric fol-               For 69 program–strategy pairs with zero baseline coverage,
lowing prior work [3, 5, 112], considering that Symbolon               Symbolon covers at least one line, and for 68 of these pairs,
transforms the program before symbolic execution, making               it covers at least 1,000 lines.
KLEE’s internal bitcode coverage not representative of the                 The gains hold across most benchmark programs. For
coverage on the original source code. We thus report external          each program, we compute the improvement ratio by sum-
coverage: after KLEE generates tests on either the original            ming the covered lines over all 16 search strategies with
or transformed code, we replay those tests on a separately             Symbolon and dividing by the corresponding baseline sum.
instrumented native build of the original program and mea-             Symbolon improves coverage on 30 of the 32 programs,
sure line coverage with llvm-cov. The coverage is measured             with at least 1.5× improvement on 25 programs. On 19 pro-
over 10 independent runs with a 12-hour end-to-end budget.             grams, Symbolon covers more lines than the baseline under
For Symbolon, this budget includes repo-level transformation           every evaluated search strategy. The largest program-level
and validation time, so any time spent by the agent directly           improvement is 22.75× on lua. We leave the discussion of


                                                                   8
+ Symbolon
   Baseline
                 dfs       bfs       random-state random-path nurs:covnew   nurs:md2u     nurs:depth   nurs:rp     nurs:icnt      nurs:cpicnt      nurs:qc         sgs         cgs            cbc           empc              learch
              (1.69×)   (1.90×)         (6.56×)     (2.62×)     (5.54×)      (6.41×)       (7.51×)     (2.08×)     (5.37×)         (3.20×)         (5.32×)       (6.88×)     (1.89×)        (1.70×)        (1.68×)           (1.56×)

      bash 1.66×                  bc 13.47×               bison 7.97×                   cjpeg 1.04×              cjson 0.95×                    combine 1.84×                 curl 2.17×                        diff 3.12×




     expat 3.52×                  find 3.20×               flex 4.04×               flvmeta 2.06×                gawk 2.10×                      grep 1.72×                   gzip 1.16×                   jasper 6.47×




       jq 3.76×              xmllint 6.66×                 lua 22.75×                   make 2.67×               nasm 0.96×                     objcopy 3.41×               openssl 2.08×                   patch 1.25×




     readelf 1.44×                sed 2.10×               sqlite 3.68×             strip-new 1.44×                tic 2.36×                     tiffinfo 2.66×              transicc 1.77×                  vim 2.66×




Figure 3: Per-program line coverage across 16 search strategies after 12 hours. Each subplot shows one program. Bars
follow the legend order. For each bar, the dark segment represents baseline coverage, and the light segment represents
additional coverage obtained from Symbolon under the same strategy. The ratio in each subplot title is Symbolon’s average
improvement on that program across all strategies, while the ratio below each legend entry is the average improvement of
that strategy across all programs. Each subplot uses an independent 𝑦-axis. Very small or visually similar baseline bars, e.g.,
lua and flex, reflect low or similar baseline coverage at this scale.

                                                                                                                    + Symbolon
why Symbolon does not improve cjson or nasm to Section 6,                                                              Baseline
though it still improves a subset of search strategies.                                                                              vanilla        -O2          -sccp     -ipsccp     -gvn_hoist      -sroa          -adce
                                                                                                                                    (3.39×)       (3.77×)       (3.21×)    (3.69×)      (3.44×)       (3.34×)        (3.77×)

    Symbolon also improves coverage across all search strate-                                                                                    jasper 5.28×                        make 1.75×
gies. As some programs have zero baseline coverage, im-
provement ratios for baselines on these programs are unde-
fined. Therefore, for each strategy, we report an aggregate
improvement ratio, computed as the total number of lines
covered by Symbolon across all 32 programs divided by                                                        Figure 4: Line coverage of Symbolon under different
the corresponding total baseline coverage. The improvement                                                   compiler-optimization flags. Each bar is one flag (color);
ranges from 1.56× to 7.51×, with a mean of 3.87×. No-                                                        the solid base is the baseline coverage with that flag and the
tably, Symbolon also reduces the dependence on the choice                                                    lighter cap is the additional lines Symbolon covers. Titles
of search strategy. On the original programs, the strongest                                                  report the per-program improvement ratio.
strategy covers 7.4× as many lines as the weakest one. After
applying Symbolon, this gap drops to 1.7×. This suggests
that Symbolon makes the transformed programs easier to                                                       that Symbolon can further augment rigid compiler transfor-
explore across a wide range of search strategies, rather than                                                mations, which are strictly semantics-preserving and often
only benefiting a particular strategy.                                                                       misaligned with the objective of symbolic execution.

Improving compiler optimizations. Beyond improving                                                           5.3. Execution Efficiency
search strategies, we show that Symbolon also complements
existing transformation-based approaches, e.g., compiler op-                                                     Symbolic execution can stop making progress when the
timizations [81]. Specifically, for a program compiled with                                                  state set or solver workload exhausts the analysis budget. We
a compiler optimization flag deemed effective by prior                                                       thus evaluate whether Symbolon makes programs cheaper to
work [81], we further transform it with Symbolon and com-                                                    explore. For each program, we report peak resident memory
pare the resulting coverage improvement against that on the                                                  and average solver time per query, averaged across all 16
original program. As shown in Figure 4, Symbolon con-                                                        search strategies. As shown in Table 3, Symbolon reduces
sistently improves coverage across all compiler-flag config-                                                 peak memory on 28 of 32 programs and average solver time
urations by 3.52× on average. This observation validates                                                     per query on 29 of 32 programs. The mean per-program


                                                                                                        9
Table 3: Runtime overhead of symbolically executing the                       Table 4: Unique security violations found in original pro-
original (Vanilla) versus the Symbolon-transformed program,                   grams. Tests are generated on original (Vanilla) versus
for peak resident memory and average solving time per                         Symbolon-transformed programs. Δ is the absolute gain
query. The reduction factor Ratio column is computed as                       achieved by Symbolon.
Vanilla/Symbolon (a ratio >1 means Symbolon costs less
                                                                                                  UBSan Violations              ASan Violations
and higher is better); the last row reports arithmetic means                   Strategy
across programs.                                                                              Vanilla   Symbolon      Δ    Vanilla   Symbolon      Δ
                                                                               bfs                26          47     +21        5           5      0
                Peak Memory (MB)            Avg. Solving Time (ms)             dfs                13          24     +11        2           1     -1
 Program                                                                       random-path        21          43     +22        3           5     +2
             Vanilla   Symbolon   Ratio   Vanilla    Symbolon    Ratio         random-state       14          19      +5        6           9     +3
 bash        29,998      14,215    2.1      5,543         983     5.6          nurs:depth         16          26     +10        0           1     +1
 bc          19,353         260   74.3      1,739          5.7    307          nurs:covnew        17          42     +25        2           5     +3
 bison        7,751       1,028    7.5     16,601           90    184          nurs:cpicnt        24          39     +15        3           2     -1
 cjpeg       19,279      16,362    1.2     41,427      13,703     3.0          nurs:qc            14          19      +5        2           1     -1
 cjson       26,845      24,189    1.1        282         260     1.1          nurs:icnt          15          24      +9        0           3     +3
 combine     26,902         405   66.4         43           14    3.2          nurs:md2u          18          31     +13        2           4     +2
 curl        17,719         292   60.6        318          2.4    133          nurs:rp            29          45     +16        3           8     +5
 diff        14,116       1,727    8.2     18,854         212    88.9          cbc                20          31     +11        4           7     +3
 expat       15,625         305   51.3      4,577           26    178          cgs                32          44     +12        6          10     +4
 find        22,211         616   36.1        486           36   13.5          empc               37          67     +30        9           9      0
 flex            96         186   0.52         1.5         5.8   0.25          learch             29          62     +33        6           7     +1
 flvmeta     25,644         336   76.4      2,855           46   61.6          sgs                 8          10      +2        1           2     +1
 gawk        23,464      25,194   0.93      6,232           16    384          Total             333         573   +240        54          79     +25
 grep        13,194      11,683    1.1     35,440       8,836     4.0
 gzip         1,142         994    1.1    192,424       4,211    45.7
 jasper      19,174         205   93.6        343          2.3    149
 jq          22,203         283   78.5         27       1,195    0.02         and openssl. These savings show that Symbolon improves
 xmllint     17,604         444   39.7      5,011           31    159
 lua         11,354       5,981    1.9        215       1,918    0.11         exploration not only by reaching more code, but also by
 make        23,199      19,377    1.2      6,289       1,189     5.3         making transformed programs cheaper for both the engine
 nasm        22,011      26,941   0.82     10,405           87    120         and the solver to process.
 objcopy     18,916       1,726   11.0      8,196       4,824     1.7
 openssl     16,969       2,309    7.3     12,396           36    342
 patch       32,094      28,756    1.1        659         570     1.2         5.4. Finding Bugs
 readelf        649         271    2.4     53,188         166     321
 sed         26,368      26,734   0.99        408         249     1.6
 sqlite      26,356         768   34.3      4,975           13    397             We evaluate the ability of Symbolon to help discover real-
 strip-new   18,891         462   40.8      8,079           42    193
 tic         25,562         308   82.9        348        0.99     351
                                                                              world security violations. Specifically, we apply Symbolon to
 tiffinfo    14,884         326   45.6        725          6.5    111         (1) directly find security violations in user-space programs,
 transicc    25,815         317   81.4      2,821           18    155         and (2) generate syscall descriptions using SyzSpec [20] for
 vim         19,094         881   21.7    143,495         624     230
                                                                              the Linux kernel to assist kernel fuzzing.
 Average     18,890       6,684   29.2     18,263       1,232     123
                                                                              Finding security violations with sanitizers. We first use
                                                                              KLEE and Symbolon to detect memory-safety bugs and un-
reduction factors are 29.2× for peak memory and 123× for                      defined behaviors in the same set of programs. This leverages
solver time per query.                                                        KLEE’s built-in memory error detector and its integration
                                                                              with the Undefined Behavior Sanitizer (UBSan). Since the
Memory. Symbolon reduces memory by removing or com-                           program is transformed by Symbolon, sanitizer reports ob-
pressing sources of state growth before the engine reaches                    tained from the transformed program do not necessarily
them, e.g., summarizing byte-by-byte checks, bounding sym-                    indicate violations in the original program. Following similar
bolic loops, and bypassing exploration-irrelevant I/O. The                    practices in prior work [112, 115], we build the original
arithmetic mean peak memory drops from 18,890 MB to                           program with UBSan and Address Sanitizer (ASan), replay
6,684 MB, while the median transformed peak memory is                         the tests generated by KLEE/Symbolon on it, and count the
only 824 MB. Moreover, 18 transformed programs run un-                        unique security violations reported by each sanitizer.
der 1 GB. The largest reductions exceed 70× on memory-                            As Table 4 shows, across 16 search strategies, Symbolon
bound programs such as jasper, tic, and bc, indicating                        reports 240 more UBSan violations and 25 more ASan viola-
that Symbolon substantially reduces the live state space that                 tions than running KLEE on the original programs. We have
KLEE must keep resident.                                                      manually validated these sanitizer reports and have respon-
                                                                              sibly disclosed confirmed issues that present real security
Constraint solving time. Symbolon also reduces solver-
                                                                              risks to the respective maintainers.
side cost by changing the expressions that enter solver queries,
e.g., concretizing symbolic sizes or bounds and rewriting                     Finding crashes by generating syscall descriptions. Sym-
solver-hostile computations. The arithmetic mean solver time                  bolic execution can support kernel fuzzing by generating
per query drops from 18,263 ms to 1,232 ms, and the mean                      syscall descriptions that help construct valid syscall inputs.
per-program reduction factor is 123×. The largest reductions                  For example, SyzSpec [20] symbolically analyzes kernel
exceed 300× on query-bound programs such as sqlite, gawk,                     syscall handlers and extracts input types, sizes, and constraints


                                                                         10
Table 5: 24-hour syzkaller fuzzing results using syscall                              Table 7: Per-program deployment cost of Symbolon: wall-
descriptions generated by running SyzSpec on the original                             clock time, token usage, and dollar cost of applying the
kernel (Vanilla) and on the Symbolon-transformed kernel.                              distilled skill library with default model configuration.
                                 Edge Coverage                   Crashes                           Time    #Tok.   Cost               Time    #Tok.   Cost
 Kernel Target                                                                         Program     (min)     (M)    ($)    Program    (min)     (M)    ($)
                      Vanilla      Symbolon      Ratio    Vanilla    Symbolon
                                                                                       bash         17.5    7.72   11.39   bc          20.6    9.41   14.52
 i2c                    1,621          1,743      1.08       2               2         bison        17.8    7.83   12.46   cjpeg       25.5    4.34    8.22
 infiniband               714          1,831      2.56       0               1         cjson        14.0    6.06   10.96   combine     17.9    7.77   14.23
 input_event            1,940          1,798      0.93       1               1         curl         18.5    8.16   11.46   diff        25.4    7.41   13.94
 io_uring               1,708          2,727      1.60       1               1         expat        20.3    6.64   11.11   find        26.8    7.02   11.34
 mapper_control         1,185         26,234     22.14       1               4         flex         22.6    6.33   11.89   flvmeta     24.0    5.71   10.10
 ppp                    3,878          3,022      0.78       1               2         gawk         23.8    7.74   11.57   grep        18.5    6.98   11.29
 ptmx                   1,846          5,055      2.74       1               3         gzip         21.6    5.09   10.13   jasper      25.9    7.32   14.62
 sg                     3,044          2,844      0.93       4               1         jq           21.6    5.23   13.94   tiffinfo    20.7    6.38   12.29
 snd_seq                1,620          2,108      1.30       0               1         xmllint      17.8    4.07    8.98   lua         18.8    3.95    8.40
 uinput                 2,767          2,898      1.05       1               2         make         19.3    5.19   11.18   nasm        24.7    6.41   10.22
                                                                                       objcopy      22.0    5.12   11.81   openssl     19.4    8.15   11.66
 Total                20,323          50,260      2.47      12           18            patch        19.5    5.71   11.95   readelf     21.8    7.46   12.94
                                                                                       sed          24.4    4.61    7.84   sqlite      24.8    5.64   10.73
Table 6: New linux kernel bugs discovered by Symbolon.                                 strip-new    23.5    5.26   10.75   tic         21.4    8.61   13.92
                                                                                       transicc     22.6    5.92   12.15   vim         23.2    5.98   12.51
File: enclosing source file (kernel-relative). Function: enclos-
ing kernel function.                                                                   Average     21.44    6.41   11.58   -              -       -       -

 File                              Function                          Type
 jfs/jfs_imap.c                    diRead                            NPD              improves edge coverage on 7 of 10 targets, with the largest
 net/socket.c                      kernel_sock_shutdown              NPD              gain on mapper_control. The generated descriptions also
 vidtv/vidtv_psi.c                 vidtv_psi_ts_psi...1              NPD              increase the total number of unique crashes from 12 to 18,
 jfs/file.c                        jfs_open                          OOB              improving crash discovery on 6 of 10 targets. These results
 jfs/jfs_txnmgr.c                  txAbort                           Assertion
                                                                                      show that transforming the symbolic-analysis target can help
 ipv4/udp_tunnel_nic.c             udp_tunnel_nic_device...2         UAF
 gfs2/rgrp.c                       read_rindex_entry                 WARN             SyzSpec recover more useful syscall descriptions and translate
 hfsplus/super.c                   hfsplus_commit_superblock         Hang             into better kernel-fuzzing outcomes on the original kernel.
 events/core.c                     perf_event_release_kernel         Hang                 We further run an extended continuous fuzzing campaign
 ipv4/ip_input.c                   ip_rcv                            RCU stall        beyond the 24-hour comparison. This campaign uncovers 21
 mm/memfd.c                        memfd_create                      RCU stall
 fs/stat.c                         newfstat                          RCU stall        previously unknown Linux kernel bugs that were not reported
 fs/stat.c                         newlstat                          RCU stall        by syzbot at the time of discovery. As shown in Table 6,
 fs/fcntl.c                        sys_fcntl                         RCU stall        these bugs include use-after-free, out-of-bounds access, null-
 events/core.c                     perf_fasync                       RCU stall        pointer dereference, hang, and RCU-stall cases. At the time
 events/core.c                     perf_release                      RCU stall
 block/blk-mq.c                    blk_mq_free_rqs                   OOB
                                                                                      of writing, we have responsibly reported all identified bugs to
 v4l2-core/v4l2-dev.c              v4l2_open                         UAF              the relevant maintainers and have suggested potential patches
 module/main.c                     try_module_get                    OOB              to help the fixing process. Among these bugs, two of them
 jfs/jfs_logmgr.c                  lbmIODone                         UAF              have been acknowledged by the maintainers and one bug has
 dvb-core/dvbdev.c                 dvb_device_put                    UAF
 1 vidtv_psi_ts_psi_write_into           2 udp_tunnel_nic_device_sync_work
                                                                                      been forwarded to the public mail list for discussion. We
                                                                                      continue to actively monitor the status of these reports and
                                                                                      will provide update for each bug.
for syzkaller. However, native kernel code is difficult for                           Case studies. Figure 5 shows two representative bugs ex-
symbolic execution to analyze, so we use Symbolon as a                                posed by Symbolon-generated tests. In flvmeta, Symbolon
front end to SyzSpec. We run SyzSpec on both the original                             enables KLEE to reach yaml_on_tag, where a 64-bit tag offset
kernel and the Symbolon-transformed kernel, generate syscall                          is printed with sprintf into a 20-byte stack buffer. The gener-
descriptions from each, and then fuzz the unmodified original                         ated input makes the decimal offset require 21 bytes including
kernel with syzkaller. Following SyzSpec’s setup, we target                           the null terminator, triggering a one-byte ASan-reported
the same Linux drivers and subsystems that remain available                           stack overflow. In the Linux JFS case, Symbolon helps
in our evaluated kernel version, excluding capi20 because it                          SyzSpec recover syscall descriptions that guide syzkaller
has been removed. Each target is fuzzed for 24 hours over                             to jfs_open, where an on-disk extent descriptor is decoded
three runs, using four CPU cores split across two QEMU                                into an unchecked allocation-group index and used to access
instances. We report average final KCOV edge coverage and                             db_active[MAXAG].
the number of unique crashes.
    Table 5 shows that descriptions generated from the                                5.5. Deployment Cost
Symbolon-transformed kernel improve end-to-end fuzzing
effectiveness. Across all targets, aggregate edge coverage                                 Symbolon incurs a recurring per-project cost before sym-
increases from 20,323 to 50,260, a 2.47× improvement over                             bolic execution, i.e., the agent retrieves learned skills, instan-
descriptions generated from the original kernel. Symbolon                             tiates local rewrites, and validates candidate transformations.


                                                                                 11
   1 static int yaml_on_tag(flv_tag *tag, flv_parser *parser) {                     1 static int jfs_open(struct inode *inode, struct file *file) {
   2      char buffer[20];   /* 20-byte stack buffer */                             2      struct jfs_inode_info *ji     = JFS_IP(inode);
   3      /* ... */                                                                 3      struct jfs_sb_info    *jfs_sb = JFS_SBI(inode->i_sb);
   4      /* current_tag_offset is a 64-bit file offset taken straight              4      /* ... */
   5       * from the parsed stream with no bound. A crafted FLV makes its          5      /* BLKTOAG decodes an on-disk PXD with no validation that
   6       * unsigned-decimal form need 21 bytes (20 digits + NUL). */              6       * the result falls inside db_active[MAXAG = 128]. A crafted
   7      sprintf(buffer, "%" FILE_OFFSET_PRINTF_FORMAT "u",                        7       * inode forces a negative index. */
   8        FILE_OFFSET_PRINTF_TYPE(parser->stream->current_tag_offset));           8      ji->active_ag = BLKTOAG(addressPXD(&ji->ixpxd), jfs_sb);
   9      /* ^^ ASAN: stack-buffer-overflow, WRITE of size 21 into                  9      atomic_inc(&jfs_sb->bmap->db_active[ji->active_ag]);
         ,→ buffer[20] ^^ */                                                       10      /* ^^ UBSAN: index = -128, size 128 ^^ */
  10 }                                                                             11 }



(a) A buffer overflow bug in yaml_on_tag: a 64-bit tag offset is              (b) An out-of-bounds access in jfs_open: BLKTOAG decodes an
printed with sprintf into a 20-byte stack buffer, but a crafted FLV           on-disk PXD without validating that the result indexes within
forces an offset whose 20-digit decimal form needs 21 bytes, writing          db_active[MAXAG], so a crafted inode forces a negative index and
one past buffer[20].                                                          an out-of-bounds atomic increment.
Figure 5: Two representative bugs exposed by Symbolon-generated tests and missed by the evaluated baselines under the
same budget. (a) An ASan-reported stack overflow in flvmeta. (b) An out-of-bounds access in Linux JFS that can corrupt
kernel memory or trigger a crash.


Table 7 reports this deployment cost for applying the dis-                        Table 8: Sensitivity analysis of Symbolon to different set-
tilled skill library, excluding the one-time offline rule-learning                tings. Agent and Models: different agent setting for the online
phase. Across the 32 programs, deployment takes 21.44 min-                        inference in Symbolon. Skill Library: different settings for
utes, consumes 6.41M tokens, and costs $11.58 on average.                         integrating the skill library to the agent. LCov is averaged line
We charge this time to Symbolon under the same 12-hour end-                       coverage across 32 benchmark programs with nurs:covnew
to-end budget used by the baselines. On average, deployment                       search strategy; Δ is the relative change compared to the full
consumes only 3.0% of the budget, leaving the remaining                           Symbolon (top row).
time for symbolic exploration. The worst-case time is 26.8
                                                                                        Configuration                                      LCov       Δ (%)
minutes on find, and the highest cost is $14.62 on jasper.
As the transformed source is produced before symbolic ex-                         Symbolon (default)
ecution and is independent of the engine configuration, it                            Claude Code + Claude Opus 4.6                        5,336      —
can be reused across repeated campaigns, different budgets,                       Agent and Models
and, in our evaluation, all 16 search strategies. Therefore,                           Claude Code + Claude Sonnet 4.6                     4,427      -17.0
the recurring deployment overhead remains reasonably small                             Codex + GPT 5.5 high effort                         6,590      +23.5
relative to the symbolic execution campaigns it accelerates,                           Codex + GPT 5.3-Codex high effort                   4,892      -8.3
while the more expensive open-ended transformation rule
                                                                                  Skill Library
discovery is amortized through offline one-time skill learning.
                                                                                     w/o Pattern Augmentation                              2,951      -44.7
                                                                                     w/o Transformation                                    1,468      -72.5
5.6. Sensitivity Analysis                                                            w/o Barrier Description                               1,163      -78.2

    We further study how Symbolon behaves under different
implementation choices and deployment settings. Specifically,                     runtime, while stronger backends can further improve repo-
we vary the agent and LLM backend, ablate components of                           level transformation.
the learned skill library, and test whether the same high-level                   Skill library. We next ablate the skill library to understand
workflow transfers to other symbolic execution engines and                        which learned information is most useful during repo-level
programming languages.                                                            transformation. Removing pattern augmentation reduces aver-
Agent and LLM backends. We first vary the agent and                               age line coverage by 44.7%, showing that additional trigger
model used during repo-level transformation while keeping                         patterns help the agent recognize transformation opportunities
the learned skill library fixed. As shown in Table 8, Symbolon                    across diverse target contexts. Removing concrete before-and-
remains effective across different backends, while their final                    after transformation examples causes a larger drop of 72.5%,
coverage depends on model and agent quality. Replacing                            indicating that examples are critical for turning a barrier
the default Claude Code + Claude Opus 4.6 with Claude                             diagnosis into an actionable rewrite. Removing the barrier
Sonnet 4.6 reduces average line coverage by 17.0%, suggest-                       description reduces coverage by 78.2%, the largest degrada-
ing that stronger reasoning and code capability help adapt                        tion among the ablations. This suggests that effective skill
learned transformations to target programs. Using Codex                           transfer requires both what to transform and why the code
with GPT 5.5 in high-effort mode improves coverage by                             impedes symbolic execution. Syntactic patterns or examples
23.5% over the default, while GPT 5.3-Codex performs 8.3%                         alone are insufficient for context-sensitive transformation.
below the default but remains competitive. These results                          Generalization to other languages. Symbolon operates
show that Symbolon is not tied to a single LLM or agent                           at the source level and does not depend on specific inter-


                                                                             12
Table 9: Generalization of Symbolon across symbolic-                    transformation types and applies each type a handful of times
execution engines and source languages. We report aggregate             per program (Table 12). One potential explanation can be the
line coverage over each engine’s benchmark projects. Δ: rel-            limited types of program in our evaluation. Most evaluated
ative gain of Symbolon over running the engine alone.                   programs are file or command-line parsers, whose symbolic-
                                                                        execution challenges arise from a small set of recurring
                                            Line Coverage
Engine      Language        #Projects                                   patterns, such as input-parsing loops. In contrast, on the
                                        Vanilla Symbolon Δ (%)          logic-bomb benchmark designed for symbolic execution [79],
Owi            Rust            2           171       312     +82        Symbolon resolves a broader range of challenges using more
CrossHair      Python          2           141       393    +178        diverse and more intricate transformations (Table 14). An-
ExpoSE         JavaScript      2         1,079     1,464     +35        other factor might be the limited inference budget allocated to
                                                                        the agent, as we reserve most of the fixed end-to-end budget
Total                          6         1,391     2,169    +56
                                                                        for symbolic execution. That said, note that even under this
                                                                        constrained setting, the resulting transformations produce
                                                                        nontrivial coverage gains (Section 5.2). The restricted budget
mediate representations, solver APIs, or search policies. To
                                                                        prevents the agent from discovering additional or more di-
test this generalizability, we integrate Symbolon with three
                                                                        verse transformations that could further improve exploration.
additional symbolic execution engines, i.e., Owi [130] for
                                                                        Appendix E provides preliminary evidence that allocating
Rust, CrossHair [131, 132] for Python, and ExpoSE [46]
                                                                        a larger inference budget to the agent can result in further
for JavaScript. As these engines expose different execution
                                                                        coverage gains. Future work could develop adaptive allocation
interfaces, we keep the experiment lightweight. Specifically,
                                                                        policies that decide whether the next unit of budget is bet-
Symbolon starts from the existing learned skill library and
                                                                        ter spent searching for another transformation or continuing
performs repo-level transformation, without engine-specific
                                                                        symbolic execution.
rule learning. We evaluate two projects per language using
each engine’s default configuration, under the same 12-hour             Learning–deployment gap. Symbolon learns transforma-
budget for both the baseline and the transformed program.               tion skills from small benchmark programs because reward
Each configuration is repeated three times, and coverage                evaluation is cheap in that setting. While our evaluation shows
is measured by replaying generated inputs on the original               that these skills transfer to larger real-world projects, a gap can
program. The evaluated projects and versions are listed in              remain between offline-learning programs and deployment
Appendix C.                                                             targets. Real projects often include domain-specific APIs,
    Table 9 summarizes the results. Symbolon improves cov-              macros, and long-range dependencies that may not appear
erage for all three engines, with gains of 82% for Owi, 178%            in small coding benchmarks. As a result, some real-world
for CrossHair, and 35% for ExpoSE. The coverage increases               barriers may not be covered by our learned skill library, and
by 56% across the six projects. These results are not intended          some learned rules may need to be substantially adapted
as a full benchmark for non-C engines, but they provide                 before becoming useful. Future work could reduce this gap
evidence that the source-level transformation workflow can              by learning from broader or domain-specific corpora, main-
transfer beyond the default C/KLEE setting with minimal                 taining project-specific skill libraries, or developing cheaper
engine-specific engineering.                                            proxy rewards for transformation search.

6. Discussion                                                           7. Related Work
Cost of agentic transformation. Symbolon amortizes open-                Optimizations for symbolic execution. A large body of
ended rule discovery by learning transformations offline on             work improves symbolic execution by optimizing the engine,
small programs, but applying learned skills to a new reposi-            solver, or exploration policy. Existing approaches employ
tory still incurs a repo-level transformation cost. The agent           search strategies and learned state-selection policies to prior-
must locate candidate contexts, instantiate rules, validate             itize promising program states [22, 112, 113, 114, 116], and
transformed code, and run symbolic execution and replay a               leverage pruning, slicing, memoization, and under-constrained
few times before the main campaign. In our evaluation, we               execution to reduce the program region to explore or reuse
charge this repo-level transformation and validation time to            prior reasoning [24, 133, 134, 135]. Solver-aware techniques
Symbolon by reducing its remaining symbolic-execution bud-              use concrete executions, constraint simplification, or spe-
get, so Symbolon and the baselines are compared under the               cialized reasoning to reduce query cost [6, 80, 115]. Other
same end-to-end budget (Section 5.1). However, this setting             systems improve symbolic execution engines for specific
still does not rule out the possibility that a promising initial        deployment settings, such as hybrid fuzzing, binary analysis,
transformation fails to translate into improved performance             firmware analysis, and long-running campaigns [40, 55, 57, 65,
over a longer campaign, in which case the transformation                111, 126], leveraging domain-specific optimization opportu-
overhead can outweigh the eventual coverage gain.                       nities. Recent ML/LLM-assisted symbolic execution further
Limited transformations applied. We observe that in                     optimizes the analysis loop to generate tests, interpret or
practice, the applied transformations per project are rare.             solve path constraints, complete structured inputs, summarize
Across our benchmark programs, the agent uses only a few                constraints, or guide vulnerability discovery [23, 117, 118,


                                                                   13
119, 136, 137, 138, 139, 140]. Symbolon complements these              target aligned with the goal of symbolic execution, while
approaches by changing the source representation before                allowing a broad transformation space. Our evaluation across
these approaches take place, while staying disentangled from           32 real-world C programs and 16 search strategies shows
all optimizations during symbolic execution.                           consistent improvements in coverage, with substantially re-
Program transformation for symbolic execution. A com-                  duced overhead in symbolic execution. Symbolon also finds
plementary direction reduces symbolic execution cost by                new security violations in these programs, as well as Linux
enriching the program representation (via compilation and              kernel bugs when used to augment state-of-the-art kernel
transformation) exposed to the symbolic execution engine [5,           bug finders based on symbolic execution.
74]. As program analyses are known to be sensitive to
code transformations [83, 84, 85, 86, 87, 88, 141], existing           Acknowledgments
approaches have also exploited this to improve symbolic
execution [80, 81, 90, 91, 92, 93, 94, 95, 96, 97]. However,               This research is in part based upon work supported by
their transformation spaces are usually fixed by compiler              Coefficient Giving and by credits supported through Ama-
passes or narrow expert-written templates tied to specific             zon Nova AI Challenge: Trusted Software Agents. Results
program constructs. Symbolon builds on a similar insight               presented in this paper were obtained using the Chameleon
but treats transformation discovery as a learning problem. It          testbed supported by the National Science Foundation. Any
automatically searches for diverse transformation rules from           opinions, findings, and conclusions or recommendations ex-
symbolic execution feedback, stores them as persistent agent           pressed in this material are those of the author(s) and do
skills, and instantiates them across diverse contexts in the           not necessarily reflect the views of the sponsors. Language
project to optimize symbolic execution.                                model assistants were used to help polish the paper.
LLM-guided code evolution. Recent work has shown that
LLMs can serve not only as code generators but also as                 References
proposal mechanisms in efficient search over programs, algo-
rithms, and agentic systems [103, 104, 105, 142, 143]. For
                                                                       [1]    J. C. King, “Symbolic execution and program testing,” Commun.
example, AlphaEvolve and ADRS use evolutionary coding-                        ACM, vol. 19, no. 7, p. 385–394, 1976.
agent loops to find state-of-the-art algorithms and system ar-
                                                                       [2]    C. Cadar, P. Godefroid, S. Khurshid, C. S. Păsăreanu, K. Sen, N. Till-
chitectures that human experts have missed for decades [105,                  mann, and W. Visser, “Symbolic execution for software testing in
106]. These approaches suggest a new form of learning in                      practice: preliminary assessment,” in Proceedings of the 33rd Inter-
which knowledge is accumulated through code and agent                         national Conference on Software Engineering, 2011, pp. 1066–1071.
memory/skills, rather than solely through updates to model             [3]    C. Cadar, D. Dunbar, and D. R. Engler, “KLEE: Unassisted and
weights. Symbolon follows a similar spirit, but differs in both               automatic generation of high-coverage tests for complex systems
the optimization target and the deployment model. Rather                      programs,” in Proceedings of the 8th USENIX Symposium on Op-
than evolving the program to improve its own performance,                     erating Systems Design and Implementation (OSDI’08). USENIX
                                                                              Association, 2008, pp. 209–224.
Symbolon evolves program representations that improve how
symbolic execution reasons about them. Moreover, Symbolon              [4]    V. Chipounov, V. Kuznetsov, and G. Candea, “S2e: A platform for
does not run expensive evolution on every large repository.                   in-vivo multi-path analysis of software systems,” in Proceedings of
                                                                              the sixteenth international conference on Architectural support for
It performs cheap transformation discovery offline on small                   programming languages and operating systems. ACM, 2011.
programs, and transfers the learned knowledge via persistent
                                                                       [5]    S. Poeplau and A. Francillon, “Symbolic execution with SYMCC:
agent skills [108, 109] to repo-level transformations. There-                 don’t interpret, compile!” in Proceedings of the 29th USENIX Con-
fore, Symbolon suggests a broader future direction for evolu-                 ference on Security Symposium. USENIX Association, 2020, pp.
tionary search when reward computation is expensive, making                   181–198.
it promising to extend program representation learning to              [6]    E. Coppa, D. C. D’Elia, and C. Demetrescu, “Rethinking pointer rea-
other code reasoning tasks, e.g., fuzzing, formal verification,               soning in symbolic execution,” in Proceedings of the 32nd IEEE/ACM
and agentic software analysis.                                                International Conference on Automated Software Engineering (ASE).
                                                                              IEEE, 2017, pp. 613–618.

8. Conclusion                                                          [7]    M. H. Schwerhoff, “Advancing automated, permission-based pro-
                                                                              gram verification using symbolic execution,” Ph.D. dissertation, ETH
                                                                              Zurich, 2016.
    This paper introduces Symbolon, a framework that learns
source-level program transformations to improve symbolic               [8]    Y. Hu, G. Huang, and P. Huang, “Automated reasoning and detection
                                                                              of specious configuration in large systems with symbolic execution,”
execution. Rather than relying on fixed compiler optimiza-                    in Proceedings of the 14th USENIX Symposium on Operating Systems
tions or hand-written rewrite rules, Symbolon automatically                   Design and Implementation (OSDI 20), 2020, pp. 719–734.
searches for program representations amenable to symbolic
                                                                       [9]    D. Kuts, “Towards symbolic pointers reasoning in dynamic symbolic
execution, validates them by replaying the tests on the orig-                 execution,” in 2021 Ivannikov Memorial Workshop (IVMEM). IEEE,
inal program, and learns transformation rules as persistent                   2021, pp. 42–49.
agent skills for agentic, repo-level transformation on pop-            [10]   L. Borzacchiello, M. Cornacchia, D. Maiorca, G. Giacinto, and
ular real-world software projects. By measuring progress                      E. Coppa, “Droidreach++: Exploring the reachability of native code
on the original program, Symbolon keeps the optimization                      in android applications,” Computers & Security, p. 104657, 2025.



                                                                  14
[11]   P. Godefroid, N. Klarlund, and K. Sen, “Dart: Directed automated               [28]   Z. Zhang, Y. Hao, W. Chen, X. Zou, X. Li, H. Li, Y. Zhai, and B. Lau,
       random testing,” in Proceedings of the 2005 ACM SIGPLAN confer-                       “Symbisect: Accurate bisection for fuzzer-exposed vulnerabilities,” in
       ence on Programming language design and implementation, 2005,                         33rd USENIX Security Symposium (USENIX Security 24), 2024, pp.
       pp. 213–223.                                                                          2493–2510.
[12]   S. Person, G. Yang, N. Rungta, and S. Khurshid, “Directed incremental          [29]   X. Shao, Z. Ling, Y. Zhang, H. Yan, Y. Wei, L. Luo, Z. Liu, J. Luo,
       symbolic execution,” in Proceedings of the 32nd ACM SIGPLAN                           and X. Fu, “The cost of performance: Breaking threadx with kernel
       Conference on Programming Language Design and Implementation,                         object masquerading attacks,” in 34th USENIX Security Symposium
       2011, pp. 504–515.                                                                    (USENIX Security 25), 2025, pp. 7507–7524.
[13]   S. Y. Chau, M. Yahyazadeh, O. Chowdhury, A. Kate, and N. Li,                   [30]   M. Alharthi, F. Sang, D. Kuvaiskii, M. Vij, and T. Kim, “Rakis:
       “Analyzing semantic correctness with symbolic execution: A case                       Secure fast i/o primitives across trust boundaries on intel sgx,” in
       study on pkcs# 1 v1. 5 signature verification,” in Network and                        Proceedings of the Twentieth European Conference on Computer
       Distributed Systems Security (NDSS) Symposium 2019, 2019.                             Systems, 2025, pp. 1177–1193.
                                                                                      [31]   K. Man, Z. Wang, Y. Hao, S. Zheng, X. Zhou, Y. Cao, and Z. Qian,
[14]   V. Kuznetsov, J. Kinder, S. Bucur, and G. Candea, “Efficient state                    “Scad: Towards a universal and automated network side-channel vul-
       merging in symbolic execution,” in Proceedings of the 33rd ACM                        nerability detection,” in 2025 IEEE Symposium on Security and
       SIGPLAN Conference on Programming Language Design and Im-                             Privacy (SP). IEEE, 2025, pp. 1861–1876.
       plementation, 2012, pp. 193–204.
                                                                                      [32]   Y. Ding, A. Gervais, R. Wattenhofer, and H. Sato, “Hunting defi
[15]   Z. Susag, S. Lahiri, J. Hsu, and S. Roy, “Symbolic execution for                      vulnerabilities via context-sensitive concolic verification,” in Pro-
       randomized programs,” Proceedings of the ACM on Programming                           ceedings of the 2024 IEEE/ACM 46th International Conference on
       Languages, vol. 6, no. OOPSLA2, pp. 1583–1612, 2022.                                  Software Engineering: Companion Proceedings, 2024, pp. 324–325.
[16]   R. Baldoni, E. Coppa, D. C. D’Elia, and C. Demetrescu, “Assisting              [33]   P. Godefroid, M. Y. Levin, and D. Molnar, “Sage: whitebox fuzzing
       malware analysis with symbolic execution: A case study,” in Inter-                    for security testing,” Commun. ACM, vol. 55, no. 3, p. 40–44, 2012.
       national conference on cyber security cryptography and machine                 [34]   E. Bounimova, P. Godefroid, and D. Molnar, “Billions and billions of
       learning. Springer, 2017, pp. 171–188.                                                constraints: whitebox fuzz testing in production,” in Proceedings of
[17]   N. Stephens, J. Grosen, C. Salls, A. Dutcher, R. Wang, J. Corbetta,                   the 2013 International Conference on Software Engineering. IEEE
       Y. Shoshitaishvili, C. Kruegel, and G. Vigna, “Driller: Augmenting                    Press, 2013, p. 122–131.
       fuzzing through selective symbolic execution.” in NDSS, vol. 16, no.           [35]   N. Tillmann and J. De Halleux, “Pex: white box test generation for
       2016, 2016, pp. 1–16.                                                                 .net,” in Proceedings of the 2nd International Conference on Tests
[18]   Y. Chen, P. Li, J. Xu, S. Guo, R. Zhou, Y. Zhang, T. Wei, and L. Lu,                  and Proofs. Springer-Verlag, 2008, p. 134–153.
       “Savior: Towards bug-driven hybrid testing,” in 2020 IEEE Symposium            [36]   N. Tillmann, J. de Halleux, and T. Xie, “Transferring an automated
       on Security and Privacy (SP). IEEE, 2020, pp. 1580–1596.                              test generation tool to practice: from pex to fakes and code digger,”
                                                                                             in Proceedings of the 29th ACM/IEEE International Conference
[19]   H. Huang, P. Yao, R. Wu, Q. Shi, and C. Zhang, “Pangolin: Incre-
                                                                                             on Automated Software Engineering. Association for Computing
       mental hybrid fuzzing with polyhedral path abstraction,” in 2020
                                                                                             Machinery, 2014, p. 385–396.
       IEEE Symposium on Security and Privacy (SP). IEEE, 2020, pp.
       1613–1627.                                                                     [37]   P. Godefroid, “Higher-order test generation,” SIGPLAN Not., vol. 46,
                                                                                             no. 6, p. 258–269, 2011.
[20]   Y. Hao, J. Pu, X. Li, Z. Qian, and A. A. Sani, “SyzSpec: specification
       generation for linux kernel fuzzing via under-constrained symbolic             [38]   N. Redini, A. Machiry, D. Das, Y. Fratantonio, A. Bianchi,
       execution,” in Proceedings of the 2025 ACM SIGSAC Conference on                       E. Gustafson, Y. Shoshitaishvili, C. Kruegel, and G. Vigna, “Boot-
       Computer and Communications Security. Association for Computing                       stomp: On the security of bootloaders in mobile devices,” in 26th
       Machinery, 2025, pp. 813–826.                                                         USENIX Security Symposium (USENIX Security 17), 2017, pp. 781–
                                                                                             798.
[21]   Y. Ling, G. Rajiv, K. Gopinathan, and I. Sergey, “Sound and effi-
                                                                                      [39]   H. Sun, Y. Shen, J. Liu, Y. Xu, and Y. Jiang, “{KSG}: Augmenting
       cient generation of data-oriented exploits via programming language
                                                                                             kernel fuzzing with system call specification generation,” in 2022
       synthesis,” in 34th USENIX Security Symposium (USENIX Security
                                                                                             USENIX Annual Technical Conference (USENIX ATC 22), 2022, pp.
       25), 2025, pp. 413–429.
                                                                                             351–366.
[22]   N. Ruaro, K. Zeng, L. Dresel, M. Polino, T. Bao, A. Continella,                [40]   R. David, S. Bardin, T. D. Ta, L. Mounier, J. Feist, M.-L. Potet, and
       S. Zanero, C. Kruegel, and G. Vigna, “Syml: Guiding symbolic                          J.-Y. Marion, “Binsec/se: A dynamic symbolic execution toolkit for
       execution toward vulnerable states through pattern learning,” in Pro-                 binary-level analysis,” in 2016 IEEE 23rd International Conference
       ceedings of the 24th International Symposium on Research in Attacks,                  on Software Analysis, Evolution, and Reengineering (SANER), vol. 1.
       Intrusions and Defenses, 2021, pp. 456–468.                                           IEEE, 2016, pp. 653–656.
[23]   M. Shafiuzzaman, A. Desai, W. Guo, and T. Bultan, “Guiding sym-                [41]   J. Liu, L. Yi, W. Chen, C. Song, Z. Qian, and Q. Yi, “Linkrid:
       bolic execution with static analysis and llms for vulnerability discov-               Vetting imbalance reference counting in linux kernel with symbolic
       ery,” arXiv preprint arXiv:2604.06506, 2026.                                          execution,” in 31st USENIX Security Symposium (USENIX Security
[24]   D. A. Ramos and D. Engler, “Under-constrained symbolic execu-                         22), 2022, pp. 125–142.
       tion: Correctness checking for real code,” in 24th USENIX Security             [42]   H. Han, J. Kyea, Y. Jin, J. Kang, B. Pak, and I. Yun, “Queryx:
       Symposium (USENIX Security 15), 2015, pp. 49–64.                                      Symbolic query on decompiled code for finding bugs in cots binaries,”
                                                                                             in 2023 IEEE Symposium on Security and Privacy (SP). IEEE,
[25]   F. Brown, D. Stefan, and D. Engler, “Sys: A static/symbolic tool for                  2023, pp. 3279–3295.
       finding good bugs in good (browser) code,” in 29th USENIX Security
       Symposium (USENIX Security 20), 2020, pp. 199–216.                             [43]   K. Kim, T. Kim, E. Warraich, B. Lee, K. R. Butler, A. Bianchi, and
                                                                                             D. J. Tian, “Fuzzusb: Hybrid stateful fuzzing of usb gadget stacks,”
[26]   Y. Wang, C. Zhang, Z. Zhao, B. Zhang, X. Gong, and W. Zou,                            in 2022 IEEE Symposium on Security and Privacy (SP). IEEE,
       “Maze: Towards automated heap feng shui,” in 30th USENIX security                     2022, pp. 2212–2229.
       symposium (USENIX security 21), 2021, pp. 1647–1664.
                                                                                      [44]   G. Li, E. Andreasen, and I. Ghosh, “Symjs: Automatic symbolic
[27]   K. Huang, Y. Huang, M. Payer, Z. Qian, J. Sampson, G. Tan, and                        testing of javascript web applications,” in Proceedings of the 22nd
       T. Jaeger, “The taming of the stack: Isolating stack data from memory                 ACM SIGSOFT International Symposium on Foundations of Software
       errors,” in NDSS, 2022.                                                               Engineering, 2014, pp. 449–459.



                                                                                 15
[45]   F. Marques, M. Ferreira, A. Nascimento, M. E. Coimbra, N. Santos,                [62]   J. Zaddach, L. Bruno, A. Francillon, D. Balzarotti et al., “Avatar:
       L. Jia, and J. Fragoso Santos, “Automated exploit generation for node.                  A framework to support dynamic security analysis of embedded
       js packages,” Proceedings of the ACM on Programming Languages,                          systems’ firmwares.” in NDSS, vol. 14, no. 2014, 2014, pp. 1–16.
       vol. 9, no. PLDI, pp. 1341–1366, 2025.
                                                                                        [63]   D. Davidson, B. Moench, T. Ristenpart, and S. Jha, “Fie on firmware:
[46]   B. Loring, D. Mitchell, and J. Kinder, “ExpoSE: Practical symbolic                      Finding vulnerabilities in embedded systems using symbolic execu-
       execution of standalone javascript,” in Proceedings of the 24th ACM                     tion,” in 22nd USENIX Security Symposium (USENIX Security 13),
       SIGSOFT International SPIN Symposium on Model Checking of                               2013, pp. 463–478.
       Software, 2017, pp. 196–199.                                                     [64]   T. Scharnowski, N. Bars, M. Schloegel, E. Gustafson, M. Muench,
[47]   L. Borzacchiello, E. Coppa, D. Maiorca, A. Columbu, C. Demetrescu,                      G. Vigna, C. Kruegel, T. Holz, and A. Abbasi, “Fuzzware: Using pre-
       and G. Giacinto, “Reach me if you can: On native vulnerability                          cise mmio modeling for effective firmware fuzzing,” in 31st USENIX
       reachability in android apps,” in European Symposium on Research                        Security Symposium (USENIX Security 22), 2022, pp. 1239–1256.
       in Computer Security. Springer, 2022, pp. 701–722.                               [65]   C. Liu, A. Mera, E. Kirda, M. Xu, and L. Lu, “Co3: concolic
[48]   Z. Liu, T. Lee, J. Yu, Z. Kang, and Y. Cao, “The domino effect: De-                     co-execution for firmware,” in 33rd USENIX Security Symposium
       tecting and exploiting dom clobbering gadgets via concolic execution                    (USENIX Security 24), 2024, pp. 5591–5608.
       with symbolic dom,” in 34th USENIX Security Symposium (USENIX                    [66]   H. Kim, M. O. Ozmen, Z. B. Celik, A. Bianchi, and D. Xu, “Patchverif:
       Security 25), 2025, pp. 8293–8312.                                                      Discovering faulty patches in robotic vehicles,” in 32nd USENIX
[49]   X. Huang, L. Zhang, Y. Liu, P. Deng, Y. Cao, Y. Zhang, and M. Yang,                     Security Symposium (USENIX Security 23), 2023, pp. 3011–3028.
       “Towards automatic detection and exploitation of java web applica-               [67]   C. S. Păsăreanu and N. Rungta, “Symbolic pathfinder: symbolic
       tion vulnerabilities via concolic execution guided by cross-thread                      execution of java bytecode,” in Proceedings of the 25th IEEE/ACM
       object manipulation,” in 34th USENIX Security Symposium (USENIX                         International Conference on Automated Software Engineering, 2010,
       Security 25), 2025, pp. 8367–8384.                                                      pp. 179–180.
[50]   S. Artzi, A. Kiezun, J. Dolby, F. Tip, D. Dig, A. Paradkar, and M. D.            [68]   G. Yang, S. Person, N. Rungta, and S. Khurshid, “Directed incremental
       Ernst, “Finding bugs in dynamic web applications,” in Proceedings of                    symbolic execution,” ACM Trans. Softw. Eng. Methodol., vol. 24,
       the 2008 international symposium on Software testing and analysis,                      no. 1, 2014.
       2008, pp. 261–272.
                                                                                        [69]   K. Luckow, C. S. Păsăreanu, M. B. Dwyer, A. Filieri, and W. Visser,
[51]   S. Artzi, J. Dolby, F. Tip, and M. Pistoia, “Directed test generation for               “Exact and approximate probabilistic symbolic execution for nondeter-
       effective fault localization,” in Proceedings of the 19th International                 ministic programs,” in Proceedings of the 29th ACM/IEEE Interna-
       Symposium on Software Testing and Analysis. Association for                             tional Conference on Automated Software Engineering. Association
       Computing Machinery, 2010, p. 49–60.                                                    for Computing Machinery, 2014, p. 575–586.
[52]   J. F. Santos, P. Maksimović, T. Grohens, J. Dolby, and P. Gardner,               [70]   E. Kurian, D. Briola, P. Braione, and G. Denaro, “Automatically gen-
       “Symbolic execution for javascript,” in Proceedings of the 20th In-                     erating test cases for safety-critical software via symbolic execution,”
       ternational Symposium on Principles and Practice of Declarative                         Journal of Systems and Software, vol. 199, p. 111629, 2023.
       Programming. Association for Computing Machinery, 2018.
                                                                                        [71]   T. Kim, A. Ding, S. Etigowni, P. Sun, J. Chen, L. Garcia, S. Zonouz,
[53]   N. Mirzaei, S. Malek, C. S. Păsăreanu, N. Esfahani, and R. Mahmood,                     D. Xu, and D. Tian, “Reverse engineering and retrofitting robotic
       “Testing android apps through symbolic execution,” ACM SIGSOFT                          aerial vehicle control firmware using dispatch,” in Proceedings of
       Software Engineering Notes, vol. 37, no. 6, pp. 1–5, 2012.                              the 20th Annual International Conference on Mobile Systems, Appli-
[54]   S. Poeplau and A. Francillon, “Symqemu: Compilation-based sym-                          cations and Services, 2022, pp. 69–83.
       bolic execution for binaries,” in Ndss 2021, network and distributed             [72]   C. Cadar and K. Sen, “Symbolic execution for software testing: Three
       system security symposium. Internet Society, 2021.                                      decades later,” Commun. ACM, vol. 56, no. 2, pp. 82–90, 2013.
[55]   F. Wang and Y. Shoshitaishvili, “Angr-the next generation of binary              [73]   R. Baldoni, E. Coppa, D. C. D’elia, C. Demetrescu, and I. Finocchi,
       analysis,” in 2017 IEEE Cybersecurity Development (SecDev). IEEE,                       “A survey of symbolic execution techniques,” ACM Comput. Surv.,
       2017, pp. 8–9.                                                                          vol. 51, no. 3, pp. 50:1–50:39, 2018.
[56]   S. K. Cha, T. Avgerinos, A. Rebert, and D. Brumley, “Unleashing                  [74]   G. Wei, S. Jia, R. Gao, H. Deng, S. Tan, O. Bračevac, and T. Rompf,
       mayhem on binary code,” in 2012 IEEE Symposium on Security and                          “Compiling parallel symbolic execution with continuations,” in 2023
       Privacy. IEEE, 2012, pp. 380–394.                                                       IEEE/ACM 45th International Conference on Software Engineering
[57]   Z. Qi, J. Hu, Z. Xiao, and H. Yin, “Symfit: Making the common                           (ICSE). IEEE, 2023, pp. 1316–1328.
       (concrete) case fast for binary-code concolic execution,” in 33rd                [75]   S. Bucur, V. Ureche, C. Zamfir, and G. Candea, “Parallel symbolic
       USENIX Security Symposium (USENIX Security 24), 2024, pp. 415–                          execution for automated real-world software testing,” in Proceedings
       432.                                                                                    of the sixth conference on Computer systems, 2011, pp. 183–198.
[58]   L.-A. Daniel, S. Bardin, and T. Rezk, “Binsec/rel: Efficient relational          [76]   X. Xiao, S. Li, T. Xie, and N. Tillmann, “Characteristic studies of
       symbolic execution for constant-time at binary-level,” in 2020 IEEE                     loop problems for structural test generation via symbolic execution,”
       Symposium on Security and Privacy (SP). IEEE, 2020, pp. 1021–                           in 2013 28th IEEE/ACM International Conference on Automated
       1038.                                                                                   Software Engineering (ASE). IEEE, 2013, pp. 246–256.
[59]   V. Chipounov, V. Georgescu, C. Zamfir, and G. Candea, “Selective                 [77]   A. Fromherz, K. S. Luckow, and C. S. Păsăreanu, “Symbolic arrays
       symbolic execution,” in Workshop on Hot Topics in Dependable                            in symbolic pathfinder,” ACM SIGSOFT Software Engineering Notes,
       Systems, vol. 559559, 2009.                                                             vol. 41, no. 6, pp. 1–5, 2017.
[60]   C. Cebeci, Y. Zou, D. Zhou, G. Candea, and C. Pit-Claudel, “Practical            [78]   L. Borzacchiello, E. Coppa, D. Cono D’Elia, and C. Demetrescu,
       verification of system-software components written in standard c,”                      “Memory models in symbolic execution: key ideas and new thoughts,”
       in Proceedings of the ACM SIGOPS 30th Symposium on Operating                            Software Testing, Verification and Reliability, vol. 29, no. 8, p. e1722,
       Systems Principles, 2024, pp. 455–472.                                                  2019.
[61]   R. Iyer, K. Argyraki, and G. Candea, “Automatically reasoning about              [79]   H. Xu, Z. Zhao, Y. Zhou, and M. R. Lyu, “Benchmarking the capability
       how systems code uses the cpu cache,” in 18th USENIX Symposium                          of symbolic execution tools with logic bombs,” IEEE Transactions
       on Operating Systems Design and Implementation (OSDI 24), 2024,                         on Dependable and Secure Computing, vol. 17, no. 6, pp. 1243–1256,
       pp. 581–598.                                                                            2020.



                                                                                   16
[80]   J. Chen, W. Hu, L. Zhang, D. Hao, S. Khurshid, and L. Zhang,                  [97]   H. Converse, O. Olivo, and S. Khurshid, “Non-semantics-preserving
       “Learning to accelerate symbolic execution via code transformation,”                 transformations for higher-coverage test generation using symbolic
       in 32nd European Conference on Object-Oriented Programming                           execution,” in 2017 IEEE International Conference on Software
       (ECOOP 2018). Schloss Dagstuhl–Leibniz-Zentrum für Informatik,                       Testing, Verification and Validation (ICST). IEEE, 2017, pp. 241–
       2018, pp. 6–1.                                                                       252.
[81]   Y. Zhang, M. Sirlanci, R. Wang, and Z. Lin, “When compiler optimiza-          [98]   D. Trabish and S. Itzhaky, “Enhancing symbolic execution with
       tions meet symbolic execution: An empirical study,” in Proceedings                   machine-checked safety proofs,” in Proceedings of the 15th ACM
       of the 2024 on ACM SIGSAC Conference on Computer and Commu-                          SIGPLAN International Conference on Certified Programs and Proofs,
       nications Security, 2024, pp. 4212–4225.                                             2026, pp. 294–308.
[82]   G. Wei, O. Bračevac, S. Tan, and T. Rompf, “Compiling symbolic                [99]   N. He, Z. Zhao, J. Wang, Y. Hu, S. Guo, H. Wang, G. Liang, D. Li,
       execution with staging and algebraic effects,” Proceedings of the                    X. Chen, and Y. Guo, “Eunomia: Enabling user-specified fine-grained
       ACM on Programming Languages, vol. 4, no. OOPSLA, pp. 1–33,                          search in symbolically executing webassembly binaries,” in Proceed-
       2020.                                                                                ings of the 32nd ACM SIGSOFT International Symposium on Software
                                                                                            Testing and Analysis, 2023, pp. 385–397.
[83]   R. van Tonder and C. Le Goues, “Tailoring programs for static analysis
                                                                                     [100] J. Crawford, M. Ginsberg, E. Luks, and A. Roy, “Symmetry-breaking
       via program transformation,” in Proceedings of the ACM/IEEE 42nd
                                                                                           predicates for search problems,” KR, vol. 96, no. 1996, pp. 148–159,
       International Conference on Software Engineering, 2020, pp. 824–
                                                                                           1996.
       834.
                                                                                     [101] I. P. Gent and B. Smith, Symmetry breaking during search in con-
[84]   K. S. Namjoshi and Z. Pavlinovic, “The impact of program transfor-                  straint programming. University of Leeds, School of Computer
       mations on static program analysis,” in International Static Analysis               Studies Leeds, 1999.
       Symposium. Springer, 2018, pp. 306–325.
                                                                                     [102] Klee, “Klee intrinsics,” Intrinsics, 2023.
[85]   J. Jung, H. Hu, D. Solodukhin, D. Pagan, K. H. Lee, and T. Kim,
       “Fuzzification:anti-fuzzing techniques,” in 28th USENIX Security              [103] B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P.
       Symposium (USENIX Security 19), 2019, pp. 1913–1930.                                Kumar, E. Dupont, F. J. Ruiz, J. S. Ellenberg, P. Wang, O. Fawzi
                                                                                           et al., “Mathematical discoveries from program search with large
[86]   H. Peng, Y. Shoshitaishvili, and M. Payer, “T-fuzz: fuzzing by program              language models,” Nature, vol. 625, no. 7995, pp. 468–475, 2024.
       transformation,” in 2018 IEEE Symposium on Security and Privacy
                                                                                     [104] K. Sen, “Kiss sorcar: A stupidly-simple general-purpose and software
       (SP). IEEE, 2018, pp. 697–710.
                                                                                           engineering ai assistant,” arXiv preprint arXiv:2604.23822, 2026.
[87]   E. Güler, C. Aschermann, A. Abbasi, and T. Holz, “Antifuzz: impeding          [105] A. Novikov, N. Vũ, M. Eisenberger, E. Dupont, P.-S. Huang, A. Z.
       fuzzing audits of binary executables,” in 28th USENIX Security                      Wagner, S. Shirobokov, B. Kozlovskii, F. J. Ruiz, A. Mehrabian et al.,
       Symposium (USENIX Security 19), 2019, pp. 1931–1947.                                “Alphaevolve: A coding agent for scientific and algorithmic discovery,”
[88]   J. Zhu, C. Shen, Z. Li, J. Yu, Y. Chen, and K. Pei, “Locus: Agen-                   arXiv preprint arXiv:2506.13131, 2025.
       tic predicate synthesis for directed fuzzing,” in Proceedings of the          [106] A. Cheng, S. Liu, M. Pan, Z. Li, B. Wang, A. Krentsel, T. Xia,
       ACM/IEEE 48nd International Conference on Software Engineering.                     M. Cemri, J. Park, S. Yang et al., “Barbarians at the gate: How ai is
       Association for Computing Machinery, 2026.                                          upending systems research,” arXiv preprint arXiv:2510.06189, 2025.
[89]   H. Zhang, Y. Pei, J. Chen, and S. H. Tan, “Statfier: Automated testing        [107] Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond,
       of static analyzers via semantic-preserving program transformations,”               T. Eccles, J. Keeling, F. Gimeno, A. D. Lago, T. Hubert, P. Choy,
       in Proceedings of the 31st ACM Joint European Software Engi-                        C. de Masson d’Autume, I. Babuschkin, X. Chen, P.-S. Huang,
       neering Conference and Symposium on the Foundations of Software                     J. Welbl, S. Gowal, A. Cherepanov, J. Molloy, D. J. Mankowitz, E. S.
       Engineering, 2023, pp. 237–249.                                                     Robson, P. Kohli, N. de Freitas, K. Kavukcuoglu, and O. Vinyals,
                                                                                           “Competition-level code generation with alphacode,” Science, vol.
[90]   S. Dong, O. Olivo, L. Zhang, and S. Khurshid, “Studying the influ-
                                                                                           378, no. 6624, pp. 1092–1097, 2022.
       ence of standard compiler optimizations on symbolic execution,” in
       2015 IEEE 26th International Symposium on Software Reliability                [108] R. Xu and Y. Yan, “Agent skills for large language models: Archi-
       Engineering (ISSRE). IEEE, 2015, pp. 205–215.                                       tecture, acquisition, security, and the path forward,” arXiv preprint
                                                                                           arXiv:2602.12430, 2026.
[91]   C. Cadar, “Targeted program transformations for symbolic execution,”
       in Proceedings of the 2015 10th Joint Meeting on Foundations of               [109] Anthropic, “Equipping agents for the real world with
       Software Engineering, 2015, pp. 906–909.                                            agent      skills,”        https://www.anthropic.com/engineering/
                                                                                           equipping-agents-for-the-real-world-with-agent-skills, 2025.
[92]   C. Saumya, M. Hassan, R. Gangaraju, M. Kulkarni, and K. Sun-
       dararajah, “Taming the hydra: Targeted control-flow transformations           [110] J. Chen, W. Han, M. Yin, H. Zeng, C. Song, B. Lee, H. Yin, and
       for dynamic symbolic execution,” Proceedings of the ACM on Pro-                     I. Shin, “Symsan: Time and space efficient concolic execution via
       gramming Languages, vol. 10, no. OOPSLA1, pp. 59–85, 2026.                          dynamic data-flow analysis,” in 31st USENIX Security Symposium
                                                                                           (USENIX Security 22), 2022, pp. 2531–2548.
[93]   K. Zhu, C. Guo, K. Yan, X. Jia, H. Du, Q. Huang, Y. Xie, and
                                                                                     [111] I. Yun, S. Lee, M. Xu, Y. Jang, and T. Kim, “Qsym: A practical con-
       J. Tang, “Loopscc: Towards summarizing multi-branch loops within
                                                                                           colic execution engine tailored for hybrid fuzzing,” in 27th USENIX
       determinate cycles,” arXiv preprint arXiv:2411.02863, 2024.
                                                                                           Security Symposium (USENIX Security 18), 2018, pp. 745–761.
[94]   D. S. Bouras and S. Mechtaev, “Defusing logic bombs in sym-                   [112] S. Yao and D. She, “Empc: effective path prioritization for symbolic
       bolic execution with llm-generated ghost code,” arXiv preprint                      execution with path cover,” in 2025 IEEE Symposium on Security
       arXiv:2603.19239, 2026.                                                             and Privacy (SP). IEEE Computer Society, 2025, pp. 2772–2790.
[95]   D. M. Perry, A. Mattavelli, X. Zhang, and C. Cadar, “Accelerating             [113] J. He, G. Sivanrupan, P. Tsankov, and M. Vechev, “Learning to
       array constraints in symbolic execution,” in Proceedings of the 26th                explore paths for symbolic execution,” in Proceedings of the 2021
       ACM SIGSOFT International Symposium on Software Testing and                         ACM SIGSAC Conference on Computer and Communications Security.
       Analysis, 2017, pp. 68–78.                                                          ACM, 2021, pp. 2526–2540.
[96]   E. T. Barr, D. Clark, M. Harman, and A. Marginean, “Indexing                  [114] Q. Yi, Y. Yu, and G. Yang, “Compatible branch coverage driven
       operators to extend the reach of symbolic execution,” arXiv preprint                symbolic execution for efficient bug finding,” in Proc. ACM Program.
       arXiv:1806.10235, 2018.                                                             Lang., vol. 8, no. PLDI, 2024, pp. 213:1633–213:1655.



                                                                                17
[115] Y. Sun, G. Yang, S. Lv, Z. Li, and L. Sun, “Concrete constraint              [134] D. Trabish, A. Mattavelli, N. Rinetzky, and C. Cadar, “Chopped sym-
      guided symbolic execution,” in Proceedings of the IEEE/ACM 46th                    bolic execution,” in Proceedings of the 40th International Conference
      International Conference on Software Engineering. ACM, 2024, pp.                   on Software Engineering, 2018, pp. 350–360.
      1–12.
                                                                                   [135] G. Yang, C. S. Păsăreanu, and S. Khurshid, “Memoized symbolic
[116] Y. Li, Z. Su, L. Wang, and X. Li, “Steering symbolic execution to                  execution,” in Proceedings of the 2012 International Symposium on
      less traveled paths,” in Proceedings of the 2013 ACM SIGPLAN                       Software Testing and Analysis, 2012, pp. 144–154.
      international conference on Object oriented programming systems
                                                                                   [136] J. Xu, J. Xu, T. Chen, and X. Ma, “Symbolic execution with test
      languages & applications. ACM, 2013, pp. 19–32.
                                                                                         cases generated by large language models,” in 2024 IEEE 24th
[117] H. Tu, S. Lee, Y. Li, P. Chen, L. Jiang, and M. Böhme, “ Cottontail:               International Conference on Software Quality, Reliability and Security
      Large Language Model-Driven Concolic Execution for Highly Struc-                   (QRS). IEEE, 2024, pp. 228–237.
      tured Test Input Generation ,” in 2026 IEEE Symposium on Security
      and Privacy (SP). IEEE Computer Society, 2026, pp. 2047–2065.                [137] S. Cha and H. Oh, “Making symbolic execution promising by learning
                                                                                         aggressive state-pruning strategy,” in Proceedings of the 28th ACM
[118] Z. Luo, H. Zhao, D. Wolff, C. Cadar, and A. Roychoudhury, “Agentic                 Joint Meeting on European Software Engineering Conference and
      Concolic Execution,” in 2026 IEEE Symposium on Security and                        Symposium on the Foundations of Software Engineering, 2020, pp.
      Privacy (SP). IEEE Computer Society, 2026, pp. 1–19.                               147–158.
[119] Y. Li, R. Meng, and G. J. Duck, “Large language model powered                [138] Y. Wu, X. Zhou, A. Humayun, M. A. Gulzar, and M. Kim, “Generating
      symbolic execution,” Proceedings of the ACM on Programming                         and understanding tests via path-aware symbolic execution with llms,”
      Languages, vol. 9, no. OOPSLA2, pp. 3148–3176, 2025.                               arXiv preprint arXiv:2506.19287, 2025.
[120] Google, “syzkaller: an unsupervised coverage-guided kernel fuzzer,”          [139] S. Xia, M. He, S. Shao, T. Yu, Y. Zhang, N. Yoshida, and L. Song,
      https://github.com/google/syzkaller, 2024.                                         “SymGPT: Auditing smart contracts via combining symbolic execu-
[121] libsdl-org, “libtiff,” https://github.com/libsdl-org/libtiff, n.d.                 tion with large language models,” in Proc. ACM Program. Lang.,
                                                                                         vol. 10, no. OOPSLA1. Association for Computing Machinery,
[122] L. De Moura and N. Bjørner, “Z3: An efficient smt solver,” in
                                                                                         2026.
      International conference on Tools and Algorithms for the Construction
      and Analysis of Systems. Springer, 2008, pp. 337–340.                        [140] Y. Yang, S. Yao, J. Chen, and W. Lee, “Hybrid language processor
[123] C. Gomes and M. Sellmann, “Streamlined constraint reasoning,” in                   fuzzing via llm-based constraint solving,” in Proceedings of the 34th
      International Conference on Principles and Practice of Constraint                  USENIX Conference on Security Symposium. USENIX Association,
      Programming. Springer, 2004, pp. 274–289.                                          2025.
[124] A. Sharma, “Openevolve: an open-source evolutionary coding agent,”           [141] Z. Luo, M. Zafar, D. Wolff, and A. Roychoudhury, “Code-augur:
      2025.                                                                              Agentic vulnerability detection via specification inference,” arXiv
                                                                                         preprint arXiv:2606.18619, 2026.
[125] M. Böhme, V.-T. Pham, M.-D. Nguyen, and A. Roychoudhury, “Di-
      rected greybox fuzzing,” in Proceedings of the 2017 ACM Sigsac               [142] J. Zhang, S. Hu, C. Lu, R. Lange, and J. Clune, “Darwin godel
      Conference on Computer and Communications Security. ACM,                           machine: Open-ended evolution of self-improving agents,” arXiv
      2017, pp. 2329–2344.                                                               preprint arXiv:2505.22954, 2025.
[126] F. Busse, M. Nowack, and C. Cadar, “Running symbolic execution               [143] C. S. Xia, Z. Wang, Y. Yang, Y. Wei, and L. Zhang, “Live-swe-
      forever,” in Proceedings of the 29th ACM SIGSOFT International                     agent: Can software engineering agents self-evolve on the fly?” arXiv
      Symposium on Software Testing and Analysis. Association for                        preprint arXiv:2511.13646, 2025.
      Computing Machinery, 2020, pp. 63–74.
[127] J. Metzman, L. Szekeres, L. Simon, R. Sprabery, and A. Arya,                 Appendix A.
      “FuzzBench: an open fuzzer benchmarking platform and service,”
      in Proceedings of the 29th ACM Joint Meeting on European Soft-               KLEE Command-Line Configuration
      ware Engineering Conference and Symposium on the Foundations
      of Software Engineering. Association for Computing Machinery,                    The evaluation uses the following KLEE options:
      2021, pp. 1393–1403.
[128] K. Keahey, J. Anderson, Z. Zhen, P. Riteau, P. Ruth, D. Stanzione,           --solver-backend=z3 --max-memory=32768 --watchdog \
      M. Cevik, J. Colleran, H. S. Gunawi, C. Hammock, J. Mambretti,               --only-output-states-covering-new --posix-runtime \
      A. Barnes, F. Halbach, A. Rocha, and J. Stubbs, “Lessons learned from        --libc=uclibc --dump-states-on-halt=false \
      the chameleon testbed,” in Proceedings of the 2020 USENIX Annual             --write-kqueries --write-smt2s --write-cov
      Technical Conference (USENIX ATC ’20). USENIX Association,
      2020.
[129] L. De Moura and N. Bjørner, “Z3: an efficient smt solver,” in Pro-           Appendix B.
      ceedings of the Theory and Practice of Software, 14th International          Per-program Symbolic Environments
      Conference on Tools and Algorithms for the Construction and Analysis
      of Systems. Springer-Verlag, 2008, p. 337–340.
                                                                                       Table 10 lists the exact per-program argument sequence
[130] OWI Team, “Seamless bug-finding for c, c++, go, rust, wasm and
      zig,” https://github.com/OCamlPro/owi, 2025.
                                                                                   appended after the program bitcode in each KLEE invocation.
                                                                                   Literal tokens are passed to the target as concrete command-
[131] CrossHair Team, “An analysis tool for python that blurs the line
      between testing and type systems.” https://github.com/pschanely/             line arguments, whereas the –sym-* options are interpreted
      crosshair, 2025.                                                             by KLEE’s POSIX runtime.
[132] A. D. Bruni, T. Disney, and C. Flanagan, “A peer architecture for
      lightweight symbolic execution,” Universidad de California, Santa            Appendix C.
      Cruz, 2011.
[133] J. H. Siddiqui and S. Khurshid, “Scaling symbolic execution using
                                                                                   Projects for Evaluating Generalization
      ranged analysis,” in Proceedings of the ACM international conference
      on Object oriented programming systems languages and applications,               Table 11 details the projects behind the per-language
      2012, pp. 523–536.                                                           results in Table 9, with their versions and sources.


                                                                              18
Table 10: Exact symbolic-environment and concrete program arguments used for the 32 evaluated programs. Each sequence
is appended after the program bitcode; order is preserved from the corresponding symEnv definition.

Program Symbolic Environment                                            Program       Symbolic Environment
bash        –sym-args 0 3 10 –sym-stdin 100                             bc        –sym-stdin 40
bison       –sym-args 0 2 2 A –sym-files 1 100                          cjpeg     –sym-args 0 2 4 A –sym-files 1 100
cjson       A –sym-files 1 100 yes                                      combine   –sym-args 0 2 4 A B –sym-files 2 50
curl        –sym-args 0 4 6 –sym-args 0 1 20                            diff      –sym-args 0 2 2 A B –sym-files 2 50
expat       –sym-stdin 100                                              find      –sym-args 0 3 10 –sym-files 1 40 –sym-stdin 40
flex        –sym-args 0 5 12 A –sym-files 1 300                         flvmeta   –sym-arg 2 –sym-args 0 2 6 A –sym-files 1 300
                                                                                  –save-all-writes
gawk        -f A B –sym-files 2 50                                      grep      –sym-args 0 2 2 –sym-arg 10 A –sym-files 1 50
gzip        –sym-args 0 2 2 A –sym-files 1 50                           jasper    –input A –output B –input-format –sym-arg 3
                                                                                  –output-format –sym-arg 3 –sym-args 0 3 15
                                                                                  –sym-files 2 300 –save-all-writes
jq          –sym-args 1 1 10 –sym-stdin 50                              xmllint   A –sym-files 1 40
lua         –sym-stdin 64                                               make      -n -f A –sym-files 1 40
nasm        –sym-args 0 2 2 A –sym-files 1 100                          objcopy   –sym-args 0 3 20 A –sym-files 1 100
openssl     asn1parse -inform DER –sym-stdin 64                         patch     –sym-args 0 2 2 A B –sym-files 2 50
readelf     -a A –sym-files 1 100                                       sed       –sym-arg 10 –sym-args 0 2 2 –sym-files 1 8
                                                                                  –sym-stdin 8
sqlite   –sym-stdin 20 –sym-stdout                                      strip-new –sym-args 0 2 8 A –sym-files 1 100
tic      –sym-args 0 2 8 A –sym-files 1 100                             tiffinfo –sym-args 0 3 8 A –sym-files 1 300
transicc –sym-args 0 2 4 A B –sym-files 2 200                           vim       -N -E -s –sym-stdin 120
         –save-all-writes


Table 11: Projects used to evaluate cross-language general-                 keeping the total end-to-end evaluation budget fixed at 12
ization (Table 9).                                                          hours across all settings. We then evaluate the resulting trans-
                                                                            formed program using the replay-based coverage procedure
Language        Project            Source
                                                                            described in Section 5.1.
                semver (1.0.28) crates.io/crates/semver                        As shown in Table 13, coverage improves at every tested
   Rust
                humantime (2.1.0) crates.io/crates/humantime                budget for both programs, suggesting that additional inference
                tomllib (stdlib)   docs.python.org/3/library/tomllib        time allows Symbolon to discover and apply further coverage-
   Python
                json (stdlib)      docs.python.org/3/library/json           enhancing transformations.
                mathjs (15.2.0)    www.npmjs.com/package/mathjs
   JavaScript                                                               Table 13: Line coverage of bc and flvmeta under increasing
                css (3.0.0)        www.npmjs.com/package/css
                                                                            Symbolon inference time budgets. The vanilla column reports
                                                                            the coverage without applying Symbolon.
Appendix D.                                                                                       Covered LoC by inference budget
Transformation Composition per Program                                      Program
                                                                                        Vanilla      10min     20min     30min      40min
    For each of the 32 benchmark programs, Table 12 reports                 bc           660          773       953      1,384      1,615
the number of transformation instances in the final Symbolon-               flvmeta     1,426        1,970     2,080     3,354      3,508
transformed program, together with a per-transformation
breakdown. We treat each diff hunk as the minimum counting                  Appendix F.
unit. The reported frequencies may therefore underestimate
the actual number of transformations, as a single hunk may                  Evaluations on Logic-Bomb Benchmarks
contain multiple applications of the same transformation or
several distinct transformations.                                               We further evaluate Symbolon on the logic-bomb
                                                                            symbolic-execution benchmark [79]. This benchmark con-
                                                                            tains 53 small C/C++ programs for KLEE covering 12 dif-
Appendix E.                                                                 ferent categories. For each program, we follow the same
Coverage Gains with Longer Inference Time                                   experiment setting as in Section 5.1 with a 60-second time
                                                                            budget. Symbolon applies diverse transformation skills and
    We conduct additional experiments on bc and flvmeta                     achieves 100% coverage on 50 of the 53 programs, covering
to study how the Symbolon inference-time budget affects                     38 more programs than vanilla symbolic execution. The
coverage improvement. For each program, we run Symbolon                     remaining three programs cannot be fully covered because
with inference budgets of 10, 20, 30, and 40 minutes while                  the target flag resides in dead code in stack_bo_l2, depends


                                                                       19
Table 12: Per-program transformation composition: the number of distinct source-level transformation instances (#) applied
in each program’s final Symbolon-transformed version and their per-transformation breakdown classified from each patch’s
recorded rationale. Program names and ordering follow Table 1.
Program # Transformation Breakdown                                 Program       # Transformation Breakdown
bash       3   loop-bound (2), noexec-guard                        bc            3   lookup-to-dataflow (2), solver-hotspot-stub
bison      3   loop-bound (2), reuse-input-var                     cjpeg         2   format-dispatch-pin, valid-image-pin
cjson      1   loop-bound                                          combine       2   loop-bound, state-killer-stub
curl       2   cmd-prefix-bound, recur-to-iter                     diff          3   loop-bound, input-prefix-pin, stat-pin
expat      2   loop-bound, menu-pin                                find          2   array-to-scalar-vars, string-compare
flex       4   loop-bound (2), state-killer-stub, out-bypass       flvmeta       3   loop-bound, menu-pin, concretize-hash
gawk       2   loop-bound (2)                                      grep          3   loop-bound (2), switch-lowering
gzip       2   concretize-hash, state-killer-stub                  jasper        2   menu-pin, recur-to-iter
jq         2   loop-bound, switch-lowering                         xmllint       2   switch-lowering, symbolic-bound-mem
lua        3   loop-bound, tty-reroute, longjmp-model              make          3   loop-bound, state-killer-stub (2)
nasm       3   loop-bound, symbolic-bound-mem, menu-pin            objcopy       2   input-prefix-pin, valid-image-pin
openssl    3   loop-bound (2), menu-pin                            patch         2   loop-bound, input-prefix-pin
readelf    1   input-prefix-pin                                    sed           2   loop-bound, input-prefix-pin
sqlite     2   string-compare, switch-lowering                     strip-new     2   input-prefix-pin, avoid-bound-sentinels
tic        2   concretize-hash, input-prefix-pin                   tiffinfo      3   loop-bound, symbolic-bound-mem, io-model
transicc   3   loop-bound, float-to-int, loop-removing             vim           3   io-model (2), avoid-loop-based-search


on an unmodeled process identifier in pid_csv, or is absent            Name: lower-symbolic-lookup-to-dataflow
from file_posix_cp_l1. Table 14 lists the 38 successfully              Trigger: A symbolic value indexes a constant table whose
triggered logic bombs, together with the transformation skills         entry encodes which class the value falls into, and a branch
Symbolon applied.                                                      then tests that entry.
                                                                       Transformation: Recast the lookup as data flow: a single
Appendix G.                                                            branchless arithmetic predicate over the index (bitwise
Sample Transformations                                                 &/|, never ||/&&) evaluated on one path.
                                                                       Rationale: Symbolic indexing is control flow in disguise;
    Symbolon’s offline learning phase (Section 3.1) produces
                                                                       KLEE must encode the entire table through the SMT
211 transformation rules, each of which is packaged as an
                                                                       theory of arrays. Coverage gain: +38%.
agent skill that records a natural-language trigger, the trans-
formation it performs, the reason it helps symbolic execution,         Before
and a verified before/after C example. We present a few                 1  // b64[c] >= 0 iff c is a base64 character
                                                                        2  signed char b64[256] = {[0 ... 255] = -1,
representative rules below. Interestingly, some of them have            3      [43] = 62,
also been found useful in recent work [92], yet Symbolon                 4     [47] = 63,
                                                                         5     [48 ... 57] = 52,
discovered them through automated learning without relying               6     [65 ... 90] = 0,
on any human expert.                                                     7     [97 ... 122] = 26};
                                                                         8 scanf("%c", &c); // c symbolic
                                                                         9 if (b64[c] >= 0)
                                                                        10   puts("base64"); // 256-entry array-theory query


                                                                       After
                                                                        1 scanf("%c", &c); // c symbolic
                                                                        2 int ok = (c == 43) | ((c >= 47) & (c <= 57)) |
                                                                        3          ((c >= 65) & (c <= 90)) | ((c >= 97) & (c <= 122));
                                                                        4 if (ok)
                                                                        5   puts("base64"); // branchless, one query




                                                                  20
Table 14: The successfully triggered logic-bomb benchmark programs [79] evaluated with Symbolon, grouped by category.
#: number of triggered programs in the category.
Category                         # Programs                                                   Used Transformations
                                                                                              explicit-adjacent-memory-model,
buffer_overflow                  3 heap_bo_l1, stack_bo_l1, stacknocrash_bo_l1                model-overflow-into-field,
                                                                                              heap-to-global-aliasing-model
contextual_symbolic_value 2 ping_csv, syscall_csv                                             unmodeled-syscall-as-nondeterministic-input
                                                                                              inline-asm-to-equivalent-c,
                                     echo_cp_l1, echofile_cp_l1, file_cp_l1,                  in-memory-string-conversion, in-memory-io-roundtrip,
covert_propogation               6
                                     file_posix_cp_l1, socket_cp_l1, stack_cp_l1              external-process-to-in-memory-model,
                                                                                              loopback-socket-to-in-memory-buffer
                                                                                              finite-domain-preimage-enumeration,
crypto_functions                 2 aes_cf, sha_cf
                                                                                              algebraic-key-schedule-inversion
                                                                                              symbolic-to-concrete-case-split,
                                                                                              external-prng-concretization-loop,
                                                                                              sink-external-call-after-branch,
                                     atof_ef_l2, ln_ef_l2, pow_ef_l2, printfloat_ef_l1,
external_functions               7                                                            concrete-case-split-on-input-byte,
                                     printint_int_l1, rand_ef_l2, sin_ef_l2
                                                                                              float-to-integer-arithmetic,
                                                                                              concretize-finite-domain-float-call,
                                                                                              symbolic-integer-decimal-compare
                                                                                              finite-domain-float-concretization,
                                                                                              float-to-integer-branch-decision,
                                   float1_fp_l1, float2_fp_l1, float3_fp_l2,
floating_point                   5                                                            inline-integer-mantissa-annotation,
                                   float4_fp_l2, float5_fp_l2
                                                                                              float-free-decision-via-threshold-tables,
                                                                                              concrete-indexed-accepting-interval-scan
                                                                                              input-domain-concretization,
                                     5n+1_lo_l1, 7n+1_lo_l1, collaz_lo_l1, collaz_lo_l2,      input-domain-enumeration, byte-concretization-fork,
loop                             5
                                     paraloop_lo_l2                                           small-domain-input,
                                                                                              concurrency-to-nondeterministic-schedule
                                                                                              thread-schedule-sequentialization,
                                   2thread_pp_l1, 2thread_pp_l2, forkpipe_pp_l1,              thread-race-analytic-outcome-set,
parallel_program                 5
                                   forkshm_pp_l1, mthread_pp_l2                               model-opaque-ipc-roundtrip-as-direct-copy,
                                                                                              thread-to-sequential-schedule
symbolic_jump                    2 arrayjmp_sj_l2, jmp_sj_l1                                  longjmp-model, state-killer-stub
symbolic_memory                  1 heapoutofbound_sm_l2                                       symbolic-index-to-explicit-select



 Name: avoid-nonlinear-symbolic-constraints                                     Name: precompute-recursion-to-table
 Trigger: A branch condition is a nonlinear function of                         Trigger: A value is computed by multi-way (branching)
 symbolic inputs, such as a product or square of symbolic                       recursion that is re-evaluated for each input.
 variables.                                                                     Transformation: Precompute the recurrence into a table
 Transformation: Offload the nonlinear term to a concrete                       once, reducing each query to a concrete, constant-index
 computation so the residual comparison is effectively                          lookup.
 linear in the symbolic inputs.                                                 Rationale: The per-input recursion multiplies path con-
 Rationale: KLEE’s SMT backend models such nonlinear                            straints and explodes the call tree. Coverage gain: +10%.
 arithmetic imprecisely or times out on it. Coverage gain:                      Before
 +54%.
                                                                                   1 int fn(int n) {
 Before                                                                            2
                                                                                   3
                                                                                       if (n == 0)
                                                                                         return 1;
   1 long long a, b, c;                                                            4   if (n < 0)
   2 scanf("%lld%lld%lld", &a, &b, &c);                                            5     return 0;
   3 if (4 * a * b < (c - a - b) * (c - a - b) && c - a - b > 0)                   6   return fn(n - 1) + fn(n - 2) + fn(n - 3);
   4   puts("Yes");                                                                7 }
   5 else
   6   puts("No");
                                                                                After
 After                                                                             1 int dp[31];
                                                                                   2 dp[0] = dp[1] = 1;
   1   int a, b, c;                                                                3 dp[2] = 2;
   2   scanf("%d%d%d", &a, &b, &c);                                                4 for (i = 3; i < 31; i++)
   3   puts(a + 2 * sqrtl((long long) a * b) + b < c ? "Yes" : "No");              5   dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3];
                                                                                   6 // per query: use dp[n] in place of fn(n)




                                                                          21
Name: avoid-large-fixed-arrays                                     Name: bitmask-instead-of-array-flags
Trigger: A large fixed-size array is pre-allocated and pop-        Trigger: Set membership or per-element boolean flags
ulated as scratch storage, then accessed at input-dependent        are stored in an auxiliary array and queried by indexed
indices.                                                           lookups, often inside a loop.
Transformation: Replace the array with on-the-fly com-             Transformation: Encode the set as bits of an integer and
putation of each value when it is needed, removing the             test membership with a single branchless bitwise AND.
bulk storage.                                                      Rationale: KLEE forks on every symbolic-indexed load
Rationale: The large array creates complex symbolic                and data-dependent branch. Coverage gain: +87%.
memory constraints and many symbolic-indexed accesses.             Before
Coverage gain: +61%.
                                                                    1  int D[10];
Before                                                              2
                                                                    3
                                                                       for (i = 0; i < K; i++) {
                                                                         scanf("%d", &h);
 1  int box[55555] = {};                                             4   D[h] = 1;
 2  for (i = 2; i < 55555; i++)                                      5 }
  3   box[i] = 1;                                                    6 do {
  4 for (i = 2; i < 55555; i++)                                      7   flag = 0;
  5   if (box[i]) {                                                  8   temp = N;
  6     if (i % 10 == 1)                                             9   while (temp != 0)
  7       a[cnt++] = i;                                             10      if (D[temp % 10]) {
  8     for (j = i; j < 55555; j += i)                              11        flag = 1;
  9       box[j] = 0;                                               12        break;
 10     if (cnt == n)                                               13      } else
 11       break;                                                    14        temp /= 10;
 12   }                                                             15   if (flag)
                                                                    16      N++;
                                                                    17 } while (flag);
After
 1  for (i = 3;; i += 2) {                                         After
 2    k = 0;
  3   for (j = 3; j <= sqrt(i); j += 2)                             1  int bit(int x) {
  4     if (i % j == 0) {                                           2    int r = 0;
  5       k = 1;                                                     3   while (x) {
  6       break;                                                     4     r |= 1 << (x % 10);
  7     }                                                            5     x /= 10;
  8   if (k == 0 && i % 5 == 1) {                                    6   }
  9     printf("%d ", i);                                            7   return r;
 10     if (++l == n)                                                8 }
 11       break;                                                     9 while (K--) {
 12   }                                                             10   scanf("%d", &x);
 13 }                                                               11   b |= 1 << x;
                                                                    12 }
                                                                    13 while (bit(N) & b)
                                                                    14   N++;




                                                              22
