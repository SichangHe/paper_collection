                                        A Learning Method for Symbolic Systems Using Large Language
                                                                  Models
                                                                 Jian Fang                                                      Yixun Yao                                    Yingfei XiongB
                                              Key Laboratory of High Confidence                              Key Laboratory of High Confidence                   Key Laboratory of High Confidence
                                                Software Technologies (Peking                                  Software Technologies (Peking                       Software Technologies (Peking
                                               University), Ministry of Education;                            University), Ministry of Education;                 University), Ministry of Education;
                                              School of Computer Science, Peking                             School of Computer Science, Peking                  School of Computer Science, Peking
                                                            University                                                     University                                          University
                                                         Beijing, China                                                 Beijing, China                                      Beijing, China
                                                   fangjian@stu.pku.edu.cn                                        yaoyixun@stu.pku.edu.cn                               xiongyf@pku.edu.cn
arXiv:2605.08694v1 [cs.SE] 9 May 2026




                                        Abstract                                                                                        ACM Reference Format:
                                        Automated theorem proving is essential for the formal verification                              Jian Fang, Yixun Yao, and Yingfei XiongB . 2018. A Learning Method for
                                                                                                                                        Symbolic Systems Using Large Language Models. In Proceedings of Make
                                        of safety-critical systems. As the corpus of formal proofs grows, a
                                                                                                                                        sure to enter the correct conference title from your rights confirmation email
                                        natural paradigm is to learn from existing proofs. However, cur-                                (Conference acronym ’XX). ACM, New York, NY, USA, 12 pages. https://doi.
                                        rent learning-based approaches predominantly train Large Lan-                                   org/XXXXXXX.XXXXXXX
                                        guage Models (LLMs) as end-to-end provers, which yields resource-
                                        intensive, opaque systems. Conversely, while traditional symbolic                               1    Introduction
                                        provers are computationally efficient, how to automatically improve
                                                                                                                                        Automating formal verification is important for ensuring the cor-
                                        these solvers from data remains an open challenge.
                                                                                                                                        rectness of safety-critical software [20, 23, 26] and hardware sys-
                                           This paper bridges this gap by proposing LLM2Ltac, the first
                                                                                                                                        tems [37, 38]. Interactive theorem provers (ITPs) such as Rocq
                                        approach that leverages the reasoning power of LLMs not as end-to-
                                                                                                                                        (Coq) [39], Isabelle [43], and Lean [14] provide rigorous mathemati-
                                        end provers, but as intelligent synthesizers to mine purely symbolic
                                                                                                                                        cal frameworks for constructing machine-checked proofs. However,
                                        tactics from data. Given a corpus of formal proofs, LLM2Ltac asks
                                                                                                                                        manual proof construction requires substantial expertise and ef-
                                        an LLM to identify latent proof strategies and formalize them into
                                                                                                                                        fort, significantly limiting the scalability of formal verification to
                                        reusable tactics. These tactics are verified for validity and general-
                                                                                                                                        large-scale industrial applications.
                                        izability, and finally integrated into symbolic provers to enhance
                                                                                                                                            The state-of-the-art approach to automating formal verifica-
                                        their automated proving capabilities without the runtime cost of
                                                                                                                                        tion combines large language models (LLMs) with symbolic au-
                                        LLMs.
                                                                                                                                        tomated theorem provers (ATPs) [22, 27, 40]. Though many ef-
                                           We implement LLM2Ltac on Rocq 8.20.0 and mine tactics from
                                                                                                                                        forts are devoted to improving LLM performance in these proving
                                        11,725 theorems in the standard library. We evaluate our approach
                                                                                                                                        agents [22, 24, 27, 31, 40], we argue that enhancing symbolic provers
                                        on 6,199 theorems from four large real-world verification projects,
                                                                                                                                        themselves remains equally important. First, as revealed in existing
                                        namely, CompCert, Coq-Art, Ext-Lib, and Vfa. Results show that
                                                                                                                                        studies [11], symbolic provers complement LLMs effectively. If the
                                        the mined tactics improve CoqHammer to prove 23.87% more theo-
                                                                                                                                        improvement falls outside the proving capabilities of LLMs, the
                                        rems, and when integrating the improved CoqHammer with Claude
                                                                                                                                        overall performance of the proving agent improves. Second, even
                                        Code, the overall proved theorems increases by 9.90%, indicating
                                                                                                                                        if the improvement of symbolic provers falls within the capabili-
                                        the effectiveness of LLM2Ltac.
                                                                                                                                        ties of LLMs, we can reduce the expensive cost of invoking LLMs
                                                                                                                                        by offloading proving tasks to symbolic provers. Third, in many
                                        CCS Concepts                                                                                    real-world scenarios, LLM-based approaches cannot be used at all.
                                        • Theory of computation → Automated reasoning; • Software                                       For example, small companies cannot afford the cost of their own
                                        and its engineering → Formal software verification.                                             LLM servers, and cannot use public services due to confidentiality
                                                                                                                                        concerns. Therefore, this paper aims to improve the performance
                                        Keywords                                                                                        of symbolic provers for automated theorem proving.
                                        Automated Theorem Proving, Large Language Models, Tactic Min-                                       A key observation is that existing symbolic provers rely on the ex-
                                        ing, Formal Verification.                                                                       isting decision procedures [4, 15], and do not work well in domains
                                                                                                                                        that lack decision procedures. However, in many such domains, ex-
                                        Permission to make digital or hard copies of all or part of this work for personal or
                                        classroom use is granted without fee provided that copies are not made or distributed           isting proofs have already been written by human developers, and
                                        for profit or commercial advantage and that copies bear this notice and the full citation       these proofs embed reusable proof strategies that serve as practical
                                        on the first page. Copyrights for components of this work owned by others than the              alternatives to the missing decision procedures. Based on this ob-
                                        author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
                                        republish, to post on servers or to redistribute to lists, requires prior specific permission   servation, our basic idea is to enable symbolic provers to learn from
                                        and/or a fee. Request permissions from permissions@acm.org.                                     existing proofs: we mine the proof strategies from existing proofs,
                                        Conference acronym ’XX, Woodstock, NY                                                           formalize them as reusable tactics, and equip symbolic provers with
                                        © 2018 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                        ACM ISBN 978-1-4503-XXXX-X/2018/06                                                              this mined knowledge to handle cases where they would otherwise
                                        https://doi.org/XXXXXXX.XXXXXXX                                                                 fail.
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                      Jian Fang, Yixun Yao, and Yingfei XiongB


   We propose LLM2Ltac, the first approach that enables symbolic             Contribution. The contributions of this paper are as follows:
provers to mine proof strategies from existing formal proofs, using
LLMs as the bridge to mine and formalize proof knowledge into
reusable tactics. Note that LLM2Ltac does not train or fine-tune
                                                                              • We propose the first approach that enables symbolic provers
any neural network model; rather, it uses LLMs as an mining tool
                                                                                to mine reusable proof strategies from existing formal proofs
to surface proof strategies that already exist in proofs and make
                                                                                through LLMs, allowing the prover to apply this acquired
them accessible to symbolic provers. Concretely, the workflow of
                                                                                knowledge at proof time without runtime LLM interaction
LLM2Ltac is as follows: i) we collect a corpus of formal proofs from
                                                                                and supporting deployment in constrained environments.
existing verification projects as the knowledge source; ii) the LLM
                                                                              • We design a testing methodology that ensures mined tactics
analyzes each proof to understand the underlying reasoning pro-
                                                                                are generalizable to new proof goals outside the mining
cess; iii) the LLM identifies generalizable proof strategies embedded
                                                                                dataset.
in the proof; iv) the LLM formalizes each strategy as a symbolic
                                                                              • We implement and evaluate LLM2Ltac on multiple bench-
tactic; v) the mined tactics are integrated into the symbolic prover,
                                                                                marks, demonstrating that it enhances the automation capa-
enabling it to apply this acquired knowledge for automated proving.
                                                                                bility of symbolic provers.
   Key challenges in this approach are: i) How can we ensure that
mined tactics are useful? Many tactics generated by LLMs may be
syntactically incorrect, or they may be overfitted to the specific
proof from which they were mined, failing to generalize to new
problems. ii) How can we retrieve appropriate tactics for a given        2    Background
proof state? Traditional retrieval methods such as BM25 rely on          The Rocq Proof Assistant. Rocq [39] (formerly known as Coq)
textual similarity. Since tactics are a structured representation with   is an interactive theorem prover based on the Calculus of Induc-
limited textual content, textual similarity measures are insufficient    tive Constructions (CIC) [32]. Users state theorems and construct
for identifying relevant tactics effectively.                            machine-checked proofs interactively. At each step, the system
   To address the first challenge, we design a testing process that      maintains a proof goal: the proposition that remains to be proved.
ensures: i) the tactic can be correctly represented in the symbolic      When a proof begins, the goal is the theorem statement itself. Users
system; and ii) the tactic is generalizable by demonstrating appli-      enter tactics, each of which transforms the current goal into zero
cability to other theorems outside the mining dataset. To address        or more subgoals. Once all subgoals are discharged, the Rocq ker-
the second challenge, we record the theorem from which each tac-         nel type-checks the proof term, guaranteeing correctness inde-
tic was mined, and retrieve tactics by using BM25 to match the           pendently of the tactics that produced it. Rocq provides a rich
theorems that the tactices are mined from. By indexing tactics via       set of built-in tactics for common proof steps, including introduc-
their source theorems, we effectively enrich the text for retrieval,     ing hypotheses (intros), applying known lemmas (apply), rewrit-
as theorem statements carry richer textual information than tactics      ing with equalities (rewrite), and performing structural induction
themselves.                                                              (induction).
                                                                             Ltac. Ltac [17] is the tactic scripting language built into Rocq. It
    Evaluation. To evaluate LLM2Ltac, we collect 11,725 theorems         allows users to compose built-in tactics into higher-level, reusable
from Rocq standard library as the dataset for tactic mining. We          proof procedures. An Ltac definition binds a name to a tactic ex-
choose the standard library because it contains a substantial num-       pression. The language supports pattern matching on the proof
ber of theorems on commonly used data structures such as natural         goal and hypotheses via the match goal construct, recursion, back-
numbers, lists, and real numbers. To evaluate generalization capa-       tracking with the + and || operators, and looping via repeat and
bility, we collect a validation set containing 6,462 theorems from       do. Ltac is widely used to encode domain-specific proof automation
C-CoRN [12], including common algebraic structures (e.g., setoids,       in Rocq projects. In this paper, LLM2Ltac produces Ltac tactics
monoids, groups). We randomly select 93,424 different positions          as its reasoning strategy representation, so that the mined proof
across these theorems’ proof scripts to assess how broadly the           strategies can be directly loaded and invoked by the Rocq system.
mined tactic applies under different proof contexts. To evaluate the         CoqHammer. CoqHammer [13] is an automated theorem prov-
enhancement to the symbolic prover, we select large, real-world          ing tool for Rocq. It adapts the "hammer" methodology that has
open-source Rocq projects focused on software verification: Coq-         been effective in other proof assistants (e.g., Sledgehammer for Is-
Art [5], Ext-Lib [29], Vfa [3], and CompCert [25], in total 6199         abelle [8, 43]). The tool operates in three phases: Given a proof goal,
theorems. We collect a testing benchmark of 6199 theorems from           CoqHammer performs premise selection, translation to first-order
these four benchmarks, and evaluate whether our approach can             logic with external ATP invocation, and proof reconstruction inside
improve the proof capability of CoqHammer [13], the state-of-the-        Rocq to produce a fully checked proof term. CoqHammer is the
art symbolic prover in Rocq on these projects. Our results show          state-of-the-art general-purpose symbolic prover for Rocq [13]. We
that using the tactics mined by Deepseek-V3.2 [16], LLM2Ltac             use it as the baseline symbolic prover in our evaluation. Despite
enhances the number of theorems proved by CoqHammer directly             its strength, CoqHammer does not learn new proof strategies from
by 23.87%. When integrating the improved CoqHammer into the              existing proofs; it relies on the fixed set of ATPs and reconstruction
state-of-the-art proving agent, Claude Code [1], the overall number      tactics. LLM2Ltac addresses this limitation by mining reusable Ltac
of theorems proved increases by 9.90%, and the token consumption         tactics from proof corpora and integrating them into CoqHammer’s
is reduced by 10.51%.                                                    proof search.
A Learning Method for Symbolic Systems Using Large Language Models                              Conference acronym ’XX, June 03–05, 2018, Woodstock, NY


3     Overview                                                             Proof. induction i; simpl; congruence. Qed.
In this section, we present an overview of LLM2Ltac, a framework           where positive is an inductive data type that represents strictly
designed to mine reasoning strategies. We will use some examples           positive integers in a binary way.
to demonstrate the workflow of our approach.                                  The LLM provides the following natural language description
   We consider the theorem LTree_bisimilar_label in Figure 2,              for the effect of each tactic:
which comes from the Coq-Art project. This theorem describes a
                                                                           ### Step -by - step explanation
fundamental property of infinite trees. LTree is a tree data structure     1. ** induction i **
                                                                               - ** Effect :** Performs induction on the binary positive
defined by CoInductive [9]. Unlike inductive types that construct              integer i.
finite structures, coinductive types allow the definition of poten-            So the induction generates three subgoals :
                                                                                 - Base case : i = xH
tially infinite structures. The CoInductive keyword enables the                  - Inductive case for xO p with IH for p ...
construction of infinite trees where branches can continue indefi-         2. ** simpl **
                                                                               - ** Effect :** ...
nitely. The LTree_bisimilar defines a property between infinite                ...
trees, establishing when two trees should be considered equivalent.
This relation states that two trees are bisimilar if they have the         We can observe that the LLM analyzed the roles of three tactics
same structure: either both are leaves, or both are binary nodes           (induction, simpl, congruence) in this proof and the impact on
with the same label and bisimilar left and right subtrees.                 the goals when each tactic is applied. Then, by providing the proof
   Here, a path is defined as a list of directions (left or right) that    process and the meaning of each proof step as input, we guide the
navigates through the tree structure. The function L_subtree tra-          LLM to give a general reasoning strategy.
verses the tree following the given path to extract a specific subtree,       NL strategies generalization. In the second step, we require the
while LTree_label extracts the label at the root of that subtree.          LLM to summarize the given proof analysis into generalizable strate-
   The theorem LTree_bisimilar_label states that if two trees              gies. After providing the above proof analysis to the LLM, the LLM
are bisimilar, they must have the same label at any given path. That       gave the following general proof method:
establishes that bisimilarity preserves labels throughout the entire
                                                                           ## General Proof Strategies
tree structure, which is a fundamental property for reasoning about        ### 1. **Structural Induction with Recursive Data Types**
infinite trees. However, this theorem cannot be directly proven by         This pattern is widely applicable to theorems about recursive data
                                                                            structures like lists , trees , and natural numbers , where
the automatic theorem prover CoqHammer.                                    properties can be proven by following the structure 's definition .
                                                                           ...
   The workflow of LLM2Ltac is shown in Figure 1. The entire               ### 2. **Definition-Driven Simplification Followed by Automated Equality
framework is divided into three stages, where the first two steps are                Resolution**
                                                                           This two - step approach combines :
performed offline, similar to the training phase of machine learning,      1. ** simpl tactic **: Expands and reduces terms based on their
and the last step is performed online when proving new theorems.           definitions in the context
                                                                           2. ** congruence tactic **: Automatically solves goals that become
      • Stage 1: Tactic mining. In this stage, we use large language       simple equalities after simplification
                                                                           ...
        models to mine reasoning strategies from a set of theorems         ### 3. **Combination Pattern Recognition**
                                                                           The proof demonstrates a common pattern : when a property is
        and their proofs.                                                  definitionally true for a recursive type , the proof often follows
      • Stage 2: Validity and generalization testing. After mining         the template :
                                                                           induction < variable >; simpl ; <auto - solver like congruence / auto >
        the tactics, we need to ensure their validity and generalizabil-   ...
        ity. We design specific tests to verify that the mined tactics
        can be applied in various scenarios.                                  We can observe that the LLM provides general proof strategies.
      • Stage 3: Tactic integration. We combine the mined tactics          The first strategy is a standard one for recursive data types, which
        with symbolic provers to form a new prover with better             suggests the use of structural induction. The LLM also gives poten-
        theorem-proving capability. The prover uses these tactics to       tial usage scenarios such as lists, trees, and natural numbers. The
        convert complex theorems into simpler goals until they can         second strategy is to use automated equality resolution after simpli-
        be automatically solved.                                           fication operations. The third strategy is a combination pattern that
                                                                           prescribes how to compose multiple tactics into a single reusable
3.1     Tactic Mining                                                      sequence, it describes how the three tactics can be combined to
                                                                           form higher-level proof methods. We can observe that all strategies
   Proof analysis. For each theorem and proof in the dataset, we ask       generalize beyond the current lemma and can be used in proving
the LLM to explain the purpose of each tactic in the proof, and what       other theorems.
it means to use this tactic at the current position in natural language
(NL). We analyze each tactic individually rather than asking the              Autoformalization. We require the LLM to formalize the new
LLM to describe the proof as a whole, because the LLM tends to             general proof strategies described in natural language into the
omit tactics whose effects are less apparent when summarizing              tactic language used by the symbolic system. Since the theorems
an entire proof at once. Per-tactic analysis yields more detailed          we selected are obtained from Rocq projects, for consistency, we
descriptions that capture the specific effect of every proof step. For     formalize the new proof strategies into tactics represented in Ltac
example, the following is a theorem from the dataset:                      in Rocq [17]. Note that the role of autoformalization here is solely to
                                                                           translate natural language strategies into a symbolic representation;
Lemma append_neutral_r :                                                   the correctness and generalizability of the resulting tactics are not
  forall (i : positive), append i xH = i.                                  assumed but are instead verified by the subsequent testing stage.
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                         Jian Fang, Yixun Yao, and Yingfei XiongB




                                                          Figure 1: The workflow of LLM2Ltac


(* Infinite trees with internal nodes labeled *)                             Ltac structural_induction_recursive :=
CoInductive LTree (A:Type) : Type :=                                           match goal with
  LLeaf : LTree A                                                              | [ |- forall p : positive, _ ] ⇒
| LBin : A → LTree A → LTree A → LTree A.                                    induction p; simpl; try congruence
                                                                               | [ |- forall n : nat, _ ] ⇒
(* An extensional equality on (LTree A) *)                                   induction n; simpl; try congruence
CoInductive LTree_bisimilar : LTree A → LTree A → Prop :=                      | [ |- forall l : list ?A, _ ] ⇒
  LTree_bisimilar_leaf : LTree_bisimilar LLeaf LLeaf                         induction l; simpl; try congruence
| LTree_bisimilar_bin :                                                        | [ |- forall t : ?T, _ ] ⇒
    forall (a:A) (t1 t'1 t2 t'2 : LTree A),                                        match T with
      LTree_bisimilar t1 t'1 →                                                     | ?T' ⇒ induction t; simpl; try congruence
      LTree_bisimilar t2 t'2 →                                                     end
      LTree_bisimilar (LBin a t1 t2) (LBin a t'1 t'2).                         end.

Theorem LTree_bisimilar_label :
                                                                             Figure 3: One mined tactic from lemma append_neutral_r by
  forall (p:path) (t t': LTree A),
                                                                             LLM2Ltac
    LTree_bisimilar t t'
      → LTree_label t p = LTree_label t' p.

                                                                             theorems that are not included in the mining dataset. We then apply
        Figure 2: Theorem to be proved in benchmarks                         the tactic into each position in the theorems’ proving processes. If
                                                                             the proof statement changes after the application, we consider the
                                                                             tactic to have generalization capability and retain it; otherwise, we
In this example, multiple tactics are formalized, and we show one            discard it. For the retained tactics, LLM2Ltac records the source
tactic formalized from Strategy 3 as an example.                             theorem from which the tactic was mined, which will be used for
                                                                             retrieval when proving new theorems.
3.2     Validity and Generalization Testing
Due to LLM hallucinations, the generated code by LLM may not be              3.3    Tactic Integration
valid, so we need to test whether it is formalized correctly in Rocq         In this stage, LLM2Ltac combines the mined tactics with a symbolic
Ltac. In addition, LLM2Ltac also tests the generalization of tactics         prover. Given a proof goal that cannot be directly resolved by the
to ensure they can be used for proving other theorems. Note that             symbolic prover, we retrieve relevant tactics. As mentioned before,
a valid tactic is correct by construction in the Rocq system, and            tactics contain limited textual information and direct retrieval of
would never result in a incorrect proof.                                     tactics is ineffective. Our approach uses the theorems for mining
   To test validity, we employ a test-and-repair framework using             tactics as the bridge for retrieval. We first use BM25 to identify the
the Rocq compiler. If compilation fails, we ask the LLM to repair the        theorems that are most similar to the current proof goal from the
tactic. Tactics that fail after a fixed number of repairing attempts are     dataset for tactic mining, and return the tactics mined from the
discarded. To test generalizability, we use a validation set containing      theorems. Next, we apply each of the retrieved tactics to transform
A Learning Method for Symbolic Systems Using Large Language Models                             Conference acronym ’XX, June 03–05, 2018, Woodstock, NY




                                                   Figure 4: Workflow of generalization testing


the current proof goal and then apply the symbolic prover again.           in Figure 6. We use natural language descriptions for proof analy-
We construct an And-Or tree [10] to try different combinations of          sis and generalization, as LLMs are more powerful in understand-
the above process until the theorem is proved.                             ing and generating natural language compared to symbolic lan-
   For the theorem in Figure 2, though CoqHammer cannot directly           guage [42].
prove the theorem, the enhanced prover can retrieve the theorem               Autoformalization. In the autoformalization step [44], we use
append_neutral_r and use tactic structural_induction_recursive             LLMs to convert the natural language descriptions of reasoning
to convert the theorem into new goals that can be automatically            strategies into the formal language. The prompts used in the LLM
solved by CoqHammer.                                                       are shown in Figure 7. During autoformalization, the LLM trans-
                                                                           lates the high-level strategic descriptions into Ltac [17], the tactic
                                                                           language of Rocq. We provide the LLM with Ltac documentation
4     Approach                                                             and examples to facilitate accurate translation, and instruct it to
In this section, we present the detailed design of LLM2Ltac. As            generate parameter-free tactics that match patterns in the proof
illustrated in Figure 1, the workflow of LLM2Ltac consists of three        goal.
main stages: i) Tactic mining. In this stage, LLM2Ltac mines
potential tactics from LLMs. ii) Validity and generalization test-
ing. The testing checks the tactics that are syntactically valid and
applicable to other theorems. iii) Tactic integration. LLM2Ltac            4.2    Validity and Generalization Testing
incorporates the mined tactics into the symbolic prover, employing         Validity Testing. The purpose of this stage is to test the tactics
a new retrieval method to select appropriate tactics based on the          mined from the LLM. In validity testing, we design a test-and-repair
proof goal.                                                                framework to test whether the mined tactics are valid. We use
                                                                           the symbolic verifier to compile each tactic. If the verifier finishes
                                                                           compilation without errors, we consider the tactic to be valid within
4.1    Tactic Mining                                                       the logical system. If the verifier reports errors, we provide both the
By inputting a dataset of theorems, we aim to mine the reasoning           error message and the current tactic back to the LLM, prompting
patterns that are already formed within proofs. This mining process        it to repair the errors. If the number of repair attempts exceeds a
consists of three steps: proof analysis, natural language strategy         threshold, we discard this tactic.
generalization, and autoformalization.                                         Generalization Testing. Generalization testing evaluates whether
   Proof Analysis. In the proof analysis step, we prompt LLMs to           the tactics can be applied to theorems in other projects. We collect
analyse the proof steps of given theorems. We require the LLM to           a large number of theorems from other projects as the benchmark.
perform two tasks. The prompts are shown in Figure 5. Specifically,        The workflow is shown in Figure 4. The overall workflow proceeds
the LLM performs two tasks per proof step: (1) explaining the              as follows: first, since a single theorem may yield multiple tactics,
semantic meaning of each tactic (e.g., what rewrite or induction           we employ a parser to decompose the tactic into individual tactic
does), and (2) describing the effect of each tactic on the current         definitions along with their required header files and type defini-
proof goal. To support accurate analysis, we supply the LLM with           tions. This decomposition step is crucial as it isolates each tactic as
the types and definitions of inductive data referenced in the tactic       an independent unit while preserving all necessary dependencies
parameters.                                                                for compilation. Then, for each mined tactic, LLM2Ltac automat-
   Natural language strategies generalization. In this step, we            ically generates a Rocq plugin that wraps the tactic with all its
prompt the LLM to identify which steps from the previous proof             required dependencies and exposes it through a named interface.
analysis can be abstracted to a higher level. The prompt is shown          This plugin-based method allows each proof script to load a tactic
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                        Jian Fang, Yixun Yao, and Yingfei XiongB




                       Figure 5: Prompts in proof analysis                 Figure 6: Prompts in natural language generaliza-
                                                                           tion


                                                                             4.3    Tactic Integration
                                                                            Tactics that pass the generalization testing are combined with a
                                                                            symbolic prover for better theorem proving. Since existing symbolic
                                                                            provers do not support the utilization of the tactics presented in the
                                                                            code, we design an algorithm to alternately invoke the symbolic
                                                                            prover and apply tactics, shown as algorithm Solve in Algorithm 1.
                                                                            The algorithm models proof search by constructing an And-Or
                                                                            tree [10]. Each proof goal forms an Or-node: it is solved if any tactic
                                                                            succeeds. Each tactic application forms an And-node: it requires
                                                                            all resulting subgoals to be proved.

                                                                            Algorithm 1 And-Or Tree Proof Search with Tactic Retrieval
            Figure 7: Prompts in Autoformalization                            1: function Solve(𝑔𝑜𝑎𝑙)
                                                                              2:     𝑟𝑜𝑜𝑡 ← OrNode(𝑔𝑜𝑎𝑙)
                                                                              3:     𝑞𝑢𝑒𝑢𝑒 ← Queue( ); 𝑞𝑢𝑒𝑢𝑒.Enqeue(𝑟𝑜𝑜𝑡)
                                                                              4:     while 𝑞𝑢𝑒𝑢𝑒 is not empty ∧ ¬ 𝑟𝑜𝑜𝑡 .𝑠𝑜𝑙𝑣𝑒𝑑 do
                                                                              5:        𝑛 ← 𝑞𝑢𝑒𝑢𝑒.Deqeue( )
                                                                              6:         if ApplyATP(𝑛.𝑔𝑜𝑎𝑙) then
                                                                              7:             Propagate(𝑛); continue
via a single command, avoiding repeated script modifications and
dependency conflicts across different tactics.                                8:         Thms ← RetrieveTheorems(𝑛.𝑔𝑜𝑎𝑙, 𝑘)
   For generalization testing, we insert each mined tactic after ev-          9:        𝑇 ← GetTactics(Thms)
ery original tactic in the benchmark proof scripts (except for the           10:         for each 𝑡 ∈ 𝑇 do
last tactic that closes the goal), and check whether it successfully         11:             𝑠𝑢𝑏𝑔𝑜𝑎𝑙𝑠 ← Apply(𝑡, 𝑛.𝑔𝑜𝑎𝑙)
produces a new proof state. As shown in Figure 4 theorem 3, a con-           12:             𝑎 ← AndNode( ); 𝑛.AddChild(𝑎)
crete example demonstrates the inserting positions of the tactics            13:             if 𝑠𝑢𝑏𝑔𝑜𝑎𝑙𝑠 = ∅ then
(marked by "Ltac position"). A tactic is considered to be generaliz-         14:                 Propagate(𝑎)
                                                                             15:             else
able if, given the current proof state and theorem, it produces new
proof states without reporting errors (a tactic without errors but           16:                 for each 𝑔′ ∈ 𝑠𝑢𝑏𝑔𝑜𝑎𝑙𝑠 do
makes no changes to the proof state is discarded). We record the             17:                    𝑐 ← OrNode(𝑔′ ); 𝑎.AddChild(𝑐)
                                                                             18:                    𝑞𝑢𝑒𝑢𝑒.Enqeue(𝑐)
number of successful applications across all benchmark positions
as a metric of generalization capability. Specifically, we consider a        19:     return 𝑟𝑜𝑜𝑡 .𝑠𝑜𝑙𝑣𝑒𝑑
tactic to have generalization capability if its application success rate
across all benchmark positions falls within [10%, 100%) (details in             Given a proof goal, Solve first attempts to close it with the au-
Section 5.1). A tactic with a success rate below 10% is considered too       tomated theorem prover. If that fails, it retrieves the top-𝑘 most
narrow to use reliably. Conversely, a tactic that succeeds in 100%           similar theorems using RetrieveTheorems. Since Ltac is a struc-
of positions is considered over-general: such a tactic typically only        tured representation, term-frequency algorithms such as BM25 [34]
introduces a fresh variable to alias an existing term in the proof           cannot be directly applied. To address this, LLM2Ltac records the
context, which changes the proof state without making meaningful             source theorem from which each tactic was mined during general-
reasoning progress.                                                          ization testing. In our algorithm, the current proof goal is compared
A Learning Method for Symbolic Systems Using Large Language Models                              Conference acronym ’XX, June 03–05, 2018, Woodstock, NY


           Table 1: Impact of 𝑘 value on Algorithm 1                             • Ext-Lib [29]: a community-driven Rocq library that is widely
                                                                                   reused across diverse Rocq projects.
             𝑘 value     Proved      Time Consumption                            • Vfa [3]: the third volume of Software Foundations covering
                10         77             2212.89s                                 well-established properties of verified functional algorithms.
                20         85             3571.96s                               • CompCert [25]: an industrial-scale formally verified C com-
                30         87             4103.70s                                 piler with machine-checked proofs of semantic preservation
                                                                                   across multiple compilation passes, memory models, and
                                                                                   target architectures.
against these source theorems using a retrieval algorithm. Then, it         Together, they span varying levels of proof complexity and applica-
locates the tactics mined from these theorems using the GetTac-             tion domains, making them a rigorous testbed for evaluating the
tics function. Each tactic application creates an And-node whose            generalization of LLM2Ltac.
children are new Or-nodes for the resulting subgoals, which are                Configurations. We used OpenAI GPT-5.2 [30] and Deepseek-
enqueued for subsequent processing. When a node is solved, Propa-           V3.2 [16] for evaluation experiments. For the tactic repair process
gate walks upward through the tree: an Or-node is marked solved             in Section 4.2, we set the threshold to 3. The total API cost for
when any child succeeds; an And-node is marked solved only when             tactic mining was $1,528.65, of which Deepseek-V3.2 accounted for
all its children are solved.                                                $108.93 and GPT-5.2 for $1,419.72, well below the cost of GPU infras-
    The parameter 𝑘 controls how many similar theorems are re-              tructure to host comparable models locally. We set CoqHammer’s
trieved at each node. A larger 𝑘 increases the chance of finding a          timeout to default value, which is 20 seconds, and for each theorem
useful tactic but also expands the search space and increases time          to be proved, we set the timeout to 600 seconds. We select mined tac-
cost. We randomly select 50 samples from each benchmark (men-               tics whose application success rate falls within [10%, 100%) (at least
tioned in Section 1), for a total of 200 samples. we set 𝑘 to 10, 20, and   10% but less than 100%) in generalization testing. For the retrieval
30, respectively, and record the number of proved theorems and the          algorithm, since our approach targets resource-constrained settings,
time consumed for each setting. and the result is shown in Table 1.         embedding-based models that require high-performance GPUs are
We evaluate this trade-off and set 𝑘 = 20 for our approach.                 not applicable for tactic retrieval. We therefore choose BM25 to
                                                                            index tactics, which runs efficiently on CPUs [34]. Prior work has
5    Evaluation                                                             also shown that BM25 outperforms embedding-based models for
We focus on the following research questions:                               retrieval in theorem proving [40]. All experiments were conducted
     • RQ1: How effective is LLM2Ltac in mining tactics?                    on a server equipped with four 26-core Intel Xeon Platinum 8270
     • RQ2: To what extent do the tactics mined from LLMs by                CPUs, 256 GB RAM, and running Ubuntu 24.04.4.
       LLM2Ltac improve the success rate of symbolic provers?
     • RQ3: Do the mined tactics benefit LLM agents?                        5.1    RQ1: How effective is LLM2Ltac in mining
     • RQ4: How does LLM2Ltac perform compared to existing                         tactics?
       lemma extraction methods?                                               Procedure. This experiment evaluates the tactic mining of LLM2Ltac.
     • RQ5: How do mining methods affect the mined tactics?                 We apply LLM2Ltac to mine tactics from 11,725 theorems in the
     • RQ6: To what extent does the generalization testing in               Rocq standard library. For validity testing, we record the number
       LLM2Ltac impact the improvement of symbolic provers?                 of tactics obtained by OpenAI GPT-5.2 and Deepseek-V3.2 at each
    Implementation. We have implemented LLM2Ltac on Rocq                    stage of the LLM2Ltac. For generalization testing, we count the
8.20.0. To obtain the argument information in Section 4.1, we mod-          generalizability distribution of valid tactics, and classify all valid
ified parts of the Rocq compiler to extract argument types and              tactics into groups based on their success rate with an interval of
type definitions. We selected CoqHammer, the state-of-the-art au-           10%, as shown in Figure 8.
tomated theorem prover in Rocq [13], as the symbolic prover for
evaluating performance improvements.                                                 Table 2: Detailed Statistics for Tactic Mining
    Dataset. We selected different benchmarks from Rocq open-
source projects for different stages in LLM2Ltac. We collected                                                      OpenAI GPT-5.2        Deepseek-V3.2
11,725 theorems from the Rocq standard library for mining tactics.           Mined Tactics                              49909                35408
We collected 6,462 theorems from the C-CoRN [12] dataset, which              Valid Tactics                              16902                13174
contains theorems on common algebraic structures (e.g., setoids,             Generalizable Tactics ([10%,100))           5766                 2025
monoids, groups) and large proof procedures for complex proper-
ties, for testing generalization. For each candidate tactic, we insert
it at all 93,424 different positions across these 6,462 theorems’ proof        Results. As shown in Table 2, “mined tactics” represents the
processes to assess how broadly the tactic applies under different          number of natural language tactics obtained from LLMs, “valid
proof contexts. To evaluate the improvement to symbolic provers,            tactics” represents the number of tactics that pass the Rocq compiler,
we selected the following four benchmarks to evaluate different             and “generalizable tactics” represents the number of tactics whose
verification tasks:                                                         generalization testing success rate falls within [10%, 100%).
     • Coq-Art [5]: a Rocq textbook covering well-established                  We observe that OpenAI GPT-5.2 mines more tactics (49,909)
       properties of data structures and algorithms.                        compared to Deepseek-V3.2 (35,408). After validity testing, the pass
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                      Jian Fang, Yixun Yao, and Yingfei XiongB


                                                                             Results. As shown in Table 3, integrating the tactics mined by
                                                                          LLM2Ltac significantly improves the performance of CoqHam-
                                                                          mer across all four benchmarks. Using tactics mined by OpenAI
                                                                          GPT-5.2, CoqHammer proves 1950 theorems, compared to 1592
                                                                          theorems by the original CoqHammer, representing a 22.49% over-
                                                                          all improvement. The improvements on individual benchmarks
                                                                          range from 17.27% on Coq-Art to 26.58% on Ext-Lib. Using tac-
                                                                          tics mined by Deepseek-V3.2, CoqHammer proves 1972 theorems,
                                                                          achieving 23.87% overall improvement. While both models demon-
                                                                          strate substantial improvements, the performance of tactics mined
                                                                          from different LLMs is different. This difference indicates that the
                                                                          reasoning strategies mined from different LLMs have an impact
                                                                          on the performance of LLM2Ltac. Notably, as shown in Table 2,
       Figure 8: Distribution of Tactic Generalizability                  GPT-5.2 produces nearly three times more generalizable tactics than
                                                                          Deepseek-V3.2 (5,766 vs. 2,025), yet its proving count is slightly
                                                                          lower (1,950 vs. 1,972). This suggests that a larger number of tac-
rates are comparable: 33.87% for OpenAI GPT-5.2 and 37.21% for            tics does not necessarily lead to better proving performance. A
Deepseek-V3.2. For generalization testing, we observe that LLMs           larger tactic pool introduces more noise during retrieval, causing
still exhibit severe hallucinations in tactic mining: most generated      the prover to spend time on less effective tactics before finding the
tactics are incorrect and lack generalization capability, even though     right one.
LLMs believe they are correct and generalizable. We further observe
notable differences in the generalization distributions across models,
and the majority of mined tactics fall below the 10% success rate.          Answer to RQ2: The tactics mined by LLM2Ltac significantly
This also indicates the necessity of the testing process in LLM2Ltac.       enhance the capability of CoqHammer by 17.27% to 26.58%,
                                                                            and the improvements are related to the reasoning capability
   Case Study. To illustrate the diversity of mined tactics, we present
                                                                            of the underlying LLMs, suggesting further improvements as
a representative example beyond the induction-based strategy shown
                                                                            LLMs advance.
in Figure 3. The following tactic shows a tactic mined by LLM2Ltac
that operates in a fundamentally different way.
Ltac apply_constructor_auto_217 :=                                        5.3    RQ3: Do the mined tactics benefit LLM
  match goal with
                                                                                 agents?
  | [ |- ?R ?A ?B ] ⇒
      try (apply permA_swap; auto);
                                                                             Procedure. Due to the high cost of LLM-based agents, we sam-
      try (intuition; auto)
                                                                          ple 50 theorems from the test set of each benchmark, in total 200
  end.
                                                                          theorems, the same as in RQ2, to evaluate whether LLM2Ltac can
                                                                          benefit the LLM-based agent. We select Claude Code [1], the state-
   This tactic first pattern-matches the current proof goal against       of-the-art LLM-based agent, powered by Claude Sonnet 4.6 [2] as
a relational structure ?R ?A ?B, then attempts to apply a lemma           the base model. [31] shows that Claude Code also performs well
permA_swap and invokes built-in Rocq tactics auto and intuition           on Rocq theorem proving.
to discharge remaining subgoals. Unlike the induction-based tactic           We write three categories of skills to instruct Claude Code to
in Figure 3, this example shows that LLM2Ltac can mine strate-            write theorem proofs. The first category covers the base proving
gies that reason about the goal’s structure, apply project-specific       pipeline, guiding the agent to locate the target theorem within
lemmas, and compose multiple existing tactics in Rocq.                    a project and verify whether a constructed proof is correct. This
                                                                          category is common to all three settings in the following evaluation.
  Answer to RQ1: LLM2Ltac is able to mine generalizable tac-              The second category is CoqHammer-specific: it instructs the agent
  tics from LLMs, and the testing process is necessary to filter          on how to import the required header files into the proof script and
  out invalid or non-generalizable tactics.                               which tactics to apply. The third category is LLM2Ltac-specific: it
                                                                          explains to the agent how to use the LLM2Ltac-enhanced prover.
5.2     RQ2: To what extent do the tactics mined                          Both categories direct the agent to first attempt to prove the theorem
                                                                          with the respective tool, and only if that attempt fails, to synthesize
        from LLMs by LLM2Ltac improve the                                 a proof on its own. For each task, we grant Claude Code three tool
        success rate of symbolic provers?                                 permissions: bash, read, and edit, allowing the agent to execute
   Procedure. We use CompCert, Ext-Lib, Coq-Art, and Vfa four             shell commands, read files, and edit files. We set a timeout of 600
benchmarks, 6199 theorems in total, to test the automatic capability      seconds for each proof task.
of the prover. We compare the LLM2Ltac-enhanced CoqHammer                    We evaluate three settings: i) Claude Code proves theorems
against the original CoqHammer. For each experiment, we use the           without access to CoqHammer; ii) Claude Code proves theorems
default configuration of CoqHammer and the timeout is set to 20           with access to CoqHammer via the corresponding skills; iii) Claude
seconds.                                                                  Code proves theorems with the LLM2Ltac-specific skills. For each
A Learning Method for Symbolic Systems Using Large Language Models                               Conference acronym ’XX, June 03–05, 2018, Woodstock, NY


                               Table 3: Performance of CoqHammer with and Tactics Mined By LLM2Ltac

                                                               OpenAI GPT-5.2                   Deepseek-V3.2
                                                                       CoqHammer                        CoqHammer
                                           #Lemma       CoqHammer                       CoqHammer
                                                                        +LLM2Ltac                       +LLM2Ltac
                           CompCert          4840          1022      1269 (↑ 24.17%)       1022       1276 (↑ 24.85%)
                            Ext-Lib           187           79         100 (↑ 26.58%)       79           99 (↑ 25.32%)
                           Coq-Art            842           411        482 (↑ 17.27%)      411         498 (↑ 21.17%)
                              Vfa             330           80          99 (↑ 23.75%)       80           99 (↑ 23.75%)
                             Total           6199          1592      1950 (↑ 22.49%)       1592       1972 (↑ 23.87%)


setting, we record the number of theorems successfully proved and            Table 5: Comparison with the lemma extraction approach
the total token consumption of Claude Code.                                  Strat2Rocq

            Table 4: Performance of the LLM Agents                                                               CoqHammer           CoqHammer
                                                                                              CoqHammer
                                                                                                                +Strat2Rocq          +LLM2Ltac
                                Claude Code            Claude Code              CompCert          1022              1072                1276
             Claude Code                                                         Ext-Lib           79                73                  99
                               + CoqHammer             + LLM2Ltac
 #Thm             71                 101               111 (↑ 9.90%)            Coq-Art           411               379                 498
 Tokens        59899928           38346691          34317809 (↓ 10.51%)            Vfa             80                71                  99
                                                                                  Total           1592              1595                1972

   Results. As reported in Table 4, the LLM2Ltac-enhanced agent
proved 111 out of 200 randomly sampled theorems, compared to
101 by the CoqHammer-enhanced agent (a 9.90% improvement).                   mining lemmas and the dataset for testing are more related, and
This result demonstrates that LLM2Ltac is more effective than                may come from the same project, while in our evaluation the two
CoqHammer when integrated into a LLM-based proving agent.                    sets are from strictly different projects, better matching real-world
Meanwhile, the token consumption decreased from 38346691 to                  scenarios. This result suggests that the tactics mined by our ap-
34317809, a 10.51% reduction. This demonstrates that LLM2Ltac                proach are more generalizable across different projects compared
not only enhances the proving capability of LLM agents but also              to the lemmas mined by Strat2Rocq.
reduces their token cost.
                                                                               Answer to RQ4: LLM2Ltac significantly outperforms
  Answer to RQ3: The mined tactics from LLM2Ltac can benefit
                                                                               Strat2Rocq, especially when the dataset for mining and the
  LLM agents by improving their theorem-proving success rate
                                                                               dataset for testing are less closely related.
  and reducing token consumption.


5.4    RQ4: How does LLM2Ltac perform                                        5.5    RQ5: How do mining methods affect the
       compared to existing lemma extraction                                        mined tactics?
       methods?                                                                 Procedure. To evaluate the contribution of different components
   Procedure. As will be discussed in Section 6, a recently posted           in the mining process, we conduct an ablation study using Deepseek-
work, Strat2Rocq [18], mines lemmas from the LLM reasoning                   V3.2. Specifically, we compare three configurations: (1) the original
process to enhance symbolic provers. To compare our approach                 LLM2Ltac with all components, (2) LLM2Ltac without the nat-
with Strat2Rocq, we implemented their approach to extract lem-               ural language analysis step (the first step in Section 4.1), and (3)
mas from the LLM reasoning process over the same dataset used                LLM2Ltac without the natural language generalization step (the
in RQ1. We then integrate the extracted lemmas into CoqHam-                  second step in Section 4.1). We apply these configurations to mine
mer and evaluate the performance improvement on the same four                tactics from the same dataset and measure the number of mined
benchmarks used in RQ2.                                                      tactics, valid tactics, and generalizable tactics.

   Results. The results are shown in Table 5. By reproducing Strat2Rocq,    Results. As shown in Table 6, the ablation study reveals the im-
we extracted 2,977 new lemmas and integrated them into CoqHam-           portance of both natural language analysis and generalization steps
mer’s context. In our experiments, we observe that, under the cur-       in LLM2Ltac. Removing the natural language analysis step leads
rent experimental setup, Strat2Rocq does not effectively enhance         to a 34.31% reduction in mined tactics, with more drops in valid
the symbolic prover. This discrepancy from the existing evaluation       tactics (51.64% decrease) and generalizable tactics (71.56% decrease)
results reported in the Strat2Rocq paper may be attributed to            test pass rates. This indicates that the analysis step is helpful for
the differences in dataset selection. In their paper, the dataset for    guiding LLMs to generate higher-quality tactic candidates.
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                               Jian Fang, Yixun Yao, and Yingfei XiongB


                                                Table 6: The ablation study of the mining methods

                                                                                                 -NL                 -NL
                                                                    Original Tactics
                                                                                               Analysis          Generalization
                                                                                             #     Change         #     Change
                          Mined Tactics                                     35408          23256 ↓ 34.31%      38003 ↑ 7.33%
                          Valid Tactics                                     13174           6371 ↓ 51.64%       4415 ↓ 66.49%
                          Generalizable Tactics ([10%, 100%))                2025           576   ↓ 71.56%      231    ↓ 88.59%


   Without the natural language generalization step, valid tactics                      Answer to RQ6: The results demonstrate that the general-
drop by 66.49%. This indicates that directly formalizing proof anal-                    ization testing is effective in improving the performance of
ysis is more challenging for LLMs than describing tactics in natural                    LLM2Ltac.
language. Generalizable tactics decreased by 88.59%. This demon-
strates that the tactic generalization step plays a crucial role in
producing the final usable generalizable tactics.                                   6     Related Work
                                                                                    Recent work uses LLMs to extract structured knowledge such as
  Answer to RQ5: Both the proof analysis and tactic general-                        logic rules [28], mathematical equations [36], knowledge graphs [46],
  ization steps are essential for LLM2Ltac to mine tactics from                     and lemmas [18]. These methods target specific rule types and data
  LLMs.                                                                             sources, and none of them mine reusable tactics from formal proofs.
                                                                                    LLM2Ltac fills this gap by mining reasoning strategies from exist-
                                                                                    ing proofs and using the mined tactics to enhance symbolic provers.
5.6     RQ6: To what extent does the generalization                                    The most related work is Strat2Rocq [18], which also enhances
        testing in LLM2Ltac impact the                                              automatic theorem proving but extracts lemmas rather than tac-
        improvement of symbolic provers?                                            tics. LLM2Ltac differs in three ways: (1) we mine reusable tactics
                                                                                    from existing formal proofs (written by humans or LLMs), rather
   Procedure. To evaluate the impact of generalization testing, we
                                                                                    than extracting strategies solely from LLM internals; (2) tactics are
compare two settings using tactics mined from Deepseek-V3.2: (1)
                                                                                    more generally applicable than lemmas, which only match proof
CoqHammer enhanced with all mined tactics, without applying gen-
                                                                                    goals of specific types; and (3) we introduce an indirect retrieval
eralization testing, and (2) CoqHammer enhanced only with tactics
                                                                                    method that addresses the lack of textual information in Ltac tactics.
that have passed generalization testing (passing rate in [10%, 100%)).
                                                                                    Our evaluation shows that LLM2Ltac significantly outperforms
We use the same four benchmarks and experimental configuration
                                                                                    Strat2Rocq.
as in RQ2 to measure the performance difference.
                                                                                       Machine learning-based methods. Many machine learning meth-
                                                                                    ods have been applied to theorem proving [6, 7, 19, 21, 22, 27, 35,
Table 7: Impact of Generalization Testing on Performance                            40, 41, 45]. These approaches can be divided into two categories: i)
with LLM2Ltac                                                                       training new models for theorem proving through large amounts
                                                                                    of corpus, and ii) implementing agents to interact with LLMs to
                                                          CoqHammer                 generate proof scripts. In other way, a non-trivial neural model is
                                      CoqHammer
                 CoqHammer                                +LLM2Ltac                 involved in the proving process. On the other hand, LLM2Ltac fo-
                                    +LLM2Ltac
                                                          -(GT)                     cuses on enhancing symbolic provers, and as our evaluation shows,
 CompCert        1022               1276                  1092                      the enhancement complements neural models, and can further im-
 Ext-Lib         79                 99                    79                        prove the performance of proving agents as well as reducing their
 Coq-Art         411                498                   460                       costs.
 Vfa             80                 99                    77
                                                                                       Symbolic provers. Many existing symbolic provers are proposed
 Total           1592               1972                  1708 (↓ 13.39%)
                                                                                    to reduce the burden of manually writing proof scripts, such as
                                                                                    CoqHammer [13], Lean-auto [33], and Sledgehammer [8]. These
                                                                                    provers typically focus on integrating existing automated theorem
   Results. As shown in Table 7, we observe that for CompCert and                   provers (ATPs) such as SMT solver to prove theorems in the target
Coq-Art, CoqHammer enhanced with tactics that have not passed                       proof language, and none of them attempt to mine new tactics from
generalization testing shows improvement over the original Co-                      existing proofs as far as we are aware.
qHammer. However, their performance is lower than CoqHammer
enhanced with tactics that have passed generalization testing. This                 7     Conclusion and Future Work
demonstrates the effectiveness of generalization testing. Without                   In this paper, we studied how to enhance provers to mine general-
generalization testing, many ineffective tactics are present, prevent-              izable tactics from large language models. We proposed LLM2Ltac,
ing the retrieval of effective tactics.                                             the first framework for mining tactics from LLMs with support for
                                                                                    generalization validation. Our evaluation experiments demonstrate
A Learning Method for Symbolic Systems Using Large Language Models                                                     Conference acronym ’XX, June 03–05, 2018, Woodstock, NY


that by using LLM2Ltac, the success rate of CoqHammer improved                               [16] DeepSeek-AI. 2025. DeepSeek-V3.2: Pushing the Frontier of Open Large Language
by 23.87%.                                                                                        Models.
                                                                                             [17] David Delahaye. 2000. A Tactic Language for the System Coq. In Logic for Pro-
   Currently, because automated theorem provers in interactive                                    gramming and Automated Reasoning, 7th International Conference, LPAR 2000,
theorem assistants do not support user-defined tactics, the mined                                 Reunion Island, France, November 11-12, 2000, Proceedings (Lecture Notes in Com-
                                                                                                  puter Science, Vol. 1955), Michel Parigot and Andrei Voronkov (Eds.). Springer,
tactics can only be used externally to the symbolic prover. But                                   85–95. doi:10.1007/3-540-44404-1_7
this way cannot be deeply integrated into the automated proving                              [18] Jian Fang, Yican Sun, and Yingfei Xiong. 2025. Proof Strategy Extraction from
processes of the symbolic solvers. How to integrate mined tactics                                 LLMs for Enhancing Symbolic Provers. arXiv:2510.10131 [cs.LO] https://arxiv.
                                                                                                  org/abs/2510.10131
into the automated proving processes remains as future work.                                 [19] Emily First, Yuriy Brun, and Arjun Guha. 2020. TacTok: semantics-aware proof
                                                                                                  synthesis. Proc. ACM Program. Lang. 4, OOPSLA (2020), 231:1–231:31. doi:10.
                                                                                                  1145/3428299
References                                                                                   [20] Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan (Newman) Wu, Jieung Kim,
 [1] Anthropic. 2025. Claude Code: An agentic coding tool. https://code.claude.com/.              Vilhelm Sjöberg, and David Costanzo. 2016. CertiKOS: An Extensible Architec-
 [2] Anthropic. 2026. Introducing Claude Sonnet 4.6. https://www.anthropic.com/                   ture for Building Certified Concurrent OS Kernels. In 12th USENIX Symposium
     news/claude-sonnet-4-6.                                                                      on Operating Systems Design and Implementation, OSDI 2016, Savannah, GA,
 [3] Andrew W. Appel. 2024. Verified Functional Algorithms. Software Foundations,                 USA, November 2-4, 2016, Kimberly Keeton and Timothy Roscoe (Eds.). USENIX
     Vol. 3. Electronic textbook.                                                                 Association, 653–669. https://www.usenix.org/conference/osdi16/technical-
 [4] Haniel Barbosa, Clark W. Barrett, Martin Brain, Gereon Kremer, Hanna Lachnitt,               sessions/presentation/gu
     Makai Mann, Abdalrhman Mohamed, Mudathir Mohamed, Aina Niemetz, Andres                  [21] Albert Q. Jiang, Wenda Li, Szymon Tworkowski, Konrad Czechowski, Tomasz
     Nötzli, Alex Ozdemir, Mathias Preiner, Andrew Reynolds, Ying Sheng, Cesare                   Odrzygóźdź, Piotr Miłoś, Yuhuai Wu, and Mateja Jamnik. 2022. Thor: Wielding
     Tinelli, and Yoni Zohar. 2022. cvc5: A Versatile and Industrial-Strength SMT                 Hammers to Integrate Language Models and Automated Theorem Provers. CoRR
     Solver. In Tools and Algorithms for the Construction and Analysis of Systems -               abs/2205.10893 (2022). doi:10.48550/arXiv.2205.10893
     28th International Conference, TACAS 2022, Held as Part of the European Joint           [22] Saketh Ram Kasibatla, Arpan Agarwal, Yuriy Brun, Sorin Lerner, Talia Ringer,
     Conferences on Theory and Practice of Software, ETAPS 2022, Munich, Germany,                 and Emily First. 2024. Cobblestone: Iterative Automation for Formal Verification.
     April 2-7, 2022, Proceedings, Part I (Lecture Notes in Computer Science, Vol. 13243),        CoRR abs/2410.19940 (2024). arXiv:2410.19940 doi:10.48550/ARXIV.2410.19940
     Dana Fisman and Grigore Rosu (Eds.). Springer, 415–442. doi:10.1007/978-3-030-          [23] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David A. Cock,
     99524-9_24                                                                                   Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt, Rafal Kolanski, Michael
 [5] Yves Bertot and Pierre Castéran. 2013. Interactive theorem proving and program               Norrish, Thomas Sewell, Harvey Tuch, and Simon Winwood. 2009. seL4: formal
     development: Coq’Art: the calculus of inductive constructions. Springer Science &            verification of an OS kernel.. In Proceedings of the 22nd ACM Symposium on
     Business Media.                                                                              Operating Systems Principles 2009, SOSP 2009, Big Sky, Montana, USA, October 11-
 [6] Lasse Blaauwbroek, Mirek Olsák, Jason Rute, Fidel Ivan Schaposnik Massolo,                   14, 2009, Jeanna Neefe Matthews and Thomas E. Anderson (Eds.). ACM, 207–220.
     Jelle Piepenbrock, and Vasily Pestun. 2024. Graph2Tac: Online Representation                 doi:10.1145/1629575.1629596
     Learning of Formal Math Concepts. In Forty-first International Conference on            [24] Andrei Kozyrev, Nikita Khramov, Gleb Solovev, and Anton Podkopaev. 2026.
     Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024. OpenReview.net.              RocqStar: Leveraging Similarity-driven Retrieval and Agentic Systems for Rocq
     https://openreview.net/forum?id=A7CtiozznN                                                   generation. arXiv:2505.22846 [cs.LG] https://arxiv.org/abs/2505.22846
 [7] Lasse Blaauwbroek, Josef Urban, and Herman Geuvers. 2020. Tactic Learning and           [25] Robbert Krebbers, Xavier Leroy, and Freek Wiedijk. 2014. Formal C Semantics:
     Proving for the Coq Proof Assistant. In LPAR 2020: 23rd International Conference             CompCert and the C Standard. In Interactive Theorem Proving - 5th International
     on Logic for Programming, Artificial Intelligence and Reasoning, Alicante, Spain,            Conference, ITP 2014, Held as Part of the Vienna Summer of Logic, VSL 2014, Vienna,
     May 22-27, 2020 (EPiC Series in Computing, Vol. 73), Elvira Albert and Laura                 Austria, July 14-17, 2014. Proceedings (Lecture Notes in Computer Science, Vol. 8558),
     Kovács (Eds.). EasyChair, 138–150. doi:10.29007/WG1Q                                         Gerwin Klein and Ruben Gamboa (Eds.). Springer, 543–548. doi:10.1007/978-3-
 [8] Sascha Böhme and Tobias Nipkow. 2010. Sledgehammer: Judgement Day. In                        319-08970-6_36
     Automated Reasoning, 5th International Joint Conference, IJCAR 2010, Edinburgh,         [26] Xavier Leroy, Sandrine Blazy, Daniel Kästner, Bernhard Schommer, Markus Pister,
     UK, July 16-19, 2010. Proceedings (Lecture Notes in Computer Science, Vol. 6173),            and Christian Ferdinand. 2016. CompCert – A Formally Verified Optimizing
     Jürgen Giesl and Reiner Hähnle (Eds.). Springer, 107–121. doi:10.1007/978-3-642-             Compiler. In ERTS 2016: Embedded Real Time Software and Systems. SEE. http:
     14203-1_9                                                                                    //xavierleroy.org/publi/erts2016_compcert.pdf
 [9] Venanzio Capretta. 2005. General recursion via coinductive types. Log. Methods          [27] Minghai Lu, Benjamin Delaware, and Tianyi Zhang. 2024. Proof Automation
     Comput. Sci. 1, 2 (2005). doi:10.2168/LMCS-1(2:1)2005                                        with Large Language Models. In Proceedings of the 39th IEEE/ACM International
[10] Brigitte Chauvin, Philippe Flajolet, Danièle Gardy, and Bernhard Gittenberger.               Conference on Automated Software Engineering, ASE 2024, Sacramento, CA, USA,
     2004. And/Or Trees Revisited. Comb. Probab. Comput. 13, 4-5 (2004), 475–497.                 October 27 - November 1, 2024, Vladimir Filkov, Baishakhi Ray, and Minghui Zhou
     doi:10.1017/S0963548304006273                                                                (Eds.). ACM, 1509–1520. doi:10.1145/3691620.3695521
[11] Yizhou Chen, Zeyu Sun, Guoqing Wang, and Dan Hao. 2025. Gpass: A Goal-                  [28] Linhao Luo, Jiaxin Ju, Bo Xiong, Yuan-Fang Li, Gholamreza Haffari, and Shirui Pan.
     Adaptive Neural Theorem Prover Based on Coq for Automated Formal Verifica-                   2025. ChatRule: Mining Logical Rules with Large Language Models for Knowledge
     tion. In 47th IEEE/ACM International Conference on Software Engineering, ICSE                Graph Reasoning. In Advances in Knowledge Discovery and Data Mining - 29th
     2025, Ottawa, ON, Canada, April 26 - May 6, 2025. IEEE, 29–41. doi:10.1109/                  Pacific-Asia Conference on Knowledge Discovery and Data Mining, PAKDD 2025,
     ICSE55347.2025.00116                                                                         Sydney, NSW, Australia, June 10-13, 2025, Proceedings, Part II (Lecture Notes in
[12] Luís Cruz-Filipe, Herman Geuvers, and Freek Wiedijk. 2004. C-CoRN, the Con-                  Computer Science, Vol. 15871), Xintao Wu, Myra Spiliopoulou, Can Wang, Vipin
     structive Coq Repository at Nijmegen. In Mathematical Knowledge Manage-                      Kumar, Longbing Cao, Yanqiu Wu, Yu Yao, and Zhangkai Wu (Eds.). Springer,
     ment, Third International Conference, MKM 2004, Bialowieza, Poland, Septem-                  314–325. doi:10.1007/978-981-96-8173-0_25
     ber 19-21, 2004, Proceedings (Lecture Notes in Computer Science, Vol. 3119), An-        [29] Gregory Malecha, Gregory Malecha, and Yishuai Li. 2024. coq-ext-lib. https:
     drea Asperti, Grzegorz Bancerek, and Andrzej Trybulec (Eds.). Springer, 88–103.              //github.com/rocq-community/coq-ext-lib
     doi:10.1007/978-3-540-27818-4_7                                                         [30] OpenAI. 2025. Introducing GPT-5.2.
[13] Lukasz Czajka and Cezary Kaliszyk. 2018. Hammer for Coq: Automation for                 [31] Zoe Paraskevopoulou. 2026. Machine-Generated, Machine-Checked Proofs for a
     Dependent Type Theory. J. Autom. Reason. 61, 1-4 (2018), 423–453. doi:10.1007/               Verified Compiler (Experience Report). arXiv:2602.20082 [cs.PL] https://arxiv.
     S10817-018-9458-4                                                                            org/abs/2602.20082
[14] Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 Theorem Prover and            [32] Christine Paulin-Mohring. 2015. Introduction to the calculus of inductive con-
     Programming Language. In Automated Deduction - CADE 28 - 28th International                  structions. All about Proofs, Proofs for All 55 (2015).
     Conference on Automated Deduction, Virtual Event, July 12-15, 2021, Proceedings         [33] Yicheng Qian, Joshua Clune, Clark Barrett, and Jeremy Avigad. 2025. Lean-
     (Lecture Notes in Computer Science, Vol. 12699), André Platzer and Geoff Sutcliffe           auto: An Interface between Lean 4 and Automated Theorem Provers.
     (Eds.). Springer, 625–635. doi:10.1007/978-3-030-79876-5_37                                  arXiv:2505.14929 [cs.LO] https://arxiv.org/abs/2505.14929
[15] Leonardo Mendonça de Moura and Nikolaj S. Bjørner. 2008. Z3: An Efficient               [34] Stephen E. Robertson and Hugo Zaragoza. 2009. The Probabilistic Relevance
     SMT Solver. In Tools and Algorithms for the Construction and Analysis of Systems,            Framework: BM25 and Beyond. Found. Trends Inf. Retr. 3, 4 (2009), 333–389.
     14th International Conference, TACAS 2008, Held as Part of the Joint European                doi:10.1561/1500000019
     Conferences on Theory and Practice of Software, ETAPS 2008, Budapest, Hungary,          [35] Alex Sanchez-Stern, Yousef Alhessi, Lawrence K. Saul, and Sorin Lerner. 2020.
     March 29-April 6, 2008. Proceedings (Lecture Notes in Computer Science, Vol. 4963),          Generating correctness proofs with neural networks. In Proceedings of the 4th
     C. R. Ramakrishnan and Jakob Rehof (Eds.). Springer, 337–340. doi:10.1007/978-               ACM SIGPLAN International Workshop on Machine Learning and Programming
     3-540-78800-3_24                                                                             Languages, MAPL@PLDI 2020, London, UK, June 15, 2020, Koushik Sen and Mayur
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                                                Jian Fang, Yixun Yao, and Yingfei XiongB


     Naik (Eds.). ACM, 1–10. doi:10.1145/3394450.3397466                                     [41] Haiming Wang, Huajian Xin, Chuanyang Zheng, Zhengying Liu, Qingxing Cao,
[36] Parshin Shojaee, Kazem Meidani, Shashank Gupta, Amir Barati Farimani, and                    Yinya Huang, Jing Xiong, Han Shi, Enze Xie, Jian Yin, Zhenguo Li, and Xiaodan
     Chandan K. Reddy. 2025. LLM-SR: Scientific Equation Discovery via Program-                   Liang. 2024. LEGO-Prover: Neural Theorem Proving with Growing Libraries.
     ming with Large Language Models. In The Thirteenth International Conference on               In The Twelfth International Conference on Learning Representations, ICLR 2024,
     Learning Representations, ICLR 2025, Singapore, April 24-28, 2025. OpenReview.net.           Vienna, Austria, May 7-11, 2024. OpenReview.net. https://openreview.net/forum?
     https://openreview.net/forum?id=m2nmp8P5in                                                   id=3f5PALef5B
[37] Yuheng Su, Qiusong Yang, Yiwei Ci, Tianjun Bu, and Ziyu Huang. 2025. The rIC3           [42] Yile Wang, Sijie Cheng, Zixin Sun, Peng Li, and Yang Liu. 2024. Speak It Out:
     Hardware Model Checker. In Computer Aided Verification - 37th International                  Solving Symbol-Related Problems with Symbol-to-Language Conversion for
     Conference, CAV 2025, Zagreb, Croatia, July 23-25, 2025, Proceedings, Part I (Lecture        Language Models. arXiv:2401.11725 [cs.CL] https://arxiv.org/abs/2401.11725
     Notes in Computer Science, Vol. 15931), Ruzica Piskac and Zvonimir Rakamaric            [43] Makarius Wenzel, Lawrence C. Paulson, and Tobias Nipkow. 2008. The Isabelle
     (Eds.). Springer, 185–199. doi:10.1007/978-3-031-98668-0_9                                   Framework. In Theorem Proving in Higher Order Logics, 21st International Confer-
[38] Yuheng Su, Qiusong Yang, Yiwei Ci, Yingcheng Li, Tianjun Bu, and Ziyu Huang.                 ence, TPHOLs 2008, Montreal, Canada, August 18-21, 2008. Proceedings (Lecture
     2025. Deeply Optimizing the SAT Solver for the IC3 Algorithm. In Computer                    Notes in Computer Science, Vol. 5170), Otmane Aït Mohamed, César A. Muñoz,
     Aided Verification - 37th International Conference, CAV 2025, Zagreb, Croatia, July          and Sofiène Tahar (Eds.). Springer, 33–38. doi:10.1007/978-3-540-71067-7_7
     23-25, 2025, Proceedings, Part I (Lecture Notes in Computer Science, Vol. 15931),       [44] Yuhuai Wu, Albert Q. Jiang, Wenda Li, Markus N. Rabe, Charles Staats, Mateja
     Ruzica Piskac and Zvonimir Rakamaric (Eds.). Springer, 237–257. doi:10.1007/978-             Jamnik, and Christian Szegedy. 2022. Autoformalization with Large Language
     3-031-98668-0_12                                                                             Models. arXiv:2205.12615 [cs.LG] https://arxiv.org/abs/2205.12615
[39] The Coq Development Team. 2024. The Coq Reference Manual – Release 8.20.0.              [45] Kaiyu Yang and Jia Deng. 2019. Learning to Prove Theorems via Interacting with
     https://rocq-prover.org/doc/V8.20.0/refman/index.html                                        Proof Assistants. In Proceedings of the 36th International Conference on Machine
[40] Kyle Thompson, Nuno Saavedra, Pedro Carrott, Kevin Fisher, Alex Sanchez-                     Learning, ICML 2019, 9-15 June 2019, Long Beach, California, USA (Proceedings of
     Stern, Yuriy Brun, João F. Ferreira, Sorin Lerner, and Emily First. 2025. Rango:             Machine Learning Research, Vol. 97), Kamalika Chaudhuri and Ruslan Salakhutdi-
     Adaptive Retrieval-Augmented Proving for Automated Software Verification.                    nov (Eds.). PMLR, 6984–6994. http://proceedings.mlr.press/v97/yang19a.html
     In 47th IEEE/ACM International Conference on Software Engineering, ICSE 2025,           [46] Bowen Zhang and Harold Soh. 2024. Extract, Define, Canonicalize: An LLM-
     Ottawa, ON, Canada, April 26 - May 6, 2025. IEEE, 347–359. doi:10.1109/ICSE55347.            based Framework for Knowledge Graph Construction. arXiv:2404.03868 [cs.CL]
     2025.00161                                                                                   https://arxiv.org/abs/2404.03868
