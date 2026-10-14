                                                           Lean Meets Theoretical Computer Science:
                                           Scalable Synthesis of Theorem Proving Challenges in Formal-Informal Pairs


                                                            Terry Jingchen Zhang * 1 Wenyuan Jiang * 2 Rongchuan Liu * 2 Yisong Wang 2
                                                           Junran Yang 3 Ning Wang 2 Nicole Ni 4 Yinya Huang 2 5 † Mrinmaya Sachan 2 5 †



                                                                  Abstract                                    1. Introduction
arXiv:2508.15878v2 [cs.LO] 18 May 2026




                                               Formal theorem proving (FTP) has emerged as                    Capability evaluation of Large Language Models (LLMs)
                                               a critical foundation for evaluating the reasoning             reasoning is increasingly shadowed by rapid saturation
                                               capabilities of large language models, enabling                of benchmarks that rely on only final answers such as
                                               automated verification of mathematical proofs at               MATH (Hendrycks et al., 2021) and GPQA (Rein et al.,
                                               scale. However, progress has been constrained by               2023), which cannot fully validate logical correctness of
                                               limited datasets due to the high cost of manual                intermediate steps. Formal Theorem Proving (FTP) (Chen
                                               curation and the scarcity of challenging problems              et al., 2025) emerges as a new frontier to automate stepwise
                                               with verified formal-informal correspondences.                 validation of logical derivation by harnessing the power
                                               We propose leveraging theoretical computer sci-                of formal theorem provers such as Lean (de Moura &
                                               ence (TCS) as a scalable source of rigorous proof              Ullrich, 2021) and Isabelle (Nipkow et al., 2002). How-
                                               problems, where algorithmic definitions enable                 ever, current FTP datasets such as MiniF2F (Zheng et al.,
                                               automated generation of arbitrarily many chal-                 2022), ProofNet (Azerbayev et al., 2023), and Putnam-
                                               lenging theorem-proof pairs. We demonstrate                    Bench (Tsoukalas et al., 2024) remain limited in scope and
                                               this approach on two TCS domains: Busy Beaver                  diversity due to laborious manual curation of public data
                                               problems, which involve proving bounds on Tur-                 prone to contamination (Magar & Schwartz, 2022; Dong
                                               ing machine halting behavior, and Mixed Boolean                et al., 2024) that inflate benchmark scores (Dekoninck et al.,
                                               Arithmetic problems, which combine logical and                 2024) and obscure true model capabilities.
                                               arithmetic reasoning. Our framework automati-
                                               cally synthesizes problems with parallel formal                We propose Theoretical Computer Science (TCS) as a pow-
                                               (Lean4) and informal (Markdown) specifications,                erful and underutilized testbed for structured reasoning eval-
                                               creating a scalable pipeline for generating verified           uation. We explore TCS problems such as Busy Beaver (BB)
                                               proof challenges. Evaluation on frontier mod-                  and Mixed Boolean Arithmetic (MBA) problems, which
                                               els reveals substantial gaps in automated theo-                are uniquely suited for benchmark development as they
                                               rem proving: while DeepSeekProver-V2-671B                      admit precise algorithmic modeling, are easily verifiable
                                               achieves 57.5% success on Busy Beaver prob-                    through proof assistants, and allow for automatic synthe-
                                               lems, it manages only 12% on Mixed Boolean                     sis with tunable complexity. This enables us to construct
                                               Arithmetic problems. These results highlight the               infinitely scalable benchmark problems that are fully au-
                                               difficulty of long-form proof generation even for              tomated, contamination-resistant through exponential pa-
                                               problems that are computationally easy to ver-                 rameter variation, and designed to probe generalization and
                                               ify, demonstrating the value of TCS domains for                abstraction by targeting specific reasoning strategies with
                                               advancing automated reasoning research.                        controllable complexity gradients.
                                                                                                              We introduce a new framework that leverages TCS problem
                                                                                                              modules to systematically evaluate the limits of formal rea-
                                           *
                                            Equal contribution 1 D-CHAB, ETH Zurich, Zurich, Switzer-         soning in LLMs. Our work makes three major contributions:
                                         land. 2 D-INFK, ETH Zurich, Zurich, Switzerland. 3 Independent
                                         Researcher. 4 University of Pennsylvania, PA, USA. 5 ETH AI
                                         Center, Zurich, Switzerland.. Correspondence to: Yinya Huang         A scalable and contamination-resistant benchmarking
                                         <yinya.huang@ethz.ch>.                                               framework. We present a synthesis pipeline that program-
                                         The second AI for MATH Workshop at the 42nd International Con-       matically generates theorem-proving challenges as rigor-
                                         ference on Machine Learning, Vancouver, Canada. Copyright            ously aligned formal-informal pairs, eliminating risks of
                                         2025 by the author(s).                                               hallucination by grounding all problems in rigorous seman-

                                                                                                          1
                                                      Lean Meets TCS

                                                                    A step-level analysis protocol revealing reasoning decom-
                                                                    position bottlenecks. We introduce controlled step-level
                                                                    evaluation using an Out-of-Distribution (OOD) lemma li-
                                                                    brary to probe abstract thinking capabilities. Our analysis
                                                                    shows that models like OpenAI-o4-mini achieve 98.88%
                                                                    accuracy at individual reasoning steps, yet fail at assem-
                                                                    bling those steps into complete proofs. This isolates the
                                                                    transition from local reasoning competence to global proof
                                                                    construction as a fundamental bottleneck, revealing failure
                                                                    modes that existing benchmarks cannot detect.

                                                                    2. Related Work
                                                                    Synthetic Benchmark Against Contamination Rising
                                                                    concerns about whether benchmarks reflect genuine reason-
                                                                    ing capability of LLMs (Magar & Schwartz, 2022; Dong
                                                                    et al., 2024) have motivated various approaches to detect
                                                                    and mitigate data contamination (Dekoninck et al., 2024).
                                                                    LiveBench (White et al., 2024) refreshes benchmark ques-
                                                                    tions every 6 months, while MixEval (Ni et al., 2024)
                                                                    adopts a mixture of benchmarks to remove preference bias.
                                                                    NPHardEval (Fan et al., 2024) takes inspiration from com-
                                                                    putational complexity theory to generate questions provably
                                                                    free from training data contamination through algorithmic
                                                                    construction rather than web scraping. Recent anti-leakage
                                                                    frameworks construct samples with explicitly new knowl-
                                                                    edge absent from LLMs’ training sets (Wu et al., 2025).
                                                                    Nevertheless, contamination remains persistent when ques-
                                                                    tions are sourced from the public Internet.

Figure 1: Overview of our synthesis framework: A problem            FTP for Contamination-Free Generation Formal the-
is instantiated using expert-defined templates to generate          orem proving offers a promising solution to contamina-
theorem-proving challenges, with the formal description in          tion through mechanized verification using interactive the-
Lean4 and the natural language description in Markdown.             orem provers such as Lean, Isabelle, and Coq. Evalua-
                                                                    tion datasets like miniF2F (Zheng et al., 2022) provide
                                                                    unified cross-system benchmarks with 488 Olympiad-level
                                                                    problems, while psychometric frameworks introduce diffi-
tics validated by proof assistants. This enables fine-grained       culty grading reflecting theorem complexity as perceived
control over problem difficulty and supports experiments            by LLMs (Zhang et al., 2025b). LLMs have shown remark-
on reasoning generalization across complexity gradients,            able potential to advance mathematics through FTP (Polu &
opening a new research paradigm for studying how models             Sutskever, 2020), endorsed by leading mathematicians such
scale their reasoning as problem structures become deeper           as Peter Scholze (Scholze, 2022) and Terence Tao (Tao,
and more abstract.                                                  2025). Large-scale synthetic approaches like DeepSeek-
                                                                    Prover demonstrate synthesis of millions of formal state-
                                                                    ments with proofs (Ren et al., 2025). Integration in LLM-
Systematic evaluation revealing abstraction failure                 based Agents (Li et al., 2024a), RAG systems (Zayyad &
modes in frontier models. We evaluate several advanced              Adi, 2024), and applications like code copilots (Murphy
provers, including Kimina-Prover-Preview (Wang et al.,              et al., 2024) and optimization (Yang et al., 2024) further
2025), Goedel-Prover-SFT (Lin et al., 2025), and DeepSeek-          demonstrate FTP’s potential.
Prover-v2-671B across our TCS challenges. While these
models perform well on standard tasks, they fail dramati-           Automated Formal-Informal Pair Generation Autofor-
cally on our benchmarks (e.g., 12% on MBA and 0% on                 malization automatically translates natural language into
several modules), exposing critical limitations where current       formal language, addressing the costly and challenging man-
benchmarks overestimate generalization ability.                     ual process. Recent advances employ theorem provers as

                                                                2
                                                          Lean Meets TCS

judges to validate synthetic data generation through itera-             blank symbol; and F = {qHALT } is the set of final states.
tive approaches (Leang et al., 2025), while methods gen-                The machine operates on an infinite tape initially filled
erate arbitrary numbers of theorems across mathematical                 with zeros, where each step applies δ(q, s) = (q ′ , s′ , d) to
domains using Lean proof tactics. Previous synthetic data               determine the next state q ′ , symbol s′ to write, and direction
approaches (Wu et al., 2021; Huang et al., 2024; Ying et al.,           d to move the head.
2024) for LLM-based autoformalization (Li et al., 2024b;
                                                                        The Busy Beaver function is formally defined as BB(N ) =
Wu et al., 2022; Lu et al., 2024) remain limited by expert
                                                                        max{|steps(M )| : M ∈ HN } where HN denotes all N -
annotation requirements for proofreading LLM-generated
                                                                        state machines that halt on blank tape, and |steps(M )|
formal content, which is labor-intensive and suffers from
                                                                        counts execution steps before halting. This function is
inter-annotator inconsistencies. This work aims to automate
                                                                        undecidable because determining BB(N ) requires solv-
the entire (in)formalization process through templates en-
                                                                        ing instances of the halting problem. Each machine
suring rigorous alignment, rendering manual curation an
                                                                        is specified by its state transition table with tuples
optional quality check rather than an expensive necessity.
                                                                        (State, Symbol, Next State, Move, Write Symbol), as illus-
                                                                        trated in Figure 1.
3. Methodology
                                                                        The parameter N provides natural difficulty scaling through
Our approach employs a systematic three-stage synthesis                 exponential growth in machine count, detailed in Table 1,
framework that generates infinite families of formally rigor-           ranging from 64 machines for N = 1 to over 4 billion for
ous mathematical challenges with provable correctness. The              N = 4.
framework consists of: (1) Problem Module that defines
parameterized computational problems with adjustable diffi-                              n    Number of Machines
culty; (2) Ground-Truth Generation that employs algorith-                                 1                      64
mic methods to determine correct answers; (3) Template-                                   2                  20,736
Based Synthesis that generates rigorously aligned formal-                                 3              16,777,216
informal pairs using expert-defined templates. We demon-                                  4           4,294,967,296
strate this pipeline through two exemplar instantiations:
Busy Beaver machines testing undecidable halting prob-
                                                                        Table 1: Number of Busy Beaver (BB) Machines for In-
lems, and Mixed Boolean-Arithmetic expressions testing
                                                                        creasing Values of N .
symbolic algebraic manipulation, as illustrated in Figure 1.

3.1. The Busy Beaver (BB) Challenge                                     Challenge Task Models must prove whether a given N -
The busy beaver game aims to find a terminating program of              state Busy Beaver machine M (represented by its state
a given size that either produces the most output possible or           transition table as in Figure 1) halts or runs indefinitely
runs for the longest number of steps, with busy beavers de-             when initialized on a blank tape. This directly instantiates
fined as Turing machines that perform a maximum number                  the classical halting problem in a concrete, mathematically
of steps when started on an initially blank tape before halt-           well-defined setting requiring genuine logical reasoning.
ing. This problem, introduced by Rado in 1962, represents
one of the most fundamental undecidable problems in com-                Generating Easy-to-Verify Ground-Truth We leverage
putational theory. The profound mathematical significance               precisely known values of BB(N ) for small N to establish
extends far beyond theoretical computer science: recent                 provably correct classifications. Our algorithm executes
breakthroughs have demonstrated that major mathematical                 each candidate machine for exactly BB(N ) + 1 steps using
conjectures, including the Collatz Conjecture and Goldbach              deterministic simulation. Machines reaching qHALT within
Conjecture, reduce to specific Busy Beaver instances BB(6)              this bound are classified as halting; machines failing to halt
and BB(27) respectively, establishing Busy Beaver problems              are provably non-halting by the maximality property of the
as canonical representatives of mathematical undecidability.            Busy Beaver function. This provides computationally effi-
                                                                        cient verification with mathematically rigorous classification
                                                                        boundaries.
Formal Definition of a BB Machine We de-
fine a Busy Beaver Turing machine as a 7-                               Template-Based Synthesis for Hard-to-Prove Challenges
tuple M = (Q, Σ, Γ, δ, q0 , B, F ) where: Q =                           Following Figure 1, we instantiate each machine through
{q0 , q1 , . . . , qN −1 , qHALT } is a finite set of N + 1             expert-designed templates generating both formal Lean the-
states; Σ = {0, 1} is the binary input alphabet; Γ = Σ is the           orem statements and natural language descriptions from
tape alphabet; δ : (Q \ {qHALT }) × Γ → Q × Γ × {L, R}                  identical state transition tables. The Lean template incorpo-
is the transition function; q0 is the initial state; B = 0 is the       rates necessary definitions, complete machine specification,

                                                                    3
                                                       Lean Meets TCS

                                                                     Linear MBA Equations These equations take the form:
                                                                             X                  X
                                                                               ak × ek (x, y) =   bk × e′k (x, y)
                                                                                  k                         k
                                                                              |         {z         }    |         {z         }
                                                                              Linear MBA expression A   Linear MBA expression B

                                                                     where each coefficient ak , bk ∈ {±1, ±2, . . . , ±11} and
                                                                     each atomic boolean expression ek (x, y), e′k (x, y) is drawn
                                                                     from the complete basis of 16 two-variable boolean combi-
                                                                     nations:
                                                                                                                           
                                                                          
                                                                             x     x∨y            x∧y          x⊕y         
                                                                                                                            
                                                                             ¬x    x ∨ ¬y         x ∧ ¬y      ¬(x ⊕ y)
                                                                                                                           
                                                                          
                                                                             y   ¬(x ∨ y)        ¬x ∧ y      ¬(x ∧ y)     
                                                                              ¬y ¬(x ∨ ¬y) ¬(x ∧ ¬y) ¬(¬x ∧ y)
                                                                                                                           
Figure 2: Performance degradation as BB complexity in-
creases for best-performing DeepSeek-Prover-v2-671B
                                                                     Nonlinear MBA Equations These involve products of
                                                                     MBA sub-expressions ek1 (x, y) × ek2 (x, y) and arbitrar-
                                                                     ily nested bitwise operations, such as:
                                                                                                                   
                                                                           10 × ¬ 1 × (x ∧ y) ∨ ¬ (−1) × (x ∨ ¬y)
and theorem statement with sorry placeholder for model
proofs. The Markdown template provides structured nat-               This hierarchical structure creates multiple levels of alge-
ural language descriptions of the same mathematical ob-              braic complexity requiring sophisticated symbolic manipu-
jects, ensuring rigorous semantic alignment. The example             lation techniques.
in Figure 1 demonstrates this dual representation maintain-
ing mathematical precision across both modalities.                   Dataset Generation Following Synthesis Pipeline Fol-
                                                                     lowing the established MBA obfuscator protocol and our
3.2. The Mixed Boolean-Arithmetic (MBA) Challenge                    synthesis pipeline in Figure 1, we construct equations by
                                                                     first generating linear MBA expressions that are identically
Mixed Boolean Arithmetic (MBA) obfuscation transforms
                                                                     zero, then randomly redistributing terms across equation
a program expression into an equivalent but complex ex-
                                                                     sides with appropriately flipped signs to ensure semantic
pression that is hard to understand, performing semantics-
                                                                     equivalence. Each equation translates into a Lean theorem
preserving transformation from simple expressions to rep-
                                                                     paired with an informal Markdown description as demon-
resentations that are difficult to analyze. MBA expressions
                                                                     strated in Figure 1. All variables and constant coefficients
strategically combine arithmetic operators (+, −, ×) with
                                                                     are declared as BitVec 32, ensuring arithmetic and bit-
bitwise operations (∧, ∨, ⊕, ¬) over integer variables, creat-
                                                                     wise operations operate on 32-bit bitvectors modulo 232 .
ing expressions that use both conventional computer integer
                                                                     The parameter space scales infinitely by incrementing vari-
arithmetic on n-bit words and bitwise logic operations. This
                                                                     able numbers in MBA expressions, guaranteeing sufficient
technique finds extensive application in cryptographic sys-
                                                                     problem diversity through combinatorial explosion.
tems, malware protection, and software obfuscation, where
the goal is generating semantically equivalent but syntac-           The specific MBA equation shown in Figure 1 exemplifies
tically complex expressions that resist automated analysis           this approach: variables x, y are 32-bit bitvectors with the
while preserving computational correctness.                          theorem requiring step-by-step proof that two syntactically
                                                                     complex but semantically equivalent MBA expressions rep-
The mathematical foundation of MBA expressions operates
                                                                     resent identical computational functions. The formal Lean
on bitvectors Z2w where w represents the word size (typi-
                                                                     statement precisely captures bitwise arithmetic semantics
cally 32 or 64 bits). The fundamental insight exploits the
                                                                     while the informal description explains the same mathemat-
fact that arithmetic and bitwise operations can be systemati-
                                                                     ical relationship in natural language.
cally combined to create equivalent expressions with vastly
different syntactic representations. For example, simple ad-
                                                                     Challenge Task Models must prove equivalence between
dition x + y can be obfuscated as (x ⊕ y) + 2 × (x ∧ y),
                                                                     two MBA expressions through explicit step-by-step sym-
exploiting carry propagation properties of binary addition.
                                                                     bolic reasoning using fundamental algebraic identities, bit-
MBA equations manifest in two distinct structural cate-              wise operation laws, and distributive properties. We explic-
gories:                                                              itly prohibit automatic tactics such as bv decide (which

                                                                 4
                                                          Lean Meets TCS

invokes external SAT solvers) to ensure genuine symbolic             Morgan’s laws for bitwise negation, and specialized identi-
manipulation rather than computational verification, thereby         ties like x ⊕ y = x + y − 2 × (x ∧ y) that connect bitwise
testing authentic theorem proving capabilities rather than           and arithmetic operations. The library enables automatic
automated decision procedures.                                       generation and verification of all ground-truth proofs while
                                                                     ensuring model solutions depend solely on fundamental
Generating Easy-to-Verify Ground-Truth via Weighted                  mathematical reasoning rather than domain-specific automa-
2-DNF Canonical Forms To establish verifiable ground-                tion.
truth for MBA equation equivalence, we employ a system-
atic normalization process that converts any MBA expres-             Step-Level Task Decomposition To evaluate fine-grained
sion into a unique canonical representation. For any linear          reasoning capabilities beyond complete proof construction,
MBA equation E1 (x, y) = E2 (x, y) over two variables, we            we decompose each ground-truth proof into sequences of
normalize both sides into their Weighted 2-Disjunctive Nor-          individual step-level tasks corresponding to the systematic
mal Form (W2DNF). This canonical form represents any                 transformation process illustrated in Figure 1. After each
boolean-arithmetic expression as a weighted sum of all pos-          tactic application in our ground-truth proofs, Lean reports
sible conjunctions of the two variables and their negations:         updated proof goals, and whenever the left-hand side (LHS)
                        X                                            or right-hand side (RHS) of the current goal changes, we
    W2DNF(E) =                   cij (E) × (ℓi (x) ∧ ℓj (y))         extract a corresponding step lemma following systematic
                     i,j∈{0,1}                                       rules. For LHS changes, the extracted lemma has its LHS
                                                                     matching the previous goal’s LHS and its RHS matching
where the literal functions are defined as ℓ0 (z) = ¬z and           the current goal’s LHS; for RHS changes, the lemma’s LHS
ℓ1 (z) = z, creating four fundamental conjunctive terms:             matches the previous goal’s RHS and its RHS matches the
¬x ∧ ¬y, ¬x ∧ y, x ∧ ¬y, and x ∧ y. Each coefficient                 current goal’s RHS. Each problem’s final step employs the
cij (E) ∈ Z232 represents the weight of the corresponding            simp tactic for goal completion, while all non-final tac-
conjunctive term and is uniquely determined by the structure         tics exclusively use simp only, rw, or nth rewrite
of expression E.                                                     with lemmas from our custom library. This decomposition
                                                                     ensures that every individual reasoning step can be indepen-
The key mathematical property is that two MBA expres-
                                                                     dently verified and evaluated, enabling detailed analysis of
sions E1 and E2 are semantically equivalent if and only
                                                                     model capabilities at the granular level of single algebraic
if their W2DNF representations have identical coefficients:
                                                                     transformations.
cij (E1 ) = cij (E2 ) for all i, j ∈ {0, 1}. This provides an
algorithmic decision procedure: we compute the four coeffi-
cients for each expression and verify their pairwise equality.       4. Experiments
For the concrete example shown in Figure 1, both complex
                                                                     We report Pass@16 on various frontier models, which
MBA expressions on the left and right sides of the equation
                                                                     counts a case as successful if and only if at least one of
reduce to identical W2DNF coefficient vectors, thereby con-
                                                                     the 16 attempts could pass Lean compiler verification, that
firming their mathematical equivalence through systematic
                                                                     is, no errors are reported and no ’sorry’ is used in the proof.
algebraic normalization.
                                                                     While it’s possible to set other n for Pass@n, we note that
We implement this normalization process by systematically
                                                                     n = 16 is the common best practice for existing formal
applying algebraic identities to reduce each MBA expres-
                                                                     theorem proving benchmarks (Zheng et al., 2022; Tsoukalas
sion to its canonical W2DNF form, then translating these
                                                                     et al., 2024; Liu et al., 2025), which strikes a balance of
reduction steps directly into sequences of verifiable Lean
                                                                     reasonable budget and non-deterministic inference. For
tactics using our curated lemma library. This approach
                                                                     unexpected failures such as Timeout, Out-Of-Memory and
provides complete ground-truth solutions that models must
                                                                     API error, we re-run each trial without counting the failed
replicate through symbolic reasoning, ensuring that success-
                                                                     case into n = 16.
ful proof construction demonstrates genuine understanding
of bitwise-arithmetic identities rather than computational
guessing.                                                            4.1. Evaluation Setup
                                                                     Evaluated models. We evaluated both frontier general-
Customized Lemma Library We developed a compre-                      purpose reasoning models and LLM-based theorem provers.
hensive custom library containing all necessary algebraic            Dedicated formal theorem provers are fine-tuned using FTP
identities to reduce any 2-variable linear MBA expression            data on base models such as DeepSeekMath (Shao et al.,
into W2DNF canonical form without external theorem de-               2024). For general-purpose LRMs, we chose a mixture of
pendencies. This library includes fundamental laws such              advanced open-source and proprietary models: DeepSeek-
as distributivity of arithmetic over bitwise operations, De          R1-671B (DeepSeek-AI et al., 2025), QwQ-32B (Qwen,

                                                                 5
                                                       Lean Meets TCS

                   Model                           BB(1)     BB(2)       BB(3)      BB(4)         Total
                   General LRMs
                   DeepSeek-R1                      21/50    12/50        10/50     12/50    55/200 (27.5%)
                   QwQ-32B-Preview                  26/50    21/50        26/50     25/50    98/200 (49.0%)
                   OpenAI-o3                        15/50    17/50        19/50     17/50    68/200 (34.0%)
                   OpenAI-o4-mini                   19/50    10/50        12/50     13/50    54/200 (27.0%)
                   Theorem Provers
                   Goedel-Prover-SFT                 0/50    0/50         0/50      0/50      0/200 (0.0%)
                   Leanabell-Prover-GD-RL            0/50     0/50         0/50      0/50     0/200 (0.0%)
                   Kimina-Prover-Preview-7B          0/50     0/50         0/50      0/50     0/200 (0.0%)
                   DeepSeek-Prover-v2-7B             9/50     9/50        10/50     10/50    38/200 (19.0%)
                   DeepSeek-Prover-v2-671B          34/50    30/50        26/50     25/50   115/200 (57.5%)

Table 2: Pass@16 Results on BB Challenge, where each column represents an incremental setting for state count N as a
complexity parameter.


2025), OpenAI-o3 and o4-mini (OpenAI, 2025). Both Ope-               4.2. Results
nAI models carry default settings of 200K context win-
                                                                     BB challenge. We report Pass@16 in Table 2 and ana-
dow, 100K max output tokens, and a knowledge cut-off
                                                                     lyze detailed failure modes in Section 4.4. Frontier LRMs
date on June 1, 2024. For LLM-based theorem provers,
                                                                     OpenAI-o3 and o4-mini have struggled to score past 35% on
we evaluated various frontier models including Goedel-
                                                                     our BB challenge, marking a critical gap in formal reason-
Prover-SFT (Lin et al., 2025), Leanabelle-Prover (Zhang
                                                                     ing capability despite rapid saturation on static benchmarks
et al., 2025a), Kimina-Prover-Preview-7B (Wang et al.,
                                                                     from public sources.
2025), DeepSeek-Prover-v2-7B, and DeepSeek-Prover-v2-
671B (Ren et al., 2025).                                             Among LLM-based theorem provers, best-performing
                                                                     DeepSeek-Prover-v2-671B (Ren et al., 2025) scored 57.5%,
                                                                     but we notice rapid performance degradation as models
                                                                     scale down to 7B, where advanced theorem provers such as
                                                                     Goedel-Prover-SFT (Lin et al., 2025), Leanabelle-Prover-
                                                                     GD-RL (Zhang et al., 2025a) and Kimina-Prover-Preview-
                                                                     7B (Wang et al., 2025) struggled to solve even 1 instance of
Inference setting. For open-source models, we use greedy
                                                                     our challenges.
sampling to aid reproducibility, which is equivalent to fixing
the sampling temperature to T = 0.0 as recommended by                Paradoxically, QwQ-32B (Qwen, 2025) attained best per-
the model developers (DeepSeek-AI et al., 2025; Qwen,                formance among general LRMs with only 32B parameters,
2025) for math and coding tasks. Furthermore, We enable              which raises an intriguing question as to how scaling affects
thinking mode for all models whenever possible and follow            the performance of general reasoning models vs. dedicated
default settings on Reasoning Efforts, Context Length, Max           theorem provers in a potentially different manner.
Tokens, and System Prompts in model metadata.
We implemented our code under a Linux environment
                                                                     MBA challenge. We report Pass@16 in Table 3, revealing
with Python 3.10. All open-source models are de-
                                                                     even more pronounced difficulties than BB challenge. Fur-
ployed using transformer library and PyTorch on a
                                                                     ther, we decompose 10 randomly selected MBA challenge
4xGH200 server, with open-source models downloaded via
                                                                     into 365 steps and report step-level performance in Table 4.
huggingface-cli. The proprietary models are used
directly via the OpenAI API. We prompted models to follow            Frontier LRMs including DeepSeek-R1 (DeepSeek-AI et al.,
detailed instruction as in Appendix C.                               2025) and QwQ-32B (Qwen, 2025), struggled to solve any
                                                                     of our challenges, while OpenAI-o4-mini (OpenAI, 2025)
After generation, model outputs are parsed to extract Lean
                                                                     solved only 6 problems.
proof, which is validated using a regular expression. The
proof is then verified using Kimina-Lean-Server (San-                Specialized theorem provers exhibited extreme stratification:
tos et al., 2025) built with Lean and Mathlib                        DeepSeek-Prover-v2-671B (Ren et al., 2025) solved 12% of
v4.19.0 via a RESTful API.                                           linear problems with lemmas, but failed all problems with-

                                                                 6
                                                      Lean Meets TCS

out lemmas and all non-linear problems. Smaller provers             model remains heavily reliant on automated tactics and lacks
showed near-universal failure, with only Kimina-Prover-             a clear understanding of what these tactics actually do.
7B (Wang et al., 2025) solving a single instance. This              DeepSeek-Prover-v2-671B:
demonstrates that even state-of-the-art formal systems strug-       theorem mba_challenge_3165c251 (x y : BitVec 32) :
gle with fundamental algebraic reasoning when deprived of             -3#32 * (x | | | ˜˜˜y) - 1#32 * x - 2#32 * y + 1#32 *
                                                                           ,→˜˜˜(x | | | y) + 2#32 * ˜˜˜(x | | | ˜˜˜y) + 2#32 *
lemma support or faced with non-linear complexity.                         ,→(x &&& ˜˜˜y) + 6#32 * (x &&& y) = -2#32 * ˜˜˜y
                                                                           ,→:= by
4.3. Success Cases                                                    have h1 := bv32_not_xor_eq_or x y
                                                                      ...
                                                                      have h2 1 := bv32_sum_all y x
We present a successful case of a non-halting BB(4) ma-
                                                                      norm_num [Nat.add_assoc, Nat.add_comm, Nat.
chine and show more case study in Appendix E. The model                    ,→add_left_comm, Nat.mul_assoc, Nat.mul_comm, Nat
DeepSeekProver-v2-671B leveraged proof by induction and                    ,→.mul_left_comm] at *
                                                                      <;> simp_all (config := {decide := true})
attempted various automated tactics, such as aesop and
                                                                      <;> bv_decide
omega, showing that a considerable manipulation of the                <;> simp_all (config := {decide := true})
automated tactic taxonomy.                                            <;> bv_decide

DeepSeek-Prover-v2-671B:
theorem machine_never_halts : ∀ n, (nth_cfg n).isSome
     ,→:= by                                                        4.4. Failure Cases
  intro n
  have h : ∀ n, (nth_cfg n).isSome := by                            Our experiments reveal several key failure modes of frontier
    intro n                                                         models. These failure can be categorized into 4 major types
    induction n with
    | zero => simp [nth_cfg, init]
                                                                    with signature patterns as shown in Table 3. More cases in
    | succ n ih =>                                                  Appendix E.
       cases h1 : nth_cfg n with
       | none => simp_all [nth_cfg, step, machine, Cfg,
            ,→Stmt, Γ, Fin.forall_fin_succ, Fin.                    Hallucination. Hallucination consistently appears within
            ,→forall_fin_succ’]                                     7B theorem provers, where they often tried to use non-
       | some cfg =>                                                existent theorems or tactics. DeepSeek-Prover-v2-671B
         simp_all [nth_cfg, step, machine, Cfg, Stmt, Γ,
              ,→ Fin.forall_fin_succ, Fin.forall_fin_succ           has exhibited much stronger anti-hallucination capability
              ,→’]                                                  thanks to its large base model.
         <;>
         (try cases cfg <;> simp_all [nth_cfg, step,                Here we show 2 cases where Goedel-Prover-SFT attempted
              ,→machine, Cfg, Stmt, Γ, Fin.                         to prove by induction on a completely unrelated problem.
              ,→forall_fin_succ, Fin.forall_fin_succ’])
         <;>                                                        Similarly, Kimina-Prover-Preview tried to rename the given
         (try aesop)                                                theorem head nth cfg to nth configuration, which
         <;>                                                        led to an unsolved goal at the end of the proof.
         (try omega)
         <;>                                                        Goedel-Prover-SFT:
         (try aesop)                                                theorem sequence_formula {a : N → N} (h1 : a 1 = 1)
  exact h n                                                             (h_rec : ∀ n : N, n ≥ 1 → a (n + 1) = 2 * a n + 1)
                                                                             ,→:
                                                                        ∀ n : N, n ≥ 1 → a n = 2ˆn - 1 := by
In this successful MBA case, the problem is simple enough
that bv decide is able to solve it within its default 10-
                                                                    Kimina-Prover-Preview:
second timeout by leveraging a SAT solver.                          theorem machine_never_halts : ∀ n, (nth cfigurations n)
                                                                         ,→.isSome := by
o4-mini:
                                                                      intro n
theorem mba_challenge_88282d89 (x y : BitVec 32) : 1#32
                                                                      induction n with
     ,→ * ˜˜˜(x &&& ˜˜˜y) + 1#32 * ˜˜˜(x ˆˆˆ y) - 3#32 *
                                                                      | zero =>
     ,→ (x | | | ˜˜˜y) + 1#32 * ˜˜˜(x | | | y) + 3#32 * (x
                                                                        simp [nth configurations]
     ,→&&& ˜˜˜y) + 1#32 * (x &&& y) = 1#32 * ˜˜˜(x | | |
                                                                      | succ n ih =>
     ,→˜˜˜y) := by
                                                                        simp [nth configurations, ih]
  bv_decide
                                                                        <;> aesop


This case is more complex such that bv decide alone                 For the MBA challenge, we show another failure case of
cannot solve. However, the combination of norm num                  OpenAI-o4-mini where model hallucinates a non-existent
and bv decide is sufficient to complete the proof. No-              tactic bv simp.
tably, the sequence of have statements introducing previ-
ously proven lemmas is entirely unused, and the tactics             o4-mini:
                                                                    theorem mba_challenge_14b066fa (x y : BitVec 32) :
following the first bv decide are never executed, as the                 ,→-1#32 * ˜˜˜(x ˆˆˆ y) + 2#32 * ˜˜˜x + 2#32 * ˜˜˜(x
goal is already solved at that point. This suggests that the             ,→ &&& y) + 1#32 * (x | | | y) - 3#32 * x + 3#32 * (x


                                                                7
                                                       Lean Meets TCS

                 Model                           Linear w/ Lemma           Linear w/o Lemma         Non-Linear
                 Reasoning LLMs
                 DeepSeek-R1                            0/100                      0/100                0/40
                 OpenAI-o4-mini                         2/100                      4/100                0/40
                 QwQ-32B-Preview                        0/100                      0/100                0/40
                 Theorem Provers
                 DeepSeek-Prover-v2-7B                   0/100                     0/100                0/40
                 Goedel-Prover                          0/100                      0/100                0/40
                 Kimina-Prover-7B                        1/100                     0/100                0/40
                 Leanabelle-Prover                       0/100                     0/100                0/40
                 DeepSeek-Prover-v2-671B                12/100                     0/100                0/40

Table 3: Pass@16 Performance on MBA challenge. We evaluated all models using 2 parallel settings where models are
tested with vs. without our customized lemma library as detailed in Appendix F. This parallel setting aims to gauge their
capability of in-context learning unseen lemma to tackle novel problems out of their training corpora.


      Model                           #Correct Steps                   intro n
                                                                       ...
      OpenAI-o4-mini                      352/356                        <;> aesop
      DeepSeek-Prover-v2-671B             258/356
                                                                     This tendency is even more pronounced in the following
Table 4: Step-level task performance on linear MBA where             examples. The model gathers many lemmas into one call
models are asked to choose an appropriate lemma from our             without checking their relevance and then blindly invokes
customized lemma library for each step of the proof.                 ring. The proof is bloated with invalid rewrites and heavy au-
                                                                     tomation, yet still fails，demonstrating a systematic failure
       Error Message Type          %(#Errors)                        to reason about lemma and tactic applicability.
       Irrelevant Hallucination    67.27% (122404)                   o4-mini with lemmas:
                                                                     theorem mba_challenge_080db093 (x y : BitVec 32) :
       Tactic Misuse               23.22% (42247)                      -5#32 * ˜˜˜y + 1#32 * ˜˜˜(x &&& ˜˜˜x) + 4#32 * (x | | |
       Voluntary Give Up           4.88% (8871)                             ,→ y) - 6#32 * (x ˆˆˆ y) - 6#32 * ˜˜˜(x &&& ˜˜˜y)
       Type Mismatch               4.47% (8136)                             ,→ - 1#32 * ˜˜˜(x &&& y) - 3#32 * y - 11#32 * ˜˜˜
                                                                            ,→x + 24#32 * ˜˜˜(x | | | y) + 22#32 * ˜˜˜(x | | |
       Others                      0.16% (300)                              ,→˜˜˜y) + 13#32 * (x &&& ˜˜˜y) + 6#32 * (x &&& y
                                                                            ,→) = -4#32 * ˜˜˜(x ˆˆˆ y) + 6#32 * (x | | | ˜˜˜y)
                                                                            ,→:= by
Table 5: Summary of error type distribution for both BB
                                                                       simp only [bv32_and_not_self, bv32_not_and_self,
and MBA Challenge.                                                          ,→bv32_or_not_self, bv32_not_or_self] at *
                                                                       simp only [bv32_x_distr, bv32_y_distr, ...] at *
                                                                       simp only [bv32_sum_all] at *
                                                                       ring
     ,→ | | | ˜˜˜y) - 2#32 * (x ˆˆˆ y) + 1#32 * ˜˜˜(x &&&
     ,→˜˜˜x) - 5#32 * y - 8#32 * ˜˜˜(x | | | y) - 2#32 * (
     ,→x &&& ˜˜˜y) + 3#32 * (x &&& y) = -1#32 * ˜˜˜(x
     ,→&&& ˜˜˜y) := by
                                                                     This sample illustrates a tactic misuse wherebv decide
    bv_simp                                                          fails to solve the goal within the 10-second timeout. The fail-
    ring                                                             ure highlights the limitations of relying solely on automated
                                                                     tactics for large or intricate goals.
                                                                     o4-mini:
Tactic misuse. Models showed a dangerous tendency to                 import Std.Tactic.BVDecide
blindly apply automated proof tactics such as aesop (which           /--
automatically looks for search tactics recursively in a proof        Let x,y be 32-bit bit-vectors. Prove the equivalence of
                                                                          ,→ the following two expressions: 7 · x - 5 · y - 2 · (x⊕
tree) without understanding the necessary conditions for                  ,→y) - 6 ·¬(x ∧ ¬x) - 5 · (x∨y) - 2 ·¬(x∧y) - (x∨¬y) +
aesop to be applicable, resulting in the failure of exhaustive            ,→4 ·¬y - 7 ·¬(x⊕y) + 13 ·¬(x∨y) + 21 ·¬(x∨¬y) + 17 · (x∧
search.                                                                   ,→y) and -5 · (x∧¬y) + 1 ·¬x
                                                                     -/
DeepSeek-Prover-v2-671B:                                             theorem mba_challenge_6f99807f (x y : BitVec 32) :
theorem machine_never_halts : ∀ n, (nth configurations                    ,→((7#32 * x) - (5#32 * y) - (2#32 * (x ˆˆˆ y)) -
     ,→n).isSome := by                                                    ,→(6#32 * (˜˜˜(x &&& (˜˜˜x)))) - (5#32 * (x | | | y))


                                                                 8
                                                        Lean Meets TCS

     ,→ - (2#32 * (˜˜˜(x &&& y))) - (1#32 * (x | | | (˜˜˜y            pattern indicating a fundamental disconnect between syntac-
     ,→))) + (4#32 * (˜˜˜y)) - (7#32 * (˜˜˜(x ˆˆˆ y))) +              tic manipulation and strategic reasoning that fundamentally
     ,→ (13#32 * (˜˜˜(x | | | y))) + (21#32 * (˜˜˜(x | | |
     ,→(˜˜˜y)))) + (17#32 * (x &&& y))) = ((-5#32) * (x               undermines verification integrity.
     ,→&&& (˜˜˜y))) + (1#32 * (˜˜˜x)) := by
  bv_decide
                                                                      The Reasoning Gap between Step-Level vs. Holistic
                                                                      Proof Task Our step-level task decomposition setting re-
                                                                      veals a significant discrepancy between step-level perfor-
Type mismatch. Type mismatch is a fundamental syn-
                                                                      mance and holistic proof synthesis with a simple overhead
tactic error arising from the type-dependent nature of Lean
                                                                      proof goal. Models demonstrate near-perfect capability in
system, which directly reflects models’ failure to understand
                                                                      choosing unseen out-of-distribution lemma for atomic infer-
and correctly apply respective Lean tactics in question. In
                                                                      ence tasks yet exhibit catastrophic failure rates in composing
this case, the 7B theorem-proving models failed to interpret
                                                                      these operations into complete proofs. This divergence indi-
and adapt to Lean’s inherent type rules, producing expres-
                                                                      cates that the primary bottleneck resides not in local opera-
sions whose inferred types did not match the expected ones.
                                                                      tions but in global proof planning and strategic integration.
Fortunately, this type of error occurs rarely at 4.47% in the
                                                                      The persistent inability to reconcile stepwise correctness
big picture, which speaks to the promising progress that
                                                                      with end-to-end whole proof generation suggests reasoning
frontier models have a considerably correct understanding
                                                                      capabilities of frontier models remain constrained in long
of the Lean tactic taxonomy.
                                                                      contexts by insufficient strategic planning for orchestrating
Kimina-Prover-Preview:                                                atomic transformations into coherent proof strategies when
theorem machine_never_halts : ∀ n, (nth_cfg n).isSome
     ,→:= by
                                                                      challenged with lengthy proofs containing multiple steps.
  intro n
  induction n with
                                                                      Contamination-Resistant Evaluation Framework Our
    ...
  | succ n ih =>                                                      methodology establishes a novel evaluation paradigm
    simp [nth_cfg, step, machine]                                     through the integration of Lean with Theoretical Computer
    exact ih
                                                                      Science. Our framework achieves infinite scalability via
                                                                      algorithmic problem generation from parameterized TCS
                                                                      modules, with granular difficulty modulation through com-
Voluntary give-up. In this case, the model voluntarily
                                                                      putational parameters (e.g., Turing Machine state complex-
chose to give up by leaving sorry under the proof goal
                                                                      ity, MBA expression depth). Automated verifiability pro-
without even attempting to solve the problem with any tac-
                                                                      vides ground-truth validation without human intervention,
tics at all. This type of error makes up 4.88% of total errors,
                                                                      while dynamically generated problem spaces ensure intrin-
which could be seen as a failure of instruction-following
                                                                      sic resistance to dataset contamination. By enabling rig-
often depicted by reasoning models comparing to general-
                                                                      orous formal-informal alignment absent expert curation,
purpose LLMs.
                                                                      this TCS-inspired synthesis creates a sustainable evalua-
Kimina-Prover-Preview:                                                tion ecosystem where benchmark freshness and complexity
theorem machine_never_halts : ∀ n, (nth_cfg n).isSome                 scales along with the progress of frontier theoretical com-
     ,→:= by
  sorry                                                               puter science research.

                                                                      6. Conclusion
5. Discussion
                                                                      We propose Theoretical Computer Science as a promising
The Automation Trap in Theorem Proving Our empir-                     testbed for formal theorem proving, which by design is
ical analysis identifies a systematic overreliance on auto-           capable of utilizing modularized, fully automatic problem
mated tactics as primary proof mechanisms across fron-                generation to systematically overcome contamination and
tier models. Models predominantly deploy tactics such as              scalability limitations in legacy benchmarks. Our TCS-
aesop for recursive proof search and bv decide for SAT-               inspired modular synthesis paradigm enables the creation of
based solving as black-box oracles, demonstrating minimal             infinitely scalable, formally rigorous problem spaces with
comprehension of their formal operational boundaries. This            adjustable complexity through computational parameters
dependency manifests in two critical failure modalities: (1)          such as Turing Machine state configurations and MBA ex-
proofs that circumvent genuine deductive understanding                pression depth. Our experimental results demonstrate a
when tactics succeed coincidentally, and (2) complete proof           profound reasoning gap: while models achieve near-perfect
collapse when tactics fail without fallback mechanisms. No-           scores of 98.88% on atomic step-level tasks involving out-of-
tably, models frequently generate elaborate lemma declara-            distribution lemma selection, they collapse to a mere 12%
tions while defaulting to brute-force tactic sequencing—a             success rate when synthesizing complete lengthy proofs.

                                                                  9
                                                     Lean Meets TCS

This drastic performance degradation highlights the devas-          References
tating role of hallucination during long-context reasoning
                                                                    Anthropic.    Claude 3.7 sonnet system card.
sequences, which may act as a roadblock for models to form
                                                                      https://assets.anthropic.com/m/
any systematic strategies for tasks requiring lengthy whole
                                                                     785e231869ea8b3b/original/claude-3-
proofs. We also reveal the dangerous tendency of frontier
                                                                     7-sonnet-system-card.pdf, 2025. Accessed:
models’ over-reliance on automated tactics like aesop and
                                                                      2025-05-10.
bv decide without understanding their applicability with
limitations. To tackle these challenges, we call on the Lean        Azerbayev, Z., Piotrowski, B., Schoelkopf, H., Ayers, E. W.,
community to further explore the massive potential of theo-           Radev, D., and Avigad, J. Proofnet: Autoformalizing
retical computer science and its interplay with the realm of          and formally proving undergraduate-level mathematics.
formal theorem proving, thereby leveraging the joint effort           CoRR, abs/2302.12433, 2023. doi: 10.48550/ARXIV.
to advance both domains synergistically.                              2302.12433. URL https://doi.org/10.48550/
                                                                      arXiv.2302.12433.

                                                                    Chen, S., Yu, W., Dou, G., and Zhang, Q. A review on
                                                                      mechanical proving and formalization of mathematical
                                                                      theorems. IEEE Access, 13:50672–50686, 2025. doi:
                                                                     10.1109/ACCESS.2025.3552634. URL https://doi.
                                                                      org/10.1109/ACCESS.2025.3552634.

                                                                    de Moura, L. and Ullrich, S. The lean 4 theorem prover
                                                                      and programming language. In Platzer, A. and Sutcliffe,
                                                                      G. (eds.), Automated Deduction - CADE 28 - 28th Inter-
                                                                      national Conference on Automated Deduction, Virtual
                                                                      Event, July 12-15, 2021, Proceedings, volume 12699
                                                                      of Lecture Notes in Computer Science, pp. 625–635.
                                                                      Springer, 2021. doi: 10.1007/978-3-030-79876-5\ 37.
                                                                      URL https://doi.org/10.1007/978-3-030-
                                                                      79876-5_37.

                                                                    DeepSeek-AI, Guo, D., Yang, D., Zhang, H., Song, J.,
                                                                      Zhang, R., Xu, R., Zhu, Q., Ma, S., Wang, P., Bi, X.,
                                                                      Zhang, X., Yu, X., Wu, Y., Wu, Z. F., Gou, Z., Shao,
                                                                      Z., Li, Z., Gao, Z., Liu, A., Xue, B., Wang, B., Wu, B.,
                                                                      Feng, B., Lu, C., Zhao, C., Deng, C., Zhang, C., Ruan,
                                                                      C., Dai, D., Chen, D., Ji, D., Li, E., Lin, F., Dai, F., Luo,
                                                                      F., Hao, G., Chen, G., Li, G., Zhang, H., Bao, H., Xu,
                                                                      H., Wang, H., Ding, H., Xin, H., Gao, H., Qu, H., Li,
                                                                      H., Guo, J., Li, J., Wang, J., Chen, J., Yuan, J., Qiu, J.,
                                                                      Li, J., Cai, J. L., Ni, J., Liang, J., Chen, J., Dong, K.,
                                                                      Hu, K., Gao, K., Guan, K., Huang, K., Yu, K., Wang,
                                                                      L., Zhang, L., Zhao, L., Wang, L., Zhang, L., Xu, L.,
                                                                      Xia, L., Zhang, M., Zhang, M., Tang, M., Li, M., Wang,
                                                                      M., Li, M., Tian, N., Huang, P., Zhang, P., Wang, Q.,
                                                                      Chen, Q., Du, Q., Ge, R., Zhang, R., Pan, R., Wang, R.,
                                                                      Chen, R. J., Jin, R. L., Chen, R., Lu, S., Zhou, S., Chen,
                                                                      S., Ye, S., Wang, S., Yu, S., Zhou, S., Pan, S., and Li,
                                                                      S. S. Deepseek-r1: Incentivizing reasoning capability in
                                                                      llms via reinforcement learning. CoRR, abs/2501.12948,
                                                                      2025. doi: 10.48550/ARXIV.2501.12948. URL https:
                                                                     //doi.org/10.48550/arXiv.2501.12948.

                                                                    Dekoninck, J., Müller, M. N., and Vechev, M. T. Constat:
                                                                      Performance-based contamination detection in large
                                                                      language models. In Globersons, A., Mackey, L.,

                                                               10
                                                     Lean Meets TCS

  Belgrave, D., Fan, A., Paquet, U., Tomczak, J. M.,                Li, Z., Hua, W., Wang, H., Zhu, H., and Zhang, Y. Formal-
  and Zhang, C. (eds.), Advances in Neural Informa-                   llm: Integrating formal language and natural language
  tion Processing Systems 38: Annual Conference                       for controllable llm-based agents, 2024a. URL https:
  on Neural Information Processing Systems 2024,                      //arxiv.org/abs/2402.00798.
  NeurIPS 2024, Vancouver, BC, Canada, December
  10 - 15, 2024, 2024.      URL http://papers.                      Li, Z., Wu, Y., Li, Z., Wei, X., Zhang, X., Yang, F., and Ma,
  nips.cc/paper_files/paper/2024/hash/                                X. Autoformalize mathematical statements by symbolic
  a7f89793b9e6f8c6568dbbb6ff727b9b-                                   equivalence and semantic consistency. In Globersons,
  Abstract-Conference.html.                                           A., Mackey, L., Belgrave, D., Fan, A., Paquet, U.,
                                                                      Tomczak, J. M., and Zhang, C. (eds.), Advances in
Dong, Y., Jiang, X., Liu, H., Jin, Z., Gu, B., Yang, M., and          Neural Information Processing Systems 38: Annual
  Li, G. Generalization or memorization: Data contamina-              Conference on Neural Information Processing Systems
  tion and trustworthy evaluation for large language models.          2024, NeurIPS 2024, Vancouver, BC, Canada, December
  In Ku, L., Martins, A., and Srikumar, V. (eds.), Findings           10 - 15, 2024, 2024b.           URL http://papers.
  of the Association for Computational Linguistics, ACL               nips.cc/paper_files/paper/2024/hash/
 2024, Bangkok, Thailand and virtual meeting, August                  6034a661584af6c28fd97a6f23e56c0a-
 11-16, 2024, pp. 12039–12050. Association for Com-                   Abstract-Conference.html.
  putational Linguistics, 2024. doi: 10.18653/V1/2024.
                                                                    Lin, Y., Tang, S., Lyu, B., Wu, J., Lin, H., Yang, K., Li,
  FINDINGS-ACL.716. URL https://doi.org/10.
                                                                      J., Xia, M., Chen, D., Arora, S., and Jin, C. Goedel-
 18653/v1/2024.findings-acl.716.
                                                                      prover: A frontier model for open-source automated the-
Fan, L., Hua, W., Li, L., Ling, H., and Zhang, Y. Nphard-             orem proving, 2025. URL https://arxiv.org/
  eval: Dynamic benchmark on reasoning ability of large               abs/2502.07640.
  language models via complexity classes, 2024. URL                 Liu, J., Lin, X., Bayer, J., Dillies, Y., Jiang, W., Liang,
  https://arxiv.org/abs/2312.14890.                                   X., Soletskyi, R., Wang, H., Xie, Y., Xiong, B., Yang,
Google DeepMind. Gemini 2.5: Our most intelligent                     Z., Zhang, J., Zhi, L., Li, J., and Liu, Z. Combibench:
  ai model. Google AI Blog, Mar 2025; https:                          Benchmarking llm capability for combinatorial math-
 //blog.google/technology/google-                                     ematics, 2025. URL https://arxiv.org/abs/
  deepmind/gemini-model-thinking-                                     2505.03171.
  updates-march-2025/, 2025.                                        Lu, J., Liu, Z., Wan, Y., Huang, Y., Wang, H., Yang, Z.,
Hendrycks, D., Burns, C., Kadavath, S., Arora, A.,                    Tang, J., and Guo, Z. Process-driven autoformalization
  Basart, S., Tang, E., Song, D., and Steinhardt,                     in lean 4. CoRR, abs/2406.01940, 2024. doi: 10.48550/
  J. Measuring mathematical problem solving with                      ARXIV.2406.01940. URL https://doi.org/10.
  the MATH dataset. In Vanschoren, J. and Yeung,                      48550/arXiv.2406.01940.
  S. (eds.), Proceedings of the Neural Information                  Magar, I. and Schwartz, R. Data contamination: From
  Processing Systems Track on Datasets and Bench-                    memorization to exploitation. In Muresan, S., Nakov,
  marks 1, NeurIPS Datasets and Benchmarks 2021,                     P., and Villavicencio, A. (eds.), Proceedings of the 60th
  December 2021, virtual, 2021.     URL https:                       Annual Meeting of the Association for Computational
 //datasets-benchmarks-proceedings.                                  Linguistics (Volume 2: Short Papers), ACL 2022, Dublin,
  neurips.cc/paper/2021/hash/                                        Ireland, May 22-27, 2022, pp. 157–165. Association for
  be83ab3ecd0db773eb2dc1b0a17836a1-                                  Computational Linguistics, 2022. doi: 10.18653/V1/
  Abstract-round2.html.                                              2022.ACL-SHORT.18. URL https://doi.org/10.
                                                                     18653/v1/2022.acl-short.18.
Huang, Y., Lin, X., Liu, Z., Cao, Q., Xin, H., Wang, H., Li,
  Z., Song, L., and Liang, X. MUSTARD: mastering uni-               Murphy, W., Holzer, N., Qiao, F., Cui, L., Rothkopf, R.,
  form synthesis of theorem and proof data. In The Twelfth           Koenig, N., and Santolucito, M. Combining LLM code
  International Conference on Learning Representations,              generation with formal specifications and reactive pro-
  ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenRe-                gram synthesis. CoRR, abs/2410.19736, 2024. doi:
  view.net, 2024. URL https://openreview.net/                        10.48550/ARXIV.2410.19736. URL https://doi.
  forum?id=8xliOUg9EW.                                               org/10.48550/arXiv.2410.19736.
Leang, J. O. J., Hong, G., Li, W., and Cohen, S. B. Theorem         Ni, J., Xue, F., Yue, X., Deng, Y., Shah, M., Jain, K.,
  prover as a judge for synthetic data generation, 2025.              Neubig, G., and You, Y. Mixeval: Deriving wisdom
  URL https://arxiv.org/abs/2502.13137.                               of the crowd from LLM benchmark mixtures. In

                                                               11
                                                  Lean Meets TCS

  Globersons, A., Mackey, L., Belgrave, D., Fan, A.,            Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X.,
  Paquet, U., Tomczak, J. M., and Zhang, C. (eds.),               Zhang, H., Zhang, M., Li, Y. K., Wu, Y., and Guo,
  Advances in Neural Information Processing Systems 38:           D. Deepseekmath: Pushing the limits of mathemat-
  Annual Conference on Neural Information Processing              ical reasoning in open language models, 2024. URL
  Systems 2024, NeurIPS 2024, Vancouver, BC, Canada,              https://arxiv.org/abs/2402.03300.
  December 10 - 15, 2024, 2024. URL http://papers.
  nips.cc/paper_files/paper/2024/hash/                          Tao, T. ams.org. https://www.ams.org/notices/
  b1f34d7b4a03a3d80be8e72eb430dd81-                               202501/rnoti-p6.pdf, 2025. [Accessed 10-05-
  Abstract-Conference.html.                                       2025].

                                                                Tsoukalas, G., Lee, J., Jennings, J., Xin, J., Ding, M.,
Nipkow, T., Paulson, L. C., and Wenzel, M. Isabelle/HOL
                                                                  Jennings, M., Thakur, A., and Chaudhuri, S. Put-
 - A Proof Assistant for Higher-Order Logic, volume
                                                                  nambench: Evaluating neural theorem-provers on the
  2283 of Lecture Notes in Computer Science. Springer,
                                                                  putnam mathematical competition. In Globersons,
  2002. ISBN 3-540-43376-7. doi: 10.1007/3-540-
                                                                  A., Mackey, L., Belgrave, D., Fan, A., Paquet, U.,
  45949-9. URL https://doi.org/10.1007/3-
                                                                  Tomczak, J. M., and Zhang, C. (eds.), Advances in
  540-45949-9.
                                                                  Neural Information Processing Systems 38: Annual
OpenAI.   Openai o3 and o4-mini system card.                      Conference on Neural Information Processing Systems
  https://cdn.openai.com/pdf/2221c875-                            2024, NeurIPS 2024, Vancouver, BC, Canada, Decem-
  02dc-4789-800b-e7758f3722c1/o3-and-                             ber 10 - 15, 2024, 2024. URL http://papers.
  o4-mini-system-card.pdf, 2025.                                  nips.cc/paper_files/paper/2024/hash/
                                                                  1582eaf9e0cf349e1e5a6ee453100aa1-
Polu, S. and Sutskever, I. Generative language modeling           Abstract-Datasets_and_Benchmarks_
  for automated theorem proving. CoRR, abs/2009.03393,            Track.html.
  2020.     URL https://arxiv.org/abs/2009.
                                                                Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., San-
  03393.
                                                                 tos, M. D., Sung, F., Vinyes, M., Ying, Z., Zhu, Z.,
                                                                 Lu, J., de Saxcé, H., Bailey, B., Song, C., Xiao, C.,
Qwen. Qwq - 32b: The power of scaling rl, March 2025.
                                                                 Zhang, D., Zhang, E., Pu, F., Zhu, H., Liu, J., Bayer,
 URL https://qwenlm.github.io/blog/qwq-
                                                                 J., Michel, J., Yu, L., Dreyfus-Schmidt, L., Tunstall,
 32b/. Accessed: 2025 - 05 - 14.
                                                                 L., Pagani, L., Machado, M., Bourigault, P., Wang, R.,
                                                                 Polu, S., Barroyer, T., Li, W.-D., Niu, Y., Fleureau, Y.,
Rein, D., Hou, B. L., Stickland, A. C., Petty, J., Pang,
                                                                 Hu, Y., Yu, Z., Wang, Z., Yang, Z., Liu, Z., and Li, J.
  R. Y., Dirani, J., Michael, J., and Bowman, S. R.
                                                                 Kimina-prover preview: Towards large formal reason-
  GPQA: A graduate-level google-proof q&a benchmark.
                                                                 ing models with reinforcement learning, 2025. URL
  CoRR, abs/2311.12022, 2023. doi: 10.48550/ARXIV.
                                                                 https://arxiv.org/abs/2504.11354.
  2311.12022. URL https://doi.org/10.48550/
  arXiv.2311.12022.                                             White, C., Dooley, S., Roberts, M., Pal, A., Feuer, B., Jain,
                                                                 S., Shwartz-Ziv, R., Jain, N., Saifullah, K., Naidu, S.,
Ren, Z. Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao,         Hegde, C., LeCun, Y., Goldstein, T., Neiswanger, W., and
  W., Zhang, L., Fu, Z., Zhu, Q., Yang, D., Wu, Z. F.,           Goldblum, M. Livebench: A challenging, contamination-
  Gou, Z., Ma, S., Tang, H., Liu, Y., Gao, W., Guo, D.,          free LLM benchmark. CoRR, abs/2406.19314, 2024. doi:
  and Ruan, C. Deepseek-prover-v2: Advancing formal              10.48550/ARXIV.2406.19314. URL https://doi.
  mathematical reasoning via reinforcement learning for          org/10.48550/arXiv.2406.19314.
  subgoal decomposition, 2025. URL https://arxiv.
  org/abs/2504.21801.                                           Wu, X., Pan, L., Xie, Y., Zhou, R., Zhao, S., Ma, Y., Du, M.,
                                                                 Mao, R., Luu, A. T., and Wang, W. Y. Antileakbench: Pre-
Santos, M. D., Wang, H., de Saxcé, H., Wang, R.,                venting data contamination by automatically constructing
  Baksys, M., Unsal, M., Liu, J., Liu, Z., and Li, J.            benchmarks with updated real-world knowledge, 2025.
  Kimina lean server: Technical report. arXiv preprint           URL https://arxiv.org/abs/2412.13670.
  arXiv:2504.21230, 2025.
                                                                Wu, Y., Jiang, A., Ba, J., and Grosse, R. B. {INT}: An
Scholze, P. Liquid tensor experiment. Exp. Math.,                inequality benchmark for evaluating generalization in the-
  31(2):349–354, 2022. doi: 10.1080/10586458.2021.               orem proving. In International Conference on Learning
  1926016.    URL https://doi.org/10.1080/                       Representations, 2021. URL https://openreview.
  10586458.2021.1926016.                                         net/forum?id=O6LPudowNQm.

                                                           12
                                                      Lean Meets TCS

Wu, Y., Jiang, A. Q., Li, W., Rabe, M. N., Staats, C., Jamnik,
 M., and Szegedy, C. Autoformalization with large
 language models. In Koyejo, S., Mohamed, S., Agarwal,
 A., Belgrave, D., Cho, K., and Oh, A. (eds.), Advances
 in Neural Information Processing Systems 35: Annual
 Conference on Neural Information Processing Systems
 2022, NeurIPS 2022, New Orleans, LA, USA, November
 28 - December 9, 2022, 2022. URL http://papers.
 nips.cc/paper_files/paper/2022/hash/
 d0c6bc641a56bebee9d985b937307367-
 Abstract-Conference.html.
Yang, Z., Wang, Y., Huang, Y., Guo, Z., Shi, W., Han, X.,
  Feng, L., Song, L., Liang, X., and Tang, J. Optibench
  meets resocratic: Measure and improve llms for optimiza-
  tion modeling, 2024. URL https://arxiv.org/
  abs/2407.09887.
Ying, H., Wu, Z., Geng, Y., Wang, J., Lin, D., and Chen,
  K. Lean workbook: A large-scale lean problem set
  formalized from natural language math problems. In
  Globersons, A., Mackey, L., Belgrave, D., Fan, A.,
  Paquet, U., Tomczak, J. M., and Zhang, C. (eds.),
  Advances in Neural Information Processing Systems 38:
  Annual Conference on Neural Information Processing
  Systems 2024, NeurIPS 2024, Vancouver, BC, Canada,
  December 10 - 15, 2024, 2024. URL http://papers.
  nips.cc/paper_files/paper/2024/hash/
  bf236666a2cc5f3ae05d2e08485efc4c-
  Abstract-Datasets_and_Benchmarks_
  Track.html.

Zayyad, M. and Adi, Y. Formal language knowledge corpus
  for retrieval augmented generation, 2024. URL https:
  //arxiv.org/abs/2412.16689.
Zhang, J., Wang, Q., Ji, X., Liu, Y., Yue, Y., Zhang, F.,
  Zhang, D., Zhou, G., and Gai, K. Leanabell-prover:
  Posttraining scaling in formal reasoning, 2025a. URL
  https://arxiv.org/abs/2504.06122.
Zhang, J., Zhao, Y., Zhang, L., Hu, J., Luan, X., Xu, Z.,
  and Yang, F. Psychometric-based evaluation for theo-
  rem proving with large language models, 2025b. URL
  https://arxiv.org/abs/2502.00855.

Zheng, K., Han, J. M., and Polu, S. minif2f: a cross-
  system benchmark for formal olympiad-level mathemat-
  ics. In The Tenth International Conference on Learn-
  ing Representations, ICLR 2022, Virtual Event, April
  25-29, 2022. OpenReview.net, 2022. URL https:
  //openreview.net/forum?id=9ZPegFuFTFv.




                                                             13
                                                       Lean Meets TCS

A. Limitations
While this work has been conducted according to best practices of previous work on formal theorem proving, there are
several potential limitations:
Firstly, our evaluation for proprietary OpenAI models are conducted with their default configuration, combined with our
zero-temperature setting for open-sourced models to enhance reproducibility, all evaluated models may not have shared
completely identical settings due to the undisclosed parameter settings of proprietary models.
Meanwhile, in order to strike a balance between budgetary restraints and performance representativeness, we only selected
best-performing models on mainstream formal theorem proving benchmarks such as PutnamBench (Tsoukalas et al., 2024)
and miniF2F (Zheng et al., 2022) for evaluation. There may be merit in exploring how other frontier proprietary models
such as Gemini-2.5 (Google DeepMind, 2025) and Claude-3.7-Sonnet (Anthropic, 2025) would perform on our dataset.
Therefore, we plan to open-source our codebase and dataset to the community for researchers with ample resources to
explore more models.
Lastly, while we leverage Lean compiler to automate proof validation, the proof is graded on a pass/fail basis as a whole.
However, we note it’s possible to implement a stepwise grading metric by dynamically masking each step in a whole proof
and ask the model to fill in each step respectively, thereby gauging models’ capability to implement key intermediate steps.

B. Automated Proof Validation
In our validation pipeline, we adopt the open-source Lean 4 server implementation from Kimina Lean Server (Santos et al.,
2025). The Kimina Lean Server provides a Python interface allowing real-time feedback for generated proofs. With a
Python function call verify, the server receives a list of Lean proofs and returns validation results for each proof. The server
itself handles multiple requests efficiently by spreading verification across multiple Lean REPL processes.

C. Complete Example with Our Prompting Strategy
{lean_code}
‘‘‘
You can make your own auxiliary corollaries and theorems to support the proof, instead of only completing the part
     ,→with the sorry. Please output the entire program and not just the last part. Please output only the program
     ,→and add no other comment, such that your answer is a compilable lean code. Make sure to reason enough to make
     ,→ your code correct.
"""




System Prompt      We used default system prompts as in the evaluated models’ metadata.

A complete BB example. Below we demonstrate a complete record of evaluation, including the problem statement in
Lean 4 and Markdown, our evaluation prompt and the model response:
import Mathlib.Computability.TuringMachine

inductive Γ
  | zero
  | one
   deriving DecidableEq

instance : Inhabited Γ := ⟨ Γ.zero ⟩

structure Stmt where
  move : Turing.Dir
  write : Γ

def Machine := Fin 2 → Γ → Option (Fin 2 × Stmt)

structure Cfg where
  q : Fin 2
  Tape : Turing.Tape Γ

def init (l : List Γ) : Cfg := ⟨ ⟨0, by omega⟩, Turing.Tape.mk1 l⟩


                                                              14
                                                   Lean Meets TCS


def step (M : Machine) : Cfg → Option Cfg :=
  fun ⟨q, T⟩ 7→ (M q T.head).map fun ⟨q’, a⟩ 7→ ⟨q’, (T.write a.write).move a.move⟩

def machine : Machine
| ⟨000, _⟩, Γ.zero => some ⟨ ⟨000, by omega⟩, ⟨Turing.Dir.left, Γ.zero⟩ ⟩
| ⟨000, _⟩, Γ.one => none
| ⟨001, _⟩, Γ.zero => none
| ⟨001, _⟩, Γ.one => some ⟨ ⟨000, by omega⟩, ⟨Turing.Dir.left, Γ.one⟩ ⟩
| ⟨_+2, _⟩, _ => by omega

def nth_cfg : (n : Nat) -> Option Cfg
| 0 => init []
| Nat.succ n => match (nth_cfg n) with
                | none => none
                | some cfg => step machine cfg

/--
Prove the following Turing Machine with the transition table never halts.
| State | Symbol | Next State | Move | Write |
| ------ | ------ | ------ | ------ | ------ |
| 000 | zero | 000 | left | zero |
| 000 | one | HALT | - | - |
| 001 | zero | HALT | - | - |
| 001 | one | 000 | left | one |
-/
theorem machine_never_halts : ∀ n, (nth_cfg n).isSome := by
   sorry
‘‘‘

You can make your own auxiliary corollaries and theorems to support the proof, instead of only completing the part
     ,→with the sorry. Please output the entire program and not just the last part. Please output only the program
     ,→and add no other comment, such that your answer is a compilable lean code. Make sure to reason enough to make
     ,→ your code correct.
### Response:

‘‘‘lean4
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

/-- Given a sequence {an} with a1 = 1 and an+1 = 2an + 1,
     prove that an = 2ˆn - 1 for all n ≥ 1 -/
theorem sequence_formula {a : N → N} (h1 : a 1 = 1)
     (h_rec : ∀ n : N, n ≥ 1 → a (n + 1) = 2 * a n + 1) :
    ∀ n : N, n ≥ 1 → a n = 2ˆn - 1 := by
  /-
  We need to prove that for a sequence \( \{a_n\} \) defined by \( a_1 = 1 \) and \( a_{n+1} = 2a_n + 1 \), the
        ,→general term \( a_n \) is given by \( a_n = 2ˆn - 1 \) for all \( n \geq 1 \).
  1. **Base Case**: For \( n = 1 \), we have \( a_1 = 1 \). This matches \( 2ˆ1 - 1 = 1 \), so the base case holds.
  2. **Inductive Step**: Assume \( a_n = 2ˆn - 1 \) holds for some \( n \geq 1 \). We need to show it holds for \( n
        ,→ + 1 \).
      - By the recurrence relation, \( a_{n+1} = 2a_n + 1 \).
      - Using the inductive hypothesis \( a_n = 2ˆn - 1 \), we get:
         \[
         a_{n+1} = 2(2ˆn - 1) + 1 = 2ˆ{n+1} - 2 + 1 = 2ˆ{n+1} - 1
         \]
      - Thus, \( a_{n+1} = 2ˆ{n+1} - 1 \), completing the inductive step.
  By induction, \( a_n = 2ˆn - 1 \) holds for all \( n \geq 1 \).
  -/
  intro n hn
  induction’ hn with n hn
  -- Base case: n = 1
  -- We know a 1 = 1, which matches 2ˆ1 - 1 = 1
  simp_all
  -- Inductive step: Assume a n = 2ˆn - 1, prove a (n + 1) = 2ˆ(n + 1) - 1
  cases n with
  | zero =>
     -- When n = 0, the induction hypothesis does not apply, so we directly use the initial condition


                                                          15
                                                      Lean Meets TCS

    simp_all
  | succ n =>
    -- For n = succ n, use the recurrence relation and the inductive hypothesis
    simp_all [Nat.succ_eq_add_one, Nat.pow_succ, Nat.mul_succ]
    -- Simplify the expression to match the form 2ˆ(n + 1) - 1
    ring
    <;> omega




A complete step lemma challenge example. Below we demonstrate a complete record of evaluation, including the
problem statement in Lean 4 and Markdown, our evaluation prompt and the model response:
Theorem library:

‘‘‘lean4
import Mathlib.Tactic.Lemma
import Mathlib.Tactic.NthRewrite

@[simp]
theorem bv32_and_not_self(x : BitVec 32) :
  x &&& ˜˜˜x = 0 := by
  simp

@[simp]
theorem bv32_not_not(x : BitVec 32) :
  ˜˜˜˜˜˜x = x := by
  simp

@[simp]
theorem bv32_or_not_self(x : BitVec 32) :
  x | | | ˜˜˜x = BitVec.allOnes 32 := by
  simp

@[simp]
theorem bv32_not_or_self(x : BitVec 32) :
  ˜˜˜x | | | x = BitVec.allOnes 32 := by
  simp

@[simp]
theorem bv32_neg_mul (x y : BitVec 32) :
  -x * y = -(x * y) := by
  simp

theorem bv32_not_and (x y : BitVec 32) :
  ˜˜˜(x &&& y) = ˜˜˜x | | | ˜˜˜y := by
  rw [BitVec.not_and]

theorem bv32_not_or (x y : BitVec 32) :
  ˜˜˜(x | | | y) = ˜˜˜x &&& ˜˜˜y := by
  rw [BitVec.not_or]

theorem bv32_not_xor_eq_or (x y : (BitVec 32)) :
  ˜˜˜(x ˆˆˆ y) = (˜˜˜x &&& ˜˜˜y) | | | (x &&& y) := by
  ext i
  simp
  cases h1 : x[i] <;> cases h2 : y[i]
  simp
  simp
  simp
  simp

theorem bv32_xor_eq_or (x y : (BitVec 32)) :
  (x ˆˆˆ y) = (˜˜˜x &&& y) | | | (x &&& ˜˜˜y) := by
  ext i
  simp
  cases h1 : x[i] <;> cases h2 : y[i]
  simp
  simp
  simp
  simp



                                                           16
                                                    Lean Meets TCS

theorem bv32_x_distr (x y: BitVec 32) :
  x = (x &&& y) | | | (x &&& ˜˜˜y) := by
  ext i
  simp
  simp [← Bool.and_or_distrib_left]

theorem bv32_y_distr (x y: BitVec 32) :
  y = (x &&& y | | | ˜˜˜x &&& y) := by
  ext i
  simp
  simp [← Bool.and_or_distrib_right]


theorem bv32_add_assoc (x y z : BitVec 32) :
  x + y + z = x + (y + z) := by
  rw [BitVec.add_assoc]

theorem bv32_add_comm(x y : BitVec 32) :
  x + y = y + x := by
  rw [BitVec.add_comm]

theorem bv32_add_neg_eq_sub {x y : BitVec 32} :
  x + -y = x - y := by
  rw [BitVec.add_neg_eq_sub]

theorem bv32_mul_comm (x y : BitVec 32) :
  x * y = y * x := by
  rw [BitVec.mul_comm]

theorem bv32_var_mul_comm (x y z: BitVec 32) :
  (x &&& y) * z = z * (x &&& y) := by
  rw [BitVec.mul_comm]

theorem bv32_mul_add (x y z : BitVec 32) :
  x * (y + z) = x * y + x * z := by
  rw [BitVec.mul_add]

theorem bv32_neg_eq_mul (x : BitVec 32) :
  -x = x * (BitVec.allOnes 32) := by
  rw [← BitVec.neg_one_eq_allOnes]
  rw [BitVec.mul_neg]
  rw [BitVec.mul_one]

theorem bv32_add_mul_one (x y : BitVec 32) :
  x + x * y = x * (1#32 + y) := by
  rw [BitVec.mul_add]
  rw [BitVec.mul_one]

/--
1: x &&& y
2: ˜˜˜x &&& y
3: x &&& ˜˜˜y
4: ˜˜˜x &&& ˜˜˜y
-/
theorem bv32_or_eq_add12 (x y : BitVec 32) :
   (x &&& y) | | | (˜˜˜x &&& y) = (x &&& y) + (˜˜˜x &&& y) := by
   apply Eq.symm
   apply BitVec.add_eq_or_of_and_eq_zero
   simp [← BitVec.and_assoc]
   simp [BitVec.and_comm _ (˜˜˜x)]
   simp [← BitVec.and_assoc]

theorem bv32_or_eq_add13 (x y : BitVec 32) :
  (x &&& y) | | | (x &&& ˜˜˜y) = (x &&& y) + (x &&& ˜˜˜y) := by
  apply Eq.symm
  apply BitVec.add_eq_or_of_and_eq_zero
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ x]
  simp [BitVec.and_assoc]

theorem bv32_or_eq_add14 (x y : BitVec 32) :
  (x &&& y) | | | (˜˜˜x &&& ˜˜˜y) = (x &&& y) + (˜˜˜x &&& ˜˜˜y) := by


                                                           17
                                                    Lean Meets TCS

  apply Eq.symm
  apply BitVec.add_eq_or_of_and_eq_zero
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ (˜˜˜x)]
  simp [← BitVec.and_assoc]

theorem bv32_or_eq_add21 (x y : BitVec 32) :
  (˜˜˜x &&& y) | | | (x &&& y) = (˜˜˜x &&& y) + (x &&& y) := by
  apply Eq.symm
  apply BitVec.add_eq_or_of_and_eq_zero
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ x]
  simp [← BitVec.and_assoc]

theorem bv32_or_eq_add23 (x y : BitVec 32) :
  (˜˜˜x &&& y) | | | (x &&& ˜˜˜y) = (˜˜˜x &&& y) + (x &&& ˜˜˜y) := by
  apply Eq.symm
  apply BitVec.add_eq_or_of_and_eq_zero
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ x]
  simp [← BitVec.and_assoc]

theorem bv32_or_eq_add31 (x y : BitVec 32) :
  (x &&& ˜˜˜y) | | | (x &&& y) = (x &&& ˜˜˜y) + (x &&& y) := by
  apply Eq.symm
  apply BitVec.add_eq_or_of_and_eq_zero
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ x]
  simp [← BitVec.and_assoc]
  simp [BitVec.and_assoc]

theorem bv32_or_eq_add32 (x y : BitVec 32) :
  (x &&& ˜˜˜y) | | | (˜˜˜x &&& y) = (x &&& ˜˜˜y) + (˜˜˜x &&& y) := by
  apply Eq.symm
  apply BitVec.add_eq_or_of_and_eq_zero
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ (˜˜˜x)]
  simp [← BitVec.and_assoc]

theorem bv32_or_eq_add41 (x y : BitVec 32) :
  (˜˜˜x &&& ˜˜˜y) | | | (x &&& y) = (˜˜˜x &&& ˜˜˜y) + (x &&& y) := by
  apply Eq.symm
  apply BitVec.add_eq_or_of_and_eq_zero
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ x]
  simp [← BitVec.and_assoc]

theorem bv32_or_eq_add_three (x y : BitVec 32) :
  (x | | | y) = (x &&& ˜˜˜y) + (x &&& y) + (˜˜˜x &&& y) := by
  nth_rw 1 [bv32_y_distr x y]
  nth_rw 1 [bv32_x_distr x y]
  simp [← BitVec.or_assoc]
  simp [BitVec.or_comm _ (x &&& y)]
  simp [← BitVec.or_assoc]
  rw [BitVec.or_comm (x &&& y)]
  apply Eq.symm
  rw [BitVec.add_eq_or_of_and_eq_zero]
  rw [BitVec.add_eq_or_of_and_eq_zero]
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ x]
  simp [BitVec.and_assoc]
  rw [BitVec.add_comm]
  rw [← bv32_or_eq_add13]
  rw [← bv32_x_distr x y]
  simp [← BitVec.and_assoc]

theorem bv32_sum_all (x y : BitVec 32) :
  (˜˜˜x &&& ˜˜˜y) + (˜˜˜x &&& y) + (x &&& y) + (x &&& ˜˜˜y) = BitVec.allOnes 32 := by
  simp [BitVec.add_comm _ (˜˜˜x &&& y)]
  simp [BitVec.add_comm _ (x &&& _)]
  simp [← BitVec.add_assoc]
  rw [BitVec.add_eq_or_of_and_eq_zero]


                                                          18
                                                     Lean Meets TCS

  rw [← bv32_or_eq_add_three x y]
  nth_rw 1 [bv32_x_distr x y]
  simp [BitVec.or_comm _ y]
  nth_rw 1 [bv32_y_distr x y]
  simp [← BitVec.or_assoc]
  simp [BitVec.or_comm _ (x &&& y)]
  simp [← BitVec.or_assoc]
  simp [BitVec.or_comm _ (˜˜˜x &&& _)]
  simp [← BitVec.or_assoc]
  simp [BitVec.or_comm _ (˜˜˜x &&& y)]
  rw [← bv32_x_distr (˜˜˜x) y]
  rw [BitVec.or_assoc]
  rw [← bv32_x_distr x y]
  simp
  rw [← bv32_or_eq_add_three x y]
  simp [← BitVec.not_or]

theorem bv32_self_eq_neg_mul (x: BitVec 32):
  x = -x * (BitVec.allOnes 32) := by
  rw [BitVec.neg_mul]
  rw [BitVec.mul_comm]
  rw [← BitVec.neg_mul]
  simp [← BitVec.neg_one_eq_allOnes]

theorem bv32_not_self_and_not (x y : BitVec 32) :
  ˜˜˜(x &&& ˜˜˜x) = (˜˜˜x &&& ˜˜˜y) + (˜˜˜x &&& y) + (x &&& y) + (x &&& ˜˜˜y) := by
  rw [bv32_not_and]
  rw [BitVec.not_not]
  rw [bv32_not_or_self]
  rw [bv32_sum_all]

/--
Let x,y be 32-bit bit-vectors. Prove the equivalence of the following two expressions: $2\cdot \lnot (x\land \lnot y
      ,→)-1\cdot (x\lor \lnot y)-7\cdot \lnot (x\oplus y)+11\cdot \lnot (x\land y)-5\cdot \lnot (x\lor y)-13\cdot \
      ,→lnot (x\lor \lnot y)+6\cdot (x\land y)$, $10\cdot (x\land \lnot y)$
-/
theorem mba_challenge_02a2f35e (x y : BitVec 32) : 2#32 * ˜˜˜(x &&& ˜˜˜y) - 1#32 * (x | | | ˜˜˜y) - 7#32 * ˜˜˜(x ˆˆˆ
      ,→y) + 11#32 * ˜˜˜(x &&& y) - 5#32 * ˜˜˜(x | | | y) - 13#32 * ˜˜˜(x | | | ˜˜˜y) + 6#32 * (x &&& y) = 10#32 * (x &&&
      ,→ ˜˜˜y) := by
   simp only [← bv32_add_neg_eq_sub] /- step 1 -/
   simp only [← bv32_neg_mul] /- step 2 -/
   simp only [bv32_not_and] /- step 3 -/
   simp only [bv32_not_or] /- step 4 -/
   sorry

lemma mba_challenge_02a2f35e_lhs_step_1 (x y : BitVec 32) : 2#32 * ˜˜˜(x &&& ˜˜˜y) - 1#32 * (x | | | ˜˜˜y) - 7#32 *
     ,→˜˜˜(x ˆˆˆ y) + 11#32 * ˜˜˜(x &&& y) - 5#32 * ˜˜˜(x | | | y) - 13#32 * ˜˜˜(x | | | ˜˜˜y) + 6#32 * (x &&& y) = 2#32
     ,→ * ˜˜˜(x &&& ˜˜˜y) + -(1#32 * (x | | | ˜˜˜y)) + -(7#32 * ˜˜˜(x ˆˆˆ y)) + 11#32 * ˜˜˜(x &&& y) + -(5#32 * ˜˜˜(x
     ,→ | | | y)) + -(13#32 * ˜˜˜(x | | | ˜˜˜y)) + 6#32 * (x &&& y) := by
  simp only [← bv32_add_neg_eq_sub]

lemma mba_challenge_02a2f35e_lhs_step_2 (x y : BitVec 32) : 2#32 * ˜˜˜(x &&& ˜˜˜y) + -(1#32 * (x | | | ˜˜˜y)) + -(7#32
     ,→ * ˜˜˜(x ˆˆˆ y)) + 11#32 * ˜˜˜(x &&& y) + -(5#32 * ˜˜˜(x | | | y)) + -(13#32 * ˜˜˜(x | | | ˜˜˜y)) + 6#32 * (x &&&
     ,→ y) = 2#32 * ˜˜˜(x &&& ˜˜˜y) + -1#32 * (x | | | ˜˜˜y) + -7#32 * ˜˜˜(x ˆˆˆ y) + 11#32 * ˜˜˜(x &&& y) + -5#32 *
     ,→˜˜˜(x | | | y) + -13#32 * ˜˜˜(x | | | ˜˜˜y) + 6#32 * (x &&& y) := by
  simp only [← bv32_neg_mul]

lemma mba_challenge_02a2f35e_lhs_step_3 (x y : BitVec 32) : 2#32 * ˜˜˜(x &&& ˜˜˜y) + -1#32 * (x | | | ˜˜˜y) + -7#32 *
     ,→˜˜˜(x ˆˆˆ y) + 11#32 * ˜˜˜(x &&& y) + -5#32 * ˜˜˜(x | | | y) + -13#32 * ˜˜˜(x | | | ˜˜˜y) + 6#32 * (x &&& y) =
     ,→2#32 * (˜˜˜x | | | ˜˜˜˜˜˜y) + -1#32 * (x | | | ˜˜˜y) + -7#32 * ˜˜˜(x ˆˆˆ y) + 11#32 * (˜˜˜x | | | ˜˜˜y) + -5#32 *
     ,→˜˜˜(x | | | y) + -13#32 * ˜˜˜(x | | | ˜˜˜y) + 6#32 * (x &&& y) := by
  simp only [bv32_not_and]

lemma mba_challenge_02a2f35e_lhs_step_4 (x y : BitVec 32) : 2#32 * (˜˜˜x | | | ˜˜˜˜˜˜y) + -1#32 * (x | | | ˜˜˜y) + -7#32
     ,→ * ˜˜˜(x ˆˆˆ y) + 11#32 * (˜˜˜x | | | ˜˜˜y) + -5#32 * ˜˜˜(x | | | y) + -13#32 * ˜˜˜(x | | | ˜˜˜y) + 6#32 * (x &&& y
     ,→) = 2#32 * (˜˜˜x | | | ˜˜˜˜˜˜y) + -1#32 * (x | | | ˜˜˜y) + -7#32 * ˜˜˜(x ˆˆˆ y) + 11#32 * (˜˜˜x | | | ˜˜˜y) + -5#32
     ,→ * (˜˜˜x &&& ˜˜˜y) + -13#32 * (˜˜˜x &&& ˜˜˜˜˜˜y) + 6#32 * (x &&& y) := by
  simp only [bv32_not_or]

lemma mba_challenge_02a2f35e_lhs_step_5 (x y : BitVec 32) : 2#32 * (˜˜˜x | | | ˜˜˜˜˜˜y) + -1#32 * (x | | | ˜˜˜y) + -7#32
     ,→ * ˜˜˜(x ˆˆˆ y) + 11#32 * (˜˜˜x | | | ˜˜˜y) + -5#32 * (˜˜˜x &&& ˜˜˜y) + -13#32 * (˜˜˜x &&& ˜˜˜˜˜˜y) + 6#32 * (x
     ,→ &&& y) = 2#32 * (˜˜˜x | | | ˜˜˜˜˜˜y) + -1#32 * (x | | | ˜˜˜y) + -7#32 * (˜˜˜x &&& ˜˜˜y | | | x &&& y) + 11#32 *


                                                           19
                                                     Lean Meets TCS

       ,→(˜˜˜x | | | ˜˜˜y) + -5#32 * (˜˜˜x &&& ˜˜˜y) + -13#32 * (˜˜˜x &&& ˜˜˜˜˜˜y) + 6#32 * (x &&& y) := by
      simp only [<Theorem here>]
‘‘‘

You are proving a single step of theorem ’mba_challenge_02a2f35e’. Based on the previous steps, select exactly one
     ,→appropriate theorem from the Theorem library above and insert it in place of <Theorem here> to complete the
     ,→proof of lemma ’mba_challenge_02a2f35e_lhs_step_5’. Do not modify any code from previous theorems or lemmas.
     ,→You are also not allowed to add any other tactics to the proof body.
### Response:
You need the lemma that rewrites ˜˜˜(x ˆˆˆ y) into (˜˜˜x &&& ˜˜˜y) | | | (x &&& y). That is
bv32_not_xor_eq_or
So your step 5 becomes:
lemma mba_challenge_02a2f35e_lhs_step_5 (x y : BitVec 32) :
  2#32 * (˜˜˜x | | | ˜˜˜˜˜˜y) + -1#32 * (x | | | ˜˜˜y) + -7#32 * ˜˜˜(x ˆˆˆ y) + 11#32 * (˜˜˜x | | | ˜˜˜y) + -5#32 * (˜˜˜x
       ,→&&& ˜˜˜y) + -13#32 * (˜˜˜x &&& ˜˜˜˜˜˜y) + 6#32 * (x &&& y) = 2#32 * (˜˜˜x | | | ˜˜˜˜˜˜y) + -1#32 * (x | | | ˜˜˜
       ,→y) + -7#32 * (˜˜˜x &&& ˜˜˜y | | | x &&& y) + 11#32 * (˜˜˜x | | | ˜˜˜y) + -5#32 * (˜˜˜x &&& ˜˜˜y) + -13#32 *
       ,→(˜˜˜x &&& ˜˜˜˜˜˜y) + 6#32 * (x &&& y) := by
  simp only [bv32_not_xor_eq_or]
This completes the requested rewrite.




D. Template-Based Formal-Informal Translation
We use the following Python program to produce problem descriptions in rigorously aligned Lean-Markdown pair.
import srsly
from tqdm import tqdm

output_dir = "busy_beaver/prompts_to_run"

tables = list(srsly.read_jsonl("busy_beaver/bb_with_table.jsonl"))

template = """Complete the following Lean 4 code:

‘‘‘lean4
{lean_code}
‘‘‘

You can make your own auxiliary corollaries and theorems to support the proof, instead of only completing the part
     ,→with the sorry. Please output the entire program and not just the last part. Please output only the program
     ,→and add no other comment, such that your answer is a compilable lean code. Make sure to reason enough to make
     ,→ your code correct.
"""

informal_tmplate = """
/--
{informal}
-/
"""

for problem in tables:
    lean_path = problem["file_name"]
    file_name = lean_path.split("/")[-1]
    out_path = f"{output_dir}/{file_name.removesuffix(’.lean’)}.txt"
    is_halting = True
    if "nonhalting" in file_name:
        is_halting = False
    informal_head = "Prove the following Turing Machine with the transition table " + (
        "halts." if is_halting else "never halts."
    )
    # print(out_path)
    lean_code = None
    with open(lean_path, "r") as f:
        lean_code = f.read().removeprefix("\n")
    assert lean_code != None
    informal = "/-- \n" + informal_head + "\n" + problem["table"] + "-/\n"
    with open(out_path, "w") as f:
        f.write(
            template.format(
                 lean_code=lean_code.replace(
                     "theorem machine_", informal + "theorem machine_"


                                                            20
                                                       Lean Meets TCS

                   ).replace("\n\ndef nth_cfg", "\ndef nth_cfg")
                   .replace("\n\n/--", "\n/--")
                   .replace("sorry\n", "sorry")
               )
        )
        pass




E. More Success and Failure Cases
We demonstrate additional full record of evaluation, including problem statements in their Lean-Markdown pair and model
responses for both successful and failed evaluation cases. The comprehensive record of model responses for cases can be
found in the results folder of our dataset.

E.1. Success Case
E.1.1. D EEPSEEK - PROVER - V 2-671B/ BB -4 STATE - CASE 107- NONHALTING
This is a trivial non-halting case, meaning there is no ”HALT” entry in the transition table. It can therefore be resolved via a
single structural induction. Although the proof completes, warning messages appear, such as ”aesop: failed to prove the
goal after exhaustive search”, ”(try aesop) tactic does nothing”, and ”this tactic is never executed”. These suggest the model
does not fully reason about the proof and instead relies on automated tactics, hoping some may resolve the goal.
import Mathlib.Computability.TuringMachine

inductive Γ
  | zero
  | one
   deriving DecidableEq

instance : Inhabited Γ := ⟨ Γ.zero ⟩

structure Stmt where
  move : Turing.Dir
  write : Γ

def Machine := Fin 4 → Γ → Option (Fin 4 × Stmt)

structure Cfg where
  q : Fin 4
  Tape : Turing.Tape Γ

def init (l : List Γ) : Cfg := ⟨ ⟨0, by omega⟩, Turing.Tape.mk1 l⟩

def step (M : Machine) : Cfg → Option Cfg :=
  fun ⟨q, T⟩ 7→ (M q T.head).map fun ⟨q’, a⟩ 7→ ⟨q’, (T.write a.write).move a.move⟩

def machine : Machine
| ⟨000, _⟩, Γ.zero => some ⟨ ⟨001, by omega⟩, ⟨Turing.Dir.left, Γ.one⟩ ⟩
| ⟨000, _⟩, Γ.one => some ⟨ ⟨001, by omega⟩, ⟨Turing.Dir.right, Γ.one⟩ ⟩
| ⟨001, _⟩, Γ.zero => some ⟨ ⟨000, by omega⟩, ⟨Turing.Dir.right, Γ.one⟩ ⟩
| ⟨001, _⟩, Γ.one => some ⟨ ⟨003, by omega⟩, ⟨Turing.Dir.left, Γ.one⟩ ⟩
| ⟨002, _⟩, Γ.zero => some ⟨ ⟨001, by omega⟩, ⟨Turing.Dir.right, Γ.zero⟩ ⟩
| ⟨002, _⟩, Γ.one => some ⟨ ⟨000, by omega⟩, ⟨Turing.Dir.right, Γ.zero⟩ ⟩
| ⟨003, _⟩, Γ.zero => some ⟨ ⟨000, by omega⟩, ⟨Turing.Dir.left, Γ.zero⟩ ⟩
| ⟨003, _⟩, Γ.one => some ⟨ ⟨001, by omega⟩, ⟨Turing.Dir.left, Γ.zero⟩ ⟩
| ⟨_+4, _⟩, _ => by omega

def nth_cfg : (n : Nat) -> Option Cfg
| 0 => init []
| Nat.succ n => match (nth_cfg n) with
                | none => none
                | some cfg => step machine cfg

/--
Prove the following Turing Machine with the transition table never halts.
| State | Symbol | Next State | Move | Write |
| ----- | ----- | ----- | ----- | ----- |


                                                              21
                                                     Lean Meets TCS

| 000 | zero | 001 | left | one |
| 000 | one | 001 | right | one |
| 001 | zero | 000 | right | one |
| 001 | one | 003 | left | one |
| 002 | zero | 001 | right | zero |
| 002 | one | 000 | right | zero |
| 003 | zero | 000 | left | zero |
| 003 | one | 001 | left | zero |
-/
theorem machine_never_halts : ∀ n, (nth_cfg n).isSome := by
   intro n
   have h : ∀ n, (nth_cfg n).isSome := by
     intro n
     induction n with
     | zero => simp [nth_cfg, init]
     | succ n ih =>
       cases h1 : nth_cfg n with
       | none => simp_all [nth_cfg, step, machine, Cfg, Stmt, Γ, Fin.forall_fin_succ, Fin.forall_fin_succ’]
       | some cfg =>
         simp_all [nth_cfg, step, machine, Cfg, Stmt, Γ, Fin.forall_fin_succ, Fin.forall_fin_succ’]
         <;>
         (try cases cfg <;> simp_all [nth_cfg, step, machine, Cfg, Stmt, Γ, Fin.forall_fin_succ, Fin.forall_fin_succ
              ,→’])
         <;>
         (try aesop)
         <;>
         (try omega)
         <;>
         (try aesop)
   exact h n




E.2. Failure Case
E.2.1. D EEPSEEK - PROVER - V 2-671B/ BB -2 STATE - CASE 102- NONHALTING
This is a case where the Turing machine’s state remains fixed at 000. A correct proof requires showing that the machine
consistently executes the first rule of the transition table. The model attempts a single structural induction; however, in
the inductive case succ n ih, it leaves two unsolved goals F alse. These cannot be resolved via the induction hypothesis,
suggesting that the model fails to generalize inductive reasoning in this setting.
import Mathlib.Computability.TuringMachine

inductive Γ
  | zero
  | one
   deriving DecidableEq

instance : Inhabited Γ := ⟨ Γ.zero ⟩

structure Stmt where
  move : Turing.Dir
  write : Γ

def Machine := Fin 2 → Γ → Option (Fin 2 × Stmt)

structure Cfg where
  q : Fin 2
  Tape : Turing.Tape Γ

def init (l : List Γ) : Cfg := ⟨ ⟨0, by omega⟩, Turing.Tape.mk1 l⟩

def step (M : Machine) : Cfg → Option Cfg :=
  fun ⟨q, T⟩ 7→ (M q T.head).map fun ⟨q’, a⟩ 7→ ⟨q’, (T.write a.write).move a.move⟩

def machine : Machine
| ⟨000, _⟩, Γ.zero => some ⟨ ⟨000, by omega⟩, ⟨Turing.Dir.left, Γ.zero⟩ ⟩
| ⟨000, _⟩, Γ.one => none
| ⟨001, _⟩, Γ.zero => none
| ⟨001, _⟩, Γ.one => some ⟨ ⟨000, by omega⟩, ⟨Turing.Dir.left, Γ.one⟩ ⟩


                                                            22
                                                    Lean Meets TCS

| ⟨_+2, _⟩, _ => by omega

def nth_cfg : (n : Nat) -> Option Cfg
| 0 => init []
| Nat.succ n => match (nth_cfg n) with
                | none => none
                | some cfg => step machine cfg

/--
Prove the following Turing Machine with the transition table never halts.
| State | Symbol | Next State | Move | Write |
| ------ | ------ | ------ | ------ | ------ |
| 000 | zero | 000 | left | zero |
| 000 | one | HALT | - | - |
| 001 | zero | HALT | - | - |
| 001 | one | 000 | left | one |
-/
theorem machine_never_halts : ∀ n, (nth_cfg n).isSome := by
   intro n
   have h : ∀ n, (nth_cfg n).isSome := by
     intro n
     induction n with
     | zero =>
       simp [nth_cfg, init]
     | succ n ih =>
       simp_all [nth_cfg, step, machine, Cfg.q, Cfg.Tape, Turing.Tape.move, Option.isSome]
       <;> aesop
   exact h n



E.2.2. G OEDEL - PROVER / BB -2 STATE - CASE 102- NONHALTING
The model produced proof of a completely unrelated theorem about sequences. This seems to be a hallucination, where
the model matched a common pattern like theorem...by sorry and filled in a generic proof without understanding the
actual task. This shows a key limitation of small provers: Without symbolic grounding or verification, they can only match
surface-level patterns rather than truly reasoning.
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

/-- Given a sequence {an} with a1 = 1 and an+1 = 2an + 1,
     prove that an = 2ˆn - 1 for all n ≥ 1 -/
theorem sequence_formula {a : N → N} (h1 : a 1 = 1)
     (h_rec : ∀ n : N, n ≥ 1 → a (n + 1) = 2 * a n + 1) :
    ∀ n : N, n ≥ 1 → a n = 2ˆn - 1 := by
  /-
  We need to prove that for a sequence \( \{a_n\} \) defined by \( a_1 = 1 \) and \( a_{n+1} = 2a_n + 1 \), the
        ,→general term \( a_n \) is given by \( a_n = 2ˆn - 1 \) for all \( n \geq 1 \).
  1. **Base Case**: For \( n = 1 \), we have \( a_1 = 1 \). This matches \( 2ˆ1 - 1 = 1 \), so the base case holds.
  2. **Inductive Step**: Assume \( a_n = 2ˆn - 1 \) holds for some \( n \geq 1 \). We need to show it holds for \( n
        ,→ + 1 \).
      - By the recurrence relation, \( a_{n+1} = 2a_n + 1 \).
      - Using the inductive hypothesis \( a_n = 2ˆn - 1 \), we get:
         \[
         a_{n+1} = 2(2ˆn - 1) + 1 = 2ˆ{n+1} - 2 + 1 = 2ˆ{n+1} - 1
         \]
      - Thus, \( a_{n+1} = 2ˆ{n+1} - 1 \), completing the inductive step.
  By induction, \( a_n = 2ˆn - 1 \) holds for all \( n \geq 1 \).
  -/
  intro n hn
  induction’ hn with n hn
  -- Base case: n = 1
  -- We know a 1 = 1, which matches 2ˆ1 - 1 = 1
  simp_all
  -- Inductive step: Assume a n = 2ˆn - 1, prove a (n + 1) = 2ˆ(n + 1) - 1
  cases n with
  | zero =>


                                                           23
                                                     Lean Meets TCS

    -- When n = 0, the induction hypothesis does not apply, so we directly use the initial condition
    simp_all
  | succ n =>
    -- For n = succ n, use the recurrence relation and the inductive hypothesis
    simp_all [Nat.succ_eq_add_one, Nat.pow_succ, Nat.mul_succ]
    -- Simplify the expression to match the form 2ˆ(n + 1) - 1
    ring
    <;> omega



E.2.3. K IMINI -P ROVER -7B/ BB -4 STATE - CASE 122- NONHALTING
The model just outputs sorry, which means it didn’t complete the proof. This might be because it couldn’t figure out how to
reason about the problem, or because it has seen sorry used as a placeholder in Lean and assumed that was enough to count
as a valid answer.
import Mathlib.Computability.TuringMachine

inductive Γ
  | zero
  | one
   deriving DecidableEq

instance : Inhabited Γ := ⟨ Γ.zero ⟩

structure Statement where
  move : Turing Dir
  write : Γ

def Machine := Fin 4 → Γ → Option (Fin 4 × Statement)

structure Cfg where
  q : Fin 4
  Tape : Turing Tape Γ

def init (l : List Γ) : Cfg := ⟨ ⟨0, by omega⟩, ⟨Turing Dir.right, Γ.zero⟩ ⟩

def step (M : Machine) : Cfg → Option Cfg :=
  fun ⟨q, T⟩ 7→ (M q T.head).map fun ⟨q’, a⟩ 7→ ⟨q’, (T.map a).move a⟩

def machine : Machine
| ⟨000, _⟩, Γ.zero => some ⟨ ⟨001, by omega⟩, ⟨Turing Dir.right, Γ.zero⟩ ⟩
| ⟨000, _⟩, Γ.one => some ⟨ ⟨003, by omega⟩, ⟨Turing Dir.left, Γ.zero⟩ ⟩
| ⟨001, _⟩, Γ.zero => some ⟨ ⟨003, by omega⟩, ⟨Turing Dir.left, Γ.one⟩ ⟩
| ⟨001, _⟩, Γ.one => some ⟨ ⟨002, by omega⟩, ⟨Turing Dir.right, Γ.zero⟩ ⟩
| ⟨002, _⟩, Γ.zero => some ⟨ ⟨003, by omega⟩, ⟨Turing Dir.left, Γ.zero⟩ ⟩
| ⟨002, _⟩, Γ.one => some ⟨ ⟨001, by omega⟩, ⟨Turing Dir.left, Γ.one⟩ ⟩
| ⟨003, _⟩, Γ.zero => some ⟨ ⟨001, by omega⟩, ⟨Turing Dir.left, Γ.one⟩ ⟩
| ⟨003, _⟩, Γ.one => some ⟨ ⟨000, by omega⟩, ⟨Turing Dir.right, Γ.zero⟩ ⟩
| ⟨_+4, _⟩, _ => by omega

def nth configurations (n : Nat) : Option Cfg :=
  | 0 => init []
  | Nat.succ n => match (nth configurations n) with
                 | none => none
                 | some cfg => step machine cfg

/--
Prove the following Turing Machine with the transition table never halts.
| State | Symbol | Next State | Move | Write |
| ------- | -------- | ------------ | ------ |
| 000 | zero | 001 | right | zero |
| 000 | one | 003 | left | zero |
| 001 | zero | 003 | left | one |
| 001 | one | 002 | right | zero |
| 002 | zero | 003 | left | zero |
| 002 | one | 001 | left | one |
| 003 | zero | 001 | left | one |
| 003 | one | 000 | right | zero |
-/
theorem machine_never_halts : ∀ n, (nth configurations n).isSome := by


                                                            24
                                                      Lean Meets TCS

  sorry




F. Customized Lemma Library.
import Mathlib.Tactic.NthRewrite

@[simp]
theorem bv32_and_not_self(x : BitVec 32) :
  x &&& ˜˜˜x = 0 := by
  simp

@[simp]
theorem bv32_not_not(x : BitVec 32) :
  ˜˜˜˜˜˜x = x := by
  simp

@[simp]
theorem bv32_or_not_self(x : BitVec 32) :
  x | | | ˜˜˜x = BitVec.allOnes 32 := by
  simp

@[simp]
theorem bv32_not_or_self(x : BitVec 32) :
  ˜˜˜x | | | x = BitVec.allOnes 32 := by
  simp

@[simp]
theorem bv32_neg_mul (x y : BitVec 32) :
  -x * y = -(x * y) := by
  simp

theorem bv32_not_and (x y : BitVec 32) :
  ˜˜˜(x &&& y) = ˜˜˜x | | | ˜˜˜y := by
  rw [BitVec.not_and]

theorem bv32_not_or (x y : BitVec 32) :
  ˜˜˜(x | | | y) = ˜˜˜x &&& ˜˜˜y := by
  rw [BitVec.not_or]

theorem bv32_not_xor_eq_or (x y : (BitVec 32)) :
  ˜˜˜(x ˆˆˆ y) = (˜˜˜x &&& ˜˜˜y) | | | (x &&& y) := by
  ext i
  simp
  cases h1 : x[i] <;> cases h2 : y[i]
  simp
  simp
  simp
  simp

theorem bv32_xor_eq_or (x y : (BitVec 32)) :
  (x ˆˆˆ y) = (˜˜˜x &&& y) | | | (x &&& ˜˜˜y) := by
  ext i
  simp
  cases h1 : x[i] <;> cases h2 : y[i]
  simp
  simp
  simp
  simp

theorem bv32_x_distr (x y: BitVec 32) :
  x = (x &&& y) | | | (x &&& ˜˜˜y) := by
  ext i
  simp
  simp [← Bool.and_or_distrib_left]

theorem bv32_y_distr (x y: BitVec 32) :
  y = (x &&& y | | | ˜˜˜x &&& y) := by
  ext i
  simp
  simp [← Bool.and_or_distrib_right]


                                                           25
                                                    Lean Meets TCS



theorem bv32_add_assoc (x y z : BitVec 32) :
  x + y + z = x + (y + z) := by
  rw [BitVec.add_assoc]

theorem bv32_add_comm(x y : BitVec 32) :
  x + y = y + x := by
  rw [BitVec.add_comm]

theorem bv32_add_neg_eq_sub {x y : BitVec 32} :
  x + -y = x - y := by
  rw [BitVec.add_neg_eq_sub]

theorem bv32_mul_comm (x y : BitVec 32) :
  x * y = y * x := by
  rw [BitVec.mul_comm]

theorem bv32_var_mul_comm (x y z: BitVec 32) :
  (x &&& y) * z = z * (x &&& y) := by
  rw [BitVec.mul_comm]

theorem bv32_mul_add (x y z : BitVec 32) :
  x * (y + z) = x * y + x * z := by
  rw [BitVec.mul_add]

theorem bv32_neg_eq_mul (x : BitVec 32) :
  -x = x * (BitVec.allOnes 32) := by
  rw [← BitVec.neg_one_eq_allOnes]
  rw [BitVec.mul_neg]
  rw [BitVec.mul_one]

theorem bv32_add_mul_one (x y : BitVec 32) :
  x + x * y = x * (1#32 + y) := by
  rw [BitVec.mul_add]
  rw [BitVec.mul_one]

/--
1: x &&& y
2: ˜˜˜x &&& y
3: x &&& ˜˜˜y
4: ˜˜˜x &&& ˜˜˜y
-/
theorem bv32_or_eq_add12 (x y : BitVec 32) :
   (x &&& y) | | | (˜˜˜x &&& y) = (x &&& y) + (˜˜˜x &&& y) := by
   apply Eq.symm
   apply BitVec.add_eq_or_of_and_eq_zero
   simp [← BitVec.and_assoc]
   simp [BitVec.and_comm _ (˜˜˜x)]
   simp [← BitVec.and_assoc]

theorem bv32_or_eq_add13 (x y : BitVec 32) :
  (x &&& y) | | | (x &&& ˜˜˜y) = (x &&& y) + (x &&& ˜˜˜y) := by
  apply Eq.symm
  apply BitVec.add_eq_or_of_and_eq_zero
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ x]
  simp [BitVec.and_assoc]

theorem bv32_or_eq_add14 (x y : BitVec 32) :
  (x &&& y) | | | (˜˜˜x &&& ˜˜˜y) = (x &&& y) + (˜˜˜x &&& ˜˜˜y) := by
  apply Eq.symm
  apply BitVec.add_eq_or_of_and_eq_zero
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ (˜˜˜x)]
  simp [← BitVec.and_assoc]

theorem bv32_or_eq_add21 (x y : BitVec 32) :
  (˜˜˜x &&& y) | | | (x &&& y) = (˜˜˜x &&& y) + (x &&& y) := by
  apply Eq.symm
  apply BitVec.add_eq_or_of_and_eq_zero
  simp [← BitVec.and_assoc]


                                                           26
                                                    Lean Meets TCS

  simp [BitVec.and_comm _ x]
  simp [← BitVec.and_assoc]

theorem bv32_or_eq_add23 (x y : BitVec 32) :
  (˜˜˜x &&& y) | | | (x &&& ˜˜˜y) = (˜˜˜x &&& y) + (x &&& ˜˜˜y) := by
  apply Eq.symm
  apply BitVec.add_eq_or_of_and_eq_zero
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ x]
  simp [← BitVec.and_assoc]

theorem bv32_or_eq_add31 (x y : BitVec 32) :
  (x &&& ˜˜˜y) | | | (x &&& y) = (x &&& ˜˜˜y) + (x &&& y) := by
  apply Eq.symm
  apply BitVec.add_eq_or_of_and_eq_zero
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ x]
  simp [← BitVec.and_assoc]
  simp [BitVec.and_assoc]

theorem bv32_or_eq_add32 (x y : BitVec 32) :
  (x &&& ˜˜˜y) | | | (˜˜˜x &&& y) = (x &&& ˜˜˜y) + (˜˜˜x &&& y) := by
  apply Eq.symm
  apply BitVec.add_eq_or_of_and_eq_zero
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ (˜˜˜x)]
  simp [← BitVec.and_assoc]

theorem bv32_or_eq_add41 (x y : BitVec 32) :
  (˜˜˜x &&& ˜˜˜y) | | | (x &&& y) = (˜˜˜x &&& ˜˜˜y) + (x &&& y) := by
  apply Eq.symm
  apply BitVec.add_eq_or_of_and_eq_zero
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ x]
  simp [← BitVec.and_assoc]

theorem bv32_or_eq_add_three (x y : BitVec 32) :
  (x | | | y) = (x &&& ˜˜˜y) + (x &&& y) + (˜˜˜x &&& y) := by
  nth_rw 1 [bv32_y_distr x y]
  nth_rw 1 [bv32_x_distr x y]
  simp [← BitVec.or_assoc]
  simp [BitVec.or_comm _ (x &&& y)]
  simp [← BitVec.or_assoc]
  rw [BitVec.or_comm (x &&& y)]
  apply Eq.symm
  rw [BitVec.add_eq_or_of_and_eq_zero]
  rw [BitVec.add_eq_or_of_and_eq_zero]
  simp [← BitVec.and_assoc]
  simp [BitVec.and_comm _ x]
  simp [BitVec.and_assoc]
  rw [BitVec.add_comm]
  rw [← bv32_or_eq_add13]
  rw [← bv32_x_distr x y]
  simp [← BitVec.and_assoc]

theorem bv32_sum_all (x y : BitVec 32) :
  (˜˜˜x &&& ˜˜˜y) + (˜˜˜x &&& y) + (x &&& y) + (x &&& ˜˜˜y) = BitVec.allOnes 32 := by
  simp [BitVec.add_comm _ (˜˜˜x &&& y)]
  simp [BitVec.add_comm _ (x &&& _)]
  simp [← BitVec.add_assoc]
  rw [BitVec.add_eq_or_of_and_eq_zero]
  rw [← bv32_or_eq_add_three x y]
  nth_rw 1 [bv32_x_distr x y]
  simp [BitVec.or_comm _ y]
  nth_rw 1 [bv32_y_distr x y]
  simp [← BitVec.or_assoc]
  simp [BitVec.or_comm _ (x &&& y)]
  simp [← BitVec.or_assoc]
  simp [BitVec.or_comm _ (˜˜˜x &&& _)]
  simp [← BitVec.or_assoc]
  simp [BitVec.or_comm _ (˜˜˜x &&& y)]
  rw [← bv32_x_distr (˜˜˜x) y]


                                                          27
                                                  Lean Meets TCS

  rw [BitVec.or_assoc]
  rw [← bv32_x_distr x y]
  simp
  rw [← bv32_or_eq_add_three x y]
  simp [← BitVec.not_or]

theorem bv32_self_eq_neg_mul (x: BitVec 32):
  x = -x * (BitVec.allOnes 32) := by
  rw [BitVec.neg_mul]
  rw [BitVec.mul_comm]
  rw [← BitVec.neg_mul]
  simp [← BitVec.neg_one_eq_allOnes]

theorem bv32_not_self_and_not (x y : BitVec 32) :
  ˜˜˜(x &&& ˜˜˜x) = (˜˜˜x &&& ˜˜˜y) + (˜˜˜x &&& y) + (x &&& y) + (x &&& ˜˜˜y) := by
  rw [bv32_not_and]
  rw [BitVec.not_not]
  rw [bv32_not_or_self]
  rw [bv32_sum_all]




                                                        28
