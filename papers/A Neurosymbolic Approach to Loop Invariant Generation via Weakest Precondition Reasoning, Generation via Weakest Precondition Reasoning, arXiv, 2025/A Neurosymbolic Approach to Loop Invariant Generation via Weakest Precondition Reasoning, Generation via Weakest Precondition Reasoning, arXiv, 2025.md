                                         A Neurosymbolic Approach to Loop Invariant
                                         Generation via Weakest Precondition Reasoning
                                         Daragh King1 #
                                         Department of Computer Science and Statistics, Trinity College Dublin, Dublin, Ireland
                                         Vasileios Koutavas #
                                         Lero, Research Ireland Centre for Software
                                         Department of Computer Science and Statistics, Trinity College Dublin, Dublin, Ireland
                                         Laura Kovács #
                                         Faculty of Informatics, TU Wien, Vienna, Austria

                                                 Abstract
arXiv:2512.15816v1 [cs.PL] 17 Dec 2025




                                         Loop invariant generation remains a critical bottleneck in automated program verification. Recent
                                         work has begun to explore the use of Large Language Models (LLMs) in this area, yet these
                                         approaches tend to lack a reliable and structured methodology, with little reference to existing
                                         program verification theory. This paper presents NeuroInv, a neurosymbolic approach to loop
                                         invariant generation. NeuroInv comprises two key modules: (1) a neural reasoning module that
                                         leverages LLMs and Hoare logic to derive and refine candidate invariants via backward-chaining
                                         weakest precondition reasoning, and (2) a verification-guided symbolic module that iteratively
                                         repairs invariants using counterexamples from OpenJML. We evaluate NeuroInv on a comprehensive
                                         benchmark of 150 Java programs, encompassing single and multiple (sequential) loops, multiple arrays,
                                         random branching, and noisy code segments. NeuroInv achieves a 99.5% success rate, substantially
                                         outperforming the other evaluated approaches. Additionally, we introduce a hard benchmark of 10
                                         larger multi-loop programs (with an average of 7 loops each); NeuroInv’s performance in this setting
                                         demonstrates that it can scale to more complex verification scenarios.

                                         2012 ACM Subject Classification Software and its engineering → Formal software verification;
                                         Theory of computation → Program verification; Computing methodologies → Artificial intelligence

                                         Keywords and phrases Loop invariants, Program verification, Hoare logic, Neurosymbolic AI, Large
                                         language models


                                             1    Introduction
                                         Loop invariant generation is a central challenge in automated program verification. Within
                                         Hoare logic [12], loop invariants are the inductive assertions for establishing the correctness
                                         of looping computations; loop invariants must: (a) hold before the loop, (b) be preserved
                                         by each loop iteration, and (c) imply the loop postcondition upon exit (see Section 1.1 for
                                         additional details on Hoare logic and loop invariants). Despite their conceptual simplicity,
                                         discovering suitable loop invariants is an undecidable problem and notoriously difficult to
                                         achieve with heuristics. Traditional static techniques—including abstract interpretation [4],
                                         logical abduction [1], symbolic execution [21], and recurrence solving [13]—perform well
                                         in narrow domains but often struggle to generalise across programs with more complex
                                         structures, such as programs with multiple loops. Dynamic approaches such as [7] can infer
                                         loop invariants from program executions, but their soundness is fundamentally constrained
                                         by the trace quantity and quality.
                                             The advent of Large Language Models (LLMs) has led to recent work exploring whether
                                         they can generate program properties such as weakest preconditions [17, 16], postcondi-


                                         1
                                             Corresponding Author
2   A Neurosymbolic Approach to Loop Invariant Generation via WP Reasoning


    tions [6], and even loop invariants [23, 14]. While these early investigations demonstrate
    promise, existing LLM-based approaches to loop invariant generation typically rely on ad-hoc
    prompting, and provide no systematic alignment with program verification theory. Moreover,
    because these methods lack a principled mechanism for the guided refinement of loop invari-
    ants, the invariants that are produced are often brittle (both syntactically and semantically)
    — these invariants may be sufficient for simple integer loops but unreliable for programs
    involving arrays, multiple loops, or noisy and semantically irrelevant code.
        To address these limitations in LLM-based loop invariant inference, we introduce NeuroInv,
    a neurosymbolic [10] framework for loop invariant generation that integrates LLMs with
    weakest precondition (WP) reasoning [5] and counterexample-guided symbolic verification.
    NeuroInv comprises two complementary modules. The neural module segments the input
    program into loop-free and looping components, it then leverages an LLM to perform three
    primary tasks: (1) calculate WPs of loop-free code segments, (2) generate candidate loop
    invariants, and (3) check and refine candidate loop invariants according to the preservation
    and exit obligations defined by Hoare logic (Section 1.1) – when the aforementioned obligations
    fail, the module attempts targeted refinement of the candidate loop invariant. The process
    employed by the neural module yields a structured and theory-guided reasoning procedure
    that stands in contrast to ad-hoc prompting approaches [14].
        The symbolic module strengthens the above approach by validating the neurally-derived
    invariants using OpenJML, extracting counterexamples when verification fails, and attempting
    invariant repair through a feedback-directed process. This dual-level refinement and repair
    approach enables NeuroInv to reliably generate correct loop invariants.
        We evaluate NeuroInv on a comprehensive benchmark of 150 Java programs, encompassing
    single and multiple (sequential) loops, multiple arrays, random branching, and noisy code
    segments. NeuroInv achieves a 99.5% success rate, substantially outperforming ad-hoc
    prompting, neural-only ablations, and a state-of-the-art LLM-based specification generator
    for Java [19]. A hard benchmark of 10 larger multi-loop programs further demonstrates
    that NeuroInv scales effectively to more complex programs, with the neural module playing
    a key role in handling longer and more complex reasoning chains. Taken together, these
    results illustrate that systematic WP reasoning, when integrated with verification feedback,
    significantly enhances the robustness and reliability of LLM-assisted invariant generation.
        The remainder of the paper is structured as follows. Section 1.1 outlines the requisite
    background on Hoare logic [9, 12], weakest preconditions [5], and loop invariants necessary
    for understanding NeuroInv. Section 2 presents the method behind NeuroInv, while Section 3
    outlines our experimental evaluation and the obtained results. Section 4 discusses threats to
    validity and future work. Section 5 highlights related work, and Section 6 concludes.


    1.1    Hoare Logic, Weakest Preconditions and Loop Invariants
    Hoare logic provides a formal system for reasoning about the correctness of imperative
    programs. The core unit of this logic is the Hoare triple (Definition 1). Hoare triples
    fundamentally rely on the notions of pre- and postconditions: postconditions specify the
    desired property of the program state upon termination, whilst preconditions specify the
    required property of the initial program state for it to behave as intended (i.e. to satisfy the
    program’s postcondition). The logic has a total and partial correctness version, depending
    on whether it proves termination or not. Here, we focus on partial correctness.

    ▶ Definition 1 (Hoare Triple (Partial Correctness)). A Hoare triple {P } C {Q} asserts
    that if the precondition P holds before executing command C, and C terminates, then the
D. King, V. Koutavas, and L. Kovács                                                               3


postcondition Q holds after execution.

    Reasoning over Hoare triples enables compositional program verification, but to do so
effectively one must carefully consider the notion of a precondition. Consider the Hoare
triple {P } C {Q}, if P is too restrictive (or strong), then it may exclude initial states that
would in fact satisfy Q after C executes and terminates. It has been shown [5] that for
a program C and postcondition Q, there exists a unique largest precondition, called the
weakest precondition (WP).

▶ Definition 2 (Weakest Precondition). The weakest precondition WP(C, Q) is the most
general condition that, if true before executing command C, guarantees that postcondition Q
holds after execution (assuming termination).

    The WP calculus [5] provides a proof technique for Hoare Triples: to prove {P } C {Q},
one must compute WP(C, Q), and prove that P ⇒ WP(C, Q). This means that any starting
state satisfying P also satisfies WP(C, Q), and that after executing C, the final state will
satisfy Q.

▶ Definition 3 (Initialisation).

   P ⇒ WP(C, Q)                                                                             (1)

    Crucially, the WP calculus offers compositional rules for computing weakest preconditions.
A core rule of the calculus states that the WPs of sequential commands are composed in a
backward manner: for a sequence of commands C1 ; C2 , the WP of C2 (with respect to an
overall postcondition Q) serves as the immediate postcondition of C1 (Definition 4). (Other
rules compose WPs in the case of branching and assignment commands.)

▶ Definition 4 (WP of Sequence).

   WP(C1 ; C2 , Q) = WP(C1 , WP(C2 , Q))                                                    (2)

    For loops however, calculating weakest preconditions is undecidable, and the WP calculus
relies on externally provided loop invariants. Broadly speaking, loop invariants are assertions
that hold before and after each loop iteration. In the context of the WP calculus however,
sufficient loop invariants must also satisfy the following two conditions:

▶ Definition 5 (Preservation). If the invariant I holds and the loop condition B is true,
executing the loop body C must preserve the invariant. Equivalently:

   I ∧ B ⇒ WP(C, I)                                                                         (3)

▶ Definition 6 (Exit). When the invariant I holds and the loop exits (i.e. B is false), the
loop’s postcondition Q must be satisfied.

   I ∧ ¬B ⇒ Q                                                                               (4)

    These conditions, together with equation (1) and the WP-composition rules, ensure
that the WP calculus correctly builds a verification proof within the framework of Hoare
logic. In Section 2.1, the two conditions in Definitions 5 and 6 play a major role in the
loop invariant refinement process. Additionally, Definition 4 forms the basis of the neural
module’s reasoning.
4   A Neurosymbolic Approach to Loop Invariant Generation via WP Reasoning



                                               NeuroInv




                                                    M'
                 M             Neural Module              Symbolic Module              M''


                                     LLM                     LLM   OpenJML




                                 Refinement                    Repair
                                  Failure                      Failure



       Figure 1 High-level architecture of NeuroInv; M is the input program, M ′ is the input program
    with the neurally-derived loop invariants, and M ′′ represents M with the correct loop invariants as
    JML annotations.

         Algorithm 1 Neurosymbolic Loop Invariant Generation
    Require: Java method M with JML precondition Pre and postcondition Post
    Ensure: Verified method M ′ with loop invariants
     1: Module 1: Neural Reasoning (Algorithm 2)
     2: invariants ← NeuralReasoningModule(M, Pre, Post)
     3:
     4: Module 2: Symbolic Verification (Algorithm 3)
     5: M ′ ← SymbolicVerificationModule(M, invariants,Pre,Post)
     6: return M ′



     2      Method
    Our approach, NeuroInv, aims to generate sufficient loop invariants for verifying the cor-
    rectness of Java methods against their given pre- and postconditions. The system is built
    around a two-module neurosymbolic architecture that combines weakest precondition (WP)
    reasoning with symbolic verification.
        Neural Module: Given a Java method with JML pre- and postconditions, the neural
    module attempts to derive high-quality candidate loop invariants via backward-chaining WP
    reasoning. The module leverages an LLM to perform three primary tasks: (1) calculate
    WPs of loop-free code segments; (2) generate candidate loop invariants; (3) check and refine
    candidate loop invariants according to the logical implications defined in Definitions 5 and 6.
        Symbolic Module: Given the candidate loop invariant(s) derived by the neural module,
    the symbolic module translates these into JML annotations and attempts program verification
    via OpenJML. If verification fails, the module extracts counterexample information from
    the OpenJML output, and attempts to use this to repair the candidate loop invariant. This
    process iterates until verification succeeds or a maximum repair limit is reached.
        The key insight of our neurosymbolic design is dual-level refinement and repair: The
    refinement process employed by the neural module attempts to ensure that the candidate
    loop invariants are generated in a manner consistent with Hoare logic and the WP calculus.
    The repair process of the symbolic module leverages verification feedback to repair loop
    invariants according to errors that have eluded the neural module.
        Figure 1 illustrates the high-level architecture of NeuroInv. Algorithm 1 describes the
D. King, V. Koutavas, and L. Kovács                                                                       5



                                                                                      ...
          Postcondition of                  Postcondition of
      preceding code segment P          preceding code segment P




             WP(C, Q)                       Loop Invariant I                          Loop
                                                                                      Link




                                                                               While-loop C1 with
                                                                          postcondition Q1 = WP(C0, Q0)

             Loop-Free
                                               Loop Link
               Link
                                                                                     Loop-
                                                                                     Free
                                                                                     Link




      Loop-free code segment C           While-loop C with loop                Loop-free C0 with
        with postcondition Q                postcondition Q                     postcondition Q0




    Figure 2 The two left-most entities depict the link types used within the neural module’s backward
chaining WP reasoning. The entity on the right shows the chain between a "Loop-Free" and "Loop"
link, for a hypothetical program segment which is comprised of a while loop followed by loop-free
code.


overall approach, whilst Algorithms 2 and 3 depict the details of the neural and symbolic
modules respectively. Additionally, Appendix A contains NeuroInv’s prompts.

2.1     Neural Module
The neural module generates candidate loop invariants via backward-chaining weakest
precondition reasoning. This process relies on the LLM to perform three core tasks: (1)
calculate WPs of loop-free code segments; (2) generate candidate loop invariants; (3) check
and refine candidate loop invariants according to the logical implications of Definitions 5
and 6. This process follows Algorithm 2 below.

2.1.1      Program Segmentation
Before attempting any reasoning, the neural module first splits the input program into
looping and loop-free segments. Each segment is tagged with opening and closing marker
comments, such as:
   // code N open ... // code N close: The N th loop-free code segment.
   // while N open ... // while N close: The N th while loop
This segmentation enables systematic processing: the marker comments allow for the pro-
grammatic extraction of the desired code segments.

2.1.2      Backward-Chaining WP Reasoning
Starting from the program’s given postcondition, the neural module works backwards through
the segmented program (Section 2.1.1), chaining together WP calculations and loop invariant
derivations.
   Conceptually, the aforementioned chains consist of two link types, with each link type
being associated to a particular type of code segment and set of LLM-based computations:
1. Loop-Free Link:
6   A Neurosymbolic Approach to Loop Invariant Generation via WP Reasoning


       Algorithm 2 Neural Module: Loop Invariant Generation via Backward-Chaining WP Reasoning
    Require: Method M , precondition Pre, postcondition Post
    Ensure: Candidate loop invariants, or ERROR if refinement limit is reached
     1: Phase 1: Program Segmentation
     2: ⟨codeSegments, loops⟩ ← SegmentProgram(M )
     3:
     4: Phase 2: Backward-Chaining WP Reasoning
     5: Post ← ExtractPostcondition(M )                                        ▷ From JML postcondition
     6: currentPost ← Post
     7: invariants ← {}
     8: if ∃ final code segment after all loops then
     9:     currentPost ← LLM-ComputeWP(finalSegment, currentPost)
    10: end if
    11: for loopIndex ← |loops| down to 1 do                              ▷ Process loops in reverse order
    12:     currentLoop ← loops[loopIndex]
    13:     loopCondition ← condition(currentLoop)
    14:     loopBody ← body(currentLoop)
    15:     loopPost ← currentPost
    16:     invariant ← LLM-GenerateInvariant(currentLoop, loopPost)
    17:     validated ← false
    18:     for attempt ← 1 to MAX_REFINEMENT do
    19:         weakestPre ← LLM-ComputeWP(loopBody, invariant)
    20:         preservation ← LLM-CheckImplication(invariant ∧ loopCondition ⇒ weakestPre)
    21:         exit ← LLM-CheckImplication(invariant ∧ ¬loopCondition ⇒ loopPost)
    22:         if preservation ∧ exit then
    23:             validated ← true
    24:             break                                                         ▷ Both implications hold
    25:         else
    26:             invariant ← LLM-RefineInvariant(invariant, preservation, exit)
    27:         end if
    28:     end for
    29:     if ¬validated then
    30:         throw ERROR                                                    ▷ Refinement limit reached
    31:     end if
    32:     invariants[currentLoop] ← invariant
    33:     currentPost ← invariant                  ▷ Invariant becomes postcondition for preceding code
    34:     if ∃ code segment before currentLoop then
    35:         precedingSegment ← codeSegments[loopIndex]
    36:         currentPost ← LLM-ComputeWP(precedingSegment, currentPost)
    37:     end if
    38: end for
    39:
    40: Precondition Sanity Check
    41: entailment ← LLM-CheckImplication(Pre ⇒ currentPost)                               ▷ Non-blocking
    42: return invariants



         Code segment type: Loop-free.
         Computation: Calculating the WP of a loop-free code segment, given a postcondition
         Q.
    2. Loop Link:
         Code segment type: while loop.
         Computation (sequence):
        a. Generating a candidate loop invariant I, given a loop postcondition Q.
        b. Calculating the WP of the loop body S, using the loop invariant I as the postcon-
            dition, i.e. calculating W P (S, I).
        c. Verifying that I satisfies Definition 5.
        d. Verifying that I satisfies Definition 6.
        e. Refining I if steps c or d fail, if this occurs, then the sequence restarts at step b
            with the refined loop invariant I.
D. King, V. Koutavas, and L. Kovács                                                                      7


        Algorithm 3 Symbolic Module: Verification with Counterexample-Guided Repair
Require: Method M , candidate invariants invs, precondition Pre, postcondition Post
Ensure: Verified method M ′ or ERROR
 1: Phase 3: Finalization and Verification
 2: M ′ ← LLM-ConvertToJML(M, invs)                                         ▷ Convert to JML syntax
 3: for repairAttempt ← 1 to MAX_REPAIR do
 4:     ⟨verified, counterexamples⟩ ← OpenJML-Verify(M ′ )
 5:     if verified then
 6:         return M ′                                                         ▷ Successfully verified
 7:     end if
 8:     invs ← LLM-RepairInvariant(invs, counterexamples)
 9:     M ′ ← LLM-ConvertToJML(M, invs)
10: end for
11: return ERROR                                            ▷ Could not verify within the repair limit



    Fig. 2 depicts the two link types; the ultimate goal of both links is to produce the
postcondition for the preceding code segment (if it exists). By chaining together these links,
the neural module can work backwards from a program’s given postcondition to derive loop
invariants. At the end of this process, the neural module checks that last WP derived satisfies
Definition 3.


2.2        Symbolic Module
The symbolic module is conceptually simple and can be summarised by the following steps:
1. Translating loop invariants produced by the neural module into the corresponding JML
   annotations.
2. Attempting to verify the annotated program using OpenJML.
3. If Step 2 fails, extracting counterexample information from OpenJML and using it to
   repair the loop invariant(s). The process then repeats from Step 2 with the repaired
   invariant(s), until either (a) verification succeeds or (b) the maximum repair limit is
   reached.
Algorithm 3 details this procedure.


    3      Evaluation

3.1        Experimental Setup
The following sections outline the basic components of our experimental evaluation. Sec-
tion 3.1.1 describes the the benchmark suite. Section 3.1.2 describes the methods evaluated.
Section 3.1.3 presents the implementation details. And finally, Section 3.1.4 details the
evaluation metrics used.


3.1.1        Benchmark Suite
The benchmark suite used in our evaluation is divided into two subsets: (1) the standard
benchmark and (2) the hard benchmark. The programs of these subsets share common at-
tributes, each features: (a) single Java methods annotated with JML pre- and postconditions,
and (b) at least one while loop. 2


2
    Both standard and hard benchmarks will be archived in Zenodo.
8   A Neurosymbolic Approach to Loop Invariant Generation via WP Reasoning


        Table 1 Standard benchmark composition and key characteristics.

            Category    Count     Arrays    Multi-loop     Noisy    Rand. Branch      ∀-Inv    ∃-Inv

               1.           62      ✗            ✗           ✗             ✗            ✗        ✗
               2.           35      ✓            ✗           ✗             ✗            ✓        ✗
               3.           21      ✓            ✓           ✗             ✗            ✓        ✗
               4.           15      ✓†           ✗           ✓             ✗            ✓†       ✗
               5.           10      ✓            ✗           ✗             ✓            ✓        ✗
               6.            5      ✓            ✗           ✗             ✗            ✗        ✓
               7.            2      ✓            ✗           ✗             ✗            ✓        ✗

             Total         150
    †
     Only a subset of the noisy programs are array-based and require universally quantified invariants (those
    derived from Category 2.).


        Standard Benchmark. The standard benchmark consists of 150 programs, with the
    following split into high-level categories (summarised in Table 1):
    1. 62 programs are single-loop Java translations of programs originating from the Code2Inv [26]
        dataset; these 62 programs were chosen because they do not feature non-determinism in
        their loop guards.
    2. 35 programs are array-manipulating single-loop programs derived from the work of [16];
        these 35 programs can feature multiple arrays, and require loop invariants with universal
        quantification.
    3. 21 programs are obtained as semantics-preserving multi-loop decompositions of a subset
        of the programs described in point 2 above.
    4. 15 programs are obtained as semantics-preserving "noisy" translations of a subset of the
        programs described in points 1 and 2 above. These programs feature dead, irrelevant, or
        unreachable code, alongside (potentially) misrepresentative variable names.
    5. 10 programs are single-loop Java translations of programs originating from [17]; each of
        these programs feature random branching within their respective loops.
    6. 5 programs are array-manipulating single-loop programs derived from the work of [16];
        these 5 programs can feature multiple arrays, and require loop invariants with existential
        quantification.
    7. 2 programs fall outside of the above categories, one program creates a reversal of a given
        array, and the other checks for equality between two arrays.

       Hard Benchmark. The hard benchmark features 10 programs which are deliberately
    designed to stress-test the evaluated methods (Section 3.1.2) and their scalability. The
    characteristics of this benchmark are described in Section 3.3.


    3.1.2     Methods Evaluated
    We evaluate four methodologies in our experiments: ad-hoc prompting, NeuroInv (Section 2),
    NeuroInv*, and SpecGen [19].
        Ad-hoc prompting: this approach directly asks the LLM for the correct loop invariants
    for a given program; this is done without providing any annotated examples, and can thus be
    viewed as a zero-shot prompting approach [25]. The prompt utilised can be seen in Listing 1
    of Appendix A.
D. King, V. Koutavas, and L. Kovács                                                              9


    NeuroInv: this is our proposed neurosymbolic approach to loop invariant generation
detailed in Section 2.
    NeuroInv*: this approach consists only of the neural module outlined in Section 2.1.
We include this “neural-only” variant as an ablation to better understand the contributions
of the neural and symbolic modules. Note that NeuroInv subsumes NeuroInv*, therefore
both approaches will share certain results in the following sections.
    SpecGen: SpecGen [19] is a recent LLM-based approach to automatically generating full
program specifications (including loop invariants and pre- and postconditions). Consequently,
the intended goals of SpecGen are broader than loop invariant generation alone – SpecGen
may also alter the given JML pre- and postconditions, since it was originally designed for use
with unspecified programs (experimentally, we found that this occurred for approximately
68% of programs in the standard benchmark). In our setting, we regard such cases as failures
in the statistics reported in Section 3.2, this is because we can no longer guarantee that
the verified pre- and postconditions are equivalent to the originals. Despite this, we include
SpecGen in our evaluation as it is the most closely related approach to our own: SpecGen
targets Java, produces JML-based specifications, and can generate loop invariants – to the
best of our knowledge, a more suitable LLM-based loop invariant generator for Java does not
exist currently. Moreover, SpecGen has been shown to outperform other related methods for
specification generation, such as AutoSpec [27], Daikon [7], and Houdini [8].

3.1.3    Implementation Details
We utilise the following configuration for our experiments.
  Experimental Protocol: We complete 5 independent experimental runs of the meth-
  ods outlined in Section 3.1.2, this is done for both the standard and hard benchmark
  evaluations.
  Model: We use o4-mini [22] as the underlying model for each method evaluated
  (including SpecGen). At the time of writing, o4-mini is the most performant and
  affordable of OpenAI’s reasoning models.
  OpenJML and Solver: we use openjml 21-0.11 and Z3 version 4.13.4 - 64 bit
  as its underlying solver.
  Refinement and Repair Parameters:
 1. MAX_REFINEMENT: refers to the maximum number of refinement attempts that can be
     made by the neural module for each loop in a given program. We use MAX_REFINEMENT=
     5.
 2. MAX_REPAIR: refers to the maximum number of repair attempts that can be made by
     the symbolic module per program. We use MAX_REPAIR= 5

3.1.4    Evaluation Metrics
The following metrics form the basis of our analysis.
   Success Rate: this denotes the percentage of programs for which the generated loop
   invariants enable successful verification. The "Avg." success rate in Table 2 denotes the
   mean success rates obtained over 5 experimental runs of all programs in the standard
   benchmark (i.e. 750 total program evaluations).
   Standard Deviation: we use this to measure the stability of the "Success Rate" results
   across multiple experimental runs.
   Pass@k: this metric quantifies the probability that at least one solution (out of k) is
   correct for a given problem [2]. We use this metric on a per-program basis to observe how
10   A Neurosymbolic Approach to Loop Invariant Generation via WP Reasoning


           Table 2 Overall standard benchmark results, obtained across 5 experimental runs.

                       Avg. Success Rate     Std. Dev.   Avg. Refinement   Avg. Repair     Avg.       Avg.
         Method
                             (%)                (%)           Iters.          Iters.      Pass@3     Pass@5
         Ad-hoc                66.4               3.11          -                -          0.87      0.91
         SpecGen†              28.5               2.47          -                -            -         -
         NeuroInv*             84.7               2.31        0.59               -          0.95      0.97
         NeuroInv              99.5               0.87        0.59             0.24           1         1
     †
         See Section 3.1.2 for SpecGen caveats.



           increasing k affects the probability that at least one of the k generated loop invariants (or
           loop invariant sets, in the multi-loop case) for a program will enable successful verification.
           The "Avg." pass@k values denoted in Table 2 represent the mean pass@3 and pass@5
           values obtained for the standard benchmark.
           Refinement Iterations: this denotes the average number of attempts the neural module
           has made to refine candidate loop invariants per program – this is computed across a set
           of programs, e.g. the standard or hard benchmark. The "Avg." Refinement Iterations in
           Table 2 denotes the mean number of Refinement Iterations observed across 5 experimental
           runs on the standard benchmark.
           Repair Iterations: this denotes the average number of attempts the symbolic module
           has made to repair loop invariant(s) per program – this is computed across a set of
           programs, e.g. the standard or hard benchmark. The "Avg." Repair Iterations in Table 2
           denotes the mean number of Repair Iterations observed across 5 experimental runs on
           the standard benchmark.


     3.2       Main Results
     3.2.1        Overall Performance
     Table 2 and Fig. 3 present the overall results obtained on the standard benchmark.
         In terms of the average success rate observed, NeuroInv clearly trumps the other ap-
     proaches; with a value of 99.5%, NeuroInv far surpasses the performance of both SpecGen
     (28.5%) and ad-hoc prompting (66.4%). Although NeuroInv* (84.7%) fares better than both
     SpecGen and ad-hoc prompting, it falls short of the full NeuroInv approach. This suggests
     that the addition of the symbolic module enables the generation of higher quality loop
     invariants, i.e. the counter-example feedback provided by OpenJML can practically aid the
     repair of candidate loop invariants. It is worth noting that the relatively poor performance
     of SpecGen is likely due to it being an approach for generating full program specifications,
     and not loop invariants specifically. The performance gap between NeuroInv and SpecGen
     suggests that a blanket approach to program specification will not suffice for generating
     intricate loop invariants in the presence of given pre- and postconditions.
         Considering result stability, NeuroInv achieves the lowest standard deviation of the
     success rate. Taken together with its superior average success rate, these two measures
     show that NeuroInv can consistently generate correct loop invariants – this notion is further
     supported by NeuroInv’s average pass@3 score being equal to 1 (this means that in any given
     3 experimental runs, NeuroInv finds the correct loop invariant(s) for any given standard
     benchmark program at least once). Although NeuroInv* is less stable than NeuroInv, its
     standard deviation is still lower than both ad-hoc prompting and SpecGen; suggesting that
D. King, V. Koutavas, and L. Kovács                                                                        11


                                         Average Success Rates of Loop Invariant Generation Methods
                                   100                                                        99.47±0.87

                                                                                 84.67±2.31
           Avg. Success Rate (%)    80
                                             64.40±3.11
                                    60

                                    40
                                                           28.53±2.47

                                    20

                                     0
                                              Ad-hoc       SpecGen               NeuroInv*    NeuroInv
                                                                        Method
   Figure 3 Average success rates (with std. deviation bars), obtained across 5 experimental runs.



the systematic approach employed by the neural module leads to correct loop invariants
consistently.

Takeaway: On our benchmarks, NeuroInv reliably generates the most correct loop invariants
(99.5%); SpecGen fares the worst (28.5%), and is even succeeded by an ad-hoc prompting
approach (66.4%) specific to loop invariant generation.



3.2.2    Refinement Results
In this section we present the loop invariant refinement results derived by NeuroInv’s neural
module (i.e. NeuroInv*) on the standard benchmark.
    Recall that a loop invariant refinement occurs in the neural module (Section 2.1) when
the LLM deems that a candidate invariant does not satisfy at least one of Definition 5 (i.e.
an Implication 1 failure) and Definition 6 (i.e. an Implication 2 failure). Note that an
Implication 1 failure precludes the possibility of an Implication 2 failure being recorded –
this is a by-product of the current implementation.
    Fig. 4 depicts the proportion of programs which require (and do not require) loop invariant
refinements; the stability of these plots suggests that the number of programs requiring loop
invariant refinements is relatively consistent. This consistency is somewhat surprising when
considering the "Total Refinements" plot (i.e. the dashed-line); with minimum and maximum
values of 77 and 102 respectively, this statistic appears to be more erratic in comparison.
Taken together, these observations suggest that there is not a strong relationship between
the number of programs requiring refinements and the total number of refinements entailed.
    Fig. 5 displays the proportion of refinements induced by Implication 1 and Implication 2
failures; the split between the two failure types is close to 50 : 50 for each experimental run.

Takeaway: A consistently-sized subset of programs trigger loop invariant refinement; the
type of logical failure which triggers refinement is evenly split between Implication 1 and
Implication 2 failures; and the number of refinements required varies considerably across
experimental runs.
12   A Neurosymbolic Approach to Loop Invariant Generation via WP Reasoning


                                                           NeuroInv Refinement Statistics Across Runs
                                                                                              Programs with Refinements (%)    110
                                                                                              Programs with no Refinements (%)
                                              65                                              Total Refinements
                                                   62.7                       62.0            104                             105
                                                              60.0                                                    60.0
                                              60                                              58.7
                 Percentage of Programs (%)
                                                                                                                              100




                                                                                                                                Total Refinements (Count)
                                              55                                                                              95
                                                               92
                                              50                                                                              90
                                                    86
                                              45                                                                              85
                                                                               83
                                                                                              41.3
                                                              40.0                                                    40.0
                                              40                                                                              80
                                                   37.3                       38.0                                     77

                                              35                                                                              75
                                                   Run 1      Run 2           Run 3           Run 4                   Run 5
                                                                              Run

         Figure 4 The proportions of programs which do (and do not) require loop invariant refinements
     across each experimental run (solid lines). Additionally, the dashed line depicts the total number of
     refinements required per experimental run.


     3.2.3     Repair Results and Ablation Analysis
     In order to understand how the individual modules of our neurosymbolic approach contribute
     to producing correct loop invariants, we further discuss NeuroInv* (i.e. the neural module)
     and NeuroInv (the combined neural and symbolic modules).
         The overall standard benchmark results (Table 2) show that NeuroInv* and NeuroInv
     achieve average success rates of 84.7% and 99.5% respectively. In other words, the inclusion
     of the symbolic module leads to an average success rate increase of +14.8%. On the other
     hand, recall that loop invariant repair is carried out by the symbolic module (Section 2.2)
     when the loop invariants produced by the neural module (i.e. NeuroInv*) do not enable
     program verification with OpenJML. Considering NeuroInv*’s average success rate of 84.7%
     (Table 2), this implies that the vast majority of cases never require invariant repair by the
     symbolic module. This notion is further backed by the average repair iterations statistic
     (0.24) denoted in Table 2.
         Additionally, the pass@5 scores in Table 2 show that there exists a subset of programs for
     which NeuroInv* never derives the correct loop invariant(s), whilst NeuroInv does at least
     once. We will refer to this set of programs as the "problem" set.
         Upon investigation, we find that the problem set contains 5 programs and showcases a key
     limitation of the neural-only approach. For each program in the problem set, the candidate
     loop invariant generated by the neural module failed OpenJML verification – in each case
     this was due to the invariant not holding before the loop. In fact, the neural module was also
     able to highlight this limitation, this was done by checking the implication of Definition 3 at
     the end of its reasoning process. At this stage though, it is simply too little, too late – the
     current implementation of the neural module has no effective recourse to backtrack along
     its reasoning process at this point – hence, the feedback provided by OpenJML and the
     symbolic module is essential here for generating the correct loop invariants.

     Takeaway: NeuroInv’s inclusion of the symbolic module leads to an average success rate
     increase of +14.8% over NeuroInv*, and the symbolic module is essential to producing the
D. King, V. Koutavas, and L. Kovács                                                                                                             13


                                                            Refinements Induced by Implication Type
                                    Implication 1 (Preservation)
                                    Implication 2 (Exit)
                              60
                                                                                                                 53
                                                              50                                           51 (51.0%)
                                                            (54.3%)                                      (49.0%)
                              50
                                     43      43                         42            43
                                   (50.0%) (50.0%)                    (45.7%)       (51.8%) 40
           Refinement Count

                                                                                           (48.2%)                        39      38
                              40                                                                                        (50.6%) (49.4%)


                              30


                              20


                              10


                               0
                                        Run 1                      Run 2                Run 3               Run 4           Run 5
                                                                                        Run

   Figure 5 The proportions of refinements induced by Implication 1 and Implication 2 failures,
evaluated across 5 experimental runs.

   Table 3 Hard benchmark composition and key characteristics.

           Program                       # Loops                   # Arrays          ∀-Inv       ∃-Inv        Noisy     Lines Of Code

                              1                       2                         0         ✗          ✗          ✗                          29
                              2                       3                         0         ✗          ✗          ✗                          43
                              3                       4                         0         ✗          ✗          ✗                          56
                              4                       5                         0         ✗          ✗          ✗                          77
                              5                       4                         2         ✓          ✗          ✗                          62
                              6                       4                         3         ✓          ✓          ✗                          62
                              7                       8                         1         ✓          ✗          ✗                          78
                              8                       8                         3         ✓          ✓          ✗                          95
                              9                      10                         2         ✓          ✗          ✓                         152
                              10                     12                         2         ✓          ✗          ✗                         117



correct loop invariants for a small subset of standard benchmarks.


3.3    A Brief Scalability Analysis: The Hard Benchmark
In order to test the scalability of NeuroInv to complex programs, we created a hard benchmark
consisting of 10 programs; Table 3 depicts the characteristics of these programs. Following
the protocol of the standard benchmark evaluation (i.e. using the implementation details
of Section 3.1.3), we conduct 5 experimental runs of ad-hoc prompting (Section 3.1.2) and
NeuroInv (and its subsumed NeuroInv*) – we refrain from evaluating SpecGen in this context
due to its performance on the standard benchmark (Section 2). Table 4 presents these results.
    NeuroInv achieves an average success rate of 62%, whilst ad-hoc prompting and NeuroInv*
only achieve 14% and 40% respectively – NeuroInv succeeds ad-hoc prompting by a large
margin of +48% points. These results show that NeuroInv can scale to difficult programs
(albeit with a hit in performance when compared to standard benchmark programs), whilst
ad-hoc prompting fails to do so. These results also highlight that there is still value in the
14   A Neurosymbolic Approach to Loop Invariant Generation via WP Reasoning


          Table 4 Overall hard benchmark results, obtained across 5 experimental runs.

                     Avg. Success Rate   Std. Dev.    Avg. Refinement    Avg. Repair
      Method
                           (%)              (%)            Iters.           Iters.
      Ad-hoc                14             5.48              -                 -
      NeuroInv*             40             7.07             2.9                -
      NeuroInv              62             10.95            2.9              0.54



     systematic approach employed by NeuroInv* (i.e. NeuroInv’s neural module) in this setting.
         Additionally, the neural module clearly appears to be performing more refinements; the
     average value of 2.9 in Table 4 is an almost 5x increase when compared to the corresponding
     value for the standard benchmark (0.59) – this is likely due to the large increase in the average
     number of loops per program in the hard benchmark. In contrast, the average number of
     repairs being carried out by the symbolic module only increased by approximately 2x (0.54
     vs. 0.24); upon investigation, we found that the vast majority of failures (94%) occurred
     whilst the neural module was performing invariant refinements (i.e. the max number of
     refinements for a particular loop was reached and the process was aborted) – therefore, the
     symbolic module had fewer chances to perform invariant repair.
     Takeaway: NeuroInv scales to complex programs and succeeds ad-hoc prompting by a
     significant margin (+48% points); the application of NeuroInv to hard benchmark programs
     results in more loop invariant refinements being performed by the neural module, and the
     vast majority of observed failures occur during this process (94%).

      4      Discussion
     4.1     Threats to Validity
     The primary threats to the validity of this work stem from our usage of LLMs. The outputs
     of LLMs are inherently stochastic, hence the results of this study are not exactly reproducible
     – we attempt to mitigate this threat by performing multiple experimental runs for each
     evaluation. Data leakage poses a similar threat – data leakage occurs when the information
     from a test set is present in the training data of the LLM. We attempt to alleviate this
     particular threat by deriving a large proportion of our benchmark programs from works
     after the knowledge cut off of o4-mini (i.e. after the 1st of June 2024); additionally, the
     benchmark programs used with origins prior to this date are translations from their original
     programming language (e.g. from C to Java for the Code2Inv derived benchmark programs,
     Section 3.1.1). Another threat arises when considering this work’s sole usage of o4-mini;
     the argument could be made that the results obtained are biased in this respect, and that
     other models, from other vendors, may perform significantly better or worse when used in
     tandem with the methods evaluated (Section 3.1.2).

     4.2     Future Work
     Several avenues of future work arise naturally from this study.
         The links (introduced in Section 2.1) which constitute the backward-chaining WP reas-
     oning of the neural module are currently fragile. In other words, there are currently no
     strong guarantees about what these links produce; for example, the weakest preconditions
     produced by the loop-free link type (Fig. 2) are not formally verified in any capacity – we
D. King, V. Koutavas, and L. Kovács                                                                 15


assume that if the final loop invariant(s) for a given program are correct, then the constituent
WPs are likely correct also. This use of unverified LLM-generated WPs is not without basis,
prior works such as [17] and [16] show that reasoning models can often generate correct
method-level WPs without additional tool intervention or feedback. Alleviating the fragility
of these links by incorporating a verifier earlier in the invariant generation process will allow
for potential errors to become localised; we leave this intervention to future work.
    In a similar vein, Section 3.2.3 highlights an inherent flaw of the neural module. The
current implementation has no recourse to backtrack along its reasoning process when it finds
that the final generated weakest precondition for a program does not satisfy Definition 3.
Implementing this ability to effectively backtrack is a valuable line of future work; the
results of Section 3.2.3 suggest that a solution to this issue will enable the neural module to
effectively generate more correct loop invariants without need for feedback from OpenJML.
    The expansion and standardisation of the hard benchmark (Section 3.3) is another relevant
line of future work; to the best of our knowledge, a similar such benchmark of difficult (i.e.
containing 2+ loops over multiple arrays, etc.) Java-based loop invariant generation problems
does not exist.


 5     Related Work
Loop invariant generation is a central challenge in automated program verification. While
no complete solution can exist due to theoretical limitations, substantial prior work has
approached the problem through a variety of methods.

5.1    Traditional Techniques
We define traditional techniques as those that do not employ a learning-based approach or
rely on LLMs; these techniques span the spectrum of dynamic and static program analysis.
    Dynamic approaches attempt to infer loop invariants from program execution traces.
Daikon [7], a popular invariant generation tool for Java, attempts to derive invariants
(including pre- and postconditions) for a given program from its test suite traces. Despite its
capabilities, Daikon is innately constrained by the quality and coverage of the given test-suite;
as a consequence, the invariants that Daikon generates may not hold universally.
    On the other hand, static approaches attempt to reason about loop invariants without
program execution; these techniques typically rely upon strong theoretical foundations
and make stronger guarantees when compared to dynamic approaches. A wide array of
techniques have evolved in this space and found application towards loop invariant generation,
e.g. abstract interpretation [4], logical abduction [1], recurrence analysis [13], symbolic
execution [21], etc. These techniques tend to excel within their well-defined contexts, but
fail to scale and generalise more broadly.

5.2    Learning- and LLM-Based Approaches
Learning-based approaches utilise machine learning in some capacity to aid loop invariant
generation. Code2Inv [26] is a prime example of such an approach: it uses deep reinforcement
learning (RL) to learn loop invariants through interactions with a proof checker. In a similar
vein, LIPuS [30] uses RL-based pruning and SMT solving to generate loop invariants.
    More recently, researchers have begun to explore the use of LLMs in generating program
properties such as weakest preconditions [16, 17], postconditions [6], and full program
specifications [19]. Concurrently, researchers have also started to investigate the use of
16   A Neurosymbolic Approach to Loop Invariant Generation via WP Reasoning


     LLMs for generating loop invariants; the works of [15, 23, 14] lay the foundations for such
     investigations and establish the notion that LLMs can indeed generate useful loop invariants.
     Since then, a plethora of further works has emerged.
         The authors of [24] generate loop invariant candidates with LLMs; these are then validated
     by the Vampire theorem prover [18] and used to replace loops in the context of bounded model
     checking [3]. Similarly, the work of [28] uses both LLMs and bounded model checking: their
     method employs LLMs to generate loop invariant candidates and bounded model checking
     to filter incorrect predicates. The Lemur framework [29] uses LLMs to generate and repair
     candidate loop invariants, which are then used within the ESBMC [20] and UAutomizer [11]
     frameworks for program verification.
         A common theme that emerges from these recent works is the benefit of integrating LLMs
     with formal tools; these approaches can be considered under the umbrella of “neurosymbolic
     AI”. Our work follows a similar tack, but distinguishes itself through: (1) systematic backward
     chaining using LLM-based weakest precondition reasoning; (2) dual-level neurosymbolic
     refinement and repair that combines internal, LLM-based Hoare-logic reasoning with external
     OpenJML feedback; (3) automatic handling of (sequentially composed) multi-loop programs;
     and (4) a focus on Java, in contrast to existing works which primarily target C.


      6     Conclusion
     This paper presents NeuroInv, a neurosymbolic approach to loop invariant generation that
     features dual-level refinement and repair. NeuroInv contains two key modules: (1) a neural
     reasoning module that leverages LLMs and Hoare logic to derive and refine candidate loop
     invariants via backward-chaining weakest precondition reasoning, and (2) a verification-guided
     symbolic module that iteratively repairs invariants using counterexamples from OpenJML.
         We evaluate NeuroInv on a comprehensive benchmark of 150 Java programs, this bench-
     mark features programs which include: single loops, multiple (sequential) loops, multiple
     arrays, random branching, and noisy code segments. NeuroInv achieves a 99.5% success rate,
     substantially outperforming ad-hoc prompting (66.4%), neural-only ablations (84.7%), and a
     state-of-the-art LLM-based specification generator for Java (28.5%) [19].
         Additionally, a hard benchmark of 10 larger multi-loop programs (containing an average
     of 7 loops) further demonstrates that NeuroInv scales to more complex contexts. In this
     setting, the performance gap between NeuroInv and ad-hoc prompting widens, with NeuroInv
     achieving a success rate of 62%, whilst ad-hoc prompting only achieves 14%.
         Given the results achieved, NeuroInv constitutes an effective framework for loop invariant
     generation. The future work we have outlined is intended to extend this neurosymbolic
     approach to broader and more demanding verification scenarios.


          References
      1   Cristiano Calcagno, Dino Distefano, and Viktor Vafeiadis. Bi-abductive resource invariant
          synthesis. In Asian Symposium on Programming Languages and Systems, pages 259–274.
          Springer, 2009.
      2   Mark Chen.         Evaluating large language models trained on code.          arXiv preprint
          arXiv:2107.03374, 2021.
      3   Edmund Clarke, Armin Biere, Richard Raimi, and Yunshan Zhu. Bounded model checking
          using satisfiability solving. Formal methods in system design, 19(1):7–34, 2001.
      4   Patrick Cousot and Radhia Cousot. Abstract interpretation: a unified lattice model for static
          analysis of programs by construction or approximation of fixpoints. In Proceedings of the 4th
D. King, V. Koutavas, and L. Kovács                                                                   17


     ACM SIGACT-SIGPLAN symposium on Principles of programming languages, pages 238–252,
     1977.
 5   Edsger W. Dijkstra. Guarded commands, nondeterminacy and formal derivation of programs.
     Commun. ACM, 18(8):453–457, August 1975. URL: https://doi-org.elib.tcd.ie/10.1145/
     360933.360975, doi:10.1145/360933.360975.
 6   Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, and Shuvendu K Lahiri. Can large
     language models transform natural language intent into formal method postconditions? Pro-
     ceedings of the ACM on Software Engineering, 1(FSE):1889–1912, 2024.
 7   Michael D Ernst, Jeff H Perkins, Philip J Guo, Stephen McCamant, Carlos Pacheco, Matthew S
     Tschantz, and Chen Xiao. The daikon system for dynamic detection of likely invariants. Science
     of computer programming, 69(1-3):35–45, 2007.
 8   Cormac Flanagan and K Rustan M Leino. Houdini, an annotation assistant for esc/java. In
     International Symposium of Formal Methods Europe, pages 500–517. Springer, 2001.
 9   Robert W Floyd. Assigning meanings to programs1 . Mathematical Aspects of Computer
     Science, 19:19, 1967.
10   Artur d’Avila Garcez and Luis C Lamb. Neurosymbolic ai: The 3 rd wave. Artificial Intelligence
     Review, 56(11):12387–12406, 2023.
11   Matthias Heizmann, Daniel Dietsch, Marius Greitschus, Jan Leike, Betim Musa, Claus Schätzle,
     and Andreas Podelski. Ultimate automizer with two-track proofs: (competition contribution).
     In International Conference on Tools and Algorithms for the Construction and Analysis of
     Systems, pages 950–953. Springer, 2016.
12   C. A. R. Hoare. An axiomatic basis for computer programming. Commun. ACM, 12:576–580,
     October 1969.
13   Andreas Humenberger, Maximilian Jaroschek, and Laura Kovács. Invariant generation for
     multi-path loops with polynomial assignments. In International Conference on Verification,
     Model Checking, and Abstract Interpretation, pages 226–246. Springer, 2017.
14   Christian Janßen, Cedric Richter, and Heike Wehrheim. Can chatgpt support software
     verification? In International Conference on Fundamental Approaches to Software Engineering,
     pages 266–279. Springer, 2024.
15   Adharsh Kamath, Aditya Senthilnathan, Saikat Chakraborty, Pantazis Deligiannis, Shuvendu K
     Lahiri, Akash Lal, Aseem Rastogi, Subhajit Roy, and Rahul Sharma. Finding inductive loop
     invariants using large language models. arXiv preprint arXiv:2311.07948, 2023.
16   Daragh King, Vasileios Koutavas, and Laura Kovacs. Fuzzfeed: An automatic approach to
     weakest precondition generation using llms and fuzzing, 2025. URL: https://arxiv.org/abs/
     2507.05272, arXiv:2507.05272.
17   Daragh King, Vasileios Koutavas, and Laura Kovács. Llm-based generation of weakest
     preconditions and precise array invariants. In 2025 IEEE/ACM 13th International Conference
     on Formal Methods in Software Engineering (FormaliSE), pages 1–5, 2025. doi:10.1109/
     FormaliSE66629.2025.00016.
18   Laura Kovács and Andrei Voronkov. First-order theorem proving and vampire. In International
     Conference on Computer Aided Verification, pages 1–35. Springer, 2013.
19   Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. Specgen: Automated generation of
     formal program specifications via large language models. arXiv preprint arXiv:2401.08807,
     2024.
20   Rafael Sá Menezes, Mohannad Aldughaim, Bruno Farias, Xianzhiyu Li, Edoardo Manino,
     Fedor Shmarov, Kunjian Song, Franz Brauße, Mikhail R Gadelha, Norbert Tihanyi, et al.
     Esbmc v7. 4: Harnessing the power of intervals: (competition contribution). In International
     Conference on Tools and Algorithms for the Construction and Analysis of Systems, pages
     376–380. Springer, 2024.
21   ThanhVu Nguyen, Matthew B Dwyer, and Willem Visser. Symlnfer: Inferring program
     invariants using symbolic states. In 2017 32nd IEEE/ACM International Conference on
     Automated Software Engineering (ASE), pages 804–814. IEEE, 2017.
18   A Neurosymbolic Approach to Loop Invariant Generation via WP Reasoning


     22    OpenAI.        introducing-o3-and-o4-mini, 2025.          URL: https://openai.com/index/
           introducing-o3-and-o4-mini/.
     23    Kexin Pei, David Bieber, Kensen Shi, Charles Sutton, and Pengcheng Yin. Can large language
           models reason about program invariants? In International Conference on Machine Learning,
           pages 27496–27520. PMLR, 2023.
     24    Muhammad AA Pirzada, Giles Reger, Ahmed Bhayat, and Lucas C Cordeiro. Llm-generated
           invariants for bounded model checking without loop unrolling. In Proceedings of the 39th
           IEEE/ACM International Conference on Automated Software Engineering, pages 1395–1407,
           2024.
     25    Sander Schulhoff, Michael Ilie, Nishant Balepur, Konstantine Kahadze, Amanda Liu, Chenglei
           Si, Yinheng Li, Aayush Gupta, HyoJung Han, Sevien Schulhoff, et al. The prompt report: a
           systematic survey of prompt engineering techniques. arXiv preprint arXiv:2406.06608, 2024.
     26    Xujie Si, Aaditya Naik, Hanjun Dai, Mayur Naik, and Le Song. Code2inv: A deep learn-
           ing framework for program verification. In International Conference on Computer Aided
           Verification, pages 151–164. Springer, 2020.
     27    Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He, Haokun Li, Shing-Chi
           Cheung, and Cong Tian. Enchanting program specification synthesis by large language models
           using static analysis and program verification. In International Conference on Computer Aided
           Verification, pages 302–328. Springer, 2024.
     28    Guangyuan Wu, Weining Cao, Yuan Yao, Hengfeng Wei, Taolue Chen, and Xiaoxing Ma. Llm
           meets bounded model checking: Neuro-symbolic loop invariant inference. In Proceedings of
           the 39th IEEE/ACM International Conference on Automated Software Engineering, pages
           406–417, 2024.
     29    Haoze Wu, Clark Barrett, and Nina Narodytska. Lemur: Integrating large language models in
           automated program verification. arXiv preprint arXiv:2310.04870, 2023.
     30    Shiwen Yu, Ting Wang, and Ji Wang. Loop invariant inference through smt solving enhanced
           reinforcement learning. In Proceedings of the 32nd ACM SIGSOFT International Symposium
           on Software Testing and Analysis, pages 175–187, 2023.


     A        Prompts

          Listing 1 Ad-hoc prompt for loop invariant generation.
     Compute the loop invariant ( s ) for the loop ( s ) in the following Java
     code . Please use the format of JML annotations . Annotate the loop ( s )
     with the invariant ( s ). Provide no additional explanations beyond the
     program code and the required annotation . Reason through your
     solution internally .


          Listing 2 The NeuroInv prompt for weakest precondition calculations.
     ** Task : Calculate Weakest Precondition **

     You are given a Java program with segmented code . Your task is to
     calculate the weakest precondition ( WP ) for a specific code
     segment with respect to a given postcondition .

     ** Segmented Program :**
     ‘‘‘ java
     { segmented_program }
     ‘‘‘

     ** Code Segment to Analyze :**
D. King, V. Koutavas, and L. Kovács                                          19


Segment index : { segment_index } { tag_description }

** Postcondition ( must be true AFTER the segment executes ):**
{ postcondition }

** Instructions :**
1. Identify the code segment between the specified tags
2. Apply weakest precondition calculus rules to work backward
through the statements
3. For assignments : WP ( x := e , R ) = R [ x -> e ] ( substitute e for x
in R )
4. For sequences : WP ( S1 ; S2 , R ) = WP ( S1 , WP ( S2 , R ))
5. For conditionals : WP ( if B then S1 else S2 , R ) = ( B = > WP ( S1 ,
R )) AND ( NOT B = > WP ( S2 , R ))
6. Simplify your result as much as possible
7. Express the result using logical notation
( AND , OR , = > , NOT , FORALL , EXISTS )

** Example :**
For code segment : ‘x = x + 1; ‘ with postcondition : ‘x > 5 ‘
The WP would be : ‘x + 1 > 5 ‘ which simplifies to ‘x > 4 ‘


  Listing 3 The NeuroInv prompt for loop invariant generation.
** Task : Generate Loop Invariant **

You are given a Java program with segmented code . Your task is to
generate a suitable loop invariant for a specific while loop .

** Segmented Program :**
‘‘‘ java
{ segmented_program }
‘‘‘

** While Loop to Analyze :**
Loop index : { loop_index } ( between tags ‘// while { loop_index }
open ‘ and ‘// while { loop_index } close ‘)

** Loop Postcondition ( must be true after loop exits ):**
{ lo op _postcondition }

** Instructions :**
1. Identify the while loop between the specified tags
2. Extract the loop guard condition B
3. Analyze the loop body to understand what the loop does
4. Generate the weakest possible loop invariant I that :
    - Is true before the first iteration ( initialization )
    - Is preserved by each iteration ( I AND B = > WP ( loop_body , I ))
    - Combined with loop exit ( I AND NOT ( B )) establishes the loop
    postcondition , { loop_postcondition }
5. Express the invariant using logical notation
( AND , OR , = > , NOT , FORALL , EXISTS )

** A good loop invariant typically includes :**
- Bounds on loop variables ( e . g . , 0 <= i <= N )
20   A Neurosymbolic Approach to Loop Invariant Generation via WP Reasoning


     - Relationships between variables ( e . g . , i < j )
     - Quantified properties about arrays / data structures ( e . g . ,
     FORALL ( k ). 0 <= k < i = > a [ k ] > 0)
     - Progress measures ( what has been accomplished so far and what
     remains to be accomplished )

     Note : when an existential quantifier is needed in the loop
     invariant , perform the following steps :
     1. Introduce and initialise a ghost variable before the loop
     2. Add a "// @ set " annotation at the end of the loop body to show
     how this variable needs to change
     3. Express the invariant in terms of this variable


       Listing 4 The NeuroInv prompt for checking implication one.
     ** Task : Verify Implication One ( Loop Preservation )**

     You are given a loop invariant and must verify that it is
     preserved through one iteration of the loop .

     ** Segmented Program :**
     ‘‘‘ java
     { segmented_program }
     ‘‘‘

     ** While Loop :**
     Loop index : { loop_index } ( between tags ‘// while { loop_index }
     open ‘ and ‘// while { loop_index } close ‘)

     ** Loop Invariant ( I ):**
     { loop_invariant }

     ** Loop Guard ( B ):**
     { loop_guard }

     ** Weakest Precondition of Loop Body w . r . t . I :**
     WP ( loop_body , I ) = { wp_loop_body }

     ** Implication to Verify :**
     I AND B = > WP ( loop_body , I )

     ** Explanation :**
     If the invariant holds and the loop continues ( guard is true ) ,
     does executing the loop body preserve the invariant ?

     ** CRITICAL CONSTRAINT :**
     A loop invariant must be ** self - sufficient ** for formal
     verification . You may ONLY use ‘I AND B ‘ to prove WP ( loop_body , I ).
     You MUST NOT reference :
     - Method preconditions
     - Variable values from before the loop
     - Any facts not explicitly stated in the invariant I

     If you need external facts ( like preconditions ) to complete the
     proof , the implication ** does NOT hold ** - the invariant is
D. King, V. Koutavas, and L. Kovács                                    21


insufficient and must be strengthened .

** Instructions :**
1. Assume ONLY that I and B are true
2. Using ONLY these facts , determine if WP ( loop_body , I )
logically follows
3. Do NOT use preconditions , even if variables are unmodified
4. If you need any additional facts to prove WP ( loop_body , I ) ,
the implication FAILS
5. If it fails , identify exactly what facts are missing from the
invariant


  Listing 5 The NeuroInv prompt for checking implication two.
** Task : Verify Implication Two ( Loop Termination Correctness )**

You are given a loop invariant and must verify that when the loop
exits , the desired loop postcondition is satisfied .

** Segmented Program :**
‘‘‘ java
{ segmented_program }
‘‘‘

** While Loop :**
Loop index : { loop_index } ( between tags ‘// while { loop_index }
open ‘ and ‘// while { loop_index } close ‘)

** Loop Invariant ( I ):**
{ loop_invariant }

** Loop Guard ( B ):**
{ loop_guard }

** Loop Postcondition ( must be true after loop exits ):**
{ lo op _postcondition }

** Implication to Verify :**
I AND NOT ( B ) = > LoopPostCondition

** Explanation :**
If the invariant holds and the loop exits ( guard is false ) , is
the loop postcondition satisfied ?

** CRITICAL CONSTRAINT :**
A loop invariant must be ** self - sufficient ** for formal
verification . You may ONLY use ‘I AND NOT ( B ) ‘ to prove the loop
postcondition . You MUST NOT reference :
- Method preconditions
- Variable values from before the loop
- Any facts not explicitly stated in the invariant I

If you need external facts ( like preconditions ) to complete the
proof , the implication ** does NOT hold ** - the invariant is
insufficient and must be strengthened .
22   A Neurosymbolic Approach to Loop Invariant Generation via WP Reasoning



     ** Instructions :**
     1. Assume ONLY that I and NOT ( B ) ( negation of the loop guard ) are
     true
     2. Using ONLY these facts , determine if the loop postcondition
     logically follows
     3. Do NOT use preconditions , even if variables are unmodified
     4. If you need any additional facts to prove the loop
     postcondition , the implication FAILS
     5. If it fails , identify exactly what facts are missing from the
     invariant


       Listing 6 The NeuroInv prompt for loop invariant refinement.
     ** Task : Refine Loop Invariant **

     A loop invariant has failed verification . Your task is to refine
     it by strengthening or adjusting it to satisfy the Hoare logic
     requirements .

     ** Segmented Program :**
     ‘‘‘ java
     { segmented_program }
     ‘‘‘

     ** While Loop :**
     Loop index : { loop_index } ( between tags ‘// while { loop_index }
     open ‘ and ‘// while { loop_index } close ‘)

     ** Current Invariant ( FAILED ):**
     { current_invariant }

     ** Failed Implication :**
     { implication_name }

     ** Failure Reason :**
     { failure_reason }

     { r efinement_guidance }

     ** Instructions :**
     1. Analyze why the current invariant failed
     2. Identify what additional conditions or strengthenings are
     needed
     3. Propose a refined invariant that :
         - Still holds initially ( before the first iteration )
         - Is strong enough to pass the failed implication
         - Is not overly restrictive ( can be maintained by the loop )
     4. Explain your refinement strategy


       Listing 7 Refinement guidance for implication one failures.
     ** Refinement Strategy for Implication One :**
     - The invariant is not preserved through the loop body
     - The invariant must be self - sufficient - it cannot rely on
D. King, V. Koutavas, and L. Kovács                                        23


preconditions or external facts
- Consider strengthening the invariant by adding conditions about :
   - Facts from preconditions about unmodified variables / arrays
   ( if needed to prove preservation )
   - Variables modified in the loop body
   - Relationships that must be maintained across iterations
   - Bounds that are always respected
   - Properties that hold before and after each iteration
- Ensure the strengthened invariant still allows initialization
( holds before first iteration )


  Listing 8 Refinement guidance for implication two failures.
** Refinement Strategy for Implication Two :**
- The invariant + loop exit doesn ’ t imply the loop postcondition
- The invariant must be self - sufficient - it cannot rely on
preconditions or external facts
- Consider strengthening the invariant to explicitly include :
   - Facts from preconditions about unmodified variables / arrays
   ( e . g . , if precondition says a [ k ] >= k and ’a ’ is never
   modified , add this to the invariant )
   - Properties that hold throughout but aren ’ t stated in the
   current invariant
   - What has been accomplished when the loop exits
   - Relationships needed for the loop postcondition
   - Quantified properties over the full range
- Ensure the strengthened invariant can still be preserved by the
loop


  Listing 9 The NeuroInv prompt for loop invariant repair.
** Task **
For the Java method { method_name } shown below ( under ** Program **) ,
repair ONLY the loop specifications to resolve the
verification issues identified by OpenJML .
Specifically :
- You MAY modify loop invariants and , if present , the loop
variant ( decreases clause ).
- You MUST NOT modify method preconditions , postconditions ,
assignable clauses , or any other JML specifications outside of
the loop .
- You MUST NOT modify the Java code .

The OpenJML output ( under ** OpenJML Output **) describes the
failures . Use it carefully to strengthen the loop invariant and /
or adjust the variant to ensure inductiveness and termination as
required .

** Scope **
- Allowed changes :
   - Loop invariants
   - Loop variants ( if present )
- Forbidden changes ( leave exactly as - is ):
   - Method - level requires / ensures / assignable clauses
   - Class - level specifications
24   A Neurosymbolic Approach to Loop Invariant Generation via WP Reasoning


       - Any Java implementation code

     ** Deliverable **
     Return the complete program with only the loop invariant ( s ) ( and
     variant ( s ) , if present ) updated . Do not include explanations or
     comments beyond what is explicitly requested .

     ** OpenJML Output **
     { openjml_output }

     ** Program **
     { program }
