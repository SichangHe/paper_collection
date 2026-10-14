                                             LLVM Translation Validation Automated with Large
                                                       Language Models and Lean
                                                       Chunhao Liao                                  Hongxu Xu                              Xintong Zhou
                                                   University of Waterloo                      University of Waterloo                   University of Waterloo
                                                           Canada                                     Canada                                   Canada
                                                 chunhao.liao@uwaterloo.ca                    hongxu.xu@uwaterloo.ca                    x27zhou@uwaterloo.ca

                                                                             Yizhou Zhang                            Chengnian Sun
                                                                          University of Waterloo                   University of Waterloo
                                                                                 Canada                                   Canada
                                                                          yizhou@uwaterloo.ca                       cnsun@uwaterloo.ca
arXiv:2609.19583v1 [cs.PL] 17 Sep 2026




                                         Abstract                                                            optimization, the IR provides highly expressive semantics,
                                         LLVM is the cornerstone of modern compilers, but its subtle         including Undefined Behavior (UB) [25]. This expressiveness
                                         intermediate representation (IR) semantics make transforma-         comes at a cost: combined with the sophisticated reason-
                                         tions error-prone and necessitate formal verification. Alive2,      ing required by optimization passes, it makes correct imple-
                                         a state-of-the-art translation validator based on satisfiabil-      mentation notoriously difficult—developers must account
                                         ity modulo theories, has achieved substantial success in au-        for every edge case by hand, and a single overlooked one
                                         tomating the validation of LLVM transformations. However,           can silently produce a miscompilation. Indeed, optimization
                                         it still faces scalability limitations, does not support symbolic   passes account for a significant portion of reported bugs in
                                         bitwidths, and offers only bounded guarantees for loops. In         LLVM [17, 51, 60], making reliable optimizer development a
                                         contrast, interactive theorem provers such as Lean can ad-          persistent challenge.
                                         dress these cases but require substantial proof engineering.        Translation Validation. To provide formal guarantees
                                             In this paper, we present Trivet, a framework combin-           that compiler transformations preserve program semantics,
                                         ing large language models (LLMs) and Lean for automated             modern compiler development increasingly relies on trans-
                                         translation validation of LLVM transformations. Trivet gen-         lation validation [44, 49]. This technique compares a source
                                         erates structured proof scaffolds based on source and target        function (pre-transformation program) with its correspond-
                                         functions, automatically discharges obligations amenable            ing target function (post-transformation program) using a
                                         to deterministic reasoning, and delegates transformation-           formal semantic model, ultimately either proving that the
                                         specific obligations to LLMs. It produces refinement proofs         target refines the source (see theorem 2.1) or generating a
                                         or counterexample-based refutations, with every successful          counterexample if the transformation is invalid. A prominent
                                         verdict checked by the Lean kernel. On 148 LLVM trans-              instance of this methodology is Alive2 [38], a state-of-the-
                                         formations, Trivet verifies or refutes 147, leaving one in-         art, SMT-based [3] bounded translation validator specifically
                                         valid case unresolved. Successful cases include 60 loop-free        designed for LLVM IR. Alive2 has been widely adopted by
                                         transformations with symbolic bitwidths, 27 cases from a            the LLVM community to rigorously vet compiler transfor-
                                         restricted class of loop-containing transformations, and 10         mations before they are accepted [24].
                                         complex valid fixed-bitwidth cases on which Alive2 times               Despite its practical effectiveness, Alive2 has three inher-
                                         out. Compared with an unscaffolded baseline, scaffolding            ent limitations:
                                         enables 26 additional proofs. On cases solved by both con-
                                         figurations, it reduces mean proof time by 75.9% and mean           1. Solver Scalability. As an SMT-based tool, Alive2 can
                                         monetary cost by 88%.                                                  time out on large bitwidths, long instruction sequences,
                                                                                                                and complex formulas [45].
                                         Keywords: Compilers, Translation Validation, Large Lan-             2. Fixed-Bitwidth Reasoning. Alive2 only supports valida-
                                         guage Models, Formal Verification                                      tion of fixed-bitwidth transformation instances, limiting
                                                                                                                its ability to verify optimizations that hold across sym-
                                                                                                                bolic bitwidths [21, 43].
                                         1    Introduction                                                   3. Bounded Loop Unrolling. Alive2 validates loops by
                                         The LLVM compiler infrastructure [16] is a cornerstone of              unrolling them up to a fixed bound, leaving subsequent
                                         modern software development in industry and academia.                  iterations unchecked.
                                         At its core is the LLVM Intermediate Representation (IR), a
                                         strongly typed language that bridges high-level source lan-         These limitations motivate a complementary approach to
                                         guages and diverse target architectures. To enable aggressive       formally validating LLVM transformations.
                                                                            Chunhao Liao, Hongxu Xu, Xintong Zhou, Yizhou Zhang, and Chengnian Sun


   Interactive theorem provers (ITPs) offer a promising alter-                    or counterexamples, while the Lean kernel rigorously cer-
native for translation validation. Compared to SMT-based                          tifies every verdict.
bounded translation validation, an ITP can efficiently express                  • We develop an automated, non-LLM generator that ex-
and validate transformations involving symbolic bitwidths,                        tracts a Lean refinement theorem and structured proof
large bitwidths, long instruction sequences, and loops. While                     scaffolds from the source and target functions. These scaf-
these benefits are compelling in principle, the practical adop-                   folds encode compiler domain knowledge to guide the
tion of such provers has historically been hindered by the                        LLM, reducing validation to focused, transformation-specific
prohibitive cost of proof engineering, which often requires                       holes and converting LLM-proposed counterexamples into
an order of magnitude more proof code than implementation                         machine-checked proofs.
code [8, 9, 18]. However, recent advances in Large Language                     • We evaluate Trivet on 148 LLVM transformations, success-
Models (LLMs) make ITP-based workflows increasingly vi-                           fully validating all 74 valid cases and refuting 73 invalid
able. LLMs can iteratively synthesize and repair proof scripts,                   ones, leaving only one invalid transformation unresolved.
while the ITP kernel rigorously guarantees the correctness                        Trivet validates symbolic-bitwidth and loop-containing
of the final proof [40, 53, 55].                                                  transformations beyond Alive2’s scope. Scaffolding re-
Trivet. To this end, this paper presents Trivet1 , a frame-                       duces mean proof time by 75.9% and mean monetary cost
work that pioneers the application of LLMs and Lean [10, 11]                      by 88% compared to an unscaffolded baseline, enabling 26
to the automated translation validation of LLVM transforma-                       additional proofs in total.
tions. By leveraging domain knowledge of compiler optimiza-
tions, Trivet automatically extracts a Lean refinement theo-
rem and structured proof scaffolds directly from the source                     2     Background
and target functions. These scaffolds not only minimize ex-
pensive LLM queries, but also systematically guide the LLM                      This section provides necessary background on LLVM trans-
through both verification and refutation. For verification,                     formations and LLVM translation validation.
the scaffold leaves focused typed holes for transformation-
specific proof obligations, which an LLM can solve, using
Lean’s diagnostic feedback to iteratively repair proofs when                    2.1   LLVM Transformations
necessary. For refutation, a structured prompt guides the                       LLVM transformations rewrite LLVM IR while preserving
LLM to propose a concrete counterexample. Trivet uses a                         the program’s observable behavior. They range from local
deterministic scaffold to check the candidate counterexam-                      instruction-level rewrites to optimizations involving mul-
ple and, upon successful validation, construct a machine-                       tiple basic blocks or loops. Following prior work [43], we
checked proof of non-refinement. In both cases, Lean re-                        represent a transformation by the following judgment:
mains the trusted checker of the final verdict.
                                                                                                      PRE ⊨ LHS ⇒ RHS
   We evaluate Trivet on a dataset of 148 LLVM transforma-
tions. The dataset includes a loop-free subset (60 valid, 60                    where LHS (left-hand side) denotes the pre-transformation
invalid) and a loop-containing subset (14 valid, 14 invalid).                   fragment, RHS (right-hand side) denotes its replacement,
Both subsets cover fixed-bitwidth and symbolic-bitwidth                         and PRE is a logical predicate over the operands in LHS that
cases. Overall, Trivet successfully validates all 74 valid trans-               defines when the transformation is valid. Specifically, this
formations and refutes 73 invalid ones, leaving only one in-                    judgment states that replacing LHS with RHS is semantics-
valid transformation unresolved. Moreover, compared to an                       preserving when PRE holds. When no explicit precondition
unscaffolded baseline, scaffolding reduces mean proof time                      is specified, PRE defaults to true, indicating that the trans-
by 75.9% and mean monetary cost by 88%, while enabling                          formation is always valid and imposing no constraints on
26 additional proofs in total. In contrast, Alive2 validates 20                 the operands.
out of 30 loop-free, fixed-bitwidth LLVM transformations,                          In practice, LLVM IR translation validation instantiates
but cannot validate symbolic-bitwidth cases or provide un-                      this judgment as a pair of LLVM functions [24]: a src func-
bounded guarantees for loop-containing transformations.                         tion, which encodes PRE and LHS, and a tgt function, which
These results demonstrate Trivet’s effectiveness in automat-                    encodes RHS. The PRE is expressed within the src function
ing the translation validation of LLVM transformations.                         through the llvm.assume intrinsic, which restricts the in-
Contributions. Our main contributions are listed below.                         puts to those satisfying PRE [28].
• We introduce Trivet, the first framework applying LLMs                        Undefined Behavior Semantics. LLVM has two forms of
   and Lean to the automated translation validation of LLVM                     Undefined Behavior (UB): immediate UB and deferred UB [25].
   transformations: the LLM synthesizes refinement proofs                       Immediate UB, such as division by zero, permits arbitrary
                                                                                program behavior. Deferred UB, such as integer overflow, in-
1 Trivet vets LLVM transformations based on the integration of three com-       stead produces an ill-defined value that propagates through
ponents: Lean, LLMs, and LLVM.                                                  downstream computations. These ill-defined values take two
LLVM Translation Validation Automated with Large Language Models and Lean


forms in LLVM: poison [29] and undef [32]. Our work sup-                    for transformations involving nonlinear bit-vector opera-
ports poison, which taints dependent computations and trig-                 tions (e.g. bvudiv) or generalized rewrites [21, 43].
gers immediate UB when used in a way that requires a well-                  Limitation: Fixed-Bitwidth Reasoning. Since standard SMT
defined value, such as a branch condition. In contrast, an                  bit-vector logics, such as the quantifier-free logic over fixed-
undef value nondeterministically takes any value of its type                size bit-vectors (QF_BV), reason about fixed bitwidths [2],
at each use, which has long complicated reasoning about                     Alive2 [38] cannot validate transformations over symbolic
LLVM semantics. LLVM has deprecated undef [37], and thus                    bitwidths. Prior work therefore commonly bounds valida-
our work does not support it.                                               tion to selected bitwidths (e.g. 64 bits) [39, 43]. Consequently,
Refinement Relation. Since optimizers routinely exploit                     validation at selected bitwidths leaves every other width un-
UB, correctness cannot be formulated as equivalence. Follow-                verified. Moreover, transformations with multiple bitwidths
ing Alive2 [26, 38], we formalize transformation correctness                require validating each width combination separately, sub-
in terms of refinement.                                                     stantially increasing the validation overhead.
                                                                            Limitation: Bounded Loop Unrolling. Alive2 handles trans-
Definition 2.1 (Refinement). A target function tgt refines a                formations involving loops by unrolling them to a fixed
source function src, denoted src ⊒ tgt, if for every input:                 depth [38]. Choosing this depth poses a dilemma: shallow
• if src triggers immediate UB, tgt may exhibit any behav-                  unrolling misses bugs that manifest only at later iterations,
  ior [27];                                                                 while deeper bounds make the generated queries intractable.
• if src returns poison, tgt may return poison or any other                 Consequently, bounded loop validation guarantees correct-
  value, but must not trigger immediate UB [29];                            ness only within the selected bound, leaving subsequent
• if src returns a well-defined value, tgt must return the                  iterations unchecked.
  same value and must not trigger immediate UB [33].
                                                                            2.2.2 ITP-Based Translation Validation. Interactive the-
In the absence of UB, this relation degenerates to equivalence.
                                                                            orem provers (ITPs) such as Rocq [52] and Lean [10, 11]
                                                                            provide a rigorous alternative to SMT-based translation vali-
2.2 LLVM Translation Validation                                             dation. In an ITP, the semantics of the compiler IR and the tar-
Translation validation checks each transformation result                    get refinement relation are formalized in higher-order logic,
independently. Given source and target functions src and                    with correctness proofs mechanically verified by a small,
tgt, the validator determines whether src ⊒ tgt. A successful               trusted kernel. For example, Vellvm [5, 62, 64, 65] formalizes
check verifies the transformation; otherwise, it reports a                  LLVM IR semantics in Rocq, while Lean-MLIR [6] provides a
counterexample showing that tgt does not refine src.                        Lean framework to validate transformations across multiple
                                                                            MLIR dialects, including LLVM.
2.2.1 Bounded SMT-Based Translation Validation.                                While ITP-based validation naturally handles symbolic
Bounded SMT-based translation validation encodes the se-                    bitwidths and unbounded loops, it fundamentally relies on
mantics of the source and target functions as logical con-                  manual proof construction—a labor-intensive process requir-
straints over bounded domains, such as bit-vectors with                     ing specialized formal methods expertise. Recent advances
fixed-bitwidth and finitely unrolled loops. An SMT solver                   in applying Large Language Models (LLMs) to automated
then searches for an input on which tgt does not refine src; if             theorem proving offer a viable path to mitigate this burden.
no such input exists, the transformation is verified within the             In this work, we combine the foundational correctness guar-
encoded bounds [20, 38]. Alive2, the state-of-the-art LLVM                  antees of ITPs with the automation of LLMs to synthesize
translation validator [24, 38], follows this approach.                      formal proofs for LLVM transformations.
Inherent Limitations of Alive2. Despite its widespread
adoption in the LLVM community, Alive2 inherits fundamen-
tal limitations from its underlying bounded SMT-based de-                   3   Methodology
sign, particularly concerning solver scalability, fixed-bitwidth            This section presents the design of Trivet, a framework that
reasoning, and bounded loop unrolling.                                      integrates an LLM with Lean to automate translation valida-
Limitation: Solver Scalability. Alive2 suffers from scala-                  tion for LLVM transformations.
bility bottlenecks due to its whole-function formulation of                    Figure 1 shows Trivet’s workflow. For each transformation,
refinement checking and its reliance on bit-blasting in the un-             Trivet launches two branches in parallel, each producing a
derlying SMT solver. It encodes complete source and target                  proof for the Lean kernel to check:
functions without decomposition, causing solver complexity                  • Refinement branch. Trivet first emits a refinement scaf-
to grow rapidly with instruction count and bitwidth [45].                      fold that discharges routine obligations and leaves typed
Furthermore, bit-blasting lowers fixed-width arithmetic to                     holes for the transformation-specific proof obligations;
Boolean circuits, which can become particularly expensive                      the LLM later fills the holes.
                                                                                             Chunhao Liao, Hongxu Xu, Xintong Zhou, Yizhou Zhang, and Chengnian Sun


               Refinement Proof Generation                                                       Lean kernel type-checking without open goals, strictly pre-
                                    Propose                                                      serves the original definitions and theorem statement, and
                                                                        Refinement Success
                                                                                                 relies exclusively on standard axioms [54].




                                                   Lean Proof Checker
              Refinement          LLM Proof
               Scaffold           Generation                              Stop Cx Branch

                            Diagnostics & Repair                                                 3.1.1 Illustrative Example. Figure 2 illustrates refine-
 src, tgt                                                                                        ment proof generation for a real-world LLVM transforma-
                                    Fail
                                                                                                 tion [23]. Let 𝑤 be a positive bitwidth, and 𝑎 and 𝑏 be 𝑤-bit
             LLM Proposes         Refutation                            Refutation Success
                                                                                                 inputs. The transformation is:
             Cx Candidate          Scaffold                                   Stop
                                                                        Refinement Branch             (𝑦 < 0) = (𝑇 <s 0) ⊨ 𝑦 <u 𝑇 =⇒ 𝑎 +nuw 𝑏 <u 1,
                   Cx Proof Generation
                                                                                                      | s           {z              }       | {z }
                                                                                                                    src (𝑤 )                       tgt (𝑤 )
                                                                                                        where 𝑇 = 𝑤 × 𝑤, 𝑦 = (𝑏 +nuw (𝑇 − 1)) +nuw 𝑎.
Figure 1. The workflow of Trivet. Cx denotes counterexam-
                                                                                                 Here, all arithmetic uses 𝑤-bit values. Multiplication and
ple.
                                                                                                 subtraction wrap modulo 2𝑤 , while nuw additions produce
                                                                                                 poison on unsigned overflow. The operators <s and <u de-
• Counterexample branch. The LLM first proposes a coun-                                          note signed and unsigned comparisons, respectively. src(𝑤)
   terexample candidate; Trivet then emits a refutation scaf-                                    and tgt (𝑤) denote the source and target functions instan-
   fold that turns the candidate into a complete Lean proof                                      tiated with input bitwidth 𝑤. The refinement goal for the
   of non-refinement.                                                                            functions src and tgt is:
Lean checks each proof, with its diagnostics guiding the LLM                                                  ∀𝑤 ∈ N, 𝑤 > 0 :      src(𝑤) ⊒ tgt (𝑤).
to revise the refinement proof or propose a new counterex-                                          As shown in Figure 2 (i), Trivet identifies five UB-sensitive
ample. Each branch repeats generation and checking until                                         constructs: poison inputs (C1), unsigned overflow in two
a proof is accepted or the time budget expires. The first ac-                                    source additions (C2, C3), an assumption violation (C4), and
cepted proof establishes validity or invalidity; Trivet stops                                    unsigned overflow in the target addition (C5). While C1–C4
the other branch and reports the result. If neither succeeds,                                    stem from the source, C5 is target-specific. Because C5 could
Trivet leaves the transformation unresolved.                                                     cause the target to evaluate to poison for a well-defined
   This section is organized as follows. §§ 3.1 and 3.2 present                                  source execution (violating refinement), it must be proven
the refinement and counterexample branches for loop-free,                                        unreachable and cannot be discharged automatically.
single-block transformations. § 3.3 extends these workflows                                         In Figure 2 (ii), Trivet performs case analysis on C1–C4 to
to a restricted class of loop-containing transformations. § 3.4                                  cover all source outcomes. If any of C1–C3 holds, the source
describes the implementation and limitations.                                                    evaluates to poison, and a pre-existing lemma discharges
                                                                                                 the obligation since the target produces no immediate UB.
3.1     Refinement Proof Generation
                                                                                                 If C4 holds, the source triggers immediate UB, vacuously
Generating complete refinement proofs with an LLM is costly,                                     satisfying refinement.
particularly across diverse UB cases. To address this, we                                           Otherwise, the source is well-defined. Trivet then gener-
design a scaffold construction strategy that delegates only                                      ates two proof holes: a value equivalence hole (𝑦 <u 𝑇 ) =
transformation-specific reasoning to the LLM: it decomposes                                      (𝑧 <u 1), and a target-UB hole ensuring that 𝑎 + 𝑏 does not
the refinement goal (src ⊒ tgt) via UB-triggering condi-                                         overflow (C5). In Figure 2 (iii), the LLM fills these two holes
tions, automatically discharges deterministic obligations, and                                   under the accumulated branch hypotheses (which rule out
leaves only typed proof holes for the LLM to complete.                                           C1–C4). Finally, the Lean kernel type-checks the assembled
   To guide scaffold construction, we examine Lean-MLIR’s                                        proof within the scaffold.
LLVM dialect [6] and identify nine cases in which an operator
or instruction flag may produce UB. We call such operators                                       3.1.2 Proof Scaffold Generation. Trivet first identifies
and flags UB-sensitive constructs and associate each with                                        UB-sensitive constructs across both functions and systemati-
its precise UB-triggering circumstance, the condition under                                      cally splits on three categories: 1 the source’s UB-triggering
which each construct triggers UB, such as signed overflow                                        circumstances, ordered by when values are first demanded;
for nsw or a zero divisor for udiv.                                                               2 target-specific circumstances that can trigger immediate
   Trivet constructs the scaffold by splitting cases on these                                    UB; and 3 value-selection conditions (e.g., in select instruc-
conditions and automatically discharging proof obligations                                       tions [31]), which guides the LLM to prove each branch sep-
whenever the source yields UB. For well-defined source cases,                                    arately. These splits produce proof obligations under distinct
Trivet generates typed proof holes—establishing value equiv-                                     branch hypotheses, such that the original refinement goal
alence and absence of target UB—to be completed by the LLM                                       holds if and only if all resulting obligations are discharged.
under the corresponding branch hypotheses. To guarantee                                             Each obligation is handled according to the source out-
soundness, Trivet ensures that the generated proof passes                                        come. For immediate UB, Trivet automatically discharges
LLVM Translation Validation Automated with Large Language Models and Lean


       Transformation                         (i) UB-Sensitive Constructs Identification                                      (iii) Complete Refinement Proof
                                        ID    Construct         UB-triggering Circumstances Target-specific?                  -- Comments: Let T = w × w, S = (b + (T − 1)) + a
  src:
  Inputs a: w, b: w                     C1      a,b                     Poison inputs                        ✗
                                                                                                                              theorem value_hole (a b : w) (h0 h₁ h₂ hs ) :
  bw: w = constant w                    C2    add nuw b, T1             Unsigned Overflow                    ✗                      (S <ᵤ T) = (a + b <ᵤ 1) := by
  T: w = mul bw, bw                     C3    add nuw x, a              Unsigned Overflow                    ✗                  ... -- Invoke the LLM to finish this proof
  T1: w = sub T, 1
                                        C4    assume Sign               Assumption Failure                   ✗
  x: w = add nuw b, T1                                                                                                        theorem target_ub_hole (a b : w) (h0 h₁ h₂ hs ) :
  y: w = add nuw x, a                   C5    add nuw a,b               Unsigned Overflow                    ✓                      noUOverflow (a + b) := by
  Sign: i1 = (y <s 0)==(T <s 0)                                                                                                  ... -- Invoke the LLM to finish this proof
  assume Sign                                    (ii) Refinement Scaffold Generation                                          theorem example (w : Nat) (w > 0):
  return y <u T                                                                                                                     src w ⊒ tgt w := by
                                   1 Case Decomposition                                 Insert Proof Holes in 3 :             ...
  tgt:                             Split on UB-Sensitive                                  (a) (y <u T)==(z <u 1)              -- Case Decomposition
  Inputs a: w, b: w                Constructs                                             (b) C5: target-specific UB          · cases h0 : no_poison_input
                                                                        Goal
  z: w = add nuw a,b                                                                                                            · cases h₁ : nuw1
                                                                          1
  return z <u 1                    2   Discharge UB branches                                                                      · cases h₂ : nuw2
                                                                   C1          ¬C1                                                  · cases hs : Sign
                                   Discharge UB branches            2           1                                                     -- Insert Proof Holes:
                                   with deterministic rules                                                                           · have hval := value_hole a b h0 h₁ h₂ hs
                                                                          C2              ¬C2
                                                                                                                                        have hsafe := target_ub_hole a b h0 h₁ h₂ hs
   Goal:                           3   Insert Proof Holes
                                                                          2                 1
                                                                                                                 Refinement             simp_all
                                                                                C3                  ¬C3                       ...
   ∀ w ∈ ℕ, w > 0:                  Insert value and target-                        2                1
                                                                                                                 3
                                                                                                                  Scaffold
                                                                                                                              -- Discharge UB branches automatically
                                    specific UB holes for the
   src(w) ⊒ tgt(w)                  LLM.
                                                                                            C4             ¬C4
                                                                                                                                  Lean Proof Check
                                                                                                2                                                                  Axiom Audit


                           Figure 2. An illustrative example of refinement proof generation in Trivet.

the obligation because any target behavior is permitted [26].                               • Hard Rules. To preserve proof integrity, the prompt ex-
For poison, it discharges the obligation once target imme-                                    plicitly forbids changes to the refinement theorem state-
diate UB is ruled out, as the target may yield either poison                                  ment or the source and target definitions.
or a well-defined value [30]. For a well-defined value, Trivet
leaves one hole for value equality and separate holes to rule                               3.2          Counterexample Proof Generation
out each target-specific UB-triggering circumstance. Finally,
                                                                                            The counterexample branch refutes invalid transformations
Trivet validates the scaffold’s syntactic and type correctness
                                                                                            by turning a candidate counterexample into a proof of non-
using Lean.
                                                                                            refinement. Because refinement quantifies universally over
3.1.3 LLM-Driven Proof Completion. Trivet asks the                                          all admissible bitwidths and inputs, a single counterexample
LLM to fill the remaining typed holes with proofs of value                                  suffices to disprove it. The LLM is restricted solely to propos-
equivalence and the absence of target-specific UB. A candi-                                 ing a candidate counterexample with concrete bitwidths and
date proof is accepted when it satisfies the following condi-                               input values, after which a deterministic scaffold constructs
tions:                                                                                      the complete Lean proof. Because this scaffold introduces
                                                                                            no additional axiomatic dependencies, we omit the axiom
1. the completed proof passes kernel checking;                                              audit from § 3.1.3. The proof is accepted once it passes Lean
2. the proof contains neither sorry nor admit;                                              kernel type-checking.
3. the proof depends exclusively on the standard axioms [54];
   and                                                                                      3.2.1 Illustrative Example. Figure 3 illustrates the coun-
4. the source and target definitions and the theorem state-                                 terexample proof generation in Trivet using an incorrect
   ment remain unchanged.                                                                   generalization of a real-world LLVM transformation [22, 43].
Prompt Design.         The prompt template comprises three                                  This transformation involves two symbolic bitwidths satis-
core elements.                                                                              fying 0 < 𝑤 1 < 𝑤 2 , where inputs 𝑥 and 𝐶 2 are of width 𝑤 1 ,
                                                                                            whereas 𝐶 1 is of width 𝑤 2 :
• System and Task. The prompt assigns the LLM the role                                         𝐶 2 = 𝑤 1 − 1 ⊨ (0 − zext(𝑥 ≫u 𝐶 2 )) & (𝐶 1 − sext(𝑥))
  of a Lean theorem prover and identifies the target proof                                      |                           {z                      }
                                                                                                                       src (𝑤1 ,𝑤2 )
  file. It instructs the LLM to finish the proof by replacing
                                                                                                   =⇒ 𝑥 <s (1 ≪ (𝐶 2 + 1)) ? (𝐶 1 − sext(𝑥)) : 0.
                                                                                                                                 
  the sorry placeholders with valid proofs.                                                            |                     {z                  }
• Instructions. The prompt instructs the LLM to inspect                                                                            tgt (𝑤1 ,𝑤2 )
  proof goals and retrieve diagnostics. The prompt also spec-                               The source constructs a mask from the sign bit of 𝑥, whereas
  ifies that the LLM may add auxiliary lemmas and raise re-                                 the target replaces this mask with a signed comparison and a
  source limits, such as maxHeartbeats and maxRecDepth,                                     conditional selection. The counterexample goal is to establish
  when necessary.                                                                           that there exist admissible bitwidths for which the source is
                                                                               Chunhao Liao, Hongxu Xu, Xintong Zhou, Yizhou Zhang, and Chengnian Sun



          Transformation                                    (i) LLM-based Cx Proposal                                (iii) Complete Cx Proof
  src:                                                    Counterexample Value         x=1, C1=0, C2=1            -- Set up Comparison Rules
  Inputs x: w1, C1: w2, C2: w1                            Counterexample Width         w1=2, w2=3                 local instance : Decidable (a ⊒ b) := …

  bw1: w1 = constant w1                                                                                           -- Certify the Cx
  w_minus_1: w1 = sub bw1, 1                              (ii) Scaffold-based Cx Proof                            theorem verify_cx :
  same: i1 = (C2 == w_minus_1)                                                     1    Comparison Rules             ¬ (src 2 3 ⊒ tgt 2 3) := by
                                           1       Set up Comparison Rules                                        -- To prove ¬P, assume P and derive False.
  assume same                                                                          Per-case decision for ⊒;
                                           Deciding refinement between                                             intro h
  xLshr: w1 = lshr x, C2                                                               Decidable (a ⊒ b)
                                           different outcomes (well-defined                                       -- Instantiate h with the Cx input.
  negMask: w2 = sub 0, zext(xLshr)
  sub: w2 = sub C1, sext(x)                value / poison / immediate UB)          2    Certify the Cx             have hyp := h cxInput
  result: w2 = and negMask, sub                                                        Assumption:                -- Move the instantiated hypothesis
                                                                                       src(w1=2, w2=3) ⊒          -- back into the goal.
  return result                             2      Certify the Cx
                                                                                       tgt(w1=2, w2=3)             revert hyp
                                           Assume refinement, instantiate it           At input:
  tgt:                                     at the Cx input, and let the kernel                                    -- Evaluates both programs and refutes it
  Inputs x: w1, C1: w2, C2: w1                                                         x=1, C1=0, C2=1             decide
                                           check it.                                   Kernel check:
                                                                                       Does 0 ⊒ poison hold? No
  sub: w2 = sub C1, sext(x)                                                                                       -- Refute Refinement
  threshold: w1 = shl 1, (C2 + 1)              3   Refute Refinement               3    Refute Refinement         theorem refute_refinement :
  cond: i1 = (x <s threshold)               Apply the certified Cx to refute                                         ∃ (w1 w2 : Nat) (h : w1 < w2) (h1 : 0 < w1),
                                                                                  Cx width: w1=2, w2=3
  result: w2 = select cond, sub, 0          the refinement.                                                           ¬ (src w1 w2 ⊒ tgt w1 w2) :=
                                                                                 Condition: w1 < w2 ✓ w1 > 0 ✓
  return result                                                                                                    ⟨2, 3, by decide, by decide, verify_cx⟩

                                          Goal: ∃ w1 w2: ℕ , (w1 < w2) ∧ (w1 > 0):
       *Cx: Counterexample                                                                                                   Lean Proof Check
                                          ¬(src(w1, w2) ⊒ tgt(w1, w2))


                         Figure 3. An illustrative example of counterexample proof generation in Trivet.

not refined by the target:                                                         a new candidate. This process repeats until Lean verifies a
∃𝑤 1, 𝑤 2 ∈ N, 0 < 𝑤 1 < 𝑤 2 : ¬ src(𝑤 1, 𝑤 2 ) ⊒ tgt (𝑤 1, 𝑤 2 )
                                                                                  proof of non-refinement or five attempts have been made.
                                                                                   Prompt Design. The prompt template follows the same
   The counterexample proof process comprises three stages.
                                                                                   structure as the refinement prompt in § 3.1.3.
First, the LLM proposes a candidate with bitwidths 𝑤 1 = 2
and 𝑤 2 = 3 and input values 𝑥 = 1, 𝐶 1 = 0, and 𝐶 2 = 1, as                       • System and Task. The prompt assigns the LLM the role
shown in Figure 3 (i). Second, the scaffold constructs a formal                      of a counterexample generator. It asks the LLM to find a
proof of non-refinement from this candidate (Figure 3 (ii)).                         counterexample that violates the refinement claim.
To enable proof by computation, the scaffold provides a com-                       • Instructions. The prompt instructs the LLM to propose a
putable Decidable instance for 𝑎 ⊒ 𝑏, covering well-defined                          counterexample by assigning concrete values to the sym-
values, poison, and immediate UB. This instance allows the                           bolic bitwidths and inputs. If a candidate cannot be certi-
Lean kernel to check that the concrete source and target                             fied, the next prompt includes the Lean diagnostics and
outcomes violate refinement, thereby certifying the coun-                            asks the LLM to propose a new counterexample candidate.
terexample. To establish the contradiction, the scaffold as-                       • Hard Rules. The LLM must save one candidate to the
sumes src(2, 3) ⊒ tgt (2, 3), specializes this assumption to the                     designated file as JSON, with complete bitwidths and
proposed counterexample inputs, and invokes kernel eval-                             inputs objects and no extra text. Before returning, it must
uation. The source evaluates to a well-defined 0, whereas                            check all constraints and confirm that the instantiated
the target evaluates to poison under LLVM semantics [29]                             target function does not refine its source function.
because shl 1, 2 shifts a two-bit value by its bitwidth. The
                                                                                   3.2.3 Scaffold-Based Proof Construction. Given a can-
kernel therefore refutes 0 ⊒ poison. Together with proofs of
                                                                                   didate counterexample proposed by the LLM, Trivet deter-
the instantiated width constraints 𝑤 1 < 𝑤 2 (i.e., 2 < 3) and
                                                                                   ministically synthesizes a proof of non-refinement in two
0 < 𝑤 1 (i.e., 0 < 2), this fixed-width contradiction refutes the
                                                                                   steps:
refinement theorem. Finally, Trivet accepts the proof once it
                                                                                   Contradiction via Decidable Evaluation. The scaffold
passes Lean kernel type-checking.
                                                                                   assumes the claimed refinement theorem for contradiction
                                                                                   and specializes it with the proposed bitwidths and input val-
                                                                                   ues. To evaluate the resulting concrete proposition, Trivet
3.2.2 LLM-Driven Counterexample Proposal. Trivet                                   leverages a Decidable instance of the refinement relation
asks the LLM to propose a candidate counterexample with                            (𝑎 ⊒ 𝑏) that formalizes comparisons across well-defined val-
concrete bitwidths and input values. If Trivet fails to refute                     ues, poison, and immediate UB. Kernel evaluation reduces the
the refinement theorem using the candidate, it appends the                         source and target expressions to concrete semantic outcomes;
Lean diagnostics to the prompt and asks the LLM to generate                        because these outcomes violate refinement (e.g., deriving
LLVM Translation Validation Automated with Large Language Models and Lean


0 ⊒ poison), the decision procedure reduces the proposition                   src:                                   tgt:
to False.                                                                     Inputs n, a, b: i64
                                                                              Entry:
                                                                                                                     Inputs n, a, b: i64
                                                                                                                     Entry:
Precondition Discharge and Verification. The scaffold                          p: i64 = mul nuw a, b                  p: i64 = mul nuw a, b
                                                                               pnz: i1 = icmp ne p, 0                 res: i64 = udiv n, p
then discharges the concrete bitwidth constraints (e.g., 0 <                   assume pnz                             return res
𝑤 1 < 𝑤 2 ) via computation, assembling the counterexample                     x: i64 = udiv n, a
                                                                               br Loop(x, 0)
and the contradiction into a complete proof of the negated                                                               Loop elimination by
                                                                                                                        quotient composition
refinement theorem. The final proof contains no remaining                     Loop(x: i64, q: i64):
                                                                               x1: i64 = sub x, b
holes and is validated by Lean kernel type-checking.                           q1: i64 = add q, 1
                                                                               small: i1 = icmp ult x, b
                                                                               cond_br small, Out(q), Loop(x1, q1)
3.3   Loop-Containing Transformations
                                                                              Out(result: i64):
For loop-free transformations, refinement can be established                   return result
by directly comparing the source and target behaviors for all
possible inputs. For transformations involving loops, how-
                                                                            Figure 4. An illustrative example for a loop-containing trans-
ever, the proof must also account for all feasible loop iteration
                                                                            formation
counts, since a loop may execute an arbitrary number of it-
erations depending on the inputs. To address this challenge,
Alive2 applies bounded loop unrolling, checking refinement
only up to a selected unrolling bound and thereby potentially               holes to rule out UB in the target when the source returns a
missing counterexamples that require more iterations [38].                  well-defined value. For well-defined source outcomes, Trivet’s
By contrast, Trivet establishes refinement by induction, yield-             loop-free scaffold uses a single value hole requiring the
ing a single correctness proof that covers all feasible loop                source and target functions to return the same value. In
iteration counts without relying on a fixed unrolling bound.                contrast, for transformations involving loops, Trivet replaces
   In this paper, Trivet provides preliminary support for a                 this single hole with loop-specific holes that jointly specify
restricted class of loop-containing transformations, from a                 the proof obligations for refinement over an arbitrary num-
source function containing LLVM’s canonical loop form [35,                  ber of iterations. Table 1 provides an overview of the general
36] to a loop-free target function with a single basic block.               and loop-specific holes in the refinement scaffold. Finally,
Specifically, the source function consists of three blocks: an              Trivet invokes the LLM to provide the loop invariant and
entry preheader, a single self-looping body block with one                  fill the proof holes in the scaffold and checks the completed
back edge, and a dedicated exit block that returns imme-                    proof following the same procedure in § 3.1.3.
diately. This fixed topology enables Trivet to reuse a fixed                Illustrative Example. Figure 4 shows an illustrative loop-
proof scaffold and is grounded in practice: canonical loop                  containing transformation that replaces a quotient computa-
form is enforced before the loop-pass execution, and the                    tion by repeated subtraction with an unsigned division. The
single-block, single-back-edge form is targeted by several                  source loop implements Euclidean division [7]: for 𝑥, 𝑏 ∈ N
loop idiom recognizers [34, 35].                                            with 𝑏 > 0, the unique quotient–remainder pair (𝑞, 𝑟 ) satis-
   For general loop-containing transformations, however, the                fies 𝑥 = 𝑞 · 𝑏 + 𝑟 and 0 ≤ 𝑟 < 𝑏, where 𝑞 = ⌊𝑥/𝑏⌋ counts the
proof scaffold varies with the source function’s control-flow               subtractions. Starting from x = udiv n, a and 𝑞 = 0, the
graph (CFG). This variation arises because inductive proofs                 source repeatedly updates (𝑥, 𝑞) to (𝑥 − 𝑏, 𝑞 + 1) while 𝑥 ≥ 𝑏
require every cycle in the CFG to pass through an invariant-                and then returns 𝑞. It thus computes ⌊⌊𝑛/𝑎⌋/𝑏⌋ = ⌊𝑛/(𝑎 ·𝑏)⌋,
bearing cutpoint [12], resulting in CFG-specific invariants                 which the target computes directly using udiv n, p, where
and induction obligations. Accordingly, we leave support for                𝑝 = 𝑎 · 𝑏.
general loop structures to future work.                                     Refinement Proof for the Example. Trivet’s refinement
                                                                            proof scaffold first applies the case decomposition process
3.3.1 Loop-Aware Refinement Scaffold and Proof Gen-
                                                                            to discharge the source entry block’s poison and immediate
eration. Following the loop-free workflow in § 3.1, Trivet
                                                                            UB cases (e.g. 𝑝 = 0 violates assume pnz). For the remaining
first constructs a loop-aware scaffold by extending the loop-
                                                                            cases, the scaffold leaves target-specific UB obligations and
free scaffold in § 3.1.2 to loop-containing transformations
                                                                            three loop-specific holes:
and then invokes the LLM to fill the proof holes and complete
the proof.                                                                  1. Target-specific UB. Proofs that the target’s mul nuw cannot
   For loop-containing transformations, Trivet reuses the                      overflow and that 𝑝 ≠ 0 for udiv n, p.
loop-free scaffold’s case decomposition, refinement rules,                  2. Loop invariant. A predicate 𝐼 (𝑛, 𝑎, 𝑏, 𝑥, 𝑞) relating the tgt
and target-specific UB holes. In the source entry block, it                    inputs (𝑛, 𝑎, and 𝑏) to the src loop state (𝑥, and 𝑞).
splits cases and automatically applies the refinement rules to              3. Inductive step. A proof that 𝐼 is preserved by (𝑥, 𝑞) ↦→
discharge obligations for poison and immediate UB outcomes.                    (𝑥 − 𝑏, 𝑞 + 1) when 𝑥 ≥ 𝑏 and implies 𝑞 = ⌊𝑛/𝑝⌋ when
For the target function, Trivet generates target-specific UB                   𝑥 < 𝑏.
                                                                             Chunhao Liao, Hongxu Xu, Xintong Zhou, Yizhou Zhang, and Chengnian Sun


Table 1. General and loop-specific holes in the preliminary                      3.4   Implementation and Limitations
loop-containing scaffold.                                                        We build Trivet on top of the LLVM dialect in Lean-MLIR [6],
                                                                                 a Lean 4 framework that formalizes the semantics of MLIR
   Type      Hole and Role                                                       programs: it parses MLIR code into well-typed Lean terms
  General    • Target-specific UB: rules out each relevant target-side UB        with precise per-operation semantics, so that properties of
                condition whenever the source is defined.                        MLIR programs become Lean theorems. Using MLIR’s trans-
             • Loop invariant: summarizes the reachable source-loop              lation mechanisms [42], LLVM IR converts bidirectionally
   Loop-                                                                         to and from the LLVM dialect without loss of semantic in-
                state and function inputs.
  specific                                                                       formation [41].
             • Inductive step: preserves the invariant and proves equality
                with the target result at loop exit.                                However, Lean-MLIR originally modeled only a simplified
                                                                                 subset of the LLVM dialect. To enable translation validation
             • Final assembly: establishes the invariant at loop entry,
                                                                                 of real-world transformations, we extended it along three
                then uses the inductive proof to establish refinement for
                any number of loop iterations.                                   dimensions: 1 refining its semantic foundations to support
                                                                                 immediate UB and transformation preconditions, 2 adding
                                                                                 missing bit-manipulation operators (e.g. ctpop, cttz, ctlz),
                                                                                 and 3 generalizing the framework to multiple symbolic-
4. Final assembly. A proof establishing 𝐼 at loop entry, where                   bitwidth parameters and multi-block transformations.
   (𝑥, 𝑞) = ( ⌊𝑛/𝑎⌋, 0), and using the inductive step to show                       In Trivet, the LLM operates as an agent: we use the Codex
   that the source loop’s result equals ⌊𝑛/𝑝⌋.                                   CLI [46] with the gpt-5.5 model [48] to perform proof com-
The LLM completes the proof by filling these holes as follows:                   pletion in the refinement branch and counterexample pro-
                                                                                 posal in the counterexample branch. Trivet itself remains
1. Target-specific UB. It uses 𝑎 · 𝑏 < 264 and 𝑝 ≠ 0 from the                    a deterministic harness, accepting the agent’s output only
   source entry conditions to exclude overflow in mul nuw                        after the Lean kernel checks the resulting proof.
   and division by zero in udiv n, p.                                               Our formalization currently targets integer instructions,
2. Loop invariant. It defines 𝐼 to require well-defined inputs                   and our workflows support loop-free, single-block trans-
   and loop values, 0 < 𝑎 · 𝑏 < 264 , and 𝑞 + ⌊𝑥/𝑏⌋ = ⌊𝑛/(𝑎 ·                    formations plus a restricted class of loop-containing ones.
   𝑏)⌋. Here, 𝑞 and ⌊𝑥/𝑏⌋ count completed and remaining                          Extending the formalization to memory operations, floating-
   subtractions, respectively.                                                   point arithmetic, and richer loop classes is left as future
3. Inductive step. On the back edge (𝑥 ≥ 𝑏), it derives 𝑞 + 1 <                  work.
   264 from 𝐼 , so neither 𝑥 − 𝑏 nor 𝑞 + 1 wraps. It then uses
   ⌊𝑥/𝑏⌋ = 1+ ⌊(𝑥 −𝑏)/𝑏⌋ to prove that (𝑥, 𝑞) ↦→ (𝑥 −𝑏, 𝑞+1)                     4     Evaluation
   preserves 𝐼 . At exit (𝑥 < 𝑏), ⌊𝑥/𝑏⌋ = 0 gives 𝑞 = ⌊𝑛/𝑝⌋,
   matching the target result.                                                   This section presents our extensive evaluation of Trivet,
4. Final assembly. At loop entry, 𝑥 = ⌊𝑛/𝑎⌋ and 𝑞 = 0. The                       demonstrating its effectiveness in automating translation
   source entry conditions and the identity ⌊⌊𝑛/𝑎⌋/𝑏⌋ =                          validation for LLVM transformations. We organize our eval-
   ⌊𝑛/(𝑎 · 𝑏)⌋ establish 𝐼 for this initial state. The LLM com-                  uation around four research questions:
   bines this initialization proof with the inductive step to                    • RQ1: Can Trivet effectively validate real-world valid LLVM
   prove refinement for any number of loop iterations.                              transformations?
                                                                                 • RQ2: Can Trivet effectively refute real-world invalid LLVM
Trivet checks the completed proof following § 3.1.3.
                                                                                    transformations?
3.3.2 Loop-Aware Counterexample Certification. The                               • RQ3: Can Trivet effectively validate and refute loop-containing
counterexample branch extends the loop-free workflow in                             LLVM transformations derived from real-world cases?
§ 3.2. The LLM proposes a counterexample candidate with                          • RQ4: What is the impact of Trivet’s scaffold on refinement
concrete bitwidths, inputs, and an execution bound that lim-                        and counterexample proof generation?
its the loop iteration count and ensures evaluation terminates.                     We intentionally separate loop-free (RQ1 and RQ2) and
The scaffold accepts a counterexample candidate only if the                      loop-containing transformations (RQ3) because Alive2 offers
loop execution completes within this bound. Otherwise, the                       different guarantees. For loop-free transformations, Alive2
scaffold rejects the candidate and requests a new one. Given                     can validate them under its modeled semantics, while for
this candidate, Trivet reuses the deterministic stages from                      loop-containing transformations, it only provides bounded
§ 3.2.3: decidable comparison of execution outcomes, certifi-                    guarantees due to its finite loop unrolling [38].
cation of the concrete candidate, and construction of a proof                    Setup. All experiments were conducted on an Ubuntu
of non-refinement from the certified counterexample. Follow-                     22.04 (64-bit) server equipped with a 32-core Intel Xeon Gold
ing the loop-free workflow in § 3.2, Trivet allows at most five                  5217 CPU @ 3.00GHz and 376 GB of RAM. We applied a time
counterexample generation attempts per transformation.                           limit of two hours per transformation across all RQs. Since
LLVM Translation Validation Automated with Large Language Models and Lean


                  Table 2. Dataset Composition                                  Table 3. Trivet versus Alive2 on 60 valid transformations.

                                            Bitwidth                                                                                                   Trivet                          Alive2
      Loop Structure    RQ    Validity   Fixed   Symbolic   Total             Stratum                                          𝑁           Proved          Mean (s)          Proved            Mean (s)
                        RQ1   Valid         30         30      60             Symbolic bitwidth                                30                 30             722               n/a                 n/a
      Loop-free
                        RQ2   Invalid       30         30      60             Fixed bitwidth                                   30                 30             647                20                 206
                        RQ3   Valid          7          7      14             Total                                            60                 60             684                   20              206
      Loop-containing
                        RQ3   Invalid        7          7      14
      Overall           –     –             74         74     148                                                  Symbolic Bitwidth                                      Fixed Bitwidth
                                                                                                                                              1748 s                                        2635 s
                                                                                                 100%
                                                                                                          Trivet: 30/30                                                                     Trivet: 30/30




                                                                            Fraction validated
                                                                                                 75%      Alive2: n/a
                                                                                                                                      895 s                                      758 s
                                                                                                                           602 s
Trivet does not support undef for the reasons discussed in                                       50%                                                                484 s                   Alive2: 20/30

§ 2.1, we ran Alive2 with –disable-undef-input; this con-                                        25%
                                                                                                                  333 s
                                                                                                                                   Trivet: 138–1748 s
                                                                                                                                                                 344 s
                                                                                                                                                                                    Trivet: 197–2635 s
figuration ensures a fair comparison because our dataset has                                      0%
                                                                                                                                           Alive2: n/a                            Alive2: 0.032–7200 s

no other mechanism for introducing undef. As the under-                                                 100          300              1k                3k 100     300            1k            3k     7.2k

lying LLM, Trivet uses gpt-5.5 with extra-high reasoning                                                             Validation time (s)                                 Validation time (s)

effort.
                                                                             Figure 5. Validation time distributions for RQ1 (log scale).
4.1    Dataset
Our dataset comprises 148 real-world LLVM transformation                    4.2                          RQ1: Validating Transformations
instances from the LLVM GitHub repository. Table 2 summa-                   In RQ1, we investigate whether Trivet can establish refine-
rizes their distribution by loop structure, validity, bitwidth,             ment for real-world LLVM transformations and compare its
and research question.                                                      validation capability with Alive2. Table 3 summarizes the
Loop-Free Dataset. The loop-free dataset contains fixed-                    aggregate results for both systems on the same 60 transfor-
and symbolic-bitwidth cases.                                                mations and Figure 5 shows the validation-time distributions.
   In the fixed-bitwidth portion, Alive2 proves the 15 valid
cases and refutes the 15 invalid cases within its standard                  4.2.1 Experimental Results. Trivet validates all 60 trans-
10 s time limit. The remaining 15 valid cases and 15 invalid                formations, with median and mean validation times of 522 s
cases involve nonlinear bit-vector operations, interdepen-                  and 684 s, respectively. Alive2 applies only to the 30 fixed-
dent preconditions, and relatively large but common con-                    bitwidth transformations and validates 20; the remaining 10
crete bitwidths (e.g. i32 and i64). These structures make it                runs do not complete within the time limit.
challenging for SMT-based methods such as Alive2 to finish                     For the symbolic-bitwidth cases, Trivet validates all 30
within the standard 10 s time limit [45]. We include these                  cases in 138–1748 s, with a median of 614 s and a mean of
cases to assess whether Trivet can validate or refute trans-                722 s. Each generated theorem is parametric in the bitwidth
formations that are challenging for SMT-based methods.                      and establishes refinement for every width satisfying the
   In the symbolic-bitwidth portion, we derive each valid case              required constraints (e.g. 𝑤 mod 2 = 0). Since Alive2 does
by applying the transformation-generalization techniques                    not support transformations with symbolic bitwidths, Table 3
developed in prior work [21, 43] to its fixed-bitwidth coun-                reports “n/a” for these cases.
terpart. We manually construct each invalid case from its                      For the fixed-bitwidth cases, Alive2 takes less than 1 s to
fixed-bitwidth counterpart by replacing the concrete integer                validate each of the 15 cases, whereas Trivet validates the
bitwidth with a symbolic one, because these techniques do                   same cases with a median of 463 s and a mean of 487 s. In
not support the generalization of invalid transformations.                  the remaining 15 challenging cases, Alive2 validates only
                                                                            5 within the time limit of two hours; its successful runs
Loop-Containing Dataset. The loop-containing dataset
                                                                            have a median of 941 s and a mean of 823 s. In contrast,
comprises 14 valid and 14 invalid transformations. Each
                                                                            Trivet validates all 15 challenging cases in 207–1257 s, with a
group contains equal numbers of fixed- and symbolic-bitwidth
                                                                            median of 492 s. Overall, Alive2 is faster on the 15 cases but
cases. Each transformation replaces a three-basic-block source
                                                                            validates only a subset of the 15 challenging cases, whereas
function with a loop-free target function with a single ba-
                                                                            Trivet validates all fixed-bitwidth cases.
sic block. We derive each symbolic-bitwidth case from its
fixed-bitwidth counterpart by manually replacing the con-                   4.2.2 Result Analysis. The symbolic-bitwidth results show
crete integer bitwidth with a symbolic one because prior                    that a single Trivet proof establishes refinement for all ad-
transformation-generalization techniques [21, 43] do not                    missible widths rather than for one concrete instantiation,
support loop-containing transformations.                                    providing a width-independent guarantee outside Alive2’s
                                                                                                                                Chunhao Liao, Hongxu Xu, Xintong Zhou, Yizhou Zhang, and Chengnian Sun


Table 4. Trivet versus Alive2 on 60 invalid transformations.                                                                        4.3     RQ2: Refuting Invalid Transformations
                                                                                                                                    In RQ2, we investigate whether Trivet can refute real-world
                                                              Trivet                                  Alive2                        invalid LLVM transformations and compare its refutation
Stratum                                 𝑁           Refuted            Mean (s)             Refuted               Mean (s)          capability with Alive2. Table 4 summarizes the aggregate
Symbolic bitwidth                      30                   30                   66                  n/a               n/a          results, while Figure 6 shows the corresponding refutation-
Fixed bitwidth                         30                   30                   56                   29                47          time distributions.
Total                                  60                   60                   61                   29                   47
                                                                                                                                    4.3.1 Experimental Results. Trivet produces certified
                                                                                                                                    refutations for all 60 invalid transformations, with a mean
                              Symbolic Bitwidth                                           Fixed Bitwidth                            refutation time of 61 s. Candidate generation accounts for
                   100%
                                                         204 s                                                210 s                 47 s (77%), while scaffold-based certification accounts for 14 s
                                                    Trivet: 30/30
                                                     Alive2: n/a
                                                                              Trivet: 30/30                                         (23%). For the symbolic-bitwidth transformations, Trivet re-
                   75%
fraction refuted




                                                                              Alive2: 29/30
                                       69 s                                                                 69 s
                                                                                                                                    futes all 30 cases in 32–204 s, with a median of 56 s and a
                                                                                                     46 s
                   50%        56 s
                                                                                                                                    mean of 66 s. For each case, the LLM proposes a counterex-
                           44 s                                                                34 s
                   25%
                                                Trivet: 32–204 s              Trivet: 31–210 s                                      ample candidate containing concrete bitwidths and input
                    0%
                                                     Alive2: n/a              Alive2: 0.08–1023 s                                   values, which the scaffold automatically certifies. For the
                      20          50          100                300    0.1           1         10          100       1k            fixed-bitwidth transformations, Trivet refutes all 30 cases in
                              Refutation Time (s)                                     Refutation Time (s)                           31–210 s, with a median of 46 s and a mean of 56 s. In con-
                                                                                                                                    trast, Alive2 refutes 29 and times out on the remaining one.
Figure 6. Refutation time distributions for RQ2 (log scale).                                                                        Successful runs take 0.08–1023 s, with a median of 0.103 s
                                                                                                                                    and a mean of 47 s.

supported scope. For fixed bitwidths, Alive2 exhibits a perfor-                                                                     4.3.2 Result Analysis. The symbolic-bitwidth results show
mance cliff as proof difficulty increases. Similarly, the original                                                                  that Trivet can refute a width-parametric transformation
Alive2 study found that extending the timeout from one to                                                                           by certifying a counterexample that instantiates both the
five minutes yielded less than 5% additional results [38]. By                                                                       bitwidth and inputs, extending coverage beyond Alive2’s
contrast, Trivet exhibits more consistent runtimes across the                                                                       scope. For fixed bitwidths, Alive2 is faster on most cases
fixed-bitwidth cases.                                                                                                               but still exhibits a pronounced long tail and leaves one case
   The performance cliff stems primarily from two factors:                                                                          unresolved after two hours, consistent with its behavior on
Alive2’s whole-function refinement formulation and the bit-                                                                         valid transformations in § 4.2. In contrast, Trivet has more
blasting in the SMT solver. Alive2 encodes the complete                                                                             concentrated runtimes and refutes every case.
source and target functions rather than decomposing vali-
dation into smaller independent obligations, producing in-
                                                                                                                                    4.4     RQ3: Loop-Containing Transformations
creasingly difficult queries as the transformations grow more
complex. Moreover, this difficulty is exacerbated by the bit-                                                                       Table 5 summarizes the experimental results for the 28 in-
blasting mechanism, especially for transformations involving                                                                        stances. Trivet provides refinement proofs for all valid cases
nonlinear operators (e.g. div, mul, and urem). Although bit-                                                                        at both fixed and symbolic bitwidths. The symbolic proofs
blasting enables automated reasoning via SAT, expanding                                                                             establish correctness for all widths and inputs, with median
𝑤-bit operations into Boolean circuits obscures their alge-                                                                         and mean proof-generation times of 1471.2 s and 1673.5 s.
braic structure and makes particular arithmetic operations                                                                          The fixed-width runs have corresponding times of 1741.7 s
expensive to solve [4, 14, 45]. In contrast, Trivet leverages the                                                                   and 1821.7 s. Fixed-width refutation certifies 6/7 invalid cases,
LLM’s algebraic reasoning capabilities to decompose com-                                                                            with a median time of 211.1 s. Symbolic-width refutation
plex proof obligations, completing the proof step by step,                                                                          certifies all 7 invalid cases, with a median of 87.5 s. Each
thereby avoiding this performance cliff.                                                                                            symbolic counterexample specifies concrete inputs and a
   Prior work shows that bit-blasting can be extremely ex-                                                                          bitwidth. We omit Alive2 because it does not support sym-
pensive at common bitwidths such as 32 bits [45]; whole-                                                                            bolic bitwidths and establishes correctness only within a
function refinement checking can further amplify this cost.                                                                         user-configurable unrolling bound, rather than proving the
For                                                                                                                                 transformation correct for all loop iteration counts [38].
   example, consider a simple transformation (𝑥/u𝑦) · 𝑦 ≤                                                                             For the unresolved invalid transformation, Trivet exhausted
𝑥 =⇒ true, where /u denotes unsigned integer division.
Although this transformation is clearly valid under LLVM                                                                            its counterexample candidate attempts after 306 s without
semantics, Alive2 times out on its i32 instance after two                                                                           finding a certified counterexample. With 𝑥, 𝑛, 𝑎𝑖 : i32, the
hours, whereas Trivet validates the same i32 instance in                                                                            transformation replaces a loop with a multiplication:
339 s.                                                                                                                                    𝑎 0 = 0,   𝑎𝑖+1 = 𝑎𝑖 + 𝑥,   return 𝑎𝑛 → return(𝑥 × 𝑛).
LLVM Translation Validation Automated with Large Language Models and Lean


Table 5. RQ3 results for loop-containing transformations.                                 These results are consistent with scaffolding reducing
                                                                                       proof generation overhead. We observe that generating proofs
  Bitwidth    Task             𝑁     Succeeded        Median (s)        Mean (s)       from scratch can be inefficient due to extensive tactic explo-
  Symbolic    Validation        7                7            1471.2      1673.5       ration and repeated proof attempts, with loose proof struc-
  Fixed       Validation        7                7            1741.7      1821.7       ture and diverse UB cases adding further complexity. In con-
  Symbolic    Refutation        7                7              87.5        88.6       trast, the scaffold guides the LLM through well-defined sub-
  Fixed       Refutation        7                6             211.1       207.8       goals, yielding proofs with a clearer logical structure.

Table 6. Scaffold ablation results. Mean runtimes are in sec-
onds for successful cases in both configurations. The column                           4.5.2 Monetary Cost. We report per-transformation proof-
Δ is the cost reduction from Trivet− to Trivet.                                        generation costs based on OpenAI’s pricing as of September
                                                                                       2026 [47]. For loop-free transformations, mean costs decrease
              Successful            Mean Runtime (s)           Mean Cost (USD)         from $13.23 to $1.47 for the 47 valid cases and from $3.15 to
Bitwidth 𝑁 Trivet− Trivet Trivet− Trivet Speedup Trivet− Trivet                    Δ   $0.08 for the 49 invalid cases, corresponding to reductions of
                           Refinement proofs (loop-free)                               88.9% and 97.5%, respectively. For loop-containing transfor-
Symbolic 30     24         30    3265.9 760.6          4.3×    $13.93   $1.48 89.4%
Fixed    30     23         30    2791.6 634.3          4.4×    $12.49   $1.45 88.4%    mations with complete usage records, mean costs decrease
Total    60     47         60    3033.8 698.8          4.3×    $13.23   $1.47 88.9%    from $12.7 to $2.93 for refinement proofs and from $2.29 to
                     Counterexample proofs (loop-free)                                 $0.24 for counterexample proofs.
Symbolic 30     25     30     907.4    64.2      14.1×          $2.80   $0.08 97.1%
Fixed    30     24     30      934       58      16.1×          $3.52   $0.08 97.7%
Total    60     49     60     920.4    61.1      15.1×          $3.15   $0.08 97.5%
                     Refinement proofs (loop-containing)
Symbolic 7       6        7   2784.5 1446.6         1.9 ×      $12.06   $2.76 77.1%    5   Related Work
Fixed     7      6        7   3042.1 1603.4         1.9 ×      $13.35   $3.10 76.8%
Total    14     12       14   2913.3     1525       1.9 ×       $12.7   $2.93 76.9%    We review the following three areas related to Trivet.
                   Counterexample proofs (loop-containing)                             Translation Validation. Translation validation checks
Symbolic 7       7       7    697.2      88.6      7.9 ×        $2.20   $0.12 94.5%
Fixed     7      6       6    842.4 207.8          4.1 ×        $2.40   $0.37 84.6%
                                                                                       individual compiler runs or transformations rather than veri-
Total    14     13      13   764.22 143.62         5.3 ×        $2.29   $0.24 89.7%    fying the compiler implementation [1, 44, 49]. Equality-based
                                                                                       approaches use equality saturation or normalized value graphs
                                                                                       to check LLVM and MLIR transformations [50, 56, 61]. Alive [39]
For x=poison, n=0, the source executes no loop iterations,                             and Alive2 [38] provide SMT-based refinement checking for
leaving the accumulator at its initial value of zero. The tar-                         LLVM. AliveInLean follows this design by verifying its con-
get instead evaluates x * n, which propagates poison. Al-                              dition generator in Lean but still relies on an SMT solver,
though the arithmetic identity holds for defined operands,                             whereas Crellvm checks compiler-emitted proofs with a Coq-
the rewrite introduces a dependence on x into the source’s                             verified validator [15, 19]. Trivet instead uses an LLM to
otherwise constant return value when n=0.                                              synthesize per-transformation Lean proofs checked by the
4.5   RQ4: Ablation Study                                                              kernel.
                                                                                       LLMs for Compilers. Recent work applies LLMs to com-
In RQ4, we assess the contribution of the scaffold by com-
                                                                                       piler optimization and debugging. For optimization devel-
paring Trivet with its unscaffolded variant Trivet− , which
                                                                                       opment, LPO [58] discovers formally verified peephole opti-
requires the LLM to generate complete Lean proofs from
                                                                                       mizations, while LPG [21] generalizes concrete optimiza-
scratch. Keeping all other experimental settings fixed and
                                                                                       tions into reusable rules. Recent studies evaluate agents
evaluating on the RQ1–RQ3 datasets, we measure proof suc-
                                                                                       implementing LLVM optimizations [13, 57]. For compiler
cess rate, runtime, and monetary cost in the ablation study.
                                                                                       debugging, LPR and subsequent agentic work minimize bug-
4.5.1 Success Rate and Runtime. For loop-free transfor-                                triggering programs [63, 66]. By contrast, Trivet uses an LLM
mations, Table 6 shows that Trivet completes all refinement                            to construct correctness or counterexample proofs for a given
and counterexample proofs. In contrast, Trivet− succeeds on                            transformation, with Lean checking the result.
47 of 60 refinement cases and 49 of 60 counterexample cases.                           LLMs for Interactive Theorem Proving. LLMs have been
Among cases successfully completed by both configurations,                             used to automate proof construction in interactive theorem
Trivet is faster in every case. The speedups in mean runtime                           provers. LeanDojo and Rango use retrieval augmentation
are 4.3× for refinement and 15.1× for counterexamples. For                             for Lean and Rocq, respectively [55, 59]. COPRA combines
loop-containing transformations, Trivet− and Trivet prove                              stateful search with prover feedback, while PALM itera-
12 and 14 of 14 valid instances, respectively, and refute 13 and                       tively repairs generated proofs [40, 53]. Trivet applies LLM-
13 of 14 invalid instances. Among cases solved by both con-                            based proof synthesis to LLVM translation validation, using a
figurations, the ratios of baseline to scaffolded mean runtime                         domain-specific scaffold to produce machine-checked proofs
are 1.9 × for refinement and 5.3 × for counterexamples.                                in Lean.
                                                                                   Chunhao Liao, Hongxu Xu, Xintong Zhou, Yizhou Zhang, and Chengnian Sun


6    Conclusion                                                                             – CADE 28: 28th International Conference on Automated Deduction,
                                                                                            Virtual Event, July 12–15, 2021, Proceedings. Springer-Verlag, Berlin,
This paper presents Trivet, a framework integrating LLMs                                    Heidelberg, 625–635. doi:10.1007/978-3-030-79876-5_37
and Lean for automated LLVM translation validation. By                                 [12] Robert W Floyd. 1993. Assigning meanings to programs. In Program
combining deterministic scaffolds, LLM-guided proof syn-                                    Verification: Fundamental Issues in Computer Science. Springer, 65–81.
thesis, and Lean kernel checking, Trivet produces refinement                           [13] Batu Guan, Zirui Wang, and Shaohua Li. 2026. Understand-
and counterexample proofs for fixed and symbolic bitwidths,                                 ing Agent-Based Patching of Compiler Missed Optimizations.
                                                                                            arXiv:2607.02370 [cs.SE] https://arxiv.org/abs/2607.02370
covering loop-free transformations and a restricted class of
                                                                                       [14] Liana Hadarean, Kshitij Bansal, Dejan Jovanović, Clark Barrett, and
loop-containing ones. Our evaluation shows that Trivet vali-                                Cesare Tinelli. 2014. A Tale of Two Solvers: Eager and Lazy Ap-
dates transformations beyond the practical reach of Alive2,                                 proaches to Bit-Vectors. In Computer Aided Verification, Armin Biere
the state-of-the-art SMT-based validator, while scaffolding                                 and Roderick Bloem (Eds.). Springer International Publishing, Cham,
improves proof completion and efficiency.                                                   680–695.
                                                                                       [15] Jeehoon Kang, Yoonseung Kim, Youngju Song, Juneyoung Lee,
                                                                                            Sanghoon Park, Mark Dongyeon Shin, Yonghyun Kim, Sungkeun
References                                                                                  Cho, Joonwon Choi, Chung-Kil Hur, and Kwangkeun Yi. 2018. Crel-
                                                                                            lvm: verified credible compilation for LLVM. In Proceedings of the
 [1] Clark Barrett, Yi Fang, Benjamin Goldberg, Ying Hu, Amir Pnueli, and
                                                                                            39th ACM SIGPLAN Conference on Programming Language Design and
     Lenore Zuck. 2005. TVOC: a translation validator for optimizing com-                   Implementation (Philadelphia, PA, USA) (PLDI 2018). Association for
     pilers. In Proceedings of the 17th International Conference on Computer                Computing Machinery, New York, NY, USA, 631–645. doi:10.1145/
     Aided Verification (Edinburgh, Scotland, UK) (CAV’05). Springer-Verlag,                3192366.3192377
     Berlin, Heidelberg, 291–295. doi:10.1007/11513988_29                              [16] Chris Lattner and Vikram Adve. 2004. LLVM: A Compilation Frame-
 [2] Clark Barrett, Pascal Fontaine, and Cesare Tinelli. 2025. The SMT-LIB                  work for Lifelong Program Analysis & Transformation. In Proceedings
     Standard: Version 2.7. Technical Report. Department of Computer                        of the International Symposium on Code Generation and Optimization:
     Science, The University of Iowa. http://www.SMT-LIB.org                                Feedback-Directed and Runtime Optimization (Palo Alto, California)
 [3] Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia, and Cesare Tinelli.               (CGO ’04). IEEE Computer Society, USA, 75.
     2021. Satisfiability Modulo Theories. In Handbook of Satisfiability               [17] Vu Le, Mehrdad Afshari, and Zhendong Su. 2014. Compiler valida-
     (second ed.), Armin Biere, Marijn Heule, Hans van Maaren, and Toby                     tion via equivalence modulo inputs. In Proceedings of the 35th ACM
     Walsh (Eds.). IOS Press, Chapter 33, 1267–1329.                                        SIGPLAN Conference on Programming Language Design and Imple-
 [4] Max Barth, Matthias Heizmann, and Jochen Hoenicke. 2026. A lazy                        mentation (Edinburgh, United Kingdom) (PLDI ’14). Association for
     and modular approach to int-blasting. Acta Inf. 63, 2 (April 2026),                    Computing Machinery, New York, NY, USA, 216–226. doi:10.1145/
     33 pages. doi:10.1007/s00236-026-00529-y                                               2594291.2594334
 [5] Calvin Beck, Irene Yoon, Hanxi Chen, Yannick Zakowski, and Steve                  [18] Hayley Leblanc, Nathan Taylor, James Bornholt, and Vijay Chi-
     Zdancewic. 2024. A Two-Phase Infinite/Finite Low-Level Memory                          dambaram. 2025. SquirrelFS: Using the Rust Compiler to Check File-
     Model: Reconciling Integer–Pointer Casts, Finite Space, and undef at                   System Crash Consistency. ACM Trans. Storage 21, 4, Article 27 (Nov.
     the LLVM IR Level of Abstraction. Proc. ACM Program. Lang. 8, ICFP,                    2025), 39 pages. doi:10.1145/3769109
     Article 263 (Aug. 2024), 29 pages. doi:10.1145/3674652                            [19] Juneyoung Lee, Chung-Kil Hur, and Nuno P. Lopes. 2019. AliveInLean:
 [6] Siddharth Bhat, Alex Keizer, Chris Hughes, Andrés Goens, and Tobias                    A Verified LLVM Peephole Optimization Verifier. In Computer Aided
     Grosser. 2024. Verifying Peephole Rewriting in SSA Compiler IRs. In                    Verification, Isil Dillig and Serdar Tasiran (Eds.). Springer International
     15th International Conference on Interactive Theorem Proving (ITP 2024)                Publishing, Cham, 445–455.
     (Leibniz International Proceedings in Informatics (LIPIcs), Vol. 309), Yves       [20] Juneyoung Lee, Dongjoo Kim, Chung-Kil Hur, and Nuno P. Lopes.
     Bertot, Temur Kutsia, and Michael Norrish (Eds.). Schloss Dagstuhl –                   2021. An SMT Encoding of LLVM’s Memory Model for Bounded Trans-
     Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 9:1–9:20. doi:10.
                                                                                            lation Validation. In Computer Aided Verification: 33rd International
     4230/LIPIcs.ITP.2024.9                                                                 Conference, CAV 2021, Virtual Event, July 20–23, 2021, Proceedings, Part
 [7] Raymond T. Boute. 1992. The Euclidean definition of the functions div                  II. Springer-Verlag, Berlin, Heidelberg, 752–776. doi:10.1007/978-3-
     and mod. ACM Trans. Program. Lang. Syst. 14, 2 (April 1992), 127–144.                  030-81688-9_35
     doi:10.1145/128861.128862                                                         [21] Chunhao Liao, Hongxu Xu, Xintong Zhou, Zhenyang Xu, and Cheng-
 [8] Tej Chajed, Joseph Tassarotti, Mark Theng, Ralf Jung, M. Frans                         nian Sun. 2026. Leveraging Large Language Models for Gener-
     Kaashoek, and Nickolai Zeldovich. 2021. GoJournal: a verified, con-                    alizing Peephole Optimizations. arXiv:2603.18477 [cs.PL] https:
     current, crash-safe journaling system. In 15th USENIX Symposium                        //arxiv.org/abs/2603.18477
     on Operating Systems Design and Implementation (OSDI 21). USENIX                  [22] LLVM Project. 2022. Missed optimization for -(foo < 0) in Clang
     Association, 423–439. https://www.usenix.org/conference/osdi21/                        when foo was previously sign-extended and in LLVM for all cases.
     presentation/chajed                                                                    https://github.com/llvm/llvm-project/issues/57381
 [9] Yun-Sheng Chang, Ralf Jung, Upamanyu Sharma, Joseph Tassarotti,                   [23] LLVM Project. 2025. Missed Optimization: Fold a Same-Sign Unsigned
     M. Frans Kaashoek, and Nickolai Zeldovich. 2023. Verifying vMVCC, a                    Comparison into a Zero-Sum Test. https://github.com/llvm/llvm-
     high-performance transaction library using multi-version concurrency                   project/issues/166890
     control. In 17th USENIX Symposium on Operating Systems Design and
                                                                                       [24] LLVM Project. 2026. InstCombine Contributor Guide. https://llvm.
     Implementation (OSDI 23). USENIX Association, Boston, MA, 871–886.                     org/docs/InstCombineContributorGuide.html. Accessed: 2026-04-30.
     https://www.usenix.org/conference/osdi23/presentation/chang                       [25] LLVM Project. 2026. LLVM IR Undefined Behavior (UB) Manual.
[10] Leonardo De Moura, Soonho Kong, Jeremy Avigad, Floris Van Doorn,                       https://llvm.org/docs/UndefinedBehavior.html. Accessed: 2026-07-13.
     and Jakob von Raumer. 2015. The lean theorem prover (system de-                   [26] LLVM Project. 2026. LLVM IR Undefined Behavior (UB) Manual:
     scription). In International conference on automated deduction. Springer,              Summary. https://llvm.org/docs/UndefinedBehavior.html#summary.
     378–388.                                                                               Accessed: 2026-07-25.
[11] Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 The-
     orem Prover and Programming Language. In Automated Deduction
LLVM Translation Validation Automated with Large Language Models and Lean


[27] LLVM Project. 2026. LLVM Language Reference Manual: Immediate                   Columbia, Canada) (PLDI ’00). Association for Computing Machinery,
     Undefined Behavior. https://llvm.org/docs/UndefinedBehavior.html#               New York, NY, USA, 83–94. doi:10.1145/349299.349314
     immediate-ub. Accessed: 2026-07-13.                                        [45] Aina Niemetz, Mathias Preiner, and Yoni Zohar. 2024. Scalable Bit-
[28] LLVM Project. 2026. LLVM Language Reference Manual: ’llvm.assume’               Blasting with Abstractions. In Computer Aided Verification: 36th Inter-
     Intrinsic. https://llvm.org/docs/LangRef.html#llvm-assume-intrinsic.            national Conference, CAV 2024, Montreal, QC, Canada, July 24–27, 2024,
     Accessed: 2026-07-26.                                                           Proceedings, Part I (Montreal, QC, Canada). Springer-Verlag, Berlin,
[29] LLVM Project. 2026. LLVM Language Reference Manual: Poison                      Heidelberg, 178–200. doi:10.1007/978-3-031-65627-9_9
     Values. https://llvm.org/docs/UndefinedBehavior.html#poison-values.        [46] OpenAI. 2025. Codex CLI. https://github.com/openai/codex Accessed:
     Accessed: 2026-07-13.                                                           2026-09-10.
[30] LLVM Project. 2026. LLVM Language Reference Manual: Poison                 [47] OpenAI. 2026. API Pricing. https://developers.openai.com/api/docs/
     Values. https://llvm.org/docs/LangRef.html#poison-values. Accessed:             pricing Accessed: 2026-09-06.
     2026-07-25.                                                                [48] OpenAI. 2026. GPT-5.5 Model. https://developers.openai.com/api/
[31] LLVM Project. 2026. LLVM Language Reference Manual: ’select’                    docs/models/gpt-5.5 Accessed: 2026-09-06.
     Instruction. https://llvm.org/docs/LangRef.html#select-instruction.        [49] Amir Pnueli, Michael Siegel, and Eli Singerman. 1998. Translation
     Accessed: 2026-09-09.                                                           Validation. In Proceedings of the 4th International Conference on Tools
[32] LLVM Project. 2026. LLVM Language Reference Manual: Undefined                   and Algorithms for Construction and Analysis of Systems (TACAS ’98).
     Values. https://llvm.org/docs/UndefinedBehavior.html#undef-values.              Springer-Verlag, Berlin, Heidelberg, 151–166.
     Accessed: 2026-07-13.                                                      [50] Michael Stepp, Ross Tate, and Sorin Lerner. 2011. Equality-based
[33] LLVM Project. 2026. LLVM Language Reference Manual: Well-Defined                translation validator for LLVM. In Proceedings of the 23rd International
     Values. https://llvm.org/docs/LangRef.html#well-defined-values. Ac-             Conference on Computer Aided Verification (Snowbird, UT) (CAV’11).
     cessed: 2026-09-08.                                                             Springer-Verlag, Berlin, Heidelberg, 737–742.
[34] LLVM Project. 2026. LLVM Loop Idiom Recognize Pass Source                  [51] Chengnian Sun, Vu Le, Qirun Zhang, and Zhendong Su. 2016. Toward
     Code.      https://github.com/llvm/llvm-project/blob/main/llvm/lib/             understanding compiler bugs in GCC and LLVM. In Proceedings of
     Transforms/Scalar/LoopIdiomRecognize.cpp Idiom recognizers gated                the 25th International Symposium on Software Testing and Analysis
     on getNumBlocks() == 1 and getNumBackEdges() == 1.                              (Saarbrücken, Germany) (ISSTA 2016). Association for Computing Ma-
[35] LLVM Project. 2026.              LLVM Loop Pass Manager Source                  chinery, New York, NY, USA, 294–305. doi:10.1145/2931037.2931074
     Code.                 https://github.com/llvm/llvm-project/blob/main/      [52] The Rocq Development Team. 2025. The Rocq Prover. doi:10.5281/
     llvm/include/llvm/Transforms/Scalar/LoopPassManager.h                           zenodo.15149629
     FunctionToLoopPassAdaptor runs LoopSimplify and LCSSA                      [53] Amitayush Thakur, George Tsoukalas, Yeming Wen, Jimmy Xin, and
     before every loop pass.                                                         Swarat Chaudhuri. 2024. An In-Context Learning Agent for Formal
[36] LLVM Project. 2026. LLVM Loop Terminology (and Canonical Forms).                Theorem-Proving. In First Conference on Language Modeling. https:
     https://llvm.org/docs/LoopTerminology.html#loop-simplify-form Ac-               //openreview.net/forum?id=V7HRrxXUhN
     cessed: 2026-09-03.                                                        [54] The Lean Project. [n. d.]. standard-axioms. The Lean Language Refer-
[37] Pedro Lobo, John McIver, George Mitenkov, Juneyoung Lee, Kirshan-               ence. https://lean-lang.org/doc/reference/latest/Axioms/#standard-
     than Sundararajah, and Nuno P. Lopes. 2026. Towards Removing                    axioms Accessed 2026-07-28.
     Undef Values from LLVM IR. Proc. ACM Program. Lang. 10, PLDI,              [55] Kyle Thompson, Nuno Saavedra, Pedro Carrott, Kevin Fisher, Alex
     Article 172 (June 2026), 24 pages. doi:10.1145/3808250                          Sanchez-Stern, Yuriy Brun, João F. Ferreira, Sorin Lerner, and Emily
[38] Nuno P. Lopes, Juneyoung Lee, Chung-Kil Hur, Zhengyang Liu, and                 First. 2025. Rango: Adaptive Retrieval-Augmented Proving for Auto-
     John Regehr. 2021. Alive2: bounded translation validation for LLVM.             mated Software Verification. In Proceedings of the IEEE/ACM 47th Inter-
     In Proceedings of the 42nd ACM SIGPLAN International Conference on              national Conference on Software Engineering (Ottawa, Ontario, Canada)
     Programming Language Design and Implementation (Virtual, Canada)                (ICSE ’25). IEEE Press, 347–359. doi:10.1109/ICSE55347.2025.00161
     (PLDI 2021). Association for Computing Machinery, New York, NY,            [56] Jean-Baptiste Tristan, Paul Govereau, and Greg Morrisett. 2011. Eval-
     USA, 65–79. doi:10.1145/3453483.3454030                                         uating value-graph translation validation for LLVM. In Proceedings
[39] Nuno P. Lopes, David Menendez, Santosh Nagarakatte, and John                    of the 32nd ACM SIGPLAN Conference on Programming Language De-
     Regehr. 2015. Provably correct peephole optimizations with alive.               sign and Implementation (San Jose, California, USA) (PLDI ’11). As-
     In Proceedings of the 36th ACM SIGPLAN Conference on Programming                sociation for Computing Machinery, New York, NY, USA, 295–305.
     Language Design and Implementation (Portland, OR, USA) (PLDI ’15).              doi:10.1145/1993498.1993533
     Association for Computing Machinery, New York, NY, USA, 22–32.             [57] Hongxu Xu, Chunhao Liao, Xintong Zhou, and Chengnian Sun.
     doi:10.1145/2737924.2737965                                                     2026. Can Coding Agents Implement Missed Compiler Optimiza-
[40] Minghai Lu, Benjamin Delaware, and Tianyi Zhang. 2024. Proof                    tions? Evaluating LLM Agents on LLVM Peephole Optimizations.
     Automation with Large Language Models. In Proceedings of the 39th               arXiv:2607.02684 [cs.SE] https://arxiv.org/abs/2607.02684
     IEEE/ACM International Conference on Automated Software Engineering        [58] Zhenyang Xu, Hongxu Xu, Yongqiang Tian, Xintong Zhou, and Cheng-
     (Sacramento, CA, USA) (ASE ’24). Association for Computing Machin-              nian Sun. 2026. LPO: Discovering Missed Peephole Optimizations
     ery, New York, NY, USA, 1509–1520. doi:10.1145/3691620.3695521                  with Large Language Models. In Proceedings of the 31st ACM Inter-
[41] MLIR Project. 2026. ‘llvm’ Dialect. https://mlir.llvm.org/docs/Dialects/        national Conference on Architectural Support for Programming Lan-
     LLVM/. Accessed: 2026-05-03.                                                    guages and Operating Systems, Volume 2 (USA) (ASPLOS ’26). Asso-
[42] MLIR Project. 2026. LLVM IR Target. https://mlir.llvm.org/docs/                 ciation for Computing Machinery, New York, NY, USA, 1136–1150.
     TargetLLVMIR/. Accessed: 2026-07-22.                                            doi:10.1145/3779212.3790184
[43] Manasij Mukherjee and John Regehr. 2024. Hydra: Generalizing Peep-         [59] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song,
     hole Optimizations with Program Synthesis. Proc. ACM Program. Lang.             Shixing Yu, Saad Godil, Ryan J Prenger, and Animashree Anandku-
     8, OOPSLA1, Article 120 (April 2024), 29 pages. doi:10.1145/3649837             mar. 2023. LeanDojo: Theorem Proving with Retrieval-Augmented
[44] George C. Necula. 2000. Translation validation for an optimizing                Language Models. In Advances in Neural Information Processing
     compiler. In Proceedings of the ACM SIGPLAN 2000 Conference on                  Systems, A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt,
     Programming Language Design and Implementation (Vancouver, British              and S. Levine (Eds.), Vol. 36. Curran Associates, Inc., 21573–21612.
                                                                              Chunhao Liao, Hongxu Xu, Xintong Zhou, Yizhou Zhang, and Chengnian Sun


     doi:10.52202/075280-0944
[60] Xuejun Yang, Yang Chen, Eric Eide, and John Regehr. 2011. Find-
     ing and understanding bugs in C compilers. In Proceedings of the
     32nd ACM SIGPLAN Conference on Programming Language Design
     and Implementation (San Jose, California, USA) (PLDI ’11). Asso-
     ciation for Computing Machinery, New York, NY, USA, 283–294.
     doi:10.1145/1993498.1993532
[61] Jiaqi Yin, Zhan Song, Nicolas Bohm Agostini, Antonino Tumeo, and
     Cunxi Yu. 2025. HEC: equivalence verification checking for code trans-
     formation via equality saturation. In Proceedings of the 2025 USENIX
     Conference on Usenix Annual Technical Conference (Boston, MA, USA)
     (USENIX ATC ’25). USENIX Association, USA, Article 69, 16 pages.
[62] Yannick Zakowski, Calvin Beck, Irene Yoon, Ilia Zaichuk, Vadim Zaliva,
     and Steve Zdancewic. 2021. Modular, compositional, and executable
     formal semantics for LLVM IR. Proc. ACM Program. Lang. 5, ICFP,
     Article 67 (Aug. 2021), 30 pages. doi:10.1145/3473572
[63] Mengxiao Zhang, Yongqiang Tian, Zhenyang Xu, Yiwen Dong,
     Shin Hwei Tan, and Chengnian Sun. 2024. LPR: Large Language
     Models-Aided Program Reduction. In Proceedings of the 33rd ACM
     SIGSOFT International Symposium on Software Testing and Analysis
     (Vienna, Austria) (ISSTA 2024). Association for Computing Machinery,
     New York, NY, USA, 261–273. doi:10.1145/3650212.3652126
[64] Jianzhou Zhao, Santosh Nagarakatte, Milo M.K. Martin, and Steve
     Zdancewic. 2012. Formalizing the LLVM intermediate represen-
     tation for verified program transformations. In Proceedings of the
     39th Annual ACM SIGPLAN-SIGACT Symposium on Principles of
     Programming Languages (Philadelphia, PA, USA) (POPL ’12). Asso-
     ciation for Computing Machinery, New York, NY, USA, 427–440.
     doi:10.1145/2103656.2103709
[65] Jianzhou Zhao, Santosh Nagarakatte, Milo M.K. Martin, and Steve
     Zdancewic. 2013. Formal verification of SSA-based optimizations for
     LLVM. In Proceedings of the 34th ACM SIGPLAN Conference on Pro-
     gramming Language Design and Implementation (Seattle, Washington,
     USA) (PLDI ’13). Association for Computing Machinery, New York,
     NY, USA, 175–186. doi:10.1145/2491956.2462164
[66] Xintong Zhou, Hongxu Xu, Chunhao Liao, Puzhuo Liu, Yongqiang
     Tian, and Chengnian Sun. 2026.            Semantic-aware and Self-
     improving Program Reduction via Agentic Large Language Models.
     arXiv:2607.03766 [cs.SE] https://arxiv.org/abs/2607.03766
