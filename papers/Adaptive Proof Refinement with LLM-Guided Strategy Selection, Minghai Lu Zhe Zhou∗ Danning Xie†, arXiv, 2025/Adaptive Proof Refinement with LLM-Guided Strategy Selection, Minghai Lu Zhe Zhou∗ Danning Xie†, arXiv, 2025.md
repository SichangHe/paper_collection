                                        Adaptive Proof Refinement with LLM-Guided Strategy Selection
                                                             Minghai Lu                                                Zhe Zhou∗                                  Danning Xie†
                                                         Purdue University                                         Purdue University                                   Meta
                                                        West Lafayette, USA                                       West Lafayette, USA                             Menlo Park, USA
                                                        lu1074@purdue.edu                                        zhou956@purdue.edu                               dxie@meta.com

                                                             Songlin Jia                                       Benjamin Delaware                                  Tianyi Zhang
                                                         Purdue University                                         Purdue University                             Purdue University
                                                        West Lafayette, USA                                       West Lafayette, USA                           West Lafayette, USA
                                                        jia137@purdue.edu                                         bendy@purdue.edu                              tianyi@purdue.edu
arXiv:2510.25103v2 [cs.SE] 9 Sep 2026




                                        Abstract                                                                                1   Introduction
                                        Formal verification via theorem proving enables rigorous proofs                         Interactive theorem provers (ITPs) such as Rocq [46] and Lean [37]
                                        of software correctness, but it is difficult to scale due to the signifi-               are powerful tools for formally reasoning about complex software
                                        cant manual effort and expertise required. While Large Language                         systems. These tools have been used to mechanically verify deep
                                        Models (LLMs) have shown potential in automating proof genera-                          correctness properties of safety-critical applications, including com-
                                        tion, they frequently produce incorrect proofs on the first attempt                     pilers [29], distributed systems [50], and OS kernels [20, 26]. These
                                        that require iterative refinement to fix. However, most existing                        successes have come at the cost of significant human effort and
                                        approaches employ fixed refinement strategies and cannot dynami-                        expertise, however, requiring developers to interactively guide the
                                        cally choose an effective strategy, which limits their performance.                     proof assistant step-by-step. The proof of correctness for the Com-
                                        To overcome this limitation, we introduce Adapt, a novel proof re-                      pCert verified C compiler, for example, consists of 100,000 lines of
                                        finement framework that leverages an LLM-guided decision-maker                          proof scripts [29] that took 6 person-years to develop.
                                        to dynamically select a suitable refinement strategy according to                          Motivated by these costs, recent years have seen increasing in-
                                        the state of the proof assistant and available context of an incorrect                  terest in using Large Language Models (LLMs) to automate the
                                        proof. We evaluate Adapt on two benchmark suites against five                           development of proofs in ITPs [13, 19, 33, 47, 49, 53]. Many existing
                                        existing methods and find that it significantly outperforms the best                    approaches adopt an iterative refinement paradigm—they use an
                                        baseline on both by proving 11.26% and 18.58% more theorems, re-                        LLM to generate an initial proof attempt and then incrementally
                                        spectively. Furthermore, we demonstrate Adapt’s generalizability                        repair that proof [10, 19, 33, 34, 49, 51]. Yet they either rely on a
                                        by evaluating it across six different LLMs. We also conduct abla-                       single refinement strategy to repair every proof error [10, 19, 33, 49]
                                        tion studies to measure the contribution of each component and                          or use a set of hard-coded rules to select a repair strategy based
                                        compare the trade-offs of alternative decision-maker designs.                           solely on error messages [34, 51]. This stands in contrast to how hu-
                                                                                                                                man experts fix broken proofs: rather than relying on a single error
                                        CCS Concepts                                                                            message, developers comprehensively analyze the entire context of
                                        • Software and its engineering → Formal software verifica-                              a failed proof attempt to decide between different repair strategies.
                                        tion.                                                                                   For example, they may introduce new helper lemmas when existing
                                                                                                                                ones are insufficient, draw inspiration from similar proofs and reuse
                                        Keywords                                                                                relevant lemmas, or iteratively repair proofs based on ITP feedback.
                                                                                                                                This sort of strategic decision-making is particularly important in
                                        Software and its engineering → Software verification; Formal
                                                                                                                                the ITP setting, where a wrong choice may send a proof down
                                        software verification.
                                                                                                                                an unproductive path, compounding the mistake by significantly
                                        ACM Reference Format:                                                                   increasing proof effort or eventually leading to outright failure.
                                        Minghai Lu, Zhe Zhou, Danning Xie, Songlin Jia, Benjamin Delaware,                         To address this limitation in prior work, we propose Adapt, an
                                        and Tianyi Zhang. 2026. Adaptive Proof Refinement with LLM-Guided
                                                                                                                                adaptive proof refinement framework that emulates the decision-
                                        Strategy Selection. In Proceedings of the 41st IEEE/ACM International Con-
                                                                                                                                making process of human experts. Adapt employs an LLM-guided
                                        ference on Automated Software Engineering (ASE ’26), October 12–16, 2026,
                                        Munich, Germany. ACM, New York, NY, USA, 13 pages. https://doi.org/10.                  decision-maker to analyze the current state of the proof assistant
                                        1145/3832783.3834382                                                                    and available context, then dynamically selects an appropriate strat-
                                                                                                                                egy. As illustrated in Figure 1, when a proof attempt fails, the
                                        ∗ Corresponding author.
                                        † Work done while at Purdue University.
                                                                                                                                decision-maker employs one of three strategies: (1) proposing new
                                                                                                                                helper lemmas, (2) searching for relevant lemmas and proofs to
                                                                                                                                guide the refinement, or (3) regenerating the proof. This iterative
                                                                                                                                process allows Adapt to flexibly adapt its approach at each step,
                                        This work is licensed under a Creative Commons Attribution 4.0 International License.   enabling it to effectively prove complex theorems.
                                        ASE ’26, Munich, Germany
                                        © 2026 Copyright held by the owner/author(s).
                                                                                                                                   Our evaluation of Adapt against three state-of-the-art methods,
                                        ACM ISBN 979-8-4007-2882-2/2026/10                                                      Cobblestone [24], PALM [34] and Rango [47], and two alternative
                                        https://doi.org/10.1145/3832783.3834382
ASE ’26, October 12–16, 2026, Munich, Germany                           Minghai Lu, Zhe Zhou, Danning Xie, Songlin Jia, Benjamin Delaware, and Tianyi Zhang

                                                                           1 (* Definitions *)
                                                                           2 Inductive nat : Set := (* Datatype of natural numbers *)
                                                                           3    | O : nat
                                                                           4    | S : nat -> nat .
                                                                           5 Notation " n + 1" := ( S n ) .
                                                                           6
                                                                           7 Fixpoint leb ( n m : nat ) : bool := (* Comparison function *)
                                                                           8   match n , m with
                                                                           9     | O , _ = > true
                                                                          10     | _ , O = > false
                                                                          11     | n + 1 , m + 1 = > leb n m
                                                                          12   end .
                                                                          13
                                                                          14 Inductive le : nat -> nat -> Prop := (* Comparison relation *)
                                                                          15   | le_n ( n : nat ) : le n n
                                                                          16   | le_S ( n m : nat ) ( H : le n m ) :
                                                                          17     le n ( S m ) .
                                                                          18 Notation " n <= m " := ( le n m ) .
                   Figure 1: Overview of Adapt.                           19
                                                                          20 (* Theorems *)
                                                                          21 Lemma O_le_n : forall n , O <= n .
refinement designs demonstrates its effectiveness. On the CoqStoq         22 Proof .
benchmark [47], Adapt proves 41.33% of 1,171 theorems, outper-            23    intros n . induction n .
forming the strongest baseline by 11.26%. This lead increases to          24    - apply le_n .
                                                                          25    - apply ( le_S O n IHn ) .
18.58% on CoqDev, a new, more challenging benchmark comprised             26 Qed .
of 1,720 theorems that we have developed. Further experiments             27
                                                                          28 Lemma n_le_m_Sn_le_Sm :
confirm the generalizability of Adapt across six LLMs and, through        29   forall n m , n <= m -> ( n + 1) <= ( m + 1) .
ablation studies, validate the contribution of each refinement strat-     30 Proof . (* Proof omitted *) Qed .
egy and the LLM-guided decision-maker.                                    31
                                                                          32 Theorem leb_complete : forall n m ,
   In summary, we make the following contributions:                       33   leb n m = true -> n <= m .
                                                                          34 Proof .
    (1) We propose Adapt, an adaptive proof refinement framework          35   intros n .
                                                                          36   induction n . (* Induction on n *)
        that dynamically selects from different refinement strategies     37   - intros .       (* Base case *)
        based on the proof state and available context.                   38       apply O_le_n .
    (2) We construct CoqDev, a new, more challenging benchmark            39   - intros .       (* Inductive case *)
                                                                          40       destruct m . (* Case analysis on m *)
        mined from real-world Rocq commit histories that model            41       + discriminate .
        the incremental development process.                              42       + apply n_le_m_Sn_le_Sm . (* Use lemma *)
    (3) We conduct a comprehensive evaluation of Adapt on Co-             43         simpl in H . apply IHn in H . apply H .
                                                                          44 Qed .
        qDev and the most recent CoqStoq benchmark, demon-
        strating that Adapt achieves significant improvements over         Figure 2: An example Rocq development that includes a
        state-of-the-art techniques.                                       datatype definition (nat), a recursive function (leb), and an
                                                                           inductive relation (le), two lemmas and a theorem.
2    Background and Motivation                                             is less than or equal to any natural number, and n_le_m_Sn_le_Sm,
To motivate our ideas, Figure 2 presents a self-contained example of       which shows that if n <= m, then n + 1 <= m + 1.
a proof development in Rocq [46]—a widely used theorem prover for
                                                                               Proof State and Context. Given a theorem statement, Rocq enters
software verification and the primary ITP considered in this work.
                                                                           an interactive proof mode and displays the current proof state. This
We start with a brief overview of the proof process in Rocq and
                                                                           state includes the goal (i.e., the obligation that the user needs to
then introduce the problem setting of adaptive proof refinement.
                                                                           prove) and the local context (i.e., any local variables and hypothe-
                                                                           ses used in that goal). The user applies tactics to transform this state
   Definitions and Theorems. As is common in Rocq, the example
                                                                           by, e.g., simplifying the goal or introducing new hypotheses. Rocq
in Figure 2 begins with the definition of data structures, functions,
                                                                           then updates the state or reports an error when tactic application
and inductive relations. Lines 1–4 define Peano natural numbers
                                                                           is invalid. The proof of leb_complete uses the induction tactic
(nat) with a base constructor (O) and an inductive successor con-
                                                                           on n (line 36) and case analysis (destruct) on m (line 40). Figure 3a
structor (S), where S n returns the number that is one more than n.
                                                                           shows the proof state before the tactic on line 38 is applied; the
The file then defines a boolean function leb that recursively checks
                                                                           context is above the double line and the goal is below.
if one number is less than or equal to another, and an inductive
relation le that provides a formal definition of the same concept.            Proof Failure. Rocq reports an error for invalid tactic applications.
   After the definitions, theorems are stated and proven. They             For instance, under the proof state in Figure 3b derived from line
start with the keyword Theorem or Lemma, which are functionally            42 of Figure 2, the erroneous tactic apply n_le_m_Sn_le_Sm in H
identical but used by convention to distinguish key results from           leads to a proof failure. It attempts to perform forward reasoning
helper proofs. The main theorem, leb_complete (line 32), states            by applying the lemma to the hypothesis H, but fails with the error
that if leb n m is true, then n is less than or equal to m. To prove       message: “Unable to apply lemma of type "forall n m : nat, n <= m ->
this, two helper lemmas are required: O_le_n, which proves that O          n + 1 <= m + 1" on hypothesis of type "leb (n + 1) (m + 1) = true"”.
Adaptive Proof Refinement with LLM-Guided Strategy Selection                                            ASE ’26, October 12–16, 2026, Munich, Germany

m : nat
H : leb 0 m = true                                                      to leb_complete, suggesting a similar proof pattern (induction
================================================                        on n, case analysis on m). Of course, naïvely copying the proof of
0 <= m
                                                                        leb_complete and reusing it does not work, since the helper lem-
               (a) Proof state before line 38 in Figure 2.              mas used in leb_complete do not directly apply to leb_correct.
n , m: nat
                                                                        An additional refinement strategy is required: the developer can
IHn : forall m: nat , leb n m = true -> n <= m                          draw inspiration from them to propose and prove a new, necessary
m : nat                                                                 lemma: Sn_le_Sm_n_le_m (Figure 4b).
H : leb (n + 1) (m + 1) = true
================================================                           This example highlights the importance of adaptive proof refine-
n + 1 <= m + 1                                                          ment that integrates multiple proof refinement strategies according to
                                                                        the available context (i.e., local and global context) as well as the cur-
               (b) Proof state before line 42 in Figure 2.
                                                                        rent state of the proof assistant (e.g., partial proof, erroneous tactic,
n : nat                                                                 error message, and proof state). A tool that only retrieves existing
IHn : forall m: nat , n <= m -> leb n m = true                          lemmas would fail because the necessary lemma Sn_le_Sm_n_le_m
m : nat
H : n + 1 <= m + 1                                                      does not exist in the leb_correct example. Conversely, an ap-
================================================                        proach focusing only on lemma discovery would have to generate
leb (n + 1) (m + 1) = true
                                                                        both the new lemmas and proofs from scratch, which is difficult
               (c) Proof state before line 52 in Figure 4a.             and costly without the guidance of existing lemmas and proofs. The
                                                                        core challenge, therefore, is to create a system that can dynamically
Figure 3: Intermediate proof states. (a) shows the goal for             assess the available context and current state of the proof assistant
the base case; (b) shows the inductive step requiring a helper          to select the most promising strategy, like a human expert.
lemma; (c) shows a state during the proof of leb_correct.
                                                                        3     Approach
45 Theorem leb_correct :
46     forall n m , n <= m -> leb n m = true .                          Given a theorem statement to prove, Adapt first generates an initial
47 Proof .                                                              proof and checks it using Rocq. If the proof fails, Adapt captures
     intros n. induction n .             (* Induction on n *)
48
49   - intros . simpl . reflexivity .    (* Base case *)
                                                                        the state of the proof assistant, including the erroneous tactic, the
50   - intros . destruct m .             (* Inductive case *)           proof state at the point of failure, the error message from Rocq, and
51       + inversion H .                                                the partial proof preceding the error. It then initializes a working
52       + apply Sn_le_Sm_n_le_m in H . (* Use lemma *)
53         simpl . apply IHn in H . apply H .                           context by retrieving essential information from the global context,
54 Qed .                                                                including relevant lemmas and similar proofs in the repository.
                                                                           Adapt then iteratively refines the failed proof attempt. In each it-
  (a) A Rocq theorem stating the correctness of the leb function
                                                                        eration, the decision-maker analyzes the state of the proof assistant
  with respect to the le relation, and its proof script.
                                                                        and working context to select and apply a strategy, including lemma
55 Lemma Sn_le_Sm_n_le_m :                                              discovery, context enrichment, and regeneration. If the attempt fails,
56    forall n m , ( n + 1) <= ( m + 1) -> n <= m .
57 Proof . (* Proof omitted *) Qed .
                                                                        Adapt proceeds to the next iteration using the updated state of the
                                                                        proof assistant and working context. This process continues until a
     (b) A helper lemma used in the proof of leb_correct above.         successful proof is found or an iteration limit is reached. The rest
Figure 4: Example of proof construction by searching and                of this section elaborates on each of these components.
reusing existing proofs.
                                                                        3.1     Initial Proof Generation
   Project Management and Refinement Strategies. To manage com-         Adapt’s iterative process begins with an initial proof attempt.
plexity, formal proofs are often organized into a proof project with    Adapt is agnostic to the underlying proof generator, and can freely
multiple files and imported libraries, similar to a software project.   use, e.g., LLM-based [19, 34, 47, 49], deep learning-based [17, 18, 43,
When writing a proof, developers use not only the local context but     52], or symbolic approaches [12]. In this work, we use the retrieval-
also a global context of definitions and theorems from other files      augmented generation method proposed by Lu et al. [34] to generate
and imported libraries. This leads to several refinement strategies.    the initial proof, since it is a recent method with the source code
One common strategy is to search the current project for helpful        publicly available. Specifically, this approach first identifies candi-
lemmas. For example, to make progress from the state in Figure 3b,      date theorems and lemmas using TF-IDF and KNN, then reranks
the proven lemma n_le_m_Sn_le_Sm is applied to the goal, simpli-        them with BM25 [40]. Figure 5 shows the prompt template used to
fying it to n <= m. When no suitable existing lemma is available,       generate the initial proof.1 The prompt includes the target theorem
a developer may need to invent a new one, a strategy known as           statement to be proven, all definitions appearing in the statement,
lemma discovery [9, 23, 28, 44].                                        and the top K relevant theorems and lemmas. When fewer than K
   Similar to how developers search and reuse existing code to write    candidates are available, all are included. In this work, we set K to
new code [41], existing proofs can also serve as a source of inspira-   10 to avoid exceeding the context window limit.
tion in proof construction. For example, suppose a developer, after
proving everything in Figure 2, now wants to prove leb_correct          1 Coq was recently renamed to Rocq. Our experiments were conducted before the

(Figure 4a). The statement of leb_correct is structurally similar       name change; our prompt templates retain the name “Coq”, which was used in our
                                                                        experiments.
ASE ’26, October 12–16, 2026, Munich, Germany                              Minghai Lu, Zhe Zhou, Danning Xie, Songlin Jia, Benjamin Delaware, and Tianyi Zhang


 INSTRUCTIONS                                                                   INSTRUCTIONS
 You will be given a theorem statement written in Coq, with                     We are proving a theorem in Coq but get stuck in a proof state,
 related definitions, theorems, and lemmas. Your job is to write a              you need to select a refinement strategy to fix it. You will be
 proof. You should first analyze how to prove it based on the                   provided with the theorem, and the diagnostic information,
 definitions, and which theorems and lemmas can be used. Leverage               including the stuck proof state, the erroneous tactic that causes
 as many theorems and lemmas as possible to facilitate your proof.              the error, the error message from Coq and the partial proof
 INPUT                                                                          preceding the erroneous tactic. Additional supporting context,
 - Theorem Statement: <theorem>                                                 including related definitions and lemmas, and a similar theorem
                                                                                with its proof are also provided.
 - Definitions: <definitions>                                                   INPUT
 - Theorems and Lemmas: <theorems and lemmas>                                   - Theorem Statement: <theorem>
                                                                                - Definitions: <definitions>
  Figure 5: Prompt template for initial proof generation.
                                                                                - Stuck Proof State: <proof state>

3.2     Context Initialization                                                  - Erroneous Tactic: <erroneous tactic>
                                                                                - Error Message: <error message>
If the initial proof attempt fails, Adapt collects several pieces of in-
                                                                                - Partial Proof: <partial proof>
formation to help guide its iterative refinement loop. It first captures
                                                                                - Theorems and Lemmas: <theorems and lemmas>
the state of the proof assistant, which includes the following:
                                                                                - Similar Proof: <similar proof>
      • Erroneous tactic: the specific tactic that caused the error.            OUTPUT
      • Error message: Rocq’s explanation of why the tactic failed.             Analyze the provided information, then choose one of the
                                                                                following strategies:
      • Partial proof: the proof script before the erroneous tactic.            1. Strategy: Lemma Discovery
      • Stuck proof state: the proof state resulting from the exe-              Description: Propose new lemmas or refine existing ones to help
        cution of the partial proof, which includes the remaining               the proof.
                                                                                 Output Format:‘Lemma Discovery; [name_1, name_2 ...]’ . This
        goals to prove and any local variables and hypotheses that
                                                                                strategy always proposes new lemmas. Optionally, provide the
        are available, as defined in Section 2.                                 names of existing lemmas or theorems to refine. Provide an empty
                                                                                list ‘[]’ to only propose new lemmas.
   The combination of the erroneous tactic, its error message, and              2. Strategy: Context Enrichment
the stuck proof state reveals the immediate cause of failure, while             Description: Retrieve more relevant definitions, lemmas,
the stuck proof state and the partial proof indicate the overall                theorems, and proofs from the project and imported libraries.
progress of the current proof. For instance, a simple syntax error in            Output Format:‘Context Enrichment; [keyword_1, keyword_2,...]’
                                                                                where you list keywords to search for, such as names of
a nearly completed proof could be fixed by regeneration, whereas                definitions or lemmas. Lemmas with the listed keywords in the
a failure near the beginning could signal a more fundamental issue              statements will be retrieved.
with the overall proof strategy. This comprehensive information                 3. Strategy: Regeneration
                                                                                Description: Directly regenerate the proof if the current context
reflects the feedback a human developer receives and enables the                seems sufficient or the previous proof is unpromising.
decision-maker to examine different aspects of the failure and select            Output Format:‘Regeneration’ .
a proper refinement strategy.
   In addition to the state of the proof assistant, Adapt’s refinement                Figure 6: Prompt template for decision-making.
loop maintains a working context that guides its decision-maker
and refinement strategies. Adapt initializes this context with the            reasons and assess the sufficiency of the current context for solving
statements of theorems and lemmas retrieved during the initial                the proof goal. Based on the analysis, the LLM is asked to select
proof generation, and the proof script of a similar theorem from the          one of three predefined strategies. We do not claim that these three
global context. Due to the context window limit of the LLM, we only           strategies are complete, as other useful refinement strategies may
include one proof script as an example. This proof provides a poten-          exist. Our goal is to demonstrate the effectiveness of adaptively se-
tial proof structure to guide subsequent proof attempts. Following            lecting from different refinement strategies, rather than to propose
prior work [47], we select a similar theorem using BM25 [40], which           all possible strategies.
compares the textual similarity between the statement of the target
theorem and the statements of other theorems in the global context.               (1) Lemma discovery: When a proof goal is too complex to be
We select the theorem with the highest similarity score and include                   solved directly with the available context, human developers
its proof, without setting a minimum similarity threshold. This                       often propose new helper lemmas to decompose the proof
initialized context is then provided to the decision-maker to select                  into manageable sub-tasks. This process, known as lemma
the refinement strategy.                                                              discovery, has been proven to be effective when leveraging
                                                                                      LLMs to propose new lemmas [9, 49]. Inspired by this, we in-
3.3     Decision-Maker                                                                tegrate the lemma discovery strategy to generate lemmas to
Adapt leverages the reasoning capabilities of LLMs to decide which                    decompose complex proof goals. As shown in Figure 6, when
refinement strategy to take based on both the current project and                     selecting this strategy, the decision-maker is also prompted
state of the proof assistant described in Section 3.2. Figure 6 shows                 to propose a set of existing theorems and lemmas that can
the prompt template for decision making. Specifically, Adapt pro-                     be potentially adapted to generate a new lemma.
vides the LLM with the target theorem statement and the definitions               (2) Context enrichment: This strategy is designed to address
that appear in it, the state of the proof assistant, and the working                  failures caused by an insufficient working context by search-
context. The prompt then instructs the LLM to analyze the failure                     ing for additional definitions, lemmas, theorems, and proofs.
Adaptive Proof Refinement with LLM-Guided Strategy Selection                                        ASE ’26, October 12–16, 2026, Munich, Germany


       The decision-maker is also prompted to provide a set of key-      INSTRUCTIONS
                                                                         We are proving a theorem in Coq but get stuck in a proof state,
       words to guide the following context enrichment process,          your task is to propose some new lemma statements to help solve
       such as the names of definitions or lemmas present in the         it. You will be given the theorem statement and proof state,
       stuck proof state.                                                together with related definitions, existing theorem and lemmas.
                                                                         Your lemmas must state new, non-trivial properties. For each
   (3) Regeneration: This strategy is employed to either repair          proposed lemma statement, explain why it is correct and useful.
       simple errors, such as a syntax mistake, or to try a new          INPUT
       proof approach when the previous proof contains significant       - Theorem Statement: <theorem>
       errors, such as applying induction on wrong variables or          - Proof State: <proof state>
       failing to generalize the induction hypothesis correctly.         - Definitions: <definitions>
                                                                         - Existing Theorems and Lemmas: <theorems and lemmas>
   Alternative decision-maker designs offer different trade-offs in
terms of performance and cost. Section 4.7 explores decision-makers       Figure 7: Prompt template for proposing new lemmas.
based on heuristic rules and machine learning (ML) models. We
describe each refinement strategy in the following sections.            to reuse the original proof to simplify the proof generation task.
                                                                        Finally, Adapt validates each refined lemma by executing its state-
3.4     Lemma Discovery Strategy                                        ment and proof in Rocq. Only those lemmas with both a well-formed
                                                                        statement and a correct proof are added to the working context.
Lemma discovery takes as input the theorem statement, the stuck
                                                                           After updating the working context, Adapt prompts an LLM
proof state, and the working context. The stuck proof state can
                                                                        to regenerate a proof. The prompt provides the original theorem
reveal the specific difficulty encountered by the proof assistant,
                                                                        statement, the updated working context, and the state of the proof
which helps Adapt generate lemmas tailored to the specific obstacle.
                                                                        assistant from the prior proof failure. It also instructs the LLM to
For example, the proof state in Figure 3c suggests that a lemma
                                                                        leverage the new lemmas in its proof attempt.
establishing (n + 1) <= (m + 1) -> n <= m could be helpful,
as it bridges the hypotheses H and IHn. Besides proposing new
                                                                         INSTRUCTIONS
lemmas directly, Adapt also refines existing lemmas selected by the      We are proving a theorem in Coq but get stuck in a proof state,
decision-maker (described in Section 3.3) to maximize the chance         your task is to refine an existing lemma to help solve it. You
of finding useful lemmas, since existing lemmas may inspire the          will be given the theorem statement to prove, the stuck proof
                                                                         state, related definitions and the specific lemma to refine,
generation of similar lemmas tailored for the stuck proof state.         including its proof. A set of existing theorems and lemmas are
Adapt applies both mechanisms rather than choosing between the           also provided. First analyze how to adapt this given lemma to
                                                                         help solve the proof goal, then produce the refined lemma
two. We elaborate on these two mechanisms below.                         statement together with its proof. Try to reuse the original
   Directly Propose New Lemmas. Proposing new lemmas re-                 proof of the given lemma where possible.
quires an agent not only to formulate a statement that is both           INPUT
syntactically valid and helpful, but also to generate a correct proof    - Theorem Statement: <theorem>
                                                                         - Proof State: <proof state>
of the statement. To address this, Adapt employs a two-stage pro-
cess that decouples the generation of lemma statements from the          - Definitions: <definitions>
generation of their proofs.                                              - Existing Theorems and Lemmas: <theorems and lemmas>
   In the first stage, an LLM is instructed to generate statements of    - Lemma to Refine: <lemma and proof>

new lemmas. As shown in the prompt in Figure 7, it is provided with
                                                                         Figure 8: Prompt template for adapting existing lemmas.
existing theorems and lemmas in the working context and stuck
proof state, so that it can generate semantically relevant lemma
statements, while avoiding redundant lemmas that already exist.         3.5   Context Enrichment Strategy
These generated statements are then checked by Rocq for syntactic       When this strategy is selected, Adapt searches for additional defi-
and semantic correctness. Any invalid statements are discarded.         nitions, lemmas, theorems, and proofs from the global context to
   In the second stage, Adapt attempts to generate a proof for each     enrich its working context. Specifically, the decision-maker iden-
valid lemma statement, using the same procedure as the initial proof    tifies a set of keywords based on the state of the proof assistant
generation described in Section 3.1. The statement of a successfully    and context, as described in Section 3.3. Adapt then performs a
proven lemma is added to the working context.                           targeted search by matching these keywords against the statements
   Adapt Existing Lemmas. Some existing theorems and lemmas,            of available theorems and lemmas. For example, recognizing that
while not directly applicable, can be adapted to work in the current    the proof state in Figure 3c involves the relation le and function
proof. For example, the existing lemma n_le_m_Sn_le_Sm (Figure 2,       leb, the LLM may suggest these terms as keywords to find more
line 28) cannot be applied to the proof state in Figure 3c. However,    relevant lemmas when the existing ones are deemed insufficient.
a human developer might observe that its converse could be helpful      Similarly, if Adapt has retrieved the proof of leb_complete, it
and propose the new lemma Sn_le_Sm_n_le_m shown in Figure 4b.           may identify the lemmas n_le_m_Sn_le_Sm and O_le_n used in
   To refine a theorem or lemma selected by the decision-maker,         its proof, and generate their names as keywords if they are not
Adapt provides an LLM with its statement and proof. The prompt,         in the working context. Subsequently, Adapt employs the same
as shown in Figure 8, instructs the LLM to analyze how the lemma        proof generation procedure used after lemma discovery described
can be adapted to solve the proof goal. It then directs the model       in Section 3.4, but supplies it with the enriched working context
to generate both the refined statement and proof, encouraging it        and instructs the LLM to leverage the newly retrieved context.
ASE ’26, October 12–16, 2026, Munich, Germany                           Minghai Lu, Zhe Zhou, Danning Xie, Songlin Jia, Benjamin Delaware, and Tianyi Zhang


 INSTRUCTIONS                                                                    • RQ5: How does Adapt’s iteration limit impact its perfor-
 I’m proving a theorem in Coq but got stuck in a proof state. You
 will be given the theorem statement to prove and the diagnostic
                                                                                   mance?
 information, including the stuck proof state, the erroneous
 tactic that causes the error, the error message from Coq and the
 partial proof preceding the erroneous tactic. Additional context,         4.1      Benchmarks
 including related definitions, theorems and lemmas, and a similar         We perform experiments using two different sets of benchmarks.
 theorem with its proof are also provided. First analyze how to
 prove the theorem based on the provided context, then write a             The first is CoqStoq, a state-of-the-art benchmark based on 14 real-
 correct proof. You can repair the proof if the error is simple,           world Rocq projects on GitHub [47]. We use its cut-off split, created
 or generate a new proof if the prior proof is infeasible.
 INPUT
                                                                           to mitigate data leakage issues, consisting of 1,171 theorems.
 - Theorem Statement: <theorem>                                                We have also built a new set of benchmarks, called CoqDev,
    - Stuck Proof State: <proof state>                                     that represents a more realistic and challenging setting for auto-
    - Erroneous Tactic: <erroneous tactic>
                                                                           matic proof generation. The motivation is based on our observation
    - Error Message: <error message>                                       that proof generation tasks from existing benchmarks are typically
    - Partial Proof: <partial proof>
                                                                           constructed by simply omitting the proof of the target theorem,
                                                                           leaving any helper lemmas and similar proofs available to the LLM.
    - Definitions: <definitions>
                                                                           In practice, however, the relevant helper lemmas are introduced
    - Theorems and Lemmas: <theorems and lemmas>
                                                                           while constructing a proof, and similar proofs may be subsequently
    - Similar Proof: <similar proof>
                                                                           introduced after the commit of the proof. In other words, this sim-
          Figure 9: Prompt template for regeneration.                      ple masking-in-the-middle evaluation setting provides the LLM
                                                                           with important information that may not exist when the proof was
   This design contrasts with prior work [47], which selects theo-         actually written. Therefore, this setup may not fully reflect the
rems and lemmas by assessing the similarity between their state-           capabilities of proof generation tools in real-world settings.
ments and the entire proof state. The intuition is that the entire             We constructed CoqDev by mining the commit histories of
proof state may contain terms that are not critical for making             open-source Rocq projects on GitHub. Specifically, we searched for
progress and therefore using the entire proof state in a query can         projects using Rocq as their primary language as of February 20,
retrieve irrelevant theorems and lemmas or miss important ones.            2025, and ranked them by creation date, prioritizing newer projects
For example, in Figure 3c, the proof state contains common types           to mitigate potential data leakage. We only included projects that
like nat and bool. Including them in the query would lead the              can be built automatically with Makefile or _CoqProject, resulting in
retrieval system to fetch broadly related but unhelpful lemmas             a final set of 14 projects. These projects span a range of verification
about natural numbers or booleans, potentially missing a lemma             domains, including logic, data structures, programming languages,
n_le_m_Sn_le_Sm particularly relevant to the inequality in the cur-        and mathematics. We collected all commits of each selected project
rent goal. Section 4.6 validates this design choice by comparing           to get 2,225 commits in total. Next, we compare each commit against
Adapt to Adapt_full_state, a variant of Adapt that utilizes all terms      its parent to identify any newly introduced or modified theorems.
in the stuck proof state for searching instead of LLM-generated                For each theorem, we masked its proof body as well as the other
keywords. The result shows that using LLM-generated keywords               theorems and lemmas introduced in the commit. In this way, we
indeed leads to more theorems to be proved (651 vs. 625).                  make sure that LLMs cannot access any helper lemmas or theorems
                                                                           introduced during the construction of the proof. As a result, LLMs
                                                                           need to propose these lemmas or theorems as human developers
3.6      Regeneration Strategy                                             did when writing the proof. In addition, any theorems and lemmas
The regeneration strategy can either repair simple errors in the           introduced in future commits are also not available to LLMs. Only
previous proof, or explore a new proof approach when the previous          the previously committed lemmas and theorems are available to
one is deemed infeasible. When this strategy is selected, Adapt            the LLMs, mimicking how proofs are actually developed in practice.
provides an LLM with the target theorem statement, the working             On average, 60.34 same-commit lemmas and theorems are masked
context, and the state of the proof assistant from the current proof       per task. Moreover, 23.2% of the human-written proofs use at least
failure. This strategy prompts the LLM to reason about the previous        one declaration introduced in the same commit, indicating that the
failure and then generate a new proof (Figure 9).                          masked context is relevant to proof construction. To prevent a few
                                                                           large projects from dominating the benchmark and ensure diversity,
                                                                           we randomly sampled at most 200 theorems from each project to
4      Evaluation
                                                                           form the final benchmark. In the end, we collected 1,720 theorems.
We investigate five research questions in our evaluation:                  The average number of tactics in the human-written proofs is 16.1,
                                                                           and the median is 7.0.
      • RQ1: How effective is Adapt compared to state-of-the-art
        proof generation tools?
      • RQ2: How sensitive is Adapt to the underlying LLMs used?           4.2      Comparison Baselines
      • RQ3: How much does each proof refinement strategy con-             We compare Adapt against three state-of-the-art LLM-based Rocq
        tribute to the overall effectiveness of Adapt?                     proof generation tools. We select Cobblestone [24] and Rango [47]
      • RQ4: How does our LLM-guided decision-maker compare                as they achieved state-of-the-art performance on the most recent
        to other alternative designs?                                      CoqStoq benchmark. We also include PALM [34] which employs
Adaptive Proof Refinement with LLM-Guided Strategy Selection                                            ASE ’26, October 12–16, 2026, Munich, Germany


hard-coded rules to select a refinement strategy. Since PALM does                  Table 1: Theorems proven by each approach.
not query the LLM during refinement, we build two additional
baselines, Self-Refine and Self-Refine+RAG, that refine proofs               Approach
                                                                                                    # of Theorems Proven
                                                                                                                                   Avg. Cost ($)
with iterative LLM queries. Each baseline is described below.                                       CoqDev         CoqStoq
      • Cobblestone [24] adopts a divide-and-conquer strategy. It            Cobblestone          527 (30.64%)    435 (37.15%)          0.154
        prompts an LLM to generate whole proofs, preserves the suc-          Rango                481 (27.97%)    352 (30.06%)            -
        cessful sub-proofs, and queries the LLM to resolve remaining         PALM                 522 (30.35%)    415 (35.44%)          0.012
        unproven subgoals.                                                   Self-Refine          503 (29.24%)    357 (30.49%)          0.051
      • Rango [47] fine-tunes the DeepSeek-Coder 1.3B [21] for               Self-Refine+RAG      549 (31.92%)    410 (35.01%)          0.058
        step-by-step proof generation. At each proof step, it retrieves      Adapt                651 (37.85%)    484 (41.33%)          0.085
        helper lemmas and existing proofs based on their similarity
        to the current proof state.                                        context enrichment strategy; and (3) Adapt_base, which retains
      • PALM [34] employs hard-coded rules to select repair heuris-        only the regeneration strategy. When a strategy is disabled, we
        tics that fix common errors based on error types. If the heuris-   modify the prompt for the decision-making LLM accordingly to
        tics fail, it falls back to a backtracking strategy to incremen-   prevent its selection. Furthermore, to validate our keywords-based
        tally regenerate previous proof steps with CoqHammer [16].         searching within the context enrichment strategy, we implemented
      • Self-Refine [35] adopts a simple iterative repair loop. Af-        a variant called Adapt_full_state that utilizes all terms in the stuck
        ter the initial proof failure, it repeatedly prompts the LLM to    proof state for searching instead of LLM-generated keywords.
        generate a new proof based on the state of the proof assistant        In RQ4, we investigate alternative designs of the decision-maker
        from the previous failure, without a working context, further      used by Adapt, experimenting with deep learning-based, rule-
        lemma discovery or context enrichment.                             based, random, and sequential approaches. Section 4.7 describes
      • Self-Refine+RAG enhances Self-Refine by initializing               each decision-maker in more detail.
        the working context before entering the iterative repair loop.        In all experiments except the one in RQ5, we set the refinement it-
        In each iteration, it instructs the LLM to explicitly analyze      eration limit to 3 for Adapt and the baselines. RQ5 investigates how
        the state of the proof assistant and working context, then         the limit on refinement iterations impacts Adapt’s performance.
        regenerate a proof. However, it does not perform further
        adaptive lemma discovery or context enrichment.                    4.4    RQ1: Overall Effectiveness of Adapt
                                                                           Table 1 presents the number and percentage of theorems proven by
4.3     Experimental Setup                                                 each approach on both the existing CoqStoq and CoqDev. Overall,
All experiments are conducted on a server with an AMD EPYC 7313            Adapt significantly outperforms all baselines on both benchmarks.
CPU, an NVIDIA A5500 GPU, and 128 GB memory, running 64-bit                On CoqStoq, Adapt proves 11.26%, 16.63%, and 37.50% more theo-
Ubuntu 22.04 LTS.                                                          rems than Cobblestone, PALM and Rango, respectively. On Co-
   To enable a fair comparison with Cobblestone and PALM, we               qDev, which simulates a more realistic development scenario with
allow Adapt, Self-Refine, and Self-Refine+RAG to use CoqHam-               limited context, Adapt’s advantage is maintained. It outperforms
mer. We first invoke CoqHammer on the initial proof state, and             the baselines by 23.53%, 24.71%, and 35.34%, respectively. Moreover,
once more when a tactic fails. In the latter case, if CoqHammer fails      it surpasses the strongest baseline, Self-Refine+RAG, by 18.58%.
to solve the goal, the proof attempt is considered unsuccessful. We        These results demonstrate the effectiveness of Adapt in integrating
have not modified Rango to use CoqHammer, as doing so would                and dynamically selecting different refinement strategies in proof
require significant changes to its source code.                            generation compared to state-of-the-art methods.
   In all experiments, we set the temperature to 0 to mitigate ran-            We can also compare the sets of theorems uniquely proved by
domness. In all experiments except the one in RQ2, we use GPT-             either Adapt or one of our baselines. On CoqDev, Adapt proves
4o-2024-08-06 [2] as the underlying LLM for Adapt and the non-             91 (5.29%) theorems that no baseline proves, while 133 (7.73%) the-
Rango comparison baselines. Rango uses a finetuned LLM for                 orems are proved by at least one baseline but not by Adapt. On
step-by-step proof generation, and our experiments use the fine-           CoqStoq, the corresponding counts are 54 (4.61%) and 61 (5.21%),
tuned DeepSeek-Coder model from its original implementation. We            respectively. These results show that Adapt is complementary to
choose not to finetune GPT-4o for Rango due to its high cost. In           the baselines.
RQ2, we further experiment with five additional popular LLMs with              To better understand the refinement strategies selected by Adapt,
varying parameter sizes as the backbone of Adapt. These mod-               we analyzed the percentage of tasks where Adapt selected each
els include GPT-5.2 [4], GPT-4o-mini [3], Claude-3.7-Sonnet [1],           strategy in each refinement iteration, as shown in Figure 10. The re-
DeepSeek-V3 [32], and Llama-4-Maverick-17B-128E [5]. Due to the            sult shows that the LLM decision-maker in Adapt selects different
high computational and token costs, we conduct the RQ2 experi-             strategies throughout the refinement loop, instead of adhering to a
ment on 500 randomly sampled theorems from CoqDev.                         single fixed approach. This indicates that each strategy contributes
   In RQ3, we conduct an ablation study to measure the contribution        to solving different proof challenges.
of Adapt’s proof refinement strategies. Specifically, we created           Cost Analysis. On average, Adapt costs $0.085 USD per theorem,
three variants of Adapt: (1) Adapt_no_lemma, which disables the            due to the multiple LLM calls required during iterative refinement.
lemma discovery strategy; (2) Adapt_no_enrich, which disables the          Self-Refine and Self-Refine+RAG cost $0.051 USD and $0.058
ASE ’26, October 12–16, 2026, Munich, Germany                           Minghai Lu, Zhe Zhou, Danning Xie, Songlin Jia, Benjamin Delaware, and Tianyi Zhang


                                                                           Table 2: Theorems proven by Adapt using different LLMs on
                                                                           500 theorems sampled from CoqDev.

                                                                                  Approach                             # of Theorems Proven
                                                                                  GPT-5.2                                     196 (39.20%)
                                                                                  GPT-4o                                      188 (37.60%)
                                                                                  GPT-4o-mini                                 152 (30.40%)
Figure 10: Percentage of strategies selected in each iteration.                   Claude-3.7-Sonnet                           185 (37.00%)
                                                                                  DeepSeek-V3                                 179 (35.80%)
USD per theorem, respectively, as they also repeatedly regenerate                 Llama-4-Maverick-17B-128E                   177 (35.40%)
proofs after failures. Cobblestone has the highest cost at $0.154
USD per theorem. This is expected based on its divide-and-conquer           Table 3: Effectiveness of refinement strategies on CoqDev.
strategy which prompts the LLM to discharge unproven subgoals.
PALM only costs $0.012 USD per theorem, since it only prompts                           Variant                  # of Theorems Proven
an LLM to generate the initial proof, and relies solely on symbolic                     Adapt_no_lemma                  590 (34.30%)
methods to repair any proof failures. Rango incurs the minimal cost,                    Adapt_no_enrich                 622 (36.16%)
since it runs a fine-tuned local model rather than querying a closed-                   Adapt_base                      519 (30.17%)
source API. Overall, these results highlight a trade-off between                        Adapt_full_state                625 (36.34%)
cost and performance. Adapt achieves the best performance at a                          Adapt                           651 (37.85%)
moderate cost.
                                                                           Learning-Based Decision Making. Another mechanism we ex-
4.5     RQ2: Sensitivity of Adapt to LLM Choices                           plored is a learning-based approach, which employs a machine
Table 2 presents the number of theorems proven by Adapt us-                learning (ML) model to predict the strategy a developer would use
ing each underlying LLM. We observe that Adapt performs the                in a given state of the proof assistant. Training such a model re-
best with GPT-5.2, successfully proving 196 theorems. The default          quires a labeled dataset of the state of the proof assistant and the
model used in RQ1, GPT-4o, also performs strongly, proving 188             corresponding strategies taken by human developers, which is not
theorems. Its performance remains comparable when using other              available. To address this, we collect a training dataset of 18,628
large models such as Claude-3.7-Sonnet, DeepSeek-V3, and Llama-            examples from the human-written proofs in CoqDev, and evaluate
4-Maverick-17B-128E, proving 185, 179, and 177 theorems, respec-           the model using ten-fold cross-validation.
tively. As expected, Adapt proves 19.15% fewer theorems when                  To generate each data point in the training dataset, we first
using GPT-4o-mini, which is significantly smaller (estimated to            simulate the working context at each step of a human-written
have 8 B parameters) compared to GPT-4o (estimated to have 200 B           proof by using the same retrieval method described in Section 3.2.
parameters). This is a reasonable reduction given the limited ca-          We then extract the following features to characterize the state of
pability of smaller models. However, Adapt’s performance with              the proof assistant:
GPT-4o-mini is still comparable to state-of-the-art baselines like
PALM, which uses the more powerful GPT-4o model in RQ1.                        (1) The number of unique definitions appearing in the proof
                                                                                   goal.
4.6     RQ3: Contribution of Refinement Strategies                             (2) The number of unique definitions appearing in the local
                                                                                   hypotheses.
Table 3 presents the performance of these variants compared to                 (3) The count of definitions that appear in the goal but not in
the complete Adapt framework on the CoqDev benchmark. We                           the hypotheses.
observe that the full Adapt proves 10.34% and 4.66% more theorems              (4) The count of definitions that appear in the goal but not in
than Adapt_no_lemma and Adapt_no_enrich, respectively. These                       existing lemmas in the working context.
results indicate that both lemma discovery and context enrichment              (5) The similarity score of the retrieved similar theorem.
contribute to the overall effectiveness of Adapt, and lemma dis-               (6) The number of lemmas used in the similar proof that are not
covery is particularly critical. Furthermore, Adapt_base performs                  present in the working context.
comparably to Self-Refine, which is expected because Adapt_base
functions as a standard iterative refinement loop. Finally, replacing      We select features 1 and 2 to reflect proof state complexity. Features
generated keywords with the full proof state for searching reduces         3–5 measure how many definitions in the goal lack supporting
the success rate by 4.00% and increases token consumption by 7.44%,        lemmas in the working context. Feature 6 assesses if potentially
confirming the efficiency of our keyword-based approach.                   useful information in a similar theorem has not been incorporated.
                                                                               Given the extracted features, the ML model predicts which re-
4.7     RQ4: Comparing Decision-Maker Designs                              finement strategy to take at the given proof state, which is a typical
While Adapt leverages the reasoning capabilities of LLMs for               classification problem. The ground-truth labels are derived from
adaptive strategy selection based on reflection over the current           the corresponding human-written tactic at the proof state: if the
proof progress and available context, we also investigate alterna-         tactic applies a new helper lemma introduced in the same commit,
tive decision-making mechanisms to understand the trade-offs.              it is labeled as Lemma Discovery; if it applies a lemma that existed
Adaptive Proof Refinement with LLM-Guided Strategy Selection                                           ASE ’26, October 12–16, 2026, Munich, Germany


  Table 4: Average accuracy and F1 scores for each model.

                     Model              Acc.(%)     F1
                     SVM                   41       0.48
                     Decision Tree         25       0.29
                     Random Forest         41       0.47
                     XGBoost               71       0.74
                     DNN                   82       0.78

Table 5: Performance and cost comparison of Adapt with
different decision-makers on CoqDev.

                      # of Theorems                    # of Tokens
      Approach                            # Iters
                          Proven                     (Input / Output)
      Adaptml           595 (34.59%)        1.24          9801 / 3157
      Adaptrule         647 (37.62%)        1.37         24244 / 6109
      Adaptrandom       605 (35.17%)        1.61         12568 / 3476     Figure 11: Percentage of theorems proven by refinement
      Adaptseq          613 (35.64%)        1.58         11376 / 3296     iterations.
      Adapt             651 (37.85%)        1.35         16348 / 4383
                                                                          Results. Table 5 compares the success rates and average costs of
prior to the current commit, it is labeled as Context Enrichment;         different decision-makers in terms of refinement iterations and
otherwise, it is labeled as Regeneration.                                 token consumption. Overall, the results indicate that the LLM-
   We conduct a preliminary experiment using ten-fold cross val-          guided decision-maker achieves the best balance of performance
idation to compare several ML models and select the best one to           and efficiency. Although the rule-based decision-maker achieves a
be compared with other types of decision-makers. We evaluate              comparable success rate, it is significantly less efficient, consuming
traditional models, including Support Vector Machine (SVM) [22],          nearly 50% more tokens on average. This inefficiency stems from
Decision Tree [42], Random Forest [11], and XGBoost [14]. In ad-          its simple heuristics, which often unnecessarily select the resource-
dition, we build a Deep Neural Network (DNN) [31] with three              intensive lemma discovery strategy.
fully-connected layers, using ReLU [38] as the activation function            The importance of intelligent strategy selection is further high-
and a dropout rate of 0.2. We train this DNN for 50 epochs using          lighted by the random baseline, which proves 7.07% fewer theorems
the Adam optimizer [25], with a learning rate of 0.001. The aver-         than the LLM decision-maker and requires, on average, 19.26% more
age accuracy and F1 score of each model is shown in Table 4. We           iterations to find a proof. The learning-based decision-maker using
ultimately select DNN as it achieves the highest average accuracy         DNN performs even worse than the random baseline. We attribute
and F1 score.                                                             its underperformance to two key challenges: first, our quantitative
                                                                          features may not fully capture the complex semantics of a proof
Rule-Based Decision Making. One alternative is a rule-based               state, and second, the scarcity of training data, especially for lemma
method, which employs heuristics to select a strategy. First, it          discovery, makes the model overly conservative.
checks whether the retrieved similar proof uses lemmas that are
missing from the current working context. If so, it prioritizes con-
text enrichment. Next, it analyzes the definitions (e.g., types and       4.8    RQ5: Impact of Refinement Iteration Limit
functions) in the current proof state. If the proof state involves def-   Figure 11 shows the cumulative percentage of theorems successfully
initions that are not present in any lemmas in the working context,       proven on CoqDev as the iteration count increases. We observe that
it selects lemma discovery. The intuition is that formal proofs rely      while all three approaches benefit from more iterations, the success
on lemmas to specify the properties of definitions. A definition in       rates for Self-Refine and Self-Refine+RAG begin to saturate after
the goal without corresponding lemmas indicates an absence of             3 attempts. In contrast, Adapt continues to improve its performance
established properties and therefore requires lemma discovery. If         more steadily across all 5 iterations. This suggests that Adapt’s
neither of these two conditions is met, it defaults to Regeneration.      ability to introduce powerful new lemmas via lemma discovery and
Random Decision Making. We also implement a baseline decision-            context enrichment provides it with more opportunities to make
maker that randomly selects one of the refinement strategies in           progress on challenging theorems where simpler iterative repair
each iteration. This is expected to be the weakest baseline, as it        methods have stalled.
does not incorporate any reasoning or contextual information when
choosing a strategy.                                                      4.9    Failure Analysis
Sequential Decision Making. We further evaluate Adaptseq , a              To understand the limitations of our approach, we manually ana-
deterministic baseline that cycles through strategies in a fixed, cost-   lyzed 100 randomly sampled theorems from the CoqDev bench-
ascending order: (1) Regeneration, (2) Context Enrichment, and (3)        mark that Adapt failed to prove. Our analysis identified three
Lemma Discovery.                                                          primary failure modes:
                                                                          1. Incorrect Strategic Decisions (39%). A primary cause of fail-
                                                                          ure is the decision-maker’s inability to identify the correct strategy.
ASE ’26, October 12–16, 2026, Munich, Germany                           Minghai Lu, Zhe Zhou, Danning Xie, Songlin Jia, Benjamin Delaware, and Tianyi Zhang


(* Required existing lemma *)
                                                                           3. Proof Generation Failures (29%). Despite correct strategic de-
Lemma Ordered_iff_Ordered ' t :
   Ordered t <-> Ordered ' t .                                             cisions and execution, the LLM may still fail to generate the correct
                                                                           proof script. In 9% of cases, the LLM failed to utilize the theorems
(* Theorem statement and human-written proof *)                            or synthesized lemmas, although they were provided in the prompt.
Lemma rotate_right_Ordered_imp v l r :                                     The remaining 20% of failures were caused by incorrect tactic ap-
   Ordered ( rotate_right v l r ) -> Ordered ( Node v l r ) .
Proof .
                                                                           plications or syntax errors. For instance, Figure 12c illustrates an
   destruct l as [| lv ll lr ]; eauto 2.                                   example where the correct lemma (const_unfold) is provided in
   rewrite ! Ordered_iff_Ordered '.                                        the prompt, but the LLM mistakenly tried to apply it to the goal
   ...                                                                     using the rewrite tactic instead of the apply tactic.
(a) Incorrect strategy selection: Adapt selects regeneration in all
iterations and never retrieves the required existing lemma [7].
(* Required lemma statement correctly proposed by Adapt *)
Lemma valt_dec : forall T1 n n1 v1 ,
   val_type n v1 T1 -> n1 <= n -> val_type n1 v1 T1 .
                                                                           5 Discussion
                                                                           5.1 Threats to Validity
(* Theorem statement and human-written proof *)
Lemma envt_dec : forall n n1 H G ,                                         Internal Validity. The main threat to internal validity arises from
   env_type n H G -> n1 <= n -> env_type n1 H G .                          the inherent randomness of LLMs. To mitigate this threat, we set
Proof .                                                                    the temperature of all evaluated LLMs to 0 for more determinis-
   ...
   eapply valt_dec ; eauto .
                                                                           tic outputs. Furthermore, we conducted evaluations across two
Qed .                                                                      benchmarks and with six LLMs of different parameter sizes. The
                                                                           consistent results observed across these varied settings help to
(b) Ineffective strategy execution: Adapt correctly proposes the re-
                                                                           reduce this threat.
quired helper lemma but fails to prove it [6].
                                                                           External Validity. The threat to external validity concerns the
(* Required existing lemma correctly retrieved by Adapt *)
                                                                           generalizability of our experimental results. To mitigate this threat,
Lemma const_unfold : forall T ( x : T ) ,
   const x = Cons x ( const x ) .                                          we conducted experiments on two benchmarks that include various
                                                                           real-world projects covering multiple domains. However, while the
(* Theorem statement *)                                                    principles of Adapt’s approach are applicable to other interactive
Lemma L_as_K : forall n , L n = K n << 0.                                  proof assistants such as Isabelle and Lean, our current implemen-
Proof .
  (* Human-written proof *)
                                                                           tation and evaluation are confined solely to the Rocq ecosystem.
   destruct n as [| n ].                                                   Extending Adapt to and evaluating it within these other ITPs re-
   - apply const_unfold .                                                  mains for future work.
   ...
                                                                           Construct Validity. A potential threat to construct validity is that
  (* LLM-generated proof *)                                                we measure the effectiveness of a decision-maker with the overall
  destruct n.                                                              success rate, which is an indirect metric. This is because a good
  - rewrite const_unfold .                                                 strategic choice does not guarantee a successful proof. For example,
  ...
                                                                           the decision-maker could select a suitable strategy, such as lemma
(c) Proof generation failure: the required lemma is available, but         discovery, but the execution of this strategy may fail, leading to an
Adapt applies it using an invalid tactic [8].                              overall proof failure that does not reflect a poor decision.
 Figure 12: Representative failure examples from CoqDev.

Specifically, in 25% of cases, the LLM failed to select context en-
richment in any refinement iteration, despite the need for existing
lemmas. For instance, Figure 12a shows an example where the
                                                                           5.2      Limitations and Future Work
LLM repeatedly selected regeneration, failing to find the neces-           The framework of Adapt can be expanded by integrating more
sary lemma. Similarly, in 14% of cases, it never attempted lemma           refinement strategies, such as proof repair models fine-tuned on
discovery, though new helper lemmas were required.                         ITP feedback, similar to the approach of Baldur [19]. Our decision-
                                                                           maker primarily leverages LLM reasoning, with initial explorations
2. Ineffective Strategy Execution (32%). Even when the correct
                                                                           into rule-based and machine learning approaches. Future research
strategy is selected, the execution modules may still fail. In 17% of
                                                                           could investigate more sophisticated methods. For instance, this
cases, Context Enrichment failed to select required lemmas because
                                                                           could involve creating more nuanced heuristics for rule-based meth-
the LLM generated ineffective search keywords. In 15% of cases, the
                                                                           ods or incorporating richer features for the machine learning mod-
lemma discovery strategy only proposed trivial lemmas or failed to
                                                                           els. Currently, Adapt relies solely on LLMs to propose lemma
prove the proposed lemmas. For instance, Figure 12b illustrates an
                                                                           statements, but the quality of these LLM-generated statements can
example where the lemma discovery strategy correctly proposed
                                                                           vary; some are trivial, syntactically flawed, or unprovable. Future
the statement of the required lemma, but failed to prove it.
                                                                           work could enhance the lemma discovery strategy by developing
                                                                           advanced prompting techniques or integrating symbolic methods.
Adaptive Proof Refinement with LLM-Guided Strategy Selection                                            ASE ’26, October 12–16, 2026, Munich, Germany


6    Related Work                                                          and specifications to synthesize and prove helper lemmas that are
                                                                           relevant to program semantics. It then adapts these lemmas to
Proof Refinement. Recent work in proof refinement has focused
                                                                           the verification condition using feedback from the proof assistant.
on combining a vanilla LLM proof generation model with a stan-
                                                                           Quarry [54] decomposes a proof by prompting an LLM to propose
dalone repair procedure when errors occur. These approaches typi-
                                                                           helper lemmas. It then ranks the proposed lemmas based on a
cally generate an initial proof attempt with an LLM and then employ
                                                                           difficulty model, and recursively proves each lemma. While these
various repair strategies that leverage proof error information. For
                                                                           tools use lemma discovery as their main refinement mechanism,
instance, Baldur [19] fine-tunes a second LLM specifically for proof
                                                                           Adapt selects from multiple refinement strategies dynamically.
repair, regenerating a new proof from both the incorrect proof and
the Rocq error message. SAFE [15] fine-tunes an LLM for both               Agentic Theorem Proving. COPRA [45] leverages the in-context
proof generation and refinement. PALM [34] employs hard-coded              learning capabilities of LLMs to perform a backtracking search. At
rules to select bug-fixing heuristics based on error types. If the         each step, it prompts the LLM with the current proof state, pre-
heuristics fail, it falls back to a backtracking strategy that incremen-   vious failures, and retrieved lemmas to generate the next tactic.
tally reverts proof steps and leverages automated theorem provers          Failed or non-progressing tactics are recorded and avoided in subse-
such as CoqHammer [16] to regenerate those steps. AutoVerus [51]           quent attempts. It backtracks to the preceding state after repeated
automates the verification of Rust programs using Verus [30] by            unsuccessful attempts at a proof state. RocqStar [27] employs a
refining LLM-generated proofs based on the specific error type. Cob-       multi-agent framework. It first uses multi-agent debate to generate
blestone [24] employs a divide-and-conquer strategy. It samples            and rank candidate proof plans, and then assigns an executor agent
whole proofs from the LLM and uses additional LLM calls to resolve         to execute the selected plan. If execution repeatedly fails, a critic
failed subgoals while preserving successful proof steps. A common          model analyzes the current proof state and context, after which a
limitation of these methods lies in their rule-based decision-making       replanner model revises the plan for another execution attempt.
mechanisms. In contrast, Adapt adopts an LLM-guided decision-              AutoRocq [48] represents the current proof as a tree and prompts
maker to dynamically select suitable proof refinement strategies           the LLM to generate one tactic each iteration. Upon failures, it first
based on the proof failure and related context.                            prompts the LLM to regenerate the tactic, and prompts the LLM to
                                                                           generate a query to search for additional lemmas when an error
Retrieval-Augmented Proof Generation. Another line of work
                                                                           persists after several regenerations. APOLLO [39] is an agentic
enhances automated proof generation by integrating retrieval mech-
                                                                           framework for repairing Lean proofs. It uses compiler feedback
anisms for relevant context. A common approach is to retrieve
                                                                           to fix syntax errors, localize failing sub-lemmas, apply automated
premises like definitions and lemmas. For instance, ReProver [53]
                                                                           solvers, and invoke an LLM on the remaining goals. All these sys-
fine-tunes a retrieval model to find relevant premises given a proof
                                                                           tems employ a fixed workflow, while Adapt employs a decision-
state. Magnushammer [36] improves the retrieval process by train-
                                                                           maker to dynamically select refinement strategies based on the
ing a reranking model to prioritize the most relevant premises.
                                                                           state of the proof assistant and current working context.
Furthermore, Rango [47] retrieves both relevant proofs and lemmas
via textual similarity to the current proof state, providing richer
guidance for the proof search. While these methods focus on en-            7   Conclusion
hancing proof generation with retrieval methods, Adapt integrates          In this paper, we propose Adapt, an adaptive proof refinement
multiple strategies and selects from them adaptively. Furthermore,         framework. Adapt integrates multiple refinement strategies, in-
Adapt leverages pretrained LLMs, whereas these approaches often            cluding lemma discovery, context enrichment and regeneration.
require significant training or fine-tuning.                               Upon proof failures, Adapt employs an LLM-based decision-maker
Lemma Discovery. Lemma discovery facilitates automated proof               to select an appropriate strategy based on the state of the proof
generation by proposing helper lemmas aimed at simplifying com-            assistant and available context. We also introduce CoqDev, a new
plex proofs. These techniques range from neuro-symbolic approaches         benchmark that better simulates more challenging real-world devel-
to data-driven methods. For instance, Lemmanaid [9] employs a              opment processes. Our experiments show that Adapt significantly
neuro-symbolic pipeline where a fine-tuned model generates lemma           outperforms state-of-the-art baselines on both CoqDev and the ex-
templates with symbolic holes that a symbolic engine then instanti-        isting CoqStoq benchmark. Further analysis demonstrates Adapt’s
ates with concrete variables. Lfind [44] offers a data-driven alterna-     generalizability on six different LLMs, and measures the contribu-
tive, framing lemma discovery as a synthesis task that generalizes         tion of its refinement strategies. We also compare the trade-offs of
the proof goal into a sketch and then finds instantiations. These          alternative decision-maker designs.
dedicated lemma discovery techniques are complementary to our
work. Integrating them into Adapt’s adaptive framework to im-              8   Data Availability Statement
prove the quality of proposed lemmas remains a promising avenue            A replication artifact is publicly available: https://doi.org/10.5281/
for future research.                                                       zenodo.21708212
   LegoProver [49] uses an LLM to propose and prove new lemmas.
The verified lemmas are stored in a library and retrieved through
embedding-based search. It also refines existing lemmas to improve         Acknowledgments
their reusability. LemmaNet [55] focuses on lemma discovery for            We thank the anonymous reviewers for their valuable suggestions
proving verification conditions. It first analyzes the source code         and feedback. This work is supported in part by NSF grants CCF-
                                                                           2340408, CCF-2321680, and ITE-2333736.
ASE ’26, October 12–16, 2026, Munich, Germany                                               Minghai Lu, Zhe Zhou, Danning Xie, Songlin Jia, Benjamin Delaware, and Tianyi Zhang


References                                                                                          on Software Engineering (Rio de Janeiro, Brazil) (ICSE ’26). 13 pages.
 [1] 2025. Claude 3.7 Sonnet. https://www.anthropic.com/news/claude-3-7-sonnet.                [25] Diederik P. Kingma and Jimmy Ba. 2017. Adam: A Method for Stochastic Opti-
 [2] 2025. GPT-4o. https://openai.com/index/hello-gpt-4o.                                           mization. arXiv:1412.6980 [cs.LG] https://arxiv.org/abs/1412.6980
 [3] 2025. GPT-4o-mini. https://openai.com/index/gpt-4o-mini-advancing-cost-                   [26] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David Cock,
     efficient-intelligence.                                                                        Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt, Rafal Kolanski, Michael
 [4] 2025. GPT-5.2. https://openai.com/index/introducing-gpt-5-2/.                                  Norrish, et al. 2009. seL4: Formal verification of an OS kernel. In Proceedings of
 [5] 2025.      Llama 4 Maverick.       https://ai.meta.com/blog/llama-4-multimodal-                the ACM SIGOPS 22nd symposium on Operating systems principles. 207–220.
     intelligence.                                                                             [27] Andrei Kozyrev, Nikita Khramov, Gleb Solovev, and Anton Podkopaev. 2026.
 [6] 2026.                                 Failure due to ineffective strategy execution.           RocqStar: Leveraging Similarity-driven Retrieval and Agentic Systems for Rocq
     https://github.com/TiarkRompf/types-and-proofs/blob/                                           generation. In Proceedings of the 25th International Conference on Autonomous
     8818bd6e622cb13902f6221cf18e0b21bc255ae6/pub/stlc_rec_indexed_eff.v#L298.                      Agents and Multiagent Systems (Paphos, Cyprus) (AAMAS ’26). International Foun-
 [7] 2026. Failure due to wrong strategy selection. https://github.com/Dessertion/                  dation for Autonomous Agents and Multiagent Systems, Richland, SC, 1256–1264.
     coq-bst/blob/87bcd47f57705bbd967a9825f587cf0043188f23/AVL.v#L958.                              doi:10.65109/ZQXK7747
 [8] 2026. Proof generation failure. https://github.com/meithecatte/busycoq/blob/              [28] Cole Kurashige, Ruyi Ji, Aditya Giridharan, Mark Barbone, Daniel Noor, Shachar
     979611edb7364ed99de1d160f69611620c6f7d8c/verify/ShiftOverflowBins.v#L42.                       Itzhaky, Ranjit Jhala, and Nadia Polikarpova. 2024. CCLemma: e-graph guided
 [9] Yousef Alhessi, Sólrún Halla Einarsdóttir, George Granberry, Emily First, Moa                  lemma discovery for inductive equational proofs. Proceedings of the ACM on
     Johansson, Sorin Lerner, and Nicholas Smallbone. 2025. Lemmanaid: Neuro-                       Programming Languages 8, ICFP (2024), 818–844.
     Symbolic Lemma Conjecturing. arXiv preprint arXiv:2504.04942 (2025).                      [29] Daniel Kästner, Ulrich Wünsche, Jörg Barrho, Marc Schlickling, Bernhard Schom-
[10] Chenyang An, Zhibo Chen, Qihao Ye, Emily First, Letian Peng, Jiayun Zhang, Zi-                 mer, Michael Schmidt, Christian Ferdinand, Xavier Leroy, and Sandrine Blazy.
     han Wang, Sorin Lerner, and Jingbo Shang. 2024. Learn from Failure: Fine-tuning                2018. CompCert: Practical experience on integrating and qualifying a formally
     LLMs with Trial-and-Error Data for Intuitionistic Propositional Logic Proving. In              verified optimizing compiler. In ERTS 2018: Embedded Real Time Software and
     Proceedings of the 62nd Annual Meeting of the Association for Computational Lin-               Systems. SEE. http://xavierleroy.org/publi/erts2018_compcert.pdf
     guistics (Volume 1: Long Papers), Lun-Wei Ku, Andre Martins, and Vivek Srikumar           [30] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe,
     (Eds.). Association for Computational Linguistics, Bangkok, Thailand, 776–790.                 Yi Zhou, Jon Howell, Bryan Parno, and Chris Hawblitzel. 2023. Verus: Verifying
     doi:10.18653/v1/2024.acl-long.45                                                               Rust Programs using Linear Ghost Types. Proc. ACM Program. Lang. 7, OOPSLA1,
[11] Leo Breiman. 2001. Random Forests. Mach. Learn. 45, 1 (Oct. 2001), 5–32. doi:10.               Article 85 (April 2023), 30 pages. doi:10.1145/3586037
     1023/A:1010933404324                                                                      [31] Yann LeCun, Yoshua Bengio, and Geoffrey Hinton. 2015. Deep learning. nature
[12] Alan Bundy. 2002. A Critique of Proof Planning. In Computational Logic: Logic                  521, 7553 (2015), 436–444.
     Programming and Beyond, Essays in Honour of Robert A. Kowalski, Part II. Springer-        [32] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Cheng-
     Verlag, Berlin, Heidelberg, 160–177.                                                           gang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. 2024. Deepseek-v3
[13] Jialun Cao, Yaojie Lu, Meiziniu Li, Haoyang Ma, Haokun Li, Mengda He, Cheng                    technical report. arXiv preprint arXiv:2412.19437 (2024).
     Wen, Le Sun, Hongyu Zhang, Shengchao Qin, et al. 2025. From informal to formal–           [33] Haoxiong Liu, Jiacheng Sun, Zhenguo Li, and Andrew C Yao. 2025. ProofAug:
     incorporating and evaluating llms on natural language requirements to verifiable               efficient neural theorem proving via fine-grained proof structure analysis. In
     formal proofs. In Proceedings of the 63rd Annual Meeting of the Association for                Proceedings of the 42nd International Conference on Machine Learning (Vancouver,
     Computational Linguistics (Volume 1: Long Papers). 26984–27003.                                Canada) (ICML’25). JMLR.org, Article 1583, 19 pages.
[14] Tianqi Chen and Carlos Guestrin. 2016. Xgboost: A scalable tree boosting system.          [34] Minghai Lu, Benjamin Delaware, and Tianyi Zhang. 2024. Proof Automation
     In Proceedings of the 22nd acm sigkdd international conference on knowledge                    with Large Language Models. In Proceedings of the 39th IEEE/ACM International
     discovery and data mining. 785–794.                                                            Conference on Automated Software Engineering (Sacramento, CA, USA) (ASE
[15] Tianyu Chen, Shuai Lu, Shan Lu, Yeyun Gong, Chenyuan Yang, Xuheng Li,                          ’24). Association for Computing Machinery, New York, NY, USA, 1509–1520.
     Md Rakib Hossain Misu, Hao Yu, Nan Duan, Peng Cheng, et al. 2025. Automated                    doi:10.1145/3691620.3695521
     proof generation for rust code via self-evolution. In International Conference on         [35] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah
     Learning Representations, Vol. 2025. 71891–71918.                                              Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank
[16] Łukasz Czajka and Cezary Kaliszyk. 2018. Hammer for Coq: Automation for                        Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir
     Dependent Type Theory. J. Autom. Reason. 61, 1–4 (jun 2018), 423–453. doi:10.                  Yazdanbakhsh, and Peter Clark. 2023. SELF-REFINE: iterative refinement with self-
     1007/s10817-018-9458-4                                                                         feedback. In Proceedings of the 37th International Conference on Neural Information
[17] Emily First and Yuriy Brun. 2022. Diversity-driven automated formal verification.              Processing Systems (New Orleans, LA, USA) (NIPS ’23). Curran Associates Inc.,
     In Proceedings of the 44th International Conference on Software Engineering (Pitts-            Red Hook, NY, USA, Article 2019, 61 pages.
     burgh, Pennsylvania) (ICSE ’22). Association for Computing Machinery, New                 [36] Maciej Mikuła, Szymon Tworkowski, Szymon Antoniak, Bartosz Piotrowski,
     York, NY, USA, 749–761. doi:10.1145/3510003.3510138                                            Qiaochu Jiang, Jin Zhou, Christian Szegedy, Łukasz Kuciński, Piotr Miłoś, and
[18] Emily First, Yuriy Brun, and Arjun Guha. 2020. TacTok: semantics-aware proof                   Yuhuai Wu. 2024. Magnushammer: A transformer-based approach to premise se-
     synthesis. Proc. ACM Program. Lang. 4, OOPSLA, Article 231 (Nov. 2020), 31 pages.              lection. In International Conference on Learning Representations, Vol. 2024. 39326–
     doi:10.1145/3428299                                                                            39350.
[19] Emily First, Markus N. Rabe, Talia Ringer, and Yuriy Brun. 2023. Baldur: Whole-           [37] Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 Theorem Prover and
     Proof Generation and Repair with Large Language Models. In Proceedings of                      Programming Language. In Automated Deduction – CADE 28: 28th International
     the 31st ACM Joint European Software Engineering Conference and Symposium                      Conference on Automated Deduction, Virtual Event, July 12–15, 2021, Proceedings.
     on the Foundations of Software Engineering (San Francisco, CA, USA) (ESEC/FSE                  Springer-Verlag, Berlin, Heidelberg, 625–635. doi:10.1007/978-3-030-79876-5_37
     2023). Association for Computing Machinery, New York, NY, USA, 1229–1241.                 [38] Vinod Nair and Geoffrey E. Hinton. 2010. Rectified linear units improve restricted
     doi:10.1145/3611643.3616243                                                                    boltzmann machines. In Proceedings of the 27th International Conference on Inter-
[20] Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan (Newman) Wu, Jieung Kim,                            national Conference on Machine Learning (Haifa, Israel) (ICML’10). Omnipress,
     Vilhelm Sjöberg, and David Costanzo. 2016. CertiKOS: An Extensible Architecture                Madison, WI, USA, 807–814.
     for Building Certified Concurrent OS Kernels. In 12th USENIX Symposium on                 [39] Azim Ospanov, Farzan Farnia, and Roozbeh Mohit. 2026. Apollo: Automated
     Operating Systems Design and Implementation (OSDI 16). USENIX Association,                     llm and lean collaboration for advanced formal reasoning. Advances in Neural
     Savannah, GA, 653–669. https://www.usenix.org/conference/osdi16/technical-                     Information Processing Systems 38 (2026), 41599–41633.
     sessions/presentation/gu                                                                  [40] Stephen Robertson, Hugo Zaragoza, et al. 2009. The probabilistic relevance
[21] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang,                          framework: BM25 and beyond. Foundations and Trends® in Information Retrieval
     Guanting Chen, Xiao Bi, Yu Wu, YK Li, et al. 2024. DeepSeek-Coder: When the                    3, 4 (2009), 333–389.
     Large Language Model Meets Programming–The Rise of Code Intelligence. arXiv               [41] Caitlin Sadowski, Kathryn T. Stolee, and Sebastian Elbaum. 2015. How developers
     preprint arXiv:2401.14196 (2024).                                                              search for code: a case study. In Proceedings of the 2015 10th Joint Meeting on
[22] Marti A. Hearst, Susan T Dumais, Edgar Osuna, John Platt, and Bernhard                         Foundations of Software Engineering (Bergamo, Italy) (ESEC/FSE 2015). Association
     Scholkopf. 1998. Support vector machines. IEEE Intelligent Systems and their                   for Computing Machinery, New York, NY, USA, 191–201. doi:10.1145/2786805.
     applications 13, 4 (1998), 18–28.                                                              2786855
[23] Moa Johansson. 2019. Lemma discovery for induction: a survey. In Intelligent              [42] S Rasoul Safavian and David Landgrebe. 1991. A survey of decision tree classifier
     Computer Mathematics: 12th International Conference, CICM 2019, Prague, Czech                  methodology. IEEE transactions on systems, man, and cybernetics 21, 3 (1991),
     Republic, July 8–12, 2019, Proceedings 12. Springer, 125–139.                                  660–674.
[24] Saketh Ram Kasibatla, Arpan Agarwal, Yuriy Brun, Sorin Lerner, Talia Ringer, and          [43] Alex Sanchez-Stern, Emily First, Timothy Zhou, Zhanna Kaufman, Yuriy Brun,
     Emily First. 2026. Cobblestone: A Divide-and-Conquer Approach for Automating                   and Talia Ringer. 2023. Passport: Improving Automated Formal Verification Using
     Formal Verification. In Proceedings of the IEEE/ACM 48th International Conference              Identifiers. ACM Trans. Program. Lang. Syst. 45, 2, Article 12 (June 2023), 30 pages.
                                                                                                    doi:10.1145/3593374
Adaptive Proof Refinement with LLM-Guided Strategy Selection                                                                 ASE ’26, October 12–16, 2026, Munich, Germany


[44] Aishwarya Sivaraman, Alex Sanchez-Stern, Bretton Chen, Sorin Lerner, and Todd             ACM SIGPLAN Conference on Programming Language Design and Implementation
     Millstein. 2022. Data-driven lemma synthesis for interactive proofs. Proc. ACM            (Portland, OR, USA) (PLDI ’15). Association for Computing Machinery, New York,
     Program. Lang. 6, OOPSLA2, Article 143 (Oct. 2022), 27 pages. doi:10.1145/3563306         NY, USA, 357–368. doi:10.1145/2737924.2737958
[45] Amitayush Thakur, George Tsoukalas, Yeming Wen, Jimmy Xin, and Swarat                [51] Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Jianan Yao, Weidong Cui,
     Chaudhuri. 2024. An In-Context Learning Agent for Formal Theorem-Proving.                 Yeyun Gong, Chris Hawblitzel, Shuvendu Lahiri, Jacob R. Lorch, Shuai Lu, Fan
     In First Conference on Language Modeling. https://openreview.net/forum?id=                Yang, Ziqiao Zhou, and Shan Lu. 2025. AutoVerus: Automated Proof Generation
     V7HRrxXUhN                                                                                for Rust Code. Proc. ACM Program. Lang. 9, OOPSLA2, Article 396 (Oct. 2025),
[46] The Rocq Prover Development Team. 2025. The Rocq Prover, Version 9.1.0.                   29 pages. doi:10.1145/3763174
     doi:10.5281/zenodo.15149628                                                          [52] Kaiyu Yang and Jia Deng. 2019. Learning to prove theorems via interacting
[47] Kyle Thompson, Nuno Saavedra, Pedro Carrott, Kevin Fisher, Alex Sanchez-Stern,            with proof assistants. In International Conference on Machine Learning. PMLR,
     Yuriy Brun, João F. Ferreira, Sorin Lerner, and Emily First. 2025. Rango: Adaptive        6984–6994.
     Retrieval-Augmented Proving for Automated Software Verification. In Proceedings      [53] Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing
     of the IEEE/ACM 47th International Conference on Software Engineering (Ottawa,            Yu, Saad Godil, Ryan Prenger, and Anima Anandkumar. 2023. LeanDojo: theorem
     Ontario, Canada) (ICSE ’25). IEEE Press, 347–359. doi:10.1109/ICSE55347.2025.             proving with retrieval-augmented language models. In Proceedings of the 37th
     00161                                                                                     International Conference on Neural Information Processing Systems (New Orleans,
[48] Haoxin Tu, Huan Zhao, Yahui Song, Mehtab Zafar, Ruijie Meng, and Abhik                    LA, USA) (NIPS ’23). Curran Associates Inc., Red Hook, NY, USA, Article 944,
     Roychoudhury. 2026. Agentic Verification of Software Systems. Proc. ACM Softw.            40 pages.
     Eng. 3, FSE, Article FSE157 (June 2026), 24 pages. doi:10.1145/3808164               [54] Ning Zhang, Nongyu Di, Zenan Li, Yuan Yao, and Xiaoxing Ma. 2026. Planning
[49] Haiming Wang, Huajian Xin, Chuanyang Zheng, Zhengying Liu, Qingxing Cao,                  to Hammer: Difficulty-Aware Decomposition for Automating Rocq Proofs. arXiv
     Yinya Huang, Jing Xiong, Han Shi, Enze Xie, Jian Yin, et al. 2024. Lego-prover:           preprint arXiv:2606.17981 (2026).
     Neural theorem proving with growing libraries. In International Conference on        [55] Huan Zhao, Haoxin Tu, Zhengyao Liu, Martin Rinard, and Abhik Roychoud-
     Learning Representations, Vol. 2024. 31566–31597.                                         hury. 2026. Lemma Discovery in Agentic Program Verification. arXiv preprint
[50] James R. Wilcox, Doug Woos, Pavel Panchekha, Zachary Tatlock, Xi Wang,                    arXiv:2603.22114 (2026).
     Michael D. Ernst, and Thomas Anderson. 2015. Verdi: a framework for imple-
     menting and formally verifying distributed systems. In Proceedings of the 36th       Received 2026-03-26; accepted 2026-06-18
