                                                             Formal Mathematics Statement Curriculum Learning


                                           Stanislas Polu 1 Jesse Michael Han 1 Kunhao Zheng 2 Mantas Baksys 3 Igor Babuschkin 1 Ilya Sutskever 1


                                                                  Abstract                                  whether a trajectory (i.e. a proof) is successful (i.e. formally
                                             We explore the use of expert iteration in the con-             correct). But the vast scope of formal mathematics means
                                             text of language modeling applied to formal math-              that any strong reasoning result obtained in it will be more
                                                                                                            meaningful than comparable results in games (e.g. finding
arXiv:2202.01344v1 [cs.LG] 3 Feb 2022




                                             ematics. We show that at same compute bud-
                                             get, expert iteration, by which we mean proof                  proofs to mathematical conjectures), and could even be
                                             search interleaved with learning, dramatically out-            applicable to important practical problems (e.g. software
                                             performs proof search only. We also observe that               verification).
                                             when applied to a collection of formal statements              However, tackling formal mathematics involves two main
                                             of sufficiently varied difficulty, expert iteration is         challenges that we must address in order to continue making
                                             capable of finding and solving a curriculum of in-             progress:
                                             creasingly difficult problems, without the need for
                                             associated ground-truth proofs. Finally, by apply-             Infinite action space Not only does formal mathematics
                                             ing this expert iteration to a manually curated set            have an extremely large search space (like Go for example),
                                             of problem statements, we achieve state-of-the-art             it also has an infinite action space. At each step of proof
                                             on the miniF2F benchmark, automatically solving                search, the model must choose not from a well-behaved
                                             multiple challenging problems drawn from high                  finite set of actions, but a complex and infinite set of tac-
                                             school olympiads.                                              tics, potentially involving exogenous mathematical terms
                                                                                                            that have to be generated (e.g., generating a mathematical
                                                                                                            statement to be used as a witness, an object used steps such
                                        1. Introduction                                                     as “there exists an x ...”, or a cut, the introduction and the
                                                                                                            chaining of a lemma in the middle of a proof).
                                        Deep learning has enjoyed spectacular success in many do-
                                                                                                            No direct self-play setup In formal mathematics, a prover
                                        mains, including language (Brown et al., 2020; Devlin et al.,
                                                                                                            is not playing against an opponent but against a set of state-
                                        2018; Wu et al., 2016), vision (Radford et al., 2021; Tan
                                                                                                            ments to prove. When faced with a statement that is just too
                                        & Le, 2019), and image generation (Ramesh et al., 2021;
                                                                                                            hard, there is no obvious reframing of the formal mathemat-
                                        Karras et al., 2019). One domain where deep learning has
                                                                                                            ics setup that will let the prover generate intermediary easier
                                        not yet enjoyed a comparable success is in tasks that re-
                                                                                                            statements to tackle first. This asymmetry prevents naive ap-
                                        quire extensive planning and symbolic reasoning, with the
                                                                                                            plication of the symmetric self-play algorithms commonly
                                        exception of two-player games (Silver et al., 2016; 2017;
                                                                                                            used in 2-player games.
                                        Berner et al., 2019; Vinyals et al., 2019). In such games,
                                        deep learning systems exhibit a considerable degree of rea-         These two differences make a naive application of reinforce-
                                        soning, especially when trained with self-play combined             ment learning to formal mathematics unlikely to succeed.
                                        with a search procedure such as Monte Carlo Tree Search             Past work proposed to address the infinite action space prob-
                                        (MCTS) (Browne et al., 2012). But the resulting reasoning           lem by sampling from a language model (Polu & Sutskever,
                                        abilities achieved are limited due to the relatively narrow         2020). This paper focuses on this second problem and our
                                        scope of games.                                                     basis for addressing it is the observation that the key role
                                                                                                            of self-play is to provide an unsupervised curriculum. We
                                        As such, theorem proving in interactive proof assistants, or
                                                                                                            propose instead to supply auxiliary sets of problem state-
                                        formal mathematics, appears as an interesting game-like
                                                                                                            ments (without requiring proofs) of varying difficulty. We
                                        domain to tackle due to its increased scope. Like games,
                                                                                                            empirically show that, when the difficulty of these auxil-
                                        formal mathematics has an automated way of determining
                                                                                                            iary problems is varied enough, a simple expert iteration
                                                                                                            procedure is able to solve a curriculum of increasingly diffi-
                                           1
                                             OpenAI 2 École Polytechnique 3 University of Cambridge. Cor-   cult problems, eventually generalizing to our target distri-
                                        respondence to: Stanislas Polu <spolu@openai.com>.                  bution. We show that this works with both automatically-
                                        Preprint. Under review.                                             generated and manually-curated auxiliary distributions of
                                    Formal Mathematics Statement Curriculum Learning

problems and leverage this to achieve state-of-the-art on the    the miniF2F benchmark (Zheng et al., 2021)–Lean proofs
miniF2F benchmark. Our results suggest that continuous           are typically 10x shorter than Metamath’s. Also, Lean has
self-improvement in formal mathematics can potentially           recently received a lot of attention from the mathemati-
be reduced to the problem of generating such sets of for-        cal community, thanks to projects such as the Perfectoid
mal statements, which we have done in part manually in           Spaces (Buzzard et al., 2019) and the Liquid Tensor experi-
this work, but could eventually be scaled in the future with     ment (Scholze, 2020), and benefits from a vibrant commu-
more automation (such as more domain-specific statements         nity of hundreds of contributors to its main mathematical
generator or even informal to formal machine translation).       library called mathlib. We refer to the PACT paper’s Back-
                                                                 ground section (Han et al., 2021) for a detailed introduction
1.1. miniF2F benchmark                                           to Lean in the context of neural theorem proving.
In this work, we target the miniF2F (Zheng et al., 2021)
                                                                 3.1. lean-gym
benchmark, which consists of 244 validation and 244 test
formalized statements of mathematical problems from var-         In the PACT paper (Han et al., 2021), proof search is per-
ious competitions. We believe it to be a better measure          formed by the Lean runtime using the L EAN S TEP environ-
of mathematical reasoning compared to a formal library-          ment, with a generic backend interface to models. While
derived split. Also, the extreme scarcity in formal libraries    easy to use–one just needs to plug in their model–this ap-
of this type of problems makes it an ideal test-bed for the      proach makes it difficult to alter and iterate on the search
expert iteration methodology studied in this paper.              procedure because it is programmed in Lean (which is not
                                                                 designed or intended for cluster-wide parallelised I/O inten-
1.2. Contribution                                                sive tasks), and the coupling of the search procedure with
                                                                 the Lean runtime introduces challenges when scaling to a
Our contributions are the following: we present lean-gym,        large number of parallel workers.
a simple REPL interface for interacting with the Lean the-
orem prover; we propose an expert iteration methodology          To solve these issues we implemented lean-gym1 – a
for GPT-f (Polu & Sutskever, 2020) which uses proofs gen-        simple REPL interface over the standard input/output im-
erated by our models as training data to iteratively improve     plemented in Lean directly. We present lean-gym’s API
their performance; we demonstrate that, at fixed compute         and discuss some of its advantages and limitations in Ap-
budget, expert iteration outperforms proof search only; we       pendix B.
present a synthetic inequality generator and study how ex-
pert iteration finds and solves a curriculum of increasingly     3.2. Proof datasets extraction
difficult problems from a set of generated statements of var-
                                                                 We rely on the proof extraction methodology presented
ious difficulty; finally, we present a manually curated set of
                                                                 in the PACT paper (Han et al., 2021) to extract human
formalized problem statements and leverage it to achieve
                                                                 tactic proof steps from mathlib (the tactic dataset) as
state-of-the-art performance on the miniF2F benchmark.
                                                                 well as the various other proof artifacts (mix1 and mix2
                                                                 datasets). We also extract mathlib-{train,valid,test}, the
2. Related Work                                                  set of statements from mathlib along the split proposed in
                                                                 Han et al. (2021) (the validation and test splits of tactic,
Our work strongly relies on, and can be seen as a natural
                                                                 mix1, mix2 being aligned with mathlib-{valid, test} as
continuation of the work presented in the original GPT-f
                                                                 the splits are determined by declaration name hashes (across
paper (Polu & Sutskever, 2020) which studies the use of
                                                                 all data sources including proof-term mining) as opposed to
language models to generate tactics, the PACT paper (Han
                                                                 individual proof steps or data-points).
et al., 2021) which applies GPT-f to Lean and studies the
benefits from co-training on self-supervised objectives, and
the miniF2F benchmark (Zheng et al., 2021).                      4. Expert Iteration
We present additional related work in Appendix A.                Expert iteration was introduced in Silver et al. (2017) and
                                                                 broadly consists in iteratively training models on their previ-
3. Formal Environment                                            ously sampled trajectories, to achieve continuous improve-
                                                                 ment. In this section we present our expert iteration method-
We choose Lean (de Moura et al., 2015; lea) as our for-          ology, including the models and pre-training strategies we
mal environment. Unlike Metamath (Megill & Wheeler,              rely on.
2019), which has been studied in the original GPT-f pa-             1
                                                                        https://github.com/openai/lean-gym
per (Polu & Sutskever, 2020), Lean benefits from high-level
tactics which were shown to be beneficial in the context of
                                      Formal Mathematics Statement Curriculum Learning

4.1. Model                                                         proof sizes.
We use decoder-only Transformers similar to GPT-3 (Brown           We use 11 buckets B = 0...10 and compute the proofsize
et al., 2020). Throughout this paper we focus on a model           bucket b(g) for a goal g by assigning infinite proof sizes to
with 36 layers and 774 million trainable parameters (referred      bucket 0, all proof sizes over 20 to bucket 1 and linearly pro-
to as the 700m model in the GPT-f paper (Polu & Sutskever,         jecting proof sizes lower than 20 on the remaining buckets
2020)).                                                            2, ..., 10 (10 being the bucket for the shortest proof sizes).
                                                                   In practice, when training and sampling from the model, we
4.2. Pre-Training                                                  map B to the tokens ’A’...’K’.

We pre-train our models successively on GPT-3’s post-              To value goals as we run proof searches, we sample the
processed version of CommonCrawl (for 300B tokens) and             proofsize bucket token and record the logits pb (g) for each
an updated version of WebMath (Polu & Sutskever, 2020)             viable bucket and use them to get a P
                                                                                                       weighted average with
                                                                                                   1
(for 72B tokens) whose mix is presented in Appendix C.             the following formula: v(g) = #B      b∈B pb (g).b.

                                                                   As an example, if the model assigns p0 = 1 (hence pb6=0 =
4.3. Training objectives                                           0) then v(g) = 0. Conversely if the model assigns p10 =
4.3.1. Proofstep objective                                         1 (10 being the bucket for the shortest proof sizes) then
                                                                   v(g) = 1.
The proofstep objective, introduced in Polu & Sutskever
                                                                   The rationale for using this proofsize objective instead of
(2020), consists in generating a PROOFSTEP (a Lean
                                                                   the outcome objective described in Polu & Sutskever (2020)
tactic) given a GOAL (a Lean tactic state). We also
                                                                   is that (i) it achieves better performance compared to the
condition this objective on the current DECLARATION
                                                                   outcome objective (see table 1), and (ii) it prioritizes goals
(a Lean theorem name), which remains the same
                                                                   that potentially lead to shorter proofs during proof search,
throughout a proof search: DECL <DECLARATION>
                                                                   creating an intrinsic incentive for the system to converge to-
GOAL <GOAL> PROOFSTEP <PROOFSTEP>.
                                                                   wards shorter proofs. Similarly to Polu & Sutskever (2020)
The rationale for conditioning on the declaration name is to       we favor this token-based approach to the introduction of
hint our models on the position of the current declaration in      a separate value head to keep the overall architecture sim-
the mathlib library. It can be considered as a weak proxy          ple. This way the proofsize objective can be implemented
signal for the large amount of information not shown to            by simply augmenting the training dataset and without any
the model (the full environment consisting of the available        architectural change.
imports and currently open declarations such as module
names, notations, declared instances, ...). The declaration        4.4. Bootstrapping
name lets models at least in principle memorize and then
retrieve some of that information, knowing that lean-gym           Bootstrapping consists in the steps required to train an initial
errors if a theorem or definition that is not available in         model on both the proofstep objective and the proofsize
the environment associated with the current declaration is         objective.
used by tactics generated by our models. Also note that            Given a pre-trained model on WebMath, we fine-tune it
conversely to Polu & Sutskever (2020) and like Han et al.          on the tactic dataset extracted from mathlib as well as
(2021) <GOAL> is not necessarily a single goal but a Lean          the proof artifacts dataset mix1 as described in Han et al.
tactic state, which possibly comprises multiple goals.             (2021). This initial model, which we denote θ0 is solely
                                                                   trained on the proofstep objective. We use the validation
4.3.2. Proofsize objective                                         splits of the tactic and m1 datasets to early-stop training.
We depart from Polu & Sutskever (2020) and use a                   Note that this is our only use of mathlib-valid to influence
proofsize objective to guide our proof searches, which             the training process throughout this paper.
consists in generating one token that represents a proof           To generate data for the proofsize objective, we use θ0 to
size estimate bucket for the current goal (Lean tac-               sample proofs for statements from mathlib-train. For each
tic state): DECL <DECLARATION> GOAL <GOAL>                         statement from mathlib-train (25k) we attempt a = 1 proof
PROOFSIZE <PROOFSIZE_BUCKET_TOKEN>                                 searches using the cumulative logprob priority search de-
For a given goal g, either the goal was proved as part of the      scribed in Polu & Sutskever (2020) (which does not require
proof search and we denote its proof size (the number of           a trained value function) using d = 512 expansions and
tactic applications (compounded Lean tactics counting as           e = 8 samples per expansion. We denote the set of success-
one)) as ps(g), or the goal was not proved in which case we        ful proof searches created in this process as S0 .
assign the goal to a bucket that virtually represents "infinite"   Using S0 we generate dataset D0 by concatenating: (i) the
                                       Formal Mathematics Statement Curriculum Learning

                                                                      strating that training a value function on proofs sampled
Table 1. Performance of θ0 and θ1 on mathlib-valid and miniF2F-
                                                                      from mathlib-train has limited transfer to miniF2F-valid.
valid compared to PACT Lean GPT-f as reported in Han et al.
(2021); Zheng et al. (2021). All models have the same architecture.   The main differences with Zheng et al. (2021), potentially
θ0 is sampled using cumulative logprob priority best-first search.    explaining the gap on minif2f-valid (27.6% vs 23.9%), con-
θ1 is sampled using best-first search based on the proofsize objec-   sists in the new pre-training described in section 4.2 as well
tive. We report our setup (d = 512 expansions and e = 8 tactic        as the use of a more recent mathlib checkpoint for the mix1,
samples per expansions) as well as the setups used in Han et al.      mix2 and tactic datasets.
(2021); Zheng et al. (2021) to control for compute. We also report
the performance of θ1 on mathlib-valid when trained using the         4.5. Iterated sampling and training
outcome objective from Polu & Sutskever (2020) as an ablation of
our proposed proofsize objective.                                     Our expert iteration process takes as input: (i) a set of
                                                                      formal statements St, (ii) a function a : St →  − N indicating
   Model                         d     e   pass@1      pass@8
                                                                      the number of proof search attempts to run per statement at
   mathlib-valid                                                      each iteration, (iii) a base model θ0 to fine-tune from at each
   PACT                       512    16     48.4%                     iteration, and (iv) a mathlib bootstrapped model θ1 trained
   θ0 (PACT setup)            512    16     48.5%       57.6%
   θ0                         512     8     46.7%       57.5%         on both objectives.
   θ1                         512     8     56.3%       66.3%         Each iteration k consists in sampling proof searches for
   θ1 (outcome objective)     512     8     55.6%       65.9%
                                                                      statements in St using θk , filtering successful proof searches
   miniF2F-valid                                                      Sk to extract a new dataset Dk , and fine-tuning θ0 on it to
   MiniF2F                    128    16     23.9%       29.3%
   θ0 (MiniF2F setup)         128    16     27.6%       31.8%         obtain θk+1 , on which we can iterate. To sample proof
   θ0                         512     8     28.4%       33.6%         searches from St we use the best-first search described in
   θ1                         512     8     28.5%       35.5%         Polu & Sutskever (2020) with the value function described
   θ1 (outcome objective)     512     8     28.3%       34.7%         in section 4.3.2. We attempt a(s ∈ St) proof searches
                                                                      for each statement s with d = 512 expansions and e = 8
                                                                      samples per expansion. We denote the set of successful
                                                                      proof searches for iteration k as Sk .
initial tactic dataset (proofstep objective), (ii) a dedu-
plicated set of proofsteps extracted from the proofs in S0            Using Sk we generate datasets Dk by concatenating: (i) the
(proofstep objective) and (iii) a deduplicated set of proofsize       initial tactic dataset (proofstep objective), (ii) a dedu-
tuples (goals and proofsize) extracted from the full proof            plicated
                                                                      S         set of proofsteps extracted from the proofs in
searches in S0 (proofsize objective).                                           S
                                                                        1≤i≤k k (proofstep objective), and (iii) a deduplicated
                                                                      set of proofsize tuples (goals
                                                                                                 S and proofsize) extracted from
Note that the full proof searches in S0 include goals that            the full proof searches in 1≤i≤k Sk (proofsize objective).
are visited but eventually remain unproved, which provides
useful negative examples for the trained value function (even         Note that we use a global deduplication across iterations
if these negatives may include provable goals that simply             for both proofsteps and proofsize tuples which we found to
were not prioritized by the search). Also note that S0 doesn’t        be important to maintain the stability of the expert iteration
include failed proof searches (which would contain only               procedure. This global deduplication is somewhat equiva-
negative examples and no proofstep objective data).                   lent for each statement to growing a unique proof tree by
                                                                      aggregating all the proof searches that have been run for
We fine-tune θ0 on D0 for exactly one epoch (no use of val-           it across iterations. This virtual proof tree accumulates a
idation data for early-stopping) to obtain our initial model          growing number of positive proof paths as well as a grow-
θ1 trained on both the proofstep objective and the proofsize          ing number of visited goals that remain unproven. We use
objective. θ0 is used in our expert iteration setup as base           these goals as negative examples for the proofsize objective,
model to fine-tune from at each iteration, and θ1 is our first        labeling them with an infinite proofsize. Positive goals are
iterated model or mathlib bootstrapped model trained on               deduplicated keeping the minimum proof sizes across proof
both objectives.                                                      searches.
We report in Table 1 the pass rates of θ0 and θ1 on mathlib-          Finally θk is obtained by fine-tuning θ0 for exactly one
valid and miniF2F-valid and compare with previously re-               epoch on Dk . Note that the initial tactic dataset is in-
ported pass rates for equivalent amounts of compute. As               cluded in each Dk , despite θ0 being already trained on it
reported in Polu & Sutskever (2020), training a value func-           (along with mix1). We found this repetition to be beneficial
tion to guide search greatly improves the pass rates of θ1            overall (as it adds the mathlib extracted proofsteps to our
on mathlib-valid (see Polu & Sutskever (2020) for an abla-            deduplicated per statements virtual proof trees) despite it
tion of the value function). Interestingly, the gap between           leading to a slight overfit on the tactic dataset in terms
θ0 and θ1 on miniF2F-valid is not as significant, demon-
                                          Formal Mathematics Statement Curriculum Learning

of validation loss.                                                                 mathlib-valid                   minif2f-valid
                                                                          78                                46


4.6. Expert iteration on mathlib-train                                    76                                44

In this section we propose to set St to the statements in
                                                                          74                                42
mathlib-train, run our expert iteration process with it and re-
port performance on both mathlib-valid and miniF2F-valid.
                                                                          72                                40
Performance is reported in terms of pass rate (percentage of
successful proof searches) as a function of the number of                 70                                38
                                                                                                                         Expert iteration

attempts per statement, noted pass@k where k is the num-                                                                 Sample only
                                                                                                                         Adjusted compute
ber of attempts per statement at test time. To reduce noise               68                                36
                                                                                     2       4      6   8           2         4      6      8
in these metrics we generally run more than k attempts at
test time (generally 32 to compute pass@1 and pass@8),
averaging across attempts as needed to obtain a smoother
                                                                       Figure 2. Cumulative pass rate for our expert iteration loop as well
pass@k value.                                                          as a sample only loop where we skip re-training the model between
Given the large number of statements in mathlib-train (25k)            iterations. The adjusted compute line is computed by fitting the
we uniformly set a = 1 and use θ0 and θ1 as described in               sample only curve and shifting it to approximate a setup where we
                                                                       would focus all the additional compute used by expert iteration
section 4.4 and report pass@1 and pass@8 across 8 itera-
                                                                       (sampling training data from mathlib-train as well as re-training
tions in figure 1. The pass@1 on mathlib-valid goes from
                                                                       models at each iteration) towards running proof searches against
56.3% for θ1 to 62.6% for θ9 . The performance steadily                mathlib-valid.
improves and follows a clear logarithmic scaling law on
mathlib-valid. It is also notable that, initially, transfer to out-
of-distribution minif2f-valid appears limited but eventually
kicks in as we reach better performance on mathlib-valid.
This demonstrates that the expert iteration process does not           cumulative pass rate at iteration k can be seen as a noisy
just overfit to mathlib but also leads to improved perfor-             ensembled pass@16k (multiple models (θk ), no averaging).
mance on out-of-distribution statements.                               In figure 2, we report this cumulative pass rate for two it-
                                                                       eration loops, our normal one and a sampling-only loop
             mathlib-valid                   minif2f-valid             where we skip re-training the model between iterations and
                                                             pass@1
                                                                       solely sample from θ1 . This directly compares test-time
   70
                                                             pass@8    compute scaling (scaling proof search attempts) to expert
                                     40
                                                                       iteration scaling (interleaved training on new data sampled
   65
                                                                       from mathlib-train) and provides a very clear visualization
                                     35
                                                                       of the gains of expert iteration. For a fair comparison, we
                                                                       also report an adjusted compute line which approximates
   60                                                                  the test-time performance we would get at each iteration if
                                     30                                we were to focus all the additional compute used by expert
                                                                       iteration (sampling proofs from mathlib-train as well as
   55
              2       4      6   8            2       4      6   8     re-training models at each iteration) towards solely running
                                                                       proof searches against mathlib-valid.

Figure 1. pass@1 (plain) and pass@8 (dotted) for mathlib-valid
                                                                       As shown by figure 2, the scaling exponent of expert it-
and minif2f-valid when running 8 expert iterations with St set to      eration is substantially higher than the scaling exponent
be the statements in mathlib-train. The x-axis is log-scaled. It       associated with solely scaling test-time compute (running
corresponds to the indices of the θk models and serves as a good       more proof searches), demonstrating the clear benefit of
proxy to compute (the amount of test-time and train-time compute       expert iteration. We’ll denote the fully iterated model from
per iteration being fixed). The y-axis is scaled linearly and simply   this section as θ9mathlib .
shifted between the two graphs (spans an equal range).
                                                                       Even in the presence of ground-truth proofs for each of
                                                                       the statements in mathlib-train (tactic dataset), expert
                                                                       iteration generates data that further improves the perfor-
We define the cumulative pass rate at iteration k as the pass          mance of the model. The number of statements proved
rate consisting of all proof searches up to iteration k (neces-        in mathlib-train goes from 17390 (67.8%) at iteration 1 to
sarily monotonic in k). Since we set a = 16 for evaluation             19476 (76.0%) at iteration 9, while the average proof length
on mathlib-valid and minif2f-valid at each iteration, the              of these statements goes from 4.8 to 4.0. We hypothesize
                                    Formal Mathematics Statement Curriculum Learning

that this continuously improving performance through ex-         5.2. Expert iteration on synthetic inequality statements
pert iteration stems from two effects: (i) the model finding
                                                                 In this section we propose to set St to the union of the state-
new original proofs for the same statements and (ii) the
                                                                 ments in mathlib-train and synth-ineq. Again, we uniformly
model closing marginally harder statements at each itera-
                                                                 set a = 1 and use θ0 and θ1 as described in section 4.4,
tion – which in turn provides more useful training data for
                                                                 except that they are now also trained on synth-ineq-train.
the next iteration. By iteration 9, the model is trained on
more than 90% generated data. We present in Appendix E           Similarly to the previous section, we report in figure 3 the
a few examples of original proofs found by our models on         cumulative pass rate for two loops, our standard expert
mathlib-train compared with their ground-truth versions.         iteration loop, and a proof search only loop where we don’t
                                                                 interleave training between iterations. The pass rates are
To verify our hypothesis that expert iteration is capable of
                                                                 reported split by values of ND (pooling together 0 ≤ NS ≤
closing a curriculum of increasingly difficult problems out
                                                                 7) which we found to be the main driver for difficulty.
of a set of problem statements, and that this capability is
independent of having access to ground-truth proofs, we
                                                                             Expert iteration                 Sample only
propose in the next section to study expert iteration applied
to a synthetically generated set of problems for which we           50        0                         50
                                                                              1
have fine-grained control on the difficulty of each statement.
                                                                    40        2                         40
                                                                              3
                                                                              4
5. Statement curriculum learning                                    30                                  30
                                                                              5
                                                                              6
In this section we focus on running expert iteration on syn-        20                                  20

thetic statements generated by an inequality generator. The
                                                                    10                                  10
use of synthetic statements enables us to control the dif-
ficulty of each statement to present evidence that expert            0                                  0
                                                                               2        4       6   8         2        4    6   8
iteration can hill-climb the intrinsic difficulty gradient of
the resulting set of statements. In particular, we show that,
at fixed compute budget, expert iteration eventually closes
                                                                 Figure 3. Cumulative pass rate for our expert iteration loop as well
proofs of hard statements that remain completely out of
                                                                 as a sample only loop where we skip re-training the model between
reach of simply sampling proof searches without interleaved      iterations. Pass rates are reported for each value of ND (pooling
training.                                                        together 0 ≤ NS ≤ 7).

5.1. Synthetic inequality generator
We designed a synthetic inequality statement generator for       Despite the challenging nature of these synthetic inequali-
Lean in the spirit of the INT (Wu et al., 2020) generator.       ties, figure 3 demonstrates that expert iteration is capable of
The generator consists in generating inequalities from well      learning the intrinsic curriculum induced by synth-ineq. In
known inequality theorems (AM-GM, Trivial inequality,            particular, expert iteration is capable of closing 6 problems
Cauchy-Schwarz, Bernoulli, Young, Hölder) and compos-            of difficulty ND = 6 without having been provided with
ing them. It is driven by two difficulty parameters: ND          any seed ground-truth proof for this difficulty level. Note
which controls depth of composition of inequalities and          that difficulty ND = 6 remains completely out of reach of
NS which controls the complexity of the input expressions        simply scaling the number of attempts per statements (the
to the composed inequalities. We provide details on its          sample only loop remaining stuck at 0 for ND = 6).
implementation in Appendix D.                                    This confirms on our synthetic statements dataset synth-ineq
Using this generator we generate a curriculum of 5600 in-        that not only expert iteration is capable of learning the cur-
equality statements (for which we don’t have proofs), 100        ricula occurring in a set of statements, but this process also
for each values of 0 ≤ NS ≤ 7 and 0 ≤ ND ≤ 6. We                 enables the emergence of new capabilities without the need
denote this set of statements as synth-ineq.                     for ground-truth proofs (ability to close, highly challenging,
                                                                 deeply composed inequalities).
To bootstrap our models capabilities on this specific task, we
also generate 100 statements of low difficulty (ND = 1 and
NS = 5) and formalize a proof for each of these statements.
                                                                 6. Targeting miniF2F
We refer to this dataset as synth-ineq-train. In the rest of     Motivated by the results from Section 5, we curated and
this paper we adjunct this training dataset to the tactic        manually formalized a set of math exercises to target
dataset used to train our models.                                miniF2F. miniF2F statements being quite out of distribu-
                                                                 tion compared to the distribution of statements present in
                                     Formal Mathematics Statement Curriculum Learning

mathlib (which typically includes generic theorems and lem-                    minif2f-valid                     minif2f-valid
mas but very few exercises), we hypothesized that if the
                                                                                                                 pass@1 mathlib
difficulty of this set of statements was made varied enough,                                                     pass@1 full
expert iteration could potentially leverage it to effectively                                           40
                                                                                                                 pass@8 mathlib
                                                                      45
shift our models’ distribution closer to miniF2F’s, and in                                                       pass@8 full

turn, improve their eventual performance on it.
                                                                                                        35


6.1. Formalization effort                                             40
                                                                                        mathlib a=1
                                                                                                        30
We manually formalized 327 statements2 drawn from the fol-                              mathlib a=2
                                                                                        full
lowing sources: 302 examples and exercises from Lehoczky
                                                                               2        4      6   8              2            4   6   8
& Rusczyk (a;b). The books are classic problem solving
textbooks for students in grades 7-12 preparing for contests
such as AMCs and AIMEs. 25 problems from the MATH
                                                                  Figure 4. Left: cumulative pass rate on miniF2F-valid for our
dataset (Hendrycks et al., 2021). All problems were drawn         expert iteration loop using our full curriculum (mathlib-train, synth-
from the train split of the dataset, focusing on difficulty 5     ineq and miniF2F-curriculum) compared to the expert iteration
problems (miniF2F only contains problems from the test            loop from section 4.6. The total number of attempts per iteration
split).                                                           in our full loop is 25k + 5.6k + 8 ∗ 327 ≈ 33.2k, which means
                                                                  the total compute deployed is higher than in the mathlib-train only
We refer to Zheng et al. (2021) for more details on the
                                                                  loop (25k). We therefore also report in dotted a mathlib-train only
formalization procedure and the typical time needed for it        loop, taking a = 2, whose total number of attempts per iteration is
as these problems were formalized in similar conditions.          ≈ 50k. Right: pass@1 (plain) and pass@8 (dotted) for our expert
We denote this set of statements as miniF2F-curriculum            iteration loop using our full curriculum (mathlib-train, synth-ineq
and verified (based on problem provenance and manual              and miniF2F-curriculum) compared to the expert iteration loop
inspection of statements) that it had an empty intersection       from section 4.6.
with miniF2F-{test,valid}.

6.2. Transfer to miniF2F
In this section we propose to set St to the union of the state-   effective transfer between miniF2F-curriculum, synth-ineq
ments in mathlib-train, synth-ineq and miniF2F-curriculum.        and miniF2F-valid through expert iteration. We’ll denote
We uniformly set a = 1 on mathlib-train and synth-ineq            the fully iterated model from this section as θ9full .
and a = 8 on miniF2F-curriculum and use θ0 and θ1 as
described in section 5.                                           6.3. Results

Similarly to previous sections, we report in figure 4 (left)      We report in table 2 the pass rates on mathlib-{valid, test}
the cumulative pass rate on miniF2F-valid of our full cur-        and miniF2F-{valid, test} for the models trained in previous
riculum expert iteration loop and compare them with the           sections, namely θ1 , θ9mathlib , and θ9full . We achieve a 47.3%
mathlib-train only expert iteration from section 4.6. Since       pass rate (using a = 64 attempts) on miniF2F-valid and a
more compute is deployed in our full-curriculum loop (more        36.6% pass rate on miniF2F-test, substantially improving
statements) we also report a mathlib-train only loop taking       from the previous state-of-the-art (Zheng et al., 2021).
a = 2. At the end of the expert iteration, 100 out of the 327     These results include the resolution of 26 AMC12
statements from miniF2F-curriculum end up being closed,           problems, 6 AIME problems and 2 problems adapted
suggesting a lack of density in our manually formalized set       from the IMOs. Out of these statements, 4 AMC12
of statement.                                                     problems (amc12b_2020_p5, amc12a_2009_p9,
We also report in figure 4 (right) the pass@1 and pass@8          amc12a_2003_p24, amc12b_2003_p17), 2 AIME
for our full curriculum expert iteration loop. The steady im-     problems     (aime_1984_p1,              aime_1990_p4),
provement on miniF2F-valid shows that the expert iteration        and 2 IMO-adapted problems (imo_1961_p13 ,
procedure we propose does not overfit on the statements           imo_1964_p2) are uniquely solved by expert iter-
that compose the curriculum it uses. Despite the potential        ated models, the two IMO-adapted and the two AIME
inefficiency of our curriculum, the improved performance          problems being uniquely solved by θ9full .
associated with its use demonstrates, as hypothesized, an         We provide a selection of the proofs found by our models
   2
   https://github.com/openai/miniF2F/tree/                           3
                                                                      Note that this IMO-adapted statement from miniF2F-valid is
statement_curriculum_learning/lean/src/                           a much weaker version than the original problem (see Appendix F
statement_curriculum_learning                                     for more context)
                                        Formal Mathematics Statement Curriculum Learning

                                                                        Indicatively, with our 774m parameters model, running a
Table 2. Performance of θ1 (value-function based search), θ9mathlib     full expert iteration to train θ9full required about 2000 A100
(expert iterated on mathlib-train) and θ9full (expert iterated on our
                                                                        days of compute. Running one full proof search (a = 1
full curriculum) on mathlib-{valid, test} and miniF2F-{valid, test}.
All proof searches are run with d = 512 and e = 8.
                                                                        d = 512 e = 8) when properly parallelised, requires on
                                                                        average about 0.1 A100 hour of compute.

 Model                            pass@1      pass@8      pass@64       7.2. Limitations
 mathlib-valid
  PACT (Han et al., 2021)          48.4%            -            -      Despite our models’ capability, as discussed in Ap-
  θ1                               56.3%       66.3%        72.0%       pendix F.1, to generate cuts and witnesses, we believe that
  θ9mathlib                        62.6%       70.7%        75.8%       their current main limitation lies in their inability (under
  θ9full                           61.7%       69.8%        75.3%       our proposed search procedure) to chain more than 2 or
 mathlib-test                                                           3 non-trivial steps of mathematical reasoning, preventing
  θ1                               56.5%       66.9%        73.7%
                                                                        them from consistently (instead of exceptionally) solving
  θ9mathlib                        63.0%       71.5%        77.1%
  θ9full                           62.9%       71.6%        76.3%
                                                                        challenging olympiad problems. We’ve been repeatedly
                                                                        impressed by the complexity of some of the proofsteps gen-
 miniF2F-valid                                                          erated by our models. But, proofs requiring many of such
  PACT (Zheng et al., 2021)        23.9%       29.3%             -
  θ1                               28.5%       35.5%        41.2%       reasoning steps remain beyond our current compute horizon.
  θ9mathlib                        31.3%       38.3%        44.1%       Even if we solved a selection of challenging olympiad prob-
  θ9full                           33.6%       41.2%        47.3%       lems, our models are still very far from being competitive
 miniF2F-test                                                           with the brightest students in these competitions.
  PACT (Zheng et al., 2021)        24.6%       29.2%             -
  θ1                               25.9%       31.1%        33.6%       While our models have demonstrated some capabilities to
  θ9mathlib                        27.2%       33.0%        35.2%       generate cuts, the cuts they generate are often shallow (they
  θ9full                           29.6%       34.5%        36.6%       involve only a few proofsteps and don’t necessarily deeply
                                                                        change the structure of the proof–we refer the reader to the
                                                                        Cut-Elimination theorem and Carbone & Semmes (1996)
                                                                        for a discussion of the influence of cuts on proof size). We
for these statements as well as a qualitative analysis of them          believe that studying language models’ ability to generate
in Appendix F.                                                          cuts, and designing search procedures that leverage that
Also, we achieve a higher than 75% pass rate (using a = 64              capability (related ideas can be found in Czechowski et al.
attempts) on mathlib-{valid, test} (a new state-of-the-art as           (2021)), are interesting avenues of research to alleviate this
well) suggesting that our models have the potential to be               limitation.
effectively leveraged as proof assistants in the formalization
efforts associated with mathlib.                                        8. Conclusion
                                                                        In this paper we presented an expert iteration procedure
7. Discussion                                                           for GPT-f (Polu & Sutskever, 2020), demonstrating that it
7.1. Model Size                                                         is capable of solving a curriculum of increasingly difficult
                                                                        problems out of a set of formal statements of sufficiently var-
Throughout this paper, we used a single model size (774m                ied difficulty. Our results suggest that the lack of self-play
trainable parameters). We briefly experimented with dif-                in the formal mathematics setup can be effectively compen-
ferent model sizes (not reported in this paper) and found               sated for by automatically as well as manually curated sets
that model size scaling is not as straightforward as in the             of formal statements, which are much cheaper to formalize
case of unsupervised learning (Kaplan et al., 2020). We                 than full proofs. Finally, we hope that the statement curricu-
found that bigger models are better, in the sense that they             lum learning methodology we presented in this work will
consistently exhibit higher pass@1. But, they are also much             help accelerate progress in automated reasoning, especially
more expensive to sample from. And despite their pass@1                 if scaled with automated generation and curation of formal
being higher, it is often the case that for a fixed amount              statements in the future.
of compute, sampling more attempts from a smaller model
leads to a better final performance.
                                                                        References
For the compute budget we had available, we estimated the
model size we used to be a compelling trade-off. We leave               Lean theorem prover.             https://leanprover.
as future work a more thorough study of these dynamics to                 github.io/about/.
better understand the different compute frontiers involved.
                                    Formal Mathematics Statement Curriculum Learning

Bansal, K., Loos, S., Rabe, M., Szegedy, C., and Wilcox, S.      Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart,
  Holist: An environment for machine learning of higher            S., Tang, E., Song, D., and Steinhardt, J. Measuring math-
  order logic theorem proving. In International Conference         ematical problem solving with the math dataset. arXiv
  on Machine Learning, pp. 454–463, 2019a.                         preprint arXiv:2103.03874, 2021.

Bansal, K., Loos, S. M., Rabe, M. N., and Szegedy, C.            Huang, D., Dhariwal, P., Song, D., and Sutskever, I.
  Learning to reason in large theories without imitation.          Gamepad: A learning environment for theorem proving.
  arXiv preprint arXiv:1905.10501, 2019b.                          arXiv preprint arXiv:1806.00608, 2018.
Berner, C., Brockman, G., Chan, B., Cheung, V., D˛ebiak, P.,     Irving, G., Szegedy, C., Alemi, A. A., Eén, N., Chollet,
  Dennison, C., Farhi, D., Fischer, Q., Hashme, S., Hesse,          F., and Urban, J. Deepmath-deep sequence models for
  C., et al. Dota 2 with large scale deep reinforcement             premise selection. In Advances in Neural Information
  learning. arXiv preprint arXiv:1912.06680, 2019.                  Processing Systems, pp. 2235–2243, 2016.
Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan,
                                                                 Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B.,
  J., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G.,
                                                                   Chess, B., Child, R., Gray, S., Radford, A., Wu, J., and
  Askell, A., et al. Language models are few-shot learners.
                                                                   Amodei, D. Scaling laws for neural language models.
  arXiv preprint arXiv:2005.14165, 2020.
                                                                   arXiv preprint arXiv:2001.08361, 2020.
Browne, C. B., Powley, E., Whitehouse, D., Lucas, S. M.,
  Cowling, P. I., Rohlfshagen, P., Tavener, S., Perez, D.,       Karras, T., Laine, S., and Aila, T. A style-based genera-
  Samothrakis, S., and Colton, S. A survey of monte carlo          tor architecture for generative adversarial networks. In
  tree search methods. IEEE Transactions on Computa-               Proceedings of the IEEE/CVF Conference on Computer
  tional Intelligence and AI in games, 4(1):1–43, 2012.           Vision and Pattern Recognition, pp. 4401–4410, 2019.

Buzzard, K., Commelin, J., and Massot, P. Lean perfectoid        Lehoczky, S. and Rusczyk, R. The Art of Problem Solving,
  spaces.      https://leanprover-community.                       Volume 1: the Basics, a. ISBN:978-0-9773045-6-1.
  github.io/lean-perfectoid-spaces/,
  2019.                                                          Lehoczky, S. and Rusczyk, R. The Art of Problem Solving,
                                                                   Volume 2: and Beyond, b. ISBN:978-0-9773045-8-5.
Carbone, A. and Semmes, S. Making proofs without modus
  ponens: An introduction to the combinatorics and com-          Li, W., Yu, L., Wu, Y., and Paulson, L. C. Modelling high-
  plexity of cut elimination. Bulletin of the American Math-       level mathematical reasoning in mechanised declarative
  ematical Society, 34:131–159, 1996.                              proofs. arXiv preprint arXiv:2006.09265, 2020.
Czechowski, K., Odrzygóźdź, T., Zbysiński, M., Zawalski,      Loos, S., Irving, G., Szegedy, C., and Kaliszyk, C.
  M., Olejnik, K., Wu, Y., Kucinski, L., and Miłoś, P. Sub-       Deep network guided proof search. arXiv preprint
  goal search for complex reasoning tasks. Advances in             arXiv:1701.06972, 2017.
  Neural Information Processing Systems, 34, 2021.
                                                                 Megill, N. D. and Wheeler, D. A. Metamath: A
de Moura, L., Kong, S., Avigad, J., Van Doorn, F., and von
                                                                  Computer Language for Pure Mathematics, 2019.
  Raumer, J. The lean theorem prover (system description).
                                                                  URL http://us.metamath.org/downloads/
  In International Conference on Automated Deduction, pp.
                                                                  metamath.pdf.
  378–388. Springer, 2015.

Devlin, J., Chang, M.-W., Lee, K., and Toutanova, K. Bert:       Polu, S. and Sutskever, I. Generative language model-
  Pre-training of deep bidirectional transformers for lan-         ing for automated theorem proving. arXiv preprint
  guage understanding. arXiv preprint arXiv:1810.04805,            arXiv:2009.03393, 2020.
  2018.
                                                                 Rabe, M. N., Lee, D., Bansal, K., and Szegedy, C. Mathe-
Firoiu, V., Aygun, E., Anand, A., Ahmed, Z., Glorot, X.,           matical reasoning via self-supervised skip-tree training.
  Orseau, L., Zhang, L., Precup, D., and Mourad, S. Train-         arXiv preprint arXiv:2006.04757, 2020.
  ing a first-order theorem prover from synthetic data. arXiv
  preprint arXiv:2103.03798, 2021.                               Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G.,
                                                                   Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J.,
Han, J. M., Rute, J., Wu, Y., Ayers, E. W., and Polu, S. Proof     et al. Learning transferable visual models from natural
  artifact co-training for theorem proving with language           language supervision. arXiv preprint arXiv:2103.00020,
  models. arXiv preprint arXiv:2102.06203, 2021.                   2021.
                                     Formal Mathematics Statement Curriculum Learning

Ramesh, A., Pavlov, M., Goh, G., Gray, S., Voss, C., Rad-         Zheng, K., Han, J. M., and Polu, S. Minif2f: a cross-system
  ford, A., Chen, M., and Sutskever, I. Zero-shot text-             benchmark for formal olympiad-level mathematics. arXiv
  to-image generation. arXiv preprint arXiv:2102.12092,             preprint arXiv:2109.00110, 2021.
  2021.

Scholze, P. Liquid tensor experiment. https:
  //xenaproject.wordpress.com/2020/
  12/05/liquid-tensor-experiment/, 2020.

Selsam, D., Lamm, M., Bünz, B., Liang, P., de Moura, L.,
  and Dill, D. L. Learning a sat solver from single-bit
  supervision. arXiv preprint arXiv:1802.03685, 2018.

Silver, D., Huang, A., Maddison, C. J., Guez, A., Sifre, L.,
  Van Den Driessche, G., Schrittwieser, J., Antonoglou, I.,
   Panneershelvam, V., Lanctot, M., et al. Mastering the
   game of go with deep neural networks and tree search.
   nature, 529(7587):484–489, 2016.

Silver, D., Hubert, T., Schrittwieser, J., Antonoglou, I., Lai,
   M., Guez, A., Lanctot, M., Sifre, L., Kumaran, D., Grae-
   pel, T., et al. Mastering chess and shogi by self-play
  with a general reinforcement learning algorithm. arXiv
   preprint arXiv:1712.01815, 2017.

Tan, M. and Le, Q. Efficientnet: Rethinking model scaling
  for convolutional neural networks. In International Con-
  ference on Machine Learning, pp. 6105–6114. PMLR,
  2019.

Urban, J. and Jakubův, J. First neural conjecturing datasets
  and experiments. arXiv preprint arXiv:2005.14664, 2020.

Vinyals, O., Babuschkin, I., Czarnecki, W. M., Mathieu, M.,
  Dudzik, A., Chung, J., Choi, D. H., Powell, R., Ewalds,
  T., Georgiev, P., et al. Grandmaster level in starcraft ii
  using multi-agent reinforcement learning. Nature, 575
  (7782):350–354, 2019.

Wang, M., Tang, Y., Wang, J., and Deng, J. Premise selec-
 tion for theorem proving by deep graph embedding. In
 Advances in Neural Information Processing Systems, pp.
 2786–2796, 2017.

Wu, Y., Schuster, M., Chen, Z., Le, Q. V., Norouzi, M.,
 Macherey, W., Krikun, M., Cao, Y., Gao, Q., Macherey,
 K., et al. Google’s neural machine translation system:
 Bridging the gap between human and machine translation.
 arXiv preprint arXiv:1609.08144, 2016.

Wu, Y., Jiang, A. Q., Ba, J., and Grosse, R. Int: An inequal-
 ity benchmark for evaluating generalization in theorem
 proving. arXiv preprint arXiv:2007.02924, 2020.

Yang, K. and Deng, J. Learning to prove theorems
  via interacting with proof assistants. arXiv preprint
  arXiv:1905.09381, 2019.
                                    Formal Mathematics Statement Curriculum Learning

A. Related Work
Deep learning applied to premise selection and proof guidance Early applications of deep learning to formal mathe-
matics focused primarily on premise selection and proof guidance. DeepMath (Irving et al., 2016) explored the use of CNNs
and RNNs to predict whether a premise is useful to demonstrate a given conjecture. Their results were later improved with
FormulaNet (Wang et al., 2017) by the use of graph neural networks, reminiscent of NeuroSAT (Selsam et al., 2018). Proof
guidance consists in selecting the next clause to process inside an automated theorem prover. Loos et al. (2017) investigated
the use of models similar to DeepMath’s for proof guidance and demonstrated a significant uplift on the Mizar library.
More recently Firoiu et al. (2021) demonstrated the potential of deep learning techniques to be competitive with E prover’s
heuristics when applied to resolution calculus while training on fully synthetic data.

Deep learning applied to automated theorem-proving HOList (Bansal et al., 2019a) proposes a formal environment
based on HOL Light. They achieve their best performance (Bansal et al., 2019b) with a GNN model designed for premise
selection and the use of exploration. The same team studied the use of a skip-tree objective with Transformers on formal
statements (Rabe et al., 2020), demonstrating, along with GPT-f (Polu & Sutskever, 2020), the potential of leveraging
Transformers for formal reasoning. GamePad (Huang et al., 2018) and CoqGymn/ASTactic (Yang & Deng, 2019) introduce
environments based on the Coq theorem prover. ASTactic generates tactics as programs by sequentially expanding a
partial abstract syntax tree. Urban & Jakubův (2020) studied the capability of GPT-2 to produce useful conjectures for the
Mizar library and IsarStep (Li et al., 2020) explored the synthesis of intermediate propositions in declarative proofs for
Isabelle/HOL using Transformers.

B. Lean-gym
lean-gym presents the following API:

  • init-search: declaration → tactic_state. Takes a declaration name (a theorem name from the loaded library)
    and initializes a search while setting the run-time environment at that particular declaration. It returns the initial tactic
    state along with a fresh search_id and tactic_state_id.
  • run_tac: (tactic_state, tactic) → tactic_state. Takes a search_id and a tactic_state_id to identify a
    tactic state, as well as a tactic string to apply to it. It returns a new tactic state and its associated tactic_state_id.

Below is an example in-terminal trace demonstrating the use of lean-gym’s REPL interface:

$ lean --run src/repl.lean
["init_search", ["int.prime.dvd_mul", ""]]
{
  "error":null,
  "search_id":"0",
  "tactic_state":"` ∀ {m n : Z} {p : N}, nat.prime p →
                     ↑p | m * n → p | m.nat_abs ∨ p | n.nat_abs",
  "tactic_state_id":"0"
}
...
["run_tac",["1","1","apply (nat.prime.dvd_mul hp).mp"]]
{
  "error":null,
  "search_id":"1",
  "tactic_state":"m n : Z, p : N, hp : nat.prime p, h : ↑p | m * n
                   ` p | m.nat_abs * n.nat_abs",
  "tactic_state_id":"2"
}
...

Using lean-gym is virtually equivalent to opening a Lean editor at a specific theorem, deleting its proof and interacting
with Lean to reconstruct it.
                                   Formal Mathematics Statement Curriculum Learning


                         Table 3. Mix and source of data involved in the updated WebMath pre-training.
                                           Dataset                     Size    Mix
                                           Github Python           179 GB     25%
                                           arXiv Math               10 GB     25%
                                           Math StackExchange        2 GB     25%
                                           PACT mix2                28 GB     17%
                                           Math Overflow            200 M      5%
                                           ProofWiki                 30 M      2%
                                           PlanetMath                25 M      1%



Providing a REPL interface over the standard input/output makes it very easy to integrate lean-gym from any programming
language. Writing a wrapper in Python, as an example, only takes a few dozen lines of code. Since lean-gym is a Lean
program, managing the loaded libraries is done directly using Lean’s own infrastructure (using leanpkg.toml), making
it quite straightforward to have access to both mathlib and miniF2F statements from the same lean-gym instance.
Note that lean-gym is stateful, meaning that distributing proof searches on multiple lean-gym instances requires to
track which instance is associated with which proof search. In practice, we were able to scale the use of lean-gym to
thousands of cores running thousands of proof searches in parallel. Finally, lean-gym’s REPL interface is blocking,
preventing inner-proof search parallelization, though this limitation can probably be removed in the future.

C. WebMath
Our updated WebMath pre-training dataset consists in the mix presented in table 3.
As demonstrated in table 3, we empirically up-weighted (compared to their token size) parts of WebMath with high-quality
mathematical content while making sure they don’t overfit (despite running >1 epochs for some of them). We also included
PACT mix2 directly in the WebMath pre-training to avoid having to sequence more than two pre-training phases to prepare
Lean models.

D. Synthetic inequalities
D.1. Design
The generator consists of three phases:

Seed expressions generation The first phase consists in generating seed expressions for which we track the sign. We start
by initializing an expression set E composed of tuples of expressions and sign constraints, by generating nv variable names
(letters) assumed strictly positive as well as nn integers (for which we know the sign). For NS rounds, we compose elements
of E using unary (log(·), log(1/·), sqrt(·)) or binary operations (+, −, ×, /, ∧, max, min) for which we can deduce the
sign based on the sign condition of the input expression(s) and re-inject the resulting expression and sign constraint in E.
This produces a set E of signed seed expressions of size nv + nn + NS .

Inequality composition The second phase consists in generating inequalities from well known inequality theorems (AM-
GM, Trivial inequality, Cauchy-Schwarz, Bernoulli, Young, Hölder) taking as input to these theorems expressions from E
based on the sign constraints required for each theorem. We finally compose these inequalities ND times using compositions
theorems detailed in D.2. The resulting inequality is a composed inequality of depth ND based on nv + nn + NS seed
expressions.

Simplification We finally post-process these inequalities so that they are parsable by Lean and run them through Lean’s
simp tactic for a final simplification.
ND and NS together control for the difficulty of the resulting inequality. ND controls depth of composition, while NS
controls for obfuscation as it increases the complexity of the input expressions to the composed inequalities. When sampling
inequalities, we nn = 4 and randomly sample 2 ≤ nv ≤ 8 at each generation. We report below examples of generated
inequalities for various values of ND and NS .
                                   Formal Mathematics Statement Curriculum Learning

D.2. List of inequality composition theorems
Below is the list of theorem names from mathlib that we use to compose inequalities together. One third of the time, we only
transform the current composed inequality with one of the following theorems:

  • neg_le_neg
  • inv_le_inv

  • mul_self_le_mul_self
  • div_le_one_of_le

We otherwise compose the current composed inequality with a newly generated inequality using the following theorems:

  • mul_le_mul
  • add_le_add

  • div_le_div
  • mul_le_mul_of_nonneg
  • le_mul_of_ratio

D.3. Examples
ND = 0 NS = 0

       Compositions             AmGm a b (67:R) ((1:R)/(10:R)) ((1:R)/(10:R)) ((8:R)/(10:R))

                             theorem synthetic_ineq_nb_seed_var_0_depth_0_p_1
                               (a b : R)
                               (h0 : 0 < a)
         Statement             (h1 : 0 < b) :
                               (67:R) ^ ((8:R) / (10:R)) * b ^ (10:R)− ¹ *
                                 a ^ (10:R)− ¹ ≤ (8:R) / (10:R) * (67:R) +
                                 (10:R)− ¹ * a + b * (10:R)− ¹ := sorry



ND = 0 NS = 4

       Compositions          Sqnonneg a ((a) + ((-68:R)))

                             theorem synthetic_ineq_nb_seed_var_4_depth_0_p_4
                               (a b : R)
                               (h0 : 0 < a)
         Statement             (h1 : 0 < b) :
                               (2:R) * (a * (a + -(68:R))) ≤
                                 (a + -(68:R)) ^ 2 + a ^ 2 := sorry
                        Formal Mathematics Statement Curriculum Learning

ND = 4 NS = 4

                    AddLeAdd
                    Bernoulli 99 c
                    AddLeAdd
                    SelfDivConst ((a) / (f)) 6
     Compositions   LeMulOfRatio
                    SelfDivConst c 70
                    DivLeDiv
                    Cauchy ((a) / (f)) d c (log (((59:R) + f)))
                    Young ((a) / (f)) a ((3:R)/(2:R)) ((3:R)/(1:R))

                    theorem synthetic_ineq_nb_seed_var_4_depth_4_p_13
                      (a b c d e f : R)
                      (h0 : 0 < a)
                      (h1 : 0 < b)
                      (h2 : 0 < c)
                      (h3 : 0 < d)
                      (h4 : 0 < e)
       Statement      (h5 : 0 < f) :
                      (1:R) + (99:R) * c + (a / f / (6:R) + a * (a / f) /
                        ((d ^ 2 + a ^ 2 / f ^ 2) *
                        (real.log ((59:R) + f) ^ 2 + c ^ 2))) ≤
                        ((a / f) ^ ((3:R) / (2:R)) / ((3:R) / (2:R)) +
                        a ^ 3 / (3:R)) /
                        (real.log ((59:R) + f) * d + a / f * c) ^ 2 *
                        (c / (c / (70:R))) + a / f + (c + (1:R)) ^ 99 := sorry
                                   Formal Mathematics Statement Curriculum Learning

E. Example proofs from mathlib-train
We present in this section original proofs found by our models from mathlib-train, compared with their ground-truth version.

comap_eq_of_inverse

                             lemma comap_eq_of_inverse {f : filter α} {g : filter β}
                               {φ : α → β} (ψ : β → α) (eq : ψ ◦ φ = id)
         Statement             (hφ : tendsto φ f g) (hψ : tendsto ψ g f) :
                               comap φ g = f :=

                             begin
                               refine ((comap_mono $
                                 map_le_iff_le_comap.1 hψ).trans _).antisymm
        Ground-truth             (map_le_iff_le_comap.1 hφ),
                               rw [comap_comap, eq, comap_id],
                               exact le_rfl
                             end

                             begin
                               refine le_antisymm _ (filter.map_le_iff_le_comap.1 hφ),
                               refine λ s hs, _,
        Model proof            rw mem_comap,
                               use [ψ − ¹’ s, hψ hs],
                               rw [← preimage_comp, eq, preimage_id]
                             end
                          Formal Mathematics Statement Curriculum Learning

sum_range_sub_sum_range

                    lemma sum_range_sub_sum_range {α : Type*} [add_comm_group α]
      Statement       P : N → α} {n m : N} (hnm
                      {f                     P    : n ≤ m) :
                      P  k in range m, f k -    k in range n, f k =
                         k in (range m).filter (λ k, n ≤ k), f k :=

                    begin
                      rw [← sum_sdiff (@filter_subset _ (λ k, n ≤ k) _
                        (range m)), sub_eq_iff_eq_add,
                        ← eq_sub_iff_add_eq, add_sub_cancel’],
                      refine finset.sum_congr
     Ground-truth       (finset.ext $ λ a, 〈λ h, by simp at *; finish,
                        λ h, have ham : a < m :=
                          lt_of_lt_of_le (mem_range.1 h) hnm,
                          by simp * at *〉)
                        (λ _ _, rfl)
                    end

                    begin
                      rw [← sum_Ico_eq_sub _ hnm],
                      congr,
     Model proof      apply finset.ext,
                      simp [Ico.mem, *],
                      tauto
                    end
                        Formal Mathematics Statement Curriculum Learning

prod_inv_distrib

                                                 x in s, (f x)− ¹) =
                                               Q
                    lemma
                        Q prod_inv_distrib  : (
      Statement       (               −
                          x in s, f x) ¹ :=

                    begin
                      classical,
                      by_cases h : ∃ x ∈ s, f x = 0,
                      { simpa [prod_eq_zero_iff.mpr h, prod_eq_zero_iff]
                          using h },
                      { push_neg at h,
     Ground-truth       have h’ := prod_ne_zero_iff.mpr h,
                        have hf : ∀ x ∈ s, (f x)− ¹ * f x = 1 := λ x hx,
                        inv_mul_cancel (h x hx),
                        apply mul_right_cancel’ h’,
                        simp [h, h’, ← finset.prod_mul_distrib,
                          prod_congr rfl hf] }
                    end

                    begin
                      classical; induction s using
                        finset.induction_on with a s has ih,
     Model proof      { simp, },
                      simp only [has, prod_insert has, mul_inv_rev’],
                      finish
                    end
                                    Formal Mathematics Statement Curriculum Learning

F. Example proofs from minif2f-{test,valid,curriculum}
We present in this section proofs found by our models from minif2f-{test,valid,curriculum}, demonstrating some of the
capabilities emerging from our training procedure.

F.1. Qualitative analysis of proofs
We provide qualitative insights in the nature of the proofs found by our models, which we believe are useful to build a better
intuition of their capabilities beyond pass rate numbers. Throughout this section, we refer to statements and solutions found
by our models that are presented in Appendix F along with comments describing the specificity of each proof.
First, we observe that a large number of olympiad problems that are designed to be computationally challenging for humans
are rendered trivial for our models through the use of Lean tactics. As an example, mathd_numbertheory_447 which
is not necessarily considered straightforward for humans, can be closed in Lean by a simple refl (proof found by our
models).
In recent years, Lean’s mathlib community has developed high-powered tactics such as linarith/nlinarith
(solves (non)linear inequalities), norm_num (normalizes numerical expressions), simp (simplifies goals and hypotheses)
and ring (normalizes expressions in a ring). These tactics can be used with arguments to guide their underlying search
procedure. As mentioned in Zheng et al. (2021), we confirm here that our models acquire advanced capabilities to leverage
these high-level tactics by providing exogenous arguments which are not present in the current tactic state. The generation
of these exogenous arguments through language modeling seems to require a non-trivial amount of mathematical intuition.
imo_1964_p2, imo_1961_p1 and aime_1990_p15 are good examples of such uses.
We have also observed a number of proofs that require multiple non-trivial reasoning steps through the use of lower-
level tactics such as use, have, or by_cases that generally involve producing a witness or chaining implications,
requiring the generation of context specific exogenous terms. These interesting reasoning steps are structurally different
from simple normalization, simplification and rewriting of hypotheses or goals because they heavily rely on our models
ability to generate meaningful cuts or witnesses. This capability is, in our opinion, the most exciting stepping stone
towards solving more challenging mathematical problems. See, aopsbook_v2_c8_ex1, amc12b_2020_p6 and
mathd_train_algebra_217 for examples of such proofs.
More generally, we also observe that proofs generated by our models have a distinctive style compared to proofs formalized
by humans. This stems in part from the model’s capability to leverage high-level tactics in a way that is challenging for
humans as discussed in this section (e.g. one-liners such as nlinarith [sq_nonneg (x - y), sq_nonneg (y
- z)] where humans would generally decompose the problem in a less machine-like way). Additionally, as a result of our
search procedure and despite the bias towards shorter proofs introduced by our value function, extraneous proofsteps (such
as reversion/introduction of hypotheses, or no-op rewrites) are often interleaved with useful ones, which rarely happens in
human formalizations.
                            Formal Mathematics Statement Curriculum Learning

imo_1961_p1

                      Solve the system of equations:

                                                                   x+y+z =a
                                                              x + y 2 + z 2 = b2
                                                               2

 Natural language                                                        xy = z 2

                       where a and b are constants. Give the conditions that a and b must satisfy so that x, y, z (the
                      solutions of the system) are distinct positive numbers. Note: the formalized statement in miniF2F is
                      a weaker problem as it focuses on the second part of the question, providing the actual conditions,
                      and asking for a proof that the requirement entails them.
                      theorem imo_1961_p1
                         (x y z a b : R)
                         (h0 : 0 < x ∧ 0 < y ∧ 0 < z)
                         (h1 : x 6= y)
                         (h2 : y 6= z)
                         (h3 : z 6= x)
                         (h4 : x + y + z = a)
                         (h5 : x^2 + y^2 + z^2 = b^2)
                         (h6 : x * y = z^2) :
                         0 < a ∧ b^2 < a^2 ∧ a^2 < 3 * b^2 :=
                      begin
                         revert_all,
                         intros,
        Model proof      rw mul_comm,
                         split,
                         { nlinarith [sq_nonneg (x - y), sq_nonneg (y - z)], },
                         split,
                         { nlinarith [sq_nonneg (z - 1)], },
                         revert h3 h4 ,
                         field_simp [mul_comm a b],
                         rw [mul_comm, ← h5 ],
                         contrapose!,
                         rw mul_comm at h6 ,
                         rw mul_comm,
                         intro h,
                         nlinarith [sq_nonneg (x - y), sq_nonneg (y - z)]
                      end
        Comments      The model is able to close this problem by splitting into cases, contraposing for the last case and
                      using nlinarith. It must be noted that the arguments for the first two nlinarith uses are not
                      necessary, however the [sq_nonneg (x - y), sq_nonneg (y - z)] argument provided
                      on the last line is crucial to close the goal and are completely exogenous (present in no form in the
                      tactic state before).
                            Formal Mathematics Statement Curriculum Learning

imo_1964_p2

                      Suppose a, b, c are the sides of a triangle. Prove that
 Natural language
                                    a2 (b + c − a) + b2 (c + a − b) + c2 (a + b − c) ≤ 3abc
                      theorem imo_1964_p2
                        (a b c : R)
                        (h0 : 0 < a ∧ 0 < b ∧ 0 < c)
                        (h1 : c < a + b)
                        (h2 : b < a + c)
                        (h3 : a < b + c) :
        Model proof     a^2 * (b + c - a) + b^2 * (c + a - b) + c^2 * (a + b - c)
                          ≤ 3 * a * b * c :=
                      begin
                         nlinarith [sq_nonneg (b - a), sq_nonneg (c - b),
                           sq_nonneg (a - c), sq_nonneg (c - a)]
                      end
        Comments      The model is able to close an IMO problem in one-line. It correctly provides exogenous arguments to
                      nlinarith, which are necessary to close the goal. Note that either one of the last two arguments in
                      the sequence [sq_nonneg (b - a), sq_nonneg (c - b), sq_nonneg (a - c),
                      sq_nonneg (c - a)] can be omitted.
                            Formal Mathematics Statement Curriculum Learning

aime_1990_p15

                      Find ax5 + by 5 if the real numbers a, b, x, and y satisfy the equations

                                                                  ax + by = 3,
                                                               ax2 + by 2 = 7,
 Natural language                                              ax3 + by 3 = 16,
                                                               ax4 + by 4 = 42.


                      Note: the formalized statement in miniF2F provides the answer and asks for a proof of it.
                      theorem aime_1990_p15
                        (a b x y : R)
                        (h0 : a * x + b * y = 3)
                        (h1 : a * x^2 + b * y^2 = 7)
                        (h2 : a * x^3 + b * y^3 = 16)
                        (h3 : a * x^4 + b * y^4 = 42) :
                        a * x^5 + b * y^5 = 20 :=
        Model proof   begin
                        revert_all,
                        intros a b x y h3 h1 h2 h4 ,
                        ring_nf at h1 h2 ,
                        rw ← sub_eq_zero at h1 ,
                        nlinarith [sq_nonneg (x - y), sq_nonneg (a + b - 2),
                           sq_nonneg (x + y - (2:R)), sq_nonneg (a - b - 2)]
                      end
        Comments      The model is able to close a challenging AIME problem by providing crucial exogenous arguments
                      sq_nonneg (x - y) and sq_nonneg (x + y - (2 : R)) to nlinarith, which are
                      required to close the goal (while the other two can be removed).
                            Formal Mathematics Statement Curriculum Learning

mathd_train_algebra_217

                      Let f (x) = Ax + B and g(x) = Bx + A, where A 6= B.
 Natural language     If f (g(x)) − g(f (x)) = B − A, what is A + B? Note: the formalized statement in our curriculum
                      provides the answer and asks for a proof of it.
                      theorem mathd_train_algebra_217
                          (a b : R)
                          (f g : R → R)
                          (h0 : ∀ x, f x = a * x + b)
                          (h1 : ∀ x, f x = b * x + a)
                          (h2 : a 6= b)
                          (h3 : ∀ x, f (g x) - g (f x) = b - a) :
                          a + b = 0 :=
                      begin
        Model proof       revert_all,
                          intros a b,
                          intros f g,
                          contrapose!,
                          rintro 〈h0 , 〈h1 , h2 〉〉,
                          use (0 : R),
                          simp only [sub_eq_iff_eq_add, h0 , mul_zero] at *,
                          simp only [*, zero_add],
                          norm_num at h0
                      end
        Comments      The model is able to close the goal by contraposing, supplying a witness by the use of use (0 : R)
                      and finally leveraging the simp and norm_num. This example demonstrates the model’s ability to
                      chain multiple non-trivial steps of reasoning including the generation of witnesses.
                            Formal Mathematics Statement Curriculum Learning

amc12b_2020_p6

                      For all integers n ≥ 9, the value of

                                                               (n + 2)! − (n + 1)!
 Natural language                                                       n!
                      is always which of the following?
                      (A) a multiple of 4     (B) a multiple of 10       (C) a prime number
                      (D) a perfect square     (E) a perfect cube.
                      theorem amc12b_2020_p6
                        (n : N)
                        (h0 : 9 ≤ n) :
                        ∃ x : N, (x:R)^2 = (nat.factorial (n + 2) -
                          nat.factorial (n + 1)) / nat.factorial n :=
                      begin
        Model proof     revert_all,
                        intros n hn,
                        use n + 1,
                        field_simp [nat.factorial_ne_zero, pow_succ’],
                        ring_exp
                      end
        Comments      The model exhibits here its ability to implicitly interpret factorial expressions by guessing the correct
                      answer with the use of use n + 1 and straightforwardly proving its claim right after.
                            Formal Mathematics Statement Curriculum Learning

mathd_algebra_140

                      The expression 24x2 − 19x − 35 can be written as (Ax − 5)(2Bx + C), where A, B, and C are
 Natural language     positive numbers. Find AB − 3C. Note: the formalized statement in miniF2F provides the answer
                      and asks for a proof of it.
                      theorem mathd_algebra_140
                         (a b c : R)
                         (h0 : 0 < a ∧ 0 < b ∧ 0 < c)
                         (h1 : ∀ x, 24 * x^2 - 19 * x - 35 =
                            (((a * x) - 5) * ((2 * (b * x)) + c))) :
                         a * b - 3 * c = -9 :=
                      begin
                         revert_all,
                         rintro a b c h1 ,
                         rw mul_comm,
                         rw ←sub_eq_zero,
                         field_simp,
        Model proof      rw sub_eq_add_neg,
                         rw ← eq_neg_iff_add_eq_zero,
                         rw [mul_comm, ← sub_eq_add_neg, sub_eq_add_neg,
                         ← sub_eq_add_neg],
                         rw ←sub_eq_zero,
                         simp only [mul_add, neg_mul_eq_neg_mul_symm, mul_comm,
                         add_left_comm],
                         norm_num,
                         simp only [pow_two],
                         intro h0 ,
                         rw ← sub_eq_zero,
                         linarith [h1 .2, h1 .1, h0 3, h0 1, h0 2]
                      end
        Comments      The model mostly "struggles" to make progress up to the last line. There, it presents us with
                      the idea to specialize the statement given in h1 (which became h0 in the process of the proof) at
                      three consecutive natural numbers 1, 2, 3 which closes the goal with nlinarith. This proof is
                      interesting as it demonstrates the model’s ability to evaluate symbolic expressions implicitly.
                            Formal Mathematics Statement Curriculum Learning

aime_1984_p1

                      Find the value of a2 + a4 + a6 + a8 + . . . + a98 if a1 , a2 , a3 . . . is an arithmetic progression with
 Natural language     common difference 1, and a1 + a2 + a3 + . . . + a98 = 137. Note: the formalized statement in
                      miniF2F provides the answer and asks for a proof of it.
                      theorem aime_1984_p1
                         (u : N → Q)
                         (h0 : ∀  P n, u (n + 1) = u n + 1)
                         (h1 :
                         P            k in finset.range 98, u k.succ = 137) :
                             k in finset.range 49, u (2 * k.succ) = 93 :=
                      begin
                         revert_all,
                         simp [finset.sum_range_succ],
                         ring,
        Model proof      simp [pow_succ, mul_comm, add_left_comm, add_assoc],
                         simp [two_mul],
                         rintro p,
                         revert p,
                         simp [add_comm],
                         intros p hp,
                         simp [hp], ring_nf,
                         intros,
                         nlinarith
                      end
        Comments      The model finds a rather short proof of the statement compared to typical
                      human    formalizations (see   https://gist.github.com/MantasBaksys/
                      3efd5c0d42f440d16c09076db42822f2).
                            Formal Mathematics Statement Curriculum Learning

aopsbook_v2_c8_ex1

                                                n
 Natural language     Consider the sequence { n+1  } = 12 , 23 , 34 , ...
                      Prove that this sequence tends to 1 as n → ∞
                      theorem aopsbook_v2_c8_ex1
                         (u : N → R)
                         (h0 : ∀ n, u n = n / (n + 1)) :
                         filter.tendsto u filter.at_top (N 1) :=
                      begin
                         revert_all,
                         simp [← nnreal.coe_one],
                         norm_cast,
                         intros,
                         revert h0 ,
                         assume h,
                         simp [tendsto_const_nhds, ← nnreal.coe_one, h],
                         revert u,
                         assume f,
        Model proof      norm_num,
                         rw tendsto_iff_norm_tendsto_zero,
                         assume H,
                         convert tendsto_norm_zero.comp
                           tendsto_one_div_add_at_top_nhds_0_nat,
                         funext n,
                         have h0 : (((n:R) + 1) : R) 6= 0,
                         { norm_cast, exact n.succ_ne_zero, },
                         rw H,
                         field_simp [h0 , norm_neg],
                         ring,
                         rw [← sub_eq_zero],
                         simp [← sub_eq_zero],
                         simp [sub_eq_add_neg],
                      end
        Comments      An interesting example of a generated have statement, denoted by h0 , which is introduced as a cut
                      in order to simplify the expression containing divisions by using field_simp[h0 , norm_neg]
                      at a later step.


mathd_numbertheory_447

                      What is the sum of the units digits of all the multiples of 3 between 0 and 50? Note: the formalized
 Natural language
                      statement in miniF2F provides the answer and asks for a proof of it.
                      theorem
                         P        mathd_numbertheory_447 :
                             k in finset.filter (λ x, 3|x)
                         (finset.erase (finset.range 50) 0), (k % 10) = 78 :=
        Model proof   begin
                         refl
                      end
        Comments      Because the predicate λ x, 3|x is registered as decidable over N, we can state the problem by
                      using finset.filter, which is computable. Hence, refl is able to close the goal.
