                                                     Probabilistic Guarantees for Reducing Contextual
                                                                            Hallucinations in LLMs
                                                                 Nils Rautenberg∗                          Sven Schippkus 
                                                          Deutsche Aktuarvereinigung e.V.                 University of Hamburg

                                                                                       January 5, 2026
arXiv:2601.00641v1 [cs.CL] 2 Jan 2026




                                            Key Points
                                             •   Independent prompt repetition makes it overwhelmingly likely that a correct answer appears.
                                             •   An LLM-as-a-judge identifies correct answers; majority vote improves reliability when needed.
                                             •   Together, these give explicit probabilistic guarantees with exponentially decreasing error rates.


                                                                                            Abstract

                                                    Large language models (LLMs) frequently produce contextual hallucinations, where gen-
                                                 erated content contradicts or ignores information explicitly stated in the prompt. Such errors
                                                 are particularly problematic in deterministic automation workflows, where inputs are fixed
                                                 and correctness is unambiguous. We introduce a simple and model-agnostic framework that
                                                 provides explicit probabilistic guarantees for reducing hallucinations in this setting.
                                                    We formalize the notion of a specific task, defined by a fixed input and a deterministic
                                                 correctness criterion, and show that issuing the same prompt in independent context windows
                                                 yields an exponential reduction in the probability that all model outputs are incorrect. To
                                                 identify a correct answer among repeated runs, we incorporate an LLM-as-a-judge and prove
                                                 that the probability that the judged pipeline fails decays at a rate determined by the judge’s
                                                 true- and false-positive probabilities. When the judge is imperfect, we strengthen it through
                                                 majority vote over independent judge calls, obtaining ensemble-level error rates that decrease
                                                 exponentially in the number of votes. This yields an explicit bound on the probability that
                                                 the pipeline selects a hallucinated answer.
                                                    Experiments on controlled extraction tasks with synthetic noisy judges match these pre-
                                                 dictions exactly: pipeline failure decreases exponentially with the number of repetitions, and
                                                 hallucination-selection decreases exponentially with the number of judges in the ensemble.
                                                 Together, these results provide a lightweight, modular, and theoretically grounded method
                                                 for driving hallucination probabilities arbitrarily low in fixed-input LLM workflows-without
                                                 modifying model weights, decoding strategies, or prompt engineering.



                                        1        Introduction
                                        Large language models (LLMs) are increasingly capable of solving complex tasks, following instruc-
                                        tions, and synthesizing information across long chains of reasoning. Yet even the most advanced
                                        models still fail in a surprisingly human way: they occasionally assert things that are not true, not
                                            ∗ contact: nils.rautenberg@rub.de




                                                                                                 1
Figure 1: The repetition-judge pipeline gives probabilistic guarantees for reducing contextual hal-
lucinations. Left: For a given specific task, the likelihood that all answers are hallucinated is
reduced by repeating the task N times and judging the output Xn of each for correctness. The
pipeline fails (”all answers are judged as incorrect”) exponentially decreasing with N . Right:
From the judged-correct answers, a true correct answer can be found at guaranteed rates. If the
judge is perfect (q ++ = 1, q −+ = 0), any Xn with Yn = 1 is a correct answer. If the judge is
noisy but better than random (q −+ < 0.5), an ensemble judge selects a hallucination exponentially
decreasing with the number of judges K.


implied, or directly contradicted by the information they were given. These hallucinations pose a
challenge for automated pipelines that require deterministic correctness.
   A growing body of work has shown that hallucinations take many forms rather than one.
Comprehensive reviews (Huang et al. 2025; Zhang et al. 2025) map out diverse error types—from
contradictions with world knowledge to logical slips or instruction confusion—revealing that hal-
lucination is a structural property of present-day models rather than a rare glitch (Kalai et al.
2025). Summarization studies further demonstrate that even conditioned generation systems often
produce unsupported claims (Fabbri et al. 2021; Kryscinski et al. 2020; Maynez et al. 2020), and
retrieval-augmented models continue to introduce content not present in the retrieved passages
(Adlakha et al. 2024). Contextual hallucinations, where the model contradicts or ignores informa-
tion that is explicitly provided in the prompt, have proven particularly difficult to eliminate. Prior
work attributes these failures to long-context degradation (Chang et al. 2024; Kim et al. 2024; Liu
et al. 2025), competition between contextual and parametric knowledge (Longpre et al. 2021), and
the inherent difficulty of reliable evidence tracking in autoregressive generation.
   Ongoing efforts have sought to detect and mitigate hallucinations. Techniques such as FactCC
(Kryscinski et al. 2020), AlignScore (Zha et al. 2023), REFChecker (Hu et al. 2024), and Veri-
FastScore (Rajendhran et al. 2025) attempt to identify unsupported content post-hoc, while con-
trastive decoding strategies (Chang et al. 2023; Shi et al. 2023) and faithfulness-inspired heuristics
(Wan et al. 2023) aim to reduce hallucinations during inference. Multi-agent refinement and LLM-
as-a-judge systems (Cohen et al. 2023; Du et al. 2023; Jain et al. 2023; Liu et al. 2023; Luo et al.
2023; Madaan et al. 2023; Shinn et al. 2023; Wang et al. 2024) combine several model calls to im-
prove reliability, but empirical studies show that judges can themselves be inconsistent or biased
in challenging cases (Kim et al. 2024; Laban et al. 2023). Despite substantial progress, existing


                                                  2
mitigation strategies do not provide explicit quantitative guarantees on the likelihood of residual
hallucinations.
    In this paper, we focus on a restricted but practically important setting: a class of tasks that
we call specific tasks. A specific task is one where: (i) the input is fixed, (ii) the prompt is issued
only once per run, (iii) and correctness can be evaluated by a deterministic criterion. Typical
examples include slot extraction, reference lookup, formatting tasks, or locating a particular word
or number in a known text. Such tasks are common in automated workflows and provide a clean
setting where correctness is unambiguous. In this setting, reliability decomposes naturally into
two independent questions: (i) how likely is that at least one correct answer appears among the
model outputs, and (ii) how reliably a judge can identify such an answer when it exists. These
two stages-existence and identification-can be improved separately through repetition and judged
selection.
    Two simple observations motivate our framework:

    1. Repetition amplifies correctness. Even if a model sometimes answers incorrectly, running
      the same task several times independently, for example by issuing each call in a fresh context
      window, makes it very likely that at least one of the answers will be correct. This is a direct
      probabilistic consequence of independence, and we formalize it as the Repetition Lemma.

    2. Identification requires a judge. Repetition alone does not tell us which of the responses
      is correct. Selecting an answer uniformly at random from the repeated runs yields the same
      correctness probability as a single run. To select a correct answer among all that appear,
      we need a secondary mechanism to filter out hallucinations: an LLM-as-a-judge. Even if the
      judge is imperfect, its reliability can itself be improved through repetition.

    Figure 1 illustrates the repetition–judge pipeline based on these core concepts. Repetition
makes it overwhelmingly likely that at least one correct answer appears among the model outputs,
and an appropriate judge–strengthened via majority vote if necessary—identifies such an answer
with task-dependent true- and false-positive rates. Taken together, these components form a
lightweight, model-agnostic pipeline for achieving arbitrarily low error rates on fixed-input tasks
without modifying model weights or relying on complex decoding schemes.
    The remainder of the paper develops these ideas in a simple formal setting. Section 2 intro-
duces specific tasks and shows how independent repetitions sharply reduce the chance that all
responses are wrong. Section 3 then explains how a judge can be used to identify a correct answer
once repetition makes its existence likely, and how ensemble judging provides explicit bounds on
hallucination-selection probability even for imperfect judges. Section 4 presents controlled experi-
ments validating both effects, and Section 5 concludes.


2     Existence of correct answers
At the heart of our framework lies a simple but powerful modelling assumption: independent LLM
calls made in fresh context windows behave as independent samples from a fixed output distri-
bution. This assumption is the mathematical basis for all existence guarantees in this paper. It
reflects the practical reality that each model call carries its own sampling randomness and that
starting from an empty, uncontaminated context eliminates cross-run interference. Under this in-
dependence assumption, repeated executions of the same prompt provide statistically independent
“attempts” at solving a fixed task.


                                                  3
     We now formalize the setting in which our analysis applies. At this stage, we focus solely on the
probability that a correct answer appears among repeated calls to the model. The identification
step (”find a correct answer”) is developed separately in Section 3, where we incorporate a judge
and, when needed, majority-vote aggregation.
     A specific task is one where the input is fixed, the prompt is issued only once per run, and
correctness can be evaluated by a deterministic rule. In this setting, each call to the LLM behaves
as a random draw from a fixed distribution. Running the same task independently multiple times
therefore produces a sequence of independent and identically distributed random variables. This
structure is all we need to derive explicit probabilistic guarantees on the likelihood that at least
one correct answer appears among repeated executions.


2.1     Specific tasks
Let Z denote the set of possible LLM inputs and outputs. A specific task consists of:

     • a fixed input A ∈ Z,

     • a fixed prompt function B : Z → Z producing the query to the LLM,

     • a deterministic correctness function C : Z → Z,

     • and a correctness criterion c0 ∈ Z.

     One execution of the task consists of issuing the prompt B(A) to the LLM in a fresh context
window and obtaining an output X ∈ Z. We say the model answers correctly if C(X) = c0 , and
we call the response a hallucination otherwise.
     Crucially, issuing each call in a fresh context window makes the outputs X1 , X2 , . . . behave as
independent and identically distributed random variables. This is the only, yet powerful, structural
property we assume about the model. Because the input, prompt, and correctness criterion are
fixed, the per-run success probability

                                            p = P(C(Xn ) = c0 ),

is a stable property of the task. A task is solvable if p > 0.


2.2     Repetition Lemma
We are interested in the probability that N independent model calls all fail to produce a correct
answer. Since each call succeeds with probability p and fails with probability (1 − p), independence
gives
                              P(C(X1 ) ̸= c0 , . . . , C(XN ) ̸= c0 ) = (1 − p)N .

     This yields the following simple but powerful observation.

Theorem 2.1 (Repetition Lemma). For any solvable specific task with per-run correctness prob-
ability p > 0, the probability that N independent executions all produce hallucinated responses
is
                                                  (1 − p)N .

This probability decreases exponentially with increasing N .


                                                       4
Proof. Since the events {C(Xn ) ̸= c0 } are independent and each has probability (1 − p), the joint
failure probability is exactly (1 − p)N .

    Intuitively, if the model occasionally produces the correct answer, then repeatedly running the
same task makes it overwhelmingly likely that a correct answer appears somewhere among the
responses. The lemma provides an explicit quantitative guarantee: a small amount of repetition
is sufficient to make the event “every answer is a hallucination” extremely unlikely. Repetition
therefore provides a guarantee on the existence of a correct answer among the repeated outputs.
The problem of identifying such an answer is addressed next.


3     Identification of correct answers
Repetition ensures that a correct answer is likely to appear among the repeated outputs. However,
repetition alone does not determine which of the responses is correct. Selecting a response uniformly
at random from the repeated runs yields the same correctness probability as a single model call.
To identify a correct answer among the repeated outputs, we use an LLM-as-a-judge, strengthened
through majority vote if necessary. This section introduces the judge, derives the probability that
the pipeline fails to identify any correct answer, and provides an explicit bound on the probability
that the selected answer is a hallucination.


3.1    Judging model
For each model output Xn , we issue a separate yes/no query to a judge asking whether Xn is
correct with respect to the fixed criterion C, that is C(Xn ) = c0 . Each query is sent in a fresh
context window so that judge evaluations across different n are independent. We write the judge
response as a Bernoulli random variable

                 Yn ∈ {0, 1},    Yn = 1 meaning “the judge asserts Xn is correct.”

To characterise the judge, we define is true-positive and false-positive rates

                 q ++ = P(Yn = 1 | C(Xn ) = c0 ),       q −+ = P(Yn = 1 | C(Xn ) ̸= c0 ).

These quantities depend on the task and judge prompt but are fixed across repetitions. A perfect
judge satisfies q ++ = 1 and q −+ = 0. We emphasise that judge evaluation itself constitutes a
specific task with fixed correctness criterion, and thus inherits the same independence assumptions
as the model calls.


3.2    Reliability of judged existence
The judged-selection pipeline fails if, and only if, no model output is judged correct. For any given
model call, two events must occur to obtain a correct-and-judged-correct output: (i) the model
produces a correct answer, which happens with probability p, and (ii) the judge accepts it, which
happens with probability q ++ . Thus the per-trial probability of producing a correct-and-judged-
correct answer is pq ++ .
    Similarly, an incorrect answer is nevertheless judged correct with probability (1 − p)q −+ , pro-
ducing a false-positive candidate. Although such false positives do not help the pipeline identify a


                                                    5
correct answer, they influence the behaviour of the judged-correct set and therefore appear in the
full derivation of pipeline failure.
   Putting these observations together yields the following guarantee.

Theorem 3.1 (Reliability of the repetition-judge pipeline). For a specific task with per-trial cor-
rectness probability p > 0 and judge rates q ++ > 0 , q −+ ≥ 0, the probability that the pipeline fails,
i.e., that no judged-correct answer appears among N repetitions, is
                                                                 N
                                       1 − (pq ++ + (1 − p)q −+ ) .

Proof. For any fixed n, the probability that the output is judged correct (whether correctly or
incorrectly) is pq ++ + (1 − p)q −+ . Independence across repetitions implies that the probability
that no judged-correct answer appears across all N trials is the stated expression. This event
contains, in particular, the event that no correct-and-judged-correct answer appears.

   Let
                                            S = {n : Yn = 1}

denote the set of responses that the single judge asserts as correct. Theorem 3.1 characterizes the
probability that S = ∅, i.e., that the pipeline reports failure. From now on, we condition on the
natural event S ̸= ∅, meaning that at least one model output was judged correct by the pipeline.


3.3      Identification via ensemble judging
Given the repetition-judge pipeline succeeds (S ̸= ∅), we can define bounds on how likely we find
a correct answer in S, depending on the judge quality. In the following, we investigate the case
where the judge is better than random (q ++ > 12 , q −+ < 21 ).
   For simple assessment tasks, e.g., when c0 is a single word and we ask the judge “Is Xn exactly
c0 ?”, an LLM-as-a-judge is often perfect in practice, meaning q ++ = 1 and q −+ = 0. In this case,
the pipeline failure rate (Theorem 3.1) simplifies to the Repetition Lemma (Theorem 2.1) and
when the pipeline succeeds (S ̸= ∅), selecting any answer guarantees a correct answer.
   However, if q −+ is non-zero, a hallucinated answer may appear in the judged set S and could
be chosen. If the judge is better than random (q −+ < 21 ), we can use an ensemble of judges and
issue a majority vote among them to reduce the probability of selecting a hallucination.
   For each Xn , let Yn1 , ... , YnK be independent Bernoulli variables with

                P(Ynk = 1 | C(Xn ) = c0 ) = q ++ ,       P(Ynk = 1 | C(Xn ) ̸= c0 ) = q −+ .

Thus every judge in the ensemble has the same quality as the original base judge. This is not
required for the guarantees we derive in the following but it simplifies the implementation in
practice, as the same LLM-as-a-judge can be re-used for all judging tasks.
   The ensemble judge accepts Xn if a strict majority of the K votes are positive, i.e.,
                                  (        K
                                                         )                     
                             ∼        1 X       1                             1
                             S=    n:     Ynk >              =       n:Yn >       .
                                      K         2                             2
                                          k=1




                                                     6
We denote the ensemble true- and false-positive rates by
                                                                                               
           ++                1                                −+                   1
           Q    (K) = P Y n > | C(Xn ) = c0 ,                 Q       (K) = P Y n > | C(Xn ) ̸= c0 .
                             2                                                     2
                                                                                 ∼
   In the selection stage, the final answer is chosen uniformly from S . We therefore condition on
                      ∼
the natural event S ̸= ∅, which holds whenever the ensemble judge accepts at least one candidate.
We now compute the probability that this chosen answer is a hallucination.

Theorem 3.2 (Hallucination-selection with an ensemble judge). Let

   • p be the per-trial model correctness probability,

   • q ++ and q −+ be the true- and false-positive rates of the base judge, and

   • Q++ (K) and Q−+ (K) be the corresponding true- and false-positive rates of the ensemble
      judge formed from K independent votes.

Because the ensemble judge is applied only to those outputs that the base judge has first accepted,
only candidates in S = {n : Yn = 1} are forwarded to the ensemble and thus a correct model answer
is accepted by the ensemble judge with probability

                                                pq ++ Q++ (K).

Similarly, an incorrect answer is accepted with probability

                                             (1 − p)q −+ Q−+ (K).
                  ∼                                                                   ∼
Conditioned on S ̸= ∅, the probability that a uniformly chosen element of S is a hallucination is

                                      ∼                   (1 − p) q −+ Q−+ (K)
                  P(C(Xn ) ̸= c0 | S ̸= 0) =                                           .
                                                 p q ++ Q++ (K) + (1 − p) q −+ Q−+ (K)
                            ∼
Proof. An answer enters S if and only if (i) the model produces it, (ii) the base judge marks it
correct, and (iii) the majority of the ensemble judges mark it as correct. A correct answer therefore
       ∼
enters S with probability
                                              p × q ++ × Q++ (K),

and a hallucinated answer enters with probability

                                          (1 − p) × q −+ × Q−+ (K).
                  ∼                                               ∼
Conditioning on S ̸= ∅ and selecting uniformly from S , the selection probability is proportional to
these entry rates, and normalisation yields the stated expression.


3.4    Ensemble judge accuracy
The ensemble false-positive rate can be written in closed form as

                                              K         
                                −+
                                              X         K
                            Q        (K) =                (q −+ )i (1 − q −+ )K−i ,
                                                        i
                                             i=⌈K/2⌉



                                                          7
and similarly for Q++ (K). Standard Hoeffding bounds give, for any q −+ < 21 ,
                                                               2
                                                      1   −+
                                    Q−+ (K) ≤ e−2K 2 −q             ,

showing exponential decay with the number of judges K. Substituting these rates into Theorem 3.2
yields an exponentially decreasing hallucination-selection probability.


3.5    Algorithmic formulation
The following procedure summarizes the repetition–judge pipeline for a perfect judge.

Algorithm 1 Repetition–Judge Pipeline (Perfect-Judge Case)
Require: Specific task with fixed input A and correctness criterion C; number of repetitions N
Ensure: A selected answer or Failure
 1: for n = 1 . . . N do
 2:     Xn ← LLM query with task prompt
 3:     Yn ← judge query in a fresh context window: “Is Xn exactly correct?”
 4: end for
 5: S ← {n : Yn = 1}                          ▷ All answers judged correct by the (perfect) judge
 6: if S = ∅ then
 7:     return Failure
 8: else
 9:     Choose n uniformly random from S
10:     return Xn
11: end if




4     Experiments
We conduct controlled experiments to validate the two quantitative guarantees established in Theo-
rem 3.1 (“How likely are all answers hallucinated?”) and Theorem 3.2 (“How likely will an ensemble
judge select a hallucinated answer?”) using three fixed-input extraction tasks (Appendix A). All
model outputs are generated using Qwen3-4B-Instruct-2507 (Yang et al. 2025). We provide the
implementation online (Schippkus 2026).
    Each task requires the model to return a specific word from a short prompt, making correctness
unambiguous. For each task we estimate the model’s per-trial correctness probability p from 10, 000
independent samples. To control judge quality, we use a synthetic judge that independently flips the
assigned labels Yn with probability 0.25, which yields the base judge quality rates q ++ ≈ 0.75 and
q −+ ≈ 0.25. For ensemble judging, we generate K ∈ {1, 3, . . . , 17} independent judge evaluations
per output and apply a majority vote.
    We execute the full pipeline 10, 000 times and record (i) whether the pipeline fails (the event
                                                                                      ∼
S = ∅) and (ii) whether a hallucination is selected from the ensemble-judged set S . Across all
tasks, empirical pipeline failure decreases with N exactly as predicted by Theorem 3.1 (Figure 2a–
c). Similarly, hallucination-selection rates are shown in Figures 2d–f and decrease with K exactly
as predicted by Theorem 3.2.




                                                 8
Figure 2: Empirical performance of the repetition–judge pipeline and ensemble judge, estimated
over 10, 000 pipeline runs. We present three example tasks with different p and use an imperfect
judge (q ++ = 0.75, q −+ = 0.25). a–c) Pipeline failure rate (”all answers are judged as incorrect”)
decreases exponentially with the number of repetitions N . Theorem 3.1 predicts the observed
decay, indicated by the dashed line. d–f ) Hallucination-selection rate (”the ensemble judge selects
a hallucinated answer”) decreases exponentially with ensemble size K. Theorem 3.2 predicts the
observed decay, indicated by the dashed line. All error bars indicate Wilson confidence intervals.
Together, these demonstrate that the repetition-judge pipeline lays the foundation for reducing
contextual hallucinations to desired rates, even for imperfect judges.


5     Conclusion
This paper presents a probabilistic framework that provides explicit reliability guarantees for
fixed-input LLM workflows. We focus on specific tasks, where the prompt and correctness criterion
are fixed, and show that reliability separates naturally into two independent components: ensuring
that a correct answer appears, and reliably identifying it. We show how under the assumption of
independence between context windows both can be solved.
    For existence, independent repetitions of the same prompt in fresh context windows reduce the
probability that all model outputs are incorrect at an exponential rate (Theorem 2.1). For identi-
fication, we incorporate an LLM-as-a-judge. The reliability of the judged pipeline depends only on
the judge’s true- and false-positive rates (Theorem 3.1). When the judge is imperfect, majority vot-
ing over independent judge calls yields ensemble-level error rates that also decrease exponentially
(Theorem 3.2). These two components—repetition and judged selection—give explicit end-to-end
guarantees with two independent, tunable parameters: the number of model repetitions N and the
number of judge calls K.
    Experiments on controlled extraction tasks with synthetic noisy judges show that empirical
behavior closely matches the theoretical predictions: pipeline failure decreases exponentially with
N and hallucination-selection decreases exponentially with K. This demonstrates that highly reli-
able fixed-input pipelines can be achieved without changing model weights, prompts, or decoding
strategies. It crucially also demonstrates that our assumption of independence is appropriate, at
least for the simple tasks investigated here. We encourage developing this concept further under


                                                 9
less strict requirements.
   Open directions include analyzing judge robustness across domains, optimizing the computa-
tional trade-off between N and K, and extending the framework to tasks with graded correctness or
longer multi-step workflows. Nonetheless, the results establish that any specific task with non-zero
success probability can, in principle, be solved to arbitrarily high reliability by combining indepen-
dent repetitions with judged selection, providing a simple and theoretically grounded foundation
for dependable agentic LLM systems


Acknowledgements
This research was partially funded by the Federal Ministry of Education and Research (BMBF) and
the Free and Hanseatic City of Hamburg under the Excellence Strategy of the Federal Government
and the Länder.


Author contributions (CRediT)
Conceptualization: NR, SS; Formal analysis: NR; SS; Funding Acquisition: SS; Investigation: SS;
Methodology: NR, SS; Resources: SS; Software: SS; Visualization: SS; Writing – original draft:
NR, SS; Writing – review & editing: NR, SS.


References
Adlakha, V., P. BehnamGhader, X. H. Lu, N. Meade, and S. Reddy (2024). Evaluating Correctness
   and Faithfulness of Instruction-Following Models for Question Answering. doi: 10 . 48550 /
   arXiv.2307.16877.
Chang, C.-C., D. Reitter, R. Aksitov, and Y.-H. Sung (2023). KL-Divergence Guided Temperature
  Sampling. doi: 10.48550/arXiv.2306.01286.
Chang, Y., K. Lo, T. Goyal, and M. Iyyer (2024). BooookScore: A Systematic Exploration of Book-
   Length Summarization in the Era of LLMs. doi: 10.48550/arXiv.2310.00785.
Cohen, R., M. Hamri, M. Geva, and A. Globerson (2023). LM vs LM: Detecting Factual Errors
   via Cross Examination. doi: 10.48550/arXiv.2305.13281.
Du, Y., S. Li, A. Torralba, J. B. Tenenbaum, and I. Mordatch (2023). Improving Factuality and
   Reasoning in Language Models through Multiagent Debate. doi: 10.48550/arXiv.2305.14325.
Fabbri, A. R., W. Kryściński, B. McCann, C. Xiong, R. Socher, and D. Radev (2021). “SummEval:
   Re-evaluating Summarization Evaluation”. In: Transactions of the Association for Computa-
   tional Linguistics 9, pp. 391–409. issn: 2307-387X. doi: 10.1162/tacl_a_00373.
Hu, X., D. Ru, L. Qiu, Q. Guo, T. Zhang, Y. Xu, Y. Luo, P. Liu, Y. Zhang, and Z. Zhang
   (2024). RefChecker: Reference-based Fine-grained Hallucination Checker and Benchmark for
   Large Language Models. doi: 10.48550/arXiv.2405.14486.
Huang, L., W. Yu, W. Ma, W. Zhong, Z. Feng, H. Wang, Q. Chen, W. Peng, X. Feng, and B.
   Qin (2025). “A Survey on Hallucination in Large Language Models: Principles, Taxonomy,
   Challenges, and Open Questions”. In: ACM Transactions on Information Systems 43.2, pp. 1–
   55. issn: 1558-2868. doi: 10.1145/3703155.




                                                 10
Jain, S., V. Keshava, S. M. Sathyendra, P. Fernandes, P. Liu, G. Neubig, and C. Zhou (2023).
   “Multi-Dimensional Evaluation of Text Summarization with In-Context Learning”. In: Findings
   of the Association for Computational Linguistics: ACL 2023, pp. 8487–8495. doi: 10.18653/
   v1/2023.findings-acl.537.
Kalai, A. T., O. Nachum, S. S. Vempala, and E. Zhang (2025). Why Language Models Hallucinate.
   doi: 10.48550/arXiv.2509.04664.
Kim, Y., Y. Chang, M. Karpinska, A. Garimella, V. Manjunatha, K. Lo, T. Goyal, and M. Iyyer
   (2024). FABLES: Evaluating Faithfulness and Content Selection in Book-Length Summariza-
   tion. doi: 10.48550/arXiv.2404.01261.
Kryscinski, W., B. McCann, C. Xiong, and R. Socher (2020). “Evaluating the Factual Consistency
   of Abstractive Text Summarization”. In: Proceedings of the 2020 Conference on Empirical
   Methods in Natural Language Processing (EMNLP). Ed. by B. Webber, T. Cohn, Y. He, and
   Y. Liu. Online: Association for Computational Linguistics, pp. 9332–9346. doi: 10.18653/v1/
   2020.emnlp-main.750.
Laban, P., W. Kryściński, D. Agarwal, A. R. Fabbri, C. Xiong, S. Joty, and C.-S. Wu (2023). LLMs
   as Factual Reasoners: Insights from Existing Benchmarks and Beyond. doi: 10.48550/arXiv.
   2305.14540.
Liu, S., K. Halder, Z. Qi, W. Xiao, N. Pappas, P. M. Htut, N. A. John, Y. Benajiba, and D. Roth
   (2025). Towards Long Context Hallucination Detection. doi: 10.48550/arXiv.2504.19457.
Liu, Y., D. Iter, Y. Xu, S. Wang, R. Xu, and C. Zhu (2023). G-Eval: NLG Evaluation Using GPT-4
   with Better Human Alignment. doi: 10.48550/arXiv.2303.16634.
Longpre, S., K. Perisetla, A. Chen, N. Ramesh, C. DuBois, and S. Singh (2021). “Entity-Based
   Knowledge Conflicts in Question Answering”. In: Proceedings of the 2021 Conference on Empir-
   ical Methods in Natural Language Processing. Ed. by M.-F. Moens, X. Huang, L. Specia, and
   S. W.-t. Yih. Online and Punta Cana, Dominican Republic: Association for Computational
   Linguistics, pp. 7052–7063. doi: 10.18653/v1/2021.emnlp-main.565.
Luo, Z., Q. Xie, and S. Ananiadou (2023). ChatGPT as a Factual Inconsistency Evaluator for Text
   Summarization. doi: 10.48550/arXiv.2303.15621.
Madaan, A., N. Tandon, P. Gupta, S. Hallinan, L. Gao, S. Wiegreffe, U. Alon, N. Dziri, S. Prab-
   humoye, Y. Yang, S. Gupta, B. P. Majumder, K. Hermann, S. Welleck, A. Yazdanbakhsh, and
   P. Clark (2023). Self-Refine: Iterative Refinement with Self-Feedback. doi: 10.48550/arXiv.
   2303.17651.
Maynez, J., S. Narayan, B. Bohnet, and R. McDonald (2020). On Faithfulness and Factuality in
   Abstractive Summarization. doi: 10.48550/arXiv.2005.00661.
Rajendhran, R., A. Zadeh, M. Sarte, C. Li, and M. Iyyer (2025). VeriFastScore: Speeding up Long-
   Form Factuality Evaluation. doi: 10.48550/arXiv.2505.16973.
Schippkus, S. (Jan. 2026). schipp/hallucination guarantees: Pre-print. Version pre-print. doi: 10.
   5281/zenodo.18128071. url: https://doi.org/10.5281/zenodo.18128071.
Shi, W., X. Han, M. Lewis, Y. Tsvetkov, L. Zettlemoyer, and S. W.-t. Yih (2023). Trusting Your
   Evidence: Hallucinate Less with Context-aware Decoding. doi: 10.48550/arXiv.2305.14739.
Shinn, N., F. Cassano, E. Berman, A. Gopinath, K. Narasimhan, and S. Yao (2023). Reflexion:
   Language Agents with Verbal Reinforcement Learning. doi: 10.48550/arXiv.2303.11366.
Wan, D., M. Liu, K. McKeown, M. Dreyer, and M. Bansal (2023). Faithfulness-Aware Decoding
   Strategies for Abstractive Summarization. doi: 10.48550/arXiv.2303.03278.



                                               11
Wang, Z., S. Mao, W. Wu, T. Ge, F. Wei, and H. Ji (2024). Unleashing the Emergent Cogni-
     tive Synergy in Large Language Models: A Task-Solving Agent through Multi-Persona Self-
     Collaboration. doi: 10.48550/arXiv.2307.05300.
Yang, A., A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, C. Zheng,
     D. Liu, F. Zhou, F. Huang, F. Hu, H. Ge, H. Wei, H. Lin, J. Tang, J. Yang, J. Tu, J. Zhang,
     J. Yang, J. Yang, J. Zhou, J. Zhou, J. Lin, K. Dang, K. Bao, K. Yang, L. Yu, L. Deng, M. Li,
     M. Xue, M. Li, P. Zhang, P. Wang, Q. Zhu, R. Men, R. Gao, S. Liu, S. Luo, T. Li, T. Tang,
     W. Yin, X. Ren, X. Wang, X. Zhang, X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Zhang, Y. Wan,
     Y. Liu, Z. Wang, Z. Cui, Z. Zhang, Z. Zhou, and Z. Qiu (2025). Qwen3 Technical Report. doi:
     10.48550/arXiv.2505.09388.
Zha, Y., Y. Yang, R. Li, and Z. Hu (2023). AlignScore: Evaluating Factual Consistency with a
     Unified Alignment Function. doi: 10.48550/arXiv.2305.16739.
Zhang, Y., Y. Li, L. Cui, D. Cai, L. Liu, T. Fu, X. Huang, E. Zhao, Y. Zhang, C. Xu, Y. Chen,
     L. Wang, A. T. Luu, W. Bi, F. Shi, and S. Shi (2025). Siren’s Song in the AI Ocean: A Survey
     on Hallucination in Large Language Models. doi: 10.48550/arXiv.2309.01219.


A       Task prompts

       {task}                                                             {target}     c0           p
 A     Sentence one: She wore a bright red striped shirt to the party.    sixth        striped      0.46
       Sentence two: It was very stylish.
 B     Sentence one: Information about the new project was sent to        seventh      sent         0.33
       all staff members.
       Sentence two: Please check your email.
 C     Sentence one: Those three small round silver coins were found      eighth       found        0.59
       in the dirt.
       Sentence two: They looked like ancient Roman money.

Table 1: Three example tasks with {task} and {target} interpolated in the prompt template.
For each task, the ground truth c0 is returned with a probability of p, estimated from 10, 000
model runs.

     We use the following prompt template into which we interpolate {task} and {target} as listed in
Table 1. The resulting prompts are the three specific tasks A, B, and C we investigate empirically
(Figure 2). Prompt template:
       “Below are two sentences.
       Your task: From the *first* sentence, find the {target} word and respond with only
       that word.
       Note: The first sentence has many words, including some that are distractors. The key
       word is near the middle but might be obscured by distractors or complex phrasing. If
       the answer is clear, give the target word. If you are unsure or find it too confusing, say
       ”I don’t know”.
       Here are the sentences:
       {task}
       Respond only with the {target} word of the first sentence, or ”I don’t know” if you’re
       unsure.”


                                                  12
