                                             Ranking LLM-Generated Loop Invariants for Program Verification

                                              Saikat Chakraborty, Shuvendu K. Lahiri, Sarah Fakhoury, Madanlal Musuvathi,
                                              Akash Lal, Aseem Rastogi, Aditya Senthilnathan, Rahul Sharma, Nikhil Swamy
                                                                           Microsoft Research
                                                      {saikatc, shuvendu, sfakhoury, madanm, akashl, aseemr,
                                                              t-adityas, rahsha, nswamy}@microsoft.com


                                                               Abstract                               2020; Si et al., 2018).
                                                                                                         In recent years, Large Language Models
                                             Synthesizing inductive loop invariants is fun-
                                             damental to automating program verification.
                                                                                                      (LLMs) (Radford et al., 2018) have emerged as
                                             In this work, we observe that Large Language             foundational AI models that have revolutionized
arXiv:2310.09342v3 [cs.PL] 12 Feb 2024




                                             Models (such as gpt-3.5 or gpt-4) are capa-              Language Processing applications. Though LLMs
                                             ble of synthesizing loop invariants for a class          were originally proposed for natural languages,
                                             of programs in a 0-shot setting, yet require sev-        they have exhibited great success in formal lan-
                                             eral samples to generate the correct invariants.         guages such as programming languages (Chen
                                             This can lead to a large number of calls to a            et al., 2021). In fact, with the increased size, mod-
                                             program verifier to establish an invariant. To
                                                                                                      els have started to exhibit emergent properties. For
                                             address this issue, we propose a re-ranking ap-
                                             proach for the generated results of LLMs. We             example, modern LLMs such as gpt-3.5 (Ouyang
                                             have designed a ranker that can distinguish be-          et al., 2022), gpt-4 (OpenAI, 2023), PaLM (Chowd-
                                             tween correct inductive invariants and incor-            hery et al., 2022) are capable of reasoning about a
                                             rect attempts based on the problem definition.           given task with few-shot (Brown et al., 2020), or
                                             The ranker is optimized as a contrastive ranker.         even zero-shot prompting (Kojima et al., 2022).
                                             Experimental results demonstrate that this re-           Such an impressive footprint of LLM naturally
                                             ranking mechanism significantly improves the
                                                                                                      raises the question: How well can LLMs automati-
                                             ranking of correct invariants among the gen-
                                             erated candidates, leading to a notable reduc-
                                                                                                      cally synthesize inductive loop invariants?
                                             tion in the number of calls to a verifier. The              To this end, we employ two different state-of-the-
                                             source code and the experimental data for this           art LLMs for synthesizing loop invariants. We ob-
                                             paper are available in https://github.com/               serve that these models can generate well-formed
                                             microsoft/NeuralInvariantRanker.                         invariants, but finding the correct one often re-
                                                                                                      quires a large number of samples. A solution
                                         1   Introduction                                             based on guess and check, with the aid of an au-
                                         Program verification is a crucial step toward build-         tomated program verifier based on Z3 (De Moura
                                         ing trustworthy software. Unfortunately, the prob-           and Bjørner, 2008), can be computationally very
                                         lem of verifying properties of programs contain-             expensive due to several invocations on incorrect
                                         ing loops is undecidable. Verifying properties of            invariants. To minimize such costs, we propose
                                         programs containing loops boils down to inferring            reranking the generated invariants based on their
                                         loop invariants, which are facts that hold for any           likelihood of successful verification. Inspired by
                                         iteration of the loop, and also ensure the desired           the use of contrastive learning in information re-
                                         property. There is a rich body of prior work on syn-         trieval (Karpukhin et al., 2020), our approach,
                                         thesizing loop invariants for program verification           called iRank, transforms the problem and invariants
                                         through symbolic techniques (Cousot and Cousot,              to bring the correct solution closer in vector space
                                         1977; Colón et al., 2003; Graf and Saïdi, 1997;              while pushing away incorrect ones. Empirical re-
                                         McMillan, 2003), and their use in verifying safety           sults show that such re-ranking moves the median
                                         properties of real-world programs (Ball et al., 2001;        rank of the verified invariant to 4 in contrast to the
                                         Blanchet et al., 2003; Lahiri et al., 2009). More re-        expected median rank of 31 for the generations
                                         cently, there is a growing interest in the application       from gpt-3.5.
                                         of machine learning towards invariant synthesis                 In summary, in this paper, we propose to rerank
                                         (Garg et al., 2016; Padhi et al., 2016; Yao et al.,          the LLM-generated loop invariants to reduce the

                                                                                                  1
cost of wasted verification effort. We have de-
signed a ranker to contrast correct and incorrect                S    ::=        x := a | skip | S; S | if b then S else S
invariants and show a significant reduction in the               a    ::=           n | x | a + a | a − a | a ∗ a | ...
invariant checking effort compared to raw LLM                    b    ::=    true | false | a = a | a < a | b ∧ b | b ∨ b | ¬b

generations.
                                                              In its simplest form, the goal of program verifica-
2     Related Work                                         tion is to verify that a program fragment satisfies its
                                                           specifications denoted by the Hoare-triple (Hoare,
Prior works on loop invariant generation can be            1969) - {pre} while b do S {post}. Given a pro-
broadly grouped into symbolic or machine learn-            gram p and a pair of Boolean expressions (denoted
ing based. Symbolic approaches either construct            by b in the grammar) ϕ and ψ denoting the precon-
invariants that are correct by construction (Cousot        dition and postcondition of a program p, the Hoare-
and Cousot, 1977; Colón et al., 2003), or leverage         triple {ϕ} p {ψ} denotes that every terminating
Satisfiability-Modulo-Theories (SMT) solvers such          execution of p that starts in an pre-state satisfying
as Z3 (De Moura and Bjørner, 2008) to enumer-              the predicate ϕ ends up in a post-state that satisfies
ate and check candidate invariants over a space            the predicate ψ. Since loops can execute an un-
of pre-defined predicates (Flanagan and Leino,             bounded number of iterations, verifying programs
2001; Flanagan and Qadeer, 2002; Lahiri and                with a loop requires a loop invariant i that satisfies
Bryant, 2007; Gulwani et al., 2009; Fedyukovich            the following conditions:
and Bodík, 2018) or predicates constructed through                                           {pre} skip {i}
variants of Craig’s interpolants (McMillan, 2003;                                            {i ∧ b} S {i}                       (1)
Henzinger et al., 2004; Dillig et al., 2013). On                                       {i ∧ ¬b} skip {post}

the other hand, recent techniques leverage machine            The conditions respectively denote that the loop
learning to synthesize candidate invariants that are       invariant i holds on loop-entry, is preserved by an
checked for correctness using an SMT-based pro-            arbitrary iteration of the loop and implies the post
gram verifier. Techniques range from incorporating         condition on exit. The problem of loop invariant
the feedback from a verifier using active learning         inference is to infer an i that satisfies the three
over decision trees (Garg et al., 2016), learning          checks above, and denoted as i ⊢ p.
from counter examples (Sharma and Aiken, 2016;                Furthermore, for the loop-free statements S in
Padhi et al., 2016), reinforcement learning over           the grammar above, checking the Hoare-triple
graph neural networks (Si et al., 2018) and the            {ψ} S {ϕ} can be reduced to (decidable) logi-
use of continuous logic networks (Yao et al., 2020;        cal formulas in the Satisfiability-Modulo-Theories
Ryan et al., 2020). Unlike these techniques, our ap-       (SMT) using standard techniques in program ver-
proach leverages an LLM for generation and ranks           ification (Leino, 2010). One can use a predicate
using a purely neural model and does not require           transformer called weakest precondition WP to con-
a program verifier at the inference time. This is          vert the Hoare-triple to a decidable SMT formula
important for scenarios where the verifier is semi-        that can be checked by Z3.
automated, as is the case of most real-world pro-                                       ψ =⇒ WP(S, ϕ)
gram verification tools such as Dafny (Leino, 2010)                                       {ψ} S {ϕ}
and F* (Swamy et al., 2011). Finally, Pei et al.              The WP is defined inductively on the structure
(2023) predict program invariants using LLMs, but          of statements as follows:
they do not aim at generating inductive invariants                   WP(x := a, ϕ)
                                                                                               .
                                                                                               =              ϕ[a/x]
that are sufficient for formal program verification.                  WP(skip, ϕ)
                                                                                               .
                                                                                               =                 ϕ
                                                                                               .
                                                                     WP(S1 ; S2 , ϕ)           =        WP(S1 , WP(S2 , ϕ))
3     Background & Motivation                                                                  .    V    (b =⇒ WP(S1 , ϕ))
                                                             WP(if b then S1 else S2 , ϕ)      =
                                                                                                        (¬b =⇒ WP(S2 , ϕ))
3.1    Background: Loop Invariant Inference
In this section, we recall the problem of loop in-         3.2       Motivation and Problem Formulations
variant generation in program verification. First,         Given a problem definition p that consists of pre-
let us define a grammar for program statements S,          conditions pre, a loop while b do S, and postcon-
integral expressions a and Boolean expressions b,          ditions post, we can query LLMs to generate an
operating on scalar variables. Most statements and         invariant i that satisfies the conditions specified
expressions are self-explanatory.                          in Equation (1). Although we have observed that

                                                       2
                  Annotated example from training data
                                                           Wrong Invariant
                                                          Wrong Invariant
                                                         Wrong Invariant




                                                                                                                                                                                   Transformed Embedding
                                                                                                         Initial Embedding




                                                                                                                                                                                      (used for ranking)
                                                                                                         (wrong invariants)                             Increase Distance

                                                                Problem
                                                                                                         Initial Embedding
                                                                                                        (problem definition)                           Decrease Distance
                                                                                     Embedding
                                                                                       Model
                                                            Verified Invariant
                                                          Verified
                                                              Verified
                                                                    Invariant
                                                                        Invariant
                                                         Verified
                                                            Verified
                                                                  Invariant
                                                                      Invariant
                                                          Verified Invariant
                                                                                                           Initial Embedding         Embedding
                                                                                                          (correct invariants)    Transformation
                                                                                                                                    (3-layer fully
                                                                                                                                  connected ANN)
                                                                                                      iRank during Training


                   Invariant Synth. Problem
                   (define-fun pre_fun ...)                                                                                                Similarity (Dot Products)
                  (define-fun trans_fun ...)                                                                                        (problem emb. and candidate inv. emb.)
                  (define-fun post_fun ...)                                                                                                                            =>(<= i n)
                                                                                                                                                                         nor(<= n
                                                                                                                                                                       ((j and(<
                                                                                                                                                                            Int)) i n)
                  nor(<= n                                                                                                                                  0.7              or(<= i n)
                                                                                                                                                                        i forall((j
                   and(< i n)                                                                                                                                          (=> kforall((j
                                                                                                                                                                            (and (
                     or(<= i n)
                 i forall((j                                                                                                                                0.8               (forall((
                                                                                                                                                                         Int))   (=>
                       =>(<= i n)
                   kforall((j                                                                                                                               0.9             Int)) (=
                                                                                                                                                                           ...
                      (forall((
                  Int))  (=>                                                                                                                                             (andj (Int))(=>
                                                                                                                                                                                  ...
                       ((j (=
                    Int))   Int))                                                                                                                           0.5             (and (...
                 (andj (
                       Int))(=>
                          ...                                              Embedding                                                                                          (and ...
                       (=>(...
                    (and    (and (                                           Model
                      (and ...                                                                                                                                     Re-ranked Candidate
                           ...                                                                                                                                          Invatiants
                 Candidate Invariants                                                      Initial Embeddings                     Transformed Embeddings

                                                                                                     iRank during Ranking


                                                                                    Figure 1: LLM for Loop Invariant synthesis.


LLMs are capable of producing loop invariants                                                                          tract the embedding of problem definitions and the
without syntax errors, they often require numerous                                                                     invariants with an embedder, Φ, i.e., x = Φ(p),
samples before generating a correct invariant (we                                                                      and y = Φ(i), where x and y are the embeddings
refer to Appendix B for a details). This results in in-                                                                of problem definition p, and invariant i, respec-
efficient resource utilization during the verification                                                                 tively. We learn a transformation function, Ψ(x|θ),
process, particularly when dealing with complex                                                                        which applies non-linear transformation on input
problem instances. More importantly, for a more                                                                        vector x with learnable parameter θ. We then trans-
practical scenario where generated invariants are                                                                      form problem embedding x to x′ = Ψ(x|θ), and
used as part of an interactive verification system                                                                     transform invariant embedding y to y ′ = Ψ(y|θ).
such as Dafny/F*, an incorrect invariant would take                                                                    Now our target is to maximize the similarity be-
up valuable user time to perform a manual failed                                                                       tween x′ and y ′ , when y ′ corresponds to a cor-
verification effort. Consequently, we propose the                                                                      rect invariant, minimize the similarity otherwise.
utilization of iRank to prioritize the generated in-                                                                   We use the absolute cosine similarity as the mea-
variants based on their likelihood of being correct.                                                                   surement. Use of such allows us to set the max-
Figure 1 provides a high-level overview of the en-                                                                     imum similarity to 1 (in the case of correct in-
visioned invariant generation-ranking system.                                                                          variant) and the minimum to 0 (in the case of
                                                                                                                       wrong invariant). We optimize the mean squared
4   iRank: Methodology                                                                                                 error loss to learn the parameters in Ψ. We ex-
                                                                                                                       perimented with two different embedding models
The main intuition behind iRank is learning to pull
                                                                                                                       based on LLMs, i.e.,text-embedding-ada-002
the likely correct invariants to the front of a ranked
                                                                                                                       and davinci-similarity. Appendix A presents
list. Figure 1 shows a high-level overview of the
                                                                                                                       further details of iRank’s working procedure.
ranker. We rely on a dataset, D = {(p, I + , I − )},
containing Loop Invariant generation problem, p, a
                                                                                                                        5        Experimental Design and Results
set of verified loop invariants, I + = {i+ | i+ ⊢
p}, and a set of wrong loop invariant, I − =                                                                            5.1       Experimental Setup
{i− | i− ⊬ p} for each of the problems, to
build iRank. Our goal is to learn a function be-                                                                        Benchmarks. We use Loop Invariant Synthesis
tween a problem definition p and invariant i, i.e.,                                                                     benchmarks assimilated by Padhi et al. (2016) 1
σ(p, i), which should satisfy the following con-                                                                        constituting a set 940 challenge problems in Sy-
straint ∀{i+ ,i− } (σ(p, i+ ) > σ(p, i− )).                                                                                1
                                                                                                                             https://github.com/SaswatPadhi/LoopInvGen/
Contrastive Ranking. To learn σ, we first ex-                                                                           tree/master/benchmarks


                                                                                                                  3
Gus (Alur et al., 2013) format, with a SMT for-                                                   i+ ranks                V@K (%)
                                                                            Experiment
                                                                                                Mean   Median      K=1     K=5    k=10
mula for the pre-condition, post-condition, and the                         LLM-ranks          189.78     62.00     5.2    11.6   18.4
transfer-function for the loop. We chose a SMT                           Expected ranks         95.35     31.02     8.0    19.2   25.2
representation for our problem description p to be                             TF-IDF          103.45     24.00    17.6    32.0   38.8
agnostic to different encoding of C programs into                                  Ada         115.89     31.50    11.2    21.6   30.0
                                                                        Emb.
logic. Among these problems, 541 were in the                                       Davinci     120.02     32.00    10.4    20.8   33.6

scope of LLM due to the context window size. We                                    Ada          38.78      5.00    28.0    51.2   60.8
                                                                        iRank
                                                                                   Davinci      34.48      4.00    29.2    52.8   62.8
set the maximum context size as 4096 (with 3584                                 (a) Invariants generated by gpt-3.5-turbo .
for prompt, 512 for generation).
                                                                                                  i+ ranks                V@K (%)
Gathering LLM-generated Invariants. We con-                                 Experiment
                                                                                               Mean    Median      K=1     K=5    k=10
ducted experiments involving two distinct language                          LLM-ranks           39.20      9.00    17.6    40.4   51.6
models: gpt-3.5-turbo and gpt-4. Our objec-                              Expected ranks         20.23      4.96    31.9    52.1   65.4
tive was to assess the capabilities of these language                          TF-IDF           24.16      3.00   32.00    45.6   53.6
models out-of-the-box, and thus we employed a                           Emb.
                                                                                   Ada          20.69      5.50    26.6    51.1   64.9
                                                                                   Davinci      23.56      5.00    27.7    52.1   63.3
zero-shot prompting approach. This involved pro-
                                                                                   Ada          13.18      2.00    44.7    74.4   81.4
viding a problem description and an appropriate                         iRank
                                                                                   Davinci      11.96      2.00    44.7    71.8   81.9
task explanation as a prompt (refer to Appendix C                                       (b) Invariants generated by gpt-4 .
for an example). For each problem, we allowed                         Table 1: Comparison between different ranking strategies for
both the models to generate invariants for a maxi-                    re-ranking the invariants generated by different LLMs.
mum duration of 10 minutes or until a verified in-
variant was found, whichever occurred first, result-
ing in solving 250 problems by gpt-3.5-turbo,
                                                                      Baselines. (a) LLM-ranks. We take the invariants,
and 188 problems for gpt-42 . It is important to
                                                                      in the order generated by the LLMs, as a ranklist.
clarify that the purpose of this paper is not to con-
                                                                      (b) Expected-ranks. We estimate the expected val-
duct a comparative analysis of these language mod-
                                                                      ues of the evaluated metrics in this paper by ran-
els in relation to this specific problem. Instead,
                                                                      domly permuting the LLM-generated list of invari-
our objective is to propose a method to orthogo-
                                                                      ants (see Appendix D for more details). (c) Em-
nally augment LLM capabilities by reranking LLM
                                                                      beddings. We use the raw embeddings from LLM-
generated invariants.
                                                                      based embedding models to calculate similarity
Training Data. We create the training dataset for                     without training. (d) TF-IDF. We use the textual
iRank (D = {(p, I + , I − )}) by combining invari-                    similarity between the problem description and the
ants generated from different sources, such as dif-                   candidate invariants for ranking.
ferent generations from LLMs, and invariants gen-
                                                                      Research Questions. In this paper, we studied
erated by LoopInvGen (Padhi et al., 2017). We
                                                                      two research questions. (i) How effective are LLM-
divided the problems into five folds and trained 5
                                                                      based embeddings for ranking invariants? and (ii)
different rankers, one for each fold. During the
                                                                      Can a trained iRank help reduce the verification
evaluation, we select and load the trained model
                                                                      cost?
based on the problem under evaluation. Detailed
statistics of data is available in Appendix A.3.                      5.2      Results
Evaluation Metric. We then sequentially attempt
                                                                      Table 1 shows the quantitative evaluation of iRank.
to check invariants from a ranked list. We evaluate
                                                                      If we consider LLM-generated list of invariants as
three metrics – (i) i+ ranks - rank of the correct
                                                                      is, we observe that LLMs are able to generate a ver-
invariant in the list, (ii) V@K - the percentage of
                                                                      ified invariant after a significant number of wasted
problems where the verified invariant is found in
                                                                      trials. For example, on average, gpt-3.5-turbo
top K invariants from the re-ranked list, and (iii)
                                                                      found an invariant after ∼190 failed attempt at
Number of Z3 calls - the total number of z3 calls
                                                                      generation. gpt-4 does much better, in compar-
before finding and reporting a correct invariant, a
                                                                      ison, with the mean rank of verified invariants be-
higher number of z3 calls indicate a high waste of
                                                                      ing 39.20. The expected rank of the verified in-
computational resources.
                                                                      variant from LLM-generations is 95.35 and 20.23,
   2
     Note that the rate limit for gpt-4 was an order lower than       for gpt-3.5-turbo and gpt-4, respectively. The
gpt-3.5 in our usage resulting in an order less samples.              use of LLM-based embeddings (without any train-

                                                                  4
                                  500                                                                                                                                           1200




                                                                                                                                                                                                                                                                                      Rank of the verified invariant
Rank of the verified invariant
                                                                                                                                                                                1000                                                                                                                                   80                                                                                                                     200
                                  400




                                                                                                                                                                                                                                                                                                                                                                                                                         Number of Z3 calls
                                                                                                                                                     Number of Z3 calls
                                                                                                                                                                                 800                                                                                                                                   60                                                                                                                     150
                                  300
                                                                                                                                                                                 600
                                  200                                                                                                                                                                                                                                                                                  40                                                                                                                     100
                                                                                                                                                                                 400
                                  100                                                                                                                                                                                                                                                                                  20                                                                                                                      50
                                                                                                                                                                                 200
                                       0                                                                                                                                             0                                                                                                                                  0                                                                                                                       0




                                                                                                                                                                                                                                                                                                                                                                                 Ada emb.
                                                                                                                                                                                                                                                                                                                                                                                            iRank-Ada
                                                                                                                                                                                                                                                                                                                                                                                                         iRank-Davinci




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         Ada emb.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    iRank-Ada
                                                                                                                                                                                                                                                                                                                                        Expected Ranks
                                                                                                                                                                                                                                                                                                                                                         TF-IDF
                                                                                                                                                                                                                                                                                                                                                                  Davinci emb.
                                                                                                                                                                                                                                                                                                                            LLM Ranks




                                                                                                                                                                                                                                                                                                                                                                                                                                                    LLM Ranks
                                                                                                                                                                                                                                                                                                                                                                                                                                                                Expected Ranks
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 TF-IDF
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          Davinci emb.




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                iRank-Davinci
                                                                                                                 iRank-Ada




                                                                                                                                                                                                                                                          iRank-Ada
                                               LLM Ranks




                                                                                                      Ada emb.
                                                           Expected Ranks




                                                                                                                             iRank-Davinci




                                                                                                                                                                                         LLM Ranks




                                                                                                                                                                                                                                               Ada emb.



                                                                                                                                                                                                                                                                      iRank-Davinci
                                                                              TF-IDF

                                                                                       Davinci emb.




                                                                                                                                                                                                      Expected Ranks

                                                                                                                                                                                                                       TF-IDF

                                                                                                                                                                                                                                Davinci emb.
                                                                                 Experiments                                                                                                                              Experiments                                                                                                                       Experiments                                                                                                             Experiments

                                                                              Rank                                                                                                                         # Z3 calls                                                                                                                                     Rank                                                                                                         # Z3 calls
                                                                                                        (a) gpt-3.5-turbo.                                                                                                                                                                                                                                                                              (b) gpt-4.

                                                                                            Figure 2: Detailed results comparing ranks of the correct invariants and number of z3 calls.


                                                      LLM Ranks
                                                      Expected Ranks
                                                                                                          Ada emb.
                                                                                                          iRank-Ada
                                                                                                                                                                                              LLM Ranks
                                                                                                                                                                                              Expected Ranks
                                                                                                                                                                                                                                                 Ada emb.
                                                                                                                                                                                                                                                 iRank-Ada                                                              ference between text-embedding-ada-002 and
                                                      TF-IDF                                              iRank-Davinci                                                                       TF-IDF                                             iRank-Davinci
                                                      Davinci emb.                                                                                                                            Davinci emb.                                                                                                              davinci-similarity models, the performance
                                                                                                                                                                               100                                                                                                                                      differences are not different with statistical sig-
Percentage of Problems Verified




                                                                                                                                             Percentage of Problems Verified




                                  80
                                                                                                                                                                                80                                                                                                                                      nificance (with p-value > 0.1). In both models’
                                  60
                                                                                                                                                                                60
                                                                                                                                                                                                                                                                                                                        cases, there is no statistically significant difference
                                  40                                                                                                                                                                                                                                                                                    between the expected rank and raw embedding-
                                                                                                                                                                                40
                                  20                                                                                                                                                                                                                                                                                    based ranking. Note that, similar to the existing
                                                                                                                                                                                20
                                           0               10                   20        30       40                             50                                                 0               10             20        30       40                              50
                                                                                                                                                                                                                                                                                                                        works (Ryan et al., 2020), we use z3 call to mea-
                                                                            Top k Invariants Tried                                                                                                              Top k Invariants Tried                                                                                  sure resource wastage. However, depending on the
                                               (a) gpt-3.5-turbo                                                                                                                                      (b) gpt-4                                                                                                         system the experiments are carried on, the time
                                                                                                                                                                                                                                                                                                                        saved from reranking with iRank could be different.
  Figure 3: Percentage of problems solved w.r.t. number of
  invariants from the (re-)ranked list.                                                                                                                                                                                                                                                                                 We report our experimental results of wall clock
                                                                                                                                                                                                                                                                                                                        time in Appendix B (Table 2).
                                                                                                                                                                                                                                                                                                                           Figure 3 shows the percentage of problems veri-
  ing) such as from text-embedding-ada-002 or
                                                                                                                                                                                                                                                                                                                        fied after trying k invariants (V@K). We observe
  davinci-similarity results is the mean rank of
                                                                                                                                                                                                                                                                                                                        that the iRank curves are very steep at the begin-
  the verified invariant to be 115.89 and 120.02,
                                                                                                                                                                                                                                                                                                                        ning of the curves compared to the baseline, sig-
  respectively for gpt-3.5-turbo, and 20.69 and
                                                                                                                                                                                                                                                                                                                        nifying that it could rank the verified invariants in
  23.56, respectively for gpt-4. While such a result
                                                                                                                                                                                                                                                                                                                        significantly higher positions than baselines.
  looks like a significant improvement over LLM-
  ranks, it is slightly worse than expected ranks.
                                                                                                                                                                                                                                                                                                                            ✓ Contrastive training in iRank brings the veri-
                       ✓ LLM-based embeddings standalone may not                                                                                                                                                                                                                                                            fied invariant closer to the problem while pushing
                       serve well for reranking verified invariants.                                                                                                                                                                                                                                                        the wrong ones resulting in a significant reduc-
                                                                                                                                                                                                                                                                                                                            tion in the verification cost.
     The training procedure in iRank significantly
  contributes to improving the ranking of verified
  invariants by transforming the embeddings. The
  median rank of the verified invariant is 32 when                                                                                                                                                                                                                                                                      6               Conclusion
  using the embedding from davinci-similarity
  embeddings. With the contrastive training in                                                                                                                                                                                                                                                                          We presented a novel approach, iRank, to rank the
  iRank, the median rank is brought down to 4,                                                                                                                                                                                                                                                                          loop invariants generated by LLMs based on their
  showing a significant improvement. Such a trend                                                                                                                                                                                                                                                                       likelihood of being correct. Our ranker leverages
  persists across different embedding models and                                                                                                                                                                                                                                                                        a contrastive learning technique to discriminate
  generations from different LLMs. Figure 2a,                                                                                                                                                                                                                                                                           between correct and incorrect invariants. Our eval-
  and Figure 2b shows the detailed results invari-                                                                                                                                                                                                                                                                      uation demonstrates that our approach significantly
  ants generated by gpt-3.5-turbo and gpt-4.                                                                                                                                                                                                                                                                            reduces the invariant checking effort compared to
  In both trained and raw embeddings, the dif-                                                                                                                                                                                                                                                                          the original LLM outputs.

                                                                                                                                                                                                                                                                                              5
Limitations                                                 Thomas Ball, Rupak Majumdar, Todd D. Millstein, and
                                                              Sriram K. Rajamani. 2001. Automatic predicate ab-
Assumptions of LLM inference cost. In this                    straction of C programs. In Proceedings of the 2001
paper, we assumed the cost of calling LLMs is neg-            ACM SIGPLAN Conference on Programming Lan-
                                                              guage Design and Implementation (PLDI), Snowbird,
ligible compared to the cost of calling the verifier          Utah, USA, June 20-22, 2001, pages 203–213. ACM.
for checking an invariant. Current access to LLMs
(at least the one we studied in the paper) is avail-        Bruno Blanchet, Patrick Cousot, Radhia Cousot, Jérome
able through the rest API, which can be scaled up             Feret, Laurent Mauborgne, Antoine Miné, David
                                                              Monniaux, and Xavier Rival. 2003. A static analyzer
by the API vendor with distributed processing of              for large safety-critical software. In Proceedings of
LLM. However, with the increase in the problem                the ACM SIGPLAN 2003 Conference on Program-
complexity, i.e., non-linear invariants, high number          ming Language Design and Implementation, PLDI
of variables, the check for correctness of an invari-         ’03, page 196–207, New York, NY, USA. Association
                                                              for Computing Machinery.
ant become exponentially more expensive. In the
case where call to LLM is much more expensive               Tom Brown, Benjamin Mann, Nick Ryder, Melanie
than LLM, iRank will reduce the number of Z3                  Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind
calls, but may not contribute to actual cost savings.         Neelakantan, Pranav Shyam, Girish Sastry, Amanda
                                                              Askell, et al. 2020. Language models are few-shot
                                                              learners. Advances in neural information processing
Comparison with state-of-the-art (SOTA) invari-               systems, 33:1877–1901.
ant synthesis. The goal of this paper is not to
establish SOTA for loop invariant synthesis. In con-        Mark Chen, Jerry Tworek, Heewoo Jun, Qiming
trast, we investigate LLMs’ capacity to generate             Yuan, Henrique Ponde de Oliveira Pinto, Jared Ka-
                                                             plan, Harri Edwards, Yuri Burda, Nicholas Joseph,
Loop invariant relying on their emergent behav-              Greg Brockman, et al. 2021. Evaluating large
ior. iRank is proposed as an orthogonal tool and             language models trained on code. arXiv preprint
evaluated to rank LLM generations in this paper.             arXiv:2107.03374.
However, in theory, iRank should be able to rerank
                                                            Aakanksha Chowdhery, Sharan Narang, Jacob Devlin,
invariants generated by any generator. Neverthe-              Maarten Bosma, Gaurav Mishra, Adam Roberts,
less, the design of the SOTA technique of Loop                Paul Barham, Hyung Won Chung, Charles Sutton,
Invariant Synthesis with LLM (perhaps with other              Sebastian Gehrmann, et al. 2022. Palm: Scaling
tools) remain an open problem, which we leave for             language modeling with pathways. arXiv preprint
                                                              arXiv:2204.02311.
future research.
                                                            Michael A. Colón, Sriram Sankaranarayanan, and
Stability of LLM predictions. Due to the                      Henny B. Sipma. 2003. Linear invariant generation
stochastic (and nondeterministic 3 ) nature of the            using non-linear constraint solving. In Computer
LLM, especially in higher temp, we observe un-               Aided Verification, pages 420–432, Berlin, Heidel-
                                                              berg. Springer Berlin Heidelberg.
stable generation from the LLM. Nevertheless, we
evaluated the results from one sample run from              Patrick Cousot and Radhia Cousot. 1977. Abstract inter-
gpt-3.5-turbo and one from gpt-4 as case stud-                pretation: A unified lattice model for static analysis
ies. While we acknowledge the possibility of un-              of programs by construction or approximation of
                                                              fixpoints. In Proceedings of the 4th ACM SIGACT-
stable behavior, similarity in the performance trend          SIGPLAN Symposium on Principles of Programming
(i.e., iRank’s performance improvement over LLM               Languages, POPL ’77, page 238–252, New York,
and expected ranks, also over raw embeddings)                 NY, USA. Association for Computing Machinery.
give us confidence about the impact of iRank.
                                                            Leonardo De Moura and Nikolaj Bjørner. 2008. Z3:
                                                              An efficient smt solver. In Tools and Algorithms for
                                                              the Construction and Analysis of Systems: 14th In-
References                                                    ternational Conference, TACAS 2008, Held as Part
                                                              of the Joint European Conferences on Theory and
Rajeev Alur, Rastislav Bodik, Garvit Juniwal, Milo MK         Practice of Software, ETAPS 2008, Budapest, Hun-
  Martin, Mukund Raghothaman, Sanjit A Seshia,                gary, March 29-April 6, 2008. Proceedings 14, pages
  Rishabh Singh, Armando Solar-Lezama, Emina Tor-             337–340. Springer.
  lak, and Abhishek Udupa. 2013. Syntax-guided syn-
  thesis. IEEE.                                             Isil Dillig, Thomas Dillig, Boyang Li, and Ken McMil-
                                                               lan. 2013. Inductive invariant generation via abduc-
   3
     https://platform.openai.com/docs/guides/gpt/              tive inference. Acm Sigplan Notices, 48(10):443–
why-are-model-outputs-inconsistent                             456.


                                                        6
Grigory Fedyukovich and Rastislav Bodík. 2018. Accel-        Shuvendu K. Lahiri, Shaz Qadeer, Juan P. Galeotti,
  erating syntax-guided invariant synthesis. In Tools          Jan W. Voung, and Thomas Wies. 2009. Intra-module
  and Algorithms for the Construction and Analysis             inference. In Computer Aided Verification, 21st Inter-
  of Systems, pages 251–269, Cham. Springer Interna-           national Conference, CAV 2009, Grenoble, France,
  tional Publishing.                                           June 26 - July 2, 2009. Proceedings, volume 5643 of
                                                               Lecture Notes in Computer Science, pages 493–508.
Cormac Flanagan and K. Rustan M. Leino. 2001. Hou-             Springer.
  dini, an annotation assistant for esc/java. In FME
  2001: Formal Methods for Increasing Software Pro-          K Rustan M Leino. 2010. Dafny: An automatic pro-
  ductivity, International Symposium of Formal Meth-           gram verifier for functional correctness. In Logic
  ods Europe, Berlin, Germany, March 12-16, 2001,              for Programming, Artificial Intelligence, and Reason-
  Proceedings, volume 2021 of Lecture Notes in Com-            ing: 16th International Conference, LPAR-16, Dakar,
  puter Science, pages 500–517. Springer.                      Senegal, April 25–May 1, 2010, Revised Selected
                                                               Papers 16, pages 348–370. Springer.
Cormac Flanagan and Shaz Qadeer. 2002. Predicate
  abstraction for software verification. SIGPLAN Not.,       Shang-Wei Lin, Jun Sun, Hao Xiao, Yang Liu, David
  37(1):191–202.                                               Sanán, and Henri Hansen. 2017. Fib: Squeez-
                                                               ing loop invariants by interpolation between for-
Pranav Garg, Daniel Neider, P. Madhusudan, and Dan             ward/backward predicate transformers. In 2017 32nd
  Roth. 2016. Learning invariants using decision trees         IEEE/ACM International Conference on Automated
  and implication counterexamples. In Proceedings              Software Engineering (ASE), pages 793–803. IEEE.
  of the 43rd Annual ACM SIGPLAN-SIGACT Sym-
                                                             Kenneth L. McMillan. 2003. Interpolation and sat-
  posium on Principles of Programming Languages,
                                                               based model checking. In Computer Aided Verifi-
  POPL 2016, St. Petersburg, FL, USA, January 20 -
                                                               cation, 15th International Conference, CAV 2003,
  22, 2016, pages 499–512. ACM.
                                                               Boulder, CO, USA, July 8-12, 2003, Proceedings,
Susanne Graf and Hassen Saïdi. 1997. Construction of           volume 2725 of Lecture Notes in Computer Science,
  abstract state graphs with PVS. In Computer Aided            pages 1–13. Springer.
  Verification, 9th International Conference, CAV ’97,       OpenAI. 2023. Gpt-4 technical report.
  Haifa, Israel, June 22-25, 1997, Proceedings, volume
  1254 of Lecture Notes in Computer Science, pages           Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida,
  72–83. Springer.                                             Carroll Wainwright, Pamela Mishkin, Chong Zhang,
                                                               Sandhini Agarwal, Katarina Slama, Alex Ray, et al.
Sumit Gulwani, Saurabh Srivastava, and Ramarathnam             2022. Training language models to follow instruc-
  Venkatesan. 2009. Constraint-based invariant in-             tions with human feedback. Advances in Neural
  ference over predicate abstraction. In Verification,         Information Processing Systems, 35:27730–27744.
  Model Checking, and Abstract Interpretation, pages
  120–135, Berlin, Heidelberg. Springer Berlin Heidel-       Saswat Padhi, Rahul Sharma, and Todd Millstein.
  berg.                                                        2017. Loopinvgen: A loop invariant generator
                                                               based on precondition inference. arXiv preprint
Thomas A. Henzinger, Ranjit Jhala, Rupak Majumdar,             arXiv:1707.02029.
  and Kenneth L. McMillan. 2004. Abstractions from
  proofs. In Proceedings of the 31st ACM SIGPLAN-            Saswat Padhi, Rahul Sharma, and Todd D. Millstein.
  SIGACT Symposium on Principles of Programming                2016. Data-driven precondition inference with
  Languages, POPL 2004, Venice, Italy, January 14-16,          learned features. In Proceedings of the 37th ACM
  2004, pages 232–244. ACM.                                    SIGPLAN Conference on Programming Language
                                                               Design and Implementation, PLDI 2016, Santa Bar-
Charles Antony Richard Hoare. 1969. An axiomatic               bara, CA, USA, June 13-17, 2016, pages 42–56.
  basis for computer programming. Communications
                                                             Kexin Pei, David Bieber, Kensen Shi, Charles Sutton,
  of the ACM, 12(10):576–580.
                                                               and Pengcheng Yin. 2023. Can large language mod-
Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick           els reason about program invariants?
  Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and           Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya
  Wen-tau Yih. 2020. Dense passage retrieval for               Sutskever, et al. 2018. Improving language under-
  open-domain question answering. arXiv preprint               standing by generative pre-training.
  arXiv:2004.04906.
                                                             Gabriel Ryan, Justin Wong, Jianan Yao, Ronghui Gu,
Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yu-            and Suman Jana. 2020. Cln2inv: Learning loop in-
  taka Matsuo, and Yusuke Iwasawa. 2022. Large lan-            variants with continuous logic networks. In Interna-
  guage models are zero-shot reasoners. arXiv preprint         tional Conference on Learning Representations.
  arXiv:2205.11916.
                                                             Rahul Sharma and Alex Aiken. 2016. From invariant
Shuvendu K. Lahiri and Randal E. Bryant. 2007. Predi-          checking to invariant inference using randomized
  cate abstraction with indexed predicates. ACM Trans.         search. Formal Methods in System Design, 48:235–
  Comput. Logic, 9(1):4–es.                                    256.


                                                         7
                                   i+ ranks                 V@K (%)                            Time(s) (Mean/Median)
              Experiment
                                 Mean   Median       K=1      K=5   k=10         Embed        Ranking    Verification              Total
               LLM-ranks         189.78    62.00      5.2     11.6   18.4           0/0            0/0      7.33 / 2.23       7.33 / 2.23
             Expected ranks       95.35    31.02      8.0     19.2   25.2           0/0            0/0      3.67 / 1.12       3.67 / 1.12
                   TF-IDF        103.45    24.00     17.6     32.0   38.8           0/0      0.05 / 0.02    3.83 / 0.94       3.88 / 1.00
                       Ada       115.89    31.50     11.2     21.6   30.0     1.29 / 0.42    0.05 / 0.01    4.43 / 1.23       5.78 / 1.82
            Emb.
                       Davinci   120.02    32.00     10.4     20.8   33.6     9.17 / 3.02    0.45 / 0.15    4.79 / 1.20      14.41 / 4.48
                       Ada        38.78     5.00     28.0     51.2   60.8     1.29 / 0.42    0.06 / 0.02    1.64 / 0.19       2.98 / 0.97
            iRank
                       Davinci    34.48     4.00     29.2     52.8   62.8     9.17 / 3.02    0.48 / 0.15    1.28 / 0.16      10.93 / 3.68
                                            (a) Invariants generated by gpt-3.5-turbo .

                                    i+ ranks                V@K (%)                            Time(s) (Mean/Median)
              Experiment
                                 Mean    Median      K=1      K=5   k=10         Embed         Ranking    Verification             Total
               LLM-ranks         39.20     9.00      17.6     40.4   51.6           0/0             0/0      1.61 / 0.24      1.61 / 0.24
             Expected ranks      20.23     4.96      31.9     52.1   65.4           0/0             0/0      0.83 / 0.19      0.83 / 0.19
                   TF-IDF        24.16     3.00     32.00     45.6   53.6           0/0      0.01 / 0.006    0.80 / 0.11      0.81 / 0.12
                       Ada       20.69     5.50      26.6     51.1   64.9     0.23 / 0.06    0.01 / 0.004    0.67 / 0.19      0.94 / 0.26
            Emb.
                       Davinci   23.56     5.00      27.7     52.1   63.3     1.93 / 0.48     0.12 / 0.03    0.75 / 0.16      2.80 / 0.77
                       Ada       13.18     2.00      44.7     74.4   81.4     0.25 / 0.06    0.02 / 0.004    0.44 / 0.06      0.71 / 0.16
            iRank
                       Davinci   11.96     2.00      44.7     71.8   81.9     1.93 / 0.48     0.13 / 0.03    0.74 / 0.06      2.80 / 0.72
                                                   (b) Invariants generated by gpt-4 .
      Table 2: Comparison between different ranking strategies for re-ranking the invariants generated by different LLMs.



Xujie Si, Hanjun Dai, Mukund Raghothaman, Mayur                                                               i+ ranks                   V@K (%)
                                                                                    Experiment
                                                                                                            Mean Median           K=1     K=5 k=10
  Naik, and Le Song. 2018. Learning loop invariants
                                                                                             Original       95.35         31.02    8.0      19.2   25.2
  for program verification. Advances in Neural Infor-                       Expected ranks
                                                                                             Deduplicated   65.24         24.07    8.4      22.8   31.2
  mation Processing Systems, 31.
                                                                                             Original       38.78          5.00   28.0      51.2   60.8
                                                                            iRank-ada
                                                                                             Deduplicated   18.79          4.00   28.4      56.0   65.6
Nikhil Swamy, Juan Chen, Cédric Fournet, Pierre-
                                                                                   (a) Invariants generated by gpt-3.5-turbo .
  Yves Strub, Karthikeyan Bhargavan, and Jean Yang.
  2011. Secure distributed programming with value-                                                            i+ ranks                   V@K (%)
                                                                                    Experiment
  dependent types. In Proceedings of the 16th ACM                                                           Mean Median           K=1     K=5 k=10
  SIGPLAN International Conference on Functional                            Expected ranks
                                                                                             Original       20.23          4.96   31.9      52.1   65.4
  Programming, ICFP ’11, page 266–278, New York,                                             Deduplicated   13.99          4.89   31.4      53.7   72.8
  NY, USA. Association for Computing Machinery.                             iRank-ada
                                                                                             Original       13.18          2.00   44.7      74.4   81.4
                                                                                             Deduplicated    8.73          2.00   46.8      77.1   86.7
Jianan Yao, Gabriel Ryan, Justin Wong, Suman Jana,                                   (b) Invariants generated by gpt-4-turbo .
   and Ronghui Gu. 2020. Learning nonlinear loop in-
   variants with gated continuous logic networks. In                     Table 3: Ranking result of correct invariant by de-duplicating
                                                                         semantic equivalent candidates
   Proceedings of the 41st ACM SIGPLAN Conference
   on Programming Language Design and Implementa-
   tion, pages 106–120.
                                                                         davinci-similarity, to acquire initial embed-
A     Further Details of iRank                                           dings for both the problems and candidate solutions.
                                                                         These initial embeddings undergo transformation
In this section, we present a comprehensive                              via a three-layered fully connected feedforward
overview of the operational workflow of iRank,                           network to yield transformed embeddings. The
as visualized in Figure 1.                                               training objective is twofold: minimize the dis-
                                                                         tance between the transformed embedding of the
A.1     Training iRank                                                   problem and the corresponding correct solutions,
As elucidated in Section 4, the training of iRank                        while maximizing the distance from incorrect ones.
necessitates a dataset containing invariant synthesis                    Once this model is trained, it is employed to rank
problems, akin to those illustrated in Figure 4. Each                    the candidate invariants generated by the LLM or
problem in the training dataset requires at least one                    any other generator.
correct invariant and a set of incorrect invariants,
all expressed in the SyGus format (refer to Figure 5                     A.2       Ranking with iRank
for an example). We employ the specified embed-                          Upon successful training of the transformation
ding model, namely text-embedding-ada-002 or                             network within iRank, it is used for ranking pur-

                                                                     8
                               Problem Statistics                                  Number of Layers                 3

      Total Problems                         541                                     Hidden Size       1536 (text-embedding-ada-002)
                                                                                                        12288 (davinci-similarity)
                            Problem Types Statistics                                  Optimizer                   Adam
      Linear Integer (LIA)                   496 (91.68%)                          # Training Epochs                20
      Non-Linear Integer (NIA)               27 (4.99%)
      Array Linear Integer (ALIA)            18 (3.33%)                             Weight Decay                   0.001

                          Problem Semantics Statistics                            Max Gradient Norm                 1.0

      Number of functions                    Min = 3, Max = 9                       Learning Rate                5 ∗ 105

      Number of Variables                    Min = 2, Max = 90                    LR Scheduler Type               Linear

                                             Integer = 80.31%                       Warmup Steps                   500
                                             Boolean = 19.31%                    Table 5: Hyperparameter for Model and Training
      Variable types
                                             Array[Integer] = 0.36%
                                             Array[Boolean] = 0.03%

                  Operator Statistics (of the correct invariants)
                                             43% (of all operators)
      Conjuctions                                                           used in this study.
                                             1.12 (avg. per example)
                                             20% (of all operators)
      Disjunctions
                                             0.53 (avg. per example)

      Negations
                                             37% (of all operators)         B    Detailed Results
                                             0.96 (avg. per example)
                                             43% (of all operators)
      Addition/Subraction
                                             0.5 (avg. per example)         In addition to comparing the number of Z3 calls,
                                             3.1% (of all operators)        we compared the wall clock time. Table 2 shows
      Multiplication/Division
                                             0.18 (avg. per example)
                                                                            a comparison of time (as an extension of Table 1).
                                             88.5% (of all operators)
      Logical Comparison
                                             5.25 (avg. per example)        We conducted all the experiments in 24 cores
                                Length Statistics
                                                                            AMD Epyc 7V13 Linux server running on Linux
                                             Min = 92 (N), 88 (T)           Ubuntu 20.04 LTS with 220 GB RAM, and a sin-
      Problem Length                         Max = 2732 (N), 3146 (T)       gle NVIDIA A100-PCIE-80GB GPU. For LLM-
                                             Mean = 740 (N), 922 (T)
                                             Min = 18 (N), 15 (T)
                                                                            Ranks, Expected ranks there is no embedding and
      Invariant Length (gpt-3.5-turbo)       Max = 605 (N), 506 (T)         ranking, thus the verification time is the bottleneck.
                                             Mean = 110 (N), 125 (T)
                                             Min = 18 (N), 15 (T)
                                                                            For TF-IDF, while there is no embedding time, the
      Invariant Length (gpt-4)               Max = 513 (N), 488 (T)         is a little bit of ranking time.
                                             Mean = 90 (N), 102 (T)
                         N = Tokenized with NLTK                               The Ada embedding time in iRank was very
                        T = Tokenized with TikToken
                                                                            small compared to the Davinci embedding, thus,
         Table 4: Stattistics of the experimental data                      in the case of iRank-ada, embedding and ranking
                                                                            time was offset by the time iRank reduced in the
                                                                            verification effort. In contrast, the Davinci embed-
poses. To rank the candidate invariants, iRank                              ding in iRank is more expensive than the reduc-
initially extracts the initial embedding of the                             tion in the verification time, resulting in a worse
problem and a list of solutions, using the same                             wall clock time performance than the LLM ranks.
embedding model (text-embedding-ada-002 or                                  We conjecture that the text-embedding-ada-002
davinci-similarity) as employed during train-                               (embedding dim = 1536) is a smaller model com-
ing. The trained transformation network is then                             pared to davinci-similarity (embedding dim =
used to transform these embeddings. These trans-                            12188), thus requiring significantly longer time to
formed embeddings serve as vectors for the re-                              embed an input sequence (problem description or
ranking process, where iRank calculates the cosine                          invariant).
similarity between the transformed embedding of                                It is important to note here that, this experiment
the problem and each of the candidate solutions.                            is only meant for an illustration of potential threats
The candidate solutions are then sorted and re-                             to iRank, and is dependent on a lot of variables,
turned based on their similarity with the problem.                          including, but not limited to OpenAI subscription
                                                                            maximum rate limit, network latency for initial
A.3    Data Details and Training                                            embeddings, etc.
       Hyperparameters                                                         In addition, we analyzed the generated invariant
Table 4 shows the statistics of the data we used to                         candidates from LLMs, and removed any semantic
experimentally evaluate iRank. Table 5 shows the                            duplicates. Given two invariant candidates ia and
hyperparameters for the models and training we                              ib parameterized by set of variables {v1 , . . . vn },

                                                                        9
we define semantic equivalence as,                                            Synthesize a necessary and sufficient invariant .

                                                                              Start the invariant with
  ∀v1 , . . . , vn : ia (v1 , . . . , vn ) ⇔ ib (v1 , . . . , vn )            " ( define - fun inv_fun (( i Int ) ( n Int ) ( a Int )
                                                                              ( b Int ) ) Bool ( " and end with " ) " .

For comparing equivalence of two candidate invari-                            Surround only the invariant with < code > and
                                                                              </ code >. You don 't need to explain the invariant ,
ants, we make one call to the z3. Such a seman-                               just synthesize it .
tic deduplication requires comparison of a newly
generated candidate invariant with all previous can-                        The gpt-3.5-turbo model generated invariant
didates, necessitating Θ(n2 ) z3 calls, just to dedu-                     shown in Figure 5 after 144 unsuccessful attempts.
plicate. Table 3 shows the results on deduplicated
candidates in comparison with the original list of                         (define-fun inv_fun ((i Int) (n Int) (a Int) (b Int))
invariants. As expected, after deduplicating, the                          Bool
expected ranks improves. Interestingly, even in                                 (or
                                                                                    (and (<= i n) (= (+ a b) (* 3 i)))
the list of candidates where all candidates are se-                                 (and (> i n) (= (+ a b) (* 3 n)))
mantically unique, iRank improves the rank of the                               )
                                                                           )
correct invariant, resulting in higher V @K.
                                                                           Figure 5: Correct invariant generated by gpt-3.5-turbo.
C       Illustrative example
As an illustration of our proposed approach, we                              The gpt-4 model generated the invariant shown
present an example from FiB (Lin et al., 2017)                            in Figure 6 after 2 unsuccessful attempts.
benchmark 4 . The problem is represented in SyGus
format as shown in Figure 4.                                               (define-fun inv_fun ((i Int) (n Int) (a Int) (b Int))
                                                                           Bool
                                                                                (and (<= i n) (= (+ a b) (* i 3)))
 (set-logic LIA)
                                                                           )
 (synth-inv inv_fun ((i Int) (n Int) (a Int) (b Int)))

 (define-fun pre_fun ((i Int) (n Int) (a Int) (b Int)) Bool
     (and
         (= i 0) (= a 0) (= b 0) (>= n 0)                                        Figure 6: Correct invariant generated by gpt-4.
     )
 )
 (define-fun trans_fun ((i Int) (n Int) (a Int) (b Int)
         (i! Int) (n! Int) (a! Int) (b! Int)) Bool
                                                                             iRank trained based on text-embedding-ada-
     (or                                                                  002 repositioned the gpt-3.5-turbo at 8th posi-
         (and
             (< i n) (= i! (+ i 1)) (= a! (+ a 1))
                                                                          tion in the list and the gpt-4 generated correct
             (= b! (+ b 2)) (= n! n)                                      invariant in position 2. Note that we show this
         )
         (and                                                             example only for illustration purposes.
             (< i n) (= i! (+ i 1)) (= a! (+ a 2))
             (= b! (+ b 1)) (= n! n)
         )                                                                D     Experiment on Expected re-ranking
         (and
             (>= i n) (= i! i) (= a! a) (= b! b) (= n! n)
         )                                                                The list of invariants generated by LLM as a ranked
     )                                                                    list could be unstable and susceptible to variations
 )
 (define-fun post_fun ((i Int) (n Int) (a Int) (b Int)) Bool              in performance across different experiments. Thus,
     (=> (not (< i n)) (= (+ a b) (+ (+ n n) n))))
                                                                          as described in Section 5.1, we estimate the ex-
 (inv-constraint inv_fun pre_fun trans_fun post_fun)                      pected ranks by randomly permutating the list. Ide-
 (check-synth)                                                            ally, to get a perfect estimation, we should consider
                                                                          all possible permutations of the list, which can be
        Figure 4: Invariant synthesis problem in FiB-8.sl                 very expensive (exponential order on the number
                                                                          of elements in the list). Figure 7 shows ablation
    We create the following prompt to call LLMs.                          of mean rank w.r.t. the number of random permuta-
    Here is a loop invariant synthesis problem                            tions. As we can see, with a gradual increase in the
    in SyGus format .
                                                                          number of permutations, the variance in the met-
    <<<< The problem definition from above > > > > >
                                                                          rics gradually reduces, i.e., the metrics converges.
                                                                          Throughout the paper, we set the number of permu-
    https://github.com/spencerxiao/
    4

ase2017-results-and-tools/tree/master/FiB_Tool/                           tations to be 100 for estimating the expected rank
benchmarks                                                                metrics.

                                                                     10
                   102.5

                   100.0

                    97.5
       Mean Rank

                    95.0

                    92.5

                    90.0

                    87.5

                            5 10 15 20 25 30 35 40 45 50 55 60 70 80 90 100
                                      Number of Random Permutations

                                   (a) gpt-3.5-turbo

                   22

                   21
       Mean Rank




                   20

                   19

                   18

                           5 10 15 20 25 30 35 40 45 50 55 60 70 80 90 100
                                    Number of Random Permutations

                                         (b) gpt-4

Figure 7: Result stabilization with an increasing number of
random permutations


E    Visualization of the impact of training
     in iRank
Figure 8 show a t-SNE plot of the raw LLM em-
beddings and the transformed embeddings for a
few example problems. For the first three exam-
ples(Figures 8a, 8b, 8c, respectively), iRank brings
the correct invariant closer to the problem than any
other invariants. For the example presented in Fig-
ure 8d, iRank could not make the correct invariant
as the closest to the problem. While there are cases
where iRank’s transformation fails to bring the cor-
rect invariant in the closest proximity, in most cases,
it can bring correct invariants closer to the trans-
formed problem embedding, as corroborated by the
results in Appendix B




                                                                              11
                    Problem     Correct Invariant   Incorrect Invariant    Problem   Correct Invariant   Incorrect Invariant




                                W/O training                                         With training
                                                            (a) Example - 1

                    Problem     Correct Invariant   Incorrect Invariant    Problem   Correct Invariant   Incorrect Invariant




                                W/O training                                         With training
                                                            (b) Example - 2

                    Problem     Correct Invariant   Incorrect Invariant    Problem   Correct Invariant   Incorrect Invariant




                                W/O training                                         With training
                                                            (c) Example - 3

                    Problem     Correct Invariant   Incorrect Invariant    Problem   Correct Invariant   Incorrect Invariant




                                W/O training                                         With training
                                                            (d) Example - 4

Figure 8: t-SNE plots of embeddings with and without training for a few example problems. The number of incorrect invariants
is downsampled for better visualization clarity.




                                                                      12
