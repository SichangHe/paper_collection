Article

Scalable watermarking for identifying large
language model outputs

https://doi.org/10.1038/s41586-024-08025-4                  Sumanth Dathathri1,3 ✉, Abigail See1,3, Sumedh Ghaisas1,3, Po-Sen Huang1,3, Rob McAdam2,3,
                                                            Johannes Welbl1, Vandana Bachani1, Alex Kaskasoli1, Robert Stanforth1,
Received: 8 April 2024
                                                            Tatiana Matejovicova1, Jamie Hayes1, Nidhi Vyas2, Majd Al Merey2, Jonah Brown-Cohen1,
Accepted: 5 September 2024                                  Rudy Bunel1, Borja Balle1, Taylan Cemgil1, Zahra Ahmed1, Kitty Stacpoole1, Ilia Shumailov1,
                                                            Ciprian Baetu2, Sven Gowal1, Demis Hassabis1 & Pushmeet Kohli1 ✉
Published online: 23 October 2024

Open access
                                                            Large language models (LLMs) have enabled the generation of high-quality synthetic
    Check for updates
                                                            text, often indistinguishable from human-written content, at a scale that can markedly
                                                            affect the nature of the information ecosystem1–3. Watermarking can help identify
                                                            synthetic text and limit accidental or deliberate misuse4, but has not been adopted in
                                                            production systems owing to stringent quality, detectability and computational
                                                            efficiency requirements. Here we describe SynthID-Text, a production-ready text
                                                            watermarking scheme that preserves text quality and enables high detection
                                                            accuracy, with minimal latency overhead. SynthID-Text does not affect LLM training
                                                            and modifies only the sampling procedure; watermark detection is computationally
                                                            efficient, without using the underlying LLM. To enable watermarking at scale, we
                                                            develop an algorithm integrating watermarking with speculative sampling, an
                                                            efficiency technique frequently used in production systems5. Evaluations across
                                                            multiple LLMs empirically show that SynthID-Text provides improved detectability
                                                            over comparable methods, and standard benchmarks and human side-by-side ratings
                                                            indicate no change in LLM capabilities. To demonstrate the feasibility of watermarking
                                                            in large-scale-production systems, we conducted a live experiment that assessed
                                                            feedback from nearly 20 million Gemini6 responses, again confirming the preservation
                                                            of text quality. We hope that the availability of SynthID-Text7 will facilitate further
                                                            development of watermarking and responsible use of LLM systems.


Large language models (LLMs) are widely adopted tools for synthetic                        and may have higher false-positive rates for certain groups, such as
text generation, finding applications in language-based assistants,                        non-native speakers17. Furthermore, such classifiers fundamentally rely
code generation, writing support and various other domains. As LLMs                        on underlying differences between machine and human text, which may
advance in quality, coherence, coverage and expertise, it can become                       diminish as LLMs improve. This necessitates continuous maintenance
difficult to distinguish synthetically generated text from human-written                   of the classifier, including re-training and re-calibrating.
text1–3. Given the widespread use of LLMs in education, software develop-                    A third approach is text watermarking—a way of marking the generated
ment and web content generation, identification and attribution of LLM                     text so that it can subsequently be identified. Text watermarking can be
text is critical to ensure safe and responsible use of the technology8–11.                 done during the generative process (generative watermarking), by edit-
   Multiple strategies have emerged to address this problem. One is a                      ing already generated text (edit-based watermarking) or by altering the
retrieval-based approach, which involves keeping a growing record of                       LLM’s training data (data-driven watermarking)4. Edit-based watermark-
all generated texts and checking against it for matches12. This requires                   ing frequently relies on applying rule-based transformations such as
scale and coordination, and raises privacy concerns as it requires                         synonym substitution or inserting special Unicode characters18, whereas
accessing and storing all LLM interactions. Another approach is post                       data-driven watermarking involves training the LLM on specific trigger
hoc detection, often using the statistical features of text or training a                  phrases19. With data-driven watermarking, the model outputs are water-
machine-learning-based classifier to distinguish human-written from                        marked only when the model is prompted with specific trigger phrases;
artificial-intelligence-generated text13–15. This approach can potentially                 the primary objective is to identify unauthorized misuse of LLMs rather
provide broader detection without the need for record-keeping or any                       than attributing pieces of text to an LLM more broadly. Furthermore,
intervention at the text generation stage. However, post hoc detection                     both of these approaches can leave noticeable artefacts in the text4.
systems can themselves be computationally expensive to run, and                              When watermarking an LLM deployed within a large-scale-production
their practical usage is limited by their inconsistent performance16. In                   setting, it is important to carefully control any impact from water-
particular, they are known to perform poorly on out-of-domain data                         marking on text quality and, by extension, user experience. It is also

Google DeepMind, London, UK. 2Google, Mountain View, CA, USA. 3These authors contributed equally: Sumanth Dathathri, Abigail See, Sumedh Ghaisas, Po-Sen Huang, Rob McAdam.
1

✉e-mail: sdathath@google.com; pushmeet@google.com



818 | Nature | Vol 634 | 24 October 2024
                            LLM text generation

                                                                                                                Sample
                                 Preceding text x<t            LLM            LLM distribution pLM( • |x<t)               Output token xt

                                                                                Append




                            Generative watermarking: text generation and watermark detection


                                            Watermarking key               Random seed
                                                                                                     Random seed rt
                                                                            generator



                                                                                                        Sampling
                               Preceding text x<t        LLM         LLM distribution pLM( • |x<t)                        Output token xt
                                                                                                        algorithm

                                                                                 Append

                                        Text x1, …, xT                                        Apply threshold     Decision:
                                                                Scoring
                                                                                  Score(x)                        Watermarked/
                                    Watermarking key            function
                                                                                                                  not watermarked

Fig. 1 | Overview of LLM text generation and generative watermarking.                  boxes: random seed generator, sampling algorithm and scoring function.
Top: LLM text generation typically involves generating text from left to right         These can be used to provide a text generation method and a watermark
by repeatedly sampling from the LLM distribution. Bottom: a generative                 detection method. In the SynthID-Text generative watermarking scheme,
watermarking scheme typically consists of the three components, in the blue            we use the Tournament sampling algorithm.



important that we are able to watermark with minimal computational                     SynthID-Text into large-scale production systems with negligible addi-
costs. To meet both of these criteria, this work focuses on generative                 tional computational overhead.
watermarking, which allows us to embed watermarks while carefully
controlling the impact on quality and maintaining low computational
cost. However, we note that no text detection method is foolproof, and                 Watermarking with SynthID-Text
many of the approaches discussed in this section are complementary                     LLMs generate text based on preceding context (for example, a
and can be used in conjunction4.                                                       response to a provided prompt). More precisely, given a sequence of
   Generating text with an LLM is often autoregressive: the LLM assigns                input text x<t = x1, …, xt−1 consisting of t − 1 tokens from a vocabulary
probabilities to the elements (tokens) of the vocabulary and then selects              V, the LLM computes the probability distribution pLM(⋅∣x<t) of the next
the next token by sampling according to these probabilities conditional                token xt given the preceding text x<t. To generate the full response, xt
on text generated so far (Fig. 1, top). Generative watermarking (Fig. 1,               is sampled from pLM(⋅∣x<t), and the process repeats until either a maxi-
bottom) works by carefully modifying the next-token sampling proce-                    mum length is reached or an end-token is generated. The process is
dure to inject subtle, context-specific modifications into the generated               illustrated in Fig. 1 (top).
text distribution. Such modifications introduce a statistical signature                   A generative watermarking scheme typically comprises three com-
into the generated text; during the watermark detection phase, the                     ponents: a random seed generator, a sampling algorithm and a scoring
signature can be measured to determine whether the text was indeed                     function21. As shown in Fig. 1 (bottom), the random seed generator pro-
generated by the watermarked LLM. A key benefit of the approach is                     vides a random seed rt on each generation step t (potentially based on
that the detection process does not require performing computation-                    the preceding text along with the watermarking key), and the sampling
ally expensive operations or even access to the underlying LLM (which                  algorithm uses rt to sample the next token xt from pLM(⋅∣x<t). Importantly,
is often proprietary).                                                                 the sampling algorithm introduces correlations between rt and xt; during
   In this work, we propose a generative watermarking scheme,                          watermark detection, these correlations are measured by the scoring
SynthID-Text, which builds on previous generative watermarking                         function. Given a piece of text and the watermarking key, the scoring
components, but uses a novel sampling algorithm, Tournament                            function provides a score that quantifies the strength of the correlation
sampling. SynthID-Text can be configured to be non-distortionary                       (that is, the watermarking evidence); this can be compared with a thresh-
(preserving text quality) or distortionary (improving watermark                        old to determine whether the text originates from the watermarked LLM.
detectability at the cost of text quality). We show that in both settings,                In this work, we present the sampling algorithm Tournament sam-
SynthID-Text provides improved detection rates, compared with the                      pling, which is described in the following section. For the random seed
best existing approaches in each category. We show empirically that                    generator, in our experiments we use the existing sliding-window
non-distortionary SynthID-Text preserves text quality, including                       method22,23, where the random seed is a hash of the most recent H tokens
through a large-scale user feedback assessment over nearly 20 million                  (xt−H, …, xt−1; we use H = 4) along with the watermarking key (Fig. 2, top);
responses from live Gemini interactions. Consequently, SynthID-Text                    but we note that Tournament sampling can be paired with any random
has been used to watermark Gemini and Gemini Advanced20. This serves                   seed generator. We experiment with several scoring functions, some of
as practical proof that generative text watermarking can be successfully               which are from existing work and others are from this work; we discuss
implemented and scaled to real-world production systems, serving                       them in the following sections. Together, our generative watermarking
millions of users and playing an integral role in the identification and               scheme is called SynthID-Text.
management of artificial-intelligence-generated content.
   Furthermore, we provide an algorithm to combine generative water-                   SynthID-Text’s Tournament sampling approach
marking with speculative sampling5—a frequently used technique to                      The key idea of Tournament sampling is to use a tournament-like
increase LLM text generation speed—allowing for the integration of                     process to choose an output token that scores highly with respect to


                                                                                                                         Nature | Vol 634 | 24 October 2024 | 819
Article
some random watermarking functions. An illustration is given in Fig. 2           LLM probabilities and random watermarking functions

(top). First, we take the random seed rt provided by the random seed                                                             Random seed                 Random seed
                                                                                                                                   generator
generator. This seed is passed to m (in this case, m = 3) watermark-                                                                                        y pLM
                                                                                                                                                   Vocabulary             Random watermarking functions
ing functions g1, g2, g3, …, gm—these are independent pseudorandom                   Watermarking key
                                                                                                                                                    mango        0.50             1         0           1
number functions that assign a score gℓ(xt, rt) (in this case, a 0 or 1) to                                                                         lychee       0.30             0         1           0
                                                                                              … my favourite tropical
                                                                                                                pical fru
                                                                                                                      fruit is
any candidate token xt ∈ V.                                                                                  Recent context                         papaya       0.15             0         0           1
   In the second stage (Fig. 2, bottom), we start by sampling M = 2m                                                                                durian       0.05             1         0           0
candidate tokens from the LLM distribution pLM(⋅∣x<t) (some tokens may                                                                                                            g1        g2          g3

appear multiple times): these are the initial participants of the m-layer
tournament. We randomly divide these candidates into M/2 pairs, and,             Tournament sampling: over-generation with watermark-based iterative selection

in the first tournament layer, in each pair the token with the higher                                                  durian    1   g1: tie




                                                                                   Candidate tokens sampled from pLM
score under g1(⋅, rt) is selected, and the other discarded (any ties are                                               mango     1             durian   0      g2: tie
broken randomly). The remaining M/2 tokens are regrouped randomly
                                                                                                                                               mango    0
into M/4 pairs, and the function g2(⋅, rt) determines the winners for this                                             lychee
                                                                                                                        y        0

second tournament layer. This iterative process continues until one                                                    mango     1   g1: winner                                            g3: winner
                                                                                                                                                                         mango         1
                                                                                                                                                                                                        mango
token emerges as the final winner, which becomes the output token                                                                                                        lychee        0
                                                                                                                       papaya
                                                                                                                       p p       0   g1: tie                                                            Output
xt. A formal description of Tournament sampling is given in Algorithm                                                                                                                                   token
                                                                                                                       llychee
                                                                                                                           h     0
2 in Methods.                                                                                                                                  lychee   1
                                                                                                                                               mango    0      g2: winner
                                                                                                                       mango
                                                                                                                          g      1
Watermark detection                                                                                                    mango     1   g1: tie
By design, Tournament sampling selects a token from the LLM distribu-
tion that is likely to score higher under the random watermarking func-          Fig. 2 | SynthID-Text’s Tournament-based watermarking. Top: to generate a
tions g1(⋅, rt), …, gm(⋅, rt). To detect whether a piece of text x = x1, …, xT   new token x t, we first score each token in the vocabulary using multiple (in this
is watermarked, we measure how highly x scores with respect to these             case, m = 3) random watermarking functions g1, …, g m . These assign random
functions. Specifically, we compute the mean g-values of the text:               values using a random seed, which is generated based on both the recent
                                                                                 context and a watermarking key. Bottom: then, we choose the next token using
                                                                                 a tournament process. First, we sample 2 m = 8 (possibly non-unique) tokens
                                        T   m
                                    1                                            from pLM(⋅∣x<t). These are split into pairs of competing tokens; in each pair, the
                     Score (x) =      ∑ ∑ g (x , r ).
                                   mT t =1 ℓ =1 ℓ t t                            highest scoring one (based on g1) is chosen, breaking ties randomly. The
                                                                                 resulting tokens compete in the next layer, where winners are chosen based on
                                                                                 g 2, until in the last tournament layer the final winner is selected based on g m:
Given the selection of tokens xt based on higher g-values, we expect             this becomes the next generated token x t.
watermarked text generally to score higher under this score than unwa-
termarked text.
   There are two primary factors that affect the detection performance              Finally, we note that there are other scoring functions beyond equa-
of the scoring function. The first is the length of the text x: longer texts     tion (1); in Supplementary Information section A, we describe several
contain more watermarking evidence, and so we have more statistical              others, and find that some can improve detection performance.
certainty when making a decision. The second is the amount of entropy
in the LLM distribution when it generates the watermarked text x. For            Preserving the quality of generative text
example, if the LLM distribution is very low entropy, meaning it almost          As previously mentioned, a watermarking scheme can be non-
always returns the exact same response to the given prompt, then                 distortionary, a property relating to quality preservation; however,
Tournament sampling cannot choose tokens that score more highly                  the phrase and its variants have been used in the literature to mean
under the g functions. In short, like other generative watermarks21,             several distinct definitions24,25,27, causing some confusion. In this
Tournament sampling performs better when there is more entropy in                work, we resolve the confusion by providing clear definitions of
the LLM distribution, and is less effective when there is less entropy.          non-distortion, from weakest to strongest. The weakest version is
In Supplementary Information section H, we provide a theoretical                 single-token non-distortion, which says that, on average over the
analysis describing the watermarking strength of a layer of Tournament           random seed rt, the distribution of the output token xt generated by
sampling as a function of a certain kind of entropy; similar analyses            the watermarking sampling algorithm is equal to the original LLM
have been done for other generative watermarks23–25. The entropy of              distribution pLM(⋅∣x<t) (Fig. 1). Stronger versions of non-distortion
the LLM distribution itself depends on several factors, including the            expand this definition to one or more sequences of text, ensuring that
model—for example, larger or more advanced models tend to be more                on average the probability of the watermarking scheme generating
certain and thus lower entropy21, and reinforcement learning from                a particular text or sequence of texts is the same as for the original
human feedback can reduce entropy (also known as ‘mode collapse’)26.             LLM. Full definitions are provided in Supplementary Information
Other factors that affect LLM distribution entropy include the prompts,          section G.
the temperature and other decoding settings such as top-k and top-p                 In Supplementary Information section G.1, we show that when
sampling settings (see ‘The LLM distribution’ in Methods).                       Tournament sampling is configured with exactly two ‘competitors’
   Increasing the number of tournament layers m provides additional              for each match in the tournament (as in the example in Fig. 2), then
watermarking evidence per token, and decreases the variance of                   Tournament sampling is single-token non-distortionary. Furthermore,
the score in equation (1). This allows SynthID-Text to provide better            in Supplementary Information section G.2, we show that by applying
detectability than other methods (see ‘Evaluation’). However, detect-            repeated context masking27, we can make the scheme non-distortionary
ability does not increase indefinitely with the number of layers. Each           for one or more sequences. Choosing the level of non-distortion
layer of the tournament uses some of the available entropy to embed              involves a trade-off; weaker levels of non-distortion can reduce text
a watermark, and the strength of the watermark corresponding to a                quality and diversity, whereas stronger levels of non-distortion can
layer diminishes deeper into the tournament. For our experiments, we             reduce detectability and increase computational complexity (Sup-
generally use m = 30 layers unless otherwise stated; see Supplementary           plementary Information section G.3). For our experiments, we con-
Information section C.1 for full details.                                        figure SynthID-Text to be single-sequence non-distortionary; this


820 | Nature | Vol 634 | 24 October 2024
preserves text quality and provides good detectability, while having        discussion of how we chose our baselines. To create a like-for-like
some reduction to inter-response diversity. We call this configuration      comparison, we focus on comparing our sampling algorithm, Tour-
‘non-distortionary SynthID-Text’ (and where not otherwise specified,        nament sampling, against the Gumbel and Soft Red List sampling
‘SynthID-Text’ also refers to this).                                        algorithms while keeping the other parts of the watermarking
   Alternatively, for instances where strong watermark detectability        scheme the same (Fig. 1). Accordingly, for all baselines we use the
is critical, SynthID-Text can take a distortionary configuration that       same sliding-window random seed generator, and the same repeated
provides higher detectability, at the cost of some quality loss. In this    context masking methodology as described in ‘Watermarking with
configuration of Tournament sampling, there are more than two com-          SynthID-Text’—this means that (like non-distortionary SynthID-Text)
petitors in each match of the tournament (a formal definition is given in   the Gumbel baseline is single-sequence non-distortionary and
Algorithm 2 in Methods). We show that in this case, Tournament sam-         preserves text quality. Furthermore, we note that the hashing and
pling is distortionary at the token level (Supplementary Information        scoring schemes from refs. 24,25 can be directly adapted with
section G.1); however, it applies a stronger watermark (Supplementary       SynthID-Text, and a detailed comparison of the benefits and draw-
Information section H.3). We call this configuration ‘distortionary         backs of various hashing and scoring procedures (for example,
SynthID-Text’.                                                              the edit-distance based scoring as in ref. 24) is beyond the scope of
   In ‘Evaluation’, we compare non-distortionary and distortionary          this work.
SynthID-Text to the best existing methods in each category and show            In the remainder of this section, we empirically demonstrate that
that SynthID-Text provides better detectability in both categories.         SynthID-Text, like some other generative watermarks, has several key
                                                                            desirable properties (quality and scalability) that enable its deploy-
Ensuring computational scalability                                          ment in large-scale production, while also offering additional desirable
Generative watermarking schemes (Fig. 1, bottom) are typically com-         properties such as improved detectability and diversity of the gener-
putationally inexpensive as the text generation process involves a          ated text. First, we show that (like other non-distortionary watermarks)
modification to only the sampling layer, which is often negligible in       non-distortionary SynthID-Text preserves response quality; our evalu-
the context of the LLM’s forward pass. For Tournament sampling, in          ations include the first large-scale human evaluation in a production-
some cases, it is more efficient to use a vectorized implementation,        ized system. Then, across multiple models, we show that SynthID-Text
which we describe in Supplementary Information section E. We pro-           provides improved detection performance while also preserving a
vide a theoretical complexity analysis of both implementations, and         greater amount of the underlying diversity within the LLM responses.
existing baselines in Supplementary Information section F. Overall, we      We also show that SynthID-Text, similar to other generative watermark-
show empirically in ‘Evaluation’ that, in practice, SynthID-Text induces    ing schemes, has negligible computational impact in the context of a
negligible additional latency.                                              large-production LLM.
   In large-scale productionized systems, the text generation process
is often more complex than the simple loop depicted in Fig. 1 (top). For    SynthID-Text preserves quality including in a large-scale-
example, productionized systems often use speculative sampling5, a          production system
method to accelerate text generation from large models. Speculative         To evaluate the production readiness of non-distortionary SynthID-Text,
sampling works by having a smaller draft model propose the next few         we ran a live experiment with the Gemini production system (previously
tokens; these are then checked against the large target model, which        known as Bard). A random fraction of queries were routed to a water-
either accepts or rejects the proposed tokens. Combining generative         marked model and an equivalent number to the unwatermarked coun-
watermarking with speculative sampling is an important step to make         terpart. The Gemini user interface allows users to provide feedback on
watermarking practically useful to production systems; however, to          model responses via a thumbs-up (good response) and a thumbs-down
our knowledge, it has not yet been investigated.                            (bad response). We analysed approximately 20 million watermarked
   To make progress in this area, we propose two generative water-          and unwatermarked responses and computed the thumbs-up and
marking with speculative sampling algorithms, which can combine             thumbs-down rates (both as a fraction of the total number of thumbs-up
a generative watermarking scheme with speculative sampling (Sup-            and thumbs-down feedback received). We found that the thumbs-up
plementary Information section I). First, we propose high-detectability     rate for the two models differed by 0.01% (with the watermarked model
watermarked speculative sampling, which preserves the detectability         being higher); and the thumbs-down rate differed by 0.02% (with the
of the watermark, but may decrease the efficiency (and thus increase        watermarked model being lower). We found both of these differences
the overall latency) of speculative sampling (Supplementary Infor-          to be statistically insignificant, and well within the 95% confidence
mation section I.4). Alternatively, we propose fast watermarked             intervals.
speculative sampling, which (provided the watermark is single-token            From this experiment, we conclude that over a wide variety of real
non-distortionary) preserves the efficiency of speculative sampling,        chatbot interactions, the difference in response quality and utility,
but may decrease the detectability of the watermark (Supplemen-             as judged by humans, is negligible. Subsequently, non-distortionary
tary Information section I.5). For this approach, we also propose a         SynthID-Text has been productionized and is currently watermarking
learned Bayesian scoring function that improves the detectability of        responses in Gemini and Gemini Advanced. To the best of our knowl-
this method (Supplementary Information section I.5.2). Fast water-          edge, this evaluation represents the first systematic watermarking
marked speculative sampling is most helpful when speed is important         investigation of its kind within a large-scale production system.
in production environments.                                                    To provide a reproducible human evaluation, we also run a smaller-
                                                                            scale controlled human preference test, for which we also publish the
                                                                            collected data. In this experiment, we ask raters to compare water-
Evaluation                                                                  marked versus unwatermarked Gemma 7B-IT responses to 3,000 ELI5
We compare SynthID-Text to, at the time of writing, the best-performing     questions, assessing five aspects of response quality in a side-by-side
non-distortionary and distortionary generative text watermarking            comparison. For all five aspects—grammaticality/coherence, relevance,
schemes and show empirically that SynthID-Text provides superior            correctness, helpfulness and overall quality—we find no significant
detectability in both categories. In the non-distortionary category,        difference in rater preference (Extended Data Table 1). This holds
we compare against Gumbel sampling22,24, and in the distortionary           both in a three-way analysis that includes tie ratings and conducts a
category, we compare against the Soft Red List sampling algorithm23;        trinomial test, as well as when restricting the analysis to the non-tie
see Supplementary Information section B.1 for a full description and        responses, using bootstrap resampling over the watermarked versus


                                                                                                       Nature | Vol 634 | 24 October 2024 | 821
Article
   a               0.9                                            b                                                             c
                         SynthID-Text                                                              Watermarked text                          1.0
                         Gumbel sampling                                        0.7                Unwatermarked text
                   0.8
                                                                                0.6                                                          0.8
                   0.7
 TPR@ FPR = 1% →




                                                                                                                           TPR@ FPR = 1% →
                                                            ← Abstention rate
                                                                                0.5
                   0.6                                                                                                                       0.6
                                                                                0.4
                   0.5
                                                                                                                                             0.4
                                                                                0.3
                   0.4
                                                                                                                                                                SynthID-Text
                   0.3                                                          0.2                                                          0.2                Soft Red List (ref. 23)
                                                                                                                                                                log(Perplexity)
                   0.2                                                          0.1                                                                             Unwatermarked LLM
                                                                                                                                             0.0

                         100     200         300      400                             100     200         300        400                           0.4         0.6           0.8
                               Number of tokens                                             Number of tokens                                             ←log(Perplexity)

Fig. 3 | Detection performance of SynthID-Text. a, For non-distortionary                        same as that in a; other temperatures are in Extended Data Fig. 3. c, For
watermarking, we compare watermark detectability as a function of text                          distortionary watermarking, we compare detectability of watermarks that
length (number of tokens), for non-distortionary SynthID-Text and the Gumbel                    allow text quality to be traded off against detectability by adjusting a strength
sampling 22,24 watermark. Watermark detectability is measured using the                         hyperparameter. Texts are of length 200 tokens generated by Gemma 7B-IT
true-positive rate (TPR) when the false-positive rate (FPR) is set to 1%. Responses             with temperature = 0.7; other text lengths and temperatures are provided
are generated from Gemma 7B-IT with temperature = 0.7 using prompts from                        in Extended Data Fig. 2. Compared with the distortionary Soft Red List
the ELI5 dataset; other models and temperatures are provided in Extended                        watermark 23, distortionary SynthID-Text offers a more favourable trade-off,
Data Fig. 1. b, The fraction of watermarked and unwatermarked texts that the                    with substantially higher detection rates for the same effect on text quality
selective prediction mechanism (Supplementary Information section C.8)                          as measured by log(perplexity). The arrows indicates the direction for
abstains on to achieve a true-positive rate of 95% and a false-positive rate of 1%.             performance improvement. The dashed lines correspond to a bootstrap
The mechanism makes predictions only when the scoring function is confident,                    estimate (500 resamples) of the mean of the metric on the y axis and the shaded
and is thus able to maintain a low error rate when making predictions, at the                   regions correspond to the 90% confidence interval on the mean estimate.
cost of abstaining on some of the data. The model set-up and the prompts are



unwatermarked preference ratio (full details in Supplementary Infor-                               In the distortionary category, we compare the trade-off of detect-
mation section C.4).                                                                            ability and text quality for distortionary SynthID-Text and Soft Red List.
   To further validate the quality-neutral property of non-distortionary                        Both methods have a strength parameter that controls this trade-off;
SynthID-Text, we conduct additional automatic evaluations across                                in Fig. 3c, we see that the trade-off is more favourable for distortionary
different models and metrics. We find no significant difference                                 SynthID-Text.
between non-distortionary SynthID-Text and the equivalent unwater­
marked model in terms of perplexity or performance on automated                                 SynthID-Text has minimal computational impact
benchmarks. Full details are provided in Supplementary Information                              As discussed in ‘Watermarking with SynthID-Text’ and Supplemen-
section C.5.                                                                                    tary Information section F, Tournament sampling does in some cases
   To summarize: human quality feedback, both from a large-scale                                have greater computational complexity than Gumbel or Soft Red List
live experiment and a small-scale controlled study, perplexity sta-                             sampling, but these differences are minimal relative to the cost of
tistics and standard model capability benchmarks all indicate that                              generating text from an LLM. For example, the Gemma 7B-IT model
non-distortionary SynthID-Text causes no loss in text quality.                                  served on 4 v5e tensor processing units31 generates text at a rate of
                                                                                                15.527 ms per token; this increases to 15.615 ms per token with 30-layer
SynthID-Text provides better detectability than existing                                        Tournament sampling, a latency increase of only 0.57%. In comparison,
watermarks                                                                                      Gumbel sampling increases latency by 0.26% and Soft Red List by 0.28%.
We evaluate watermark detectability empirically across several pub-                             Furthermore, the computational complexity of all three watermarks
licly available models, including the instruction-tuned (IT) variants of                        remains constant even as the LLM grows. Thus, as large production
Gemma 2B and Gemma 7B28, and the Mistral 7B-IT29 model (see ‘LLMs                               models can grow by orders of magnitude larger than Gemma 7B in terms
and LLM configurations’ in Methods for details). We prompt the models                           of computational complexity, so too does the relative complexity of
with questions from the ELI5 dataset30 (see ‘Data’ in Methods).                                 watermarking shrink by orders of magnitude.
   In the non-distortionary category, Fig. 3a shows that non-distortionary                         As described in ‘Watermarking with SynthID-Text’, we propose an
SynthID-Text provides better detectability than Gumbel sampling,                                algorithm—fast watermarked speculative sampling—to integrate gen-
for the same length text. We find that the SynthID-Text’s improve-                              erative watermarking with speculative sampling and thus enable fast
ment over Gumbel sampling is greater in lower-entropy settings                                  deployment of watermarked LLMs at scale. We evaluate our algorithm
(for example, lower temperatures); when the entropy is higher, the                              with non-distortionary SynthID-Text, using Gemma 7B-IT as the target
detectability of the two methods is more comparable (Extended                                   model and Gemma 2B-IT as the smaller draft model that proposes three
Data Fig. 1). In Extended Data Fig. 4, we also show that although both                          ‘lookahead’ tokens at a time. When paired with a non-distortionary
non-distortionary SynthID-Text and the Gumbel sampling baseline                                 watermark (Supplementary Information section I.3), fast watermarked
reduce inter-response diversity, SynthID-Text provides a better diver-                          speculative sampling is theoretically guaranteed to preserve the accept-
sity/detectability trade-off than Gumbel sampling. In scenarios where                           ance rate (that is, the average number of lookahead tokens accepted
low error rates are desirable, we can use a selective prediction mecha-                         by the target model). We confirm this experimentally, finding that
nism (Supplementary Information section C.8) to abstain on samples                              the acceptance rate (and thus overall latency) is very similar with and
for which the scoring function is uncertain, thus achieving the desired                         without watermarking (Supplementary Information section I.5.3).
error rates on the remaining data (Fig. 3b).                                                    Although we ran our experiment with non-distortionary SynthID-Text,


822 | Nature | Vol 634 | 24 October 2024
we expect the same result would hold for any non-distortionary gen-                                4.    Wu, J. et al. A survey on LLM-generated text detection: necessity, methods, and future
                                                                                                         directions. Preprint at https://arxiv.org/abs/2310.14724 (2024).
erative watermark.                                                                                 5.    Chen, C. et al. Accelerating large language model decoding with speculative sampling.
                                                                                                         Preprint at https://arxiv.org/abs/2302.01318 (2023).
                                                                                                   6.    Team, G. et al. Gemini: a family of highly capable multimodal models. Preprint at https://
Discussion                                                                                               arxiv.org/abs/2312.11805 (2023).
                                                                                                   7.    SynthID-Team Code and data. GitHub https://github.com/google-deepmind/synthid-text
We have introduced SynthID-Text, a method for watermarking LLM text.                                     (2024).
SynthID-Text uses certain elements introduced in previous work22,23,27,                            8.    Shumailov, I. et al. AI models collapse when trained on recursively generated data.
                                                                                                         Nature 631, 755–759 (2024).
but differs in the use of the sampling algorithm, Tournament sam-                                  9.    Alemohammad, S. et al. Self-consuming generative models go MAD. In Proc. Twelfth
pling, which we find provides superior detectability compared with                                       International Conference on Learning Representations (ICLR, 2024).
existing methods. SynthID-Text comes with rigorous and customiz-                                   10.   Taori, R. & Hashimoto, T. Data feedback loops: model-driven amplification of dataset
                                                                                                         biases. In Proc. 40th International Conference on Machine Learning 33883–33920 (JMLR,
able non-distortion properties that can be configured to guarantee                                       2023).
text quality preservation; we confirm this empirically, including via                              11.   Wyllie, S., Shumailov, I. & Papernot, N. Fairness feedback loops: training on synthetic data
real user feedback measured over approximately 20 million Gemini                                         amplifies bias. In Proc. 2024 ACM Conference on Fairness, Accountability, and
                                                                                                         Transparency 2113–2147 (Association for Computing Machinery, 2024).
chatbot interactions. We have also proposed an algorithm to combine                                12.   Krishna, K., Song, Y., Karpinska, M., Wieting, J. F. & Iyyer, M. Paraphrasing evades
generative watermarking with speculative sampling, thus enabling the                                     detectors of AI-generated text, but retrieval is an effective defense. In Proc. Thirty-seventh
efficient deployment of generative watermarks in high-performance,                                       Conference on Neural Information Processing Systems (NeurIPS, 2023).
                                                                                                   13.   Mitchell, E., Lee, Y., Khazatsky, A., Manning, C. D. & Finn, C. DetectGPT: zero-shot
large-scale-production LLMs.                                                                             machine-generated text detection using probability curvature. In Proc. 40th International
                                                                                                         Conference on Machine Learning 24950–24962 (JMLR, 2023).
Limitations                                                                                        14.   Verma, V., Fleisig, E., Tomlin, N. & Klein, D. Ghostbuster: detecting text ghostwritten by
                                                                                                         large language models. In Proc. 2024 Conference of the North American Chapter of the
Generative watermarks such as SynthID-Text provide several advan-                                        Association for Computational Linguistics: Human Language Technologies (Volume 1:
tages compared with other approaches. For example, in Supplementary                                      Long Papers) 1702–1717 (Association for Computational Linguistics, 2024).
Information section C.7, we show that SynthID-Text performs consist-                               15.   Hans, A. et al. Spotting LLMs with binoculars: zero-shot detection of machine-generated
                                                                                                         text. In Proc. 41st International Conference on Machine Learning 17519-17537 (PMLR, 2024).
ently across different languages. In comparison, a post hoc detector                               16.   Elkhatat, A. M., Elsaid, K. & Almeer, S. Evaluating the efficacy of AI content detection tools
performs poorly on languages that its underlying machine-learning                                        in differentiating between human and AI-generated text. Int. J. Educ. Integrity 19, 17
                                                                                                         (2023).
model was not trained on. However, generative watermarks such as
                                                                                                   17.   Liang, W., Yuksekgonul, M., Mao, Y., Wu, E. & Zou, J. GPT detectors are biased against
SynthID-Text do not offer a complete solution to artificial-intelligence                                 non-native English writers. Patterns 4, 100779 (2023).
text detection; rather they are complementary to other approaches.                                 18.   Kamaruddin, N. S., Kamsin, A., Por, L. Y. & Rahman, H. A review of text watermarking:
                                                                                                         theory, methods, and applications. IEEE Access 6, 8011–8028 (2018).
In particular, generative watermarks require coordination between
                                                                                                   19.   Gu, C., Huang, C., Zheng, X., Chang, K.-W. & Hsieh, C.-J. Watermarking pre-trained
actors running the LLM text generation services to apply the water-                                      language models with backdooring. Preprint at https://arxiv.org/abs/2210.07543 (2022).
mark. To detect artificial-intelligence-generated text produced by                                 20.   SynthID-Team Watermarking AI-generated text and video with SynthID. Google DeepMind
                                                                                                         Blog https://deepmind.google/discover/blog/watermarking-ai-generated-text-and-video-
other actors who do not to implement watermarking, other approaches
                                                                                                         with-synthid (2024).
are required, such as post hoc detection. Furthermore, the rise of                                 21.   Piet, J., Sitawarin, C., Fang, V., Mu, N. & Wagner, D. Mark my words: analyzing and evaluating
open-source models presents a challenge, as enforcing watermark-                                         language model watermarks. Preprint at https://arxiv.org/abs/2312.00273 (2023).
                                                                                                   22.   Aaronson, S. & Kirchner, H. Watermarking of large language models. Scott Aaronson
ing on these models deployed in a decentralized manner is difficult.
                                                                                                         https://www.scottaaronson.com/talks/watermark.ppt (2022).
Another limitation of generative watermarks is their vulnerability to                              23.   Kirchenbauer, J. et al. A watermark for large language models. In Proc. 40th International
stealing, spoofing and scrubbing attacks, which is an area of ongo-                                      Conference on Machine Learning 17061–17084 (PMLR, 2023).
                                                                                                   24.   Kuditipudi, R., Thickstun, J., Hashimoto, T. & Liang, P. Robust distortion-free watermarks
ing research32. In particular, generative watermarks are weakened by
                                                                                                         for language models. Trans. Mach. Learn. Res. https://openreview.net/pdf?id=FpaCL1MO2C
edits to the text, such as through LLM paraphrasing33—although this                                      (2024).
usually does change the text significantly. We provide evaluations of                              25.   Christ, M., Gunn, S. & Zamir, O. Undetectable watermarks for language models. In Proc.
                                                                                                         Thirty Seventh Conference on Learning Theory 1125–1139 (PMLR, 2024).
SynthID-Text’s performance under edits and paraphrasing in Supple-                                 26.   Casper, S. et al. Open problems and fundamental limitations of reinforcement
mentary Information section C.6.                                                                         learning from human feedback. Trans. Mach. Learn. Res. https://openreview.net/
                                                                                                         pdf?id=bx24KpJ4Eb (2023).
                                                                                                   27.   Hu, Z. et al. Unbiased watermark for large language models. In Proc. Twelfth International
Conclusion
                                                                                                         Conference on Learning Representations (ICLR, 2024).
Overall, our work provides proof of the real-world viability of gen-                               28.   Team, G. et al. Gemma: open models based on Gemini research and technology. Preprint
erative text watermarks. SynthID-Text has been productionized in the                                     at https://arxiv.org/abs/2403.08295 (2024).
                                                                                                   29.   Jiang, A. Q. et al. Mistral 7B. Preprint at https://arxiv.org/abs/2310.06825 (2023).
user-facing Gemini and Gemini Advanced chatbots, which is, to our                                  30.   Fan, A. et al. ELI5: long form question answering. In Proc. 57th Annual Meeting of the
knowledge, the first deployment of a generative text watermark at scale,                                 Association for Computational Linguistics (eds Korhonen, A. et al.) 3558–3567
serving millions of users. As such, our work sets a practical milestone                                  (Association for Computational Linguistics, 2019).
                                                                                                   31.   Cloud, G. TPU v5e. Google Cloud https://cloud.google.com/tpu/docs/v5e-inference (2024).
for accountable, transparent and responsible LLM deployment.                                       32.   Jovanović, N., Staab, R. & Vechev, M. Watermark stealing in large language models.
                                                                                                         In Proc. 41st International Conference on Machine Learning 22570–22593 (PMLR, 2024).
                                                                                                   33.   Zhang, H. et al. Watermarks in the sand: impossibility of strong watermarking for language
Online content                                                                                           models. In Proc. 41st International Conference on Machine Learning 58851–58880
                                                                                                         (PMLR, 2024).
Any methods, additional references, Nature Portfolio reporting summa-
ries, source data, extended data, supplementary information, acknowl-
                                                                                                   Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims in
edgements, peer review information; details of author contributions                                published maps and institutional affiliations.
and competing interests; and statements of data and code availability
are available at https://doi.org/10.1038/s41586-024-08025-4.                                                          Open Access This article is licensed under a Creative Commons Attribution
                                                                                                                      4.0 International License, which permits use, sharing, adaptation, distribution
                                                                                                                      and reproduction in any medium or format, as long as you give appropriate
1.   Köbis, N. & Mossink, L. D. Artificial intelligence versus Maya Angelou: experimental          credit to the original author(s) and the source, provide a link to the Creative Commons licence,
     evidence that people cannot differentiate AI-generated from human-written poetry.             and indicate if changes were made. The images or other third party material in this article are
     Comput. Hum. Behav. 114, 106553 (2021).                                                       included in the article’s Creative Commons licence, unless indicated otherwise in a credit line
2.   Clark, E. et al. All that’s ‘human’ is not gold: evaluating human evaluation of generated     to the material. If material is not included in the article’s Creative Commons licence and your
     text. In Proc. 59th Annual Meeting of the Association for Computational Linguistics and       intended use is not permitted by statutory regulation or exceeds the permitted use, you will
     the 11th International Joint Conference on Natural Language Processing (Volume 1: Long        need to obtain permission directly from the copyright holder. To view a copy of this licence,
     Papers) (eds. Zong, C. et al.) 7282–7296 (Association for Computational Linguistics, 2021).   visit http://creativecommons.org/licenses/by/4.0/.
3.   Jakesch, M., Hancock, J. T. & Naaman, M. Human heuristics for AI-generated language are
     flawed. Proc. Natl Acad. Sci. USA 120, 2208839120 (2023).                                     © The Author(s) 2024



                                                                                                                                         Nature | Vol 634 | 24 October 2024 | 823
Article
Methods                                                                          g-values. As illustrated in Fig. 2, Tournament sampling requires
                                                                                 g-values to decide which tokens win each match in the tournament.
Detailed SynthID-Text method                                                     Intuitively, we want a function that takes a token x ∈ V, a random seed
In this section, we provide a detailed description of SynthID-Text.              r ∈ R and the layer number ℓ ∈ {1, …, m}, and outputs a g-value gℓ(x, r)
                                                                                 that is a pseudorandom sample from some probability distribution fg
The LLM distribution. Most LLMs are autoregressive, providing the                (the g-value distribution).
probability pLM(xt∣x<t) of the next token xt given the text so far x<t. Text         For example, in Fig. 2, the g-value distribution is Bernoulli(0.5). Given
is typically generated from the LLM using an autoregressive decod­               the random seed r, gℓ(x, r) produces pseudorandom g-values of 0 or 1
ing method, which optionally modifies the LLM distribution pLM(⋅∣x<t)            for each token x in the vocabulary, for each layer ℓ = 1, 2, 3. In this paper,
before sampling from it. Such modifications include top-k and top-p34            we primarily use the Bernoulli(0.5) g-value distribution, although we
sampling, which truncate pLM(⋅∣x<t) to the k most likely tokens or the           also explore Uniform[0, 1]. In general, any g-value distribution can be
tokens covering the top-p probability mass; this can be combined with            chosen, as a hyperparameter of the Tournament sampling method.
applying a temperature parameter τ (ref. 35). Although these modifica-           Definition 3 (g-value distribution). The g-value distribution is a prob-
tions increase or decrease the amount of entropy in pLM(⋅∣x<t),                  ability distribution of any real-valued random variable. We write Fg to
SynthID-Text is compatible with any autoregressive decoding method               denote the cumulative distribution function, and fg to denote the prob-
that has non-zero entropy in the modified distribution. Thus,                    ability density function (if continuous) or probability mass function
SynthID-Text is compatible with top-k sampling for all k ≥ 2, top-p sam-         (if discrete).
pling for all p ∈ (0, 1], and all temperatures τ > 0.                                Next, we need a way to produce a hash h(x , ℓ , r ) ∈ R of a token x ∈ V,
   SynthID-Text is applied after any such modifications have been made,          an integer ℓ ∈ {1, …, m} and a random seed r ∈ R. Let’s assume we have
so for the purposes of this paper we define the LLM distribution pLM(⋅∣x<t)      a pseudorandom function family {h(⋅, ⋅, r )}r∈R similar to the one
to be the distribution after any such modifications.                             described in the ‘Random seed generator’ section, such that the dis-
Definition 1 (LLM distribution). Given an autoregressive LLM, an                 tribution of {h(⋅, ⋅, r )}r~Unif(R) is computationally indistinguishable from
autoregressive decoding method, and x<t = x1, …, xt−1, a sequence of tokens      a function sampled uniformly randomly from the set of all functions
from the vocabulary V, the LLM distribution pLM(⋅∣x<t) is the probability dis-   from V × [m] to {0, 1}n sec.
tribution from which the decoding method samples the next token xt ∈ V.          Definition 4 (g-value). Given a g-value distribution with cumulative
                                                                                 density function. Fg, a random seed r ∈ R, and integer ℓ ∈ 1, …, m, the
Watermarking framework. We present SynthID-Text as comprising a                  layer-ℓ g-value of a token x ∈ V is given by:
random seed generator, a sampling algorithm and a scoring function;
this is similar to the generative watermarking framework of ref. 21. Intui-                                                   h(x , ℓ , r ) 
                                                                                                         gℓ (x , r ) := Fg−1     n          ,
tively, the sampling algorithm samples text from the LLM in a way that                                                        2 sec 
is biased by random seeds provided on each step by the random seed
generator; later we can identify the watermark by detecting this bias            where Fg−1 is the generalized inverse distribution function of Fg, and h is
through the scoring function. We describe the random seed generator              a hash function as described above.
and sampling algorithm in this section and describe several scoring                 Intuitively, Definition 4 says that we take a hash h(x, ℓ, r) of x, ℓ and
functions in Supplementary Information section A. See Supplementary              r, which gives us a uniformly distributed n-bit integer, and divide it by
Information section B for a detailed discussion of related generative            2n to get a number in [0, 1]. For large n, this converges to a uniformly
watermarking approaches.                                                         distributed number in [0, 1]. We then perform inverse transform sam-
                                                                                 pling to turn this number into a sample from the g-value distribution
Random seed generator. To generate a piece of watermarked text                   given by Fg.
x1, …, xT, we require a sequence of random seeds r1, …, rT ∈ R (where            Tournament sampling algorithm. Definition 5 (watermarking
R is the space of all random seeds) to bias the sampling from the                sampling algorithm). In a watermarking scheme, a sampling algorithm
LLM distribution on each step. The random seed generator is the pro-             S : ΔV × R → V is an algorithm that takes as input a probability distribu-
cess by which we generate these random seeds. One approach is to                 tion p ∈ ΔV and a random seed r ∈ R and returns a token S(p, r ) ∈ V .
make the random seed generator a deterministic function fr that                  If S always returns the same token given the same p and r, it is deter­
takes as input the sequence of tokens so far x<t = x1, …, xt−1 and a water-      ministic. Otherwise, S is probabilistic.
marking key k and outputs a random seed rt := fr (x< t , k) ∈ R . Rando­            We propose a new probabilistic sampling algorithm called Tourna-
mizing the key k should randomize the seed; that is, for all                     ment sampling. We present the simplest, single-layer version of Tour-
x< t , Pk~Unif(R) [ fr (x< t , k)] = Unif (R).                                   nament sampling in Algorithm 1. Instead of sampling directly from
   There are several possible choices for fr (ref. 21); for our experiments,     pLM(⋅∣x<t), we sample N tokens from pLM(⋅∣x<t), compute their g-values as
we use the sliding window fr(x<t, k) ≔ h(xt−H, …, xt−1, k), which is a hash      described in the previous section and choose uniformly among those
function h of the last H tokens (for some context length H ≥ 1) and              that have the maximal g-value.
of the key k. This random seed generator is the same as that used by                Algorithm 2 presents the full multilayer version of Tournament sam-
refs. 22,23. In this work, we also assume the watermarking key k and             pling, which has an additional hyperparameter m, the number of layers.
random seed rt exist in the same space of nsec-bit integers, where nsec is       The process can be thought of as a knockout tournament with m stages,
the security parameter.                                                          where each match is an instantiation of the single-layer algorithm;
Definition 2 (random seed space, random seed distribution). Given                this continues until there is one winner. Importantly, each layer ℓ of
a security parameter nsec, the random seed space R = {0, 1}n sec is the          the tournament uses different g-values gℓ(⋅, rt) to decide the winners.
space of all nsec-bit integers. The random seed distribution is the uniform      Figure 2 gives a concrete example for m = 3 layers, N = 2 samples and a
distribution over all such integers Unif (R).                                    Bernoulli(0.5) g-value distribution.
   We also assume that the family of functions {h(⋅, …, ⋅, k)}k∈R is a pseu-     Algorithm 1. Sampling a token with single-layer Tournament sampling
dorandom function family, meaning that (1) h(xt−H, …, xt−1, k) is effi-             Require: LLM distribution pLM(⋅∣x<t), random seed rt ∈ R, number of
ciently computable for any xt−H, …, xt−1 and k, and (2) the distribution         samples N ≥ 2, g function with g-value distribution fg (see Definition 4).
of {h(⋅, …, ⋅, k)}k~Unif(R) is computationally indistinguishable from a             1: Draw Y = [ y1, y2, …, yN] containing N independent samples from
function sampled uniformly randomly from the set of all functions                      pLM(⋅∣x<t) (may contain repeats).
from VH to {0, 1}n sec.                                                             2: Y * := [ y ∈ Y : g1( y, rt) = maxg1( y ′, rt)] (may contain repeats).
                                                                                                               y ′ ∈Y
  3: Sample xt ~ Unif(Y*)                                                         then be compared with a threshold to classify the text as watermarked
  4: return xt                                                                    or unwatermarked. Here the random seeds rt = fr(x<t, k) are from the
Algorithm 2. Sampling a token with multilayer Tournament sampling.                random seed generator (‘Random seed generator’ section). It is noted
  Require: LLM distribution pLM(⋅∣x<t), random seed rt ∈ R, number of             that a scoring function only requires access to the tokenized text, the
samples N ≥ 2, g function with g-value distribution fg (see Definition 4),        watermarking key k and the random seed generator fr; no access to the
number of layers m ≥ 1.                                                           LLM is required.
  1: Draw Nm independent samples y00 , y10 , …, yN0m−1 ~ pLM(⋅ x< t ) (may          For SynthID-Text, we propose several scoring functions, which are
      contain repeats).                                                           in Supplementary Information section A. All the scores are computed
  2: for 1 ≤ ℓ ≤ m do                                                             from the g-values of the text. The simplest of these is the mean score,
  3: for 0 ≤ j ≤ Nm−ℓ − 1 do                                                      which is simply the mean of the g-values across all timesteps and layers.
  4:    Y := [ yNjℓ −1 , yNjℓ −1
                              +1
                                 , …, yNjℓ −1
                                           + N −1
                                                  ] (may contain repeats).        We also propose a weighted mean score, which re-weights the evidence
  5:    Y * := [ y ∈ Y : gℓ ( y, rt) = maxgℓ ( y ′, rt)] (may contain repeats).   of each tournament layer. We propose frequentist versions of these
                                    y ′ ∈Y                                        scores, which perform a hypothesis test on these means to produce a
  6:   Sample yjℓ ~ Unif (Y *).                                                   P value. Lastly, we propose a parameterized Bayesian scoring function,
  7: end for                                                                      which achieves better performance by learning from data (watermarked
  8: end for                                                                      and unwatermarked texts) to compute the posterior probability that
  9: return xt := y0m                                                             a text is watermarked.

Repeated context masking. To generate a full response, we could sim-              Experimental details
ply apply Algorithm 2 on every decoding step, using the sliding-window            LLMs and LLM configurations. In our experiments, we use the IT vari-
random seed generator (‘Random seed generator’ section) to generate               ants of the Gemma 2B and 7B models28. We also use the v0.2 Mistral
the random seed rt for each step. However, it is possible that the same           7B-IT model29. To generate text, we use top-k sampling36. Following
window of context, and thus the same random seed might occur more                 default settings, we use k = 100 for the IT models. We experiment with
than once (particularly if the sliding-window size H is small or the res­         temperatures of 0.5, 0.7 and 1.0, as varying the temperature changes
ponse is long). It has been shown that in this scenario, the watermark            the entropy of the model, which affects watermark detectability.
can introduce a repeated bias that affects the quality of the text, for
example, causing repeating loops24,25. One way to avoid this problem              Data. To prompt our models we use the ELI530 dataset, which consists
is to apply repeated context masking27, which prevents the watermark              of English questions that require explanatory multi-sentence answers.
from being applied on step t if the context window (xt−H, …, xt−1) has been       This simulates a more task-oriented setting. For experiments with
used to watermark previously.                                                     non-distortionary watermarking, our ELI5 test set and the development
   We present the method in Algorithm 3, which we call K-sequence                 set each contain sets of 10,000 disjoint prompts that are used to prompt
repeated context masking. The integer parameter K ≥ 1 controls for                the model to obtain watermarked responses. For experiments with dis-
how long context windows are held in the history. In the simplest case            tortionary watermarking, we use 1,500 prompts from ELI5 for the test
of K = 1, we only hold the context history for the duration of generating         set to prompt the watermarked model. For the unwatermarked samples
a single response. For larger integers K > 1, we check against a history          used as negatives, we use two disjoint sets of human-written responses
of contexts used in the last K responses. In the extreme case, we could           to 10,000 questions from the ELI5 for the development and test sets.
set K = ∞ and retain the context history indefinitely. In Supplementary
Information section G.2, we show that applying K-sequence repeated                Text lengths. For some experiments, we evaluate texts of fixed length—
context masking achieves K-sequence non-distortion, an important                  for example, 200 tokens. To obtain text of length exactly 200 tokens,
property for quality preservation. In Supplementary Information sec-              we select the subset of texts that are longer than 200 tokens and then
tion G.3, we discuss the trade-offs of smaller and larger K. For most of          truncate them to have exactly 200 tokens.
our experiments we use K = 1.
Algorithm 3. Generating watermarked responses with sliding-window                 Detectability metric. To report detectability, we use the true-positive
random seed generation and K-sequence repeated context masking.                   rate (TPR) for a fixed false-positive rate (FPR) of x%, measured empiri-
   Require: LLM pLM(⋅∣⋅), context window size H, pseudorandom hash                cally. We denote this metric as TPR @ FPR = x%. For example to compute
function h, watermarking key k ∈ R, sampling algorithm S : ΔV × R → V,            TPR @ FPR = 1%, we take the scores (under some scoring function) of
integer K ≥ 1, stream of prompts (x1, x2, …).                                     the unwatermarked texts and compute a threshold corresponding
   1: for i ≥ 1 do                                                                to the top-1% highest scores. Then we compute the true-positive rate
   2: Ci := ∅                                                                     by measuring the fraction of watermarked texts that score above this
   3: t ≔ n where n is the length of xi = xi1, …, xin                             threshold. Although some scoring functions allow a precise theoretical
   4: while xit ≠ EOS do                                                          guarantee on the false-positive rate—for example, the frequentist scor-
   5:    t ≔ t + 1                                                                ing functions (Supplementary Information section A.3) which provide
   6:    if (xit − H, …, xit −1) ∈ Ci ∪ Ci −1 ∪ ⋯ ∪ Ci − K +1 then                a P value—in this work we take the empirical approach described above.
   7:    Sample xit ~ pLM(⋅ xi< t)
   8:    else                                                                     Random seed generator settings. For all watermarking experi-
   9:    rt := h(xit − H, …, xit −1, k)                                           ments (including Tournament, Gumbel and Soft Red List sampling
   10:    Sample xit := S(pLM(⋅ xi< t), rt)                                       algorithms), we use the same sliding-window-based random seed gen-
   11:    Ci := Ci ∪ {(xit − H, …, xit −1)}                                       erator described in the ‘Random seed generator’ section, with context
   12:    end if                                                                  window size H = 4. We apply one-sequence repeated context masking
   13: end while                                                                  (‘Repeated context masking’ section).
   14: return Response yi := xin +1:t
   15: end for                                                                    SynthID-Text settings. Unless otherwise mentioned, for all SynthID-
                                                                                  Text experiments, we use m = 30 tournament layers, a Bernoulli(0.5)
Scoring functions. A scoring function takes a piece of text x1, …, xT             g-value distribution fg (Algorithm 2) and the Bayesian scoring function
along with the random seeds r1, …, rT and computes a score, which can             (Supplementary Information section A.4).
Article
                                                                                                       project from conceptualization to the first large-scale system implementation and evaluation.
Data availability                                                                                      S. Ghaisas was the engineering lead of the project. S.D. led the development of the algorithms,
                                                                                                       with contributions from B.B., P.-S.H., R.M., A.S. and J.W. A.S. led the theoretical analysis, with
The data from the human evaluation study described in Supplementary                                    contributions from B.B., J.B.-C., S.D. and R.M. S. Ghaisas led the development of the codebase
Information section C.4 (model responses and human annotations) is                                     with contributions from V.B., R.B., S.D., P.-S.H., R.M., A.S. and R.S. S.D. and S. Ghaisas led the
                                                                                                       productionization of the algorithm with V.B., C.B., P.-S.H. and R.M. contributing critically to
available in ref. 7.                                                                                   code development and evaluations, along with contributions from M.A.M., A.S. and R.S.
                                                                                                       S. Ghaisas and J.W. ran the smaller-scale human evaluations in the paper. C.B. ran the live
                                                                                                       experiment with the Gemini web application. S. Ghaisas and P.-S.H. led the infrastructure for
Code availability                                                                                      the experiments in the paper, with contributions from S.D. S.D., S. Ghaisas and P.-S.H. led the
                                                                                                       experiments measuring the detectability and automated metrics presented in the paper, with
The code to generate and detect text with SynthID-Text watermarking                                    contributions from V.B., R.M. and I.S. S. Ghaisas led the open-sourcing with contributions from
is available in ref. 7.                                                                                S.D., T.M., R.M., A.S. and R.S. P.-S.H., A.K. and T.M. contributed to extended analysis of the system.
                                                                                                       S.D. and A.S. led the writing and revision of the paper, with contributions from B.B., P.-S.H., P.K.,
                                                                                                       R.M., I.S. and J.W. T.C., S. Gowal, J.H. and P.K. provided feedback on the paper and technical
34. Holtzman, A., Buys, J., Du, L., Forbes, M. & Choi, Y. The curious case of neural text
                                                                                                       advice on the project. Z.A., S.D., P.K., K.S. and N.V. coordinated the product delivery of SynthID-
    degeneration. In Proc. Eighth International Conference on Learning Representations
                                                                                                       Text. D.H. provided strategic feedback and advice. The authorship order is randomized among
    (ICLR, 2020).
                                                                                                       A.K., R.S., T.M., J.H., N.V., M.A.M., J.B.-C., R.B., B.B., T.C., Z.A., K.S., I.S., C.B., S. Gowal and D.H.
35. Ackley, D. H., Hinton, G. E. & Sejnowski, T. J. A learning algorithm for Boltzmann machines.
                                                                                                       The authorship order is randomized among A.S., S. Ghaisas, P.-S.H. and R.M.
    Cogn. Sci. 9, 147–169 (1985).
36. Fan, A., Lewis, M. & Dauphin, Y. Hierarchical neural story generation. In Proc. 56th
                                                                                                       Competing interests Work funded and performed by Google DeepMind, with some
    Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
                                                                                                       collaborators at Google. S.D., A.S., B.B., S. Ghasias, P.K., P.-S. H. and J. W. have filed patent
    (eds Gurevych, I. & Miyao, Y.) 889–898 (Association for Computational Linguistics,
                                                                                                       applications EP23162983.3, PCT/EP2024/057423 and US18611417, currently pending
    2018).
                                                                                                       publication, on behalf of DeepMind Technologies Limited, relating to the SynthID-Text
                                                                                                       watermarking method.
Acknowledgements We thank N. Shabat, N. Dal Santo, V. Anklin and B. Hekman for their
collaboration on product integration; A. Senoner, E. Hirst, P. Kirk, M. Trebacz and many others        Additional information
who contributed across Google DeepMind and Google, including our partners at Gemini and                Supplementary information The online version contains supplementary material available at
CoreML, for their support in bringing this technology to production; D. Stutz for technical            https://doi.org/10.1038/s41586-024-08025-4.
inputs on the selective prediction mechanism; R. Mullins for helping with the open-sourcing            Correspondence and requests for materials should be addressed to Sumanth Dathathri or
of the work; and M. Raykova for feedback on the paper.                                                 Pushmeet Kohli.
                                                                                                       Peer review information Nature thanks the anonymous reviewers for their contribution to the
Author contributions P.K. initiated and framed the project and brought together the team.              peer review of this work.
S.D. led the research, contributing critically to all parts of the project. P.-S.H. and J.W. led the   Reprints and permissions information is available at http://www.nature.com/reprints.
Extended Data Fig. 1 | Detectability comparison of non-distortionary          lower entropy settings (lower temperature and larger models). The dashed
SynthID-Text vs Gumbel sampling, for additional model and temperature         lines correspond to a bootstrap estimate (500 resamples) of the mean true
combinations. We show a range of temperatures from 0.5–1.0, which is the      positive rate (TPR) at a false positive rate of 1%, and the shaded regions
range most often used in practice. SynthID-Text generally provides improved   correspond to the 90% confidence interval on the mean estimate.
detection over Gumbel sampling, with the improvements being greatest in
Article




Extended Data Fig. 2 | Detectability and text quality comparison of                  Texts are generated by Gemma 7B-IT. See Supplementary Information section
distortionary SynthID-Text and Soft Red List, for additional temperatures            D for details. Dashed lines correspond to a bootstrap estimate (500 resamples)
and text lengths. Detectability is measured by true positive rate at a fixed false   of the mean TPR@FPR=1%, and the shaded regions correspond to the 90%
positive rate of 1% (TPR@FPR=1%), and text quality is measured by log perplexity.    confidence interval on the mean estimate.
Extended Data Fig. 3 | Abstention rates for non-distortionary SynthID-              remaining texts. The abstention rate is lower for longer texts and higher
Text, for additional temperatures. The fraction of watermarked and                  temperatures. Dashed lines correspond to a bootstrap estimate (500 resamples)
unwatermarked texts abstained on by the selective prediction mechanism              of the mean abstention rate on watermarked and unwatermarked texts, and the
described in Supplementary Information section C.8, for Gemma 7B-IT. The            shaded regions correspond to the 90% confidence interval on the mean
mechanism abstains when the scoring function is uncertain, and is configured        estimate.
here to obtain a true positive rate of 95% and a false positive rate of 1% on the
Article




Extended Data Fig. 4 | Comparing the tradeoff between diversity and             temperatures. We observe that SynthID-Text provides a more favorable
detectability for non-distortionary SynthID-Text and Gumbel sampling.           trade-off across temperatures. Dashed lines correspond to a bootstrap
Diversity is indicated by low Self-BLEU and detectability is measured by true   estimate (500 resamples) of the mean TPR@FPR=1%, and shaded regions
positive rate when false positive rate is fixed at 1% (TPR@FPR=1%). Texts are   correspond to the 90% confidence interval on the mean estimate. See
length 400 tokens, generated from Gemma 7B-IT at three different model          Supplementary Information section C.3 for details.
Extended Data Table 1 | Human preference ratings for unwatermarked responses vs. responses watermarked with
non-distortionary SynthID-Text




Responses are generated by Gemma 7B-IT in response to 3,000 ELI5 questions. We find no statistically significant difference in the preference for watermarked vs. unwatermarked responses.
On the right, relative ratio of prefer watermarked vs. prefer unwatermarked outcomes with bootstrapped symmetric 95% confidence interval (A:B, excluding ties); and the p-value under a
trinomial test for a symmetric distribution between watermarked and unwatermarked responses, in which ties are included and grouped as the third possible outcome. See Supplementary
Information section C.4 for more details.
