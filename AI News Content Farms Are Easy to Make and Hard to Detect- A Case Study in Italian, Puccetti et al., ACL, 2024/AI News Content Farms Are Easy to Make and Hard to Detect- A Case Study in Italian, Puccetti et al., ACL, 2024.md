              AI ‘News’ Content Farms Are Easy to Make and Hard to Detect:
                                 A Case Study in Italian
         Giovanni Puccettiα , Anna Rogersβ , Chiara Alzettaγ , Felice Dell’Orlettaγ , Andrea Esuliα
                       α
                         Istituto di Scienza e Tecnologia dell’Informazione “A. Faedo”
                            {giovanni.puccetti,andrea.esuli}@isti.cnr.it
                                         β
                                           IT University of Copenhagen
                                                 arog@itu.dk
               γ
                 ItaliaNLP Lab, Istituto di Linguistica Computazionale “Antonio Zampolli”
                          {chiara.alzetta,felice.dellorletta}@ilc.cnr.it

                              Abstract
           Large Language Models (LLMs) are increas-
           ingly used as ‘content farm’ models (CFMs),
           to generate synthetic text that could pass for
           real news articles. This is already happening
           even for languages that do not have high-quality
           monolingual LLMs. We show that fine-tuning
           Llama (v1), mostly trained on English, on as lit-
           tle as 40K Italian news articles, is sufficient for
           producing news-like texts that native speakers
           of Italian struggle to identify as synthetic.            Figure 1: Detecting synthetic Italian news text generated
           We investigate three LLMs and three methods              by fine-tuned Llama-65B: error rates for DetectGPT,
           of detecting synthetic texts (log-likelihood, De-        native speakers of Italian and random guess.
           tectGPT, and supervised classification), finding
           that they all perform better than human raters,
           but they are all impractical in the real world           2024 their count1 was 840. Sometimes such sites
           (requiring either access to token likelihood in-         publish original ‘content’, and sometimes they au-
           formation or a large dataset of CFM texts). We           tomatically ‘rewrite’ articles from real news outlets
           also explore the possibility of creating a proxy         without attribution (Brewster et al., 2023). They
           CFM: an LLM fine-tuned on a similar dataset              are primarily created for serving programmatic ads,
           to one used by the real ‘content farm’. We find          and even major brands may unwittingly support
           that even a small amount of fine-tuning data suf-
                                                                    such ‘outlets’ (Ryan-Mosley, 2023). They already
           fices for creating a successful detector, but we
           need to know which base LLM is used, which               operate in many languages.2 The problem will
           is a major challenge.                                    likely only get worse with time, and it needs more
                                                                    attention both on the policy & regulation side and
           Our results suggest that there are currently no
           practical methods for detecting synthetic news-          from the NLP researchers.
           like texts ‘in the wild’, while generating them             We illustrate how easy it is to create ‘content
           is too easy. We highlight the urgency of more            farm’ models (CFMs), and how hard to detect
           NLP research on this problem.                            them, by considering a case that should be rela-
                                                                    tively tricky. In §3 we successfully turn Llama, a
     1     Introduction                                             relatively old LLM mostly trained on English, into
     The modern Large Language Models (LLMs) can                    an Italian news CFM – by fine-tuning it on only
     generate increasingly fluent and plausible-sounding            40k Italian news texts. For Llama65B this turns
     texts, which sparks concerns about their potential             out to be sufficient to mislead native speakers of
     misuse by bad actors. One of the emerging prob-                Italian, who identify synthetic texts with only 64%
     lems is AI-driven news “content farms”: news-like              accuracy, vs 50% random guess (see §4). We also
     sites filled with synthetic texts that are not neces-          find that existing detection methods perform better
     sarily serving a misinformation campaign, but are                   1
                                                                         https://www.newsguardtech.com/
     plausible-looking enough to deceive the readers                special-reports/ai-tracking-center/
                                                                       2
     and generate web traffic. Already in May 2023                       NewsGuard AI Tracking Center currently states that
                                                                    they found such ‘outlets’ in Arabic, Chinese, Czech, Dutch,
     NewsGuard reported that they found 49 such ‘out-               English, French, German, Indonesian, Italian, Korean, Por-
     lets’ (Sadeghi and Arvanitis, 2023), and on June 4th           tuguese, Russian, Spanish, Tagalog, Thai, and Turkish.

                                                                 15312
Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 15312–15338
                               August 11-16, 2024 ©2024 Association for Computational Linguistics
than humans (§5), but are impractical in the real         estimation, (iv) negative log-likelihood curvature,
world (§7).                                               (v) stylometric variation, and (vi) classifier-based
    In §6 we explore an alternative approach: fine-       approaches.
tuning another LLM as a proxy for the real CFM               After the release of ChatGPT (OpenAI, 2022)
and relying on its token likelihood scores as proxies     and GPT-4 (OpenAI, 2023), a lot of studies (mostly
for the scores of the real CFM. We find that this         not yet peer reviewed) focused specifically on the
works with even a small amount of fine-tuning data        detection of text generated by these models (Dhaini
(only 3% of the full fine-tuning dataset) but only        et al., 2023). Since it is not possible to access token
given that we know which base LLM was used as             probabilities for a candidate generated text, some of
CFM. We also experiment with using these proxy            this work relies on a proxy model (Vasilatos et al.,
scores to identify the base LLM, but this method          2023), but most rely on supervised classification
would also be impractical if there are dozens, if not     (Mitrović et al., 2023; Liao et al., 2023; Guo et al.,
hundreds possible alternatives.                           2023; Liu et al., 2023), including OpenAI itself
    We hope that our findings will boost similar in-      (Kirchner et al., 2023). Sometimes classical ma-
vestigations for other languages, and highlight the       chine learning techniques are reported to perform
urgency of developing model-agnostic methods for          well: e.g. Desaire et al. (2023) report a high perfor-
synthetic text detection. To facilitate future re-        mance on chemistry articles with XGBoost classi-
search on Italian, we release (i) 15k news passages       fier and 20 features extracted from paragraphs.
generated by models fine-tuned on the CHANGE-it              Recently, several benchmarks for the synthetic
dataset, an Italian news dataset (Mattei et al., 2020),   text detection task have been released, Wang et al.
(ii) ratings produced by 5 human annotators on 400        (2024b,a) contribute a large multilingual, multi-
texts, with a balanced distribution of 50% human-         domain dataset that can be used to benchmark syn-
written and 50% synthetic passages, and (iii) 600k        thetic text detection systems. Macko et al. (2023)
synthetic alterations of both the original samples        propose a benchmark for the detection of text gen-
from the CHANGE-it dataset and the synthetic              erated by multilingual LLMs, while Dugan et al.
texts. The code and data are publicly available.3         (2024) propose a very large benchmark for syn-
    We will not publicly release our fine-tuned           thetic text detection, controlling for the temperature
LLMs (since they are best suited to be used as            used to generated the text, which has been shown
CFMs), but we welcome direct requests from re-            to be relevant for detection (Mitchell et al., 2023).
searchers working on this problem.                           The above works focus on the scenario where the
                                                          effort of detecting synthetic texts is on the user side.
2       Related work                                      The complementary direction on the developer side
                                                          is watermarking: ensuring that the LLM output cre-
Driven by the increasing number of strong openly
                                                          ates some kind of statistical “signature” that would
available LLMs (Touvron et al., 2023a; Brown
                                                          help to identify it. There are multiple proposals for
et al., 2020; Raffel et al., 2020; Jiang et al., 2023),
                                                          how to do this (Fernandez et al., 2023; Kirchner
several studies focused on the detection of synthetic
                                                          et al., 2023; Kuditipudi et al., 2024; Li et al., 2023;
text detection.
                                                          Takezawa et al., 2023; Wu et al., 2023; Yoo et al.,
   Ghosal et al. (2023) identified two main groups
                                                          2023, inter alia), and some initial results suggesting
of approaches: those based on token likelihood,
                                                          that such techniques could be sufficiently robust to
and supervised classification. Among the former,
                                                          human and machine paraphrasing (Kirchenbauer
Mitchell et al. (2023); Su et al. (2023); Hans et al.
                                                          et al., 2023, 2024). However, most of the current
(2024); Gehrmann et al. (2019); Mireshghallah
                                                          ‘open’ LLMs are freely available without any wa-
et al. (2024) proposed detection methods that rely
                                                          termarking, and as we will show, they are already
on language models token distribution. For the su-
                                                          sufficient to be used as CFMs.
pervised detection, Verma et al. (2023) proposed an
                                                             For the problem of detecting synthetic text with-
approach that relies on the availability of labelled
                                                          out watermarking, the current research focuses
datasets of synthetic and human-written texts.
                                                          on either monolingual or multilingual-by-design
   Chakraborty et al. (2023a) propose a 6-way split
                                                          LLMs, and most studies do not focus on a spe-
of synthetic text detection methodologies: (i) water-
                                                          cific domain. We stress the importance of also
marking, (ii) perplexity estimation, (iii) burstiness
                                                          investigating fine-tuned models because LLMs are
    3
        https://github.com/gpucce/synthetic_llm_data      expensive to both train and run inference on (Samsi
                                                       15313
et al., 2023). Hence, starting from a public, rela-               could increase the number of bad actors.
tively small, but high-quality LLM and fine-tuning
it for a specific type of content is probably the most            4    Detection of Synthetic News in Italian
plausible scenario for ‘content farms’ that aim to                     By Native Speakers
produce texts cheaply. To the best of our knowl-                   Methodology. To assess whether native Italian
edge, this is the first study to focus on the scenario             speakers would be able to identify synthetic news
where the ‘CFM’ is fine-tuned for news, and in a                   texts generated by our CFM, we set up a crowd-
language that it was not meant for originally. More-               based study following the general recommenda-
over, except for the recent work by Wang et al.                    tions for human evaluation of automatically gen-
(2024a), existing resources do not cover Italian.                  erated texts proposed by van der Lee et al. (2021).
                                                                   Specifically, we created 4 surveys, with 100 ques-
3       Fine-tuning of Llama as an Italian
                                                                   tions in each. To maintain the rater engagement,
        ‘Content Farm’ Model                                      we administered the surveys in five sessions, each
As our ‘CFM’, we choose the original Llama model                   comprising 20 questions. The raters were anony-
(Touvron et al., 2023a), in 7B and 65B parameter                   mously recruited among Italian native speakers via
versions. Since this is one of the first public high-              the Prolific6 online crowd-sourcing platform. Five
performing LLMs of this size, our Llama results                    different raters participated in each survey session,
serve as a lower bound for what could be expected                 with no limitations on the number of sessions a rater
from later LLMs, such as Llama 2 (Touvron et al.,                  could undertake. The 20-question sessions took 8
2023b) and Llama 3,4 Aya (Aryabumi et al., 2024),                  mins 23 secs on average, and the raters were com-
and others. We do not suggest that it is possible                  pensated at 9,68$ per hour.7 The study involved a
to obtain good results with any language and any                   total of 93 different raters, with an average age of
LLM (see also §10): such a transfer depends on the                 32.01 (±10.76).
similarity between languages and their coverage                       Each of the 4 surveys is designed to assess the
in the training data. But given that ‘content farms’               texts generated by a different model: Llama 7B
have already been identified in at least 16 languages              and 65B, both with and without fine-tuning on Ital-
(see §1), many others could follow.                                ian news. Each question required raters to read
   Our choice of Italian enables a lower-bound                     two texts, denoted as A and B, and answer the
estimate of what could be expected of monolin-                     question “Text B follows text A, do you think text
gual or multilingual LLMs with more exposure to                   B is written by a machine?”. The answer was a
the target language. Llama is a ‘mostly-English’                   rating on a 5-point Likert scale, where 1 indicates
model, not intended to be multilingual. The re-                   ‘certainly human-written’ and 5 ‘certainly machine-
sources it was trained on, such as C4 corpus (Raffel               generated’. In 50% of the questions, both text A
et al., 2020), made deliberate efforts to filter out               and B were human-written news articles coming
non-English text. However, it was exposed to at                    from the original CHANGE-it test dataset.
least Italian Wikipedia (Touvron et al., 2023a, p.2).                 The topics included daily national political
Hence, Wikipedia is likely the main, if not the only               events (e.g. politicians’ declarations), general news
source of Italian in Llama.                                       (e.g. climate catastrophes), and relevant interna-
   We experiment with the original Llama baseline                  tional news (e.g. European leadership meetings).
(65B pre-trained model with no extra training), and                   To estimate the accuracy of human raters on this
two versions of our Llama fine-tuned on Italian                    task, we map the scores on the 5-point scale to a bi-
news, after 20K and 60K steps. The technical de-                   nary score by computing the average score assigned
tails for fine-tuning are provided in App. B.1. We                 by the raters to a given sample. We interpret the
remark that creating such a CFM now comes with                     average score above 3 as indicating that a given
very few technical or financial difficulties,5 which               sample B was generally perceived as machine-
    4
                                                                   generated. We also experimented with a different
     https://ai.meta.com/blog/meta-llama-3/
    5
     Renting GPUs on cloud providers such as Amazon is now        our results would highlight the necessity of more research on
relatively cheap (approx 15$ per hour for 8x40Gb A100) and        synthetic text detection.
                                                                     6
would require as little as 100$ to replicate one of our LLM            https://www.prolific.co/. The participant group
training sessions and data generation. The technical barrier to   was balanced in terms of gender (49.46% female) and stu-
fine-tuning LLMs is also low now, thanks to tools like Hug-       dent status (50.60% reported being students).
                                                                     7
gingface’s Autotrain:https://huggingface.co/autotrain.                 This hourly payment rate was certified as ‘Fair’ by the
We do not criticize open-sourcing such tools, but we hope that    Prolific platform.

                                                             15314
          Model          Accuracy   STD     Fleiss k           Prompt: "[...] l’ex presidente della Generalitat cata-
                                                               lana la cui coalizione ha conquistato ieri il voto re-
     Llama 7B pretrain     83.2       7.0    36.45
                                                               gionale e che non..." EN: [...] the former president of Catalan
    Llama 7B finetuned     69.5      12.2    22.30
                                                               Generalitat, whose coalition won the regional election yesterday, and
    Llama 65B pretrain     73.7      5.8     33.01             who...
   Llama 65B finetuned     64.2      11.2    20.56             Pre-trained: ... vuole rinunciare alla secessione.
                                                               In the 6-week period prior to 12/06/19... EN: ... does not
                                                               want to give up the secession. In the 6-week period prior to 12/06/19 ...
Table 1: Accuracy and standard deviation achieved              Fine-tuned: ...aveva perso tempo per dire la sua. Da
by human raters in assessing human-written versus              Bruxelles, dove si trova da allora ... EN: ... does not waste
machine-generated news. We report the inter-rater              time to mention his opinion. From Brussels, where he resides since...
agreement measured as group Fleiss’ k.

                                                          Figure 2: Example: without fine-tuning on Italian,
thresholding approach, using the average rating as a      Llama is prone to switching to English.
threshold, that showed similar results; these results
are available in App. C.
                                                          with grammatical errors and 21 with expressions
Results. Table 1 shows the outcome of our anal-           that are grammatically correct but unnatural in Ital-
ysis. Since the raters’ accuracy in detecting news        ian. Annotated examples for each model are shown
generated by the largest fine-tuned Llama 65B is as       in App. D.
low as 64%, we can answer our research question              We stress that this study focuses only on the
positively: Llama can be fine-tuned to generate           problem of synthetic news-like text, which is suffi-
hard-to-detect news-like text in Italian. We only         ciently plausible for the ‘content farms’ to lead the
used 40K samples for fine-tuning a relatively old         users to ‘news’ websites and be served ads. Their
model, so even more plausible-sounding synthetic          success also likely depends on the quality of the
text could likely be created with more data and           ‘headlines’, their match to the interests of the au-
more recent LLMs.                                         dience, the position in the search engine rankings
   Overall, the raters’ accuracy reflects two fore-       and other factors beyond the scope of this study.
seeable trends: the smaller 7B models are easier          Still, having such texts is a necessary, though not
to detect, and the fine-tuned models are harder to        sufficient condition for operating a ‘content farm’.
detect. Interestingly, the small 7B version, when
                                                          5       Automatic Detection of Synthetic News
fine-tuned on Italian, is identified by raters with
accuracy close to the larger pretrained 65B.
                                                                  in Italian
   Table 1 also reports the average inter-rater agree-    5.1       Approaches based on token likelihood
ment for each survey. Fleiss κ (Fleiss et al., 1971) is
                                                          Methodology. Similarly to Jawahar et al. (2020);
in the range between 22%-36%, indicating a “mod-
                                                          Sadasivan et al. (2023); Chakraborty et al. (2023b),
erate” agreement (Landis and Koch, 1977) consis-
                                                          we attempt the zero-shot detection of artificially
tent with similar human-evaluation studies (van der
                                                          generated text. We experiment with two ap-
Lee et al., 2021). The raters agree more strongly
                                                          proaches for synthetic text detection. Both assume
when assessing non-fine-tuned models, possibly
                                                          to have access to the likelihood of each token in a
because they occasionally switch from Italian to
                                                          sentence, according to the model whose “author-
English mid-generation, a characteristic identified
                                                          ship” is under analysis.
by raters as indicative of machine-generated texts.
                                                             The log-likelihood measures how likely a sen-
Figure 2 shows an example of such a switch.
                                                          tence is according to the probability assigned by
   The qualitative analysis of 100 machine-
                                                          the model to each token. The core idea behind the
generated instances (25 per model) showed that
                                                          DetectGPT score (Mitchell et al., 2023) is getting a
46/100 examples had no obvious issues with lan-
                                                          more robust score by normalising the log-likelihood
guage, but, as expected for LLM-generated texts,
                                                          of a sentence based on modifications8 of that same
their content was factually incorrect and, worry-
                                                          sentence generated by a different model (which we
ingly, the factual errors were not necessarily obvi-
ous without extra fact-checking effort. Addition-             8
                                                                In our case, we are interested in the likelihood of a syn-
ally, in this sample of 100 texts, we found 7 ex-         thetic sentence estimated by Llama, vs the normalized likeli-
                                                          hood that Llama assigns to modifications of that same sentence
amples where the generated text contradicted the          that we generate with T5 (Raffel et al., 2020) as the bootstrap
prompt, 8 cases of language-switching, 18 samples         model. See App. D for examples of such modifications.

                                                       15315
            (a) Original Llama 65B                    (b) Fine-tuned epoch 2                  (c) Fine-tuned epoch 6

Figure 3: ROC curve for DetectGPT and log-likelihood. In (a) for Llama 65B measured over 100 sentences from
the CHANGE-it data-set (Italian), in (b) the same measure for Llama 65B model after 20,000 fine tuning steps on
CHANGE-it training set and in (c) after 60,000 fine-tuning steps.


refer to as the bootstrap model).                                   we find that fine-tuning should have made the task
   Given a sentence, both log-likelihood and De-                    more rather than less difficult. Without fine-tuning,
tectGPT can be used with a threshold to tell if                     our Llama CFM has a tendency to switch to English
that sentence is more likely written by a human or                  mid-generation, as we also observed this in the hu-
by a language model. The threshold is estimated                     man detection study (see Figure 2, more examples
empirically based on a collection of synthetic and                  available in App. D). This language switch should
real samples. We refer the reader to Mitchell et al.                be a clear marker for detecting both the original
(2023) for details of likelihood-based methods.                     7B and the 65B models, and it vanishes after fine-
   We start by validating our codebase and imple-                   tuning. But both log-likelihood and DetectGPT are
mentation by repeating prior experiments on xsum                    missing this clear signal.
(Narayan et al., 2018) dataset in English, and we                      Although the DetectGPT and log-likelihood per-
obtain comparable results (see App. E).                             form relatively well in our tests, we stress that this
   To measure the ROC of both DetectGPT and                         indicates a measure of the difficulty of this task,
log-likelihood we select 100 random sentences and                   rather than a solution to synthetic news detection
generate9 another 100 by using the first 30 tokens                  (see section 7). We remark that DetectGPT score
of each sentence as a prompt for the model under                    can be turned into an accuracy measurement by
analysis. After this, we clip all sentences to 150                  fixing a threshold, for a direct comparison with the
tokens,10 measure the score for each sample, and                    human evaluation accuracy. In our case, Detect-
compute the AUROC on all 200 sentences (half                        GPT accuracy is ≈ 80% using the median11 score
human-written and half machine-completed).                          as the threshold for fine-tuned Llama 65B.
   To compare the detection approaches for the orig-
                                                                    5.2   Supervised Detection of Synthetic Texts
inal and fine-tuned Llama, we use the CHANGE-it
test dataset for Italian. As the bootstrap model, we                A different approach to identifying synthetic texts
use IT5-large (Sarti and Nissim, 2022) for Italian.                 is to train supervised classifiers (Liu et al., 2019;
                                                                    Conneau et al., 2020). However, this requires a la-
Results. Figure 3 shows the AUROC of Detect-                        belled and balanced dataset of human and synthetic
GPT and log-likelihood for all our models. log-                     texts. To understand the challenges of this scenario,
likelihood does not seem to react to fine-tuning at                 we use DICE, a different Italian news dataset fo-
all: the fine-tuned models have almost the same                     cusing on crime news (Bonisoli et al., 2023). We
AUROC as the pre-trained one. DetectGPT does                        mix DICE with the CHANGE-it data as well as the
have a 5-6 points higher AUROC for the fine-tuned                   synthetic texts. This simulates a more realistic data
models. However, by qualitative analysis, see §4,                   collection process compared to previous studies
                                                                    that solely focused on fully in-domain data.
   9
      All generation tasks are performed using Nucleus Sam-
pling for decoding (Holtzman et al., 2020).                           11
                                                                         We choose this threshold knowing that the dataset is bal-
   10
      Due to different tokenizers, this step results in sentences   anced and that DetectGPT is monotonic, otherwise we would
with a varying number of words, but a similar length.               need to tune it.

                                                               15316
                                                          specifically made for multilingual settings. We use
                                                          the same hyper-parameters for both classifiers, and
                                                          we train them for 3 epochs. The technical details
                                                          are provided in App. B.3.
                                                          Results. Figure 4 shows that at 8k training sam-
                                                          ples xlm-roberta-large accuracy ranges between
                                                          84% and 92% depending on the generator. With 4k
                                                          training samples, the accuracy decreases between
                                                          81% and 86%, with a similar difference between
                                                          in domain and mixed source. With 2k training sam-
                                                          ples, the performance for all but 3 models drops to
                                                          under 56% – i.e. almost random chance level. The
                                                          RoBERTa-based classifier yields a similar trend.
                                                          See App. B.3 for the graph for RoBERTa and nu-
Figure 4: Accuracy of classifier based on xlm-            merical results for both experiments.
RoBERTa-large for human/synthetic text classification        We find that for these datasets there is a thresh-
task, for synthetic texts generated by three LLMs fine-   old between 2k and 4k samples that marks a strong
tuned on CHANGE-it. The classifier was trained on         difference in the performance of the supervised
50% synthetic texts and either 50% CHANGE-it texts
(in domain), or 25% texts from CHANGE-it and 25%
                                                          classifier (20-25% loss in accuracy), while increas-
from DICE (mixed source). Classification is only suc-     ing the dataset size further provides diminishing
cessful at at least 4K labeled samples, and the mixed     returns (2-8% gain). Our mixed source scenario
source scenario is consistently more challenging.         at 8K samples is also consistently harder for the
                                                          classifier; at 4K the results are mixed across differ-
                                                          ent LLMs, and at 2K it is hard to draw firm con-
Methodology. To create synthetic news, we fine-           clusion for llama-2-7b_it and mistral_it because
tune the following recent models: llama2-7b,              their performance is generally low. This is with a
llama2-13b (Touvron et al., 2023b) and Mistral-7b         multilingual classifier base; for RoBERTa-based
(Jiang et al., 2023) on the full CHANGE-it training       classifier, the mixed setting is consistently harder
set (see App. B.2 for the fine-tuning details). We        in all settings (see App. B.3).
refer to the resulting fine-tuned models as llama-2-
7b_it, llama-2-13b_it, and mistral_it.                    6     Detecting CFMs with Proxy Models
   For each of these models, we create a suite of         6.1    How Much Fine-tuning Do We Need?
datasets with training sets composed of 2K, 4K or         So far we only considered the scenarios where the
8K samples. In all settings, the test sets comprise       model generating synthetic texts is the same that
2K samples, namely 1K texts from the CHANGE-it            computes the likelihood used to detect them. Let
test set and 1K synthetic news with the same titles.      us now consider an alternative: a proxy model ap-
The training sets are built in two ways. In in domain     proximating the likelihood scores of the CFM. This
setting, 50% texts are synthetic, and 50% are arti-       could be expected to work if the proxy model and
cles sourced from CHANGE-it. In mixed source,             the CFM were fine-tuned on the same dataset. But
the human-authored articles come from two differ-         that assumption is also too strong to be practical.
ent datasets, 25% each (CHANGE-it and DICE).                 We explore relaxing it further to the scenario
Mixed source is closer to the scenario where we do        where we only have access to a small set of texts
not know what dataset was used to fine-tune the           similar to the fine-tuned model outputs. This could
CFM, and sample from a wide range of possible             be a small subset of the fine-tuning dataset or, more
news articles. The more diverse this set of non-          generally, samples from a similar distribution (e.g.
synthetic examples, the harder the classification         different samples from a given newspaper or a
task will probably become.                                social media account). We ask whether this is
  Similarly to Wang et al. (2024b), we experiment         enough: can we train a model on a small set
with two classifiers, based on RoBERTa (Liu et al.,       of in-distribution texts, so that the likelihood it
2019) and XLM-RoBERTa (Conneau et al., 2020).             assigns to tokens is sufficient to detect texts from
The former is pre-trained on English and the latter       a fully fine-tuned CFM?
                                                     15317
                         Detector model                       Generator model
                                            llama-2-13b_it      llama-2-7b_it      mistral_it
                                            dGPT      llh      dGPT       llh    dGPT       llh
                             llama-2-13b    0.73     0.61      0.54      0.40    0.56      0.43
                    llama-2-13b_it_3981     0.84     0.69      0.53      0.35    0.56      0.42
                    llama-2-13b_it_7862     0.85     0.70      0.53      0.34    0.56      0.41
                          llama-2-13b_it    0.87     0.70      0.48      0.27    0.55      0.39
                              llama-2-7b    0.58     0.49      0.75      0.59    0.57      0.46
                     llama-2-7b_it_3981     0.63     0.48      0.86      0.67    0.60      0.45
                     llama-2-7b_it_7862     0.63     0.47      0.87      0.68    0.60      0.44
                           llama-2-7b_it    0.62     0.44      0.88      0.66    0.61      0.44
                                  mistral   0.54     0.46      0.52      0.40    0.68      0.54
                         mistral_it_3981    0.54     0.42      0.48      0.34    0.80      0.65
                         mistral_it_7862    0.54     0.41      0.47      0.32    0.81      0.67
                               mistral_it   0.44     0.29      0.35      0.20    0.94      0.85

Table 2: The AUROC achieved by all the models (rows) at different levels of fine-tuning, from pretrained only to
fine-tuned on the full dataset. In all settings, the AUROC for models fine-tuned on 3981 and 7861 samples is very
close to the results of the fully fine-tuned model. However, the best results are always on the diagonal cells, where
the detector and generator models are the same.


Methodology. To answer this question, we fine-               Results. Table 2 suggests that the answer to our
tune the three LLMs used in the supervised de-               research question is positive: a small subset of
tection experiment in §5.2 (namely llama-2-7b_it,            fine-tuning samples is indeed sufficient to de-
llama-2-13b_it and mistral_it) on varying subsets            tect a full fine-tuned model. A model fine-tuned
of the CHANGE-it dataset. We then use their likeli-          on only 3% of the fine-tuning dataset achieves be-
hood and DetectGPT score to detect synthetic text            tween 86.1% and 95.4% of the AUROC measured
from models fine-tuned on the full CHANGE-it                 for the fine-tuned one.
dataset, as described in §5.                                    However, this is only effective if the same LLM
                                                             is both the generator and the detector, see App.
   For that, we select 5000 samples from the                 G for the ROC curves in this case. Simply fine-
CHANGE-it test set, and for each sample, we                  tuning different LLMs does not make them similar
prompt all models with the title and initial tokens          enough to use one for detecting another. In the case
of the original article (see Appendix F for more             of mistral_it, it actually gets worse after fine-tuning
details). This results in 3 datasets with 10k samples        (we hypothesize that it could be due to differences
in each, 5k human written (from the CHANGE-it                in tokenization).
test set) and 5k synthetically generated news with              While this study focuses on the Italian news, in
the same titles, which can be used as a benchmark            App. E.2 we perform the same experiments on the
for the detection of synthetic news in Italian.              XSUM dataset in English, and come to equivalent
  Afterwards, we select two subsets of the                   conclusions: we can detect a fully fine-tuned model
CHANGE-it training dataset with 3981 and 7862                with a model that is fine-tuned on a small subset of
samples, respectively 3% and 6% times the origi-             the whole fine-tuning dataset.
nal fine-tuning dataset size. We fine-tune the same          6.2   Can Ensembling Help?
LLMs on both of these smaller training sets, see
App. B.2 for details on the fine-tuning procedure            As shown in Table 2, fine-tuning on few samples is
and Table 4 for a summary of the model naming.               sufficient to achieve strong AUROC both with log-
                                                             likelihood and DetectGPT on fine-tuned versions of
   Finally, for each of the three synthetic datasets         the same LLM – but detecting fine-tuned versions
generated with llama-2-7b_it, llama-2-13b_it and             of different LLMs is harder, and longer fine-tuning
mistral_it, we compute log-likelihood and Detect-            does not improve the performance of statistical
GPT score with all 12 models: 3 fine-tuned on the            detection methods. This makes the proxy model
full CHANGE-it dataset, 3 fine-tuned on 3981 sam-            approach impractical, since in the real world we
ples, 3 on 7862 samples, and the original LLMs               would not know which base LLM was used.
without any fine-tuning.                                        To address this limitation, a straightforward ap-
                                                       15318
    CHANGE-      Mode     llama-2-   llama-2-   mistral_it   is far from being solved (§6.2), and will only get
    it samples            7b_it      13b_it                  harder as more LLMs are published. The offending
                 max      0.75       0.74       0.92         CFM could also be a ‘closed’ model like GPT-4, to
    Full         mean     0.61       0.69       0.79
                 random   0.57       0.65       0.68
                                                             which we would never have white-box access.
                                                                Supervised approaches can be used, but, as we
                 max      0.62       0.84       0.62
    3981         mean     0.66       0.73       0.68         showed in §5.2, they rely on a relatively large12
                 random   0.63       0.63       0.64         dataset of texts that were manually identified as
                 max      0.58       0.83       0.68         CFM texts, and human-written texts to serve as
    7962         mean     0.65       0.73       0.69         ‘negative‘ examples, and it is difficult13 to get the
                 random   0.62       0.63       0.64
                                                             human-written samples right. It would take time,
Table 3: We experiment with ensembling the DetectGPT         expertise, and resources to develop such a dataset.
score measured by models with the same amount of fine-       And we might want to detect a CFM before it pub-
tuning (indicated in the first column). We devise three      lishes even 2K “news”. The synthetic examples
new scores: random is computed by randomly picking           could also come from multiple CFMs, making the
the DetectGPT score from one of the models, mean is          classification task even harder. It is telling that the
computed by taking the average value of all models and       classifier developed by OpenAI, presumably aim-
max by taking the highest value.
                                                             ing to detect only OpenAI models, was soon shut
                                                             down due to low accuracy (Kirchner et al., 2023).
proach would be ensembling the DetectGPT score,                 Concerning watermarking, in the CFM case, it
which different candidate LLMs assign to a given             is safe to assume that the deployers of such models
sample. If texts from a certain source consistently          would likely try to remove or obfuscate the water-
get a high AUROC, this would signal that they                marking, which is relatively easy to do by altering
are probably synthetic. This is reasonable on the            the generation strategy. And the public easy-to-use
assumption that the CFM is one of the recent high-           tools highlighting the statistical ‘evidence’ of the
performing open-source LLMs, and there are not               watermark14 could be used not only by those look-
too many of these. Still, to evaluate the potential of       ing to detect CFMs, but also the CFM operators, to
this approach we experiment with computing both              obscure the evidence.
the mean and max DetectGPT score among three                    We conclude that at the moment there are no
LLMs with the same fine-tuning, to understand if             practical options for detecting news ‘content farms’
this provides a score with higher AUROC.                     in the wild, and both the open-source LLM com-
   The results are shown in Table 3. Neither the             munity and providers of ‘closed’ LLMs need to
average nor the maximum DetectGPT score of-                  consider ways to address that. We are hopeful that
fer a simple solution, but in most cases, one of             some combination of centralized watermarking ef-
them yields a significantly higher AUROC than                fort and further development of detection methods
the random guess. We believe that this is overall            could provide a working solution in the future.
a promising direction for developing new statistic              Since the hardest problem is identifying the base
approaches based on mixing the likelihoods of sev-           LLM, one policy direction to consider would be
eral models, but, once again, it would be difficult          to (a) mandate watermarking, ideally built-into-
to scale to dozens of candidate LLMs.                        model-weights, as a pre-requisite for either com-
                                                             mercial deployment of LLMs or their open-source
7      Discussion: Are There Practical                       publication, (b) maintain a public watermark detec-
       Solutions to Synthetic Text Detection?                tion library, allowing to identify a candidate LLM
                                                             given a text sample. This would not be bullet-proof,
As described in §1, the ‘content farms’ for news are
already wide-spread, and it is in the public interest           12
                                                                   Verma et al. (2023) used 30k samples for English alone.
to identify such ‘outlets’, as soon as possible.                13
                                                                   As a binary classification task, the detection of synthetic
   One key problem is that we would not know                 texts from a particular CFM seems intrinsically very challeng-
                                                             ing, since ideally we would need the non-synthetic examples
which base LLMs were used, and we would not                  to accurately represent all possible non-synthetic sources, and
have access to their token likelihood information.           also to be matched with a comparable number of synthetic
This completely precludes using methods like De-             examples.
                                                                14
                                                                   E.g.     demo by Kirchenbauer et al. (2023) at
tectGPT (§5.1). Our proxy model approach (§6)                https://huggingface.co/spaces/tomg-group-umd/
could address the latter problem, but the former             lm-watermarking

                                                        15319
but it would raise both the costs of avoiding detec-       least for languages with a similar level of coverage
tion and the awareness of the problem in the NLP           in datasets used for training LLMs. More research
community.                                                 is needed to establish both the factors impacting
                                                           the success of such transfer, and better methods to
8    Conclusion                                            detect synthetic texts.
In this work we have shown how creating a ‘content             For the original Llama, according to Touvron
farm’ generative model for news-like text can be           et al. (2023a, p.2), it was exposed to Italian
easy, even though we started with a relatively old         Wikipedia in pre-training. Italian Wikipedia cur-
LLM and a language it was not originally meant             rently has about 500K articles.15 For other sources
for. After fine-tuning Llama 65B on only 40K               included in Llama, such as C4 (Raffel et al., 2020),
Italian news texts, native speakers of Italian have        we cannot exclude the possibility that there was
only ≈ 64% accuracy on the synthetic news text             some Italian – but deliberate effort was made to
detection task.                                            filter out non-English texts, and so we assume that
   We show that the current approaches to auto-            there was at least not much contamination. Other
matic text detection, based on token likelihood and        languages in Llama with about the same amount
supervised classification, outperform human raters         of Wikipedia data as Italian are Polish and Dutch
in the synthetic text detection, but they would all be     (≈ 500K articles). In the ≈ 400K range there are
impractical in the real world, since they require ac-      Spanish and Portuguese, and at about ≈ 300K –
cess to the token likelihood information or a large        Russian and Swedish. A future study could explore
training dataset. We further consider the proxy            how the amount of Wikipedia data, the amount of
model approach, and we find that it works well             fine-tuning data, and the typological distance from
even with little data for fine-tuning, but only if it is   English impact the success of the transfer.
known which base LLM was used. Our study high-                 It is of course also possible and likely that a
lights the urgency of further work on developing           CFM developer aiming for a specific language
model-agnostic methods of synthetic text detection.        would start with an LLM that is multilingual by
                                                           design, such as BLOOM (Scao et al., 2022) or
9    Acknowledgements                                      AYA (Aryabumi et al., 2024), and probably get
                                                           even better transfer.
We acknowledge the CINECA award under
the ISCRA initiative, for the availability of              Other methods of detecting synthetic text. In
high-performance computing resources and sup-              the scope of this paper, we experimented with two
port IsCb2_GELATINO (HP10CQRW2J) and                       statistical detection methods (based on likelihood
IsCb3_TRAVEL (HP10CY9V7K).                                 scores and supervised detection), but there are oth-
   This work was also partially supported by               ers, including more sophisticated likelihood based
FAIR (PE00000013) project under the NextGenera-            approaches (Su et al., 2023) that however share the
tionEU programme, partially by the PNRR project            same dependency on the likelihood of the original
ITSERR (CUP B53C22001770006) and partially                 models, and therefore the core limitations of the
by the Project PRIN 2022EPTPJ9 (WEMB –                     methods we experiment with. This does not invali-
“Word EMBeddings: From Cognitive Linguistics               date our conclusions and the general answer to our
to Language Engineering, and Back”), funded by             research question, but it could be expanded in the
the Italian Ministry of University and Research            future work.
(MUR).
   The authors’ opinions do not necessarily reflect        Limitations of the human evaluation. Our se-
those of the funding bodies.                               lection of human raters was based solely on Italian
                                                           as their native language. Future work could inves-
10    Limitations                                          tigate whether the results would differ across dif-
                                                           ferent occupations and education levels, and with
Generalizability to other languages. We
                                                           different kinds of synthetic and real articles.
present a case study on a single language, and do
not intend to claim that it is possible to generate           Our human evaluation protocol considers the
plausible-sounding text in any language, by                setting where the model is prompted with the first
fine-tuning a mostly-English model like Llama.                15
                                                               https://en.wikipedia.org/wiki/Wikipedia:
But our results suggest that it may be possible, at        Multilingual_statistics

                                                      15320
30 tokens of a real human-written article, because      of Service broadly prohibit “any harmful, illegal,
the model is not trained using the articles headlines   or abusive activity”, but it is not immediately clear
but just to generate news, to make the adaptation       which definitions for ‘harm’ and ‘legality’ must
from English to Italian simpler. Another scenario       be followed, and whether the news ‘content farms’
to be tested in future work is when the model is        websites are covered. The most directly relevant
prompted with headlines (authored by the content        clause currently16 seems to be representing “that
farm owner or auto-generated). That could affect        Output was human-generated when it was not”. We
the quality of the generated text or the ease of its    do not know how this is enforced, and how many
detection.                                              bad actors are successfully stopped with API-level
   Finally, our study focuses on the possibility to     controls – but clearly not all of them.17
create plausible-sounding news-like text that could
be used by “content farms”, rather than text created    11    Broader Impacts
for specific misinformation campaigns or to spread
                                                        Impact on society. This work aims to highlight
conspiracy theories. It is possible that, similarly
                                                        a potential problem for the information infrastruc-
to human-authored fake news, the human raters
                                                        ture of worldwide communities, that may currently
would be more likely to doubt the authenticity of
                                                        consider themselves safe from plausible-looking
the article when it had some big factual claims that
                                                        synthetic text due to the lack of high-quality mono-
were easy to check. This factor also remains to be
                                                        lingual models for their languages. We show that a
explored in future work.
                                                        relatively old Llama model, exposed only to Italian
   The best case scenario with a CFM is that the
                                                        Wikipedia and 40K news articles for fine-tuning,
users would soon realize that the site is fake, and
                                                        is sufficient for generating very plausible-looking
leave – but even in that case they would already
                                                        synthetic news in Italian, and there are no practical
have wasted time and resources, and potentially
                                                        solutions for detecting such text. We hope that this
increased their digital footprint because of tracking
                                                        work would spark similar investigations for other
on the CFM website. Further possible harms from
                                                        languages, and highlight the urgency of develop-
misinformation, manipulative targeted ads etc. are
                                                        ment of reliable and model-agnostic methods for
beyond the scope of this study, and will require a
                                                        detecting synthetic text.
more detailed investigation of various types of fac-
                                                           In particular, we hope to draw the attention to the
tually problematic content, deliberate attempts to
                                                        fact that at present, the most authoritative source of
introduce certain narratives, awareness and training
                                                        information about the extent of the problem with
of the users, etc.
                                                        the ‘content farm’ news websites seems to be the
Detection of API-based models. This study fo-           aforementioned NewsGuard reports (Sadeghi and
cused on the scenario where the ‘content farm’ used     Arvanitis, 2023; Sadeghi et al., 2024). They are
its own model, created by fine-tuning a publicly        based on extensive expert research and manually
available high-performing base LLM. It could of         vetting different news outlets, and are provided as
course also use an external API service, which          a paid service. Ideally, the society would be better
would make its task even easier technically.            informed about the scope of the problem18 , have
   Famously, GPT-2 (Radford et al., 2019) initially     a reliable public infrastructure for news resources
came with warnings about it being “too danger-          that come from real outlets with editorial respon-
ous to release”, precisely because of the danger of     sibility, and taking quick action on the misleading
synthetic ‘news’ (Wakefield, 2019). Section 7.4 in         16
                                                              https://openai.com/policies/terms-of-use,
the GPT-3 (Brown et al., 2020) report is dedicated      accessed on Feb 10 2023.
                                                           17
to synthetic news generation and the finding that             For example, Gizmodo identified a fake story about the
                                                        death of Joe Biden that started with “I’m sorry, I cannot com-
humans detect such 200-word GPT-3 texts in the          plete this prompt as it goes against OpenAI’s use case policy
52%-76% accuracy range. At that time, too, there        on generating misleading content. It is not ethical to fabri-
was coverage of the dangers of synthetic news (e.g.     cate news about the death of someone, especially someone as
                                                        prominent as a President.” (DeGeurin, 2023)
Mak, 2019; Knight, 2021), but no policies ensued.          18
                                                              The fact that number of such websites grew so quickly
   Now that OpenAI offers the most popular gener-       in the past year (from 49 to 840, see section 1) must mean
ative AI services, its proposed solution is its Terms   that they are sufficiently profitable. Hence, a large number
                                                        of people must be mislead at least to waste their time and
of Service, presumably enforced via constant moni-      resources on visiting a spammy website, and there are other
toring of the API use by all users. Its current Terms   possible harms (e.g. resulting from misinformation).

                                                   15321
AI-generated websites. The problem with the cur-             2023a. Counter Turing test (CT2): AI-generated text
rent wave of such ‘news’ originates in the field of          detection is not as easy as you may think - introducing
                                                             AI detectability index (ADI). In Proceedings of the
NLP, and we hope that our field can also contribute
                                                             2023 Conference on Empirical Methods in Natural
practical solutions to the problems of detecting syn-        Language Processing, pages 2206–2239, Singapore.
thetic texts and assisting with their reporting.             Association for Computational Linguistics.

Human and computational resources. This                   Souradip Chakraborty, Amrit Singh Bedi, Sicheng Zhu,
work is based on the publicly available models              Bang An, Dinesh Manocha, and Furong Huang.
                                                            2023b. On the possibilities of AI-generated text de-
(Radford et al., 2019; Touvron et al., 2023a,b; Raf-        tection.
fel et al., 2020; Sarti and Nissim, 2022; Jiang et al.,
2023) and resources (Narayan et al., 2018; Mattei         Alexis Conneau, Kartikay Khandelwal, Naman Goyal,
et al., 2020), and documents its emissions (App. H),        Vishrav Chaudhary, Guillaume Wenzek, Francisco
                                                            Guzmán, Edouard Grave, Myle Ott, Luke Zettle-
annotation procedure and compensation to the hu-            moyer, and Veselin Stoyanov. 2020. Unsupervised
man raters (§4). The code to reproduce our experi-          cross-lingual representation learning at scale. In Pro-
ments accompanies the submission will be publicly           ceedings of the 58th Annual Meeting of the Asso-
available with the publication of the paper.                ciation for Computational Linguistics, pages 8440–
                                                            8451, Online. Association for Computational Lin-
                                                            guistics.
References                                                Mack DeGeurin. 2023. No, Biden Isn’t Dead: AI Con-
                                                           tent Farms Are Pumping Out Fake Stories.
Viraat Aryabumi, John Dang, Dwarak Talupuru,
  Saurabh Dash, David Cairuz, Hangyu Lin, Bharat          Heather Desaire, Aleesa E. Chua, Min-Gyu Kim, and
  Venkitesh, Madeline Smith, Jon Ander Campos,              David Hua. 2023. Accurately detecting AI text when
  Yi Chern Tan, Kelly Marchisio, Max Bartolo, Se-           ChatGPT is told to write like a chemist. Cell Reports
  bastian Ruder, Acyr Locatelli, Julia Kreutzer, Nick       Physical Science, 4(11):101672.
  Frosst, Aidan Gomez, Phil Blunsom, Marzieh Fadaee,
  Ahmet Üstün, and Sara Hooker. 2024. Aya 23: Open        Mahdi Dhaini, Wessel Poelman, and Ege Erdogan. 2023.
  weight releases to further multilingual progress.         Detecting ChatGPT: A survey of the state of detecting
                                                            ChatGPT-generated text. In Proceedings of the 8th
Giovanni Bonisoli, Maria Pia di Buono, Laura Po, and       Student Research Workshop associated with the In-
  Federica Rollo. 2023. Dice: A dataset of italian          ternational Conference Recent Advances in Natural
  crime event news. In SIGIR ’23: The 46th Inter-          Language Processing, pages 1–12, Varna, Bulgaria.
  national ACM SIGIR Conference on Research and             INCOMA Ltd., Shoumen, Bulgaria.
  Development in Information Retrieval, Taipei, Tai-
  wan, July 23 - 27, 2023. ACM.                           Liam Dugan, Alyssa Hwang, Filip Trhlik, Josh Mag-
                                                            nus Ludan, Andrew Zhu, Hainiu Xu, Daphne Ip-
Jack Brewster, Macrina Wang, and Coalter Palmer. 2023.      polito, and Chris Callison-Burch. 2024. Raid: A
   Plagiarism-Bot? How Low-Quality Websites Are Us-         shared benchmark for robust evaluation of machine-
   ing AI to Deceptively Rewrite Content from Main-         generated text detectors.
   stream News Outlets - Misinformation Monitor: Au-
   gust 2023.                                             Pierre Fernandez, Antoine Chaffin, Karim Tit, Vivien
                                                             Chappelier, and Teddy Furon. 2023. Three Bricks to
Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie             Consolidate Watermarks for Large Language Models.
  Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind           In 2023 IEEE International Workshop on Information
  Neelakantan, Pranav Shyam, Girish Sastry, Amanda          Forensics and Security (WIFS), pages 1–6.
  Askell, Sandhini Agarwal, Ariel Herbert-Voss,
  Gretchen Krueger, Tom Henighan, Rewon Child,            J.L. Fleiss et al. 1971. Measuring nominal scale agree-
  Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu,              ment among many raters. Psychological Bulletin,
  Clemens Winter, Christopher Hesse, Mark Chen, Eric         76(5):378–382.
  Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess,
  Jack Clark, Christopher Berner, Sam McCandlish,         Sebastian Gehrmann, Hendrik Strobelt, and Alexander
  Alec Radford, Ilya Sutskever, and Dario Amodei.           Rush. 2019. GLTR: Statistical detection and visual-
  2020. Language models are few-shot learners. In Ad-       ization of generated text. In Proceedings of the 57th
  vances in Neural Information Processing Systems 33:       Annual Meeting of the Association for Computational
  Annual Conference on Neural Information Process-          Linguistics: System Demonstrations, pages 111–116,
  ing Systems 2020, NeurIPS 2020, December 6-12,            Florence, Italy. Association for Computational Lin-
  2020, virtual.                                            guistics.
Megha Chakraborty, S.M Towhidul Islam Tonmoy,             Soumya Suvra Ghosal, Souradip Chakraborty, Jonas
 S M Mehedi Zaman, Shreya Gautam, Tanay Kumar,              Geiping, Furong Huang, Dinesh Manocha, and Amrit
 Krish Sharma, Niyar Barman, Chandan Gupta, Vinija          Bedi. 2023. A survey on the possibilities & impossi-
 Jain, Aman Chadha, Amit Sheth, and Amitava Das.            bilities of AI-generated text detection. Transactions
                                                     15322
  on Machine Learning Research. Survey Certifica-         Peixuan Li, Pengzhou Cheng, Fangqi Li, Wei Du,
  tion.                                                     Haodong Zhao, and Gongshen Liu. 2023. PLM-
                                                            mark: A Secure and Robust Black-Box Watermark-
Biyang Guo, Xin Zhang, Ziyuan Wang, Minqi Jiang, Jin-       ing Framework for Pre-trained Language Models.
  ran Nie, Yuxuan Ding, Jianwei Yue, and Yupeng Wu.         Proceedings of the AAAI Conference on Artificial
  2023. How Close is ChatGPT to Human Experts?              Intelligence, 37(12):14991–14999.
  Comparison Corpus, Evaluation, and Detection.
                                                          Wenxiong Liao, Zhengliang Liu, Haixing Dai,
Abhimanyu Hans, Avi Schwarzschild, Valeriia                Shaochen Xu, Zihao Wu, Yiyang Zhang, Xiaoke
  Cherepanova, Hamid Kazemi, Aniruddha Saha,               Huang, Dajiang Zhu, Hongmin Cai, Quanzheng Li,
  Micah Goldblum, Jonas Geiping, and Tom Goldstein.        Tianming Liu, and Xiang Li. 2023. Differentiating
  2024. Spotting llms with binoculars: Zero-shot           ChatGPT-Generated and Human-Written Medical
  detection of machine-generated text.                     Texts: Quantitative Study. JMIR Medical Education,
                                                           9:e48904.
Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, and
  Yejin Choi. 2020. The curious case of neural text       Yikang Liu, Ziyin Zhang, Wanyang Zhang, Shisen Yue,
  degeneration. In 8th International Conference on          Xiaojing Zhao, Xinyuan Cheng, Yiwen Zhang, and
  Learning Representations, ICLR 2020, Addis Ababa,         Hai Hu. 2023. ArguGPT: Evaluating, understanding
  Ethiopia, April 26-30, 2020. OpenReview.net.              and identifying argumentative essays generated by
                                                            GPT models.
Ganesh Jawahar, Muhammad Abdul-Mageed, and Laks
  Lakshmanan, V.S. 2020. Automatic detection of ma-       Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Man-
  chine generated text: A critical survey. In Proceed-      dar Joshi, Danqi Chen, Omer Levy, Mike Lewis,
  ings of the 28th International Conference on Com-         Luke Zettlemoyer, and Veselin Stoyanov. 2019.
  putational Linguistics, pages 2296–2309, Barcelona,       Roberta: A robustly optimized bert pretraining ap-
  Spain (Online). International Committee on Compu-         proach.
  tational Linguistics.
                                                          Sasha Luccioni, Victor Schmidt, Alexandre Lacoste,
Albert Q. Jiang, Alexandre Sablayrolles, Arthur Men-
                                                            and Thomas Dandres. 2019. Quantifying the carbon
  sch, Chris Bamford, Devendra Singh Chaplot, Diego
                                                            emissions of machine learning. In NeurIPS 2019
  de las Casas, Florian Bressand, Gianna Lengyel, Guil-
                                                            Workshop on Tackling Climate Change with Machine
  laume Lample, Lucile Saulnier, Lélio Renard Lavaud,
                                                            Learning.
  Marie-Anne Lachaux, Pierre Stock, Teven Le Scao,
  Thibaut Lavril, Thomas Wang, Timothée Lacroix,
                                                          Dominik Macko, Robert Moro, Adaku Uchendu, Ja-
  and William El Sayed. 2023. Mistral 7b.
                                                            son Lucas, Michiharu Yamashita, Matúš Pikuliak,
John Kirchenbauer, Jonas Geiping, Yuxin Wen,                Ivan Srba, Thai Le, Dongwon Lee, Jakub Simko, and
  Jonathan Katz, Ian Miers, and Tom Goldstein. 2023.        Maria Bielikova. 2023. MULTITuDE: Large-scale
  A watermark for large language models. In Proceed-        multilingual machine-generated text detection bench-
  ings of the 40th International Conference on Machine      mark. In Proceedings of the 2023 Conference on
  Learning, volume 202 of Proceedings of Machine            Empirical Methods in Natural Language Processing,
  Learning Research, pages 17061–17084. PMLR.               pages 9960–9987, Singapore. Association for Com-
                                                            putational Linguistics.
John Kirchenbauer, Jonas Geiping, Yuxin Wen, Manli
  Shu, Khalid Saifullah, Kezhi Kong, Kasun Fernando,      Aaron Mak. 2019. When Is Technology Too Dangerous
  Aniruddha Saha, Micah Goldblum, and Tom Gold-             to Release to the Public? Slate.
  stein. 2024. On the reliability of watermarks for
  large language models. In The Twelfth International     Lorenzo De Mattei, Michele Cafagna, Felice
  Conference on Learning Representations.                   Dell’Orletta, Malvina Nissim, and Albert Gatt.
                                                            2020. CHANGE-IT @ EVALITA 2020: Change
Jan Hendrik Kirchner, Lama Ahmad, Scott Aaronson,           headlines, adapt news, generate (short paper). In
  and Jan Leike. 2023. New AI classifier for indicating     Proceedings of the Seventh Evaluation Campaign
  AI-written text.                                          of Natural Language Processing and Speech Tools
                                                            for Italian. Final Workshop (EVALITA 2020), Online
Will Knight. 2021. AI Can Write Disinformation              event, December 17th, 2020, volume 2765 of CEUR
  Now—and Dupe Human Readers. Wired.                        Workshop Proceedings. CEUR-WS.org.

Rohith Kuditipudi, John Thickstun, Tatsunori              Niloofar Mireshghallah, Justus Mattern, Sicun Gao,
  Hashimoto, and Percy Liang. 2024.        Robust           Reza Shokri, and Taylor Berg-Kirkpatrick. 2024.
  distortion-free watermarks for language models.           Smaller language models are better zero-shot
  Transactions on Machine Learning Research.                machine-generated text detectors. In Proceedings
                                                            of the 18th Conference of the European Chapter of
J. Richard Landis and Gary G. Koch. 1977. The mea-          the Association for Computational Linguistics (Vol-
   surement of observer agreement for categorical data.     ume 2: Short Papers), pages 278–293, St. Julian’s,
   biometrics, pages 159–174.                               Malta. Association for Computational Linguistics.
                                                     15323
Eric Mitchell, Yoonho Lee, Alexander Khazatsky,             Teven Le Scao, Angela Fan, Christopher Akiki, El-
  Christopher D. Manning, and Chelsea Finn. 2023.             lie Pavlick, Suzana Ilić, Daniel Hesslow, Roman
  Detectgpt: zero-shot machine-generated text detec-          Castagné, Alexandra Sasha Luccioni, François Yvon,
  tion using probability curvature. In Proceedings of         Matthias Gallé, Jonathan Tow, Alexander M. Rush,
  the 40th International Conference on Machine Learn-         Stella Biderman, Albert Webson, Pawan Sasanka Am-
  ing, ICML’23. JMLR.org.                                     manamanchi, Thomas Wang, Benoît Sagot, Niklas
                                                              Muennighoff, Albert Villanova del Moral, Olatunji
Sandra Mitrović, Davide Andreoletti, and Omran Ayoub.        Ruwase, Rachel Bawden, Stas Bekman, Angelina
  2023. ChatGPT or Human? Detect and Explain.                 McMillan-Major, Iz Beltagy, Huu Nguyen, Lucile
  Explaining Decisions of Machine Learning Model              Saulnier, Samson Tan, Pedro Ortiz Suarez, Vic-
  for Detecting Short ChatGPT-generated Text.                 tor Sanh, Hugo Laurençon, Yacine Jernite, Julien
                                                              Launay, Margaret Mitchell, Colin Raffel, Aaron
Shashi Narayan, Shay B. Cohen, and Mirella Lapata.            Gokaslan, Adi Simhi, Aitor Soroa, Alham Fikri
  2018. Don’t give me the details, just the summary!          Aji, Amit Alfassy, Anna Rogers, Ariel Kreisberg
  topic-aware convolutional neural networks for ex-           Nitzav, Canwen Xu, Chenghao Mou, Chris Emezue,
  treme summarization. In Proceedings of the 2018             Christopher Klamm, Colin Leong, Daniel van Strien,
  Conference on Empirical Methods in Natural Lan-             David Ifeoluwa Adelani, Dragomir Radev, Ed-
  guage Processing, pages 1797–1807, Brussels, Bel-           uardo González Ponferrada, Efrat Levkovizh, Ethan
  gium. Association for Computational Linguistics.            Kim, Eyal Bar Natan, Francesco De Toni, Gérard
                                                              Dupont, Germán Kruszewski, Giada Pistilli, Hady
OpenAI. 2022. Introducing ChatGPT.
                                                              Elsahar, Hamza Benyamina, Hieu Tran, Ian Yu, Idris
OpenAI. 2023. GPT-4 Technical Report.                         Abdulmumin, Isaac Johnson, Itziar Gonzalez-Dios,
                                                              Javier de la Rosa, Jenny Chim, Jesse Dodge, Jian Zhu,
Alec Radford, Jeffrey Wu, Rewon Child, David Luan,            Jonathan Chang, Jörg Frohberg, Joseph Tobing, Joy-
  Dario Amodei, and Ilya Sutskever. 2019. Language            deep Bhattacharjee, Khalid Almubarak, Kimbo Chen,
  models are unsupervised multitask learners. Techni-         Kyle Lo, Leandro Von Werra, Leon Weber, Long
  cal report.                                                 Phan, Loubna Ben allal, Ludovic Tanguy, Manan
                                                              Dey, Manuel Romero Muñoz, Maraim Masoud,
Colin Raffel, Noam Shazeer, Adam Roberts, Katherine           María Grandury, Mario Šaško, Max Huang, Max-
  Lee, Sharan Narang, Michael Matena, Yanqi Zhou,             imin Coavoux, Mayank Singh, Mike Tian-Jian Jiang,
  Wei Li, and Peter J. Liu. 2020. Exploring the limits        Minh Chien Vu, Mohammad A. Jauhar, Mustafa
  of transfer learning with a unified text-to-text trans-     Ghaleb, Nishant Subramani, Nora Kassner, Nuru-
  former. J. Mach. Learn. Res., 21:140:1–140:67.              laqilla Khamis, Olivier Nguyen, Omar Espejel, Ona
                                                              de Gibert, Paulo Villegas, Peter Henderson, Pierre
Tate Ryan-Mosley. 2023. Junk websites filled with AI-         Colombo, Priscilla Amuok, Quentin Lhoest, Rheza
  generated text are pulling in money from program-           Harliman, Rishi Bommasani, Roberto Luis López,
  matic ads. MIT Technology Review.                           Rui Ribeiro, Salomey Osei, Sampo Pyysalo, Se-
                                                              bastian Nagel, Shamik Bose, Shamsuddeen Hassan
Vinu Sankar Sadasivan, Aounon Kumar, Sriram Bala-             Muhammad, Shanya Sharma, Shayne Longpre, So-
  subramanian, Wenxiao Wang, and Soheil Feizi. 2023.          maieh Nikpoor, Stanislav Silberberg, Suhas Pai, Syd-
  Can AI-generated text be reliably detected?                 ney Zink, Tiago Timponi Torrent, Timo Schick, Tris-
McKenzie Sadeghi and Lorenzo Arvanitis. 2023. Rise            tan Thrush, Valentin Danchev, Vassilina Nikoulina,
 of the Newsbots: AI-Generated News Websites Pro-             Veronika Laippala, Violette Lepercq, Vrinda Prabhu,
 liferating Online.                                           Zaid Alyafeai, Zeerak Talat, Arun Raja, Benjamin
                                                              Heinzerling, Chenglei Si, Davut Emre Taşar, Eliz-
McKenzie Sadeghi, Lorenzo Arvanitis, Virginia                 abeth Salesky, Sabrina J. Mielke, Wilson Y. Lee,
 Padovese, Giulia Pozzy, Sara Badilini, Chiara Vercel-        Abheesht Sharma, Andrea Santilli, Antoine Chaffin,
 lone, Madeline Roache, Macrina Wang, Jack Brew-              Arnaud Stiegler, Debajyoti Datta, Eliza Szczechla,
 ster, Natalie Huet, Becca Schimmel, Andie Slomka,            Gunjan Chhablani, Han Wang, Harshit Pandey, Hen-
 Leonie Pfaller, Louise Vallee, and Natalie Adams.            drik Strobelt, Jason Alan Fries, Jos Rozen, Leo
 2024. Tracking AI-enabled Misinformation: Over               Gao, Lintang Sutawika, M. Saiful Bari, Maged S.
 650 ‘Unreliable AI-Generated News’ Websites (and             Al-shaibani, Matteo Manica, Nihal Nayak, Ryan
 Counting), Plus the Top False Narratives Generated           Teehan, Samuel Albanie, Sheng Shen, Srulik Ben-
 by Artificial Intelligence Tools.                            David, Stephen H. Bach, Taewoon Kim, Tali Bers,
                                                              Thibault Fevry, Trishala Neeraj, Urmish Thakker,
Siddharth Samsi, Dan Zhao, Joseph McDonald, Baolin            Vikas Raunak, Xiangru Tang, Zheng-Xin Yong,
   Li, Adam Michaleas, Michael Jones, William Berg-           Zhiqing Sun, Shaked Brody, Yallow Uri, Hadar
   eron, Jeremy Kepner, Devesh Tiwari, and Vijay Gade-        Tojarieh, Adam Roberts, Hyung Won Chung, Jae-
   pally. 2023. From words to watts: Benchmarking the         sung Tae, Jason Phang, Ofir Press, Conglong Li,
   energy costs of large language model inference.            Deepak Narayanan, Hatim Bourfoune, Jared Casper,
                                                              Jeff Rasley, Max Ryabinin, Mayank Mishra, Minjia
Gabriele Sarti and Malvina Nissim. 2022. It5: Large-          Zhang, Mohammad Shoeybi, Myriam Peyrounette,
  scale text-to-text pretraining for italian language un-     Nicolas Patry, Nouamane Tazi, Omar Sanseviero,
  derstanding and generation.
                                                       15324
Patrick von Platen, Pierre Cornette, Pierre François      nis Labrak, Yash Shailesh Bajaj, Yash Venkatraman,
Lavallée, Rémi Lacroix, Samyam Rajbhandari, San-          Yifan Xu, Yingxin Xu, Yu Xu, Zhe Tan, Zhongli
chit Gandhi, Shaden Smith, Stéphane Requena, Suraj        Xie, Zifan Ye, Mathilde Bras, Younes Belkada, and
Patil, Tim Dettmers, Ahmed Baruwa, Amanpreet              Thomas Wolf. 2022. BLOOM: A 176B-Parameter
Singh, Anastasia Cheveleva, Anne-Laure Ligozat,           Open-Access Multilingual Language Model.
Arjun Subramonian, Aurélie Névéol, Charles Lover-
ing, Dan Garrette, Deepak Tunuguntla, Ehud Reiter,     Jinyan Su, Terry Zhuo, Di Wang, and Preslav Nakov.
Ekaterina Taktasheva, Ekaterina Voloshina, Eli Bog-       2023. DetectLLM: Leveraging log rank information
danov, Genta Indra Winata, Hailey Schoelkopf, Jan-        for zero-shot detection of machine-generated text.
Christoph Kalo, Jekaterina Novikova, Jessica Zosa         In Findings of the Association for Computational
Forde, Jordan Clive, Jungo Kasai, Ken Kawamura,           Linguistics: EMNLP 2023, pages 12395–12412, Sin-
Liam Hazan, Marine Carpuat, Miruna Clinciu, Na-           gapore. Association for Computational Linguistics.
joung Kim, Newton Cheng, Oleg Serikov, Omer
                                                       Yuki Takezawa, Ryoma Sato, Han Bao, Kenta Niwa,
Antverg, Oskar van der Wal, Rui Zhang, Ruochen
                                                         and Makoto Yamada. 2023. Necessary and Sufficient
Zhang, Sebastian Gehrmann, Shachar Mirkin, Shani
                                                         Watermark for Large Language Models.
Pais, Tatiana Shavrina, Thomas Scialom, Tian Yun,
Tomasz Limisiewicz, Verena Rieser, Vitaly Protasov,    Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier
Vladislav Mikhailov, Yada Pruksachatkun, Yonatan         Martinet, Marie-Anne Lachaux, Timothée Lacroix,
Belinkov, Zachary Bamberger, Zdeněk Kasner, Al-         Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal
ice Rueda, Amanda Pestana, Amir Feizpour, Am-            Azhar, Aurelien Rodriguez, Armand Joulin, Edouard
mar Khan, Amy Faranak, Ana Santos, Anthony               Grave, and Guillaume Lample. 2023a. Llama: Open
Hevia, Antigona Unldreaj, Arash Aghagol, Are-            and efficient foundation language models.
zoo Abdollahi, Aycha Tammour, Azadeh HajiHos-
seini, Bahareh Behroozi, Benjamin Ajibade, Bharat      Hugo Touvron, Louis Martin, Kevin Stone, Peter Al-
Saxena, Carlos Muñoz Ferrandis, Danish Contrac-          bert, Amjad Almahairi, Yasmine Babaei, Nikolay
tor, David Lansky, Davis David, Douwe Kiela,             Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti
Duong A. Nguyen, Edward Tan, Emi Baylor, Ez-             Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton
inwanne Ozoani, Fatima Mirza, Frankline Onon-            Ferrer, Moya Chen, Guillem Cucurull, David Esiobu,
iwu, Habib Rezanejad, Hessie Jones, Indrani Bhat-        Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller,
tacharya, Irene Solaiman, Irina Sedenko, Isar Ne-        Cynthia Gao, Vedanuj Goswami, Naman Goyal, An-
jadgholi, Jesse Passmore, Josh Seltzer, Julio Bonis      thony Hartshorn, Saghar Hosseini, Rui Hou, Hakan
Sanz, Livia Dutra, Mairon Samagaio, Maraim El-           Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa,
badri, Margot Mieskes, Marissa Gerchick, Martha          Isabel Kloumann, Artem Korenev, Punit Singh Koura,
Akinlolu, Michael McKenna, Mike Qiu, Muhammed            Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Di-
Ghauri, Mykola Burynok, Nafis Abrar, Nazneen Ra-         ana Liskovich, Yinghai Lu, Yuning Mao, Xavier Mar-
jani, Nour Elkott, Nour Fahmy, Olanrewaju Samuel,        tinet, Todor Mihaylov, Pushkar Mishra, Igor Moly-
Ran An, Rasmus Kromann, Ryan Hao, Samira Al-             bog, Yixin Nie, Andrew Poulton, Jeremy Reizen-
izadeh, Sarmad Shubber, Silas Wang, Sourav Roy,          stein, Rashi Rungta, Kalyan Saladi, Alan Schelten,
Sylvain Viguier, Thanh Le, Tobi Oyebade, Trieu Le,       Ruan Silva, Eric Michael Smith, Ranjan Subrama-
Yoyo Yang, Zach Nguyen, Abhinav Ramesh Kashyap,          nian, Xiaoqing Ellen Tan, Binh Tang, Ross Tay-
Alfredo Palasciano, Alison Callahan, Anima Shukla,       lor, Adina Williams, Jian Xiang Kuan, Puxin Xu,
Antonio Miranda-Escalada, Ayush Singh, Benjamin          Zheng Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan,
Beilharz, Bo Wang, Caio Brito, Chenxi Zhou, Chirag       Melanie Kambadur, Sharan Narang, Aurelien Ro-
Jain, Chuxin Xu, Clémentine Fourrier, Daniel León        driguez, Robert Stojnic, Sergey Edunov, and Thomas
Periñán, Daniel Molano, Dian Yu, Enrique Manjava-        Scialom. 2023b. Llama 2: Open foundation and
cas, Fabio Barth, Florian Fuhrimann, Gabriel Altay,      fine-tuned chat models.
Giyaseddin Bayrak, Gully Burns, Helena U. Vrabec,
Imane Bello, Ishani Dash, Jihyun Kang, John Giorgi,    Chris van der Lee, Albert Gatt, Emiel van Miltenburg,
Jonas Golde, Jose David Posada, Karthik Ranga-           and Emiel Krahmer. 2021. Human evaluation of
sai Sivaraman, Lokesh Bulchandani, Lu Liu, Luisa         automatically generated text: Current trends and best
Shinzato, Madeleine Hahn de Bykhovetz, Maiko             practice guidelines. Computer Speech & Language,
Takeuchi, Marc Pàmies, Maria A. Castillo, Mari-          67:101151.
anna Nezhurina, Mario Sänger, Matthias Samwald,
                                                       Christoforos Vasilatos, Manaar Alam, Talal Rah-
Michael Cullan, Michael Weinberg, Michiel De Wolf,
                                                         wan, Yasir Zaki, and Michail Maniatakos. 2023.
Mina Mihaljcic, Minna Liu, Moritz Freidank, Myung-
                                                         HowkGPT: Investigating the Detection of ChatGPT-
sun Kang, Natasha Seelam, Nathan Dahlberg,
                                                         generated University Student Homework through
Nicholas Michio Broad, Nikolaus Muellner, Pascale
                                                         Context-Aware Perplexity Analysis.
Fung, Patrick Haller, Ramya Chandrasekhar, Renata
Eisenberg, Robert Martin, Rodrigo Canalli, Rosaline    Vivek Verma, Eve Fleisig, Nicholas Tomlin, and Dan
Su, Ruisi Su, Samuel Cahyawijaya, Samuele Garda,         Klein. 2023. Ghostbuster: Detecting text ghostwrit-
Shlok S. Deshmukh, Shubhanshu Mishra, Sid Ki-            ten by large language models.
blawi, Simon Ott, Sinee Sang-aroonsiri, Srishti Ku-
mar, Stefan Schweter, Sushil Bharati, Tanmay Laud,     Jane Wakefield. 2019. ’Dangerous’ AI offers to write
Théo Gigant, Tomoya Kainuma, Wojciech Kusa, Ya-          fake news. BBC News.
                                                  15325
Yuxia Wang, Jonibek Mansurov, Petar Ivanov, Jinyan
  Su, Artem Shelmanov, Akim Tsvigun, Osama Mo-
  hanned Afzal, Tarek Mahmoud, Giovanni Puccetti,
  Thomas Arnold, Alham Fikri Aji, Nizar Habash,
  Iryna Gurevych, and Preslav Nakov. 2024a. M4gt-
  bench: Evaluation benchmark for black-box machine-
  generated text detection.
Yuxia Wang, Jonibek Mansurov, Petar Ivanov, Jinyan
  Su, Artem Shelmanov, Akim Tsvigun, Chenxi White-
  house, Osama Mohammed Afzal, Tarek Mahmoud,
  Toru Sasaki, Thomas Arnold, Alham Aji, Nizar
  Habash, Iryna Gurevych, and Preslav Nakov. 2024b.
  M4: Multi-generator, multi-domain, and multi-
  lingual black-box machine-generated text detection.
  In Proceedings of the 18th Conference of the Euro-
  pean Chapter of the Association for Computational
  Linguistics (Volume 1: Long Papers), pages 1369–
  1407, St. Julian’s, Malta. Association for Computa-
  tional Linguistics.
Yihan Wu, Zhengmian Hu, Hongyang Zhang, and Heng
  Huang. 2023. DiPmark: A Stealthy, Efficient and
  Resilient Watermark for Large Language Models.
KiYoon Yoo, Wonhyuk Ahn, and Nojun Kwak. 2023.
  Advancing Beyond Identification: Multi-bit Water-
  mark for Large Language Models.




                                                   15326
    pretrained                         CHANGE-it fine-tuning samples                             HuggingFace model
                       3,981               7,862                40,000           127,392
    llama-1-7b            -                     -             llama-7b_it           -           huggyllama/llama-7b
 llama-1-65b              -                     -            llamam-65b_it          -           huggyllama/llama-65b
  llama-2-7b      llama-2-7b_it_3981    llama-2-7b_it_7862         -           llama-2-7b_it   meta-llama/Llama-2-7b
 llama-2-13b     llama-2-13b_it_3981   llama-2-13b_it_7862         -          llama-2-13b_it   meta-llama/Llama-2-13b
     mistral         mistral_it_3981       mistral_it_7862                        mistral_it   meta-llama/Llama-2-70b

Table 4: Model naming based on pretrained model and number of fine-tuning samples. The fine-tuning samples
number refers to the training set of CHANGE-it (Mattei et al., 2020) dataset. HuggingFace model names correspond
to the current links on HuggingFace hub (e.g. for meta-llama/Llama-2-7b the pre-trained model comes from
https://huggingface.co/meta-llama/Llama-2-7b).


A      Model Sources and Naming Scheme
All LLMs used in this study are listed in Table 4.
We also add name of the models in Huggingface-
Hub, e.g. for meta-llama/Llama-2-7b the pre-
trained model comes from https://huggingface.
co/meta-llama/Llama-2-7b.

B      Fine-tuning Details
B.1     Llama 1
We fine-tune both Llama 7b and 65b models on a
randomly chosen 40K subset of the CHANGE-it
news dataset. The articles are arranged in training
sequences composed of 128 tokens, adding subse-
                                                             Figure 5: Accuracy of classifier based on RoBERTa-
quent segments one after the other.
                                                             large for human/synthetic text classification task, for
   The training was performed on 8 nodes, each               synthetic texts generated by three LLMs fine-tuned on
with 4 V100 GPUs with 16GB VRAM. The effec-                  CHANGE-it. The classifier was trained on 50% syn-
tive batch size is 128, real batch size 2, 64 accumu-        thetic texts and either 50% CHANGE-it texts (in do-
lation steps. The maximum learning rate is 0.0005,           main), or 25% texts from CHANGE-it and 25% from
with a one-cycle scheduler without warmup.                   DICE (mixed source). Classification is only successful
   Due to memory constraints, instead of the most            at at least 4K labeled samples, and the mixed source
                                                             scenario is consistently more challenging.
effective AdamW optimizer we use simple Stochas-
tic Gradient Descent. We train for 60,000 steps
(120,000 samples split into 3 epochs of 40,000)              needed and we perform full fine-tuning without
saving checkpoints every 10,000 steps (20,000 sam-           using any parameter efficient technique.
ples). This takes approximately 3 days.                         For the fine-tuning on subsets of the CHANGE-
                                                             it dataset we keep most things equal to the longer
B.2     Llama 2 and Mistral                                  training-set.
We fine-tune Llama 2 7b and 13b as well as Mistral              For the XSUM dataset the same setting is kept
models on the full training set of the CHANGE-it             almost identical.
news dataset. With a length up to 2048 tokens.
   The training is performed on 4 nodes, each with           B.3       Fine Tuning Supervised Synthetic Text
4 A100 GPUs with 64GB VRAM. The effective                              Detectors
batch size is 256, real batch size 4 with 4 accumu-          We fine-tune two classifiers to identify real or syn-
lation steps. The maximum learning rate is 1.e-5,            thetic texts, RoBERTa-large and XLM-RoBERTa-
with a one-cycle scheduler without warm-up.                  Large. The models are trained on three different
   We use AdamW optimizer with FSDP, we train                dataset size, 2k, 4k, 8k and two data mixing.
for three epochs in bfloat16 to limit the memory               The max learning rate is 5.e-5 we use the a batch
                                                        15327
 generator         n samples    roberta-large   xlm-large                     model          accuracy   std
                        In Domain                                        Llama 7B pretrain     85.3     6.1
                                                                         Llama 7B finetune     73.7     8.8
                      2000            0.52         0.73
 llama-2-13b_it       4000            0.77         0.81                 Llama 65B pretrain     72.6     3.9
                      8000            0.84         0.90                 Llama 65B finetune     65.3     16.9
                      2000            0.56         0.59
 llama-2-7b_it        4000            0.80         0.86        Table 6: Accuracy achieved by human raters in assess-
                      8000            0.87         0.92        ing human-written versus machine generated news. We
                      2000            0.51         0.52        report the overall accuracy and the standard deviation.
 mistral_it           4000            0.82         0.81
                      8000            0.88         0.84
                       Mixed Source                            D    Generation examples
                      2000            0.51         0.53        This appendix lists further examples of LLMs pre-
 llama-2-7b_it        4000            0.75         0.79
                      8000            0.81         0.88
                                                               trained mostly on English switching from English
                                                               to Italian when generating the text, as well as the
                      2000            0.50         0.61
 llama-2-13b_it       4000            0.78         0.86        same examples where our CFMs don’t do so. We
                      8000            0.80         0.90        show this for Llama 7b not-pretrained Table 8,
                      2000            0.50         0.55        Llama 7b fine-tuned Table 9, Llama 65b pre-trained
 mistral_it           4000            0.78         0.82        Table 10 and Llama 65b pre-trained Table 11. The
                      8000            0.77         0.83
                                                               captions also report a break down of the output
Table 5: Accuracy achieved by supervised classification
                                                               of the qualitative study we carried out, listing the
models when trained to classify real and synthetic text        amount and type of mistakes we spot.
generated by the various fine-tuned models. We report             Furthermore, Table 12 shows examples of the
the accuracy on in domain (where all synthetic texts are       changes done by it5 when generating the modifica-
generated from the same source) and on mixed source            tions necessary to compute the DetectGPT score.
data (where half of the human written texts come from          These modifications can sometimes lchange mean-
a different Italian news outlet). Our results suggest          ing in Italian, although when the modified spans
that supervised classification of synthetic texts critically
                                                               are only 1 or 2 words long they keep their original
depends on the availability of a large (at least 4K in
this case) labelled training set, particularly in the mixed    meaning.
source scenario.


size of 128 and a linear decaying learning rate with-
out warmup. The rest of the parameters are the
daults parameters used by Huggingface Trainer.
   The performance is reported in Figure 4 for
XLM-RoBERTa and Figure 5 for RoBERTa.
   The detailed numerical results are also listed in
Table 5.

C    Alternative Threshold for Human
     Evaluation Metric
To compute the readers accuracy on identifying
machine generated texts, we threshold the average
score assigned to a sample to obtain a binary label.
In §4 we show the results using 3 as a threshold,
which is the mean possible rating, but we find that
the results are similar when the threshold is the
scaled mean: the mean score of all questions in
a 100-question survey. Table 6 shows all results
with this threshold, and they are well aligned with
Table 1.
                                                            15328
 Models Switching to English
 Original Text: Due sbarchi in sole ventiquattr’ore a Lampedusa. Sono 84 gli immigrati giunti nell’isola tra
 venerdì e sabato e ospitati all’Hotspot di contrada Imbriacola. Tra loro ci sono anche I tre unici superstiti
 dell’ultimo naufragio avvenuto a 50 chilometri a nord est dalla Libia, costato la vita a 117 persone, che erano
 partite giovedì a bordo di un gommone sgonfiatosi a circa undici ore di navigazione. I passeggeri sono morti
 annegati, mentre I tre naufraghi sono riusciti a trovare un appiglio fino all’arrivo dei soccorsi italiani. I tre
 stranieri...

 Pre-trained Llama: Due sbarchi in sole ventiquattr’ore a Lampedusa. Sono 84 gli immigrati giunti nell’isola tra
 venerdì e sabato e ospitati all’Hotspot di contrada Imbriacola. Tra loro ci sono anche I tre naufraghi di Tortuga,
 recuperati da un mercantile libanese. Non è ancora stata resa nota l’identità nazionale dei naufraghi, ma non
 mancano inchieste di persone che si sono rivolte ai carabinieri per cercare i loro cari. Lampedusa, 38 migrants -
 mostly from Tunisia - arrived safely on the island ...

 Fine tuned epoch 6 Llama: Due sbarchi in sole ventiquattr’ore a Lampedusa. Sono 84 gli immigrati giunti
 nell’isola tra venerdì e sabato e ospitati all’Hotspot di contrada Imbriacola. Tra loro ci sono anche I tre bambini
 rimasti uccisi durante lo stesso sbarcho, due di questi non appartenevano a una famiglia, ma erano stati imbarcati
 separati dai genitori per il viaggio da Libia verso l’Italia. È stato appunto il maggiore Damiano Maiorino, di
 stanza a Lampedusa, a scoprire i morti. "Non sono morti cadendo in mare da una barca troppo affollata. Hanno
 subito commentato ...
 Field

 Original Text: L’ Onu è pronta a fare la sua parte alla conclusione del vertice europeo, ma il segretariato non ha
 in agenda alcuna azione militare, anche se ci possono essere alcune similarità con l’operazione in Somalia ". In
 una intervista a Qn il vicesegretario generale dell’Onu Jan Eliasson apre "all’uso della forza" per fermare gli
 sbarchi dei clandestini ed evitare nuove stragi nel Mediterraneo. Ma, al tempo stesso, sottolinea "una differenza
 qualitativa" con l’operazione in Somalia: "L’attività dei pirati era solo criminale, mentre in Libia abbiamo un
 urgentissimo problema umanitario prima che criminale". Parlando dell’affondamento preventivo dei barconi nei
 porti libici...

 Pre-trained Llama: L’ Onu è pronta a fare la sua parte alla conclusione del vertice europeo, ma il segretariato
 non ha in agenda alcuna azione militare, anche se ci possono essere alcune iniziative sul campo degli aiuti
 umanitari", ha affermato un portavoce dell’organizzazione internazionale. Per il segretario generale, "l’ Italia
 deve avere una posizione di leader ed essere la prima a proporre una risposta alla crisi europea, visto anche che l’
 Italia ha avuto un ruolo molto importante nei negoziati sul tema del contingente europeo". UNITED NATIONS,
 January 31 – Without waiting for the European Union’s decision on...

 Fine tuned epoch 6 Llama: L’ Onu è pronta a fare la sua parte alla conclusione del vertice europeo, ma il
 segretariato non ha in agenda alcuna azione militare, anche se ci possono essere alcune azioni umanitarie" . Così
 parla il portavoce dell’organizzazione internazionale, Stephane Dujarric, che aggiunge: "Un vertice europeo è
 una questione interna". La conferma che l’Onu non è pronta a seguito di una intervista rilasciata dal segretario
 generale aggiunto, Jeffrey Feltman, a radio 24. “Non abbiamo notizie di alcuna iniziativa che possa condurre
 all’attuazione di un mandato militare contro l’islamic State sul territorio siriano, anche se ritengo che si stia...

Table 7: Real and generated sentences in Italian from Llama 65B pretrained and Llama 65B fine-tuned on Italian
all starting from the same prompt. The sentences generated by Llama 65B pretrained are not detected by either
DetectGPT or log-likelihood, despite being partially written in English – which could not happen in a real Italian
news article.




                                                              15329
       Llama 7B Pre-Trained
       Generated Text: I dodici ragazzi rimasti intrappolati con il loro allenatore nella grotta di Tham Luang, nella
       provincia di Chiang Rai, in Thailandia, per oltre due settimane, hanno lasciato oggi l’ospedale dove
       erano ricoverati. La polizia ha riferito che i ragazzi sono stati sottoposti a un test del DNA che ha dimostrato che
       tutti erano discendenti di due genitori, ma non vi è nessuna prova che uno o più ragazzi non sia rimasto tra loro
       durante la fuga dalla grotta. Il...

       Translation: The 12 boys who were trapped with their coach in the Tham Luang cave in Thailand’s Chiang Rai
       province for more than two weeks left the hospital today where they were hospitalized. Police reported that the
       boys underwent a DNA test that showed that all were descendants of two parents, but there is no evidence that
       one or more of the boys did not remain among them while escaping the cave. The

       Issue type: Grammatical error.
       Original Text: Se dovesse darsi un voto, lei si darebbe un “sette e mezzo”. Sette romani su dieci, però, secondo
       un sondaggio di Repubblica, non le darebbero nemmeno la sufficienza. Ad un anno e mezzo dal suo insediamento,
       è la dimostrazione più esplicita del limpido disaccordo che la popolazione ha con la sua amministrazione. From
       the review of A. Kersalme’s “Odysseus” on the site of French journal “La Revue de Belles Lettres” (98th issue,
       March 2019). From the review of M....

       Translation: If she had to give herself a grade, she would give herself a "seven and a half." Seven out of ten
       Romans, however, would not even give her a sufficiency, according to a Repubblica poll. A year and a half
       after taking office, it is the most explicit demonstration of the limpid disagreement the population has with her
       administration. From the review of A. Kersalme’s "Odysseus" on the site of French journal "La Revue de Belles
       Lettres" (98th issue, March 2019). From the review of M....

       Issue type: Factual error.
       Generated Text: Passerà in carcere da un minimo di 42 anni fino all’ergastolo. Si è chiuso con la lettura di una
       sentenza durissima da parte del giudice della Superior Court di Los Angeles. La condanna dura fino al 2019, ma
       la rischia se si insulta o rinnega ancora una volta le sue azioni. Il procuratore generale della California, Kamala
       Harris, ha anche chiesto per lui la revoca di libertà condizionata. Il giovane è stato arrestato a Hong Kong nel
       maggio 2014....

       Translation: He will spend from a minimum of 42 years to life in prison. It ended with the reading of a very
       harsh sentence by the Los Angeles Superior Court judge. The sentence lasts until 2019, but he risks it if he
       insults or disavows his actions again. California Attorney General Kamala Harris also sought revocation of
       parole for him. The young man was arrested in Hong Kong in May 2014...

       Issue type: Grammatically correct, but does not sound natural in Italian and shows factual errors.

Table 8: Examples of mistakes made by pretrained Llama 7B. The smaller Llama 7b without fine-tuning shows
several kinds of weaknesses generating both factual to grammatical errors. Out of 25 samples manually examined
for this model, we find 0 contradicting the prompt, 5 switching to English, 8 unnatural Italian expressions and 6
grammatical errors.




                                                             15330
       Llama 7B Fine-Tuned
       Generated Text: Passa per sette punti il programma di Matteo Salvini per bloccare I flussi e dare maggiore
       sicurezza al Paese. Il blocco dei porti a navi che battono bandiera di uno stato membro dell’Unione europea e
       non il Regno Unito, come annunciato da Salvini, sarebbe contro il diritto e il trattato, secondo l’ex ministro
       della Giustizia Franco Frattini. "Vi è un’interpretazione di diritto internazionale. A me pare che sia totalmente
       sbagliata", ha detto il politico liberale di Palazzo Chigi. "Sotto...

       Translation: It passes for seven points in Matteo Salvini’s program to stop the flows and give more security
       to the country. Blocking ports to ships flying the flag of a European Union member state and not the United
       Kingdom, as announced by Salvini, would be against law and treaty, according to former Justice Minister Franco
       Frattini. "There is an interpretation of international law. It seems to me that it is totally wrong," said the liberal
       politician from Palazzo Chigi. "Under...

       Issue type: Factual errors.
       Original Text: Alla vigilia dell’incontro, a Bruxelles, tra Jean-Claude Juncker e il presidente del Consiglio
       Giuseppe Conte, che sarà accompagnato dal ministro dell’Economia Tria, il commissario Ue Pierre Moscovici
       usa tona concilianti per suggerire che l’Italia non dovrebbe fare la spola tra l’Europa e le banche a credito. "Sarà
       difficile", dice il francese, "se la Banca centrale germanica non pone il suo veto alla pesca in una sola mano per
       un paese come l’Italia che sta in cerca di finanziamenti". "La...

       Translation: On the eve of a meeting in Brussels between Jean-Claude Juncker and Prime Minister Giuseppe
       Conte, who will be accompanied by Economy Minister Tria, EU Commissioner Pierre Moscovici uses concilia-
       tory tones to suggest that Italy should not shuttle between Europe and banks on credit. "It will be difficult," says
       the Frenchman, "if the German Central Bank does not veto single-handed fishing for a country like Italy that is
       looking for financing." "The...

       Issue type: Unnatural expression.
       Generated Text: Forti temporali si sono abbattuti nella mattinata di oggi su Milano e sul nord-ovest della
       Lombardia, spazzando via il caldo degli ultimi giorni. Il nubifragio ha creato qualche rallentamento sulle strade.
       Poche colture e alcune piantine. Questi sono i principali danni dei fenomeni atmosferici che hanno colpito
       l’Italia. L’Italia centro-meridionale ha visto 304.363 colture danneggiate, quasi 15mila piantine e 1.532 migliaia
       di alberi, una pioggia netta di oltre 10mila mila chili sul versante del Po e una coltura danneggiata...

       Translation: Strong thunderstorms hit Milan and northwestern Lombardy in the morning today, sweeping away
       the heat of the past few days. The cloudburst created some slowdowns on roads. Few crops and a few seedlings.
       These are the main damages of the weather phenomena that hit Italy. South-central Italy saw 304,363 crops
       damaged, nearly 15,000 seedlings and 1,532,000 trees, a net rainfall of more than 10,000,000 kilograms on the
       Po River side, and a damaged crop...

       Issue type: Factual error.

Table 9: Examples of mistakes made by Llama 7B fine-tuned on Italian. The smaller Llama 7b after fine-tuning
generates flowing text but the facts are anyway less accurate than for larger models. Out of 25 samples manually
examined for this model, we find 5 contradicting the prompt, 0 switching to English, 5 unnatural Italian expressions
and 6 grammatical errors.




                                                              15331
       Llama 65B Pre-Trained
       Generated Text: In centro Italia continuano le scosse e il numero dei morti sale. Paesi afoni e distrutti, palazzi
       accartocciati, mozziconi di chiese, rovine sinistre che fissano le piazze. E I corpi stanno fuori dalle case, senza
       casa, senza neanche la tomba che li ricuopre. Le indagini del Giornalista Enrico Lucci e le testimonianze dei
       superstiti. The BBC’s Gavin Lee reports from Norcia, the central Italian town hardest hit by the quake. Italian
       Prime Minister Matteo Renzi has visited one of...

       Translation: In central Italy, the tremors continue and the death toll rises. Aphonious and destroyed villages,
       crumpled buildings, church butts, sinister ruins staring into squares. And The bodies stand outside homes,
       homeless, without even the grave to cover them. Journalist Enrico Lucci’s investigation and survivor testimony.
       The BBC’s Gavin Lee reports from Norcia, the central Italian town hardest hit by the quake. Italian Prime
       Minister Matteo Renzi has visited one of...

       Issue type: Grammatically correct, but does not sound natural in Italian.
       Original Text: Due sbarchi in sole ventiquattr’ore a Lampedusa. Sono 84 gli immigrati giunti nell’isola tra
       venerdì e sabato e ospitati all’Hotspot di contrada Imbriacola. Tra loro ci sono anche I tre naufraghi di Tortuga,
       recuperati da un mercantile libanese. Non è ancora stata resa nota l’identità nazionale dei naufraghi, ma non
       mancano inchieste di persone che si sono rivolte ai carabinieri per cercare I loro cari. Lampedusa, 38 migrants -
       mostly from Tunisia - arrived safely on the island in...

       Translation: Two landings in just twenty-four hours on Lampedusa. A total of 84 immigrants arrived on the
       island between Friday and Saturday and were housed at the contrada Imbriacola Hotspot. Among them are also
       The three shipwrecked Tortuga, recovered by a Lebanese merchant ship. The national identity of the castaways
       has not yet been released, but there is no shortage of inquiries from people who have turned to the Carabinieri to
       search for their loved ones. Lampedusa, 38 migrants - mostly from Tunisia - arrived safely on the island in...

       Issue type: Switch to English
       Generated Text: I numeri fanno spavento. Cinquemila disperati sbarcati solo nelle ultime quarantott’ore, quasi
       65mila nei primi sei mesi dell’anno. Che l’ operazione "Mare Nostrum", varata dopo la strage di Lampedusa,
       fosse riuscita a fermare il flusso di barche di migranti, lo abbiamo rilevato già da pochi mesi. Che la spinta
       verso l’Italia del prossimo potesse crescere di conseguenza, lo sapevamo. Che si dovesse progettare una strategia
       efficace e responsabile, in grado di dire dove e come, giustamente, stava l’ opportunità...

       Translation:The numbers are frightening. Five thousand desperate people landed in the last forty-eight hours
       alone, nearly 65,000 in the first six months of the year. That operation "Mare Nostrum," launched after the
       Lampedusa massacre, had succeeded in stopping the flow of migrant boats, we noted a few months ago. That the
       push to Italy of the next could grow as a result, we knew. That an effective and responsible strategy had to be
       designed that could tell where and how, rightly, the ’opportunity lay....

       Issue type: Contradicts the prompt.

Table 10: Examples of subtle mistakes made by pretrained Llama 65B. While the quality of the language is almost
on par with the prompts, written by professional journalists (for these short examples), the content is largely made
up although in a realistic way. Out of 25 samples manually examined for this model, we find 2 contradicting the
prompt, 3 switching to English, 7 unnatural Italian expressions and 2 grammatical errors.




                                                            15332
       Llama 65B Fine-Tuned
       Generated Text: Gabriele Gravina è stato eletto presidente della Figc. Ha ottenuto il 92,2% dei voti (al primo
       turno serviva il 75%). Si chiude la gestione commissariale di Roberto Fabbricini, durata 9 mesi. L’ultimo
       presidente eletto era Carlo Tavecchio nel 2014, che aveva ottenuto il 63%. Gravina: "Riconoscendomi orgogliosa-
       mente l’apostrofe di figlio della Sicilia e della Normandia che le mie origini e la mia vita mi fanno, ho iniziato la
       mia esperienza nel calcio. Un calcio che ho giocato da bambino,...

       Translation: Gabriele Gravina has been elected president of Figc. He has obtained 92.2% of the votes (on first
       round he needed 76%), This ends the Roberto Fabbricini’s technical administration, which lasted 9 months. The
       last president to be elected was Carlo Tavecchio in 2014, he scored 63%. Gravina: "Proudly acknowledging
       the apostrophe of son of Sicily and Normandy that my origins and my life make me, I began my experience in
       soccer. A soccer I played as a child,..."

       Issue type: Factual errors.
       Original Text: “È superficiale dire che è risorta la Dc ”. Parola di Francesco Rutelli che, intervistato dal Corriere,
       ripercorre le tappe della vita della Margherita, partito in cui hanno militato sia lui che Bertinotti. Rutelli l’ha
       lasciato da qualche anno e adesso è presidente dei Liberali per l’Italia, la lista che recentemente ha lanciato al
       Senato. E Bertinotti è tornato alla Dc per partecipare alle primarie del partito di D’Alema e Bersani, l’unico che
       ha il voto dei sostenitori della...

       Translation: “It is superficial to say that the DC has risen again." Word of Francesco Rutelli, who, interviewed
       by Corriere, traces the stages of the life of Margherita, a party in which both he and Bertinotti militated. Rutelli
       left it a few years ago and is now president of Liberals for Italy, the list he recently launched in the Senate. And
       Bertinotti returned to the DC to participate in the primaries of D’Alema and Bersani’s party, the only one that
       has the supporter vote of the...

       Issue type: Factual errors.
       Generated Text: Dopo 19 giorni, grazie all’accordo trovato dall’Europa, I 49 migranti di Sea Watch e Sea Eye
       sono sbarcati nel porto maltese di La Valetta, dove sono stati trasportati a bordo di autobus. Il ministro Migranti
       e Strade del Popolo Gabriele Toccafondi nei giorni scorsi ha incontrato a Parigi il ministro degli Esteri francese
       Jean-Yves Le Drian, il ministro dell’interno Christophe Castaner, il ministro della giustizia Nicole Belloubet e il
       ministro dell’istruzione Jean-Michel Blanquer. Si tratta di una missione di...

       Translation: After 19 days, thanks to the agreement found by Europe, The 49 migrants from Sea Watch and
       Sea Eye landed in the Maltese port of La Valetta, where they were transported aboard buses. Migrants and
       People’s Roads Minister Gabriele Toccafondi in recent days met in Paris with French Foreign Minister Jean-Yves
       Le Drian, Interior Minister Christophe Castaner, Justice Minister Nicole Belloubet, and Education Minister
       Jean-Michel Blanquer. This is a mission of...

       Issue type: Factual errors.

Table 11: Examples of subtle mistakes made by Llama 65B fine-tuned on Italian. While the quality of the language
is almost on par with the prompts, written by professional journalists (for these short examples), the content is
largely made up although in a realistic way. Out of 25 samples manually examined for this model, we find 0
contradicting the prompt, 0 switching to English, 1 unnatural Italian expressions and 4 grammatical errors.




                                                              15333
     Field             Content
     Original Text:    Dato il seguente titolo di un articolo di giornale scrivi l’articolo. ### Titolo:"Nel Pd niente
                       conte interne". Ma su un sito i nomi dei pro M5S ### Articolo: Alla vigilia della direzione che
                       potrebbe, ma non necessariamente, sancire la separazione con gli scissionisti guidati da Renzi,
                       il Pd cerca di chiudere la partita che tra poco si apre. La maggioranza del partito, insistono al
                       Nazareno, per ora "non intende partecipare ad un conto interne",
     Translation       Given the following title of a newspaper article, write the article. ### Title:"No internal counts
                       in the Democratic Party". But on a site the names of the M5S pros ### Article: On the eve of
                       the direction that could, but not necessarily, sanction the separation with the splinterists led by
                       Renzi, the Democratic Party tries to close the game that will soon open . The majority of the
                       party, the Nazareno insists, for now "does not intend to participate in an internal account"
     Modification 1:   Dato il seguente titolo di anteprima di giornale scrivi lárticolo.### Titolo: "Nel Pd niente esodati,
                       Ma su un sito I nomi dei pro M5S ### Articolo: Alla vigilia della direzione che potrebbe, ma
                       non necessariamente, sancire la rottura definitiva con gli scissionisti guidati da Renzi, il pd cerca
                       il suo partner di governo dietro la partita m5s che da poco si apre. La maggioranza del partito,
                       insistono al Nazareno, per ora "non intende partecipare ad un conto interne"
     Translation:      Given the following newspaper preview title, write an article.### Title: "No exoduses in the
                       Democratic Party, but on a site the names of the M5S pros ### Article: On the eve of the
                       direction that could , but not necessarily, sanction the definitive break with the splinterists led by
                       Renzi, the Democratic Party is looking for its government partner behind the m5s match that has
                       recently opened. The majority of the party, the Nazareno insists, for now "does not intend to
                       participate in an internal account"
     Modification 2:   Dato il seguente titolo di un articolo di giornale scrivi lárticolo. ### Titolo: "Nel Pd niente conte
                       interne". Ma su un annuncio già I nomi dei pro M5S ### Articolo: Alla vigilia al voto che
                       potrebbe, ma non necessariamente, sancire la separazione con I dem guidati da Renzi, il pd cerca
                       di chiudere la partita che tra poco si apre. La maggioranza del partito, insistono al Nazareno, è
                       ferma sulla linea del "non cedere ad un conto interne"
     Translation:      Given the following title of a newspaper article, write the article. ### Title:"No internal counts in
                       the Democratic Party". But on an announcement already the names of the M5S pros ### Article:
                       On the eve of the vote that could, but not necessarily, sanction the separation with the democrats,
                       the Democratic Party tries to close the game that will soon open . The majority of the party, the
                       Nazareno insists, is fixed on the idea of "not giving in to an internal account"

Table 12: Examples of Italian text modifications from IT5 models, used to compute the DetectGPT score. We
show the translation and two modifications, in red the chunks that have been replaced. Depending on the length the
modifications can alter the meaning of the original sentences, however they work to normalize a sentence likelihood
and compute DetectGPT.


D.1 Modifications from IT5
The modification from IT5 to compute the Detect-
GPT score don’t necessarily need to have a mean-
ing as they are only used to normalize the log-
likelihood values, however, it is interesting to note
that often they don’t disrupt the sentence meaning,
and that they can create new sentences, although
with similar meaning, that can themselves be use-
ful as synthetic data. We release 600k of these
sentences that are half modifications of the original
news and half modifications of the synthetic texts
generated by our fine-tuned models.




                                                            15334
                                                                   Temperature    DetectGPT        log-likelihood
                                                                          0.6         48%              86%
                                                                          0.8         63%              73%
                                                                          1.0         77%              52%

                                                            Table 14: AUROC achieved by DetectGPT and log-
                                                            likelihood on Llama 13B varying the temperature used
                                                            while generating the synthetic sentences.
         (a) GPT2                 (b) Llama 13B
                                                             generator           llama-2-7b_xsum      mistral_xsum
Figure 6: ROC curve for DetectGPT and log-likelihood.                             dGPT      llh       dGPT       llh
In (a) for the GPT2 model over 100 samples from              llama-2-7b           0.82      0.63        0.65        0.52
xsum (coherent with (Mitchell et al., 2023)), in (b) for
                                                             llama-2-7b_xsum      0.86      0.69        0.65        0.53
llama13b model over 100 samples from xsum.                   (995 samples)
                                                             llama-2-7b_xsum      0.89      0.75        0.65        0.54
                    DetectGPT           log-likelihood
              t5-base t5-3b t5-11b                           Mistral-7B-v0.1      0.59      0.41        0.77        0.59

 Llama 13b     66%      71%     75%          78%             mistral_xsum         0.57      0.44        0.85        0.75
                                                             (995 samples)
 Llama 65b      -       62%     66%          70%
                                                             mistral_xsum         0.53      0.43        0.95        0.92

Table 13: AUROC achieved by DetectGPT (varying
bootstrapping model) and log-likelihood on the xsum         Table 15: The AUROC achieved by all the models
data-set for Llama 13B and Llama 65B.                       (rows) at different levels of fine-tuning, from pretrained
                                                            only to fine-tuned on the full dataset. In bold the higher
                                                            AUROC in each column.
E     Generalizability to English
E.1    Synthetic Text Detection Based on Token                 To establish a fair comparison with DetectGPT
       Likelihoods                                          while testing Llama, we perform an ablation study
To confirm that our setup in subsection 5.1 is com-         based on varying the temperature used in genera-
parable to the previous efforts, we start by repli-         tion.
cating a core result by Mitchell et al. (2023): on             Table 14 shows different AUROC values for dif-
xsum data (Narayan et al., 2018), and using differ-         ferent temperatures. It appears that there is a strong
ent versions of t5 (Raffel et al., 2020) DetectGPT          sensitivity of the detection methodologies to this
outperforms the log-likelihood in detecting GPT2            hyper-parameter, which merits further investigation
text (Radford et al., 2019) (see Figure 6a).                in future work. The value 0.8 where DetectGPT
   We apply the same methodology to sentences ob-           and log-likelihood are more aligned, is also the
tained using Llama 13B and Llama 65B. For Llama,            value reported in the Llama repository.
we were unable to get DetectGPT to achieve a
higher AUROC than the log-likelihood. We believe            E.2    Detecting CFMs with Proxy Models
this to be due to the stronger performance of Llama         We repeat the experiments done for the CHANGE-
compared to the t5 model used to generate new               it dataset also for the XSUM dataset (Narayan et al.,
sentences (Figure 6b). This suggests that English           2018).
text generated by Llama is harder to detect.                    That is we fine-tuned llama-2-7b and mistral on
   To test this hypothesis we measure the impor-            the full XSUM training set. We generate 2 datasets
tance of the bootstrap model in this case. Table 13         with 1k synthetic texts generated with each of the
shows the AUROC of DetectGPT depending on the               fine-tuned models and 1k samples from the xsum
bootstrap model, a larger t5 model leads to higher          test set (less than for CHANGE-it to limit compute
AUROC.                                                      costs). Then we also fine-tune these two models
   We repeat the experiment with both DetectGPT             on a small subset of the trainig set, 995 samples
and log-likelihood at various temperature settings          and finally we compute DetectGPT achieved by
(0.6, 0.8, 1.0), and we find a strong sensitivity to        these 6 models, llama-2-7b and mistral pre-trained,
this hyper-parameter, which merits further investi-         llama-2-7b_xsum_995 and mistral_xsum_995 fine-
gation.                                                     tuned on 995 samples and llama-2-7b_xsum and
                                                         15335
mistral_xsum fine-tuned on the xsum dataset.
   Table 15 shows the results that closely match
those for CHANGE-it shown in Table 2, namely
that fine-tuning also on a small set of the same do-
main leads to high AUROC while if models come
from different pre-trained ones the performance is
low.

F      Prompting details
Figure 7 shows the exact prompt that was used for
generating the synthetic texts in section 6. In the
prompt, we retain a few initial tokens of the original
article, ensuring that the prompt never exceeded 30
words in total.

    """Given the following article title, generate the article.
    ### Title:
    {title}
    ### Article:
    {article}"""


Figure 7: Prompt used for generating news-like texts in
section 6.


G      Receiver Operating Characteristic
       (ROC) Curves
The receiver operating curve is a measure to under-
stand how setting a threshold over a score would
influence the true positive rate (TPR, the numer
of instances marked as positive divided by the to-
tal number of positives) and the false positive rate
(FPR, the number of false positive divided by the
number of all negatives). That means how setting
all instances with a score above a certain thresh-
old as positive would influence the number of true
positive and false positive.
   Given that when we set as a threshold the maxi-
mum value of a score all instances are classified as
negative TPR equals 0 and FPR equals 0, viceversa
when it is set to the minimum TPR equals 1 and
FPR equals 1. The ROC curve is a plot of the TPR
against the FPR for different thresholds.
   To show further details about the proxy models
AUROC values shown in Table 2. Figure 8 shows
the ROC curves for the case when the proxy models
come from the same pre-trained one.
   We can see tha computing the AUROC over 10k
examples leads to a smooth curve and that the shape
is very consistent across different amounts of fine-
tuning futher validating the strngth of proxy mod-
els.
                                                                  15336
         Llama-2-13b_it




            (a) llama-2-13b_it   (b) llama-2-13b_it_3981 (c) llama-2-13b_it_7862   (d) llama-2-13b


         Llama-2-7b_it




             (e) llama-2-7b_it   (f) llama-2-7b_it_3981   (g) llama-2-7b_it_7862   (h) llama-2-7b


         Mistral_it




            (i) llama-2-13b_it   (j) llama-2-13b_it_3981 (k) llama-2-13b_it_7862     (l) mistral

Figure 8: The ROC curves for the proxy models when evaluated on data generated by models fine-tuned starting
from the same pre-trained model.




                                                     15337
H    Computational Costs
The fine-tuning run of our ‘CFM’ Llama (§3) lasted
5 days, as we wasted approximately 2 days due
to exploding loss. Experiments were conducted
using a private infrastructure, which has a carbon
efficiency of 0.432 kgCO2 eq/kWh. A cumulative
of 2,304 hours of computation was performed, and
total emissions are estimated to be 298.6 kgCO2 eq.
   The fine-tuning of llama-2-7b_it, llama-2-13b_it
and mistral_it on CHANGE-it took 64 GPU hours
each on A100 64Gb GPUs. With the costly syn-
thetic data generation, all together resulted in ap-
proximately 2000 GPU hours. Experiments were
conducted using the LEONARDO cluster, which
has a carbon efficiency of 0.432 kgCO2 eq/kWh. A
cumulative of 2000 hours of computation was per-
formed on hardware similar to A100 PCIe 40/80GB
(TDP of 250W). Total emissions are estimated to
be 216 kgCO2 eq (Luccioni et al., 2019).
   Thus, we estimate that the total emissions for
experiments in this study amount to approximately
515 kgCO2 eq.




                                                  15338
