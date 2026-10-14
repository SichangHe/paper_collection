                                             LLM-based Automated Theorem Proving Hinges on
                                                   Scalable Synthetic Data Generation


                                              Junyu Lai1      Jiakun Zhang1 Shuo Xu1 Taolue Chen2 Zihang Wang1 Yao Yang1
                                                                      Jiarui Zhang1 Chun Cao1 Jingwei Xu1∗
                                                     1
                                                       State Key Laboratory for Novel Software Technology, Nanjing University, China
arXiv:2505.12031v1 [cs.AI] 17 May 2025




                                                 2
                                                   School of Computing and Mathematical Sciences, Birkbeck, University of London, UK
                                             {junyu_lai, zjk, shuoxu, wangzihang, yangyao, jiarui_zhang}@smail.nju.edu.cn
                                                               t.chen@bbk.ac.uk, {caochun, jingweix}@nju.edu.cn



                                                                                            Abstract

                                                       Recent advancements in large language models (LLMs) have sparked considerable
                                                       interest in automated theorem proving and a prominent line of research integrates
                                                       stepwise LLM-based provers into tree search. In this paper, we introduce a novel
                                                       proof-state exploration approach for training data synthesis, designed to produce
                                                       diverse tactics across a wide range of intermediate proof states, thereby facilitating
                                                       effective one-shot fine-tuning of LLM as the policy model. We also propose an
                                                       adaptive beam size strategy, which effectively takes advantage of our data synthesis
                                                       method and achieves a trade-off between exploration and exploitation during tree
                                                       search. Evaluations on the MiniF2F and ProofNet benchmarks demonstrate that our
                                                       method outperforms strong baselines under the stringent Pass@1 metric, attaining
                                                       an average pass rate of 60.74% on MiniF2F and 21.18% on ProofNet. These
                                                       results underscore the impact of large-scale synthetic data in advancing automated
                                                       theorem proving.


                                         1        Introduction
                                         Reasoning has emerged as a frontier in large language model (LLM) research. Numerous approaches
                                         have been proposed to enhance their reasoning capabilities [Yu et al., 2024, Giadikiaroglou et al.,
                                         2024], among which mathematical reasoning [Ahn et al., 2024] has received special attention from
                                         both academia and industry. The reasons are twofold: (1) it is widely considered as a strong indicator
                                         of LLM’s cognitive proficiency; and (2) it has a direct application in the emerging AI4Math area and
                                         great potential in software engineering [Li et al., 2024, Liu et al., 2024]. While extensive research
                                         has focused on solving mathematical problems given in natural language [Muennighoff et al., 2025,
                                         Xiang et al., 2025], we are mostly interested in proving theorems formulated in formal mathematical
                                         languages, because it represents a more fundamental challenge. To this end, we synergize interactive
                                         theorem provers (ITPs, aka proof assistant), represented by Lean [Moura and Ullrich, 2021], Isabelle
                                         [Paulson, 1994] and Rocq (previously known as Coq, [Barras et al., 1997]), and LLMs, effectively
                                         giving rise to a neuro-symbolic approach towards automated theorem proving (ATP).
                                         In the literature, there are generally two classes of approaches which harness LLMs for ATP, com-
                                         monly referred to as tree search methods and whole-proof generation methods [Ren et al., 2025]. The
                                         former repeatedly performs proof step generation, utilizing LLMs to prescribe a tactic to be applied
                                         to the current proof state. Overall, it is cast as a tree search process to generate the final proof. In
                                         contrast, the latter is performed in an end-to-end style, where LLMs are asked to produce an entire
                                         proof directly from the theorem, which is then verified by the proof assistant. Generally speaking, the
                                              ∗
                                                  Corresponding author


                                         Preprint. Under review.
                                                              Initial state          Initial proof state               Exploration
      Exploration
      (Large beam size)
                                                                                                        x y z: ℝ
                          rw          rcases        have                      have             h0 : 0 < x ∧ 0 < y ∧ 0 < z

                                                                    …                   ⊢ 9/(x+y+z) ≤ 2/(x+y) + 2/(y+z) + 2/(z+x)


                                                                                     Proof state with high score          Exploitation
                     apply       field_simp                have
                                                                                                         x y z: ℝ
                                                   …                                           hx:0 < x hy:0 < y hz:0 < z
                                                                                                      ⊢ 9/(x+y+z) ≤
                                                                                      ((2*(y+z)+2*(x+y))*(z+x)+2*((x+y)*(y+z)))/((x
                                 rw                 rw                                     +y)*(y+z)*(z+x))/((x+y)*(y+z)*(z+x))



                                                                                      Intermediate state           Error state
                          nlinarith
     Exploitation
     (Small beam size)                   Proof finish !                               Proof finish state           Unexpanded state



Figure 1: An illustration of the proposed tree search strategy. The example is derived from the
MiniF2F benchmark, specifically the problem algebra_9onxpypzleqsum2onxpy. For simplicity, only
the tactics are retained in the depicted proof states, while the associated premises are omitted.




whole-proof methods are simpler, requiring less communication to coordinate between the LLM and
the ITP. However, as the intermediate proof states are hidden, LLMs typically struggle to generate a
long proof. In practice, these methods usually heavily rely on additional techniques, such as natural
language comments to assist the proof [Lin et al., 2025, Xin et al., 2024a].
In our work, we adopt a tree search approach. This class of methods is advantageous in demanding
relatively lower capability on the policy model, making it suitable for settings with smaller model sizes
and limited computational resources. It also offers greater flexibility for incorporating customized,
problem-specific strategies into the search process [Wang et al., 2024, An et al., 2024]. Furthermore,
starting from a small number of seed problems, tree search enables extensive exploration of proof
states, facilitating the synthesis of large volumes of new data for iterative training of the policy model,
which is considerably challenging to achieve in whole-proof generation [Xin et al., 2024b]. We take
Lean 4 as the base ITP due to its popularity in the community, although our methodology can be
easily applied to other proof assistants.
Despite the advance in LLMs, they remain notably limited in formal mathematical reasoning [Yang
et al., 2024a]. An fundamental cause is that LLMs are typically trained for general-purpose language
understanding rather than for theorem proving, which requires substantial domain expertise in
mathematics. To overcome this gap, post-training is indispensable, for which we focus on fine-tuning.
A major challenge lies in the scarcity of high-quality training data for theorem proving. Proofs in ITPs
are typically expressed as code in a domain-specific language (DSL) defined by the corresponding
prover. Compared to widely used programming languages such as Python, proofs written in Lean
are extremely limited in volume. For instance, standard Lean 4 libraries (e.g., Mathlib [mathlib
Community, 2020]) provide less than 1GB data in total, insufficient for effectively fine-tuning LLMs.
As a result, synthetic data generation has become a crucial component in adapting LLMs for ATP.
Recent efforts have explored translating natural language mathematics into Lean 4 syntax using LLMs
[Wu et al., 2022, Ying et al., 2024, Murphy et al., 2024], generating new problems by sampling from
distributions (e.g., a fine-tuned policy model) learned over existing Lean 4 formalizations [Dong and
Ma, 2025, Poesia et al., 2024, Xin et al., 2024b]. Another approach to improving model capability is
Expert Iteration (EI) [Polu and Sutskever, 2020], which can be treated as a form of rejection sampling.
Given a set of formalized mathematical problems, a model may fail to solve the more difficult
instances but succeed on simpler ones. By collecting successful proofs from these solvable cases, a
new dataset can be constructed to fine-tune the model, thereby gradually enhancing its capabilities.
This method has been widely used in prior work [Polu and Sutskever, 2020, Polu et al., 2022, Wu
et al., 2024, Xin et al., 2025]. However, EI suffers from significant inefficiency when applied in
conjunction with tree search. In each iteration, the number of newly solvable problems is often
limited, while performing full search over the entire dataset incurs substantial computational cost.
This inefficiency makes EI impractical in settings with limited computational resources, highlighting
the need for a more direct and resource-efficient data generation strategy.


                                                                              2
In this paper, we propose a data synthesis method called proof state exploration for fine-tuning
LLMs in ATP, along with a complementary adaptive beam size strategy for tree search during the
proving process. Our data synthesis method begins with a set of formalized mathematical problems
as seeds and leverages the existing policy model to explore related intermediate proof states via
tree search. These intermediate states may correspond to goals that are logically equivalent to the
original ones after a sequence of transformations, or to subgoals resulting from original problem
decomposition. During the process, we explicitly decouple the generation of tactics from that of
premises. Specifically, we adopt a constrained decoding algorithm [Hokamp and Liu, 2017] that
restricts the model to sample from and de-duplicate within a curated set of commonly used tactics,
followed by premise completion handled by the policy model. In addition, we introduce a heuristic
pruning strategy to balance the trade-off between diversity in the generated outputs and computational
efficiency during the exploration. This enables large-scale synthesis of intermediate proof states and
transformation steps within tree search, thereby reducing the distribution gap between the training
data and real-world proving scenarios. Moreover, our method does not rely on EI. Instead, our policy
model is trained on data generated from a single, exhaustive exploration over existing formalized
problems. This one-pass generation approach significantly reduces computational overhead while
achieving competitive performance.
Although the LLM fine-tuned on this synthetic dataset can serve as a policy model capable of
generating diverse tactics, it may not always prioritize proof completion during actual theorem
proving. To mitigate this limitation, we propose a simple yet effective adaptive beam size strategy
tailored to our data synthesis framework and integrated into the tree search process (cf. Figure 1).
The strategy starts with a relatively large beam size to encourage broad exploration of the space of
proof states. As the search proceeds, the beam size is gradually reduced, enabling the policy model to
concentrate on high-scoring proof states. This dynamic adjustment improves the focus of the search
and enhances the overall success rate of proof completion. Besides, we develop Dojo-BeamSearch-
Visualization (DoBeVi) (cf. Appendix A.3) as the basic interaction tool between the model and the
Lean 4 prover with a visualization module for tree search analysis.
Evaluation. We evaluate our method on two widely adopted benchmarks, MiniF2F and ProofNet,
achieving average pass rates of 60.74% and 21.18%, respectively, under the constraints of Pass@1
and a limited computational budget. These results outperform the current state-of-the-art methods
based on tree search.
The main contributions of this paper are as follows.

• We propose a novel data synthesis method, proof state exploration, which enables large-scale
  generation of exploration data for fine-tune LLMs as policy models in ATP.
• We propose a simple but efficient adaptive beam size strategy that synergistically operates with the
  data synthesis method, effectively guiding the search process towards proof completion.
• We carry out extensive experiments demonstrating that our method can effectively balance explo-
  ration and exploitation during tree search, achieving state-of-the-art performance among existing
  tree search methods.

2   Background
ITP and ATP. In a nutshell, interactive theorem proving is a process to develop and verify formal
proofs with the assistance of a computer, usually within a proof assistant (e.g., Lean, Isabelle,
Rocq), and involves human guidance to structure and complete the proof. The general process is to
formalize the theorem to be proven (i.e., the goal) in the language of the proof assistant first, and
then repeatedly apply tactics to break the goal into subgoals. The tactic may involve case analysis,
induction, rewriting, application of lemmas or axioms, etc. As such, the human user iteratively refines
the proof to guide the prover, choosing which rules to apply and in what order. The prover checks that
each inference step is valid according to the rules of the formal system. A major drawback is that this
process requires heavy human expertise and thus largely lacks automation. LLM-based Automated
Theorem Proving aims to find a proof automatically by simulating this process, effectively replacing
the human user by an LLM.
Tree Search LLM-based ATP. As mentioned in the Section 1, we adopt a tree search approach towards
LLM-based ATP. Generally speaking, tree search is a class of decision-making algorithms which


                                                  3
                                Transformed                             Proof state
                                                                                                                     Post-processing
         Formal math
                                  by REPL
                                                      Initial proof     exploration           Explored
                                                                                                                                          Training set
          problems                                       states                             intermediate
                                                                                                                                           𝑺𝐞𝐱𝐩𝐥𝐨𝐫𝐚𝐭𝐢𝐨𝐧
                                                                                            proof states




      Current proof state                             Tactics only                         Proof steps: tactics and premises                   Next proof states


        𝒔𝒊             Policy model                                   Policy model                                             Lean 4 prover              𝒔𝟏𝒊 𝟏
                                        Constrained                                     Batch
                                         Decoding        …                            Inference          …                                                …
                        Predefined
                       tactic set 𝒯                                                                                                                       𝒔𝑩
                                                                                                                                                           𝒊 𝟏
       One step of
       exploration




                                      Figure 2: An illustration of the data synthesis pipeline.


consists of searching combinatorial spaces represented by trees, where nodes denote states and
edges denote transitions (actions) from one state to another. In our setting, they enable an efficient
navigation of the large and complex proof space.
At a high level, tree search LLM-based ATP can be cast as a reinforcement learning (RL) problem,
where the state space comprises the proof states (aka proof terms). In general, proof states represent
the current status of the proof at any given point in the interactive session between LLM and the
proof assistant. Typically, they comprise the context (i.e, a list of assumptions, hypotheses and local
variables), the current (sub)goals (i.e., the proposition needing to prove to complete the proof) and
the number of subgoals to be proven. LLM acts as an actor, which, given the current proof state si ,
generates a tactic. In other words, LLM serves as the policy model. In theorem proving, tactics refer
to commands, or instructions, that guide the process of constructing a proof. In RL terms, tactics
can be regarded as an action ai , based on which the proof assistant produces a new proof state si+1 .
This process continues until either the theorem is successfully proved or the maximum number of
iterations is reached.
There are a plethora of search strategies, for instance, Monte Carlo tree search (MCTS) or best-first
search (BFS). In BFS, each expansion step involves using the policy model to perform beam search
decoding, generating a fixed number of top candidates (called the beam size). Typically, the process
begins at the root node and iteratively expands the current node to produce potential child nodes.
These candidates are then evaluated using a heuristic scoring function, and the node with the highest
score is selected for the next expansion. The expansion-score-selection steps are repeated until a goal
is reached or a termination condition is met. In our work, LLM, as the policy model, generates a set
of tactics {tji }B
                 j=1 for a proof state si , which are executed by the proof assistant one by one to obtain
the corresponding set of next proof states {sji+1 }B   j=1 .



3     Methods

3.1   Data synthesis by proof state exploration

In ITP, tactics play a central role. Normally, a tactic (e.g., rw [add_assoc add_comm]) consists
of the tactic operator (e.g., rw) and the premises (e.g., add_assoc and add_comm). In this paper, to
facilitate a finer-grained decomposition, what is commonly referred to as tactics are called proof steps,
while tactic refers to the operator only. We propose to carry out proof state exploration to synthesize
data. This is similar to tree search, but the crucial difference is that we prioritize the diversity of
tactics. Our data synthesis method is described as Algorithm 1. (cf. Figure 2 as well).
Motivated explanation. The intuition is that proof assistants (e.g., Lean 4) normally provide
a versatile range of tactics, which is considerably larger than, e.g., the set of reserved words in
programming languages, and can even be defined by users. It is practically infeasible to adopt all of
them in tree search. On the other hand, in practice, their actual use in theorem proving may not be as
wild as, e.g., user-defined functions (which are virtually infinite, or at least cannot be enumerated
exhaustively). Hence, as a trade-off, a reasonably curated set of commonly used tactics is sufficient
to solve the vast majority of problems in practice. Besides that, for tree search, critically we need an
“effective" set of (proof state, tactic) pairs. The observation is that in theorem proving, the same tactic


                                                                                 4
may have multiple meanings and can be used across various scenarios; for instance, the apply tactic
may be used in five different scenarios.2 Moreover, sometimes a tactic can be used in much broader
cases; for instance, the tactic rfl can handle all definitional equalities. However, as the policy model,
the LLM, like an inexperienced problem solver, may fail to realize that a tactic can actually be used
when a proof state is encountered. Ideally, such domain-specific knowledge should be injected into
LLMs via training, as they largely fall short of a certain level of abstraction capabilities so would be
hard to learn via the standard tree search.
The proposed proof state exploration method. We intend to identify those tactics which occur
rarely (with low probability) at a proof state. Just like a human problem solver normally has the
“comfort zone" for certain methods when facing a problem, in tree search, the policy model likely
picks up the tactic which has a higher probability. Quite often, this is sub-optimal or may represent a
missed opportunity. Our proof state exploration may force the policy model to explore those tactics
which it does not typically explore (i.e., force it to jump out of its comfort zone), by which a more
diverse training set can be constructed.
To this end, we first identify the frequently used tactics. We scan the entire Mathlib to collect all
defined tactics.3 There are hundreds of them, most of which are rarely used. To filter these out, we
need a representative dataset from which the frequency of each tactic can be collected. In our work,
we use the STP dataset [Dong and Ma, 2025] from which a total of 173 distinct tactics are obtained.
To further refine the set, we apply nucleus sampling with a threshold of P = 0.999 to filter out rarely
used tactics, ultimately yielding a set T of 60 commonly used tactics.
The design of the proof state exploration is guided by the above intuition and resembles the tree
search. For each expansion step, we apply Constrained Decoding to force the LLM to output B
different tactics (without premises) in T . We set a large beam size (e.g., B = 32). After obtaining
{(si , tji )}B         j
             j=1 with ti ∈ T , we feed these pairs back into the policy model to complete the premises,
yielding a set {(si , tji , pji )}B                                               j j
                                  j=1 of proof steps from si . By applying each (ti , pi ) to si using Lean 4
                                                                     j
prover, we generate the corresponding set of next proof states si+1 . Note that for exploration, even if
proof finish state is encountered, the exploration continues until the entire budget is exhausted.
Potential issues for this proof state exploration include (1) as B is often large, obtaining deeper proof
states (i.e., those “far away” from s0 ) can take a long time under limited computational resources; (2)
in certain proof states, a large beam size can lead to the generation of meaningless proof steps. For
example, the model may construct hypotheses that do not contribute to the progress of the proof.
To address these, we apply two heuristic strategies: (1) During each expansion, we prune the set by
retaining only αB branches, typically setting α = 0.25. When pruning, we keep the top β branches
with the highest joint probabilities and then randomly sample the remaining (αB − β) branches
uniformly from the rest. This balances exploration diversity and efficiency while preserving some of
the policy model’s inherent tendency toward proof finish. (2) Some seeds are overly simple and do
not require extensive exploration; too much exploration may even degrade the quality of the synthetic
data. To control this, we use proof finish as a signal: if a distinct path achieving proof finish is found
during an expansion, we reduce the expansion budget by a factor of γ = 0.9. This allows a simple
seed to quickly terminate exploration after generating multiple distinct solutions, improving overall
data synthesis efficiency.
After the proof state exploration, we obtain a dataset Sexploration . To produce the final dataset, we apply
three post-processing steps: (1) De-duplication, to remove redundant samples; (2) Decontamination,
where we use BLEU as a similarity metric to eliminate examples with high overlap with the evaluation
benchmark; and (3) Rejection Sampling, where we discard all transitions that are invalid from the
Lean 4 prover. The generated data is ultimately used to train policy LLM by performing Supervised
Fine-Tuning on a base model using the full accumulated training data corpus.

3.2       Adaptive beam size strategy

The tree search approaches used for ATP are conceptually similar [Polu and Sutskever, 2020, Polu
et al., 2022, Wu et al., 2024, Xin et al., 2025], differing mainly in (1) the policy model, (2) the scoring
      2
     https://www.ma.imperial.ac.uk/~buzzard/xena/formalising-mathematics-2024/Part_C/
tactics/apply.html#
   3
     https://github.com/haruhisa-enomoto/mathlib4-all-tactics


                                                     5
Algorithm 1: Proof State Exploration Algorithm for Data synthesis.
                   |S|
Data: S = {s0,n }n=1 ;                          /* S is the original formalized datasets. */
Result: Sexploration
Sexploration ← ∅;
for s0,n ∈ S do
    s0 ← s0,n ;                                              /* ignore index n for simplicity */
    q ← ∅;
    b←0;                                                        /* b is the consumed budget. */
    q.add(s0 );
    while |q| > 0 and b < budget do
          si ← q.get();
          {tji }Bj=1 ← policy_model.constrained_decoding(si , T );
          {pi }j=1 ← policy_model.batch_inference(si , {tji }B
              j B
                                                                    j=1 );
          for j ∈ [1, B] do
                si+1 ← lean_prvoer(si , tji , pji );
                Sexploration .add((si+1 , tji , pji , si ));
                if si+1 is a valid proof state then
                     q.add(si+1 );
                end
          end
          b.add_budget();
    end
end
Sexploration ← post_processing(Sexploration )


function, (3) the beam size, and (4) other budget-related parameters. In our tree search procedure, the
policy model is trained using data collected by the proof state exploration, as in Section 3.1. For the
score function, we take the sum of the LLM’s logarithmic joint probability over the beam (during
beam search) and the parent node’s score as the current node’s score, that is:
                                score(sji+1 ) = log Pθ (tj |si ) + score(si )                         (1)
where P (tj |si ) is the model’s predicted probability of applying the tactic tj at the state si and θ
denotes the policy models parameters.
In this work, we focus the pruning strategy on dynamically decaying the beam size during the tree
search process. This design is motivated by the empirical finding that beam size has a particularly
significant impact on overall performance compared to other factors in tree search. The details of
the finding are presented in Section 4.3. The optimal beam size is difficult to determine in advance.
The general observation is that, if the beam size is too small, the search may fail to discover proof
states, missing potential opportunities; if the beam size is too large, the search may risk being trapped
within one sub-tree rooted at a high-scoring intermediate node, resulting in futile expansions. Hence,
it is necessary to adapt the beam size to better control the tree search.
We adopt a larger beam size at the early stages of tree search; as the search proceeds (i.e., the depth
increases), we gradually reduce the beam size. This is largely aligned with the aforementioned
observation. In particular, during the later stages of tree search, being trapped is particularly harmful
as it may dump the search budget. By reducing the beam size, we effectively prune away less relevant
branches and prevent the search from over-committing to one sub-tree too much. One may intuitively
understand the design by taking an analogy of an IMO contestant. At the early stage, (s)he may want
to widen the horizon by exploring different problem-solving strategies (e.g., reading books, surfing
AoPS). However, when sitting in the competition (i.e., at a later stage), (s)he would better focus on
relatively small strategies to attempt, prioritizing solving the problems successfully. To this end, we
design an adaptive beam size function, namely,
                         beam_size = Bmin + (Bmax − Bmin ) × max(1 − λM, 0)                           (2)
where M = e/E, with e denoting the current expansion step and E representing the maximum
number of expansions allowed by the budget. The parameter λ is a hyperparameter controlling the


                                                     6
decay rate of the beam size. The beam size gradually decreases from Bmax to Bmin as the search
proceeds, thereby realizing the adaptive behavior described earlier. This search dynamic has also
been confirmed empirically (cf. Figure 3 in Appendix).

4         Experiments
4.1       Evaluation settings

Below are the basic experimental settings (cf. Section A.4 for more details). All experiments were
conducted on a server with 8 H800 GPUs; the code and model checkpoint are available4 .
Models. We use Qwen2.5-Math-7B [Yang et al., 2024b] as the base model to train the policy model.
During full fine-tuning, we use a batch size of 2,048 and a learning rate of 2 × 10−5 , training for one
epoch. A cosine annealing schedule is employed for learning rate, reaching 10% of its initial value
by the end of the epoch. Notably, the model training process does not incorporate EI.
Datasets. We use the STP dataset [Dong and Ma, 2025] as the seed and adopt BFS-Prover [Xin
et al., 2025] as the policy model for proof state exploration. We first generate the synthetic dataset
following the method in Section 3.1. Then, before the actual training begins, the dataset is further
combined with human-authored data from Mathlib, followed by deduplication and decontamination.
This results in a final training set comprising approximately 20 million proof transitions.
Baselines. We select two state-of-the-art models that also use tree search methods, InternLM2.5-
StepProver [Wu et al., 2024] and BFS-Prover [Xin et al., 2025], as main baseline models, applying
the same search budget in our experiments.
Environments. We develop DoBeVi (cf. Appendix A.3) as the basic interaction tool between the
model and the Lean 4 prover (v4.10.0).
Benchmarks, metrics and computation budgets. We evaluate on two popular benchmarks, MiniF2F
[Zheng et al., 2021] and ProofNet [Azerbayev et al., 2023a], using Pass@1 as the metric. We follow
the commonly adopted search budget in tree search methods: K × B × E, where K is the number of
searches per theorem (i.e., k in Pass@k); B is the beam size per expansion; and E is the maximum
number of expansions allowed in a single search.

4.2       Main results

Table 1 presents the results of our model alongside baseline methods on MiniF2F and ProofNet. We
fix K = 1 and E = 600 and adopt the beam sizes used in the original baseline papers. If a baseline
has reported results under the same computational budget, we directly use those results; otherwise,
we re-evaluate the baseline using our own tree search implementation under identical experimental
settings, including additional search techniques detailed in Appendix A.4.
The results demonstrate that our method achieves better evaluation performance even under a relatively
constrained computational budget without relying on EI. Moreover, under the fixed beam size setting,
the optimal beam sizes for our policy model are found to be 8 on MiniF2F and 32 on ProofNet,
respectively. By adopting our adaptive beam size strategy, we are able to further improve performance
without searching for the best beam size settings.

4.3       Discussions

Unlike whole-proof generation methods, the performance of tree search methods is influenced by a
variety of factors, in addition to the policy model. We found that the beam size is particularly critical,
sometimes even comparable in importance to the policy model’s capability. As shown in Table 1,
both our model and the baselines exhibit different optimal beam size choices across the MiniF2F
and ProofNet benchmarks. We attribute this primarily to differences in training data distribution.
Currently, most publicly available Lean 4 training datasets are derived from Lean-Workbook [Ying
et al., 2024], whose distribution resembles the MATH subset of MiniF2F. Consequently, using a
larger beam size in such settings tends to introduce redundant search branches, causing the search to
      4
    The implementation code is accessible at https://github.com/NJUDeepEngine/llm_based_atp. The
policy model is accessible at https://huggingface.co/NJUDeepEngine/llm_based_atp


                                                    7
Table 1: Overall evaluation results across MiniF2F-test and ProofNet-test. All baseline results
evaluated by us are marked with an asterisk (*), while the remaining results are directly imported
from the original papers.
                   Method                     Model Size       Budget         MiniF2F-test       ProofNet-test
        Llemma [Azerbayev et al., 2023b]         7B         1 × 32 × 100         26.23%                -
           ReProver [Yang et al., 2023]         229M            K=1              26.50%             13.80%
          Lean-STaR [Lin et al., 2024]           7B          64 × 1 × 50         46.30%                -
    InternLM2.5-StepProver[Wu et al., 2024]      7B         1 × 32 × 600      47.3% ± 1.1%     19.89% ± 0.68% *
          BFS-Prover[Xin et al., 2025]           7B          1 × 2 × 600    55.49% ± 0.61% *   12.37% ± 1.44% *
                                                             1 × 4 × 600    56.56% ± 1.13%     13.01% ± 0.79%
                                                             1 × 8 × 600    59.51% ± 0.79%     17.53% ± 0.26%
            Ours (fixed beam size)               7B
                                                            1 × 16 × 600    59.02% ± 1.13%     19.35% ± 0.96%
                                                            1 × 32 × 600     57.05% ± 0.4%     20.75% ± 0.94%
           Ours (adaptive beam size)             7B        K = 1, E = 600   60.74% ± 0.88%     21.18% ± 0.55%




waste the budget without improving results. In contrast, for benchmarks such as ProofNet, which
contain more out-of-distribution samples, increasing the beam size is necessary, which allows the
model to explore a broader set tactics in the hope of reaching intermediate proof states similar to
those encountered during training.
In tree search, a smaller beam size naturally makes the entire tree taller and thinner, resulting in longer
average search depths (cf. Appendix A.7). Moreover, if the first expansion results are suboptimal, the
subsequent search process may not reach proof finish at all. Therefore, when restricted to Pass@1, a
beam size of 2 leads to larger variance, often requiring an increase in K within the budget to reduce
the impact of randomness. This small beam size scenario is suitable when, during tree search, the
policy model encounters a state similar to one it has learned before and can confidently select a
proof step which likely leads to proof finish. Conversely, a larger beam size makes the tree structure
shallower and wider, reducing the average search depth but potentially introducing many useless
proof steps into the tree, lowering the search efficiency.
In addition, we adopt a standard formulation for the scoring function, which evaluates the tactic tj
rather than the new state sji+1 . As shown in Equation 1, the effectiveness of this scoring function
primarily stems from the fact that a higher value of P (tj | si ) indicates that the policy model is
more likely to have encountered proof states similar to si during training. As a result, it can, to some
extent, prioritize proof steps that are more helpful for completing the proof. However, we argue
that this scoring function still suffers from significant issues. For a detailed discussion and several
unsuccessful attempts, please refer to Appendix A.5.


5   Related Work

Automated theorem proving. ATP has been a classic research area which is historically dominated
by symbolic approaches [Pastre, 1993, Schürmann and Pfenning, 1998, Leino, 2013]. In recent years,
the rise of LLMs has spurred renewed interest. One representative work is GPT-f [Polu and Sutskever,
2020], which uses the Expert Iteration approach to train the LLM for next proof step generation based
on the current state, combined with tree search methods to prove theorems. Subsequent tree search
methods have followed similar ideas, e.g., Polu et al. [2022], Lample et al. [2022], Lin et al. [2024].
Additionally, some work improves tree search tailored in ATP. For example, Wu et al. [2024] uses the
DPO algorithm to train an auxiliary value network to evaluate intermediate proof states, avoiding the
issue of directly using raw beam search probabilities as scoring signals.
In contrast, whole-proof generation methods [Xin et al., 2024a, Lin et al., 2025, Zhang et al., 2025,
Wang et al., 2025a] aim to produce an entire proof in a single forward pass from the initial goal. While
these methods do not leverage intermediate proof states, they are typically more efficient and allow
for multiple rollouts to increase the likelihood of success. A notable example is DeepSeek-Prover-
V1.5 [Xin et al., 2024a], which enhances performance by inserting natural language chain-of-thought
(CoT) commentary into Lean 4 proofs during inference. Additionally, MA-LoT [Wang et al., 2025b]
introduces a multi-agent architecture where separate models are responsible for analyzing and revising
incorrect proofs, enabling iterative refinement toward a correct solution.


                                                           8
Data synthesis for theorem proving. One of the major bottlenecks in LLM-based automated
theorem proving remains the lack of high-quality training data, particularly for Lean 4, a relatively
new language with limited existing formalized data. Existing data generation methods can be broadly
categorized into two groups.
The first category leverages LLMs to generate Lean 4 problems by building on the abundance of
natural language mathematics. These approaches are generally referred to as autoformalization.
However, current efforts primarily focus on autoformalizing problem statements, with less attention
given to the autoformalization of proof processes [Wang et al., 2025a, Lu et al., 2024].
The second category bootstraps from a small set of existing Lean 4 problems to generate new ones
through iterative synthesis. These methods typically involve a two-model framework: one model
generates new conjectures, and the other attempts to prove them, enabling co-evolution of data and
model capabilities. For instance, STP [Dong and Ma, 2025] uses problems from the Lean-Workbook
dataset [Ying et al., 2024] as seeds. A conjecturer proposes conjectures related to the original
problems, while a prover attempts to validate them—allowing both the training set and the model to
be refined through this iterative process.

6   Limitations
Limited adaptivity in beam size selection. As discussed in Section 4.3, beam size is a critical factor
in the effectiveness of tree search. While our proposed strategy provides a simple and effective means
of dynamically adjusting the beam size, a more principled solution would involve training a dedicated
model that, given a current proof state, predicts the optimal beam size for the policy model to use.
Ideally, such a model would offer fully adaptive control during search. However, in practice, we
found this approach challenging to implement. The primary difficulty lies in collecting sufficient
high-quality training data for learning beam size prediction. Moreover, it is difficult for such a model
to operate independently of the policy model, since the optimal beam size can be highly dependent
on the specific behavior of the underlying policy model. As a result, we opted for a simple adaptive
beam size decay strategy that complements our data synthesis framework. Exploring how to build
more sophisticated, model-agnostic beam selection mechanisms, potentially via auxiliary learning
signals or joint training, remains an open direction for future work.
Potentially suboptimal scoring function. Most current tree search methods based on best-first
search apply the scoring function directly to the tactic or action, rather than to the resulting proof
state. We argue that a more general and expressive scoring function should evaluate the entire
transformation path from the root state s0 to the current state si , i.e.,

                                                                                                
                    score(si ) = f (s0 , t0 , s1 ), (s1 , t1 , s2 ), . . . , (si−1 , ti−1 , si ) .

Since this formulation may be too complex to implement in practice, we adopt a simplified approxima-
tion inspired by first-order Markov processes, assuming score(si ) = f (si−1 , ti−1 , si ). This structure
provides two key advantages: (1) it allows for immediate pruning of low-quality transformations
during search, saving computational budget; and (2) it supports path-level quality estimation via
                                 Pj                 Qj
aggregation, e.g., by computing n=1 score(sn ) or n=1 score(sn ) across the trajectory. Neverthe-
less, further exploration is needed to design more expressive, yet computationally feasible, scoring
functions that better capture long-range dependencies in proof trajectories.
Dependence on the seed dataset. A fundamental limitation of our data generation framework is
its dependence on the seed dataset. The synthesized data is effectively constrained to the local
neighborhood of the seed problems in the sample space. As a result, if the target problem lies far
from the seed set in terms of distribution or difficulty, our method may struggle to generate useful
intermediate states or transformations. In other words, under our current formulation, producing
examples that are significantly more difficult than those in the seed set remains an open challenge.

7   Conclusions
In this paper, we have presented a data synthesis method and an adaptive tree search pruning strategy
for automated theorem proving in Lean 4. Our proposed approach enables large-scale generation of


                                                          9
intermediate proof states and transformation steps without relying on ground-truth solutions, while
maintaining diversity in the synthetic data. Combining with the adaptive beam size strategy, our
method effectively balances exploration and exploitation throughout the tree search process. Together
with the developed DoBeVi Lean 4 interaction tool, we expect our contributions will support and
inspire further research within the ATP community, which is burgeoning but under development.




                                                 10
References
Fei Yu, Hongbo Zhang, Prayag Tiwari, and Benyou Wang. Natural language reasoning, a survey.
  ACM Computing Surveys, 56(12):1–39, 2024.
Panagiotis Giadikiaroglou, Maria Lymperaiou, Giorgos Filandrianos, and Giorgos Stamou. Puzzle
  solving using reasoning of large language models: A survey. arXiv preprint arXiv:2402.11291,
  2024.
Janice Ahn, Rishu Verma, Renze Lou, Di Liu, Rui Zhang, and Wenpeng Yin. Large language models
  for mathematical reasoning: Progresses and challenges. arXiv preprint arXiv:2402.00157, 2024.
Jia Li, Edward Beeching, Lewis Tunstall, Ben Lipkin, Roman Soletskyi, Shengyi Huang, Kashif
   Rasul, Longhui Yu, Albert Q Jiang, Ziju Shen, et al. Numinamath: The largest public dataset in
   ai4maths with 860k pairs of competition math problems and solutions. Hugging Face repository,
   13:9, 2024.
Junwei Liu, Kaixin Wang, Yixuan Chen, Xin Peng, Zhenpeng Chen, Lingming Zhang, and Yiling
  Lou. Large language model-based agents for software engineering: A survey. arXiv preprint
  arXiv:2409.02977, 2024.
Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi, Luke
  Zettlemoyer, Percy Liang, Emmanuel Candès, and Tatsunori Hashimoto. s1: Simple test-time
  scaling. arXiv preprint arXiv:2501.19393, 2025.
Violet Xiang, Charlie Snell, Kanishk Gandhi, Alon Albalak, Anikait Singh, Chase Blagden, Duy
  Phung, Rafael Rafailov, Nathan Lile, Dakota Mahan, et al. Towards system 2 reasoning in llms:
  Learning how to think with meta chain-of-though. arXiv preprint arXiv:2501.04682, 2025.
Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language. In
  Automated Deduction–CADE 28: 28th International Conference on Automated Deduction, Virtual
  Event, July 12–15, 2021, Proceedings 28, pages 625–635. Springer, 2021.
Lawrence C Paulson. Isabelle: A generic theorem prover. Springer, 1994.
Bruno Barras, Samuel Boutin, Cristina Cornes, Judicaël Courant, Jean-Christophe Filliatre, Eduardo
  Gimenez, Hugo Herbelin, Gerard Huet, Cesar Munoz, Chetan Murthy, et al. The Coq proof
  assistant reference manual: Version 6.1. PhD thesis, Inria, 1997.
Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang,
   Zhe Fu, Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang, Yuxuan Liu,
  Wenjun Gao, Daya Guo, and Chong Ruan. Deepseek-prover-v2: Advancing formal mathematical
   reasoning via reinforcement learning for subgoal decomposition, 2025. URL https://arxiv.
   org/abs/2504.21801.
Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu, Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou Xia,
  Danqi Chen, Sanjeev Arora, et al. Goedel-prover: A frontier model for open-source automated
  theorem proving. arXiv preprint arXiv:2502.07640, 2025.
Huajian Xin, ZZ Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue
  Zhang, Xuan Lu, Qiushi Du, et al. Deepseek-prover-v1. 5: Harnessing proof assistant feedback for
  reinforcement learning and monte-carlo tree search. arXiv preprint arXiv:2408.08152, 2024a.
Haiming Wang, Huajian Xin, Zhengying Liu, Wenda Li, Yinya Huang, Jianqiao Lu, Zhicheng
 Yang, Jing Tang, Jian Yin, Zhenguo Li, et al. Proving theorems recursively. arXiv preprint
  arXiv:2405.14414, 2024.
Chenyang An, Zhibo Chen, Qihao Ye, Emily First, Letian Peng, Jiayun Zhang, Zihan Wang, Sorin
  Lerner, and Jingbo Shang. Learn from failure: Fine-tuning llms with trial-and-error data for
  intuitionistic propositional logic proving. arXiv preprint arXiv:2404.07382, 2024.
Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li,
  and Xiaodan Liang. Deepseek-prover: Advancing theorem proving in llms through large-scale
  synthetic data. arXiv preprint arXiv:2405.14333, 2024b.


                                               11
Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li, Kristin Lauter, Swarat Chaudhuri, and Dawn
  Song. Formal mathematical reasoning: A new frontier in ai. arXiv preprint arXiv:2412.16075,
  2024a.
The mathlib Community. The Lean mathematical library. In Proceedings of the 9th ACM SIGPLAN
  International Conference on Certified Programs and Proofs, CPP 2020, pages 367–381, New
  York, NY, USA, 2020. Association for Computing Machinery. ISBN 9781450370974. doi:
  10.1145/3372885.3373824. URL https://doi.org/10.1145/3372885.3373824.
Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus Rabe, Charles Staats, Mateja Jamnik, and
  Christian Szegedy. Autoformalization with large language models. Advances in Neural Information
  Processing Systems, 35:32353–32368, 2022.
Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang, Dahua Lin, and Kai Chen. Lean workbook:
 A large-scale lean problem set formalized from natural language math problems. arXiv preprint
  arXiv:2406.03847, 2024.
Logan Murphy, Kaiyu Yang, Jialiang Sun, Zhaoyu Li, Anima Anandkumar, and Xujie Si. Autofor-
  malizing euclidean geometry. arXiv preprint arXiv:2405.17216, 2024.
Kefan Dong and Tengyu Ma. Stp: Self-play llm theorem provers with iterative conjecturing and
  proving. arXiv e-prints, pages arXiv–2502, 2025.
Gabriel Poesia, David Broman, Nick Haber, and Noah Goodman. Learning formal mathematics from
  intrinsic motivation. Advances in Neural Information Processing Systems, 37:43032–43057, 2024.
Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving.
  arXiv preprint arXiv:2009.03393, 2020.
Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor Babuschkin, and Ilya
  Sutskever. Formal mathematics statement curriculum learning. arXiv preprint arXiv:2202.01344,
  2022.
Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan Ying, Jiayu Wang, Dahua Lin, and Kai Chen.
  Internlm2. 5-stepprover: Advancing automated theorem proving via expert iteration on large-scale
  lean problems. arXiv preprint arXiv:2410.15700, 2024.
Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang Wu, Xia Xiao, Yifan Sun, Shen Zheng, and Kai
  Shen. Bfs-prover: Scalable best-first tree search for llm-based automatic theorem proving. arXiv
  preprint arXiv:2502.03438, 2025.
Chris Hokamp and Qun Liu. Lexically constrained decoding for sequence generation using grid
  beam search. arXiv preprint arXiv:1704.07138, 2017.
An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao, Bowen Yu, Chengpeng Li, Dayiheng Liu,
 Jianhong Tu, Jingren Zhou, Junyang Lin, Keming Lu, Mingfeng Xue, Runji Lin, Tianyu Liu,
 Xingzhang Ren, and Zhenru Zhang. Qwen2.5-math technical report: Toward mathematical expert
  model via self-improvement. arXiv preprint arXiv:2409.12122, 2024b.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: a cross-system benchmark for
  formal olympiad-level mathematics. arXiv preprint arXiv:2109.00110, 2021.
Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W Ayers, Dragomir Radev, and
  Jeremy Avigad. Proofnet: Autoformalizing and formally proving undergraduate-level mathematics.
  arXiv preprint arXiv:2302.12433, 2023a.
Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster, Marco Dos Santos, Stephen McAleer, Albert Q
  Jiang, Jia Deng, Stella Biderman, and Sean Welleck. Llemma: An open language model for
  mathematics. arXiv preprint arXiv:2310.10631, 2023b.
Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J
  Prenger, and Animashree Anandkumar. Leandojo: Theorem proving with retrieval-augmented
  language models. Advances in Neural Information Processing Systems, 36:21573–21612, 2023.


                                               12
Haohan Lin, Zhiqing Sun, Sean Welleck, and Yiming Yang. Lean-star: Learning to interleave thinking
  and proving. arXiv preprint arXiv:2407.10040, 2024.
Dominique Pastre. Automated theorem proving in mathematics. Annals of Mathematics and Artificial
  Intelligence, 8:425–447, 1993.
Carsten Schürmann and Frank Pfenning. Automated theorem proving in a simple meta-logic for lf.
  In International Conference on Automated Deduction, pages 286–300. Springer, 1998.
K Rustan M Leino. Automating theorem proving with smt. In International Conference on Interactive
  Theorem Proving, pages 2–16. Springer, 2013.
Guillaume Lample, Timothee Lacroix, Marie-Anne Lachaux, Aurelien Rodriguez, Amaury Hayat,
 Thibaut Lavril, Gabriel Ebner, and Xavier Martinet. Hypertree proof search for neural theorem
  proving. Advances in neural information processing systems, 35:26337–26349, 2022.
Jingyuan Zhang, Qi Wang, Xingguang Ji, Yahui Liu, Yang Yue, Fuzheng Zhang, Di Zhang, Guorui
   Zhou, and Kun Gai. Leanabell-prover: Posttraining scaling in formal reasoning. arXiv preprint
   arXiv:2504.06122, 2025.
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,
  Marina Vinyes, Zhenzhe Ying, Zekai Zhu, et al. Kimina-prover preview: Towards large formal
  reasoning models with reinforcement learning. arXiv preprint arXiv:2504.11354, 2025a.
Ruida Wang, Rui Pan, Yuxin Li, Jipeng Zhang, Yizhen Jia, Shizhe Diao, Renjie Pi, Junjie Hu, and
  Tong Zhang. Ma-lot: Multi-agent lean-based long chain-of-thought reasoning enhances formal
  theorem proving. arXiv preprint arXiv:2503.03205, 2025b.
Jianqiao Lu, Yingjia Wan, Zhengying Liu, Yinya Huang, Jing Xiong, Chengwu Liu, Jianhao Shen,
   Hui Jin, Jipeng Zhang, Haiming Wang, et al. Process-driven autoformalization in lean 4. arXiv
   preprint arXiv:2406.01940, 2024.
Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E.
 Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model
 serving with pagedattention. In Proceedings of the ACM SIGOPS 29th Symposium on Operating
 Systems Principles, 2023.
Haiming Wang, Huajian Xin, Chuanyang Zheng, Lin Li, Zhengying Liu, Qingxing Cao, Yinya Huang,
  Jing Xiong, Han Shi, Enze Xie, et al. Lego-prover: Neural theorem proving with growing libraries.
  arXiv preprint arXiv:2310.00656, 2023.
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
  Mingchuan Zhang, YK Li, Y Wu, et al. Deepseekmath: Pushing the limits of mathematical
  reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024.




                                                13
A      Appendix

A.1     Prompts used for policy model

For the policy model, we use the similar prompt template as in GPT-f [Polu and Sutskever, 2020],
where the prompt only describes the current proof state without introducing any additional information.
The template and an example are shown below:


    Template:

    [GOAL]
    <state>
    [PROOFSTEP]


    Example: (aime_1983_p1 in MiniF2F)

      [GOAL]
      xyzw:N
      ht : 1 < x ∧ 1 < y ∧ 1 < z
      hw : 0 ≤ w
      h0 : Real.log ↑w / Real.log ↑x = 24
      h1 : Real.log ↑w / Real.log ↑y = 40
      h2 : Real.log ↑w / Real.log (↑x * ↑y * ↑z) = 12
      ⊢ Real.log ↑w / Real.log ↑z = 60
      [PROOFSTEP]



A.2     Case study

Below we present two example proofs generated by our model on MiniF2F and ProofNet, respectively.


      Example: amc12a_2009_p6 in MiniF2F

      theorem amc12a_2009_p6
        (m n p q : R) R
        (h0 : p = 2 ^ m)
        (h1 : q = 3 ^ n) :
        p^(2 * n) * (q^m) = 12^(m * n) := by
          subst_vars
          simp [mul_comm, Real.rpow_mul]
          have h0 : (0 : R) < 2 := by norm_num
          have h1 : (0 : R) < 3 := by norm_num
          field_simp [Real.rpow_def_of_pos, h0, h1]
          rw [← Real.exp_add]
          rw [mul_comm]
          rw [
               show (n * 2 * (Real.log 2 * m) + Real.log 3 * n * m) = (Real.log 12 *
            m * n) by
               have h3 : Real.log 12 = Real.log (2 ^ 2 * 3) := by norm_num
               rw [h3]
               field_simp [Real.log_mul, Real.log_rpow, mul_assoc]
               ring_nf
          ]




                                                  14
      Example: Rudin_exercise_4_11a in ProofNet
      theorem exercise_4_11a
          {X : Type*} [MetricSpace X]
          {Y : Type*} [MetricSpace Y]
          (f : X → Y) (hf : UniformContinuous f)
          (x : N → X) (hx : CauchySeq x) :
          CauchySeq (λ n => f (x n)) :=
              rw [Metric.cauchySeq_iff] at hx ⊢,
              intro ε hε,
              obtain ⟨δ, hδ, hδ’⟩ := Metric.uniformContinuous_iff.mp hf ε hε,
              obtain ⟨ N, hN ⟩ := hx δ hδ,
              exact ⟨ N, fun m hm n hn => hδ’ <| hN _ hm _ hn ⟩



A.3     Our DoBeVi REPL

To enable better interaction with Lean 4 prover and visualization of the search process, we develop
Dojo-BeamSearch-Visualization (DoBeVi) REPL, a tool built upon a simplified and customized
version of LeanDojo [Yang et al., 2023]. The tool consists of two main components: interactive
theorem proving environment and visualization module.

A.3.1    Interactive theorem proving environment
In the component of interactive theorem proving environment, we present a streamlined adaptation of
the LeanDojo framework, establishing a lightweight but robust foundation for distributed interactive
theorem proving. Our implementation retains two core functionalities from LeanDojo:

        • AST extraction and semantic analysis of target Lean files with precise theorem declaration
          identification.
        • Core interactive logic execution via the lean_dojo_repl custom tactic.

In our DoBeVi REPL refines the architecture by removing three categories of non-essential compo-
nents from LeanDojo:

        • Partial initialization workflows.
        • Premise and dependency tracking modules.
        • Secondary data processing components.

Then we add the following new useful features for better interaction with the prover:

        • Proof state tracking using globally unique identifiers (excluding ProofFinish nodes).
        • Decoupled session management architecture enabling parallel theorem processing.
        • Resilient recovery mechanisms for:
            – Tactic execution timeouts.
            – Lean process failures.

After that, the DoBeVi provides an optimized architecture that reduces runtime overhead while
maintaining stable interfaces for integrating model-based theorem proving components.

A.3.2    Visualization of the search tree
The visualization module serves to clearly illustrate the entire proof search process by graphically
representing the evolving search tree structure. In this module, each proof state encountered during
the search is abstracted as a node in a graph, and each proof step applied to transition between states
is represented as a directed edge. To better reflect the semantics of the search process, nodes are
categorized into three types:

        • Prooffinished node: Indicates that the proof has been successfully completed at this node.


                                                  15
         • Error node: Represents a failed search node due to errors such as Lean syntax errors,
           timeouts, or unexpected crashes of the Lean process.
         • Open node: Denotes an intermediate state that can still be expanded during the search.

Similarly, edges are divided into two categories:

         • Tree edge: Connects to a previously unseen state, resulting in the creation of a new node.
           Tree edges are essential for expanding the search space and discovering new proof paths.
         • Back edge: Leads to a state that has already been visited earlier in the search process. Back
           edges help identify convergence and redundancy in the search, enabling cycle detection and
           pruning.

Although the structure is referred to as a "search tree", it is, strictly speaking, a directed acyclic graph
(DAG). This distinction stems from two key characteristics:

         • Non-tree structure: Different but semantically similar proof steps may both lead from the
           same current state to the same next state, resulting in multiple paths converging to a single
           node. The property that there are no loops inside the tree is violated.
         • Acyclic design: Cycles in the search path (e.g., s1 → s2 → · · · → s1 ) are explicitly
           detected and pruned in advance, as we consider such loops to be semantically meaningless
           and computationally redundant.

This visualization module is part of the DoBeVi system, which is organized in a modular fashion.
The system consists of the following four components:

         • Search tree module: Defines the core data structures, including Node, Edge, and the overall
           Tree layout.
         • Tactic generation module: Interfaces with LLMs. Given the current state as input, it returns
           a set of candidate proof steps along with their associated scores. This module is extensible
           and allows users to integrate custom models as needed.
         • Search strategy module: Specifies the logic for node expansion. We provide several default
           strategies such as Best-First Search, which always expands the node with the highest current
           score that has not yet been explored. Users are free to implement additional strategies
           tailored to their tasks.
         • Visualization module: Responsible for rendering the entire search tree graphically, enabling
           an intuitive understanding of the search process and state transitions.

Figure 3 presents the visualization result of applying the Best-First Search strategy to the problem
amc12_2000_p6 from the MiniF2F dataset. Node IDs increment from 0, indicating the order in
which nodes were expanded during the search. In this example, the search sequentially expanded
nodes with IDs 0, 3, 11, 14, 16, 19, and 21, ultimately completing the proof successfully after the
seventh expansion.
In summary, this module visualizes the search tree to record the entire search process, making it
easier to review after execution and to inspire the design of better search and pruning strategies.

A.4     Detailed experimental settings

In our experiments, similar to most tree search methods, we separate the tree search and model
generation components to improve overall evaluation efficiency. We refer to the implementation
in ReProver [Yang et al., 2023] and use Python’s Ray 5 and vLLM [Kwon et al., 2023] libraries
to implement the system. We launch multiple processes for tree search, where each process pulls
unprocessed theorems from a queue and uses LeanDojo as the interaction tool between Python and the
Lean 4 prover. When fetching proof steps, multiple tree search workers share several asynchronous
LLM engines launched by vLLM, with one LLM instance deployed per GPU. In practice, we use
dozens of tree search processes to maximize GPU utilization. For each search, we set a global timeout
of 1,800 seconds; if the search time exceeds this value, the search process is forcibly terminated.
   5
       https://github.com/ray-project/ray


                                                    16
                                                                                                                                                                                                                                                                 Nodes, red elliptical nodes indicate Error Nodes, and green nodes denote ProofFinished Nodes.
                                                                                                                                                                                                                                                                 Figure 3: A example of search tree(amc12_2000_p6 in MiniF2F). Rectangular nodes represent Open

                                                                                                                                                                                                                                                                 Edges are labeled with the applied tactic and its associated beam probability (beam_prob). Each
                                                                                               Internal
                                                                                                 id=0
                                                                                             score=0.00
                                         intro h          rintro h norm_num         norm_num at h₁ h₂ ⊢         rcases h₀ with ⟨hp, hq⟩      rcases h₁ with ⟨hp1, hp2⟩            rcases h₁ with ⟨hp₁, hp₂⟩      rcases h₁ with ⟨h₁_0, h₁_1⟩
                                          0.04              0.08      0.01                 0.00                          0.12                          0.02                                 0.01                            0.00
                                               Internal                 Internal                              Internal                      Internal                          Internal                          Internal
                                                 id=1                     id=2                                  id=3                          id=4                              id=5                              id=6
                                             score=0.04               score=0.01                            score=0.12                    score=0.02                        score=0.01                        score=0.00
         rcases h₁ with ⟨hp_4, hp_18⟩    rcases h₁ with ⟨hp₁, hp₈⟩      rcases h₁ with ⟨h₁_left, h₁_right⟩ rcases h₁ with ⟨h1_left, h1_right⟩               rcases h₁ with ⟨hp1, hp2⟩           have h₃ := hp.two_le        rcases h₁ with ⟨hp_left, hp_right⟩
                     0.02                          0.00                               0.16                               0.02                                         0.36                              0.05                              0.02
  Internal                        Internal                        Internal                                    Internal                                    Internal                         Internal                      Internal
    id=7                            id=8                            id=9                                       id=10                                       id=11                            id=12                         id=13
score=0.14                      score=0.12                      score=0.28                                  score=0.14                                  score=0.48                       score=0.17                    score=0.14
                                                                                                                                                             rcases h₂ with ⟨hq1, hq2⟩
                                                                                                                                                                       0.25
                                                                                                                                                          Internal
                                                                                                                                                           id=14
                                                                                                                                                        score=0.73
                                                                                            rcases hp.eq_two_or_odd with (rfl | hpo) have h₁ := hp.two_le                have hp' := Nat.prime_def_lt.mp hp                have h₀ := Nat.Prime.two_le hp
                                                                                                             0.09                            0.86                                       0.01                                            0.04




                                                                                                                                                                                                                                                                 node is annotated with its unique id and current score.
                                                                                       Internal                                         Internal                       Internal                                       Internal
                                                                                        id=15                                            id=16                          id=17                                          id=18
                                                                                     score=0.82                                       score=1.59                     score=0.74                                     score=0.77




                                                                                                                                                                                                                                                                                                                                                                   17
                                                                                                                 have h₂ := hq.two_le      have h₂ := Nat.Prime.two_le hq             have h₂ := hq.one_lt
                                                                                                                         0.52                           0.22                                  0.04
                                                                                                                           Internal                                                  Internal
                                                                                                                            id=19                                                     id=20
                                                                                                                         score=2.11                                                score=1.64
                                                                                                                                                                have h₃ : (p * q - (p + q)) < 195 := by
                                                                                                                                                                               cases p with
                                                                                                                                                                            | zero => omega
                                                                                                                                                                               | succ p' =>
                                                                                                                                                                                cases q with
                                                                                                           interval_cases p have h₃ := hp.two_le
                                                                                                                                                                             | zero => omega
                                                                                                                 0.48               0.04
                                                                                                                                                                                | succ q' =>
                                                                                                                                                                          norm_num at hp1 hq1
                                                                                                                                                                   have : p' * q' < 360 := by nlinarith
                                                                                                                                                                                    omega
                                                                                                                                                                                   0.00
                                                                                                     Internal              Internal
                                                                                                      id=21                 id=22                       ✗LeanError
                                                                                                   score=2.59            score=2.15
                                                                                     all_goals decide all_goals interval_cases q <;> decide              all_goals interval_cases q <;> norm_num [Nat.Prime] at * <;> omega
                                                                                           0.43                        0.26                                                               0.08
                                                                             ✗LeanError            ✗LeanError
                                                                                                                                                       ✓Proof
                                                                                                                                                       id=23
For each proof step, we impose a timeout of 20 seconds. While there are occasional cases - such
as when using aesop - where longer execution times may be required, we consider any proof step
exceeding this threshold as a timeout. This constraint is intended to prevent individual proof steps
from disproportionately consuming the overall time budget.
During tree search, we use the REPL functionality provided by DoBeVi (Appendix A.3). When
executing proof steps, errors can broadly be categorized into two types: (1) syntax errors or similar
issues that directly cause the Lean 4 prover to return an error, which are usually caught quickly with
an error message; and (2) timeout errors. To prevent infinite loops caused by certain tactics, we set a
timeout for tactic execution. If such a timeout occurs, the Lean 4 prover becomes unable to execute
new proof steps, forcing the entire proof process to stop. To handle this, we save the proof context
before executing each tactic; if a timeout occurs, we restart the Lean REPL environment and restore
the context. This avoids cases where a proof that should have succeeded with tree search ultimately
fails just because a faulty tactic caused the Lean 4 prover to hang.
In addition, based on observations of certain failure cases during tree search, we identified an important
phenomenon: erroneous proof steps tend to appear in batches. Specifically, when performing beam
search from an proof state, if several consecutive proof steps are incorrect, it is highly likely that the
remaining proof steps in the beam will also be incorrect. This pattern may stem from the fact that the
current proof state represents an out-of-distribution input for the policy model, making it difficult
for the model to generate valid Lean 4 code. Under such circumstances, these erroneous proof steps
can substantially consume the global timeout allocated for the tree search, leading to inefficient
exploration. To mitigate this issue, we adopt an early termination strategy: during expansion at a
given state, if the number of incorrect child nodes exceeds a predefined threshold (usually 0.5×
beam size), we immediately discard the current node from further search. We found that this pruning
technique did not degrade overall proving performance while significantly reducing computational
time.
Regarding the choice of hyperparameters in the adaptive beam size strategy, we set Bmax = 16,
Bmin = 4, and λ = 15 for MiniF2F, and Bmax = 48, Bmin = 24, and λ = 2 for ProofNet.


A.5   Unsuccessful attempts and discussions

Separating tactics and premises. In our early experiments, we explored a more straightforward
separation of tactics and premises. Specifically, we adopted a two-model design: one model directly
outputs a valid tactic to serve as the starting token of the code, while a second model, analogous to
the policy model, completes the required premises. However, this approach yielded unsatisfactory
results. We frequently observed that the second model either failed to generate complete premises or
produced outputs that violated the Lean 4 grammar. A key challenge lies in the highly imbalanced
data distribution for a model that generates only tactics without premises. To quantify this imbalance,
we analyzed the STP dataset and computed the tactic usage statistics, presented in Appendix A.6.
For example, tactics like rw and have appear in nearly every proof context, leading the model to
overwhelmingly favor these high-frequency tactics. In contrast, the policy model must guide the proof
state toward completion, which does not always align with simply selecting the most common tactics.
This mismatch introduces conflicting objectives that ultimately degrade performance. Therefore,
we conclude that forcibly separating the generation of tactics and premises is infeasible. Instead, it
may be more effective to adopt external augmentation strategies, such as the retrieval-augmented
generation (RAG) method in Yang et al. [2023] or the lemma library construction approach in Wang
et al. [2023].
An ineffective scoring function. One major drawback of tree search methods compared to whole-
proof methods lies in the complexity of the neural-symbolic system: it involves many interacting
components, making it difficult to diagnose failure modes when performance is suboptimal. In some
cases, the coupling between components may even be inherently unavoidable. As discussed in the
main text, we identify several key factors in tree search methods that have a non-negligible impact on
performance:


       • Policy model. As the actor in the system, the policy model is clearly the most critical
         determinant of overall performance.


                                                   18
       • Scoring function (sometimes value network). The scoring function determines the order
         in which nodes are expanded within the tree structure. In some cases, a value network may
         be used for scoring instead of a rule-based method.
       • Beam size. The beam size represents a special type of budget. As discussed in Section 4.3,
         increasing the beam size does not necessarily lead to better results. On the contrary, for
         certain settings, a small beam size (such as 4) can sometimes unlock greater potential from
         the policy model. Moreover, the empirically optimal beam size varies across benchmarks
         and is not a fixed value.
       • Other budget-related factors. These include parameters like K, E, and the timeout
         threshold. Compared to the previous factors, these are relatively straightforward: given fixed
         settings for other components, larger budgets generally increase the likelihood of achieving
         better results.

In our early experiments, we hypothesized that the problem setting resembled reinforcement learning,
and thus sought inspiration from algorithms such as GRPO Shao et al. [2024]. We aimed to avoid
introducing a separate value network, instead using the average performance of a set of actions
generated by the actor as a scoring criterion. Concretely, for any intermediate proof state s, we
computed the following score:

                                                  B
                                               1 X
                                  score(s) =         log Pθ (ti | s)                               (3)
                                               B i=1

Here, θ denotes the policy model’s parameters, and Pθ (ti | s) represents the joint probability of
the i-th beam. The intuition behind this scoring function is that, on an average sense, higher beam
probabilities suggest that the policy model is more likely to have encountered similar examples
during training. Therefore, the current proof state s is more likely to lie on a path leading to proof
completion.
However, subsequent experiments indicate that the evaluation results obtained using this scoring
function are nearly indistinguishable from those derived using Equation 1, suggesting that this
approach may not be particularly effective within the context of tree search methods.
Dynamic beam size via top_p strategy. Another adaptive beam search strategy we explored is
inspired by the top_p (nucleus sampling) strategy commonly used in decoding. Specifically, after
normalizing the joint probabilities of each beam, we sort the beams by their joint probabilities and
then filter out beams with lower probabilities according to the top_p threshold.
Considering all of the strategies we experimented with, we conclude that the scoring function
(Equation 1) used in current tree search methods still suffers from significant shortcomings. As a
result, the experimental outcomes of these various approaches showed little impact on performance.

A.6   Tactic usage statistics on the STP dataset

We performed a comprehensive scan of all tactics used across the entire STP dataset, identifying a
total of 173 unique tactics. By applying a threshold of P = 0.999 under the top_p strategy to exclude
infrequently used tactics, we obtained a final set of 60 common tactics. The frequency distribution of
these tactics is shown in Figure 4.

A.7   Search depth statistics on the MiniF2F benchmark

We conducted experiments using our policy model on the MiniF2F benchmark with varying beam
sizes during search. The results, shown in Figure 5, indicate that under a fixed maximum number of
expansions, smaller beam sizes tend to produce proving paths with greater search depth.




                                                 19
                                                                                                                          Frequency




                                                                                                                0
                                                                                                                     20
                                                                                                                          40
                                                                                                                                      60
                                                                                                                                               80
                                                                                                                                                                                                                                                                                                            Frequency




                                                                                                                                                                                                                                                                                       0.00
                                                                                                                                                                                                                                                                                              0.05
                                                                                                                                                                                                                                                                                                     0.10
                                                                                                                                                                                                                                                                                                                        0.15
                                                                                                                                                                                                                                                                                                                               0.20
                                                                                                                                                                                                                                                                                                                                      0.25




                                                                                                             1
                                                                                                                                                                                                                                                                 no h
                                                                                                                                                                                                                                                                     rm ave
                                                                                                                                                                                                                                                                     nl _num




                                                                                                             2
                                                                                                                                                                                                                                                                    po inarit
                                                                                                                                                                                                                                                                        sit h
                                                                                                                                                                                                                                                                            ivi
                                                                                                                                                                                                                                                                                 ty
                                                                                                                                                                                                                                                                       lin rw
                                                                                                                                                                                                                                                                     simarith
                                                                                                                                                                                                                                                                           p_a




                                                                                                             3
                                                                                                                                                                                                                                                                           sim ll
                                                                                                                                                                                                                                                                          ap p
                                                                                                                                                                                                                                                                               p
                                                                                                                                                                                                                                                                          ex ly
                                                                                                                                                                                                                                                                               a
                                                                                                                                                                                                                                                                  fi i ct
                                                                                                                                                                                                                                                                co eld_sntro




                                                                                                             4
                                                                                                                                                                                                                                                                    ns im
                                                                                                                                                                                                                                                                       tru p
                                                                                                                                                                                                                                                                       omctor
                                                                                                                                                                                                                                                                       rin ega
                                                                                                                                                                                                                                                                            g
                                                                                                                                                                                                                                                                         ca _nf




                                                                                                             5
                                                                                                                                                                                                                                                                        rcases'
                                                                                                                                                                                                                                                                               se
                                                                                                                                                                                                                                                                             c s
                                                                                                                                                                                                                                                                 no ca alc
                                                                                                                                                                                                                                                                     rm ses
                                                                                                                                                                                                                                                                           _ca
                                                                                                                                                                                                                                                                       g




                                                                                                             6
                                                                                                                                                                                                                                                            int con st
                                                                                                                                                                                                                                                               erv gr
                                                                                                                                                                                                                                                                     al_ rin
                                                                                                                                                                                                                                                                    all caseg
                                                                                                                                                                                                                                                                        _go s
                                                                                                                                                                                                                                                                        ref als
                                                                                                                                                                                                                                                                              in




                                                                                                             7
                                                                                                                                                                                                                                                                          rin e'
                                                                                                                                                                                                                                                                                tr
                                                                                                                                                                                                                                                                    by uso
                                                                                                                                                                                                                                                          ex            _
                                                                                                                                                                                                                                                             ac casee
                                                                                                                                                                                                                                                                t_m sim s
                                                                                                                                                                                                                                                                      o
                                                                                                                                                                                                                                                                  ind d_capa




                                                                                                           8
                                                                                                                                                                                                                                                                        uc st
                                                                                                                                                                                                                                                                            t




20
                                                                                                                                                                                                                                                                        ob ion'
                                                                                                                                                                                                                                                                             t
                                                                                                                                                                                                                                                                         ae ain




                                                                                                                                                                                                                                                 Tactics
                                                                                                                                                                                                                                                                              sop




                                                                                                            Depth
                                                                                                                                                                                                                                                             co d le




                                                                                                                 9
                                                                                                                                                                                                                                                                 ntr ec t
                                                                                                                                                                                                                                                                     ad ide
                                                                                                                                                                                                                                                                          ict
                                                                                                                                                                                                                                                                 by ion
                                                                                                                                                                                                                                                               ass_con rfl
                                                                                                                                                                                                                                                                     um tra
                                                                                                                                                                                                                                                                           pti !




                                                                                                             10
                                                                                                                                                                                                                                                                          ha on
                                                                                                                                                                                                                                                                               ve
                                                                                                                                                                                                                                                                                   I
                                                                                                                                                                                                                                                                      e cas
                                                                                                                                                                                                                                                                   ind xfalse
                                                                                                                                                                                                                                                                         uc o
                                                                                                                                                                                                                                                                             tio
                                                                                                                                                                                                                                                                                  n




                                                                                                             11
                                                                                                                                                                                                                                                                         ref try
                                                                                                                                                                                                                                                                               in
                                                                                                                                                                                                                                                                            ne e
                                                                                                                                                                                                                                                                  by subxt
                                                                                                                                                                                                                                                                      _co st
                                                                                                                                                                                                                                                                            nt




                                                                                                             13
                                                                                                                                                                                                                                                                           clera
                                                                                                                                                                                                                                                                  co intr ar
                                                                                                                                                                                                                                                                      nti os
                                                                                                                                                                                                                                                                           nu
                                                                                                                                                                                                                                                                          tauity
                                                                                                                                                                                                                                                                  s to




                                                                                                             15
                                                                                                                                                                                                                                                               co peci left
                                                                                                                                                                                                                                                                   ntr ali
                                                                                                                                                                                                                                                                       ap ze
                                                                                                                                                                                                                                                                            os
                                                                                                                                                                                                                                                      lin                  r e!
                                                                                                                                                                                                                                                         ea p ight
                                                                                                                                                                                                                                                            r_c u e
                                                                                                                                                                                                                                                                      s
                                                                                                                                                                                                                                                                om h_ xt




                                                                                                             16
                                                                                                                                                                                                                                                                     bin neg
                                                                                                                                                                                                                                                                   ap ati
                                                                                                                                                                                                                                                                      ply on
                                                                                                                                                                                                                                                                            _fu
                                                                                                                                                                                                                                                                                  n




                                                                                                             17
                                                                                                                                                                Figure 4: Distribution of the top 60 most frequent tactics in the STP dataset.




                                                                                                                                           B=8
                                                                                                                                           B=4
                                                                                                                                           B=2


                                                                                                                                           B = 32
                                                                                                                                           B = 16




     the MiniF2F benchmark, with the maximum number of expansions fixed at 600 (E = 600).
                                                                                                             24
                                                                                                                                           Adaptive Beam Size




     Figure 5: Frequency distribution of search depths of proving paths generated by our policy model on
