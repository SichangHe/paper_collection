                                                                      AdapTrack: Constrained Decoding
                                                                    without Distorting LLM’s Output Intent
                                                                     Yongmin Li                                                              Jia Li
                                                              liyongmin@pku.edu.cn                                             jia_li@mail.tsinghua.edu.cn
                                                  Key Lab of High Confidence Software Technology                            College of AI, Tsinghua University
                                                     (Peking University), Ministry of Education;                                      Beijing, China
                                                   School of Computer Science, Peking University
                                                                   Beijing, China

                                                                         Ge Li∗                                                             Zhi Jin
arXiv:2510.17376v1 [cs.SE] 20 Oct 2025




                                                                  lige@pku.edu.cn                                                zhijin@pku.edu.cn
                                                  Key Lab of High Confidence Software Technology                   Key Lab of High Confidence Software Technology
                                                     (Peking University), Ministry of Education;                      (Peking University), Ministry of Education;
                                                   School of Computer Science, Peking University                    School of Computer Science, Peking University
                                                                    Beijing, China                                                  Beijing, China

                                         Abstract                                                                popular. These tools can understand the developer’s intent from the
                                         Language model-based code generation and completion tools have          context and generate code that aligns with their intent by leveraging
                                         been widely adopted, but they may sometimes produce code that           the capabilities of the language models [2, 10, 18, 20, 23].
                                         does not meet necessary constraints, such as syntactic correctness         Legitimate code must satisfy various constraints, such as adher-
                                         or API existence. Constrained decoding techniques are developed         ing to syntax rules and ensuring that the called APIs exist. Language
                                         to help the model generate code that adheres to the constraints         models are designed solely to predict the distribution of the next
                                         by greedily eliminating generation options that violate constraints     token [30, 33], but lack built-in mechanisms to guarantee that the
                                         at each step of the generation process. However, there is a severe      generated code complies with these constraints. As a result, the gen-
                                         limitation of constrained decoding, that it distorts the model’s out-   erated code, while potentially aligned with the developer’s intent,
                                         put intent, forcing it to produce code that may satisfy the con-        may sometimes be illegitimate.
                                         straint but does not match the development intent and is therefore         Constrained decoding methods [3, 29, 32, 35] are developed to
                                         incorrect. In response to this challenge, we propose AdapTrack.         tackle such problems. Using a constrainer to identify tokens ille-
                                         By incorporating backtracking into the generation process, Adap-        gal to come after already generated text, it simply eliminates the
                                         Track avoids distorting the output intent of the language model,        possibility to generate these illegal tokens by directly setting their
                                         thereby producing results that are not only constraint-compliant        probability to zero in the model’s output distribution. Such con-
                                         but also more semantically aligned with model’s output intent.          strainers are often available [3, 35], because the Integrated Devel-
                                         On our synthetic API completion dataset, AdapTrack can achieve          opment Environment (IDE) often provides developers with similar
                                         up to 360.87% improvement compared to constrained decoding;             functionality during their development.
                                         on the real-world API completion dataset we collect that exhibits          However, there is a severe limitation of constrained decod-
                                         similar issues, AdapTrack can also achieve an improvement of up         ing[4, 22, 27], that it distorts the output intent of the model and
                                         to 38.93% over constrained decoding; in general code genration          forces the model to produce unnatural code. In other words, the gen-
                                         benchmarks, compared to constrained decoding, AdapTrack can             erated code, while satisfying the constraints, may deviate from the
                                         achieve up to 7.84% improvement on HumanEval, and up to 6.42%           model’s expected functionality and fail to align with the contextual
                                         improvement on MBPP. This indicates that, simply by better adher-       semantics. Figure 1 shows an example to explain this limitation. The
                                         ing to the model’s output intent, AdapTrack can achieve significant     input code context is shown in Figure 1a. The user wants to calculate
                                         improvements. We provide a theoretical proof that the distribution      the rank of a matrix using PyTorch [6] 2.0. Two APIs can accomplish
                                         produced by AdapTrack aligns with the model’s distribution given        this task: torch.matrix_rank for PyTorch 1.0 to PyTorch 1.8, and
                                         the generated tokens, thereby ensuring that the model’s output          torch.linalg.matrix_rank for PyTorch after 1.8. Depending on
                                         intent is not distorted. Experiments on domain-specific language        the user’s PyTorch version, the model needs to select the appropri-
                                         problems show that, compared to existing methods, our approach          ate API. Figure 1b shows the API names the model intends to output,
                                         can provide generation results that are more consistent with the        along with their corresponding probabilities. Its top candidate is
                                         language model’s distribution.                                          matrix_rank, and second candidate is linalg.matrix_rank. Us-
                                                                                                                 ing a constrainer, it becomes clear that the only legal API in the
                                         1    Introduction                                                       current version is linalg.matrix_rank. Ideally, since we have
                                                                                                                 prohibited the now-illegal matrix_rank by constrained decoding,
                                         In recent years, language model-based code generation and comple-
                                                                                                                 the decoding process should most likely output the most possible
                                         tion tools, such as GitHub Copilot [13], have become increasingly
                                                                                                                 candidate under constraint, i.e. linalg.matrix_rank. However, as
                                         ∗ Corresponding author.                                                 shown in Figure 1c, the API with the highest generation probability
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                                 Yongmin Li, Jia Li, Ge Li, and Zhi Jin


                                                          candidates            probability    usable         candidates                   probability
# pytorch 2.0.0                                           matrix_rank               57.44%       ✘            matrix_power                     57.70%
import torch                                              linalg.matrix_rank        19.21%       ✔            linalg.matrix_rank               20.12%
def matrix_rank(x: torch.Tensor):                         ...                                                 ...
    return torch.                                         matrix_power                0.20%      ✔
(a) The example code context. We want an            (b) Candidate APIs the model wants to generate,        (c) Candidate APIs in constrained decoding.
API to calculate the rank of the tensor.            and whether they are usable in PyTorch 2.0.0.          Compare with Figure 1b.
                                                                        99.59% ⟹ 0.00%
                                                                               rank
               57.96% ⟹ 60.46%                  100.00%                 0.35% ⟹ 97.07%
                     matrix                         _                          power
                                                                        0.01% ⟹ 2.81%
  .                   ...                                                      exp
          21.58% ⟹ 22.51%              100.0%                 100.0%           100%           89.49% ⟹ 89.77%             100.0%                 99.87%
                      l                  inal                    g              .                 matrix                    _                     rank

                                                  (d) What happened during the constrained decoding.

                                Figure 1: An example of incorrect decoding results in constrained decoding.


in constrained decoding is actually matrix_power at 57.70%! This                    If a human were writing this code and discovered that the previ-
is entirely unexpected because, without constrained decoding, the                ously used API matrix_rank was no longer available, but recalled
generation probability of matrix_power is only 0.20%, indicating                 having seen the API linalg.matrix_rank, they would typically
that the model considers it highly unsuitable for this context. How              delete the previously written matrix_ and start over again. Inspired
does this API suddenly become the top choice under constrained                   by this behavior, we wonder if a similar mechanism could be in-
decoding?                                                                        troduced into constrained decoding, allowing the model to quickly
   Let us examine the constrained decoding process step by step,                 backtrack to a point where it might have gone wrong and start
as illustrated in Figure 1d. In the first time step, the legal options in-       anew when encountering such difficulties.
clude matrix, l, and several other less possible tokens. Since there                Based on this idea, we propose AdapTrack, which, during the
are other valid APIs starting with matrix, such as matrix_power                  constrained decoding process, dynamically backtracks according
and matrix_exp, the constrainer does not eliminate the possibil-                 to the proportion of invalid options among the current next-
ity of generating matrix. As a result, the model still chooses the               step choices. If this proportion is large, it indicates that the model
token matrix with a probability of 60.46%. However, once matrix                  is unlikely to want to continue generating along this branch and
and the subsequent _ token are generated, we find that the token                 should switch to another branch; otherwise, it suggests that most of
rank, which accounts for 99.59% of the model’s generation intent, is             the model’s output intent remains on this branch, and we can pro-
prohibited by the constrainer. At this point, since the model has al-            ceed with generation. In this way, we address the aforementioned
ready generated matrix_, it is forced to continue under constrained              issue by dynamically backtracking to avoid generating results that
decoding, leading it to select the token power, which is entirely                deviate too far from the model’s intent under constraints.
misaligned with its output intent. Consequently, even though the                    We provide proof for our algorithm, demonstrating that the
model knows that, aside from matrix_rank, the most appropriate                   distribution it produces is identical to the model’s distribution under
output here should be linalg.matrix_rank, constrained decoding                   constraints given the known generation history. This proves that
compels it to output matrix_power with a 57.70% probability – an                 our method effectively avoids the issue of constrained decoding
answer the model considers highly incorrect.                                     distorting the model’s generation intent, achieving generation that
   We observe that, in the process described above, the model is                 is both constraint-compliant and aligned with the model’s intent.
ultimately forced to select an API that is entirely misaligned                      To demonstrate that AdapTrack does address the issue we raised
with its generation intent. The constrainer can only identify                    in Figure 1 – using unfamiliar APIs correctly with a constrainer, we
errors one step at a time, so the matrix option remains valid. How-              construct a synthetic dataset, TFv1, based on the update in Tensor-
ever, when we realize that the model’s primary intent is thwarted                Flow [1] APIs, deliberately prompting the model to use APIs that
later, we are still compelled to continue generating based on the                are unique to TensorFlow v1. These v1 APIs are still usable in Ten-
previously produced tokens, i.e. matrix_. As a result, the generated             sorFlow v2, except that they have a longer prefix. Since the model
code, while satisfying the constraints, deviates from the model’s                is unaware of the TensorFlow version, its output intent inherently
original output intent.                                                          includes options for both versions. By using the constrainer, we
AdapTrack: Constrained Decoding without Distorting LLM’s Output Intent                                 Conference acronym ’XX, June 03–05, 2018, Woodstock, NY


                                                          60.46% × 99.59% ≈ 60.21% ⟹ 0.00%
                                                               matrix_rank
                                     99.59%                                                                                             99.59% ⟹ 0.00%
                                                              60.46% × 0.35% ≈ 0.21% ⟹ 0.53%
                                      rank                                                                                                 rank
                                                                 matrix_power
          60.46%        100.00% 0.35%                                                                 60.46% ⟹ 0.55% 100.00% 0.35% ⟹ 97.07%
                                                              60.46% × 0.01% ≈ 0.01% ⟹ 0.02%
           matrix            _        power                                                                       matrix         _         power
                                                                 matrix_exp
                                     0.01%                                                                                                0.01% ⟹ 2.81%
 .          ...                       exp             .          ...                                  .           ...                      exp
          22.51%                                                22.51% ⟹ 56.58%                      22.51% ⟹ 56.58%
            l                                                    l                                                l

         (a) The problematic scene.                  (b) Figure 2a is actually equivalent to this.   (c) Collect the probabilities in Figure 2b gives this.
                                                                     0.00%                                              0.00%
                                                                     rank                                               rank
                             0.55%
                                   ≈ 0.91%           100.00% 97.07%
                            60.46%                                                          0.55%         100.00% 97.07%
                                      matrix              _          power                   matrix           _         power
                                                                     2.81%                                              2.81%
                            .          ...                           exp            .         ...                       exp
                                                                                            56.58%
                                       l                                                      l

                          (d) To actually choose the samples the way in          (e) After rejection sampling, the generation
                          Figure 2c, we have to do rejection sampling.           probably looks like what we want.

                           Figure 2: Motivating example: how backtracking works on the example in Figure 1.


examine whether the model can generate these APIs compliant                       divergence from the correct distribution, compared to existing meth-
with TensorFlow v1 or v2. The results show that, across multiple                  ods, indicating that it better aligns with the actual distribution.
code language models, AdapTrack significantly improves API gen-                      We also conduct robustness analysis on temperature and model
eration accuracy compared to naive constrained decoding, with an                  size to ensure AdapTrack works with different hyperparameters.
improvement of up to 360.87%.                                                     Due to potential concerns of efficiency and scalability, we conduct
   To ensure that these results are not merely effective on this                  experiments with limited backtrack distance, showing that a certain
synthetic dataset, we construct a dataset, TFv1Real, based on real-               short-range backtracking is enough on TFv1 and TFv1Real.
world usage examples of these APIs on GitHub, and ask the model                      In summary, our contributions are as follows.
to complete the API given the preceding context. The results on
this dataset show that AdapTrack achieves up to 38.93% improve-
ment over constrained decoding, once again demonstrating the
effectiveness of AdapTrack.                                                             • We propose AdapTrack, a constrained decoding method that
   To verify this issue’s presence and AdapTrack’s generalizability                       can avoid distortion of the model’s output intent in greedy
in constrained decoding of general code generation, we conduct ex-                        constrained decoding.
periments on HumanEval [10] and MBPP [7] with type constrainer                          • We prove that AdapTrack’s distribution aligns with the model’s
[26]. The results show that AdapTrack can achieve up to 7.84%                             distribution given the generated tokens. Experiments on DSL
improvement on HumanEval, and up to 6.42% improvement on                                  problems show that the distribution produced by AdapTrack
MBPP, showing the generalizability of AdapTrack.                                          aligns closer with the model’s true intent.
   To demonstrate that the generation results of our method are                         • We construct the TFv1 and TFv1Real datasets to simulate
indeed more aligned with the model’s output intent, we conduct                            scenarios where the model is unfamiliar with APIs. The
experiments on domain-specific language problems, sampling 2000                           results demonstrate that our method significantly improves
results for each problem consecutively and comparing them with                            the accuracy of API generation, with an improvement up to
2000 results by previous approaches. The results show that the                            360.87% on TFv1 and 38.93% on TFv1Real. Experiments on
distribution produced by our method has a significantly lower KL                          HumanEval and MBPP demonstrate the generalizability of
                                                                                          AdapTrack in general code generation.
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                                     Yongmin Li, Jia Li, Ge Li, and Zhi Jin


2    Motivating example                                                 sampling processes, we achieve a sampling outcome where matrix
We have seen the problem of constrained decoding in Figure 1. The       is adopted with a probability of 0.55%.
problem occurs when the decoding process eliminates the proba-             After this resampling, one possible result is shown in Figure 2e,
bility of one API, but fails to generate another highly possible API    where the first token is changed to l. This directs us towards the
with a different prefix. We propose to introduce backtracking into      generation of the second candidate, linalg.matrix_rank.
the decoding process as a potential solution, and in this section we
will delve into a more comprehensive discussion of this approach.       3 Background
    Figure 2 shows step by step how to utilize this intuition to mod-   3.1 Goal
ify the constrained decoding process. The arrows between tokens
                                                                        We have demonstrated, by example, that the output of constrained
represent the generation order. A solid arrow indicates that the
                                                                        decoding can be far away from the model’s intent, which can be
current state of generation includes this step, whereas a dashed
                                                                        shown by the large difference between the probability distribution
arrow signifies other potential generation options. A red dashed
                                                                        of constrained decoding and that of the language model.
box denotes tokens that are invalid in the current context, and a
                                                                           To keep the output aligned with the model’s intent, the best
green solid box represents valid tokens. The numbers on the to-
                                                                        option is to perfectly align with the probability distribution of the
kens indicate their conditional generation probabilities given the
                                                                        language model while keeping the constraints. In this subsection,
preceding context.
                                                                        we will formalize this goal.
    Figure 2a illustrates the scenario where the issue mentioned in
                                                                           Given a context 𝑠 <𝑖 , an autoregressive language model can pro-
Figure 1 occurs. At this point, we have generated matrix_, and
                                                                        duce a distribution over the next token 𝑃 (𝑠𝑖 |𝑠 <𝑖 ). This allows us
subsequently identified the following token options, their validity,
                                                                        to define a distribution over all possible sequences, i.e., the joint
and how much the language model wants to generate them. We
                                                                        probability distribution of the entire sequence,
observe that the model has a 99.59% probability to generate the
invalid rank token.                                                                                                   𝑛
                                                                                                                      Ö
    We now consider the overall probability of the sequence from                             𝑃 (𝑠 0, . . . , 𝑠𝑛 ) =         𝑃 (𝑠𝑖 |𝑠 <𝑖 ).
                                                                                                                      𝑖=0
the first token up to each candidate option, as shown in Figure 2b.
For example, the probability of the model generating matrix_rank           A constrainer is a function defined on a sequence 𝑐 : 𝑠 ↦→ {0, 1},
is roughly 60.21%. After eliminating invalid options, we can renor-     where the result is 0 if all sequences that start with this sequence
malize the probabilities of all remaining valid options. This process   as their prefix is invalid, and 1 otherwise. We use 𝐶 (𝑠) = {𝑡 |𝑐 (𝑠 ::
ensures that all valid options experience an equivalent proportional    [𝑡]) = 1} to represent all valid tokens after the prefix 𝑠.
increase in their probabilities.                                           Our task is to define a distribution 𝑃𝑐 over all valid sequences,
    We can reorganize the probabilities, resulting in Figure 2c. The    such that the probability of generating any sequence is proportional
probability of matrix has decreased from 60.46% to 0.55%, which         to its probability under the language model. This can be formally
aligns more closely with our intuition that, after learning that the    expressed as follows,
top candidate matrix_rank is invalid, the model should aim to
generate the second candidate, which does not begin with matrix.                        𝑃 (𝑠 |𝑐) ∝ 𝑃 (𝑠)𝑐 (𝑠), ∀𝑠 that is complete.
This happens because we have performed a global probability ad-           Or equivalently, for any two valid complete sequences 𝑠 and 𝑠 ′ ,
justment after eliminating the invalid option matrix_rank, thereby      we should have the following property,
allowing the probability of matrix to correctly decrease.
    Now we want to backtrack and change the initial choice of                                         𝑃 (𝑠 |𝑐)    𝑃 (𝑠)
                                                                                                                =         .                                   (1)
matrix, so that we can follow the output intent of the model to                                       𝑃 (𝑠 ′ |𝑐) 𝑃 (𝑠 ′ )
not generate matrix and circumvent the limitation of constrained
decoding. But now comes the question: given that we have already        3.2    Constrained decoding and its problem
generated matrix with a probability of 60.46%, how can we adjust        Constrained decoding is an ad-hoc modification of rejection sam-
this probability to 0.55%? One option is to directly resample. In       pling, where illegal options are directly removed during the sam-
practice, however, this would imply that we would resample the          pling process. Specifically, instead of repeatedly sampling and dis-
entire sequence regardless of how minor the new error identified        carding invalid sequences, constrained decoding eliminates invalid
by the constrainer is, which would be wasteful of time and com-         options at each step, ensuring that only valid tokens are considered
putational resources. We have an intuition that if the probability      for generation.
change is substantial, we are likely inclined to depart from this           Consider the generation probability of a valid sequence 𝑠 =
branch; otherwise, we probably wish to remain within the same           (𝑠 0, . . . , 𝑠𝑛 ) under constrained decoding. At each step of sampling 𝑠𝑖 ,
branch.                                                                 the probability can be viewed as a form of rejection sampling, where
    To formalize this intuition, we propose the use of rejection sam-   the probability of sampling 𝑠𝑖 given the prefix 𝑠 <𝑖 is normalized over
pling for adaptive backtracking, as shown in Figure 2d. We have         all valid continuations. Specifically, the probability of sampling 𝑠𝑖
generated matrix with a probability of 60.46%. We can perform a         is given by the following equation,
second sampling with an acceptance rate of roughly 0.91%. If the                      𝑃con (𝑠𝑖 | 𝑠 <𝑖 ) ∝ 𝑃 (𝑠𝑖 | 𝑠 <𝑖 )⟦𝑠𝑖 ∈ 𝐶 (𝑠 <𝑖 )⟧,
sampling succeeds, we can continue to use matrix; otherwise, we
switch to another token. Thus, by combining the results of the two                                          𝑃 (𝑠𝑖 | 𝑠 <𝑖 )⟦𝑠𝑖 ∈ 𝐶 (𝑠 <𝑖 )⟧
                                                                                      𝑃con (𝑠𝑖 | 𝑠 <𝑖 ) =      Í                            .
                                                                                                                 𝑡 ∈𝐶 (𝑠 <𝑖 ) 𝑃 (𝑡 | 𝑠 <𝑖 )
AdapTrack: Constrained Decoding without Distorting LLM’s Output Intent                                   Conference acronym ’XX, June 03–05, 2018, Woodstock, NY


  Let us compare the generation probabilities of two valid se-                 Algorithm 1 Collect a sequence from next tokens
quences 𝑠 and 𝑠 ′ .                                                              1: procedure CollectSeqence(𝑁 )
                               Î𝑛′ Í                       ′                           𝑠 ←𝜀
                                             ′ ) 𝑃 (𝑡 | 𝑠 )                      2:
            𝑃con (𝑠)    𝑃 (𝑠) 𝑖=0 𝑡 ∈𝐶 (𝑠 <𝑖               <𝑖
                      =                                         .                3:    while Contains(𝑁 , 𝑠) do
           𝑃con (𝑠 ′ ) 𝑃 (𝑠 ′ ) 𝑛𝑖=0 𝑡 ∈𝐶 (𝑠 <𝑖 ) 𝑃 (𝑡 | 𝑠 <𝑖 )
                               Î    Í
                                                                                 4:       𝑠 ← 𝑠 :: [𝑁 [𝑠]]
   When compared to the equation 1, the second term in the prod-                 5:    end while
                                                       ′ ), cannot
uct, which depends on the sums over 𝐶 (𝑠 <𝑖 ) and 𝐶 (𝑠 <𝑖                        6:    return 𝑠
be canceled out. This shows that the generation probabilities of                 7: end procedure
sequences under constrained decoding are distorted relative to their
original language model probabilities.

4    AdapTrack                                                                    The estimated validity 𝑄 [𝑥 :: [𝑁 [𝑥]]] of the current next token
                                                                               𝑁 [𝑥] decreases during the update because we always overestimate
After defining our goal and necessary notations in section 3, we
                                                                               the validity. This reduces the probability of drawing 𝑁 [𝑥] from
can now describe our algorithm AdapTrack. Overall, our algorithm
                                                                               𝑃𝑄 (·|𝑥), as shown in formula 3. We decide whether we continue
keeps track of the validity of all known incomplete sequences and
                                                                               to use 𝑁 [𝑥] as the sample from the updated 𝑃𝑄 (·|𝑥) by rejection
maintains a sample for each prefix based on the validity information.
                                                                               sampling. Denote 𝑄 before updating as 𝑄, and that after updat-
Our algorithm repeatedly samples an incomplete sequence and
                                                                               ing as 𝑄 ′ . We sample a Bernoulli distribution with the probability
collects the validity information into the sample. We compare the
                                                                               of 𝑃𝑄 ′ (𝑁 [𝑥]|𝑥)/𝑃𝑄 (𝑁 [𝑥]|𝑥) to keep the current next token 𝑁 [𝑥]
validity information before and after this sampling and perform
                                                                               unchanged, and otherwise change to other tokens 1 . If we change
rejection sampling to correct the samples for each prefix. When the
                                                                               to another next token, which means backtracking occurs, we
rejection happens, our algorithm will next time select a different
                                                                               sample a new next token from all other tokens with probability
token on this prefix. This is equivalent to backtracking, because
                                                                               𝑃𝑄 (·|𝑐, 𝑥), but we explicitly exclude the old 𝑛 := 𝑁 [𝑥].
we no longer use the same partially generation sequence.
   Let us start from the beginning. We want to sample the distribu-                                   𝑃𝑄′ (𝑛 ′ |𝑥, 𝑛) ∝ 𝑃𝑄 (𝑛 ′ |𝑥)⟦𝑛 ′ ≠ 𝑛⟧.                          (4)
tion 𝑃 (𝑠 |𝑐), which can be decomposed as a series of sampling from
𝑃 (𝑠𝑖 |𝑐, 𝑠 <𝑖 ) as follows,                                                      Collectively, our procedure can be summarized in algorithm 2.
                                      Ö
                           𝑃 (𝑠 |𝑐) =   𝑃 (𝑠𝑖 |𝑐, 𝑠 <𝑖 ).
                                         𝑖
                                                                               Algorithm 2 AdapTrack
    𝑃 (𝑠𝑖 |𝑐, 𝑠 <𝑖 ) can be decomposed by the Bayesian rule as follows,
                                                                                 1: procedure BacktrackSample(𝑃 LM , 𝑐)
                 𝑃 (𝑠𝑖 |𝑐, 𝑠 <𝑖 ) ∝ 𝑃 (𝑠𝑖 |𝑠 <𝑖 )𝑃 (𝑐 |𝑠 <𝑖 :: [𝑠𝑖 ]).           2:    𝑄←∅                      ⊲ Estimate of 𝑃 (𝑐 |𝑠) for all known 𝑠
   For every prefix 𝑥, we define our current estimation of 𝑃 (𝑐 |𝑥) as           3:    𝑁 ←∅                     ⊲ Sample of 𝑃𝑄 (·|𝑠) for all known 𝑠
𝑄 [𝑥], where 𝑄 is an associative array. We call a prefix 𝑥 is new if             4:    while true do
we have not calculated 𝑃 (·|𝑥); otherwise we call it old. If the prefix          5:       𝑠 ← CollectSeqence(𝑁 )
𝑥 is invalid, 𝑄 [𝑥] should be 0; otherwise, if 𝑥 is old, which means we          6:       if 𝑠 −1 is complete then
know possible valid sequences starting from 𝑥, we simply aggregate               7:            return 𝑠
the information; otherwise, we just assume that its children are                 8:       end if
always valid and use 1 as an estimation.                                         9:       𝑁 [𝑠] ∼ 𝑃𝑄 (·|𝑠)
              (                                                                 10:       Update 𝑄 by formula 2, denote the updated 𝑄 as 𝑄 ′
               𝑐 (𝑥)                     if 𝑐 (𝑥) = 0 or 𝑥 is new;                             ⊲ Update from the longest sequence to the shortest
    𝑄 [𝑥] := Í                                                       (2)
                  𝑢 𝑃 (𝑢 |𝑥)𝑄 [𝑥 :: [𝑢]] if 𝑐 (𝑥) = 1 and 𝑥 is old.             11:       for each prefix 𝑥 of 𝑠 excluding 𝑠 itself do
                                                                                12:            𝑛 ← 𝑁 [𝑥]                               ⊲ The old 𝑁 [𝑥]
We use 𝑃𝑄 (·) to denote the distribution of 𝑃 (·|𝑐) estimated with 𝑄,           13:            𝑝 ← 𝑃𝑄 (𝑛|𝑥)
                  𝑃𝑄 (𝑠𝑖 |𝑠 <𝑖 ) ∝ 𝑃 (𝑠𝑖 |𝑠 <𝑖 )𝑄 [𝑠 <𝑖 :: [𝑠𝑖 ]].       (3)    14:            𝑝 ′ ← 𝑃𝑄 ′ (𝑛|𝑥)
                                                                                15:            𝑏 ∼ Bernoulli(𝑝 ′ /𝑝)             ⊲ Rejection sample
   For every prefix 𝑥 we have encountered during decoding, we
                                                                                16:            if 𝑏 = 0 then                               ⊲ Backtrack
maintain a next token 𝑁 [𝑥] sampled from 𝑃𝑄 (·|𝑥), where 𝑁 is an
                                                                                17:                𝑁 [𝑥] ∼ 𝑃𝑄′ (·|𝑥, 𝑛) as formula 4
associative array. We can concatenate all the next token samples to
get a sample from 𝑃𝑄 (·), as shown in algorithm 1.                              18:            end if
   Our decoding process first samples a prefix 𝑠 from 𝑃𝑄 (·) as in-             19:       end for
dicated by 𝑁 . If it is a complete sequence, we can just return it.             20:    end while
                                                                                21: end procedure
Otherwise, we call the constrainer for every possible next token and
record their information in 𝑄 accordingly. We sample 𝑁 [𝑠] from all
the valid next tokens by their probability from the language model
(the same distribution as 𝑃𝑄 (·|𝑠)). We update 𝑄 [𝑥] for all prefixes
𝑥 of the sequence 𝑠 and decide whether we want to backtrack at                 1 This probability is different from 𝑄 ′ [𝑥 :: [𝑁 [𝑥 ] ] ]/𝑄 [𝑥 :: [𝑁 [𝑥 ] ] ] , because the
this prefix by updating the prefix’s next token 𝑁 [𝑥].                         denominator in 𝑃𝑄 (· |𝑥 ) is also changed.
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                                      Yongmin Li, Jia Li, Ge Li, and Zhi Jin


5    The proof of AdapTrack                                                                RQ1. How does AdapTrack perform in predicting correct and
AdapTrack focuses on not distorting the model distribution under                        valid APIs?
constraint and, therefore, not distorting its output intent. We now
                                                                                           RQ2. How does AdapTrack perform in predicting correct and
give a proof of this statement.
                                                                                        valid APIs in real-world scenarios?
  Theorem 5.1. Algorithm 2 only returns a valid complete sequence,
and the probability of generating different sequences that have been                      RQ3. How does AdapTrack perform in general code generation?
explored during decoding satisfies equation 1.                                             RQ4. How does AdapTrack align with the oracle distribution of
                                                                                        language models under constraint?
   Proof. The only return statement is step 7, so the returned
sequence is always complete. Also, the returned sequence is col-
lected from 𝑁 , where 𝑁 [𝑥] ∼ 𝑃𝑄 (·|𝑥) ∝ 𝑃 (·|𝑥)𝑄 [𝑥 :: [·]] always                     6.1   RQ1: Performance of AdapTrack in
guarantees that 𝑁 [𝑥] is a valid subsequent token for any prefix 𝑥,                           predicting correct and valid APIs
so the algorithm always returns valid well-ended sequences.                             As the library evolves, it often happens that an old API is transi-
   Collecting one sample sequence from 𝑁 is equivalent to sampling                      tioned into another new API. If the user has updated their library,
a result from 𝑃𝑄 (·) because we always maintain this property in                        only the new APIs should be used; if not, only the old APIs should
the algorithm by rejection sampling, as shown in theorem 5.2.                           be used. In RQ1, we aim to simulate this scenario. We ask the model
   For any new sequence 𝑠 = (𝑠 0, . . . , 𝑠𝑛 ),                                         to use the same API with the old and the new versions of the same
                  𝑛                          𝑛                                          library, respectively. The APIs used by the model should not only
                  Ö                         Ö    𝑃 (𝑠𝑖 |𝑠 <𝑖 )𝑄 [𝑠 <𝑖 :: [𝑠𝑖 ]]
       𝑃𝑄 (𝑠) =          𝑃𝑄 (𝑠𝑖 |𝑠 <𝑖 ) =       Í                               ,       have the correct semantics, but also be valid in the correspond-
                  𝑖=0                       𝑖=0  𝑢 𝑃 (𝑢 |𝑠 <𝑖 )𝑄 [𝑠 <𝑖 :: [𝑢]]          ing library version. With the new library, the model should adopt
                  𝑛
                  Ö 𝑃 (𝑠𝑖 |𝑠 <𝑖 )𝑄 [𝑠 ≤𝑖 ]          𝑄 [𝑠]           1                   the new API; with the old one, it should stick to the old API.
              =                                 =         𝑃 (𝑠) =       𝑃 (𝑠).      □
                  𝑡 =0
                              𝑄 [𝑠 <𝑖 ]             𝑄 [𝜀]         𝑄 [𝜀]

   Theorem 5.2. The update process of 𝑁 in steps 11 to 19 in algo-                      import tensorflow as tf
rithm 2 makes 𝑁 [𝑥] follows distribution 𝑃𝑄 (·|𝑥) for prefix 𝑥.
                                                                                        def mean_pairwise_squared_error(*args, **kwargs):
    Proof. We give a proof by induction on the update of 𝑁 [𝑥].                             """
                                                                                            wrapper for losses.mean_pairwise_squared_error
    Base case. In step 9, 𝑁 [𝑥] is drawn from 𝑃𝑄 (·|𝑥).                                     """
                                                                                            return tf
    Induction step. When the distribution 𝑄 [𝑥] is updated in step 10,
denote the original 𝑁 [𝑥] by 𝑛.
    By rejection sampling with an acceptance rate of 𝑃𝑄 ′ (𝑛|𝑥)/𝑃𝑄 (𝑛|𝑥) ≤                     Figure 3: An example code in the TFv1 dataset.
1, the total probability of generating 𝑛 as a sample after the prefix
𝑥 is as follows.
                                     𝑃𝑄 ′ (𝑛|𝑥)
                     𝑃𝑄 (𝑛|𝑥) ×                 = 𝑃𝑄 ′ (𝑛|𝑥).                              Dataset. We construct a dataset, TFv1, based on the update from
                                     𝑃𝑄 (𝑛|𝑥)                                           TensorFlow v1 to v2. We prompt the model to generate an API
   The probability of generating another token 𝑛 ′ ≠ 𝑛 as a sample                      unique to v1 in a context where it cannot infer the library ver-
after the prefix 𝑥 is as follows.                                                       sion and then evaluate its ability to correctly generate the API
                                                                                        in both v1 and v2 settings. The version information is given
                                                               𝑃𝑄 (𝑛 ′ |𝑥)
                                                     
                                          𝑃𝑄 ′ (𝑛|𝑥)
        𝑃𝑄 (𝑛 ′ |𝑥) + 𝑃𝑄 (𝑛|𝑥) × 1 −                    ×                  ,            to the constrainer, so the constrainer is aware of all the valid
                                          𝑃𝑄 (𝑛|𝑥)          1 − 𝑃𝑄 (𝑛|𝑥)                APIs in the setting. To guide the model toward using a specific
                              𝑃𝑄 (𝑛 ′ |𝑥)                                               API, we explicitly annotate the function as a wrapper, encour-
      =(1 − 𝑃𝑄 ′ (𝑛|𝑥)) ×                   ,
                            1 − 𝑃𝑄 (𝑛|𝑥)                                                aging the model to directly forward calls to this API. An exam-
                              𝑃 (𝑛 ′ |𝑥)𝑄 [𝑥 :: [𝑛 ′ ]]                                 ple is illustrated in Figure 3. For this example, the correct an-
      =(1 − 𝑃𝑄 ′ (𝑛|𝑥)) × Í                                  ,                          swer is .losses.mean_pairwise_squared_error and .compat.-
                              𝑢≠𝑛 𝑃 (𝑢|𝑥)𝑄 [𝑥 :: [𝑢]]
                                                                                        v1.losses.mean_pairwise_squared_error for TensorFlow v1 and
                               𝑃 (𝑛 ′ |𝑥)𝑄 ′ [𝑥 :: [𝑛 ′ ])]
      =(1 − 𝑃𝑄 ′ (𝑛|𝑥)) × Í                       ′
                                                                 ,                      v2 settings, respectively.
                              𝑢≠𝑛 𝑃 LM (𝑢 |𝑥)𝑄 [𝑥 :: [𝑢]]                                  We collect all legal APIs under TensorFlow 2.16 from the official
                              𝑃𝑄 ′ (𝑛 ′ |𝑥)
      =(1 − 𝑃𝑄 ′ (𝑛|𝑥)) ×                      = 𝑃𝑄 ′ (𝑛 ′ |𝑥).              □          TensorFlow website. From them, we filter all APIs starting with
                            1 − 𝑃𝑄 ′ (𝑛|𝑥)                                              tf.compat.v1. We exclude APIs that have counterparts in v2 based
                                                                                        on the last part of the API name. To avoid interference from classes
6    Evaluation                                                                         and methods, we retain only APIs where all parts of its name start
We have proven AdapTrack aligns with the language model in                              with a lowercase letter. To avoid interference from subpackages,
section 5. In this section, we evaluate AdapTrack against other                         we remove all APIs that can be a prefix of another API. Ultimately,
decoding methods to answer the following research questions:                            we obtained 419 standalone TensorFlow v1-specific APIs.
AdapTrack: Constrained Decoding without Distorting LLM’s Output Intent                                 Conference acronym ’XX, June 03–05, 2018, Woodstock, NY


                                        Table 1: Exact match on TFv1 in different TensorFlow versions.

                                                     TensorFlow v1 setting                                  TensorFlow v2 setting
      Method                           EM@1        EM@3 EM@5 EM@10                 EM@20      EM@1        EM@3 EM@5 EM@10                    EM@20
      Qwen2.5 Coder 7B
      Unconstrained decoding           61.58%     73.07%      81.51%     88.85%    92.84%      7.16%     19.04%      26.17%       37.77%      50.60%
      Constrained decoding             66.11%     76.35%      83.50%     90.10%    94.03%     18.38%     31.84%      39.63%       50.34%      60.86%
      AdapTrack (Ours)                 80.19%     87.36%      91.86%     95.96%    98.33%     54.89%     62.51%      68.87%       76.52%      82.82%
      DeepSeek Coder Base 6.7B
      Unconstrained decoding           62.53%     68.63%      78.50%     88.43%    94.27%      5.97%     16.91%      24.12%       36.49%      50.60%
      Constrained decoding             65.63%     73.34%      82.03%     90.26%    94.75%     10.98%     25.31%      33.32%       45.90%      59.43%
      AdapTrack (Ours)                 83.29%     86.98%      92.47%     96.48%    98.09%     50.60%     56.62%      64.76%       74.57%      82.82%
      StarCoder2 7B
      Unconstrained decoding           72.79%     76.37%      85.12%     92.30%    96.18%      1.67%     12.66%      18.62%       29.76%      44.15%
      Constrained decoding             73.99%     79.99%      87.36%     93.23%    96.42%     10.26%     21.48%      28.83%       40.48%      53.70%
      AdapTrack (Ours)                 83.53%     88.78%      92.97%     96.36%    98.33%     45.35%     50.90%      59.70%       69.75%      77.57%
      CodeLlama Python 7B
      Unconstrained decoding           59.90%     70.63%      78.86%     86.61%    91.41%     11.93%     25.20%      32.52%       43.46%      55.37%
      Constrained decoding             66.35%     76.36%      83.47%     89.78%    93.56%     21.24%     38.35%      46.12%       56.96%      67.54%
      AdapTrack (Ours)                 83.29%     89.37%      92.82%     95.70%    97.14%     60.86%     68.20%      73.37%       79.56%      85.20%


   Metrics. We use exact match (EM) metrics. We report EM@𝑘                       Python 7B[31]. We only use base models in this experiment, be-
[10],                                                                             cause the task of code completion aligns better with the training
                                  "    𝑛−𝑐 
                                             #                                    target of the base models than that of the instruct models.
                                                   𝑘
                    EM@𝑘 := EProblems 1 −          𝑛    ,               (5)
                                                   𝑘
                                                                                     Results. As shown in Table 1, for both TensorFlow v1 and
where 𝑛 is the sample size, 𝑐 is how many samples exactly match
                                                                                  v2 settings, AdapTrack performs significantly better than
the oracle in 𝑛 samples, and 𝑘 is in 1, 3, 5, 10, 20. EM@𝑘 reflects the
                                                                                  constrained decoding, with an improvement up to 360.87%.
expected value of achieving an exact match within 𝑘 attempts.
                                                                                     In the TensorFlow v1 setting, Qwen2.5 Coder 7B can already
   For each method on each problem in each setting, we sample
                                                                                  achieve an EM@1 of 61.58%. If we equip it with a constrainer, the
one result by greedy decoding and then sample 20 results randomly.
                                                                                  result can be improved to 66.11%, indicating the model may still
For EM@1, we use the greedy result, and the sample size is 1. For
                                                                                  generate some API calls invalid in TensorFlow v1 and eliminated
EM@𝑘 where 𝑘 > 1, we calculate the metrics from the 20 samples.
                                                                                  by the constrainer. But using AdapTrack, the result can be further
Because unconstrained decoding does not depend on the version
                                                                                  improved to 80.19%, indicating that, in roughly 14% cases, the model
information, we reuse the same sampling results and only change
                                                                                  considers the oracle as its best candidate under constraint but fails
the oracle between the two settings.
                                                                                  to generate it, because constrained decoding does not allow the
   Baselines. We compare with two baselines, unconstrained decod-                 model to modify already generated tokens. Since AdapTrack does
ing and constrained decoding. Unconstrained decoding is decoding                  allow the model to modify them to better express its output intent,
without a constrainer. At each time step, the next token is sampled               AdapTrack performs significantly better than simple constrained
from the model distribution without filtering. Constrained decod-                 decoding.
ing is the decoding method we describe in section 3. At each time                    It is more dramatic in TensorFlow v2. Without a constrainer,
step, the probabilities of invalid tokens are set to 0 in the model               Qwen2.5 Coder 7B can only achieve an EM@1 of 7.16%. This result
distribution before sampling.                                                     should be considered together with EM@1 in the TensorFlow v1
                                                                                  environment. For 61.58% cases, the model wants to generate v1-
   Implementation. For the TensorFlow v2 setting, we use all col-                 compliant APIs as the best candidate, and then it cannot generate v2-
lected TensorFlow APIs as valid APIs in the constrainer. For Ten-                 compliant APIs by unconstrained decoding. If we add a constrainer,
sorFlow v1 setting, we use all the v1 APIs as valid APIs in the                   this result can be improved to 18.38%, because APIs that are invalid
constrainer, but we remove their additional prefix compatv̇1, to                  in TensorFlow v2 cannot be generated now.
keep the same syntax as in TensorFlow v1. We implement the Adap-                     Now consider the results of AdapTrack. With the help of the con-
Track algorithm with PyTorch[6] and Transformers[36] library.                     strainer to remove invalid APIs, the model can now freely generate
We conduct experiments on a 64-core Intel Xeon machine with 8                     the best remaining option in its candidates, resulting in an EM@1
NVIDIA RTX A6000 GPUs.                                                            of 54. 89%, which is an improvement of 198. 70% over the 18. 38%
                                                                                  EM@1 of constrained decoding. This is even better than EM@10
  Models. We conduct experiments on Qwen2.5 Coder 7B[16],                         of constrained decoding, further showing the importance of not
DeepSeek Coder Base 6.7B[14], StarCoder2 7B[25] and CodeLlama                     distorting the language model’s output intent.
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                            Yongmin Li, Jia Li, Ge Li, and Zhi Jin


                Table 2: Exact match on TFv1Real.                              Take Qwen2.5 Coder 7B as an example. Qwen2.5 Coder 7B can
                                                                            already correctly generate 21.70%. With a constrainer to eliminate
                                    Exact Match @ 𝑘 (↑)                     invalid options, the EM@1 can be further improved to 35.60%, indi-
 Method               EM@1        EM@3 EM@5 EM@10                  EM@20    cating that the model is generating many invalid APIs when not
 Qwen2.5C 7B                                                                constrained. With AdapTrack, this result can be further improved
 Unconstrained        21.70%     29.45%      35.28%       43.88%   53.00%   to 49.30%, an improvement of 38.48% compared to the result of
 Constrained          35.60%     41.86%      47.64%       55.29%   62.30%   constrained decoding, indicating that in constrained decoding, the
 AdapTrack            49.30%     53.87%      59.28%       65.84%   71.70%   model is forced to generate many suboptimal options that are mis-
 DSC Base 6.7B                                                              aligned with the model’s output intent. The improvement is not
 Unconstrained        18.90%     25.62%      30.93%       38.66%   47.10%   as significant as in the TFv1 dataset. Nevertheless, 49.30% is still a
 Constrained          31.10%     38.45%      44.09%       51.23%   57.70%   large improvement.
 AdapTrack            41.90%     49.45%      55.26%       62.25%   68.30%      Similar analysis can be applied to the results of other models,
 SC2 7B                                                                     while the largest improvement, 38.93% compared to constrained
 Unconstrained        15.90%     21.91%      27.33%       35.59%   44.70%   decoding, happens in the results of StarCoder2 7B at EM@1, from
 Constrained          29.80%     35.55%      41.69%       49.59%   56.60%   29.80% to 41.40%.
 AdapTrack            41.40%     47.60%      53.85%       61.62%   68.10%
 CL Python 7B                                                               6.3    RQ3: Performance of AdapTrack in general
 Unconstrained        19.60%     26.88%      32.26%       40.48%   49.40%          code generation
 Constrained          34.40%     40.77%      46.99%       55.10%   62.30%
 AdapTrack            46.80%     52.61%      58.75%       66.41%   73.00%   In RQ1 and RQ2, we conduct experiments on two API comple-
                                                                            tion datasets, TFv1 and TFv1Real. Now we want to know whether
                                                                            AdapTrack is effective in general code generation.
   Similar analysis can be applied to the results of other models,             Dataset. We adopt the widely used HumanEval [10] and MBPP
while the biggest improvement, 360.87% compared to constrained              [7] benchmarks. We use a type constrainer [26] to ensure the gen-
decoding, happens at EM@1 of DeepSeek Coder Base 6.7B in Ten-               erated programs are well-typed. Because the constrainer is only
sorFlow v2 environment, from 10.98% to 50.60%.                              available for programs written in TypeScript, we use the TypeScript-
                                                                            translated versions from the MultiPL-E dataset [9].
6.2     RQ2: Performance of AdapTrack in
        real-world API completion                                             Metrics. We report pass@𝑘 [10], which is given by replaces 𝑐 in
We have found that AdapTrack is extremely effective on tf.-                 equation 5 with how many samples can pass the test.
compat.v1. APIs in RQ1, but the results come from a synthetic
                                                                               Sampling strategy. It is too time-consuming to check the validity
dataset, TFv1. We want to know whether this phenomenon also
                                                                            of the whole vocabulary after every prefix. We introduce a vari-
occurs in real-world code completion.
                                                                            ant of top-𝑝 (nucleus) sampling [15] to reduce the tokens to be
   Dataset. We collect real usage of such APIs from GitHub. For             checked. We check the vocabulary from the most possible token to
every v1 API in TFv1, we search for tf.compat.v1.API(, and col-             the least possible one. After calculating the validity of each token,
lect 46,785 Python files from GitHub. We deduplicate these files            we calculate the total probability of known valid tokens, and its
and split each file on the first usage of tf.compat.v1. in code. We         ratio to the total probability of possibly valid tokens (i.e. known
then remove all files that contain tf.compat.v1 in the prefix. If the       valid tokens + unchecked tokens). Once this ratio exceeds 𝑝, all re-
suffix does not start with an API call, the file is also removed. After     maining unchecked tokens are considered invalid. In unconstrained
these cleaning steps, we now obtain 14,237 files. We use the prefix         decoding, this sampling strategy naturally becomes the classic top-
as the completion prefix and the starting API call in the suffix as         𝑝 sampling, because the constrainer now considers every token to
the oracle.                                                                 be valid.
   We then calculate the length distribution of the prefixes. We
use the tokenizer of CodeLlama 7B Python to tokenize the prefixes               Implementation. We modify the constrainer to fix several bugs
because it has a relatively small vocabulary of 32,000 tokens, which        and speed up the calculation. We open-source the modified package
makes it easier to overflow the model’s max position after tokeniza-        together with our source code.
tion. The average length of the prefixes is 1,624.78 tokens, and 90%            We restart generation when the constrainer cannot determine
of the prefixes have less than or equal to 3,463.0 tokens. To make          validity of one token in 60 seconds. Since greedy sampling always
the dataset friendlier to models with smaller context windows, we           returns the same answer for the same problem, if greedy sampling
remove files whose prefix is longer than 4,096 - 512 = 3,584 tokens.        is restarted 20 times for the same problem, the sample is considered
This gives us 12,883 files. We then randomly pick 1,000 files as the        empty.
TFv1Real dataset.
                                                                              Results. As shown in Table 3, AdapTrack almost always out-
  Results. As shown in Table 2, AdapTrack performs signifi-                 performs constrained decoding, with an improvement of
cantly better than constrained decoding for all models, with                pass@1 up to 7.84% on HumanEval and 6.42% on MBPP, com-
an improvement up to 38.93%.                                                pared to constrained decoding, indicating that distortion also
AdapTrack: Constrained Decoding without Distorting LLM’s Output Intent                                   Conference acronym ’XX, June 03–05, 2018, Woodstock, NY


                                      Table 3: Pass@𝑘 on general-purpose code generation benchmarks.

                                                          HumanEval                                                            MBPP
  Method                           pass@1      pass@3      pass@5 pass@10         pass@20       pass@1         pass@3        pass@5 pass@10         pass@20
  Qwen2.5 Coder 7B
  Unconstrained decoding           65.41%       63.05%      73.66%       84.36%    90.57%       66.92%         72.28%        79.10%      85.04%       88.72%
  Constrained decoding             64.15%       70.66%      79.00%       86.08%    89.31%       66.67%         75.13%        80.60%      85.56%       88.46%
  AdapTrack (Ours)                 69.18%       72.22%      79.98%       86.65%    92.45%       70.77%         76.26%        81.55%      86.59%       89.74%
  DeepSeek Coder Base 6.7B
  Unconstrained decoding           44.65%       46.52%      56.26%       68.23%    77.36%       36.41%         65.62%        73.77%      81.17%       85.38%
  Constrained decoding             47.17%       51.88%      60.36%       70.00%    78.62%       60.00%         67.87%        74.26%      80.24%       84.10%
  AdapTrack (Ours)                 49.69%       55.43%      63.84%       73.16%    80.50%       63.85%         70.29%        76.54%      82.26%       85.90%
  StarCoder2 7B
  Unconstrained decoding           37.74%       28.00%      35.79%       46.85%    57.86%       56.67%         45.94%        55.72%      66.36%       74.36%
  Constrained decoding             37.11%       37.67%      46.35%       58.18%    68.55%       52.05%         57.43%        65.09%      73.17%       78.72%
  AdapTrack (Ours)                 37.74%       40.72%      49.62%       60.75%    69.18%       54.36%         58.60%        66.17%      74.33%       80.51%
  CodeLlama 7B
  Unconstrained decoding           33.96%       32.15%      39.50%       49.89%    61.64%       48.72%         45.68%        54.57%      64.42%       71.54%
  Constrained decoding             34.59%       35.19%      42.62%       53.43%    65.41%       45.90%         52.25%        60.19%      68.89%       75.64%
  AdapTrack (Ours)                 36.48%       35.89%      43.41%       53.89%    64.15%       47.69%         53.26%        61.25%      70.34%       77.18%


widely happens to constrained decoding in general code gen-                          The CP (constituency parsing) dataset contains 6 problems of
eration, which can be fixed by AdapTrack to improve the per-                      constituency parsing[12], i.e., to generate the constituency parse
formance. The only outlier is pass@20 of CodeLlama 7B on Hu-                      trees from English sentences. The constrains are used to make sure
manEval.                                                                          that the parentheses in the generated sequence are well-paired.
   When compared to unconstrained decoding, AdapTrack some-                          The binary dataset [27] is specifically designed to demonstrate
times performs worse (pass@1 of StarCoder2 7B and CodeLlama 7B                    this problem. There is only one problem in this dataset that asks the
on MBPP). This is due to the constrainer’s limitation. Note that                  model to generate a random sequence of 5 bits, but the constraint
pass@1 is calculated from the greedy samples. If the greedy samples               only allows 00000 and any 5-bit string that starts with 1. For a
of uncontrained decoding can pass the test, it should pass the con-               correctly constrained decoding method, the probability to generate
strainer and be greedily sampled by constrained decoding. However,                00000 should be roughly 1/17, because there are 17 valid samples,
in these cases, unconstrained decoding outperforms constrained                    and they should all have the same probability. But constrained
one. Nevertheless, AdapTrack can still improve the performance of                 decoding will give 00000 a much higher probability, roughly 1/2,
constrained decoding by fixing the distribution distortion.                       because in the first step, there are only 2 valid options, i.e., 0 and 1,
                                                                                  and their probabilities are roughly the same.
6.4     RQ4: Alignment between AdapTrack and                                         Metrics. Following previous work[27], for each problem in the
        the oracle distribution                                                   SLIA, INV-BV and CP datasets, we generate 2000 samples; for the
We have conducted experiments on both API completion and code                     binary dataset, we generate 100 samples. We use as metrics the
generation. Now we want to verify the statement that the distri-                  Kullback–Leibler (KL) divergence between the distribution formed
bution produced by AdapTrack aligns better with the oracle distri-                by the samples and the language model distribution. Lower the KL
bution, as an explanation of the previous results. Some previous                  divergence, the closer the two distributions. For any distribu-
work [27] also focuses on fixing the language model’s probability                 tion 𝑄 that only contains constrained samples, the KL divergence
in constrained decoding, so we follow their work and duplicate                    between 𝑄 and 𝑃LM reflects the KL divergence between 𝑄 and
their experiments on AdapTrack in RQ4.                                            𝑃 (·|𝑐).

   Datasets. Following previous work [27], we use 4 datasets in
                                                                                                          ∑︁                  𝑄 (𝑠)     ∑︁             𝑄 (𝑠)
                                                                                    𝐷 KL (𝑄 ∥𝑃 (·|𝑐)) =          𝑄 (𝑠) log            =    𝑄 (𝑠) log          ,
domain-specific languages.                                                                                 𝑠
                                                                                                                             𝑃 (𝑠 |𝑐)    𝑠
                                                                                                                                                     𝑃LM (𝑠)𝑍
   The SLIA (strings with linear integer arithmetic) dataset and                                ∑︁                𝑄 (𝑠)
the INV-BV (loop invariant generation with bit-vector arithmetic)                           =        𝑄 (𝑠) log           − log 𝑍 = 𝐷 KL (𝑄 ∥𝑃LM ) − log 𝑍,
                                                                                                𝑠
                                                                                                                 𝑃LM (𝑠)
dataset each contain 15 problems from the Syntax-Guided Synthesis
(SyGuS) problems [5]. Given the grammar and specification of a                    where 𝑍 is the normalizing constant in 𝑃 (·|𝑐).
domain-specific language, the goal is to generate a function that                   It should be noted that these metrics are only meaningful when
satisfies the specification using the given grammar. Each problem                 compared with results on the same problem because an identical
comes with its own grammar and logical specification, provided to                 unknown constant log 𝑍 has been added to all of them.
the model in the prompt. Each prompt also contains 3 in-context                     For each question, we calculate the average KL divergence be-
examples in the form of (Problem, Solution) pairs.                                tween all the samples and the language model. We also present
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                                                                    Yongmin Li, Jia Li, Ge Li, and Zhi Jin


the average KL divergence of the four datasets, weighted by the         KL divergence between the distribution formed by the 𝑥th to the
number of problems in each dataset.                                     (𝑛 + 𝑥)th samples and the model distribution.
   To see how each method converges to the oracle distribution,             With more and more information stored in 𝑄, decoding
we also calculate the KL divergence between a sliding window of         results of AdapTrack become better and better. On the SLIA,
𝑛 samples and the language model, where 𝑛 is one-fourth of the          CP and binary dataset, AdapTrack has a low KL divergence from the
sampling size for each problem.                                         start and continues to be low for the entire generation, indicating
                                                                        that AdapTrack has already found a good distribution from the
   Baselines. We compare with two baselines, constrained decoding
                                                                        first one-fourth samples. On the INV-BV dataset, the KL divergence
(CD) and Adaptive Sampling with Approximate Expected Futures
                                                                        of AdapTrack declines greatly, indicating that AdapTrack is still
(ASAp) [27]. ASAp can be regarded as a variant of AdapTrack,
                                                                        learning new things in repeated sampling.
where after sampling a sequence from 𝑃𝑄 , instead of backtracking
and adjusting all the previous sampling results, it just continues to   7 Discussion
use the current partially generated prefix. It uses the information
collected in 𝑄 only in the later samples on the same problem. To        7.1 Robustness analysis
match its behavior, we also share the estimation data 𝑄 between         7.1.1 Temperature. Performance of decoding method often de-
different generations; only the sample data 𝑁 is updated for a new      pends on the sampling temperature. In previous RQs, the tempera-
sample.                                                                 ture is always 1. Therefore, we conduct experiments to see how the
                                                                        performance of AdapTrack changes with different sampling tem-
  Implementation. We reuse ASAp code to replicate their settings
                                                                        peratures, i.e. 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9. The experiments
and the same transformers-CFG[12] library for the constrainer.
                                                                        are conducted with best-performing models on TFv1 and TFv1Real,
  Models. Following previous work[27], we use the Mistral-7B[17]        i.e. CodeLlama Python 7B and Qwen2.5 Coder 7B, respecitively.
model for all decoding algorithms.
                                                                                  EM@20                                               EM@20                                       0.7      EM@20
                                                                        0.95      EM@10                                      0.8      EM@10                                                EM@10
                                                                                  EM@5                                                EM@5                                                 EM@5
                                                                        0.90      EM@3                                       0.7      EM@3                                                 EM@3
                                                                                  EM@1                                                EM@1                                        0.6      EM@1
Table 4: Comparison of KL divergence of different methods               0.85                                                 0.6
                                                                                                                                                                                  0.5
                                                                        0.80                                                 0.5
on DSL datasets. CD means constrained decoding.                         0.75                                                 0.4                                                  0.4
                                                                        0.70                                                 0.3
                                                                        0.65                                                                                AdapTrack             0.3                           AdapTrack
                                                                                                       AdapTrack             0.2
                                                                                                       Constrained                                          Constrained                                         Constrained
                                                                        0.60                           Unconstrained                                        Unconstrained                                       Unconstrained
                                                                                                                             0.1                                                  0.2
                                  KL-divergence (↓)                         0.0      0.2   0.4   0.6   0.8             1.0      0.0      0.2   0.4   0.6    0.8             1.0      0.0      0.2   0.4   0.6   0.8             1.0


    Method          SLIA     INV-BV      CP binary        average         (a) TFv1 (v1 setting)                                (b) TFv1 (v2 setting)                                         (c) TFv1Real
    CD              11.37       7.13 19.86      23.05       11.46
    ASAp            12.05       7.76 19.85      19.87       11.90
                                                                               Figure 5: The change of EM@𝑘 in different temperature.
    AdapTrack        9.31       7.04 16.86 19.53             9.97
                                                                           As shown in figure 5, under temperatures from 0.0 to 1.0, for
                                                                        EM@𝑘 where 𝑘 ∈ {1, 3, 5, 10, 20}, AdapTrack always outperforms
   Results. As shown in Table 4, in all four datasets, AdapTrack
                                                                        both constrained and unconstrained decoding. As the temperature
performs significantly better than both constrained decoding
                                                                        increases, the performance of all methods increases, because ap-
and ASAp. In both the SLIA and CP datasets, constrained decod-
                                                                        propriately higher temperature encourages the model to explore
ing and ASAp perform roughly the same, while AdapTrack has a
                                                                        answers in a larger range, and EM@𝑘 is 1 if any of the 𝑘 attempts
large advantage. In the INV-BV dataset, all three methods perform
                                                                        hits the correct answer, except for EM@1, where greedy sampling
roughly the same. This might indicate that the portion of illegal
                                                                        always gives the same result.
tokens on different tokens in this dataset is roughly the same, so
constrained decoding can perform roughly the same as AdapTrack.         7.1.2 Model size. Performance of decoding method often depends
The binary dataset is the only dataset where ASAp performs much         on the model size. Some methods only work with small models or
better than constrained decoding, while AdapTrack still has some        large models. In previous RQs, we always experiment with models
advantage over ASAp.                                                    sized roughly 7B. Therefore, we conduct experiments to see how the
                                                                        performance of AdapTrack changes with differently sized models.
                                                                        The experiments are conducted with Qwen2.5 Coder series (0.5B,
                                                                        1.5B, 3B, 7B, 14B, 32B) on TFv1 and TFv1Real datasets, because
                                                                        Qwen2.5 Coder series provide a balanced and various range of
                                                                        choices for model sizes. To reduce needed GPU memory, for models
                                                                        larger than 7B, we use the bfloat16 format during inference.
    (a) SLIA          (b) INV-BV             (c) CP       (d) Binary
                                                                           As shown in figure 6, under all different model sizes, on both
                                                                        TFv1 and TFv1Real datasets, AdapTrack always outperforms both
Figure 4: The change of KL divergence (↓) between every 500             constrained decoding and unconstrained decoding. As the model
samples and the oracle distribution on different datasets.              size increases, the performance of all methods on TFv1 is saturated
                                                                        or even decreases after a certain threshold. One possible reason is
   Figure 4 shows how the KL divergence evolves in repeated sam-        that TFv1 is synthetic and too simple, so the difference in model
pling. The point with the abscissa 𝑥 in the figure represents the       size does not influence the result. As the model size increases, all
AdapTrack: Constrained Decoding without Distorting LLM’s Output Intent                                                                                                                             Conference acronym ’XX, June 03–05, 2018, Woodstock, NY

1.0                                                                                                           0.8
             EM@20
             EM@10
             EM@5                                      0.8
                                                                    EM@20
                                                                    EM@10
                                                                    EM@5                                      0.7
                                                                                                                           EM@20
                                                                                                                           EM@10
                                                                                                                           EM@5
                                                                                                                                                                                Table 5: Numbers of calls to language model in RQ1.
0.9          EM@3                                                   EM@3                                                   EM@3
             EM@1                                                   EM@1                                      0.6          EM@1
                                                       0.6
0.8                                                                                                           0.5

                                                       0.4                                                    0.4                                                                                                                   calls to LM (↓)
0.7                                                                                                           0.3
                                                       0.2
                                                                                                              0.2
                                                                                                                                                                                                                        TFv1 (v1 settings) TFv1 (v2 settings)
                                       AdapTrack                                              AdapTrack                                              AdapTrack
0.6                                    Constrained                                            Constrained                                            Constrained
                                       Unconstrained
                                                       0.0
                                                                                              Unconstrained   0.1                                    Unconstrained      Method                                            avg (min, max)       avg (min, max)
      0.5B           1.5B   3B   7B   14B       32B          0.5B           1.5B   3B   7B   14B       32B          0.5B           1.5B   3B   7B   14B       32B
                                                                                                                                                                        Qwen2.5 Coder 7B
  (a) TFv1 (v1 setting)                                  (b) TFv1 (v2 setting)                                               (c) TFv1Real                               Unconstrained decoding                                5.85 (4.12, 8.47)                5.85 (4.12, 8.47)
                                                                                                                                                                        Constrained decoding                                  4.64 (2.75, 6.07)                5.04 (2.91, 7.82)
Figure 6: The change of EM@𝑘 for differently-sized models.                                                                                                              AdapTrack (Ours)                                      5.56 (4.12, 7.42)               7.94 (4.41, 11.73)
                                                                                                                                                                        DeepSeek Coder Base 6.7B
                                                                                                                                                                        Unconstrained decoding                          10.36 (6.32, 15.59)                  10.36 (6.32, 15.59)
methods’ performance on TFv1Real increases, indicating larger                                                                                                           Constrained decoding                             8.27 (4.93, 11.43)                   8.82 (4.74, 14.40)
models’ better understanding in API completion.                                                                                                                         AdapTrack (Ours)                                 9.85 (6.24, 11.37)                  13.90 (6.70, 22.87)
                                                                                                                                                                        StarCoder2 7B
7.2                  Efficiency and scalability of AdapTrack                                                                                                            Unconstrained decoding                           9.11 (5.75, 13.65)                   9.11 (5.75, 13.65)
One might concern the efficiency and scalability of AdapTrack from                                                                                                      Constrained decoding                             7.62 (4.47, 10.03)                   7.70 (4.33, 12.50)
two perspectives: (1) updating 𝑄 and 𝑁 from step 10 to step 19 in                                                                                                       AdapTrack (Ours)                                 8.83 (5.93, 12.60)                  12.08 (5.47, 20.32)
algorithm 2 can be inefficient; (2) AdapTrack may need too much                                                                                                         CodeLlama Python 7B
time before generating a complete sequence.                                                                                                                             Unconstrained decoding                          10.68 (7.56, 12.90)                  10.68 (7.56, 12.90)
7.2.1 Parallel update. The update of 𝑄 and 𝑁 can be parallelized                                                                                                        Constrained decoding                             8.41 (5.38, 10.75)                   9.73 (5.88, 14.02)
on GPU, rather than performed token by token. If 𝑄 [𝑥] is updated                                                                                                       AdapTrack (Ours)                                10.03 (7.36, 13.45)                  14.29 (8.81, 20.25)
from 1 to 𝑞, where 𝑥 becomes an old prefix during the update, if
𝑥 = Concat(𝑠, 𝑥 ′ ), following formula can be used to update 𝑄 [𝑠],                                                                                                  0.95                                 0.8                                    0.70

                                                                                                                                                                     0.90                                 0.7                                    0.65
                                                                                             ′
                                      𝑄 [𝑠] ← 𝑄 [𝑠] − 𝑃LM (𝑥 |𝑠)(1 − 𝑞),                                                                                             0.85                                 0.6
                                                                                                                                                                                                                                                 0.60

                                                                                                                                                                                                                                                 0.55
                                                                                                                                                                     0.80                                 0.5
                                                                                                                                                                                                                                                 0.50
where 𝑃LM (𝑥 ′ |𝑠) can be computed in parallel for all prefix 𝑠 of 𝑥.It is                                                                                           0.75                         EM@1
                                                                                                                                                                                                  EM@3
                                                                                                                                                                                                          0.4
                                                                                                                                                                                                                                         EM@1
                                                                                                                                                                                                                                         EM@3
                                                                                                                                                                                                                                                 0.45                         EM@1
                                                                                                                                                                                                                                                                              EM@3
                                                                                                                                                                     0.70                         EM@5    0.3                            EM@5    0.40                         EM@5
then natural to compute the updated 𝑃𝑄 (·|𝑠) in parallel, and perform                                                                                                0.65
                                                                                                                                                                                                  EM@10
                                                                                                                                                                                                  EM@20   0.2
                                                                                                                                                                                                                                         EM@10
                                                                                                                                                                                                                                         EM@20   0.35
                                                                                                                                                                                                                                                                              EM@10
                                                                                                                                                                                                                                                                              EM@20
                                                                                                                                                                            0     1   2   4   8                 0   1     2     4    8                  0     1   2   4   8
the rejection sampling needed. It should be noted that the rejection
sampling and the sampling after rejection can also be fused into                                                                                                       (a) TFv1 (v1 setting)                (b) TFv1 (v2 setting)                           (c) TFv1Real
one sampling, further reducing branching in the calculation.
                                                                                                                                                                     Figure 7: The change of EM@𝑘 with different maximum
7.2.2 Number of LM calls. The most computationally intensive
                                                                                                                                                                     backtrack distance.
part of the decoding process is the invocation of the language
model. We count the number of calls to the language model per
sample in the RQ1 experiments, as shown in Table 5. In the Tensor-                                                                                                   a short backtracking distance is enough for most of AdapTrack’s
Flow v1 setting, AdapTrack invokes the language model on average                                                                                                     performance.
20% more frequently than constrained decoding, whereas, in the
TensorFlow v2 setting, this number rises to an average of 60% more                                                                                                   7.3          Threats to validity
calls than constrained decoding. Similar numbers also apply to
                                                                                                                                                                     7.3.1 Dataset selection. The first threat lies in the selection of
the averaged maximum number of calls to LM. Considering that
                                                                                                                                                                     dataset: Does this problem of constrained decoding happen only
EM@1 of AdapTrack is often comparable to EM@5 of constrained
                                                                                                                                                                     in deprecated APIs or only in API completion? We mitigate this
decoding, this level of increase in the number of invocations can
                                                                                                                                                                     threat by experiments in RQ1 where we ask the model to gener-
be justified.
                                                                                                                                                                     ate a TensorFlow v1 API in a TensorFlow v1 setting, where these
   If theoretical completeness is sacrificed, we can take additional
                                                                                                                                                                     APIs are not considered deprecated, which can be fixed by Adap-
constraints on AdapTrack to avoid extremely long backtracking dis-
                                                                                                                                                                     Track to provide significant improvement. Experiments on general
tances. For example, a lower bound can be set for the backtracking
                                                                                                                                                                     code generation benchmarks in RQ3 show that such distortion also
probability, prohibiting backtracking if the probability falls below
                                                                                                                                                                     happens in general code generation, and AdapTrack can provide
this threshold. An upper limit can also be set for the backtracking
                                                                                                                                                                     performance improvement by fixing such distortion.
distance, disallowing backtracking beyond this specified maximum.
   In particular, as shown in Figure 7, we conduct experiments with                                                                                                  7.3.2 Model selection. The second threat lies in the selection of
limited backtracking distances (including 1, 2, 4, 8) with CodeLlama                                                                                                 the models: Is this issue due to the limitation in model’s capability?
Python 7B on TFv1 and Qwen2.5 Coder 7B on TFv1Real, respec-                                                                                                          We mitigate this threat by using multiple models in experiments,
tively. For both models and datasets, the performance increases as                                                                                                   and using differently-sized models in robustness analysis. Although
the allowed backtracking distance increases, but stops increasing                                                                                                    they have different capabilities, AdapTrack shows a consistent im-
after a certain threshold. From the figure, we can see that a back-                                                                                                  provement. It should be noted that this is an inherent problem of
tracking distance of 2 or 4 is roughly enough for TFv1 (v1 settings),                                                                                                constrained decoding. As long as constrained decoding is employed,
4 or 8 for TFv1 (v2 settings), and 2 for TFv1Real. This indicates that                                                                                               the problem will persist to some extent.
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                                  Yongmin Li, Jia Li, Ge Li, and Zhi Jin


8 Related work                                                           9    Conclusion and future work
8.1 API-aware code generation                                            In this work, we propose a new decoding method, AdapTrack, to
                                                                         fix the distribution distortion problem in constrained decoding by
APIs evolve over time, and code LLMs need to handle that. CERT[38]
                                                                         introducing backtracking that is adaptive to the invalidated prob-
introduces a sketcher to predict the sketch of API usage, and then
                                                                         ability mass into the generation process. We collect two datasets,
uses a generator to use the API in the relevant context. Toolcoder[39]
                                                                         the synthetic TFv1 dataset and the real-world TFv1Real dataset to
introduces an API search tool to help the model search for wanted
                                                                         verify the effectiveness of AdapTrack. Experiments on general code
APIs. Wang et al. [34] conduct the first evaluation study on the usage
                                                                         generation benchmarks verifies the generalizability of AdapTrack.
of deprecated APIs in LLM-based code completion. VersiCode[37]
                                                                         We give theoretical proof of our method that it does follow the out-
dataset focuses on version-specific code completion and version-
                                                                         put intent of the model and conduct experiments on DSL problems
aware code migration. CodeUpdateArena[24] dataset constructs
                                                                         to verify that.
synthetic API function update to evaluate LLM’s ability to handle
                                                                            In the future, we will explore this phenomenon on more APIs,
API update.
                                                                         and explore how to help the model align better with the constraints.

8.2     Constrained decoding in code generation
                                                                         Acknowledgments
Constrained decoding is a greedy method to ensure the generated
                                                                         This research is supported by the National Key R&D Program under
sequence statisfy certain constraints. Picard [32] and Synchromesh
                                                                         Grant No. 2023YFB4503801, the National Natural Science Founda-
[29] introduce incremental parser into code generation to help
                                                                         tion of China under Grant No. 62192733, 62192730, 62192731, and
the model reject inadmissible tokens at each decoding step. Later
                                                                         the Major Program (JD) of Hubei Province (No.2023BAA024).
grammar-based constrainers [8, 11, 21, 28] focus on the acceleration
of constraint calculation. Monitor-guided decoding [3] and Repilot
[35] introduce constrained decoding in the generation of general-        References
purpose programming languages, by communicating with static               [1] Martín Abadi, Ashish Agarwal, Paul Barham, Eugene Brevdo, Zhifeng Chen,
analysis tools in IDEs, e.g., language servers in Visual Studio Code,         Craig Citro, Greg S. Corrado, Andy Davis, Jeffrey Dean, Matthieu Devin, San-
                                                                              jay Ghemawat, Ian Goodfellow, Andrew Harp, Geoffrey Irving, Michael Isard,
to collect information about the whole repository to help API gen-            Yangqing Jia, Rafal Jozefowicz, Lukasz Kaiser, Manjunath Kudlur, Josh Levenberg,
eration. Mündler et al. [26] introduce type system into constrained           Dandelion Mané, Rajat Monga, Sherry Moore, Derek Murray, Chris Olah, Mike
decoding, ensuring the generated program to be type-safe.                     Schuster, Jonathon Shlens, Benoit Steiner, Ilya Sutskever, Kunal Talwar, Paul
                                                                              Tucker, Vincent Vanhoucke, Vijay Vasudevan, Fernanda Viégas, Oriol Vinyals,
                                                                              Pete Warden, Martin Wattenberg, Martin Wicke, Yuan Yu, and Xiaoqiang Zheng.
                                                                              2015. TensorFlow: Large-Scale Machine Learning on Heterogeneous Systems.
8.3     Fixing greedy constrained decoding                                    https://www.tensorflow.org/ Software available from tensorflow.org.
                                                                          [2] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Floren-
Naïve greedy constrained decoding is known to be problematic,                 cia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal
and there are some work trying to fix that. GeDi[22] introduces               Anadkat, et al. 2023. Gpt-4 technical report. arXiv preprint arXiv:2303.08774
another trained model to model the expected validity of each prefix,          (2023).
                                                                          [3] Lakshya A Agrawal, Aditya Kanade, Navin Goyal, Shuvendu Lahiri, and Sriram
but training another model is a large overhead. ASAp[27] samples              Rajamani. 2023. Monitor-guided decoding of code lms with static analysis of
multiple sequences from the language model and use the validity               repository context. Advances in Neural Information Processing Systems 36 (2023),
                                                                              32270–32298.
information from previous samples to direct future sampling. This         [4] Kareem Ahmed, Kai-Wei Chang, and Guy Van den Broeck. 2025. Control-
can be regarded as a variant of AdapTrack without backtracking.               lable Generation via Locally Constrained Resampling. In The Thirteenth Interna-
Gen-C[4] models the constraint with constraint circuits and resam-            tional Conference on Learning Representations. https://openreview.net/forum?id=
                                                                              8g4XgC8HPF
ples using the pseudolikelihood in the neighborhood of a sentence,        [5] Rajeev Alur, Dana Fisman, Saswat Padhi, Rishabh Singh, and Abhishek Udupa.
but constraint circuits are only constructible for regular expressions        2019. Sygus-comp 2018: Results and analysis. arXiv preprint arXiv:1904.07146
and, therefore, unsuitable for code generation.                               (2019).
                                                                          [6] Jason Ansel, Edward Yang, Horace He, Natalia Gimelshein, Animesh Jain, Michael
                                                                              Voznesensky, Bin Bao, Peter Bell, David Berard, Evgeni Burovski, et al. 2024.
                                                                              Pytorch 2: Faster machine learning through dynamic python bytecode trans-
8.4     Non-linear code generation techniques                                 formation and graph compilation. In Proceedings of the 29th ACM International
                                                                              Conference on Architectural Support for Programming Languages and Operating
Non-linear code generation techniques is not unheard of. PG-TD                Systems, Volume 2. 929–947.
[40] uses Monte-Carlo tree search, and executes public test cases to      [7] Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk
determine the quality of generated code. Rocode [19] detects errors           Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le,
                                                                              et al. 2021. Program synthesis with large language models. arXiv preprint
after generating every statement by running static analysis tools             arXiv:2108.07732 (2021).
and executing public test cases, and rollbacks to the statement of the    [8] Luca Beurer-Kellner, Marc Fischer, and Martin Vechev. 2024. Guiding LLMs The
error report or earlier statements with high generation uncertainty.          Right Way: Fast, Non-Invasive Constrained Generation. In Forty-first International
                                                                              Conference on Machine Learning. https://openreview.net/forum?id=pXaEYzrFae
However, these methods are not designed to address distribution           [9] Federico Cassano, John Gouwar, Daniel Nguyen, Sydney Nguyen, Luna Phipps-
distortion and consequently still produce distorted distributions,            Costin, Donald Pinckney, Ming-Ho Yee, Yangtian Zi, Carolyn Jane Anderson,
                                                                              Molly Q Feldman, et al. 2023. Multipl-e: A scalable and polyglot approach to
while AdapTrack specifically targets this issue and provides prov-            benchmarking neural code generation. IEEE Transactions on Software Engineering
ably undistorted results. These methods often use public test cases           49, 7 (2023), 3675–3691.
to filter out incorrect programs, but, while possible, similar pro-      [10] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde
                                                                              De Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph,
cedure is not executed in AdapTrack, because AdapTrack focuses                Greg Brockman, et al. 2021. Evaluating large language models trained on code.
more on the distribution distortion problem.                                  arXiv preprint arXiv:2107.03374 (2021).
AdapTrack: Constrained Decoding without Distorting LLM’s Output Intent                                            Conference acronym ’XX, June 03–05, 2018, Woodstock, NY


[11] Yixin Dong, Charlie F Ruan, Yaxing Cai, Ruihang Lai, Ziyi Xu, Yilong Zhao, and           Scott Wen-tau Yih (Eds.). Association for Computational Linguistics, Online
     Tianqi Chen. 2024. Xgrammar: Flexible and efficient structured generation engine         and Punta Cana, Dominican Republic, 9895–9901. doi:10.18653/v1/2021.emnlp-
     for large language models. Proceedings of Machine Learning and Systems 7 (2024).         main.779
[12] Saibo Geng, Martin Josifoski, Maxime Peyrard, and Robert West. 2023. Grammar-       [33] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,
     Constrained Decoding for Structured NLP Tasks without Finetuning. In Proceed-            Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all
     ings of the 2023 Conference on Empirical Methods in Natural Language Processing,         you need. Advances in neural information processing systems 30 (2017).
     Houda Bouamor, Juan Pino, and Kalika Bali (Eds.). Association for Computational     [34] Chong Wang, Kaifeng Huang, Jian Zhang, Yebo Feng, Lyuye Zhang, Yang Liu,
     Linguistics, Singapore, 10932–10952. doi:10.18653/v1/2023.emnlp-main.674                 and Xin Peng. 2025. LLMs Meet Library Evolution: Evaluating Deprecated
[13] GitHub. 2023. GitHub Copilot. https://github.com/features/copilot.                       API Usage in LLM-based Code Completion. arXiv:2406.09834 [cs.SE] https:
[14] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang,                    //arxiv.org/abs/2406.09834
     Guanting Chen, Xiao Bi, Yu Wu, YK Li, et al. 2024. DeepSeek-Coder: When the         [35] Yuxiang Wei, Chunqiu Steven Xia, and Lingming Zhang. 2023. Copiloting the
     Large Language Model Meets Programming–The Rise of Code Intelligence. arXiv              copilots: Fusing large language models with completion engines for automated
     preprint arXiv:2401.14196 (2024).                                                        program repair. In Proceedings of the 31st ACM Joint European Software Engi-
[15] Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, and Yejin Choi. 2020. The                 neering Conference and Symposium on the Foundations of Software Engineering.
     Curious Case of Neural Text Degeneration. In International Conference on Learning        172–184.
     Representations. https://openreview.net/forum?id=rygGQyrFvH                         [36] Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue,
[16] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu            Anthony Moi, Pierric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, et al.
     Liu, Jiajun Zhang, Bowen Yu, Keming Lu, et al. 2024. Qwen2. 5-coder technical            2020. Transformers: State-of-the-art natural language processing. In Proceedings
     report. arXiv preprint arXiv:2409.12186 (2024).                                          of the 2020 conference on empirical methods in natural language processing: system
[17] Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, De-               demonstrations. 38–45.
     vendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel,         [37] Tongtong Wu, Weigang Wu, Xingyu Wang, Kang Xu, Suyu Ma, Bo Jiang, Ping
     Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux,              Yang, Zhenchang Xing, Yuan-Fang Li, and Gholamreza Haffari. 2024. VersiCode:
     Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix,              Towards Version-controllable Code Generation. arXiv:2406.07411 [cs.SE] https:
     and William El Sayed. 2023. Mistral 7B. arXiv:2310.06825 [cs.CL] https:                  //arxiv.org/abs/2406.07411
     //arxiv.org/abs/2310.06825                                                          [38] Daoguang Zan, Bei Chen, Dejian Yang, Zeqi Lin, Minsu Kim, Bei Guan, Yongji
[18] Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim. 2024. A survey          Wang, Weizhu Chen, and Jian-Guang Lou. 2022. CERT: Continual Pre-training on
     on large language models for code generation. arXiv preprint arXiv:2406.00515            Sketches for Library-oriented Code Generation. In Proceedings of the Thirty-First
     (2024).                                                                                  International Joint Conference on Artificial Intelligence, IJCAI-22, Lud De Raedt
[19] Xue Jiang, Yihong Dong, Yongding Tao, Huanyu Liu, Zhi Jin, and Ge Li. 2025.              (Ed.). International Joint Conferences on Artificial Intelligence Organization,
     ROCODE: Integrating Backtracking Mechanism and Program Analysis in Large                 2369–2375. doi:10.24963/ijcai.2022/329 Main Track.
     Language Models for Code Generation. In 2025 IEEE/ACM 47th International            [39] Kechi Zhang, Huangzhao Zhang, Ge Li, Jia Li, Zhuo Li, and Zhi Jin. 2023. Tool-
     Conference on Software Engineering (ICSE). 334–346. doi:10.1109/ICSE55347.2025.          coder: Teach code generation models to use api search tools. arXiv preprint
     00133                                                                                    arXiv:2305.04032 (2023).
[20] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press,   [40] Shun Zhang, Zhenfang Chen, Yikang Shen, Mingyu Ding, Joshua B. Tenenbaum,
     and Karthik R Narasimhan. 2024. SWE-bench: Can Language Models Resolve                   and Chuang Gan. 2023. Planning with Large Language Models for Code Gen-
     Real-world Github Issues?. In The Twelfth International Conference on Learning           eration. In The Eleventh International Conference on Learning Representations.
     Representations. https://openreview.net/forum?id=VTF8yNQM66                              https://openreview.net/forum?id=Lr8cOOtYbfL
[21] Terry Koo, Frederick Liu, and Luheng He. 2024. Automata-based constraints
     for language model decoding. In First Conference on Language Modeling. https:       Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009
     //openreview.net/forum?id=BDBdblmyzY
[22] Ben Krause, Akhilesh Deepak Gotmare, Bryan McCann, Nitish Shirish Keskar,
     Shafiq Joty, richard socher, and Nazneen Rajani. 2021. GeDi: Generative Dis-
     criminator Guided Sequence Generation. https://openreview.net/forum?id=
     TJSOfuZEd1B
[23] Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi
     Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, et al. 2022.
     Competition-level code generation with alphacode. Science 378, 6624 (2022),
     1092–1097.
[24] Zeyu Leo Liu, Shrey Pandit, Xi Ye, Eunsol Choi, and Greg Durrett.
     2025. CodeUpdateArena: Benchmarking Knowledge Editing on API Updates.
     arXiv:2407.06249 [cs.CL] https://arxiv.org/abs/2407.06249
[25] Anton Lozhkov, Raymond Li, Loubna Ben Allal, Federico Cassano, Joel Lamy-
     Poirier, Nouamane Tazi, Ao Tang, Dmytro Pykhtar, Jiawei Liu, Yuxiang Wei,
     et al. 2024. Starcoder 2 and the stack v2: The next generation. arXiv preprint
     arXiv:2402.19173 (2024).
[26] Niels Mündler, Jingxuan He, Hao Wang, Koushik Sen, Dawn Song, and Mar-
     tin Vechev. 2025. Type-Constrained Code Generation with Language Models.
     Proceedings of the ACM on Programming Languages 9, PLDI (2025), 601–626.
[27] Kanghee Park, Jiayu Wang, Taylor Berg-Kirkpatrick, Nadia Polikarpova, and Loris
     D’Antoni. 2024. Grammar-aligned decoding. Advances in Neural Information
     Processing Systems 37 (2024), 24547–24568.
[28] Kanghee Park, Timothy Zhou, and Loris D’Antoni. 2025. Flexible and Efficient
     Grammar-Constrained Decoding. In Forty-second International Conference on
     Machine Learning. https://openreview.net/forum?id=L6CYAzpO1k
[29] Gabriel Poesia, Alex Polozov, Vu Le, Ashish Tiwari, Gustavo Soares, Christopher
     Meek, and Sumit Gulwani. 2022. Synchromesh: Reliable Code Generation from
     Pre-trained Language Models. In International Conference on Learning Represen-
     tations. https://openreview.net/forum?id=KmtVD97J43e
[30] Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever, et al. 2018.
     Improving language understanding by generative pre-training. (2018).
[31] Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiao-
     qing Ellen Tan, Yossi Adi, Jingyu Liu, Romain Sauvestre, Tal Remez, et al. 2023.
     Code llama: Open foundation models for code. arXiv preprint arXiv:2308.12950
     (2023).
[32] Torsten Scholak, Nathan Schucher, and Dzmitry Bahdanau. 2021. PICARD:
     Parsing Incrementally for Constrained Auto-Regressive Decoding from Language
     Models. In Proceedings of the 2021 Conference on Empirical Methods in Natural
     Language Processing, Marie-Francine Moens, Xuanjing Huang, Lucia Specia, and
