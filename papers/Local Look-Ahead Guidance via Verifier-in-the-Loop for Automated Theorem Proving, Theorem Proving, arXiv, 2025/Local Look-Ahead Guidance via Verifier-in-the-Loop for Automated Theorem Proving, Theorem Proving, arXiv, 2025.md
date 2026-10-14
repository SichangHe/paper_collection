                                                 Local Look-Ahead Guidance via Verifier-in-the-Loop for Automated
                                                                       Theorem Proving

                                                           Sara Rajaee* †1 , Kumar Pratik∗2 , Gabriele Cesa2 , Arash Behboodi2
                                                                  Language Technology Lab, University of Amsterdam1
                                                                          Qualcomm AI Research‡ , Amsterdam2
                                                                                   s.rajaee@uva.nl
                                                                  {kpratik, gcesa, behboodi}@qti.qualcomm.com


                                                                     Abstract                         Silver et al., 2018). These solutions are usually
                                                                                                      verified by formal proof verification systems like
                                                 The most promising recent methods for AI rea-
                                                                                                      Lean (Moura and Ullrich, 2021) or Coq (Coq De-
arXiv:2503.09730v2 [cs.AI] 24 Jun 2025




                                                 soning require applying variants of reinforce-
                                                 ment learning (RL) either on rolled out trajec-      velopment Team, 2024). Relying on Reinforcement
                                                 tories from the LLMs, even for the step-wise         Learning (RL) is advantageous in terms of data ef-
                                                 rewards, or large quantities of human-annotated      ficiency but comes with high computational and
                                                 trajectory data. The reliance on the rolled-out      training costs (Gloeckle et al., 2024). Part of this
                                                 trajectory renders the compute cost and time         complexity is related to the necessity of rolling out
                                                 prohibitively high. In particular, the correctness   the proofs and computing rewards from successful
                                                 of a reasoning trajectory can typically only be
                                                                                                      episodes.
                                                 judged at its completion, leading to sparse re-
                                                 wards in RL or requiring expensive synthetic            In contrast, ReProver (Yang et al., 2023) takes a
                                                 data generation in expert iteration-like methods.    simpler supervised training approach, specifically
                                                 In this work, we focus on the Automatic The-         imitation learning, paired with premise retrieval
                                                 orem Proving (ATP) task and propose a novel          methods. The key components of this proof sys-
                                                 verifier-in-the-loop design, which, unlike exist-    tem are as follows: the theorem we would like to
                                                 ing approaches that leverage feedback on the         prove, tactics that are actions toward the final proof
                                                 entire reasoning trajectory, employs an auto-        and itself consist of a set of goals to be proven,
                                                 mated verifier to give intermediate feedback
                                                                                                      premises that are used to prove goals, and the state
                                                 at each step of the reasoning process. Using
                                                 Lean as the verifier, we empirically show that       of the proof which includes the set of goals that
                                                 the step-by-step local verification produces a       are still unproven. The approach consists of retriev-
                                                 global improvement in the model’s reasoning          ing the relevant premises from a database given
                                                 accuracy and efficiency.                             the final theorem and the state of the proof, and
                                                                                                      then using ReProver to provide tactics for getting
                                         1       Introduction                                         to the next state. The proof terminates when all
                                         As the new applications of modern large language             the goals are proven. The method achieves com-
                                         models (LLMs) are emerging in various scientific             petitive performance with an order of magnitude
                                         and engineering domains, automated mathematical              smaller complexity and training time (Gloeckle
                                         theorem proving has garnered interest from both              et al., 2024). While the computational cost and
                                         machine learning researchers and mathematicians.             simplicity of ReProver are appealing, we empir-
                                         Many ongoing efforts leverage reinforcement learn-           ically observed that many failure cases of tactic
                                         ing and expert iteration, inspired by the success            generators like ReProver are due to syntactically
                                         of methods like AlphaZero, to build models that              incorrect tactics or tactics that are not applicable to
                                         search the proof space and provide step-wise or              the current state of a proof. This has detrimental
                                         holistic solutions (Lample et al., 2022; Xin et al.,         effects on the beam search performed at inference
                                         2024a; Gloeckle et al., 2024; Anthony et al., 2017;          time, as many beams result in invalid tactics that
                                             * Equal contribution.
                                                                                                      need to be verified by Lean, thus taking away time
                                             †
                                              Work done during an internship at Qualcomm AI Re-       from exploring more promising tactics.
                                         search, Amsterdam.                                              To preserve the desirable computational effi-
                                            ‡
                                              Qualcomm AI Research is an initiative of Qualcomm       ciency of the ReProver and simultaneously address
                                         Technologies, Inc.
                                         ©2025 Qualcomm Technologies, Inc. and/or its affiliated      this problem, the natural choice is to fine-tune the
                                         companies. All Rights Reserved.                              model to remove syntactic errors and increase the
number of useful tactics for the proof at each state.     not compute the step-wise reward based on the full
Recently, feedback-based alignment has been gain-         trajectory information and only rely on local look-
ing attraction in various other similar fields, such as   ahead feedback from the number of remaining and
automated code generation and various preference          unsolved goals in the next immediate steps and,
optimization methods where the rewards come ei-           therefore, we address the complexity of the trajec-
ther from human feedback (RLHF) or other reward           tory based preference association. Thanks to this
models (Ouyang et al., 2022; Ziegler et al., 2019;        fine-tuning strategy, we expect the model to rank
Rafailov et al., 2024). Since applying many such          valid and effective tactics higher than invalid ones,
reinforcement learning methods for training large         even if they were not previously observed in the
models can be complex and expensive, various ap-          human-labeled trajectories. As a result, our fine-
proaches have been introduced in the literature with      tuned model can make better use of the beam search
moderate complexity, among which we can refer             used at inference time. Besides, as we will show in
to Direct Preference Optimization (DPO) (Rafailov         our numerical results, the local look ahead, online
et al., 2024) and Group Reward Preference Opti-           training with Lean-in-loop, and GRPO are crucial
mization (GRPO) (Shao et al., 2024). In the context       components in improving the final performance of
of mathematical reasoning and theorem proving,            the model. To summarize, our contributions are
many works have emphasized the importance of              as follows. We propose a framework for efficient
trajectory-level preferences in mathematical prob-        training of a tactic generator LLM to leverage the
lem solving with large language models (LLMs)             feedback provided by the external tool, in this case,
(e.g., see (Xiong et al., 2024) and Preference Op-        the Lean solver. We use GRPO for training the
timization paragraph in Sec. 2). Even when com-           model using the reward that is based on the ap-
plexity is saved in the RL training algorithms, com-      plicable tactics and the number of unsolved goals.
puting these trajectory-level preferences can incur       The GRPO training is particularly beneficial com-
additional complexity. This discussion extends to         pared to DPO training in our case. We show that
more general episodic reasoning tasks with step-          the training based on offline dataset generation of
wise verification, where the model needs to provide       positive-negative samples is ineffective, and online
outputs that are both syntactically and semantically      training is crucial. The online verification from
correct and useful for solving the problem at hand.       the tool automatically adds new tactics to the train-
                                                          ing data. Finally, we can obtain noticeable gains
Our contribution. In this work, we aim to ad-             by computing the reward using local look-ahead
dress the above issues by fine-tuning a pre-trained       without recourse to the trajectory level preference.
prover, which listens and uses the feedback from
the tool, in this case Lean, during the training. At      2   Related Works
each step, our framework, called LeanListener, ob-        In this section, we discuss the closest works related
tains feedback on the generated tactics directly via      to our paper. We included an extended version
its interaction with the Lean software, and performs      of the related works in App. A, and in particular
policy optimization with a reward that is designed        summarize some works in Table 3.
based on Lean feedback. Given the pre-trained tac-
tic generator from (Yang et al., 2023), we sample         Theorem Proving. Large Language Models
different tactics from its output for each proof state    (LLMs) are currently used in automatic theorem
in the training set and use Lean feedback to com-         proving to generate the whole proof, or provide
pute the reward. The reward consists of a negative        assistance in sequential proofs by finding the right
return for invalid tactics, a positive one for appli-     premise or right tactics, or assisting in theorem
cable tactics, and a return based on the number of        prover specific formalization of mathematical state-
remaining unsolved goals. The RL training is done         ments, as well as combination of these ideas; see
using GRPO. First, note that the sampling step for        (Xin et al., 2024a,b; Polu and Sutskever, 2020;
the generator’s output can yield applicable and new       Jiang et al., 2022a; Wang et al., 2023; Jiang et al.,
tactics that differ from the provided human label.        2022b; Wu et al., 2022) for some pointers. A
Therefore, it helps the data efficiency of the method     key component for theorem proving is the formal
by exploring and adding new tactics like what we          proof management systems and verifiers like Lean
see in expert iteration. Second, unlike methods like      (Moura and Ullrich, 2021) and Coq (Coq Develop-
Process-supervised Reward Model (PRM), we do              ment Team, 2024).
Figure 1: We start with a dataset of human-annotated theorems and their proofs, including the gold tactics, in Lean.
During training, the ReProver retrieves the relevant premises from the premise database, and based on those and the
state of the proof, generates the next tactics. The generated tactics are verified by Lean, and its feedback is used by
RL training loop to fine-tune the ReProver. The loop continues using the steps from the human-annotated tactics
until proof termination.


   In Thor (Jiang et al., 2022a), the authors intro-         ture of Lean. In particular, it uses the Group-
duce a class of methods to use automated theorem             Relative Policy Optimization (GRPO) algorithm
provers for premise selection. LeanDojo (Yang                originally introduced for DeepSeek-Math in (Shao
et al., 2023) provided a framework that retrieves            et al., 2024), which removes the need for a separate
the premise from a database of Lean premises and             critic model, thereby simplifying the reinforcement
uses ReProver, an encoder-decoder model, to gen-             learning pipeline and reducing its computational
erate tactics for theorem proving in Lean. Lean-             cost. In comparison, we consider a step-wise ap-
Agent (Kumarappan et al., 2024) adds a dynamic               proach, leveraging the verifier feedback at each
database to LeanDojo, which enables the continual            intermediate step of the proof.
learning of the agent. Besides, a new curriculum
learning based on the difficulty of the theorems is          Preference Optimization. Other works in the
also added. GPT-f was introduced in (Polu and                literature have considered the idea of model align-
Sutskever, 2020) using Metamath as the formaliza-            ment to improve the reasoning capabilities of lan-
tion framework. Besides, they showed that iterative          guage models, too. In general, there are online
training a value function on proofs generated by             versions of Reinforcement Learning with Human
the LLM prover can continually improve the per-              Feedback (RLHF) as in (Bai et al., 2022; Ouyang
formance. Another example is LLEMMA, which                   et al., 2022), and offline versions with either an
is based on pre-trained Llama Code (Azerbayev                explicit reward model (e.g. (Christiano et al., 2017;
et al., 2024). DeepSeek-Prover (Xin et al., 2024a)           Ziegler et al., 2019)) or an implicit reward model
generated Lean4 proof data by translating natural            (e.g. DPO (Rafailov et al., 2024)) to encode the
language problems into their formal versions in              preference. The later method directly optimizes
Lean4, and the model produces whole proofs in                the model without training any independent re-
single turns. DeepSeekV1.5 (Xin et al., 2024b)               ward model. Many follow-up works explored
provides a middle ground by generating the whole             DPO variations and its shortcomings, such as re-
proof, verifying it via Lean, and then truncating the        ward over-optimization, for example, by introduc-
proof until the first error. The authors propose ad-         ing Kahneman-Tversky Optimization (KTO) (Etha-
ditional techniques relying on proper appending of           yarajh et al., 2024).
previous states and including truncate-and-resume               In the context of reasoning and, in particular,
in the Monte-Carlo Tree Search (MCTS) proce-                 mathematical problem solving, many recent works
dure. Additionally, DeepSeekV1.5 leverages ver-              have explored different forms of direct preference
ification feedback from Lean on whole-proofs to              optimization, for example (Xiong et al., 2024; Yuan
improve model’s alignment with the formal struc-             et al., 2024; Jiao et al., 2024; Cobbe et al., 2021;
Lightman et al., 2023; Wang et al., 2024; Pang et al.,            number of goals yet to be proven. Our model can
2024; Chen et al., 2024; Lu et al., 2024b). The au-               utilize the feedback received from Lean during the
thors in (Xiong et al., 2024) introduce a multi-turn              training and for the next tactic generation. Note
version of DPO to use feedbacks from the veri-                    that Lean is a formal language; hence, it has a strict
fiers, in their case the code interpreters, particularly          syntax, and only certain tactics can be applied on
for multi-turn scenarios, which requires trajectory-              each state. At each step, the agent relies only on
level preference optimization. The trajectory-level               the Lean feedback about the current state to gen-
preference can be obtained by dataset labels of                   erate the next tactic until the theorem T is proved
the gold answers or Outcome-supervised Reward                     or the model runs out of predefined time. Figure
Models (ORMs) (Cobbe et al., 2021; Lightman                       4 presents a Lean proof example. Finally, the se-
et al., 2023). A more fine-grained step-wise super-               quence of state-tactic pairs {⟨st , at ⟩}t composes
vision can be used as in PRMs (Lightman et al.,                   the proof of the original theorem T .
2023) or by leveraging trajectory level preferences                  In general, a certain state st can include multiple
(Wang et al., 2024). The idea of ORM and PRM                      (sub-) goals, representing a number of independent
has also been originally discussed in (Uesato et al.,             statements to be simultaneously proved in order to
2022). These works focus on mathematical rea-                     prove the original statement. An intuitive exam-
soning, rather then formal theorem proving, which                 ple is given by application of an induction tactic,
is the focus of our work. In our work, the theo-                  which turns a single statement into two indepen-
rem prover automatically provides the preference,                 dent ones (the base case and the inductive step).
which is used either during training or for an offline            Hence, the application of a tactic at on a certain
generated dataset. Furthermore, our work follows                  state st can prove certain goals but also turn some
PRM philosophy as we consider feedback from                       into more sub-goals. As a result, the number of
Lean at each step of proof generation.                            sub-goals G(st+1 ) can increase, decrease or remain
                                                                  unchanged after the application of each tactic.
3       Methodology                                                  Tactic prediction is one of the primary tasks in
                                                                  training LLM provers (Yang et al., 2023; Welleck
In this section, we begin with an overview of Inter-
                                                                  and Saha, 2023; Lample et al., 2022). In a su-
active Theorem Proving (ITP), outlining the task
                                                                  pervised learning framework, during training, the
formulation and key terminology. We then intro-
                                                                  model is fed the current state (st ) and asked to
duce our framework, LeanListener, and describe
                                                                  predict a tactic (at ). Recent studies have shown
its main components.
                                                                  that providing related premises, in addition to the
3.1      Background                                               current state, can also enhance the model’s perfor-
                                                                  mance (Mikuła et al., 2023; Yang et al., 2023). In
In ITP, an LLM-based prover interacts with an ex-                 the inference phase, however, for each theorem, the
ternal proof assistant and receives feedback on the               model employs an inference time-compute tech-
steps to be taken to prove the given theorem. In                  nique. It observes the current state (st ) and gen-
this work, we use the proof assistant software Lean1              erates a set of tactics ({ a0 , ..., ak }) using beam
(de Moura et al., 2015; Moura and Ullrich, 2021)                  search with a size of k. Building a proof search
as the formal environment which LLMs employ to                    tree, the tactic generator interacts with the Lean as-
verify each proof step in a proof sequence. In par-               sistant, starting with the tactic with the highest ac-
ticular, we used the open-source LeanDojo frame-                  cumulative log probability (best first search). The
work (Yang et al., 2023), which provides toolkits                 returned state can be an error state if the tactic
to interact with Lean, as well as readily extracted               execution is unsuccessful, e.g., due to timeout or
data and pre-trained models.                                      inapplicable tactic. In this case, the model explores
   An agent can interact with Lean to prove a theo-               the next tactic in the queue. This process will con-
rem T by iteratively observing the current "proof                 tinue until we reach a valid next state (st+1 ) or
state" st and performing an action at , called a "tac-            prove the given theorem. It is worth mentioning
tic" (i.e., proof steps), which leads to the next state           that the generated proof by the model can be differ-
st+1 . Lean inspects each tactic, accepts or rejects              ent from the human-written one in the test dataset.
it, and provides additional information, like the                 As many inference-time compute approaches, the
    1
     We use Lean 4, and for brevity, simply refer to it as Lean   model (generator) utilizes feedback from an exter-
in the rest of the manuscript.                                    nal expert (verifier) and can explore creative proofs
at the cost of extra computation at inference.          els like RLHF. The key ingredient in DPO is creat-
    While the pre-training objective is a supervised    ing a static preference dataset in the form of pair-
sequence-to-sequence task, in the evaluation phase,     wise comparisons D = {(xi , yi+ , yi− )}i such that
the model acts like an RL agent, which receives         for each prompt xi , the generated output yi+ is pre-
feedback on its actions (generated tactics) and uses    ferred over yi− . DPO directly optimizes the policy
it to choose the next action via the search strategy    πθ (possibly, initialized to a reference policy πref )
explained above.                                        via the following loss based on the static dataset:
    In this work, we resolve this discrepancy and
bring the proof-tree expansion-based exploration
to the training regime, leveraging the feedback pro-       LDP O (πθ , πref ) = −E(x,y+ ,y− )∼D                  (1)
                                                                            πθ (y + |x)          πθ (y − |x)
                                                                                                            
vided to each tactic to construct step-wise rewards.        log σ β log                 − β log
Inspired by human preference in LLMs alignment,                           πref (y + |x)         πref (y − |x)
we present a novel framework, LeanListener, in
which we align the pre-trained tactic generator with       where σ is the logistic function. The DPO pref-
guidance from Lean in a step-wise scenario. In          erence dataset can be built based on applicable/not
contrast with similar works with RL training like       applicable tactics as the positive and negative sam-
(Xin et al., 2024b), we only need a single step look    ples in a pair. In essence, the model can be trained
ahead and do not utilize the full trajectory to com-    to prefer the applicable tactics, i.e., tactics that lead
pute the rewards. In what follows, we explain our       to a valid proof state, over inapplicable tactics, i.e.,
LeanListener framework in detail.                       tactics that lead to an error state. The unsophisti-
                                                        cated DPO pairing configuration will intrinsically
3.2   LeanListener                                      reward all the applicable tactics equally, irrespec-
Our LeanListener framework is based on employ-          tive of whether it takes the proof toward a conclu-
ing external proof assistant feedback as a guid-        sive state or not. However, a more intricate scoring
ance signal. To bridge the discrepancy between          of tactics can be performed by looking deeper into
the seq2seq-based training and beam search-based        the Lean feedback, such as the number G(st+1 ) of
proof full tree expansion during inference, we bring    theorem sub-goals that remains to be proven at step
the per-step proof-tree expansion based exploration     st+1 . To craft a more differential scoring of ap-
to the training regime. Aside from transitioning        plicable tactics, as reward rt for a tactic at , we
to the next proof state, applying a tactic in Lean      choose R(at ; st ) = softplus (G(st ) − G(st+1 )),
results in valuable information, which can be used      where softplus(x, β) = β1 ln(1 + eβx ). We invari-
to score the efficacy of the tactic at the concerned    ably score the invalid tactics with a score of 0. Such
proof step, and consequently guide the model to-        a scoring strategy rewards, and hence, trains the
ward proving theorems. For example, a syntacti-         model to prioritize generating tactics that help re-
cally valid tactic can be gauged for the number of      solve more sub-goals. We choose softplus over a
sub-goals in the theorem it helps resolve.              naive linear delta to prevent negative reward values,
   Lean feedback includes helpful information that      since the number of intermediate sub-goals may
can be employed to guide the model toward proving       temporarily increase before the proof is completed.
theorems, such as if the generated tactic is applica-      To take the most out of the Lean feedback and
ble to the current state and how many (sub-)goals       incorporate the number of proven (sub-) goals by
are solved by applying the tactic. Then, LeanLis-       the tactics as well, we need a more sophisticated
tener utilizes this to reward the model not only for    objective. In this regard, we propose to use Group
generating an applicable and syntactically correct      Relative Policy Optimization (GRPO) (Shao et al.,
tactic but also for encouraging the model to gener-     2024), a variant of reinforcement learning (RL)
ate tactics that solve more (sub)goals. This results    Proximal Policy Optimization (PPO) algorithm
in a more efficient proof-generation process.           (Schulman et al., 2017), in which each tactic is re-
   A straightforward approach to do so is em-           warded based on the sub-goals criterion discussed
ploying Direct Preference Optimization (DPO)            above. For each prompt q (current state st ), GRPO
(Rafailov et al., 2024), a popular lightweight but      samples a group of outputs {o1 , o2 , · · · , oG } (gen-
effective algorithm used to align LLMs with human       erated tactics) from the old policy πθold and maxi-
preferences, which is often replacing reinforcement     mizes the policy model with the following objec-
learning based solutions with separate reward mod-      tive:
                                                                               model (offline) or the target model (online).
                                                    G        |oi | 
                                                                               More specifically, for each proof state st in
                                                 1 X 1 X                       human-annotated theorem proof in training split,
 JGRPO (θ) = Eq∼P (Q),{oi }G
                               i=1 ∼πθ old (O|q) G     |oi | t=1
                                                   i=1                         we sample w = 8 tactics {ajt ∼ πref (a|st )}w    j via
                                                                   (2)
                                                                              beam search and sort them by their likelihood
                       πθ (oi,t |q, oi,<t )                                    score given by the sampling model. Additionally,
               min                             Âi,t ,
                      πθ old (oi,t |q, oi,<t )
                                                                            we look for the presence of the ground truth tactic,
                      πθ (oi,t |q, oi,<t )
               clip    old
                                             , 1 − ϵ, 1 + ϵ Âi,t              i.e., gold tactic, in the beam search proposals: if
                      πθ (oi,t |q, oi,<t )
                                                                              the golden tactic abt for the current state st happens
               − βDKL [πθ ||πref ]                                             to be absent from the top w proposals, we append
                                                                               it as a w + 1 = 9-th tactic at the end of the list
   Where πθ and πθold are current and old policy                               (i.e. with lowest likelihood); this means states
models, and q, o are questions and outputs sam-                                can have either 8 or 9 tactic proposals for training.
pled from the dataset and the old policy πθold ,                               The next step involves accruing feedback from the
respectively. ϵ and β are hyper-parameters, and                                Lean framework by individual application of each
Âi,t is the advantage calculated based on the re-                             proposed tactic on the current proof state.
ward for each sampled tactic. More specifically,
                                                                               Dataset for DPO To construct the dataset of pair-
assume the reward value for all generated tactics
                                                                               wise comparisons D required by DPO, for each
in a beam search with a size of w is represented
                                                                               state st , we need to label its tactics as the positive
by r = {r1 , r2 , · · · , rw }. Then, the advantage Âi,t
                                                                               and negative samples using Lean feedback. A tactic
is the normalized reward Âi,t = r˜i = ri −mean(r)
                                                std(r)   .                     is positive if it is syntactically correct and applica-
Following (Shao et al., 2024), we estimate the KL                              ble to the current state st by Lean, and it is nega-
divergence with the following equation:                                        tive if it gets rejected by Lean. We consider three
                                                                               strategies in the pair creation. random: We pair
  DKL (πθ || πref ) =                                                    (3)   each negative tactic with a positive tactic randomly.
                                                                               zero accuracy: Each negative tactic is paired with
                                                                   
        πref (oi,t |q, oi,<t )             πref (oi,t |q, oi,<t )
                               − log                                    −1
        πθ (oi,t |q, oi,<t )               πθ (oi,t |q, oi,<t )                the highest-likelihood positive one among those
                                                                               mistakenly ranked lower. hard: Similar to zero
  We use the pre-trained generator in the ReProver                             accuracy, but we pick the lowest-likelihood posi-
model from (Yang et al., 2023) both as a base refer-                           tive tactic. In practice, we also include some minor
ence model for πref and to initialize the policy to                            heuristics to avoid resampling the same positive
optimize πθ .                                                                  tactics too often, see Algorithm 1. Finally, for data
3.2.1    Dataset Curation                                                      augmentation purposes, rather than using the origi-
                                                                               nal prompt comprising the state and the retrieved
For both DPO and GRPO finetuning, we build our
                                                                               premises x = (st , pt ), we dynamically generate a
training dataset using the training split of Lean-
                                                                               new prompt like in (Yang et al., 2023) by applying
Dojo Benchmark (Yang et al., 2023) to avoid data
                                                                               random dropout on the retrieved premises. Then,
contamination as the ReProver model has already
                                                                               once a positive tactic y + is chosen, and the aug-
been pre-trained on it. Inspired by the online-RL
                                                                               mented prompt x is generated, we add the tuple
training paradigms for eliciting reasoning in LLMs
                                                                               (x, y + , y − ) to the dataset D. Each proof state st
(Gloeckle et al., 2024), we, too, build our training
                                                                               appears in the dataset for each negative tactic the
paradigm in an online setting. During online train-
                                                                               reference model generated for it. In the end, the
ing, we update the model used in the beam search
                                                                               offline preference dataset consists of 251k triplets
to generate tactic proposals for every 50 training
                                                                               (x, y + , y − ). For online DPO, we keep the same
iteration with the target model. We also experi-
                                                                               procedure, except for the reference model used for
ment with the offline setting, where we use the
                                                                               generating the beam-search tactic proposals per
pre-trained ReProver model to generate the train-
                                                                               proof step, which gets updated every 50 iterations
ing data offline. We discuss the relative advantages
                                                                               with the target model. We describe precisely this
of online over offline training in Table 1 and Sec. 4.
                                                                               dataset generation procedure in Algorithm 1.
   To generate the fine-tuning data, we parse
the human-annotated proofs in the LeanDojo                                     Dataset for GRPO For the GRPO scenario, the
benchmark using either the reference ReProver                                  dataset is being built dynamically throughout the
                                                                    Len. Valid   Len. All
     Strategy          dropout    Prec.@8 ↑    MAP      MRR                                 % 0-precision steps ↓
                                                                     Tactics     Tactics
     Offline DPO
                       p = 0.3      37.75      60.75    64.43         26.66      111.20              29.10
      (zero acc.)
     Offline DPO
                       p = 0.3      35.71      59.90    63.42         28.59      116.00              29.80
        (hard)
     Offline DPO
                          /         34.86      57.92    61.08         29.37      115.39              32.14
        (hard)
     Online DPO
                       p = 0.3      44.75      64.99    71.22         19.72       27.44              11.88
        (hard)
     Online GRPO      p = 0.25       51.01     70.09    77.05         16.26       19.87               7.44
       ReProver
                          /         40.77      59.85    65.70         18.08       22.34              12.74
     (base model)

Table 1: The DPO objective optimizes the model to prefer valid tactics. In this table, we report different metrics to
measure the step-wise performance. Prec.@8 = the percentage of the number of valid tactics among the top 8 tactics
sampled at each proof state. MAP= percentage of mean average precision. MRR = percentage of mean reciprocal
rank. Len. Valid Tactics = average length (in terms of tokens) of the generated tactics which are valid. Len. All
Tactics = average length of all generated tactics. %0-precision steps = fraction of states with no valid tactics.


training. More specifically, for each state in the          benchmarks. The test set has two variants, random,
training set, the model generates a set of tactics          where the whole dataset is randomly split into
using beam search. Then, using the reward func-             training, validation, and test set, and the more
tion described in Sec. 3.2, each generated tactic           challenging one, novel premises, where the test
is scored. The more (sub)goals a tactic solves, the         set includes premises that do not appear in the
greater its reward. Since the policy model is get-          training data2 . In the following experiments, we
ting updated through GRPO objective, the model’s            first verify whether incorporating Lean feedback
generated tactics change over time. Similar, to the         enhances the quality of generated tactics. Then, we
online case in DPO, we update the model used for            examine the performance on theorem proving task.
sampling tactics every 50 training iterations with          Finally, we study the improved theorem proving
the on-policy target model.                                 speed of our method.

3.2.2   Training Setting                                    Tactic validity. To begin with, we investigate to
                                                            what extent adding DPO and GRPO in the training
We use the pre-trained generator model in ReProver
                                                            pipeline increases the number of valid tactics gener-
from (Yang et al., 2023) both as a base reference
                                                            ated by the model. As mentioned before, a tactic is
model for πref and to initialize the policy to op-
                                                            valid if it is applicable to a state by Lean, even if it
timize πθ . The generator is an encoder-decoder
                                                            does not lead to a proof. The validity is also about
Transformer based on the ByT5 model (Xue et al.,
                                                            the syntactic correctness of the tactic. We expect
2022), accompanied by a premises retrieval system
                                                            that if the model generates more valid tactics in the
that provides the most relevant premises as input.
                                                            best first search, the chance of proving the given
We fine-tune the pre-trained ReProver model us-
                                                            theorem, as well as the efficiency of the proof, will
ing the described datasets for 10k steps with the
                                                            increase.
AdamW optimizer (learning rate 2.25e − 6, batch
                                                               Table 1 presents the numerical results on the
size 16). The overall fine-tuning process in the
                                                            validity of the generated tactics under different sce-
LeanListener framework requires approximately
                                                            narios using DPO and GRPO objectives. In this
40 A100 GPU-days, with over 80% of the time
                                                            table, we compare the state-wise metrics which
spent on interactions with Lean, which are CPU-
                                                            we expect to correlate with our training objective.
bound. All experiments were conducted using Hug-
                                                            First of all, using the DPO objective, we observe
gingFace TRL trainers.
                                                                2
                                                                 (Yang et al., 2023) only released the model trained on
4   Experiments                                             the random split, which we use as the base for our method.
                                                            We report the performance of the methods also on the novel
                                                            premises test despite the possible overlap with the training
We evaluate the effectiveness of LeanListener               set since this testset is still more challenging than the random
in different aspects on the test set of LeanDojo            one. See github issue.
                                                                       Policy                  Pairing                                        novel
                                 Model                                                                                 Online   random
                                                                     Opt. Method               Strategy                                     premises
                                 tidy                                                                                             23.8          5.3
                                 GPT-4                                                                                            29.0          7.4
                                 ReProver (w/o retrieval)                                                                         47.6         23.2
                                 ReProver                                                                                         51.2         26.3
                                 ReProver*                                                                                       52.76        40.86
                                                                                                rand.                    ×       35.99
                                                                                              zero acc.                  ×       33.18
                                                                                                hard                     ×       31.27
                                                                DPO (binary)
                                 LeanListener (Ours)                                            rand.                    ∨       50.25
                                                                                              zero acc.                  ∨       50.90
                                                                                                hard                     ∨       50.85
                                                                GRPO (#sub-goals)                 -                      ∨       53.21       41.11

Table 2: Pass@1 (%) performance on the LeanDojo benchmark on the random and novel premises splits. The
performance of the first four baselines is the one reported in (Yang et al., 2023), while ReProver* is the newly
provided pre-trained model, which we evaluated ourselves.


                           600         LeanListener                                                      600           LeanListener
                           500
                                       ReProver                                                          500
                                                                                                                       ReProver
      Inference Time (s)




                                                                                    Inference Time (s)
                           400                                                                           400
                           300                                                                           300
                           200                                                                           200
                           100                                                                           100
                             0                                                                               0
                                 600     700      800          900     1000                                      400      500         600     700      800
                                       Number of proved theorems                                                       Number of proved theorems
                                            (a) random split                                                            (b) novel premises split


Figure 2: To understand the improvement in inference speed, in these figures, we visualize the number of theorems
in the two test sets which are proven by each model within different inference time limits. While the overall number
of theorems proved within 10 minutes by the two models is comparable, we see LeanListener is consistently faster,
which means, it takes significantly less time to solve the same number of theorems (see the purple lines for example).


that all offline strategies fail to improve the number                                  benchmark when using the random split. 3 . We
of valid tactics generated by the model, while the                                      first observe that while DPO training on binary
online strategy significantly improves the number                                       feedback improves the number of valid tactics, it
of valid tactics, and reduces the number of states                                      always leads to a small degradation in the num-
with no valid tactics. Among all, online GRPO                                           ber of proven theorems. We believe that there is a
provides the best results. It is interesting to observe                                 spurious correlation between the low-ranked valid
that the length of valid tactics decreases in the best                                  tactics and their length in the paired samples in
models, thereby reducing unnecessarily complex                                          DPO training, which leads to a bias toward gen-
tactic generation.                                                                      erating longer and not necessarily useful tactics.
                                                                                        GRPO effectively addresses this issue by online
                                                                                        training and avoiding paired samples for training,
Performance evaluation. Moving forward, we                                              as well as employing more informative feedback
investigate whether improved tactic generation re-                                      about the number of solved sub-goals. Indeed, we
sults in stronger reasoning capabilities or not. Ta-                                    find that this finer reward, which incorporates the
ble 2 presents the final theorem proving the per-                                       number of solved sub-goals, is more effective and
formance of our models with the pre-trained Re-                                         leads to an increased number of proven theorems.
Prover baseline along with GPT-4 (Achiam et al.,
2023) and tidy (which is a non-machine learning                                                          3
                                                                                            The evaluation results on the MiniF2F (Zheng et al., 2022)
and heuristic-based approach), on the LeanDojo                                          and ProofNet (Azerbayev et al., 2023) datasets are reported in
                                                                                          103
    Proof Length: ReProver   Fail   2     13     13      5     908




                                                                        # test theorems
                               4           3      2     15      3
                                                                                          102
                               3    2      8     84      1     12

                               2    18   253      9             8
                                                                                          101
                               1 624       8                    1
                                                                                                LeanListener -2   -1    0    1     2 ReProver
                                                                                                   Failure                            Failure
                                    1      2      3      4     Fail                                           Relative Proof Length
                             Proof Length: LeanListener (Our)                                             ReProver - LeanListener (Our)
                                (a) Per-theorem proof-length analysis                      (b) Per-theorem relative proof-length comparison

Figure 3: For each valid theorem in the LeanDojo test set, we plot and compare the proof-length performance for
both the LeanListener and ReProver models. 3(a) depicts the proof lengths for the proofs generated by the ReProver
model on the y-axis, and by the LeanListener model on the x-axis. The plot shows a higher density above the
diagonal, indicating that the proofs generated by LeanListener generally have fewer proof steps than those generated
by ReProver for the same theorem. 3(b) illustrates the relative proof-length advantage of the LeanListener method
over ReProver. For each theorem, we plot the difference in proof lengths generated by both models, observing that
instances where LeanListener has a positive advantage outnumber those where it does not.


Inference time. In the previous experiments, we                         theorem, which is intuitive. Since LeanListener
show that LeanListener generates a more efficient                       is trained with a one-step look-ahead process, it
search tree by having more valid tactics. Now, we                       excels at proving theorems that can be solved in a
want to evaluate if this approach leads to a more                       single step. We observe that the number of failed
efficient inference time. Figure 2 compares the in-                     proofs increases for theorems requiring more than
ference time in LeanListener and ReProver as the                        one proof step. This suggests potential for further
baseline model on the LeanDojo benchmark. As                            improvements in LeanListener’s performance with
can be observed, LeanListener proves more theo-                         training that incorporates more than one step look-
rems in up to 20% less time for both random and                         ahead.
novel premises splits.
                                                                        5                 Conclusions
Proof length In addition to the aggregate Pass@1
                                                                        In this paper, we propose a novel RL-based
performance metric discussed earlier, we present
                                                                        framework, LeanListener, based on the provided
an analysis of the proof lengths generated by the
                                                                        feedback by an external automatic verifier to im-
LeanListener and ReProver models on the Lean-
                                                                        prove trained LLMs in automatic theorem proving.
Dojo benchmark4 . Generally, concise proofs, i.e.,
                                                                        LeanListener considers the general applicability of
those with fewer proof steps, are considered more
                                                                        tactics as well as their local effectiveness, i.e., their
efficient and desirable than lengthier ones. Our aim
                                                                        impact on the number of unproven (sub)goals in a
here is to provide insights into the quality of proofs
                                                                        proof sequence, to fine-tune theorem provers. Such
generated by both models. As shown in Figure 3,
                                                                        step-wise reinforcement with the corresponding
our LeanListener consistently produces more con-
                                                                        reward can efficiently harness the benefits of
cise proofs compared to the base ReProver model.
                                                                        the trajectory level guidance without outcome
   An interesting observation in Figure 3(a) is the                     dependent reward computation. Our experimental
last row, which corresponds to proofs that were                         results show that LeanListener not only surpasses
proved in just one step by the ReProver model. In                       the considered baselines in proving more theorems
this category, LeanListener fails to prove only one                     on the LeanDojo benchmark but also does so faster
                                                                        in less inference time.
Appendix C.
   4
     See Appendix C for the analysis on MiniF2F and
ProofNet.
6   Limitations                                           Lasse Blaauwbroek, Miroslav Olšák, Jason Rute, F I S
                                                            Massolo, Jelle Piepenbrock, and Vasily Pestun. 2024.
In this work, we have focused on a well-known               Graph2Tac: Online representation learning of formal
open-source ITP model to show the effectiveness of          math concepts. ICML, 235:4046–4076.
the LeanListener framework. Applying our frame-
                                                          Guoxin Chen, Minpeng Liao, Chengxi Li, and Kai
work to more tactic generator models with different         Fan. 2024. Step-level value preference optimiza-
architecture, model sizes, and components in the            tion for mathematical reasoning. arXiv preprint
training pipelines is an interesting future direction.      arXiv:2406.10858.
We also mainly study the performance of LeanLis-
                                                          Wenhu Chen, Xueguang Ma, Xinyi Wang, and
tener on the LeanDojo benchmark. Investigating             William W Cohen. 2022. Program of thoughts
the performance of LeanListener on other theo-             prompting: Disentangling computation from reason-
rem proving datasets is another potential follow-up        ing for numerical reasoning tasks. Trans. Mach.
work.                                                      Learn. Res., 2023.

                                                          Paul F Christiano, Jan Leike, Tom Brown, Miljan Mar-
                                                            tic, Shane Legg, and Dario Amodei. 2017. Deep
References                                                  reinforcement learning from human preferences. Adv.
Josh Achiam, Steven Adler, Sandhini Agarwal, Lama           Neural Inf. Process. Syst., 30.
  Ahmad, Ilge Akkaya, Florencia Leoni Aleman,
  Diogo Almeida, Janko Altenschmidt, Sam Altman,          Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
  Shyamal Anadkat, et al. 2023. Gpt-4 technical report.     Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
  Technical report, OpenAI.                                 Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
                                                            Nakano, Christopher Hesse, and John Schulman.
Alberto Alfarano, Francois Charton, and Amaury Hayat.       2021. Training verifiers to solve math word prob-
  2024. Global lyapunov functions: a long-standing          lems. arXiv [cs.LG].
  open problem in mathematics, with symbolic trans-
  formers. In The Thirty-eighth Annual Conference on      Coq Development Team. 2024. The Coq proof assistant.
  Neural Information Processing Systems.
                                                          Leonardo Mendonça de Moura, Soonho Kong, Jeremy
Thomas Anthony, Zheng Tian, and David Barber. 2017.         Avigad, Floris van Doorn, and Jakob von Raumer.
  Thinking fast and slow with deep learning and tree        2015. The lean theorem prover (system description).
  search. Advances in neural information processing         In CADE.
  systems, 30.
                                                          Kawin Ethayarajh, Winnie Xu, Niklas Muennighoff,
Zhangir Azerbayev, Bartosz Piotrowski, Hailey               Dan Jurafsky, and Douwe Kiela. 2024. KTO: Model
  Schoelkopf, Edward W. Ayers, Dragomir Radev, and          alignment as prospect theoretic optimization. arXiv
  Jeremy Avigad. 2023. Proofnet: Autoformalizing            [cs.LG].
  and formally proving undergraduate-level mathemat-
  ics. Preprint, arXiv:2302.12433.                        Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon,
                                                            Pengfei Liu, Yiming Yang, Jamie Callan, and Gra-
Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster,        ham Neubig. 2023. PAL: Program-aided language
  Marco Dos Santos, Stephen Marcus McAleer, Al-             models. In International Conference on Machine
  bert Q. Jiang, Jia Deng, Stella Biderman, and Sean        Learning, pages 10764–10799. PMLR.
  Welleck. 2024. Llemma: An open language model
  for mathematics. In The Twelfth International Con-      Fabian Gloeckle, Jannis Limperg, Gabriel Synnaeve,
  ference on Learning Representations.                      and Amaury Hayat. 2024. ABEL: Sample efficient
                                                            online reinforcement learning for neural theorem
Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda               proving. In The 4th Workshop on Mathematical Rea-
  Askell, Anna Chen, Nova DasSarma, Dawn Drain,             soning and AI at NeurIPS’24.
  Stanislav Fort, Deep Ganguli, Tom Henighan,
  Nicholas Joseph, Saurav Kadavath, Jackson Kernion,      Alexey Gorbatovski, Boris Shaposhnikov, Alexey
  Tom Conerly, Sheer El-Showk, Nelson Elhage, Zac           Malakhov, Nikita Surnachev, Yaroslav Aksenov, Ian
  Hatfield-Dodds, Danny Hernandez, Tristan Hume,            Maksimov, Nikita Balagansky, and Daniil Gavrilov.
  Scott Johnston, Shauna Kravec, Liane Lovitt, Neel         2024. Learn your reference model for real good
  Nanda, Catherine Olsson, Dario Amodei, Tom                alignment. arXiv [cs.LG].
  Brown, Jack Clark, Sam McCandlish, Chris Olah,
  Ben Mann, and Jared Kaplan. 2022. Training a help-      Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen,
  ful and harmless assistant with reinforcement learn-      Yujiu Yang, Minlie Huang, Nan Duan, and Weizhu
  ing from human feedback. arXiv [cs.CL].                   Chen. 2023. ToRA: A tool-integrated reasoning
                                                            agent for mathematical problem solving. In The
Lasse Blaauwbroek. 2024. The tactician’s web of large-      Twelfth International Conference on Learning Repre-
  scale formal knowledge. arXiv [cs.LO].                    sentations.
Xinyu Guan, Li Lyna Zhang, Yifei Liu, Ning Shang,          Giovanni Luca Marchetti, Gabriele Cesa, Kumar Pratik,
  Youran Sun, Yi Zhu, Fan Yang, and Mao Yang. 2025.          and Arash Behboodi. 2023. Neural lattice reduction:
  RStar-math: Small LLMs can master math reasoning           A self-supervised geometric deep learning approach.
  with self-evolved deep thinking. arXiv [cs.CL].            arXiv [cs.LG].
Geoffrey Irving, Christian Szegedy, Alexander A Alemi,     Maciej Mikuła, Szymon Antoniak, Szymon
  Niklas Een, Francois Chollet, and Josef Urban. 2016.      Tworkowski, Bartosz Piotrowski, Albert Jiang,
  DeepMath - deep sequence models for premise se-           Jin Peng Zhou, Christian Szegedy, Łukasz Kuciński,
  lection. Advances in Neural Information Processing        Piotr Miłoś, and Yuhuai Wu. 2023. Magnushammer:
  Systems, 29.                                              A transformer-based approach to premise selection.
Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski,          In The 3rd Workshop on Mathematical Reasoning
  K Czechowski, Tomasz Odrzyg’o’zd’z, Piotr Milo’s,         and AI at NeurIPS’23.
  Yuhuai Wu, and M Jamnik. 2022a. Thor: Wield-
  ing hammers to integrate language models and au-         Leonardo de Moura and Sebastian Ullrich. 2021. The
  tomated theorem provers. Neural Inf Process Syst,          lean 4 theorem prover and programming language.
  abs/2205.10893:8360–8373.                                  In Automated Deduction – CADE 28, Lecture notes
                                                             in computer science, pages 625–635. Springer Inter-
Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou,           national Publishing, Cham.
  Timothee Lacroix, Jiacheng Liu, Wenda Li, Mateja
  Jamnik, Guillaume Lample, and Yuhuai Wu. 2022b.          Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Car-
  Draft, sketch, and prove: Guiding formal theorem           roll L Wainwright, Pamela Mishkin, Chong Zhang,
  provers with informal proofs. In The Eleventh Inter-       Sandhini Agarwal, Katarina Slama, Alex Ray, John
  national Conference on Learning Representations.           Schulman, Jacob Hilton, Fraser Kelton, Luke E
                                                             Miller, Maddie Simens, Amanda Askell, P Welin-
Fangkai Jiao, Chengwei Qin, Zhengyuan Liu, Nancy F           der, P Christiano, J Leike, and Ryan J Lowe. 2022.
  Chen, and Shafiq Joty. 2024. Learning planning-            Training language models to follow instructions
  based reasoning by trajectories collection and             with human feedback. Neural Inf Process Syst,
  process reward synthesizing.     arXiv preprint            abs/2203.02155:27730–27744.
  arXiv:2402.00658.
                                                           Richard Yuanzhe Pang, Weizhe Yuan, He He,
Adarsh Kumarappan, Mo Tiwari, Peiyang Song,
                                                             Kyunghyun Cho, Sainbayar Sukhbaatar, and Jason E
  Robert Joseph George, Chaowei Xiao, and Anima
                                                             Weston. 2024. Iterative reasoning preference opti-
  Anandkumar. 2024. LeanAgent: Lifelong learn-
                                                             mization. In The Thirty-eighth Annual Conference
  ing for formal theorem proving. arXiv preprint
                                                             on Neural Information Processing Systems.
  arXiv:2410.06209.
Xin Lai, Zhuotao Tian, Yukang Chen, Senqiao Yang,          Lawrence C Paulson. 1994. Isabelle: A Generic Theo-
  Xiangru Peng, and Jiaya Jia. 2024. Step-DPO: Step-         rem Prover, 1994 edition. Lecture Notes in Computer
  wise preference optimization for long-chain reason-        Science. Springer, Berlin, Germany.
  ing of llms. arXiv preprint arXiv:2406.18629.
                                                           Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Man-
Guillaume Lample, Timothee Lacroix, Marie-Anne                tas Baksys, Igor Babuschkin, and Ilya Sutskever.
  Lachaux, Aurelien Rodriguez, Amaury Hayat,                  2023. Formal mathematics statement curriculum
  Thibaut Lavril, Gabriel Ebner, and Xavier Martinet.         learning. In The Eleventh International Conference
  2022. Hypertree proof search for neural theorem             on Learning Representations.
  proving. Advances in neural information processing
  systems, 35:26337–26349.                                 Stanislas Polu and Ilya Sutskever. 2020. Generative
                                                              language modeling for automated theorem proving.
Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harri-          arXiv [cs.LG].
  son Edwards, Bowen Baker, Teddy Lee, Jan Leike,
  John Schulman, Ilya Sutskever, and Karl Cobbe.           Rafael Rafailov, Archit Sharma, Eric Mitchell, Christo-
  2023. Let’s verify step by step. In The Twelfth Inter-     pher D Manning, Stefano Ermon, and Chelsea Finn.
  national Conference on Learning Representations.           2024. Direct preference optimization: Your language
Zimu Lu, Aojun Zhou, Ke Wang, Houxing Ren,                   model is secretly a reward model. Advances in Neu-
  Weikang Shi, Junting Pan, Mingjie Zhan, and Hong-          ral Information Processing Systems, 36.
  sheng Li. 2024a. MathCoder2: Better math reason-
  ing from continued pretraining on model-translated       Esteban Real, Yao Chen, Mirko Rossini, Connal
  mathematical code. arXiv preprint arXiv:2410.              de Souza, Manav Garg, Akhil Verghese, Moritz
  08196.                                                     Firsching, Quoc V Le, Ekin Dogus Cubuk, and
                                                             David H Park. 2023. AutoNumerics-zero: Au-
Zimu Lu, Aojun Zhou, Ke Wang, Houxing Ren,                   tomated discovery of state-of-the-art mathematical
  Weikang Shi, Junting Pan, Mingjie Zhan, and Hong-          functions. arXiv [cs.NE].
  sheng Li. 2024b. Step-controlled dpo: Leveraging
  stepwise error for enhanced mathematical reasoning.      Peter Scholze. 2022. Liquid tensor experiment. Exp.
  arXiv preprint arXiv:2407.00782.                           Math., 31(2):349–354.
John Schulman, Filip Wolski, Prafulla Dhariwal, Alec       Sean Welleck and Rahul Saha. 2023. Llmstep: Llm
  Radford, and Oleg Klimov. 2017. Proximal policy            proofstep suggestions in lean. arXiv preprint
  optimization algorithms. ArXiv, abs/1707.06347.            arXiv:2310.18457.

Zhihong Shao, Fei Huang, and Minlie Huang. 2022.           Emily Wenger, Mingjie Chen, Francois Charton, and
  Chaining simultaneous thoughts for numerical rea-          Kristin Lauter. 2022. SALSA: Attacking lattice cryp-
  soning. In Findings of the Association for Computa-        tography with transformers. In Advances in Neural
  tional Linguistics: EMNLP 2022, pages 2533–2547,           Information Processing Systems.
  Stroudsburg, PA, USA. Association for Computa-
                                                           Ti-Rong Wu, Chung-Chin Shih, Ting Han Wei, Meng-
  tional Linguistics.
                                                              Yu Tsai, Wei-Yuan Hsu, and I-Chen Wu. 2021.
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,               AlphaZero-based proof cost network to aid game
  Junxiao Song, Mingchuan Zhang, Y K Li, Y Wu, and            solving. In International Conference on Learning
  Daya Guo. 2024. DeepSeekMath: Pushing the limits            Representations.
  of mathematical reasoning in open language models.       Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, M Rabe,
  arXiv [cs.CL].                                             Charles Staats, M Jamnik, and Christian Szegedy.
                                                             2022. Autoformalization with large language mod-
David Silver, Thomas Hubert, Julian Schrittwieser, Ioan-     els. Neural Inf Process Syst, abs/2205.12615:32353–
  nis Antonoglou, Matthew Lai, Arthur Guez, Marc             32368.
  Lanctot, Laurent Sifre, Dharshan Kumaran, Thore
  Graepel, Timothy Lillicrap, Karen Simonyan, and          Yuxi Xie, Anirudh Goyal, Wenyue Zheng, Min-Yen
  Demis Hassabis. 2018. A general reinforcement              Kan, Timothy P Lillicrap, Kenji Kawaguchi, and
  learning algorithm that masters chess, shogi, and go       Michael Shieh. 2024. Monte carlo tree search boosts
  through self-play. Science, 362(6419):1140–1144.           reasoning via iterative preference learning. arXiv
                                                             preprint arXiv:2405.00451.
Yuxuan Tong, Xiwen Zhang, Rui Wang, Ruidong Wu,
  and Junxian He. 2024. DART-math: Difficulty-             Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren,
  aware rejection tuning for mathematical problem-           Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and
  solving. arXiv [cs.CL].                                    Xiaodan Liang. 2024a. DeepSeek-Prover: Advanc-
                                                             ing theorem proving in LLMs through large-scale
Jonathan Uesato, Nate Kushman, Ramana Kumar, Fran-           synthetic data. arXiv preprint arXiv:2405.14333.
  cis Song, Noah Siegel, Lisa Wang, Antonia Creswell,
  Geoffrey Irving, and Irina Higgins. 2022. Solving        Huajian Xin, Z Z Ren, Junxiao Song, Zhihong Shao,
  math word problems with process- and outcome-              Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
  based feedback. arXiv [cs.LG].                             Xuan Lu, Qiushi Du, Wenjun Gao, Qihao Zhu, Dejian
                                                             Yang, Zhibin Gou, Z F Wu, Fuli Luo, and Chong
Haiming Wang, Huajian Xin, Chuanyang Zheng,                  Ruan. 2024b. DeepSeek-prover-V1.5: Harnessing
  Zhengying Liu, Qingxing Cao, Yinya Huang, Jing             proof assistant feedback for reinforcement learning
  Xiong, Han Shi, Enze Xie, Jian Yin, Zhenguo Li, and        and monte-carlo tree search. arXiv [cs.CL].
  Xiaodan Liang. 2023. LEGO-prover: Neural theo-
  rem proving with growing libraries. In The Twelfth       Wei Xiong, Chengshuai Shi, Jiaming Shen, Aviv Rosen-
  International Conference on Learning Representa-           berg, Zhen Qin, Daniele Calandriello, Misha Khal-
  tions.                                                     man, Rishabh Joshi, Bilal Piot, Mohammad Saleh,
                                                             Chi Jin, Tong Zhang, and Tianqi Liu. 2024. Build-
Mingzhe Wang and Jia Deng. 2020. Learning to prove           ing math agents with multi-turn iterative preference
  theorems by learning to generate theorems. Advances        learning. arXiv [cs.LG].
  in Neural Information Processing Systems, 33:18146–      Linting Xue, Aditya Barua, Noah Constant, Rami Al-
 18157.                                                      Rfou, Sharan Narang, Mihir Kale, Adam Roberts,
                                                             and Colin Raffel. 2022. ByT5: Towards a token-free
Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai
                                                             future with pre-trained byte-to-byte models. Transac-
  Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang Sui.
                                                             tions of the Association for Computational Linguis-
  2024. Math-shepherd: Verify and reinforce LLMs
                                                             tics, 10:291–306.
  step-by-step without human annotations. In Proceed-
  ings of the 62nd Annual Meeting of the Association       Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chala-
  for Computational Linguistics (Volume 1: Long Pa-          mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan
  pers), pages 9426–9439, Stroudsburg, PA, USA. As-          Prenger, and Anima Anandkumar. 2023. LeanDojo:
  sociation for Computational Linguistics.                   Theorem proving with retrieval-augmented language
                                                             models. In Neural Information Processing Systems
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten             (NeurIPS).
   Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc V Le,
   and Denny Zhou. 2022. Chain-of-thought prompt-          Lifan Yuan, Ganqu Cui, Hanbin Wang, Ning Ding,
   ing elicits reasoning in large language models. In        Xingyao Wang, Jia Deng, Boji Shan, Huimin Chen,
  Advances in Neural Information Processing Systems,          Ruobing Xie, Yankai Lin, et al. 2024. Advancing llm
   volume 35, pages 24824–24837. Curran Associates,           reasoning generalists with preference trees. In AI for
   Inc.                                                      Math Workshop@ ICML.
Xueliang Zhao, Wenda Li, and Lingpeng Kong. 2023.
  Decomposing the enigma: Subgoal-based demon-
  stration learning for formal theorem proving. arXiv
  [cs.CL].
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
  2022. miniF2F: a cross-system benchmark for for-
  mal olympiad-level mathematics. In International
  Conference on Learning Representations.
Xinyu Zhu, Junjie Wang, Lin Zhang, Yuxiang Zhang,
  Yongfeng Huang, Ruyi Gan, Jiaxing Zhang, and Yu-
  jiu Yang. 2023. Solving math word problems via
  cooperative reasoning induced language models. In
  Proceedings of the 61st Annual Meeting of the Asso-
  ciation for Computational Linguistics.
Daniel M Ziegler, Nisan Stiennon, Jeffrey Wu, Tom B
  Brown, Alec Radford, Dario Amodei, Paul Chris-
  tiano, and Geoffrey Irving. 2019. Fine-tuning lan-
  guage models from human preferences. arXiv
  [cs.CL].
A    Extended Discussions on Related Works

                                                                                     Premise        Proof
             Reference                   Verifier         Task          Output
                                                                                     Retrieval     Search
               GPT-f                                                                              Best First
                                        Metamath         Prover       Proof Step          -
     (Polu and Sutskever, 2020)                                                                    Search
                                                                                                  Best First
                                                                                                   Search
    Lean-Gym (Polu et al., 2023)           Lean          Prover       Proof Step          -
                                                                                                   Expert
                                                                                                  iteration
                                                                                       RAG
             LeanDojo                                                                             Best First
                                           Lean          Prover       Proof step      Offline
         (Yang et al., 2023)                                                                       Search
                                                                                     Database
                                                                                       RAG
           LeanAgent                                                                              Best First
                                           Lean          Prover       Proof step      Online
     (Kumarappan et al., 2024)                                                                     Search
                                                                                     Database
 HyperTree Proof Search (HTPS)           Lean
                                                         Prover       Proof step          -         HTPS
      (Lample et al., 2022)             Metamath
        DeepSeek-Prover                                 Prover
                                           Lean                      Whole Proof          -           -
       (Xin et al., 2024a)                             Reasoning
      DeepSeek-Prover 1.5                               Prover       Proof Step
                                           Lean                                           -        MCTS
       (Xin et al., 2024b)                             Reasoning     Whole Proof
            LLEMA                                       Prover         Proof                      Best First
                                        Any Tool                                          -
    (Azerbayev et al., 2024)                           Reasoning        Text                       Search
       Verify Step by Step                                                                        Best First
                                       ORM-PRM         Reasoning         Text             -
     (Lightman et al., 2023)                                                                       Search

                Table 3: A summary of models for theorem proving and mathematical reasoning


Theorem Proving. Machine learning is currently used in automatic theorem proving to generate the
whole proof, or provide assistance in sequential proofs by finding the right premise or right tactics, or
assisting in theorem prover specific formalization of mathematical statements, as well as combination of
these ideas; see (Xin et al., 2024a,b; Polu and Sutskever, 2020; Jiang et al., 2022a; Wang et al., 2023; Jiang
et al., 2022b; Wu et al., 2022) for some pointers. We review some of these works in more details. A key
component for theorem proving is the formal proof management systems and verifiers like Lean (Moura
and Ullrich, 2021) and Coq (Coq Development Team, 2024). Lean has received particular attention in
the mathematics community for example by its use in verification of some components in the condensed
mathematics research program (Scholze, 2022). We use Lean in this work, and a framework that consists
of a premise retrieval part and a prover that generates step-wise proof tactics.
   Machine learning can be used to find useful premises, definitions and theorems (Irving et al., 2016).
For Coq framework (Coq Development Team, 2024), the authors in (Blaauwbroek et al., 2024) introduce
a graph neural network for embedding the new definitions using a hierarchical representation based on
graph representations of theorems and definitions in the Tactician platform (Blaauwbroek, 2024). This
enables them to use recent proofs and theorems in Coq, while kNN is used for the more recent tactics
written by the user. In Thor (Jiang et al., 2022a), the authors introduce a class of methods to use automated
theorem provers for premise selection. LeanDojo (Yang et al., 2023) provided a framework that retrieves
the premise from a database of Lean premises and uses ReProver to generate tactics for theorem proving
in Lean. LeanAgent (Kumarappan et al., 2024) adds a dynamic database to LeanDojo, which enables the
continual learning of the agent. Besides, a new curriculum learning based on the difficulty of the theorems
is also added.
   Searching over different proofs and tactics is another component explored in various works, for example
(Polu et al., 2023; Xin et al., 2024b; Lample et al., 2022). As discussed in (Polu et al., 2023), any RL
algorithm for theorem proving should address two challenges, namely an infinite dimensional action
space, and the absence of a natural opponent for self-play. Therefore, the authors suggest using expert
iteration (Anthony et al., 2017), which amounts to iteratively fine-tuning a based model and searching to
generate correct proofs. They also introduce lean-gym to facilitate the search procedure in Lean. HTPSs
was introduced in (Lample et al., 2022) which is a new search algorithms within an online reinforcement
learning procedure. The key idea is that the search is represented over a hypergraph, where a policy
network generates tactics composed of sub-goals, and then each goal is expanded for proof using new
tactics. The provability of each goal is approximated using a critic. The idea of keeping the visit counts,
action values and their statistics follows the similar MCTS procedure. In (Gloeckle et al., 2024), the
authors introduce a reinforcement learning based framework for theorem proving in Lean 4, which consist
of using a programming interface based on Aesop for proof search organization, the HTPS ((Lample
et al., 2022)) procedure with an online reinforcement learning step. In (Zhao et al., 2023), the authors
use subgoal learning from reinforcement learning to decompose an informal LLM generated proof into
subgoals and verify using a verifier. They also use a diffusion model for demonstration organization.
   The transformer based language models are used also for theorem proving. For example GPT-f was
introduced in (Polu and Sutskever, 2020) using Metamath as the formalization framework. Besides, they
showed that iterative training a value functionon proofs generated by the prover can continually improve
the performance. Another example is LLEMMA which is based on pretrained Llama Code (Azerbayev
et al., 2024).
   The proofs in some frameworks are already in the language of formal theorem provers. Besides,
the external tools for mathematical reasoning can include codes for mathematical arguments. Machine
learning has been used to help the formalization of mathematical statements suitable for the automatic
theorem provers (Wu et al., 2022; Jiang et al., 2022b; Zhao et al., 2023). Furthermore, there is a spectrum
of methods that starts here with methods operating in a formal language and ends with informal proofs
and solutions in natural language. In MathCoder2 (Lu et al., 2024a), the authors provided pairs of
mathematical codes and the associated natural language versions.
   DeepSeek-Prover (Xin et al., 2024a) generated Lean4 proof data by translating natural language
problems into their formal versions in Lean4. The model produces the whole proof in a single turn.
DeepSeekV1.5 (Xin et al., 2024b) provides a middle ground by generating the whole proof, verifying it
via Lean, and then truncating the proof until the first error. The authors propose additional techniques
relying on proper appending of previous states and including truncate-and-resume in the MCTS procedure.
They also leverage Verification feedback from Lean and improve model’s alignment with the formal
structure of Lean. The authors in (Wang et al., 2023) provide another hybrid solution where first an
informal proof is generated, then broken into sub-components, and then a lemma is retrieved from a library
of lemmas considered as skills, and finally the final formalized proof is generated using the previous
components. They use the framework of Isabelle (Paulson, 1994) for theorem proving.
   Treating mathematical problem solving as a reasoning task has been considered in many works, for
example (Tong et al., 2024; Zhu et al., 2023; Shao et al., 2022, 2024; Guan et al., 2025). Among them,
there are models, like (Shao et al., 2024), based on chain-of-thought (Wei et al., 2022) or program of
thought (Gao et al., 2023; Chen et al., 2022). The generator-verifier configuration has been considered in
(Zhu et al., 2023), where they train a step and path verifier for reasoning. Integrating a tool for improving
reasoning of large language models has been used in (Gou et al., 2023). In contrast to our work, these
models do not rely on theorem provers. The authors in (Wang and Deng, 2020) address the lack of human
labeled theorems and proofs to use for supervised training by training a generative model and, then, use
the synthesized pairs to train a theorem prover model.
   The idea of proof size and using it for guiding the search has been discussed in (Wu et al., 2021;
Polu et al., 2023). There is a line of work related to discovering new mathematical functions or solving
mathematical problems, see for example (Real et al., 2023; Alfarano et al., 2024; Marchetti et al., 2023;
Wenger et al., 2022). However, these works do not rely on proof verifiers and fall outside the scope of this
work.
Figure 4: A simple proof example in Lean on the left shows the min function is symmetric, and its proof tree is at
the right. The numbers next to the boxes refer to the corresponding line numbers in the written proof.


Preference Optimization. Another important step in theorem proving, and many other alignment related
tasks, is to align the output of a given model based on the positive-negative preference pair of samples.
There are online version of RLHF as in (Bai et al., 2022; Ouyang et al., 2022), and offline versions with
either an explicit reward model (e.g. (Christiano et al., 2017; Ziegler et al., 2019)) or an implicit reward
model (e.g. DPO (Rafailov et al., 2024)) to encode the preference. The later method directly optimizes the
model without training any independent reward model. In particular DPO uses Bradley-Terry preference
model and the fact that the optimal solution to the KL-constrained reward maximization objective is known
in closed form to simplify the training loss without dependence on a reward model (Rafailov et al., 2024).
Many follow-up works explored DPO variations and its shortcomings such as reward over-optimization
(Gorbatovski et al., 2024; Ethayarajh et al., 2024).
   Different forms of direct preference optimization have been explored in the recent literature for
enhancing the reasoning capabilities of language models, in particular for mathematical problem solving,
for example (Xiong et al., 2024; Yuan et al., 2024; Jiao et al., 2024; Cobbe et al., 2021; Lightman et al.,
2023; Wang et al., 2024; Pang et al., 2024; Chen et al., 2024; Lu et al., 2024b). The authors in (Xiong
et al., 2024) introduce a multi-turn version of DPO to use feedbacks from the verifiers, in their case
the code interpreters, particularly for multi-turn scenarios, which requires trajectory-level preference
optimization. The trajectory-level preference can be obtained by dataset labels of the gold answers or
ORMs (Cobbe et al., 2021; Lightman et al., 2023). A more fine-grained step-wise supervision can be used
as in PRMs (Lightman et al., 2023) or by leveraging trajectory level preferences (Wang et al., 2024). The
idea of ORM and PRM has also been originally discussed in (Uesato et al., 2022). These works focus on
mathematical reasoning, rather then formal theorem proving, which is the focus of our work. In our work,
the theorem prover automatically provides the preference, which is used either during training or for an
offline generated dataset. Furthermore, our work follows PRM philosophy as we consider feedback from
Lean at each step of proof generation.
   The authors in (Jiao et al., 2024; Yuan et al., 2024) applied the original DPO or KTO by taking trajectory
completion as a meta action. The online iterative versions of DPO originally designed for chat is adapted
to achieve better CoT reasoning in (Pang et al., 2024; Xie et al., 2024). In the papers (Chen et al., 2024;
Lai et al., 2024; Xie et al., 2024; Lu et al., 2024b), the authors have explored generating proxy step-wise
labels for the intermediate steps of the reasoning trajectories.

B    Additional Details
Algorithm 1 DPO dataset generation using the zero accuracy strategy
    Input: training dataset Dtrain , reference policy πref , retrieval model retriever
    D←[]
    for theorem and g.t. proof (T, P ) ∈ Dtrain do
      for proof state and g.t. tactic (st , abt ) ∈ P do
         pt ← retriever(st )                                          // compute the premises for retrieval-augmentation
                     j
         At ← {at ∼ πref (at |st , pt ) | j = 1, . . . , 8}                       // with beam-search (beam-width w = 8)
         sort(At )                                                                 // by decreasing πref (a|st , pt ) (if needed)
         if abt ∈
                / At then
             append abt at the end of At (w = 9)                                      // add the ground truth tactic if needed
         end if
                       j             j
         A+ t ← {at | Lean(at |st , T ) = +}                              // gather Lean feedback for each sampled tactic
                       j             j
         A− t  ←   {a  t | Lean(a      |s
                                     t t  , T ) =  −}
         for y − ∈ A−    t do
             for y + ∈ A+   t do
                if πref (y − |st , pt ) > πref (y + |st , pt ) then
                   x ← dynamic_prompt(st , pt )                               // prompt augmentation by premises dropout
                   D.append((x, y + , y − ))
                   move y + at the end of A+      t to lower its priority // simple heuristic to avoid oversampling y
                                                                                                                                +

                   break                                         // exit the inner loop over A+   t and move to the next y
                                                                                                                               −

                end if
             end for
         end for
      end for
    end for
    Output: D


C     MiniF2F and ProofNet Results

                                                             MiniF2F        ProofNet
                                         ReProver               26.5           13.8
                                         ReProver*              37.7           15.3
                                         LeanListener           36.9           14.4

Table 4: Pass@1 (%) performance of the ReProver (Yang et al., 2023) and our framework, LeanListener, on
MiniF2F and ProofNet. The ReProver* is the newly provided pre-trained model, which we evaluated ourselves.
            (a) Per-theorem proof-length analysis                 (b) Per-theorem relative proof-length comparison

Figure 5: For each valid theorem in the MiniF2F test set, we plot and compare the proof-length performance
for both the LeanListener and ReProver models. 5(a) depicts the proof lengths for the proofs generated by the
ReProver model on the y-axis, and by the LeanListener model on the x-axis. 5(b) illustrates the relative proof-length
advantage of the LeanListener method over ReProver. For each theorem, we plot the difference in proof lengths
generated by both models, observing that instances where LeanListener has a positive advantage outnumber those
where it does not.




            (a) Per-theorem proof-length analysis                 (b) Per-theorem relative proof-length comparison

Figure 6: For each valid theorem in the ProofNet test set, we plot and compare the proof-length performance
for both the LeanListener and ReProver models. 5(a) depicts the proof lengths for the proofs generated by the
ReProver model on the y-axis, and by the LeanListener model on the x-axis. 5(b) illustrates the relative proof-length
advantage of the LeanListener method over ReProver. For each theorem, we plot the difference in proof lengths
generated by both models, observing that instances where LeanListener has a positive advantage outnumber those
where it does not.
