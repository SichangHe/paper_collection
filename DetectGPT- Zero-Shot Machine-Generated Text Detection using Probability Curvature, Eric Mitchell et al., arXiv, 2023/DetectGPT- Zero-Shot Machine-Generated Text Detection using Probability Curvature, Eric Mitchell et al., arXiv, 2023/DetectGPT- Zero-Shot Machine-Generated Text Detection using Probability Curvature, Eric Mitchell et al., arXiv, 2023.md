                                                          DetectGPT: Zero-Shot Machine-Generated Text Detection
                                                                       using Probability Curvature


                                                  Eric Mitchell 1 Yoonho Lee 1 Alexander Khazatsky 1 Christopher D. Manning 1 Chelsea Finn 1


                                                                 Abstract                                                                                 Candidate passage       :
                                              The increasing fluency and widespread usage of                        “Joe Biden recently made a move to the White House
arXiv:2301.11305v2 [cs.CL] 23 Jul 2023




                                              large language models (LLMs) highlight the de-                        that included bringing along his pet German Shepherd…”
                                              sirability of corresponding tools aiding detection
                                              of LLM-generated text. In this paper, we identify
                                                                                                                                                            DetectGPT
                                              a property of the structure of an LLM’s proba-                                        (reword
                                                                                                                        (1) Perturb with T5)
                                                                                                                                                                (2) Score             (3) Compare
                                              bility function that is useful for such detection.
                                                                                                                                                ”
                                                                                                                                            long
                                              Specifically, we demonstrate that text sampled                              te “b
                                                                                                                               ring
                                                                                                                                    in ga
                                                                                                                    Dele

                                              from an LLM tends to occupy negative curva-
                                                                                                                x          “pet” → “do
                                                                                                                                      g”                     GPT-3




                                                                                                                                                    ...
                                              ture regions of the model’s log probability func-




                                                                                                                                                                            ...
                                                                                                                  “ma
                                                                                                                        de a
                                                                                                                               move
                                                                                                                                      ”→
                                              tion. Leveraging this observation, we then define                                            “mo
                                                                                                                                              ved”


                                              a new curvature-based criterion for judging if a
                                              passage is generated from a given LLM. This                                                     Yes                                     No
                                              approach, which we call DetectGPT, does not re-
                                              quire training a separate classifier, collecting a                    🤖                 from GPT-3                            🤔     from other source
                                              dataset of real or generated passages, or explic-
                                              itly watermarking generated text. It uses only                  Figure 1. We aim to determine whether a piece of text was gener-
                                              log probabilities computed by the model of in-                  ated by a particular LLM p, such as GPT-3. To classify a candidate
                                              terest and random perturbations of the passage                  passage x, DetectGPT first generates minor perturbations of the
                                              from another generic pre-trained language model                 passage x̃i using a generic pre-trained model such as T5. Then
                                              (e.g., T5). We find DetectGPT is more discrimi-                 DetectGPT compares the log probability under p of the original
                                                                                                              sample x with each perturbed sample x̃i . If the average log ratio
                                              native than existing zero-shot methods for model
                                                                                                              is high, the sample is likely from the source model.
                                              sample detection, notably improving detection of
                                              fake news articles generated by 20B parameter
                                              GPT-NeoX from 0.81 AUROC for the strongest                      While recent work has found that cogent-sounding LLM-
                                              zero-shot baseline to 0.95 AUROC for Detect-                    generated responses are often simply wrong (Lin et al.,
                                              GPT. See ericmitchell.ai/detectgpt                              2022), the articulate nature of such generated text may still
                                              for code, data, and other project information.                  make LLMs attractive for replacing human labor in some
                                                                                                              contexts, notably student essay writing and journalism. At
                                                                                                              least one major news source has released AI-written content
                                         1. Introduction                                                      with limited human review, leading to substantial factual er-
                                                                                                              rors in some articles (Christian, 2023). Such applications of
                                         Large language models (LLMs) have proven able to gen-                LLMs are problematic for a variety of reasons, making fair
                                         erate remarkably fluent responses to a wide variety of user          student assessment difficult, impairing student learning, and
                                         queries. Models such as GPT-3 (Brown et al., 2020), PaLM             proliferating convincing-but-inaccurate news articles. Un-
                                         (Chowdhery et al., 2022), and ChatGPT (OpenAI, 2022)                 fortunately, humans perform only slightly better than chance
                                         can convincingly answer complex questions about science,             when classifying machine-generated vs human-written text
                                         mathematics, historical and current events, and social trends.       (Gehrmann et al., 2019), leading researchers to consider
                                            1
                                              Stanford University. Correspondence to: Eric Mitchell           automated detection methods that may identify signals dif-
                                         <eric.mitchell@cs.stanford.edu>.                                     ficult for humans to recognize. Such methods might give
                                                                                                              teachers and news-readers more confidence in the human
                                         Proceedings of the 40 th International Conference on Machine         origin of the text that they consume.
                                         Learning, Honolulu, Hawaii, USA. PMLR 202, 2023. Copyright
                                         2023 by the author(s).                                               As in prior work (Jawahar et al., 2020), we study the

                                                                                                          1
                           Zero-Shot Machine-Generated Text Detection using Probability Curvature

                                                                                                                               x real ∼ phuman(x)
                                                                                         x fake ∼ pθ (x)
machine-generated text detection problem as a binary clas-




                                                                   log pθ(x)
                                                                                                                                                        x̃real
                                                                                                                                                          4
sification problem. Specifically, we aim to classify whether
                                                                                                                                      x̃real
                                                                                                                                        2
a candidate passage was generated by a particular source
model. While several works have investigated methods for                       x̃ fake
                                                                                  2                  x̃ fake
                                                                                                        3                    x̃real
                                                                                                                               1
training a second deep network to detect machine-generated                                                     x̃ fake                         x̃real
                                                                                   x̃ fake
                                                                                      1                           4                              3
text, such an approach has several shortcomings, including
                                                                                                                         …
a tendency to overfit to the topics it was trained on as well as
the need to train a new model for each new source model that                   Log likelihood       Fake/real sample          Perturbed fake/real sample

is released. We therefore consider the zero-shot version of
machine-generated text detection, where we use the source
model itself, without fine-tuning or adaptation of any kind,           Figure 2. We identify and exploit the tendency of machine-
                                                                       generated passages x ∼ pθ (·) (left) to lie in negative curvature
to detect its own samples. The most common method for
                                                                       regions of log p(x), where nearby samples have lower model
zero-shot machine-generated text detection is evaluating the           log probability on average. In contrast, human-written text
average per-token log probability of the generated text and            x ∼ preal (·) (right) tends not to occupy regions with clear nega-
thresholding (Solaiman et al., 2019; Gehrmann et al., 2019;            tive log probability curvature; nearby samples may have higher or
Ippolito et al., 2020). However, this zeroth-order approach            lower log probability.
to detection ignores the local structure of the learned proba-
bility function around a candidate passage, which we find              probability function’s Hessian to detect a model’s samples.
contains useful information about the source of a passage.
This paper poses a simple hypothesis: minor rewrites of                2. Related Work
model-generated text tend to have lower log probability un-            Increasingly large LLMs (Radford et al., 2019; Brown et al.,
der the model than the original sample, while minor rewrites           2020; Chowdhery et al., 2022; OpenAI, 2022; Zhang et al.,
of human-written text may have higher or lower log prob-               2022) have led to dramatically improved performance on
ability than the original sample. In other words, unlike               many language-related benchmarks and the ability to gen-
human-written text, model-generated text tends to lie in               erate convincing and on-topic text. GROVER (Zellers
areas where the log probability function has negative curva-           et al., 2019) was the first LLM trained specifically for gen-
ture (for example, near local maxima of the log probability).          erating plausible news articles. Human evaluators found
We empirically verify this hypothesis, and find that it holds          GROVER-generated propaganda at least as trustworthy as
true across a diverse body of LLMs, even when the minor                human-written propaganda, motivating the authors to study
rewrites, or perturbations, come from alternative language             GROVER’s ability to detect its own generations by fine-
models. We leverage this observation to build DetectGPT,               tuning a detector on top of its features; they found GROVER
a zero-shot method for automated machine-generated text                better able to detect GROVER-generated text than other pre-
detection. To test if a passage came from a source model pθ ,          trained models. However, Bakhtin et al. (2019); Uchendu
DetectGPT compares the log probability of the candidate                et al. (2020) note that models trained explicitly to detect
passage under pθ with the average log probability of several           machine-generated text tend to overfit to their training dis-
perturbations of the passage under pθ (generated with, e.g.,           tribution of data or source models.
T5; Raffel et al. (2020)). If the perturbed passages tend
to have lower average log probability than the original by             Other works have trained supervised models for machine-
some margin, the candidate passage is likely to have come              generated text detection on top of neural representations
from pθ . See Figure 1 for an overview of the problem and              (Bakhtin et al., 2019; Solaiman et al., 2019; Uchendu et al.,
DetectGPT. See Figure 2 for an illustration of the under-              2020; Ippolito et al., 2020; Fagni et al., 2021), bag-of-words
lying hypothesis and Figure 3 for empirical evaluation of              features (Solaiman et al., 2019; Fagni et al., 2021), and hand-
the hypothesis. Our experiments find that DetectGPT is                 crafted statistical features (Gehrmann et al., 2019). Alterna-
more accurate than existing zero-shot methods for detect-              tively, Solaiman et al. (2019) notes the surprising efficacy
ing machine-generated text, improving over the strongest               of a simple zero-shot method for machine-generated text
zero-shot baseline by over 0.1 AUROC for multiple source               detection, which thresholds a candidate passage based on its
models when detecting machine-generated news articles.                 average log probability under the generative model, serving
                                                                       as a strong baseline for zero-shot machine-generated text
Contributions. Our main contributions are: (a) the identi-             detection in our work. In our work, we similarly use the
fication and empirical validation of the hypothesis that the           generating model to detect its own generations in a zero shot
curvature of a model’s log probability function tends to be            manner, but through a different approach based on estimat-
significantly more negative at model samples than for hu-              ing local curvature of the log probability around the sample
man text, and (b) DetectGPT, a practical algorithm inspired            rather than the raw log probability of the sample itself. See
by this hypothesis that approximates the trace of the log              Jawahar et al. (2020) for a complete survey on machine-

                                                                   2
                          Zero-Shot Machine-Generated Text Detection using Probability Curvature

generated text detection. Other work explores watermarks             Algorithm 1 DetectGPT model-generated text detection
for generated text (Kirchenbauer et al., 2023), which modify          1: Input: passage x, source model pθ , perturbation function q,
a model’s generations to make them easier to detect. Our                 number of perturbations k, decision threshold ϵ
work does not assume text is generated with the goal of easy          2: x̃i ∼ q(·P| x), i ∈ [1..k] // mask spans, sample replacements
                                                                      3: µ̃ ← k1 i log pθ (x̃i ) // approximate expectation in Eq. 1
detection; DetectGPT detects text generated from publicly
                                                                      4: d̂x ← log pP θ (x) − µ̃                          // estimate d (x, pθ , q)
available LLMs using standard LLM sampling strategies.                5: σ̃x2 ← k−1
                                                                                  1
                                                                                          (log p   (x̃   ) − µ̃) 2
                                                                                                                   // variance  for normalization
                                                                                        i        θ     i

The widespread use of LLMs has led to much other con-                 6: if √d̂σ̃xx > ϵ then
temporaneous work on detecting LLM output. Sadasivan                  7:    return true                             // probably model sample
et al. (2023) show that the detection AUROC of the an de-             8: else
tector is upper bounded by a function of the TV distance              9:    return false                       // probably not model sample
between the model and human text. However, we find that
AUROC of DetectGPT is high even for the largest publicly-
                                                                     ability of a sample log pθ (x). The white box setting does
available models (Table 2), suggesting that TV distance may
                                                                     not assume access to the model architecture or parameters.
not correlate strongly with model scale and capability. This
                                                                     Most public APIs for LLMs (such as GPT-3) enable scoring
disconnect may be exacerbated by new training objectives
                                                                     text, though some exceptions exist, notably ChatGPT. While
other than maximum likelihood, e.g., reinforcement learn-
                                                                     most of our experiments consider the white box setting, see
ing with human feedback (Christiano et al., 2017; Ziegler
                                                                     Section 5.2 for experiments in which we score text using
et al., 2020). Both Sadasivan et al. (2023) and Krishna et al.
                                                                     models other than the source model. See Mireshghallah
(2023) show the effectiveness of paraphrasing as a tool for
                                                                     et al. (2023) for a comprehensive evaluation in this setting.
evading detection, suggesting an important area of study
for future work. Liang et al. (2023) show that multi-lingual         The detection criterion we propose, DetectGPT, also makes
detection is difficult, with non-DetectGPT detectors show-           use of generic pre-trained mask-filling models in order to
ing bias against non-native speakers; this result highlights         generate passages that are ‘nearby’ the candidate passage.
the advantage of zero-shot detectors like DetectGPT, which           However, these mask-filling models are used off-the-shelf,
generalize well to any data generated by the original gener-         without any fine-tuning or adaptation to the target domain.
ating model. Mireshghallah et al. (2023) study which proxy
scoring models produce the most useful log probabilities             4. DetectGPT: Zero-shot Machine-Generated
for detection when the generating model is not known (a
                                                                        Text Detection with Random Perturbations
large-scale version of our Figure 6). Surprisingly (but con-
sistent with our findings), they find that smaller models are        DetectGPT is based on the hypothesis that samples from a
in fact better proxy models for performing detection with            source model pθ typically lie in areas of negative curvature
perturbation-based methods like DetectGPT.                           of the log probability function of pθ , unlike human text. In
The problem of machine-generated text detection echoes ear-          other words, if we apply small perturbations to a passage
lier work on detecting deepfakes, artificial images or videos        x ∼ pθ , producing x̃, the quantity log pθ (x) − log pθ (x̃)
generated by deep nets, which has spawned substantial ef-            should be relatively large on average for machine-generated
forts in detection of fake visual content (Dolhansky et al.,         samples compared to human-written text. To leverage this
2020; Zi et al., 2020). While early works in deepfake de-            hypothesis, first consider a perturbation function q(· | x)
tection used relatively general-purpose model architectures          that gives a distribution over x̃, slightly modified versions of
(Güera & Delp, 2018), many deepfake detection methods               x with similar meaning (we will generally consider roughly
rely on the continuous nature of image data to achieve state-        paragraph-length texts x). As an example, q(· | x) might be
of-the-art performance (Zhao et al., 2021; Guarnera et al.,          the result of simply asking a human to rewrite one of the
2020), making direct application to text difficult.                  sentences of x, while preserving the meaning of x. Using
                                                                     the notion of a perturbation function, we can define the
                                                                     perturbation discrepancy d (x, pθ , q):
3. The Zero-Shot Machine-Generated Text
                                                                            d (x, pθ , q) ≜ log pθ (x) − Ex̃∼q(·|x) log pθ (x̃)               (1)
   Detection Problem
                                                                     We state our hypothesis more formally as the Local Pertur-
We study zero-shot machine-generated text detection, the             bation Discrepancy Gap Hypothesis, which describes a gap
problem of detecting whether a piece of text, or candidate           in the perturbation discrepancy for model-generated text
passage x, is a sample from a source model pθ . The problem          and human-generated text.
is zero-shot in the sense that we do not assume access to
human-written or generated samples to perform detection.             Perturbation Discrepancy Gap Hypothesis. If q produces
As in prior work, we study a ‘white box’ setting (Gehrmann           samples on the data manifold, d (x, pθ , q) is positive and
et al., 2019) in which the detector may evaluate the log prob-       large with high probability for samples x ∼ pθ . For human-
                                                                     written text, d (x, pθ , q) tends toward zero for all x.
                                                                 3
                                           Zero-Shot Machine-Generated Text Detection using Probability Curvature

            1.0               gpt2-xl                  EleutherAI/gpt-neo-2.7B            AUROC by around 0.020, so we use this normalized version
                                           Human
            60                             Model                                          of the perturbation discrepancy in our experiments. The
            0.8
            40
                                                                                          resulting method, DetectGPT, is summarized in Alg. 1. Hav-
                                                                                          ing described an application of the perturbation discrepancy
            20
                                                                                          to machine-generated text detection, we next provide an
            0.60
Frequency




                   0.0       0.1     0.2       0.3   0.0      0.1     0.2    0.3          interpretation of this quantity.
                         EleutherAI/gpt-j-6B           EleutherAI/gpt-neox-20b
            0.4                                                                           Interpretation of perturbation discrepancy as curvature
            60
                                                                                          While Figure 3 suggests that the perturbation discrepancy
            40
            0.2                                                                           may be useful, it is not immediately obvious what it mea-
            20                                                                            sures. In this section, we show that the perturbation dis-
            0.00                                                                          crepancy approximates a measure of the local curvature
               0.0 0.0       0.1
                              0.2    0.2   0.4 0.3   0.00.6   0.1   0.80.2   0.31.0
                     Log Probability Change (Perturbation Discrepancy)                    of the log probability function near the candidate passage,
                                                                                          more specifically, that it is proportional to the negative trace
 Figure 3. The average drop in log probability (perturbation discrep-                     of the Hessian of the log probability function.2 To han-
 ancy) after rephrasing a passage is consistently higher for model-                       dle the non-differentiability of discrete data, we consider
 generated passages than for human-written passages. Each plot                            candidate passages in a latent semantic space, where small
 shows the distribution of the perturbation discrepancy d (x, pθ , q)                     displacements correspond to valid edits that retain similar
 for human-written news articles and machine-generated arti-                              meaning to the original. Because our perturbation function
 cles of equal word length. Human-written articles are a sample                           (T5) models natural text, we expect our perturbations to
 of 500 XSum articles; machine-generated text, generated from
                                                                                          roughly capture such meaningful variations of the original
 models GPT-2 (1.5B), GPT-Neo-2.7B (Black et al., 2021), GPT-J
 (6B; Wang & Komatsuzaki (2021)) and GPT-NeoX (20B; Black
                                                                                          passage, rather than arbitrary edits.
 et al. (2022)), is generated by prompting each model with the first                      We first invoke Hutchinson’s trace estimator (Hutchinson,
 30 tokens of each XSum article, sampling from the raw conditional                        1990), giving an unbiased estimate of the trace of matrix A:
 distribution. Discrepancies are estimated with 100 T5-3B samples.
                                                                                                                 tr(A) = Ez z⊤ Az                        (2)
 If we define q(· | x) to be samples from a mask-filling model
                                                                                          provided that the elements of z ∼ qz are IID with E[zi ] = 0
 such as T5 (Raffel et al., 2020), rather than human rewrites,
                                                                                          and Var(zi ) = 1. To use Equation 2 to estimate the trace
 we can empirically test the Perturbation Discrepancy Gap
                                                                                          of the Hessian of f at x, we must therefore compute the
 Hypothesis in an automated, scalable manner. For real data,
                                                                                          expectation of the directional second derivative z⊤ Hf (x)z.
 we use 500 news articles from the XSum dataset (Narayan
                                                                                          We approximate this expression with finite differences:
 et al., 2018); for model samples, we use the output of four
 different LLMs when prompted with the first 30 tokens of                                                      f (x + hz) + f (x − hz) − 2f (x)
 each article in XSum. We use T5-3B to apply perturbations,                                   z⊤ Hf (x)z ≈                                               (3)
                                                                                                                              h2
 masking out randomly-sampled 2-word spans until 15% of
 the words in the article are masked. We approximate the                                  Combining Equations 2 and 3 and simplifying with h = 1,
 expectation in Eq. 1 with 100 samples from T5.1 Figure 3                                 we have an estimate of the negative Hessian trace
 shows the result of this experiment. We find the distribution
 of perturbation discrepancies is significantly different for                               −tr (Hf (x)) ≈ 2f (x) − Ez [f (x + z) + f (x − z)] . (4)
 human-written articles and model samples; model samples
 tend to have a larger perturbation discrepancy. Section 5.3                              If our noise distribution is symmetric, that is, p(z) = p(−z)
 explores a relaxation of the assumption that q only produces                             for all z, then we can simplify Equation 4 to
 samples on the data manifold, finding that a gap, although                                           −tr (Hf (x))
 reduced, still exists in this case.                                                                               ≈ f (x) − Ez f (x + z).               (5)
                                                                                                           2
  Given these results, we can detect if a piece of text was
  generated by a model pθ by simply thresholding the pertur-                              We note that the RHS of Equation 5 corresponds to the
  bation discrepancy. In practice, we find that normalizing the                           perturbation discrepancy (1) where the perturbation func-
  perturbation discrepancy by the standard deviation of the ob-                           tion q(x̃ | x) is replaced by the distribution qz (z) used
  served values used to estimate Ex̃∼q(·|x) log pθ (x̃) provides                          in Hutchinson’s trace estimator (2). Here, x̃ is a high-
  a slightly better signal for detection, typically increasing                            dimensional sequence of tokens while qz is a vector in a
             1                                                                               2
      We later show in Figure 8 that varying the number of samples                             Rather than the Hessian of the log likelihood with respect to
  used to estimate the expectation effectively allows for trading off                     model parameters (the Fisher Information Matrix), here we refer
  between accuracy and speed.                                                             to the Hessian of the log probability with respect to the sample x.

                                                                                      4
                             Zero-Shot Machine-Generated Text Detection using Probability Curvature

                             XSum                                               SQuAD                                        WritingPrompts
Method      GPT-2 OPT-2.7 Neo-2.7 GPT-J NeoX        Avg. GPT-2 OPT-2.7 Neo-2.7 GPT-J NeoX            Avg. GPT-2 OPT-2.7 Neo-2.7 GPT-J NeoX             Avg.
log p(x)    0.86    0.86    0.86    0.82    0.77    0.83    0.91    0.88    0.84     0.78    0.71    0.82    0.97    0.95      0.95    0.94    0.93*   0.95
Rank        0.79    0.76    0.77    0.75    0.73    0.76    0.83    0.82    0.80     0.79    0.74    0.80    0.87    0.83      0.82    0.83    0.81    0.83
LogRank     0.89*   0.88*   0.90*   0.86*   0.81*   0.87*   0.94*   0.92*   0.90*    0.83*   0.76*   0.87*   0.98*   0.96*     0.97*   0.96*   0.95    0.96*
Entropy     0.60    0.50    0.58    0.58    0.61    0.57    0.58    0.53    0.58     0.58    0.59    0.57    0.37    0.42      0.34    0.36    0.39    0.38
DetectGPT   0.99    0.97    0.99    0.97    0.95    0.97    0.99    0.97    0.97     0.90    0.79    0.92    0.99    0.99      0.99    0.97    0.93*   0.97
Diff        0.10    0.09    0.09    0.11    0.14    0.10    0.05    0.05    0.07     0.07    0.03    0.05    0.01    0.03      0.02    0.01    -0.02   0.01

Table 1. AUROC for detecting samples from the given model on the given dataset for DetectGPT and four previously proposed criteria
(500 samples used for evaluation). From 1.5B parameter GPT-2 to 20B parameter GPT-NeoX, DetectGPT consistently provides the most
accurate detections. Bold shows the best AUROC within each column (model-dataset combination); asterisk (*) denotes the second-best
AUROC. Values in the final row show DetectGPT’s AUROC over the strongest baseline method in that column.

compact semantic space. Since the mask-filling model sam-                       (log-)rank are likely machine-generated. We also evalu-
ples sentences similar to x with minimal changes to seman-                      ate an entropy-based approach inspired by the hypothesis
tic meaning, we can think of the mask-filling model as first                    in Gehrmann et al. (2019) that model-generated texts will
sampling a similar semantic embedding (z̃ ∼ qz ) and then                       be more ‘in-distribution’ for the model, leading to more
mapping this to a token sequence (z̃ 7→ x̃). Sampling in                        over-confident (thus lower entropy) predictive distributions.
semantic space ensures that all samples stay near the data                      Empirically, we find predictive entropy to be positively cor-
manifold, which is useful because we would expect the log                       related with passage fake-ness more often that not; there-
probability to always drop if we randomly perturb tokens.                       fore, this baseline uses high average entropy in the model’s
We can therefore interpret our objective as approximating                       predictive distribution as a signal that a passage is machine-
the curvature restricted to the data manifold.                                  generated. While our main focus is on zero-shot detectors
                                                                                as they do not require re-training for new domains or source
5. Experiments                                                                  models, for completeness we perform comparisons to su-
                                                                                pervised detection models in Section 5.1, using OpenAI’s
We conduct experiments to better understand multiple facets                     RoBERTa-based (Liu et al., 2019) GPT-2 detector models,3
of machine-generated text detection; we study the effective-                    which are fine-tuned on millions of samples from various
ness of DetectGPT for zero-shot machine-generated text de-                      GPT-2 model sizes and decoding strategies.
tection compared to prior zero-shot approaches, the impact
                                                                                Datasets & metrics Our experiments use six datasets that
of distribution shift on zero-shot and supervised detectors,
                                                                                cover a variety of everyday domains and LLM use-cases.
and detection accuracy for the largest publicly-available
                                                                                We use news articles from the XSum dataset (Narayan et al.,
models. To further characterize factors that impact detec-
                                                                                2018) to represent fake news detection, Wikipedia para-
tion accuracy, we also study the robustness of zero-shot
                                                                                graphs from SQuAD contexts (Rajpurkar et al., 2016) to
methods to machine-generated text that has been partially
                                                                                represent machine-written academic essays, and prompted
revised, the impact of alternative decoding strategies on
                                                                                stories from the Reddit WritingPrompts dataset (Fan et al.,
detection accuracy, and a black-box variant of the detec-
                                                                                2018) to represent detecting machine-generated creative
tion task. Finally, we analyze more closely DetectGPT’s
                                                                                writing submissions. To evaluate robustness to distribution
behavior as the choice of perturbation function, the number
                                                                                shift, we also use the English and German splits of WMT16
of samples used to estimate d (x, pθ , q), the length of the
                                                                                (Bojar et al., 2016) as well as long-form answers written by
passage, and the data distribution is varied.
                                                                                human experts in the PubMedQA dataset (Jin et al., 2019).
Comparisons. We compare DetectGPT with various exist-                           Each experiment uses between 150 and 500 examples for
ing zero-shot methods for machine-generated text detection                      evaluation, as noted in the text. For each experiment, we
that also leverage the predicted token-wise conditional dis-                    generate the machine-generated text by prompting with the
tributions of the source model for detection. These methods                     first 30 tokens of the real text (or just the question tokens
correspond to statistical tests based on token log probabil-                    for the PubMedQA experiments). We measure performance
ities, token ranks, or predictive entropy (Gehrmann et al.,                     using the area under the receiver operating characteristic
2019; Solaiman et al., 2019; Ippolito et al., 2020). The                        curve (AUROC), which can be interpreted as the probability
first method uses the source model’s average token-wise log                     that a classifier correctly ranks a randomly-selected posi-
probability to determine if a candidate passage is machine-                     tive (machine-generated) example higher than a randomly-
generated or not; passages with high average log probability                    selected negative (human-written) example. All experiments
are likely to be generated by the model. The second and                         use an equal number of positive and negative examples.
third methods use the average observed rank or log-rank of                        3
                                                                                    https://github.com/openai/gpt-2-output-
the tokens in the candidate passage according to the model’s                    dataset/tree/master/detector
conditional distributions. Passages with smaller average

                                                                            5
                                                            Zero-Shot Machine-Generated Text Detection using Probability Curvature

                                   XSum GPT-2 Detection                     WMT16-en mGPT Detection                                              PMQA           XSum        WritingP      Avg.
                  1.0      0.981 0.997                           0.991
                                                                                                                  0.957
                                                         0.915                    0.946
                  0.9                    0.889                            0.888                           0.863                  RoB-base      0.64 / 0.58    0.92 / 0.74   0.92 / 0.81   0.77
                                                                                          0.838
                  0.8                            0.800                                            0.795                          RoB-large     0.71 / 0.64    0.92 / 0.88   0.91 / 0.88   0.82
                  0.8
                  0.7
                                                                                                                                 log p(x)      0.64 / 0.55    0.76 / 0.61   0.88 / 0.67   0.69
Detection AUROC



                  0.6
                  0.5
                                                                                                                                 DetectGPT     0.84 / 0.77    0.84 / 0.84   0.87 / 0.84   0.83
                               e lg      d k        k         T                 e g          d k       k        T
                  0.6
                           -bas oB- lihoo Ran LogRan tectGrsP)              -bas RoB-l elihoo Ran ogRan tectGsP)
                        RoB R Like                 De (Ou                RoB          Lik         L De Our
                                                                                                         (                    Table 2. DetectGPT detects generations from GPT-3 and Jurassic-2
                  0.4
                      PubMedQA PubMedGPT Detection                          WMT16-de mGPT Detection                           Jumbo (175B models from OpenAI and AI21 Labs) with average
                  1.0                                                                                             0.962
                               Supervised                                                                                     AUROC on-par with supervised models trained specifically for
                  0.9          Unsupervised                                                       0.838 0.861
                                                                 0.836                                                        machine-generated text detection. For more ‘typical’ text, such
                  0.8                  0.768             0.773                            0.795
                  0.2           0.713                                                                                         as news articles, supervised methods perform strongly. The GPT-
                  0.7                            0.664
                  0.6      0.604                                                                                              3 AUROC appears first in each column, the Jurassic-2 AUROC
                                                                                  0.537
                  0.5
                  0.0                                                     0.394                                               appears second (i.e., after the slash).
                               e lg 0.2 d k         k         T                  e    g        od 0.8nk nk        T
                     0.0
                           -bas oB- lihoo Ran LogRan tectGrsP)
                                                    0.4
                                                                            -ba B-l
                                                                                s
                                                                              0.6
                                                                                  Ro
                                                                                                                P1.0
                                                                                           liho Ra LogRa etectGrs)
                        RoB R Like                 De (Ou                RoB           Like             D (Ou                 and the average margin of improvement is narrow.4 For 14
                                                         Detection Method                                                     of the 15 combinations of dataset and model, DetectGPT
                                                                                                                              provides the most accurate detection performance, with a
  Figure 4. Supervised machine-generated text detection models
  trained on large datasets of real and generated texts perform as
                                                                                                                              0.06 AUROC improvement on average. Log-rank threshold-
  well as or better than DetectGPT on in-distribution (top row)                                                               ing proves to be a consistently stronger baseline than log
  text. However, zero-shot methods work out-of-the-box for new                                                                probability thresholding, although it requires slightly more
  domains (bottom row) such as PubMed medical texts and German                                                                information (full predicted logits), which are not always
  news data from WMT16. For these domains, supervised detectors                                                               available in public APIs.
  fail due to excessive distribution shift.
                                                                                                                              Comparison with supervised detectors. While our experi-
                                                                                                                              ments generally focus on zero-shot detection, some works
                                                                                                                              have evaluated the detection performance of supervised
  Hyperparameters. The key hyperparameters of DetectGPT
                                                                                                                              methods (typically fine-tuned transformers) for detecting
  are the fraction of words masked for perturbation, the length
                                                                                                                              machine-generated text. In this section, we explore several
  of the masked spans, the model used for mask filling, and the
                                                                                                                              domains to better understand the relative strengths of super-
  sampling hyperparameters for the mask-filling model. Using
                                                                                                                              vised and zero-shot detectors. The results are presented in
  BERT (Devlin et al., 2019) masked language modeling as
                                                                                                                              Figure 4, using 200 samples from each dataset for evalua-
  inspiration, we use 15% as the mask rate. We performed
                                                                                                                              tion. We find that supervised detectors can provide similar
  a small sweep over masked span lengths of {2, 5, 10} on a
                                                                                                                              detection performance to DetectGPT on in-distribution data
  held-out set of XSum data, finding 2 to perform best. We
                                                                                                                              like English news, but perform significantly worse than zero-
  use these settings for all experiments, without re-tuning.
                                                                                                                              shot methods in the case of English scientific writing and
  We use T5-3B for almost all experiments, except for GPT-
                                                                                                                              fail altogether for German writing. This finding echoes past
  NeoX and GPT-3 experiments, where compute resources
                                                                                                                              work showing that language models trained for machine-
  allowed for the larger T5-11B model; we also use mT5-3B
                                                                                                                              generated text detection overfit to their training data (source
  instead of T5-3B for the WMT multilingual experiment. We
                                                                                                                              model, decoding strategy, topic, language, etc.; Uchendu
  do not tune the hyperparameters for the mask filling model,
                                                                                                                              et al. (2020); Ippolito et al. (2020); Jawahar et al. (2020)).
  sampling directly with temperature 1.
                                                                                                                              In contrast, zero-shot methods generalize relatively easily
                                                                                                                              to new languages and domains; DetectGPT’s performance
   5.1. Main Results
                                                                                                                              in particular is mostly unaffected by the change in language
  We first present two groups of experiments to evaluate De-                                                                  from English to German.
  tectGPT along with existing methods for zero-shot and su-                                                                   While our experiments have shown that DetectGPT is ef-
  pervised detection on models from 1.5B to 175B parameters.                                                                  fective on a variety of domains and models, it is natural to
  Zero-shot machine-generated text detection. We present                                                                      wonder if it is effective for the largest publicly-available
  the comparison of different zero-shot detection methods in                                                                  LMs. Therefore, we also evaluate multiple zero-shot and su-
  Table 1. In these experiments, model samples are gener-                                                                     pervised methods on two 175B parameter models, OpenAI’s
  ated by sampling from the raw conditional distribution with                                                                 GPT-3 and AI21 Labs’ Jurassic-2 Jumbo. Because neither
  temperature 1. DetectGPT most improves average detec-                                                                       API provides access to the complete conditional distribution
  tion accuracy for XSum stories (0.1 AUROC improvement)                                                                          4
                                                                                                                                    The overall ease of detecting machine-generated fake writing
  and SQuAD Wikipedia contexts (0.05 AUROC improve-                                                                           corroborates anecdotal reporting that machine-generated creative
  ment). While it also performs accurate detection for Writing-                                                               writing tends to be noticeably generic, and therefore relatively easy
  Prompts, the performance of all methods tends to increase,                                                                  to detect (Roose & Newton, 2022).

                                                                                                                          6
                                              Zero-Shot Machine-Generated Text Detection using Probability Curvature

                    1.0                    Rank            LogRank             Entropy                         XSum             SQuAD                             WritingPrompts
                                           DetectGPT       Likelihood
                                                                                              Method       top-p    top-k   top-p                         top-k top-p    top-k
                    0.9
  Detection AUROC


                                                                                              log p(x)      0.92    0.87     0.89                         0.85    0.98    0.96
                    0.8                                                                       Rank          0.76    0.76     0.81                         0.80    0.84    0.83
                                                                                              LogRank       0.93*   0.90*    0.92*                        0.90*   0.98    0.97
                    0.7                                                                       Entropy       0.53    0.55     0.54                         0.56    0.32    0.35
                                                                                              DetectGPT     0.98    0.98     0.94                         0.93    0.98    0.97
                    0.6
                                                                                             Table 3. AUROC for zero-shot methods averaged across the five
                          0.00    0.04    0.08     0.12     0.16        0.20     0.24
                            Fraction of GPT-J-generated news article re-written              models in Table 1 for both top-k and top-p sampling, with k =
                                                                                             40 and p = 0.96. Both settings enable slightly more accurate
Figure 5. We simulate human edits to machine-generated text by                               detection, and DetectGPT consistently provides the best detection
replacing varying fractions of model samples with T5-3B gener-                               performance. See Appendix Tables 4 and 5 for complete results.
ated text (masking out random five word spans until r% of text is
masked to simulate human edits to machine-generated text). The
four top-performing methods all generally degrade in performance                             detecting machine-generated text, prior work notes that
with heavier revision, but DetectGPT is consistently most accurate.                          the decoding strategy (i.e., temperature sampling, top-k,
Experiment is conducted on the XSum dataset.                                                 nucleus/top-p) can impact the difficulty of detection. We re-
                                                                                             peat the analysis from Section 5.1 using top-k sampling and
                                                                                             nucleus sampling. Top-k sampling truncates the sampling
for each token, we cannot compare to the rank, log rank, and                                 distribution to only the k highest-probability next tokens;
entropy-based prior methods. We sample 150 examples5                                         nucleus sampling samples from only the smallest set of to-
from the PubMedQA, XSum, and WritingPrompts datasets                                         kens whose combined probability exceeds p. The results
and compare the two pre-trained RoBERTa-based detector                                       are summarized in Table 3; Appendix Tables 4 and 5 show
models with DetectGPT and the probability thresholding                                       complete results. We use k = 40, and p = 0.96, in line with
baseline. We show in Table 2 that DetectGPT can provide                                      prior work (Ippolito et al., 2020). We find that both top-k
detection competitive with or better than the stronger of the                                and nucleus sampling make detection easier, on average.
two supervised models, and it again greatly outperforms                                      Averaging across domains, DetectGPT provides the clearest
probability thresholding on average.                                                         signal for zero-shot detection.
                                                                                             Detection when the source model is unknown. While
5.2. Variants of Machine-Generated Text Detection
                                                                                             our experiments have focused on the white-box setting
Detecting paraphrased machine-generated text. In prac-                                       for machine-generated text detection, in this section, we
tice, humans may manually edit or refine machine-generated                                   explore the effect of using
text rather than blindly use a model’s generations for their                                 a different model to score a         Scoring Model
                                                                                                                                 GPT-J GPT-Neo GPT-2
task of interest. We therefore conduct an experiment to                                      candidate passage (and per-
                                                                                                                                  0.92   0.83   0.79
                                                                                                                                                (0.02) 0.85
                                                                                                                                    GPT-2 GPT-Neo GPT-J




simulate the detection problem for model samples that have                                   turbed texts) than the model         (0.02) (0.04)
                                                                                                                              Base Model




been increasingly heavily revised. We simulate human re-                                     that generated the passage.
vision by replacing 5 word spans of the text with samples                                    In other words, we aim               0.64
                                                                                                                                  (0.06)
                                                                                                                                         0.97
                                                                                                                                         (0.01)
                                                                                                                                                0.83
                                                                                                                                                (0.02) 0.81
from T5-3B until r% of the text has been replaced, and                                       to classify between human-
report performance as r varies. Figure 5 shows that De-                                      generated text and text from         0.60
                                                                                                                                  (0.09)
                                                                                                                                         0.85
                                                                                                                                         (0.05)
                                                                                                                                                0.99
                                                                                                                                                (0.00) 0.81
tectGPT maintains detection AUROC above 0.8 even when                                        model A, but without ac-
                                                                                                                                 0.72 0.88 0.87
nearly a quarter of the text in model samples has been re-                                   cess to model A to com-
placed. Unsurprisingly, almost all methods show a gradual                                    pute log probabilities. In-   Figure 6. DetectGPT performs
degradation in performance as the sample is more heavily                                     stead, we use log probabil-   best when scoring samples
revised. The entropy baseline shows surprisingly robust                                      ities computed by a surro-    with the same model that gen-
performance in this setting (althought it is least accurate                                  gate model B. We con-         erated them (diagonal), but
on average), even slightly improving detection performance                                   sider three models, GPT-J,    the column means suggest that
up to 24% replacement. DetectGPT shows the strongest                                         GPT-Neo-2.7, and GPT-2,       some models (GPT-Neo, GPT-
                                                                                             evaluating all possible com-  2) may be better ‘scorers’ than
detection performance for all revision levels.
                                                                                                                           others (GPT-J). White values
                                                                                             binations of source model
Impact of alternative decoding strategies on detection.                                                                    show mean (standard error)
                                                                                             and surrogate model (9 to-    AUROC over XSum, SQuAD,
While Table 1 suggests that DetectGPT is effective for
                                                                                             tal). We average the perfor-  and WritingPrompts; black
   5
     We reduce the number of evaluation samples from 500 in our                              mance across 200 samples      shows row/column mean.
main experiments to reduce the API costs of these experiments.                               from XSum, SQuAD, and

                                                                                         7
                                                  Zero-Shot Machine-Generated Text Detection using Probability Curvature

                  1.0    5 perturbations                   25 perturbations                                       1.0 GPT-2                           GPT-J
Detection AUROC

                  0.9




                                                                                                Detection AUROC
                                                                                                                  0.9
                  0.8
                                                                                Random                            0.8
                  0.7                                                           GPT2-sm
                                                                                GPT2-md                           0.7              XSum
                  0.6                                                           GPT2-lg                                            SQuAD
                                                                                GPT2-xl                                            WritingPrompts
                  0.5                                                                                             0.6
                        60M     220M       770M    2.7B   60M     220M        770M   2.7B                               1     10      100     1000   1        10   100   1000
                                   Mask filling model size (# parameters)                                                             Number of perturbations
Figure 7. There is a clear association between capacity of mask-                                Figure 8. Impact of varying the number of perturbations (samples
filling model and detection performance, across source model                                    of mask and mask-fill) used by DetectGPT on AUROC for GPT-2
scales. Random mask filling (uniform sampling from mask filling                                 (left) and GPT-J (right) to estimate the perturbation discrepancy
model vocabulary) performs poorly, reinforcing the idea that the                                on detection. Averaging up to 100 perturbations greatly increases
perturbation function should produce samples on the data manifold.                              DetectGPT’s reliability. Perturbations sampled from T5-large.
Curves show AUROC scores on 200 SQuAD contexts.

WritingPrompts. The results are presented in Figure 6,                                           larly how the domain impacts the threshold separating the
showing that when the surrogate model is different from the                                      perturbation discrepancy distributions of model-generated
source model, detection performance is reduced, indicating                                       and human texts as well as the impact of passage length on
that DetectGPT is most suited to the white-box setting. Yet                                      detection. Figure 9 shows the perturbation discrepancy dis-
we also observe that if we fix the model used for scoring                                        tributions for model-generated and human texts across four
and average across source models whose generations are                                           data distributions, using GPT-Neo-2.7B to generate sam-
detected (average within column), there is significant varia-                                    ples. A threshold of slightly below 0.1 separates human and
tion in AUROC; GPT-2 and GPT-Neo-2.7 seem to be better                                           model texts across data distributions, which is important for
‘scorers’ than GPT-J. These variations in cross-model scor-                                      practical scenarios in which a passage may be analyzed with-
ing performance suggest ensembling scoring models may                                            out knowing its domain a priori. Finally, Figure 10 shows an
be a useful direction for future research; see Mireshghallah                                     analysis of DetectGPT’s performance as a function of pas-
et al. (2023) for reference.                                                                     sage length. We bin the paired human- and model-generated
                                                                                                 sequences by their average length into three bins of equal
                                                                                                 size (bottom/middle/top third), and plot the AUROC within
 5.3. Other factors impacting performance of DetectGPT
                                                                                                 each bin. The relationship between detection performance
 In this section, we explore how factors such as the size of the                                 and passage length generally depends on the dataset and
 mask-filling model, the number of perturbations used to es-                                     model (or tokenizer). For very long sequences, DetectGPT
 timate the expectation in Equation 1, or the data distribution                                  may see reduced performance because our implementation
 of the text to be detected impact detection quality.                                            of DetectGPT applies all T5 mask-filling perturbations at
                                                                                                 once, and T5 may fail to track many mask tokens at once.
 Source and mask-filling model scale. Here we study the
                                                                                                 By applying perturbations in multiple sequential rounds of
 impact of the size of the source model and mask-filling
                                                                                                 smaller numbers of masks, this effect may be mitigated.
 model on DetectGPT’s performance; the results are shown
 in Figure 7. In particular, the increased discrimination power
 of DetectGPT for larger mask-filling models supports the                                        6. Discussion
 interpretation that DetectGPT is estimating the curvature
                                                                                                 As large language models continue to improve, they will
 of the log probability in a latent semantic space, rather
                                                                                                 become increasingly attractive tools for replacing human
 than in raw token embedding space. Larger T5 models
                                                                                                 writers in a variety of contexts, such as education, jour-
 better represent this latent space, where random directions
                                                                                                 nalism, and art. While legitimate uses of language model
 correspond to meaningful changes in the text.
                                                                                                 technologies exist in all of these settings, teachers, readers,
 Number of perturbations for DetectGPT. We evaluate the                                          and consumers are likely to demand tools for verifying the
 performance of DetectGPT as a function of the number of                                         human origin of certain content with high educational, so-
 perturbations used to estimate the expectation in Equation 1                                    cietal, or artistic significance, particularly when factuality
 on three datasets. The results are presented in Figure 8.                                       (and not just fluency) is crucial.
 Detection accuracy continues to improve until 100 pertur-
                                                                                                 In light of these elevated stakes and the regular emergence of
 bations, where it converges. Evaluations use 100 examples
                                                                                                 new large language models, we study the zero-shot machine-
 from each dataset.
                                                                                                 generated text detection problem, in which we use only the
 Data distributional properties. We study more closely                                           raw log probabilities computed by a generative model to
 the impact of the data distribution on DetectGPT, particu-                                      determine if a candidate passage was sampled from it. We

                                                                                            8
                                          Zero-Shot Machine-Generated Text Detection using Probability Curvature

            1.0             XSum                         WritingPrompts                                                    gpt-2                                             opt-2.7
                                                                                                      0.995                                             0.99
            60
                                                                                                                                                        0.98




                                                                                              AUROC




                                                                                                                                                AUROC
            40
            0.8                                                                                       0.990

            20                                                                                        0.985                                             0.97         XSum
                                                                                                                                                                     SQuAD
            0.60
Frequency




                                                                                                                                                                     WritingPrompts
                     0.0     0.1    0.2           0.1     0.0      0.1     0.2                                                                          0.96
                                                                                                                    Average length                                    Average length
                           SQuAD                                PubMed                                              EleutherAI/gpt-j-6b                          EleutherAI/gpt-neox-20b
            0.4                       Human                                                           0.975
            60                        Model
                                                                                                      0.950                                              0.9




                                                                                              AUROC




                                                                                                                                                 AUROC
            40                                                                                        0.925
            0.2
            20                                                                                        0.900                                              0.8
                                                                                                      0.875
            0.00                                                                                                                                         0.7
               0.0   0.0   0.20.1    0.20.4     0.1 0.6 0.0      0.1 0.8 0.2     0.31.0                       130    140   150     160    170                  130     140      150    160   170
                     Log Probability Change (Perturbation Discrepancy)                                              Average length                                    Average length

Figure 9. Perturbation discrepancy distributions for GPT-Neo                                  Figure 10. DetectGPT AUROC vs passage length. The relation-
(2.7B) and humans across domains. A threshold of 0.1 gener-                                   ship between detection performance and passage length generally
ally separates model- and human-generated text well, which is                                 depends on the dataset and model (or tokenizer). Decreases in
important for practical scenarios where the domain is unknown.                                detection quality with increasing length may be due to T5 failing
                                                                                              to track many (20+) masks to fill at once; this problem may be
 identify a property of the log probability function computed                                 mitigated by applying mask-fills in a sequence of smaller batches.
 by a wide variety of large language models, showing that a
 tractable approximation to the trace of the Hessian of the
                                                                                              of lower quality perturbations. Finally, DetectGPT is more
 model’s log probability function provides a useful signal
                                                                                              compute-intensive than other methods for detection, as it
 for detecting model samples. Our experiments find that
                                                                                              requires sampling and scoring the set of perturbations for
 this signal is more discriminative than existing zero-shot
                                                                                              each candidate passage, rather than just the candidate pas-
 detection methods and is competitive with bespoke detection
                                                                                              sage; a better tuned perturbation function or more efficient
 models trained with millions of model samples.
                                                                                              curvature approximation may help mitigate these costs.
DetectGPT and Watermarking. One interpretation of
                                                                                              Future Work. While the methods in this work make no
the perturbation function is producing semantically similar
                                                                                              assumptions about the models generating the samples, fu-
rephrasings of the original passage. If these rephrasings
                                                                                              ture work may explore how watermarking algorithms can be
are systematically lower-probability than the original pas-
                                                                                              used in conjunction with detection algorithms like Detect-
sage, the model is exposing its bias toward the specific (and
                                                                                              GPT to further improve detection robustness as language
roughly arbitrary, by human standards) phrasing used. In
                                                                                              models continually improve their reproductions of human
other words, LLMs that do not perfectly imitate human
                                                                                              text. Separately, the results in Section 5.2 suggest that ex-
writing essentially watermark themselves implicitly. Under
                                                                                              tending DetectGPT to use ensembles of models for scoring,
this interpretation, efforts to manually add watermarking bi-
                                                                                              rather than a single model, may improve detection in the
ases to model outputs (Aaronson, 2022; Kirchenbauer et al.,
                                                                                              black box setting. Another topic that remains unexplored
2023) may further improve the effectiveness of methods
                                                                                              is the relationship between prompting and detection; that
such as DetectGPT, even as LLMs continue to improve.
                                                                                              is, can a clever prompt successfully prevent a model’s gen-
 Limitations. One limitation of probability-based methods                                     erations from being detected by existing methods? Finally,
 for zero-shot machine-generated text detection (like Detect-                                 future work may explore whether the local log probabil-
 GPT) is the white-box assumption that we can evaluate log                                    ity curvature property we identify is present for generative
 probabilities of the model(s) in question. For models be-                                    models in other domains, such as audio, video, or images.
 hind APIs that do provide probabilities (such as GPT-3),                                     We hope that the present work serves as inspiration to fu-
 evaluating probabilities nonetheless costs money. Another                                    ture work developing effective, general-purpose methods
 assumption of DetectGPT is access to a reasonable pertur-                                    for mitigating potential harms of machine-generated media.
 bation function. While in this work, we use off-the-shelf
 mask-filling models such as T5 and mT5 (for non-English                                      Acknowledgements
 languages), some domains may see reduced performance
 if existing mask-filling models do not well represent the                                    EM gratefully acknowledges funding from a Knight-
 space of meaningful rephrases, reducing the quality of the                                   Hennessy Graduate Fellowship. CF and CM are CIFAR
 curvature estimate. While DetectGPT provides the best                                        Fellows. The Stanford Center for Research on Foundation
 available detection performance for PubMedQA, its drop                                       Models (CRFM) provided part of the compute resources
 in performance compared to other datasets may be a result                                    used for the experiments in this work.

                                                                                          9
                          Zero-Shot Machine-Generated Text Detection using Probability Curvature

References                                                              G., Yin, P., Duke, T., Levskaya, A., Ghemawat, S., Dev,
                                                                        S., Michalewski, H., Garcia, X., Misra, V., Robinson,
Aaronson, S. My Projects at OpenAI, Nov 2022. URL
                                                                        K., Fedus, L., Zhou, D., Ippolito, D., Luan, D., Lim,
  https://scottaaronson.blog/?p=6823.
                                                                        H., Zoph, B., Spiridonov, A., Sepassi, R., Dohan, D.,
Bakhtin, A., Gross, S., Ott, M., Deng, Y., Ranzato, M.,                 Agrawal, S., Omernick, M., Dai, A. M., Pillai, T. S.,
  and Szlam, A. Real or fake? Learning to discriminate                  Pellat, M., Lewkowycz, A., Moreira, E., Child, R., Polo-
  machine from human generated text. arXiv, 2019. URL                   zov, O., Lee, K., Zhou, Z., Wang, X., Saeta, B., Diaz,
  http://arxiv.org/abs/1906.03351.                                      M., Firat, O., Catasta, M., Wei, J., Meier-Hellstern, K.,
                                                                        Eck, D., Dean, J., Petrov, S., and Fiedel, N. PaLM:
Black, S., Gao, L., Wang, P., Leahy, C., and Biderman, S.               Scaling language modeling with pathways, 2022. URL
  GPT-Neo: Large Scale Autoregressive Language Model-                   https://arxiv.org/abs/2204.02311.
  ing with Mesh-Tensorflow, March 2021. URL https:
  //doi.org/10.5281/zenodo.5297715.                                   Christian, J. CNET secretly used AI on articles that
                                                                        didn’t disclose that fact, staff say. https://web.
Black, S., Biderman, S., Hallahan, E., Anthony, Q., Gao,                archive.org/web/20230124063916/https:
  L., Golding, L., He, H., Leahy, C., McDonell, K., Phang,              //futurism.com/cnet-ai-articles-label,
  J., Pieler, M., Prashanth, U. S., Purohit, S., Reynolds, L.,          2023. Accessed: 2023-01-25.
  Tow, J., Wang, B., and Weinbach, S. GPT-NeoX-20B:
  An open-source autoregressive language model. In Pro-               Christiano, P. F., Leike, J., Brown, T., Martic, M., Legg,
  ceedings of the ACL Workshop on Challenges & Perspec-                 S., and Amodei, D. Deep reinforcement learning from
  tives in Creating Large Language Models, 2022. URL                    human preferences. In Guyon, I., Luxburg, U. V.,
  https://arxiv.org/abs/2204.06745.                                     Bengio, S., Wallach, H., Fergus, R., Vishwanathan, S.,
                                                                        and Garnett, R. (eds.), Advances in Neural Information
Bojar, O. r., Chatterjee, R., Federmann, C., Graham, Y.,                Processing Systems, volume 30. Curran Associates, Inc.,
  Haddow, B., Huck, M., Jimeno Yepes, A., Koehn, P.,                    2017. URL https://proceedings.neurips.
  Logacheva, V., Monz, C., Negri, M., Neveol, A., Neves,                cc/paper_files/paper/2017/file/
  M., Popel, M., Post, M., Rubino, R., Scarton, C., Specia,             d5e2c0adad503c91f91df240d0cd4e49-Paper.
  L., Turchi, M., Verspoor, K., and Zampieri, M. Findings               pdf.
  of the 2016 conference on machine translation. In Pro-
  ceedings of the First Conference on Machine Translation,            Devlin, J., Chang, M.-W., Lee, K., and Toutanova, K. BERT:
  pp. 131–198, Berlin, Germany, August 2016. Associa-                   Pre-training of deep bidirectional transformers for lan-
  tion for Computational Linguistics. URL http://www.                   guage understanding. In Proceedings of the 2019 Confer-
  aclweb.org/anthology/W/W16/W16-2301.                                  ence of the North American Chapter of the Association for
                                                                        Computational Linguistics: Human Language Technolo-
Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan,                    gies, Volume 1 (Long and Short Papers), pp. 4171–4186,
  J. D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry,              Minneapolis, Minnesota, June 2019. Association for
  G., Askell, A., Agarwal, S., Herbert-Voss, A., Krueger,               Computational Linguistics. doi: 10.18653/v1/N19-1423.
  G., Henighan, T., Child, R., Ramesh, A., Ziegler, D.,                 URL https://aclanthology.org/N19-1423.
  Wu, J., Winter, C., Hesse, C., Chen, M., Sigler, E.,
                                                           Dolhansky, B., Bitton, J., Pflaum, B., Lu, J., Howes, R.,
  Litwin, M., Gray, S., Chess, B., Clark, J., Berner, C.,
                                                             Wang, M., and Ferrer, C. C. The deepfake detection chal-
  McCandlish, S., Radford, A., Sutskever, I., and Amodei,
                                                             lenge dataset, 2020. URL https://ai.facebook.
  D. Language models are few-shot learners. In Larochelle,
                                                             com/datasets/dfdc/.
  H., Ranzato, M., Hadsell, R., Balcan, M., and Lin,
  H. (eds.), Advances in Neural Information Processing     Fagni, T., Falchi, F., Gambini, M., Martella, A., and
  Systems, volume 33, pp. 1877–1901. Curran Asso-            Tesconi, M. Tweepfake: About detecting deepfake tweets.
  ciates, Inc., 2020. URL https://proceedings.               PLOS ONE, 16(5):1–16, 05 2021. doi: 10.1371/journal.
  neurips.cc/paper/2020/file/                                pone.0251415. URL https://doi.org/10.1371/
  1457c0d6bfcb4967418bfb8ac142f64a-Paper.                    journal.pone.0251415.
  pdf.
                                                           Fan, A., Lewis, M., and Dauphin, Y. Hierarchical neu-
Chowdhery, A., Narang, S., Devlin, J., Bosma, M., Mishra,    ral story generation. In Proceedings of the 56th An-
  G., Roberts, A., Barham, P., Chung, H. W., Sutton,         nual Meeting of the Association for Computational Lin-
  C., Gehrmann, S., Schuh, P., Shi, K., Tsvyashchenko,       guistics (Volume 1: Long Papers), pp. 889–898, Mel-
  S., Maynez, J., Rao, A., Barnes, P., Tay, Y., Shazeer,     bourne, Australia, July 2018. Association for Computa-
  N., Prabhakaran, V., Reif, E., Du, N., Hutchinson, B.,     tional Linguistics. doi: 10.18653/v1/P18-1082. URL
  Pope, R., Bradbury, J., Austin, J., Isard, M., Gur-Ari,    https://aclanthology.org/P18-1082.

                                                                 10
                         Zero-Shot Machine-Generated Text Detection using Probability Curvature

Gehrmann, S., Strobelt, H., and Rush, A. GLTR: Statistical            text, but retrieval is an effective defense. arXiv preprint
  detection and visualization of generated text. In Proceed-          arXiv:2303.13408, 2023.
  ings of the 57th Annual Meeting of the Association for
  Computational Linguistics: System Demonstrations, pp.             Liang, W., Yuksekgonul, M., Mao, Y., Wu, E., and Zou,
 111–116, Florence, Italy, July 2019. Association for Com-            J. Gpt detectors are biased against non-native english
  putational Linguistics. doi: 10.18653/v1/P19-3019. URL              writers. arXiv preprint arXiv:2304.02819, 2023.
  https://aclanthology.org/P19-3019.                                Lin, S., Hilton, J., and Evans, O. TruthfulQA: Measuring
Guarnera, L., Giudice, O., and Battiato, S. Deepfake detec-           how models mimic human falsehoods. In Proceedings of
  tion by analyzing convolutional traces. In Proceedings              the 60th Annual Meeting of the Association for Compu-
  of the IEEE/CVF Conference on Computer Vision and                   tational Linguistics (Volume 1: Long Papers), pp. 3214–
  Pattern Recognition (CVPR) Workshops, June 2020.                    3252, Dublin, Ireland, May 2022. Association for Com-
                                                                      putational Linguistics. doi: 10.18653/v1/2022.acl-long.
Güera, D. and Delp, E. J. Deepfake video detection                   229. URL https://aclanthology.org/2022.
  using recurrent neural networks. In 2018 15th IEEE                  acl-long.229.
  International Conference on Advanced Video and Sig-
  nal Based Surveillance (AVSS), pp. 1–6, 2018. doi:                Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D.,
  10.1109/AVSS.2018.8639163.                                          Levy, O., Lewis, M., Zettlemoyer, L., and Stoyanov, V.
                                                                      Roberta: A robustly optimized bert pretraining approach.
Hutchinson, M. A stochastic estimator of the trace of                 arXiv preprint arXiv:1907.11692, 2019.
  the influence matrix for laplacian smoothing splines.
 Communications in Statistics - Simulation and Com-                 Mireshghallah, F., Mattern, J., Gao, S., Shokri, R., and Berg-
  putation, 19(2):433–450, 1990.       doi: 10.1080/                 Kirkpatrick, T. Smaller language models are better black-
  03610919008812866. URL https://doi.org/10.                         box machine-generated text detectors. arXiv preprint
 1080/03610919008812866.                                             arXiv:2305.09859, 2023.

Ippolito, D., Duckworth, D., Callison-Burch, C., and Eck,           Narayan, S., Cohen, S. B., and Lapata, M. Don’t give me
  D. Automatic detection of generated text is easiest when            the details, just the summary! Topic-aware convolutional
  humans are fooled. In Proceedings of the 58th Annual                neural networks for extreme summarization. In Proceed-
  Meeting of the Association for Computational Linguis-               ings of the 2018 Conference on Empirical Methods in
  tics, pp. 1808–1822, Online, July 2020. Association                 Natural Language Processing, Brussels, Belgium, 2018.
  for Computational Linguistics. doi: 10.18653/v1/2020.
                                                                    OpenAI. Chatgpt: Optimizing language models for
  acl-main.164. URL https://www.aclweb.org/
                                                                      dialogue.  http://web.archive.org/web/
  anthology/2020.acl-main.164.
                                                                      20230109000707/https://openai.com/
Jawahar, G., Abdul-Mageed, M., and Lakshmanan, L. V. S.               blog/chatgpt/, 2022. Accessed: 2023-01-10.
  Automatic detection of machine generated text: A critical
  survey. In International Conference on Computational              Radford, A., Wu, J., Child, R., Luan, D., Amodei,
  Linguistics, 2020.                                                  D., and Sutskever, I.      Language models are
                                                                      unsupervised multitask learners, 2019.    URL
Jin, Q., Dhingra, B., Liu, Z., Cohen, W., and Lu, X. Pub-             https://d4mucfpksywv.cloudfront.net/
   MedQA: A dataset for biomedical research question an-              better-language-models/language_
   swering. In Proceedings of the 2019 Conference on Em-              models_are_unsupervised_multitask_
   pirical Methods in Natural Language Processing and                 learners.pdf.
   the 9th International Joint Conference on Natural Lan-
   guage Processing (EMNLP-IJCNLP), pp. 2567–2577,                  Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang,
   Hong Kong, China, November 2019. Association for                   S., Matena, M., Zhou, Y., Li, W., and Liu, P. J. Ex-
   Computational Linguistics. doi: 10.18653/v1/D19-1259.              ploring the limits of transfer learning with a unified
   URL https://aclanthology.org/D19-1259.                             text-to-text transformer. Journal of Machine Learning
                                                                      Research, 21(140):1–67, 2020. URL http://jmlr.
Kirchenbauer, J., Geiping, J., Wen, Y., Katz, J., Miers, I.,          org/papers/v21/20-074.html.
  and Goldstein, T. A watermark for large language mod-
  els, 2023. URL https://arxiv.org/abs/2301.                        Rajpurkar, P., Zhang, J., Lopyrev, K., and Liang, P. SQuAD:
  10226.                                                              100,000+ questions for machine comprehension of text.
                                                                      In Proceedings of the 2016 Conference on Empirical
Krishna, K., Song, Y., Karpinska, M., Wieting, J., and                Methods in Natural Language Processing, pp. 2383–
  Iyyer, M. Paraphrasing evades detectors of ai-generated             2392, Austin, Texas, November 2016. Association for

                                                               11
                         Zero-Shot Machine-Generated Text Detection using Probability Curvature

  Computational Linguistics. doi: 10.18653/v1/D16-1264.
  URL https://aclanthology.org/D16-1264.
Roose, K. and Newton, C. ChatGPT transforms a
  classroom and is ‘M3GAN’ real?  Hard Fork, a
  New York Times Podcast, 2022. URL https://
  www.nytimes.com/2023/01/13/podcasts/
  hard-fork-chatgpt-teachers-gen-z-cameras-m3gan.
  html.
Sadasivan, V. S., Kumar, A., Balasubramanian, S., Wang,
  W., and Feizi, S. Can ai-generated text be reliably de-
  tected? arXiv preprint arXiv:2303.11156, 2023.
Solaiman, I., Brundage, M., Clark, J., Askell, A., Herbert-
  Voss, A., Wu, J., Radford, A., and Wang, J. Release
  strategies and the social impacts of language models,
  2019. URL https://arxiv.org/ftp/arxiv/
  papers/1908/1908.09203.pdf.
Uchendu, A., Le, T., Shu, K., and Lee, D. Authorship attribu-
  tion for neural text generation. In Proceedings of the 2020
  Conference on Empirical Methods in Natural Language
  Processing (EMNLP), pp. 8384–8395, Online, November
  2020. Association for Computational Linguistics. doi:
 10.18653/v1/2020.emnlp-main.673. URL https://
  aclanthology.org/2020.emnlp-main.673.
Wang, B. and Komatsuzaki, A.      GPT-J-6B: A
 6 Billion Parameter Autoregressive Language
 Model.   https://github.com/kingoflolz/
 mesh-transformer-jax, May 2021.
Zellers, R., Holtzman, A., Rashkin, H., Bisk, Y., Farhadi,
  A., Roesner, F., and Choi, Y. Defending against neural
  fake news. In Neural Information Processing Systems,
  2019.
Zhang, S., Roller, S., Goyal, N., Artetxe, M., Chen, M.,
  Chen, S., Dewan, C., Diab, M., Li, X., Lin, X. V., Mi-
  haylov, T., Ott, M., Shleifer, S., Shuster, K., Simig, D.,
  Koura, P. S., Sridhar, A., Wang, T., and Zettlemoyer,
  L. Opt: Open pre-trained transformer language mod-
  els, 2022. URL https://arxiv.org/abs/2205.
  01068.
Zhao, H., Zhou, W., Chen, D., Wei, T., Zhang, W., and Yu, N.
  Multi-attentional deepfake detection. In Proceedings of
  the IEEE/CVF conference on computer vision and pattern
  recognition, pp. 2185–2194, 2021.
Zi, B., Chang, M., Chen, J., Ma, X., and Jiang, Y.-G. Wild-
  deepfake: A challenging real-world dataset for deepfake
  detection. In Proceedings of the 28th ACM international
  conference on multimedia, pp. 2382–2390, 2020.
Ziegler, D. M., Stiennon, N., Wu, J., Brown, T. B., Radford,
  A., Amodei, D., Christiano, P., and Irving, G. Fine-tuning
  language models from human preferences, 2020.

                                                                12
                             Zero-Shot Machine-Generated Text Detection using Probability Curvature

A. Complete Results for Top-p and Top-k Decoding
Tables 4 and 5 contain the complete results for XSum, SQuAD, and WritingPrompts for the five models considered in
Table 1. On average, both top-p and top-k sampling seem to make the detection task easier. This result is perhaps intuitive,
as both sampling methods strictly increase the average log likelihood of model generations under the model (as they truncate
low-probability tokens, albeit with different heuristics). Therefore methods based on probability or rank of tokens should
become more discriminative.
                              XSum                                                 SQuAD                                           WritingPrompts
Method      GPT-2 OPT-2.7 Neo-2.7 GPT-J NeoX         Avg.    GPT-2 OPT-2.7 Neo-2.7 GPT-J NeoX             Avg.    GPT-2 OPT-2.7 Neo-2.7 GPT-J NeoX Avg.
log p(x)    0.93    0.93    0.94     0.91    0.87    0.92    0.96    0.94         0.91    0.87    0.79    0.89    0.99*    0.98*      0.98*   0.97*   0.97*   0.98
Rank        0.80    0.77    0.77     0.75    0.73    0.76    0.84    0.82         0.81    0.80    0.75    0.81    0.87     0.84       0.83    0.83    0.81    0.84
LogRank     0.95*   0.94*   0.96*    0.93*   0.89*   0.93*   0.98*   0.96*        0.94*   0.90    0.83    0.92*   0.99*    0.98*      0.98*   0.98    0.98    0.98
Entropy     0.55    0.46    0.53     0.54    0.58    0.53    0.53    0.50         0.55    0.56    0.57    0.54    0.32     0.37       0.28    0.32    0.32    0.32
DetectGPT   0.99    0.98    1.00     0.98    0.97    0.98    0.99    0.98         0.98    0.90    0.82*   0.94    1.00     0.99       0.99    0.97*   0.93    0.98
Diff        0.04    0.04    0.04     0.05    0.08    0.05    0.01    0.02         0.04    0.00    -0.01   0.02    0.01     0.01       0.01    -0.01   -0.05   0.00


Table 4. Nucleus (top-p) sampling evaluation with p = 0.96. AUROC for detecting samples from the given model on the given dataset for
DetectGPT and four previously proposed criteria. Nucleus sampling generally makes detection easier for all methods, but DetectGPT still
provides the highest average AUROC. For WritingPrompts, however, the LogRank baseline performs as well as DetectGPT.


                              XSum                                                 SQuAD                                           WritingPrompts
Method      GPT-2 OPT-2.7 Neo-2.7 GPT-J NeoX         Avg.    GPT-2 OPT-2.7 Neo-2.7 GPT-J NeoX             Avg.    GPT-2 OPT-2.7 Neo-2.7 GPT-J NeoX Avg.
log p(x)    0.89    0.89    0.89     0.84    0.81    0.87    0.93    0.90         0.88    0.82    0.74    0.85     0.97    0.95       0.97    0.96    0.95*   0.96
Rank        0.79    0.77    0.77     0.75    0.73    0.76    0.84    0.82         0.80    0.80    0.75    0.80     0.87    0.84       0.83    0.82    0.81    0.83
LogRank     0.92*   0.91*   0.93*    0.89*   0.85*   0.90*   0.96*   0.94*        0.92*   0.87*   0.79*   0.90*    0.98*   0.97*      0.98*   0.97    0.96    0.97
Entropy     0.58    0.49    0.55     0.56    0.59    0.55    0.55    0.52         0.56    0.56    0.58    0.56     0.35    0.41       0.30    0.34    0.37    0.35
DetectGPT   0.99    0.97    0.99     0.96    0.96    0.98    0.99    0.98         0.98    0.89    0.80    0.93     0.99    0.98       0.99    0.97    0.93    0.97
Diff        0.07    0.06    0.06     0.07    0.11    0.08    0.03    0.04         0.06    0.02    0.01    0.03     0.01    0.01       0.01    0.00    -0.03   0.00


Table 5. Top-k sampling evaluation with k = 40. DetectGPT generally provides the most accurate performance (highest AUROC),
although the gap is narrowed comparing to direct sampling, presumably because top-k generations are more generic.




                                                                             13
