                                                      Uncovering Hidden Correctness in LLM Causal Reasoning
                                                                     via Symbolic Verification

                                                      Paul He1,2 * Yinya Huang3,5 Mrinmaya Sachan3,5 Zhijing Jin1,2,4
                                                              1
                                                                University of Toronto 2 Vector Institute 3 ETH Zürich
                                                                   4
                                                                     MPI for Intelligent Systems 5 ETH AI Center
                                                                         {hepaul,zjin}@cs.toronto.edu
                                                                 {yingya.huang,mrinmaya.sachan}@inf.ethz.ch


                                                                  Abstract                                         Prompt: Imagine a diagnostic system where ambient temperature affects


                                             Large language models (LLMs) are increas-                         ✏️    both affects both calibration and output. Component stress influences
                                                                                                                       system failure and output. Humidity and sensor calibration affects
arXiv:2601.21210v1 [cs.AI] 29 Jan 2026




                                                                                                                    measurement of error. System failure affects output. What is the effect of
                                             ingly being applied to tasks that involve causal                                 intervening on component stress on system failure?
                                                                                                                   **Generate a causal graph and expression that models the problem**
                                             reasoning. However, current benchmarks often

                                                                                                               🤖
                                             rely on string matching or surface-level met-
                                                                                                                     Graph: A->D, A->G, B->F,B->G, C->E, D->E, F->G
                                             rics that do not capture whether the output of a                       Causal Expression: P(F | do(C), do(A), do(B), D)
                                             model is formally valid under the semantics of
                                                                                                                   Does the LLM generated expression entail (⊢) the target expression
                                             causal reasoning. To address this, we propose                                                under the graph?
                                             D OV ERIFIER, a simple symbolic verifier that                                              String Match


                                                                                                                                                                                       ❌
                                                                                                                           LLM Expression                             Label
                                             checks whether LLM-generated causal expres-                             P(F|do(C),do(A),do(B),D)                      P(F|do(B))
                                             sions are derivable from a given causal graph
                                                                                                                                            DoVerifier
                                             using rules from do-calculus and probability                                          P(F|do(C),do(A),do(B),D)
                                             theory. This allows us to recover correct an-
                                             swers to causal queries that would otherwise be
                                             marked incorrect due to superficial differences                         P(F|C,do(A),do(B),D)                 P(F|do(C),do(B),D)
                                             in their causal semantics. Our evaluations on
                                             synthetic data and causal QA benchmarks show                              BFS over all valid rule
                                                                                                                           applications,                      P(F|do(B),D)
                                             that D OV ERIFIER more accurately captures se-
                                                                                                                      each path is a proof tree
                                             mantic correctness of causal reasoning traces,                            under the given DAG.
                                             offering a more rigorous and informative way
                                             to evaluate LLMs on causal reasoning.
                                                                                                                                                                P(F|do(B))
                                                                                                                                                                                       ✅
                                             § https://github.com/Hepaul7/doverifier
                                                                                                               Figure 1: Our symbolic verifier checks whether a model-
                                         1    Introduction                                                     generated causal expression is semantically equivalent
                                                                                                               to the ground truth under a given DAG. Unlike string
                                         Causal reasoning lies at the core of human intelli-                   match, it explores all valid derivations using do-calculus
                                         gence. Unlike mere pattern recognition, it enables                    and probability rules to identify formal equivalence.
                                         us to reason about interventions, explain effects,
                                         and predict outcomes under hypothetical scenarios.
                                         As large language models (LLMs) (OpenAI, 2024;                        2024) have begun to evaluate LLMs on causal ques-
                                         Team, 2025; DeepSeek-AI, 2025) are increasingly                       tion answering. However, these efforts primarily
                                         being deployed in scientific, medical, and policy-                    focus on surface-level correctness: whether the
                                         related domains, their ability to generate and in-                    model’s answer matches a gold string or produces
                                         terpret causal claims is no longer optional—it is                     the right outcome in simple scenarios. While use-
                                         critical (Doshi-Velez and Kim, 2017). An LLM                          ful, these metrics fail to capture a more fundamen-
                                         that can distinguish between correlation and causa-                   tal question: does the model’s output represent a
                                         tion could support tasks ranging from experimental                    valid causal expression under formal semantics?
                                         design to scientific hypothesis generation.                              Furthermore, LLMs often produce expressions
                                            Recent causal reasoning benchmarks such as                         that are logically correct but syntactically different
                                         CLadder (Jin et al., 2023) and CausalBench (Wang,                     from the reference. These answers are penalized
                                             * This work was done while the author was at the University
                                                                                                               in the evaluations despite being correct, leading to
                                         of Toronto and the Vector Institute; the author is now at NTU         an incomplete picture of model capabilities. Cur-
                                         Singapore.                                                            rent causal reasoning benchmarks systematically

                                                                                                           1
penalize models that produce semantically valid             these techniques to causal reasoning, where correct-
causal expressions while rewarding outputs that are         ness is defined by do-calculus and DAG semantics.
syntactically similar but causally incorrect.
   This gap arises because causal inference relies          2   Related Work
on symbols: the validity of an expression like              Causal QA and LLM Evaluation Recent bench-
P (Y | do(X)) depends not on its string form, but           marks evaluate large language models (LLMs) on
on whether it is derivable from a given causal graph        their ability to answer causal questions expressed
using rules of do-calculus and probability theory.          in natural language. CLadder (Jin et al., 2023) and
In mathematical formalization tasks, models can of-         CausalBench (Wang, 2024) present standardized
ten be evaluated by plugging in values or checking          datasets of associational, interventional, and coun-
numerical correctness (Gao et al., 2025; Fan et al.,        terfactual queries grounded in causal graphs. How-
2024; Cobbe et al., 2021; Hendrycks et al., 2021).          ever, evaluation typically hinges on string similarity
However, as shown in Figure 1, we rarely know               to a gold-standard answer, without any guarantee
the full joint distribution P (·) in causal reasoning       of causal validity (Jin et al., 2023; Bondarenko
queries, preventing us from substituting numerical          et al., 2022; Joshi et al., 2024). Standard metrics
values; the ground truth is defined not by observed         like exact match, BLEU (Papineni et al., 2002),
values, but by derivability under a causal graph            token-level F1, and BERTScore (Zhang* et al.,
using the rules of do-calculus (Pearl, 1995). As a          2020) are commonly used to evaluate LLMs on
result, causal expressions must be evaluated based          causal QA tasks (Hu and Zhou, 2024). However,
on their formal relationship to a directed acyclic          these metrics assess surface similarity, not seman-
graph (DAG) and other expressions, rather than by           tic equivalence. Semantically incorrect expressions
simulation or numerical substitution.                       might score well due to shared tokens. As shown
   In this work, we propose D OV ERIFIER, a sym-            in Figure 2, they may penalize logically correct
bolic verifier to evaluate the equivalence of causal        outputs due to formatting differences, or falsely re-
expressions generated by LLM. Given a causal                ward incorrect answers that share common tokens.
graph and model generations, our system deter-              To our knowledge, no prior work evaluates causal
mines whether a generated causal expression is              QA using symbolic derivability as a criterion for
formally derivable from another using the set of            semantic correctness.
known rules. This allows us to recover semanti-
cally equivalent and correct outputs that existing          Formal Verification in Causal Inference The
benchmarks miss. Figure 1 illustrates an exam-              causal inference community has long relied on do-
ple for the core failure mode we address: causal            calculus (Pearl, 1995) and probability theory to
correctness depends on whether an expression is             determine whether a causal query is identifiable
derivable under a causal graph using do-calculus,           from observational data. Classical identifiability
not on its surface form.                                    algorithms (Shpitser and Pearl, 2008) and modern
   Our contributions are as follows:                        tools like dosearch (Tikka et al., 2021) formalize
                                                            this process as a search over valid derivations. How-
   • We propose a formal verification framework             ever, these tools are designed to compute causal
     for LLM-generated causal expressions, based            effects from structured inputs, not to verify whether
     on proof search over do-calculus and proba-            a model-generated expression is valid or equivalent
     bility transformations.                                under the causal graph. This verification step is
   • We show that D OV ERIFIER recovers a large             critical when evaluating the intermediate reason-
     portion of causally correct but syntactically          ing of LLMs. Another line of work, like Sheth
     mismatched outputs on both synthetic data              et al. (2025), checks if answers align with prede-
     and real benchmarks, outperforming standard            fined causal graphs but relies on template matching
     evaluation metrics used in causal reasoning.           rather than formal derivations and cannot handle
   • We demonstrate that symbolic verification en-          expressions involving do-calculus transformations.
     ables feedback for model self-correction, im-          In contrast, our approach treats verification as a
     proving causal accuracy without supervision.           symbolic proof search problem: given a model-
                                                            generated expression, we check whether it can be
Our approach builds on a long tradition of symbolic         derived from known assumptions using formally
verification in logic and mathematics, and adapts           defined rules. This enables both robust evaluation

                                                        2
      BLEU Score P(Y | do(X), Z) = P(Y | Z, do(X))                   Token-level F1 P(Y | do(X), Z) ≠ P(Y | X)
            Equivalent expressions but low BLEU score due to              Inequivalent expressions but high Token-level F1 score
      ❌           reordering and short expression bias
                                                                      ❌             since variables (tokens) are shared


      BERTScore              P(Y) ≠ P(Y | X)                         String match     P(Y | do(X), Z) = P(Y | Z)
           Inequivalent expressions but high BERTScore because              Equivalent expressions under some DAG fails to get
      ❌            tokens are close in embedding space
                                                                      ❌                recognized by string matching



Figure 2: Examples of evaluation failures in causal expression matching. Even logically equivalent expressions can
receive low scores due to surface-level differences (e.g., reordering), while inequivalent ones may score high due to
shared tokens or embeddings. Highlights the limitations of BLEU, token-level F1, BERTScore, and string match in
causal reasoning tasks.


and fine-grained error analysis.                                     the conditioning set Z may include both obser-
                                                                     vational variables and interventional terms of the
Formalization in Mathematical and Logical Rea-                       form do(X).
soning Efforts in mathematical reasoning have                           We write ϕ ⊢G ψ to denote that ψ is derivable
primarily focused on verifying answers to quan-                      from ϕ via a finite sequence of applications of do-
titative problems. For instance, Hendrycks et al.                    calculus and standard probability rules, while re-
(2021) evaluates LLMs on math competition prob-                      specting the conditional independencies entailed
lems, while Glazer et al. (2024) investigates sym-                   by G. The graph G encodes the causal structure,
bolic solvers for arithmetic tasks. To further val-                  which governs valid derivations and conditional
idate intermediate reasoning steps, another line                     independencies. We read ⊢ as entails.
of work (Ren et al., 2025; Wang et al., 2024) re-
sorts to formal math descriptions (de Moura and                      Problem Statement Given a causal DAG G ∈ G
Ullrich, 2021; Nipkow et al., 2002) that facilitate                  and two causal expressions ϕ, ψ ∈ Lcausal , we aim
the step-wise consistency inspection. Although                       to design a model
it is promising to formalize a math problem (Al-                                F : Lcausal × Lcausal × G → [0, 1],
phaProof and teams, 2024; Lin et al., 2025), check-
                                                                     that determines whether ϕ entails ψ under G, where
ing its semantic correctness is found crucial yet
                                                                     G denotes the space of causal DAGs. Formally, this
under evolving (Lu et al., 2024; Xin et al., 2025).
                                                                     corresponds to checking whether ϕ ⊢G ψ holds.
Recent work in geometry (Murphy et al., 2024) and
logic (Li et al., 2024) uses satisfiability modulo the-                 Motivating Example: Hidden Correctness
ories (SMT) solvers to assess logical equivalence
between informal text and formal theorems.                              From Figure 1, let

                                                                           ϕpred = P (F | do(C), do(A), do(B), D),
3     D OV ERIFIER: Causal Symbolic
      Verification Framework                                                   ψ = P (F | do(B)),

3.1     Preliminaries                                                   and let G be the following DAG:
Notation Let G = (V, E) denote a causal di-                                                           A             D
rected acyclic graph (DAG), where V is a finite
set of variables and E ⊆ V × V is the set of di-                           B          F
                                                                                                                     C
rected edges. We treat variables in V as symbolic
nodes in the causal graph, without assuming they                                           G                                       E
are necessarily directly observed in data.                              If F relies on exact match, then
   We define the language Lcausal as the set of ex-                     F(ϕpred , ψ, G) = 0. However, this is in-
pressions of the form P (Y | Z), where Y ⊆ V                            correct, since ϕpred ⊢G ψ holds: under G, F is
and Z ⊆ V ∪ {do(X) : X ⊆ V }. Throughout                                unaffected by interventions on A and C and is
the paper, we use Greek letters (e.g., ϕ, ψ, χ) to                      independent of D under do(B). Our goal is
denote elements of Lcausal , that is, symbolic causal                   to design a verification-based evaluator that
expressions.                                                            captures such equivalences more accurately.
   Here, Y denotes the outcome variable set, while

                                                                 3
   To determine whether ϕ ⊢G ψ holds, we rely on                             This allows us to replace an intervention
the rules of do-calculus and standard probability                            do(Z) with a simple observation, if Z be-
theory (Pearl, 1995). These rules define how causal                          haves like a non-manipulated variable under
expressions in Lcausal can be transformed while                              this graphical condition.
preserving validity under a given causal graph G.
Because causal expressions may involve interven-                       Rule 3 (Insertion/deletion of actions):
tions (via do(·)), entailment cannot be determined                            P (y | do(x), do(z), w) = P (y | do(x), w)
by surface-level syntactic matching alone, but de-
pends on the structure of G and the conditional                                             if (Y ⊥⊥ Z | X, W )GX Z(W )
independencies it encodes. Do-calculus provides                                                                        (3)
a sound and complete set of transformation rules
                                                                             This allows us to ignore an intervention on Z
for this purpose, and forms the basis of our veri-
                                                                             when it has no causal effect on Y , given the
fication framework. We now introduce the three
                                                                             rest of the variables.
do-calculus rules that underpin D OV ERIFIER and
specify when terms can be added to or removed                          Notation: Z(W ) denotes the subset of nodes in Z
from interventional distributions.                                     that are not ancestors of any node in W in the graph
                                                                       GX . We use GX Z(W ) to denote the graph obtained
The Rules of do-calculus Let X, Y, Z, and W be
arbitrary disjoint sets of nodes in a causal directed                  by removing incoming edges to X and to Z(W ).
acyclic graph (DAG) G 1 . Following the notation                       This restriction ensures that we remove only those
of Pearl (2012), we denote:                                            do-interventions that do not “leak” back into parts
                                                                       of the graph relevant to W . The notation (Y ⊥
   • GX the graph obtained from G by removing                          ⊥ Z | X, W )G represents d-separation in graph
     all the edges pointing to the nodes in X.                         G, meaning that all paths between Y and Z are
                                                                       blocked by conditioning on X and W .
   • GX the graph obtained by deleting all the
     edges emerging from the nodes in X.                               3.2   Method
                                                                       We define a symbolic verifier, D OV ERIFIER, for
   • GXZ the graph obtained by deleting edges                          assessing equivalence between causal expressions
     into X and out of Z.                                              derived from natural language. We first outline
                                                                       a set of desired properties for causal evaluation
Each rule applies only if a certain d-separation
                                                                       metrics in Section A, and later show why existing
condition holds in the modified graph.
                                                                       metrics fail to satisfy them. Given a DAG G (which
Rule 1 (Insertion/deletion of observations):                           may be generated by the model) and two expres-
                                                                       sions ϕpred , ψ ∈ Lcausal , D OV ERIFIER performs a
         P (y | do(x), z, w) = P (y | do(x), w)                        breadth-first search (BFS) starting from ϕpred over
                           if (Y ⊥
                                 ⊥ Z | X, W )GX (1)                    all expressions reachable by applying the rules in
                                                                       R.
      This allows us to add or remove observed vari-                      In the resulting derivation graph, each node cor-
      ables Z from the conditioning set if they are                    responds to a well-formed causal expression, and
      irrelevant to Y once X and W are known (af-                      each directed edge corresponds to a valid rule ap-
      ter intervention X).                                             plication. All transformation rules in R are unary
                                                                       rewrites mapping a single causal expression to a
Rule 2 (Action/observation exchange):                                  single expression. Consequently, derivations cor-
                                                                       respond to linear sequences rather than branching
      P (y | do(x), do(z), w) = P (y | do(x), z, w)                    proof trees. A sequence of rule applications
                                if (Y ⊥
                                      ⊥ Z | X, W )GXZ
                                                                                       Ri1
                                                                                                Ri
                                                                                                2
                                                                                                         Ri
                                                                                                          k
                                                            (2)                  ϕpred −−→ ϕ1 −−→ . . . −−→ ϕk         (4)
    1
      In do-calculus, X, Y , Z, and W are disjoint sets of vari-       represents a single path in this graph. If ϕk = ψ,
ables representing interventions (X), outcomes (Y ), observed          the verifier declares equivalence; otherwise, the
variables (Z), and other variables (W ). These sets can be
empty, allowing the rules to generalize to many causal infer-          search continues until no new expressions can be
ence scenarios.                                                        generated under the given rules and depth limit, or

                                                                   4
until a previously visited expression is encountered.       concerns the soundness and completeness of the
Because each rule in R corresponds to a sound               verification algorithm:
transformation under the causal semantics of G,             Proposition 3.2 (Soundness & Completeness of
any successful derivation certifies a valid equiva-         Proof Search). Let G be a causal DAG, and let
lence. Moreover, since the search systematically            ϕ, ψ ∈ Lcausal . If ϕ ⊢G ψ, then Algorithm 1 re-
explores all possible rule applications without rep-        turns a valid proof sequence within depth d, for
etition, it is complete for a finite R and variable         some finite d. Conversely, if no such derivation
set. Details of the preprocessing and normaliza-            exists within depth d, Algorithm 1 returns None. If
tion steps, as well as implementation specifics, are        the depth bound is removed and cycle detection is
provided in Section B.                                      enforced, the verifier is both sound and complete.
3.3   Theoretical Guarantees of D OV ERIFIER                  Proof. Proved in Section D.                     ■
In this section, we establish the theoretical founda-
tions of D OV ERIFIER. We first analyze the sound-             In addition, if no derivation exists between ϕ
ness and completeness of the verification algorithm,        and ψ with k ≤ d steps, breadth-first search (BFS)
and then show that derivability in our system cor-          will terminate after exploring all expressions within
responds exactly to semantic correctness under              depth d. Further practical considerations are ex-
causal semantics. We begin by introducing formal            plained in Section E.
notations that support these proofs. These guaran-             While the above result establishes soundness
tees ensure that verified expressions are not merely        and completeness of the verification algorithm as
heuristically plausible, but formally correct under         a bounded proof search procedure, it does not yet
causal semantics. Soundness ensures that every              guarantee that proof search corresponds to seman-
equivalence established by D OV ERIFIER is valid;           tic correctness of causal expressions. To justify
completeness ensures that if an equivalence exists          using derivability as an evaluation criterion, we ad-
between two expressions, D OV ERIFIER will find it.         ditionally view D OV ERIFIER as a logical system
First, we model causal equivalence as a reachability        defined over a formal language Lcausal , equipped
problem in a derivation graph:                              with a set of derivation rules R and a background
                                                            causal model G (the DAG), which may be provided
Proposition 3.1 (Derivation Graph). Let ϕ ∈
                                                            or generated by an LLM. In this logical view, we
Lcausal . Define a directed graph S(ϕ) as follows:
                                                            distinguish between:
   • Each node corresponds to a unique causal
     expression derivable from ϕ;                           Syntactic entailment (H ⊢G ψ): ψ is derivable
                                                                from the hypothesis H = {G, ϕ} using the
   • A directed edge ϕ → ϕ′ exists if ϕ′ can be                 symbolic transformation rules admissible un-
     obtained from ϕ by applying a single valid                 der the causal graph.
     transformation rule.
                                                            Semantic entailment (H |=G ψ): ψ is true in all
Then S(ϕ) is a well-defined, finite-branching                  causal models consistent with G in which all
graph.                                                         assumptions in H hold.
   The branching factor is finite since the number
                                                            In simple terms, syntactic entailment asks whether
of variables in G is finite and each transformation
                                                            one expression can be transformed into another
rule applies only to bounded subsets of variables.
                                                            using the allowed symbolic rules, while semantic
   Proof. Proved in Section C.                   ■
                                                            entailment asks whether the two expressions repre-
                                                            sent the same causal quantity under the given graph.
Verification Algorithm Given a causal graph G,              The former is a property of the derivation system,
source expression ϕ, target expression ψ, and max-          whereas the latter is a property of the underlying
imum depth d, we present Algorithm 1 as an algo-            causal semantics.
rithm to verify if ϕ and ψ are equivalent bounded              We require our inference system to satisfy the
by depth d.                                                 following properties:
   This approach guarantees finding the shortest
sequence of transformations if one exists within                     Soundness: H ⊢G ψ ⇒ H |=G ψ,
the depth limit, as stated in our main theorem that              Completeness: H |=G ψ ⇒ H ⊢G ψ.

                                                        5
These properties are properties of the underlying              Model                  Exact    LLM      D OV ERIFIER
logical system rather than the verification algorithm          Llama3.1-8B             0.57     0.60        0.73
itself, and are satisfied due to the completeness of           Mistral-7B              0.58     0.80        0.94
                                                               Llama3.1-8B-Instruct    0.88     0.66        0.90
do-calculus for causal identifiability (Pearl, 1995)           Gemma-7B-it             0.80     0.58        0.84
together with the standard axioms of probability
theory. As a result, semantic correctness of model-           Table 1: D OV ERIFIER recovers more semantically cor-
generated causal expressions can be verified equiv-           rect causal expressions than exact string match or LLM-
alently through syntactic derivation, which forms             based judging across four LLMs on CLadder. Accuracy
the theoretical basis of our verifier.                        is measured with respect to formal derivability under
   This equivalence is crucial for evaluation: it guar-       the causal graph.
antees that checking derivability via proof search is
sufficient to determine semantic correctness under              We first construct a base expression
the given causal graph.
                                                               ϕ = P (Y | do(X1 ), . . . , do(Xk ), Z1 , . . . , Zm ) ,
4     Experiments and Results                                                                                       (5)

We evaluate our verifier in two settings.                     where Y ∈ V is chosen uniformly at random. A
                                                              subset of V \ {Y } is sampled as intervention vari-
   Synthetic Data. This setting enables precise
                                                              ables {Xi }, and an additional subset is sampled
control over the graph structure, derivation path,
                                                              as observational conditioning variables {Zj }. To
and rule usage. It allows us to test whether the
                                                              ensure structural diversity, the numbers of interven-
verifier behaves correctly under known conditions,
                                                              tional variables k and observational variables m
and whether it can recover known valid derivations.
                                                              are randomly chosen for each sample, subject to
   LLM Causal Reasoning. This setting evaluates
                                                              DAG constraints.
the verifier’s practical utility in assessing causal
                                                                 We then sample a sequence of ℓ rule applications
reasoning in free-form LLM outputs. Here, we
                                                              ⟨r1 , . . . , rℓ ⟩ and apply them sequentially,
test whether the verifier can recognize semantically
                                                                              1r    2   r    ℓ    r
correct answers that would be missed by surface-                           ϕ −→ ϕ1 −→ . . . −→ ψ,                  (6)
level metrics such as string match.
                                                              where each ri ∈ {Rule 1, Rule 2, Rule 3} ∪ P.
4.1    Synthetic Data Test                                    Rule applications are randomized but constrained
                                                              to be valid under the conditional independencies
To verify the internal consistency of the verifier,           implied by G. We treat the initial expression as ϕ
and to show that existing metrics fail in cases where         and the final expression as ψ.
syntactically different expressions are the same se-             The mean number of edges in sampled graphs is
mantically, we construct a synthetic dataset of over          7 (minimum 3, maximum 10). Rule 1 was applied
10,000 expression pairs (ϕ, ψ) such that ψ is prov-           21,172 times, Rule 2 was applied 29,563 times,
ably derivable from ϕ under a known DAG G. Each               and Rule 3 was applied 22,508 times.
pair involves between 1–4 rule applications and
includes randomized use of do-calculus and prob-              Synthetic Data Performance Our symbolic veri-
ability rules P. A description of data samples is             fier achieves 100% precision and recall under depth
shown in Section F.                                           limit d = 5, demonstrating correctness of the
                                                              derivation engine, while other methods such as
Sampling Procedure Let V = {v1 , . . . , vn } be              string match, or token-level F1 performed poorly
a finite set of variables, and let G = (V, E) be              due to ϕ and ψ being too distinct syntactically.
a randomly sampled acyclic graph. We sample                      The experimental results show a key strength of
directed edges independently according to                     our framework: it can correctly recognize when
                                                              two expressions are equivalent under the rules of
            P(vi → vj ) = p     for i < j,                    do-calculus and probability, even if they differ in
                                                              formatting, variable order, or surface form.
where p ∈ (0, 1) is the edge probability. The im-
posed ordering ensures that the resulting graph is            4.2   LLM Causal Reasoning Test
acyclic. In our experiments, we fix n ≤ 10 and                Uncovering Missed Correct Answers We eval-
p = 0.5 to balance expressivity and tractability.             uate the ability of our symbolic verifier to improve

                                                          6
the accuracy of large language model (LLM) eval-            evaluation due to superficial differences in format-
uation in causal reasoning. Specifically, we ask:           ting, variable order, or phrasing. The running time
Can our method recover correct answers that are             of verifying through BFS is minimal (milliseconds),
missed by naive evaluation metrics?                         and the formalization step is relatively stable.
                                                               Our symbolic verifier recovers this missing ac-
Evaluated Dataset and Models To investigate
                                                            curacy by judging expressions based on their se-
this, we use the CLadder benchmark (Jin et al.,
                                                            mantic content, not their surface form. It enables
2023), a suite of causal questions grounded in
                                                            a more faithful and rigorous assessment of causal
known DAGs. Each question is paired with a
                                                            reasoning in LLMs, ensuring that models receive
ground-truth answer expressed as a formal causal
                                                            credit for valid reasoning even when their output
expression. We prompt Llama-3-8B (Grattafiori
                                                            does not match the reference verbatim.
et al., 2024), Llama-3-8BInstruct (Grattafiori
                                                               When high-performing models such as
et al., 2024), Mistral-7B (Jiang et al., 2023), and
                                                            Llama3.1-Instruct already align well with the
Gemma-7B-IT (Team et al., 2024) to answer these
                                                            ground-truth format, the relative gain over string
questions and parse their responses, including a
                                                            match is naturally smaller. This suggests that the
DAG that models the problem into symbolic ex-
                                                            benefit of symbolic evaluation is most pronounced
pressions. Detailed prompts and parsing are demon-
                                                            when models exhibit partial causal understanding
strated in Section G. Because CLadder provides a
                                                            but struggle with precise formalization. In addition,
canonical mapping from natural-language descrip-
                                                            CLadder instances involve only a small number
tions to variable symbols and uses a constrained
                                                            of variables, limiting the number of distinct but
expression format, the formalization step is stable
                                                            semantically valid expressions. As graph size
in this setting; we discuss formalization assump-
                                                            increases, the space of equivalent causal expres-
tions and edge cases in Section H. Each prediction
                                                            sions grows rapidly, and correctness becomes less
is then compared to the ground-truth using three
                                                            about producing a single canonical form than
metrics:
                                                            about remaining within a large equivalence class.
   • String Match: A response is marked correct             In this regime, surface-level metrics increasingly
     only if it matches the ground-truth expression         conflate formatting variation with reasoning errors.
     exactly (after normalizing).                           Furthermore, when using LLM-as-a-judge, we lose
                                                            the soundness guarantee that both string match and
   • LLM-as-a-judge: We provide the generated               D OV ERIFIER provide2 . We also hypothesize that
     causal expression, generated causal graph,             including the DAG in LLM-as-a-judge prompts
     and the ground truth expression for OpenAI’s           may act as a source of noise, leading the model
     GPT-4o (OpenAI, 2024) to determine if the              to overinterpret structural cues and misjudge
     two expressions are equivalent.                        otherwise valid expressions.
                                                               We identified several common patterns where
   • Symbolic (Ours): A response is considered
                                                            symbolic verification offers substantial advantages:
     correct if it is derivable from the ground-truth
     using valid applications of do-calculus and
     probability rules (under 20 steps).                    Intervention with conditioning: Our system val-
                                                                 idates equivalence between expressions like
  Alternative metrics are discussed in Section I.                P (Y | do(X), Z = z) and P (Y | do(X), Z)
                                                                 by correctly handling instantiated versus sym-
Results As shown in Table 1, our symbolic                        bolic values.
method identifies more correct answers than string
match and LLM-as-a-judge, raising the accuracy              Rule-based transformations: Our system cor-
across all models. We find that a substantial frac-             rectly identifies that P (Y | do(X), Z) can
tion of model outputs marked incorrect by string                be transformed into P (Y | X, Z) in DAGs
match are in fact causally valid under the given                where Z d-separates Y from incoming edges
DAG. Our method is more useful when models                      of X. This conversion from interventional to
such as Llama3.1-8b and Mistral-7B output an                    observational queries represented the majority
alternative form of the correct use. This improve-              of all verified equivalences. Note that this is
ment highlights an important phenomenon: many
                                                               2
model responses are causally correct but fail naive                While string match is sound, it is not complete.


                                                        7
      important since the ground-truth of CLadder                     Model                  Before Feedback   After Feedback
      is in observational queries.                                    LLaMA3.1-8B                 0.73              0.93
                                                                      Mistral-7B                  0.94              0.99
Multi-step proofs: For more complex cases, our                        LLaMA3.1-8B-Instruct        0.90              0.98
                                                                      Gemma-7B-it                 0.84              0.87
    verifier successfully applied sequential rules.
    These accounted for fewer verified equiva-                       Table 2: Accuracy before and after applying verifier-
    lences but are representative of some of the                     guided feedback. Feedback improves semantic correct-
    most challenging verification scenarios.                         ness across all models.
4.3   Improving LLMs with Symbolic Feedback
Beyond evaluation, D OV ERIFIER provides sym-                            2. Treatment Confounding: If Z ∈ Zobs is a
bolic feedback3 at inference time to improve LLM-                           common cause of both a treatment variable
generated causal expressions without access to                              X ∈ Xdo and the outcome Y , that is,
ground-truth answers. The feedback relies solely
on the predicted causal graph and the model output,                                   Z→X         and    Z → Y,             (9)
and is designed to correct violations of do-calculus
semantics rather than errors in question interpreta-                       then Z is a confounder. In such cases, we sug-
tion or graph construction. Prior work has shown                           gest replacing Z with do(Z) when feasible,
that symbolic feedback loops (e.g., SMT-based ver-                         since intervening on Z may help eliminate
ification in mathematics and logic) can improve                            confounding bias, particularly when front-
LLM accuracy by providing formal, structured cor-                          door adjustment is applicable.
rections (Hong et al., 2025; Murphy et al., 2024).                       3. d-Separation Violation: Let
   The feedback experiment is intended as a proof
of concept; improvements may partially reflect                                      W = (Zobs \ {Z}) ∪ Xdo .               (10)
generic re-prompting effects rather than the sym-
bolic content of the verifier alone, which we leave                        If X ̸⊥⊥ Y | W, then conditioning on Z may
to future ablations.                                                       introduce bias, since Z is not independent of
                                                                           Y given the remaining variables W.
Formal Description of Feedback Loop Given a
causal graph G = (V, E) (potentially generated by                       Each diagnostic message is appended verbatim
an LLM) and an LLM-generated expression                              to the original prompt and the model is re-queried
          ϕLLM = P (Y | do(Xdo ), Zobs ) ,                (7)        once. The exact feedback strings and formal checks
                                                                     are provided in Section J.
with no access to the ground-truth target ψ, our
goal is to compute a revised expression ϕ′LLM that                   Results Table 2 shows the improvement of LLM
is causally more valid (i.e., more likely to match                   performance using our feedback loop. We find that
ψ) using structural reasoning over G.                                the effectiveness of symbolic feedback depends
   Here, Xdo ⊆ V denotes the interventional vari-                    heavily on the type of error in the original expres-
ables and Zobs ⊆ V the observational conditioning                    sion. For example, when the model incorrectly uses
variables. For each variable Z ∈ Zobs , we test:                     P (Y | X) instead of P (Y | do(X)), feedback
                                                                     guided by d-separation and rule-based reasoning
  1. Mediator Detection: If Z lies on a directed                     often corrects the mistake. In contrast, if the model
     path from some ancestor A ∈ Zobs ∪ Xdo to                       hallucinates an irrelevant variable or misrepresents
     the outcome Y ,                                                 the structure of the DAG itself, our framework is
                 A → · · · → Z → · · · → Y,               (8)        less effective since the symbolic transformations
                                                                     cannot fix structurally flawed inputs.
      then Z is a mediator. In this case, we prompt
      the model to avoid conditioning on Z, since                    5     Discussions
      doing so may block part of the causal path-
      way and lead to underestimation of the causal                  Interpreting evaluation results for causal reason-
      effect.                                                        ing requires distinguishing between surface-level
    3
                                                                     variation and genuine semantic error in language
      In formal methods, verifiers typically return diagnostic
information such as violated constraints rather than a binary        model outputs. Symbolic verification provides a
signal.                                                              principled way to make this distinction explicit by

                                                                 8
grounding evaluation in causal semantics rather             variation from substantive semantic error. By mak-
than surface form. In doing so, it clarifies what it        ing failure conditions explicit, symbolic verifica-
means for an output to be causally correct, when            tion provides a principled way to identify when a
deviations reflect true violations of causal assump-        model’s output reflects genuinely incorrect causal
tions, and why sound but incomplete verification            reasoning, rather than merely an alternative expres-
can nevertheless be effective for practical evalua-         sion of the correct answer.
tion.
Semantic Equivalence as Proof-Theoretic                     Scalability and Practical Scope A common con-
Reachability From an NLP evaluation perspec-                cern with formal verification methods is scalability:
tive, causal correctness is inherently a property of        complete equivalence checking in expressive sym-
equivalence classes rather than individual surface          bolic languages can be computationally expensive
forms. We formalize this by defining semantic               or even undecidable in the worst case, leading to
equivalence with respect to a causal graph G as             the perception that such methods apply only to “toy”
mutual derivability:                                        problems. Indeed, this becomes a tradeoff between
                                                            completeness and speed. In the context of evalu-
   ϕ ≡G ψ ⇐⇒ (ϕ ⊢G ψ ∧ ψ ⊢G ϕ).                 (11)        ation, this tradeoff is often acceptable. Even an
                                                            incomplete but sound verifier can recover a sub-
This definition groups expressions into equivalence
                                                            stantial amount of “hidden correctness” missed by
classes [ϕ]≡G ⊂ Lcausal , each representing a single
                                                            surface-level metrics, and can provide precise, rule-
causal quantity under G.
                                                            level diagnostic feedback when verification fails.
   Empirically, we find that LLM-generated outputs
                                                            As problem size grows (e.g., larger graphs or longer
often belong to the correct equivalence class while
                                                            expressions), practical techniques such as canoni-
differing syntactically from reference answers. For
                                                            calization, memoization of visited expressions, and
example, P (Y | X, Z) and P (Y | do(X), Z) may
                                                            heuristic or learned rule ordering can improve cov-
be lexically distinct but semantically equivalent un-
                                                            erage under fixed compute, while preserving sound-
der appropriate d-separation conditions. Our sym-
                                                            ness. Formal properties of bounded proof search
bolic verifier captures this distinction by checking
                                                            are discussed in the Section K.
derivability rather than string identity.
Failure Types Align with Non-derivability Al-               6   Conclusion
though many apparent errors arise from surface-
form variation, our framework also makes explicit
                                                            We introduced D OV ERIFIER, a formal verifica-
when an LLM output is genuinely causally in-
                                                            tion approach that evaluates the causal validity of
correct. Common failure modes in causal QA
                                                            LLM-generated expressions by modeling causal
benchmarks, such as conditioning on colliders or
                                                            reasoning as a symbolic derivation task using do-
omitting required adjustments, correspond to cases
                                                            calculus and probability rules. Our approach recov-
where no valid symbolic derivation exists under the
                                                            ers semantically correct answers that are missed by
causal graph. These outputs therefore lie outside
                                                            standard metrics, improves recall on causal bench-
the correct semantic equivalence class, rather than
                                                            marks, and enables structured feedback to refine
being alternative but valid formulations.
                                                            model outputs.
   For example, when
                                                               These findings reveal a significant gap in current
                 (Y ̸⊥
                     ⊥ Z | X)GX ,               (12)        evaluation methods for language-based causal rea-
                                                            soning and highlight the importance of symbolic
we have                                                     verification for building reliable causal reasoning
     P (Y | X, Z) ̸≡G P (Y | do(X), Z).         (13)        systems. By connecting natural language genera-
                                                            tion with formal inference, D OV ERIFIER offers a
In such cases, symbolic verification fails not be-          principled step toward evaluating models based on
cause of lexical mismatch, but because the model’s          what they truly understand rather than how they
reasoning violates core causal independence as-             phrase it. As language model outputs increasingly
sumptions.                                                  involve symbolic and causal structure, evaluation
   From an NLP evaluation perspective, this dis-            must move beyond surface similarity toward se-
tinction is critical as it separates benign surface         mantic verification.

                                                        9
Limitations                                                  cisions. We caution against interpreting verified
                                                             expressions as endorsements of correctness in real-
While promising, our approach has several limi-
                                                             world applications without domain expertise. To
tations and opens directions for future work. On
                                                             avoid misuse, we release our tools with clear dis-
the one hand, the space of valid derivations can
                                                             claimers that they are intended for research and
grow rapidly with the number of variables and the
                                                             educational purposes.
depth of allowed transformations. Although we
employ optimizations like expression normaliza-              Acknowledgments
tion and memoization, our breadth-first search re-
mains computationally expensive in dense or deep             We thank Dominik Janzing for helpful discussions
DAGs. Future work could explore neural-guided                that clarified aspects of this work. Resources used
proof search or approximate symbolic methods.                in preparing this research were provided, in part,
On the other hand, regarding the feedback mech-              by the Province of Ontario, the Government of
anism, the current feedback module improves the              Canada through CIFAR, and companies sponsor-
causal validity of model outputs using only the              ing the Vector Institute www.vectorinstitute.
predicted DAG and the initial expression. It does            ai/partnerships/. This research was supported
not incorporate the original natural language ques-          by the ETH AI Center through an ETH AI Center
tion. As a result, the revised expression may be             postdoctoral fellowship to Yinya Huang.
causally correct under the graph, but not necessar-
ily faithful to the question intent. In practice, we
observe that most LLM errors stem from misap-                References
plying causal semantics rather than misreading the           AlphaProof and AlphaGeometry teams. 2024.
question, but integrating question-aware feedback              Ai achieves silver-medal standard solving in-
                                                               ternational mathematical olympiad problems.
remains a valuable direction for future work. Fur-             https://deepmind.google/discover/blog/ ai-solves-
thermore, some recent frontier models can achieve              imo-problems-at-silver-medal-level/.
near-ceiling performance on causal benchmarks
such as CLadder, which involve only a few vari-              Alexander Bondarenko, Magdalena Wolska, Ste-
                                                               fan Heindorf, Lukas Blübaum, Axel-Cyrille
ables and limited syntactic variation. In such set-            Ngonga Ngomo, Benno Stein, Pavel Braslavski,
tings, surface-level metrics may appear sufficient,            Matthias Hagen, and Martin Potthast. 2022.
even though they fail to capture semantic equiva-              CausalQA: A benchmark for causal question
lence in more complex regimes. Evaluating how                  answering. In Proceedings of the 29th Interna-
                                                               tional Conference on Computational Linguistics,
semantic verification behaves as both model capac-
                                                               pages 3296–3308, Gyeongju, Republic of Ko-
ity and graph size increase is an important direction          rea. International Committee on Computational
for future work.                                               Linguistics.

Ethical Considerations                                       Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
                                                               Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
This work focuses on the formal verification of                Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
                                                               Nakano, Christopher Hesse, and John Schulman.
causal expressions generated by large language
                                                               2021. Training verifiers to solve math word prob-
models (LLMs), with the goal of improving their                lems. CoRR, abs/2110.14168.
semantic correctness and reliability in reasoning
tasks. Our proposed framework does not involve               Leonardo de Moura and Sebastian Ullrich. 2021. The
                                                               lean 4 theorem prover and programming language.
human subject data, personally identifiable infor-
                                                               In Automated Deduction - CADE 28 - 28th Interna-
mation, or real-world deployment in high-stakes                tional Conference on Automated Deduction, Virtual
settings such as healthcare or public policy. How-             Event, July 12-15, 2021, Proceedings, volume 12699
ever, we acknowledge that causal claims can in-                of Lecture Notes in Computer Science, pages 625–
fluence decision-making in sensitive domains. As               635. Springer.
such, we emphasize that symbolic correctness un-             DeepSeek-AI. 2025. Deepseek-r1: Incentivizing rea-
der do-calculus does not guarantee practical va-               soning capability in llms via reinforcement learning.
lidity unless the underlying causal graph is itself            Preprint, arXiv:2501.12948.
accurate and contextually appropriate.                       Finale Doshi-Velez and Been Kim. 2017. Towards a
   Our framework is designed for evaluation and                rigorous science of interpretable machine learning.
diagnostic purposes, not for automating causal de-             Preprint, arXiv:1702.08608.


                                                        10
Jingxuan Fan, Sarah Martinson, Erik Y. Wang, Kaylie             Zenan Li, Yifan Wu, Zhaoyu Li, Xinming Wei, Xian
   Hausknecht, Jonah Brenner, Danxian Liu, Nianli                 Zhang, Fan Yang, and Xiaoxing Ma. 2024. Autofor-
   Peng, Corey Wang, and Michael Brenner. 2024.                   malize mathematical statements by symbolic equiva-
   HARDMATH: A benchmark dataset for challeng-                    lence and semantic consistency. In The Thirty-eighth
   ing problems in applied mathematics. In The 4th                Annual Conference on Neural Information Process-
   Workshop on Mathematical Reasoning and AI at                   ing Systems.
   NeurIPS’24.
                                                                Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu,
Bofei Gao, Feifan Song, Zhe Yang, Zefan Cai, Yibo                 Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou Xia,
  Miao, Qingxiu Dong, Lei Li, Chenghao Ma, Liang                  Danqi Chen, Sanjeev Arora, and Chi Jin. 2025.
  Chen, Runxin Xu, Zhengyang Tang, Benyou Wang,                   Goedel-prover: A frontier model for open-source
  Daoguang Zan, Shanghaoran Quan, Ge Zhang, Lei                   automated theorem proving. CoRR, abs/2502.07640.
  Sha, Yichang Zhang, Xuancheng Ren, Tianyu Liu,
  and Baobao Chang. 2025. Omni-MATH: A univer-                  Jianqiao Lu, Yingjia Wan, Yinya Huang, Jing Xiong,
  sal olympiad level mathematic benchmark for large                Zhengying Liu, and Zhijiang Guo. 2024. For-
  language models. In The Thirteenth International                 malalign: Automated alignment evaluation for auto-
  Conference on Learning Representations.                          formalization. CoRR, abs/2410.10135.
Elliot Glazer, Ege Erdil, Tamay Besiroglu, Diego                Logan Murphy, Kaiyu Yang, Jialiang Sun, Zhaoyu Li,
   Chicharro, Evan Chen, Alex Gunning, Caroline Falk-             Anima Anandkumar, and Xujie Si. 2024. Autofor-
   man Olsson, Jean-Stanislas Denain, Anson Ho,                   malizing euclidean geometry. In Forty-first Interna-
   Emily de Oliveira Santos, Olli Järviniemi, Matthew             tional Conference on Machine Learning.
   Barnett, Robert Sandler, Matej Vrzala, Jaime Sevilla,
   Qiuyu Ren, Elizabeth Pratt, Lionel Levine, Grant             Tobias Nipkow, Lawrence C. Paulson, and Markus Wen-
   Barkley, Natalie Stewart, Bogdan Grechuk, Tetiana              zel. 2002. Isabelle/HOL - A Proof Assistant for
   Grechuk, Shreepranav Varma Enugandla, and Mark                 Higher-Order Logic, volume 2283 of Lecture Notes
  Wildon. 2024. Frontiermath: A benchmark for                     in Computer Science. Springer.
   evaluating advanced mathematical reasoning in ai.
   Preprint, arXiv:2411.04872.                                  OpenAI. 2024. Hello gpt-4o. Accessed: 2025-04-30.

Aaron Grattafiori et al. 2024. The llama 3 herd of mod-         Kishore Papineni, Salim Roukos, Todd Ward, and Wei-
  els. Preprint, arXiv:2407.21783.                                Jing Zhu. 2002. Bleu: a method for automatic evalu-
                                                                  ation of machine translation. In Proceedings of the
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul                40th Annual Meeting of the Association for Compu-
  Arora, Steven Basart, Eric Tang, Dawn Song, and                 tational Linguistics, pages 311–318, Philadelphia,
  Jacob Steinhardt. 2021. Measuring mathematical                  Pennsylvania, USA. Association for Computational
  problem solving with the MATH dataset. In Thirty-               Linguistics.
  fifth Conference on Neural Information Processing
  Systems Datasets and Benchmarks Track.                        Judea Pearl. 1995. Causal diagrams for empirical re-
                                                                  search. Biometrika, 82(4):669–688.
Sungee Hong, Zhengling Qi, and Raymond K. W.
  Wong. 2025. Distributional off-policy evaluation              Judea Pearl. 2012. The do-calculus revisited. In Pro-
  with bellman residual minimization. Preprint,                   ceedings of the Twenty-Eighth Conference on Uncer-
  arXiv:2402.01900.                                               tainty in Artificial Intelligence, UAI’12, page 3–11,
Taojun Hu and Xiao-Hua Zhou. 2024. Unveiling llm                  Arlington, Virginia, USA. AUAI Press.
  evaluation focused on metrics: Challenges and solu-
                                                                ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin,
  tions. Preprint, arXiv:2404.09135.
                                                                  Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe
Albert Q. Jiang et al. 2023. Mistral 7b. Preprint,                Fu, Qihao Zhu, Dejian Yang, et al. 2025. Deepseek-
  arXiv:2310.06825.                                               prover-v2: Advancing formal mathematical reason-
                                                                  ing via reinforcement learning for subgoal decompo-
Zhijing Jin, Yuen Chen, Felix Leeb, Luigi Gresele,                sition. arXiv preprint arXiv:2504.21801.
  Ojasv Kamal, Zhiheng LYU, Kevin Blin, Fernando
  Gonzalez Adauto, Max Kleiman-Weiner, Mrinmaya                 Ivaxi Sheth, Bahare Fatemi, and Mario Fritz. 2025.
  Sachan, and Bernhard Schölkopf. 2023. Cladder:                   CausalGraph2LLM: Evaluating LLMs for causal
  Assessing causal reasoning in language models. In                queries. In Findings of the Association for Computa-
  Advances in Neural Information Processing Systems,               tional Linguistics: NAACL 2025, pages 2076–2098,
  volume 36, pages 31038–31065. Curran Associates,                 Albuquerque, New Mexico. Association for Compu-
  Inc.                                                             tational Linguistics.
Nitish Joshi, Abulhair Saparov, Yixin Wang, and He He.          Ilya Shpitser and Judea Pearl. 2008. Complete identifi-
  2024. LLMs are prone to fallacies in causal inference.           cation methods for the causal hierarchy. Journal of
  In Proceedings of the 2024 Conference on Empiri-                 Machine Learning Research, 9(64):1941–1979.
  cal Methods in Natural Language Processing, pages
  10553–10569, Miami, Florida, USA. Association for             Gemma Team. 2025. Gemma 3 technical report.
  Computational Linguistics.                                      Preprint, arXiv:2503.19786.


                                                           11
Gemma Team et al. 2024. Gemma: Open models                     Desideratum 1 (Syntactic Invariance). Let D
  based on gemini research and technology. Preprint,           be a derivation and D′ a derivation obtained by a
  arXiv:2403.08295.
                                                               sequence of syntactic equivalences to the interme-
Santtu Tikka, Antti Hyttinen, and Juha Karvanen. 2021.         diate steps. Then:
  Causal effect identification from multiple incomplete
  data sources: A general search-based approach. Jour-                           s(D) = s(D′ )                 (15)
  nal of Statistical Software, 99(5):1–40.

Haiming Wang, Huajian Xin, Chuanyang Zheng,                    Definition (Well-Typed Step). A step
  Zhengying Liu, Qingxing Cao, Yinya Huang, Jing               ϕi      →      ϕi+1 using do-calculus Rule
  Xiong, Han Shi, Enze Xie, Jian Yin, Zhenguo Li, and          r ∈ {Rule1, Rule2, Rule3} is valid if and
  Xiaodan Liang. 2024. LEGO-prover: Neural theo-
  rem proving with growing libraries. In The Twelfth           only if the required graphical conditional indepen-
  International Conference on Learning Representa-             dence is entailed by DAG G associated with the
  tions.                                                       problem.

Zeyu Wang. 2024. Causalbench: A comprehensive                  Desideratum 2 (Rule Sensitivity). If D and D′
  benchmark for evaluating causal reasoning capabil-
  ities of large language models. In Causality and             differ only in that D′ includes a rule application r
  Large Models @NeurIPS 2024.                                  that violates the required independence, then:

Huajian Xin, Luming Li, Xiaoran Jin, Jacques Fleuriot,                           s(D′ ) < s(D)                 (16)
  and Wenda Li. 2025. Ape-bench i: Towards file-level
  automated proof engineering of formal math libraries.
  arXiv preprint arXiv:2504.19110.                             This ensures the evaluator penalizes logically in-
                                                               valid or unsound reasoning.
Tianyi Zhang*, Varsha Kishore*, Felix Wu*, Kilian Q.
  Weinberger, and Yoav Artzi. 2020. Bertscore: Eval-           Definition (Commutativity of Independent
   uating text generation with bert. In International
  Conference on Learning Representations.                      Steps). Consider two derivation steps ϕi → ϕi+1
                                                               and ϕj → ϕj+1 that apply valid rules to disjoint
A    Desired Properties of a Good Verifier                     subexpressions of a causal expression. Two deriva-
                                                               tions are said to be commutative if they differ only
A central question in the design of verifiers for sym-         in the order in which these independent steps are
bolic causal reasoning is: what kinds of differences           applied.
between derivations should not affect the evalua-
tion? In other words, what transformations should              Desideratum 3 (Invariance to Independent Step
a good evaluator be invariant to. In this section,             Order). If two derivations differ only by the or-
we formalize the invariance and sensitivity prop-              dering of commutative independent steps, the eval-
erties that an ideal evaluator should satisfy. These           uator should assign them the same score. This
properties are motivated both by formal semantics              ensures that evaluation is not sensitive to arbitrary
and by practical considerations in modeling causal             ordering choices among logically independent rule
reasoning.                                                     applications.
   Given an initial expression ϕ0 , a target ex-
pression ϕ⋆ , and a derivation sequence D =                    Definition (Derivational Equivalence). Let D1
(ϕ0 , ϕ1 , . . . , ϕk = ϕ⋆ ), the evaluator should as-         and D2 be distinct derivations from ϕ0 to ϕ⋆ such
sign a score s(D) ∈ R that reflects the logical                that all steps in both derivations are valid under
correctness, minimality, and interpretability of the           the causal graph, although they may differ in the
derivation.                                                    choice or order of applied rules.

Definition (Syntactic Equivalence). Let ϕ and                  Desideratum 4 (Robustness to Valid Alterna-
ϕ′ be probability expressions. We write ϕ ≡syn                 tives). The evaluator should treat derivationally
ϕ′ if they differ only by a syntactic permutation              equivalent sequences as equally correct, assigning
that preserves semantic content, such as reordering            similar scores to alternative but valid reasoning
terms in a conditioning set:                                   paths. This prevents penalizing models for produc-
                                                               ing different symbolic derivations that nevertheless
         P (Y | X, Z) ≡syn P (Y | Z, X)           (14)         correspond to the same causal semantics.

                                                          12
Algorithm 1 Causal Expression Equivalence Veri-                • Recognizing both observational terms like
fication                                                         P (Y | X) and interventional ones like P (Y |
  1: Initialize queue Q ← [(ϕ, [])] ▷ (expression,               do(X), Z).
     proof path π)
                                                               • Converting string-based expressions into a
  2: Initialize visited set V ← {ϕ}
                                                                 canonical symbolic form using a custom
  3: while Q not empty do
                                                                 SymPy-based object4 that allows equivalence
  4:     (ϕcur , π) ← Q.dequeue()
                                                                 checks that are invariant to variable reordering
  5:     if ϕcur = ψ then
                                                                 or formatting.
  6:          return π            ▷ Found derivation
  7:     end if                                                • If a causal graph is provided, it is parsed into
  8:     if |π| < d then                                         a standard NetworkX 5 DAG object.
  9:          for each applicable rule r do
 10:              ϕnext ← apply(r, ϕcur )                   This step is necessary to interface LLM outputs
 11:              if ϕnext ∈
                           / V then                         with our proof search module.
 12:                  V.add(ϕnext )                         Causal Graph Representation Causal graphs
 13:                  Q.enqueue((ϕnext , π + [r]))          are represented using NetworkX directed graphs,
 14:              end if                                    where nodes correspond to variables and edges rep-
 15:          end for                                       resent causal relationships. For each rule applica-
 16:     end if                                             tion, we create modified graph structures according
 17: end while                                              to the do-calculus definitions:
 18: return None        ▷ No derivation found within
     depth d                                                   • For Rule 1, we remove incoming edges to
                                                                 intervention variables using GX

B    Implementation Details of                                 • For Rule 2, we remove both incoming edges
     D OV ERIFIER                                                to primary interventions and outgoing edges
                                                                 from secondary interventions using GXZ
Our implementation converts abstract causal ex-
pressions into concrete computational objects that             • For Rule 3, we perform the appropriate graph
can be manipulated through rule applications. The                modifications for GXZ(W ) as specified by
core components are implemented as follows:                      Pearl

Expression Representation We represent causal               D-separation Testing To determine rule applica-
expressions using a symbolic framework built                bility, we implement d-separation tests using Net-
on SymPy. Each causal probability expres-                   workX’s built-in is_d_separator function. For
sion P (Y | do(X), Z) is represented as a                   each potential rule application, we:
CausalProbability object with an outcome vari-
                                                              1. Create the appropriate modified graph based
able and a list of conditioning factors, which may
                                                                 on the rule
include both observational variables and interven-
tional variables (wrapped in Do objects). This rep-           2. Identify the variables that need to be tested for
resentation allows for:                                          conditional independence
    • Unique identification of expressions through            3. Perform the d-separation test with the appro-
      consistent string conversion                               priate conditioning set
    • Distinction between interventional and obser-           4. Apply the rule only if the independence con-
      vational variables                                         dition is satisfied
    • Manipulation of expressions through rule ap-            For example, when applying Rule 1 to remove
      plications                                            an observation Z from P (Y | do(X), Z), we test
Expression Parser. As a preprocessing step, this            whether Y and Z are d-separated given X in the
part parses expressions from natural language or            graph GX .
symbolic form into normalized structured represen-             4
                                                                   https://www.sympy.org
tations in Lcausal . This includes:                            5
                                                                   https://networkx.org/


                                                       13
Search Algorithm Optimization To make the                    Since X ∈ {0, 1} the sum becomes:
breadth-first search efficient, we implement several
                                                                  = 0 · P(X = 0 | Z) + 1 · P(X = 1 | Z)       (19)
optimizations:
                                                                  = P(X = 1 | Z)                              (20)
   • Expression normalization: We convert ex-
                                                                                                             ■
     pressions to canonical string representations
                                                             Since CLadder contains only binary variables, we
     with consistent ordering and whitespace re-
                                                             use Proposition B.1 to replace expression that in-
     moval.
                                                             volve an expectation with a probability.
   • Memoization: We cache the results of d-
                                                             C     Proof of Theorem 3.1
     separation tests to avoid redundant graph op-
     erations.                                               We restate the theorem for convenience:
                                                             Proposition C.1 (Derivation Graph). Let ϕ ∈
   • Early termination: We immediately return
                                                             Lcausal . Define a directed graph S(ϕ) where:
     a proof path when the target expression is
     found.                                                      • Each node is a unique causal expression deriv-
                                                                   able from ϕ;
   • Visited set tracking: We maintain a set of
     already-visited expressions to avoid cycles                 • A directed edge ϕ → ϕ′ exists if ϕ′ can be
     and redundant exploration.                                    obtained from ϕ by applying a single valid
                                                                   transformation rule.
Handling Incomplete Knowledge A key inno-                    Then S(ϕ) is a well-defined, finite-branching
vation in our implementation is the ability to work          graph.
with incomplete causal knowledge. When the full
DAG structure is unknown, our system can:
                                                                 Proof. Let G = (V, E) be a causal DAG
                                                                 with finite node set V , and let Lcausal denote
   • Work with explicitly provided independence
                                                                 the set of well-formed causal expressions over
     pairs between variables
                                                                 V . Each expression is of the form P (Y | Z),
   • Infer independence relationships from partial               where Y ⊆ V and Z consists of observational
     graph information                                           variables in V and interventional variables of
                                                                 the form do(X) with X ⊆ V . Since V is finite,
   • Explore potential equivalences under different              and expressions are maintained in canonical
     assumptions                                                 normalized form, there are only finitely many
                                                                 such choices of Y and Z, and hence Lcausal is
Scope of Verification In CLadder (Jin et al.,                    finite.
2023), the variables are binary, i.e., X ∈ {0, 1}.               Let R denote the set of valid transformation
We state the following theorem:                                  rules. Each rule r ∈ R defines a partial func-
Proposition B.1 (Binary Expectation-Probability                  tion
Equivalence). If X is a binary random variable
                                                                              r : Lcausal → Lcausal ,       (21)
taking values in {0, 1}, then for any conditioning
event or a set of variables Z,                                   whose domain is determined by syntactic con-
                                                                 ditions and graphical independence constraints
            E[X | Z] = P(X = 1 | Z)             (17)             in G. This induces a derivation relation ⇒ on
                                                                 Lcausal , defined by

   Proof. Let X be a binary random variable tak-                  ϕ ⇒ ϕ′ ⇐⇒ ∃r ∈ R such that r(ϕ) = ϕ′ .
ing values in {0, 1}, and fix an arbitrary condition-                                               (22)
ing set Z. By definition of conditional expectation              The derivation graph S(ϕ) consists of all ex-
for a discrete random variable:                                  pressions reachable from ϕ under ⇒, with
                   X                                             edges corresponding to single rule applications.
     E[X | Z] =          x · P(X = x | Z)       (18)
                                                                 Since each rule is well defined on its domain,
                 x∈{0,1}



                                                        14
    the relation ⇒ is well defined, and therefore                 2. The path does not end at the target expres-
    so is S(ϕ).                                                      sion, i.e., ϕn ̸= ψ.
    Moreover, for any ϕ ∈ Lcausal , the set
                                                                  3. There exists some i such that ϕi+1 is not
                   ′                        ′                        derivable from ϕi by any valid transfor-
                {ϕ ∈ Lcausal | ϕ ⇒ ϕ }            (23)
                                                                     mation rule admissible under G.
    is finite. Indeed, the rule set R is finite, and
    each rule ranges over subsets of V , of which               We now show that none of these cases can
    there are finitely many. Consequently, each                 occur by construction:
    expression admits only finitely many valid in-                 • The algorithm initializes the search fron-
    stantiations of transformation rules.                            tier with {ϕ}, so every returned path must
    It follows that every vertex in S(ϕ) has finite                  begin with ϕ1 = ϕ. Hence, Case (1) can-
    out-degree. Therefore, S(ϕ) is a well-defined,                   not occur.
    finite-branching directed graph.              ■
                                                                   • The algorithm terminates only when an
                                                                     expression syntactically identical to ψ is
D     Proof of Theorem 3.2                                           reached, hence ϕn = ψ. Hence, Case (2)
                                                                     cannot occur.
We formally prove the soundness and completeness
of our verification framework by modeling it as a                  • The algorithm expands nodes exclusively
symbolic derivation system over a finite-branching                   by applying rules from R (do-calculus
graph induced by transformation rules.                               and standard probability rules), and each
   We restate the theorem for convenience:                           rule is applied only when its graphical and
Proposition D.1 (Soundness & Completeness of                         syntactic preconditions (e.g., d-separation
Proof Search). Let G be a causal DAG, and let                        in G) are satisfied. Hence, Case (3) can-
ϕ, ψ ∈ Lcausal . If ϕ ⊢G ψ, then Algorithm 1 re-                     not occur.
turns a valid proof sequence within depth d, for
some finite d. Conversely, if no such derivation                Thus, every returned path is a valid derivation
exists within depth d, Algorithm 1 returns None. If             from ϕ to ψ, contradicting our assumption.
the depth bound is removed and cycle detection is               Therefore, D OV ERIFIER is sound.            ■
enforced, the verifier is both sound and complete.
   We first show that D OV ERIFIER is sound.
                                                                 We now prove completeness, first by showing
                                                               under the case where there is a depth bound d.
    Proof. Fix a causal DAG G and let ϕ, ψ ∈
    Lcausal denote the initial and target expressions,
                                                                Proof. Suppose ϕ ⊢G ψ. By definition of ⊢G ,
    respectively. Assume for contradiction that
                                                                there exists a finite sequence of rule applica-
    D OV ERIFIER is not sound. Then there exists
                                                                tions forming a path in S(ϕ) from ϕ to ψ. Let
    some proof path
                                                                the length of the shortest such sequence be d⋆ .
                   π = ⟨ϕ1 , . . . , ϕn ⟩                       By Proposition 3.1, S(ϕ) is finite-branching.
                                                                Since Algorithm 1 performs breadth-first
    returned by the algorithm such that π is not a
                                                                search, it explores all expressions reachable
    valid derivation from ϕ to ψ.
                                                                from ϕ in increasing order of path length. In
    By definition, a valid derivation from ϕ to ψ
                                                                particular, with depth bound d, Algorithm 1
    is a finite sequence ⟨ϕ1 , . . . , ϕn ⟩ with ϕ1 = ϕ
                                                                enumerates every node in S(ϕ) at graph dis-
    and ϕn = ψ, such that for all i < n, ϕi+1 is
                                                                tance at most d from ϕ before returning None.
    obtained from ϕi by a valid transformation rule
                                                                Therefore:
    admissible under G. Hence, any sequence that
    is not a valid derivation must violate at least                • If d ≥ d⋆ , then ψ lies at distance at most d
    one of the following conditions:                                 from ϕ in S(ϕ), so Algorithm 1 will reach
                                                                     ψ and return a valid proof sequence.
      1. The path does not start at the initial ex-
         pression, i.e., ϕ1 ̸= ϕ.                                  • If d < d⋆ , then no path of length at most


                                                          15
                                                                These optimizations preserve the theoretical
         d from ϕ to ψ exists in S(ϕ), and Algo-
                                                             guarantees while making the approach computa-
         rithm 1 correctly returns None.
                                                             tionally feasible for practical use in evaluating
    Hence, Algorithm 1 is complete up to depth d.            causal reasoning in language models.
    ■
                                                             F     Data Samples of Synthetic Data
                                                             To support the evaluation of causal inference meth-
  We further consider the unbounded-depth setting
                                                             ods, we construct synthetic datasets using directed
with cycle detection.
                                                             acyclic graphs (DAGs) that encode assumed causal
                                                             relationships among variables. Each DAG consists
    Proof. Assume that the algorithm maintains
                                                             of nodes representing variables and directed edges
    a global visited set and discards any successor
                                                             representing direct causal influences. These graphs
    expression that has been previously encoun-
                                                             serve as the basis for simulating both observational
    tered (after canonical normalization), thereby
                                                             and interventional data.
    preventing revisiting states and eliminating
                                                                The data samples are designed to validate sym-
    cycles. By construction, all expressions are
                                                             bolic derivations using do-calculus. Each example
    maintained in canonical normalized form and
                                                             contains:
    range over finitely many subsets of V (Sec-
    tion B). Since V is finite, the set of canoni-               • A DAG representing the underlying causal
    cal well-formed expressions over V is finite,                  structure.
    and hence the derivation graph S(ϕ) contains
    finitely many vertices.                                      • A pair of probability expressions (ϕ, ψ),
    The algorithm performs breadth-first search on                 where ϕ is an interventional expression in-
    S(ϕ) while expanding each reachable vertex at                  volving do(·) operators and ψ is an equivalent
    most once. Consequently, every vertex reach-                   or simplified observational expression.
    able from ϕ is eventually explored after finitely
    many expansion steps.                                        • A proof sequence specifying the ordered ap-
    If ψ is reachable from ϕ in S(ϕ), the algorithm                plications of do-calculus rules (Rule 1, Rule 2,
    will therefore visit ψ and return a valid                      Rule 3) used to transform ϕ into ψ.
    derivation. Otherwise, no such derivation
                                                               These synthetic samples are not drawn from real-
    exists. Hence, D OV ERIFIER is complete in the
                                                             world distributions, but they adhere strictly to the
    unbounded-depth setting.                       ■
                                                             independence constraints implied by the DAGs, en-
                                                             suring the theoretical correctness of all derivations.
E     Practical Considerations                               G     Prompt Examples
Fact E.1 (Complexity). The time complexity of
                                                             To evaluate and guide language model performance
BFS is O(bd ) where b is the maximum branching
                                                             on causal reasoning tasks, we designed a two-shot
factor and d is the depth limit.
                                                             prompt that consists of: A set of instructions, two
   While theoretically sound, practical implementa-          fully worked examples, a new query prompt for the
tions must consider several optimizations:                   model to solve in the same format.
    1. Expression normalization to avoid revisiting              ## Instructions:
       equivalent states (e.g., removing redundant               1. For each problem, identify the correct
                                                                     ,→ expression that represents the query
       conditions, standardizing variable order)                 2. Draw the graphical representation as a
                                                                     ,→ text description of edges
    2. Efficient d-separation testing for determin-              3. Show your mathematical reasoning step by
       ing rule applicability                                        ,→ step
                                                                 4. Provide a final yes/no answer
    3. Memoization of independence tests to avoid                5. Keep your response concise and focused on
                                                                     ,→ the solution
       redundant graph operations
                                                                 ## Examples:
    4. Bidirectional search from both ϕ and ψ to
       reduce the effective search depth                         Example 1:


                                                        16
Prompt: Imagine a self-contained,                   H    Formalization Quality
    ,→ hypothetical world with only the
    ,→ following conditions, and without any        In the CLadder setting, the formalization step is
    ,→ unmentioned factors or causal
    ,→ relationships: Poverty has a direct
                                                    relatively stable because the benchmark uses a very
    ,→ effect on liking spicy food and              constrained format. Variables are binary, expres-
    ,→ cholera. Water company has a direct          sions follow a fixed schema, and expectations can
    ,→ effect on liking spicy food. Liking
    ,→ spicy food has a direct effect on            be rewritten as probabilities through a simple proof.
    ,→ cholera. Poverty is unobserved. The          Importantly, CLadder itself supplies a canonical
    ,→ overall probability of liking spicy          mapping from natural-language event descriptions
    ,→ food is 81%
Let V2 = water company; V1 = poverty; X =           to variable symbols in the first step of each item’s
    ,→ liking spicy food; Y = cholera               reasoning field. We follow this provided mapping
                                                    directly, so no additional interpretation or heuristic
Expression: P(Y | X)
Graphical Representation: V1->X,V2->X,V1->Y,        conversion is introduced on our side. Because the
    ,→ X->Y                                         resulting expressions lie in a fixed and regular lan-
Reasoning: P(X = 1, Y = 1)/P(X = 1) - P(X =
                                                    guage, simple regex-based parsing is sufficient, and
    ,→ 0, Y = 1)/P(X = 0)
P(X=1) = 0.81                                       in our testing we did not observe parsing errors for
P(Y=1, X=0) = 0.13                                  well-formed items. A small number of CLadder
P(Y=1, X=1) = 0.17
0.17/0.81 - 0.13/0.19 = -0.44
                                                    instances contain NaN values in the ground-truth
-0.44 < 0                                           expressions; in these cases, the benchmark’s own
Final Answer: No                                    symbolic representation is incomplete, and we skip
Example 2:                                          only these specific items.
Prompt: Imagine a self-contained,
    ,→ hypothetical world with only the             I   Alternative Metrics
    ,→ following conditions, and without any
    ,→ unmentioned factors or causal                Evaluation of causal expression generation has of-
    ,→ relationships: Poverty has a direct
    ,→ effect on liking spicy food and
                                                    ten relied on surface-level metrics such as exact
    ,→ cholera. Water company has a direct          string match, BLEU score, BERTscore, and token-
    ,→ effect on liking spicy food. Liking          level F1.
    ,→ spicy food has a direct effect on
    ,→ cholera. Poverty is unobserved. For          BLEU and Token-level F1 Fails for Causal Eval-
    ,→ people served by a local water
    ,→ company, the probability of cholera          uation BLEU computes precision over n-grams
    ,→ contraction is 64%                           between a candidate and reference string. In causal
Let V2 = water company; V1 = poverty; X =
    ,→ liking spicy food; Y = cholera.
                                                    reasoning, it suffers from

Expression: E[Y | do(X = 1)] - E[Y | do(X =         Small expression length bias: Causal   expres-
    ,→ 0)]                                             sions are often short; hence, BLEU becomes
Graphical Representation: V1->X,V2->X,V1->Y,
    ,→ X->Y
                                                       unstable when evaluating < 10 token strings
Reasoning: E[Y | do(X = 1)] - E[Y | do(X =             since higher-order n-grams vanish.
    ,→ 0)]
[P(Y=1|V2=1)-P(Y=1|V2=0)]/[P(X=1|V2=1)-P(X          Syntactic Fragility: Expressions that are seman-
    ,→ =1|V2=0)]
P(Y=1 | V2=0) = 0.64
                                                        tically equivalent but have different variable
P(Y=1 | V2=1) = 0.66                                    order get penalized.
P(X=1 | V2=0) = 0.50
P(X=1 | V2=1) = 0.45                                Non-semantic penalties: BLEU may still reward
(0.66 - 0.64) / (0.45 - 0.50) = -0.39
-0.39 < 0                                               inclusion of irrelevant variables if they over-
Final Answer: Yes                                       lap with the gold string, even if the overall
                                                        expression is wrong.
## Your Task:
Solve the following problem using the format
    ,→ above. Begin your response with "            Token-level F1 computes overlap between tokens,
    ,→ Solution:" and provide only the              treating the expression as a bag of symbols. How-
    ,→ expression, graphical representation,        ever, it still leads to multiple failure cases:
    ,→ reasoning, and final answer.
Prompt: {description}
                                                    Ignores structure role of variables: F1 cannot
                                                        distinguish P (Y ) from P (Y | X) or
                                                        P (Y | do(X)). They all share some subset

                                               17
               Model                                                  BLEU      Token-level F1
               Llama-3.1-8B-Instruct (Grattafiori et al., 2024)         0.46          0.70
               Mistral-7B-v0.1 (Jiang et al., 2023)                     0.33          0.58
               Llama-3.1-8B (Grattafiori et al., 2024)                  0.36          0.57
               Gemma-7b-it (Team et al., 2024)                          0.19          0.55

           Table 3: Average BLEU and token-level F1 scores for each model evaluated on CLadder.

                     LLM Output       Formal Label           Correct?    BERTScore F1
                     P(Y | V1)        P(Y | X)                  No             0.91
                     P(Y)             P(Y | X)                  No             0.91

Table 4: Incorrect model outputs with high BERTScore. While these expressions differ from the gold standard,
BERTScore assigns high similarity, demonstrating its over-generosity in causal evaluation.


     of overlapping tokens and will inflate the             BERTScore Failure Cases BERTScore (Zhang*
     accuracy.                                              et al., 2020) is a widely used metric that computes
                                                            semantic similarity by aligning contextualized to-
No notion of well-formedness: Syntactically in-             ken embeddings from a pretrained BERT model. It
    valid expressions such as P (X Y ) or Y |               is often promoted as a semantically aware alterna-
    P (X) might have high F1 if they reuse com-             tive to BLEU. However, in the context of causal
    mon symbols despite being invalid.                      reasoning, BERTScore exhibits a distinct failure
No semantics: Conditioning vs intervention is               mode: it confuses lexical proximity with logical
    completely ignored, a model can be rewarded             validity.
    for guessing the right letters, not the right              Table 4 shows common failure cases where
    logic.                                                  BERTScore assigns high similarity scores to ex-
                                                            pression pairs that are not causally equivalent. Let
Table 3 shows the average BLEU and token-level              ϕpred , ϕgold ∈ Lcausal be causal expressions en-
F1 score for each model evaluated on causal lan-            coded as strings. BERTScore computes
guage tasks. We see that both BLEU and F1 lack                                                                
                                                            BERTScore(ϕpred , ϕgold ) = F1BERT hϕpred , hϕgold ,
a formal grounding in the semantics of causal in-
ference. There is no transformation set T under                                                             (25)
which they define an equivalence class. In contrast,        where hϕ denotes contextual token embeddings
our symbolic verifier defines:                              produced by a pretrained BERT model.
                                                               Crucially, BERTScore has no access to causal
   ϕ1 ≡G ϕ2 ⇐⇒ ϕ1 ⊢G ϕ2 ∧ ϕ2 ⊢G ϕ1             (24)         semantics, independence structure, or the formal
                                                            syntax of do-calculus. Tokens such as P, (, and )
Thus, BLEU and F1 may disagree with formal cor-
                                                            are close in embedding space regardless of their
rectness, and worse, may systematically overesti-
                                                            role in a logical formula. As a result, BERTScore
mate the validity of incorrect outputs.
                                                            assigns high similarity scores to expressions that
   Furthermore, it was surprising to see token-level
                                                            are semantically disjoint under the causal graph.
F1 perform worse than string match at first. In sym-
                                                               Unlike D OV ERIFIER, BERTScore does not sat-
bolic probability expressions, operators such as the
                                                            isfy a soundness guarantee:
conditioning bar (|) or the intervention operator
do(·) may be tokenized jointly with adjacent vari-               BERTScore(ϕpred , ϕgold ) > 0.9 ̸⇒
ables depending on the tokenizer (e.g., | Z versus                                    ϕpred ≡G ϕgold .     (26)
separate tokens | and Z). As a result, semanti-
cally equivalent expressions such as P (Y | Z, X)              This failure mode is particularly concerning
and P (Y | X, Z) can exhibit reduced token over-            in high-stakes settings, where plausible-looking
lap when token boundaries differ, leading to lower          causal statements may lead to incorrect conclu-
token-level F1 scores despite identical semantics.          sions when evaluated using BERTScore. While one

                                                       18
could plot ROC curves for similarity-based metrics           Let
using symbolic derivability as ground truth, such an
analysis is fundamentally misaligned: BERTScore               Path(S(ϕ)) ≜ {π | π is a derivation in S(ϕ)}.
is not designed to approximate causal validity, as it                                                   (28)
ignores graph structure, interventions, and admis-             A breadth-first search with resource bound b ex-
sible rewrite rules. For this reason, we focus on            plores the subset of derivations
qualitative failure cases that directly expose these
semantic mismatches.                                          S≤b (ϕ) ≜ {π ∈ Path(S(ϕ)) | depth(π) ≤ b},
                                                                                                     (29)
J   Feedback Prompts
                                                             which induces the truncated distribution
In Section 4.3, verifier-guided feedback is imple-
mented as a single diagnostic string produced by                                        I[π ∈ S≤b (ϕ)]
                                                                        Pb (π | ϕ) =                   .      (30)
suggest_fix() from the predicted DAG and the                                               |S≤b (ϕ)|
model-generated causal expression. Concretely,
                                                                More generally, let R(ϕ) denote the set of rules
the LLM is re-prompted with the same original
                                                             applicable at expression ϕ. A locally normalized
problem context and its prior expression, plus one
                                                             rule-selection policy
of the following messages verbatim (depending on
which condition is triggered).                                                    wr
                                                                 P (r | ϕ) = P                   (r ∈ R(ϕ))   (31)
                                                                               r′ ∈R(ϕ) wr′
Diagnostic feedback strings (verbatim).
                                                             induces a distribution over derivations. We repre-
    • "All    observed    variables    are                   sent a derivation π as a sequence of state–rule pairs
      d-separated   from   {Y}    in   the                   (ϕ, r) corresponding to successive rule applications,
      interventional graph. Consider using                   so that
      P({Y}) instead — no conditioning is                                               Y
      necessary."                                                        P (π | ϕ) =        P (r | ϕ).        (32)
                                                                                       (ϕ,r)∈π
    • "{z} is a mediator between a cause
      and {Y}. Avoid conditioning on {z}                       For any choice of weights {wr } and any finite
      to prevent post-treatment bias."                       bound b, the induced derivability relation ⊢bR is
                                                             sound with respect to |=, and satisfies
    • "{z} causes {Y}, but is only observed.
      Consider using do({z}) if you intend                         ⊢bR ⊆⊢b+1
                                                                         R ⊆ ⊢R ,         lim ⊢bR =⊢R .       (33)
                                                                                          b→∞
      an intervention."
                                                             L     Frequently asked questions
    • "Conditioning on {z} may bias
      results; {Y} is not d-separated from                   What problem does D OV ERIFIER actually
      {z} given {W}."                                        solve? D OV ERIFIER addresses the gap be-
                                                             tween surface-form evaluation of causal reason-
   Here, {Y } denotes the outcome variable in the            ing in LLM outputs (e.g., string match, BLEU,
current expression, {z} ranges over observed condi-          BERTScore) and semantic correctness under causal
tioning variables, and {W } denotes the remaining            inference rules. It checks whether a model’s pre-
conditioning set used in the d-separation check.             dicted causal expression is formally derivable from
                                                             a given causal graph using do-calculus and proba-
K    Bounded Search                                          bility rules, recovering correct answers that naive
A practical middle ground is to keep the verifier            metrics miss.
sound (i.e., only applying valid rewrite rules) while        Does D OV ERIFIER require the ground truth an-
guiding expansion using heuristics learned from              swer? For evaluation, yes - the framework needs
data. Let S(ϕ) denote the derivation graph of ex-            the correct expression to compare against. How-
pressions reachable from ϕ under rule set R. Se-             ever, for feedback and self-correction, it can op-
mantic entailment is defined as                              erate without the ground truth by checking the
                                                             model’s answer against the DAG and suggesting
            ϕ |= ψ ⇐⇒ ψ ∈ S(ϕ).                 (27)         corrections.

                                                        19
Can’t we just use the ID algorithm by Shpitser
and Pearl (2008) to see if both are identifiable,
and then compare? There are cases when the
expressions are unidentifiable but can be simplified
such as

          ϕ = P (Y | do(X), do(W ), Z)
         ψ = P (Y | do(X), Z)

under specific DAGs, which can be easily con-
structed to satisfy do-calculus rule 3.
How is D OV ERIFIER different from Lean
or other proof assistants? Lean is a general-
purpose formal proof assistant used to verify math-
ematical theorems in a wide range of domains. It
requires users to construct complete proofs in a for-
mal language. D OV ERIFIER is a domain-specific
verifier for causal inference. It operates only on
causal expressions, uses a fixed set of rules from
do-calculus and probability theory, and performs
automated proof search to determine equivalence
between expressions given a causal graph. Users
do not supply the proof steps; the system infers
them automatically.




                                                        20
