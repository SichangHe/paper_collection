                                        Next-Token Prediction Task Assumes Optimal Data Ordering for LLM
                                                            Training in Proof Generation
                                                 Chenyang An1 * , Shima Imani2 , Feng Yao1 , Chengyu Dong1 , Ali Abbasi3 ,
                                              Harsh Shrivastava2 , Samuel Buss1† , Jingbo Shang1† , Gayathri Mahalingam2† ,
                                                                 Pramod Sharma2† , Maurice Diesendruck2†
                                             University of California, San Diego1 Microsoft Research2 Vanderbilt University3
                                                           {c5an, fengyao, cdong, sbuss, jshang}@ucsd.edu
                                              {shimanihs, hshrivastava, gmahalingam, pramod.sharma}@microsoft.com
                                                                         ali.abbasi@vanderbilt.edu
                                                                             moglobal@gmail.com
                                                           Abstract                    1 Introduction
                                                                                                 Recent works have shown the potential of LLMs
arXiv:2411.00863v2 [cs.CL] 3 Jul 2025




                                            In the field of large language model (LLM)-          to perform mathematical reasoning and proof gen-
                                            based proof generation, despite extensive train-     eration in both natural language and formalized
                                            ing on large datasets such as ArXiv, LLMs            environments (Yang et al., 2023a; Welleck et al.,
                                            still exhibit only modest performance on prov-
                                                                                                 2021; Lample et al., 2022; Mikuła et al., 2023;
                                            ing tasks of moderate difficulty. We believe
                                            that this is partly due to the widespread pres-      Wang et al., 2023).
                                            ence of suboptimal ordering within the data             Meanwhile, leading models consume far more
                                            for each proof used in training. For example,        data than a human could (datasets like OpenWeb-
                                            published proofs often follow a purely logical       Math contain 14B tokens), and still perform sub-
                                            order, where each step logically proceeds from       optimally on reasoning benchmarks (Paster et al.,
                                            the previous steps based on the deductive rules.     2023; Azerbayev et al., 2023; Touvron et al., 2023;
                                            This order is designed to facilitate the verifi-
                                                                                                 Dubey et al., 2024; Paster et al., 2023). This is also
                                            cation of the proof’s soundness, rather than
                                            to help people and models learn the discovery        true for downstream reasoning tasks where LLMs
                                            process of the proof. In proof generation, we        need further fine-tuning (Yang et al., 2023b; An
                                            argue that the optimal order for one training        et al., 2024). We identify this phenomenon as the
                                            data sample occurs when the relevant interme-        training inefficiency problem.
                                            diate supervision for a particular proof step in        One possible explanation for such low training
                                            the proof is always positioned to the left of that   efficiency in proof generation for LLMs is poor in-
                                            proof step. We call such order the intuitively
                                                                                                 ternal order within each training data sample in the
                                            sequential order. We validate our claims us-
                                            ing two tasks: intuitionistic propositional logic    math domain. For instance, consider the purely
                                            theorem-proving and digit multiplication. Our        logical order that many textbook proofs follow,
                                            experiments verify the order effect and provide      where each step logically proceeds from the previ-
                                            support for our explanations. We demonstrate         ous steps based on the deductive rules. This order
                                            that training is most effective when the proof       is widely adopted for presenting proofs publicly
                                            is in the intuitively sequential order. Moreover,    because it allows for straightforward verification
                                            the order effect and the performance gap be-
                                                                                                 of the proof’s correctness. However, from a proof
                                            tween models trained on different data orders
                                            can be substantial – with an 11 percent im-          discovery perspective, this order is not intuitive,
                                            provement in proof success rate observed in          i.e. not the order in which the proof is actually
                                            the propositional logic theorem-proving task,        discovered. For human learners, the most intuitive
                                            between models trained on the optimal order          order of proof steps is one in which all steps con-
                                            compared to the worst order. Lastly, we define       tributing to the discovery of a particular proof step
                                            a common type of order issue in advanced math        are presented prior to it. We call such order the
                                            proofs and find that 17.3 percent of theorems        intuitively sequential order. These steps, which aid
                                            with nontrivial proofs in the first two chapters
                                                                                                 in the discovery of a given proof step, are referred
                                            of a widely used graduate-level mathematics
                                            textbook suffer from this issue. A detailed list     to as intermediate supervision for that step.
                                            of those proofs is provided in the appendix.            Consider a concrete scenario where an intuitive
                                                                                                 sequential order is preferable to a purely logical
                                        *    Internship project at Microsoft Research.           one in learning and model training. When prov-
                                        †
                                             Corresponding authors.                              ing a theorem, a researcher quickly identifies a key
                      Purely Logical Order                                Intuitively Sequential Order
         Given the function 𝑓 𝑥 = 𝑥 2 + 4𝑥 + 5. Is this function   Given the function 𝑓 𝑥 = 𝑥 2 + 4𝑥 + 5. Is this function
         always positive?                                          always positive?
         Solution:                                                 Solution:
         Step 1: The function is equal to 𝑥 2 + 4𝑥 + 4 + 1         Step 3: Apply lemma: the square of an equation is
                                                                   always positive
         Step 2: The function is equivalent to 𝑥 + 2 2 + 1
                                                                   Step 2: The function is equivalent to 𝑥 + 2 2 + 1
         Step 3: Apply lemma: the square of an equation is
         always positive.                                          Step 1: The function is equal to 𝑥 2 + 4𝑥 + 4 + 1


Figure 1: An illustrative example of the purely logical order versus the intuitively sequential order. The arrows
indicate the direction of intermediate supervision.


lemma but must first perform preliminary steps to                  inefficiency problem of LLMs in solving reason-
apply it. Textbooks typically present these steps                  ing tasks is partly due to the suboptimal order of
first, following a purely logical order. However, in               each proof’s data during training. We claim that
LLM training—and human learning—these steps                        the intuitively sequential order is the optimal or-
are easier to derive after seeing the key lemma,                   der for fine-tuning models. We show that there are
which serves as intermediate supervision to these                  two causes for the order effect. Assume we have
steps. Without the lemma, it is unclear why these                  proof step a, and proof steps {ai } that serve as
preliminary steps are necessary. We refer to this                  intermediate supervision toward a, and they occur
issue as Delayed Insight Issue (DII)—a problem                     in the order “a, {ai }”. The first cause is that when
where crucial insights are introduced too late, dis-               learning to predict a, the model will not directly
rupting intuition and understanding. To avoid DII,                 learn to use the supervision {ai }, because it does
training data should present the lemma before the                  not look forward during training. The second cause
preliminary steps in such cases. DII represents one                is that this order also induces the model to fit the
of the many causes of the difference between the                   non-existent dependency of {ai } on a, which we
purely logical order and the intuitively sequential                call the spurious relation. Note that in reasoning
order for advanced math proofs.                                    tasks, intermediate supervision is usually another
   We give a simple illustrative example of DII in                 sequence of reasoning steps.
Figure 1. In Figure 1, Step 3 serves as the inter-                    To verify our claims, we conduct experiments
mediate supervision that assists in predicting Step                on two downstream tasks: (1) 4-by-4 digit multi-
2, which in turn serves as the intermediate supervi-               plication and, (2) intuitionistic propositional logic
sion that assists in predicting Step 1. Inexperienced              theorem-proving. Various metrics were employed
students typically struggle to understand this proof               to measure model performance. The results con-
in the purely logical order on their first read, as it is          sistently show that models fine-tuned/trained-from-
unclear why the problem statement should lead to                   scratch on the intuitively sequential proofs outper-
Step 1. If they are instead taught to first apply the              formed those fine-tuned/trained-from-scratch on
lemma as in Step 3, the learning process becomes                   proofs in other orders.
faster. In practice, the confusion of suboptimal or-                  Our experiments also validate the two causes for
der can be overcome through repeated reflection                    the order effect we propose. We find that models do
for humans. As for model training with next to-                    not learn to use future tokens to predict the current
ken prediction, without introducing more elaborate                 proof step. We also show evidence in the multipli-
training objectives, the only way to achieve a sim-                cation task that models are negatively impacted by
ilar effect is to modify the order of the training                 spurious step dependencies learned during training
data.                                                              when it’s trained on data in suboptimal orders.
   Given that (i) proofs and reasoning are often                      To demonstrate the prevalence of ordering is-
presented in the suboptimal order, and (ii) next-                  sues in mathematical texts, we analyze the first two
token prediction is the predominant method used                    chapters of a widely used graduate-level textbook
for pre-training and fine-tuning cutting-edge autore-              in analysis, which contain a total of 57 theorems
gressive LLMs, we hypothesize that the training                    with nontrivial proofs. We find that 17.3 percent
of these proofs exhibit DII. A detailed list of the    needs to utilize information in the middle.
affected proofs is provided in Appendix A.2.           Order effect on LLM: digits.         For long-digit
   Our main contributions are summarized as fol-       addition, prior works demonstrated that reversing
lows:                                                  numbers in training data can help LLMs achieve
   • We find that data order significantly affects     better performance on digit-addition tasks (Lee
     LLM training efficiency on reasoning tasks,       et al., 2023; Zhou et al., 2023b, 2024). While their
     which we refer to as the order effect.            work only applies to digit computation since they
   • We claim optimal order to be the intuitively      employed digit-wise reversal, our work studies the
     sequential order, where intermediate supervi-     positional role of intermediate supervision in gen-
     sion is placed on the left.                       eral for the proof generation task.
   • Through the propositional logic theorem-
                                                       3     Preliminary
     proving task and the digit multiplication task,
     our experiments show that this order effect is    3.1    Problem setting
     due to next-token prediction. Two causes are      Given a nondeterministic algorithm A and input r0
     (1) LLMs do not look forward during training,     from the problem space, we assume:
     (2) LLMs may learn spurious token dependen-
     cies if trained with data samples in suboptimal       1. Finiteness.         Algorithm A generates
     order.                                                   a finite sequence of steps A(r0 ) =
   • We show that the Delayed Insight Issue—a                 r1 , A({r0 , r1 }) = r2 , ..., A({ri }n−1
                                                                                                    i=0 ) =
     specific ordering problem—frequently arises              rnr0 , where rnr0 is the last step that A will
     in advanced mathematical proofs, as illus-               generate when given r0 , which usually is the
     trated by 9 examples from a popular textbook             final answer. Here nr0 is the position of the
     listed in the appendix.                                  last token (final answer) generated by algo-
                                                              rithm A with input r0 .
2   Related Work                                           2. Intuitively sequential order.           Each step
                                                              ri highly depends on rj for 1 <= j < i,
Problem of next-token prediction training.
Existing research has exposed weaknesses in the               i.e. the probability for A({ri }j−1 i=0 ) = rj is
next-token prediction mechanism. For example,                 high for all j. For every r0 , {ri }mi=0 serves as
(Berglund et al., 2023) showed the Reversal Curse:            intermediate supervision for models to predict
a model trained on “A is B" does not know that “B             rm+1 for all 0 <= m < nr0 . We call this
is A". (Golovneva et al., 2024) proposed to train a           order the intuitively sequential order. All other
model both sequentially and reversely, using two              orders of the sequence have a weaker right-
tasks together to enhance performance. In contrast,           to-left dependency than the aforementioned
our work demonstrates that optimal orders exist for           order.
next-token prediction learning, specifically by the       Given a model Mθ with θ as weights of the
rule of positioning intermediate supervision to the    model, our goal is to enable Mθ to imitate algo-
left. (Bachmann and Nagarajan, 2024) highlighted       rithm A through the next-token prediction task.
a similar toy problem known as the star-path prob-     Specifically, we aim to find weights θ0 such
                                                                                  nr0
lem, where initial errors substantially reduced the    that θ0 = arg minθ n1r Σm=1    Er0 |Mθ ({ri }m
                                                                                                    i=1 ) −
                                                                              0
model’s ability to predict later tokens.                       m
                                                       A({ri }i=1 )|. To put it in another way, we want
                                                                                                        nr
Order effect on LLM: context. Several works            the model to predict the entire sequence {ri }i=10
have studied how disrupting order in prompts might     given r0 . Importantly, the loss function does not
affect model performance. (Chen et al., 2024)          exclusively focus on rnr0 but also accounts for the
showed that LLMs achieve the best performance          intermediate steps rm for m = 1, ..., rnr0 −1 when
on GSM8K when the premise order aligns with the        computing loss. This scenario arises in practice in
context required in intermediate reasoning steps.      theorem-proving tasks, where we are interested in
(Liu et al., 2024) discover the lost in-the-middle     both the intermediate proofs and the final answer.
phenomenon in the long-context scenario: LLM
performance is best when relevant information is       3.2    Causes of the order effect
placed at the beginning or the end of the input con-   In preparation for training model Mθ to learn A,
text, while the performance is worst when the LLM      we collect a set of training data. Each data sample is
                                  nr
a finite sequence of steps {ri }i=00 . In the next-token       follow the original sequential order (referred to as
prediction task, given a training data point r =               SEQ order, see Table 1). We note that SEQ or-
     nr
{ri }i=00 , autoregressive LLMs update their parame-           der follows the intuitively sequential order: all the
                                   nr0
ter by minimizing the loss of Σm=1       |Mθ ({ri }m i=0 )−    previous tactics and states help generate the next
          m
A({ri }i=0 )| over batches. Now, without loss of               tactic and state. For the second type, the proofs
                                        nr
generality, if the data point {ri }i=00 in the set of          are reversed (referred to as SER order), such that
training data satisfies the assumption above, and              the last tactic and the last state become the first
is reordered into {r0 , rnr0 , r1 , ..., rnr0 −1 }, the fol-   tactic and the first state, the second-to-last tactic
lowing things happen:                                          and the second-to-last state become the second tac-
                                                               tic and the second state, and so forth. Note that
    • Model cannot look forward: intermediate                  this dataset was published after the Llama-2 family
      supervision fails to help if placed on the               was released so the model hasn’t seen this dataset
      right. The model will not be able to learn               during pre-training. See an example of a statement
      the dependency of rnr0 on {r1 , ..., rnr0 −1 }.          and a proof in Appendix A.4.
      Through the next-token prediction training                  For training and testing, we select all statements
                                   nr
      loss, given ri ∈ r = {ri }i=00 , the model has           in the PropL dataset that are proved using 3, 4,
      no way to look forward and use rj with j > i             or 5 tactics, totaling 21,000 instances. The last
      to help learn to predict ri . The model would            1,000 statements are reserved for testing so that we
      find it much harder to learn to predict rnr0 di-         have 20,000 training instances and 1,000 testing in-
      rectly from r0 , since this task is not split into       stances. During fine-tuning, the statement together
      sub-tasks like given {r0 } predict r1 , given            with its proof (in SEQ or SER order) forms one
      {r0 , r1 } predict r2 , and so on (Wies et al.,          training data sample. Models see each training data
      2022).                                                   sample at most once during training.
    • Model may learn spurious rela-                           4.1.2   4-by-4 digit multiplication
      tions.        Since rnr0 is positioned before
                                                               For our second dataset, we choose the 4-digit by
      {r1 , ..., rnr0 −1 }, the model might learn a
                                                               4-digit multiplication task as a proof generation
      spurious dependency of {r1 , ..., rnr0 −1 }
                                                               task. After a pair of 4-digit numbers (num1, num2)
      on rnr0 at the early stage of training, and
                                                               is picked, the problem is generated as: “Tell me
      could take many training steps to realize that
                                                               what is num1*num2 and prove it". A proof of
      rnr0 contains no information for predicting
                                                               a problem consists of the steps where we induce
      {r1 , ..., rnr0 −1 }.
                                                               different axioms of the integer ring to derive the
Later in Sec 4.3 we display evidence supporting                middle steps for computation, and the last step of
our claim that the aforementioned two reasons are              the proof is the final answer of the multiplication.
among the causes of the order effect.                             We use an algorithm to generate the problems,
                                                               the proofs, and the final answers of 4-digit by 4-
4     Experimental Setup                                       digit multiplication. It has been shown that such
                                                               problems, even prompted with “Let’s think step by
4.1     Tasks and datasets
                                                               step”, are challenging for cutting-edge models like
4.1.1   Intuitionistic propositional logic                     GPT-4 (Liu and Low, 2023). We create three types
        theorem-proving                                        of proofs with the same proof steps but in different
For the first dataset, we use theorem statements and           orders, whose compositions are summarized in the
proofs in intuitionistic propositional logic (PropL),          table. Examples of all three types of data can be
as introduced in (An et al., 2024). A proof consists           found in the Appendix A.4. Note that for the multi-
of tactics and intermediate states, where a tactic             plication task, for proofs in the SEQ order, given
refers to an actual proof step, and a state repre-             a proof step, all previous steps serve as the natural
sents what remains to be proved after a tactic is              intermediate supervision toward that step, hence
applied. Both the statements and the proofs are                making this dataset ideal for testing our claims.
written in Lean, a popular formalized environment                 For training and testing, we first enumerated all
for theorem-proving in the mathematical commu-                 4-digit by 4-digit tuples. The list of tuples was then
nity (de Moura et al., 2015). We have two types                randomly shuffled. We used the first 1,000,000
of PropL data. In the first type of data, all proofs           tuples as our training number tuples. Together with
the proofs, they formed our training dataset. We          4.3   Models and hyperparameters
used the last 1,000 tuples to construct our testing
                                                          We use Gemma-2B (Team et al., 2024) and Llama-
number tuples.
                                                          2-7B-hf (Touvron et al., 2023) as our proof gen-
4.2   Metrics                                             erators and the default pre-trained tokenizers for
                                                          both of the models, even in train-from-scratch ex-
Metrics for the intuitionistic propositional logic
                                                          periments. We use the function AutoModelFor-
theorem-proving task. For the theorem-proving
                                                          CausalLM.from_config from Huggingface to ran-
task, we evaluate model performance using two key
                                                          domly initialize the models. Unless otherwise
metrics. The first metric is tactic prediction correct-
                                                          stated, the models that we fine-tune are pre-trained
ness, which assesses whether the tactics generated
                                                          with default weights. The learning rate of all train-
by the model can prove the theorem. The second
                                                          ing processes is set to be 5 × 10−5 . We use Adam
metric is proof generation correctness, which not
                                                          as our optimizer (Diederik, 2014). All training pro-
only checks if the generated tactics prove the the-
                                                          cesses are performed on 4 NVIDIA A100, with
orem, but also ensures that all intermediate states
                                                          the per-device batch size set to 1. This makes the
are correctly generated. The entire evaluation pro-
                                                          batch size to be 4 for all experiments. All experi-
cess is automated using Lean. We input the theo-
                                                          ments are completed within 24 hours, except for the
rem statement and the model-generated tactics into
                                                          train-from-scratch experiments, which take about
Lean. Lean computes a state after applying the
                                                          3 days to finish. Every training process is based on
given tactic to the given state. We then compare the
                                                          prediction with cross-entropy loss.
model-generated intermediate states with the states
computed by Lean. Lean automatically determines              During the experiments, for the multiplication
whether the tactics successfully prove the theorem.       task, we fine-tune Gemma-2b and Llama-2-7b-hf
Metrics for the multiplication task. In contrast          on SEQ, PSER, and SER datasets, resulting in a
to prior works, we treat 4-digit by 4-digit computa-      total of six models. We also train from scratch
tion as a proof generation task, not as a computation     randomly initialized Gemma-2b on SEQ, PSER,
task (Liu and Low, 2023; Zhou et al., 2023b, 2024;        and SER as well so that we have additional three
Lee et al., 2023). We evaluate model performance          models. We call models that are fine-tuned/trained
using the proof correctness metric, final answer          from scratch on SEQ, PSER, and SER datasets as
correctness metric, and Step 1 correctness metric,        SEQ models (3 in total), PSER models (3 in total),
where Step 1 refers to the first step in the proof        and SER models (3 in total) respectively.
according to the optimal order in the multiplication         For the theorem-proving task, we fine-tune
task. For the proof correctness metric, our model         Llama-2-7b-hf on SEQ and SER datasets. We call
is prompted with only the problem, “Tell me what          the two models the SEQ model and the SER model.
num1*num2 is and prove it”, and a successful gen-         Zero-shot performance of the models on the mul-
eration of the model requires every proof step in         tiplication and theorem-proving tasks.           We
the generation to be correct, together with the final     begin by evaluating the zero-shot performance of
answer. It is in parallel with the usual proof gen-       both Gemma-2b and Llama-2-7b-hf on two tasks
eration scenario, where one is given a statement          with 3-shots examples. For the theorem-proving
and is asked to generate the proof to prove whether       task, we prompt Llama-2-7b-hf with a theorem
the statement is true or false. In mathematical rea-      statement and request it to generate a proof in Lean,
soning, simply giving out a true or false answer is       see Figure 5f. The model, however, fails to produce
not enough without correct convincing arguments.          any correct solution measured by either the tactic
For the final answer prediction task, we prompt the       prediction metric or the proof correctness metric,
model in two ways. The first prompt contains only         achieving a success rate of 0 out of 1000 test cases.
the problem. The second prompt contains both the          For the multiplication task, we conduct tests using
problem and all the intermediate proof steps except       100 cases. The models are provided with two types
the final answer correspondingly. For both prompts,       of prompts. The first prompt is, “Tell me what
we check the correctness of the final answer. For         num1 * num2 is and prove it." The second prompt
Step 1 correctness metric, we prompt the model            incorporates a chain-of-thought (CoT) instruction:
with the problem and the intermediate proof steps,        “Tell me what num1 * num2 is and prove it. Let’s
except for Step 1. We then check the correctness          think step by step." Both two prompts also include
of Step 1 output by the model.                            3 examples in their corresponding formats. De-
                                        Table 1: Three Types of Data. See Appendix A.4 for examples.

                             Type Name                                                   Proof Steps Composition
                           Sequential (SEQ)                                      Problem + Sequential Proof + Final Answer
               Partially Sequentially Reversed (PSER)                       Problem + Sequentially Reversed Proof + Final Answer
                    Sequentially Reversed (SER)                             Problem + Final Answer + Sequentially Reversed Proof

                  SEQ                                                SEQ                                                  SEQ
                  PSER
                  SER                                          0.6
                                                                     PSER
                                                                     SER
                                                                                                                    0.4   PSER
                                                                                                                          SER
           0.6
                                                                                                                    0.3
Success rate




                                                    Success rate




                                                                                                         Success rate
           0.4                                                 0.4
                                                                                                                    0.2
           0.2                                                 0.2                                                  0.1
           0.0                                                 0.0                                                  0.0
                  10000 20000 30000 40000 50000                      10000     20000     30000   40000                           50000     100000     150000
                           Checkpoint                                           Checkpoint                                               Checkpoint

 (a) Pre-trained Gemma-2b tested on                  (b) Pre-trained Llama-7b tested on proof             (c) Train-from-scratch Gemma-2b
 proof generation                                    generation                                           tested on proof generation
                  SEQ                                                SEQ                                            0.8   SEQ
           0.8    PSER
                  SER                                          0.8   PSER
                                                                     SER
                                                                                                                          PSER
                                                                                                                          SER

           0.6                                                 0.6                                                  0.6
Success rate




                                                    Success rate




                                                                                                         Success rate
           0.4                                                 0.4                                                  0.4
           0.2                                                 0.2                                                  0.2
           0.0                                                 0.0                                                  0.0
                  10000 20000 30000 40000 50000                      10000     20000     30000   40000                           50000     100000     150000
                           Checkpoint                                           Checkpoint                                               Checkpoint

 (d) Pre-trained Gemma-2b tested on fi-              (e) Pre-trained Llama-7b tested on final             (f) Train-from-scratch Gemma-2b tested
 nal answer                                          answer                                               on final answer

 Figure 2: Experimental results on the multiplication task measured by the metrics of proof generation correctness
 and final answer correctness. SER models achieves 0 percent success rate for all cases. In (a), (b) and (c), models
 are prompted with the problems only and performances are measured by the proof correctness metric. In (d), (e) and
 (f), SEQ and PSER models are prompted with both the problems and the intermediate steps, whereas SER model is
 prompted with the problems only. Performances are measured by the final answer correctness metric. Results show
 no evidence for the claim that the model can look forward during training.


 spite these variations, both pre-trained Gemma-2b                                     theorem statement. See Figure 5f for prompting
 and Llama-2-7b-hf fail on the 4-by-4 multiplication                                   configuration. We use both the tactic prediction
 task with a success rate of 0/1000 based on proof                                     metric and the proof correctness metric to measure
 correctness and final answer accuracy. This result                                    model performance for this task. As shown in Fig-
 aligns with expectations, as the 4-by-4 multiplica-                                   ure 2a, 2b, 2c, 4a, 4b, SEQ models learn the task a
 tion task poses significant challenges even for more                                  lot more efficiently than the models PSER models
 advanced models like GPT-4 (Liu and Low, 2023).                                       and SER models for the multiplication task. For
                                                                                       the propositional logic theorem-proving task, the
 Main observation: training efficiency is maxi-
                                                                                       SEQ model also outperforms the SER model by
 mized when models are trained on intuitive se-
                                                                                       20 percent measured by the tactic prediction met-
 quential order.       We conduct experiments on
                                                                                       ric. Note that for the multiplication task, for all
 both the intuitionistic propositional logic theorem-
                                                                                       three base models, PSER models do get a small
 proving task and the multiplication task. For all
                                                                                       number of test problems right in the second half
 the nine models that are fine-tuned/trained from
                                                                                       of the training, and SER models failed all test data
 scratch for the multiplication task, we prompt the
                                                                                       consistently. This performance difference is in line
 models with “Tell me what is num1*num2 and
                                                                                       with our claim that putting more intermediate su-
 prove it”, where (num1, num2) is in the testing
                                                                                       pervision on the left will improve model training
 data. See Figure 5a, 5b, 5c for prompting config-
                                                                                       efficiency in reasoning.
 uration. We then measure the generated output of
 the model by the proof correctness metric. For the                                    LLMs don’t look forward in training. For this
 intuitionistic propositional logic theorem-proving                                    experiment, we focus on the multiplication task.
 task, we prompt the SEQ and SER models with the                                       We use the same 9 models as in our first experi-
ments, but for SEQ and PSER models, we prompt           compared to SEQ models based on the evidences
the model with both the problems and the inter-         shown in Figure 3a, 3b, 3c. This slow convergence
mediate steps excluding the final answer, so that       in the early training stage shows that SER models
we exclude the snow-balling effect (the effect that     try hard to fit the spurious dependency of Step 1 on
the earlier errors model makes will affect model        all other proof steps at first. They need more train-
performance in later outputs). See Figure 5d, 5e for    ing steps to realize that Step 1 does not depend on
prompting configuration. For SER models, since          all the other proof steps, including the final answer.
there is no intermediate step before the final an-
swer in the data, we prompt it with the problem         5   Other Results and Discussion
only. See Figure 5c for prompting configuration in
this case. We use final answer prediction correct-      Bias in pre-training data is not the major cause
ness for this experiment to measure model perfor-       of the order effect. One might argue that the
mance. As displayed in Figure 2d, 2e, 2f, in this       order bias in the pre-training dataset could poten-
setting, for all three base models, models that are     tially be the primary cause of the order effects ob-
fine-tuned/trained from scratch on SER got 0 final      served in this study. However, for the multiplica-
answers correct consistently. The results of SER        tion task, we conduct controlled experiments on
show that LLMs don’t look forward during training,      both pre-trained models and randomly initialized
i.e. fail to learn to use intermediate supervision on   model, thereby ruling out this possibility given the
the right in training.                                  results as shown in Figure 2f.
   We also note that when both the problem and          SEQ is better than PSER even when problem
all intermediate proof steps (except for the final      and proof steps are masked during training.
answer) are provided as prompts to the models,          In this experiment, we don’t use our 9 models men-
SEQ models still outperform PSER models in              tioned before. We fine-tune pre-trained Gemma-2b
terms of final answer correctness, as shown in Fig-     on SEQ and PSER but with all tokens except final
ure 2d, 2e, 2f. See Figure 5d, 5e for prompting         answers masked out. Therefore the only input-
configuration. By giving the correct intermediate       output pair that enters into the loss function is
steps as prompts to both SEQ and PSER models,           (problem+intermediate proof steps, final answer).
we eliminate the snowballing effect during model        During testing, we prompt both models with the
generation.                                             problem and the intermediate proof steps. See Fig-
SER models learn spurious dependency. In                ure 5d,5e for the prompting configuration. Fig-
this experiment, we test our SEQ and SER mod-           ure 10b shows that the model fine-tuned on masked
els for the multiplication task. The testing prompt     SEQ outperforms the model fine-tuned scratch on
of the model is the problem only, and the mod-          masked PSER measured by final answer correct-
els are expected to generate the full proof. See        ness for the pre-trained case.
Figure 5a, 5c. We use the Step 1 correctness met-       Models treat the same data with reversed order
ric, i.e. checking the correctness of Step 1 in the     very differently during training.          Lastly, we
models’ generated output. Step 1 is the decompo-        study the question of whether the model will con-
sition step that splits the 4-digit number into sim-    verge faster when it is fine-tuned on SEQ after it is
ple terms, e.g. 2345 to 2*1000+3*100+4*10+5*1.          fine-tuned on PSER. For the multiplication task, we
During the training, the model should be able to        first fine-tune Gemma-2b on PSER for 50000 steps,
learn this step quickly given the problem due to        and then keep fine-tuning it on SEQ. As shown in
its simplicity. Indeed, from Figure 3a, 3b, we see      Figure 10a, we see that the model converges much
that for SEQ models based on pre-trained models,        slower after it’s fine-tuned on PSER compared to
they learn Step 1 almost perfectly after the first      the case when the pre-trained model is directly
2500 steps. For the randomly initialized Gemma-         fine-tuned on SEQ, measured by the proof correct-
2b trained from scratch on SEQ, the model perfor-       ness metric. This suggests that the knowledge that
mance measured by the Step 1 correctness metric         the model learns from the proof in reverse order
quickly reaches more than 90% and is approach-          doesn’t help but hurts it in learning the proof in the
ing perfect scores followed by some fluctuations,       right order. Essentially, models treat the same data
as shown by Figure 3c. For SER models, how-             with reversed order very differently during training.
ever, they converge much slower measured by the         Discussion: artificiality of the dataset. It is im-
Step 1 correctness metric in the early training stage   portant to note that the datasets used in this study
           1.00      SEQ
                     SER
                                                                       1.0   SEQ
                                                                             SER
                                                                                                                                         1000        SEQ
                                                                                                                                                     SER

           0.75
Success rate




                                                            Success rate




                                                                                                                              Success rate
                                                                       0.8                                                                   900
           0.50
           0.25                                                        0.6                                                                   800
           0.00
                     10000 20000 30000 40000 50000                                 10000 20000 30000 40000                                             20000 40000 60000 80000
                                 Checkpoint                                              Checkpoint                                                         Checkpoint

 (a) Pre-trained Gemma-2b tested on                          (b) Pre-trained Llama-7b tested on Step                           (c) Train-from-scratch                    Gemma-2b
 Step 1                                                      1                                                                 tested on Step 1

 Figure 3: Step 1 success rate for the multiplication task. In (a), (b) and (c), models are prompted with the problem
 only. Results show that models learn the spurious dependency of Step 1 on Step 2-8, which negatively impact their
 ability to predict Step 1.


                           SEQ
                           SER                                                                                   0.20   SEQ
                                                                                                                        SER

               0.4                                                                                               0.15
Success rate




                                                                                                      Success rate
                                                                                                                 0.10
               0.2
                                                                                                                 0.05
                           2000        4000          6000            8000                                               2000                       4000     6000         8000
                                              Checkpoint                                                                                            Checkpoint
   (a) Pre-trained Llama-2-7b-hf tested on tactic prediction                                           (b) Pre-trained Llama-2-7b-hf tested on proof generation

 Figure 4: Experiment result on the intuitionistic propositional logic theorem-proving task. In (a) and (b), models are
 prompted with the theorem statement. For (a), performance is measured by the tactic prediction metric. For (b),
 performance is measure by the proof generation metric. With the same training steps, the model fined-tuned on
 SEQ proofs perform better than the model fined-tuned on SER proofs


 for training and evaluating models are artificially                                          We claim that the optimal order of a data sample,
 constructed. Ideally, we would prefer to train and                                           which we call the intuitively sequential order, is
 evaluate models on graduate- and research-level                                              to put intermediate supervision toward a particular
 mathematical theorems and proofs. However, al-                                               proof step on the left for all proof steps in a data
 though state-of-the-art (SOTA) models can partially                                          sample. We show the two causes for this order
 reorder proofs into a more intuitively sequential                                            effect: given suboptimal data order, training inef-
 structure, there remains no reliable method for ver-                                         ficiency arises from (i) inability to look forward
 ifying the correctness of model-generated proofs.                                            during training, i.e. learning to use future interme-
 To illustrate the widespread nature of ordering is-                                          diate supervision to predict the current token, (ii)
 sues in mathematical texts, we include in the ap-                                            propensity to learn spurious token dependencies in
 pendix a list of proofs exhibiting the Dependency-                                           the early training stage. Our experiments on the
 Inversion Issue (DII), drawn from graduate-level                                             theorem-proving task and 4-by-4-digit multiplica-
 mathematics textbooks. These constitute 17.3 per-                                            tion provide strong support for these explanations,
 cent of the theorems with nontrivial proofs in the                                           highlighting the importance of finding the optimal
 first two chapters of the examined textbook, high-                                           data order in model training. We explicitly define
 lighting the severity of ordering problems in ad-                                            a particular kind of order issue, Delayed Insight
 vanced mathematical reasoning.                                                               Issue, that frequently appear in advanced math text-
                                                                                              books, and we present a list of proofs that suffer
 6              Conclusion and Future work                                                    from DII in the appendix. Notably, 17.3 percent
                                                                                              of theorems with non-trivial proofs in the first two
 In conclusion, our study highlights the significant                                          chapters of the textbook we analyze suffer from
 impact of order for each data sample on LLMs’                                                DII.
 training efficiency for the proof generation task.
   A promising direction for future work is to in-           Computational Linguistics and Speech Processing
vestigate this claim during the pre-training stage of        (ROCLING 2023), pages 188–193.
LLMs for reasoning tasks. Another future work is           Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
to employ machine learning methods to discover               Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
optimal data order. This holds significance on its           Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
own, independent of the gain it can bring to model           Nakano, Christopher Hesse, and John Schulman.
                                                             2021. Training verifiers to solve math word prob-
training. For example, suppose the true supervision          lems. arXiv preprint arXiv:2110.14168.
structures are discovered for mathematical proofs
and those proofs are reordered accordingly. In that        Alex Davies, Petar Veličković, Lars Buesing, Sam
                                                             Blackwell, Daniel Zheng, Nenad Tomašev, Richard
case, it might facilitate the learning process of stu-       Tanburn, Peter Battaglia, Charles Blundell, András
dents, making it linear and intuitive.                       Juhász, et al. 2021. Advancing mathematics by guid-
                                                             ing human intuition with AI. Nature, 600(7887):70–
7   Limitations                                              74.

In this paper, we conduct experiments on models            Leonardo de Moura, Soonho Kong, Jeremy Avigad,
                                                             Floris Van Doorn, and Jakob von Raumer. 2015. The
with sizes of 2B and 7B. We did not extend our               lean theorem prover (system description). In Auto-
experiments to larger models due to limitations in           mated Deduction-CADE-25: 25th International Con-
computational resources.                                     ference on Automated Deduction, Berlin, Germany,
   Furthermore, due to computational constraints,            August 1-7, 2015, Proceedings 25, pages 378–388.
                                                             Springer.
we did not repeat our training-from-scratch experi-
ments multiple times.                                      P Kingma Diederik. 2014. Adam: A method for stochas-
                                                              tic optimization. (No Title).
                                                           Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey,
References                                                   Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman,
Chenyang An, Zhibo Chen, Qihao Ye, Emily First,              Akhil Mathur, Alan Schelten, Amy Yang, Angela
  Letian Peng, Jiayun Zhang, Zihan Wang, Sorin               Fan, et al. 2024. The llama 3 herd of models. arXiv
  Lerner, and Jingbo Shang. 2024. Learn from failure:        preprint arXiv:2407.21783.
  Fine-tuning llms with trial-and-error data for intu-
                                                           David Steven Dummit and Richard M Foote. 2004. Ab-
  itionistic propositional logic proving. arXiv preprint
                                                             stract algebra, volume 3. Wiley Hoboken.
  arXiv:2404.07382.
                                                           Olga Golovneva, Zeyuan Allen-Zhu, Jason Weston,
Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster,         and Sainbayar Sukhbaatar. 2024. Reverse train-
  Marco Dos Santos, Stephen McAleer, Albert Q Jiang,         ing to nurse the reversal curse. arXiv preprint
  Jia Deng, Stella Biderman, and Sean Welleck. 2023.         arXiv:2403.13799.
  Llemma: An open language model for mathematics.
  arXiv preprint arXiv:2310.10631.                         Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B
                                                              Brown, Benjamin Chess, Rewon Child, Scott Gray,
Gregor Bachmann and Vaishnavh Nagarajan. 2024. The            Alec Radford, Jeffrey Wu, and Dario Amodei. 2020.
  pitfalls of next-token prediction. arXiv preprint           Scaling laws for neural language models. arXiv
  arXiv:2403.06963.                                           preprint arXiv:2001.08361.
Kshitij Bansal, Christian Szegedy, Markus N Rabe,          Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying
  Sarah M Loos, and Viktor Toman. 2019. Learning            Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E.
  to reason in large theories without imitation. arXiv      Gonzalez, Hao Zhang, and Ion Stoica. 2023. Effi-
  preprint arXiv:1905.10501.                                cient memory management for large language model
                                                            serving with pagedattention. In Proceedings of the
Lukas Berglund, Meg Tong, Max Kaufmann, Mikita              ACM SIGOPS 29th Symposium on Operating Systems
  Balesni, Asa Cooper Stickland, Tomasz Korbak, and         Principles.
  Owain Evans. 2023. The reversal curse: Llms trained
  on" a is b" fail to learn" b is a". arXiv preprint       Guillaume Lample, Timothee Lacroix, Marie-Anne
  arXiv:2309.12288.                                          Lachaux, Aurelien Rodriguez, Amaury Hayat,
                                                             Thibaut Lavril, Gabriel Ebner, and Xavier Martinet.
Xinyun Chen, Ryan A Chi, Xuezhi Wang, and Denny              2022. Hypertree proof search for neural theorem
  Zhou. 2024. Premise order matters in reason-               proving. Advances in Neural Information Processing
  ing with large language models. arXiv preprint             Systems, 35:26337–26349.
  arXiv:2402.08939.
                                                           Nayoung Lee, Kartik Sreenivasan, Jason D Lee, Kang-
Vincent Cheng and Zhang Yu. 2023. Analyzing chat-            wook Lee, and Dimitris Papailiopoulos. 2023. Teach-
  gpt’s mathematical deficiencies: Insights and contri-      ing arithmetic to small transformers. arXiv preprint
  butions. In Proceedings of the 35th Conference on          arXiv:2307.03381.
Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paran-        Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le,
  jape, Michele Bevilacqua, Fabio Petroni, and Percy         Ed Chi, Sharan Narang, Aakanksha Chowdhery, and
  Liang. 2024. Lost in the middle: How language mod-         Denny Zhou. 2022. Self-consistency improves chain
  els use long contexts. Transactions of the Association     of thought reasoning in language models. arXiv
  for Computational Linguistics, 12:157–173.                 preprint arXiv:2203.11171.

Tiedong Liu and Bryan Kian Hsiang Low. 2023. Goat:         Sean Welleck, Jiacheng Liu, Ronan Le Bras, Hannaneh
   Fine-tuned llama outperforms gpt-4 on arithmetic          Hajishirzi, Yejin Choi, and Kyunghyun Cho. 2021.
   tasks. arXiv preprint arXiv:2305.14201.                   Naturalproofs: Mathematical theorem proving in nat-
                                                             ural language. arXiv preprint arXiv:2104.01112.
Eran Malach. 2023. Auto-regressive next-token pre-
  dictors are universal learners.  arXiv preprint          Noam Wies, Yoav Levine, and Amnon Shashua. 2022.
  arXiv:2309.06979.                                          Sub-task decomposition enables learning in sequence
                                                             to sequence tasks. arXiv preprint arXiv:2204.02892.
Maciej Mikuła, Szymon Antoniak, Szymon                     Yiran Wu, Feiran Jia, Shaokun Zhang, Hangyu Li,
 Tworkowski, Albert Qiaochu Jiang, Jin Peng                  Erkang Zhu, Yue Wang, Yin Tat Lee, Richard Peng,
 Zhou, Christian Szegedy, Łukasz Kuciński, Piotr            Qingyun Wu, and Chi Wang. 2023. An empirical
 Miłoś, and Yuhuai Wu. 2023. Magnushammer: A                study on challenging math problem solving with gpt-
 transformer-based approach to premise selection.            4. arXiv preprint arXiv:2306.01337.
 arXiv preprint arXiv:2303.04488.
                                                           Kaiyu Yang, Aidan M Swope, Alex Gu, Rahul Chala-
Keiran Paster, Marco Dos Santos, Zhangir Azerbayev,          mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan
  and Jimmy Ba. 2023. Openwebmath: An open                   Prenger, and Anima Anandkumar. 2023a. LeanDojo:
  dataset of high-quality mathematical web text. arXiv       Theorem Proving with Retrieval-Augmented Lan-
  preprint arXiv:2310.06786.                                 guage Models. arXiv preprint arXiv:2306.15626.
Paulo Shakarian, Abhinav Koyyalamudi, Noel Ngu, and        Kaiyu Yang, Aidan M Swope, Alex Gu, Rahul Chala-
  Lakshmivihari Mareedu. 2023. An independent eval-          mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan
  uation of chatgpt on mathematical word problems            Prenger, and Anima Anandkumar. 2023b. Leandojo:
  (mwp). arXiv preprint arXiv:2302.13814.                    Theorem proving with retrieval-augmented language
                                                             models. arXiv preprint arXiv:2306.15626.
Hui Su, Zhi Tian, Xiaoyu Shen, and Xunliang Cai. 2024.
  Unraveling the mystery of scaling laws: Part i. arXiv    Aojun Zhou, Ke Wang, Zimu Lu, Weikang Shi, Sichun
  preprint arXiv:2403.06563.                                 Luo, Zipeng Qin, Shaoqing Lu, Anya Jia, Linqi Song,
                                                             Mingjie Zhan, et al. 2023a. Solving challenging
Usman Syed, Ethan Light, Xingang Guo, Huan Zhang,            math word problems using gpt-4 code interpreter
  Lianhui Qin, Yanfeng Ouyang, and Bin Hu. 2024.             with code-based self-verification. arXiv preprint
  Benchmarking the capabilities of large language mod-       arXiv:2308.07921.
  els in transportation system engineering: Accuracy,
  consistency, and reasoning behaviors. arXiv preprint     Hattie Zhou, Arwen Bradley, Etai Littwin, Noam Razin,
  arXiv:2408.08302.                                          Omid Saremi, Josh Susskind, Samy Bengio, and Pree-
                                                             tum Nakkiran. 2023b. What algorithms can trans-
Gemma Team, Thomas Mesnard, Cassidy Hardin,                  formers learn? a study in length generalization. arXiv
  Robert Dadashi, Surya Bhupatiraju, Shreya Pathak,          preprint arXiv:2310.16028.
  Laurent Sifre, Morgane Rivière, Mihir Sanjay Kale,       Yongchao Zhou, Uri Alon, Xinyun Chen, Xuezhi Wang,
  Juliette Love, et al. 2024. Gemma: Open models             Rishabh Agarwal, and Denny Zhou. 2024. Trans-
  based on gemini research and technology. arXiv             formers can achieve length generalization but not
  preprint arXiv:2403.08295.                                 robustly. arXiv preprint arXiv:2402.09371.
Hugo Touvron, Louis Martin, Kevin Stone, Peter Al-
  bert, Amjad Almahairi, Yasmine Babaei, Nikolay           A     Appendix
  Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti
  Bhosale, et al. 2023. Llama 2: Open founda-
                                                           A.1    Limitation
  tion and fine-tuned chat models. arXiv preprint          In this paper, we conduct experiments on models
  arXiv:2307.09288.                                        with 2B and 7B parameters. Due to computational
Haiming Wang, Ye Yuan, Zhengying Liu, Jianhao Shen,        constraints, we did not extend our experiments to
  Yichun Yin, Jing Xiong, Enze Xie, Han Shi, Yujun         larger models or incorporate additional ordering
  Li, Lin Li, et al. 2023. Dt-solver: Automated theo-      variations. As discussed in Section 5, we didn’t
  rem proving with dynamic-tree sampling guided by         train and evaluate models on graduate or research-
  proof-level value function. In Proceedings of the
  61st Annual Meeting of the Association for Compu-
                                                           level math-proving datasets, since there is no di-
  tational Linguistics (Volume 1: Long Papers), pages      rect way to check the correctness of the model-
  12632–12646.                                             generated proofs.
A.2 Delayed Insight Issue: A common type of               up with the idea of applying Proposition 1.4 given
    order issue that occurs frequently in                 the theorem.
    graduate-level math textbooks
To illustrate DII, we compile a list of 9 cases from
the first two chapters of a classic graduate-level        A.2.3   Folland, Chapter 1, Proposition 1.16
textbook: Real Analysis, Modern Techniques and
Their Applications authored by Gerald B. Folland             Example 3
(?). We find 17.3 percent of the theorems with non-
trival proofs in the first two chapters of the textbook      Proposition. If F : R 7→ R is any increas-
suffer from Delayed Insight Issue as defined in the          ing, right continuous function, there is a
main text.                                                   unique Borel measure µF on R such that
                                                             µF ((a, b]) = F (b) − F (a) for all a, b. If G
A.2.1   Folland, Chapter 1, Proposition 1.3                  is another such function, we have µF = µG
   Example 1                                                 iff F − G is a constant.

   Proposition.  If A is countable, then                     Proof: Each F induces a premeasure on A
                                                             by Proposition 1.15. It is clear that F and
   N
    Qα∈A Mα is the σ-algebra generated by
   { α∈A Eα : Eα ∈ Mα }                                      G induces the same premeasure iff F − G
                                                             is constant, and that these premeasures are
   Proof: If Eα ∈ Mα , then πα−1 (Eα ) =
   Q                                                         σ-finite (since R = ∪∞  −∞ (j, j + 1]). The
     β∈A Eβ where Eβ = Q      Xβ for β ̸=                    first two assertions therefore follow from
   α; on the other hand,        α∈A Eα    =                  Theorem 1.14.
   ∩α∈A πα−1 (Eα ). The result therefore fol-
   lows from Lemma 1.1.
                                                            Here, Theorem 1.14 serves as the major lemma,
  Here, Lemma 1.1 serves as the major lemma,              and the previous steps set up the stage for applying
and the previous steps set up the stage for applying      Theorem 1.14. Note that it is natural to first come
Proposition 1.4. Note that it is natural to first come    up with the idea of applying Theorem 1.14 given
up with the idea of applying Lemma 1.1 given the          the theorem.
theorem.

A.2.2   Folland, Chapter 1, Proposition 1.5
                                                          A.2.4   Folland, Chapter 2, Proposition 2.6
   Example 2

   Proposition. Let Q    X1 , .., Xn be metric               Example 4
   spaces and let X = n1 XjN     , equipped with             Proposition. If f, g : X 7→ C are M -
   the product metric. Then n1 B       Xj ⊂ BX .             measurable, then so are f + g and f g
   If the Xj ’s are separable, then n1 BXj =
                                     N
   BX                                                        Proof: Define F : X 7→ C × C, ϕ :
                                                             C × C 7→ C by F (x) = (f (x), g(x)),
   Proof: ...... Moreover, the set of the set of             ϕ(z, w) = z N
                                                                         + w, ψ(z, w) = zw. Since
   points in X whose jth coordinate is in Cj for             BC×C = BC BC by Proposition 1.5, F
   all j is a countable dense subset of X, and               is (M, BC×C )-measurable by Proposition
   the balls of radius r in X are merely prod-               2.4.
   ucts of the balls of radius r in the Xj ’s. It
   follows that BXj Qis generated by Ej and BX
   is generatedN  by n1 Ej : Ej ∈ Ej . There-                Here, Proposition 2.4 serves as the major lemma,
   fore BX = n1 BXj by Proposition 1.4                    and the previous steps set up the stage for applying
                                                          Theorem 1.14. Note that it is natural to first come
  Here, Proposition 1.4 serves as the major lemma,        up with the idea of applying Proposition 2.4 given
and the previous steps set up the stage for applying      the theorem, and then make the constructions as in
Proposition 1.4. Note that it is natural to first come    the early part of the proof.
A.2.5    Folland, Chapter 2, Corollary 2.17                A.2.7   Folland, Chapter 2, Theorem 2.25
                                                              Example 7

    Example 5
                                                              Theorem. Suppose that
                                                                    1               ∞
                                                                                      R {fj } is a sequence
                                                              in L such that Σ1 |fj | < ∞. Then
    Corollary. If {fn } ⊂ L+ , f ∈ L+ , and                   Σ∞1 fRj converges a.e. R to a function in L ,
                                                                                                            1
                                                                        ∞
                                                              and Σ1 fj = Σ1 fj  ∞
    fRn (x) increases
                R     to f (x) for a.e x, then
       f = lim fn                                                                              R ∞
                                                              Proof:    By   Theorem    2.15,     Σ1 |fj | =
                                                                ∞
                                                                   R
   Proof: If fn (x) increases to f (x) for x ∈ E              Σ1 |fj | < ∞, so that function g =
   where µ(E c ) = 0, then f − f χE = 0 a.e.                  Σ∞               1
                                                                1 |fj | is in L . In particular, by Propo-
   and fn − fn χE = 0 a.e., so                                sition 2.20, Σ∞ 1 |fj (x)| is finite for a.e. x,
                                R by theR mono-               and for each such x the series Σ∞
   toneRconvergence theorem,      f  =    f χE =                                                 1 fj (x) con-
   lim fn χE = lim fn
                       R                                      verges. Moreover, |Σn1 fj | ≤ g for all n, so
                                                              we can apply the dominated convergence
                                                              theorem R to∞the sequenceR of partial sums to
                                                              obtain Σ1 fj = Σ1 fj   ∞


   For this problem, the first instinct after looking at      For this problem, the first instinct after looking
the corollary should be to apply the monotone con-         at the lemma should be to apply the dominated con-
vergence theorem. The earlier steps explicitly state       vergence theorem. The earlier steps explicitly state
how the monotone convergence theorem should be             how to make sure the conditions of the dominated
applied to the given corollary.                            convergence theorem are satisfied by the statement.
                                                           A.2.8   Folland, Chapter 2, Theorem 2.27
                                                              Example 8

                                                              Theorem. Suppose that f : X × [a, b] 7→
A.2.6    Folland, Chapter 2, Fatou’s Lemma                    C(−∞ < a < b < ∞) and that f (·, t) :
         2.18                                                 X 7→ C is Rintegrable for each t ∈ [a, b].
                                                              Let F (t) = X f (x, t)dµ(x). Suppose that
                                                              ∂f /∂t exists and there is a g ∈ L1 (µ)
    Example 6                                                 such that |(∂f /∂t)(x, t)| ≤ g(x) for all
                                                              x,                                 ′
                                                              R t. Then F is differentiable and F (x) =
    Fatou’s Lemma.  If {fn } is any sequence in                 (∂f /∂t)(x, t)dµ(x).
    L+ , then (lim inf fn ) ≤ lim inf fn
             R                        R
                                                              Proof: Observe that ∂f /∂t(x, t0 ) =
    Proof: For each k ≥ 1 we have                             lim hn (x) where hn (x) = f (x,tntn)−f
                                                                                                   −t0
                                                                                                      (x,t0 )
                                                                                                              ,
    R n≥k fn ≤ fj Rfor j ≥ k, hence
    inf                                                       {tn } again being any sequence converg-
           R fn ≤
      inf n≥k            fj for Rj ≥ k,                       ing to t0 . It follows that ∂f /∂t is mea-
    hence inf n≥k fn ≤ inf j≥k fj . Now                       surable, and by the mean value theorem,
    let k 7→ ∞ and apply    R       monotone                  |hn (x)| ≤ supt∈[a,b] |∂f /∂t(x, t)| ≤ g(x),
    convergence
              R theorem:      (lim inf
                                    R fn ) =                  so the dominated convergence theorem
    limk7→∞ (inf n≥k fn ) ≤ lim inf fn                        can be invoked again to give F ′ (t0 ) =
                                                              lim F (tntn)−F (t0 )      R
                                                                          −t0      = lim hn (x)dµ(x) =
                                                              R
                                                                ∂f /∂t(x, t)dµ(x)

   For this problem, the first instinct after looking         For this problem, the first instinct after looking
at the lemma should be to apply the monotone               at the lemma should be to apply the dominated con-
convergence theorem. The earlier steps explicitly          vergence theorem. The earlier steps explicitly state
state how to transform the problem to a state so that      how to make sure the conditions of the dominated
one can apply the monotone convergence theorem.            convergence theorem are satisfied by the statement.
A.2.9    Folland, Chapter 2, Theorem 2.47
   Example 9

   Theorem. Suppose that Ω is an open set
   in Rn and G : Ω 7→ Rn is a C 1 dif-
   feomorphism. If f is a Lebesgue mea-
   surable function on G(Ω), then f ◦ G is
   Lebesgue measurable on RΩ. If f ≥ 0 or
   f ∈ L1 (G(Ω), m), then G(Ω) f (x)dx =
   R
    Ω f ◦ G(x)| det Dx G|dx.

   Proof: ...A lot of estimation....By the
   preceding estimate and the dominated
   convergence theorem, m(G(E))              ≤
   m(G(∩   ∞ U ))     =    lim m(G(U      )) ≤
       R 1      j             R         j
   lim Uj | det Dx G|dx = E | det Dx G|dx.
   Finally, if E is any Borel subset...

  For this problem, without first having a clear
goal as expressed in the previous equation, one will
be completely confused for why we need to do all
the estimation at the beginning.

A.3     Prompting configuration for testing
See Figure 5.

A.4     Data Examples in training
We show here examples of our data for the multi-
plication task and the intuitionistic propositional
logic theorem-proving task. See Figure 6, 7, 8, 9.

A.5     Fine-grained result regarding data order
In Figure 10 we present more fine-grained results
on the order effect in the multiplication task.
                    Tell me what is 2198*1589 and prove           Tell me what is 2198*1589 and prove        Tell me what is 2198*1589 and prove
                    it.                                           it.                                        it.
                    Step 1                                        Step 8                                     3492622
                    Step 2                                        Step 7                                     final answer printed
                    ……                                            ……                                         Step 8
                    Step 8                                        Step 1                                     Step 7
                    3492622                                       3492622                                    ……
                    final answer printed                          final answer printed                       Step 1
                                                     (a)                                          (b)                                                          (c)


                                                                                                             Statement:
                    Tell me what is 2198*1589 and prove           Tell me what is 2198*1589 and prove        p1 p2 p3 p4 p5 : Prop ⊢ p3 ∧ ((((((p4 ∨ p3 ∧ ……
                    it.                                           it.                                        Proof:
                    Step 1                                        Step 8                                     Tactic
                                                                                                             apply Or.inr
                    Step 2                                        Step 7                                     State
                    ……                                            ……                                         case h p1 p2 p3 p4 p5 : Prop ⊢ True ∨ True ……
                    Step 8                                        Step 1                                     Tactic
                    3492622                                       3492622                                    ……
                                                                                                             State
                    final answer printed                          final answer printed
                                                     (d)                                          (e)        No goal
                                                                                                             Proof is complete    (e)                          (f)


Figure 5: Prompt configuration for testing the models on the multiplication task and the theorem-proving task: texts
colored in red are prompt. Texts colored in black are the expected output from the model.




 Tell me what is 2198*1589 and prove it.
 Obviously, we can decompose the numbers in the following ways:
 (2*1000+1*100+9*10+8*1)*(1*1000+5*100+8*10+9*1)
 Next, by the distributivity axiom of integers, we have:
 2*1000*1*1000+2*1000*5*100+2*1000*8*10+2*1000*9*1+1*100*1*1000+1*100*5*100+
 1*100*8*10+1*100*9*1+9*10*1*1000+9*10*5*100+9*10*8*10+9*10*9*1+8*1*1*1000+8*
 1*5*100+8*1*8*10+8*1*9*1
 Then, we apply commutativity axiom of integers to get
 2*1*1000*1000+2*5*1000*100+2*8*1000*10+2*9*1000*1+1*1*100*1000+1*5*100*100+
 1*8*100*10+1*9*100*1+9*1*10*1000+9*5*10*100+9*8*10*10+9*9*10*1+8*1*1*1000+8*
 5*1*100+8*8*1*10+8*9*1*1
 After that, multiply the ﬁrst two terms
 2*1000000+10*100000+16*10000+18*1000+1*100000+5*10000+8*1000+9*100+9*10000
 +45*1000+72*100+81*10+8*1000+40*100+64*10+72*1
 Now, we make the multiplications
 2000000+1000000+160000+18000+100000+50000+8000+900+90000+45000+7200+810+8
 000+4000+640+72
 We make additions from here
 3000000+178000+150000+8900+135000+8010+12000+712
                                                                                         Tell me what is 2198*1589 and prove it.
 3178000+158900+143010+12712
                                                                                         3492622
 3336900+155722
                                                                                         ﬁnal answer printed
 3492622
 ﬁnal answer printed                                                                     We know the following
                                                                                         3336900+155722
                                                                                         This is exactly because we can make the addition
                                                                                         3178000+158900+143010+12712
Figure 6: Example of the SEQ data for multiplication                                     This comes from using addition
                                                                                         3000000+178000+150000+8900+135000+8010+12000+712
                                                                                         This is true because we can make the addition
                                                                                         2000000+1000000+160000+18000+100000+50000+8000+900+90000+45000+7200+810+8
                                                                                         000+4000+640+72
                                                                                         This comes from making the multiplications
                                                                                         2*1000000+10*100000+16*10000+18*1000+1*100000+5*10000+8*1000+9*100+9*10000
                                                                                         +45*1000+72*100+81*10+8*1000+40*100+64*10+72*1
                                                                                         This is true because of the commutativity axiom of integers
Tell me what is 2198*1589 and prove it.                                                  2*1*1000*1000+2*5*1000*100+2*8*1000*10+2*9*1000*1+1*1*100*1000+1*5*100*100+
                                                                                         1*8*100*10+1*9*100*1+9*1*10*1000+9*5*10*100+9*8*10*10+9*9*10*1+8*1*1*1000+8*
We know the following
                                                                                         5*1*100+8*8*1*10+8*9*1*1
3336900+155722
                                                                                         This is true because of the distributivity axiom of integers
This is exactly because we can make the addition
                                                                                         2*1000*1*1000+2*1000*5*100+2*1000*8*10+2*1000*9*1+1*100*1*1000+1*100*5*100+
3178000+158900+143010+12712
                                                                                         1*100*8*10+1*100*9*1+9*10*1*1000+9*10*5*100+9*10*8*10+9*10*9*1+8*1*1*1000+8*
This comes from using addition
                                                                                         1*5*100+8*1*8*10+8*1*9*1
3000000+178000+150000+8900+135000+8010+12000+712
                                                                                         This is true since we can decompose the numbers in the following way
This is true because we can make the addition
                                                                                         (2*1000+1*100+9*10+8*1)*(1*1000+5*100+8*10+9*1)
2000000+1000000+160000+18000+100000+50000+8000+900+90000+45000+7200+810+8
000+4000+640+72
This comes from making the multiplications
2*1000000+10*100000+16*10000+18*1000+1*100000+5*10000+8*1000+9*100+9*10000              Figure 8: Example of the SER data for multiplication
+45*1000+72*100+81*10+8*1000+40*100+64*10+72*1
This is true because of the commutativity axiom of integers
2*1*1000*1000+2*5*1000*100+2*8*1000*10+2*9*1000*1+1*1*100*1000+1*5*100*100+
1*8*100*10+1*9*100*1+9*1*10*1000+9*5*10*100+9*8*10*10+9*9*10*1+8*1*1*1000+8*
5*1*100+8*8*1*10+8*9*1*1
This is true because of the distributivity axiom of integers
2*1000*1*1000+2*1000*5*100+2*1000*8*10+2*1000*9*1+1*100*1*1000+1*100*5*100+
1*100*8*10+1*100*9*1+9*10*1*1000+9*10*5*100+9*10*8*10+9*10*9*1+8*1*1*1000+8*
1*5*100+8*1*8*10+8*1*9*1
This is true since we can decompose the numbers in the following way
(2*1000+1*100+9*10+8*1)*(1*1000+5*100+8*10+9*1)
Hence we have the answer
3492622
ﬁnal answer printed



Figure 7: Example of the PSER data for multiplication
 state_0:
 p1 p2 p3 p4 p5 : Prop                                                                                    state_0:
 ⊢ p5 → False → ((p5 ∨ ((p1 ∨ p5) ∧ True) ∧ (p5 ∨ (True → (p4 → False) ∧ (p4 ∨ True)))                    p1 p2 p3 p4 p5 : Prop
 ∨ p4 → p5) ∧ p5 ∨ p5) ∧ False                                                                            ⊢ p5 → False → ((p5 ∨ ((p1 ∨ p5) ∧ True) ∧ (p5 ∨ (True → (p4 → False) ∧ (p4 ∨ True)))
 tactic                                                                                                   ∨ p4 → p5) ∧ p5 ∨ p5) ∧ False
 intro h1                                                                                                 tactic
 state                                                                                                    apply False.elim h2
 p1 p2 p3 p4 p5 : Prop                                                                                    state
 h1 : p5                                                                                                  no goals
 ⊢ False → ((p5 ∨ ((p1 ∨ p5) ∧ True) ∧ (p5 ∨ (True → (p4 → False) ∧ (p4 ∨ True))) ∨ p4                    proof is complete
                                                                                                          tactic
 → p5) ∧ p5 ∨ p5) ∧ False
                                                                                                          apply False.elim h2
 tactic
                                                                                                          state
 intro h2
                                                                                                          case right
 state                                                                                                    p1 p2 p3 p4 p5 : Prop
 p1 p2 p3 p4 p5 : Prop                                                                                    h1 : p5
 h1 : p5                                                                                                  h2 : False
 h2 : False                                                                                               ⊢ False
 ⊢ ((p5 ∨ ((p1 ∨ p5) ∧ True) ∧ (p5 ∨ (True → (p4 → False) ∧ (p4 ∨ True))) ∨ p4 → p5) ∧                    tactic
 p5 ∨ p5) ∧ False                                                                                         apply And.intro
 tactic                                                                                                   state
 apply And.intro                                                                                          case left
 state                                                                                                    p1 p2 p3 p4 p5 : Prop
 case left                                                                                                h1 : p5
 p1 p2 p3 p4 p5 : Prop                                                                                    h2 : False
 h1 : p5                                                                                                  ⊢ (p5 ∨ ((p1 ∨ p5) ∧ True) ∧ (p5 ∨ (True → (p4 → False) ∧ (p4 ∨ True))) ∨ p4 → p5) ∧
 h2 : False                                                                                               p5 ∨ p5
 ⊢ (p5 ∨ ((p1 ∨ p5) ∧ True) ∧ (p5 ∨ (True → (p4 → False) ∧ (p4 ∨ True))) ∨ p4 → p5) ∧                     tactic
 p5 ∨ p5                                                                                                  intro h2
 tactic                                                                                                   state
 apply False.elim h2                                                                                      p1 p2 p3 p4 p5 : Prop
 state                                                                                                    h1 : p5
 case right                                                                                               h2 : False
 p1 p2 p3 p4 p5 : Prop                                                                                    ⊢ ((p5 ∨ ((p1 ∨ p5) ∧ True) ∧ (p5 ∨ (True → (p4 → False) ∧ (p4 ∨ True))) ∨ p4 → p5) ∧
 h1 : p5                                                                                                  p5 ∨ p5) ∧ False
 h2 : False                                                                                               tactic
 ⊢ False                                                                                                  intro h1
 tactic                                                                                                   state
 apply False.elim h2                                                                                      p1 p2 p3 p4 p5 : Prop
 state                                                                                                    h1 : p5
 no goals                                                                                                 ⊢ False → ((p5 ∨ ((p1 ∨ p5) ∧ True) ∧ (p5 ∨ (True → (p4 → False) ∧ (p4 ∨ True))) ∨ p4
 proof is complete                                                                                        → p5) ∧ p5 ∨ p5) ∧ False



(a) Example of the SEQ data for theorem-proving                                                           (b) Example of the SER data for theorem-proving

                     Figure 9: Examples of data for the intuitionistic propositional logic theorem-proving task




                                                               0.6           SEQ
                                                                             PSER-then-SEQ
                                                    Success rate




                                                               0.4

                                                               0.2

                                                               0.0
                                                                  5000 10000 15000 20000 25000 30000
                                                                                             Checkpoint
                                                         (a) Gemma first fine-tuned on PSER then fine-tuned on SEQ

                                                               0.8           SEQ
                                                                             PSER

                                                               0.6
                                                    Success rate




                                                               0.4
                                                               0.2
                                                               0.0
                                                                          10000 20000 30000 40000 50000
                                                                                             Checkpoint
                                                            (b) Pre-trained Llama-2-7b-hf, problems and steps masked

                              Figure 10: More fine-grained result on the order effect in the multiplication task
