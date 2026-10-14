                                         Reasoning in Transformers – Mitigating Spurious
                                              Correlations and Reasoning Shortcuts

                                                    Daniel Enström1 , Viktor Kjellberg1 , and Moa Johansson2
                                                          1
                                                           University of Gothenburg, Gothenburg, Sweden.
                                                             {gusensda, guskjevia}@student.gu.se
arXiv:2403.11314v1 [cs.LG] 17 Mar 2024




                                                     2
                                                       Chalmers University of Technology, Gothenburg, Sweden.
                                                                   moa.johansson@chalmers.se



                                               Abstract. Transformer language models are neural networks used for a
                                               wide variety of tasks concerning natural language, including some that
                                               also require logical reasoning. However, a transformer model may eas-
                                               ily learn spurious patterns in the data, short-circuiting actual reason-
                                               ing. In this paper we investigate to what extent transformers can be
                                               trained to a) approximate reasoning in propositional logic while b) avoid-
                                               ing known reasoning shortcuts via spurious correlations in the training
                                               data. To do so, we use a dataset with known spurious correlation be-
                                               tween truth and e.g. the number of rules in the problem. We augment
                                               the data with proofs, and train two models: a generative transformer,
                                               WP-BART, trained on problems and their whole proofs, and a neuro-
                                               symbolic model, SIP-BART, trained on individual proof steps and com-
                                               bining the generative transformer model BART with a symbolic proof
                                               checker. We find that SIP-BART succeeds in avoiding reasoning short-
                                               cuts, while WP-BART does not. For SIP-BART, we then identify a few
                                               remaining reasoning errors, not previously described in the literature,
                                               arising from using a pre-trained language model. These are qualitatively
                                               analysed to create a taxonomy of four different types of additional pit-
                                               falls.


                                         1   Introduction

                                         Transformer models [22], have successfully been applied to a range of tasks in
                                         natural language processing [1,16], including those that requires the model to
                                         approximate reasoning [17]. It is generally acknowledged that inducing large lan-
                                         guage models to reason step by step improves their results on reasoning tasks in
                                         natural language and when solving maths problems [8,12,10,15,23]. We are inter-
                                         ested in understanding how and why step-by-step reasoning helps transformers
                                         solve logic problems. Does it help the model avoid learning spurious patterns
                                         and instead learn to better approximate actual reasoning?
                                             In this study, we consider problems in propositional logic, expressed in struc-
                                         tured natural language. We are not suggesting that transformer models are any-
                                         where near specialised solvers on problems in propositional logic, and this is not
                                         the purpose of this study. Rather, we are interested in the reasoning capabilities
2       Enström, Kjellberg and Johansson

(and pitfalls) of models processing primarily natural language, but also able to
do at least some reasoning on problems expressed in English. Transformers have
been reported to successfully having learnt to reason about the truth of these
types of logic queries, essentially by classifying the query as True or False [2,20].
However, it is not always clear if this emergent functionality corresponds to a
model really having learnt deductive reasoning, or if it is picking up on some
other pattern in the data. Zhang et al. [24], have experimentally shown that
transformers are susceptible to learning spurious patterns inherent to reasoning
problems, such as the number of rules in the problem description. With more
available rules, chances are bigger that at least some of them will apply to the
query and help prove it. So, it is not a bad heuristic for guessing if a query is true,
but it does not constitute logical reasoning as we know it. They demonstrate this
using a BERT classifier [4], trained on a dataset called SimpleLogic, consisting of
propositional reasoning problems expressed in natural language and divided into
subsets with different (spurious) statistical patterns correlating with the truth
of the query. The BERT model fails to generalise between subsets and they con-
clude that it is difficult to ensure that transformers really do learn to reason:
there are countless potential spurious patterns present in reasoning problems.
This lack of reliable deductive reasoning capabilities in large language models
has been argued to be a significant obstacle for their further development [21,5].
    We experiment with ways of addressing this problem: reasoning ought to be
robust also over data with spurious correlations between problem properties and
truth values. First, we augment the training data in SimpleLogic to include not
only a True/False label but also the proof steps generated by a standard forward
chaining algorithm. This leads to our first research question: (1) To what extent
can a generative transformer model avoid learning spurious correlation if trained
to also generate short proofs?
    Next, we also investigate a neuro-symbolic architechture more closely cou-
pling the transformer with a symbolic checker. Here, instead of training on the
whole proof at once, the generative neural model is trained to produce inter-
mediate inference steps, one at the time, which are iterated via a rule-based
symbolic system to update the proof state [18,19,3]. This leads to our second
research question: (2) Can a generative transformer model fully avoid learning
spurious correlations if train to generate only one proof step at the time?
    Previous work has showed that training on step-by-step reasoning should
improve accuracy on benchmarks, but no investigation has been made into the
errors still made by the model. For instance, it may also be the case that the
model correctly conclude a query being true/false, but still produce some faulty
proof-steps along the way. This leads to our third research question: (3) What
are the sources of other consistency errors and how can we avoid them?


2    Method

We first introduce our augmented dataset SimpleLogicPS (SimpleLogic with
Proof Steps), which extends the original SimpleLogic [24] with inference steps.
                  Mitigating Spurious Correlations and Reasoning Shortcuts         3

We then describe our models, one generative transformer trained to produce
whole proofs (WP-BART), and one neuro-symbolic model which combines a
generative model for selecting inferences, with a symbolic module for keeping
track of the proof state (SIP-BART). Finally, we describe our evaluation strategy.
Additional details regarding the models can be found in the MSc thesis of the
first two authors [6], and the code is available online.3

2.1    Data
The original SimpleLogic dataset [24], consists of 840 000 simple inference prob-
lems in propositional logic. Each problem consists of a set of rules, expressed
as Horn clauses with 1-3 premises, a set of facts (literals that are True) and
a query literal for which a truth value is to be determined. We operate under
a closed-world assumption, meaning that any query for which truth cannot be
derived from the existing rules and facts, is assumed to be False. The depth of
a problem refers to the minimum number of rule applications required to prove
the query. For False queries, the depth refers to the maximum depth of the
shallowest failing branch for that problem. See Appendix A for an illustration.
    SimpleLogic is divided into three sub-sets, equal in size, with different statis-
tical features. Each subset is divided with a 80-10-10 split for training, validation
and testing.
Rule-Priority (RP) problems were generated by first randomly generating
   rules, facts, and a query and then computing its label by forward chaining.
Label-Priority (LP) problems were generated in the opposite way as RP, i.e.
   first determining a query and its truth value and then randomly sampling
   rules and facts consistent with this.
For both RP and LP, Zhang et al. shows that the number of rules and facts, as
well as the branching factor of proofs are spurious statistical features correlated
with the truth value of the query [24]. They thus also introduce a third subset:
Balanced Rule-Priority (RP_b) is similar to RP but the correlation be-
   tween the number of rules and the boolean labels of queries has been re-
   moved.
   In the original SimpleLogic dataset, the target label is just the boolean truth
value of the query. To give the generative model increased guidance during train-
ing the dataset is augmented with proofs. We have thus extended all problems
with inference steps to allow the transformer to learn to identify the next infer-
ence rule to apply, rather than classifying the whole query as True or False at
once. The proof steps in SimpleLogicPS were generated using forward chaining
from known facts until the query was found (True queries), or until the search
space was exhausted (False queries).
   For the neuro-symbolic model, which we train on single proof steps, rather
than whole proofs, so each original problem was then divided into individual
3
    https://anonymous.4open.science/r/paradox_alvis-FF17/
4       Enström, Kjellberg and Johansson

proof steps. Each training data point thus consist of an input problem with an
applicable rule as desired output (or True or False if it represented the final
step). This resulted in a total of 3 986 165 proof step training instances. Three
such example instances along with a complete proof string can be found in figure
1.




Fig. 1: Example of how the generation procedure works. The three blue boxes
represent three instances of input strings in SimpleLogicPS and the white boxes
represent their respective output strings. The neural model thus regard each step
of the proof as an isolated problem to be solved, since each step is a separate
training instance. The complete proof string created by the model when inference
is finished for a given problem is represented by the purple box.




2.2   Model Design and Training
We experiment with two different models trained also on proof information. Both
are based on a pre-trained generative transformer model called BART [9], which
is similar in size to the BERT classifier used in [24]. BART can also generate
short text outputs, in our case a proof or proof step, not just a true/false answer.
For comparison, we also replicate the experiment by [24]: training BERT based
binary classifiers on each subset of SimpleLogic to produce a True/False label
for each problem.

Whole-Proof BART (WP-BART). The WP-BART model is trained to
generate the proof for the input problem as a string, ending in TRUE or FALSE.
                   Mitigating Spurious Correlations and Reasoning Shortcuts       5

It is trained on SimpleLogic proofs generated by a simple backward chaining
algorithm.


Symbolic Iterative Proof-BART (SIP-BART). The SIP-BART model
combines the neural BART-component with a symbolic module responsible for
updating the current state of the proof, see Figure 2.




Fig. 2: An overview of the SIP-BART architecture using an example of data-flow
during inference.


    The neural module is a pre-trained BART model which is fine-tuned to gener-
ate the next applicable rule for SimpleLogicPS-problems as an output, a boolean
string True when the proof is judged to be completed, or False when the search
space is judged to be exhausted and no more rules are applicable. The symbolic
module is responsible for applying the rule produced by the neural module, and
produce a new textual representation for the next proof step, which serves as the
next input to the neural model. Should the neural model produce a suggestion
of a rule which is in fact not applicable, the symbolic model records this faulty
step, but does not update the state, and asks the neural model to "try again".
This is however very rare, most generated steps are valid (see analysis of consis-
tency in §3.2). This iteration continues until the neural model outputs True or
False, or the number of iterations reaches a maximum threshold to avoid poten-
tial non-termination4 . The symbolic module then terminates the generation and
4
    This was set to 100 iterations, however in practice a much lower threshold could
    have been used, as non-applicable suggestions turned out to be rare.
6       Enström, Kjellberg and Johansson

outputs the final sequence of inference steps. If the system fails to return a chain
of inferences ending in True or False the result is treated as a False Positive or
False Negative depending on the ground truth label.


Training. We train one WP-BART/SIP-BART model for each subset of Sim-
pleLogic: LP, RP and RP_b. We denote the differently trained models by WP-
BART(LP)/SIP-BART(LP) etc. Each model was then evaluated on all subsets to
be able to analyse to what extent the models learned spurious correlations from
the data. The models were all trained for one epoch (as additional epochs did
not improve results) on four NVIDIA Tesla A40 GPUs. Refer to the Appendix
B for detailed information about training parameters and hardware.


2.3   Evaluation

Evaluation was performed in two stages. First, addressing research questions
1 and 2, we evaluate the correctness of the truth-value of the query. Here, we
compare the accuracy of the BERT replication with the final labels produced by
WP-BART and SIP-BART (disregarding the intermediate details of the proof).
    Secondly, to address our third research question, we analyse the sequence of
inferences produced of our best performing architecture above. Here, the sound-
ness and completeness of the inference steps were evaluated to check its con-
sistency. A proof with no validity issues or extra faulty steps and no missing
inference steps is regarded as consistent. We analyse the errors in inconsistent
proofs and identify four situations which give rise to inconsistencies:

Non-existing Rule (NonExR). Here, the neural model have suggested a rule
   which is not present in the problem description.
Inapplicable Rule (InappR). The neural model have suggested a rule which
   is present, but not applicable, as its premises are not satisfied (the relevant
   facts are not present in the problem description).
Spurious Match (SpMatch). Here, the neural model have produced the final
   output True to conclude the proof prematurely (the query is in fact not
   proved to be True yet - a spurious match with some other fact).
Unexhausted Search Space (UnexhS). The neural model have prematurely
   produced the final output False, while there are still rules available that
   would be applicable (the search space is not yet fully explored).


3     Results

3.1   Accuracy of Truth Values

We first assess the accuracy of the final labels (True or False) assigned to the
queries of each problem in the SimpleLogic test sets. The results of the replication
experiment of [24] are shown Table 1. We observe the same pattern in the data as
                    Mitigating Spurious Correlations and Reasoning Shortcuts          7

is described in their article5 - a BERT classifier trained on specific distributions
has a hard time generalizing to other distributions due to the model learning
statistical features rather than approximating reasoning. The model trained on
RP and RP_b generalised better to LP (total accuracy of 86.7 % and 87.5%
respectively) than LP to RP and RP_b (total accuracy of 75.0 % and 72.5%
respectively). Training on RP_b result in slightly better performance than on
RP. The accuracy also generally drops with increased proof-depth.


 TRAIN TEST        0        1       2        3       4        5       6        TOT
 LP    LP          99.8     99.8    99.8     99.6    98.8     97.2    95.4     98.6
 LP    RP          97.4     92.5    64.5     60.2    67.6     72.6    69.9     75.0
 LP    RP_b        97.7     93.3    60.2     56.7    63.9     68.7    68.5     72.7
 RP    LP          99.9     99.9    99.0     94.3    83.8     65.6    50.0     84.7
 RP    RP          99.8     100.0   99.4     98.9    98.6     96.9    95.9     98.5
 RP    RP_b        99.2     99.2    98.6     98.0    96.6     93.9    89.1     96.4
 RP_b LP           99.7     99.4    99.3     96.4    87.6     72.6    57.2     87.5
 RP_b RP           99.8     99.9    99.5     98.9    98.6     97.9    96.9     98.8
 RP_b RP_b         99.6     99.5    99.0     98.4    98.0     96.7    94.1     97.9
Table 1: Accuracy from the BERT-classifier replication of [24] trained on the
different distributions. The integers in the heading refer to the depth of the
ground-truth proof. TOT is the average accuracy across all proof depths. There
are roughly the same number of problems with proofs of each depth.




Accuracy of WP-BART. Table 2 shows accuracy for the WP-BART model. It
does not significantly improve overall compared to the baseline BART classifier.
While WP-BART(LP) appears to generalise slightly better, the other variants
perform worse. However, we also noticed that with increasing depth, the propor-
tion of false queries in the data increase. The WP-BART(LP) model appears to
have learned this as a reasoning shortcut, and over-predict the conclusion False,
which can be seen in as an increased rate of False Negatives with proof depth, see
Table 1 in Appendix C. We also note that the WP-BART(RP) model (trained
on data where the number of rules correlated with truth) does not generalise
as well as the model WP-BART(RP_b) (trained on balanced data), suggesting
that WP-BART is still prone to learn reasoning shortcut correlating the number
of rules and truth.

Accuracy of SIP-BART. The accuracy scores from the three SIP-BART mod-
els tested on all subsets are summarised in Table 3. There is a clear improve-
ment in accuracy when compared to the BERT classifier in Table 1. Additionally,
5
    As expected, despite using the same hyperparameter and seeds, we do not get exactly
    the same results. This is a know issue with neural network libraries and due to e.g.
    differences in hardware platforms used [14].
8      Enström, Kjellberg and Johansson

 TRAIN TEST      0       1       2        3      4       5       6       TOT
 LP    LP        100.    100.    92.6     90.2   89.8    91.2    93.3    93.9
 LP    RP        100.    99.9    83.3     65.5   67.3    72.0    76.5    80.6
 LP    RP_b      100.    99.9    82.1     64.9   66.3    74.0    83.0    81.4
 RP    LP        84.7    85.4    79.2     73.9   71.6    68.5    63.4    75.2
 RP    RP        84.3    88.5    87.9     87.6   85.0    79.8    78.1    84.5
 RP    RP_b      87.7    88.3    88.8     87.7   85.4    80.7    79.7    85.5
 RP_b LP         84.1    94.3    89.6     85.1   80.9    76.6    71.6    83.2
 RP_b RP         84.0    94.2    94.3     92.2   89.3    84.8    82.2    88.7
 RP_b RP_b       87.2    93.6    94.1     93.3   88.6    86.8    85.7    89.9
Table 2: Accuracy for the WP-BART models trained on the different distribu-
tions measured in percentage of correct predictions. The integers refer to the
depth of the ground-truth proof. TOT is the overall average accuracy across
proofs of all depths. There are roughly the same number of inference-problems
for each depth.



the SIP-BART models achieved an almost perfect accuracy on all three testing
sets, regardless of training set, with minimal or no drop as proof-depth increase.
The accuracy for SIP-BART(RP) and SIP-BART(RP_b) are equal, and slightly
better than SIP-BART(LP) which performs worse on proofs of increased depth.
Furthermore, no substantial over-prediction of conclusion False can be seen with
the increased proof depths for SIP-BART(LP), see Table 1 in Appendix D. This
indicates that, unlike the BERT classifier and WP-BART, SIP-BART has to a
much larger extent avoided learning the spurious patterns present such as the
number of rules. The SIP-BART architecture is still not completely invariable to
changes in distribution, as seen by the slightly lower accuracy for SIP-BART(LP)
tested on RP and RP_b. Though, it must be said this is only a minor issue -
the accuracy of the different SIP-BART models are all above 99.8% in total.
    In summary, this reinforces the result by [19]: a stepwise generation of the
proof improves the models ability to solve logic based problems expressed in
natural language. In addition, we also show that the reason for this improvement
is that the models are less likely to internalise spurious correlations that exist
in the data. But even if the models are able to achieve a high accuracy they
are not able to solve all problems, which indicates that there are still flaws in
their approximation of reasoning. It is therefore necessary to further analyse
what type of errors that are committed and the reasons for them. We proceed
by doing so for our best performing model, SIP-BART.


3.2   Consistency of SIP-BART

Although the accuracy tells us how well a given model is able to determine the
truth-value of the query in each problem, it does not take into account if each
of the inference steps themselves are sound and complete (i.e., consistent). Even
though the consistency scores where high, with all SIP-BART models achieving
                 Mitigating Spurious Correlations and Reasoning Shortcuts           9

 TRAIN TEST     0       1        2       3         4       5        6       TOT
 LP    LP       99.94   100.     99.97   100.      100.    100.     100.    99.98
 LP    RP       99.97   99.97    100.    99.92     99.90   99.872   99.49   99.87
 LP    RP_b     100.    99.97    99.97   99.89     99.94   99.74    99.25   99.81
 RP    LP       99.97   100.     100.    100.      100.    100.     100.    99.99
 RP    RP       100.    100.     100.    100.      100.    100.     99.97   99.99
 RP    RP_b     100.    100.     100.    100.      100.    100.     100.    100.
 RP_b LP        99.97   100.     99.97   100.      100.    100.     100.    99.99
 RP_b RP        99.94   100.     100.    100.      99.97   99.97    99.97   99.98
 RP_b RP_b      100.    100.     100.    100.      100.    99.97    100.    99.99
Table 3: Accuracy for the SIP-BART models trained on the different distribu-
tions measured in percentage of correct predictions. The integers refer to the
depth of the ground-truth proof. TOT is the overall average accuracy across
proofs of all depths. There are roughly the same number of inference-problems
for each depth. 100. means exactly 100.. Values very close to 100. have been
floored to 99.99.



above 99% fully consistent proofs, there are four types of reoccurring errors, as
described in §2.3. The frequencies of these are shown in Table 4. Again, SIP-
BART(LP) gets a somewhat lower score that compared to the other two models,
with the lowest consistency of the series of inference steps being 99.11% when
tested on RP_b. The following sections will be dedicated to analysing each of
these types and highlighting some of the reasons for why they occur.


Train Test    NonExR InappR         SpMatch UnexhS         Error       Tot. Consis-
                                                           Rate        tency
LP   LP   0.036          0.         0.007        0.004     0.046       99.954
LP   RP   0.661          0.         0.004        0.021     0.686       99.314
LP   RP_b 0.868          0.         0.           0.021     0.889       99.111
RP   LP   0.018          0.004      0.004        0.        0.025       99.975
RP   RP   0.007          0.018      0.           0.004     0.029       99.971
RP   RP_b 0.021          0.014      0.004        0.        0.039       99.961
RP_b LP   0.011          0.         0.004        0.004     0.018       99.982
RP_b RP   0.032          0.011      0.007        0.011     0.061       99.939
RP_b RP_b 0.025          0.007      0.004        0.004     0.039       99.961
Table 4: Frequencies of different types of consistency-errors in percent for the
different training and testing sets. The 0.000 values are close to zero but not
exactly zero. The 0. values are exactly zero.




Non-existing Rule Across most of the SIP-BART models, the most common
error was Non-existing Rule, which occurred in between 0.01% - 0.87% of proofs,
10     Enström, Kjellberg and Johansson

depending on the test set. Based on qualitative analysis, it could be observed that
the most common reason for this error was that the model had generated part of
a existing rule but not the complete rule. The generated step often included the
latter part of an existing rule but had missed one or more of the premises, see
the right-side example in Figure 3. Another error was that the model generated
synonyms to the word in a rule instead of the word that existed in the original
rule (Figure 3, left), where the generated rule includes the word "courageous"
instead of "fearless". Interestingly, most of the steps in the inference procedure
that include non-existing rules are still almost correct (we can view them as near
misses). In most cases, the model still provides a correct final classification of
the problem, even when out-of-distribution.




Fig. 3: Two examples of where the Non-existing Rule error has occurred. On
the left, the generated rule include a synonym word "courageous" instead of
"fearless". The second example (right) the model generated part of the rule but
missed the premise "charming".




Inapplicable Rule Inapplicable Rule errors occurred in up to 0.02 percent of
the attempted proofs. It was the second most common error for SIP-BART(RP)
and SIP-BART(RP_b) but did not occur at all for SIP-BART(LP), see Table
4. Qualitative analysis suggests that the cause for this error type is the order
                  Mitigating Spurious Correlations and Reasoning Shortcuts        11

and location of rules and facts in the input: The input is structured so that the
query, rules and facts are located following each other in the input string, and
the analysis indicates that the model has mistaken parts of the rules close to the
facts, as facts. Two examples of this are shown in Figure 4.




Fig. 4: Two examples of where the generated inference steps include inapplicable
rules. In both examples the conclusion of the last rule has been mistaken as
a fact. The model confuses the conclusion of the last rule in the input string,
regarding it as a fact instead of a rule that is not yet satisfied.




Spurious Match The third type of error, Spurious Match, is the least common
error in total, with a prevalence of 0.000 to 0.007 percent. In all cases, the reason
was that the model mistakes a synonym word to the query as the actual query
and the model predicts the query as True (similar to what happened for Non-
existent Rule). In essence, this error means that the system has proved the wrong
query. This is exemplified in Figure 5 where the series of inference steps ends
with a rule with the conclusion adorable and a True label is generated, but the
query to the problem asked for is in fact the synonym cute.

Unexhausted Search Space The final type of error, Unexhausted Search
Space, is only applicable for problems predicted to be False, with a prevalence
of up to 0.02%. This was the second most common error for SIP-BART(LP)
when tested on RP and RP_b and was the only error that was found for the
false negative problems. No obvious patterns could be observed in why this error
12      Enström, Kjellberg and Johansson




Fig. 5: Two examples of where a Spurious Match has occurred. In the first ex-
ample (left) the fact glamorous has been mistaken as the query gorgeous. In the
second example (right) the conclusion in the generated rule aggressive,attentive
⇒ adorable is mistaken as the query cute.


occurred, other than that in most cases the model had found all but one rule,
which meant that most of these errors occurred on true negatives. This is likely
due to the probability of generating the token False increases as the search space
is getting closer to exhaustion. When that happens, the probability for that token
might get too high slightly too quickly, i.e., before the search space is exhausted.

Summary In summary, even if all the models achieve high levels of consis-
tency, they are not immune to producing errors. In total the most frequent error
is Non-existing Rule, but the different SIP-BART models differ somewhat in the
distribution of error-types. For all the models the accuracy is higher than the
consistency, some proofs contain erroneous steps, but still end with the correct
Boolean label for the query. However, the difference between accuracy and con-
sistency is quite small, which means that almost all correct classifications are
consistent - no model has more than 0.7% consistency errors on any of the given
testing set.

4    Discussion and Conclusion
By generating inference steps, SIP-BART minimises the effect of known spurious
correlations present in the SimpleLogic dataset. The model divides each prob-
lem into smaller sub-problems that are easier to solve, which helps approximate
                     Mitigating Spurious Correlations and Reasoning Shortcuts            13

reasoning without exploiting statistical features as shortcuts. This also makes it
easier for the model to approach the parts of the problem in the correct order.
SIP-BART does this by playing to the strengths of each of its modules. The
pattern recognition task, which is handled by the neural-module, is in essence
an inductive task where conclusions are drawn from observations. The symbolic
module instead handles the deductive part, the transition between each reason-
ing step. By limiting the work that needs to be done by the neural-module,
the SIP-BART model can focus on only trying to find rules that are applicable
without the need to take into consideration the previous or the next steps of
the inference procedure. One explanation for this is the importance of locality
in the training data [13]: training on individual proof-steps instead of the final
outcome increase locality between the current goal and the desired output (the
next applicable rule).

4.1     Mitigation Strategies
Although SIP-BART perform much better than the BERT classifier, it still
makes some spurious errors which we identified in our experiments. Below, we
also suggest some strategies for mitigating these. Evaluating the strategies fully
is left as further work, and should ideally be done on a dataset where these errors
are more common than in SimpleLogic to ensure effects are significant.

Dealing with Synonyms All the SIP-BART models were fine-tuned from
a pre-trained BART-model. A adverse effect of this became apparent from the
quantitative analysis: words were occasionally swapped for synonyms. This makes
sense in natural language, but not in logic inferences. All Spurious Matches and
many of the Non-existing Rule-errors are due to such synonym-issues. One solu-
tion is to train a transformer from scratch, on a restricted vocabulary, instead of
starting from a pre-trained model. However, if we want a model that can both
reason and understand instructions expressed in natural language, this is not
the best solution. This may also require additional computational resources for
training. Another potential solution could be to use a constrained decoder [7],
which only allows generation of strings adhering to a specified grammar, i.e. only
well-formed rules over a specific vocabulary.

Dealing with Locality Bias The input string describing the problem contains
the list of rules, followed by the list of facts. Inapplicable Rule and Non-existing
Rule errors are closely tied to the locality structure of the input and can be con-
sidered a spurious statistical feature learned by the models. In the Inapplicable
Rule-case, the models mistakenly treat the tokens toward the end of the input
string as facts, instead of the conclusion of a rule, despite facts being demar-
cated by a different symbol6 . Similarly, when the model disregards a premise of
6
    e.g. if aggressive and inquisitive are conclusions to rules, they are written as aggres-
    sive: and inquisitive: in the input, while if they were facts they would be followed
    by a different symbol, i.e. aggressive1 and inquisitive1.
14      Enström, Kjellberg and Johansson

a rule when making a Non-existing Rule error, it seems like it has not completely
internalised the scope of the rules premises, despite that all the literals in the
premise are demarcated with a ","-sign. A possible way of solving this would be
to shuffle the order of the query, rules and facts in the input string of the training
data. This might teach the model to avoid focusing on the token’s position in
the input string when it instead should be paying attention to the demarcation
symbols that follow the token.

Dealing with Search Space Issues This strategy relies on a neuro-symbolic
architecture (unlike the previous two). A standard approach is to let the neural
model generate multiple answers for the same input, then letting the symbolic
module check which ones are in fact valid inferences. This will of course induce a
small overhead in runtime. This strategy is particularly relevant for Unexhausted
Search Space errors, where we need to compensate for the neural model jumping
to conclusions too quickly, before the final inferences has been generated.

4.2   Conclusion
Our study provides empirical evidence as to why inducing transformers to rea-
soning step by step generally better approximated logical reasoning - it helps
avoiding spurious statistical patterns such as correlations between the number
of rules and facts and the truth value of the query. Training on whole proofs
was not sufficient, the transformer still picked up reasoning shortcuts. Part of
the reason for this is likely that training on proof-steps gave more training data:
the model would benefit for each step in each training proof. It is also possi-
ble that the representation of "failed" proofs for false queries was difficult to
learn for WP-BART. However, for computational resource reasons, this was not
investigated further.
     We also identify four additional types of spurious errors made by the trans-
former model, arising from replacement of a word by a synonym (an effect of
pre-training on natural language), mistaking part of a rule for a fact when lo-
cated closely in the input or jumping to a final conclusion before completing the
proof. We proposed some mitigation strategies to counter this, some of which can
be implemented directly for the transformer, but for robust reasoning, we believe
it is necessary to implement a neuro-symbolic architecture. Here, a neural mod-
ule suggests (perhaps multiple) rules and a symbolic module checks them and
deals with updates to the problem representation. Another approach is to use
a language model just as a semantic parser and train it to translate the whole
problem into the input language of a symbolic prover [11]. However, one still
needs to deal with similar errors as those discussed here causing subtle mistakes
in translation to propagate through to the reasoning engine.

Acknowledgement
The computations and storage of data were enabled by resources provided by
the National Academic Infrastructure for Supercomputing in Sweden (NAISS) at
                   Mitigating Spurious Correlations and Reasoning Shortcuts         15

Chalmers Centre for Computational Science and Engineering (C3SE), partially
funded by the Swedish Research Council through grant agreement no. 2022-
06725. We would also like to thank Nicholas Smallbone for feedback on a draft
of this paper.


References
 1. Britz, D., Goldie, A., Luong, M.T., Le, Q.V.: Massive exploration of neural machine
    translation architectures. arXiv preprint arXiv:1703.03906 (2017)
 2. Clark, P., Tafjord, O., Richardson, K.: Transformers as soft reasoners over lan-
    guage. In: Proceedings of the Twenty-Ninth International Joint Conference on Ar-
    tificial Intelligence. IJCAI’20 (2021)
 3. Creswell, A., Shanahan, M., Higgins, I.: Selection-inference: Exploiting large lan-
    guage models for interpretable logical reasoning. In: The Eleventh International
    Conference on Learning Representations (2023), https://openreview.net/forum?
    id=3Pf3Wg6o-A4
 4. Devlin, J., Chang, M.W., Lee, K., Toutanova, K.: BERT: Pre-training of deep
    bidirectional transformers for language understanding. In: Proceedings of the 2019
    Conference of the North American Chapter of the Association for Computational
    Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers).
    pp. 4171–4186. Association for Computational Linguistics, Minneapolis, Minnesota
    (Jun 2019). https://doi.org/10.18653/v1/N19-1423, https://aclanthology.
    org/N19-1423
 5. Elazar, Y., Kassner, N., Ravfogel, S., Ravichander, A., Hovy, E., Schütze, H.,
    Goldberg, Y.: Measuring and improving consistency in pretrained language mod-
    els. Transactions of the Association for Computational Linguistics 9, 1012–1031
    (2021). https://doi.org/10.1162/tacl_a_00410, https://aclanthology.org/
    2021.tacl-1.60
 6. Enström, D., Kjellberg, V.: Approximating reasoning with transformer lan-
    guage models (2023), https://gupea.ub.gu.se/handle/2077/78873, MSc thesis
    Gothenburg University
 7. Geng, S., Josifosky, M., Peyrard, M., West, R.: Flexible grammar-based constrained
    decoding for language models (2023)
 8. Kojima, T., Gu, S.S., Reid, M., Matsuo, Y., Iwasawa, Y.: Large language models
    are zero-shot reasoners. In: Oh, A.H., Agarwal, A., Belgrave, D., Cho, K. (eds.)
    Advances in Neural Information Processing Systems (2022), https://openreview.
    net/forum?id=e2TBb5y0yFf
 9. Lewis, M., Liu, Y., Goyal, N., Ghazvininejad, M., Mohamed, A., Levy, O.,
    Stoyanov, V., Zettlemoyer, L.: BART: Denoising sequence-to-sequence pre-
    training for natural language generation, translation, and comprehension. In:
    Proceedings of the 58th Annual Meeting of the Association for Computa-
    tional Linguistics. pp. 7871–7880. Association for Computational Linguistics,
    Online (Jul 2020). https://doi.org/10.18653/v1/2020.acl-main.703, https:
    //aclanthology.org/2020.acl-main.703
10. Nye, M., Andreassen, A.J., Gur-Ari, G., Michalewski, H., Austin, J., Bieber, D.,
    Dohan, D., Lewkowycz, A., Bosma, M., Luan, D., Sutton, C., Odena, A.: Show your
    work: Scratchpads for intermediate computation with language models (2021)
11. Olausson, T., Gu, A., Lipkin, B., Zhang, C., Solar-Lezama, A., Tenenbaum, J.,
    Levy, R.: LINC: A neurosymbolic approach for logical reasoning by combining
16      Enström, Kjellberg and Johansson

    language models with first-order logic provers. In: Bouamor, H., Pino, J., Bali,
    K. (eds.) Proceedings of the 2023 Conference on Empirical Methods in Natu-
    ral Language Processing. pp. 5153–5176. Association for Computational Linguis-
    tics, Singapore (Dec 2023). https://doi.org/10.18653/v1/2023.emnlp-main.
    313, https://aclanthology.org/2023.emnlp-main.313
12. Polu, S., Sutskever, I.: Generative language modeling for automated theorem prov-
    ing (2020). https://doi.org/10.48550/ARXIV.2009.03393, https://arxiv.org/
    abs/2009.03393
13. Prystawski, B., Goodman, N.D.: Why think step-by-step? Reasoning emerges from
    the locality of experience (2023)
14. PyTorch Development Team: Reproducibility. https://pytorch.org/docs/
    stable/notes/randomness.html (Accessed 2023), accessed on May 23, 2023
15. Rabe, M.N., Lee, D., Bansal, K., Szegedy, C.: Mathematical reasoning via
    self-supervised skip-tree training. arXiv: Learning (2020). https://doi.org/10.
    48550/ARXIV.2006.04757, https://arxiv.org/abs/2006.04757
16. Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., Sutskever, I., et al.: Language
    models are unsupervised multitask learners. OpenAI blog 1(8), 9 (2019)
17. Saxton, D., Grefenstette, E., Hill, F., Kohli, P.: Analysing mathematical reasoning
    abilities of neural models. In: International Conference on Learning Representa-
    tions (2019), https://openreview.net/forum?id=H1gR5iR5FX
18. Susskind, Z., Arden, B., John, L.K., Stockton, P.A., John, E.B.: Neuro-
    symbolic ai: An emerging class of ai workloads and their characterization. ArXiv
    abs/2109.06133 (2021)
19. Tafjord, O., Dalvi, B., Clark, P.: ProofWriter: Generating implications, proofs,
    and abductive statements over natural language. In: Findings of the Association
    for Computational Linguistics: ACL-IJCNLP 2021. pp. 3621–3634. Association for
    Computational Linguistics, Online (Aug 2021). https://doi.org/10.18653/v1/
    2021.findings-acl.317, https://aclanthology.org/2021.findings-acl.317
20. Talmor, A., Tafjord, O., Clark, P., Goldberg, Y., Berant, J.: Leap-of-thought:
    Teaching pre-trained models to systematically reason over implicit knowledge. In:
    Proceedings of the 34th International Conference on Neural Information Processing
    Systems. NIPS’20, Curran Associates Inc., Red Hook, NY, USA (2020)
21. Valmeekam, K., Olmo, A., Sreedharan, S., Kambhampati, S.: Large language mod-
    els still can’t plan (a benchmark for llms on planning and reasoning about change).
    ArXiv abs/2206.10498 (2022). https://doi.org/10.48550/ARXIV.2206.10498,
    https://arxiv.org/abs/2206.10498
22. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N.,
    Kaiser, L., Polosukhin, I.: Attention is all you need. In: Proceedings of the 31st
    International Conference on Neural Information Processing Systems. p. 6000–6010.
    NIPS’17, Curran Associates Inc., Red Hook, NY, USA (2017). https://doi.org/
    10.48550/ARXIV.1706.03762, https://arxiv.org/abs/1706.03762
23. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F.,
    Chi, E., Le, Q.V., Zhou, D.: Chain-of-thought prompting elicits reason-
    ing in large language models. In: Koyejo, S., Mohamed, S., Agarwal,
    A., Belgrave, D., Cho, K., Oh, A. (eds.) Advances in Neural Infor-
    mation Processing Systems. vol. 35, pp. 24824–24837. Curran Associates,
    Inc. (2022), https://proceedings.neurips.cc/paper_files/paper/2022/file/
    9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf
24. Zhang, H., Li, L.H., Meng, T., Chang, K., den Broeck, G.V.: On the paradox of
    learning to reason from data. In: Proceedings of the Thirty-Second International
              Mitigating Spurious Correlations and Reasoning Shortcuts      17

Joint Conference on Artificial Intelligence, IJCAI 2023, 19th-25th August 2023,
Macao, SAR, China. pp. 3365–3373. ijcai.org (2023). https://doi.org/10.24963/
IJCAI.2023/375, https://doi.org/10.24963/ijcai.2023/375
                                                                                                                                 18



A    Example SimpleLogic Problem
                                                                                                                                 Enström, Kjellberg and Johansson




Fig. 6: Example of the structure of a problem in SimpleLogic. The query can be seen in the purple circle. The rules are
represented in each rectangle, with the premises on the left side and the conclusion in bold text on the right side. The facts
are represented as single words in each diamond shape.
                  Mitigating Spurious Correlations and Reasoning Shortcuts     19

B    Hyperparameters and Hardware

We fine-tuned a BART model from Huggingface (https://huggingface.co/
facebook/bart-base) with the default hyperparameters with the exception of
batch size and gradient accumulation steps, which was tuned to maximize the
memory usage of the GPUs used. For all experiments we used four NVIDIA
Tesla A40 GPUs with 48GB RAM.


               Hyperparameter                    Value
               Learning rate                     0.00002
               Batch size                        8
               Gradient accumulation steps       4
               fp16                              True
               Warmup steps                      200
               Weight decay                      0.01
               Epoch                             1




C    Evaluation of WP-BART
The evaluation based on the precision, recall and F1-score of the worst perform-
ing model, WP-BART(LP), on the RP dataset. Together with the precision,
recall and F1-score for each of the WP-BART models based on which training
and testing datasets where used.


 Depth     TPR       FPR       TNR       FNR       Preci-    Recall    F1-
                                                   sion                Score
 0         0.80      0.        0.21      0.        1.        1.        1.
 1         0.75      0.        0.25      0.        1.        1.        1.
 2         0.48      0.        0.35      0.17      1.        0.74      0.85
 3         0.19      0.        0.46      0.35      1.        0.35      0.52
 4         0.07      0.00      0.60      0.33      0.99      0.18      0.31
 5         0.02      0.        0.70      0.28      1.        0.07      0.13
 6         0.01      0.00      0.76      0.23      0.86      0.03      0.05
 Total     0.33      0.00      0.47      0.19      0.99      0.63      0.77
Table 1: Evaluation metrics for the WP-BART(LP) tested on RP dataset. In the
heading the acronyms for True Positive Rate (TPR), False Positive Rate (FPR),
True Negative Rate (TNR) and False Negative Rate (FNR) are used. The 0.00
values are close to zero but not exactly zero. The 0. values are exactly zero. The
corresponding information for exactly one is true for 0.99 and 1., respectively.
20      Enström, Kjellberg and Johansson

Train    Test      TPR       FPR        TNR     FNR        Preci-   Recall    F1-
                                                           sion               Score
LP       LP        0.431     0.001      0.507   0.061      0.999    0.877     0.934
LP       RP        0.332     0.000      0.474   0.194      0.999    0.631     0.773
LP       RP_b      0.346     0.000      0.474   0.180      0.999    0.657     0.793
RP       LP        0.462     0.218      0.290   0.030      0.680    0.940     0.789
RP       RP        0.487     0.117      0.358   0.038      0.807    0.927     0.863
RP       RP_b      0.492     0.113      0.362   0.034      0.814    0.936     0.871
RP_b     LP        0.461     0.137      0.371   0.031      0.771    0.937     0.846
RP_b     RP        0.482     0.069      0.405   0.044      0.874    0.917     0.895
RP_b     RP_b      0.488     0.065      0.410   0.037      0.883    0.929     0.905
Table 2: Precision, Recall and F1 score for all WP-BART models. In the heading
the acronyms for True Positive Rate (TPR), False Positive Rate (FPR), True
Negative Rate (TNR) and False Negative Rate (FNR) are used. All numbers are
rounded to three decimals. The 0.000 values are close to zero but not exactly
zero.



D    Evaluation of SIP-BART

The evaluation based on the precision, recall and F1-score of the worst perform-
ing model, SIP-BART(LP), on the RP dataset. Together with the precision,
recall and F1-score for each of the SIP-BART models based on which training
and testing datasets where used.


 Depth     TPR       FPR        TNR         FNR         Preci-   Recall      F1-
                                                        sion                 Score
 0         0.795     0.000      0.204       0.          0.999    1.          0.999
 1         0.754     0.000      0.245       0.          0.999    1.          0.999
 2         0.652     0.         0.347       0.          1.       1.          1.
 3         0.537     0.000      0.461       0.000       0.999    0.999       0.999
 4         0.400     0.001      0.598       0.000       0.998    0.999       0.998
 5         0.297     0.001      0.701       0.000       0.997    0.998       0.997
 6         0.239     0.005      0.755       0.000       0.980    0.998       0.989
Table 1: Evaluation metrics for the SIP-BART(LP) tested on RP dataset. In the
heading the acronyms for True Positive Rate (TPR), False Positive Rate (FPR),
True Negative Rate (TNR) and False Negative Rate (FNR) are used. The values
0.000 are close to zero but not exactly zero. The values that are 0. are exactly
zero, an example is found for depth 2 for FP, and means that not a single case
was found. The values 1. means exactly 1.
                  Mitigating Spurious Correlations and Reasoning Shortcuts       21




Train    Test     TPR      FPR      TNR      FNR      Preci-   Recall    F1-
                                                      sion               Score
LP       LP       0.492    0.000    0.507    0.000    0.999    0.999     0.999
LP       RP       0.525    0.001    0.473    0.000    0.998    0.999     0.998
LP       RP_b     0.525    0.002    0.472    0.000    0.997    0.999     0.998
RP       LP       0.492    0.000    0.507    0.       0.999    1.        0.999
RP       RP       0.525    0.       0.474    0.000    1.       0.999     0.999
RP       RP_b     0.525    0.       0.475    0.       1.       1.        1.
RP_b     LP       0.492    0.000    0.507    0.000    0.999    0.999     0.999
RP_b     RP       0.525    0.000    0.474    0.000    0.999    0.999     0.999
RP_b     RP_b     0.525    0.       0.474    0.000    1.       0.999     0.999
Table 2: Precision, Recall and F1 score for all WP-BART models. In the heading
the acronyms for True Positive Rate (TPR), False Positive Rate (FPR), True
Negative Rate (TNR) and False Negative Rate (FNR) are used. The 1. values
are exactly one. All other numbers are rounded to three decimals, except those
very close to 1. Values very close to 1 have been floored to 0.999. Similarly, the
0.000 values are close to zero but not exactly zero. The 0. values are exactly
zero, an example is row 5 for FP, and means that not a single case was found.
