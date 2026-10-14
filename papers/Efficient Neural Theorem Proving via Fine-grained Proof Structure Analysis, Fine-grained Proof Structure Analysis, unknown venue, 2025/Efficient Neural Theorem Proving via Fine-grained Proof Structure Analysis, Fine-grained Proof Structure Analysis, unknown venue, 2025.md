                                                                ProofAug: Efficient Neural Theorem Proving via
                                                                     Fine-grained Proof Structure Analysis


                                                                   Haoxiong Liu 1 Jiacheng Sun 2 Zhenguo Li 2 Andrew C Yao 1 3


                                                                Abstract                                   1. Introduction
                                             The synergy between deep learning models and                  Automated theorem proving is a field that not only appeals
                                             traditional automation tools, such as built-in tac-           to mathematicians looking for efficient formalization and
arXiv:2501.18310v2 [cs.LG] 6 Jun 2025




                                             tics of the proof assistant and off-the-shelf auto-           proof automation for mathematical theorems, but also finds
                                             mated theorem provers, plays a crucial role in                significant applications in real-world industries such as inte-
                                             developing robust and efficient neural theorem                grated circuit design and software engineering (Bibel, 2013;
                                             provers (NTPs). However, for proof synthesis                  Schumann, 2013). Early applications of machine learn-
                                             with LLMs, previous work applies automation                   ing methods on automated theorem proving focus on tasks
                                             tools either only when explicitly invoked by the              such as premise selection (Irving et al., 2016) and proof
                                             model or at a single granularity level, failing to            search (Loos et al., 2017) in SMT solvers or resolution/-
                                             fully exploit their power. To solve this issue, we            superposition provers, often interleaved with handcrafted
                                             propose ProofAug, a procedure that equips LLMs                heuristics. Recently, rapid progress in mathematical rea-
                                             with automation methods at various granularities              soning with large language models (LLMs) has awoken a
                                             through fine-grained structure analysis of model-             flourishing interest for directly synthesizing formal proofs
                                             generated proof proposals. ProofAug also serves               using generative language models.
                                             as a versatile plug-and-play module that seam-
                                                                                                           In literature, there are primarily two paradigms for direct
                                             lessly integrates with any tree-search algorithm,
                                                                                                           proof synthesis: the proof-step generation paradigm and
                                             enabling our construction of an efficient recursive
                                                                                                           the whole-proof generation paradigm, each corresponding
                                             proving (ERP) module to further enhance perfor-
                                                                                                           to a distinct proof style. For proof assistants where proofs
                                             mance. The superiority of our method is validated
                                                                                                           are mainly in the procedural style (or tactic-style), such as
                                             on the miniF2F benchmark using the open-source
                                                                                                           MetaMath (Megill & Wheeler, 2019) and HOL Light (Harri-
                                             deepseek-math-7b-base model and the Isabelle
                                                                                                           son, 2009), previous work adopts the proof-step generation
                                             proof assistant. Notably, by additionally employ-
                                                                                                           paradigm (Polu & Sutskever, 2020; Lample et al., 2022; Han
                                             ing a mixed prompting strategy, we achieve a
                                                                                                           et al., 2022; Polu et al., 2022), where in each iteration the
                                             cumulative pass rate of 66.0% after curation of
                                                                                                           model is requested to generate one tactic to be applied in the
                                             the dataset (61.9% for the original version) with
                                                                                                           interactive theorem prover (ITP)1 . Then the ITP provides
                                             at most 2100 queries to the model per problem (In
                                                                                                           information on the updated proof state, which sometimes
                                             contrast, the previous SOTA in Isabelle, Subgoal-
                                                                                                           could be indispensable for people to finish the remaining
                                             XL (Zhao et al., 2024), only achieves 56.1% us-
                                                                                                           proof. Proof-step generation methods typically use tree-
                                             ing 16384 queries per problem). We also imple-
                                                                                                           search algorithms to guide the proof process, inspired by
                                             ment a Lean 4 version of ProofAug that can im-
                                                                                                           the success of AlphaGo (Silver et al., 2016). In contrast, for
                                             prove the pass@1 performance of Kimina-Prover-
                                                                                                           proof systems where declarative style proofs are common,
                                             Preview-Distill-1.5B from 44.3% to 50.4% on
                                                                                                           such as Isabelle and Lean 4, computation-efficient whole-
                                             miniF2F-test. Our code is available at https://
                                                                                                           proof generation methods become possible. However, the
                                             github.com/haoxiongliu/ProofAug.
                                                                                                           efficiency in this paradigm is not free. Any incorrect appli-
                                             1
                                               Institute for Interdisciplinary Information Sci-            cation of a proof method that bridges the gap between two
                                        ences, Tsinghua University 2 Huawei Noah’s Ark Lab                 proof terms (or goals/conjectures) will cause the proof to
                                        3
                                          Shanghai Qi Zhi Institute.   Correspondence to: Haox-            fail to pass the ITP verification check.
                                        iong Liu <liuhx20@mails.tsinghua.edu.cn>, Zhenguo Li
                                        <li.zhenguo@huawei.com>.                                               1
                                                                                                                 We use the terms ‘interactive theorem prover’ and ‘proof
                                                                                                           assistant’ interchangeably with a nuance: the former emphasizes
                                        Proceedings of the 42 nd International Conference on Machine       the formal system aspects, while the latter highlights its role in
                                        Learning, Vancouver, Canada. PMLR 267, 2025. Copyright 2025        assisting users.
                                        by the author(s).

                                                                                                       1
                     ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis

To avoid this issue, the Draft, Sketch, and Prove (DSP)                   issue in the first place. For the generated proof proposal,
framework (Jiang et al., 2023) proposes to let the model                  we first find its corresponding maximal compatible semi-
first write a formal proof sketch (Wiedijk, 2004) according               proof (MCSP) that maintains most structural information
to an informal proof draft, then offload the proofs of in-                yet can pass the check of ITP. Then, departing from it, we
termediate conjectures to off-the-shelf ATPs2 and heuristic               recursively resort to a more coarse semi-proof whenever
proof methods. Many subsequent works (Wang et al., 2023a;                 ATPs fail to fill in some gap in the current one. This proce-
Zhao et al., 2023; Zheng et al., 2024; Zhao et al., 2024) also            dure solves the ‘Complicated Draft’ issue, thus significantly
follow the practice of DSP when designing their few-shot                  improving the sample efficiency. We call this procedure
prompts: The proof methods in the original proofs of the                  ProofAug. Figure 1 shows an example flow of our method.
demonstration examples are replaced with a placeholder,
                                                                          We also demonstrate that the application of proof structure
which signifies that ATPs are responsible for completing
                                                                          analysis is not restricted to single-pass generation. In fact,
the task. We observe that while this approach can signifi-
                                                                          ProofAug can be incorporated into any tree-search algorithm
cantly enhance performance compared to direct full-proof
                                                                          to expand the candidate node set at each iteration. This will
generation, it may also result in proof failures in unintended
                                                                          become evident in our unified view of theorem proving
ways:
                                                                          introduced in Section 2.1. In Section 3.3, we illustrate
   • (Hard Conjectures) In DSP, the in-context learning                   its application in constructing a sample-efficient recursive
     ability of LLMs makes them follow the style of the                   proving (Wang et al., 2024) module on top of ProofAug.
     few-shot prompt to generate rough sketches according
                                                                          We list our contributions with corresponding key evalua-
     to the informal proof, refusing to dive into the neces-
                                                                          tion results below. All experiments use the open-source
     sary details. As a result, the generated intermediate
                                                                          deepseek-math-7b-base model (Shao et al., 2024) if not
     conjectures could be too hard for ATPs to solve.
                                                                          otherwise specified.
   • (Complicated Draft) Due to common inconsistencies
     between informal proof and formal system, there are                     • We propose a versatile plug-and-play procedure
     conjectures that despite being easy to be solved by                       ProofAug that can significantly enhance the perfor-
     ATPs, humans need to write complicated informal                           mance of neural theorem provers, based on fine-grained
     proofs for them. The unnecessary intermediate steps                       proof structure analysis. On miniF2F-test5 (Zheng
     could be translated into formal conjectures that are in-                  et al., 2021), ProofAug achieves a pass rate of 52.5%
     appropriate in syntax or even harder than the original                    with no more than 100 queries to the model. Abla-
     theorem.                                                                  tion results show that when compared with the DSP
                                                                               baseline, the improvement brought by ProofAug imple-
Here, a dilemma appears. On one hand, instructing the                          mentation for Isabelle is 7.8%, 4.1% and 3.3% under
model to produce a rough sketch increases the risk of miss-                    sample budgets of 1, 10 and 100, respectively.
ing critical details, making it challenging for ATPs to bridge
                                                                             • ProofAug can be incorporated into any tree-search al-
the gaps. On the other hand, directing the model to gener-
                                                                               gorithms under our unified view of existing genera-
ate highly detailed sketches can exacerbate formalization
                                                                               tive LM based theorem proving methods. We show-
issues.3 Neither way is ideal for fully leveraging the power
                                                                               case that when integrated with our Efficient Recursive
of off-the-shelf automation methods.
                                                                               Proving (ERP) module, 0-shot ProofAug performance
In this paper, we propose to address this dilemma through                      improves from 54.5% to 56.1% with a limit of 500
performing fine-grained structural analysis on the proof                       queries per problem. For comparison, RMaxTS (Xin
proposals generated by LLMs, based on the observation                          et al., 2024b) only shows an advantage of < 0.2% over
that regardless of correctness, full proofs contain rich struc-                naive single-pass retrying under a sample budget of
tural information from which valid semi-proofs4 of varying                     3200.
granularities can be derived. Specifically, given a theorem                  • Moreover, using a mixture of strategies with different
statement, instead of instructing the model to generate a                      prompting methods, we achieve a total pass rate of
proof sketch as previous work does, we choose to start from                    61.9% within 1700 model queries. After curating the
generating a full proof to suppress the ‘Hard Conjectures’                     miniF2F-test data, we manage to prove 66.0% of the
    2                                                                          theorems with no more than 2100 requests, setting a
      For simplicity, we follow the practice of Jiang et al. (2023)
to use the abbreviation ATP to refer to any automated method,                  new state-of-the-art across methods using the Isabelle
including SMT solvers and what traditionally known as automated                proof assistant.
theorem provers.                                                             • We also build a Lean implementation of ProofAug and
    3
      We refer the readers to Appendix B for two concrete examples
that illustrate these two issues.                                            5
                                                                               We use ‘miniF2F-test’ to refer to the miniF2F test split Isabelle
    4
      By semi-proofs, we refer to proofs that possibly contain sym-       data included in the code repository of Jiang et al. (2023). See
bols indicating pending proof, such as sorry in Isabelle and Lean.        Section 4.1 for a detailed discussion on the versions of miniF2F.

                                                                      2
                      ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis




Figure 1: Illustration example of ProofAug. Each box in the flowchart corresponds to a proof step. (a) The initial proof
encounters an error when proving Conjecture 1-0. (b) We replace the original proof of Conjecture 1-0 with a sorry and
continue, until a syntactic error occurs at Conjecture 1-1. (c) The proof of Conjecture 1 is replaced by sorry and we obtain
a semi-proof with two sorrys. (d) Automation tools are called to prove Conjecture 0 and Conjecture 1, but failing at the
latter one. (e) The ERP module (introduced in Section 3.3) sends a completion request at Conjecture 1. (f) The generated
ERP proof still fails at Conjecture 1. (g) We finally resort to a more coarse level of proof and successfully find a proof with
automation tools. Refer to Algorithm 2 for a pseudo-code description of ProofAug.


       shows that the pass@1 accuracy of Kimina-Prover-                        • T : S × A → S is the state transition function of the
       Preview-Distill-1.5B on miniF2F-test can be improved                      ITP.
       from 44.3% to 50.4%, exhibiting the generality of
                                                                            For any string x ∈ Σ∗ , we use sx to denote T (s0 , x), where
       ProofAug for various proof systems.
                                                                            we have lifted the notation T to express consecutive state
                                                                            transitions, i.e., for s ∈ S,
2. Preliminaries
                                                                            T (s, x) := T (·, a[n]) ◦ T (·, a[n − 1]) ◦ · · · ◦ T (·, a[1])(s)
2.1. A Unified View of Theorem Proving with
     Generative Language Models                                             if Parse(x) = (a[1], a[2], · · · , a[n]).
We first formulate the task of theorem proving in the context               Given a theorem statement (with context) xf ∈ Σ∗ , we say
of language modeling and introduce our notations. We                        yf ∈ Σ∗ is a proof of xf if sxf ∥yf .finish = True, where ∥
assume there is a global alphabet Σ. An ITP is formulated                   denotes the concatenation of two strings. A generative lan-
as a triple (A, S, T ), where:                                              guage model (with a decoding strategy) is a map that outputs
   • A ⊂ Σ∗6 is the set of proof steps. There is also a                     a distribution π(·|x) on Σ∗ when conditioned on a prompt
     parser Parse : Σ∗ → A∗ that transforms a string into                   x ∈ Σ∗ . A response is a sample y ∼ π(·|x). The task of
     a sequence of proof steps.                                             theorem proving is to find a proof yf of the given theorem
                                                                            statement xf using the black-box distribution generator π.
   • S is the set of states. A state s ∈ S represents our ab-
                                                                            Some benchmarks also provide a corresponding informal
     straction of the proof object underlying the ITP, which
                                                                            statement xi and informal proof yi for each theorem.
     contains all information the ITP needs to proceed with
     the proof, including s.state, s.error, s.finish, etc.,                 We state our unified view of existing generative-LM-based
     varying depending on the specific ITP environment.                     theorem proving methods as follows. In each round, an
     Additionally, there is a special element s0 , which rep-               algorithm completes three steps:
     resents the initial state.
                                                                              1. (State Selection) Select a state to work with in this
   6
    A∗ denotes the set of all finite lists (or sequences) of elements            round.
from A, including the empty list.
                                                                              2. (Prompt Formation) Form a prompt and present it to

                                                                        3
                   ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis

Table 1: A summary of current theorem proving methods using generative language modeling under our unified view,
including DSP (Jiang et al., 2023), LEGO-Prover (Wang et al., 2023a), Lyra (Zheng et al., 2024), GPT-f (Polu & Sutskever,
2020), HTPS (Lample et al., 2022), ReProver (Yang et al., 2023), Lean-STaR (Lin et al., 2024), POETRY (Wang et al.,
2024), RMaxTS (Xin et al., 2024b). We use the terms node and state interchangeably.

 Method           State Selection       Prompt Components                 Expected Output                  Response Processing
 Single-pass generation methods
 Naive              Always sxf                    xf                       a full proof                   verify the proof in ITP
 DSP                Always sxf           xf + informal draft              proof sketch                   call ATPs to fill the gaps
 LEGO               Always sxf            xf + draft + skills     skill comple. + proof sketch       call ATPs + update skill library
 Lyra               Always sxf          xf + last attempt error           proof sketch                 tool correction + call ATPs
 Proof-step generation methods
 GPT-f          max logprob goal          the selected goal                     a tactic             expand the goal-based search tree
 HTPS          max PUCT value goal        the selected goal                     a tactic            expand and backprop the hypertree
 ReProver       max logprob state       retrieved prem. + ps                    a tactic             expand the state-based search tree
 Lean-STaR         current state              proof state             a proof step with rationale         proceed the step in ITP
 POETRY         max logprob state       context + proof state         a proof step (with ‘sorry’)      update the recursive proof tree
 RMaxTS          discounted UCB         context + proof state              proof completion         add a new node for each valid step
 Ours
 ProofAug           Always sxf           xf + informal draft                 a full proof           FindMCSP + Proof Augmentation
 + ERP          the first ATP failure   context + proof state         a proof of this conjecture       + new nodes for each block



     the model.                                                            theorem "((A −→ B) −→ A) −→ A"
  3. (Response Processing) Use the response of the model                   proof
     to interact with ITP to generate new states.                            assume "(A −→ B) −→ A"
                                                                             show A
Compared to typical views of tree-search algorithms, our ap-                 proof (rule classical)
proach integrates their expansion step and back-propagation                    assume "¬ A"
step with the process of interacting with the ITP into a sin-                  have "A −→ B"
                                                                               proof
gle response processing module. We isolate the prompt                            assume A
formation procedure into a single module to emphasize its                        with ⟨¬ A⟩ show B by contradiction
importance, as proof-step generation methods and whole-                        qed
proof generation methods differ fundamentally at this point.                   with ⟨(A −→ B) −→ A⟩ show A ..
Besides, this allows us to place not only these two lines of                 qed
                                                                           qed
work, but also methods that lie in between, under our unified
view.
Table 1 summarizes and compares different methods under                Figure 2: An example proof in Isar with hierarchical
this view. Our view disentangles the different modules of              proof...qed block structures.
algorithm design, naturally motivating us to optimize exist-
ing algorithms in the module-level. Our method ProofAug,               and demonstrate its superiority.
which will be introduced in Section 3.2, is a procedure
belonging to the response processing step. Thus, we can                2.2. The Isabelle/Isar Proof Language
integrate effective practices in other modules with ProofAug
                                                                       Although the basic idea of our method in general fits any
to make further improvements. We showcase such an ap-
                                                                       ITP, the implementation details vary depending on specific
plication in Section 3.3. Moreover, since the goal of theo-
                                                                       features of the proof assistant. In this paper, we use Is-
rem proving is to improve the overall pass rate rather than
                                                                       abelle/Isar (Wenzel et al., 2004) as an example to introduce
the success rate of each attempt, an appropriate ‘portfolio’
                                                                       the spirit of ProofAug and how to implement it in a spe-
of different strategies for each module could significantly
                                                                       cific proof system.7 In this section, we introduce some basic
improve the pass rate than a single strategy. Such a phe-
                                                                       knowledge and unique features that ease the implementation
nomenon has been observed in the CoT & non-CoT mode
                                                                           7
combination (Xin et al., 2024b; Zhao et al., 2024). In Sec-                 See Appendix C for a detailed explanation of why our method
tion 4.4, we explore this idea across additional combinations          is generic across different systems and a brief summary of our
                                                                       Lean implementation.

                                                                  4
                     ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis

of our method in Isar.                                                  Algorithm 1 Find the Maximal Compatible Semi-Proof
The specific object corresponding to our ‘state’ abstrac-                 Input: initial proof yf0 , ITP (A, S, T )
tion formulated in Section 2.1 is Isar/VM transition. The                 a ← Parse(yf0 )
transitions are typed with different modes, including                     s ← [Null] × len(a)                ▷ States before each step
proof(prove), proof(state) and proof(chain). We find that                 i, sthis ← 1, s0
identifying the mode proof(prove) is particularly useful for              while i ≤ len(a) do
the analysis of proof structure since it indicates that a goal               s[i] ← sthis
has just been declared and the next proof step is required                   snext ← T (sthis , a[i])
to contain a proof method. In Isar, proof methods are only                   if snext .error then
allowed to be invoked after the keywords proof and qed. As                      if sthis .mode = proof(prove) then
a result, a typical proof in Isar is organized by hierarchical                      a[i] ← sorry
proof...qed blocks.                                                             else           ▷ Error in other modes, skip the block
                                                                                    block ← InnermostBlock(i, a)
Figure 2 shows an example of Isar proof. Users are allowed
                                                                                    if block is Null then
to have or show are keywords that Isabelle allows to appear
                                                                                       return Null ▷ a[i] not in any block, terminate
in the proof(state) mode to introduce new local goals. To
                                                                                    end if
prove a goal with some proof method m, one can use a
                                                                                    a[block.start..(block.end − 1)] ← Null
single clause ‘by m’, which is an abbreviation of ‘proof m
                                                                                    a[block.end] ← sorry
qed’. The other keywords, assume and with, serve exactly
                                                                                    i, sthis ← block.end, s[block.start]
the same purpose as they do when used in natural language
                                                                                end if
proofs. Benefiting from the above properties, Isar proofs are
                                                                             else
readable even for people unfamiliar with Isabelle, thus easy
                                                                                i, sthis ← i + 1, snext
to be analyzed just like how we analyze the structure of an
                                                                             end if
informal proof.
                                                                          end while
Finally, we specify the attributes we can access from a state             if sthis .f inish then
s through the ITP environment used in this work. We can                      return Concat(a)
have a proof state string s.state that corresponds to the                 end if
‘proof state’ Isabelle shows to the user, a corresponding
mode s.mode, a list of all available facts s.facts that can
be obtained by the print facts command in Isabelle, and
two boolean-type attributes s.error and s.finish indicating
whether ‘an error has occurred’ and whether ‘a theorem
is proved’, respectively. We say s1 = s2 for two states
s1 , s2 ∈ S if all the values of these five attributes are equal.       semi-proof y is compatible to yf0 if each sorry in y matches
                                                                        a proof...qed block or a by clause in yf0 and the remaining
3. Method                                                               parts are equal. Thus, by MCSP, we refer to the particular
                                                                        compatible semi-proof yfM from which all compatible semi-
Algorithm 2 describes our method, ProofAug. It mainly                   proofs (w.r.t. yf0 ) can be obtained by substituting some
consists of three parts: finding the Maximal Compatible                 proof...qed blocks or by clauses of yfM with sorrys.
Semi-Proof (MCSP), proof augmentation, and an optional
Efficient Recursive Proving (ERP) module. In this section,              The FindMCSP routine is described in Algorithm 1. Firstly,
we state each of them in detail. For an illustrative walk-              yf0 is parsed into a sequence of proof steps a. Then we
through example of ProofAug, refer to Figure 1.                         create a pointer i indicating the current position and an
                                                                        array s indicating the states before the ith step. In each
3.1. Find the Maximal Compatible Semi-Proof                             iteration, we first try to proceed the current proof step a[i]
                                                                        from the current state s[i] in the ITP. If this step succeeds, we
Given a proof proposal yf0 sampled from π(·|p(xi ∥yi , xf ))            continue to the next proof step; otherwise, according to the
(where p(·, ·) is a few-shot/zero-shot prompter that ap-                proof mode of s[i], we take different strategies: if s[i].mode
propriately combines its arguments), the first procedure                is proof(prove), we replace a[i] with sorry; otherwise, we
of ProofAug is to find the Maximal Compatible Semi-                     find the innermost proof...qed block of yf0 that contains the
Proof (MCSP) of yf0 .                                                   i-th step and substitute the whole block with a single sorry
We first explain what the MCSP is. Recall that a semi-proof             step, then move the pointer accordingly. The algorithm
refers to a proof that possibly contains sorry steps. We say a          terminates when a failed step occurs outmost or all steps
                                                                        pass the check of the ITP.

                                                                    5
                    ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis

Algorithm 2 Proof Augmentation (ProofAug)                                we encounter a sorry step as we progress with the proof,
  Input: theorem statement xf , informal statement & draft               we try a predefined set of Isabelle built-in heuristic methods
  xi ∥yi , prompter p(·, ·), LM π(·|·), ITP (A, S, T )                   and Sledgehammer to find a proof of the current goal. This
  yf0 ∼ π(·|p(xi ∥yi , xf ))            ▷ Sample an initial proof        procedure can be seen as a special proof method <ATP>
  a ← Parse(FindMCSP(yf ))         0
                                            ▷ Apply Algorithm 1          created by us, similar to the built-in proof method try. If
  s ← [Null] × len(a)                                                    this <ATP> method fails, we can rule out the possibility
  i, sthis ← 1, s0                                                       that the final proof contains the innermost proof...qed block
  while i ≤ len(a) do                                                    in which this sorry lives and replace the block with sorry.
     snext ← T (sthis , a[i])                                            We iteratively perform this operation until we finish the
     if a[i] ̸= sorry then                                               proof, or the semi-proof degrades into a single sorry step
        error ← F alse                                                   and <ATP> fails to directly prove the original theorem.
     else                                                                For a concrete example of ProofAug inducing a proof from
        error ← T (sthis , <ATP>).error               ▷ Try ATPs         a failed initial proof proposal, refer to Appendix I.
     end if
     if error and useERP then                     ▷ ERP module           3.3. Efficient Recursive Proving
        yfp ← a[1..i − 1]∥sthis .state
        yfc ∼ π(·|p(xi ∥yi , xf ∥yfp ))                                  Solving a complicated theorem from a single proof proposal
        if T (sthis , yfc ) = snext then                                 generated by the language model π(·|·) is challenging even
            a[i], error ← yfc , F alse                                   with our ProofAug procedure. By simply sampling more
        else                                                             proof proposals, we can probably get better results as long as
            yfa ← FailedTactics2ATP(yfc )                                there is some randomness underlying the decoding strategy
            if T (sthis , yfa ) = snext then                             of π. We ask the question: how can we outperform this
               a[i], error ← yfa , F alse                                naive retrying strategy, given a fixed sample budget?
            end if                                                       On miniF2F, Wang et al. (2023a); Zheng et al. (2024)
        end if                                                           achieve better performance than the naive approach by mak-
     end if                                                              ing use of the previous error messages or proved lemmas in
     if error then                      ▷ Resort to the last level       the previous attempts of proofs. Nevertheless, these meth-
        block ← InnermostBlock(i, a)                                     ods all belong to the whole-proof generation paradigm and
        if block is Null then return Null                                benefit from the strong instruction-following ability of GPT-
        a[block.start..(block.end − 1)] ← Null                           series models. Here, we are more interested in going beyond
        a[block.end] ← sorry                                             whole-proof generation to investigate whether tree-search
        i, sthis ← block.end, s[block.start]                             methods used in the proof-step generation paradigm can
     else                                                                help improve the sample efficiency.
        i, sthis ← i + 1, snext
     end if                                                              To the best of the authors’ knowledge, RMaxTS(Xin et al.,
  end while                                                              2024b) is the only successful attempt to integrate some tree-
  return Concat(a)                             ▷ The final proof         search algorithm with whole-proof generation. However,
                                                                         the advantage of RMaxTS only becomes clear when the
                                                                         sample budget comes to 4 × 6400. Our explanation for this
                                                                         inefficiency is that, for proofs that deviate from the correct
3.2. Proof Augmentation                                                  paths at a very early stage, RMaxTS could spend much
                                                                         time in searching after the proof steps that have already
The goal of ProofAug is to determine whether there exists                misled the direction of proof. We argue that this can be
a compatible semi-proof that can be completed into a valid               largely avoided if we can first check whether the proof pro-
proof using ATPs or built-in heuristic proof methods to fill             posal forms a valid reasoning path. POETRY(Wang et al.,
the sorry gaps. Instead of first finding out all compatible              2024) is a top-down approach that satisfies this property
semi-proofs and trying them sequentially, we should design               through fine-tuning the model to never step into the next
a more efficient way that makes use of the overlap among                 proof level. However, POETRY falls in the proof-step gener-
these semi-proofs to avoid waste of computation resources                ation paradigm and requires fine-tuning the model to follow
spent on calling ATPs. The resulting proof augmentation                  their special proof-step generation strategy.
algorithm is shown in Algorithm 2 (Ignore the ERP module
for now).                                                                In order to achieve a more sample efficient and fine-tuning
                                                                         free recursive proving method, we design our algorithm
Specifically, we first parse the MCSP and create a pointer               in a modularized way under the unified view described in
and a corresponding state array as in Algorithm 1. When

                                                                     6
                    ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis

Section 2.1. Firstly, for the prompt design module that deter-         for each problem compared to the OpenAI miniF2F 9 . While
mines the expected output content, we borrow the proof com-            both versions contain many mistakes and various extents of
pletion module of RMaxTS to replace the proof-generation               inaccuracies in the formal statements, previous work (Wang
step of POETRY; then, for the response processing module,              et al., 2023a; Zheng et al., 2024; Wang et al., 2024; Zhao
we perform proof structure analysis as in the proof augmen-            et al., 2024) in general chooses to use this DSP-version
tation procedure and try <ATP> for the failed proof...qed              for a fair comparison between different methods. Thus, in
blocks or by clauses. A new node is added if the <ATP>                 order to show the superiority of our ProofAug, we first fol-
method fails to solve the corresponding conjecture. For the            low previous work to do experiments on the DSP-version
state selection strategy, we follow the best-first strategy, but       miniF2F-test.
the priority is modified from the cumulative log-probability
                                                                       However, as the performance of neural theorem provers
to the end position of the failed proof block, i.e., if one
                                                                       has significantly improved recently, the ratio of unprovable
node is an ancestor of another, we prioritize the descendant;
                                                                       theorems resulting from the mistakes to the total number
otherwise, we prioritize the one that appears first in the
                                                                       of statements that provers fail to provide proofs becomes
semi-proof.
                                                                       no longer ignorable, and is one of the possible reasons that
In practice, to simplify the algorithm and suppress the sam-           Isabelle-based provers have fallen behind Lean-based ones
pling cost wasted in low-level details, we only try <ATP>              on this cross-language benchmark. So, we build a curated
and add new nodes for failed conjectures belonging to                  dataset and part of our experiments are done on the curated
the original MCSP. Such simplifications make the above                 version.10
procedure become a plug-and-play ERP module over our
ProofAug, as shown in Algorithm 2. This coincidence can                4.2. Experimental Setup
be interpreted as that each conjecture naturally inherits one
proof try from the original proof proposal. In other words,            The Isabelle version we use is Isabelle2022. We use
the ProofAug without ERP module is already implicitly a                the PISA environment (Jiang et al., 2021) to inter-
recursive proving method, in the sense that each compatible            act with Isabelle. Our <ATP> method is the combi-
semi-proof exactly corresponds to one proof tree during the            nation of 8 Isabelle proof methods (auto, simp, auto,
search process of POETRY if the two methods share the                  blast, fastforce, eval, sos, arith, simp:field simps, simp
same final proof.                                                      add:mod simps) and Sledgehammer. Following Jiang et al.
                                                                       (2023), we set the timeout for any proof step and Sledge-
For an illustrative example of how the ERP module works                hammer as 10s and 120s, respectively. During verifica-
in ProofAug, one can refer to Figure 1.                                tion, we run 12 PISA instances in parallel on one In-
                                                                       tel(R) Xeon(R) Gold 6326 CPU @ 2.90GHz11 .
4. Experiments                                                         The language model we use across all our experiments is
A summary of our experimental results and comparison with              deepseek-math-7b-base (Shao et al., 2024), run on Nvidia
previous methods is shown in Table 2. Below, we state the              GeForce RTX 3090 with vLLM (Kwon et al., 2023). Unless
experimental setup and describe how different parts of the             otherwise specified, we follow Jiang et al. (2023) to use a
results are obtained and provide additional ablation study             sampling temperature T = 0.6 with top p = 0.95. The
results. For the results in Lean implementation, please refer          default max number of tokens of the response is set to 2048,
to Appendix C.                                                         and when the length of the prompt exceeds 2048, we adjust
                                                                       the max number of tokens to 4096 − #token of the prompt.
4.1. Benchmark                                                         For few-shot prompting (and similarly for zero-shot prompt-
                                                                       ing), we prepare few-shot examples that are the same as
We evaluate our methods on the Isabelle part of
                                                                       those of Jiang et al. (2023) except that the proof sketches
miniF2F (Zheng et al., 2021), a benchmark for formal
                                                                       are modified to new full proofs written by us. For n-shots
Olympiad-level mathematics problems across four differ-
ent formal languages. Unless otherwise specified, we use                   9
                                                                             https://github.com/openai/miniF2F/tree/
‘miniF2F-test’ or ‘the original version of miniF2F-test’ or            main/isabelle
                                                                          10
‘the DSP-version miniF2F-test’ to refer to the dataset in-                  You can find our curated version here: https://
cluded in the code repository8 of Jiang et al. (2023), which           github.com/haoxiongliu/ProofAug/blob/main/
                                                                       isabelle_src/datasets/minif2f-test-curated.
provides an additional informal statement and informal draft           jsonl. See also Appendix H for the details of how we curate
  8                                                                    miniF2F.
    https://github.com/albertqjiang/draft_                                11
sketch_prove/blob/main/aligned_problems/                                     To reproduce our results, using the same CPU is a necessary
new_complete_mini.jsonl                                                requirement. See Appendix D for more discussion on the repro-
                                                                       ducibility issues.



                                                                   7
                     ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis

Table 2: Comparison of methods using Isabelle as the proof assistant on MiniF2F-test. For BFS methods, the sample
budget N × S × T corresponds to N attempts of S expansion with T iterations. As to tree-search methods, it becomes
N × T , with the same meanings for the symbols. Results with a ‘† ’ are obtained using a mixed strategy.

            Method                                                  Model                 Sample Budget     miniF2F-test
            Methods using Isabelle
            DSP (Jiang et al., 2023)                            CodeX                          100             39.3%
            Subgoal-XL (Zhao et al., 2024)               Fine-tuned Llama-8B                   64              39.3%
                                                                                             16384†            56.1%
            LEGO-Prover (Wang et al., 2023a)                  mixed GPTs                       100             50.0%
            Lyra (Zheng et al., 2024)                           GPT-4                          100             47.1%
                                                                                               200             51.2%
            POETRY (Wang et al., 2024)                Fine-tuned ProofGPT (1.3B)          1 × 32 × 128         42.2%
            Our Experiments (using Isabelle)
            DSP baseline                                deepseek-math-7b-base                   1              28.7%
                                                                                                10             40.6%
                                                                                               100             49.2%
            ProofAug                                    deepseek-math-7b-base                   1          36.5%(+7.8%)
                                                                                                10         44.7%(+4.1%)
                                                                                               100         52.5%(+3.3%)
            ProofAug (0-shot)                           deepseek-math-7b-base                  500             54.5%
            ProofAug (0-shot) + ERP                     deepseek-math-7b-base                  500             56.1%
            ProofAug + Mixed Strategy                   deepseek-math-7b-base                 1400†            61.9%
            ProofAug + Mix. + Dataset Curation          deepseek-math-7b-base                 2100†            66.0%
            Methods using Lean
            HTPS (Lample et al., 2022)                      Evariste (600M)                64 × 5000           41.0%
            RMaxTS (Xin et al., 2024b)              DeepSeek-Prover-V1.5-RL (7B)           32 × 6400†          63.5%
            BFS + CG (Wu et al., 2024)               InternLM2.5-StepProver (7B)         256 × 32 × 600        65.9%


prompting, we randomly sample n examples from the candi-
dates. By default, we use 1-shot prompting. See Appendix E
for our specific prompt text, the reason for choosing 1-shot,
and more details on the prompt construction process.
For multiple attempts of proof, we record the checked semi-
proofs and skip them when obtaining them in the subsequent
attempts. This, in fact, harms the final performance since
some tactics and Sledgehammer do not always give the
same result under the same conditions. Nevertheless, this
practice can help us significantly reduce the elapsed time of
the experiments.

4.3. Results of ProofAug
We do ablation studies to validate the effectiveness of
ProofAug (without the ERP module). We first get the DSP                     Figure 3: Ablation of three different prompting ways.
baseline results in our setting. Compared to the performance
of the original DSP implementation on miniF2F-test, our                  formance of 36.5%, 44.7% and 52.5%, significantly outper-
DSP baseline is 9.9% higher (49.2% v.s 39.3% in 100 at-                  forming the baseline by 7.8%, 4.1% and 3.3%, respectively.
tempts) due to differences in proving environments12 , choice
                                                                         Note that ProofAug can also be applied to the proof sketches
of the prompting methods and model selection. Then we
                                                                         generated by DSP. Figure 3 shows how the number of
compare ProofAug results with our DSP baselines. Under
                                                                         proved theorems changes as the number of attempts in-
sample budgets of 1, 10 and 100, ProofAug achieves per-
                                                                         creases w/ or w/o ProofAug for three prompting methods:
  12
    See Appendix D for a discussion on the differences of theorem        DSP prompting, full proof prompting, and the more token-
proving environment between ours and that of Jiang et al. (2023).        usage friendly zero-shot prompting. By w/o ProofAug,

                                                                     8
                    ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis

we mean the ‘Prove’ step in DSP, i.e., <ATP> is tried at              through its ability to operate across various granularities and
the sorrys in the proof sketch. It can be seen that while             the fallback mechanism. Robustness is a highly desirable
the performance of our few-shot prompting and zero-shot               property for systems lacking inherent verification mecha-
prompting w/o ProofAug is much lower than that of DSP                 nisms, such as informal mathematical problem-solving and
prompting, ProofAug helps them achieve a comeback. This               software engineering. Therefore, we are also highly inter-
justifies our choice of generating full proofs instead of proof       ested in exploring the effective application of ProofAug in
sketches.                                                             these domains.

4.4. Results of the ERP module                                        Impact Statement
We try 500 attempts of proof for each problem, using zero-            This paper presents work whose goal is to advance the field
shot prompting for ProofAug w/ and w/o ERP module.                    of Machine Learning. There are many potential societal
When the ERP module is turned on, we record the cumula-               consequences of our work, none of which we feel must be
tive number of queries and stop verifying when it reaches             specifically highlighted here.
500 for a fair comparison.
The result shows that the ERP module can bring an extra               References
1.6% performance gain. If we do not restrict the number
of queries, we can achieve a pass rate of 57.4%(+2.9%                 Avigad, J., De Moura, L., and Kong, S. Theorem proving in
compared to the ProofAug without ERP).                                  lean, 2021. URL https://leanprover.github.
                                                                        io/theorem_proving_in_lean4.
4.5. Cumulative Results of Mixed Strategy Experiments                 Barras, B., Boutin, S., Cornes, C., Courant, J., Coscoy,
During the completion of this work, we have tried various se-           Y., Delahaye, D., de Rauglaudre, D., Filliâtre, J.-C.,
tups to search for the best recipe. While some setups fail to           Giménez, E., Herbelin, H., et al. The coq proof assistant
achieve the best performance on the benchmark compared to               reference manual. INRIA, version, 6(11):17–21, 1999.
results we present above, diverse ways of generating proofs
                                                                      Bibel, W. Automated theorem proving. Springer Science &
help prove more theorems. The setups include: 1) Different
                                                                        Business Media, 2013.
versions of prompts. We have three versions of demon-
stration examples for few-shot prompt generation, and two             Dong, K., Mahankali, A., and Ma, T. Formal theorem
versions of zero-shot prompt are used in our experiments.               proving by rewarding llms to decompose proofs hier-
2) Whether to include Informal drafts. The informal drafts              archically, 2024. URL https://arxiv.org/abs/
could mislead LLMs. Although ProofAug can sometimes                     2411.01829.
be a rescue, it is not always the case.
                                                                      First, E., Rabe, M. N., Ringer, T., and Brun, Y. Baldur:
In total, we try each problem of the original miniF2F-test
                                                                        Whole-proof generation and repair with large language
under a sample budget of around 1400 in total, and 2100 for
                                                                        models, 2023. URL https://arxiv.org/abs/
the two versions in total. See Table 3 in Appendix F for a
                                                                        2303.04910.
breakdown of these two numbers. On the original miniF2F-
test, we solve 61.9% of the problems, which is 5.8% higher            Goertzel, Z. A., Jakubův, J., Kaliszyk, C., Olšák, M., Piepen-
than the previous Isabelle SOTA. On the curated version,                brock, J., and Urban, J. The isabelle enigma, 2022. URL
the solving rate comes to 66.0%.                                        https://arxiv.org/abs/2205.01981.

                                                                      Han, J. M., Rute, J., Wu, Y., Ayers, E. W., and Polu, S.
5. Discussion and Future Directions                                     Proof artifact co-training for theorem proving with lan-
Although this work demonstrates that our ProofAug method                guage models, 2022. URL https://arxiv.org/
significantly improves the performance of the neural the-               abs/2102.06203.
orem prover on the miniF2F benchmark, there remains a
notable gap in tackling IMO-level problems or research-               Harrison, J. Proof style. In International workshop on types
level challenges within formal systems. How to incorporate              for proofs and programs, pp. 154–172. Springer, 1996.
ProofAug into expert iteration methods (Xin et al., 2024a)            Harrison, J. Hol light: An overview. In International
or online learning methods (Lample et al., 2022) to further             Conference on Theorem Proving in Higher Order Logics,
improve the performance is one direction of future work.                pp. 60–66. Springer, 2009.
We believe that another important direction for future work
                                                                      Irving, G., Szegedy, C., Alemi, A. A., Eén, N., Chollet,
is to fully leverage the robustness introduced by ProofAug
                                                                         F., and Urban, J. Deepmath-deep sequence models for

                                                                  9
                    ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis

  premise selection. Advances in neural information pro-                Polu, S., Han, J. M., Zheng, K., Baksys, M., Babuschkin,
  cessing systems, 29, 2016.                                              I., and Sutskever, I. Formal mathematics statement cur-
                                                                          riculum learning, 2022. URL https://arxiv.org/
Jiang, A. Q., Li, W., Han, J. M., and Wu, Y. Lisa: Language               abs/2202.01344.
   models of isabelle proofs. 6th Conference on Artificial
   Intelligence and Theorem Proving, 2021.                              Schumann, J. M. Automated theorem proving in software
                                                                          engineering. Springer Science & Business Media, 2013.
Jiang, A. Q., Welleck, S., Zhou, J. P., Li, W., Liu, J., Jamnik,
   M., Lacroix, T., Wu, Y., and Lample, G. Draft, sketch,               Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X.,
   and prove: Guiding formal theorem provers with infor-                  Zhang, H., Zhang, M., Li, Y. K., Wu, Y., and Guo,
   mal proofs, 2023. URL https://arxiv.org/abs/                           D. Deepseekmath: Pushing the limits of mathemat-
   2210.12283.                                                            ical reasoning in open language models, 2024. URL
                                                                          https://arxiv.org/abs/2402.03300.
Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu,
 C. H., Gonzalez, J. E., Zhang, H., and Stoica, I. Efficient            Silver, D., Huang, A., Maddison, C. J., Guez, A., Sifre, L.,
 memory management for large language model serving                       Van Den Driessche, G., Schrittwieser, J., Antonoglou, I.,
 with pagedattention. In Proceedings of the ACM SIGOPS                     Panneershelvam, V., Lanctot, M., et al. Mastering the
 29th Symposium on Operating Systems Principles, 2023.                     game of go with deep neural networks and tree search.
                                                                           nature, 529(7587):484–489, 2016.
Lample, G., Lacroix, T., Lachaux, M.-A., Rodriguez, A.,
  Hayat, A., Lavril, T., Ebner, G., and Martinet, X. Hyper-             Thakur, A., Tsoukalas, G., Wen, Y., Xin, J., and Chaud-
  tree proof search for neural theorem proving. Advances in               huri, S. An in-context learning agent for formal theorem-
  neural information processing systems, 35:26337–26349,                  proving, 2024. URL https://arxiv.org/abs/
  2022.                                                                   2310.04353.

                                                                        Wang, H., Xin, H., Zheng, C., Li, L., Liu, Z., Cao, Q.,
Limperg, J. and From, A. H. Aesop: White-box best-
                                                                         Huang, Y., Xiong, J., Shi, H., Xie, E., Yin, J., Li, Z.,
  first proof search for lean. In Proceedings of the 12th
                                                                         Liao, H., and Liang, X. Lego-prover: Neural theorem
  ACM SIGPLAN International Conference on Certified
                                                                         proving with growing libraries, 2023a. URL https:
  Programs and Proofs, pp. 253–266, 2023.
                                                                         //arxiv.org/abs/2310.00656.
Lin, H., Sun, Z., Yang, Y., and Welleck, S. Lean-star:
                                                                        Wang, H., Yuan, Y., Liu, Z., Shen, J., Yin, Y., Xiong, J., Xie,
  Learning to interleave thinking and proving, 2024. URL
                                                                         E., Shi, H., Li, Y., Li, L., et al. Dt-solver: Automated
  https://arxiv.org/abs/2407.10040.
                                                                         theorem proving with dynamic-tree sampling guided by
Loos, S. M., Irving, G., Szegedy, C., and Kaliszyk, C. Deep              proof-level value function. In Proceedings of the 61st
  network guided proof search. In LPAR, volume 46 of                     Annual Meeting of the Association for Computational
  EPiC Series in Computing, pp. 85–105. EasyChair, 2017.                 Linguistics (Volume 1: Long Papers), pp. 12632–12646,
                                                                         2023b.
Lu, M., Delaware, B., and Zhang, T. Proof automation
  with large language models. In Proceedings of the 39th                Wang, H., Xin, H., Liu, Z., Li, W., Huang, Y., Lu, J., Yang,
  IEEE/ACM International Conference on Automated Soft-                   Z., Tang, J., Yin, J., Li, Z., and Liang, X. Proving theo-
  ware Engineering, pp. 1509–1520, 2024.                                 rems recursively, 2024. URL https://arxiv.org/
                                                                         abs/2405.14414.
Megill, N. D. and Wheeler, D. A. Metamath: A Com-
                                                                        Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., Santos,
 puter Language for Mathematical Proofs. Lulu Press,
                                                                         M. D., Sung, F., Vinyes, M., Ying, Z., Zhu, Z., et al.
 Morrisville, North Carolina, 2019. URL https://us.
                                                                         Kimina-prover preview: Towards large formal reason-
 metamath.org/downloads/metamath.pdf.
                                                                         ing models with reinforcement learning. arXiv preprint
Mikuła, M., Tworkowski, S., Antoniak, S., Piotrowski, B.,                arXiv:2504.11354, 2025.
 Jiang, A. Q., Zhou, J. P., Szegedy, C., Łukasz Kuciński,
                                                                        Wang, M., Tang, Y., Wang, J., and Deng, J. Premise selec-
 Miłoś, P., and Wu, Y. Magnushammer: A transformer-
                                                                         tion for theorem proving by deep graph embedding, 2017.
 based approach to premise selection, 2024. URL https:
                                                                         URL https://arxiv.org/abs/1709.09994.
 //arxiv.org/abs/2303.04488.
                                                                        Wenzel, M. et al. The isabelle/isar reference manual, 2004.
Polu, S. and Sutskever, I. Generative language modeling
  for automated theorem proving, 2020. URL https:                       Wiedijk, F. Formal proof sketches. In Types for Proofs and
  //arxiv.org/abs/2009.03393.                                            Programs: International Workshop, TYPES 2003, Torino,

                                                                   10
                   ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis

  Italy, April 30-May 4, 2003, Revised Selected Papers, pp.          Zheng, K., Han, J. M., and Polu, S. Minif2f: a cross-system
  378–393. Springer, 2004.                                             benchmark for formal olympiad-level mathematics. arXiv
                                                                       preprint arXiv:2109.00110, 2021.
Wiedijk, F. The seventeen provers of the world: Foreword
 by Dana S. Scott, volume 3600. Springer, 2006.

Wiedijk, F. A synthesis of the procedural and declarative
 styles of interactive theorem proving. Logical Methods in
 Computer Science, Volume 8, Issue 1, March 2012. ISSN
 1860-5974. doi: 10.2168/lmcs-8(1:30)2012. URL http:
 //dx.doi.org/10.2168/LMCS-8(1:30)2012.

Wu, Y., Jiang, A. Q., Li, W., Rabe, M. N., Staats, C., Jam-
 nik, M., and Szegedy, C. Autoformalization with large
 language models, 2022. URL https://arxiv.org/
 abs/2205.12615.

Wu, Z., Huang, S., Zhou, Z., Ying, H., Wang, J., Lin, D., and
 Chen, K. Internlm2.5-stepprover: Advancing automated
 theorem proving via expert iteration on large-scale lean
 problems, 2024. URL https://arxiv.org/abs/
 2410.15700.

Xin, H., Guo, D., Shao, Z., Ren, Z., Zhu, Q., Liu, B.,
  Ruan, C., Li, W., and Liang, X. Deepseek-prover: Ad-
  vancing theorem proving in llms through large-scale
  synthetic data, 2024a. URL https://arxiv.org/
  abs/2405.14333.

Xin, H., Ren, Z. Z., Song, J., Shao, Z., Zhao, W., Wang,
  H., Liu, B., Zhang, L., Lu, X., Du, Q., Gao, W., Zhu,
  Q., Yang, D., Gou, Z., Wu, Z. F., Luo, F., and Ruan, C.
  Deepseek-prover-v1.5: Harnessing proof assistant feed-
  back for reinforcement learning and monte-carlo tree
  search, 2024b. URL https://arxiv.org/abs/
  2408.08152.

Yang, K., Swope, A. M., Gu, A., Chalamala, R., Song,
  P., Yu, S., Godil, S., Prenger, R., and Anandkumar, A.
  Leandojo: Theorem proving with retrieval-augmented
  language models, 2023. URL https://arxiv.org/
  abs/2306.15626.

Zhao, X., Li, W., and Kong, L. Decomposing the enigma:
  Subgoal-based demonstration learning for formal the-
  orem proving, 2023. URL https://arxiv.org/
  abs/2305.16366.

Zhao, X., Zheng, L., Bo, H., Hu, C., Thakker, U., and
  Kong, L. Subgoalxl: Subgoal-based expert learning for
  theorem proving, 2024. URL https://arxiv.org/
  abs/2408.11172.

Zheng, C., Wang, H., Xie, E., Liu, Z., Sun, J., Xin, H.,
  Shen, J., Li, Z., and Li, Y. Lyra: Orchestrating dual
  correction in automated theorem proving, 2024. URL
  https://arxiv.org/abs/2309.15806.

                                                                11
                    ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis

A. Other Related Work
In the main body, Table 1 and Table 2 only include representative neural theorem proving methods that are most related to
this work: they all focus on solving Olympic-level mathematical problems with generative language models. Below we
introduce other related work.
Premise Selection. One line of work uses embedding models to facilitate the selection of premises for automation
tools (Irving et al., 2016; Wang et al., 2017; Goertzel et al., 2022; Yang et al., 2023). The machine-learning enhanced
automation tools can be used to strengthen the power of the <ATP> method in our ProofAug algorithm. For example, the
Magnushammer(Mikuła et al., 2024) is an ideal substitution for the sledgehammer, whose solving rate on miniF2F is 34.0%
(against 20.9% of sledgehammer) and has a mode that does not require GPU or TPU accelerators. We believe that access to
such tools can help ProofAug achieve better performance on theorem proving.
Hierarchical Theorem Proving. We note that the idea of hierarchically proving theorems in declarative ITP systems has
been explored in several previous works. Besides the proof-step based recursive proving method POETRY (Wang et al.,
2024) discussed in Section 3.3, LEGO-Prover (Wang et al., 2023a) uses a skill library to record the previously proved
lemmas and retrieves relative skills when instructing GPT series models to synthesize its proof based on a decomposed
informal draft. It is a hierarchical proving method in the sense that the lemmas used for proving the current theorem can be
built on more low-level lemmas. From another point of view, LEGO-Prover uses all previous queries to solve the current
theorem hierarchically. In contrast, Dong et al. (2024) does not record a skill library, but finishes the hierarchical proving
from scratch. The key difference between these hierarchical proving methods and our ProofAug (without ERP module) is
that we work in a bottom-up fashion to best exploit the power of traditional automation tools, contrary to their top-down
frameworks that all require extra queries to the model when stepping into the next level proof. We argue that bottom-up
fashion aligns more with the pre-trained corpus, thus making best use of the theorem proving knowledge possessed by the
model. In contrast, top-down methods require in-context learning or fine-tuning to control the behavior of LMs, which
could hurt the intrinsic ability of the model and bring extra complexity to the problem. This is likely the underlying reason
why ProD-RL (Dong et al., 2024) fails to make significant improvements over the simple SFT method on miniF2F-test.
Whereas our ProofAug serves as a play-and-plug module and can fall back to naive single-pass generation, being superior
in efficiency, robustness, and flexibility. Moreover, by adding the ERP module, we integrate the top-down and bottom-up
fashions in a sample-efficient way.
While finalizing this paper, the authors became aware of a concurrent and independent work Lu et al. (2024), which proposes
 PALM, that shares similar high-level ideas with ProofAug. However, our work is distinct in several key aspects: 1) PALM
works in Coq (Barras et al., 1999), a procedural proof language where declarative modes (such as the ‘Mathematical Proof
 Language’ introduced in the Coq reference manual) are less common. Since tactics in the procedural style proof languages
 are designed in the spirit that the user decides what tactic to use next by observing the resulting goal or proof state after using
 the last tactic, it is often the case that new variables or facts are introduced by one tactic and the subsequent tactics need to
 specify the names of these facts. Thus, performing whole-proof generation as PALM does for Coq is generally harder than
 in the declarative style proofs and could be detrimental to the performance. Besides, in Coq proofs, there are few explicit
 intermediate conjectures or block structures as in those in Isar or Lean 4. Thus, for each tactic, the backtracking procedure
 of PALM simply goes back to the proof state before the unrepairable error and continues backtracking, except for the
 bullet point structure that is equivalent to the ‘case’ structure in Isabelle/Isar (rather than the more common ‘have’ method).
 Consequently, the proofs found by PALM mostly show scarce high-level structures as we can observe from the results
 provided in its code repository 13 . In contrast, our ProofAug departs from the DSP framework and takes an ‘augmentation’
 perspective to solve the issues of DSP. We first determine all compatible semi-proofs, then sequentially prune the semi-proofs
 that become impossible to be extended into a full proof after each time we apply <ATP > to an intermediate conjecture.
This procedure makes ProofAug fit with the ‘sketch’ procedure of DSP that translates the informal proof into intermediate
 conjectures, and each semi-proof is expected to align with the corresponding part of the informal proof. Note that such
 correspondence is hard to achieve for procedural proofs and obligating the LLMs to use the uncommon declarative mode or
‘assert’ keywords in Coq could be detrimental to the performance. Although in Appendix C we also discuss how to transform
 a procedural style proof language into a declarative one in the spirit described in Wiedijk (2012) and then train models and
 apply ProofAug accordingly, this procedure needs to fine-tune a model on enough data, which is in general expensive. In
 total, ProofAug is the choice for theorem proving models such as the DeepSeek-Prover series and the Kimina-Prover (Wang
 et al., 2025) series that achieve SOTA performance on the cross-language benchmark miniF2F, and provide detailed solutions
   13
        https://github.com/lachinygair/PALM/tree/main/evaluation/proof


                                                                12
                   ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis

and code. 2) Our work further explores the Efficient Recursive Proving module and shows it can boost the performance
with a relatively small number of queries. In fact, the counterpart of the ERP module for procedural-style proofs should
be some kind of truncate-and-resume tree-search algorithm (that only adds new nodes based on the initial proof proposal)
proposed in Xin et al. (2024b). However, since the proof style adopted by Deepseek-Prover-V1.5 series models is rather
declarative, RMaxTS becomes inefficient for them due to the potential reasons we analyzed in Section 3.3. 3) We make extra
contributions such as exploring extended mixture of strategies to enhance the performance, curating the Isabelle version of
miniF2F-test and finally achieving a cumulative pass rate of 66.0% on this benchmark, while the performance of Coq-based
methods remains unclear on the problems of miniF2F since the Coq version is not included by now.
Declarative versus Procedural. The discussion of proof styles dates back to Harrison (1996). Wiedijk (2006) compares the
proof styles of a wide range of different systems. Wiedijk (2012) discusses how to convert from a procedural system to a
declarative one. Avigad et al. (2021) introduces the two styles of proof in Lean and provides concrete examples.
Other proof-step generation works. Aside from works introduced in Table 1, such as Polu & Sutskever (2020); Lample
et al. (2022), Han et al. (2022); Polu et al. (2022); Wang et al. (2023b) are also valuable explorations on what practice is
beneficial for tree-search proof-step generation methods. Thakur et al. (2024) designs an agent that makes use of the history
ITP feedbacks in a serialization way.
Other whole-proof generation works. Xin et al. (2024a); Wu et al. (2022) verify the effectiveness of expert iteration on
neural theorem proving using the naive whole-proof generation method. They build the first-round theorem statements
through autoformalization of the informal problems. First et al. (2023) employs Isabelle error messages to enhance the
direct full proof synthesis ability of LLM.

B. Examples of the DSP Issues
Figure 4 and Figure 5 show examples of the ‘Hard Conjecture’ issue and the ‘Complicated Draft’ issue described in
Section 1.

   theorem numbertheory_sqmod3in01d:
     fixes a :: int
     shows "aˆ2 mod 3 = 0 \<or> aˆ2 mod 3 = 1"
   proof -
   (* Let a be an integer, then a \pmod 3 \in {0, 1, 2}. *)
     have c0: "a mod 3 \<in> {0,1,2}" by fastforce
   (* Using that aˆ2 \pmod 3 = (a \pmod 3)ˆ2 \pmod 3 *)
     have "aˆ2 mod 3 = (a mod 3)ˆ2 mod 3" by (simp add: power_mod)
   (* we have aˆ2 \pmod 3 \in {0, 1}. *)
     then show ?thesis using c0 sledgehammer
   qed
    Isabelle Info: Sledgehammering... No proof found



Figure 4: An example of the ‘Hard Conjectures’ issue. In this example, although the informal draft is reasonable to
human, sledgehammer fails to find a proof for the final step.


C. Discussion of Implementing ProofAug for Other Proof Assistants
Lean. Although Lean proofs can be completely tactic-based, block-structures starting with by are very common as
well, especially for the proofs of Olympics-level math problems (refer to Xin et al. (2024b); Wang et al. (2025) for the
example proofs they find). As a result, Lean proofs are also amendable for proof structure analysis, so we also build a
simple implementation of ProofAug in Lean. As to the substitution of the <ATP> method, we use the combination of
Aesop(Limperg & From, 2023), omega and our hand-made heuristic try norm num [*]; try field simp [*]
at *; try ring nf at *; try nlinarith. For the proof structure analysis process, given a line of code, we
manually infer whether it is intended to be part of a statement or tactic from its indent and context. Our experiment result
shows that ProofAug improves the performance of Kimina-Prover-Preview-Distill-1.5B from 44.3% to 50.4% on miniF2F.
The improvement can be further enhanced if we can obtain a more proper control of the parsing and structure analysis

                                                             13
                    ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis


   theorem
     "gcd 180 168 = (12::nat)"
     by eval


   theorem
     "gcd 180 168 = (12::nat)"
   proof -
   (* If a number divides into both 180 and 168 *)
     have "gcd 180 168 dvd 180" sledgehammer
     moreover have "gcd 180 168 dvd 168" sledgehammer
   (* it must also divide into their difference. *)
     finally have "gcd 180 168 dvd 12" sledgehammer
   qed
    Isabelle Info: Sledgehammering... No proof found



Figure 5: An example of the ‘Complicated Draft’ issue. In this example, while the eval proof method can prove the
theorem easily in Isabelle, the translation of informal draft into a formal proof fails to pass the verification due to the lack of
explicit type annotations, which is a typical error the language models could make in autoformalization.




process and get better substitutions of the <ATP> method. Readers may refer to our code for more implementation details.
For procedural ITPs that work mostly in a tactic-based way and do not have block structures in the proofs explicitly, in
principle, one can follow Wiedijk (2012) to build a proof interface that supports declarative style proofs upon the original
system. Since Wiedijk (2012) also provides a generic way to convert the proofs in the original procedural language to
declarative ones, one may obtain data for training language models on this new language by conversion of the corpora in the
original language. Then one can perform ProofAug on this new declarative language.

D. Theorem Proving Environment Setup Details and Discussion on the Reproducibility
Our theorem proving environment setup mainly follows that described in Jiang et al. (2023), but there are some subtle
differences. For the setup of PISA, we set the candidate provers of Sledgehammer to CVC4 vampire verit e spass
z3 zipperposition, with a 30s timeout for each and 120s in total, as in Jiang et al. (2023). However, we find that
in their PISA source code, they use cvc5 instead of CVC4 and the actual total timeout for Sledgehammer is around 35s
instead of the intended 120s, seemingly due to an implementation bug. We fix this bug and still use CVC4 since cvc5
is not integrated in Isabelle 2022. We do not compile the Archive of Formal (AoF) library due to lack of disk space
to simultaneously run 12 instances possessing compiled AoF heaps on our server. As a result, we do not import the
Symmetric Polynomials.Vieta theory as in Jiang et al. (2023). Besides, The heuristics used in our <ATP> method
and those in Jiang et al. (2023) differ in that we add an extra simp:add mod simps, remove force since we already
have fastforce and remove presburger,linarith since arith integrates the two in a rough sense.
To reproduce the results that involve the use of complex built-in proof methods or off-the-shelf ATPs, one has to make sure to
run PISA instances on the same CPU since the performance of these automation methods heavily rely on the computational
power of the CPU.
Nevertheless, even using the same environment, it is still hard to produce exactly the same results due to the inherent
randomness of these automation methods. The good news, however, is that for theorem proving, we are confident that we
have made some progress when new theorems get proved, no matter whether this is completely reproducible or not. So we
focus on making sure the obtained proofs are correct by verifying them again in Isabelle. We provide the found proofs in
attachment to our code. Note that although there are cases where the reconstructed proof fails due to the timeout of Isabelle
built-in methods such as smt and metis, it does not mean that the theorems are not proved. It is only the limitation of
these tactics.

                                                                14
                   ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis

E. Prompt Construction
The prompts in our experiments are all constructed from three components: prompt template, few-shot demonstration
examples. and a prompter. The prompt template is a JSON file that contains different roles as names and corresponding
templates as values. Each example is also an JSON object whose names occur in the templates. A prompter mainly consists
of a chat template that maps the sampled examples to a conversation consisted by messages according to the prompt
template.
For example, for few-shot prompting for ProofAug, we use the prompt template shown in Figure 6. The examples contain
names xi,yi,xf,yf, corresponding to an informal statement, an informal draft, the formal statement, and the formal full
proof. For zero-shot prompting (possibly with ERP), we use the prompt template in Figure 8, which has two extra fields ps
and yf p. For non-ERP prompting, they are set to null string. For ERP prompting at state s, they corresponds to the ‘proof
state’ s.state and the partial proof that have been verified at this state.
As to the chat template, we simply use three newlines to separate pairs of user-assistant messages and concatenate the user
message and assistant message in each pair. Nevertheless, we mainly expect the response to stop at the end of the Isabelle
code block.
Figure 7 shows an example of the sampled 1-shot prompt.

{
      "user": "Please complete the following Isabelle proof.\n‘‘‘isabelle\n(*
         Informal statement:\n{xi}\n\nInformal proof:\n{yi} *)\n{xf}\n",
      "assistant": "{yf}\n‘‘‘\n\n",
      "stop": ["‘‘‘", "\ntheorem", "\nend"]
}

                              Figure 6: The prompt template we use for few-shot prompting.

As to the choice of the number of shots to use, in Jiang et al. (2023), they set #shot=3 when prompting the model to translate
a draft. We find that since the maximum sequence length of deepseek-math-7b-base is only 4096, few-shot prompting can
lead to failure of proofs that are long in nature. As a consequence, DSP with 3-shots prompting solves 117/244, 2-shots
118/244, both smaller than 1-shot (120/244). Thus, across the paper, we use 1-shot prompting unless otherwise stated.

F. Breakdown of the Mixture of Strategies
Table 3 shows the breakdown of the mixture of strategies in Section 4.4. Below are some explanations of the options
appearing in Table 3.
As to the prompt version, we have 3 versions of few-shot prompting and two versions of zero-shot prompting. The three
versions of few-shot prompting share the same prompt template shown in Figure 6, but differ in examples: ‘DSP’ refers to
the examples in Jiang et al. (2023), and ‘few-shot’ refers to examples used for ProofAug, where we write full proofs that
strictly match the informal proofs provided in the miniF2F dataset of Jiang et al. (2023). In contrast, many of the informal
proofs of DSP few-shot prompting examples are just descriptions of formal sketches prepared in advance. We also have
a ‘few-shot-legacy’ version where we first write the simplest proof (rather than a proof sketch) we can come up for each
theorem, then write a natural language description for it as an informal proof. Although it turns out that the ‘few-shot’
version is the best one for 1-shot prompting, the three sets of examples form a complement to each other. Since zero-shot
prompting do not involve examples, the two versions of our zero-shot prompts only differ in the instruction text and format.
For the 0-shot-legacy prompt, we do not have the ‘Below is a complete proof of a statement in Isabelle/Isar, translated from
the informal proof.’ text in the “user” field shown in Figure 8.
A ‘×’ in the ‘Draft’ column means that informal statement and the informal proof are not included in the prompt.
For the experiments using the ERP module, we only count the proved theorem using fewer than 700 and 200 requests to the
model, for the experiments with 500 attempts and 100 attempts, respectively. As to the pass rates of these experiments, since
we only evaluate on the previously unproved theorems for the curated version dataset, we put N/As for them.
For further information, such as the contents of the examples, please refer to our code.

                                                             15
                    ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis


   Please complete the following Isabelle proof.
   (* Informal statement:
   When Rachel divides her favorite number by 7, she gets a remainder of 5.
   What will the remainder be if she multiplies her favorite number by 5 and then divides by 7?
   Show that it is 4.

   Informal proof:
   Let n be Rachel’s favorite number. Then n ≡ 5 (mod 7), so 5n ≡ 5 · 5 ≡ 25 ≡ 4 (mod 7). *)
   theorem mathd_numbertheory_335:
     fixes n :: nat
     assumes h0 : "n mod 7 = 5"
     shows "(5 * n) mod 7 = 4"
   proof -
     (* so 5n ≡ 5 · 5 ≡ 25 ≡ 4 (mod 7). *)
     have c0: "(5 * n) mod 7 = (5 * 5) mod 7"
     proof -
       have c00: "(5 * n) mod 7 = (5 mod 7 * (n mod 7)) mod 7"
         by (auto simp: mod_simps)
       then show ?thesis unfolding h0
         by auto
     qed
     also have "... = 4 mod 7" by auto
     finally show ?thesis by auto
   qed


   Please complete the following Isabelle proof.
   (* Informal statement:
   {informal statement of the problem}

   Informal proof:
   {informal draft of the problem} *)
   {formal statement of the problem}


                                 Figure 7: An example of final 1-shot prompt for ProofAug.




G. Additional Experimental Results
On miniF2F-valid, ProofAug w/ and w/o ERP module achieve 58.6% and 57.0% in 100 attempts of proof respectively.
During the experiment, we make sure the problem to prove is not in the candidate examples.

H. Curation of the Isabelle part of miniF2F
Our curation of DSP-version miniF2F test split mainly includes two types: 1) Typo fix: Statements with typos in variable
names or numbers are mostly completely wrong and unprovable. 2) Modifying the type of the variables from nat to int
for theorems that could potentially involve the minus operation in the proofs. This is important because, for example, the
operation (2::nat) - (3::nat) is valid and expected to be (0::nat) in Isabelle/HOL. Although sometimes the
original statement can still be proved in the sense that the resulting 0 also satisfies the constraints in the statement, it does
not express the intent of the original problem. Figure 9 shows such an example.
After finishing the curation process, the authors get to learn about that there is a FAIR version repository of miniF2F14
that is actively in maintenance and most of the typos and inappropriate uses of minus of nat type numbers we find in the
DSP-version have been fixed in the latest commits. Nevertheless, several typos and some inappropriate use of nat type
remain. Thus, we still make a pull request15 to the FAIR miniF2F repository to update part of our curation to the upstream.
  14
       https://github.com/facebookresearch/miniF2F
  15
       https://github.com/facebookresearch/miniF2F/pull/18

                                                               16
                  ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis

{
     "user": "Please complete the following Isabelle proof.\n‘‘‘isabelle\n(*
        Informal statement:\n{xi}\n\nInformal proof:\n{yi} *)\n{xf}\n{yf_p} {ps}",
     "assistant": "{yf_c}\n‘‘‘\n\n",
     "stop": ["‘‘‘", "\ntheorem", "\nend", "\nlemma"]
}

      Figure 8: The prompt template we use for zero-shot prompting for efficient recursive proving (ERP) module.

                       Table 3: Breakdown of the mixture of strategies introduced in Section 4.4.

                 #attempts    Prompt Ver.      #shots   Draft     ERP   #queries   Curated Ver.   Pass Rate
                   500           0-shot          0       ×        ×       500          ✓            N/A
                   500           0-shot          0       ✓        ✓       700          ×           57.4%
                   100          few-shot         1       ✓        ×       100          ×           52.5%
                   100          few-shot         1       ✓        ×       100          ✓            N/A
                   100       few-shot-legacy     1       ×        ×       100          ×           48.4%
                   100       few-shot-legacy     1       ✓        ×       100          ×           50.8%
                   100            DSP            1       ✓        ×       100          ×           49.2%
                   100        0-shot-legacy      0       ✓        ×       100          ✓            N/A
                   100        0-shot-legacy      0       ✓        ×       100          ×           50.8%
                   100        0-shot-legacy      0       ✓        ✓       200          ×           52.0%



I. An Example of How ProofAug Induce a Proof
Figure 10 shows an example of ProofAug inducing a proof from a failed proof proposal generated by the model.




                                                             17
                ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis




Differences:
  theorem imo_2001_p6:
- fixes a b c d ::nat
+ fixes a b c d ::int
    assumes "0 < a \<and> 0 < b \<and> 0 < c \<and> 0 < d"
      and "d < c"
      and "c < b"
      and "b < a"
-     and "a * c + b * d = (b + d + a - c) * (b + d - a + c)"
+     and "a * c + b * d = (a + b - c + d) * (- a + b + c + d)"
    shows "\<not> prime (a * b + c * d)"

Figure 9: How we fix the imo 2001 p6 in DSP-version miniF2F-test. The "a * c + b * d = (b + d + a -
c) * (b + d - a + c)" constraint does not express what it intends in the original statement when a > b + d.




                                                        18
                   ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis


   theorem algebra_sqineq_at2malt1_init_proof:
     fixes a::real
     shows "a * (2 - a) \<le> 1"
   proof -
     have "(a - 1)\<ˆsup>2 \<ge> 0" for a::real
     proof -
       have "0 \<le> (a - 1) * (a - 1)"
         using zero_le_square by auto
       then show "(a - 1)\<ˆsup>2 \<ge> 0"
         by (simp add: power2_eq_square)
     qed
     then have "a * (2 - a) \<le> 1" for a::real
     proof -
       have "a * (2 - a) = 2 * a - a\<ˆsup>2" by (simp add: power2_eq_square)
       also have "... = (a - 1)\<ˆsup>2 + 1 - a\<ˆsup>2" by (simp add: algebra_simps)
       also have "... \<le> 1"
         using \<open>0 \<le> (a - 1)\<ˆsup>2\<close> by linarith
       finally show ?thesis .
     qed
     then show ?thesis .
   qed

   theorem algebra_sqineq_at2malt1_MCSP:
     fixes a::real
     shows "a * (2 - a) \<le> 1"
   proof -
     have "(a - 1)\<ˆsup>2 \<ge> 0" for a::real
     proof -
       have "0 \<le> (a - 1) * (a - 1)"
         using zero_le_square by auto
       then show "(a - 1)\<ˆsup>2 \<ge> 0"
         by (simp add: power2_eq_square)
     qed
     then have "a * (2 - a) \<le> 1" for a::real
     proof -
       have "a * (2 - a) = 2 * a - a\<ˆsup>2" sorry
       also have "... = (a - 1)\<ˆsup>2 + 1 - a\<ˆsup>2" sorry
       also have "... \<le> 1"
         using \<open>0 \<le> (a - 1)\<ˆsup>2\<close> sorry
       finally show ?thesis .
     qed
     then show ?thesis .
   qed

   theorem algebra_sqineq_at2malt1_final:
     fixes a::real
     shows "a * (2 - a) \<le> 1"
   proof -
     have "(a - 1)\<ˆsup>2 \<ge> 0" for a::real
     proof -
       have "0 \<le> (a - 1) * (a - 1)"
         using zero_le_square by auto
       then show "(a - 1)\<ˆsup>2 \<ge> 0"
         by (simp add: power2_eq_square)
     qed
     then have "a * (2 - a) \<le> 1" for a::real by sos
     then show ?thesis .
   qed


Figure 10: An example of ProofAug inducing a proof from a failed initial proof proposal. It can be seen that the
initial proof fails inside the proof...qed block of proving a(2 − a) ≤ 1 due to the wrong intermediate claim 2 ∗ a − a2 =
(a − 1)2 + 1 − a2 . ProofAug finds that a(2 − a) ≤ 1 can be directly proved with the proof method sos given the previous
proved fact (a − 1)2 ≥ 0.
                                                              19
