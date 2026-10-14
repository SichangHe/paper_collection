                                                                   Beyond SEO: A Transformer-Based Approach for
                                                                       Reinventing Web Content Optimisation


                                                                            Florian Lüttgenau, 1 Imar Colic 2 Gervasio Ramirez 2


                                                                    Abstract                              nature of generative models intensifies this challenge, un-
                                                                                                          derscoring the urgent need for fresh theoretical frameworks
                                                 This paper presents a fine-tuned BART-base               and practical strategies.
arXiv:2507.03169v1 [stat.ML] 3 Jul 2025




                                                 model for optimising travel website content to im-
                                                 prove visibility in generative search engines. Us-       Recent work by Aggarwal et al. (2024) proposes Gener-
                                                 ing synthetically generated training data of 1905        ative Engine Optimisation (GEO), a new framework that
                                                 cleaned instances and domain-specific strategies,        rethinks visibility as a multidimensional metric rooted in
                                                 the model was trained in a supervised approach           how web content is transformed and evaluated within gen-
                                                 and achieved measurable gains in ROUGE-L and             erative model outputs. Leveraging generative pre-trained
                                                 BLEU compared to the BART-base model. In                 transformers (GPTs), their approach uses a black-box op-
                                                 simulations, our proposed model boosted website          timisation pipeline and benchmarks multiple optimisation
                                                 visibility in generative engines by up to 30.96%.        strategies across domains. GEO uses a set of optimisa-
                                                 Our work shows that even small-scale, domain-            tion strategies that differ from conventional SEO practices,
                                                 focused fine-tuning can significantly enhance con-       like for instance: Content fluency, quotation addition, sta-
                                                 tent discoverability in AI-driven search engines.        tistical data, or authoritative tone. Aggarwal et al. (2024)
                                                                                                          demonstrate that previous SEO techniques are largely inef-
                                                                                                          fective for enhancing visibility within generative engines,
                                                                                                          while GEO-specific strategies can boost visibility by up to
                                          1. Introduction                                                 40%. However, the effectiveness of these methods varies
                                          The era of keyword-driven search engines pioneered and          across sectors, calling for domain-specific research (Ag-
                                          lead by Google, and conventional SEO (Search Engine Op-         garwal et al., 2024). Additionally, they emphasise the im-
                                          timisation) tactics focused on keyword placement and back-      portance of studying proposed GEO optimisation methods
                                          link building is coming to an end. This disruption stems        in combination, as practitioners are likely to use multiple
                                          from the rise of large language models (LLMs) and the rapid     approaches together, making theoretical research more ap-
                                          adoption of generative AI-driven search models powered          plicable to real-world practice.
                                          such as ChatGPT Search or Perplexity AI (Amer & El-             In this report, we aim to contribute to this emerging field
                                          boghdadly, 2024). Unlike conventional search engines that       by focusing on the travel and tourism industry, a content-
                                          return ranked link lists, generative engines draw on multiple   rich domain that depends heavily on online visibility. Our
                                          sources to craft coherent, conversational, and personalized     goal is to explore whether model fine-tuning and domain-
                                          answers—transforming how information is retrieved, how          adapted optimisation techniques can improve content visibil-
                                          users interact with given content, and how content and in-      ity in generative search settings. We fine-tune a pre-trained
                                          formation is discovered (Aggarwal et al., 2024).                BART-base model on tourism-specific data in a supervised
                                          By 2026, Gartner predicts a 25% reduction in conventional       setting, aiming to reduce data and compute requirements -
                                          search engine usage (LoDolce & Howley, 2024), signalling        while maintaining high accuracy. We evaluate the perfor-
                                          a paradigm shift that poses substantial challenges for web-     mance of optimised website content generated by this model
                                          site owners, digital marketers, and content creators striving   using objective visibility metrics.
                                          to maintain online visibility. The opaque, fast-changing        Hence, our contributions are threefold:
                                             1
                                               Department of Management, London School of Economics
                                          and Political Science, London, United Kingdom 2 Department of     1. We apply GEO methods on a domain-specific scope:
                                          Statistics, London School of Economics and Political Science,
                                          London, United Kingdom. Correspondence to: Florian Lüttgenau
                                                                                                               Travel and tourism industry.
                                          <f.e.luttgenau@lse.ac.uk>, Imar Colic <i.colic@lse.ac.uk>.
                                                                                                            2. We introduce a fine-tuning approach to train an efficient
                                                                                                               transformer that learns to generate optimised content.
                                      Transformer-Based Generative Engine Optimization

  3. We evaluate the effectiveness of applying multiple           the introduction of GEO-bench, a large-scale benchmark
     GEO methods in combination, reflecting realistic usage       encompassing diverse user queries across multiple domains
     scenarios.                                                   and topics, they demonstrated that GEO-specific strategies
                                                                  could boost content visibility by up to 40% in generative
                                                                  engine outputs.
The fine-tuned model achieved a ROUGE-L score of 0.249,
approximately 25%, indicating moderate recall of key infor-       Aggarwal et al. (2024) introduce seven methods to trans-
mation. The model achieved a BLEU score of 0.2, indicating        form raw website content into a more appealing style to be
20% n-gram precision between its output and the reference         favored by generative search engines. For instance, these in-
texts. This suggests a moderate alignment in vocabulary and       clude adopting an authoritative tone, citing credible sources,
structure, reflecting a reasonable level of content similarity.   adding statistical evidence, or improving linguistic fluency.
The proposed model boosts website visibility by 15.63%            Among these, the most effective methods were statistics ad-
in absolute word count and 30.96% in position-adjusted            dition and citations, as identified through their experimental
word count, with results normalised and outliers excluded         evaluation. Notably, their approach utilized publicly avail-
to ensure robustness.                                             able GPTs without any model fine-tuning or task-specific
                                                                  adaptation.
The remainder of this report is organised as follows. We first
review related work on emerging approaches for generative         To the best of our knowledge, no existing research has
engine optimisation. Then, we describe our methodology,           explored the application of model fine-tuning to develop
including data collection, content preprocessing, and the         domain-tailored models for web content optimisation in
application of domain-specific optimisation as a labelling        generative search engines.
strategy using existing large language models. We follow
with a presentation of our model architecture, before detail-     3. Approach
ing our training methods and evaluation framework. Finally,
we present results, discuss and interpret key findings, and       3.1. Data Generation
conclude with reflections on limitations and future direc-        To train our transformer model, we created a custom dataset
tions.                                                            tailored to the travel and tourism domain. Each data point
                                                                  consists of a pair (w, w’), where w is raw website content and
2. Related Work                                                   w’ is a version optimised for visibility in generative engine
                                                                  responses (label). Since there are no publicly available
Given the novelty of the field and its rapid pace of devel-       datasets containing such website content or associated user
opment, there is limited academic research specifically ad-       queries, we generated all data from scratch, following a
dressing web content optimisation for generative search           structured approach informed by the findings of Aggarwal
engines. Although several scholars have explored the use          et al. (2024).
of generative AI to enhance conventional SEO practices
(e.g. Ziakis & Vlachopoulou, 2024; Yuniarthe, 2017), novel        The first step of data generation began with creating realis-
methods going beyond SEO remain sparse.                           tic user queries across 11 subcategories within the domain.
                                                                  To achieve this, we used Meta-Llama-3-8B-Instruct via the
The emergence of LLM-based search systems gave rise for           HuggingFace API, with a temperature of 0.9 and a set of
initial works in this emerging domain. For example, Liu           carefully crafted templates to ensure variation and authen-
et al. (2023) and Menick et al. (2022) emphasise verifiabil-      ticity. After generation, the query set was cleaned to remove
ity, factual correctness and coherence of LLM-generated           duplicates and ensure diversity.
responses, but do not address the visibility or ranking of
source content within those responses. Sporadic contribu-         The second step of the data generation process was con-
tions in boosting visibility in generative engines include        ducted to collect raw website content (w). For each query,
Kumar & Lakkaraju (2024) who investigate how modifying            we used the Google Search API to scrape website data from
textual input can enhance product visibility in LLM outputs.      the top five search results. If a website blocked scraping or
However, their work is narrowly scoped to e-commerce              contained less than 100 characters of content, it was marked
scenarios and focuses on content addition rather than trans-      as irrelevant for our dataset and thus excluded. We contin-
formation.                                                        ued scraping subsequent results until five usable sources
                                                                  were collected per query. This gave us a reliable set of raw
The foundational contribution to the field concerned - and        website texts.
the root of this report - is the work by Aggarwal et al. (2024)
who coined the notion of GEO. They propose a black-box
optimisation framework designed to enhance the visibility of
web content in generative search engine responses. Through
                                      Transformer-Based Generative Engine Optimization

3.2. Content Pre-Processing                                       as our main model due to its powerful sequence transfor-
                                                                  mation capabilities. The architecture consists of a bidirec-
Raw website content required thorough cleaning before anal-
                                                                  tional encoder (BERT) and an autoregressive decoder (GPT)
ysis. Due to input length limitations, we trimmed content
                                                                  (Soper et al., 2021), making it ideally suited for transform-
to a maximum of 4000 characters while preserving essen-
                                                                  ing raw website content into optimised versions - for more
tial information. The process began with HTML content
                                                                  visibility in generative search engines.
extraction using BeautifulSoup, which removed script and
style elements while maintaining proper text formatting. We
                                                                  4.2. Pre-Training Approach
focused on eliminating non-essential website elements such
as navigation menus, advertisements, footers, and social          Before examining the specific architectural components,
media widgets that did not contribute substantive informa-        it’s important to understand BART’s distinctive pre-training
tion. Quality control metrics ensured only valuable content       approach:
was included by filtering out websites with insufficient text
and avoiding domains known to block scrapers. We also             Denoising Autoencoder: BART is pre-trained as a denois-
conducted a manual cleaning iteration, to further increase        ing autoencoder, using a training objective that corrupts
data quality resulting in the database which will be used for     input text and then tasks the model with reconstructing the
labelling - optimising the given text input.                      original. Merging BERT’s bidirectional context modelling
                                                                  with GPT’s autoregressive generation creates a backbone
                                                                  that adapts efficiently to downstream text-generation tasks.
3.3. Labelling
                                                                  Noising Functions: Before any token embeddings or neural
To produce optimised versions of raw website content, we
                                                                  layers, one of five different noising functions is randomly
transformed each text w into a visibility-optimised version w’
                                                                  chosen and applied to the raw text, producing a ”corrupted”
using strategies shown by Aggarwal et al. (2024) and treat-
                                                                  version that the model must learn to reconstruct:
ing these labelled outputs as ground truth for our model. Our
optimisation pipeline employed Llama-3.3-70B-Instruct-
Turbo-Free via the together.ai API in a systematic three-step      Noise type      What it does
process. (1) Credible-sounding citations were integrated           Token Masking   Randomly replace tokens with a spe-
to enhance content authority. (2) Language fluency was                             cial [MASK] token. The model
improved, complex phrasing was simplified, and key in-                             must predict the original token from
formation was preserved. (3) Compelling statistics were                            context.
placed strategically to reinforce key points. All three phases     Token Deletion  Remove random tokens entirely.
involved reorganizing content into clearly separable sections                      The model learns to infer which
with descriptive headings and structured paragraphs.                               words were dropped.
                                                                   Text Infilling  Sample spans of text (of varying
The pipeline maintained careful pacing between API calls
                                                                                   length) and replace each span with
to avoid rate limiting issues. Following optimisation, we
                                                                                   a single [MASK]. The model must
conducted thorough data cleaning to remove entries affected
                                                                                   generate the missing span.
by API errors or formatting inconsistencies, ensuring high
                                                                   Sentence Permu- Split the document into sentences
quality across the dataset. Finally, we obtained a dataset
                                                                   tation          and shuffle their order. The model
with the raw website text w and the respective optimised text
                                                                                   must recover the original discourse
w’ in the final dataset: X final filtered labelled dataset.csv.
                                                                                   sequence.
                                                                   Document Rota- Pick a random token index, rotate
4. Architecture                                                    tion            the text so that this point becomes
                                                                                   the ”start.” The model must re-align
4.1. Introduction to BART
                                                                                   and recover the original start.
BART (Bidirectional and Auto-Regressive Transformers)
is a sequence-to-sequence model developed by Facebook                      Table 1. BART pre-training noising functions
AI in 2019 that combines the strengths of both BERT (Bidi-
rectional Encoder Representations from Transformers) and
GPT (Generative Pre-trained Transformer). It was designed         This corruption-reconstruction objective makes BART natu-
as a flexible architecture particularly suitable for a wide       rally robust to imperfect, noisy, or incomplete input data -
range of text generation tasks, including summarisation,          a valuable property regarding the variability and messiness
paraphrasing, and content rewriting (Lewis et al., 2019).         prevalent in scraped web content (Lewis et al., 2019). Re-
                                                                  search has even shown performance improvements resulting
For our web content optimisation project, we selected BART
                                                                  from added noise in input text (Soper et al., 2021).
                                     Transformer-Based Generative Engine Optimization

4.3. Tokenisation                                                 4. Second Residual Connection + LayerNorm: This
                                                                     adds the FFN output back to its input and normalises it
Tokenisation transforms human-readable text into numer-
                                                                     also once again:
ical format for neural network processing. BART uses a
standard token embedding layer to convert discrete input to-                    x ← LayerNorm(x + FFN(x))
kens into dense vector representations. Each token from the
vocabulary is mapped to a continuous vector of fixed dimen-
sionality - 768 in the BART-base model (Lewis et al., 2019).     Encoder Function: The encoder’s self-attention mecha-
It employs Subword Tokenisation using byte-pair encoding         nism allows it to weigh the importance of each word or
(BPE). Additionally, it maps each token to an integer ID         token in the input sequence in relation to all other tokens,
from the vocabulary. Besides this, it creates attention masks,   enabling the model to capture long-range dependencies and
padding, and special tokens. Positional embeddings are then      relationships efficiently (Alokla et al., 2022). The 6-layer
added to these token embeddings to encode the sequential         depth provides several benefits: (1) Hierarchical feature
order of the tokens. This allows the model to associate each     extraction: Lower layers learn local patterns while deeper
word with an integer and assign its position within texts and    layers capture higher-level semantics. (2) Greater mod-
sentences. The resulting combined embeddings are passed          elling capacity: Each additional layer refines the represen-
into the encoder (Alokla et al., 2022).                          tation. (3) Long-range dependency modelling: The full
                                                                 self-attention mechanism allows BART to consider interac-
4.4. Encoder Architecture (6 Layers)                             tions between any pair of tokens in the sequence regardless
                                                                 of their distance (Lewis et al., 2019).
The encoder in BART ingests the (noised and tokenized)
input and produces a rich contextual representation that the     4.5. Decoder Architecture (6 Layers)
decoder will use when generating text. Each encoder block
consists of the following layers which perform the following     The decoder is responsible for generating the optimised
operations:                                                      output token-by-token based on the encoded input. Each de-
                                                                 coder block consists of the following layers which perform
  1. Multi-Head Self-Attention: This component projects          the following operations:
     the input into Query (Q), Key (K), and Value (V )
     spaces which enables it to compute attention using:          1. Masked Multi-Head Self-Attention: It allows the
                                        QK T                         decoder to look only at previous tokens it has generated
          Attention(Q, K, V ) = softmax( √ )V                        so far, which are not future tokens. Additionally it
                                          dk
                                                                     ensures autoregressive decoding (one word at a time)
     Variable d resembles the embedding size - being the             and it uses a lower triangular mask matrix:
     dimension of the embedding matrix E ∈ RV ×d , where
     dk stands for the dimension per attention head. This                                                 QK T
     means that it allows each token to ”look at” every other         MaskedAttention(Q, K, V ) = softmax( √ +mask)V
                                                                                                            dk
     token and to gather relations within the whole context.
  2. Residual Connection + LayerNorm: This adds the               2. Encoder–Decoder Cross-Attention: This takes the
     attention output back to the original input (”skip con-         encoder’s output as keys and values and the decoder’s
     nection”), and then normalises it:                              hidden states as queries and enables the decoder to
                                                                     focus on relevant parts of the input sequence.
            x ← LayerNorm(x + MultiHead(x))

  3. Position-wise Feed-Forward Network (FFN): Here               3. Feed-Forward Network (FFN): This neural network
     two linear transformations with GeLU activation func-           is the basic building block and is identical to the en-
     tions are applied in between, where W and b are re-             coder’s FFN in applying a non-linear transformation
     spectively the weight matrix and the bias term for the          independently to each token’s representation.
     first and the second linear transformation within the
                                                                  4. Residual Connections + Layer normalisation: Each
     neural network. The GeLU functions (Gaussian Er-
                                                                     sub-layer applies a residual connection by adding its
     ror Linear Unit) is preferred over the ReLU activation
                                                                     output to its own input, followed by layer normalisa-
     function. The GeLU is partly similar to the general ap-
                                                                     tion. Residual connections mainly help mitigate the
     plicable ReLU, but is differentiable everywhere, which
                                                                     vanishing gradient problem. Note that this input al-
     helps optimisation and gradient flow in deep models
                                                                     ready includes the positional embeddings (added once
     like transformers:
                                                                     at the start), but positional encodings are not repeatedly
           FFN(x) = W2 (GeLU(W1 x + b1 )) + b2                       added in residual connections.
                                        Transformer-Based Generative Engine Optimization

                                                                      Parameter             Configuration
                                                                      Vocabulary size       Derived from the pre-trained tok-
                                                                                            enizer
                                                                      Position embed-       Maximum length of 1024 tokens
                                                                      dings
                                                                      Model depth       6 layers each for encoder and de-
                                                                                        coder
                                                                      Model width       768-dimensional embeddings with
                                                                                        12 attention heads
                                                                      Feed-forward net- 3072-dimensional inner representa-
                                                                      works             tions (4× the model dimension)
                                                                      Regularisation    Dropout rate of 0.1
                                                                      Initialisation    Parameters sampled from N(0, 0.02)

                                                                               Table 2. BART-base model parametrisation
Figure 1. Outline of BART’s architecture. Source: (Vaswani et al.,
2023)
                                                                     The parametrisation of BART-base is balanced for both
Decoder Function: The decoder generates output se-                   expressiveness and computational efficiency. With six layers
quences autoregressively, which means it is relying on pre-          each in the encoder and decoder, hidden layers with size of
viously generated tokens while attending to the encoder’s            768 dimensions, and 12 attention heads, the model offers a
output (Tan et al., 2024). This cross-attention mechanism en-        strong balance between expressiveness and computational
ables the decoder to: (1) It uses the encoder’s full, two-way        tractability.
grasp of the input to guide its writing. (2) As it picks each
word, it zooms in on the most relevant parts of that encoded         4.7. Why choosing pre-trained BART instead of training
input. (3) It keeps its own previous words in mind so the                 from scratch
sentence stays coherent.                                             Our project initially explored implementing BART from
                                                                     scratch as an educational exercise, but we encountered sev-
4.6. Complete BART Model Architecture                                eral practical limitations that led us to adopt the pre-trained
The full BART architecture integrates the encoder and de-            BART-base model with fine-tuned parameters instead:
coder into a cohesive sequence-to-sequence model with                Data Scarcity Barrier: The modest performance metrics
three crucial components:                                            we observed stemmed primarily from our limited dataset
Model Components:                                                    size (only 1905 texts). The original (pre-trained, ready to be
                                                                     imported) BART was trained on over 160GB of text data in-
                                                                     cluding books, news, stories, and web text (Aggarwal et al.,
  1. Shared Token Embeddings: BART uses a single                     2024). At the same time, our from-scratch implementation
     shared embedding layer for both encoder and decoder,            is trained on 1905 website content examples, which shows
     whereas the parameter sharing reduces total parameter           the big discrepancy in data usage size. This represented a
     count and encourages consistency.                               fundamental data scale mismatch of several orders of magni-
                                                                     tude. Transformers require extensive exposure to linguistic
  2. Encoder-Decoder Pipeline: The encoder transforms                patterns to develop robust internal representations.
     input text into contextualized representations. After
     that, the decoder uses these representations in its cross-      Parameter Initialisation Challenge: When training from
     attention layers. This cross-attention acts as an infor-        scratch, our model began with randomly initialised parame-
     mation bridge between encoding and generation.                  ters (following the N(0, 0.02) distribution). These random
                                                                     starting points required substantial data and training iter-
  3. Language Modelling Head: Finally, the decoder’s                 ations to converge to useful representations, whereas pre-
     hidden states are mapped through a linear layer to              trained models begin with parameters that already encode
     produce a probability distribution over the vocab-              rich linguistic knowledge.
     ulary. This output layer shares weights with the                Computational Efficiency Trade-off: The computational
     input-embedding layer.                                          demands we encountered (1.5 hours for 3 epochs on a 16GB
                                                                     RAM Apple MacBook M1 Pro) highlighted the resource
Parameter Configuration:                                             intensity of training transformer models. This practical
                                      Transformer-Based Generative Engine Optimization

constraint limited our ability to train for sufficient epochs     Controlling over-fitting: Besides regularizing with weight
to reach optimal performance. Training on Google Colab            decay, the transformer already embeds dropout at 0.1.
crashed due to usage limitations.                                 Rather than intervening with early stopping, the run stores
                                                                  a checkpoint at the end of every epoch; the model with the
4.8. BART’s Advantages for Our Content optimisation               smallest validation loss is retained. This strategy avoids
                                                                  premature termination caused by high-variance sequence
BART’s architecture makes it particularly well-suited for         metrics while still protecting against over-fitting.
our web content transformation task. BART’s Transformer
architecture allows direct paths for gradients and informa-       Handling overly short and repetitive outputs: During
tion to flow between all tokens suitable for long website         early runs, we observed that the model often produced out-
content with distributed information. Bidirectional context       puts that were much shorter than the ground truth. This
(BERT) and autoregressive Generation (GPT) excels at com-         was problematic because short outputs could still score
prehending content and transforming it                            high on ROUGE-L by simply copying a few keywords,
                                                                  yet they failed to deliver the full rewritten version desired.
While building BART from scratch provided valuable ar-            To address this, two constraints were applied during decod-
chitectural understanding, for the task concerned, leverag-       ing: We introduce a length penalty α = 1.1 to the model’s
ing a pre-trained BART model and fine-tuning it on our            scoring so that shorter outputs incur a larger penalty, mak-
website content optimisation task yields superior perfor-         ing longer responses more likely. And we also activated
mance while requiring significantly less data and computa-        a no repeat ngram size of 3, a rule that forbids the
tional resources. For this reason, we chose the pre-trained       same 3-word phrase from appearing more than once, which
BART model. The full model architecture of BART-base              helps reduce exact copying.
can be found in the notebook /2 Deep Learning Model/BART
from scratch/OurBART.ipynb, while the pre-trained model
used for the project can be found in the /2 Deep Learn-           6. Numerical results
ing Model/Code/BART base supervised model.ipynb. The              6.1. Experimental settings
OurBART.ipynb notebook acts as a ”zoom-in” into the im-
ported model, which is reflected as Step 3 in the pre-trained     The hyperparameters of proposed model (our fine-tuned
BART base supervised model.ipynb file.                            model) and the BART-base (from Facebook AI) differ in
                                                                  the size of the context window that flows through the en-
                                                                  coder–decoder stack. Our proposed model enlarges the en-
5. Training Methods
                                                                  coder window to MAX IN= 384 and caps the decoder at the
5.1. Tokenisation of the dataset                                  same length, while BART-base is set to MAX IN= 256 and
                                                                  MAX OUT= 448 tokens. All remaining hyper-parameters,
The generated dataset contains travel-related web pages (w        optimisation schedule and hardware budget are held con-
and w’) that have slightly different length. To preserve the      stant.
natural imbalance between short and long content while
keeping training and validation distributions aligned, the
                                                                  6.2. Optimisation objective
raw page length is first partitioned into ten equiprobable
bins. Within every bin the same proportion of items is sam-       The optimisation objective during fine-tuning is the min-
pled, yielding splits of 80 % for training, 20 % for validation   imisation of token-level cross-entropy, which quantifies the
and a disjoint test set composed of 50 unseen queries (250        divergence between the true next-token distribution q and
instances of websites).                                           the model’s predicted distribution pθ . For a target sequence
                                                                  y = (y1 , . . . , yT ) generated conditionally on an input x, the
5.2. Training-argument rationale                                  cross-entropy is defined as:
Optimiser and learning-rate schedule: Fine-tuning uses
the AdamW optimiser (Kingma & Ba, 2017; Loshchilov                                        T
                                                                                          X
& Hutter, 2019) with a target learning rate of 3×10−5 and                 H(q, pθ ) = −         q(yt ) log pθ (yt | x, y<t )
decoupled weight decay for the regularisation in training                                 t=1

(λ = 0.01). To escape shallow minima the learning rate
increases from near zero for the first 250 updates reaching       which reduces to the negative log-likelihood of the observed
the target learning rate of 3×10−5 . The learning rate then       tokens under a one-hot encoding of q. This quantity is
follows a cosine decay towards zero, a heuristic shown to         computed at each training step and averaged between tokens
favour both faster convergence and better final generalisa-       in the batch. Figure 2 shows that the proposed model not
tion (Loshchilov & Hutter, 2017).                                 only starts better, but also converges faster in the loss of
                                                                  validation, despite its larger input window.
                                        Transformer-Based Generative Engine Optimization




Figure 2. Training and validation loss for Proposed and Baseline    Figure 3. Validation ROUGE-L (solid) and BLEU (dashed) for
models.                                                             Proposed and Baseline models.


6.3. Evaluation metrics
To evaluate the generative capabilities of the model beyond
token-level likelihoods, four complementary metrics are
                                                                    7. Interpretation
calculated after every epoch:                                       7.1. Model Evaluation
                                                                    Loss curve interpretation (Figure 2): Both models show
  1. ROUGE-L: Length of the longest shared word                     the expected monotonic decline in cross-entropy as training
     sequence between generated output and reference.               progresses, but the proposed configuration starts lower and
     Higher values mean better coverage of key phrases              falls steeper, converging to a validation loss below 2.0 by
     and structure.                                                 epoch 7. In contrast, the baseline flattens near 2.1. The gap
                                                                    suggests that the larger encoder window (384 vs. 256 tokens)
  2. BLEU: Precision of matching 1–4-word sequences                 helps the decoder ground its predictions in a richer context,
     (clipped n-gram precision (n ≤ 4)), with a penalty             shortening the ”learning runway”. Training loss sits above
     if the output is too short (brevity penalty). Higher           validation loss for both models because the training split
     scores indicate more exact overlaps and fewer invented         contains systematically longer passages whose input side
     phrases.                                                       is artificially truncated. The parallel trajectories and the
                                                                    absence of sudden divergence argue against over-fitting.
  3. Length ratio: Ratio of output length to reference
     length. A value near 1 means the lengths match.                ROUGE-L and BLEU interpretation (Figure 3): Qual-
                                                                    ity metrics echo the loss picture. BLEU and ROUGE-L
  4. Perplexity (PPL): Model’s average uncertainty per              rise sharply during the first three epochs, plateau around
     token. Lower PPL means more fluent, predictable text.          epoch 5, and stabilise thereafter showing that the optimiser
                                                                    has reached a region of diminishing returns rather than os-
Figure 3 contrasts ROUGE-L and BLEU. Both models                    cillating. Across the entire sweep the proposed model main-
plateau after four epochs, and consistent improvements are          tains a consistent ≈0.02 absolute lead in ROUGE-L and
observed for our proposed model.                                    a ≈0.03 lead in BLEU, validating that its lower loss does
                                                                    translate into better content overlap and n-gram precision.
6.4. Final test performance                                         The fact that BLEU (dashed) improves in lock-step with
                                                                    ROUGE-L (solid) indicates that the gains are not merely
Table 3 summarises the scores on the 250-instance test set          caused by copying longer substrings but by more faithful
(50 queries × 5 documents each).                                    phrasing at finer granularity.
                                                                    Length control efficacy: Prior runs produced ≈ 200-token
        Table 3. Best checkpoint (epoch 7) on the test set.         summaries of inputs that artificially inflated ROUGE-L.
                                                                    After adding a 384-token ceiling, a mild length penalty
Model        ROUGE-L ↑        BLEU ↑      PPL ↓     Len. ratio ≈1
                                                                    (α = 1.1) and “no-repeat 3-gram” blocking, the system de-
Baseline         0.226         0.173       1.71          1.01       livers outputs whose word counts track the reference within
Proposed         0.249         0.200       1.50          1.00       five percent, while still gaining metric points.
                                          Transformer-Based Generative Engine Optimization

7.2. GEO Evaluation                                                 our GEO-tailored model lifts ROUGE-L by +2.3 pp, BLEU
                                                                    by +2.7 pp and reduces perplexity by 12 %, all while hold-
To evaluate the effectiveness of our optimisation strategies,
                                                                    ing the output length within the 5 % corridor. A downstream
we conducted a second-stage model assessment focused on
                                                                    evaluation with Llama-3.3-70B confirms that these textual
website visibility within generative responses. Using our
                                                                    improvements translate into a +30.96 % boost in position-
final test dataset, we employed our fine-tuned BART model
                                                                    adjusted word count, bringing the rewritten pages noticeably
to transform unoptimised website content w into its opti-
                                                                    closer to the “top answer” zone in generative search. Cru-
mised counterpart w’. A subset of 50 evaluation queries was
                                                                    cially, these gains are obtained without retraining a multi-
created from the original set of 250, with each query contain-
                                                                    billion-parameter backbone, without access to proprietary
ing five unoptimised websites and one randomly selected
                                                                    retrieval infrastructure, and on a single commodity GPU -
optimised version. We queried Llama-3.3-70B via API in
                                                                    conditions that mirror the realities of most content publish-
two conditions: (1) using only the five unoptimised sources
                                                                    ers. The study therefore provides concrete evidence that
and (2) randomly replacing one with its optimised version.
                                                                    GEO is tractable with open-source tooling and modest com-
In both scenarios Llama was asked to answer the query
                                                                    pute, offering a practical bridge between academic research
provided only by using information out of these sources
                                                                    and day-to-day digital-marketing needs.
and citing them numerically. Inspired by (Aggarwal et al.,
2024), we assessed visibility changes in the Llama response         However, this work was significantly constrained by limited
from (1) to (2) based on two metrics: absolute word count           computational resources, which influenced model selection
improvement and position-adjusted word count improve-               and training efficiency. Additionally, the novelty of the task
ment. The absolute word count wc is the number of words             introduced further challenges, particularly the absence of
of the source ci in the sentences s of the response r citing        existing labelled datasets suitable for fine-tuning. Syntheti-
ci , mathematically defined as                                      cally constructing a high-quality, domain-specific training
                                                                    dataset at sufficient scale proved non-trivial. Despite system-
                                       X                            atic data generation efforts, issues such as noise, formatting
                     wc(ci , r) =             |s|
                                                                    inconsistencies, and weak alignment between website con-
                                      s∈Sci
                                                                    tent and user queries emerged as limiting factors. These
The position-adjusted wordcount is the same metric, but             imperfections had a measurable impact on model perfor-
weighted by a linear decaying function of the citation posi-        mance during evaluation, particularly in cases where the
tion. Citations that appear earlier in a generative response        relevance of query-content was poor and diminished visibil-
tend to receive greater user attention, so the second metric        ity outcomes.
places more emphasis on these positions (Aggarwal et al.,           Future research can address these limitations by scaling
2024).                                                              dataset generation using more robust scraping and alignment
                                                                    techniques, and evaluating models across other domains.
                                                     
                             X                 pos(s)               Additionally, reinforcement learning could directly optimize
          wcadj (ci , r) =           |s| · 1 −                      for visibility metrics, improving practical performance in
                                                |S|
                             s∈Sci
                                                                    generative search settings. Lastly, future research should
To ensure robustness, we normalised the results and ex-             explore retrieval-augmented generation (RAG) to improve
cluded outliers. Our results show that the model improves           factual grounding in optimised web content.
website visibility by 15.63% based on absolute word count           Overall, this study demonstrates that targeted fine-tuning
and by 30.96% using the position-adjusted word count met-           with domain-specific strategies can meaningfully enhance
ric. This is consistent with results of (Aggarwal et al., 2024),    web content visibility in generative search, even under con-
but faces several limitations. The sample size (n=50) is too        strained resources.
small for statistical significance, Llama’s token constraints
restricted context and response length leading to extreme
values, and noisy data occasionally introduced bias (e.g.
                                                                    9. Statement about individual contributions
poor website-query match).                                          All four group members have worked equally on this project
                                                                    and provided equal parts of work. Two group members
8. Conclusion                                                       have focused on the data generation and preparation side
                                                                    while the two others have focused on researching the right
This work delivers the first end-to-end demonstration that          model to chose and to work with. In the end, tasks consider-
a medium-size sequence-to-sequence transformer, when                ing model creation, fine-tuning, and evaluation have been
lightly fine-tuned on synthetic optimisation pairs, can mea-        worked on by all four members interchangeably.
surably increase a travel website’s visibility inside LLM-
generated answers. Relative to a length-matched baseline,
                                     Transformer-Based Generative Engine Optimization

References                                                       Soper, E., Fujimoto, S., and Yu, Y.-Y. Bart for post-
                                                                   correction of ocr newspaper text. In Proceedings of
Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A.,
                                                                   the 7th Workshop on Noisy User-generated Text (W-
  Narasimhan, K., and Deshpande, A. Geo: Generative
                                                                   NUT 2021), pp. 284–290, 2021. URL https://
  engine optimization. In Proceedings of the 30th ACM
                                                                   aclanthology.org/2021.wnut-1.31/.
 SIGKDD Conference on Knowledge Discovery and Data
 Mining (KDD ’24), pp. 5–16, 2024. URL https://dl.               Tan, S., Lee, C.-P., Lim, K., Tee, C.-R., and Alqahtani,
  acm.org/doi/10.1145/3637528.3671900.                             A. Qarrfsqa: Question-answer replacement and removal
                                                                   pretraining framework for few-shot question answering.
Alokla, A., Gad, W., Nazih, W., Aref, M., and Salem, A.
                                                                   IEEE Access, 2024. URL https://ieeexplore.
  B. M. Pseudocode generation from source code using the
                                                                   ieee.org/document/10737355.
  bart model. Mathematics, 10(21), 2022. URL https:
  //www.mdpi.com/2227-7390/10/21/3967.                           Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones,
                                                                   L., Gomez, A. N., Kaiser, L., and Polosukhin, I. Attention
Amer, E. and Elboghdadly, T. The end of the search engine
                                                                   is all you need, 2023. URL https://arxiv.org/
 era and the rise of generative ai: A paradigm shift in infor-
                                                                   abs/1706.03762.
 mation retrieval. pp. 374–379, 11 2024. URL https://
 ieeexplore.ieee.org/document/10783559.                          Yuniarthe, Y. Application of artificial intelligence (ai) in
                                                                   search engine optimization (seo). In International Con-
Kingma, D. P. and Ba, J. Adam: A method for stochastic op-
                                                                   ference on Soft Computing, Intelligent System and Infor-
  timization, 2017. URL https://arxiv.org/abs/
                                                                   mation Technology, pp. 96–101, 2017. URL https://
  1412.6980.
                                                                   ieeexplore.ieee.org/document/8262550.
Kumar, A. and Lakkaraju, H. Manipulating large language
                                                                 Ziakis, C. and Vlachopoulou, M.        Artificial Intelli-
  models to increase product visibility, 2024. URL https:
                                                                   gence’s Revolutionary Role in Search Engine Optimiza-
 //arxiv.org/abs/2404.07981.
                                                                   tion, pp. 391–399. 2024. ISBN 978-3-031-51037-3.
Lewis, M., Liu, Y., Goyal, N., Ghazvininejad, M., Mo-              URL https://link.springer.com/chapter/
  hamed, A., Levy, O., Stoyanov, V., and Zettlemoyer, L.           10.1007/978-3-031-51038-0_43.
  Bart: Denoising sequence-to-sequence pre-training for
  natural language generation, translation, and comprehen-
  sion. 2019. URL https://arxiv.org/abs/1910.
  13461.

Liu, N. F., Zhang, T., and Liang, P.        Evaluating
  verifiability in generative search engines.   ArXiv,
  2023. URL https://api.semanticscholar.
  org/CorpusID:258212854.

LoDolce, M. and Howley, C. Gartner predicts search engine
  volume will drop 25% by 2026, due to ai chatbots and
  other virtual agents, 2024. URL https://tinyurl.
  com/babb9njm.

Loshchilov, I. and Hutter, F. Sgdr: Stochastic gradi-
  ent descent with warm restarts, 2017. URL https:
  //arxiv.org/abs/1608.03983.

Loshchilov, I. and Hutter, F. Decoupled weight decay regu-
  larization, 2019. URL https://arxiv.org/abs/
  1711.05101.

Menick, J., Trebacz, M., Mikulik, V., Aslanides, J., Song,
 F., Chadwick, M., Glaese, M., Young, S., Campbell-
 Gillingham, L., Irving, G., and McAleese, N. Teaching
 language models to support answers with verified quotes.
 2022. URL https://api.semanticscholar.
 org/CorpusID:247594830.
